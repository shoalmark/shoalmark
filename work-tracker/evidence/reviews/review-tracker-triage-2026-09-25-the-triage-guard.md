# Review — the pass of 2026-09-25, the triage guard, at 511451a (2026-09-25 19:29 CEST, Reviewer, session `8e509911/reviewer-14`)

- **Branch:** `tracker/triage-2026-09-25-the-triage-guard` (PR 80), tip `511451a`
  (`511451a5289ff5e5c2441c8fe9d65afe792c2cd6`). It has three commits on `b336a53` (PR 78's merge), all by the principal
  seat (`Session: 8e509911`, `Worktree: shoalmark-principal`):
  - `8b0877f` 19:03:56: FM-037 filed, and the pass applied by `--triage` from today's worksheet;
  - `6725b28` 19:04:33: FM-037 set In Progress, with one ship-log row (AU-20);
  - `511451a` 19:04:48: one paragraph under *Passes* in TRIAGE.md.
- **Main moved during this review.** `origin/main` is now `63fabb6`: PR 77 merged at 19:08:43 (R1).
- **Tier: docs, one pass.** `git diff --name-only origin/main...HEAD` names 14 paths, all under `work-tracker/`: FM-005,
  FM-006, FM-024, FM-028 … FM-030, FM-033 … FM-037, INDEX, TRIAGE.md and the worksheet. There is no `shoalmark.py`, test,
  configuration, hook or new key. The pass changes no rule and no code; the build it ranks is critical three ways under
  line 3 (the gate, signing and rights, P1), and that build is not this review. A P2 sends it back.
- **Independence:** same session — 8e509911's own sub-agent, reported. `--check` will count this verdict *same session*.

## What I ran

| run | result |
|---|---|
| `shasum -a 256` on the paste file | `12e77e72…c74bf`, the brief's hash |
| the paste file against the Principal's transcript: the user record stamped `2026-09-25T16:58:54.543Z`, its pasted content | byte-identical; 16:58:54Z is 18:58:54 CEST ✓ |
| FM-037 lines 27–39 (`## Why`) against the paste, with `cmp` | byte-identical, 13 lines; the sha256 of those lines is the paste's |
| the tool's derivation: a scratchpad clone at `b336a53`, FM-037 with the four triage keys stripped, main's worksheet, then `--triage` | *1 trackers to judge*; FM-037's generated row (check 3, R6) |
| a scratchpad clone at `b336a53`, signers file set, FM-037 as above, the worksheet of `8b0877f` copied in, then `--triage` | exit 0, *Applied 11*. Every `FM-*.md`, INDEX.md and the worksheet are byte-identical to `8b0877f` |
| the same clone, a second `--triage` | *0 trackers to judge*, *Applied nothing — no new filled rows*; the tree unchanged |
| the worksheet's filled rows, counted per tracker | 12 rows, none for a tracker twice: the 11 this pass wrote, and FM-007's row from the second-raise pass, unchanged, which applies nothing |
| `git diff 8b0877f 511451a` | FM-037's `status: Proposed` → `In Progress` with one ship-log row, INDEX, and TRIAGE.md; nothing else |
| sha256 of TRIAGE.md's head, *The intent*, *The current path* and *Passes*, at `b336a53`, `63fabb6` and `511451a` | the first three are identical at all three commits. *Passes* differs by one paragraph and one blank line, inserted first |
| `git log` on TRIAGE.md since 00:00 | three other paragraphs of 2026-09-25 under *Passes*, all by the Principal seat (R3) |
| `python3 shoalmark.py --check` | exit 0; *INDEX.md is up to date — 37 trackers*; *judged before build: on*; *filing freeze: 21 open, at or above 8 — only bug filings*. FM-037 is `tags: bug` |
| `python3 shoalmark.py --session-check` | exit 0 |
| `python3 shoalmark.py` | exit 0; `git status --short` empty |
| both suites, as the pre-commit hook runs them (`python3`, then `/usr/bin/python3`) | exit 0 on 3.14.3 and 3.9.6: `test_shoalmark.py` 399 ok, *0 checks skipped*; `test_core.py` 148 ok |
| `--next` | #1 FM-037 … #10 FM-033; each rank held once, 1–10 contiguous; `START WITH: FM-037` |
| `git merge-tree --write-tree b336a53 511451a` | clean |
| `git merge-tree --write-tree origin/main 511451a` (`63fabb6`) | **exit 1:** conflicts in FM-006 and INDEX.md; FM-030 auto-merges (R1) |
| a scratchpad merge of `63fabb6`, resolved as briefed (FM-006 takes PR 77's text, with this pass's `triaged:` and `rank: 6`; INDEX regenerated), then `--triage` | *Applied 1: FM-006: keep P2 #6 build*. The run rewrites `next: owner` → `build`, `--owner` prints NOTHING NEEDS THE OWNER, and `--check` exits 0 (R1) |
| the same merge, the FM-006 row made `keep P2 #6 owner` (control for R1's fix) | `--triage` applies nothing, `next: owner` stays, and `--owner` prints *1 NEED THE OWNER* |
| `--queue`, before 19:29 | `PR 80  wait: conflict in …FM-006…, work-tracker/INDEX.md` |
| `--related FM-037` | FM-019 10.2 · FM-014 7.1 · FM-022 6.6 · FM-033 5.0 · FM-009 4.9 · FM-029 4.2 (R6) |
| a fresh clone at `511451a` without `allowedSignersFile`, `--check` | exit 4: one line for the checkout's own finding, and *INDEX.md is up to date*. FM-034's fix holds (R4) |
| `git log` on the two sections of TRIAGE.md at `b336a53`, commit by commit, with `%G?` | six `G` commits, `45198d5` … `ad9bf67`; `ae1f05e` is `N`, a rename with no text change; two merges, `1e6c333` (`N`) and `57aac8d` (`E`), each carries one parent's text (R7) |
| the Principal's transcript, the user record stamped `17:12:15Z` (after the tip) | the Auditor seat's AU-13 and a second point, both P3 (R2, R3) |

## The checks

**1. FM-037's body: ✓ on every point the brief names. Confidence 99%.**
- **Why:** it holds the paste word for word, all 13 lines, byte-identical, under a header that gives the time and the
  hash. The time 18:58:54 is the transcript's own.
- **`considered:`** is filled: FM-008, FM-033, FM-007, FM-019, FM-022. The paragraph under the paste says what each
  was held against. The one the tool ranks closest and does not find there is FM-014 (R6).
- **Done when:**
  - it names the seven clauses by reference (*The seven clauses of the Owner's word above, as written*), each with its
    synthetic test, and clause 7;
  - it names the tier: *the gate — critical under path line 3; the Owner's cold session reviews it; the Auditor seat
    verifies after, against its plan sealed at 18:57:38*.
- **Ship log:** two rows:
  - the filing, at 18:58:54, with the pass's verdict;
  - In Progress, set on the pass branch before the first build commit, citing AU-20.
- **Hook and title:** both are the paste's *Title:* line.
- **What is true now:** its history claim holds commit by commit (see the table).

**2. The worksheet and the front matter: ✓ at `511451a` against its base; ✗ after main's move (R1). Confidence 99%.**
- **Replay:** `--triage` applied from `b336a53` reproduces `8b0877f` byte for byte, in every tracker, INDEX and the
  sheet. A second run applies nothing.
- **Every changed key is a row:**
  - FM-037: `triaged: 2026-09-25`, `rank: 1`, `next: build`, `tier: P1`, above `hook:`, in `apply_verdict`'s order.
  - FM-030 #2, FM-029 #3, FM-036 #4, FM-005 #5, FM-006 #6, FM-035 #7, FM-028 #8, FM-024 #9, FM-033 #10.
  - FM-034: `rank:` removed, and `triaged:` re-dated.
  - FM-006, FM-024, FM-028, FM-033 and FM-034 also have `triaged:` re-dated, as the command dates every row it
    applies (R5).
- **By hand:** only FM-037's `status: In Progress`, in `6725b28`, with its ship-log row. The command never writes that
  key, and the schema lets the working seat set it.
- **The sheet:** one filled row per tracker, which is what FM-036 needs. There are twelve rows, not eleven: FM-007's
  row stays from the second-raise pass and applies nothing.

**3. The rows themselves: honest in verdict, not in the derived cells. Confidence high (R6).**
- The six rows this pass added (FM-037, FM-006, FM-028, FM-024, FM-033, FM-034) are written by hand:
  - Hook, Now and Facts are `—`;
  - Closest is *— (the seat's cell)*;
  - none of them says *written by hand*.
- FM-037 is the one row the tool generates today, and the hand row replaced it. The generated row carries:
  - *NEW FILING*;
  - the hook, and the opening of *What is true now*;
  - `repos — · reads 1.2k`;
  - *closest: FM-019 (10, Shipped) ✓ · FM-014 (7, Shipped) NOT considered · FM-022 (7, Shipped) ✓*.

**4. TRIAGE.md: ✓ on scope, ✗ on three facts (R3). Confidence 99% on scope.**
- The head, *The intent* and *The current path* are byte-identical at `b336a53`, at `63fabb6` and at the tip.
  *Passes* gains one paragraph, first, as its header asks (*Newest first*).
- **This is exactly what FM-037 will enforce, and here nothing enforced it.** The only guard on the two sections today
  is a seat's own restraint. The byte comparison above is the check FM-037 will make.
- **Against the sheet and the filing:**
  - 18:58:54 ✓;
  - the Auditor seat's AU-12, the local probe on `b336a53`, and the plan sealed at 18:57:38 ✓ (the paste);
  - the superseded FM-030 verdict, *keep P1 #1 build*, is quoted as main's sheet has it ✓;
  - the ranks ✓;
  - FM-034's reason, *its fix shipped in v0.18.3* ✓. That is true (`447469a`, the CHANGELOG's 0.18.3 section), and
    it is why the verdict should have been `fix` (R4).
- Three phrases are wrong: *of this morning*, *the only line of this file a seat wrote today*, and *every ranked
  tracker moved down one* (R3).

**5. Gates: ✓ against the base, ✗ against main now. Confidence 99%.**
- `--check` exits 0 with the freeze line, and FM-037 is a bug filing, which the freeze admits.
- `--session-check` exits 0.
- Both suites are green on both Pythons, as the hook runs them.
- Every path is under `work-tracker/`.
- Merge-tree is clean on `b336a53`. On `63fabb6` it conflicts in FM-006 and INDEX.md (R1).

**6. The judgement: P1 ✓ (85%), #1 ✓ (85%).**

Line 3, whole: *A pull request merges only with a review's evidence file on its head: a Reviewer from another
independent session for critical changes (critical = a release, the gate or hooks, signing and rights, TRIAGE.md or
AGENTS.md rules changed by a seat, anything tagged security or P1); inline Reviewer passes on other code; one Reviewer
pass for documentation; a review of the Owner's own answers and TRIAGE lines reports and never blocks, until FM-007's
hardware key signs them. The Owner merges on a ready line, or over any other verdict with a signed reason.*

**The tier.** The command's scale is *P0 harm to people who use it today, or the current path is blocked now · P1 on
the current path*.
- Not P0. On this main, every change to the two sections is his signed commit, the probe was never pushed, and
  nothing is blocked.
- P1, because the path names it three times:
  - its own header, *only the Owner changes it* (which FM-037 turns from a written rule into a checked one);
  - line 5, *the Owner's signed mandate* (the path is his signed word);
  - line 3's critical list, *TRIAGE.md … rules changed by a seat*.
- The intent's *for* says the same: *writable only for those with the rights to do so*.
- The row's Reason says *a rule of his own path* and names no line. It should have named the header. That is noted
  here, not graded.
- Line 3 also sets the build's review: the gate, signing and rights, and P1 each make it critical. *The Owner's cold
  session reviews it* is a Reviewer from another independent session. ✓

**The rank.** His own words are *let's fix this first then* (R2).
- #1 is, in the command's words, *THE FIRST ITEM TO WORK ON NEXT … working order*. That is the plain expression of
  *first*.
- FM-030 has harm today and sits on lines 6 and 1. The rule puts harm *after the path's own work*, and both trackers
  are the path's work, so the order between them is working order, and he gave it.
- His word is not a signed answer (path 5). A rank is the seat's judgement, and *the Owner ranks it* counts. If he
  disagrees, the seat re-makes the row on his word.
- The filing's own gloss is weaker than the rank: *before the 0.18.4 release is cut, this guard is in it*. FM-030 is in
  0.18.4 too, so the gloss would not order the two. The rank, not the gloss, is the honest reading.
- The rest moved down one, and FM-034 left: its fix is shipped (R4). The rank holds a slot for work that is done
  nowhere else.

## Findings

**R1 · P2 · confidence 99% on the facts, 90% on the grade · The branch conflicts with main, and the briefed resolution
would take his open ask off his list.**
- PR 77 (`63fabb6`, 19:08:43) changed FM-006's front matter and body. It set `next: owner` with the go-public ask
  (`ask-kind: action`, since 2026-09-25). This branch changed FM-006's `triaged:` and `rank:` in the same hunk.
  INDEX.md conflicts too.
- The sheet's FM-006 row is `keep P2 #6 build`. If the merge keeps PR 77's text and only this pass's rank, the front
  matter says `owner` and the row says `build`. That is a verdict the front matter does not reproduce.
- Reproduced in a scratchpad merge, the next run of `--triage` today:
  - applies the row and rewrites `next: owner` → `build`;
  - `owner_queue` needs `next == "owner"`, so `--owner` prints *NOTHING NEEDS THE OWNER* while his ask stands;
  - `--check` exits 0.
- That breaks path line 6 on the very tracker that asks him when the tool goes public.
- **Fix, as briefed and one step more:**
  - the Principal merges `origin/main` into the branch; never a rebase;
  - FM-006 keeps PR 77's text and front matter, with `triaged: 2026-09-25` and `rank: 6`;
  - **the sheet's FM-006 row becomes `keep P2 #6 owner`**, and its Reason says the ask came with PR 77;
  - INDEX.md is regenerated;
  - `--triage` then applies nothing, and `--owner` lists FM-006;
  - the merged head is verified again under `## Verified again` below.

**R2 · P3 · confidence 95% on the fact, 80% on the grade · The Owner's word is attributed as the relay wrote it (the
Auditor seat's AU-13, its own error, which arrived at 19:12:15, after the tip).**
- The Auditor seat's correction: his own words at 18:55:33 were *`stop a seat from editing your TRIAGE.md` - let's
  fix this first then*, with spelling normalised. The part in backticks quotes the Auditor seat's line of the minute
  before. The relay of 18:58:54 wrote the two as one.
- The *Why* is right to hold the paste byte for byte: the paste is the record of what reached the seat. But other
  places present *stop a seat from editing your TRIAGE.md — let's fix this first* as *his word*:
  - the paragraph;
  - FM-037's ship-log row;
  - the Reasons of FM-037 and FM-030.
- Not P2. The branch misquotes nothing it was given. His meaning and his order are unchanged: he quoted the line
  and ordered it fixed first. The *your* in the sentence already shows that the words were addressed to him.
- **Fix, forward:**
  - the correcting row AU-13 gives, on FM-037's build branch;
  - the attributions stay as filed, pointing at it.

**R3 · P3 · confidence high · The paragraph's account of itself.**
- *This paragraph is the only line of this file a seat wrote today* is false. The Principal seat wrote the other three
  paragraphs of 2026-09-25:
  - `f8d2cfd`, 07:09;
  - `42f4eca` → `c8939e3`, 12:15–12:30;
  - `b430d7e` → `84fddb7`, 13:36–15:17.
  
  What is true is *the only change this branch makes to this file*.
- *its verdict of this morning on this sheet, keep P1 #1 build*: that verdict is the afternoon's (`b430d7e`,
  13:36:05). The morning's was `keep #3 P1 build` (`f8d2cfd`), and the paragraph just below calls that one *the
  morning's*.
- *Every ranked tracker moved down one*, which is also `8b0877f`'s subject: FM-034 left the ranks at #10 instead. The
  sheet says so correctly. This is the Auditor seat's second point of 19:12:15.
- **Fix:** R1 sends the branch back anyway, so the three phrases can be put right in their own commit.

**R4 · P3 · confidence 95% on the fact, 80% on the verdict · FM-034 is kept `build` for work that has shipped.**
- The row's own Reason says its fix shipped at v0.18.3. It did: `447469a`, the CHANGELOG's 0.18.3 section. A fresh
  clone without the signers file prints the checkout's line once, and *INDEX.md is up to date*.
- The rules name this case: `fix`, *its status is simply wrong (merged code says Shipped). BY HAND: correct it, cite
  the commit*.
- `build` means *code or a document still has to be written by a seat*, and none is.
- The tracker still says *nothing is built*, and the board shows it under *progress*.
- **Fix, forward:** `fix`: Shipped, citing `447469a` and `v0.18.3`, with a ship-log row. Do it in R1's re-make, or at
  the next pass.

**R5 · P3 · confidence high on the fact, 70% on the grade · Five inherited judgements are dated today.**
- Five rows read *re-ranked … unchanged otherwise*, and the command dates each one `triaged: 2026-09-25`:
  - FM-006, from 09-23;
  - FM-024, FM-028, FM-033 and FM-034, from 09-24.
- The rules say *EVERY KEEP CARRIES A TIER JUDGED TODAY … An inherited tier is no judgement*.
- The concrete cost is FM-024 #9 `owner`:
  - his act, a cold Reviewer session on 0.18.3, is done: `01a0d6e7`, `e3aa64e`, READY at 10:29:27;
  - the answer is uncleared and the move is stale;
  - it is now dated as judged today, so the 7-day window lists it on 10-03, not 10-02.
- **Fix, forward:**
  - FM-024's row is re-judged: the seat that acted clears the answer, and the move is read again;
  - a line under the freeze in FM-036, the same-day sheet's tracker: a row that only moves a rank should not re-date
    the judgement.

**R6 · P3 · confidence high · The hand rows replace the tool's cells, unmarked, and the new filing's closest tracker
is not opened.**
- Check 3 has the cells.
- The NEW FILINGS rule says *OPEN every one marked NOT considered*. FM-014 is marked so, and `--related FM-037` ranks
  it second (7.1). It is the rights gate: `transitions` and `rights_problems` judge which seat may change what, and
  refuse the rest. That is the class of FM-037's guard, and possibly its home in the code.
- FM-014 is in neither `considered:` nor the Reason.
- FM-007's carried row still reads *FM-030's defect, #1 above*.
- Hand rows that depart from the derived cells were found before. The morning's R1, and R6 of the second-raise pass's
  review, said: copy the tool's cells, or mark each one that is not the tool's.
- **Fix, forward:**
  - FM-037's `considered:` gains FM-014, or its Why says why the rights gate is not the same work;
  - the next hand row copies the derived cells or marks each one.

**R7 · P3 · confidence 70% · Two of the Owner's clauses meet on `ae1f05e`, and line 3 reads differently after the
build.**
- **`ae1f05e` against clauses 1 and 7:**
  - `ae1f05e` (holgo99, `%G?` N, 2026-09-22) renames TRIAGE.md from `docs/work-tracker/` to `work-tracker/`.
  - Clause 1 refuses a commit that *deletes or moves TRIAGE.md* unless it is the Owner's signed commit.
  - Clause 7 requires `ae1f05e` accepted.
  - Accepting it rests on a reading the clauses do not state: *no text change*, or *before signing existed*, or *on
    the base*.
- **The two merges:** the history also holds `1e6c333` (Implementer seat, `N`) and `57aac8d` (`E`). Each changes the
  sections against one parent, and clause 1's merge rule accepts both, but clause 7 does not list them.
- **Line 3 after the build:** it calls *TRIAGE.md … rules changed by a seat* a critical change to be reviewed. Once
  FM-037 is built, the gate refuses that change to the two sections outright.
- The words are his, and no seat changes them or picks a reading. The filing did not raise the question. His *never*
  covers *a potential misunderstanding … never questioned*.
- **Fix, forward:** the build's plan states the reading for `ae1f05e` and the merges. Line 3's clause is his to settle,
  as an ask if he wants one. The Auditor seat's sealed plan may already hold both.

## Verdict — NOT READY (R1 P2), 90%

**NOT READY.**
- At `511451a` against its base, the pass is sound:
  - the filing holds his paste byte for byte;
  - the sheet reproduces every front-matter change, and a second run applies nothing;
  - the Owner's two sections are untouched;
  - every gate is green;
  - P1 #1 is the honest reading of *let's fix this first*.
- Main has since moved to `63fabb6`, and the branch cannot land on it. The resolution must re-make FM-006's row to
  `owner`, or the next run of `--triage` hides his open ask (R1).
- R2–R7 are P3, fixed forward under the docs tier. R3 and R4 can ride in R1's re-make.
- After the merge, this file gains `## Verified again`, on the merged head.

Not verifiable here:
- The plan sealed at 18:57:38; its hash is with the Owner.
- The Owner's own words behind the relay beyond what AU-13 states. I read the Auditor seat's correction, not his line.
- The probe on `b336a53`; it was never pushed.

## Verified again on f2f03f5

**Scope.** `f2f03f5` (`f2f03f5da89d357ec230db76a8ef5d36190df530`), two commits on this verdict's `886a4b7`, both by the
principal seat (`Session: 8e509911`):
- `4cdbfcf` 19:37:29 merges `origin/main` `63fabb6`. Its parents are `886a4b7` and `63fabb6` ✓, and it is a merge, not a
  rebase.
- `f2f03f5` 19:38:01 fixes R3 and R6.

Same tier, docs, one pass; same session, reported. Verified by 19:51 CEST.

| run | result |
|---|---|
| `git show --remerge-diff 4cdbfcf` | FM-006 is resolved to PR 77's front matter with `triaged: 2026-09-25` and `rank: 6`, and `next: owner` stays. INDEX.md takes the pass's board, with FM-006 as `owner`. The merge also changes the sheet's FM-006 row, a file with no conflict, to `keep P2 #6 owner`; its Reason names the R1 correction, and the merge's subject says so |
| `git diff 63fabb6 f2f03f5` on every `FM-0*.md` | the pass's `rank:` and `triaged:` lines, and FM-037, and nothing else; FM-030 keeps main's 0.18.4 line (`1429785`) with `rank: 2` |
| a scratchpad clone at `f2f03f5`, signers file set, `--triage`, run twice | *0 trackers to judge*; *Applied nothing — no new filled rows* both times; the tree clean |
| that clone, `--owner` | *1 NEED THE OWNER*: FM-006, action, *When and how does shoalmark go public?* ✓ R1 |
| that clone, `python3 shoalmark.py` | the tree clean, so INDEX.md is byte-identical to the regenerator's output; the same in this worktree |
| `--next` | #1 FM-037 … #6 FM-006 `owner` … #10 FM-033; each rank held once; `START WITH: FM-037` |
| sha256 of TRIAGE.md's head, *The intent* and *The current path*, at `63fabb6` and `f2f03f5` | identical (`2f8d9d60…`, `74ff308a…`, `a100dbd4…`); *Passes* differs by the one paragraph |
| FM-037 lines 27–39 against the paste | still byte-identical |
| `--check` | exit 0; *INDEX.md is up to date — 37 trackers*; *judged before build: on*; *filing freeze: 21 open …* |
| `--session-check` | exit 0 |
| both suites, as the hook runs them | exit 0 on 3.14.3 and 3.9.6: 399 ok and 148 ok |
| `git diff --name-only origin/main...HEAD` | 15 paths, all under `work-tracker/` (this review is the fifteenth) |
| `git merge-tree --write-tree origin/main HEAD` | exit 0, clean; `63fabb6` is an ancestor of the tip |

**The findings on 511451a:**
- **R1 ✓ closed.** FM-006 keeps his ask at `next: owner`, rank 6. The sheet row says `owner`, so the next `--triage`
  run leaves it alone, and `--owner` lists the ask.
- **R3 ✓ closed, with one new slip (R8).** The paragraph now reads:
  - *The ranked trackers moved down one and FM-034 left the ranks*;
  - *its verdict of 13:36*;
  - *FM-034 out of the ranks*;
  - *the two sections above `## Passes` are untouched — the very thing FM-037 will enforce*.
- **R6 ✓ closed for FM-014.** FM-037's `considered:` gains FM-014. The Why's list says *FM-014 (the rights gate — the
  seat rights this guard reads)*. `--check` accepts the change under the triage right. The hand-row marking is not
  fixed, and is carried to the next hand row.
- **Carried, not fixed here (P3):**
  - R2 goes on FM-037's build branch as its first commit: the Auditor seat's own correcting row, AU-13.
  - R4, R5 and R7 go to the next pass and to the build brief:
    - FM-034 marked `fix`, Shipped;
    - the five re-dated rows, and FM-024's stale `owner`;
    - `ae1f05e` against clauses 1 and 7, and line 3 after the build.

**R8 · P3 · confidence high · The paragraph points the wrong way.**
- The new sentence says *This paragraph, like the three above it, is a seat's*.
- *Passes* is newest first, and this paragraph is the first under the heading (line 29). The other three paragraphs of
  2026-09-25 are below it (lines 31, 33, 35), and nothing above it is a pass paragraph.
- **Fix, forward:** *below it*, at the next touch of this file by a seat.

**The merge's own change, not a finding.**
- `4cdbfcf` edits the worksheet, a file that had no conflict. Under FM-019 that is the merger's own change, and the
  merge's subject names it.
- The replay above shows it is the only content the merge adds beyond its two parents' resolutions.

## Verdict on f2f03f5 — READY WITH FINDINGS (R8 P3; R2, R4, R5, R7 carried P3), 90%

- R1, the only P2, is closed: the merge is clean against `origin/main`, and his go-public ask stands on `--owner`
  after a fresh `--triage`.
- INDEX.md is the regenerator's own output.
- The Owner's two sections are byte-identical to main.
- Every gate is green.
- R3 and R6 are fixed. R8 is new and P3. R2 goes on the build branch; R4, R5 and R7 go to the next pass and the build
  brief.

*the Owner lands this by merging; a merge rules nothing.*
