# Playbook: Event-driven processing

> Domain events flowing across services with schemas, routing, replay, and a recovery story when a downstream is broken.

**Tags:** `production-ready` · `high-scale`

**Status:** ✅ Available

---

## 1. Problem

Service A does something interesting (`order_placed`, `user_signed_up`, `file_uploaded`). Services B, C, and D care. The naïve solution — A calls B, C, and D directly — couples them together. Adding service E means changing service A. A bug in B retries forever. The org grows; coupling decays.

Event-driven flips it: A emits an event to a bus. B, C, D, and future E subscribe. A doesn't know who's listening. Each subscriber controls its own retries, idempotency, error handling. The bus is the contract.

This playbook is the AWS-native version of that pattern — schemas, routing, archive, replay, DLQs — without the operational pain of running Kafka.

## 2. Constraints

- **Event volume** — 1/sec to 100k/sec; affects bus choice (EventBridge vs Kinesis)
- **Ordering requirements** — usually not needed; if needed, partition explicitly
- **Latency** — event to subscriber typically <1s for EventBridge; <100ms for SNS direct
- **Replay window** — debugging needs replay; how far back? (EventBridge archive supports up to indefinite)
- **Schema evolution** — events live forever; backwards-compatible changes only after launch
- **Cross-account / cross-region** — common in mature orgs; affects routing setup
- **Cost ceiling** — high event volumes get expensive on EventBridge; consider hybrid

## 3. Reference architecture

```
┌────────────┐   PutEvents   ┌─────────────────────────────┐
│ Producer A │──────────────▶│        EventBridge          │
│ (order     │               │   custom event bus          │
│  service)  │               │                             │
└────────────┘               │  ┌──────────────────────┐   │
                             │  │  Schema Registry     │   │
                             │  │  (versioned)         │   │
                             │  └──────────────────────┘   │
                             │                             │
                             │  ┌──────────────────────┐   │
                             │  │  Archive             │   │
                             │  │  (replay window)     │   │
                             │  └──────────────────────┘   │
                             │                             │
                             │  ┌──────────────────────┐   │
                             │  │  Rules               │   │
                             │  │  (pattern → target)  │   │
                             │  └─────────┬────────────┘   │
                             └────────────┼────────────────┘
                                          │
              ┌───────────────────────────┼───────────────────────────┐
              │                           │                           │
              ▼                           ▼                           ▼
       ┌──────────────┐           ┌──────────────┐           ┌──────────────┐
       │   SQS queue  │           │   Lambda     │           │  HTTP target │
       │      ↓       │           │  (subscriber │           │ (API dest.   │
       │   Subscriber │           │   B)         │           │  signed,     │
       │   ECS / Lambda│           │              │           │  retry)      │
       │      ↓       │           │      ↓       │           │      ↓       │
       │     DLQ      │           │     DLQ      │           │     DLQ      │
       └──────────────┘           └──────────────┘           └──────────────┘
```

1. **Producer** — emits to a custom event bus via `PutEvents` (10 events per call max). Schema registry enforces structure.
2. **EventBridge** — routes events based on **rules** that match against the event JSON. Each rule has 1+ targets. Failed deliveries to a target go to that target's DLQ.
3. **Archive** — every event landing on the bus can be archived; replay an archive into the bus to reprocess history.
4. **Subscribers** — Lambda for in-process work, SQS+worker when subscriber needs durable buffering and slower drain, API destinations for cross-system HTTP webhooks (signed, with retries).
5. **DLQ per target** — when EventBridge can't deliver to a target after retries, it puts the event on the target's DLQ. Each subscriber owns its DLQ runbook.

The pattern: **subscribers always pull from a queue, not directly from the bus**, when the work has any chance of being slow or unreliable. The queue is your buffer and your DLQ source.

## 4. Architecture variants

| Variant | When | Notes |
|---------|------|-------|
| **EventBridge default bus → Lambda** | Cross-AWS-service events | Default for AWS-source events (S3, EC2 state changes) |
| **EventBridge custom bus → Lambda** | Domain events between your services | Default starting point |
| **EventBridge → SQS → worker** | Subscriber needs durable buffering | Most production patterns; isolates subscriber pace |
| **SNS → SQS fan-out** | Pub/sub without routing complexity | Cheaper than EventBridge at high volume; no schema registry |
| **EventBridge Pipes** | Filter / enrich / transform between source and target | Lower-code; replaces a chain of Lambdas |
| **Kinesis Data Streams** | High throughput, ordered, replayable | When EventBridge cost/throughput ceiling matters |
| **MSK / Kafka** | Existing Kafka investment, complex topologies | More features, more ops |
| **EventBridge cross-account** | Multi-account org architecture | Resource policies + bus permissions |

## 5. Failure modes

