# Review — FM-030's board-reads-git build at ada15c6 (2026-09-28, Reviewer, session `8e509911/reviewer-43`)

- **Branch:** `fm/030-the-board-reads-his-unmerged-acts`, tip `ada15c6` (`ada15c61b02560bc5e8bc80df0a50bbf592f186e`,
  confirmed by `git ls-remote` before and after this pass). Since `origin/main` (`02f3c5c`): item 1 `867f649` (05:27:41),
  item 2 `1205790` (06:10:45), item 3 `a3f2b81` (06:28:31), item 4 `320771a` (06:47:42), item 5 `1433fa9` (07:31:38), and
  two merges of main, `ce119a4` (07:53:34) and `ada15c6` (08:20:17). The merges touch trackers and evidence only:
  `git diff 1433fa9 ada15c6` is empty for `shoalmark.py`, the suites, `vendor/`, the CHANGELOG, the README, `docs/` and
  `examples/`. `origin/main` is the merge base, so `git merge-tree --write-tree origin/main ada15c6` is clean and gives the
  tip's own tree (`5588ed0`).
- **The ruling:** his signed answer `920970b7` (2026-09-27 14:56:15): *accepted - the board reads git: an unmerged
  `origin/answer/*` tip with a `done:` or `answer:` main lacks shows as done, on its way* — option 1 of the ask of
  14:14:18; his words of 13:57:50 and 14:09:46 under FM-030's `## Raised`; the paragraph *The ask of 2026-09-27*.
