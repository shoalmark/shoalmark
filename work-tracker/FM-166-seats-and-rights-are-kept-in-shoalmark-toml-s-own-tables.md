---
id: FM-166
status: Proposed
considered: FM-010, FM-015, FM-024, FM-026, FM-100, FM-156, FM-161, FM-165
tags: process
next: review
hook: "Who sits where and what each seat may change: shoalmark reads it from [seats] and [rights] in shoalmark.toml, and hail/1's first edition defines a signed roster of its own. A repository that adopts both holds it twice, and the two can drift. The proposal, put to the Owner as FM-166-Q1: one [roster] table, defined by sealanes/1, in the adopter's own configuration, one per repository and found in a fixed order. In shoalmark.toml it replaces [seats] and [rights], with a migration, in v0.20.3."
---

# FM-166 — seats and rights are kept in shoalmark.toml's own tables while hail/1 has a roster of its own, so a repository adopting both holds who sits where twice

Seat: the Planner (27f31560) · filed 2026-11-13, on the Auditor's word of that day.

## What is true now

**Filed 2026-11-13, Proposed; nothing is built.** Its ask, FM-166-Q1, is put to the Owner with v0.20.3 as the
proposal. It waits on the roster table's shape: a later edition of hail/1 moves its roster into sealanes/1, the roster
spec in shoalmark/sealanes. `blocked-by:` names trackers and the Owner only, so the wait is written here.

