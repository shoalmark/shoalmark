# Work Tracker — Index

> **GENERATED — do not hand-edit.** Run `python3 shoalmark.py` after changing any tracker's front matter
> (or its `# title`). Rows are *pointers* — the detail lives in the tracker, never duplicated here.
>
> **Status** = code lifecycle; `Shipped` means merged, **not** a production claim.
>
> **Tier · Board · Triaged** = the triage picture — the same one the board (`index.html`) shows, from the
> same function: `progress` kept by a pass · `triage` owed a pass · `backlog` waiting · `ended` shipped or closed.
> One rule this file cannot show, because it has no clock: a judgement on work in progress older than 7 days
> counts as `triage` again.

## Triage — the current path, and what to work on next

> From [`TRIAGE.md`](TRIAGE.md) and each tracker's `rank:` — what the dashboard's board shows the Owner.
> Everything unranked follows below by status; a triage pass (`--triage`) re-judges open work weekly.
> *Kind* is the kind of problem that is left: plain where a seat judged it (`kind-of-problem:`), *italic* where the move already says it.

*The Owner's. A pass judges every tier against it; only the Owner changes it.*

1. v0.20.0 is a simple trust layer for the Owner and an effective workbench for the agents: Subversion without git, and the release archive. For v0.20.0, work that serves neither waits. A security fix for a released version does not wait: it ships as a patch release on the Owner's word (v0.19.4, 13 October).
2. A pull request merges on a verdict that names what it covers: the reviewed commit, its base, the tier and the checks run, as a Reviewed: line in the commit. The review commit carries the findings, their evidence and dispositions, its limits and who reviewed; a separate file only where the evidence needs one. Critical work takes a Reviewer in a session of its own, never one the building session started, and at most two rounds per finding. Critical means: a release, the gate or hooks, signing and rights, auth, migrations, deploy and secrets tooling, run sheets for the Owner, TRIAGE.md or AGENTS.md rules changed by a seat, and rules and code under a P1 or security tracker. Other code takes one inline Reviewer pass; records take one pass; neither runs re-check rounds: findings are fixed forward and named in the commit. Relevant local checks run before a pull request; the complete suites run in CI, not locally before every pull request. A review of the Owner's own answers and TRIAGE lines reports and never blocks. The Owner merges on a ready line, or over any other verdict with a signed reason.
3. v0.20 is one milestone: v0.20.0, v0.20.1 and v0.20.2, as FM-023 allocates them. It is announced publicly when its last target is done, not before. Then the trial runs, and what it finds is filed as trackers and comes first. Until its findings are in, nothing else on Subversion is built, and on Subversion the tool says once what it cannot verify — no signature, and without a server's login no author — and never claims it. The held rulings, the plain folder among them, are looked at again on 20 October.
4. A seat's question for the Owner goes on the board as an ask, with its proposal, and the seat keeps working; the Owner answers in one sitting. A seat interrupts the Owner only to stop harm.
5. The v0.20.x releases after v0.20.0 make shoalmark reliable and simpler first, then quick to use: the deletions of the 12 October rulings, each shipped with the quick win that takes its place where one exists, and B1's landing with Copy the prompt. Within a release, deleting comes before adding. A quick win is small, reads only and runs nothing for the Owner, works the same for every harness, says what each version control cannot give, and needs no research.
6. Research and complex work waits for v0.21.x, each piece starting from a research or design round the Owner allocates: check-ins and silent sessions, switching to a running session, the plain folder.

| # | Tier | Next | Kind | Needs | ID | Hook | Status |
|---|------|------|------|-------|----|------|--------|
| 1 | P1 | build | — | intended, kind | [FM-032](FM-032-the-loop-costs-the-same-for-a-docs-row-as-for-a-migration.md) | The loop — a session row, a Reviewer pass, fixes, re-verification, merges of main — costs the same for a docs row as fo… | In Progress |
| 2 | P1 | build | — | intended, kind | [FM-004](FM-004-nobody-knows-whether-another-project-s-agents-would.md) | A first outside Owner will hand ADOPT.de.md to his agents mid-way through a 60-package plan. My guess was 35 % yes if a… | In Progress |


