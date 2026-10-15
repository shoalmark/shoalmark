---
id: FM-051
status: Proposed
considered: FM-019, FM-032, FM-031, FM-009, FM-011
tags: process
next: wait
hook: "Dependency updates have no path: the gate refuses every Dependabot pull request, and the site's dependencies are first built at a release tag"
---

# FM-051 — dependency updates have no path: the gate refuses every Dependabot pull request

## What is true now

**Filed 2026-10-15 as the standing home of dependency updates; nothing is built.** Dependabot's commit prefix will
name this tracker, so it stays open while updates come. The fix below is its first slice. Until it lands, each release
runs `docs.yml` by hand on its candidate before the tag.

**Facts,** read at main `70fe288`.
- #175 (Dependabot, zensical 0.0.67 → 0.0.69, `ec49825`) failed all five suites at the gate, run `38614154565`:
  `refused: commit ec49825 "Bump zensical from 0.0.67 to 0.0.69" changes requirements-docs.txt outside work-tracker/ —
  names no tracker: no FM-N in its subject`.
- `.github/dependabot.yml` sets no `commit-message` prefix for pip or for github-actions, so every such update is
  refused the same way.
- `ci.yml` never installs `requirements-docs.txt`. `docs.yml` installs it only on a `v*` tag or a manual run, so a site
  dependency is first built at a release tag.
- The site pins `zensical==0.0.67` (`requirements-docs.txt:2`). The suite's fixture builds with `zensical@0.0.65`
  (`test_shoalmark.py:13235`, used at `:13374`).

**Fix, as the Auditor proposes:**
- a standing upkeep tracker, named in `dependabot.yml`'s `commit-message` prefix for both ecosystems, so the gate
  accepts an update;
- a docs build in pull-request CI that runs only when `requirements-docs.txt` changes;
- one zensical pin, which the suite reads from `requirements-docs.txt`.

**Test for the class:**
- every package pinned anywhere in the repository (the requirements files, the suite and the workflows) has one
  version, and two pins of one package fail the test;
- `dependabot.yml`'s prefix names an existing open tracker, for every ecosystem it lists;
- a change to any file a published build installs from triggers that build in pull-request CI. `ci.yml` is read, and a
  mutant that drops the path fails.

**Tier:** critical. It adds a job to `ci.yml` and changes `dependabot.yml`, by the same rule as defect 3.

## Done when

`dependabot.yml`'s prefix names FM-051 for both ecosystems, a pull request that changes `requirements-docs.txt` builds
the site, the suite reads its one zensical pin from `requirements-docs.txt`, and the class test is in CI. The tracker
then stays open, and each update is a ship-log row.

## Ship log

| Date | Event |
|---|---|
| 2026-10-15 | Filed. |
