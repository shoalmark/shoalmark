# Review — FM-006, the site wears the Pricke

- **Date:** 2026-09-24, 07:22 CEST (`date`)
- **Seat:** Reviewer (`reviewer@seat`) · **Session:** `8e509911/reviewer-1` · **Model:** Claude Opus 5.5
- **Tip reviewed:** `2f1e6c0` on `fm/006-the-site-wears-the-pricke`: four commits by `implementer@seat`, sessions
  `8e509911/implementer-6` and `-7`.
- **Base:** `92f485b`, the Pricke branch with this seat's earlier review.
- **Method:** reviewed detached in `shoalmark-research`, because the Owner's checkout holds the branch. Built in a
  scratch venv (Zensical 0.0.64) from `git archive`, so `site/` never touched a worktree.

## The checks

**(1) The build and the pixels.**
- `zensical build` exits 0 with *No issues found*.
- In the header, the mark is 16 × 16 CSS px at `(130, 16)`.
- **Hard-edged**, read from my own headless-Chrome screenshots of the built page:

  | scheme | 1× | 2× |
  |---|---|---|
  | light | 2 colours: 210 ground, 46 ink | 2 colours: 840 ground, 184 ink (46 × 4 exactly) |
  | dark | 2 grey levels (11 and 189) | 2 grey levels (11 and 189) |

  In dark, RGB shows 4 values, pairs differing by one unit in a single channel: the translucent header composited over
  the page. There is no intermediate grey.
- **The stake equals the stems:** 2 px at 1× and 4 px at 2×. The Mono wordmark's vertical stems on its middle row are
  2 px at 1× (one 1 px, two 3 px) and 4 px at 2× (3–5).

**(2) The icon override is the theme's sanctioned path.**
- `zensical.toml` sets `custom_dir = "overrides"` and `[project.theme.icon] logo = "shoalmark/pricke"`. The file is
  `overrides/.icons/shoalmark/pricke.svg`, the Material convention for a custom icon set.
- The built page inlines that SVG in `[data-md-component="logo"]`, and I built it myself from the committed sources,
  so nothing is hand-patched.
- Its path equals `d.svg`'s path exactly, and `d.svg` is unchanged from `92f485b`.

**(3) The CSS touches only the site name and the logo size.**
- `docs/stylesheets/shoalmark.css`:
  - sets Plex Mono 500 on `.md-header__ellipsis > .md-header__topic:first-child .md-ellipsis`;
  - pins the logo SVG at 16 px.
- In the browser:
  - the name's computed font is *"IBM Plex Mono", monospace 500*, and the text's is *"IBM Plex Sans", …*;
  - **0** paragraphs, list items or headings in the page text render in Mono;
  - `document.fonts.check` is true for Plex Mono 500 and for Plex Sans 400.

**(4) The palette.**
- The built HTML carries both schemes (`default` and `slate`) with their toggle labels, *Switch to dark mode* / *Switch
  to light mode*.
- The logo's computed colour equals the header's in both: `rgba(0,0,0,0.87)` and `rgba(226,228,233,0.82)`.

**(5) The tab.**
- `docs/assets/favicon.svg` has the same `viewBox` and **byte-equal path** as `d.svg`. It adds `crispEdges` and a
  fill that is `#1a1a1a`, or white under `prefers-color-scheme: dark`.
- `<link rel="icon" href="./assets/favicon.svg">` (and `../assets/…` from `de/`).

**(6) The gates.**
- `llms_txt.py site` exits 0, 9 pages.
- `--check` exits 0.
- `--session-check` exits 0 for this commit (`8e509911/reviewer-1` is open).

**(7) The rest.**
- Nothing under `site/` in the diff.
- No consumer or client name or id.
- Every PNG is under 400 KB; the largest is `site-header-dark-2x.png` at 145 KB.
- The FM-006 row quotes the Owner's trial, *"wait. let's try d alone as proposed with the mono, this could be
  stellar"*, marked *relayed*. The note quotes the 16 px decision marked *spelling normalised*.

## Findings

### R1 · P3 · The Owner's 16 px decision is in the note, not in FM-006

- **What:** *"16 px is the better-fitting one; we could try a 24 px variant, but 16 px will do."* appears only at
  `pricke-2026-09-23.md:144`. FM-006's one new row records the trial, and says his lock (*`a` in the header*) stands
  *until he has seen the built header and says which*. The tracker is canonical, and it does not say that he has seen
  it or what he said.
