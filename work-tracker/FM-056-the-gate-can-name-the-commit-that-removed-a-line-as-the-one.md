---
id: FM-056
status: Proposed
considered: FM-019, FM-024, FM-004, FM-007
tags: bug
next: wait
hook: "The gate names who set a tracker's line with a pickaxe that also matches the commit that removed it, so a line a merge kept can be credited to the wrong commit and the wrong signature checked"
---

# FM-056 — the gate can name the commit that removed a line as the one that set it

## What is true now

**2026-10-27 — *who asked* moves to v0.20.3, and this fix goes with it, since *who asked* reads the same line,** on the Owner's word of 27 October, as relayed by the Auditor. FM-023's ask of 27 October puts the move to the Owner.

**Filed 2026-10-15; nothing is built.** It ships in v0.20.1 with *who asked*, which reads the same line (FM-023's
table of 2026-10-15).

**Facts,** read at main `272e374`.
- **How the setter is found.** `line_author` (`shoalmark.py:5537`) names who set a guarded line with
  `git log -1 --full-history -G <the exact line>` over `HEAD` and any merge heads (`:5605`). A merge carries no diff
  there, so the pickaxe names the last ordinary commit that wrote **or removed** the line.
- **The case.** FM-004's `next: owner` at `272e374`: `--check` verifies `6dda9b8`, the Owner's signed commit, as the
  commit that set it. `6dda9b8` removed that line. The line FM-004 carries came back through the resolution of the merge
  `696ee66`, a Planner-seat merge.
- **What it gets wrong:** who is shown as having set the line, and so whose signature the gate checks for it. *Who
  asked*, a v0.20.1 quick win, reads the same line.
- **What it does not open:** `rights_problems` judges a made merge's own `next: owner` on its change, under the merge's
  author (`:6393`). A seat without `ask` cannot bring the line in through a merge.

**Fix.** A removal never names a setter.
- A line the file carries is credited to the commit that added it, on the side the merge kept.
- A line no parent had stays the merge's own, judged as today.
- The method, a walk per parent or another, is the build's to choose and the review's to check.

**Test for the class.** A fixture table over a line set, removed and restored:
- on one branch;
- through a merge from either parent;
- in a merge's own resolution.

Each case names the commit that added the line the file carries, never one that removed it.
- A mutant that lets a removing commit win fails the table.
- The table includes this probe: a seat without `ask` merges `next: owner` in, and is refused.

**Tier:** critical: the gate's attribution and the signature it checks.

## Done when

The gate and *who asked* name the commit that added each guarded line, never one that removed it, and the class table,
its mutant and the merge probe are in CI.

## Ship log

| Date | Event |
|---|---|
| 2026-10-27 | *Who asked* moves to v0.20.3, and this fix with it, on the Owner's word of 27 October; FM-023's ask puts it to the Owner. Records only. |
| 2026-10-15 | Filed. |
