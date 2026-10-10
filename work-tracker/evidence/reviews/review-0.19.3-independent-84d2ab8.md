# Independent critical re-check of shoalmark 0.19.3 at 84d2ab8

This pass ran in a session the Owner started, independent of the Planner's session.

Verdict: **READY**.

Reviewed: 84d2ab8d58d2087edb4914e7a2476c95967de251

Scope: `git diff 82edbf5 84d2ab8` and `git log 82edbf5..84d2ab8`; base 82edbf565a62d9493b8ac638d78f5c33c821c00d. Every changed line of `shoalmark.py` and `test_shoalmark.py` was read, together with the single commit's message.

Tier: critical. The wider `git diff --name-only origin/main...HEAD` includes code and tests, so the code review loop applies.

## What holds

- **RV-2783:** recorded privately.
- **RV-2785:** recorded privately.
- **RV-2806:** recorded privately.
- **RV-2830:** recorded privately.
- **RV-2831:** recorded privately.
- **RV-2841:** recorded privately.
- **RV-2842:** recorded privately.
- **RV-2843:** recorded privately.
- **RV-2844:** recorded privately.
- **RV-2845:** recorded privately.
- **RV-2906:** recorded privately.
- **RV-2907:** recorded privately.
- **RV-2908:** recorded privately.
- **RV-2940:** recorded privately.
- **RV-2960:** recorded privately.
- **RV-2980:** recorded privately.
- **RV-2981:** recorded privately.

- Compilation, all 158 core checks and this repository's `--check` passed.
- The scoped commit message retains the stipulated wording and ordinary trailers. Source comments and test names were read for disclosure.

Claims 11 and 12 remain reserved for the scoped release-commit pass.

## Findings

- **RV-2980:** recorded privately.
- **RV-2981:** recorded privately.
- **RV-2783:** recorded privately.
- **RV-2785:** recorded privately.
- **RV-2806:** recorded privately.
- **RV-2830:** recorded privately.
- **RV-2831:** recorded privately.
- **RV-2841:** recorded privately.
- **RV-2842:** recorded privately.
- **RV-2843:** recorded privately.
- **RV-2844:** recorded privately.
- **RV-2845:** recorded privately.
- **RV-2906:** recorded privately.
- **RV-2907:** recorded privately.
- **RV-2908:** recorded privately.
- **RV-2940:** recorded privately.
- **RV-2960:** recorded privately.

RV-2982 to RV-2999 remain unused.

## Commands and controls

Times below are exactly as `date` printed them. Blocks and controls ran serially. Numbered invocations retain the disclosure boundary of this pass.

| Command or invocation | Started | Finished | Exit |
| --- | --- | --- | --- |
| `python3 -m py_compile shoalmark.py test_shoalmark.py test_core.py` | Sat Oct 10 03:19:01 CEST 2026 | Sat Oct 10 03:19:02 CEST 2026 | 0 |
| `python3 -u test_core.py` | Sat Oct 10 03:19:02 CEST 2026 | Sat Oct 10 03:19:20 CEST 2026 | 0 |
| `python3 shoalmark.py --check` | Sat Oct 10 03:19:20 CEST 2026 | Sat Oct 10 03:19:28 CEST 2026 | 0 |
| Invocation 04 | Sat Oct 10 03:19:29 CEST 2026 | Sat Oct 10 03:19:57 CEST 2026 | 0 |
| Invocation 05 | Sat Oct 10 03:19:58 CEST 2026 | Sat Oct 10 03:20:02 CEST 2026 | 1 |
| Invocation 06 | Sat Oct 10 03:20:03 CEST 2026 | Sat Oct 10 03:21:12 CEST 2026 | 0 |
| Invocation 07 | Sat Oct 10 03:21:13 CEST 2026 | Sat Oct 10 03:22:23 CEST 2026 | 1 |
| Invocation 08 | Sat Oct 10 03:22:23 CEST 2026 | Sat Oct 10 03:23:53 CEST 2026 | 0 |
| Invocation 09 | Sat Oct 10 03:23:54 CEST 2026 | Sat Oct 10 03:26:40 CEST 2026 | 0 |
| Invocation 10 | Sat Oct 10 03:26:40 CEST 2026 | Sat Oct 10 03:27:47 CEST 2026 | 0 |
| Invocation 11 | Sat Oct 10 03:27:53 CEST 2026 | Sat Oct 10 03:28:05 CEST 2026 | 0 |
| Scope and commit-message audit | Sat Oct 10 03:28:42 CEST 2026 | Sat Oct 10 03:28:42 CEST 2026 | 0 |
| Final HEAD and worktree check | Sat Oct 10 03:28:42 CEST 2026 | Sat Oct 10 03:28:42 CEST 2026 | 0 |

Final HEAD: 84d2ab8d58d2087edb4914e7a2476c95967de251. `git status --short` was empty at the final check. The pass made no source edit, commit, branch, tag or shared-hook change; the requested detached checkout moved HEAD. No tracked record or product lines were added by this pass, so its effect on the repository's records-to-product ratio is zero.
