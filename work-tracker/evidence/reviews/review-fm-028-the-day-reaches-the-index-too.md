# Review — the --day addendum, at 3ce50e4 (2026-09-25 16:08 CEST, Reviewer, session `8e509911/reviewer-11`)

- **Branch:** `fm/028-the-day-reaches-the-index-too`, tip `3ce50e4` (`3ce50e4f7835563985129639adddf6a4c73f4b4b`). It has
  two commits on `origin/main` `e163ec2` (PR 75's merge, 15:51:47), both by the principal seat (`Session: 8e509911`,
  `Worktree: shoalmark-principal-3`):
  - `99f0ec0` 15:54:03: the addendum row, plus the earlier R1/R2 fixes;
  - `3ce50e4` 16:02:29: the addendum's credit corrected on the Owner's word before the merge.
- **Tier: docs, one pass.** `git diff --name-only origin/main...HEAD` names FM-028 and FM-029, ship-log rows only.
- **Independence:** this seat is a sub-agent of the branch's own session (`8e509911`). `--check` counts it as *same
  session*. Reported.
- **A verdict written for `99f0ec0` was not pushed.** Origin had moved to `3ce50e4`, and the push was refused as not a
  fast-forward. This file is written on the head.

## What I ran

| run | result |
|---|---|
| the Principal's transcript, searched for *FM-028 --day* | the user record (`origin: human`) at `2026-09-25T13:52:59.761Z` = 15:52:59 CEST ✓ |
| its content against FM-028's new row | byte-identical to the italic quotation, 170 bytes; nothing in the record precedes or follows it ✓ |
| **the credit line**, against the Owner's correction | the user record at `14:01:42.692Z` (16:01:42 CEST): *the new FM-028 row credits the Auditor's relay line to the Owner … He pasted it; the Auditor wrote it. Fix the row before merge …: "The Auditor seat's addendum, through the Owner at 15:52:59"*. The row now opens with exactly those words, then *(as pasted):* in place of *(spelling as given)* ✓. It matches the row above, which credits *the Auditor seat's item 2 through the Owner (15:34:27)* ✓ |
| `shoalmark.py` on `origin/main`, lines 5043, 5077 and 5089 | 5043 is `today = datetime.date.today().isoformat()` in `--triage`. 5077 is the same call in the generator. 5089 is `> Generated {today} · …` in INDEX's header ✓ |
| the seat's reading after the quotation | `drift_normalize` (:4273) blanks the Generated date, so *the same tree only under `drift_normalize`* holds ✓. It is the seat's reading, and it follows *— so* unmarked (not graded) |
| 15:34:27 in both rows | the Auditor's item 2, through the Owner, is the user record at 13:34:27.395Z (see the review of `d5507a0`) ✓ |
| FM-029's placement note | *the item named FM-028 for both lines — the seat put this one here, the relation's own tracker* ✓ (the earlier R2) |
| placement and order | FM-028's addendum is appended last in its oldest-first log ✓. The two rows fixed for the earlier R1/R2 are edited in place (R1 below). `3ce50e4` edits the addendum row in place too, but that row is not yet merged: the evening R10's reading, and not graded |
| `--check` · `--session-check` | exit 0 (*87 verdict(s)*; *filing freeze: 20 open*) · exit 0 |
| `python3 shoalmark.py` | the tree is clean after it |
| `git merge-tree --write-tree origin/main HEAD` | clean (tree `4b55563`) |
| `test_shoalmark.py` · `test_core.py` | exit 0, 394 ok · exit 0, 148 ok |
| origin's refs, for the note | `git ls-remote origin`: of the `fm/028` names, only `refs/heads/fm/028-the-day-reaches-the-index-too` exists (now `3ce50e4`). `fm/028-a-pass-replayed-on-a-later-day` is gone. `refs/pull/75/head` is `049554c`, PR 75's merged head. No PR 76 exists (`gh pr list`) |

**Note, for the record and not graded:** no trace of the briefly recreated `fm/028-a-pass-replayed-on-a-later-day`
remains on origin — no branch, and no pull request, and PR 75's head is untouched. GitHub's own event log was not read.

## Findings

**R1 · P3 · confidence high · Two ship-log rows already on `main` are rewritten in place.**
- FM-028's row of the Auditor's item 2 (*15:3x — …* → *15:34:27*) and FM-029's row (the time and the placement note
  added) both merged with PR 75 at 15:51:47. `99f0ec0` edits them where they stand.
- AGENTS.md rule 1: *only the ship log is append-only*. The evening's R10 graded in-place edits of *unmerged* rows P3;
  these rows were merged.
