# Review — the same-day pass after v0.18.4 (FM-002 raised; the release close-out), at 8f98103 (2026-09-26, Reviewer)

- **date:** 2026-09-26, 11:15 CEST.
- **Seat:** Reviewer · **session:** `8e509911/reviewer-23` · **worktree:** `shoalmark-review-5`.
- **Tier: docs, one pass.** `git diff --name-only origin/main...8f98103` names 8 paths, all under `work-tracker/`:
  FM-002, FM-006, FM-034, FM-035, FM-036, INDEX.md, TRIAGE.md and the worksheet. No `shoalmark.py`, test,
  configuration, hook, key or signers file. A P3 is fixed forward; a P2 sends it back.
- **Independence: same session** — Principal session 8e509911's own sub-agent, reviewing its Principal seat's branch.
  Reported as such; `--check` will count this verdict *same session*.
- **Reviewed:** `tracker/triage-2026-09-26-the-brand-raised`, tip `8f981030fe5845861f2c85d752d1e2e4ba207f13`, three
  commits on `origin/main` `a7e5291` (the `v0.18.4` tag), all by the Principal seat (`Session: 8e509911`,
  `Worktree: shoalmark-principal`):
  - `4527ca1` FM-002 raised: `status: In Progress` by hand, `next: owner` and the five `ask*` keys, the Raised line,
    *What is true now*, a ship-log row;
  - `c3bae92` FM-006: the landing-page line and its row;
  - `8f98103` the pass: the worksheet with four filled rows, FM-034, FM-035 and FM-036 set Shipped by hand with a body
    line and a row each, FM-035's `rank:` removed, INDEX.md, one paragraph under TRIAGE.md's *Passes*.
- No pull request is open for the branch (`gh pr list --head …`: none). PR 82 (`fm/006-the-board-s-themes`, head
  `9704140`) is open and edits FM-006 (R2).
- The sources: the Owner's three words as the brief names them, in the Principal's scratchpad — his word of 07:41:00
  through the Auditor seat (pasted 07:55:40), his word of 09:23:58, his word of 10:25:41.

## What I ran

