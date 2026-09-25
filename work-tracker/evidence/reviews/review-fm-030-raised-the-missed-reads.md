# Review — FM-030's second raise and its same-day pass, at d2de1f7 (2026-09-25 14:02 CEST, Reviewer, session `8e509911/reviewer-11`)

- **Branch:** `fm/030-raised-the-missed-reads`, tip `d2de1f7` (`d2de1f7f717221bd40a7655c36980e18be6d1c32`). It has four
  commits on `origin/main` `f34de1e` (PR 73's merge), all by the principal seat (`Session: 8e509911`,
  `Worktree: shoalmark-principal`):
  - `bd81954` 13:34:50: FM-030's second `## Raised` line and one ship-log row;
  - `b430d7e` 13:36:05: the pass. Three hand rows on today's worksheet, FM-007's and FM-029's front matter, INDEX, and
    one paragraph under *Passes*;
  - `ff30d2d` 13:37:23: one ship-log row, the Owner's word on invites and notifications;
  - `d2de1f7` 13:38:24: that row's *13:3x* changed to 13:33:29, in place.
- **Tier: docs, one pass.** `git diff --name-only origin/main...HEAD` names six paths, all under `work-tracker/`: FM-007,
  FM-029, FM-030, INDEX, TRIAGE.md and the worksheet. Front-matter values change, but no key does. There is no
  `shoalmark.py`, test, configuration or hook. A P2 sends it back.
- **Independence:** this seat is a sub-agent of the branch's own session (`8e509911`; this seat is
  `8e509911/reviewer-11`). `--check` counts it as *same session*. Reported, not refused.

## What I ran

