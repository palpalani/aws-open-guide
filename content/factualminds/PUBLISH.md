# Publish checklist — factualminds.com (published 2026-06-21)

All pages below are live under existing `/compare/` and `/blog/` routes. No `/implement/` or `/integrate/` routes — aws-open-guide links use these final URLs.

| Draft file | Final URL |
|------------|-----------|
| `integrate/aws-finops-tool-implementation.md` | `/blog/aws-finops-tool-implementation/` |
| `implement/prowler-security-hub-aws.md` | `/blog/prowler-security-hub-aws/` |
| `implement/prowler-remediation-aws.md` | `/blog/prowler-remediation-aws/` |
| `implement/kubecost-eks-optimization.md` | `/blog/kubecost-eks-optimization/` |
| `compare/prowler-vs-checkov-aws.md` | `/compare/prowler-vs-checkov-aws/` |
| `blog/finops-tools-vs-aws-cost-consulting.md` | `/compare/finops-tools-vs-aws-cost-consulting/` |
| `compare/nops-vs-aws-cost-optimization.md` | `/compare/nops-vs-aws-cost-optimization/` |
| `implement/prosperops-aws-savings-plans.md` | `/blog/prosperops-aws-savings-plans/` |
| `security-compliance/soc-2-prowler-security-hub.md` | `/compare/soc-2-prowler-security-hub/` |
| `compare/vantage-alternative-aws-implementation.md` | `/compare/vantage-alternative-aws-implementation/` |
| `blog/wiz-findings-remediation-aws.md` | `/blog/wiz-findings-remediation-aws/` |
| `blog/nat-gateway-cost-implementation-aws.md` | `/blog/nat-gateway-cost-implementation-aws/` |

## Grep to verify links

```bash
rg "factualminds.com/(integrate|implement|blog/finops-tools-vs|security-compliance/soc-2/prowler)" README.md use-cases/ content/factualminds/
```

UTM parameters on playbook/readme links:

```
?utm_source=aws-open-guide&utm_medium=readme&utm_campaign={section}
?utm_source=aws-open-guide&utm_medium=playbook&utm_campaign={playbook-slug}
```
