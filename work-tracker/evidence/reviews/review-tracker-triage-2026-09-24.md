# Review — the triage pass of 2026-09-24, at 7d3e632 (2026-09-24 15:12 CEST, Reviewer, session `8e509911/reviewer-1`)

- **Branch:** `tracker/triage-2026-09-24`, tip `7d3e632` (`7d3e632256d72339981e81f401d74e900a003dd2`), one commit on
  `origin/main` `095f1d3` (PR 49's merge, `v0.18.0`), by the principal seat (`principal@seat`, `Session: 8e509911`,
  `Worktree: shoalmark-principal`): the worksheet, the front matter the command wrote, the by-hand finishes for FM-024
  (`fix`) and FM-026 (`merge FM-004`), the paragraph under *Passes*, INDEX.
- **Tier: docs, one pass.** `git diff --name-only origin/main...HEAD` names 14 files, all under `work-tracker/`: ten
  trackers, FM-004, INDEX, TRIAGE.md and the worksheet. No `shoalmark.py`, no test, no configuration, no hook, no new
  key. P3 is fixed forward; P2 or above sends it back.
- **Independence:** same session `8e509911`. The author is the root session; this seat is its sub-session. Reported,
  not refused. `--check` will count this verdict as *same session*.

## What I ran

| run | result |
|---|---|
| `python3 shoalmark.py --triage` | exit 0: *0 trackers to judge*, *Applied nothing — no new filled rows*; `git status --porcelain` empty before and after |
| `python3 shoalmark.py --check` | exit 0; the freeze line: *14 open, at or above 8 — only bug filings* |
| `python3 shoalmark.py --session-check` | exit 0 |
| `python3 shoalmark.py` | 32 trackers, 0 unknown-status; `git status --porcelain` empty, so INDEX is the generated one |
| `python3 shoalmark.py --next` | ranks #1 … #9 as below; `START WITH: FM-029`; *NOTHING NEEDS THE OWNER* |
| `test_shoalmark.py` | exit 0, 285 ok, all green (Python 3.14.3) |
| `test_core.py` | exit 0, 148 ok, all green |
| `git diff origin/main -- work-tracker/TRIAGE.md` | two lines added under *Passes*, the new paragraph and a blank line; the intent and the path byte-identical |
| a clone of this worktree in the scratchpad, detached at `095f1d3`, `--triage` run there | its fresh worksheet equals the branch's in every cell but Verdict and Reason (compared cell by cell, and by `diff` with those two cells blanked) |
| the branch's worksheet copied into that clone, `--triage` run again | the ten trackers' front matter equals the branch's, except FM-024 and FM-026, whose `status:` and dropped `next:` are the by-hand finishes |
| `OPEN_STATUSES` counted on both trees (`git show`) | `origin/main` 16, this tip 14 |
| `grep -H '^rank:' work-tracker/FM-*.md` | 1 FM-029 · 2 FM-007 · 3 FM-018 · 4 FM-005 · 5 FM-006 · 6 FM-032 · 7 FM-030 · 8 FM-031 · 9 FM-028; none held twice, #10 free |
| the parent project, read-only `git log --all` | the RV ids in FM-027's reason; its 0.18.0 vendoring commit and its time |

## Claims

**The command applied exactly the ten verdicts.** ✓
- `keep P2 #1 build` FM-029, `#6 wait` FM-032, `#7 build` FM-030, `#8 wait` FM-031, `#9 build` FM-028: each carries
  `triaged: 2026-09-24`, `tier: P2`, its rank and its move. `park P3` FM-023, FM-025, FM-027: `status: Parked`,
  `tier: P3`, `triaged:`, and no rank. `fix` FM-024 and `merge FM-004` FM-026: `triaged:` only from the command.
- Every `next:` the pass changed is one the rules let it change. FM-028 and FM-030 said `review`, and their *Now*
  opens *nothing is built*. FM-031 and FM-032 said `build`, and both are built and tagged in 0.18.0. FM-029 said
  `owner`, and its answer is signed (`140f799`, `G`, 14:24:00).
- No hand edit of `triaged:`, `tier:`, `rank:` or a park. `next:` is dropped by hand on FM-024 and FM-026. The schema
  does not require that, and it does not forbid it either. The first pass's done trackers keep theirs (FM-008,
  FM-011, FM-016, FM-020 … FM-022), so the repository has both forms. That is not a finding.

