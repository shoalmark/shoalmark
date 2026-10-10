# FM-006: 0.19.3, the release, its critical verdict at 763a0da

Verdict: **READY WITH FINDINGS**. Only P3s stand open: RV-2961, RV-2962, RV-2963 and RV-2964, for 0.19.4.
Reviewed: 763a0da89904ada688c573867ad744a0755b5fd5. Scope: `84d2ab8..763a0da`: the guard's merge (baa58cc), the release commit (0bb1b3b) and RV-2950's fix (763a0da). Tier: critical.

## The parts, and where each verdict was given

- Part A, the notice, Check A, the deriver's texts and the timing checks: READY, reviewer-121, at 31f38b4 (RV-2940 and RV-2941 fixed).
- Part B with C: READY WITH FINDINGS, reviewer-129, at 84d2ab8 (RV-2961 to RV-2964, P3).
- The Windows guard: READY WITH FINDINGS, reviewer-121, fdf1f01 at 7b55f46. RV-2942 is fixed at 3a0757c, and RV-2943 at 0bb1b3b.
- The Owner's independent re-check: READY at 84d2ab8. Its file is unchanged (sha256 d8624767…d2b1).
- This scope: READY, with RV-2950 fixed at 763a0da.

## What holds

- **The merge** brings the guard's change exactly: its patch-id equals 6828dba..3a0757c's. `shoalmark.py` is 84d2ab8's with the guard alone.
  - On Windows `--notify` starts no program, prints each notice with its status, and counts what it printed.
  - macOS and Linux are as at 84d2ab8, and the reads RV-2960, RV-2980 and RV-2981 changed are untouched.
  - Check A reads the tool clean.
- **The headline** is the Owner's version B, word for word, and each Security and Hardening bullet says what the code at the head does.
  - The board's reads: no fetch, no program a configuration names but the SSH signature check, no fsmonitor, no textconv, and `--text` on its six history reads.
  - The four pathspec variables are dropped for every git the tool starts.
  - Each read that lists what a commit or pending change touches lists submodule pointers too.
  - On macOS the notice's code is fixed and its text travels as data; on Linux the text goes after `--`; one failed notice never stops the others; on Windows each notice is printed and no program starts.
  - `view/built.json`, the deriver's texts and the notice's code as Check A reads it.
- **The GHSA ids** appear only in the CHANGELOG's Security section: its heading, and the two labels each bullet sits under.
- **The pins:** VERSION is 0.19.3. ADOPT.md and ADOPT.de.md name `v0.19.3` and 4a617ee4…b467, the SHA-256 of `shoalmark.py` at the head. Both setup pages clone `v0.19.3`.
- **The dates:** the CHANGELOG heading (2026-10-10), the landing's footer (10 October 2026), FM-030's and FM-045's rows, and INDEX.md all give the tag day. The top bar and the footer's link name v0.19.3.
- **The records:**
  - FM-045 keeps `status: Shipped` and says C's read-only half is in v0.19.3.
  - FM-030 says the notice's fix ships in 0.19.3, and what Windows does.
  - The history names private items only as recorded privately.

## Findings

- RV-2950: recorded privately. Fixed at 763a0da.
- Open, P3, for 0.19.4: RV-2961, RV-2962, RV-2963, RV-2964.

## Commands and controls: 2026-10-10, CEST, as `date` printed each

- At 763a0da, each exit 0 (03:50:23–03:50:55): `py_compile` under Python 3.14 and 3.9.6; `test_core.py`, all green; `--check`; `--session-check`.
- run-one-check, two at a time, at 763a0da: 16 blocks, 163 checks, each exit 0 (03:50:23–04:01:27). They are the notice, D and Check A blocks, the three submodule blocks, the footer, the setup pages and the version, `--vendor`, ADOPT and CHANGELOG readers.
- Controls beside 84d2ab8, each exit 1 (04:00:56–04:02:15): the notice block (its 5 Windows checks fail), and the footer check.
