# Anti-patterns: what teams get wrong on AWS

> The mistakes that show up across every workload — drawn from postmortems, bill-shock stories, and migrations done twice. Each entry: what teams do, why it bites, the better pattern.
>
> Workload-specific anti-patterns live in their playbook's §9. This catalog is the cross-cutting layer.

---

## Compute

### Lambda for >15 minute or CPU-bound jobs

**What teams do:** chain multiple Lambda invocations to handle long-running work, or run heavy CPU/ML inference inside Lambda.

**Why it bites:** Lambda has a 15-minute hard limit. CPU is allocated proportional to memory; you pay for memory whether you need it or not. Cold starts add up. ML model loading dominates.

**Better:** AWS Batch for batch jobs. ECS Fargate for long-running services. SageMaker / Bedrock for inference. Step Functions if you genuinely need to chain — but that's usually a workflow problem, not a duration problem.

### Lambda for low-latency hot paths without provisioned concurrency

**What teams do:** put Lambda behind a customer-facing API and discover p99 includes cold starts.

**Why it bites:** cold start adds 100ms–10s depending on runtime, package size, VPC config, and language. p99 latency is dominated by the slowest 1%.

**Better:** provisioned concurrency for predictable hot paths. Or pick Fargate if "always warm" is the dominant requirement and Lambda's autoscaling isn't needed.

### Lambda inside a VPC without need

**What teams do:** put Lambda in a VPC for "security" without checking what it actually needs to access.

**Why it bites:** historically added significant cold-start cost; now better but still adds elastic network interface management overhead. Often the resource the Lambda needs (DynamoDB, S3, Secrets Manager) is reachable via VPC endpoint or doesn't need VPC at all.

**Better:** keep Lambda outside VPC unless it must reach something only inside VPC (e.g., RDS without RDS Proxy public endpoint, internal microservice). Use VPC endpoints for AWS services to avoid NAT Gateway costs.

### Microservices before product-market fit

**What teams do:** decompose into 12 services on day one because "that's what scales."

**Why it bites:** distributed monolith. Every change crosses three repos. Local dev requires Docker Compose with 12 containers. The team is 4 engineers.

**Better:** modular monolith first. Split when (a) different parts have different scaling requirements, (b) different teams own different parts, or (c) deploy cadence diverges. Not earlier.

---

## Storage and databases

### DynamoDB without modelling access patterns

**What teams do:** throw entities into DynamoDB the way they'd use a relational DB. Generic `id` partition key. `Scan` everywhere. Hot partitions on a customer-id key.

**Why it bites:** DynamoDB cost is fine when access patterns match the keys; it's catastrophic when they don't. `Scan` reads the whole table. Hot partitions throttle. Eventually you'll need a secondary index, then another, then your bill is 4× what it should be.

**Better:** list every access pattern *before* schema. Single-table design. PK and SK chosen to make access patterns O(1). Use GSIs sparingly and intentionally.

### Treating DynamoDB and RDS as interchangeable

**What teams do:** "we'll migrate from DynamoDB to RDS later" or vice versa.

**Why it bites:** they're not the same shape. DynamoDB enforces access-pattern thinking; RDS enforces schema thinking. Migrating either direction is a rewrite, not a swap.

