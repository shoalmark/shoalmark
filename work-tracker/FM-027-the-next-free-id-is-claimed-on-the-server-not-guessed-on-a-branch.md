---
id: FM-027
status: Parked
considered: FM-008, FM-011, FM-024
tags: research
kind-of-problem: complicated
next: owner
triaged: 2026-09-28
tier: P3
ask: "How are review ids (RV-…) allocated across sessions, so that two Reviewers never mint the same id?"
ask-kind: ruling
ask-since: 2026-09-28
ask-options: "a block per session, claimed on the server in the review folder: FM-027's design for tracker ids, extended to review ids | each session's Principal allocates ranges to its Reviewers and announces its block in chat; both forges grepped first | as today: the next free id across both forges, read right before writing"
ask-proposal: "a block per session, claimed on the server in the review folder: FM-027's design for tracker ids, extended to review ids"
hook: "`--new` takes the next id it can see on the branch it runs on; two branches that have not merged both get it — it happened twice in one evening. A readable prefix and a counting number stay; the claim moves to the one place that is atomic for everyone, the server"
---

# FM-027 — the next free id is claimed on the server, not guessed on a branch

Seat: Principal · filed 2026-09-23 on the Owner's word *(spelling and wording normalised at his request; the meaning
unchanged)*: *"This is the biggest issue I see right now: how to get the next free id and then claim the unique id for a
tracker. This is simpler in a solo setup like ours — and it can still fail for non-merged local branches, right? … I do
not want UUIDs or anything nobody can read or remember — never. Humans like a prefix and a number that counts upwards."*
Written to be attacked.

## What is true now

**2026-09-28 — raised and asked (PortDive ledger row 55 first, 06:45:49):** the class returned for review ids across sessions (see `## Raised`); the pass of 2026-09-28 keeps it P3, Parked, `next: owner` for the ask above — the Principal's counsel is the first option, a block per session claimed on the server, this tracker's own design extended; the status stays Parked until his answer names a design worth building.

**Filed 2026-09-23; nothing is built.** `--new` reads the trackers on the branch it runs on and takes the next number
after the highest it sees. Two branches cut from the same trunk both see the same highest number; both get the same id;
the first to merge keeps it and the second is refused by the H1/filename gate at merge time — or worse, both merge as
different files with one id. On 2026-09-23 it happened twice within an hour in this repository (FM-025 allocated on two
branches; FM-026 scaffolded as FM-025 because FM-025's branch had not merged), each time caught by a person reading the
filename. In a fleet with several sessions on several branches it is the normal case, not the exception.

**How others do it (read 2026-09-23):** the distributed trackers that live in git — git-bug, ticgit, git-issue, Fossil's
tickets — give up the readable number: an id is a hash, and the number a person sees is a local listing index that is
not stable across clones. That is the trade the Owner refuses. Where readable numbers survive, a server hands them out:
a forge's issue counter, a database sequence, a ticket server. **The one atomic act every git server already offers is
creating a ref: a push that creates `refs/claims/<ID>` succeeds for exactly one pusher and is rejected for every other
(a `--force-with-lease=refs/claims/<ID>:` push, expecting the ref not to exist, is the exact form). Subversion has the
same act: `svn mkdir <repo>/claims/<ID>` commits for exactly one client.**

## Why

An id is the routing key of the whole record — files, branches, evidence folders, the board, the history. A duplicated
id is two records wearing one name; a person cannot tell them apart and neither can the tool. The number must stay
readable and count upwards, and it must be claimed once, by an act that cannot succeed twice.

## Candidates — to be attacked, none chosen

1. **A claim ref on the server (recommended):** `--new` asks the remote for the claims it holds (`git ls-remote origin
   'refs/claims/*'`), takes the next free number, and claims it by pushing `refs/claims/<ID>` pointing at the commit (or
   an empty tree object) with a lease that expects the ref not to exist; on rejection it retries with the next number.
   The tracker file follows on any branch. The gate at `--check` refuses a tracker whose id has no claim ref, and a claim
   ref that no tracker on any branch names for more than a day is listed as abandoned. Subversion: a `claims/<ID>`
   directory committed the same way. No second repository, no counter file to merge, readable ids, works from any
   branch, needs the network once per filing. Cost ≈ 80 lines and a suite that plants two claimants.
2. **A counting repository (the Owner's proposal):** a second repository whose `main` holds the counter; merging to it
   claims the id. Atomic and readable, but it is a second thing to create, permission, and keep running, and a claim is
   still a branch merge — the same race one step removed, unless the push itself is the claim (which is candidate 1 with
   a separate repository).
3. **The forge's issue counter:** create an issue, take its number. Readable and atomic; binds the tool to one forge,
   mixes two kinds of record, and Subversion has none.
4. **Reserved ranges per seat or per session** (Implementer 100–199 …): no server, but ids stop counting upwards and a
   range runs out or leaks.
5. **Drop it:** the filename gate catches the collision at merge time; a person renames. The cost is what it cost tonight,
   times the number of sessions.

## What would decide it

- Two sessions filing at the same second against one remote: exactly one gets `<ID>`, the other `<ID+1>`, ten of ten
  runs, on git and on Subversion.
- A filing with no network: refused with a clear line, or a provisional id that the gate refuses to merge until claimed
  — decided by the Owner's rule for offline work.
- The board and `--check` read claims in under a second on a 500-tracker corpus.

## Done when

The Owner has ruled the candidate; two branches can no longer hold one id; `--new` claims before it writes; the gate
refuses an unclaimed id; the number stays a prefix and a count.

## Raised

- 2026-09-28 02:00:26 and 02:06:06 · two Reviewer seats of one session, each minting "the next free RV id" across both forges (the Principal's briefs said RV-681 onward to both, six minutes apart) · RV-681 minted twice — on shoalmark `e7d16b8` and on PortDive `97fa9ada`; the later renumbered RV-685 before merge. The same evening the Owner's other session took RV-686…690 (`9318ee1b`) and RV-692 while this session's Reviewers minted, and RV-700 crossed this session's own two allocations. The class this tracker names for tracker ids (`--new` on two branches), now for review ids across sessions; RV-473…480 were minted twice on 2026-09-24 as well. The Principal's word, 2026-09-28: a rule is owed — the ask below.

## Ship log

| Date | Event |
|---|---|
| 2026-09-23 | Filed on the Owner's word after two collisions in one evening, tagged `research`; held against FM-008 (the gate as the machine layer), FM-011 (a pin that says what it came from), FM-024 (a session named in the record). Not built this week — the path's line 2. |
