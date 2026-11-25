---
id: FM-188
status: Proposed
considered: FM-033, FM-076, FM-095, FM-097, FM-117, FM-118, FM-139, FM-161, FM-164, FM-170, FM-175, FM-187
tags: process
next: owner
hook: "Rulings collide unseen: an ask is put and answered without the earlier rulings it overturns, because --related reads titles and hooks, not asks and answers. Two decisions met FM-175's signed answer that way, and the releases meet the tracker cut. FM-188-Q1 puts five additions, FM-175 amended, no v0.20.4, and v0.20.3 reopened to add FM-187, FM-161 and the cut's provenance change, so the cut's release can come before v0.21.0."
ask-id: FM-188-Q1
ask: "Do you take FM-188's rulings as proposed, or as changed under other: Part 1's five additions in v0.21.0, FM-175 amended (trackers private in org, views uncommitted, git only, verdicts by signed tag), no v0.20.4, and v0.20.3 from main with FM-187 and FM-161 added, for the cut?"
ask-kind: ruling
ask-since: 2026-11-25
ask-options: "yes, as proposed | yes, but v0.20.3 without FM-187 and FM-161, which go in v0.21.0 | yes, but v0.20.3 folded into v0.21.0 | no, not now"
ask-proposal: "yes, as proposed"
---

# FM-188 — rulings collide unseen: an ask is put and answered without the rulings it overturns, and the release plan meets the move

Seat: the Planner (27f31560), the tool team's lead · filed 2026-11-25, on the coordinator's word of that day.

## What is true now

**2026-11-25 — filed, Proposed, with FM-188-Q1 put; nothing is built.** One ask holds three parts, on the
coordinator's word of that day: the additions that let a ruling's collisions be seen (Part 1), FM-175 amended (Part 2),
and the releases (Part 3), which decide where [FM-187](FM-187-the-gate-passes-a-project-below-the-git-top-unjudged-and-a.md)
and [FM-161](FM-161-a-team-can-only-be-one-whole-repository-so-a-team-in-a.md) ship.

- **The finding:** on 25 November a seat stated the state of things from one source, without looking further, seven
  times. Two decisions collided with [FM-175](FM-175-trackers-are-prose-the-gate-cannot-read-so-each-becomes-a.md)'s
  signed answer of 19 November, and no one saw it: where the tool team's trackers go, and whether built views are
  committed. The instances, the collisions and three `--related` results: recorded privately.
- **What exists:** the gate makes a filing carry `considered:`, and `--related` finds candidates. It covers filings,
  not asks; it reads titles and hooks, not asks and answers; and it reads one repository.
  [FM-095](FM-095-the-owner-s-rulings-live-in-chat-memories-and-briefs-not-in.md),
  [FM-097](FM-097-find-drift-does-not-audit-the-owner-s-rulings-whether-each.md) and
  [FM-117](FM-117-find-drift-does-not-read-decisions-against-git-find-stranded.md) name the same gap and are Proposed.
  [FM-170](FM-170-trackers-hold-the-state-agents-act-on-as-prose-so-every.md) measures the state held as prose.
- **The releases today:** v0.20.3 is not tagged. The newest tag is v0.20.2, and main's `VERSION` reads 0.20.2.
  [FM-139](FM-139-v0-20-3-s-rows-sit-in-fm-023-fm-006-and-fm-053-so-no-one.md) records v0.20.3's four items.
  [FM-164](FM-164-subversion-support-is-deprecated-then-removed-while-the-vcs.md)-Q2's signed answer puts Subversion's
  notice in a v0.20.4 of its own and its removal in v0.21.0.
- **The tracker cut needs a release:** the plan for moving the trackers into the organisation's repository lands
  FM-187's and FM-161's changes in a tool release, which the organisation pins before the import. The plan also names a
  provenance change for that release and leaves its form to the Owner's choice. That choice is not part of this ask;
  decision 10 says how v0.20.3 waits for it.

## Why

A ruling put without the rulings it overturns can be signed into a contradiction, and the record then holds both. A
seat that reads one source repeats it as the state of things. The tool already makes a filing look before it is made;
an ask needs the same, and an answer needs to say what it replaces.

## Decisions, for the Owner

All are put as FM-188-Q1. An answer to it replaces FM-164-Q2's answer (decision 7) and FM-139-Q1's item 4 (decision 9),
and it reopens the Owner's word of 18 to 20 November on v0.20.3's scope (decision 10).

**Part 1: the additions.**

