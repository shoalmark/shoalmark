---
id: FM-032
status: In Progress
considered: FM-031, FM-024, FM-027, FM-005
tags: process
triaged: 2026-09-24
tier: P2
next: build
ask: "After a READY WITH FINDINGS verdict, how does a fix of its findings reach main without a second Reviewer pass?"
ask-kind: ruling
ask-since: 2026-09-28
ask-options: "the Auditor's S5: exact fix texts, a decision file per finding; the gate covers a commit whose diff is just those texts | a docs verdict with only sub-P1 findings and exact fixes reads READY WITH FINDINGS; no fix commit before the merge | as today: every commit after a verdict is a new head; the same seat re-checks the lines the finding names"
ask-proposal: "the Auditor's S5: exact fix texts, a decision file per finding; the gate covers a commit whose diff is just those texts"
answer: "accepted - the Auditor's S5: exact fix texts, a decision file per finding; the gate covers a commit whose diff is just those texts"
answered: 2026-09-28
answered-by: holgo99
hook: "The loop — a session row, a Reviewer pass, fixes, re-verification, merges of main — costs the same for a docs row as for a change to the gate. This morning a bug filing with no code in it paid three merges of main after verdicts, each conflicting on the registry. The Owner asked whether shoalmark's good intentions are turning into a bureaucratic nightmare."
---

# FM-032 — the loop costs the same for a docs row as for a migration — overregulation, named by the Owner

## What is true now

