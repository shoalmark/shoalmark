---
id: FM-077
status: Proposed
considered: FM-024, FM-076
tags: security
hook: "an Owner-signed commit that carries a seat's Session: line passes silently"
---

# FM-077 — an Owner-signed commit that carries a seat's Session: line passes silently

## What is true now

**Filed 2026-10-27, Proposed, from RV-3911 (P3) of the Auditor's review.** It comes after v0.20.2; nothing is built.

An Owner-signed commit that carries a seat's `Session:` line passes the gate silently.

## Why

A session line under the Owner's signature claims a seat's work as the Owner's, or the Owner's as a seat's, and nothing says so.

## Done when

- `--check` names such a commit in one line, and a test pins it.

## Ship log

| Date | Event |
|---|---|
| 2026-10-27 | Filed, Proposed, from RV-3911; after v0.20.2. |
