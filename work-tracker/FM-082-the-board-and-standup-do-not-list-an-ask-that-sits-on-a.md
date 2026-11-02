---
id: FM-082
status: Proposed
considered: FM-062, FM-050
tags: process
hook: "the Board and --standup do not list an ask that sits on a branch not on main"
---

# FM-082 — the Board and --standup do not list an ask that sits on a branch not on main

## What is true now

**2026-10-27 — design input, not ruled, from the Auditor's relay of 27 October: one Board section for what is on its way and not yet on main.** It carries what today's work found missing:

- beside each blocked item, the one line that names what unblocks it;
- the asks waiting on branches not merged into main;
- the open pull requests, each with its CI word from `--queue`'s snapshot (FM-084), and the time that snapshot was read.

It is drawn from the snapshot `--queue` leaves, so the Board itself stays offline. Two neighbours belong elsewhere: the digest's settled half goes to FM-005, and live sessions in progress stay with `--sessions`, with nothing filed for them now. FM-082 stays unallocated.

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
| 2026-10-27 | Design input, not ruled: one Board section for what is on its way and not yet on main, with what unblocks each item, the asks off main and the open pull requests with their CI, drawn from a snapshot `--queue` leaves. The digest's settled half goes to FM-005; live sessions stay with `--sessions`. Still unallocated. |
