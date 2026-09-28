# Re-check — FM-030's board-reads-git build at 1d9cc0c (2026-09-28, Reviewer, session `8e509911/reviewer-43`)

- **Branch:** `fm/030-the-board-reads-his-unmerged-acts`, tip `1d9cc0c` (`1d9cc0cda41130b87a0d95873d075eb0caa3fdad`,
  09:42:55, implementer-52, pushed 10:04:18; confirmed by `git ls-remote` before and after this pass). It is one commit
  past this seat's verdict `90b8c34` on `ada15c6` (NOT READY: RV-730 a P2, RV-731–RV-734 P3). Scoped re-check: the
  three closures, the tier guard, the gates.
- **Tier: code — not critical; the queue's output byte-identical.** `lefthook.yml`, `scripts/` and `.github/` are
  untouched against `origin/main`. By an AST diff against main's tool, the changed and added functions are the same set
  as at `ada15c6`: `on_their_way`, `way_lines`, `owed_now`, `board_stamp`, `board_after_act` and `revoke_cmd` are new;
  `answer_cmd` now takes `flag`/`verb`, and `REVOKE_DONE_SUBJECT` is new. `queue_actions` (with `answered_at` and
  `addenda_only`), `answer_reading`, `triage_reading`, `latest_verdicts`, `verdict_reports`, `queue_cmd`, `queue_lines`,
  `forge_prs`, `pushed_branches`, the FM-037 guard, `judged_before_build`'s gate, `lint`, `schema_problems` and the hook's
  code are byte-identical, and none reaches a changed or added function. `--queue`, run by main's tool and by
  `1d9cc0c`'s on the first pass's scratch repository, prints the same bytes on stdout and stderr.