- **shoalmark's side today:**
  - `shoalmark.toml` names the seats in `[seats]`
    ([`shoalmark.toml` L7](https://github.com/shoalmark/shoalmark/blob/c1e1cea2be92ff433933732a077dacfcb9079e8d/shoalmark.toml#L7)),
    and `[rights]` gives a name of the repository's own its rights; the four built-in names have theirs, and with
    neither table nothing is enforced
    ([`shoalmark.py` L91–L100](https://github.com/shoalmark/shoalmark/blob/c1e1cea2be92ff433933732a077dacfcb9079e8d/shoalmark.py#L91-L100),
    [L785](https://github.com/shoalmark/shoalmark/blob/c1e1cea2be92ff433933732a077dacfcb9079e8d/shoalmark.py#L785)).
  - A seat cannot add itself unseen: the change is in the same diff as anything it would allow
    ([L89](https://github.com/shoalmark/shoalmark/blob/c1e1cea2be92ff433933732a077dacfcb9079e8d/shoalmark.py#L89)).
  - Old spellings are still read beside the new: `[seats] owner` beside the top-level `owner`
    ([L7092](https://github.com/shoalmark/shoalmark/blob/c1e1cea2be92ff433933732a077dacfcb9079e8d/shoalmark.py#L7092)),
    and `answerers` where neither `owner` nor `[seats]` is given
    ([README L324](https://github.com/shoalmark/shoalmark/blob/c1e1cea2be92ff433933732a077dacfcb9079e8d/README.md#L324)).
    [FM-010](FM-010-the-answerers-deprecation-warning-never-reaches-the.md) carried that key's warning.
- **hail/1's side today:** its first edition, not yet in force, keeps its own roster, "the one signed file that says
  who may do what, with which keys"
  ([`spec/hail-1.md` §8](https://github.com/shoalmark/hail/blob/f5b160698a180481240dbff5c8cc605aaab06121/spec/hail-1.md#L347)).
  The file's form is not settled: it is "settled together with `hail check`"
  ([L1207](https://github.com/shoalmark/hail/blob/f5b160698a180481240dbff5c8cc605aaab06121/spec/hail-1.md#L1207)).
- **What is already decided elsewhere:** [FM-100](FM-100-the-stand-up-prompt-is-code-and-english-on-every-board-while.md)'s
  decision 9, as proposed, names sealanes/1 as the roster spec and says a later edition of hail/1 takes its roster from
  it. FM-100 needs three things of the roster: no session, no machine path, and that only the Owner's signed commit
  changes it.

## Why

Who sits where, and what each seat may change, is one fact about a team. Kept in shoalmark's own tables and again in
hail/1's roster, it can say two things in one repository, and each tool reads only its own. One table, defined once by
sealanes/1, read by every adopter in the same order, gives one answer.

## Decisions, for the Owner

1. **The table:** `[roster]`, its shape defined by sealanes/1. sealanes/1 defines the table, not a file name. This
   tracker adopts that shape and defines none of it.
2. **Where it lives:** in the adopter's configuration. That is `shoalmark.toml` where shoalmark is adopted, and
   `hail.toml` where only hail/1 is.
3. **One roster per repository, found in a fixed order:**
   - the tool looks in `shoalmark.toml`, then `hail.toml`, then later adopters' files as sealanes/1 lists them;
   - a second `[roster]` in the same repository is refused as soon as it is detected, with one line naming both files.
4. **In place, or by reference:**
   - a `[roster]` is written in place, or refers to an organisation's roster pinned to a commit;
   - a pinned roster is checked before it is read;
   - how the reference names its repository, file and commit, and how the check is made, follow sealanes/1.
5. **The migration, in `shoalmark.toml`:**
   - `[roster]` replaces `[seats]` and `[rights]`;
   - where no `[roster]` exists, the old tables are still read, with a warning naming the `[roster]` lines to write, as
     the old spellings above are read today;
   - a `[roster]` beside either old table is refused, with one line naming both;
   - the old tables are removed in a later release, named by its own ask;
   - ADOPT's upgrade notes name the step, and shoalmark's own `shoalmark.toml` moves in the same lane;
   - whether the top-level `owner` and the tool's built-in seat names move into the roster follows sealanes/1's shape;
     until then both stay as they are.
6. **The limit, stated in the README and the docs:**
   - a repository that adopts hail/1 alone, without git, has no signed commit guarding the roster: whoever can write
     its file can change who sits where, and nothing records who did;
   - in a git repository under shoalmark, a roster change is in the same diff as anything it would allow, and FM-100
     needs the Owner's signed commit for it.
7. **The release, v0.20.3:**
   - this is the proposal;
   - the lane starts once the table's shape is settled;
   - if the shape is not settled when v0.20.3's lanes are set, the lane waits, and a new ask names its release.
8. **The review is critical:** it touches rights.

**Where it meets other trackers:**

- [FM-165](FM-165-a-tracker-can-only-be-closed-by-hand-so-its-open-asks-where.md)'s drafted question names "a seat
  whose [rights] entry holds close". If this tracker is taken, that entry is the seat's entry in the roster.
- [FM-161](FM-161-a-team-can-only-be-one-whole-repository-so-a-team-in-a.md): one roster per repository holds every
  team in it. How teams in one repository keep their work apart stays FM-161's.
- [FM-024](FM-024-a-seat-s-commit-names-its-session-and-the-record-knows-the.md): a seat's identities, one or a
  list, and the Owner who is not a seat, carry over into the roster unchanged in meaning.

## Done when

Each item names its commit or pull request when it lands.

- [ ] **The Owner has answered FM-166-Q1.**
- [ ] **The roster table's shape is settled** in sealanes/1.
- [ ] **The tool reads `[roster]`** from `shoalmark.toml` or `hail.toml` in the fixed order, in place or by a pinned
  reference, each with its tests.
- [ ] **A second `[roster]` is refused,** naming both files, with a class test and its mutant.
- [ ] **The migration:** the old tables read with a warning, a `[roster]` beside either refused, each with its tests;
  ADOPT's upgrade notes; shoalmark's own `shoalmark.toml` moved.
- [ ] **README and the docs** describe the roster and its limit, with their German twins.
- [ ] **The critical review is READY.**

## Asks

**FM-166-Q1** · 2026-11-13 · Do you take FM-166's decisions as proposed: a [roster] table defined by sealanes/1, one per repository and found in a fixed order, replaces [seats] and [rights] in shoalmark.toml with a migration, and the lane in v0.20.3?
**withdrawn** — no answer was given

## Ship log

| Date | Event |
|---|---|
| 2026-11-13 | FM-166-Q1 withdrawn with no answer given, so that two decisions can join before the ask is put again. Records only. |
| 2026-11-13 | Filed, Proposed, with FM-166-Q1 put: v0.20.3 proposed, waiting on the roster table's shape. Records only. |
