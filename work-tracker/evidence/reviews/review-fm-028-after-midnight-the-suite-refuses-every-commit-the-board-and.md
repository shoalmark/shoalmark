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
