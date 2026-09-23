# Review — 0.17.5, one id finds one row, and an empty section says why

- **Date:** 2026-09-23, 14:08 CEST (`date`)
- **Seat:** Reviewer (`reviewer@seat`) · **Model:** Claude Opus 5.5 (`claude-opus-5-5`)
- **Tip reviewed:** `8402732` on `fix/0.17.5-one-id-one-row-and-an-empty-bucket-says-why` · **Base:** `b341657` (`origin/main`, tag `v0.17.4`)
- **Commits:** `0231287 2cc1db3 cac3d64 89c401f 7bc780d a61451c` (Implementer seat), `8402732` (Principal seat)
- **Scope:** FM-020 (search), FM-021 (progress line), FM-022 (the intent scaffold), the docket (eight trackers set to Shipped, `kind-of-problem:`, `[seats] reviewer`), and the release plumbing (`VERSION`, `CHANGELOG.md`).

## Cold start

1. **What virtue do I bring?** Doubt. Every claim the `v0.17.5` tag would carry has to be re-derived first-hand: the
   gates, whether each new check fails on 0.17.4, and the Implementer's numbers from the consumer's board.
2. **How does it turn into blindness?** I could grade a change the Owner asked for (one id, one row) as a defect. I
   could count a deliberate control check as a missing fail-before. I could mistake severity for rigour.
3. **What would show that failure here?** A finding with no measured difference between 0.17.4 and 0.17.5, or with no
   count behind it. As a positive control, I first reproduced the Implementer's consumer numbers (24→1, 10→1, 28, 40,
   64) in headless Chrome. If those had not matched, my harness would have been wrong, not the release.
4. **Who gets the record, independently of me?** The Principal seat, which grades and disposes of these findings, and
   then the Owner, who merges and tags. This file disposes of nothing.

## Method

- **Suites:** both suites under `python3` (3.14.3) and `/usr/bin/python3` (3.9.6), the interpreters the pre-commit hook
  uses. I ran `--check` and `--html-only` on the tree.
- **Fail-before:** I archived `origin/main` into a scratch directory, copied in this branch's two test files, and ran
  them against the 0.17.4 tool.
- **Consumer board:** I rendered the consumer's board in memory: its `docs/work-tracker`, 505 trackers, deriver in
  `board` mode, both tool versions. `render_html` wrote only to scratch, and `git status` in the consumer showed 0
  changes afterwards. I read each board in headless Chrome by appending a probe script that drives `draw()` in three
  views: board · story/open · story/all, plus suite/open.
- **Scaffold and progress line:** `--init`, `--triage` and the progress-line cases ran in scratch repositories.
- **`--vendor`:** into a scratch copy of the consumer's `tools/shoalmark` (0.17.4).

## Findings

### R1 · P2 · An id searched in an *open* view counts a closed tracker as "1 open"

- **What:** An exact id skips the open filter (`exact?t==exact:(every||OPEN.has(t[2]))&&…`). The counter still picks
  its noun from the view: `hood ? around : every ? trackers : open`. So in any view except the board, with *open*
  pressed, a Shipped or Closed tracker searched by its id is counted as open.
- **Repro:** On the consumer's board, 0.17.5. `BUG-246` (Closed) in the story view with *open*, and in the suite view
  with *open*, both give `1 open · 0 P0/P1 · 0 in progress` beside a row whose status reads Closed. The board view,
  the first view, says `1 trackers` and is correct, because its open/all toggle is hidden there. `~ID` has its own noun
  (`N around ID`) and does not have this problem.
- **Where:** `shoalmark.py:1206` and `:1208` (the exact path), `:1226` (the counter).
- **Cost:** The count on the page is wrong about the one row it shows. The FM-020 tracker says the exact path behaves
  "like `~ID`", but `~ID` changes the noun and this path does not.
- **Confidence:** High. Measured in Chrome in two views.
- **Falsifier:** A non-board view with *open* pressed that shows a closed id and a noun other than `open`.
- **What closes it:** Give the exact path its own noun: `count.trackers`, or a label such as `id`. Add a Chrome check
  that searches a Shipped id in a non-board view with *open* pressed.

