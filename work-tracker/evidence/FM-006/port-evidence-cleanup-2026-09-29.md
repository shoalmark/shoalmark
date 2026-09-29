# FM-006 — remove archived port artifacts from the current tree

Principal session `01a0ec25`, 2026-09-29. Base: `80d0811974a1d39b679cfd374c80109ddd62acce` (merged PR 117).

The Owner instructed this cleanup before recording his publication act. The six artifacts are
obsolete migration evidence, not the active deriver or synthetic core suite. The accepted option
retains the parent’s public historical traces; this is a normal deletion commit, not history erasure.
The repository was already public: this change cannot establish deletion before publication.
The Owner’s explanation and client approval are recorded in FM-006, explicitly as his chat statement.

## Exact scope

The six removed files, with their preserved blob IDs and sizes at the base:

```text
100644 blob dea1b0038630b02b2277e9e23a55cc07e4251235    7678	work-tracker/evidence/FM-001/port/build-test-core-from-the-origin.py
100644 blob 5af1cf12f0098cfccfeaa40d7f28e4599ff3b20d   10199	work-tracker/evidence/FM-001/port/derive.py
100644 blob 1c47138e2e2df1f4711560a1dc02449cf7a7b7ba    1403	work-tracker/evidence/FM-001/port/run-origin-checks-statementwise.py
100644 blob aa7cc9f1687beab0f275324898fa04195593c7f4     479	work-tracker/evidence/FM-001/port/shoalmark.toml
100644 blob dd4c3145fcc4fac6939546102b9d5f82485e030b     566	work-tracker/evidence/FM-001/port/theme.css
100644 blob 6fbc5e89b240f7e23fb728bfcd65fcb95aece5b6     730	work-tracker/evidence/FM-001/port/wrapper.gen-tracker-index.py

```

FM-001’s historical builder and directory links and the exploration report’s directory link now
resolve to the immutable base commit. Dated review statements remain historical statements.
No active tool, tests, dependencies, hooks, workflow, signing policy or version changes.

## Verification and handoff

- The staged deletion manifest must match exactly the six files above; the directory is absent.
- A scoped dependency search across the tool, both suites, scripts and workflows found no references
  to this port directory or its two named helper scripts. References in historical evidence remain.
- Pinned Zensical 0.0.66 clean build, llms generation and the site validator pass.
- Historical link targets are checked directly against the preserved base tree.
- Commit hooks run the focused core suite and tracker gates; final branch --check follows the commit.
- Review and required PR CI remain pending. The Owner opens and merges the PR, then records the act
  after the other publication prerequisites and live deployment have been verified. No release tag due.
