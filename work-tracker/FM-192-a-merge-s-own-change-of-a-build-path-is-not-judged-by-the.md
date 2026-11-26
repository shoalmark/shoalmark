---
id: FM-192
status: Proposed
considered: FM-019, FM-033, FM-161
tags: bug
hook: "A seat merges a side branch and moves a build path inside the merge, naming a tracker, and the hooks and --check pass it: the build gate judges the commits a merge brings and never the merge's own change, so a build change made inside a merge is judged by the session rule alone."
---

# FM-192 — a merge's own change of a build path is not judged by the build gate

Seat: the Planner (27f31560), the tool team's lead · filed 2026-11-26, from FM-161's critical review.

## What is true now

**Filed 2026-11-26, Proposed; no release is named, and nothing is built.** FM-161's critical review met it in its
second round. It is not that lane's.

- **The build gate judges no merge.** `commit_list` reads `git log --no-merges`, and `pending_judgement` judges a merge
  being made by the commits it brings. That is FM-033's design, the same on main's tool at the git top and below it.
- **A merge's own change** is what its result holds and no parent does, as FM-019 reads a merge for the rights rules.
  A seat whose session is set merges a side branch and, inside the merge, moves `src/app.py` into a team's project,
  naming the team's tracker. The hooks pass it, and `--check` passes after it, at the outer project and at the team's,
  exit 0. The same merge with no move passes the same way, in both layouts.
- **Only the session rule** judges what a merge itself changes.

## Why

A build change made inside a merge is a build change. Where only the commits a merge brings are judged, a merge can
carry work no pass has judged, which FM-033 closed for ordinary commits.

## Done when

Each item names its commit or pull request when it lands.

- [ ] **Decided** whether the build gate judges a merge's own change of a build path.
- [ ] **If it does:** judged as FM-019 reads a merge's own change, against every parent and under the merger, with a
  row for a merge made through the hooks and one judged after it; a clean merge adds nothing of its own and passes as
  now, with a row.

## Ship log

| Date | Event |
|---|---|
| 2026-11-26 | Filed, Proposed: the build gate judges the commits a merge brings and not the merge's own change; FM-161's critical review met it. Records only. |
