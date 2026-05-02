# Playbook: CI/CD for AWS workloads

> Code → tests → build → deploy → verify → roll back if needed. Without long-lived AWS keys, without production-only firefights, without CI as a single point of failure.

**Tags:** `production-ready`

**Status:** ✅ Available

---

## 1. Problem

Shipping software to AWS used to mean an IAM user with admin keys pasted into a CI secret. That door is finally closing — OIDC federation makes it possible to deploy without long-lived credentials. But CI/CD is more than auth: it's tests, builds, IaC plans, staged rollouts, automated rollback, and a story for incidents.

This playbook is the deployment topology that holds up under the realities of AWS: many accounts, many environments, many services, and the requirement that "deploy" means "deploy safely" — never "yolo to prod."

## 2. Constraints

- **Repository host** — GitHub, GitLab, Bitbucket; affects integration patterns
- **Environment count** — dev, staging, prod, per-region; affects pipeline complexity
- **Account topology** — single account vs landing zone with per-environment accounts
- **IaC tool** — Terraform, CDK, Pulumi, SAM, CloudFormation; pipeline differs slightly per tool
- **Test footprint** — unit, integration, end-to-end, load
- **Compliance** — SOX change management, separation of duties, audit trails
- **Recovery time** — how fast must rollback be?
- **Team size** — solo to platform team

## 3. Reference architecture

```
┌──────────────┐
│  Developer   │
│  pushes PR   │
└──────┬───────┘
       │
       ▼
┌──────────────────────────────────────────────────────────────────┐
│                          GitHub                                  │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐            │
│  │  CODEOWNERS  │  │  Branch      │  │  Required    │            │
│  │  review      │  │  protection  │  │  checks      │            │
│  └──────────────┘  └──────────────┘  └──────────────┘            │
└──────────────┬───────────────────────────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────────────────────────┐
│                  GitHub Actions workflow                         │
│                                                                  │
│  1. Checkout                                                     │
│  2. Lint, type-check, unit tests                                 │
│  3. Build artifacts (container, Lambda zip, frontend bundle)     │
│  4. SAST / dependency scan                                       │
│  5. IaC plan (Terraform plan / CDK diff) — POSTED ON PR          │
│  6. Push image to ECR (only on merge to main)                    │
│  7. Deploy to dev → run integration tests                        │
│  8. Deploy to staging → run E2E tests + smoke                    │
│  9. Manual approval gate                                         │
│  10. Deploy to prod (canary / staged ring)                       │
│  11. Auto-rollback on regression                                 │
└──────────────┬───────────────────────────────────────────────────┘
               │
               │ OIDC AssumeRole (no long-lived keys)
               ▼
┌──────────────────────────────────────────────────────────────────┐
│            AWS (per environment, separate accounts)              │
│                                                                  │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐                    │
│  │   Dev    │───▶│ Staging  │───▶│   Prod   │                    │
│  │  account │    │  account │    │  account │                    │
│  └──────────┘    └──────────┘    └──────────┘                    │
│                                       │                          │
│                                       ▼                          │
│                              ┌──────────────────┐                │
│                              │ CloudFormation / │                │
│                              │ Terraform state  │                │
│                              │ change record    │                │
│                              └──────────────────┘                │
└──────────────────────────────────────────────────────────────────┘
```

1. **PR opened** — branch protection requires CODEOWNERS approval, status checks, conversation resolution.
2. **CI on PR** — lint, type-check, unit tests, security scans, IaC plan posted as comment. Read-only AWS role used for plan.
3. **Merge to main** — full deploy pipeline runs. Build artifacts once, deploy that exact artifact through every environment.
4. **OIDC trust** — GitHub Actions assumes a per-environment IAM role via OIDC. No access keys anywhere.
5. **Dev → staging → prod** — each gates on the previous; manual approval before prod (or gated on automated checks if mature).
6. **Canary / staged rollout** — deploy to one region or one cell first; monitor SLIs; auto-rollback on regression.
7. **Audit trail** — every deploy creates a change record; CloudTrail captures the role assumption and all AWS calls.

## 4. Architecture variants

