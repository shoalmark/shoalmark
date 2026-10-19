---
id: FM-062
status: In Progress
considered: FM-042, FM-037, FM-026, FM-023
tags: process
next: owner
triaged: 2026-10-19
tier: P2
hook: "an agent drifts off track where a rule is held only as prose, two sources disagree, or obsolete text still reads as live"
ask: "Do /find-drift's five layers keep your order of 18 October, with a skill below a rule a reviewer checks, as FM-062's section The layer order, for the Owner sets out?"
ask-kind: ruling
ask-since: 2026-10-19
ask-options: "yes, the order stays | no: a skill ranks above a rule a reviewer checks"
ask-proposal: "yes, the order stays"
---

# FM-062 — an agent drifts off track where a rule is held only as prose, two sources disagree, or obsolete text still reads as live

## What is true now

**2026-10-19 17:22:20 CEST — `/prune-drift`'s spec and proof are built in `7983283` and `8f22b12`; nine fixtures and six mutants pass on Python 3.15.0 and 3.9.6, review next.**

**2026-10-19 — one ask, on the layer order.** `/find-drift`'s spec keeps the five layers in the order the Owner
accepted. Whether a skill should rank above a rule a reviewer checks is put to the Owner, under *The layer order, for
the Owner* below. The build goes on meanwhile.

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

## The layer order, for the Owner

- **The question:** does a skill rank above a rule a reviewer checks?
- **Today's order,** which the Owner accepted with v0.20.2's allocation on 18 October (FM-023, `88bf707`):
  1. impossible to break;
  2. the build fails;
  3. a rule or a review;
  4. a skill;
  5. a style guide.
- **Why it is asked:** the spec's second run, on a codebase shoalmark did not shape, met fixes that are a command or a
  skill carrying a rule. By today's order such a fix ranks below a rule a reviewer checks. The seat that ran it
  proposed putting a skill third and a reviewed rule fourth, at 55 %.
- **Already settled in the spec:** a generator that writes the result is layer 1, so a command that writes what the
  rule asks for is not graded as a skill.
- **The proposal: the order stays (65 %).** A review stands on every merge's path (the current path's line 2), while a
  skill acts only where an agent invokes it. A rule moved into a skill stops no break that nobody invokes it for.
- **If the order changes,** only step 5 of the spec changes, the grading.

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
| 2026-10-19 17:22:20 CEST | `/prune-drift`'s spec and proof built on `/find-drift`'s READY head: the sort, record-before-delete steps, reader and directive safeguards, and nine-fixture class test are in `7983283` and `8f22b12`; all six scratch mutants are caught on both interpreters. Review next; suite registration waits for v0.20.2's integration branch. |
| 2026-10-19 13:12:55 CEST | Round 1's RV-3491, RV-3492 and RV-3493 fixed: the description names the report destination, the tracker folder's fallback is explicit, and scoped runs retain the snapshot and source hashes; round 2 next. |
| 2026-10-19 12:38:39 CEST | `/find-drift`'s spec and the plugin built in `818eb0c` and `0289061`; the standalone structure test passes on Python 3.15 and 3.9.6, with all four mutants refused on both. Review next; suite registration and `drift_sources` reader support follow on the integration lane. |
| 2026-10-19 | *What is true now* corrected by the Planner: `/find-drift` reads the repository and writes only its report, its hash or a named private supplement; it is not read-only. |
| 2026-10-19 | One ruling ask put by the Planner: whether a skill ranks above a rule a reviewer checks; the proposal keeps the order the Owner accepted. |
| 2026-10-19 | Judged In Progress, P2, by the Planner, before the first build commit: `/find-drift`'s spec and the plugin, on `fm/062-find-drift`. |
| 2026-10-18 | The second skill named `/prune-drift`, the Owner's word of 18 October (recorded privately); v0.20.2's allocation accepted (`88bf707`). |
| 2026-10-18 | Filed, with v0.20.2's allocation ask on FM-023. |
