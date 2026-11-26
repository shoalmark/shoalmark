---
id: FM-189
status: In Progress
considered: FM-139, FM-161, FM-175, FM-187, FM-188
tags: process
next: build
triaged: 2026-11-25
tier: P1
hook: "An import brings trackers into another repository without their history, so every rule that reads who set a line, which ask numbers an id has used, or which commit answered an ask finds only the importer. The organisation's answer of 25 November takes the Owner's signed import as the Owner's attestation of every guarded line of the open trackers it brings, with no bridge to the source history."
---

# FM-189 — an import brings trackers without their history, so who put each ask, answer and line is lost unless the Owner's signed import attests them

Seat: the Planner (27f31560), the tool team's lead · filed 2026-11-25, on the coordinator's word of that day.

## What is true now

**2026-11-25 — filed In Progress, P1; nothing is built,** on the coordinator's word of that day. The tracker cut needs
it in the release the organisation pins before the import, beside
[FM-187](FM-187-the-gate-passes-a-project-below-the-git-top-unjudged-and-a.md) and
[FM-161](FM-161-a-team-can-only-be-one-whole-repository-so-a-team-in-a.md).
- **What fails today:** the tool reads provenance from the project's own history.
  - The ask numbers an id has used come from `git log -G ^ask-id:` of the tracker's file.
  - Who set a guarded line (`next: owner`, `answer:`, `status:`, `considered:`, the triage keys) is the author of the
    last commit that changed it.
  - The commit that answered an ask is found by its `Answers:` trailer and its signature. So are the commit that wrote
    or cleared an answer and each record's signed line.
- **After an import,** that history is one commit, the importer's:
  - each ask is credited to the importer and leaves the Owner's queue;
  - a standing answer is refused, as one that no commit gives;
  - an ask number used before the import can be used again.
- **The organisation's answer:** the Owner's signed import is read as the Owner's attestation of every guarded line of
  the open trackers it brings, as the import's commit holds them, with no bridge to the source history. It is signed in
  the organisation's records on 25 November. It attests the open trackers; FM-187 freezes a tracker the import adds
  already Shipped, and only for the Shipped rule. Who put each ask stays readable in the code repository's history,
  at the commit the import's trailer names.
- **Its one open point:** by which state the import commit verifies as the Owner's, in a project the import itself
  creates. FM-161's pass 3 shows whether the cut's rows hold without an answer to that. If they do not, it goes to the
  Owner as an ask on FM-161.
- **2026-11-26 — the lane's limit,** from its critical review, kept as the lead answered it: an answer that stands
  beside its id in a tracker the import adds already Shipped or Closed is read, and refused as one that no commit gives,
  since the import attests the open trackers alone. None of this team's 52 Shipped or Closed trackers carries an answer.
  The code stays as it is.
- **2026-11-26 — two more limits, from the critical review's last round, kept as the lead answered them:**
  - A seat's commit on a branch cut before a merge import, that writes the trackers as the import's copy holds them and
    lands after it, is named for those lines. The import's `next: owner`, triage keys and an answer with no ask id are
    read as the seat's, and `--check` refuses that answer. An ordinary import made after the same commit is named
    itself, since its own change holds the line. The refusal fails closed, the reading predates that round, and a
    commit beside the import stands, as the rule reads it.
  - An import made again keeps the ask ids its copy holds, and the number rule refuses an open ask whose number the
    first import used. It fails closed; the tracker cut imports once.

## Why

Without it, the open trackers arrive in the organisation's repository with every ask credited to the importer. The
Owner's queue loses them, standing answers are refused, and used ask numbers can be reused. The bridge, which would read
each line from the source repository, needs a reading across repositories that waits for the migration.

## Decisions, as the organisation's answer takes them

1. **The import attests.** Under Git, a commit that carries `Tracker-import: <repository> <commit>` and verifies as the
   Owner's own signed commit, as FM-187's frozen rule verifies it, attests every guarded line of each tracker it adds,
   as that commit holds it.
2. **Who set a line.** A guarded line present at the import and unchanged since is the Owner's attested line. Each rule
   that asks who set it reads the import's verified Owner, and each rule that asks whether its setter held the right
   takes it as held.
3. **Answers and records.** An answer present at the import counts as given, with the import as its commit. The records
   under `## Asks` that the import brings stand as written: their signed lines are not looked up in this history.
4. **Ask numbers.** The numbers an id has used are read from the imported file as the import holds it, beside the
   history after it.
5. **After the import,** every change is judged as today. A line changed later is credited to its own commit, and an
   answer given later needs its own `Answers:` commit.
6. **Nothing else changes.**
   - A seat's import, an unsigned one, or one whose commit does not verify attests nothing, and its lines are credited
     to its committer as today.
   - Without the trailer, nothing changes.
   - Under Subversion and without version control, nothing changes.
7. **Tests:** a row and a mutant for each decision, in a fixture whose trackers come in by the Owner's signed import:
   - an open ask stays in the Owner's queue;
   - a standing answer counts, and a record's signed line stands;
   - the next ask number follows the imported records;
   - a line changed after the import is judged as today;
   - a seat's import, or an unsigned one, attests nothing.
8. **The lane** reads FM-187's import check and lands below FM-161's top. The three ship in the cut's release, as
   [FM-188](FM-188-rulings-collide-unseen-an-ask-is-put-and-answered-without.md)-Q1 put the release.

## Done when

- [ ] **The import attests** the guarded lines of the open trackers it adds, with its tests and mutants.
- [ ] **The critical review** is READY.
- [ ] **The organisation's acceptance** passes on one candidate that holds FM-187, FM-161 and this.
- [ ] **It ships in the tracker cut's release,** with FM-187 and FM-161.

## Ship log

| Date | Event |
|---|---|
| 2026-11-26 | Two more limits recorded: a seat's commit beside a merge import, made before it, is named for the lines it writes as imported; an import made again is refused by the number rule for the ids its copy holds. Both fail closed. Records only. |
| 2026-11-26 | The lane's limit recorded: an answer beside its id in a tracker the import adds already Shipped or Closed is refused, since the import attests the open trackers alone; FM-187 freezes a Shipped tracker for the Shipped rule only. Records only. |
| 2026-11-25 | Filed In Progress, P1: the Owner's signed import attests every guarded line of the open trackers it brings, as the organisation's answer puts it. Records only. |
