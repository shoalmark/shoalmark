# Review — FM-030's done-dialog build at 9c96f5b (2026-09-27 19:36 CEST, Reviewer, session `8e509911/reviewer-40`)

- **Branch:** `fm/030-the-done-dialog-shows-the-question`, tip `9c96f5b` (`9c96f5bda1b64489498b7d5dcef78877fac3001a`,
  confirmed by `git ls-remote` before and after this pass). Since `origin/main` (`67f1bd2`): the raise `5e6d816`, item 1
  `a752c87`, item 2 `5f558f7`, item 3 `2935cf7`, item 4 `a7d0f52`, the merge of main `746fe16`, item 5 `a7f26ae`
  (18:39:21), its ship-log row `536378c`, and the merge of main `9c96f5b` (18:55:01).
- **Tier: code — not critical.** `git diff origin/main...9c96f5b -- lefthook.yml scripts/ .github/` is empty. In
  `shoalmark.py`, by an AST diff of every function and module constant:
  - changed: `act_of`, `acts_lines`, `answer_cmd` (and its `write`), `done_cmd`, `due_cmd`, `front_matter_schema` (the
    text of the `due:` and `done:` rows; no shape), `invite_cmd`, `notify_cmd`, `owner_change` (and its `undo`),
    `render_triage`, `HTML_PAGE`, `LABELS`;
  - added: `answer_due`, `local_time`, `promise_of`, `record_refusal` (inside `owner_change`), `refusal_reason`,
    `result_facts`, `seed_said`, `ANSWER_TIME_RE`, `_WEEKDAY`, `VERDICT_LINE_RE`, `_FILE_SHA_RE`, `_FILE_SESSION_RE`.

  The FM-037 guard (`guard_walk`, `guard_verdicts`, `guard_lines`, `triage_guard`), `judged_before_build`'s gate
  (`build_judgement`, `pending_judgement`, `judge_commits`, `build_problems`), `--check`'s `lint` and its readers,
  `--queue`'s readers (`answer_reading`, `triage_reading`, `queue_actions`, `latest_verdicts`, `verdict_reports`) and
  the hook's code (`commit_msg_hook`, `commit_msg_check`, `install_hook`) are unchanged. None of them reaches a changed
  or added function in the call graph. The one path from them is `run_deriver` → `front_matter_schema`, which carries
  row text only.
- **Independence:** same session — a sub-agent of 8e509911, reported.
- **Verdict: NOT READY.** R1 is a P2: item 5 records a review's first stated verdict, and in 22 of this repository's 76
  review files a later pass in the same file has superseded it. R2–R5 are P3. Items 1–3 do what the brief and his words
  ask, verified by running them.

## What I ran

