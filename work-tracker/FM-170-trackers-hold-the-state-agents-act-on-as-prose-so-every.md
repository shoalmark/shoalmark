---
id: FM-170
status: Proposed
considered: FM-139, FM-162, FM-168
tags: research
next: build
hook: "Trackers hold much of the state agents act on as prose: a row's release, what blocks what, the Done when items and their commits, an option list before it is put, when a rule or grant ends, rulings that bind seats. Agents read whole files to find it. The step is a measurement, not a design: sort the trackers into record and acting state, count each, name the readers, rank the kinds."
---

# FM-170 — trackers hold the state agents act on as prose, so every agent reads whole files to find it

## What is true now

**Drafted 2026-11-13 and filed 2026-11-16, Proposed, on the Owner's word of 13 November; nothing is built, and this
tracker measures before anything is designed.** A tracker's front matter carries its status, `next`, tags and open ask,
and the tool reads them as data. Much else that a seat or the tool acts on sits in prose: - which release a row belongs
to (FM-139 exists because v0.20.3's rows sat in three trackers); - what blocks what; - the Done when items, and the
commits that meet them; - an ask's options before it is put; - the date a rule or a grant ends; - rulings that bind
seats.

An agent finds that state by reading whole trackers. That costs tokens, and it invites misreads. A tracker's record
(why something was decided, what happened, the Owner's signed answers) is written for people, and prose is its
right layer.

## The step: a measurement, not a design

1. Sort the trackers on main, at a named commit, into two classes: **record** (history, reasons, the Owner's
   answers) and **acting state** (something a seat or the tool acts on, by its kind from the list above). Count the
   lines and characters of each class, per tracker and in all.
2. For each kind of acting state, name its readers (a seat, the Board, `--whoami`, the stand-up), and where the tool
   already reads it as data.
3. Rank the kinds by volume, by how often a misread of one shows in the trackers' history and in review findings, and
   by what a key in the front matter would cost. Cite each misread.
4. The result goes here with its method. A design, if any, follows as its own ask.

## Why

What the code or a check holds costs less to read, and is misread less, than what prose holds. The order is: the
codebase, static checks, verification, prose, review. Records are prose by nature; the state an agent acts on need
not be. FM-162 makes the same move for the acts a seat must never do, and FM-168 for a spec's conformance cases.

## Done when

- Every tracker on main at a named commit is sorted, with the counts per class and per kind, and the method beside
  them.
- Each kind of acting state has its readers named and its misreads cited, or "none found".
- The ranking is written here, and the Owner has it.

## Ship log

| Date | Event |
|---|---|
| 2026-11-16 | Filed, Proposed, with no ask: a measurement of the acting state trackers hold as prose, before any design. Records only. |