- **Tier: code — not critical; the queue's output byte-identical.** `git diff origin/main...ada15c6 -- lefthook.yml
  scripts/ .github/` is empty. In `shoalmark.py`, by an AST diff of every function:
  - changed: `answer_cmd` (and its `check_ask`), `owner_change` (and its `undo`), `owner_digest`, `standup`,
    `render_html`, the page's script, `LABELS`, `front_matter_schema` (the text of the `answer:` and `done:` rows — every
    shape and every *required* flag is unchanged), `parse_args`, `main` (the `--revoke` dispatch only);
  - added: `on_their_way`, `way_lines`, `owed_now`, `board_stamp`, `board_after_act`, `revoke_cmd`, `WAY_TITLE`.

  The FM-037 guard (`guard_walk`, `guard_verdicts`, `guard_lines`, `triage_guard`), `judged_before_build`'s gate
  (`build_judgement`, `pending_judgement`, `judge_commits`, `build_problems`), the hook's code (`commit_msg_hook`,
  `commit_msg_check`, `install_hook`), `--check`'s `lint` and `schema_problems`, and `--queue`'s readers
  (`queue_actions` with its `answered_at` and `addenda_only`, `answer_reading`, `triage_reading`, `latest_verdicts`,
  `verdict_reports`, `queue_cmd`, `queue_lines`, `forge_prs`, `pushed_branches`) are byte-identical, and none of them
  reaches a changed or added function in the call graph. `on_their_way` CALLS `answer_reading`; it does not change it.
  **`--queue` run on one scratch repository by main's tool and by the tip's** — a bare `origin`, `gh` stubbed with three
  open pull requests: `answer/ap-001` (his signed answer), `answer/ap-002` (his signed `done:` with a Reviewer's verdict
  commit on top — RV-679's shape), `ap/004-work` (a READY verdict); `ap/005-plain` pushed without one; `answer/ap-003`
  merged; `answer/ap-006` a body edit only — **stdout and stderr byte-identical**: `PR 1  merge: your answer`, `PR 4
  merge … verdict READY`, `PR 2  wait: not an answerer (rev@seat)` (RV-679 itself, FM-031's, untouched), `branch
  ap/005-plain … no verdict`. The guard did not trip; this pass goes on.
- **Independence:** same session — a sub-agent of 8e509911, reported.
- **Verdict: NOT READY.** RV-730 is a P2: `--due` — the *reschedule* button — is the one act command whose result is not
  on his board after the press, and on an act that was done it reads *done revoked, on its way*, which he never did.
  RV-731–RV-734 are P3. Items 1, 2, 4 and 5 do what the brief and his answer ask for `done:` and `answer:`, verified by
  running them; item 3 does for `--answer` and `--done`.

## What I ran

- **Suites** at the tip, one interpreter at a time, each started at a 1-minute load under 6: Python 3.14.3 —
  `test_shoalmark.py` 528 ok, 0 skipped, all green (816 s); `test_core.py` 148 ok, all green. Python 3.9.6 —
  `test_shoalmark.py` 528 ok, 0 skipped, all green (839 s); `test_core.py` 148 ok, all green — started at 09:11, once
  no other suite ran on this machine and the load was under 6. The worktree stayed clean.
- **Gates:** `--check` 0 — *judged before build: on — 5 commit(s) … every build commit under a judged In Progress
  tracker* (FM-030 In Progress, triaged 2026-09-27, P1, rank 2), *the Owner's two sections: guarded — 7 commit(s) …
  none changes them or his signers file*, filing freeze 21; `--session-check` 0; `--queue` on the branch: `branch
  fm/030-the-board-reads-his-unme… @ ada15c6  wait: no pull request — no verdict on ada15c6`; merge-tree clean against
  `origin/main`; `git diff --check` clean.
- **Live, read-only, on this clone:** the tip's `--owner` in this worktree (`gh` stubbed to fail) lists the three answers
  the Owner pushed this morning — FM-024, FM-027, FM-032 — *answered, on its way*, signed, *your merge is next*, and his
  first line reads `NO QUESTION FOR THE OWNER · 2 ACT(S) OWED, WITH THEIR TIME · 3 ON THEIR WAY — YOUR MERGE IS NEXT`.
  RV-679's lesson holds live: `origin/answer/fm-024`'s head is `b60e001`, a Reviewer's pass at 08:27:09, and the reader
  names his `4127dba` (08:11:26, `G`), read *merge: your answer*. The reader alone took about 1 s here.
- **The reader (item 1)**, on the scratch repository above: it lists `AP-001` (*answer*, commit `= tip`, `G`, *merge:
  your answer*) and `AP-002` (*done*; the commit named is his `done:` commit below the Reviewer's head, `G`), and nothing
  for the merged `answer/ap-003`, the body-only `answer/ap-006`, or the plain branches. No fetch, no forge: it reads
  `for-each-ref --no-merged` and `cat-file`. A fresh clone of a walk-through repository's `origin` lists the same rows,
  the same shas (another machine). No pull request is looked up; every row says *your merge is next* — the record says so.
- **The board (item 2):** rendered by both tools on a copy of that repository with the two unmerged answer refs removed
  (the merged and the body-only branch left): the rows (`T=[…]`) are byte-identical, and the DOM headless Chrome builds
  from each page, scripts aside, is byte-identical (13 762 bytes each). The page file itself differs by its script and
  its labels — see RV-733. With the two branches: *waiting for you: 1* (AP-001 gone from it), no *your acts* (AP-002 gone
  from it), *on their way: 2* — his promise or his answer first, *answered, on its way* / *done, on its way — <where>*,
  the branch, the commit, its time, *signed*, *your merge is next*, the question below, and one button, **revoke**,
  where *accept*/*reject* and *done*/*reschedule* were. Looked at in headless Chrome at 1440 and 390 px: at 1440 it
  reads cleanly; at 390 the Owner's box is wider than the viewport and its lines are cut at the right edge — on main's
  page too, the same way (its *waiting* and *acts* lines), so not this build's. `--owner` and `--standup` print the same
  section after the asks and acts. The revoke dialog, driven in Chrome with a *why* carrying `"` and two spaces: the
  second screen gives `--revoke AP-002 'wrong '\''file'\'' here'`, says it commits on `answer/ap-002` where it is on its
  way, and its *when it worked* is what the command prints. The German labels: all 14 new keys in
  `examples/de/labels.yaml`; with it as the repository's brand the dialog, the row and its steps read in German
  (160 of 161 labels changed — `footer`, empty, as on main).