| run | result |
|---|---|
| `shasum -a 256` on the three word files | the paste `34ee13d1…` · the board-header word `21497e4d…` · the *go* word `416d54ce…` |
| the files against the Principal's transcript | the paste: the queued record stamped `05:55:40.139Z` (07:55:40 CEST); its pasted block equals the file, 3,631 characters, `34ee13d1…`; its first line dates the word 07:41:00 through the Auditor seat. The user records `07:23:58.346Z` and `08:25:41.001Z` (09:23:58 and 10:25:41 CEST) are the verbatim lines the other two files quote ✓ |
| `python3 shoalmark.py --triage` on the tip | *0 trackers to judge*; *Applied nothing — no new filled rows*; no row named superseded; `git status --short` empty |
| replay: a scratch clone at `c3bae92`; `8f98103`'s hand edits to FM-034, FM-035 and FM-036 (FM-036's `rank: 4` left in); the sheet copied in; `--triage` as `principal@seat` | *Applied 2: FM-036: rank #4 freed — FM-002 holds it now · FM-002: keep P2 #4 owner*. Every `FM-*.md`, the sheet and INDEX.md byte-identical to `8f98103`; a second run applies nothing |
| the same replay with the three statuses still open | the command also dates FM-034/035/036 `triaged: 2026-09-26` and drops both ranks — not the tip. The seat flipped the statuses first, and `apply_worksheet` skips a tracker that is not open, as its comment says |
| FM-035 with `rank: 7` put back, `--check` | *lint: FM-035: `rank:` is 1–10, on work that is In Progress or Proposed — remove it when the tracker ships* — the lint's word ✓ |
| FM-002's front matter at `a7e5291`, `4527ca1`, `c3bae92`, `8f98103` | `4527ca1` adds by hand `status: In Progress`, `next: owner` and the ask keys; `8f98103` adds `triaged: 2026-09-26`, `rank: 4`, `tier: P2` — the command's (the replay) |
| the ask against the draft in `git show 7344a78:…FM-006…` | ask, options and proposal equal as strings; options 85, 108 and 84 characters; the proposal is the first |
| `--owner` on a clone of the tip | *2 NEED THE OWNER*: FM-006 · action, FM-002 · ruling — on his list (path 6) ✓ |
| `gh run view 36228506657 --repo holgo99/shoalmark` | `v0.18.4`, head `a7e5291`, push, success; five jobs green (ubuntu 3.9 and 3.12, macos 3.12, windows 3.9 and 3.12); each job's log ends *skipped here: 0 checks — every check ran* |
| FM-034: `447469a`, `65d7266`, `4de6320` against `v0.18.3` (`57aac8d`); a fresh clone of the tip without `allowedSignersFile`, `--check` | all three ancestors of the tag. The clone: exit 4, one checkout line on stderr, *INDEX.md is up to date*; this worktree, with the file: exit 0. The suite's FM-034 cases, `test_shoalmark.py:3931–3994` |
| FM-036: `f5c72f7` against `v0.18.4`; `--triage`'s printed rules; the suite | an ancestor of the tag; *ONE TRACKER, TWO ROWS … The LAST filled row in the file is applied* printed; the FM-036 · F cases on FM-030's rows, `:3282–3321` |
| FM-029: `ffa63b8` in either suite; CHANGELOG 0.18.4 | absent from both; *Named for 0.18.4 and not in it* lists *FM-029's real-history relation case for FM-032's record* |
| FM-030 against its *Done when* | `--triage`'s rules still test `run` before `owner` (*even where the Owner must attend it*, `shoalmark.py:3140`); CHANGELOG's not-in-it list names the move after an answer and `--answer`'s cut subject |
| sha256 of TRIAGE.md's head, *The intent* and *The current path* at `origin/main` and the tip | identical (`2f8d9d60…`, `74ff308a…`, `85c20a49…`); *Passes* gains one paragraph, first |
| FM-006's front matter at `origin/main` and the tip | byte-identical (`69f8d577…`); the diff adds 3 lines and removes none |
| `python3 shoalmark.py --check` | exit 0; *INDEX.md is up to date — 37 trackers*; *judged before build: on*; *the Owner's two sections: guarded — 3 commit(s) … none changes them or his signers file*; *filing freeze: 19 open* |
| `python3 shoalmark.py --session-check` | exit 0 |
| both suites by hand, `python3` then `/usr/bin/python3` | 3.14.3 and 3.9.6: `test_shoalmark.py` 462 ok, *skipped here: 0 checks — every check ran*; `test_core.py` 148 ok; the tree clean after |
| `git merge-tree --write-tree origin/main 8f98103` | clean |
| `git merge-tree --write-tree 9704140 8f98103` (PR 82's head) | **exit 1: a conflict in FM-006** (R2) |

## The checks

**1. The worksheet and the front matter: ✓. Confidence 99%.**
- Four filled rows, one per tracker. FM-002's is the tool's own row — *NEW FILING*, the hook, the Now, Facts
  `repos — · reads 1.6k · next owner` — with the Verdict `keep P2 #4 owner` and a Reason that names his three words,
  the tier's ground, the rank's and the move's.
- The three `fix` rows are written by hand. The tool writes no row for a tracker judged on 2026-09-25, so their `—`
  cells stand for nothing derived; their Reasons say what was done by hand.
- `--triage` on the tip applies nothing and names nothing superseded. The replay reproduces the tip byte for byte.
- Every FM-002 key the pass commit adds is the command's. `next: owner` is older: set by hand in `4527ca1` with the
  ask, which the schema lets a Principal do (`--check` 0). The row's `owner` re-applies the same value. The rules say
  to write none where Facts already says `next owner`; here that is harmless.
- FM-034, FM-035 and FM-036 keep `triaged: 2026-09-25`, because the command does not date a tracker that is not open.
  Each body line dates the fix.

**2. The tier and the rank: I read the rules the same way. Confidence 85%.**
- **P2.** The current path's six lines name the sitting, filing, merging, his involvement, answers and his board.
  None names a theme or the site's look. The rule: *What the path does not name is P0 or P1 only if people who use it
  are being harmed today* — nobody is. *P2 next* fits his line for 0.18.5. *P1 the day he writes it into his path by
  his own signed commit* is right: FM-037's guard admits no other writer.
- **#4.** It comes after FM-037 (#1, P1), FM-030 (#2, P1) and FM-029 (#3, P2), each of which can be worked now.
  - The Reason's *into the rank FM-036's flip frees* names a free slot, not an order.
  - The order that holds is the rule's. An `owner` move is work, and this one can be done now. It gates 0.18.5's
    first build (slice A). FM-006's going-public ask (#6) proposes acting after the 09-29 scoring. So #4 ahead of #6
    is working order.
  - *After the two P1 builds*: FM-037's move is `review`.
- **`owner`.** A ruling is his alone. ✓
- **Observed, not this pass's.** #7 is now empty: ranks 1–6 and 8–10, which `--check` accepts. FM-005 (#5, `wait`)
  still ranks ahead of FM-006, FM-028, FM-024 and FM-033, all of which can be worked now. The rule says *what cannot
  be worked on now … is not ranked ahead of what can*. That rank is 2026-09-25's, and this pass judged four rows; the
  next full pass re-ranks.

**3. The ask on FM-002: ✓. Confidence 99%.**
- `ask-kind: ruling`: no hands are needed. `ask-since: 2026-09-26`.
- The three options follow the order of his item 2: the shoalmark theme worn and no themes shipped; both shipped as
  starters with shoalmark worn; not yet. They are 85, 108 and 84 characters, each within his 120.
- The proposal is the first option. `monochrome` is not offered as the worn theme, which was his condition.
- The text equals `7344a78`'s draft as strings.
- The disclosure is in the ship-log row: *the proposal the GtM seat's, disclosed — the cheap step first*. That is the
  reason in four words. `7344a78`'s fuller reason is not carried: one Reviewer pass instead of the code tier, and no
  file `--vendor` copies changes before he rules. Noted, not graded.
- `--check` accepts it. `--owner` lists it.

**4. The Raised line: ✓ on source and reading; R3 on how it is sourced. Confidence 95%.**
- The three times are the transcript's. The two hashes given are the files'.
- The words are quoted as chat words, normalised, and marked as normalised.
- No word is read as an answer (path 5):
  - the ask stands with *not yet* among its options;
  - *nothing is built before his answer*;
  - neither *proceed* (07:41:00) nor *align for both* (09:23:58) is taken as a pick.
- The line says it names no signed rule. Under the RAISED rule, the same-day pass is therefore the seat's choice on
  his *go*, not the rule's. That is honest.

**5. The three flips: ✓. Confidence 95%.**
- **FM-034.** Its *Done when* holds on the tip: a fresh clone gives one finding and no STALE; a configured clone gives
  none; the suite builds both.
  - The body cites `57aac8d`, the `v0.18.3` tag's merge. The fix commits are `447469a`, `65d7266` and `4de6320`; the
    tag carries all three.
  - *Byte-identical … under drift_normalize, the Generated date aside* is the reading `65d7266` wrote, and the body
    states it.
- **FM-035.** Run 36228506657 on `a7e5291`: five of five jobs green, nothing skipped.
  - The three causes are in their fixing commits: `df4c8ab` (CRLF), `29dbd10` (cp1252), and `b6e2030` with `4e4d63b`
    (macOS; the cause stated as inferred).
  - A check that cannot run skips by name.
  - Its R3 is carried as briefed (R4).
- **FM-036.** `f5c72f7` is in `v0.18.4`. `--triage` prints the rule, and the suite tests it on FM-030's rows.
- No Shipped tracker carries `rank:`.
- All three keep `next: build`, as FM-008 and FM-011 do on main: nothing reads a move on done work. Noted.

**6. The six held: two checked, both gaps real. Confidence 85%.**
- **FM-029 is real.** The real-history relation case for FM-032's record (`ffa63b8`) is in neither suite, and
  CHANGELOG lists it as not in 0.18.4.
  - It is a line for 0.18.4 in FM-029's ship log (the Auditor seat's item 2), not a bullet under *Done when*. The
    paragraph's *one Done-when line* names the wrong section; the gap is the right one.
