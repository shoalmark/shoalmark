---
id: FM-045
status: In Progress
considered: FM-030, FM-037
tags: bug
next: review
triaged: 2026-10-08
tier: P0
hook: "Where an answer waits on an answer branch and the signers file lies in the working tree, the board's refresh stops and the board goes stale."
---

# FM-045 — The board's refresh stops on git ls-tree, which its read-only list does not hold

## What is true now

**Built, and cut as 0.19.2 on `release/v0.19.2`, dated 2026-10-10; not yet reviewed as a release, merged or tagged.**
- **What happened (v0.19.1):** `--html-only`, the board's run that the checkout, merge and rewrite hooks start, stopped
  with "the board's run was stopped: it would start git ls-tree -r -z — it starts nothing but read-only git and writes
  only the board", exit 4, nothing written. The hooks never blocked: each printed "the board is not refreshed (exit 4)"
  and exited 0. The rebuild right after an answer (`board_after_act`) stopped the same way.
- **Where it came from:** `READ_ONLY_GIT` held no `ls-tree`. Four places start it: `tree_paths`, `path_mode`,
  `shipped_moves` and `judge_commits`. The board's run came to `tree_paths` through `on_their_way`, `signers_args`,
  `trusted_signers` and `signers_rel`, where all three hold:
  - `gpg.ssh.allowedSignersFile` names a file in this repository's working tree;
  - origin's default branch is known;
  - an unmerged `answer/<id>` branch on origin sets an answer.
- **The fix:** `ls-tree` is on `READ_ONLY_GIT` (`5a81370`); `--output` and a foreign `-c` are still refused. A check builds
  the shape above and runs `--html-only` in process and as a program, origin/HEAD set and unset: exit 0, the board
  written, the answer on its way (`b2b8bdb`). Beside v0.19.1 it fails.
- **Every git command classified** (`e44f73e`): `NEVER_IN_BOARD_RUN`, beside `READ_ONLY_GIT`, names the fourteen other git
  commands the tool starts, each with why the board's run never starts it. A check reads the tool's source with `ast`
  and fails on an unclassified command or an unread form. Its runtime half watches each `--html-only` the suite runs in
  process, each of this tool's own file it runs as a program in its own environment, and every board's run of the board
  matrix through git's trace.
- **The board matrix** (`bdda4ad`, `df63f68`, `7823a7d`): real merges, checkouts and rebases fire the real hooks, and an
  `--answer` its rebuild, in eight git shapes; on Subversion the board's run follows `svn update` and `svn switch`. Its
  control takes each event's own hook out. Every board's run of it — the hooks', the runner's, `--answer`'s and by hand —
  is watched through git's trace, each git it starts a read `read_only_git` admits (`f9cd059`, its control `65b6875`).
- **On `release/v0.19.2`:** slice 1 merged at `13bb2c4`, slice 2 at `b62ad2a`, main at `a36bc03`; the release commit
  `09d5b31` — VERSION, the CHANGELOG section, both ADOPT pins and the setup pages.
- **Left:** the release's critical verdict and the full run on its final head, the merge and the tag; then Shipped. The
  keep is unranked: the next full pass ranks it.

## Why

The board's run starts nothing but read-only git. `git ls-tree` lists a tree and writes nothing, so a list without it
refuses a read the run needs, and the board an Owner returns to stays stale.

## Done when

The Owner's rule: a failed board refresh is a product failure, so the fix carries checks for the whole class, not this
case alone. It ships as 0.19.2, a patch release that holds this fix and the checks for its whole class.
- `ls-tree` is on the board's run's read-only list. Nothing that writes is added.
- A check builds the shape above, runs `--html-only`, and asserts exit 0, the board written, and the answer shown on its
  way. Its control fails beside v0.19.1.
- **Every git command is classified.** A check classifies every git command the tool can start, each either on
  `READ_ONLY_GIT` or named as never started in the board's run, with its reason (`ls-remote` among them). An unclassified
  one fails CI.
