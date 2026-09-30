# FM-024 — cold review of the shipped seat definitions

Verdict: READY WITH FINDINGS (P3 only).
Reviewed: b872b93d542544407d567f71b4a064d7c12aad15
Reviewer: dc55e1df, independent of 8e509911; own worktree shoalmark-seat-definitions-cold; 2026-09-30.
Tier: critical; origin/main...HEAD contains two harness prompt/configuration files and FM-024, requiring an independent session.
Scope: bd34852..b872b93d is exactly three files, +24/-0; FM-024 front matter and INDEX unchanged.
Frontmatter: Implementer name/description/model: sonnet/effort: xhigh; Reviewer name/description/model: opus; no tools or capability-granting fields.
Harness fields, project-over-user precedence and inherited tool pool verified against [official subagent documentation](https://code.claude.com/docs/en/sub-agents); runtime model execution was not tested.
Bodies bind both seats to AGENTS.md, the complete brief and their own worktree; Reviewer requires quality read, allocated ids and Reviewed trailer.
P3 finding (no id allocated): reviewer.md omits the brief's explicit spawning and pull-request prohibitions; Implementer includes both.
Exact fix: insert `Spawn nothing. Open no pull request.` after `and never in another seat's worktree.` in reviewer.md.
This is an omitted prompt constraint, not an added tool grant; fix forward. No P2 or higher finding.
Quality read: concise scoped definitions; no AGENTS.md contradiction, foreign project name or secret shape; no obsolete tracked artifact identified.
Owner raise: one physical line, 09:12:44, normalised and marked; source is his word, with no relay or hash. Ship log adds one row.
Trailers verified: Session: 8e509911; Worktree: shoalmark-principal-4.
Checks: python3 shoalmark.py --check exit 0; --session-check exit 0; git diff --check exit 0.
Merge: git merge-tree --write-tree origin/main b872b93d exit 0, tree e7c373c1e1b0a589a76fcc0d59fc98e3759af2d2; origin/main = bd34852b2a3f63d88524561b27fdb4bbeb1684b3.
Queue quoted: `branch fm/024-the-seat-definitions-shi… @ b872b93  wait: no pull request — no verdict on b872b93`
Queue quoted: `4 waiting on you: 0 merge, 0 close, 2 wait, 2 pushed without a pull request` (PRs 118, 121; this branch and fm/032).
Four numbers at reviewed tip: records +2; product +22; records deletions 0; product deletions 0. This 22-line evidence file adds records +22: totals +24/+22/0/0.
path 5 — a merge rules nothing.
