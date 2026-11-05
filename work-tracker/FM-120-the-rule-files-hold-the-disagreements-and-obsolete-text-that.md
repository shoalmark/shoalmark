---
id: FM-120
status: Proposed
considered: FM-062, FM-117, FM-095
tags: process
epic: FM-139
hook: "The rule files hold disagreements and obsolete text. A fresh /find-drift run on shoalmark finds them, and /prune-drift fixes them: v0.20.3's first lane."
---

# FM-120 — the rule files hold the disagreements and obsolete text that /find-drift finds on shoalmark

## What is true now

**2026-11-03 — filed for v0.20.3, its first lane; nothing is built.** It leaves FM-062 at its split. On the Owner's word
of 2 November it is v0.20.3's, and it is not one of FM-023's v0.20.3 rows.
- **What it takes:** a fresh `/find-drift` run on shoalmark at v0.20.3's start, then the fresh `/prune-drift` run
  that fixes what it finds in the rule files.
- **The first run's report** is held privately. This tracker works from the fresh run.

## Why

Two rule files that disagree, or a rule that no longer holds, send an agent off track. The skills built in v0.20.2 find
and fix them; this is their first full use on shoalmark.

## Done when

- [ ] A fresh `/find-drift` run on shoalmark is in the record.
- [ ] Its disagreements and obsolete text in the rule files are fixed by `/prune-drift`, or each is filed.

## Ship log

| Date | Event |
|---|---|
| 2026-11-03 | Filed from FM-062's split, for v0.20.3, its first lane, on the Owner's word of 2 November. Records only. |
| 2026-11-04 | `epic: FM-139`: a chapter of v0.20.3's epic. Records only. |
