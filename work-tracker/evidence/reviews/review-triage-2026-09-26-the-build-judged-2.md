# Review — the build judged before its first commit, the second pass (2026-09-26, Reviewer, session `8e509911/reviewer-32`)

- **Date:** 2026-09-26, from 15:30 CEST.
- **Seat:** Reviewer (Opus 5.5, highest effort), a sub-agent of Principal session `8e509911`.
- **Session:** `8e509911/reviewer-32`, the same seat as the first pass.
- **Worktree:** `shoalmark-review-5`, detached at the tip. The `--triage` runs and a scratch merge with main were made in
  scratch clones in the session's scratchpad. The Owner's checkout, `shoalmark-gtm`, every other worktree and every
  folder of session `8b91dba2` stayed outside every command. The Principal's three paste files were read and hashed, not
  changed.
- **Tier:** docs, one pass. `git diff --name-only origin/main...HEAD` names 9 paths, all under `work-tracker/`: FM-002,
  FM-006, INDEX.md, TRIAGE.md, the worksheet, this seat's first verdict and three new evidence files under
  `evidence/FM-002/`. No `shoalmark.py`, test, configuration, hook, key or signers file is among them. A P3 is fixed
  forward; a P2 sends it back.
- **Independence:** same session. The two new commits are `8e509911/implementer-40`'s, a sibling sub-agent of the same
  Principal. Reported as such, not independent.

**Reviewed:** `tracker/triage-2026-09-26-the-build-judged` at `2468cf0264112306132a874042109f457f48f37f`.
- `git ls-remote` at the start gave `2468cf0…` for the branch and `2a9f7eb…` for `main`.
- Since this seat's first pass (`13d7018`, on `e2ccd04`: READY WITH FINDINGS, R1–R4 P3,
  `review-triage-2026-09-26-the-build-judged.md`), the Implementer seat made two commits (`Worktree: shoalmark-impl-2`,
  unsigned):
  - `412240e` (15:16:03) closes the first pass's R1–R4 and the same-day pass's R1 and R3, and leaves its R2.
    It makes 18 replacements across FM-002, FM-006, TRIAGE.md and the worksheet.
  - `2468cf0` (15:26:57) files the Owner's three words whole, for the same-day pass's R2, and changes the FM-002 Reason
    cell for R1.
- *The same-day pass* is `review-triage-2026-09-26-the-brand-raised-2.md`, on main.

## The checks

