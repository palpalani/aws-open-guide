# Decision trees: which AWS service for which job

> When you know the workload but not the service. Decision trees + selection tables for the questions teams ask most often.
>
> For X-vs-Y comparisons (EC2 vs Lambda, RDS vs Aurora, …), see the [Decision Guides section in the root README](../README.md#decision-guides--x-vs-y). This doc starts from the workload and lands on a service; that section starts from two services and picks one.

---

## Event processing — what runs in response to an event?

```
                     What kind of event?
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
   Domain event         Message /          Stream of records
   (order created)      command             (clickstream, IoT)
        │                   │                   │
        ▼                   ▼                   ▼
   EventBridge          SQS / SNS          Kinesis Data Streams
   (routing,            (queueing,         (ordered, replayable,
    schemas,            fan-out)            sharded)
    archive)
        │                   │                   │
        ▼                   ▼                   ▼
   Targets: Lambda,    Consumers: Lambda,  Consumers: Lambda,
   Step Functions,     ECS, on-prem        Kinesis Data
   API destinations,                       Firehose, Flink
   SQS, SNS
```

**When in doubt:** EventBridge for cross-service domain events; SQS for "I have work to do later"; Kinesis when ordering or replay matters.

| If the workload… | Pick | Why |
|------------------|------|-----|
| Domain events crossing service boundaries, schemas matter | **EventBridge** | Built-in schema registry, archive/replay, content-based routing |
| Background jobs, retry-and-DLQ pattern, low/medium volume | **SQS** | Simplest reliable queue; FIFO if ordering needed |
| Fan-out one event to many subscribers | **SNS** | Pub/sub; pair with SQS for durable subscribers |
| High-volume telemetry / clickstream / IoT / log shipping | **Kinesis Data Streams** | Ordered shards, 24h–365d retention, replayable |
| Append to S3/Redshift/OpenSearch with buffering, no compute | **Kinesis Data Firehose** | Fully managed delivery, built-in transforms |
| Stateful stream processing, windowing, joins | **Managed Service for Apache Flink** | Real-time SQL/Java/Python with state |
| Real-time analytics over hot data | **OpenSearch Ingestion / Kinesis → OpenSearch** | Full-text + aggregations |

**Don't use:**
- Lambda direct invocation across services for events that should be auditable — use EventBridge so there's a record
- SNS without an SQS subscriber if delivery is critical and the subscriber can be down
- Kinesis when you don't need ordering or replay — SQS is cheaper and simpler

Cross-links: [`failure-first.md`](failure-first.md) for retries/DLQs, [`anti-patterns.md`](anti-patterns.md) for queue mistakes.

---

## Database — where does the data live?

```
                     What's the access pattern?
                            │
        ┌───────────────────┼───────────────────────┐
        │                   │                       │
   Key-value /         Relational              Search /
   item lookup         (joins, transactions)   ranking / aggregation
        │                   │                       │
        ▼                   ▼                       ▼
   DynamoDB            RDS or Aurora           OpenSearch
        │                   │                       │
        │              ┌────┴────┐                  │
        │         Aurora       RDS                  │
        │       (cloud-native, (managed             │
        │        Serverless v2) Postgres/MySQL)     │
        ▼                                            ▼
   DAX (cache),                              + DynamoDB or RDS
   Streams (CDC)                              as system of record
                                              (OpenSearch is index,
                                               not source of truth)
```

| Access pattern | Pick | Notes |
|----------------|------|-------|
| Known partition key, single-digit ms reads | **DynamoDB** | Single-table design; model access patterns first |
| Joins, transactions, complex filters | **RDS / Aurora** | Aurora for cloud-native scale; RDS for compatibility |
| Time-series telemetry, IoT, observability data | **Timestream LiveAnalytics** [maintenance] → **InfluxDB on AWS or OpenSearch** | Timestream is in maintenance per AWS lifecycle |
| Document store with rich query | **DocumentDB** or **MongoDB Atlas on AWS** | DocumentDB for tighter AWS integration; Atlas for full Mongo feature set |
| Graph (social, fraud, RAG over relationships) | **Neptune** | Property graph + RDF |
| Analytics warehouse | **Redshift** or **Snowflake on AWS** | Redshift Serverless for low-floor; Snowflake for cross-cloud |
| Data lake querying | **Athena** | SQL on S3; pair with Glue Data Catalog |
| Vector search (RAG) | **OpenSearch with k-NN**, **Aurora pgvector**, **DocumentDB vector** | Pick based on existing stack |
| Embedded cache | **ElastiCache (Redis / Valkey / Memcached)** | Redis for richer data types |

**Common multi-database patterns:**
- DynamoDB system of record + OpenSearch projection for search
- RDS system of record + ElastiCache for hot reads
- S3 data lake + Athena for ad-hoc + Redshift for BI

For X-vs-Y depth: [DynamoDB vs RDS](https://www.factualminds.com/compare/dynamodb-vs-rds/), [RDS vs Aurora](https://www.factualminds.com/compare/aws-rds-vs-aurora/), [Aurora Serverless vs Provisioned](https://www.factualminds.com/compare/aws-aurora-serverless-vs-aurora-provisioned/), [Which AWS database](https://www.factualminds.com/decide/which-aws-database/).

---

## Compute — where does the code run?

```
                  How long does the job run?
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
    < 15 min,           Long-running        Heavy CPU/GPU
    request-response    container           batch (>15min,
        │               or worker            specialised HW)
        │                   │                   │
        ▼                   ▼                   ▼
   Lambda             ┌─────────┐           AWS Batch
   (provisioned       │  ECS    │           (or EC2 spot
    concurrency       │ Fargate │            if you need
    if cold start     │  vs     │            full control)
    matters)          │  EC2    │
                      └────┬────┘
                           │
              Stable utilisation? → EC2 Reserved
              Bursty / unknown?   → Fargate (no nodes to manage)
              Need specific HW?   → EC2 (GPU, bare-metal)
              Already on K8s?     → EKS (Fargate or EC2)
```

| Workload | Pick | Why |
|----------|------|-----|
| HTTP API request-response, ≤15min, sub-second cold-start tolerance | **Lambda** | Auto-scales to zero; no idle cost |
| Same as above but cold-start sensitive | **Lambda + provisioned concurrency** or **Fargate** | Fargate has no cold start at the cost of always-on |
| Long-running services (>15min) | **ECS Fargate** | Managed, no node ops |
| Heavy CPU / GPU / specialised hardware | **EC2** | Full instance type catalogue |
| Existing Kubernetes investment | **EKS (Fargate or managed nodes)** | Reuse K8s tooling; bring your own cluster ops |
| Batch jobs, scientific compute | **AWS Batch** | Job queues + compute environments + spot |
| Spiky, unpredictable workloads | **Lambda or Fargate Spot** | Pay-per-use, scale-to-zero |
| Edge / low-latency to user | **Lambda@Edge** or **CloudFront Functions** | Functions are JS-only and faster; Edge supports Python/Node and longer-running |

For X-vs-Y depth: [EC2 vs Lambda](https://www.factualminds.com/compare/aws-ec2-vs-lambda/), [Lambda vs ECS Fargate](https://www.factualminds.com/compare/aws-lambda-vs-ecs-fargate/), [ECS vs EKS](https://www.factualminds.com/compare/aws-ecs-vs-eks/), [Which AWS compute](https://www.factualminds.com/decide/which-aws-compute/).

---

## Async work — how do you orchestrate background processing?

```
                    What's the work shape?
                            │
        ┌───────────────────┼─────────────────────┐
        │                   │                     │
   Single job, retry    Multi-step               Many parallel
   on failure           workflow with state      tasks, fan-out
        │                   │                     │
        ▼                   ▼                     ▼
    SQS + Lambda      Step Functions        SNS → SQS fan-out
    (or ECS worker)   (Standard for         or EventBridge →
                       long, Express        multiple targets
                       for high-volume)
        │                   │                     │
        ▼                   ▼                     ▼
   DLQ for poison     Built-in retry,        Per-subscriber DLQ
   messages           catch, parallel
                      branches, .map
```

| Pattern | Pick | Notes |
|---------|------|-------|
| Single async task with retry | **SQS + Lambda/ECS** | Cheapest, simplest; DLQ catches poison |
| Multi-step workflow, branching, parallel | **Step Functions Standard** | Up to 1y duration, $0.025 per 1k transitions |
| High-volume event-driven workflow | **Step Functions Express** | Sub-second, $1 per 1M, at-least-once |
| Long-running human-in-the-loop | **Step Functions Standard with .waitForTaskToken** | Pause until callback |
| Cross-service event routing | **EventBridge** | Pattern matching, schema registry, archive |
| Stream processing | **Kinesis or Managed Flink** | See Event processing tree above |
| Cron / scheduled | **EventBridge Scheduler** | Replaces CloudWatch Events scheduled rules |

For X-vs-Y depth: [Step Functions vs EventBridge](https://www.factualminds.com/compare/aws-step-functions-vs-eventbridge/).

---

## File processing — how do you transform data files?

```
                    What's the file size + cadence?
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
   Small files,         Many files,         Large files
   per-file (<10s)      batched job          (GB-TB) or
        │               (5min-24h)           complex transform
        ▼                   │                   │
   S3 Event              ▼                   ▼
   Notification         AWS Batch            EMR (Spark)
   → Lambda             (queue + scaled                or
                         compute env)        Glue (Spark/
                                              Python ETL)
```

| Workload | Pick | Why |
|----------|------|-----|
| Per-file transforms <15min, low complexity | **S3 → Lambda** | Event-driven, no infra to run |
| Per-file transforms >15min or high CPU | **S3 → SQS → ECS/Batch** | Lambda 15min hard limit |
| Scheduled or batch ETL | **AWS Glue** | Managed Spark; Glue Studio for low-code |
| Large-scale Spark / Hadoop | **EMR** or **EMR Serverless** | Full Spark ecosystem; serverless for sub-hourly |
| Streaming ETL to S3 | **Kinesis Firehose** with Lambda transform | Buffered delivery, no compute to manage |
| Image / video processing | **MediaConvert** (video) or **Lambda + Rekognition** (image) | Specialised services beat hand-rolled |
| Document parsing / OCR | **Textract** + Lambda orchestration | Output → DynamoDB or S3 |
| Vector embedding generation | **Bedrock + Lambda or Step Functions** | Bedrock embedding models invoked from your pipeline |

---

## Authentication / authorisation — how do users sign in?

```
                    Who's signing in?
                            │
        ┌───────────────────┼─────────────────────┐
        │                   │                     │
   Your end-users       Internal employees    Service-to-service
   (B2C, B2B SaaS)      (workforce SSO)       (no humans)
        │                   │                     │
        ▼                   ▼                     ▼
   Cognito User        IAM Identity Center   IAM Roles +
   Pools (or 3rd       (SSO across AWS       STS AssumeRole
   party: Auth0,       accounts and SaaS     (or signed
   WorkOS, Clerk)      apps via SAML/OIDC)   requests via SigV4)
```

| Use case | Pick | Notes |
|----------|------|-------|
| Customer auth (sign-up, sign-in, MFA, social login) | **Cognito User Pools** or **Auth0/Clerk/WorkOS** | Cognito for cost; 3rd party for DX |
| Workforce SSO across AWS and SaaS | **IAM Identity Center** | Replaces AWS SSO |
| Service-to-service inside AWS | **IAM Roles** | No tokens to rotate |
| Cross-account access | **STS AssumeRole** | Temporary credentials, audited via CloudTrail |
| Federated B2B (customer's IdP) | **Cognito Identity Pools** or **WorkOS** | WorkOS for out-of-the-box SCIM + SAML directory sync |
| Per-tenant auth in SaaS | See [`multi-tenant-saas.md`](multi-tenant-saas.md) | Single Cognito pool with custom attributes vs pool-per-tenant |

For X-vs-Y depth: [IAM Identity Center vs Cognito](https://www.factualminds.com/compare/aws-iam-identity-center-vs-cognito/).

---

## Caching — where does the cache live?

| Pattern | Pick | Notes |
|---------|------|-------|
| Database read cache | **ElastiCache Redis / Valkey** | Persist sessions, leaderboards, rate-limit counters |
| DynamoDB read cache | **DAX** | Transparent in-front-of-DDB; eventual consistency aware |
| HTTP / static asset cache | **CloudFront** | Origin can be S3, ALB, custom |
| API response cache | **API Gateway caching** or **CloudFront in front of API** | API GW cache is per-stage, hourly billing |
| Edge compute cache | **Lambda@Edge** + CloudFront cache key manipulation | Personalisation at edge |
| In-process cache | App-level (in Lambda warm container, ECS process) | Cheapest; lost on restart/scale |

---

## CI/CD — how do you ship?

```
              Where does code live?
                       │
        ┌──────────────┼──────────────┐
        │              │              │
   GitHub          GitLab         CodeCommit [shutdown for new]
        │              │              │
        ▼              ▼              ▼
   GitHub          GitLab CI       (migrate to GitHub
   Actions or                       or GitLab)
   CodePipeline
```

| Need | Pick | Notes |
|------|------|-------|
| Most teams in 2024+ | **GitHub Actions** | OIDC to AWS replaces long-lived keys |
| Heavy AWS-native, multi-account orchestration | **CodePipeline** + GitHub source | Cross-account deploys via CodeDeploy |
| Container build pipeline | **CodeBuild** or GitHub Actions runners | Cache layers via ECR |
| IaC | **Terraform** or **CDK** or **Pulumi** | All viable; pick on team taste + ecosystem |

For X-vs-Y depth: [CodePipeline vs GitHub Actions](https://www.factualminds.com/compare/aws-codepipeline-vs-github-actions/), [Terraform vs CDK](https://www.factualminds.com/blog/terraform-vs-aws-cdk-infrastructure-as-code-decision-guide/).

---

## When trees lie

These are heuristics. Real decisions involve cost ceilings, team skills, existing investments, regulatory constraints, and the political reality of "we already standardised on X." The trees here are starting points — diverge consciously, document why.

A common failure mode is picking a service from a tree without modelling the access pattern (DynamoDB), warming plan (SES dedicated IPs), or operational story (EKS without K8s ops). Tree → table → playbook: read all three before committing.

---

*See also: [`failure-first.md`](failure-first.md) · [`anti-patterns.md`](anti-patterns.md) · [`cost-pitfalls.md`](cost-pitfalls.md) · [Decision Guides X-vs-Y in root README](../README.md#decision-guides--x-vs-y).*