- **The rebuild after the act (item 3):** without a checkout hook, `--answer AP-001 accept` ends on `main` with *the board
  is rebuilt — no checkout hook rebuilt it* and the page shows it on its way; with `--install-hook`'s hooks, `--done
  AP-002 "evidence/AP-002/read.md"` ends with *the board was rebuilt by the checkout hook*; with the board file deleted
  before the act, the command writes it; with the board tracked by git, it leaves it and says why. How it knows: the
  board file's `(st_mtime_ns, st_size)` taken after the push and compared after the switch back. Judged: `put` always
  writes, so a rebuild always moves the stamp; on a filesystem with 1–2 s times and a same-size page, the error is a
  second rebuild, not a stale page. It can say *rebuilt by the hook* over a stale page only where another process that
  read git before the push writes the board between the push and the switch back — a window of a checkout; not a finding.
- **`--revoke` (item 4):** on the act done on its way (from `main`): switched to `answer/ap-002`, committed `95da60e`
  (`G`) on top of his `done:` commit, pushed, back on `main`, the hook's rebuild; at the tip `done:` is gone, `next:
  owner`, and `## Acts` carries `**2026-09-28** · done revoked — wrong file · it was done 2026-09-28T08:36:52+02:00 ·
  evidence/AP-002/read.md · yes, at seven · Owner`; the act is back under *your acts* and nothing is on its way for it.
  On an answer merged into `main`: `answer/ap-001` cut fresh, `revoked - changed my mind` on its way (*revoked, on its
  way*). A seat (`impl@seat`) is refused before anything is cut, exit 4. On an answer, `--revoke` is `--answer <id>
  revoke` (FM-031's rules), with `onto` only where `answer/<id>` is not merged; without it `answer_cmd` and
  `owner_change` run main's paths unchanged (`cut_at` is `start`), and `--answer <id> revoke` itself still refuses on an
  unmerged branch — the two paths do not overlap. No remote branch is deleted and nothing unmerged is (a merged local
  `answer/<id>` is cut fresh, as main does); every revocation is a new signed commit, never an overwrite.
- **The record (item 5):** CHANGELOG `## Unreleased — 0.18.6` — three bullets naming FM-030, `920970b7`, his words of
  13:57:50 and 14:09:46, RV-679, and `done:`'s recorded time under `--schema`; README's new row; `--schema`'s `answer:`
  and `done:` rows; FM-030's *What is true now* paragraph with RV-680's line; the ship-log row naming `867f649`,
  `1205790`, `a3f2b81`, `320771a` and the record's own commit. `docs/standup.md` and `docs/de/standup.md` are not
  touched — RV-733.

## Findings

**RV-730 · P2 · confidence high on the mechanism (reproduced; his own `--due` of 08:25:42 is the case); high on the tier
for (2), medium-high for (1) and (3) — the *reschedule* button's result is not on his board after the press, and on an
act that was done it reads *done revoked*.** `on_their_way` reads `done:` and `answer:` only. Reproduced:

1. An act owed (`AP-002`, due 07:00, *missed*): `--due AP-002 2026-09-29T09:00:00+02:00` commits `6553127` (`G`) on
   `answer/ap-002`, pushes, ends on `main` and prints *the board is rebuilt — … it reads the branch just pushed*. The
   board, `--owner` and `--standup` still show `AP-002 — yes, at seven · missed — due 2026-09-28 07:00` with *done* and
   *reschedule*; nothing is on its way. Pressing either again gives a command that is refused from `main` (RV-731).
2. An act that was done and merged: `--due AP-002 2026-09-30T09:00:00+02:00` — *on an act that was done, a new act* —
   removes `done:` on the branch, and the reader, seeing `done:` on `main` and none at the tip, names it kind `undone`:
   `AP-002 — yes, at seven · done revoked, on its way`. He revoked nothing. This is his own act of this morning: on
   PortDive, `5f307d34` (08:25:42, `G`, read-only from its objects) — `--due BUG-327 2026-09-28T11:00:00+02:00`, sitting
   two — drops `done: "2026-09-27T20:21:07+02:00 · …"` and writes the new `due:`; until its merge this tool would have
   shown it on his board as *done revoked*. And the Auditor's raise of 08:21:57 (on
   `fm/030-a-done-act-has-no-button-for-the-next-raised` @ `d0ae8ab`, not merged) makes exactly this `--due` the next
   slice's button.
3. The same gap, not a label: an accepted action answer whose promise names its hour seeds `due:` at the tip (`AP-003`,
   *yes, Monday 2026-09-28 10:00*); the row reads *answered, on its way* with no time, and the act is on no list, in no
   `--notify`, until his merge.

Why a P2: his words of 13:57:50 are about the button — *they pushed the button, did the answer and expect the page to
display that state right away*, the raise line's *the button's result is not on his board after the press*; the act row
has two buttons and this build answers one. The brief's item 3 names `--due` beside `--done` and `--answer`. And (2) is
worse than absent: the board states an act of his that did not happen, on the page he trusts for his own record — for
an act he made this morning, which the next slice puts behind a button. The build follows the ruling's letter (`done:`
or `answer:`) faithfully; the finding is against that scope, as the dialog pass's R1 was against its spec — and (2) is
not in the letter at all: `undone` is the build's own inference.

