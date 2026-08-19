#!/usr/bin/env python3
"""Splice shared SVG partials into the committed HTML pages.

The pages in this repo are plain static HTML with no build step — they open
straight from the filesystem and Claude Design reads them as-is. The logo and
icon sprites still need to live in one place, so they are stored as partials and
inlined here between marker comments:

    <!-- partial:assets/logo/logo-sprite.html -->
    ...generated content...
    <!-- /partial -->

Run after editing a partial:

    python3 tools/inline-partials.py
    python3 tools/inline-partials.py --check   # exit 1 if any page is stale
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGETS = sorted([*ROOT.glob("pages/*.html"), *ROOT.glob("components/*.html"), *ROOT.glob("*.html")])

BLOCK = re.compile(
    r"(<!-- partial:(?P<path>[^\s]+) -->)(?P<body>.*?)(<!-- /partial -->)",
    re.DOTALL,
)


def splice(text: str) -> tuple[str, int]:
    count = 0

    def replace(match: re.Match[str]) -> str:
        nonlocal count
        count += 1
        partial = (ROOT / match.group("path")).read_text(encoding="utf-8").rstrip()
        return f"{match.group(1)}\n{partial}\n{match.group(4)}"

    return BLOCK.sub(replace, text), count


def main() -> int:
    check = "--check" in sys.argv
    stale: list[str] = []
    touched = 0
    for page in TARGETS:
        original = page.read_text(encoding="utf-8")
        updated, count = splice(original)
        if not count:
            continue
        touched += 1
        if updated == original:
            continue
        if check:
            stale.append(str(page.relative_to(ROOT)))
        else:
            page.write_text(updated, encoding="utf-8")
            print(f"updated {page.relative_to(ROOT)} ({count} partial(s))")
    if check:
        if stale:
            print("stale pages — run: python3 tools/inline-partials.py")
            for name in stale:
                print(f"  {name}")
            return 1
        print(f"all partials in sync across {touched} page(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
