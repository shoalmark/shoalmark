---
id: FM-113
status: Proposed
epic: FM-107
considered: FM-006, FM-092
tags: process
hook: "The landing's chart draws every tracker tagged bug or security as a wreck, Shipped and Closed ones included, with no limit. It should show only the active ones, at most 12, and keep the full totals in the top bar."
---

# FM-113 — the landing's wreck chart shows every bug and security tracker ever filed, closed ones included, with no limit

## What is true now

**2026-11-03 — filed; nothing is built.** On the Owner's word of 2 November.
- **Today:** `scripts/landing_facts.py` gives the chart every tracker tagged `bug` or `security`, Shipped and
  Closed included. The top bar counts the wrecks and the open ones.
- **What it does after this:**
  - the chart shows only active wrecks, In Progress and Proposed;
  - the top bar keeps the full totals and links the complete list;
  - at most 12 show, the most recently changed first, with security first, and "+N more" with the link when there
    are more.
- **When:** after v0.20.2's tag, in a landing update on main. It goes live by the Owner's own deploy.

## Why

A chart of every wreck ever filed hides the ones still open among the ones long cleared.

## Done when

- [ ] The chart shows only In Progress and Proposed wrecks: at most 12, the most recently changed first, with
  security first, and "+N more" with the link when there are more.
- [ ] The top bar keeps the full totals and links the complete list.
- [ ] It is live after the Owner's deploy of main.

## Ship log

| Date | Event |
|---|---|
| 2026-11-03 | Filed as a child of FM-107, on the Owner's word of 2 November. Records only. |
