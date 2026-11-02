---
id: FM-074
status: Proposed
considered: FM-003, FM-031
tags: process
hook: "the docs do not name two Subversion limits first: no gate on the svn command line, and one shared account"
---

# FM-074 — the docs do not name two Subversion limits first: no gate on the svn command line, and one shared account

## What is true now

**Filed 2026-10-27, Proposed, from a field report from a Windows working copy, on v0.20.1.** It comes after v0.20.2, on the Owner's allocation as relayed by the Auditor; nothing is built.

The adoption report names two Subversion limits as first-class, and the docs do not put them first:
- the svn command line has no gate: an agent's commit there is ungated, while a TortoiseSVN commit is gated;
- one shared Subversion account leaves seats and rights without weight.

## Why

A person deciding whether to adopt shoalmark on Subversion needs both limits before they start, not after a trial finds them.

## Done when

- Where README.md, `docs/setup.md`, `ADOPT.svn.md` and their German twins describe Subversion, both limits are named first, in the person's terms.

## Ship log

| Date | Event |
|---|---|
| 2026-10-27 | Filed, Proposed, from a field report from a Windows working copy; after v0.20.2. |
