# Playbook: Real-time analytics pipeline

> Stream of events (clickstream, IoT, app telemetry) processed in seconds for hot dashboards, archived to S3 for cold queries with Athena.

**Tags:** `production-ready` · `high-scale`

**Status:** ✅ Available

---

## 1. Problem

Events arrive continuously: page views, button clicks, IoT sensor readings, transaction logs. Two consumers want different things:
- **Real-time** dashboard wants to see "last 5 minutes" within seconds (sub-minute freshness, small windows)
- **Analytics / ML / BI** wants to query "last 30 days" cheaply (high-latency tolerance, large scans)

The pattern below is the **lambda architecture** done with AWS-managed services: a hot path for low-latency aggregations and a cold path for cheap historical queries, both fed from the same source stream.

## 2. Constraints

- **Event volume** — events/sec; affects Kinesis shard count, Firehose throughput
- **Event size** — bytes/event; affects bandwidth and storage
- **Hot-path latency target** — typically 10s–60s end-to-end
- **Cold-path query latency** — typically seconds-to-minutes for ad-hoc analytics
- **Retention** — hot (minutes-hours), cold (months-years)
- **Schema evolution** — fields will be added, renamed; pipeline must tolerate
- **Dedup / ordering** — usually approximate is fine; if exact, design for it

## 3. Reference architecture

```
┌────────────┐   PutRecords   ┌─────────────────────┐
│  Producer  │───────────────▶│  Kinesis Data       │
│ (web app,  │                │  Streams            │
│  mobile,   │                │  (sharded, 24h-365d │
│  IoT,      │                │   retention)        │
│  backend)  │                └─────┬───────────┬───┘
└────────────┘                      │           │
                                    │           │
                       hot path     │           │   cold path
                        ▼           │           │   ▼
            ┌────────────────────┐  │           │  ┌──────────────────┐
            │  Lambda or Flink   │◀─┘           └─▶│ Kinesis Firehose │
            │  (windowed agg,    │                 │  - buffer 60s/5MB│
            │   filter, alert)   │                 │  - convert to    │
            └─────────┬──────────┘                 │    Parquet       │
                      │                            │  - partition by  │
                      ▼                            │    event_date    │
            ┌────────────────────┐                 └────────┬─────────┘
            │   ElastiCache /    │                          │
            │   DynamoDB         │                          ▼
            │   (latest counts,  │                 ┌──────────────────┐
            │    rolling p99)    │                 │       S3         │
            └─────────┬──────────┘                 │   data lake      │
                      │                            │   raw/, parquet/ │
                      ▼                            └────────┬─────────┘
            ┌────────────────────┐                          │
            │   Real-time API /  │                          ▼
            │   WebSocket /      │                 ┌──────────────────┐
            │   AppSync sub      │                 │   Glue Catalog   │
            └────────────────────┘                 │   (table schemas)│
                                                   └────────┬─────────┘
                                                            │
                                                            ▼
                                                   ┌──────────────────┐
                                                   │     Athena       │
                                                   │  (ad-hoc SQL)    │
                                                   └────────┬─────────┘
                                                            │
                                                            ▼
                                                   ┌──────────────────┐
                                                   │  QuickSight /    │
                                                   │  Redshift /      │
                                                   │  Snowflake / BI  │
                                                   └──────────────────┘
```

1. **Producer** — every event source writes to one Kinesis Data Stream (`PutRecords` for batched writes; partition key spreads across shards).
2. **Hot path** — Lambda (or Managed Service for Apache Flink for stateful windowing) consumes from the stream. Computes rolling aggregates (last 5 min counts, p99 latency, error rate). Writes summaries to ElastiCache or DynamoDB. A real-time API or WebSocket pushes updates to dashboards.
3. **Cold path** — Kinesis Firehose subscribes to the same stream, buffers for 60s/5MB, converts JSON to Parquet via inline conversion, partitions by date, writes to S3.
4. **Catalog** — Glue Crawler builds and updates table schemas in the Glue Data Catalog. Athena queries via the catalog.
5. **BI** — Athena or QuickSight for ad-hoc; Redshift or Snowflake if higher concurrency or complex joins are needed.

For sustained gigabyte-per-second-class workloads, replace Kinesis + Firehose with **MSK + Flink + S3 sink** if Kafka familiarity is in-house.

