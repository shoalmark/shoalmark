---
id: FM-001
status: Proposed
considered: none
next: build
hook: "fathom-mark 0.1.0 was cut out of a larger repository's tracker generator on 2026-09-21 — and that repository still runs its own 1,900-line copy. Two tools under one idea diverge with every fix. Port it onto this core, with its release axis kept as an extension around the core, and delete the copy."
---

# FM-001 — The repository it was cut from still runs its own copy

## What is true now

**Filed 2026-09-21; nothing is built.** The core here was cut by script from the origin's generator the same
day: 18 of its 49 functions touched something specific to that repository — a release-target registry, a deploy
(`Live`) column derived from submodule tags, product-area rosters — and all of it was left behind. What came
across is the schema and its gate, a filing looks first, the triage pass, the board. 36 checks, each in a
throwaway repository. The origin keeps running its own copy until this lands; every fix made in one is owed to
the other until then.

## Why

The Owner chose *its own repository from day one* knowing the cost: two diverging copies until the origin is
ported. This tracker is that cost, written down.

## What it needs

- An **extension seam** in the core, which has none today: extra front-matter keys with their shapes, extra
  lints, extra INDEX columns and page fields, contributed by a module the configuration names. The origin's
  release axis (`target:` / `version:` / `Live` / product areas) becomes that module, living in the origin.
- The origin vendors a pinned copy and deletes its generator's core. **Proof, as for every sweep there:** its
  `INDEX.md` and board are byte-identical before and after.
- Its ~840-line test file splits the same way: core checks live here already; the release-axis checks stay there.

## Done when

The origin's generator is the extension module only, its gates are green on a vendored pin, and a fix to the
core is made in one place.

## Ship log

| Date | Event |
|---|---|
| 2026-09-21 | Filed with the first commit. |
