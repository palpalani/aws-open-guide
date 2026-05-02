<div align="center">

# ☁️ AWS Open Guide

### A curated, opinionated map of Amazon Web Services

**Services · official docs · production deep-dives · OSS tools · battle-tested references — organized by AWS's own service taxonomy.**

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg?style=flat-square)](https://creativecommons.org/licenses/by/4.0/)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat-square)](CONTRIBUTING.md)
[![GitHub stars](https://img.shields.io/github/stars/palpalani/aws-open-guide?style=flat-square&logo=github)](https://github.com/palpalani/aws-open-guide/stargazers)
[![GitHub last commit](https://img.shields.io/github/last-commit/palpalani/aws-open-guide?style=flat-square&logo=github)](https://github.com/palpalani/aws-open-guide/commits)
[![GitHub issues](https://img.shields.io/github/issues/palpalani/aws-open-guide?style=flat-square&logo=github)](https://github.com/palpalani/aws-open-guide/issues)

[**🚀 Get Started**](#how-to-use-this-guide) ·
[**🎯 Use-Case Playbooks**](#use-case-playbooks) ·
[**🧭 Browse Services**](#table-of-contents) ·
[**⚖️ Decision Guides**](#decision-guides--x-vs-y) ·
[**💰 Cost & FinOps**](#cost-management--finops) ·
[**🤖 AI & MCP**](#ai-coding-agents-mcp--skills) ·
[**🤝 Contribute**](CONTRIBUTING.md)

<sub>Maintained by <a href="https://github.com/palpalani">Palaniappan P</a> · Updated continuously</sub>

</div>

---

## Why this guide?

The AWS console has **200+ services**. The official docs are exhaustive but fragmented across hundreds of microsites. This guide cuts through the noise:

| | |
|---|---|
| 🗂️ **Canonical taxonomy** | Organized the way AWS thinks — Compute, Storage, Database, Networking — not by tool category. |
| 📚 **Three-tier resources per service** | Official docs first, then in-depth production guides, then OSS tools. |
| ⚠️ **Real cost & gotcha callouts** | Limits, surprise-bill traps, and migration pain points the brochure won't mention. |
| ⚖️ **Decision-first** | Every "X vs Y" question gets a comparison link. |
| ⏳ **Lifecycle-aware** | Flags services in maintenance, sunset, or full shutdown so you don't anchor on dead AWS products. |
| 🤖 **AI-native** | First-class coverage of MCP servers, agent plugins, and Claude Code skills for AWS. |

> [!TIP]
> If a category here is empty or thin, [contributions are warmly welcomed](CONTRIBUTING.md). One link per line, em-dash separator — see [CONTRIBUTING.md](CONTRIBUTING.md) for the full format.

## How to use this guide

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

The service taxonomy below is the **reference layer** ("what links exist about S3"). Playbooks are the **building layer** ("how do I build X on AWS in production"). Each playbook follows a strict 11-section template — see [`use-cases/_template.md`](use-cases/_template.md).

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

**Cross-cutting frameworks** (referenced by every playbook):

- 🌳 [Decision trees](use-cases/decision-trees.md) — which AWS service for event processing, database, compute, async work, file processing
- 🛡️ [Failure-first patterns](use-cases/failure-first.md) — retries, idempotency, DLQs, regional failover, backpressure, circuit breakers
- 🚫 [Anti-patterns](use-cases/anti-patterns.md) — the mistakes that show up across every workload, with the better pattern
- 💸 [Cost pitfalls](use-cases/cost-pitfalls.md) — line items that surprise teams (NAT Gateway, cross-AZ, CloudWatch Logs, egress)

> [!TIP]
> Browse all playbooks at [`use-cases/`](use-cases/). Want to add one? Copy [`_template.md`](use-cases/_template.md) and follow the [contribution guide](CONTRIBUTING.md#adding-a-use-case-playbook).

<details>
<summary><strong>📑 Table of Contents</strong> — click to expand</summary>

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
- [Decision trees](use-cases/decision-trees.md)
- [Failure-first patterns](use-cases/failure-first.md)
- [Anti-patterns](use-cases/anti-patterns.md)
- [Cost pitfalls](use-cases/cost-pitfalls.md)

### 🟧 Core AWS services

- [📖 How to use this guide](#how-to-use-this-guide)
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
- [AWS Well-Architected Framework — 6 pillars explained](https://www.factualminds.com/blog/aws-well-architected-framework-6-pillars-explained/)
- [AWS Shared Responsibility Model](https://www.factualminds.com/glossary/aws-shared-responsibility-model/) — what AWS secures vs what you secure
- [Microservices vs monolith on AWS — architecture decision guide](https://www.factualminds.com/blog/microservices-vs-monolith-on-aws-architecture-decision-guide/)
- [Top 20 modern AWS AI services — overview](https://www.factualminds.com/blog/top-20-aws-ai-modern-services-2026/)

**Recent AWS Service Announcements (changelog-style):**
- [March 2026 announcements](https://www.factualminds.com/blog/aws-service-announcements-march-2026/)
- [May 2026 announcements](https://www.factualminds.com/blog/aws-service-announcements-may-2026/)

**Architecture Deep Reading (essential AWS canon):**
- [AWS Architecture Center](https://aws.amazon.com/architecture/) — start here for high-level mental model
- [AWS Builders Library](https://aws.amazon.com/builders-library/) — operations + resilience essays from AWS principal engineers
- [Static Stability Using Availability Zones](https://aws.amazon.com/builders-library/static-stability-using-availability-zones/) — Builders Library essay on designing for failure
- [Multi-Tier Architectures on AWS (whitepaper)](https://docs.aws.amazon.com/whitepapers/latest/overview-deployment-options/multi-tier-architectures.html)
- [AWS Multi-Region Fundamentals (whitepaper)](https://docs.aws.amazon.com/whitepapers/latest/aws-multi-region-fundamentals/aws-multi-region-fundamentals.html) — active-active patterns

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

**Production Guides:**
- [EC2 high-performance API optimization](https://www.factualminds.com/blog/ec2-high-performance-api-optimization/)
- [EC2 Spot Instance intelligent selection for cost optimization](https://www.factualminds.com/blog/ec2-spot-instance-intelligent-selection-cost-optimization/)
- [Hybrid compute — EC2 + serverless cost efficiency](https://www.factualminds.com/blog/hybrid-compute-ec2-serverless-cost-efficiency/)
- [Auto-scaling strategies for EC2, ECS, Lambda](https://www.factualminds.com/blog/aws-auto-scaling-strategies-ec2-ecs-lambda/)
- [Amazon EC2 — glossary entry](https://www.factualminds.com/glossary/amazon-ec2/)

**Decision Guides:**
- [Which AWS compute should I use?](https://www.factualminds.com/decide/which-aws-compute/)
- [EC2 vs Lambda — when to use which](https://www.factualminds.com/compare/aws-ec2-vs-lambda/)

**OSS Tools:**
- [99designs/aws-vault](https://github.com/99designs/aws-vault) — secure storage of AWS credentials on developer laptops
- [AutoSpotting/AutoSpotting](https://github.com/AutoSpotting/AutoSpotting) — automatically replace on-demand EC2 in ASGs with spot instances

### AWS Graviton — Arm-based processors

> Custom Arm chips with 40% better price/performance than x86 on most workloads.

- [Graviton overview](https://aws.amazon.com/ec2/graviton/)
- [Graviton cost optimization guide](https://www.factualminds.com/blog/aws-graviton-cost-optimization-guide/) — m5.large → t4g.medium real savings

### AWS Trainium & Inferentia — ML accelerators

> Purpose-built chips for training (Trainium) and inference (Inferentia).

- [Trainium](https://aws.amazon.com/ai/machine-learning/trainium/) · [Inferentia](https://aws.amazon.com/ai/machine-learning/inferentia/)
- [Trainium2 + Inferentia2 deep dive](https://www.factualminds.com/blog/aws-trainium2-inferentia2-ai-chips/)

### AWS Batch

- [Batch documentation](https://docs.aws.amazon.com/batch/)

### AWS Lightsail

> Simple VPS pricing for predictable workloads.
- [Lightsail](https://aws.amazon.com/lightsail/)

### AWS App Runner

> Fully managed container service for web apps and APIs.
- [App Runner](https://aws.amazon.com/apprunner/)

### Amazon Elastic VMware Service (EVS)

- [EVS deep dive](https://www.factualminds.com/blog/amazon-elastic-vmware-service-evs/) — VMware workloads on AWS

### AWS Outposts

> AWS-managed hardware in your own data centre. Use for low-latency, data-residency, or hybrid workloads that must stay on-prem.

- [Outposts](https://aws.amazon.com/outposts/)
- [Outposts FAQs](https://aws.amazon.com/outposts/faqs/)

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

**Production Guides:**
- [Production Laravel/Django/Node on ECS](https://www.factualminds.com/blog/production-laravel-django-node-on-ecs-2026/)
- [How to migrate a monolith to ECS Fargate with zero downtime](https://www.factualminds.com/blog/how-to-migrate-monolith-ecs-fargate-zero-downtime/)
- [Blue-green deployments with ECS + CodeDeploy](https://www.factualminds.com/blog/how-to-implement-blue-green-deployments-ecs-codedeploy/)
- [Modernizing monolithic APIs with Amazon ECS — case study](https://www.factualminds.com/case-study/microservices-on-amazon-ecs/)

### Amazon EKS — Elastic Kubernetes Service

> Managed Kubernetes. Use when you need K8s portability or have existing K8s expertise.

> 🎯 **Building multi-tenant SaaS on EKS?** See the [Multi-tenant SaaS playbook](use-cases/multi-tenant-saas.md) — silo / pool / bridge isolation models with per-tenant cost attribution and noisy-neighbour controls.

**Official:**
- [EKS Documentation](https://docs.aws.amazon.com/eks/)
- [EKS Best Practices Guides](https://aws.github.io/aws-eks-best-practices/)

**Production Guides:**
- [Deploy EKS with Karpenter for cost-optimized autoscaling](https://www.factualminds.com/blog/how-to-deploy-eks-karpenter-cost-optimized-autoscaling/)
- [Karpenter vs Cluster Autoscaler — EKS cost optimization](https://www.factualminds.com/blog/karpenter-vs-cluster-autoscaler-eks-cost-optimization/)
- [Host n8n on AWS EKS — production guide](https://www.factualminds.com/blog/how-to-host-n8n-on-aws-eks-production-guide/)
- [Amazon EKS — glossary entry](https://www.factualminds.com/glossary/amazon-eks/)

**Tools:**
- [Karpenter](https://karpenter.sh/) — node autoscaling for EKS
- [eksctl](https://eksctl.io/) — official CLI for EKS

### AWS Fargate

> Serverless compute for containers. Pay per task, not per VM.
- [Fargate](https://aws.amazon.com/fargate/)
- [Lambda vs ECS Fargate — when to use which](https://www.factualminds.com/compare/aws-lambda-vs-ecs-fargate/)

### Amazon ECR — Elastic Container Registry

> Private Docker/OCI registry, integrated with IAM and image scanning.
- [ECR Documentation](https://docs.aws.amazon.com/ecr/)

### Finch — open-source container client

> AWS-built local Docker alternative — `nerdctl` + `containerd` + `Lima` packaged for macOS/Linux/Windows. Drop-in replacement for `docker build/run/push`.

- [Finch](https://runfinch.com/)
- [runfinch/finch](https://github.com/runfinch/finch) — open-source repo

### Decision

- [ECS vs EKS — container orchestration decision guide](https://www.factualminds.com/blog/aws-ecs-vs-eks-container-orchestration-decision-guide/) · [Compare](https://www.factualminds.com/compare/aws-ecs-vs-eks/)
- [Kubernetes on AWS EKS — integration guide](https://www.factualminds.com/integrations/kubernetes-aws-eks/)

---

## Serverless

Run code without managing servers.

### AWS Lambda

> Event-driven function-as-a-service. The default for sporadic, async, glue-code workloads.

> 🎯 **Building with Lambda in production?** See [Async job processing](use-cases/async-jobs.md) (queue + worker), [High-scale API backend](use-cases/high-scale-api.md) (caching + rate limits), and [Event-driven processing](use-cases/event-driven.md) (EventBridge + DLQs).

**Official:**
- [Lambda Documentation](https://docs.aws.amazon.com/lambda/)
- [Lambda Pricing](https://aws.amazon.com/lambda/pricing/)
- [Lambda Powertools (Python/TypeScript/Java)](https://docs.powertools.aws.dev/)
- [Lambda invocation, scaling and concurrency (official docs)](https://docs.aws.amazon.com/lambda/latest/dg/invocation-scaling.html)
- [AWS Lambda blog category (Compute Blog)](https://aws.amazon.com/blogs/compute/category/aws-lambda/) — patterns, deep dives, releases

**Production Guides:**
- [Lambda cost optimization — pay-per-request vs provisioned](https://www.factualminds.com/blog/aws-lambda-cost-optimization-pay-per-request-vs-provisioned/)
- [AWS Lambda — glossary entry](https://www.factualminds.com/glossary/aws-lambda/)
- [Going Serverless at Scale — Adrian Cockcroft (re:Invent talk)](https://www.youtube.com/watch?v=EBSdyoO3goc)

**Comparisons:**
- [Lambda vs container cost calculator](https://www.factualminds.com/tools/aws-lambda-vs-container-cost-calculator/)

### AWS Step Functions

> Visual workflow orchestrator for distributed apps.
- [Step Functions Documentation](https://docs.aws.amazon.com/step-functions/)
- [Step Functions workflow orchestration patterns](https://www.factualminds.com/blog/aws-step-functions-workflow-orchestration-patterns/)
- [AWS Step Functions — glossary entry](https://www.factualminds.com/glossary/aws-step-functions/)
- [Step Functions vs EventBridge](https://www.factualminds.com/compare/aws-step-functions-vs-eventbridge/)
- [Bedrock Agents vs Step Functions](https://www.factualminds.com/compare/aws-bedrock-agents-vs-step-functions/)

### Amazon EventBridge

> Serverless event bus for SaaS, AWS services, and custom events.
- [EventBridge Documentation](https://docs.aws.amazon.com/eventbridge/)
- [EventBridge event-driven architecture patterns](https://www.factualminds.com/blog/aws-eventbridge-event-driven-architecture-patterns/)
- [AWS Event-Driven Architecture (overview)](https://aws.amazon.com/event-driven-architecture/) — official intro, services, patterns
- [AWS Event-Driven Architecture (architecture overview)](https://aws.amazon.com/event-driven-architecture/) — patterns and reference architectures

### AWS SAM & Serverless Framework

- [AWS SAM (Serverless Application Model)](https://aws.amazon.com/serverless/sam/)
- [Serverless Framework](https://www.serverless.com/)

### OSS Lambda Frameworks (community)

- [aws/chalice](https://github.com/aws/chalice) — Python serverless microframework (official AWS, Flask-style)
- [zappa/Zappa](https://github.com/zappa/Zappa) — serverless WSGI Python on Lambda + API Gateway (Django, Flask)
- [claudiajs/claudia](https://github.com/claudiajs/claudia) — deploy Node.js projects to Lambda + API Gateway with one command
- [jeremydaly/lambda-api](https://github.com/jeremydaly/lambda-api) — lightweight web framework for serverless Node.js
- [awslabs/aws-lambda-web-adapter](https://github.com/awslabs/aws-lambda-web-adapter) — run any HTTP web app (Express, Flask, FastAPI, Next.js) on Lambda unmodified
- [getmoto/moto](https://github.com/getmoto/moto) — mock AWS services for unit/integration tests (also useful beyond Lambda)

### Local Lambda Dev

- [AWS SAM CLI — `sam local`](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-cli-command-reference-sam-local.html) — invoke Lambda + API Gateway locally
- [aws/aws-lambda-runtime-interface-emulator](https://github.com/aws/aws-lambda-runtime-interface-emulator) — `aws-lambda-rie` — run Lambda container images locally with `docker run`

**Other Serverless Patterns:**
- [Scaling EdTech platforms on AWS serverless architecture](https://www.factualminds.com/blog/scaling-edtech-platforms-on-aws-serverless-architecture/)

---

## Storage

### Amazon S3 — Simple Storage Service

> Object storage. 11 9's durability. The default landing pad for files in AWS.

> 🎯 **Handling user file uploads?** See the [File upload and processing playbook](use-cases/file-upload.md) — pre-signed URLs, malware scan, MIME sniffing, async transform pipeline, lifecycle policies.

**Official:**
- [S3 Documentation](https://docs.aws.amazon.com/s3/)
- [S3 Pricing](https://aws.amazon.com/s3/pricing/)
- [S3 Storage Classes](https://aws.amazon.com/s3/storage-classes/)

**Production Guides:**
- [S3 security best practices — preventing data exposure](https://www.factualminds.com/blog/aws-s3-security-best-practices-preventing-data-exposure/)
- [S3 storage costs aren't actually cheap](https://www.factualminds.com/blog/aws-s3-storage-costs-not-cheap/) — real teardown
- [Building a data lake on S3 + Glue + Athena](https://www.factualminds.com/blog/building-a-data-lake-on-aws-s3-glue-athena-architecture/)
- [Amazon S3 — glossary entry](https://www.factualminds.com/glossary/amazon-s3/)

**Tools:**
- [s3cmd](https://github.com/s3tools/s3cmd) — full-featured CLI
- [Mountpoint for Amazon S3](https://github.com/awslabs/mountpoint-s3) — official FUSE mount
- [s5cmd](https://github.com/peak/s5cmd) — fastest S3 CLI
- [s3fs-fuse](https://github.com/s3fs-fuse/s3fs-fuse) — community FUSE-based S3 mount (Linux + macOS)
- [goofys](https://github.com/kahing/goofys) — S3 file system in Go, optimized for read throughput
- [MinIO](https://github.com/minio/minio) — self-hosted S3-compatible object storage (good for hybrid + dev/test)
- [MinIO `mc` client](https://github.com/minio/mc) — S3-compatible CLI (works with S3 + MinIO)
- [rclone](https://github.com/rclone/rclone) — rsync for S3 + 70+ other cloud storage backends

> [!WARNING]
> **Gotchas:**
> - Bucket names are globally unique across all AWS accounts.
> - Default encryption (SSE-S3) is now ON for all new buckets — was opt-in pre-2023.
> - Cross-region replication does NOT replicate delete markers by default.

### Amazon S3 Vectors

> Native vector storage in S3 — purpose-built for RAG and AI workloads.
- [S3 Vectors deep dive](https://www.factualminds.com/blog/amazon-s3-vectors-native-vector-storage/)

### Amazon EBS — Elastic Block Store

- [EBS Documentation](https://docs.aws.amazon.com/ebs/)
- [EBS encryption + snapshot hygiene + KMS lifecycle](https://www.factualminds.com/blog/aws-ebs-encryption-snapshot-hygiene-kms-lifecycle/)

### Amazon EFS — Elastic File System

- [EFS Documentation](https://docs.aws.amazon.com/efs/)

### Amazon FSx

- [FSx](https://aws.amazon.com/fsx/) — managed Windows, Lustre, NetApp ONTAP, OpenZFS

### AWS Backup

> Centralized backup service across AWS resources.
- [AWS Backup](https://aws.amazon.com/backup/)
- [AWS backup strategies — automated data protection](https://www.factualminds.com/blog/aws-backup-strategies-automated-data-protection/)

### AWS Storage Gateway

- [Storage Gateway](https://aws.amazon.com/storagegateway/)

---

## Databases

### Amazon RDS — Relational Database Service

> Managed Postgres, MySQL, MariaDB, Oracle, SQL Server.

**Official:**
- [RDS Documentation](https://docs.aws.amazon.com/rds/)
- [RDS Pricing](https://aws.amazon.com/rds/pricing/)

**Production Guides:**
- [RDS database performance best practices](https://www.factualminds.com/blog/aws-rds-database-performance-best-practices/)
- [RDS vs Aurora — when to use which database](https://www.factualminds.com/blog/aws-rds-vs-aurora-when-to-use-which-database/) · [Compare](https://www.factualminds.com/compare/aws-rds-vs-aurora/)
- [RDS max connection calculator](https://www.factualminds.com/tools/aws-rds-max-connection-calculator/)
- [High-scale Postgres on AWS — cost optimization](https://www.factualminds.com/blog/high-scale-postgres-aws-cost-optimization/)
- [Amazon RDS — glossary entry](https://www.factualminds.com/glossary/amazon-rds/)

### Amazon Aurora

> AWS-built relational DB. Postgres/MySQL-compatible, 5x performance of stock MySQL.

- [Aurora Documentation](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/CHAP_AuroraOverview.html)
- [Aurora Limitless Database](https://www.factualminds.com/blog/amazon-aurora-limitless-database/) — horizontal scaling
- [Aurora Serverless v2 vs Aurora provisioned](https://www.factualminds.com/compare/aws-aurora-serverless-vs-aurora-provisioned/)
- [Amazon Aurora — glossary entry](https://www.factualminds.com/glossary/amazon-aurora/)

### Amazon DynamoDB

> Single-digit millisecond NoSQL key-value + document store.

- [DynamoDB Documentation](https://docs.aws.amazon.com/dynamodb/)
- [DynamoDB best practices (official)](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/best-practices.html) — partition keys, indexes, scaling
- [DynamoDB single-table design — Alex DeBrie](https://www.alexdebrie.com/posts/dynamodb-single-table/) — canonical reading
- [Advanced design patterns for DynamoDB — Rick Houlihan (re:Invent talk)](https://www.youtube.com/watch?v=HaEPXoXVf2k)
- [DynamoDB single-table design patterns for SaaS](https://www.factualminds.com/blog/dynamodb-single-table-design-patterns-for-saas/)
- [Amazon DynamoDB — glossary entry](https://www.factualminds.com/glossary/amazon-dynamodb/)
- [DynamoDB vs RDS](https://www.factualminds.com/compare/dynamodb-vs-rds/)

**OSS Tools:**
- [sensedeep/dynamodb-onetable](https://github.com/sensedeep/dynamodb-onetable) — Node.js library for single-table designs
- [jeremydaly/dynamodb-toolbox](https://github.com/jeremydaly/dynamodb-toolbox) — Jeremy Daly's TypeScript library for single-table modeling

### Amazon Redshift

> Petabyte-scale data warehouse.

- [Redshift Documentation](https://docs.aws.amazon.com/redshift/)
- [Redshift Serverless vs Provisioned — when to use each](https://www.factualminds.com/blog/amazon-redshift-serverless-vs-provisioned-when-to-use-each/)
- [Amazon Redshift — glossary entry](https://www.factualminds.com/glossary/amazon-redshift/)

### Amazon ElastiCache

> Managed Redis & Memcached.
- [ElastiCache Documentation](https://docs.aws.amazon.com/elasticache/)
- [ElastiCache Redis caching strategies for production](https://www.factualminds.com/blog/aws-elasticache-redis-caching-strategies-for-production/)
- [Redis-Valkey cost-saving layer on AWS](https://www.factualminds.com/blog/redis-valkey-cost-saving-layer-aws/)

### Amazon MemoryDB for Redis

- [MemoryDB](https://aws.amazon.com/memorydb/)
- [MemoryDB vector search](https://www.factualminds.com/blog/amazon-memorydb-vector-search/)

### Amazon DocumentDB

- [DocumentDB](https://aws.amazon.com/documentdb/) — MongoDB-compatible
- [Migrate from MongoDB Atlas to DocumentDB](https://www.factualminds.com/compare/mongodb-atlas-to-documentdb/)
- [MongoDB scalable, cost-efficient on AWS](https://www.factualminds.com/blog/mongodb-scalable-cost-efficient-aws/)

### Amazon Neptune

- [Neptune](https://aws.amazon.com/neptune/) — graph database
- [Neptune Analytics — graph + vector](https://www.factualminds.com/blog/amazon-neptune-analytics-graph-vector/)

### Amazon Timestream

- [Timestream](https://aws.amazon.com/timestream/) — time-series; LiveAnalytics closed to new customers June 20, 2025

### Decision Guides

- [Which AWS database should I use?](https://www.factualminds.com/decide/which-aws-database/)
- [Heroku Postgres → AWS RDS](https://www.factualminds.com/compare/heroku-postgres-to-aws-rds/)

---

## Networking & Content Delivery

### Amazon VPC — Virtual Private Cloud

- [VPC Documentation](https://docs.aws.amazon.com/vpc/)
- [VPC networking best practices for production](https://www.factualminds.com/blog/aws-vpc-networking-best-practices-for-production/)
- [VPC peering vs Transit Gateway](https://www.factualminds.com/glossary/vpc-peering-vs-transit-gateway/)
- [Amazon VPC — glossary entry](https://www.factualminds.com/glossary/amazon-vpc/)

### NAT Gateway

- [NAT Gateway billing — idle cost alternatives](https://www.factualminds.com/blog/aws-nat-gateway-billing-idle-cost-alternatives/) — bill teardown
- [Bill teardown — healthcare's NAT Gateway problem](https://www.factualminds.com/blog/aws-bill-teardown-2-healthcare-nat-gateway-problem/)

### Amazon Route 53

- [Route 53](https://aws.amazon.com/route53/) — DNS + traffic management
- [Route 53 DNS traffic management patterns](https://www.factualminds.com/blog/aws-route-53-dns-traffic-management-patterns/)

### Amazon CloudFront

> Global CDN with 600+ edge locations.

- [CloudFront Documentation](https://docs.aws.amazon.com/cloudfront/)
- [CloudFront vs Cloudflare — which CDN for your enterprise](https://www.factualminds.com/blog/aws-cloudfront-vs-cloudflare-which-cdn-for-your-enterprise/) · [Compare](https://www.factualminds.com/compare/aws-cloudfront-vs-cloudflare/)
- [Image optimization + CloudFront — case study](https://www.factualminds.com/case-study/image-optimization-cloudfront/)
- [Automated image pipeline + CloudFront — 30% cost reduction](https://www.factualminds.com/case-study/cloudfront/)
- [AWS CloudFront Consulting](https://www.factualminds.com/services/aws-cloudfront-consultant/)

### Amazon API Gateway

> 🎯 **Building a high-traffic API?** See the [High-scale API backend playbook](use-cases/high-scale-api.md) — CloudFront + WAF + API Gateway with caching, rate limits, and graceful degradation under load.

- [API Gateway Documentation](https://docs.aws.amazon.com/apigateway/)
- [API Gateway patterns — REST, HTTP, WebSocket](https://www.factualminds.com/blog/aws-api-gateway-patterns-rest-http-websocket/)

### AWS Verified Access

- [Verified Access — ZTNA zero-trust network](https://www.factualminds.com/blog/aws-verified-access-ztna-zero-trust-network/)

### AWS Direct Connect / Transit Gateway / Global Accelerator

- [Direct Connect](https://aws.amazon.com/directconnect/) · [Transit Gateway](https://aws.amazon.com/transit-gateway/) · [Global Accelerator](https://aws.amazon.com/global-accelerator/)

---

## Security & Identity

### AWS IAM — Identity & Access Management

- [IAM Documentation](https://docs.aws.amazon.com/iam/)
- [IAM best practices — least-privilege access control](https://www.factualminds.com/blog/aws-iam-best-practices-least-privilege-access-control/)
- [AWS IAM — glossary entry](https://www.factualminds.com/glossary/aws-iam/)

### AWS IAM Identity Center (formerly SSO)

- [IAM Identity Center workforce SSO + identity propagation](https://www.factualminds.com/blog/aws-iam-identity-center-workforce-sso-identity-propagation/)
- [IAM Identity Center vs Cognito](https://www.factualminds.com/compare/aws-iam-identity-center-vs-cognito/)

### Amazon Cognito

- [Cognito](https://aws.amazon.com/cognito/) — user identity for apps
- [Cognito authentication for SaaS applications](https://www.factualminds.com/blog/aws-cognito-authentication-for-saas-applications/)

### AWS KMS — Key Management Service

- [KMS Documentation](https://docs.aws.amazon.com/kms/)
- [KMS post-quantum cryptography — ML-KEM, ML-DSA](https://www.factualminds.com/blog/aws-kms-post-quantum-cryptography-ml-kem-ml-dsa/)
- [AWS KMS — glossary entry](https://www.factualminds.com/glossary/aws-kms/)

### Amazon GuardDuty

> Managed threat detection across AWS accounts.
- [GuardDuty](https://aws.amazon.com/guardduty/)
- [GuardDuty threat detection production guide](https://www.factualminds.com/blog/aws-guardduty-threat-detection-production-guide/)
- [GuardDuty vs Security Hub](https://www.factualminds.com/compare/aws-guardduty-vs-security-hub/)

### AWS Security Hub

- [Security Hub](https://aws.amazon.com/security-hub/)
- [Security Hub compliance monitoring setup](https://www.factualminds.com/blog/how-to-set-up-aws-security-hub-compliance-monitoring/)

### AWS WAF — Web Application Firewall

- [WAF Documentation](https://docs.aws.amazon.com/waf/)
- [WAF web application firewall production guide](https://www.factualminds.com/blog/aws-waf-web-application-firewall-production-guide/)
- [WAF API protection beyond basics](https://www.factualminds.com/blog/how-to-configure-aws-waf-api-protection-beyond-basics/)
- [WAF vs Network Firewall](https://www.factualminds.com/compare/aws-waf-vs-network-firewall/)
- [WAF case study — 99% threat blocking for eLearning](https://www.factualminds.com/case-study/aws-waf-security/)
- [WAF case study — DDoS mitigation for BI](https://www.factualminds.com/case-study/aws-waf-ddos-protection-analytics/)
- [WAF case study — PCI compliance for eCommerce](https://www.factualminds.com/case-study/aws-waf-pci-compliance/)

### Amazon Inspector

- [Inspector v2 — container + Lambda scanning](https://www.factualminds.com/blog/amazon-inspector-v2-container-lambda/)

### Amazon Macie & Detective

- [Macie + Detective — data security investigation](https://www.factualminds.com/blog/aws-macie-detective-data-security-investigation/)

### AWS Network Firewall & Firewall Manager

- [Network Firewall + Firewall Manager — multi-account](https://www.factualminds.com/blog/aws-network-firewall-firewall-manager-multi-account/)

### AWS Secrets Manager / Parameter Store

- [Secrets Manager](https://aws.amazon.com/secrets-manager/) · [Parameter Store](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html)
- [Secrets Manager vs Parameter Store — when to use which](https://www.factualminds.com/blog/aws-secrets-manager-vs-parameter-store-when-to-use-which/)

### AWS CloudTrail

- [CloudTrail Documentation](https://docs.aws.amazon.com/cloudtrail/)
- [CloudTrail production setup — multi-region + validation + Lake](https://www.factualminds.com/blog/aws-cloudtrail-production-setup-multi-region-validation-lake/)
- [AWS CloudTrail — glossary entry](https://www.factualminds.com/glossary/aws-cloudtrail/)

### Amazon Verified Permissions (Cedar)

- [Verified Permissions + Cedar policy language](https://www.factualminds.com/blog/amazon-verified-permissions-cedar/)

### Amazon Security Lake

- [Security Lake — OCSF schema](https://www.factualminds.com/blog/amazon-security-lake-ocsf/)

### AWS Shared Responsibility Model

- [Shared Responsibility Model — glossary entry](https://www.factualminds.com/glossary/aws-shared-responsibility-model/)

### Holistic Security Guides

- [10 AWS cloud security best practices](https://www.factualminds.com/blog/10-aws-cloud-security-best-practices-implementation-guide/)
- [Securing AWS workloads beyond the basics](https://www.factualminds.com/blog/securing-aws-workloads-beyond-the-basics/)
- [From reactive to proactive — automating AWS security remediation](https://www.factualminds.com/blog/from-reactive-to-proactive-automating-aws-security-remediation/)
- [AWS resource hardening quick wins (DMS, OpenSearch, SageMaker, Lambda)](https://www.factualminds.com/blog/aws-resource-hardening-quick-wins-dms-opensearch-sagemaker-lambda/)
- [AWS vulnerability management program — CVSS + KEV prioritization](https://www.factualminds.com/blog/aws-vulnerability-management-program-cvss-kev-prioritization/)
- [Protect AWS infrastructure from cost-based attacks](https://www.factualminds.com/blog/protect-aws-infrastructure-cost-based-attacks/)
- [Security & Compliance hub](https://www.factualminds.com/security-compliance/)

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
- [policy_sentry](https://github.com/salesforce/policy_sentry) — Salesforce IAM least-privilege policy generator
- [algo](https://github.com/trailofbits/algo) — Trail of Bits one-click personal IPSEC VPN on EC2 (and other clouds)

---

## Compliance

### HIPAA

- [HIPAA Eligible AWS Services](https://aws.amazon.com/compliance/hipaa-eligible-services-reference/)
- [HIPAA on AWS — complete compliance checklist](https://www.factualminds.com/blog/hipaa-on-aws-complete-compliance-checklist/)
- [HIPAA-compliant architecture on AWS](https://www.factualminds.com/blog/how-to-implement-hipaa-compliant-architecture-aws/)
- [HIPAA-compliant AI on AWS Bedrock](https://www.factualminds.com/blog/hipaa-compliant-ai-aws-bedrock/)
- [HIPAA telehealth platform — case study (8 weeks)](https://www.factualminds.com/case-study/hipaa-compliant-telehealth-platform-aws/)
- [HIPAA-eligible AWS services — glossary](https://www.factualminds.com/glossary/hipaa-eligible-aws-services/)
- [HIPAA compliance checker tool](https://www.factualminds.com/tools/hipaa-compliance-checker/)

### PCI DSS

- [PCI DSS compliance on AWS — fintech guide](https://www.factualminds.com/blog/pci-dss-compliance-aws-architecture-guide-fintech/)
- [PCI DSS fintech AWS migration — case study (12 weeks)](https://www.factualminds.com/case-study/pci-dss-fintech-aws-migration/)
- [PCI DSS Cardholder Data Environment — glossary](https://www.factualminds.com/glossary/pci-dss-cardholder-data-environment/)

### SOC 2

- [SOC 2 compliance on AWS — implementation guide](https://www.factualminds.com/blog/how-to-achieve-soc2-compliance-aws-2026/)
- [SOC 2 Type 2 — glossary](https://www.factualminds.com/glossary/soc2-type-2/)

### ISO 27001

- [ISO 27001 certification on AWS — ISMS implementation](https://www.factualminds.com/blog/iso-27001-certification-aws-isms-implementation/)

### GDPR

- [GDPR compliance on AWS for SaaS data protection](https://www.factualminds.com/blog/gdpr-compliance-aws-saas-data-protection/)

### NIS2

- [NIS2 directive — AWS for critical infrastructure](https://www.factualminds.com/blog/nis2-directive-aws-critical-infrastructure/)

### NIST CSF 2.0

- [NIST CSF 2.0 — AWS implementation guide](https://www.factualminds.com/blog/nist-csf-2-0-aws-implementation-guide/)

### DORA (Digital Operational Resilience Act)

- [DORA compliance — AWS for financial services](https://www.factualminds.com/blog/dora-compliance-aws-financial-services/)

### EU AI Act

- [EU AI Act compliance — AWS Bedrock + SageMaker](https://www.factualminds.com/blog/eu-ai-act-compliance-aws-bedrock-sagemaker/)

---

## Analytics & Big Data

> 🎯 **Building a real-time analytics pipeline?** See the [Real-time analytics playbook](use-cases/real-time-analytics.md) — Kinesis hot path + Firehose cold path → S3 + Athena, with cost model and partitioning patterns.

### Amazon Athena

> Serverless SQL on S3.
- [Athena Documentation](https://docs.aws.amazon.com/athena/)
- [Athena query cost optimization — partition, compress, cache, Iceberg](https://www.factualminds.com/blog/athena-query-cost-optimization-partition-compress-cache-iceberg/)

### AWS Glue

> Serverless ETL + data catalog.
- [Glue Documentation](https://docs.aws.amazon.com/glue/)
- [Glue 5 + Apache Iceberg — modern ETL](https://www.factualminds.com/blog/aws-glue-5-apache-iceberg-modern-etl/)
- [Glue vs dbt on AWS — data transformation guide](https://www.factualminds.com/blog/aws-glue-vs-dbt-on-aws-data-transformation-guide/)

### Amazon Kinesis

- [Kinesis Documentation](https://docs.aws.amazon.com/kinesis/)
- [Kinesis Data Streams vs MSK — which streaming platform](https://www.factualminds.com/blog/amazon-kinesis-data-streams-vs-msk-which-streaming-platform/)
- [Real-time data pipeline — Kinesis + Lambda + DynamoDB](https://www.factualminds.com/blog/real-time-data-pipeline-kinesis-lambda-dynamodb/)

### Amazon Managed Service for Apache Flink

- [Apache Flink on AWS — managed streaming analytics](https://www.factualminds.com/blog/apache-flink-on-aws-managed-service-streaming-analytics/)

### Amazon OpenSearch Service

- [OpenSearch Documentation](https://docs.aws.amazon.com/opensearch-service/)
- [OpenSearch architecture patterns + cost optimization](https://www.factualminds.com/blog/amazon-opensearch-service-architecture-patterns-cost-optimization/)

### Amazon EMR

- [EMR Serverless vs EC2 vs EKS — cost comparison](https://www.factualminds.com/blog/aws-emr-serverless-vs-ec2-vs-eks-cost-comparison/)

### Amazon QuickSight

> Serverless BI + ML insights + GenAI dashboards.
- [QuickSight Documentation](https://docs.aws.amazon.com/quicksight/)
- [QuickSight production guide + best practices](https://www.factualminds.com/blog/amazon-quicksight-production-guide-best-practices/)
- [QuickSight embedding analytics in SaaS apps](https://www.factualminds.com/blog/amazon-quicksight-embedding-analytics-saas-applications/)
- [QuickSight real-time analytics dashboards](https://www.factualminds.com/blog/aws-quicksight-real-time-analytics-dashboards-guide/)
- [Amazon Q in QuickSight — generative BI](https://www.factualminds.com/blog/amazon-q-quicksight-generative-bi/)
- [QuickSight + SPICE case study](https://www.factualminds.com/case-study/amazon-quicksight-spice/)
- [Amazon Q for QuickSight service](https://www.factualminds.com/services/amazon-q-for-quicksight/)

### Amazon DataZone

- [DataZone — enterprise governance](https://www.factualminds.com/blog/amazon-datazone-enterprise-governance/)

### AWS Clean Rooms

- [Clean Rooms — privacy-safe analytics](https://www.factualminds.com/blog/aws-clean-rooms-privacy-analytics/)

### Data Pipelines & Lakes

- [Building a data lake on S3 + Glue + Athena](https://www.factualminds.com/blog/building-a-data-lake-on-aws-s3-glue-athena-architecture/)
- [Build a serverless data pipeline — Glue + Athena](https://www.factualminds.com/blog/how-to-build-serverless-data-pipeline-glue-athena/)
- [AWS virtual data modeling guide](https://www.factualminds.com/blog/aws-virtual-data-modeling-guide/)
- [Snowflake on AWS — integration](https://www.factualminds.com/integrations/snowflake-aws/)

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

**Production Guides:**
- [Why Bedrock is the fastest path to enterprise GenAI](https://www.factualminds.com/blog/why-aws-bedrock-is-the-fastest-path-to-enterprise-genai/)
- [Bedrock cost optimization — token budgets + model selection](https://www.factualminds.com/blog/aws-bedrock-cost-optimization-token-budgets-model-selection/)
- [Bedrock Provisioned Throughput vs On-Demand — break-even analysis](https://www.factualminds.com/blog/aws-bedrock-provisioned-throughput-vs-on-demand-break-even-2026/)
- [Bedrock vs OpenAI API — enterprise comparison](https://www.factualminds.com/blog/aws-bedrock-vs-openai-api-enterprise/)
- [Build a Bedrock Agent with tool use](https://www.factualminds.com/blog/how-to-build-amazon-bedrock-agent-tool-use-2026/)
- [Build a RAG pipeline with Bedrock Knowledge Bases](https://www.factualminds.com/blog/how-to-build-rag-pipeline-amazon-bedrock-knowledge-bases/)
- [Set up Bedrock Guardrails in production](https://www.factualminds.com/blog/how-to-set-up-amazon-bedrock-guardrails-production/)
- [Implementing GenAI guardrails — secure AI governance](https://www.factualminds.com/blog/implementing-genai-guardrails-secure-ai-governance-aws/)
- [Bedrock AI agents + agentic workflows](https://www.factualminds.com/blog/aws-bedrock-ai-agents-agentic-workflows/)
- [Bedrock multi-agent supervisor pattern](https://www.factualminds.com/blog/aws-bedrock-multi-agent-supervisor-pattern/)
- [Bedrock OpenAI models, Codex, Managed Agents](https://www.factualminds.com/blog/amazon-bedrock-openai-models-codex-managed-agents/)
- [Bedrock AgentCore — production patterns](https://www.factualminds.com/blog/amazon-bedrock-agentcore-production/)
- [Bedrock Flows — workflow orchestration](https://www.factualminds.com/blog/amazon-bedrock-flows-workflow-orchestration/)
- [Bedrock Marketplace — third-party models](https://www.factualminds.com/blog/amazon-bedrock-marketplace-third-party-models/)
- [Bedrock Automated Reasoning Checks — hallucination prevention](https://www.factualminds.com/blog/amazon-bedrock-automated-reasoning-checks-hallucination-prevention/)
- [Bedrock Data Automation](https://www.factualminds.com/blog/amazon-bedrock-data-automation/)
- [Fine-tuning vs RAG on Bedrock — when to use each](https://www.factualminds.com/blog/fine-tuning-vs-rag-bedrock-when-to-use/)
- [Multi-tenant GenAI on Bedrock](https://www.factualminds.com/blog/multi-tenant-genai-bedrock/)
- [Bedrock Nova models guide](https://www.factualminds.com/blog/aws-bedrock-nova-models-guide/)
- [Amazon Bedrock — glossary entry](https://www.factualminds.com/glossary/amazon-bedrock/)
- [RAG pipeline — glossary entry](https://www.factualminds.com/glossary/rag-pipeline/)

### Amazon Bedrock AgentCore

> Managed runtime for production AI agents — sessions, memory, tool gateways, identity, and observability. The "everything around the agent" layer that Bedrock Agents alone doesn't give you.

**Official:**
- [Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [AgentCore documentation](https://docs.aws.amazon.com/bedrock-agentcore/)

**Production Guides:**
- [AgentCore production patterns](https://www.factualminds.com/blog/amazon-bedrock-agentcore-production/)

**OSS Tools:**
- [awslabs/agentcore-samples](https://github.com/awslabs/agentcore-samples) — official sample patterns
- [Amazon Bedrock AgentCore MCP Server](https://awslabs.github.io/mcp/servers/amazon-bedrock-agentcore-mcp-server) — build/deploy/manage agents from a coding agent

### Amazon Nova

> Amazon's foundation model family — text, multimodal (Canvas, Reel).

- [Nova Canvas + Reel — multimodal](https://www.factualminds.com/blog/amazon-nova-canvas-reel-multimodal/)

### Amazon SageMaker

> Build, train, deploy ML models at any scale.

**Official:**
- [SageMaker Documentation](https://docs.aws.amazon.com/sagemaker/)

**Production Guides:**
- [SageMaker Unified Studio](https://www.factualminds.com/blog/amazon-sagemaker-unified-studio/)
- [Run SageMaker training jobs cost-efficiently](https://www.factualminds.com/blog/how-to-run-sagemaker-training-jobs-cost-efficiently/)

**Decision Guides:**
- [Bedrock vs SageMaker](https://www.factualminds.com/compare/aws-bedrock-vs-sagemaker/)

### Amazon Q

> AI assistant family for developers, business users, and analytics.

**Official:**
- [Amazon Q for Business](https://aws.amazon.com/q/business/)

**Production Guides:**
- [Q for Business vs ChatGPT Enterprise — CTO guide](https://www.factualminds.com/blog/amazon-q-for-business-vs-chatgpt-enterprise-cto-guide/) · [Compare](https://www.factualminds.com/compare/amazon-q-vs-chatgpt-enterprise/)
- [Set up Q for Business with SharePoint + S3](https://www.factualminds.com/blog/how-to-set-up-amazon-q-for-business-sharepoint-s3/)
- [Q vs GitHub Copilot](https://www.factualminds.com/blog/amazon-q-vs-github-copilot-2026/)
- [Q for Business case study](https://www.factualminds.com/case-study/amazonq/)

### Kiro IDE

- [Kiro IDE — AWS agentic coding](https://www.factualminds.com/blog/kiro-ide-aws-agentic-coding/)

### Other AI/ML Services

- [Amazon Comprehend](https://aws.amazon.com/comprehend/) — NLP
- [Amazon Rekognition](https://aws.amazon.com/rekognition/) — image/video analysis
- [Amazon Textract](https://aws.amazon.com/textract/) — OCR + document AI
- [Amazon Polly](https://aws.amazon.com/polly/) — text-to-speech
- [Amazon Translate](https://aws.amazon.com/translate/) · [Amazon Transcribe](https://aws.amazon.com/transcribe/)

### Cost Control for AI

- [AWS autoscaling for AI workloads — avoid budget overrun](https://www.factualminds.com/blog/aws-autoscaling-ai-workloads-budget-overrun/)
- [Bedrock token cost calculator](https://www.factualminds.com/tools/aws-bedrock-token-cost-calculator/)

### Roundup

- [Top 20 modern AWS AI services — overview](https://www.factualminds.com/blog/top-20-aws-ai-modern-services-2026/)

---

## Developer Tools, DevOps & CI/CD

> 🎯 **Setting up CI/CD?** See the [CI/CD playbook](use-cases/ci-cd.md) — GitHub Actions + OIDC + per-environment accounts, with canary deploys, drift detection, and rollback runbook.

### AWS CloudFormation

> Native infrastructure-as-code in YAML/JSON.
- [CloudFormation Documentation](https://docs.aws.amazon.com/cloudformation/)
- [CloudFormation best practices — IaC](https://www.factualminds.com/blog/aws-cloudformation-best-practices-infrastructure-as-code/)
- [Application Composer — IaC generator](https://www.factualminds.com/blog/aws-application-composer-iac-generator/)

### AWS CDK — Cloud Development Kit

> Imperative IaC in TypeScript / Python / Java / Go / .NET.
- [CDK Documentation](https://docs.aws.amazon.com/cdk/)
- [Construct Hub](https://constructs.dev/) — community CDK constructs
- [Terraform vs AWS CDK — IaC decision guide](https://www.factualminds.com/blog/terraform-vs-aws-cdk-infrastructure-as-code-decision-guide/)

**OSS Tools:**
- [cdklabs/cdk-nag](https://github.com/cdklabs/cdk-nag) — checks CDK apps against AWS Solutions, HIPAA, NIST, PCI rule packs at synth time
- [projen/projen](https://github.com/projen/projen) — define and synthesise project configuration as code (CDK-style for repos)
- [aws-samples/aws-cdk-examples](https://github.com/aws-samples/aws-cdk-examples) — official patterns in TS, Python, Java, Go, .NET

### Terraform on AWS

- [HashiCorp AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest)
- [Terraform AWS provider upgrade strategy](https://www.factualminds.com/blog/terraform-aws-provider-upgrade-strategy/)
- [Terraform state management — import, move, repair](https://www.factualminds.com/blog/terraform-state-management-aws-import-move-repair/)
- [Safe Terraform apply workflows — approval gates](https://www.factualminds.com/blog/safe-terraform-apply-workflows-approval-gates-aws/)
- [AWS infrastructure drift detection — Terraform](https://www.factualminds.com/blog/aws-infrastructure-drift-detection-terraform/)
- [Migrate Terraform → OpenTofu on AWS](https://www.factualminds.com/blog/migrate-terraform-opentofu-aws/)
- [Terraform on AWS — integration guide](https://www.factualminds.com/integrations/terraform-aws/)

### Pulumi on AWS

> Imperative IaC in TypeScript / Python / Go / .NET / Java with real programming-language constructs.

- [Pulumi AWS provider](https://www.pulumi.com/registry/packages/aws/) — official provider docs
- [Pulumi AWS Native](https://www.pulumi.com/registry/packages/aws-native/) — generated from CloudFormation schema for full coverage
- [Pulumi vs Terraform](https://www.pulumi.com/docs/iac/concepts/vs/terraform/) — official comparison
- [Pulumi vs CDK](https://www.pulumi.com/docs/iac/comparisons/cloud-template-transpilers/aws-cdk/) — official comparison

### SST

> TypeScript-native IaC purpose-built for serverless on AWS.

- [SST](https://sst.dev/) — full-stack framework on AWS
- [SST Documentation](https://sst.dev/docs/) — Ion (v3) is AWS-only with Pulumi/Terraform under the hood
- [SST Components](https://sst.dev/docs/components/) — high-level constructs for common AWS patterns

### AWS CodePipeline / CodeBuild / CodeDeploy

- [CodePipeline](https://aws.amazon.com/codepipeline/) · [CodeBuild](https://aws.amazon.com/codebuild/) · [CodeDeploy](https://aws.amazon.com/codedeploy/)
- [CodePipeline CI/CD patterns for production](https://www.factualminds.com/blog/aws-codepipeline-cicd-pipeline-patterns-for-production/)
- [DevOps on AWS — CodePipeline vs GitHub Actions vs Jenkins](https://www.factualminds.com/blog/devops-on-aws-codepipeline-vs-github-actions-vs-jenkins/) · [Compare](https://www.factualminds.com/compare/aws-codepipeline-vs-github-actions/)

### GitHub Actions on AWS

- [GitHub Actions AWS CI/CD security best practices](https://www.factualminds.com/blog/github-actions-aws-cicd-security-best-practices/)
- [GitHub Actions on AWS — integration guide](https://www.factualminds.com/integrations/github-actions-aws/)

### General DevOps Practice

- [10 AWS DevOps practices for production](https://www.factualminds.com/blog/10-aws-devops-practices-production-2026/)
- [DevOps Exercises on AWS — production reality](https://www.factualminds.com/blog/devops-exercises-aws-production-reality/)
- [AWS environment parity — dev / staging / production](https://www.factualminds.com/blog/aws-environment-parity-dev-staging-production/)
- [Cost-aware CI/CD pipelines on AWS](https://www.factualminds.com/blog/cost-aware-cicd-pipelines-aws/)
- [Debug production distributed AWS systems](https://www.factualminds.com/blog/debug-production-distributed-aws-systems/)

### Local Dev / Emulators

- [LocalStack](https://localstack.cloud/) — AWS-in-a-box for local dev
- [Ministack — free LocalStack alternative](https://www.factualminds.com/blog/ministack-free-localstack-alternative-aws-emulator/)
- [getmoto/moto](https://github.com/getmoto/moto) — mock AWS services for Python tests (boto3 stub library)
- [AWS CLI chmod /dev/null streaming bug](https://www.factualminds.com/blog/aws-cli-chmod-dev-null-streaming-bug-2026/) — gotcha alert

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
- [AWS SDK list](https://aws.amazon.com/developer/tools/) — Python (boto3), JS, Java, Go, Rust, ...
- [AWS CloudShell](https://aws.amazon.com/cloudshell/) — browser shell with credentials pre-loaded
- [AWS Toolkit for VS Code / JetBrains](https://aws.amazon.com/visualstudiocode/)

### Asset Pipelines / Runtimes

- [Tune PHP / Node / Python / Go for high concurrency](https://www.factualminds.com/blog/tune-php-node-python-go-high-concurrency/)
- [Ultra-fast asset pipelines — Bun + Vite + Rust](https://www.factualminds.com/blog/ultra-fast-asset-pipelines-bun-vite-rust/)
- [Nginx vs FrankenPHP — modern runtimes comparison](https://www.factualminds.com/blog/nginx-frankenphp-modern-runtimes-comparison/)

---

## Observability & Monitoring

> 🎯 **Building an observability pipeline at scale?** See the [Observability pipeline playbook](use-cases/observability-pipeline.md) — hot CloudWatch + cold S3-Athena, EMF metrics, trace sampling, PII redaction, and cost discipline.

### Amazon CloudWatch

**Official:**
- [CloudWatch Documentation](https://docs.aws.amazon.com/cloudwatch/)
- [CloudWatch Application Signals](https://aws.amazon.com/cloudwatch/features/application-observability-apm/) — auto-instrumented APM with SLO tracking
- [CloudWatch Logs Insights](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/AnalyzingLogData.html) — query language for log analytics

**Production Guides:**
- [CloudWatch observability — metrics, logs, alarms best practices](https://www.factualminds.com/blog/aws-cloudwatch-observability-metrics-logs-alarms-best-practices/)
- [CloudWatch logging costs](https://www.factualminds.com/blog/aws-cloudwatch-logging-costs-observability/)
- [Amazon CloudWatch — glossary entry](https://www.factualminds.com/glossary/amazon-cloudwatch/)

### AWS X-Ray

- [X-Ray](https://aws.amazon.com/xray/) — distributed tracing; in maintenance per AWS lifecycle docs [maintenance]

### OpenTelemetry on AWS

**Official:**
- [AWS Distro for OpenTelemetry (ADOT)](https://aws-otel.github.io/) — recommended successor to X-Ray for new tracing
- [ADOT Documentation](https://aws-otel.github.io/docs/introduction)
- [ADOT Lambda layer](https://aws-otel.github.io/docs/getting-started/lambda) — auto-instrumentation for Lambda

**Production Guides:**
- [OpenTelemetry demo game — AWS observability + chaos engineering](https://www.factualminds.com/blog/otel-demo-game-aws-observability-chaos-engineering/)

### Amazon Managed Service for Prometheus / Grafana

- [Amazon Managed Prometheus (AMP)](https://aws.amazon.com/prometheus/) · [Amazon Managed Grafana (AMG)](https://aws.amazon.com/grafana/)

### Operational Monitoring

- [The real cost of no 24/7 AWS monitoring](https://www.factualminds.com/blog/real-cost-of-no-24-7-aws-monitoring/)
- [AWS 24/7 managed support + monitoring](https://www.factualminds.com/blog/aws-24-7-managed-support-monitoring/)

### Log Pipelines

- [Stream CloudWatch Logs to S3 via Firehose](https://docs.aws.amazon.com/firehose/latest/dev/writing-with-cloudwatch-logs.html) — official log pipeline pattern
- [Querying CloudWatch logs in S3 with Athena](https://docs.aws.amazon.com/athena/latest/ug/cloudwatch-logs.html) — long-term log analytics on cold storage
- [Centralized Logging with OpenSearch (Solutions)](https://aws.amazon.com/solutions/implementations/centralized-logging-with-opensearch/) — official deployable reference

### Third-party

- [Datadog on AWS — integration](https://www.factualminds.com/integrations/datadog-aws/)

---

## Cost Management & FinOps

> 🎯 **Hunting a surprise bill?** See the [Cost pitfalls playbook](use-cases/cost-pitfalls.md) — NAT Gateway egress, cross-AZ traffic, CloudWatch Logs ingestion, and the other line items that surprise teams.

### Cost Tools (Native)

- [AWS Cost Explorer](https://aws.amazon.com/aws-cost-management/aws-cost-explorer/)
- [AWS Budgets](https://aws.amazon.com/aws-cost-management/aws-budgets/)
- [AWS Compute Optimizer](https://aws.amazon.com/compute-optimizer/)
- [AWS Cost Anomaly Detection](https://aws.amazon.com/aws-cost-management/aws-cost-anomaly-detection/)
- [AWS Trusted Advisor](https://aws.amazon.com/premiumsupport/technology/trusted-advisor/)
- [AWS Billing and Cost Management — official user guide](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/) — accounts, invoices, allocation tags
- [AWS Customer Carbon Footprint Tool](https://aws.amazon.com/aws-cost-management/aws-customer-carbon-footprint-tool/) — estimated emissions by service + region (free, in Billing console)

### Strategy & Playbooks

- [Cost Explorer + Budgets monitoring guide](https://www.factualminds.com/blog/aws-cost-explorer-budgets-monitoring-guide/)
- [Cost Optimization Hub guide](https://www.factualminds.com/blog/aws-cost-optimization-hub-guide/)
- [Use Cost Anomaly Detection to catch surprise bills](https://www.factualminds.com/blog/how-to-use-aws-cost-anomaly-detection-catch-surprise-bills/)
- [5 cost optimization strategies most teams overlook](https://www.factualminds.com/blog/5-aws-cost-optimization-strategies-most-teams-overlook/)
- [Cloud cost optimization — modern strategies](https://www.factualminds.com/blog/cloud-cost-optimization-2026-modern-strategies/)
- [AWS cost prediction playbook](https://www.factualminds.com/blog/aws-cost-prediction-2026-playbook/)
- [AWS cost control architecture optimization playbook](https://www.factualminds.com/blog/aws-cost-control-architecture-optimization-playbook/)
- [Designing cost-stable AWS architectures](https://www.factualminds.com/blog/aws-cost-stable-architecture-design/)
- [Eliminate surprise bills with autoscaling](https://www.factualminds.com/blog/aws-eliminate-surprise-bills-autoscaling/)
- [Multi-region AWS without doubling costs](https://www.factualminds.com/blog/multi-region-aws-without-doubling-costs/)
- [AWS pricing emergent behavior — billing complexity](https://www.factualminds.com/blog/aws-pricing-emergent-behavior-billing-complexity/)
- [Prevent queue cost explosions on AWS](https://www.factualminds.com/blog/prevent-queue-cost-explosions-aws/)
- [Cost-optimized SaaS stack on AWS — end to end](https://www.factualminds.com/blog/cost-optimized-saas-stack-aws-end-to-end/)
- [AWS data transfer costs for startups](https://www.factualminds.com/blog/aws-data-transfer-costs-startups/)

### FinOps

- [FinOps on AWS — complete cost governance guide](https://www.factualminds.com/blog/finops-on-aws-complete-guide-cloud-cost-governance/)
- [AWS FinOps gap — engineering cost ownership](https://www.factualminds.com/blog/aws-finops-gap-engineering-cost-ownership/)
- [FinOps — glossary entry](https://www.factualminds.com/glossary/finops/)
- [FinOps Foundation](https://www.finops.org/) — global community

### Bill Teardowns (real customer incidents)

- [Bill teardown #1 — SaaS startup with $40k/mo overrun](https://www.factualminds.com/blog/aws-bill-teardown-1-saas-startup-40k-month-overrun/)
- [Bill teardown #2 — healthcare's NAT Gateway problem](https://www.factualminds.com/blog/aws-bill-teardown-2-healthcare-nat-gateway-problem/)
- [Bill teardown #3 — retail's data transfer trap](https://www.factualminds.com/blog/aws-bill-teardown-3-retail-data-transfer-trap/)
- [AWS startup cost explosion — real failure patterns](https://www.factualminds.com/blog/aws-startup-cost-explosion-real-failure-patterns/)
- [SaaS cost optimization — case study ($85k → $58k/mo)](https://www.factualminds.com/case-study/saas-cost-optimization-30-percent-reduction/)

### Savings Plans / Reserved Instances

- [Savings Plans](https://aws.amazon.com/savingsplans/) · [Reserved Instances](https://aws.amazon.com/ec2/pricing/reserved-instances/)
- [Reserved Instances vs Savings Plans](https://www.factualminds.com/glossary/reserved-instances-vs-savings-plans/)
- [AWS Savings Plans — glossary](https://www.factualminds.com/glossary/aws-savings-plans/)

### Managed vs DIY Cost

- [AWS managed services vs DIY — total cost of ownership](https://www.factualminds.com/blog/aws-managed-services-vs-diy-total-cost-of-ownership/)

**OSS Cost Tools:**
- [Infracost](https://www.infracost.io/) — Terraform → cost diff in PRs
- [Komiser](https://github.com/tailwarden/komiser) — multi-cloud cost + resource viewer
- [aws-nuke](https://github.com/rebuy-de/aws-nuke) — wipe orphaned dev accounts
- [Cloud Intelligence Dashboards](https://github.com/aws-samples/aws-cudos-framework-deployment) — CUR analytics dashboards (CUDOS, Cost Intelligence, KPI)
- [cloud-custodian/cloud-custodian](https://github.com/cloud-custodian/cloud-custodian) — YAML rules engine for resource governance, cost, and compliance enforcement
- [Similarweb/finala](https://github.com/similarweb/finala) — scans AWS for wasteful and unused resources to cut spend

---

## Migration & Transfer

### AWS Migration Hub & MAP

- [AWS Migration Hub](https://aws.amazon.com/migration-hub/)
- [Migration Acceleration Program (MAP)](https://aws.amazon.com/migration-acceleration-program/)
- [MAP for SMBs — guide](https://www.factualminds.com/blog/aws-migration-acceleration-program-map-smb-guide/)

### AWS Application Migration Service (MGN) & DMS

- [Application Migration Service](https://aws.amazon.com/application-migration-service/)
- [Database Migration Service (DMS)](https://aws.amazon.com/dms/)

### Migration Strategy

- [AWS migration strategy — choose the right approach](https://www.factualminds.com/blog/aws-migration-strategy-choose-right-approach/)
- [Application modernization — refactor / replatform / rearchitect](https://www.factualminds.com/blog/aws-application-modernization-refactor-replatform-rearchitect/)
- [Application modernization ROI + business case](https://www.factualminds.com/blog/aws-application-modernization-roi-business-case/)
- [Migrate without cost surprises](https://www.factualminds.com/blog/aws-migration-without-cost-surprises/)
- [7 signs you need a migration partner](https://www.factualminds.com/blog/7-signs-you-need-an-aws-cloud-migration-partner/)
- [Cloud migration estimator tool](https://www.factualminds.com/tools/cloud-migration-estimator/)

### Disaster Recovery

- [DR strategies — pilot light / warm standby / multi-site](https://www.factualminds.com/blog/aws-disaster-recovery-strategies-pilot-light-warm-standby-multi-site/)

### VMware → AWS

- [Amazon Elastic VMware Service (EVS)](https://www.factualminds.com/blog/amazon-elastic-vmware-service-evs/)

---

## Internet of Things (IoT)

### AWS IoT Core

- [IoT Core Documentation](https://docs.aws.amazon.com/iot/)
- [IoT Core MQTT for industrial workloads](https://www.factualminds.com/blog/aws-iot-core-mqtt-industrial-workloads/)
- [IoT solutions architecture guide](https://www.factualminds.com/blog/aws-iot-solutions-architecture-guide/)

### AWS IoT Greengrass

- [Greengrass v2 — edge computing for the factory floor](https://www.factualminds.com/blog/aws-iot-greengrass-v2-edge-computing-factory-floor/)

### AWS IoT SiteWise

- [SiteWise native anomaly detection — predictive maintenance](https://www.factualminds.com/blog/aws-iot-sitewise-native-anomaly-detection-predictive-maintenance/)
- [OPC UA → IoT SiteWise edge gateway setup](https://www.factualminds.com/blog/opc-ua-aws-iot-sitewise-edge-gateway-setup/)

### AWS IoT TwinMaker

- [TwinMaker — digital twin for manufacturing](https://www.factualminds.com/blog/aws-iot-twinmaker-digital-twin-manufacturing/)

### Architecture

- [OT/IT convergence — AWS architecture patterns](https://www.factualminds.com/blog/ot-it-convergence-aws-architecture-patterns/)
- [Manufacturing IoT predictive maintenance — case study](https://www.factualminds.com/case-study/manufacturing-iot-predictive-maintenance-aws/)

---

## Application Integration

> 🎯 **Building async/event-driven systems?** See [Async job processing](use-cases/async-jobs.md) (queue + worker + DLQ) and [Event-driven processing](use-cases/event-driven.md) (EventBridge with schemas, replay, per-target DLQs).

### Amazon SQS

- [SQS Documentation](https://docs.aws.amazon.com/sqs/)
- [SQS reliable messaging patterns for production](https://www.factualminds.com/blog/aws-sqs-reliable-messaging-patterns-for-production/)
- [Reliable queue systems on AWS — SQS, Kafka, Redis](https://www.factualminds.com/blog/reliable-queue-systems-aws-sqs-kafka-redis/)

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
- [SES e-commerce email marketing](https://www.factualminds.com/blog/aws-ses-ecommerce-email-marketing/)
- [Migrate from SendGrid to SES](https://www.factualminds.com/blog/how-to-migrate-from-sendgrid-to-amazon-ses/)
- [SES at scale — case study (200M+ messages/mo)](https://www.factualminds.com/case-study/aws-ses/)

### SES Migrations from Competitors

- [SendGrid → SES](https://www.factualminds.com/compare/sendgrid-to-aws-ses/)
- [Mailgun → SES](https://www.factualminds.com/compare/mailgun-to-aws-ses/)
- [Postmark → SES](https://www.factualminds.com/compare/postmark-to-aws-ses/)
- [Resend → SES](https://www.factualminds.com/compare/resend-to-aws-ses/)
- [SparkPost → SES](https://www.factualminds.com/compare/sparkpost-to-aws-ses/)
- [Elastic Email → SES](https://www.factualminds.com/compare/elastic-email-to-aws-ses/)

---

## Management & Governance

### AWS Organizations

- [AWS Organizations](https://aws.amazon.com/organizations/)
- [Organizations + SCPs — glossary](https://www.factualminds.com/glossary/aws-organizations-scps/)

### AWS Control Tower & Landing Zone

- [Control Tower](https://aws.amazon.com/controltower/)
- [Set up Control Tower for multi-account governance](https://www.factualminds.com/blog/how-to-set-up-aws-control-tower-multi-account-governance/)
- [AWS multi-account strategy — landing zone best practices](https://www.factualminds.com/blog/aws-multi-account-strategy-landing-zone-best-practices/)
- [AWS Control Tower — glossary](https://www.factualminds.com/glossary/aws-control-tower/)
- [AWS Landing Zone — glossary](https://www.factualminds.com/glossary/aws-landing-zone/)

### AWS Config

- [AWS Config](https://aws.amazon.com/config/) — resource inventory + compliance
- [AWS Config Rules — glossary](https://www.factualminds.com/glossary/aws-config-rules/)

### Service Limits, Quotas & Throttling

> Hard vs soft limits, retry strategy, and the throttling behaviour that bites at scale.

**Official:**
- [Service Quotas console](https://docs.aws.amazon.com/servicequotas/latest/userguide/intro.html) — view and request increases for soft limits
- [AWS service quotas reference](https://docs.aws.amazon.com/general/latest/gr/aws_service_limits.html) — per-service hard and soft limits
- [Error retries and exponential backoff (SDK guidance)](https://docs.aws.amazon.com/general/latest/gr/api-retries.html) — official retry behaviour
- [Timeouts, retries, and backoff with jitter (Builders Library)](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/) — first-principles guidance
- [API Gateway throttling](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-request-throttling.html) — account-, stage-, and key-level limits
- [Lambda concurrency and throttling](https://docs.aws.amazon.com/lambda/latest/dg/lambda-concurrency.html) — reserved vs provisioned concurrency
- [DynamoDB throttling and adaptive capacity](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-partition-key-design.html) — partition-level throttling

### AWS Support & MSP

- [AWS Support Plans](https://aws.amazon.com/premiumsupport/plans/)
- [AWS managed services vs Support plans — difference](https://www.factualminds.com/blog/aws-managed-services-vs-aws-support-plans-difference/)
- [What does an AWS MSP actually do](https://www.factualminds.com/blog/what-does-aws-msp-actually-do/)
- [When do you need an AWS MSP](https://www.factualminds.com/blog/when-do-you-need-aws-managed-services-provider/)
- [How to evaluate an AWS MSP](https://www.factualminds.com/blog/how-to-evaluate-aws-managed-services-provider/)

### Hiring an AWS Consultant

- [How to choose an AWS cloud consulting partner](https://www.factualminds.com/blog/aws-cloud-consulting-partner-how-to-choose/)
- [Benefits of hiring a certified AWS consultant](https://www.factualminds.com/blog/benefits-of-hiring-certified-aws-consultant/)
- [What to look for when hiring an AWS consultant](https://www.factualminds.com/blog/hire-aws-consultant-what-to-look-for/)
- [When to hire an AWS consultant — business triggers](https://www.factualminds.com/blog/when-to-hire-aws-consultant-business-triggers/)

### AWS Partner Network

- [AWS Partner Network (APN)](https://aws.amazon.com/partners/)
- [AWS Retail Competency — what it means for your business](https://www.factualminds.com/blog/aws-retail-competency-what-it-means-for-your-business/)

---

## Well-Architected Framework

> Six pillars: Operational Excellence, Security, Reliability, Performance Efficiency, Cost Optimization, Sustainability.

- [Well-Architected Framework — official](https://aws.amazon.com/architecture/well-architected/)
- [WAF Tool (free review)](https://aws.amazon.com/well-architected-tool/)
- [WAF lenses (Serverless, SaaS, GenAI, ...)](https://aws.amazon.com/architecture/well-architected/?ref=wellarchitected-wp&wa-lens-whitepapers.sort-by=item.additionalFields.sortDate&wa-lens-whitepapers.sort-order=desc)
- [Reliability Pillar (official whitepaper)](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/) — failure isolation, recovery, multi-AZ
- [Cost Optimization Pillar (official whitepaper)](https://docs.aws.amazon.com/wellarchitected/latest/cost-optimization-pillar/) — practices for spend efficiency
- [WAF 6 pillars explained](https://www.factualminds.com/blog/aws-well-architected-framework-6-pillars-explained/)
- [Well-Architected Framework — glossary](https://www.factualminds.com/glossary/well-architected-framework/)
- [AWS Well-Architected Review service](https://www.factualminds.com/services/aws-architecture-review/)
- [Free Well-Architected self-assessment tool](https://www.factualminds.com/tools/aws-well-architected-assessment/)

---

## Industry Architectures

End-to-end reference architectures for verticals.

### SaaS

- [SaaS multi-tenancy on AWS — silo vs pool vs bridge](https://www.factualminds.com/blog/saas-multi-tenancy-on-aws-silo-vs-pool-vs-bridge-model/)
- [Multi-tenant SaaS on AWS — architecture pattern](https://www.factualminds.com/patterns/multi-tenant-saas-on-aws/)
- [SaaS industry hub](https://www.factualminds.com/industries/saas/)

### Startups

- [AWS for Startups industry hub](https://www.factualminds.com/industries/aws-startups/)

### Fintech

- [Fintech architecture patterns on AWS](https://www.factualminds.com/blog/building-fintech-applications-on-aws-architecture-patterns/)
- [Fintech industry hub](https://www.factualminds.com/industries/aws-fintech/)

### Healthcare

- [Healthcare industry hub](https://www.factualminds.com/industries/aws-healthcare/)

### Retail & eCommerce

- [AWS for retail — complete guide](https://www.factualminds.com/blog/aws-for-retail-complete-guide/)
- [Retail architecture for Black Friday peak traffic](https://www.factualminds.com/blog/aws-retail-architecture-black-friday-peak-traffic/)
- [Custom AWS development for retail / eCommerce](https://www.factualminds.com/blog/custom-aws-development-retail-ecommerce/)
- [Retail & eCommerce industry hub](https://www.factualminds.com/industries/aws-retail-ecommerce/)

### Manufacturing & Industrial IoT

- [Manufacturing industry hub](https://www.factualminds.com/industries/aws-manufacturing/)

### Education / EdTech

- [Education industry hub](https://www.factualminds.com/industries/aws-education/)

### Real Estate / PropTech

- [Real Estate industry hub](https://www.factualminds.com/industries/aws-real-estate/)

---

## Decision Guides — X vs Y

When you know what you need but not which AWS service to use:

### Compute

- [EC2 vs Lambda](https://www.factualminds.com/compare/aws-ec2-vs-lambda/)
- [Lambda vs ECS Fargate](https://www.factualminds.com/compare/aws-lambda-vs-ecs-fargate/)
- [ECS vs EKS](https://www.factualminds.com/compare/aws-ecs-vs-eks/)
- [Which AWS compute?](https://www.factualminds.com/decide/which-aws-compute/)

### Databases

- [RDS vs Aurora](https://www.factualminds.com/compare/aws-rds-vs-aurora/)
- [Aurora Serverless vs Aurora provisioned](https://www.factualminds.com/compare/aws-aurora-serverless-vs-aurora-provisioned/)
- [DynamoDB vs RDS](https://www.factualminds.com/compare/dynamodb-vs-rds/)
- [Which AWS database?](https://www.factualminds.com/decide/which-aws-database/)

### Networking & CDN

- [CloudFront vs Cloudflare](https://www.factualminds.com/compare/aws-cloudfront-vs-cloudflare/)
- [WAF vs Network Firewall](https://www.factualminds.com/compare/aws-waf-vs-network-firewall/)

### Security & Identity

- [GuardDuty vs Security Hub](https://www.factualminds.com/compare/aws-guardduty-vs-security-hub/)
- [IAM Identity Center vs Cognito](https://www.factualminds.com/compare/aws-iam-identity-center-vs-cognito/)

### Integration

- [Step Functions vs EventBridge](https://www.factualminds.com/compare/aws-step-functions-vs-eventbridge/)
- [Bedrock Agents vs Step Functions](https://www.factualminds.com/compare/aws-bedrock-agents-vs-step-functions/)

### CI/CD

- [CodePipeline vs GitHub Actions](https://www.factualminds.com/compare/aws-codepipeline-vs-github-actions/)
- [Terraform vs CDK — IaC decision guide](https://www.factualminds.com/blog/terraform-vs-aws-cdk-infrastructure-as-code-decision-guide/)
- [Pulumi vs Terraform](https://www.pulumi.com/docs/iac/concepts/vs/terraform/) — official comparison
- [Pulumi vs CDK](https://www.pulumi.com/docs/iac/comparisons/cloud-template-transpilers/aws-cdk/) — official comparison

### AI/ML

- [Bedrock vs SageMaker](https://www.factualminds.com/compare/aws-bedrock-vs-sagemaker/)
- [Amazon Q vs ChatGPT Enterprise](https://www.factualminds.com/compare/amazon-q-vs-chatgpt-enterprise/)

### Cloud Platform

- [AWS vs Azure for enterprise](https://www.factualminds.com/compare/aws-vs-azure-for-enterprise/)
- [AWS vs GCP for startups](https://www.factualminds.com/compare/aws-vs-gcp-for-startups/)

### Consulting Partner Comparisons

- [FactualMinds vs Big 4 AWS](https://www.factualminds.com/compare/factualminds-vs-big4-aws/)
- [FactualMinds vs Cloudreach](https://www.factualminds.com/compare/factualminds-vs-cloudreach/)
- [FactualMinds vs Slalom](https://www.factualminds.com/compare/factualminds-vs-slalom/)

---

## Migration Guides — From Other Platforms

- [DigitalOcean → AWS](https://www.factualminds.com/compare/digitalocean-to-aws/)
- [Heroku Postgres → AWS RDS](https://www.factualminds.com/compare/heroku-postgres-to-aws-rds/)
- [GCP → AWS migration](https://www.factualminds.com/compare/gcp-to-aws-migration/)
- [MongoDB Atlas → DocumentDB](https://www.factualminds.com/compare/mongodb-atlas-to-documentdb/)
- [SendGrid → SES](https://www.factualminds.com/compare/sendgrid-to-aws-ses/)
- [Mailgun → SES](https://www.factualminds.com/compare/mailgun-to-aws-ses/)
- [Postmark → SES](https://www.factualminds.com/compare/postmark-to-aws-ses/)
- [Resend → SES](https://www.factualminds.com/compare/resend-to-aws-ses/)
- [SparkPost → SES](https://www.factualminds.com/compare/sparkpost-to-aws-ses/)
- [Elastic Email → SES](https://www.factualminds.com/compare/elastic-email-to-aws-ses/)

---

## AWS Service Lifecycle & Deprecations

> What state is each service in? AWS publishes explicit lifecycle states — Maintenance, Sunset, Full Shutdown — and the roster changes faster than most curated lists track. This section flags the services that affect new architectural decisions and points at official replacements.

### Lifecycle reference

- [AWS Service Lifecycle](https://docs.aws.amazon.com/general/latest/gr/service-lifecycle.html) — official definitions of Maintenance, Sunset, Full Shutdown
- [Services in Full Shutdown](https://docs.aws.amazon.com/general/latest/gr/full_shutdown_services.html) — official roster of shut-down services with dates
- [AWS service changes — May 2025](https://aws.amazon.com/about-aws/whats-new/2025/05/aws-service-changes/) — most recent batch of lifecycle announcements
- [AWS Product Lifecycle blog post](https://aws.amazon.com/blogs/aws/introducing-the-aws-product-lifecycle-page-and-aws-service-availability-updates/) — context behind the lifecycle page

### Full shutdown — already removed

Highlights from the [official roster](https://docs.aws.amazon.com/general/latest/gr/full_shutdown_services.html); see that page for the complete list and exact dates.

- [Amazon QLDB](https://aws.amazon.com/qldb/) — ledger database; shut down July 31, 2025 [shutdown]
- [Amazon Kinesis Data Analytics for SQL](https://aws.amazon.com/kinesis/data-analytics/) — replacement → Managed Service for Apache Flink [shutdown]
- [Amazon CloudWatch Evidently](https://aws.amazon.com/cloudwatch/) — feature flags and A/B; shut down October 17, 2025 [shutdown]
- [AWS DataSync Discovery](https://aws.amazon.com/datasync/) — on-prem storage assessment; shut down May 20, 2025 [shutdown]
- [AWS Private 5G](https://aws.amazon.com/private5g/) — managed cellular networks; shut down May 20, 2025 [shutdown]
- [AWS BugBust](https://aws.amazon.com/bugbust/) — code-fix gamification; shut down August 13, 2025 [shutdown]
- [AWS OpsWorks (Stacks, Chef, Puppet)](https://aws.amazon.com/opsworks/) — config management; shut down May 1, 2024 [shutdown]
- [AWS CodeStar](https://aws.amazon.com/codestar/) — project templates; shut down July 25, 2024 [shutdown]
- [AWS RoboMaker](https://aws.amazon.com/robomaker/) — robotics simulation; shut down September 10, 2025 [shutdown]
- [Amazon Lookout for Metrics](https://aws.amazon.com/lookout-for-metrics/) — anomaly detection; shut down October 10, 2025 [shutdown]
- [Amazon Lookout for Vision](https://aws.amazon.com/lookout-for-vision/) — defect detection; shut down October 31, 2025 [shutdown]
- [Amazon WorkDocs](https://aws.amazon.com/workdocs/) — file storage and sharing; shut down April 25, 2025 [shutdown]

### End-of-support announced — avoid for new projects

Per the [May 2025 AWS service changes announcement](https://aws.amazon.com/about-aws/whats-new/2025/05/aws-service-changes/). AWS has not yet published exact end-of-support dates for most.

- [Amazon Pinpoint](https://aws.amazon.com/pinpoint/) — multi-channel messaging; replacement → SES, SNS, EventBridge [sunset]
- [AWS IoT Analytics](https://aws.amazon.com/iot-analytics/) — replacement → IoT Core + Kinesis or EventBridge [sunset]
- [AWS IoT Events](https://aws.amazon.com/iot-events/) — event detection; replacement → EventBridge + Lambda [sunset]
- [AWS Panorama](https://aws.amazon.com/panorama/) — appliance-based computer vision at the edge [sunset]
- [AWS SimSpace Weaver](https://aws.amazon.com/simspaceweaver/) — large-scale spatial simulations; ends March 31, 2026 [sunset]
- [Amazon Inspector Classic](https://docs.aws.amazon.com/inspector/v1/userguide/inspector_introduction.html) — replacement → Amazon Inspector v2 [sunset]
- [AWS IQ](https://aws.amazon.com/iq/) — freelance AWS experts marketplace [sunset]
- [AWS DMS Fleet Advisor](https://docs.aws.amazon.com/dms/latest/userguide/fleet-advisor.html) — replacement → AWS DMS [sunset]
- [Amazon Connect Voice ID](https://docs.aws.amazon.com/connect/latest/adminguide/voice-id.html) — caller authentication; end-of-support announced [sunset]

### Maintenance — closed to new customers

Per AWS lifecycle docs: existing customers retain access; no new features, no onboarding.

- [AWS X-Ray](https://aws.amazon.com/xray/) — distributed tracing; in maintenance per AWS lifecycle docs [maintenance]
- [Amazon Timestream for LiveAnalytics](https://aws.amazon.com/timestream/) — closed to new customers June 20, 2025 [maintenance]

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

- [AWS Cost Savings Calculator](https://www.factualminds.com/tools/aws-cost-savings-calculator/)
- [AWS Cost Waste Quiz](https://www.factualminds.com/tools/aws-cost-waste-quiz/)
- [AWS Feature Cost Estimator](https://www.factualminds.com/tools/aws-feature-cost-estimator/)
- [AWS Free Tier Calculator](https://www.factualminds.com/tools/aws-free-tier-calculator/)
- [AWS IOPS Cost Calculator](https://www.factualminds.com/tools/aws-iops-cost-calculator/)
- [AWS Lambda vs Container Cost Calculator](https://www.factualminds.com/tools/aws-lambda-vs-container-cost-calculator/)
- [AWS Reserved Instance Calculator](https://www.factualminds.com/tools/aws-reserved-instance-calculator/)
- [AWS Savings Plans Calculator](https://www.factualminds.com/tools/aws-savings-plans-calculator/)
- [AWS Scaling Cost Simulator](https://www.factualminds.com/tools/aws-scaling-cost-simulator/)
- [AWS Tenancy Cost Calculator](https://www.factualminds.com/tools/aws-tenancy-cost-calculator/)
- [AWS Unit Economics Calculator](https://www.factualminds.com/tools/aws-unit-economics-calculator/)
- [AWS RDS Max Connection Calculator](https://www.factualminds.com/tools/aws-rds-max-connection-calculator/)
- [AWS Bedrock Token Cost Calculator](https://www.factualminds.com/tools/aws-bedrock-token-cost-calculator/)

### Migration & Assessment

- [Cloud Migration Estimator](https://www.factualminds.com/tools/cloud-migration-estimator/)
- [AWS Well-Architected Assessment](https://www.factualminds.com/tools/aws-well-architected-assessment/)
- [GenAI Readiness Assessment](https://www.factualminds.com/tools/genai-readiness-assessment/)
- [HIPAA Compliance Checker](https://www.factualminds.com/tools/hipaa-compliance-checker/)

### Official AWS Tools

- [AWS Pricing Calculator](https://calculator.aws/)
- [AWS Total Cost of Ownership (TCO) Calculator](https://aws.amazon.com/tco-calculator/)

---

## AWS Glossary

Plain-language definitions of common AWS terms:

- [Amazon Aurora](https://www.factualminds.com/glossary/amazon-aurora/)
- [Amazon Bedrock](https://www.factualminds.com/glossary/amazon-bedrock/)
- [Amazon CloudWatch](https://www.factualminds.com/glossary/amazon-cloudwatch/)
- [Amazon DynamoDB](https://www.factualminds.com/glossary/amazon-dynamodb/)
- [Amazon EC2](https://www.factualminds.com/glossary/amazon-ec2/)
- [Amazon EKS](https://www.factualminds.com/glossary/amazon-eks/)
- [Amazon RDS](https://www.factualminds.com/glossary/amazon-rds/)
- [Amazon Redshift](https://www.factualminds.com/glossary/amazon-redshift/)
- [Amazon S3](https://www.factualminds.com/glossary/amazon-s3/)
- [Amazon VPC](https://www.factualminds.com/glossary/amazon-vpc/)
- [AWS CloudTrail](https://www.factualminds.com/glossary/aws-cloudtrail/)
- [AWS Config Rules](https://www.factualminds.com/glossary/aws-config-rules/)
- [AWS Control Tower](https://www.factualminds.com/glossary/aws-control-tower/)
- [AWS IAM](https://www.factualminds.com/glossary/aws-iam/)
- [AWS KMS](https://www.factualminds.com/glossary/aws-kms/)
- [AWS Lambda](https://www.factualminds.com/glossary/aws-lambda/)
- [AWS Landing Zone](https://www.factualminds.com/glossary/aws-landing-zone/)
- [AWS Organizations + SCPs](https://www.factualminds.com/glossary/aws-organizations-scps/)
- [AWS Savings Plans](https://www.factualminds.com/glossary/aws-savings-plans/)
- [AWS Shared Responsibility Model](https://www.factualminds.com/glossary/aws-shared-responsibility-model/)
- [AWS Step Functions](https://www.factualminds.com/glossary/aws-step-functions/)
- [FinOps](https://www.factualminds.com/glossary/finops/)
- [HIPAA-eligible AWS services](https://www.factualminds.com/glossary/hipaa-eligible-aws-services/)
- [Multi-tenant architecture](https://www.factualminds.com/glossary/multi-tenant-architecture/)
- [PCI DSS Cardholder Data Environment](https://www.factualminds.com/glossary/pci-dss-cardholder-data-environment/)
- [RAG pipeline](https://www.factualminds.com/glossary/rag-pipeline/)
- [Reserved Instances vs Savings Plans](https://www.factualminds.com/glossary/reserved-instances-vs-savings-plans/)
- [SOC 2 Type 2](https://www.factualminds.com/glossary/soc2-type-2/)
- [VPC peering vs Transit Gateway](https://www.factualminds.com/glossary/vpc-peering-vs-transit-gateway/)
- [Well-Architected Framework](https://www.factualminds.com/glossary/well-architected-framework/)

---

## AWS Certifications & Learning Paths

### Official

- [AWS Certifications overview](https://aws.amazon.com/certification/)
- [AWS Skill Builder](https://skillbuilder.aws/) — official free training
- [AWS Workshops catalog](https://workshops.aws/)

### Cert Deep Dives

- [AWS Solutions Architect — Associate](https://www.factualminds.com/certifications/aws-solutions-architect-associate/)
- [AWS Security — Specialty](https://www.factualminds.com/certifications/aws-security-specialty/)

---

## Architecture Patterns

Reference patterns for the workloads that show up most often. Each links into the relevant service sections for depth.

### Multi-tenant SaaS

> 🎯 **Building a multi-tenant SaaS?** Start with the [Multi-tenant SaaS playbook](use-cases/multi-tenant-saas.md) — full architecture, failure modes, cost model, anti-patterns, and production checklist.

- [Multi-tenant SaaS on AWS — pattern](https://www.factualminds.com/patterns/multi-tenant-saas-on-aws/)
- [SaaS multi-tenancy — silo vs pool vs bridge](https://www.factualminds.com/blog/saas-multi-tenancy-on-aws-silo-vs-pool-vs-bridge-model/)
- [Multi-tenant architecture — glossary](https://www.factualminds.com/glossary/multi-tenant-architecture/)

**Reference implementations:**
- [aws-samples/aws-saas-factory-ref-solution-serverless-saas](https://github.com/aws-samples/aws-saas-factory-ref-solution-serverless-saas) — production serverless multi-tenant reference
- [aws-samples/aws-saas-factory-eks-reference-architecture](https://github.com/aws-samples/aws-saas-factory-eks-reference-architecture) — EKS multi-tenant reference
- [AWS SaaS Factory](https://aws.amazon.com/partners/saas-factory/) — AWS programme with reference architectures and tooling

See also: [Cognito for SaaS auth](#amazon-cognito) · [DynamoDB single-table for SaaS](#amazon-dynamodb) · [Multi-tenant SaaS playbook](use-cases/multi-tenant-saas.md)

### Event-driven & async

- [EventBridge event-driven architecture patterns](https://www.factualminds.com/blog/aws-eventbridge-event-driven-architecture-patterns/)
- [AWS Event-Driven Architecture (official)](https://aws.amazon.com/event-driven-architecture/) — patterns and reference architectures
- [Step Functions workflow orchestration patterns](https://www.factualminds.com/blog/aws-step-functions-workflow-orchestration-patterns/)
- See also: [SQS reliable messaging patterns](#amazon-sqs) · [EventBridge](#amazon-eventbridge)

### Multi-region & resilience

- [AWS Multi-Region Fundamentals (whitepaper)](https://docs.aws.amazon.com/whitepapers/latest/aws-multi-region-fundamentals/aws-multi-region-fundamentals.html)
- [Static Stability Using Availability Zones (Builders Library)](https://aws.amazon.com/builders-library/static-stability-using-availability-zones/) — designing for failure
- [Reliability Pillar (whitepaper)](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/)
- [DR strategies — pilot light / warm standby / multi-site](https://www.factualminds.com/blog/aws-disaster-recovery-strategies-pilot-light-warm-standby-multi-site/)
- [Multi-region AWS without doubling costs](https://www.factualminds.com/blog/multi-region-aws-without-doubling-costs/)

**Reference implementations:**
- [Route 53 Application Recovery Controller (ARC)](https://aws.amazon.com/route53/application-recovery-controller/) — readiness checks and zonal shift
- [Multi-region failover with Route 53 ARC — AWS blog walkthrough](https://aws.amazon.com/blogs/networking-and-content-delivery/creating-disaster-recovery-mechanisms-using-amazon-route-53/) — official end-to-end pattern

### Data lake & analytics

- [Building a data lake on S3 + Glue + Athena](https://www.factualminds.com/blog/building-a-data-lake-on-aws-s3-glue-athena-architecture/)
- [Build a serverless data pipeline — Glue + Athena](https://www.factualminds.com/blog/how-to-build-serverless-data-pipeline-glue-athena/)
- [Real-time pipeline — Kinesis + Lambda + DynamoDB](https://www.factualminds.com/blog/real-time-data-pipeline-kinesis-lambda-dynamodb/)
- [Glue 5 + Apache Iceberg — modern ETL](https://www.factualminds.com/blog/aws-glue-5-apache-iceberg-modern-etl/)

### GenAI & RAG

- [Build a RAG pipeline with Bedrock Knowledge Bases](https://www.factualminds.com/blog/how-to-build-rag-pipeline-amazon-bedrock-knowledge-bases/)
- [Bedrock multi-agent supervisor pattern](https://www.factualminds.com/blog/aws-bedrock-multi-agent-supervisor-pattern/)
- [Multi-tenant GenAI on Bedrock](https://www.factualminds.com/blog/multi-tenant-genai-bedrock/)
- [Fine-tuning vs RAG on Bedrock](https://www.factualminds.com/blog/fine-tuning-vs-rag-bedrock-when-to-use/)

### Migration

- [Refactor / replatform / rearchitect](https://www.factualminds.com/blog/aws-application-modernization-refactor-replatform-rearchitect/)
- [Migrate a monolith to ECS Fargate with zero downtime](https://www.factualminds.com/blog/how-to-migrate-monolith-ecs-fargate-zero-downtime/)
- [Migrate without cost surprises](https://www.factualminds.com/blog/aws-migration-without-cost-surprises/)

### Anti-patterns & common mistakes

> What teams get wrong on AWS — drawn from postmortems, bill-shock case studies, and scaling war stories.

- [The Amazon Builders' Library](https://aws.amazon.com/builders-library/) — first-person engineering writeups including how AWS itself avoids common mistakes
- [Avoiding insurmountable queue backlogs (Builders Library)](https://aws.amazon.com/builders-library/avoiding-insurmountable-queue-backlogs/) — the classic queue anti-pattern
- [Caching challenges and strategies (Builders Library)](https://aws.amazon.com/builders-library/caching-challenges-and-strategies/) — when caches make things worse
- [Avoiding overload in distributed systems by putting the smaller service in control (Builders Library)](https://aws.amazon.com/builders-library/avoiding-overload-in-distributed-systems-by-putting-the-smaller-service-in-control/) — load shedding done right
- [Bill teardowns — NAT Gateway, data transfer, Lambda runaway](#bill-teardowns-real-customer-incidents) — see Cost Management section for real customer incidents
- [Protect AWS infrastructure from cost-based attacks](https://www.factualminds.com/blog/protect-aws-infrastructure-cost-based-attacks/) — denial-of-wallet patterns

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
- [AWS MCP Server (managed, in preview — re:Invent 2025)](https://docs.aws.amazon.com/aws-mcp/latest/userguide/what-is-mcp-server.html) — fully-managed remote server with Agent SOPs + CloudTrail logging

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
- [Amazon Bedrock AgentCore MCP Server](https://awslabs.github.io/mcp/servers/amazon-bedrock-agentcore-mcp-server) — build, deploy, manage Bedrock agents
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
- [Model Context Protocol — official spec](https://modelcontextprotocol.io/) — Anthropic-led open protocol
- [punkpeye/awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers) — community catalog of all MCP servers (cross-vendor)
- [PulseMCP — AWS MCP servers directory](https://www.pulsemcp.com/servers?q=aws) — searchable index

---

## Engineering Blogs & Case Studies

How real companies run on AWS — production architectures, postmortems, and at-scale lessons. The "official docs" tell you what's possible; these tell you what actually broke.

### Engineering blogs from companies on AWS

- [Netflix Tech Blog](https://netflixtechblog.com/) — large-scale streaming, microservices, resilience
- [Netflix Simian Army (origin of chaos engineering)](https://netflixtechblog.com/the-netflix-simian-army-16e57fbab116) — the canonical "break things on purpose" essay
- [Netflix Chaos Engineering tag](https://netflixtechblog.com/tagged/chaos-engineering) — ongoing chaos posts
- [Airbnb Engineering](https://medium.com/airbnb-engineering) — search & infra at hospitality scale
- [Dropbox Tech — Infrastructure](https://dropbox.tech/infrastructure) — famous AWS-→-bare-metal exit + return-to-cloud insights
- [Pinterest Engineering](https://medium.com/@Pinterest_Engineering) — high-RPS feed + storage architecture
- [Capital One Tech — Cloud](https://www.capitalone.com/tech/cloud/) — regulated-finance cloud-native transformation

### AWS leadership blogs

- [All Things Distributed](https://www.allthingsdistributed.com/) — Werner Vogels (AWS CTO); architecture philosophy, eventual consistency, "you build it, you run it"
- [Jeff Barr — Things I Like](https://jeff-barr.com/) — AWS Chief Evangelist; release commentary and historical context
- [AWS Geek (Jerry Hargrove)](https://www.awsgeek.com/) — illustrated AWS service diagrams + cheat sheets

### AWS official postmortems & resilience reading

- [Amazon S3 Outage Postmortem (Feb 2017, us-east-1)](https://aws.amazon.com/message/41926/) — the classic teardown; required reading for designing resilient architectures
- [Kinesis Data Streams Outage (Nov 2020, us-east-1)](https://aws.amazon.com/message/11201/) — thread-limit cascade that took down Cognito, CloudWatch, and dozens of dependents
- [Lambda / API Gateway / EventBridge Disruption (Jun 2023, us-east-1)](https://aws.amazon.com/message/061323/) — control-plane failure mode; lessons on regional blast radius
- [AWS Builders Library — Resilience & Failures](https://aws.amazon.com/builders-library/) — operations essays from AWS principal engineers (also linked from [Foundations](#foundations))

> [!IMPORTANT]
> Pair these with the [Reliability Pillar](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/) and [Static Stability Using AZs](https://aws.amazon.com/builders-library/static-stability-using-availability-zones/) for the full failure-design picture. The recurring lesson: **us-east-1 is not a single region for outage purposes — global control planes live there.**

---

## Community, Social & Continuous Learning

How to plug into the AWS conversation, follow signal-rich voices, and stay current as services ship weekly.

### Official AWS learning & Q&A portals

- [AWS re:Post](https://repost.aws/) — official Q&A staffed by AWS engineers + community
- [AWS Skill Builder](https://skillbuilder.aws/) — official free training (also in [Certifications](#aws-certifications--learning-paths))
- [AWS Workshops](https://workshops.aws/) — guided, step-by-step builds (also in [Certifications](#aws-certifications--learning-paths))
- [AWS re:Invent session catalog](https://reinvent.awsevents.com/) — annual deep architecture + announcements

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
- [AWS Community Builders](https://aws.amazon.com/developer/community/community-builders/) — recognized community experts
- [AWS Heroes](https://aws.amazon.com/developer/community/heroes/) — top community contributors
- AWS-focused Slack / Discord communities — high signal for live ops issues

### Learning platforms (free + paid)

- [freeCodeCamp AWS courses](https://www.freecodecamp.org/news/tag/aws/) — free long-form video courses
- [Tutorials Dojo](https://tutorialsdojo.com/) — cert prep + practice exams
- [A Cloud Guru](https://acloudguru.com/) — structured cert paths (also in [Books, Courses & Newsletters](#books-courses--newsletters))
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

- [Datadog on AWS](https://www.factualminds.com/integrations/datadog-aws/)
- [GitHub Actions on AWS](https://www.factualminds.com/integrations/github-actions-aws/)
- [HashiCorp Vault on AWS](https://www.factualminds.com/integrations/hashicorp-vault-aws/)
- [Kubernetes on AWS EKS](https://www.factualminds.com/integrations/kubernetes-aws-eks/)
- [MongoDB on AWS](https://www.factualminds.com/integrations/mongodb-aws/)
- [Okta on AWS](https://www.factualminds.com/integrations/okta-aws/)
- [Salesforce on AWS](https://www.factualminds.com/integrations/salesforce-aws/)
- [Snowflake on AWS](https://www.factualminds.com/integrations/snowflake-aws/)
- [Stripe on AWS](https://www.factualminds.com/integrations/stripe-aws/)
- [Terraform on AWS](https://www.factualminds.com/integrations/terraform-aws/)

---

## Books, Courses & Newsletters

### Newsletters (free)

- [Last Week in AWS](https://www.lastweekinaws.com/) — Corey Quinn
- [The Cloud Pod](https://www.thecloudpod.tv/) — multi-cloud podcast
- [AWS What's New RSS](https://aws.amazon.com/about-aws/whats-new/recent/feed/)
- [AWS Blog](https://aws.amazon.com/blogs/aws/)
- [FactualMinds Blog](https://www.factualminds.com/blog/) — production AWS guides

### Books

- [AWS Well-Architected Framework whitepaper](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html) (free)
- *AWS in Action* — Manning
- *AWS Cookbook* — Fitch & Mishra (O'Reilly)
- *Architecting for Scale* — Lee Atchison
- *Building Microservices* — Sam Newman (cloud-agnostic but AWS-applicable)

### Courses (paid)

- [A Cloud Guru](https://acloudguru.com/) — cert-focused video courses
- [Stephane Maarek on Udemy](https://www.udemy.com/user/stephane-maarek/) — top-rated AWS cert prep
- [Adrian Cantrill](https://learn.cantrill.io/) — deep-dive cert courses

### YouTube Channels

- [Amazon Web Services](https://www.youtube.com/@amazonwebservices) — official AWS channel
- [AWS Events](https://www.youtube.com/c/AWSEventsChannel) — re:Invent, summits, deep-dive sessions
- [Be A Better Dev](https://www.youtube.com/@BeABetterDev) — AWS tutorials

---

## Conferences & Events

- [AWS re:Invent](https://reinvent.awsevents.com/) — Las Vegas, annual (December)
- [AWS re:Inforce](https://reinforce.awsevents.com/) — security-focused
- [AWS Summits](https://aws.amazon.com/events/summits/) — regional, free
- [AWS Community Days](https://aws.amazon.com/events/community-day/) — community-organized
- [Cloud Next](https://cloud.withgoogle.com/next) (GCP) and [Microsoft Build](https://build.microsoft.com/) — useful for cross-cloud context

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
- [awslabs/mountpoint-s3](https://github.com/awslabs/mountpoint-s3) — high-throughput FUSE client for S3
- [awslabs/aws-sdk-rust](https://github.com/awslabs/aws-sdk-rust) — official Rust SDK
- [aws/karpenter-provider-aws](https://github.com/aws/karpenter-provider-aws) — node autoscaling for EKS

**AI / agents / MCP:**
- [awslabs/mcp](https://github.com/awslabs/mcp) — official MCP servers (50+)
- [awslabs/agent-plugins](https://github.com/awslabs/agent-plugins) — Claude Code / Cursor / Q Developer plugins
- [awslabs/agentcore-samples](https://github.com/awslabs/agentcore-samples) — production patterns for Bedrock AgentCore
- [awslabs/generative-ai-atlas](https://github.com/awslabs/generative-ai-atlas) — GenAI architecture catalog

**Best-practice references:**
- [aws/aws-eks-best-practices](https://github.com/aws/aws-eks-best-practices) — published EKS guide
- [aws-samples/aws-cdk-examples](https://github.com/aws-samples/aws-cdk-examples) — CDK patterns in TS, Python, Java, Go, .NET
- [aws-samples/aws-secure-environment-accelerator](https://github.com/aws-samples/aws-secure-environment-accelerator) — multi-account landing zone
- [aws-samples/aws-cudos-framework-deployment](https://github.com/aws-samples/aws-cudos-framework-deployment) — Cloud Intelligence Dashboards (CUR analytics)

**Developer tooling:**
- [aws/aws-cli](https://github.com/aws/aws-cli) — official CLI
- [aws-actions/configure-aws-credentials](https://github.com/aws-actions/configure-aws-credentials) — OIDC auth from GitHub Actions to AWS
- [awslabs/nx-plugin-for-aws](https://github.com/awslabs/nx-plugin-for-aws) — Nx monorepo plugin for AWS

### Curated awesome lists & community indexes

- [donnemartin/awesome-aws](https://github.com/donnemartin/awesome-aws) — the original, encyclopedic
- [open-guides/og-aws](https://github.com/open-guides/og-aws) — opinionated practitioner's guide (huge inspiration for this repo)
- [dabit3/awesome-aws-amplify](https://github.com/dabit3/awesome-aws-amplify) — Amplify-focused
- [iann0036/AWSConsoleRecorder](https://github.com/iann0036/AWSConsoleRecorder) — record console actions as IaC
- [punkpeye/awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers) — cross-vendor MCP catalog (incl. AWS)

---

## Need Implementation Help?

- [Free AWS Cost Audit](https://www.factualminds.com/aws-cost-audit/)
- [AWS Migration Services](https://www.factualminds.com/services/aws-migration/)
- [AWS Cost Optimization & FinOps](https://www.factualminds.com/services/aws-cloud-cost-optimization-services/)
- [AWS Cloud Security](https://www.factualminds.com/services/aws-cloud-security/)
- [Generative AI on AWS](https://www.factualminds.com/services/generative-ai-on-aws/)
- [AWS Managed Services](https://www.factualminds.com/services/aws-managed-services/)
- [Hire a Dedicated AWS Expert](https://www.factualminds.com/services/hire-a-dedicated-aws-expert/)
- [Browse all 25+ services →](https://www.factualminds.com/services/)

---

## Contributing

Contributions are warmly welcomed. See [CONTRIBUTING.md](CONTRIBUTING.md) for the format.

**Quick rules:**

1. One link per line, format: `[Name](URL) — short description`.
2. Resources must be in active use (no dead repos / dead docs).
3. New top-level categories require an issue first — let's discuss.
4. Self-promotion is fine if the resource is genuinely useful, but disclose any affiliation in the PR description.

| Action | Link |
|---|---|
| 💡 Suggest a resource | [Open a "New Resource" issue](https://github.com/palpalani/aws-open-guide/issues/new?template=new-resource.yml) |
| 🔗 Report a broken link | [Open a "Broken Link" issue](https://github.com/palpalani/aws-open-guide/issues/new?template=broken-link.yml) |
| ⭐ Show appreciation | [Star the repo](https://github.com/palpalani/aws-open-guide) — helps others discover it |

---

## License

<div align="center">

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg?style=for-the-badge)](https://creativecommons.org/licenses/by/4.0/)

This work is licensed under **[Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/)**.

You're free to share and adapt the material for any purpose, even commercially, as long as you give appropriate credit.

---

<sub>Built with care by <a href="https://github.com/palpalani">Palaniappan P</a> · If this guide saved you time, <a href="https://github.com/palpalani/aws-open-guide">⭐ star the repo</a></sub>

</div>
