#!/usr/bin/env python3
"""Report duplicate Markdown links across aws-open-guide (informational; exit 0).

Normalizes URLs by stripping a trailing slash for grouping only; files keep
canonical slashes per CONTRIBUTING.md.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from collections import defaultdict
from pathlib import Path

LINK_RE = re.compile(r"\[([^\]]*)\]\((https?://[^)\s]+)\)")
SKIP_SUBSTRINGS = frozenset({"https://...", "http://..."})


def iter_md_files(root: Path) -> list[Path]:
    """All *.md under root, excluding common junk."""
    out: list[Path] = []
    for path in root.rglob("*.md"):
        parts = path.parts
        if any(p in (".git", "node_modules", ".venv") for p in parts):
            continue
        out.append(path)
    return sorted(out)


def extract_links(text: str) -> list[tuple[str, str, int]]:
    """Return list of (normalized_url, raw_url, line_no)."""
    found: list[tuple[str, str, int]] = []
    for m in LINK_RE.finditer(text):
        raw = m.group(2)
        if any(s in raw for s in SKIP_SUBSTRINGS):
            continue
        line_no = text[: m.start()].count("\n") + 1
        norm = raw.rstrip("/")
        found.append((norm, raw, line_no))
    return found


def within_file_duplicates(
    links: list[tuple[str, str, int]],
) -> dict[str, tuple[int, list[int]]]:
    """URL -> (occurrence_count, sorted unique line numbers)."""
    by_norm: dict[str, list[int]] = defaultdict(list)
    for norm, _raw, line in links:
        by_norm[norm].append(line)
    return {
        u: (len(lines), sorted(set(lines)))
        for u, lines in by_norm.items()
        if len(lines) >= 2
    }


def global_counts(
    root: Path, files_and_links: list[tuple[Path, list[tuple[str, str, int]]]]
) -> dict[str, list[tuple[str, int]]]:
    """normalized_url -> [(relpath, line_no), ...]"""

    def to_rel(path: Path) -> str:
        try:
            return str(path.relative_to(root))
        except ValueError:
            return str(path)

    acc: dict[str, list[tuple[str, int]]] = defaultdict(list)
    for path, links in files_and_links:
        rel = to_rel(path)
        for norm, _raw, line in links:
            acc[norm].append((rel, line))
    return dict(acc)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="Repository root (default: parent of scripts/)",
    )
    parser.add_argument(
        "--top-global",
        type=int,
        default=15,
        metavar="N",
        help="Show up to N busiest URLs repo-wide (default: 15)",
    )
    args = parser.parse_args()
    root = args.root.resolve()
    if not root.is_dir():
        print(f"Not a directory: {root}", file=sys.stderr)
        return 1

    md_files = iter_md_files(root)
    loaded: list[tuple[Path, list[tuple[str, str, int]]]] = []
    for path in md_files:
        text = path.read_text(encoding="utf-8", errors="replace")
        loaded.append((path, extract_links(text)))

    total_urls = sum(len(links) for _, links in loaded)
    norms = global_counts(root, loaded)
    unique_norms = len(norms)
    multi_global = sum(1 for locs in norms.values() if len(locs) > 1)

    lines_out: list[str] = []
    lines_out.append("# Duplicate Markdown link report\n")
    lines_out.append(f"- Files scanned: **{len(md_files)}**")
    lines_out.append(f"- Total `[text](url)` links: **{total_urls}**")
    lines_out.append(f"- Unique URLs (normalized, trailing `/` stripped for grouping): **{unique_norms}**")
    lines_out.append(
        f"- Normalized URLs with **2+** link occurrences anywhere in the repo: **{multi_global}**"
    )
    lines_out.append("")

    # Within-file section (focus: use-cases, then README)
    lines_out.append("## Within-file duplicates\n")
    playbook_hits = 0
    readme_hits = 0
    other_hits = 0

    def rel(p: Path) -> str:
        try:
            return str(p.relative_to(root))
        except ValueError:
            return str(p)

    within_file_blocks: list[tuple[int, str, dict[str, tuple[int, list[int]]]]] = []
    for path, links in loaded:
        dup = within_file_duplicates(links)
        if not dup:
            continue
        r = rel(path)
        if r.startswith("use-cases/") and r != "use-cases/_template.md":
            playbook_hits += 1
            sort_key = 0
        elif r == "README.md":
            readme_hits += 1
            sort_key = 1
        else:
            other_hits += 1
            sort_key = 2
        within_file_blocks.append((sort_key, r, dup))

    for _sk, r, dup in sorted(within_file_blocks, key=lambda t: (t[0], t[1])):
        lines_out.append(f"### `{r}`\n")
        for norm in sorted(dup, key=lambda u: (-dup[u][0], u)):
            cnt, uniq_lines = dup[norm]
            lines_out.append(
                f"- **{cnt}×** `{norm}` — lines {', '.join(str(n) for n in uniq_lines)}"
            )
        lines_out.append("")

    if playbook_hits == 0 and readme_hits == 0 and other_hits == 0:
        lines_out.append("_No within-file duplicates found._\n")

    # Global busiest (informational)
    top_n = args.top_global
    if top_n > 0:
        lines_out.append("## Busiest URLs repo-wide (normalized)\n")
        ranked = sorted(norms.items(), key=lambda kv: (-len(kv[1]), kv[0]))
        for norm, locs in ranked[:top_n]:
            if len(locs) < 2:
                break
            by_file: dict[str, list[int]] = defaultdict(list)
            for f, ln in locs:
                by_file[f].append(ln)
            summary = "; ".join(
                f"`{f}` ({len(set(by_file[f]))} lines)"
                for f in sorted(by_file.keys())
            )
            lines_out.append(f"- **{len(locs)}×** `{norm}` — {summary}")
        lines_out.append("")

    lines_out.append(
        "_Editorial: avoid duplicate outbound HTTPS links within one file — "
        "`README.md` uses same-page `#fragments` to the first occurrence; playbooks keep URLs "
        "canonical in References (section 11). Repo-wide repeats across files are normal. "
        "See [CONTRIBUTING.md — Duplicate links](CONTRIBUTING.md#duplicate-links)._"
    )
    lines_out.append("")

    report = "\n".join(lines_out)
    print(report)
    summary_file = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_file:
        try:
            with open(summary_file, "a", encoding="utf-8") as fh:
                fh.write(report)
        except OSError as e:
            print(f"Could not append GITHUB_STEP_SUMMARY: {e}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
