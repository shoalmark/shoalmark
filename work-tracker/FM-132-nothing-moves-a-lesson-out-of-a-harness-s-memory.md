---
id: FM-132
status: Proposed
epic: FM-088
considered: FM-088, FM-130, FM-078, FM-083
tags: process, seamanship
hook: "A lesson stays in the harness's memory where it was learned. The Board raises consider a memory sync per seat, and /sync-memory proposes each new entry with its scope and target, private details stripped."
---

# FM-132 — nothing moves a lesson out of a harness's memory

## What is true now

**2026-11-13 — proposed to move to shoalmark/chart, not yet public, with its epic [FM-088](FM-088-the-team-s-lessons-live-only-in-each-harness-s-local-memory.md),** on the Auditor's
word of that day. Its place in v0.20.3 comes from FM-088's, which is the Owner's signed answer (`febbed9`), so
only an answer moves it: FM-139-Q1, when it is put on [FM-139](FM-139-v0-20-3-s-rows-sit-in-fm-023-fm-006-and-fm-053-so-no-one.md), asks the Owner to take it out of v0.20.3. It leaves
v0.20.3 in the commit that records that answer, and keeps FM-088 as its epic. It closes with `--close --moved-to`
once [FM-165](FM-165-a-tracker-can-only-be-closed-by-hand-so-its-open-asks-where.md) lands. No status changes by hand.

**2026-11-03 — filed for v0.20.3; nothing is built.** It is a part of the epic
[FM-088](FM-088-the-team-s-lessons-live-only-in-each-harness-s-local-memory.md), its items 6 and 7, as the Owner's sweep
words it. The design is FM-088's.
- **What it takes:** the Board's soft signal per seat, *consider a memory sync*, and the `/sync-memory` skill with
  its eval. The tool never reads a harness's own folders.

## Why

A lesson that would help another session is lost when it stays where only one session can read it.

## Done when

- [ ] The Board raises *consider a memory sync* per seat, with its default key, and never refuses.
- [ ] `/sync-memory` proposes entries with their scope and target, with private details stripped, and has its own
  eval.

## Ship log

| Date | Event |
|---|---|
| 2026-11-13 | Proposed to move to shoalmark/chart, not yet public, with its epic FM-088; FM-139-Q1 is to ask the Owner to take it out of v0.20.3, and it leaves v0.20.3 in the commit that records the answer. Records only. |
| 2026-11-03 | Filed for v0.20.3 as a part of the epic FM-088, its items 6 and 7. Records only. |
