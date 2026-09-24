---
id: FM-032
status: Proposed
considered: FM-031, FM-024, FM-027, FM-005
tags: process
next: owner
ask: "Rule the deregulation: one Reviewer pass for docs and ledgers, findings below P2 fixed forward, no re-pass; the registry a report generated from commit trailers, not a gate; a miss rowed only if it cost you a command or a decision; a filing freeze except product defects until the open count falls?"
ask-kind: ruling
ask-since: 2026-09-24
ask-options: "all four now | the review tier and the freeze now, the registry and the miss rule later | the review tier only | none — keep the loop as it is"
ask-proposal: "all four now"
hook: "The loop — a session row, a Reviewer pass, fixes, re-verification, merges of main — costs the same for a docs row as for a change to the gate. This morning a bug filing with no code in it paid three merges of main after verdicts, each conflicting on the registry. The Owner asked whether shoalmark's good intentions are turning into a bureaucratic nightmare."
---

# FM-032 — the loop costs the same for a docs row as for a migration — overregulation, named by the Owner

## What is true now

**Filed 2026-09-24 09:30 CEST on the Owner's question. Nothing is built. The four measures below are a draft ask
(`next: review`); the proposal is the Principal's to set.**

**The loop** is what every change pays here: a session row opened, the work, the gate, a Reviewer pass, fixes, a
re-verification, a merge of `main` whenever it moved, the row closed. It costs the same whatever the change risks.
The evidence, from git and the forge on 2026-09-24 in the morning, unless marked *reported*:

- **A change with no code pays the full loop.**
  - In the parent project that vendors this tool, its ledger pull request 807 needed seven Reviewer passes before
    READY (*reported*). The forge shows that every file it changed sits under its `docs/work-tracker/`, and that 11 of
    its 29 commits are the Reviewer's: eight on the branch's own work (seven before the last READY), three
    on a second tracker the branch carried. It merged at 08:50 CEST.
  - Here, PR 35 (FM-028, a bug filing) changes four files: the tracker, its review, `INDEX.md` and `sessions.md`. It
    took 11 commits: 6 Implementer, 3 Reviewer verdicts and 2 merges by the Principal.
