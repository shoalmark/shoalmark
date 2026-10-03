# FM-024 — the Builder's model, by tier: the review at a9aff9d

Verdict: **READY WITH FINDINGS**. Two P3s, fixed forward with no re-pass (docs tier). RV-2321 is taken on main (`review-security-ledger-7a37da0.md`); RV-2324 to RV-2329 are unused.
Reviewed: a9aff9d9ba3ea9704a827a75f195c599244570e1 — `git diff d9c154b a9aff9d`, the Planner's `2ae5ba5` and `a9aff9d`, against the Owner's ruling of 2026-10-02 as FM-024 files it.
Reviewer: b3bdb000/reviewer-84 (claude-opus-5-5, xhigh), at the reviewer's bot address, unsigned, in worktree shoalmark-review-10, on 2026-10-03. Independence: the change's session (b3bdb000), so not independent. Tier: docs — `git diff --name-only origin/main...HEAD` names `.claude/agents/builder.md`, FM-024 and `work-tracker/INDEX.md`; `builder.md` changes in its description and one body sentence, its `model:` and `effort:` keys are unchanged, and the gate reads none of it.

## What holds

- `builder.md` keeps `model: sonnet` and `effort: xhigh`. Its description: Sonnet 5.5 at xhigh by default, Opus 5.5 at xhigh for a critical brief, and the four critical areas.
- The body sentence reads as a condition — *where your brief is critical and you are not running on Opus, or where your work reaches a critical path your brief did not name* — and names the gate as a hook, a refusal, what a commit is judged by. Its stop on an unnamed critical path follows from the ruling: such a change is critical, and its brief must name that tier.
- FM-024's section states the ruling's four parts and attributes nothing else to it; beyond them it records the change's route only. Its copy of the body sentence states the same rule. No other file states the Builder's model.
- The diff names no unfixed 0.19.1 item. The two commit messages say what changed; `a9aff9d`'s names the wording it fixes, as AGENTS.md (FM-032 S3) asks of a fixing commit.

## Findings

- **RV-2322 · P3:** `builder.md` drops the ruling's *in doubt, it is critical* from its description and its body sentence. Fix — the description: "… seats and rights, the gate; in doubt, critical (the Owner's ruling of 2026-10-02)."; the body: "Your brief names its tier in its first lines, and in doubt it is critical: where your brief is critical and you are not running on Opus, …".
- **RV-2323 · P3:** FM-024's *What is true now* names neither the ruling of 2026-10-02 nor this branch (AGENTS.md rule 1). Fix — at its top: "**2026-10-02 — the Builder's model, by tier.** The Owner's ruling is filed below, in *The Builder's model, by tier — after v0.19.0*; `builder.md` says it on `fm/024-the-builder-s-model-by-tier`. **What is left:** the Owner's merge."

## Commands — 2026-10-03, CEST, each time as `date` printed it

- The branch tip on origin is `a9aff9d` (21:49:55). At `a9aff9d`: `py_compile` exit 0 (21:51:57); `test_core.py` all green, 158 ok, exit 0 (21:52:09); `--check` exit 0, INDEX.md up to date (21:52:21); `--session-check` exit 0 (21:52:21).
- `git merge-tree --write-tree origin/main a9aff9d`, main at `1f73865`: clean, tree `e4f5086`. `--check` at that tree in a scratch clone: exit 0, INDEX.md up to date (21:53:27). Both sides change only INDEX.md's Generated line, to the same date, so it is not stale after the merge.
- Controls at that tree (21:53:41–21:53:55): FM-024's triage row removed from INDEX.md — `--check` exit 3, STALE; the Generated line alone changed — exit 0.

Quality read: the two defects are RV-2322 and RV-2323; the rest reads clean.
