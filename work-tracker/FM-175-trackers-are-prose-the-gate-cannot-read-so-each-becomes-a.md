---
id: FM-175
status: In Progress
considered: FM-033, FM-139, FM-161, FM-162, FM-165, FM-166, FM-170
tags: process
next: build
triaged: 2026-11-19
tier: P2
hook: "A tracker's Done when, its ship log and much of its state are prose: the gate cannot verify one box, and agents read whole files to find what they act on. The design, settled by the Owner on 17 and 18 November: each tracker becomes one .toml file in one canonical form, its Done when five kinds of check the gate decides from data, every write a command the gate replays, the Owner's signed edit never refused, views built from the files. The proposal, put to the Owner as FM-175-Q1: the lane in v0.21.0, built in one repository first."
---

# FM-175 — trackers are prose the gate cannot read, so each becomes a toml file the tool writes and checks

Seat: the Planner (a1730572) · filed 2026-11-18, on the coordinator's word of that day.

## What is true now

**2026-11-25 — [FM-188](FM-188-rulings-collide-unseen-an-ask-is-put-and-answered-without.md)-Q1 puts an amendment of four decisions,** on the coordinator's word of that day:
decision 9 (the tool team's trackers move privately into the organisation's repository at the tracker cut, which comes
before v0.21.0 under its proposal and after it under its other options), decision 5 (views are not committed), decision 8 (git only, every commit that counts signed) and decision 2
(a verdict check reads the signed verdict tag). Nothing here changes until its answer.

**2026-11-19 — FM-175-Q1 answered "yes, as proposed", with the Owner's signature; judged before its first build commit,
keep P2, In Progress; nothing is built.** The lane is in v0.21.0, as the answer gives it.

**Filed 2026-11-18, Proposed, with FM-175-Q1 put; nothing is built.** The schema and its cases are being filed in
`shoalmark/tracker` as a draft not in force, and the tool team's trackers move to a public records repository with
v0.21.0. The design is settled: a design round on 17
November, a count of every `Done when` item in this repository's trackers and those of the organisation's other teams, and the Owner's rulings of 17 and 18 November on each of its open
questions. This tracker is the lane that builds it in `shoalmark.py`.

- **Today:** a tracker is Markdown with front matter. The tool reads the front matter as data. It notes whether a body
  has a `Done when` heading, and verifies no item in it. The ship log is a table written by hand. What is true now, what
  blocks what and which commit met which item sit in prose, where agents read whole files to find them
  ([FM-170](FM-170-trackers-hold-the-state-agents-act-on-as-prose-so-every.md)).
- **The count:** every one of those `Done when` items was sorted into five kinds of check. Five checks in all fit
  none of them.

## Why

What the code or a check holds costs less to read, and is misread less, than what prose holds. A gate that can read
each item of a `Done when` can say when a tracker is done; one that reads a ticked box cannot.

## Decisions, for the Owner

All are put as FM-175-Q1. The design settles each; the lane builds them. Its review's tier is the triage pass's to set.

1. **One file per tracker:** `<id>.toml`, of named tables, written by the tool in one canonical form. A bot's file
   that differs from that form fails. The Owner's signed edit gets the tool's own form-only commit after it, proven by
   parsing to the same content, and is never refused.
2. **The five kinds of done check:**
   - each `Done when` item is one table with its kind and the data the kind needs;
   - the kinds are answer, file, command, verdict and judgment;
   - the gate decides each from data it can read;
   - a command check's result is frozen with its commit;
   - the named judge records a judgment, and the judge never built the change.
3. **Bounded intent fields:** a few free-text fields stay, each one line and capped, and nothing decides from them.
4. **Writes by command only:**
   - one writer in the tool changes trackers;
   - every commit that changes one names its command, and the gate replays the command and refuses what it cannot
     reproduce;
   - ship-log events are written only by commands, each naming the commit it records.
   The Owner's signed hand edit is never refused. A failed check in it warns and opens an item for the Owner; an edit
   that does not parse shows the tracker as unreadable, with an item. A warning blocks no other commit. A bot's hand
   edit is refused.
5. **Views:** `INDEX.md` and one `.md` view per tracker are built, committed and checked by bytes; the rest are
   computed when asked for. No view is ever read as input.
6. **Two retrieval checks:** no reference that does not resolve, and no evidence file nothing names.
7. **One schema, in its own repository:** the schema and its cases are filed now in `shoalmark/tracker` as "tracker/1,
   draft, not in force", and the tool reads the schema from there at a pin, so the shape has one source; `--schema`
   prints it, and nothing else states a field's shape or meaning. The signed edition comes when the format has held.
