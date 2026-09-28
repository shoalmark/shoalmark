Reviewed: 3bb53ec6d7fc7f48087bf4c8fb239cb92416957a
Tier: critical under TRIAGE.md path line 3 — the queue's reader interprets the Owner's own acts.
Independence: cold — a session the Owner started, no part of session 8e509911.

# FM-031 — cold review of 3bb53ec

The production change is one expression in `answered_at`: the `git log -G` pattern widens from `^answer:` to
`^(answer|done|due):`. The documented RV-679 cases work: a signed Owner `done:` or `due:` commit followed only by the
Reviewer's evidence commit is selected instead of the Reviewer head. A non-review commit above the act still makes
`addenda_only` false and leaves the head to be read.

## Runs

Each suite started only after `uptime` showed a 1-minute load below 6 and
`pgrep -fl '[Pp]ython[0-9.]* [^ ]*test_(shoalmark|core)\.py'` printed nothing. They ran one at a time.

| Run | Time (CEST) | Result |
|---|---|---|
| Python 3.14.3 `test_shoalmark.py` | 14:32:19–14:45:23 (784 s) | 510 ok, 0 failed; skipped here: 0 checks; all green |
| Python 3.14.3 `test_core.py` | 14:45:33–14:45:36 (3 s) | 148 ok, 0 failed; all green |
| Python 3.9.6 `/usr/bin/python3 test_shoalmark.py` | 14:45:44–14:55:20 (576 s) | 510 ok, 0 failed; skipped here: 0 checks; all green |
| Python 3.9.6 `/usr/bin/python3 test_core.py` | 14:55:32–14:55:35 (3 s) | 148 ok, 0 failed; all green |

- `python3 shoalmark.py --check`: exit 0, 14:56:34–14:56:55, after this fresh clone was configured to use the committed
  `work-tracker/allowed_signers`. The first run correctly exited 4 because a fresh clone had no allowed-signers setting;
  it reported four historical signed commits as unverifiable here, not a ledger defect.
- `python3 shoalmark.py --session-check`: exit 0, 14:56:13.
- `python3 shoalmark.py --queue`: exit 0, 14:56:13–14:56:22. Its line for this branch was:
  `branch fm/031-the-queue-reads-his-newe… @ 3bb53ec  wait: no pull request — conflict in CHANGELOG.md`.

## Findings

### RV-710 · P1 · confidence high (99%) — the widening newly says merge for a PR that contains a seat's commit

`answered_at` checks only the commits *after* the selected act commit. It does not check the pull request's own commits
between its base and that act. `owner_change` cuts `answer/<id>` from the branch on which the Owner runs the command, so a
real branch can have this shape:

1. a seat's non-review commit;
2. the Owner's signed `done:` or `due:` commit;
3. a Reviewer's review-file-only commit.

At this tip, the widened `-G` selects commit 2; `addenda_only(2, 3, None)` passes; `answer_reading(2)` returns
`merge: your answer`. That instruction applies to the whole pull request and therefore admits commit 1 as though the PR
were only the Owner's act. At the parent implementation, no `answer:` match exists, so the Reviewer head is read and the
same branch waits as `not an answerer`. This is introduced behavior for both newly recognized keys, even though the
analogous `answer:` defect predates this branch.

This is the critical boundary named for the review: a commit not his is carried by a pull request the queue calls
`merge: your answer`. It is P1 under the supplied rule and contradicts path line 5's separation of an answer from other
acts. The three RV-679 checks cover only the Owner act plus review, its `due:` twin, and a seat commit *above* the Owner
act; none covers a seat commit below it.

Fix before merge: require every own commit below the selected Owner act to be his or an allowed review addendum (or cut
and validate the act branch from the default branch), and pin the seat-commit / Owner-act / review shape for both `done:`
and `due:`. A safe implementation must keep RV-679's two intended cases green while making this shape wait and naming the
non-owner commit.

## Verdict

**NOT READY.** RV-679's intended cases pass and all four suites are green, but RV-710 is a newly widened false-merge path
in the Owner's queue reader. The earlier local pass's RV-735 mechanism is correct; its classification as P3 and “not
introduced here” is not: row 8 changes from wait to merge specifically because this commit adds `done:`/`due:` to the
selector.

Path 5 — a merge rules nothing.
