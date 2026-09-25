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

## Pass on 05b68a4 (2026-09-25 14:59 CEST, Reviewer, session `8e509911/reviewer-11`)

**Scope.** The tip is `05b68a4` (`05b68a4aae2e5ef91aa6dfd9cd2e9d3570132933`), three commits after the verdict above
(`3e025e8`), all by the principal seat (`Session: 8e509911`):
- `9498419` 14:44:02 re-makes the pass on R1–R8;
- `069651d` 14:46:05 files FM-036 (`tags: bug`, under the freeze);
- `05b68a4` 14:47:16 judges FM-036 `keep P2 #4 build` and frees FM-005's #4.

The paths are FM-005, FM-030, FM-036, INDEX, TRIAGE.md and the worksheet, all under `work-tracker/`. **Tier: docs, one
pass.** **Independence:** this seat and the branch share a session (`8e509911`); reported.

**What I ran at `05b68a4`.**
- **`--triage` on a clean clone, three times:** each run exits 0 with *0 trackers to judge* and *Applied nothing*, and the
  tree is clean after each ✓.
- **Replays:**
  - On `bd81954` with `9498419`'s sheet: *Applied 3* (FM-029, FM-007, FM-030 `keep P1 #1 build`). FM-007, FM-029, INDEX
    and the sheet are byte-identical to `9498419`. FM-030's front matter also matches; the only difference is two
    ship-log rows the command does not write. TRIAGE.md differs by its paragraph alone ✓.
  - On `069651d` with the tip's sheet: *Applied 2: FM-005: rank #4 freed — FM-036 holds it now · FM-036: keep P2 #4
    build*. Everything matches the tip except TRIAGE.md's paragraph ✓.
  - FM-036's row, generated on `069651d`: its eight derived cells equal the tip's ✓.
- **`--next`:** #1 FM-030 · #2 FM-029 · #4 FM-036 · #5 FM-006 · #6 FM-035 · … #10. Each rank is held once, and #3 is empty.
- **Gates:**
  - `--check` 0 (*83 verdict(s)*; *filing freeze: 20 open*) and `--session-check` 0;
  - the generator leaves the tree clean;
  - both suites are green: `test_shoalmark.py` 394 ok, `test_core.py` 148 ok;
  - `git merge-tree` against `origin/main` is clean (tree `8cee1b3`).
- **`origin/fm/035-ci-green-on-every-platform`** (`b730c29`, its own latest verdict NOT READY) **conflicts in
  TRIAGE.md and INDEX.md**:
  - TRIAGE.md: that branch rewrites FM-035's paragraph (*12:1x* → 12:11:44), which sits directly under this branch's new
    paragraph.
  - INDEX.md: FM-035's rows change next to FM-036's new #4 row.
  - When the CI branch lands first, the resolution here is mechanical: keep both paragraphs, newest first, and let the
    generator write INDEX.
- **`--related FM-036`:** FM-032 7.1 · FM-030 6.0 · FM-019 4.7 · FM-027 4.0 · FM-016 3.7 · FM-028 3.4 · FM-001 3.3 ·
  FM-014 3.1. On `9498419`, before the filing, the title search found nothing above 0.6. At the tip, it ranks FM-036
  itself first (13.6).
- **Text written under the table:** a line added there is gone after one `--triage` run. `triage_worksheet` writes only
  the header, the generated rows and the filled rows.

**R1–R8.**
- **R1 closed on the board:** FM-030 holds `rank: 1` in its front matter and in INDEX; the sheet has one filled row per
  tracker; runs converge. How the row was made is R9.
- **R2 closed in form:** there is a not-P0 line. Its ground is R10.
- **R3 closed:** FM-007's Reason weighs line 6. The act sits on no list until FM-030 (#1) is built, and a rank would say a
  seat's work is next. That is the seat's judgement, reasoned, and it stands. See R13 for FM-005.
- **R4 open (P3):** FM-007's Reason now says the tier line is FM-007's, and FM-029's Reason drops it. But FM-029's Now cell
  still reads *…and the tier said beside a signature*, and the paragraph still reads *AU-29 and the tier line remain*.
- **R5 closed** in the paragraph and in FM-030's Reason (*main runs 0.18.3 … its strict rule*). The FM-030 row's own
  cells still say otherwise (R9).
- **R6 closed for FM-029 and FM-007:** each cell is marked, and the marks match the cells. Only the title, still the file
  slug, is unmarked. **Not closed for FM-030** (R9).
