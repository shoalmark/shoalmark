---
id: FM-031
status: In Progress
considered: FM-005, FM-023, FM-024, FM-027
tags: process
next: wait
triaged: 2026-09-24
tier: P2
hook: "In fourteen hours 22 seat sessions, under 21 ids, opened 22 pull requests, and only the Owner sees the whole queue. By 08:18 six were open: one sat inside another, one had been copied into another, two conflicted on the file every session writes. He asked which to merge five times."
---

# FM-031 — the streams run in parallel and only the Owner sees the whole queue

## What is true now

**Filed 2026-09-24 08:24 CEST on the Owner's question; ruled by his signed answer at 11:08:24 (`d20bc89`): all three
rules now, S1 then S2 — then the cap of 2 revoked by his own signed edit at 12:39:56 (`7c97c5b`, PR 46, merged
12:53:19), so two rules stand: one channel, and the detached switch. Built for 0.18.0 on one branch: S2, `--queue` —
the pull requests at `90d3d6f`, the branches pushed without one and the Owner's `answer/*` at `636f56e`; S1 as FM-032's
S2, the registry a report from the trailers (`3c0754f`); the rules in AGENTS.md (`fbc2697`, the cap paragraph
rewritten on the merge of PR 46). What is left: a week of parallel streams read against *Done when*.**

The measurements below are read from the record: git, the forge, and `work-tracker/sessions.md` on every remote
branch. They cover 2026-09-23 18:00 to 2026-09-24 08:20 CEST.

