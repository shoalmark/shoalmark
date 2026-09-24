# Review — FM-033 filed, at 7c04534 (2026-09-24 16:01 CEST, Reviewer, session `8e509911/reviewer-1`)

**Scope.** `origin/main` `095f1d3`…`7c04534` (`7c04534f619d4b8e38d485bd338bf153c0b26376`), two commits by the
principal seat under `8e509911`:
- `35c7664` (15:31:27) files the tracker and regenerates INDEX.
- `7c04534` (15:49:58) changes only the tracker: the ask, its options, its proposal, and the filing sentence.

The pass began at `35c7664`. The branch moved before any verdict, so this verdict is on `7c04534`, and nothing was
committed on `35c7664`. Tier: docs, one pass. There is one exception: a defect in `ask:` or `ask-options:` that would
make the Owner's signed answer ambiguous or wrong is P2.

**What I ran.**
- `shasum -a 256` on the Auditor's draft.
- `diff` of the filed file against the draft with `FM-0NN` replaced by `FM-033`.
- `git log`, `git show`, `git merge-base --is-ancestor` and `git grep` across every `origin/*` ref.
- `--schema`, `--related FM-033`, `--owner`, `--check`, `--session-check`, and `python3 shoalmark.py` twice.
- `test_shoalmark.py` and `test_core.py` on Python 3.14.3. Python 3.9 is not on this machine.
- `gh pr view 51`, read-only.
- The parent project's ledger, read with the one `fetch` and `show` the brief allows. Its two commits' times come from
  the forge.

## Checked, and true

**Word for word.**
- ✓ The draft's hash begins `19d16c62c22ea3b8`. It has 74 lines, and the filed file has 79 (74 plus the 5 ask keys).
- ✓ The `diff` has two hunks.
  - Front matter: `next: review` becomes `next: owner`, and `ask`, `ask-kind`, `ask-since`, `ask-options` and
    `ask-proposal` are added.
  - `:19`: *Filed 2026-09-24 by the Auditor seat (session src-d6)* becomes *Written 2026-09-24 by the Auditor seat
    (session 8b91dba2), filed word for word by the Principal*. This is the one body edit the brief allows.
- ✓ Nothing else is added, changed, softened or dropped. The file ends with the draft's final byte.
- ✓ At `35c7664` the only differences were the keys and `next:`, as that commit message says.
- Note, not a finding: the edited `:19` is 165 characters long and is not wrapped. The draft's own lines run to 131.

**The ask at `7c04534`.**
- ✓ `ask: "Does a signed answer that says *now* count as the judgement?"` is the draft's own question under *For the
  Owner to rule*, word for word. It is 60 characters, one question, with one `?` at its end.
- ✓ There are three options: 117, 69 and 62 characters. None starts with *yes* or *no*.
- ✓ The draft's two consequences are carried.
  - *If yes, `--answer` writes the judgement fields* is option 2.
  - *If no, a pass runs before the first build commit* is option 1.
  - Option 3 is a *no* that adds a preview, and the gate in *Done when* still refuses the build until a pass writes
    `triaged:`.
  - The three options are distinct.
- ✓ `ask-proposal` is option 1 word for word. `ask-kind: ruling`, `ask-since: 2026-09-24` and `next: owner`.
- ✓ The ledger row's question equals `ask:` word for word. Its bold proposal equals option 1, and its two other
  options equal options 2 and 3, joined by ` · ` instead of ` | `.
- ✓ The row came first both times. On the forge, the ledger commit named in `35c7664`'s message is 15:29:43 CEST,
  before 15:31:27. The one named in `7c04534`'s message is 15:48:28, before 15:49:58.
- At `35c7664` the ask would have been P2, and none of it survives at `7c04534`:
  - Option 3 was *yes for now only*. That is either option 2 again, since the question is already about a *now*, or
    *yes* with no end date.
  - Two options began with *yes* or *no*, so they would have been signed as `accepted - no — …`.

**The filing.**
- ✓ `tags: bug`. `--check` prints *filing freeze: 17 open, at or above 8 — only bug filings* and exits 0.
- ✓ `considered:` names five trackers, and all five exist (FM-005, FM-024, FM-030, FM-031, FM-032). R4 is about the
  ones it leaves out.