| run | result |
|---|---|
| the Principal's transcript: the user record stamped `2026-09-25T11:31:26.030Z`, read alone | a fenced line, then a pasted assessment. The line appears twice (in the fence, and indented inside the paste), identical both times |
| that line against FM-030's second `## Raised` bullet at all four commits | byte-identical after the `- ` (384 bytes; the only non-ASCII character is `·`) |
| every added line and the four commit messages, checked for the paste's consumer detail | none of its identifiers, times, paths, names or counts; one element beyond the raise line entered (check 1) |
| the transcript, searched for *Better than only invites* | queue records: enqueued at 11:33:13.626Z as *…would be notifications.*, pulled back at 11:33:22.020Z, sent at 11:33:29.972Z as *Better than only invites would be invites + notifications.* The `queued_command` attachment has the same stamp; absorbed mid-turn at 11:36:18Z |
| a scratchpad clone at `bd81954` (signers file configured), its own worksheet, `--triage` | exit 0, *0 trackers to judge*, *Applied nothing*. `--version` prints 0.18.3 |
| that clone with `b430d7e`'s worksheet copied in, `--triage` | *Applied 3: FM-030: keep P1 #1 build · FM-029: keep P2 #2 build · FM-007: keep P1 owner*. FM-007, FM-029 and the worksheet are byte-identical to `b430d7e`. **FM-030 (`rank: 1`) and INDEX (#1 FM-030) differ** (R1) |
| a clean clone at `d2de1f7`, `--triage` run four times | *Applied 1* every time, alternating *FM-030: keep P1 #1 build* and *FM-030: keep #3 P1 build*; FM-030's `rank:` goes 1, 3, 1, 3 (R1) |
| positive control: on `bd81954`, FM-030 set to `triaged: 2026-09-24` and its earlier row removed from the sheet, then `--triage` | *1 trackers to judge*: FM-030 RAISED, Closest FM-029 (15), Facts `reads 2.5k`. Its Now is the **first** raise (07:06:48), not the second (R5) |
| control: FM-029's and FM-007's `triaged:` set back, `--triage` | their derived rows, compared cell by cell with the hand rows (R6) |
| `--owner`, `--standup` and `--next` at `bd81954` and at `d2de1f7` | `--owner` prints *NOTHING NEEDS THE OWNER.* both times, and `--standup` prints *0 item(s)* both times. `--next` loses *#2 FM-007 · P1 · next: owner* and now opens at #2 FM-029, #3 FM-030. Nothing holds #1 |
| `python3 shoalmark.py --check` | exit 0; *82 verdict(s) · independent 6 · same session 71 · untraced 5*; *filing freeze: 19 open* |
| `python3 shoalmark.py --session-check` | exit 0 |
| `python3 shoalmark.py` | the tree is clean after it |
| `test_shoalmark.py` · `test_core.py` | exit 0, 394 ok · exit 0, 148 ok; all green |
| `git merge-tree --write-tree origin/main HEAD` | clean: the result is the tip's own tree, `dff29aa` |
| `origin/fm/035-ci-green-on-every-platform` | not on origin (`git ls-remote`), so there was nothing on origin to merge-tree against. For information only: the local branch of that name (`df4c8ab`, another seat's, still moving) conflicts with this one in TRIAGE.md, because both add a *Passes* paragraph at the top |
| `git show -s` on every sha and time cited | `1034602` 2026-09-25 07:29:54 `G` (FM-007's answer); `57aac8d` 11:56:39 (`v0.18.3`, a lightweight tag); `ea630c1` 09:14:14 (PR 69); `9e48ee8` 2026-09-24 18:59:10 `G` (the raise rule) |

## The checks

**1. The raise line is word for word ✓. Leaks ✓: one element beyond the line entered. Confidence high.**
- The record's 11:31:26.030Z is 13:31:26 CEST, as the ship-log row, the paragraph and the Facts cell all say.
- The fenced line equals FM-030's second bullet byte for byte at all four commits. The copy inside the paste is identical.
- The assessment in the paste is not filed. No identifier, time, path, name or count from it appears anywhere on the branch.
- One element beyond the raise line did enter: the ship-log row's *The Auditor's product line: …*. It is the paste's
  product bullet, paraphrased: its precedent clause and *not just asks* are dropped, and *first in 0.18.4* comes from
  the paste's closing line. The paragraph and the Reason carry the same list. It is attributed, it describes shoalmark,
  and it holds nothing of the consumer. Not a finding.

**2. Every front-matter change is the command's: ✓ FM-007 and FM-029, ✗ FM-030 (R1). Confidence high.**
- `b430d7e` changes FM-029 (`triaged:` 09-24 → 09-25, `rank:` 1 → 2) and FM-007 (`triaged:` → 09-25, `rank: 2` removed).
  The replay writes exactly these.
- `b430d7e` does not touch FM-030, so at the tip it still holds `rank: 3`, although the pass's lead verdict is
  `keep P1 #1 build`.

**3. The hand rows: marked in part, Now cells honest in part (R4, R5, R6). Confidence high.**
- All three rows mark the Closest cell as the seat's, and all three say in Facts *this row written by hand by the
  Principal seat*. No other cell is marked on its own.
- FM-030's Now is the second raise ✓.
- FM-029's Now is the seat's summary:
  - true on 0.18.3: PR 65, `57aac8d`, and the cold Reviewer's four passes (three NOT READY, the fourth READY);
  - true on AU-29;
  - wrong on the tier line (R4).
- FM-007's Now quotes his answer verbatim (`1034602`, 07:29:54, `G`) ✓, reads it as *no day this week* ✓, and cites PR 69
  ✓. It leaves out the tracker's own seat line (R4).
- The reason the rows were written by hand is stated wrongly (R5).

**4. The three verdicts against the path.**
- **FM-030 `keep P1 #1 build`:**
  - P1 ✓ on line 6, which the raise meets plainly: the act lived in chat and a run sheet. Line 1 rests on the raise
    naming it.
  - #1 ✓: FM-029's 0.18.3 scope has shipped.
  - Line 6's quotation is altered (R8), and there is no P0 line although the raise records harm (R2). Confidence
    medium-high.
- **FM-029 `keep P2 #2 build`:** ✓ re-ranked, not re-tiered. P2 stands as judged on 09-24, 0.18.3 shipped, and AU-29
  remains. The tier line is not FM-029's (R4). Confidence high.
- **FM-007 `keep P1 owner`, unranked:**
  - P1 on path 5 ✓.
  - `owner` ✓: the act is his, and his answer dates it after 09-29.
  - The unranking is R3. Confidence medium.

**5. TRIAGE.md: ✓ in form, ✗ in three facts.**
- ✓ One paragraph is added under *Passes*. The intent and the current path are byte-identical, and path 5 is kept.
- ✗ Three of its facts: FM-030 is #1 (not on the board, R1), *this board of 0.18.2* (R5), and *13:3x* (R8).

**6. The 13:33:29 row: ✓ the quote and the time; ✗ the seat's design is not marked as the seat's (R7).**

**7. Times: ✓ sourced, except *13:3x* (R8).**

**8. Gates: ✓ all green. None of them reads a sheet's verdict against the front matter, so none sees R1.**

## Findings

**R1 · P2 · confidence high · The pass records FM-030 at #1, the board has it at #3, and every run of the command on today's
sheet flips it.**
- The worksheet, the paragraph, `b430d7e`'s subject and FM-030's ship-log row all say FM-030 is #1. At the tip, FM-030
  holds `rank: 3`, INDEX's ranked table and `--next` both open at #2, and nothing holds #1.
- Today's sheet holds two filled rows for FM-030: this pass's `keep P1 #1 build` and the morning pass's `keep #3 P1 build`
  (07:09).
  - `apply_worksheet` applies every filled row, each against the file as it was first read, and writes whichever one
    differs from that file.
  - So each run flips FM-030's rank: four runs on the tip gave 1, 3, 1, 3, each reporting *Applied 1*.
  - The claim that *`--triage` on the tip prints Applied nothing* is false on a clean checkout.
- `b430d7e` matches the state after an even number of runs. One run on `bd81954` gives FM-030 `rank: 1` and INDEX with a
  #1 row. FM-007, FM-029 and the worksheet come out byte-identical to `b430d7e`, and TRIAGE.md differs only by the
  paragraph, which the command does not write.
- After this merges, any seat's `--triage` on main flips the Owner's ranked table until midnight, when the sheet stops
  being today's. `--check`, the generator and both suites stay green through all of it.
- **Why P2:** the pass's lead verdict is not on the board it was made for, and that board is unstable under the command
  every pass runs.
- **Fix:** the sheet stops holding two filled rows for one tracker, or the tool applies only the newest one:
  - the first route rewrites a merged row, so the paragraph must say so;
  - the second is code: 0.18.4, the full loop, and a `--tags bug` filing under the freeze.
  - The route is the Principal's to choose.
- **Then:** commit FM-030 `rank: 1` and INDEX's #1 row as the command writes them, and run `--triage` twice on a clean
  checkout. Both runs must print *Applied nothing*.

**R2 · P3 · confidence high that the line is missing, 50 % on the tier · The raise records harm today, and the Reason does
not say why FM-030 is not P0.**
- The scale the command prints: *P0 harm to people who use it today, or the current path is blocked now · P1 on the
  current path*.
- The raise: a person using the tool missed a production read he owed at a fixed hour, twice, because no list showed it.
  The Reason says *this tracker's own case, now with harm*, and then gives P1.
- The morning pass's R2 asked the next pass to state its not-P0 ground as a fact the record holds. This pass faced actual
  harm and gave no ground.
- What P0 would move: the order against the CI fix. The Reason puts FM-030 *after the CI fix*, and the CI fix is ranked #6.
- **Fix, forward (or in R1's re-make):** a P0 line in the Reason, either P0 itself or the fact that contains the harm
  until the build, filed where the record holds it.

**R3 · P3 · confidence high on the facts, 65 % on the judgement · With FM-007 unranked, no list the tool prints shows the
act the Owner owes.**
- Before the pass, `--next` showed *#2 FM-007 · P1 · next: owner*. After it, `--owner` still prints *NOTHING NEEDS THE
  OWNER*, `--standup` prints *0 item(s)*, and `--next` no longer names FM-007. His answer of 07:29:54 promises the act,
  and FM-030 is the defect that drops such promises.
- The raise under judgement names line 6: *What the Owner owes is on their board with one button; nothing owed to them
  lives only in a ledger, a tracker body or a chat.* FM-007's Reason judges only path 5.
- The rule the Reason cites, *a wait ranks after the builds*, puts FM-007 after the builds, not off the table. FM-005,
  also `wait`, holds #4.
- The Reason says *nothing a seat does before then moves it*, but FM-007's ship log holds a 0.18.4 seat line of its own,
  *the tool says the tier* (R4).
- Against this finding: the morning pass unranked FM-018 (`wait`), and its review let that stand.
- **Fix, forward:** rank FM-007 after the builds so that `--next` says what waits on him, or say in the Reason where his
  act shows until FM-030 is built.

**R4 · P3 · confidence high · The tier line is FM-007's, and the pass gives it to FM-029.**
- FM-029's Now, FM-029's Reason and the paragraph all say what is left of FM-029 is AU-29 *and the tier said beside a
  signature* (*the tier line*).
- FM-029 holds AU-29 (its row of 06:52) and no tier line. The tier line is FM-007's row of 2026-09-25: *A line under the
  freeze for 0.18.4, this tracker's: the tool says the tier, not a bare verified*.
- FM-007's Now says *the seat's work under it … shipped in PR 69*, which leaves that line out.
- **Fix, forward:** the Reason says whose line it is. If FM-029's build takes it, a line in FM-029 says so, and FM-007's
  Reason counts it.

**R5 · P3 · confidence high · Main already runs 0.18.3, and 0.18.3's own rule is why it stayed silent on this raise.**
- The paragraph says *on this board of 0.18.2 — 0.18.3's tool lists a raised tracker itself*. FM-030's Closest cell says
  *0.18.3's tool derives RAISED, this board runs main*.
- In fact `v0.18.3` (`57aac8d`) is an ancestor of `f34de1e`, VERSION reads 0.18.3, and `--version` prints 0.18.3 at
  `bd81954`.
- Main's tool has the raise rule. It lists no row because both raises are dated 2026-09-25, the same date as FM-030's
  `triaged:`. `mark_raised` takes only a raise dated *after* `triaged:`, and its docstring says *a raise written after
  the same day's pass is re-judged by that seat's own re-run*. The hand row is that re-run, as designed.
- The control shows that even when forced to list FM-030, the tool puts the first raise in Now. The hand row's Now is the
  right one.
- This seat's brief also said 0.18.2.
- **Fix, forward:** the next paragraph says why the tool was silent. Whether a same-day second raise should reach Now is
  a possible 0.18.4 line, and the Principal's call.

**R6 · P3 · confidence high · As the morning's R1 found, the hand rows depart from the tool's derivation, and they are marked
per row, not per cell.**
- Against the tool's own rows (the controls above):
  - **Title:**
    - FM-030 reads *…before the act*; the tool prints *…before the act is done*.
    - FM-029 reads *…picked another*, which is the file's slug; the title is *…picked an option other than the
      proposal*.
    - FM-007 is in full, where the tool cuts at 70 characters with `…`.
  - **Hook:** in full, where the tool cuts at 220.
  - **Closest:** *—*, marked as the seat's. The tool gives FM-029 (15), FM-030 (15) and FM-001 (5).
  - **Facts:** no `reads`, and seat prose instead. The *written by hand* mark covers it.
  - **Now:**
    - FM-030's keeps the bullet's `- `.
    - FM-029's and FM-007's are the seat's summaries, where the tool prints the opening of *What is true now*. FM-029's
      opening still says 0.18.1 is *not yet merged*.
    - The row's mark covers these cells, but no cell says it is the seat's.
- The front matter is unaffected: the command reads only the Verdict cell.
- **Fix, forward:** as the morning's R1 said: copy the tool's cells, or mark each cell that is not the tool's.

**R7 · P3 · confidence high on the fact, medium on the weight · The 13:33:29 row follows the Owner's one sentence with the
seat's design, and does not say whose the design is.**
- The quote is exact, and the time is that of the version he sent. A first draft (13:33:13, *…would be notifications.*)
  was pulled back before sending.
- *On the product line above* ✓: the paste of 13:31:26 carried *an .ics per act*, and his word answers it.
- After the dash comes a design:
  - an `.ics` alarm before the window;
  - a notification when an act falls due and again when its window passes;
  - a `--notify`, scheduled by launchd or cron, that reads due times from the board's data and posts a system
    notification;
  - *the .ics alarm is the first notification*.
- He said *invites + notifications*; the form is the seat's. It stands unmarked beside his quote, in a line *for 0.18.4's
  build*.
- **Fix, forward:** a correcting row saying the form is the Principal seat's proposal, for the build's design to settle
  with him.

**R8 · P3 · confidence high · A time approximated, a path line misquoted, and a ship-log row rewritten in place.**
- **The time:** the paragraph's *(Principal seat, 13:3x, …)*. The pass commit is 13:36:05. FM-035's review raised the same
  fault as its R6 (*12:1x*).
- **The quotation:** FM-030's Reason quotes line 6 in italics as *what the Owner owes is on his board with one button*.
  - The line reads *their board*.
  - Its second clause is cut: *nothing owed to them lives only in a ledger, a tracker body or a chat*. That is the clause
    the raise meets most plainly.
  - The meaning holds, but the italics present the words as his.
- **The rewrite:** `d2de1f7` rewrites `ff30d2d`'s row in place (*13:3x* → 13:33:29).
  - It is unmerged, which is how the evening's R10 read the same case.
  - It is the third such rewrite in two days, after the evening's R10 and FM-035's R8.
- **Fix, forward:** 13:36:05; line 6 quoted whole; a correcting row next time.

## Verdict

**NOT READY — R1 is P2.** R2–R8 are P3. They are fixed forward, or taken into the re-make that R1 needs.

What holds:
- The tier is docs.
- The raise line is the Owner's paste byte for byte; 13:31:26 is true to the transcript; no consumer detail entered.
- The command wrote FM-007's and FM-029's front matter and the worksheet, as the replay shows.
- Against the path: FM-030 P1 holds on line 6, FM-029 is re-ranked and not re-tiered, and FM-007 stays P1 `owner`.
- TRIAGE.md gains one paragraph; the current path is untouched, and path 5 is kept.
- The Owner's word is quoted exactly, at the true time, 13:33:29.
- `--check` 0, `--session-check` 0, the generator clean, both suites green (394, 148), merge-tree clean against
  `origin/main`.

Carried, not re-graded:
- FM-035 (#6) is built before FM-030 (#1), as *the first build of 0.18.4 after the CI fix* says. This is FM-035's R5 and
  R7, still open.
- FM-029's *What is true now* still opens on 0.18.1 *not yet merged*, stale since PR 65. Changing it is not this pass's
  job.
- `--owner` prints nothing for the acts owed under FM-007's and FM-032's answers. That is FM-030's defect, and no pass
  changes it.

Not verified:
- Why `b430d7e` holds FM-030 at #3. The command's alternation explains it (an even number of runs), but the Principal's
  worktree is not this seat's to open.
- The Auditor seat's own record: it is sealed and barred. The line is checked against the Owner's paste alone.
- A merge-tree against `origin/fm/035-ci-green-on-every-platform`: the branch is not on origin.

The Owner lands this by merging; a merge rules nothing.
