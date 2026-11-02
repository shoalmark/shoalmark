---
id: FM-140
status: Proposed
considered: FM-023, FM-032, FM-134
tags: process
hook: "A root test file can sit outside CI, run by no job and named nowhere as excluded. The CI class fix makes every root test_*.py run in CI, directly or through test_core.py, or be named as excluded."
---

# FM-140 — a root test file can sit outside CI, run by no job and named nowhere as excluded

## What is true now

**2026-11-03 — filed for v0.20.3; nothing is built.** On the Owner's word of 29 October, the CI class fix moves to
v0.20.3 whole, with its three findings ([FM-023](FM-023-a-plan-names-its-seats-their-estimates-and-when-the-person.md)).
- **What it does:** every root `test_*.py` runs in CI, directly or through `test_core.py`, or is named as excluded.
- **Its three findings:** RV-3920 to RV-3922, from the review of the CI item that #219 merged.

## Why

A test file that no job runs holds nothing, and nothing says so.

## Done when

- [ ] Every root `test_*.py` runs in CI, directly or through `test_core.py`, or is named as excluded.
- [ ] A check holds it, so a new root test file is either run in CI or named.
- [ ] RV-3920 to RV-3922 are each fixed.

## Ship log

| Date | Event |
|---|---|
| 2026-11-03 | Filed for v0.20.3, from FM-023's entry of 29 October. Records only. |
