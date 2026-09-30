---
id: FM-042
status: In Progress
considered: FM-006, FM-005, FM-023, FM-033
tags: research
kind-of-problem: complicated
triaged: 2026-09-30
rank: 10
next: build
tier: P2
hook: "Developer and tester work from one ground truth — requirements in the repository, tested as a contract, not by reading the implementation; test plans drift"
---

# FM-042 — requirements in the repository, tested as a contract: a layer for shoalmark's adopters

Seat: Principal · filed 2026-09-30 on the Owner's word — *"Stage 0 is a go from my side."* (normalised, 10:19:57) — an explicit
exception to the filing freeze (FM-032 S4), filed by hand because `--new` refuses what is not a defect while the freeze holds.

## What is true now

The idea, from the first pitch (the signal is under FM-006): developer and tester work from one ground truth — requirements
in the repository, tested as a contract, not by reading the implementation, because test plans drift. A prospect made a
requirements folder the same day, started with regulatory requirements, the easiest to formulate, and found two defects; a
trial is planned for the weekend, most likely run by an agent.

**Stage 0 — the convention, docs only (this filing's build):** a `requirements/` folder, one line per requirement — a stable
id, a *shall* statement, its source, an acceptance criterion; trackers cite ids in a body line (`Satisfies: REQ-001`), tests name them; changing a
requirement is the Owner's signed decision. A regulatory requirement cites its clause (standard, edition, clause number) and
derives the company's own *shall*; *not applicable* is a signed answer. Never copy a standard's text; never claim compliance.
It lands in the agent-facing entry — AGENTS.md, README's first screen, ADOPT.de.md — before the v0.19.0 cut, Thursday 2026-10-01 evening (the Owner's release plan of 10:2x), so the
trial can use it, and passes FM-006's claim screen.

**Stage 1 — an ask later, after the trial and one more prospect:** coverage and citation checks; stale-marking on a changed
requirement; `--trace REQ-<id>`; a traceability matrix per release, generated from git. **Stage 2:** a spec-only tester seat.

**The ratio:** a `requirements/` folder counts as records, not product, unless the Owner rules otherwise — records could be
relabelled as product. Requirements replace records: a tracker cites ids instead of restating behaviour, never a third copy.
The `[ratio]` line that lists the folder follows when `--ratio` (FM-032) lands.

**A cold run before the tag:** a fresh session, given only the public repository's address and a small C or C++
repository, adopts shoalmark with `requirements/` per Stage 0 and reports where it stalls.

## Done when

Stage 0: the convention stands in the three entries and the claim screen passed — done on the Owner's word. Stage 1 and 2:
their ask answered, then built.

## Ship log

| Date | Event |
|---|---|
| 2026-09-30 | Filed on the Owner's go, an explicit freeze exception; judged by the pass of the same day. |
| 2026-09-30 | **Stage 0 built** — the convention in `requirements/README.md`, AGENTS.md, README's first screen, ADOPT.de.md; the signal under FM-006; the Reviewer's claim screen by hand: `review-fm-042-stage-0-7eca3ab.md`, NOT READY, reworked on its findings; done when the Owner says so. Lines of the Implementer's change, `f3d19dd..` the rework tip, the Reviewers' review files left out: by the Owner's rule (`requirements/` as records) 52 records added, 34 product added, 8 deleted; as `--ratio` will count it until FM-032's toml line lands (`requirements/` as product) 9 records added, 77 product added, 8 deleted. |