- **Independence:** same session — a sub-agent of 8e509911, reported.
- **Verdict: READY WITH FINDINGS.** RV-730, RV-733 and RV-734 are closed, each verified by running it. RV-731 and
  RV-732 are forward, each with its line under FM-030's *What is true now*, as the Principal ruled. RV-736–RV-738 are new
  and P3. **Not landable as it stands:** since `origin/main` moved to `9e9fcb3` (PR 111, 10:05:42, FM-030's raise), the
  branch conflicts with main in FM-030's ship-log table. Both sides append rows at its end, so the fix is to keep both,
  in time order. A merge of main is owed first, and after it a scoped re-check.

## What I ran

- **Suites** at `1d9cc0c`, one interpreter at a time, each started only with no other suite process on the machine and
  the 1-minute load under 6: Python 3.9.6 — `test_core.py` 148 ok, all green; `test_shoalmark.py` **533 ok (528 + the
  five new), 0 skipped, all green** (716 s). Python 3.14.3 — `test_core.py` 148 ok, all green. **`test_shoalmark.py` on
  3.14.3 was not run by this seat.** Its turn came after 10:20, the bound for a new suite run; a 3.9 run of mine, started
  in the wrong order, was stopped and run again. The Implementer's commit went through the pre-commit hook, which runs
  both suites when a `.py` is staged, on `python3` (3.14.3); it printed no counts. The worktree stayed clean.
- **Gates:** `--check` 0 — *judged before build: on — 7 commit(s) … every build commit under a judged In Progress
  tracker*; *the Owner's two sections: guarded — 9 commit(s) … none changes them or his signers file*; freeze 21.
  `--session-check` 0. `git diff --check` clean. `git merge-tree --write-tree`: clean against `eb00e96` (main when this
  pass began); **CONFLICT against `9e9fcb3`** (main at 10:06) in
  `work-tracker/FM-030-an-accepted-action-ask-leaves-the-person-s-list-before-the.md`, lines at the ship log's end.
  `CHANGELOG.md` does not conflict with main. The live `--queue`: `branch fm/030-the-board-reads-his-unme… @ 1d9cc0c
  wait: no pull request — conflict in work-tracker/FM-030-…md`.
- **RV-730, closed — verified in fresh scratch repositories with `1d9cc0c`'s tool** (a bare `origin`, SSH-signed owner
  commits, the first pass's builder):
  - `--due AP-002 2026-09-29T09:00:00+02:00` on an open act (due 07:00, *missed*): `--owner` drops the act from *ACTS*
    and lists `AP-002 — yes, at seven · rescheduled, on its way — due 2026-09-29 09:00:00+02:00 · answer/ap-002 @ … ·
    signed · your merge is next`, with the question below it.
  - `--done`, a merge into main, then `--due AP-002 2026-09-30T09:00:00+02:00`, which drops `done:` on the branch:
    `--owner` and `--standup` both read *rescheduled, on its way — due 2026-09-30 …*, never *done revoked*.
  - `--done`, a merge, then a real `--revoke AP-002 "wrong read"`: the commit's subject is `AP-002: done revoked — wrong
    read`, and the row reads *done revoked, on its way*.
  - An accepted action answer that names its hour (`--answer AP-003 accept "yes, Monday 2026-09-28 10:00"`): *answered,
    on its way — due 2026-09-28 10:00:00+02:00*.
  - With nothing on its way, the board's rows (`T=[…]`) from main's tool and from `1d9cc0c`'s are byte-identical.
  - The German label is `way.due: verschoben, unterwegs`.
  - The five new suite checks are among the suite's (see above).
- **RV-734, closed:** `--revoke AP-001 "changed my mind"` on an answer on its way prints *revoking AP-001 — 1/4 … 4/4*.
  The row reads `AP-001 — Does the launcher ship before the site? · revoked, on its way — changed my mind`, the question
  and then the reason. A seat's refusal now opens with `--revoke:`.
- **RV-733, closed:** `docs/standup.md` gains *On their way — before your merge* and `docs/de/standup.md` gains *Unterwegs —
  vor Ihrem Merge*: the five labels, the one **revoke** button, no button on a reschedule. The CHANGELOG, the README and
  the code comment now say *the rows and the rendered board* (the page's file carries the new script and labels).
- **RV-731, RV-732:** forward, each with its line under *What is true now*, on the Principal's ruling.

## Findings

**RV-736 · P3 · confidence high (reproduced) — after `--revoke` on a merged act done, the command says *it is back on
your list*, and it is not, until the merge.** Main still carries `done:`, so *your acts* leaves the act out and the row
reads *done revoked, on its way*. On an unmerged `done:` the line is true at once. **Fix:** where `--revoke` committed
on a branch cut fresh (the act done on main), say *on its way — back on your list after your merge*.

**RV-737 · P3 · confidence high (reproduced), low on how often — `--revoke` typed on a reschedule on its way revokes his
answer, not the reschedule.** `--due AP-002 …` is on its way, then `--revoke AP-002 "take the new time back"`. The tip
carries no `done:`, so the command goes to the answer: `answer: "revoked - take the new time back"`, with the new
`due:` kept, and the row reads *revoked, on its way*. No button leads there: a reschedule carries none, and both
standup pages say to run `--due` on its branch. But the command's help says *takes back what he last did*, and what he
last did was the reschedule. **Fix:** refuse `--revoke` where the tip's newest change of his is a `due:` — *a new time
is moved by `--due`* — or say what it will take back before it does.

**RV-738 · P3 · confidence high — a word.** `act.sign.step.due` in `examples/de/labels.yaml` reads *das Board zeigt es
verschoben, unterwegs*, while the German table's labels and both German pages say *Tafel*. **Fix:** *die Tafel zeigt
es verschoben, unterwegs*.

## Not proven here

- A pull request is not looked up; every row says *your merge is next*, as the record says.
- The merge of main that the conflict needs, and its re-check.

## Verdict

**READY WITH FINDINGS.** RV-730, RV-733 and RV-734 are closed; RV-731 and RV-732 are forward, as ruled; RV-736–RV-738
are P3, fixed forward. His answer's intent holds: the board reads git, one truth and no second store. His answer, his
act done, his reschedule and his revocation each show *on its way* right after the press. The queue is untouched, and a
Reviewer's verdict on top of his act is no act. Before his merge, a merge of main (the ship-log conflict) and its
scoped re-check.

The Owner lands this by merging; a merge rules nothing.
