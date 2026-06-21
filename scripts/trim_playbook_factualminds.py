#!/usr/bin/env python3
"""Trim factualminds links: max 4 in §11 References; none in sections 1–10."""

from __future__ import annotations

import re
import sys
from pathlib import Path

MAX_LINKS = 4
REFS_HEADER = re.compile(r"^## 11\. References\s*$", re.MULTILINE)

PRIORITY = (
    (re.compile(r"/compare/|/decide/"), 0),
    (re.compile(r"/services/|/aws-cost-audit"), 1),
    (re.compile(r"/blog/"), 2),
    (re.compile(r"/for/|/case-study/"), 3),
)


def link_priority(url: str) -> tuple[int, int]:
    for pattern, score in PRIORITY:
        if pattern.search(url):
            return (score, 0)
    return (9, 0)


FM_LINE = re.compile(
    r"^[^\n]*\[[^\]]+\]\(https?://[^)]*factualminds\.com[^)]*\)[^\n]*\n?",
    re.IGNORECASE | re.MULTILINE,
)

FM_INLINE = re.compile(
    r"\[[^\]]+\]\(https?://[^)]*factualminds\.com[^)]*\)",
    re.IGNORECASE,
)


def strip_fm_lines(text: str) -> str:
    return FM_LINE.sub("", text)


def trim_references_section(refs_body: str) -> tuple[str, int]:
    pattern = re.compile(
        r"\[[^\]]+\]\((https?://[^)]*factualminds\.com[^)]*)\)",
        re.IGNORECASE,
    )
    matches = list(pattern.finditer(refs_body))
    if len(matches) <= MAX_LINKS:
        return refs_body, 0

    ranked = sorted(matches, key=lambda m: (link_priority(m.group(1)), m.start()))
    keep_starts = {m.start() for m in ranked[:MAX_LINKS]}

    removed = 0
    parts: list[str] = []
    last = 0
    for m in matches:
        if m.start() in keep_starts:
            parts.append(refs_body[last : m.end()])
            last = m.end()
        else:
            line_start = refs_body.rfind("\n", 0, m.start()) + 1
            line_end = refs_body.find("\n", m.end())
            if line_end == -1:
                line_end = len(refs_body)
            removed += 1
            parts.append(refs_body[last:line_start])
            last = line_end
    parts.append(refs_body[last:])
    return "".join(parts), removed


def process_file(text: str) -> tuple[str, int, int]:
    match = REFS_HEADER.search(text)
    if not match:
        # No §11 — strip all factualminds list lines from entire file
        cleaned = strip_fm_lines(text)
        inline_removed = len(FM_INLINE.findall(text)) - len(FM_INLINE.findall(cleaned))
        return cleaned, inline_removed, 0

    before = text[: match.start()]
    refs_and_after = text[match.start() :]

    # Remove factualminds from prose sections 1–10 (list lines and inline markdown links)
    before_clean = strip_fm_lines(before)
    before_clean = FM_INLINE.sub("", before_clean)
    # Collapse awkward whitespace left by stripped inline links
    before_clean = re.sub(r"  +", " ", before_clean)
    before_clean = re.sub(r"\(\s*\)", "", before_clean)
    before_clean = re.sub(r"\s+\.", ".", before_clean)
    before_clean = re.sub(r"\s+,", ",", before_clean)
    before_clean = re.sub(r"\n{3,}", "\n\n", before_clean)

    refs_clean, ref_removed = trim_references_section(refs_and_after)
    inline_removed = len(FM_INLINE.findall(before)) - len(FM_INLINE.findall(before_clean))

    return before_clean + refs_clean, inline_removed, ref_removed


def main() -> int:
    root = Path(__file__).resolve().parents[1] / "use-cases"
    total_inline = 0
    total_refs = 0
    for path in sorted(root.glob("*.md")):
        if path.name.startswith("_") or path.name == "README.md":
            continue
        original = path.read_text(encoding="utf-8")
        updated, inline_r, ref_r = process_file(original)
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            print(f"{path.name}: inline={inline_r}, refs={ref_r}")
            total_inline += inline_r
            total_refs += ref_r
    print(f"Total: inline={total_inline}, refs={total_refs}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
