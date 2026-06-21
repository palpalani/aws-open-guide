# Playbook: FinOps governance on AWS

> Cost visibility, allocation, commitments, and architecture savings — wired as an operating model, not a one-off spreadsheet exercise.

**Tags:** `production-ready` · `low-cost` · `complex`

**Status:** ✅ Available

---

## 1. Problem

Finance sees an AWS bill. Engineering sees dashboards nobody opens. Leadership wants unit economics and predictable spend. FinOps platforms (Vantage, CloudZero, Finout, nOps) and native tools (Cost Explorer, CUR, Cost Optimization Hub) can show where money goes — but teams stall when tagging is inconsistent, commitments lag architecture changes, and recommendations sit in a queue with no owner.

This playbook defines the **governance layer**: how data flows from AWS billing into decisions engineering executes — with or without third-party FinOps SaaS.

## 2. Constraints

- **AWS spend** — $10k/mo (startup) to $500k+/mo (scale-up); governance overhead must match
- **Account topology** — single account vs Organizations with OUs per env/product
- **Allocation target** — typically 80–90% of spend attributable to team/product/customer
- **Commitment appetite** — finance tolerance for 1- or 3-year Savings Plans
- **Tooling** — native-only vs Vantage/CloudZero/nOps/ProsperOps/Kubecost
- **Engineering capacity** — hours per sprint for cost work (benchmark: 5–10% platform capacity)
- **Compliance** — SOX showback, investor reporting, or internal chargeback

## 3. Reference architecture

```
┌─────────────────────────────────────────────────────────────────┐
│ AWS Organizations │
│ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ │
│ │ Prod │ │ Staging │ │ Dev │ │ Sandbox│ │
│ └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘ │
│ └────────────┴────────────┴────────────┘ │
│ │ tag policies │
└─────────────────────────┼───────────────────────────────────────┘
 ▼
 ┌───────────────────────┐
 │ CUR 2.0 → S3 → Athena │
 │ Cost Categories │
 └───────────┬───────────┘
 │
 ┌─────────────────┼─────────────────┐
 ▼ ▼ ▼
┌───────────────┐ ┌───────────────┐ ┌───────────────┐
│ Cost Explorer │ │ FinOps SaaS │ │ CID dashboards│
│ + Budgets │ │ (optional) │ │ (optional) │
└───────┬───────┘ └───────┬───────┘ └───────┬───────┘
 │ │ │
 └─────────────────┼─────────────────┘
 ▼
 ┌───────────────────────┐
 │ Quarterly optimization│
 │ cadence + architecture│
 │ sprints │
 └───────────────────────┘
```