**The worksheet.** ✓ Its derived cells are what `--triage` writes on `095f1d3`. Every Verdict is well-formed. No `|`
is inside a cell. The reasons are in the worksheet. What reached the trackers is the by-hand finishes, and R2 covers
the one sentence that goes beyond them.

**The ten reasons against the record.**
- FM-029 ✓ The answer *the relation only — no new verbs* is `140f799`, signed at 14:24:00. *0.18.1 in build now*: an
  Implementer worktree holds `fm/029-0-18-1-the-relation-computed`, cut at `095f1d3`, with no commit yet.
- FM-031 ✓ S2 (`90d3d6f`, `636f56e`) and S1-as-FM-032's-S2 (`3c0754f`) are in 0.18.0's CHANGELOG. The cap was revoked
  by his signed `7c97c5b` (PR 46). *What is left* is its *Now*, word for word.
- FM-032 ✓ S2 and S4 are in the CHANGELOG, and S1 and S3 are AGENTS.md rules (`fbc2697`). *Done when*'s third line is
  *the open count falls for a week*. ✗ in part: *this pass's three parks … are its first evidence*. A park leaves
  the count as it is, as the pass's own paragraph says. Only the fix and the merge lower it (R6).
- FM-028 ✓ It was reproduced twice on 0.17.8: `916cd26` after midnight, and the `Etc/GMT±` runs at 07:37.
- FM-030 ✓ The *Now* agrees: found at a consumer's morning sitting. The parent's tracker id alone is named, as allowed.
- FM-027 ✓ The session-id case is moot: FM-032 S2 made the registry a report. The review-id case recurred. The parent
  minted *RV-473 …* at 09:48:44 (`dd49ee5e`) and again at 09:49:24 (`5850683b`). ✗ in what it names and leaves out
  (R7).
- FM-023 ✓ *used once and praised*. ✗ *nobody is on it this week*: it has four commits on 09-23 (R4).
- FM-025 ✓ The measurement was 25–35k tokens. *today's cold Principal session read the record on its own* is not
  verifiable from the record.
- FM-024 ✓ The registry was retired by FM-032 S2 in 0.18.0. ✗ *shipped in 0.17.7* (R5). The reason says nothing of the
  tracker's open slice 2 (R1).
- FM-026 ✗ Both grounds fail. *its considered names FM-004*: the schema reads `considered:` as *looked at, not
  merged*. *today's vendoring of 0.18.0 into the parent project is the case*: see R2.

**The by-hand finishes.**
- FM-024 → `Shipped`, with a closing row. Shipped is the right word for what 0.17.6 merged. The trailer rule stands,
  and *Closed* would say nothing shipped. What the fix leaves open is R1.
- FM-026 → `Closed`, with a ship-log row, a paragraph under FM-004's *What is true now* and a row in FM-004. What the
  paragraph leaves behind is R2.

**TRIAGE.md's paragraph.** ✓ on every count:
- 10 judged, FM-023 … FM-032.
- Kept 5 at P2: #1 FM-029, #6 FM-032 (wait), #7 FM-030, #8 FM-031 (wait), #9 FM-028.
- Parked 3 at P3: FM-023, FM-025, FM-027. Fixed 1: FM-024. Merged 1: FM-026 into FM-004.
- The open count goes 16 → 14. I counted `OPEN_STATUSES` on both trees myself.

The current path is untouched. ✗ The seat's count of its own miss, and one time (R6).

**Scope.** ✓ Nothing outside `work-tracker/`. The commit message carries no pull-request number with the sign. The
TRIAGE paragraph's `#1` … `#9` are ranks, as in the first pass's paragraph.

## Findings

**R1 · P2 · confidence high · The `fix` closes FM-024 with its slice 2 open, and no open tracker holds that slice.**
- **What:** FM-024 `:227–228` reads *Not in slice 1: … the refusal of same-session verdicts (slice 2)*. Other
  places say the same:
  - 0.17.6's CHANGELOG, as consumers read it: *The refusal of a same-session verdict is a later slice, after a week of
    counts.*
  - README §6 on this tip (`:326`): *A count, not a refusal: the refusal is a later slice*.
  - FM-024's *What would decide it* waits on the 09-29 count.
- **Not retired by the ruling:** the Owner's *all four now* on FM-032 S2 lists what is lost: the refusal of a second
  session in one worktree, *convened by* and *scope*, open rows. The same-session refusal is not among them. S2
  keeps *a verdict's independence … read from the trailers* (FM-032 `:74–81`).
