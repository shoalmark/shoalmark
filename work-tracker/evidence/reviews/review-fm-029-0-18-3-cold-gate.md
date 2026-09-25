# 0.18.3 — cold review of `8d46957`

**Verdict: NOT READY. Tier: code, full loop.** Reviewed
`8d469576ebcf7b6c6849092ef00fa72c61a89129`. This is a cold Reviewer session started by the Owner on his answer
to FM-024, session `01a0d6e7`, independent of the building session `8e509911`. The tier follows
`git diff --name-only origin/main...HEAD`: `shoalmark.py`, tests, configuration, a hook's workflow, documentation and
trackers change. The Reviewer verified and did not fix the build.

## What I ran

- `python3 test_shoalmark.py`: exit 0, 383 checks, `all green`.
- `python3 test_core.py`: exit 0, 148 checks, `all green`.
- `python3 shoalmark.py --check`: exit 0, `work-tracker/INDEX.md is up to date — 34 trackers`,
  `judged before build: on — 10 commit(s) on a detached HEAD since origin/main, every build commit under a judged In Progress tracker`.
- `python3 shoalmark.py --session-check`: exit 0. `git merge-tree --write-tree origin/main HEAD`: clean, tree
  `13dede1280eb5ad880754842fa606511c1d0cc67`.
- `python3 shoalmark.py --schema`: `ask-kind:` says a yes needing the Owner's hands is `action`; `next:` says the answer
  writes `build` after ruling, determination or ceremony, and keeps `owner` for action. The tests exercise accept,
  revoke and supersede in a temporary repository.
- `python3 shoalmark.py --queue`: `branch fm/029-… @ 8d46957  wait: no pull request — no verdict on 8d46957`, and
  `2 waiting on you: 0 merge, 0 close, 1 wait, 1 pushed without a pull request`. The new test also exercises the
  no-pull-request case with a bare remote and a stubbed `gh`.
- On the branch's FM-031 and FM-032 records, `record_relation` returned `accepted with a change` from `7c97c5b`
  and `accepted the proposal` from `ffa63b8`. The new test also exercised an absent answer commit, a relation line
  already present, batching, `--answered`, and the board view. A load makes no relation-recovery git call.
- Against the five historical build commits, `judge_commits(commit_list(sha+'^..'+sha), '')` refused `89e0586`
  (FM-024 not judged), `3c0754f` (FM-032 not judged and Proposed), `90d3d6f` (FM-031 likewise), `bd7d5ea`
  (names no tracker), and `4dfb999` (FM-029 not judged and Proposed). The branch's build commits pass at their
  parents.
- The raised-tracker tests cover a later `## Raised` line naming path 5 or a signed answer, a same-day line,
  unrelated text, a missing path/answer, a done tracker, the board and worksheet RAISED cells, and re-judgement.
  FM-007's same-day raise and pass are not owed another pass. Rule 4 in the tool and README says the seat judges and
  a merge rules nothing. The 0.18.0 revoke/supersede bullet names the Owner's authority without an RV id. Commit
  `9409cba` appends the evening review's R7–R10 corrections.
- A fresh clone of this worktree with no `gpg.ssh.allowedSignersFile`: `--check` exited 4 with one `checkout:` line
  for two unverified signed commits, and no `STALE`. With `work-tracker/allowed_signers` configured, it exited 0
  with `INDEX.md is up to date`. Generating the INDEX in the clone produced the date difference in R2.
- `VERSION` is `0.18.3`; the `## 0.18.3` CHANGELOG section names FM-029, FM-030, FM-031, FM-033 and FM-034 and
  their checks. `git status --porcelain` in the review worktree was empty after the checks.

## Findings

**R1 · P2 · confidence high — the commit hook accepts a build under the wrong tracker.** In a scratch clone of
`8d46957`, I installed Lefthook, set `seat.session = 01a0d6e7`, switched to `fm/029-probe`, staged a new
`gate-probe.txt`, and ran `git commit -m 'FM-007: gate probe'`. The installed pre-commit hook printed `session ✓`
and made `dab9475` with exit 0. Its `--session-check` knows only the branch and judged this as FM-029, which is In
Progress. The commit subject names FM-007 first, which is Proposed. `python3 shoalmark.py --check` then exited 4:
`refused: commit dab9475 "FM-007: gate probe" changes gate-probe.txt outside work-tracker/ — FM-007: not In Progress
(Proposed)`. This is the same commit, with no changed tracker state. `named_trackers` uses the subject before the
branch in history, while the pre-commit call to `judge_commits` passes an empty subject. The promised commit-time
refusal can therefore be bypassed by committing on a judged branch with an unready tracker in the subject. The fix
must make the commit-time and history checks agree; an actual commit must be refused before it is made. The scratch
commit was local only and is not on the reviewed branch.

**R2 · P3 · confidence high — the brief's byte-identity claim fails across the day boundary.** The committed
`work-tracker/INDEX.md` says `Generated 2026-09-24`. In a fresh clone on 2026-09-25, `python3 shoalmark.py` changed
only that line to `Generated 2026-09-25`; `git diff --exit-code -- work-tracker/INDEX.md` exited 1. `--check` correctly
normalizes the date and reports the INDEX up to date, with or without the signers setting. The brief's requirement
that the committed INDEX be byte-identical to either clone's generated file is false on the review date. Clarify that
claim or remove the date from the generated file if byte identity across days is required.

**R3 · P3 · confidence high — rule 4's vendored text hard-codes this repository's path 5.**
`shoalmark.py`'s `TRIAGE_RULES` and README §4 end `a merge rules nothing (path 5)`. A consumer's path 5 may say
something else. Keep the no-merge-ruling rule, but do not attach this repository's path number to the vendored rule.
This was flagged in the brief.

**R4 · P3 · confidence high — AGENTS.md describes the gate as still pending.** Its FM-033 bullet ends `the gate ...
builds under FM-033`, while this branch builds and enables it. Update the wording with the release. This was flagged
in the brief.

FM-030's broader accepted-action promise remains open in its tracker: an answered action is excluded from `--owner`
and `--standup`. The 0.18.3 claim is expressly its second widening, the `next:` change, so this is not a finding
against that slice. No other material discrepancy was found in the claims tested above.

## Verdict

**NOT READY:** R1 is P2. The code tier requires a fix and a fresh verification of the new branch tip. R2–R4 are P3.
The tool suites, release files, historical refusals and the current `--check` pass, but the installed hook failed to
refuse a commit that the new history gate rejects.

The Owner lands this by merging and tags v0.18.3; a merge rules nothing (path 5).
