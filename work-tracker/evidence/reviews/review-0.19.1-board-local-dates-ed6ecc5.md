# v0.19.1 — the board's page counts local calendar days, at ed6ecc5

Verdict: **READY**. RV-2380 (P3) is closed at ed6ecc5, and no finding stands against this change.
Reviewed: ed6ecc5ecb179ff2b688e28e5a5637cc8c4b1e89 — `git diff 8570dc2 ed6ecc5`, two commits to `shoalmark.py`, `test_core.py` and `test_shoalmark.py`.
Reviewer: b3bdb000/reviewer-92 (claude-opus-5-5, xhigh), at the reviewer's bot address, unsigned, in worktree shoalmark-review-11, on 2026-10-04. Tier: lower, the board's display; code.

- **`ago`, the page's one helper,** is the difference of two local calendar dates. It is used for the ask's age, the fresh badge and the verdict's stale mark, each with its threshold unchanged: fresh through day 7, stale from day 8.
  - For text that is not a bare date, it is NaN. No age is shown, and the judgement is neither fresh nor marked stale.
  - It agreed with Python's local-date count on 1,048,950 (instant, date) pairs, at every quarter hour across the clock changes of 2026–27.
  - Those pairs span 14 zones, among them three that change at midnight, UTC−12 and UTC+14.
  - `--standup` reads the count `--owner` reads.
- **RV-2380 (P3), closed at ed6ecc5:** where the page's probe sets no `data-probe`, or sets text that is not JSON, each of the three "days" checks fails and names the pin. The kept skips each go through `skip`, by the block's name: another zone or offset in Chrome, a zone not installed, a clock that cannot be pinned, and no `time.tzset`.
- **Source pins:** the two in `test_core.py` and the one in `test_shoalmark.py` pin `fresh` and the stale mark whole, each with its threshold.
- **Controls:**
  - Each of the three "days" checks exits 1 beside `1f73865`'s tool and 0 at ed6ecc5, 10:00:40–10:08:37 CEST.
  - Under `TZ=Etc/GMT+12`, the two FM-030 checks, *waiting for you* and the board's first words, exit 0 at ed6ecc5 and 1 beside `1f73865`'s tool, 10:08:39–10:14:19 CEST.
  - With the probe made to throw, or to set text that is not JSON, the block fails at ed6ecc5. Made to throw, it skips at 64f3528. These ran 10:14:19–10:17:02 CEST.
- **Commands:** at ed6ecc5, 10:03:45–10:04:01 CEST: `py_compile` ok; `test_core.py` 158 ok, all green, exit 0; `--check` and `--session-check` exit 0.
- **The CHANGELOG line** goes in with the VERSION bump. The check at `test_shoalmark.py` 1441–1443 holds the newest heading to VERSION.
- **The two commit messages and the new test names** say what is asserted.
