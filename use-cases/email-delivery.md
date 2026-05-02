# Playbook: Email delivery (transactional)

> Send transactional email at scale on AWS with deliverability tracking, bounce/complaint handling, and a feedback loop you can actually act on.

**Tags:** `production-ready` · `high-scale` · `low-cost`

**Status:** ✅ Available

---

## 1. Problem

You need to send email that reaches the inbox — receipts, magic links, password resets, notifications, alerts. Volume ranges from a few thousand a day to millions. The hard part isn't the API call. It's everything around it: getting out of the sandbox, warming an IP, handling bounces and complaints before mailbox providers blacklist you, proving you're not a spammer with SPF/DKIM/DMARC, and being able to answer "did this email actually get delivered?" three months later when a customer asks.

The cost of getting it wrong is invisible until it isn't. Then your password resets stop arriving and the support queue catches fire.

## 2. Constraints

- **Latency** — sender expects send-API to return in <500ms; recipient delivery is best-effort (seconds to minutes)
- **Scale** — 10k/day → 10M/day spans three orders of magnitude with very different architectures
- **Cost ceiling** — typically $0.10–$1.00 per 1k delivered for the AWS-native path; alternatives quoted below
- **Compliance** — CAN-SPAM (US), CASL (Canada), GDPR (EU), unsubscribe must be honoured, sender domain must be authenticated
- **Deliverability** — reputation lives at the sending IP and the domain; both must be warmed and protected
- **Failure tolerance** — transient send failures retried; permanent failures must be suppressed before they tank reputation
- **Region** — SES is regional; pick a region close to recipients or use multi-region for failover

## 3. Reference architecture

```
                                     ┌────────────────────────┐
                                     │  Configuration Set     │
                                     │  (per-stream policy)   │
                                     └───────────┬────────────┘
                                                 │
┌──────────┐    ┌──────────────┐    ┌────────────▼─────────┐
│   App    │───▶│   SES API    │───▶│  Mailbox provider    │
│ (Lambda, │    │  (SendEmail, │    │  (Gmail, Outlook,    │
│  ECS,    │    │  SendBulk)   │    │   Yahoo, Apple)      │
│  EC2…)   │    │              │    └────────────┬─────────┘
└──────────┘    └──────┬───────┘                 │
                       │                         │
                       │ events: send,           │ bounce,
                       │ delivery, open,         │ complaint
                       │ click, bounce,          │ feedback
                       │ complaint, reject       ▼
                       │
                       ▼
                ┌──────────────┐
                │   SNS topic  │ ─────▶ Lambda (suppression list,
                │  (per event  │        billing, alerting)
                │   type)      │
                └──────┬───────┘
                       │
                       ▼
                ┌──────────────┐    ┌──────────┐    ┌──────────┐
                │   Firehose   │───▶│    S3    │───▶│  Athena  │
                │  (buffered)  │    │ (raw +   │    │ (SQL on  │
                │              │    │  Parquet)│    │  events) │
                └──────────────┘    └──────────┘    └──────────┘
```

1. **App → SES** — call `SendEmail` (templated) or `SendBulkEmail` (up to 50 destinations per call). Authenticate the sender domain with SPF, DKIM (Easy DKIM via SES), and DMARC. Always send through a **configuration set** so you can route events.
2. **Configuration set** — controls reputation tracking, IP pool selection, event destinations, suppression list options. One per traffic stream (transactional, marketing, password-reset).
3. **Events → SNS** — SES emits events (`send`, `delivery`, `bounce`, `complaint`, `reject`, `open`, `click`) to an SNS topic. Subscribe Lambda for real-time reactions (suppress, alert) and Firehose for archival.
4. **Firehose → S3** — buffered (60s/5MB) writes to S3, partitioned by event type and date. Use Parquet to keep Athena cheap.
5. **Athena** — queries the event archive. "What's our 30-day bounce rate by domain?" is a 5-second query, not a ticket.
6. **Suppression list** — SES maintains an account-level suppression list automatically; configuration sets can opt in/out. Add custom entries via the `PutSuppressedDestination` API for hard bounces from your own logic.

## 4. Architecture variants

| Variant | When | Cost (10M/mo) | Ops burden | Notes |
|---------|------|---------------|------------|-------|
| SES on shared IPs | <1M/mo, mixed tenants | ~$1k | Lowest | Default; AWS-managed reputation pool |
| SES on dedicated IP | 1M+/mo on a stable cadence | +$25/IP/mo | Medium | Need to warm; need ≥2 for HA per region |
| SES dedicated IP pool | Multiple traffic streams | +$25/IP/mo | Medium | Isolate marketing from transactional |
| SES + 3rd-party fallback | Reputation hedge | $1k + fallback fees | High | Active-active with provider routing |
| SES multi-region | Region failure tolerance | 2× send | High | DKIM keys per region; warm both |

