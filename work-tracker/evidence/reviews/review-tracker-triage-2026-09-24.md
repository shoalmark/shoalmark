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

## Pass on 87bac4e (2026-09-24 15:35 CEST, Reviewer, session `8e509911/reviewer-1`)

**Scope.** `87bac4e` (`87bac4ead0ae39c835b8e1d9114d482b746072e0`) is one commit by the principal seat, under
`8e509911`, on this verdict `b3d9002`.
- Against `origin/main`, it touches the ten trackers (front matter only), INDEX, TRIAGE.md (two lines added) and the
  worksheet. FM-004 is byte-identical to main's again.
- This review file is unchanged by it.
- The tier is still docs. The commit message carries no pull-request number with the sign.
- Independence: same session `8e509911`, reported.

**What I ran at `87bac4e`.**
- `--triage`: *Applied nothing — no new filled rows*, and `git status --porcelain` is empty after it.
- `--check` 0; its freeze line reads *16 open*. `--session-check` 0.
- `python3 shoalmark.py`: 32 trackers, and the tree is still clean.
- `test_shoalmark.py` 0 (285 ok); `test_core.py` 0 (148 ok).
- `git merge-tree` with `origin/main`: clean.
- `--next`: `#1 FM-029 build · #2 FM-007 owner · #3 FM-018 wait · #4 FM-005 wait · #5 FM-006 build · #6 FM-030 build ·
  #7 FM-028 build · #8 FM-024 build · #9 FM-032 wait · #10 FM-031 wait`, then `START WITH: FM-029`.
- Ranks 1–10, each held once.
- `OPEN_STATUSES` on the tip: 16.

**The command applied exactly the worksheet.** ✓
- The scratchpad clone was reset to `095f1d3`. The branch's worksheet was copied in and `--triage` run. Every
  tracker came out byte-identical to the branch's, and so did the worksheet.
- INDEX differs only by the clone's own signature-lint lines: that clone has no `allowedSignersFile`.
- No hand edit of anything the command writes, and no body edit at all.

**The findings of the first pass.**
- **R1 ✓ closed.** FM-024 is `keep P2 #8 build` and still `In Progress`. Its reason names slice 2, README §6's later
  slice and the path's line 3, and it says *0.17.6*. See R8 for the tier.
- **R2 ✓ closed.** FM-026 is `park P3` and still open, with its candidates and *Done when* in place. FM-004 is main's.
  The reason says why this is no merge.
- **R3 ✓ closed.** The builds come first (#6, #7, #8), and the waits after them (#9, #10).
- **R4 · P3 · stands, for the Owner to rule.**
  - The rows of FM-023, FM-025, FM-026 and FM-027 still read *keep*. The rule's letter is unchanged: *a row that
    fails the keep test*, *park it, unless it was worked on this week*.
  - The pass now states its ground in the paragraph: the filing itself is the only date, and nobody is on them. It
    holds on git: FM-026 and FM-027 have no commit after 09-23, and FM-023's last is 09-23 15:33.
  - I do not count it as meeting the rule. It reads *worked on* as *worked on since filing*, which the rules do not
    say. It is now open and checkable, which is what he needs to strike it or let it stand.
  - Two smaller points:
    - FM-026's and FM-027's reasons name no restart. The rule asks for one: *"the Owner ranks it" counts*.
    - All four still say `next: review` with nothing built.
- **R5 ✓ moot.** There is no Shipped status and no closing row.
- **R6 ✓ closed in the paragraph.**
  - *Three built on (FM-024, FM-031, FM-032) and three asked about (FM-029, FM-031, FM-032)*: my count.
  - *Fourteen minutes after 0.18.0 was tagged*: git bounds it at 14:35:25 → 14:49:42. The tag is lightweight, so
    fourteen is the most it can be.
  - *Nothing closed, the open count stays at 16*. All other numbers are right: 10 judged; 6 kept at P2 with the ranks
    above; 4 parked at P3.
  - One new claim fails (R9).
- **R7 ✓ closed.** FM-027's reason names no ids of the parent project. It states its own case: `--new` guessing the
  next number on a branch.

**R8 · P3 · FM-024's reason places slice 2 on the path's line 3, and its tier and rank read as if it did not.**
- **What:** the scale the command prints is *P1 on the current path* and *harm … after the path's own work, unless it
  blocks it*. FM-024 is P2 and ranked #8, behind FM-030 (#6) and FM-028 (#7), two defects the path does not name.
- **Fix:** the Owner's to strike when he merges. Or the next pass either makes it P1 and ranks it ahead of those two,
  or says in the reason why line 3 does not name it.
- **Not the pass's to fix:** FM-024's *What is true now* still opens *open for the merge, not merged*, and `--next`
  prints that under #8. A pass writes no note into a tracker. The seat that takes FM-024 up rewrites it first (README
  §3).

