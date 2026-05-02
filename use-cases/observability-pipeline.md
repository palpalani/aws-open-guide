# Playbook: Observability pipeline

> Logs, metrics, and traces collected, routed, retained, and queryable — without CloudWatch Logs becoming a five-figure monthly bill.

**Tags:** `production-ready` · `low-cost`

**Status:** ✅ Available

---

## 1. Problem

Every service produces logs, metrics, and traces. The default — ship everything to CloudWatch — works at small scale and breaks at large scale. Ingestion at $0.50/GB plus storage adds up; CloudWatch Logs Insights is fine for hot debugging but expensive for analytics; multi-account aggregation is its own project; and you still want a way to keep 90 days of logs cheap.

This playbook is the routing-and-retention pipeline that sits behind your apps: hot logs in CloudWatch for short-window debugging, warm logs in S3+Athena for analytics and audit, metrics consolidated, traces sampled. Same idea — separate hot and cold paths — applied to operational data.

## 2. Constraints

- **Volume** — GB/day across services; biggest cost driver
- **Hot retention** — minutes-hours where you want CloudWatch Logs Insights speed
- **Warm retention** — days-months for "investigate last month's issue"
- **Cold retention** — months-years for compliance / audit
- **PII / sensitive data** — what's allowed in logs at each tier
- **Multi-account** — one observability account, or per-account, or hybrid
- **Vendor lock-in tolerance** — pure AWS vs Datadog/Grafana/Honeycomb

## 3. Reference architecture

```
┌──────────────────────────────────────────────────────────┐
│  Application services (Lambda, ECS, EC2, RDS, …)          │
│  - structured JSON logs to stdout                         │
│  - EMF metrics in log lines                               │
│  - X-Ray / OTel traces sent to collector                  │
└──────┬─────────────────────────┬──────────────────────────┘
       │                         │
       │ logs                    │ traces
       ▼                         ▼
┌──────────────┐          ┌──────────────┐
│  CloudWatch  │          │  X-Ray /     │
│  Logs        │          │  ADOT        │
│  - hot, 7-30d│          │  collector   │
│  - INSIGHTS  │          └──────┬───────┘
└──────┬───────┘                 │
       │                         │
       │ subscription            │ sample %
       │ filter                  │
       ▼                         ▼
┌──────────────┐          ┌──────────────┐
│  Firehose    │          │  Trace       │
│  - buffer    │          │  storage     │
│  - convert   │          │  (X-Ray or   │
│  - partition │          │   3rd-party) │
└──────┬───────┘          └──────────────┘
       │
       ▼
┌──────────────┐
│      S3      │
│  log lake    │
│  raw/+parquet│
└──────┬───────┘
       │
       ▼
┌──────────────┐    ┌──────────────┐
│   Glue       │───▶│   Athena     │
│   Catalog    │    │  (SQL on     │
│              │    │   logs)      │
└──────────────┘    └──────────────┘

Metrics path:
┌──────────────┐  EMF in log line  ┌──────────────┐
│  Application │──────────────────▶│  CloudWatch  │
│  (Powertools │                   │  Metrics     │
│   logger)    │                   │  (auto-      │
│              │                   │   extracted) │
└──────────────┘                   └──────┬───────┘
                                          │
                                          ▼
                                   ┌──────────────┐
                                   │  CloudWatch  │
                                   │  alarms +    │
                                   │  dashboards  │
                                   └──────────────┘
```

1. **Application** — emits **structured JSON** logs to stdout. Embedded Metric Format (EMF) lines turn into CloudWatch metrics automatically — no separate `PutMetricData` calls. Traces go via OpenTelemetry / X-Ray SDK to a collector.
2. **CloudWatch Logs** — short retention (7–30 days). Used for hot debugging via Logs Insights, alerting on patterns, log-based metric filters.
3. **Subscription filter** — every log group ships to Firehose; Firehose buffers, optionally converts JSON to Parquet, partitions, writes to S3.
4. **S3 log lake** — long retention. Partitioned by `service/event_date/`. Glue catalog + Athena for SQL queries. Lifecycle to Glacier after warm window if compliance demands long retention.
5. **Traces** — X-Ray for AWS-native; OpenTelemetry → AWS Distro for OpenTelemetry (ADOT) for portability.
6. **Metrics** — EMF for application metrics; CloudWatch native for AWS service metrics; consolidated via **Cross-Account Observability** in a single observability account.

