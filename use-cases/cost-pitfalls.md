# Cost pitfalls

> The line items that surprise teams. Each entry: what it costs, why it spirals, the mitigation.
>
> Pricing changes; verify on the linked AWS pricing page before committing to a number.

---

## NAT Gateway

**The cost:**
- $0.045/hour per NAT Gateway × 3 AZs for HA = $97/mo per region just to exist
- $0.045/GB processed
- 100GB/day egress × 30 days = $135/mo data processing alone

**Why it spirals:**
- Every byte from a private subnet to AWS services (S3, DynamoDB, ECR pulls, Secrets Manager) pays the data-processing fee
- Container builds and ECS task launches pull image layers via NAT
- Cross-region replication, cross-region writes, and OS package updates all flow here
- Cost is opaque: hidden in "Data Processing" line, not labelled "you forgot to use VPC endpoints"

**Mitigation:**
- **Gateway VPC endpoints** for S3 and DynamoDB — free, route via AWS backbone
- **Interface VPC endpoints** for STS, Secrets Manager, KMS, ECR, SSM, CloudWatch Logs, etc. — $7.20/endpoint/month per AZ but pays back fast at any volume
- Audit VPC flow logs to see what's actually going through NAT
- Consider [VPC Lattice](https://aws.amazon.com/vpc/lattice/) for service-to-service across VPCs without NAT

**Reference:** [VPC pricing](https://aws.amazon.com/vpc/pricing/) · [VPC endpoint types](https://docs.aws.amazon.com/vpc/latest/privatelink/concepts.html)

---

## Cross-AZ data transfer

**The cost:** $0.01/GB **each direction** between AZs in the same region. Yes, both ways.

**Why it spirals:**
- Multi-AZ ALB cross-zone load balancing → traffic re-routed across AZs unnecessarily
- DB primary in AZ-1, read replicas across AZs, app servers across AZs — every read can be a cross-AZ hop
- Kafka / MSK with multi-AZ replication: every write replicated × cross-AZ pricing
- Microservices gossiping across AZs at high QPS

**Mitigation:**
- **Topology-aware routing** in EKS / ECS Service Connect to keep traffic within AZ when possible
- ALB cross-zone load balancing **off** when target sets are evenly sized per AZ
- Kafka tiered storage and rack-aware producers
- For high-throughput intra-region, evaluate AWS PrivateLink or VPC peering (still has data transfer cost but sometimes cheaper paths)

**Reference:** [EC2 data transfer pricing](https://aws.amazon.com/ec2/pricing/on-demand/#Data_Transfer)

---

## CloudWatch Logs

**The cost:**
- **Ingestion:** $0.50/GB
- **Storage:** $0.03/GB/month
- **CloudWatch Logs Insights queries:** $0.005/GB scanned

**Why it spirals:**
- Verbose application logs with full request/response bodies
- Lambda logs every invocation by default; one chatty Lambda at 100 invocations/sec = ~1MB/sec = ~30TB/year ingestion = $15k/yr in ingestion alone
- VPC Flow Logs piped to CloudWatch instead of S3
- Default retention is **never expire** — pay storage forever

**Mitigation:**
- **Log retention** — set explicit retention (7d, 30d, 90d) on every log group
- **Sample debug logs** in production; INFO/WARN/ERROR only for steady state
- **Ship to S3** via subscription filter → Firehose → S3 (S3 storage is $0.023/GB; query with Athena for $5/TB)
- **VPC Flow Logs to S3**, not CloudWatch
- **CloudTrail to S3 only** unless you need real-time detection in CloudWatch
- **Embedded Metric Format** so structured fields become metrics without separate `PutMetricData` calls

**Reference:** [CloudWatch pricing](https://aws.amazon.com/cloudwatch/pricing/)

---

## Egress to internet

**The cost:**
- First 100GB/month free
- Up to 10TB/month: $0.09/GB
- Tiered down to ~$0.05/GB at 150TB/month

**Why it spirals:**
- API responses to mobile/web clients at scale
- Public image / video / file downloads
- API replies to webhooks back out to customer infrastructure
- Cross-cloud sync (data lake to BigQuery, etc.)

**Mitigation:**
- **CloudFront** for cacheable content — egress from CloudFront is cheaper than from EC2/S3 directly, and free between AWS and CloudFront edge
- **CloudFront origin shield** for additional cache layer
- **S3 + CloudFront** for static and media assets, never serve directly from S3 to public
- For API responses, evaluate compression (gzip, Brotli) and pagination — every byte saved is billed
- **Direct Connect** if egress is sustained and high-volume (custom pricing, requires negotiation)

**Reference:** [CloudFront pricing](https://aws.amazon.com/cloudfront/pricing/) · [Bill teardowns in root README](../README.md#cost-management--finops)

---

## DynamoDB hot partitions and scan-heavy tables

**The cost:**
- On-demand: $1.25 per 1M write requests, $0.25 per 1M read requests
- Provisioned: WCU $0.00065/hr, RCU $0.00013/hr
- A `Scan` reads every item — full-table scan on a 100GB table = millions of read units

**Why it spirals:**
- Bad partition key choice → hot partition → throttling → app retries → more capacity needed
- Generic `Scan` on a non-trivial table — once is fine, in a hot loop is catastrophic
- Switching from provisioned to on-demand "for autoscaling" — on-demand is 7× the per-request cost; only worth it for unpredictable workloads

**Mitigation:**
- Model partition key for **uniform distribution** — high-cardinality, well-distributed
- Use `Query` not `Scan`; create a GSI before resorting to `Scan`
- Provisioned + autoscaling for predictable workloads; on-demand only for unpredictable
- DynamoDB Reserved Capacity for stable workloads (1y or 3y commit, ~50% discount)
- Caching layer (DAX or ElastiCache) for hot reads

**Reference:** [DynamoDB pricing](https://aws.amazon.com/dynamodb/pricing/) · [Best practices for partition key design](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-partition-key-design.html)

---

## EBS gp2 vs gp3 (almost free win)

**The cost:**
- gp2: $0.10/GB/month, IOPS scales with volume size
- gp3: $0.08/GB/month + $0.005/IOPS-month above 3,000 baseline + $0.04/MBps-month above 125 baseline
- Most gp2 volumes can be migrated in-place to gp3 with **same or better** performance for **~20% less cost**

**Why teams miss it:** gp2 was the default for years; new accounts often still pick it; in-place migration is supported but not advertised.

**Mitigation:**
- AWS **Compute Optimizer** flags gp2 → gp3 migrations
- For most workloads, the gp3 default (3,000 IOPS, 125 MBps) is sufficient
- Migrate non-prod first, then prod during a maintenance window

**Reference:** [EBS pricing](https://aws.amazon.com/ebs/pricing/)

---

## Idle resources

**The cost:** EC2 / RDS / Aurora / ElastiCache instances run while idle. The bill keeps coming.

**Why it spirals:**
- Dev/test environments left running 24/7
- Pre-prod environments with same instance class as prod
- Decommissioned services with infra that nobody removed
- ELBs with no targets, EIPs not attached, EBS volumes unattached

**Mitigation:**
- **AWS Compute Optimizer** identifies under-utilised resources
- **AWS Trusted Advisor** flags idle resources (free at Business+ Support)
- **Instance Scheduler** to start/stop dev environments outside business hours
- **Savings Plans** for committed usage (up to 72% off vs on-demand for 3-year all-upfront)
- **Reserved Instances** for stable workloads on RDS, ElastiCache, OpenSearch
- **Resource cleanup** — tag everything with `owner` and `expires`; automate deletion of un-tagged resources after a grace period

**Reference:** [Compute Optimizer](https://aws.amazon.com/compute-optimizer/) · [Savings Plans](https://aws.amazon.com/savingsplans/)

---

## Lambda over-provisioned memory

**The cost:** Lambda billed per GB-second. Over-provisioning memory linearly multiplies cost.

**Why teams miss it:**
- Default 128MB is often too low (slow); first instinct is to crank to 1024MB or 3008MB
- More memory = more vCPU, so over-provisioned functions sometimes finish faster, but past a point you pay for unused capacity
- Optimal memory is workload-specific and counter-intuitive

**Mitigation:**
- **AWS Lambda Power Tuning** — open-source Step Functions tool that runs your function at every memory setting and plots cost vs duration
- Optimise for cost-per-invocation, not just speed
- Re-tune when code changes meaningfully

**Reference:** [Lambda Power Tuning](https://github.com/alexcasalboni/aws-lambda-power-tuning)

---

## Reserved capacity and Savings Plans

**The cost:** on-demand pricing is the highest tier. Committing buys discounts up to 72%.

**Why teams skip it:**
- Don't trust their forecast → leave money on the table
- One person owns commitments; that person leaves; nobody renews

**Mitigation:**
- **Compute Savings Plans** are flexible across EC2/Lambda/Fargate; commit at ~70% of stable baseline
- **EC2 Instance Savings Plans** lower discount, more flexible across families
- **Reserved Instances** for RDS, ElastiCache, OpenSearch — non-fungible, commit per family/region
- **Marketplace** for buying/selling unused RIs if your forecast changes
- **Cost Explorer recommendations** show specific commit suggestions backed by your usage history

**Cadence:** quarterly review. Don't over-commit (60–80% of baseline, not 100%) — you want flexibility for new workloads.

**Reference:** [Savings Plans](https://aws.amazon.com/savingsplans/) · [Reserved Instances](https://aws.amazon.com/ec2/pricing/reserved-instances/)

---

## Cross-region traffic

**The cost:**
- Inter-region: $0.02/GB (varies by source/destination region)
- Multiplied by replication factor for active-active multi-region

**Why it spirals:**
- Multi-region active-active without locality routing → users in EU hitting US backends
- DynamoDB Global Tables replication
- S3 Cross-Region Replication
- Logs / metrics / observability data centralised in one region

**Mitigation:**
- **Latency-based routing** at Route 53 to keep users in their nearest region
- For DR-only multi-region (warm standby), don't replicate hot data — replicate config and run minimal warm capacity
- Consolidate logs in S3 in primary region; replicate **selectively** to DR region

**Reference:** [Multi-region AWS without doubling costs](https://www.factualminds.com/blog/multi-region-aws-without-doubling-costs/)

---

## Free-tier-as-DoS

**The cost:** sign-up costs are real (Cognito MAU, S3 storage allocation, default IAM roles, Lambda invocations). Bots can incur spend without ever paying.

**Why it spirals:**
- Self-serve sign-up with no rate limit on account creation
- Free-tier customer with no usage caps consuming significant resources
- Adversary signs up many free accounts, runs expensive operations on each

**Mitigation:**
- **CAPTCHA / WAF** on sign-up endpoint
- **Email verification** before any provisioning
- **Per-tenant cost cap** — soft suspension at threshold
- **Anomaly detection** on per-tenant resource usage
- AWS WAF rate-limit rules

**Reference:** [Protect AWS infrastructure from cost-based attacks](https://www.factualminds.com/blog/protect-aws-infrastructure-cost-based-attacks/)

---

## Bedrock and GenAI tokens

**The cost:**
- Bedrock charges per 1k input tokens + per 1k output tokens; varies by model (Claude Sonnet 4.5 ≈ $3 in / $15 out per 1M tokens)
- Embedding models cheap per token but sum quickly at high volume
- Vector DB storage and query costs separate

**Why it spirals:**
- Long system prompts repeated per request without caching
- RAG pipelines retrieving more context than needed → token bloat → cost + latency
- Agent loops without termination conditions
- Streaming output where users abandon mid-stream — full output still billed

**Mitigation:**
- **Prompt caching** in Bedrock for repeated system prompts (significant discount)
- Tune retrieval `top_k`; measure precision before adding more context
- Cap agent iterations
- Per-tenant token budgets in multi-tenant SaaS
- Cheaper model for cheaper tasks (Haiku for routing, Sonnet for reasoning, Opus reserved)

**Reference:** [Bedrock pricing](https://aws.amazon.com/bedrock/pricing/) · [Multi-tenant GenAI on Bedrock](https://www.factualminds.com/blog/multi-tenant-genai-bedrock/)

---

## Tools to find these proactively

- **AWS Cost Explorer** — slice by service, tag, region; spot anomalies
- **AWS Budgets** — alarms at thresholds before bills land
- **AWS Cost Anomaly Detection** — ML-based detection on top of Cost Explorer
- **AWS Trusted Advisor** — free tier covers a small set; Business+ Support unlocks the full set
- **Compute Optimizer** — right-sizing for EC2, EBS, Lambda, ECS Fargate
- **AWS Pricing Calculator** — model before you build

---

## Cost discipline checklist

- [ ] Account-level budget with alarms at 50%, 80%, 100%, 150% of monthly target
- [ ] Per-service alarms on top 3 spenders
- [ ] Anomaly detection enabled
- [ ] Tag policy enforced via SCP; un-tagged resources flagged daily
- [ ] Cost Categories rolling tags up to per-team / per-product / per-tenant
- [ ] Quarterly Savings Plan review with commit at 60–80% of stable baseline
- [ ] Quarterly cleanup sweep — un-attached EBS volumes, idle ELBs, un-attached EIPs, unused snapshots
- [ ] VPC endpoint coverage audit — every AWS service Lambda/ECS reaches has an endpoint or a justification
- [ ] CloudWatch log retention policy on every log group
- [ ] EBS gp2 → gp3 migration completed
- [ ] Lambda Power Tuning run on top 5 most-invoked functions

---

*See also: [`anti-patterns.md`](anti-patterns.md) · [Bill teardowns and FinOps in root README](../README.md#cost-management--finops) · [Cost Optimization Pillar (whitepaper)](https://docs.aws.amazon.com/wellarchitected/latest/cost-optimization-pillar/).*
