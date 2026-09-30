# FM-006 — public hardening preparation review

**READY for independent review; no implementation findings. This does not clear merge.**
Reviewed `e996a8d8748834965ee1cdbcbcaa2097a1fa67b8` against base `2eb803b293eeb51ee20f95d595ea5d065caa6a2f`.
Reviewer `reviewer@seat`, session `01a0ec25/reviewer-10`, worktree `shoalmark-review-public-hardening`.
Same root as the Principal: not independent. AGENTS rules make this critical under TRIAGE path 3;
an independent session must review before merge. The diff is documentation only, with no active gate/config change.

Read the complete two-file diff. GitHub's official ruleset, Actions, CodeQL and security-configuration
[documentation](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets)
supports the sheet's linked instructions: creation bypass is isolated from immutable-tag restrictions;
GitHub-only external actions preserve the disclosed local/org exception; new-public-repository defaults are scoped.
Live read-only main-ruleset and CodeQL responses match the baseline. Workflow references all use `actions/`.
Git confirms PR #119 deleted six port files, modified `port-rd.md`, and retained history. No rewrite is claimed.
The agent rule separates contributed data from authority without granting authority merely through membership.
Reserved identity decisions remain with the Owner; FM-006 filing remains with Principal `8e509911`.

`git diff --check origin/main...HEAD` passed. Application suites were not repeated for this documentation change.
The Principal's six shell-block rehearsals were reviewed as reported evidence, not independently rerun.
No settings writes, browser execution, tag push or enforcement probe: applied settings and successful CodeQL analysis remain unverified.
