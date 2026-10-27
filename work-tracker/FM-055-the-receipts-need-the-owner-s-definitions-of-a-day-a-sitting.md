---
id: FM-055
status: Proposed
considered: FM-032, FM-023, FM-050, FM-004
tags: process
next: wait
hook: "The receipts count what the record holds, and they need the Owner's definitions of a day, a sitting and repositories counted together"
---

# FM-055 — the receipts need the Owner's definitions of a day, a sitting and repositories counted together

## What is true now

**Filed 2026-10-15, with its ask; nothing is built.** The receipts are a quick win of v0.20.1, beside R13 (FM-023's
table of 2026-10-15): the ratio command goes, and this view counts what the record holds instead.

- **What it shows,** read from git alone, in one repository or in the ones you name: per day, the oldest waiting ask,
  the answers and how many of them are signed, the sittings with the answers in each, and the sessions. The same counts
  in two windows, split at a day you pick, lead the output.
- **What it never shows:** a total in a heading, or a cause. Each count stands with its definition, its method and its
  date range. History that cannot be read is named as *not read*, with why, and counted in nothing.
- **Where it waits:**
  - on R4, so that both answer shapes are read, the answer branches and the ordinary signed commit;
  - on this ask: what a day is, what a sitting is, and whether repositories named together give one count.
- **The proposal:** a day in the machine's time zone; a sitting as answers at most 30 minutes apart; the repositories
  you name counted together. R13 removes `--ratio`, whose Berlin-day code is not reused.
- **Tier:** code, with the full review loop. **Size:** M.
- **Source:** the quick-wins design of 15 October, recorded privately.

## Done when

- The Owner's answer defines the three terms.
- Built: `--receipts` and the board's folded receipts section read the counts above from git, each with its
  definition, never a total in a heading; the class test covers a day's edge, a sitting's gap and two repositories.

## Asks

**2026-10-17** · Do the receipts count a day in the machine's time zone, a sitting as answers at most 30 minutes apart, and the repositories you name together as one count?
**answered** — accepted - yes · holgo99
**relation** — accepted the proposal
**signed** — 33e4f3b · G

## Ship log

| Date | Event |
|---|---|
| 2026-10-15 | Filed, with its ask. |
