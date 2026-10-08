From: unavailable — `--whoami` reports no `seat.session`; no session identity was invented or configured.

# FM-045: v0.19.2, independent scoped re-check at 6b228b5

This pass ran in a session the Owner started, independent of the Planner's session.

Verdict: **NOT READY**.

Reviewed: 6b228b5250cce258de91791b847c87b4af1145b3. Scope: `git diff 9a7ed43 6b228b5` and `git log 9a7ed43..6b228b5`, following the brief's re-check section. Tier: critical. The diff changes tests, CHANGELOG, the landing and FM-045; it takes the code review loop. `git diff --name-only origin/main...HEAD` also includes code and configuration (Git reported multiple merge bases); that wider listing determines the review tier, not this re-check's scope.

## What holds

- The authorized detached checkout and `rev-parse HEAD` agree on the full reviewed SHA. The product file is byte-for-byte unchanged from 9a7ed43: SHA-256 `5dfcbff1115b4aef67ddd4e280451dc17217d0ccd5b7403289082199c6660d2f`. Both ADOPT pins still match; VERSION and both setup pages name 0.19.2.
- The stock classification block passes on the unchanged product: 29 commands, fourteen classified as never started by the board, including `ls-remote`; its twelve original and nineteen added injected controls pass.
- RV-2781 is fixed for the measured events. In the independent repeat, `--answer` records 51 Git starts across two board hooks, switch 32, merge 33, and rebase 64 across two hooks: 180 starts across six board runs. Six `ls-tree` starts independently located inside those board-hook intervals all appear in `_BOARD_GIT`. The preceding manual refresh separately records nineteen starts. The suite's controls reject an otherwise successful switch when its recorded starts are emptied, and show no recorded starts when tracing is disabled.
- The scoped run executes sixteen actual suite blocks in source order: 57 checks pass, zero fail, zero skip. Its runtime half sees 1,966 starts across five in-process runs, six program runs and 65 traced runs; the injected `ls-tree`-as-never-started and `env git log` controls are detected.
- All eight Git matrix shapes and Subversion run: in-tree signers with signed answers, local/remote answer branches, linked worktrees, moved tracker folder, origin/HEAD set and unset, 304 trackers, the foreign runner, and SVN update/switch followed by refresh. The matrix contributes 49 checks: 44 positive checks, three removed-hook controls and two recording controls. Real operations fire installed hooks in disposable synthetic repositories; the checks assert the refreshed content, exits and absence of stopped/traceback output. No matrix skip occurred. This is local evidence, not a claim that remote CI or every operating system was run in this session.
- The actual `ls-tree` argv forms pass the allowlist check and the bent `--output`/foreign `-c` forms fail. FM-045's original shape passes all four current-tool variants; the negative control uses v0.19.1 and is recorded below.
- RV-2782 is fixed: the visible landing label and tag link name v0.19.2, and its footer version/date match VERSION and the CHANGELOG's 10 October 2026 heading. The upgrade commands remain present. The independent HTML check fails on the stale label/link/date at 9a7ed43 and passes all four checks at this head. The date move is allowed by the brief.
- The changed release and tracker wording narrows claims to the implemented allowlist repair and the measured recording paths. Compilation, the 158-check core suite and the repository gate pass. No requirement line, product source, tracker or shared hook was edited by this review.

## Findings

- **RV-2780 · P2 · fixed:** `test_shoalmark.py:1924` and `test_shoalmark.py:1949` now recognize the original path, executable-name and wrapper probes; does not block the tag.
- **RV-2781 · P2 · fixed:** `test_shoalmark.py:7723` and `test_shoalmark.py:7763` record the installed-hook and answer board runs in the runtime collection; the recording control and the new empty/disabled-watch controls pass; does not block the tag.
- **RV-2782 · P3 · fixed:** `overrides/landing.html:326` and `overrides/landing.html:525` now agree with the release metadata; does not block the tag.
- **RV-2783:** recorded privately.
- **RV-2784:** recorded privately.

## Commands and controls

Times below are the shell's `date` output on Thu Oct 8, CEST 2026. Durations are not estimates. Tests and mutation controls used disposable repositories; executable test runs denied network access. Nothing was installed and no remote service was consulted.

