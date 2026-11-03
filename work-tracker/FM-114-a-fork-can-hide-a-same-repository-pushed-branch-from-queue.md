---
id: FM-114
status: Proposed
considered: FM-006, FM-084, FM-019
tags: bug
hook: "--queue leaves out a pushed branch whose name or commit matches a pull request's head, or that a pull head contains, without asking which repository the pull request comes from. So a fork's pull request can hide a branch of this repository from the queue."
---

# FM-114 — a fork can hide a same-repository pushed branch from --queue, by name, by containment or by a closed pull head

## What is true now

**2026-11-03 — filed; nothing is built.** It is the remainder FM-006 left on 30 September from the review of the fork
queue's hardening ([review R3](evidence/reviews/review-fm-006-fork-queue-c2027d2.md)). It stands alone, on the Owner's
word of 2 November.
- `pushed_branches` in `shoalmark.py` takes the open pull requests' names and commits and every pull head's
  commit, with no repository provenance.
- It leaves out a branch that matches one of them by name or by commit, or that a pull head contains.
- It reads so at the release head.

## Why

The queue is where a pushed branch waits to be seen. A branch that a stranger's fork can hide from it is not seen.

## Done when

- [ ] `pushed_branches` reads open and closed pull requests by their provenance, so a fork's pull request hides no
  branch of this repository, by name, by commit or by containment.
- [ ] A class test covers each of the three, with a mutant of each.

## Ship log

| Date | Event |
|---|---|
| 2026-11-03 | Filed on its own from FM-006's close, on the Owner's word of 2 November. Records only. |
