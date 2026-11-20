---
id: FM-182
status: Proposed
considered: FM-033, FM-176
tags: bug
hook: "The contract that --init writes into an adopter's AGENTS.md says branches carry the id as `feat/fm-012-slug`; the gate reads a branch's tracker only from `fm/012-…`. A branch named as the contract says names no tracker, and the refusal names a form the contract never gives. Proposed: one form, read where the contract writes it."
---

# FM-182 — the contract names branches `feat/fm-012-slug`, but the gate reads a tracker only from `fm/012-…`

Seat: the Planner (a1730572) · filed 2026-11-20, on the coordinator's word of that day.

## What is true now

**Filed 2026-11-20, Proposed; nothing is built.** Three forms of a branch name are in use, and the tool reads one. At
`c7e27fa`:

- **The contract's form, `<type>/<kind>-<NNN>-slug`:** the work-tracker contract, which `--init` writes between its
  markers into an adopter's `AGENTS.md`, says "Branches carry the id: `feat/{lkey}-012-slug`, `fix/{lkey}-013-slug`."
  (`shoalmark.py` line 11724). This repository's own copy reads `feat/fm-012-slug`, `fix/fm-013-slug` (`AGENTS.md`
  line 16). The first-run hint repeats the form: "branches carry the id: `feat/…-001-slug`" (`shoalmark.py` line
  12489).
- **The gate's form, `<kind>/<NNN>-…`:** `branch_tracker` (`shoalmark.py` lines 8992 to 8996) reads a branch's tracker
  only from a name such as `fm/029-…`: the kind, a slash, the number. Its refusal names that form, "its branch `…`
  names none (`<kind>/<NNN>-…`)" (line 9107), and so do two help lines (lines 6434 and 10970).
- **The form this repository's own lanes use, `lane/fm-NNN-…`:** for example `lane/fm-172-answer-changes-b`, the
  branch of pull request #311.
- **What each gives:** by `branch_tracker`'s pattern, `fm/029-slug` gives FM-029; `feat/fm-012-slug`,
  `fix/fm-013-slug`, `feat/fm-001-slug` and `lane/fm-172-answer-changes-b` give none.
- **Where it bites:** a commit is judged under the trackers its subject names, else its branch's (`named_trackers`, line
  8999). A commit whose subject names no id, on a branch named as the contract says, is refused as naming no tracker
  (lines 9105 to 9107), and the refusal names a form the contract never gives. The refusal comes only where the gate
  judges the commit: `judged_before_build` is true, which is off by default (line 83) and on in this repository
  (`shoalmark.toml` line 5); the commit changes a path outside the tracker folder and is not an Owner's
  (`judge_commits`, lines 9060 to 9068); and its branch is not the default branch (lines 9140 to 9142). A records-only
  commit, an Owner's commit, or one whose subject names an id is not refused.

## Why

The contract is what an agent reads; the gate is what it meets. When they name different forms, an agent that follows
the contract, in a repository whose gate is on, is refused for a build commit whose subject names no id, and the refusal
teaches it a third way to read the rule.

## The decision, proposed

One branch form, read where the contract writes it:

1. `branch_tracker` reads the id as the contract writes it: a path segment that starts `<kind>-<NNN>`, after a prefix
   such as `feat/`, `fix/` or `lane/`. It keeps reading today's `<kind>/<NNN>-…`, so no branch that names a tracker
   today stops naming it.
2. The refusal and the two help lines name the contract's form, with today's form beside it.
3. The contract's sentence stays as it is.

Set aside: changing the contract to the gate's form. The contract's sentence sits in every adopter's `AGENTS.md`, and
a change there reaches each copy only when its owner runs `--init` again; the code is one place.

## Done when

- [ ] A branch named as the contract says (`feat/fm-012-slug`), and a lane branch (`lane/fm-012-slug`), give their
  tracker; `fm/012-slug` still does.
- [ ] The refusal and the two help lines name the contract's form.
- [ ] A row for each form, with a mutant that drops the contract's form, killed.

## Ship log

| Date | What |
|---|---|
| 2026-11-20 | The refusal's conditions stated, in *Where it bites* and *Why*: the gate on, a commit outside the tracker folder that is not an Owner's, off the default branch. Records only. |
| 2026-11-20 | Filed, Proposed. |
