# Review — FM-030's done-dialog build, the fix pass at 6585cd2 (2026-09-27 22:06 CEST, Reviewer, session `8e509911/reviewer-40`)

- **Branch:** `fm/030-the-done-dialog-shows-the-question`, tip `6585cd2`
  (`6585cd2821ab380c43ae71be24e3b61e4cebaf9f`, confirmed by `git ls-remote`). It adds two Implementer commits
  (`implementer-44`) on my first verdict `d18c9ba` (NOT READY on `9c96f5b`):
  - `2f84d47` — the code for R1–R4, with tests;
  - `6585cd2` — the tracker only: R5, and a ship-log row for the pass.

  `origin/main` is still `67f1bd2`.
- **Tier: code — not critical.** `lefthook.yml`, `scripts/` and `.github/` are untouched, now as at `9c96f5b`. An AST
  diff of `d18c9ba` against `6585cd2` finds these changes in `shoalmark.py`:
  - changed: `result_facts`, `answer_due`, `ANSWER_TIME_RE`, `front_matter_schema` (the row text only), `HTML_PAGE`
    (one CSS rule);
  - added: `_LINE_ANCHOR_RE`.

  None of them is a guard, gate, queue or hook function.
- **Independence:** same session — a sub-agent of 8e509911, reported.
- **Verdict: READY WITH FINDINGS.** R1–R5 are closed. Two new findings, R6 and R7, are P3. The suites' one failure is
  FM-035's 5 s browser case. It fails the same way at the same minute on `origin/main`'s tool: FM-039's, with no diff
  at fault, recorded here and not a blocker.

## What I ran

