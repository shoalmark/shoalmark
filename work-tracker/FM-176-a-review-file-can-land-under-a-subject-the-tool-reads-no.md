---
id: FM-176
status: Proposed
considered: FM-031, FM-033, FM-087
tags: bug
hook: "The tool reads a verdict from a commit's subject, by its verdict word, beside its Reviewed: trailer. Nothing checks that word when the review lands: a commit that adds a review file under a subject without it passes the hook, and the queue then says no verdict. The fix, on the Owner's word of 18 November: the commit hook refuses such a commit and prints the wording the tool reads."
---

# FM-176 — a review file can land under a subject the tool reads no verdict from, so the queue says no verdict

Seat: the Planner (a1730572) · filed 2026-11-18, on the coordinator's word of that day.

## What is true now

**Filed 2026-11-18, Proposed; nothing is built.** The Owner's word of 18 November: a correction goes into a check,
not into the memory of one harness. This is that check for the verdict word.

- **How the tool reads a verdict today:** the queue and the gate take a commit as a verdict when its subject carries
  one of the words the tool reads (`READY`, `READY WITH FINDINGS`, `READY TO TAG`, `NOT READY`) and its body a
  `Reviewed:` trailer naming the commit it read. A review's own file lives in the review folder (`[paths] reviews`,
  `evidence/reviews/` by default).
- **What nothing checks:** that a commit which adds a review file carries that word in its subject. Without it the
  review is filed, and the queue still says "no verdict" on the head it read.

## Why

A verdict the tool cannot read is no verdict for the gate, the queue or the Owner. The place to catch it is the
commit that lands it, where the fix is one word.

## Decisions

1. **The commit hook** refuses a commit that adds a file under the review folder when its subject carries none of the
   verdict words the tool reads.
2. **Its refusal prints the wording** the tool reads, and the subject forms it accepts, so the fix is plain.
3. **A test** for each word and for a subject with none, with its mutant; the gate's own reading is unchanged.

## Done when

Each item names its commit or pull request when it lands.

- [ ] **The hook refuses** a commit that adds a review file without a verdict word, and prints the wording, with its
  test and mutant.
- [ ] **The review, at the tier the triage pass sets, is READY.**

## Ship log

| Date | Event |
|---|---|
| 2026-11-18 | Filed, Proposed: the commit hook is to refuse a review file landed under a subject without a verdict word the tool reads. Records only. |
