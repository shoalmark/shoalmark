# Review — 0.17.6, a seat's commit names its session, and the record knows the session

- **Date:** 2026-09-23, 17:17 CEST (`date`)
- **Seat:** Reviewer (`reviewer@seat`) · **Session:** `8e509911/reviewer-1` · **Model:** Claude Opus 5.5
- **Tip reviewed:** `0743a45` on `fix/0.17.6-a-seats-commit-names-its-session-and-the-record-knows-the-session`
- **Base:** `59eebeb` (`origin/main`, v0.17.5)
- **Commits:**
  - `fe4d9eb`, `bc18c37`, `5a4ad6e` — the Principal seat: the FM-024 filing.
  - `2557df0` — the merge of `origin/main`.
  - `89e0586` … `0743a45` — the Implementer seat: S1–S7 and the release.
- **Read:** FM-024 §Slice 1 (S1–S8), §Examples a–f, the decisions taken in the build, README §6 *Sessions*, and the
  `CHANGELOG.md` `## 0.17.6` section.

## Cold start

1. **What virtue do I bring?** Doubt. Every rule of slice 1 has to be re-derived and attacked first-hand, the
   decisions recorded "for the Reviewer" included, before a tag carries them.
2. **How does it turn into blindness?** Here, by grading a recorded design decision as a defect because it can be
   broken. Adoption by existence, or the gate running only on some commits, were chosen with reasons.
3. **What would show that failure here?** Each finding is paired with a planted fixture and a measured outcome, and
   with the decision's own stated reason. The positive controls are the Implementer's claims I could reproduce: 11
   checks (10 fail, 1 control), the three refusals, and the rehearsal. If those had failed, my harness would have been
   wrong.
4. **Who gets the record, independently of me?** The Principal seat, which grades and disposes, and the Owner, who
   merges and tags. This file disposes of nothing.

**The seat's own session.** The harness gives this sub-agent only its parent's id: `CLAUDE_CODE_SESSION_ID=8e509911…`,
with `CLAUDE_CODE_CHILD_SESSION=1`, the same pair the Implementer reports. So this worktree's `seat.session` is S3's
sub-agent form, `8e509911/reviewer-1`: the parent's first eight hex characters and the hand. Its row was opened with
`--session open 8e509911/reviewer-1 reviewer "the Principal session a9" "attack 0.17.6" shoalmark-research`.

**The hook.** This worktree's `core.hooksPath` is set at worktree level to a private directory under its own git
admin directory, as the Implementer did, and `lefthook install` synced three hooks there: `post-merge`, `pre-commit`
and `prepare-commit-msg`. The repository's shared `.git/hooks` are unchanged (dated 2026-09-22). lefthook rewrote the
timestamp in `.git/info/lefthook.checksum`.

## Method

- **Tools:** the tip and 0.17.5, each archived into a scratch directory.
- **Fixtures:** four scratch repositories, each vendoring the tip into `tools/shoalmark` with `[seats]`
  (owner · principal · implementer · reviewer) and the plain hooks from `--install-hook`:
  - `fx1`: the refusals, sub-agent ids, close, a merge of a pre-registry commit, and deleting the registry;
  - `fx2`: the reviewed range on a branch that merged main in;
  - `fx3`: abandoned rows, the verdict report, the board's strip, the digest and the triage close, in English and
    with the German labels;
  - a scratch clone of this repository: the Owner's no-ff merge rehearsal, and a simulated verdict of this seat.
- **The consumer's board:** rendered in memory with both versions, read-only; the consumer tree showed 0 changes
  afterwards.

## Findings

### R1 · P2 · Deleting `sessions.md` switches the gate off, silently, for that commit and every later one

- **What:** `session_problems()` (`shoalmark.py:2569`) judges each change against the registry in its **own** tree.
  For a commit being made that is the working tree; for a made commit it is `git show <commit>:sessions.md`. With no
  registry, `text is None` and the change is not judged (`:2581–2583`). So the commit that deletes the registry is
  judged against no registry, and so is every later one.
