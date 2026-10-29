---
id: FM-062
status: In Progress
considered: FM-042, FM-037, FM-026, FM-023
tags: process
next: build
triaged: 2026-10-19
tier: P2
hook: "an agent drifts off track where a rule is held only as prose, two sources disagree, or obsolete text still reads as live"
ask: "Do /find-drift's five layers keep your order of 18 October, with a skill below a rule a reviewer checks, as FM-062's section The layer order, for the Owner sets out?"
ask-kind: ruling
ask-since: 2026-10-27
ask-options: "yes, the order stays | no: a skill ranks above a rule a reviewer checks"
ask-proposal: "yes, the order stays"
answer: "accepted - yes, the order stays"
answered: 2026-10-28
answered-by: holgo99
---

# FM-062 — an agent drifts off track where a rule is held only as prose, two sources disagree, or obsolete text still reads as live

## What is true now

**2026-10-27 — its layer-order ask filed on main.** It was put on 19 October on `fm/062-prune-drift`, a branch main
never received, so the Board never showed it. It comes to main now, so the Owner can answer it before `/find-drift`
ships, with the section *The layer order, for the Owner* below. The rest of that branch's records go with
`/prune-drift`'s rebuild onto the v0.20.2 lane.

**2026-10-19 — one ask, on the layer order.** `/find-drift`'s spec keeps the five layers in the order the Owner
accepted. Whether a skill should rank above a rule a reviewer checks is put to the Owner, under *The layer order, for
the Owner* below. The build goes on meanwhile.

**2026-10-27 — `/prune-drift` stays in v0.20.2; its outputs move to v0.20.3,** on the Owner's word of 27 October, as relayed by the Auditor: the prose prune of `shoalmark.py` with the comment ratchet, the five conversions, and the text fixes. FM-023's ask of 27 October puts the move to the Owner.

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

**2026-10-27 12:45:28 CET** — CI runs `test_plugin.py` after `test_core.py` under the full-suite tier condition and includes all three suites and exits in its TZ report; the CI checks and mutants cover the third suite and its tracker-read scan. Critical review next.

**2026-10-19 17:22:20 CEST — `/prune-drift`'s spec and proof are built in `7983283` and `8f22b12`; nine fixtures and six mutants pass on Python 3.15.0 and 3.9.6, review next.**

**Filed 2026-10-18. Judged In Progress, P2, on 2026-10-19, before the first build commit; `/find-drift`'s spec and the plugin are built, review next.** Its work
is v0.20.2's allocation, which the Owner accepted in FM-023 (`88bf707`). Work on v0.20.2 starts on branches, on the
Owner's ruling of 19 October, and lands after v0.20.1. `/find-drift`'s spec and the plugin come first.
The second skill is named `/prune-drift`, the Owner's word of 18 October (recorded privately).

- **The problem:** a rule an agent should keep is often held only as prose: in `AGENTS.md`, the contributing guide, the
  triage rules, a seat definition or a brief. An agent may never read it, or may read it and go the other way. Two
  sources can state one rule differently, and text that a later ruling revoked can still read as live.
- **What v0.20.2 proposes,** in FM-023's table of 2026-10-18:
  - **`/find-drift`,** a skill that reads the repository and writes only its report and the report's hash, or a
    private supplement where the person names its folder. It commits nothing. It finds these three kinds of drift
    point, grades each rule on five layers, and ranks what can become a check. The layers are: impossible to break;
    the build fails; a rule or a review; a skill; a style guide.
  - **`/prune-drift`,** the second skill, built on it, that moves history to the record and rules to checks.
  - Both skills ship in one Claude plugin.
- **Its first run,** on shoalmark at `5dcdcc5`, is recorded privately.

## The layer order, for the Owner

- **The question:** does a skill rank above a rule a reviewer checks?
- **Today's order,** which the Owner accepted with v0.20.2's allocation on 18 October (FM-023, `88bf707`):
  1. impossible to break;
  2. the build fails;
  3. a rule or a review;
  4. a skill;
  5. a style guide.
