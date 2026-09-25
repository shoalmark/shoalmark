---
id: FM-028
status: Proposed
considered: FM-024, FM-027, FM-005
tags: bug
next: build
triaged: 2026-09-24
rank: 7
tier: P2
hook: "Between midnight and two in the morning the pre-commit suite refused every commit; they went through only with TZ=UTC. The board counts an ask's age from UTC midnight while the suite and --standup count it by the local calendar, so for the hours the two dates differ they disagree by a day."
---

# FM-028 — After midnight the suite refuses every commit: the board and the tool count days by different clocks

## What is true now

**Filed 2026-09-24; nothing is built.** Found on 0.17.8 (`v0.17.8` = `62db9f8`; `main` at `474794b`).

**What happened.** In the night of 2026-09-23 to 09-24, between 00:00 and 02:00 CEST, the pre-commit suite failed on
every commit in this repository and blocked it. Commits went through only as
`TZ=UTC git -c commit.gpgsign=false commit`. **That is the workaround:** with `TZ=UTC` the local date and the UTC date
are the same date, and the two clocks below agree.

**Why: one age, two clocks.**

| side | where | how it counts |
|---|---|---|
| the suite's fixture | `test_shoalmark.py:1282` | `old = (datetime.date.today() - datetime.timedelta(days=3)).isoformat()` — the **local** calendar |
| the board | `shoalmark.py:1241` | `Math.floor((Date.now()-Date.parse(t[29][2]))/864e5)` — `Date.parse("YYYY-MM-DD")` is **UTC** midnight |
| `--owner`, `--standup` | `shoalmark.py:704–706` | `today = datetime.date.today()` … `(today - date.fromisoformat(ask_since)).days` — the **local** calendar |

Whenever the local date and the UTC date differ, the board's *oldest N days* is one day off. So this is not only the
test: **the tool disagrees with itself**. The board says one age, `--standup` another, for the same ask. In Central
Europe the dates differ from 00:00 to 01:00 (CET) or to 02:00 (CEST), with local time ahead of UTC. The board then says
2 days where the suite expects 3. The same UTC reading sits in the board's triage freshness (`shoalmark.py:1199`,
`fresh`) and the viewer's stale mark (`:1323`), while the triage worksheet dates by the local calendar. Those two are
**not measured**.

**Reproduced 2026-09-24 07:37 CEST, without waiting for midnight.** A zone behind UTC gives the same disagreement with
the opposite sign.

| `TZ` | local · UTC | `test_shoalmark.py` | the board, for an ask three local days old | `--standup` |
|---|---|---|---|---|
| `Etc/GMT-14` | 2026-09-24 19:34 · 05:34 | exit 0 | *oldest 3 days* | *3 day(s)* |
| `Etc/GMT+12` | 2026-09-23 17:37 · 05:37 | **exit 1** | *oldest 4 days* | *3 day(s)* |

`test_core.py` passed in both zones. The one failing check (evidence below), whose assertion is
`"waiting for you: 2 · oldest 3 days · holding up 2 more" in shown` (`test_shoalmark.py:1359`):

```
  FAIL  rendered: the board's first words are the answer — how many wait, the oldest, what is held up — then each question, the oldest first, before the path and before any table
```

The board and `--standup` columns come from a minimal repro: a scratch repository with one ask dated as
`test_shoalmark.py:1282` dates it, the board read in headless Chrome, `--standup` run beside it.

