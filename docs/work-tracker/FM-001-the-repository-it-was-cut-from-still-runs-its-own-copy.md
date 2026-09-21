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

- **The seam exists since 0.4.0 — a deriver by convention** (`<tracker dir>/derive`), proven before it was merged against
  the origin's 501 trackers: 0 differing cells, its six refusals intact, its release view identical in a browser bar the
  header words, its 19 roster files byte-identical — [the R&D record](evidence/FM-001/seam-bprime-rd.md), with the
  [deriver the spike ran](evidence/FM-001/spike/origin-release-axis.derive.py) (128 lines). **Left for the port itself:**
  the *work packages* roll-up (it leaves `INDEX.md` for a generated file), two header notes, and the
  `--allow-missing-submodules` override, which a deriver can only take from the environment.
- **The project-key ids go back with it — ruled by the Owner on 2026-09-21, parked the same hour (*"mark this
  for later"*), nothing built:** the origin's existing trackers keep their ids forever (the rule that motivates
  the change forbids renaming them); new filings carry the key **`PD`**, the counter starts at **400** — above
  every existing number, so a bare spoken number stays unambiguous; its gate refuses a new id under the old
  prefixes from the first unfiled number on. Touches its generator's kinds and page patterns, one docs-lint
  pattern, and four pages of its agent contract that spell the old convention — under a line ceiling with
  eight lines of headroom.
- The origin vendors a pinned copy and deletes its generator's core. **Proof, as for every sweep there:** its
  `INDEX.md` and board are byte-identical before and after.
- Its ~840-line test file splits the same way: core checks live here already; the release-axis checks stay there.

## Done when

The origin's generator is the extension module only, its gates are green on a vendored pin, and a fix to the
core is made in one place.

## Ship log

| Date | Event |
|---|---|
| 2026-09-21 | **0.4.0 — the seam, merged on the Owner's ruling after R&D.** What is left of this tracker is the port itself. |
| 2026-09-21 | **The debt's first instalment, the same day:** 0.2.1 fixed six things found on a second repository. Three of them are in the origin's copy too and are now owed there — a hook's quotation marks in the INDEX row, a tracker's own id linking to itself in the viewer, `--related` reading only a–z. |
| 2026-09-21 | Filed with the first commit. |
