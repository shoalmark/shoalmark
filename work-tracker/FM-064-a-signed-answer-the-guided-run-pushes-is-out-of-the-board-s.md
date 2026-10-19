---
id: FM-064
status: Proposed
considered: FM-059, FM-050, FM-030
tags: bug
next: wait
hook: "a signed answer the guided run pushes is out of the board's sight until its branch is merged"
---

# FM-064 — a signed answer the guided run pushes is out of the board's sight until its branch is merged

## What is true now

**Filed 2026-10-19; nothing is built.** The Designer found it in the Owner's spot-check of FM-059's design on 17
October. It is filed under its own id, on the Owner's word. Its fix lands with FM-059's build in v0.20.1, and that
build's Reviewer checks it.

- **What the board reads:** *answered, on its way* comes only from `origin/answer/<id>` branches not merged into the
  default branch: `on_their_way`, `shoalmark.py` lines 1958–1962 at `5dcdcc5`, and 1966–1970 at `be19828`.
- **Where FM-059's run pushes:** to the ask's home, which is the seat's branch that proposes the ask, or to the run's
  own `answers/<date>-<code>` (FM-059's *The design*, item 4).
- **What follows:** after the Owner signs, an ask the board shows as waiting goes on reading *waiting for you* until the
  merge.
- **There are two ways to fix it:**
  - the run pushes where the board reads;
  - the board reads the run's branches.
- **The Planner's lean: the board reads them (70 %).** R4 makes an ordinary Owner-signed commit the canonical answer, and
  removes the answer-branch code (FM-023's table under *What is true now*, 2026-10-15). So `answer/<id>` is no place to
  read. The board would read the answer commits on every branch of `origin` not merged into the default branch: each
  one bound to its ask by R4 (`Answers: <ask-id>`, FM-050 3b), and keyed by the ask's id. FM-050's design round places
  *on their way* in the guide.
- **Tier:** it is critical with FM-059's build, since it decides whether an answer the Owner signed reads as theirs.

## Why

The Owner reads the board after a sitting. An answer they signed and the run pushed must not read as waiting for them.

## Done when

- An answer the run pushes reads *answered, on its way* on the board, keyed by its ask's id, until its branch is merged.
  This holds for an answer pushed to a seat's branch and for one pushed to the run's own branch.
- The run's end says how the board shows each answer.
- FM-059's class test has a row for each of the two pushes. A mutant that reads `origin/answer/` only turns that row
  red.
- FM-059's build Reviewer has checked it.

## Ship log

| Date | Event |
|---|---|
| 2026-10-19 | Filed by the Planner seat, from the Designer's spot-check of FM-059's design, under its own id on the Owner's word; its fix lands with FM-059's build. Nothing is built. |
