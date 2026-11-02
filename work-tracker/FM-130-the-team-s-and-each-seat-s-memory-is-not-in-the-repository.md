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
| 2026-11-03 | Filed for v0.20.3 as a part of the epic FM-088, its items 1 to 3, blocked by FM-104. Records only. |
