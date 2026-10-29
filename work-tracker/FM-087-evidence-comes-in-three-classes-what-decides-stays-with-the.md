---
id: FM-087
status: Proposed
considered: FM-006, FM-086, FM-024, FM-021, FM-027
tags: process, seamanship
epic: FM-089
hook: "Every round files its proof as files, and nothing tells what decides a verdict from what was worked with, or retires either. The evidence grows with every round: clones get slower for adopters, noise hides what decides, and each extra file is more surface for a leak."
---

# FM-087 — evidence comes in three classes: what decides stays with the record, what supports moves out, scratch stays on the machine

## What is true now

**Filed 2026-10-29; nothing is built. Allocated to v0.20.3 on the Owner's word of 29 October, as the Auditor relays
it;** v0.20.3's allocation, once it is filed, records it for the Owner's signed answer.

**The case, measured at main `d526547`:**
- `work-tracker/evidence/` holds 466 files, 23.7 MB.
- [FM-006](FM-006-shoalmark-has-one-document-written-for-agents-the-humans-who.md)'s evidence alone is 201 files,
  17.9 MB, 127 of them PNG.
- Every adopter clones all of it with the tool's repository.

**The design, on the Owner's word of 29 October:**
1. **Three classes:**
   - **What decides stays with the record:**
     - the verdict commit;
     - the hand-back's decisions;
     - the Owner's rulings and the messages that carry them;
     - one `SHA256SUMS` over everything else.
   - **What supports moves out:** logs, check and slice output, tars and screenshots go to a separate evidence
     repository.
     - They sit on a branch per release, one folder per review or run, each folder with its own `SHA256SUMS`.
     - Each release's branch is deleted once the release ships. The manifest still proves that each file existed and
       has not changed.
   - **Scratch stays on the machine and is never committed:** working copies, venvs, fixture homes, site builds and
     caches.
2. **A hand-back's shape:** its first part holds the verdict, the decisions and the open items, short enough to read
   at once. Tables of every check and every hunk are supports.
3. **Caches are refused:**
   - scripts run in an evidence folder write no bytecode (`PYTHONDONTWRITEBYTECODE=1`, or `-B`);
   - a manifest check refuses `__pycache__` and other caches, whose file names can carry local paths.
4. **Worktrees retire with their lane.** A seat's worktree is removed when its lane merges or is dropped; its evidence
   is kept by the manifest.
   - `--check` reads at most `WORKTREE_READ_CAP` (32) worktrees for its shared-harness check, so a sprawl of old
     worktrees hides seats from it.
   - On 29 October this repository moved from 118 worktrees to 18, and `--check` reads them all again.
5. **A soft budget,** as [FM-086](FM-086-a-tracker-states-one-deliverable-and-closes-when-it-ships.md)'s signals are:
   one line suggests that a tracker's evidence past a size, or a binary past a size, should move to supports. It never
   refuses.
6. **The public repository:**
   - images the site does not serve move out with the supports;
   - the setup page clones with `--depth 1`, so an adopter carries no history;
   - history is not rewritten.

## Why

A record is meant to be read back. What decides must stay small enough to read and to keep forever. What was worked
with is proof that the work happened, and a manifest keeps that proof without keeping the bulk beside the record.

## Done when

- [ ] The contract and the README name the three classes, and where each one lives.
- [ ] A check refuses caches in evidence, and its test shows the refusal.
- [ ] The soft budget's line is raised with its default keys, and has its test.
- [ ] The setup page clones with `--depth 1`, in English and German.
- [ ] The worktree rule is in the contract, and `--check` names the count it reads.
- [ ] v0.20.3's own reviews file their supports the new way.

## Ship log

| Date | Event |
|---|---|
| 2026-10-29 | Filed, on the Owner's word of 29 October, for v0.20.3. Records only. |