**2026-10-01 — one full local run before a pull request opens (the Owner's ruling):** the suites run in full once on a branch's final tip before its pull request opens, not per commit; a later commit that adds only a review file needs none — CI covers it; never between 00:00 and 02:00 CEST until FM-028 is fixed; CI on the pull request stays the full pass.

**Ruled 2026-09-24 11:07:43 CEST by the Owner's signed answer `ffa63b8` (PR 44): *all four now*.** Built for 0.18.0 on
this branch, the same day: S2, the registry as a report from the commit trailers (`3c0754f`; it is FM-031's S1 by the two
answers); S4, the filing freeze at 8 with `--tags` on `--new` (`43e6815`, `66f4b7b`); S1 the review tier and S3 the miss
threshold written into AGENTS.md as rules (`fbc2697`). The tier and the miss rule apply from the ruling; the first
pull request under the tier was the parent project's ledger, one pass, P3 fixed forward. The ask is cleared below as
acted on; the Owner tags the release. The path-3 ask of the same day (kind action, answered 21:32:35, signed `97fa87a`)
was cleared on 2026-09-28 by `--clear-ask FM-032 build`: its act is done — the Owner's own hands wrote the exception into
TRIAGE.md's path 3 in `fe36cc0` (2026-09-25 11:14:26, signed G); the record below keeps the answer's lines, the act's result is that commit.

**2026-09-28 — the ask of this pass (PortDive ledger row 54 first, 06:45:49):** the Owner's question of 02:07:38 (normalised): *"if we have these READY WITH FINDINGS, wouldn't it be good to forward-fix those with a commit before the merge that does not require another Reviewer run? The findings shall be verified first, graded, and then, based on confidence score with threshold and rationale, decided if this issue is fixed or left open as no-fix?"* (his two sentences after *Question:*; spelling and punctuation normalised, no word dropped or added) — asked after FM-040's filing took four commits and two re-checks for P3s (37 min, first verdict 02:00:26 to last re-check 02:37:10) and, later that morning, two ledger rows three passes (17 min 33 s by the same measure, 06:07:40 to 06:25:13). The Auditor's checks and design, relayed by the Owner 02:33:25, word for word (sha256 of the filed text `06ea1596923a9358b342888b05a9c9de7e2202b6247632a4bbeba61dfbbb5749`; its first character is missing in his paste and kept so):

> he Owner's question on READY WITH FINDINGS, with the Auditor's checks (2026-09-28, about 02:30 CEST):
> 1. Confirmed: a commit after a verdict that touches more than review files reads `wait: no verdict` (shoalmark's queue_actions / addenda_only; PortDive's review_gate at f101aeaa).
> 2. Ledger 28 is not the example: its passes were NOT READY, NOT READY, READY, on P2s (RV-667, RV-668, RV-676; grade confidence 0.6–0.7). The proposal as asked saves none of them.
> 3. The design for the ask, as slice S5 on FM-032 (the freeze holds at 20 open):
>    - the Reviewer writes each fix as exact old → new text;
>    - the author records, per finding, fixed / forward / no-fix / rejected, with confidence and a reason, in a review-folder file;
>    - after READY WITH FINDINGS, the gate covers a commit only when its diff is exactly the fixed findings' texts, in docs files only, and it names the verdict. "Files the verdict names, small diff" is too loose: RV-673's fix said only "a line on F84", and the new line carried a wrong time;
>    - below P2 the author decides; a no-fix or rejection at P2 or above goes to the Reviewer (a scoped check) or to the Owner;
>    - the threshold is his (counsel: 0.9).
> 4. A second option for him: a docs verdict whose findings are all below P1, with exact fixes, is READY WITH FINDINGS, not NOT READY.
> 5. The decision file can start now as a convention. The gate change is critical (shoalmark, and PortDive's scripts/review_gate.py): the full loop and a cold Reviewer. The Auditor seals a plan before the build.
> 6. The filing freeze: no lift needed for this. If he asks, an ask on FM-032 about freeze_at (keep 8 / raise / off / parked not counted).
> 7. BUG-327, holgo99/portdive-monorepo, branch bug/327-the-act-done-the-exchange-cleared @ b4645c0d: review_gate passes (2 commits past 3de57f54, review files only).

The Principal's counsel, disclosed as such: the first option — S5 as the Auditor designed it, the threshold his (its counsel 0.9); the decision file may start as a record without a tool change; the gate change (shoalmark's `queue_actions`/`addenda_only` and PortDive's `scripts/review_gate.py`) is critical under path line 3 — the full loop and a cold Reviewer, the Auditor sealing its verification plan before the build. Nothing is acted on before his answer.

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

## The records-to-product ratio — the Owner's concern of 2026-09-30

The Owner, 2026-09-30, *normalised*: 06:54:04 *"The records-to-code ratio shall become our main concern now. These numbers must even
out or invert."*; 07:04:27 *"We shall track added lines vs deletions — so separately."* and *"If a check output regenerates, keep
only its summary; if it doesn't, it stays in git."*; 07:14:05 *"We split."*; 07:21:58 *"Go, freeze excepted."*; 19:16:21 *"an output is replaced by a summary and a check only where it is larger than the two together"*, and the Jev
scorer's output (`jev-gate-test-score-output-2026-09-23.txt`, 44 lines) stays on main as it is. The definition is
filed on its own page, public and with no other project's numbers: `work-tracker/evidence/FM-032/records-to-product-ratio.md`.

**Decisions**, graded by the Principal and taken by the Owner (decisions, not quotations):
- The ruling is applied here: the summary of a regenerable check output is the command, the tested commit, the environment, the
  pass and fail counts and the failing check ids, plus a committed check that proves regeneration; an output that does not
  regenerate stays and counts. **Their condition of 19:16:21:** *"an output is replaced by a summary and a check only where it is larger than the two together"*; by the same word the Jev scorer's output stays on main as it is,
  and the large JSONs of this branch stay replaced.
- D9 is in force: a verdict names the reviewed commit, base, tier and checks, through the `Reviewed:` trailer that FM-024's S6 reads.
- D1 (no review file outside a critical tier) changes S1, the Owner's signed rule, is not yet asked: its ask is placed on this tracker after this branch merges and the exchange is cleared — not built here.

**What this slice builds:** the page; `--ratio`, their explicit exception to the filing freeze (*"Go, freeze excepted."*); the ruling
applied to the regenerable outputs, each replaced by its summary in its README; and the committed regeneration check
(`SHOALMARK_REGENERATE=1`). **What stays in git, and why:** `browser-fonts.json` (no committed command), `results.json` (a CI read-back), `scanned-refs.txt`, the six
`jev-*` request, response and key files (an external service's exchange), the two `requests.json` (FM-002 slice A's and the start page's:
`render.mjs` writes them from a Chrome run, but no committed check regenerates them and they hold that run's network and page measures, so
they stay until one does) and the triage page's `demo.out` and `demo-de.out` (`demo.sh` makes fresh keys and times on every run, so a run
never repeats its ids, and the script's own header says `docs/triage.md` quotes them) do not regenerate from git, so they stay and count. **The Jev scorer's output stays, by the Owner's word of 19:16:21:** `jev-gate-test-score-output-2026-09-23.txt` regenerates from the committed
scorer; the Owner took it out of this branch (19:16:21), so it stays on main as it is, with no block or check.

**PR 131 as merged** (`c525a41^1..c525a41`, by the page's rule, renames off): records +699 −33,529, product +538 −9, 1.3:1. The page's *own numbers*
(543 / 547, against `7e7c8ac`) are an earlier tip's and stay as filed.

## Done when

- A docs change merges with one Reviewer pass.
- Two branches landing never conflict on the registry.
- The open count falls for a week.

## Asks

**2026-09-24** · Rule the deregulation: one Reviewer pass for docs and ledgers, findings below P2 fixed forward, no re-pass; the registry a report generated from commit trailers, not a gate; a miss rowed only if it cost you a command or a decision; a filing freeze except product defects until the open count falls?
**answered** — accepted - all four now · holgo99

**2026-09-24** · How does an answer pull request — your signed answer and nothing else — pass path 3, which lets no pull request merge without a review file?
**answered** — accepted - one Reviewer docs pass until FM-007's hardware key signs your answers, the signature alone after — written into path 3 · holgo99
**relation** — accepted the proposal
**signed** — 97fa87a · G

## Ship log

| Date | Event |
|---|---|
| 2026-09-30 19:21 CEST | **The Owner's condition on the check-output rule (19:16:21):** *"an output is replaced by a summary and a check only where it is larger than the two together"*; the Jev scorer's output, its summary block and its check come out of the branch (`b1a7b41`) — the output stays on main as it is. The rule's places (this section, the page, the CHANGELOG) say so in the next commit. |
| 2026-09-30 09:48 CEST | **The Reviewer's code pass on `b52437a` (NOT READY, `13cdf7d`): its four findings fixed** on the merge of `origin/main` (`bd34852`, `186c589`). RV-726 and RV-727 (`8316a96`): `[ratio] records` defaults to the configured tracker directory, a scalar `records`/`exclude` is one refused line (exit 2), the trunk is `origin/HEAD`'s target through `default_trunk`, and the first-parent line and the default window are planted in the tests. RV-728 (`4ebb488`): slice A's ten controls are counted (24 checks), the summaries state their units (verdicts; measurements apart), and the `requests.json` and `demo*.out` files that stay are named with their reasons — (a), the Jev score output, which the ruling reaches, is not yet applied. RV-729 (this commit): the ruling's time (07:23:33), the page reflowed, the committer day and no rename detection said, D1 not yet asked. |
| 2026-09-30 07:5x CEST | **Built on the Owner's concern of 06:54:04 and his ruling of 07:04:27**, as one change on `fm/032-the-ratio-command-and-the-check-outputs-rule` — an explicit exception to the freeze (his 07:21:58): the definition page and this section (`991f978`); `--ratio` with `[ratio]` in `shoalmark.toml` (`3deafb9`); the four regenerable check outputs replaced by their summaries in their READMEs, each held in git at the commit named there (`c819cde`); the regeneration check, `facts.mjs` always and the browser checks behind `SHOALMARK_REGENERATE=1` (`c3d56ec`). The page's own numbers are the change's, from the rule. |
| 2026-09-24 12:45 CEST | The two 0.18.0 branches merged by the Principal: S2 (`a2956a5`, the registry as a report) with `--queue`, the freeze and `--tags`, the rules in AGENTS.md, `--answer` after an earlier answer and revoke/supersede (`66f4b7b`). Conflicts: the dispatch in `shoalmark.py`, README §5's refusal table, FM-031's ship log, INDEX regenerated, `sessions.md` stays deleted. Gates and both suites green on the merged tree. The ask cleared as acted on, next move `build`: the Owner tags, the parent project vendors. The Reviewer takes the code loop next. |
| 2026-09-24 11:43 CEST | **S2 built** for 0.18.0 at `3c0754f` (docs `6a14704`, VERSION and CHANGELOG `2fcd15b`) on `fm/032-0-18-0-the-registry-becomes-a-report` — by the Owner's two answers of 2026-09-24 (here *all four now*, on FM-031 *all three rules now, S1 then S2*) it is FM-031's S1 as well, one design. **The report:** `--sessions` reads the `Session:` trailers of the checkout's history (`git log` of HEAD) — per id its seat through `[seats]`, first and last commit, how many commits, and its worktree from a `Worktree:` trailer the hook now appends beside `Session:` (`—` before); the board's strip and the digest read it (the sessions with a commit in the last day). `work-tracker/sessions.md` is deleted; `--check` warns where one is left. **The gate** keeps one rule: a seat's commit carries a `Session:` of the shape `<8 hex>[/<seat>-<n>]` whose seat part is its own; a commit whose history has no `Session:` is not judged (adoption moved from the file to the first trailer). **Removed:** `--session open` and `close` (one line, exit 2), the open-row check, the worktree clash, the removal, drop and re-open judgement, abandoned rows in `--check` and `--triage`. Checks 264 + 148 → 266 + 148. |
| 2026-09-24 09:48 CEST | Verified READY WITH FINDINGS at `db15a31` (R1–R5, all P3); closed in the text before the ask reaches him because two touch what he answers: R3 — the freeze's number is 8, half of today's 16, carried by *all four now*; R4 — FM-031's S1 is read as this S2, one design; R1 the -15 instance; R2 the parent's hash gone; R5 *a fifth, like for like*. One more pass, the last. |
| 2026-09-24 09:39 CEST | The Principal sets the proposal — *all four now* — and puts the ask to the Owner (`next: owner`), on his ruling of ≈ 09:19 that the proposal becomes an ask. Main after PR 35 merged in first. Verified next, then the pull request. |
| 2026-09-24 09:30 CEST | Filed on the Owner's question (≈ 09:12), and on his word at ≈ 09:19 that the Principal's proposal becomes an ask. The evidence is re-derived from git and the forge; the seven passes, the parent project's two docs-only branches (four passes, about 800K tokens, 75 minutes) and the Principal's four catches are marked *reported*. The ask is drafted (`next: review`, four options, trimmed to 298 characters: *the session registry* is now *the registry*, *docs and ledger changes* is now *docs and ledgers*). The proposal is the Principal's. Held against FM-031 (the fan-out; its S1 is refined here into a report), FM-024 (the registry as a gate), FM-027 (ids claimed on the server, moot under S2) and FM-005 (the Owner's decisions). |
| 2026-09-24 | Asked, kind action — a yes writes path 3, which only the Owner's hands write (the Reviewer's R3, this branch's own FM-030 line): how an answer pull request passes path 3 (the Auditor seat's check 21; its AU-11 on the seat's first proposal — the signature alone is what any process on the account can produce until FM-007's key) — the parent project's ledger row came first. #10 freed to FM-034 by the evening re-run of the pass: a wait ranks after the builds. |
| 2026-09-24 | The row of 20:24 above was edited in place before the branch merged (the pass Reviewer's R10); from here, a correction is an appended row. |