- **Measured** (`fx1`, registry adopted, rows open):

  | step | outcome |
  |---|---|
  | `principal@seat`, **no `seat.session`**, commits `git rm sessions.md` with a tracker change | committed; no refusal; no trailer |
  | `implementer@seat`, no session, commits a tracker change next | committed |
  | `--check` | exit 0, and not a word about the missing registry |

  A merge that brings these commits judges each against its own tree, where there is no registry, so they pass there
  too.
- **Same class:** in `fx3` a seat reopened a closed row by editing *Ended* back to `—` in the commit that uses it, and
  `--check` passed (exit 0). Before the edit, `--check` exited 4: *Session: Z has no open row*. No right covers
  `sessions.md`, so the committing seat writes the registry it is judged against.
- **Cost:** The rule is only as durable as one file that any seat can remove. An agent refused by the gate is shown
  the shortest way past it: the refusal names `sessions.md`. Removing it silences every later judgement, including
  the independence report. This is inside the tool's stated bound (*catches an agent that does not know the rule, not
  one that lies*), but the removal leaves no message anywhere.
- **The decision's reason still holds:** it keeps an un-adopted consumer, and every pre-0.17.6 commit, unjudged.
  Nothing below breaks that.
- **Confidence:** High.
- **Falsifier:** A seat commit that deletes the registry and is refused, or reported, by the pre-commit hook or
  `--check`.
- **What closes it:** One of these. The choice is the Principal's.
  - **(a), what I'd recommend:** a tree whose commit **removes** the registry is judged against its parent's registry,
    and a seat's commit that removes it is refused (*the registry is the Owner's to remove*), with the Owner exempt.
    Adoption by existence stays for trees that never had one.
  - **(b):** a config switch, `[seats] sessions = required`. It is heavier, and it is one more key a seat can edit.

  Either way, add a check that deletes the registry as a seat.

### R2 · P2 · The reviewed range is wrong both ways: it takes in the trunk a branch merged, and it is empty for a tip on the trunk

- **What:** `verdict_reports()` (`:2644`) starts the range at the first commit of the tip's first-parent chain that
  lies on the trunk's first-parent line (`:2663`). It then takes `git log base..tip`, which is everything reachable,
  merged-in trunk commits included.
- **(a) A branch that merged main in.** This branch is that case (`2557df0`). Its range, `73f8ca1..0743a45`, is
  **36 commits: 11 are its own, and 25 are the 0.17.5 release** the merge brought in. That release includes this
  seat's three 0.17.5 review commits and the Owner's merge #16. Their sessions would count as authors of 0.17.6. Today
  they carry no `Session:`, so the effect is nil; from 0.17.6 on, every trunk commit carries one.
- **Planted in `fx2`:**
  1. Release N's docket is committed by session `P` on its own branch, and the Owner merges it into main.
  2. Branch N+1 is forked before that merge and built by session `I` alone.
  3. N+1 merges main in. Its own sessions (`tip ^main`) are `['I']`.

  | verdict's session | reported | the truth |
  |---|---|---|
  | `P/reviewer-1` | **same session**, range `I, P` | independent (`P` authored nothing on N+1) |
  | `K` | independent | independent |
  | `I/reviewer-1` | same session | same session |

  The report is identical after N+1 merges into main.
