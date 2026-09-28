# Re-check — FM-018, FM-030, FM-040: the fixes of RV-755…759, at 2ec5e1b (2026-09-28 13:38 CEST, Reviewer, session `8e509911/reviewer-48`)

Reviewed: 2ec5e1b37abbb12e0435f5a092ab1a6c7f9d2abd
Session: 8e509911/reviewer-48

- **Scope.** `2ec5e1b` (the Principal, 13:29:37) is one tracker-only commit on my verdict `992fb5d`. My fetch at 13:31:53
  showed the branch at that sha. The Principal committed it from this worktree, so HEAD was already there, and the tree
  was clean.
  - `git diff 992fb5d 2ec5e1b` changes 3 files, +12/−9: FM-018, FM-030 and FM-040. The spawn message said two files,
    +9/−4.
  - My first review file is untouched. No `.py`, `vendor/` or `docs/` file changed, so no suite was run.
- **Tier: docs — a scoped re-check** of the five findings and the ask's form, with the same gates.
- **Independence:** same session. I am a sub-agent of 8e509911.
- **Verdict: READY, for this commit on main as I fetched it (`9e9fcb33`).** RV-755 to RV-759 are closed, nothing new, no id minted. **Not mergeable as it stands:** main moved to `fa9e9ac` at 13:35:21 (PR 113), and FM-030's ship-log tail now conflicts. The merge of main is owed. It will be a new head, and it needs a scoped re-check before any merge.

## Gates

| run | result |
|---|---|
| `--check` in the worktree (13:33:26–13:34:05, load 4.69) | Exit 0. *INDEX.md is up to date — 41 trackers*; *filing freeze: 22 open, at or above 8 — only bug filings*; judged before build and the Owner's two sections are both guarded (3 commits) |
| `--session-check` (13:35:05, load 5.64; the runner waited at 7.75) | Exit 0, no output. The worktree was clean afterwards |
| `--triage` on the scratch copy at `2ec5e1b` (13:35:05–13:35:32) | No row is marked RAISED, and FM-018 and FM-030 are not on the worksheet. The one tracker to judge is FM-041's NEW FILING row. Exit 4 again, because the copy cannot verify signatures. It again applied the worksheet's FM-027 row (*keep P3 owner*), which is outside this diff and was reported in my first pass |
| `git merge-tree --write-tree origin/main HEAD` in the worktree, against `9e9fcb33` as fetched at 13:31:53 | Clean, a fast-forward (tree `22a7695`). `git diff --check` is clean. No `.py`, `vendor/` or `docs/` path |
| `--queue` on the scratch copy (13:35:32; it fetches origin) | *branch fm/018-his-two-dashboard-requir… @ 2ec5e1b  wait: no pull request — **conflict in work-tracker/FM-030-…md***. Main moved at **13:35:21**: `fa9e9ac`, *Merge pull request #113 from holgo99/fm/030-the-board-reads-his-unmerged-acts* |
| `git merge-tree` against `fa9e9ac` (the copy) | One conflict: the last rows of FM-030's ship log. Main appended two 2026-09-28 rows (the board built on `fm/030-the-board-reads-his-unmerged-acts`; the pass on `ada15c6`), and this branch appended two (the 12:43:02 raise; RV-758). Every other hunk merges automatically. The resolution keeps all four rows, main's two first, because the table runs oldest to newest |

## The closures

**RV-755 (P2) — closed (confidence 80 %).**
- **The ask** (248 characters) names the freeze's two routes as his rule. It reads *files only defects and sends the rest
  into an open tracker's body, or to wait*, which is the `--new` refusal's own wording (:6229–6231), and it asks *Which
  route for these two?*
- **The options** (94, 99 and 86 characters; three, split by ` | `; none opens with yes or no):
  - *lift for one pass: `freeze_at` 24, then back to 8 — any seat's feature filing passes meanwhile* now states both
    its reach (any seat) and its end (back to 8).
  - *fold, the freeze's own route: …* and *hold, the freeze's other route: …* are marked as his rule as written.
  - *hold* no longer claims a record on FM-030.
- **The proposal** equals option 1 byte for byte, and `next: owner` stands, so his answer is still required.
- **The raise line** carries the full reach that the 120-character lint keeps out of the fields:
  - 24 by his word, and back to 8 on the pass's branch that files the two;
  - while it stands at 24, any seat's feature filing passes;
  - fold and hold change no count.
- The option now says what it does to his rule and to who can file, so no default is hidden.

**RV-756 — closed.** The 12:50:35 line now reads `changed_paths` (:2018) and `dirty_refusal` (:2031) at `9e9fcb33`. I checked
both numbers with `git show 9e9fcb33:shoalmark.py | grep -n`.

**RV-757 — closed.** FM-040's reading and its ship-log row now agree with the body:
- point 2 is counsel (b);
- point 3 is a candidate beside (a), decided at the build's design;
- point 1 is measured first;
- *Done when* is unchanged, and the text says so.

**RV-758 — closed.**
- FM-018 now reads *the paste's closing line — the Auditor's, not the Owner's*, and FM-030 reads *the Auditor's closing
  line*. The paste is the Auditor's message (its *To:* line), so that reading is the paste's own frame.
- FM-040 marks his words, *`waiting: tracker-dashboard` is painful*, as the Auditor quotes them. That span is in the paste
  byte for byte.

**RV-759 — closed.** The raise line and the ship-log row both say that after his answer the seat runs `--clear-ask FM-018 wait`,
and that FM-018's own design stays unruled.
- `--clear-ask <id> <move>` takes `wait` from `MOVES` (:285). It sets `next:` to the move and moves the exchange under
  `## Asks`.
- So `next: build`, which `--answer` writes for a ruling, does not stand.

**The quotes, again.** Each span is checked again with `grep -F` against the saved pastes, and all 12 still match. The fix
commit changed no quoted span.

**Notes, no id.**
- FM-018's *Asked* ship-log row now opens *the proposal* ***lift for one pass***, but further on it still says *lift for them,
  fold here, or hold*. The heading is right and the reach is in the ask. This is a wording tidy, confidence 50 %.
- The ask no longer says *22 open*, so why the number is 24 is only in the raise line. With the lint's 120-character limit on
  options, that is a fair split.

**A disclosure of my own.** At about 13:36:50, a no-op `python3 -c 1` went into one of my draft-editing commands by mistake. I did not check the load first; it was 4.87 at 13:36:58. Every gate above ran at a load under 6.

## Verdict

**READY** on `2ec5e1b`'s content. All five findings are closed, and the gates pass against `9e9fcb33`.

The branch does not merge clean onto today's main, `fa9e9ac` (13:35:21, PR 113): the conflict is FM-030's last ship-log rows. The Principal merges main, keeping all four rows with main's first. The gate treats that merge commit as a new head, and it gets a scoped re-check. Until then nothing here is the Owner's to merge.

path 5 — a merge rules nothing.
