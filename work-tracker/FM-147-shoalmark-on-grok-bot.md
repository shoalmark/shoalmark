---
id: FM-147
status: Proposed
considered: FM-024, FM-078, FM-025, FM-007, FM-059
tags: research
next: wait
hook: "Shoalmark on Grok Bot: the Auditor's audit found gaps in session proof, harness attestation, a companion connector and onboarding; this story collects them, three as slices of trackers that exist and one as a new chapter."
---

# FM-147 — Shoalmark on Grok Bot

Seat: Planner · filed 2026-11-04 on the Auditor's direction, relayed by the Owner.

## What is true now

**2026-11-04 — story filed; nothing is built.** How Shoalmark seats run as Grok Bot assistants. Its parts, as placed on the Auditor's direction (three of the four already had a tracker on `main` at `c02ca26`, so they are slices, not new trackers):

| # | Where | Problem |
|---|---|---|
| 1 | slice of FM-024, 2026-11-04 | Session proof: on Grok Bot `seat.session` is self-report; a second worktree can set the same value |
| 2 | slice of FM-078, 2026-11-04 | No harness log on Grok Bot: model and effort are unknown, with no harness-neutral record |
| 3 | FM-148 | Companion app connector: notify only; whether and with which keys the Owner signs on mobile is the Owner's ruling (ask FM-148-Q3) |
| 4 | slice of FM-025, 2026-11-04 | Onboarding gaps: what a cold seat on Grok Bot meets before it can work |

FM-024, FM-078 and FM-025 keep their own status and triage; this story names their slices and does not adopt them as chapters. FM-148 is its one new chapter (`epic: FM-147`).

**Placement.** Everything here describes the tool on Grok Bot generally and holds no secret, key material, adopter identity, or path beyond what a finding needs. A further finding is recorded privately.

**The Auditor** files its own records under these trackers and re-runs to verify. It does not own, gate or rule on any of them.

## Why

Grok Bot is a workbench for Shoalmark seats. The audit found gaps that touch trust (which run sat, which model), the Owner's signing path (the companion app), and first-run friction (onboarding). One story keeps them readable together; each part ships with its own tracker.

## Done when

- Each slice is closed out in its tracker (FM-024, FM-078, FM-025), and FM-148 is Shipped or Closed, or Parked by a triage pass against the current path.
- The Auditor's verify re-runs under these ids are linked from the ship logs.

## Ship log

| Date | Event |
|---|---|
| 2026-11-04 | Filed by the Planner seat on the Auditor's direction (relayed by the Owner): story, the new chapter FM-148, and dated slices on FM-024, FM-078 and FM-025. |