| Command or control | Start (`date`) | End (`date`) | Result |
|---|---|---|---|
| Authorized `checkout --detach 6b228b5250cce258de91791b847c87b4af1145b3`, `rev-parse HEAD`, status | Thu Oct 8 13:19:39 CEST 2026 | Thu Oct 8 13:19:41 CEST 2026 | Exact SHA; clean. |
| Brief, tracker/requirements inventory, `--next`, `--whoami`, scope log/diff reads | Thu Oct 8 13:19:51 CEST 2026 | Thu Oct 8 13:20:15 CEST 2026 | Brief and every changed line read; no seat identity configured. Requirements are Stage 0's convention. |
| `python3 -m py_compile shoalmark.py test_shoalmark.py test_core.py` | Thu Oct 8 13:21:14 CEST 2026 | Thu Oct 8 13:21:14 CEST 2026 | Exit 0. |
| `python3 -u test_core.py` | Thu Oct 8 13:21:14 CEST 2026 | Thu Oct 8 13:21:29 CEST 2026 | Exit 0; 158 checks pass. |
| `python3 shoalmark.py --check` | Thu Oct 8 13:21:29 CEST 2026 | Thu Oct 8 13:21:36 CEST 2026 | Exit 0. |
| `run-scoped.py`: suite definitions and sixteen selected actual source blocks, in the style of the supplied single-block runner | Thu Oct 8 13:22:05 CEST 2026 | Thu Oct 8 13:27:14 CEST 2026 | Exit 0; 57 checks, no skips. |
| `probe-classifier.py`: ten cases against each revision's reader and actual Check A predicate | Thu Oct 8 13:23:07 CEST 2026 | Thu Oct 8 13:23:57 CEST 2026 | detailed evidence recorded privately |
| Initial runtime probe through `run-one-check.py` | Thu Oct 8 13:23:50 CEST 2026 | Thu Oct 8 13:25:13 CEST 2026 | Board events pass, 180 starts recorded. An added equality assertion fails because it compares six board `ls-tree` calls with twelve calls from all traces; refined below. |
| `git diff --check 9a7ed43 6b228b5` | Thu Oct 8 13:24:54 CEST 2026 | Thu Oct 8 13:24:54 CEST 2026 | Exit 0. |
| `probe-complete-classifier.py`: the entire actual three-check classification block on a temporary product copy | Thu Oct 8 13:26:09 CEST 2026 | Thu Oct 8 13:26:40 CEST 2026 | detailed evidence recorded privately |
| `probe-landing.py`: parsed HTML versus each revision's VERSION and CHANGELOG | Thu Oct 8 13:26:30 CEST 2026 | Thu Oct 8 13:26:30 CEST 2026 | Old label/link/date fail; new label/link/date and upgrade commands all pass. |
| Completed-run logs and source/brief inspection | Thu Oct 8 13:29:34 CEST 2026 | Thu Oct 8 13:29:42 CEST 2026 | Scoped run and complete classifier reproduction verified. |
| `probe-runtime-refined.py` through the supplied single-block runner | Thu Oct 8 13:30:28 CEST 2026 | Thu Oct 8 13:31:39 CEST 2026 | Exit 0; six board-hook `ls-tree` calls match six recorded calls. Five other transaction calls and the preceding manual-refresh call explain the initial twelve. |
| Verdict-format/source lines, counts, tier and metadata inspection | Thu Oct 8 13:30:49 CEST 2026 | Thu Oct 8 13:31:30 CEST 2026 | 57 scoped / 49 matrix checks; exact SHA and clean status reconfirmed. |
| First old-shape driver attempt | Thu Oct 8 13:31:53 CEST 2026 | Thu Oct 8 13:32:06 CEST 2026 | Discarded as an old-version control: the supplied runner defaults to HEAD and re-clones, so replacing an outer copy did not change its tool. The check passed against HEAD; corrected with `--tool` below. |
| Product-byte equality, ADOPT pins and both setup pages | Thu Oct 8 13:32:27 CEST 2026 | Thu Oct 8 13:32:27 CEST 2026 | All assertions pass. |
| Corrected `run-one-check.py --tool v0.19.1 "the board's refresh where the signers file lies"` | Thu Oct 8 13:32:38 CEST 2026 | Thu Oct 8 13:32:48 CEST 2026 | Expected exit 1; all four variants return exit 4 on `ls-tree`. Current head's corresponding variants all return 0. |

The full `python3 -u test_shoalmark.py` was **not rerun at 6b228b5**. This is a scoped re-check of tests/documentation with unchanged product bytes. The earlier 9a7ed43 attempt under the same no-network requirement stopped at an unrelated loopback-socket bind, after 643 passing checks; it was not a completed full-suite pass. No full-suite or remote-CI pass is claimed here. The scoped run's 57 checks and zero skips are its own results, not a substitute count for the full suite.

Final verification at `Thu Oct  8 13:35:32 CEST 2026`: `git rev-parse HEAD` is `6b228b5250cce258de91791b847c87b4af1145b3`; `git status --short` is empty; `git diff --check 9a7ed43 6b228b5` exits 0. The worktree is clean. The report was written after this check.
