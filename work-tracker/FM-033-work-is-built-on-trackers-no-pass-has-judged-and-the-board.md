---
id: FM-033
status: Proposed
considered: FM-005, FM-021, FM-024, FM-029, FM-030, FM-031, FM-032
tags: bug
next: build
ask: "Does a signed answer that says *now* count as the judgement?"
ask-kind: ruling
ask-since: 2026-09-24
ask-options: "a pass judges before the first build commit, the same day as a now, and a pass that finds it not ready asks you again | the signed now is the judgement: --answer writes the judgement fields | --answer prints what a pass would judge, and a pass still runs"
ask-proposal: "a pass judges before the first build commit, the same day as a now, and a pass that finds it not ready asks you again"
answer: "accepted - a pass judges before the first build commit, the same day as a now, and a pass that finds it not ready asks you again"
answered: 2026-09-24
answered-by: holgo99
triaged: 2026-09-24
rank: 9
tier: P2
hook: "On 2026-09-24 the board showed the day's release work under triage and four idle trackers under progress: code for four pieces of work was built before any pass had judged it, one of them under no tracker at all, and the record said nothing."
---

# FM-033 — Work is built on trackers no pass has judged, and the board shows the person that work as waiting for triage

## What is true now

**Written 2026-09-24 by the Auditor seat (session 8b91dba2), filed word for word by the Principal, on the Owner's word: *"This shall be tracked as a violation of the
rules and as a new issue."* Nothing is built.** Every time and sha below is from git or GitHub. Times are CEST.

## The violation

**The rules in force:**
- The Owner's signed intent, `work-tracker/TRIAGE.md`, *never* (signed `45198d5`, 2026-09-23 14:29:54): *"a rogue tasking or
  unauthorised work; nothing that is not in the record; … take up work that is not ready or cannot be delivered when due"*.
- `AGENTS.md:7`: *"Start here: `python3 shoalmark.py --next` says what to work on"*. `AGENTS.md:17–18`: `triaged:` `tier:`
  `rank:` are written by `--triage`, and the seat judges.
- The first pass (2026-09-23) left FM-023 and FM-024 out: *"the next pass reads them"*. The second pass ran on 2026-09-24 at
  14:49 (`7d3e632`), after the Owner pointed at the board.

**Four builds, after the intent was signed, before any judgement:**

| Work | Filed | Authority at the time | First build commit | Marked In Progress | Judged |
|---|---|---|---|---|---|
| FM-024, the session trailer and the registry | `fe4d9eb` 09-23 15:24 | "on the Owner's word": no ask, no answer, unsigned seat commit `5a4ad6e` | `89e0586` 16:16 (S1–S8, R1–R7 until 18:18, `8b5588e`) | `5a4ad6e` 16:02 | 09-24 14:49: the pass's first version (`7d3e632`) marked it Shipped, by the seat that built it; the pass re-made on its Reviewer's R1 (`87bac4e`) keeps it, P2 #8, judged by that seat's own session |
| FM-032 S2 and S4, the registry as a report and the freeze | `4af2c9b` 09-24 09:35 | signed answer `ffa63b8` 11:07:43, *"all four now"* | `3c0754f` 11:31 | `a2956a5` 11:45, **14 min after the build began** | 14:49 |
| FM-031 S2, `--queue` | `d935807` 08:25 | signed answer `d20bc89` 11:08:24, *"all three rules now, S1 then S2"* | `90d3d6f` 12:01 | `fbc2697` 12:19, on the release branch, **18 min after the build began**; on `main` only at 14:35 (PR 49) | 14:49 |
| `--answer … revoke` and `--supersede` | **no tracker** | the Owner's chat request of 11:29:05, *"we need a path that the user can choose"* (written and signed nowhere) | `bd7d5ea` 12:15, subject "RV-479", a finding id from another repository | never | never |

All four shipped in `v0.18.0` (tag on `095f1d3`, PR 49 merged 14:35).

## Why the person saw nothing

- **`progress` lists only judged trackers** ("kept by triage — by rank, then tier"). **`triage` lists everything unjudged**,
  whatever is being built on it. Neither reads activity: branches, commits, pull requests.
- **The board reads `main`.** A status written on a branch is invisible until its merge. FM-031 read *Proposed* on the Owner's
  board at 14:32 while its branch had said *In Progress* since 12:19.
- **So the board showed** four trackers under `progress`, FM-005 (the shadow week, waiting), FM-006 (judged and worked through
  09:05) and two idle P3 rows, while the day's release was listed as unjudged filings.

## Why a gate on the status alone misses it

A gate proposed to the Owner in chat on 2026-09-24, not in this repository and never built, would refuse "an In Progress tracker without a judgement". Applied to the four builds:
- FM-024 would have been refused at the status commit (16:02), before its build.
- FM-032 and FM-031 were built while still *Proposed*. That gate would have fired only at the later status change, after the build.
- The revoke/supersede work named no tracker, so that gate never fires.
- It refuses the seat that updates the status and passes the one that leaves it *Proposed*.

## What would have refused all four

**The gate keys on the work, not on the status.** A commit that changes anything outside `work-tracker/` must name a tracker,
through its branch (`fm/NNN-…`) or a trailer. At the commit's parent, that tracker must be judged (`triaged:` set, not parked)
and *In Progress*. Otherwise the commit is refused, and a commit that names no tracker is refused too. `--queue` and the board
flag a pushed branch whose commits name an unjudged tracker. By construction this refuses the first build commit of all four.

## For the Owner to rule

**Does a signed answer that says *now* count as the judgement?**
- If yes, `--answer` writes the judgement fields with the answer.
- If no, a pass runs before the first build commit.

Today the seats read *"all four now"* and *"all three rules now"* as leave to build, and skipped the pass.

## Done when

- The gate above refuses a build commit on an unjudged, not-In-Progress, or unnamed tracker (suite cases for the four rows above).
- The board shows activity beside judgement: a tracker with commits on a pushed branch in the last day says so, in whichever section it sits.
- The four rows above are recorded against this tracker as the violation, and the seat's ledger row links here.
