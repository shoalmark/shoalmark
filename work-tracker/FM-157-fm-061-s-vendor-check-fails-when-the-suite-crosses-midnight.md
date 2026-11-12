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
| 2026-11-12 | Judged keep P2 by a partial triage pass; In Progress. Records only. |
| 2026-11-12 | Filed. |
