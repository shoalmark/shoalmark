---
id: FM-059
status: In Progress
considered: FM-050, FM-007, FM-054, FM-058
tags: process
next: build
triaged: 2026-10-17
tier: P2
hook: "The Owner answers each ask in a Board view that holds only its dialog; a prepared run stops there, and signs and pushes only the line the Owner chose"
ask: "Which release builds the guided answer view: the Board view that holds only one ask's dialog, opened by a prepared run that signs what you chose?"
ask-kind: ruling
ask-since: 2026-10-16
ask-options: "v0.20.1 | the first release after v0.20.1 | a later release, which I name in my answer"
ask-proposal: "v0.20.1"
answer: "accepted - v0.20.1"
answered: 2026-10-16
answered-by: holgo99
---

# FM-059 — the Owner answers each ask in a view of its own, and a prepared run signs only what they chose

## What is true now

**2026-10-17 — S2 built, awaiting independent critical review:** `3baabe1` records the hooks' copy's source commit and canonical file comparison; its reader retains older short records as incomplete and names `--install-hook` without refusing them. The scoped checks and four mutants pass on Python 3.15 and 3.9.6, with the CRLF stand-in on 3.15. Requirements recorded privately.

**2026-10-17 — judged In Progress, P2, for v0.20.1's build (quick win 11), before the first build commit.** Its first
slice, the hooks' copy recording the tool's full commit, is built on `fm/059-copy-provenance`.

**Filed 2026-10-16 on the Owner's direction, with its ask. Its design started the same day, the Owner with the Designer;
nothing is built.** On the Owner's word of the same day it is quick win 11, in v0.20.1: the ask's first proposal, the
first release after v0.20.1, is withdrawn (its record is under `## Asks`), and the ask is filed again proposing v0.20.1.

- **What the Owner asks for:** a prepared run (today a run sheet) brings each branch that carries an ask, then stops at
  the answer and opens a Board view holding only that ask's dialog, with help text on what the answer signs and what
  follows it. The Owner reads it and chooses an option, or rejects. Only then does the run sign exactly the line they
  chose, push it, and go on to the next ask.
- **Until it ships:** a run sheet prepares and stops before any answer, and the Owner answers from the Board.
- **Two requirements for its design, recorded privately.** They go into its design brief.
- **The ask** asks only which release builds it; proposed, v0.20.1, on the Owner's word.
- **What it needs first:** R4's ask ids (FM-050), and FM-058's fix, so that a command a person runs has no time bound;
  FM-058 moves into v0.20.1 with it. The seat's confidence, *because* and *then* are new record data and stay outside it:
  without them the view shows the proposal and the options alone.

## Done when

- Its design is reviewed, and the Owner's signed answer here names the release that builds it.
- Built in that release, and reviewed.

## Asks

**2026-10-16** · Which release builds the dedicated answer view: the Board view that holds only one ask's dialog, opened by a prepared run that signs what you chose?
**withdrawn** — no answer was given

## Ship log

| Date | Event |
|---|---|
| 2026-10-17 | Judged In Progress, P2, by the Planner for quick win 11's build, before the first build commit, on `fm/059-copy-provenance`. |
| 2026-10-16 | Filed on the Owner's direction (relayed by the Auditor), with its ask. Nothing is designed or built. |
| 2026-10-16 | Its design started, the Owner with the Designer; the ask now asks only which release builds it. |
| 2026-10-16 | Quick win 11 in v0.20.1, on the Owner's word: the first proposal withdrawn, the ask filed again proposing v0.20.1. |
| 2026-10-17 | S2 built in `3baabe1` by the Builder seat: source provenance for the hooks' COPY, its reader and legacy notice, with the scoped checks and four mutants on Python 3.15 and 3.9.6 and the CRLF stand-in on 3.15. An independent critical review remains. |
