# Review — FM-006 slice L, the landing page is the site's start page (2026-09-26, Reviewer, session `8e509911/reviewer-36`)

- **Date:** 2026-09-26, from 18:51 CEST.
- **Seat:** Reviewer (Opus 5.5, highest effort), a sub-agent of Principal session `8e509911`.
- **Session:** `8e509911/reviewer-36`.
- **Worktree:** `shoalmark-review-2`, detached at the tip. Every build, render and Chrome run was made from `git archive`
  exports in the session's scratchpad. The Owner's checkout, `shoalmark-gtm`, every other worktree and every folder of
  session `8b91dba2` stayed outside every command.
- **Tier:** docs/site, one pass — the tier the judging pass gave slice L (`13d70189`). A P3 is fixed forward; a P2 sends
  it back.
- **Independence:** same session — a sub-agent of `8e509911`. The seven slice commits are `8e509911/gtm-5`'s
  (`Worktree: shoalmark-impl-3`), a sibling sub-agent of the same Principal. Reported as such, not independent.

**Reviewed:** `fm/006-the-landing-page` at `21bf14ecbac714f091cc14513ac1054c8bd480b7` (pushed 18:50:23).
- `git ls-remote` at the start gave `21bf14e…` for the branch; `origin/main` is `bef2a1e`.
- The branch is slice A's verdict tip `b9644b7e` + main `bef2a1e` merged at `25e0d58` (a clean merge: its tree is
  `git merge-tree`'s own, `91f7b52`) + seven commits: `9307cf8` the page, `ab69afb` R3 and R4, `e26c648` the facts,
  `a0daf0c` the fonts, `cb49101` the German line, `08798a8` the renders and checks, `21bf14e` the record.

**The Owner's rule, the measure of this pass:** the mock `work-tracker/evidence/FM-006/landing/index.html` is taken as
it is, full-bleed, no site chrome, nothing added. The only edits are (a) the facts dated, (b) R4's report cuts, (c) R3's
overlay contrast, rendered before and after for him to strike, and (d) the fonts' loading. Any other difference from
the mock is a finding.

## The checks

