---
id: FM-023
status: Proposed
considered: FM-004, FM-005, FM-006
tags: research
kind-of-problem: complex
next: review
hook: "A plan names its seats, their estimates and when the person is needed; it is updated as the work runs and recorded when done — so a person can plan what to take in, and when to be available"
---

# FM-023 — a plan names its seats, their estimates and when the person is needed, updated as it runs, recorded when done

Seat: Principal · filed 2026-09-23 on the Owner's requirement. Tagged `research`: written to be attacked before anything
is designed or built.

## What is true now

**Filed 2026-09-23; nothing is built.** A tracker today holds what and why, a `next:`, an ask and its answer, a ship log.
It holds no plan: which seat does which step, how long each is expected to take, and when the person in charge is
needed — before the work, updated while it runs, recorded when done. The board can say *what waits on you*; it cannot
say *when you will be needed, for what, for how long*.

**The Owner's requirement, 2026-09-23** *(spelling normalised at his request; the meaning unchanged)*: *"When this is
tracked and updated, we can communicate to a person in charge, or even a seat, when they are expected to be involved or
available. Better planning becomes possible only by giving an estimate before, then updating during, recording when
done. This feeds back into the system. What I especially liked in the initial estimate was a time window listing the
task splits with seats and their timing — having this available when planning what to take in or not, and when I have
to be available, would be awesome."*

**The instance that raised it (numbers only).** A release arc estimated at 12:55 as six seat steps and two Owner
windows: Research ≈ 13:05 · filings ≈ 13:30 · build ≈ 14:30 · review + one fix round ≈ 15:30 → window 1 ≈ 15:30–16:00
(open + merge, tag) · vendor + review ≈ 16:30 → window 2 ≈ 16:30–17:00 (the pin); three named things that would move it,
+1 h each. Observed: Research 13:00 · build 13:44 · first review 14:12 · two fix-and-verify rounds the estimate did not
have · window 1 not open at 15:15. The estimate lived in a chat message and one ship-log row; the update in another chat
message; nothing in the tracker could be read by a person or a seat as *when am I needed*.

## Why

A person plans a day around windows, not around seats' work. An estimate written before, updated during and closed with
the actual is what makes a plan a prediction the record can check — per seat, per step — and what lets a person decide
what to take in. Without it, the same information is typed into chat twice a day and lost.

## Candidates — to be attacked, none chosen

1. **A `## Plan` section the tool reads:** one table per tracker — step · seat · estimate (a clock time or a duration) ·
   actual · the person's window (`needed: owner ≈ 15:30–16:00 — open + merge, tag`). The board and `--owner` print the
   next window; a seat's report writes the actual. Cost: a parser, two board lines, one label pair. Risk: a plan nobody
   updates becomes a stale promise.
2. **Front matter only:** `plan-next: owner 2026-09-23 15:30–16:00 "open + merge, tag"` — one line the board reads; the
   split stays prose. Cheapest; carries one window, not the split.
3. **Ship-log rows by convention** (`estimate:` / `actual:` prefixes a scorer greps). No code; nothing prints *when you
   are needed*.
4. **Drop it:** the estimate stays in chat and the ship log, as today.

## What would decide it

- How often a plan is updated once it exists (candidate 1's risk): updates per plan over one week, with the
  estimate–actual gap per seat and step. Plans written once and never updated → candidate 2 or 3.
- Whether a person acts on *needed at ≈ hh:mm*: was the window used, or did the person wait in chat anyway.
- The estimate's error per seat over ten arcs — the number that turns *what to take in* into arithmetic.

## Done when

The Owner has ruled which candidate, if any; the chosen one prints *who is needed, when, for what* on the board and in
the digest, from a plan written before the work, updated by each seat's report and closed with the actual; and one full
arc has run on it with its estimate–actual gap in the record.

## Ship log

| Date | Event |
|---|---|
| 2026-09-23 | Filed on the Owner's requirement, tagged `research`, with the instance that raised it as its first evidence. Held against FM-004 (adoption), FM-005 (the person asked mid-flight), FM-006 (a page for the humans). Not built this week — the current path's line 2: tracked, not built. |
