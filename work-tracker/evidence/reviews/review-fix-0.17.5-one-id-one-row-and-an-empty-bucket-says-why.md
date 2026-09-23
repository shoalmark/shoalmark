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
- **Repro:** On the consumer's board, 0.17.5. `<closed id>`, a closed tracker's id, in the story view with *open*, and in the suite view
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
  | a chapter's `epic:` (all of one story, `<story>`) | 30 |
  | the id in a hook | 35 |
  | a triage verdict | 18 |
  | other | 3 |

  `<story>`, the consumer's largest story, 42 chapters:

  | search | rows |
  |---|---|
  | `<story>` at 0.17.4 (all · open) | 87 · 74 |
  | `<story>` at 0.17.5 | 1 |
  | `~<story>` at 0.17.5 | 49 |

  The 49 rows of `~<story>` include none of the 30 chapters that do not link to it.

  In the story view the header still says *42 chapters: 1 done · 41 open* over the single row, because the header
  counts from `T`, not from the rows shown.
- **Where:** `CHANGELOG.md:15–16`, and the comment at `shoalmark.py:1205` ("`~ID` is how to ask for those").
- **Cost:** The note that `--vendor` prints to every consumer points the Owner to a search that silently leaves out
  the chapters of his most active story. The story view still lists them, but nothing in the release says so.
- **Confidence:** High. Both versions measured in headless Chrome.
- **Falsifier:** A `~<story>` result that contains the 30 unlinked chapters.
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

- **What:** `CHANGELOG.md:12` says *`<linked id>` showed 17 rows on a 505-tracker board, 16 of them only through a
  link*. Measured at 0.17.4:

  | view | rows |
  |---|---|
  | board · all | 24 |
  | open | 10 |
  | one group of the suite view | 17 |

  Of those 17, 16 match only through `t[12]`, the ids a row's body links to. The FM-020 tracker states this
  correctly; the CHANGELOG compresses it into a board count.
- **Where it ships:** `CHANGELOG.md` is in `TOOL_FILES` (`shoalmark.py:2788`), so `--vendor` copies it into every
  consumer, the two client repositories included. That id is the first consumer tracker id in any
  CHANGELOG/README line. A `git grep` for the consumer's id prefixes over `CHANGELOG.md` and `README.md` on `origin/main` finds none.
  The brief's grep for the consumer's and the clients' names does not catch it.
- **Also:** The new FM-020 tracker names the consumer (`:35`). The tracker tree is not vendored, and main
  already names the consumer under `evidence/FM-001/port/`, so that is house precedent, not a leak.
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
  - An id followed by a word (`<linked id> stale`) takes the substring path: 1 row in *all*, 0 in *open*, the same on
    both versions.
  - An unknown id (`<unknown id>`) takes the substring path: 0 on both versions.
  - I reproduced the Implementer's consumer numbers in headless Chrome:

    | query | 0.17.4 | 0.17.5 |
    |---|---|---|
    | `<linked id>` (all) | 24 | 1 |
    | `<linked id>` (open) | 10 | 1 |
    | `~<linked id>` | 28 | 28 |
    | `<partial id>` | 40 | 40 |
    | `<two words>` | 64 | 64 |

  - For `<linked id>` itself, every one of the 24 former rows is in `~<linked id>`.
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

## Verification addendum

