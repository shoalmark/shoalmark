# FM-006 — public repository hardening: Owner run sheet

Prepared 2026-09-30 by session `01a0ec25`, Principal. Scope: `shoalmark/shoalmark` and its organisation.
This prepares settings; none have been changed by the seat. The Owner applies them in GitHub's browser UI.
FM-006's filing remains with Principal `8e509911`; this sheet supplies the result for that filing.

## Read-only baseline and limits

Checked against main `2eb803b293eeb51ee20f95d595ea5d065caa6a2f` and live GitHub API on 2026-09-30:
- Repository permits merge, squash and rebase; main ruleset `24177420` permits the same three methods.
- Main ruleset is active, no bypass, with creation/deletion/force-push restrictions and five required `suites` checks.
- No tag ruleset; org teams list empty; sole org administrator returned: `holgo99`.
- CodeQL default setup: `not-configured`; repository Actions: enabled, `allowed_actions: all`.
- Org defaults: dependency graph, Dependabot alerts/security updates, secret scanning/push protection all false.
- Code-security configuration defaults: empty. Org Actions policy read: HTTP 403, missing `admin:org` scope.
- Existing workflow action references are all under `actions/`; no third-party action replacement is needed at this head.
These are dated observations, not a repeat of the Auditor's full history/PR-head audit.
No token scope expansion, release tag, test push or history rewrite was performed.

## Owner steps — stop on an unexpected screen or value

Use the Owner's browser login `holgo99`. Each command only opens the named settings page on macOS.
The changes described below are explicit browser actions. Complete both tag rulesets before Friday's `v0.19.0` tag.
Do not test protection by pushing a disposable `v*` tag: it would trigger release CI and documentation deployment.

1. Create a visible team `release-owner`, with **only `holgo99`** as member/maintainer, no parent team.
   Give this team Write access to `shoalmark/shoalmark`; check there are no inherited/additional members.
   The dedicated team avoids granting tag creation to every present or future repository administrator.

   ```sh
   open 'https://github.com/orgs/shoalmark/teams'
   ```
   Expected: team `release-owner`, visible (not secret), one member `holgo99`, repository Write access.
   Stop if the team already exists with other members or inheritance. Paste back: `release-owner: holgo99 only, Write, no parent`.

2. Create two **tag** rulesets, targeting Include by pattern `v*`, no exclusions, enforcement **Active**.
   First `release-tags-immutable`: Restrict updates + Restrict deletions; **empty bypass list**.
   Then `release-tags-owner-create`: Restrict creations only; bypass team `release-owner`, **Always allow**.
   Do not put update/deletion restrictions in the creation ruleset: its bypass would permit both.

   ```sh
   open 'https://github.com/shoalmark/shoalmark/settings/rules'
   ```
   Expected: both active tag rulesets, same `v*` scope; immutable has zero bypass actors; creation has exactly that team.
   Stop if either restriction or team cannot be selected. Paste back: both ruleset URLs and `active; immutable: no bypass; creation: release-owner`.
   Rules aggregate. The Owner may create a new release tag but cannot move/delete one while these rules hold.
   Admins can still edit rules, and an agent using the Owner's credentials is indistinguishable from him.

3. In repository Settings → General → Pull Requests, keep **Allow merge commits**, clear **Allow squash merging**
   and **Allow rebase merging**. Then edit main ruleset `24177420`: in its pull-request rule, allow **merge only**.
   Preserve all five required suites, all existing restrictions and its empty bypass list. Do not enable linear history.

   ```sh
   open 'https://github.com/shoalmark/shoalmark/settings'
   ```
   Expected: repository and main rule both allow only merge; other main rules unchanged.
   Stop on any changed required-check list. Paste back: `repo merge only; main allowed_merge_methods=[merge]; five suites; no bypass`.

4. In repository Actions → General, choose the policy allowing own actions and selected external actions.
   Check **Allow actions created by GitHub**, clear **verified creators**, and leave specified external patterns empty.
   Apply the same selection in organisation Settings → Actions → General using the org-settings link in that UI.
   Preserve enabled repositories, read-only workflow token and fork approval requirements.

   ```sh
   open 'https://github.com/shoalmark/shoalmark/settings/actions'
   ```
   Expected: selected-actions policy; GitHub-owned true, verified false, patterns empty, at both levels.
   GitHub's policy also allows local/organisation-owned actions; it cannot literally prohibit every non-GitHub action.
   Stop if the org policy is inaccessible or imposes a different restriction; do not widen it to make this step pass.
   Paste back: `repo + org selected; GitHub-owned only external; verified off; patterns empty`.

