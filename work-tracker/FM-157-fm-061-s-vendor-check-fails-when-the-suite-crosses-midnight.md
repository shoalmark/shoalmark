---
id: FM-157
status: Shipped
considered: FM-061, FM-028, FM-011
tags: bug
next: build
triaged: 2026-11-12
tier: P2
hook: "FM-061's vendor check fails when the suite crosses midnight UTC: it reads today's date once, before the vendor runs"
---

# FM-157 — FM-061's vendor check fails when the suite crosses midnight UTC: it reads today's date once, before the vendor runs

Seat: the Planner (27f31560) · filed 2026-11-12, on the Auditor's word of that day.

## What is true now

**2026-11-12 — Shipped: merged to main as #287 (`9af3680`).** FM-061's class test and the suite's three `PIN`-date
checks read the date just before and just after each `--vendor` run, through one helper, `dated_run`, and accept a
`PIN` dated either day and no other. Every Done when item is met.

- **The review:** the standard review is READY WITH FINDINGS at `befdf49` (`1f5fd35`). Its two P3s, RV-4821 and
  RV-4822, are fixed forward in `b49c7d4` and `c619dc1`.
- **CI:** ci.yml's run 43216009955 passed on all five suites, the Pacific/Kiritimati rerun on Ubuntu with Python 3.9
  among them, and on CodeQL.
- **The change:** test files only, `test_vendor_release.py` and `test_shoalmark.py`; `shoalmark.py` is unchanged.

**2026-11-12 — built: FM-061's class test reads the date on both sides of each `--vendor` run; the review is next.**
`test_vendor_release.py` no longer reads the date once at the start of `steps()`. One helper, `dated_run`, reads the
local date just before a `--vendor` run and just after it, with `datetime.date.today` as its default clock, and accepts
a `PIN` dated either day and no other. The first control and the four "…and `--vendor` from a release names it once more
and replaces it" checks use it. A new check, "a PIN's date is read before and after each --vendor run: where the clock
changes day during the run, …", gives the same helper a clock that changes day during the run and shows a `PIN` dated
either day accepted and one dated the day before or the day after those two refused. A second, "a PIN's date is read
before and after each --vendor run: where the clock keeps its day during the run, …", gives the helper a clock that
keeps its day and shows only that day accepted, so a helper that reads once and also accepts the next day fails it
alone. The class test holds 52 checks, the base's 50 and the two new ones, each passing on Python 3.15 and on 3.9. Its
`--mutants` run kills all 19 as it did before the change. In scratch copies, the first new check alone turns red when
the helper reads the date once, before the run, as the base did. The base with its date read as yesterday's fails the
first control and the four checks above, where run 42914315538 failed three of the four and passed its first control,
and the head passes with the same shift. In `test_shoalmark.py`, the three checks that compared a `PIN`'s date by one
read, FM-011's at line 2400 and FM-004's at lines 2794 and 2952, now use `dated_run` too, and the FM-004 check that
reads `--check`'s line expects the day the `PIN` holds. `shoalmark.py` is unchanged. Nothing in *Done when* is ticked:
the review and the merge do that.

**2026-11-12 — judged before its first build commit: keep P2, In Progress.** A partial triage pass judged this
row alone ([worksheet](evidence/triage/triage-2026-11-12.md)). Unranked. The fix is built alone, in the test only,
on a branch from this filing, with a standard review; its pull request follows the filing's merge.

**Filed 2026-11-12; nothing is built.** On ci.yml's run 42914315538, the job *suites (windows, 3.9)* ran from 22:24 to
00:02 UTC. FM-061's class test, `test_vendor_release.py`, passed its first control, "from a clean clone at its release
tag, `--vendor` vendors the whole tool". At 00:00:25 UTC on 2026-11-11 it then failed its three later checks, "…and
`--vendor` from a release names it once more and replaces it": one with `--allow-untagged`, one with `--partial`, and
one with both flags.

**Why:** `steps()` reads the date once, at its start (`test_vendor_release.py` line 203,
`today = datetime.date.today().isoformat()`). It then expects every `PIN` to say `vendored {today}`. But each `--vendor`
run writes the date it runs on, and those three runs fell after midnight.

**Not FM-028:** there the board and the tool count days by two different clocks. Here one clock is read too early in a
long run. The fix is in the test only.

## Why

A check that fails on the time of day makes CI's verdict depend on when the run starts. It also hides a real failure
of the same check behind a known flake.

## Done when

- [x] each check that compares a `PIN`'s date reads the date at its own `--vendor` run, or accepts the dates read just
  before and just after that run;
  · `5eea477`, `0d7579e`, merged in `9af3680`
- [x] a check shows that the comparison holds across a date change, without waiting for midnight;
  · `5eea477`, and `b49c7d4` for a clock that keeps its day
- [x] the change touches the test only, and the suite passes;
  · `test_vendor_release.py` and `test_shoalmark.py` only; ci.yml's run 43216009955 green on all five suites
- [x] a review is READY.
  · READY WITH FINDINGS at `befdf49`, `1f5fd35`; its two P3s fixed forward

## Ship log

| Date | Event |
|---|---|
| 2026-11-12 | Shipped: merged to main as #287 (9af3680). The vendor checks read a PIN's date on both sides of each run (5eea477, 0d7579e), the review READY WITH FINDINGS (1f5fd35) with its two P3s fixed forward (b49c7d4, c619dc1), CI green, and every Done when item is met. |
| 2026-11-12 | RV-4821 and RV-4822, the review's two P3s, fixed forward: a second check holds `dated_run` where the clock keeps its day, and the record names run 42914315538 as it failed. |
| 2026-11-12 | The suite's three PIN-date checks, FM-011's and two of FM-004's in test_shoalmark.py, read the date on both sides of their --vendor run through `dated_run`, labels unchanged. |
| 2026-11-12 | Built: FM-061's class test reads each PIN's date before and after its --vendor run through `dated_run`, and a new check holds the comparison across a date change; 51 checks, 19 mutants killed, the review next. |
| 2026-11-12 | Judged keep P2 by a partial triage pass; In Progress. Records only. |
| 2026-11-12 | Filed. |