- **22 sessions began, under 21 ids:** 9 GtM, 9 Implementer, 2 Principal and 2 Reviewer, across 6 worktrees. The
  Implementer's nine carry eight ids: `8e509911/implementer-6` named two, the site slice at 01:02 and FM-028 at 07:41
  (FM-028's R1, the class of FM-027).
- **22 pull requests were opened.** 13 were merged, and six were open by 08:18: #33 from 07:52, #34–#38 from 08:17 to
  08:18.
- **Of the six open ones, at most one could be merged as it stood:**
  - #33 was ready: a Reviewer's verdict names its head, and it merges cleanly.
  - #37's head is an ancestor of #33's head, so #37 is contained in #33.
  - #38's two rows had been carried verbatim into #33. Merging both would write them twice.
  - #35 conflicted in `sessions.md`.
  - #34 and #36 had no verdict on their head.
- **The conflicts were on the shared files.**
  - Every parallel pull request appends its session's row to `work-tracker/sessions.md`, all at the same place. That
    conflicted on #33, #35 and #37.
  - In the parent project that vendors this tool, two pull requests conflicted on its registry the same morning (its
    pull requests 806 and 807; resolved by merging one into the other before the verdict), and earlier on a tracker's ship log.
- **The Owner asked one Implementer session five integration questions in about two hours:**
  - which pull requests to merge;
  - that one of them had a conflict;
  - to run the Reviewer;
  - the list of what was open;
  - this question.

  A seat answered each one by reading the forge and `git merge-tree` by hand.
- **Rulings reached the seats by three routes:**
  - relayed by the coordinating Principal;
  - typed by the Owner into a seat's own session;
  - pasted from another seat's chat.
- **The Owner's own checkout had a seat's branch checked out.** Git refused that branch to the seats twice, and they
  worked on a detached head instead.

**Filing outruns closing about two to one.** The Owner asked it on 2026-09-24 (spelling normalised): *"How much faster
are we filing than we are being able to close?"* **Method:** a filing is the first commit that adds its id under
`docs/work-tracker/` or `work-tracker/`, on `main` or any remote branch; a close is the first commit on `main` whose
status reads *Shipped* or *Closed*; one window, from the first filing to the measurement.

- **The record starts 2026-09-21 13:13 (FM-001, `8cbe3a4`); measured to 2026-09-24 08:53 CEST, 2.82 days.** Re-dated
  on the Reviewer's R1: the first measurement started at 2026-09-22 11:09, `ae1f05e`, the commit that moved the
  trackers to `work-tracker/`, and so dated five filings (FM-001–FM-005) and two closes (FM-002, FM-003) a day late.

  | Day | Filed | Closed | Open at the day's end |
  |---|---|---|---|
  | 2026-09-21 | 5 | 2 | 3 |
  | 2026-09-22 | 6 | 0 | 9 |
  | 2026-09-23 | 16 | 13 | 12 |
  | 2026-09-24, to 08:53 | 4 | 0 | 16 |

- **Three of the 09-24 filings are on branches, not yet on `main`:** FM-028, FM-029 and FM-030. That makes 31 filed
  against 15 closed, and 16 open. FM-011's close is on #36's branch, not on `main`, and is not counted.
- **Rate:** 11.0 filed a day against 5.3 closed, a ratio of 2.07. The open count grows by about 5.7 a day.
- **The window barely moves the ratio.** From the move (2026-09-22 11:09) to the first measurement (08:26), 1.89 days:
  26 filed against 13 closed — FM-002 and FM-003 closed on 09-21, before it — 13.8 against 6.9 a day, 2.00 to one.
- **Filing to closing takes half an hour to 26 hours** for the 15 that closed; 10 of them take between 2.7 and 7.7
  hours.
- **The pull requests show the same shape,** from 2026-09-23 18:00 to 2026-09-24 08:20: 22 opened, 13 merged.

**What coordinates today:**
- Every commit names its session (FM-024).
- The registry says who is running where.
- Every slice is reviewed before it is called ready.

**What does not:**
- **Nothing orders the streams.** Branches stack on each other without saying so.
- **A carry-over leaves its source pull request open.**
- **The registry is the file every stream conflicts on.**
- **Only the Owner holds the whole queue,** so he is the integrator by default.

**Widened 2026-09-26, a line under the freeze for 0.18.4 (S2, `--queue`):** `--queue` reads an `answer/*` pull request by its
head commit's author, so an answer branch whose head is the Reviewer's docs-pass commit on the answer prints *wait: not an
answerer (reviewer@seat)* — the parent project's PRs 836, 849 and 853, in its pinned queue's line at 21:24:12 on 2026-09-25
and its PR 855 cold review (RV-573, 00:44 on 2026-09-26). The queue must read an answer branch by its answer commit — the
commit that wrote `answer:` — not its head, where only review files follow it. It fits the 0.18.4 cut with a suite case (the
stubbed forge, a review commit on top of the answer): built on `release/0.18.4` in its own commit, before the cut.

**Found 2026-09-26, a line for the next release:** the `[paths] reviews` glob crosses folders and the defaults admit
without a key, so `--queue` can print *merge* over a head no verdict judged — the line under *Open lines* below, filed
on the parent project's RV-630 and its closure test.

## Open lines

**2026-09-28, a line for the queue (S2) — RV-679, the Reviewer seat's (`8e509911/reviewer-42`) on the Owner's own `--done BUG-327` act (PortDive `answer/bug-327`: his `--done` c502c7a4 at 2026-09-27 20:21:18, the verdict 66884f5f at 20:45:02):** a Reviewer's verdict commit on top of his act commit (`--done`, `--due`) turns `--queue`'s line for that pull request from *merge: your answer* into *wait: not an answerer (reviewer@seat)* — `queue_actions` reads the head, and `answered_at` finds the commit under the verdict only for an `answer:` change; an `--answer` branch under a verdict has been read at its answer commit since 0.18.4 (review addenda) and is not affected — and FM-032's signed rule (one docs pass on every answer pull request) makes it happen on every act branch. The fix reads the act commit — the newest `done:`/`due:` change — as `answered_at` reads `answer:`; the queue's reader is critical under path line 3 — a cold Reviewer. Filed by the pass of 2026-09-28; no ask.

**2026-09-26, a line for the next release (S2, `--queue`) — the `[paths] reviews` glob crosses folders, and the default
admits without it; the Implementer seat's (`8e509911/implementer-35`), on the parent project's cold Reviewer session and
its closure test:** 0.18.4 turns the key into a glob by appending `/*` — `queue_actions` builds
`folder = str({…}["reviews"]).strip().strip("/") + "/*"` and matches a path with
`fnmatch.fnmatchcase(x[len(rel) + 1:], folder)` — and `fnmatch`'s `*` crosses `/`. So `reviews = "evidence/*/"` becomes
`evidence/*/*`, and after a verdict it admits every later commit, by any seat and any session, that touches only files
under any `evidence/<id>/` folder — results, data, scripts, not reviews — and `--queue` prints *merge* for a head the
consumer's review gate refuses: the head was not judged. The key cannot be narrowed to review files:
`evidence/*/review*` becomes `evidence/*/review*/*` and matches no `review*.md` file. **The admission is the tool's
default, not only a consumer's key:** with no key at all, `DEFAULTS` reads `"paths": {"reviews": "evidence/reviews/"}`,
and `queue_actions` sets `registry = f"{rel}/sessions.md"` and lets `x == registry` through whatever `[paths]` says — so
after a verdict a later commit by any seat that touches only `evidence/reviews/` (a `note.md` there) or only
`sessions.md` reads *merge* while the consumer's review gate fails it, and no setting in a consumer's configuration
closes the second. **Sources:** the parent project's RV-630 (11:16:13 CEST), in its
`docs/work-tracker/evidence/PD-400/review-pd-400-the-pin-is-0-18-4.md` on its branch `pd/400-the-pin-is-0-18-4`; its
Implementer's closure test at 11:55:26 CEST, X5 and X6, whose run that branch's commit `962a69c4` quotes; and this
seat's reproduction, in a scratch repository of its own on `a7e5291` (`v0.18.4`), never pushed — a READY verdict, then a
commit adding `evidence/x/results.csv` and `evidence/x/run/score.py`: *merge* with `reviews = "evidence/*/"`, *wait: no
verdict on …* with the default; with `evidence/*/review*`, a commit adding only `evidence/x/review-2.md` after the
verdict reads *wait: no verdict* too; with no key, a commit adding only `evidence/reviews/note.md`, or touching only
`sessions.md`, reads *merge*. **The smallest honest fix, this seat's proposal for the next release, not ruled:** the
key's pattern matches one path segment and never crosses `/`, and what the queue admits after a verdict is the verdict
session's own `review*.md` files only, in whatever folder the key names, as the parent's review gate reads them —
`sessions.md` is not a review. **Until then** a consumer's key names no folder that holds non-review files, and no key
closes the `sessions.md` admission.

## Ruled — the rules for a message between two sessions

**Ruled 2026-09-24 21:29:12 by the Owner's signed answer `eef0c2e` (PR 62): *the nine hold as written* — the proposal, the first of two.** Recorded as open the same evening at 19:53 on the Auditor seat's check 18 on v0.18.2 (P2), through the Owner; until then neither ruled nor recorded. Sessions of one account can message each other directly (the harness's peer channel, found 2026-09-23 when two
Principal sessions collided in one worktree); the parent project's fleet wrote eight rules for it that day (its integration plan,
D11), and the fog incident of the morning of 2026-09-24 (its ledger, PR 812 and PR 813) showed the ninth. Signed as written, the nine:

