# Work Tracker — Index

> **GENERATED — do not hand-edit.** Run `python3 shoalmark.py` after changing any tracker's front matter
> (or its `# title`). Rows are *pointers* — the detail lives in the tracker, never duplicated here.
>
> **Status** = code lifecycle; `Shipped` means merged, **not** a production claim.
>
> **Tier · Board · Triaged** = the triage picture — the same one the board (`index.html`) shows, from the
> same function: `progress` kept by a pass · `triage` owed a pass · `backlog` waiting · `done`.
> One rule this file cannot show, because it has no clock: a judgement on work in progress older than 7 days
> counts as `triage` again.
>
> Generated 2026-09-23 · 25 trackers (25 work).

## Triage — the current path, and what to work on next

> From [`TRIAGE.md`](TRIAGE.md) and each tracker's `rank:` — what the dashboard's board shows the Owner.
> Everything unranked follows below by status; a triage pass (`--triage`) re-judges open work weekly.
> *Kind* is the kind of problem that is left: plain where a seat judged it (`kind-of-problem:`), *italic* where the move already says it.

*The Owner's. A pass judges every tier against it; only the Owner changes it.*

1. The daily sitting runs on a tagged release with a signed answer and no failed run.
2. What a sitting finds is filed that day and fixed when it is small and ready; the rest is tracked.
3. A pull request without an independent review's evidence file cannot merge - checked, not asked.
4. The owner shall be involved less when trust in the process has been built, but the trust must come from evidence and has to be earned first.

| # | Tier | Next | Kind | Needs | ID | Hook | Status |
|---|------|------|------|-------|----|------|--------|
| 1 | P1 | review | obvious | intended | [FM-011](FM-011-vendoring-from-an-incomplete-source-copies-what-it-finds-and.md) | `vendor()` skips a source file that is not there — `if not src.exists(): continue` — so vendoring from an incomplete so… | In Progress |
| 2 | P2 | owner | *complicated* | intended | [FM-007](FM-007-a-signature-proves-the-key-not-the-hand-an-agent-running-as.md) | The gate accepts an answer only from a commit signed by the Owner's key. But a signature proves which key was used, not… | Proposed |
| 3 | P1 | wait | *complex* | intended | [FM-018](FM-018-the-answer-flow-must-be-convenient-and-fail-safe-for-a-normal.md) | Answering takes a normal user through branch switches, a checkout a seat's worktree may hold, an older pinned tool on t… | Proposed |
| 4 | P1 | wait | *complex* | intended | [FM-005](FM-005-the-human-is-asked-for-many-small-decisions-mid-flight-he.md) | Measured: 200 pull requests merged in 22 days, 85 % under a minute after opening, none reviewed — and in a rehearsal th… | In Progress |
| 5 | P2 | build | — | intended, kind | [FM-006](FM-006-shoalmark-has-one-document-written-for-agents-the-humans-who.md) | One README, written for the agent that has to use the tool, is the whole documentation. The people who own the reposito… | In Progress |


## Work

