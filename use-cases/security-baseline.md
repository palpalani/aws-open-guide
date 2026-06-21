# Playbook: AWS security baseline

> Continuous posture on AWS — Prowler, Security Hub, Config, and IaC gates — with a remediation workflow that produces auditor-ready evidence, not an eternal finding backlog.

**Tags:** `production-ready` · `complex`

**Status:** ✅ Available

---

## 1. Problem

Security teams need a defensible baseline across AWS accounts: identity boundaries, encryption, logging, network controls, and compliance mapping. Scanners (Prowler, Checkov, Wiz, Orca) and AWS native services (Security Hub, GuardDuty, Config) detect misconfigurations. Most organizations stall translating detections into **remediated infrastructure**, **CI/CD prevention**, and **audit evidence**.

This playbook is the production operating model between "we ran a scan" and "our SOC 2 auditor accepted the control sample."

## 2. Constraints

- **Account count** — 1–500+ via Organizations
- **Compliance frameworks** — CIS, SOC 2, HIPAA, PCI DSS, or internal baseline
- **IaC standard** — Terraform, CDK, CloudFormation, or mixed (higher drift risk)
- **Team model** — central platform security vs embedded champions
- **CNAPP** — Wiz/Orca optional; not required for AWS-native baseline
- **Audit timeline** — Type I vs Type II; drives remediation SLA strictness
- **Change velocity** — daily deploys require shift-left (Checkov) not just periodic Prowler

## 3. Reference architecture

```
                    ┌─────────────────────────────────────┐
                    │         AWS Organizations            │
                    │  Security Hub delegated admin        │
                    └──────────────────┬──────────────────┘
                                       │
     ┌─────────────────────────────────┼─────────────────────────────────┐
     ▼                                 ▼                                 ▼
┌─────────────┐              ┌─────────────────┐              ┌─────────────────┐
│  GuardDuty  │              │  AWS Config     │              │  Inspector v2   │
│  (threat)   │              │  conformance    │              │  (CVE/vuln)     │
└──────┬──────┘              └────────┬────────┘              └────────┬────────┘
       │                              │                                │
       └──────────────────────────────┼────────────────────────────────┘
                                      ▼
                           ┌─────────────────────┐
                           │   AWS Security Hub   │
                           │   (aggregation)      │
                           └──────────┬───────────┘
                                      │
              ┌───────────────────────┼───────────────────────┐
              ▼                       ▼                       ▼
       ┌─────────────┐         ┌─────────────┐         ┌─────────────┐
       │   Prowler   │         │ EventBridge │         │  Audit Mgr   │
       │  (scheduled)│         │  → SNS/PD   │         │  (evidence)  │
       └─────────────┘         └─────────────┘         └─────────────┘

Shift-left (CI/CD):
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   Git PR     │───▶│   Checkov    │───▶│   Deploy     │
│              │    │   (IaC gate) │    │   (OIDC)     │
└──────────────┘    └──────────────┘    └──────────────┘
```

1. **Organizations** with SCPs for region/service guardrails.
2. **Security Hub** aggregates native and third-party findings org-wide.
3. **Prowler** validates runtime posture on schedule; ingests ASFF to Security Hub.
4. **Config** conformance packs operationalize controls with history for audits.
5. **Checkov** blocks insecure IaC before merge.
6. **EventBridge** routes CRITICAL findings to on-call; SLAs tracked in ticketing.
7. **Audit Manager** (optional) collects evidence for SOC 2 control sets.

## 4. Architecture variants

| Variant | When to use | Cost | Ops burden | Lock-in |
|---------|-------------|------|------------|---------|
| **Native + OSS (this playbook)** | Most teams; cost-conscious | $–$$ | Medium | Low |
| **+ Wiz/Orca CNAPP** | Multi-cloud, agentless graph needed | $$$ SaaS | Medium | High |
| **+ Steampipe ad hoc SQL** | Security engineers need custom queries | $ | Low | Low |
| **Consulting baseline sprint** | Audit < 90 days, backlog > 200 | $ one-time | Low during sprint | None |
| **Console-only hardening** | Never for production | $ | High drift | N/A |