- **An end-to-end board matrix:**
  - **The events:** real merges, checkouts and rebases fire the real hooks (`post-merge`, `post-checkout`,
    `post-rewrite`), and an `--answer` fires `board_after_act`.
  - **What each asserts:** the board changed, exit 0, no "stopped" line and no traceback.
  - **The shapes:**
    - a signers file in the tree, with signed answers;
    - answer branches, local and on origin;
    - linked worktrees;
    - a moved tracker folder;
    - origin/HEAD set and unset;
    - several hundred trackers;
    - a foreign hook runner, in the style of lefthook;
    - Subversion.
  - **Where it runs:** in CI on Ubuntu, macOS and Windows, on synthetic data only.

## Ship log

| Date | Event |
|---|---|
| 2026-10-08 | Filed. |
| 2026-10-08 | Built by `b3bdb000/implementer-115`: `5a81370` — `ls-tree` joins the board's run's read-only git; a check holds the tree listings the tool sends to the same rule. |
| 2026-10-08 | Built by `b3bdb000/implementer-115`: `e44f73e` — every git command the tool can start is classified: `NEVER_IN_BOARD_RUN` beside READ_ONLY_GIT, fourteen commands with their reasons; a check that reads the tool's source with `ast`, its control, and the runtime half that watches the suite's board runs. |
| 2026-10-08 | Built by `b3bdb000/implementer-115`: `b2b8bdb` — a check builds FM-045's shape and runs `--html-only` in process and as a program, origin/HEAD set and unset: exit 0, the board written, the answer on its way; beside v0.19.1 it fails. |
| 2026-10-08 | **The board matrix — built** (slice 2) by the Builder seat (`b3bdb000/implementer-116`) on `fm/045-the-board-matrix`, in `test_shoalmark.py` only: `bdda4ad` — an `--answer`, `git switch`, `git merge --no-ff` and `git rebase` fire the real hooks in eight git shapes (a signers file in the tree with signed answers, answer branches local and on origin, a linked worktree, a moved tracker folder, origin/HEAD set, origin/HEAD unset, 304 trackers, a lefthook-style runner), and `svn update` and `svn switch` are followed by `--html-only`: 35 checks; `df63f68` — its control, each event's own board hook taken out: 3 checks; `7823a7d` — the matrix's total printed only where its shapes ran. The signers shape fails on this branch and beside v0.19.1: its board's run stops on `git ls-tree`. |
| 2026-10-08 | **0.19.2 cut** by `b3bdb000/implementer-115` on `release/v0.19.2`: `09d5b31` — VERSION 0.19.2, the CHANGELOG section dated 2026-10-12, both ADOPT pins (SHA-256 `5dfcbff1…0d2f`) and the setup pages. RV-2730 to RV-2733 (P3, verdict `8ee4998`) fixed forward in *What is true now* and *Done when*; `next: review`. |
| 2026-10-08 | Built by `b3bdb000/implementer-115` on `fm/045-rv-2780-check-a-reads-wrapped-git`: `de05c9c` — Check A reads the program as `read_only_git` does (any path, `git.exe`, any case); reads through command wrappers (`env`, `env -i`, `VAR=value`, nested: `nice`, `timeout` and the rest of its list), and git started through one must be a command named never started; names as not read what it cannot resolve — an argv[0] or a wrapper's word it cannot see, git in a shell's code or in an unknown wrapper's words, code handed to a shell it cannot see, an argv list changed in place, through a helper, at module level or by an alias. A control for each form; the runtime half holds every program a board's run starts to be git itself. The tool's own reading is unchanged: 29 commands, nothing unread. RV-2780 (P2), RV-2770 and RV-2771 (P3). |
| 2026-10-08 | **Every board's run of the matrix watched** by the Builder seat (`b3bdb000/implementer-116`) on `fm/045-rv-2781-every-board-run-watched-3`, from `9a7ed43`, in `test_shoalmark.py` only: `f9cd059` — through git's trace (`GIT_TRACE2_EVENT`), the runs the hooks' copy makes for `post-checkout`, `post-merge` and `post-rewrite`, the lefthook-style runner's, `--answer`'s and the runs by hand: each event's own run seen, every git it starts a read `read_only_git` admits, `ls-tree` counted, all recorded for the runtime half; `65b6875` — the watch's control; `2490ebc` — the runtime half's name says exactly what it watches. |
