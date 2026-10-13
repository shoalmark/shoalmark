# FM-045: 0.19.2's re-date at c458e4d, code tier

Verdict: **READY**. No finding; RV-2851 to RV-2859 are unused.
Reviewed: c458e4d76494b36fba8ec3128ae2d33f906cb35e. Scope: `git diff cee6292 c458e4d`, one commit. Tier: code.

## What holds

- Each of the six changed lines changes only the release day: 2026-10-10 to 2026-10-09, or 10 October 2026 to 9 October 2026. The changed lines are the CHANGELOG heading, the landing's footer line and its template comment, the footer check's string and name, and FM-045's lines 16 and 49.
- The footer line keeps the Owner's words, with only the date changed.
- The CHANGELOG heading `## 0.19.2 — 2026-10-09` and the footer's "released 9 October 2026" agree. No other 2026-10-10 or "10 October 2026" remains outside the evidence folder.
- FM-045 gives 2026-10-09 where it states the release date, and its ship log is unchanged.

## Commands: 2026-10-08, CEST, as `date` printed each

- At c458e4d: `py_compile` exit 0; `test_core.py` exit 0, all green; `--check` exit 0; `--session-check` exit 0 (20:53:08–20:53:30).
- run-one-check, two at a time (20:50:45–20:53:08):
  - at c458e4d: the footer check, the `--vendor` CHANGELOG block (4 checks) and the signed-identity texts check, each exit 0;
  - controls: the footer check exits 1 beside 9a7ed43's landing and beside cee6292's.

Quality read: the commit message and the changed lines say what is asserted; reads clean.