- **Not in the record:** neither the reason nor the closing row (`:253`) names slice 2. No open tracker names it. I
  grepped all 14 for *independen*, *same session* and *refus*.
- **Why it matters:** the current path's line 3 is *a pull request without an independent review's evidence file
  cannot merge — checked, not asked*. `--check` counts 37 of this week's 39 verdicts as *same session*.
  - A `fix` is for a status that is *simply wrong* (`shoalmark.py:2109`), and README §3 says *a story stays open while
    a chapter is*.
  - The shipped README still promises the later slice, and it now has no home: the intent's *a fix that is forgotten*.
  - This close is one of the two that lower FM-032's measure.
- **Fix:** one of these two.
  - Keep FM-024 open (`In Progress`). Rewrite its *Now* opening to slice 2. It gets a keep verdict, and the path's
    line 3 names it.
  - Or say in the closing row where slice 2 goes, and carry it as one line into the open tracker nearest line 3.
    FM-031's `--queue` already reads verdicts. The freeze bars a new filing for it (README §2).

**R2 · P2 · confidence high on the facts, medium on the grade · The merge moves FM-026's problem, not its scope, and
FM-004 can close without it.**
- **What moved:** four lines, `FM-004:39–42`: the gap, and a *case to write it from*.
- **What did not move:**
  - The Owner's direction quoted at FM-026 `:13`: *has to be tracked, and … has to land within the gist prompt*.
  - The four candidates: `--migrate`, ≈ 300 lines; the note alone; both; drop it.
  - *What would decide it*.
  - The *Done when*: the Owner rules a candidate; an outside fleet migrates in one sitting; FM-004's prompts rerun give
    ≥ 2 of 3.
- **Why it matters:** FM-004's *Done when* (`:58–61`) is untouched: *three reports recorded, the note corrected, the
  limits said*. Read as written, the 09-21 runs and 0.12.1 met it. So FM-004 can close with the migration never
  written.
- **The first pass did it differently:** its merge (FM-016 → FM-018) moved the whole state and the candidates, under
  *Merged in from FM-016*.
- **The `Closed — merged into [FM-004](…), 2026-09-24` line is missing** under FM-026's title. The rule names it
  (`shoalmark.py:2107`), and so does the command's own BY HAND line (`:2344`). FM-016 `:13` carries it.
- **The grounds in the reason and the paragraph:**
  - `considered: FM-004` means the filer looked at FM-004 and filed apart (the schema). It is not a sign that the two
    belong together.
  - *The case* is wrong in two ways:
    - The parent project's vendoring of 0.18.0 upgrades a tool that project has run since 09-21 (FM-001). It is not
      an existing fleet's record moving over, which is FM-026's gap.
    - Its commit (`cff617d3`, 14:56:12, on a branch) came after this pass's commit (14:49:42). So FM-004 records *a
      fleet that moved its registry, its hooks and its house rules in one pull request* before it happened.
  - That sentence is the seat's own addition, written into a tracker during a pass, and it names more of a consumer
    than its id.
- **Fix:**
  - A section *Merged in from FM-026* in FM-004 with the quote, the candidates and *what would decide it*. FM-026's
    three done lines go into FM-004's *Done when*.
  - The `Closed — merged into` line in FM-026.
  - Drop *the case*, or restate it as a fact that exists.
  - Whether the scope belongs to FM-004 at all is the seat's judgement, and I do not grade it.

**R3 · P3 · Two waits are ranked ahead of builds.**
- **What:** #6 FM-032 (`wait`) sits before #7 FM-030 (`build`), and #8 FM-031 (`wait`) before #9 FM-028 (`build`).
  The rule the command prints (`shoalmark.py:2113`) is *what cannot be worked on now — it waits for a date … — is not
  ranked ahead of what can*.
- **Effect:** none on `START WITH`, which skips `wait` and `owner` (`:3961`). The ranked table reads out of working
  order.
- **Fix:** FM-030 #6, FM-028 #7, FM-032 #8, FM-031 #9. Change the worksheet's Verdict cells and run `--triage` again
  today, or leave it to the next pass.

**R4 · P3 · Three parks where the row's keep test reads *keep*.**
- **What:** FM-023, FM-025 and FM-027 read *2026-09-23 · keep · NEW FILING*.
  - A park is *a row that fails the keep test* (`:2103`), and *park it, unless it was worked on this week* (`:2096`).
  - FM-023 has four commits on 09-23 (15:04–15:33), made on the Owner's ask.
  - The first pass kept P3 filings of that age unranked (FM-001, FM-004).
