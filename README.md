# Essential Report Claude Design system

A working component codebase for Essential Research, built to be synced into
Claude Design. Static HTML and CSS, no build step, no dependencies — open any
page straight from the filesystem.

Start with **[DESIGN.md](DESIGN.md)**: brand personality, voice rules for
on-canvas copy, logo usage, which component to reach for, and the anti-patterns
list.

## Layout

```
tokens/
  tokens.css            Single source of truth. The only file allowed a literal value.
  tokens.json           Generated mirror. Never hand-edit.
  sync-tokens.py        Regenerates the mirror.
styles/
  base.css              Reset, document defaults, type primitives.
  components.css        Buttons, forms, cards, quotes, tables, charts, panels.
  patterns.css          Slide canvas, the dot field, page furniture.
components/
  index.html            Every component, in every state it ships in.
pages/
  landing.html          Marketing page.
  report.html           Long-form report.
  slides.html           The seven deck layouts, at true 1280x720 geometry.
  social.html           Feed and carousel frames.
assets/
  logo/                 Three lock-ups, plus a tokenised inline copy and a sprite.
  icons/icons.html      Placeholder icon sprite — see DESIGN.md section 8.
  patterns/             The seven supplied dot-pattern PNGs. Authoritative for print.
tools/
  lint-tokens.py        Fails if anything outside tokens.css holds a literal.
  inline-partials.py    Splices the shared SVG sprites into the pages.
```

## Checks

```bash
python3 tools/lint-tokens.py && python3 tokens/sync-tokens.py --check && python3 tools/inline-partials.py --check
```

Run all three before committing. The first is the one that matters: it enforces
the rule the whole system rests on, which is that no component carries a
hard-coded design value.

## Viewing

Any page opens directly in a browser, but the relative stylesheet links need a
server if your browser blocks local file requests:

```bash
python3 -m http.server 8000
```

## Provenance

Values were extracted from the Essential brand asset pack and from two reference
reports — National Legal Aid (October 2025) and Oxfam Australia (2025). Every
token records its source in a trailing comment, carried through to `tokens.json`.

| Source | Tokens |
|---|---:|
| `[measured]` geometry from a reference render, normalised to 1280x720 | 41 |
| `[sampled]` pixel-sampled from a flat fill | 26 |
| `[theme]` PowerPoint theme XML | 13 |
| `[xml]` slide-level XML | 6 |
| `[pdf]` the report PDF's embedded font table | 2 |
| `[svg]` the supplied logo files | 2 |
| `[INFERRED]` derived, with the basis stated | 48 |
| semantic aliases pointing at other tokens | 8 |
| **total** | **146** |

Read the `[INFERRED]` tags before trusting a value. The source corpus is slides
and PDF only — there is no web or interface precedent in it, so every control,
state, motion value and social dimension was derived rather than extracted.
DESIGN.md section 7 lists the corrections this system makes to earlier
measurements, and section 8 lists what code cannot carry.

Copy in the reference pages is drawn from those two published reports. Figures
are illustrative of the pattern, not fresh population estimates.
