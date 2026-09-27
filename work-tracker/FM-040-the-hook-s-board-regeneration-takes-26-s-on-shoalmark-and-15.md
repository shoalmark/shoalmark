---
id: FM-040
status: Proposed
considered: FM-018, FM-025, FM-034, FM-035, FM-039
tags: bug
hook: "the hook's board regeneration takes 26 s on shoalmark and 15 s on PortDive — every checkout and commit waits for it"
---

# FM-040 — the hook's board regeneration takes 26 s on shoalmark and 15 s on PortDive — every checkout and commit waits for it

## What is true now

**Filed 2026-09-28; nothing is built.**

## Why

The Owner's word of 2026-09-28 ~01:40 CEST, with the two hook summaries he pasted — shoalmark *`✔️ tracker-board (25.88 seconds)`*, PortDive
*`✔️ tracker-dashboard (14.48 seconds)`* — (spelling normalised, marked): *"Execution time has increased to a point where using the tool through the
hook feels painful. Routes from here: a. profile the Python path — what takes up time, where would optimisation bite; b. explore the Rust port. If we
expand the product to mobile clients, path b could be valuable — a single code base, like PortDive's. Tool builds and integration through `brew
install shoalmark` would be the price to pay upfront."* (normalised)

Measured the same night, before any profiling: a full `python3 shoalmark.py` on shoalmark main `bbbfc0b` took **real 42.7 s — user 16.8 s, sys
24.3 s** (the system time is the tell: subprocesses or file I/O, not Python arithmetic); the hook runs `python3 shoalmark.py --html-only` on every
checkout and commit (`lefthook.yml`, `tracker-board`). On PortDive, the pre-commit hook's `tracker-index` step took 18.57 s at 01:47 on the pinned
0.18.5 (`scripts/gen-tracker-index.py`, 507 trackers). Every seat's loop — checkout, commit, verdict — pays it dozens of times a day, and the Owner
pays it at every button.

Held against: FM-018 (the answer flow's convenience — this is the hook's, not the flow's), FM-025 (a cold start's tokens — a different cost),
FM-034 (a fresh clone's `--check` — the same header path, not its time), FM-035 and FM-039 (the suite's 5 s Chrome budget — a render budget, not the
regeneration's). None names the regeneration's wall-clock time; a new filing.

**The two routes, the Owner's, for his ruling once the profile is in:**
- **a. profile the Python path** — `cProfile` of `--html-only` on both repositories at low load, the number of `git` subprocesses per run, the ten
  functions by cumulative time; then the optimisation that bites (a cache of per-tracker git facts across a run, one `git log` for all files instead
  of one per file, or whatever the profile names). The cheap route; it keeps the single Python file every consumer vendors.
- **b. explore the Rust port** — one code base for the tool and for mobile clients, as PortDive's Rust core is; the upfront price: a build per
  platform, `brew install shoalmark` for consumers, the pin and the vendoring redone. A product decision, his, not a performance fix.

The profile (slice 1) is a seat's read-only work and needs no ruling; the route after it is an ask to the Owner, rowed first in the ledger, with the
profile's numbers as its input and no default.

## Done when

Slice 1: the profile stands in this tracker's body — both repositories, the ten functions by cumulative time, the subprocess count, the machine's
load at the run — and the ask on the route (a or b) is filed on the Owner's answer flow with a ledger row first. The fix's own Done-when is written
after his ruling, as a wall-clock number for the hook on both repositories that he sets or accepts.

## Ship log

| Date | Event |
|---|---|
| 2026-09-28 | Filed on the Owner's word of ~01:40 (his two hook summaries: 25.88 s / 14.48 s); a full regeneration on `bbbfc0b` measured 42.7 s real (16.8 user, 24.3 sys) at 01:4x; PortDive's `tracker-index` pre-commit step 18.57 s at 01:47. Slice 1 (the profile, read-only) started the same night; the route is his ask after it. |
