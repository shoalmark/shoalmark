---
id: FM-102
status: Proposed
considered: FM-030
tags: bug
hook: "An origin that only a url.<base>.insteadOf rule turns into GitHub's takes the stand-up of git without a forge, though --queue reads it as GitHub. Read those settings with the config reads the step already makes, and apply them in Python."
---

# FM-102 — the stand-up and --queue disagree on an origin that an insteadOf rule turns into GitHub's

## What is true now

**2026-11-03 — filed for v0.20.3; nothing is built.**
- **What happens:** an `origin` that only a `url.<base>.insteadOf` rule turns into GitHub's takes the stand-up of git
  without a forge, though `--queue` reads it as GitHub ([FM-030](FM-030-an-accepted-action-ask-leaves-the-person-s-list-before-the.md)).
- **The fix:** read the `url.<base>.insteadOf` settings with the config reads the stand-up's step already makes, and
  apply them in Python, so that both agree. No new kind of git start.

## Why

Two readings of one `origin` give the person two answers to one question: is this repository on GitHub?

## Done when

- [ ] The stand-up and `--queue` read an `origin` that an `insteadOf` rule rewrites the same way, under a test for
  each.
- [ ] The stand-up starts no new kind of git process for it.

## Ship log

| Date | Event |
|---|---|
| 2026-11-03 | Filed for v0.20.3. Records only. |