## 4. Architecture variants

| Variant | When | Notes |
|---------|------|-------|
| **CloudWatch only** | Small scale, single account | Simplest; expensive past ~100 GB/day logs |
| **CloudWatch hot + S3 cold (this playbook)** | Default at scale | Cheap warm/cold path, hot kept short |
| **Direct to S3 + ADOT** | Skip CloudWatch entirely | Cheapest; lose Logs Insights and metric extraction; not recommended |
| **CloudWatch + Datadog/Grafana/Honeycomb** | UX over cost | Vendor cost; richer dashboards and tracing UX |
| **OpenSearch ingestion** | Full-text search + dashboards | Replaces Athena for hot queries; OpenSearch storage cost |
| **Cross-Account Observability hub** | Multi-account org | Single observability account aggregates many |
| **Tail sampling at ADOT collector** | High-volume tracing | Keep error/slow traces, drop the rest |

## 5. Failure modes

Cross-cutting patterns: see [`failure-first.md`](failure-first.md). Observability-pipeline-specific:

### Subscription filter falls behind

- **What it looks like** — S3 log lake stops receiving recent data; Firehose `IncomingBytes` flat
- **Why it happens** — log volume spike beyond Firehose throughput; Firehose error to S3
- **Recovery** — alarm on Firehose `DeliveryToS3.DataFreshness`; raise Firehose throughput limits; Firehose error backup destination configured

### CloudWatch ingestion costs spike

- **What it looks like** — bill jumps; one log group dominates
- **Why it happens** — log level dialed to DEBUG in production; new chatty service deployed; runaway Lambda logging on every invocation
- **Recovery** — CloudWatch Contributor Insights to find top talkers; per-log-group ingestion alarms; log-level guardrails in CI; reduce retention if appropriate

### Logs without context can't be correlated

- **What it looks like** — multi-service incident; can't trace a request across services
- **Why it happens** — missing `request_id` / trace context propagation
- **Recovery** — middleware enforces context propagation; logs always include `request_id`, `tenant_id` (multi-tenant), trace IDs; auto-instrument with ADOT

### Sensitive data in logs

- **What it looks like** — PII, secrets, PCI data in CloudWatch and S3
- **Why it happens** — exception with full request body, debug log of headers, stacktrace with credentials
- **Recovery** — Macie scans S3 log lake; CloudWatch Logs data protection policies (managed PII detection + masking); never log full request body or headers; structured logger with field allow-list

### Trace sampling miss

- **What it looks like** — error happened, no trace exists
- **Why it happens** — head-based sampling at low rate dropped this trace
- **Recovery** — tail-based sampling at the collector — keep all error traces and a sample of successes; or always-sample errors via context propagation

### Athena log queries slow / expensive

- **What it looks like** — Athena queries take minutes; bill grows
- **Why it happens** — partition not matched in WHERE clause; querying raw JSON
- **Recovery** — partition projection; require date predicate via Athena workgroup query restrictions; convert JSON to Parquet at Firehose

### Cross-account observability blind spots

- **What it looks like** — production account fine; staging account "where are the logs?"
- **Why it happens** — observability hub access not configured
- **Recovery** — Cross-Account Observability monitoring account; sharing every account by default

## 6. Cost model

Worked example: 50 services, 200 GB/day total logs, 10M traces/day, EMF metrics, 30-day hot + 90-day warm retention.