## 4. Architecture variants

| Variant | When | Notes |
|---------|------|-------|
| **Kinesis + Lambda + Firehose** | Default; up to ~10 MB/s/shard | Most teams should start here |
| **Kinesis + Managed Flink + Firehose** | Stateful windows, joins, exactly-once | Flink for complex stream processing |
| **MSK (Kafka) + Flink + S3** | Existing Kafka, multi-cloud, complex topologies | More features; more ops |
| **Direct PutObject to S3 (mini-batch)** | Low volume, no real-time need | Simpler; loses real-time capability |
| **Kinesis Data Firehose direct (no streaming consumer)** | Cold path only, no real-time | Cheapest; just an S3 ingestion pipe |
| **EventBridge + Pipes + Firehose** | Event-driven sources, lower volume | When events come from EventBridge already |
| **OpenSearch ingestion** | Full-text + dashboards | Replace Athena with OpenSearch for hot queries |

## 5. Failure modes

Cross-cutting patterns: see [`failure-first.md`](failure-first.md). Real-time-pipeline-specific:

### Producer drops events on retry exhaustion

- **What it looks like** — gaps in the stream; counts off vs source-of-truth
- **Why it happens** — `PutRecord` 5xx, retry budget exhausted, app crash mid-batch
- **Recovery** — Kinesis Producer Library (KPL) handles retries; producer-side WAL or local buffer; reconcile counts daily against source

### Shard hot-spotting

- **What it looks like** — one shard at 100% utilisation, others idle; throttling on writes
- **Why it happens** — partition key not high-cardinality enough (e.g., `country` when 90% of users in one country)
- **Recovery** — partition key with high cardinality (user ID, request ID); add a salt for known-skewed keys

### Consumer lag

- **What it looks like** — `IteratorAge` metric grows; data is hours behind real-time
- **Why it happens** — consumer too slow, downstream throttling, expensive computation per record
- **Recovery** — increase consumer concurrency (more Lambda concurrency, or Flink parallelism); profile per-record cost; downstream batching; checkpoint Flink more efficiently

### Late-arriving events

- **What it looks like** — events with timestamps from minutes-to-hours ago
- **Why it happens** — mobile clients with offline buffers; queued at producer
- **Recovery** — windowing in hot path uses **event time**, not processing time; allowed lateness configured (Flink) or watermark-based; cold path partitions by event_date so late events land in correct partition

### Schema drift breaks Athena

- **What it looks like** — Athena query fails after a producer change
- **Why it happens** — added field of incompatible type; renamed column
- **Recovery** — Glue schema registry with strict mode; backwards-compatible-only changes; Parquet handles added columns gracefully if downstream uses column names; use Iceberg or Delta Lake for schema evolution at table level

### S3 small-object explosion

- **What it looks like** — millions of small Parquet files; Athena queries slow; PUT cost spirals
- **Why it happens** — Firehose buffer too small; high partition cardinality
- **Recovery** — Firehose buffer 60s/5MB minimum; periodic compaction job (Glue or Athena CTAS) merges small files; partition only by date (or date+hour at high volume)

### Cost runaway via Athena

- **What it looks like** — bill explodes; team complains "queries are slow"
- **Why it happens** — full-table scans, missing partition predicates, querying raw JSON instead of Parquet
- **Recovery** — workgroup query limits; partition projection; Parquet compression; teach team to always include date predicates; CloudWatch alarm on Athena scanned-bytes

### Replay required

- **What it looks like** — bug downstream; need to reprocess last 24h
- **Recovery** — Kinesis retention covers replay window; Firehose archive in S3 covers longer; reprocess from S3 with Glue/EMR job into a new partition or table version

## 6. Cost model

Worked example: 10k events/sec average (~26B/month), 1KB events, hot + cold paths.

