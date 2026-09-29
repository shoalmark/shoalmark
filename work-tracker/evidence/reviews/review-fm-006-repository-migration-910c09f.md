# FM-006 — independent migration re-review

Date: 2026-09-29.
Reviewed: `910c09fbdec55c067c501b54afe36d97c9ab3496`.
Base: `origin/main`, `1c344ed89ca1c0e1dd714c8beb737f92fc2983c4`.
Reviewer: `reviewer@seat`, session `01a0ed68`.
Review branch: `fm/006-review-migration-910c09f`.
Worktree: `/private/tmp/shoalmark-review-fm006-3fe27f3`.

**Tier: code, critical. Verdict: READY. R1 is closed; no open review findings.**

This is review clearance. The five required CI jobs on the final PR revision
must still pass before the Owner merges. This session performs no merge,
deployment, tag or repository-setting change.

## Range and independence

The remote migration branch and PR 117 both name `910c09f`. Git confirms that it
merges fix `4c638a8` and the original independent verdict `91ba9f6`, preserving
both commits. Compared with `4c638a8`, only FM-006's tracker and the original
review evidence change; the implementation is identical.

The whole range remains critical code under `git diff --name-only
origin/main...HEAD`: tool, tests, hooks, workflows, configuration and AGENTS rules.
The new implementation since the [first review](review-fm-006-repository-migration-3fe27f3.md)
changes README links and `scripts/check_site.py`, with changelog and tracker
evidence. I read the entire follow-up diff and the merge's tracker resolution.

Reviewer root `01a0ed68` differs from implementation root `01a0ec25`. The prior
independent verdict is a review commit, not implementation by this Reviewer.
Owner commit `d1a269b` is still unchanged in the ancestry.

## R1 verification

The README remains the single source of the contract. Its AGENTS.md,
LICENSE-APACHE, LICENSE-MIT and NOTICE anchors now point to
`https://github.com/shoalmark/shoalmark/blob/main/<file>`.

- Clean Zensical **0.0.66** build at `910c09f`: exit 0, no issues.
- `python3 scripts/llms_txt.py site`: exit 0, **11 Markdown twins**.
- Parsed the rendered contract: all four exact repository URLs are present.
  Each target exists in `origin/main`; independent GitHub Contents API reads
  confirm each is a file at that exact public URL.
- The fixed checker passes the clean and restored site on **Python 3.14.3 and
  3.9.6**. It now checks both the landing and contract pages, resolves relative
  links from the page's directory, and checks organization `blob/main` targets
  against the source checkout.
- In disposable copies, changed each of the four URLs separately to a missing
  target. **All eight runs fail** (four targets on each interpreter), naming
  `broken repository link in agents/index.html` and the missing target.
- Restored the original relative `AGENTS.html` destination in another negative
  control: **both interpreters refuse it** as a broken contract link.
- Regression control: the same missing LICENSE-MIT fixture is accepted by the
  checker from `3fe27f3` (exit 0) and rejected by the fixed checker (exit 1).

The reported defect and the gap in its validation are both closed. The old
relative source-document links and landing-only validation are obsolete and
replaced; no duplicate copy of the contract or its linked files was added.

## Gates and remaining boundaries

`python3 shoalmark.py --check` at the reviewed head: **exit 0** on the isolated
FM-006 branch. INDEX is current; the build-judgement and Owner-section gates pass.
`git diff --check origin/main...HEAD`: **exit 0**.

The first independent pass's core suite (148 checks), integration suite (508
passing, 39 browser checks skipped), hook probes and repository-settings reads
remain recorded in its preserved evidence. The follow-up changes no tool,
suite, hook, workflow or dependency pin; this pass runs the affected site build
and checker tests. It does not claim a new full-suite or browser run.

On **910c09f**, Ubuntu 3.12 had passed and the other four required CI jobs were
still running at the pre-commit observation:
[Actions run 36579870354](https://github.com/shoalmark/shoalmark/actions/runs/36579870354).
Results from `3fe27f3` or `4c638a8` are not substituted for that run. No historical
privacy/secret audit, publication-prerequisite completion or release readiness is
certified. FM-006's standing Owner act remains open.

Next: required CI green on the final PR revision, then the Owner's merge and
manual Pages deployment from updated main. No release tag is due for this slice.
