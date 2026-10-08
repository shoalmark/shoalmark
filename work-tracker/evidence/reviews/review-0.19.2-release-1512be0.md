# FM-045: v0.19.2, the release, its critical verdict at 1512be0

Verdict: **READY WITH FINDINGS**.
Reviewed: 1512be0d359186e94f3848c92f2b8ce435d2f1fa. Scope: the release, `origin/main...1512be0` (origin/main 706a1a1): the fix, Check A, the shape check, the board matrix, the release commit, RV-2780 to RV-2782 merged, and Check A rebuilt (42fbd86, 55f9f2b, 29e3262, 588294a, 1512be0). Tier: critical.

## What holds

- `ls-tree` is on READ_ONLY_GIT, and nothing else is added. `read_only_git` and the tripwire are otherwise unchanged. Every form of `ls-tree` the tool sends lists a tree. Each of NEVER_IN_BOARD_RUN's fourteen reasons holds, traced from `board_run`.
- Check A accepts a start only in the form the product writes: a process API called by its plain name, with its argument list and every argument that can choose the program or a shell resolved in full. A helper's forwarded options and argv are read from every call of it, in any order, list or tuple. Its controls show each other access form they inject, options or argv changed apart from where they are bound, code handed to any shell or interpreter, and a start through a wrapper read as not read, failing the check. The product reads clean: 29 commands classified, nothing unread.
- The Owner's two exceptions are each matched by its site, and each site is met once: `notify_argv`'s code handed to osascript and to PowerShell, which ends when that code is made literal; and the repository's deriver, which `run_deriver` starts directly and on Windows as `[sys.executable, derive]`, permanent, started in no hook's run and never in the board's run. Each exception's form outside its site, directly or through a helper, fails the check, and so does a second start at a site.
- The shape check and the board matrix: real merges, checkouts and rebases fire the real hooks, and `--answer` its rebuild, in the Owner's shapes and on Subversion. Every board's run of the matrix is watched through git's trace, and each git it starts is a read `read_only_git` admits.
- The release: VERSION and `__version__` are 0.19.2. `shoalmark.py` is unchanged since 9a7ed43; both ADOPT pins name v0.19.2 and its SHA-256, 5dfcbff1…0d2f. The setup pages clone v0.19.2. The CHANGELOG section is dated 2026-10-10 under the Owner's headline, with no Security heading, and the 0.19.1 section is byte-identical. The landing's top bar, footer link and footer line name v0.19.2, the line in the Owner's words.
- FM-045 says what is built.

## Findings

- Fixed: RV-2770 to RV-2773, RV-2777, RV-2780 to RV-2782 and RV-2805.
- RV-2774: recorded privately.
- RV-2775: recorded privately.
- RV-2776: recorded privately.
- RV-2784: recorded privately.
- RV-2800: recorded privately.
- RV-2801: recorded privately.
- RV-2802: recorded privately.
- RV-2803: recorded privately.
- RV-2804: recorded privately.
- RV-2806: recorded privately.
- RV-2850: recorded privately.
- RV-2783: recorded privately.

## Commands and controls: 2026-10-08, CEST, as `date` printed each

- At 1512be0: `py_compile` exit 0, and `test_shoalmark.py` compiles under Python 3.9.6. `test_core.py` exit 0, all green. `--check` exit 0 and `--session-check` exit 0 (17:05:04–17:05:30).
- run-one-check, two at a time, at 1512be0, each exit 0 (17:05:05–17:21:22): every FM-045 block (15 blocks, 58 checks); both deriver blocks, no deriver in hooks (7 checks) and the board's run never reaches the deriver (6); the footer check; the VERSION, CHANGELOG and ADOPT readers (10 blocks, 93 checks).
- Controls, each exit 1: beside 211ce0b, the `ls-tree` check, Check A's block (4 of 5), the shape check, the matrix's signers shape (5 of 5) and the runtime half (1 of 2); beside 9a7ed43, the footer check.

Quality read: the commit messages and FM-045 read clean.
