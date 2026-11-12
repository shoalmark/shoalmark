---
id: FM-157
status: In Progress
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

**2026-11-12 — built: FM-061's class test reads the date on both sides of each `--vendor` run; the review is next.**
`test_vendor_release.py` no longer reads the date once at the start of `steps()`. One helper, `dated_run`, reads the
local date just before a `--vendor` run and just after it, with `datetime.date.today` as its default clock, and accepts
a `PIN` dated either day and no other. The first control and the four "…and `--vendor` from a release names it once more
and replaces it" checks use it. A new check, "a PIN's date is read before and after each --vendor run: where the clock
changes day during the run, …", gives the same helper a clock that changes day during the run and shows a `PIN` dated
either day accepted and one dated the day before or the day after those two refused. The class test holds 51 checks, the
base's 50 and the new one, each passing on Python 3.15 and on 3.9. Its `--mutants` run kills all 19 as it did before the
change. In scratch copies, the new check alone turns red when the helper reads the date once, before the run, as the
base did. The base with its date read as yesterday's fails the first control and the four checks above, as run
42914315538 did, and the head passes with the same shift. `shoalmark.py` is unchanged. Nothing in *Done when* is ticked:
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

- each check that compares a `PIN`'s date reads the date at its own `--vendor` run, or accepts the dates read just
  before and just after that run;
- a check shows that the comparison holds across a date change, without waiting for midnight;
- the change touches the test only, and the suite passes;
- a review is READY.

## Ship log

| Date | Event |
|---|---|
| 2026-11-12 | Built: FM-061's class test reads each PIN's date before and after its --vendor run through `dated_run`, and a new check holds the comparison across a date change; 51 checks, 19 mutants killed, the review next. |
| 2026-11-12 | Judged keep P2 by a partial triage pass; In Progress. Records only. |
| 2026-11-12 | Filed. |