- **(b) A reviewed tip on the trunk's first-parent line**, for example work committed on main. Then `base == tip`,
  the range is empty, and the word is *untraced* although the tip carries a session (`fx3`: *verdict 2fc677328a on
  1d2292d114: untraced — its session K; the range's (none)*).
- **Where:** `shoalmark.py:2635–2675`; README §6 *Verdicts*; FM-024 *Decided in the build*, "The reviewed range".
- **Cost:** A misleading count. It is the count slice 1 exists to produce ("one week of counts" before any refusal;
  FM-024 *What would decide it*: "whether the independence count changes a verdict on 09-29"). (a) overstates *same
  session*; (b) hides verdicts in *untraced*.
- **Confidence:** High on the mechanism, from two fixtures. It has no effect on today's branch.
- **Falsifier:** `fx2`'s `P/reviewer-1` verdict reported *independent*, and `fx3`'s reported *independent*.
- **What closes it:** Define the range as the commits reachable from the tip and not from the trunk *as it stood
  before the tip entered it*:
  - an unmerged tip: `tip --not origin/main`;
  - a merged tip: `tip --not M^1`, where `M` is the trunk's first-parent commit that brought it;
  - a tip on the trunk: `tip^..tip`, or `tip --not tip^1`.

  Add a check for each of the three shapes.

### R3 · P2 · The release's own first proof reads a sibling sub-agent's verdict as *independent*

- **What:** FM-024 records that the Implementer's id is `8d6537be` from `--session new`, "not `a9/implementer-1`",
  on the coordinator's instruction. It does not record what that does to the measurement. The Implementer and this
  Reviewer are sub-agents of the one harness session: both report `CLAUDE_CODE_SESSION_ID=8e509911…` with
  `CLAUDE_CODE_CHILD_SESSION=1`, and both rows are *convened by the Principal session a9*. Registered as S3 says
  (`8e509911/reviewer-1`), this verdict's report is **independent**.
- **Measured:** In the scratch clone, the verdict commit, with `Reviewed: 0743a45` and `Session: 8e509911/reviewer-1`,
  reads *verdict 0e615968e4 on 0743a45: independent — its session 8e509911/reviewer-1; the range's 8d6537be*. Had the
  Implementer's id been `8e509911/implementer-1`, the same line would read *same session*, which is the finding FM-024
  was filed to measure ("a Reviewer sub-agent of the Principal's session … is counted as not independent").
  `--session new` and a bare `8e509911` also give *independent*, so no choice of mine repairs it.
- **Defect or acceptable?** A defect in effect, with an honest origin. FM-024 names the choice and its reason, but
  not its consequence: the release's first data point for the 09-29 count is a false *independent*.
- **Where:** `work-tracker/sessions.md` row `8d6537be`; FM-024 `:33–35`; the trailers of seven commits
  (`89e0586` … `0743a45`), which cannot be renamed.
- **Cost:** A misleading count at n = 1. From this release on, every sub-agent that uses `--session new` erases its
  parent.
- **Confidence:** High.
- **What closes it:** Choosing is the Principal's call.
  - FM-024 states that 0.17.6's own verdict is not a measurement of independence, and says why.
  - S1's instruction reads *a sub-agent derives its id from its parent's (`<parent>/<seat>-<n>`); `--session new` is
    for a session with no parent*.
  - Optionally, slice 2: when a harness says it is a child, the hook refuses a `seat.session` whose root is not the
    parent's id prefix.

### R4 · P3 · A seat's commit that touches no tracker is refused by no automatic run in shoalmark's own setup

- **What:** The plain pre-commit hook runs the gate only when a tracker, the configuration or the tool is staged
  (`shoalmark.py:3301`). shoalmark's own lefthook `tracker-index` runs only for `work-tracker/*.md`. After that, a
  commit is judged only by `--check` while it is HEAD, or when a merge commit brings it.
  - shoalmark's CI runs the suites and no `--check`.
  - The post-merge hook runs `--html-only`.
  - A fast-forward or rebase merge brings nothing.
- **Measured** (`fx3`):

  | step | outcome |
  |---|---|
  | `implementer@seat`, no session, commits `app.py` | committed (`8778abd`) |
  | `--check` at it | exit 4 |
  | one tracker commit later, with a session | `--check` exit 0; `8778abd` is no longer judged |

- **Where:** `shoalmark.py:3301`; `lefthook.yml`; FM-024 *Decided in the build*, "Where the gate runs"; README §6.
- **Cost:** The refusal described as the gate's reaches code-only commits only by chance: a manual `--check`, or a
  merge commit that someone runs `--check` on.
- **Confidence:** High.
- **What closes it:** Either run the session rule on every commit from the pre-commit hook (one `git config` read and
  one parse of the registry), or run `--check` in CI on the ready pull request. Or say in the README that a code-only
  commit is refused only when someone runs `--check`.

### R5 · P3 · FM-024's worked examples carry a client's and a consumer's state

- **What:** Example c's row `b0` (`FM-024…md:144`) names a **client repository** as its worktree. Example d
  (`:160–168`) and example c's row `a9/reviewer-1` (`:142`) carry a consumer's tracker ids, its review-id range and
  two of its commit hashes. The Owner's rule, stated in the 0.17.5 pass, is that consumer state does not enter
  shoalmark; numbers may.
- **Where it sits:** The work tracker is not vendored (`TOOL_FILES`), so this stays in shoalmark's repository. The
  text came with the Principal's filing (`fe4d9eb`, `bc18c37`). The Implementer's diff adds none. `git diff
  origin/main` shows no consumer id in any shipped file.
- **What closes it:** Placeholders, as this seat's 0.17.5 file was redacted: *a client repository*, *a consumer's
  ids*, *a tip*.

## What survives the pass

- **S1:** `seat.session` per worktree, and `--session new` prints eight hex characters no row carries. The S1 check
  fails on 0.17.5.
- **S2:** `--install-hook` writes `prepare-commit-msg` beside `pre-commit`.
  - In `fx1` a `principal@seat` commit with `seat.session P1` carried `Session: P1`, untyped.
  - The Owner's checkout, with no `seat.session`, got nothing appended.
  - A message already carrying the trailer is left alone (the S2 check).
  - A foreign hook is left alone, and the tool prints the one line to add.
  - lefthook consumers: README §6 carries the `prepare-commit-msg` block, and the CHANGELOG says to run
    `--install-hook` again.
- **S3:** `--session open` writes and stages the row.
  - `P1/reviewer-1` for seat reviewer: accepted (exit 0).
  - `P1/implementer-1` for seat reviewer: exit 4, *names the hand `implementer-1`, not the seat `reviewer`*.
  - A reused id: exit 4, *an id is used once*.
  - A held worktree: exit 4, *wt-principal is open under session P1 — one worktree per session*.
  - `--session close`: exit 0; closing again: exit 4, *closed already*.
- **S4, the three refusals**, each exit 4 through `--check` on a pending seat change, and git rc 1 through the hook,
  with example e's words:
  - *carries no Session: trailer*;
  - *Session: q7 has no open row*;
  - *wt-principal is open under session P1 — one worktree per session*, for a hand-written second row.

  Also measured:
  - A fourth refusal, *open for the seat principal, and … is the seat implementer*.
  - A commit carrying a closed session is refused.
  - The Owner is exempt.
  - A merge bringing a seat commit from before the registry passes `--check` (exit 0), not judged.
- **S5:** a row two days idle is listed by `--check` as *abandoned; the next triage pass closes it*, not refused.
  `--triage` closed it as *closed by the pass of 2026-09-23 — no commit since …* and printed the line for the pass's
  paragraph. Afterwards `--check` lists nothing.
- **S6:** `--check` prints *reviews this week · n verdict(s) · independent · same session · untraced* and one line per
  verdict. The mechanics are right where the range is right (see R2 and R3).
- **S7:**
  - English board strip: *sessions · 3 open — I implementer (build it) · K reviewer (attack it) · Z principal (gone
    quiet) · abandoned* and *reviews this week · independent 0 · same session 0 · untraced 1*.
  - German board strip: *Sitzungen · 3 offen — … · verwaist*, *Prüfungen dieser Woche · unabhängig 0 · gleiche Sitzung 0
    · ohne Spur 1*.
  - `--owner` ends *SESSIONS OPEN · implementer 1 (I) · reviewer 1 (K) · principal 1 (Z)*.
  - German key parity (C4) is green.
- **S8, the checks:**

  | test file | ok at the tip | ok on 0.17.5 |
  |---|---|---|
  | `test_shoalmark.py` | 254 | 244 (+10) |
  | `test_core.py` | 148 | 147 (+1) |

  Against the 0.17.5 tool, **10 of the 11 new checks fail, and 1 passes: the S4 control**, as FM-024 claims. The
  existing C4 also fails there, because the German fixture gained the four keys.
- **The consumer:** rendered with 0.17.6 in memory, its board has `REG=null` and its rows are byte-identical to
  0.17.5's. It has no `sessions.md`, so nothing is judged.
- **The Owner's no-ff merge, repeated in a scratch clone:**
  - Setup: `trunk` = `59eebeb`, merged with the release branch `0743a45` under the Owner's forge (noreply) identity, giving `d166bac`.
  - With `gpg.ssh.allowedSignersFile` set: `--check` exit 0.
  - Without it: exit 4, on FM-007's signed answer (an older answer, not 0.17.6).
  - The brought 0.17.6 commits pass: S3 onward against their own open row; `89e0586` and the Principal's filing have
    no registry in their tree.
- **Docs:** `--help` documents `--session` and `--session-trailer`. README §5 and §6 and the CHANGELOG say what
  exists, and the CHANGELOG states the adoption rule and the code-only limit plainly. `--schema` is front-matter keys
  only; the trailers are not keys, which is correct.
- **Consumer ids:** none in the Implementer's diff (R5 is the filing's).