**Cadence vs volume matters more than total volume.** 10M/mo at 13/sec is fine on shared IPs; 10M sent in two hours once a month will be throttled and may be flagged as spam regardless of IP class.

## 5. Failure modes

Generic retry/idempotency/DLQ patterns: see [`failure-first.md`](failure-first.md). Email-specific modes below.

### Hard bounces

- **What it looks like** — `Bounce` event with `bounceType: Permanent` arrives within seconds of send
- **Why it happens** — invalid address, mailbox doesn't exist, domain doesn't exist
- **Detection** — SNS event; aggregate to CloudWatch metric, alarm at >5% rolling 24h
- **Recovery** — add to suppression list immediately; do not retry; remove from your address list

### Soft bounces

- **What it looks like** — `Bounce` event with `bounceType: Transient`
- **Why it happens** — mailbox full, recipient server temporarily unavailable, greylisting
- **Detection** — same as hard bounce
- **Recovery** — SES retries internally for ~14 hours; do not implement your own retry layer for soft bounces

### Complaints (spam reports)

- **What it looks like** — `Complaint` event from feedback loop
- **Why it happens** — recipient hit "Mark as spam"
- **Detection** — SNS event; alarm at >0.1% rolling 24h (AWS will pause sending at sustained 0.5%)
- **Recovery** — suppress immediately and **forever** for that address; investigate the source — usually a bad list, a leaked unsubscribe, or unwanted notifications

### Throttling / send-rate exceeded

- **What it looks like** — `Throttling` exception from SES API; `SendRateExceeded`
- **Why it happens** — exceeded account send rate (varies; check Service Quotas)
- **Detection** — exceptions in app logs; CloudWatch metric `Send` flatlines
- **Recovery** — exponential backoff with jitter (SDK default is reasonable); request quota increase if persistent; queue ahead of SES with SQS for spiky traffic

### Send quota exhausted

- **What it looks like** — daily quota hit; `Throttling` with quota message
- **Why it happens** — exceeded 24-hour send quota
- **Recovery** — quota auto-increases as reputation grows; manual increase via Service Quotas; do not split across accounts to dodge — that's the IP-block fast track

### Reputation drop / sending paused

- **What it looks like** — SES auto-pauses sending; CloudWatch `Reputation.BounceRate` or `Reputation.ComplaintRate` alarm
- **Why it happens** — sustained high bounce or complaint rate
- **Detection** — CloudWatch alarms must exist before this happens, not after
- **Recovery** — find the source (run Athena query for top bounce/complaint domains in last 24h), purge bad addresses, file a SES support case to resume

### IP warming failures

