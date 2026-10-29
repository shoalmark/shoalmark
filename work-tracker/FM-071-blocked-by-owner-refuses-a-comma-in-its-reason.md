---
id: FM-071
status: Proposed
considered: FM-020
tags: bug
hook: "blocked-by: Owner refuses a comma in its reason"
---

# FM-071 — blocked-by: Owner refuses a comma in its reason

## What is true now

**Filed 2026-10-27, Proposed, from a field report from a Windows working copy, on v0.20.1.** It comes after v0.20.2, on the Owner's allocation as relayed by the Auditor; nothing is built.

The front-matter line `blocked-by: Owner — <reason>` refuses a reason that holds a comma.

## Why

A reason a person writes in their own words often holds a comma, and the refusal does not say that the comma is what it refuses.

## Done when

- A comma is allowed after "Owner —", or `--schema` states the rule.
- A test pins the choice.

## Ship log

| Date | Event |
|---|---|
| 2026-10-27 | Filed, Proposed, from a field report from a Windows working copy; after v0.20.2. |
