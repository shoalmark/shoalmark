# Review — FM-032, the Owner's merge of main at 2a19789, this round's last step (2026-09-30, Reviewer, session `8e509911/reviewer-59`)

Reviewed: 2a1978938d228b518cb4751a3cfcab8082367da7

- **Branch:** `fm/032-the-ratio-command-and-the-check-outputs-rule`, PR 131, tip `2a19789` = `origin/fm/032-…` (one `git
  fetch origin`, 14:33, no `--prune`; the local branch fast-forwarded to it). `2a19789` is the Owner's merge from the
  forge (14:22:30, `holgo99`, GitHub's web signature — `E` here, where GitHub's key is not held): parents `57ba840` (my
  verdict on `7f451e3`) and `3feaf28` (main after PR 129). `origin/main` is now `2c00aba`.
- **Tier: code** — a merged `.py` makes a new tree; the same ids, none new.
- **Independence: same session** — a sub-agent of Principal session 8e509911 (seat `reviewer-59`).
- **Verdict: READY.** The merge resolves one conflict, in `CHANGELOG.md`, and loses nothing; everything else it brings is
  main's own change, byte for byte; the suites are green on the merged tree. No finding is open.

## What I ran (on `2a19789`)

| run | result |
|---|---|
| `git log -1 --remerge-diff 2a19789` | one file, `CHANGELOG.md`: the Unreleased sections of both sides become one, `## Unreleased — 0.19.0`, main's FM-041 bullet first, then FM-032's two and the five FM-006 bullets; the heading comment no longer names another branch; the bullets lose their blank separators, as the released `## 0.18.6` section has none |
| no line lost | every non-blank line of both parents' Unreleased sections, headings and the comment aside, is in the merged section, and nothing else is (`sort -u` of both parents = the merge's); every released section equals both parents' |
| `git diff 57ba840 2a19789` against main's own change (`git diff 7e7c8ac 3feaf28`, the merge base) | `shoalmark.py`, `test_shoalmark.py`, `test_core.py`: the added and removed lines are identical to main's — FM-041's `board()` change and its checks, nothing else; the other files alike but `CHANGELOG.md` |
| `--check`, 14:35:39 · `--session-check` | exit 0 — *INDEX.md is up to date — 42 trackers*, *judged before build … every build commit under a judged In Progress tracker*, *the Owner's two sections: guarded* · exit 0 |
| `git merge-tree --write-tree origin/main HEAD` | clean against `2c00aba` (`ebd3fa97`): main's commits since `3feaf28` are FM-042's site page, touching none of this branch's files |
| `git diff --numstat origin/main...HEAD` (merge base `3feaf28`), 14:36 | records +595 −33,575, product +545 −9: the page's +543 −33,575 / +547 −2, plus my verdict on `7f451e3` (52 record lines), and `CHANGELOG.md` against main now +16 −8 (the FM-032 bullets and the new comment in; 6 blank separators, main's second heading and its old comment out) |
| `SHOALMARK_REGENERATE=1 python3` 3.14.3 `test_shoalmark.py` (14:56:41–15:16:43) | **570 ok / 0 FAIL**, *skipped here: 0 checks — every check ran*, exit 0 — FM-041's check with the rest; slice A's `checks.json` regenerated as 24 checks, none failing |
| `python3` 3.14.3 `test_core.py` (15:16:43–15:16:48) | **149 ok / 0 FAIL**, exit 0 (FM-041's check included) |
| `/Library/Developer/CommandLineTools/usr/bin/python3.9` 3.9.6 `test_shoalmark.py` (15:16:48–15:32:45) | **567 ok / 0 FAIL**, exit 0; *skipped here: 3 check(s)* — the browser block, *SHOALMARK_REGENERATE=1 is not set* |
| the same 3.9.6 `test_core.py` (15:32:45–15:32:51) | **149 ok / 0 FAIL**, exit 0 |
| the guards | one runner at a time; before each run the `pgrep` pattern printed nothing and the 1-minute load was 2.87, 3.26, 3.08, 3.25; HEAD `2a19789`, the tree clean. From 14:37 to 14:56 my own wait loop's command line held the text the pattern matches, so it kept my runner — and possibly another loop's guard — waiting; fixed by waiting on a file instead |

## The findings

RV-726 to RV-729 stay closed: the merge touches none of the lines they concern — `--ratio`, its tests, the READMEs, the
page and FM-032's section are byte-equal to `57ba840`'s.

## Unproven here

CI on PR 131 (not read here); Windows; a machine with no tz database; the web signature (GitHub's key is not in this clone).

## For the record

This file adds 45 record lines, no product line: after it the change reads records +640 −33,575, product +545 −9.
The page's own-numbers line (+543 / +547) predates my last verdict and this merge; the merge commit of PR 131 will read the
figures above.

path 5 — a merge rules nothing.
