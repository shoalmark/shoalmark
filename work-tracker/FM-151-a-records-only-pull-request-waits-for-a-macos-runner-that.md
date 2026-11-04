---
id: FM-151
status: Proposed
considered: FM-003, FM-032, FM-134, FM-143
tags: process
epic: FM-139
next: build
hook: "A pull request that changes records only still starts all five required jobs on their own images, though four of them only skip their steps. On 4 November the macOS job of two such runs waited about ten minutes for a runner, then ran under 20 seconds."
ask-id: FM-151-Q1
ask: "Does macOS stay a required check for pull requests that change code?"
ask-kind: ruling
ask-since: 2026-11-04
ask-options: "yes, keep it required | required only before a release"
ask-proposal: "yes, keep it required"
answer: "accepted - yes, keep it required"
answered: 2026-11-04
answered-by: holgo99
---

# FM-151 — a records-only pull request waits for a macOS runner that runs no test

## What is true now

**2026-11-04 — filed, Proposed, on the Auditor's brief; nothing is built.** Its one ask, FM-151-Q1, is decision 4.

1. **Main requires five checks,** as its ruleset gives them: suites (ubuntu, 3.9), suites (ubuntu, 3.12),
   suites (macos, 3.12), suites (windows, 3.9) and suites (windows, 3.12).
