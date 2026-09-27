---
id: FM-039
status: Proposed
considered: FM-035, FM-038, FM-028, FM-012
tags: bug
triaged: 2026-09-27
rank: 7
next: build
tier: P2
hook: "FM-035's healthy-board case fails under machine load: a 5 s wall-clock Chrome budget, 469/470 at load 9–27"
---

# FM-039 — FM-035's healthy-board case fails under machine load: a 5 s wall-clock Chrome budget, 469/470 at load 9–27

## What is true now

**Filed 2026-09-26 by the Implementer seat (`8e509911/implementer-39`) at the 0.18.5 cut, under the freeze as a bug, on the slice B seat's finding of 18:3x; nothing is built.** FM-035's case *Chrome here and a page that never comes back* (`test_shoalmark.py`) runs the board's browser block twice, as the suite runs it, with the Chrome budget cut to 5 s of wall-clock time: once on a page that hangs, which must fail, and once on the healthy board, which must pass. Under machine load the healthy run does not return in time and the case fails. The slice B seat (`8e509911/implementer-37`), on 2026-09-26: `test_shoalmark.py` on 3.9.6 read 469 of 470 in 3 of 3 full runs, each time this case, at a 1-minute load of 9–27 while other seats' suites and their Chrome ran; run alone at load 27, the pushed tip `f11bc04` failed it 4 of 4, as the slice's tree did, and at load 5 both passed it, 3 of 3 each — so it is the load, not a diff (`9f2f525`'s body). The Reviewer's pass on `9f2f525` saw the same on 3.14.3: 469 of 470 twice at load 5–9; the case alone failed on `main` and on `f11bc04` at load 12–20, passed with a 60 s budget, and passed 2 of 2 at load 3.9 (`evidence/reviews/review-fm-002-slice-b-f11bc04.md`, row 9). Since then the Principal starts seats' suites only under a 1-minute load of 6, one interpreter at a time. The fix — a CPU-time or load-scaled budget, or one retry — is forward, not in the 0.18.5 cut. Held against FM-035 (the case is its own; Shipped, its Done-when met by the v0.18.4 tag's green matrix — this is a new defect in its test, not an unmet line), FM-038 (the hook hides the suites' output — another cause at the same moment), FM-028 (the suite refused after midnight — a clock, not the load) and FM-012 (*load* there is a load of the trackers, not of the machine): none holds this.

## Why

A check that fails on a busy machine and passes on an idle one reads red about green code: a seat loses its hour to a re-run, or learns to discount a red suite, and the hook refuses a commit for the load, not the change. Several seats' suites and their Chrome run on one machine as a matter of course.

## Done when

The healthy run of FM-035's case passes on a machine at a 1-minute load of 20 or more while the hanging run still fails by name — its budget counted in the CPU time Chrome gets, scaled to the load, or retried once — and a suite case says which; judged by a pass before its first build commit (FM-033).

## Ship log

| Date | Event |
|---|---|
| 2026-09-26 | Filed at the 0.18.5 cut by the Implementer seat (`8e509911/implementer-39`), under the freeze as a bug, on the slice B seat's finding (`9f2f525`) and the Reviewer's row 9 on it; the facts, the why and the Done-when above. Nothing built. |
