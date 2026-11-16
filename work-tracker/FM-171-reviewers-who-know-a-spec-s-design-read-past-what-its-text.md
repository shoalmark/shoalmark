---
id: FM-171
status: Proposed
considered: FM-083, FM-168
tags: process
next: wait
hook: "Reviewers who know a spec's design read past what its text leaves out. A fresh session given only sealanes/1's text built a small executable model and found outcome-changing gaps no reviewer had reported. The proposal: a skill in shoalmark/skills that builds such a model from a spec's text alone, measured as FM-083 has it. The build waits for a run on a second spec."
---

# FM-171 — reviewers who know a spec's design read past what its text leaves out, and nothing builds from the text alone

## What is true now

**Drafted 2026-11-13 and filed 2026-11-16, Proposed, on the Owner's word of 13 November; nothing is built, and the build
waits for a run on a second spec.**

- **What happened on sealanes/1's first-edition text:**
  - A fresh session was given only the text and asked to build, not to review. It wrote a small executable model of
    the spec's change control, with one function per defined term, and used the spec's own histories and cases as
    fixtures.
  - In 17 minutes it ran 133 fixtures, 132 passing. It found four problems that change an outcome, three guesses and
    one contradiction among the spec's rules, none of which the reviewer of the same revision had reported.
  - It handed each back as a history on which two honest implementations differ, never as wording for the text.
- **What the reviewers showed:** a reviewer who knows the design supplies what the text omits without noticing. On
  the first revision, a reviewer who knew the design missed sixteen of a stranger's twenty-seven findings, fourteen of
  them silences: a grammar, a default, which field, which clock.
- **Where it runs next:** a second run on the next revision is under way. A run on hail/1, a different spec of about
  three times the size, tests whether the procedure holds beyond one spec. The skill is written from what those runs
  show.

## The design, as proposed

1. **A skill in shoalmark/skills,** under `plugins/shoalmark/skills/`, beside `find-drift` and `prune-drift`. Its name
   is settled when it is built (working name `spec-model`).
2. **Independence comes first.** It runs only in a session that has not seen the spec's drafting or its reviews, in
   a fresh folder whose only input is the spec text, and the specs it cites where it names them. A session that has
   seen them says so and stops. It seals its plan before it reads the spec.
3. **What it builds:** a model that is not normative, in a language's standard library alone, run in isolation:
   - one function per defined term, each citing its lines;
   - fixtures taken from the spec's own histories, examples and cases, each stating the result the text gives, with
     its lines;
   - the fixtures run, and the output kept as printed.
4. **What it hands back:**
   - every guess: a fixture on which two honest choices give different results;
   - every contradiction: a fixture whose stated result does not follow, or two rules giving one history two results;
   - any route round the spec's own authority, as the most severe class;
   - a verdict (builds, builds with guesses, cannot build) and a hash manifest.

   It never proposes wording for the spec.
5. **The concordance:** a script that lists every use of each term the spec's terminology defines, including a term
   split over a line end, so that a fix to a definition re-reads every use. Whether it ships in this skill or in
   `find-drift` is settled when it is built.
6. **Measured as FM-083 has it:**
   - one case: a small spec with planted gaps and a sealed answer key, run on two harnesses;
   - scored by gaps found and missed, and by claims the run did not back;
   - never a CI gate.
7. **Never:** the network, another repository, a test suite or the spec's own tools. It stops on a secret, as
   `find-drift` does.

## Why

A reader who knows the design fills a spec's silences without noticing; a builder who has only the text cannot. The
order of what costs less and is misread less runs: the codebase, static checks, verification, prose, review. A model
moves a spec's rules from prose toward verification, and its fixtures are a first step toward FM-168's plain-file
conformance cases.

## Done when

- The procedure has run by hand on a second spec, with its record filed.
- The skill is in shoalmark/skills with its eval case, built from a brief and reviewed at the critical tier, since
  `skills/**` is a critical path.
- The eval case has been run on two harnesses, and the Owner has the scores.

## Ship log

| Date | Event |
|---|---|
| 2026-11-16 | Filed, Proposed, with no ask: a skill that builds a model of a spec from its text alone; the build waits for a run on a second spec. Records only. |
