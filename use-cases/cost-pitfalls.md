# Cost pitfalls

> The line items that surprise teams. Each entry: what it costs, why it spirals, the mitigation.
>
> Pricing changes; verify on the linked AWS pricing page before committing to a number.
>
> **Audit workbook:** [`cost-pitfalls-audit.xlsx`](cost-pitfalls-audit.xlsx) — filterable pitfall registry and quarterly checklist. Regenerate after edits: `uv run --python python3 --with openpyxl python3 scripts/generate_cost_pitfalls_audit.py`.

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

**Variant — Regional NAT Gateway:**
- Same $0.045/hour **per AZ where the regional NAT is configured** — three AZs still ≈ $97/mo baseline ($0.135/hr), not one flat hourly fee
- Same $0.045/GB data processing; hourly billing drops for an AZ only when AWS removes that AZ from the regional NAT footprint
- One managed NAT resource routes egress across AZs — simpler HA than per-AZ NAT failover, but **not** a way to cut idle NAT cost if all AZs stay in scope
- Workloads in AZ-a using the regional NAT ENI in AZ-b still pay [cross-AZ data transfer](#cross-az-data-transfer) on top of NAT processing
- Endpoint coverage still matters: regional NAT does not stop S3/ECR/Secrets Manager traffic from incurring NAT data-processing fees

**Reference:** [VPC pricing](https://aws.amazon.com/vpc/pricing/) · [NAT gateway pricing](https://docs.aws.amazon.com/vpc/latest/userguide/nat-gateway-pricing.html) · [VPC endpoint types](https://docs.aws.amazon.com/vpc/latest/privatelink/concepts.html)

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

## S3 small-object PUT-heavy without aggregation

**The cost:**
- S3 Standard PUT/COPY/POST/LIST: **$0.005 per 1,000 requests** (us-east-1; verify your region on the pricing page)
- Storage is cheap; **request charges dominate** when you write one tiny object per event
- Example: 100k PUTs/sec × 86,400 sec/day × 30 days ≈ 259B requests/month → **~$1.3M/month in PUT fees alone** (before storage)

**Why it spirals:**
- Async job workers writing one result object per job (see [`async-jobs.md`](async-jobs.md))
- Event streams landing as individual S3 objects instead of batched files
- No lifecycle policy — millions of small objects accumulate; Athena/Glue partition scans get slow and expensive downstream
- Request charges are easy to miss in Cost Explorer until you filter by **S3 Requests** usage type

**Mitigation:**
- **Batch before PUT** — buffer in memory or Kinesis Data Firehose (60s / 5MB buffering) so one object holds many events
- **Aggregate job outputs** — write NDJSON or Parquet files on a schedule, not per invocation
- **Lifecycle rules** — expire scratch prefixes after N days; transition cold prefixes to IA or Intelligent-Tiering
- **Cost Explorer** — slice S3 spend by usage type; use [S3 Storage Lens](https://docs.aws.amazon.com/AmazonS3/latest/userguide/storage_lens.html) or CUR to find high-PUT buckets

**Reference:** [S3 pricing](https://aws.amazon.com/s3/pricing/) · [Optimize S3 API request charges (AWS Storage Blog)](https://aws.amazon.com/blogs/storage/optimize-storage-costs-by-analyzing-api-operations-on-amazon-s3/) · [`anti-patterns.md` — same pattern](anti-patterns.md#s3-small-object-put-heavy-without-aggregation)

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

**Reference:** [Compute Optimizer](https://aws.amazon.com/compute-optimizer/) · Savings Plans (linked under Reserved capacity and Savings Plans below)

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
- **Prompt caching** for repeated prefixes (system prompts, RAG documents, tool definitions) — cached reads bill at a reduced rate; cache writes can cost more than standard input tokens. Claude Sonnet 4.5 requires **≥4,096 tokens** per cache checkpoint (TTL: 5 minutes or 1 hour). Place static context first so it hits the cache.
- Tune retrieval `top_k`; measure precision before adding more context
- Cap agent iterations
- Per-tenant token budgets in multi-tenant SaaS
- Cheaper model for cheaper tasks (Haiku for routing, Sonnet for reasoning, Opus reserved)

**Reference:** [Bedrock pricing](https://aws.amazon.com/bedrock/pricing/) · [Prompt caching (Bedrock User Guide)](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html) · [Multi-tenant GenAI on Bedrock](https://www.factualminds.com/blog/multi-tenant-genai-bedrock/)

---

## Quarterly optimization cadence

Run this workflow every quarter (or after a bill spike). Each step maps to sections elsewhere in this playbook and the [Cost Management & FinOps](../README.md#cost-management--finops) index.

1. **Visibility** — Slice [Cost Explorer](https://aws.amazon.com/aws-cost-management/aws-cost-explorer/) by service, tag, and region. Review [Cost Optimization Hub](https://aws.amazon.com/aws-cost-management/cost-optimization-hub/) or CUR exports for recommendations. Triage open [Cost Anomaly Detection](https://aws.amazon.com/aws-cost-management/aws-cost-anomaly-detection/) alerts.

2. **Waste** — Hunt idle EC2, RDS, ELB, EIP, and unattached EBS ([Idle resources](#idle-resources)). Use Trusted Advisor, [Finala](https://github.com/similarweb/finala), or Cost Optimization Hub idle-resource findings.

3. **Rightsizing** — Export [Compute Optimizer](#idle-resources) recommendations for EC2, EBS, Lambda, and RDS. Run [Lambda Power Tuning](#lambda-over-provisioned-memory) on the top 10 functions by spend. Migrate remaining gp2 volumes to gp3 ([EBS gp2 vs gp3](#ebs-gp2-vs-gp3-almost-free-win)).

4. **Commitments** — Review Savings Plans and RI coverage in Cost Explorer. Commit at **60–80%** of stable baseline, not 100% ([Reserved capacity and Savings Plans](#reserved-capacity-and-savings-plans)).

5. **Architecture** — [VPC endpoint coverage audit](#nat-gateway) for every service Lambda or ECS reaches. Set S3 [lifecycle policies](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lifecycle-mgmt.html) and Intelligent-Tiering where access is unpredictable. Review cross-AZ topology ([Cross-AZ data transfer](#cross-az-data-transfer)).

6. **Governance** — Verify required tag keys and [Cost Categories](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/manage-cost-categories.html). Refresh budget thresholds and [budget actions](https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-action-configure.html). Update team-facing billing views if org structure changed.

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
- [ ] Compute Optimizer recommendations reviewed for EC2, EBS, Lambda, and RDS
- [ ] Savings Plans / RI coverage within 60–80% of stable baseline
- [ ] Spot or Fargate Spot evaluated for fault-tolerant batch and CI workloads
- [ ] S3 lifecycle and Intelligent-Tiering on buckets without a retention policy
- [ ] Cost Categories and required tag keys enforced (Tag Policies or Config rules)
- [ ] Quarterly Savings Plan review with commit at 60–80% of stable baseline
- [ ] Quarterly cleanup sweep — un-attached EBS volumes, idle ELBs, un-attached EIPs, unused snapshots
- [ ] VPC endpoint coverage audit — every AWS service Lambda/ECS reaches has an endpoint or a justification
- [ ] CloudWatch log retention policy on every log group
- [ ] EBS gp2 → gp3 migration completed
- [ ] Lambda Power Tuning run on top 5 most-invoked functions

---

*See also: [`anti-patterns.md`](anti-patterns.md) · [Bill teardowns and FinOps in root README](../README.md#cost-management--finops) · [Cost Optimization Pillar (whitepaper)](https://docs.aws.amazon.com/wellarchitected/latest/cost-optimization-pillar/).*
