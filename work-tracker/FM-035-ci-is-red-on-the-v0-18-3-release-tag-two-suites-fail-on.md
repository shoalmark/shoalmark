---
id: FM-035
status: Proposed
considered: FM-003, FM-028, FM-011, FM-006
tags: bug
triaged: 2026-09-25
rank: 6
next: build
tier: P2
hook: "The tag v0.18.3 ran CI (actions run 36121290371, 2026-09-25 09:57–10:02 UTC): ubuntu 3.9 and 3.12 green; windows 3.9 and 3.12 fail two checks of test_shoalmark.py — the wordmark past the size cap, and RV-479's merged answer branch cut fresh; macos 3.12 dies in a traceback at test_shoalmark.py:1529 in the answer-dialog checks — headless Chrome past 60 s, TimeoutExpired. A red release tag on two of three platforms, found the day the tag was cut."
---

# FM-035 — CI is red on the v0.18.3 release tag: two suites fail on Windows and one traceback on macOS while Ubuntu is green

## What is true now

**Filed 2026-09-25 by the Principal seat on the Owner's word of 12:11:44 (*for v0.18.4 we need to fix CI*), from the run's logs he handed
over (actions run 36121290371, five jobs, 09:57–10:03 UTC); nothing is built.** The tag `v0.18.3` was cut on `57aac8d` at 11:56:39
CEST on the cold Reviewer's READY; the suites were green on this machine (394 and 148) and on ubuntu in CI. They are not green
everywhere the matrix runs:

| job | result | what |
|---|---|---|
| ubuntu-latest, 3.9 and 3.12 | green | both suites |
| windows-latest, 3.9 and 3.12 | **2 FAIL** in `test_shoalmark.py` | *0.18.2 · a wordmark past the size cap is skipped with a warning that names its bytes* — and *RV-479 · a merged `answer/<id>` left from an earlier answer is deleted and cut fresh … `revoke` writes `revoked - <reason>` and moves the answer it replaces into the ship log* (the run printed the deletion line and stopped short of the revoke's record) |
| macos-latest, 3.12 | **traceback**, the suite stops | `test_shoalmark.py`, line 1529, `_, b83 = _rows("AP-080", _pick)` in the answer-dialog checks: `subprocess.TimeoutExpired` — headless Chrome ran past the check's 60 s |

The logs are the Owner's download; the seat keeps a copy for the build. Nothing of 0.18.3's behaviour on this machine or on
ubuntu is in doubt; what is in doubt is the tool on Windows (paths, line endings, a byte count) and one check's 60-second budget for headless Chrome on
macOS in CI — to be read from the logs and the code, not guessed here.

## Why

The Owner's path, line 1, whole: *the daily sitting runs on a tagged release with a signed answer and no failed command in the
sitting* — the sitting's own commands ran green here, so a red CI is not that failed command (the Reviewer's R1); what it is: the
tool's first outside user works on Windows (FM-003), and two of the checks that fail there are the answer flow and the board — the
site says *measured, not promised*. Line 3: a release is a critical change; its CI is what the cold Reviewer could not run
(*unproven: CI*, the Implementer's own line on 0.18.3). P2, next — as the fresh-clone finding FM-034 was judged.

## Done when

- The five jobs of the matrix are green on the commit that becomes `v0.18.4`, and the reason each of the three failures had is
  written in the fixing commit's message; the fix ships in 0.18.4 before FM-030's slice, which waits on its design — the rank orders
  the queue, the release orders its own commits.
- A test that cannot run on a platform says so and skips by name, never fails silently or dies in a traceback.

## Ship log

| Date | Event |
|---|---|
| 2026-09-25 | Filed, from the run's logs the Owner handed over; `--related` held it against FM-003 (the tool's first outside user: Windows, Subversion — the matrix's prior art), FM-028 (the suite and the clock), FM-011 and FM-006 (the brand checks, where one Windows failure sits). Re-made on the Reviewer's R1–R5: path line 1 quoted whole and the tier re-judged P2; the macOS failure is the answer-dialog check's 60 s for headless Chrome, not the brand checks; the times exact. |
