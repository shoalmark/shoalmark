---
id: FM-044
status: Proposed
considered: FM-003
tags: bug
next: wait
hook: "A Subversion team without git cannot run the tool at all: every command but --session-check stops with a traceback before it writes anything."
---

# FM-044 — shoalmark stops with a traceback where git is not installed, on Subversion too

## What is true now

**Filed 2026-10-08, for 0.19.2; nothing is built.** Where `git` is not installed, every command except `--session-check`
stops with a Python traceback (`FileNotFoundError`) before it writes anything. That holds in a folder with no version
control and in a Subversion working copy alike. The first call to fail is `git_dirs()` (`shoalmark.py:273`), which a
command reaches when it judges the tracker folder. The tool runs `git` directly in 53 places and through `git_out` in
the rest, and none of them handles a missing `git`. CI installs `git` on every system, so no check runs without it.

## Why

FM-003's S1 claims that a Subversion working copy "with no git at all" runs `--init`, `--new`, the gate, `INDEX.md`, the
board and `--triage`. Its check builds that working copy on a machine where `git` is installed, so the claim fails
exactly where a Subversion team has no `git`. Until this is fixed, the probe names `git` as a prerequisite on every
machine (the Owner's ruling of 2026-10-08).

## Done when

- Where `git` is not installed, every command that needs no `git` runs. Every command that needs it refuses in one line
  that names `git`, before any write.
- No run stops with a traceback, and none judges less: the write rule, the guard and the judgement of the tracker
  folder fail closed.
- A check runs the Subversion cases with no `git` on `PATH`, on every system in CI.
- README and ADOPT say what works without `git`.

## Ship log

| Date | Event |
|---|---|
| 2026-10-08 | Filed, for 0.19.2. |