Cross-cutting patterns: see [`failure-first.md`](failure-first.md). Event-driven-specific:

### Subscriber broken; events accumulate

- **What it looks like** — DLQ depth growing on one subscriber while others process fine
- **Why it happens** — code bug, downstream dependency outage, schema drift the subscriber didn't handle
- **Detection** — DLQ alarm; subscriber error rate alarm
- **Recovery** — fix subscriber, redrive DLQ events; **other subscribers are unaffected** — that's the whole point of pub/sub

### Schema drift breaks subscribers

- **What it looks like** — producer adds/changes a field; one subscriber 500s on every event
- **Why it happens** — no schema registry, or registry not enforced; backwards-incompatible change
- **Recovery** — Schema Registry with strict mode; backwards-compatible-only changes (add optional fields, never rename or remove); version the event type (`order_placed.v1`, `order_placed.v2`) for breaking changes

### Event lost (producer side)

- **What it looks like** — subscribers never see an event they should have
- **Why it happens** — producer's `PutEvents` failed and wasn't retried; producer crashed before publish
- **Recovery** — outbox pattern: producer writes event to its own DB transactionally with the business change; separate process publishes from outbox to EventBridge; on failure, retry from outbox

### Duplicate events

- **What it looks like** — subscriber processes the same event twice
- **Why it happens** — EventBridge guarantees at-least-once; producer retried after timeout; outbox publisher republished
- **Recovery** — every event has an `event_id`; subscribers idempotency-key on it (DynamoDB conditional write); see [`failure-first.md`](failure-first.md#2-idempotency)

### Replay storm during recovery

- **What it looks like** — replaying an archive floods subscribers; downstream APIs throttle; cascading failure
- **Why it happens** — full-speed replay of hours of events
- **Recovery** — replay with rate limit; use Step Functions for paced replay; staging replay in non-prod first

### Cross-account routing fails silently

- **What it looks like** — events emitted, archived, but no subscriber sees them
- **Why it happens** — missing bus resource policy, missing IAM permission on target account
- **Recovery** — EventBridge CloudWatch metrics show failed invocations; verify resource policy on bus + IAM trust on target

### Event bus throttled

- **What it looks like** — `PutEvents` returns errors at high volume
- **Why it happens** — EventBridge has account-level limits (PutEvents throttle, target invocation rate)
- **Recovery** — request quota increase; for sustained high volume, consider Kinesis or sharding across multiple buses

## 6. Cost model

EventBridge pricing: $1.00 per 1M custom events + $0.64 per 1M cross-region or schema-discovered events. Targets pay their own costs.

Worked example: 100M events/month, 3 subscribers per event.

| Line item | Monthly | Notes |
|-----------|---------|-------|
| EventBridge custom events | $100 | 100M × $1/M |
| Schema Registry | ~$1 | Pay only for discovery enabled |
| Archive (storage) | ~$10 | $0.10/GB; ~10 GB at 100M small events |
| Replay (when used) | $0 + targets | Replays free, target costs apply |
| Lambda subscriber (3 × 100M × 200ms × 256MB) | ~$300 | Subscriber compute dominates |
| SQS for buffered subs | ~$40 | $0.40/M requests × poll volume |
| DLQ + alarms | ~$1 | Marginal |
| **Total** | **~$450** | ~$0.0045 per event delivered to 3 subs |

**Scaling shape:** linear with events × subscribers for compute; linear with events for the bus. Big lever: **filter aggressively in rules** so subscribers don't pay to process events they don't care about.

**Cost traps:**
- **Subscribing the same Lambda to many narrow rules** instead of one rule with broader pattern — duplicate invocations
- **Archive of all events forever** — storage grows unboundedly; set retention
- **High-volume events on EventBridge** — at >100k events/sec, Kinesis is cheaper
- **Schema discovery on production** — $1/M discovered events on top; turn off after schemas stable

## 7. When NOT to use this

- **Tightly coupled request-response** — sync HTTP is fine; events add complexity for no benefit
- **Strict ordering across all events** — EventBridge is unordered; use Kinesis with partitioning, or FIFO SQS, or Kafka
- **Sub-millisecond latency** — EventBridge has tens-of-milliseconds latency; for HFT-style needs use Kinesis or direct invocation
- **Tiny system, single team** — don't pay the complexity tax until you have >1 producer/consumer team or events that need replay

## 8. Alternatives

| Approach | Best for | Tradeoff |
|----------|----------|----------|
| **EventBridge (this playbook)** | AWS-native domain events | Pay per event; account-level limits |
| **SNS + SQS fan-out** | Simple pub/sub at high volume | No schema registry, no archive/replay |
| **Kinesis Data Streams** | Ordered, replayable, high-volume | Shard management; consumers track position |
| **MSK (managed Kafka)** | Multi-cloud, complex stream topologies | Most features; most ops |
| **Direct service-to-service (HTTP/gRPC)** | Few services, no replay need | Tight coupling |
| **Database CDC (DMS / Debezium)** | Source of truth is a database | Latency depends on CDC mechanism |

## 9. Anti-patterns

- **Producers calling subscribers directly to "trigger" the event** — recreates coupling; use the bus, end of story
- **Synchronous wait for "event processed" on the producer side** — defeats decoupling; if you need a result, use a request-response pattern instead
- **No schema registry** — every consumer parses fields ad-hoc; first schema change breaks half of them
- **Schema-incompatible changes** (rename, remove, change type) — version the event type instead
- **Subscribing Lambda directly to a high-throttle source** — Lambda concurrency caps become subscriber backpressure that EventBridge can't see; SQS in front of Lambda
- **Catch-all rule pattern (`{}`)** — every event delivered to one consumer; cost explodes; explicit patterns
- **No DLQ on EventBridge targets** — failed deliveries silently disappear after EventBridge's internal retries
- **Archive enabled, replay never tested** — archive is dead weight if you can't replay; quarterly drill
- **Event payload includes secrets or PII** — events live in archive forever; treat as long-lived; PII goes by reference, not value
- **Using EventBridge for high-volume metrics / telemetry** — wrong tool; that's CloudWatch Metrics or Kinesis
- **Outbox pattern not implemented** — first DB-write-then-PutEvents failure leaks state; one of them succeeds and the other doesn't

For cross-cutting AWS anti-patterns, see [`anti-patterns.md`](anti-patterns.md).

## 10. Production checklist

- [ ] **Custom event bus** per domain (don't use the default bus for your own events)
- [ ] **Schema Registry** with backwards-compatible-only enforcement; CI checks schema diff on PR
- [ ] **Event versioning** — type names include version (`v1`); breaking changes go to v2 with v1 still consumed
- [ ] **`event_id` on every event** — UUID, used for idempotency by subscribers
- [ ] **Outbox pattern** for events that must reflect a DB transaction
- [ ] **DLQ on every target** with depth alarm
- [ ] **Subscriber idempotency** on `event_id` — DynamoDB conditional write or Powertools utility
- [ ] **Subscribers behind SQS** when work duration is variable or downstream is fragile
- [ ] **Archive configured** with explicit retention (not "forever" by default)
- [ ] **Replay tested** in non-prod; rate-limited replay path documented
- [ ] **Cross-account permissions** documented if multi-account; resource policies version-controlled
- [ ] **Quotas tracked** — `PutEvents` rate, target invocation rate per rule
- [ ] **Observability** — every event carries trace context; subscribers log `event_id`, `rule`, `outcome`
- [ ] **Cost alarms** at 1.5× and 5× expected baseline

## 11. References

**Official:**
- [EventBridge Documentation](https://docs.aws.amazon.com/eventbridge/) — full guide
- [EventBridge schema registry](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-schema-registry.html) — schema versioning and discovery
- [EventBridge event archive and replay](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-archive.html) — replay mechanism
- [EventBridge Pipes](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-pipes.html) — filter/enrich/transform
- [AWS Event-Driven Architecture (official)](https://aws.amazon.com/event-driven-architecture/) — patterns and reference architectures
- [Outbox pattern (AWS prescriptive guidance)](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html) — transactional outbox
- [SNS Documentation](https://docs.aws.amazon.com/sns/) — alternative for fan-out
- [Kinesis Data Streams Documentation](https://docs.aws.amazon.com/streams/) — alternative for high-volume

**Production guides:**
- [EventBridge event-driven architecture patterns](https://www.factualminds.com/blog/aws-eventbridge-event-driven-architecture-patterns/) — patterns deep dive
- [Step Functions workflow orchestration patterns](https://www.factualminds.com/blog/aws-step-functions-workflow-orchestration-patterns/) — when to wrap events in workflows

**Decision guides:**
- [Step Functions vs EventBridge](https://www.factualminds.com/compare/aws-step-functions-vs-eventbridge/) — orchestration vs routing
- [Bedrock Agents vs Step Functions](https://www.factualminds.com/compare/aws-bedrock-agents-vs-step-functions/) — when each fits

**OSS tools:**
- [aws-lambda-powertools-python](https://github.com/aws-powertools/powertools-lambda-python) — event source data classes for EventBridge
- [eventbridge-atlas](https://github.com/boyney123/eventbridge-atlas) — discover and document EventBridge schemas
- [eventcatalog](https://github.com/event-catalog/eventcatalog) — event documentation site generator

---

*See also: [`async-jobs.md`](async-jobs.md) · [`failure-first.md`](failure-first.md) · [`decision-trees.md`](decision-trees.md#event-processing--what-runs-in-response-to-an-event).*