- **Two docs-only branches cost four Reviewer passes, about 800K tokens and 75 minutes** (*reported by the parent
  project's second Principal session*). In the parent project that vendors this tool, two docs-only branches took four
  Reviewer passes this morning: about 800K sub-agent tokens in total (174K, 211K, 194K, 224K) and about 75 minutes of
  wall time. The passes found real errors: a false "new fact" in a re-ask, wrong dates, paraphrased Owner lines, a name
  leak into this repository. They also found about ten P3 wording items that changed nothing the Owner would decide.
- **The registry conflicts whenever two branches land.** PR 35 merged `main` three times after a verdict on it.
  Replayed with `git merge-tree` on each merge's two parents:

  | Merge | When, by whom | After | Conflicts in |
  |---|---|---|---|
  | `64f7b99` | 08:58, the Implementer, fixing the NOT READY | `30c4f89`, NOT READY | `sessions.md`, `INDEX.md` |
  | `f8ccf60` | 09:07, the Principal, before the re-verdict | `30c4f89`, NOT READY | `sessions.md` |
  | `3131e8c` | 09:21, the Principal | `6a9fa8f`, READY TO TAG | `sessions.md`, `INDEX.md` |

  Each was resolved by hand, as a union. The third needed another verdict, `5dcc854` (09:24), the pull request's
  third, to say that the merge brought only `main`'s files.
- **A closed row never re-opens, so every return to a branch costs a new id.** The gate refuses a re-open
  (`shoalmark.py:2626` at `9bde71f`). So a seat that comes back to fix findings or to merge `main` opens a new session:
  - `8e509911/implementer-12`: PR 35's R1 and R2, and a merge of `main`. Five commits from 08:57 to 09:00: an open,
    three of work, a close.
  - `8e509911/implementer-13`: FM-031's R1–R4. Three commits from 08:50 to 08:56: an open, one of work, a close.

  This filing is `-14`. The Principal's own merges (`f8ccf60`, `3131e8c`) ran under its open row and needed none. Its
  Implementer's one-merge follow-up, after `-14` had closed, would have needed a new id: `-15` was made locally, never
  pushed, and the merge ran under the Principal's open row instead (*reported by that Implementer*).
- **A guessed id needed a simulation and a ruling.** The gate keys the rows by id (`now_by_id = {r["id"]: r for r in
  rows}`, `shoalmark.py:2621`). Two rows under one id therefore read as one row. Once both branches are on `main` and
  one of the two rows is still open, that reads as a re-open (`:2626`). `8e509911/implementer-6` was guessed on a
  branch at 07:41 and already named the site slice's session from 01:02. FM-028's ship log, on PR 35's branch, records
  what that cost:
  - the Reviewer's R1 (`30c4f89`, P2);
  - a ruling by the Principal: the registry is append-only, so the duplicate is recorded in its row and the row closed;
  - a simulation against PR 33's tip `f2cc7bd`: `--session-check` 4 with the row open, 0 with both closed;
  - an archive ref that spawned a twin pull request, 41.
- **Filing outruns closing about two to one** (FM-031's record, to 08:53): 11.0 filed a day against 5.3 closed, over
  2.82 days, with 16 open. FM-011 has shipped since (PR 36), and this filing makes it 16 again.
  - Of the 15 that were open before this filing (on `main` and on PR 34's and PR 35's branches), 4 carry `tags: bug`.
    The rest: 7 `research`, 2 `process`, 1 `security`, 1 untagged.
  - Most of what is filed is about the tool's own process (asks, answers, sessions, seats, plans), not a defect a
    consumer meets. That is the Principal's reading; the tags are the measure.

**What the rigor caught this morning, before it reached the Owner** (the Principal, *reported*):
- a misread ask;
- a filing rate overstated by about a fifth, like for like (FM-031's first 16.4 a day against 13.8 in the same window;
  11.0 a day over the full window);
- a NOT READY shown on the wrong pull request by the forge's cross-linking;
- a registry that breaks `main` when two branches merge (FM-028's ship log).

## Why

The Owner, 2026-09-24, in chat (spelling and idiom normalised):
- ≈ 09:12: *"Are we on the verge of turning shoalmark's good intentions into a bureaucratic nightmare?"*
- ≈ 09:19: *"I want your previous proposal to become an ask — yes. This is the first step in the right direction:
  spotting and fixing overregulation."*

The Principal's answer, ≈ 09:15 (*reported*): yes, at the edge. The line is that the loop applies the full cost to
every change, whatever its risk. What earns its keep is the four catches above. So the measures below keep the loop
where the risk is, in code, and take it off where it is not.

**Why a tracker of its own** — held against `considered:`:
- **FM-031** rules on the fan-out: the WIP cap, one channel for the Owner, the detached switch; S1 the registry off the
  conflict path, S2 the queue in one view. This tracker is about what the loop costs per change, not how many changes
  run at once. FM-031's S1 is refined here: not one file per session with a generated table, but a report generated from
  the commit trailers, with no gate on open and closed rows (S2 below). For his answer: FM-031's first option says *S1
  then S2*. A ruled FM-031 S1 waits for this ask. If S2 here is ruled, it is FM-031's S1 as well, one design: the design
  decided here, the order there. If he rules *the registry later* or *none* here, FM-031's S1 is built as FM-031 wrote
  it, per-session files with a generated table.
- **FM-024** built the registry as a gate with open and closed rows. This asks to make it a report generated from the
  commit trailers. FM-024's core stays: every seat's commit names its session. What goes is the gate on the row.
- **FM-027** claims the next free id on the server. That is moot if the registry is a report: a duplicate id stops
  being a refusal on `main` and becomes a line the report shows (one id, two worktrees).
- **FM-005** owns the Owner's decisions: the asks, the mandate, the shadow week. This puts one ruling to him through
  that machinery and does not change it.

## The four measures, as slices

Each takes effect on the Owner's answer, never on a default.

**S1: review tiers.**
- *What changes:* a change that touches only trackers, their evidence and the documentation gets one Reviewer pass.
  That means no `shoalmark.py`, no test, no configuration and no hook.
  - Findings below P2 are fixed forward in the next change, with no re-pass.
  - A P2 or above sends it back, as today.
  - Code keeps the full loop: pass, fix, verify, until READY.
  - The rule goes into AGENTS.md; the Reviewer reads the tier from the diff (`git diff --name-only origin/main...HEAD`).
- *What it costs:*
  - A P3 wording error can reach `main` and stand there until the next change.
  - A docs change that alters what the gate reads (a front-matter key, `shoalmark.toml`) is code, and the Reviewer has
    to say so.
  - On PR 35, the verdict `5dcc854` on a merge of `main` would not have been asked for.

**S2: the registry becomes a report.**
- *What changes:*
  - `sessions.md` is no longer written by hand and is no longer a gate. It is generated from the `Session:` trailers in
    `git log`, the way INDEX is from the trackers: each id's first and last commit, its seat, its worktree.
  - `--session open` and `--session close` go, and so do the refusals of a re-open and of a second session in one
    worktree.
  - The trailer rule stays: a seat's commit without a `Session:` is still refused.
- *What is kept of FM-024:*
  - every seat's commit names its session;
  - a verdict's independence (the same root or not) is already read from the trailers;
  - who ran what, and when, is in the report.
- *What is lost:*
  - the refusal of a second session in one worktree;
  - *convened by* and *scope* stop being a row the gate reads (they could ride as trailers on a session's first commit);
  - a session ends at its last commit, so an open row that nobody closed stops being a thing.
- *What it costs:* INDEX is generated too, and it still conflicted on two of PR 35's three merges (`64f7b99`,
  `3131e8c`). A generated file that is committed conflicts. So the report is either not committed at all (printed by a
  command, and on the git-ignored board), or it is committed with a merge rule that regenerates it. The first is
  cheaper. This slice takes in FM-031's S1 and makes FM-027 moot.

**S3: the miss threshold.**
- *What changes:* a miss is a seat's own error, found after it was made. It gets a row (a ship-log line, a tracker, a
  pitfall) only if it cost the Owner a command or a decision. Otherwise it is fixed, and the fixing commit's message
  says what was wrong: git is its record.
- *What it costs:*
  - A miss that costs nothing but recurs is seen late.
  - The record that FM-025 would read to know which rules burn gets thinner.
  - Nothing is built: it is a rule in AGENTS.md.

**S4: the filing freeze.**
- *What changes:* while the open count is at or above **8** — half of the 16 open at filing, the number that *all four
  now* carries; he may name another in his answer — only product defects are filed: `tags: bug`, something the tool does
  wrong for the person using it. Anything else goes as one line into the closest open tracker's body (AGENTS.md rule 6),
  or waits.
- *Optional code:* `--new` refuses a tracker without `bug` while the count is over the line, and says what the count is.
- *What it costs:*
  - A real process problem waits, or rides as a line in another tracker. This tracker would not have been filed under
    the freeze.
  - The number is the Owner's to set: 15 were open before this filing.

## Done when

- A docs change merges with one Reviewer pass.
- Two branches landing never conflict on the registry.
- The open count falls for a week.

## Ship log

| Date | Event |
|---|---|
| 2026-09-24 09:48 CEST | Verified READY WITH FINDINGS at `db15a31` (R1–R5, all P3); closed in the text before the ask reaches him because two touch what he answers: R3 — the freeze's number is 8, half of today's 16, carried by *all four now*; R4 — FM-031's S1 is read as this S2, one design; R1 the -15 instance; R2 the parent's hash gone; R5 *a fifth, like for like*. One more pass, the last. |
| 2026-09-24 09:39 CEST | The Principal sets the proposal — *all four now* — and puts the ask to the Owner (`next: owner`), on his ruling of ≈ 09:19 that the proposal becomes an ask. Main after PR 35 merged in first. Verified next, then the pull request. |
| 2026-09-24 09:30 CEST | Filed on the Owner's question (≈ 09:12), and on his word at ≈ 09:19 that the Principal's proposal becomes an ask. The evidence is re-derived from git and the forge; the seven passes, the parent project's two docs-only branches (four passes, about 800K tokens, 75 minutes) and the Principal's four catches are marked *reported*. The ask is drafted (`next: review`, four options, trimmed to 298 characters: *the session registry* is now *the registry*, *docs and ledger changes* is now *docs and ledgers*). The proposal is the Principal's. Held against FM-031 (the fan-out; its S1 is refined here into a report), FM-024 (the registry as a gate), FM-027 (ids claimed on the server, moot under S2) and FM-005 (the Owner's decisions). |
