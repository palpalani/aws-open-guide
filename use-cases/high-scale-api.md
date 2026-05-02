# Playbook: High-scale API backend

> A public HTTP API that handles tens of thousands of requests per second with caching, rate limiting, WAF, and predictable latency under load.

**Tags:** `production-ready` · `high-scale`

**Status:** ✅ Available

---

## 1. Problem

Your API is the front door. Customers depend on it. Bots find it. A buggy client retries in a tight loop. A spike from a launch day makes it the bottleneck. The work is no longer "build a CRUD API" — it's "build an API that survives the internet."

This playbook is the architecture for HTTP APIs at scale: edge caching, layered rate limits, WAF, regional routing, observability, and a graceful-degradation story for when the database is the actual bottleneck.

## 2. Constraints

- **Throughput** — sustained QPS and peak QPS (peak/sustained ratio matters)
- **p99 latency target** — typically 100–500ms; defines cache hit-rate goals
- **Geographic distribution** — global vs single-region; affects edge strategy
- **Auth model** — public, API-key, signed (JWT, SigV4), per-user; affects caching
- **Idempotency requirements** — POST/PUT semantics for retries
- **Compliance** — PCI for payment, HIPAA for health, etc.
- **Budget** — at high QPS, infrastructure is the dominant cost; architecture decisions show up on the bill

## 3. Reference architecture

```
                          ┌──────────────────────────────────┐
                          │              Client              │
                          │   (browser, mobile, server)      │
                          └────────────────┬─────────────────┘
                                           │
                                           ▼
                          ┌──────────────────────────────────┐
                          │           Route 53               │
                          │   (latency-based / failover)     │
                          └────────────────┬─────────────────┘
                                           │
                                           ▼
                          ┌──────────────────────────────────┐
                          │           CloudFront             │
                          │   ┌──────────────────────────┐   │
                          │   │  WAF (managed rules,     │   │
                          │   │  rate-based rules,       │   │
                          │   │  geo, IP reputation)     │   │
                          │   └──────────────────────────┘   │
                          │   ┌──────────────────────────┐   │
                          │   │  Cache (cacheable GETs)  │   │
                          │   └──────────────────────────┘   │
                          └────────────────┬─────────────────┘
                                           │ origin pull
                                           ▼
                          ┌──────────────────────────────────┐
                          │   API Gateway (REST / HTTP)      │
                          │   - usage plans (per-key limits) │
                          │   - request validation           │
                          │   - authoriser (Lambda / Cognito)│
                          └────────────────┬─────────────────┘
                                           │
                                           ▼
                          ┌──────────────────────────────────┐
                          │        ALB (if container)        │
                          │   or direct Lambda integration   │
                          └────────────────┬─────────────────┘
                                           │
              ┌────────────────────────────┼────────────────────────────┐
              │                            │                            │
              ▼                            ▼                            ▼
       ┌──────────────┐            ┌──────────────┐             ┌──────────────┐
       │   Lambda     │            │ ECS Fargate  │             │  ElastiCache │
       │  (low-state, │            │  (steady     │             │   (read      │
       │   bursty)    │            │   traffic)   │             │   cache)     │
       └──────┬───────┘            └──────┬───────┘             └──────────────┘
              │                            │
              └────────────┬───────────────┘
                           │
                           ▼
                   ┌──────────────┐
                   │   Database   │
                   │  (DynamoDB,  │
                   │   Aurora,    │
                   │   ...)       │
                   └──────────────┘
```

1. **Route 53** — latency-based routing for multi-region; health checks for failover.
2. **CloudFront** — global edge cache; WAF inspection at edge before request reaches origin; absorbs L7 DDoS; serves cacheable GETs without origin hit.
3. **WAF** — managed rule sets (OWASP, bot control), rate-based rules per IP, geo restrictions if relevant. Counts mode in non-prod first; block mode in prod.
4. **API Gateway** — request validation (schema), authoriser (Cognito or custom Lambda), per-API-key rate limits via usage plans.
5. **Compute** — Lambda for spiky traffic and low-utilisation endpoints; ECS Fargate for steady traffic and lower per-request cost; mix is normal.
6. **Cache** — ElastiCache (Redis/Valkey) in front of expensive reads; per-tenant or per-key cache keys.
7. **Database** — chosen based on access patterns; Aurora with read replicas for SQL, DynamoDB with adaptive capacity for key-value.

