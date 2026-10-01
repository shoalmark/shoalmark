---
id: FM-041
status: In Progress
considered: FM-036, FM-002, FM-021, FM-033
tags: bug
triaged: 2026-09-30
next: wait
tier: P3
hook: "the board places a ranked Proposed tracker in the backlog while the progress caption promises rank order"
---

# FM-041 — the board places a ranked Proposed tracker in the backlog while the progress caption promises rank order

## What is true now

**2026-10-01 — stays In Progress until the parent project's pin moves (the Owner's ruling).** Its fix, `a80a713e9b`, is in
v0.19.0; the tracker ships, naming that commit, once the parent project's pin has moved and its ranked ten show together.

**Filed 2026-09-28 on the Auditor's finding through the Owner — his paste of 09:01:54, headed *To: 8e509911 principal (shoalmark-principal-4)*, four
lines, saved word for word, sha256 `a375a843e12228c9229076e9af8b0f6ff22516f16f31156d67f0a75a870118ac`; nothing was built at filing.** The Auditor's line, word for word: *"Bug, 95% on
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

**Shipped 2026-09-30 on `fm/041-a-ranked-open-tracker-sits-in-progress-by-rank`, for v0.19.0 (the Owner's word: *"FM-024's build and FM-041 ride v0.19.0."*, 2026-09-30 10:40:31).** `board()` now returns *progress* for open work with a rank whatever its status — `In Progress` or `Proposed`, the two a rank may stand on (`lint`) — the open unranked *backlog*, *triage* keeps its precedence, *done* is unchanged. INDEX.md and the dashboard read the same function; the dashboard already sorts a section by rank, then tier, so the caption stays true. Proof: `test_core.py` and `test_shoalmark.py` each plant a ranked Proposed tracker (progress), an unranked one (backlog), a ranked In Progress one (unchanged), a raised and an unjudged one (triage); the `test_core.py` check fails on `origin/main` `2eb803b` at `board()`'s last line.

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
| 2026-09-30 | Built on `fm/041-a-ranked-open-tracker-sits-in-progress-by-rank`: `board()` places a ranked open tracker in *progress* whatever its status; suite checks in `test_core.py` and `test_shoalmark.py`; CHANGELOG under `## Unreleased — 0.19.0`. |
