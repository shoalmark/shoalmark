---
id: FM-118
status: Proposed
considered: FM-062, FM-065
tags: process
hook: "shoalmark.py's comments and docstrings have not been pruned by /prune-drift, and nothing holds a code comment to the external quirk it explains. The prose prune, proven prose-only, with its ratchet."
---

# FM-118 — shoalmark.py's prose is not pruned, and nothing holds code comments to external quirks

## What is true now

**2026-11-03 — filed; nothing is built.** It leaves FM-062 at its split, as the Owner's sweep words it, for v0.20.3.
- **What it takes:** the prose prune of `shoalmark.py`, proven prose-only, with the comment ratchet. It is one of
  `/prune-drift`'s outputs, moved to v0.20.3 on the Owner's word of 27 October, and one of FM-023's v0.20.3 rows.

## Why

Prose that outlives the code it describes reads as live. A prune that changes only prose, proven so, removes it without
risk to what runs.

## Done when

- [ ] `shoalmark.py`'s prose is pruned, and the change is proven prose-only.
- [ ] A ratchet holds each code comment to the external quirk it explains, with a mutant.

## Ship log

| Date | Event |
|---|---|
| 2026-11-03 | Filed from FM-062's split, for v0.20.3. Records only. |
