---
id: FM-097
status: Proposed
considered: FM-062, FM-088, FM-095, FM-096
tags: seamanship
hook: "/find-drift reads decisions against git, but not the Owner's rulings. It would report each ruling as holding, drifted or broken, with every breach traced to its commit, pull request and CI run, so that with the register's signed history it becomes the full audit trail."
---

# FM-097 — /find-drift does not audit the Owner's rulings: whether each holds, drifted or was broken, and where

## What is true now
**Filed 2026-10-29 for v0.20.x; nothing is built.** On the Owner's word of 29 October: `/find-drift` must include
rulings, and trace where they were broken, so that it becomes the full audit trail. It is considered for every v0.20
release and pulled into one when it fits. [FM-089](FM-089-agentic-seamanship-v0-20-3.md), v0.20.3's chapter, names it as
a candidate, not a part.

- **Two questions per ruling:**
  - **Drift:** does what the ruling names still exist as named? A tool's path and hash, a check's name, a brief's line,
    a test file. An entry whose dependency is gone raises *consider retiring* or *consider re-stating*, as
    [FM-088](FM-088-the-team-s-lessons-live-only-in-each-harness-s-local-memory.md) does for memory.
  - **Breach:** where was it broken, and by whom? Each finding is traced to its commit, pull request, CI run and record.
    Three examples:
    - a pull request whose head was a commit holding only a verdict, with the CI run it cancelled;
    - a merge by the forge's button into a base that is not the default branch, which the gate already refuses (R14);
    - a pull request into such a base that was not a draft.
- **The report, per ruling:** *holds*, *drifted* (with what is missing), or *broken at* (with the traces, newest
  first), naming the seat and session that the trailers name.
  - Together with [FM-095](FM-095-the-owner-s-rulings-live-in-chat-memories-and-briefs-not-in.md)'s signed history, that
    is the audit trail: what was ruled, when and by whom, what enforces it, and every time it did not hold.
- **What it reads:** only what the repository holds: git and its trailers, pull requests, CI runs and records.
  - A ruling whose breach cannot be seen there says so in the register, and its eval scenario in
    [FM-096](FM-096-nothing-measures-whether-a-session-follows-the-rules-and.md) is its only proof.
  - Private findings appear only as "RV-…: recorded privately".
- **The order:** the last of the three, after FM-095 and FM-096. Its drift half needs only the register; the breach half
  is the larger part.

## Why
A ruling's record says what was decided, not whether it was kept.
[FM-062](FM-062-an-agent-drifts-off-track-where-a-rule-is-held-only-as-prose.md)'s `/find-drift` already reads decisions
and the record against git. The rulings are the decisions that bind every seat, so they belong in the same audit.

## Done when

- [ ] `/find-drift` reports each ruling as holds, drifted or broken at, with its traces.
- [ ] A fixture with one planted breach of each traceable kind is reported with its commit, pull request and run.
- [ ] Nothing private is read.

## Ship log

| Date | Event |
|---|---|
| 2026-10-29 | The order names FM-097 last of the three, after FM-096. Records only. |
| 2026-10-29 | Filed for v0.20.x, on the Owner's word of 29 October. Records only. |
