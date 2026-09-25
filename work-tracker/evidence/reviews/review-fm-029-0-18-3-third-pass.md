# 0.18.3 — cold Reviewer, third pass on `3b35f0f` (PR 65)

**Verdict: NOT READY. Tier: code, full loop.** Reviewed
`3b35f0f13bc555ed08e6a4e925494c3bd16da50e`. This is the cold Reviewer session `01a0d6e7`, started by the
Owner on his signed answer to FM-024, independent of the building session `8e509911`. `git diff --name-only
origin/main...HEAD` names code, tests, configuration, hooks, documentation and trackers, so the code tier applies.
The first and second verdicts are in `review-fm-029-0-18-3-cold-gate.md` and
`review-fm-029-0-18-3-second-pass.md`. I verified; I did not fix the build.

## What I ran

- `git diff 52eaa47..3b35f0f`, and the fix commits `ee1c5a2`, `f57e4ce`, `8afe81a`, `4de6320` and the merge
  `3b35f0f`. The conflict in `TRIAGE.md` was resolved by retaining both Passes paragraphs; its intent and current
  path were untouched. `git merge-tree --write-tree origin/main HEAD` exited 0 with tree
  `72f26cc2b58aaaa78e88753929b26cd12637c84e`, against main `ea630c1`.
- `python3 test_shoalmark.py`: exit 0, 391 `ok` checks, `all green`.
  `python3 test_core.py`: exit 0, 148 `ok` checks, `all green`.
- `python3 shoalmark.py --check`: exit 0, `work-tracker/INDEX.md is up to date — 34 trackers` and
  `judged before build: on — 19 commit(s) on a detached HEAD since origin/main, every build commit under a judged
  In Progress tracker`. `python3 shoalmark.py --session-check`: exit 0; the worktree remained clean.
- `judge_commits(commit_list(sha+'^..'+sha), '')` refused each historical first build: `89e0586` (FM-024 not
  judged), `3c0754f` (FM-032 not judged and Proposed), `90d3d6f` (FM-031 likewise), `bd7d5ea` (no tracker),
  and `4dfb999` (FM-029 not judged and Proposed). The branch's own history passes.
- In a scratch clone with Lefthook installed, `git commit -m '# FM-023: comment subject probe'` on an FM-029
  branch was refused by `commit-msg`: `FM-023: Parked`; HEAD stayed at `3b35f0f`. This replaces the second
  pass's FM-007 probe, because FM-007 is now In Progress and rightly passes. The Principal's stated ruling in
  this round grades a hook-only bypass that `--check` catches P3; the tested literal-subject bypass is closed.
- `python3 shoalmark.py --html-only` rendered FM-031's two `## Asks` records with two relations: the older one
  `accepted with a change · read from the answer's commit 7c97c5b`, the newer one `accepted the proposal`.
  The second pass's R2 is closed for that real record. R1 below is a separate two-record case.
- A fresh clone without `gpg.ssh.allowedSignersFile`: `--check` exited 4 with one `checkout:` line, no `STALE`,
  and four distinct signed commits named once. With `work-tracker/allowed_signers` configured, `--check` exited 0;
  `python3 shoalmark.py` left the INDEX and worktree byte-identical on this date. The generated-date exception
  across days is stated in the release text and covered by the suite.
- `--schema` still says a yes needing the Owner's hands is an `action`, and the answer's `next:` move by kind.
  The temporary-repository tests cover accept, revoke and supersede, signed-rule raises and the RAISED worksheet,
  a pushed branch without a pull request using a bare remote and stubbed `gh`, and missing answer commits. FM-007's
  same-day raise remains not owed. The 0.18.0 authority clause, the evening pass's appended R7–R10 lines, and
  rule 4's seat judgement with no vendored path number remain in place. `VERSION` is `0.18.3`; the release section
  names FM-029, FM-030, FM-031, FM-033 and FM-034 with their checks.

## Finding

**R1 · P2 · confidence high — two older records with identical answer text are assigned the newer answer's relation
and commit.** I made a temporary Git repository with one tracker and two separate asks. Both were answered
`accepted - yes` and cleared into `## Asks` without relation lines, as before 0.18.1. The first ask proposed
`yes`, so its relation is *accepted the proposal*; the second proposed `no`, so its relation is *accepted with a
change*. Their answer commits were `de439d9` and `0f4b9e5`. After both asks were cleared,
`recover_relations` produced one entry, `{'accepted - yes': ('accepted with a change', '0f4b9e5')}`.
`write_views` printed that same newer relation and
commit under **both** records. The first record therefore misstates the Owner's choice and its source.

`unrelated_answers` deduplicates by normalized answer text, `recover_from_log` keeps commits by that text, and
`write_views` looks up each record using the same text. The answer string cannot identify an exchange when it
was reused. Use each record's question/date or its place in the sequence to select its own answer commit, or
write *relation not computable* where the match is ambiguous; never assign one answer's relation to another.
The new test covers two distinct answer strings and does not exercise this case.

The second pass's R1–R4 are closed in their tested cases: the literal `#` subject is refused for a Parked
tracker, FM-031's actual older record has its relation, current main merges cleanly, and the checkout line
deduplicates commits. No other material discrepancy was found in the release claims checked above. I did not
inspect the sealed Auditor session.

## Verdict

**NOT READY:** R1 is P2. The code tier requires a fix and a new verification of the tip. The suites, branch
gate, clone checks and merge check pass, but the relation claim fails on a valid repeated-answer history.

The Owner lands this by merging and tags v0.18.3; a merge rules nothing (path 5).
