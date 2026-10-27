---
id: FM-082
status: Proposed
considered: FM-062, FM-050
tags: process
hook: "the Board and --standup do not list an ask that sits on a branch not on main"
---

# FM-082 — the Board and --standup do not list an ask that sits on a branch not on main

## What is true now

**2026-10-27 — design input, not ruled, from the Auditor's relay of 27 October.** The Board's part would be one section for what is on its way and not yet on main: asks waiting on branches not merged, open pull requests with their CI (FM-084), and one line that names what unblocks them. It is drawn from a snapshot that `--queue` leaves, shown with the time it was read, so the Board itself stays offline. FM-082 stays unallocated.

**Filed 2026-10-27, Proposed, as a candidate check from FM-062's entry of 27 October, on the Auditor's word, for the Owner's allocation; nothing is built.**

An ask in a tracker's front matter on a branch the default branch never received does not show on the Board or in `--standup`. The records pass of 21 October held two such asks, and the Board never showed them.

## Why

An ask the person never sees cannot be answered, and its work waits unseen.

## Done when

- The Board and `--standup` list every ask on a local branch not on the default branch, read from local refs, with no network, each with its branch and sha.

## Ship log

| Date | Event |
|---|---|
| 2026-10-27 | Filed, Proposed, a candidate check from FM-062's entry of 27 October, for the Owner's allocation. |
| 2026-10-27 | Design input, not ruled: one Board section for what is on its way and not yet on main, drawn from a snapshot `--queue` leaves; still unallocated. |
