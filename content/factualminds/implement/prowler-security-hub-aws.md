---
title: "Implement Prowler + Security Hub on AWS (Production Checklist)"
slug: /blog/prowler-security-hub-aws/
meta_description: "Production checklist for Prowler and AWS Security Hub — multi-account setup, scheduled scans, finding workflows, and remediation patterns on AWS."
---

# Implement Prowler + Security Hub on AWS (Production Checklist)

Prowler plus AWS Security Hub gives you continuous posture visibility across accounts. This checklist covers the production wiring — not a one-off scan — so findings flow to owners and auditors see deployed controls, not exported spreadsheets.

## Architecture overview

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐
│  Prowler    │────▶│ Security Hub │────▶│ EventBridge/SNS │
│ (scheduled) │     │  (org admin) │     │  → ticketing    │
└─────────────┘     └──────┬───────┘     └─────────────────┘
                           │
                           ▼
                    ┌──────────────┐
                    │ AWS Config   │
                    │ conformance  │
                    └──────────────┘
```

## Prerequisites

- AWS Organizations with all accounts enrolled
- Security Hub delegated administrator account designated
- CIS AWS Foundations Benchmark v3.x and AWS Foundational Security Best Practices enabled
- IAM roles: Prowler scan role per account (read-only + Security Hub write)
- Terraform or CDK for repeatable deployment

## Implementation steps

### 1. Enable Security Hub organization-wide

- Designate admin account in Organizations
- Auto-enable standards for new accounts
- Enable cross-region aggregation if multi-region

### 2. Deploy Prowler scan infrastructure

**Options:**

| Pattern | When |
|---------|------|
| ECS Fargate scheduled task | Weekly full scan, large accounts |
| Lambda + container image | Daily lightweight scan |
| GitHub Actions OIDC | Scan from CI against sandbox/prod read-only role |
| Prowler Cloud (SaaS) | Managed scheduling if self-host ops burden is high |

Store results in S3; push ASFF findings to Security Hub via `prowler aws -M json-asff -B <bucket>` or native integration.

### 3. Integrate native AWS sources

Enable in Security Hub admin:

- GuardDuty
- Inspector v2
- IAM Access Analyzer
- Macie (if data classification required)
- Firewall Manager (if WAF/Network Firewall org policies)

Deduplicate overlapping controls before SLA assignment.

### 4. Finding workflow

- **CRITICAL/HIGH** → PagerDuty or on-call within 4h
- **MEDIUM** → sprint backlog, 30-day SLA
- **LOW** → quarterly hygiene batch
- Use Security Hub custom insights for: unassigned findings, aged > 30 days, by account owner

### 5. Config conformance packs

Deploy packs aligned to your framework:

- `Operational-Best-Practices-for-CIS-AWS-Foundations-Benchmark`
- PCI DSS or HIPAA packs if applicable
- Custom Config rules for org-specific policies

Link Config remediation to Systems Manager Automation where auto-fix is safe.

### 6. Evidence for audits

- Security Hub export to S3 (daily)
- Config compliance timeline
- Change tickets linked to remediation PRs
- AWS Audit Manager assessment (optional, for SOC 2)

## Production checklist

- [ ] Security Hub enabled org-wide with delegated admin
- [ ] CIS + FSBP standards active in all regions in scope
- [ ] Prowler scheduled; last run < 7 days
- [ ] Findings ingested to Security Hub (verify ASFF record count)
- [ ] GuardDuty + Inspector integrated
- [ ] Custom insights for aged and unassigned findings
- [ ] EventBridge → SNS/Slack/PagerDuty on new CRITICAL
- [ ] Config conformance packs deployed
- [ ] IaC modules for top 10 recurring failures
- [ ] Quarterly drill: sample finding → fix → re-scan → close

## Common stall points (and fixes)

| Stall | Fix |
|-------|-----|
| Findings without owner | Account tags + Security Hub workflow automation |
| Same finding reopens weekly | Fix root cause in IaC, not console-only |
| Scan role too permissive | Dedicated read-only role; no admin for scanner |
| Multi-region gaps | Enable standards in every in-use region |
| Audit asks for "proof of fix" | Link Config timeline + merged Terraform PR |

## When to add implementation help

Platform teams often stall at step 5–6 — conformance packs and audit evidence. **FactualMinds Scanner Remediation Sprint** delivers steps 4–6 in two weeks with Terraform handoff.

## Related resources

- [Who remediates Prowler findings?](https://www.factualminds.com/blog/prowler-remediation-aws/)
- [Prowler vs Checkov](https://www.factualminds.com/compare/prowler-vs-checkov-aws/)
- [Security Hub compliance monitoring setup](https://www.factualminds.com/blog/how-to-set-up-aws-security-hub-compliance-monitoring/)
- [AWS Cloud Security](https://www.factualminds.com/services/aws-cloud-security/)
- [Security baseline playbook (GitHub)](https://github.com/palpalani/aws-open-guide/blob/main/use-cases/security-baseline.md)

---

**[Free AWS Cost & Architecture Audit →](https://www.factualminds.com/aws-cost-audit/)**
