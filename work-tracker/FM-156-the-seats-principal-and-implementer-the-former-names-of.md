---
id: FM-156
status: Proposed
considered: FM-024, FM-010, FM-015
tags: process
next: build
hook: "The seats principal and implementer, the former names of planner and builder, still read as seats in configuration"
---

# FM-156 — The seats principal and implementer, the former names of planner and builder, still read as seats in configuration

Seat: the Planner (27f31560) · filed 2026-11-12, on the Auditor's word of that day.

## What is true now

**Filed 2026-11-12; nothing is built.** The seats have been `planner` and `builder` since 0.19.0 (FM-024). Their former
names, `principal` and `implementer`, still work as seats in `shoalmark.toml`, and that is drift: one seat with two
names in configuration. At main `e75e9a0` they live in:
- **`shoalmark.py`:**
  - `BUILTIN_RIGHTS` (lines 785–787) gives `principal` the planner's rights and `implementer` the builder's;
  - `FORMER_NAMES` (line 8798) and `session_names` read them in session ids;
  - the `[seats]` help (lines 6321–6324) says both "still read and hold the same";
  - the comment at line 92 gives `"principal@seat"` as its example.
- **The documentation:**
  - README §*Seats* (around lines 402–404 and 534);
  - `docs/setup.md` (line 72) and `docs/de/setup.md` (line 73);
  - the seats page's opening, `docs/seats/index.md` line 6: "`principal` and `implementer` are their former names and
    still work".
- **The suite:** about 320 lines of `test_shoalmark.py` name them.

**Order:** this lands after the pull request now changing the seats page's opening, because both change its first
paragraph.

**The Builder's question, settled with evidence before the build: what still reads the old names in the record?**
Session ids already in history carry them (`<id>/implementer-<n>`): 227 lines under `work-tracker/` name such sessions.
This repository's own `shoalmark.toml` also lists `principal@seat` and `implementer@seat` as old addresses under
`planner` and `builder`. Those are identities, not seats, and `session_names` already reads a label from every
`<name>@seat` address.
- **The Auditor recommends** keeping old session ids read as the seat's, since reading the past grants nothing, and
  retiring only the configuration names.
- **The Builder shows** what reads `<id>/implementer-<n>` and `principal@seat` after the change, with and without
  `FORMER_NAMES`, and runs this repository's history through it.

**Tier: critical (seats and rights).** An Opus Builder, and an independent review.

## Why

A seat has one name in configuration. Two spellings that hold the same rights are a second way to write the same thing,
and a reader of `shoalmark.toml` meets both. Retiring the configuration names closes that. Refusing them out loud
matters, because a silent fallback is worse: a `[seats] principal` line would become an unknown seat with no rights,
and the rights it was meant to carry would go missing without a word.

## Done when

- a `[seats]` or `[rights]` line named `principal` or `implementer` is refused when the configuration is read, exit 1
  as every configuration refusal, with one line that names `planner` or `builder`; a test for each of the four lines;
- `BUILTIN_RIGHTS` holds the Owner and the three built-in seats only;
- the `[seats]` help, the README, both setup pages and the seats page name only `planner` and `builder`, and no
  `"principal@seat"` example is left;
- the Builder's question is settled with evidence, and the history this repository holds still reads as before, or
  the change says what it no longer reads and why;
- the suite passes, with every alias check rewritten or removed and each removal named in the change;
- an independent review is READY.

## Ship log

| Date | Event |
|---|---|
| 2026-11-12 | Filed. |