1. **Tag policies** enforce `Environment`, `Team`, `CostCenter`, `Product` (or your schema) at resource creation.
2. **CUR 2.0** is the source of truth; export daily to S3 with resource-level detail.
3. **Cost Categories** roll tags into finance-friendly dimensions.
4. **Budgets + Anomaly Detection** guard payer account; actions at thresholds.
5. **FinOps platform** (optional) adds UX and automation — not a substitute for tags or architecture fixes.
6. **Quarterly cadence** executes visibility → waste → rightsizing → commitments → architecture ([cost-pitfalls.md](cost-pitfalls.md#quarterly-optimization-cadence)).

## 4. Architecture variants

| Variant | When to use | Cost | Ops burden | Lock-in |
|---------|-------------|------|------------|---------|
| **Native-only (CUR + CE + COH)** | <$30k/mo, strong platform team | $ | Medium | Low |
| **Vantage / CloudZero + native** | Need eng-friendly unit economics | $$ SaaS | Low–medium | Medium |
| **nOps + native** | AWS-heavy, EKS focus | $$ SaaS | Low | Medium |
| **ProsperOps + baseline workshop** | Stable compute, SP automation | $$ SaaS | Low | Medium |
| **Kubecost + EKS** | K8s showback/chargeback | $$ SaaS | Medium | Medium |
| **Consulting sprint + any above** | Execution gap, audit deadline | $ one-time | Low during sprint | None |

## 5. Failure modes

### Tag drift → allocation lies

- **Symptom:** FinOps dashboard shows 40% "unallocated"
- **Cause:** Tag policies not enforced; legacy resources; CloudFormation stacks without tags
- **Detection:** Monthly allocation accuracy report from CUR
- **Recovery:** Tag compliance scan (Config rule `required-tags`); remediate top spend untagged resources first

### Commitment mismatch after migration

- **Symptom:** SP utilization drops; effective savings rate falls
- **Cause:** Graviton migration, serverless refactor, or account consolidation changed compute shape
- **Detection:** Cost Explorer SP utilization report; ProsperOps/nOps alerts
- **Recovery:** Pause autopilot; re-baseline 30 days; exchange or reduce commitments

### Recommendation shelfware

- **Symptom:** Cost Optimization Hub or nOps shows 100+ open recommendations
- **Cause:** No sprint capacity; recommendations lack owner; fear of breaking prod
- **Detection:** Age of recommendations; zero closed in 90 days
- **Recovery:** Fixed-scope architecture sprint; prioritize NAT, idle, rightsizing ([cost-pitfalls.md](cost-pitfalls.md))

### FinOps dashboard ignored

- **Symptom:** Only finance logs in; engineering leads never see showback
- **Cause:** No ritual; metrics not in team reviews; blame culture
- **Detection:** Platform analytics on dashboard usage (if available)
- **Recovery:** Monthly 15-min cost review in eng leads meeting; tie 1 sprint ticket/quarter to cost OKR

### Anomaly without runbook

- **Symptom:** Budget alert fires; nobody knows first step
- **Cause:** Alert wired to email list, not on-call
- **Detection:** MTTR on past anomalies > 4h
- **Recovery:** Runbook: Cost Explorer filter → service → resource → owner tag → rollback/scale

## 6. Cost model

Governance tooling cost is usually **small vs waste found**.

| Component | Typical monthly cost | Notes |
|-----------|---------------------|-------|
| CUR S3 + Athena queries | $50–$500 | Scales with query volume |
| FinOps SaaS (Vantage/CloudZero/nOps) | $500–$5k+ | Tiered by spend |
| ProsperOps | % of savings or flat | Often pays for itself on SP |
| Kubecost (EKS) | $0–$2k+ | Free tier for small clusters |
| Platform engineer time (5% FTE) | $8k–$15k/mo loaded | The real cost — and the real value |

**Worked example:** $100k/mo AWS spend, 15% waste from NAT + idle + over-provisioned Lambda. Fixing waste saves $15k/mo ($180k/yr). FinOps SaaS at $2k/mo ($24k/yr) + 8-week implementation sprint at $45k one-time → ROI in quarter one if savings stick.

Cross-link: [cost-pitfalls.md](cost-pitfalls.md) for line-item traps.

## 7. When NOT to use this

- **Spend <$3k/mo** — Cost Explorer + Budgets sufficient; governance overhead exceeds savings
- **Pre-product-market-fit startup** — optimize for speed; revisit at $10k+/mo sustained
- **Single static workload, one account** — annual rightsizing review may suffice
- **No finance stakeholder** — FinOps without finance partnership becomes unused dashboards
- **Expecting SaaS alone to cut bill** — buy platform after tagging baseline exists, or pay for implementation

## 8. Alternatives

| Approach | Cost | Visibility | Execution | When it wins |
|----------|------|------------|-----------|--------------|
| This playbook (governance + optional SaaS) | $$ | High | Medium–high | Scale-up with eng + finance |
| Native-only, no SaaS | $ | Medium | Depends on team | Strong platform, <$50k/mo |
| FinOps SaaS only | $$ SaaS | High | Low without sprint | Mature team with cost sprint capacity |
| Big 4 cost assessment | $$$$ | Slides | External, slow | Enterprise procurement requirements |
| Ignore until bill spike | $0 | None | Reactive | Never (but common) |

## 9. Anti-patterns

- **Buy CloudZero before tags work** — unit economics on garbage dimensions mislead leadership; fix tag policies first
- **SP autopilot on day one** — commit before architecture stabilizes; lock in wrong shape
- **Cost as finance-only OKR** — engineering must own showback targets
- **One-off "cost week"** — savings revert without quarterly cadence
- **Chargeback without context** — teams game tags; use showback before hard chargeback
- **Ignoring cross-AZ and NAT** — FinOps platform shows compute; network line items dominate surprises

Link cross-cutting patterns: [anti-patterns.md](anti-patterns.md).

## 10. Production checklist

- [ ] Organizations tag policies deployed and compliance monitored (Config)
- [ ] CUR 2.0 export daily to S3; Athena/Glue or CID dashboards
- [ ] Cost Categories map tags to finance dimensions
- [ ] Budgets on payer with actions at 80/100/120% forecast
- [ ] Cost Anomaly Detection subscribed with on-call runbook
- [ ] Cost Optimization Hub enabled all linked accounts
- [ ] Allocation accuracy ≥ 85% (measured monthly)
- [ ] Quarterly cadence scheduled ([cost-pitfalls.md](cost-pitfalls.md#quarterly-optimization-cadence))
- [ ] SP/RI strategy documented; autopilot paused during major migrations
- [ ] FinOps platform (if used) IAM roles least-privilege
- [ ] Engineering leads receive monthly showback (automated or semi-automated)

## 11. References

**Official:**
- [AWS Cost Management documentation](https://docs.aws.amazon.com/cost-management/latest/userguide/) — CUR, Budgets, Cost Categories
- [Cost Optimization Hub](https://aws.amazon.com/aws-cost-management/cost-optimization-hub/) — consolidated recommendations
- [FinOps Foundation](https://www.finops.org/) — community standards and capabilities framework

**Production guides:**
- [Multi-region AWS without doubling costs](https://www.factualminds.com/blog/multi-region-aws-without-doubling-costs/) — DR and replication cost trade-offs
- [Protect AWS infrastructure from cost-based attacks](https://www.factualminds.com/blog/protect-aws-infrastructure-cost-based-attacks/) — abuse and runaway spend controls

**OSS tools:**
- [Cloud Intelligence Dashboards](https://github.com/aws-solutions-library-samples/cloud-intelligence-dashboards-framework) — CUR analytics on AWS
- [CloudBurn](https://cloudburn.io/) — open-source cost policy engine for IaC and live AWS

**Decision guides:**
- [FactualMinds decide hub](https://www.factualminds.com/decide/) — interactive compare and decision trees
- [AWS Cost Optimization & FinOps services](https://www.factualminds.com/services/aws-cloud-cost-optimization-services/) — fixed-scope engagements

---

*See also: [`cost-pitfalls.md`](cost-pitfalls.md) · [`multi-tenant-saas.md`](multi-tenant-saas.md) (cost attribution) · [Cost Management & FinOps in root README](../README.md#cost-management--finops).*
