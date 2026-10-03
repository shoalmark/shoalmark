# v0.19.1 — A1, a merge a merge brings: the scoped check at 6fb9b83

Verdict: **READY**. RV-2324's README half and RV-2325 are fixed; no new finding. RV-2326 to RV-2339 are unused. The rest stands as `review-0.19.1-a1-merges-efd500c.md` judged it.
Reviewed: 6fb9b8348fe802bc814dbe8a5d6f0d607ea62b1f — `git diff 8a29c15 6fb9b83`, the Builder's `3dbbe1b` and `6fb9b83`. Reviewer: b3bdb000/reviewer-84 (claude-opus-5-5, xhigh), unsigned, in worktree shoalmark-review-10, on 2026-10-04. Not independent. Tier: critical.

- **The texts:** README.md:345–346, `seat_problems`' docstring, `rights_problems`' docstring and the `on_line` comment are word for word the verdict's fix texts. `rights_problems`' parenthetical also drops its sentence on the merge being committed. `seat_problems`' docstring still says how a line not yet committed is read, so nothing asserted is lost. The Subversion sentence is rewrapped with the same words.
- **The AST**, with every docstring masked, hashes the same at `8a29c15`, `3dbbe1b` and `6fb9b83`; unmasked, it differs, as the docstrings do. `test_shoalmark.py` is unchanged.
- **The commit messages** say what is asserted, and are lean.
- **Commands** (CEST, as `date` printed them): `py_compile` exit 0 (00:18:36); `test_core.py` all green, 158 ok, exit 0 (00:18:49); `--check` exit 0 (00:18:56); `--session-check` exit 0 (00:18:57); the 21 `test_shoalmark.py` blocks that read the README, 76 ok, 0 failed, exit 0 (00:18:35–00:22:41).

Quality read: clean.
