# FM-006 — cold review of the public-hardening run sheet and the AGENTS.md section

Verdict: NOT READY — one P2, RV-2040, run-sheet step 6; no other finding.
Reviewed: b1ffbb8e70e427eb80059418726fbdb8d6112e0a (e996a8d and its same-session docs pass); base origin/main 2eb803b.
Reviewer: 606d54f2, independent of 01a0ec25 and 8e509911; own worktree shoalmark-cold-hardening-b1ffbb8; 2026-09-30.
Tier: critical, path 3 (AGENTS.md rules changed by a seat). `git diff --name-only origin/main...b1ffbb8`: AGENTS.md and two
work-tracker/evidence files, +157/-0; no .py, toml, hook, test or .github change, so no suite was run.
(1) The AGENTS.md section, outside the markers, agrees with the loop's signed rules, message rule 6, path 5 and the relay
ruling (a relay is a finding to grade); it grants nothing; every sentence can be obeyed and checked (author association).
(2) Steps 1–5 and 7 match GitHub's current docs: any team but a secret one may bypass; tag rules Restrict creations, updates,
deletions and Always allow exist; rulesets aggregate, so the creation bypass cannot move or delete a tag; the merge checkboxes
and allowed merge methods; GitHub-created actions cover `actions` and `github` (CodeQL); Advanced Security → CodeQL analysis
→ Set up → Default. No agent writes a setting, pushes a tag or probes; every step stops; credentials and email stay his.
RV-2040, P2 (the block RV-2040 to RV-2049; the rest unused): step 6 cannot be done as written. Current docs: organisation
Settings → Advanced Security → Configurations (the sheet: Code security); secret scanning and push protection sit inside
"Secret Protection", which the page calls "a paid feature for private repositories". The sheet says to enable them and
not to "enable paid products", so the Owner stops or guesses. GitHub's API places configurations under
/organizations/shoalmark/settings/security_products/; the sheet opens …/settings/security_analysis (unverified: login).
Fix, lines 82–84: `In organisation Settings → Advanced Security → Configurations, choose New configuration, name it
public-repository-defaults. Enable Secret Protection (paid only for private repositories) with secret scanning and push
protection; enable dependency graph, Dependabot alerts and security updates; leave Code Security unset. Under Use as default
for newly created repositories choose Public; apply it to no existing repository.` Line 89: open …/security_products,
expecting Configurations. Line 92: stop if payment or a licence is requested. Sheet only; AGENTS.md needs no change.
Baseline, GET only: merge, squash, rebase on; ruleset 24177420 active, no bypass, deletion, force-push, creation, five suites,
allowed_merge_methods [merge, squash, rebase]; no tag ruleset, no teams, admin holgo99; CodeQL not-configured (actions,
javascript-typescript, python); Actions all, token read, fork approval all external; Free plan; org and configuration
defaults off and []. Not readable: the org Actions policy (403) and the settings pages (login).
(3) b041cb2 (PR 119) deletes the six port/ files and modifies port-rd.md; all six are at 80d0811, an ancestor of main.
No rewrite is claimed. (4) Only holgo99, in setting steps and the admin read; no other project, person, relay or hash.
(5) --check 0; --session-check 0; git diff --check 0; git merge-tree --write-tree origin/main b1ffbb8 0, tree 8e4a1d67;
trailers Session: 01a0ec25 (e996a8d), 01a0ec25/reviewer-10 (b1ffbb8). Queue quoted, then its count:
`branch fm/006-public-hardening-follow-… @ b1ffbb8  wait: no pull request — no verdict on b1ffbb8`
`5 waiting on you: 0 merge, 0 close, 2 wait, 3 pushed without a pull request`
Four numbers at the tip: records +150, product +7, deletions 0 and 0; this file adds records +35: totals +185/+7/0/0.
path 5 — a merge rules nothing.
