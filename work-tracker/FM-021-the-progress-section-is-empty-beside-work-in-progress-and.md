---
id: FM-021
status: In Progress
considered: FM-002, FM-005, FM-006, FM-009
tags: bug
next: review
hook: "The board says 13 trackers are in progress, and its progress section beside that reads 0. Nothing on the line says that the section stays empty until a first triage pass has run. The Owner read it as a defect."
---

# FM-021 — The progress section is empty beside work in progress and does not say why

## What is true now

**Built 2026-09-23 on `fix/0.17.5-one-id-one-row-and-an-empty-bucket-says-why`, for 0.17.5; open for review, not
merged.** The Principal chose the fix: a line that says why the section is empty. The rule itself stays. While no
tracker carries `triaged:` and `TRIAGE.md` records no pass (`LAST` and `HOME.last` both empty), the board's
`progress` line reads *empty until a first triage pass has run — --triage* (German: *leer, bis eine erste Sichtung
gelaufen ist — --triage*), under the new label `desc.progress.none`. Otherwise it reads as before. Only the page
changes. `INDEX.md` and `board()` do not.

| check | result |
|---|---|
| Chrome: two trackers `In Progress`, no pass | the new line. On 0.17.4: *kept by triage — by rank, then tier* (fails, as it should) |
| Chrome: one tracker carries `triaged:` | the usual line |
| Chrome: no `triaged:` left, but `TRIAGE.md` records a pass | the usual line |
| `test_core.py`, for a machine without a browser | the condition and the label are in the page; fails on 0.17.4 |
| key parity: the shipped German table and the suite's German fixture | both carry `desc.progress.none` (the fixture gained that one line) |

**What is left:** review, merge, the tag.

**The rule, on purpose.** `board()` (`shoalmark.py:606–614` at 0.17.4) puts `In Progress` work under `progress` only
once a pass has dated it with `triaged:`. Until then the work sits under `triage`. `owed_a_pass()` (:598–603) is the
one definition both the board and `--triage` ask, so the two never disagree.

**What the Owner sees.** No pass has ever run on this repository (the Research seat, 2026-09-23). So the board reads
`progress · 0 · kept by triage — by rank, then tier` while its counter says *13 in progress*. The `triaged` line says
*no triage pass has run yet*. The `progress` line gives no reason at all.

**Not chosen:** counting `In Progress` as progress until a first pass. The board would then list work that `--triage`
also lists as owed a pass, and the two would disagree.

## Why

A section that is empty by design has to say so. Otherwise it reads as a defect to the person the board is for.

## Done when

- On a board with `In Progress` work where no pass has run (no `triaged:` on any tracker, no pass in `TRIAGE.md`),
  the `progress` line says it is empty until a first triage pass has run, and names `--triage`.
- Once one tracker carries `triaged:`, the line is back to its usual text.
- The German table carries the same key.
- A check renders both cases in Chrome, plus a string check for a machine without a browser.

## Ship log

| Date | Event |
|---|---|
| 2026-09-23 | Built: the empty `progress` line says why while no pass has run, in English and German; three Chrome checks and a string check, shown to fail on 0.17.4. |
| 2026-09-23 | Filed. |
