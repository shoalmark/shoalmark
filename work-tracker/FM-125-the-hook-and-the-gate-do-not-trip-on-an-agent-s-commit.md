---
id: FM-125
status: Proposed
considered: FM-007, FM-054
tags: security
hook: "A signature proves the key, not the hand. The hook and the gate do not trip on an agent's commit signed with the Owner's key: FM-007's tripwire, closure 3, with a mutation witness."
---

# FM-125 — the hook and the gate do not trip on an agent's commit signed with the Owner's key

## What is true now

**2026-11-03 — filed; nothing is built.** It leaves FM-007 at its split, as the Owner's sweep words it.
- **What it takes:** the tripwire, closure 3 of FM-007, in the tool, with a mutation witness.
- **Already shipped under FM-007:** the Owner's act of 15 October. The signing pages' key state is FM-108, and the
  proof line stays with FM-054.

## Why

An agent running as the Owner, with the Owner's key loaded, signs as them. A tripwire is the one closure the tool itself
can hold.

## Done when

- [ ] The hook and the gate trip on an agent's commit signed with the Owner's key, as closure 3 says.
- [ ] A mutation witness shows the tripwire catching it.

## Ship log

| Date | Event |
|---|---|
| 2026-11-03 | Filed from FM-007's split. Records only. |