### R2 · P2 · The release note says "`~ID` is that search", but on the consumer's board it misses 86 rows the id search used to find, including 30 chapters of one story

- **What:** `CHANGELOG.md:15–16` tells a consumer: *If you used an id to find what references it, `~ID` is that
  search.* `~ID` is the id itself, what its body links to, and what links to it — Markdown links only (`near`,
  `shoalmark.py:1207`; `inb`, `:1181–1182`; `TRACKER_LINK_RE`, `:220`). A row that refers to the id another way was
  found by 0.17.4's substring search and is found by neither search in 0.17.5. The other ways are a chapter's
  `epic:`, `blocked-by:`, an id in plain text in a hook, or a triage verdict.
- **Measured:** On the consumer's board at 0.17.4 I searched every one of the 505 ids whole, with a word-boundary
  match so a longer id with the same prefix does not count.

  | measure | count |
  |---|---|
  | rows found that are not the id's own row | 2 199 |
  | of those, also in `~ID` | 2 113 |
  | in neither search at 0.17.5 | **86 rows, across 43 ids** |

  Why the 86 were found at 0.17.4:

  | reason | rows |
  |---|---|
  | a chapter's `epic:` (all `FEAT-124`) | 30 |
  | the id in a hook | 35 |
  | a triage verdict | 18 |
  | other | 3 |

  `FEAT-124`, the story with 42 chapters:

  | search | rows |
  |---|---|
  | `FEAT-124` at 0.17.4 (all · open) | 87 · 74 |
  | `FEAT-124` at 0.17.5 | 1 |
  | `~FEAT-124` at 0.17.5 | 49 |

  The 49 rows of `~FEAT-124` include none of the 30 chapters that do not link to it.

  In the story view the header still says *42 chapters: 1 done · 41 open* over the single row, because the header
  counts from `T`, not from the rows shown.
- **Where:** `CHANGELOG.md:15–16`, and the comment at `shoalmark.py:1205` ("`~ID` is how to ask for those").
- **Cost:** The note that `--vendor` prints to every consumer points the Owner to a search that silently leaves out
  the chapters of his most active story. The story view still lists them, but nothing in the release says so.
- **Confidence:** High. Both versions measured in headless Chrome.
- **Falsifier:** A `~FEAT-124` result that contains the 30 unlinked chapters.
- **What closes it:** One of two changes. Either widen `near` to cover chapters (`t[13]==id`), the id's own story
  (`hood[13]`) and `blocked-by:` (`t[16]`), with a Chrome check for an unlinked chapter. Or narrow the sentence to
  what `~ID` actually shows ("what links to it") and name the story view for chapters. Choosing between them is the
  Principal's decision.

### R3 · P3 · The ship logs say every new Chrome check was "shown to fail on 0.17.4"; three of the five pass on 0.17.4 by design

- **What:** FM-020's ship log (`FM-020…md:59`) says *two Chrome checks and a string check, shown to fail on 0.17.4*.
  FM-021's ship log (`FM-021…md:59`) says *three Chrome checks and a string check, shown to fail on 0.17.4*.
- **Measured:** I ran this branch's tests against the 0.17.4 tool.
  - **Fail on 0.17.4:** FM-020 whole id, FM-021 "before", FM-022, and both `test_core.py` string checks.
  - **Pass on 0.17.4, as controls should:** FM-020 `~ID`/partial/word, FM-021 "after", and FM-021 "TRIAGE.md
    records a pass".
  - **Also passes on 0.17.4:** the new CHANGELOG/version consistency check.
  - The existing C4 German-parity check also fails on 0.17.4, because the fixture gained the new key.
  - The tables in the trackers state the controls correctly. Only the ship-log sentences overcount.
- **Cost:** Wording. The fail-before claim of each behaviour does hold.
- **Confidence:** High.
- **What closes it:** Reword each ship-log line to "…one fails on 0.17.4; the others are controls".

### R4 · P3 · Two lines of the board disagree on whether a pass has run

