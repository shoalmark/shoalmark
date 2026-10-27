---
id: FM-076
status: In Progress
considered: FM-007, FM-024, FM-037, FM-054
tags: security
next: build
triaged: 2026-10-27
tier: P1
hook: "a seat's work that only another seat can push is refused, or recorded as that seat's own"
---

# FM-076 — a seat's work that only another seat can push is refused, or recorded as that seat's own

## What is true now

**2026-10-27 — judged In Progress, P1, critical, for v0.20.2's tag, on the Owner's word as relayed by the Auditor; the
seven points below are its design.** A Builder first writes a short design note into this tracker, the Auditor checks
it, then it builds, then the Auditor's independent critical review. RV-3910: recorded privately joins the round. It
reaches a host only through a tagged release, since `--vendor` takes nothing else, so it must be in v0.20.2's tag.

**Filed 2026-10-27, on the Owner's word as relayed by the Auditor.** It touches seats and rights, so it is critical.

On a host where one seat alone can push, another seat's work reaches the repository only through that seat. Today the
gate either refuses it, because the author is not a seat it knows, or records it as the relay's own. Both are false.

**The design:**
1. **Git keeps both.** The author is the seat that did the work, and the committer is the relay. A `Relayed-by:` trailer
   names the relay. `--check` requires it exactly when the committer is a relay and the author another seat.
2. **`[relays]` names who may relay for whom,** for example `auditor = ["planner", "designer"]`. It is the Owner's: it
   is read from the default branch, or changed only by the Owner's signed commit. A seat can never add itself on its own
   branch.
3. **A relay can write any author it likes, so an author's name proves nothing.** Until the author's own signature is
   checked, a relayed commit carries only acts that grant nothing: a new tracker, an ask, a note. The gate refuses a
   relayed triage, status change, verdict, rights or configuration change, signers or `TRIAGE.md` change, and `answer:`.
4. **Later, with a key for each seat on its own user,** a relayed commit signed by its author's key carries the author's
   rights, and the relay only transports it.
5. **The `Session:` line on a relayed commit is the author's claim.** Independence never counts it, and the Board and
   `--whoami` show the commit as relayed.
6. **The relay is a seat of its own,** with its own name and identity. It never shares another seat's, so two sessions
   never commit as one seat.
7. **Tests:** a relayed ask passes. Refused: a relay not in `[relays]`, an author that is not a known seat, each act in
   point 3, a relay that lists itself on a branch, and a missing or mismatched `Relayed-by:`. Plus the upgrade path for
   a repository on an older pin.

## Why

A record that names the wrong seat, or refuses true work, cannot be trusted on who did what. Rights follow who did it.

## Done when

- Points 1 to 7 are built with their tests, the Auditor's critical review finds them READY, and they ship in v0.20.2's
  tag.

## Ship log

| Date | Event |
|---|---|
| 2026-10-27 | Filed and judged In Progress, P1, critical, for v0.20.2's tag, on the Owner's word as relayed by the Auditor: relayed commits keep their author and name their relay. RV-3910: recorded privately joins the round. Records only. |