- **FM-030 is real.** I can name three unmet lines:
  - the triage rule split (*Done when*: `owner` tested before `run` for a run only his hands can make);
  - the move after an answer following the picked option (*For 0.18.4*);
  - `--answer`'s cut subject (a ship-log line).
  
  The paragraph does not name its three, so mine may not be the seat's.
- **Not this branch's text.** FM-030's *What is true now* still opens *Filed 2026-09-24; nothing is built*, and that
  line is what `--next` shows at #2. It is false since 0.18.3 and 0.18.4 built A–E. The next seat on FM-030 rewrites
  the opening.

**7. FM-006: ✓, with R2. Confidence 95%.**
- The line states his word, its time 10:25:41, its hash, and *not a signed answer*.
- The seat's reading is marked: *the site's start page unless he says otherwise*.
- *He answers now that v0.18.4 has landed* is his own word.
- The front matter is byte-identical to main's, and the going-public ask is untouched.
- *The mock … is its starting point* reads his *see mockup work* without marking it as a reading. Minor; noted.

**8. TRIAGE.md: ✓ on scope. Confidence 99%.**
- Only *Passes* changes, by one paragraph, placed first. The head and the two sections above are byte-identical, and
  `--check`'s guard line says so. R5 is on the paragraph's text.

**9. Gates: ✓. Confidence 99%.**
- `--check` exits 0 and `--session-check` exits 0.
- Both suites are green on both Pythons.
- merge-tree against `origin/main` is clean.
- Every path is under `work-tracker/`.

