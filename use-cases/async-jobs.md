# Playbook: Async job processing

> Decouple the API from the work. Accept the request fast, process in the background, expose progress and results without blocking.

**Tags:** `production-ready` · `low-cost`

**Status:** ✅ Available

---

## 1. Problem

The user clicks "Generate report" or "Import 50,000 rows" or "Render PDF." The work takes 30 seconds to 30 minutes. You can't keep the HTTP connection open that long; you can't show a spinner forever; you can't drop the work if the user closes the tab. You need to accept the request, return immediately, do the work asynchronously, and let the user check on it.

The naïve solution — kick off a background thread in your API process — falls over the moment the API instance restarts, the request volume spikes, or the work needs to retry. The pattern below is what every well-built async system converges on.

## 2. Constraints

- **Request acceptance latency** — API returns in <500ms regardless of work size
- **Work duration** — seconds to hours; affects compute choice
- **Volume** — 1/sec to 1k/sec affects queue choice and cost
- **Result delivery** — polling, webhook, WebSocket, or email; must be explicit
- **Failure tolerance** — retries, DLQ, idempotency are not optional
- **Visibility** — user wants to know "is it running, queued, failed, done?"
- **Ordering** — usually doesn't matter; if it does, FIFO queue or per-tenant partitioning

## 3. Reference architecture

```
┌────────────┐    ┌──────────────┐    ┌──────────────┐
│   Client   │───▶│  API Gateway │───▶│   Lambda     │
│            │    │   /jobs POST │    │  (validate,  │
│            │◀───│              │    │   enqueue)   │
└─────┬──────┘    └──────────────┘    └──────┬───────┘
      │ job_id                                │
      │                                       ▼
      │                              ┌────────────────┐
      │                              │  DynamoDB      │
      │                              │  jobs table:   │
      │                              │  status=queued │
      │                              └────────┬───────┘
      │                                       │
      │                                       ▼
      │                              ┌────────────────┐
      │                              │     SQS        │
      │                              │   (job queue)  │
      │                              └────────┬───────┘
      │                                       │
      │                                       ▼
      │                              ┌────────────────┐
      │                              │    Worker      │
      │                              │ (Lambda / ECS) │
      │                              │ - process work │
      │                              │ - update status│
      │                              │ - handle retry │
      │                              └────────┬───────┘
      │                                       │
      │                                       ▼
      │                              ┌────────────────┐
      │   GET /jobs/{id} ─────────▶  │  jobs table:   │
      │                              │  status=done,  │
      │   or webhook callback ◀──────│  result_url=…  │
      │                              └────────────────┘
                                              │
                                              ▼
                                     ┌────────────────┐
                                     │  Result store  │
                                     │  (S3 for blobs,│
                                     │   DDB for JSON)│
                                     └────────────────┘
```

1. **POST /jobs** — Lambda validates the request, generates `job_id` (UUID), writes `(job_id, status=queued, created_at)` to DynamoDB, sends a message to SQS with `job_id` and the work payload. Returns `202 Accepted` with `job_id`.
2. **Worker** — pulls from SQS. Updates DynamoDB to `status=running`. Does the work. On success: writes result (S3 if blob, DynamoDB if small) and updates job to `status=done` with result reference. On failure: lets SQS retry; after `maxReceiveCount` SQS sends to DLQ.
3. **GET /jobs/{id}** — Lambda reads from DynamoDB and returns current status + result reference if done.
4. **Webhook (optional)** — when status flips to `done` or `failed`, a Lambda notifies the client URL with idempotent retry.

