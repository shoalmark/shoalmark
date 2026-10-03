# v0.19.1 — A4, `--install-hook`'s configuration check: the review at e9d9e0a

Verdict: **READY WITH FINDINGS** — three P3, and none holds READY. RV-2343 onward are unused.
Reviewed: e9d9e0ae028fc9f6f8e93745c3da6c6817ece806 — `git diff 1f73865 e9d9e0a`, four commits to `shoalmark.py` and `test_shoalmark.py`, against the Owner's ruling of 2026-10-03.
Reviewer: b3bdb000/reviewer-85 (claude-opus-5-5, xhigh), at the reviewer's bot address, unsigned, in worktree shoalmark-review-9, on 2026-10-03. Independence: this is the build's session (b3bdb000), so not independent. Tier: critical — code, by `git diff --name-only origin/main...HEAD`: the full loop.

## What holds

- **8093fcb, a refactor:** behaviour is identical. `in_git_dir` gets the same path, the trees are compared in the same order, and the same tree is returned and named.
- **c0dc6f7, every worktree:** every path is judged against every folder `git worktree list` names, removed ones included. Each worktree's settings are read from its git directory (`git --git-dir=… config --list --show-origin -z`), its `config.worktree` and its includes with them. `worktree_tops` has two callers, and both judge every worktree.
- **4ad3922, unreadable:** where `git config` fails, or a file of a worktree's own configuration is not a regular file that opens, the refusal is one line. It names the worktree and git's error, or the file and why, and no hook and no copy is written. A `config.worktree` that is not a regular file is refused where `extensions.worktreeConfig` is off. That is right, not a finding: it fails closed, and git reads that file once the extension is on.
- **e9d9e0a, the file system's comparison:** a path lies in a tree where it, or an existing ancestor, is the tree's folder by device and inode; a target not there yet goes by its nearest existing ancestor. The `normcase` compare stays beside it. A path in the git directory spelled in another case passes only where that spelling is the git directory by device and inode. On Windows both `normcase` compares stay, and identity only adds refusals.
- **Still accepted at e9d9e0a:** `.git/hooks`, `.git/config`, a target outside every tree, and a removed worktree with no settings of its own.
- **Probed on this macOS machine (APFS, case-insensitive), in scratch:** each of these is refused in one line, with nothing written — an include into the tree, the tree or an ancestor spelled in another case, the target there or not yet; an include into a removed tree, spelled the same way; a `config.worktree` that is not a regular file, or does not open. The git directory spelled in another case is accepted, both as an include target and as `core.hooksPath`.
- **README:** no sentence changed, and none about these checks is false. The four commit messages and the new test names say what is asserted.

## The findings

- **RV-2340 · P3:** in `fs_chain`. Its fix text goes to the Planner, not here.
- **RV-2341 · P3, the cost:** with 60 worktrees, 10 of them removed, the configuration check takes 5.9 s. With each tree's identity read once, it takes 3.6 s. Fix: build `{top: fs_chain(top)[:1] for top in tops}` once in each caller and pass it to `tree_holding`, which reads `folder = tops[top]`. In `config_file_problem`, judge each origin once per worktree: `for origin in dict.fromkeys(listing[0::2]):`.
- **RV-2342 · P3:** no caller passes `include_targets`' `here` any more (rule 6). Fix: drop `here=None`, read a relative origin from `ROOT`, and say "run at the repository's root" in the docstring.

## Commands, as `date` printed them

- `python3 -m py_compile shoalmark.py test_shoalmark.py`: ok. `python3 -u test_core.py`: 158 ok, all green, exit 0. 23:13:18–23:13:32 CEST.
- `--check` exit 0, `--session-check` exit 0. 23:13:38–23:13:59 CEST.
- The blocks the change reaches, run at e9d9e0a with `run-one-check.py`, every one exit 0, 23:16:25–23:33:02 CEST:
  - the hooks folder: 5 checks and its control;
  - the git configuration's files: 3, and 2 controls;
  - every include setting's target: 2, and 2 controls;
  - every worktree's configuration: 2, and its control;
  - the three new blocks: 11.

## The controls

- `run-one-check.py --tool 1f73865`: each of the nine new checks that refuse exits 1. At e9d9e0a, each exits 0. 23:16:25–23:23:18 CEST.
- The two new checks that accept exit 0 at both: a target outside every worktree, and `core.hooksPath` as the git directory's `hooks` in another case. They show the comparison refuses no more than it should.
