---
id: FM-121
status: Proposed
considered: FM-037, FM-065
tags: bug
hook: "The gate guards the Owner's two sections of TRIAGE.md. It does not guard the seat definitions or the skills folder, so a seat can change them and the gate lets it through. A design round first, then v0.20.3."
---

# FM-121 — a seat can change the seat definitions and the skills folder, and the gate lets it through

## What is true now

**2026-11-03 — filed; nothing is built.** It leaves FM-037 at its split, as the Owner's sweep words it, for v0.20.3,
after a design round.
- **What it takes:** the guard over the seat definitions and the skills folder. It moved to v0.20.3 on the Owner's
  word of 27 October, and FM-023's allocation holds it.
- **Already shipped under FM-037:** the guard over the Owner's two sections.

## Why

A seat definition and a skill say what a seat does. A seat that can change its own, unseen, changes its rules.

## Done when

- [ ] A design round, reviewed, and the Owner's word on it.
- [ ] The gate refuses a seat's change to the seat definitions and the skills folder, as the design says, with its
  tests and mutants.

## Ship log

| Date | Event |
|---|---|
| 2026-11-03 | Filed from FM-037's split, for v0.20.3 after a design round. Records only. |