| run | result |
|---|---|
| a scratch tracker set without acts, rendered by main's tool and by the tip's (`git archive`, no worktree) | `INDEX.md`, `view/` and stdout are byte-identical. `index.html` differs only in the template: the `#p .aq` rule, the row-layout comment, the two act templates, and four labels in `L` (`act.done.hint`, `acts.promised` reworded; `act.done.hint.promise`, `acts.asked` new). Every data row is identical |
| a scratch set with FM-024's shape (`answer: accepted - a cold Reviewer session you start reviews 0.18.3`, `due:` set), a `due:` beside an unanswered ruling, and a bare `accepted` | the page's act rows: `[promise, answer, date, due, 60, question]`. The unanswered one: `[title, "", "", due, 60, ""]`, and its question stays under *waiting for you*. INDEX.md's Act column shows the promise and Promised shows the signed answer |
| headless Chrome on that board (its list, and `OWE(…)` for *done* on AP-024 and AP-026 and *reschedule* on AP-025), DOM dump and screenshot | the list shows *AP-024 a cold Reviewer session you start reviews 0.18.3 · promised 2026-09-24 · due …* with *done* and *reschedule*, then *asked: Who verifies 0.18.3 — …* below, smaller. The *done* dialog leads with the promise in 16 px, then *asked: …* in `.ddim` and the time, and its placeholder reads *the path to the result of this promise, or where it is*. The *reschedule* dialog for the `due:`-only act has no *asked* line. Seen on the screenshot; R4 |
| `--owner`, `--standup` | the same order: `AP-024 — <promise> · due … · promised 2026-09-24`, then `       asked: <question>`; AP-025 keeps its title, and its question is in the rulings section. Main prints the question as the act |
| `--notify`, in process with `post_notice` stubbed, one act due in 10 min | the notice's body is `<promise> · due …\nasked: <question>`. The AppleScript `notify_argv` builds for it compiles with `osacompile`; it was not posted |
| `--invite AP-024` | `SUMMARY:scratch — AP-024: a cold Reviewer session you start reviews 0.18.3`, DESCRIPTION opens with the promise, then `Asked: …`, then *Promised …*, and the alarm names the promise. Main's SUMMARY is the question |
| `examples/de/labels.yaml` | the four changed labels in German: `zugesagt {0}`, `gefragt: {0}`, and both hints |
| scratch repo with an origin, `--answer … accept "<text>"` on action asks | `2026-10-03T09:00+02:00` and `2026-10-03 09:00` → `due: 2026-10-03T09:00:00+02:00`, written in the answer's own commit (`git show`: `answer:`, `answered:`, `answered-by:`, `due:`), and it says *due: … — read from your answer's `…`, written with it*. `Sat 10-03 09:00 CEST` (BUG-327's form) → the same. `Sat 09:00 CEST` (a weekday alone) → no `due:`, and it says *no date read … a weekday alone is not a date … `--due AP-203 <time>` sets it*. A ruling accepted with `2026-10-03 10:00` gets no `due:` and no line. BUG-327's exact text answered today is read as 2027-09-26, a Sunday: not read, and it says why |
| `answer_due("Sat 09-26 09:00 CEST", 2026-09-25)` on this machine's real zone, no stand-in | `2026-09-26T09:00:00+02:00`: E0 row 20's own case is read |
| scratch repo, a pre-commit hook refusing any commit that adds `due:`/`done:`/`answer:` | `--due`, `--done` and `--answer` are each refused after the cut. The undo prints *the commit was refused … What refused it: gate: …*, *restored …*, *back on `main`* and *recorded under `## Acts` on `answer/ap-30x`: `<sha>`, unsigned — pushed*. `origin/answer/ap-30x` carries one line, `**2026-09-27 19:23** · --due AP-301 2026-09-29T10:00:00+02:00 refused — the commit was refused: gate: …`, in a commit `%G?` N. A tree with changes is refused before the cut: printed only, no branch |
| …the next `--due` from `main`; then on `answer/ap-301` | refused on the unmerged path, naming `93ec09e AP-301: --due refused …` and *`git switch answer/ap-301`, then …*. Run there, the act commits on top, and `## Acts` holds the refusal and then the act |
| a `[seats] owner = "h@x signed"` repo, `user.signingkey` pointing at a missing file | `git commit -S` fails after the cut, and the refusal is recorded unsigned: *…refused — the commit was refused: error: Couldn't load public key …*. With the key back, his signed `--due` on top. On that branch `--check` has no rights or guard finding (only the scratch INDEX, which no hook regenerates there), `answer_reading(HEAD)` → *merge: your answer*, `answer_reading(HEAD~1)` → *wait: unsigned answer*, `triage_reading` → None |
| a push remote that fails | not an undo: the change is committed and *NOT pushed*, as on main; no refusal line (none is due) |
| scratch repo, `--done` on 10 acts (R1's scratch) | a review with a stated verdict line, `Reviewed:` and `Session:` → *(verdict READY WITH FINDINGS, reviewed 0123456, session 8e509911/reviewer-40, added in 5e52db4 2026-09-27T19:28:21+02:00)*. A plain committed file → *(added in …)* only. An untracked file → *(not committed)*. `PR65` → *(not in the repository)*, exit 0. *the forge's comment on PR 65*, a link and a folder → nothing beside them. `evidence/AP-502/read.md`, from the tracker directory → *(docs/work-tracker/evidence/AP-502/read.md, added in …)*. A file whose only verdicts are prose (*came back NOT READY at 14:23 …*) and a backticked `` `Verdict: READY` `` → no verdict. A two-pass file → R1 |
| `--due` on the done AP-501, on its branch | *scheduled — due …, a new act — the one before was done 2026-09-27T19:28:29+02:00 · docs/…/review-ap-501.md (verdict READY WITH FINDINGS, reviewed 0123456, …)*, and `done:` leaves the front matter |
| `result_facts` on every `review*.md` at the tip (76) | the draft's `VERDICT_LINE_RE` and the final one give the same first verdict in 76 of 76 (the Implementer's 73 are `evidence/reviews/` at `a7f26ae`). Against the newest commit that touched each file, the **first** stated verdict agrees in 54 of 76 and the **last** in 76 of 76: R1 |
| `changes_since("0.18.4")`, `("0.18.5")` | `## 0.18.5 — 2026-09-27` only, and nothing. `## Unreleased — 0.18.6` is never read. `VERSION` is 0.18.5 |
| both suites, one interpreter at a time, started at a 1-minute load of 1.42 | `test_shoalmark.py` 502 ok / 0 FAIL, *skipped here: 0 checks — every check ran*, and `test_core.py` 148 ok / 0 FAIL, on both 3.14.3 and 3.9.6 (`/usr/bin/python3`). All four exit 0. FM-039's case passed first time on both |
| `python3 shoalmark.py --check` | exit 0. *INDEX.md is up to date — 39 trackers*; *judged before build: on — 7 commit(s) on a detached HEAD since origin/main, every build commit under a judged In Progress tracker* (FM-030: In Progress, `triaged: 2026-09-27`); *the Owner's two sections: guarded — 9 commit(s) … none changes them or his signers file* |
| `--session-check` | exit 0 |
| `--queue` | `branch fm/030-the-done-dialog-shows-th… @ 9c96f5b  wait: no pull request — no verdict on 9c96f5b` |
| `git merge-tree --write-tree origin/main HEAD` | clean (`7413f23`). The merge `9c96f5b` against both parents: main's FM-030 front matter (`answer:`, `next: build`) and the branch's body, both whole |

## The Implementer's report on item 5

- **Suites, `--check`, `--session-check`, merge-tree:** reproduced above.
- **(1) `VERDICT_LINE_RE` skips a verdict's shape quoted in code:** agreed. The first verdict is the same before and
  after in every file (76 of 76), and the suite's AP-485 case covers it.
- **(2) the `--schema` test:** present, and it passes. The `done:` row carries the rule; see R1 for its wording.
- **(3) 13:5x → 13:42:40:** done. No *13:5x* is left, and the docstring, the CHANGELOG and the raise line read 13:42:40.
- **(4) FM-030 C's expected line now carries *(not in the repository)*:** the case still tests what it tested: `done:`'s
  value, `next: build`, `due:`, the record line, the `G` signature, the push, and the run ending back where it began.
  Only the record line's text moved: item 1 made it the promise (*at seven*), and item 5 added *(not in the repository)*
  for a path with no file behind it. The case now pins that path too. Agreed.
- **A review that writes `Reviewed <sha>` without a colon:** one file, `review-0.18.4-fm030-52cfcc7.md`. Its adding
  commit's trailer names `52cfcc7`, the file's first `Reviewed` mention. On its own that is no finding. The file holds
  three passes, though, and its last (`6270118`, READY WITH FINDINGS) is in `510bc94`'s trailer. R1's fix reads that
  trailer.

## Where the brief and the build differ, and the build is right

- **The CHANGELOG has four bullets, not five.** There is one bullet per built item (1, 2, 3 and 5), and each names
  FM-030, his time (13:38:30 or 13:42:40) or E0 row 20. Item 4 is the record itself.
- **BUG-327's text is not a weekday alone.** *Sat 09-26 09:00 CEST* is a weekday with its month and day, and the rule
  reads it. `--schema` states the rule under `due:`: *"`--answer` writes it with an accepted action answer whose
  promise names a date with its hour — `2026-09-26 09:00`, `2026-09-26T09:00+02:00`, or the weekday with its month and
  day, `Sat 09-26 09:00`, the next such day on or after the answer, its weekday checked — in the zone it names (an
  offset, `Z`, `UTC`, `GMT`, or this machine's own name for its zone, `CEST`), else this machine's zone; a weekday
  alone, a month and day with neither year nor weekday, a zone name this machine does not carry, or two times are not
  read, and the act shows *no date yet*. A `due:` already set is left, and `--answer` says so"*. Reading that form is
  what makes E0 row 20's own case work.
- **`## Raised` is in time order where a line has a time.** The lines run 13:38:30, 13:42:40, 13:57:50, 14:09:46. The
  E0 line carries no time and sits after 13:42:40, as the item-5 brief listed them. Both quotes of his are marked
  *(spelling normalised)*.

## Findings

**R1 · P2 · confidence high — `--done` records a review's first stated verdict, which a later pass has superseded in
22 of this repository's 76 review files.**

`result_facts` takes the *first* line that states a verdict. It takes `Reviewed:` and `Session:` from the file's
first such lines, else from the *adding* commit's trailers. In this repository a review is often re-verified in the
same file: a NOT READY pass, then a later pass that ends READY. For those files the record states the superseded
verdict. The findings below were measured at the tip:

- **The count.** In 22 of the 76 `review*.md`, the first stated verdict differs from the verdict of the newest commit
  that touched the file. The last stated verdict agrees with that commit in all 76.
- **`review-tracker-triage-2026-09-24-evening.md`.** It reads *verdict NOT READY, reviewed cb1d05e, session
  8e509911/reviewer-2, added in ea4d98a*. The adding commit `ea4d98a` itself says *…at cb1d05e — READY WITH FINDINGS*.
  The record would pair `cb1d05e` with a verdict that sha never had.
- **`review-0.18.4-fm030-52cfcc7.md`, this tracker's own pass.** It reads *verdict NOT READY, reviewed 52cfcc7*. Its
  last pass (`510bc94` on `6270118`) is READY WITH FINDINGS.
- **Scratch AP-509.** The file holds a first pass whose bold opening line states NOT READY, then a second pass stating
  READY on `89abcde`. `--done` wrote *(verdict NOT READY, reviewed 0123456, session 8e509911/reviewer-40, …)*. The
  sha and the session came from the commit that added this file together with AP-501's review, so they are that
  other review's trailers.
- **The Owner's own example reads right.** `review-fm-029-0-18-3-fourth-pass.md` → *verdict READY, reviewed 8c3c10b,
  session 01a0d6e7, added in e3aa64e*.

Why this is a P2: on his word of 13:42:40 the person gives the path and the record gathers the facts, in his signed
commit, because he will not check them. For roughly three reviews in ten here, the record would tell him the opposite
of the act's result, as *what the repository says of it*. That undermines path 4 (trust comes from evidence), and the
harm comes from the command meant to carry the evidence. The rule came from the spec (*the first stated line*), and the
Implementer followed it faithfully. The finding is against the rule, not against the build's fidelity to it.

**Fix:**

1. Read the **last** line that states a verdict (the last `VERDICT_LINE_RE` match).
2. Take `Reviewed:` and `Session:` from the file's last such lines. Where the file has none, take them from the trailers
   of the **newest** commit that touched the file and carries a `Reviewed:` trailer (`git log --no-renames -- <rel>`),
   not from the adding commit. Keep *added in* as it is.
3. Say *the last* in the docstring, in `--schema`'s `done:` row, in the README's act row and in the CHANGELOG bullet.
4. Tests: a two-pass file (NOT READY, then READY on another sha) records READY and the second sha. A commit that adds
   two review files gives neither the other's trailers. AP-480's prose case stays.

**R2 · P3 · confidence high — `ANSWER_TIME_RE` drops what follows the minute, and reads the rest as 24-hour and in the
machine's zone.**

- `2026-10-03T09:00:00.000Z` becomes `2026-10-03T09:00:00+02:00`. The `.000` stops the zone from being read: two hours
  early here, and late on a machine west of UTC.
- `2026-10-03 9:00 PM` becomes 09:00.
- `sat 10-03 09:00 cest` is read in the machine's zone, because the lower-case name is not read.

`--answer` quotes the words it read (*read from your answer's `2026-10-03 9:00`*), so the drop is visible. The Owner's
promises so far are 24-hour, with an upper-case zone (BUG-327). An upper-case word after the time (*09:00 THEN …*) is
taken as a zone and not read, which is safe.

**Fix:** do not read a time that is followed by `[.,]\d`, by `\s*[AaPp]\.?[Mm]\b`, or by a letter run the zone group
does not take, and say why. Or read fractional seconds before the zone. Add a test for each.

**R3 · P3 · confidence medium — a real file given with a line or anchor suffix is recorded *not in the repository*.**
`docs/work-tracker/evidence/AP-502/read.md#L1` and `…/read.md:1` both get *not in the repository*. A person who pastes
`file.md:123` from a review gets a false fact. **Fix:** strip a trailing `#…` or `:<digits>` before resolving the
path. Or say nothing beside it where the rest of the path resolves.

**R4 · P3 · confidence high — on the board, a long question under a promise wraps back to the left edge.** `.aq` is an
inline span, so `padding-left:2ch` indents only its first line. In the render, the rest of FM-024's question (*a
same-session verdict?*) starts in the ids' column under AP-024, where the next act's id stands. **Fix:** make `#p .aq`
an `inline-block`, keeping its padding, and check the wrap in the rendered block.

**R5 · P3 · confidence high — the record.**

- `a7d0f52` changed `shoalmark.py` (four comments) and a test heading, and no ship-log row names it. The rows name
  `a752c87`, `5f558f7`, `2935cf7` and `a7f26ae`.
- FM-030's *What is true now* still opens with main's **Filed 2026-09-24; nothing is built.**, directly above the new
  *Built for 0.18.6* clause, which contradicts it.

**Fix forward:** name `a7d0f52` in the next row, and reword the lead.

## Not proven here

- The notices on Linux and Windows. On macOS the two-line AppleScript literal compiles; no notice was posted.
- **E0 row 20's own refusal.** What refused it is not traced. If a gate refused on the repository's state, the refusal
  line's own commit meets the same gate, and the run prints *NOT recorded: …* only. So whether that exact run would now
  leave a record is not known.
- **A branch that holds only a refusal.** `--queue` lists no `answer/*` branch without a pull request
  (`pushed_branches`), and the board reads `main`. Such a branch is seen only in the undo's print and on the forge until
  the Owner's next run on that tracker. The board reading git is the next slice, not this one.

## Verdict

**NOT READY.** R1 is a P2: record the last stated verdict, and the `Reviewed:`/`Session:` of that pass. R2–R5 are P3,
to be fixed with R1 or forward. The fix loop comes back to a Reviewer.

The Owner lands this by merging; a merge rules nothing.