| # | Check | How | Result |
|---|---|---|---|
| 1 | R1: built at a tag, live at the go-public act; the fonts item | the diff `13d7018..2468cf0` of FM-002, FM-006, TRIAGE.md and the worksheet; `docs.yml` | FM-006's first paragraph (`:25`) says both asks are answered. It says the site *is built at a release tag and live only at* the go-public act, because `docs.yml` deploys only when `github.event.repository.private == false`. It makes the Google Fonts item due before publication: the Plex open item of 2026-09-24, plus slice L's mock, which loads Plex Mono and Silkscreen from Google (`landing/index.html:11`). FM-002's two lines, *What is true now* (`:24`) and *Done when* (`:44`), now read *built at the next release tag and live … at the go-public act*. So do the FM-002 Reason cell and the *Passes* paragraph. No *goes live at the next tag* sentence is left in either tracker, the worksheet or TRIAGE.md, outside ship-log rows. No workflow changed. ✓ |
| 2 | R2, the same-day R1 and R3: the trackers after his answers | the same diff; counts over FM-002's body; `git show 3339b79`; the README at `3339b79` | FM-002's opening names the ruling (`4e00f85`, PR 90, option 2, *not the proposal*). It quotes option 2 once in the body, and says slice B is *ruled in*, with the hooks *where the pass placed them*. The 0.8.0 *Done when* is marked *Met, 0.8.0, 2026-09-21*. `3339b79` (2026-09-21 17:21:16, holgo99, on main) turns `status: In Progress` into `Shipped`. Section 9 of that commit's README, *Branding the board*, runs from line 184 to line 204: 21 lines, under the 25. The themes' contrast line reads *in both schemes*, and so do 3 lines of FM-002. FM-006's two passages (`:25`, `:27`) say both asks are answered (`4e00f85`, PR 90; `8defe63`, PR 91). The slices bullet points to FM-002. *v0.18.4 is not tagged* now reads *tagged … at 09:58 (`a7e5291`)*: `a7e5291` is the tag's commit (`git ls-remote --tags`), 09:58:57. ✓ |
| 3 | The same-day R2: the three words filed whole | `tail -n +5` of each file, then `shasum -a 256` and `cmp` against the Principal's paste file | `owner-words-2026-09-26-0741.md` hashes to `34ee13d103b1…` and is byte-identical to `owner-themes-word-paste.md`. `…-0923.md` hashes to `21497e4dbd26…` and is byte-identical to `owner-board-header-word.md`. `…-1025.md` hashes to `416d54ce7808…` and is byte-identical to `owner-go-fm002-and-landing-word.md`. Each head is three lines (time, channel, the body's full sha256) and a blank line 4, and states the same hash. No address, key, token or local path is in the bodies. FM-002's Raised line adds only its closing parenthesis, which names the three paths. Its three quotes are byte-identical to `e2ccd04`'s. ✓ |
| 4 | R3: the FM-006 Reason cell; R1: the FM-002 Reason cell | the worksheet's rows at `e2ccd04` and at the tip, cell by cell | Every cell before *Reason* is identical in all six rows: Tracker, Tier and Verdict (`keep P2 #4 build`, `keep P2 #6 owner`). Only the two new rows' Reason cells changed. FM-006's opens *re-dated, not re-judged … an inherited tier, the next pass's to judge with reasons*. FM-002's ends *built at the next release tag (0.18.5), live at the go-public act*. ✓ |
| 5 | R4: the *Passes* paragraph | the diff; `gh pr view 90/91 --json mergedAt` of the first pass | It now reads *14:24:52 and 14:25:12 by the forge's `mergedAt`*, which matches `12:24:52Z` and `12:25:12Z`. It adds *the landing page is the site's start page: the seat's reading, his to strike* and the built-versus-live sentence. ✓ |
| 6 | `--triage` on the tip | a scratch clone at `2468cf0`, `python3 shoalmark.py --triage` | *0 trackers to judge*, *Applied nothing — no new filled rows*, exit 0. *FM-002: `keep P2 #4 owner` — superseded on this sheet by the later row, `keep P2 #4 build`*. The clone was clean after. ✓ |
| 7 | Front matter; TRIAGE.md's guarded sections | sha256 at `origin/main` (`2a9f7eb`) and the tip; `git diff` | FM-002's front matter is `51507121…` on both, identical. FM-006 differs from main in `triaged:` alone (2026-09-25 → 2026-09-26), and its front matter is still `b0229da8…`, as at `e2ccd04`. TRIAGE.md above `## Passes` is `60579d25…`, the intent `74ff308a…` and the path `a100dbd4…` on both. Against main the file gains the one paragraph and a blank line. ✓ |
| 8 | INDEX.md; `--check`; `--session-check` | in this worktree at the tip | INDEX.md is unchanged since `e2ccd04`, and `--check` says *up to date — 37 trackers*. `--check` exits 0: *judged before build: on — 4 commit(s) … every build commit under a judged In Progress tracker*; *the Owner's two sections: guarded — 4 commit(s) … none changes them or his signers file*. `--session-check` exits 0 and prints nothing. ✓ |
| 9 | Both suites by hand | `python3` (3.14.3) in this worktree; `/usr/bin/python3` (3.9.6) in a scratch clone at the tip | `test_core.py`: 148 ok, *all green*, on both. `test_shoalmark.py`: 462 ok on each, *skipped here: 0 checks — every check ran*, *all green*; 8 min 46 s on 3.14.3 and 7 min 26 s on 3.9.6. Both trees were clean after. ✓ |
| 10 | merge-tree against `origin/main` (`2a9f7eb`, PR 92) | `git merge-tree --write-tree origin/main 2468cf0`; a scratch merge, then `python3 shoalmark.py`, `--check` and `--triage` on it | Clean, exit 0, tree `0bbe73cd…`. INDEX.md auto-merges. On the merge it regenerates to itself (*38 trackers*), and `--check` exits 0 with the signers file set. `--triage` there applies nothing and names the same superseded row. It lists FM-038 as the one tracker to judge, a new filing from main, which is not this branch's. ✓ |

## Findings

None graded. Each of the first pass's R1–R4 and the same-day pass's R1–R3 is closed as the commits claim.

**Noted, not graded.**
- The FM-002 Reason cell still reads *contrast at 4.5:1 on the built files*, without *in both schemes*. The *Done when*
  that the build is tested against now says it, and the first pass's R2 asked for no more. The row can take the words at
  its next touch.
- The two Reason cells were re-worded after they were applied, by the Implementer seat on the Principal's pass, before
  the merge. The Verdict cells are unchanged, so `--triage` re-applies nothing. Printed rule 4 lets a seat re-make a
  row, and `412240e` says so. The board shows the new words, because `latest_verdicts` takes the last row.
- Each filed word carries the Principal's framing and the seat's normalised reading beside his verbatim text. The heads
  and FM-002's Raised line say so, and the hashes cover the files as they stand.
- Carried from the first pass, and not this branch's: `FM-006:31` still calls the TRIAGE.md page *built, in review*.
  `docs/triage.md` is on main.

## Verdict — READY, 90%

**READY.**
- R1: both trackers, the worksheet and TRIAGE.md say the site is built at the tag and live at the go-public act, as
  `docs.yml` has it. The Google Fonts item is due before publication, slice L's mock included.
- R2 and the same-day R1 and R3: FM-002 and FM-006 read as after his answers. The 0.8.0 *Done when* is marked met on
  `3339b79`'s facts, and the contrast line says *in both schemes*.
- The same-day R2: the three words are filed whole, each byte-identical to its paste and hashing to the hash FM-002 cites.
- R3 and R4 are closed in the Reason cell and the *Passes* paragraph.
- No verdict, tier or rank cell moved, and `--triage` applies nothing.
- The front matter and the guarded sections are as the first pass found them.
- `--check` and `--session-check` exit 0, the suites are green by hand, and merge-tree is clean on `2a9f7eb`.

*The Owner lands this by merging, and a merge rules nothing (path 5).*
