# Review — the pass after the tag, 2026-09-27 (Reviewer, session `8e509911/reviewer-36`)

- **Date:** 2026-09-27, from 12:18 CEST.
- **Seat:** Reviewer (Opus 5.5, highest effort), a sub-agent of Principal session `8e509911`.
- **Session:** `8e509911/reviewer-36`.
- **Worktree:** `shoalmark-review-2`, detached at the tip. I made the `--clear-ask` and `--triage` reproductions, the
  `--brand --from` run and the board's renders in scratch clones and a `git archive` of the tag, all in the session's
  scratchpad. In those clones, signatures were checked against the committed `work-tracker/allowed_signers`. The Owner's
  checkout, `shoalmark-gtm`, every other worktree and every folder of session `8b91dba2` stayed outside every command.
- **Tier:** docs, one pass. `git diff --name-only b15c6d9 HEAD` names 6 paths, all under `work-tracker/`: FM-002,
  FM-038, FM-039, INDEX.md, TRIAGE.md and the new worksheet. No `shoalmark.py`, suite, hook, workflow, key or signers
  file is among them. A P3 is fixed forward; a P2 sends the branch back.
- **Independence:** same session. Both commits are the Principal's (`Session: 8e509911`), and this seat is its
  sub-agent. Reported as such, not independent.

**Reviewed:** `tracker/triage-2026-09-27-the-release-shipped` at `ea85f4d57acb5f0854adf0f837e540656c38fcaf`.
- `git ls-remote` at the start gave `ea85f4d…` for the branch, and `b15c6d9…` for both `main` and the tag `v0.18.5`
  (a lightweight tag).
- The branch is `b15c6d9` plus two commits:
  - `d15616d` (12:15:49): `--clear-ask FM-002 build`.
  - `ea85f4d` (12:17:43): the worksheet `triage-2026-09-27.md`, three rows applied, FM-002 set Shipped by hand with
    one ship-log row, and TRIAGE.md's Passes paragraph.

## The checks

