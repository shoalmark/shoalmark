---
id: FM-100
status: Proposed
considered: FM-030, FM-088, FM-095
tags: process
blocked-by: FM-104
hook: "The stand-up prompt is code today, and English on every board, while the Board's own words already come from the language pack. It moves into the pack as STAND-UP.md, in the Board's language, with English when the pack has none, and the person edits it with their own signed commit, while no seat can."
---

# FM-100 — the stand-up prompt is code and English on every board, while the Board's words come from the language pack

## What is true now

**2026-10-30 — where this tracker's files go comes from
[FM-104](FM-104-the-person-s-own-files-are-spread-over-the-repository-and.md).** It waits on that decision, on the
Owner's word of 30 October, and nothing of it is built before it.

**Filed 2026-10-30 for v0.20.3; nothing is built.** On the Owner's word of 30 October: the stand-up prompt is localised
to the Board's language, with English as the fallback, and the German pack takes it as `STAND-UP.md`.

- **What is true today:**
  - The stand-up prompt is code, and English on every board.
  - The Board's words already come from the language pack: `examples/de/` holds `labels.yaml`, `TEMPLATE.md` and
    `TRIAGE.md`.
  - ADOPT has its language twins.
- **Where this comes from:** the stand-up prompt's growth in v0.20.2, part A, ships in English as built. Its part B, the
  prompt in the Board's language, moves here.
- **STAND-UP.md is the person's own:** the Owner of the repository edits it freely, with their own signed commit, as
  they sign an answer; the gate refuses a change any seat makes. "The Owner" here is the product's role, the person
  in charge of a repository.
- **Open, for its design:** whether the close-out prompt takes the same form, and what it is called.

## Why

A person who reads the Board in their own language should be handed a prompt in that language too. And a prompt the
Board copies into a session is words a seat could plant, so only the Owner should change them.

## Done when

- [ ] The Board copies `<tracker dir>/STAND-UP.md`, which `--init` writes in the Board's language, for the repository's
  own setup only: forge, local git, Subversion or a plain folder. Where the pack has none, it is English, and the
  Board says so.
- [ ] The German pack holds `examples/de/STAND-UP.md`.
- [ ] The languages agree in their fill-in fields, steps and code blocks, checked as ADOPT's twins are. An unknown field
  is refused, and every value still passes `day_value_problem`.
- [ ] `STAND-UP.md` is the person's own: the Owner of the repository edits it freely, with their own signed commit, as
  they sign an answer. The gate refuses a change any seat makes, with a class test and its mutant, so that no seat can
  plant words the Board hands on.
- [ ] The class test pins the shipped defaults.

## Ship log

| Date | Event |
|---|---|
| 2026-10-30 | Blocked by FM-104, which decides where the person's files live, on the Owner's word of 30 October. Records only. |
| 2026-10-30 | Filed for v0.20.3, on the Owner's word of 30 October. Records only. |
