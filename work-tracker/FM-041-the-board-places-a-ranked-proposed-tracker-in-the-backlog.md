---
id: FM-041
status: Proposed
considered: FM-036, FM-002, FM-021, FM-033
tags: bug
triaged: 2026-09-30
next: build
tier: P3
hook: "the board places a ranked Proposed tracker in the backlog while the progress caption promises rank order"
---

# FM-041 — the board places a ranked Proposed tracker in the backlog while the progress caption promises rank order

## What is true now

**Filed 2026-09-28 on the Auditor's finding through the Owner — his paste of 09:01:54, headed *To: 8e509911 principal (shoalmark-principal-4)*, four
lines, saved word for word, sha256 `a375a843e12228c9229076e9af8b0f6ff22516f16f31156d67f0a75a870118ac`; nothing is built.** The Auditor's line, word for word: *"Bug, 95% on
the cause: board() places a tracker by status only (tools/shoalmark/shoalmark.py:734), so ranked Proposed trackers (BUG-328 #3, PD-402 #4, PD-401 #10)
fall into the 165-row backlog, although progress reads "kept by triage — by rank, then tier". Proposal: any open tracker with a rank sits in progress, by
rank. board() also writes INDEX.md: one Reviewer pass."* Checked by the Principal in the tool at main `eb00e96b` (`shoalmark.py` 739–747): `board(t)`
returns *progress* only for the status In Progress; a Proposed tracker with a rank returns *backlog*; the progress section's caption (`desc.progress`,
line 2488) reads *kept by triage — by rank, then tier*. The finding holds. The three trackers named are the parent project's; the rule places any
consumer's ranked Proposed tracker the same way.

**The design — the Auditor's proposal as the Principal reads it, for the pass that judges this filing:** an open tracker with a rank sits in *progress*,
ordered by rank then tier, whatever its status; the backlog holds the open unranked; the *triage* rule (a raise on a signed rule, or a judgment owed and
missing) keeps its precedence; *done* is unchanged. `board()` is the one definition INDEX.md and the dashboard share, so one change places both. Tier:
the board's placement and INDEX.md — code, not critical (no queue reader, no gate touched): AGENTS.md's code loop — NOT READY on any P2 until READY,
same-session Reviewers; the Auditor counselled one pass, and a clean first pass is where the loop ends.

## Why

The progress section is the working set the Owner reads at a glance; its caption promises rank order, and three of the ranked ten sit 165 rows down
instead. A status is what a seat set; a rank is what a pass judged — the board should follow the judgment.

## Done when

- `board()` places a ranked open tracker of any status in *progress*, by rank then tier; the unranked open in *backlog*; the *triage* and *done* rules
  unchanged — with a suite check for a ranked Proposed tracker.
- INDEX.md and the dashboard show the parent project's ranked ten together under *progress* once the pin moves.
- The caption stays true to what the section holds.

## Ship log

| Date | Event |
|---|---|
| 2026-09-28 | Filed on the Auditor's finding through the Owner (09:01:54; sha256 `a375a843…`), checked in the tool at `eb00e96b`; considered FM-036, FM-002, FM-021, FM-033 — FM-021 shipped the section's caption, FM-033 the judged-before-build rule; neither owns placement by rank. A bug under the freeze; judged by the next pass. |
