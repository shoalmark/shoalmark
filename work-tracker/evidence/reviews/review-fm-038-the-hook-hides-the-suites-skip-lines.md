# Review — FM-038, the filing: the pre-commit hook hides the suites' skip lines (2026-09-26, Reviewer, session `8e509911/reviewer-28`)

- **Date:** 2026-09-26, from 13:38 CEST.
- **Seat:** Reviewer (Opus 5.5, highest effort), a sub-agent of Principal session `8e509911`.
- **Session:** `8e509911/reviewer-28`.
- **Worktree:** `shoalmark-review-5`, detached at the tip. The replays (`--new`, `--related`, the lefthook probes, a
  merge) ran in a scratch clone in the session's scratchpad. `shoalmark`, `shoalmark-gtm`, every other worktree and
  every folder of session `8b91dba2` stayed outside every command.
- **Tier:** docs, one pass. `git diff --name-only origin/main...HEAD` names the new tracker and `work-tracker/INDEX.md`;
  no `shoalmark.py`, test, configuration, hook, key or signers file. A P3 is fixed forward; a P2 sends it back.
- **Independence:** same session. This is 8e509911's own sub-agent, reviewing its Principal seat's filing
  (`Session: 8e509911`, `Worktree: shoalmark-principal`). Reported as such, not independent.

**Reviewed:** `fm/038-the-hook-hides-the-suites-skip-lines` at `5558b1a3c84c2fed684e855b532eabcb067954cd` — one commit
off `origin/main` `8725440`, by `principal@seat`, unsigned, 13:35:57. No pull request is open.
- `origin/main` moved during the pass, by other sessions' fetches (the shared ref's reflog): `b7d8528` (PR 88, FM-031)
  at 13:39:39, `86b78e3` (PR 89, the same-day triage pass) at 13:52:24. Checks 6, 8 and 15 read `86b78e3`.

## The checks

