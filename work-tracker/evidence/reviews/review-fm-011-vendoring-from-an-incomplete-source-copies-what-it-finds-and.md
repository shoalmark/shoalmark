# Review — FM-011 set to Shipped, at 86a4540 (2026-09-24 08:22 CEST, Reviewer, session `8e509911/reviewer-1`)

- **The diff from `main`** (three-dot) is `status: In Progress` → `Shipped`, `rank: 1` removed, one ship-log row,
  and the regenerated INDEX. Nothing else.
- **The row's facts hold:**
  - `v0.17.8` points at `62db9f8`, the merge of PR #20.
  - The tag is lightweight, so its time is the commit's: 2026-09-23 21:15:46 +0200, which is *≈ 21:16 CEST*.
  - R2 (P3, a hand-moved manifest reads as none) is kept open, as the 0.17.8 review left it.
- **INDEX** shows FM-011 as *Shipped · done*, and gone from the ranked table.
- **Gates:** `--check` 0; `--session-check` 0. Shipped is a terminal status, and the principal seat holds the close
  right.
- **R1 · P3:** the row carries a date without a time or zone, and its *07:56 CEST* for the flip disagrees with git
  (`86a4540` is 08:02:44 +0200).
- **Verdict:** READY WITH FINDINGS. R1 is a P3; R2 of the 0.17.8 review stays open as the row says.

## Re-verified at 3d205d4 (2026-09-24 08:33 CEST)

- **`git diff 9a43e86 3d205d4`** is one cell of the FM-011 row: *07:56 CEST* → *08:02 CEST (`86a4540`, its commit
  date 08:02:44 +02:00 — not the seat's clock, which had said 07:56)*. INDEX is unchanged, as it should be.
- **Git** has `86a4540` at 2026-09-24 08:02:44 +0200, so the row agrees. R1 is closed.
- **Gates:** `--check` 0; `--session-check` 0; `test_shoalmark.py` exit 0 (264 ok); `test_core.py` exit 0 (148 ok).
- **Verdict:** READY TO TAG. The 0.17.8 review's R2 (P3) stays open, as the row says.
