# Playbook: Multi-tenant SaaS

> Build a SaaS where multiple customers share infrastructure but get tenant isolation, predictable cost per tenant, and a blast radius that doesn't span the whole customer base.

**Tags:** `production-ready` · `complex`

**Status:** ✅ Available

---

## 1. Problem

You're building software-as-a-service. Every customer signs in and sees their own data. They might be on a free tier (you're losing money per signup) or a $50k/year contract (a 30-minute outage gets escalated to your CEO). You can't run a separate deployment for each — that doesn't scale below ~$10k/month per tenant — but you can't fully share either, or one customer's runaway query takes everyone down and one customer's data leaks across tenant boundaries.

The hard part isn't the first ten tenants. It's the architecture decision that's still defensible at a thousand. The wrong choice early shows up later as a six-month migration project under regulatory pressure.

## 2. Constraints

- **Isolation level required** — data only, compute, network, or all three (driven by compliance more than engineering preference)
- **Tenant count** — 10s (silo viable), 100s (pool default), 1000s+ (pool mandatory, sharding likely)
- **Per-tenant cost ceiling** — what's the floor cost of an inactive tenant? An idle silo tenant still costs money
- **Compliance regime** — HIPAA, SOC2, PCI; some prescribe isolation, most just require evidence of it
- **Tenant size variance** — top 1% of tenants typically generate 50%+ of load; bridge model exists because of this
- **Team size** — silo-per-tenant requires per-tenant ops; small teams should not pick this
- **Onboarding cadence** — self-serve sign-up vs sales-led; self-serve forces pool because you can't provision infra in <2 minutes
- **Offboarding obligations** — GDPR/CCPA require provable data deletion; harder in pool than silo

## 3. Reference architecture

The default for most SaaS is the **pool model**: shared infrastructure, tenant ID propagated through every layer, isolation enforced in code and IAM rather than separate deployments. Silo is the answer when compliance or contract terms demand it. Bridge is the realistic answer at scale.

```
                                         ┌────────────────────────────────────┐
                                         │  Identity (Cognito / IDP)          │
                                         │  tenant_id encoded in JWT claims   │
                                         └────────────────┬───────────────────┘
                                                          │
                                                          ▼
┌──────────────┐    ┌─────────────────┐    ┌───────────────────────────┐
│   Browser /  │───▶│   API Gateway   │───▶│  App (Lambda / ECS)       │
│   Mobile     │    │   per-route     │    │  - reads tenant_id from   │
│              │    │   throttling    │    │    JWT, never the body    │
└──────────────┘    └─────────────────┘    │  - tenant_id on every     │
                                           │    DB query, log line,    │
                                           │    metric, downstream call│
                                           └─────────┬─────────────────┘
                                                     │
                          ┌──────────────────────────┼──────────────────────────┐
                          │                          │                          │
                          ▼                          ▼                          ▼
                  ┌──────────────┐           ┌──────────────┐           ┌──────────────┐
                  │ DynamoDB     │           │   S3         │           │   Search     │
                  │ PK starts    │           │ prefix:      │           │   tenant     │
                  │ with         │           │ tenants/<id> │           │   filter on  │
                  │ tenant_id    │           │              │           │   every query│
                  └──────────────┘           └──────────────┘           └──────────────┘
                          │                          │                          │
                          └──────────────────────────┼──────────────────────────┘
                                                     │
                                                     ▼
                                       ┌──────────────────────────┐
                                       │  Tagging + Cost Categories│
                                       │  cost-per-tenant rollup   │
                                       └──────────────────────────┘
```

1. **Identity** — tenant ID lives in the token, signed by your IDP. Never trust a tenant ID from the request body or URL alone.
2. **API gateway** — per-tenant rate limits via usage plans or custom authoriser. Per-route limits per tenant prevent one tenant from starving others.
3. **App layer** — tenant ID extracted from JWT once, then forced onto every downstream call. Logs, metrics, traces all carry it. Treat it like a request ID.
4. **Storage** — tenant ID is the leftmost component of every partition key (DynamoDB), every S3 prefix, every search index filter. RDBMS: row-level security or a query-builder mandate that injects `WHERE tenant_id = ?` automatically.
5. **Cost attribution** — `tenant:<id>` tag on every resource that can carry one; AWS Cost Categories roll those up to per-tenant cost in Cost Explorer. AWS Application Cost Profiler for fine-grained Lambda/Bedrock attribution.

