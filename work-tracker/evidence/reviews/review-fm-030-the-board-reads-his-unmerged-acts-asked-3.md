# Review — FM-030's ask on the board, third pass at 6daf7e6 (2026-09-27 14:48 CEST, Reviewer, session `8e509911/reviewer-39`)

- **Branch:** `fm/030-the-board-reads-his-unmerged-acts-asked`, tip `6daf7e6` (`6daf7e687c8ccbdfb96838c1c81949a4348c4f97`,
  confirmed by `git ls-remote`). It is one Principal commit (`principal@seat`, `Session: 8e509911`,
  `Worktree: shoalmark-principal-4`) on my second verdict `09ba433`. It was authored and committed 14:44:09; the brief's
  14:44:27 is most likely the push. It answers the second pass's N1–N3.
- **Tier: docs, one pass.** The commit touches three paths under `work-tracker/`: FM-030, TRIAGE.md (*Passes*) and the
  day's worksheet. No `.py` has changed since `28e54bf`, so no suite was run.
- **Independence:** same session (`8e509911`), reported.
- **Verdict: READY WITH FINDINGS.** N1–N3 are fixed. One new P3 (N4) is a consequence of N2's cure. One P3 is noted for
  the build branch.

## What I ran

| run | result |
|---|---|
| `git diff --word-diff 09ba433..HEAD` | the worksheet's FM-030 Reason and the TRIAGE.md paragraph reworded; the 14:09:46 bullet's `· undermines: path 6` dropped; the ship-log row moved from the table's top to its end, its text unchanged. FM-030's front matter is unchanged: `triaged: 2026-09-27`, `rank: 2`, `tier: P1`, `next: owner` |
| `raise_lines`, the tool's parser, on FM-030 | 13:57:50 → `['path 6']`; 14:09:46 → `[]`. One raise on a signed rule, dated 13:57:50 |
| scratch clone at `6daf7e6`, `--triage` | *0 trackers to judge*, *Applied nothing*, the tree unchanged |
| replay: FM-030's `triaged:` set back to 09-25 and `dd9a19e`'s worksheet, `--triage` | *1 trackers to judge*: FM-030 *2026-09-27 · keep · RAISED*, with the 13:57:50 bullet as its Now |
| the replay with `6daf7e6`'s worksheet restored, `--triage` | *Applied 1: FM-030: keep P1 #2 owner*. The tree then equals `6daf7e6`. The re-judge stands on the one raise |
| `python3 shoalmark.py --check` | exit 0. *INDEX.md is up to date — 39 trackers*. *the Owner's two sections: guarded — 5 commit(s) … none changes them or his signers file* |
| `git diff -U0 09ba433..HEAD -- work-tracker/TRIAGE.md` | one hunk at line 29, under `## Passes`. *The intent* and *The current path* are untouched |
| `python3 shoalmark.py --session-check` | exit 0 |
| `--owner` | *1 NEED THE OWNER*: FM-030, the ask word for word |
| `git merge-tree --write-tree origin/main HEAD` (`62b4a05`) | clean (`993d398`). The merge made in the scratch clone passes `--check` 0, and INDEX stays up to date |
| `git merge-tree 5e6d816 HEAD` | the same conflict in FM-030's `## Raised`, left to the merger (R2) |

## The second pass's findings

- **N1 ✓.** The Reason names the one raise this branch carries: *13:57:50 names path 6 — the board rebuilt from main
  shows an act he just gave (his \`--done FM-024\`, f8246fae, 13:44:51) as still open*. It records his 14:09:46 word
  *beside it, not as a raise*. It places the *done* dialog's raise (13:38:30, screenshot 13:35:40) on the build branch.
  The TRIAGE.md paragraph says the same. All the times agree with the transcript and git (second pass).
- **N2 ✓.** The 14:09:46 bullet no longer carries the mark. The tool lists one raise (13:57:50), and the verdict still
  applies, reproduced above.
- **N3 ✓.** The ship-log row is the last row of the table, after 2026-09-26.

## Findings

**N4 — P3 · the moved ship-log row still says *the two raises name path 6*.** After N2 one raise does (13:57:50). The
second pass said this clause could stay. That was true when I wrote it, but I did not say that N2's cure would make it
false. *Cure:* *the raise of 13:57:50 names path 6, so FM-030 was re-judged the same day*.

**For the build branch — P3, outside this review.** `5e6d816` dates its *done*-dialog bullet `2026-09-27 13:35:40 ·
the Owner, in chat`. 13:35:40 is the screenshot. His chat message is 13:38:30 (the transcript, 11:38:30Z). After both
branches merge, the Passes paragraph (13:38:30) and that bullet (13:35:40) will disagree. The same bullet's `undermines
line 6 (…)` is still not in the form the tool parses. Both fixes are the build branch's.

## Not checked

- `--queue`, which needs `gh`.
- The suites: no `.py` changed.

The Owner lands this by merging. A merge rules nothing: his signed answer through the board rules the ask.
