# FM-024 — the Builder's model, by tier: the check at 6b4d4d1

Verdict: **READY**. RV-2322 and RV-2323 are fixed; no new finding. The rest stands as `review-fm024-the-builder-s-model-by-tier-a9aff9d.md` judged it.
Reviewed: 6b4d4d144ad142ecbefc1af0ededa0969c5a0500 — `ed64ca2` on `1782c8c`, and `6b4d4d1`, which merges main at `1f73865`.
Reviewer: b3bdb000/reviewer-84 (claude-opus-5-5, xhigh), at the reviewer's bot address, unsigned, in worktree shoalmark-review-10, on 2026-10-04. Not independent. Tier: docs — `git diff --name-only origin/main...HEAD` names `.claude/agents/builder.md`, FM-024, `work-tracker/INDEX.md` and the a9aff9d verdict.

- **RV-2322:** builder.md's description ends "…the gate; in doubt, critical (the Owner's ruling of 2026-10-02)." Its body sentence reads "Your brief names its tier in its first lines, and in doubt it is critical: where your brief is critical and you are not running on Opus, …". Both match the verdict's fix text word for word, and no other word of builder.md changes. `model: sonnet` and `effort: xhigh` stand.
- **RV-2323:** FM-024's *What is true now* opens with the verdict's paragraph, word for word.
- **`git diff 1782c8c ed64ca2`:** exactly builder.md, FM-024 and INDEX.md's Generated line.
- **The merge:** `git diff 1f73865 6b4d4d1` carries the branch's own changes to builder.md, FM-024 and the a9aff9d verdict, line for line, and INDEX.md's Generated line, nothing else. `git merge-tree --write-tree 1f73865 6b4d4d1` is clean, and its tree is the head's own, `4f8e23c` (08:43:39).
- **Commands** (CEST, as `date` printed them): at `6b4d4d1`, `--check` exit 0, INDEX.md up to date (08:43:59); `--session-check` exit 0 (08:43:59).

Quality read: clean.
