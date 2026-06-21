---
title: "AWS Cost Pitfall: NAT Gateway — Implementation Guide"
slug: /blog/nat-gateway-cost-implementation-aws/
meta_description: "Step-by-step AWS NAT Gateway cost reduction — VPC endpoints, endpoint coverage audit, Terraform patterns, and when architecture consulting pays off."
---

# AWS Cost Pitfall: NAT Gateway — Implementation Guide

NAT Gateway is the most common "surprise bill" line item for teams running workloads in private subnets. FinOps dashboards flag it. **Only architecture changes remove it** — this is the implementation guide behind the [NAT Gateway cost pitfall](https://github.com/palpalani/aws-open-guide/blob/main/use-cases/cost-pitfalls.md#nat-gateway) in AWS Open Guide.

**Dashboards don't delete NAT Gateways.**

## The cost (quick reference)

- **Hourly:** ~$0.045/hour per NAT Gateway per AZ (~$32/mo each; ~$97/mo for 3-AZ HA)
- **Data processing:** $0.045/GB on all traffic through NAT
- **Hidden driver:** Private-subnet traffic to **AWS services** (S3, DynamoDB, ECR, Secrets Manager) still flows through NAT unless you use VPC endpoints

Verify current pricing: [VPC NAT Gateway pricing](https://docs.aws.amazon.com/vpc/latest/userguide/nat-gateway-pricing.html).

## Step 1 — Measure what's using NAT

1. Enable **VPC Flow Logs** (to S3, not CloudWatch — cheaper at volume)
2. Filter: traffic from private subnets → NAT Gateway ENI
3. Group by destination IP/port — identify AWS service prefixes vs internet
4. Cross-check Cost Explorer: `NAT Gateway` → `DataProcessed-Bytes`

**Target:** Quantify GB/month through NAT before changing architecture.

## Step 2 — Gateway endpoints (free wins)

Deploy **gateway endpoints** first — no hourly charge:

| Service | Endpoint type | Impact |
|---------|---------------|--------|
| Amazon S3 | Gateway | High for data lakes, backups, artifact storage |
| DynamoDB | Gateway | High for app data access from private subnets |

Update route tables for private subnets: S3/DynamoDB prefixes → gateway endpoint, not NAT.

## Step 3 — Interface endpoints (paid but often ROI-positive)

**Interface endpoints** (~$7.20/endpoint/AZ/month + data processing) pay back when NAT GB is material:

| Service | Typical private-subnet consumer |
|---------|--------------------------------|
| ECR (api + dkr) | ECS, EKS, CodeBuild |
| Secrets Manager | Lambda, ECS tasks |
| STS | AssumeRole from private compute |
| SSM / SSM Messages | Session Manager, patching |
| CloudWatch Logs | Lambda, containers |
| KMS | Encryption operations |

**Pattern:** One endpoint per service per VPC; shared across AZs via endpoint ENIs in each AZ.

## Step 4 — Terraform implementation checklist

- [ ] `aws_vpc_endpoint` for S3/DynamoDB (gateway) with correct route table associations
- [ ] Interface endpoints with `private_dns_enabled = true` where required
- [ ] Security groups on endpoint ENIs allow HTTPS from workload subnets
- [ ] No hard-coded NAT dependency in user-data or bootstrap scripts
- [ ] Document exceptions (true internet egress still uses NAT or egress-only IGW for IPv6)

## Step 5 — Validate savings

1. Re-run flow log analysis after deploy
2. Compare NAT `DataProcessed-Bytes` week-over-week
3. Account for new endpoint hourly charges in net savings
4. Update [FinOps platform](https://www.factualminds.com/blog/aws-finops-tool-implementation/) dashboards if Vantage/nOps/CloudZero is in use

**Worked example:** 500 GB/mo through NAT for S3/ECR alone ≈ $22.50 processing + idle hourly. Gateway S3 endpoint: $0. ECR interface endpoints in 3 AZs ≈ $65/mo — often net positive above ~200 GB/mo NAT processing to AWS APIs.

## Regional NAT Gateway note

[Regional NAT Gateway](https://docs.aws.amazon.com/vpc/latest/userguide/nat-gateways.html#nat-gateway-regional) simplifies HA but **does not replace endpoint strategy** — S3/ECR traffic still incurs NAT processing without endpoints.

## When FinOps tools stall here

| Tool shows | Implementation delivers |
|------------|-------------------------|
| NAT line item up 40% | Endpoint coverage map + Terraform PRs |
| "Enable VPC endpoints" recommendation | Service-by-service rollout plan |
| EKS cost spike | ECR + S3 endpoints + [Kubecost + architecture fixes](https://www.factualminds.com/blog/kubecost-eks-optimization/) |

**FinOps Foundation Build (4–8 weeks)** includes NAT/endpoint architecture as a standard deliverable when CUR shows material NAT spend.

## Production checklist

- [ ] Flow logs identify top NAT destinations
- [ ] Gateway endpoints for S3 and DynamoDB (if used from private subnets)
- [ ] Interface endpoints for ECR, STS, Secrets Manager, Logs as applicable
- [ ] NAT GB trending down in Cost Explorer after changes
- [ ] Endpoint costs included in net savings calculation
- [ ] Quarterly re-audit in [cost pitfalls cadence](https://github.com/palpalani/aws-open-guide/blob/main/use-cases/cost-pitfalls.md#quarterly-optimization-cadence)

## Related resources

- [Cost pitfalls — NAT Gateway (GitHub)](https://github.com/palpalani/aws-open-guide/blob/main/use-cases/cost-pitfalls.md#nat-gateway)
- [FinOps governance playbook (GitHub)](https://github.com/palpalani/aws-open-guide/blob/main/use-cases/finops-governance.md)
- [Vantage alternative — past visibility](https://www.factualminds.com/compare/vantage-alternative-aws-implementation/)
- [AWS Cost Optimization services](https://www.factualminds.com/services/aws-cloud-cost-optimization-services/)

---

**[Free AWS Cost & Architecture Audit →](https://www.factualminds.com/aws-cost-audit/)**
