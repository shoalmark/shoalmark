---
id: FM-128
status: Proposed
considered: FM-085, FM-039
tags: process
hook: "The suite sets Chrome's mock keychain and a fresh profile itself, and the agents' contract does not say so. And no real browser block's run is in the record with its profile folder shown gone after it."
---

# FM-128 — the agents' contract does not say that the suite sets Chrome's mock keychain and fresh profile itself

## What is true now

**2026-11-03 — filed; nothing is built.** It leaves FM-085 at its split, as the Owner's sweep words it.
- **Item 4 of FM-085:** the contract's one line, once the Owner gives the word on the contract change.
- **Item 3 of FM-085, on the Owner's word of 2 November:** one browser block runs green with the flags, and its
  temporary profile folder is gone after the run. The record names CI's run, and not the removal after it.
- **Already shipped under FM-085:** every Chrome the suite starts gets the mock keychain and a fresh profile of its
  own, with a test of each launch path.

## Why

An agent reads the contract, not the suite. A rule the suite holds is one the contract should say it holds.

## Done when

- [ ] One browser block runs green with the flags, and its temporary profile folder is shown gone after the run.
- [ ] The agents' contract says the suite sets both flags itself, on the Owner's word.

## Ship log

| Date | Event |
|---|---|
| 2026-11-03 | Filed from FM-085's split, with its items 3 and 4. Records only. |
