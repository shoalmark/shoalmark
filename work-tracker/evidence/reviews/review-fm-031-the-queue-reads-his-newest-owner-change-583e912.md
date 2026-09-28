# Scoped re-check — FM-031: the cold session's coverage list, as checks, at 583e912 (2026-09-28 22:15 CEST, Reviewer, session `8e509911/reviewer-54`)

Reviewed: 583e9126f8f231810e3f73ce98b1a595d421e59d
Session: 8e509911/reviewer-54

- **Scope.** `583e9126` is one commit on top of `0842ce8`, the Owner's cold verdict on `2185250` (READY, 21:44:11 CEST):
  the commit dated 21:47:54, pushed 22:10:01 per the standup ledger. My `git fetch origin` (no `--prune`) at checkout
  showed the branch at this sha, main at `50c3a104`; the worktree was clean before and after.
- **Tier: critical (scoped) under TRIAGE.md path line 3** — the branch is the queue's reader of the Owner's own acts;
  this pass is a scoped re-check of a tests-only commit sitting on an already-cold-READY tip, not a fresh reading of the
  reader itself.
- **Independence:** same session. I am a sub-agent of Principal session `8e509911`.
- **Verdict: READY.** The commit adds the cold session's own coverage list as checks, touches no production code, and
  every new assertion reads correctly against the tool's existing behaviour.

## Checks

| check | what I ran | result |
|---|---|---|
| (1) Scope — only tests + tracker changed, reader untouched | `git diff 0842ce8 583e9126 --stat`; `git diff 0842ce8 583e9126 -- shoalmark.py` | `2 files changed, 17 insertions(+), 6 deletions(-)`: `test_shoalmark.py` (+16/-6) and `work-tracker/FM-031-the-streams-run-in-parallel-and-only-the-owner-sees-the.md` (+1/-0). The `shoalmark.py` diff is empty |
| (2) The test diff itself | Read the full `0842ce8..583e9126` diff of `test_shoalmark.py` | Three name-bindings added (`r19_`, `r26_`, `r29_` now capture `record31_()`'s return, previously discarded) plus one new fixture row, `b31_(30)`: `truth31_()` inserts the refusal-shaped line directly under the `## What is true now` heading (an unsigned commit, in his name by construction), then `his31_(due31_)` lays his **signed** `due:` act on top of it, then `review31_` adds a review commit. `rec31_[30]` is asserted `== (f"wait: an unverified commit in your name on your answer branch ({f30_[:7]})", "")` — the forged commit still waits under his signed act. A new dict, `shapes31_`, calls `fm.refusal_record` directly (via the existing `_no_git_env` helper, the same pattern used elsewhere in this file, e.g. line 3801) on the raw commit shas: `True` for `r19_`, `r26_`, `r29_` (the tool's own placements) and `False` for `f25_`, `f27_`, `f28_`, `f30_` (the forged ones) — asserted `shapes31_ == {19: True, 25: False, 26: True, 27: False, 28: False, 29: True, 30: False}`. The check's title now names RV-712, RV-715 and RV-716, adding the `## What is true now` sentence and the `shapes31_` clause to its existing prose |
| (3) `record31_`/`append_record`, and the forged helpers | Read `record31_` (test_shoalmark.py:4989), `forged31_` (5001), `sections31_`/`tail31_` (5009/5014), `midacts31_` (5021), and `fm.append_record` (shoalmark.py:5569) | `record31_` builds its one line by calling `fm.append_record(body_, fm.ACTS_HEAD_RE, fm.HEAD["acts"], line)` — the tool's own placement function — never hand-rolled text splicing; rows 19, 26, 29 all go through it. Every forged fixture (`forged31_`, `tail31_`, `midacts31_`, `truth31_`) instead splices the string directly at a specific, non-tool location |
| (4) The five coverage items against the rows | Matched each item named in the brief to the diff | RV-715 line under `## What is true now`, signed `due:` above it → **row 30** (`truth31_` + `his31_(due31_)`). RV-716 genuine via `append_record` → **rows 19, 26, 29** (`record31_`). RV-716 forged at EOF inside `## Asks` → **row 27** (`sections31_` makes `## Acts`+`## Asks`, `tail31_` appends at EOF, landing inside `## Asks`). No existing `## Acts` accepted only where `append_record` creates it → **row 28** (`midacts31_` inserts a new `## Acts` before `## Done when`, not one of `append_record`'s two placements — still waits). Prefer `append_record` in genuine fixtures → **rows 19, 26, 29**, same as above — `record31_` is the only fixture that calls it |
| (5) FM-031's ship-log row | Top row (newest-first) of `work-tracker/FM-031-….md`'s log table | `2026-09-28 21:47 CEST`: states the Owner's cold READY on `2185250` at `0842ce8` (21:44:11, no findings, RV-717…719 not minted) and, after it, that this commit adds the cold session's listed coverage — the `## What is true now` line under his signed `due:` (row 30) and `refusal_record` asserted on all seven shapes (three `True`, four `False`) — the reader untouched. Matches the diff exactly |
| `--check` | `uptime` first (load 2.01, under 6); ran 22:13:29–22:14:03 CEST | Exit 0. `INDEX.md is up to date — 41 trackers`; the independence line printed over 164 verdicts; `judged before build: on`; `the Owner's two sections: guarded`; `filing freeze: 22 open, at or above 8 — only bug filings` |
| `--session-check` | 22:14:08 CEST | Exit 0, no output |
| Merge onto main | `git fetch origin main`; `git merge-tree --write-tree origin/main HEAD` | Clean, no conflict. Tree `3629e644ffc9dc641e6f82f0170792b8a66080f7`, main `50c3a104725d94781b20e756e9a427b294eea550` |
| `--queue` | 22:14:15–22:14:21 CEST | `branch fm/031-the-queue-reads-his-newe… @ 583e912  wait: no pull request — no verdict on 583e912` — as expected, before this review's commit is pushed |
| The hook's tests line | — | Not visible to me: I did not create `583e9126`, so I cannot see the pre-commit hook's console output for it. The standup ledger states the hook ran both suites on both Pythons for this commit; that is input to this pass, not a run of mine. No suite was run here — the tip changes no `.py` but `test_shoalmark.py`, and a suite of mine would be a second runner |

## Findings

None. No id minted from RV-747…749.

## Verdict

**READY.** The commit is exactly what it claims: the cold session's own coverage list, added as tests on top of an
already-cold-READY tip. `shoalmark.py` is untouched, the new row-30 fixture and the `shapes31_` dict both exercise real,
previously-undertested corners of `refusal_record` (the line directly under `## What is true now`, and a direct check
of the function on all seven shapes rather than only through the queue's read), every genuine fixture goes through the
tool's own `append_record`, every forged one does not, and the ship-log row states the change factually. The gates are
green and the merge onto main is clean.

path 5 — a merge rules nothing.

Trailer: this verdict's `Reviewed:` trailer rides the commit that adds this line — the reviewed tip is unchanged.
