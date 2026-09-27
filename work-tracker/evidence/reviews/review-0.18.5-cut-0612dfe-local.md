# Review — the 0.18.5 cut at 0612dfe, the same-session pass before the Owner's cold session (2026-09-26/27, Reviewer, session `8e509911/reviewer-37`)

- **Date:** 2026-09-26 23:11 – 2026-09-27 00:20 CEST.
- **Seat:** Reviewer (Opus 5.5, highest effort), a sub-agent of Principal session `8e509911`.
- **Session:** `8e509911/reviewer-37`.
- **Worktree:** `shoalmark-review-3`, detached at the tip. The suites and the gates ran here and the tree was clean after
  each run. Every clone, build, vendoring, render and measure ran in the session's scratchpad (a clone of `origin` at the
  tip, one at `v0.18.4`, checkouts at `b9644b7e`, `bef2a1e`, `2a9f7eb`, `361336a`, `cb49101`, two consumer
  repositories). The Owner's checkout, `shoalmark-gtm`, every other worktree and every folder of session `8b91dba2`
  stayed outside every command.
- **Tier:** *code — a release, critical*, the full loop: NOT READY on any P2, with the fix named.
- **Independence:** *same session — a sub-agent of 8e509911; the cold session follows* (the Owner's path line 3). Its
  Implementer was `8e509911/implementer-39`. Reported as such, not independent.
- **The measure:** the cold brief's checklist (`brief-review-0185-cut-cold.md`, *Verify, by running it*), run item by
  item; and the Owner's intent against what the tree renders — FM-002's answer `4e00f85`, his words of 09:23:58 and
  10:25:41 (filed whole under `evidence/FM-002/`, their three hashes re-computed and equal), his rule of 16:0x (*the
  mockups are taken as-is, nothing changed or added; direction kept*) and his approval of slice A's renders at 16:06.
- **Clock:** the suites ran 23:12–23:51 CEST, before midnight, so without `TZ=UTC`; the verdict commit is made after
  midnight with `TZ=UTC` (FM-028), so the hook keeps INDEX.md's date.

**Reviewed:** `release/0.18.5` at **`0612dfe3d3ade969e048ebb98abcca3b6db6d299`** (pushed 23:09:35; ls-remote 23:11 and
00:17). Base: slice B's verdict tip `9704145` (carrying slice A at `b9644b7e`); `631a8bc` merges slice L's verdict tip
`dd88edc` — its tree is `git merge-tree --write-tree 9704145 dd88edc`'s own (`361cb586`), no hand edit; then the cut:
`3826a03` VERSION 0.18.5, `84bc65d` FM-039 filed by `--new`, `522db92` the start page's three version strings,
`0612dfe` the 0.18.5 section. `origin/main` is `bef2a1e` and an ancestor of the tip. No pull request is open.

## The cold checklist, item by item

| # | Item | How | Result |
|---|---|---|---|
| 1 | Suites on an idle machine | `uptime` logged at each start and end; one interpreter at a time | **3.9.6:** `test_shoalmark.py` **481 ok**, `test_core.py` **148 ok**, *skipped here: 0 checks — every check ran*, *all green* (23:31–23:40, load 2.62 → 3.24). **3.14.3:** `test_core.py` **148 ok**. `test_shoalmark.py`'s first run (23:12–23:23, started at 3.94) read **480 of 481**: the one failure is FM-035's healthy-board case, the 5 s budget FM-039 files; the load rose to 10, and another session's 3.14 run of the same suite, in `shoalmark-principal-4`, overlapped it. **Re-run at load 2.89 (23:40–23:51): 481 ok, 0 skipped, all green**, the case *ok*. Counted green. `git status` empty after every run. ✓ |
| 2 | Gates, the fresh clone, the site, the queue | this worktree; a fresh clone of `origin` at the tip with `GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null` | `--check` **0** (*INDEX.md is up to date — 39 trackers*; *judged before build: on*; *the Owner's two sections: guarded*; *filing freeze: 21 open … only bug filings*). `--session-check` **0**. The fresh clone, no `allowedSignersFile`: exit 4, **one** finding (the checkout's, six signed commits named), *INDEX.md is up to date*, **no STALE**. `uvx zensical build` (0.0.65): *No issues found*; the built `index.html` names `v0.18.5` three times and carries no `{#`; `setup.html` and `de/setup.html` clone `--branch v0.18.5`; **no built page names v0.18.4**. `--queue`: `release/0.18.5 @ 0612dfe  wait: no pull request — no verdict on 0612dfe`. ✓ |
| 3 | A consumer that chooses nothing sees no change | two repositories, both named `acme`: one vendored from the `v0.18.4` tag, one from the tip (`--allow-untagged`; *19 files, pinned*); the same `--init --key ACME`, the same four trackers, one commit at a fixed date; the board built; board, search, tracker and story views, 1440/1000/390 px, light and dark, full page | The two scaffolds are identical (`diff -r`), `view/` identical. **24 of 24 renders differ only in one 7×9 px box: the running line's last digit, `v0.18.4` → `v0.18.5`** (48–49 px, seen). The HTML differs only in the three hooks, the default CSS line, the label table and the version. Vendoring the tip over the 0.18.4 copy prints *(was 0.18.4)* and the 0.18.5 section whole; `--brand` there marks the tool's `brand/` *no brand file here: its themes/ are starters*. ✓ |
| 3b | `--from` renders as the committed mocks | FM-006's `build-mocks.py` (unchanged since `9467b83`) on this repository's board as main's tool builds it (`bef2a1e`'s tool and brand, the tip's trackers), `--plex` the shipped cuts; against the tip's tool with the same brand and each starter worn from the person's place, written by `--brand $XDG/shoalmark --from <theme>`; board, search, tracker, story, the acts dialog; 1440/1000/390, light and dark, full page | **shoalmark and monochrome: search and tracker 0 px (24 of 24).** Board and story 313–420 px each, all in one 100×12 px box at the search field — (310, 90) at 1440, (43, 66) at 390: the placeholder, the one marked rule. The dialog adds its note's placeholder (1,620–2,161 px). **No other pixel differs.** `--from catkin`: exit 2, *the tool ships no such theme — monochrome or shoalmark; nothing was written*, no folder made. `--from` alone: exit 2. A second `--from` into a filled place keeps all five files. The copy is `diff -r`-equal to the theme's folder. ✓ |
| 4 | The three hooks | item 3's renders; `grep` of `brand/themes/` | No visible change without a theme (item 3). Both starters style hook 1 (`#p>.pt`) and hook 2 (`#F`); outside their comments, no `#p::before` rule and no lift rule (`~ #r`) remain, and no `WORKAROUND` mark (monochrome's one hit is its header naming the mock's two). Hook 3 (`zebra`) is used by neither: `shoalmark` keeps the mock's `tr.t:nth-child(even)` stripe, marked where it stands — the Principal's ruling at `9f2f525` on the Owner's *as-is* (slice B pass 1, R4: `tr.zebra` changed 266,939–364,075 px against the mock). The README says *a theme styles three hooks*; that holds. ✓ |
| 5 | shoalmark's own board and site wear `shoalmark` | **(a)** slice A's approved state — `b9644b7e`'s tool and brand — against the tip's, both on the tip's trackers, built seconds apart; board, search, tracker, story, the acts dialog (its *done* clicked); 1440/1000/390, light and dark, full page. **(b)** `#H`'s box probed. **(c)** slice A's committed `checks.mjs` on the tip's built board, its tracker view and dialog, and a themed site page (`setup.html` served as the stage's start page — `index.html` is now the landing page). **(d)** slice A's committed `render.mjs` on its own *Rebuild* at the pinned shas, against the 16 committed PNGs | **(a) 30 of 30 byte-identical** — what the Owner approved at 16:06 is what ships, slice B's re-cut included. **(b)** `#H` at (283, 48), 874×18, inside the chart's top border, **in both schemes**. **(c)** AU-16: 0 figures and 0 markers read on the board, tracker view, dialog and site, both schemes; the control, alt text removed, reads 261 figures and 37/18 markers. AU-18: 838 px, 8.4 px a character, **99.8 characters**, the longest line 99 of 56. Contrast: 920 measurements a scheme, **0 below 4.5:1** — by day lowest 5.76 (`#526214` on `#e3eff7`), under a chart line 4.87; by night 5.98. The pipeline's control reads 4.542. The tracker view: after = mock, (283, 62). **(d)** 12 of 16 identical; the two board *after* 1440 differ in the sessions band (y 988–1000), the two *before* in the same band (y 845–1000) — the clock; *site after 1440 light* by 327 px in the nav's *Deutsch* — antialiasing, as slice A's pass saw. The renders are their sources'. See R3 for the recipe. ✓ |
| 6 | The landing page | built at the tip; slice L's committed `render.mjs` and `checks.mjs` on it; the same `render.mjs` on `cb49101`'s build; my own reading of `bef2a1e`'s trackers against `WRECKS` | It is the site's start page, every other page keeps its chrome. **24 wrecks** — the page says *from main at bef2a1e*, and `bef2a1e` holds exactly 24 trackers tagged `bug`/`security` (the brief's *23* is the mock's count, before FM-038): status, title and link equal for all 24; 15 Shipped, 5 In Progress, 3 Proposed, 1 Closed; FM-039, filed at the cut, is not on the chart, as the CHANGELOG says. **R4:** each of the 24 reports is a prefix of its tracker's `hook:`. **R3:** lowest chart text 4.80:1 at 1024 px (both methods); at 1440 px the two west-edge figures under the title read 3.99 R / 1.30 S — slice L's carried *not a finding*, his to strike, named in FM-006; flat pairs lowest 5.14; the foot's fine print 5.69. **No script error** at 1440, 1024, 390; no sideways scroll; 24 focusable wrecks, no chart figure read; **reduced motion: two captures 7 s apart identical**; a light preference draws the same pixels. `checks.json`'s summary at the tip equals the committed one but the page's height, 5819 → 5837. The committed renders re-render at `cb49101` **0 px** on all six first screens; at the tip they differ in 459–460 px, a 28×29 box: the HUD's `v0.18.4` → `v0.18.5` (seen) — see R4. ✓ |
| 7 | CHANGELOG against the commits; VERSION, running line, clone tag; front matter | `git log v0.18.4..0612dfe --no-merges` (57 commits, every subject read) and main's merges since the tag; `git diff --name-status v0.18.4 0612dfe -- 'work-tracker/*.md'`; the cut's own diffs | Every PR and sha a bullet names is the commit it claims: PR 82, 87, 88, 89, 90 (`4e00f85`, 13:54:50), 91 (`8defe63`), 92, 93; `9467b83`, `9f2f525`, `bef2a1e`, `f11bc04`. FM-039's numbers are `9f2f525`'s body's and the pass's row 9. FM-031's open line is its tracker's. `VERSION` 0.18.5 = the newest heading = the setup pages' `--branch v0.18.5` = the board's running line = the start page's HUD, foot link and fine print. The README carries no version line. `shoalmark.py:1300,1317` and the suite's case names keep `0.18.4`: each names the release a behaviour was built in — right to leave. **The cut changes no tracker's front matter:** its only tracker change is FM-039's new file, written by `--new` (`considered:` filled from `--related`, as its brief says), and INDEX.md by the hook. **No status flip:** FM-002, FM-006, FM-031 stay In Progress, FM-038 and FM-039 Proposed — as 0.18.4's cut left FM-030 and FM-037; the flips are the tag's same-day pass. Findings R1 and R2. ✓ |
| 8 | The gate and the hooks | `git diff 631a8bc 0612dfe` and `git diff v0.18.4 0612dfe` on the gate paths; every top-level function of `shoalmark.py` hashed at `v0.18.4` and at the tip | The cut's own commits touch no `shoalmark.py`, suite, `lefthook.yml`, `scripts/`, `.github/` or `shoalmark.toml`, and since `v0.18.4` none of the last four changed at all. Slice B's `shoalmark.py` changes: `HTML_PAGE` (CSS, markup, `draw()`), `LABELS` (`owner.title`), `brand_report`, `render_schema`, `parse_args`, `vendor`, `main` (the flag table, one call), and two new, `shipped_themes` and `theme_files`. **Byte-identical:** `build_judgement`, `commit_msg_check`, `commit_msg_hook`, `judge_commits`, `guard_walk`, `guard_lines`, `guard_proof`, `triage_guard`, `triage_pending`, `lint`, `pin_problems`, `verified_as`, `trusted_signers`, `queue_actions`, `session_check`, `install_hook` and every other gate's. `git merge-tree --write-tree origin/main 0612dfe`: clean. ✓ |

## The Owner's intent against what the tree renders

- **FM-002's answer, option 2** — the tool ships both starters (`brand/themes/`, vendored and pinned: item 3); this
  repository's board wears `shoalmark` (item 5a, 0 px against his approved state) and its site's pages wear it (item 5c).
  Kept.
- **09:23:58, the header inline inside the graticule, both themes, the site excluded** — `#H` at (283, 48) inside the
  border in both schemes on this board; both starters equal the aligned mocks (`9467b83`) in every view but the
  placeholder; the site's header untouched. Kept.
- **10:25:41, the landing page for v0.18.5** — the mock his word points to (`9704140`, PR 82) is the site's start
  page; *start page* is the seat's reading, his to strike, and the record says so. Kept.
- **16:0x, the mocks as-is, nothing changed or added** — the board and the starters: no pixel but the marked
  placeholder (item 3b; slice A's placeholder, 3.63 → 6.42:1 by night). The site: the foot's link rule, marked (slice A,
  1.12 → 13.69:1). The landing page: the built page against the mock differs in the edits marked in
  `overrides/landing.html` and nothing else (the diff read line by line) — **(c)** R3, the overlay's contrast, his to
  strike; **(a)** the facts dated, the release included (the cut's `522db92`); **(b)** R4, the reports his trackers'
  own first sentences; **(d)** the fonts' loading, the same faces and pixels. (a), (b) and (d) are outside the three
  marked, rule-forced deviations the brief names. I judge none a P2: (a) and (b) keep the page true to the sources the
  mock's own README names for every fact and report — the mock's reports were paraphrases presented as the trackers'
  own words — and (d) changes no pixel; none changes a colour, a layout, a section or the direction. The judging pass
  he merged (PR 93) required R3 and R4 in the build. The German start page's one added line is on a page no mock
  covers, the seat's default, his to strike.
- **16:06, slice A's renders** — 30 of 30 renders of this board byte-identical to his approved state (item 5a).

## Findings

**R1 · P3 · confidence 95% on the facts, 70% on the grade · Two of the Owner's chat words are quoted in the 0.18.5
section altered, without their marks.**
- *The gap:* the slice L bullet quotes 10:25:41 as *for the v0.18.5 release we also add a landing page requirement,
  alongside the restyle and rebrand of shoalmark's brand identity*. Filed whole (`owner-words-2026-09-26-1025.md`):
  *for the `v0.18.5` release we also add a landing page requirment, that goes alongside the re-style and re-brand of
  `shoalmark`s brand identity*. Spelling and idiom are normalised and *that goes* is dropped, and the bullet carries no
  *spelling normalised* mark (the start page's evidence README does). The slice B bullet quotes 09:23:58 with its mark,
  but *over this variant, where the header sits outside the graticule* drops *used in the dar mode* between *variant*
  and *where*, with no `…`; the one `…` covers another span.
- *Why it matters:* a release note is where a consumer and the Owner read what he said; normalising his words is the
  house rule only when marked.
- *What closes it:* *(spelling normalised, not a signed answer)* on the slice L quote, and *used in the dark mode* (or
  a second `…`) restored in the slice B quote.

**R2 · P3 · confidence 90% on the facts, 65% on the grade · The closing list names FM-033 among the trackers touched,
and no commit since `v0.18.4` changes it.**
- *The gap:* *Trackers touched: … FM-033, FM-034, FM-035 and FM-036, by the passes only.* `git diff --name-only v0.18.4
  0612dfe -- 'work-tracker/FM-033*'` is empty. The passes applied FM-033's rule and read its gaps; they changed FM-034,
  FM-035 and FM-036 by `fix` rows.
- *What closes it:* FM-033 out of the list, or *FM-033's rule applied by the pass* where the *Also since 0.18.4* line
  already says it.

**R3 · P3 · confidence 95% on the facts, 75% on the grade · Slice A's R1 and R2, both marked *fixed forward*, are
unfixed at the release tip, and R1 now bites.**
- *The gap:* slice A's evidence README, *Rebuild*, takes *before* with `git checkout origin/main -- …` and *after* with
  `git checkout HEAD -- …` of two stylesheets only. At `0612dfe` HEAD's start page is slice L's landing page, so the
  recipe's *after* site renders the landing page, not the start page its committed `site-after-*.png` show; once the
  Owner merges the slices first, as the cold brief says he will, `origin/main` gives *after* as *before*. Slice A's R2 —
  the site foot's one deviation from the mock in no committed render — is open too.
- *Seen:* the recipe with `2a9f7eb` and `361336a` in place of the two moving refs rebuilds the 16 committed renders
  (12 identical, 4 differing only in the clock's band and one antialiased word; item 5d).
- *What closes it:* the README's *Rebuild* names `2a9f7eb` and `361336a`; and the foot's render (FM-006's `render.mjs`
  *foot* shot), or its measure in the README's table, for R2.

**R4 · P3 · confidence 95% on the facts, 60% on the grade · The start page as the release ships it is in no committed
render, and its evidence README still reads v0.18.4.**
- *The gap:* `522db92` changes the page's HUD, its foot's link and its fine print, which grows by one line (5819 →
  5837 px). The committed `start-page/shots/` are `cb49101`'s (they re-render there at 0 px), and the README's table
  (a) reads *release v0.18.4 … unchanged from the mock*. The Owner's rule of 07:41 is *real renders … He sees them
  before the merge*.
- *What closes it:* slice L's `render.mjs` on the tip's build into `shots/` (three first screens and three full pages),
  and row (a) naming the cut's re-read (`522db92`). Or one line in the README naming `522db92` and saying the renders
  predate it.

**R5 · P3 · confidence 90% on the facts, 60% on the grade · `NOTICE` does not name the fonts 0.18.5 bundles into every
vendored copy.**
- *The gap:* `NOTICE` names one bundled third-party component, `marked`, with its licence. 0.18.5's `--vendor` copies
  six IBM Plex Mono files (`brand/themes/*/fonts/`, SIL OFL 1.1, Reserved Font Name *Plex*) into every consumer, and
  `NOTICE` travels with them. The OFL's own condition holds — each copy carries `fonts/LICENSE.txt`, byte-identical to
  IBM's.
- *What closes it:* one `NOTICE` line: *This product bundles IBM Plex Mono (`brand/themes/*/fonts/`), Copyright 2017
  IBM Corp., with Reserved Font Name "Plex", under the SIL Open Font License 1.1.*

## Noted, not findings

- **The section's date.** `## 0.18.5 — 2026-09-26` is the cut's day. If the Owner tags on 2026-09-27, it is **two lines,
  not one**: CHANGELOG.md:5 and `overrides/landing.html:466`, *v0.18.5, released 26 September 2026*. Not a finding at
  this tip, where the tag's day is unknown; precedent: 0.18.3 was cut on 2026-09-24, tagged on 2026-09-25 and kept its
  heading, and its independent review found nothing. If he tags on the 27th and wants the tag's day, it is a P3: the
  two lines in one commit before the tag, or *cut 26 September* on the page.
- **`git diff --check origin/main...0612dfe` exits 2**, only on the two `brand/themes/*/fonts/LICENSE.txt`: CRLF, as
  IBM's package ships them, byte-identical to it. This repository's own `work-tracker/brand/fonts/LICENSE.txt` is CRLF
  since 0.18.2. Everything else is clean.
- The cold brief says *23 wrecks* (the page has 24 at `bef2a1e`) and `…/FM-006/landing/site/` (the folder is
  `start-page/`: the root `.gitignore` matches `site/`).
- A theme copied with `--from` over a full place prints *yours to change* and exits 0 though nothing was written; each
  file says *kept*. As slice B's pass read it.
- The two P3s of slice L (R1 three qualifiers, R2 the absolute links and the favicon) are the Owner's to rule and stand
  in the CHANGELOG as *open* lines.

## Not verified

- The tag's five-job CI matrix, Windows in particular for the new theme and vendoring checks; the tag is the Owner's
  act after the merges.
- Firefox, Safari, print, a real phone (390 px is Chrome's device metrics), a screen reader.
- The site live: `docs.yml` deploys only while the repository is public.
- A vendoring from the `v0.18.5` tag: the tip was vendored untagged.
- Independence: same session, not independent.

## Verdict

**READY WITH FINDINGS** — R1 to R5, all P3; no P2. Tier *code — a release, critical*. Independence *same session — a
sub-agent of 8e509911; the cold session follows*.

**Confidence that the cold session finds no P2: 70%.** For: every checklist item ran and held; the board he approved is
byte-identical in 30 renders; the starters and the consumer's board differ from their references only by the marked
placeholder and the version digit; 481 + 148 green on both Pythons, 0 skipped. Against: R3 and R4 are evidence that
does not re-render at the tip, and a cold reading of *the renders are the committed sources'* could grade that higher;
the date line if the tag falls on the 27th; what I could not run — the CI matrix, other browsers.

The Owner lands this by merging; a merge rules nothing.
