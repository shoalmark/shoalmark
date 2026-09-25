# Review — FM-030 raised and re-judged the same day, at f8d2cfd (2026-09-25 07:23 CEST, Reviewer, session `8e509911/reviewer-6`)

- **Branch:** `fm/030-raised-two-acts-with-no-button`, tip `f8d2cfd` (`f8d2cfd8c6dc97ff84e100e90b3c8bfed1289bf4`), two
  commits on `origin/main` `a77798b` (PR 62's merge), both by the principal seat (`Session: 8e509911`,
  `Worktree: shoalmark-principal-3`):
  - `76b3ea2` 07:08:44 — FM-030's `## Raised` section with the Auditor seat's line, one ship-log row, INDEX's date;
  - `f8d2cfd` 07:09:32 — the same-day pass: today's worksheet, FM-030's and FM-018's front matter, INDEX, one paragraph
    under *Passes*.
- **Tier: docs, one pass.** `git diff --name-only origin/main...HEAD` names 5 files, all under `work-tracker/`: FM-018,
  FM-030, INDEX, TRIAGE.md and the worksheet. No `shoalmark.py`, no test, no configuration, no hook. Under FM-032's
  tiers a finding below P2 is fixed forward; a P2 sends it back.
- **Independence:** this verdict is by a sub-agent of the same session as both commits (`8e509911`; this seat
  `8e509911/reviewer-6`). `--check` will count it *same session*. Reported, not refused.

## What I ran

| run | result |
|---|---|
| the Principal's transcript: the record holding *two acts owed to the Owner have no button* stamped `2026-09-25T05:06:48` | the `enqueue` record at `05:06:48.151Z`, its content the line in a code fence. A second record with the same stamp (an attachment) seen by type and time only, not read |
| that line against FM-030's `## Raised` bullet at `76b3ea2` and at `f8d2cfd` | byte-identical after the bullet's `- ` (364 bytes; the one non-ASCII character is `·`) |
| a scratchpad clone at `76b3ea2` (signers file configured), no worksheet for today, `--triage` | exit 0, *0 trackers to judge*, *Applied nothing*. The worksheet it writes has no row, and its ten lines are byte-identical to the branch's header |
| that clone, `f8d2cfd`'s worksheet copied in, `--triage` | exit 0, *Applied 2: FM-018: rank #3 freed — FM-030 holds it now · FM-030: keep #3 P1 build*. FM-018, FM-030, INDEX and the worksheet byte-identical to `f8d2cfd`; the one difference left is TRIAGE.md's paragraph, which the command does not write |
| positive control: 0.18.3's tool (`d79949f`, not on main) on that clone at `76b3ea2`, `--triage` | *1 trackers to judge*: FM-030, marked RAISED. Its derived row against the hand row: R1 |
| `--triage` on the tip (the clone at `f8d2cfd`) | exit 0, *0 trackers to judge*, *Applied nothing — no new filled rows*; `git status --short` empty after it |
| `--owner` at `a77798b`, `76b3ea2` and `f8d2cfd` | the three outputs identical, *NOTHING NEEDS THE OWNER.* — the defect the raise names, which a pass does not change |
| `python3 shoalmark.py --check` | exit 0; *61 verdict(s) · independent 2 · same session 56 · untraced 3*; *filing freeze: 18 open* |
| `python3 shoalmark.py --session-check` | exit 0 |
| `python3 shoalmark.py` at the tip, and in the clone at `76b3ea2` | 34 trackers; the tree clean after it both times |
| `python3 shoalmark.py --next` | #1 FM-029 build · #2 FM-007 P1 owner · #3 FM-030 P1 build · #4 FM-005 P1 wait · #5 FM-006 · #7 FM-028 · …; no rank held twice; #6 empty |
| `test_shoalmark.py` | exit 0, 355 ok, all green |
| `test_core.py` | exit 0, 148 ok, all green |
| `git merge-tree --write-tree origin/main HEAD` | clean: the tree is the tip's own (`f44d0d0`); `a77798b` is the merge base |
| `git show -s --format='%h %ad %G?'` on every sha cited | `9e48ee8` 2026-09-24 18:59:10 `G`, *FM-033: accepted - a raise naming a signed rule re-judges the tracke…* (PR 59); `97fa87a` 2026-09-24 21:32:35 `G`; `7521116` 2026-09-22 19:36:25 `G`; `d79949f` 2026-09-25 06:58:39 |