DLQ has a CloudWatch alarm; runbook describes how to inspect and redrive after fixing the upstream issue. See [`failure-first.md`](failure-first.md#3-dead-letter-queues-dlqs).

## 4. Architecture variants

| Variant | When | Notes |
|---------|------|-------|
| **SQS + Lambda worker** | Default; jobs <15min | Simplest; auto-scales |
| **SQS + ECS Fargate worker** | Jobs >15min or heavy CPU/memory | Long-running container; manual scaling rules |
| **Step Functions** | Multi-step workflows with branching | State machine + Tasks; built-in retry/catch |
| **Step Functions Express** | High-volume, sub-second steps | Cheaper at scale, at-least-once |
| **EventBridge Pipes** | Stream → filter → enrich → target | Lower-code; Lambda still does heavy lifting |
| **AWS Batch** | Scientific compute, large fleets | Job queues + compute environments + spot |
| **FIFO SQS** | Strict per-tenant ordering | Lower throughput (300 TPS without batching) |
| **Kinesis** | High volume + replay needed | Use if SQS throughput insufficient or you need history |

## 5. Failure modes

Cross-cutting patterns: see [`failure-first.md`](failure-first.md). Async-job-specific modes:

### Worker crashes mid-job

- **What it looks like** — DynamoDB still says `status=running` but no progress; SQS message visibility timeout expires and message reappears
- **Why it happens** — Lambda timeout, OOM, container kill, ECS task replacement
- **Detection** — heartbeat — worker updates `last_heartbeat_at` periodically; alarm on jobs `running` for longer than expected
- **Recovery** — visibility timeout < (typical job duration × 1.5); use heartbeats and `ChangeMessageVisibility` for long jobs; idempotent worker so re-processing is safe

### Duplicate processing

- **What it looks like** — same job runs twice; side effects fire twice (charges, emails, third-party calls)
- **Why it happens** — SQS at-least-once delivery; visibility-timeout expiry while worker is still alive; webhook retry
- **Detection** — usually by user complaint; can be detected by counting state transitions per job
- **Recovery** — idempotent worker keyed on `job_id`; first state-changing operation acquires a lock via DynamoDB conditional write; non-idempotent side effects guarded by a separate idempotency key

### Poison messages

- **What it looks like** — same message fails repeatedly; queue depth never drops; DLQ fills
- **Why it happens** — malformed payload, missing dependency, non-retryable error treated as retryable
- **Detection** — DLQ alarm; per-job retry count via DynamoDB
- **Recovery** — DLQ + alarm + runbook; classify errors as retryable vs non-retryable in the worker — non-retryable goes straight to `status=failed` without queue retry

### Backpressure / queue overflow

- **What it looks like** — queue depth grows faster than workers drain; oldest message age increases
- **Why it happens** — sudden load, worker concurrency capped too low, downstream throttling
- **Detection** — `ApproximateNumberOfMessagesVisible` and `ApproximateAgeOfOldestMessage` alarms
- **Recovery** — auto-scale workers; reduce upstream throughput (rate-limit POST /jobs); shed lowest-priority work; see [`failure-first.md`](failure-first.md#6-backpressure)

### Result lost / orphaned

- **What it looks like** — job done but result link broken or expired
- **Why it happens** — pre-signed URL expired; S3 lifecycle deleted result; DynamoDB TTL expired status
- **Recovery** — match S3 lifecycle and DynamoDB TTL to your SLA for result retention; results meant to live longer go to a no-TTL "archived" partition

### Tenant noisy neighbour (multi-tenant context)

- **What it looks like** — one tenant submits a flood of jobs and starves others
- **Recovery** — per-tenant queue, per-tenant rate limit at API, or fair-share scheduler; see [`multi-tenant-saas.md`](multi-tenant-saas.md)

## 6. Cost model

Worked example: 100k jobs/day, 30s avg duration, 1MB result.

| Line item | Daily | Monthly | Notes |
|-----------|-------|---------|-------|
| API Gateway requests | $0.35 | ~$10 | $3.50/M requests |
| Lambda enqueue (100k × 100ms × 256MB) | $0.04 | ~$1 | Per-request overhead minimal |
| SQS requests (POST + worker poll) | ~$0.05 | ~$1.50 | $0.40/M requests; long-polling reduces empty receives |
| Lambda worker (100k × 30s × 1GB) | ~$50 | ~$1,500 | Bulk of cost; size memory carefully |
| DynamoDB on-demand (300k writes, 200k reads) | ~$0.45 | ~$13 | Status updates dominate |
| S3 PUT + storage (100k × 1MB × 30d retention) | ~$0.15 + $0.07/GB/mo | ~$15 | Lifecycle to IA after 30d |
| **Total** | ~$51 | **~$1,540** | ~$0.015 per job |

**Scaling shape:** linear with job count for compute; sub-linear for fixed services. Big lever: **right-size Lambda memory** with Lambda Power Tuning — typical savings 20–40% (see References — OSS tools).

**Cost traps:**
- **Lambda memory over-provisioned** for short jobs — direct cost multiplier
- **Worker concurrency set too high** during a backpressure spike — Lambda spins up thousands of containers, each calling DynamoDB → DynamoDB throttling → cascade
- **DynamoDB on-demand** for predictable steady load — switch to provisioned with autoscaling at scale
- **S3 small-object** results without lifecycle — see [`cost-pitfalls.md`](cost-pitfalls.md#s3-small-object-put-heavy-without-aggregation)

## 7. When NOT to use this

- **Jobs <500ms** — return synchronously; the queue overhead exceeds the work
- **Strict FIFO across all jobs** — global FIFO doesn't scale on SQS (300 TPS / partition); reconsider whether you really need it
- **Jobs that must guarantee exactly-once delivery to a non-idempotent third party** — exactly-once is a known impossibility; if your downstream can't handle dedup, you can't either; pick a different downstream
- **Real-time streaming work** (sub-second per record at high volume) — use Kinesis + Lambda or Flink instead

## 8. Alternatives

| Approach | Best for | Tradeoff |
|----------|----------|----------|
| **SQS + Lambda (this playbook)** | Default, <15min jobs | Lambda 15min hard limit |
| **SQS + ECS Fargate** | Long jobs, container ergonomics | Slightly more ops; pays even when idle |
| **Step Functions Standard** | Multi-step workflows | Costs $0.025/1k transitions; built-in retry/catch |
| **AWS Batch** | HPC, ML training, large parallel batches | Job queues + compute envs; spot for cost |
| **Celery + Redis on ECS** | Existing Python codebase | More ops; familiar; less AWS lock-in |
| **Sidekiq + Redis on ECS** | Ruby on Rails | Same as above for Ruby |
| **External queue (RabbitMQ MQ, Confluent Kafka)** | Multi-cloud, complex topologies | More features; more ops |

## 9. Anti-patterns

- **Fire-and-forget without DLQ** — failures are silent; weeks later "where did those jobs go?"
- **Retrying non-idempotent side effects** — retry sends 5 emails, charges card 3 times; idempotency key first
- **Visibility timeout shorter than typical job** — message reappears mid-process, two workers race on the same job
- **Visibility timeout much longer than typical job** — failed jobs sit invisible for hours before retry
- **Polling DynamoDB at 1Hz from a UI** — wasted reads at scale; use API Gateway WebSockets or AppSync subscriptions for live status, or webhook on completion
- **Storing entire job payload in SQS** — 256KB SQS limit; oversized messages → use S3 for the payload, SQS message holds the S3 reference (Claim Check pattern — see References — Official)
- **Single shared queue for all tenants in multi-tenant SaaS** — noisy tenant blocks others; per-tenant queues or fair-share scheduling
- **Status field as freeform string** — typos, drift; enum: `queued | running | done | failed | cancelled`
- **No timeout on the worker** — runaway job pegs Lambda for 15 minutes per attempt × retries × concurrency
- **No `failed` terminal state** — jobs stuck `running` forever after a worker crash; reaper job that times out stale `running` records

For cross-cutting AWS anti-patterns, see [`anti-patterns.md`](anti-patterns.md).

## 10. Production checklist

- [ ] **Idempotency key** on every state-changing operation in the worker (DynamoDB conditional write or Powertools idempotency utility)
- [ ] **DLQ configured** with `maxReceiveCount` (3–10) and CloudWatch alarm on depth >0
- [ ] **DLQ runbook** — how to inspect, fix upstream, redrive
- [ ] **Visibility timeout** ≥ 1.5× typical job duration; use heartbeat + `ChangeMessageVisibility` for variable jobs
- [ ] **Worker timeout** at the Lambda or ECS level shorter than visibility timeout, longer than expected job duration
- [ ] **Status state machine** documented; only legal transitions allowed
- [ ] **Reaper** for stale `running` jobs (auto-fail after 2× max expected duration)
- [ ] **Result retention** matched between S3 lifecycle and DynamoDB TTL
- [ ] **Backpressure alarms** on queue depth, oldest message age, DLQ count
- [ ] **Per-tenant rate limits** at the API for multi-tenant systems
- [ ] **Webhook delivery** (if used) is idempotent and signs requests so receiver can verify origin
- [ ] **Observability** — `job_id`, `tenant_id`, status transitions logged on every step
- [ ] **Cost alarms** at 1.5× and 5× expected baseline
- [ ] **Drill** — kill a worker mid-job; confirm message reappears and re-runs cleanly

## 11. References

**Official:**
- [SQS Documentation](https://docs.aws.amazon.com/sqs/) — full SQS guide
- [Lambda with SQS event source](https://docs.aws.amazon.com/lambda/latest/dg/with-sqs.html) — auto-scaling and batch behaviour
- [Lambda concurrency and throttling](https://docs.aws.amazon.com/lambda/latest/dg/lambda-concurrency.html) — reserved vs provisioned concurrency
- [SQS visibility timeout](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-visibility-timeout.html) — official explanation
- [Step Functions Documentation](https://docs.aws.amazon.com/step-functions/) — workflow orchestration
- [Avoiding insurmountable queue backlogs (Builders Library)](https://aws.amazon.com/builders-library/avoiding-insurmountable-queue-backlogs/) — canonical queue anti-pattern reference
- [Claim Check pattern (AWS prescriptive guidance)](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/claim-check.html) — for oversized payloads
- [AWS Powertools for Lambda — Idempotency](https://docs.powertools.aws.dev/lambda/python/latest/utilities/idempotency/) — idempotency utility

**Production guides:**
- [EventBridge event-driven architecture patterns](https://www.factualminds.com/blog/aws-eventbridge-event-driven-architecture-patterns/) — broader event-driven patterns
- [Step Functions workflow orchestration patterns](https://www.factualminds.com/blog/aws-step-functions-workflow-orchestration-patterns/) — multi-step workflow patterns

**Decision guides:**
- [Step Functions vs EventBridge](https://www.factualminds.com/compare/aws-step-functions-vs-eventbridge/) — orchestration vs routing
- [Lambda vs ECS Fargate](https://www.factualminds.com/compare/aws-lambda-vs-ecs-fargate/) — worker compute choice

**OSS tools:**
- [aws-lambda-powertools-python](https://github.com/aws-powertools/powertools-lambda-python) — idempotency, batch, structured logging
- [aws-lambda-powertools-typescript](https://github.com/aws-powertools/powertools-lambda-typescript) — same for Node.js
- [Lambda Power Tuning](https://github.com/alexcasalboni/aws-lambda-power-tuning) — optimise memory for cost/perf

---

*See also: [`event-driven.md`](event-driven.md) · [`failure-first.md`](failure-first.md) · [`cost-pitfalls.md`](cost-pitfalls.md) · [`decision-trees.md`](decision-trees.md#async-work--how-do-you-orchestrate-background-processing).*
