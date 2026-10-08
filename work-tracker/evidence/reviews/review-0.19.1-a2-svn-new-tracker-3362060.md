# FM-006: v0.19.1 A2, Subversion's new tracker and the rights gate, the review at 3362060

Verdict: **READY WITH FINDINGS**: two P3s and two findings recorded privately. Ids RV-2670 to RV-2673; RV-2674 to RV-2689 are unused.
Reviewed: 33620600294e782535576c969a65b7cf4a6284eb. A2 had a full critical pass at 1959bba; this is the scoped critical pass at 3362060, against the Owner's rulings of 2026-10-07. Its scope is round 7, `git diff 6827813 3362060` (4116b21 and 3362060: `shoalmark.py`, `test_shoalmark.py`, `README.md`), and the message-only re-make of the 22 commits d06b5de..3362060. Tier: critical (security: the rights gate on Subversion).

## What holds

- On Subversion the first revision of a tracker's path on its line is read with `svn log --stop-on-copy`. Where that revision merged anything (`svn log -g`), each guarded line older than it is refused in one line that names the way through; the line is neither credited to that revision's author nor followed. Where the revision merged nothing, the line is that revision's author's, so a copy is its copier's. A read that fails, of the root or of a revision's merges, is refused.
- Refused at 3362060, each with exit 4:
  - a close made on a branch by a seat without `close`, merged by the planner;
  - a copy filed together with a merge, recorded or real;
  - a copy made on a branch, merged by the planner or by that seat;
  - a seat's tracker taken out and put back from a branch's copy, whether added or copied;
  - a right holder's own tracker filed on a branch and merged. It passes once its line is set again on trunk in commits of its own.
- Still accepted: an ordinary edit on trunk, a holder's own close on trunk, a holder's own close merged from a branch, a merge that brings no guarded line, and the planner's branch of trunk.
- The three checks the ruling names keep their names and their cases, and they assert the refusal; the line they expect is the merge's refusal. No check is removed.
- `--check` in a branch's working copy makes 6 svn calls for 1 tracker and 84 for 40; at 1959bba it made 6 and 162.
- Both readers read a working tree whose diff git cannot make the same way, as no edit. README's gate section names the checkouts that cannot read origin.
- The re-make: each of the 22 commits has its original's tree, author line and single parent, on one chain from 44bc1dd. Every commit is unsigned, as on `backup/a2-before-message-remake` (278f3ea). Only the messages of d06b5de and 66e1c29 differ, and each only in the Auditor's sentence.

## Findings

- **RV-2670:** recorded privately.
- **RV-2671:** recorded privately.
- **RV-2672 · P3 · class 1:** A2's next change after 0.19.1.
- **RV-2673 · P3 · class 1, records:** the Auditor's list.

## Commands and controls: 2026-10-07, CEST, as `date` printed each

- `py_compile` exit 0; `test_core.py` 158 ok, all green, exit 0 (14:52:56–14:53:09). `--check` exit 0; `--session-check` exit 0 (15:01:48–15:01:57).
- Round 7's 139 blocks (the Subversion, rights and FM-037 blocks, and the README and docs readers): 766 ok, 0 failed (15:00:13–15:31:11). The block at :4232 stops before its check, in both runners alike.
- The ruling's cases, measured by probe at 3362060: each exit 4 (14:35:35–14:42:57). The accepted cases: each exit 0 (14:43:16–14:44:15). With the root or `log -g` unreadable: each exit 4 (15:32:36–15:32:42).
- Controls, run-one-check two at a time (14:59:50–15:30:10):
  - Exit 1 beside 1f73865 and beside 1959bba, and 0 at HEAD: round 7's checks on the corrupt index, on the planner's copy merged by a seat, on the holder's own branch filing, on the tracker put back (added and copied), and on the svn call count.
  - The acceptance after the line is set again: 0 at HEAD and beside 1959bba.
  - The three named checks: 0 at HEAD.

Quality read: the defects are RV-2670 to RV-2673; the rest reads clean.
