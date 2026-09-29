# FM-006 — independent repository-migration review

Date: 2026-09-29.
Reviewed: `3fe27f3555c2063e37f8eb03bda49ad8197f80c4`.
Base: fetched `origin/main`, `1c344ed89ca1c0e1dd714c8beb737f92fc2983c4`.
Branch reviewed: `fm/006-repository-migration`, PR 117.
Reviewer: `reviewer@seat`.
Session: `01a0ed68` (harness `01a0ed68-914e-7b02-ae6a-dfde6a1cc474`).
Review branch: `fm/006-review-migration-3fe27f3`.
Worktree: `/private/tmp/shoalmark-review-fm006-3fe27f3`.

**Tier: code, critical.** `git diff --name-only origin/main...HEAD` includes
`shoalmark.py`, `test_shoalmark.py`, `lefthook.yml`, both CI workflows, dependency
configuration, a site-check script and `AGENTS.md` rules. The docs-only review
exception does not apply.

**Verdict: NOT READY — R1 must be fixed and verified on the resulting head.**

This is an independent session, not a child of the implementation session
`01a0ec25`. The prior Reviewer was `01a0ec25/reviewer-2`; that preparatory pass is
not counted as independent. The preserved Owner commit `d1a269b` has no Session
trailer; no identity or trailer was fabricated for that commit.

## R1 — P2: the rendered contract publishes four dead source-document links

Location: `zensical.toml:57–58`; coverage gap at `scripts/check_site.py:27`.
Confidence: high; reproduced from the pinned clean build.

Enabling README inclusion makes its relative links resolve below
`/shoalmark/agents/`. Zensical emits these four destinations in
`site/agents/index.html`, but none is present in the generated site:

| Contract link | Generated href | Missing published destination |
|---|---|---|
| Repository review/house rules, `AGENTS.md` | `AGENTS.html` | `/shoalmark/agents/AGENTS.html` |
| Apache license | `LICENSE-APACHE` | `/shoalmark/agents/LICENSE-APACHE` |
| MIT license | `LICENSE-MIT` | `/shoalmark/agents/LICENSE-MIT` |
| Notices | `NOTICE` | `/shoalmark/agents/NOTICE` |

These are README lines 496 and 500, now rendered by the new snippets extension.
A reader following the contract's own links to contribution rules or license
texts gets a missing page. The previous site exposed a literal include; these
links are newly exposed by the working inclusion. The other generated relative
HTML links resolve.

Reproduction:

```sh
uvx --from zensical==0.0.66 zensical build --clean
python3 scripts/llms_txt.py site
python3 scripts/check_site.py site
```

All three exit 0. Parse the anchors in `site/agents/index.html` and resolve the four
hrefs above against its parent directory: neither the files nor a directory
`index.html` exists. The checker validates the contract's title/include marker,
then checks link destinations only in the landing page and only for absolute
organization Pages URLs; it never checks these contract links.

Fix: keep the README as the single source, but give its repository-document links
valid organization-repository URLs or a site transformation with real published
destinations. Cover these contract destinations in the site validation.
Closure: rebuild with 0.0.66, verify all four destinations, and demonstrate that
breaking one is rejected before upload. Re-review the fix under the code tier.

## Independent checks

- Read FM-006, its migration validation, the preparatory review of `e0a21dd`,
  relevant earlier site review, `AGENTS.md`, `TRIAGE.md` and the complete changed
  file list. Inspected the implementation diff; the large landing wreck-data line
  differs only in its repository URL prefix.
- Confirmed the requested remote branch and PR 117 both name `3fe27f3`; the base
  is `1c344ed`. `d1a269b` is an unchanged ancestor, followed by the implementation
  and preparatory review commits. No version or tag change.
- `python3 shoalmark.py --check`: **exit 0** on the isolated tracker-named branch.
  INDEX is current (41 trackers); all three branch commits pass the judgement
  and Owner-section gates. This closes the detached-checkout limitation in the
  preparatory review without rewriting the Owner's commit.
- `python3 -u test_core.py`: **exit 0, 148 checks, no skips**, Python 3.14.3.
- `python3 -u test_shoalmark.py`: **exit 0, 508 passing checks, no failures**,
  Python 3.14.3. **39 checks skipped in 19 browser blocks** because Chrome could
  not start (exit -6); the suite explicitly says this is not a full pass.
- Pinned Zensical 0.0.66 clean build: **exit 0, no issues**. Markdown generation:
  **exit 0, 11 twins**. `check_site.py`: **exit 0**, with R1's limitation.
- Site negative controls in disposable copies: a literal contract include,
  missing German signing page and old personal-account public URL each cause
  the checker to fail.
- Extracted the exact syntax-hook command into a disposable git repository:
  invalid staged/valid worktree source refuses; valid staged/invalid worktree
  source passes; a source that raises at execution compiles without executing.
  A nested filename containing a space works. Actual Lefthook dispatch with the
  two Python commands confirms the nested glob, failure propagation, and one
  visible invocation of a core-suite probe. The real core suite ran separately.
- `lefthook dump` parses the configuration; session, trailer and commit-judgement
  hooks remain. CI retains both full suites and the same five OS/Python pairs,
  now unbuffered; non-draft opened/synchronize/reopened/ready events run them.
  The CI workflow token is explicitly `contents: read`.
- `git diff --check origin/main...HEAD`: **exit 0**.

## Live repository read-back and limits

Read-only GitHub API observations during this pass:

- Repository public at `shoalmark/shoalmark`; homepage and workflow-based Pages
  destination are `https://shoalmark.github.io/shoalmark/`.
- Ruleset 24177420 is active, with no bypass actors, PR required, deletion and
  force-push restrictions, and all five exact `suites (OS, Python)` contexts
  required from Actions app 15368. Pages jobs are not required PR checks.
- Default workflow permissions read; Actions cannot approve PRs; fork workflow
  approval policy `all_external_contributors`.
- Secret scanning, push protection, Dependabot security updates and private
  vulnerability reporting enabled.
- PR CI at the reviewed head: both Ubuntu jobs, macOS 3.12 and Windows 3.12
  succeeded; Windows 3.9 was still running in the last pre-commit observation
  (2026-09-29, approximately 16:00 CEST),
  [Actions run 36577464167](https://github.com/shoalmark/shoalmark/actions/runs/36577464167).
  This records the observed checks, not a five-job green result.

Browser coverage is limited: the local suite's Chrome control could not start
inside the sandbox (exit -6). A separate headless landing-page probe with a
disposable profile outside the sandbox timed out after 45 seconds; no successful
viewport measurement is claimed. Source inspection confirms the Docs link points
to `setup.html` and remains selected by the mobile navigation CSS.

No historical secret/privacy audit, publication-prerequisite completion or
deployment is certified. Earlier public-release obligations remain in FM-006;
this migration review does not clear its Owner act. The old active URL constants,
unfixed literal include and repeated full-suite commit hook were replaced in the
implementation; historical evidence remains intentionally unchanged. This pass
adds review evidence and the tracker handoff only.

Next: fix R1, obtain the code-tier verification pass and green required CI on the
resulting PR head. The Owner retains merge and deployment; this session does
neither and creates no tag.
