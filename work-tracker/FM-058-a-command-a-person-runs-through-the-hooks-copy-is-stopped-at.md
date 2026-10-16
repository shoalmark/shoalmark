---
id: FM-058
status: Proposed
considered: FM-006, FM-045, FM-050
tags: bug
next: owner
hook: "A command a person runs through the hooks' copy is stopped after the hook's 35 s, and an answer's PIN, touch and push can take longer"
ask: "How long may a run of shoalmark take before the tool stops it: a hook's run, the board's run, and a command a person runs?"
ask-kind: ruling
ask-since: 2026-10-16
ask-options: "60 s for a hook's run and the board's run; no bound on a command a person runs | 60 s for every run, a person's commands included | the bounds I name in my answer"
ask-proposal: "60 s for a hook's run and the board's run; no bound on a command a person runs"
---

# FM-058 — a command a person runs through the hooks' copy is stopped at the hook's 35 s

## What is true now

**Filed 2026-10-16, defect 10, with its ask; nothing is built.** On the Owner's word of the same day it moves into
v0.20.1: the guided answer view (FM-059, quick win 11) needs a command a person runs to have no bound, so it is built
first.

**Facts,** read at main `5f792d6`.
- **A run of the hooks' copy is a hook's run.** `HOOK_RUN` (`shoalmark.py:59`) is true for every run of the copy of the
  tool that `--install-hook` keeps in the git directory, a person's run of it by hand included.
- **Such a run is bounded.** The board's run, and every hook's run of the copy, starts `board_watchdog` (`:10685–10686`,
  `:10232`): after `BOARD_RUN_SECONDS` (`:10229`), 35 s unless `SHOALMARK_BOARD_SECONDS` sets it, the process ends,
  exit 4, whatever it waits on.
- **What a person's command waits on.** `--answer` signs its commit, which can ask for the key's PIN and a touch, and
  pushes the answer branch. Neither is a hook's work, and together they can take longer than 35 s.
- **The case.** On 16 October, `0f61c45` on `answer/fm-004` recorded the Owner's refused `--answer`; its reason begins
  `the commit was refused: error: Signing file`. The signed answer `92ecdce` followed. The Auditor attributed the attempt
  to the bound; these commits do not verify the invocation path, elapsed time or a watchdog exit. The 35 s line was seen
  in the Owner's terminal, as the Auditor relays it; no commit shows the run's time.
- **Until it is built:** `SHOALMARK_BOARD_SECONDS=60`, or more, in the environment gives a run longer, as the hook's
  refusal line says.

**The Owner's word:** the default bound is raised to 60 s at least. The ask above asks for the signed answer.

**Fix, as proposed:**
- a hook's run and the board's run: 60 s by default, and `SHOALMARK_BOARD_SECONDS` still sets it;
- a command a person runs, through the hooks' copy or the tree's tool: no bound;
- only the bound changes. What a hook's run of the copy may do stays as it is;
- how the tool tells a hook's run from a person's is the build's to choose and the review's to check.

**Test for the class.** For each run: a hook's run of the copy, the board's run, and a person's command through the
copy and through the tree's tool.
- With a short bound set for the test, a child that waits past it: the hook's run and the board's run are stopped,
  exit 4, with their one line; a person's command is not.
- With nothing set, the bound is 60 s.
- A mutant that reads a person's run of the copy as a hook's run fails the test.

## Done when

- The Owner's signed answer stands here, and the build's brief cites it.
- Built in v0.20.1, before the guided answer view, with its class test.

## Ship log

| Date | Event |
|---|---|
| 2026-10-16 | Filed, defect 10, with its ask (the Auditor's finding, relayed by the Owner). Nothing is built. |
| 2026-10-16 | Moved into v0.20.1 on the Owner's word: the guided answer view (FM-059) needs it first. |