## Gates on 0743a45

| Gate | Result |
|---|---|
| `python3 test_shoalmark.py` (3.14.3) | exit=0 · 254 ok |
| `python3 test_core.py` (3.14.3) | exit=0 · 148 ok |
| `/usr/bin/python3 test_shoalmark.py` (3.9.6) | exit=0 · 254 ok |
| `/usr/bin/python3 test_core.py` (3.9.6) | exit=0 · 148 ok |
| Chrome | ran; no skip line |
| `python3 shoalmark.py --check` | exit=0 — 23 trackers |
| `python3 shoalmark.py --html-only` | exit=0 |
| `python3 -m py_compile` (the three `.py` files) | exit=0 each |
| the tip's tests against the 0.17.5 tool | `test_shoalmark.py` exit=1 (9 FM-024 + C4) · `test_core.py` exit=1 (S7) |
| `--vendor` onto a scratch 0.17.5 consumer | exit=0 · `(was 0.17.5)` · only `## 0.17.6 — 2026-09-23` · PIN `OK` × 8 · `shoalmark.py` byte-identical |

- **Not run:** CI on Linux and Windows.
- **Not seen by this file:** this commit's own trailer, which is reported with the commit.

## Verdict

**NOT READY: R1, R2 and R3 (P2).** R4 and R5 are P3.

