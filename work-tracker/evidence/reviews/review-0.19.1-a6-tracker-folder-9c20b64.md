# v0.19.1 — A6, the tracker folder: the review at 9c20b64

Verdict: **READY**. RV-2346 (P2) is closed. RV-2347 onward are unused.
Reviewed: 9c20b641a33f2990a2448c2b48af15e9beaff759 — `git diff 1f73865 9c20b64`: three commits (96fa872, 9fd5e19, 9c20b64) to `shoalmark.py` and `test_shoalmark.py`, against the Owner's rulings of 2026-10-04.
Reviewer: b3bdb000/reviewer-85 (claude-opus-5-5, xhigh), at the reviewer's bot address, unsigned, in worktree shoalmark-review-9, on 2026-10-04. Not independent: this is the build's session. Tier: critical — code, so the full loop.

## What holds

- **`--init`** judges the tracker folder first, as every run does. Where the folder lies outside the repository, resolves outside it, is reached through a symlink or lies in a git directory, `--init` refuses in the tracker folder's one line, exit 4, and writes nothing anywhere. Probed in scratch, listing the whole folder (git directory included) before and after: `../outside`, the same through a symlink, an absolute path, a link to a folder beside the repository, a link to a folder inside it, `.git/inert`, and `docs/../../outside`.
- **The other writers:** every command that writes under the tracker folder judges it before its first write. Probed: the default run, `--print-written`, `--new`, `--triage`, `--standup FILE`, and `--html-only` with its own check. The rest write nothing under it.
- **9c20b64:** the write rule and the tracker folder's judgement find the git directory as the file system compares paths, taking the path both as written and as it resolves. `git_dir_holding`, `fs_identity` and `fs_fold` are release/v0.19.1's at 64f3528, byte for byte.
- **Probed at 9c20b64:** each of these is refused in one line, exit 4, with nothing written into the git directory: `.GIT/inert` and `.Git/Hooks` under `--init`; `.GIT/hooks` under the default run and under `--html-only`; `.GIT/inert` with `--root` given in the other Unicode normalization. `docs/work-tracker` is accepted.
- **Still accepted:** `--init` in a fresh repository, and in one already initialised.
- **The changed check** (`--brand DIR` and `--init` through a folder that is a symlink) now asserts, for `--init`, the tracker folder's line, exit 4 and nothing written, as the ruling says. Its name keeps the ledger row's words.
- **The skip:** the two new checks skip, visibly, only where a probe shows the file system keeps case. Where the probe cannot run, they fail.
- The commit messages and test names say what is asserted.

## Findings

- **RV-2346 · P2, closed in 9c20b64:** the git directory, found as the file system finds it.

## Commands and controls, as `date` printed them

- At 9c20b64: `py_compile` ok. `test_core.py`: 158 ok, all green, exit 0. `--check` and `--session-check` exit 0. 10:09:40–10:10:01 CEST.
- At 9c20b64, with `run-one-check.py`, every one of these exits 0, 10:08:48–10:11:57 CEST: A6's six refusal cases and its still-accepted check; the changed check and its control; the write rule's blocks (INDEX.md, the calendar files, the copies, the triage worksheet); two `--init` blocks.
- A6's six cases and the changed check exit 1 beside `1f73865`'s tool and 0 at 9fd5e19, 09:32:57–09:38:01 CEST. The still-accepted check exits 0 at both.
- The two new checks exit 1 beside `1f73865` and beside 9fd5e19, and 0 at 9c20b64. 10:08:48–10:11:57 CEST.
