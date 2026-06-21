#!/usr/bin/env python3
"""Remove empty **Production Guides:** / **Foundational Guides:** headers from README."""

from __future__ import annotations

import re
from pathlib import Path

EMPTY_TIER = re.compile(
    r"^\*\*(Production Guides|Foundational Guides|Decision Guides|Strategy & playbooks):\*\*\s*\n(?=\n|\*\*)",
    re.MULTILINE,
)


def main() -> None:
    readme = Path(__file__).resolve().parents[1] / "README.md"
    text = readme.read_text(encoding="utf-8")
    prev = None
    while prev != text:
        prev = text
        text = EMPTY_TIER.sub("", text)
    text = re.sub(r"\n{4,}", "\n\n\n", text)
    readme.write_text(text, encoding="utf-8")
    print("Removed empty tier headers")


if __name__ == "__main__":
    main()
