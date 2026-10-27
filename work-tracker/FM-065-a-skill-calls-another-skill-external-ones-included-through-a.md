---
id: FM-065
status: Proposed
considered: FM-062, FM-011, FM-009, FM-004
tags: process
next: build
hook: "a skill calls another skill, external ones included, through a contract that pins what it calls and checks what it gets back"
---

# FM-065 — a skill calls another skill, external ones included, through a contract that pins what it calls and checks what it gets back

## What is true now

**Filed 2026-10-19; nothing is designed or built.** The Owner's word of 19 October is recorded privately. The
contract lands in v0.20.2, so that the plugin is ready for external skills from its first release: the contract,
nothing less and nothing more for now. A design round comes first, then the Owner's ruling on the design, then the
build.

- **Today:** `/prune-drift` names its call of `/find-drift` in prose. It reads the newest report, and runs
  `/find-drift` first where none is fresh. That works because both skills share one set of conventions. A skill from
  outside the plugin brings its own inputs, requirements, outputs and completion rules. Installing it only makes its
  instructions available.
- **What lands in v0.20.2:**
  - **the contract's six parts:**
    - **identity:** the repository, the exact commit, the skill's entry point, and the hashes of the whole package,
      its scripts and schemas included;
    - **inputs:** the target revision, the paths in scope, the mode asked for, the budget, and the prior evidence the
      child may use;
    - **capabilities:** the tools, delegation, file-system access, network and execution isolation it needs;
    - **outputs:** the artifacts it must return, their formats, and the checks they pass before a parent uses them;
    - **completion:** whether the work completed, stopped partway, was blocked, or failed;
    - **provenance:** the parent's and the child's run ids, the version that ran, the input snapshot, the artifacts'
      hashes, the checks and the limits;
  - **a registration format** for each call, and **a check** of every registration;
  - **its first use:** `/prune-drift` calling `/find-drift`, in a commit of its own after `/prune-drift` is READY;
  - **synthetic child skills that prove it:**
    - changed package bytes are refused;
    - a stale result is refused;
    - a call cycle is found;
    - a child's budget is held;
    - a missing or invalid artifact never satisfies a dependency;
    - completion is judged apart from acceptance, both ways: a completed run with findings, and an incomplete run
      with none.
- **Not in v0.20.2:** running any external skill, an adapter or a pilot for one, and a security-scan skill. An
  external skill that executes target code needs an OS-enforced sandbox outside the Owner's user, which shoalmark
  does not have.
- **Completion is not acceptance.** A completed run can find something serious, and an interrupted one can find
  nothing. So a parent asks two questions, apart:
  - did the child finish the work and return valid evidence?
  - does that evidence meet the parent's acceptance rule?

  An exit code or an empty list of findings answers neither.
- **A playbook's steps table** names the skills its steps use and what each step depends on. It calls them through
  this contract, so the design covers it as a caller.
- **Tier: critical.** The contract decides which skill a parent trusts, and which result counts.

## Why

A skill that calls another must know exactly what it called, and whether what came back counts. Pins, hashes and a
record of what ran are how shoalmark already trusts its own tool. The same holds for skills.

## Done when

- The design is written here, reviewed by an independent critical Reviewer, and ruled by the Owner.
- The contract, its registration format and its check ship in v0.20.2's plugin. The synthetic children prove each case
  above, and each part is reviewed like code.
- `/prune-drift` calls `/find-drift` through it.

## Ship log

| Date | Event |
|---|---|
| 2026-10-19 | Filed by the Planner seat on the Owner's word of 19 October (recorded privately): the contract lands in v0.20.2, with a design round first. Nothing is designed or built. |
