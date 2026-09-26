# Review — FM-006: the board's themes record (PR 82)

**date** 2026-09-26 09:05 CEST · **seat** Reviewer · **session** `8e509911/reviewer-21` · **worktree** `shoalmark-review-4`
(branch `themes-review` at the tip) · **tier** docs, one pass (P3 fixed forward, P2 sends it back) · **independence** same
session — 8e509911's own sub-agent, reported. The branch's sessions: `4ebd9569` (the GtM seat's `96aa05e` and `f3f994b`),
`8e509911` (the Principal's merge `a680581`), `8e509911/gtm-3` (the re-make `7344a78`).

**Reviewed:** `fm/006-the-board-s-themes` at `7344a78df58d19bf313d408567d0d6e41787cc0a`, four commits over `origin/main`
`0c3b30d` (PR 85's merge). The Owner's word it lands on: 07:41:00 through the Auditor seat, his paste of 07:55:40 —
*merging lands the mockups and renders as FM-006's evidence; it rules nothing.* I fixed nothing.

This file sits beside the record. Main's `shoalmark.toml` has no `[paths]`, so addenda count under `evidence/reviews/`
(the default); a verdict's own `review*.md` counts anywhere under `work-tracker/evidence/` (`--queue`, `own_review`).

## What I checked

| Check | What I ran | Result |
|---|---|---|
| Scope | `git diff --name-status origin/main...HEAD` | 26 paths: 25 new under `evidence/FM-006/themes/` (README, `build-mocks.py`, `render.mjs`, four stylesheets, 18 renders) and FM-006. INDEX.md is byte-identical to main's: `f3f994b`'s one-line change was superseded in the merge. The brief's *27* is `f3f994b`'s count (25, the tracker, INDEX.md). `shoalmark.py`, `brand/`, `work-tracker/brand/`, `docs/`, both suites, `CHANGELOG.md`, `VERSION`, `lefthook.yml` and `shoalmark.toml` are untouched ✓ |
| The renders are real | Rebuilt from this tip with the committed scripts: the board from `python3 shoalmark.py --html-only`, the site from `uvx --offline zensical build` (0.0.65, as the README's), `build-mocks.py` and `render.mjs` into an ignored folder of this worktree, `TMPDIR` there too, Chrome with every host but 127.0.0.1 unresolvable, no `--plex` | 18 of 18 made. The styling is the committed renders' own. The 0.6–8.8 % of pixels that differ are the record's content since 02:05 (*oldest 0 → 1 days*, sessions 20 → 25, the site's two new TRIAGE nav lines). All 18 labels match theme and scheme: grounds sampled `#ffffff`/`#0b0c0f` for monochrome and the band `#15293c`/`#15293d` for shoalmark. The board is 1300 px wide and the site 1440 px. No PNG carries a metadata chunk ✓. Not byte-equal: bold and italic are synthesised without `--plex`, and uv's cache was read |
| Contrast | 64 text pairs from the committed tokens, WCAG as the tool's `contrast()`, alpha composited. For `site-monochrome`, Zensical 0.0.65's own palette was read from the built CSS. Status marks too | Every pair is 4.5:1 or more in both schemes, the lowest at 4.50. The status marks are 5.24–11.49 ✓. The README's 8.2 (8.25/8.24), 6.06, 5.76, 16.6 (16.56) and 6.94 match. Its 4.84 and 4.75 do not (R1) |
| Markers and figures never read | Chrome's accessibility tree through CDP (`Accessibility.getFullAXTree`) on the seven mock pages (both boards, both dialogs, the tracker view, both sites), both schemes. **Control:** the same pages with the 62 alt texts `/ ""` removed | No latitude or longitude figure is in the tree, and no `#`, `//`, `[ ]` or `>` marker. The buttons are named *accept*, *reject*, *done*, *reschedule*, *OK — give me the command* and *abort*. In the control, the chart's strings are read in full (64 latitudes, 40 longitudes), the buttons read `[ accept ]` and so on, and the markers are exposed. The README states the claim as tested and names its control (*without the alt text*): reproduced ✓. *owed to the owner* stays in the tree. It is a label, as meant |
| The Owner's words | The themes section against the README | Marked *in chat … spelling normalised* and *His words, not a signed answer: the ask below makes them one*; the README says *His words, not a signed answer*. The quotes are the README's word for word, and the tracker marks its one cut with `…` ✓. The chat is not in the repository, so fidelity to his words is unverified. Nothing is called decided, except R4's two phrases |
| The re-made ask (AU-24) | Counted in Python; compared with the tool's ask rules | Kind *ruling*. The ask is 258 characters with one `?` (within `ASK_MAX` 300). The options are 85, 108 and 84 characters, as claimed, each at most 120. There are three, in the Owner's order, each saying both the worn theme and the shipped themes. The proposal is option 1 verbatim, as the tool requires. It is disclosed as the GtM seat's, with its reason. `monochrome` is not offered as worn: the seat's written no. It is a draft in the body, and the README's draft is identical. Front-matter lines 1–17 are byte-identical to `origin/main`'s (*When and how does shoalmark go public?*, `action`) ✓ |
| The GtM seat's disclosure | The four passages the brief names | The three hooks are `shoalmark.py` changes, in neither slice. Slice A wears the mocks' workarounds on today's board, and *the pass says where the hooks go*: open by its words. *What is true now*, the themes bullet, *How a theme is chosen* and the README's *What the build is* do not state the tool ships themes as settled ✓. The 2026-09-25 ship-log row's *to ship as files* is append-only history |
| The merge `a680581` | Diffed against both parents | The parents are `f3f994b` and `0c3b30d`. Against main, FM-006 only gains lines (0 removed). Main's text is whole: the *built, in review* paragraph, the heading's times, *21 open*, the two 2026-09-26 page rows. Against `f3f994b`, only main's changes show. The stale *is owed* paragraph is gone, not duplicated. The themes paragraph comes first, then the section and its rows. Every other path equals main's ✓. Rows are newest first by date. Within 2026-09-26, the narrowed row (02:05:19) sits below the page-built row (02:04:25), 54 s older. The rows carry dates only, so this is not a finding |
| Gates | On the tip, at 08:38–08:50 CEST (outside FM-028's window, no `TZ=UTC`) | `--check` 0: *INDEX.md is up to date — 37 trackers*, freeze *21 open*, the Owner's two sections guarded. `--session-check` 0. `test_shoalmark.py` 456 and `test_core.py` 148 on 3.14.3 and 3.9.6, 0 skipped. `git merge-tree --write-tree origin/main HEAD` is clean, tree `02d407e`, HEAD's own ✓ |
| Secret screen | `lefthook.yml` carries none (tests, session, tracker-index, session trailer, *judged*), so I screened the diff by hand. I also read all 18 renders | No email, key, token, credential, local path, parent name or client name. Hosts: 127.0.0.1 (CDP), fonts.googleapis.com, and webtui.ironclad.sh (a public library's site, quoted). The renders show tracker text, session ids, worktree names and `holgo99/shoalmark` on the site's source link, as main's site does ✓. The README's own note (the private review page deleted, nothing about the themes outside this folder) cannot be checked from here |

Also checked and holding: the chart's geometry (2 × cos 53.9° = 1.18; 18 ch of 11 px Plex Mono = 118.8 px; 64 latitude
and 40 longitude figures); both media queries (board ≥ 1040 px, site ≥ 1380 px, `screen` only); every `content:` string
Latin-1; `v0.18.4` not tagged; the Regular's sha256 `10d3c7fa…`; the paste's sha256 `34ee13d1…` against the Principal's
file, byte for byte.

## Findings

**R1 (P3) — three contrast numbers are not the committed CSS's.** *Why it matters:* the build's Reviewer re-measures
on built files. The record tells slice A there is headroom where there is none. *The gap:* README lines 96–99.
- `monochrome`'s foot by day is `#737373` on `#f9f9f9`: 4.50:1 (4.504), not 4.84:1. The render's pixels are exactly
  those two colours.
- Its figures by day are 4.74:1 (4.742), not 4.75.
- The site's own pairs start at 4.74:1, not 5.76, if the range covers both sites: `site-monochrome`'s heading marks
  are Zensical's `#0000008c` on white.

Every pair holds 4.5:1, so the claim itself stands. *What closes it:* the three numbers corrected, the monochrome
foot's zero margin named, and the site the range covers said. *Confidence:* 95 %.

**R2 (P3) — the stylesheets cannot be taken as the lines they say they are.** *Why it matters:* slice A is
`work-tracker/brand/theme.css` *from the chosen theme* and *the site's theme as lines in `docs/stylesheets/`*.
*The gap:*
- (a) `monochrome.css`'s two `@font-face` urls are page-relative (`brand/fonts/…`). The tool re-bases every url in a
  `theme.css` relative to its own file. In `work-tracker/brand/theme.css` they become `brand/brand/fonts/…`, which
  does not exist, so SemiBold and Italic are synthesised. I ran the tool's own regex on the file to see this. The mocks
  inject a `<style>` into the page, so their renders cannot show it.
- (b) `site-monochrome.css` opens with an `@import`. As lines added to `docs/stylesheets/shoalmark.css`, it would
  follow rules, and a browser drops a late `@import`. It is also a second Google Fonts load, on a site whose
  self-hosting is FM-006's open item before publication (R3 of 2026-09-24).

*What closes it:* the slice A line says a theme's urls are relative to its file (`fonts/…`), and that the site's Mono
600 and italic join the existing import or the self-hosting slice. *Confidence:* 90 %.

**R3 (P3) — the reason given for leaving a phone's width unchecked does not hold for this harness.** *Why it
matters:* the Owner's item 4 wants the build's renders at phone width, and the record reads as if they cannot be made.
*The gap:* README line 113 says *headless Chrome will not go below about 500px*. But `render.mjs` sets the width through
CDP's device metrics, and at 390 px Chrome lays out the site and the tracker view at 390 px. What stays wider is the
board's table: 504–505 px under the themes, and 905 px on today's board. *What closes it:* the sentence corrected: the
chart is off there by design, and the board overflows to about 505 px themed and 905 px today. *Confidence:* 85 %.

**R4 (P3) — two phrases presume an answer the ask leaves open.** *Why it matters:* path 5 — the record should read
true under all three options. *The gap:*
- *How a theme is chosen* ends *shoalmark's own board and site wear one theme, which the ask picks*, but the third
  option keeps today's look.
- The README's file table and `shoalmark.css`'s first line call `shoalmark` *the starter to make yours from*. Only
  the second option ships it as a starter.

*What closes it:* *wear at most one; the ask says which, or none*, and *a starter if the tool ships themes*.
*Confidence:* 60 %.

**R5 (P3) — the word the record cites is not in the record.** *Why it matters:* the FM-033 pass and the build read
the tracker, not the Principal's scratchpad. This tracker files the pastes it acts on word for word elsewhere (*Going
public*, *the page on his word*). *The gap:* the ship-log row cites the Owner's word of 07:41:00 by sha256
`34ee13d1…`. The hash matches, but the text lives outside the repository. The tracker paraphrases item 3's slices and
leaves out two things:
- item 3's order: *after FM-037 and the 0.18.4 tag, unless the pass judges otherwise*;
- item 4's carry-overs: AU-16, AU-18, contrast re-measured on built files, real renders at desktop and phone width seen
  before the merge, and the site live with the next tag.

*What closes it:* the paste filed word for word under the themes section with its hash, or its order and carry-overs
written as lines. *Confidence:* 60 %.

Not findings:
- `monochrome.css` lines 10–11 repeat a comment.
- `build-mocks.py` says pages without the site's stylesheet are *none today*, but `404.html` is one (its links are
  absolute).
- The brief named the GtM seat's session `1dd8a5e9`; its two commits carry `Session: 4ebd9569`.

## Verdict

**READY WITH FINDINGS** — R1–R5, all P3, fixed forward; no P2. The record's claims hold where they were run: the
renders are the real board and site, every text pair is at 4.5:1 or more, and no marker or figure is read aloud (the
control shows the difference). The ask is re-made as AU-24 draws it, and the merge keeps main whole.

*The Owner lands this by merging, and a merge rules nothing (path 5).*