- ✓ The id is the next free one. No `origin/*` ref carries FM-033 … FM-039 other than this branch.
- ✓ `slug_of(title)` gives `work-is-built-on-trackers-no-pass-has-judged-and-the-board`, the file's name.
- ✓ INDEX is generated. `python3 shoalmark.py` leaves `git status --porcelain` empty. INDEX changes only by FM-033's
  row and the count (32 to 33).
- ✓ `--owner` prints *1 NEED THE OWNER* and FM-033 · ruling with the ask.

**The draft's facts, from git and the forge.**
- ✓ Every sha resolves.
  - `45198d5` is the Owner's, signed (`G`), 09-23 14:29:54.
  - FM-024: `fe4d9eb` 09-23 15:24:23; `5a4ad6e` 16:02:42, the principal seat, unsigned (`N`). It sets
    `status: In Progress` with no `ask:` and no `answer:`, and its subject says *on the Owner's word*. Then `89e0586`
    16:16:39.
  - FM-032: `4af2c9b`, committed 09:35:00; `ffa63b8` 11:07:43 signed, *accepted - all four now*; `3c0754f` 11:31:53;
    `a2956a5` 11:45:51 sets In Progress. The gap is 14 min.
  - FM-031: `d935807` 08:25:33; `d20bc89` 11:08:24 signed, *accepted - all three rules now, S1 then S2*; `90d3d6f`
    12:01:51; `fbc2697` 12:19:29 sets In Progress. The gap is 18 min.
  - `bd7d5ea` 12:15:26 has the subject *RV-479: …*. It touches `shoalmark.py`, the two suites, README and a label file,
    and no tracker.
- ✓ `v0.18.0` is a lightweight tag on `095f1d3` (PR 49, 14:35:25). All four first build commits and both status
  commits are in it.
- ✓ `fbc2697` and `a2956a5` are not in `095f1d3^1`, which is `main` at 14:24:35. There FM-031 reads
  `status: Proposed`, which is the board of 14:32.
- ✓ FM-006's last merge to `main` is PR 33 at 09:05:50.
- ✓ The progress section at `095f1d3` is FM-006, FM-005, FM-004 and FM-001. FM-024, FM-031 and FM-032 are
  *In Progress* but under *triage*.
- ✓ `board()` (`shoalmark.py:627`) puts an unjudged tracker under *triage* and a judged In Progress one under
  *progress*. `desc.progress` is *kept by triage — by rank, then tier*. Neither reads a branch.
- ✓ The TRIAGE.md *never* quote is exact. `AGENTS.md:7` and `:17–18` say what the draft says; `:7` is quoted up to
  *what to work on*.
- ✓ The first pass's *the next pass reads them* is exact. `7d3e632` is 14:49:42. R1 is about what followed it.
- ✓ The proposed gate's construction holds against the four rows.
  - `5a4ad6e` sets In Progress before `89e0586`.
  - `3c0754f` and `90d3d6f` come before their status commits.
  - `bd7d5ea` names no tracker.
  - A gate keyed on the build commit, with the tracker judged and In Progress at the parent, refuses all four first
    build commits.

**Gates at `7c04534`.**
- `--check` 0; `--session-check` 0; `test_shoalmark.py` 0 (285 ok, all green); `test_core.py` 0 (148 ok, all green).
- `origin/main` `095f1d3` is the branch's base, so the merge is a fast-forward.
- Neither commit message carries a pull-request number with the sign.
- No name of the parent project is in the tracker.

**The commit messages' claims.**
- ✓ The hash prefix and *nothing else changed* (at `35c7664`).
- ✓ *The body is otherwise untouched* (at `7c04534`).
- ✓ The ledger row came first, both times.
- Not verifiable here:
  - The Owner's *go for FM-033 filing* at 15:23:00. That was in chat, not in git.
  - *The three options are the Auditor's own words* and *two of its three conditions*. The Auditor's review of PR 51
    is not on the forge, and the pull request has no comments.
  - The Owner's 11:29:05 chat request, and that session `8b91dba2` is the Auditor's. `8b91dba2` has no commit here,
    so `--sessions` does not know it.