- **Why it is asked:** the spec's second run, on a codebase shoalmark did not shape, met fixes that are a command or a
  skill carrying a rule. By today's order such a fix ranks below a rule a reviewer checks. The seat that ran it
  proposed putting a skill third and a reviewed rule fourth, at 55 %.
- **Already settled in the spec:** a generator that writes the result is layer 1, so a command that writes what the
  rule asks for is not graded as a skill.
- **The proposal: the order stays (65 %).** A review stands on every merge's path (the current path's line 2), while a
  skill acts only where an agent invokes it. A rule moved into a skill stops no break that nobody invokes it for.
- **If the order changes,** only step 5 of the spec changes, the grading.

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
| 2026-10-27 | Its layer-order ask of 19 October filed on main, from `fm/062-prune-drift`, which main never received; the section *The layer order, for the Owner* with it. Records only. |
| 2026-10-27 | `/prune-drift` stays in v0.20.2; the prose prune with the comment ratchet, the five conversions and the text fixes move to v0.20.3, on the Owner's word of 27 October. Records only. |
| 2026-10-27 | Its next round recorded, from v0.20.1's debrief and a user's question, as relayed by the Auditor: decisions as sources, the record against git, stranded work, and an evidence chain for each finding. Briefed after the v0.20.2 lane is pushed. Records only. |
| 2026-10-27 12:45:28 CET | CI adds the plugin suite in `89b7f7a`; both Python versions pass the plugin, core, CI and release-workflow slices. The plugin reads no tracker paths; a synthetic tracker-read control proves that a future read needs a records-tier exclusion. Critical review next. |
| 2026-10-20 09:45:15 CEST | Round 2 RV-3501 addressed in `a5296ee`: the proof retains the active shebang line from the original bytes, including its terminator; executable LF/CRLF regressions verify exact committed blobs. All 17 fixtures pass and all nine scratch mutants are caught on Python 3.15.0 and 3.9.6. The Owner authorized this fix after the original final round; independent verification remains pending. |
| 2026-10-19 21:34:00 CEST | Round 1 RV-3500 addressed in `46eff9f`: the proof compares raw-byte shebang activation, including a preceding BOM, and directive attachment to its physical code line. All 15 fixtures pass and all eight scratch mutants are caught on Python 3.15.0 and 3.9.6; round 2 next. |
| 2026-10-19 17:22:20 CEST | `/prune-drift`'s spec and proof built on `/find-drift`'s READY head: the sort, record-before-delete steps, reader and directive safeguards, and nine-fixture class test are in `7983283` and `8f22b12`; all six scratch mutants are caught on both interpreters. Review next; suite registration waits for v0.20.2's integration branch. |
| 2026-10-19 13:12:55 CEST | Round 1's RV-3491, RV-3492 and RV-3493 fixed: the description names the report destination, the tracker folder's fallback is explicit, and scoped runs retain the snapshot and source hashes; round 2 next. |
| 2026-10-19 12:38:39 CEST | `/find-drift`'s spec and the plugin built in `818eb0c` and `0289061`; the standalone structure test passes on Python 3.15 and 3.9.6, with all four mutants refused on both. Review next; suite registration and `drift_sources` reader support follow on the integration lane. |
| 2026-10-19 | *What is true now* corrected by the Planner: `/find-drift` reads the repository and writes only its report, its hash or a named private supplement; it is not read-only. |
| 2026-10-19 | Judged In Progress, P2, by the Planner, before the first build commit: `/find-drift`'s spec and the plugin, on `fm/062-find-drift`. |
| 2026-10-18 | The second skill named `/prune-drift`, the Owner's word of 18 October (recorded privately); v0.20.2's allocation accepted (`88bf707`). |
| 2026-10-18 | Filed, with v0.20.2's allocation ask on FM-023. |