## Findings

**R1 · P3 · confidence 99% on the fact, 70% on the grade · FM-002 is In Progress, and its *Done when* is 0.8.0's,
already met.**
- *Why it matters:* the re-opened scope has no done-condition in the section a pass reads when it tests *merged code
  says Shipped*. This same pass flipped three trackers by exactly that test. Read cold, FM-002's *Done when* reads as
  met today: it is the condition its 0.8.0 ship met.
- *The gap:* the slices and the carry-overs are prose in *What is true now*. *Done when* is unchanged since 0.8.0.
- *What closes it:* a *Done when* for the re-opened scope, written before or by the build's pass (FM-033):
  - slice A's lines: the chosen theme worn by the committed board and the built site; AU-16, both clauses (R3);
    AU-18; contrast re-measured on the built files; real renders seen by him before the merge; live at the next tag;
  - slice B's lines only if he rules it;
  - the 0.8.0 lines marked as met.

**R2 · P3 · confidence 99% on the facts, 75% on the grade · Once PR 82 merges, the themes' ask and scope have two
homes, and PR 82 conflicts with this branch in FM-006.**
- *Why it matters:* this branch moves the drafted ask out of FM-006's body and onto FM-002's board. But the body it
  moved from is PR 82's, and PR 82 has not merged.
  - PR 82's FM-006 still says the drafted ask *waits for the going-public ask to be answered*.
  - Its section *The ask, raised when this tracker's open ask is answered … still a draft* sits outside the conflict,
    so it merges silently.
  - A seat that follows it after he answers going public raises the same ask a second time.
  - PR 82's landing line (*nothing is built, and no ask is drafted*) meets this branch's *a requirement of v0.18.5* in
    the conflicting hunk.
- *The gap:* `git merge-tree 9704140 8f98103` conflicts in FM-006, in the top of *What is true now* and in the
  ship-log head. The `evidence/FM-006/themes/` and `9467b83` that FM-002 cites exist only on PR 82's branch.
