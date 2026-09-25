# Review — FM-035 filed and judged the same day, at 42f4eca (2026-09-25 12:28 CEST, Reviewer, session `8e509911/reviewer-6`)

- **Branch:** `fm/035-ci-red-on-the-release-tag`, tip `42f4eca` (`42f4ecad7c8e650675f0ff39d139be2c14c90aa3`), two
  commits on `origin/main` `57aac8d` (`v0.18.3`, PR 65's merge), by the principal seat (`Session: 8e509911`):
  `840dabe` 12:14:40 files FM-035 (`--tags bug`, under the freeze); `42f4eca` 12:15:38 is the same-day pass.
- **Tier: docs, one pass.** Four paths, all under `work-tracker/`: FM-035, INDEX, TRIAGE.md, the worksheet.
- **Independence:** a sub-agent of the branch's own session (`8e509911`); `--check` counts it *same session*. Reported.

## What I ran

- **The logs** (the seat's copy, five job files, `ci-36121290371/`), read against the filing's table:
  - ubuntu 3.9 and 3.12: *all green* twice each, 394 + 148 ok ✓.
  - windows 3.9 and 3.12: `FAILED: 2` in `test_shoalmark.py`, 392 ok, `test_core.py` not reached. The two names match ✓.
    RV-479's `saw` text is step *1/4 reading the trackers* and the line *`answer/ap-080` was left by an earlier answer and
    is merged into `origin/main` — deleted, and cut fresh*, then nothing more: *stopped short of the revoke's record* ✓.
  - macos 3.12: a traceback at `test_shoalmark.py`, line 1529, `_, b83 = _rows("AP-080", _pick)` ✓. Where it is and what it
    raised: R2.
  - Times: the jobs' logs open at 09:57:09 and the last one, windows 3.9, exits at 10:03:06.79 UTC (R4).
- **The Owner's word:** the user turn at `2026-09-25T10:11:44.435Z` reads *for v0.18.4 we need to fix CI*, with the run's
  link, three failed jobs pasted and the logs' path. The filing quotes it verbatim ✓; nothing needed normalising. Its time
  is 12:11:44 CEST (R4).
- **The replay:** a scratchpad clone at `840dabe`, `--triage`: *1 trackers to judge*, and FM-035's row, generated, equals
  the branch's in all eight derived cells. With `42f4eca`'s worksheet copied in: *Applied 1: FM-035: keep P1 #6 build*.
  FM-035, INDEX and the worksheet then match `42f4eca` byte for byte, and TRIAGE.md differs by the paragraph alone.
  Every front-matter change (`triaged:`, `rank: 6`, `next: build`, `tier: P1`) is the command's ✓.
- **At the tip:** `--triage` *Applied nothing*, exit 0, tree clean. `--check` 0 (*19 open*), `--session-check` 0, the
  generator leaves no diff, `merge-tree` against `origin/main` is clean, `test_shoalmark.py` 0 (394 ok), `test_core.py`
  0 (148 ok). `--next`: #1 FM-029 · #2 FM-007 · #3 FM-030 · #4 FM-005 · #5 FM-006 · #6 FM-035 · #7 … #10, each once. #6
  was free ✓.
- **TRIAGE.md:** two lines added under *Passes*; the intent and the current path are unchanged. The paragraph's last line
  keeps path 5: *the Owner lands it by merging — a merge rules nothing* ✓.

## Findings

**R1 · P2 · confidence high on the quote, medium (65%) on the tier · Path line 1 is quoted without *in the sitting*, and
the tier rests on the cut.**
- The Owner re-wrote line 1 at 10:37:13 today (`fe36cc0`, signed `G`): *… and no failed command in the sitting*.
- The Why quotes it as *the daily sitting runs on a tagged release with a signed answer and no failed command*. The hook
  paraphrases it as *no failed command — a red tag is one*. The Reason and the paragraph judge P1 on *a failed command on
  the current path, line 1*.
- With its last three words, line 1 does not carry a red CI. The sitting's commands on this machine are green (the
  filing's own *394 and 148*, and this run). On that ground the evening pass of 09-24 made FM-034 P2: *line 1's sitting
  runs in the Owner's checkout … so the sitting sees no failed run*. Today's review of his path update also read the
  narrowing that way: FM-030's anchor moved to line 6.
- The tier carries weight: line 3 makes *anything tagged … P1* a critical change.
- **Why P2:** the record changes the meaning of a line he signed today, and uses it to ground a judgement and write the
  board's hook.
- **Fix:** quote line 1 whole, in the hook and the Why. Judge the tier against it in the Reason, then run `--triage`.
  P1 holds if the record carries it:
  - line 2, if his word is a sitting's finding, filed that day and small;
  - or harm today to a user on Windows, if the logs show the tool failing and not the check (RV-479's `--answer` stops
    after deleting the branch).
  - Otherwise P2, *next*, which is what his *for v0.18.4* says.

**R2 · P3 · confidence high · The macOS traceback is not in the brand checks, and the log names its exception.**
- Line 1529 is in the answer-dialog checks: the radios, then *OK gives one command carrying the chosen option VERBATIM*.
  The brand checks are elsewhere: C1 at :1085, the 0.18.2 wordmark at :1156. The log interleaves stdout's C1–C5 lines
  with the traceback on stderr. The last check printed, *an ask that offers nothing shows only Other*, is the one just
  before :1529.
- The exception is `subprocess.TimeoutExpired`: headless Chrome, rendering `dlg-AP-080.html` in `_rows` (:1513), timed
  out after 60 seconds.
  - The filing says *the exception's text is in the job's log*, then guesses *no `HOME`? a font? `git` output?*. None of
    the three is the cause.
- The wrong place is also in the hook (*in the brand checks*) and in the ship-log row's reason for FM-011 and FM-006.
- **Fix forward:** the hook and the Now name the dialog check and the timeout; a correcting ship-log row.

**R3 · P3 · confidence high · `considered:` leaves out FM-003, the machine's first; FM-009 is not owed.**
- `--related FM-035`: FM-003 9.3, FM-006 7.9, FM-019 6.5, FM-001 6.3, FM-031 6.1, FM-028 6.0, FM-026 5.3, FM-009 5.3.
  On the title alone, at `57aac8d`: FM-003 8.1, FM-019 4.3, FM-006 2.4, FM-010 1.9, FM-009 1.1. FM-011 is in neither
  list.
- **FM-003** is the prior art. It is the Windows and Subversion tracker, and its 0.12.0 claim reads *Windows (3.9, 3.12),
  Linux (3.9, 3.12) and macOS are green on both suites*. Its findings were Windows paths and line endings: the filing's
  own *paths, line endings, a byte count*. FM-035 is that claim failing on a release tag, so FM-003 should be named.
- **FM-009** (`__version__` against `VERSION`, `--vendor`'s changelog) shares only the release words, and it is eighth.
  It need not be named.
- The worksheet marks FM-003 and FM-019 *NOT considered*, and the printed rule is *OPEN every one marked NOT considered*.
  The Reason names neither.
- The ship-log row credits *`--related`* with the choice of FM-028, FM-011 and FM-006. The seat chose them; `--related`
  put FM-003 first.
- **Fix forward:** `considered:` gains FM-003; a correcting row.

**R4 · P3 · confidence high · Two times.**
- *12:1x*, in the Now, the paragraph and the worksheet's Now cell, stands in for a time: the turn is 12:11:44 CEST
  (10:11:44Z). It should be exact.
- *09:57–10:02 UTC*, in the hook, the Now and INDEX, ends a minute early: windows 3.9 exits at 10:03:06 UTC.
- A detail: the first Windows check's name drops *, never inlined* without a `…`.

**R5 · P3 · confidence medium · The rank's reason does not match the rank.**
- The subject and the paragraph say *0.18.4's first build*, but #6 comes after FM-030 (#3, the 0.18.4 slice) and FM-006
  (#5, a P2 build).
- The Reason's *ahead of the unbuilt P2s* is not true of FM-006.
- **Fix forward:** say which build 0.18.4 starts with, and order the ranks to match, or drop *first*.

## Verdict

**NOT READY — R1 is P2.** The pass changes the meaning of the Owner's path line 1, and its tier rests on that change.
R2–R5 are P3; they are fixed forward, or taken into the same re-make.

What holds:
- The filing's facts that the logs carry: the jobs, the two Windows names and the `saw` text, line 1529, *394 and 148*.
- The Owner's words, quoted verbatim.
- Every front-matter change is the command's: the replay is byte-identical.
- #6 was free. The current path is untouched and path 5 is kept.
- The gates are green.

Carried, not graded:
- FM-029 holds #1 with its 0.18.3 work now tagged in `v0.18.3`.
- FM-005, a wait, holds #4 ahead of builds.

Not verified:
- *unproven: CI*, called *the Implementer's own line on 0.18.3*: it is not in this repository.
- Whether the Windows failures are the tool's or the checks'.

The Owner lands this by merging; a merge rules nothing (path 5).