| Line item | Monthly | Notes |
|-----------|---------|-------|
| CloudWatch Logs ingestion (200 GB/day × 30d) | ~$3,000 | $0.50/GB; biggest line |
| CloudWatch Logs storage (6 TB at 30d retention) | ~$200 | $0.03/GB-month |
| CloudWatch Logs Insights queries (50 GB/day scanned) | ~$8 | $0.005/GB |
| Firehose (200 GB/day) | ~$170 | $0.029/GB after first 500 GB |
| Firehose Parquet conversion | ~$110 | $0.018/GB |
| S3 storage (Parquet 90d, ~6 TB compressed) | ~$140 | $0.023/GB-month |
| Athena queries (1 TB scanned/month, partitioned) | ~$5 | $5/TB |
| Glue Crawler (or partition projection) | ~$10 | If crawler |
| EMF metrics (~10M custom metrics generated) | ~$300 | $0.30/metric/month above free tier |
| X-Ray traces (10M/day, 100% recorded, 10% sampled) | ~$150 | $5/M traces |
| **Total** | **~$4,090** | |

**Without the S3 path** (everything in CloudWatch with 90d retention): roughly **$5,500+/mo** because storage adds up.
**With aggressive cuts** (sampling, log-level discipline, EMF for metrics, S3 for warm path): **~$2,500/mo**.

The **S3 cold path is the biggest cost lever**: every GB-day in S3 instead of CloudWatch saves ~94% storage cost and unlocks cheap analytics.