- The edit was invited: my R1 and R2 on `d5507a0` said *15:34:27 in both rows* and *placed here by the Principal seat*,
  words that read as an edit in place.
- No meaning changes: a time is made exact, and a placement is stated. Git keeps both versions.
- **Fix:** none to this text. A merged row is corrected by a correcting row, and this seat will word such fixes that way.

## Verdict

**READY WITH FINDINGS (R1 P3).**
- The addendum is quoted byte for byte at its true time of 15:52:59, and credited as the Owner's correction asks: the
  Auditor seat's, through the Owner.
- Lines 5043, 5077 and 5089 say what the row says.
- The earlier R1 and R2 are closed in substance.
- The gates, the generator and both suites are green, and merge-tree against `origin/main` is clean.
- R1 is fixed forward under the docs tier.

The Owner lands this by merging; a merge rules nothing.

## Verified: the verdict-commit date line, fd5d70c

**Scope.** Branch `fm/028-a-verdict-commit-carries-the-new-date`, tip `fd5d70c` (`fd5d70cecdb33919c48e03f7215ed67bd11aeae2`),
one commit by the principal seat (`Session: 8e509911`, `Worktree: shoalmark-principal`) at 00:47:31 CEST. Its parent is
`87ee09e`, today's `origin/main` (PR 81). The brief named `0d60d55`; that is an ancestor, and PR 81 merged after it. The
commit adds a paragraph before FM-028's Ship log and a ship-log row, both filing the cold session's RV-577 from the
parent project's PR 855. **Tier: docs, one pass.** **Independence:** same session. This seat is `8e509911/reviewer-18`,
a sub-agent of the branch's own session, and that is reported here. Verified 00:49–01:15 CEST on 2026-09-26, inside
the window FM-028 is about.

| run | result |
|---|---|
| `lefthook.yml:8-10`, the pre-commit `tracker-index` hook | `written=$(python3 shoalmark.py --print-written) && printf … \| git add --pathspec-from-file=-`: it regenerates, then stages what the generator names ✓ |
| `shoalmark.py:5605` and `:5617`; `:5654-5658` | `today = datetime.date.today().isoformat()` (the **local** calendar) → `> Generated {today} · …`; under `--print-written` INDEX.md is always printed, so it is always staged ✓ |
| `python3 shoalmark.py` on a scratchpad clone at `fd5d70c` (signers file set) | local zone: no diff. `TZ=UTC`: one line, `> Generated 2026-09-26` → `2026-09-25`, and nothing else ✓ |
| `drift_normalize`, `shoalmark.py:4774` (`GENERATED_RE`, :4771), used by `--check` at :5630 | that clone, INDEX.md's date alone changed: `--check` exit 0, *INDEX.md is up to date*. **Positive control:** the tracker count changed instead: exit 3, *STALE* ✓ |
| does the hook run on a verdict commit at all? scratch clone, `lefthook install`, a commit staging one review file only, under `TZ=UTC` | lefthook 2.1.4: `tests (skip) no matching staged files`, `✔️ tracker-index`. The commit (`e3c9210`, scratch only) carries `work-tracker/INDEX.md \| 2 +-`, the date line alone. `glob: "work-tracker/*.md"` matches `work-tracker/evidence/reviews/*.md` ✓ |
| the source: the parent's RV-577 (`review-feat-190-the-queue-rule-in-the-output-styles-cold.md:170`, on PR 855's head `feat/190-a-pull-requests-state-is-queue-output-from-the-same-turn`; `gh pr view 855`: that head, merged) | the verdict commit `242b701d`, 00:43 CEST, carries `docs/work-tracker/INDEX.md \| 2 +-`: *Generated 2026-09-25* → *2026-09-26* only ✓. The paragraph's 00:44 is the relay's minute, not the commit's (not graded) |
| the parent's `scripts/review_gate.py` at `f1b10dfb`, read and not run | `beyond` (:313) is every file not matching `review_re` (:266, `evidence/(…/)?review*.md`), and INDEX.md is not exempt. The finding at :363-367, *a verdict and what follows it change only review files*. The tip line at :370, *all the verdict's own review files*, or *N it does not cover*. The finding does not depend on the verdict word, so *would fail a READY verdict the same way* ✓ |
| *the parent's wrapper has the same hook* | parent `lefthook.yml:38-41`: `tracker-index`, `glob: "{docs/work-tracker/*.md,…}"`, `gen-tracker-index.py --print-written` piped to `git add` ✓ |
| two remedies, none chosen; the release | (a) the hook leaves the date alone on a commit that did not touch the trackers; (b) the review gate reads a date-only INDEX.md change as no change. Neither is chosen ✓. *For 0.18.4 or the release after* ✓. See R4 on (a)'s wording |
| the ship-log row | it matches the paragraph: RV-577, the Owner's cold session, PR 855, 00:44, the hook and the gate ✓. See R3 on its place |
| front matter | the only hunk starts at line 117; lines 1–11 untouched, `triaged: 2026-09-25` stands ✓ |
| `git diff --name-only origin/main...HEAD` | FM-028 and `work-tracker/INDEX.md`. INDEX.md's change is **its date alone** (`2026-09-25` → `2026-09-26`), written by the hook into `fd5d70c` at 00:47 |
| `--check` · `--session-check` | exit 0 (*up to date — 37 trackers*; *judged before build: on*; *filing freeze: 21 open …*) · exit 0 |
| `python3 shoalmark.py`, local zone | exit 0, the tree clean: INDEX.md is the generator's own output |
| both suites, as the hook runs them, at 00:56 CEST | **local: `test_shoalmark.py` exit 1 on 3.14.3 and 3.9.6**, 437 ok and one FAIL, *rendered: the board's first words are the answer …*. That is FM-028's own known failure, and this branch changes no code. `test_core.py`: exit 0, 148 ok. **Under `TZ=UTC`, at 01:05:** exit 0 on both interpreters, 438 ok and 148 ok |
| `git merge-tree --write-tree origin/main HEAD` | exit 0, clean (tree `f786682`); `origin/main` is an ancestor of the tip |

