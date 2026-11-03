---
id: FM-138
status: Proposed
considered: FM-018, FM-001
tags: bug
hook: "When the only change in the Owner's checkout is a moved submodule pointer, a tracker-only write refuses. It should not count it, or its refusal should name the fix, git submodule update <path>."
---

# FM-138 — a moved submodule pointer alone stops a tracker-only write

## What is true now

**2026-11-03 — filed; nothing is built.** It is the Auditor's raise of 28 September, through the Owner, held in FM-018.
It is filed anew at FM-018's close, as the Owner's sweep words it.
- **What happened:** `--done` refused the Owner because the only change in their checkout was a moved submodule
  pointer.

## Why

A refusal over a change the person did not make, with no fix named, is where a person who is not technical stops.

## Done when

- [ ] When the only change in the checkout is a submodule pointer, a tracker-only write either does not count it,
  or its refusal names the fix, `git submodule update <path>`; the builder chooses.
- [ ] A test holds each case.

## Ship log

| Date | Event |
|---|---|
| 2026-11-03 | Filed from FM-018's close. Records only. |
