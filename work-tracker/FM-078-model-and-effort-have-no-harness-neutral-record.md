---
id: FM-078
status: Proposed
considered: FM-024
tags: process
hook: "model and effort have no harness-neutral record"
---

# FM-078 — model and effort have no harness-neutral record

## What is true now

**2026-11-04 — slice filed: no harness log on Grok Bot (story FM-147); nothing is built.** Grok Bot writes no local harness log of the kind `--whoami` and the commit hook read (`seat.harness` → a log whose newest model and effort fill `Model:` and `Effort:`), so a seat there cannot have its model or effort attested: `--whoami` prints `From: 28862432 planner (planner-1) · — · —`, and session resume commands are missing. A seat must never write its own model. Candidates, none chosen: an explicit *unattested* state distinct from `—`; an Owner-signed record of which bot runs which seat.

**Filed 2026-10-27, Proposed, from RV-3912 (P3) of the Auditor's review.** It comes after v0.20.2; nothing is built.

Model and effort are recorded from Claude Code's and Codex's own logs, with no harness-neutral way to record them.

## Why

A seat on another harness, or a harness whose log changes, leaves its commits without model and effort.

## Done when

- A harness-neutral way to record model and effort is designed and ruled before it is built.

## Ship log

| Date | Event |
|---|---|
| 2026-10-27 | Filed, Proposed, from RV-3912; after v0.20.2. |
| 2026-11-04 | **Slice filed — no harness log on Grok Bot** (story FM-147, on the Auditor's direction relayed by the Owner): model and effort unknown there, no harness-neutral record. Nothing built; status unchanged. |
