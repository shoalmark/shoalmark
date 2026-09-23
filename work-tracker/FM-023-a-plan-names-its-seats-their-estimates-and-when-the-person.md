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

## Examples — how candidate 1 would look, on the Owner's ask (illustrative, nothing is built)

One front-matter line the tool reads and prints on the board and in `--owner` (*needed: owner ≈ 15:30–16:00 — …*), and one
`## Plan` table in the body that people and seats edit. Estimates are never overwritten: a re-estimate is appended in the
same cell with its time, so the record keeps both. Times are clock times of the day the plan is written; a plan that
spans days carries dates.

### a. The estimate, as filed before the work (12:55)

```markdown
---
id: FM-0xx
status: In Progress
next: build
needed: "owner 15:30–16:00 — open + merge the release PR, tag v0.17.5; then 16:30–17:00 — open + merge the pin PR"
---

## Plan

*Estimated 12:55 by the Principal seat. Moves it: a P1 from the Reviewer (+1 h) · the search fix being template
surgery rather than a filter (+1 h) · the triage pass finding more than the two issues worth fixing today (the rest is
filed, not built).*

| # | Step | Seat | Estimate | Actual | Note |
|---|---|---|---|---|---|
| 1 | Research: the triage state, the two board issues | research | ≈ 13:05 | | |
| 2 | Filings for the two issues; the first triage pass | principal | ≈ 13:30 | | |
| 3 | Build the release on a branch | implementer | ≈ 14:30 | | |
| 4 | Review, one fix round, verification of the final tree | reviewer · implementer | ≈ 15:30 | | |
| W1 | **Open + merge the release PR, tag** | **owner** | **15:30–16:00** | | |
| 5 | Vendor the tag into the consumer as its own pin PR; review | implementer · reviewer | ≈ 16:30 | | |
| W2 | **Open + merge the pin PR** | **owner** | **16:30–17:00** | | before 07:30 |
```

### b. An update while it runs (14:38) — the cells that change, and the one line the board reads

```diff
-needed: "owner 15:30–16:00 — open + merge the release PR, tag v0.17.5; then 16:30–17:00 — open + merge the pin PR"
+needed: "owner 15:40–16:00 — open + merge the release PR, tag v0.17.5; then 16:40–17:10 — open + merge the pin PR"

-*Estimated 12:55 by the Principal seat. Moves it: …*
+*Estimated 12:55 by the Principal seat · updated 14:38 (two fix-and-verify rounds the estimate did not have). Moves it: …*

-| 1 | Research: the triage state, the two board issues | research | ≈ 13:05 | | |
+| 1 | Research: the triage state, the two board issues | research | ≈ 13:05 | 13:00 | |
-| 2 | Filings for the two issues; the first triage pass | principal | ≈ 13:30 | | |
+| 2 | Filings for the two issues; the first triage pass | principal | ≈ 13:30 | 13:33 filings · pass deferred | the pass waits for the release — the Owner's word, 14:40 |
-| 3 | Build the release on a branch | implementer | ≈ 14:30 | | |
+| 3 | Build the release on a branch | implementer | ≈ 14:30 | 13:44 | one more tracker taken in mid-flight (the Owner's finding) |
-| 4 | Review, one fix round, verification of the final tree | reviewer · implementer | ≈ 15:30 | | |
+| 4 | Review, one fix round, verification of the final tree | reviewer · implementer | ≈ 15:30 → ≈ 15:40 (14:38) | 14:12 pass · 14:36 fixes · 15:10 NOT READY, one P2 | a second round; the estimate had one |
-| W1 | **Open + merge the release PR, tag** | **owner** | **15:30–16:00** | | |
+| W1 | **Open + merge the release PR, tag** | **owner** | **15:30–16:00 → 15:40–16:00 (14:38)** | | |
```

*Who writes an update:* the seat whose step moved, in its own report commit — the actual into its row, a re-estimate only
by the seat that owns the plan (here the Principal), the `needed:` line whenever a window moves. The board shows the
newest `needed:` and, beside it, how many times it moved.

### c. The record of a finished tracker (closed the same evening)

