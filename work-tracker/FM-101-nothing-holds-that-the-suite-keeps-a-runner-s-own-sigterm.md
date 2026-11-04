---
id: FM-101
status: Proposed
considered: FM-085
tags: bug
epic: FM-139
hook: "The suite sets its own SIGTERM handler only where the default handler stands, so a runner's own handler is kept. No test holds that: a mutant that replaces a runner's handler passes the suite."
---

# FM-101 — nothing holds that the suite keeps a runner's own SIGTERM handler, so a mutant that replaces it survives

## What is true now

**2026-11-03 — filed for v0.20.3; nothing is built.** A mutant that survived the review of the suite's Chrome change
([FM-085](FM-085-the-suite-starts-chrome-with-a-mock-keychain-and-a-fresh.md)).
- **What the code does:** the suite sets its own SIGTERM handler, which removes its folder for Chrome when a runner's
  time limit ends the run, only where the default handler stands (`test_shoalmark.py:699` at this filing). A runner's
  own handler is kept.
- **What no test holds:** that the suite keeps it. A mutant that replaces a runner's own handler passes the suite.

## Why

A guard that no test holds can be removed in the next change, and the runner's own clean-up stops running with it.

## Done when

- [ ] A test sets a SIGTERM handler of its own before the suite's first Chrome start, and holds that it is still
  the handler after.
- [ ] The mutant that replaces it fails that test.

## Ship log

| Date | Event |
|---|---|
| 2026-11-03 | Filed for v0.20.3. Records only. |
| 2026-11-04 | `epic: FM-139`: a chapter of v0.20.3's epic. Records only. |
