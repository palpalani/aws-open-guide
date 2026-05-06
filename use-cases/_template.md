# Playbook: <Use case name>

> One sentence: the workload or outcome — plain language, specific, no hype.

**Tags:** `production-ready` · `high-scale` · `low-cost` · `complex` · `deprecated-pattern`
*(Pick the ones that apply. Remove the rest.)*

**Status:** ✅ Available · 🚧 Draft · ⚠️ Needs update
*(Pick one.)*

---

## 1. Problem

What is the team actually trying to build? Who is the user? What does success look like?

One paragraph, plain English. No AWS service names yet — describe the problem, not the solution.

## 2. Constraints

The non-negotiables that shape every architectural choice. Be specific — numbers beat adjectives.

- **Latency** — e.g., p99 < 200ms; or batch, latency-insensitive
- **Scale** — current and 12-month volume (requests/day, GB/day, tenants)
- **Cost ceiling** — order-of-magnitude target ($/month or $/unit)
- **Compliance** — HIPAA, PCI, SOC2, GDPR, data residency
- **Team size & on-call appetite** — 2-person team vs platform team
- **Failure tolerance** — RTO/RPO targets

## 3. Reference architecture

The default answer. Diagram first, prose second.

```
┌──────────┐    ┌──────────┐    ┌──────────┐
│  Client  │───▶│   API    │───▶│  Worker  │
└──────────┘    └──────────┘    └──────────┘
                      │               │
                      ▼               ▼
                  <store>         <queue>
```

Numbered explanation of each hop:

1. Client → API: protocol, auth, rate limits
2. API → Worker: sync vs async, payload shape
3. Worker → store: write pattern, consistency model

## 4. Architecture variants

When the default isn't right. Compare with a tradeoff table — don't just list options.

| Variant | When to use | Cost | Ops burden | Lock-in |
|---------|-------------|------|------------|---------|
| Default (above) | Most cases | $$ | Low | Medium |
| Variant A | Specific trigger | $ | Medium | Low |
| Variant B | Specific trigger | $$$ | High | High |

## 5. Failure modes

What breaks in production, how to detect it, how to recover. Cross-link to [`failure-first.md`](failure-first.md) for shared patterns (retries, idempotency, DLQs); cover what's specific to this workload here.

For each mode:
- **What it looks like** — symptom in metrics/logs
- **Why it happens** — the underlying cause
- **Detection** — alarm or signal
- **Recovery** — runbook step or auto-mitigation

Cover at minimum: throttling, partial failure, downstream outage, data corruption, region/AZ outage.

## 6. Cost model

Unit economics, not list pricing. Show the math.

- **Per-unit cost** — what each request/event/GB actually costs end-to-end
- **Fixed costs** — anything that costs even when idle
- **Scaling behaviour** — does cost grow linearly, sub-linearly, or step-function?
- **Cost traps** — line items that surprise teams (cross-link [`cost-pitfalls.md`](cost-pitfalls.md))

Worked example with concrete numbers at one volume tier.

## 7. When NOT to use this

Explicit kill criteria. If the reader has any of these conditions, they should bail and use something else.

- Trigger A → use <alternative> instead
- Trigger B → use <alternative> instead
- Trigger C → don't build this on AWS at all

## 8. Alternatives

Same problem, different stack. Side-by-side, not "ours is best."

| Approach | Cost | Deliverability/quality | Control | Lock-in | When it wins |
|----------|------|------------------------|---------|---------|--------------|
| This playbook | … | … | … | … | … |
| Alternative 1 | … | … | … | … | … |
| Alternative 2 | … | … | … | … | … |

## 9. Anti-patterns

Common mistakes specific to this use case. Each: one-line statement → why it bites → the better pattern.

- **Anti-pattern A** — what teams do, why it fails, the better pattern
- **Anti-pattern B** — what teams do, why it fails, the better pattern

For cross-cutting AWS anti-patterns (Lambda for long jobs, NAT Gateway costs, etc.), link to [`anti-patterns.md`](anti-patterns.md) instead of repeating them.

## 10. Production checklist

The pre-ship gate. If any of these are missing, don't ship.

- [ ] IAM least-privilege per component
- [ ] Observability — logs, metrics, traces, structured with workload identifier
- [ ] Alarms on the failure modes from §5
- [ ] Backups and DR tested (RTO/RPO confirmed by drill, not assumed)
- [ ] Scaling limits documented (account-level quotas + per-component)
- [ ] Cost alarms at 1.5×, 2×, 5× expected baseline
- [ ] Runbook for each failure mode in §5
- [ ] Tenant/customer offboarding tested (data deletion, IAM cleanup)

## 11. References

The existing curated links land here. Three tiers, same convention as the root README:

**Official:**
- `[Title](https://...)` — short factual description

**Production guides:**
- `[Title](https://...)` — short factual description

**OSS tools:**
- `[Title](https://...)` — short factual description

**Decision guides** (optional):
- `[X vs Y](https://...)` — short factual description

---

*Format rules from [CONTRIBUTING.md](../CONTRIBUTING.md): em-dash separator, descriptions under 100 chars, sentence case, HTTPS URLs.*