| Line item | Monthly | Notes |
|-----------|---------|-------|
| Kinesis Data Streams (10 shards) | ~$110 | $0.015/shard-hour + PUT cost |
| Kinesis PUT payload | ~$390 | $0.014 per 1M records (1KB units) at 26B records |
| Lambda hot consumer (10 shards × 24h × $X) | ~$200 | Depends on processing per record |
| Firehose ingestion | ~$760 | $0.029/GB after first 500 GB; ~26TB |
| Firehose Parquet conversion | ~$50 | $0.018/GB |
| S3 storage (Parquet, ~5TB compressed, 90d) | ~$115 | $0.023/GB/month |
| S3 PUT (Firehose batches; few hundred per day) | ~$1 | Marginal |
| Glue Crawler (daily run) | ~$5 | Per-DPU pricing |
| Athena queries (1TB scanned/day, partitioned) | ~$150 | $5/TB; partitioning critical |
| ElastiCache for hot summaries | ~$200 | cache.m6g.large × 2 |
| **Total** | **~$1,990** | ~$0.077 per 1M events |

**Scaling shape:** Kinesis is sub-linear (shards added in steps); Firehose scales linearly; S3 scales linearly. Athena cost is **query-driven, not data-driven** — partitioning is the biggest cost lever.

**Cost traps:**
- **Over-provisioned Kinesis shards** — `OnDemand` mode auto-scales but at premium; pick provisioned + scaling rules for steady workloads
- **No partitioning on S3** — Athena scans everything; bill explodes
- **Storing JSON not Parquet** — Athena scans 5–10× more bytes; Firehose Parquet conversion pays for itself fast
- **Daily Glue Crawler on huge dataset** — partition projection often replaces crawler entirely
- **Hot-path Lambda doing too much** — push compute to Flink for stateful, push aggregation to materialised views in Redshift / Snowflake

## 7. When NOT to use this

- **Low event volume (<100/sec)** — overkill; direct PutObject to S3 + Glue + Athena is simpler
- **Strict exactly-once + ordered** end-to-end — Kafka with idempotent producer + transactional consumer is cleaner
- **Sub-second freshness for high-volume** — push to in-memory only (ElastiCache, MemoryDB); skip Firehose
- **Simple metric monitoring** — CloudWatch metrics + Embedded Metric Format is the right tool; don't build a pipeline for what CloudWatch does

## 8. Alternatives

| Approach | Best for | Tradeoff |
|----------|----------|----------|
| **Kinesis + Lambda + Firehose + Athena (this playbook)** | Default | Many moving parts |
| **MSK (Kafka) + Flink + S3** | Existing Kafka, complex topology | Operationally heavier |
| **Snowflake Snowpipe + Streams** | Already in Snowflake | Cross-cloud egress; no AWS lock-in either |
| **OpenSearch Ingestion + Dashboards** | Full-text + dashboards together | Cost grows with data |
| **Timestream LiveAnalytics** [maintenance] | Time-series specific | In maintenance per AWS lifecycle; pick alternative |
| **InfluxDB on AWS / TimescaleDB** | Time-series with SQL | Self-managed or partner-managed |
| **Datadog / Honeycomb / etc.** | Operational telemetry | Vendor cost; faster to ship |

## 9. Anti-patterns

- **One shard for everything** — Kinesis hot-spots immediately; partition key planning matters
- **Partition key = constant** — single shard receives all writes
- **No retention buffer** — set Kinesis retention to ≥24h so consumer downtime ≤24h is recoverable without replay
- **Storing JSON in S3 long-term** — 5–10× more storage and Athena scan cost than Parquet
- **No partitioning on S3** — Athena scans entire dataset for every query
- **Partition cardinality too high** — `partition by user_id` creates millions of partitions; query planner suffers
- **Same Lambda for hot path + cold path** — different scaling and cost characteristics; keep paths separate
- **Long-running Lambda hot consumer** — cold start penalty per shard; reserved concurrency or Flink for stable workloads
- **Athena workgroup without query bytes limit** — first runaway query is expensive
- **Hot-path aggregations stored in DynamoDB without TTL** — table grows forever
- **No replay path tested** — first time you need it, it's during an incident
- **Aggregations recomputed from raw data on each query** — pre-aggregate into materialised views or Redshift / Snowflake tables for repeated queries

For cross-cutting AWS anti-patterns, see [`anti-patterns.md`](anti-patterns.md).

## 10. Production checklist

