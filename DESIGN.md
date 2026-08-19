# Essential Research — design system

Australian English throughout, in the code and in the output.

This is a working component codebase, not a specification. If a rule matters, it
lives in a token or a class, not in this file. What is here is the part code
cannot hold: why the system is shaped this way, which component to reach for,
and what this brand never does.

| | |
|---|---|
| Tokens | [`tokens/tokens.css`](tokens/tokens.css) — the only file allowed to hold a literal value |
| Token mirror | [`tokens/tokens.json`](tokens/tokens.json) — generated, never hand-edited |
| Components | [`styles/components.css`](styles/components.css), rendered in [`components/index.html`](components/index.html) |
| Page furniture | [`styles/patterns.css`](styles/patterns.css) |
| Reference pages | [`pages/landing.html`](pages/landing.html), [`pages/report.html`](pages/report.html), [`pages/slides.html`](pages/slides.html), [`pages/social.html`](pages/social.html) |
| Checks | `python3 tools/lint-tokens.py`, `python3 tokens/sync-tokens.py --check`, `python3 tools/inline-partials.py --check` |

---

## 1. Brand personality

Essential Research sells defensibility. Everything else follows from that.

**Evidence, not opinion.** Every claim carries its working — the question as
fielded, the base, the n. A number without its base is a claim, not a finding.
The design's job is to make that discipline visible at a glance.

**Plain, not plain-spoken.** The tone is direct and unhedged in its
recommendations, and precisely hedged in its findings. Those are different
registers and the system keeps them apart: recommendations get imperative
headings, findings get the calibrated ladder in §3.

**Flat, not decorated.** There is not one shadow in the entire source corpus.
Surfaces separate by fill and by hairline. `--es-elevation-raised` is
deliberately `none`; if you find yourself wanting a shadow, you want a different
surface token.

**One argument per surface.** One finding per slide, one idea per social frame,
one decision per page. If the title cannot summarise what is below it, that is
two surfaces.

---

## 2. The three colours that carry meaning

The palette is small and each part of it has a job. Reaching for a colour
because it looks good is how a system stops meaning anything.

**Cyan is a voice, navy is a surface.** This is the brand's defining move and
the one most often got wrong. Headings run cyan on light surfaces
(`--es-colour-text-heading`). Navy is what you build the surface out of —
covers, dividers, panels, the first chart series. A navy heading on white is not
this brand.

**Gold marks the participant voice.** `--es-colour-surface-highlight` is not a
general accent. It marks where a real person is speaking or being counted:
audience badges, the public research phase, the verdict pills on message
testing, the eyebrow on an inverse surface. It also carries focus, because it is
the only colour that clears both the light and the dark surfaces this system
uses.

**Coral belongs to the scale, not the palette.** `--es-colour-scale-3` and
`-scale-2` exist for the negative end of a Likert battery. Coral outside a chart
is a mistake.

Two colour systems for data, and they never mix in one chart:

- **Categorical** (`--es-colour-data-1` … `-5`) compares named audiences.
- **Ordered** (`--es-colour-scale-5` … `-1`) runs a Likert or attention battery.

---

## 3. Voice and tone for on-canvas copy

These are measured from the source reports, not invented. The full rules and
their measurements are in the reference pack's `voice.md`; what follows is what
you need while writing into a component.

**Titles state the finding.** A complete sentence carrying the insight, never a
topic label.

> Yes — *There is shock that legal aid is only accessible to eight per cent of people, and this makes people realise how limited the service is*
> No — *Accessibility of Legal Aid*

Budget: 28pt, three lines, roughly 140 characters. The measure comes from the
canvas content column, not from a `max-width` — see the note on `.es-title` in
[`styles/base.css`](styles/base.css).

**The two-tone title** is for message testing only: frame name in ink, finding
in cyan. Use `.es-title__frame`.

**Attribution format is fixed.** Public participants read `Gender, Age band,
Qualifier` — *Female, 36-55, Receives Centrelink*. Stakeholders are attributed
simply as *Stakeholder*. Never name a participant. Never attribute a quote to an
organisation.

**Hedges are calibrated and they do real work.** In descending order: *most* or
*the majority*, then *many*, then *some*, then *a few*. *Participants note*
means reported; *the research found* means Essential's own conclusion. Never upgrade a hedge to
make a finding sound stronger, and never put a percentage on a qualitative
finding.

**Recommendations are directive.** Imperative headings and concrete actions —
*The campaign needs to*, *What can be shared*. Not *it could be considered
that*. The client is paying for a position.

