# Playbook: File upload and processing

> Browser uploads directly to S3 via pre-signed URL; downstream pipeline processes asynchronously without your API ever touching the bytes.

**Tags:** `production-ready` · `low-cost`

**Status:** ✅ Available

---

## 1. Problem

Users upload files — images, videos, PDFs, CSVs, datasets. Sizes range from KB to GB. The naïve solution — POST the file to your API, the API forwards to S3 — wastes compute, eats memory, and fails on large files. Worse, your API now has a uniform-distribution-of-traffic problem driven by the largest file someone uploads, not by request count.

The right pattern: client uploads directly to S3 with a short-lived signed URL. Your API only ever issues the URL and reacts to the upload-complete event. Heavy work happens in a separate pipeline.

## 2. Constraints

- **File size** — KB to multi-GB; affects whether multipart upload is required
- **Volume** — uploads/sec; affects pipeline scaling
- **MIME types accepted** — validation happens after upload, not before
- **Latency from upload to "processed"** — seconds (thumbnails) to minutes (video transcode)
- **Retention** — original kept? processed copy kept? both?
- **Compliance** — virus scanning, content moderation, age verification, geographic residency
- **Cost ceiling** — S3 storage and request costs add up at volume; lifecycle is mandatory at scale

## 3. Reference architecture

```
┌────────────┐                          ┌──────────────┐
│            │   1. POST /uploads       │              │
│  Browser   │─────────────────────────▶│  API Gateway │
│            │                          │   + Lambda   │
│            │   2. {url, fields}       │              │
│            │◀─────────────────────────│              │
│            │                          └──────┬───────┘
│            │                                 │
│            │                                 │ create
│            │                                 │ pending
│            │                                 ▼
│            │                          ┌──────────────┐
│            │                          │  DynamoDB    │
│            │                          │  uploads     │
│            │                          │  table       │
│            │                          └──────────────┘
│            │
│            │   3. PUT (or multipart)
│            │      directly to S3
│            │      with pre-signed
│            │      URL
│            ▼
│      ┌──────────────┐                 ┌──────────────┐
│      │   S3 bucket  │─────────────────│  S3 Event    │
│      │   uploads/   │   ObjectCreated │  Notification│
└──────│   raw/       │                 │   → SQS      │
       └──────────────┘                 └──────┬───────┘
              │                                │
              │                                ▼
              │                         ┌──────────────┐
              │                         │  Validator   │
              │                         │  Lambda      │
              │                         │ - check MIME │
              │                         │ - virus scan │
              │                         │ - update DDB │
              │                         └──────┬───────┘
              │                                │
              │                                ▼
              │                         ┌──────────────┐
              │                         │   Workflow   │
              │                         │  (Step Fns)  │
              │                         └──────┬───────┘
              │                                │
              │           ┌────────────────────┼──────────────────┐
              ▼           ▼                    ▼                  ▼
       ┌──────────────┐ ┌─────────┐      ┌──────────┐       ┌──────────┐
       │ image resize │ │ thumbnail│     │ transcode │      │ extract  │
       │   (Lambda)   │ │ (Lambda) │     │  (ECS)    │      │ (Textract│
       │              │ │          │     │           │      │  /Compre-│
       │              │ │          │     │           │      │   hend)  │
       └──────┬───────┘ └────┬─────┘     └────┬──────┘      └────┬─────┘
              │              │                 │                  │
              └──────────────┴────────┬────────┴──────────────────┘
                                      ▼
                              ┌──────────────┐
                              │  S3 bucket   │
                              │  processed/  │
                              └──────────────┘
                                      │
                                      ▼
                              ┌──────────────┐
                              │  DynamoDB    │
                              │  status=done │
                              └──────────────┘
```

