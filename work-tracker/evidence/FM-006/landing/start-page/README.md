# The landing page is the site's start page — FM-006 slice L, the GtM seat, 2026-09-26

**Built on `fm/006-the-landing-page`, not merged.** On the Owner's word in chat of 10:25:41 (spelling normalised, not a
signed answer): *for the v0.18.5 release we also add a landing page requirement, alongside the restyle and rebrand of
shoalmark's brand identity* — the mock one folder up (`../index.html`, `9704140`, PR 82), on which his word was *"you
nailed it — file, commit and push"*. The seat's reading, his to strike: the landing page is the site's start page — what
a person sees first at the site's root; the agents' page stays `agents/README.md`.

**His rule for this slice (16:0x): the mock is taken as-is** — the same HTML, CSS and script, full-bleed, no site chrome,
no new section, copy, colour or font. The only edits are the four below, each marked in `overrides/landing.html` with a
Jinja comment the build drops, so the built page carries no trace of them but the change itself.

## How the page became the start page

`overrides/landing.html` is the mock, byte for byte, under one comment; `docs/index.md` selects it with front matter,
`template: landing.html`. Zensical 0.0.65 renders a page through a template of `custom_dir` named in its front matter, and
a template that extends nothing is emitted as written. So `site/index.html` is the mock: no header, nav, sidebar, search
or footer; every other page keeps its chrome, and `zensical.toml` and the nav are unchanged (*Start* is still
`index.md`). At item 1 the built page equalled the mock but for its final newline, which the template engine drops.

Why a template and not the page as the root document: the site's root must be `index.md`'s output for the nav's *Start*
to reach it, and a template keeps the prose as the page's source — the German start page's original, and the Markdown
twin `scripts/llms_txt.py` writes for agents beside the page. The site does not show that prose; a comment in
`docs/index.md` says so. Zensical's search still indexes it, and a hit leads to the landing page.

**The page is dark by choice and does not follow `prefers-color-scheme`**: `color-scheme: dark` and no scheme query, as
the mock — it is a screen. Under a light preference Chrome draws the same pixels (`checks.json`, `scheme`).

**Its links are the mock's, absolute** — `https://holgo99.github.io/shoalmark/setup.html` and so on: live once the site
is published at the go-public act; in a local build they leave the build. Not changed: the rule allows no edit there.

## The four edits

| | Where | What |
|---|---|---|
| (a) the facts dated | `WRECKS`, the HUD's source figures, the register's summary, the board's excerpt, the foot's fine print | read from `main` at `bef2a1e` on 26 September 2026 at 18:00:51 CEST — the table below; the foot says *read on 26 September 2026, 18:00 CEST from main at bef2a1e* |
| (b) R4 | every wreck's `report` | its tracker's `hook:`, cut to its first sentence or two, verbatim, code spans kept |
| (c) R3, his to strike | `.name` z-index 4 → 7, `.fig` 5 → 7 | the chart's names and figures above the CRT overlay (`.crt`, 6) |
| (d) the fonts | the three `<link>`s in the head | one Google Fonts load the site's way |

## (a) The facts, dated

Read with `facts.mjs` (git only; its first run was a Python form of the same reading, which the Node script reproduces
field for field — `facts.json` was that 18:00:51 reading, replaced by its summary below on 2026-09-30), and the board rendered in Chrome from `git archive bef2a1e`
(`python3 shoalmark.py --html-only`) at 18:01.

| On the page | Read from `main` at `bef2a1e`, 18:00:51 CEST |
|---|---|
| release **v0.18.5**, *released 27 September 2026*, its summary | re-read at the 0.18.5 cut: `VERSION` 0.18.5 and `CHANGELOG.md`'s 0.18.5 head line (`522db92`), the day the tag's earliest (`69552ed`); at `bef2a1e` the page read v0.18.4 — `VERSION` 0.18.4, the tag `v0.18.4` on `a7e5291` (09:58:57), the 0.18.4 headline, unchanged from the mock |
| **24 wrecks**, not 23: 8 open, 15 raised, 1 closed | the trackers tagged `bug` or `security`: FM-038 was filed at 13:35 (`5558b1a`), after the mock; the register's heading is *Every defect, on the chart* |
| each wreck's incident ID and filing day | `git log --diff-filter=A` on its file, the earliest, the day in Europe/Berlin — unchanged for the 23 |
| each wreck's status and title | its front matter and `# ` line: FM-034, FM-035, FM-036 now Shipped (raised); FM-037's title in main's lower case |
| the register's summary, *22–26 September 2026* | the first and last filing day |
| the board's excerpt | *waiting for you: 0*; *your acts, with their time: 4*, the first FM-006's: *promised 2026-09-26: accepted - … after the scoring, gates held · no date yet*, **done** and **reschedule** — the answer's middle cut, marked `…`; the markup is the mock's, only its words changed |
| 12/15 and 10/37 and how they were counted, the four stages, what a day costs, what it is not, the three ways in | `docs/index.md`, unchanged at `bef2a1e` |
| 200 pull requests in 22 days, 85 %, none reviewed; the three agents | `README.md`, unchanged |
| the claim | `work-tracker/brand/labels.yaml`'s footer, unchanged |