## 4. Architecture variants

| Variant | When | Notes |
|---------|------|-------|
| **CloudFront → API Gateway → Lambda** | Default; bursty / unpredictable | Auto-scales to zero; cold starts a concern at p99 |
| **CloudFront → API Gateway → Fargate** | Steady high traffic | Lower per-request cost; no cold start |
| **CloudFront → ALB → Fargate** | API Gateway features unneeded | Lower latency; no API Gateway cost |
| **CloudFront → AppSync (GraphQL)** | GraphQL workloads | Caching, subscriptions, real-time |
| **Multi-region active-active** | Strict uptime SLA | Aurora Global, DynamoDB Global Tables; complex |
| **Edge compute (Lambda@Edge / CloudFront Functions)** | Personalisation at edge | Functions = JS only, microsecond, free; Edge = Python/Node, ms, paid |
| **Cell-based architecture** | Massive scale (>100k QPS) | Tenants partitioned across independent cells |

## 5. Failure modes

Cross-cutting patterns: see [`failure-first.md`](failure-first.md). High-scale-API-specific:

### Database is the actual bottleneck

- **What it looks like** — API latency spikes, all tracing arrows point at DB calls
- **Why it happens** — connection pool exhaustion, hot row, missing index, scan
- **Recovery** — read cache (ElastiCache), RDS Proxy for connection multiplexing, query analysis, indexes; for DynamoDB hot partitions, redistribute keys

### Cache stampede

- **What it looks like** — cache entry expires under heavy load; thousands of requests hit DB simultaneously to refill it
- **Recovery** — single-flight refill (only one request rebuilds cache, others wait), pre-warming, jittered TTL, request coalescing at API Gateway via cache key

### Bot / scraper traffic

- **What it looks like** — sudden traffic increase from a few IPs or a botnet; pattern doesn't match real users
- **Recovery** — WAF Bot Control managed rule, rate-based rules per IP, CAPTCHA challenge for ambiguous traffic, honeypot endpoints

### L7 DDoS

- **What it looks like** — sustained high QPS; CloudFront and WAF absorb, but origin still gets hit
- **Recovery** — Shield Advanced for protection + cost protection; rate limits per source IP; geo-block if attack is geographically clustered; AWS Shield response team engagement

### Hot tenant / customer

- **What it looks like** — one customer's traffic exceeds others combined; their pain becomes everyone's pain
- **Recovery** — per-tenant rate limits at API Gateway usage plans; per-tenant Lambda reserved concurrency; cell isolation for top tenants; see [`multi-tenant-saas.md`](multi-tenant-saas.md)

### Lambda concurrency exhausted

- **What it looks like** — Lambda throttling, 429s; downstream services unaffected (they're fine — Lambda just can't take the work)
- **Why it happens** — account-level concurrency limit, function-level reserved concurrency too low, or runaway recursive invocation
- **Recovery** — request quota increase (account); raise reserved concurrency; check for unbounded retries / recursion

### Provider outage in primary region

