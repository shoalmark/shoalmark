---
id: FM-058
status: In Progress
considered: FM-006, FM-045, FM-050
tags: bug
next: build
triaged: 2026-10-17
tier: P1
hook: "A command a person runs through the hooks' copy is stopped after the hook's 35 s, and an answer's PIN, touch and push can take longer"
ask: "How long may a run of shoalmark take before the tool stops it: a hook's run, the board's run, and a command a person runs?"
ask-kind: ruling
ask-since: 2026-10-16
ask-options: "60 s for a hook's run and the board's run; no bound on a command a person runs | 60 s for every run, a person's commands included | the bounds I name in my answer"
ask-proposal: "60 s for a hook's run and the board's run; no bound on a command a person runs"
answer: "accepted - 60 s for a hook's run and the board's run; no bound on a command a person runs"
answered: 2026-10-17
answered-by: holgo99
---

# FM-058 — a command a person runs through the hooks' copy is stopped at the hook's 35 s

## What is true now

**Built at `93f064f` on `fm/058-run-bounds`, for v0.20.1; independent critical-tier review remains.** The Owner's signed answer (`96afebd`) is implemented: a hook's run of the copy and the board's `--html-only` run default to 60 s, still set by `SHOALMARK_BOARD_SECONDS`; explicit person commands through the copy or the tree's tool have no watchdog. For the timeout alone, parsed arguments identify hook modes (`--session-check`, `--session-trailer`, `--commit-msg`, `--print-written`, `--tsvn-hook`, `--html-only`), which stay bounded even in mixed commands. Plain, unknown or malformed copy invocations are ambiguous and stay bounded, including by hand. The `COPY` marker and every existing restriction of the copy are unchanged. The obsolete 35 s default and blanket copy timeout are replaced, and the README and both setup pages name the distinction. `test_run_bounds.py` passes 22 process-entry controls and rejects all three mutants on Python 3.15 and 3.9.6, also in the 3.15 CRLF stand-in; changed-file compilation, CLI, core with skeleton and launch ratchet, Git entry differential and affected suite blocks pass on both interpreters. Next: the independent Reviewer judges this build and its record against the signed answer; the status and next field remain as judged until that review.

## Done when

- The Owner's signed answer stands here, and the build's brief cites it.
- Built in v0.20.1, before the guided answer view, with its class test.

## Ship log

| Date | Event |
|---|---|
| 2026-10-17 | Judged In Progress, P1, by the Planner on the Owner's signed answer (`96afebd`), before the first build commit, on `fm/058-run-bounds`. |
| 2026-10-16 | Filed, defect 10, with its ask (the Auditor's finding, relayed by the Owner). Nothing is built. |
| 2026-10-16 | Moved into v0.20.1 on the Owner's word: the guided answer view (FM-059) needs it first. |
| 2026-10-17 | Built `93f064f`: 60 s hook/board default, explicit person commands unbounded, ambiguous copy invocations bounded; COPY restrictions unchanged. Class controls and three mutants, CLI, core/skeleton/ratchet, Git entry differential and affected blocks pass on Python 3.15 and 3.9.6; the 3.15 CRLF class stand-in passes. Independent critical-tier review is next. |
