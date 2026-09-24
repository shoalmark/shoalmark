---
id: FM-032
status: In Progress
considered: FM-031, FM-024, FM-027, FM-005
tags: process
next: wait
triaged: 2026-09-24
rank: 9
tier: P2
hook: "The loop — a session row, a Reviewer pass, fixes, re-verification, merges of main — costs the same for a docs row as for a change to the gate. This morning a bug filing with no code in it paid three merges of main after verdicts, each conflicting on the registry. The Owner asked whether shoalmark's good intentions are turning into a bureaucratic nightmare."
---

# FM-032 — the loop costs the same for a docs row as for a migration — overregulation, named by the Owner

## What is true now

**Ruled 2026-09-24 11:07:43 CEST by the Owner's signed answer `ffa63b8` (PR 44): *all four now*.** Built for 0.18.0 on
this branch, the same day: S2, the registry as a report from the commit trailers (`3c0754f`; it is FM-031's S1 by the two
answers); S4, the filing freeze at 8 with `--tags` on `--new` (`43e6815`, `66f4b7b`); S1 the review tier and S3 the miss
threshold written into AGENTS.md as rules (`fbc2697`). The tier and the miss rule apply from the ruling; the first
pull request under the tier was the parent project's ledger, one pass, P3 fixed forward. The ask is cleared below as
acted on; the Owner tags the release.

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

## Asks

**2026-09-24** · Rule the deregulation: one Reviewer pass for docs and ledgers, findings below P2 fixed forward, no re-pass; the registry a report generated from commit trailers, not a gate; a miss rowed only if it cost you a command or a decision; a filing freeze except product defects until the open count falls?
**answered** — accepted - all four now · holgo99

## Ship log

| Date | Event |
|---|---|
| 2026-09-24 12:45 CEST | The two 0.18.0 branches merged by the Principal: S2 (`a2956a5`, the registry as a report) with `--queue`, the freeze and `--tags`, the rules in AGENTS.md, `--answer` after an earlier answer and revoke/supersede (`66f4b7b`). Conflicts: the dispatch in `shoalmark.py`, README §5's refusal table, FM-031's ship log, INDEX regenerated, `sessions.md` stays deleted. Gates and both suites green on the merged tree. The ask cleared as acted on, next move `build`: the Owner tags, the parent project vendors. The Reviewer takes the code loop next. |
| 2026-09-24 11:43 CEST | **S2 built** for 0.18.0 at `3c0754f` (docs `6a14704`, VERSION and CHANGELOG `2fcd15b`) on `fm/032-0-18-0-the-registry-becomes-a-report` — by the Owner's two answers of 2026-09-24 (here *all four now*, on FM-031 *all three rules now, S1 then S2*) it is FM-031's S1 as well, one design. **The report:** `--sessions` reads the `Session:` trailers of the checkout's history (`git log` of HEAD) — per id its seat through `[seats]`, first and last commit, how many commits, and its worktree from a `Worktree:` trailer the hook now appends beside `Session:` (`—` before); the board's strip and the digest read it (the sessions with a commit in the last day). `work-tracker/sessions.md` is deleted; `--check` warns where one is left. **The gate** keeps one rule: a seat's commit carries a `Session:` of the shape `<8 hex>[/<seat>-<n>]` whose seat part is its own; a commit whose history has no `Session:` is not judged (adoption moved from the file to the first trailer). **Removed:** `--session open` and `close` (one line, exit 2), the open-row check, the worktree clash, the removal, drop and re-open judgement, abandoned rows in `--check` and `--triage`. Checks 264 + 148 → 266 + 148. |
| 2026-09-24 09:48 CEST | Verified READY WITH FINDINGS at `db15a31` (R1–R5, all P3); closed in the text before the ask reaches him because two touch what he answers: R3 — the freeze's number is 8, half of today's 16, carried by *all four now*; R4 — FM-031's S1 is read as this S2, one design; R1 the -15 instance; R2 the parent's hash gone; R5 *a fifth, like for like*. One more pass, the last. |
| 2026-09-24 09:39 CEST | The Principal sets the proposal — *all four now* — and puts the ask to the Owner (`next: owner`), on his ruling of ≈ 09:19 that the proposal becomes an ask. Main after PR 35 merged in first. Verified next, then the pull request. |
| 2026-09-24 09:30 CEST | Filed on the Owner's question (≈ 09:12), and on his word at ≈ 09:19 that the Principal's proposal becomes an ask. The evidence is re-derived from git and the forge; the seven passes, the parent project's two docs-only branches (four passes, about 800K tokens, 75 minutes) and the Principal's four catches are marked *reported*. The ask is drafted (`next: review`, four options, trimmed to 298 characters: *the session registry* is now *the registry*, *docs and ledger changes* is now *docs and ledgers*). The proposal is the Principal's. Held against FM-031 (the fan-out; its S1 is refined here into a report), FM-024 (the registry as a gate), FM-027 (ids claimed on the server, moot under S2) and FM-005 (the Owner's decisions). |
