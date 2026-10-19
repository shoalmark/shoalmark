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

**Filed 2026-10-18. Judged In Progress, P2, on 2026-10-19, before the first build commit; nothing is built.** Its work
is v0.20.2's allocation, which the Owner accepted in FM-023 (`88bf707`). Work on v0.20.2 starts on branches, on the
Owner's ruling of 19 October, and lands after v0.20.1. `/find-drift`'s spec and the plugin come first.
The second skill is named `/prune-drift`, the Owner's word of 18 October (recorded privately).

- **The problem:** a rule an agent should keep is often held only as prose: in `AGENTS.md`, the contributing guide, the
  triage rules, a seat definition or a brief. An agent may never read it, or may read it and go the other way. Two
  sources can state one rule differently, and text that a later ruling revoked can still read as live.
- **What v0.20.2 proposes,** in FM-023's table of 2026-10-18:
  - **`/find-drift`,** a read-only skill. It finds these three kinds of drift point, grades each rule on five layers,
    and ranks what can become a check. The layers are: impossible to break; the build fails; a rule or a review; a
    skill; a style guide.
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
| 2026-10-19 | Judged In Progress, P2, by the Planner, before the first build commit: `/find-drift`'s spec and the plugin, on `fm/062-find-drift`. |
| 2026-10-18 | The second skill named `/prune-drift`, the Owner's word of 18 October (recorded privately); v0.20.2's allocation accepted (`88bf707`). |
| 2026-10-18 | Filed, with v0.20.2's allocation ask on FM-023. |
