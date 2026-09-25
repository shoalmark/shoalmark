# 0.18.3 — cold Reviewer, fourth pass on `8c3c10b` (PR 65)

**Verdict: READY. Tier: code, full loop.** Reviewed
`8c3c10bf46431a68254e385e4abf467f454b1cad`. This is the cold Reviewer session `01a0d6e7`, started by the
Owner on his signed answer to FM-024, independent of building session `8e509911`. The tier follows `git diff
--name-only origin/main...HEAD`: code, tests, configuration, hooks, documentation and trackers change. The three
earlier verdict files record the first, second and third passes. This pass verified the new tip and fixed nothing.

## What I ran and found

- `git show 8c3c10b` and its four changed paths: the recovery now keys each old record by normalized question and
  answer. It reads candidate answer commits and uses one only when exactly one revision holds both; ambiguous or
  missing pairs read *relation not computable*. The README and CHANGELOG describe the same rule.
- I reran the third pass's temporary Git history with two cleared records, both answered `accepted - yes`.
  `Pick one?` proposed `yes` and was answered in `50301a5`; `Pick again?` proposed `no` and was answered in
  `3731cd0`. The board view now gives the first *accepted the proposal · read from 50301a5*, and the second
  *accepted with a change · read from 3731cd0*. The new suite also checks identical question and answer text
  answered twice: neither record is assigned a guessed commit. R1 of the third pass is closed.
- `python3 shoalmark.py --html-only`: FM-031's board view has two answers and two relations, its older record
  *accepted with a change* from `7c97c5b`; FM-032's older record resolves from `ffa63b8`. A record with no
  matching or unique commit reads *relation not computable*; the suite checks that a load makes no recovery git
  call and the print path batches its `git log`. The live FM-007 record already carries a relation line; the new
  test reads its real two same-text answer commits without that line and gets *not computable*.
- `python3 test_shoalmark.py`: exit 0, 394 `ok` checks, `all green`.
  `python3 test_core.py`: exit 0, 148 `ok` checks, `all green`.
- `python3 shoalmark.py --check`: exit 0, `work-tracker/INDEX.md is up to date — 34 trackers`,
  `judged before build: on — 21 commit(s) on a detached HEAD since origin/main, every build commit under a
  judged In Progress tracker`. `python3 shoalmark.py --session-check`: exit 0. The worktree stayed clean.
- `judge_commits(commit_list(sha+'^..'+sha), '')` refused all five historical first builds: `89e0586`,
  `3c0754f`, `90d3d6f`, `bd7d5ea`, `4dfb999`. In a scratch clone with Lefthook installed, a staged
  `gate-probe.txt` on `fm/029-probe` and `git commit -m 'FM-023: gate probe'` was refused before a commit was
  made: `FM-023: Parked`. The branch gate on the actual PR head is green. The Principal's stated ruling treats
  the hook as best-effort and `--check` on the branch as the merge gate.
- A fresh clone without `gpg.ssh.allowedSignersFile`: `--check` exited 4 with one `checkout:` line naming four
  distinct commits, no `STALE`, and `INDEX.md is up to date`. With `work-tracker/allowed_signers` configured,
  `--check` exited 0. The generated INDEX is the committed one on this date; across dates the tool explicitly
  normalizes the `Generated` line for drift.
- The temporary-repository tests cover `--answer`'s `next: build` for ruling, determination and ceremony,
  `next: owner` for action, revoke and supersede after the move, signed-rule raises and the RAISED worksheet,
  and `--queue` for a pushed branch without a PR using a bare remote and stubbed `gh`. `--schema` names an
  Owner-hands yes as `action`. FM-007's current `raised` set is empty: its same-day raise was re-judged.
- The 0.18.0 revoke/supersede bullet names its authority; rule 4 says the seat judges and the Owner lands, and
  its vendored text has no hard-coded path number. The evening pass's R7–R10 corrections remain appended.
  `VERSION` and `__version__` read `0.18.3`, the release section names FM-029, FM-030, FM-031, FM-033 and FM-034
  with their checks, and the generated page reads `v0.18.3`.
- `git merge-tree --write-tree origin/main HEAD` exited 0, tree
  `4f360831884392694c7c41da395a2a7b1c16bc36`, after main advanced through PR 70 to `c3cd54c`. No
  conflict remains.

## Findings and limits

**No new findings.** The third pass's R1 is closed, and the earlier passes' findings remain closed. The broad
FM-030 accepted-action promise is still open in its tracker, outside 0.18.3's `next:` slice. The brief's literal
FM-007 *not owed a pass* check was written before FM-007 became In Progress: an In Progress tracker is owed the
ordinary pass, while this raise does not reopen it (`raised` is empty). The brief's byte-identity statement is
likewise qualified by the generated date in the release text. I did not inspect the sealed Auditor session.

## Verdict

**READY.** The code tier's full loop has a green branch gate, passing suites, a clean merge with current main,
and a direct reproduction showing the last P2 fixed. PR 65 may proceed to the Owner's merge; v0.18.3 is due
as the Owner's tag on main after that merge.

The Owner lands this by merging and tags v0.18.3; a merge rules nothing (path 5).
