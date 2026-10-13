From: unavailable — `--whoami` reports no `seat.session`; no session identity was invented or configured.

# FM-045: v0.19.2, independent scoped re-check at a15a969

This pass ran in a session the Owner started, independent of the Planner's session.

Verdict: **NOT READY**.

Reviewed: a15a96982b2367332d77e15606651b445a84ee28. Scope: `git diff acbc9c7 a15a969` and `git log acbc9c7..a15a969`, as the Owner requested. Tier: critical. Tests change, so this takes the code review loop. The wider `git diff --name-only origin/main...HEAD` also names code and configuration; Git reported multiple merge bases. That listing determines the tier, not this re-check's scope. Grading follows the Owner's current rule: P2 for a form an honest change could plausibly write; P3, fixed forward, for a form requiring code written to defeat the reader.

## What holds

- The authorized detached checkout and `rev-parse HEAD` agree on the full reviewed SHA. Every changed line was read, including the added verdict after the independent probes had been constructed. All measurements below were made in this session.
- `shoalmark.py` is byte-for-byte unchanged from acbc9c7, SHA-256 `5dfcbff1115b4aef67ddd4e280451dc17217d0ccd5b7403289082199c6660d2f`. Both ADOPT pins match. This review changes no repository files: zero product lines and zero repository record lines.
- The stock classification block passes: 29 commands and fourteen named as never started in the board's run. Its two notification sites and two deriver forms are each counted once. All **115 supplied controls** pass: twelve original cases, 21 program-form cases, 68 API/argument cases and fourteen exception cases. The requested independent controls and additional adversarial controls were rerun; their detailed evidence is recorded privately.
- The independent installed-hook/answer recording control passes: 180 Git starts across six board-hook runs, with six independently located board `ls-tree` calls matching six recorded calls. The preceding manual refresh separately records nineteen starts. The suite's empty-record and disabled-trace controls also pass.
- Sixteen actual suite blocks run in source order: **59 checks pass, zero fail, zero skip**. Their runtime collection contains 1,966 starts across five in-process runs, six program runs and 65 traced runs; its supplied controls pass.
- All 49 matrix checks pass: 44 positive checks, three removed-hook controls and two recording controls. All eight Git shapes and Subversion run in disposable synthetic repositories: in-tree signers with signed answers, local/remote answer branches, linked worktrees, moved tracker folder, origin/HEAD set and unset, 304 trackers, the foreign hook runner, and SVN update/switch followed by refresh. Actual operations fire installed hooks; refreshed content, exits and stopped/traceback output are checked. No matrix case skipped.
- The deriver's operational boundary is measured separately: **seven no-deriver-in-hooks checks** pass, including two historical negative controls; **six checks in the board/explicit-run deriver block** pass. The board does not reach the deriver, while an explicit run does.
- FM-045's current-tool shape passes all four variants. Its v0.19.1 control fails as expected: all four old-tool variants return exit 4, and the single-block runner exits 1.
- The independent landing control rejects the old 9a7ed43 label/link/date and passes this head's visible release label, tag link, version/date and upgrade commands. The stock landing assertion passes. The permitted CHANGELOG date remains 10 October 2026.
- Compilation, the **158-check core suite**, and `python3 shoalmark.py --check` pass. The requirements folder is Stage 0's convention. No requirement, tracker or shared hook was edited. These are local results; no separate operating-system or remote-CI run is claimed.

## Findings

- **RV-2780 · P2 · fixed:** `test_shoalmark.py:1976` and `test_shoalmark.py:2031` hold the original executable-name/path controls and reject the wrapper control as unread under the current rule; does not block the tag.
- **RV-2781 · P2 · fixed:** `test_shoalmark.py:8004` and `test_shoalmark.py:8057` record the installed-hook and answer board runs; the independent recording control and empty/disabled-watch controls pass; does not block the tag.
- **RV-2782 · P3 · fixed:** `overrides/landing.html:326` and `overrides/landing.html:525` agree with the release metadata; independent old/new controls pass; does not block the tag.
- **RV-2783:** recorded privately.
- **RV-2784:** recorded privately.

## Commands and controls

Times below are shell `date` output on Thu Oct 8, CEST 2026. Test execution denied network access; mutation controls used temporary copies/repositories. Nothing was installed and no remote service was consulted. Detailed evidence is recorded privately.

