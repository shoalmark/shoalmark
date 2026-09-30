# FM-024 — the Reviewer's scoped check of de9e85a, the Owner's merge of main into the sessions strip

Verdict: **READY WITH FINDINGS (P3 only)** — RV-2098; RV-2099 unminted.
Reviewed: de9e85a83c1aa7b8174d368b09f7021147e07c9c
Reviewer: 8e509911/reviewer-61 (Opus), worktree shoalmark-review-6, 2026-09-30 20:09–20:12 CEST. Independence: same session; reviewer-61, the strip's own Reviewer. Tier: docs, one pass.
Scope: the merge commit de9e85a, parents 37f4be4 (this branch, carrying the READY on cfeb29c) and 5c31699 (main after PR 131 and PR 138), made by the Owner on GitHub at 20:02:03 CEST with `CHANGELOG.md` resolved by hand — a fact, not a finding. Nothing else is in scope.
The proof: `git merge-tree --write-tree 37f4be4 5c31699` conflicts in `CHANGELOG.md` only; `git diff --stat <that tree> de9e85a` lists `CHANGELOG.md` alone (+1 −9). The tree id depends on the conflict markers' labels — 4596344a… with short shas, 17d024e1… with full ones — so the brief's eb7f4d0d… is not reproduced here; the one-path result holds under both.
The resolution (`git diff 4596344a de9e85a -- CHANGELOG.md`): the markers removed, 37f4be4's second heading `## Unreleased` dropped, and the blank lines between bullets removed. The section on de9e85a has one heading, `## Unreleased — 0.19.0`, under main's provisional comment.
Bullet by bullet: 37f4be4's two sections hold 10 top-level bullets and main's section holds 9, 7 of them shared; de9e85a holds 12. Every bullet appears once. None is lost or duplicated. Eleven match their source text exactly; one does not (RV-2098).
The convention: de9e85a's bullets are contiguous, with no blank line between them. Main itself had one, between its fork bullet (FM-006) and FM-041's, and the resolution removed it — consistent with the rest, not a finding.
**RV-2098 · P3 · confidence 97 % — the addressing-rule bullet lost its final full stop in the hand resolution.** On 37f4be4 it ends ``run `--init` again to take it.``, and on de9e85a ``… to take it`` (the Principal's read, verified here). Fix, forward, in the wording pass's post-merge docs commit on main — never a fix commit on this branch: CHANGELOG.md, the bullet *The addressing rule ships with the contract*, ``run `--init` again to take it`` → ``run `--init` again to take it.``
A note for that wording pass, not a finding of this check (the text predates the merge and is not in its resolution): the strip's two bullets name the Owner as `through him` and `his answer of 2026-09-28`, where the Owner's pronoun rule of 2026-09-30 asks for they/them — `through them` and `their answer of 2026-09-28`.
Gates at de9e85a: `--check` exit 0 (*INDEX.md is up to date — 42 trackers*); `--session-check` exit 0.
CI: no local suite (the Owner's ruling of 19:41:15: CI green on the final tree is the full pass). `gh pr checks 139` at 20:12:06 CEST, run 36755674647 on de9e85a: suites macos-latest 3.12, ubuntu-latest 3.12 and 3.9 pass; windows-latest 3.12 and 3.9 pending; CodeQL and Analyze (actions, javascript-typescript, python) pass. Not waited for. PR 139 open, mergeable.
Quality read: the resolution does what the conflict required and no more, but for one lost full stop (RV-2098).
Four numbers for this verdict: records +17, product 0.
path 5 — a merge rules nothing.
