# Production readiness plan

This document is the **definition of done** for changes to `aws-open-guide`: what must be true before content is production-ready on `main`, how CI enforces it, and what to run locally. For editorial rules (entry format, inclusion criteria, tags), see [CONTRIBUTING.md](CONTRIBUTING.md).

## What “production ready” means here

Readers treat this repo as a **trusted index**. Production ready means:

1. **Links resolve** — URLs in `README.md` and `use-cases/**/*.md` are checked on every relevant PR and on a weekly schedule.
2. **Playbooks are complete** — Each use-case doc follows the [11-section template](use-cases/_template.md); failure modes, “when not to use,” and anti-patterns are non-optional differentiators.
3. **Discoverability stays in sync** — New playbooks appear in [use-cases/README.md](use-cases/README.md), the [Use-Case Playbooks](README.md#use-case-playbooks) block in the root README, and the playbook links inside the collapsible **Table of Contents** `<details>` near the top of [README.md](README.md).
4. **Duplicates are controlled** — Within a file, repeated outbound URLs add noise; contributors follow the [duplicate links](CONTRIBUTING.md#duplicate-links) policy.
5. **Lifecycle tags are evidence-based** — `[shutdown]`, `[sunset]`, `[maintenance]`, and `[preview]` require an official AWS citation in the PR (see [CONTRIBUTING.md — Status tags](CONTRIBUTING.md#status-tags)).

## CI hard gates

| Check | Workflow | When it runs | Failure effect |
|-------|----------|----------------|----------------|
| **Lychee link check** | [.github/workflows/link-check.yml](.github/workflows/link-check.yml) | Push/PR when `README.md`, `PRODUCTION_READINESS.md`, `use-cases/**.md`, `scripts/report_duplicate_md_links.py`, or the workflow itself changes; **weekly** Monday 08:00 UTC; manual `workflow_dispatch` | Fails the PR/push job; scheduled failure opens an automated issue (`lychee/out.md`) for triage; you can also [open a Broken Link issue](https://github.com/palpalani/aws-open-guide/issues/new?template=broken-link.yml) manually |
| **Duplicate Markdown links** | Same workflow, `python3 scripts/report_duplicate_md_links.py` | Same paths as above | **Does not fail CI**; inspect the job log / step summary and clear within-file duplicates when editing |

Maintainers can re-run the workflow from the Actions tab (`workflow_dispatch`) after fixing upstream site outages or transient 429s.

**Note:** Lychee accepts `200`, `206`, `403`, and `429` (see workflow `args`). URLs that return other error codes fail the check.

## Optional local verification

Before opening a PR (especially large README edits):

```bash
python3 scripts/report_duplicate_md_links.py
```

Review the report: fix **within-file** duplicate destinations per [CONTRIBUTING.md](CONTRIBUTING.md#duplicate-links). Repo-wide duplicate counts are informational.

There is **no** pinned `lychee` install in this repo; to mirror CI locally, install [lychee](https://github.com/lycheeverse/lychee) and run with the same paths and flags as [link-check.yml](.github/workflows/link-check.yml), or rely on the PR check.

## Pre-merge checklist — contributors

### Any change to `README.md`

- [ ] New entries use `- [Name](URL) — description` with an **em dash** (`—`), HTTPS, sentence case, description under 100 characters, **no emojis in list items** ([CONTRIBUTING.md — Entry format](CONTRIBUTING.md#entry-format)).
- [ ] Resources meet [inclusion criteria](CONTRIBUTING.md#inclusion-criteria) (maintained, AWS-specific or AWS-first-class, not pure marketing).
- [ ] New **[status tags](CONTRIBUTING.md#status-tags)** include an official AWS source in the PR description.
- [ ] **New top-level README categories** were discussed in an issue first ([CONTRIBUTING.md — Categories](CONTRIBUTING.md#categories)).
- [ ] **Self-promotion**: affiliation disclosed in the PR description ([CONTRIBUTING.md — Self-Promotion](CONTRIBUTING.md#self-promotion)).
- [ ] **Duplicate links**: first canonical link in reading order; elsewhere use fragments or merge bullets per [CONTRIBUTING.md](CONTRIBUTING.md#duplicate-links).
- [ ] If you added **playbook links**, add them under **Use-Case Playbooks** in the collapsible Table of Contents `<details>` near the top of [README.md](README.md).

### Any change to `use-cases/*.md`

- [ ] All **11 sections** present in order ([CONTRIBUTING.md — Adding a Use-Case Playbook](CONTRIBUTING.md#adding-a-use-case-playbook)); do not skip failure modes, when not to use, or anti-patterns.
- [ ] **References (section 11)** use the same list format as the rest of the guide; earlier sections avoid repeating the same `[text](url)` targets (use “see References”).
- [ ] **Tags** at the top use only the vocabulary in CONTRIBUTING; **status** is one of Available / Draft / Needs update.

### New or renamed playbook (additional)

- [ ] Row added to [use-cases/README.md](use-cases/README.md).
- [ ] Bullet + description in root [README.md — Use-Case Playbooks](README.md#use-case-playbooks).
- [ ] Links added under **Use-Case Playbooks** inside the [TOC `<details>`](README.md) block.
- [ ] PR description mentions any **major** reference URL additions (helps reviewers spot scope).

## Pre-merge checklist — maintainers

- [ ] CI green on the PR (link check + informational duplicate report reviewed if noisy).
- [ ] For weekly link-failure issues: triage `lychee/out.md`, update or remove URLs, or add durable excludes only with justification in the workflow comments.
- [ ] **Dependabot** [.github/dependabot.yml](.github/dependabot.yml): merge grouped GitHub Actions bumps so the link workflow stays on supported action versions.

## Operations (ongoing)

| Cadence | Action |
|--------|--------|
| **Weekly** | Link Check cron; if it fails, the workflow opens an automated issue — close it when links are fixed or documented as permanently gone. |
| **On PR** | Contributed changes to scoped paths trigger the same checks. |
| **Ad hoc** | Re-run **Link Check** from Actions if a third-party site had a transient outage. |

## Scope explicitly out of CI

- No spell checker, markdown linter, or line-length gate in this repo (content-only; keep changes reviewable in GitHub).
- No requirement to run `lychee` locally; PR checks are the authority.

---

**Related:** [CONTRIBUTING.md](CONTRIBUTING.md) · [CLAUDE.md](CLAUDE.md) · [use-cases/_template.md](use-cases/_template.md)