- **What it looks like** — sudden volume increase from a new dedicated IP → spam folder placement
- **Why it happens** — mailbox providers throttle unrecognised IPs that send high volume from day one
- **Recovery** — follow [SES warmup schedule](https://docs.aws.amazon.com/ses/latest/dg/dedicated-ip-warming.html); ramp over 4–6 weeks; mix shared and dedicated during warmup

### Region outage

- **What it looks like** — SES API in primary region returns 5xx/timeouts
- **Recovery** — fail over to secondary region; DKIM keys must already be configured per region; suppression lists do **not** sync across regions (replicate via DynamoDB Global Tables if you maintain your own list)

## 6. Cost model

**Unit cost** at 1M emails/month, mixed traffic, in `us-east-1`:

| Line item | Cost | Notes |
|-----------|------|-------|
| SES send | $100 | $0.10 per 1k emails |
| SES inbound (if any) | $1 | $0.10 per 1k received |
| Attachment data | ~$1 | $0.12/GB outbound; transactional is small |
| Configuration set events → SNS | ~$0.50 | $0.50 per 1M publishes |
| SNS → Firehose | ~$0.30 | $0.50 per 1M deliveries |
| Firehose ingestion | ~$30 | $0.029/GB; events are JSON, ~1KB each |
| S3 storage (1y, Parquet) | ~$5 | Compressed columnar |
| Athena queries | ~$5 | $5 per TB scanned; partitioning matters |
| **Total at 1M/mo** | **~$140** | ~$0.14 per 1k delivered |

**Fixed costs:** $24.95/mo per dedicated IP (need ≥2 for HA = $50/mo minimum if you go dedicated).

**Cost traps:**
- **CloudWatch Logs** for every send → $0.50/GB ingestion. Don't log full message body. See [`cost-pitfalls.md`](cost-pitfalls.md#cloudwatch-logs).
- **Firehose buffering set too low** → more PUTs to S3 → more cost. 60s/5MB is the sweet spot.
- **Athena scanning all-time data for daily reports** → partition by `event_date`; force date predicate in queries.
- **Sending from EC2 in a non-SES region** → cross-region data transfer charges. Use a VPC endpoint or co-locate.
- **Open tracking pixels** → bandwidth on your CDN; turn off open tracking for transactional unless you need it.

**Scaling shape:** SES send cost is linear. Firehose+S3+Athena is sub-linear with Parquet+partitioning. Dedicated IPs are step-function (add a $25/mo IP at thresholds).

## 7. When NOT to use this

- **Heavy marketing automation** with segmentation, journeys, A/B testing, drag-and-drop editor → use a marketing platform (Customer.io, Iterable, Braze). SES is the transport layer, not the marketing tool.
- **<1k emails/month** → a third-party with a free tier (Resend, Postmark) is simpler; the AWS plumbing isn't worth it.
- **Strict EU data residency on senders + recipients + event archive** → confirm SES region availability and configure all event destinations in-region; if uncertain, a EU-headquartered provider may be lower-risk.
- **Inbound email parsing as the core product** (e.g., a help-desk inbox) → SES inbound works but Postmark or Mailgun have richer parsing primitives and webhooks; revisit if you already have SES outbound.
- **You're sending cold outreach** → SES has zero tolerance for spam; reputation will tank on day one. Use a tool built for sales outreach with explicit warmup and inboxing controls.

## 8. Alternatives

| Provider | Cost (1M/mo) | Deliverability | Control | Lock-in | When it wins |
|----------|--------------|----------------|---------|---------|--------------|
| **SES (this playbook)** | ~$140 | High with own IPs | Full | Low (SMTP fallback) | High volume, infra-savvy team |
| **SendGrid** | ~$300+ | High | Medium | Medium | Marketing + transactional combo |
| **Postmark** | ~$120 | Highest for transactional | Low | Low | Pure transactional, no fuss |
| **Mailgun** | ~$200 | High | Medium | Medium | API-first, EU-friendly |
| **Resend** | ~$100 | High | Low | Low | Modern DX, small/mid scale |
| **Self-hosted Postfix on EC2** | ~$50 + ops | Low without effort | Full | Zero | Specific compliance need; usually a mistake |

Cost numbers exclude dedicated IPs and assume in-region sending. Deliverability numbers assume warmup is done correctly on whichever path you pick — provider choice matters less than authentication + list hygiene.

## 9. Anti-patterns

- **Sending direct via SMTP from your app server** — no event stream, no suppression list, no telemetry. SES API gives you all three; SMTP via SES is for legacy clients only.
- **Ignoring bounces and just retrying** — every retry to a hard-bounced address damages reputation. Suppress on first hard bounce, full stop.
- **No DKIM / SPF / DMARC** — Gmail and Yahoo now reject unauthenticated bulk senders outright. This isn't optional in 2024+.
- **Sending from the SES sandbox in production** — sandbox limits are 200/day, recipient must be verified. If you're calling SES from staging, that's fine; if it's leaking into production traffic, you're losing emails silently.
- **No IP warmup before going live on a dedicated IP** — straight to spam folder. Follow the AWS-recommended ramp.
- **Hard-coding the suppression list in your app DB** — SES already maintains one. Use it. Adding your own layer means two sources of truth and inevitable drift.
- **Logging the full message body to CloudWatch** — privacy issue, cost issue, compliance issue. Log `MessageId` + recipient + status; archive bodies (if needed) in encrypted S3 with short retention.
- **One configuration set for everything** — when reputation tanks for one stream, it tanks for all. Separate transactional from marketing from internal alerts.
- **Open tracking on transactional email** — adds latency, adds bandwidth, breaks if recipient blocks images, leaks data. Transactional rarely needs open rates.
- **Treating "delivered" as "read"** — `Delivery` event means the recipient mailbox accepted it. The user may never see it. Different problem; don't conflate.

For cross-cutting AWS anti-patterns (Lambda for >15min jobs, NAT Gateway billing, etc.), see [`anti-patterns.md`](anti-patterns.md).

## 10. Production checklist

Pre-ship gate for an SES integration. If any of these is missing, don't ship.

- [ ] Production access requested and granted (out of sandbox)
- [ ] Sender domain verified
- [ ] **SPF** record published (`v=spf1 include:amazonses.com ~all` or appropriate)
- [ ] **DKIM** enabled (Easy DKIM); CNAMEs published; signing verified for every region you send from
- [ ] **DMARC** record published, starting at `p=none` for monitoring, ramping to `p=quarantine` then `p=reject` after a clean reporting window
- [ ] At least one **configuration set** per traffic stream (transactional / marketing / alerting)
- [ ] **Event destinations** configured: SNS for real-time + Firehose→S3 for archive
- [ ] **Suppression list** mode chosen at account or configuration-set level; tested with a known hard-bounce address
- [ ] **CloudWatch alarms** on `Reputation.BounceRate` (>5%) and `Reputation.ComplaintRate` (>0.1%) — alarms must trigger paging, not just dashboards
- [ ] **Cost alarms** at 1.5×, 2×, 5× expected baseline
- [ ] **Send-rate / quota** documented; SQS buffer in front of SES if your peak QPS exceeds account limit
- [ ] Bounce / complaint webhook handler is **idempotent** (the same event can fire twice)
- [ ] Body templating tested for header injection, newline injection, and Unicode normalisation
- [ ] **Unsubscribe link** in marketing streams (legal requirement) and one-click unsubscribe header
- [ ] Multi-region failover plan documented if business-critical (DKIM keys per region; suppression list replication strategy)
- [ ] PII in event archive minimised; S3 bucket encrypted; lifecycle policy set
- [ ] **Drill** — paused-sending recovery tested at least once; warmup plan written for each dedicated IP

## 11. References

**Official:**
- [SES Documentation](https://docs.aws.amazon.com/ses/) — full SES developer guide
- [Production access request](https://docs.aws.amazon.com/ses/latest/dg/request-production-access.html) — getting out of the sandbox
- [Dedicated IP warming](https://docs.aws.amazon.com/ses/latest/dg/dedicated-ip-warming.html) — official ramp schedule
- [SES sending quotas](https://docs.aws.amazon.com/ses/latest/dg/manage-sending-quotas.html) — daily quota and send rate
- [Configuration sets](https://docs.aws.amazon.com/ses/latest/dg/using-configuration-sets.html) — per-stream policy and event destinations
- [SES event types reference](https://docs.aws.amazon.com/ses/latest/dg/monitor-using-event-publishing.html) — bounce/complaint/delivery payloads
- [SES suppression list](https://docs.aws.amazon.com/ses/latest/dg/sending-email-suppression-list.html) — account-level and configuration-set scopes
- [Email authentication — SPF, DKIM, DMARC](https://docs.aws.amazon.com/ses/latest/dg/email-authentication.html) — official SES auth guide
- [SES Mail Manager](https://aws.amazon.com/ses/mail-manager/) — inbound and outbound email pipelines

**Production guides:**
- [SES e-commerce email marketing](https://www.factualminds.com/blog/aws-ses-ecommerce-email-marketing/) — patterns for retail transactional + marketing
- [Migrate from SendGrid to SES](https://www.factualminds.com/blog/how-to-migrate-from-sendgrid-to-amazon-ses/) — migration playbook with cutover strategy
- [SES at scale — case study (200M+ messages/mo)](https://www.factualminds.com/case-study/aws-ses/) — real-world deployment at high volume

**Decision and migration guides:**
- [SendGrid → SES](https://www.factualminds.com/compare/sendgrid-to-aws-ses/) — comparison and migration cost
- [Mailgun → SES](https://www.factualminds.com/compare/mailgun-to-aws-ses/) — comparison and migration cost
- [Postmark → SES](https://www.factualminds.com/compare/postmark-to-aws-ses/) — comparison and migration cost
- [Resend → SES](https://www.factualminds.com/compare/resend-to-aws-ses/) — comparison and migration cost
- [SparkPost → SES](https://www.factualminds.com/compare/sparkpost-to-aws-ses/) — comparison and migration cost
- [Elastic Email → SES](https://www.factualminds.com/compare/elastic-email-to-aws-ses/) — comparison and migration cost

**OSS tools:**
- [aws-lambda-ses-forwarder](https://github.com/arithmetric/aws-lambda-ses-forwarder) — forward inbound SES email to a different mailbox
- [serverless-ses-template](https://github.com/innovate-technologies/serverless-ses-template) — manage SES templates as code
- [dmarc-report-converter](https://github.com/tierpod/dmarc-report-converter) — parse DMARC aggregate reports to JSON/CSV
- [parsedmarc](https://github.com/domainaware/parsedmarc) — DMARC report parser with Elasticsearch ingestion

**Need help?** [Amazon SES Deliverability service](https://www.factualminds.com/services/aws-ses/) · [SES Migration & Email Delivery](https://www.factualminds.com/services/aws-ses-migration/)

---

*Format rules from [CONTRIBUTING.md](../CONTRIBUTING.md): em-dash separator, descriptions under 100 chars, sentence case, HTTPS URLs.*
