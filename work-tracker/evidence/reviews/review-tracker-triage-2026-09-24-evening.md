# Review — the evening re-run of the 2026-09-24 pass and three asks, at a3ff174 (2026-09-24 20:25 CEST, Reviewer, session `8e509911/reviewer-2`)

- **Branch:** `tracker/triage-2026-09-24-the-raise`, tip `a3ff174` (`a3ff1743e8b3b3de9e6fb6c7d13b99af2d636f7d`), seven
  commits on `origin/main` `5bd3ad5` (PR 59's merge, `v0.18.2`), all by the principal seat (`Session: 8e509911`,
  `Worktree: shoalmark-principal`), 19:44:49 → 19:53:41:
  - `d1618dc` FM-034 filed;
  - `29466fc` the pass re-run: two rows added to the day's worksheet, the paragraph under *Passes*;
  - `6e3afb4` FM-033's fifth case and FM-030's second widening;
  - `7ba62ea`, `3b83966`, `db8a57a` FM-030, FM-033 and FM-034 set to In Progress;
  - `a3ff174` three asks, on FM-031, FM-032 and FM-024.
- **Tier: docs, one pass.** `git diff --name-only origin/main...HEAD` names 10 files, all under `work-tracker/`: FM-007,
  FM-024, FM-030 … FM-034, INDEX, TRIAGE.md and the worksheet. No `shoalmark.py`, no test, no configuration, no hook, no
  new key. A finding below P2 is fixed forward; P2 or above sends it back; a defect in an ask's text is P2.
- **Independence:** this verdict is by a sub-agent of the same session as every commit on the branch (`8e509911`; this
  seat `8e509911/reviewer-2`). `--check` will count it *same session*. Reported, not refused.

## What I ran

| run | result |
|---|---|
| `python3 shoalmark.py --triage` on the tip | **exit 4.** *NOT applied — fix the Verdict cell and run again: FM-032: `keep P2 #10 wait` — #10 is already claimed by FM-034 on this sheet*; *Applied 2: FM-024: keep P2 #8 build · FM-031: keep P2 wait*, which write `next: owner` → `build` and → `wait`. Discarded with `git checkout -- .` (R1) |
| `--owner` before and after that run, in a scratchpad clone at `a3ff174` | *3 NEED THE OWNER* → *1 NEED THE OWNER* (FM-032 alone) |
| a scratchpad clone detached at `d1618dc` (FM-034 filed, no pass yet), `--triage` on main's worksheet | FM-034's row generated, its eight derived cells equal to the branch's row cell for cell; *1 trackers to judge*: FM-007 is not listed, as its row says (no raised tracker is listed yet) |
| that clone, the branch's worksheet of `29466fc` copied in, `--triage` | *FM-032: rank #10 freed — FM-034 holds it now · FM-034: keep P3 #10 build · FM-007: keep #2 P2 owner · FM-033: keep P2 #9 build*, and the same *NOT applied* line for FM-032. Every tracker and the worksheet byte-identical to `29466fc`; INDEX differs only by the clone's signature-lint lines |
| the three Verdict cells of R1's fix, tried in the clone at `a3ff174` | exit 0, *Applied nothing — no new filled rows*, `--owner` still 3 |
| `python3 shoalmark.py --check` | exit 0; *57 verdict(s) · independent 2 · same session 55*; *filing freeze: 18 open* |
| `python3 shoalmark.py --session-check` | exit 0 |
| `python3 shoalmark.py` | 34 trackers; the tree clean after it, so INDEX is the generated one |
| `python3 shoalmark.py --next` | #1 FM-029 build · #2 FM-007 owner · #3 FM-018 wait · #4 FM-005 wait · #5 FM-006 build · #6 FM-030 build · #7 FM-028 build · #8 FM-024 owner · #9 FM-033 build · #10 FM-034 build; each rank held once; `START WITH: FM-029` |
| `python3 shoalmark.py --owner` | 3 NEED THE OWNER: FM-024 action, FM-031 ruling, FM-032 ruling; nothing sent back |
| `test_shoalmark.py` | exit 0, 355 ok, all green (Python 3.14.3) |
| `test_core.py` | exit 0, 148 ok, all green |
| `git merge-tree --write-tree origin/main HEAD` | clean; `5bd3ad5` is an ancestor of the tip |
| a clone without `allowedSignersFile`, `--check` | `work-tracker/INDEX.md is STALE — a tracker changed without regenerating` beside the signers lint: FM-034's defect, reproduced |
| `git show -s --format='%h %ci %G?'` on every sha the branch cites | checks 5 and 10 |
| the parent project, read-only (`git show`, `git log --all`) | `d7657081` 19:48:27 and its three ask rows; PR 812 and PR 813; FEAT-190's scorers |
| the Principal's transcript, entries of `type == "user"` only | the Owner's pastes at 17:10:48Z, 17:28:28Z and 17:37:25Z (check 6); one timestamp, 12:38:29Z, listed without its content (check 5) |

