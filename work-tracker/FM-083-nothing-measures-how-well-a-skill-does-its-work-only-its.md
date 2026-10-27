---
id: FM-083
status: Proposed
considered: FM-062, FM-065
tags: research
next: owner
hook: "nothing measures how well a skill does its work, only its structure and its proof"
ask: "Is FM-083's suite for skills allocated to v0.20.3, as FM-083's section The allocation, for the Owner sets out?"
ask-kind: ruling
ask-since: 2026-10-27
ask-options: "yes, v0.20.3 | no: a later release"
ask-proposal: "yes, v0.20.3"
---

# FM-083 — nothing measures how well a skill does its work, only its structure and its proof

## What is true now

**Filed 2026-10-27, Proposed, on the Owner's word of 27 October as relayed by the Auditor; nothing is built.** The
tests of `/find-drift` and `/prune-drift` on the v0.20.2 lane check a skill's files and its proof. Nothing measures
what an agent does when it runs the skill. The Owner's design words: the score is a rubric; after its run, the agent
states in its own words how well it performed the skill, and how confident it is; and every harness is covered.

Before any suite, the Owner runs both skills by hand on Claude Code and on Codex, once both are on the v0.20.2 lane.
Its scores come here.

## The design, as proposed

1. **One case, the same on every harness, as plain files:** a prompt, a fixture repository at a fixed sha, a sealed
   answer key, and a rubric of three to six criteria, written before the run.
   - What can be counted is counted. The rest is judged by a model of another family, and a person checks the judge.
   - No case name says eval, test or judge.
2. **A fresh session per run.** After the skill finishes, a second turn asks for a self-assessment: an overall score
   from 0 to 100 %, with its reasons in its own words; a confidence for each finding; and what it skipped.
   - The self-assessment never counts toward the score.
   - It gives two measures: calibration, each confidence against the finding's labelled outcome; and unbacked claims,
     each claim against the transcript.
3. **A thin runner per harness,** reading that harness's own JSON output: `claude -p --output-format stream-json`, and
   `codex exec --json`. `claude plugin eval` is one runner, always with `--no-publish`. No runner reads a harness's
   session store.
4. **Never a CI gate.** The seat that changes a skill never writes or sees its cases. Some fixtures are held out. The
   Owner sets the thresholds and a cost ceiling.
5. **Its source** is [pstack's eval playbook](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/eval.md).

## Why

A skill's files can be right while the agent running it misses what it should find, or claims work it never did.
Tests of structure and proof see neither. A self-assessment set against the labels also shows whether an agent knows
when it is wrong.

## Done when

- One case each for `/find-drift` and `/prune-drift` runs on Claude Code and on Codex, with held-out fixtures. Each
  run is scored by its rubric, with its calibration and unbacked claims beside the score.
- The runners read only each harness's JSON output, and none is a CI gate.
- The Owner has set the thresholds and the cost ceiling.

## The allocation, for the Owner

- **The question:** is the suite allocated to v0.20.3?
- **The proposal:** yes. v0.20.2 ships as signed, and the suite measures both skills once they have shipped.
- **The options:** yes, v0.20.3; or no, a later release.

## Ship log

| Date | Event |
|---|---|
| 2026-10-27 | Filed, Proposed, on the Owner's word of 27 October, with one ruling ask: its allocation to v0.20.3. |