**Independence.** Same session `8e509911`. That is reported, not refused, and `--check` will count this verdict as
*same session*.

## Findings

**R1 · P3 · high · The FM-024 row's *Judged* and the second pass are stale against the pass that stands.**
- The draft was written at 14:53. It says FM-024 was judged at *09-24 14:49, marked Shipped in that pass by the seat
  that built it*, and it gives 14:49 for FM-031 and FM-032.
- That pass, `7d3e632`, was graded NOT READY (`b3d9002`, 15:13) and re-made at `87bac4e` (15:19:52). In the re-made
  pass FM-024 is kept In Progress, P2 #8, for its unbuilt slice 2, and *nothing is closed by the seat that built it*.
- The standing judgement is only on `tracker/triage-2026-09-24` (PR 50). At `7c04534` all three still sit under
  *triage* on `main`.
- Both filing commits (15:31 and 15:49) come after the re-make. As history the row is true, but read now it says FM-024
  is Shipped.
- Fix, the Auditor's to make: one clause in the row or under the table, saying that the re-made pass `87bac4e`
  (15:19) kept FM-024 open and that the judgement is not on `main` until PR 50 merges.

**R2 · P3 · high · FM-024's build ran until 18:18, not 18:15.**
- *R1–R6 until 18:15* stops at `3988cb8`.
- `8b5588e` (R7, 18:18) changes `README.md`. By the draft's own gate, a change outside `work-tracker/` is a build
  commit.
- Fix: *R1–R7 until 18:18*.

**R3 · P3 · medium · The quoted 0.18.1 gate has no source in this repository.**
- *The proposed gate for 0.18.1 would refuse "an In Progress tracker without a judgement"*: `git grep` across every
  `origin/*` ref finds that phrase only in FM-033.
- FM-029's *Candidates for 0.18.1*, the one 0.18.1 plan here, has no such gate. A reader starting cold cannot find
  what the section argues against, or learn that it was pulled.
- Fix: say where it was proposed and that it was withdrawn, without naming a consumer.

**R4 · P3 · medium · `considered:` leaves out `--related`'s second and third hits.**
- `--related FM-033` ranks FM-032 (6.3), then FM-021 (6.2), then FM-029 (4.5).
- FM-021, Shipped, is the fix that made *progress* mean *kept by triage*. That is the definition *Why the person saw
  nothing* charges.
- FM-029 carries the 0.18.1 plan that the *status alone* section answers.
- A listed tracker means one that was looked at, so a pass cannot tell whether these two were.
- Fix, the Auditor's: add FM-021 and FM-029 to `considered:`, or leave them out on purpose and say so.

**Verdict:** READY WITH FINDINGS. R1–R4 are P3. The ask at `7c04534` carries no defect.

## Pass on 063e46d (2026-09-24 16:14 CEST, Reviewer, session `8e509911/reviewer-1`)

**Scope.** `063e46d` (`063e46d336139a3db7c2e2449fc97d8dc61e2cea`) is one merge by the principal seat, under
`8e509911`. It merges `origin/main` `3015b66` (PR 50, the second triage pass, 16:02:18) into this verdict's `6e7ca2f`.

**The merge brought only `main`'s files.**
- `git diff 6e7ca2f 063e46d` changes 14 files. All of them are PR 50's: ten trackers' judgement fields, TRIAGE.md, the
  pass's worksheet, its review, and INDEX.
- The FM-033 tracker is unchanged (the diff is empty), and so is this review file.
- `git diff origin/main 063e46d` names three files: the FM-033 tracker, this review, and INDEX. INDEX differs from
  `main`'s only by FM-033's row and the count (32 to 33). Every other file of `main` is byte-identical.

**Gates at `063e46d`.**
- `python3 shoalmark.py` rewrites nothing, and `git status --porcelain` stays empty. `--check` 0, with the freeze at
  17 open, bug filings only. `--session-check` 0.
- `test_shoalmark.py` 0 (285 ok, all green); `test_core.py` 0 (148 ok, all green).
- `--owner` prints *1 NEED THE OWNER*: FM-033 · ruling, with the ask.
- `git merge-tree --write-tree origin/main 063e46d` is clean and writes the tip's own tree, `5af04ec`. `origin/main`
  is an ancestor, so the merge is a fast-forward.