## 4. Architecture variants

| Model | Cost per tenant | Isolation | Ops burden | Blast radius | Best for |
|-------|----------------|-----------|------------|--------------|----------|
| **Silo** (per-tenant infra) | High (>$X00/mo floor) | Strongest | Highest | One tenant | Enterprise, regulated, large contracts |
| **Pool** (shared, tenant_id everywhere) | Lowest | Code-enforced | Lowest | All tenants | Self-serve, mid-market, default |
| **Bridge** (silo for top tier, pool for rest) | Mixed | Mixed | Medium | Tier-bounded | Scaled SaaS with mixed-tier customers |
| **Sharded pool** (pool but multiple shards) | Low | Pool inside shard | Medium | Shard | High-scale (1000s of tenants) |

**Common bridge pattern:** free + paid in pool, enterprise on dedicated stacks (silo). The shared codebase serves both — the difference is deployment topology and IAM scope.

**RDBMS pool sub-variants:**
- **Shared schema, tenant_id column on every table** — simplest, most common; relies on application correctness
- **Schema-per-tenant in shared DB** — mid-isolation; pgbouncer connection cost grows with tenants
- **Database-per-tenant in shared cluster** — closer to silo on isolation, complex migrations

For SaaS on Bedrock/GenAI specifically, see the multi-tenant GenAI variants (References — Production guides).

## 5. Failure modes

Cross-cutting patterns: see [`failure-first.md`](failure-first.md). SaaS-specific modes below.

### Cross-tenant data leakage

- **What it looks like** — tenant A sees tenant B's data; usually surfaced by a customer support ticket, sometimes by a security researcher
- **Why it happens** — query missing `tenant_id` filter; wrong tenant ID extracted from token; cache key collision (cache keyed on resource ID without tenant prefix); admin endpoint not scoped
- **Detection** — extremely hard after the fact; primary defence is shift-left — query-builder that mandates tenant filter, IAM session policies that scope by tenant, integration tests that assert isolation
- **Recovery** — there is no clean recovery from a leak. Disclose, audit, rotate any exposed credentials. This is the failure mode you build the entire architecture around preventing.

### Noisy neighbour

- **What it looks like** — one tenant's load spikes (export job, runaway integration); other tenants see latency
- **Why it happens** — no per-tenant rate limiting; no per-tenant resource caps; shared DynamoDB hot partition; Lambda concurrency exhausted by one tenant
- **Detection** — per-tenant p99 latency tracked; alarm when any tenant's traffic exceeds 30% of platform total
- **Recovery** — usage plans / per-tenant throttling at API Gateway; reserved Lambda concurrency per tenant tier; DynamoDB on-demand or per-tenant adaptive capacity; SQS-per-tenant for batch work

### Tenant ID forgery / privilege escalation

- **What it looks like** — request claims to be tenant B from tenant A's session
- **Why it happens** — accepting tenant ID from request body / query string / cookie; not verifying JWT signature; allowing one user to be a member of multiple tenants without explicit context switch
- **Detection** — authoriser logs that show JWT-claim tenant_id ≠ requested tenant_id
- **Recovery** — tenant ID **must** come from the verified JWT only; if cross-tenant operations are needed (admin, support), build a separate authenticated path with audit logs

### Billing reconciliation drift

- **What it looks like** — your usage records and Stripe invoices disagree by more than the rounding budget
- **Why it happens** — usage events lost (no idempotency in metering pipeline); double-counted on retry; resource tag missing or mistyped
- **Detection** — daily reconciliation job comparing aggregated event count to billed amount; alarm on >0.1% drift
- **Recovery** — hold invoice generation until reconciliation passes; tag-coverage report for any new resource type before it ships