- [ ] **Partition key** is high-cardinality and well-distributed; verified with shard utilisation metrics
- [ ] **Kinesis retention** ≥24h (≥7d if downstream reliability is uncertain)
- [ ] **Producer uses KPL** or batched `PutRecords` for efficiency
- [ ] **Producer-side buffer / WAL** for events that must not be lost on producer crash
- [ ] **Consumer concurrency** sized; `IteratorAge` alarmed
- [ ] **Hot path windows use event time** with bounded lateness
- [ ] **Firehose buffer** 60s/5MB or larger; Parquet conversion enabled; partitioned by date
- [ ] **Glue Catalog** updated by partition projection (preferred) or scheduled crawler
- [ ] **Athena workgroup** query bytes limit + alarm
- [ ] **CloudWatch alarms** — `IteratorAge`, write throttles, Firehose delivery failures, Athena scanned-bytes
- [ ] **DLQ** on hot consumer; reprocess runbook
- [ ] **Schema registry** with strict mode; CI checks for compatibility
- [ ] **Compaction job** for small-file problem (weekly Glue or Athena CTAS)
- [ ] **Cost alarms** at multiple thresholds; Athena cost broken down by workgroup / user
- [ ] **Replay tested** — reprocess 1 day of data into a side table
- [ ] **Late-arriving event handling** documented; reconciliation job daily
- [ ] **Egress / cross-region** audited if multi-region

## 11. References

**Official:**
- [Kinesis Data Streams Documentation](https://docs.aws.amazon.com/streams/) — full guide
- [Kinesis Data Firehose Documentation](https://docs.aws.amazon.com/firehose/) — managed delivery
- [Firehose Parquet conversion](https://docs.aws.amazon.com/firehose/latest/dev/record-format-conversion.html) — record format conversion
- [Managed Service for Apache Flink](https://docs.aws.amazon.com/managed-flink/) — stateful stream processing
- [AWS Glue Data Catalog](https://docs.aws.amazon.com/glue/latest/dg/components-overview.html) — schema catalog
- [Athena partition projection](https://docs.aws.amazon.com/athena/latest/ug/partition-projection.html) — partitioning without crawlers
- [Apache Iceberg on AWS](https://docs.aws.amazon.com/AmazonS3/latest/userguide/querying-iceberg.html) — schema evolution at table level
- [Lake Formation](https://docs.aws.amazon.com/lake-formation/) — access control on data lake
- [QuickSight Documentation](https://docs.aws.amazon.com/quicksight/) — BI on Athena / Redshift
- [Real-time pipeline reference architecture](https://docs.aws.amazon.com/whitepapers/latest/streaming-data-solutions-amazon-kinesis/streaming-data-solutions-amazon-kinesis.html) — official whitepaper

**Production guides:**
- [Real-time pipeline — Kinesis + Lambda + DynamoDB](https://www.factualminds.com/blog/real-time-data-pipeline-kinesis-lambda-dynamodb/) — production walkthrough
- [Building a data lake on S3 + Glue + Athena](https://www.factualminds.com/blog/building-a-data-lake-on-aws-s3-glue-athena-architecture/) — cold-path deep dive
- [Build a serverless data pipeline — Glue + Athena](https://www.factualminds.com/blog/how-to-build-serverless-data-pipeline-glue-athena/) — Glue/Athena patterns
- [Glue 5 + Apache Iceberg — modern ETL](https://www.factualminds.com/blog/aws-glue-5-apache-iceberg-modern-etl/) — Iceberg on AWS

**Decision guides:**
- [Which AWS database](https://www.factualminds.com/decide/which-aws-database/) — for query-side store
- [Step Functions vs EventBridge](https://www.factualminds.com/compare/aws-step-functions-vs-eventbridge/) — orchestration choices

**OSS tools:**
- [aws-kinesis-aggregation](https://github.com/awslabs/kinesis-aggregation) — Kinesis Producer Library aggregation
- [Kinesis Client Library (KCL)](https://github.com/awslabs/amazon-kinesis-client) — checkpointing consumer
- [PyAthena](https://github.com/laughingman7743/PyAthena) — Athena driver for Python
- [duckdb](https://github.com/duckdb/duckdb) — local Parquet querying for development

---

*See also: [`event-driven.md`](event-driven.md) · [`observability-pipeline.md`](observability-pipeline.md) · [`cost-pitfalls.md`](cost-pitfalls.md) · [`decision-trees.md`](decision-trees.md#event-processing--what-runs-in-response-to-an-event).*
