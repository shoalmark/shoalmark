# Independent critical review of shoalmark 0.19.3 at 6828dba

This pass ran in a session the Owner started, independent of the Planner's session.

Verdict: **NOT READY**.

Reviewed: 6828dba64fda3fd9fd2a5e7a1afc8f009c8ad23f

Scope: `git diff ceb21b8 6828dba` and `git log ceb21b8..6828dba`; base ceb21b823680fa03c59ace7f7f58f49c52eeb208. Every changed line of `shoalmark.py` was read.

Tier: critical.

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

Check A passes at the release head

- C records the tracker files, configuration and answer references in `view/built.json`, written after the page and every view. The nine basis checks, the commit-hook check and the two non-git checks passed. An interrupted refresh preserves the previous record; HEAD moving alone produces no older-board line. The exact-path checks passed (`shoalmark.py:4353`, `:4383`, `:4392`; `test_shoalmark.py:10594`).
- The basis is obtained after the preliminary refresh checks succeed (`shoalmark.py:9687`).
- The deriver's timeout text agrees with the tool's entry paths, including TortoiseSVN. Seven checks passed. The changed timing checks measure this thread's CPU time; the normal inputs passed, and deliberately slow CPU controls were rejected by both timing limits (`shoalmark.py:8643`, `:8690`; `test_shoalmark.py:1401`, `:5216`).
- The scoped private-item commit messages retain the stipulated wording and ordinary trailers. The changed records and comments were read for disclosure.

Claims 11 and 12 are reserved for the scoped release-commit pass, as directed.

## Findings

- **RV-2980:** recorded privately.

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

RV-2981 to RV-2999 remain unused.

## Commands and controls

Times below are exactly as `date` printed them. Selected blocks and controls ran serially. Numbered invocations retain the disclosure boundary of this pass.