| # | Check | How | Result |
|---|---|---|---|
| 1 | The branch | `git fetch origin`; `git log origin/main..HEAD`; `git diff --name-only origin/main...HEAD`; the trailers | One commit, `5558b1a`, `principal@seat`, unsigned, `Session: 8e509911`, `Worktree: shoalmark-principal`. Two paths: the FM-038 tracker (+27) and INDEX.md (+2 −1: *37 trackers* → *38*, and FM-038's row). ✓ |
| 2 | Fact (1) against `lefthook.yml` | `origin/main:lefthook.yml:3–5`; where the suites print a skip; the real `run:` line through `sh -c` on two stub suites in the scratch clone | `$py $t >/dev/null \|\| { $py --version; $py $t \| grep -v "^  ok"; exit 1; }`: stdout goes to `/dev/null`, and only while the suite exits 0. Skips print to stdout (`test_shoalmark.py:476`, `:2482`, `:3852`; the summary `:4299`). A stub exiting 0 with a skip line and *NOT a full pass*: nothing printed, exit 0. A stub exiting 1: *Python 3.14.3*, the skip line, *FAILED: 1*, exit 1. True for a commit whose suites pass; *never* is wider (R2). |
| 3 | Fact (1)'s sources | `review-fm-035-ci-green-on-every-platform.md`; `CHANGELOG.md` | R3, P3, at line 227 (round two, on `4e4d63b`), its closure at 241–245. CHANGELOG 0.18.4, lines 133–135: *Open, for the release after (the CI fix's review, R3)* … *on a run that exits 0* … *CI prints the suites whole*. ✓ The citation is ambiguous (R1). |
| 4 | Fact (2) against `lefthook.yml` | `origin/main:lefthook.yml:4`; lefthook 2.1.4 in the scratch clone, `lefthook run pre-commit --command tests`, the `run:` replaced by an `echo` (the real config for the cut's shape) | `glob: "*.py"`. A docs page staged: *tests (skip) no matching staged files*. `VERSION` and `CHANGELOG.md` staged — the cut's shape; `ac9eadb` stages just those two — skipped, with the real config. A `.py` staged: the step ran. `3fe7e3a` (on main) adds the setup pages' clone-tag check to `test_shoalmark.py`. ✓ |
| 5 | Fact (2)'s source | `review-0.18.4-cut-df48d67.md`, read whole | The statement is at lines 59–66 and 91–93, and there it is *not a finding*. Line 3 is the file's `Reviewed:` sha. The content ✓; the citation and the framing, R1 and R5. |
| 6 | The same-day pass and its R4 | `origin/main` at `86b78e3`; the two triage review files | FM-035 `status: Shipped`, R3 carried at lines 16 and 52 ✓ — on main since 13:52:24, not on the branch's base. R4 (`review-triage-2026-09-26-the-brand-raised.md:199–213`, `…-2.md:132–137`) asks for this filing and for FM-035's line to point to it (R6). |
| 7 | `--related`, replayed | the scratch clone at `8725440`, four phrasings; the tip | The hook's words: FM-003 3.2, FM-011 2.4, FM-017 2.0, FM-004 1.9, FM-024 1.7 — the five `--new` printed. The `/dev/null` words: FM-003, FM-009, FM-017, FM-035 1.5, FM-028 1.0. The *.py staged, docs-only* words: FM-017 3.4, FM-003 2.5, **FM-032 2.3**, FM-018, FM-035. *lefthook pre-commit suite*: FM-028 3.5, first. At the tip FM-038 ranks first for the first three (16.9, 12.9, 2.8). |
| 8 | The three considered, and a home | each tracker read; `git grep` of every tracker on `86b78e3` for `/dev/null`, the glob, *docs-only* | FM-035: the source, Shipped on main — no queue (R4's point). FM-028 (Proposed, P2, rank 8): two clocks — the suite's fixture counts by the local date, the board by UTC; its fix is date arithmetic, and the hook is only where it bit. Not the home ✓. FM-017 (Shipped): `--answer`'s writes after a refusal ✓. Also read: FM-024 (In Progress), 68–70, the session rule on every commit, not the suites; FM-003, FM-009, FM-011, Shipped, other subjects. No tracker holds either fact ✓. FM-032 is not considered (R4). |
| 9 | The form | `--new FM "<the filed title>" --tags bug` in the scratch clone at `8725440`, diffed against the filing; the same with `--tags process` | Exit 0, the same file name. The front matter is byte-identical but `considered:`; the four headings and the table as the tool wrote them; the three sections filled; the row's *Filed.* expanded ✓. With `--tags process`: *filing freeze — 21 open … nothing was written*, exit 4. The freeze is `--new`'s (`shoalmark.py:5918`); `--check` only reports it — the tag set to `process` in this worktree, `--check` still exits 0 (restored). |
| 10 | The Done-when, decidable | clause by clause | Four observable clauses: the summary and every named skip printed at commit time; both suites on every commit, or one line saying why not; a suite case that fails on a silent skip under the hook's own invocation; a docs-only commit that shows the suites ran. Each can be run and seen ✓. The *or* cannot serve a docs-only commit (R4); R3's second part is absent (R3). |
| 11 | The Why | read | The filing's: a silent skip is a check that did not run, and a cut with no `.py` passes commit time without the suites. No mechanism prescribed ✓. |
| 12 | The ship-log row | each citation against its source | *FM-035's review R3* ✓, ambiguous (R1). *carried since the 0.18.4 CHANGELOG* ✓. *homed on a Shipped tracker by the same-day pass* ✓ on `86b78e3`. *the pass's Reviewer R4*: named without what it found (R1). *the cold session's line 3* ✗ (R1). |
| 13 | `--check`, `--session-check` | this worktree, at the tip | `--check` exits 0: *INDEX.md is up to date — 38 trackers*; *filing freeze: 22 open, at or above 8 — only bug filings*; the Owner's sections guarded; judged before build on. `--session-check` exits 0 ✓. |
| 14 | Both suites by hand | `python3` (3.14.3) and `/usr/bin/python3` (3.9.6) | `test_shoalmark.py`: 462 ok, 0 skip, *skipped here: 0 checks — every check ran*, *all green* on each (526 s and 382 s, load average 6–8). `test_core.py`: 148 ok, *all green* on each (4 s). The tree was clean after ✓. |
| 15 | merge-tree | `git merge-tree --write-tree` against `8725440` and `86b78e3`; a scratch merge of `86b78e3` with INDEX.md regenerated | `8725440`: the tip's own tree, `af2468d4…`. `86b78e3`: clean, exit 0, tree `806882ef…`. The scratch merge's INDEX.md is the regenerated one, but for the ledger lines its own trailer-less commit adds ✓. |
| 16 | Fact (2) in this worktree | this verdict file staged alone; `lefthook run pre-commit --command tests` | *tests (skip) no matching staged files*: the verdict commit below runs no suite ✓. |

## Findings

**R1 · P3 · confidence 97% · The two sources are cited where a reader will not find them.**
- *The gap:*
  - Fact (2) cites `review-0.18.4-cut-df48d67.md`, *its line 3*; the ship-log row says *the cold session's line 3*. The
    file's line 3 is its `Reviewed:` sha. The statement is at lines 59–66 (under R1, *The placement*: *One precision on
    where it bites, not a finding*) and 91–93 (*Findings*). *Line 3* is the Owner's path line 3, under which that
    session was started (its line 10).
  - Fact (1) cites *FM-035's review R3*. Two FM-035 review files have an R3: `review-fm-035-ci-red-filed.md:67`
    (`considered:` leaves out FM-003) and `review-fm-035-ci-green-on-every-platform.md:227` (the hook). The CHANGELOG
    says which (*the CI fix's review*); the filing does not.
  - The row's *homed on a Shipped tracker by the same-day pass — the pass's Reviewer R4* names R4 without what it
    found: a Shipped tracker is a record, not a queue — no pass and no list reads it — and the line wants this filing.
- *Why it matters:* a filing is read cold. Its citations are how a reader checks its facts without the Principal.
- *What closes it:* `review-0.18.4-cut-df48d67.md:59–66` (and 91–93) for fact (2);
  `review-fm-035-ci-green-on-every-platform.md`, R3 (round two, on `4e4d63b`) for fact (1); R4 named as the finding
  that asked for this filing. In the line and in the row.

**R2 · P3 · confidence 95% · Fact (1) is stated wider than the hook does it.**
- *The gap:* *never seen at commit time; only CI on the tag shows it*. `lefthook.yml:5` hides the output only while a
  suite exits 0. On a non-zero exit it prints the interpreter and runs the suite again with only the `^  ok` lines
  dropped — the skip lines shown (check 2). CI also runs on a ready pull request and by dispatch (`ci.yml:6–8`), and a
  run by hand shows them. The CHANGELOG's own line is exact: *on a run that exits 0*, *CI prints the suites whole*.
- *Why it matters:* the Done-when is judged against the fact. *Never* reads as if a failing commit hid them too.
- *What closes it:* *on a commit whose suites pass*, and *only CI — a tag, a ready pull request — or a run by hand shows
  it*, in the What-is-true-now line. The title and `hook:` can keep the short form.

**R3 · P3 · confidence 90% on the fact, 70% on the grade · The Done-when carries half of R3's closure.**
- *The gap:* R3's closure (`review-fm-035-ci-green-on-every-platform.md:241–245`) has two parts: keep a passing suite's
  skip summary in the hook's output, *and qualify the final success line when checks were omitted* — proved with an
  unavailable-browser fixture, and without changing the non-zero exit for a broken page. `test_shoalmark.py:4298–4303`
  still prints *all green* after *this is NOT a full pass*. The Done-when asks for the summary lines at commit time and
  a suite case for a silent skip. It does not ask for the last line, and it does not keep the exit.
- *Why it matters:* the filing is on R3. A build judged against this Done-when can close it with *all green* still
  printed under a partial run — the qualification R3 said the summary was designed to carry.
- *What closes it:* the Done-when takes R3's second part (a run with skips does not end *all green*), or says why it
  leaves it; and the broken page's non-zero exit is kept.

**R4 · P3 · confidence 85% on the fact, 60% on the grade · FM-032 is not held against, and the Done-when prices every
docs commit at the full suites.**
- *The gap:*
  - `--related` at `8725440`, in fact (2)'s own words, ranks FM-032 third (2.3). FM-032 is In Progress: *the loop costs
    the same for a docs row as for a migration*, on the Owner's word *overregulation*; its line is *keep the loop where
    the risk is, in code, and take it off where it is not*. `considered:` names FM-035, FM-028 and FM-017.
  - The Done-when requires *runs both suites on every commit* and *a docs-only commit shows the suites ran*, so its *or
    prints one line saying it did not* cannot serve a docs-only commit.
  - Here, under load average 6–8, `test_shoalmark.py` took 526 s on 3.14.3 and 382 s on 3.9.6, `test_core.py` 4 s each:
    about 15 minutes of hook on every verdict, filing and ledger commit. The glob and the redirect date from `a680fdf`
    (0.1.0); neither was a ruling on cost.
- *Why it matters:* the Done-when picks a cost that the Owner's ruled direction weighs against, and does not say so.
  The FM-033 pass before the build would meet it unannounced.
- *What closes it:* FM-032 in `considered:` with one clause, and the Done-when naming the cost it accepts, or stating
  the outcome it wants for a docs-only commit and leaving the mechanism to the judging pass. Not a design ruling of this
  pass.

**R5 · P3 · confidence 90% on the facts, 55% on the grade · The filing does not say why a defect of the repository's
own hook passes the freeze, and fact (2)'s source called it not a finding.**
- *The gap:*
  - AGENTS.md, lines 51–54: under the freeze *only product defects are filed — `tags: bug`, something the tool does wrong
    for the person using it*; anything else is a line in the closest open tracker, or waits. The filing says *the tool
    is not changed by them*. `lefthook.yml` and the suites are not in `TOOL_FILES` (`shoalmark.py:5411`); README §6's
    lefthook block for a consumer has no suite step; the vocabulary's `process` names *tooling* (`shoalmark.py:103`).
  - The filing calls both facts *findings of the day*. The cut review called (2) *not a finding* and *not a defect of
    this cut — the binding holds before every merge* (lines 59–66, 91–93).
  - The case for `bug` is on the record, and the filing does not make it. `ci.yml:3–4` runs CI only on a tag and a
    ready pull request because *the suites run locally on every commit through the hook*; the glob makes that false —
    *something that worked, or was meant to, and does not* (`bug`, `shoalmark.py:100`). The checks a docs-only cut
    skips — the setup pages' tag, `__version__` and the CHANGELOG head against `VERSION` — guard what the person using
    the tool clones.
  - `--new --tags bug` admitted it; the gate reads only the tag. Both triage passes' R4 said the freeze admits a bug
    filing (*a bug filing, which the freeze admits*; *the bug filing (the freeze admits it)*).
- *Why it matters:* the freeze is the Owner's rule (FM-032 S4). A filing that passes it should say why in its own text,
  above all when one of its sentences reads against the rule's gloss. A stricter reader grades this P2 and sends the
  two facts to a line on FM-028.
- *What closes it:* one sentence in *What is true now* or *Why*: why this is a bug (the `ci.yml` premise), and that the
  cut review ruled (2) not a finding of that cut. Or the Principal carries both as a line on FM-028 instead. The
  Principal's call; this pass does not rule it.

**R6 · P3 · confidence 95% on the fact, 75% on the grade · Triage R4's closure is half done: FM-035's line does not
point here.**
- *The gap:* both triage passes close R4 on *the bug filing …, with FM-035's line pointing to it*
  (`review-triage-2026-09-26-the-brand-raised.md:211–213`; `…-2.md:137`). On `origin/main` `86b78e3` (PR 89, merged
  during this pass) FM-035's lines 16 and 52 carry R3 and name no FM-038. The branch's base, `8725440`, predates PR 89,
  so the filing could not.
- *Why it matters:* a reader of FM-035 finds an *open, for the release after* line on a Shipped tracker, with no home
  named. R4's queue gap stays open.
- *What closes it:* after a merge of `origin/main` into this branch, FM-035's carried line and row name FM-038.

**Noted, not graded.**
- The hook's interpreter loop passes silently where `/usr/bin/python3` is absent (`[ -x "$(command -v $py)" ] && …`):
  the suites then run once. The Done-when's *or prints one line saying it did not and why* covers it; the facts do not
  name it.
- The freeze is enforced by `--new` alone. The brief's *the freeze line says a bug filing passes* holds only as far as
  `--check`'s line goes: it reports the freeze and judges no filing (check 9).

## Verdict — READY WITH FINDINGS (R1–R6, all P3), 80%

**READY WITH FINDINGS.**
- Both facts are true on `origin/main`, by reading and by control. The hook sends a passing suite's output, skip lines
  included, to `/dev/null` (check 2). The `tests` step runs only when a `.py` is staged, and a cut stages none (check 4).
- The filing is `--new`'s own skeleton and front matter, plus `considered:` (check 9). No open tracker holds either
  fact, and FM-028 is rightly not the home (check 8). The Done-when is decidable, and the Why is the filing's.
- `--check` and `--session-check` exit 0. Both suites are green on both Pythons. merge-tree is clean on `8725440` and on
  `86b78e3`.
- The six P3s are text. R1, R2 and R5 fall on the What-is-true-now line and the row; R3 and R4 on the Done-when and
  `considered:`; R6, after a merge of main, on FM-035. None needs a re-pass. R5 is the one a stricter reader grades P2,
  and it is the Principal's call, with its evidence here.

*The Owner lands this by merging, and a merge rules nothing (path 5).*
