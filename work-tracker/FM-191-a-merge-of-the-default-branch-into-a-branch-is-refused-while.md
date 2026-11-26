---
id: FM-191
status: Proposed
considered: FM-050, FM-141, FM-161
tags: bug
hook: "While the default branch is merged into a branch, the ledger's lint reads the asks the default branch put and answered since the branch's base as asks the branch proposes, and the commit hook refuses the merge commit with advice to renumber a record that is right."
---

# FM-191 — a merge of the default branch into a branch is refused while the default branch's tracker holds asks the branch's base lacks

Seat: the Planner (27f31560), the tool team's lead · filed 2026-11-26, on the coordinator's word of that day.

## What is true now

**Filed 2026-11-26, Proposed; no release is named, and nothing is built.** FM-161's lane met it, on the coordinator's
word of that day.

- **The lint.** `proposed_id_problems` reads each tracker that carries an ask id three ways: the working tree's copy,
  the copy at `HEAD`'s merge base with the default branch, and the default branch's copy. The ids the working tree holds
  and the merge base does not are the ids the branch proposes. One the default branch holds in a record, or below a
  higher number, is refused, with the advice to renumber the branch's ask.
- **During a merge of the default branch into a branch,** `HEAD` is still the branch's tip, so the merge base is the
  branch's old one. The working tree holds the default branch's tracker, with the asks it put and answered since. The
  lint reads those as asks the branch proposes, and refuses the merge commit in the commit hook, and `--check` says the
  same while the merge is made. Renumbering, as the line advises, would edit the default branch's record of an answered
  ask.
- **The merge that met it:** FM-161's lane, pass 6. The merge of main `62d5f15a` into the lane's `181f772e` was refused,
  "FM-161-Q3 is taken on origin/main". The same merge was made from main's side instead, main its first parent and the
  lane its second, so that `HEAD` was main while it was made: `c3f97710`, on that lane. Its tree is the one the refused
  merge staged, and FM-161's ask and answer lines are main's.
- **Once a merge commit is made,** the merge base is the default branch's commit, and the lint finds nothing. Only the
  commit being made is refused.

## Why

A gate that refuses a sound merge teaches a seat to look for a way around it. The default branch's own asks are not a
branch's proposal, and the line's advice, if followed, would rewrite a record that is right.

## Done when

Each item names its commit or pull request when it lands.

- [ ] **During a merge, the asks the merged commits bring from the default branch are not the branch's proposal:**
  the merge base is read with every `MERGE_HEAD`, or an id passes where the branch's copy holds the default branch's
  record of it unchanged. A row holds the merge through the commit hook, and a mutant of the change is killed.
- [ ] **An id the branch itself proposes is refused as now,** during a merge too, with a row.

## Ship log

| Date | Event |
|---|---|
| 2026-11-26 | Filed, Proposed: the ledger's lint refuses a merge of the default branch into a branch while that branch's tracker holds asks the branch's base lacks; FM-161's merge of main was made from main's side, `c3f97710`. Records only. |
