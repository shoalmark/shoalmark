---
id: FM-096
status: Proposed
considered: FM-083, FM-088, FM-095
tags: seamanship
hook: "Nothing measures whether a session follows the rules and lessons it is given. An eval harness would run real sessions on Claude Code and Codex, sealed, in fixture repositories built from real failures, three times each, and gate only on a scenario that always passed and now always fails."
---

# FM-096 — nothing measures whether a session follows the rules and lessons it is given

## What is true now

**Filed 2026-10-29 for v0.20.x; nothing is built.** On the Owner's word of 29 October, "file those", for agentic
seamanship. It is considered for every v0.20 release and pulled into one when it fits.
[FM-089](FM-089-agentic-seamanship-v0-20-3.md), v0.20.3's chapter, names it as a candidate, not a part.

- **What it measures:** the agent harness as a user meets it.
  - shoalmark's contract, briefs, hooks and gate are harness work around Claude Code and Codex.
  - So a scenario runs a real session (`claude -p`, `codex exec`) under the real `AGENTS.md` and a real brief, in a
    fixture repository.
  - It is never a model call given a summary of the rules.
- **The method, in six steps:**
  1. **Start from real failures, and name their types.** The first set comes from the work of 29 October:
     - suite runs piling up on one machine;
     - seats each writing their own lock script;
     - a paused run breaking a timed check;
     - a guard matching a process it did not start;
     - a verdict pushed onto a pull request's branch, restarting its CI;
     - the merge button pressed for a base that is not the default branch;
     - a shell modifier eating a refspec;
     - a claim about the site made from the code instead of the rendered page.
  2. **A golden per rule:** the situation, the expected decision, and the rule behind it. Scenarios where the right act
     is to go ahead are goldens too, so that a rule does not fire where it should not.
  3. **One grader per failure type, given only the evidence it needs.**
     - Outcome checks come first, and are deterministic: refs, processes left running, files, and the commands in the
       session's log.
     - A model judge grades only the words of a report.
     - Each grader is tried on labelled good and bad runs before it is trusted, as every check here meets its mutants.
  4. **Each scenario three times, on each harness:** always pass, always fail, or flaky. A flaky case is read: did the
     session vary, or the grader?
  5. **Compare two runs:** fixed, regressed, now flaky, still failing. The list of work comes first and the pass rate
     last, with one change per run.
  6. **The gate:**
     - It is red only when a scenario that always passed now always fails, over three runs.
     - A missing result is an error, never a pass.
     - Flaky cases are listed for a person, and block nothing.
- **Sessions act, so every scenario runs sealed:** no credentials, no network and a scratch home. The fixture repository
  has stand-ins for `gh` and the forge. Every process a scenario starts ends with it, as the browser rule's guard does.
- **The real failures stay private:** the public scenarios are made-up fixtures in their shape.
- **A scenario is a whole session, and costs model calls.**
  - It never runs on a public pull request, and no key is reachable from one.
  - It runs when a ruling, the contract, a brief or a model changes, on the Owner's machine or a private runner.
  - Its report is filed.
- **One harness, two users:** it runs [FM-088](FM-088-the-team-s-lessons-live-only-in-each-harness-s-local-memory.md)'s
  scenarios for prose memory, and [FM-095](FM-095-the-owner-s-rulings-live-in-chat-memories-and-briefs-not-in.md)'s for
  rules held by generated words or by words alone. Building it once is why it is a tracker of its own.
  - FM-088's own eval may run on the smallest runner that does the job until this harness takes it over.
- **The order:** after FM-095.

## Why

A rule or a lesson that no check can hold is only as good as the sessions that follow it, and nothing measures that
today. [FM-083](FM-083-nothing-measures-how-well-a-skill-does-its-work-only-its.md) found the same gap for skills: their
structure and proof are checked, but not how well they do their work.

## Done when

- [ ] The harness runs a first set of scenarios from the failures of 29 October, on Claude Code and on Codex, three
  times each, sealed, and writes the compare report.
- [ ] Its gate is red on a planted regression, and green on a planted flaky case.
- [ ] A missing result counts as an error.

## Ship log

| Date | Event |
|---|---|
| 2026-10-29 | Filed for v0.20.x, on the Owner's word of 29 October. Records only. |