**Evidence for the line, and not a finding.**
- `fd5d70c` is itself a date-only INDEX.md commit. It touched a tracker's body, so the hook did what it should. Under
  RV-577's content-keyed remedy it would have carried nothing (R4).
- The generator dates by the local calendar, so FM-028's own workaround moves the date **backwards**. Between 00:00
  and 02:00 CEST, a commit made under `TZ=UTC` writes yesterday's date over today's. The scratch probe `e3c9210` shows
  it: a review-only commit staged `2026-09-26` → `2026-09-25`. A seat that needs `TZ=UTC` for the suite hands its
  verdict commit exactly the change the line describes.
- **This verdict commit carries no INDEX.md change.** `fd5d70c` had already written today's date, and I committed in
  the local zone: a review-only commit skips the suite, so `TZ=UTC` was not needed. Had I committed under `TZ=UTC`, it
  would have carried `2026-09-25` (the probe above). The date line reached the first commit of the day, `fd5d70c`,
  which is a tracker commit, and so did not reach this one.

**R2 · P3 · confidence high · *The `--day` line above* points the wrong way.**
- The only `--day` lines in FM-028 are the two 2026-09-25 ship-log rows (lines 135–136). They are **below** the new
  paragraph, and nothing above it names `--day`.
- **Fix, forward:** *(the `--day` rows in the Ship log below)*.

**R3 · P3 · confidence high · The new row opens a log that runs oldest first.**
- FM-028's log runs 09-24, 09-24, 09-25, 09-25, and the review above calls it *its oldest-first log*. The 09-26 row is
  placed first.
- The house is mixed (FM-008 and FM-011 run newest first), but this file has one order.
- **Fix:** move it last before the merge. After the merge, leave it: moving a merged row is an in-place edit (R1).

**R4 · P3 · confidence medium · Remedy (a) is narrower than its source, and (b) is not this repository's.**
- RV-577's own words: *either the generator leaves the date line alone when nothing else in the INDEX changes, or the
  gate reads a generated INDEX that differs only in that line as an addendum*.
- The filing's (a) is keyed on the commit (*a commit that did not touch the trackers*); RV-577's is keyed on the
  content. They part on a body-only tracker commit such as `fd5d70c`: the date change stays under the first and goes
  under the second. Neither choice is wrong, but the paraphrase changes the proposal.
- (b) lives in the parent's `scripts/review_gate.py`. Shoalmark has no review gate (`shoalmark.py:1288`: *as the
  parent project's review gate reads it*), so *For 0.18.4* can carry (a) only.
- **For the builder, not a remedy proposed here:** the hook fires on a review-only commit because lefthook's `*`
  crosses `/` (the probe above).
- **Fix, forward:** at the next touch of FM-028, quote RV-577's two remedies and say that (b) is the parent's.

**R5 · P3 · confidence high · Form.**
- There is a double blank line before the paragraph (lines 119–120).
- The paragraph's lines run 147–156 characters, where the file wraps at about 120.
- **Fix, forward:** with R2.

## Verdict on fd5d70c — READY WITH FINDINGS (R2–R5 P3), 90%

