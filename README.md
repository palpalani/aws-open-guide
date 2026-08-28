<div align="center">

# ☁️ AWS Open Guide

### A curated, opinionated map of Amazon Web Services

**Official links, production guides, OSS tools, and X-vs-Y comparisons — grouped the way AWS names services so you land on the right resource, not a random category.**

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg?style=flat-square)](https://creativecommons.org/licenses/by/4.0/)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat-square)](CONTRIBUTING.md)
[![GitHub stars](https://img.shields.io/github/stars/palpalani/aws-open-guide?style=flat-square&logo=github)](https://github.com/palpalani/aws-open-guide)
[![GitHub last commit](https://img.shields.io/github/last-commit/palpalani/aws-open-guide?style=flat-square&logo=github)](https://github.com/palpalani/aws-open-guide/commits)
[![GitHub issues](https://img.shields.io/github/issues/palpalani/aws-open-guide?style=flat-square&logo=github)](https://github.com/palpalani/aws-open-guide/issues)
[![Link Check](https://github.com/palpalani/aws-open-guide/actions/workflows/link-check.yml/badge.svg?style=flat-square)](https://github.com/palpalani/aws-open-guide/actions/workflows/link-check.yml)

[**🚀 Get Started**](#how-to-use-this-guide) ·
[**🎯 Use-Case Playbooks**](#use-case-playbooks) ·
[**🧭 Browse Services**](#table-of-contents) ·
[**⚖️ Decision Guides**](#decision-guides--x-vs-y) ·
[**💰 Cost & FinOps**](#cost-management--finops) ·
[**🤖 AI & MCP**](#ai-coding-agents-mcp--skills) ·
[**🤝 Contribute**](CONTRIBUTING.md) ·
[**✅ Production readiness**](PRODUCTION_READINESS.md)

</div>

---

## Why this guide?

AWS lists **200+ services** in the console. The docs are accurate but spread across hundreds of sites, so you lose time tab-hopping and second-guessing which service fits. This guide is a single index with two layers: browse by **service** when you know the name, or by **workload** when you know the problem.

| | |
|---|---|
| 🗂️ **Same taxonomy as AWS** | Compute, Storage, Databases, Networking — the way the console and docs are organized, not a third-party topic list. |
| 📚 **Three tiers per topic** | Official sources first, then deep production write-ups, then OSS tools you can run today. |
| ⚠️ **Costs and gotchas called out** | Limits, bill surprises, and migration friction you rarely see in a product page. |
| ⚖️ **Comparisons when it matters** | Common "should I use X or Y?" questions point to a decision guide, not guesswork. |
| ⏳ **Lifecycle you can trust** | Maintenance, sunset, and shutdown flags so you do not design on services AWS is winding down. |
| 🤖 **Built for how teams work now** | MCP servers, agent plugins, and skills for AI-assisted AWS work sit alongside the traditional links. |

> [!TIP]
> If a category here is empty or thin, [contributions are warmly welcomed](CONTRIBUTING.md). One link per line, em-dash separator — see [CONTRIBUTING.md](CONTRIBUTING.md) for the full format.

## How to use this guide

Match the row to what you need **today** — each path sends you to a different slice of this repo (building, evaluating, debugging, or learning).

### 🧭 Pick your entry point

| You are... | Start here |
|---|---|
| 🏗️ **Building a workload** (email at scale, multi-tenant SaaS, …) | [Use-Case Playbooks](#use-case-playbooks) — problem, architecture, failure modes, cost, anti-patterns |
| 🌱 **New to AWS** | [Foundations](#foundations) → Architecture Deep Reading → pick a service section |
| 🎯 **Picking a service** | [Decision Guides — X vs Y](#decision-guides--x-vs-y) — every common "should I use X or Y" question |
| 💸 **Hunting a surprise bill** | [Cost Management & FinOps](#cost-management--finops) → Bill Teardowns · [Cost pitfalls playbook](use-cases/cost-pitfalls.md) |
| 🤖 **Building with AI** | [AI/ML services](#artificial-intelligence--machine-learning) for services · [AI Coding Agents, MCP & Skills](#ai-coding-agents-mcp--skills) for AI-assisted dev |
| 📰 **Staying current** | [Community, Social & Continuous Learning](#community-social--continuous-learning) → Minimal curated stack |
| 🛠️ **Migrating from another platform** | [Migration Guides — From Other Platforms](#migration-guides--from-other-platforms) |

### 📐 Convention used in every service section

| Tier | What you'll find | When to read |
|---|---|---|
| **Official** | AWS's own docs, pricing, announcements | Authoritative facts |
| **Production Guides** | Third-party deep-dives | When official docs leave you with "yes but how at scale?" |
| **OSS Tools** / **Tools** | Open-source utilities | Day-to-day workflow upgrades |
| **⚠️ Gotchas** | Limits, bill traps, surprise behaviour | Before you ship to production |
| **Decision Guides** | "X vs Y" comparisons | When picking between similar services |

> [!NOTE]
> **Quick decisions:** if you already know the workload and just need to pick the AWS service, skip to [Decision Guides — X vs Y](#decision-guides--x-vs-y).

## Use-Case Playbooks

> How to build common workloads on AWS in production — problem, architecture, failure modes, cost, anti-patterns. Not a links list; a playbook.

**You have a feature to ship** (email at scale, uploads, async jobs, RAG, and the rest). Open a playbook first when you need a production-shaped answer, not a tour of one service. The service taxonomy below is the **reference layer** ("what exists about S3"). Playbooks are the **building layer** ("how do I run X safely in prod"). Each one follows the same 11-section template — see [`use-cases/_template.md`](use-cases/_template.md).

**Workload playbooks:**

- 🏗️ [Email delivery](use-cases/email-delivery.md) — transactional email at scale on SES with bounce/complaint handling and deliverability tracking
- 🏗️ [Multi-tenant SaaS](use-cases/multi-tenant-saas.md) — silo / pool / bridge isolation with per-tenant cost attribution
- 🏗️ [Async job processing](use-cases/async-jobs.md) — API → queue → worker → result store with idempotency, DLQ, and webhooks
- 🏗️ [Event-driven processing](use-cases/event-driven.md) — EventBridge with schemas, replay, and per-target DLQs
- 🏗️ [File upload and processing](use-cases/file-upload.md) — pre-signed S3 uploads with malware scan and async transform
- 🏗️ [High-scale API backend](use-cases/high-scale-api.md) — CloudFront + WAF + API Gateway + cache with rate limits and graceful degradation
- 🏗️ [Real-time analytics pipeline](use-cases/real-time-analytics.md) — Kinesis hot path + Firehose cold path → S3 + Athena
- 🏗️ [Observability pipeline](use-cases/observability-pipeline.md) — hot CloudWatch + cold S3-Athena with EMF metrics and trace sampling
- 🏗️ [GenAI / RAG application](use-cases/genai-rag.md) — Bedrock + vector store + retrieval + Guardrails with evals
- 🏗️ [CI/CD for AWS workloads](use-cases/ci-cd.md) — GitHub Actions + OIDC + per-environment accounts with canary and rollback
- 🏗️ [FinOps governance](use-cases/finops-governance.md) — tagging, CUR, allocation, commitments, and quarterly optimization cadence
- 🏗️ [AWS security baseline](use-cases/security-baseline.md) — Prowler, Security Hub, Config, Checkov, and remediation workflow

**Cross-cutting frameworks** (referenced by every playbook):

- 🌳 [Decision trees](use-cases/decision-trees.md) — which AWS service for event processing, database, compute, async work, file processing
- 🛡️ [Failure-first patterns](use-cases/failure-first.md) — retries, idempotency, DLQs, regional failover, backpressure, circuit breakers
- 🚫 [Anti-patterns](use-cases/anti-patterns.md) — the mistakes that show up across every workload, with the better pattern
- 💸 [Cost pitfalls](use-cases/cost-pitfalls.md) — line items that surprise teams (NAT Gateway, cross-AZ, CloudWatch Logs, egress)

> [!TIP]
> All playbooks live under [`use-cases/`](use-cases/). To propose a new one, copy [`_template.md`](use-cases/_template.md), fill every section, then follow [Adding a use-case playbook](CONTRIBUTING.md#adding-a-use-case-playbook) before you open a PR (the link checker will run on your URLs).

<details>
<summary><strong>📑 Table of Contents</strong> — click to expand</summary>

- [📖 How to use this guide](#how-to-use-this-guide)

### 🎯 Use-Case Playbooks

- [Use-Case Playbooks (overview)](#use-case-playbooks)
- [Email delivery](use-cases/email-delivery.md)
- [Multi-tenant SaaS](use-cases/multi-tenant-saas.md)
- [Async job processing](use-cases/async-jobs.md)
- [Event-driven processing](use-cases/event-driven.md)
- [File upload and processing](use-cases/file-upload.md)
- [High-scale API backend](use-cases/high-scale-api.md)
- [Real-time analytics pipeline](use-cases/real-time-analytics.md)
- [Observability pipeline](use-cases/observability-pipeline.md)
- [GenAI / RAG application](use-cases/genai-rag.md)
- [CI/CD for AWS workloads](use-cases/ci-cd.md)
- [FinOps governance](use-cases/finops-governance.md)
- [AWS security baseline](use-cases/security-baseline.md)
- [Decision trees](use-cases/decision-trees.md)
- [Failure-first patterns](use-cases/failure-first.md)
- [Anti-patterns](use-cases/anti-patterns.md)
- [Cost pitfalls](use-cases/cost-pitfalls.md)

### 🟧 Core AWS services

- [🏛️ Foundations](#foundations)
- [💻 Compute](#compute)
- [📦 Containers](#containers)
- [⚡ Serverless](#serverless)
- [💾 Storage](#storage)
- [🗄️ Databases](#databases)
- [🌐 Networking & Content Delivery](#networking--content-delivery)
- [🔐 Security & Identity](#security--identity)
- [📋 Compliance](#compliance)
- [📊 Analytics & Big Data](#analytics--big-data)
- [🤖 Artificial Intelligence & Machine Learning](#artificial-intelligence--machine-learning)
- [🛠️ Developer Tools, DevOps & CI/CD](#developer-tools-devops--cicd)
- [🔭 Observability & Monitoring](#observability--monitoring)
- [💰 Cost Management & FinOps](#cost-management--finops)
  - [Analysis & visibility](#analysis--visibility)
  - [FinOps platforms (third-party)](#finops-platforms-third-party)
  - [Rightsizing](#rightsizing)
  - [Commitment discounts](#commitment-discounts-savings-plans--reserved-instances)
  - [Cost allocation & tagging](#cost-allocation--tagging)
  - [Bill teardowns](#bill-teardowns-real-customer-incidents)
  - [Cost pitfalls playbook](use-cases/cost-pitfalls.md)
  - [FinOps governance playbook](use-cases/finops-governance.md)
- [🚚 Migration & Transfer](#migration--transfer)
- [📡 Internet of Things (IoT)](#internet-of-things-iot)
- [🔄 Application Integration](#application-integration)
- [✉️ Email & Communication](#email--communication)
- [🏢 Management & Governance](#management--governance)

### 🟦 Frameworks & guidance

- [🏗️ Well-Architected Framework](#well-architected-framework)
- [🏭 Industry Architectures](#industry-architectures)
- [⚖️ Decision Guides — X vs Y](#decision-guides--x-vs-y)
- [🔁 Migration Guides — From Other Platforms](#migration-guides--from-other-platforms)
- [⏳ AWS Service Lifecycle & Deprecations](#aws-service-lifecycle--deprecations)
- [🧮 Free Tools & Calculators](#free-tools--calculators)
- [📓 AWS Glossary](#aws-glossary)
- [🎓 AWS Certifications & Learning Paths](#aws-certifications--learning-paths)
- [🧩 Architecture Patterns](#architecture-patterns)

### 🟪 Community, AI tooling & resources

- [🧠 AI Coding Agents, MCP & Skills](#ai-coding-agents-mcp--skills)
- [📰 Engineering Blogs & Case Studies](#engineering-blogs--case-studies)
- [🌐 Community, Social & Continuous Learning](#community-social--continuous-learning)
- [🔌 Third-Party Integrations](#third-party-integrations)
- [📚 Books, Courses & Newsletters](#books-courses--newsletters)
- [🎤 Conferences & Events](#conferences--events)
- [🔖 Other Awesome AWS Lists](#other-awesome-aws-lists)
- [🤝 Contributing](#contributing)
- [✅ Production readiness plan](PRODUCTION_READINESS.md)
- [📄 License](#license)

</details>

---

## Foundations

Start here if you're new to AWS or evaluating whether to build on it.

**Official:**
- [AWS Documentation Home](https://docs.aws.amazon.com/)
- [AWS Architecture Center](https://aws.amazon.com/architecture/)
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)
- [AWS Service Health Dashboard](https://health.aws.amazon.com/health/status)
- [AWS Pricing Calculator](https://calculator.aws/)
- [AWS Free Tier](https://aws.amazon.com/free/)

**Foundational Guides:**
- [AWS Cloud Adoption Framework (CAF)](https://aws.amazon.com/cloud-adoption-framework/) — official six-perspective enterprise migration framework
- [AWS Well-Architected Framework — six pillars (FactualMinds)](https://www.factualminds.com/blog/aws-well-architected-framework-6-pillars-explained/?utm_source=aws-open-guide&utm_medium=readme&utm_campaign=foundations) — pillar walkthrough with production context

**Architecture Deep Reading (essential AWS canon):**
- [AWS Architecture Blog](https://aws.amazon.com/blogs/architecture/) — reference architectures and AWS engineering posts
- [AWS Builders Library](https://aws.amazon.com/builders-library/) — operations + resilience essays from AWS principal engineers
- [Static Stability Using Availability Zones](https://aws.amazon.com/builders-library/static-stability-using-availability-zones/) — Builders Library essay on designing for failure
- [Workload isolation using shuffle-sharding (Builders Library)](https://aws.amazon.com/builders-library/workload-isolation-using-shuffle-sharding/) — fault isolation beyond naive sharding
- [Automating safe hands-off deployments (Builders Library)](https://aws.amazon.com/builders-library/automating-safe-hands-off-deployments/) — cells, waves, and limiting deployment blast radius
- [Avoiding fallback in distributed systems (Builders Library)](https://aws.amazon.com/builders-library/avoiding-fallback-in-distributed-systems/) — why distributed fallback often widens outages
- [Making retries safe with idempotent APIs (Builders Library)](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-apis/) — idempotency for safe retries under UNKNOWN outcomes
- [Using load shedding to avoid overload (Builders Library)](https://aws.amazon.com/builders-library/using-load-shedding-to-avoid-overload/) — overload feedback loops and shedding layers
- [Leader election in distributed systems (Builders Library)](https://aws.amazon.com/builders-library/leader-election-in-distributed-systems/) — leases, partitions, and consistency trade-offs
- [Using dependency isolation / circuit breakers (Builders Library)](https://aws.amazon.com/builders-library/dependency-isolation/) — bulkheads and concurrency overload containment
- [Implementing health checks (Builders Library)](https://aws.amazon.com/builders-library/implementing-health-checks/) — health checks and correlated fleet automation risks
- [Instrumenting distributed systems for operational visibility (Builders Library)](https://aws.amazon.com/builders-library/instrumenting-distributed-systems-for-operational-visibility/) — structured logs, metrics, trace propagation
- [Challenges with distributed systems (Builders Library)](https://aws.amazon.com/builders-library/challenges-with-distributed-systems/) — independent failures, nondeterminism, and testing permutations
- [Multi-Tier Architectures on AWS (whitepaper)](https://docs.aws.amazon.com/whitepapers/latest/overview-deployment-options/)
- [AWS Multi-Region Fundamentals (whitepaper)](https://docs.aws.amazon.com/prescriptive-guidance/latest/aws-multi-region-fundamentals/) — active-active patterns

---

## Compute

Virtual servers, containers' substrate, and specialized chips.

### Amazon EC2 — Elastic Compute Cloud

> Virtual servers in the cloud. The original AWS service and still the workhorse.

**Official:**
- [EC2 Documentation](https://docs.aws.amazon.com/ec2/)
- [EC2 Instance Types](https://aws.amazon.com/ec2/instance-types/)
- [EC2 Pricing](https://aws.amazon.com/ec2/pricing/)
- [Spot Instance Advisor](https://aws.amazon.com/ec2/spot/instance-advisor/)
- [AWS Compute Blog](https://aws.amazon.com/blogs/compute/) — EC2, Lambda, Batch, and Step Functions posts

**OSS Tools:**
- [99designs/aws-vault](https://github.com/99designs/aws-vault) — secure storage of AWS credentials on developer laptops
- [AutoSpotting/AutoSpotting](https://github.com/LeanerCloud/AutoSpotting) — automatically replace on-demand EC2 in ASGs with spot instances

### AWS Graviton — Arm-based processors

> Custom Arm chips with up to 40% better price/performance than x86. Graviton5 (M9g/M9gd) GA June 2026 for agentic AI and general-purpose workloads.

**Official:**
- [Graviton overview](https://aws.amazon.com/ec2/graviton/)
- [EC2 M9g instances](https://aws.amazon.com/ec2/instance-types/m9g/) — Graviton5 general-purpose instance specs and sizes
- [EC2 M9g and M9gd instances — Graviton5 GA](https://aws.amazon.com/about-aws/whats-new/2026/06/ec2-m9g-m9gd-instances-graviton5-processors-available/) — fifth-gen Graviton processors, GA June 2026
- [M9g/M9gd GA — AWS News Blog](https://aws.amazon.com/blogs/aws/now-available-amazon-ec2-m9g-and-m9gd-instances-powered-by-new-aws-graviton5-processors/) — Graviton5 launch details and customer results
- [Graviton5 chiplet architecture — Amazon Science](https://www.amazon.science/blog/graviton5s-improved-design-increases-speed-and-energy-efficiency-beyond-moores-law) — DDR5-8800, PCIe Gen6, Nitro Isolation Engine
- [M9g preview announcement](https://aws.amazon.com/about-aws/whats-new/2025/12/ec2-m9g-instances-graviton5-processors-preview/) — Dec 2025 preview; superseded by GA


### AWS Trainium & Inferentia — ML accelerators

> Purpose-built chips for training (Trainium) and inference (Inferentia). For agentic AI orchestration on general-purpose compute, see [AWS Graviton](#aws-graviton--arm-based-processors).

- [Trainium](https://aws.amazon.com/ai/machine-learning/trainium/) · [Inferentia](https://aws.amazon.com/ai/machine-learning/inferentia/)
- [EC2 Trn3 UltraServers — Trainium3](https://aws.amazon.com/ec2/instance-types/trn3/) — fourth-gen Trainium chips for frontier-scale training

### AWS Batch

- [Batch documentation](https://docs.aws.amazon.com/batch/)

### AWS Lightsail

> Simple VPS pricing for predictable workloads.
- [Lightsail](https://aws.amazon.com/lightsail/)

### AWS App Runner

> Fully managed container service for web apps and APIs.
- [App Runner](https://aws.amazon.com/apprunner/)

### Amazon Elastic VMware Service (EVS)


### AWS Outposts

> AWS-managed hardware in your own data centre. Use for low-latency, data-residency, or hybrid workloads that must stay on-prem.

- [Outposts](https://aws.amazon.com/outposts/)
- [Outposts FAQs](https://aws.amazon.com/outposts/rack/faqs/)

### AWS ParallelCluster

> Open-source HPC cluster orchestrator on EC2 — Slurm scheduling, EFA networking, FSx for Lustre.

- [ParallelCluster](https://aws.amazon.com/hpc/parallelcluster/)
- [aws/aws-parallelcluster](https://github.com/aws/aws-parallelcluster) — official OSS repo

---

## Containers

Container orchestration and registry.

### Amazon ECS — Elastic Container Service

> AWS-native container orchestration. Lower operational overhead than EKS for most teams.

**Official:**
- [ECS Documentation](https://docs.aws.amazon.com/ecs/)
- [ECS Pricing](https://aws.amazon.com/ecs/pricing/)
- [AWS Containers Blog](https://aws.amazon.com/blogs/containers/) — ECS, EKS, Fargate, and ECR architecture posts


See also: [Spot & interruptible compute — ECS capacity providers](#spot--interruptible-compute) · [Container cost optimization](#container-cost-optimization)

### Amazon EKS — Elastic Kubernetes Service

> Managed Kubernetes. Use when you need K8s portability or have existing K8s expertise.

> 🎯 **Building multi-tenant SaaS on EKS?** See the [Multi-tenant SaaS playbook](use-cases/multi-tenant-saas.md) — silo / pool / bridge isolation models with per-tenant cost attribution and noisy-neighbour controls.

**Official:**
- [EKS Documentation](https://docs.aws.amazon.com/eks/)
- [EKS Best Practices Guides](https://docs.aws.amazon.com/eks/latest/best-practices/introduction.html)

**Tools:**
- [Karpenter](https://karpenter.sh/) — node autoscaling for EKS
- [eksctl](https://docs.aws.amazon.com/eks/latest/eksctl/what-is-eksctl.html) — official CLI for EKS
- [terraform-aws-modules/terraform-aws-eks](https://github.com/terraform-aws-modules/terraform-aws-eks) — community Terraform module for EKS clusters and node groups
- [aws-ia/terraform-aws-eks-blueprints](https://github.com/aws-ia/terraform-aws-eks-blueprints) — Terraform patterns and add-ons for production-style EKS stacks

**Kubernetes cost & ops (vendor blogs):**
- [Cast AI Blog](https://cast.ai/blog/) — Kubernetes cost optimization and autoscaler guidance for cloud workloads

### AWS Fargate

> Serverless compute for containers. Pay per task, not per VM.
- [Fargate](https://aws.amazon.com/fargate/)

See also: [Fargate Spot — capacity providers](#spot--interruptible-compute) · [Container cost optimization](#container-cost-optimization)

### Amazon ECR — Elastic Container Registry

> Private Docker/OCI registry, integrated with IAM and image scanning.
- [ECR Documentation](https://docs.aws.amazon.com/ecr/)

### Finch — open-source container client

> AWS-built local Docker alternative — `nerdctl` + `containerd` + `Lima` packaged for macOS/Linux/Windows. Drop-in replacement for `docker build/run/push`.

- [Finch](https://runfinch.com/)
- [runfinch/finch](https://github.com/runfinch/finch) — open-source repo

### Decision


---

## Serverless

Run code without managing servers.

### AWS Lambda

> Event-driven function-as-a-service. The default for sporadic, async, glue-code workloads.

> 🎯 **Building with Lambda in production?** See [Async job processing](use-cases/async-jobs.md) (queue + worker), [High-scale API backend](use-cases/high-scale-api.md) (caching + rate limits), and [Event-driven processing](use-cases/event-driven.md) (EventBridge + DLQs).

**Official:**
- [Lambda Documentation](https://docs.aws.amazon.com/lambda/)
- [Lambda Pricing](https://aws.amazon.com/lambda/pricing/)
- [Lambda Powertools (Python/TypeScript/Java)](https://docs.aws.amazon.com/powertools/python/latest/)
- [Lambda invocation, scaling and concurrency (official docs)](https://docs.aws.amazon.com/lambda/latest/dg/lambda-concurrency.html)
- [AWS Lambda blog category (Compute Blog)](https://aws.amazon.com/blogs/compute/category/aws-lambda/) — patterns, deep dives, releases

**Production Guides:**
- [Going Serverless at Scale — Adrian Cockcroft (re:Invent talk)](https://www.youtube.com/watch?v=EBSdyoO3goc)

See also: [Cost Management — rightsizing](#rightsizing) · [Cost pitfalls — Lambda memory](use-cases/cost-pitfalls.md#lambda-over-provisioned-memory)

**Comparisons:**

### AWS Step Functions

> Visual workflow orchestrator for distributed apps.

**Official:**
- [Step Functions Documentation](https://docs.aws.amazon.com/step-functions/)
- [AWS Step Functions blog category (Compute Blog)](https://aws.amazon.com/blogs/compute/category/aws-step-functions/) — workflow patterns and launches

**Comparisons:**

### Amazon EventBridge

> Serverless event bus for SaaS, AWS services, and custom events.
- [EventBridge Documentation](https://docs.aws.amazon.com/eventbridge/)
- [AWS Event-Driven Architecture (overview)](https://aws.amazon.com/event-driven-architecture/) — official intro, services, patterns, and reference architectures

### AWS SAM & Serverless Framework

- [AWS SAM (Serverless Application Model)](https://aws.amazon.com/serverless/sam/)
- [Serverless Framework](https://www.serverless.com/)

### OSS Lambda Frameworks (community)

- [aws/chalice](https://github.com/aws/chalice) — Python serverless microframework (official AWS, Flask-style)
- [zappa/Zappa](https://github.com/zappa/Zappa) — serverless WSGI Python on Lambda + API Gateway (Django, Flask)
- [claudiajs/claudia](https://github.com/claudiajs/claudia) — deploy Node.js projects to Lambda + API Gateway with one command
- [jeremydaly/lambda-api](https://github.com/jeremydaly/lambda-api) — lightweight web framework for serverless Node.js
- [awslabs/aws-lambda-web-adapter](https://github.com/aws/aws-lambda-web-adapter) — run any HTTP web app (Express, Flask, FastAPI, Next.js) on Lambda unmodified
- [getmoto/moto](https://github.com/getmoto/moto) — mock AWS services for unit/integration tests (also useful beyond Lambda)

### Local Lambda Dev

- [AWS SAM CLI — `sam local`](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/) — invoke Lambda + API Gateway locally
- [aws/aws-lambda-runtime-interface-emulator](https://github.com/aws/aws-lambda-runtime-interface-emulator) — `aws-lambda-rie` — run Lambda container images locally with `docker run`

**Other Serverless Patterns:**

---

## Storage

### Amazon S3 — Simple Storage Service

> Object storage. 11 9's durability. The default landing pad for files in AWS.

> 🎯 **Handling user file uploads?** See the [File upload and processing playbook](use-cases/file-upload.md) — pre-signed URLs, malware scan, MIME sniffing, async transform pipeline, lifecycle policies.

**Official:**
- [S3 Documentation](https://docs.aws.amazon.com/s3/)
- [S3 Pricing](https://aws.amazon.com/s3/pricing/)
- [S3 Storage Classes](https://aws.amazon.com/s3/storage-classes/)

**Tools:**
- [s3cmd](https://github.com/s3tools/s3cmd) — full-featured CLI
- [Mountpoint for Amazon S3](https://github.com/awslabs/mountpoint-s3) — official FUSE mount
- [s5cmd](https://github.com/peak/s5cmd) — fastest S3 CLI
- [s3fs-fuse](https://github.com/s3fs-fuse/s3fs-fuse) — community FUSE-based S3 mount (Linux + macOS)
- [goofys](https://github.com/kahing/goofys) — S3 file system in Go, optimized for read throughput
- [MinIO](https://github.com/minio/minio) — self-hosted S3-compatible object storage (good for hybrid + dev/test)
- [MinIO `mc` client](https://github.com/minio/mc) — S3-compatible CLI (works with S3 + MinIO)
- [s3-server](https://github.com/opsfour/s3-server) — S3-compatible object storage server as a PHP 8.4+ Composer package
- [rclone](https://github.com/rclone/rclone) — rsync for S3 + 70+ other cloud storage backends

> [!WARNING]
> **Gotchas:**
> - Bucket names are globally unique across all AWS accounts.
> - Default encryption (SSE-S3) is now ON for all new buckets — was opt-in pre-2023.
> - Cross-region replication does NOT replicate delete markers by default.

### Amazon S3 Vectors

> Native vector storage in S3 — purpose-built for RAG and AI workloads.

### Amazon EBS — Elastic Block Store

- [EBS Documentation](https://docs.aws.amazon.com/ebs/)

### Amazon EFS — Elastic File System

- [EFS Documentation](https://docs.aws.amazon.com/efs/)

### Amazon FSx

- [FSx](https://aws.amazon.com/fsx/) — managed Windows, Lustre, NetApp ONTAP, OpenZFS

### AWS Backup

> Centralized backup service across AWS resources.
- [AWS Backup](https://aws.amazon.com/backup/)

### AWS Storage Gateway

- [Storage Gateway](https://aws.amazon.com/storagegateway/)

---

## Databases

> Pick by consistency model (ACID vs eventual), scale shape (single-region vs petabyte), and query pattern (relational, key-value, document, graph, time-series). When in doubt, [Decision Guides — X vs Y](#decision-guides--x-vs-y) maps the common choices.

### Amazon RDS — Relational Database Service

> Managed Postgres, MySQL, MariaDB, Oracle, SQL Server.

**Official:**
- [RDS Documentation](https://docs.aws.amazon.com/rds/)
- [RDS Pricing](https://aws.amazon.com/rds/pricing/)
- [AWS Database Blog](https://aws.amazon.com/blogs/database/) — RDS, Aurora, DynamoDB, and purpose-built DB posts

**Production Guides:**
- [Citus Data Blog](https://www.citusdata.com/blog) — Postgres horizontal scaling patterns relevant to RDS PostgreSQL fleets

### Amazon Aurora

> AWS-built relational DB. Postgres/MySQL-compatible, 5x performance of stock MySQL.

- [Aurora Documentation](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/CHAP_AuroraOverview.html)

### Amazon DynamoDB

> Single-digit millisecond NoSQL key-value + document store.

- [DynamoDB Documentation](https://docs.aws.amazon.com/dynamodb/)
- [DynamoDB best practices (official)](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/best-practices.html) — partition keys, indexes, scaling
- [DynamoDB single-table design — Alex DeBrie](https://www.alexdebrie.com/posts/dynamodb-single-table/) — canonical reading
- [Advanced design patterns for DynamoDB — Rick Houlihan (re:Invent talk)](https://www.youtube.com/watch?v=HaEPXoXVf2k)

**OSS Tools:**
- [sensedeep/dynamodb-onetable](https://github.com/sensedeep/dynamodb-onetable) — Node.js library for single-table designs
- [jeremydaly/dynamodb-toolbox](https://github.com/dynamodb-toolbox/dynamodb-toolbox) — Jeremy Daly's TypeScript library for single-table modeling

### Amazon Redshift

> Petabyte-scale data warehouse.

- [Redshift Documentation](https://docs.aws.amazon.com/redshift/)

### Amazon ElastiCache

> Managed Redis & Memcached.
- [ElastiCache Documentation](https://docs.aws.amazon.com/elasticache/)

### Amazon MemoryDB for Redis

- [MemoryDB](https://aws.amazon.com/memorydb/)

### Amazon DocumentDB

- [DocumentDB](https://aws.amazon.com/documentdb/) — MongoDB-compatible

### Amazon Neptune

- [Neptune](https://aws.amazon.com/neptune/) — graph database

### Amazon Timestream

- [Timestream](https://aws.amazon.com/timestream/) — time-series; LiveAnalytics closed to new customers June 20, 2025

### Decision Guides


---

## Networking & Content Delivery

> Design for blast radius (multi-AZ), latency (regional vs edge), and the bill (NAT Gateway egress and cross-AZ traffic are the usual surprises).

### Amazon VPC — Virtual Private Cloud

**Official:**
- [VPC Documentation](https://docs.aws.amazon.com/vpc/)
- [Networking & Content Delivery Blog](https://aws.amazon.com/blogs/networking-and-content-delivery/) — VPC, CDN, and hybrid connectivity posts


### NAT Gateway


See also: [Cost pitfalls — NAT Gateway](use-cases/cost-pitfalls.md#nat-gateway) · [Network cost optimization](#network-cost-optimization)

### Amazon Route 53

- [Route 53](https://aws.amazon.com/route53/) — DNS + traffic management

### Amazon CloudFront

> Global CDN with 600+ edge locations.

**Official:**
- [CloudFront Documentation](https://docs.aws.amazon.com/cloudfront/)


### Amazon API Gateway

> 🎯 **Building a high-traffic API?** See the [High-scale API backend playbook](use-cases/high-scale-api.md) — CloudFront + WAF + API Gateway with caching, rate limits, and graceful degradation under load.

- [API Gateway Documentation](https://docs.aws.amazon.com/apigateway/)

### AWS Verified Access


### AWS Direct Connect / Transit Gateway / Global Accelerator

- [Direct Connect](https://aws.amazon.com/directconnect/) · [Transit Gateway](https://aws.amazon.com/transit-gateway/) · [Global Accelerator](https://aws.amazon.com/global-accelerator/)

---

## Security & Identity

> Layer it: identity (IAM, Cognito), boundaries (SCPs, permission boundaries), encryption (KMS), detection (GuardDuty, Security Hub), and audit trails (CloudTrail, Config). For end-to-end posture and remediation, see the [security baseline playbook](use-cases/security-baseline.md) and [AWS cloud security services](https://www.factualminds.com/services/aws-cloud-security/?utm_source=aws-open-guide&utm_medium=readme&utm_campaign=security-identity).

### AWS IAM — Identity & Access Management

**Official:**
- [IAM Documentation](https://docs.aws.amazon.com/iam/)
- [AWS Security Blog](https://aws.amazon.com/blogs/security/) — IAM, encryption, and detective controls posts


### AWS IAM Identity Center (formerly SSO)


### Amazon Cognito

- [Cognito](https://aws.amazon.com/cognito/) — user identity for apps

### AWS KMS — Key Management Service

- [KMS Documentation](https://docs.aws.amazon.com/kms/)

### Amazon GuardDuty

> Managed threat detection across AWS accounts.
- [GuardDuty](https://aws.amazon.com/guardduty/)

### AWS Security Hub

- [Security Hub](https://aws.amazon.com/security-hub/)

### AWS WAF — Web Application Firewall

- [WAF Documentation](https://docs.aws.amazon.com/waf/)

### Amazon Inspector


### Amazon Macie & Detective


### AWS Network Firewall & Firewall Manager


### AWS Secrets Manager / Parameter Store

- [Secrets Manager](https://aws.amazon.com/secrets-manager/) · [Parameter Store](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html)

### AWS CloudTrail

- [CloudTrail Documentation](https://docs.aws.amazon.com/cloudtrail/)

### Amazon Verified Permissions (Cedar)


### Amazon Security Lake


### AWS Shared Responsibility Model

- [Shared Responsibility Model — glossary entry](#foundations)

### Holistic Security Guides

- [Security baseline playbook](use-cases/security-baseline.md) — Prowler, Security Hub, Config, and IaC gates in production
### Data Perimeter

- [Data perimeters on AWS](https://aws.amazon.com/identity/data-perimeters-on-aws/) — official identity, network, and resource perimeter model
- [Building a data perimeter on AWS — whitepaper](https://docs.aws.amazon.com/whitepapers/latest/building-a-data-perimeter-on-aws/building-a-data-perimeter-on-aws.html) — full implementation guidance
- [aws-samples/data-perimeter-policy-examples](https://github.com/aws-samples/data-perimeter-policy-examples) — official SCP and resource policy templates

**OSS Security Tools:**
- [Prowler](https://github.com/prowler-cloud/prowler) — AWS security audit + CIS benchmarks
- [ScoutSuite](https://github.com/nccgroup/ScoutSuite) — multi-cloud security auditing
- [CloudSploit](https://github.com/aquasecurity/cloudsploit) — AWS account misconfig scanner
- [Pacu](https://github.com/RhinoSecurityLabs/pacu) — AWS exploitation framework (offensive)
- [aws-nuke](https://github.com/rebuy-de/aws-nuke) — wipe an AWS account clean
- [Checkov](https://github.com/bridgecrewio/checkov) — static analysis for Terraform, CloudFormation, CDK, Kubernetes, ARM, Bicep
- [Steampipe](https://steampipe.io/) — query AWS security and compliance with SQL
- [Security baseline playbook](use-cases/security-baseline.md) — Prowler, Security Hub, Config, and IaC gates
- [policy_sentry](https://github.com/salesforce/policy_sentry) — Salesforce IAM least-privilege policy generator
- [algo](https://github.com/trailofbits/algo) — Trail of Bits one-click personal IPSEC VPN on EC2 (and other clouds)

---

## Compliance

> Evidence collection and audit-ready controls — Audit Manager for evidence, Artifact for AWS attestations, Config conformance packs for continuous checks.

### HIPAA

- [HIPAA Eligible AWS Services](https://aws.amazon.com/compliance/hipaa-eligible-services-reference/)

### PCI DSS


### SOC 2


### ISO 27001


### GDPR


### NIS2


### NIST CSF 2.0


### DORA (Digital Operational Resilience Act)


### EU AI Act


---

## Analytics & Big Data

> 🎯 **Building a real-time analytics pipeline?** See the [Real-time analytics playbook](use-cases/real-time-analytics.md) — Kinesis hot path + Firehose cold path → S3 + Athena, with cost model and partitioning patterns.

**Official:**
- [AWS Big Data Blog](https://aws.amazon.com/blogs/big-data/) — data lakes, streaming, OpenSearch, and analytics posts

### Amazon Athena

> Serverless SQL on S3.
- [Athena Documentation](https://docs.aws.amazon.com/athena/)

### AWS Glue

> Serverless ETL + data catalog.
- [Glue Documentation](https://docs.aws.amazon.com/glue/)

### Amazon Kinesis

- [Kinesis Documentation](https://docs.aws.amazon.com/kinesis/)

### Amazon Managed Service for Apache Flink


### Amazon OpenSearch Service

**Official:**
- [OpenSearch Documentation](https://docs.aws.amazon.com/opensearch-service/)
- [Unified observability in OpenSearch Service (Big Data Blog)](https://aws.amazon.com/blogs/big-data/unified-observability-in-amazon-opensearch-service-metrics-traces-and-ai-agent-debugging-in-a-single-interface/) — metrics, traces, and AI agent debugging together


### Amazon EMR


### Amazon QuickSight

> Serverless BI + ML insights + GenAI dashboards.
- [QuickSight Documentation](https://docs.aws.amazon.com/quick/)

### Amazon DataZone


### AWS Clean Rooms


### Data Pipelines & Lakes

- [Building a data lake on S3 + Glue + Athena](#amazon-s3-simple-storage-service)

---

## Artificial Intelligence & Machine Learning

> 🎯 **Building a RAG application?** See the [GenAI / RAG playbook](use-cases/genai-rag.md) — Bedrock + vector store + retrieval + Guardrails, with evaluation harness and per-tenant cost attribution.

### Amazon Bedrock

> Fully managed access to top foundation models (Anthropic, Meta, Amazon Nova, Mistral, Cohere, OpenAI, Stability AI).

**Official:**
- [Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
- [Bedrock Pricing](https://aws.amazon.com/bedrock/pricing/)
- [Bedrock Knowledge Bases](https://aws.amazon.com/bedrock/knowledge-bases/)
- [Bedrock Agents](https://aws.amazon.com/bedrock/agents/)
- [Bedrock Guardrails](https://aws.amazon.com/bedrock/guardrails/)


### Amazon Bedrock AgentCore

> Managed runtime for production AI agents — sessions, memory, tool gateways, identity, and observability. The "everything around the agent" layer that Bedrock Agents alone doesn't give you.

**Official:**
- [Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [AgentCore documentation](https://docs.aws.amazon.com/bedrock-agentcore/)
- [Get started with the AgentCore CLI](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agentcore-get-started-cli.html) — scaffold, deploy, and invoke with `agentcore create`
- [Get started without the AgentCore CLI](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/getting-started-custom.html) — BYO container Runtime contract (`/invocations`, `/ping`)
- [AgentCore pricing](https://aws.amazon.com/bedrock/agentcore/pricing/) — Runtime, Memory, Gateway, and eval line items
- [AgentCore resources hub](https://aws.amazon.com/bedrock/agentcore/resources/) — blogs and videos by Runtime, Gateway, Memory, and more
- [AgentCore FAQs](https://aws.amazon.com/bedrock/agentcore/faqs/) — Runtime vs managed harness, composable capabilities
- [AgentCore service quotas](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/bedrock-agentcore-limits.html) — default limits and adjustable quotas

**Production Guides:**
- [AgentCore production patterns](#amazon-bedrock)
- [Fullstack AgentCore starter template (FAST)](https://aws.amazon.com/blogs/machine-learning/accelerate-agentic-application-development-with-a-full-stack-starter-template-for-amazon-bedrock-agentcore/) — Runtime, Gateway, Memory, Cognito, and React reference app

**OSS Tools:**
- [awslabs/agentcore-samples](https://github.com/awslabs/agentcore-samples) — official sample patterns
- [Amazon Bedrock AgentCore MCP Server](https://awslabs.github.io/mcp/servers/amazon-bedrock-agentcore-mcp-server) — build/deploy/manage agents from a coding agent
- [aws/agent-toolkit-for-aws](https://github.com/aws/agent-toolkit-for-aws) — AgentCore IDE skills (scaffold, gateway, harden, evals) and MCP servers

**Decision Guides:**
- [AgentCore FAQs](https://aws.amazon.com/bedrock/agentcore/faqs/) — Bedrock Agents vs AgentCore Runtime, Gateway, and Memory

### Amazon Nova

> Amazon's foundation model family — text, multimodal (Canvas, Reel), and Nova 2 reasoning models.

**Official:**
- [Amazon Nova models overview](https://aws.amazon.com/nova/models/)
- [What is Amazon Nova 2?](https://docs.aws.amazon.com/nova/latest/nova2-userguide/what-is-nova-2.html) — Nova 2 Lite, Sonic, and embeddings
- [Nova 2 foundation models in Bedrock](https://aws.amazon.com/about-aws/whats-new/2025/12/nova-2-foundation-models-amazon-bedrock/) — Lite GA; Pro in preview
- [Nova 2 Omni](https://aws.amazon.com/about-aws/whats-new/2025/12/amazon-nova-2-omni-preview/) — multimodal reasoning and image generation [preview]


### Amazon SageMaker

> Build, train, deploy ML models at any scale.

**Official:**
- [SageMaker Documentation](https://docs.aws.amazon.com/sagemaker/)
- [AWS Machine Learning Blog](https://aws.amazon.com/blogs/machine-learning/) — training, inference, and MLOps posts


### Amazon Q

> AI assistant family for developers, business users, and analytics.

**Official:**
- [Amazon Q for Business](https://aws.amazon.com/q/business/)


### Kiro IDE


### Other AI/ML Services

- [Amazon Comprehend](https://aws.amazon.com/comprehend/) — NLP
- [Amazon Rekognition](https://aws.amazon.com/rekognition/) — image/video analysis
- [Amazon Textract](https://aws.amazon.com/textract/) — OCR + document AI
- [Amazon Polly](https://aws.amazon.com/polly/) — text-to-speech
- [Amazon Translate](https://aws.amazon.com/translate/) · [Amazon Transcribe](https://aws.amazon.com/transcribe/)

### Cost Control for AI


### External references (vectors & RAG concepts)

- [Pinecone Learning Center](https://www.pinecone.io/learn/) — vector retrieval and RAG concept guides complementary to Bedrock RAG
- [Weaviate Blog](https://weaviate.io/blog) — vector database architecture and retrieval engineering articles

### Roundup

- [Top 20 modern AWS AI services — overview](#foundations)

---

## Developer Tools, DevOps & CI/CD

> 🎯 **Setting up CI/CD?** See the [CI/CD playbook](use-cases/ci-cd.md) — GitHub Actions + OIDC + per-environment accounts, with canary deploys, drift detection, and rollback runbook.

**Official:**
- [AWS DevOps & Developer Productivity Blog](https://aws.amazon.com/blogs/devops/) — CI/CD, CDK, and platform engineering posts

### AWS CloudFormation

> Native infrastructure-as-code in YAML/JSON.
- [CloudFormation Documentation](https://docs.aws.amazon.com/cloudformation/)

### AWS CDK — Cloud Development Kit

> Imperative IaC in TypeScript / Python / Java / Go / .NET.
- [CDK Documentation](https://docs.aws.amazon.com/cdk/)
- [Construct Hub](https://constructs.dev/) — community CDK constructs

**OSS Tools:**
- [cdklabs/cdk-nag](https://github.com/cdklabs/cdk-nag) — checks CDK apps against AWS Solutions, HIPAA, NIST, PCI rule packs at synth time
- [projen/projen](https://github.com/projen/projen) — define and synthesise project configuration as code (CDK-style for repos)
- [aws-samples/aws-cdk-examples](https://github.com/aws-samples/aws-cdk-examples) — official patterns in TS, Python, Java, Go, .NET

### Terraform on AWS

- [OpenTofu](https://opentofu.org/) — open-source Terraform-compatible infrastructure-as-code engine
- [HashiCorp AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest)

### Pulumi on AWS

> Imperative IaC in TypeScript / Python / Go / .NET / Java with real programming-language constructs.

- [Pulumi AWS provider](https://www.pulumi.com/registry/packages/aws/) — official provider docs
- [Pulumi AWS Native](https://www.pulumi.com/registry/packages/aws-native/) — generated from CloudFormation schema for full coverage
- [Pulumi vs Terraform](https://www.pulumi.com/docs/iac/comparisons/terraform/) — official comparison
- [Pulumi vs CDK](https://www.pulumi.com/docs/iac/comparisons/aws-cdk/) — official comparison

### SST

> TypeScript-native IaC purpose-built for serverless on AWS.

- [SST](https://sst.dev/) — full-stack framework on AWS
- [SST Documentation](https://sst.dev/docs/) — Ion (v3) is AWS-only with Pulumi/Terraform under the hood
- [SST Components](https://sst.dev/docs/components/) — high-level constructs for common AWS patterns
- [SST Blog](https://sst.dev/blog/) — SST team posts on serverless patterns on AWS

### AWS CodePipeline / CodeBuild / CodeDeploy

- [CodePipeline](https://aws.amazon.com/codepipeline/) · [CodeBuild](https://aws.amazon.com/codebuild/) · [CodeDeploy](https://aws.amazon.com/codedeploy/)

### GitHub Actions on AWS


### CI/CD vendor engineering blogs

- [CircleCI Blog](https://circleci.com/blog/) — CI/CD pipeline engineering posts useful for AWS-deployed apps
- [Spinnaker Community](https://spinnaker.io/docs/community/) — continuous delivery platform community hub

### General DevOps Practice


### Local Dev / Emulators

- [LocalStack](https://www.localstack.cloud/) — AWS-in-a-box for local dev
- [ministackorg/ministack](https://github.com/ministackorg/ministack) — MIT local AWS emulator; 40+ services; Terraform and SDK compatible
- [floci-io/floci](https://github.com/floci-io/floci) — MIT local AWS emulator; Docker Compose; broad AWS API coverage
- [getmoto/moto](#oss-lambda-frameworks-community) — mock AWS services for Python tests (boto3 stub library)

### CLI & Productivity OSS

- [awslogs](https://github.com/jorgebastida/awslogs) — query CloudWatch Logs from the terminal (the everyday-driver tool)
- [aws-shell](https://github.com/awslabs/aws-shell) — interactive shell with autocomplete for the AWS CLI
- [awless](https://github.com/wallix/awless) — opinionated Go-based CLI for EC2, IAM, S3 (declarative templates)
- [saws](https://github.com/donnemartin/saws) — supercharged AWS CLI with autocomplete + syntax highlighting

### CloudFormation OSS Tools

- [cfn-lint](https://github.com/aws-cloudformation/cfn-lint) — official CloudFormation template linter — catches schema, resource, and intrinsic-function errors before deploy
- [Stelligent/cfn_nag](https://github.com/stelligent/cfn_nag) — CFN security linting (insecure IAM, S3 public, etc.)
- [cloudtools/troposphere](https://github.com/cloudtools/troposphere) — Python library for generating CloudFormation templates
- [cloudreach/sceptre](https://github.com/Sceptre/sceptre) — CLI-driven CloudFormation orchestration

### AWS CLI / SDKs / Cloud9

- [AWS CLI v2](https://aws.amazon.com/cli/)
- [AWS SDK list](https://builder.aws.com/build/tools) — Python (boto3), JS, Java, Go, Rust, ...
- [AWS CloudShell](https://aws.amazon.com/cloudshell/) — browser shell with credentials pre-loaded
- [AWS Toolkit for VS Code / JetBrains](https://aws.amazon.com/visualstudiocode/)

### Asset Pipelines / Runtimes


---

## Observability & Monitoring

> 🎯 **Building an observability pipeline at scale?** See the [Observability pipeline playbook](use-cases/observability-pipeline.md) — hot CloudWatch + cold S3-Athena, EMF metrics, trace sampling, PII redaction, and cost discipline.

### Amazon CloudWatch

**Official:**
- [CloudWatch Documentation](https://docs.aws.amazon.com/cloudwatch/)
- [CloudWatch Application Signals](https://aws.amazon.com/cloudwatch/features/application-observability-apm/) — auto-instrumented APM with SLO tracking
- [CloudWatch Logs Insights](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/AnalyzingLogData.html) — query language for log analytics


### AWS X-Ray

- [X-Ray](https://aws.amazon.com/cloudwatch/features/application-observability-apm/) — distributed tracing; in maintenance per AWS lifecycle docs [maintenance]

### OpenTelemetry on AWS

**Official:**
- [AWS Distro for OpenTelemetry (ADOT)](https://aws-otel.github.io/) — recommended successor to X-Ray for new tracing
- [ADOT Documentation](https://aws-otel.github.io/docs/introduction/)
- [ADOT Lambda layer](https://aws-otel.github.io/docs/getting-started/lambda/) — auto-instrumentation for Lambda


### Amazon Managed Service for Prometheus / Grafana

- [Amazon Managed Prometheus (AMP)](https://aws.amazon.com/prometheus/) · [Amazon Managed Grafana (AMG)](https://aws.amazon.com/grafana/)

### Operational Monitoring


### Log Pipelines

- [Stream CloudWatch Logs to S3 via Firehose](https://docs.aws.amazon.com/firehose/latest/dev/writing-with-cloudwatch-logs.html) — official log pipeline pattern
- [Querying CloudWatch logs in S3 with Athena](https://docs.aws.amazon.com/athena/latest/ug/) — long-term log analytics on cold storage
- [Centralized Logging with OpenSearch (Solutions)](https://docs.aws.amazon.com/solutions/centralized-logging-with-opensearch/) — official deployable reference

### Third-party

- [Honeycomb Blog](https://www.honeycomb.io/blog) — distributed systems observability engineering posts
- [Datadog Engineering — Kubernetes topic](https://www.datadoghq.com/blog/topic/kubernetes/) — Kubernetes reliability and operations articles
- [Lumigo Blog](https://lumigo.io/blog/) — serverless observability and Lambda troubleshooting articles

---

## Cost Management & FinOps

> 🎯 **Hunting a surprise bill?** See the [Cost pitfalls playbook](use-cases/cost-pitfalls.md) — NAT Gateway egress, cross-AZ traffic, CloudWatch Logs ingestion, and the other line items that surprise teams.
>
> For a quarterly optimization cadence, see the [Cost pitfalls playbook](use-cases/cost-pitfalls.md#quarterly-optimization-cadence) and the [FinOps governance playbook](use-cases/finops-governance.md). For FinOps SaaS rollout, see [AWS cost optimization services](https://www.factualminds.com/services/aws-cloud-cost-optimization-services/?utm_source=aws-open-guide&utm_medium=readme&utm_campaign=cost-management-finops).

### Analysis & visibility

**Official:**
- [AWS Cost Explorer](https://aws.amazon.com/aws-cost-management/aws-cost-explorer/)
- [AWS Cost Optimization Hub](https://aws.amazon.com/aws-cost-management/cost-optimization-hub/) — consolidated waste and savings recommendations
- [AWS Billing and Cost Management — user guide](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/) — accounts, invoices, allocation tags
- [Cost and Usage Reports (CUR)](https://docs.aws.amazon.com/cur/latest/userguide/) — hourly or daily line-item billing export
- [Billing and Cost Management data exports](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/) — CUR and cost data to S3 or Athena
- [Billing views](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/) — scoped cost views for teams and accounts
- [AWS Trusted Advisor](https://aws.amazon.com/premiumsupport/technology/trusted-advisor/)
- [AWS Customer Carbon Footprint Tool](https://aws.amazon.com/sustainability/tools/console/) — estimated emissions by service and region

**OSS Tools:**
- [Cloud Intelligence Dashboards](https://github.com/aws-solutions-library-samples/cloud-intelligence-dashboards-framework) — CUR analytics dashboards (CUDOS, Cost Intelligence, KPI)
- [Komiser](https://github.com/mlabouardy/komiser) — multi-cloud cost and resource viewer
- [Similarweb/finala](https://github.com/similarweb/finala) — scans AWS for wasteful and unused resources

### FinOps platforms (third-party)

- [nOps](https://www.nops.io/) — AWS cost optimization, Savings Plans, RI management, EKS optimization
- [CloudZero](https://www.cloudzero.com/) — cost intelligence for engineering teams
- [Vantage](https://www.vantage.sh/) — AWS/GCP/Azure cost management
- [Finout](https://www.finout.io/) — cost allocation and FinOps analytics
- [ProsperOps](https://www.prosperops.com/) — automated Savings Plans optimization
- [Kubecost](https://www.kubecost.com/) — Kubernetes cost optimization
- [CloudBurn](https://cloudburn.io/) — open-source AWS cost policy engine for IaC and live scanning
- [FinOps governance playbook](use-cases/finops-governance.md) — tagging, CUR, allocation, and quarterly optimization cadence

### Rightsizing

**Official:**
- [AWS Compute Optimizer](https://aws.amazon.com/compute-optimizer/)
- [Compute Optimizer user guide](https://docs.aws.amazon.com/compute-optimizer/latest/ug/) — EC2 rightsizing and cross-architecture Graviton migration recommendations
- [Operating Lambda — performance optimization (Compute Blog)](https://aws.amazon.com/blogs/compute/operating-lambda-performance-optimization-part-2/) — memory and cost trade-offs

**OSS Tools:**
- [alexcasalboni/aws-lambda-power-tuning](https://github.com/alexcasalboni/aws-lambda-power-tuning) — Step Functions tool to find optimal Lambda memory

See also: [AWS Graviton](#aws-graviton--arm-based-processors) · [Cost pitfalls — EBS gp2 vs gp3](use-cases/cost-pitfalls.md#ebs-gp2-vs-gp3-almost-free-win) · [Idle resources](use-cases/cost-pitfalls.md#idle-resources) · [Lambda over-provisioned memory](use-cases/cost-pitfalls.md#lambda-over-provisioned-memory)

### Commitment discounts (Savings Plans & Reserved Instances)

**Official:**
- [Savings Plans](https://aws.amazon.com/savingsplans/) · [Reserved Instances](https://aws.amazon.com/ec2/pricing/reserved-instances/)
- [Savings Plans recommendations](https://docs.aws.amazon.com/savingsplans/latest/userguide/sp-recommendations.html)
- [Reserved Instance recommendations in Cost Explorer](https://docs.aws.amazon.com/cost-management/latest/userguide/ri-recommendations.html)


See also: [Cost pitfalls — reserved capacity and Savings Plans](use-cases/cost-pitfalls.md#reserved-capacity-and-savings-plans)

### Spot & interruptible compute

**Official:**
- [EC2 Spot best practices](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/spot-best-practices.html)
- [Fargate capacity providers](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/fargate-capacity-providers.html) — includes Fargate Spot

**Production Guides:**
- [EC2 Spot Instance intelligent selection](#amazon-ec2--elastic-compute-cloud) — cost optimization for Spot workloads

### Storage optimization

**Official:**
- [S3 Intelligent-Tiering](https://docs.aws.amazon.com/AmazonS3/latest/userguide/intelligent-tiering.html)
- [S3 lifecycle configurations](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lifecycle-mgmt.html)
- [EBS pricing](https://aws.amazon.com/ebs/pricing/)

**Production Guides:**
- [S3 storage costs aren't actually cheap](#amazon-s3--simple-storage-service) — real teardown

See also: [Cost pitfalls — EBS gp2 vs gp3](use-cases/cost-pitfalls.md#ebs-gp2-vs-gp3-almost-free-win) · [File upload playbook — S3 lifecycle](use-cases/file-upload.md)

### Network cost optimization

**Official:**
- [EC2 data transfer pricing](https://aws.amazon.com/ec2/pricing/on-demand/#Data_Transfer)
- [VPC pricing](https://aws.amazon.com/vpc/pricing/) — NAT Gateway and data processing
- [CloudFront pricing](https://aws.amazon.com/cloudfront/pricing/)

**Production Guides:**
- [NAT Gateway billing — idle cost alternatives](#nat-gateway) — bill teardown

See also: [Cost pitfalls — NAT Gateway](use-cases/cost-pitfalls.md#nat-gateway) · [Cross-AZ data transfer](use-cases/cost-pitfalls.md#cross-az-data-transfer) · [Egress to internet](use-cases/cost-pitfalls.md#egress-to-internet)

### Container cost optimization

**Official:**
- [Amazon EKS best practices — cost optimization](https://docs.aws.amazon.com/eks/latest/best-practices/cost-opt.html)
- [ECS pricing](#amazon-ecs--elastic-container-service) · [Fargate pricing](#aws-fargate)

**Production Guides:**
- [Deploy EKS with Karpenter for cost-optimized autoscaling](#amazon-eks--elastic-kubernetes-service)
- [Karpenter vs Cluster Autoscaler — EKS cost optimization](#amazon-eks--elastic-kubernetes-service)

**Kubernetes cost & ops (vendor blogs):**
- [Cast AI Blog](#amazon-eks--elastic-kubernetes-service) — Kubernetes cost optimization guidance

See also: [Spot & interruptible compute](#spot--interruptible-compute) · [Fargate](#aws-fargate) · [Amazon ECS](#amazon-ecs--elastic-container-service) · [FinOps governance playbook](use-cases/finops-governance.md)

### Serverless cost optimization

**Official:**
- [Lambda pricing](#aws-lambda)
- [Step Functions pricing](https://aws.amazon.com/step-functions/pricing/)
- [API Gateway pricing](https://aws.amazon.com/api-gateway/pricing/)

**Production Guides:**
- [Lambda cost optimization — pay-per-request vs provisioned](#aws-lambda)

See also: [Rightsizing](#rightsizing) · [Cost pitfalls — Lambda over-provisioned memory](use-cases/cost-pitfalls.md#lambda-over-provisioned-memory)

### Cost allocation & tagging

**Official:**
- [Cost Categories](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/manage-cost-categories.html) — tag-based rollup in Cost Explorer
- [Tag policies (Organizations)](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_tag-policies.html)
- [Split cost allocation data](https://docs.aws.amazon.com/cur/latest/userguide/split-cost-allocation-data.html) — per-pod cost for shared EKS or ECS


See also: [Multi-tenant SaaS playbook — cost attribution](use-cases/multi-tenant-saas.md) · [FinOps Foundation](#finops-community)

### Monitoring & alerts

**Official:**
- [AWS Budgets](https://aws.amazon.com/aws-cost-management/aws-budgets/)
- [Budget actions](https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-action-configure.html) — IAM, SNS, or SSM actions at thresholds
- [AWS Cost Anomaly Detection](https://aws.amazon.com/aws-cost-management/aws-cost-anomaly-detection/)
- [Cost Anomaly Detection user guide](https://docs.aws.amazon.com/cost-management/latest/userguide/manage-ad.html)


### Strategy & playbooks


### FinOps community

- [FinOps Foundation](https://www.finops.org/) — global community
- [FinOps Foundation Insights](https://www.finops.org/insights/) — foundation articles on cloud financial operations

### Bill teardowns (real customer incidents)

- [Bill teardown #2 — healthcare's NAT Gateway problem](#nat-gateway)

**OSS cost tools:**
- [Infracost](https://www.infracost.io/) — Terraform cost diff in PRs
- [cloud-custodian/cloud-custodian](https://github.com/cloud-custodian/cloud-custodian) — YAML rules for resource governance and cost enforcement
- [aws-nuke](#data-perimeter) — wipe orphaned dev accounts

---

## Migration & Transfer

### AWS Migration Hub & MAP

- [AWS Migration Hub](https://aws.amazon.com/transform/)
- [Migration Acceleration Program (MAP)](https://aws.amazon.com/migration-acceleration-program/)

### AWS Application Migration Service (MGN) & DMS

- [Application Migration Service](https://aws.amazon.com/application-migration-service/)
- [Database Migration Service (DMS)](https://aws.amazon.com/dms/)

### Migration Strategy


### Disaster Recovery


### VMware → AWS

- [Amazon Elastic VMware Service](#amazon-elastic-vmware-service-evs)

---

## Internet of Things (IoT)

### AWS IoT Core

**Official:**
- [IoT Core Documentation](https://docs.aws.amazon.com/iot/)
- [AWS IoT Blog](https://aws.amazon.com/blogs/iot/) — device connectivity, Greengrass, and industrial IoT posts


### AWS IoT Greengrass


### AWS IoT SiteWise


### AWS IoT TwinMaker


### Architecture


---

## Application Integration

> 🎯 **Building async/event-driven systems?** See [Async job processing](use-cases/async-jobs.md) (queue + worker + DLQ) and [Event-driven processing](use-cases/event-driven.md) (EventBridge with schemas, replay, per-target DLQs).

### Amazon SQS

**Official:**
- [SQS Documentation](https://docs.aws.amazon.com/sqs/)
- [Application Integration category (AWS News Blog)](https://aws.amazon.com/blogs/aws/category/application-integration/) — EventBridge, Step Functions, and messaging launches


### Amazon SNS

- [SNS Documentation](https://docs.aws.amazon.com/sns/) — pub/sub fan-out

### Amazon EventBridge

- See [Serverless](#serverless) section

### Amazon MQ

- [Amazon MQ](https://aws.amazon.com/amazon-mq/) — managed RabbitMQ + ActiveMQ

### AWS AppFlow

- [AppFlow](https://aws.amazon.com/appflow/) — SaaS-to-AWS data sync

---

## Email & Communication

### Amazon SES — Simple Email Service

> 🎯 **Building transactional email at scale?** Start with the [Email delivery playbook](use-cases/email-delivery.md) — full architecture (SES → SNS → Firehose → S3 → Athena), bounce/complaint handling, IP warming, cost model, and 18-item production checklist.

- [SES Documentation](https://docs.aws.amazon.com/ses/)

### SES Migrations from Competitors


---

## Management & Governance

### AWS Organizations

- [AWS Organizations](https://aws.amazon.com/organizations/)

### AWS Control Tower & Landing Zone

- [Control Tower](https://aws.amazon.com/controltower/)

**Third-party narratives:**
- [Monzo Bank (AWS customer story)](https://aws.amazon.com/solutions/case-studies/) — digital bank on AWS; scale and account-boundary themes
- [How Segment uses Okta to secure access to 100 AWS accounts](https://aws.amazon.com/blogs/startups/how-segment-uses-okta-to-secure-access-to-100-accounts/) — hub-and-spoke IAM and multi-account scaling practices
- [Shopify Engineering](https://shopify.engineering/) — backend engineering posts including AWS-scale commerce infrastructure
- [Revamping with Landing Zone — multi-account rebuild (WealthPark)](https://medium.com/wealthpark-engineering/revamping-with-landing-zone-exploring-multi-account-aws-architecture-in-our-infrastructure-rebuild-6b1f2da9327) — Landing Zone–oriented infrastructure rebuild walkthrough
- [Enterprise Landing Zone decisions — lessons learned, Part 1](https://medium.com/@malavaln/dive-deep-on-our-aws-landing-zone-architecture-decisions-made-lessons-learnt-part-1-898604d7aaaf) — large-org LZ architecture decisions and tradeoffs

### AWS Config

- [AWS Config](https://aws.amazon.com/config/) — resource inventory + compliance

### Service Limits, Quotas & Throttling

> Hard vs soft limits, retry strategy, and the throttling behaviour that bites at scale.

**Official:**
- [Service Quotas console](https://docs.aws.amazon.com/servicequotas/latest/userguide/intro.html) — view and request increases for soft limits
- [AWS service quotas reference](https://docs.aws.amazon.com/general/latest/gr/aws_service_limits.html) — per-service hard and soft limits
- [Error retries and exponential backoff (SDK guidance)](https://docs.aws.amazon.com/sdkref/latest/guide/feature-retry-behavior.html) — official retry behaviour
- [Timeouts, retries, and backoff with jitter (Builders Library)](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/) — first-principles guidance
- [API Gateway throttling](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-request-throttling.html) — account-, stage-, and key-level limits
- [Lambda concurrency and throttling](https://docs.aws.amazon.com/lambda/latest/dg/lambda-concurrency.html) — reserved vs provisioned concurrency
- [DynamoDB throttling and adaptive capacity](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-partition-key-design.html) — partition-level throttling

### AWS Support & MSP

- [AWS Support Plans](https://aws.amazon.com/premiumsupport/plans/)

### Hiring an AWS Consultant


### AWS Partner Network

- [AWS Partner Network (APN)](https://aws.amazon.com/partners/)

---

## Well-Architected Framework

> Six pillars: Operational Excellence, Security, Reliability, Performance Efficiency, Cost Optimization, Sustainability.

- [Well-Architected Framework — official](#foundations)
- [WAF Tool (free review)](https://aws.amazon.com/well-architected-tool/)
- [WAF lenses (Serverless, SaaS, GenAI, ...)](https://aws.amazon.com/architecture/well-architected/?ref=wellarchitected-wp&wa-lens-whitepapers.sort-by=item.additionalFields.sortDate&wa-lens-whitepapers.sort-order=desc)
- [Reliability Pillar (official whitepaper)](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/) — failure isolation, recovery, multi-AZ
- [Cost Optimization Pillar (official whitepaper)](https://docs.aws.amazon.com/wellarchitected/latest/cost-optimization-pillar/) — practices for spend efficiency
- [WAF 6 pillars explained](#foundations)

---

## Industry Architectures

End-to-end reference architectures for verticals.

### SaaS

- [How UNiDAYS achieved AWS Region expansion in three weeks](https://aws.amazon.com/blogs/architecture/how-unidays-achieved-aws-region-expansion-in-3-weeks/) — multi-Region SaaS rollout case study

### Startups


### Fintech

- [BFS health finance transformation on AWS — PCG DACH (Medium)](https://pcg-dach.medium.com/bfs-health-finance-a-journey-of-transformation-into-the-aws-cloud-11c44aa2af8b) — regulated workload migration with ECS and IaC themes

### Healthcare

- [How Artera enhances prostate cancer diagnostics using AWS](https://aws.amazon.com/blogs/architecture/how-artera-enhances-prostate-cancer-diagnostics-using-aws/) — imaging diagnostics workload architecture

### Retail & eCommerce


### Manufacturing & Industrial IoT

- [AI on AWS for predictive maintenance — case study (Medium)](https://medium.com/@andreas.braun.2011/ai-on-aws-architecture-interface-and-resilience-a-case-study-on-leveraging-cloud-computing-in-47cdeba62e20) — industrial AI architecture, interfaces, and resilience framing on AWS

### Education / EdTech


### Real Estate / PropTech


---

## Decision Guides — X vs Y

When you know what you need but not which AWS service to use. For interactive decision trees and compare pages, see [FactualMinds decide hub](https://www.factualminds.com/decide/?utm_source=aws-open-guide&utm_medium=readme&utm_campaign=decision-guides).

### Compute

- [EC2 vs Lambda](#amazon-ec2-elastic-compute-cloud)
- [Lambda vs ECS Fargate](#aws-fargate)
- [ECS vs EKS](#decision)
- [Which AWS compute?](#amazon-ec2-elastic-compute-cloud)
- [M9g vs M8g — Graviton5 upgrade](#aws-graviton--arm-based-processors)
- [M9g vs M9gd — local NVMe or EBS](#aws-graviton--arm-based-processors)
- [Graviton vs x86 on EC2](#aws-graviton--arm-based-processors)

### Databases

- [RDS vs Aurora](#amazon-rds-relational-database-service)
- [Aurora Serverless vs Aurora provisioned](#amazon-aurora)
- [DynamoDB vs RDS](#amazon-dynamodb)
- [Which AWS database?](#decision-guides)

### Networking & CDN

- [CloudFront vs Cloudflare](#amazon-cloudfront)
- [WAF vs Network Firewall](#aws-waf-web-application-firewall)

### Security & Identity

- [GuardDuty vs Security Hub](#amazon-guardduty)
- [IAM Identity Center vs Cognito](#aws-iam-identity-center-formerly-sso)

### Integration

- [Step Functions vs EventBridge](#aws-step-functions)
- [Bedrock Agents vs Step Functions](#aws-step-functions)
- [Event-based processing for asynchronous communication (AWS Architecture Blog)](https://aws.amazon.com/blogs/architecture/event-based-processing-for-asynchronous-communication/) — choosing EventBridge vs SNS vs SQS and related characteristics

### CI/CD

- [CodePipeline vs GitHub Actions](#aws-codepipeline-codebuild-codedeploy)
- [Terraform vs CDK — IaC decision guide](#aws-cdk-cloud-development-kit)
- [Pulumi vs Terraform](#pulumi-on-aws) — official comparison
- [Pulumi vs CDK](#pulumi-on-aws) — official comparison

### AI/ML

- [Bedrock vs SageMaker](#amazon-sagemaker)
- [Bedrock Agents vs AgentCore](#amazon-bedrock-agentcore)
- [Amazon Q vs ChatGPT Enterprise](#amazon-q)

### Cloud Platform


### Consulting Partner Comparisons


---

## Migration Guides — From Other Platforms

- [Heroku Postgres → AWS RDS](#decision-guides)
- [MongoDB Atlas → DocumentDB](#amazon-documentdb)
- [SendGrid → SES](#ses-migrations-from-competitors)
- [Mailgun → SES](#ses-migrations-from-competitors)
- [Postmark → SES](#ses-migrations-from-competitors)
- [Resend → SES](#ses-migrations-from-competitors)
- [SparkPost → SES](#ses-migrations-from-competitors)
- [Elastic Email → SES](#ses-migrations-from-competitors)

---

## AWS Service Lifecycle & Deprecations

> What state is each service in? AWS publishes explicit lifecycle states — Maintenance, Sunset, Full Shutdown — and the roster changes faster than most curated lists track. This section flags the services that affect new architectural decisions and points at official replacements.

### Lifecycle reference

- [AWS Service Lifecycle](https://docs.aws.amazon.com/general/latest/gr/service-lifecycle.html) — official definitions of Maintenance, Sunset, Full Shutdown
- [Services in Full Shutdown](https://docs.aws.amazon.com/general/latest/gr/full_shutdown_services.html) — official roster of shut-down services with dates
- [AWS service changes — May 2025](https://aws.amazon.com/about-aws/whats-new/2025/05/aws-service-changes/) — most recent batch of lifecycle announcements
- [AWS Product Lifecycle blog post](https://aws.amazon.com/blogs/aws/introducing-the-aws-product-lifecycle-page-and-aws-service-availability-updates/) — context behind the lifecycle page

### Full shutdown — already removed

Highlights from the [official roster](#lifecycle-reference); see that page for the complete list and exact dates.

- [Amazon QLDB](https://aws.amazon.com/rds/aurora/) — ledger database; shut down July 31, 2025 [shutdown]
- [Amazon Kinesis Data Analytics for SQL](https://aws.amazon.com/managed-service-apache-flink/) — replacement → Managed Service for Apache Flink [shutdown]
- [Amazon CloudWatch Evidently](https://aws.amazon.com/cloudwatch/) — feature flags and A/B; shut down October 17, 2025 [shutdown]
- [AWS DataSync Discovery](https://aws.amazon.com/datasync/) — on-prem storage assessment; shut down May 20, 2025 [shutdown]
- [AWS Private 5G](https://aws.amazon.com/) — managed cellular networks; shut down May 20, 2025 [shutdown]
- [AWS BugBust](https://aws.amazon.com/codeguru/profiler/) — code-fix gamification; shut down August 13, 2025 [shutdown]
- [AWS OpsWorks (Stacks, Chef, Puppet)](https://aws.amazon.com/) — config management; shut down May 1, 2024 [shutdown]
- [AWS CodeStar](https://aws.amazon.com/) — project templates; shut down July 25, 2024 [shutdown]
- [AWS RoboMaker](https://aws.amazon.com/products/) — robotics simulation; shut down September 10, 2025 [shutdown]
- [Amazon Lookout for Metrics](https://aws.amazon.com/) — anomaly detection; shut down October 10, 2025 [shutdown]
- [Amazon Lookout for Vision](https://aws.amazon.com/) — defect detection; shut down October 31, 2025 [shutdown]
- [Amazon WorkDocs](https://aws.amazon.com/) — file storage and sharing; shut down April 25, 2025 [shutdown]
- [AWS IoT Analytics](https://aws.amazon.com/iot/) — replacement → IoT Core + Kinesis or EventBridge; shut down December 15, 2025 [shutdown]
- [AWS SimSpace Weaver](https://aws.amazon.com/) — large-scale spatial simulations; shut down March 31, 2026 [shutdown]
- [Amazon Connect Voice ID](https://docs.aws.amazon.com/connect/latest/adminguide/voice-id.html) — caller authentication; shut down May 20, 2026 [shutdown]
- [AWS DMS Fleet Advisor](https://docs.aws.amazon.com/dms/latest/userguide/) — replacement → AWS DMS; shut down May 20, 2026 [shutdown]
- [AWS IoT Events](https://aws.amazon.com/iot-events/) — event detection; replacement → EventBridge + Lambda; shut down May 20, 2026 [shutdown]
- [AWS IQ](https://aws.amazon.com/partners/find-a-partner/) — freelance AWS experts marketplace; shut down May 20, 2026 [shutdown]
- [AWS Panorama](https://aws.amazon.com/panorama/) — appliance-based computer vision at the edge; shut down May 20, 2026 [shutdown]
- [Amazon Inspector Classic](https://docs.aws.amazon.com/inspector/v1/userguide/inspector_introduction.html) — replacement → Amazon Inspector v2; shut down May 20, 2026 [shutdown]

### End-of-support announced — avoid for new projects

Per the [May 2025 AWS service changes announcement](#lifecycle-reference). AWS has not yet published an exact end-of-support date.

- [Amazon Pinpoint](https://aws.amazon.com/pinpoint/) — multi-channel messaging; replacement → SES, SNS, EventBridge [sunset]

### Maintenance — closed to new customers

Per AWS lifecycle docs: existing customers retain access; no new features, no onboarding.

- [AWS X-Ray](#aws-x-ray) — distributed tracing; in maintenance per AWS lifecycle docs [maintenance]
- [Amazon Timestream for LiveAnalytics](#amazon-timestream) — closed to new customers June 20, 2025 [maintenance]

### Status tags used in this guide

- `[shutdown]` — fully removed from AWS; no access
- `[sunset]` — end-of-support announced; plan migration now
- `[maintenance]` — no new customers, no major features
- `[preview]` — preview release; not yet generally available

See [CONTRIBUTING.md](CONTRIBUTING.md#status-tags) for sourcing rules.

---

## Free Tools & Calculators

Free, no-signup AWS planning calculators and assessments:

### Cost & Pricing

- [AWS Lambda vs Container Cost Calculator](#aws-lambda)
- [AWS RDS Max Connection Calculator](#amazon-rds-relational-database-service)
- [AWS Bedrock Token Cost Calculator](#cost-control-for-ai)

### Migration & Assessment

- [Cloud Migration Estimator](#migration-strategy)
- [AWS Well-Architected Assessment](#well-architected-framework)
- [HIPAA Compliance Checker](#hipaa)

### Official AWS Tools

- [AWS Pricing Calculator](#foundations)
- [AWS Total Cost of Ownership (TCO) Calculator](https://calculator.aws/#/)

---

## AWS Glossary

Plain-language definitions of common AWS terms:

- [Amazon Aurora](#amazon-aurora)
- [Amazon Bedrock](#amazon-bedrock)
- [Amazon CloudWatch](#amazon-cloudwatch)
- [Amazon DynamoDB](#amazon-dynamodb)
- [Amazon EC2](#amazon-ec2-elastic-compute-cloud)
- [Amazon EKS](#amazon-eks-elastic-kubernetes-service)
- [Amazon RDS](#amazon-rds-relational-database-service)
- [Amazon Redshift](#amazon-redshift)
- [Amazon S3](#amazon-s3-simple-storage-service)
- [Amazon VPC](#amazon-vpc-virtual-private-cloud)
- [AWS CloudTrail](#aws-cloudtrail)
- [AWS Config Rules](#aws-config)
- [AWS Control Tower](#aws-control-tower-landing-zone)
- [AWS IAM](#aws-iam-identity-access-management)
- [AWS KMS](#aws-kms-key-management-service)
- [AWS Lambda](#aws-lambda)
- [AWS Landing Zone](#aws-control-tower-landing-zone)
- [AWS Organizations + SCPs](#aws-organizations)
- [AWS Savings Plans](#savings-plans-reserved-instances)
- [AWS Shared Responsibility Model](#foundations)
- [AWS Step Functions](#aws-step-functions)
- [FinOps](#finops-community)
- [HIPAA-eligible AWS services](#hipaa)
- [PCI DSS Cardholder Data Environment](#pci-dss)
- [RAG pipeline](#amazon-bedrock)
- [Reserved Instances vs Savings Plans](#savings-plans-reserved-instances)
- [SOC 2 Type 2](#soc-2)
- [VPC peering vs Transit Gateway](#amazon-vpc-virtual-private-cloud)
- [Well-Architected Framework](#well-architected-framework)

---

## AWS Certifications & Learning Paths

### Official

- [AWS Certifications overview](https://aws.amazon.com/certification/)
- [AWS Skill Builder](https://skillbuilder.aws/) — official free training
- [AWS Ramp-Up Guides](https://aws.amazon.com/training/ramp-up-guides/) — role-based learning paths by job function
- [Well-Architected Labs](https://www.wellarchitectedlabs.com/) — hands-on Well-Architected Framework labs
- [AWS Workshops catalog](https://builder.aws.com/build/workshops)

### Cert Deep Dives


---

## Architecture Patterns

Reference patterns for the workloads that show up most often. Each links into the relevant service sections for depth.

### Multi-tenant SaaS

> 🎯 **Building a multi-tenant SaaS?** Start with the [Multi-tenant SaaS playbook](use-cases/multi-tenant-saas.md) — full architecture, failure modes, cost model, anti-patterns, and production checklist.

- [Multi-tenant SaaS on AWS — pattern](#saas)
- [SaaS multi-tenancy — silo vs pool vs bridge](#saas)
- [Multi-tenant architecture — glossary](#aws-glossary)

**Reference implementations:**
- [aws-samples/aws-saas-factory-ref-solution-serverless-saas](https://github.com/aws-samples/aws-saas-factory-ref-solution-serverless-saas) — production serverless multi-tenant reference
- [aws-samples/aws-saas-factory-eks-reference-architecture](https://github.com/aws-samples/aws-saas-factory-eks-reference-architecture) — EKS multi-tenant reference
- [AWS SaaS Factory](https://aws.amazon.com/partners/marketplace/) — AWS programme with reference architectures and tooling

**Official (AWS Architecture Blog):**
- [Build a multi-tenant configuration system with tagged storage](https://aws.amazon.com/blogs/architecture/build-a-multi-tenant-configuration-system-with-tagged-storage-patterns/) — tenant-scoped configuration and tagging patterns
- [6,000 AWS accounts, three people, one platform — lessons learned](https://aws.amazon.com/blogs/architecture/6000-aws-accounts-three-people-one-platform-lessons-learned/) — multi-account SaaS control-plane lessons
- [Let’s Architect! Building multi-tenant SaaS systems](https://aws.amazon.com/blogs/architecture/lets-architect-building-multi-tenant-saas-systems/) — pooled vs silo models and isolation basics

See also: [Cognito for SaaS auth](#amazon-cognito) · [DynamoDB single-table for SaaS](#amazon-dynamodb) · [Multi-tenant SaaS playbook](use-cases/multi-tenant-saas.md)

### Event-driven & async

- [EventBridge event-driven architecture patterns](#amazon-eventbridge)
- [AWS Event-Driven Architecture](#amazon-eventbridge) — patterns and reference architectures
- [Step Functions workflow orchestration patterns](#aws-step-functions)
- See also: [SQS reliable messaging patterns](#amazon-sqs) · [EventBridge](#amazon-eventbridge)

**Official (AWS Architecture Blog):**
- [Mastering millisecond latency and millions of events — Amazon Key Suite](https://aws.amazon.com/blogs/architecture/mastering-millisecond-latency-and-millions-of-events-the-event-driven-architecture-behind-the-amazon-key-suite/) — EventBridge modernization and schema governance case study
- [Recursive scaling with Amazon SQS](https://aws.amazon.com/blogs/architecture/design-pattern-for-highly-parallel-compute-recursive-scaling-with-amazon-sqs/) — parallel compute fan-out using queues

**Additional guides:**
- [Build event-driven architectures with MSK and EventBridge (EventBridge Pipes)](https://aws.amazon.com/blogs/aws/new-create-point-to-point-integrations-between-event-producers-and-consumers-with-amazon-eventbridge-pipes/) — MSK as an EventBridge Pipes source
- [Apache Kafka vs RabbitMQ (CloudAMQP)](https://www.cloudamqp.com/blog/apachekafka-vs-rabbitmq.html) — broker comparison for MSK versus RabbitMQ-class workloads on AWS
- [Confluent Blog](https://www.confluent.io/blog/) — Kafka ecosystem articles relevant to MSK streaming architectures
- [microservices.io](https://microservices.io/) — microservices and event-driven architecture patterns catalog
- [Modernizing APIs with serverless on AWS (Medium)](https://medium.com/@shriyashetal7/modernising-apis-and-serverless-architecture-with-aws-f10aeda50a17) — API modernization walkthrough using AWS serverless services
- [Case study: SaaS API integration with serverless on AWS (Medium)](https://medium.com/@nitin_26346/case-study-integrate-apis-serverless-aws-architecture-37e297724a76) — multi-API sync architecture using AWS serverless components

### Multi-region & resilience

- [AWS Multi-Region Fundamentals](#foundations)
- [Static Stability Using Availability Zones](#foundations) — designing for failure
- [Reliability Pillar](#well-architected-framework)
- [DR strategies — pilot light / warm standby / multi-site](#disaster-recovery)
- [Multi-region AWS without doubling costs](#strategy-playbooks)

**Official:**
- [Plan for Disaster Recovery — Well-Architected Reliability Pillar](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/plan-for-disaster-recovery-dr.html) — RTO/RPO objectives and DR strategies
- [Shuffle sharding — massive and magical fault isolation](https://aws.amazon.com/blogs/architecture/shuffle-sharding-massive-and-magical-fault-isolation/) — Architecture Blog companion to shuffle-sharding essay
- [Journey to cloud-native architecture — resilience and observability (series 3)](https://aws.amazon.com/blogs/architecture/journey-to-adopt-cloud-native-architecture-series-3-improved-resilience-and-standardized-observability/) — standardized telemetry and resilience adoption

**Reference implementations:**
- [Route 53 Application Recovery Controller (ARC)](https://aws.amazon.com/application-recovery-controller/) — readiness checks and zonal shift
- [Multi-region failover with Route 53 ARC — AWS blog walkthrough](https://aws.amazon.com/blogs/networking-and-content-delivery/creating-disaster-recovery-mechanisms-using-amazon-route-53/) — official end-to-end pattern

**Community walkthroughs:**
- [Automated multi-region DR with Lambda and Route 53 (Medium)](https://ammarsuhail155.medium.com/building-an-automated-multi-region-disaster-recovery-system-on-aws-using-lambda-route53-f02e0e7befab) — DR automation walkthrough using AWS primitives

### Data lake & analytics

- [Building a data lake on S3 + Glue + Athena](#amazon-s3-simple-storage-service)
- [Build a serverless data pipeline — Glue + Athena](#data-pipelines-lakes)
- [Real-time pipeline — Kinesis + Lambda + DynamoDB](#amazon-kinesis)
- [Glue 5 + Apache Iceberg — modern ETL](#aws-glue)

**Official:**
- [AWS Big Data Blog](#analytics-big-data) — analytics, streaming, and data-platform posts
- [AWS Database Blog](#amazon-rds-relational-database-service) — relational and NoSQL operational patterns

### GenAI & RAG

- [Build a RAG pipeline with Bedrock Knowledge Bases](#amazon-bedrock)
- [Bedrock multi-agent supervisor pattern](#amazon-bedrock)
- [Multi-tenant GenAI on Bedrock](#amazon-bedrock)
- [Fine-tuning vs RAG on Bedrock](#amazon-bedrock)

**Official (AWS blogs):**
- [Serverless generative AI architectural patterns (Compute Blog)](https://aws.amazon.com/blogs/compute/serverless-generative-ai-architectural-patterns/) — Lambda-centric GenAI workload shapes
- [Architect a mature generative AI foundation on AWS (ML Blog)](https://aws.amazon.com/blogs/machine-learning/architect-a-mature-generative-ai-foundation-on-aws/) — platform layers for production GenAI
- [Architecting for agentic AI development on AWS (Architecture Blog)](https://aws.amazon.com/blogs/architecture/architecting-for-agentic-ai-development-on-aws/) — agentic AI reference architecture framing
- [Automate safety monitoring with computer vision and generative AI](https://aws.amazon.com/blogs/architecture/automate-safety-monitoring-with-computer-vision-and-generative-ai/) — CV + GenAI operational monitoring pattern

**Community walkthroughs:**
- [AI-powered media processing pipeline — serverless and Bedrock (Medium)](https://ammarsuhail155.medium.com/building-an-ai-powered-media-processing-pipeline-on-aws-serverless-architecture-70333e202de8) — serverless media pipeline walkthrough using Bedrock on AWS

### Migration

- [Refactor / replatform / rearchitect](#migration-strategy)
- [Migrate a monolith to ECS Fargate with zero downtime](#amazon-ecs-elastic-container-service)
- [Migrate without cost surprises](#migration-strategy)

**Official (AWS Architecture Blog):**
- [Building a three-tier architecture on a budget](https://aws.amazon.com/blogs/architecture/building-a-three-tier-architecture-on-a-budget/) — cost-conscious web/API/data layering
- [Let’s Architect! Designing microservices architectures](https://aws.amazon.com/blogs/architecture/lets-architect-designing-microservices-architectures/) — VPC Lattice, async integration, serverless microservices patterns
- [A multidimensional approach helps you proactively prepare for failures — part 1](https://aws.amazon.com/blogs/architecture/a-multi-dimensional-approach-helps-you-proactively-prepare-for-failures-part-1-application-layer/) — application-layer resilience checklist framing
- [Let’s Architect! Migrating to the cloud with AWS](https://aws.amazon.com/blogs/architecture/lets-architect-migrating-to-the-cloud-with-aws/) — migration patterns and modernization lens

**Community walkthroughs:**
- [Secure globally accelerated three-tier web architecture on AWS (Medium)](https://medium.com/@ayotomiwavictor1/building-a-secure-globally-accelerated-3-tier-web-architecture-on-aws-49b23c180173) — layered security with Global Accelerator on AWS
- [Production-ready isolated three-tier app on AWS (Medium)](https://medium.com/@mary-ogbonna/how-i-built-and-deployed-a-production-ready-three-tier-book-review-app-on-aws-b4f7bc9c714e) — VPC-tier isolation with an example workload deployment narrative

### Anti-patterns & common mistakes

> What teams get wrong on AWS — drawn from postmortems, bill-shock case studies, and scaling war stories.

- [The Amazon Builders' Library](#foundations) — first-person engineering writeups including how AWS itself avoids common mistakes
- [Avoiding insurmountable queue backlogs (Builders Library)](https://aws.amazon.com/builders-library/avoiding-insurmountable-queue-backlogs/) — the classic queue anti-pattern
- [Caching challenges and strategies (Builders Library)](https://aws.amazon.com/builders-library/caching-challenges-and-strategies/) — when caches make things worse
- [Avoiding overload in distributed systems by putting the smaller service in control (Builders Library)](https://aws.amazon.com/builders-library/avoiding-overload-in-distributed-systems-by-putting-the-smaller-service-in-control/) — load shedding done right
- [Bill teardowns — NAT Gateway, data transfer, Lambda runaway](#bill-teardowns-real-customer-incidents) — see Cost Management section for real customer incidents
- [Protect AWS infrastructure from cost-based attacks](#holistic-security-guides) — denial-of-wallet patterns

---

## AI Coding Agents, MCP & Skills

AI-assisted development on AWS — Model Context Protocol (MCP) servers, Claude Code agent plugins, and skill bundles that let coding agents (Claude Code, Cursor, Cline, Windsurf, Kiro, Q Developer) architect, deploy, and operate AWS systems with real-time service knowledge.

### AWS MCP Servers — `awslabs/mcp`

> [!NOTE]
> AWS publishes 50+ official open-source MCP servers. They give AI assistants live access to AWS docs, APIs, and service operations — no more stale model knowledge.

**Hub & docs:**
- [awslabs/mcp](https://github.com/awslabs/mcp) — canonical repository
- [Open Source MCP Servers for AWS — catalog](https://awslabs.github.io/mcp/) — full list with usage docs
- [Introducing AWS MCP Servers (AWS ML Blog)](https://aws.amazon.com/blogs/machine-learning/introducing-aws-mcp-servers-for-code-assistants-part-1/)
- [Unlocking the power of MCP on AWS (AWS ML Blog)](https://aws.amazon.com/blogs/machine-learning/unlocking-the-power-of-model-context-protocol-mcp-on-aws/)
- [AWS MCP Server (managed, in preview — re:Invent 2025)](https://docs.aws.amazon.com/agent-toolkit/latest/userguide/) — fully-managed remote server with Agent SOPs + CloudTrail logging
- [Model Context Protocol strategies on AWS — Prescriptive Guidance](https://docs.aws.amazon.com/prescriptive-guidance/latest/mcp-strategies/introduction.html) — MCP tool design, server hosting, and governance
- [Guidance for deploying MCP servers on AWS](https://docs.aws.amazon.com/solutions/deploying-model-context-protocol-servers-on-aws/) — AWS Solutions patterns for secure MCP server deployment
- [Tool integration strategy — agentic AI frameworks](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-frameworks/tool-integration-strategy.html) — MCP vs framework-native and meta-tools for agent workloads

**Essential / Core (start here):**
- [AWS API MCP Server](https://awslabs.github.io/mcp/servers/aws-api-mcp-server) — interact with all AWS services via CLI commands
- [AWS Knowledge MCP Server](https://awslabs.github.io/mcp/servers/aws-knowledge-mcp-server) — official docs, code samples, best practices
- [AWS Documentation MCP Server](https://awslabs.github.io/mcp/servers/aws-documentation-mcp-server) — latest AWS docs and API references

**Infrastructure & Deployment:**
- [AWS Cloud Control API MCP Server](https://awslabs.github.io/mcp/servers/ccapi-mcp-server) — full CRUDL on any AWS resource + integrated security scanning
- [Amazon EKS MCP Server](https://awslabs.github.io/mcp/servers/eks-mcp-server) — Kubernetes cluster + app deployment
- [Amazon ECS MCP Server](https://awslabs.github.io/mcp/servers/ecs-mcp-server) — container orchestration + ECS deployment
- [AWS Serverless MCP Server](https://awslabs.github.io/mcp/servers/aws-serverless-mcp-server) — full SAM-CLI serverless lifecycle
- [AWS Lambda Tool MCP Server](https://awslabs.github.io/mcp/servers/lambda-tool-mcp-server) — execute Lambda functions as AI tools (private resource access)
- [Finch MCP Server](https://awslabs.github.io/mcp/servers/finch-mcp-server) — local container builds with ECR integration
- [AWS Systems Manager for SAP MCP Server](https://awslabs.github.io/mcp/servers/aws-for-sap-management-mcp-server)
- [AWS Support MCP Server](https://awslabs.github.io/mcp/servers/aws-support-mcp-server) — manage AWS Support cases

**AI & Machine Learning:**
- [Amazon Bedrock Knowledge Bases Retrieval MCP Server](https://awslabs.github.io/mcp/servers/bedrock-kb-retrieval-mcp-server) — query enterprise KBs with citations
- [Amazon Bedrock AgentCore MCP Server](#amazon-bedrock-agentcore) — build, deploy, manage Bedrock agents
- [Amazon Bedrock Custom Model Import MCP Server](https://awslabs.github.io/mcp/servers/aws-bedrock-custom-model-import-mcp-server)
- [Amazon SageMaker AI MCP Server](https://awslabs.github.io/mcp/servers/sagemaker-ai-mcp-server)
- [Amazon Kendra Index MCP Server](https://awslabs.github.io/mcp/servers/amazon-kendra-index-mcp-server)
- [Amazon Q Index MCP Server](https://awslabs.github.io/mcp/servers/amazon-qindex-mcp-server) · [Q Business anonymous](https://awslabs.github.io/mcp/servers/amazon-qbusiness-anonymous-mcp-server)

**Data & Analytics:**
- [Amazon DynamoDB MCP Server](https://awslabs.github.io/mcp/servers/dynamodb-mcp-server)
- [Amazon Aurora PostgreSQL MCP Server](https://awslabs.github.io/mcp/servers/postgres-mcp-server) · [MySQL](https://awslabs.github.io/mcp/servers/mysql-mcp-server) · [DSQL](https://awslabs.github.io/mcp/servers/aurora-dsql-mcp-server)
- [Amazon DocumentDB MCP Server](https://awslabs.github.io/mcp/servers/documentdb-mcp-server)
- [Amazon Neptune MCP Server](https://awslabs.github.io/mcp/servers/amazon-neptune-mcp-server) — graph queries (openCypher + Gremlin)
- [Amazon Redshift MCP Server](https://awslabs.github.io/mcp/servers/redshift-mcp-server)
- [Amazon ElastiCache MCP Server](https://awslabs.github.io/mcp/servers/elasticache-mcp-server) · [Valkey](https://awslabs.github.io/mcp/servers/valkey-mcp-server) · [Memcached](https://awslabs.github.io/mcp/servers/memcached-mcp-server)
- [AWS S3 Tables MCP Server](https://awslabs.github.io/mcp/servers/s3-tables-mcp-server) — SQL on S3-based tables
- [Amazon Data Processing MCP Server](https://awslabs.github.io/mcp/servers/aws-dataprocessing-mcp-server) — AWS Glue + EMR + Athena

**Integration & Messaging:**
- [Amazon SNS / SQS MCP Server](https://awslabs.github.io/mcp/servers/amazon-sns-sqs-mcp-server)
- [Amazon MQ MCP Server](https://awslabs.github.io/mcp/servers/amazon-mq-mcp-server) — RabbitMQ + ActiveMQ
- [AWS Step Functions MCP Server](https://awslabs.github.io/mcp/servers/stepfunctions-tool-mcp-server)
- [AWS AppSync MCP Server](https://awslabs.github.io/mcp/servers/aws-appsync-mcp-server)
- [Amazon Location Service MCP Server](https://awslabs.github.io/mcp/servers/aws-location-mcp-server)
- [OpenAPI MCP Server](https://awslabs.github.io/mcp/servers/openapi-mcp-server) — dynamic API integration via OpenAPI specs

**Cost & Operations:**
- [AWS Billing and Cost Management MCP Server](https://awslabs.github.io/mcp/servers/billing-cost-management-mcp-server)
- [AWS Pricing MCP Server](https://awslabs.github.io/mcp/servers/aws-pricing-mcp-server) — pre-deployment cost estimation
- [Amazon CloudWatch MCP Server](https://awslabs.github.io/mcp/servers/cloudwatch-mcp-server) — metrics, alarms, logs analysis
- [Amazon CloudWatch Application Signals MCP Server](https://awslabs.github.io/mcp/servers/cloudwatch-applicationsignals-mcp-server)
- [AWS CloudTrail MCP Server](https://awslabs.github.io/mcp/servers/cloudtrail-mcp-server)
- [AWS Managed Prometheus MCP Server](https://awslabs.github.io/mcp/servers/prometheus-mcp-server)
- [AWS Well-Architected Security Assessment MCP Server](https://awslabs.github.io/mcp/servers/well-architected-security-mcp-server)

**Developer Tools:**
- [AWS IAM MCP Server](https://awslabs.github.io/mcp/servers/iam-mcp-server) — user, role, group, policy management with security best practices
- [AWS IoT SiteWise MCP Server](https://awslabs.github.io/mcp/servers/aws-iot-sitewise-mcp-server)

**Healthcare & Life Sciences:**
- [AWS HealthOmics MCP Server](https://awslabs.github.io/mcp/servers/aws-healthomics-mcp-server) — lifescience workflows
- [HealthImaging MCP Server](https://awslabs.github.io/mcp/servers/healthimaging-mcp-server) — DICOM operations
- [HealthLake MCP Server](https://awslabs.github.io/mcp/servers/healthlake-mcp-server) — FHIR datastores

### Autonomous coding agents on AWS

- [aws-samples/remote-swe-agents](https://github.com/aws-samples/remote-swe-agents) — Official sample deploying an autonomous coding agent on AWS with Bedrock, CDK, web UI, Slack, and MCP.

### Claude Code Agent Plugins & Skills for AWS

**Official (awslabs):**
- [awslabs/agent-plugins](https://github.com/awslabs/agent-plugins) — official plugins that equip Claude Code, Cursor, and Q Developer with deploy/architect/operate skills
- [Introducing Agent Plugins for AWS (Developer Tools Blog, Feb 2026)](https://aws.amazon.com/blogs/developer/introducing-agent-plugins-for-aws/)
- [`deploy-on-aws` plugin](https://github.com/awslabs/agent-plugins/tree/main/plugins/deploy-on-aws) — generates architecture recommendations, cost estimates, and infrastructure-as-code
- [Agent Plugin for AWS Serverless (Mar 2026)](https://aws.amazon.com/about-aws/whats-new/2026/03/agent-plugin-aws-serverless/) — Lambda, EventBridge, Step Functions, SAM/CDK
- [Getting Started with Agent Plugins for AWS + Claude Code (Builder Center)](https://builder.aws.com/content/39tWkKMGjPSXv4HOVoSm5C47ijN/from-deploy-to-aws-to-live-in-minutes-getting-started-with-agent-plugins-for-aws-and-claude-code)

**Community plugin bundles:**
- [zxkane/aws-skills](https://github.com/zxkane/aws-skills) — AWS CDK (with `cdk-nag`), Cost & Operations, Serverless & EDA, Bedrock AgentCore plugins
- [Build on AWS Faster with Claude Code and AWS Skills (Kane.mx)](https://kane.mx/posts/2025/aws-skills-claude-code/)

**Anthropic + Bedrock:**
- [Claude in Amazon Bedrock](https://aws.amazon.com/bedrock/anthropic/) — Anthropic models on Bedrock (incl. Claude Code workflows)
- [Claude with Amazon Bedrock — Anthropic Academy](https://anthropic.skilljar.com/claude-in-amazon-bedrock)

**Protocol & ecosystem:**
- [Model Context Protocol — official spec](https://modelcontextprotocol.io/docs/getting-started/intro) — Anthropic-led open protocol
- [punkpeye/awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers) — community catalog of all MCP servers (cross-vendor)
- [PulseMCP — AWS MCP servers directory](https://www.pulsemcp.com/servers?q=aws) — searchable index

---

## Engineering Blogs & Case Studies

How real companies run on AWS — production architectures, postmortems, and at-scale lessons. The "official docs" tell you what's possible; these tell you what actually broke.

### AWS Architecture Blog — customer stories

- [How Generali Malaysia optimizes operations with Amazon EKS](https://aws.amazon.com/blogs/architecture/how-generali-malaysia-optimizes-operations-with-amazon-eks/) — enterprise Kubernetes operations on AWS
- [Architecting conversational observability for cloud applications](https://aws.amazon.com/blogs/architecture/architecting-conversational-observability-for-cloud-applications/) — AI-assisted ops UX patterns on AWS

### Engineering blogs from companies on AWS

- [Netflix Tech Blog](https://netflixtechblog.com/) — large-scale streaming, microservices, resilience
- [Netflix Simian Army (origin of chaos engineering)](https://netflixtechblog.com/the-netflix-simian-army-16e57fbab116) — the canonical "break things on purpose" essay
- [Netflix Chaos Engineering tag](https://netflixtechblog.com/tagged/chaos-engineering) — ongoing chaos posts
- [Airbnb Engineering](https://medium.com/airbnb-engineering) — search & infra at hospitality scale
- [Dropbox Tech — Infrastructure](https://dropbox.tech/infrastructure) — famous AWS-→-bare-metal exit + return-to-cloud insights
- [Pinterest Engineering](https://medium.com/@Pinterest_Engineering) — high-RPS feed + storage architecture
- [Capital One Tech — Cloud](https://www.capitalone.com/tech/cloud/) — regulated-finance cloud-native transformation
- [Slack Engineering](https://slack.engineering/) — Slack infrastructure and backend engineering articles

### AWS leadership blogs

- [All Things Distributed](https://www.allthingsdistributed.com/) — Werner Vogels (AWS CTO); architecture philosophy, eventual consistency, "you build it, you run it"
- [Jeff Barr — Things I Like](https://jeff-barr.com/) — AWS Chief Evangelist; release commentary and historical context
- [AWS Geek (Jerry Hargrove)](https://www.awsgeek.com/) — illustrated AWS service diagrams + cheat sheets

### AWS official postmortems & resilience reading

- [Amazon S3 Outage Postmortem (Feb 2017, us-east-1)](https://aws.amazon.com/message/41926/) — the classic teardown; required reading for designing resilient architectures
- [Kinesis Data Streams Outage (Nov 2020, us-east-1)](https://aws.amazon.com/message/11201/) — thread-limit cascade that took down Cognito, CloudWatch, and dozens of dependents
- [Lambda / API Gateway / EventBridge Disruption (Jun 2023, us-east-1)](https://aws.amazon.com/message/061323/) — control-plane failure mode; lessons on regional blast radius
- [AWS Builders Library — Resilience & Failures](#foundations) — operations essays from AWS principal engineers (also linked from [Foundations](#foundations))

> [!IMPORTANT]
> Pair these with the [Reliability Pillar](#well-architected-framework) and [Static Stability Using AZs](#foundations) for the full failure-design picture. The recurring lesson: **us-east-1 is not a single region for outage purposes — global control planes live there.**

---

## Community, Social & Continuous Learning

How to plug into the AWS conversation, follow signal-rich voices, and stay current as services ship weekly.

### Official AWS learning & Q&A portals

- [AWS re:Post](https://repost.aws/) — official Q&A staffed by AWS engineers + community
- [AWS Skill Builder](#official) — official free training (also in [Certifications](#aws-certifications--learning-paths))
- [AWS Workshops](#official) — guided, step-by-step builds (also in [Certifications](#aws-certifications--learning-paths))
- [AWS re:Invent session catalog](https://aws.amazon.com/events/reinvent/) — annual deep architecture + announcements

### Independent blogs (high signal-to-noise)

- [Jeremy Daly](https://www.jeremydaly.com/) — serverless deep dives
- [Alex DeBrie](https://www.alexdebrie.com/) — DynamoDB, NoSQL data modeling
- [Last Week in AWS](https://www.lastweekinaws.com/blog/) — Corey Quinn's weekly curated updates
- [Jayendra's Blog](https://jayendrapatil.com/) — structured AWS cert + service learning

### X / Twitter accounts worth following

- [@AWSOpen](https://twitter.com/AWSOpen) — AWS open-source + cloud-native updates
- [@QuinnyPig](https://twitter.com/QuinnyPig) — Corey Quinn, cost commentary + critique
- [@adriancantrill](https://twitter.com/adriancantrill) — deep architecture
- [@forrestbrazeal](https://twitter.com/forrestbrazeal) — learning paths, Cloud Resume Challenge
- [@theburningmonk](https://twitter.com/theburningmonk) — Yan Cui, Lambda + serverless patterns
- [@jeffbarr](https://twitter.com/jeffbarr) — official AWS announcements

### Reddit (real-world issues, troubleshooting)

- [r/aws](https://www.reddit.com/r/aws/) — news, troubleshooting, ops issues
- [r/cloud](https://www.reddit.com/r/Cloud/) — multi-cloud discussions
- [r/devops](https://www.reddit.com/r/devops/) — infra patterns
- [r/AWSCertifications](https://www.reddit.com/r/AWSCertifications/) — exam + learning

> [!TIP]
> **Community insight:** understanding real architectures beats memorizing services.

### Hacker News (trends, debates, postmortems)

- [Hacker News](https://news.ycombinator.com/) — search for `AWS architecture`, `serverless vs containers`, `AWS outage postmortem`
- Strongest for: design tradeoffs, vendor lock-in debates, production failure analysis

### Q&A and community programs

- [Stack Overflow AWS Collective](https://stackoverflow.com/collectives/aws) — curated AWS answers
- [AWS Community Builders](https://builder.aws.com/community/community-builders) — recognized community experts
- [AWS Heroes](https://builder.aws.com/community/heroes) — top community contributors
- AWS-focused Slack / Discord communities — high signal for live ops issues

### Learning platforms (free + paid)

- [freeCodeCamp AWS courses](https://www.freecodecamp.org/news/tag/aws/) — free long-form video courses
- [Tutorials Dojo](https://tutorialsdojo.com/) — cert prep + practice exams
- [Pluralsight Cloud Guru](https://www.pluralsight.com/cloud-guru) — structured cert paths (also in [Books, Courses & Newsletters](#books-courses--newsletters))
- [Adrian Cantrill](https://learn.cantrill.io/) — deep-dive cert courses (also in [Books, Courses & Newsletters](#books-courses--newsletters))

### YouTube (practical demos)

- [Andrew Brown / ExamPro](https://www.youtube.com/@ExamProChannel) — full-length cert courses
- [Tech With Lucy](https://www.youtube.com/@TechWithLucy) — beginner → intermediate AWS
- [Be A Better Dev](https://www.youtube.com/@BeABetterDev) — AWS tutorials (also in [Books, Courses & Newsletters](#books-courses--newsletters))
- [AWS Events](https://www.youtube.com/@AWSEventsChannel) — re:Invent + Summit recordings

### How to actually learn AWS (community-derived strategy)

1. Learn via **architectures**, not isolated services — start from a real workload, then pick services.
2. Use **hands-on labs early** — AWS Workshops + Skill Builder + a sandbox account beat reading docs.
3. **Follow release streams continuously** — AWS ships weekly; What's New RSS + Last Week in AWS keep you current.
4. **Combine official + community sources** — official docs for accuracy, community for tradeoffs and gotchas.

### Minimal curated stack (best signal-to-noise)

If you only follow a handful of sources:

- **Blogs**: AWS Blog + Last Week in AWS
- **X**: @AWSOpen, Corey Quinn, Yan Cui
- **Community**: r/aws + AWS re:Post
- **Learning**: AWS Skill Builder + AWS Workshops
- **Deep learning**: re:Invent talks on YouTube

---

## Third-Party Integrations

Common SaaS / OSS integrations on AWS:

- [Datadog on AWS](#third-party)
- [GitHub Actions on AWS](#github-actions-on-aws)
- [Kubernetes on AWS EKS](#decision)
- [Snowflake on AWS](#data-pipelines-lakes)
- [Terraform on AWS](#terraform-on-aws)

---

## Books, Courses & Newsletters

### Newsletters (free)

- [Last Week in AWS](https://www.lastweekinaws.com/) — Corey Quinn
- [The Cloud Pod](https://www.thecloudpod.tv/) — multi-cloud podcast
- [AWS What's New RSS](https://aws.amazon.com/about-aws/whats-new/recent/feed/)
- [AWS Blog](https://aws.amazon.com/blogs/aws/)

### Books

- [AWS Well-Architected Framework whitepaper](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html) (free)

### Courses (paid)

- [Pluralsight Cloud Guru](#learning-platforms-free-paid) — cert-focused video courses
- [Stephane Maarek on Udemy](https://www.udemy.com/user/stephane-maarek/) — top-rated AWS cert prep
- [Adrian Cantrill](#learning-platforms-free-paid) — deep-dive cert courses

### YouTube Channels

- [Amazon Web Services](https://www.youtube.com/user/AmazonWebServices/Cloud) — official AWS channel
- [AWS Events](https://www.youtube.com/c/AWSEventsChannel) — re:Invent, summits, deep-dive sessions
- [Be A Better Dev](#youtube-practical-demos) — AWS tutorials

---

## Conferences & Events

- [AWS re:Invent](#official-aws-learning-q-a-portals) — Las Vegas, annual (December)
- [AWS re:Inforce](https://aws.amazon.com/events/reinforce/) — security-focused
- [AWS Summits](https://aws.amazon.com/events/summits/) — regional, free
- [AWS Community Days](https://aws.amazon.com/events/community-day/) — community-organized
- [Cloud Next](https://cloud.withgoogle.com/next/25) (GCP) and [Microsoft Build](https://build.microsoft.com/en-US/home) — useful for cross-cloud context

---

## Other Awesome AWS Lists

### Official AWS GitHub organizations

- [aws](https://github.com/aws) — primary AWS org: SDKs, CLI, core infrastructure tools (s2n-tls, aws-cli, aws-sdk-*)
- [awslabs](https://github.com/awslabs) — experimental + high-performance AWS-built tooling (mountpoint-s3, llrt, mcp, aws-sdk-rust, agent-plugins)
- [aws-samples](https://github.com/aws-samples) — reference architectures + sample code (educational; harden before production)
- [aws-actions](https://github.com/aws-actions) — official GitHub Actions for AWS CI/CD (configure-aws-credentials, ecs-deploy-task-definition, ecr-login)
- [aws-solutions](https://github.com/aws-solutions) — vetted AWS Solutions reference implementations
- [aws-controllers-k8s](https://github.com/aws-controllers-k8s) — ACK: native AWS service operators for Kubernetes
- [aws-cloudformation](https://github.com/aws-cloudformation) — CloudFormation hooks, registry, custom resource samples
- [amzn](https://github.com/amzn) — broader Amazon-wide projects (some AWS-relevant)

### Notable AWS-built repos worth bookmarking

**Performance & runtimes:**
- [awslabs/llrt](https://github.com/awslabs/llrt) — low-latency JavaScript runtime for Lambda
- [awslabs/mountpoint-s3](#amazon-s3-simple-storage-service) — high-throughput FUSE client for S3
- [awslabs/aws-sdk-rust](https://github.com/awslabs/aws-sdk-rust) — official Rust SDK
- [aws/karpenter-provider-aws](https://github.com/aws/karpenter-provider-aws) — node autoscaling for EKS

**AI / agents / MCP:**
- [awslabs/mcp](#aws-mcp-servers-awslabs-mcp) — official MCP servers (50+)
- [awslabs/agent-plugins](#claude-code-agent-plugins-skills-for-aws) — Claude Code / Cursor / Q Developer plugins
- [awslabs/agentcore-samples](#amazon-bedrock-agentcore) — production patterns for Bedrock AgentCore
- [aws-samples/remote-swe-agents](#autonomous-coding-agents-on-aws) — autonomous Bedrock-powered coding agent (CDK, Slack, MCP)
- [awslabs/generative-ai-atlas](https://github.com/awslabs/generative-ai-atlas) — GenAI architecture catalog

**Best-practice references:**
- [aws/aws-eks-best-practices](https://github.com/aws/aws-eks-best-practices) — published EKS guide
- [aws-samples/aws-cdk-examples](#aws-cdk-cloud-development-kit) — CDK patterns in TS, Python, Java, Go, .NET
- [aws-samples/aws-secure-environment-accelerator](https://github.com/aws-samples/aws-secure-environment-accelerator) — multi-account landing zone
- [aws-samples/aws-cudos-framework-deployment](#managed-vs-diy-cost) — Cloud Intelligence Dashboards (CUR analytics)

**Developer tooling:**
- [aws/aws-cli](https://github.com/aws/aws-cli) — official CLI
- [aws-actions/configure-aws-credentials](https://github.com/aws-actions/configure-aws-credentials) — OIDC auth from GitHub Actions to AWS
- [awslabs/nx-plugin-for-aws](https://github.com/awslabs/nx-plugin-for-aws) — Nx monorepo plugin for AWS

### Curated awesome lists & community indexes

- [donnemartin/awesome-aws](https://github.com/donnemartin/awesome-aws) — the original, encyclopedic
- [open-guides/og-aws](https://github.com/open-guides/og-aws) — opinionated practitioner's guide (huge inspiration for this repo)
- [dabit3/awesome-aws-amplify](https://github.com/dabit3/awesome-aws-amplify) — Amplify-focused
- [iann0036/AWSConsoleRecorder](https://github.com/iann0036/AWSConsoleRecorder) — record console actions as IaC
- [punkpeye/awesome-mcp-servers](#claude-code-agent-plugins-skills-for-aws) — cross-vendor MCP catalog (incl. AWS)

---

## Contributing

If something here saved you a search, pay it forward: add a link, fix a 404, or tighten a playbook. [CONTRIBUTING.md](CONTRIBUTING.md) has the full editorial rules. For **merge checklists, CI gates, and ops cadence**, see the [production readiness plan](PRODUCTION_READINESS.md).

**Quick rules:**

1. One link per line: `[Name](URL) — short description` (use an em dash between title and description).
2. Prefer resources that are maintained and AWS-relevant; drop dead repos and stale docs.
3. Open an issue before adding a new top-level category so maintainers can align on scope.
4. Self-promotional links are allowed when the resource is useful; say how you are connected in the PR description.

| Action | Link |
|---|---|
| 💡 Suggest a resource | [Open a "New Resource" issue](https://github.com/palpalani/aws-open-guide/issues/new?template=new-resource.yml) |
| 🔗 Report a broken link | [Open a "Broken Link" issue](https://github.com/palpalani/aws-open-guide/issues/new?template=broken-link.yml) |
| ⭐ Show appreciation | [Star the repo](https://github.com/palpalani/aws-open-guide) — helps others discover it |

---

## Need Implementation Help?

Everything in this repo is free to read and reuse under the license below. When you need someone to review a design, run a cost pass, or own a migration on a timeline, the maintainer works with teams through [FactualMinds](https://www.factualminds.com/). Entry points below.

- [Free AWS Cost Audit](https://www.factualminds.com/aws-cost-audit/)
- [AWS Migration Services](https://www.factualminds.com/services/aws-migration/)
- [AWS Cost Optimization & FinOps](https://www.factualminds.com/services/aws-cloud-cost-optimization-services/)
- [AWS Cloud Security](https://www.factualminds.com/services/aws-cloud-security/)
- [Generative AI on AWS](https://www.factualminds.com/services/generative-ai-on-aws/)
- [AWS Managed Services](https://www.factualminds.com/services/aws-managed-services/)
- [Hire a Dedicated AWS Expert](https://www.factualminds.com/services/hire-a-dedicated-aws-expert/)
- [Browse all 25+ services →](https://www.factualminds.com/services/)

---

## License

<div align="center">

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg?style=for-the-badge)](https://creativecommons.org/licenses/by/4.0/)

This work is licensed under **[Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/)**.

You're free to share and adapt the material for any purpose, even commercially, as long as you give appropriate credit.

---

<sub>Built with care by <a href="https://github.com/palpalani">Palaniappan P</a> · If this guide saved you time, <a href="https://github.com/palpalani/aws-open-guide">⭐ star the repo</a></sub>

</div>
