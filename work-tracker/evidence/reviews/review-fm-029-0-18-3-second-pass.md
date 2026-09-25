# 0.18.3 — cold Reviewer, second pass on `797df44`

**Verdict: NOT READY. Tier: code, full loop.** Reviewed
`797df44cfbfe21672a220e4b9f9b8ed64320ad32`. This is the same cold Reviewer session `01a0d6e7`, started by
the Owner on his signed answer to FM-024, independent of building session `8e509911`. The tier follows
`git diff --name-only origin/main...HEAD`: code, tests, configuration, hooks, documentation and trackers change.
This file follows the first verdict on `8d46957` in `review-fm-029-0-18-3-cold-gate.md`. I verified; I did not
fix the build.

## What I ran

- `git log d79949f..797df44` and the diffs of `1023584`, `5e9e4f9`, `65d7266`, `da4fb98`, and the main merge:
  the original R1 probe is addressed by a `commit-msg` hook; prior R3's vendored path number and R4's stale
  AGENTS.md sentence are gone; the INDEX claim now excludes the generated date. The reviewed tip is the merge of
  main, then at `6e98d73`.
- `python3 test_shoalmark.py`: exit 0, 385 `ok` checks, `all green`. `python3 test_core.py`: exit 0, 148 `ok`
  checks, `all green`.
- `python3 shoalmark.py --check`: exit 0, `work-tracker/INDEX.md is up to date — 34 trackers` and `judged before
  build: on — 15 commit(s) on a detached HEAD since origin/main, every build commit under a judged In Progress
  tracker`. `python3 shoalmark.py --session-check`: exit 0. The worktree stayed clean.
- `judge_commits(commit_list(sha+'^..'+sha), '')` refused each historical first build: `89e0586` (FM-024 not
  judged), `3c0754f` (FM-032 not judged and Proposed), `90d3d6f` (FM-031 likewise), `bd7d5ea` (no tracker),
  and `4dfb999` (FM-029 not judged and Proposed). The current branch history passes the gate.
- In a scratch clone of `797df44`, with Lefthook installed and `seat.session = 01a0d6e7`, staged
  `gate-probe.txt` on `fm/029-probe` and ran `git commit -m 'FM-007: gate probe'`. `commit-msg` exited 4 with
  `refused: this commit "FM-007: gate probe" ... FM-007: not In Progress (Proposed)`; HEAD stayed `797df44`.
  The inverse, `FM-029: inverse gate probe` on `fm/007-inverse`, committed and passed `--check` with the signers
  file configured. R1 of the first verdict is closed for ordinary subjects. The new boundary in R1 below fails.
- The temporary-repository tests exercise `--answer`'s next moves and revoke/supersede after the flip, raises
  dated strictly after `triaged:`, the RAISED worksheet and board cells, an unrelated raise, a missing signed
  rule, a same-day raise, and a re-judgement. FM-007's same-day raise remains not owed. `--schema` names
  `action` for a yes needing the Owner's hands. The queue's no-pull-request case is tested with a bare remote and
  stubbed `gh`. Rule 4 says the seat judges, the Owner lands, and a merge rules nothing without a path number in
  vendored text. The 0.18.0 CHANGELOG bullet names its authority; `9409cba` still carries the evening R7–R10
  corrections. `VERSION` is `0.18.3`, and the release section names its trackers and checks.
- A second fresh clone of `797df44` without a signers setting: `--check` exited 4, one `checkout:` line, no
  `STALE`, and `INDEX.md is up to date`; with `work-tracker/allowed_signers`, it exited 0. The date test now
  states the normalized-index contract. The no-signers line has the counting issue in R4.
- On `origin/main` as fetched after the review began, `git merge-tree --write-tree origin/main HEAD` exited 1:
  `CONFLICT (content): Merge conflict in work-tracker/TRIAGE.md`. `--queue` reported PR 65 as
  `wait: conflict in work-tracker/TRIAGE.md`. Main had advanced from `6e98d73` to `7f492a5` (PR 68) while this
  pass ran. This is R3 below.

## Findings

**R1 · P2 · confidence high — a literal `#` subject still bypasses the commit-time gate.** In the scratch clone
on `fm/029-comment`, I staged `gate-comment.txt` and ran
`git commit -m '# FM-007: comment subject probe'`. The installed `commit-msg` hook printed `judged ✓`, and Git
made `a185e28` with that literal subject. `--check` then exited 4:
`refused: commit a185e28 "# FM-007: comment subject probe" changes gate-comment.txt ... FM-007: not In Progress
(Proposed)`. `message_subject` skips any line starting `#`, although `git commit -m` preserves this literal
subject. It returns an empty subject; `commit_msg_check` skips judgement. The same commit is then refused by
history. The fix needs the hook's subject to match the subject Git actually writes for `-m` and for edited
messages. Both scratch commits stayed local.

**R2 · P2 · confidence high — FM-031's older answer again lacks a relation in the board view.** The merge of main
added a second `## Asks` record to FM-031. Its first record, written before 0.18.1, has no `**relation** —`
line; the second has `accepted the proposal`. After `python3 shoalmark.py --html-only`, the generated
`work-tracker/view/FM-031.js` has **two** `**answered**` lines and **one** `**relation**` line. The old answer
still reads only `accepted - one channel ...` in the view, where it should read `accepted with a change` from
`7c97c5b` (verified on the first pass). `recorded_relation`, `unrelated_answer`, and `write_views` only inspect
`newest_record`, so adding a newer answer hides recovery for every earlier record. The 0.18.3 claim is that a
record written before 0.18.1 prints its relation on every reading; the actual FM-031 record no longer does.

**R3 · P2 · confidence high — the reviewed branch cannot merge into current main.** After PR 68 moved
`origin/main` to `7f492a5`, `git merge-tree --write-tree origin/main 797df44` exited 1 with a content conflict
in `work-tracker/TRIAGE.md`; `--queue` agrees. The branch was clean against the main it merged at `6e98d73`.
The Principal must integrate the current main and resolve the paragraph before a ready verdict can support a
merge. This is an integration finding against the current branch state, not a claim that `797df44` was born
conflicted.

**R4 · P3 · confidence high — the checkout diagnostic counts duplicate commits.** The fresh clone without a
signers setting prints one cause line, as promised, but says `8 signed commit(s) it could not check`. That line
repeats `FM-007 1034602c96`, `FM-024 64f843ef3a`, and `FM-032 97fa87a5d9` twice; it names five distinct
commit ids. Count unique commits, or call the eight entries checks rather than signed commits.

The first verdict's R2–R4 are closed by the new wording and edits. The broader FM-030 accepted-action promise
remains open in its own tracker and is outside this release's FM-030 slice. I did not inspect the sealed Auditor
session. The second pass did not find another material discrepancy in the other release claims.

## Verdict

**NOT READY:** R1–R3 are P2. R4 is P3. The suites and branch gate pass, but the commit-time gate and the
actual FM-031 record fail the release claims, and the branch currently conflicts with main. The code tier
requires a fix and verification of the resulting tip.

The Owner lands this by merging and tags v0.18.3; a merge rules nothing (path 5).