8. **The converter and the migration:**
   - `--convert`, once per tracker; ids stay;
   - nothing is lost: an old body that fits no field becomes an evidence file named by its hash, and the last `.md`
     commit is tagged;
   - conversion never waits on rewording: a closed tracker converts frozen, its old done items kept as history and not
     checked again; an open tracker's items that fit no kind convert to a judgment with a named judge, to be made
     exact later;
   - earlier answers keep counting, by one migration commit the tool prepares and verifies, signed by the repository's
     Owner, or the same step unsigned where an adopter does not sign;
   - a dry run prints what it would change; the change is then one commit that can be reverted (the v0.21.0 brief's
     point, beyond the four the Owner agreed);
   - in a public tracker, a privately held finding is named only as "recorded privately", and the converter checks that
     before the first push;
   - it is rehearsed before the release (likewise the brief's) on this team's trackers and the organisation's, on an adopter-style
     repository with in-repo trackers and no signing, and on a Subversion repository. How answers keep counting under
     Subversion, which has no signed commits, is not designed yet.
9. **The release and the order:**
   - v0.21.0 carries the format with its converter together with the roster
     ([FM-166](FM-166-seats-and-rights-are-kept-in-shoalmark-toml-s-own-tables.md)), so adopters migrate once, as the
     Owner's word of 18 November has it: "The roster and the tracker format stay together in v0.21.0.";
   - both formats are read throughout v0.21.x, so a repository converted halfway passes the gate; reading `.md` goes no
     earlier than the release after;
   - built and proven in one repository first, in today's in-repo mode, which stays supported (the Owner's word of 18
     November: "in-repo trackers for adopters are fine");
   - the tool team's trackers move to a public records repository with v0.21.0, not before, and only after the gate
     reads that repository at a pin; the reading at a pin is its own lane, beside
     [FM-161](FM-161-a-team-can-only-be-one-whole-repository-so-a-team-in-a.md)'s folders.

## Done when

Each item names its commit or pull request when it lands.

- [ ] **The Owner has answered FM-175-Q1.**
- [ ] **The format, the schema and the canonical form**, each with its tests, the schema read from `shoalmark/tracker` at a
  pin.
- [ ] **The five kinds of done check**, each decided by the gate from data, each with a test that fails when it should.
- [ ] **The writer and its replay**, with the Owner's signed edit never refused, each case with its test.
- [ ] **The views and the two retrieval checks**, each with its test.
- [ ] **The converter**, rehearsed on the three sets of decision 8 with no conversion stopped on an item that fits no
  kind, and the check that nothing private reaches a public tracker.
- [ ] **Both formats read** through v0.21.x, a repository converted halfway passing the gate, with its test.
- [ ] **The tool team's trackers** in their public records repository with v0.21.0, after the gate reads it at a pin.
- [ ] **The review, at the tier the triage pass sets, is READY.**

## Asks

**FM-175-Q1** · 2026-11-19 · Do you take FM-175's lane into v0.21.0 as the settled design gives it: each tracker one .toml file the tool writes and checks, five kinds of done check, writes by command only with your signed edit never refused, built in one repository first?
**answered** — accepted - yes, as proposed · holgo99
**relation** — accepted the proposal
**signed** — 3d50467 · G

## Ship log

| Date | Event |
|---|---|
| 2026-11-25 | FM-188-Q1 put, which amends decisions 2, 5, 8 and 9; nothing changes here until its answer. Records only. |
| 2026-11-20 | A correction to the row below: decision 9's first line quotes the Owner's word of 18 November, "stay together in v0.21.0", where it said "beside the roster"; "together with the roster" is the line's own phrase, not the Owner's. The row below had been rewritten in place the same day; it is restored as first written, since a ship log is only added to. Records only. |
| 2026-11-20 | Decision 9's first line reads "together with the roster", in the Owner's words of 18 November, where it read "beside". Records only. |
| 2026-11-19 | FM-175-Q1 answered, yes, as proposed; judged before its first build commit, keep P2, In Progress; the lane in v0.21.0. Records only. |
| 2026-11-18 | Filed, Proposed, with FM-175-Q1 put: the lane that makes each tracker one toml file the tool writes and checks, as the design settled by the Owner gives it, in v0.21.0. Records only. |
