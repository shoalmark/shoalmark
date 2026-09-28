# Scoped re-check — FM-018: the merge of main `fa9e9ac` (PR 113) into my READY `ca677af`, at 4cc8083 (2026-09-28 15:22 CEST, Reviewer, session `8e509911/reviewer-48`)

Reviewed: 4cc8083f116c41fda8c5456e6d0f139be35224c0
Session: 8e509911/reviewer-48

- **Scope.** `4cc8083` is the Principal's merge commit (14:57:29).
  - Its parents are `ca677af`, my re-check on `2ec5e1b`, and `fa9e9ac`, main after PR 113, the board build.
  - My fetch at 15:20:18 showed the branch at that sha and main at `fa9e9ac`. HEAD in `shoalmark-review-2` was the same,
    and the tree was clean.
- **Tier: docs — a scoped re-check of a merge.** Compared with main, the merge changes no `.py` file, nothing in `vendor/` or
  `docs/`, so no suite was run by me. The Principal reports that the hook ran both suites on both Pythons for the merge,
  14:57–15:17, all green. I cannot see that run. A red suite would have stopped the commit, since the hook's `tests` step
  exits 1.
- **Independence:** same session. I am a sub-agent of 8e509911.
- **Verdict: READY.** Nothing new. The two notes stay as notes, and no id was minted.

## Checks

| check | what I ran | result |
|---|---|---|
| (1) The merge against main equals the branch's own change | `git diff --stat fa9e9ac 4cc8083` against `git diff --stat 9e9fcb3 ca677af`, then, file by file, the `-U0` added and removed lines of each | The same 5 files: FM-018 (17 lines), FM-030 (4), FM-040 (8), and the two review files (123 and 83). The same +234/−1. Every file's added and removed lines are identical. No other path differs from main, so the tool, the suites, `docs/`, `vendor/` and INDEX.md are main's byte for byte. FM-018 and FM-040 are `ca677af`'s blobs |
| (2) FM-030's ship log | The table rows (`^\| 20…`) of the base `9e9fcb3`, of main, of the branch and of the merge, compared with `cmp` | The base has 17 rows. Main is the base plus 2 rows, and the branch is the base plus 2 rows. The merge's 21 rows equal main's 19 followed by the branch's 2, byte for byte, with no duplicates and no conflict marker in the file. That is oldest to newest, as the table runs: the board build and the pass on `ada15c6`, then the 12:43:02 raise and RV-758 |
| (3) `--check` | In the worktree, 15:20:59–15:21:31, load 1.45 | Exit 0. *INDEX.md is up to date — 41 trackers*; *filing freeze: 22 open, at or above 8 — only bug filings*; judged before build and the Owner's two sections are both guarded |
| `--session-check` | Same place, 15:21:32 | Exit 0, no output. The tree was clean afterwards |
| Merge onto main | `git merge-tree --write-tree origin/main HEAD` after the fetch (main `fa9e9ac`) | Clean. Tree `0b86883` is HEAD's own, and main is an ancestor, so the merge is a fast-forward onto `fa9e9ac`. `git diff --check` is clean |
| `--queue` | The scratch copy at `4cc8083`, 15:21:42–15:21:53, load 1.87 | *branch fm/018-his-two-dashboard-requir… @ 4cc8083  wait: no pull request — no verdict on 4cc8083*. The FM-030 conflict of 13:35 is gone |
| The commit | `git log -1` | Two parents, as above. `Session: 8e509911` and `Worktree: shoalmark-review-2`. The body names the one conflict and how it was resolved |

## (4) The two notes of my re-check on `2ec5e1b` — kept as notes, no id

- **FM-018's *Asked* row.** Its heading reads *lift for one pass: `freeze_at` 24*, but further on the row still says *lift for
  them, fold here, or hold*.
  - The row is the ship log's summary of the ask. What the Owner answers is the `ask:` and `ask-options:` fields, which carry
    the corrected option and its reach.
  - So it misleads no one about what he rules. It is a wording tidy for any later commit.
- **Why 24 — the *22 open*.** The count now lives only in the raise line. The options are capped at 120 characters, and
  `--check` prints the count every run. The split is fair.
- I have no ids left in RV-755…759, and neither note needs one.

## Verdict

**READY.** The merge carries the branch's reviewed change unchanged onto `fa9e9ac`, and it keeps every ship-log row of both
parents once, in order. It merges as a fast-forward, and the gates are green.

path 5 — a merge rules nothing.
