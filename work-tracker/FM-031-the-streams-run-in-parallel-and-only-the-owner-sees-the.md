---
id: FM-031
status: Proposed
considered: FM-005, FM-023, FM-024, FM-027
tags: process
hook: "In fourteen hours 21 seat sessions opened 22 pull requests, and only the Owner sees the whole queue. At 08:10 six were open: one sat inside another, one had been copied into another, two conflicted on the file every session writes. He asked which to merge five times."
---

# FM-031 — the streams run in parallel and only the Owner sees the whole queue

## What is true now

**Filed 2026-09-24 08:24 CEST on the Owner's question. Nothing is built.**

The measurements below are read from the record: git, the forge, and `work-tracker/sessions.md` on every remote
branch. They cover 2026-09-23 18:00 to 2026-09-24 08:20 CEST.

- **21 sessions began:** 9 GtM, 8 Implementer, 2 Principal and 2 Reviewer, across 6 worktrees.
- **22 pull requests were opened.** 13 were merged, and 6 were open at 08:10.
- **Of the six open ones, at most one could be merged as it stood:**
  - #33 was ready: a Reviewer's verdict names its head, and it merges cleanly.
  - #37's head is an ancestor of #33's head, so #37 is contained in #33.
  - #38's two rows had been carried verbatim into #33. Merging both would write them twice.
  - #35 conflicted in `sessions.md`.
  - #34 and #36 had no verdict on their head.
- **The conflicts were on the shared files.**
  - Every parallel pull request appends its session's row to `work-tracker/sessions.md`, all at the same place. That
    conflicted on #33, #35 and #37.
  - In the origin, two pull requests conflicted on the same file, and on a tracker's ship log as well.
- **The Owner asked one Implementer session five integration questions in about two hours:**
  - which pull requests to merge;
  - that one of them had a conflict;
  - to run the Reviewer;
  - the list of what was open;
  - this question.

  A seat answered each one by reading the forge and `git merge-tree` by hand.
- **Rulings reached the seats by three routes:**
  - relayed by the coordinating Principal;
  - typed by the Owner into a seat's own session;
  - pasted from another seat's chat.
- **The Owner's own checkout had a seat's branch checked out.** Git refused that branch to the seats twice, and they
  worked on a detached head instead.

**Filing outruns closing about two to one.** The Owner asked it on 2026-09-24 (spelling normalised): *"How much faster
are we filing than we are being able to close?"* The measurement is read from `main`'s history: each tracker's first
commit, and the first commit where its status reads *Shipped* or *Closed*.

- **The record starts 2026-09-22 11:09, 1.9 days ago.**

  | Day | Filed | Closed | Open at the day's end |
  |---|---|---|---|
  | 2026-09-22 | 11 | 2 | 9 |
  | 2026-09-23 | 16 | 13 | 12 |

- **Four more are filed on branches but not yet on `main`:** FM-028, FM-029, FM-030 and FM-031. That makes 31 filed
  against 15 closed, and 16 open.
- **Rate:** 16.4 filed a day against 8.0 closed, a ratio of 2.07. The open count grows by about 8 a day.
- **Filing to closing takes 0 to 26 hours** for the 15 that closed. Most take 3 to 8 hours.
- **The pull requests show the same shape,** from 2026-09-23 18:00 to 2026-09-24 08:20: 22 opened, 13 merged.

**What coordinates today:**
- Every commit names its session (FM-024).
- The registry says who is running where.
- Every slice is reviewed before it is called ready.

**What does not:**
- **Nothing orders the streams.** Branches stack on each other without saying so.
- **A carry-over leaves its source pull request open.**
- **The registry is the file every stream conflicts on.**
- **Only the Owner holds the whole queue,** so he is the integrator by default.

## Why

The Owner, 2026-09-24, in chat (spelling normalised): *"Can a human keep up with this? How could we improve here? These
are multiple streams running at the same time doing valuable work — but are they all coordinated?"*

## Candidates, cheapest first

None is chosen. The Owner or the Principal rules.

1. **The queue in one view.** The tool reads the open pull requests and gives each one action:
   - *merge*: a verdict names its head, and it merges cleanly;
   - *closes with #N*: its head is inside another open pull request;
   - *close*: it was carried into #N;
   - *wait: conflict in …*;
   - *wait: no verdict on …*;
   - *wait: NOT READY*.

   A seat built exactly this by hand tonight in about two minutes, and the Owner needed it five times. It could be its
   own command or a section of `--standup`.
2. **The registry stops being the conflict.** Either:
   - one file per session, with the table generated; or
   - a merge rule for the table. The catch: closing a session edits its row in place, so a plain union merge would
     keep both the open and the closed version of that row.
3. **Stacked work says so.**
   - A slice built on another slice opens its pull request against that branch, not `main`. The forge then shows only
     the delta, and there is no twin.
   - A carry-over closes its source pull request in the same step.
4. **A limit on work in flight.** No seat starts a new stream while N pull requests wait on the Owner. Tonight's peak
   was 6.
5. **One channel for the Owner.** He speaks to the coordinating session. His rulings are recorded once, where the seats
   read them (the tool's ask and answer), not relayed through chat.
6. **Seats never need the Owner's checkout.** The command that lets him see a branch is `git fetch && git switch
   --detach origin/<branch>`, so his checkout never holds a seat's branch.

## Done when

- The Owner can answer *what do I merge, in what order, and what waits on whom* from one command's output, in under a
  minute, without asking a seat.
- A week of parallel streams shows no conflict on the registry, and no pull request left open as a twin.

## Ship log

| Date | Event |
|---|---|
| 2026-09-24 08:26 CEST | The Owner's second question measured: filing outruns closing 2.07 to 1 (16.4 filed a day against 8.0 closed, since 2026-09-22 11:09); 16 open, and the open count grows about 8 a day. |
| 2026-09-24 08:24 CEST | Filed on the Owner's question, with tonight's record as the measurement. Held against FM-005 (his decisions: the asks, not the queue of pull requests), FM-023 (a plan's seats and estimates), FM-024 (a commit names its session) and FM-027 (ids claimed on the server). |
