# Review — the --day addendum, at 3ce50e4 (2026-09-25 16:08 CEST, Reviewer, session `8e509911/reviewer-11`)

- **Branch:** `fm/028-the-day-reaches-the-index-too`, tip `3ce50e4` (`3ce50e4f7835563985129639adddf6a4c73f4b4b`). It has
  two commits on `origin/main` `e163ec2` (PR 75's merge, 15:51:47), both by the principal seat (`Session: 8e509911`,
  `Worktree: shoalmark-principal-3`):
  - `99f0ec0` 15:54:03: the addendum row, plus the earlier R1/R2 fixes;
  - `3ce50e4` 16:02:29: the addendum's credit corrected on the Owner's word before the merge.
- **Tier: docs, one pass.** `git diff --name-only origin/main...HEAD` names FM-028 and FM-029, ship-log rows only.
- **Independence:** this seat is a sub-agent of the branch's own session (`8e509911`). `--check` counts it as *same
  session*. Reported.
- **A verdict written for `99f0ec0` was not pushed.** Origin had moved to `3ce50e4`, and the push was refused as not a
  fast-forward. This file is written on the head.

## What I ran

| run | result |
|---|---|
| the Principal's transcript, searched for *FM-028 --day* | the user record (`origin: human`) at `2026-09-25T13:52:59.761Z` = 15:52:59 CEST ✓ |
| its content against FM-028's new row | byte-identical to the italic quotation, 170 bytes; nothing in the record precedes or follows it ✓ |
| **the credit line**, against the Owner's correction | the user record at `14:01:42.692Z` (16:01:42 CEST): *the new FM-028 row credits the Auditor's relay line to the Owner … He pasted it; the Auditor wrote it. Fix the row before merge …: "The Auditor seat's addendum, through the Owner at 15:52:59"*. The row now opens with exactly those words, then *(as pasted):* in place of *(spelling as given)* ✓. It matches the row above, which credits *the Auditor seat's item 2 through the Owner (15:34:27)* ✓ |
| `shoalmark.py` on `origin/main`, lines 5043, 5077 and 5089 | 5043 is `today = datetime.date.today().isoformat()` in `--triage`. 5077 is the same call in the generator. 5089 is `> Generated {today} · …` in INDEX's header ✓ |
| the seat's reading after the quotation | `drift_normalize` (:4273) blanks the Generated date, so *the same tree only under `drift_normalize`* holds ✓. It is the seat's reading, and it follows *— so* unmarked (not graded) |
| 15:34:27 in both rows | the Auditor's item 2, through the Owner, is the user record at 13:34:27.395Z (see the review of `d5507a0`) ✓ |
| FM-029's placement note | *the item named FM-028 for both lines — the seat put this one here, the relation's own tracker* ✓ (the earlier R2) |
| placement and order | FM-028's addendum is appended last in its oldest-first log ✓. The two rows fixed for the earlier R1/R2 are edited in place (R1 below). `3ce50e4` edits the addendum row in place too, but that row is not yet merged: the evening R10's reading, and not graded |
| `--check` · `--session-check` | exit 0 (*87 verdict(s)*; *filing freeze: 20 open*) · exit 0 |
| `python3 shoalmark.py` | the tree is clean after it |
| `git merge-tree --write-tree origin/main HEAD` | clean (tree `4b55563`) |
| `test_shoalmark.py` · `test_core.py` | exit 0, 394 ok · exit 0, 148 ok |
| origin's refs, for the note | `git ls-remote origin`: of the `fm/028` names, only `refs/heads/fm/028-the-day-reaches-the-index-too` exists (now `3ce50e4`). `fm/028-a-pass-replayed-on-a-later-day` is gone. `refs/pull/75/head` is `049554c`, PR 75's merged head. No PR 76 exists (`gh pr list`) |

**Note, for the record and not graded:** no trace of the briefly recreated `fm/028-a-pass-replayed-on-a-later-day`
remains on origin — no branch, and no pull request, and PR 75's head is untouched. GitHub's own event log was not read.

## Findings

**R1 · P3 · confidence high · Two ship-log rows already on `main` are rewritten in place.**
- FM-028's row of the Auditor's item 2 (*15:3x — …* → *15:34:27*) and FM-029's row (the time and the placement note
  added) both merged with PR 75 at 15:51:47. `99f0ec0` edits them where they stand.
- AGENTS.md rule 1: *only the ship log is append-only*. The evening's R10 graded in-place edits of *unmerged* rows P3;
  these rows were merged.
- The edit was invited: my R1 and R2 on `d5507a0` said *15:34:27 in both rows* and *placed here by the Principal seat*,
  words that read as an edit in place.
- No meaning changes: a time is made exact, and a placement is stated. Git keeps both versions.
- **Fix:** none to this text. A merged row is corrected by a correcting row, and this seat will word such fixes that way.

## Verdict

**READY WITH FINDINGS (R1 P3).**
- The addendum is quoted byte for byte at its true time of 15:52:59, and credited as the Owner's correction asks: the
  Auditor seat's, through the Owner.
- Lines 5043, 5077 and 5089 say what the row says.
- The earlier R1 and R2 are closed in substance.
- The gates, the generator and both suites are green, and merge-tree against `origin/main` is clean.
- R1 is fixed forward under the docs tier.

The Owner lands this by merging; a merge rules nothing.
