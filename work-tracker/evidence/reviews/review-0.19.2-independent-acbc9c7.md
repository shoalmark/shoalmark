From: unavailable — `--whoami` reports no `seat.session`; no session identity was invented or configured.

# FM-045: v0.19.2, independent scoped re-check at acbc9c7

This pass ran in a session the Owner started, independent of the Planner's session.

Verdict: **NOT READY**.

Reviewed: acbc9c74bf3d2909861b7eaf6f8483f425dee6bc. Scope: `git diff 6b228b5 acbc9c7` and `git log 6b228b5..acbc9c7`, as the Owner requested. Tier: critical. Tests change, so this takes the code review loop. The wider `git diff --name-only origin/main...HEAD` also names code and configuration; Git reported multiple merge bases. That listing determines the tier, not this re-check's scope. Grading follows the Owner's current rule: P2 for a form an honest change could plausibly write; P3, fixed forward, for a form requiring code written to defeat the reader.

## What holds

- The authorized detached checkout and `rev-parse HEAD` agree on the full reviewed SHA. The scoped diff was read, including the added verdict after the independent probes had been constructed. All measurements below were made in this session.
- `shoalmark.py` is byte-for-byte unchanged from 6b228b5, SHA-256 `5dfcbff1115b4aef67ddd4e280451dc17217d0ccd5b7403289082199c6660d2f`. Both ADOPT pins match. This review changes no repository files: zero product lines and zero repository record lines.
- The stock classification block passes: 29 commands and fourteen named as never started in the board's run. Its two notification sites and two deriver forms are each counted once. All **95 supplied controls** pass: twelve original cases, 21 program-form cases, 51 API/argument cases and eleven exception cases. Independent adversarial controls were also run and are accounted for in Findings.
- The independent installed-hook/answer recording control passes: 180 Git starts across six board-hook runs, with six independently located board `ls-tree` calls matching six recorded calls. The preceding manual refresh separately records nineteen starts. The suite's empty-record and disabled-trace controls also pass.
- Sixteen actual suite blocks run in source order: **59 checks pass, zero fail, zero skip**. Their runtime collection contains 1,966 starts across five in-process runs, six program runs and 65 traced runs; its supplied controls pass.
- All 49 matrix checks pass: 44 positive checks, three removed-hook controls and two recording controls. All eight Git shapes and Subversion run in disposable synthetic repositories: in-tree signers with signed answers, local/remote answer branches, linked worktrees, moved tracker folder, origin/HEAD set and unset, 304 trackers, the foreign hook runner, and SVN update/switch followed by refresh. Actual operations fire installed hooks; refreshed content, exits and stopped/traceback output are checked. No matrix case skipped.
- The deriver's operational boundary is measured separately: **seven no-deriver-in-hooks checks** pass, including two historical negative controls; **six checks in the board/explicit-run deriver block** pass. The board does not reach the deriver, while an explicit run does. The product's hook guard and board path were also read.
- FM-045's current-tool shape passes all four variants. Its v0.19.1 control fails as expected: all four old-tool variants return exit 4, and the single-block runner exits 1.
- The independent landing control rejects the old 9a7ed43 label/link/date and passes this head's visible release label, tag link, version/date and upgrade commands. The stock landing assertion passes. The permitted CHANGELOG date remains 10 October 2026.
- Compilation, the **158-check core suite**, and `python3 shoalmark.py --check` pass. The requirements folder is Stage 0's convention. No requirement, tracker or shared hook was edited. These are local results; no separate operating-system or remote-CI run is claimed.

## Findings

- **RV-2780 · P2 · fixed:** `test_shoalmark.py:1971` and `test_shoalmark.py:2026` hold the original executable-name/path controls and reject the wrapper control as unread under the new rule; does not block the tag.
- **RV-2781 · P2 · fixed:** `test_shoalmark.py:7989` and `test_shoalmark.py:8026` record the installed-hook and answer board runs; the independent recording control and empty/disabled-watch controls pass; does not block the tag.
- **RV-2782 · P3 · fixed:** `overrides/landing.html:326` and `overrides/landing.html:525` agree with the release metadata; independent old/new controls pass; does not block the tag.
- **RV-2783:** recorded privately.
- **RV-2784:** recorded privately.

## Commands and controls

Times below are shell `date` output on Thu Oct 8, CEST 2026. Test execution denied network access; mutation controls used temporary copies/repositories. Nothing was installed and no remote service was consulted. Detailed evidence is recorded privately.