**R9 · P3 · The paragraph cites a filing that does not exist.**
- **What:** it says *graded by the Auditor seat and tracked as its own filing*. No Auditor commit and no new tracker
  is on any ref of shoalmark or of the parent project by 15:28 (read-only `git log --all`). Under the freeze (16
  open ≥ 8), `--new` would also refuse a filing without `tags: bug`.
- **Fix, forward:** name the filing's id and repository once it exists, or write *to be filed*. If it is filed here,
  the count reads 17.

**For the merge order, not a finding.**
- This branch merges cleanly onto `main`.
- The 0.18.1 branch (`fm/029-0-18-1-the-relation-computed`, `ad37f41`) conflicts with it in FM-029's front matter and
  INDEX. That branch sets `In Progress` and clears the ask, and this one adds `triaged:`, `rank:` and `tier:` there.
- The second to land keeps both, and regenerates INDEX.

**Verdict on 87bac4e: READY WITH FINDINGS (R4, R8, R9 P3).** R1, R2, R3, R6 and R7 are closed, and R5 is moot. Under
the docs tier the P3s are fixed forward. R4 and R8 are the Owner's to strike or keep when he merges.

Not verified: the Owner's word before the pass (chat), and the Auditor's grading (R9).

## The FM-033 row, 81dce10 (2026-09-24 16:50 CEST, Reviewer, session `8e509911/reviewer-1`)

**Scope.** Branch `tracker/triage-2026-09-24-fm-033`, tip `81dce10` (`81dce10fbba0c8da157d3beb8b6dead1e3534985`). It
is one commit by the principal seat (`Session: 8e509911`) on `origin/main` `86f7595` (PR 54, the Owner's answer to
FM-033).
- `git diff --name-only origin/main...HEAD` names FM-033, INDEX, TRIAGE.md (one paragraph changed: the addendum
  appended) and the worksheet (one row added). **Tier: docs, one pass.** It was reviewed in a fresh worktree,
  `shoalmark-review-4`.
- Independence: same session `8e509911`, reported. This matters for R11.

**What I ran.**
- `--triage`: *0 trackers to judge*, *Applied nothing*, and the tree is clean after it.
- `--check` 0, with *17 open*; `--session-check` 0.
- `python3 shoalmark.py`: 33 trackers, and the tree is clean.
- `test_shoalmark.py` 0 (298 ok, on 0.18.1); `test_core.py` 0 (148 ok).
- `git merge-tree` with `origin/main`: clean, and `86f7595` is an ancestor.
- `--next`: ranks #1 … #10 unchanged, each held once, and `START WITH: FM-029`.

**The command wrote exactly the verdict.** ✓
- FM-033's front matter differs from main's in three lines: `next: owner` → `build`, `triaged: 2026-09-24`,
  `tier: P2`.
- It has no `rank:`, and `status: Proposed` stays.
- `ask*`, `answer:`, `answered:` and `answered-by:` are untouched.
- Replayed in the scratchpad clone: `--triage` on `86f7595` writes an FM-033 row whose derived cells are identical to
  the branch's. With the branch's worksheet copied in, it writes FM-033 and the worksheet byte-identical. INDEX
  differs only by that clone's signature-lint lines.
- `owner` → `build` is allowed. The ask is answered (`65f37a4`, signed `G`, 16:29:09, the proposal verbatim), and
  *Now* says *Nothing is built*.

**The reason's facts.** ✓
- The filing is `35c7664`, 15:31:27, after the re-made pass (`87bac4e`, 15:19). It comes from the Auditor's draft,
  as *Now* says (session `8b91dba2`).
- The answer, at 16:29, is the proposal.
- *Its build is the gate keyed on the build commit and the board's activity view*: FM-033's *Done when*, lines 1–2.
- *Every rank 1–10 is held today*: true as a count. It is not a constraint (R10).
- *First of the unranked*: nothing keeps such an order. `--next` prints only the ranked when any are ranked
  (`next_up`), so FM-033 does not appear in it at all.

