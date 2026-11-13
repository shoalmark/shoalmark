---
id: FM-130
status: Proposed
epic: FM-088
considered: FM-088, FM-104, FM-095
tags: process, seamanship
blocked-by: FM-104
hook: "The team's lessons and each seat's own have no home in the repository. --init writes memory/team.md, the schema names an entry's parts, and only the Owner's signed commit changes team.md. Where the files go comes from FM-104."
---

# FM-130 — the team's and each seat's memory is not in the repository

## What is true now

**2026-11-13 — proposed to move to shoalmark/chart, not yet public, with its epic [FM-088](FM-088-the-team-s-lessons-live-only-in-each-harness-s-local-memory.md),** on the Auditor's
word of that day. Its place in v0.20.3 comes from FM-088's, which is the Owner's signed answer (`febbed9`), so
only an answer moves it: FM-139-Q1, when it is put on [FM-139](FM-139-v0-20-3-s-rows-sit-in-fm-023-fm-006-and-fm-053-so-no-one.md), asks the Owner to take it out of v0.20.3. It leaves
v0.20.3 in the commit that records that answer, and keeps FM-088 as its epic. It closes with `--close --moved-to`
once [FM-165](FM-165-a-tracker-can-only-be-closed-by-hand-so-its-open-asks-where.md) lands. No status changes by hand.

**2026-11-03 — filed for v0.20.3; nothing is built.** It is a part of the epic
[FM-088](FM-088-the-team-s-lessons-live-only-in-each-harness-s-local-memory.md), its items 1 to 3, as the Owner's sweep
words it. The design is FM-088's.
- **What it takes:** `--init`'s `memory/team.md` and the contract's line on where memory belongs; the schema of an
  entry; and the guard that only the Owner's signed commit changes `team.md`.
- **Where the files go** comes from [FM-104](FM-104-the-person-s-own-files-are-spread-over-the-repository-and.md), and nothing of it is
  built before that decision.
- **A task in its lane:** every seat of this repository classifies its harness memories as product, project or local,
  FM-088's tenth item.

## Why

Memory kept where every seat and harness reads it, and changed under the same gate as the code it describes, is memory
the team shares.

## Done when

- [ ] `--init` writes `<tracker dir>/memory/team.md` and the contract's line on where memory belongs, in `AGENTS.md`
  and `CLAUDE.md`.
- [ ] `--schema` names an entry's source, `promote:`, state and dependencies. `--check` refuses an entry that quotes
  the Owner but cites no commit of the Owner's.
- [ ] `--check` refuses a change to `memory/team.md` that is not the Owner's signed commit. A seat's memory changes
  only by that seat's commit.

## Ship log

| Date | Event |
|---|---|
| 2026-11-13 | Proposed to move to shoalmark/chart, not yet public, with its epic FM-088; FM-139-Q1 is to ask the Owner to take it out of v0.20.3, and it leaves v0.20.3 in the commit that records the answer. Records only. |
| 2026-11-03 | Filed for v0.20.3 as a part of the epic FM-088, its items 1 to 3, blocked by FM-104. Records only. |
