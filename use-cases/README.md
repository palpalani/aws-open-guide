# Use-Case Playbooks

> How to build common workloads on AWS in production — problem, architecture, failure modes, cost, anti-patterns. Not a links list; a playbook.

Each playbook follows a strict 11-section template at [`_template.md`](_template.md): Problem · Constraints · Reference architecture · Variants · Failure modes · Cost · When NOT to use · Alternatives · Anti-patterns · Production checklist · References.

The root [README.md](../README.md) is still the place to browse by AWS service. These playbooks are the place to start when you know the **workload** you're building.

## Available

| Playbook | What you'll build |
|----------|-------------------|
| [Email delivery](email-delivery.md) | Transactional email at scale on SES with bounce/complaint handling and deliverability tracking |
| [Multi-tenant SaaS](multi-tenant-saas.md) | Multi-tenant isolation with silo / pool / bridge models and per-tenant cost attribution |

## Cross-cutting frameworks

Patterns referenced across playbooks. Don't repeat — link.

| Framework | Covers |
|-----------|--------|
| [Decision trees](decision-trees.md) | Which AWS service for event processing, database, compute, async work, file processing |
| [Failure-first patterns](failure-first.md) | Retries, idempotency, DLQs, regional failover, backpressure, circuit breakers |
| [Anti-patterns](anti-patterns.md) | The mistakes that show up across every workload, with the better pattern |
| [Cost pitfalls](cost-pitfalls.md) | Line items that surprise teams (NAT Gateway, cross-AZ, CloudWatch Logs, egress) |

## Planned

These are next. Each will land as a separate PR following the same template.

- 🚧 Event-driven processing — S3 → EventBridge → Lambda → SQS → DLQ
- 🚧 Real-time analytics — Kinesis → Lambda → S3 → Athena
- 🚧 GenAI / RAG — Bedrock + vector DB + retrieval + safety
- 🚧 Async job processing — API → queue → worker → result store
- 🚧 File upload + processing — S3 pre-signed URLs + async pipeline
- 🚧 High-scale API backend — caching, rate limiting, WAF
- 🚧 Observability pipeline — logs → Firehose → S3 → Athena
- 🚧 CI/CD — GitHub Actions vs CodePipeline

## Contributing a new playbook

1. Copy [`_template.md`](_template.md) to `<use-case-slug>.md`.
2. Fill in all 11 sections in order. Don't skip §5 (Failure modes), §7 (When NOT to use), or §9 (Anti-patterns) — those are the differentiators.
3. Pick tags from the vocabulary in [CONTRIBUTING.md](../CONTRIBUTING.md): `production-ready` · `high-scale` · `low-cost` · `complex` · `deprecated-pattern`.
4. Add a row to the Available table above and link to it from the root [README.md](../README.md).
5. Open a PR. The link checker will validate every URL.