**Quotes support, they never introduce.** A verbatim carries a finding the
analysis has already stated.

---

## 4. Logo

Three lock-ups in [`assets/logo/`](assets/logo/), plus a tokenised inline copy
and a sprite the pages use.

| Situation | Variant |
|---|---|
| Light surface | Positive — ink wordmark, cyan dot |
| Navy, slate or accent surface | Reversed — white wordmark, **cyan dot retained** |
| Single-colour print, or over photography | Mono — everything takes `currentColor` |

The `.es-logo` component reads its surface scope and reverses itself. Set
`data-variant="mono"` for the single-colour lock-up; nothing else needs
overriding.

- **Clear space** is one dot diameter (`--es-layout-logo-clear`, 4.2% of logo
  width) on all four sides. The component applies it as padding, so do not add
  your own.
- **Minimum width** is 120px (`--es-layout-logo-min-w`). Below that the
  RESEARCH lock-up stops reading. Source reports run it at 128px in slide
  footers, which is the floor in practice.
- **Sizes by context**: 128px in a slide or report footer, ~190px in a site
  masthead, ~240px on a cover, ~224px on a social frame. Those multipliers are
  in [`styles/patterns.css`](styles/patterns.css) — do not set widths by hand.
- **Never** stretch it, recolour the dot to anything but cyan or `currentColor`,
  place it on a busy part of a photograph, or substitute the Essential Media
  parent lock-up (orange dot) on Essential Research work.

---

## 5. Which component, when

**Structure**

| Need | Component |
|---|---|
| Open a report or a deck | `.es-canvas--cover` |
| Open a section | `.es-canvas--photo` with `.es-divider-number` on reports over ~40 slides |
| A web page section | `.es-section`, with `.es-section--ruled` where a break needs marking |
| Close a page with an ask | `.es-cta` |

**Evidence**

| Need | Component |
|---|---|
| A participant's own words | `.es-quote` — and `.es-quote--bare` beside a dark panel, where a tint fill would compete |
| A finding restated for emphasis in long-form | `.es-pullquote` — long-form only, never on a slide |
| A number that carries an argument | `.es-stat`, with `.es-stat__base` filled in |
| The working behind a chart | `.es-qbase` — mandatory above every quantitative chart |
| Your reading of the evidence | `.es-commentary` — interpretation goes here, never inside the chart |
| A convention the reader needs to know | `.es-note`, e.g. *Responses with <5% are not labelled on chart* |
| Who is speaking | `.es-audience` — public is dark with a gold icon, stakeholders are gold with a navy icon. Do not swap them. |

**Method and testing**

| Need | Component |
|---|---|
| Two to four research phases | `.es-card--headed`, gold for the public phase |
| A sequenced method with a progression | `.es-stages`, ramping light to dark |
| Two versions of the same thing | `.es-card--comparison`, slate then navy |
| What worked and what to fix | `.es-panel` with `.es-verdict` — navy is the stronger verdict, slate the weaker |
| A logic chain the audience may not complete | `.es-flow` — navy for steps they make, grey for steps they do not |
| A verbatim marked up line by line | `.es-annotate` with `.es-legend` — the legend is mandatory |

**Interface** — all inferred, none of it has a precedent in the source reports.

| Need | Component |
|---|---|
| The primary action on a page | `.es-button--primary` (cyan) |
| A second action beside it | `.es-button--secondary` (navy) |
| An action on an inverse band | `.es-button--outline` |
| The single most important action anywhere | `.es-button--highlight` (gold) — one per page at most |
| A computed status | `.es-badge` |
| A chosen category, which may link | `.es-tag` |

**The dot field** (`.es-dots`) is the only pattern. It resolves towards the
outer edge of the artboard — sparse where the copy sits, dense at the margin.
It frames the argument, it never sits under it. The one exception is the back
cover, where there is almost no copy. For print or large scale use the supplied
PNGs in [`assets/patterns/`](assets/patterns/); the CSS is a reconstruction.

---

## 6. Anti-patterns — what this brand never does

**Layout and surface**

- **No shadows.** Not on cards, not on buttons, not on hover. Depth is
  expressed by changing the surface fill. `--es-elevation-overlay` exists for
  web menus and dialogs and nothing else.
- **No rounded corners on structural panels.** Phase cards, comparison cards,
  commentary boxes and chart bars are square. The 10px radius belongs to quote
  cards and testing panels, and nothing else.
- **No gradients**, except the dot field's opacity ramp, which is stepped, not
  smooth.
