# Independent critical re-check of shoalmark 0.19.3 at 0bb1b3b

This pass ran in a session the Owner started, independent of the Planner's session.

Verdict: **READY**.

Reviewed: 0bb1b3b5780975fc27e51d3458ee3319d5ff1341

Scope: `git diff 84d2ab8 0bb1b3b` and `git log 84d2ab8..0bb1b3b`; base 84d2ab8d58d2087edb4914e7a2476c95967de251. Every changed line of `shoalmark.py` and `test_shoalmark.py` was read, together with the release documents, tracker changes and all five scoped commit messages. Claims 6, 11 and 12 use the Owner's replacement rulings for this pass.

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
- **RV-2942:** recorded privately.
- **RV-2943:** recorded privately.
- **RV-2960:** recorded privately.
- **RV-2980:** recorded privately.
- **RV-2981:** recorded privately.

- Compilation, all 158 core checks and this repository's `--check` passed.
- VERSION and the command's version are 0.19.3. The newest CHANGELOG heading is `## 0.19.3 — 2026-10-10`; its headline and the landing's release sentence match the Owner's exact text. The Security heading names GHSA-phwg-xghr-hfvg and GHSA-xfv6-2vf2-fm94, with each set of bullets under its own advisory.
- Both ADOPT pins equal the head's `shoalmark.py` SHA-256: `4a617ee4856413fbc29b1c71d5aee85a6f63d8b7fba6b470de4cf0b15cdab467`. Both setup pages clone `--branch v0.19.3`; the landing's top bar, footer and release link name v0.19.3. The release metadata controls passed all 13 assertions.
- The scoped commit messages, added source comments, test names and release text were checked for disclosure. The earlier independent verdict committed in this scope retains its reviewed bytes.

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
- **RV-2942:** recorded privately.
- **RV-2943:** recorded privately.
- **RV-2960:** recorded privately.

No new finding is established. RV-2982 to RV-2999 remain unused.

## Commands and controls

Times below are exactly as `date` printed them. Blocks and controls ran serially. Numbered invocations retain the disclosure boundary of this pass. The ledger retains initial attempts as well as completed validation.

| Command or invocation | Started | Finished | Exit |
| --- | --- | --- | --- |
| `python3 -m py_compile shoalmark.py test_shoalmark.py test_core.py` | Sat Oct 10 03:51:30 CEST 2026 | Sat Oct 10 03:51:31 CEST 2026 | 0 |
| `python3 -u test_core.py` | Sat Oct 10 03:51:31 CEST 2026 | Sat Oct 10 03:51:48 CEST 2026 | 0 |
| `python3 shoalmark.py --check` | Sat Oct 10 03:51:48 CEST 2026 | Sat Oct 10 03:51:56 CEST 2026 | 0 |
| Invocation 04 | Sat Oct 10 03:51:56 CEST 2026 | Sat Oct 10 03:52:56 CEST 2026 | 0 |
| Invocation 05 | Sat Oct 10 03:52:57 CEST 2026 | Sat Oct 10 03:53:55 CEST 2026 | 0 |
| Invocation 06 | Sat Oct 10 03:53:55 CEST 2026 | Sat Oct 10 03:54:51 CEST 2026 | 0 |
| Invocation 07 | Sat Oct 10 03:54:56 CEST 2026 | Sat Oct 10 03:54:57 CEST 2026 | 1 |
| Invocation 08 | Sat Oct 10 03:56:02 CEST 2026 | Sat Oct 10 03:56:03 CEST 2026 | 0 |
| Release metadata controls | Sat Oct 10 03:56:04 CEST 2026 | Sat Oct 10 03:56:05 CEST 2026 | 0 |
| Version-source check | Sat Oct 10 03:56:05 CEST 2026 | Sat Oct 10 03:57:03 CEST 2026 | 0 |
| Setup release-tag check | Sat Oct 10 03:57:03 CEST 2026 | Sat Oct 10 03:58:02 CEST 2026 | 0 |
| Invocation 12 | Sat Oct 10 03:58:45 CEST 2026 | Sat Oct 10 03:58:47 CEST 2026 | 0 |
| Invocation 13 | Sat Oct 10 03:58:47 CEST 2026 | Sat Oct 10 03:58:48 CEST 2026 | 1 |
| Scope and final worktree check | Sat Oct 10 03:59:19 CEST 2026 | Sat Oct 10 03:59:19 CEST 2026 | 0 |

Final HEAD: 0bb1b3b5780975fc27e51d3458ee3319d5ff1341. `git status --short` was empty at the final check. The pass made no source edit, commit, branch, tag or shared-hook change; the requested detached checkout moved HEAD. No tracked record or product lines were added by this pass, so its effect on the repository's records-to-product ratio is zero.