## 5. Failure modes

### Finding backlog without owner

- **Symptom:** Security Hub score flat; CRITICAL count unchanged for months
- **Cause:** No SLA; findings not routed to service owners
- **Detection:** Custom insight "unassigned findings > 30 days"
- **Recovery:** Tag-based routing; 2-week remediation sprint; IaC modules for top failures

### IaC vs runtime drift

- **Symptom:** Checkov passes; Prowler fails same control in prod
- **Cause:** Console changes, manual hotfixes, resources outside Terraform
- **Detection:** Config `cloudformation-stack-drift-detection` or periodic Prowler delta
- **Recovery:** Import to IaC or destroy drift; enforce IAM deny on console for prod roles

### Over-permissive scanner roles

- **Symptom:** Prowler role has `AdministratorAccess`
- **Cause:** Quick-start templates in dev never tightened
- **Detection:** IAM Access Analyzer; Prowler self-check
- **Recovery:** Read-only scan role per [Prowler docs](https://docs.prowler.com/)

### Compliance score gaming

- **Symptom:** Score improves; auditor finds controls not operating
- **Cause:** Suppressed findings without exception registry; disabled standards in unused regions
- **Detection:** Audit sample vs Security Hub export
- **Recovery:** Exception registry with expiry; enable standards all in-use regions

### Logging gap

- **Symptom:** Cannot prove who changed security group on date X
- **Cause:** CloudTrail incomplete, no org trail, S3 logging disabled
- **Detection:** Prowler CloudTrail checks; Config `cloud-trail-enabled`
- **Recovery:** Org trail with log file validation; S3 Object Lock or MFA delete on trail bucket

### CNAPP shelfware

- **Symptom:** Wiz/Orca dashboard populated; same CRITICAL for 60 days
- **Cause:** CNAPP purchased without remediation capacity
- **Detection:** Age of top findings in CNAPP export
- **Recovery:** Remediation sprint; integrate CNAPP → Security Hub → single workflow

## 6. Cost model

| Component | Typical monthly cost | Notes |
|-----------|---------------------|-------|
| Security Hub | ~$0.0010/finding ingestion + $0.00003/findings/month storage | Varies by volume |
| Config rules | ~$0.003/rule/account/region | Conformance packs multiply rules |
| GuardDuty | Tiered by VPC/CloudTrail/DNS volume | Often $500–5k/mo at scale |
| Inspector v2 | Per resource scan | EC2, ECR, Lambda |
| Prowler self-hosted | ECS/Lambda compute only | $50–200/mo typical |
| Wiz/Orca (optional) | $50k–200k+/yr enterprise | Not required for baseline |
| Security engineer time | Dominant cost | 0.25–1 FTE for mid-size org |

**Worked example:** 20-account org, native + Prowler baseline ~$2k–4k/mo AWS security services (excluding headcount). One avoided breach or passed audit cycle exceeds tooling cost by orders of magnitude.

## 7. When NOT to use this

- **Single sandbox account, no prod data** — lighter CIS checklist may suffice
- **Air-gapped / isolated enclave** — different control set; Security Hub may not apply
- **Expecting scanner alone to pass audit** — evidence and process required
- **No IaC and no plan to adopt** — runtime-only remediation does not scale; prioritize IaC first
- **Replacing GRC platform with Security Hub** — Audit Manager complements, not replaces, policy docs

## 8. Alternatives

| Approach | Detection | Prevention | Evidence | When it wins |
|----------|-----------|------------|----------|--------------|
| This playbook (SH + Prowler + Checkov + Config) | Strong | Strong (IaC) | Strong | AWS-primary, cost-conscious |
| CNAPP-only (Wiz/Orca) | Very strong | Weak | Medium | Multi-cloud graph priority |
| Manual annual audit | Snapshot | None | Weak | Never for cloud-native prod |
| Big 4 point-in-time | Snapshot | None | Slides | Procurement-driven only |
| AWS Control Tower + LZA | Landing zone guardrails | Partial | Medium | Greenfield org design |

## 9. Anti-patterns

- **Scan without remediation SLA** — backlog becomes normalized risk
- **Console fixes for recurring findings** — fix in Terraform or accept repeat
- **Permanent suppressions** — use time-bound exceptions with approver
- **Security Hub in one region only** — workloads in eu-west-1 invisible to us-east-1 admin
- **Checkov only, no runtime scan** — prod drift undetected
- **Prowler only, no IaC gate** — new debt every merge
- **IAM users for humans in prod** — SSO + Identity Center mandatory

Link: [anti-patterns.md](anti-patterns.md), [ci-cd.md](ci-cd.md) for OIDC and pipeline gates.

## 10. Production checklist

- [ ] CloudTrail org trail, multi-region, log file validation, protected S3 bucket
- [ ] Security Hub enabled org-wide; CIS + FSBP standards active in all in-use regions
- [ ] GuardDuty and Inspector v2 enabled
- [ ] Config recorder on all accounts; conformance packs deployed
- [ ] Prowler scheduled; findings in Security Hub < 24h lag
- [ ] Checkov (or equivalent) on all IaC PRs
- [ ] CRITICAL finding SLA ≤ 7 days; on-call wired via EventBridge
- [ ] IAM Identity Center for human access; no long-lived IAM users
- [ ] KMS CMKs for data at rest; encryption defaults documented
- [ ] Exception registry with expiry and risk owner
- [ ] Quarterly restore/backup drill documented
- [ ] Audit evidence export tested (Config + Security Hub + change tickets)

## 11. References

**Official:**
- [AWS Security Hub](https://aws.amazon.com/security-hub/) — aggregation and standards
- [AWS Config](https://aws.amazon.com/config/) — conformance packs and history
- [AWS Audit Manager](https://aws.amazon.com/audit-manager/) — compliance evidence

**Production guides:**
- [Implement Prowler + Security Hub on AWS](https://www.factualminds.com/blog/prowler-security-hub-aws/?utm_source=aws-open-guide&utm_medium=playbook&utm_campaign=security-baseline) — production checklist and step-by-step setup
- [Who remediates Prowler findings?](https://www.factualminds.com/blog/prowler-remediation-aws/?utm_source=aws-open-guide&utm_medium=playbook&utm_campaign=security-baseline) — remediation workflow and automation patterns
- [SOC 2: Prowler vs Security Hub vs consultant](https://www.factualminds.com/compare/soc-2-prowler-security-hub/?utm_source=aws-open-guide&utm_medium=playbook&utm_campaign=security-baseline) — audit framing
- [10 AWS cloud security best practices](https://www.factualminds.com/blog/10-aws-cloud-security-best-practices-implementation-guide/) — baseline controls implementation
- [Wiz findings remediation on AWS](https://www.factualminds.com/blog/wiz-findings-remediation-aws/?utm_source=aws-open-guide&utm_medium=playbook&utm_campaign=security-baseline) — CNAPP findings to closed risks
- [AWS Cloud Security services](https://www.factualminds.com/services/aws-cloud-security/?utm_source=aws-open-guide&utm_medium=playbook&utm_campaign=security-baseline) — remediation sprints

**OSS tools:**
- [Prowler](https://github.com/prowler-cloud/prowler) — AWS security audit and CIS benchmarks
- [Checkov](https://www.checkov.io/) — IaC static analysis
- [Steampipe](https://steampipe.io/) — SQL queries across AWS security APIs

**Decision guides:**
- [Prowler vs Checkov on AWS](https://www.factualminds.com/compare/prowler-vs-checkov-aws/?utm_source=aws-open-guide&utm_medium=playbook&utm_campaign=security-baseline) — scanning strategy and remediation playbook
- [Prowler documentation](https://docs.prowler.com/) — runtime scanning vs Checkov IaC gates

---

*See also: [`ci-cd.md`](ci-cd.md) (Checkov in pipeline) · [`multi-tenant-saas.md`](multi-tenant-saas.md) (tenant isolation) · [Security & Identity in root README](../README.md#security--identity).*