- **What it looks like** — health checks fail; traffic must shift
- **Recovery** — Route 53 health checks + failover record; warm standby in secondary region; data replication validated; **drill quarterly** — see [`failure-first.md`](failure-first.md#8-regional-failover)

### Slow downstream

- **What it looks like** — third-party API or downstream service slows down; your API's threads/connections exhaust waiting
- **Recovery** — strict timeouts on every downstream call (shorter than your own SLA); circuit breaker for repeated failures; graceful degradation (return partial data); see [`failure-first.md`](failure-first.md#5-circuit-breakers)

## 6. Cost model

Worked example: 100M requests/month, 80% cacheable GETs, 20% writes, p50 5KB response.

| Line item | Monthly | Notes |
|-----------|---------|-------|
| CloudFront requests | $75 | $0.0075 per 10k HTTPS requests in North America/Europe |
| CloudFront data transfer | ~$50 | 500GB at $0.085/GB tier 1 |
| WAF (managed rules + custom) | ~$60 | $5/rule + $0.60/M requests |
| API Gateway HTTP API | $100 | $1.00 per million |
| Lambda (20M writes × 200ms × 512MB) | ~$70 | Bulk of compute for writes |
| Cache hits absorbed by CloudFront | $0 | Origin doesn't see them |
| ElastiCache (cache.r6g.large × 2) | ~$200 | For application-layer cache |
| DynamoDB on-demand (40M writes, 100M strongly-consistent reads) | ~$60 | Reads cheaper if eventually consistent |
| Route 53 health checks + queries | ~$5 | Marginal |
| **Total** | **~$620** | ~$0.0062 per request |

**Scaling shape:** sub-linear above ~10M requests/month due to CloudFront tiered pricing; linear for compute and database. **Cache hit rate is the biggest cost lever** — going from 50% → 80% cache hits cuts compute roughly in half.

**Cost traps:**
- **No CloudFront cache hit rate alarm** — silent regression (cache key changes, TTL drops) shows up in compute bill
- **API Gateway REST when HTTP API works** — REST is $3.50/M, HTTP is $1.00/M; REST has more features but most APIs don't need them
- **Lambda over-provisioned memory** at this volume — 100M × even 100MB extra = real money; [Power Tuning](https://github.com/alexcasalboni/aws-lambda-power-tuning)
- **WAF rate-based rules with low limits** — WAF charges per request inspected; running every request through 10 rules adds up

## 7. When NOT to use this

- **Tiny API at low volume** — single ALB + Fargate without CloudFront/WAF/edge is fine until you have abuse, scale, or geographic users
- **Internal-only API** — most of this stack is overkill for VPC-internal
- **Real-time bidirectional** — use AppSync subscriptions, API Gateway WebSockets, or AWS IoT Core
- **WebSocket-heavy workload** — different scaling primitives; use API Gateway WebSocket or IoT

## 8. Alternatives

| Approach | Best for | Tradeoff |
|----------|----------|----------|
| **CloudFront + API Gateway + Lambda (this playbook)** | Default | Mix of cost levers; many moving parts |
| **CloudFront + ALB + Fargate** | Steady traffic, no API Gateway features | Cheaper per-request at scale |
| **CloudFront + AppSync** | GraphQL | Built-in caching, subscriptions |
| **CloudFront → S3** | Static / pre-rendered | Almost free at scale; only fits static content |
| **App Runner / Elastic Beanstalk** | Smaller teams, prefer managed | Less control; cost premium |
| **Cloudflare in front of AWS** | Best-in-class WAF + edge | Multi-vendor; egress to AWS still applies |
| **API on Cloudflare Workers** | Edge-native, low cost | Different runtime; AWS data still has egress |

For X-vs-Y depth: [CloudFront vs Cloudflare](https://www.factualminds.com/compare/aws-cloudfront-vs-cloudflare/), [WAF vs Network Firewall](https://www.factualminds.com/compare/aws-waf-vs-network-firewall/).

## 9. Anti-patterns

- **No edge cache** — every request hits origin; latency and cost both worse
- **Cache key includes per-user data** for cacheable endpoints — cache hit rate ~0%; cache is dead weight
- **WAF in count mode permanently** — collecting data isn't blocking; flip to block when confidence is high
- **Rate limiting only at one layer** — defense-in-depth: edge (CloudFront), gateway (API GW usage plans), app (in-process)
- **Letting Lambda concurrency scale unbounded** — runaway invocation drains account-level concurrency, breaks every other Lambda; reserved concurrency caps the blast radius
- **Public API with no API key / auth** — abuse is inevitable; require keys for usage tracking even if you don't otherwise need auth
- **Single AZ deployment** — AZ outage = total outage
- **Cold starts ignored** at p99 — Lambda cold starts dominate p99 latency; provisioned concurrency for hot paths
- **Health check that exercises the database** — promotes partial outage to total outage; see [`anti-patterns.md`](anti-patterns.md#health-check-that-calls-the-database)
- **No canary / staged rollout** — bad deploys are global incidents
- **Logs / metrics dropped on hot path for cost** — debugging the next outage requires data; structured logs are cheap with sampling
- **Tight coupling to a specific availability zone** — for HA, cross-AZ; for cost, intra-AZ; can't have both, pick consciously

For cross-cutting AWS anti-patterns, see [`anti-patterns.md`](anti-patterns.md).

## 10. Production checklist

- [ ] **CloudFront** in front of every public origin; cache behaviours tuned per route
- [ ] **WAF** with managed rules (Core, Bot Control, IP Reputation), rate-based per-IP rule, custom rules for known abuse patterns
- [ ] **Shield Standard** included free with CloudFront; **Shield Advanced** if SLA / cost-protection demands it
- [ ] **Origin Access Control** (or restricted security group) so origin only accepts traffic from CloudFront
- [ ] **API Gateway usage plans** for per-API-key limits
- [ ] **Authoriser caching** (TTL >0) so every request doesn't re-call the authoriser Lambda
- [ ] **Request validation** schemas at API Gateway (reject malformed at edge)
- [ ] **Lambda reserved concurrency** on hot paths; per-tenant reservations in multi-tenant
- [ ] **Provisioned concurrency** on cold-start-sensitive paths (paid; targeted use)
- [ ] **ElastiCache** for hot reads; cache key includes tenant context if multi-tenant
- [ ] **Connection pooling** — RDS Proxy in front of RDS; DAX in front of DynamoDB if appropriate
- [ ] **Strict timeouts** on every downstream call; circuit breakers on flaky dependencies
- [ ] **Idempotency keys** on POST/PUT — see [`failure-first.md`](failure-first.md#2-idempotency)
- [ ] **CloudWatch alarms** — error rate, p99 latency, 5xx, cache hit rate, Lambda concurrency, throttles
- [ ] **Distributed tracing** — X-Ray or OpenTelemetry; trace context propagated to downstream
- [ ] **Cost alarms** at multiple thresholds; per-service breakdowns
- [ ] **Multi-AZ deployment** end-to-end (compute, cache, DB)
- [ ] **DR plan** with documented RTO/RPO; quarterly drill
- [ ] **Canary / staged deploys** with automated rollback on regression
- [ ] **Capacity plan** — top-line traffic forecast vs account quotas with margin

## 11. References

**Official:**
- [API Gateway Documentation](https://docs.aws.amazon.com/apigateway/) — REST, HTTP API, WebSocket
- [API Gateway throttling](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-request-throttling.html) — account, stage, key-level limits
- [CloudFront Documentation](https://docs.aws.amazon.com/cloudfront/) — distribution, behaviours, cache keys
- [AWS WAF Documentation](https://docs.aws.amazon.com/waf/) — rules, managed rule groups, rate-based rules
- [AWS Shield](https://aws.amazon.com/shield/) — DDoS protection
- [Lambda concurrency and throttling](https://docs.aws.amazon.com/lambda/latest/dg/lambda-concurrency.html) — reserved vs provisioned
- [ElastiCache Documentation](https://docs.aws.amazon.com/elasticache/) — Redis / Valkey / Memcached
- [DAX Documentation](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DAX.html) — DynamoDB cache
- [RDS Proxy Documentation](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/rds-proxy.html) — connection pooling
- [Caching challenges and strategies (Builders Library)](https://aws.amazon.com/builders-library/caching-challenges-and-strategies/) — when caches make things worse

**Decision guides:**
- [CloudFront vs Cloudflare](https://www.factualminds.com/compare/aws-cloudfront-vs-cloudflare/) — edge platform choice
- [WAF vs Network Firewall](https://www.factualminds.com/compare/aws-waf-vs-network-firewall/) — L7 vs L3/L4 filtering
- [EC2 vs Lambda](https://www.factualminds.com/compare/aws-ec2-vs-lambda/) — compute choice for API workers
- [Lambda vs ECS Fargate](https://www.factualminds.com/compare/aws-lambda-vs-ecs-fargate/) — bursty vs steady

**OSS tools:**
- [aws-lambda-powertools-python](https://github.com/aws-powertools/powertools-lambda-python) — tracing, metrics, logger
- [opossum](https://github.com/nodeshift/opossum) — circuit breaker for Node.js
- [resilience4j](https://github.com/resilience4j/resilience4j) — circuit breaker / retry / bulkhead for JVM
- [k6](https://github.com/grafana/k6) — load testing
- [Locust](https://github.com/locustio/locust) — load testing in Python

---

*See also: [`failure-first.md`](failure-first.md) · [`multi-tenant-saas.md`](multi-tenant-saas.md) · [`cost-pitfalls.md`](cost-pitfalls.md) · [`decision-trees.md`](decision-trees.md#caching--where-does-the-cache-live).*