**`fd5d70cecdb33919c48e03f7215ed67bd11aeae2`: READY WITH FINDINGS.**
- Every claim in the paragraph holds against the tool:
  - the hook regenerates and stages INDEX.md through `--print-written`;
  - the header carries a local-calendar *Generated* date;
  - `drift_normalize` reads a date-only change as none for `--check`, with a positive control;
  - the parent's gate refuses a verdict commit that carries it, and its hook is the same.
- The row matches the paragraph. No front-matter key changed.
- The gates, the generator and merge-tree are green. The suite fails locally at 00:56 only on FM-028's own known check,
  and passes under `TZ=UTC`.
- R2–R5 are P3, fixed forward under the docs tier; R3 is best done before the merge.
- Tier docs, one pass; same session, `8e509911`'s own sub-agent, reported.

*the Owner lands this by merging; a merge rules nothing.*

## Verified again on c43f694

**Scope.** `c43f694` (`c43f6944d01cff11eaef2b926a83c11533f36ec6`), one commit on this verdict's `09ac4dc`, by the
principal seat (`Session: 8e509911`, `Worktree: shoalmark-principal`) at 01:17:37 CEST. It fixes R2–R5. Same tier,
docs, one pass; same session, `8e509911/reviewer-18`, reported. Verified 01:18–01:37 CEST.

| run | result |
|---|---|
| `git diff --stat 09ac4dc c43f694` | the FM-028 tracker only, 10 insertions and 8 deletions. **The hook did not touch INDEX.md again**: `git diff fd5d70c c43f694 -- work-tracker/INDEX.md` is empty, because INDEX.md already carried *Generated 2026-09-26* from `fd5d70c`, and this commit was made in the local zone |
| `git diff --name-only origin/main...HEAD` | FM-028, INDEX.md (the date alone, from `fd5d70c`) and this review file |
| R2 | *(the `--day` rows below)*. The `--day` rows are the two 2026-09-25 ship-log rows, and they are below ✓ |
| R3 | the 2026-09-26 row is now last, after the two 09-25 rows, so the log runs oldest first ✓. The moved row is byte-identical to the one removed; the diff's `-` and `+` lines are one text. It was not yet merged, so the move is not an in-place edit of a merged row ✓ |
| R4 | (a) *the hook leaves INDEX.md's date alone when only the date would change — keyed on the INDEX content, as RV-577 is*, which is RV-577's key ✓. (b) *the parent's `review_gate.py`, not this tool, reads a date-only INDEX.md change as no change* ✓. *Two remedies, neither chosen here* ✓. *For 0.18.4 or the release after* and *the parent's wrapper has the same hook* stand ✓ |
| R5 | the double blank line is gone. Counted in characters, the paragraph's lines (120–128) are 110–118 wide; `awk` counts bytes, so it reads the em-dash lines as 120 ✓ |
| front matter | untouched: the hunk starts at line 117 ✓ |
| `--check` · `--session-check` | exit 0 (*up to date — 37 trackers*; *101 verdict(s)*; *judged before build: on*; *filing freeze: 21 open …*) · exit 0 |
| `python3 shoalmark.py`, local zone | exit 0, the tree clean |
| both suites, as the hook runs them, from 01:19:43 CEST | **local: `test_shoalmark.py` exit 1 on 3.14.3 and 3.9.6**, 437 ok and one FAIL, *rendered: the board's first words are the answer …*, which is FM-028's own known failure (no code changed). `test_core.py` exit 0, 148 ok. **Under `TZ=UTC`:** exit 0 on both interpreters, 438 ok and 148 ok |
| `git merge-tree --write-tree origin/main HEAD` | exit 0, clean (tree `0959bb9`); `origin/main` `87ee09e` is an ancestor of the tip |

**The findings on fd5d70c:**
- **R2 ✓ closed.**
- **R3 ✓ closed**, before the merge as asked.
- **R4 ✓ closed.** (a) now keys on the INDEX content, as RV-577 does, and (b) is placed in the parent's gate.
- **R5 ✓ closed.**

No new finding.

**This verdict commit carries no INDEX.md change either**: it is a review-only commit in the local zone, on a tree
already dated today. See the commit's `--stat`.

## Verdict on c43f694 — READY, 92%

- R2–R5 are closed as worded.
- The diff since `09ac4dc` is the FM-028 tracker alone, and the hook did not touch INDEX.md's date again.
- `--check` and `--session-check` are 0, the generator leaves the tree clean, and merge-tree is clean.
- The suite fails locally only on FM-028's own known check, between 00:00 and 02:00 CEST, and passes under `TZ=UTC`.
- Tier docs, one pass; same session, `8e509911`'s own sub-agent, reported.

*the Owner lands this by merging; a merge rules nothing.*

**`c43f6944d01cff11eaef2b926a83c11533f36ec6`: READY.**