FM-038's position is a drawing, as every wreck's (*positions are a drawing, not a fix*): the flat pixel farthest from
every other wreck and every name, at least 12 chart pixels inside the border, outside the title, its 7 × 5 footprint all
flat or sand — 7.077 E, 53.54 N, off the Leybucht. It is first in `WRECKS`, as the mock put the newest open wreck first.

| Wreck | Incident | Filed | On the page | Sentences | R4 |
|---|---|---|---|---|---|
| FM-038 | `5558b1a` | 2026-09-26 | open (on the chart) | 1 | new |
| FM-037 | `8b0877f` | 2026-09-25 | open (salvage under way) | 1 | capitalised, a full stop added → verbatim |
| FM-036 | `069651d` | 2026-09-25 | raised — In Progress in the mock | 1 | condensed → verbatim |
| FM-035 | `840dabe` | 2026-09-25 | raised — In Progress in the mock | 2 | condensed → verbatim |
| FM-034 | `d1618dc` | 2026-09-24 | raised — In Progress in the mock | 1 | cut mid-sentence → whole sentence |
| FM-033 | `35c7664` | 2026-09-24 | open (salvage under way) | 1 | condensed → verbatim |
| FM-030 | `137d9ba` | 2026-09-24 | open (salvage under way) | 1 | verbatim already |
| FM-029 | `137d9ba` | 2026-09-24 | open (salvage under way) | 1 | verbatim already |
| FM-028 | `f9a7e49` | 2026-09-24 | open (on the chart) | 2 | condensed → verbatim |
| FM-022 | `7bc780d` | 2026-09-23 | raised | 1 | verbatim already |
| FM-021 | `0231287` | 2026-09-23 | raised | 2 | condensed → verbatim |
| FM-020 | `0231287` | 2026-09-23 | raised | 1 | verbatim already |
| FM-019 | `e9a3414` | 2026-09-23 | raised | 2 | condensed → verbatim |
| FM-018 | `3b46cdf` | 2026-09-23 | open (on the chart) | 1 | condensed → verbatim |
| FM-017 | `8c562f0` | 2026-09-23 | raised | 1 | cut mid-sentence → whole sentence |
| FM-016 | `dfc98d7` | 2026-09-23 | closed | 1 | cut mid-sentence → whole sentence |
| FM-015 | `dfc98d7` | 2026-09-23 | raised | 2 | cut mid-sentence → whole sentence |
| FM-014 | `dfc98d7` | 2026-09-23 | raised | 2 | condensed → verbatim |
| FM-013 | `dfc98d7` | 2026-09-23 | raised | 1 | condensed → verbatim |
| FM-012 | `dfc98d7` | 2026-09-23 | raised | 2 | condensed → verbatim |
| FM-011 | `15d537c` | 2026-09-22 | raised | 1 | condensed → verbatim |
| FM-010 | `c550e6d` | 2026-09-22 | raised | 2 | condensed → verbatim |
| FM-009 | `a705c31` | 2026-09-22 | raised | 2 | verbatim already |
| FM-007 | `f937b21` | 2026-09-22 | open (salvage under way) | 2 | cut mid-sentence → whole sentence |

## (b) R4 — the reports cut as the mock's README says