| Command or invocation | Started | Finished | Exit |
| --- | --- | --- | --- |
| `python3 -m py_compile shoalmark.py test_shoalmark.py test_core.py` | Fri Oct  9 21:02:05 CEST 2026 | Fri Oct  9 21:02:05 CEST 2026 | 0 |
| `python3 -u test_core.py` | Fri Oct  9 21:02:05 CEST 2026 | Fri Oct  9 21:02:23 CEST 2026 | 0 |
| `python3 shoalmark.py --check` | Fri Oct  9 21:02:33 CEST 2026 | Fri Oct  9 21:02:40 CEST 2026 | 0 |
| Invocation 04 | Fri Oct  9 21:02:56 CEST 2026 | Fri Oct  9 21:06:45 CEST 2026 | 0 |
| Invocation 05 | Fri Oct  9 21:07:59 CEST 2026 | Fri Oct  9 21:08:59 CEST 2026 | 0 |
| Invocation 06 | Fri Oct  9 21:09:47 CEST 2026 | Fri Oct  9 21:10:43 CEST 2026 | 0 |
| Invocation 07 | Fri Oct  9 21:11:40 CEST 2026 | Fri Oct  9 21:13:31 CEST 2026 | 0 |
| Invocation 08 | Fri Oct  9 21:13:31 CEST 2026 | Fri Oct  9 21:16:04 CEST 2026 | 0 |
| Invocation 09 | Fri Oct  9 21:16:04 CEST 2026 | Fri Oct  9 21:17:31 CEST 2026 | 0 |
| Invocation 10 | Fri Oct  9 21:17:31 CEST 2026 | Fri Oct  9 21:18:34 CEST 2026 | 0 |
| Invocation 11 | Fri Oct  9 21:18:34 CEST 2026 | Fri Oct  9 21:20:41 CEST 2026 | 0 |
| Invocation 12 | Fri Oct  9 21:20:41 CEST 2026 | Fri Oct  9 21:21:52 CEST 2026 | 0 |
| Invocation 13 | Fri Oct  9 21:21:52 CEST 2026 | Fri Oct  9 21:23:03 CEST 2026 | 0 |
| Invocation 14 | Fri Oct  9 21:23:03 CEST 2026 | Fri Oct  9 21:25:07 CEST 2026 | 0 |
| Invocation 15 | Fri Oct  9 21:25:07 CEST 2026 | Fri Oct  9 21:26:20 CEST 2026 | 0 |
| C: basis and stale-board notices | Fri Oct  9 21:26:20 CEST 2026 | Fri Oct  9 21:27:39 CEST 2026 | 0 |
| C: commit hooks | Fri Oct  9 21:27:39 CEST 2026 | Fri Oct  9 21:28:47 CEST 2026 | 0 |
| C: non-git folders | Fri Oct  9 21:28:47 CEST 2026 | Fri Oct  9 21:29:46 CEST 2026 | 0 |
| Deriver checks | Fri Oct  9 21:29:46 CEST 2026 | Fri Oct  9 21:30:58 CEST 2026 | 0 |
| Large-log CPU timing | Fri Oct  9 21:30:58 CEST 2026 | Fri Oct  9 21:31:07 CEST 2026 | 0 |
| Invocation 21 | Fri Oct  9 21:31:07 CEST 2026 | Fri Oct  9 21:31:10 CEST 2026 | 0 |
| Invocation 22 | Fri Oct  9 21:31:10 CEST 2026 | Fri Oct  9 21:32:26 CEST 2026 | 0 |
| Invocation 23 | Fri Oct  9 21:32:26 CEST 2026 | Fri Oct  9 21:33:48 CEST 2026 | 0 |
| Invocation 24 | Fri Oct  9 21:33:48 CEST 2026 | Fri Oct  9 21:35:06 CEST 2026 | 0 |
| Invocation 25 | Fri Oct  9 21:35:06 CEST 2026 | Fri Oct  9 21:36:24 CEST 2026 | 0 |
| Commit-message disclosure audit | Fri Oct  9 21:37:15 CEST 2026 | Fri Oct  9 21:37:16 CEST 2026 | 0 |
| Invocation 27 | Fri Oct  9 21:36:24 CEST 2026 | Fri Oct  9 21:37:42 CEST 2026 | 0 |
| Invocation 28 | Fri Oct  9 21:37:42 CEST 2026 | Fri Oct  9 21:38:58 CEST 2026 | 0 |
| Invocation 29 | Fri Oct  9 21:38:59 CEST 2026 | Fri Oct  9 21:40:23 CEST 2026 | 0 |
| Invocation 30 | Fri Oct  9 21:40:23 CEST 2026 | Fri Oct  9 21:41:47 CEST 2026 | 0 |
| Invocation 31 | Fri Oct  9 21:41:47 CEST 2026 | Fri Oct  9 21:41:49 CEST 2026 | 2 |
| Invocation 32 | Fri Oct  9 21:41:49 CEST 2026 | Fri Oct  9 21:42:57 CEST 2026 | 0 |
| Invocation 33 | Fri Oct  9 21:42:57 CEST 2026 | Fri Oct  9 21:44:07 CEST 2026 | 0 |
| Invocation 34 | Fri Oct  9 21:44:07 CEST 2026 | Fri Oct  9 21:45:51 CEST 2026 | 1 |
| Invocation 35 | Fri Oct  9 21:45:51 CEST 2026 | Fri Oct  9 21:48:01 CEST 2026 | 1 |
| Invocation 36 | Fri Oct  9 21:48:01 CEST 2026 | Fri Oct  9 21:49:16 CEST 2026 | 1 |
| Invocation 37 | Fri Oct  9 21:49:16 CEST 2026 | Fri Oct  9 21:50:35 CEST 2026 | 1 |
| Invocation 38 | Fri Oct  9 21:50:35 CEST 2026 | Fri Oct  9 21:52:32 CEST 2026 | 1 |
| C: earlier-tool control | Fri Oct  9 21:52:32 CEST 2026 | Fri Oct  9 21:53:40 CEST 2026 | 1 |
| Deriver: earlier-tool control | Fri Oct  9 21:53:40 CEST 2026 | Fri Oct  9 21:54:43 CEST 2026 | 1 |
| Invocation 41 | Fri Oct  9 21:54:43 CEST 2026 | Fri Oct  9 21:54:46 CEST 2026 | 0 |
| Invocation 42 | Fri Oct  9 21:54:46 CEST 2026 | Fri Oct  9 21:54:47 CEST 2026 | 1 |
| Invocation 43 | Fri Oct  9 21:54:47 CEST 2026 | Fri Oct  9 21:54:48 CEST 2026 | 1 |
| Invocation 44 | Fri Oct  9 21:55:26 CEST 2026 | Fri Oct  9 21:55:28 CEST 2026 | 0 |
| CPU timing controls | Fri Oct  9 21:55:40 CEST 2026 | Fri Oct  9 21:56:04 CEST 2026 | 0 |
| Invocation 46 | Fri Oct  9 21:56:24 CEST 2026 | Fri Oct  9 21:56:39 CEST 2026 | 1 |
| Invocation 47 | Fri Oct  9 21:58:49 CEST 2026 | Fri Oct  9 22:00:01 CEST 2026 | 1 |
| Invocation 48 | Fri Oct  9 22:00:12 CEST 2026 | Fri Oct  9 22:01:28 CEST 2026 | 0 |
| Invocation 49 | Fri Oct  9 22:01:40 CEST 2026 | Fri Oct  9 22:02:45 CEST 2026 | 0 |
| Final HEAD and worktree check | Fri Oct  9 22:03:55 CEST 2026 | Fri Oct  9 22:03:56 CEST 2026 | 0 |

Final HEAD: 6828dba64fda3fd9fd2a5e7a1afc8f009c8ad23f. `git status --short` was empty. No tracked file, shared hook or ref changed in this pass.