- **Slice 1's mechanics hold:** the trailer, the registry, the refusals, the abandoned rows, the strip and the digest.
- **R2** makes the independence count, the one number slice 1 exists to produce, wrong by construction on any branch
  that merges main in, and blind for a tip on the trunk.
- **R1** lets any seat switch the gate off in one commit without a word.
- **R3** puts a false *independent* into the release's own first data point.
- **R1 and R2** each close with a few lines and a check. **R3** closes with a sentence in FM-024 and a rule for
  sub-agent ids.

## Verification addendum

- **Date:** 2026-09-23, 18:12 CEST (`date`)
- **Seat:** Reviewer (`reviewer@seat`) · **Session:** `8e509911/reviewer-1`, the same row, still open · **Model:**
  Claude Opus 5.5
- **Tip verified:** `acec312` — five commits after `0dbdb3c`: `3392b0a` (R3), `af186f0` (R1), `e264d97` (R2),
  `e25279b` (R4), `acec312` (R5). All carry `Session: 8e509911/implementer-1`.
- **Accepted by the Principal:** all five findings, plus one extension. A landed tip is measured against the trunk
  before its merge (`^M^1`), and a tip on the trunk's line reads *on trunk*.

### Each closure on the tip

**R1 · closed.** The parent-registry rule, in a fresh fixture (`fxr1`) with the plain hooks:

| # | the case | outcome |
|---|---|---|
| 1 | a seat with no session removes `sessions.md` | refused, *removes docs/work-tracker/sessions.md — the registry is the Owner's to remove* (also *carries no Session:*) |
| 2 | a seat with an open session removes it | refused, the same line |
| 3 | a seat re-opens an ended row and commits as it | refused, *re-opens Z, which had ended … an ended session stays ended*, and *Z has no open row* |
| 4 | the builder's case: a dropped row | refused, *drops the row I1* |
| 5 | the builder's case: removal forced past the hook (`--no-verify`) | `--check` at that HEAD exits 4 with the removal line |
| 6 | the builder's case: a session closing its own row in its last commit | accepted; its next commit is refused, *I1 has no open row* |
| 7 | the Owner removes the registry | accepted, and seat commits are not judged after that, as ruled |

- **Limit of case 5, not a finding:** one commit later `--check` exits 0 again. But a merge that brings the forced
  removal is refused: *in `0147ad268b` … which the merge brings — refused: … removes docs/work-tracker/sessions.md*,
  exit 4. `--no-verify` is outside the tool's bound, and the merge catches it.

**R2 · closed, with the extension.**
- My planted sibling (`fx2`) now reads *independent — its session P/reviewer-1; the branch's I* **before and after**
  the branch lands. `I/reviewer-1` still reads *same session*, and `K` *independent*.
- A tip on the trunk (`fx3`) reads *on trunk — not a branch verdict*. The board prints *on trunk 1*, and *auf dem Stamm
  1* with the German labels.
- `reviewed_range()` (`shoalmark.py:2679`) on this repository's real history:

  | reviewed tip | range | commits | authors |
  |---|---|---|---|
  | the landed 0.17.5 tip `0ee3bfc` (#16) | `0ee3bfc ^73f8ca1` (= `59eebeb^1`) | 23 | 19 implementer, 3 reviewer, 1 principal |
  | this branch's tip | `acec312 ^59eebeb` | 16 | its own commits |
  | the #16 merge `59eebeb` | — | — | *on trunk* |

  For `0ee3bfc`, the Owner's #13 commits that the 0.17.5 branch merged in are excluded. For this branch's tip, the 25
  commits of 0.17.5 it merged in are excluded.
- The real report on this branch reads *verdict 0dbdb3c396 on 0743a45: independent — its session 8e509911/reviewer-1;
  the branch's 8d6537be*. FM-024 now says that is no measurement (see R3).

**R3 · closed.**
- Row `8d6537be` is ended with the note *re-opened as 8e509911/implementer-1: the parent's id was known*.
- `8e509911/implementer-1` is open, *convened by session 8e509911*.
- `--session open` refuses `X9` convened by *session 8e509911* (exit 4, *a sub-agent's id derives from its parent's:
  `8e509911/reviewer-<n>`*) and accepts `8e509911/reviewer-2`.
- FM-024's S3 row states the cost as measured. *What is true now* says *0.17.6's own first verdict is no measurement of
  independence*, which is present and honest.
- The five fix commits carry `8e509911/implementer-1`. So this verdict's range holds both roots (`8d6537be` and
  `8e509911`), and this seat is its sibling. The report on this commit should therefore read *same session*, the
  truth. The commit's report is given with the commit.

**R4 · closed.**
- The pre-commit hook `--install-hook` writes opens with `{cmd} --session-check || exit $?`, and `lefthook.yml` gains
  `session: run: python3 shoalmark.py --session-check` with no glob, so it runs on every commit.
- In `fxr1`, `implementer@seat` with no session, staging only `app.py`, is refused (*carries no Session: trailer*).
  With row `I2` open it is accepted, and so is a second code-only commit.
- **Timing, on the consumer's 505-tracker checkout, read-only:** `--session-check` takes 0.288–0.310 s per run over
  five CLI runs as the checkout's own author, and 0.288–0.295 s with `GIT_AUTHOR_EMAIL=principal@seat`.
- Instrumented in-process with an audit hook, one run takes 0.111 s to import and 0.114 s to run. It opens **0
  tracker files** and makes **3 git calls** (`rev-parse`, `diff`, `var`). The consumer has no registry, so nothing is
  judged, and its tree showed 0 changes afterwards.

**R5 · closed.** `git diff origin/main` outside `evidence/` names no client repository and no consumer id or hash.
The only hit, the id prefix `msr`/`MSR-00n` in the new tests, is the suite's and README's example key since before
0.17.5 (README has 11 uses on `origin/main`, `test_shoalmark.py` 46), so it is not new consumer state.

