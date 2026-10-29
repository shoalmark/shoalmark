---
id: FM-072
status: Proposed
considered: FM-004, FM-026
tags: process
hook: "ADOPT's read rule for an extension can be taken to skip a folder whose name ends that way"
---

# FM-072 — ADOPT's read rule for an extension can be taken to skip a folder whose name ends that way

## What is true now

**Filed 2026-10-27, Proposed, from a field report from a Windows working copy, on v0.20.1.** It comes after v0.20.2, on the Owner's allocation as relayed by the Auditor; nothing is built.

A read rule such as "skip .accdb", given to an agent trying shoalmark, can be read as skipping a folder whose name ends that way. It means files with that extension, and never a folder.

## Why

An agent that skips a folder by its name reads less of the project than the person meant, and says nothing about it.

## Done when

- `ADOPT.md`, `ADOPT.svn.md` and their German twins say that a rule for an extension means files with that extension, never a folder whose name ends that way.

## Ship log

| Date | Event |
|---|---|
| 2026-10-27 | Filed, Proposed, from a field report from a Windows working copy; after v0.20.2. |