| ID | Tier | Hook | Status | Board | Triaged |
|----|------|------|--------|-------|---------|
| [FM-024](FM-024-a-seat-s-commit-names-its-session-and-the-record-knows-the.md) | — | Two sessions of one seat are one author in git; a seat's commit must name its session, and the record must know what th… | In Progress | triage | — |
| [FM-011](FM-011-vendoring-from-an-incomplete-source-copies-what-it-finds-and.md) | P1 | `vendor()` skips a source file that is not there — `if not src.exists(): continue` — so vendoring from an incomplete so… | In Progress | progress | 2026-09-23 |
| [FM-006](FM-006-shoalmark-has-one-document-written-for-agents-the-humans-who.md) | P2 | One README, written for the agent that has to use the tool, is the whole documentation. The people who own the reposito… | In Progress | progress | 2026-09-23 |
| [FM-005](FM-005-the-human-is-asked-for-many-small-decisions-mid-flight-he.md) | P1 | Measured: 200 pull requests merged in 22 days, 85 % under a minute after opening, none reviewed — and in a rehearsal th… | In Progress | progress | 2026-09-23 |
| [FM-004](FM-004-nobody-knows-whether-another-project-s-agents-would.md) | P3 | A first outside Owner will hand ADOPT.de.md to his agents mid-way through a 60-package plan. My guess was 35 % yes if a… | In Progress | progress | 2026-09-23 |
| [FM-001](FM-001-the-repository-it-was-cut-from-still-runs-its-own-copy.md) | P3 | fathom-mark 0.1.0 was cut out of a larger repository's tracker generator on 2026-09-21 — and that repository still runs… | In Progress | progress | 2026-09-23 |
| [FM-025](FM-025-a-cold-start-reads-thirty-thousand-tokens-before-it-can-work.md) | — | A session that takes a seat cold reads about thirty thousand tokens of pages and trackers before it can do anything; th… | Proposed | triage | — |
| [FM-023](FM-023-a-plan-names-its-seats-their-estimates-and-when-the-person.md) | — | A plan names its seats, their estimates and when the person is needed; it is updated as the work runs and recorded when… | Proposed | triage | — |
| [FM-018](FM-018-the-answer-flow-must-be-convenient-and-fail-safe-for-a-normal.md) | P1 | Answering takes a normal user through branch switches, a checkout a seat's worktree may hold, an older pinned tool on t… | Proposed | backlog | 2026-09-23 |
| [FM-007](FM-007-a-signature-proves-the-key-not-the-hand-an-agent-running-as.md) | P2 | The gate accepts an answer only from a commit signed by the Owner's key. But a signature proves which key was used, not… | Proposed | backlog | 2026-09-23 |
| [FM-022](FM-022-a-person-finds-the-three-intent-lines-hard-to-start-no.md) | — | A person finds the three intent lines hard to start: there is no beginning, and no example. *for* reads as if something… | Shipped | done | 2026-09-23 |
| [FM-021](FM-021-the-progress-section-is-empty-beside-work-in-progress-and.md) | — | The board says 13 trackers are in progress, and its progress section beside that reads 0. Nothing on the line says that… | Shipped | done | 2026-09-23 |
| [FM-020](FM-020-searching-the-board-for-a-whole-id-shows-every-tracker-that.md) | — | The Owner typed one tracker's id into the board's search and got a long list back, not the one tracker he asked for. He… | Shipped | done | 2026-09-23 |
| [FM-019](FM-019-a-merge-commit-is-judged-as-the-merger-s-own-change-and-main-s.md) | — | On a clean tree the rights gate judges HEAD against HEAD~1. For a merge commit that is everything the pull request carr… | Shipped | done | — |
| [FM-017](FM-017-a-failed-answer-leaves-its-writes-behind-and-the-next-answer.md) | — | When the pre-commit gate refuses the commit, `--answer` returns and leaves everything it wrote: the tracker staged with… | Shipped | done | — |
| [FM-015](FM-015-seats-silently-drops-a-signature-that-answerers-asked-for.md) | — | From 0.17.1 who may answer is read from `[seats]` alone wherever `[seats]` exists. A repository with `answerers = ['ali… | Shipped | done | — |
| [FM-014](FM-014-the-seat-cannot-record-that-it-acted-on-an-answer-clearing.md) | — | `--clear-ask` moves an answered exchange into the body and removes `answer:` `answered:` `answered-by:` from the front… | Shipped | done | — |
| [FM-013](FM-013-after-ok-the-answer-dialog-leaves-only-abort-and-says.md) | — | In the board's answer dialog, OK copies the command, prints one line of instruction above it and disables itself — the… | Shipped | done | — |
| [FM-012](FM-012-a-load-spawns-git-once-per-tracker-and-answer-is-silent-for.md) | — | Reading the trackers spawns `git config user.name` once for every tracker that has no `answered-by:` — nearly all of th… | Shipped | done | — |
| [FM-010](FM-010-the-answerers-deprecation-warning-never-reaches-the.md) | — | The note that tells a repository `answerers` is going away is guarded by `if ANSWERERS and SEATS:` — it fires only wher… | Shipped | done | — |
| [FM-009](FM-009-version-has-drifted-from-version-and-vendor-suppresses-the.md) | — | `__version__` in `shoalmark.py` says 0.17.0; `VERSION` and the CHANGELOG say 0.17.2. Two tags shipped that way. `--vend… | Shipped | done | — |
| [FM-008](FM-008-an-ask-reaches-the-owner-only-through-the-gate.md) | — | The ask/answer flow holds only while every agent has read AGENTS.md and chooses to obey it. Nothing in the tool refuses… | Shipped | done | 2026-09-23 |
| [FM-003](FM-003-the-tool-is-proven-only-on-macos-with-git-a-first-outside.md) | — | Every proof so far is macOS, git, one Owner. The first outside user works on Windows, with Subversion and TortoiseSVN,… | Shipped | done | — |
| [FM-002](FM-002-a-board-anyone-can-brand-the-person-the-repository-the.md) | — | The board can carry a name in the browser tab and a theme.css — nothing else: no name on the page, no logo, English onl… | Shipped | done | — |
| [FM-016](FM-016-an-answered-ask-still-shows-as-unanswered-on-the-branch-the.md) | — | After `--answer` the Owner switches back to his main branch, and that branch's board still shows the ask with accept an… | Closed | done | 2026-09-23 |
