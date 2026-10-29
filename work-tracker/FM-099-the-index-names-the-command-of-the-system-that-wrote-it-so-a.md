---
id: FM-099
status: Proposed
considered: FM-034, FM-059
tags: bug
triaged: 2026-10-29
next: wait
tier: P2
hook: "The generated INDEX names the command of the system that wrote it, `python` on Windows and `python3` elsewhere. So in a team that mixes them, every `--check` on the other system says the INDEX is STALE when no tracker changed. The INDEX must hold nothing of the machine that wrote it."
---

# FM-099 — the INDEX names the command of the system that wrote it, so a mixed team's check says it is stale

## What is true now

**Filed 2026-10-29 for v0.20.x, proposed for v0.20.3; nothing is built.** The Owner places it in a release. It was found
in S2's rebuild for [FM-059](FM-059-the-owner-answers-each-ask-in-a-view-of-its-own-and-a.md), whose test fixture met it
on CI's Windows jobs, and fixed there for the test alone.

- **What happens:** the INDEX's run line names the command of the system that generated it: `python shoalmark.py` on
  Windows, and `python3 shoalmark.py` elsewhere. `--check` compares the committed INDEX with what it would write itself.
  - **A mixed team:** an INDEX committed from macOS or Linux makes a Windows user's plain `python shoalmark.py --check`
    exit 3, "INDEX.md is STALE", though no tracker changed. The reverse fails the same way.
  - **A shared tree:** a working tree used both from WSL and from Windows meets it through the hooks' copy, which
    records the command of the system that installed it.
- **The workaround:** set `SHOALMARK_CMD` to the command the committed INDEX names. This repository's CI does so on
  every system.
- **The same class as [FM-034](FM-034-a-fresh-clone-s-check-says-the-index-is-stale-the-header.md):** there, the INDEX
  header carried a clone's own finding, and a fresh clone read STALE. FM-034 shipped and is not reopened. This is its
  sibling: the INDEX carries something of the machine that wrote it.

## Why

A false STALE teaches a person to regenerate and commit, and the next person on the other system then sees STALE the
other way. A check that a team cannot pass on both its systems is a check the team learns to ignore.

## Done when

- [ ] The INDEX holds nothing that depends on the machine, the system or the interpreter name that wrote it.
- [ ] A class test makes the INDEX under each of these and finds the same bytes:
  - `python` and `python3`;
  - LF and CRLF;
  - the signers file present and absent.
- [ ] A mutant that writes the local command back into the INDEX turns that test red.

## Ship log

| Date | Event |
|---|---|
| 2026-10-29 | Filed for v0.20.x, proposed for v0.20.3, as a P2 bug, on the Auditor's word of 29 October. Records only. |
