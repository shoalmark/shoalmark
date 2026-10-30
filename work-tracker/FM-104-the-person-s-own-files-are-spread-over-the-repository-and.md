---
id: FM-104
status: Proposed
considered: FM-088, FM-095, FM-100, FM-026, FM-042
tags: seamanship
hook: "The person's own files sit in three places today, and three v0.20.3 candidates would each add more. They should live in one home the person reaches easily, under fixed names, so that the person sees what is theirs to edit. Rank 1 when v0.20.3 starts, on the Owner's word."
---

# FM-104 — the person's own files are spread over the repository, and three more would join them

## What is true now

**Filed 2026-10-30 for v0.20.3; nothing is built.** On the Owner's word of 30 October: the files the person edits
should live in one place they reach easily, not spread over the code base. Convention over configuration has to be
weighed, and the question needs time to think it through properly. The Owner's word on its rank: **rank 1 when v0.20.3
starts.** It stays unranked until then.

- **Where the person's files sit today:**
  - the root holds `shoalmark.toml`;
  - the tracker folder holds `TRIAGE.md` and `allowed_signers`;
  - a brand folder holds the labels.
- **What three v0.20.3 candidates would add:** `RULES.md`
  ([FM-095](FM-095-the-owner-s-rulings-live-in-chat-memories-and-briefs-not-in.md)), `STAND-UP.md`
  ([FM-100](FM-100-the-stand-up-prompt-is-code-and-english-on-every-board-while.md)), and `memory/`
  ([FM-088](FM-088-the-team-s-lessons-live-only-in-each-harness-s-local-memory.md)). Each waits on this tracker for
  where its files go.
- **Nothing is built before the Owner decides.**

## Why

A person can only keep what they can find. One home under fixed names lets them see, in one place, every file that is
theirs to edit, and leaves no setting to learn.

## Done when

- [ ] An inventory of every file the person reads or edits, and of every file the tool generates.
- [ ] The options, each with its migration path for an existing repository:
  - the tracker folder as the home, with the trackers moved into a folder of their own;
  - or a visible folder of its own.
  - A hidden folder is out, by the Owner's "easy access".
- [ ] The principles:
  - one home;
  - fixed names, convention over configuration;
  - who owns each file is visible from where it sits;
  - language packs copy into the home;
  - harness files stay where harnesses look, and point to it;
  - one Board entry point to it.
- [ ] A design round with the Designer, and the Owner's decision in a sitting.
- [ ] The layout's own tracker, filed to build it.

## Ship log

| Date | Event |
|---|---|
| 2026-10-30 | Tagged `seamanship`, on the Owner's word of 30 October. Records only. |
| 2026-10-30 | Filed for v0.20.3, rank 1 at its start, on the Owner's word of 30 October. Records only. |