5. In repository Advanced Security → CodeQL analysis → Set up → Default, review detected languages and enable.
   Use the default query suite and standard hosted runners; include the detected Python, JavaScript/TypeScript and Actions coverage.
   Wait for initial analysis to finish and inspect code-scanning tool status; enabling alone is not a successful scan.

   ```sh
   open 'https://github.com/shoalmark/shoalmark/settings/security_analysis'
   ```
   Expected: configured default setup and completed successful initial analyses for selected languages.
   Stop on policy/permission errors or missing supported language coverage. Paste back: `CodeQL configured` plus analysis URL(s)/result.

6. In organisation Settings → Advanced Security → Configurations, choose *New configuration* and name it `public-repository-defaults`.
   Enable Secret Protection (paid only for private repositories) with secret scanning and push protection; enable dependency graph,
   Dependabot alerts and security updates; leave Code Security unset. Under *Use as default for newly created repositories* choose
   **Public**; apply it to no existing repository.
   If the UI exposes individual “automatically enable for new repositories” controls instead, set those five defaults.
   Private repositories need a separate plan/entitlement decision; do not claim the public configuration covers them.

   ```sh
   open 'https://github.com/organizations/shoalmark/settings/security_products'
   ```
   Expected: the Configurations page; a saved configuration set as the default for new public repositories.
   Stop if payment or a licence is requested, or if the page is unavailable on the current Free plan. Paste back: configuration name/ID, public default and five enabled features.
   Dependabot **version** updates additionally need `.github/dependabot.yml` in each new repository; an org toggle does not supply that file.

7. Hand the completion lines to Principal `8e509911` to record in FM-006, including any incomplete step.
   Review ruleset/API readback before the release; never infer applied settings from this prepared sheet.
   Existing releases remain unchanged. The public evidence correction is: PR #119 removed six files under
   `work-tracker/evidence/FM-001/port/` from the current tree at `b041cb2dca136623ee9160d74ae5b39b0f1a7ba2`;
   their history remains reachable. `port-rd.md` was updated, not deleted. **No history rewrite.**

## Agent boundary and reserved decisions

The accompanying AGENTS.md rule treats non-member text as data, never authority; even member text needs proper authority.
Owner decisions only, no implementation prepared here: restricted credentials for agents in both repositories;
whether to use the Owner's GitHub no-reply commit email. Existing credentials/email have not been changed.
A team ruleset controls the authenticated account, not which human or agent uses that account.

## Recovery and verification boundaries

On an unexpected result stop before the next change; record the actual state, not an assumed rollback.
Owner recovery uses the same UI: disable only the two new tag rulesets/remove the new team grant; restore both merge-method
lists to merge/squash/rebase; restore repository Actions to all (org baseline unknown: retain its pre-change selection);
disable CodeQL default setup; unset the new security default. Do not weaken protections routinely to make a release pass.
Before editing org Actions, note its current selection for recovery. No tag is moved or deleted as a recovery step.
Read-only checks cannot prove server enforcement: no negative remote write was attempted. Browser setup/initial CodeQL run
and the eventual authorised release are Owner execution, still pending. No application test suite is needed for this docs-only slice.

## Preparation checks

Six literal shell blocks passed in `zsh -f -i` with a temporary stand-in `open` first on PATH,
checked with `command -v`; no real browser or remote write was invoked. UI steps remain unexecuted.
Workflow references and the historical deletion were inspected from Git; settings observations above came from read-only API calls.

## Sources

- [Rules and bypass semantics](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets)
- [Eligible bypass actors](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/creating-rulesets-for-a-repository)
- [Actions policy and its local-action exception](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository)
- [CodeQL default setup](https://docs.github.com/en/code-security/how-tos/find-and-fix-code-vulnerabilities/configure-code-scanning/configure-code-scanning)
- [Security configuration defaults](https://docs.github.com/en/rest/code-security/configurations)