### Tenant onboarding race conditions

- **What it looks like** — two parallel sign-up requests for the same tenant slug create two tenants; or a tenant is half-provisioned and stuck
- **Why it happens** — non-transactional provisioning across multiple services
- **Recovery** — Step Functions or Saga pattern with explicit compensation steps; conditional writes on tenant slug uniqueness; idempotency key on the provisioning request

### Incomplete offboarding

- **What it looks like** — tenant deleted, but data persists in S3 prefix, search index, backups, log archive, downstream caches
- **Why it happens** — every place that stores tenant data is a place that needs an offboarding path; teams forget the long tail
- **Recovery** — maintain an authoritative list of "places tenant data lives"; offboarding runbook deletes from each; audited deletion proof generated; backup retention policy that caps risk window

### IAM blast radius mistakes

- **What it looks like** — a Lambda for tenant A has an IAM role that can read tenant B's bucket
- **Why it happens** — role-per-service instead of role-per-tenant-per-service; wildcard resources in policies
- **Recovery** — IAM session tags for tenant scoping; STS `AssumeRole` with session policy generated from tenant context; service control policies in the tenant account if you're going account-per-tenant

## 6. Cost model

The economics differ by model. Concrete example: a SaaS with 100 tenants, average 1k requests/tenant/day, 10MB DynamoDB data each.

| Line item | Pool | Bridge | Silo (per tenant) |
|-----------|------|--------|--------------------|
| Compute (Lambda) | ~$50/mo total | ~$50/mo + $X per silo tenant | ~$30/mo each |
| DynamoDB | ~$25/mo total | ~$25/mo + per-silo | ~$5/mo each |
| API Gateway | ~$3/mo total | shared | per-tenant URL = per-tenant cost |
| Cognito | $0.0055/MAU above free tier | shared user pool or per-tenant | per-tenant pool |
| Logging / monitoring | shared, attributed by tag | shared + per-silo | per-tenant |
| Floor cost (idle tenant) | near-zero | tier-dependent | $50–$200/mo each |
| **100-tenant total** | **~$80/mo** | **~$80 + (silo × n)** | **~$5,000–$20,000/mo** |

**Scaling shape:**
- **Pool** — sub-linear; shared overhead amortised
- **Silo** — linear with tenant count + per-tenant floor
- **Bridge** — pool baseline + silo fixed costs at the high tier

**Cost attribution mechanics:**
- Tag every resource with `tenant:<id>` (or `tenant_tier:<tier>` if pool)
- AWS Cost Categories rolls tags into per-tenant lines in Cost Explorer
- Application Cost Profiler for Lambda CPU-ms and Bedrock token-level attribution
- Untaggable resources (e.g., NAT Gateway data processing): split proportionally by request count or VPC flow log analysis