- **Date:** 2026-09-23, 15:00 CEST (`date`) · **Seat:** Reviewer (`reviewer@seat`) · **Model:** Claude Opus 5.5
- **Tip verified:** `1e6c333` — the Implementer's closures `1eb264e` … `af00a40`, the R6 check fix `5fb69fa`, and the
  merge of `origin/main` at `73f8ca1` (the Owner's #13: his intent and path in `TRIAGE.md`).
- **Rulings taken as given:** R2 reworded, `~ID` not widened. R4 fixed, not filed. R8's number dropped. R9's remainder
  moved to FM-018.

### Redaction of this file

The Owner's rule is that consumer state does not enter shoalmark; numbers may. This commit replaces every consumer
id and name above with a placeholder and keeps every number.

| placeholder | what it stands for |
|---|---|
| `<linked id>` | a parked tracker that 23 other rows reference (24 rows at 0.17.4, itself included) |
| `<story>` | the consumer's largest story, 42 chapters |
| `<closed id>` | a closed tracker |
| `<partial id>` | the linked id without its last digit |
| `<unknown id>` | an id that does not exist |
| `<two words>` | a two-word query |

Three other things were reworded the same way: the suite group, the consumer's id prefixes in a grep, and the
consumer's and clients' names.

Two commit messages on this branch still name consumer ids. They are history and stay as they are:
- `2cc1db3`, the Implementer's: one id and the board's size.
- `5a9779d`, this seat's first pass: one story id.

### Each closure on the tip

- **R1 · closed.** On the consumer's board at the tip, the closed id reads `1 tracker · <closed id> · 0 P0/P1 · 0 in
  progress` in the board, story/open, story/all and suite/open views. The new Chrome check fails at `8402732`
  (`1 open`).
- **R2 · closed by rewording, as ruled.** The CHANGELOG now says `~ID` is Markdown links only and a story's chapters
  are the story view. It also says a chapter's `epic:`, a `blocked-by:` or an id in plain text is in neither search.
  That matches what I measured. `search.help` says the same, and FM-020 carries the open design question. The
  controls on the consumer's board are unchanged at the tip:

  | query | all | open |
  |---|---|---|
  | `~<linked id>` | 28 | — |
  | `<partial id>` | 40 | 18 |
  | `<two words>` | 64 | 18 |

- **R3 · closed.** The corrections in FM-020 and FM-021 say *5 fail on 0.17.4, 4 are controls*. That is my count.
- **R4 · closed.** `PASSED` answers for both lines. In the narrow state, the triaged line now reads *judged
  2026-09-20* (rendered first-hand). The check fails at `8402732`.
- **R5 · closed for what it named, but see R11.**
  - A fresh `--init` scaffold returns `intent == ""` and `path == ""`.
  - shoalmark's own `TRIAGE.md` returns lines 10–12 exactly, the Owner's three lines.
  - One overwritten line returns that line alone.
  - `--triage` prints only his three lines under *THE INTENT*.
  - On the consumer, the tip reads 4 of the 6 lines 0.17.4 read. The 2 it drops are one italic provenance note, as
    designed.
  - *Observed, not new, not a finding:* `path` is still the whole section, so `--triage` prints the template's italic
    note *The Owner's. A pass judges every tier…* above his four path lines. That was so before this release.
- **R6 · closed at 500 px; refuted "at its narrowest", see R12.**
  - The hint fits in a 500 px window. English needs 362 px of a 392 px box. German needs 371 px of the 377 px box in
    the check's German board, a 6 px margin; both fonts are monospace, so the margin should hold on other systems,
    but CI has not run.
  - The box's title carries the whole help (189 characters).
  - The check fails at `8402732`.
- **R7 · closed in the files that ship.**
  - The CHANGELOG's example is now `FM-005`.
  - FM-020's hook and its *Reproduced* paragraph are generic.
  - Before this redaction, the only consumer ids or names in the diff against `origin/main` were in this file.
- **R8 · closed.** README §8 carries no number.
- **R9 · closed.** FM-018 carries the three points as an open item, and FM-013 points to it.
- **R10 · closed.** `examples/de/TRIAGE.md` has the lead-in and the examples. `triage_home()` reads none of them, and
  reads one written line as exactly that line. The check fails at `8402732`.
- **The merge · verified.** `TRIAGE.md` differs from `origin/main` (`73f8ca1`) only in line 3. His intent lines 10–12
  and his four path lines (19–22) are unchanged.

### R11 · P2 · The new intent reader silently drops an Owner line that has no plain word of three letters — including the line the scaffold invites him to write

- **What:** `written` (`shoalmark.py:1545`) keeps a line only if `said(l)` holds (`:1541`). That means a word of three
  or more letters must remain once every `**…**` and every `*…*` is removed. An Owner line fails that test when its
  words are all emphasised, or all short. Also, the step that strips an example after a line's dash strips *any*
  italic text there, not only the template's `*e.g. …*`. 0.17.4 read the whole section as soon as anything in it was
  said. I measured the cases with the tip's `triage_home()` in scratch repositories:

  | the Owner's line | at the tip | at 0.17.4 |
  |---|---|---|
  | `- **never** — *sell what we lack*` (his words typed inside the example's asterisks) | dropped | read |
  | `- **never** — **sell what we lack**` | dropped | read |
  | `- **never** **sell what we lack**` | dropped | read |
  | `- **so that** — it is ok` | dropped | read |
  | `- **never** — go` | dropped | read |
  | a wrapped line continuing in italics (`  *all of it*`) | dropped | read |
  | all three lines inside the asterisks | intent `""` | intent `""` |

- **Why it matters:** The first row is the natural edit of the new scaffold. The example sits inside `*…*`, and
  replacing the words while keeping the asterisks produces exactly that row. The lead-in the Owner writes under
  (`shoalmark.py:2860–2862`, and `examples/de/TRIAGE.md`) says *overwrite it* and nothing about italics. Only README
  §6 (`:170–171`) and the CHANGELOG say an italic line is a note, and neither says that bold or short lines go too.
  Nothing warns: `--check` exits 0, and `--triage` prints what is left under *this decides it*.
- **The claim the tag would carry:** CHANGELOG `:24–26` says *The intent a pass prints is what the Owner wrote … one
  line of his own is that line alone*. It is false for every row above.
- **Where:** `shoalmark.py:1541`, `:1545`, `:2860–2862`, `examples/de/TRIAGE.md:10–12`, `README.md:170–171`,
  `CHANGELOG.md:24–26`.
- **Cost:** An Owner's `never` line can leave every pass's intent without a trace. Measured: 0 of the 2 intents I
  could read are affected (shoalmark's own, the consumer's). The client repositories' intents are unread, which is
  out of scope. New adopters get the scaffold that invites the first row.
- **Confidence:** High on the mechanism (7 cases, both versions). The frequency is unknown.
- **Falsifier:** Any row above for which the tip's `triage_home()["intent"]` returns the line.
- **What closes it:** One of these, with a check for each dropped row that the fix covers:
  - Drop only the template's own text: a paragraph wholly in italics, and an example that still begins with the
    template's marker (`*e.g. `, `*z. B. `). Keep any other line with any word.
  - Or keep the design and make the lead-in say it, in English and German: *write in plain text — a line in italics
    or bold alone is read as the template's*. Then reword the CHANGELOG claim.

  The fix is about one line. Choosing between the two is the Principal's decision.

### R12 · P3 · The hint does not fit the box "at its narrowest"; the check measures a 500 px window, where the box is not at its narrowest

- **What:** FM-020's *What is true now* (`:21`) says the hint is *short enough for the box at its narrowest*. The
  commit `1d054b2` says the same. But the box is `flex:1;min-width:200px` (`shoalmark.py:1103`), so it shrinks to near
  200 px whenever the counter still fits on its line. I measured in Chrome, with no query typed:

  | board | window | box |
  |---|---|---|
  | shoalmark's own | 640 · 700 · 760 px | 231 · 291 · 351 px |
  | shoalmark's own (sweep) | ≈612–762 px | 203–354 px |
  | the consumer's, longer counter | 860 · 900 · 960 · 1000 px | 224 · 264 · 324 · 364 px |
  | the consumer's (sweep) | ≈842–1000 px | 206–366 px |

  The English hint needs 362 px and the German 371 px, so both are cut across those ranges. At 200 px the visible
  hint is *search — an id · ~ID =* in English and *Suche — eine Id · ~Id* in German.
- **Where:** `shoalmark.py:1103`, `:1350`; `FM-020…md:21`; the R6 check's `--window-size=500,900`.
- **Cost:** Wording. The tokens that matter (an id, `~ID`) stay visible, and the title holds the whole help. The
  CHANGELOG's *fits the box at about 390 px* is accurate.
- **Confidence:** High.
- **What closes it:** Reword to *in a 500 px window*, or measure the check at the box's 200 px minimum and shorten the
  hint to about 22 characters.

### Gates on 1e6c333

| Gate | Result |
|---|---|
| `python3 test_shoalmark.py` (3.14.3) | exit=0 · 243 ok (+4 since `8402732`) |
| `python3 test_core.py` (3.14.3) | exit=0 · 147 ok (+1) |
| `/usr/bin/python3 test_shoalmark.py` (3.9.6) | exit=0 · 243 ok |
| `/usr/bin/python3 test_core.py` (3.9.6) | exit=0 · 147 ok |
| `python3 shoalmark.py --check` | exit=0 — 22 trackers |
| `python3 shoalmark.py --html-only` | exit=0 |
| `python3 -m py_compile` (the three `.py` files) | exit=0 each |
| the tip's tests against the `8402732` tool | `test_shoalmark.py` exit=1, `test_core.py` exit=1 |
| `--vendor` into a fresh scratch 0.17.4 consumer | exit=0; printed only the `## 0.17.5` section; PIN `OK` × 8 |

- **The tip's tests against `8402732`:** every closure check fails there — R1, R4, R5 (FM-022), R6, R10, and the
  `count.id` / `search.help` / `PASSED` string checks.
- **Chrome:** it ran. There is no skip line.
- **CI:** not run on Linux or Windows.

### Verdict on 1e6c333

**NOT READY: R11 (P2).** R12 (P3) is wording.

- **The ten first-pass findings are closed** as ruled. R6 is closed for a 500 px window only.
- **R11 is a regression the R5 closure introduced.** It sits in the function that decides what every pass reads as
  the Owner's intent. The CHANGELOG line the tag would carry is false for it, and the new scaffold invites the edit it
  drops.
- **The fix is small:** about one line and one check, or a lead-in sentence and a reworded CHANGELOG line. Which one
  is the Principal's choice.
- **Verdict mapping:** this pass reads the rubric as *a P2 open means NOT READY*. The first pass gave READY WITH
  FINDINGS with two P2s open, which was the looser reading.

## Verification addendum 2

- **Date:** 2026-09-23, 15:32 CEST (`date`) · **Seat:** Reviewer (`reviewer@seat`) · **Model:** Claude Opus 5.5
- **Tip verified:** `b10456b` — `e83af2d` (R11) and `b10456b` (R12), two commits after `3bf6591`.

### R11 · closed

`owners_intent()` (`shoalmark.py:1545`) compares each paragraph and each line with `INTENT_SCAFFOLD` (`:2883`),
ignoring whitespace. Everything else under the heading is read. I measured it with the tip's `triage_home()` in
scratch repositories.

**Every row of my R11 table is read now:**

| the Owner's line | at the tip |
|---|---|
| his words inside the example's asterisks | read |
| a line in bold alone | read |
| `- **never** *lie*` | read |
| `- **so that** ok` | read |

**Controls:**
- An untouched scaffold gives an intent of `""`, and so do the same file with CRLF line endings and with trailing
  spaces.
- Three real lines are read exactly.
- shoalmark's own `TRIAGE.md` gives exactly the Owner's three intent lines (10–12).
- The consumer's intent is byte-identical to what 0.17.4 read (617 characters), so nothing of an existing consumer is
  lost.
- The new check fails on `1e6c333`.

**The case the Implementer names: an Owner who edits the note or the lead-in.** That text becomes his and is read. In
my runs, fixing one word of the lead-in, or deleting the blank line after it, puts the 353-character lead-in into the
intent. Editing the note puts the 114-character note in. I find that acceptable:
- The failure now runs toward reading the Owner's file too fully, never toward losing a word of his.
- The lead-in says so for itself and the examples: *leaves out only this lead-in and the examples as they stand*.
- It says nothing about the note, which is worded as his to edit.

### R12 · closed

- The placeholder is `search · ~ID` in English (109 px) and `Suche · ~Id` in German (100 px), against the box's CSS
  minimum of 200 px. The check measures exactly that, and it fails on `1e6c333`.
- On the consumer's board at 860 and 900 px windows, where the box was 224 and 264 px, the placeholder fits.
- The title carries the whole help.

### R13 · P3 · Scaffold text that was never written by the Owner can still be read as his intent — formatted, re-wrapped or re-punctuated, and the path's note always

- **What:** The comparison is exact apart from whitespace. So an untouched example, note or lead-in that a tool or an
  editor has changed without changing a word is read as the Owner's intent. I measured these cases with the tip's
  `triage_home()`, starting from an untouched scaffold:

  | change to the untouched scaffold | read as the Owner's intent |
  |---|---|
  | Emphasis written `_…_`, as Prettier's Markdown formatter writes it: the three examples | 365 characters |
  | The same for the note and the lead-in | 461 characters |
  | One example hard-wrapped onto a continuation line | 118 characters, both halves |
  | A typographic apostrophe in *library's* | 131 characters, the whole example |
  | One period added to an example | 117 characters |
  | `*` list markers in place of `-` | 365 characters |

  In each case the village library is printed under *THE INTENT — the Owner's own words … this decides it*. That is
  R5's outcome, reached here without any edit by the Owner. It contradicts *an untouched scaffold is no intent*
  (`CHANGELOG.md:26`), although *recognised by their exact text* (`:25`, `README.md:171`) says how it happens.
- **Also, older than this release:** `path` is still `said()` of the whole section. On shoalmark's own `TRIAGE.md` it
  is the scaffold's note *The Owner's. A pass judges every tier against it; only the Owner changes it.* followed by his
  four path lines (19–22), not the four lines alone. `--triage` prints it that way, and the board shows it that way.
- **Where:** `shoalmark.py:1545` (`owners_intent`), `:2883` (`INTENT_SCAFFOLD`), `:1547` (`path`), `CHANGELOG.md:26`.
- **Cost:** Noise, not loss. The *e.g.* stays visible. It needs a Markdown formatter, a re-wrapping editor or smart
  quotes. Nothing of the Owner's is dropped.
- **Confidence:** High on the mechanism (six cases). How often it happens in practice is unknown.
- **Falsifier:** A formatted but untouched scaffold for which `triage_home()["intent"]` returns `""`.
- **What closes it:**
  - Compare after folding markup and punctuation. For example, compare `re.sub(r"[\W_]+", "", s.casefold())`, and
    compare list items with their continuation lines, not raw lines. A changed word still differs.
  - Give `path` the same treatment, with its note in the scaffold tuple.
  - Or leave it, and say in the CHANGELOG that a formatter's rewrite counts as his.

### Gates on b10456b

| Gate | Result |
|---|---|
| `python3 test_shoalmark.py` (3.14.3) | exit=0 · 244 ok |
| `python3 test_core.py` (3.14.3) | exit=0 · 147 ok |
| `/usr/bin/python3 test_shoalmark.py` (3.9.6) | exit=0 · 244 ok |
| `/usr/bin/python3 test_core.py` (3.9.6) | exit=0 · 147 ok |
| Chrome | ran; no skip line |
| `python3 shoalmark.py --check` | exit=0 — 22 trackers |
| `python3 shoalmark.py --html-only` | exit=0 |
| `python3 -m py_compile` (the three `.py` files) | exit=0 each |
| the tip's `test_shoalmark.py` against the `1e6c333` tool | exit=1 · R11, R12 and R10 fail; R10 because the German lead-in is pinned to the new constant |
| `--vendor` into a fresh scratch copy of the consumer's 0.17.4 pin | exit=0 · printed `(was 0.17.4)` and only `## 0.17.5 — 2026-09-23` · PIN `OK` × 8 · the vendored `shoalmark.py` is byte-identical to the tip |

- The consumer's tree was left untouched: 0 changes.
- CI has not run on Linux or Windows.

### Verdict on b10456b

**READY WITH FINDINGS: R13 (P3).**

- R1–R12 are closed.
- R13 is noise in what a pass reads, never a loss. The tag can carry it if the Principal accepts it, or it can close
  first with the fold-before-compare change.