## The checks

**1. The raise line is the Owner's paste, word for word — ✓; confidence high.**
- The `enqueue` record's `05:06:48.151Z` is 07:06:48 CEST, as the section's note and the ship-log row say.
- Its content, the fence stripped, equals the bullet's text byte for byte, at both commits.
- The line's own facts hold in git: FM-032's answer `97fa87a` at 2026-09-24 21:32:35, signed; FM-007's `7521116` on
  09-22, signed. They are the Auditor's; checked, not graded.
- The ship log gains one row and no row is edited.

**2. Every front-matter change is the command's — ✓; confidence high.**
- `76b3ea2` changes no front matter: body lines and INDEX's date only.
- `f8d2cfd`: FM-030 `triaged: 2026-09-24 → 2026-09-25`, `rank: 6 → 3`, `tier: P2 → P1`; FM-018 loses `rank: 3`. The
  replay writes exactly these and nothing else.
- FM-030's `next: build` stands from 09-24; the verdict names it again, and nothing changes.

**3. The worksheet — ✓ generated with no row, ✓ the row hand-written and marked as the seat's, ✗ in part on its derived
cells (R1); confidence high.**
- The tool on main cannot list FM-030: its judgement of 09-24 is fresh, it is no new filing, and main has no RAISED.
  The generated sheet has no row, as the pass says.
- The row is marked as the seat's twice: the Closest cell (*the seat's cell: the tool derives Closest and RAISED from
  0.18.3 on*) and the Facts cell (*this row written by hand by the Principal seat*).
- Last worked on, keep test, Tier and Story are what 0.18.3 derives: *2026-09-25 · keep · RAISED*, P2, —.
- **The Now cell** is the `## Raised` bullet verbatim, its `- ` included. The raise line is what follows the marker
  (R1).

**4. The verdict `keep #3 P1 build` — ✓ tier, ✓ rank, ✓ move; two sentences of the Reason go further than the record
(R2); confidence medium-high.**
- **Tier against the path:** *P1 — on the current path, line 1: the sitting runs with acts owed that no list shows,
  and line 5's signed answers cannot be acted on through the board*. The raise names path 1, and the scale the command
  prints makes what the path names P1. Line 5 is argued through FM-032's answer, whose act (*until FM-007's hardware
  key*) has no route to happen.
- **Rank:** *#3, the next build after 0.18.3's items (FM-029 #1, in review)*; #2 is FM-007, the Owner's act. FM-018,
  `next: wait`, gives up #3 under the rule the command prints: *what cannot be worked on now … is not ranked ahead of
  what can*.
- **Move:** `build`. None of the three lists is built on main, and the Reason names the slice, for 0.18.4.
- The verdict parses as written, and the command applied it.

**5. TRIAGE.md — ✓; confidence high.**
- `git diff origin/main -- work-tracker/TRIAGE.md` adds two lines under *Passes*: the paragraph and a blank line. The
  intent and the current path are byte-identical.
- **Path 5 kept:** the paragraph's last line reads *The pass commit is the seat's judgement, dated today; the Owner
  lands it by merging.* No merge is read as a ruling. Main's tool still prints *4. The Owner rules by merging the pull
  request*; 0.18.3's `f44e7f9` changes that, and the paragraph follows the path, not the old line.
- Its facts hold: 07:06:48, `9e48ee8`, FM-030 kept P1 #3, FM-018's #3 freed. It does not give FM-030's former P2 #6
  (R3).

