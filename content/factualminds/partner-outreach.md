# Phase 2: Partner outreach playbook

Internal co-marketing guide for FactualMinds. Complement posture only — position as **implementation partner**, not competitor or reseller.

## Target programs

| Vendor | Program | URL | FactualMinds angle |
|--------|---------|-----|-------------------|
| **Prowler** | Partner / AWS Marketplace | https://prowler.com/partners/ | Scanner Remediation Sprint; Security Hub integration |
| **Checkov (Prisma)** | Prisma Cloud partner | https://www.paloaltonetworks.com/partners | DevSecOps IaC remediation; CI/CD gates |
| **Kubecost** | Partner program | https://www.kubecost.com/partners | EKS Cost Optimization SKU + allocation setup |
| **nOps** | Partner network | https://www.nops.io/partners/ | FinOps Foundation Build; architecture execution |
| **Wiz** | Partner program | https://www.wiz.io/partners | Post-CNAPP remediation sprints; Security Hub integration |

## Outreach email template

**Subject:** AWS Select Partner — implementation services for {Vendor} customers

Hi {Name},

I'm {Your Name} at FactualMinds, an AWS Select Tier partner focused on **production implementation** — not another dashboard.

Many {Vendor} customers we meet have strong visibility but stall on remediation: IaC fixes, Security Hub workflows, tagging models, EKS rightsizing. We publish open production playbooks on [AWS Open Guide](https://github.com/palpalani/aws-open-guide) and run fixed-scope sprints (typically 2–8 weeks).

We'd like to explore a **referral or co-marketing** relationship:

- Guest post: "How we close {Vendor} findings in 10 business days"
- Joint webinar: "{Vendor} finds it — we fix it in production"
- Marketplace / partner directory listing as implementation specialist

We're not reselling {Vendor}; we make customers successful after they buy.

Open to a 20-minute call?

{Signature}

## Co-marketing content ideas

1. **Prowler + FactualMinds:** "From CIS score to closed findings — remediation sprint case study"
2. **Checkov + FactualMinds:** "Policy-as-code in CodePipeline — custom rules that stick"
3. **Kubecost + FactualMinds:** "Allocation without savings is a report — EKS architecture fixes"
4. **nOps + FactualMinds:** "When nOps recommends VPC endpoints — who deploys them?"
5. **Wiz + FactualMinds:** "CNAPP findings to closed risks in 10 business days"

## Published content to share with partners

| Page | URL |
|------|-----|
| Prowler vs Checkov | `/compare/prowler-vs-checkov-aws/` |
| Prowler remediation | `/blog/prowler-remediation-aws/` |
| FinOps platform hub | `/blog/aws-finops-tool-implementation/` |
| nOps vs AWS native | `/compare/nops-vs-aws-cost-optimization/` |
| Wiz remediation | `/blog/wiz-findings-remediation-aws/` |
| NAT Gateway guide | `/blog/nat-gateway-cost-implementation-aws/` |

Use UTM `utm_source={vendor}&utm_medium=partner&utm_campaign=co-marketing` when partners share links.

## AWS Marketplace alignment

Consider listing fixed-scope SKUs aligned with security audit and FinOps foundation offerings (reference: competitors like ZSoftly on Marketplace for similar positioning).

## Tracking

| Metric | Tool |
|--------|------|
| Partner referral leads | CRM source field `partner-{vendor}` |
| Co-marketed content traffic | UTM `utm_source={vendor}&utm_medium=partner` |
| Closed-won from partner channel | Quarterly review |

## Status checklist

- [ ] Prowler partner application submitted
- [ ] Prisma/Checkov partner inquiry sent
- [ ] Kubecost partner application submitted
- [ ] nOps partner application submitted
- [ ] Wiz partner inquiry sent
- [ ] First guest post pitch sent (Prowler priority)
- [ ] Month 3 pages published (Vantage, Wiz, NAT Gateway)
