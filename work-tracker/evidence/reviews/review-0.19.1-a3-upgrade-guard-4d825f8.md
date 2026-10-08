# FM-006: v0.19.1 A3, the upgrade guard, the review at 4d825f8

Verdict: **READY WITH FINDINGS**: three P3s and one finding recorded privately; no P1. Ids RV-2650 to RV-2653; RV-2654 to RV-2669 are unused.
Reviewed: 4d825f8974d148d5518bf90f4309b730c6da3c08, `git diff 1f73865 4d825f8`: A3's nine commits (`shoalmark.py`, `test_shoalmark.py`), against the Owner's rulings of 2026-10-03, 2026-10-04 and 2026-10-07. Tier: critical (security: FM-037's guard and its signers file). A full pass over every round; round 6 is 4d825f8.

## What holds

- Where the default branch's configuration cannot be read (`read_config` refuses it, `tracker_dir` holds a backslash or is no folder of the repository, `[headings]` is not the table, or git records a submodule, a folder or a symlink at its path), every commit that changes a TRIAGE.md, the configuration or a signers file is refused by `--check`, `--commit-msg` and a merge being made, signed or not, in one line ending on the way through. A path with nothing at it is the adoption, and it passes. `--queue` waits, naming the configuration.
- A configuration on either side of a commit that this tool cannot read is never read as the defaults.
- The guard reads the tracker folder from `tracker_folder`, as the tool does. A TRIAGE.md, the configuration or a signers file in another case or Unicode normalization is refused on every system: in a commit, a merge, an octopus, a move of the home or at the branch tip. `--queue` waits on such a tip.
- `--commit-msg` judges what the index stages; `--check` walks every commit since the default branch.
- The signers file: which working tree holds it is decided by the file system's identity, and it is read at the default branch's copy in git's spelling. A configured path on which a name is a symlink lying in a checkout of this repository, or in another git working tree, verifies nothing; so does a file in another clone's working tree. A working tree whose folder is gone holds nothing.
- Still accepted, the Owner's signed change: with the signers file named directly, relative to the root, in another case, through `/tmp`, the firmlink or a link outside every git tree, or in no git tree; beside a gone worktree's folder. The answer gate verifies against the default branch's copy as before.
- The shared helpers `worktree_tops`, `tree_holding`, `git_dir_holding`, `fs_identity`, `fs_chain` and `fs_fold` are byte-identical to 359473c (`diff` exit 0 each).

## Findings

- **RV-2650:** recorded privately.
- **RV-2651 · P3 · class 1:** A3's next change after 0.19.1.
- **RV-2652 · P3 · class 1:** A3's next change after 0.19.1.
- **RV-2653 · P3 · class 1, records:** A3's next change after 0.19.1.

## Commands and controls: 2026-10-07, CEST, as `date` printed each

- `py_compile` exit 0; `test_core.py` 158 ok, all green, exit 0 (08:46:55–08:47:06). `--check` exit 0; `--session-check` exit 0 (09:09:50–09:09:57).
- The 17 TRIAGE.md and FM-037 blocks: 162 ok, 0 failed (09:06:15–09:14:34). The 57 signing, configuration, hook and `--queue` blocks: 267 ok, 0 failed, the Chrome block :4304 among them (09:14:43–09:25:08).
- The FM-037 block: 57 ok in 212.7 s at HEAD (09:25:36–09:29:09); 53 ok in 208.2 s at 264819d with its own tests (09:29:09–09:32:38).
- Controls, run-one-check two at a time (08:52:26–09:55:23). Round 6's three checks exit 1 beside 1f73865 and beside 264819d, and 0 at HEAD. The gone-worktree acceptance exits 1 beside 264819d, and 0 at HEAD and beside 1f73865. Round 5's eight each exit 1 beside 1f73865 and beside d5f3428. The backslash check exits 1 beside 1f73865 and 8a211dc, and 0 at HEAD.
- The FM-037 block run beside each round's parent: at HEAD its 37 v0.19.1 checks pass (57 ok). Round 4's checks fail beside 325e793, round 3's beside 8a211dc, round 2's beside cb6176a, and round 1's beside 1f73865. Every still-accepted check passes at HEAD.
- The probes of every earlier pass give the same result at 4d825f8 as at 264819d (74 cases), except the three that round 6 rules. The guard's walk names the same commits over main's history and tonight's branches at 1f73865, 264819d and 4d825f8. `--queue` makes the same git calls per pull request as at 264819d, plus one tree listing where the tip's home moved.

Quality read: the defects are RV-2650 to RV-2653; the rest reads clean.
