# v0.19.1 — A4, the fix round: the check at d4fb074

Verdict: **READY**. RV-2340, RV-2341 and RV-2342 are closed, with no new finding. RV-2343 onward are unused.
Reviewed: d4fb074f301d1d2d71fc61e24443866f15d9cd88 — `git diff 777ec02 d4fb074`, two commits to `shoalmark.py` and `test_shoalmark.py`. The pass this answers is `review-0.19.1-a4-config-check-e9d9e0a.md`.
Reviewer: b3bdb000/reviewer-85 (claude-opus-5-5, xhigh), at the reviewer's bot address, unsigned, in worktree shoalmark-review-9, on 2026-10-04. Not independent: this is the build's session. Tier: critical — code.

- **20f4c8c, a refactor (RV-2341, RV-2342):** behaviour is identical. Each tree's identity is read once per check, and each origin is judged once per worktree, in its first order. `include_targets` reads a relative origin from `ROOT`, where every caller runs git. With 60 worktrees, 10 of them removed, the configuration check takes 2.84–2.89 s, 00:26:50–00:27:34 CEST.
- **d4fb074 (RV-2340):** `fs_fold` (NFD, then case-folded, then NFD) gives the same answer as this machine's APFS on all 19 name pairs probed, for case and Unicode normalization alike. An include into a removed worktree, spelled in the other normalization, is refused in one line, with nothing written. The git directory spelled so is accepted, both as `core.hooksPath` and as an include target.
- **Controls:** the new check that refuses exits 1 beside `1f73865`'s tool and beside `e9d9e0a`'s, and 0 at d4fb074. The new check that accepts exits 0 at d4fb074 and 1 beside `e9d9e0a`'s.
- **Commands:** `py_compile` ok. `test_core.py`: 158 ok, all green, exit 0. `--check` and `--session-check` exit 0. These ran 00:23:03–00:23:29 CEST. At d4fb074, every block the change reaches exits 0, the new block included, 00:22:58–00:26:40 CEST.
- **The two commit messages and the new test names** say what is asserted.
