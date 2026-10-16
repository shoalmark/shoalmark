---
id: FM-050
status: Proposed
considered: FM-027, FM-008, FM-014, FM-016, FM-029, FM-030, FM-023
tags: process
next: wait
hook: "An ask has no id of its own, so an answer, the stand-up and the receipts cannot name the ask they mean"
---

# FM-050 — an ask has no id of its own, so an answer cannot name the ask it answers

## What is true now

**Filed 2026-10-15 as a design tracker; nothing is designed or built.**

- **Today:** a tracker holds at most one open ask, in its front matter. `--clear-ask` moves an answered exchange under
  `## Asks`, dated, with no id. An answer is tied to its ask only by its tracker and the ask's date.
- **Why now:** R4 makes an ordinary Owner-signed commit the canonical answer (FM-023's table of 2026-10-15: v0.20.1). That commit
  must name the ask it answers, so the id comes first. The receipts view counts asks too: the oldest waiting ask, the
  answers per sitting.
- **The design, as proposed:**
  - one open ask per tracker at a time, as today, and no limit on how many asks a tracker carries over its life;
  - the id is `<ITEM>-Q<n>`: the tracker's id, `-Q`, and a number counting that tracker's asks, as in `FM-023-Q2`;
  - an id is never reused: a withdrawn or replaced ask keeps its number, and the next ask takes the next one.
- **The design settles:**
  - where the id is written: the open ask's front matter, and the cleared exchange;
  - how asks already cleared under `## Asks` are numbered, without rewriting signed history;
  - how an answer commit names its ask, and what the gate refuses: an unknown id, an answered id, a reused number;
  - how two branches that each give one tracker a new ask cannot mint the same number (FM-027's lesson for tracker
    ids);
  - what the board, `--standup` and `--owner` print.
- **Tier: critical.** It decides which ask the Owner's verified word answers, so it is signing and rights. A critical
  Builder, a Reviewer in a session of its own, one CI run.
- **Order:** designed and reviewed, and ruled by the Owner, before R4 is built; R4 and the ids are built together.
- **Source:** an analysis of ask ids, recorded privately.

## Done when

- The design is written here, reviewed by an independent Reviewer, and ruled by the Owner.
- Built: every ask carries its id on the board and in `--standup` and `--owner`; an answer commit names it; the gate
  refuses an unknown, answered or reused id. One test covers the class: every way an id could be reused or mismatched,
  across two branches included.

## Ship log

| Date | Event |
|---|---|
| 2026-10-15 | Filed. |