```markdown
---
id: FM-0xx
status: Shipped
needed: none
plan-closed: 2026-09-23 17:05
---

## Plan

*Estimated 12:55 by the Principal seat · updated 14:38, 15:12 · closed 17:05. Seat time: estimated 3–4 h, actual 4 h 10.
Owner time: estimated 2 windows × 30 min, actual 2 × 6 min at the keyboard (buttons), 55 min of chat around them.
Largest miss: step 4, +1 h 10 — two rounds where one was estimated; the cause is in FM-0yy's ship log.*

| # | Step | Seat | Estimate | Actual | Note |
|---|---|---|---|---|---|
| 1 | Research: the triage state, the two board issues | research | ≈ 13:05 | 13:00 | −5 min |
| 2 | Filings for the two issues; the first triage pass | principal | ≈ 13:30 | 13:33 filings · pass deferred | moved to its own tracker |
| 3 | Build the release on a branch | implementer | ≈ 14:30 | 13:44 | −46 min; one tracker added mid-flight |
| 4 | Review, one fix round, verification of the final tree | reviewer · implementer | ≈ 15:30 → ≈ 15:40 (14:38) | 15:52 READY TO TAG | +22 min on the re-estimate; two rounds |
| W1 | **Open + merge the release PR, tag** | **owner** | **15:30–16:00 → 15:40–16:00 (14:38)** | 15:58–16:04 | 6 min at the keyboard |
| 5 | Vendor the tag into the consumer as its own pin PR; review | implementer · reviewer | ≈ 16:30 | 16:41 | +11 min |
| W2 | **Open + merge the pin PR** | **owner** | **16:30–17:00 → 16:40–17:10 (14:38)** | 16:58–17:04 | before 07:30 ✓ |
```

*What the closed record gives the next plan:* per seat, the estimate error over this arc (research −5 · implementer −46,
+11 · reviewer + implementer +22 on a re-estimate · owner 6 min per window against 30 estimated). Ten such arcs and
*what to take in* is arithmetic; the board's *needed* line can then carry a margin the record earned.

### d. An extract for a multi-session tracker — two sessions of one seat, one Owner

```markdown
---
id: FM-0xx
status: In Progress
needed: "owner 15:40–16:00 — tag (session A) · his own slot — the hands sitting, ~15 min (session B) · 16:40–17:10 — the pin PR (session A)"
---

## Plan

*Two Principal sessions run today by the Owner's design — A on the day's findings and the tool, B on the product items.
Each session owns its rows and writes only those; the `needed:` line merges every session's windows in clock order,
and ONE session reports to the Owner per topic (session A for this tracker). A row's seat names its session.*

| # | Step | Seat · session | Estimate | Actual | Note |
|---|---|---|---|---|---|
| A1 | Build, review, tag the release | implementer · reviewer · **A** | ≈ 15:40 | 15:52 ready | |
| W1 | **Tag the release** | **owner** (A reports) | **15:40–16:00** | | |
| B1 | The negative-control build, its review, the pre-registration | implementer · reviewer · **B** | ≈ 16:00 | 12:22 pushed | early; waits on B2 |
| B2 | The run sheet for the Owner's hands — four reads, one command each | principal **B** | ≈ 12:30 | 12:12 pushed | |
| WB | **The hands sitting — its own slot, outside the standup budget** | **owner** (B reports) | **his slot, ~15 min** | | not a standup item |
| A2 | Vendor the tag into the consumer; review | implementer · reviewer · **A** | ≈ 16:40 | | |
| W2 | **Open + merge the pin PR** | **owner** (A reports) | **16:40–17:10** | | before 07:30 |
```

*The rule the extract carries:* windows are the Owner's, in one line, in clock order, whoever's session they came from;
a session never edits another session's row; a collision (two sessions, one row) is a finding, not an update.

## Done when

The Owner has ruled which candidate, if any; the chosen one prints *who is needed, when, for what* on the board and in
the digest, from a plan written before the work, updated by each seat's report and closed with the actual; and one full
arc has run on it with its estimate–actual gap in the record.

## Ship log

| Date | Event |
|---|---|
| 2026-09-23 | **Four worked examples added on the Owner's ask** — the estimate as filed, an update while it runs, the finished record, a multi-session extract — all illustrative of candidate 1, nothing built. |
| 2026-09-23 | Filed on the Owner's requirement, tagged `research`, with the instance that raised it as its first evidence. Held against FM-004 (adoption), FM-005 (the person asked mid-flight), FM-006 (a page for the humans). Not built this week — the current path's line 2: tracked, not built. |
