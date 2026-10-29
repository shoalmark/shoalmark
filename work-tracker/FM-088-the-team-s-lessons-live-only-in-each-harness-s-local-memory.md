---
id: FM-088
status: Proposed
considered: FM-086, FM-062, FM-083, FM-030, FM-037, FM-078
tags: process, seamanship
next: build
ask: "In which release does shared memory land, as FM-088's What is true now sets out: the team's and each seat's memory in the repository, the four ways a lesson leaves harness memory, review by scope, the evals and staleness?"
ask-kind: ruling
ask-since: 2026-10-29
ask-options: "v0.20.3 | v0.20.4, after FM-086's signals | later, when I name it"
ask-proposal: "v0.20.4, after FM-086's signals"
answer: "accepted - v0.20.3"
answered: 2026-10-29
answered-by: holgo99
hook: "What the team learns lives only in each harness's local memory, on one machine. Another seat, another harness and every new user of the product start without it, and nothing moves a lesson from a session's scratchpad into the record where every seat can read it."
---

# FM-088 — the team's lessons live only in each harness's local memory, so another seat, another harness and every user start without them

## What is true now

**Filed 2026-10-29; nothing is built.** On the Owner's word of 29 October, as the Auditor relays it: shoalmark gets
shared memory, one file for every seat's own role and one that applies to all roles. Its release is the Owner's, and
the ask above puts it to them.

**The gap:**
- **Where lessons live:** a seat's lessons sit in its harness's local memory folder, on one machine.
- **Who misses them:** a Codex seat reads nothing a Claude seat learned, and the reverse. A new user of the product
  gets none of it.
- **What the record already holds:**
  - **episodes:** git, ship logs, verdicts and hand-backs;
  - **procedure:** the contract, the checks, the skills and the Board's prompts;
  - **intentions:** asks, `due:`, `next:` and the stand-up.
- **What it lacks:** the facts and lessons that hold beyond one episode, kept where every seat and every harness can
  read them.

### The design

1. **Where it lives: the repository.**
   - `<tracker dir>/memory/team.md` holds what applies to every role.
   - `<tracker dir>/memory/<seat>.md` holds each seat's own.
   - **Why the same repository:** memory changes in the same commit as the code and rules it describes. It is reviewed
     in the same pull request, read at the same commit a session checks out, and guarded by the same gate. A separate
     repository would let a branch read memory that does not match its code.
   - **Private material:** a lesson that holds it goes to a private overlay, never into a public repository. An adopter
     whose repository is private needs none.
2. **One entry is one fact or one lesson,** with:
   - **its source:** who, when and the commit. An entry that quotes the Owner cites the commit holding the Owner's
     words, and an agent's inference is marked as one. An agent's word is never counted as the Owner's.
   - **`promote:`,** its target on the ladder: check · template · contract · skill · docs · project · local.
   - **its state:**
     - *active*;
     - *encoded*, once a check, a rule or a skill holds it, when the entry shrinks to a pointer to that commit;
     - *retired*.
   - **what it depends on:** a file, a flag or a seat, so a stale entry can be found.
3. **How a lesson leaves harness memory.** The tool never reads a harness's own folders, and it schedules and sends
   nothing, so the reminder rides on what already runs:
   - **the contract:** `--init` writes one line into `AGENTS.md` and `CLAUDE.md`. Harness memory is a scratchpad. A
     lesson that would help another session goes to its seat's memory, or is proposed for the team's, the same day.
   - **the close-out prompt** asks every day: what did you learn today that lives only in your harness memory? File each
     lesson in your seat's memory, or propose it for the team's.
   - **a Board signal per seat,** *consider a memory sync*, raised when a seat has committed for several days with no
     change to its memory file. It is soft, like every signal of
     [FM-086](FM-086-a-tracker-states-one-deliverable-and-closes-when-it-ships.md).
   - **a `/sync-memory` skill:**
     - the session compares its harness memory with the repository's;
     - it proposes each new entry with its scope and its `promote:` target, private details stripped;
     - a team entry reaches the Owner's stand-up as an ask.
4. **Review by scope:**
   - a seat's memory changes by that seat's commit, with a standard review;
   - team memory binds every seat, so it changes only by the Owner's signed commit, with a critical review, as the
     seat definitions do.
5. **The evals: a change must not regress, in any harness.**
   - **The ladder first.** A lesson made into a check needs no eval of model behaviour: the check's own tests hold it.
     Only prose memory needs evals, so promotion is pushed hard.
   - **Golden episodes:** each prose entry carries the episode that caused it, turned into a scenario: a fixture
     repository and a task that tempts the mistake.
     - Scenarios run with and without the entry, on Claude Code and on Codex.
     - They run at each team-memory change and at each release.
   - **Across harnesses:** an entry that helps one harness and hurts the other is reworded, or moves to that harness's
     own file. Team memory stays harness-neutral.
   - **The lagging signal:** the Owner's corrections, counted per area per week. More corrections in an area after a
     memory change mark a regression, and the entry is reverted.
   - **The cost:** memory loaded at start takes context. The scenarios measure tokens, and each file has a soft size
     signal.
6. **Staleness:** `/find-drift` reads memory files as sources. An entry whose dependency no longer exists raises
   *consider retiring*.
7. **Product and project:**
   - The mechanism ships to every user: the files, the guard on team memory, the signals, the close-out step,
     `--next` loading memory, and `/sync-memory`.
   - This repository's own lessons reach users only by promotion, into the tool's checks, contract, templates and
     skills. Users never get this repository's `team.md`. They get what it learned, built in.

## Why

A team that cannot read what it learned repeats it. Lessons kept in the repository, with their source and their target
on the ladder, are read by every seat on every harness. They are checked like the rest of the record, and they leave as
soon as a check holds them.

## Done when

- [ ] `--init` writes `<tracker dir>/memory/team.md` and the contract's line on where memory belongs, in `AGENTS.md`
  and `CLAUDE.md`.
- [ ] `--schema` names an entry's source, `promote:`, state and dependencies. `--check` refuses an entry that quotes
  the Owner but cites no commit of the Owner's.
- [ ] `--check` refuses a change to `memory/team.md` that is not the Owner's signed commit. A seat's memory changes
  only by that seat's commit.
- [ ] `--next` loads the session's seat memory and the team's, and names both.
- [ ] The close-out prompt carries the memory step, and its class test pins it.
- [ ] The Board raises *consider a memory sync* per seat, with its default key, and never refuses.
- [ ] `/sync-memory` proposes entries with their scope and target, with private details stripped, and has its own
  eval.
- [ ] Each prose entry in `team.md` has its scenario. The suite runs with and without each entry on Claude Code and on
  Codex, and reports the result and the tokens.
- [ ] `/find-drift` reads the memory files and raises *consider retiring* for an entry whose dependency is gone.
- [ ] Every seat of this repository has classified its harness memories as product, project or local, and each product
  lesson names its target on the ladder.

## Ship log

| Date | Event |
|---|---|
| 2026-10-29 | Filed, on the Owner's word of 29 October, with the ask on its release. Records only. |
