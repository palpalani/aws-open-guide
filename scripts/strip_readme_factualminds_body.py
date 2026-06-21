#!/usr/bin/env python3
"""Remove factualminds.com links from README body; preserve Need Implementation Help footer."""

from __future__ import annotations

import re
import sys
from pathlib import Path

FOOTER_MARKER = "## Need Implementation Help?"
FM_LINK = re.compile(r"\[([^\]]*)\]\(https://www\.factualminds\.com[^)]*\)")
FM_URL = "factualminds.com"


def strip_fm_from_line(line: str) -> str | None:
    if FM_URL not in line:
        return line

    cleaned = FM_LINK.sub("", line)
    cleaned = re.sub(r"\s*·\s*(?=\s*$)", "", cleaned)
    cleaned = re.sub(r"\s{2,}", " ", cleaned)
    cleaned = re.sub(r" +\n", "\n", cleaned)

    stripped = cleaned.strip()
    if not stripped:
        return None
    if stripped.startswith("-") and "](http" not in stripped and "](https" not in stripped:
        return None
    if stripped.startswith(">") and FM_URL in stripped:
        return None
    if "See also:" in stripped and stripped.rstrip().endswith("See also:"):
        return None
    if "See also:" in stripped:
        parts = stripped.split("See also:")
        tail = parts[1].strip()
        if not tail or tail in ("·", "· ·"):
            return parts[0].rstrip() or None
    return cleaned.rstrip() + ("\n" if line.endswith("\n") else "")


def main() -> int:
    readme = Path(__file__).resolve().parents[1] / "README.md"
    text = readme.read_text(encoding="utf-8")
    footer_idx = text.find(FOOTER_MARKER)
    if footer_idx == -1:
        print("Footer marker not found", file=sys.stderr)
        return 1

    body, footer = text[:footer_idx], text[footer_idx:]
    out_lines: list[str] = []
    for line in body.splitlines(keepends=True):
        if line.endswith("\n"):
            core, nl = line[:-1], "\n"
        else:
            core, nl = line, ""
        result = strip_fm_from_line(core)
        if result is None:
            continue
        if not result.endswith("\n"):
            result = result + nl if nl else result + "\n"
        out_lines.append(result)

    readme.write_text("".join(out_lines) + footer, encoding="utf-8")
    remaining = sum(1 for _ in re.finditer(FM_URL, "".join(out_lines)))
    print(f"README body factualminds references remaining: {remaining}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