| Variant | When | Notes |
|---------|------|-------|
| **GitHub Actions + OIDC + per-env account (this playbook)** | Most teams in 2024+ | Default; simplest, secure |
| **CodePipeline + GitHub source** | AWS-native, multi-account orchestration | More complex; tighter AWS integration |
| **GitLab CI + OIDC** | Self-hosted GitLab | Same pattern as GitHub Actions |
| **Jenkins on EC2 + OIDC** | Existing Jenkins investment | More ops; OIDC since plugin v4 |
| **Spacelift / Atlantis (Terraform)** | Terraform-heavy, plan-on-PR | Specialised for IaC |
| **Argo CD / Flux (K8s GitOps)** | EKS workloads | Pull-based; cluster reconciles to git state |
| **AWS CDK Pipelines** | CDK shops | Pipeline-as-code in CDK; self-mutating |
| **Buildkite hybrid** | Self-hosted runners on AWS | Control over runner environment |

## 5. Failure modes

Cross-cutting patterns: see [`failure-first.md`](failure-first.md). CI/CD-specific:

### Long-lived credentials leaked

- **What it looks like** — old access key found in compromised laptop / leaked GitHub fork
- **Why it happens** — IAM user keys persisted in CI secrets
- **Recovery** — rotate immediately; revoke; review CloudTrail for misuse; **eliminate the IAM user entirely** — OIDC for CI, IAM Identity Center for humans

### Bad deploy promoted because tests didn't catch it

- **What it looks like** — staging green, prod regression after deploy
- **Why it happens** — test coverage gap; staging not production-like
- **Recovery** — canary deploy with auto-rollback; SLO-based deploy gates (error rate, latency); add the missing test post-incident

### IaC drift between environments

- **What it looks like** — staging works, prod has a subtly different config; new feature breaks
- **Why it happens** — manual change in prod console; environment-specific patches
- **Recovery** — drift detection in CI (Terraform plan, CDK diff) on schedule; alarms; remediation by re-applying IaC; **forbid console writes** in production via SCP

### Deploy halfway, system inconsistent

- **What it looks like** — half the resources updated, half rolled back; service in mixed state
- **Why it happens** — partial CloudFormation rollback; non-idempotent migration steps
- **Recovery** — keep changes small (small CFN stacks, focused commits); separate schema migration from app deploy; idempotent migration scripts

### Pipeline as single point of failure

- **What it looks like** — GitHub Actions outage means no deploys; a hot fix is blocked
- **Recovery** — emergency-deploy runbook (manual `terraform apply` from a hardened workstation, IAM role assumed via SSO, audit record created); **don't** keep a "break-glass" admin user — break glass via approval-gated SSO role

### Rollback path doesn't work

- **What it looks like** — deploy goes bad, rollback is "redeploy previous commit," takes 30 minutes
- **Recovery** — blue/green for stateless; canary with traffic-shift in/out for ALB; CodeDeploy deployment groups; immutable infrastructure means rollback = traffic shift, not redeploy

### Secrets in CI logs

- **What it looks like** — secret printed to logs; logs publicly visible on a public repo
- **Why it happens** — `echo $SECRET`, debugging hack, third-party action that prints env
- **Recovery** — secret masking in CI; pre-commit and CI scan for secrets; rotate any leaked secret; reduce blast radius via short-lived credentials in the first place

### Self-hosted runner compromise

- **What it looks like** — runner has access to many AWS accounts; one bad workflow exfiltrates
- **Recovery** — ephemeral runners (one job, then destroy); per-job-scoped IAM role; runner network-isolated

## 6. Cost model

GitHub Actions:
- 2,000 free minutes/month for private repos on team plans (unlimited on public)
- $0.008/minute for additional Linux usage; more for macOS/Windows
- Self-hosted runners: free per minute, but pay for the EC2/Fargate underneath

Worked example: small team, 200 deploys/month, 8 minutes per deploy = 1,600 minutes/month.

| Line item | Monthly | Notes |
|-----------|---------|-------|
| GitHub Actions minutes (under free tier) | $0 | Free for typical small team |
| ECR storage (50 images × 200MB) | ~$1 | $0.10/GB/month |
| S3 for build artifacts | <$1 | Negligible |
| CloudTrail (free tier) | $0 | First trail free |
| **Total** | **~$1** | Effectively free at this scale |

CodePipeline:
- $1.00 per active pipeline per month (one trial free)
- Plus per-action costs (CodeBuild minutes, etc.)

For larger teams: GitHub Actions costs scale with minutes; self-hosting on Fargate cuts cost at high volume but adds ops.