**Fix:**

1. `undone` only where the branch's OWN commit that removed `done:` is a revocation — its `## Acts` line at the tip
   (`· done revoked —`) or its subject from `--revoke`; a `done:` moved into the record by `--due` is not read as one.
2. A `due:` the default branch lacks, written by the branch's own commit, reads *rescheduled, on its way — due <time>*
   (a `way.due` label, German beside it), with the act's line first, and the act leaves *your acts* until the merge — as
   `done:` does; a `due:` a promise seeded shows its time on the *answered, on its way* row. If the Principal holds `due:`
   outside the letter of `920970b7`, then at least: (1), the command's last line after `--due` says the board shows the
   new time after his merge, the CHANGELOG and README say so, and the question goes to him.
3. Tests: `--due` on an owed act and on a done act, each read right on the board, in `--owner` and `--standup`.

**RV-731 · P3 · confidence high (reproduced) — an act owed again after `--revoke` (or after `--due`) carries *done* and
*reschedule*, and both commands are refused from the branch the dialog says to run them on.** After the revoke above,
`--done AP-002 "evidence/AP-002/read.md"` from `main` exits 4: *`answer/ap-002` exists and is not merged … `git switch
answer/ap-002`, then …*. Nothing is lost and the refusal names the way through, and the mechanism is main's (the E0
counter's row 20: the next run names the branch); but the build's own revoke flow now leads him there by the board's
buttons. **Fix:** `--done` and `--due` take the `onto` path `--revoke` has — on an unmerged `answer/<id>`, commit on top
of it (one branch per exchange) — or the act's dialog names that branch as where to run it. One change serves RV-730's
second press too.

**RV-732 · P3 · confidence high on the mechanism (reproduced), low on how often — a new question on `main` while his older
answer is on its way leaves his queue.** `AP-001` answered on `answer/ap-001`; a seat then rewrote the ask on `main`
(*Which ships first, now that the site slipped: the launcher or the CLI?*, proposal *the CLI*). The reader counts the
tip's answer as answering whatever `main` asks now: the new question is in no queue, `--owner` says *NO QUESTION FOR THE
OWNER*, and the row shows his old answer under the old question. The spec keeps a stale unmerged answer shown with its
date, which it is; the question it hides is the finding. **Fix:** `answered` only where the tip's `ask:` is the ask the
default branch carries; else the ask stays in his queue and the row says it answers an earlier question.

**RV-733 · P3 · confidence high — the record.** (a) `docs/standup.md` and `docs/de/standup.md` still say each act carries
two buttons and say nothing of *on their way* or *revoke* — the Owner-facing guide, which the brief names; one paragraph
in each. (b) The CHANGELOG's and the README's *a board with nothing on its way is the board it was, byte for byte* hold for
the rows and the rendered page, not for the file: the page carries the new script and labels — say *the rows and the
rendered board*. (c) The ship-log row names every build commit; the two merges of main after it, `ce119a4` and
`ada15c6`, carry no tool change and are not named — fine as it stands, noted.

**RV-734 · P3 · confidence high — words.** `--revoke` on an answer goes through `answer_cmd`, so steps 2–4 print
*answering AP-001 — …* under step 1's *revoking*, and a seat's refusal opens `--answer:`; a revoked answer on its way
reads *revoked - changed my mind · revoked, on its way*, the word twice. **Fix:** pass the verb and the flag through
`answer_cmd` for `--revoke`; for kind `revoked`, show the reason after the label, not the raw answer before it.

## Not proven here

- A pull request is not looked up; every row says *your merge is next*, as the record says.
- PortDive: the tip's tool was not run there — this seat does not run in the Owner's checkout; its `answer/bug-327`
  (`5f307d34`) was read with `git log`/`git show` only, and merged into its `main` before this pass ended.
- The notices on Linux and Windows; the 390 px overflow of the Owner's box, main's as much as this build's.

## Verdict

**NOT READY.** RV-730 is a P2: read `due:` on its way — at least never read a `--due` as *done revoked* — and say what
the board shows after a reschedule. RV-731–RV-734 are P3, fixed with it or forward. The ruling held for `done:` and
`answer:`: the board reads git, one truth, no second store, the queue untouched, and a Reviewer's verdict on top of his
act is no act.

The Owner lands this by merging; a merge rules nothing.