- The commit message carries no pull-request number with the sign.

**R1–R4 stand, P3, to be fixed forward.** What PR 50 changes for R1:
- The re-made pass is now on `main`. FM-024, FM-031 and FM-032 are judged (P2 #8, #10, #9) and sit under *progress*.
- So R1's *not on `main` until PR 50 merges* no longer holds.
- R1's point stands: the FM-024 row still says *marked Shipped in that pass*, and the pass on `main` keeps FM-024 In
  Progress. The fix is now one clause: *re-made at `87bac4e` (15:19), FM-024 kept open*.

**Verdict:** READY WITH FINDINGS. The merge of `main` is confirmed. R1–R4 are P3.

## The fix-forward at 645e4d4 (2026-09-24 16:39 CEST, Reviewer, session `8e509911/reviewer-1`)

**Scope.** `645e4d4` (`645e4d4a6f03ced9200a8991779243b995138ad9`), on branch `fm/033-the-auditors-fix-forward`, is
one commit by the principal seat, under `8e509911`, on `origin/main` `86f7595`. `main` now carries PR 51's merge
`412ffde`, PR 53, and the Owner's answer `65f37a4` (signed `G`, 16:29:09) through PR 54. The commit changes only the
FM-033 tracker: three lines, the Auditor seat's three replacements.

**The Auditor's check, run as a script.**
- The script replaced each of the three new texts at `645e4d4` with the text it replaced. Each occurs exactly once.
- The expected file is FM-033 at `412ffde` with the Owner's three lines from `65f37a4` (`answer:`, `answered:`,
  `answered-by:`) inserted after `ask-proposal:`.
- `diff expected reversed` is empty (exit 0), and the expected file is byte-identical to FM-033 on `main` `86f7595`.
  So the commit changes nothing but the three replacements. The ask, its options, its proposal and his answer are
  untouched.
- FM-033 at `412ffde` is byte-identical to the file verified at `7c04534`.

**The findings are closed.**
- **R1 · closed.** The row now says what each version of the pass did.
  - `7d3e632` marked FM-024 Shipped.
  - `87bac4e`, re-made on its Reviewer's R1 (*the `fix` closes FM-024 with its slice 2 open*, P2), keeps it In
    Progress, P2 #8.
  - Both carry `Session: 8e509911`, the session whose Implementers built FM-024.
  - Note, not a finding: the cell's *14:49* now times only the first version. The re-made pass is cited by its sha
    (15:19:52).
- **R2 · closed.** *R1–R7 until 18:18, `8b5588e`*: that commit is 18:18:31 and changes `README.md`.
- **R3 · closed.** The sentence now says the gate was *proposed to the Owner in chat …, not in this repository and
  never built*. That the chat happened is not verifiable here. `git grep` still finds the phrase only in FM-033,
  which is what the sentence now says.
- **R4 · closed.** `considered:` now names FM-005, FM-021, FM-024, FM-029, FM-030, FM-031 and FM-032. All seven
  exist.

**His answer.** `--answered` prints FM-033 as *answered 2026-09-24 by holgo99* with the relation *accepted the
proposal*, and it points to `--clear-ask FM-033 <next move>` after the act. `--owner` prints *NOTHING NEEDS THE
OWNER*. The tracker still says `next: owner` until that `--clear-ask`, which is the tool's order, not a defect here.

**Gates at `645e4d4`.**
- `python3 shoalmark.py` rewrites nothing, and `git status --porcelain` stays empty. `--check` 0, with the freeze at
  17 open. `--session-check` 0.
- `test_shoalmark.py` 0 (298 ok, all green); `test_core.py` 0 (148 ok, all green).
- `git merge-tree --write-tree origin/main 645e4d4` is clean and writes the tip's own tree, `3733cba`. `origin/main`
  `86f7595` is an ancestor, so the merge is a fast-forward.
- The commit message carries no pull-request number with the sign.
- `git fetch` was refused in this worktree (publickey). The refs came from the shared object store, where
  `origin/main` is `86f7595` and the branch is `645e4d4`.

**Independence.** Same session `8e509911`, reported, not refused.

**Verdict:** READY. R1–R4 are closed.
