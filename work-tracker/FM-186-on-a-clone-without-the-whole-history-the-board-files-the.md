---
id: FM-186
status: Proposed
considered: FM-034, FM-169, FM-173
tags: bug
hook: "On a clone that does not hold the default branch's history whole, the Board opens with \"NOTHING NEEDS THE OWNER.\" and files every open ask put under the Owner's identity as sent back, for the seat to fix. The asks are sound and wait for the Owner; the cause is the clone. The fix: such asks stand under a heading that says the clone cannot verify them, as the gate's summary does, and the first line no longer says nothing needs the Owner. No release is named."
---

# FM-186 — on a clone without the whole history, the Board files the Owner's open asks as the seat's to fix

Seat: the Planner (a1730572) · filed 2026-11-21, on the coordinator's word of that day.

## What is true now

**Filed 2026-11-21, Proposed; no release is named, and nothing is built.** FM-169's critical read found it, as a P3 to
fix forward: RV-9031: recorded privately.

- **On a clone of depth 1 or 2,** with nothing added, `--owner` on a ledger whose open asks were put under the Owner's
  identity prints "NOTHING NEEDS THE OWNER.", then "N ASK(S) SENT BACK — NOT FOR YOU (the seat fixes these; they reach
  you when they pass the gate)", with each of those asks under it. With the whole history, it prints "N NEED THE
  OWNER" and the same asks.
- **With FM-169's change,** each line under that heading says the clone cannot verify the commit that set
  `next: owner`, and names the way through: fetch the history whole. The gate's summary calls the same lines this
  checkout's own finding, and says the ledger is sound. The Board's two headings do not.

## Why

The Board is where the Owner reads what waits for them. A first line that says nothing needs them, while their asks
wait, sends them away; and a heading that files those asks as the seat's to fix says the opposite of what is true. The
cause is the clone, and the Board should say so where it files them.

## Done when

Each item names its commit or pull request when it lands.

- [ ] **On a clone without the whole history,** asks held only by that clone's own finding stand under a heading that
  says the clone cannot verify them and names the way through, as the gate's summary does.
- [ ] **The first line** does not say that nothing needs the Owner while such asks are open.
- [ ] **With the whole history,** `--owner` prints as it does now.
- [ ] **One row holds it,** failing before the fix and passing with it, and a mutant of the new rule is killed.

## Ship log

| Date | Event |
|---|---|
| 2026-11-21 | Filed, Proposed: on a clone without the whole history, the Board files the Owner's open asks as the seat's to fix. No release. Records only. |
