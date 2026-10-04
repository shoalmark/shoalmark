# FM-006 — the board's refresh: the critical verdict at 6e2d689, the cold review's F1

Verdict: **READY**. No finding is open. RV-2321 onward are unused.
Reviewed: 6e2d689c950a763c73d79ffdebead54fb8d6794f. The round is `df4f266..6e2d689`, at critical tier, judged against FM-006's *The cold review's F1* (P2, fixed before the tag) as the Owner amended it.
Reviewer: b3bdb000/reviewer-80 (claude-opus-5-5, xhigh), at the reviewer's bot address, unsigned, in worktree shoalmark-review-11, on 2026-10-02.
Independence: this is the builds' session (b3bdb000), so not independent. Each head was read from the shared repository.
Everything before this round is in `review-board-refresh-26bcd97-critical.md` and `review-security-ledger-593ebe1.md`.

This change answers a private security report.

## The round

| Commit | What | Judged |
|---|---|---|
| `2183924` | the Planner's filing of F1 | — |
| `85bf269` | refactor: `tracked_board_rels` names the board's tracked files as git names them | the same files, from the same one read-only call |
| `d1661e3` | the fix, with its test and control; the tool was wrong | below |
| `7f8d163` | notes: `CHANGELOG.md:44` | the tool is judged against the line as amended |
| `6e2d689` | `--check` no longer refuses a board file git tracks; that check goes; row 132 is the board check's control alone | `--check` is as it was at `df4f266`, with nothing of the refusal left |

**The red run:** CI run https://github.com/shoalmark/shoalmark/actions/runs/37029025288 on `7f8d163` was red on all five jobs. Each job stopped after the FM-012 `--answer` check, where an in-process `--check` in a test repository that commits its board met the refusal's exit. With the refusal gone, that block passes at `6e2d689`.

## What the build covers, as checked

Each case was checked by hand with inert content, both by a run of `--html-only` by hand and by the hook's run of the copy after a checkout:

- **A view git tracks, the page not tracked:**
  - The board's run writes a page that loads nothing: no script, style or image, and a policy that allows none.
  - The page names the tracked file, and the run prints that one line in place of the link, exit 0.
  - The tracked view stays as committed.
- **The page git tracks, alone or with a view:** the page is left as committed, with its one line and no link. The board's run writes over no file git tracks.
- **Outside the board's run:** the write rule writes over a board file git tracks, so a commit hook's run puts back the tool's own page and views.
- **CHANGELOG.md:44, as amended:** a page the board's run writes loads no board file git tracks, and a `blob` that is not an http(s) URL makes no forge link, with one line.
- **The rest of the board's run is unchanged,** with one more read-only `git ls-files` call, its paths compared as git prints them.

## Tests and runs

- **Row 130,** the board check: passes at the head. Run alone beside df4f266, its block stops with an AttributeError: that tool has no `tracked_board_line`, which the check uses to name its line.
- **Row 132,** the in-suite control, in its ruled form: beside df4f266's tool the board check FAILS. That tool printed the link.
- **Rows 5 and 14, case 6b and the FM-012 block:** unchanged, and green at the head.
- **`python3 -u test_core.py`** at 6e2d689: 158 ok, all green.
- **The Builder's full run** at 6e2d689: 863 ok, 0 failed, 3 skipped (FM-032's browser block). That is 26bcd97's 861 and the two F1 rows.
- **The Owner's CI run on this head:** https://github.com/shoalmark/shoalmark/actions/runs/37033610114 (workflow_dispatch), green on all five jobs. ubuntu 3.9 and 3.12 and macOS 3.12: 1021 ok, 0 FAIL, 3 skipped in 1 block; windows 3.9 and 3.12: 1012 ok, 0 FAIL, 10 skipped in 6 blocks. Every job ends "all green".
- **Disclosure:**
  - The commit messages say whether the tool was wrong, cite the ruling and say what is asserted.
  - The behaviour d1661e3 names was never in a release.
  - There are no attack steps, and the cold review's report is not quoted.

Quality read: the fix leaves one place to decide what a tracked board file means. The test uses inert content, and its control fails beside the older tool. Clean.
Next: the ledger's new rows from this run, then the Auditor's final-head checks.
