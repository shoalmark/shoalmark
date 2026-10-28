---
id: FM-062
status: In Progress
considered: FM-042, FM-037, FM-026, FM-023
tags: process
next: build
triaged: 2026-10-19
tier: P2
hook: "an agent drifts off track where a rule is held only as prose, two sources disagree, or obsolete text still reads as live"
---

# FM-062 — an agent drifts off track where a rule is held only as prose, two sources disagree, or obsolete text still reads as live

## What is true now

**2026-10-27 12:45:28 CET** — CI runs `test_plugin.py` after `test_core.py` under the full-suite tier condition and includes all three suites and exits in its TZ report; the CI checks and mutants cover the third suite and its tracker-read scan. Critical review next.

**2026-10-19 17:22:20 CEST — `/prune-drift`'s spec and proof are built in `7983283` and `8f22b12`; nine fixtures and six mutants pass on Python 3.15.0 and 3.9.6, review next.**

**Filed 2026-10-18. Judged In Progress, P2, on 2026-10-19, before the first build commit; `/find-drift`'s spec and the plugin are built, review next.** Its work
is v0.20.2's allocation, which the Owner accepted in FM-023 (`88bf707`). Work on v0.20.2 starts on branches, on the
Owner's ruling of 19 October, and lands after v0.20.1. `/find-drift`'s spec and the plugin come first.
The second skill is named `/prune-drift`, the Owner's word of 18 October (recorded privately).

- **The problem:** a rule an agent should keep is often held only as prose: in `AGENTS.md`, the contributing guide, the
  triage rules, a seat definition or a brief. An agent may never read it, or may read it and go the other way. Two
  sources can state one rule differently, and text that a later ruling revoked can still read as live.
- **What v0.20.2 proposes,** in FM-023's table of 2026-10-18:
  - **`/find-drift`,** a skill that reads the repository and writes only its report and the report's hash, or a
    private supplement where the person names its folder. It commits nothing. It finds these three kinds of drift
    point, grades each rule on five layers, and ranks what can become a check. The layers are: impossible to break;
    the build fails; a rule or a review; a skill; a style guide.
  - **`/prune-drift`,** the second skill, built on it, that moves history to the record and rules to checks.
  - Both skills ship in one Claude plugin.
- **Its first run,** on shoalmark at `5dcdcc5`, is recorded privately.

## Why

A check refuses a break every time it runs, but prose works only when it is read and kept. The places where a rule is
only prose are where an agent drifts. Finding them is the first step to making them checks.

## Done when

- `/find-drift` and `/prune-drift` ship in v0.20.2's Claude plugin, each reviewed like code.
- A second run, on a codebase shoalmark did not shape, has corrected `/find-drift`'s spec.
- shoalmark's own report is in the record.

## Ship log

| Date | Event |
|---|---|
| 2026-10-27 12:45:28 CET | CI adds the plugin suite in `89b7f7a`; both Python versions pass the plugin, core, CI and release-workflow slices. The plugin reads no tracker paths; a synthetic tracker-read control proves that a future read needs a records-tier exclusion. Critical review next. |
| 2026-10-20 09:45:15 CEST | Round 2 RV-3501 addressed in `a5296ee`: the proof retains the active shebang line from the original bytes, including its terminator; executable LF/CRLF regressions verify exact committed blobs. All 17 fixtures pass and all nine scratch mutants are caught on Python 3.15.0 and 3.9.6. The Owner authorized this fix after the original final round; independent verification remains pending. |
| 2026-10-19 21:34:00 CEST | Round 1 RV-3500 addressed in `46eff9f`: the proof compares raw-byte shebang activation, including a preceding BOM, and directive attachment to its physical code line. All 15 fixtures pass and all eight scratch mutants are caught on Python 3.15.0 and 3.9.6; round 2 next. |
| 2026-10-19 17:22:20 CEST | `/prune-drift`'s spec and proof built on `/find-drift`'s READY head: the sort, record-before-delete steps, reader and directive safeguards, and nine-fixture class test are in `7983283` and `8f22b12`; all six scratch mutants are caught on both interpreters. Review next; suite registration waits for v0.20.2's integration branch. |
| 2026-10-19 13:12:55 CEST | Round 1's RV-3491, RV-3492 and RV-3493 fixed: the description names the report destination, the tracker folder's fallback is explicit, and scoped runs retain the snapshot and source hashes; round 2 next. |
| 2026-10-19 12:38:39 CEST | `/find-drift`'s spec and the plugin built in `818eb0c` and `0289061`; the standalone structure test passes on Python 3.15 and 3.9.6, with all four mutants refused on both. Review next; suite registration and `drift_sources` reader support follow on the integration lane. |
| 2026-10-19 | *What is true now* corrected by the Planner: `/find-drift` reads the repository and writes only its report, its hash or a named private supplement; it is not read-only. |
| 2026-10-19 | Judged In Progress, P2, by the Planner, before the first build commit: `/find-drift`'s spec and the plugin, on `fm/062-find-drift`. |
| 2026-10-18 | The second skill named `/prune-drift`, the Owner's word of 18 October (recorded privately); v0.20.2's allocation accepted (`88bf707`). |
| 2026-10-18 | Filed, with v0.20.2's allocation ask on FM-023. |
