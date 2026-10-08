---
id: FM-045
status: In Progress
considered: FM-030, FM-037
tags: bug
next: build
triaged: 2026-10-08
tier: P0
hook: "Where an answer waits on an answer branch and the signers file lies in the working tree, the board's refresh stops and the board goes stale."
---

# FM-045 — The board's refresh stops on git ls-tree, which its read-only list does not hold

## What is true now

**Filed 2026-10-08; nothing is built.**
- **What happens:** `--html-only`, the board's run that the checkout, merge and rewrite hooks start, stops with "the
  board's run was stopped: it would start git ls-tree -r -z — it starts nothing but read-only git and writes only the
  board". It exits 4 and writes nothing.
- **Where it comes from:** `READ_ONLY_GIT` (`shoalmark.py:435`) holds no `ls-tree`. Two readers list a tree with it:
  `tree_paths` (`:6808`) and `path_mode` (`:6819`). `tree_paths` is also called by `guard_walk` and `tip_variants`.
- **The shape that reaches it:** the board's run comes to `tree_paths` through `on_their_way`, `signers_args`,
  `trusted_signers` and `signers_rel`, where all four hold:
  - `owner` is `signed`;
  - `gpg.ssh.allowedSignersFile` names a file in this repository's working tree;
  - origin's default branch is known;
  - an unmerged `answer/<id>` branch on origin sets an answer.
- **What it does to the hooks:** they never block. Each prints "the board is not refreshed (exit 4)" and exits 0. The
  commit hooks run no `--html-only`.
- **What it does to an answer:** the rebuild right after it (`board_after_act`) stops the same way, so the board does
  not show the answer on its way.

## Why

The board's run starts nothing but read-only git. `git ls-tree` lists a tree and writes nothing, so a list without it
refuses a read the run needs, and the board an Owner returns to stays stale.

## Done when

The Owner's rule: a failed board refresh is a product failure, so the fix carries checks for the whole class, not this
case alone. It ships as 0.19.2, a patch release that holds this fix only.
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
  - **Where it runs:** on all five CI systems, on synthetic data only.

## Ship log

| Date | Event |
|---|---|
| 2026-10-08 | Filed. |
| 2026-10-08 | Built by `b3bdb000/implementer-115`: `5a81370` — `ls-tree` joins the board's run's read-only git; a check holds the tree listings the tool sends to the same rule. |
| 2026-10-08 | Built by `b3bdb000/implementer-115`: `e44f73e` — every git command the tool can start is classified: `NEVER_IN_BOARD_RUN` beside READ_ONLY_GIT, fourteen commands with their reasons; a check that reads the tool's source with `ast`, its control, and the runtime half that watches the suite's board runs. |
| 2026-10-08 | Built by `b3bdb000/implementer-115`: `b2b8bdb` — a check builds FM-045's shape and runs `--html-only` in process and as a program, origin/HEAD set and unset: exit 0, the board written, the answer on its way; beside v0.19.1 it fails. |