- **R7 closed:** the correcting row names the notification design as the seat's.
- **R8 closed in part:** *13:3x* is gone, and the quotation reads *their board*, though still without line 6's second
  clause. The correcting row has errors of its own (R11).

**R9 · P2 · confidence 80 % · FM-030's one row is the morning's row with this pass's verdict pasted on. The raise it
judges is not on the sheet, its cells contradict their own marks, and the morning's merged verdict is gone from the file,
under a claim of preservation the command makes impossible.**
- The row's first eight cells are byte-identical to the morning row on `origin/main`: Tier *P2*, Now the **first** raise
  (07:06:48), and Facts *0.18.3 build E, which lists a raised tracker, is in review, not on main*. Its Verdict and Reason
  are this pass's.
- The row judged at 13:36, the one carrying the second raise (13:31:26), was removed. That second raise line is now
  nowhere on the sheet.
- The Reason's marks, one by one, describe a different row:
  - *Tier (P1, the morning's)*: the cell reads P2;
  - *Now (the raise line, verbatim)*: the cell holds the other raise;
  - *Facts (the seat's)*: the cell says 0.18.3 is not on main, which the Reason itself contradicts.
- The morning pass's Verdict (`keep #3 P1 build`) and its Reason are gone from the file. The morning's paragraph still
  names that file as its worksheet.
- The paragraph and FM-036 both say the morning row's *text* is *kept under the table*. No text is under the table, at
  the tip or in `9498419`, and `--triage` deletes any on its next run (shown above).
- **Why P2:** this is the pass's own record of what it judged, and it now shows another raise, another tier and a false
  fact under its verdict. The claim that the displaced record was preserved is false, and the tool cannot make it true.
- **Fix:**
  - Make the one FM-030 row the second-raise row (`d2de1f7`'s first FM-030 row, cells unchanged) carrying the re-made
    Verdict and Reason; its marks then match its cells.
  - Say in the paragraph that the morning row was removed from the sheet, and where its verdict stands: the morning's
    paragraph, and the sheet at `f34de1e` in git.
  - Correct FM-036's *kept its text under it* and its interim rule, since the command drops text under the table.
  - Then two runs of `--triage` on a clean checkout: *Applied nothing* both times.

**R10 · P3 · confidence high · The not-P0 ground is the consumer's schedule, which this record should not hold and does
not source.**
- FM-030's Reason grounds *not P0* on the days the consumer's reads were re-planned to and on how long the consumer's
  data stands. This review does not repeat them.
- The days and the retention are the consumer's production detail. The raise line was redacted precisely to keep such
  detail out: it says only *at a fixed hour on two consecutive days*. Nothing in shoalmark sources these facts.
- **Fix, forward (or with R9):** give the ground without the consumer's days, for example *the missed reads are
  re-planned in the consumer's own record; the harm is recoverable*, and point to where that record can be checked.

**R11 · P3 · confidence high · The correcting row in FM-030 misstates both of its corrections.**
- *the row first timed 13:3x was corrected in place …, now 13:31:26*: that row is the Owner's word, and it reads
  **13:33:29**.
- *the raise row's* his board *is the path's* their board: no ship-log row says *his board*. The misquotation was in the
  worksheet's Reason, which is fixed.
  - The only *his board* in FM-030 is the first raise's line (07:06:48), which is the Auditor's text word for word and is
    not a misquotation.
- **Fix, forward:** a correcting row with 13:33:29, which places the *their board* fix in the worksheet's Reason.

**R12 · P3 · confidence high · FM-036's filing credits `--related` with the seat's choices and does not open the three
it marks.**
- The ship log says *`--related` held it against FM-033 (…), FM-028 (…) and FM-027 (…)*.
  - `--related FM-036` does not list FM-033 among its eight; FM-028 is sixth and FM-027 fourth.
  - Before the filing, the title search found nothing above 0.6.
  - The three were the seat's choice. This is FM-035's R3/R8 again.
- The sheet marks the machine's three closest, FM-032 (7), FM-030 (6) and FM-019 (5), as NOT considered. The printed rule
  is *OPEN every one marked NOT considered*, and the Reason names none of them. FM-030 is the case FM-036 was found on.
- The hook's backticked *`keep P1 #3 build`* was `keep #3 P1 build`.
- *What is true now* repeats R9's claim that the text was kept under the table. Its interim rule, *quotes the superseded
  row's text under the table*, does not survive one run of the command.
- **Fix, forward:** `considered:` names what was opened (FM-030 at least), and the Reason says why FM-032 and FM-019 are
  not the same work. A correcting row says who chose the three. The interim rule says where a superseded row lives.

**R13 · P3 · confidence 60 % · FM-036 took #4, not the free #3, and FM-005 lost its rank.**
- #3 was empty after R1's fix. Taking #4 unranked FM-005 (P1, `wait`) without need.
- With FM-007, two P1s are now off `--next`.
- The rule cited, *a wait ranks after the builds*, ranks it after, not off.
- Against this finding: FM-018's unranking this morning stood.
- The paragraph also folds FM-036's pass into the re-make's. The page's rule is *one paragraph per pass*.
- **Fix, forward:** FM-036 at #3 or FM-005 ranked after the builds, or a Reason that says why neither; and a paragraph of
  FM-036's own.

**Verdict on 05b68a4: NOT READY — R9 is P2.**
- R1 is closed on the board: FM-030 is #1, and runs converge.
- R2, R3, R5, R7 and R8 are closed, R2 and R8 in part: R2's ground is R10, and R8's correcting row is R11. R4 remains
  open as a P3.
- R10–R13 are P3, fixed forward or with R9.
- Every gate is green, and merge-tree against `origin/main` is clean. Against the CI branch, TRIAGE.md and INDEX.md
  conflict mechanically.

The Owner lands this by merging; a merge rules nothing.

## Pass on 38cd89e (2026-09-25 15:14 CEST, Reviewer, session `8e509911/reviewer-11`)

**Scope.** The tip is `38cd89e` (`38cd89e2bb52655a36da07a0fd9c2dee931995a8`), one commit by the principal seat (15:05:17)
after the verdict above (`9576f85`). It touches FM-005, FM-030, FM-036, INDEX, TRIAGE.md and the worksheet, all under
`work-tracker/`. **Tier: docs, one pass.** **Independence:** same session (`8e509911`), reported.

**What I ran at `38cd89e`.**
- **`--triage` three times on a clean clone:** each run exits 0 with *0 trackers to judge* and *Applied nothing*, and the
  tree is clean after each ✓. **Nothing is under the sheet's table** ✓.
- **Replay from `bd81954`,** with FM-036 as filed at `069651d` and the tip's sheet: *Applied 5*:
  - FM-005 `keep P1 #4 wait`, FM-030 `keep P1 #1 build`, FM-036 `keep P2 #3 build`, FM-029 `keep P2 #2 build`,
    FM-007 `keep P1 owner`;
  - every command-owned key (`triaged:`, `rank:`, `tier:`, `next:`, `status:`) of all five equals the tip's;
  - INDEX and the sheet are byte-identical.
  - FM-005's keys come out in a different order: on `bd81954` it still held `rank:`, while on the tip the key was removed
    and re-added.
- **Replay from `05b68a4`,** with the tip's sheet: *Applied 2* (FM-005, FM-036).
  - FM-005, INDEX and the sheet are byte-identical to the tip.
  - FM-030, FM-036 and TRIAGE.md differ only in the seat's text: one ship-log row, FM-036's `considered:`/body, and the
    paragraph ✓.
- **FM-030's row** is `d2de1f7`'s second-raise row, its eight cells byte-identical. Its marks match its cells: Tier P1, the
  keep test *RAISED (the second raise)*, Now the 13:31:26 raise, and Facts the seat's ✓.
- **Gates:**
  - `--check` 0 (*84 verdict(s)*; *20 open*) and `--session-check` 0;
  - the generator leaves the tree clean;
  - `test_shoalmark.py` 394 ok, `test_core.py` 148 ok;
  - `git merge-tree` against `origin/main` is clean (tree `4c9ddfb`).
- **`origin/fm/035-ci-green-on-every-platform`** (now `4e4d63b`) conflicts in INDEX.md and TRIAGE.md, as before. The
  resolution is mechanical.

**R4 and R9–R13.**
- **R4 closed:** FM-029's Now ends at AU-29, and the paragraph reads *the AU-29 line remains*.
- **R9 closed on the sheet:** the row, its marks, and nothing under the table. FM-036's interim rule now names the
  paragraph. How the paragraph quotes the displaced row is R14.
- **R10 closed:** *the consumer has re-planned within its own record*. No consumer schedule is left in any added line.
- **R11 not closed:** R15.
- **R12 closed:** `considered: FM-030, FM-032, FM-019, FM-028, FM-027`, and a ship-log row names the first version's
  FM-033. That row's order is loose (R16).
- **R13 closed:** FM-036 is #3, and FM-005's #4 is restored by its own row (R17). The paragraph still folds FM-036's pass
  into this one. Carried.

**R14 · P2 · confidence high (95 % on the fact) · The paragraph's quotation of the morning's FM-030 row is not that row.**
- TRIAGE.md: *The morning's FM-030 row — keep P1 #3 build, its reason: a defect he met himself (…); nothing built; the
  tool slice after 0.18.1 — is superseded by this pass's row and lives here, not on the sheet.*
- The quoted reason is FM-030's reason on the sheet of **2026-09-24**, whose verdict was `keep P2 #6 build`.
- The morning row of 2026-09-25, on `origin/main`, reads `keep #3 P1 build`, and its reason is *re-judged the same day
  on the raise rule (his signed answer `9e48ee8`): the Auditor's line names FM-032's answer and path 1 …*.
- That reason is now on no current file, and the paragraph says the row *lives here*. The pass's own record of a
  displaced verdict is therefore a false quotation, in italics, in TRIAGE.md, directly above the morning pass's paragraph
  that contradicts it.
- The quotation also brings a consumer's bug id into TRIAGE.md. It was already on main, in the 09-24 sheet.
- FM-030's Reason repeats the verdict as `keep P1 #3 build`.
- **Why P2:** the fix for R9 was to say truthfully where the displaced record stands. This says something false about it,
  in the file the Owner reads first.
- **Fix:** quote the morning row as it is at `f34de1e`: `keep #3 P1 build`, and its reason whole or cut with `…`.
  Alternatively, cite it by place: the morning's paragraph just below, and the sheet at `f34de1e`. Either way, drop the
  09-24 reason and the bug id, and correct the Reason's backticked verdict.

**R15 · P3 · confidence high · The correcting row still times the wrong row.**
- It now reads *the raise row's 13:3x was corrected in place while unmerged to 13:31:26 …; the 13:33:29 row keeps its
  own time*.
- The raise row has read *(13:31:26)* since `bd81954`. The row first written *13:3x* is the Owner's word (`ff30d2d`),
  which `d2de1f7` made 13:33:29.
- The correcting row is itself rewritten in place, while unmerged.
- **Fix, forward:** one line: the word's row read *13:3x* until `d2de1f7` made it 13:33:29, and the raise row was
  13:31:26 throughout.

**R16 · P3 · confidence high · FM-036's text still claims a superseded row was kept under the table.**
- Its *What is true now* still reads *the seat struck the morning's row from the table and kept its text under it*. Its
  own interim rule, five lines below, says nothing under the table survives.
- The ship-log row says *`--related` listed FM-032, FM-019, FM-028 and FM-027 first*. The list is FM-032, FM-030, FM-019,
  FM-027, FM-016, FM-028.
- **Fix, forward:** correct the sentence, and give the list as printed.

**R17 · P3 · confidence high · FM-005's restoring row misdates the pass it restores, and re-dates the judgement.**
- *unchanged from the pass of 09-24*: FM-005's pass was 09-23 (`14f8fd6`, `keep P1 #4 wait`, *…the shadow week runs on it
  until 09-29*). The 09-24 sheet has no FM-005 row.
- The command set `triaged:` from 2026-09-23 to 2026-09-25 on a verdict called unchanged, which moves the weekly
  re-judgement from 09-30 to 10-02.
- Its cells are not marked one by one, as the other hand rows now are.
- **Fix, forward:** 09-23 in the Reason; the re-dating said, or accepted in words; the marks.

**Verdict on 38cd89e: NOT READY — R14 is P2.**
- R4, R9, R10, R12 and R13 are closed. R11 is not (R15).
- R15–R17 are P3, fixed forward or with R14.
- The sheet is stable (three runs apply nothing), the replays converge, every gate is green, and merge-tree against
  `origin/main` is clean.

The Owner lands this by merging; a merge rules nothing.

## Pass on 84fddb7 (2026-09-25 15:23 CEST, Reviewer, session `8e509911/reviewer-11`)

**Scope.** The tip is `84fddb7` (`84fddb751d7df8681396c2673d55798aaf10bdda`), one commit by the principal seat (15:17:25)
after `2909c55`. It touches FM-030 (one ship-log row), FM-036 (`considered:`, its body, and its ship-log row), TRIAGE.md's
paragraph, and FM-005's row on the sheet. **Tier: docs, one pass.** **Independence:** same session (`8e509911`),
reported.

**What I ran at `84fddb7`.**
- **`--triage` three times on a clean clone:** each run exits 0 with *0 trackers to judge* and *Applied nothing*, and the
  tree is clean after each. Nothing is under the table ✓.
- **Replay from `38cd89e`** with the tip's sheet: *Applied nothing*. No command-owned key changed in this commit; the
  differences are the seat's text alone ✓.
- **Gates:**
  - `--check` 0 (*85 verdict(s)*; *20 open*) and `--session-check` 0;
  - the generator leaves the tree clean;
  - `test_shoalmark.py` 394 ok, `test_core.py` 148 ok;
  - `git merge-tree` against `origin/main` is clean (tree `689df99`).
- **Against `origin/fm/035-ci-green-on-every-platform`** (`4e4d63b`), INDEX.md and TRIAGE.md conflict, as before. The
  resolution is mechanical.
- **Leaks:** no consumer bug id, day or name remains in TRIAGE.md or in any added line ✓.

**R14–R17.**
- **R14 closed:** the paragraph quotes the morning row as it stands at `f34de1e`.
  - The verdict, `keep #3 P1 build`, is byte-identical to that row's Verdict cell.
  - The reason (780 bytes) is byte-identical to its Reason cell with the cell's two asterisks removed. They set *What is
    true now* in italics, which cannot be nested inside the paragraph's italic quotation.
  - The 09-24 reason and the bug id are gone.
- **R15 closed:** the correcting row now reads *the raise row read 13:31:26 from the start; the word's row first read
  13:3x and was corrected … to 13:33:29*. That is true to `bd81954`, `ff30d2d` and `d2de1f7`.
- **R16 closed in its text:** FM-036 now says the superseded verdict is quoted in the pass's paragraph. The listing is R18.
- **R17 closed:** FM-005's row names its judgement of 09-23 (`14f8fd6`) and says the command dates every applied row
  today.
  - Its *kept on 09-24 too* has no record: there is no 09-24 row and no 09-24 paragraph for FM-005. Its #4 simply stood.
    Noted, not graded.

**R18 · P3 · confidence high · FM-036's `considered:` now leaves out the tracker the tool ranks closest.**
- The ship-log row: *`--related` listed, in its order, FM-027, FM-003, FM-019, FM-009, FM-015*.
  - That is the title search run before the filing, whose six hits all tie at 0.6 (FM-010 is the sixth), so their order
    is arbitrary.
  - `--related FM-036` prints FM-032 7.1 · FM-030 6.0 · FM-019 4.7 · FM-027 4.0 · FM-016 3.7 · FM-028 3.4.
- `considered:` went from *FM-030, FM-032, FM-019, FM-028, FM-027* to *FM-030, FM-027, FM-003, FM-019, FM-009, FM-015*.
  That drops FM-032, which the sheet's derived cell marks *NOT considered* at 7, and the Reason still does not open it.
- **Fix, forward:** `considered:` keeps FM-032, or the Reason says why it is not the same work. The ship-log row names
  which query it reports.

**R19 · P3 · confidence high · Two copies of the morning verdict are still in the wrong word order.**
- FM-030's Reason on the sheet reads *The morning's verdict for this tracker (`keep P1 #3 build`)*.
- FM-036's hook reads *the morning pass's `keep P1 #3 build`*.
- The row reads `keep #3 P1 build`, as the paragraph now quotes it.
- **Fix, forward:** `keep #3 P1 build` in both.

**Verdict on 84fddb7: READY WITH FINDINGS (R18, R19 P3).**
- No P2 remains. The sheet holds one filled row per tracker, and three runs apply nothing.
- FM-030 is #1, FM-029 #2, FM-036 #3 and FM-005 #4. FM-007 is P1 `owner` and unranked, with line 6 weighed.
- The displaced morning row is quoted byte for byte. The raise line is the Owner's paste of 13:31:26, and 13:33:29 is
  true.
- Every gate is green, and merge-tree against `origin/main` is clean. The CI branch, which lands first, leaves a
  mechanical conflict in INDEX.md and TRIAGE.md for whoever merges second.
- R18 and R19 are fixed forward under the docs tier.

The Owner lands this by merging; a merge rules nothing.