1. A message between sessions carries checkable facts only, re-checked in git before anything moves on it.
2. An agreement exists only as a commit within the hour, with the message quoted; a message alone agrees to nothing.
3. A message is never an answer: *he said yes* moves nothing — an answer is written and signed through the board (path 5).
4. Never a secret, a production read, or one repository's internal state to a session of another repository.
5. `ListAgents` and `git worktree list` before a worktree is taken; one worktree per session, and a badge is not a lock.
6. The seat is in git, never in the frame: a message carries no authority, and a seat's rights come from its commits under `[seats]`.
7. `isolatePeerMachines` is the Owner's setting; no seat changes it.
8. The parent project's scorer (its FEAT-190) reads messages for the four tells the model's System Card names — a fabricated authorization, a proposed destructive
   act, a verdict against its own reasoning, damage disclosed as *a mistake*.
9. **No message to a session the Owner stopped.** A stopped session is not woken by a peer; what it left is read from git (the
   parent project's incident of the morning, PR 812 and PR 813).

## Why

The Owner, 2026-09-24, in chat (spelling normalised): *"Can a human keep up with this? How could we improve here? These
are multiple streams running at the same time doing valuable work — but are they all coordinated?"*

**Why a tracker of its own, not a slice** — held against `considered:` on the Reviewer's R4. FM-024 owns what the
registry means: a seat's commit names its session, and the gate reads the row. S1 changes only where the rows are
stored — one file each, the table generated — so the gate reads the same facts and FM-024's *done when* neither moves
nor gains a line. FM-005 owns the Owner's decisions — the asks, the mandate, the shadow week — and waits on his
calendar (`next: wait`); S2's object is the queue of open pull requests, read from the forge so that *which do I
merge* stops being a question at all — a different object. The three house rules bind the Owner's own habits — how
much waits on him, where he speaks, how he looks at a branch — and belong to neither. The case is weakest for S1: it
edits the code FM-024 built, and a reader looking for the registry's shape looks there first.

## Candidates, cheapest first

Nothing is chosen for the Owner: the Principal's reading below names the slices and puts the three rules to him — they bind him — with a proposal; his answer decides, never a default.

1. **The queue in one view.** The tool reads the open pull requests and gives each one action:
   - *merge*: a verdict names its head, and it merges cleanly;
   - *closes with #N*: its head is inside another open pull request;
   - *close*: it was carried into #N;
   - *wait: conflict in …*;
   - *wait: no verdict on …*;
   - *wait: NOT READY*.

   A seat built exactly this by hand tonight in about two minutes, and the Owner needed it five times. It could be its
   own command or a section of `--standup`.
2. **The registry stops being the conflict.** Either:
   - one file per session, with the table generated; or
   - a merge rule for the table. The catch: closing a session edits its row in place, so a plain union merge would
     keep both the open and the closed version of that row.
3. **Stacked work says so.**
   - A slice built on another slice opens its pull request against that branch, not `main`. The forge then shows only
     the delta, and there is no twin.
   - A carry-over closes its source pull request in the same step.
4. **A limit on work in flight.** No seat starts a new stream while N pull requests wait on the Owner. Tonight's peak
   was 6.
5. **One channel for the Owner.** He speaks to the coordinating session. His rulings are recorded once, where the seats
   read them (the tool's ask and answer), not relayed through chat.
6. **Seats never need the Owner's checkout.** The command that lets him see a branch is `git fetch && git switch
   --detach origin/<branch>`, so his checkout never holds a seat's branch.

**The Principal's reading, 2026-09-24 ≈ 08:33 CEST:** candidates 2 and 1 become slices S1 and S2 of this tracker —
S1: one file per session under `work-tracker/sessions/`, the table generated the way INDEX is, so a merge
regenerates instead of conflicting, and a close edits one file; S2: a `--queue` that reads the forge and gives every
open pull request one action. Candidates 4, 5 and 6 are house rules, not code; they bind the Owner, so they are his
to rule — the ask above. Candidate 3 is deferred. No rule takes effect on a default; each takes effect on his answer.

## Done when

- The Owner can answer *what do I merge, in what order, and what waits on whom* from one command's output, in under a
  minute, without asking a seat.
- A week of parallel streams shows no conflict on the registry, and no pull request left open as a twin.

## Asks

**2026-09-24** · Rule the three house rules — at most 2 pull requests waiting on you per repository, your rulings only to the coordinating session, `git switch --detach origin/<branch>` to look at a seat's branch — and the build order, S1 the registry off the conflict path then S2 the queue in one view?
**answered** — accepted - one channel and the detached switch now, S1 then S2; the cap of 2 waiting pull requests revoked 2026-09-24 · holgo99

**2026-09-24** · Which rules hold for a message between two sessions — the nine recorded as open in this tracker's body, D11's eight and no message to a session you stopped?
**answered** — accepted - the nine hold as written · holgo99
**relation** — accepted the proposal

## Ship log

| Date | Event |
|---|---|
| 2026-09-26 12:08 CEST | The line under *Open lines* widened by the Implementer seat (`8e509911/implementer-35`) on the Principal's brief, with the parent project's closure test (X5 and X6, 11:55:26; its branch `pd/400-the-pin-is-0-18-4`, commit `962a69c4`): the admission is the tool's default too — `evidence/reviews/` by `DEFAULTS`, and `sessions.md` whatever `[paths]` says — and the proposed fix admits the verdict session's own `review*.md` files only; `sessions.md` is not a review. Reproduced once more in the same scratch repository, never pushed: both read *merge* with no key. |
| 2026-09-26 11:57 CEST | The line under *Open lines*, filed by the Implementer seat (`8e509911/implementer-35`) on the parent project's cold Reviewer session, its RV-630 (11:16:13): 0.18.4's `[paths] reviews` key becomes a glob by appending `/*`, and `fnmatch`'s `*` crosses `/` — `evidence/*/` admits every later commit under any `evidence/<id>/` folder, and `--queue` prints *merge* over a head no verdict judged; reproduced once in a scratch repository on `a7e5291` (`v0.18.4`), never pushed. The fix is proposed for the next release, not ruled; no code, CHANGELOG or front-matter change. |
| 2026-09-24 15:17 CEST | R9 of 0.18.0's review, fixed for 0.18.1 by the Implementer: PR 46's merge read *12:53:19* in *What is true now* and *12:53:18* in the 12:55 row. *What is true now* says *12:53:19* (the forge's clock); the 12:55 row stands as written, append-only, and reads 12:53:18 — corrected here, not there. The forge's `mergedAt` (10:53:19Z); `ed11081`'s commit clock says 12:53:18. AGENTS.md's cap paragraph says the same. |
| 2026-09-24 13:05 CEST | `636f56e`, by the Implementer, from the coordinating session's audit of the merged tree: `--queue` lists each branch on `origin` that no pull request carries, after the pull requests, read as a pull request is — `branch <name> @ <sha>  wait: no pull request — …` — and counts them; an `answer/*` pull request reads `merge: your answer` when the Owner signed its head and it verifies, `wait: unsigned answer` when not (PR 46 read *no verdict*); and `--check` tells a signed commit this clone cannot verify that it cannot, where it said *sign it*. |
| 2026-09-24 12:55 CEST | The answer of 11:08:24 superseded by the Owner's own signed edit `7c97c5b` (PR 46, merged 12:53:18): it read *"accepted - all three rules now, S1 then S2"* (`d20bc89`); the new one keeps one channel and the detached switch, S1 then S2, and revokes the cap of 2 waiting pull requests. Written by hand, in place, before 0.18.0's `--supersede` existed; rowed here as that command does from now on. The word *accepted* in front of a partial acceptance is FM-029's pattern, typed by hand this time. |
| 2026-09-24 12:18 CEST | S2 built by the Implementer at `90d3d6f`: `--queue` reads the open pull requests with `gh`, fetches `origin` once, and gives each one action — merge · closes with PR N · close: carried into PR N · wait: conflict in … · wait: no verdict on … · wait: NOT READY (…) — actionable first, oldest first, and a count; `--owner` and `--standup` end with it where the forge can be read. Replayed at the 08:18 heads still reachable (PR 33, 35–38): PR 33 merge, PR 37 closes with PR 33, PR 35 conflict in `sessions.md`, PR 36 no verdict, as read by hand; PR 38 reads *merge* — its rows reached PR 33 as copied text, not as its commits, which the rule does not see. S1 is being built as FM-032's S2 on the other branch. The three rules written into AGENTS.md; the cap of 2 was revoked by the Owner in chat the same day — his signed revocation is owed (`--answer FM-031 … --supersede`, or `revoke`, built on this branch at `bd7d5ea`), and until it is signed no seat counts the cap. |
| 2026-09-24 11:43 CEST | **S1 built as FM-032's S2** at `3c0754f` (0.18.0, branch `fm/032-0-18-0-the-registry-becomes-a-report`), by the Owner's two answers of 2026-09-24: not one file per session with a generated table, but no file — `--sessions` generates the registry from the commit trailers and `sessions.md` is deleted, so two branches that land cannot conflict on it. S2, the queue in one view, is another seat's. |
| 2026-09-24 08:53 CEST | The Reviewer's verdict at `3c72e84` — NOT READY (`bda30ae`, R1 P2, R2–R4 P3) — fixed by the Implementer. R1: filings re-dated by id across both paths, one window from the first filing (2026-09-21 13:13): 31 filed against 15 closed in 2.82 days, 11.0 against 5.3 a day, 2.07 to one, open growing about 5.7 a day; the Reviewer's 1.89-day window re-derived as 26 filed against 13 closed (not 15: FM-002 and FM-003 closed before it), 2.00 to one — *about two to one* stands. R2: 22 sessions under 21 ids. R3: six open by 08:18, not at 08:10. R4: why a tracker of its own, in the body under *Why*. |
| 2026-09-24 08:42 CEST | The Principal sets the proposal — *all three rules now, S1 then S2* — and puts the ask to the Owner (`next: owner`); two wording fixes from the Implementer's report ("None is chosen" read against the reading; the parent project's pull-request numbers written without the sign the forge auto-links). Verified next, then the pull request. |
| 2026-09-24 08:33 CEST | Adopted by the Principal. Candidates 2 and 1 become slices S1 (the registry off the conflict path: one file per session under `work-tracker/sessions/`, the table generated) and S2 (the queue in one view: `--queue`); candidate 3 is deferred. The ask drafted for review (`next: review`): the three house rules — candidates 4, 5 and 6 — and the build order, four options; the proposal is the Principal's to set. The parent project's registry conflict cited by its pull-request numbers only. |
| 2026-09-24 08:26 CEST | The Owner's second question measured: filing outruns closing 2.07 to 1 (16.4 filed a day against 8.0 closed, since 2026-09-22 11:09); 16 open, and the open count grows about 8 a day. |
| 2026-09-24 08:24 CEST | Filed on the Owner's question, with tonight's record as the measurement. Held against FM-005 (his decisions: the asks, not the queue of pull requests), FM-023 (a plan's seats and estimates), FM-024 (a commit names its session) and FM-027 (ids claimed on the server). |
| 2026-09-24 | The nine rules for a message between two sessions recorded as open (the Auditor seat's check 18) and put to the Owner — the parent project's ledger row came first (its tenth-hour commit). Re-made on the Reviewer's R2: the options name no scorer and neither opens with *no*; rule 8 names whose scorer (R6). |
| 2026-09-24 | The row of 20:24 above was edited in place before the branch merged (the pass Reviewer's R10); from here, a correction is an appended row. |
| 2026-09-24 | Answered 21:29:12 (`eef0c2e`, PR 62, one Reviewer docs pass on the answer branch under his FM-032 answer): *the nine hold as written* — the proposal. The exchange cleared as acted on: the nine stand in the body as ruled; `next: wait` for the week of parallel streams. |
| 2026-09-24 | Found the same evening, a line under the freeze for 0.18.4 (S2, `--queue`): `pushed_branches` leaves `answer/*` out by design, so his own three answers, pushed by `--answer` at 21:27–21:32 and opened as pull requests only at 21:44 on the Principal's word in chat, read *0 waiting on you* — an answer branch without a pull request waits on his press and belongs in the queue as *merge: your answer — open its pull request*. |
| 2026-09-25 | The Auditor seat's AU-28 on PR 64, through the Owner (06:52:21): the nine rules were in this body only, not in the contract — the same burying as its AU-1 on FM-033's rule. Fixed in the pull request before its merge: the nine stand in `AGENTS.md`'s *How the loop runs*, beside FM-031's other rules, naming `eef0c2e`. Its AU-29 (the `## Asks` record names no signing commit) is a 0.18.4 line in FM-029. |
| 2026-09-25 | The Reviewer's R4 on PR 64: the contract's bullet had paraphrased the nine; it now carries them in this body's own words. R5: the approximated times replaced by the transcript's — the Auditor's AU-28 and AU-29 relayed in one message at 06:52:21 (this row's first version claimed two replacements and cited 07:00:34, which names neither finding; corrected in place while unmerged, the Reviewer's R6). |
| 2026-09-26 | A line for 0.18.4 under the freeze (S2, `--queue`), the widening above: an answer branch whose head is the Reviewer's docs-pass commit read *wait: not an answerer (reviewer@seat)* — the parent's PRs 836, 849 and 853, its pinned queue's line at 21:24:12 on 2026-09-25 and its PR 855 cold review (RV-573, 00:44). The queue reads an answer branch by the commit that wrote `answer:`, not its head; 0.18.4 builds it on `release/0.18.4`, its own commit, with a suite case. |
