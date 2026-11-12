---
id: FM-158
status: Proposed
considered: FM-157, FM-028, FM-035
tags: bug
next: build
hook: "The suite's checks that read today's date once can fail when a run crosses midnight: one is known, two are to be judged, and the rest of the suites are to be swept"
---

# FM-158 — The suite's checks that read today's date once can fail when a run crosses midnight

Seat: the Planner (27f31560) · filed 2026-11-12, on the Auditor's word of that day.

## What is true now

**Filed 2026-11-12; nothing is built.** FM-157 found the pattern in the vendor checks: a test reads today's date once,
then compares it with a date the tool writes later, so a run that crosses midnight fails. FM-157's review named more of
the same class in `test_shoalmark.py`. They are outside FM-157, since none is a `PIN`'s date. At main `ec8479c`:
- **Known to fail:** lines 16991–16994 run `--triage`, then read `today_` and open `triage-{today_}.md`. The tool names
  the worksheet by the date it runs on. A `--triage` before midnight and a read after it look for a file that does not
  exist. FM-157's review agrees.
- **To judge:**
  - line 18519 reads `since_` and `today_` once, and writes `answered: {today_}` into its fixtures;
  - line 18580 reads `today_` once, for `answered:` and for the date of the exchange under `## Asks`.
  
  The first question is whether a later check compares either with a date the tool reads. FM-157's review, from
  reading, sees neither failing; it did not run them.
- **To sweep:** every suite (`test_shoalmark.py`, `test_core.py` and the other `test_*.py` files) for the same pattern:
  a date read once and compared with one the tool writes or reads later. Each hit is named, failing or not, and why.

**The pattern to follow** is FM-157's `dated_run` in `test_vendor_release.py`. It reads the date just before the run
and just after it, and accepts either day, and no other.

**Order:** this is not built before the coordinator icon's design round and the seat pull request are through.

## Why

A check that fails on the time of day makes CI's verdict depend on when a run starts. Windows' suites run for more
than an hour, so a late start crosses midnight UTC, as run 42914315538 did. FM-157 fixed one family of such checks; the
rest of the class stays a known flake until each is judged, and a known flake hides a real failure of the same check.

## Done when

- every hit of the sweep is listed by file and line, failing or not, with why;
- each failing check reads the date on both sides of the run it compares, through `dated_run` or the same pattern;
- a check shows that each such comparison holds across a date change, without waiting for midnight;
- the change touches the tests only, with every label unchanged, and the suite passes;
- a review is READY.

## Ship log

| Date | Event |
|---|---|
| 2026-11-12 | Filed, on the Auditor's word, from FM-157's review. |
