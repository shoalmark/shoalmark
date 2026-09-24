---
id: FM-026
status: Parked
considered: FM-004, FM-006
tags: research
kind-of-problem: complex
next: review
triaged: 2026-09-24
tier: P3
hook: "Three outside agent fleets asked cold said no, and all three named the same reason — two sources of truth — because nothing tells an existing fleet how its trackers, seats and habits move over; the adopt note must carry that migration, and the case its agents make to their owner"
---

# FM-026 — an existing fleet has no migration path — the adopt note must carry it, and the case its agents make to their owner

Seat: Principal · filed 2026-09-23 on the Owner's direction, quoted *(spelling and wording normalised at his request; the
meaning unchanged)*: *"The missing migration part of any existing fleet has to be tracked, and this one has to land within
the gist prompt that instructs agents how to do it and how they can convince their owners of this change."* Written to be
attacked.

## What is true now

**Filed 2026-09-23; nothing is built.** FM-004's run on 2026-09-21: 0 of 3 outside fleets recommended adopting, and
all three named *two sources of truth* — their tracker and this one. The note their agents were handed,
[`ADOPT.de.md`](../ADOPT.de.md) (73 lines), says what the tool is, when not to use it, a twenty-minute measurement
in a throwaway folder, a report to the owner, and *if the owner says yes* — and **not one line about the fleet's
existing trackers, issues, boards, seats or habits: where they go, what stays, who does the move, or what the owner
loses and keeps.** A fleet mid-way through a plan (FM-004's case: sixty packages) is asked to start a second record
beside its first. The human site (FM-006) has the same gap on the owner's side.

Meanwhile the tool grew what a migration would move into: `[seats]` and sessions (FM-024), a signed answer per ask,
a triage pass with the owner's intent and path, a board, a manifest per pin (FM-011). None of it is reachable from an
existing record without a person or an agent doing the transcription by hand.

## Why

An owner adopts a tool his agents can install *and* migrate to in one sitting, without losing his record; the agents
recommend a tool they can present to him as a gain they measured, not a second bookkeeping. Both are missing, and
the measurement says they are the reason for *no*.

## Candidates — to be attacked, none chosen

1. **`--migrate <source>` run by the fleet's own agents, once:** reads what exists — a folder of Markdown notes, a
   `TODO.md`, an issue export (JSON), a `CHANGELOG` — and writes one tracker per item with the front matter the gate
   needs (`id`, `status`, `hook`, `considered: none`, the original path or issue number kept in the body), a first
   `TRIAGE.md` with the owner's lines empty, `[seats]` from the committers it finds, and a report of what it could not
   place. The fleet's old record stays read-only beside it for one release; the board links back. Cost: the readers
   (three formats), the writer, a dry run that changes nothing; ≈ 300 lines and a suite.
2. **The adopt note carries the migration and the pitch, no tool change:** `ADOPT.de.md` (and an English twin) gains
   two sections — *how we move what exists* (the steps the agents take, by hand, with the measurement's throwaway
   folder as the rehearsal) and *what we tell the owner* (the gain measured in his own numbers: asks answered, minutes
   at the sitting, pull requests reviewed before opening; what he signs once; what he never loses). Cost: two pages.
3. **Both, in that order:** the note first (it is what the three agents read), the command when a second fleet asks.
4. **Drop it:** adoption starts at the next project, not mid-flight.

## What would decide it

- FM-004's three prompts rerun with the migration and the pitch in the note: 0 of 3 says the pitch is not the problem;
  2 or 3 of 3 says it was.
- One real fleet's record migrated by its own agents in a throwaway copy: items placed / items left, and the owner's
  read of the result — kept, lost, wrong.
- The owner's question after reading: if it is *what happens to my existing X*, the note still fails.

## Done when

The Owner has ruled the candidate; an outside fleet's agents can migrate what exists in one sitting from the note (or
the command) without a person transcribing, and present the change to their owner in his numbers; FM-004's three
prompts rerun give at least 2 of 3.

## Ship log

| Date | Event |
|---|---|
| 2026-09-23 | Filed on the Owner's direction, tagged `research`; held against FM-004 (the 0 of 3 and its reason) and FM-006 (the owner's page); FM-025 (the cold start's cost), on its own branch, is its neighbour. Not built this week — the path's line 2. |
