---
id: FM-117
status: Proposed
considered: FM-062, FM-097, FM-083
tags: process
hook: "/find-drift reads the rule files against each other, not decisions against the repository's state. Its next round of 27 October adds decisions as sources, the record against git, stranded work, and an evidence chain for each finding."
---

# FM-117 — /find-drift does not read decisions against git, find stranded work, or give each finding its evidence chain

## What is true now

**2026-11-03 — filed; nothing is built.** It leaves FM-062 at its split, as the Owner's sweep words it.
- **What it takes:** `/find-drift`'s next round of 27 October, its six points, as FM-062's text sets them out:
  1. decisions are sources: the trackers' asks and their allocation rows;
  2. the record against git: tags, merges and CHANGELOG sections;
  3. stranded work, a fourth kind: a READY verdict, or an ask in a tracker's front matter, on a branch the default
     branch never received, read from local refs;
  4. every finding carries its evidence chain, each commit by full sha, with the query that found it;
  5. its own claims cite the file, line or commit they read;
  6. a scoped run before every release sitting.
- **Already shipped under FM-062:** `/find-drift` and `/prune-drift` in the Claude plugin.

## Why

The drift that cost most sat between a decision, its record and the repository's state, where the skill does not look
yet.

## Done when

- [ ] The six points are in `/find-drift`'s spec, reviewed like code.
- [ ] A run shows each kind of finding with its evidence chain.

## Ship log

| Date | Event |
|---|---|
| 2026-11-03 | Filed from FM-062's split. Records only. |