| # | Check | How | Result |
|---|---|---|---|
| 1 | `--clear-ask` reproduced | A scratch clone at `b15c6d9` ran `python3 shoalmark.py --clear-ask FM-002 build`, then its FM-002 was diffed against `d15616d`'s | Byte-identical. The ask's eight keys leave the front matter, and `## Asks` carries the question, the answer, *chose option 2* and *signed — 4e00f85 · G*. `4e00f85` verifies G against the committed signers file ✓ |
| 2 | The worksheet reproduces every front-matter change | In the same clone, after the clear-ask, I placed the tip's worksheet and ran `--triage` | *Applied 3*. The tool writes FM-038 (`triaged`, `next: build`, `tier: P3`), FM-039 (`triaged`, `rank: 7`, `next: build`, `tier: P2`) and FM-002 (`triaged: 2026-09-27`, `rank: 4` removed), each byte-identical to the tip's file. The worksheet is byte-identical too. The tip differs from the tool's output only in FM-002's `status: Shipped` and its ship-log row, which the `fix` row says are made by hand. With the tip's FM-002 in place, `--print-written` writes an INDEX.md byte-identical to the tip's ✓ |
| 3 | `--triage` on the tip | A scratch clone at `ea85f4d` | *0 trackers to judge*. The worktree is clean afterwards, and the worksheet's rewrite is byte-identical ✓ |
| 4 | TRIAGE.md | `git diff b15c6d9 HEAD`; `--check` | One hunk adds two lines under *Passes*, the paragraph and a blank line; every other line is main's. `--check` reports *the Owner's two sections: guarded — none changes them or his signers file* ✓ |
| 5 | The ship-log row against the forge | `gh pr view 94–97`; the verdict commits; the tag's workflow runs | PR 94 merged 10:02:06Z (head `b9644b7`), PR 95 10:02:39Z (head `dd88edc`), PR 96 10:03:40Z (head `9704145`) and PR 97 10:05:25Z (merge `b15c6d9`, head `dac80bf`), all merged by holgo99. `b9644b7e` is slice A's READY WITH FINDINGS. `9704145` is slice B's READY on `a2850fb`, which holds slice A at `b9644b7e` (`d111ab1`). `6bef2cb` is the cut's same-session READY. `27072ef7` is the cold session `01a0e147`'s READY WITH FINDINGS, at 11:12:42+02:00 = 09:12:42 UTC and on PR 97's head. The tag: see R1 ✓ with R1 |
| 6 | The Passes paragraph | the two trackers; PR 95; the tag's tree | FM-006 and FM-031 are byte-identical to main, so neither was re-judged. FM-006 is still P2 #6 `owner`, and its ask is uncleared. FM-031's glob line is still open. PR 95 merged `dd88edc`; `overrides/landing.html` and `docs/index.md`'s `template:` are in `b15c6d9`. The tag's `docs` and `ci` runs succeeded ✓ with R1 |
| 7 | FM-002's Done-when at v0.18.5 | The Done-when read line by line against `git archive b15c6d9`; the board built there (`--html-only`) and read in Chrome by my own script at 1440 and 390 px, light and dark; `--brand DIR --from` run from the tag | **Slice A.** The board and site wear `shoalmark` from `work-tracker/brand/theme.css` and `docs/stylesheets/shoalmark.css` (`extra_css`). The header `#H` sits at (283, 48), 874 × 18, inline inside the chart's graduated border, in both schemes (rendered and seen). Contrast: 132 visible text runs at 1440 px and 119 at 390 px, each measured against the median ground under its glyphs. **None is below 4.5:1**; the lowest is 5.91 by day and 5.98 by night. My script does not measure pseudo-elements or placeholders; the same-session pass on `0612dfe` measured them at 5.76 and 5.98, on a tree whose tool, brand and stylesheets equal the tag's. Slice A had one Reviewer pass (`b9644b7e`). The site built at the tag (`docs` success); it goes live at the go-public act. **Slice B.** `brand/themes/` holds `monochrome` and `shoalmark`. `--brand DIR --from shoalmark` writes all five files byte for byte. `--from catkin` exits 2, names the two themes and writes nothing. The suite names `--from` 18 times. The 0.18.5 CHANGELOG names the themes and what a vendoring repository receives. Whether a consumer that chooses nothing looks the same rests on the cold pass: 48 pixels differ, only the running line's digit, on `6bef2cb`, whose tool paths equal the tag's. Both slices were judged before their first build commit (`13d70189`). **Met** ✓ with R3 |
| 8 | The rows' own facts | `git log --diff-filter=A`; the history of `rank: 7`; FM-038's filing review | FM-038: filed at `5558b1a` on 2026-09-26, merged by PR 92; *its six P3s (R1–R6)* are its filing review's ✓. FM-039: see R2 |
| 9 | Gates at the tip | `--check`; `--session-check`; both suites once per interpreter, one interpreter at a time, each started at load under 6; `git merge-tree --write-tree origin/main HEAD` | Suites **481 + 148**, green on 3.14.3 (12:31–12:40, load 2.2–4.0) and on 3.9.6 (12:40–12:48, load 4.0–2.7), 0 skipped; FM-035's healthy-board case passed on both at the first run. `--check` exit 0 (*INDEX.md is up to date — 39 trackers*; judgement on). `--session-check` exit 0. The merge-tree is clean, and its tree `59bf6b3` is the tip's own. **The tool is byte-identical to the tag:** `git diff b15c6d9 ea85f4d` touches nothing outside `work-tracker/` ✓ |

## Findings

