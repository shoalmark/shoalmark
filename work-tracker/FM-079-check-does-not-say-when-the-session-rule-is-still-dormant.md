---
id: FM-079
status: Proposed
considered: FM-024
tags: process
hook: "--check does not say when the session rule is still dormant"
---

# FM-079 — --check does not say when the session rule is still dormant

## What is true now

**Filed 2026-10-27, Proposed, from RV-3913 (P3) of the Auditor's review.** It comes after v0.20.2; nothing is built.

`--check` does not say when the session rule is still dormant.

## Why

A rule that does not yet apply reads, in a passing check, as a rule that held.

## Done when

- `--check` says in one line when the session rule is dormant, and why.

## Ship log

| Date | Event |
|---|---|
| 2026-10-27 | Filed, Proposed, from RV-3913; after v0.20.2. |