## Work

| ID | Tier | Hook | Status | Board | Triaged |
|----|------|------|--------|-------|---------|
| [FM-076](FM-076-a-seat-s-work-that-only-another-seat-can-push-is-refused-or.md) | P1 | a seat's work that only another seat can push is refused, or recorded as that seat's own | In Progress | progress | 2026-10-27 |
| [FM-066](FM-066-the-board-s-reads-hold-their-fixed-settings-for-every.md) | P1 | the board's reads hold their fixed settings for every program a configuration can name | In Progress | progress | 2026-10-21 |
| [FM-063](FM-063-a-seat-s-commit-message-that-ends-in-bare-links-has-them.md) | P2 | a seat's commit message that ends in bare links has them rewritten by the trailer step | In Progress | progress | 2026-10-29 |
| [FM-062](FM-062-an-agent-drifts-off-track-where-a-rule-is-held-only-as-prose.md) | P2 | an agent drifts off track where a rule is held only as prose, two sources disagree, or obsolete text still reads as live | In Progress | progress | 2026-10-19 |
| [FM-061](FM-061-vendoring-still-takes-an-untagged-or-partial-source-a-weaker.md) | P2 | vendoring still takes an untagged or partial source, a weaker trusted pin than R17 allows | In Progress | progress | 2026-10-16 |
| [FM-059](FM-059-the-owner-answers-each-ask-in-a-view-of-its-own-and-a.md) | P2 | The Owner answers each ask in a Board view that holds only its dialog; a prepared run stops there, and signs and pushes… | In Progress | progress | 2026-10-27 |
| [FM-058](FM-058-a-command-a-person-runs-through-the-hooks-copy-is-stopped-at.md) | P1 | A command a person runs through the hooks' copy is stopped after the hook's 35 s, and an answer's PIN, touch and push c… | In Progress | progress | 2026-10-17 |
| [FM-057](FM-057-the-board-rebuilds-itself-after-every-checkout-and-never.md) | P2 | The board rebuilds itself after every checkout, merge and rebase, and never says what it read or when | In Progress | progress | 2026-10-15 |
| [FM-054](FM-054-the-board-and-the-terminal-say-signed-where-nothing-is.md) | P1 | The board's answer dialog and the terminal say signed on every repository, though --answer signs only where the owner l… | In Progress | progress | 2026-10-15 |
| [FM-053](FM-053-the-board-s-design-for-v0-20-1-is-the-owner-s-word.md) | P2 | The board's design for v0.20.1 is the Owner's word in a design sitting, and a Builder acts only on a signed word | In Progress | progress | 2026-10-15 |
| [FM-050](FM-050-an-ask-has-no-id-of-its-own-so-an-answer-cannot-name-the-ask.md) | P2 | An ask has no id of its own, so an answer, the stand-up and the receipts cannot name the ask they mean | In Progress | progress | 2026-10-27 |
| [FM-041](FM-041-the-board-places-a-ranked-proposed-tracker-in-the-backlog.md) | P3 | the board places a ranked Proposed tracker in the backlog while the progress caption promises rank order | In Progress | progress | 2026-09-30 |
| [FM-037](FM-037-a-seat-can-change-the-owner-s-intent-and-current-path-in.md) | P1 | a seat can change the Owner's intent and current path in TRIAGE.md, and the gate lets it through | In Progress | progress | 2026-09-25 |
| [FM-033](FM-033-work-is-built-on-trackers-no-pass-has-judged-and-the-board.md) | P2 | On 2026-09-24 the board showed the day's release work under triage and four idle trackers under progress: code for four… | In Progress | progress | 2026-10-13 |
| [FM-032](FM-032-the-loop-costs-the-same-for-a-docs-row-as-for-a-migration.md) | P1 | The loop — a session row, a Reviewer pass, fixes, re-verification, merges of main — costs the same for a docs row as fo… | In Progress | progress | 2026-10-13 |
| [FM-031](FM-031-the-streams-run-in-parallel-and-only-the-owner-sees-the.md) | P2 | In fourteen hours 22 seat sessions, under 21 ids, opened 22 pull requests, and only the Owner sees the whole queue. By… | In Progress | progress | 2026-10-13 |
| [FM-030](FM-030-an-accepted-action-ask-leaves-the-person-s-list-before-the.md) | P2 | At the person's morning sitting, `--standup` printed 0 items and `--owner` printed NOTHING NEEDS THE OWNER, yet two act… | In Progress | progress | 2026-10-13 |
| [FM-024](FM-024-a-seat-s-commit-names-its-session-and-the-record-knows-the.md) | P2 | Two sessions of one seat are one author in git; a seat's commit must name its session, and the record must know what th… | In Progress | progress | 2026-10-15 |
| [FM-007](FM-007-a-signature-proves-the-key-not-the-hand-an-agent-running-as.md) | P1 | The gate accepts an answer only from a commit signed by the Owner's key. But a signature proves which key was used, not… | In Progress | progress | 2026-09-25 |
| [FM-006](FM-006-shoalmark-has-one-document-written-for-agents-the-humans-who.md) | P2 | One README, written for the agent that has to use the tool, is the whole documentation. The people who own the reposito… | In Progress | progress | 2026-10-13 |
| [FM-005](FM-005-the-human-is-asked-for-many-small-decisions-mid-flight-he.md) | P1 | Measured: 200 pull requests merged in 22 days, 85 % under a minute after opening, none reviewed — and in a rehearsal th… | In Progress | progress | 2026-10-13 |
| [FM-004](FM-004-nobody-knows-whether-another-project-s-agents-would.md) | P1 | A first outside Owner will hand ADOPT.de.md to his agents mid-way through a 60-package plan. My guess was 35 % yes if a… | In Progress | progress | 2026-10-13 |
| [FM-001](FM-001-the-repository-it-was-cut-from-still-runs-its-own-copy.md) | P3 | fathom-mark 0.1.0 was cut out of a larger repository's tracker generator on 2026-09-21 — and that repository still runs… | In Progress | progress | 2026-09-23 |
| [FM-042](FM-042-requirements-in-the-repository-tested-as-a-contract-a-layer-for.md) | P2 | Developer and tester work from one ground truth — requirements in the repository, tested as a contract, not by reading… | Parked | backlog | 2026-10-13 |
| [FM-039](FM-039-fm-035-s-healthy-board-case-fails-under-machine-load-a-5-s.md) | P2 | FM-035's healthy-board case fails under machine load: a 5 s wall-clock Chrome budget, 469/470 at load 9–27 | Parked | backlog | 2026-10-13 |
| [FM-029](FM-029-the-answer-says-accepted-when-the-person-picked-another.md) | P2 | The person picked the third of three options, not the proposal, and the signed record reads `accepted - <the third opti… | Parked | backlog | 2026-10-13 |
| [FM-028](FM-028-after-midnight-the-suite-refuses-every-commit-the-board-and.md) | P2 | Between midnight and two in the morning the pre-commit suite refused every commit; they went through only with TZ=UTC.… | Parked | backlog | 2026-10-13 |
| [FM-027](FM-027-the-next-free-id-is-claimed-on-the-server-not-guessed-on-a-branch.md) | P3 | `--new` takes the next id it can see on the branch it runs on; two branches that have not merged both get it — it happe… | Parked | backlog | 2026-09-28 |
| [FM-026](FM-026-an-existing-fleet-has-no-migration-path-the-adopt-note-must.md) | P3 | Three outside agent fleets asked cold said no, and all three named the same reason — two sources of truth — because not… | Parked | backlog | 2026-09-24 |
| [FM-025](FM-025-a-cold-start-reads-thirty-thousand-tokens-before-it-can-work.md) | P3 | A session that takes a seat cold reads about thirty thousand tokens of pages and trackers before it can do anything; th… | Parked | backlog | 2026-09-24 |
| [FM-023](FM-023-a-plan-names-its-seats-their-estimates-and-when-the-person.md) | P3 | A plan names its seats, their estimates and when the person is needed; it is updated as the work runs and recorded when… | Parked | backlog | 2026-09-24 |
| [FM-084](FM-084-queue-does-not-show-a-pull-request-s-ci-so-a-failing-check.md) | — | --queue does not show a pull request's CI, so a failing check is found on the forge by hand | Proposed | triage | — |
| [FM-083](FM-083-nothing-measures-how-well-a-skill-does-its-work-only-its.md) | — | nothing measures how well a skill does its work, only its structure and its proof | Proposed | triage | — |
| [FM-082](FM-082-the-board-and-standup-do-not-list-an-ask-that-sits-on-a.md) | — | the Board and --standup do not list an ask that sits on a branch not on main | Proposed | triage | — |
| [FM-081](FM-081-a-tracker-names-no-release-in-its-front-matter-so-the.md) | — | a tracker names no release in its front matter, so the release commit cannot check what it holds | Proposed | triage | — |
| [FM-080](FM-080-the-docs-do-not-say-an-answer-needs-a-merge-commit-a-squash.md) | — | the docs do not say an answer needs a merge commit: a squash merge or a forge's web-editor commit breaks it | Proposed | triage | — |
| [FM-079](FM-079-check-does-not-say-when-the-session-rule-is-still-dormant.md) | — | --check does not say when the session rule is still dormant | Proposed | triage | — |
| [FM-078](FM-078-model-and-effort-have-no-harness-neutral-record.md) | — | model and effort have no harness-neutral record | Proposed | triage | — |
| [FM-077](FM-077-an-owner-signed-commit-that-carries-a-seat-s-session-line.md) | — | an Owner-signed commit that carries a seat's Session: line passes silently | Proposed | triage | — |
| [FM-075](FM-075-seven-source-binding-controls-fail-on-apple-s-python-3-9-6.md) | — | seven source-binding controls fail on Apple's Python 3.9.6, whose bytecode cache is redirected | Proposed | triage | — |
| [FM-074](FM-074-the-docs-do-not-name-two-subversion-limits-first-no-gate-on.md) | — | the docs do not name two Subversion limits first: no gate on the svn command line, and one shared account | Proposed | triage | — |
| [FM-073](FM-073-adopt-s-time-budget-leaves-out-the-time-spent-waiting-for.md) | — | ADOPT's time budget leaves out the time spent waiting for the person | Proposed | triage | — |
| [FM-072](FM-072-adopt-s-read-rule-for-an-extension-can-be-taken-to-skip-a.md) | — | ADOPT's read rule for an extension can be taken to skip a folder whose name ends that way | Proposed | triage | — |
| [FM-071](FM-071-blocked-by-owner-refuses-a-comma-in-its-reason.md) | — | blocked-by: Owner refuses a comma in its reason | Proposed | triage | — |
| [FM-065](FM-065-a-skill-calls-another-skill-external-ones-included-through-a.md) | — | a skill calls another skill, external ones included, through a contract that pins what it calls and checks what it gets… | Proposed | triage | — |
| [FM-064](FM-064-a-signed-answer-the-guided-run-pushes-is-out-of-the-board-s.md) | — | a signed answer the guided run pushes is out of the board's sight until its branch is merged | Proposed | triage | — |
| [FM-060](FM-060-the-answer-s-refusal-record-is-committed-unsigned-under-the.md) | — | --answer's refusal record is committed unsigned under the Owner's name, and R14 then refuses every branch that carries… | Proposed | triage | — |
| [FM-056](FM-056-the-gate-can-name-the-commit-that-removed-a-line-as-the-one.md) | — | The gate names who set a tracker's line with a pickaxe that also matches the commit that removed it, so a line a merge… | Proposed | triage | — |
| [FM-055](FM-055-the-receipts-need-the-owner-s-definitions-of-a-day-a-sitting.md) | — | The receipts count what the record holds, and they need the Owner's definitions of a day, a sitting and repositories co… | Proposed | triage | — |
| [FM-052](FM-052-a-fixture-that-watches-git-lets-git-s-own-housekeeping-run.md) | — | A fixture that watches .git lets git's own housekeeping run inside the watch, so a green commit can fail once | Proposed | triage | — |
| [FM-051](FM-051-dependency-updates-have-no-path-the-gate-refuses-every.md) | — | Dependency updates have no path: the gate refuses every Dependabot pull request, and the site's dependencies are first… | Proposed | triage | — |
| [FM-049](FM-049-b1-s-probe-dialog-gives-a-visitor-one-opt-in-line-to-say.md) | — | B1's probe dialog gives a visitor one opt-in line to say what their agent found | Proposed | triage | — |
| [FM-043](FM-043-the-upgrade-notes-leave-an-adopter-with-a-hook-runner-short.md) | — | the upgrade notes leave an adopter with a hook runner short of 0.19.0 | Proposed | triage | — |
| [FM-038](FM-038-the-pre-commit-hook-hides-the-suites-skip-lines-a-test-that.md) | P3 | the pre-commit hook hides the suites' skip lines: a test that skips by name is never seen at commit time | Proposed | backlog | 2026-09-27 |
| [FM-018](FM-018-the-answer-flow-must-be-convenient-and-fail-safe-for-a-normal.md) | P1 | Answering takes a normal user through branch switches, a checkout a seat's worktree may hold, an older pinned tool on t… | Proposed | backlog | 2026-09-23 |
| [FM-046](FM-046-a-committed-tracker-s-front-matter-is-parsed-only-for-lf.md) | P1 | A committed tracker's front matter is parsed only for LF line endings and not through one normalisation, so the same tr… | Shipped | ended | 2026-10-12 |
| [FM-045](FM-045-the-board-s-refresh-stops-on-git-ls-tree-which-its-read-only.md) | P0 | Where an answer waits on an answer branch and the signers file lies in the working tree, the board's refresh stops and… | Shipped | ended | 2026-10-08 |
| [FM-044](FM-044-shoalmark-stops-with-a-traceback-where-git-is-not-installed.md) | P1 | A Subversion team without git could not run the reviewed copy: every command but --session-check and --queue stopped wi… | Shipped | ended | 2026-10-13 |
| [FM-040](FM-040-the-hook-s-board-regeneration-takes-26-s-on-shoalmark-and-15.md) | P2 | the hook's board regeneration takes 26 s on shoalmark and 15 s on PortDive — every checkout and commit waits for it | Shipped | ended | 2026-09-28 |
| [FM-036](FM-036-a-worksheet-with-two-filled-rows-for-one-tracker-applies.md) | P2 | On 2026-09-25 the day's worksheet held two filled rows for FM-030 — the morning pass's `keep P1 #3 build` and the same-… | Shipped | ended | 2026-09-25 |
| [FM-035](FM-035-ci-is-red-on-the-v0-18-3-release-tag-two-suites-fail-on.md) | P2 | The tag v0.18.3 ran CI (actions run 36121290371, 2026-09-25 09:57–10:03 UTC): ubuntu 3.9 and 3.12 green; windows 3.9 an… | Shipped | ended | 2026-09-25 |
| [FM-034](FM-034-a-fresh-clone-s-check-says-the-index-is-stale-the-header.md) | P2 | A fresh clone without the Owner's allowedSignersFile runs --check and reads two findings where there is one: the missin… | Shipped | ended | 2026-09-25 |
| [FM-022](FM-022-a-person-finds-the-three-intent-lines-hard-to-start-no.md) | — | A person finds the three intent lines hard to start: there is no beginning, and no example. *for* reads as if something… | Shipped | ended | 2026-09-23 |
| [FM-021](FM-021-the-progress-section-is-empty-beside-work-in-progress-and.md) | — | The board says 13 trackers are in progress, and its progress section beside that reads 0. Nothing on the line says that… | Shipped | ended | 2026-09-23 |
| [FM-020](FM-020-searching-the-board-for-a-whole-id-shows-every-tracker-that.md) | — | The Owner typed one tracker's id into the board's search and got a long list back, not the one tracker he asked for. He… | Shipped | ended | 2026-09-23 |
| [FM-019](FM-019-a-merge-commit-is-judged-as-the-merger-s-own-change-and-main-s.md) | — | On a clean tree the rights gate judges HEAD against HEAD~1. For a merge commit that is everything the pull request carr… | Shipped | ended | — |
| [FM-017](FM-017-a-failed-answer-leaves-its-writes-behind-and-the-next-answer.md) | — | When the pre-commit gate refuses the commit, `--answer` returns and leaves everything it wrote: the tracker staged with… | Shipped | ended | — |
| [FM-015](FM-015-seats-silently-drops-a-signature-that-answerers-asked-for.md) | — | From 0.17.1 who may answer is read from `[seats]` alone wherever `[seats]` exists. A repository with `answerers = ['ali… | Shipped | ended | — |
| [FM-014](FM-014-the-seat-cannot-record-that-it-acted-on-an-answer-clearing.md) | — | `--clear-ask` moves an answered exchange into the body and removes `answer:` `answered:` `answered-by:` from the front… | Shipped | ended | — |
| [FM-013](FM-013-after-ok-the-answer-dialog-leaves-only-abort-and-says.md) | — | In the board's answer dialog, OK copies the command, prints one line of instruction above it and disables itself — the… | Shipped | ended | — |
| [FM-012](FM-012-a-load-spawns-git-once-per-tracker-and-answer-is-silent-for.md) | — | Reading the trackers spawns `git config user.name` once for every tracker that has no `answered-by:` — nearly all of th… | Shipped | ended | — |
| [FM-011](FM-011-vendoring-from-an-incomplete-source-copies-what-it-finds-and.md) | P1 | `vendor()` skips a source file that is not there — `if not src.exists(): continue` — so vendoring from an incomplete so… | Shipped | ended | 2026-09-23 |
| [FM-010](FM-010-the-answerers-deprecation-warning-never-reaches-the.md) | — | The note that tells a repository `answerers` is going away is guarded by `if ANSWERERS and SEATS:` — it fires only wher… | Shipped | ended | — |
| [FM-009](FM-009-version-has-drifted-from-version-and-vendor-suppresses-the.md) | — | `__version__` in `shoalmark.py` says 0.17.0; `VERSION` and the CHANGELOG say 0.17.2. Two tags shipped that way. `--vend… | Shipped | ended | — |
| [FM-008](FM-008-an-ask-reaches-the-owner-only-through-the-gate.md) | — | The ask/answer flow holds only while every agent has read AGENTS.md and chooses to obey it. Nothing in the tool refuses… | Shipped | ended | 2026-09-23 |
| [FM-003](FM-003-the-tool-is-proven-only-on-macos-with-git-a-first-outside.md) | — | Every proof so far is macOS, git, one Owner. The first outside user works on Windows, with Subversion and TortoiseSVN,… | Shipped | ended | — |
| [FM-002](FM-002-a-board-anyone-can-brand-the-person-the-repository-the.md) | P2 | The board can carry a name in the browser tab and a theme.css — nothing else: no name on the page, no logo, English onl… | Shipped | ended | 2026-09-27 |
| [FM-016](FM-016-an-answered-ask-still-shows-as-unanswered-on-the-branch-the.md) | — | After `--answer` the Owner switches back to his main branch, and that branch's board still shows the ask with accept an… | Closed | ended | 2026-09-23 |
