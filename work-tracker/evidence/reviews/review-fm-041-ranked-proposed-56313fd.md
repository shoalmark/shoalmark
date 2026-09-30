# Review — FM-041, a ranked open tracker sits in progress by rank (56313fd)

Reviewed: 56313fd25b4072f888cb70ee487142f02d03140f

- Seat: reviewer-62 (session 8e509911/reviewer-62), worktree shoalmark-review-2, 2026-09-30 13:08–13:55 CEST. Range: `origin/main` 7e7c8ac … 56313fd, five
  commits: d83ecd0 (tracker only), merge b81fcc8, a80a713 (code), a12bd74 (tests), 56313fd (docs). Tier: code, the full loop's first pass. Independence:
  same session (the Implementer is 8e509911/implementer-62). **Verdict: READY WITH FINDINGS — one P3, RV-2020, fixed forward; no P2.**

## Checks
1. The rule. `board()` (`shoalmark.py:746`) returns *progress* for `In Progress`, or a rank on `Proposed`; triage's test runs first; done is unchanged. Planted in
   a scratch `git archive` copy and regenerated, INDEX.md's Board column and the page's rows agree on all seven: ranked Proposed progress, ranked Parked backlog,
   ranked Closed done, unranked In Progress progress, ranked Proposed raised on path 5 triage, ranked Reserved backlog, ranked unjudged filing triage. A ranked
   Parked in *backlog* is right: a pass parks what nobody works on, and the tool says the contradiction, not hides it. `--check` refuses it by name (5938), a
   park verdict drops the rank (3885), so *Done when*'s "any status" holds on every tree the gate admits. Callers 2464, 3510, 6598: one definition. Built in the
   worktree (`--html-only`, 38 s), rendered in headless Chrome 154: *progress · 17* holds #1–#10 in rank order, FM-040 #4 and FM-028 #8 (Proposed) among them,
   then the unranked by tier — the caption is true.
2. Tests. The tip's tests next to `origin/main`'s tool (7e7c8ac, the same `shoalmark.py` as 2eb803b) give `test_core` 148 ok and 1 FAIL, the FM-041 check alone;
   `test_shoalmark`'s check, evaluated alone, returns `backlog` first on main. The suites ran once on the tip, behind the guard (it waited 13:14–13:20 for another
   loop's runner): python3 3.14.3 gave `test_core` 149 ok in 5 s and `test_shoalmark` 548 ok in 913 s; python3.9 3.9.6 gave 149 ok in 6 s and 548 ok in 913 s;
   0 failed, 0 skipped, as claimed. a12bd74's *149 others ok* on main is 148, a miscount in a message with nothing to fix.
3. The merge. `--remerge-diff` of b81fcc8 shows one conflict, INDEX.md (generated), resolved by regeneration; b81fcc8 differs from 7e7c8ac only in FM-041's
   status line and its INDEX row. d83ecd0 (tracker only, parent 2eb803b) sits before the merge and a80a713 (code) after it. The refusal is explained: at 2eb803b
   FM-041 had no `triaged:`, and the pass's P3 reached main in 1fc73b6 (PR 126). 2eb803b..7e7c8ac touches no `.py`, so the evidence at 2eb803b holds on main.
4. Docs. The CHANGELOG bullet sits under `## Unreleased — 0.19.0`, above main's plain `## Unreleased`, which is right: his word puts FM-041 in v0.19.0, and FM-024's
   branch has the same heading. `changes_since` reads only headings that open with a digit, so `--vendor` skips both; the provisional comment keeps the file sane.
   VERSION is untouched (0.18.6). Today's ship-log row says *Built on*. D3 holds: the added lines carry his one line of 10:40:31, marked, with no relay quoted and
   no hash added. The diff's one sha256 is main's 09-28 filing line, touched only for tense. See RV-2020.
5. Gates. `--check` 0 (INDEX up to date; every build commit under a judged In Progress tracker), `--session-check` 0, `merge-tree` clean (93f57d2, HEAD's tree).
   `--queue` at 13:14:20 CEST: *branch fm/041-… @ 56313fd wait: no pull request — no verdict on 56313fd*. Trailers on all five: `Co-Authored-By: Claude Sonnet
   5.5`, `Session: 8e509911/implementer-62`, `Worktree: shoalmark-impl-3`, with no `Model:` or `Effort:`. The four numbers (`--numstat origin/main...HEAD`), as
   claimed: records +8 −5 (FM-041 +5 −2, INDEX +3 −3), product +29 −2 (CHANGELOG +10, `shoalmark.py` +5 −2, tests +14); this file +45: +53/+29/−5/−2.
6. Disclosed slips (one unguarded 6 s `test_core` run; a placeholder agent spawned with no task): recorded as disclosed, no tier; nothing in the tree.

Quality read (build: Sonnet 5.5 at medium; counted neither for nor against the Owner's switch): clean — one expression, its rule and its why said, every case pinned.

## Findings
- RV-2020 · P3 · 80 % — FM-041's new paragraph opens **Shipped 2026-09-30 on `fm/041-…`**, yet the tracker is In Progress and nothing is merged. INDEX.md
  says `Shipped` means merged, and a branch build's form is *Built … on …, for …; open for review, not merged* (FM-011). It also names `origin/main` `2eb803b`,
  which was main at the cut; main is 7e7c8ac now, with the same tool. Fix forward: `**Shipped 2026-09-30 on` → `**Built 2026-09-30 on`; after `for v0.19.0` add
  `; open for review, not merged`; `` on `origin/main` `2eb803b` `` → `` on `origin/main` `7e7c8ac` (its tool unchanged since the cut, `2eb803b`) ``.

Unproven: a ranked Proposed tracker in *progress* never goes stale. `owed_a_pass` is unchanged by design, so neither `--triage` nor the page re-lists it; only a
pass re-ranks it, which is for a pass, not this slice. Only Chrome was tried, not Safari or Firefox.

Path 5 — a merge rules nothing.