- **What:** `progress` decides with `LAST||HOME.last`. `triaged` decides with `LAST` alone (`shoalmark.py:1198`).
- **Repro:** Build the state FM-021's third check creates: `TRIAGE.md` records a pass and no tracker carries
  `triaged:`. The board reads *progress · 0 · kept by triage — by rank, then tier*. Three lines below, it reads
  *triaged · 0 · no triage pass has run yet*, with the pass paragraph printed under that heading.
- **Where:** `shoalmark.py:1198`. The `triaged` half is older than this release. FM-021 added a second definition of
  "a pass has run" beside it.
- **Cost:** A label that contradicts the line next to it. The state is narrow: every verdict of a pass writes
  `triaged:`.
- **Confidence:** High. Rendered in Chrome.
- **What closes it:** Use one predicate for both lines, and assert the `triaged` line in the existing third check.

### R5 · P3 · Once the Owner writes one intent line, the lead-in and the two remaining examples are printed to every pass as his intent

- **What:** `said()` (`shoalmark.py:1537`) treats the whole section as said or unsaid. I overwrote only
  `- **for** —` in a scratch `--init` and ran `--triage`. It printed, under *THE INTENT — the Owner's own words … this
  decides it*:
  - the three-line lead-in,
  - the Owner's one line,
  - the two library examples (`*e.g. … nothing on loan is lost*`, `*e.g. lend what the catalogue does not hold…*`).

  After all three lines are overwritten, the lead-in is still printed with every pass unless the Owner deletes it.
  The FM-022 check pins exactly this case ("one line in the Owner's words is [an intent]").