| run | result |
|---|---|
| my own count over every `review*.md` at the tip | **77** files. The first pass counted 76; the one added since is my own verdict, `review-fm-030-the-done-dialog-9c96f5b.md` (`d18c9ba`). The **last** stated verdict equals the verdict of the newest commit that touched the file and names one in **77 of 77**. The **first** does in **55 of 77**. That matches the Implementer's count |
| the fixed `result_facts` on all 77, against each file's newest verdict commit (the subject's verdict, its `Reviewed:` and `Session:` trailers) | 0 disagree on the verdict, the sha or the session. *last pass in* is written for 30 files. In two, the newest commit to touch the file is not a clean verdict commit: `2e32c3a` corrects a verdict line and carries `Reviewed:`; `0ee3bfc` is a verification pass with no trailer. Both are passes |
| the files of the first pass's R1 | `review-tracker-triage-2026-09-24-evening.md` → *verdict READY WITH FINDINGS, reviewed cb1d05e, session 8e509911/reviewer-2, added in ea4d98a*. `review-0.18.4-fm030-52cfcc7.md` → *READY WITH FINDINGS, reviewed 6270118, …, last pass in 510bc94*. His example, the fourth pass, is unchanged: *READY, reviewed 8c3c10b, session 01a0d6e7* |
| the new checks against `d18c9ba`'s tool and against the tip's (`spot.py`; three spot-checks: R1's two-pass file with its own lines, R2's refused shapes, R3's `#L1-L2`) | all three **fail** on `d18c9ba`: *NOT READY, reviewed aaaaaaa*; `.000Z`, `9:00 PM`, `cest` and `then` each seeded 09:00+02:00; the anchor gave *not in the repository*. All three **pass** on the tip |
| `answer_due` on 19 texts, on this machine's zone | refused, each saying why: `…T09:00:00.000Z` (a fraction of a second), `9:00 PM` and `09:00pm` (a 12-hour time), `cest`, `then`, `Uhr`, `in` (no zone as written). Read: `2026-10-03 09:00, then …` (a comma is no word), `09:00.` at a sentence's end, `+0200`, `Z`, `CEST, then`, and `Sat 09-26 09:00 CEST` → `2026-09-26T09:00:00+02:00` (E0 row 20's own case, kept). Also read, and not stated in `--schema`: `Saturday 09-26 at 9:00`, `sat. 09-26 9:00` and `2026-09-26 9:00`. A zone after punctuation, `09:00 (PST)`, is read in this machine's zone: R7 |
| the zone of a zone-less answer | this machine's: `local_time`, which is `naive.astimezone()`. It is the zone `--done` writes its time in (`datetime.now().astimezone()`). `--due` applies no zone of its own: it refuses a time without one (*is not a time with its zone*). Nothing disagrees; the brief's *what `--due` uses too* is the zone `--done` uses |
| `--done` in a scratch repository with `…/read.md:12`, and `evidence/AP-601/read.md#L1-L9` from the tracker directory | recorded as given, anchor and all: *done — docs/…/read.md:12 (added in 2bfd9e5 …)* and *done — evidence/AP-601/read.md#L1-L9 (docs/work-tracker/evidence/AP-601/read.md, added in …)*. `done:` keeps the anchor too |
| headless Chrome, the list of FM-024's shape, measured per line of each `.aq` by its text's client rects, by `d18c9ba`'s tool and by the tip's | **1440 px:** the old rule's line lefts `[215, 200]`, the new `[215, 215]`. **390 px** (an iframe of that width; the window's minimum is 500): old `[45, 30, 30]`, new `[45, 45, 45]`. The screenshot shows the question wrapping in its own column |
| the tracker, `d18c9ba..6585cd2` | the lead reads **Filed 2026-09-24; built in part, and more on a branch not merged.** and names 0.18.3 and 0.18.4. There is a ship-log row for `a7d0f52` in time order before item 5's, and a last row for the pass and `2f84d47`. The *Built for 0.18.6* clause says *the verdict of its last pass*. The CHANGELOG bullets, README row and `--schema` rows say *last pass*, the anchor and the refused shapes |
| both suites, one interpreter at a time, started at load 2.25 / 1.97 / 2.87, user activity asserted (`caffeinate -u -t 60`, re-asserted) | `test_core.py`: 148 ok / 0 FAIL on 3.14.3 and 3.9.6. `test_shoalmark.py`: **505 ok, 1 FAIL** on 3.14.3 and 3.9.6, *skipped here: 0 checks*. The one FAIL on both is FM-035's healthy-board case: *headless Chrome did not return index.html within 5 s, tried twice* |
| that case alone, built exactly as the suite builds `_block_run("")` (`fm035_healthy.py`), for the tip and for `origin/main`'s tool (`git archive 67f1bd2`), alternately, twice each, 22:04–22:05, load 2.73 at the start | the tip: exit 1, the same FAIL, 16.6 s and 16.3 s. `origin/main`: exit 1, the same FAIL, 16.6 s and 16.2 s. Headless Chrome alone, `--dump-dom about:blank`: **6.11 s and 6.02 s**, with 13 `CVDisplayLinkCreateWithCGDisplay failed` lines. The machine's Chrome is over FM-039's 5 s budget on a blank page, whichever tool renders the board. At 19:17 today the same case passed on `9c96f5b` |
| `--check` | exit 0. *INDEX.md is up to date — 39 trackers*; *judged before build: on — 10 commit(s) … every build commit under a judged In Progress tracker*; *the Owner's two sections: guarded — 12 commit(s) … none changes them or his signers file* |
| `--session-check` | exit 0 |
| `--queue` | `branch fm/030-the-done-dialog-shows-th… @ 6585cd2  wait: no pull request — no verdict on 6585cd2` |
| `git merge-tree --write-tree origin/main HEAD` | clean (`21f7b91`) |

## The first pass's findings

- **R1 ✓.** `result_facts` reads the last line that states a verdict. `Reviewed:` and `Session:` come from that pass's
  own lines: the nearest after the verdict line, or the file's only value. Where the file has neither, they come from
  the trailers of the newest commit that touched the file, and that commit is named *last pass in*.
  - It agrees with every one of this repository's 77 review files.
  - The two-pass suite cases (AP-485, AP-486) fail on `d18c9ba` and pass here.
  - **The departure, judged.** *last pass in* is written only for a review. That is right: a later edit of a plain
    file is no pass, and *added in* stays true of it.
  - **The ruled fallback.** The newest commit that touched the file is used, not the newest that carries a `Reviewed:`
    trailer. It holds in every file here, but it can misname a pass: R6.
- **R2 ✓** for the four shapes named: a fraction of a second, a 12-hour time, a lower-case zone, and a word after the
  time (`then`). Each is refused, says why, and the act shows *no date yet*. E0 row 20's own form is kept and read.
  - **Against *reads only the shapes `--schema` states*:** `--schema` states `2026-09-26 09:00`,
    `2026-09-26T09:00+02:00` and `Sat 09-26 09:00`, and its refusals. It does not state the single-digit hour, `at`, or
    the long and lower-case weekday spellings, which the reader also reads. It also misses a zone written after
    punctuation: R7.
- **R3 ✓.** A trailing `:12`, `:3-9`, `#L1` or `#L1-L9` is stripped for the lookup only. The name is looked up as
  given first, and the record and `done:` keep it as given.
- **R4 ✓.** `#p .aq` is an `inline-block`. The question's every line starts at 215 px at a width of 1440 and at 45 px
  at 390, against 215/200 and 45/30 before. These are the Implementer's numbers, reproduced.
- **R5 ✓.** `a7d0f52` has its ship-log row, and the lead no longer says *nothing is built*.

## Findings

**R6 · P3 · confidence high (the mechanism); 0 of 77 files here — the trailer fallback reads the newest commit that
touched a review, whatever that commit was.** In a scratch repository I made a review with no `Reviewed:` or
`Session:` line of its own, added by `review: AP-701 — READY` with `Reviewed: 1234567…` and
`Session: 8e509911/reviewer-50`. A later commit, `FM-001: a link fixed in the reviews folder`, carried
`Session: 8e509911` and touched the file. It gave:

*verdict READY, session 8e509911, added in ec35327 …, last pass in 0910834 …*

That record has three problems:
- the reviewer's sha is gone;
- the session is the link-fixer's;
- the link fix is named the last pass.

Nothing in this repository does this today. A Principal's rename or link fix in the reviews folder would. The rule
was ruled so, and the Implementer disclosed it.

**Fix:** take the fallback, and *last pass in*, from the newest commit that touched the file **and** carries a
`Reviewed:` trailer (or names a verdict in its subject). Add a test with one later non-review edit.

**R7 · P3 · confidence high — the time reader still reads beyond what `--schema` states in two ways.**
1. A zone written after punctuation is dropped. `2026-10-03 09:00 (PST)` is read as `2026-10-03T09:00:00+02:00` in
   this machine's zone. The `(` stops the word check, so a named zone gives way to the machine's (the same kind of
   drop R2 closed for a bare word).
2. The reader also reads the single-digit hour, `at`, and `Saturday` or `sat.`. That is harmless, since each is
   unambiguous and its weekday is checked, but `--schema`'s `due:` row does not state them.

**Fix:** refuse a letter run after the time that follows `(`, `/` or a dash, or read the zone inside the parentheses.
State the single-digit hour, `at` and the weekday spellings in the `due:` row and the README, or stop reading them.

## Not proven here

- The notices on Linux and Windows, as before.
- **The suites' one failure.** FM-035's healthy-board case fails on this machine tonight at a 5 s budget, and on
  `origin/main`'s tool alike, so the suites are not all green here. It passed at 19:17 on `9c96f5b`. It is FM-039's,
  with no diff at fault.

## Verdict

**READY WITH FINDINGS.** R1–R5 are closed. R6 and R7 are P3, fixed forward. One FAIL is recorded: FM-035's 5 s case,
which fails identically on `origin/main`'s tool at the same minute (FM-039).

The Owner lands this by merging; a merge rules nothing.
