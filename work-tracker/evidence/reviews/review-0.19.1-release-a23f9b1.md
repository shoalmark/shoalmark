# FM-006: v0.19.1, the release branch, the review at a23f9b1

Verdict: **READY WITH FINDINGS**: two P3s open, and four findings fixed on the branch and measured; no P1 or P2 stands. Ids RV-2690 to RV-2696; RV-2697 to RV-2709 are unused.
Reviewed: a23f9b103438aeec5ae2dac3d47b26856769637e. Scope: `git log --first-parent 359473c..a23f9b1`: the release lane (359473c: A4, B1, the date fix) with A1 (a8bfd9b), A6 (a71295e), A3 (9091fea) and A2 (c417c0e) merged in with `--no-ff`, the combine's checks and fixes, README's merge sentence, the FM-006 filing, the cut and the release's text fixes. Tier: critical (security: every Queue A fix, merged).

## What holds

- Each merge keeps both sides: every line a branch added is at a23f9b1, except where its meeting rules otherwise. No top-level name is defined twice. `git_dir_holding`, `fs_identity`, `fs_fold`, `fs_chain`, `tree_holding`, `worktree_tops` and `import unicodedata` appear once each. `in_git_dir_on_disk` serves `tree_write`, `write_problem` and `tracker_folder_problem`. The release lane's `config_file_problem` stands, and `init()` judges the tracker folder once, at its top.
- `brought`, shared by the branch's walk and a merge's, lists merges (`-c`, no `--no-merges`) and reads each against all its parents. It keeps its label and refuses a walk git cannot make. `rights_problems` reads the commit being made from the index and judges a made merge's own `next: owner` as `ask`.
- `--check` refuses a merge inside a branch whose own change closes a tracker, made by a seat without `close` under a later commit, at the tip and at the branch's merge into the trunk. A staged close inside a merge made through the hooks is refused. A merge's own `next: owner` or answer is refused, a holder's included. A merge identical to the parent that carries the Owner's answer credits the Owner.
- A tag or a branch named for the default branch moves neither the Owner, nor the signers file, nor the walk.
- On Subversion, a copied answer, `next: owner`, status or triage key is refused where its copier or its own author lacks the right, under `[seats]` and, for an answer, under `answerers`. That holds after a merge that ignores ancestry, a reverse merge, a copy of a copy, a move, a copy from an earlier revision and a copy whose source is gone. A `considered:` changed after its filing is judged under its own author.
- Still accepted: a holder's copy of a holder's close, a `considered:` set at the filing, an ordinary trunk edit, a holder's own close, a merge that brings no guarded line, and a branch of trunk.
- The filing is the draft's text. The CHANGELOG's 0.19.1 section is the Owner's text: the cut's text byte for byte, with the Owner's three changes of 2026-10-07. VERSION is 0.19.1. ADOPT.md and ADOPT.de.md name `v0.19.1` and the SHA-256 of a23f9b1's `shoalmark.py`.

## Findings

- **RV-2690:** fixed at 6141e36, measured.
- **RV-2693:** fixed at b5413fa, measured.
- **RV-2694 · P3 · records:** the CHANGELOG's Subversion copy line. Fixed at a23f9b1.
- **RV-2695 · P3:** the CHANGELOG's Subversion section repeated two statements. Fixed at a23f9b1.
- **RV-2691 · P3:** fixed at a23f9b1 in the tool's output and its docstring, but the comment at test_shoalmark.py:6362 still names the server's pre-commit hook as the layer that refuses. Fix: "and `--check` after the commit is what judges it".
- **RV-2692 · P3 · records:** 1585757's body words A3's signers-file rule differently from the CHANGELOG, and 3705340's body words a merge's own `next: owner` differently too. The CHANGELOG's words are the ones that hold.
- **RV-2696:** not a finding against this release (the Owner's ruling of 2026-10-07).

## Commands and controls: 2026-10-07, CEST, as `date` printed each

- At d7ae95b: `py_compile` exit 0; `test_core.py` exit 0, all green; `--check` exit 0, INDEX.md up to date; `--session-check` exit 0 (16:25:45–16:26:24).
- At d7ae95b, 122 blocks: every item's, rights, FM-037, the FM-019 merges, the tracker folder, `--install-hook`, `--init`, the board's days, Subversion, and the README and docs readers. 119 exit 0, with 628 checks and 0 skips; the other 3 read an earlier block's state and run in the full suite (16:49:15–17:49:09).
- At a23f9b1: `py_compile` exit 0; `test_core.py` exit 0, 158 ok; `--check` exit 0, INDEX.md up to date; `--session-check` exit 0 (18:17:07–18:17:33).
- At a23f9b1, 29 blocks: the combine's checks, the copy rule's, Subversion, and the VERSION, CHANGELOG, ADOPT, README and setup readers. All 29 exit 0, with 259 checks and 0 skips (18:17:42–18:35:43).
- Controls, run-one-check two at a time:
  - One check per item (A1, A2, A3, A4, A6, B1, the date fix): exit 1 beside 1f73865.
  - The combine's merge-in-branch check: exit 1 beside 1f73865, 0c3abb1 and a8bfd9b.
  - The two copy refusals: exit 1 beside c417c0e. These controls ran 17:38:44–17:46:04.
  - The `answerers` check: exit 1 beside d7ae95b. The `considered:` check: exit 1 beside c395594 and beside 1f73865.
  - The two checks of a merge's own answer and `next: owner`: exit 0 beside d7ae95b and exit 1 beside 1f73865 (18:11:50–18:16:21).
- Checks: 893 at d7ae95b, which is the release lane's 787 plus the branches' 6, 3, 38 and 55 plus the combine's 4. 897 at a23f9b1.
- The Subversion cases, measured by probe with a23f9b1's tool: the refusals exit 4 and the accepted cases exit 0 (18:29:26–18:35:33; with b5413fa's, 17:33:38–17:54:57).

Quality read: the open defects are RV-2691's comment and RV-2692; the rest reads clean.