- **No pattern behind body copy.**
- **No cyan headings on navy.** Reverse to white. Cyan on navy fails contrast.
- **No navy headings on white.** That is the parent brand's habit, not this one.

**Copy**

- **No topic-label titles.** State the finding.
- **No more than one finding per surface.**
- **No percentages in qualitative reporting.** Use the hedging ladder.
- **No upgraded hedges.** *Some* does not become *many* because the client would
  prefer it.
- **No quote that introduces a finding** the analysis has not already stated.
- **No named participants**, and no quote attributed to an organisation.
- **No interpunct joining a label to its value.** Write it as a sentence or put
  it on its own line. `Base: n=1,142`, not `Base · n=1,142`.
- **No source line twice.** If the footer carries *Client — Project (Year)*, the
  eyebrow does not repeat it.
- **No lorem ipsum**, in a mock-up or anywhere else. If the copy is not real,
  write something real enough to be judged.

**Evidence**

- **No chart without its Q and Base line.**
- **No stat without its base.**
- **No suppressed labels without a note saying they are suppressed.**
- **No mixing the categorical and ordered data palettes** inside one chart.
- **No stock imagery chosen for mood.** Photography either shows the subject or
  it does not appear.
- **No three-column 9pt executive summary.** Two columns, one idea per
  paragraph, no bullets.

---

## 7. Provenance

Every token records where its value came from, in a trailing comment carried
through to `tokens.json` as `source`:

| Tag | Source |
|---|---|
| `[theme]` | PowerPoint theme XML |
| `[svg]` | the supplied logo files |
| `[xml]` | slide-level XML |
| `[pdf]` | the report PDF's embedded font table |
| `[sampled]` | pixel-sampled from a flat fill in a reference render |
| `[measured]` | geometry measured and normalised to the 1280×720 canvas |
| `[INFERRED]` | no precedent in any source asset, with the basis stated |

**Read the `[INFERRED]` tags before trusting a value.** The source corpus is
slides and PDF only. There is no web or interface precedent in it at all, so
every control, state, motion value and social dimension in this system was
derived from the components that do exist. They are consistent and defensible —
they are not extracted.

### Corrections this system makes to the earlier reference pack

| Value | Was | Is |
|---|---|---|
| Edge stripe width | 18px | **38px** (measured 37.6 at 1280) |
| Canvas left margin | 48px | **80px** (measured, 0.83in) |
| Card body fill | `#F7F7F7` (theme `lt2`) | **`#F2F2F2`** — what every NLA card actually uses |
| Cover title | 40pt | **56pt** — ratio-derived against the XML-known 28pt title |
| Divider title | 32pt | **48pt** — same derivation |
| Section label | 20pt | **28pt** — there is no separate section size on a slide |
| Slate `#3F6071` | absent | the second-most-used structural fill in the corpus |
| Gold `#FFC000` | "not in the theme, barely used elsewhere" | also in the Oxfam slide XML; treated here as an official accent with a defined job |
| Coral `#D96968` | "essentially unused" | the negative end of the Likert ramp, with `#C03230` |
| Akzidenz Grotesk | not mentioned | present in the XML, but only as a bullet-glyph font — not a brand typeface |

---

## 8. What code cannot carry

Upload these to Claude Design directly. They are listed in priority order.

1. **The Aptos font files, or a licensed substitute.** Aptos ships with
   Microsoft 365 and is not licensed for webfont embedding. No font files were
   supplied. Everything in this repo falls back to a system grotesque, so the
   letterforms are approximate everywhere.
2. **A real icon set.** The icons in [`assets/icons/icons.html`](assets/icons/icons.html)
   are placeholders drawn to the corpus's rules — 96×96 grid, solid fill, no
   stroke, one flat colour. The source reports use Microsoft Office stock icons,
   which are not redistributable. Essential needs its own set, or a licence.
3. **Photography.** Every image in the reference pages is a colour block or the
   dot field. The corpus crops circles and runs full-bleed dividers under a navy
   overlay, and that is all code can tell you. Real photographs with cleared
   rights would change what these pages look like more than any other single
   addition.
4. **The logo in raster at large sizes, and any missing lock-ups.** There is no
   mark-only variant, no stacked lock-up, no favicon crop and no single-colour
   black. If those exist, they were not in the supplied assets.
5. **A print specification.** Everything here is RGB and screen. No CMYK
   breakdowns, no Pantone references, no minimum print size were supplied.
6. **The `.potx` template itself.** Component names here match the layout names
   in the Essential template where an equivalent exists, so the two vocabularies
   stay aligned. Uploading the template lets that alignment be checked.
