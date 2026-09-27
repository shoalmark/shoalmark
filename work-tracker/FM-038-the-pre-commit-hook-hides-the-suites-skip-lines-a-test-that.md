---
id: FM-038
status: Proposed
considered: FM-035, FM-028, FM-017
tags: bug
triaged: 2026-09-27
next: build
tier: P3
hook: "the pre-commit hook hides the suites' skip lines: a test that skips by name is never seen at commit time"
---

# FM-038 — the pre-commit hook hides the suites' skip lines: a test that skips by name is never seen at commit time

## What is true now

**Filed 2026-09-26 by the Principal seat, under the freeze as a bug, on two findings of the day; nothing is built.** (1) FM-035's review R3, carried in the 0.18.4 CHANGELOG as *open, for the release after* and, since the same-day pass of 2026-09-26, as a line on FM-035 (Shipped): the pre-commit hook runs the suites with their output sent to `/dev/null`, so a check that skips by name — FM-035's own rule for a check that cannot run on a platform — is never seen at commit time; only CI on the tag shows it. (2) The Owner's cold Reviewer session on the 0.18.4 cut (`evidence/reviews/review-0.18.4-cut-df48d67.md`, its line 3): the hook runs the suites only when a `.py` file is staged, so a docs-only commit — a release cut among them — never runs them, and a check that reads a page (the setup pages' clone tag against `VERSION`, added at `3fe7e3a`) first fails at the Reviewer's run or in CI. Both are the hook's, `lefthook.yml`; the tool is not changed by them. Held against FM-035 (the checks that skip by name), FM-028 (the suite refused after midnight — the same hook, another cause) and FM-017 (the pre-commit gate's refusal leaving writes behind): none holds this.

## Why

A check that skips silently is a check that did not run. FM-035 made the suites say so by name; the hook throws the words away. And a cut that changes no `.py` ships without the suites having run at commit time, which is the moment the seat reads.

## Done when

The pre-commit hook prints the suites' summary lines at commit time — the counts, and every skip with its name — and runs both suites on every commit, or prints one line saying it did not and why; a suite case fails when a skip is silent under the hook's own invocation; a docs-only commit shows the suites ran. Judged by a pass before its first build commit (FM-033).

## Ship log

| Date | Event |
|---|---|
| 2026-09-26 | Filed by the Principal seat under the freeze as a bug, on FM-035's review R3 (carried since the 0.18.4 CHANGELOG, homed on a Shipped tracker by the same-day pass — the pass's Reviewer R4) and the cold session's line 3 on the 0.18.4 cut; the two facts, the why and the Done-when above. Nothing built. |
