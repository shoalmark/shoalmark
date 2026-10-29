---
id: FM-090
status: Proposed
considered: FM-006, FM-086
tags: process
hook: "The site check that BF-95 added reads Markdown the way the site's build does, and its review found edge cases that no page holds yet. Each one goes here with its fixture, instead of opening a new round on the lane that made the check, so the check grows only when a page needs it or a release takes this tracker."
---

# FM-090 — the site check's reading of Markdown has edge cases no page holds yet, each with its fixture

## What is true now

**Filed 2026-10-29 for v0.20.3; nothing is built.** BF-95 (`fm/006-bf95-code-blocks`, FM-006) gave
`scripts/check_site.py` a check that every fenced block builds to a `<pre>` and that no built page shows a literal
fence. Its standard review ran four rounds. On the Auditor's word of 29 October, the last round set a stop rule: an edge
case in the check's reading of Markdown that no page of the site holds comes here, with its fixture, and opens no new
round. Only a P2 or higher, or a case a real page holds, reopens the lane.

**The cases so far:**
- **RV-3991 (P3):** no control tests that the include patterns end at the line's end. A mutant that allows trailing
  blanks again passes every test.
  - **The fixture:** a page `trailing.md` holding `--8<-- "inc.md"` with one trailing space.
  - **What the snippets build makes of it:** `trailing.html`, with that line as a paragraph and no `<pre>`.
  - **What the review showed:** the check at its head passes the fixture, and the mutant, which expects inc.md's three
    blocks there, is refused.

## Why

A check that copies a build's reading of Markdown can always be made a little closer to it. Rounds that change nothing a
reader sees cost a lane its release. Kept here, each case waits until a page needs it or a release takes it, and its
fixture says exactly what to build.

## Done when

- [ ] Each case listed above has its fixture in `scripts/test_check_site.py`. The fixture is red on the mutant it names,
  and green at the head.
- [ ] The built site is byte for byte unchanged by the commit that adds them.

## Ship log

| Date | Event |
|---|---|
| 2026-10-29 | Filed for v0.20.3, on the stop rule of BF-95's review, with RV-3991. Records only. |
