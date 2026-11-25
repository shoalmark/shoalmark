---
id: FM-187
status: In Progress
considered: FM-033, FM-161, FM-175
tags: process
next: build
triaged: 2026-11-25
tier: P1
hook: "A project whose shoalmark.toml sits below the top of its git repository is not judged: the gate reads each tracker at a revision by a path git takes from the top, finds nothing, and passes. And a tracker shipped before the trackers move out of a code repository fails for commits left behind. FM-187-Q1 accepted the small change: refuse to run below the top until FM-161's fix, and freeze the trackers the Owner's signed import adds already Shipped. It is to be built at once."
---

# FM-187 — the gate passes a project below the git top unjudged, and a tracker shipped before a move fails for a commit left behind

Seat: the Planner (27f31560), the tool team's lead · filed 2026-11-25, on the coordinator's word of that day.

## What is true now

**2026-11-25 — FM-187-Q1 answered "yes, as proposed", with the Owner's signature; judged before its first build
commit, P1, In Progress,** on the coordinator's word of that day. Decisions 1 to 6 stand as put. The lane is to be built
from main, from a patch prepared before the answer; nothing is built yet. Its review is critical, by a reviewer session
independent of the builder. Which release takes it is not decided: [FM-188](FM-188-rulings-collide-unseen-an-ask-is-put-and-answered-without.md)-Q1 puts it.

**2026-11-25 — filed, Proposed, with FM-187-Q1 put; nothing is built.** The organisation is moving the teams' trackers
out of the code repositories into its own repository, with each team a project in a folder of its own and its own
`shoalmark.toml`. Two things stop the tool from serving that move today.

- **A project below the git top is not judged.**
  - The tool reads a tracker at a revision as `<rev>:<path>`, with the path written from the project's root. Git reads
    that path from the top of the repository, so below the top it finds nothing.
  - So the rights rule, the Shipped rule and every rule that compares a tracker before and after a commit judge
    nothing there, and pass. A scratch repository shows it: from a folder below the top, `HEAD:work-tracker/FM-001.md`
    is missing and `HEAD:./work-tracker/FM-001.md` is found.
  - In a rehearsal of the move, a commit by no seat that set a tracker to Shipped in such a project passed. The same
    commit is refused at the top.
  - [FM-161](FM-161-a-team-can-only-be-one-whole-repository-so-a-team-in-a.md) holds the fix (FM-161-Q2). Until it
    lands, the tool must refuse such a run rather than pass it.
- **The trackers shipped before the move would fail.**
  - A tracker that the import adds already Shipped is read as a move to Shipped. It must name a commit in the history
    behind it, and its commits stay in the code repository.
  - The count is 48 of this team's trackers: 39 name commits that are only in the code repository, and 9 name none.
  - [FM-175](FM-175-trackers-are-prose-the-gate-cannot-read-so-each-becomes-a.md)'s decision 8 converts a closed tracker
    frozen. This change brings that rule forward for the move.

## Why

The tool's first promise is never a false pass. A project it cannot judge is refused, not passed, until it can judge
it. A move that only changes where trackers live must not turn trackers judged Shipped, where their commits are, into
refusals. This change leaves [FM-033](FM-033-work-is-built-on-trackers-no-pass-has-judged-and-the-board.md)'s gate,
which needs a judged tracker before a build commit, as it is. FM-161's decision 12 turns that rule off in a code
repository whose trackers live elsewhere, until the pinned read.

## Decisions, for the Owner

All six are put as FM-187-Q1.

1. **Refuse below the top.** In a git repository, a run whose project root (the nearest `shoalmark.toml`) is not the
   top of the repository is refused, with one line naming FM-161. Only `--version` and `--help` still run. The hooks
   run from the top and are not affected. Without git, nothing changes.
2. **Frozen when imported Shipped.**
   - A tracker that the import commit adds with `status: Shipped` is frozen. The Shipped rule finds no move for it, at
     that commit or later, and its done items and ship log are not judged again.
   - A later edit is judged as any change to a Shipped tracker is. A status that leaves Shipped unfreezes it for good.
3. **The import is your own signed commit.**
   - It carries the trailer `Tracker-import: <repository> <commit>`, naming the code repository and the commit its
     trackers come from, and it is verified as an answer is.
   - A seat's commit carrying the trailer freezes nothing. No other identity can hold the freeze unless you sign a rule
     that lets it.
4. **Visible, never silent.** `--check` says in one line how many trackers are frozen. The README states the rule where
   it states the Shipped rule.
5. **Tests, each with its mutant:**
   - your signed import with 48 Shipped trackers passes;
   - the same commit unsigned, or by a seat, is refused for each tracker;
   - a later move to Shipped of a tracker that is not frozen is judged as today;
   - a frozen tracker reopened and shipped again is judged;
   - a run from a project below the top is refused, and a run at the top is not.
6. **The lane:**
   - It is built at once from main. Its review is critical, since it changes `shoalmark.py`, by a reviewer session
     independent of the builder.
   - It ships where your answer on the release puts it.

## Done when

Each item names its commit or pull request when it lands.

- [x] **The Owner has answered FM-187-Q1.** · `198dd6b`, #330 (`c069017`)
- [ ] **A run below the git top is refused,** with its tests.
- [ ] **The frozen rule,** held by the Owner's signed import, with its tests and its line in `--check`.
- [ ] **The README states the frozen rule,** as decision 4 says.
- [ ] **The organisation's acceptance checks for the move** run against the build, each reported with its output, on
  the coordinator's word of 25 November.
- [ ] **The critical review is READY.**

## Asks

**FM-187-Q1** · 2026-11-25 · Do you take FM-187's small change as proposed, or as changed under other: the tool refuses to run where the project root is not the git top until FM-161's fix, and a tracker your signed import adds already Shipped is frozen and not checked again, held by its Tracker-import: trailer?
**answered** — accepted - yes, as proposed · holgo99
**relation** — accepted the proposal
**signed** — 198dd6b · G

## Ship log

| Date | Event |
|---|---|
| 2026-11-25 | The records reviews' findings fixed forward: the hook and dated line say the lane is still to be built, the release is FM-188-Q1's, FM-033's gate is left as it is, and two Done when items match decision 4 and their source. Records only. |
| 2026-11-25 | FM-187-Q1 answered, yes, as proposed; judged before its first build commit, P1, In Progress. Records only. |
| 2026-11-25 | Filed, Proposed, with FM-187-Q1 put: refuse a project below the git top until FM-161's fix, and freeze the trackers shipped before the move, held by the Owner's signed import. Records only. |