**Cost traps:**
- **Self-hosted runners idle 24/7** — auto-scale or use ephemeral
- **macOS/Windows runners** — 10× and 2× the Linux rate respectively; only when needed
- **CodeBuild on private VPC without endpoints** — NAT Gateway costs; see [`cost-pitfalls.md`](cost-pitfalls.md#nat-gateway)
- **ECR untagged image accumulation** — lifecycle policy or pay forever
- **Terraform state in S3 without lifecycle** — versions accumulate

## 7. When NOT to use this

- **Solo project, hobby site** — `terraform apply` from your laptop is fine; revisit when more than one person commits
- **Strictly regulated environment with enforced separation of duties** — may need a dedicated CI account, change-advisory-board approval; this playbook still applies but with extra gates
- **Heavy compute / GPU pipelines** — CodeBuild or Batch may be better than CI runners for the heavy step
- **Monorepo at huge scale** — purpose-built tools (Bazel, Buck2, Pants) interact with CI differently

## 8. Alternatives

| Approach | Best for | Tradeoff |
|----------|----------|----------|
| **GitHub Actions + OIDC (this playbook)** | Default 2024+ | Tied to GitHub; OIDC stable |
| **CodePipeline + CodeBuild** | AWS-native end-to-end | More AWS lock-in; clunkier UX |
| **GitLab CI** | Self-hosted GitLab or GitLab.com | Same OIDC pattern as GitHub |
| **CircleCI / Buildkite** | Specialised CI | Vendor cost; OIDC supported |
| **Jenkins** | Existing Jenkins, plugin ecosystem | Heavy ops; consider migration |
| **CDK Pipelines** | CDK-heavy | Self-mutating pipeline; CDK lock-in |
| **GitOps (Argo CD / Flux)** | Kubernetes | Different model; strong fit on EKS |

For X-vs-Y depth: [CodePipeline vs GitHub Actions](https://www.factualminds.com/compare/aws-codepipeline-vs-github-actions/), [Terraform vs CDK](https://www.factualminds.com/blog/terraform-vs-aws-cdk-infrastructure-as-code-decision-guide/), [Pulumi vs Terraform](https://www.pulumi.com/docs/iac/concepts/vs/terraform/).

## 9. Anti-patterns

- **Long-lived AWS access keys in CI secrets** — leak vector; OIDC eliminates the entire class of risk
- **One IAM role with admin in CI** — first compromised workflow = total cloud takeover; per-environment, per-pipeline scoped roles
- **Manual changes in the AWS console** — drift, no audit trail; IaC is the source of truth
- **Single account for all environments** — IAM blast radius; account-per-environment is cheap and worth it
- **Same artifact rebuilt per environment** — version drift; build once, promote artifact through environments
- **Tests skipped under "urgency"** — incidents follow; better to invest in faster tests than to bypass them
- **Deploy = `terraform apply -auto-approve` to prod** — no plan review; no audit log of intent vs change
- **Deploys without a rollback plan** — rollback is a feature, design for it
- **No staged rollout to production** — first bad deploy is a global incident
- **`main` branch direct push allowed** — branch protection on day one
- **Secrets in code or env files committed** — pre-commit hook, CI scan, secrets manager
- **CI minutes scaled by hosting more runners that sit idle** — ephemeral runners or autoscaling
- **No deploy frequency / change-failure rate tracked** — DORA metrics or equivalent; you can't improve what you don't measure
- **Disaster recovery for CI/CD itself never tested** — when CI is down, can you still deploy a critical fix?

For cross-cutting AWS anti-patterns, see [`anti-patterns.md`](anti-patterns.md).

## 10. Production checklist

- [ ] **GitHub branch protection** — required reviews, required status checks, no direct pushes to main, conversation resolution required
- [ ] **CODEOWNERS** for sensitive paths (IaC, IAM, security)
- [ ] **OIDC trust** between GitHub and AWS — no long-lived keys
- [ ] **Per-environment IAM roles**, scoped by `aud` and `sub` to specific repo+branch+environment
- [ ] **Per-environment AWS accounts** (dev / staging / prod / shared services)
- [ ] **IaC plan posted on PR** with diff visible to reviewers
- [ ] **Read-only role for plan**, write role for apply (separation)
- [ ] **CI scans** — secrets (gitleaks / trufflehog), SAST (Semgrep / CodeQL), dependency (Dependabot, npm audit, pip-audit)
- [ ] **Build once, promote** — same artifact deployed to every environment
- [ ] **Deploy gates** — automated tests pass, manual approval for prod (or fully automated with strong SLO gates if mature)
- [ ] **Canary / staged rollout** in production
- [ ] **Auto-rollback** on regression (CloudWatch alarms, deployment hooks)
- [ ] **Drift detection** scheduled (daily Terraform plan in read-only)
- [ ] **CloudTrail** to S3 in every account; auditable change history
- [ ] **Emergency deploy runbook** documented and rehearsed
- [ ] **Pipeline failure alarms** — paging on broken main, broken nightly drift, broken release pipeline
- [ ] **Container image scan** in ECR; block deploy on critical CVEs
- [ ] **ECR lifecycle policy** to prevent unbounded image accumulation
- [ ] **Terraform state in S3** with versioning, lifecycle, backend lock (DynamoDB)
- [ ] **DORA metrics** tracked: deploy frequency, change-lead-time, change-failure rate, MTTR

## 11. References

**Official:**
- [GitHub OIDC with AWS](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services) — official setup guide
- [aws-actions/configure-aws-credentials](https://github.com/aws-actions/configure-aws-credentials) — OIDC action for GitHub Actions
- [AWS CodePipeline Documentation](https://docs.aws.amazon.com/codepipeline/) — full guide
- [AWS CodeBuild Documentation](https://docs.aws.amazon.com/codebuild/) — managed build
- [AWS CodeDeploy Documentation](https://docs.aws.amazon.com/codedeploy/) — deployment, blue/green, canary
- [CDK Pipelines](https://docs.aws.amazon.com/cdk/v2/guide/cdk_pipeline.html) — pipeline-as-code in CDK
- [Terraform AWS provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs) — official docs
- [AWS Control Tower](https://docs.aws.amazon.com/controltower/) — multi-account governance
- [IAM Identity Center](https://docs.aws.amazon.com/singlesignon/) — workforce SSO

**Production guides:**
- [Set up Control Tower for multi-account governance](https://www.factualminds.com/blog/how-to-set-up-aws-control-tower-multi-account-governance/) — landing zone
- [AWS multi-account strategy — landing zone best practices](https://www.factualminds.com/blog/aws-multi-account-strategy-landing-zone-best-practices/) — account structure

**Decision guides:**
- [CodePipeline vs GitHub Actions](https://www.factualminds.com/compare/aws-codepipeline-vs-github-actions/) — CI choice
- [Terraform vs CDK — IaC decision guide](https://www.factualminds.com/blog/terraform-vs-aws-cdk-infrastructure-as-code-decision-guide/) — IaC choice
- [Pulumi vs Terraform](https://www.pulumi.com/docs/iac/concepts/vs/terraform/) — official comparison
- [Pulumi vs CDK](https://www.pulumi.com/docs/iac/concepts/vs/cloud-development-kit/) — official comparison

**OSS tools:**
- [terraform](https://github.com/hashicorp/terraform) — IaC
- [aws-cdk](https://github.com/aws/aws-cdk) — AWS CDK
- [pulumi](https://github.com/pulumi/pulumi) — IaC in real languages
- [atlantis](https://github.com/runatlantis/atlantis) — Terraform plan/apply via PR
- [tflint](https://github.com/terraform-linters/tflint) — Terraform linter
- [checkov](https://github.com/bridgecrewio/checkov) — IaC security scan
- [tfsec](https://github.com/aquasecurity/tfsec) — Terraform security scan
- [gitleaks](https://github.com/gitleaks/gitleaks) — secret scanner
- [trufflehog](https://github.com/trufflesecurity/trufflehog) — secret scanner
- [act](https://github.com/nektos/act) — run GitHub Actions locally
- [Renovate](https://github.com/renovatebot/renovate) — automated dependency updates
- [Dependabot](https://github.com/dependabot) — built into GitHub for dependency updates

---

*See also: [`failure-first.md`](failure-first.md) · [`anti-patterns.md`](anti-patterns.md) · [`decision-trees.md`](decision-trees.md#cicd--how-do-you-ship) · [Developer Tools section in root README](../README.md#developer-tools-devops--cicd).*