**Last night's direction, local ahead of UTC, was reproduced before this filing.** The Reviewer did it at 01:0x CEST
on 2026-09-24, in commit **`916cd26`** (`work-tracker/evidence/reviews/review-fm-006-the-mark-ruled-the-pricke.md`, on
`fm/006-the-mark-ruled-the-pricke`; that branch's PR #27 was closed, so the sha is the reference, not a path on `main`).
`test_shoalmark.py` failed the same one check (*rendered: the board's first words …*) with exit 1, and passed under
`TZ=UTC` with exit 0. The zone runs above cover the other sign. At 07:37 CEST, local-ahead needs UTC+19, and no zone is
that far ahead.

**Kind of problem: proposed *complicated* (found by reading, once measured), not written.** `kind-of-problem:` is a
triage key, and the implementer seat holds no `triage` right: the gate refused it on this filing. The Principal sets it.

**The session gate is not involved** (`--related` FM-024 checked): `session_now()` writes local wall-clock text, and
the abandoned-row rule compares epoch seconds (`shoalmark.py:2506`, `:2674`). Neither parses a date as UTC midnight.

**Not a slice of FM-027 or of FM-005** (the other two ids in `considered:`).
- **FM-027** claims a tracker's id on the server so that two branches cannot take the same number. It decides *which
  number* a record gets; FM-028 is *which date* a surface counts from. None of FM-027's candidates reads a date or a
  zone, and building any of them changes nothing here. The two meet only in this filing's own record: its session id
  `8e509911/implementer-6` was guessed on a branch (R1, `sessions.md`). That collision is FM-027's class, not FM-028's
  subject.
- **FM-005** designs how the Owner is asked: the mandate, asks with defaults and deadlines, the digest, a shadow week.
  Its claims are verified by his calendar. FM-028 is a defect in shipped code: an ask's age, already on the board and in
  `--owner` and `--standup`, is counted by two clocks. The fix adds or changes no ask, default or deadline, and its done
  when is the suite at any hour in any zone, not one of FM-005's claims. FM-005 only gains an age that is one number.

**Intent, proposed by the filing seat.** `intent:` is the Owner's words only, so this is his to adopt, change or strike:

- **for** — a tool that lets its seats and its Owner commit at any hour, in any zone;
- **so that** — every surface counts an age by one clock, and no commit is refused by the clock alone;
- **never** — a gate that passes or fails by the hour it runs.

## Candidates considered

1. **Pin the suite's clock to UTC** (`TZ=UTC` in the hook or at the suite's top). One line, and it unblocks commits.
   It hides the tool's own disagreement, though: the board and `--standup` still differ for every user near midnight.
2. **Make the tool date by local time everywhere.** The board would compute an age from local midnight
   (`new Date(y, m-1, d)` instead of `Date.parse(iso)`), in `days`, `fresh` and the stale mark. Board, `--standup` and
   the suite's local fixture then agree.
3. **Freeze the clock in tests.** A fixed *today* goes into the tool, and a fixed `Date.now` into the page. The suite
   becomes deterministic at any hour, but the product disagreement stays unless (2) is done as well.

None is chosen here. The Principal or the Owner rules.

## Why

A gate that fails by the hour teaches people to step around it: `TZ=UTC` last night, `--no-verify` next. And the board
telling the Owner an age that `--standup` contradicts is a small untruth on the page he reads first.

## Done when

- One clock for an ask's age on the board, in `--owner` and in `--standup` — and for triage freshness — whichever
  candidate is chosen.
- The suite passes at any hour in any zone, with a check run on both sides of UTC across a date boundary.
- The `TZ=UTC` workaround is not needed.

## Evidence

- **Prior:** `916cd26` (the Reviewer, 2026-09-24 01:0x CEST). At local time after midnight, `test_shoalmark.py` failed
  the board's first-words check with exit 1; under `TZ=UTC` it passed with exit 0.
- `Etc/GMT+12`, 2026-09-24 07:37 CEST: `python3 test_shoalmark.py` → exit 1, one failing check (above).
  `Etc/GMT-14`: exit 0. `test_core.py`: exit 0 in both zones.
- The minimal repro, in both zones: board *oldest 3 days* and `--standup` *3 day(s)* at `Etc/GMT-14`; board *oldest 4
  days* and `--standup` *3 day(s)* at `Etc/GMT+12`.

## Ship log

| Date | Event |
|---|---|
| 2026-09-24 | Filed, citing the Reviewer's reproduction after midnight (`916cd26`: exit 1 local, exit 0 under `TZ=UTC`). Reproduced on 0.17.8 at 07:37 CEST: `Etc/GMT-14` passes, `Etc/GMT+12` fails the board's first-words check. A minimal repro shows the board and `--standup` giving one ask two ages. Workaround named: `TZ=UTC`. Nothing built. |
| 2026-09-24 | 08:54 CEST, the Reviewer's R1 and R2 (`30c4f89`) answered. R1 ruled by the Principal: the registry is append-only, the duplicate id is recorded in the row and the row closed; FM-027 (ids claimed on the server) is the cure. Found on the way: the session gate indexes rows by id, so two rows with one id read as a re-open once both are on main — a tool bug of FM-027's class, to be carried into FM-031's slice S1. Simulated: this branch merged with PR #33's tip `f2cc7bd`, both -6 rows closed, then a further seat commit — `--check` 0, `--session-check` 0; with this filing's row still open, `--session-check` 4, *re-opens 8e509911/implementer-6*. An archive ref (`archive/fm-028-first-filing-implementer-6` → `30c4f89`) pushed at ≈ 08:46 CEST on a route not taken spawned a twin pull request #41 by a banner press; the Owner closes it and deletes the ref — a seat pushes no side refs from here on. R2: why FM-028 is not a slice of FM-027 or FM-005 written beside FM-024's. `main` merged in at `3ba7383`. |
| 2026-09-25 | A line under the freeze for 0.18.4, on the Auditor seat's item 2 through the Owner (15:34:27): a pass cannot be replayed on a later day — `--triage` reads the machine's date only (`shoalmark.py:5043`), so a Reviewer replaying a day's worksheet the next morning gets the next day's sheet and dates. Proposed: an explicit day for `--triage` (`--triage --day 2026-09-25`), and a suite case that replays a pass the next day and reaches the same tree. |
| 2026-09-25 | The Auditor seat's addendum, through the Owner at 15:52:59 (as pasted): *FM-028 --day: the replay reaches the same tree only if the day also reaches INDEX.md's "Generated" line (shoalmark.py:5077, printed at :5089), not just --triage at :5043.* — so `--day` governs the generator's date too, or the replay is the same tree only under `drift_normalize`; the 0.18.4 line takes both places. |