| # | Check | How | Result |
|---|---|---|---|
| 1 | Scope | `git diff --name-status 25e0d58 HEAD` (the slice's own; `b9644b7e...HEAD` adds main's ten merged paths) | 26 paths: `docs/index.md`, `docs/de/index.md`, `overrides/landing.html` (new), FM-006's tracker, `CHANGELOG.md`, and 21 files under `evidence/FM-006/landing/start-page/`. No `.github/`, `shoalmark.py`, test, `brand/`, `docs/stylesheets/`, `zensical.toml` or `lefthook.yml` against `b9644b7e` ✓ |
| 2 | The start page is the mock | `uvx zensical build` (0.0.65) at `9307cf8`, `ab69afb`, `25e0d58` and the tip; `diff` of each `site/index.html` against the mock | At `9307cf8` the built page is the mock byte for byte but its final newline. At the tip it differs in 9 hunks, every one inside (a)–(d), listed under *Differences*. No header, nav, sidebar, search or footer ✓ |
| 3 | The nav's other pages | `diff -rq` of the `site/` built at `25e0d58` and at the tip | Only `index.html`, `de/index.html` and `search.json` differ; every other page is byte-identical ✓ |
| 4 | The German start page | the built `de/index.html` against `25e0d58`'s | One paragraph added under the claim, *Die Startseite, auf Englisch: eine Seekarte des Wattenmeers, …*, linking `../index.html`; its words are otherwise unchanged ✓ |
| 5 | Every fact of the old `docs/index.md` reachable | the seat's table, each row checked in the built site; `grep` of `docs/*.md`, `docs/agents/` and `README.md` | Holds but for three sentences, as the seat says (R1) |
| 6 | R3 — the chart's texts as drawn | my own script (`contrast.mjs`, not the seat's): every `.name`, `.fig` and `.wreck span` shown, reduced motion, the overlay in place, by **R** (the pass's: the specified colour, darkened by each layer drawn above it by the factor that layer darkens the ground under its box, against the box's median ground with the text transparent and its halo off) and **S** (the seat's: the glyph core's median pixel as drawn against the same pixels with the text transparent) | **Before** (`9307cf8`): lowest 2.65 R / 2.81 S at 1440 (`53°30'N`), 2.74 / 2.80 at 1024; 19 / 16 texts below 4.5 at 1440. **After** (the tip): lowest **4.80** by both, `OSTFRIESLAND`, at 1440 and at 1024; 0 below 4.5 of 74 at 1440 and 76 at 1024, the two under the title aside. The seat's numbers reproduce (its S found 4.72 for `JUIST`; mine 4.99). At 1280 and 1920 too: lowest 4.80 R, 4.56 S ✓ |
| 7 | The two figures under the title | the same, at 1440 | `54°10'N` and `54°00'N` on the west edge: S 1.30 and 1.53 — they lie under the claim and the lede. Judged under *Not findings* |
| 8 | The flat pairs | the seat's `checks.mjs` re-run on my build of the tip | Its `chart`, `flat`, `tree`, `motion`, `scheme`, `fonts`, `errors` and `hosts` sections are identical to the committed `checks.json`. The lowest flat pair is 5.14 (a raised wreck's id on the register's zebra), 363 runs at 1440 px, none below 4.5 ✓ |
| 9 | R4 — the reports | my own reading of main at `bef2a1e`: each wreck's `report` against its tracker's `hook:` | **24 reports compared**: each is a prefix of its hook, cut at a sentence's end, backticks balanced; 14 of one sentence, 10 of two. Against the mock: 18 changed, 5 as they were (FM-009, FM-020, FM-022, FM-029, FM-030), FM-038 new — the seat's count ✓ |
| 10 | The facts, dated | my own reading of `bef2a1e`: every `work-tracker/FM-*.md` tagged `bug` or `security`, its status, `# ` title and URL, and `git log --diff-filter=A` (the earliest, its day in Europe/Berlin); `VERSION`, the tag, `CHANGELOG.md`; the board rendered in Chrome from `git archive bef2a1e` | The page's 24 wrecks are exactly main's 24 bug/security trackers of 38 (FM-038 filed at `5558b1a` after the mock). Status, title, incident ID, filing day and link match for every one; 5 In Progress + 3 Proposed = 8 open, 15 Shipped, 1 Closed, as the HUD and the register's summary say; *22–26 September*. `VERSION` 0.18.4, `v0.18.4` on `a7e5291`, `## 0.18.4 — 2026-09-26`. The board at `bef2a1e` reads *waiting for you: 0*, *your acts, with their time: 4*, the first FM-006's with **done** and **reschedule**, as the excerpt shows; its answer's middle is cut and marked `…`. One sha and one time on the page's foot (*18:00 CEST, bef2a1e*) and in the README (*18:00:51 CEST*). `facts.mjs` re-run gives `facts.json` but its read time ✓ |
| 11 | FM-038's position | my own search of the chart canvas by the seat's stated rule | The farthest flat pixel from every other wreck and name, 12 chart pixels inside the border, outside the title, its 7 × 5 footprint flat or sand, is (61, 184) = 7.0737 E, 53.5422 N: the page's 7.077 E, 53.54 N, the same pixel ✓ |
| 12 | Fonts | the built page's `<link>`s and loaded faces; the site's other pages | One Google Fonts load: Plex Mono 400, 400 italic, 500, 600 and Silkscreen 400, 700, the family from `[project.theme.font]` `code`, the theme's one preconnect and `display=fallback`, as every other page loads its fonts. No second Plex load, Silkscreen once. Self-hosting is named as due before publication (FM-006's clause of `412240e`, the slice's clause, the template's comment) ✓ |
| 13 | The renders are real | my own renders (`render-mine.mjs`) of the tip's build, Chrome offline but for the two Google Fonts hosts, at 1440, 1024 and 390 px, as the seat describes them; compared pixel by pixel with the 13 committed PNGs | Every size matches. The 3 reduced-motion shots and the 4 R3 before/after shots are pixel-identical. The 6 motion shots differ in 0.14–1.00 % of pixels, every region at a moving part: the convoys, the open wrecks' shuffle, the *press start* cursor, the ticker. R3's change is 0.93 % of the chart's pixels at 1440 px and 1.88 % at 1024, as the README says. No PNG carries a chunk but `IHDR`, `IDAT`, `IEND` ✓ |
| 14 | The page as a page | the same runs | No script error; the only failed request is `/favicon.ico` (see R2). No sideways scroll at 1440, 1024 or 390. The accessibility tree: 24 wreck buttons, all focusable, each named with its number, status and title; the canvas an image with its description; no chart figure and no chart name read (the one *PRICKEN* in the tree is the key's `<b>pricken</b>`). Reduced motion: two full captures 7 s apart are identical. A light preference draws the same pixels as a dark one at all three widths ✓ |
| 15 | His FM-006 answer not built here | the slice's removed lines; `.github/` | The slice removes one line — FM-006's landing clause, rewritten in place. No client name or parent trace removed; no workflow changed. A screen of the added text finds no path, address, key, token or client name ✓ |
| 16 | The record | FM-006's diff; `CHANGELOG.md` | The ship-log row is on top; the *What is true now* clause says the page is built as the start page, not merged, with the four edits and the follow-ups, beside `412240e`'s clause that the site is built at a tag and live only at the go-public act (the judging pass's R1). `## Unreleased — 0.18.5` gains one bullet naming FM-006 and his word of 10:25:41, *built at the release tag and live when the repository is public* ✓ |
| 17 | Gates at the tip | `--check`, `--session-check`; `test_shoalmark.py` and `test_core.py` on 3.14.3 and 3.9.6; `git merge-tree --write-tree` | Suites 462 + 148, green on 3.14.3 and 3.9.6, 0 skipped. The first runs, one interpreter at a time at load 6–12 (19:10–19:31), failed only FM-035's healthy-board case on its 5 s budget (461 + 1 on both); `test_shoalmark.py` re-run at load under 6 — 3.14 19:33–19:42, 3.9 19:42–19:51 — 462, green. `test_core.py` 148 on both at the first run. `--check` exit 0 (*INDEX.md is up to date — 38 trackers*); `--session-check` exit 0. Merge-tree clean against `origin/main` `bef2a1e` (tree `4c7c83a`) and against slice B's tip `9f2f525`, not merged (tree `0750ea2`) ✓ |

## Differences from the mock

The built page against `work-tracker/evidence/FM-006/landing/index.html`, all 9 hunks:

- **(d)** the `fonts.googleapis.com` preconnect dropped; the stylesheet link's family from `[project.theme.font]`, `&amp;`
  for `&`, `display=fallback` for `swap`.
- **(c)** `.fig` z-index 5 → 7; `.name` z-index 4 → 7.
- **(a)** the HUD's source figures 23 / 10 → 24 / 8; the board's excerpt (*waiting for you: 0*, *your acts: 4*, FM-006's
  act); one sentence on the foot, *read on 26 September 2026, 18:00 CEST from main at bef2a1e*; the register's summary,
  *22–26 September*; `WRECKS` — FM-038 added, FM-034–036 Shipped, FM-037's title in main's case.
- **(b)** 18 reports in `WRECKS`.
- The final newline, which the template engine drops.

**Beyond the four edits: none.** The Jinja comments marking each edit are dropped by the build.

## Findings

**R1 · P3 · for the Owner · confidence 90 % on the facts, 70 % on the grade · *Every fact reachable* does not hold for a
person reading the English site: three sentences of the old `docs/index.md` are now on no English page.**
- *The gap:* the page is the mock, and the mock does not carry them:
  - the count's qualifier — *a commit's date is when it was made, not when it was pushed: the forge's push events
    confirm the counted pull requests from 24 September 2026, 05:18 UTC on*. The page prints 12/15 and 10/37 and their
    counting note without it;
  - *a report, not a proof: git cannot yet show it*, on the board's independence count. `standup.md`'s *Which review
    was independent* makes the claim without it;
  - *every signature names the key that made it*. `signing.md` does not say it.
- Where they still are: the German start page (the English start page does not link it; every other page's nav does);
  `docs/index.md`, whose prose the site's search still indexes, so a hit lands on a page that does not show the words;
  and the Markdown twin `scripts/llms_txt.py` writes at deploy, behind the page's `llms.txt` link — for agents, after
  publication, not in a local build.
- *Why it matters:* the brief asked that no fact be lost; the rule that takes the mock as it is forbids the copy that
  would keep them. The seat names all three, in the README and in FM-006's clause, as his to rule.
- *The smallest cure, his call:* one sentence each where its claim stands — the push-events sentence in the page's
  counting note (a fifth edit his rule must allow), the qualifier under `standup.md`'s count, the key sentence in
  `signing.md`'s *What your record says* (two nav pages changed). Or he accepts them as lost.

**R2 · P3 · for the Owner · confidence 85 % on the facts, 65 % on the grade · The start page's links are the mock's
absolute `holgo99.github.io` addresses, and the page has no favicon.**
- *The gap:*
  - its 6 site links and its `llms.txt` alternate point at `https://holgo99.github.io/shoalmark/…`. No Pages site exists
    until the go-public act, so in a local build — the `site/` he asked to see after every pull (FM-006, 2026-09-25) —
    the start page's links leave the build for a host that serves nothing, and the page carries no site nav, only its
    own section anchors;
  - at the flip the site's address changes (FM-006's *home at the flip*: *the docs site's address* is on that slice's
    list). `overrides/landing.html` is one more place that names the old one, and the list does not name it;
  - extending no theme template, the page carries no `favicon.svg` link; the browser asks for `/favicon.ico` and gets a
    404, where every other page shows the site's `favicon.svg`.
- *Why it matters:* the old start page reached every page by relative link and by the nav. The seat names the local
  build's part in its README; the rule forbids the edit.
- *The smallest cure, his call:* the five site-relative addresses (`setup.html`, `signing.html`, `standup.html`,
  `agents/README.html`, `llms.txt`) and one favicon line — a fifth edit his rule must allow. Or a line on the flip's list
  naming `overrides/landing.html`.

## Not findings

- **The two west-edge figures under the title at 1440 px** (S 1.30 and 1.53): the seat's call holds. They are covered by
  the claim and the lede, where the mock's title stands on the open sea; the same latitudes print on the east edge at
  6.38 and 6.59; at 1024 px, where the title stands above the chart, both read 6.4 or more. Lifting them would print them
  across the h1. The pass that found R3 named one of them as a separate case. If he wants the letter of 4.5:1 for every
  figure, the cure is to leave out the west-edge figures the title covers — a fifth edit. Confidence 75 %.
- **The fact reader in Node:** the hook runs the suites only when a `.py` file is staged (FM-038), so none of the seven
  commits ran them, and the seat's by-hand numbers are not in the record. What had to run ran at this pass (row 17): the
  suites read no evidence script, and they do read docs pages, which they checked at this tip. Nothing was avoided that
  did not then run.
- **The board excerpt's `…`:** the cut is marked, and it keeps the page from printing what goes public before the act.
- **`display=fallback`:** the theme's own; with the fonts' host slow past 3 s, the fallback face stays, as on every
  other page.
- **Wider than the brief's widths:** at 2240 px (k = 7) the east edge's `53°50'N` crosses the coastline: R 2.27 (the
  box's median ground is land), S 6.43; on the mock 1.52 / 4.80 — the pass's own *crosses the coastline* case, not the
  overlay.

## Verdict

**READY WITH FINDINGS** — R1 and R2, both P3 and both his to rule; no P2.

- The built start page is the mock, full-bleed, with no site chrome; the nav's other pages are byte-identical; the only
  differences are the four edits his rule allows.
- R3 holds as drawn: the lowest chart text is 4.80:1 by both methods at 1440 and 1024 px, from 2.65; the flat pairs from
  5.14. R4 holds: 24 reports, each its hook's first sentences, verbatim.
- The facts are main's at `bef2a1e`, dated on the page and in the README; the renders are the built page's.
- The German start page keeps its words and gains one line.
- Not verified: Firefox, Safari, a screen reader, print; the page over a slow or blocked font host; the live site, which
  does not exist before the go-public act.

*The Owner lands this by merging; a merge rules nothing.*
