---
id: FM-062
status: Proposed
considered: FM-042, FM-037, FM-026, FM-023
tags: process
next: wait
hook: "an agent drifts off track where a rule is held only as prose, two sources disagree, or obsolete text still reads as live"
---

# FM-062 — an agent drifts off track where a rule is held only as prose, two sources disagree, or obsolete text still reads as live

## What is true now

**2026-10-27 — `/find-drift`'s next round: decisions, the record against git, and stranded work, each finding with its
evidence chain.** This comes from v0.20.1's debrief and a user's question, as relayed by the Auditor. It is briefed after
the v0.20.2 lane is pushed, and the lane as it stands is unchanged. A user asked: "Will /find-drift link each stale
assumption to the commit that invalidated it, so reviewers can check the evidence?" The debrief shows why it must. Its
drift sat between a decision, its record and the repository's state, where the skill does not look yet.
1. **Decisions are sources.** Step 2 adds the trackers' asks, answered and open, and their allocation rows. A signed
   answer or allocation that names a tagged release, for work that release does not hold and that no dated entry moves,
   is obsolete text still read as live (step 7). Instance: FM-059's answer *accepted - v0.20.1*, with v0.20.1 tagged.
2. **The record against git.** Step 6 also compares the record with tags, merges and CHANGELOG sections. Instance: five
   quick wins allocated to v0.20.1 reached its tag neither shipped nor moved.
3. **Stranded work, a fourth kind:** a READY verdict, or an ask in a tracker's front matter, on a branch the default
   branch never received. It is read from local refs, with no network. Instance: the records pass of 21 October,
   READY, with two asks the Board never showed.
4. **Every finding carries its evidence chain,** so a reviewer can check it with `git show`:
   - the commit that wrote the stale text, and the commit that invalidated it (a later ruling, code change, merge or
     tag), each by full sha, with the query that found it;
   - a link found by search is a candidate until a reviewer confirms it, as in step 8;
   - where no commit records the invalidation, the report says so, and that is the finding. Instance: the move of 22
     October lives in no commit of the repository;
   - stranded work names its branch and sha, marked as not on the default branch.
5. **Its own claims:** every claim of state ("no release", "never reached") cites the file, line or commit it read. An
   agent's notes and summaries are sources that drift. Where the person names their private folder, the supplement
   compares them with the record.
6. **When:** a scoped run before every release sitting, on the allocation and the release's trackers. Its report,
   committed with its hash, becomes part of the record.

**Candidates for checks,** each its own tracker for the Owner's allocation: a release field in each tracker's front
matter, checked at the release commit; and the Board and `--standup` listing every ask that sits on a branch not on
main.

**Filed 2026-10-18; nothing is built.** Its work is v0.20.2's allocation, which the Owner accepted in FM-023 (`88bf707`).
The second skill is named `/prune-drift`, the Owner's word of 18 October (recorded privately).

- **The problem:** a rule an agent should keep is often held only as prose: in `AGENTS.md`, the contributing guide, the
  triage rules, a seat definition or a brief. An agent may never read it, or may read it and go the other way. Two
  sources can state one rule differently, and text that a later ruling revoked can still read as live.
- **What v0.20.2 proposes,** in FM-023's table of 2026-10-18:
  - **`/find-drift`,** a read-only skill. It finds these three kinds of drift point, grades each rule on five layers,
    and ranks what can become a check. The layers are: impossible to break; the build fails; a rule or a review; a
    skill; a style guide.
  - **`/prune-drift`,** the second skill, built on it, that moves history to the record and rules to checks.
  - Both skills ship in one Claude plugin.
- **Its first run,** on shoalmark at `5dcdcc5`, is recorded privately.

## Why

A check refuses a break every time it runs, but prose works only when it is read and kept. The places where a rule is
only prose are where an agent drifts. Finding them is the first step to making them checks.

## Done when

- `/find-drift` and `/prune-drift` ship in v0.20.2's Claude plugin, each reviewed like code.
- A second run, on a codebase shoalmark did not shape, has corrected `/find-drift`'s spec.
- shoalmark's own report is in the record.

## Ship log

| Date | Event |
|---|---|
| 2026-10-27 | Its next round recorded, from v0.20.1's debrief and a user's question, as relayed by the Auditor: decisions as sources, the record against git, stranded work, and an evidence chain for each finding. Briefed after the v0.20.2 lane is pushed. Records only. |
| 2026-10-18 | The second skill named `/prune-drift`, the Owner's word of 18 October (recorded privately); v0.20.2's allocation accepted (`88bf707`). |
| 2026-10-18 | Filed, with v0.20.2's allocation ask on FM-023. |