The README one folder up says *the tracker's `hook:`, cut to its first sentence or two, code spans kept*; the page now
does that, so the sentence stands. How many sentences: as many as the mock's report carried — the count the Owner saw;
one for FM-038. A sentence ends at `.`, `?` or `!` followed by a space and a capital, a backtick, an
asterisk, a quote or a digit. **18 of the mock's 23 reports changed** (12 condensed, among them the five the Reviewer
named; 5 cut inside a sentence at a colon or a dash; FM-037 capitalised); 5 were verbatim already. Every report is a
prefix of its hook, checked by `facts.mjs`. Markdown emphasis stays as written (`*Applied 1*` in FM-036's): the page
renders code spans only, as the mock did. The longest is FM-035's two sentences, 447 characters.

## (c) R3 — the chart's text above the CRT overlay, measured as drawn

The smallest change that meets the 4.5:1 rule: the names and figures lifted to the wrecks' layer (7), above the overlay
(6). It changes 0.93 % of the chart's pixels at 1440 px and 1.88 % at 1024 px — the text itself. Moving the overlay under
them (`.crt` 6 → 3) meets the rule too, but also lifts the chart's graduated border out of it: 2.99 % and 4.74 %.
Thinning the overlay changes every pixel its scanlines or its vignette darken. Renders: `shots/r3-before-*.png` (the item-1
build, the mock as it is) and `shots/r3-after-*.png` (item 2), the chart alone, reduced motion.

Both methods are in `checks.mjs`; every name, figure and wreck label the page shows, at 1440 and 1024 px (at 700 px and
less the page hides them all). **R, the Reviewer's** as his record describes it: the specified colour against the median
pixel of the ground (the text transparent, its halo off); where the text lies under the overlay, or under the title's
backdrop, it is darkened by the factor those layers darken the ground under its box. **S, the seat's**: pixels only — the
page as drawn against the same page with the chart's text transparent; the ink is every pixel that differs by 16 levels
or more, the glyph core the quarter that differs most, the ratio the core's median pixel against the median ground
under it.

| Lowest chart text, not under the title | 1440 px, R | 1440 px, S | 1024 px, R | 1024 px, S |
|---|---|---|---|---|
| before — the mock (`checks-r3-before.json`) | **2.65** `53°30'N` | **2.81** `53°30'N` | 2.74 `53°30'N` | 2.80 `53°30'N` |
| texts below 4.5, before | 19 of 73 | 14 of 73 | 19 of 75 | 13 of 75 |
| after — the tip (`checks.json`) | **4.80** `OSTFRIESLAND` | **4.72** `JUIST` | 4.80 `OSTFRIESLAND` | 4.80 `OSTFRIESLAND` |
| texts below 4.5, after | 0 of 74 | 0 of 74 | 0 of 76 | 0 of 76 |

**Not changed, and his to strike:** at 1440 px two latitude figures on the chart's west edge, `54°10'N` and `54°00'N`,
lie under the title's text, which stands on the open sea by the mock's design; S reads them at 1.30 and 1.55. Lifted over
the title they would print across its h1 and its lede; they are covered, not drawn text. The Reviewer named one.

**The flat pairs** — every other text run on the page, its colour over the median pixel under its glyphs, 1440, 1024 and
390 px: the lowest is **5.14**, a raised wreck's id on the register's zebra row, as the mock's README says; none below 4.5.

## (d) The fonts — one load, the site's way

The built site loads its fonts from Google Fonts through the theme — one preconnect to `fonts.gstatic.com`, the families
from `[project.theme.font]`, `display=fallback` — plus slice A's one `@import` for Plex Mono 500 and 600. The start page
extends no theme template, so the theme's link is not emitted beside the page's own: its one link, in the template, takes
the family from `[project.theme.font]`'s `code` (IBM Plex Mono), the theme's preconnect and `display=fallback`, and carries
Silkscreen in the same load. The faces are the mock's: IBM Plex Mono 400, 400 italic, 500, 600 and Silkscreen 400, 700
(`checks.json`, `fonts`) — no Plex Sans, no second copy of Plex. The whole page, reduced motion, at 1440, 1024 and 390 px:
the same pixels before and after this edit. Silkscreen sets only the arcade's words, as the mock. **Still open, as it
stands:** Plex, and now Silkscreen, come from Google, which sends every visitor's address there — FM-006's item to
self-host the fonts under `docs/assets/fonts/` before the site is published, its own slice.

## `docs/index.md`'s facts, reachable from the start page

| The fact | On the start page, or behind its links |
|---|---|
| the claim; *Get a better-performing human Owner.* | on the page |
| *To the owner:* your agents ask mid-flight … once a day | on the page (2P) |
| *To the fleet:* you do not wait for tools, you wait for your human … one command | the agents' page (1P's *the contract*): *Agents do not wait for tools. They wait for their human.*; *once a day* and *one command per answer* on the page |
| only your signed word counts; a click, a merge or a line in chat is not an answer; four tiers | on the page (2P, *your signature*); the tiers behind *Your answer is your commit* |
| on git once your seat is marked `signed`; under Subversion the server-authenticated commit | behind *Set up in ten minutes* and *Your answer is your commit* |
| every signature names the key that made it | **not found as such** on a linked page |
| 12/15 and 10/37, the counting note, the rule of 24 September 11:07 | on the page (high scores) |
| a commit's date is not its push: the forge's push events confirm the counted pull requests from 24 September 05:18 UTC | **on no English page any more** — the German start page and `docs/index.md` keep it |
| one command, one signed commit per question | on the page (`--answer AP-007 accept`) |
| the board reports, for every review, whether it came from another session | behind *The standup* (*Which review was independent*); **its qualifier *a report, not a proof: git cannot yet show it* is on no linked page** |
| the four stages, *you lose nothing*, FM-026 | on the page (insert coin, 2P) |
| what a day costs; what it is not; the three ways in | on the page (costs, the ticker, the coins) |

