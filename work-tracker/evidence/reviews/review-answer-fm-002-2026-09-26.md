# Review — the Owner's answer to FM-002, at 4e00f85 (2026-09-26 14:16 CEST)

- **Date:** 2026-09-26
- **Seat:** Reviewer (Opus)
- **Session:** `8e509911/reviewer-29`
- **Worktree:** `shoalmark-review-4`
- **Tier:** docs, one pass. This follows the Owner's FM-032 answer: an answer pull request takes one Reviewer docs
  pass on its head before the merge. A review of the Owner's own answer reports and never blocks (TRIAGE.md, path 3).
- **Independence:** same session. I am a sub-agent of Principal session `8e509911`, and that session set this ask
  (`4527ca1`, merged as PR 89 at `86b78e3`). The answer is the Owner's.

**Reviewed:** `answer/fm-002` (PR 90), `4e00f85d4b8fdc20e9faab34288af80dbcc5884b`. It is one commit on `origin/main`
`86b78e355cb7c30e775545c124428afa5e68dd8b`, and `origin/main` has nothing that is not on the branch.

## The checks

| # | Check | Result |
|---|-------|--------|
| 1 | Author and signature | **True, 99%.** Author and committer are `holgo99 <holgoijo@gmail.com>`, 2026-09-26 13:54:50 +0200, one parent, `86b78e3`. `git log -1 --format='%G? %GS %an %ae'` gives `G holgoijo@gmail.com holgo99 holgoijo@gmail.com`. The key is `SHA256:uNcUULP20UyJ7Iyv3xImxOrg9cXTcRqIxbWsekBYzCQ`. That is the one ed25519 key in `work-tracker/allowed_signers` (`shoalmark.toml` `[seats]`: `owner = "holgoijo@gmail.com signed"`), and `ssh-keygen -lf` on that file gives the same fingerprint. `git verify-commit` against this worktree's committed copy: *Good "git" signature for holgoijo@gmail.com*. The branch does not touch the signers file. |
| 2 | The diff: FM-002's front matter as `--answer` writes it | **True, 97%.** 2 files, 5 lines added, 2 removed. **FM-002's tracker:** `next: owner` becomes `next: build`, which `ANSWER_MOVE` writes for `ask-kind: ruling`. `answer:`, `answered: 2026-09-26` and `answered-by: holgo99` are inserted under the last `ask-*` line (`ask-proposal:`), in the order `answer_cmd()`'s `write()` uses. No body line changes and no other key changes. **`work-tracker/INDEX.md`:** FM-002's row only. Next `owner` becomes `build`, Kind *complicated* becomes `—`, and Needs `intended` becomes `intended, kind`. This is the pre-commit hook `tracker-index` (`--print-written`, `git add`), which staged the regenerated index. The file is generated, not hand-edited: see check 5. Earlier answer commits (FM-007, FM-032) were one file because their `next:` stayed `owner`. From 0.18.4 the answer writes the next move, and the index shows it. The 3% is for the brief's "nothing else": read literally it does not hold. Read as "nothing the tool's flow does not write", it does. |
| 3 | The answer text against the ask's option 2 | **True, 99%.** The text after `accepted - ` equals option 2 of `ask-options:` byte for byte, 108 bytes each: *the tool ships monochrome and shoalmark as starters; shoalmark's own board and site wear the shoalmark theme*. It is not the proposal (`ask-proposal:` equals option 1), so the relation is *chose option 2*. |
| 4 | `--answered` on the branch | **True, 99%.** FM-002's entry is `FM-002 · answered 2026-09-26 by holgo99`, and its relation line is quoted exactly: `relation: chose option 2: the tool ships monochrome and shoalmark…`. |
| 5 | The board: tracker view and INDEX.md | **True, 95%.** `--html-only` builds the git-ignored board. FM-002's row carries the relation `["option", 2, "the tool ships monochrome and shoalmark…"]`. `view()` renders that through `relation.option` = *chose option {0}* beside the answer, so the view says what `--answered` says. The 5% is because this was read from the page's data and script, not from a browser render. `python3 shoalmark.py` rewrote INDEX.md and `git status --short` stayed empty, so the commit did not leave INDEX.md stale. `--check` agrees: *work-tracker/INDEX.md is up to date — 37 trackers*. |
| 6 | `--check` and `--session-check` | **True, 99%.** `--check` exits 0: *judged before build: on*; *the Owner's two sections: guarded — none changes them or his signers file*; *filing freeze: 19 open*. `--session-check` exits 0 and prints nothing. Positive control: `--check` exits 0 with the signers file set to this worktree's committed copy. Set to a missing file, it exits 4 and names FM-002 `4e00f85d4b` among the signed commits it cannot check, so the gate reads this signature. |
| 7 | Both suites, run by hand | **True, 99%.** Python 3.14.3: `test_shoalmark.py` is *all green*, *skipped here: 0 checks — every check ran*, 10 min 53 s. `test_core.py` is *all green*, 148 `ok`. Python 3.9.6 (`/usr/bin/python3`): `test_core.py` is *all green*. Not run: `test_shoalmark.py` under 3.9.6. The commit touches no `.py` file, so the hook's `tests` command did not run on it either. |
| 8 | merge-tree against `origin/main` | **True, 99%.** `git merge-tree --write-tree origin/main 4e00f85` gives `3c3d6a2`, which is the branch's own tree. It is a clean fast-forward. |

## Findings

**R1 — P3, forward; not a defect in the answer, and it does not block. Confidence 90%.** The commit subject, and PR 90's
title taken from it, read `FM-002: accepted - the tool ships monochrome and shoalmark as starte`. The tool writes
the subject as `<id>: answer[:60]`, so the subject is cut in the middle of a word. The signed `answer:` line is whole.
Both behaviours are already filed, so this needs no new tracker:

- The cut is FM-030's 0.18.4 line, *named for 0.18.4 and not in it* in the CHANGELOG.
- The word `accepted` for option 2 is one of the things FM-029's ruled option leaves as it is. The Owner's ruling of
  2026-09-24 was *the relation only, no new verbs*.

What this answer adds is a reader that FM-029's *Leaves:* line does not name. That line names the raw file and
`git log`. The pull request title is a third reader, and it is the line the Owner merges on. It says `accepted` for a
choice that every computed reading calls *chose option 2*. The 10% is for whether FM-029's owner already counts the
title as part of `git log`.

## For the record only (not judged)

This answer chose option 2, so it rules FM-002's slice B in addition to slice A. Slice A is the brand layer: the
shoalmark theme on shoalmark's own board and site. Slice B is code tier: the tool ships `monochrome` and `shoalmark`
as starters, with `brand/themes/` and `--brand DIR --from <theme>`. FM-002's *Done when* holds both slices to a pass's
judgement before their first build commit (FM-033).

**Not verifiable here:** who holds the key. A signature proves the key, not the hand (FM-007).

## Verdict — READY WITH FINDINGS, 92%

The commit is the Owner's and signed with the key his signers file trusts. The diff holds only what `--answer` and
the pre-commit hook write. The text is option 2 byte for byte, and both the tool and the board say *chose option 2*.
The gates and the suites are green, and the merge is clean. R1 is P3 and forward.

*The Owner lands this by merging, and a merge rules nothing (path 5).*
