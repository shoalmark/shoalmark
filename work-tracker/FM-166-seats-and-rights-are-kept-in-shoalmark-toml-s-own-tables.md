---
id: FM-166
status: Proposed
considered: FM-010, FM-015, FM-024, FM-026, FM-100, FM-156, FM-161, FM-162, FM-165
tags: process
next: wait
hook: "Who sits where and what each seat may change: shoalmark reads it from [seats] and [rights] in shoalmark.toml, and hail/1's first edition defines a signed roster of its own. A repository that adopts both holds it twice, and the two can drift. The proposal: one [roster] table, defined by sealanes/1, in the adopter's own configuration, one per repository and found in a fixed order. In shoalmark.toml it replaces [seats] and [rights], with a migration. FM-166-Q2 is withdrawn, since sealanes/1's design supersedes decisions 5, 8 and 9. The changed question is put once FM-139-Q1 is answered, and names the release that answer gives."
---

# FM-166 — seats and rights are kept in shoalmark.toml's own tables while hail/1 has a roster of its own, so a repository adopting both holds who sits where twice

Seat: the Planner (27f31560) · filed 2026-11-13, on the Auditor's word of that day.

## What is true now

**2026-11-13 — FM-166-Q2 withdrawn with no answer given,** on the coordinator's word of that day. sealanes/1's
design round closed on 13 November. The design supersedes decisions 5, 8 and 9, and sealanes/1's first edition
carries them. The other decisions stand.
- **The changed question,** drafted here with no id until it is put: "Do you take FM-166's decisions as proposed: a
  [roster] table defined by sealanes/1's first edition, which carries the migration, the list of acts and the version
  rule, replacing [seats] and [rights] in shoalmark.toml, and the lane in the release FM-139-Q1's answer names?"
- It is put once FM-139-Q1 is answered, since that answer names the release.

**Filed 2026-11-13, Proposed; nothing is built.** Its first ask, FM-166-Q1, was withdrawn with no answer given, so
that two decisions could join: one closed list of acts (decision 8) and the version rule (decision 9). It is put
again as FM-166-Q2, with v0.20.3 as the proposal. It waits on the roster table's shape: a later edition of hail/1 moves its roster into sealanes/1, the roster
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
sealanes/1, read by every adopter in the same order, gives one answer. A closed list of acts and one version rule,
settled before either spec's first release, let a roster outlive the tools that read it: a reader that is behind can
only withhold a right, never grant one.

## Decisions, for the Owner