**Cost traps:**
- **Default-forever log retention** — set per-log-group retention; un-tagged groups auto-default
- **Logging full request/response bodies** — bandwidth + ingestion + privacy issue
- **Custom metric per request with high cardinality dimensions** — see [`anti-patterns.md`](anti-patterns.md#metric-per-request-without-dimension-hygiene)
- **CloudTrail to CloudWatch Logs** — CloudTrail volume can be huge; ship to S3 only unless you need real-time detection
- **VPC Flow Logs to CloudWatch Logs** — same; S3 destination is much cheaper

## 7. When NOT to use this

- **Tiny system, single service** — CloudWatch alone is fine; pipeline is overhead
- **Strict compliance forbidding cross-region log replication** — verify region setup
- **You already pay for Datadog / New Relic / Splunk** — pipeline duplication; pick a shipping path and avoid double-pay
- **Real-time security alerting on every log** — pair with GuardDuty / Security Hub; pipelines are batch by nature

## 8. Alternatives

| Approach | Best for | Tradeoff |
|----------|----------|----------|
| **CloudWatch + S3 + Athena (this playbook)** | AWS-native, cost-conscious | DIY UX; CloudWatch dashboards aren't the prettiest |
| **Datadog / New Relic / Splunk** | UX, productivity, integrations | Vendor cost; egress to ship logs out |
| **Grafana Cloud / self-hosted Grafana** | Open ecosystem, dashboards | Self-host or pay; flexible |
| **Honeycomb** | Tracing-first observability | Strong tracing UX; fewer logs features |
| **OpenSearch + Dashboards** | Full-text + viz on AWS | OpenSearch storage cost; ops |
| **Loki + Tempo + Mimir** | OSS observability stack | Self-host complexity |

## 9. Anti-patterns

- **Logs as freeform strings** — can't query; structured JSON always
- **No retention policy** — bill grows monthly forever
- **Log-everything DEBUG in production** — sample debug, never on by default
- **Custom metric per (user, request)** — high-cardinality kills CloudWatch Metrics; use EMF for high-cardinality fields kept in logs, not metrics
- **CloudTrail and VPC Flow Logs to CloudWatch Logs** — both volumes are huge; ship to S3
- **Single log group for all services** — can't apply per-service retention; can't tell who's noisy
- **No request ID propagation** — every cross-service debug becomes archaeology
- **Logs include secrets / PII** — log redaction in formatters; never log full request body
- **Health-check logs at INFO** — every 30s × every target × every service drowns the signal
- **No alarm on log ingestion bytes** — first runaway logger ships before bill arrives
- **Trace sampling 100% in production** — at high QPS, trace storage dwarfs everything; sample with floor (always errors, % of successes)
- **Building dashboards before logging discipline** — beautiful dashboards on bad data don't help

For cross-cutting AWS anti-patterns, see [`anti-patterns.md`](anti-patterns.md).

## 10. Production checklist

- [ ] **Structured JSON logs** with standard fields: `timestamp`, `level`, `service`, `request_id`, `tenant_id` (if multi-tenant), `trace_id`
- [ ] **Per-log-group retention** explicitly set (7–30 days hot)
- [ ] **Subscription filter → Firehose → S3** for every business-relevant log group
- [ ] **Firehose** with 60s/5MB buffer, Parquet conversion, partitioned by `service/event_date/`
- [ ] **Glue partition projection** (or scheduled crawler) for Athena access
- [ ] **EMF for application metrics** — no separate `PutMetricData` calls except for cross-cutting concerns
- [ ] **High-cardinality fields in logs**, low-cardinality in metric dimensions
- [ ] **Log redaction / data protection** policies on PII fields
- [ ] **Macie** scanning the log lake for accidental PII
- [ ] **Trace sampling** at collector — 100% errors, sampled successes
- [ ] **Trace context propagation** instrumented in every cross-service call
- [ ] **Cross-Account Observability** if multi-account
- [ ] **Per-log-group ingestion alarms**; alarm on `IncomingBytes` anomalies
- [ ] **CloudWatch alarms** on the right SLIs (error rate, p99 latency, saturation) — not on log lines
- [ ] **Athena workgroup** with bytes-scanned limit
- [ ] **Cost dashboards** broken down by service / log group / team
- [ ] **VPC Flow Logs and CloudTrail** to S3, not CloudWatch (unless real-time need is documented)
- [ ] **Runbook** for incident: "where do I look first" — logs, metrics, traces, dashboards in one playbook
- [ ] **Drill** — pick a past incident; see if current observability would have caught it faster

## 11. References

**Official:**
- [CloudWatch Documentation](https://docs.aws.amazon.com/cloudwatch/) — full guide
- [CloudWatch Logs Insights](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/AnalyzingLogData.html) — query language
- [CloudWatch Embedded Metric Format (EMF)](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Embedded_Metric_Format_Specification.html) — high-cardinality metrics
- [CloudWatch Cross-Account Observability](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Unified-Cross-Account.html) — multi-account
- [CloudWatch Logs Data Protection](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/mask-sensitive-log-data.html) — PII masking
- [CloudWatch Logs subscription filters](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/Subscriptions.html) — Firehose / Lambda / Kinesis
- [AWS X-Ray Documentation](https://docs.aws.amazon.com/xray/) — tracing [maintenance]
- [AWS Distro for OpenTelemetry (ADOT)](https://aws-otel.github.io/) — OpenTelemetry on AWS
- [Amazon Macie](https://docs.aws.amazon.com/macie/) — PII discovery in S3

**Production guides:**
- [How to build serverless data pipeline — Glue + Athena](https://www.factualminds.com/blog/how-to-build-serverless-data-pipeline-glue-athena/) — same pattern, applied to logs
- [Building a data lake on S3 + Glue + Athena](https://www.factualminds.com/blog/building-a-data-lake-on-aws-s3-glue-athena-architecture/) — log-lake foundations

**OSS tools:**
- [aws-lambda-powertools-python](https://github.com/aws-powertools/powertools-lambda-python) — structured logging, metrics, tracing
- [aws-lambda-powertools-typescript](https://github.com/aws-powertools/powertools-lambda-typescript) — same for Node.js
- [OpenTelemetry Collector](https://github.com/open-telemetry/opentelemetry-collector) — vendor-neutral collector
- [Vector](https://github.com/vectordotdev/vector) — log shipper alternative
- [Fluent Bit](https://github.com/fluent/fluent-bit) — lightweight log forwarder
- [duckdb](https://github.com/duckdb/duckdb) — query Parquet logs locally during development

---

*See also: [`real-time-analytics.md`](real-time-analytics.md) · [`cost-pitfalls.md`](cost-pitfalls.md) · [`anti-patterns.md`](anti-patterns.md) · [Bill teardowns and FinOps in root README](../README.md#cost-management--finops).*