**R1 · P3 · confidence 90 % on the facts, 55 % on the grade · *Tagged 12:05:24* is the tagged commit's time, not the
tag's.**
- *The gap:* `v0.18.5` is a lightweight tag and records no time of its own.
  - 12:05:24 is `b15c6d9`'s commit time: GitHub's merge of PR 97, whose `mergedAt` is 12:05:25.
  - The tag reached the forge by 12:10:16. The `ci` and `docs` runs for *push v0.18.5* were created at 10:10:16Z.
  - The Passes paragraph's *seven minutes after v0.18.5 was tagged* fits 12:10: the pass's commit is 12:17:43, twelve
    minutes after 12:05:24.
  - The time stands in four places: FM-002's ship-log row, the Passes paragraph, the worksheet's `fix` Reason and both
    commit bodies.
- *Why it matters:* the record dates the release. The tag reached the forge about five minutes after the merge.
- *Why only P3:* v0.18.4's record dated its tag the same way (09:58:57, `a7e5291`'s time), and no one relies on the
  minute.
- *What closes it:* write *PR 97 merged at 12:05:25 (`b15c6d9`), tagged by 12:10:16 (the tag's runs)*, or name
  12:05:24 as the commit's time.

**R2 · P3 · confidence 95 % on the facts, 70 % on the grade · FM-039's Reason misdates its filing and names the wrong
tracker for rank #7.**
- *The gap:*
  - The Reason says *NEW FILING of 2026-09-27 (in the 0.18.5 cut, 84bc65d)*. But `84bc65d` is from 2026-09-26
    22:10:37, and the row's own *Last worked on* and FM-039's body both say 2026-09-26.
  - The Reason says *the rank free since FM-034 shipped*. But #7 was FM-035's: `8f98103` removed its `rank: 7`, and
    that pass's paragraph says *FM-035's #7 freed*. FM-034 held no rank there.
- *Why it matters:* the worksheet is the pass's record, and a reader checks the rank's history against it.
- *What closes it:* *of 2026-09-26* and *since FM-035 shipped*, in the Reason cell. Nothing the tool applies changes.

**R3 · P3 · confidence 95 % on the facts, 70 % on the grade · FM-002 is Shipped, but its *What is true now* still says
its slices are not merged.**
- *The gap:*
  - Two lines of FM-002's *What is true now* still read *Slice A built — … not merged* and *Slice B built — … not
    merged*.
  - Its status and its new ship-log row say Shipped at v0.18.5.
  - The same holds for FM-006's slice L line, *on `fm/006-the-landing-page`, not merged*. The Passes paragraph says
    that line is met by PR 95, but FM-006 is untouched here.
- *Why it matters:* a reader of *What is true now* takes both slices as unmerged, the opposite of the status line. The
  judging pass graded the same kind of gap P3 (its R2).
- *What closes it:* rewrite FM-002's two lines in place (merged PR 94 and PR 96, shipped in v0.18.5), and FM-006's
  slice L line (merged PR 95, in v0.18.5), as tracker-only lines.

## Not findings

- **FM-002 Shipped with `next: build` and `tier: P2`:** the tool leaves them, as it did for FM-034, FM-035 and FM-036
  when they were fixed to Shipped.
- **The `fix` Reason's *his word of 15:59:53* for the mocks as-is:** this time is new to the record, which elsewhere
  dates the relay of that word 16:0x (`cd1c33f`, FM-006). A word and its relay can differ by minutes. A word file, like
  FM-002's three, would source it.

## Verdict

**READY WITH FINDINGS**: R1–R3, all P3, fixed forward; no P2.

- `--triage` reproduces every front-matter change from the worksheet and applies nothing on the tip. `d15616d` is the
  tool's own output. The only hand edits are FM-002's status, its ship-log row and the Passes paragraph, and each is
  what the `fix` row says.
- The Owner's two sections are unchanged.
- The ship log's PRs and verdicts are the forge's.
- FM-002's Done-when is met at v0.18.5, measured on the tag's tree.
- The tool is the tag's.

*The Owner lands this by merging; a merge rules nothing.*
