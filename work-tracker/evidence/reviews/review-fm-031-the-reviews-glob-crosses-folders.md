# Review — the reviews glob crosses folders, at ba565e3 (2026-09-26 12:35 CEST, Reviewer, session `8e509911/reviewer-26`)

- **Date:** 2026-09-26, verified 12:20–12:50 CEST. **Seat:** Reviewer (`reviewer@seat`), session `8e509911/reviewer-26`,
  worktree `shoalmark-review-4`, detached at the tip.
- **Reviewed:** branch `fm/031-the-reviews-glob-crosses-folders`, tip `ba565e3aa118418b0a2744cfe275d80c9a245455`. It has
  two commits on `a7e5291` (`v0.18.4`), both by the Implementer seat (`Session: 8e509911/implementer-35`, `Worktree:
  shoalmark-impl-4`): `b256bd2` (12:07:56) files the line, and `ba565e3` (12:18:17) widens it. No pull request carries
  the branch yet (`gh pr list --head`, empty).
- **Tier: docs, one pass.** `git diff --name-only origin/main...HEAD` names FM-031's tracker only: 34 lines added, none
  removed.
- **Independence: same session.** This seat is a sub-agent of the branch's own session (`8e509911`), and `--check`
  counts it that way.
- **`origin/main` moved** to `5169398` (PR 82, FM-006's files only) after the brief's `a7e5291`. `shoalmark.py` is
  byte-identical at `a7e5291`, `5169398` and the tip, so every line cited below reads the same on either.

## What I ran

| run | result |
|---|---|
| `shoalmark.py` line 112 | `"paths": {"reviews": "evidence/reviews/"},` in `DEFAULTS` ✓ |
| lines 1321–1323 | 1321 `registry = f"{rel}/sessions.md"`; 1322 `folder = str({**DEFAULTS["paths"], **(CONFIG.get("paths") or {})}["reviews"]).strip().strip("/") + "/*"`; 1323 `in_folder = lambda x: … fnmatch.fnmatchcase(x[len(rel) + 1:], folder)` ✓. The line's `{…}` abbreviates the merge of the defaults with the configuration, a fair elision |
| line 1384 | `addenda_only` refuses a path unless `in_folder(x) or x == registry or (v in (None, sha) and own_review.match(x))`. `x == registry` holds whatever `[paths]` says, and `own_review` counts only for the verdict commit itself (or every commit, on the answer path) ✓ |
| the mechanism | as stated. `fnmatch`'s `*` matches `/`, so `evidence/*/` reads `evidence/*/*`, and the default reads `evidence/reviews/*` at any depth ✓ |
| **my reproduction**, a scratch repository under the session's scratchpad, never pushed | `v0.18.4`'s `shoalmark.py`, `--init --key msr`, six branches, each with a slice, a READY verdict (`Reviewed:` the slice, its file `evidence/MSR-400/review-the-slice.md`), then one later commit. `queue_actions` is called with hand-built pull requests, the suite's own stub. The table below |
| the PortDive citations, read from the parent's object store without a fetch or a checkout | RV-630 is `### RV-630 · P2` in `docs/work-tracker/evidence/PD-400/review-pd-400-the-pin-is-0-18-4.md` on `pd/400-the-pin-is-0-18-4`, and 11:16:13 is its commit `6a7368ce`'s clock ✓. `962a69c4` is on that branch, and its message quotes the closure test *run here at 11:55:26 CEST*, X5 (`evidence/reviews/note.md`) and X6 (`sessions.md`) ✓. The entry cites the parent's branch, path, id and commit only, and no internal state ✓ |
| the seat's proposal | the entry is dated (2026-09-26), names the seat and session, gives its sources, and marks the fix *this seat's proposal for the next release, not ruled* ✓ |
| the pointer sentence in *What is true now* | it names the glob, the default and *merge* over an unjudged head, and points to *Open lines* ✓ |
| the two ship-log rows | 11:57 files the line, and 12:08 widens it. Each matches its commit and the line. The 11:57 row is unchanged by `ba565e3` ✓. The order is R2 |
| front matter | untouched: the only hunks are at lines 100 and 218, and the front matter ends at line 11 ✓ |
| `--check` · `--session-check` | exit 0 (*108 verdict(s)*; *filing freeze: 21 open*) · exit 0 |
| `test_core.py` · `test_shoalmark.py`, by hand | exit 0, 148 ok · exit 0, 462 ok, 0 skipped |
| `git merge-tree --write-tree origin/main HEAD`, against `5169398` | clean (tree `ca08151`) |

**The reproduction.** `v0.18.4`, READY verdict, then one later commit:

| later commit touches only | no key (`evidence/reviews/`) | `reviews = "evidence/*/"` | `reviews = "evidence/*/review*"` |
|---|---|---|---|
| `evidence/x/results.csv`, `evidence/x/run/score.py` | wait: no verdict | **merge** | wait: no verdict |
| `evidence/x/review-2.md` | wait: no verdict | merge | wait: no verdict |
| `evidence/reviews/note.md` | **merge** | merge | wait: no verdict |
| `sessions.md` | **merge** | **merge** | **merge** |
| `evidence/x/reviews/data.csv` | wait: no verdict | merge | **merge** (R1) |
| `evidence/reviews/sub/tool.py` | **merge** | merge | wait: no verdict |

Each reading the line states is reproduced: `evidence/*/` admits results and a script, the default does not; the
narrowed key refuses a second `review-2.md`; with no key, `evidence/reviews/note.md` and `sessions.md` read *merge*;
and no key closes `sessions.md`.

**Note, not graded:** the `sessions.md` admission is vestigial. 0.18.0's CHANGELOG (line 312) says *Delete
`<tracker dir>/sessions.md` … Nothing reads or writes it any more*, and this repository has none, yet `queue_actions`
still reads it as a review addendum. This backs the proposal: the tool itself no longer writes the file, so dropping
the admission costs no tool-written commit. The line could cite it.

**Note, outside the diff and not graded:** the paragraph above the pointer, *Widened 2026-09-26, a line under the freeze
for 0.18.4*, still says *built … before the cut*. 0.18.4 is tagged (`a7e5291`), and its CHANGELOG says *Built in 0.18.4*.

## Findings

**R1 · P3 · confidence 0.9 · The narrowed key is described as matching nothing, but it admits any file under a `review*` folder.**
- The line says *`evidence/*/review*` becomes `evidence/*/review*/*` and matches no `review*.md` file*.
- Row 5 of the reproduction reads *merge* with that key: a later commit adding only `evidence/x/reviews/data.csv`, which
  is not a review. The pattern admits every file, at any depth, under any `evidence/<id>/review…/` folder. That includes
  a `review*.md` inside one, so *no `review*.md` file* is too strong as well.
- **Why it matters:** a consumer reading the line may take `evidence/*/review*` for an inert key. It still admits
  non-review files. The line's conclusion stands, and is stronger than written: the key cannot be narrowed to review
  files. The *Until then* sentence (*names no folder that holds non-review files*) already guards against it.
- **What closes it:** one clause, fixed forward. For example: *matches no `review*.md` directly under `evidence/<id>/`,
  and admits any file under a `review*` folder there*. The proposed fix (one path segment; the verdict session's own
  `review*.md` only) closes the behaviour too.

**R2 · P3 · confidence 0.9 on the facts · The ship log is not consistent, and the branch flips how the tool reads it.**
- On `main`, the log was already two blocks. Twelve rows run newest first (09-24 15:17 down to 08:24). Seven rows are
  appended below them oldest first (09-24 evening, 09-25, and 09-26, the answer-branch widening, the newest row on
  `main`). One of these says *the row of 20:24 above*.
- `ship_log_table` read `main`'s log as **oldest first**, because its first dated row (09-24) is older than its last
  (09-26). So a tool-written row (`--answer … revoke`, `--supersede`) would have landed at the bottom.
- The branch puts its two 09-26 rows on top. Rows dated 09-26 now sit at both ends, and the log reads in neither order.
  The tool now reads it **newest first** (first and last dates are equal), so its next row lands on top.
- Nothing is lost: every row is dated, and the log has no *superseded* row, so `superseded()` returns `""` either way.
- **Why it matters:** the log is the append-only record, and a reader, or the tool, cannot tell which end is newest. The
  house reading of *where the log's own order puts it* (FM-028's pass: *appended last in its oldest-first log*) would have
  put these rows last. The repository's stated order (`ship_log_table`: *this repository writes the newest on top*)
  would put them first. The branch followed the second against the tool's reading of this log.
- **What closes it:** fixed forward.
  - One way: move the two rows, which are not yet merged, under the 09-26 row at the bottom before the merge. That
    edits no merged row and restores the tool's oldest-first reading.
  - The other way: the Principal names one order for this log in a row of its own.
  - Merged rows are not reordered either way.

## Verdict

**READY WITH FINDINGS (R1 P3, R2 P3).**
- The mechanism is as stated at lines 112, 1321–1323 and 1384.
- Each reading the line reports reproduces in a scratch repository on `v0.18.4`, never pushed.
- The PortDive citations are the parent's branch, path, id and commit, and they check out.
- The entry is dated, sourced and marked as the seat's proposal, not ruled.
- The front matter is untouched, and the diff is the tracker only.
- `--check`, `--session-check` and both suites are green, and merge-tree against `origin/main` `5169398` is clean.
- R1 and R2 are fixed forward under the docs tier.

*The Owner lands this by merging, and a merge rules nothing (path 5).*