### R6 · P3 · The sub-agent rule reads the parent out of free prose

- **What:** `--session open` takes the parent from `\bsession\s+(<id>)` anywhere in *convened by*
  (`shoalmark.py:2525`), so any word after "session" becomes a parent. Measured in `fxr1`, each exit 4:

  | `--session open` | *convened by* | refused, with the parent read as |
  |---|---|---|
  | `Q1 principal` | *the Owner, after the morning session today* | `today` — *derives from its parent's: `today/principal-<n>`* |
  | `Q2 principal` | *the Owner — his session of 09-23* | `of` |
  | `8e509911/reviewer-3 reviewer` | *the Principal session a9* | `a9` |

  The last row is the very words this seat was told to use for its own row. The release's registry names the Principal
  session two ways: *the Principal session a9* (rows `8d6537be` and `8e509911/reviewer-1`) and *session 8e509911*
  (row `8e509911/implementer-1`). This seat's own row would now be refused.
- **Also:** the CHANGELOG does not say that `--session open` refuses such an id.
- **Cost:** A top-level session can be refused by its own description, with a message that invents its parent. The
  registry cannot tell whether *a9* and *8e509911* are one session.
- **What closes it:**
  - Read a parent only where it is an id the registry, or the harness form, can name — for example a registry row's id,
    or eight hex characters — or from an explicit marker such as `session:<id>`.
  - One name for the Principal session in the registry's prose.
  - One CHANGELOG clause on the refusal.

### R7 · P3 · Two texts say what is no longer true

- **FM-024 *What is true now*,** the opening paragraph, still says:
  - *Eleven new checks* — this pass counts 15 FM-024 checks, the four R-checks included;
  - *`Reviewed:` verdicts reported independent · same session · untraced*, without *on trunk*;
  - *every commit of this seat from S1+S2 on carries `Session: 8d6537be`* — the five fix commits carry
    `8e509911/implementer-1`.

  Its *Decided* section below it is correct.
- **README §6** (`:245`) says a lefthook repository *adds one line*, above a block of two entries: `pre-commit
  --session-check` and `prepare-commit-msg --session-trailer {1}`. The CHANGELOG correctly says *both lines*.
- **What closes it:** Rewrite both in place.

### Gates on acec312

| Gate | Result |
|---|---|
| `python3 test_shoalmark.py` (3.14.3) | exit=0 · 258 ok |
| `python3 test_core.py` (3.14.3) | exit=0 · 148 ok |
| `/usr/bin/python3 test_shoalmark.py` (3.9.6) | exit=0 · 258 ok |
| `/usr/bin/python3 test_core.py` (3.9.6) | exit=0 · 148 ok |
| Chrome | ran; no skip line |
| `python3 shoalmark.py --check` | exit=0 |
| `python3 shoalmark.py --html-only` | exit=0 |
| `python3 -m py_compile` (the three `.py` files) | exit=0 each |
| the tip's `test_shoalmark.py` against the `0743a45` tool | exit=1 — S3 (extended), R1 ×2, R4, R2, and C4 (the fifth German label) fail |
| the tip's `test_core.py` against the `0743a45` tool | exit=0 — unchanged at 148 |
| `--vendor` onto a scratch 0.17.5 consumer | exit=0 · `(was 0.17.5)` · only `## 0.17.6 — 2026-09-23` · PIN `OK` × 8 · `shoalmark.py` byte-identical |
| `VERSION` = `__version__` | `0.17.6` |

- The CHANGELOG section is first, and it names `--session-check`, the fifth label and the range rule. The landed-tip
  measurement is stated in README §6, not the CHANGELOG.
- **Not run:** CI on Linux and Windows.

### Verdict on acec312

**READY WITH FINDINGS: R6 and R7 (P3).**

- R1–R5 are closed, and so is the Principal's extension.
- R6 can refuse a top-level session by its wording.
- R7 is two stale texts.
- Neither changes what the gate refuses of a seat commit, or what the report counts.
