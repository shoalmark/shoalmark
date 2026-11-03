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
| 2026-11-03 | Filed for v0.20.3 as a part of the epic FM-088, its items 6 and 7. Records only. |
