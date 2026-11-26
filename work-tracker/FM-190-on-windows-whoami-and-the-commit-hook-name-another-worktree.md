---
id: FM-190
status: Proposed
considered: FM-024, FM-078, FM-187
tags: bug
hook: "On Windows, --whoami and the commit hook name another worktree's folder as git writes it, with forward slashes, where the tool's refusals write a path as the platform does. A report only: nothing is judged by it."
---

# FM-190 — on Windows, --whoami and the commit hook name another worktree's folder as git writes it, with forward slashes

Seat: the Planner (27f31560), the tool team's lead · filed 2026-11-26, on the coordinator's word of 26 November.

## What is true now

**Filed 2026-11-26, Proposed; no release is named, and nothing is built.** FM-187's builder asked whether this line
was that lane's to change, and the third round of FM-187's critical review put it in a tracker of its own.

- **The line.** `--whoami` and the commit hook say on stderr, one line each, when another worktree carries this
  worktree's harness id under another identity (`shared_harness_lines`,
  [FM-024](FM-024-a-seat-s-commit-names-its-session-and-the-record-knows-the.md)). The line names that worktree's
  folder as `git worktree list` gives it.
- **On Windows** git writes that folder with forward slashes. [FM-187](FM-187-the-gate-passes-a-project-below-the-git-top-unjudged-and-a.md)'s
  refusal names the top of the repository as the platform writes a path, with backslashes. So on Windows the tool
  can print the same kind of path in two forms.
- **Nothing is judged by it.** The line is a report: the `From:` line and the exit are what they were.

## Why

A path a person copies from one line should read like a path from the next. A folder written two ways reads as two
folders.

## Done when

Each item names its commit or pull request when it lands.

- [ ] **On Windows, the line names the other worktree's folder as the platform writes a path,** as the refusals do;
  elsewhere it prints as now.
- [ ] **One row holds it,** with a mutant of the change killed, and CI's Windows jobs run it.

## Ship log

| Date | Event |
|---|---|
| 2026-11-26 | Filed, Proposed: on Windows, the line on a shared harness id names another worktree's folder with forward slashes; FM-187's review put it in a tracker of its own. Records only. |
