---
id: FM-040
status: Proposed
considered: FM-018, FM-025, FM-034, FM-035, FM-039, FM-012, FM-024
tags: bug
triaged: 2026-09-28
rank: 4
next: build
tier: P2
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

Held against (FM-035, FM-039 and FM-012 by hand — `--related` does not return them; FM-024 on the Auditor's word): FM-018 (the answer flow's convenience — this is the hook's, not the flow's), FM-025 (a cold start's tokens — a different cost),
FM-034 (a fresh clone's `--check` — the same header path, not its time), FM-035 and FM-039 (the suite's 5 s Chrome budget — a render budget, not the
regeneration's). FM-012 (the same kind of cost — its batching fix — a design, not this bug's time) and FM-024 (S6, `294a368`, v0.17.6 — where
`verdict_reports` and its cost came from). None names the regeneration's wall-clock time; a new filing.

**The two routes, the Owner's, as they stood before the profile (the measurement below chose route a for this bug; route b stays his separate question):**
- **a. profile the Python path** — `cProfile` of `--html-only` and of the commit's `--print-written` path on both repositories at low load, the number of `git` subprocesses per run, the ten
  functions by cumulative time; then the optimisation that bites (a cache of per-tracker git facts across a run, one `git log` for all files instead
  of one per file, or whatever the profile names). The Principal's counsel, disclosed as such: the cheaper route, and it keeps the single Python file
  every consumer vendors.
- **b. explore the Rust port** — one code base for the tool and for mobile clients, as PortDive's Rust core is; the upfront price: a build per
  platform, `brew install shoalmark` for consumers, the pin and the vendoring redone. The Principal's counsel, disclosed as such: a product decision, his, not a performance fix.

**Superseded by the Auditor's measurement below (2026-09-28 02:43–02:47) — kept as the record of a reading that was wrong:** the seat's code reading
(reported 02:03:03, confidence about 55 % until profiled) put the cost in provenance's per-ask pickaxe; the profile puts 92–96 % of it in
`board_sessions → verdict_reports`, and the Auditor says to drop the pickaxe change — it would give up the wrong-seat check for nothing. The reading: the board path starts with `git branch
--show-current`, then per tracker in `render_html`: `ask_problems` runs with provenance on, so every `next: owner` tracker goes through `seat_problems`
and can cost a `git log -1 --full-history -G` history walk per ask (the docstring at line 1012, in `recover_relations`, measures that pattern at about 0.4 s per file on a
3,755-commit repository), plus `git diff`/`git show`; `board_sessions` → `verdict_reports` makes three or four git calls per verdict (rev-parse,
merge-base, rev-list --ancestry-path, log — 137 verdicts this week); `recover_relations` does one `git log -p` and one `git show` per answer commit;
`held_up_by` is O(n²) in Python but cheap beside the git calls. The change most likely to bite: the board path with `provenance=False`, or the per-ask
pickaxe batched into one `git log` — an unmeasured guess of several seconds on PortDive (~3,971 commits); the risk: the board stops marking a
wrong-seat ask as malformed, leaving `--check` the only guard. The profile itself did not run on 2026-09-28: the seat's runner waited for the machine's
load (1-minute averages of 12 to 176 between 01:52 and 02:00) and the permission classifier then refused its restart; its script
(`run_all.sh`, one command at a time, writes only under the session's scratch folder) is the Owner's to run or a permitted seat's.

**The Auditor's measurement, relayed by the Owner 2026-09-28 05:24:00 (his paste, word for word; sha256 of the filed text
`a6cb201bc20cfb7f64503ddddcf4d670a1efa098969e99bcc8b1f764fe4d7ebe`):**

> The Auditor on FM-040 (shoalmark main @ 3bc0a51), measured 2026-09-28 02:43–02:47 CEST in its own clones at load 7–14:
> 1. The profile: shoalmark --html-only 39.0 s real, 568 git calls, 96% in board_sessions → verdict_reports (4 git calls per verdict × 140 verdicts in 7 days; reviewed_range's rev-list --ancestry-path alone 24.5 s). --print-written 40.4 s, 92% in the same place: the pre-commit builds the HTML board. PortDive (pinned 0.18.5, 450c67ac) 31.2 s under the profiler, 81% in verdict_reports, 97 verdicts.
> 2. The reading's "change most likely to bite" (provenance off / pickaxe batched) does not appear in the profile. Drop it; it would give up the wrong-seat check for nothing.
> 3. considered: misses FM-012 (the same kind of cost, its batching fix) and FM-024 S6 (294a368, v0.17.6, where the cost comes from).
> 4. Counsel: (a) the pre-commit writes INDEX without building the HTML board; (b) verdict reports cached per verdict sha in .git, or read in one batch. Hook code, so the full loop. The route b ask is not needed for this bug; the Rust port is his separate product question.
> 5. The profile is done — nothing for the Owner to run.

Graded by the Principal: accepted whole. The profile is slice 1, done by the Auditor in its own clones; FM-012 and FM-024 added to `considered:`
(FM-024 S6, `294a368`, v0.17.6, is where `verdict_reports` came from); the seat's reading struck as above. **The fix, two slices per the counsel, hook
code — the full loop, a cold Reviewer:** (a) the pre-commit's `--print-written` writes INDEX.md without building the HTML board (the board is built
post-merge and post-checkout, where it is read); (b) `verdict_reports` cached per verdict sha under `.git/` or read in one batched `git` call
(`reviewed_range`'s `rev-list --ancestry-path` is 24.5 s of the 39). **Route b is not this bug's:** the Rust port stays the Owner's separate product
question and is not asked here. The route ask this tracker foresaw is therefore not filed; the measurement answered it.

The profile (slice 1) was a seat's read-only work and needed no ruling; the route ask it foresaw is not filed — the measurement chose (see the clause
above), and the Rust port remains the Owner's separate product question, asked on its own tracker if he wants it tracked.

## Done when

Slice 1 (the profile) is done: the Auditor's measurement stands in the body (568 git calls, 96 % in `verdict_reports`; both repositories; load 7–14).
The fix (slices a and b above) is done when the pre-commit step and the post-merge board build on both repositories run in a wall-clock time the Owner
sets or accepts — proposed by the build with its own measurement, before and after, at a stated load — and the board it writes is byte-identical to
today's for the same trackers.

## Raised

*One sourced line per raise — the date, who raised it, the fact, its source, what it undermines; no counts. The Auditor seat's words as the Owner pasted them, word for word.*

- 2026-09-28 12:49:43 · Auditor (8b91dba2), through the Owner (his paste headed *To: 8e509911 principal (shoalmark-principal-4)*, saved word for word, seven lines, sha256 `dd56f6a2f0a9422bd831b04568708fef2b3a32e1f19350de849230df05f12946`; quoted whole) · *The Auditor, on FM-040 — the Owner hit it again on --done ("`waiting: tracker-dashboard` is painful"): 1. --done switches his checkout to answer/<id> and back, so one --done pays post-checkout twice plus the pre-commit's index: close to a minute (70%). 2. The fix the profile points at (80%): cache verdict_reports per commit sha. A commit is immutable, so only new commits need git calls. It removes most of the 568 calls; the resulting time is unmeasured (60%). 3. Quick relief (75%): let --html-only run in the background from the hooks, and write the page to a temp file then rename, so two runs never leave a half-written page. It is a view; no gate is skipped. 4. For your judgement (55%): --done writing through a temporary worktree instead of switching his checkout — no hook waits, no dirty-tree refusal; it changes where the commit's gate runs. The Rust port is a product decision, not this wait's fix: it would make the same git calls.* — the Principal's reading, 2026-09-28: points 2 and 3 are this tracker's build (the cache per commit sha is the fix the Auditor's measurement of 02:43–02:47 points at — 568 git calls, 96 % in `verdict_reports`; the background `--html-only` with a temp-file rename is the relief); point 1 is measured before the build (`post-checkout` twice and the pre-commit's index on one `--done`); point 4 changes where the commit's gate runs and is judged at the build's design, not here; the Rust line is the Owner's product question, not this tracker's · source: the paste · undermines: no signed rule — the design of this tracker's fix

## Ship log

| Date | Event |
|---|---|
| 2026-09-28 | Filed on the Owner's word of 01:42:26 (his two hook summaries: 25.88 s / 14.48 s); a full regeneration on `bbbfc0b` measured 42.7 s real (16.8 user, 24.3 sys), started 01:44:16; PortDive's `tracker-index` pre-commit step 18.57 s at 01:47. Slice 1 (the profile, read-only) started the same night; the route is his ask after it. |
| 2026-09-28 | The filing's pass `e7d16b8` READY WITH FINDINGS (RV-681…684, reviewer-40; its own full regeneration 50.84 s real / 18.25 user / 29.50 sys at a 1-minute load of 150 falling to 72). Fixed in the next commit: the hook steps named from `lefthook.yml` (RV-681), the times exact (RV-682), FM-035/FM-039 marked as held by hand (RV-683), the route weighing disclosed as the Principal's counsel (RV-684); the seat's unmeasured code reading added; the profile not run — the permission classifier refused the seat's runner. |
| 2026-09-28 | The re-check `fd43178` (reviewer-40): RV-682/683 closed; RV-681 and RV-684 open in part, RV-691 new (an approximate time, a docstring's line) — fixed in the next commit: route a profiles `--print-written` too, route b labelled as counsel, the reading's time 02:03:03, the docstring at line 1012 in `recover_relations`. |
| 2026-09-28 | The Auditor's measurement (02:43–02:47, its own clones, load 7–14), relayed by the Owner 05:24:00 and filed word for word (sha256 `a6cb201b…`): 568 git calls, 96 % in `board_sessions → verdict_reports`, the pre-commit builds the HTML board; the seat's reading struck; FM-012/FM-024 added to `considered:`; the fix's two slices per its counsel (hook code — cold review); the route ask not filed — the Rust port is his separate question. |
| 2026-09-28 | The filing's pass `cb17819` (reviewer-40) READY WITH FINDINGS: the quoted block byte for byte the paste, `294a368` confirmed as FM-024 S6; RV-694 two lines still announced the route ask — reworded; RV-695 FM-012/FM-024 named in *Held against*. |
| 2026-09-28 | **Raised, 12:49:43** (the Auditor through the Owner, paste sha256 `dd56f6a2f0a9422bd831b04568708fef2b3a32e1f19350de849230df05f12946`): the Owner hit the wait again on `--done`; four points recorded above — the checkout switch pays `post-checkout` twice (70 %), the cache of `verdict_reports` per commit sha (80 %), `--html-only` in the background with a temp-file rename (75 %), a temporary worktree for `--done` (55 %, the Principal's judgement) — and the Rust port named a product decision, not this fix. The build (P2 #4; critical, the Owner's cold review) takes points 2 and 3 first, point 1 measured before it. |