2. **ci.yml decides the tier inside each job.**
   - One job, `suites`, runs five matrix entries, each on its pinned image
     ([ci.yml L13–L27](https://github.com/shoalmark/shoalmark/blob/c43af896efaeefea1dde4fa790d4db269ae86410/.github/workflows/ci.yml#L13-L27)).
   - Its second step decides "records only, or the full suites"
     ([L32–L96](https://github.com/shoalmark/shoalmark/blob/c43af896efaeefea1dde4fa790d4db269ae86410/.github/workflows/ci.yml#L32-L96)).
     That follows FM-032's ruling of 9 October: a records-only change runs `--check` inside the five required check
     names
     ([FM-032 L82](https://github.com/shoalmark/shoalmark/blob/c43af896efaeefea1dde4fa790d4db269ae86410/work-tracker/FM-032-the-loop-costs-the-same-for-a-docs-row-as-for-a-migration.md#L82)).
   - On a records-only pull request, `--check` runs in suites (ubuntu, 3.9) alone
     ([L100–L111](https://github.com/shoalmark/shoalmark/blob/c43af896efaeefea1dde4fa790d4db269ae86410/.github/workflows/ci.yml#L100-L111)).
     The other four write that they did not validate records
     ([L112–L116](https://github.com/shoalmark/shoalmark/blob/c43af896efaeefea1dde4fa790d4db269ae86410/.github/workflows/ci.yml#L112-L116))
     and skip the gate, Subversion and the suites; they still set up Python and set the git identity
     ([L97–L98](https://github.com/shoalmark/shoalmark/blob/c43af896efaeefea1dde4fa790d4db269ae86410/.github/workflows/ci.yml#L97-L98),
     [L135–L136](https://github.com/shoalmark/shoalmark/blob/c43af896efaeefea1dde4fa790d4db269ae86410/.github/workflows/ci.yml#L135-L136)).
   - So a records-only pull request still starts all five runners, each on its own image.
3. **What that cost on 4 November,** read from the API once each job had completed, in UTC:

   | Run | Pull request | Ubuntu and Windows jobs | suites (macos, 3.12): created, started, done |
   |---|---|---|---|
   | [41873037920](https://github.com/shoalmark/shoalmark/actions/runs/41873037920) | #262 at `2713530` | started 16:59:29, all done by 17:00:52 | 16:59:27, 17:09:40, 17:09:58 |
   | [41872939018](https://github.com/shoalmark/shoalmark/actions/runs/41872939018) | #261 at `a54b561` | started by 16:58:53, all done by 16:59:57 | 16:58:51, 17:08:54, 17:09:11 |
   | [41877258174](https://github.com/shoalmark/shoalmark/actions/runs/41877258174) | #261 at `308739f` | started by 17:24:17, done by 17:25:22; Windows 3.12 re-run, 17:49:00 to 17:49:18 | 17:24:15, 17:29:18, 17:29:37 |

4. **shoalmark/skills has the same five-check shape,** `tests (…)`.
   - On 4 November, shoalmark/skills#3's macOS job was cancelled for want of a hosted runner. Its re-run waited from
     17:16:53 to 17:26:57, then ran 15 seconds
     ([run 41873094451](https://github.com/shoalmark/skills/actions/runs/41873094451)).
   - That repository needs none of this change. It has no records tier, and every job runs both its suites
     ([its ci.yml L10–L36](https://github.com/shoalmark/skills/blob/06784be51991cd4d6accc20bb3cdfd5cdd577476/.github/workflows/ci.yml#L10-L36)).

## Why

FM-032 made a records-only change cheap: `--check` in place of the suites. But its required checks end only when the
slowest runner is found, and the macOS runner, the scarce one, then runs no test. On 4 November, three records-only
runs each waited five to ten minutes for macOS, for under 20 seconds of work. On shoalmark/skills, a code pull
request's macOS job was cancelled for want of a runner and had to be re-run by hand. That is decision 4's question.

## Decisions, for the Owner

FM-151-Q1 asks decision 4 alone. Decisions 1 to 3 are proposed with it.

1. **A tier job runs first.**
   - It computes the same records-or-full decision, the tier step's logic moved unchanged, and gives it as its output.
   - The five required jobs keep their names.
   - For a records-only pull request, each of them runs on an Ubuntu runner, its `runs-on` taken from the tier job's
     output. For any other pull request, and in any doubt, each runs on its own image, as now.
   - If the tier job fails, the five checks do not pass.
   - The build starts from a main that already carries
     [FM-143](FM-143-installing-two-skills-clones-all-of-shoalmark.md)'s decision 4, which removes the plugin's steps
     from the same file.
2. **The pins follow the new text.**
   - Today the suite's checks of ci.yml
     ([`test_shoalmark.py` L20800–L20915](https://github.com/shoalmark/shoalmark/blob/c43af896efaeefea1dde4fa790d4db269ae86410/test_shoalmark.py#L20800-L20915))
     hold one job, `suites`
     ([L20829–L20833](https://github.com/shoalmark/shoalmark/blob/c43af896efaeefea1dde4fa790d4db269ae86410/test_shoalmark.py#L20829-L20833)).
   - They follow the new text, and every pin keeps its force.
   - A mutant that classes a non-records path as records still fails.
3. **Allocation:** v0.20.3, under current path 5, "reliable and simpler first"
   ([TRIAGE.md L22](https://github.com/shoalmark/shoalmark/blob/c43af896efaeefea1dde4fa790d4db269ae86410/work-tracker/TRIAGE.md#L22)).
4. **FM-151-Q1: does macOS stay a required check for pull requests that change code?**
   - **The proposal, "yes, keep it required":** the suites hold macOS's own behaviour. Paths compare without regard to
     case there
     ([ci.yml L38](https://github.com/shoalmark/shoalmark/blob/c43af896efaeefea1dde4fa790d4db269ae86410/.github/workflows/ci.yml#L38)),
     and Subversion comes from Homebrew
     ([L121–L124](https://github.com/shoalmark/shoalmark/blob/c43af896efaeefea1dde4fa790d4db269ae86410/.github/workflows/ci.yml#L121-L124)).
   - **The other option, "required only before a release":** a code pull request could then merge without macOS.
     macOS would first run on the release's tag
     ([L7](https://github.com/shoalmark/shoalmark/blob/c43af896efaeefea1dde4fa790d4db269ae86410/.github/workflows/ci.yml#L7)).

**The build's review:** critical, since it changes CI and the boundary that decides which pull requests skip the
suites.

## Done when

Each item names its commit, pull request or run when it lands.

- [x] **The Owner has answered FM-151-Q1.** · `84be8aa`, #265 (`c9d5889`)
- [ ] **A records-only pull request's five required checks pass with no macOS or Windows runner,** measured on the
  first one after the change.
- [ ] **A code pull request still runs all five on their own images.**
- [ ] **The pins hold,** and the mutant that classes a non-records path as records fails.

## Ship log

| Date | Event |
|---|---|
| 2026-11-04 | Filed, Proposed, with one ruling ask, FM-151-Q1, on the Auditor's brief. Nothing is built. |
| 2026-11-04 | The standard review's P3 RV-4368 fixed forward: item 2 names the steps the four other jobs still run. Records only. |
| 2026-11-04 | Done when: the Owner's answer to FM-151-Q1 (#265). Records only. |
| 2026-11-04 | `epic: FM-139`: under v0.20.3's epic until the Owner decides whether it goes in. Records only. |
