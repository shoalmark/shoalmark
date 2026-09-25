# Review — FM-006's ask, when and how shoalmark goes public, at 4899353 (2026-09-25 16:39 CEST, Reviewer, session `8e509911/reviewer-6`)

- **Branch:** `fm/006-when-shoalmark-goes-public`, tip `4899353` (`48993534af7f4681f477d83697bc853069672d5a`), one commit
  on `origin/main` `8b267b4` (PR 76's merge), by the principal seat (`Session: 8e509911`), 16:29:05.
- **Tier: docs, one pass.** Two paths: FM-006 and INDEX. A defect in an ask's text is P2, because an ask cannot be
  fixed after he answers.
- **Independence:** a sub-agent of the branch's own session (`8e509911`); `--check` counts it *same session*. Reported.

## What I ran

- **The paste:** the user record at `2026-09-25T14:26:24.954Z` (16:26:24 CEST), read alone. Its fenced ```` ```Auditor ````
  block (480 bytes) equals the body's italic quote byte for byte ✓.
- **The earlier ask:** the user record at `14:22:12.928Z` (16:22:12), read alone. Its options carry five gates: a license
  chosen, CI green, the signing tier or the key, gitleaks clean, the client names ruled on. The section's *five gates, a
  license among them* is right ✓. `git log --all -S'go public'` finds only `4899353`, so the earlier ask never reached
  the board ✓.
- **The ask** against `ask_problems` and `--schema`:
  - one question, one `?`, at the end, 38 characters ✓;
  - three options of 111, 112 and 7 characters, each at most 120, all distinct ✓;
  - `ask-proposal:` is option 1, verbatim ✓. Options 2 and 3 are the Auditor's, verbatim. Option 1 is the Auditor's
    181-character first option, compressed to fit, and the body says so ✓;
  - `ask-since: 2026-09-25` and `next: owner` ✓;
  - `--owner` lists *FM-006 · ruling* with the question. The kind: R1.
- **"not yet"** passes the rule that no option opens with *yes* or *no*. It opens with *not*. To a *when* question it
  is a when, not a reply: picked, it is signed `accepted - not yet`, which reads as what he chose, and 0.18.1's relation
  names the option. It is the Auditor's wording. Confidence 75%.
- **The gates** against the counsel: the same three in substance ✓, but not word for word (R2).
- **Facts in the body:**
  - FM-007's answer reads *accepted - after the scoring, once the key is delivered.* ✓
  - FM-035's fix branch `fm/035-ci-green-on-every-platform` came back NOT READY at 14:23:59, and fixes followed at
    14:50:06, so *in review* ✓.
  - The parent project's ledger commit `17daad27` is 16:27:17, before `4899353` (16:29:05), so it came first ✓.
- **Gates:**
  - `--check` 0 (*20 open*), `--session-check` 0, the generator leaves no diff.
  - `merge-tree` against `origin/main` is clean (the tip's own tree). `origin/fm/030-the-acts-owed-to-him-on-his-board`
    does not exist (`git ls-remote`).
  - `test_shoalmark.py` 0 (394 ok), `test_core.py` 0 (148 ok).

## Findings

**R1 · P2 · confidence 70% · The ask is `ruling`, but a yes needs the Owner's hands.**
- `--schema`: *An ask whose yes needs the Owner's hands is `action`, whatever else it decides.* This is AU-22's rule.
- A yes to option 1 is a visibility switch on the forge. A yes to option 2 is a new public repository. Either happens on
  his account, at a tag after 09-29. Only *not yet* needs nothing of him.
- As a ruling, 0.18.3's `--answer` writes `next: build`, and the ask leaves `--owner` and `--standup`. The act would
  then sit on no list of his: FM-030's defect, and path line 6, *nothing owed to them lives only in … a tracker body*.
  FM-030's fix keeps accepted **action** asks on his lists, so the kind is what would keep this one there.
- The Auditor's paste says *(ruling)*. The schema's rule is the Auditor's own.
- The same class as FM-032's ask, graded P2 by the evening pass of 09-24 (its R3).
- **Fix:** `ask-kind: action`, with the ledger row to match. `--owner` then lists it as action.

**R2 · P3 · confidence high · The gates are called *word for word from the counsel*, and each adds words.**
- The counsel: *CI green on all three platforms, the signing tier stated or the hardware key live, and a gitleaks scan
  clean*.
- The body: *… on the tag that goes public*, *stated on the site*, *a `gitleaks` scan of the whole history*.
- The additions make explicit what the counsel implies, so the substance holds. But the label is false. The parent's
  ledger row gives the counsel's words and says the body has them word for word, so the two records differ.
- Option 1 points at these lines (*the three gates named in the body held*), so they are what he answers.
- **Fix:** in the same re-make, before his answer, either quote the counsel's clauses as the gates or mark the additions
  as the seat's.

**R3 · P3 · confidence medium · The proposal's condition is not on the board.**
- The body discloses it: *the first, if the client names may be public; if not, the second*.
- The dialog shows the ask, the proposal and the tracker's title (`t[6]`), so neither the condition nor the gates reach
  it.
- Option 1's *as it is*, set against option 2's *the client names removed*, is the only trace.
- **Fix:** in the same re-make, carry the condition in option 1's own words within 120 characters, for example *this
  repository as it is, client names and all, at the first tag after the 09-29 scoring, the three gates held* (110).

## Verdict

**NOT READY — R1 is P2.** R2 and R3 are P3. Take them into the same re-make: the ask cannot change after he answers.

What holds:
- The paste, quoted byte for byte.
- The earlier ask, rightly described and never on the board.
- One question, the proposal verbatim, the options distinct and within 120 characters.
- *not yet* passes.
- The facts in the body, and the ledger first.
- The gates are green.

The Owner lands this by merging; a merge rules nothing (path 5).

## Pass on 1dea28b (2026-09-25 16:58 CEST, Reviewer, session `8e509911/reviewer-6`)

**Scope.** `1dea28b` (`1dea28b7adcf31e81aa39d40d5222d240e90f012`): one commit by the principal seat (16:50:04) on the
verdict above (`92c65a0`). It changes FM-006 alone. **Tier: docs, one pass.** **Independence:** same session, reported.

**What I ran.**
- **The ask:** `ask-kind: action`. Three options of 115, 112 and 7 characters, all distinct. The proposal is option 1,
  verbatim. `--owner` lists *FM-006 · action*.
- **The body:**
  - The quote of the 14:26:24Z paste is still byte-identical.
  - Each gate is now the counsel's own clause in italics, found verbatim in the paste, with the seat's gloss in
    brackets: *CI green on all three platforms*, *the signing tier stated or the hardware key live*, *a gitleaks scan
    clean*.
  - The ship log gains one row, and no row is edited.
- **The parent ledger**, read-only (`git ls-remote`, then `git show` in `worktrees/reviewer-2`): branch
  `feat/190-day-four-the-thirteenth-hour-row-47-re-made-and-row-46-answered` is at `671e1259`, 16:50:39. Its appended
  clause carries option 1 exactly as the board has it. Options 2 and 3 stand unchanged in the row's merged cells. So the
  board and the ledger carry the same option text ✓.
- **Gates:**
  - `--check` 0, `--session-check` 0, the generator leaves no diff.
  - `merge-tree` against `origin/main` (`8b267b4`) is clean. No `fm/030*` head exists on origin.
  - `test_shoalmark.py` 0 (394 ok), `test_core.py` 0 (148 ok).

**The findings of the first pass.**
- **R1 ✓ closed.** The kind is `action`, and the body says why: *a yes switches the repository's visibility or creates
  a new one on his account*.
- **R2 ✓ closed.** The gates are in the counsel's words, and the gloss stands apart.
- **R3 ✓ closed.** The condition now stands in the option he reads before he signs.

**R4 · P3 · confidence 60% · Option 1 says *if*; his pick decides it.**
- Signed, option 1 reads `accepted - this repository as it is, if its client names may be public — …`.
- The *if* is decided by his choice between option 1 and option 2 (*the client names removed*). A seat reads a pick of
  option 1 as his judgement that the names may be public, which is sound.
- But the line itself keeps a condition. A declarative *client names and all* would leave none.
- The option also drops *09-29* and *named in the body*. *the scoring* is his own phrase, from FM-007's answer, and the
  gates are named in the body's heading.
- **Not blocking.** Change it only if the ask is touched again before the board.

Noted, not graded (the parent's record): the clause says *re-made with the board at 16:49*. The board's commit is
16:50:04 and the clause's own is 16:50:39, so the ledger followed the board by 35 seconds.

**Verdict on 1dea28b: READY WITH FINDINGS (R4 P3).** R1–R3 are closed. The ask meets every form rule, and its kind now
keeps the act on his board.

The Owner lands this by merging; a merge rules nothing (path 5).

## Verified again on 7557ed1

**Scope.** `7557ed1` (`7557ed1bfd2a10ba15201e960371aa89a613a7f5`), read 2026-09-25 18:58 CEST by the Reviewer, session
`8e509911/reviewer-10`. It holds eight commits by the Implementer seat (`8e509911/implementer-24`, 17:45–18:23) on the
verdict above (`9555d2c`): seven on FM-006 and one on FM-030. On top is one merge of `origin/main` (`b336a53`, PR 78).
**Tier: docs, one pass.** A defect in the ask's text is P2, and so is a wrong count written as verified. The rest is P3.
**Independence:** same session. This pass is 8e509911's own sub-agent. Reported.

**What I ran.**
- **The two filed pastes.** Each runs from after its opening line (`**Through the Owner at 17:23:39 …**` or
  `**… 17:37:17 …**`) to the next blank line, and includes its own heading line.
  - The addendum as filed: sha256 `281f74bbe32c32f73ef993846f95f147b7f4be492ed251b97a081c3ea7932309`, 1382 bytes.
  - The correction as filed: sha256 `a0b8244dbb6b1382d910df2dba91848db8cc8f53d34152d29b4a6d0d2f78ff01`, 1084 bytes.
  - `cmp` finds both byte-identical to the paste files the brief names, and both hashes equal the brief's ✓. Each opening
    line occurs once.
- **The ask.**
  - `ask:` is unchanged since `9555d2c`: one `?`, at the end. `ask-kind: action`, `ask-since: 2026-09-25` and
    `next: owner` are unchanged too.
  - `ask-options:` is the addendum's three options, byte for byte against item 3's quotes. They are 119, 118 and 7
    characters, all distinct, and open with *this*, *a* and *not*. `ask-proposal:` is option 1, byte for byte ✓.
  - No option carries an *if*. The condition *if either may not be public, the second* stands in the body's proposal
    paragraph and in the ship-log row, each time as the Auditor seat's counsel ✓.
- **The fourth gate.** Item 4 of the gates list is the addendum's clause in italics, *the port evidence deleted or moved,
  as ruled on 09-22*, with its gloss in brackets ✓.
  - His answer is quoted as *should consider this now* [normalised]. The pasted *Should consider this then now* appears
    only inside the filed addendum ✓.
  - *row 36* appears only inside the filed paste ✓.
- **The citation, against the brief.** The Principal's message said *row 3*. `83dc05d` changed it to *row 10* and gave
  its reason. I checked read-only, with `git show` of the ledger at its registry path on the parent's `main`:
  - the ledger numbers its rows in one count across its tables;
  - line 36 is the 2026-09-22 ruling. It is row 10 in that count, and row 3 within its own table;
  - the go-public ask is line 73, row 47 in the same count.
  - So *row 10* is the number that belongs beside this file's *row 47*, and the line number holds either way ✓.
- **What is true now** names the act ✓: the six files under `work-tracker/evidence/FM-001/port/` are still on main,
  deleting or moving them is this tracker's act, and nothing is deleted before his answer. `git ls-tree` lists the six at
  `7557ed1` and at `origin/main` (`b336a53`) ✓.
- **The count, reproduced at `9555d2c`.** Not at the tip: this file's own newer versions add to the count there.
  - Method: I listed every object of `git rev-list --all --objects` (91 refs and the 15 worktrees' HEADs) and typed them
    with `git cat-file --batch-check`. I read each blob with `git cat-file --batch` and searched it for the parent's name
    in any case. I ran it again with the forge's 78 pull heads from `git ls-remote` added by id. All were present
    locally, none was fetched as a ref, and they added no hit.
  - Today 35 blobs name the parent across all refs. 28 are reachable from `9555d2c`. The other 7 are exactly the seven
    FM-006 versions from the branch's eight commits; `1429785` left FM-006 unchanged.
  - Against `9555d2c`: 28 = 8 at the tip + 20 older. The 20 sit at 7 paths: 5 at the tip, and 2 are FM-002's pre-move
    `docs/work-tracker/` paths. 3 files (FM-020, FM-022, review-fix-0.17.5) name it only in older versions.
  - Against `8b267b4`: 8 at its tip, 18 older, and the branch's 2 FM-006 versions. 3 of the 6 port files do not carry the
    name.
  - Every number the file writes ✓.
  - The Implementer's scope (77 pull heads, no merge ref for PR 77) was the forge's state before PR 78 opened at 18:00:02
    and before this merge. At this pass there are 78 pull heads and a merge ref, and the count at `9555d2c` is the same.
- **The control, and the tip count.** At `9555d2c`, `git grep -i -l` for the name lists 8 files, and they are the paths of
  the 8 tip blobs found ✓. At `origin/main` (`b336a53`) it lists 8 files, and at `7557ed1` the same 8 paths. The struck
  *7 of their paths only in history* appears only inside the filed pastes, at FM-006's lines 113 and 120 ✓.
- **FM-030:** one line, `**For 0.18.4:**`, under its second widening. Nothing else in the file changed ✓.
- **No parent state beyond the registry path and row and line numbers** ✓.
  - The diff `9555d2c..d60c8bc` names no local path and no person, and quotes no tracker body.
  - Its only parent id outside the registry path is inside the filed addendum.
  - `scripts/gen-tracker-index.py` is named to say what the port files hold. It already appears in four files at
    `9555d2c`: the port files and FM-001's notes.
- **The ship-log row** is at the top, dated 2026-09-25, and no row below it changed ✓. It carries both hashes, the fourth
  gate with its citation, the act, the count as found, 119/118/7, the condition as counsel, FM-030's line, and row 47 as
  owed.
- **The merge `7557ed1`.**
  - Its parents are `d60c8bc` (the branch, with `9555d2c` as an ancestor) and `b336a53` (PR 78's merge). The base is
    `8b267b4`.
  - Redone in memory with `git merge-tree`, it conflicts in `work-tracker/INDEX.md` only.
  - The four paths the branch changed are byte-identical to `d60c8bc`'s. The six paths main changed are byte-identical
    to `b336a53`'s. The merge touches no other path.
  - `python3 shoalmark.py` rewrites `INDEX.md` byte-identically (sha256 `21e38595…`), with FM-006's row from the branch
    and FM-035's from main ✓.
  - The merge's message said *to be verified*. This pass is that verification.
- **Gates.**
  - `--check` 0: *INDEX.md is up to date — 36 trackers*, the freeze at 20 open, no ask problem.
  - `--session-check` 0.
  - `test_shoalmark.py` 0 (399 ok) and `test_core.py` 0 (148 ok), on 3.14.3 and on 3.9.6.
  - `git diff --name-only origin/main...HEAD` lists FM-006, FM-030, INDEX.md and this file. All are under
    `work-tracker/`: PR 77's three files plus FM-030 ✓.
  - `git merge-tree` against `origin/main` is clean, and its tree is the tip's own ✓.

**R4 ✓ closed.** The options are declarative, and the condition is no longer in their text.

**R5 · P3 · confidence 60% (the numbers are exact; whether to write them is the question) · The struck clause holds on
another reading, and that number is not written.**
- Across the history, the 28 versions sit at 18 distinct paths. 7 of those paths are absent from the tip, all under the
  pre-move `docs/work-tracker/` tree:
  - FM-001's three port files that carry the name, with `shoalmark.toml` also under its earlier name `fathom-mark.toml`;
  - FM-001's seam note;
  - FM-002's two files.
- So *7 of their paths only in history* is true when read by path. The correction reads it by version: the older
  versions sit at 7 paths, 5 of them still at the tip. On that reading the clause is wrong. Both readings give 7.
- The Implementer's brief asked for the path reading: *the distinct paths of those blobs, and which of them are absent
  from `origin/main`'s tree*.
- Nothing false is written. The file gives the correction's numbers, each reproduced, and keeps the struck clause
  inside the paste. But it records the Auditor seat's own clause as wrong and never says that, read by path, it is 7 of
  18.
- The substance does not change. *As it is* publishes the parent's traces either way, and the 7 old paths are more of
  them.
- **Fix forward, or leave:**
  - either one clause beside the count, as the seat's own number and without re-asserting the struck clause: *the 28
    versions sit at 18 paths, 7 of them only in history, all pre-move*;
  - or the Auditor seat's reading, through the Owner.
  - The filed paste stays as it is.

**Verdict on 7557ed1: READY WITH FINDINGS (R5 P3).**
- The filed pastes equal the pastes.
- The ask meets every rule and matches the addendum.
- Every number written was reproduced at `9555d2c`.
- The merge of main carries only the two sides' own work and a regenerated index.
- Tier: docs, one pass. Independence: same session, 8e509911's own sub-agent. Reported.

The Owner lands this by merging; a merge rules nothing.
