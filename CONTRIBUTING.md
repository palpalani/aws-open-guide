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

## Adding a Use-Case Playbook

Use-case playbooks live in [`/use-cases/`](use-cases/) and answer **"how to build X on AWS in production,"** not "links about X." They're the building layer; the service taxonomy in `README.md` is the reference layer.

**Required structure** — every playbook follows the strict 11-section template at [`use-cases/_template.md`](use-cases/_template.md), in this order:

1. Problem
2. Constraints
3. Reference architecture (with ASCII diagram)
4. Architecture variants
5. Failure modes
6. Cost model
7. When NOT to use this
8. Alternatives
9. Anti-patterns
10. Production checklist
11. References

Skipping §5 (Failure modes), §7 (When NOT to use), or §9 (Anti-patterns) defeats the purpose of the format — those are the differentiators from a links list.

**Tags** (pick from this vocabulary, listed at the top of every playbook):

- `production-ready` — battle-tested architecture, used at scale
- `high-scale` — designed for high throughput / concurrency
- `low-cost` — optimised for cost efficiency
- `complex` — non-trivial architecture; not a starter project
- `deprecated-pattern` — historically common but no longer recommended

**Status badges** for tables:

- ✅ Available — published and maintained
- 🚧 Draft — in progress, not yet ready
- ⚠️ Needs update — published but stale; flag for refresh

**Steps to add a playbook:**

1. Copy `use-cases/_template.md` to `use-cases/<your-use-case-slug>.md`.
2. Fill in all 11 sections. Be specific — numbers beat adjectives.
3. The References section follows the same entry-format rules as the rest of the guide: em-dash separator, descriptions under 100 characters, sentence case, HTTPS URLs.
4. Update the table in [`use-cases/README.md`](use-cases/README.md).
5. Add an entry to the Use-Case Playbooks section near the top of the root [`README.md`](README.md) and in its Table of Contents.
6. Open a PR. The link checker validates every URL in `use-cases/*.md` automatically.

**When NOT to add a playbook:** if the use case is fully covered by an existing service section in `README.md` and there's no architectural variation, failure-mode catalog, or cost model worth writing up. Prefer expanding the existing section.

## Duplicate links

**Goal:** one outbound `https://…` (or `http://…`) target per destination **per Markdown file**, unless two bullets truly need distinct anchor text to the same URL (rare). Duplicate outbound links on a single rendered page add noise and redundant anchors without helping readers.

### `README.md`

The README is long and repeats topics across taxonomy, **Decision Guides — X vs Y**, **AWS Glossary**, **Architecture Patterns**, tools, and appendix sections. **Discoverability stays high** by listing the resource where it fits contextually; **duplicate URLs do not** — keep the first HTTPS link in reading order as canonical, then reuse the resource with a same-page fragment link to that section (`[Label](#heading-slug)`). Merge adjacent bullets that pointed at the identical URL.

Heading IDs follow GitHub-flavored Markdown (lowercase, hyphenated). If a fragment link mis-scrolls after a heading edit, fix the slug to match the rendered anchor.

### `use-cases/*.md` playbooks

Treat **References** (section 11) as the canonical place for full `- [Name](URL) — …` bibliography rows. Earlier sections should not repeat the same `[text](url)` for that destination — use plain text, “see References — …”, or a relative link to another playbook section.

### Across files

The same URL may appear in `README.md` and in a playbook (reference layer vs building layer). That is normal ([`CLAUDE.md`](CLAUDE.md)).

### Audit

```bash
python3 scripts/report_duplicate_md_links.py
```

The script reports **within-file** duplicates (these should be cleared when editing) and a short **repo-wide** busiest-URL list (informational only). It does not fail CI; the link checker remains the hard gate for broken URLs.

## Broken Links

Found a dead link? [Open a Broken Link issue](https://github.com/palpalani/aws-open-guide/issues/new?template=broken-link.yml) or open a PR removing or updating it.

## Code of Conduct

This project follows the [Contributor Covenant](CODE_OF_CONDUCT.md). Be kind. Disagree on substance, not on people.

## License

By contributing, you agree your contribution is licensed under [CC BY 4.0](LICENSE) — the same license as the rest of the guide.