Decisions 5, 8 and 9, and the Done when items that follow from them, are superseded by sealanes/1's design, as the
dated line of 2026-11-13 says.

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
   - the aliases `principal` and `implementer` in `BUILTIN_RIGHTS`
     ([L785–L786](https://github.com/shoalmark/shoalmark/blob/c1e1cea2be92ff433933732a077dacfcb9079e8d/shoalmark.py#L785-L786)) retire with the
     migration, as part of this lane. [FM-156](FM-156-the-seats-principal-and-implementer-the-former-names-of.md)
     plans the same retirement; it is done once, and whichever lands second cites the first;
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
8. **One closed list of acts:**
   - sealanes/1 defines the acts a right may grant. The list starts from the four the tool holds: `answer`, `ask`,
     `close` and `triage` ([`shoalmark.py` L780–L783](https://github.com/shoalmark/shoalmark/blob/c1e1cea2be92ff433933732a077dacfcb9079e8d/shoalmark.py#L780-L783)).
   - A later act, such as merge, enters through the spec, never through one tracker.
   - `--check` refuses an act the list does not hold, in the repository whose roster it is, so a misspelt act or one
     the tool cannot enforce is caught where it is written. A reader of a roster it does not gate ignores such an
     act and warns, as decision 9 says.
   - From v0.20.3 on, everything that reads seats or rights reads `[roster]` from the start: FM-165's close right,
     and FM-100's roster and its coordinator.
   - [FM-162](FM-162-the-acts-a-seat-must-never-do-are-held-only-as-prose-so-one.md) is not touched: it reads no
     right.
9. **The version rule,** settled before either spec's first release:
   - a roster names its edition: `spec = "sealanes/1"`;
   - a reader refuses an edition it does not know, whole, naming the edition it needs;
   - within an edition, changes only add;
   - rights only grant, so a reader ignores an act or key it does not know and warns: that can only withhold a right;
   - a key that restricts, if one is ever needed, is marked must-understand, and an unknown must-understand key
     refuses the roster;
   - a roster by reference is pinned to a commit, and its edition is checked at that pin;
   - a later edition of hail/1 states the same rule for its messages.
10. **The review is critical:** it touches rights.

**Where it meets other trackers:**

- [FM-165](FM-165-a-tracker-can-only-be-closed-by-hand-so-its-open-asks-where.md)'s close right is read from
  `[roster]`, and its drafted question on who may close waits on decision 8's list of acts.
- [FM-161](FM-161-a-team-can-only-be-one-whole-repository-so-a-team-in-a.md): one roster per repository holds every
  team in it. How teams in one repository keep their work apart stays FM-161's.
- [FM-024](FM-024-a-seat-s-commit-names-its-session-and-the-record-knows-the.md): a seat's identities, one or a
  list, and the Owner who is not a seat, carry over into the roster unchanged in meaning.

## Done when

Each item names its commit or pull request when it lands.

- [ ] **The Owner has answered FM-166-Q2.**
- [ ] **The roster table's shape is settled** in sealanes/1.
- [ ] **The tool reads `[roster]`** from `shoalmark.toml` or `hail.toml` in the fixed order, in place or by a pinned
  reference, each with its tests.
- [ ] **A second `[roster]` is refused,** naming both files, with a class test and its mutant.
- [ ] **The migration:** the old tables read with a warning, a `[roster]` beside either refused, each with its tests;
  ADOPT's upgrade notes; shoalmark's own `shoalmark.toml` moved.
- [ ] **The aliases retired:** `BUILTIN_RIGHTS` holds the Owner and the three built-in seats only, here or through
  FM-156, with its tests.
- [ ] **One closed list of acts** in sealanes/1, starting from the four; `--check` refuses an act it does not hold, with
  a class test and its mutant.
- [ ] **Everything that reads seats or rights reads `[roster]`:** FM-165's close right, and FM-100's roster and its
  coordinator, each with its tests.
- [ ] **The version rule,** a class test per clause, each with its mutant: the edition named; an unknown edition
  refused whole, naming the edition needed; a key added within the edition read by a reader that predates it; an
  unknown act or key ignored with a warning; an unknown must-understand key refusing the roster; a referenced
  roster's edition checked at its pin.
- [ ] **README and the docs** describe the roster and its limit, with their German twins.
- [ ] **The critical review is READY.**

## Asks

**FM-166-Q1** · 2026-11-13 · Do you take FM-166's decisions as proposed: a [roster] table defined by sealanes/1, one per repository and found in a fixed order, replaces [seats] and [rights] in shoalmark.toml with a migration, and the lane in v0.20.3?
**withdrawn** — no answer was given

**FM-166-Q2** · 2026-11-13 · Do you take FM-166's decisions as proposed: a [roster] table defined by sealanes/1, one per repository and found in a fixed order, replacing [seats] and [rights] in shoalmark.toml with a migration, one closed list of acts, the version rule, and the lane in v0.20.3?
**withdrawn** — no answer was given

## Ship log

| Date | Event |
|---|---|
| 2026-11-13 | FM-166-Q2 withdrawn with no answer given: sealanes/1's design, closed that day, supersedes decisions 5, 8 and 9, and its first edition carries them. The changed question is drafted with no id, to be put once FM-139-Q1 is answered. Records only. |
| 2026-11-13 | FM-166-Q2 put: one closed list of acts and the version rule join the decisions, and the aliases `principal` and `implementer` retire with the migration; v0.20.3 unchanged. Records only. |
| 2026-11-13 | FM-166-Q1 withdrawn with no answer given, so that two decisions can join before the ask is put again. Records only. |
| 2026-11-13 | Filed, Proposed, with FM-166-Q1 put: v0.20.3 proposed, waiting on the roster table's shape. Records only. |
