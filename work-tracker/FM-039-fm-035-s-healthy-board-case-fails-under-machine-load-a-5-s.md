---
id: FM-039
status: In Progress
considered: FM-035, FM-038, FM-028, FM-012
tags: bug
triaged: 2026-09-27
rank: 7
next: review
tier: P2
hook: "FM-035's healthy-board case fails under machine load: a 5 s wall-clock Chrome budget, 469/470 at load 9–27"
---

# FM-039 — FM-035's healthy-board case fails under machine load: a 5 s wall-clock Chrome budget, 469/470 at load 9–27

## What is true now

**Built, not merged — on `fm/039-the-chrome-budget-follows-a-control` (`c0f9a86`), by the Implementer seat (`8e509911/implementer-48`) on 2026-09-28: the board's budget follows a control.** The suite already ran Chrome on `about:blank` before a browser block — the control that tells a platform gap from a hang; it now keeps that run's time, and every headless Chrome run's budget is counted beyond it: FM-035's healthy board gets 5 s beyond Chrome's own time, the suite's other pages 60 s beyond it. A page that does not come back is still tried twice and FAILS by name, the line naming both numbers — *headless Chrome did not return index.html within 5 s beyond Chrome's own 5.7 s, tried twice*; a control past 60 s, or no Chrome, is still the platform gap, skipped by name. Of the Done-when's three, this is the budget scaled to the load: the control is measured in the same run, just before the board, so what slows Chrome's start lengthens the budget by as much (one retry was there already). The suite case that says so is *FM-039 · a Chrome 5 s slower to start than this one … renders the healthy board and passes*: a stub adds 5 s before every Chrome run, the control's included — past a 5 s wall-clock budget before the page begins. **Proven here, 2026-09-28:** Chrome here needed 5.7–5.9 s for `about:blank` alone (5.4–5.5 s from about 19:30 the evening before); on an export of `origin/main` `bbbfc0b` the healthy run failed at a 1-minute load of 2.0 (exit 1, 16.3 s), on this branch it passed alone (17.4 s), the hang failed by name (27.3 s) and the slow start passed (36.4 s, control 11.7 s); the pre-commit hook ran both suites on both Pythons for `c0f9a86` and passed (1187 s, load 1.9–6.8). **Not proven:** a 1-minute load of 20 or more — none tonight (1.8–15.4 while this seat ran); the board's own cost beyond the control, under 1 s here, is not measured at that load.

**Filed 2026-09-26 by the Implementer seat (`8e509911/implementer-39`) at the 0.18.5 cut, under the freeze as a bug, on the slice B seat's finding of 18:3x; nothing was built then.** FM-035's case *Chrome here and a page that never comes back* (`test_shoalmark.py`) runs the board's browser block twice, as the suite runs it, with the Chrome budget cut to 5 s of wall-clock time: once on a page that hangs, which must fail, and once on the healthy board, which must pass. Under machine load the healthy run does not return in time and the case fails. The slice B seat (`8e509911/implementer-37`), on 2026-09-26: `test_shoalmark.py` on 3.9.6 read 469 of 470 in 3 of 3 full runs, each time this case, at a 1-minute load of 9–27 while other seats' suites and their Chrome ran; run alone at load 27, the pushed tip `f11bc04` failed it 4 of 4, as the slice's tree did, and at load 5 both passed it, 3 of 3 each — so it is the load, not a diff (`9f2f525`'s body). The Reviewer's pass on `9f2f525` saw the same on 3.14.3: 469 of 470 twice at load 5–9; the case alone failed on `main` and on `f11bc04` at load 12–20, passed with a 60 s budget, and passed 2 of 2 at load 3.9 (`evidence/reviews/review-fm-002-slice-b-f11bc04.md`, row 9). Since then the Principal starts seats' suites only under a 1-minute load of 6, one interpreter at a time. The fix — a CPU-time or load-scaled budget, or one retry — is forward, not in the 0.18.5 cut. Held against FM-035 (the case is its own; Shipped, its Done-when met by the v0.18.4 tag's green matrix — this is a new defect in its test, not an unmet line), FM-038 (the hook hides the suites' output — another cause at the same moment), FM-028 (the suite refused after midnight — a clock, not the load) and FM-012 (*load* there is a load of the trackers, not of the machine): none holds this.

## Why

A check that fails on a busy machine and passes on an idle one reads red about green code: a seat loses its hour to a re-run, or learns to discount a red suite, and the hook refuses a commit for the load, not the change. Several seats' suites and their Chrome run on one machine as a matter of course.

## Done when

The healthy run of FM-035's case passes on a machine at a 1-minute load of 20 or more while the hanging run still fails by name — its budget counted in the CPU time Chrome gets, scaled to the load, or retried once — and a suite case says which; judged by a pass before its first build commit (FM-033).

## Ship log

| Date | Event |
|---|---|
| 2026-09-26 | Filed at the 0.18.5 cut by the Implementer seat (`8e509911/implementer-39`), under the freeze as a bug, on the slice B seat's finding (`9f2f525`) and the Reviewer's row 9 on it; the facts, the why and the Done-when above. Nothing built. |
| 2026-09-28 | In Progress — the build, on `fm/039-the-chrome-budget-follows-a-control` off `origin/main` `bbbfc0b`, by the Implementer seat (`8e509911/implementer-48`): judged 2026-09-27, P2 #7, `next: build`; the status set before the first build commit, as the FM-033 rule asks. The rule chosen: the budget follows a control — Chrome's own time on `about:blank`, measured here before the board renders, plus 5 s for the board. Tonight Chrome here needs 5.4–5.5 s for `about:blank` alone, so the healthy run fails the 5 s budget on `main`'s own tool and the pre-commit hook refuses every commit that stages a `.py`. |
| 2026-09-28 | Built by the Implementer seat (`8e509911/implementer-48`) on `fm/039-the-chrome-budget-follows-a-control`: `1dcc2a8` (In Progress, tracker only), `c0f9a86` (the budget follows a control — `test_shoalmark.py`, the CHANGELOG bullet under *Unreleased — 0.18.6*; the pre-commit hook ran both suites on both Pythons and passed), this row (tracker only; `next: review` — the build is done, a Reviewer's pass is the next move). Not merged; the load-20 line of the Done-when unproven. |
