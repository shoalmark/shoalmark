---
id: FM-020
kind-of-problem: obvious
status: In Progress
considered: FM-002, FM-006, FM-016
tags: bug
next: review
hook: "The Owner typed one tracker's id into the board's search and got seventeen rows back, not the one tracker he asked for. He read it as the search not filtering at all."
---

# FM-020 — Searching the board for a whole id shows every tracker that links to it

## What is true now

**Built 2026-09-23 on `fix/0.17.5-one-id-one-row-and-an-empty-bucket-says-why`, for 0.17.5; open for review, not
merged.** The Principal chose the fix. In `draw()`, a query that is exactly one known id (trimmed, any case) is that
tracker alone: `exact=!hood&&byId.get(q.toUpperCase())`, and the row filter reads `hood ? neighbourhood : exact ? that
tracker : the substring match as before`. Like `~ID`, it shows the tracker whether or not it is open, and the counter
names it as itself (`1 tracker · <id>`, the label `count.id`), never as *open* (the Reviewer's R1). The hint says
*an id alone = its row · ~ID = its neighbours* (German: *eine Id allein = nur dieser Eintrag · ~Id = seine Nachbarn*).

| check | result |
|---|---|
| Chrome: MSR-002 links to MSR-001; `#MSR-001` and `#msr-001 ` | MSR-001 alone, counter `1 trackers`. On 0.17.4: MSR-001 and MSR-002, `2 trackers` (fails, as it should) |
| Chrome controls: `#~MSR-001` · `#MSR-00` · `#stock` | both neighbours · all three by substring · both title matches. The same on 0.17.4 and now |
| `test_core.py`, for a machine without a browser | the filter and the hint are in the page; fails on 0.17.4 |

**What is left:** review, merge, the tag.

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
| 2026-09-23 | R1: the counter over an id searched alone says `1 tracker · <id>`; a Chrome check searches a Shipped id in the story view with *open* pressed (it read `1 open` at `8402732`). |
| 2026-09-23 | Built: a whole id alone is its row; `~ID`, a partial id and words unchanged; two Chrome checks and a string check, shown to fail on 0.17.4. |
| 2026-09-23 | Filed. |
