#!/usr/bin/env python3
"""Fail if anything outside tokens/tokens.css carries a hard-coded design value.

The rule this repo runs on: tokens/tokens.css is the only file allowed to hold a
literal colour, size, radius, duration or easing curve. Everything else composes
from custom properties. This script enforces that so the rule survives contact
with a deadline.

    python3 tools/lint-tokens.py

Comments are ignored — a note explaining where a value came from is the point of
the token file, not a violation.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOKEN_FILE = ROOT / "tokens" / "tokens.css"

CSS_COMMENT = re.compile(r"/\*.*?\*/", re.DOTALL)
HTML_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)

CHECKS = [
    ("colour literal", re.compile(r"#[0-9A-Fa-f]{3}(?:[0-9A-Fa-f]{3})?\b")),
    ("colour function", re.compile(r"\b(?:rgba?|hsla?|oklch|lab)\s*\(")),
    ("absolute length", re.compile(r"(?<![-\w.])\d+(?:\.\d+)?(?:px|pt|pc|cm|mm|in)\b")),
    ("raw duration", re.compile(r"(?<![-\w.])\d+(?:\.\d+)?m?s\b")),
    ("raw easing", re.compile(r"\bcubic-bezier\s*\(")),
]

# The mask ramp is authored in rgba() because a mask needs an alpha channel and
# the alpha itself is tokenised. Named exemptions only — no blanket skips.
EXEMPT = {
    ("styles/patterns.css", "colour function"),
    ("styles/base.css", "absolute length"),  # .es-visually-hidden clip idiom
}


STYLE_BLOCK = re.compile(r"<style\b[^>]*>(.*?)</style>", re.DOTALL)
STYLE_ATTR = re.compile(r'style="([^"]*)"')


def stylable(text: str, html: bool) -> str:
    """Return only the parts of a file that actually style something.

    For HTML that means <style> blocks and style attributes — prose describing a
    value ("28pt, up to three lines") is documentation, not a hard-coded value,
    and the whole point of this system is that the documentation says the number.
    Line numbers are preserved so the report stays useful.
    """
    if not html:
        return CSS_COMMENT.sub(" ", text)
    lines = text.splitlines()
    keep = [""] * len(lines)
    for match in list(STYLE_BLOCK.finditer(text)) + list(STYLE_ATTR.finditer(text)):
        start = text.count("\n", 0, match.start(1))
        for offset, fragment in enumerate(match.group(1).splitlines()):
            if start + offset < len(keep):
                keep[start + offset] += " " + fragment
    return CSS_COMMENT.sub(" ", "\n".join(keep))


def scan(path: Path) -> list[str]:
    rel = str(path.relative_to(ROOT))
    html = path.suffix == ".html"
    source = stylable(path.read_text(encoding="utf-8"), html)
    problems: list[str] = []
    for line_no, line in enumerate(source.splitlines(), start=1):
        for label, pattern in CHECKS:
            if (rel, label) in EXEMPT:
                continue
            for match in pattern.finditer(line):
                if label == "absolute length" and match.group(0) in {"0px"}:
                    continue
                problems.append(f"{rel}:{line_no}  {label}: {match.group(0).strip()}")
    return problems


def main() -> int:
    targets = [
        *sorted(ROOT.glob("styles/*.css")),
        *sorted(ROOT.glob("pages/*.html")),
        *sorted(ROOT.glob("components/*.html")),
        *sorted(ROOT.glob("*.html")),
    ]
    problems: list[str] = []
    for path in targets:
        if path.resolve() == TOKEN_FILE:
            continue
        problems.extend(scan(path))

    if problems:
        print(f"{len(problems)} hard-coded value(s) found — move them into tokens/tokens.css:\n")
        for problem in problems:
            print(f"  {problem}")
        return 1

    print(f"clean — {len(targets)} file(s) compose from tokens only")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
