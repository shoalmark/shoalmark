---
id: FM-137
status: Proposed
considered: FM-018, FM-059, FM-115
tags: process
hook: "A run sheet asks a person who is not technical to read and run commands alone. The Owner's requirement of 28 September: a guided run-sheet dialog. The dashboard never runs a command, and every paste is screened for secret shapes before it is written."
---

# FM-137 — a run sheet has no guided dialog for a person who is not technical

## What is true now

**2026-11-03 — filed; nothing is built.** It is the second of the Owner's two dashboard requirements of 28 September,
held in FM-018 until v0.20.0's deletions were done, on the Owner's answer of 12 October. It is filed anew at FM-018's
close, as the Owner's sweep words it.
- **The requirement:** a guided run-sheet dialog, for non-technical users.
- **The counsel recorded with it:** a fixed step format first (command, expected output, stop rule, paste-back;
  lint-checked), then a one-step-at-a-time dialog whose paste-back fills the result table.
- **Its boundaries:** the dashboard never executes a command, and every paste is screened for secret shapes before it
  is written.
- **Next to it:** FM-059's prepared run, now [FM-115](FM-115-the-owner-answers-each-ask-in-the-board-s-one-dialog-and-no.md).

## Why

A run sheet is where a person meets the tool's hardest steps. A person who is not technical stops at the first one that
surprises them.

## Done when

- [ ] A run sheet's steps have a fixed format, lint-checked.
- [ ] A dialog guides a person through one step at a time, and their paste-back fills the result table.
- [ ] The dialog runs no command, and screens every paste for secret shapes before it is written.

## Ship log

| Date | Event |
|---|---|
| 2026-11-03 | Filed from FM-018's close. Records only. |
