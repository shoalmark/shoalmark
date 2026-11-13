---
id: FM-133
status: Proposed
epic: FM-088
considered: FM-088, FM-130, FM-042, FM-081
tags: process, seamanship
hook: "A memory entry is never tested and never retired. Each prose entry in team.md gets its scenario, run with and without it on Claude Code and on Codex, and /find-drift raises consider retiring for an entry whose dependency is gone."
---

# FM-133 — a memory entry is never tested or retired

## What is true now

**2026-11-13 — proposed to move to shoalmark/chart, not yet public, with its epic [FM-088](FM-088-the-team-s-lessons-live-only-in-each-harness-s-local-memory.md),** on the Auditor's
word of that day. Its place in v0.20.3 comes from FM-088's, which is the Owner's signed answer (`febbed9`), so
only an answer moves it: FM-139-Q1, when it is put on [FM-139](FM-139-v0-20-3-s-rows-sit-in-fm-023-fm-006-and-fm-053-so-no-one.md), asks the Owner to take it out of v0.20.3. It leaves
v0.20.3 in the commit that records that answer, and keeps FM-088 as its epic. It closes with `--close --moved-to`
once [FM-165](FM-165-a-tracker-can-only-be-closed-by-hand-so-its-open-asks-where.md) lands. No status changes by hand.

**2026-11-03 — filed for v0.20.3; nothing is built.** It is a part of the epic
[FM-088](FM-088-the-team-s-lessons-live-only-in-each-harness-s-local-memory.md), its items 8 and 9, as the Owner's sweep
words it. The design is FM-088's.
- **What it takes:** the scenario evals for each prose entry, on both harnesses with their tokens, and `/find-drift`
  reading the memory files for *consider retiring*.

## Why

Memory that is never tested can make a session worse, unseen. An entry whose subject is gone still reads as live.

## Done when

- [ ] Each prose entry in `team.md` has its scenario. The suite runs with and without each entry on Claude Code and on
  Codex, and reports the result and the tokens.
- [ ] `/find-drift` reads the memory files and raises *consider retiring* for an entry whose dependency is gone.

## Ship log

| Date | Event |
|---|---|
| 2026-11-13 | Proposed to move to shoalmark/chart, not yet public, with its epic FM-088; FM-139-Q1 is to ask the Owner to take it out of v0.20.3, and it leaves v0.20.3 in the commit that records the answer. Records only. |
| 2026-11-03 | Filed for v0.20.3 as a part of the epic FM-088, its items 8 and 9. Records only. |
