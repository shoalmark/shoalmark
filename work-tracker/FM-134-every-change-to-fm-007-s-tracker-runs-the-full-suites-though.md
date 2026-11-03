---
id: FM-134
status: Proposed
considered: FM-032, FM-007, FM-038
tags: process
hook: "ci.yml treats FM-007's tracker as read by the suites, so a pull request that changes only FM-007 runs the five full jobs. The one test that reads it depends on two pinned commits, which no change to the file can remove. The test can read those commits directly, and FM-007 leaves the list."
---

# FM-134 — every change to FM-007's tracker runs the full suites, though the one test that reads it cannot break from one

## What is true now

**2026-11-03 — filed; nothing is built.** It is FM-032's defect 3, filed anew at FM-032's close, as the Owner's sweep
words it. FM-032's text of 15 October holds its facts, its proposed fix and its controls.
- **What happens:** `.github/workflows/ci.yml`'s records rule lists FM-007's tracker as a path the suites read, so
  a pull request that changes only FM-007 is not records-only, and runs the five full jobs.
- **Why it is listed:** one test reads FM-007's live file and its path's history, for two pinned answers of 22 September.
  Only renaming or deleting the file could break it.
- **The proposed fix:** the test reads its pinned commits directly, and FM-007 leaves `ci.yml`'s list, with its
  mutant.
- **Tier and order:** critical, since `ci.yml`'s records rule decides what CI judges. It is ordered with FM-048's
  change to `ci.yml`, which is not on main.

## Why

Each answer or act on FM-007 pays five full jobs where one records run would do.

## Done when

- [ ] The test reads FM-007's two pinned answers by commit, and no longer reads the live file or its history.
- [ ] FM-007 leaves `ci.yml`'s list, and a pull request that changes only FM-007 classifies as records-only.
- [ ] A class test holds every tracker path in `ci.yml`'s list to a suite that still reads it.

## Ship log

| Date | Event |
|---|---|
| 2026-11-03 | Filed from FM-032's close, its defect 3. Records only. |
