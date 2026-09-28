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

The Owner's word of 2026-09-28 01:42:26 CEST, with the two hook summaries he pasted — shoalmark *`✔️ tracker-board (25.88 seconds)`*, PortDive
*`✔️ tracker-dashboard (14.48 seconds)`* — (spelling normalised, marked): *"Execution time has increased to a point where using the tool through the
hook feels painful. Routes from here: a. profile the Python path — what takes up time, where would optimisation bite; b. explore the Rust port. If we
expand the product to mobile clients, path b could be valuable — a single code base, like PortDive's. Tool builds and integration through `brew
install shoalmark` would be the price to pay upfront."* (normalised)

Measured the same night, before any profiling: a full `python3 shoalmark.py` on shoalmark main `bbbfc0b` took **real 42.7 s — user 16.8 s, sys
24.3 s** (the system time is the tell: subprocesses or file I/O, not Python arithmetic), the run started 01:44:16. What the hooks run, from `lefthook.yml`:
on shoalmark, `tracker-board` is the **post-merge** step (`python3 shoalmark.py --html-only || true`, line 22), a commit's pre-commit runs
`tracker-index` (`--print-written`; 27.82 s for this filing's own commit at 01:52), and a checkout runs a plain hook; on PortDive the pre-commit runs
`scripts/gen-tracker-index.py --print-written` (line 41) and post-merge and post-checkout run `--html-only` (lines 154 and 158) — the wrapper launches the
pinned `tools/shoalmark/shoalmark.py` as a child process, so a profile targets that child. On PortDive, the pre-commit hook's `tracker-index` step took 18.57 s at 01:47 on the pinned
0.18.5 (`scripts/gen-tracker-index.py`, 507 trackers). Every seat's loop — checkout, commit, verdict — pays it dozens of times a day, and the Owner
pays it at every button.

Held against (FM-035 and FM-039 by hand — `--related` does not return them): FM-018 (the answer flow's convenience — this is the hook's, not the flow's), FM-025 (a cold start's tokens — a different cost),
FM-034 (a fresh clone's `--check` — the same header path, not its time), FM-035 and FM-039 (the suite's 5 s Chrome budget — a render budget, not the
regeneration's). None names the regeneration's wall-clock time; a new filing.

**The two routes, the Owner's, for his ruling once the profile is in:**
- **a. profile the Python path** — `cProfile` of `--html-only` and of the commit's `--print-written` path on both repositories at low load, the number of `git` subprocesses per run, the ten
  functions by cumulative time; then the optimisation that bites (a cache of per-tracker git facts across a run, one `git log` for all files instead
  of one per file, or whatever the profile names). The Principal's counsel, disclosed as such: the cheaper route, and it keeps the single Python file
  every consumer vendors.
- **b. explore the Rust port** — one code base for the tool and for mobile clients, as PortDive's Rust core is; the upfront price: a build per
  platform, `brew install shoalmark` for consumers, the pin and the vendoring redone. The Principal's counsel, disclosed as such: a product decision, his, not a performance fix.

**Read, not measured (a seat's code reading reported 2026-09-28 02:03:03, confidence about 55 % until profiled):** the board path starts with `git branch
--show-current`, then per tracker in `render_html`: `ask_problems` runs with provenance on, so every `next: owner` tracker goes through `seat_problems`
and can cost a `git log -1 --full-history -G` history walk per ask (the docstring at line 1012, in `recover_relations`, measures that pattern at about 0.4 s per file on a
3,755-commit repository), plus `git diff`/`git show`; `board_sessions` → `verdict_reports` makes three or four git calls per verdict (rev-parse,
merge-base, rev-list --ancestry-path, log — 137 verdicts this week); `recover_relations` does one `git log -p` and one `git show` per answer commit;
`held_up_by` is O(n²) in Python but cheap beside the git calls. The change most likely to bite: the board path with `provenance=False`, or the per-ask
pickaxe batched into one `git log` — an unmeasured guess of several seconds on PortDive (~3,971 commits); the risk: the board stops marking a
wrong-seat ask as malformed, leaving `--check` the only guard. The profile itself did not run on 2026-09-28: the seat's runner waited for the machine's
load (1-minute averages of 12 to 176 between 01:52 and 02:00) and the permission classifier then refused its restart; its script
(`run_all.sh`, one command at a time, writes only under the session's scratch folder) is the Owner's to run or a permitted seat's.

The profile (slice 1) is a seat's read-only work and needs no ruling; the route after it is an ask to the Owner, rowed first in the ledger, with the
profile's numbers as its input and no default.

## Done when

Slice 1: the profile stands in this tracker's body — both repositories, the ten functions by cumulative time, the subprocess count, the machine's
load at the run — and the ask on the route (a or b) is filed on the Owner's answer flow with a ledger row first. The fix's own Done-when is written
after his ruling, as a wall-clock number for the hook on both repositories that he sets or accepts.

## Ship log

| Date | Event |
|---|---|
| 2026-09-28 | Filed on the Owner's word of 01:42:26 (his two hook summaries: 25.88 s / 14.48 s); a full regeneration on `bbbfc0b` measured 42.7 s real (16.8 user, 24.3 sys), started 01:44:16; PortDive's `tracker-index` pre-commit step 18.57 s at 01:47. Slice 1 (the profile, read-only) started the same night; the route is his ask after it. |
| 2026-09-28 | The filing's pass `e7d16b8` READY WITH FINDINGS (RV-681…684, reviewer-40; its own full regeneration 50.84 s real / 18.25 user / 29.50 sys at a 1-minute load of 150 falling to 72). Fixed in the next commit: the hook steps named from `lefthook.yml` (RV-681), the times exact (RV-682), FM-035/FM-039 marked as held by hand (RV-683), the route weighing disclosed as the Principal's counsel (RV-684); the seat's unmeasured code reading added; the profile not run — the permission classifier refused the seat's runner. |
| 2026-09-28 | The re-check `fd43178` (reviewer-40): RV-682/683 closed; RV-681 and RV-684 open in part, RV-691 new (an approximate time, a docstring's line) — fixed in the next commit: route a profiles `--print-written` too, route b labelled as counsel, the reading's time 02:03:03, the docstring at line 1012 in `recover_relations`. |