- **Where:** `shoalmark.py:1537`, `:3242`, and `TRIAGE_HOME` (`:2841–2869`). `README.md:170` ("Until he writes words
  of his own, the examples are not read as an intent") is true but says nothing about the partial case.
- **Cost:** A seat judging tiers is handed a village library's *never* rule as part of the Owner's intent. The
  `e.g.` marks it, which limits the harm.
- **Confidence:** High. Reproduced.
- **What closes it:** Leave italic-only lines (the lead-in, the `*e.g. …*` remainders) out of the intent as it is
  printed. Or say in README §6 that they are read until they are deleted.

### R6 · P3 · The new search hint is longer than the search box at every width measured, and `blocked · untriaged` drop out of sight

- **What:** The input is `flex:1;min-width:200px`, 15 px monospace (`shoalmark.py:1103`).

  | hint | characters | width |
  |---|---|---|
  | English, 0.17.5 | 97 | 876 px |
  | English, 0.17.4 | 77 | 695 px |
  | German, 0.17.5 | 90 | 813 px |

  | board | input width at windows 500 / 800 / 1280 |
  |---|---|
  | shoalmark's own | 392 / 391 / 691 px |
  | the consumer's | 392 / 692 / 464 px |

  What a 1280 px window shows of the hint:

  | board | 0.17.4 | 0.17.5 |
  |---|---|---|
  | shoalmark's own | `…blocked · untriaged · ~ID = its neighbour` | cut at `…tier, status, words ` |
  | the consumer's | `…blocked · untria` | `…~ID = its neighbou` |

  On the consumer's board `~ID` became visible, which it was not before.
- **Where:** `shoalmark.py:1347`, `examples/de/labels.yaml:3`.
- **Cost:** Wording and layout. The new lead phrase, the one that matters, is visible at every width.
- **Confidence:** High. Measured with the canvas in Chrome.
- **What closes it:** A shorter hint, or the full text in a `title` attribute.

### R7 · P3 · The CHANGELOG's example count reads one group as the board, and ships a consumer's tracker id

- **What:** `CHANGELOG.md:12` says *`FEAT-161` showed 17 rows on a 505-tracker board, 16 of them only through a
  link*. Measured at 0.17.4:

  | view | rows |
  |---|---|
  | board · all | 24 |
  | open | 10 |
  | the `agentic-portfolios` group of the suite view | 17 |

  Of those 17, 16 match only through `t[12]`, the ids a row's body links to. The FM-020 tracker states this
  correctly; the CHANGELOG compresses it into a board count.
- **Where it ships:** `CHANGELOG.md` is in `TOOL_FILES` (`shoalmark.py:2788`), so `--vendor` copies it into every
  consumer, the two client repositories included. `FEAT-161` is the first consumer tracker id in any
  CHANGELOG/README line. `git grep -E '(FEAT|BUG|ALIGN|PD)-[0-9]+' origin/main -- CHANGELOG.md README.md` finds none.
  The brief's grep (`portdive|msr-lager|fb-sondermasch|holgo`) does not catch it.
- **Also:** The new FM-020 tracker names "PortDive's board" (`:35`). The tracker tree is not vendored, and main
  already names PortDive under `evidence/FM-001/port/`, so that is house precedent, not a leak.
- **Cost:** Wording, and a small cross-repository disclosure.
- **Confidence:** High.
- **What closes it:** Replace the sentence with, for example, *one id showed 24 rows on a 505-tracker board, 17 in
  the group the Owner read*, with a synthetic id.

### R8 · P3 · README §8 still says "210 checks"; the suites run 385

- **What:** `README.md:294` says `# 210 checks`. `origin/main` runs 376 (232 + 144). This branch runs 385
  (239 + 146). The count went stale on 2026-09-21 (`73f7ba4`), and this release adds nine checks without updating it.
- **What closes it:** Update the number, or drop it.

### R9 · P3 · FM-013 is closed as Shipped with a remainder nobody holds

- **What:** `8402732` sets FM-013 to `status: Shipped` and removes `next:`. Its *What is true now* still ends
  *What is left: his eye on the three points not proven* (`FM-013…md:23–24`): a real clipboard, a phone-width layout,
  and the signing page. `--next` does not list a Shipped tracker, so nothing will bring that remainder up again.
- **What closes it:** One of: a slice or tracker for the three points, `next: owner` with an ask, or a sentence saying
  they are dropped. This is the Principal's close and the Principal's call.

### R10 · P3 · FM-022 does not reach a German adopter

- **What:** `docs/setup.md:26` tells a German adopter to copy `examples/de/TRIAGE.md` before `--init`. That file still
  has the bare `für —` / `damit —` / `niemals —` lines, with no lead-in and no example. `--init` never overwrites the
  copy. FM-022 names this as not changed on purpose.
- **Cost:** For a German repository, 0.17.5 changes nothing about the way into the intent.
- **What closes it:** A follow-up slice that gives `examples/de/TRIAGE.md` the lead-in and a German whole-product
  example. Or leave it, as ruled.

## What survives the pass

- **FM-020 works as built.**
  - A whole id, trimmed, in any case, shows its own row alone: `feat-161 ` gives 1 row.
  - An id followed by a word (`FEAT-161 stale`) takes the substring path: 1 row in *all*, 0 in *open*, the same on
    both versions.
  - An unknown id (`FEAT-999`) takes the substring path: 0 on both versions.
  - I reproduced the Implementer's consumer numbers in headless Chrome:

    | query | 0.17.4 | 0.17.5 |
    |---|---|---|
    | `FEAT-161` (all) | 24 | 1 |
    | `FEAT-161` (open) | 10 | 1 |
    | `~FEAT-161` | 28 | 28 |
    | `FEAT-16` | 40 | 40 |
    | `market data` | 64 | 64 |

  - For `FEAT-161` itself, every one of the 24 former rows is in `~FEAT-161`.
  - The English and German hints both say what the change does, and the key parity check (C4) is green.
- **FM-021 works as built.**
  - With no pass run, the line reads *empty until a first triage pass has run — --triage*.
  - With `triaged:` on a **Closed** tracker only, the usual line shows. That is right: a pass has run and kept
    nothing in progress.
  - With a dated paragraph in `TRIAGE.md` and no `triaged:` anywhere, the usual line shows (but see R4).
  - The consumer's board reads *kept by triage — by rank, then tier* on both versions.
  - `desc.progress.none` exists in English, in `examples/de/labels.yaml` and in the suite's German fixture.
- **FM-022 works as built.**
  - `--init` writes the lead-in naming the repository as a whole, and one generic whole-product example per line, in
    italics.
  - An untouched scaffold reads as no intent.
  - A second `--init` on an existing tree prints *nothing to write — already initialised* and leaves a line I added to
    `TRIAGE.md` in place.
  - Line 3 of shoalmark's own `TRIAGE.md` now names `shoalmark.py`. Its intent and path sections are unchanged.
  - `git grep fathom_mark` has exactly one hit, `test_shoalmark.py:1812`. It is the fixture of the legacy-hook
    migration test and already exists on main (`:1751`). Nothing else.
- **The docket holds.**
  - Each of the eight flips carries a ship-log line naming its release.
  - Tags `v0.17.3` = `b8c501d` (merge #10) and `v0.17.4` = `b341657` (merge #12) exist on `origin`.
  - FM-009 matches 0.17.3's version-drift entry, and FM-012 matches 0.17.4's "a load no longer spawns git" entry.
  - The body notes are the Implementer's (`89c401f`). The status flips and `kind-of-problem:` values are the
    Principal's (`8402732`), so the rights are split as `[seats]` requires.
  - `kind-of-problem:` values are `obvious`, `obvious`, `complicated`.
  - `[seats]` holds four names, and `--check` exits 0.
  - All three new trackers carry `considered:` and a plain-words hook.
- **Release plumbing holds.**
  - `VERSION` = `__version__` = `0.17.5`. The version is read from the file.
  - The `CHANGELOG.md` section comes first, is dated 2026-09-23 (today), and describes all three changes. It does not
    name the ids, which matches the practice of 0.17.3 and 0.17.4.
  - `--vendor` into a scratch copy of the consumer's 0.17.4 pin printed `(was 0.17.4)` and exactly the 0.17.5
    section. `shasum -a 256 -c PIN` passed on all eight files, and the vendored `shoalmark.py` is byte-identical to the
    tip.
- **Nothing outside scope in the diff.** `git diff origin/main --stat` shows 21 files. All of them are the tool, the
  tests, the docs, the German labels, `shoalmark.toml`, `VERSION`, `CHANGELOG.md` and trackers named in the brief.
- **Chrome ran.** No `skip  no browser found` line under either interpreter, and all five FM-020/021 Chrome checks
  print `ok`. The `test_core.py` string checks cover a machine without a browser.

## Gates on 8402732

| Gate | Result |
|---|---|
| `python3 test_shoalmark.py` (3.14.3) | exit=0 · 239 ok (main: 232; +7) |
| `python3 test_core.py` (3.14.3) | exit=0 · 146 ok (main: 144; +2) |
| `/usr/bin/python3 test_shoalmark.py` (3.9.6) | exit=0 · 239 ok |
| `/usr/bin/python3 test_core.py` (3.9.6) | exit=0 · 146 ok |
| `python3 shoalmark.py --check` | exit=0 — *INDEX.md is up to date — 22 trackers* |
| `python3 shoalmark.py --html-only` | exit=0, tree clean |
| lint | `AGENTS.md` names none, and none is installed (`ruff`, `pyflakes`, `flake8` absent). `python3 -m py_compile` on the three `.py` files: exit=0 each |
| this branch's tests against the 0.17.4 tool | `test_shoalmark.py` exit=1 (FM-022, FM-020 whole id, FM-021 before, C4) · `test_core.py` exit=1 (FM-020, FM-021) |
| `--vendor` into a scratch 0.17.4 consumer | exit=0 · PIN check `OK` × 8 |

## Verdict

**READY WITH FINDINGS:** R1 (P2), R2 (P2), and R3–R10 (P3).

- **No P1.** The tag would carry no wrong behaviour and no absent check.
- **The two P2s** are a count noun that lies in non-board views (R1) and a release-note sentence that sends consumers
  to a search missing 86 of the 2 199 references it replaces, 30 of them one story's chapters (R2).
- **Before `v0.17.5` is tagged,** the Principal decides whether R1 and R2 close now, with a code fix or a rewording,
  or are accepted as they are.