| Command or control | Start (`date`) | End (`date`) | Result |
|---|---|---|---|
| Brief/hash, authorized detached checkout, `rev-parse HEAD`, status | Thu Oct 8 18:05:16 CEST 2026 | Thu Oct 8 18:05:19 CEST 2026 | Exact requested SHA; clean; brief hash agrees. |
| `--next`, `--whoami`, requirements, scoped log/diff, tracker and classifier source | Thu Oct 8 18:05:28 CEST 2026 | Thu Oct 8 18:06:27 CEST 2026 | Code and records read; no configured seat identity. |
| `python3 -m py_compile shoalmark.py test_shoalmark.py test_core.py` | Thu Oct 8 18:06:19 CEST 2026 | Thu Oct 8 18:06:20 CEST 2026 | Exit 0. |
| `python3 -u test_core.py` | Thu Oct 8 18:06:20 CEST 2026 | Thu Oct 8 18:06:36 CEST 2026 | Exit 0; 158 checks pass. |
| `python3 shoalmark.py --check` | Thu Oct 8 18:06:36 CEST 2026 | Thu Oct 8 18:06:44 CEST 2026 | Exit 0. |
| `run-scoped.py`: sixteen actual suite blocks, using the supplied single-block runner’s method | Thu Oct  8 18:06:19 CEST 2026 | Thu Oct  8 18:15:26 CEST 2026 | Exit 0; 59 checks, no skips. |
| Independent installed-hook/answer recording control | Thu Oct  8 18:06:19 CEST 2026 | Thu Oct  8 18:07:44 CEST 2026 | Exit 0; trace and recorded starts agree. |
| Independent baseline and earlier adversarial controls | Thu Oct  8 18:06:19 CEST 2026 | Thu Oct  8 18:08:10 CEST 2026 | 29 cases completed; detailed evidence recorded privately. |
| Additional independent controls | Thu Oct  8 18:07:33 CEST 2026 | Thu Oct  8 18:08:03 CEST 2026 | Seven cases completed; detailed evidence recorded privately. |
| Independent order and representation controls | Thu Oct  8 18:07:49 CEST 2026 | Thu Oct  8 18:08:04 CEST 2026 | Three cases completed; detailed evidence recorded privately. |
| Independent HTML landing control | Thu Oct  8 18:07:49 CEST 2026 | Thu Oct  8 18:07:50 CEST 2026 | Old/current controls behave as expected. |
| Independent site-exception controls | Thu Oct  8 18:09:00 CEST 2026 | Thu Oct  8 18:09:40 CEST 2026 | Nine cases completed; detailed evidence recorded privately. |
| `run-one-check.py --block 'for op_, what_ in _ND_OPS' 'no deriver in hooks'` | Thu Oct  8 18:09:22 CEST 2026 | Thu Oct  8 18:11:00 CEST 2026 | Exit 0; seven checks pass. |
| `run-one-check.py "the board's run never reaches the deriver"` | Thu Oct  8 18:09:22 CEST 2026 | Thu Oct  8 18:10:44 CEST 2026 | Exit 0; all six checks in the block pass. |
| `run-one-check.py --tool v0.19.1 "the board's refresh where the signers file lies"` | Thu Oct  8 18:10:02 CEST 2026 | Thu Oct  8 18:10:21 CEST 2026 | Expected runner exit 1; four old-tool exits 4. |
| Independent complete-classification-block control, prior forms | Thu Oct  8 18:09:22 CEST 2026 | Thu Oct  8 18:13:47 CEST 2026 | Completed; detailed evidence recorded privately. |
| Independent complete-classification-block control, additional case | Thu Oct  8 18:10:02 CEST 2026 | Thu Oct  8 18:14:24 CEST 2026 | Completed; detailed evidence recorded privately. |
| Independent complete-classification-block control, additional sites | Thu Oct  8 18:10:02 CEST 2026 | Thu Oct  8 18:14:24 CEST 2026 | Completed; detailed evidence recorded privately. |
| Added verdict read after constructing and measuring independent probes | Thu Oct 8 18:09:22 CEST 2026 | Thu Oct 8 18:09:22 CEST 2026 | Remaining scoped record reviewed. |
| Unchanged product, both pins, diff whitespace, source references | Thu Oct 8 18:10:20 CEST 2026 | Thu Oct 8 18:10:20 CEST 2026 | Assertions and diff check pass. |
| Final HEAD, clean status and artifact validation | Thu Oct  8 18:17:40 CEST 2026 | Thu Oct  8 18:17:40 CEST 2026 | Exact requested SHA; `git status --short` empty; report redaction and contents verified. |

The full `python3 -u test_shoalmark.py` was **not rerun at this head**. This scoped re-check covers changed tests/records with unchanged product bytes. The earlier 9a7ed43 attempt under the no-network requirement stopped at an unrelated loopback-socket bind after 643 passing checks; it was not a completed full-suite pass. The scoped checks and the additional deriver checks are reported as those checks only. No full-suite or remote-CI pass is claimed.