**The addendum's numbers.** ✓
- 16:29, P2, unranked, `next: build`.
- The open count 17: `OPEN_STATUSES` counts 17 on `86f7595` and 17 on this tip. FM-033's filing made it 17, and the
  row changes nothing.
- It also closes the earlier **R9** in fact. *Tracked as its own filing* now exists: FM-033, written by the Auditor
  seat. The paragraph does not yet name FM-033 as that filing (R11).

**R10 · P3 · confidence high · *All ten ranks held* is not a constraint, and #1 is held by shipped work.**
- **What:** the command takes a rank from its holder for a verdict that stands, and an unranked verdict drops one
  (`apply_verdict`: `set_front(text, "rank", … else None)`). Today's sheet is re-applied as a whole.
  - So FM-033, a build the Owner answered today, could hold #9 or #10.
  - Those two are held by waits, FM-032 and FM-031. The printed rule is that *what cannot be worked on now … is not
    ranked ahead of what can*.
  - FM-029 holds #1 with `next: build` and a *Now* that says *not yet merged*. Its branch merged at 16:25:41 and is
    tagged `v0.18.1`, so `START WITH` points at shipped work.
- **Why it matters:** unranked, the cure for the day's violation is invisible in `--next`. It sits below two trackers
  that cannot move.
- **Fix:** on today's sheet, FM-033 `keep P2 #9 build`, FM-032 `#10 wait`, FM-031 unranked (or the seat's order),
  then run `--triage` again. FM-029's #1 is freed by the seat that closes FM-029 against `v0.18.1`, not by a pass.
  Or leave all of it to the Owner's strike.

**R11 · P3 · confidence medium · The self-judgement is disclosed where the Owner does not read it.** This is the CREDO
question, graded.
- **In lane:** a *keep* is triage, and the Principal signs triage. A keep clears nothing: the violation stays open,
  its record intact, its cure queued. The CREDO's bar, *may not clear its own work*, is not crossed.
- **Not a control:** *Self-critique is preparation, not clearance*, and *who independently receives the record?*
  This Reviewer is the same session, and `--check` counts it so. So the only independent receiver is the Owner,
  through his strike at the merge (README §4).
  - The disclosure is in the worksheet's Reason and the commit body.
  - It is not in the TRIAGE.md addendum, which is where he rules a pass.
  - `--owner` says *NOTHING NEEDS THE OWNER*.
- **Where the shadow could act:** in the tier and the rank. The one choice with a stated ground is the rank, and it
  rests on the constraint R10 shows is not one.
- **Grade:** enough for a keep once the Owner is shown it. Not enough as written.
- **Fix, forward:** one clause in the addendum, *judged by the session whose builds FM-033 records; the Owner strikes
  the row if he sees a conflict*. Name FM-033 as the violation's filing in the paragraph, which also completes R9.

**For the merge order, not a finding.**
- `fm/033-the-auditors-fix-forward` (`645e4d4`, with its verdict `bf5b2cc`) also touches FM-033: `considered:` gains
  FM-021 and FM-029, and the body changes. It sits on the same `86f7595`.
- `git merge-tree 81dce10 origin/fm/033-the-auditors-fix-forward` is clean. Merged in the scratchpad clone, FM-033
  auto-merges to `considered:` (7 ids), `next: build`, `triaged:` and `tier:`. The generator then changes nothing but
  that clone's own lint lines.
- **Neither needs a conflict resolution.** The second to land is behind `main` and merges cleanly as it stands. Only
  a merge rule that demands an up-to-date branch would make it take `origin/main` first, and that merge is also
  clean.
- After both land, the worksheet row still says *FM-029 … NOT considered* and *FM-021 … NOT considered*. That was
  true of the tracker when the pass read it, and the worksheet stays as written.

**Verdict on 81dce10: READY WITH FINDINGS (R10, R11 P3).** Both are fixed forward under the docs tier, or struck by
the Owner. R9 of the pass on 87bac4e is closed in fact by FM-033's filing. R4 and R8 stand as before.

Not verified: the Auditor seat's session `8b91dba2`. No commit of it is on any ref of this repository. The filing
says it was *filed word for word* from its draft (sha256 `19d16c62…`), and I did not see the draft.