**Cost traps:**
- **Cognito user pool per tenant** in a pool model → user pool count limits + per-pool MAU minimums
- **Per-tenant log group** at high tenant count → CloudWatch log group quota and ingestion floor
- **NAT Gateway** for shared egress → impossible to attribute cleanly per tenant; see [`cost-pitfalls.md`](cost-pitfalls.md#nat-gateway)
- **Free tier tenants without a usage cap** → cost-based DoS by sign-up; rate-limit aggressively, suspend free tenants on threshold

## 7. When NOT to use this

- **B2C single-tenant product** — there's no tenant boundary; don't build SaaS abstractions for users
- **Pre-PMF** — building for "scale to 10k tenants" before product-market fit is the textbook over-engineering trap; pick pool, ship, refactor when you have customer pain
- **Strict regulated workloads with per-customer data residency** — silo per region per customer is sometimes the only legal answer; this playbook still applies but the "default to pool" advice doesn't
- **Marketplace / two-sided platform** — tenants of tenants is a different problem; pure multi-tenancy patterns will mislead you
- **Embedded / on-prem deployment requirement** — customer wants to run it themselves; that's deployment-per-customer with config, not multi-tenancy

## 8. Alternatives

| Approach | Cost per tenant | Isolation | Ops burden | When it wins |
|----------|----------------|-----------|------------|--------------|
| **AWS multi-tenant (this playbook)** | Lowest in pool | Code + IAM enforced | Low | Default for new SaaS on AWS |
| **Per-customer dedicated deploy (Terraform per tenant)** | High | Strongest | High | Enterprise, on-prem-style contracts |
| **Kubernetes namespace-per-tenant (EKS)** | Medium | K8s RBAC + NetworkPolicies | Medium | Existing K8s investment, team has K8s ops |
| **Managed multi-tenant platform (Frontegg, WorkOS, ZITADEL)** | Predictable per-MAU fee | Vendor-managed | Low for auth, app remains yours | Want to skip building auth/billing/admin |
| **Database-only multi-tenancy via Postgres RLS or DynamoDB single-table** | Lowest | DB-enforced | Low if patterns are right | Most teams; this is a sub-pattern of pool |

## 9. Anti-patterns

- **Tenant ID from the request body or URL** — easy to forge. Tenant ID belongs in the verified JWT, end of discussion.
- **Single shared admin role with `*` resource scopes** — first compromise = all tenant data. Use STS session policies scoped to the tenant context for any admin operation.
- **No tenant filter in queries; rely on app code never to forget** — eventually someone forgets. Use a query builder that mandates the filter, or DB-enforced RLS.
- **Single CloudWatch log group for all tenants without tenant ID in every log line** — debugging is now archaeology. Log structured JSON with `tenant_id` always.
- **No per-tenant feature flags** — when a customer needs a fix gated to them, you'll deploy a hack. Use a feature-flag service that supports tenant context (LaunchDarkly, Flagsmith, OpenFeature).
- **Cognito user pool per tenant in a pool model** — hits user-pool count limits fast; cross-pool admin is painful. One pool with custom attributes (`tenant_id`, `role`) scales further.
- **Cache keys without tenant prefix** — first cross-tenant data leak you'll ever have. Always `<tenant_id>:<resource>:<id>`.
- **One DynamoDB table per tenant** — you'll hit table quotas. Single table with `tenant_id` as the leading partition key component is the standard.
- **Global rollouts to all tenants at once** — one bad release takes everyone down. Ring deployments by tenant tier or random sample.
- **Tenant ID stamped into URLs/subdomains as the only enforcement** — defense-in-depth means JWT is the source of truth, URL is UX only.
- **No tenant offboarding tested before launch** — you'll find out about the long tail of data residue when GDPR comes calling.

For cross-cutting AWS anti-patterns, see [`anti-patterns.md`](anti-patterns.md).

## 10. Production checklist

- [ ] **Tenant ID source of truth** — verified JWT only; tested that body/URL tampering is rejected
- [ ] **Tenant ID propagated** through every layer: HTTP → service → DB query → log → metric → downstream call → trace
- [ ] **Authorisation tested** for cross-tenant access on every sensitive endpoint (integration test suite that asserts 403 across tenants)
- [ ] **Per-tenant rate limiting** at API Gateway (usage plans or custom authoriser)
- [ ] **DynamoDB partition key** has tenant_id as leftmost component for every table holding tenant data
- [ ] **S3 prefixes** include `tenants/<tenant_id>/` for tenant-bound data; bucket policies enforce tenant scope where feasible
- [ ] **IAM scoping** — STS session tags for tenant context; session policies generated from tenant; no wildcard resource ARNs in tenant-scoped roles
- [ ] **Observability tagged** — CloudWatch metrics dimension `TenantId`; logs structured with `tenant_id`; traces include tenant baggage
- [ ] **Cost attribution** — every resource tagged `tenant:<id>` or `tenant_tier:<tier>`; Cost Categories configured; per-tenant cost report runs daily
- [ ] **Per-tenant cost alarms** at $X (free-tier ceiling), 1.5× expected (paid), and 5× (runaway flag)
- [ ] **Tenant onboarding** is idempotent and either succeeds fully or compensates fully (Step Functions or Saga)
- [ ] **Tenant offboarding runbook** lists every data location; deletion script tested; audit log generated
- [ ] **Backup retention** documented per tenant tier; after-offboarding window agreed (and matches your DPA)
- [ ] **Per-tenant feature flags** wired up before you need them
- [ ] **Ring deployments** — at minimum, free tier ahead of paid tier
- [ ] **Compliance evidence** — for regulated customers, generate per-tenant access logs, configuration snapshots, encryption proofs on schedule

## 11. References

**Official:**
- [AWS SaaS Lens (Well-Architected)](https://docs.aws.amazon.com/wellarchitected/latest/saas-lens/saas-lens.html) — official guidance for SaaS architecture decisions
- [AWS SaaS Factory program](https://aws.amazon.com/partners/saas-factory/) — reference architectures, tooling, advisory
- [Tenant isolation strategies (whitepaper)](https://docs.aws.amazon.com/whitepapers/latest/saas-tenant-isolation-strategies/saas-tenant-isolation-strategies.html) — silo / pool / bridge from the source
- [Split cost allocation data](https://docs.aws.amazon.com/cur/latest/userguide/split-cost-allocation-data.html) — per-pod cost attribution for shared EKS / ECS
- [AWS Cost Categories](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/manage-cost-categories.html) — tag-based rollup for per-tenant reports
- [Cognito multi-tenant patterns](https://docs.aws.amazon.com/cognito/latest/developerguide/multi-tenant-application-best-practices.html) — official auth multi-tenancy guidance
- [DynamoDB multi-tenant data partitioning](https://docs.aws.amazon.com/prescriptive-guidance/latest/saas-multitenant-api-access-authorization/multi-tenant-data-partitioning.html) — partition key design for SaaS
- [IAM session tags for tenant isolation](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_session-tags.html) — STS session-policy pattern

**Production guides:**
- [SaaS multi-tenancy on AWS — silo vs pool vs bridge](https://www.factualminds.com/blog/saas-multi-tenancy-on-aws-silo-vs-pool-vs-bridge-model/) — model selection deep dive
- [Multi-tenant SaaS on AWS — architecture pattern](https://www.factualminds.com/patterns/multi-tenant-saas-on-aws/) — full pattern reference
- [Multi-tenant GenAI on Bedrock](https://www.factualminds.com/blog/multi-tenant-genai-bedrock/) — SaaS layered with Bedrock
- [Multi-tenant architecture — glossary](https://www.factualminds.com/glossary/multi-tenant-architecture/) — terminology reference

**Reference implementations:**
- [aws-samples/aws-saas-factory-ref-solution-serverless-saas](https://github.com/aws-samples/aws-saas-factory-ref-solution-serverless-saas) — production serverless multi-tenant reference
- [aws-samples/aws-saas-factory-eks-reference-architecture](https://github.com/aws-samples/aws-saas-factory-eks-reference-architecture) — EKS-based SaaS sample
- [aws-saas-boost](https://github.com/awslabs/aws-saas-boost) — open-source SaaS environment from AWS Labs

**Decision guides:**
- [DynamoDB vs RDS for SaaS](https://www.factualminds.com/compare/dynamodb-vs-rds/) — pick the storage layer
- [IAM Identity Center vs Cognito](https://www.factualminds.com/compare/aws-iam-identity-center-vs-cognito/) — pick the auth surface
- [SaaS industry hub](https://www.factualminds.com/industries/saas/) — broader industry context

**OSS tools:**
- [Frontegg](https://github.com/frontegg) — managed multi-tenant auth + admin (alternative to building it)
- [WorkOS SDKs](https://github.com/workos) — SSO and directory sync for B2B SaaS
- [openfeature](https://github.com/open-feature) — vendor-neutral feature flag standard with tenant context

---

*Format rules from [CONTRIBUTING.md](../CONTRIBUTING.md): em-dash separator, descriptions under 100 chars, sentence case, HTTPS URLs.*
