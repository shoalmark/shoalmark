---
id: FM-095
status: Proposed
considered: FM-062, FM-088, FM-089
tags: seamanship
hook: "A rule the Owner gives in chat lives in dated messages, in each seat's memory and in brief templates, and nowhere in this repository. One register would hold every ruling with the commit that signed it, what enforces it and what proves it, changed only by the Owner's signed answer."
---

# FM-095 — the Owner's rulings live in chat, memories and briefs, not in one register that names what enforces each

## What is true now

**Filed 2026-10-29 for v0.20.x; nothing is built.** On the Owner's word of 29 October, "file those", for agentic
seamanship. It is considered for every v0.20 release and pulled into one when it fits: "we consider all, but we only
pull in what fits". [FM-089](FM-089-agentic-seamanship-v0-20-3.md), v0.20.3's chapter, names it as a candidate, not a
part.

- **Where a rule said in chat lives today:** in dated messages kept outside this repository, in each seat's memory and
  brief templates on one machine, and nowhere in this repository. A new session, or one on another harness, reads none
  of it unless someone pastes it.
- **The pattern this repository already has:** R1 to R28 are the Owner's signed answers of 12 October (2d62fa1).
  - Their record is [rulings-2026-10-12.md](evidence/rulings-2026-10-12.md).
  - `AGENTS.md`'s "How the loop runs" states the loop's signed answers in force, and names R15, which removed the filing
    freeze.
  - A class test holds each one that is mechanical, as `test_r9_removals.py` holds R9.
  - `AGENTS.md` also says that a word in chat changes none of them until the Owner signs it. So a rule given in chat
    is not a ruling yet.
- **One register, with one way in and one way out:**
  - A seat proposes a rule, often from a lesson in its memory, which is
    [FM-088](FM-088-the-team-s-lessons-live-only-in-each-harness-s-local-memory.md)'s way out of a harness's memory. The
    register lists it as proposed.
  - The Owner signs it on the Board as an answer, as every ruling is signed, and it takes the next R number.
  - Retiring a ruling is a signed answer too. Git's history is the trail.
- **Each entry holds** its id, its words, the seats it binds, the signed answer's commit, and the strongest enforcement
  that fits:
  1. a check: the gate's `--check` or CI refuses the breach;
  2. one shared tool: a command every seat runs, instead of each writing its own;
  3. generated words: briefs and prompts take the rule's text from the register, so no copy drifts;
  4. words only, marked as such, where nothing above fits.
  - Each entry names its proof as well: the class test for 1 and 2, and an eval scenario of
    [FM-096](FM-096-nothing-measures-whether-a-session-follows-the-rules-and.md) for 3 and 4.
- **Where it lives:** in the tracker folder, beside FM-088's `memory/team.md`, changed only by the Owner's signed
  commit. `AGENTS.md`'s section on the loop becomes a view of the register, so the two cannot disagree.
- **The first design question:** whether the register and `team.md` are one file. A ruling binds and a lesson informs,
  and a lesson the Owner signs becomes a ruling.
- **Seven proposals from the work of 29 October,** each proposed until the Owner signs or drops it:
  1. Every local suite run goes through one shared runner with a fixed number of slots. A full run also takes the
     lock.
  2. CI's suites are a lane's full run. Local full runs happen only where a branch may not reach GitHub, and at the
     release head.
  3. A run is never paused: a stopped process tree breaks every timed check in it.
  4. A guard looks only at processes its own run started.
  5. A verdict commit never goes onto a pull request's branch. It rides with the next records branch.
  6. A pull request whose base is not the default branch opens as a draft, titled "[signed merge only] …".
  7. A rule every session must follow comes as one tested tool, never as words alone.
- **The order:** this tracker builds first, since
  [FM-096](FM-096-nothing-measures-whether-a-session-follows-the-rules-and.md) and
  [FM-097](FM-097-find-drift-does-not-audit-the-owner-s-rulings-whether-each.md) both read the register.

## Why

A rule given in chat binds only the sessions that heard it, and only for as long as their memory holds it.
[FM-062](FM-062-an-agent-drifts-off-track-where-a-rule-is-held-only-as-prose.md) found the same drift where a rule is
held only as prose. A register that names each ruling's enforcement and proof makes the rulings auditable, and shows
which ones only words hold.

## Done when

- [ ] The register exists, with R1 to R28 and the commit of each signed answer.
- [ ] `--check` refuses a change to the register that is not the Owner's signed commit.
- [ ] Every ruling names its enforcement and its proof.
- [ ] The seven proposals of 29 October are listed as proposed, until the Owner signs or drops each.

## Ship log

| Date | Event |
|---|---|
| 2026-10-29 | The pattern and the Done when name R1 to R28, as the record of 12 October holds them (RV-4056). Records only. |
| 2026-10-29 | Filed for v0.20.x, on the Owner's word of 29 October. Records only. |