- **What closes it:** One FM-006 ship-log row with the quote. If he has settled `d` over `a`, say so; if not, say it is
  still open.

### R2 · P3 · The note's provenance names the wrong session for its new sections

- **What:** The single *Provenance* footer (`:168`) names `8e509911/implementer-5`. The two sections appended on
  2026-09-24 were written in sessions `-6` and `-7`, per their commits' trailers.
- **What closes it:** One provenance line per section, or a footer naming all three sessions.

### R3 · P3 · The pages load their fonts from Google — for the Owner, before the site goes public

- **What:** The theme's `[project.theme.font]` makes the pages fetch IBM Plex from `fonts.googleapis.com`, and
  `shoalmark.css` adds a second `@import` from Google for Mono 500.
- **This is not new in kind.** `main` already loaded Inter and JetBrains Mono from Google.
- **Why it matters here:** For a German-first site with German readers, remote Google Fonts transmit each visitor's IP
  to Google. German courts have held that unlawful without consent (LG München I, 20 January 2022).
- **What closes it:** Self-host the two families under `docs/assets/fonts/`, set `font = false` in the theme, and
  declare the faces in `shoalmark.css`. This fits the IBM Plex slice.

## Verdict

**READY WITH FINDINGS: R1, R2 and R3 (P3).**

- The mark is the byte-exact `d`, inlined through the theme's own icon path.
- It is hard-edged at 1× and 2× in both schemes, and takes the header colour.
- Its stake matches the Mono stems.
- The fonts load, and only the name is in Mono.
- The palette toggle and the tab icon work, and the gates exit 0.

## Confirmation at a535b61 — 2026-09-24 07:40 CEST

- **R1 is closed:** FM-006 records *"… 16 px will do"* (`6e1ea5b`), and says the ruling supersedes the lock of `a`.
- **`a3089c5` is one rule and its comment:** `[data-md-color-scheme=slate] .md-header__button.md-logo{color:…100%}`.
- **The two renders** are 63 KB and 145 KB. PIL shows the mark's ink at 255 and the name's at 255, two grey levels.
  My own rebuild: dark 255/255 (was 189/255); forced-light 1×/2× byte-identical to `2f1e6c0` (0 px).
- **Sessions:** the `implementer-8` row was opened in `a3089c5` and closed in `a535b61`; nothing else moved.
- **Gates:** build *No issues found*; `--check` 0; `--session-check` 0; `site/` untracked. There is no secret gate in
  this repository; the consumer's detector on the five changed files found 0.
- **R4 · P3:** `6e1ea5b`'s row carries a date but no time or zone (git: 07:23 +0200). `a3089c5`'s (*07:35 CEST*)
  agrees with git.
- **Verdict:** READY WITH FINDINGS. R2 (the provenance footer) and R3 (self-host Plex before publication) stay open as
  FM-006 records them; R4 is a P3.

## The tagline slice at bc50200 (contains 685bbb4) — 2026-09-24 07:58 CEST

- **The diff from `488c098`** touches only `docs/{de/,}index.md:3`, FM-006 and `sessions.md`. The built pages read *Eine
  Pricke im Watt – sie hält die Flotte im Fahrwasser.* and *A Pricke on the Wadden flats keeps the fleet in the channel.*
- **The two carried rows** are byte-identical to `916cd26`'s plus the carry note. Their rulings were absent at `488c098`.
- **R4 is closed:** *07:23 CEST* matches git (07:23:11 +0200). The P4 row (07:48) and the English row (07:51; git
  07:51:39) mark their quotes *relayed … spelling normalised*.
- **Sessions:** `implementer-9` was opened in `ee152ef` and is still open. The branch head is now `0f4b5e2`, the merge
  of `main` (#31, #32). Its `sessions.md` keeps every row of both parents and adds none; `--check` 0 there too.
- **Gates:** build *No issues found*; `--check` 0; `--session-check` 0; nothing under `site/`.
- **R5 · P3:** the Plex Mono row's carry note says *the a + d lock was superseded*, which reads as if the typeface ruling
  were superseded.
- **Verdict:** READY WITH FINDINGS. R5 is a P3; R2 and R3 stay open as FM-006 records them.
