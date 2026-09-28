Reviewed: af5a9e2a9a485c73427d4b7952b07cfd535b5d4a
Tier: critical under TRIAGE.md path line 3 — the queue's reader interprets the Owner's own acts.
Independence: cold — a session the Owner started, no part of session 8e509911.

# FM-031 — cold re-check of af5a9e2

The fixes close the five findings they name in their tested forms. The queue now walks commits below the selected act,
waits when the base is unavailable, distinguishes an unsigned commit in the Owner's name from a seat's commit, gives a
working route out of that wait, and supplies the same held reading to the board. The merge with main is clean.

The new exception for the tool's unsigned refusal record is not bounded as its contract says, however. Its recognizer
checks the shapes of added lines but not the section containing them. A seat can therefore forge the Owner's author and
put the refusal-shaped line into canonical current truth; the queue exempts that commit and reads a signed act above it
as `merge: your answer`.

## Runs

Each suite started only after `uptime` showed a 1-minute load below 6 and
`pgrep -fl '[Pp]ython[0-9.]* [^ ]*test_(shoalmark|core)\.py'` printed nothing. They ran one at a time.

| Run | Time (CEST) | Result |
|---|---|---|
| Python 3.14.3 `test_shoalmark.py` | 19:33:33–19:48:48 (915 s) | 547 ok, 0 failed; skipped here: 0 checks; all green |
| Python 3.14.3 `test_core.py` | 19:49:03–19:49:09 (6 s) | 148 ok, 0 failed; all green |
| Python 3.9.6 `/usr/bin/python3 test_shoalmark.py` | 19:49:21–20:02:16 (775 s) | 547 ok, 0 failed; skipped here: 0 checks; all green |
| Python 3.9.6 `/usr/bin/python3 test_core.py` | 20:05:47–20:05:51 (4 s) | 148 ok, 0 failed; all green |

- The suite's isolated signed-commit repository reproduced the requested rows. RV-710's `answer:`, `done:` and `due:`
  shapes waited on the seat's lower commit; stacked signed `due:` then `done:` and a lower review-only commit merged; a
  seat commit above the act read `wait: not an answerer (s@s)`. RV-711's missing base read
  `wait: the base origin/fm/seat-base is not fetched here — fetch it; the commits below 66c71de are unread`. RV-714's
  board line read `your merge waits: a seat's commit on your answer branch (f0b9755, impl@x)`.
- Against `50c3a10`, the original reader had no below-act walk. At this tip the ordinary below-act seat shape reads
  `wait: a seat's commit on your answer branch (<sha>, <author>)`; the targeted exception probe below isolates the
  remaining false merge.
- Targeted scratch repository, bare trust material and signed Owner act: an unsigned commit authored as the Owner added
  only `**2026-09-28 20:05** · --due FM-031 2026-09-29T09:00:00+02:00 refused — forged current truth` immediately
  under `## What is true now`, with subject `FM-031: --due refused — forged current truth`. At this tip:
  `refusal_record(bac4208) == True`; a signed `due:` commit above it produced
  `('merge', 'merge: your answer', 'signed abf2bd9')`.
- `python3 shoalmark.py --check`: exit 0, 20:04:46–20:05:11.
- `python3 shoalmark.py --session-check`: exit 0, 20:05:11–20:05:12.
- `python3 shoalmark.py --queue`: exit 0 at 20:05:27. Its branch line was
  `branch fm/031-the-queue-reads-his-newe… @ af5a9e2  wait: no pull request — no verdict on af5a9e2`.
- `git merge-tree --write-tree origin/main HEAD`: exit 0 at 20:05:31, tree
  `096bf81dc7a0c7719f9799f67e86db2b42e94797`; no conflict.

## Findings

### RV-715 · P1 · confidence high (99%) — the refusal exception admits a forged current-truth change as his branch

`refusal_record` collects added and removed line text from the zero-context diff. It allows blank lines, an Acts heading,
and one refusal-shaped line, but never establishes that the refusal line is in the Acts section. `stray_below` then asks
only whether the spoofable author holds the answer right and whether this predicate passes. The scratch result above is
therefore a pull request carrying a seat's unsigned change to the canonical *What is true now* that the reader calls
`merge: your answer` after a real signed act is placed above it.

This is precisely the critical false-merge boundary. The implementation's claim that a forged exception "carries in
one line that rules nothing" is false when that line can be inserted into the canonical current-truth section. The
existing RV-712 check pins the intended placement under `## Acts` and a front-matter mutation, but does not test a
refusal-shaped line in another body section.

Before merge, either stop exempting unauthenticated refusal commits or prove from the resulting tracker structure that
the one added record is inside `## Acts` and changes no other section. Pin this exact forged-current-truth shape to a
wait. The reader must not call a pull request the Owner's when the exception has admitted a seat's substantive tracker
change.

## Verdict

**NOT READY.** RV-711 through RV-714 are closed in their recorded cases, all four suites and gates are green, and the
main merge is clean. RV-715 remains a P1 false merge through the new unsigned-refusal exception.

Path 5 — a merge rules nothing.