- **Effect:** none on the board, where Parked and triaged Proposed are both backlog, and none on the open count or
  `START WITH`. The other conditions of a park hold: P3, a real remainder, nobody on it (no branch or worktree names
  them), and a restart named in the reason (loosely for FM-027, R7).
- **Also:** all three keep `next: review` while their *Now* opens *nothing is built*.
- **Fix:** the Owner strikes these rows or lets them stand; he rules by merging. If *a filing alone is not work* is
  what the seat meant, that is a rule. Under the freeze, it goes as one line into the closest open tracker.

**R5 · P3 · FM-024's closing names the wrong release and no commit.**
- **What:** the reason and the closing row say *the trailer rule shipped in 0.17.7*. It shipped in 0.17.6: CHANGELOG
  *The trailer*, and `v0.17.6` = `4bb3f32`. 0.17.7 changed only how the trailer is read.
- The fix rule says *cite the commit*. No sha is cited. The first pass cited `a522e0f` and `59eebeb`.
- *What is true now* still opens *open for the merge, not merged* (`:18–20`). The first pass put the Shipped line at
  the head of FM-008's *Now* (`:16`).
- **Fix:**
  - 0.17.6 (`4bb3f32`) and 0.18.0 (`095f1d3`) in the row.
  - One Shipped line at the head of *Now*. This folds into R1's rewrite if FM-024 stays open.

**R6 · P3 · The pass's account of itself does not match the record.**
- **The miss count:** *four of them built on and two asked about before any judgement* cannot be reproduced. On
  `origin/main` before the pass:
  - 3 of the ten were In Progress: FM-024, FM-031, FM-032.
  - 1 had `next: owner`: FM-029.
  - 3 have code on main that names them: FM-024 (10 commits), FM-031 (5), FM-032 (4).
  - 3 carry a signed answer: FM-029 `140f799`, FM-031 `d20bc89`, FM-032 `ffa63b8`.
  - That makes four distinct trackers. The commit message says *nine filings had been built on or asked about*.
- ***An hour after 0.18.0 was tagged*:** `v0.18.0` is `095f1d3`, committed 14:35:25. The pass's commit is 14:49:42,
  so at most a quarter of an hour passed.
- **FM-032's reason:** it counts the parks as evidence of the count falling (see above).
- **Fix:** *four of them worked on before any judgement, three built (FM-024, FM-031, FM-032) and three asked
  (FM-029, FM-031, FM-032)*, and *within a quarter hour of the tag*. The commit message is pushed and stays as it is.

**R7 · P3 · FM-027's reason names a consumer's review ids and leaves out FM-027's own case.**
- **What:** *RV-473 … RV-480 minted twice in a minute* is true: `dd49ee5e` 09:48:44, `5850683b` 09:49:24. But it
  names the parent project's review ids in a shoalmark file. 0.17.6's R5 made *the consumer's tracker and review ids*
  generic, and FM-029's R7 allows *only the id*.
- The tracker's own case is missing: `--new` gives two branches one tracker id. 0.18.0 did not touch it, so that is
  the remainder.
- *Its next reader is the Reviewer seat's own ids* is not a restart condition.
- **Fix, forward:** *a consumer's hand-kept review ids collided twice within a minute; `--new`'s tracker ids are the
  remainder, and the next such collision restarts it*.

## Verdict

**NOT READY: R1 and R2 are P2.** Both come from by-hand finishes that close work, and both let open scope leave the
record:
- R1: FM-024's slice 2, which the path's line 3 needs and README §6 promises.
- R2: FM-026's candidates and done-condition, which FM-004's *Done when* does not cover.

R3–R7 are P3 and are fixed forward. R5 folds into R1's fix. R3 and R4 are the Owner's to strike or keep when he
merges.

What holds:
- The gates are green, both suites pass, and INDEX is the generated one.
- The worksheet's derived cells are what `--triage` writes on `095f1d3`.
- The command applied exactly the ten verdicts, and no rank is held twice.
- Every number in the paragraph but the miss count is right, the open count 16 → 14 included.
- The path is untouched, and nothing lies outside `work-tracker/`.
- Eight of the ten reasons state facts the record bears out, and parts of the other two do too.

Not verified:
- *the Owner's word after the board showed the day's work* (chat).
- *today's cold Principal session read the record on its own* (FM-025).
- *rowed in the parent project's ledger*: no commit on any ref of the parent carried such a row by 14:57.
- Whether the Owner has run `--queue` against FM-031's first *Done when* line.
