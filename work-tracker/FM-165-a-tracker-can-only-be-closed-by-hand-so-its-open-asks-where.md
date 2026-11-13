---
id: FM-165
status: Proposed
considered: FM-008, FM-014, FM-027, FM-030, FM-050, FM-059, FM-115, FM-150, FM-164
tags: process
next: review
hook: "A tracker is closed by hand: a status, a line in its own words, and its open asks left waiting in the Owner's queue. Nothing records where its work went when it moves to another repository. The proposal: one command, --close, that writes the same record every time, withdraws the open asks, and names a moved-to or superseding tracker. Who may close is for a design round, with the question drafted."
ask: "Who may close a tracker with --close: the Owner alone, or also a seat whose [rights] entry holds close, and if a seat may, what must its close carry beyond the reason and the target?"
ask-kind: ruling
ask-options: "the Owner alone | the Owner, and a seat whose [rights] entry holds close | the Owner, and a seat's close waits for the Owner's look"
---

# FM-165 — a tracker can only be closed by hand, so its open asks, where its work went and why it closed are not recorded the same way twice

Seat: the Planner (27f31560) · filed 2026-11-13, on the Auditor's word of that day.

## What is true now

**Filed 2026-11-13, Proposed, with no release; nothing is built.** Its question on who may close is drafted, with no id
until it is put, for a design round (`next: review`).

- **The base today:**
  - `status:` is set by "the seat that changes it"
    ([`shoalmark.py` L984](https://github.com/shoalmark/shoalmark/blob/c1e1cea2be92ff433933732a077dacfcb9079e8d/shoalmark.py#L984)),
    and `Closed` covers superseded, declined and won't-fix
    ([L1091](https://github.com/shoalmark/shoalmark/blob/c1e1cea2be92ff433933732a077dacfcb9079e8d/shoalmark.py#L1091)).
  - The `close` right is "setting a terminal status — saying work is over"
    ([L782](https://github.com/shoalmark/shoalmark/blob/c1e1cea2be92ff433933732a077dacfcb9079e8d/shoalmark.py#L782)),
    and the planner holds it built in, beside the Owner
    ([L785](https://github.com/shoalmark/shoalmark/blob/c1e1cea2be92ff433933732a077dacfcb9079e8d/shoalmark.py#L785)).
  - A close is written by hand. `--triage`'s verdict `close` leaves "`status: Closed` and the `Closed —` line" to write
    ([L6077–L6078](https://github.com/shoalmark/shoalmark/blob/c1e1cea2be92ff433933732a077dacfcb9079e8d/shoalmark.py#L6077-L6078)),
    and a merge leaves "Closed — merged into [ID](file), <date>"
    ([L5825](https://github.com/shoalmark/shoalmark/blob/c1e1cea2be92ff433933732a077dacfcb9079e8d/shoalmark.py#L5825)).
  - An open ask is withdrawn one at a time, with `--clear-ask <id> <next move>`
    ([L10847](https://github.com/shoalmark/shoalmark/blob/c1e1cea2be92ff433933732a077dacfcb9079e8d/shoalmark.py#L10847)),
    and the Owner takes back an answer with `--revoke`
    ([L10840](https://github.com/shoalmark/shoalmark/blob/c1e1cea2be92ff433933732a077dacfcb9079e8d/shoalmark.py#L10840)).
  - Nothing records where a closed tracker's work went when it moves to another repository.
- **The command, as proposed:**
  - `--close <ids…> --reason "<text>"` closes one or more trackers in one commit.
  - `--moved-to <owner/repo>[#<id>]` names a tracker in another repository, including one not yet filed. The first
    use is trackers moving to shoalmark/chart.
  - `--superseded-by <id>` names the tracker that takes its place.
  - Open asks on a closed tracker are withdrawn in the same commit, each with its record under `## Asks`, as
    `--clear-ask` writes one.
  - The Board gets a Close action beside Answer.
  - A closed tracker is never reopened: new work files a new tracker that cites it. Ids are never reused.
- **Open: who may close.** The Owner closes when they see fit. Whether and how a seat holds a right to close, through
  a `[rights]` entry, and what its close must carry, is for a design round. The question above is a draft.

## Why

A close by hand ends each tracker in its own words: a status, a line, perhaps a reason, perhaps where the work went.
Its open asks stay in the Owner's queue for work that is over. One command writes the same record every time, and an
id that never comes back keeps every citation of it true.

## Decisions, for the design round

1. **The command and its options,** as above.
2. **The record a close writes:** `status: Closed`; one `Closed —` line with the date, the reason and, where given, the
   moved-to target or the superseding tracker; and a record under `## Asks` for each withdrawn ask.
3. **The Board's Close action** prepares the close as its Answer action prepares an answer, and the same command runs
   it.
4. **Never reopened, never reused:** the gate refuses a move from `Closed` to an open status, with a class test and its
   mutant. `--new` already takes only a free id on its branch;
   [FM-027](FM-027-the-next-free-id-is-claimed-on-the-server-not-guessed-on-a-branch.md) holds the server's side.
5. **Who may close:** the drafted question. Today's base is the `close` right, which the planner holds built in.
6. **The review is critical:** it touches rights.

No release is named.

## Done when

Each item names its commit or pull request when it lands.

- [ ] **The design round** settles who may close and what a seat's close carries; the question is put, and the Owner
  has answered it.
- [ ] **`--close`** with `--reason`, `--moved-to` and `--superseded-by`, several ids in one commit, each with its
  tests.
- [ ] **Open asks** on a closed tracker are withdrawn in the same commit, each with its record, with a test.
- [ ] **The gate** refuses a closed tracker reopened, with a class test and its mutant.
- [ ] **The Board's Close action,** with its labels in English and German.
- [ ] **README and the docs** describe the command, with their German twins.
- [ ] **The critical review is READY.**

## Ship log

| Date | Event |
|---|---|
| 2026-11-13 | Filed, Proposed, with no release; its question on who may close drafted for a design round. Records only. |
