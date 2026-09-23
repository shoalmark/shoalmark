---
id: FM-020
status: Proposed
considered: FM-002, FM-006, FM-016
tags: bug
next: build
hook: "The Owner typed one tracker's id into the board's search and got seventeen rows back, not the one tracker he asked for. He read it as the search not filtering at all."
---

# FM-020 — Searching the board for a whole id shows every tracker that links to it

## What is true now

**Filed 2026-09-23; nothing is built.** The Principal chose the fix: a whole id alone shows that one row.

**Why seventeen.** `draw()` (`shoalmark.py:1203–1206` at 0.17.4) matches every typed word as a lower-case substring
of about thirty fields of a row joined together. One of them is `t[12]`: the ids of every tracker the row's body
links to (`TRACKER_LINK_RE`, :220, into the row at :1590). So a whole id matches its own row **and every row that
links to it**. The search does hide the rows that do not match, and the counts do update: what it finds is every
reference.

**Reproduced** by the Research seat on PortDive's board (505 trackers, 0.17.4, headless Chrome): `FEAT-161` in the
*by suite · all* view shows 24 rows, 17 of them under *agentic-portfolios*. 16 of those 17 match only through the
linked ids. 448 of the 505 ids, searched whole, return more rows than their own. On shoalmark's own board the effect
is small: `FM-012` shows FM-012 and FM-018.

## Why

A person who types an id is looking for that tracker. The rows that link to it answer a different question, and
`~ID` already answers that one in a single keystroke.

## Done when

- A query that is exactly one known id (trimmed, any case) shows that tracker alone, under its group header, with
  the counts updated as they are now.
- `~ID` still shows the neighbourhood, and a partial id (`FM-01`) or a query of several words still matches by
  substring.
- The search hint says that an id alone shows its row and `~ID` its neighbours, in English and in German.
- A check renders the board in Chrome: B links to A; `A` gives 1 row, `~A` gives both, a partial id matches by
  substring. The check is shown to fail on 0.17.4.

## Ship log

| Date | Event |
|---|---|
| 2026-09-23 | Filed. |