1. **Client requests upload URL** — `POST /uploads` with file metadata (name, size, type). API validates (size limits, allowed types), creates `(upload_id, status=pending, owner)` in DynamoDB, generates a pre-signed URL or pre-signed POST policy (see References — Official — S3 pre-signed URLs). Returns to client.
2. **Client uploads to S3** — `PUT` for files <100MB; multipart upload for larger. The bytes never touch your API.
3. **S3 event** — `ObjectCreated` triggers an SQS message (event notification → SQS).
4. **Validator** — Lambda picks up the event, validates content (MIME sniff, file headers, virus scan via ClamAV-on-Lambda or GuardDuty Malware Protection for S3), updates DynamoDB.
5. **Processing workflow** — Step Functions orchestrates parallel transforms (resize, transcode, extract). Each step writes to `processed/` prefix. Status updated as each completes.
6. **Client polls or receives webhook** — final status from DynamoDB.

For multipart uploads, the client requests **multipart pre-signed URLs** for each part; coordination via DynamoDB.

## 4. Architecture variants

| Variant | When | Notes |
|---------|------|-------|
| **Pre-signed PUT** | Single-request upload <100MB | Simplest |
| **Pre-signed POST policy** | HTML form uploads with field constraints | Supports browser progress; more setup |
| **Multipart pre-signed URLs** | Files >100MB or unreliable networks | Required >5GB; resumable |
| **CloudFront upload distribution** | Global users, large files | Edge upload acceleration |
| **S3 Transfer Acceleration** | Cross-region high-volume | Surcharge per GB; faster from far away |
| **AWS Transfer Family** | SFTP/FTPS legacy clients | Managed SFTP server |
| **Direct upload to other regions** | Data residency requirements | Region-specific buckets and signers |

For processing:

| Variant | When |
|---------|------|
| **S3 → SQS → Lambda** | Default; processing <15min |
| **S3 → SQS → ECS Fargate** | Long transcodes, heavy CPU/GPU |
| **S3 → EventBridge → Step Functions** | Multi-step parallel pipelines |
| **S3 → Lambda direct** | Simple, low-volume — but no DLQ; **avoid in production** |

## 5. Failure modes

Cross-cutting patterns: see [`failure-first.md`](failure-first.md). File-upload-specific:

### Upload abandoned mid-flight

- **What it looks like** — DynamoDB has `pending` records that never transition to `done`
- **Why it happens** — user closes tab, network dies, mobile app backgrounded
- **Recovery** — TTL on `pending` records (24h); reaper sweeps and marks `abandoned`; for multipart, abort incomplete uploads (S3 lifecycle rule for `AbortIncompleteMultipartUpload` after N days, otherwise the parts cost money forever)

### File doesn't match metadata

- **What it looks like** — client claimed `image/jpeg`, actually uploaded an executable
- **Why it happens** — client lies; pre-signed URL doesn't enforce content
- **Recovery** — validator sniffs MIME from bytes (magic numbers), not from `Content-Type` header; reject mismatches

### Malicious upload

- **What it looks like** — malware, child sexual abuse material, executable disguised as image
- **Why it happens** — public upload endpoints will be abused
- **Detection** — virus scan on every upload (GuardDuty Malware Protection for S3, or ClamAV on Lambda); image moderation (Rekognition Content Moderation); content hashes against known-bad lists
- **Recovery** — quarantine bucket for flagged content; legal/compliance escalation path; never serve flagged content publicly

### Massive file uploaded to crash you

- **What it looks like** — someone signs URL for a 5GB file with intent to consume your processing budget
- **Recovery** — pre-signed URL includes content-length-range condition; reject mismatches; per-user quotas; cost alarm at upload pipeline level

### Pre-signed URL leaked / replayed

- **What it looks like** — same upload happens multiple times from different IPs
- **Why it happens** — URL shared, snooped, scraped
- **Recovery** — short expiry (15 minutes typical); pre-signed POST policy with key prefix matching user ID; per-user upload-rate limit; one-time-use semantics via key-uniqueness check

### Processing pipeline broken; backlog grows