## The checks

**1. Every front-matter change came from `--triage`, none by hand — ✓ for every key the command owns; confidence high.**
- FM-007: `triaged: 2026-09-23` → `2026-09-24`, nothing else. `rank: 2`, `tier: P2` and `next: owner` are main's.
- FM-034 (filed on this branch): `triaged: 2026-09-24`, `rank: 10`, `next: build`, `tier: P3`, above `hook:`, in the
  order `apply_verdict` writes them.
- FM-032: `rank: 10` removed by the command's freeing loop (*rank #10 freed — FM-034 holds it now*), not by its own
  row, which the command refused (R1).
- FM-033: `next: owner` → `build`, the afternoon's `keep P2 #9 build` re-applied. **Right.**
  - Its second ask is a ruling, answered: `9e48ee8`, signed `G`, 18:59:10.
  - `owner_queue` already drops an answered ask, so `owner` only mislabelled the move (the Auditor's check 24).
  - The act the answer calls for is a same-day re-judgement, which is FM-007's row in this pass; listing a raise is
    FM-033's 0.18.3 build. That work is `build`.
  - Not cleared: `--clear-ask` records the act and belongs to the seat that finishes it. A note, not a finding.
  - The row's Reason is the afternoon's. The evening's reasoning is in the paragraph and the commit, which is enough.
- By hand, and allowed: `status: In Progress` on FM-030, FM-033 and FM-034; the five ask lines and `next: owner` on
  FM-024, FM-031 and FM-032. The schema writes `ask:` *with `next: owner`*, by the seat that needs the Owner.
- ✗ in consequence: the day's worksheet and the asks now disagree, and the command says so (R1).

**2. FM-007's same-day re-judgement — ✓ on rank and move, ✗ in part on the tier; confidence medium.**
- The row's cells against the tracker:
  - The hook is FM-007's in full; a generated row cuts it at 220 characters.
  - The Now cell paraphrases the `## Raised` line. It leaves out the key's fingerprint, the two shas and the sources,
    under a parenthesis that reads *word for word from the draft*. That is true of the tracker's line, not of the cell
    (R6).
  - The Facts cell's *answered 2026-09-22, the act his* matches `7521116` (`G`): *accepted - a hardware key that needs a
    touch*.
  - *Last worked on* 2026-09-24 is what the tool derives (`0f0766e`, 18:08:20).
  - The Closest cell says *FM-033 (—)*. The tool derives FM-001 (4) (R6).
- The Reason argues from the raise line:
  - *the raise names a signed rule, path 5, and FM-033's answer* is the line's *undermines*.
  - *the key sits in a shared agent* is the line's fact.
  - *the session gate keys his exemption on the author string* is true: `session_problems` skips a commit whose
    `seat_of(name, email)` is `owner`.
- `owner` is the right move. The answer is a promise, and the act, a key that needs a touch, needs his hands alone
  (FM-030's own line). The *Done when*'s third closure, the tripwire in the tool, is seat work that this move does not
  show. The next pass may say whether it waits behind his key.
- The tier: the raise names path 5, and the scale the command prints makes what the current path names P1. The Reason
  argues the rank (*nothing on the board that only his hands can close is more urgent*), not the tier (R4).
- `keep #2 P2 owner` parses as written (token order is free), and the command applied it.

**3. The three asks — ✗, two P2 (R2, R3); confidence medium.**

| | FM-024 | FM-031 | FM-032 |
|---|---|---|---|
| `ask:` | 151 characters, one `?`, at the end ✓ | 156, one `?` ✓ | 140, one `?` ✓ |
| `ask-kind:` | `action` ✓: the proposal needs his hands to start a session | `ruling` ✓ | `ruling` ✗: the proposal needs his hands to write path 3 (R3) |
| `ask-since:` | 2026-09-24 ✓ | 2026-09-24 ✓ | 2026-09-24 ✓ |
| options | 3, of 48, 73 and 82 characters, distinct ✓; none opens *yes* or *no* ✓; no Auditor option (AU-18) ✓ | 2, distinct ✓; the strike option gone (AU-19) ✓; option 1 names *the scorer*, option 2 opens with *no* ✗ (R2) | 3, of 118, 50 and 73, distinct ✓; none opens *yes* or *no* ✓; option 1 conditional on FM-007's key (AU-11) ✓ |
| `ask-proposal:` | option 1, verbatim ✓ | option 1, verbatim ✓ | option 1, verbatim ✓ |
| answerable by an option or by changed text | ✓: each option is one of the question's three | ✓ | ✓ |
| no trap he cannot sign | ✓: option 3 defers; slice 2's own verdict would still need a second session, but it can be signed | ✓ | ✓ |

- `--check` exits 0, and `--owner` lists all three. The gate sends none back; it checks the form, not these points.
- The parent project's ledger row came first for each: `d7657081` 19:48:27, before `a3ff174` 19:53:41.
  - FM-031's and FM-032's questions there are the board's. FM-031's reads *in FM-031's body* for *in this tracker's
    body*.
  - FM-024's is not. The ledger asks a yes-or-no question: *Will you start a cold Reviewer session for 0.18.3's
    verdict, so it is not this session's own — FM-024's slice 2 by your hand until it is built?* The board asks *Who
    verifies 0.18.3 …?* with three options.
  - That is the parent's record, not this branch's, so it is not graded. It matters if the shadow week scores his
    answer against the ledger's wording.

**4. The nine rules in FM-031's body — ✓ open, ✓ rule 9, ✗ in part on another repository; confidence medium.**
- Recorded as open: *neither ruled nor, until this line, recorded … None is signed. As proposed, for the Owner's
  ruling*. ✓
- Rule 9 is *No message to a session the Owner stopped*, AU-10's rule. ✓
- The parent project appears as its PR numbers (812, 813), its ledger and one id, D11. That is within what FM-029's R7
  allows: an id. Two things go further:
  - Rule 8's *the scorer* is the parent's FEAT-190 scorer. No scorer is defined in this repository, and the ask's
    option 1 carries the same term (R2).
  - Rule 9's parenthesis tells the parent's incident in a sentence (R6).
- No secret, no path and no content from another repository's files.

**5. FM-033's fifth case — ✓; confidence high.**
- `git diff origin/main -- work-tracker/FM-033-*.md` adds 12 lines and removes 2. Both removed lines are front matter,
  `status:` and `next:`. No body line is removed or changed, so the Auditor's sentences and its table of four are
  byte-unchanged.
- The row against git:
  - `137d9ba` 10:17:59 (`G`) ✓. `140f799` 14:24:00 (`G`), *the relation only — no new verbs* ✓.
  - `4dfb999` 15:12:28 ✓. Its parent is `095f1d3` = `v0.18.0`, where FM-029 reads `status: Proposed`, `next: owner`,
    and has no `triaged:` ✓.
  - `68eeee6` 15:24:50, 12 min 22 s after the build began ✓. `87bac4e` 15:19:52, 7 min 24 s after ✓. `7d3e632`
    14:49:42 ✓.
  - `v0.18.1` is on `1251f84`, PR 53 merged 16:25:41 ✓. `65f37a4` 16:29:09 (`G`) ✓.
- *forty minutes after he pointed at the board*: the Auditor's own body puts the board at 14:32 (`:62`), and 14:32 →
  15:12:28 is forty minutes ✓.
- *the Owner's own word at 14:38*: a user message stands in the transcript at 12:38:29Z. I did not read it.
- *a violation, not a miss — his class* follows AU-13.

**6. The Auditor's words, where quoted — ✓; confidence high.**
- Set as the Auditor's own words:
  - *never take up work that is not ready*: check 26 at 17:10:48Z, *your intent's "never take up work that is not
    ready"* ✓.
  - *no message to a session you stopped*, in FM-031's ask: AU-10 at 17:28:28Z ✓.
- Paraphrased and credited, each true to the paste: check 26 (*P2, 80%*), check 18 (*neither ruled nor recorded as
  open*), checks 20, 21, 24 and 27, and AU-11, AU-12, AU-13, AU-17, AU-18, AU-19, AU-20 and AU-22.
- FM-024's row gives AU-17's parenthesis as *one session's own sub-agents*. `--check` says 54 of the 55 are
  `8e509911`'s and one is `e8e309df`'s (R6).
- AU-18 … AU-24 are at 17:37:25Z, as the feedback on a rejected tool call. No user entry after 17:28:30Z carries *Plan
  approved*.

**7. FM-030's second widening — ✓ on the exception, ✗ in part on the move; confidence medium.**
- It says what 0.18.3 builds: after `--answer`, `next:` leaves `owner`.
- It excepts action asks: *`next: owner` stays, because the act is still his (this tracker's own line: the answer is a
  promise, not the act)*. That agrees with the hook, *For an action ask the answer is a promise, not the act*.
- It records AU-22's rule for `--schema`.
- The move it names, `next: run`, is not what the move rules give after a ruling on unbuilt work. It is also not what
  this pass wrote for FM-033 tonight (R5).

**8. The three In Progress commits — ✓; confidence high.**
- Each changes one tracker's `status:`, adds one ship-log row and regenerates INDEX. Nothing is outside
  `work-tracker/`, and no other key changes.
- Each says why: *0.18.3 builds it … the status set here, on the pass branch, before the first build commit (the
  Auditor's AU-20)*.
- FM-007 stays `Proposed`, `next: owner`: the act is his.

**9. TRIAGE.md — ✓; confidence high.**
- `git diff origin/main -- work-tracker/TRIAGE.md` adds two lines under *Passes*: the paragraph and a blank line. The
  intent and the current path are byte-identical.
- The paragraph reads no merge as a ruling: *The pass commit is the seat's judgement, dated today; the Owner lands it
  by merging.*
- Its facts hold: PR 59 and 18:59:10; check 27 at 19:10; FM-007 kept #2 P2 `owner`, by hand; FM-034 #10 P3 `build`;
  FM-032's #10 freed; FM-033's `next:` re-applied.
- It does not say that FM-032's own row was refused (R1).

**10. Times — ✓; confidence high.**
- There is no `≈` in any added line or commit message.
- From git: 10:17:59, 14:24:00, 14:49:42, 15:12:28, 15:19:52, 15:24:50, 16:25:41, 16:29:09 and 18:59:10; the parent's
  `d7657081` 19:48:27.
- From the transcript, UTC + 2: 19:10 (17:10:48Z), 19:28 (17:28:28Z) and 14:38 (12:38:29Z).
- From the Auditor's filed body: 14:32, the board.

**11. Gates — ✓; confidence high.**
- `--check` 0, `--session-check` 0, `test_shoalmark.py` 0 (355 ok), `test_core.py` 0 (148 ok).
- `git merge-tree` against `origin/main` is clean.
- `--triage` is not a gate, and it fails (R1).

## Findings

**R1 · P2 · confidence high on the facts, medium-high on the grade · The day's worksheet no longer applies: `--triage`
on the tip exits 4, and a run today takes two of the three asks off the Owner's list.**
- **What:** the sheet holds FM-034's `keep P3 #10 build` and, below it, the afternoon's `keep P2 #10 wait` for FM-032.
  - `apply_worksheet` refuses the second: *#10 is already claimed by FM-034 on this sheet; a rank names one tracker*.
    The run exits 4 with *NOT applied — fix the Verdict cell and run again*. The code's own comment is *a pass that
    leaves the ledger failing its gate does not exit 0*.
  - FM-032 lost its rank through the freeing loop, not through its own row. Any run on this sheet prints the refusal:
    the replay on `d1618dc` does.
- **Then the asks:** `a3ff174` set `next: owner` on FM-024, FM-031 and FM-032 by hand, as an ask must.
  - The day's rows still name `#8 build` for FM-024 and `wait` for FM-031, and today's sheet is re-applied whole.
  - On the tip, `--triage` writes FM-024 `next: build` and FM-031 `next: wait`. `owner_queue` keys on `next: owner`,
    so `--owner` goes from *3 NEED THE OWNER* to *1*. Reproduced in the scratchpad clone.
  - FM-032's ask survives only because its row is refused. The obvious fix to that row, `keep P2 wait` (as FM-031's
    was on the day's R10), would take its ask off the list too.
- **When:** until midnight. From 2026-09-25 this is an older sheet, and it reaches no tracker that carries `triaged:`.
- **Why P2:**
  - The pass is left in the state its own command calls unfinished.
  - Its record gives FM-032 a rank that the tree does not hold.
  - The next run today, by any seat, silently takes two open questions off his list: *a seat that is left without
    its answer*, FM-030's class.
  - The bar the brief set for this pass was *Applied 0, or re-applications with no diff*.
- **Fix:**
  - In the worksheet, each asked tracker's Verdict cell names the move the ask left, or no move:
    - FM-024 `keep P2 #8 owner` (or `keep P2 #8`);
    - FM-031 `keep P2 owner` (or `keep P2`);
    - FM-032 `keep P2 owner` (or `keep P2`), with no `#10`.
  - Run `--triage` until it prints *Applied nothing* and exits 0. Tried in the clone: exit 0, *Applied nothing — no
    new filled rows*, and `--owner` still lists 3.
  - Add one clause to the paragraph: FM-032's row re-written, the asks' moves kept.

**R2 · P2 · confidence medium · FM-031's options: option 1 names the parent project's scorer, and option 2 opens with
*no*.**
- **Option 1**, the proposal: *the nine hold as written; the scorer reads messages by them*. (confidence 70%)
  - No scorer is defined in this repository. FM-023 and FM-029 speak only of *a* scorer, in general.
  - The one this means is the parent project's FEAT-190 scorer. The parent's ledger row for this same ask lists *the
    scorer's reading of peer messages (protocol §3)* under *Blocks*.
  - A signed *accepted* would rule, in shoalmark, how another repository's component reads. That is a second decision
    the question (*Which rules hold …?*) does not ask, and no seat here can build or verify it: *a tasking never able
    to finish*. Rule 8 in the body carries the same term.
  - He can answer with changed text. But an ask cannot be fixed after it is answered, and the record keeps *accepted*
    against the option's words.
- **Option 2** opens with *no*: *no rule yet: a message between sessions moves nothing until one is ruled*. (confidence
  55%)
  - Picked, it is signed `accepted - no rule yet: …`. That is the form the FM-033 review sent back: *would have been
    signed as `accepted - no — …`*.
  - Here *no* is a determiner in a *which* question, not a reply, so the harm is smaller than it was there.
- **Fix:**
  - Option 1 reads *the nine hold as written*, and the scorer is left to the parent's own ask. Or it names *the parent
    project's scorer (FEAT-190)*.
  - Option 2 opens otherwise: *none yet: …*, or *until one is ruled, a message between sessions moves nothing*.
  - Rule 8 names whose scorer it is.

**R3 · P2 · confidence medium · FM-032's ask is `ruling`, and its proposal needs the Owner's hands.**
- The proposal ends *— written into path 3*.
  - The current path is the Owner's: *only the Owner changes it* (TRIAGE.md) and *Nobody else edits those two sections*
    (AGENTS.md, rule 7).
  - Its lines were written in his own signed commits: `45198d5`, `c755d31`, `8d14b6b`, `7dd6ba6`.
  - So a *yes* to the proposal is an act of his hands.
- This branch's own FM-030 line (AU-12, AU-22) says *an ask whose yes needs his hands is `action`, whatever else it
  decides*, and that for one *`next: owner` stays*.
  - As a `ruling`, 0.18.3's `--answer` would write `next: run`, and the path-3 edit would leave his list. That is the
    defect FM-030 records.
  - `--standup` shows it under RULINGS, not under YOUR HANDS.
- The other two options need no act of his: a Reviewer pass, or the tool's refusal, built by a seat.
- **Fix:** `ask-kind: action`. Or re-word option 1 so that no edit of the path follows a *yes*, if the seat means
  something else by *written into path 3*.
- **Why only medium:** the schema's own word for `action` is *hands only the Owner has*, and a path edit is his by rule,
  not by credential. AU-22's rule is what makes it `action`. It is recorded here as what `--schema` will say; `--schema`
  does not say it yet.

**R4 · P3 · confidence medium · The rows do not judge two tiers against the path.**
- **FM-007:**
  - The raise names path 5 as undermined, and the scale the command prints says *P1 on the current path*.
  - The Reason keeps P2 on an argument about the rank.
  - The raise rule is *re-judges the tracker the same day*, and that includes its tier.
- **FM-034:**
  - Its own *Why* says *The Owner's path, line 1 … a `--check` that says STALE on a clean clone is a failed run*.
  - It is kept P3, *someday*, while 0.18.3 builds it tonight.
  - The Reason's ground is size (*small — one function's routing*). Size is not on the scale the command prints:
    *P0 harm … · P1 on the current path · P2 next · P3 someday*.
  - Either the Why over-reaches, because the sitting runs in his checkout, which has the signers file, or the tier is
    too low.
- This is the class of the day's R8 (FM-024).
- **Fix, forward:** the next pass judges both tiers against the path in the Reason, or a Principal seat asks. The merge
  decides nothing (path 5).

**R5 · P3 · confidence medium · FM-030's second widening names `next: run` where the move rules give `build`.**
- It says: *for a ruling, a determination or a ceremony the seat's move follows, and 0.18.3 writes `next: run` with the
  answer*.
- The moves the command prints:
  - `run` means *it is built, and what is owed is a run nobody has made yet*.
  - `build` means *anything else: code or a document still has to be written*.
- The case the widening cites is FM-033. This pass gave it `build` tonight; the tool as recorded would have written
  `run`.
- After a ruling on unbuilt work the rules give `build`. After a determination, `run` often fits.
- **Fix, forward:** 0.18.3's build B writes the move the rules give, or leaves the move to the seat that acts on the
  answer, and FM-030 says which. The build's own full loop reviews it.

**R6 · P3 · confidence high · Details in the record.**
- **FM-024's ask row:** *55 of this week's 57 verdicts are one session's own sub-agents*.
  - `--check` counts 55 as *same session*: 54 by `8e509911`'s sub-agents and one by `e8e309df`'s.
  - *Same session* means each branch's own session, not one session. AU-17's parenthesis says it loosely, and the row
    sharpens it the wrong way.
- **FM-007's hand-written row:**
  - Its Closest cell reads *FM-033 (—)* where the tool derives FM-001 (4).
  - Its Now cell paraphrases the `## Raised` line under *word for word from the draft*.
  - A row written by hand stands in for a derived one. It carries what the tool would derive, or it marks the cell as
    the seat's.
- **FM-031, rule 9:** the parenthesis tells the parent project's incident in a sentence. The parent's PR numbers
  already point to it.
- **Fix, forward:** a correcting line, not an edit of the ship-log rows.

## Verdict

**NOT READY: R1, R2 and R3 are P2.**
- R1 leaves the pass's own command failing, and one run today takes two open asks off the Owner's list.
- R2 and R3 are in the text of asks, which cannot be fixed after he answers.
- R4–R6 are P3 and are fixed forward.

What holds:
- Every path is under `work-tracker/`, and the tier is docs.
- The command wrote every key it owns. Replayed on `d1618dc`, the trackers and the worksheet come out byte-identical to
  the pass commit.
- FM-033's `next: build` is right.
- FM-034's derived cells are the tool's, and FM-034's defect reproduces in a clone without the signers file.
- FM-033's fifth case: the Auditor's text is byte-unchanged, and every sha and time is true to git.
- The three In Progress commits are tracker-only and say why. FM-007 stays Proposed.
- TRIAGE.md: one paragraph added, the intent and the path untouched, and no merge read as a ruling.
- FM-024's ask as a whole. The options AU-18 and AU-19 removed are gone, and FM-032's option 1 waits on the key
  (AU-11).
- Every time is sourced, and there is no `≈`.
- `--check` 0, `--session-check` 0, both suites green, and `merge-tree` clean.

Carried from the day's review file, not this branch's and not re-graded here:
- R4: four parks on rows that pass the keep test.
- R8: FM-024's tier against path line 3.
- The R11 control clause: the addendum's *the Owner's strike is the independent control* and FM-033's Reason *the Owner
  strikes the row* (AU-21).
- FM-029 still holds #1 for work shipped in `v0.18.1`.

Not verified:
- What the Owner said at 12:38:29Z (*his own word at 14:38*). I read only its timestamp.
- The *Plan approved* message. It is not among the transcript's user entries.
- The Auditor's draft behind FM-007's `## Raised` line. It is sealed, and the brief bars it.
- That the Principal's own `--triage` run printed the refusal. This is inferred from the replay of the pass's own sheet.

The Owner lands this by merging, and **a merge rules nothing** (path 5): his disagreement with a row is his word to the
seat, which re-makes the pass, or his signed answer.

## Pass on cb1d05e (2026-09-24 20:40 CEST, Reviewer, session `8e509911/reviewer-2`)

**Scope.** Tip `cb1d05e` (`cb1d05ed47b15677a28704196c2d351949d912d3`): two commits by the principal seat, under
`8e509911`, on `a3ff174`. The verdict above is `ec0f962`, on `review/triage-2026-09-24-the-raise`; this file carries it
word for word, and this pass is on `review/triage-2026-09-24-the-raise-2`.
- `c5696c5` (20:24:50) re-makes the pass on R1 and R4: five Verdict/Reason cells, three of FM-007's derived cells, two
  tiers, the paragraph under *Passes*, FM-034's *Why*.
- `cb1d05e` (20:24:56) re-makes the asks on R2 and R3, and fixes R5 and R6 forward, in FM-024, FM-030, FM-031 and
  FM-032.
- `git diff --name-only origin/main...HEAD` still names the same 10 files under `work-tracker/`. **Tier: docs, one pass.**
- **Independence:** same session `8e509911`, reported; `--check` will count this verdict *same session*.

**What I ran at `cb1d05e`.**
- `--triage`: exit 0, *Applied nothing — no new filled rows*, *0 trackers to judge*; `git status --porcelain` empty
  after it.
- `--owner`: *3 NEED THE OWNER* — FM-024 action, FM-031 ruling, FM-032 action; nothing sent back.
- `--check` 0 (*18 open*; *57 verdict(s) · independent 2 · same session 55*); `--session-check` 0.
- `python3 shoalmark.py`: 34 trackers, the tree clean after it.
- `test_shoalmark.py` 0 (355 ok); `test_core.py` 0 (148 ok).
- `git merge-tree --write-tree origin/main HEAD`: clean; `5bd3ad5` is an ancestor.
- `--next`: #1 FM-029 build · #2 FM-007 P1 owner · #3 FM-018 wait · #4 FM-005 wait · #5 FM-006 · #6 FM-030 · #7 FM-028 ·
  #8 FM-024 owner · #9 FM-033 · #10 FM-034 P2 build; each rank held once; `START WITH: FM-029`.
- **The replay.** In the scratchpad clone at `a3ff174`, with `c5696c5`'s worksheet copied in, `--triage` applied
  *FM-034: keep P2 #10 build* and *FM-007: keep #2 P1 owner* and refused nothing. Every tracker's front matter and the
  worksheet came out byte-identical to `c5696c5`. The one difference is FM-034's *Why*, which the command does not write
  (R8).
- The parent project, read-only: its ledger rows for FM-031 and FM-032 follow the asks as re-made at `cb1d05e`
  (`868e6e3e`, 20:28:55), FM-032 as *hands (B)*; its FM-024 row now carries the board's question (`e0113e35`, 20:14:43).
- No `≈` in the two commits.

**The findings of the first pass.**
- **R1 ✓ closed.** The asked rows name `owner`: FM-024 `keep P2 #8 owner`, FM-031 `keep P2 owner`, FM-032 `keep P2
  owner`, each Reason saying *asked … so the move is `owner` while the ask stands*. FM-032's row holds no `#10`. The
  command applies nothing and exits 0, and `--owner` still lists 3. The paragraph says so.
- **R2 ✓ closed.** FM-031's options are *the nine hold as written* (24 characters, the proposal, verbatim) and *until
  one is ruled, a message between sessions moves nothing* (60). Neither opens with *yes* or *no*; they are distinct;
  the question is unchanged. Rule 8 now names *the parent project's scorer (its FEAT-190)*. Picking option 1 still
  signs, in shoalmark, a rule only the parent project carries out; the term is now defined, and he can strike rule 8 by
  changed text.
- **R3 ✓ closed.** FM-032 is `ask-kind: action`, its ship-log row says why (*a yes writes path 3, which only the Owner's
  hands write*), and `--owner` shows it as action.
- **R4 ✓ closed.** Both tiers are judged against the path in the Reason:
  - FM-007 `keep #2 P1 owner`: *on the current path, line 5: an answer is written and signed, and the raise shows the
    signature proves the account, not the hand*. See R9 for its not-P0 and rank grounds.
  - FM-034 `keep P2 #10 build`: *line 1's sitting runs in the Owner's checkout, which has the signers file, so the
    sitting sees no failed run*. True in this worktree, which shares the repository's configuration: `--check` prints
    no signers lint here.
- **R5 ✓ closed.** FM-030's widening says 0.18.3 writes `next: build` after a ruling, a determination or a ceremony,
  *as this evening's pass gave FM-033*; action asks still keep `owner`.
- **R6 ✓ closed.**
  - FM-024 gains a correcting row: *54 of them this session's sub-agents and one another's*, as `--check` counts.
  - FM-007's row: Closest *FM-001 (4)*, what the tool derives; Now equals the `## Raised` line byte for byte; Facts
    says the row is the seat's, written by hand.
  - Rule 9 keeps the pointers only: *the parent project's incident of the morning, PR 812 and PR 813*.

**R7 · P3 · confidence high · The paragraph states two tiers twice.** Its first half still reads *FM-007 … kept #2 P2*
and *FM-034 … kept #10 P3*; its added sentence says *FM-007 P1* and *FM-034 P2*. A reader who stops before the last
sentence reads the tiers the pass withdrew. **Fix, forward:** state the final tiers once, where the rows are named.

**R8 · P3 · confidence high · The pass commit edits FM-034's *Why* by hand, and does not say so.**
- `c5696c5` rewrites FM-034's *Why* (*The sitting itself runs in his checkout, which has the signers file, so it sees
  no failed run — P2, next, not P1*). The replay shows everything else in that commit is the command's.
- A pass writes its reason in the worksheet, not into a tracker. The Principal is FM-034's filing seat, so the
  correction is its to make, and it is right: it ends the contradiction R4 named. But it rides in the pass commit, and
  neither the commit message nor the paragraph names it.
- **Fix, forward:** none to the text. The next such edit goes in its own commit, by the filing seat, named.

**R9 · P3 · confidence medium · FM-007's Reason: the not-P0 ground and the rank ground.**
- *not P0, because nothing has been signed by a hand that was not his*: the record cannot show that. The tracker's
  premise is that a signature cannot tell the hand, and its hook says agent commits were signed as him until it was
  caught. In this repository no seat-authored commit is signed (`git log --all --format=%G?`), which is as far as the
  record goes. What holds is narrower: *no answer is known to have been signed by another hand*.
- *rank #2 stands behind the build at #1: his hands, not a seat's, close it*: the rule the command prints is *an `owner`
  move is work too*. #1 is FM-029, whose build shipped in `v0.18.1` (the carried R10 remainder). `START WITH` skips
  `owner`, so the board's first line does not change.
- **Fix, forward:** the next pass words the P0 test as a fact that exists, and ranks FM-007 against FM-029 once FM-029
  is closed.

**R10 · P3 · confidence medium · Three ship-log rows edited in place.**
- `cb1d05e` rewrites the last rows of FM-030 (`next: run` → `next: build`), FM-031 and FM-032, where FM-024 got a
  correcting row. AGENTS.md rule 1: *only the ship log is append-only*.
- All three rows were written on this branch, never reached `main`, and `a3ff174` keeps their first text, so nothing
  on the trunk is rewritten. Whether an unmerged row is already the log is a reading of the rule, not a fact.
- **Fix, forward:** none to the text; a correcting row next time, as FM-024's.

**Verdict on cb1d05e: READY WITH FINDINGS (R7, R8, R9, R10 P3).** R1–R6 are closed. The P3s are fixed forward under
the docs tier. Carried, not re-graded: the day's R4, R8 and R11 control clause, and FM-029 holding #1 for shipped work.

**For the merge order, not a finding.** This branch holds `cb1d05e` and this file with both verdicts;
`review/triage-2026-09-24-the-raise` (`ec0f962`) holds `a3ff174` and the first verdict alone. Both add this file, so
landing both would conflict on it; this branch contains the whole tracker branch and supersedes the first.

Not verified: the same four items as the first pass. Both new commits are after the pastes; nothing in them quotes the
Auditor beyond what check 6 covered.

The Owner lands this by merging, and **a merge rules nothing** (path 5): his disagreement with a row is his word to the
seat, which re-makes the pass, or his signed answer.