**Better:** pick once with eyes open. [DynamoDB vs RDS](https://www.factualminds.com/compare/dynamodb-vs-rds/).

### RDS without RDS Proxy and a connection pool plan

**What teams do:** Lambda → RDS direct, scale to thousands of concurrent invocations, RDS hits `max_connections`.

**Why it bites:** RDS Postgres `max_connections` defaults are low (often 100–500). Each Lambda invocation opens a connection; thousands of cold Lambdas = thousands of connection attempts = RDS goes down.

**Better:** RDS Proxy in front of RDS for any Lambda → RDS path. Or use Aurora Serverless v2 with its larger connection ceiling. Or skip relational entirely if access patterns fit DynamoDB.

### S3 small-object PUT-heavy without aggregation

**What teams do:** write one S3 object per event for a 100k events/sec stream.

**Why it bites:** S3 PUT is $0.005 per 1k requests. 100k/sec = $0.50/sec = $1.3M/month in PUT charges alone. Plus a lot of small objects make Athena and other downstream tools slow.

**Better:** Kinesis Firehose with buffering (60s/5MB) writes batched objects. Or aggregate in-memory in your producer and PUT periodically.

### One DynamoDB table per tenant

**What teams do:** create a fresh table per customer in a multi-tenant SaaS.

**Why it bites:** AWS account table-count limit (default 2,500); per-table overhead; cross-tenant queries become impossible; capacity planning per table is brittle.

**Better:** single table, tenant ID as the leading partition key component. See [`multi-tenant-saas.md`](multi-tenant-saas.md).

### CloudWatch logs as a queryable data store

**What teams do:** "we'll just CloudWatch Logs Insights it" for high-volume application logs.

**Why it bites:** CloudWatch Logs Insights is $0.005 per GB scanned. Multi-month queries scan everything. It's a debugging tool, not an analytics database.

**Better:** ship logs to S3 via Firehose, query with Athena ($5/TB scanned, partitioned). Use CloudWatch Logs Insights for hot debugging, not for analytics.

---

## Networking

### NAT Gateway as a silent budget killer

**What teams do:** put resources in private subnets behind a NAT Gateway. Every byte to AWS services (S3, DynamoDB, ECR pulls, Secrets Manager) goes via NAT.

**Why it bites:** $0.045/GB processed plus $0.045/hour per gateway plus per-AZ for HA. A noisy ECR puller can rack up four-figure bills weekly.

**Better:** **Gateway VPC endpoints** (free) for S3 and DynamoDB. **Interface VPC endpoints** for STS, Secrets Manager, ECR, KMS, etc. Reserve NAT for actual internet egress. See [`cost-pitfalls.md`](cost-pitfalls.md#nat-gateway).

### Cross-AZ chattiness

**What teams do:** spread services across AZs without pinning paths together. Service A in AZ-1 calls Service B in AZ-2 calls DB in AZ-3.

**Why it bites:** $0.01/GB each direction for cross-AZ data transfer. Adds latency. Multiplies if a request crosses many service boundaries.

**Better:** AZ affinity for tightly-coupled services where possible (ALB cross-zone load balancing off; topology-aware routing in EKS). Multi-AZ for redundancy, single-AZ paths for hot loops.

### Single-region "scale" with no DR plan

**What teams do:** scale a single region indefinitely; treat multi-region as future work.

**Why it bites:** when AWS has a regional event (real, not theoretical — they happen yearly), you have nothing.

**Better:** even at small scale, have a backup-restore plan to a second region. Document RTO/RPO. Drill once. The realisation that you can't actually rebuild somewhere else is the real lesson.

### Public S3 buckets by default

**What teams do:** flip "block public access" off for one file, leave it off, leak data later.

**Why it bites:** every public-bucket data leak in the news.

**Better:** account-level Block Public Access on, always. Serve public assets via CloudFront with Origin Access Control. Use pre-signed URLs for time-limited public access.

---

## Reliability and operations

### Auto-retry without idempotency

**What teams do:** wrap calls in retry-with-backoff. Don't think about whether the operation is idempotent. Side-effects fire twice.

**Why it bites:** double charges, duplicate emails, two orders. Some can't be undone.

**Better:** [idempotency keys on every state-changing operation](failure-first.md#2-idempotency). Retries become safe.

### DLQ exists, no alarm

**What teams do:** configure a DLQ on SQS or Lambda. Forget to alarm on it. Six months later: "where did all those events go?"

**Why it bites:** silent data loss. The DLQ is an alert mechanism; without an alarm it's a graveyard.

**Better:** alarm on `ApproximateNumberOfMessagesVisible > 0` with a clear runbook. See [`failure-first.md`](failure-first.md#3-dead-letter-queues-dlqs).

### Health check that calls the database

**What teams do:** `/health` does `SELECT 1` from the database, returns 200 only if it succeeds. ELB uses this as the target health check.

**Why it bites:** database hiccups → every target unhealthy → ELB has no targets → service is down even though it could've served from cache. Partial outage promoted to total outage.

**Better:** shallow `/health` for ELB (process is alive). Separate `/diagnostics` for deep checks, used by humans, never by ELB.

### IAM `*` policies in production

**What teams do:** "we'll tighten IAM later." Lambda execution role has `s3:*`. Or worse, `*:*`.

**Why it bites:** first compromised credential = your entire S3. Compliance auditors will find this.

**Better:** least privilege from day one. AWS Access Analyzer to find unused permissions. Tag-based conditions for tenant scoping. Service control policies as a top-down guard.

### Hand-rolled secrets in environment variables

**What teams do:** put DB passwords, API keys, signing secrets in Lambda env vars or ECS task definitions. Commit to git "by mistake." Rotate by redeploying.

**Why it bites:** secrets in CloudFormation, in CloudTrail, in env-var dumps. Rotation requires deploy. Audit trail is impossible.

**Better:** Secrets Manager for credentials (auto-rotation for RDS, Aurora, DocumentDB). Parameter Store SecureString for less-frequent secrets. Reference by ARN in env vars; resolve at startup.

### No cost alarms

**What teams do:** check the bill at end of month.

**Why it bites:** runaway resource (NAT Gateway loop, Lambda recursion, DDoS) can rack up four-figure bills in hours.

**Better:** AWS Budgets with alerts at 50%, 80%, 100% of expected spend. CloudWatch Anomaly Detection on cost. Per-service alarms for the top spenders. **Reference:** [Protect AWS infrastructure from cost-based attacks](https://www.factualminds.com/blog/protect-aws-infrastructure-cost-based-attacks/).

---

## CI/CD and deployment

### Deploying to all customers at once

**What teams do:** push to main → deploy to production → all tenants/users see the change immediately.

**Why it bites:** every bad deploy is a global outage.

**Better:** ring deployments. Free tier first (or canary tenant), then paid tier, then enterprise. Watch error rates between rings. Auto-rollback on regression.

### Long-lived AWS access keys in CI

**What teams do:** create an IAM user with access keys, paste into GitHub Actions secrets, hope nobody leaks the repo.

**Why it bites:** keys leak (committed by mistake, exposed in build logs, team member offboarded but not rotated). Compliance issue.

**Better:** GitHub OIDC → AWS IAM role. No long-lived credentials. Per-workflow scoped role. Supported in CodePipeline equivalents too.

### Manual changes in the AWS console

**What teams do:** fix a production issue by clicking around in the console. Don't update Terraform / CDK. Drift accumulates.

**Why it bites:** next deploy reverts the fix. Or worse, an unrelated change wipes the fix and nobody remembers it.

**Better:** infrastructure-as-code is the source of truth. Console is read-only for teams beyond ~5 people. Drift detection in CI (Terraform plan, CDK diff) on a schedule.

---

## Observability

### Logs without structure

**What teams do:** `console.log("user logged in: " + email)`. Plain text. Variable format.

**Why it bites:** you can't query it. Every debugging session is a grep-pipeline. CloudWatch Logs Insights kind of works on it, but you're paying $0.005/GB to do regex.

**Better:** structured JSON logs always. Standard fields (`timestamp`, `level`, `service`, `request_id`, `tenant_id` if multi-tenant). AWS Powertools or equivalent.

### Metric per request without dimension hygiene

**What teams do:** emit a CloudWatch custom metric with high-cardinality dimensions (user ID, request ID).

**Why it bites:** CloudWatch is $0.30 per metric per month. High cardinality = millions of metrics = thousands of dollars.

**Better:** use **Embedded Metric Format** so high-cardinality dimensions stay in logs but aggregated metrics stay cheap. Or push high-cardinality data to a real telemetry backend (X-Ray, Honeycomb, Datadog).

### No request ID propagation

**What teams do:** each service generates its own request ID. Correlating across services means timestamps and praying.

**Why it bites:** debugging cross-service issues becomes archaeology.

**Better:** pass `X-Request-Id` (or trace context) through every hop. Log it on every line. Bonus: full distributed tracing with OpenTelemetry / X-Ray.

---

## Security

### Long-lived IAM users for humans

**What teams do:** create IAM users for engineers. They use access keys for CLI access.

**Why it bites:** keys end up in `~/.aws/credentials` files, leaked laptops, screenshots, Stack Overflow questions.

**Better:** IAM Identity Center for human SSO. Temporary credentials via AssumeRole. No long-lived keys for humans, ever.

### Security groups too open

**What teams do:** `0.0.0.0/0` on port 22 "for now." Or `0.0.0.0/0` on the database port "to debug."

**Why it bites:** every shodan-scanned port. Bots try defaults within minutes.

**Better:** SSM Session Manager replaces SSH (no inbound 22 needed). Database access via bastion or SSM tunnelling. Security group references over CIDR ranges where possible.

### KMS without key rotation or alias hygiene

**What teams do:** create KMS keys with default settings. Reference them by raw key ID. Forget to rotate.

**Why it bites:** rotation is automatic if enabled but isn't enabled by default for customer-managed keys. Raw key IDs make rotation/migration harder.

**Better:** enable rotation on customer-managed keys. Reference by alias (`alias/myapp-prod`) not key ID. Separate keys per data classification.

---

*See also: [`failure-first.md`](failure-first.md) · [`cost-pitfalls.md`](cost-pitfalls.md) · [The Amazon Builders' Library](https://aws.amazon.com/builders-library/) · [Bill teardowns in the root README](../README.md#cost-management--finops).*
