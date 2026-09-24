# Review — FM-028 filed, at f9a7e49 (2026-09-24 08:20 CEST, Reviewer, session `8e509911/reviewer-1`)

**Checked, and true:**
- **The three clocks are cited correctly.**
  - `test_shoalmark.py:1282`: `old = (datetime.date.today() - …days=3)` is the local calendar.
  - `shoalmark.py:1241`: `Math.floor((Date.now()-Date.parse(t[29][2]))/864e5)` counts from UTC midnight.
  - `shoalmark.py:704–706`: `today = datetime.date.today()` … `(today - date.fromisoformat(ask_since)).days` is local.
- **The two zone runs are reproduced here.** `TZ=Etc/GMT-14 python3 test_shoalmark.py` exits 0 (264 ok).
  `TZ=Etc/GMT+12` exits 1 (263 ok, 1 FAIL), on *rendered: the board's first words …*. Its assertion is at `:1359`:
  `"waiting for you: 2 · oldest 3 days · holding up 2 more" in shown`.
- **The citation of `916cd26` is accurate:** it records exit 1 after midnight and exit 0 under `TZ=UTC`.
- **The rest:** the `TZ=UTC` workaround is named. FM-028 is free on `main`, on every other branch, and in the open PRs
  #33–#38. `-4` is closed and `-6` opened, in order. `--check` 0; `--session-check` 0. The branch's own diff (three-dot)
  is the tracker, one INDEX row and `sessions.md`.

**Findings:**

**R1 · P2 · The session id collides with another branch.** This branch opens `8e509911/implementer-6` (*file FM-028
…*, 07:41), and `f9a7e49` carries `Session: 8e509911/implementer-6`.
- PR #33/#37 (`fm/006-the-site-wears-the-pricke`) already holds `8e509911/implementer-6`, *the site wears the
  Pricke*, closed at 01:14.
- Once both land, the registry has one id for two sessions, and the trailer traces to either. *An id is used once*
  only holds per tree.
- This is FM-027's class, the next free id guessed on a branch. It also merges with a conflict in `sessions.md` onto
  `main` `cdd6e3f`.
- **What closes it:** a free id (the next unused `8e509911/implementer-<n>` across open branches), and a note that
  `f9a7e49`'s trailer names the old one. Not fixed here.

**R2 · P3 · `considered:` gives no reason for two of its three ids.** FM-024 is ruled out in the body (`:64`). FM-027
and FM-005 have no line saying why they are not this.

**Verdict:** NOT READY. R1 (P2) is open, and R2 is a P3.

## Re-verified at f8ccf60 (2026-09-24 09:16 CEST)

**Scope.** `30c4f89` → `f8ccf60`. The Implementer's five commits, `ab176a4` to `53a34a3`, all under
`8e509911/implementer-12`, opened first and closed last. Then the merge `f8ccf60`, by the principal seat under
`8e509911`, whose parents are `53a34a3` and `6da5d34` (PR 33 merged on `main`).

**R1 is closed, by ruling.**
- In `c60f300` the FM-028 row `8e509911/implementer-6` (opened 07:41) is closed at 08:49 and not renamed. Its scope
  cell records the collision: the same id names *the site wears the Pricke* (01:02–01:14), FM-027's class, and the
  registry is append-only (FM-024).
- **The gate behaviour in the ship log is confirmed in the code.** `session_problems` (`shoalmark.py:2620`)
  indexes rows by id, and the last row wins. So an ended row beside a later open row with the same id reads as a
  re-open (`:2626`).

**The simulation, repeated against the real `main`.**
- I ran it in a scratch clone against `6da5d34`, which contains `f2cc7bd`:
  - I merged `53a34a3` with `6da5d34` and resolved `sessions.md` myself as a union in opened order. `--check`
    was 0.
  - Then one more seat commit (reviewer), which does not touch the registry: `--session-check` 0, `--check` 0.
  - The same, with FM-028's -6 row left open: `--session-check` 4, *re-opens 8e509911/implementer-6, which had
    ended*.
- My resolution of the registry is byte-identical to the one at `f8ccf60`.

**The unions: no row lost or doubled.**
- At `64f7b99` (with `main` `3ba7383`): 21 ids, the same set as both sides, in opened order, none doubled. The
  row `implementer-4` takes the branch's end (07:41) over `main`'s open cell, and an ended session stays ended.
- At `f8ccf60`: 24 ids in 25 rows, in opened order. The only id with two rows is `-6`, and both rows are closed.
- **`f8ccf60` brings only `main`'s files.** Against `53a34a3` it changes 21 files: 20 are byte-identical to
  `6da5d34`, and the 21st is the registry, which gains `main`'s four rows (-6 at 01:02, -7, -8, -9).
- INDEX is unchanged against `53a34a3`, as expected: `main`'s INDEX differs from the branch's only by FM-028's row.

**R2 is closed.** `considered: FM-024, FM-027, FM-005`, and the body now gives the reason for FM-027 (which number,
not which date) and for FM-005 (the ask's design, not a defect in shipped code).

**The rest.**
- None of the six commit messages from `ab176a4` to `f8ccf60` carries a pull-request number with the sign.
- The archive ref is still on the server and points at `30c4f89`, and the twin PR 41 is still open. Both are the
  Owner's to remove, as the ship log says.
- Gates at `f8ccf60`: `--check` 0; `--session-check` 0; `test_shoalmark.py` 0 (264 ok); `test_core.py` 0 (148
  ok).
- `6da5d34` is an ancestor, so the merge into `origin/main` is a fast-forward.

**Noted, not this branch's:** on `main`, the row `8e509911/implementer-9` (the tagline slice) is still open.

**Verdict:** READY TO TAG. R1 is closed by ruling and R2 is closed. No finding is open.

## Re-verified at 3131e8c (2026-09-24 09:24 CEST)

**Scope.** `3131e8c` is the principal seat's merge (under `8e509911`) of `main` `9bde71f` (PR 36 and PR 40
merged) into my verdict commit `6a9fa8f`.

**It brings only `main`'s files, the registry and INDEX.**
- Against `6a9fa8f` it changes 6 files. Four are byte-identical to `9bde71f`: FM-011's and FM-031's trackers, and
  their review files.
- The registry gains one row, `8e509911/implementer-13` (08:50–08:56), and changes no other.
- INDEX differs from `main`'s only by FM-028's row and the count (29 against 28).

**The registry loses and doubles nothing.** It has 25 ids in 26 rows, the same id set as both parents, in opened
order, and no cell differs from either parent. The two closed rows under `8e509911/implementer-6` (01:02–01:14 and
07:41–08:49) still stand.

**Gates at `3131e8c`.** `--check` 0; `--session-check` 0; `test_shoalmark.py` 0 (264 ok); `test_core.py` 0 (148
ok). `main` `9bde71f` is an ancestor, so the merge is a fast-forward. The commit message carries no `#N`.

**For FM-032:** this is the third merge of `main` that this pull request has paid for (`64f7b99`, `f8ccf60`,
`3131e8c`), each forced by the registry and INDEX that every branch writes, not by any change to FM-028's own work.

**Verdict:** READY TO TAG. No finding is open.