| Command or control | Start (`date`) | End (`date`) | Result |
|---|---|---|---|
| Authorized detached checkout, `rev-parse HEAD`, status | Thu Oct 8 15:58:01 CEST 2026 | Thu Oct 8 15:58:03 CEST 2026 | Exact requested SHA; clean. |
| Brief/hash, `--next`, `--whoami`, requirements, scoped log/diff | Thu Oct 8 15:58:27 CEST 2026 | Thu Oct 8 15:58:52 CEST 2026 | Brief hash agrees; source/record review begun; no configured seat identity. |
| `python3 -m py_compile shoalmark.py test_shoalmark.py test_core.py` | Thu Oct 8 15:58:47 CEST 2026 | Thu Oct 8 15:58:48 CEST 2026 | Exit 0. |
| `python3 -u test_core.py` | Thu Oct 8 15:58:48 CEST 2026 | Thu Oct 8 15:59:06 CEST 2026 | Exit 0; 158 checks pass. |
| `python3 shoalmark.py --check` | Thu Oct 8 15:59:06 CEST 2026 | Thu Oct 8 15:59:14 CEST 2026 | Exit 0. |
| `run-scoped.py`: definitions and sixteen actual suite blocks, following the supplied single-block runner's method | Thu Oct 8 15:58:47 CEST 2026 | Thu Oct 8 16:06:35 CEST 2026 | Exit 0; 59 checks, no skips. |
| Remaining classifier diff, deriver sites and operational guards | Thu Oct 8 16:01:27 CEST 2026 | Thu Oct 8 16:03:29 CEST 2026 | Source and controls read. |
| Independent installed-hook/answer recording control | Thu Oct 8 16:01:27 CEST 2026 | Thu Oct 8 16:02:51 CEST 2026 | Exit 0. |
| Independent HTML landing control | Thu Oct 8 16:01:27 CEST 2026 | Thu Oct 8 16:01:28 CEST 2026 | Old/current controls behave as expected. |
| Initial independent probe driver | Thu Oct 8 16:03:12 CEST 2026 | Thu Oct 8 16:03:42 CEST 2026 | Harness argument error; corrected and rerun below; not a product finding. |
| `run-one-check.py --block 'for op_, what_ in _ND_OPS' 'no deriver in hooks'` | Thu Oct 8 16:03:44 CEST 2026 | Thu Oct 8 16:05:10 CEST 2026 | Exit 0; seven checks pass. |
| `run-one-check.py "the board's run never reaches the deriver"` | Thu Oct 8 16:03:44 CEST 2026 | Thu Oct 8 16:04:54 CEST 2026 | Exit 0; named check and all six checks in its block pass. |
| `run-one-check.py --tool v0.19.1 "the board's refresh where the signers file lies"` | Thu Oct 8 16:03:44 CEST 2026 | Thu Oct 8 16:03:56 CEST 2026 | Expected runner exit 1; four old-tool exits 4. |
| Corrected independent allowlist/exception probes, including earlier controls | Thu Oct 8 16:04:41 CEST 2026 | Thu Oct 8 16:06:21 CEST 2026 | 29 cases completed; detailed evidence recorded privately. |
| Three independent complete-classification-block controls | Thu Oct 8 16:05:57 CEST 2026 | Thu Oct 8 16:08:56 CEST 2026 | Completed; individual results and end times recorded privately. |
| Added verdict read after constructing independent probes | Thu Oct 8 16:06:26 CEST 2026 | Thu Oct 8 16:06:26 CEST 2026 | Scoped record reviewed. |
| Additional independent order/representation controls | Thu Oct 8 16:08:11 CEST 2026 | Thu Oct 8 16:08:24 CEST 2026 | Completed; detailed evidence recorded privately. |
| Source-line and diff-whitespace checks | Thu Oct 8 16:08:27 CEST 2026 | Thu Oct 8 16:08:27 CEST 2026 | Diff whitespace check exits 0. |
| Counts, unchanged product, both pins and tier listing | Thu Oct 8 16:09:31 CEST 2026 | Thu Oct 8 16:09:32 CEST 2026 | All assertions pass. |
| `rev-parse HEAD`, clean status and finding references | Thu Oct 8 16:10:27 CEST 2026 | Thu Oct 8 16:10:27 CEST 2026 | Exact SHA; status empty. |

The full `python3 -u test_shoalmark.py` was **not rerun at this head**. This scoped re-check covers changed tests/records with unchanged product bytes. The earlier 9a7ed43 attempt under the no-network requirement stopped at an unrelated loopback-socket bind after 643 passing checks; it was not a completed full-suite pass. The scoped checks and the additional deriver checks are reported as those checks only. No full-suite or remote-CI pass is claimed.

Final verification at `Thu Oct  8 16:14:41 CEST 2026`: `git rev-parse HEAD` is `acbc9c74bf3d2909861b7eaf6f8483f425dee6bc`; `git status --short` is empty; `git diff --check 6b228b5 acbc9c7` exits 0. The worktree is clean. The report was written after this check.