- **What it looks like** — DLQ depth growing; users see `processing` for hours
- **Recovery** — see [`failure-first.md`](failure-first.md#3-dead-letter-queues-dlqs); per-step DLQs in Step Functions; replay-from-DLQ runbook

### Region failure

- **What it looks like** — primary region S3 unavailable; uploads fail; processed pipeline stalled
- **Recovery** — Cross-Region Replication for raw uploads if uptime SLA demands it; signer in second region; processing pipeline replicated; client retry with regional fallback URL

## 6. Cost model

Worked example: 1M uploads/month, average 5MB, all images with thumbnail + resize.

| Line item | Monthly | Notes |
|-----------|---------|-------|
| API Gateway requests (issue URL) | ~$3.50 | $3.50/M |
| Lambda issue (1M × 100ms × 256MB) | ~$1 | Tiny |
| S3 PUT (1M originals + 2M derivatives) | ~$15 | $0.005/k requests |
| S3 storage (5MB × 1M = 5TB raw + ~2TB derivatives, 30d) | ~$170 | $0.023/GB/month standard |
| SQS requests | ~$1 | Marginal |
| Lambda processing (1M × 5s × 1GB) | ~$85 | Bulk of compute |
| DynamoDB on-demand | ~$5 | Status updates |
| Egress (when downloaded; assume 50% downloaded once) | varies | $0.09/GB to internet |
| **Total (excluding egress)** | **~$280** | ~$0.28 per upload |

**Scaling shape:** linear with upload count. **S3 storage is the biggest line item over time** — lifecycle is mandatory.

**Cost traps:**
- **No lifecycle policy** — uploads accumulate forever; bill grows monthly
- **Standard storage class for everything** — old originals belong in IA or Glacier
- **Multipart uploads not aborted** — abandoned parts charged forever; S3 lifecycle `AbortIncompleteMultipartUpload`
- **Processing each variant in series** — Step Functions parallel branches process simultaneously; cheaper wall clock and same total compute
- **No CDN for downloads** — egress directly from S3 is expensive at scale; see [`cost-pitfalls.md`](cost-pitfalls.md#egress-to-internet)

## 7. When NOT to use this

- **Tiny files (<100KB) at low volume** — direct API upload is simpler; the indirection isn't worth it
- **Real-time streaming uploads** — IVS or MediaLive for live video; this pattern is for file at rest
- **Sensitive data with strict residency that S3 can't satisfy** — verify region availability and pre-signed URL behavior
- **You need to validate before storage** — pre-signed URL means file is in S3 before validation; if "no bad bytes shall ever land in S3" is a hard requirement, proxy through API (and accept the cost)

## 8. Alternatives

| Approach | Best for | Tradeoff |
|----------|----------|----------|
| **Pre-signed URL → S3 (this playbook)** | Default | Validate after, not before |
| **API proxies to S3** | Strict pre-validation | API memory/CPU bottleneck; large files struggle |
| **Tus.io resumable uploads on EC2** | Resumable, custom protocol | Self-hosted; multipart S3 covers most cases |
| **Uppy + Companion** | Rich client UX | Adds JS lib; works with S3 multipart |
| **Filestack / Cloudinary / Mux** | Off-the-shelf SaaS for media | Vendor cost; faster to ship |
| **AWS Transfer Family (SFTP)** | Legacy SFTP clients | Per-endpoint hourly cost |

## 9. Anti-patterns

- **Uploading through your API** — bytes hit your compute; OOM, cost, throughput problem
- **Long-lived pre-signed URLs** — leakage = abuse; default to 15-minute expiry
- **Trusting `Content-Type` from client** — sniff bytes, not headers
- **No size limit in the pre-signed POST policy** — `content-length-range` condition bounds the upload
- **No lifecycle policy on the bucket** — storage grows forever
- **Standard storage for all derivatives** — thumbnails are cheap to regenerate; intelligent-tiering or lifecycle to IA
- **Processing pipeline coupled to upload bucket directly** — a poison upload (huge file, malware) blocks the pipeline; SQS in front of the pipeline
- **Public bucket for processed assets** — use CloudFront with Origin Access Control; never serve directly
- **Same bucket for raw and processed** — separate buckets simplify lifecycle, IAM, and incident response
- **No virus scan** — public upload endpoints attract malware; assume your bucket is a target
- **Returning S3 URL to client for download** — pre-signed download URL or CloudFront signed URL; don't expose direct S3 URLs

For cross-cutting AWS anti-patterns, see [`anti-patterns.md`](anti-patterns.md).

## 10. Production checklist

- [ ] **Pre-signed URL expiry ≤15 minutes**
- [ ] **`content-length-range`** in POST policy or URL query bounded
- [ ] **Per-user upload rate limit** at API; daily/hourly cap
- [ ] **MIME sniffing** in validator (don't trust client `Content-Type`)
- [ ] **Virus / malware scan** on every upload (GuardDuty Malware Protection or ClamAV)
- [ ] **Content moderation** for user-generated images/video (Rekognition, Comprehend)
- [ ] **Quarantine bucket** for flagged content; access restricted; legal escalation runbook
- [ ] **Separate buckets** for raw uploads and processed derivatives
- [ ] **S3 lifecycle** — `AbortIncompleteMultipartUpload` after 7d; transition originals to IA after 30–90d; expire derivatives older than retention window
- [ ] **Server-side encryption** with KMS (or SSE-S3 for low-sensitivity)
- [ ] **Bucket policy** denies public access; account-level Block Public Access on
- [ ] **CloudFront with OAC** for downloads; signed URLs for private content
- [ ] **DynamoDB pending-record TTL** + reaper for abandoned uploads
- [ ] **DLQ on every processing step** with depth alarm
- [ ] **Cost alarms** on S3 storage growth and Lambda processing minutes
- [ ] **Drill** — upload an oversized file, malformed file, malware sample (in non-prod) — confirm rejection paths fire

## 11. References

**Official:**
- [S3 pre-signed URLs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/PresignedUrlUploadObject.html) — official guide
- [S3 multipart upload](https://docs.aws.amazon.com/AmazonS3/latest/userguide/mpuoverview.html) — for files >100MB
- [S3 event notifications](https://docs.aws.amazon.com/AmazonS3/latest/userguide/NotificationHowTo.html) — to SQS, SNS, EventBridge, Lambda
- [GuardDuty Malware Protection for S3](https://docs.aws.amazon.com/guardduty/latest/ug/malware-protection-s3.html) — managed virus scan
- [Rekognition Content Moderation](https://docs.aws.amazon.com/rekognition/latest/dg/moderation.html) — image/video moderation
- [Textract Documentation](https://docs.aws.amazon.com/textract/) — OCR and document extraction
- [MediaConvert Documentation](https://docs.aws.amazon.com/mediaconvert/) — video transcoding
- [S3 lifecycle rules](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lifecycle-mgmt.html) — storage class transitions
- [CloudFront Origin Access Control](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-restricting-access-to-s3.html) — secure S3 distribution

**Production guides:**
- [Building a data lake on S3 + Glue + Athena](https://www.factualminds.com/blog/building-a-data-lake-on-aws-s3-glue-athena-architecture/) — when uploads feed analytics

**OSS tools:**
- [Uppy](https://github.com/transloadit/uppy) — modular file uploader with S3 multipart
- [aws-sdk-s3-request-presigner](https://github.com/aws/aws-sdk-js-v3/tree/main/packages/s3-request-presigner) — generate pre-signed URLs (Node.js)
- [boto3 generate_presigned_url](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/generate_presigned_url.html) — Python SDK
- [clamav-lambda-layer](https://github.com/widdix/aws-s3-virusscan) — ClamAV antivirus on S3

---

*See also: [`async-jobs.md`](async-jobs.md) · [`event-driven.md`](event-driven.md) · [`failure-first.md`](failure-first.md) · [`cost-pitfalls.md`](cost-pitfalls.md).*