The three marked lines are lost from the English start page by the rule that takes the mock as it is: adding them is new
copy. Whether they return — a sentence in the counting note, a line on the standup page — is his to rule.

## The German start page

`docs/de/index.md` keeps its words, restyled by slice A's stylesheet, with the site's chrome, and gains one line under its
claim: *Die Startseite, auf Englisch: eine Seekarte des Wattenmeers, auf der jeder Fehler aus shoalmarks eigenem Tracker
als Wrack liegt.*, linking the landing page. A German landing page is a follow-up line on FM-006. The seat's default, his
to strike.

## Renders — `shots/`, of the built page

Chrome 154 headless, served from 127.0.0.1, offline but for the two Google Fonts hosts (`requests.json`: only they were
reached, none refused, no script error), a dark preference, device scale 1. **The first screens, the whole pages and the
reduced-motion screens are the page as v0.18.5 ships it**, built at `69552ed` — the HUD's *release* v0.18.5, the foot's
link and fine print — re-rendered at the 0.18.5 cut (27 September 2026, 00:27 CEST; the pass's R4 on `0612dfe`); the R3
pairs are `9307cf8`'s and `ab69afb`'s builds, as the slice made them.

| File | What |
|---|---|
| `start-1440.png`, `start-1024.png`, `start-390.png` | the first screen, motion allowed, 3 s after load |
| `start-1440-full.png`, `start-1024-full.png`, `start-390-full.png` | the whole page: 5837, 6459 and 11025 px tall (the fine print one line longer than at `cb49101`) |
| `reduced-1440.png`, `reduced-1024.png`, `reduced-390.png` | the first screen under reduced motion |
| `r3-before-1440.png`, `r3-after-1440.png`, `r3-before-1024.png`, `r3-after-1024.png` | the chart alone, before and after R3 |

## Checked — `checks.json`, on the tip's build

`checks.json` held every measurement until 2026-09-30; its summary is the *Summary* below, and `08798a8` holds the file.

Of the slice's tip `cb49101`, not re-run at the cut: the same-session pass on `0612dfe` ran `checks.mjs` on the release's
build and read the same summary but the page's height, 5819 → 5837.

- **No script error**, no failed request, at 1440, 1024 and 390 px.
- **No sideways scroll**: the page is as wide as the window at all three.
- **The accessibility tree**, at all three: 24 wrecks, each a focusable button named with its number, its status and its
  title; the canvas described (*A night chart of the German Bight …*); no chart figure read, and no node of the chart's
  names or figures in the tree.
- **Reduced motion**: two captures of the whole page 7 s apart are identical.
- **The scheme**: a light preference draws the same pixels as a dark one, at 1440 and 390 px.
- **Contrast**: above, (c).

**Not verified**, as the mock's README lists: Firefox, Safari, a screen reader, print.

## Summary — the check output, regenerable

**The Owner's ruling of 2026-09-30 (07:04:27, *normalised*): *"If a check output regenerates, keep only its summary; if it doesn't, it stays in
git."*** The three outputs of this folder regenerate from git by the commands of *Rebuild* below, so they are replaced by this summary; each
is in git, byte for byte, at `08798a8` (`git show 08798a8:<path>`). Regeneration is judged by the checks' results by this README's thresholds,
never by bytes: the files carry an `at` stamp and Chrome's pixel measures move.

| | `checks.json` | `checks-r3-before.json` | `facts.json` |
|---|---|---|---|
| tested | `cb49101`, the page as slice L leaves it | `9307cf8`, the mock as it is (item 1) | `bef2a1e`, `main` on 26 September 2026 |
| command as run | the *Rebuild* lines: `git archive cb49101`, `uvx zensical@0.0.65 build`, `checks.mjs stage-cb49101/site … landing/index.html` | the same for `9307cf8`, `checks.mjs stage-9307cf8/site …`, its chart part kept | `node facts.mjs bef2a1e work-tracker/evidence/FM-006/landing/index.html` |
| environment, original run | Chrome 154 headless, Zensical 0.0.65, Node 22 or later (26 September 2026, 16:10 UTC) | the same (16:11 UTC) | git and Node 22 or later (18:00:51 CEST) |
| environment, fresh run | node v26.7.0, Google Chrome 154.0.8037.58, zensical 0.0.65 (uvx zensical@0.0.65, uv 0.10.4), macOS Darwin 25.6.0, 2026-09-30 07:29-07:34 CEST | the same run | the same, 07:29 CEST |
| original: checks · failing | 18 · 3, three chart texts under the title's own text, as *Not changed* above says | 4 · 68, the mock's texts below 4.5 (19 + 13 + 20 + 16 by method and width) | 24 wrecks read, 26 September 18:00:51 |
| fresh: checks · failing | 18 · 3, the same ids | 4 · 68, the same ids | 24 wrecks; every field equal but `read`; sha256 without `read` equal |
| deleted file's sha256 | `02122dec1e6aa760f0ec317cdc343172a06a55ea30962c160ac517c77e86cb5d` | `6726f85dae11409a69d3daee6ab4da2fcf2337506868fbd0fad566072caa6246` | `b76a1d93a09233716cb838c6c562ea276298bd3aa85bcd8f3c95f8ffa0ec79e0` |
| held at | `08798a8` | `08798a8` | `08798a8` |

The failing ids are `chart <width> <method> <text>` (R the Reviewer's method, S the seat's) with the measure left out, as the checks
name a text; the other checks (flat texts, script errors, sideways scroll, the accessibility tree, reduced motion, the scheme, the fonts) failed
nothing. The blocks below are what `test_shoalmark.py` compares a fresh run against (`SHOALMARK_REGENERATE=1`; `facts.mjs` on every run
where Node exists).

```json
{
  "file": "work-tracker/evidence/FM-006/landing/start-page/checks.json",
  "tested": "cb49101",
  "command": "git archive cb49101 | tar -x -C stage-cb49101 && (cd stage-cb49101 && uvx zensical@0.0.65 build); node work-tracker/evidence/FM-006/landing/start-page/checks.mjs stage-cb49101/site checks.json work-tracker/evidence/FM-006/landing/index.html",
  "checks": 18,
  "failing": [
    "chart 1440 R 54°10'N (under the title)", "chart 1440 S 54°00'N (under the title)",
    "chart 1440 S 54°10'N (under the title)"
  ],
  "generated_by": "node work-tracker/evidence/FM-006/landing/start-page/checks.mjs"
}
```

```json
{
  "file": "work-tracker/evidence/FM-006/landing/start-page/checks-r3-before.json",
  "tested": "9307cf8",
  "command": "git archive 9307cf8 | tar -x -C stage-9307cf8 && (cd stage-9307cf8 && uvx zensical@0.0.65 build); node work-tracker/evidence/FM-006/landing/start-page/checks.mjs stage-9307cf8/site checks-r3-before.json",
  "checks": 4,
  "failing": [
    "chart 1024 R 53°30'N", "chart 1024 R 53°30'N", "chart 1024 R 53°40'N", "chart 1024 R 53°40'N",
    "chart 1024 R 54°10'N", "chart 1024 R 54°10'N", "chart 1024 R 7°00'E", "chart 1024 R 7°00'E",
    "chart 1024 R 7°20'E", "chart 1024 R 8°20'E", "chart 1024 R 8°40'E", "chart 1024 R 8°40'E",
    "chart 1024 R BUTJADINGEN", "chart 1024 R Bremerhaven", "chart 1024 R DITHMARSCHEN", "chart 1024 R Ems",
    "chart 1024 R LAND WURSTEN", "chart 1024 R Norddeich", "chart 1024 R OSTFRIESLAND", "chart 1024 S 53°30'N",
    "chart 1024 S 53°30'N", "chart 1024 S 53°40'N", "chart 1024 S 53°40'N", "chart 1024 S 54°10'N",
    "chart 1024 S 7°00'E", "chart 1024 S 8°20'E", "chart 1024 S 8°40'E", "chart 1024 S BUTJADINGEN",
    "chart 1024 S Bremerhaven", "chart 1024 S DITHMARSCHEN", "chart 1024 S LAND WURSTEN", "chart 1024 S Norddeich",
    "chart 1440 R 53°30'N", "chart 1440 R 53°30'N", "chart 1440 R 53°40'N", "chart 1440 R 53°40'N",
    "chart 1440 R 54°10'N", "chart 1440 R 54°10'N (under the title)", "chart 1440 R 7°00'E", "chart 1440 R 7°00'E",
    "chart 1440 R 7°20'E", "chart 1440 R 8°00'E", "chart 1440 R 8°20'E", "chart 1440 R 8°40'E",
    "chart 1440 R 8°40'E", "chart 1440 R BUTJADINGEN", "chart 1440 R Bremerhaven", "chart 1440 R DITHMARSCHEN",
    "chart 1440 R Ems", "chart 1440 R LAND WURSTEN", "chart 1440 R Norddeich", "chart 1440 R OSTFRIESLAND",
    "chart 1440 S 53°30'N", "chart 1440 S 53°30'N", "chart 1440 S 53°40'N", "chart 1440 S 53°40'N",
    "chart 1440 S 54°00'N (under the title)", "chart 1440 S 54°10'N", "chart 1440 S 54°10'N (under the title)",
    "chart 1440 S 7°00'E", "chart 1440 S 7°20'E", "chart 1440 S 8°20'E", "chart 1440 S 8°40'E",
    "chart 1440 S BUTJADINGEN", "chart 1440 S Bremerhaven", "chart 1440 S DITHMARSCHEN", "chart 1440 S LAND WURSTEN",
    "chart 1440 S Norddeich"
  ],
  "generated_by": "node work-tracker/evidence/FM-006/landing/start-page/checks.mjs (chart part)"
}
```

```json
{
  "file": "work-tracker/evidence/FM-006/landing/start-page/facts.json",
  "tested": "bef2a1e",
  "command": "node work-tracker/evidence/FM-006/landing/start-page/facts.mjs bef2a1e work-tracker/evidence/FM-006/landing/index.html",
  "checks": 24,
  "failing": [],
  "generated_by": "node work-tracker/evidence/FM-006/landing/start-page/facts.mjs",
  "fields": {"sha": "bef2a1e2b84565f2533bc4acb9903e9de206252f", "release": "0.18.4", "counts": {"In Progress": 5, "Proposed": 3, "Shipped": 15, "Closed": 1}, "wrecks": 24},
  "sha256_without_read": "0ed4effe2d20b8d54f2409e8d62d2b18fb42a190cc77622f9226465d91946dd8"
}
```

## Rebuild

From the repository's root, Node 22 or later, `uv`:

    for c in 9307cf8 ab69afb 69552ed; do mkdir -p stage-$c && git archive $c | tar -x -C stage-$c && (cd stage-$c && uvx zensical build); done
    # STAGE/page = 69552ed's site/ (the page as v0.18.5 ships it; cb49101's for the slice's own), STAGE/r3-before = 9307cf8's, STAGE/r3-after = ab69afb's
    node work-tracker/evidence/FM-006/landing/start-page/render.mjs STAGE shots
    node work-tracker/evidence/FM-006/landing/start-page/checks.mjs STAGE/page checks.json work-tracker/evidence/FM-006/landing/index.html
    node work-tracker/evidence/FM-006/landing/start-page/checks.mjs STAGE/r3-before checks-r3-before.json   # its chart part kept
    node work-tracker/evidence/FM-006/landing/start-page/facts.mjs bef2a1e work-tracker/evidence/FM-006/landing/index.html

This folder is `start-page/`, not `site/`: the root `.gitignore`'s `site/` matches any folder of that name.