- *What closes it:*
  - PR 82's branch, or whichever merge of main comes second, says in FM-006's themes section and drafted-ask block
    that the ask was raised on FM-002 on 2026-09-26 and the slices are FM-002's;
  - the conflict keeps this branch's landing-page line;
  - the next pass sees both on main.

**R3 · P3 · confidence 99% on the facts, 85% on the grade · The raise's words are partly outside the record, one
quote drops a sentence unmarked, and a carry-over loses half of AU-16.**
- *Why it matters:* the build's pass and its Reviewer read the tracker, not the Principal's scratchpad. PR 82's
  Reviewer raised the same gap as its R5 (`review-the-boards-themes-record.md`).
- *The gap:*
  - the 07:41:00 and 10:25:41 words are cited by the hashes of files outside the repository;
  - the 09:23:58 word has no hash (its file's is `21497e4d…`);
  - the 10:25:41 quote joins *go — raise FM-002 as proposed* to *for the v0.18.5 release …* with a semicolon, over
    the dropped *FM-006 i will answer after v0.18.4 has landed*. The 09:23:58 quote marks its own cut with *…*;
  - the carry-overs give AU-16 as *every ::before/::after marker with empty alt text* and leave out its second clause:
    *the chart's coordinate labels stay hidden from screen readers, as the refile tested*.
- FM-002 does write the order and the rest of the carry-overs as lines, which answers most of PR 82's R5.
- *What closes it:*
  - the three words filed word for word with their hashes (an `evidence/FM-002/` file, or a block in the tracker);
  - the dropped sentence marked with *…*;
  - AU-16's second clause added. It can land with R1's *Done when*.

**R4 · P3 · confidence 95% on the fact, 70% on the grade · FM-035's R3 is carried on a Shipped tracker, where no
pass and no list reads it.**
- *Why it matters:*
  - the intent's *never* includes *a fix that is forgotten*;
  - `--triage` lists open work, new filings and raises;
  - `--owner`, `--standup` and `--next` list open trackers;
  - nothing in `shoalmark.py` reads an open line on done work.
  
  Before this branch, R3 lived only in CHANGELOG 0.18.4. Now it is also a *What is true now* line and a ship-log row
  of a Shipped tracker. Both are records; neither is a queue.
- *The gap:* the pre-commit hook's `/dev/null` still hides a skipped block's name and *this is NOT a full pass* at
  commit time. The only home that would bring it back is a Shipped tracker.
- *What closes it:* a line in the closest open tracker that a pass reads, as path line 2 asks under the freeze. That
  is FM-028 (the pre-commit suite and the clock; FM-035's own `considered:` names it) or a bug filing, which the freeze
  admits. FM-035's line then points to it.

**R5 · P3 · confidence 95% · The *Passes* paragraph.**
- *The gap:*
  - the section's header asks each paragraph for *its worksheet*. This one ends *the worksheet is the record*, and
    unlike its neighbours it does not name `evidence/triage/triage-2026-09-26.md`;
  - two blank lines precede it where one is the file's rule;
  - *FM-029 one Done-when line unmet* names a ship-log line (check 6);
  - *FM-030 three* does not say which three.
- *What closes it:* the file named, and one blank line. The gaps are named in the paragraph or on the trackers the
  next time either is touched.

## Verdict — READY WITH FINDINGS (R1–R5, all P3), 85%

**READY WITH FINDINGS.**
- The pass is what the command makes: the tip replays byte for byte from `c3bae92` and the sheet, and `--triage`
  applies nothing.
- FM-002's P2, #4 and `owner` are the rules' reading. Its ask is AU-24's re-made draft, whole, and on his list.
- The raise quotes his three words at their true times and reads none of them as an answer.
- The three flips meet their *Done when* against the tag's own record, and no Shipped tracker keeps a rank.
- FM-006 gains its line, with its front matter and its ask untouched.
- TRIAGE.md changes only under *Passes*.
- Every gate is green.
- Nothing here needs a re-make before the merge. R1 and R3 are due before FM-002's build pass. R2 is due at whichever
  of this branch and PR 82 merges second.

*The Owner lands this by merging, and a merge rules nothing (path 5).*
