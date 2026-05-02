# Use-Case Playbooks

> How to build common workloads on AWS in production — problem, architecture, failure modes, cost, anti-patterns. Not a links list; a playbook.

Each playbook follows a strict 11-section template at [`_template.md`](_template.md): Problem · Constraints · Reference architecture · Variants · Failure modes · Cost · When NOT to use · Alternatives · Anti-patterns · Production checklist · References.

The root [README.md](../README.md) is still the place to browse by AWS service. These playbooks are the place to start when you know the **workload** you're building.

## Workload playbooks

| Playbook | What you'll build |
|----------|-------------------|
| [Email delivery](email-delivery.md) | Transactional email at scale on SES with bounce/complaint handling and deliverability tracking |
| [Multi-tenant SaaS](multi-tenant-saas.md) | Multi-tenant isolation with silo / pool / bridge models and per-tenant cost attribution |
| [Async job processing](async-jobs.md) | API → queue → worker → result store with idempotency, DLQ, and webhook delivery |
| [Event-driven processing](event-driven.md) | EventBridge with schemas, replay, DLQs per target, and multi-account routing |
| [File upload and processing](file-upload.md) | Pre-signed S3 uploads with malware scan, MIME sniffing, and async transform pipeline |
| [High-scale API backend](high-scale-api.md) | CloudFront + WAF + API Gateway + cache + database with rate limits and graceful degradation |
| [Real-time analytics pipeline](real-time-analytics.md) | Kinesis → Lambda hot path + Firehose cold path → S3 + Athena lambda architecture |
| [Observability pipeline](observability-pipeline.md) | Hot CloudWatch + cold S3-Athena with EMF metrics, trace sampling, and PII redaction |
| [GenAI / RAG application](genai-rag.md) | Bedrock + vector store + retrieval + Guardrails with evals and per-tenant cost attribution |
| [CI/CD for AWS workloads](ci-cd.md) | GitHub Actions + OIDC + per-environment accounts with canary, rollback, and drift detection |

## Cross-cutting frameworks

Patterns referenced across playbooks. Don't repeat — link.

| Framework | Covers |
|-----------|--------|
| [Decision trees](decision-trees.md) | Which AWS service for event processing, database, compute, async work, file processing |
| [Failure-first patterns](failure-first.md) | Retries, idempotency, DLQs, regional failover, backpressure, circuit breakers |
| [Anti-patterns](anti-patterns.md) | The mistakes that show up across every workload, with the better pattern |
| [Cost pitfalls](cost-pitfalls.md) | Line items that surprise teams (NAT Gateway, cross-AZ, CloudWatch Logs, egress) |

## Contributing a new playbook

1. Copy [`_template.md`](_template.md) to `<use-case-slug>.md`.
2. Fill in all 11 sections in order. Don't skip §5 (Failure modes), §7 (When NOT to use), or §9 (Anti-patterns) — those are the differentiators.
3. Pick tags from the vocabulary in [CONTRIBUTING.md](../CONTRIBUTING.md): `production-ready` · `high-scale` · `low-cost` · `complex` · `deprecated-pattern`.
4. Add a row to the Workload playbooks table above and link to it from the root [README.md](../README.md).
5. Open a PR. The link checker will validate every URL.
