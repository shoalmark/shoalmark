# FM-045: v0.19.2, independent scoped re-check at 2a4037a

This pass ran in a session the Owner started, independent of the Planner's session.

Verdict: **READY WITH FINDINGS**.

Reviewed: 2a4037afb0a59b88adf51c0b14d9b7d02cf83239. Scope: `git diff a15a969 2a4037a` and `git log a15a969..2a4037a`: bf79cd3 changes `test_shoalmark.py`; 2a4037a adds its Reviewer verdict. Tier: critical; code review loop. The Owner's end rule for this round applies. This pass produces review evidence and changes no product files.

## What holds

- The detached HEAD matches the reviewed SHA. Both scoped commits and every changed line were read.
- `shoalmark.py` is unchanged across this scope, SHA-256 `5dfcbff1115b4aef67ddd4e280451dc17217d0ccd5b7403289082199c6660d2f`. Both ADOPT pins match it.
- The product's Check A reading finds **29 commands, nothing unread**, fourteen commands named as never started in the board's run, and each of the four named exception entries once. All **126 supplied controls** pass: twelve command cases, 21 program cases, 76 API/argument cases and seventeen exception cases.
- All **sixteen independent per-caller controls** give the expected result: executable supplied, omitted or `None`, both call orders, lists and tuples, including overrides that select a different program from argv[0]. The actual command executions agree. Inserting an unclassified command through each product forwarding helper, in `queue_actions` and `git_ship_verdicts`, fails Check A. All nine independent outside-site helper controls are rejected.
- Sixteen suite blocks run in source order: **59 checks pass, zero fail, zero skip**. These include the changed classification block, the current FM-045 shape, the matrix and its controls, the runtime classification block, and the landing footer check.
- All **49 matrix checks** pass: 44 positive checks, three removed-hook controls and two recording controls. The eight Git shapes and Subversion run; real Git operations fire the installed hooks and an answer its rebuild. The checks assert refreshed board content, successful exits and absence of stopped/traceback output.
- The suite records **1,966 Git starts** across five in-process runs, six program runs and 65 traced runs. The independent recording control matches six board `ls-tree` calls to six recorded calls among 180 starts across six hook/answer runs; its manual refresh separately records nineteen starts.
- The seven no-deriver-in-hooks checks and all six checks in the board/explicit-run deriver block pass. Compilation, all **158 core checks**, and `python3 shoalmark.py --check` pass.

## Findings

- **RV-2780 · P2 · fixed:** executable-name/path and wrapper controls pass (`test_shoalmark.py:1976`, `test_shoalmark.py:2031`).
- **RV-2781 · P2 · fixed:** runtime recording and its independent controls pass (`test_shoalmark.py:8027`, `test_shoalmark.py:8080`).
- **RV-2782 · P3 · fixed:** the landing footer check agrees with the release metadata (`overrides/landing.html:525`).
- **RV-2783:** recorded privately.
- **RV-2784:** recorded privately.
- **RV-2785:** recorded privately.

## Commands and controls

Times are shell `date` output. This file reports this session's checks only.

| Command or control | Start (`date`) | End (`date`) | Result |
|---|---|---|---|
| Brief/hash, detached checkout, `rev-parse HEAD` | Thu Oct  8 19:17:23 CEST 2026 | Thu Oct  8 19:17:25 CEST 2026 | Exact requested SHA; brief hash verified. |
| Required record reads, scoped log/diff and source review | Thu Oct  8 19:17:36 CEST 2026 | Thu Oct  8 19:22:38 CEST 2026 | Two commits and all changed lines read. |
| `python3 -m py_compile shoalmark.py test_shoalmark.py test_core.py` | Thu Oct  8 19:18:31 CEST 2026 | Thu Oct  8 19:18:32 CEST 2026 | Exit 0. |
| `python3 -u test_core.py` | Thu Oct  8 19:18:32 CEST 2026 | Thu Oct  8 19:18:51 CEST 2026 | Exit 0; 158 checks pass. |
| `python3 shoalmark.py --check` | Thu Oct  8 19:18:51 CEST 2026 | Thu Oct  8 19:19:00 CEST 2026 | Exit 0. |
| Sixteen suite blocks, using the supplied single-block runner method | Thu Oct  8 19:18:31 CEST 2026 | Thu Oct  8 19:27:28 CEST 2026 | Exit 0; 59 checks pass, no skips. |
| Independent forwarding controls | Thu Oct  8 19:18:31 CEST 2026 | Thu Oct  8 19:19:02 CEST 2026 | Seven cases completed; evidence recorded privately. |
| Independent outside-site helper controls | Thu Oct  8 19:18:31 CEST 2026 | Thu Oct  8 19:19:09 CEST 2026 | All nine injected forms rejected. |
| Independent executable/order/representation controls | Thu Oct  8 19:19:54 CEST 2026 | Thu Oct  8 19:20:28 CEST 2026 | All sixteen expected outcomes verified. |
| Initial independent source probe | Thu Oct  8 19:20:50 CEST 2026 | Thu Oct  8 19:20:52 CEST 2026 | Driver assertion before checks; corrected run below. |
| Completed independent source probes | Thu Oct  8 19:21:56 CEST 2026 | Thu Oct  8 19:22:13 CEST 2026 | Seven cases completed; evidence recorded privately. |
| Independent execution controls | Thu Oct  8 19:24:04 CEST 2026 | Thu Oct  8 19:24:05 CEST 2026 | Two cases completed; evidence recorded privately. |
| Independent baseline and access-form controls | Thu Oct  8 19:21:34 CEST 2026 | Thu Oct  8 19:23:31 CEST 2026 | 29 cases completed; evidence recorded privately. |
| Independent hook/answer recording control | Thu Oct  8 19:21:34 CEST 2026 | Thu Oct  8 19:23:07 CEST 2026 | Exit 0; recorded starts match the trace. |
| No-deriver-in-hooks block | Thu Oct  8 19:21:34 CEST 2026 | Thu Oct  8 19:23:03 CEST 2026 | Exit 0; seven checks pass. |
| Board/explicit-run deriver block | Thu Oct  8 19:21:34 CEST 2026 | Thu Oct  8 19:22:49 CEST 2026 | Exit 0; six checks pass. |
| Product equality, both pins and `git diff --check a15a969 2a4037a` | Thu Oct  8 19:22:38 CEST 2026 | Thu Oct  8 19:22:38 CEST 2026 | Pass. |
| Final `rev-parse HEAD` and `git status --short` | Thu Oct  8 19:31:05 CEST 2026 | Thu Oct  8 19:31:05 CEST 2026 | Exact reviewed SHA; status empty. |

The full `python3 -u test_shoalmark.py` was skipped as requested. No full-suite result from another session is claimed here.