**6. Times — ✓; confidence high.**
- No `≈` and no *about* in any added line or in either commit message.
- The seat's one clock time, 07:06:48, is the transcript's 05:06:48Z plus two hours. The line's 21:32:35 is
  `97fa87a`'s own. *09-24* is FM-030's ship log; *09-22* is `7521116`.

**7. Gates — ✓; confidence high.** `--check` 0, `--session-check` 0, the generator clean, both suites green, merge-tree
clean, `--triage` on the tip *Applied nothing* with exit 0, `--owner` unchanged.

## Findings

**R1 · P3 · confidence high · The hand row departs from the tool's derivation in five cells, and three of them are not
marked.**
- The control is 0.18.3's tool on `76b3ea2`, which prints FM-030's row itself. Against it:
  - **Title:** the hand row reads *… before the act*. The title is 70 characters, and both tools print a title of 70
    in full: *… before the act is done*. Two words are dropped, with no `…`. Not marked.
  - **Hook:** in full, 340 characters, where the tool cuts at 220 with `…`. Not marked, and harmless.
  - **Now:** the bullet with its `- `. 0.18.3's `raise_lines` strips the marker, so the tool's Now is the raise line
    alone. The evening pass accepted the same form on FM-007 (*Now equals the `## Raised` line byte for byte*). Not
    marked.
  - **Closest:** *—*, marked as the seat's. The tool derives FM-029 (15 in 0.18.3; `--related FM-030` on main puts
    FM-029 first, at 23.6). In the tool's grammar *—* says no open tracker is close. The evening pass's R6 allowed a
    marked cell, and FM-007's row then carried the derived value.
  - **Facts:** no `reads 2.2k`, and seat prose (*In Progress since 09-24 for 0.18.3's second widening (B)*) in the
    column the header calls *derived, not judged*. Covered by the row's hand-written mark.
- No front-matter effect: the command reads the Verdict cell alone, and the replay is byte-identical.
- **Fix, forward:** none to this sheet. Until 0.18.3 lands, a hand row copies the tool's derivation cell for cell, or
  marks each cell it does not; from 0.18.3 the tool writes the row.

**R2 · P3 · confidence medium · Two sentences of the Reason go further than the record; the tier stands on line 1
without them.**
- *the FM-007 doorway stays open exactly as long as this stays unbuilt*: the doorway closes with the Owner's key,
  FM-007's act (#2, `owner`, `7521116`). A build of FM-030 lists that act; it does not close the doorway, and he can
  close it before the build. What holds: *while this is unbuilt, no list shows the act that closes it*.
- No line on P0, the scale's first test (*harm to people who use it today, or the current path is blocked now*),
  where the evening pass's FM-007 row had one (its R9). A ground exists: the raise itself put both acts in front of him
  at 07:06:48, and the record shows no sitting blocked by them.
- **Fix, forward:** the next pass words the doorway as FM-007's act, and gives the not-P0 ground as a fact the record
  holds.

**R3 · P3 · confidence high · The paragraph and the row leave out two states.**
- *What it changed:* the paragraph says FM-030 was *kept, P1 … ranked #3*, not that it was P2 #6. `--next` now runs
  #5 → #7 with #6 empty. An empty rank is allowed (the day's R10: *not a constraint*); the record still says from what
  to what.
- *0.18.3 build E is in review* (the paragraph, the Facts cell, the Reason): at 07:09:32 its review had returned
  NOT READY at 06:58:39 (`d79949f`, R1 P2), so the build is back with its builder. The half the row leans on,
  *not on main*, holds.
- **Fix, forward:** the next pass's paragraph names the from and the to, and says *returned NOT READY* where a review
  has.

## Verdict

**READY WITH FINDINGS (R1, R2, R3 P3).** No P2: the raise line is the Owner's paste byte for byte, every front-matter
change is the command's, and every gate is green. The P3s are fixed forward under the docs tier.

What holds:
- Every path is under `work-tracker/`; the tier is docs.
- `76b3ea2` files the raise word for word; its note and its ship-log row give 07:06:48, true to the transcript.
- Replayed on `76b3ea2` with the branch's worksheet, FM-018, FM-030, INDEX and the worksheet come out byte-identical to
  `f8d2cfd`.
- `keep #3 P1 build` is judged against the path (line 1, line 5), the rank against the printed rule, the move from what
  is left.
- `--triage` on the tip applies nothing and exits 0; `--owner` is unchanged; TRIAGE.md gains one paragraph and keeps
  path 5.

Carried, not re-graded:
- FM-005, `next: wait`, holds #4 ahead of four builds (#5, #7, #9, #10): the R10 fix review's *the first pass's two
  waits, #3 and #4, still sit ahead of builds*. This pass cures #3. FM-005's judgement is fresh until 09-30, and #4 is
  not a raise pass's to change.
- FM-029 holds #1; its 0.18.3 work returned NOT READY at 06:58:39.
- FM-030's *What is true now* still opens *nothing is built*, which is true on main.

Not verified:
- The Auditor seat's own record behind the line. It is sealed, and the brief bars it; the line is checked against the
  Owner's paste alone.
- The second transcript record stamped 05:06:48 (an attachment): seen by type and time, not read.
- That the Principal ran `--triage` rather than typing the front matter: inferred from the byte-identical replay.

The Owner lands this by merging; a merge rules nothing (path 5).

## Pass on 7a1bbc2 (2026-09-25 07:34 CEST, Reviewer, session `8e509911/reviewer-6`)

**Scope.** Tip `7a1bbc2` (`7a1bbc281c1a7e4fea3fb6f8af3a44a6f3f3bd35`): one merge commit by the principal seat (`Session:
8e509911`, 07:27:51), parents `702d99f` (the verdict above) and `1fe880a` (`origin/main`: PR 64 and PR 66, landed at
07:25:16 and 07:25:32). The merge base is `a77798b`. `git diff --name-only origin/main HEAD` names the same six paths
under `work-tracker/`. **Tier: docs, one pass.** **Independence:** same session `8e509911`, reported.

**The resolution — ✓; confidence high.**
- Main and the branch both changed two files: FM-030 and INDEX. Every other file main changed (AGENTS.md, FM-007,
  FM-029, FM-031, two review files) is byte-identical to `1fe880a` in the merge. Every other file the branch changed is
  byte-identical to `702d99f`. No file changed that neither side changed.
- **FM-030:** main added one ship-log row (2026-09-24, the 0.18.4 subject-cut line, PR 64). The merge is `702d99f`'s
  FM-030 with that row inserted directly after the 09-24 *In Progress* row, before the 09-25 *Raised* row. Checked as
  bytes: nothing else changed. `git diff 7a1bbc2^2 7a1bbc2` on FM-030 shows only the branch's front matter, the
  `## Raised` section and its row.
- **INDEX:** the merge's equals `702d99f`'s. Main's only INDEX change was the header's date, which the branch had too.
  The generator leaves it unchanged on the merged tree.

**What I ran at `7a1bbc2`.**
- `--triage` in the scratchpad clone: exit 0, *0 trackers to judge*, *Applied nothing — no new filled rows*; the tree
  clean after it.
- `--owner` at `1fe880a` and at `7a1bbc2`: *1 NEED THE OWNER* both; the one difference is the sessions line, which
  counts this seat's verdict commit on the branch.
- `--check` 0 (*67 verdict(s) · independent 2 · same session 62*; *18 open*); `--session-check` 0.
- `python3 shoalmark.py`: the tree clean after it.
- `git merge-tree --write-tree origin/main HEAD`: clean, the tip's own tree (`4decdb0`); `origin/main` is an ancestor.
- `test_shoalmark.py` 0 (355 ok); `test_core.py` 0 (148 ok).

**Verdict on 7a1bbc2: READY WITH FINDINGS (R1–R3 P3, carried).** The merge brings main in and changes nothing of the
pass. R1–R3 stay fixed forward.

The Owner lands this by merging; a merge rules nothing (path 5).