1. **`--related` reads asks and signed answers,** beside titles and hooks.
2. **An ask carries `considered:`.** The gate refuses an ask without it, and the Board shows it with the ask.
3. **An answer names the answer it replaces,** and what is in force is computed from those links.
4. **Every ruling of the Owner is an answered ask.** No second register stands beside the asks.
5. **Cases in shoalmark/tracker-tests:**
   - a new ask that contradicts an old answer brings the old one up;
   - a ruling changed in a fixture changes what a seat answers.

   The fields of items 2 and 3 go into the draft schema in shoalmark/tracker. All five ship in v0.21.0: items 1 and 2
   extend existing code and could ship sooner, but under decision 10's proposal no release before v0.21.0 carries more
   than v0.20.3's items and the cut's two lanes.

**Part 2: FM-175 amended.**

6. **FM-175's decisions change in four places:**
   - **Decision 9, where the trackers go:** the tool team's trackers move privately into the organisation's
     repository at the tracker cut, each team a project in a folder of its own, and the tool reads them there as
     FM-161 serves it. The cut comes before v0.21.0 under decision 10's proposal, and after it under the other two
     options. No public records repository is made. The read at a pin is no longer a condition of the move, as
     FM-161-Q2's signed decisions 12 and 13 already put the move before it. Until that read, FM-033's gate does not
     run in a code repository whose trackers live elsewhere.
   - **Decision 5, views:** `INDEX.md` and each tracker's view are built when asked for and are not committed.
   - **Decision 8, the migration:** git only. No rehearsal on Subversion, and no plain folder. Every commit that counts
     is signed, so the unsigned form of the migration commit goes.
   - **Decision 2, the verdict check:** a done check of kind verdict reads the signed verdict tag.

**Part 3: the releases.**

7. **No v0.20.4,** and no release that only carries a deprecation notice. This replaces FM-164-Q2's answer.
8. **v0.21.0 is git only:** it removes Subversion and the folder-only mode together.
9. **The rows planned for v0.20.4:**
   - FM-164's notice is dropped: no release carries a notice alone. Its removal stays in v0.21.0, with the folder-only
     mode's (decision 8);
   - [FM-076](FM-076-a-seat-s-work-that-only-another-seat-can-push-is-refused-or.md) moves to v0.21.0;
   - [FM-118](FM-118-shoalmark-py-s-prose-is-not-pruned-and-nothing-holds-code.md) moves to v0.21.0.
   The two moves replace FM-139-Q1's item 4, which moved both to v0.20.4. No tag, branch or open pull request is for
   v0.20.4, so nothing built is lost.
10. **v0.20.3:**
    - **Proposed:** v0.20.3 ships from main with FM-187 and FM-161 added to the four items FM-139 records. This
      reopens the Owner's word of 18 to 20 November, which set v0.20.3's scope at those four items and took FM-161 out
      of it. The organisation pins it for the tracker cut, so it also carries the cut's provenance change, once the Owner has
      chosen its form. Its tag comes when FM-161 and that change have landed: FM-161 takes about 2.5 working days from
      its answer, as FM-161's decision 13 sizes it. The provenance change adds its own build and review on top: the
      plan calls the form it proposes a small change, and the other form, a bridge to the code repository's history,
      is not sized.
    - **v0.20.3 without FM-187 and FM-161:** v0.20.3 ships as FM-139 records it, and FM-187 and FM-161 ship in
      v0.21.0. The tracker cut then waits for v0.21.0, since the cut needs them in a release, and v0.21.0 has no
      date.
    - **v0.20.3 folded into v0.21.0:** no v0.20.3 tag, and its items ship in v0.21.0. The cut waits for v0.21.0 in this
      case too, with no date.

## Done when

Each item names its commit or pull request when it lands.

- [ ] **The Owner has answered FM-188-Q1.**
- [ ] **FM-175, FM-164, FM-139, FM-076, FM-118, FM-187 and FM-161 follow the answer** in the records, each with a
  dated line.
- [ ] **Part 1's five additions** are built in v0.21.0, each with its tests, and their fields are in the draft schema.
- [ ] **v0.20.3 ships as the answer puts it,** with its tag.

## Ship log

| Date | Event |
|---|---|
| 2026-11-25 | Filed, Proposed, with FM-188-Q1 put: five additions so that a ruling's collisions are seen, FM-175 amended, no v0.20.4, v0.21.0 git only, and v0.20.3 reopened to add FM-187 and FM-161 for the tracker cut. Records only. |
