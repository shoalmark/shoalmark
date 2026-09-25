---
id: FM-036
status: Proposed
considered: FM-033, FM-028, FM-027
tags: bug
triaged: 2026-09-25
rank: 4
next: build
tier: P2
hook: "On 2026-09-25 the day's worksheet held two filled rows for FM-030 — the morning pass's `keep P1 #3 build` and the same-day re-judgement's `keep P1 #1 build` on a raise — and `apply_worksheet` applied both in order on every run: the rank read 1, then 3, then 1, each run printing *Applied 1*. A re-judgement the same day has no home on the sheet: the newest filled row for a tracker must win, or a second one be refused."
---

# FM-036 — A worksheet with two filled rows for one tracker applies both in order, so every run flips the rank

## What is true now

**Filed 2026-09-25 by the Principal seat, from its own pass's Reviewer (R1 on `fm/030-raised-the-missed-reads`); nothing is built.**
The raise rule (his answer `9e48ee8`) re-judges a tracker the same day it is raised. The day's worksheet already held FM-030's
morning row; the seat added a second filled row for the re-judgement. `apply_worksheet` reads every filled row and applies each in
order, so two runs of `--triage` on the same tree gave two different trees, and *Applied nothing* never came. The pass was sent back
on it; the seat struck the morning's row from the table and kept its text under it.

**What is left.** One of two: the newest filled row for a tracker wins (the sheet read bottom-up per tracker, the earlier row kept
as the record it is), or a second filled row for one tracker is refused by name. The first keeps a same-day re-judgement on the
day's sheet, which the raise rule needs. Until built, a seat keeps one filled row per tracker on a sheet and quotes the superseded
row's text under the table.

## Why

Path line 2: what a sitting finds is filed that day and fixed when small. A pass whose command does not converge cannot be verified
by replay, and the raise rule makes a second same-day judgement of one tracker the normal case, not the exception.

## Done when

- Two filled rows for one tracker on one sheet give one stable tree: two runs of `--triage`, the second *Applied nothing*.
- The rule the tool follows (newest wins, or refused) is printed in `--triage`'s rules and tested with today's FM-030 case.

## Ship log

| Date | Event |
|---|---|
| 2026-09-25 | Filed, from the Reviewer's R1 on the seat's same-day pass; `--related` held it against FM-033 (the pass before the build), FM-028 (the suite's clock) and FM-027 (ids claimed on a branch). |
