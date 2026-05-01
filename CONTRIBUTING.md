# Contributing to AWS Open Guide

Thanks for considering a contribution. This guide gets better every time someone adds a high-quality resource or fixes a broken link.

## Quick Start

To suggest a new resource without opening a PR, [open a New Resource issue](https://github.com/palpalani/aws-open-guide/issues/new?template=new-resource.yml).

To submit a PR directly:

1. Fork the repo.
2. Find the right section in `README.md`.
3. Add your link in the format below.
4. Open a pull request.

## Entry Format

Every link follows this shape:

```markdown
- [Name](URL) — short, factual description
```

Examples:

```markdown
- [Karpenter](https://karpenter.sh/) — node autoscaling for EKS
- [s5cmd](https://github.com/peak/s5cmd) — fastest S3 CLI
- [Lambda cost optimization guide](https://example.com/post) — pay-per-request vs provisioned breakdown
```

Keep descriptions under 100 characters. State *what it is*, not *why it's great*.

## Inclusion Criteria

A resource should meet **most** of these:

- **Useful** — solves a real problem, teaches a real concept, or saves real money.
- **Maintained** — repos updated within the last 12 months; docs that still match current AWS APIs.
- **Specific** — about AWS, not "cloud in general." Cross-cloud tools are okay if AWS is a first-class citizen.
- **Free or has a free tier** — paid-only resources are okay if they're genuinely best-in-class (e.g., a $39 cert course).

A resource should **not**:

- Be dead, archived, or unmaintained.
- Be a marketing landing page disguised as content.
- Duplicate something already in the guide (unless meaningfully better).

## Categories

The taxonomy follows AWS's own service categories. Top-level changes (new categories, renames) require an issue first so we can discuss.

If your resource doesn't obviously fit, suggest a category in your PR — we'll figure it out together.

## Self-Promotion

Self-promotion is allowed if the resource is genuinely useful and the description is honest. Disclose your affiliation in the PR description. We may ask you to tighten the description.

## Style

- One link per line.
- No emojis in entries (the README has a clean text style).
- US English, sentence case for descriptions.
- Use HTTPS URLs.
- Trailing slash on URLs that have them canonically (most do).

## Status Tags

Some entries carry an inline tag at the end of the description signalling the AWS service's lifecycle state. Stable, generally-available services get **no tag** (the default). Use these four — and only these four:

- `[shutdown]` — fully removed from the AWS portfolio; no access.
- `[sunset]` — end-of-support announced; AWS published a migration path.
- `[maintenance]` — no new customers, no major features (existing customers retain access).
- `[preview]` — preview release; not yet generally available.

Example:

```markdown
- [AWS X-Ray](https://aws.amazon.com/xray/) — distributed tracing; in maintenance per AWS lifecycle docs [maintenance]
```

**Sourcing rule:** any tag added in a PR must cite an official AWS source in the PR description — the [Service Lifecycle docs](https://docs.aws.amazon.com/general/latest/gr/service-lifecycle.html), the [Full Shutdown roster](https://docs.aws.amazon.com/general/latest/gr/full_shutdown_services.html), or an [AWS service changes announcement](https://aws.amazon.com/about-aws/whats-new/). Don't tag a service from secondary commentary alone.

Resist proposing tags beyond these four (e.g., `[recommended]`, `[beta]`, `[high-cost-risk]`). Subjective tags rot fast.

## Broken Links

Found a dead link? [Open a Broken Link issue](https://github.com/palpalani/aws-open-guide/issues/new?template=broken-link.yml) or open a PR removing or updating it.

## Code of Conduct

This project follows the [Contributor Covenant](CODE_OF_CONDUCT.md). Be kind. Disagree on substance, not on people.

## License

By contributing, you agree your contribution is licensed under [CC BY 4.0](LICENSE) — the same license as the rest of the guide.
