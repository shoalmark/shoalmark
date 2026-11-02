---
id: FM-085
status: In Progress
considered: FM-023, FM-035, FM-039, FM-021
tags: process
next: build
triaged: 2026-10-29
tier: P2
hook: "The suite's browser blocks rely on whoever runs them to start Chrome with a mock keychain and a profile of its own. A run that forgets them reaches the person's own keychain and browser profile. The suite should set both itself, on every launch, whatever the runner passes."
---

# FM-085 — the suite starts Chrome with a mock keychain and a fresh profile itself

## What is true now

**Filed 2026-10-29, and judged In Progress, P2, for v0.20.2, before the first build commit.** It is v0.20.2's row "the
suite's Chrome keychain flag" in [FM-023](FM-023-a-plan-names-its-seats-their-estimates-and-when-the-person.md)'s
allocation. On the Owner's word of 29 October, it goes to a Builder of the Planner's.

- **Today:** a browser block in the test suite starts Chrome with what its runner gives it. Keeping that run off the
  person's own keychain and browser profile is a rule the runner follows, not something the suite does.
- **The change:** every Chrome the suite starts, in process or as a child process, gets `--use-mock-keychain` and a
  fresh `--user-data-dir` in a temporary folder the suite makes, and removes after the run. A runner's own flags are no
  longer needed.
- **Built 2026-10-29, test-only, in `51cc442`:** the suite gives every Chrome it starts `--use-mock-keychain` and a
  profile folder made fresh in its own temporary folder, which the run removes: in process, in the child programs
  that carry the browser helpers, and in the three Node scripts through `_chrome_node`'s launcher. A runner's own two
  flags are left out. A stand-in test holds each launch path, and sixteen mutants turn it red. Windows starts no
  launcher, so there the two opt-in Node blocks skip by name.

## Why

A test run must never read or prompt for the person's keychain, and never open their own browser profile. Where that
holds only while every runner remembers it, one forgotten flag breaks it.

## Done when

- [ ] Every launch path of Chrome in the suite passes `--use-mock-keychain` and a fresh `--user-data-dir` under a
  temporary folder the suite makes, whatever the runner passes.
- [ ] A test reads each launch path's arguments, and fails where either flag is missing or the profile folder is not
  the suite's own.
- [ ] One browser block runs green with the flags, and its temporary profile folder is gone after the run.
- [ ] The agents' contract says the suite sets both flags itself.

## Ship log

| Date | Event |
|---|---|
| 2026-10-29 | Filed, and judged In Progress, P2, for v0.20.2, before the first build commit. Records only. |
| 2026-10-29 | Built, test-only: every launch path of Chrome in the suite passes both flags itself, with a stand-in test and its mutants. |
