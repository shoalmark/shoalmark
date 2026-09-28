# Review — the pass of the night's filings, at c730621 (2026-09-28 07:45 CEST, Reviewer, session `8e509911/reviewer-45`)

- **Branch:** `tracker/triage-2026-09-28-the-nights-filings`, tip `c730621` (`c730621b0c4bc45a0984fd2c073c5ca43eb148b9`,
  confirmed by `git ls-remote` at 07:44). It sits on `origin/main` `aff1bfb` and carries four commits, all the
  Principal's (`principal@seat`, `Session: 8e509911`, `Worktree: shoalmark-principal-4`):
  - `eda5e61`, 06:53:54 — `--clear-ask FM-032 build`;
  - `2db6f07`, 07:00:17 — the pass;
  - `2c9f5dd`, 07:04:02 — FM-032's quote and durations;
  - `c730621`, 07:25:31 — the five P3s the interrupted seat found, closed in the text.
- **Tier: docs, one pass.** `git diff origin/main c730621 -- shoalmark.py test_*.py lefthook.yml scripts/` is empty.
  The tool, both suites and the hook are main's, so no suite was run.
- **Resumed.** The seat before me in this worktree, `8e509911/reviewer-40`, lost access at 07:08 and left a draft on
  `2c9f5dd`. I take what it verified as my notes and did not re-run it: the clear-ask re-run byte-identical to
  `eda5e61`, `--triage` re-applying `2db6f07`'s worksheet, rank #4 free, the durations. I checked again anything
  that was cheap to check.
- **Independence:** same session — a sub-agent of 8e509911, reported.
- **Verdict: READY WITH FINDINGS.** There are two P3s, RV-720 and RV-721, from the range the Principal allocated.

## What I ran

| run | result |
|---|---|
| the scratch copy | A clone from GitHub under this session's scratch folder, with its own git dir, at `c730621`. I did not use `cp -R`: copying the worktree would copy its `.git` pointer into the shared git dir. `--triage`, `--owner`, `--html-only` and `--queue` ran there. `--check` and `--session-check` are read-only and ran here |
| `--check` on `c730621` | exit 0. *INDEX.md is up to date — 40 trackers*; *judged before build: on — 4 commit(s) … every build commit under a judged In Progress tracker*; *the Owner's two sections: guarded — … none changes them or his signers file*; *filing freeze: 21 open, at or above 8 — only bug filings* |
| `--session-check` | exit 0 |
| `git merge-tree --write-tree origin/main c730621` | clean (`3961f0c`) |
| `git diff --check origin/main c730621` | clean |
| `--queue` (in the scratch clone) | `branch tracker/triage-2026-09-28-the-n… @ c730621  wait: no pull request — no verdict on c730621`, and *1 waiting on you: 0 merge, 0 close, 0 wait, 1 pushed without a pull request*. The forge has no open pull request |
| `--owner` (in the scratch clone) | *3 NEED THE OWNER*: FM-024 · ruling, FM-027 · ruling, FM-032 · ruling, each asked 0 days ago. ACTS lists FM-006 and FM-007 only, so FM-032's path-3 act has left his list |
| `--html-only` (in the scratch clone) | `work-tracker/index.html` carries all three asks, each with kind `ruling`, since `2026-09-28`, its three options and its proposal |
| the asks against `--schema` | Measured with the tool's own `len` (`ASK_OPTION_MAX` 120, `ASK_MAX` 300). FM-024's ask is 123 characters and its options 104 · 75 · 90. FM-027's ask is 98 and its options 120 · 117 · 72. FM-032's ask is 110 and its options 119 · 114 · 105. In all three, `ask-proposal:` is option 1, as the schema requires (*"With `ask-options:` it must be one of them"*) |
| the RV grep, both forges | RV-720…729 appear nowhere. **shoalmark:** 114 refs after my fetch, their files and their commit messages. **PortDive:** read-only, no fetch. I read its 26 refs updated since 2026-09-27, plus the forge's two branch tips (`main` `60e6d1a7`, `e41a39a1`), which are present locally; `git ls-remote` found no forge tip missing here. The positive controls hit: RV-694 on shoalmark, RV-740 on PortDive. PortDive's RV-7xx ids are 700–711, 740 and 760 |

## The five closures on `c730621`

1. **TRIAGE.md's paragraph — closed (confidence 95 %).**
   - FM-040's body on main (line 58) times the relay *"relayed by the Owner 2026-09-28 05:24:00"*, and the paragraph
     now says 05:24:00. Nothing reads 05:40 any more.
   - *Filed 01:52* is `bbe192c` (01:52:44). *The measurement filed 05:28, PR 106* is `ed0768a` (05:28:02), merged by
     `aff1bfb` as PR 106. *His words of 01:42:26* is FM-040's line 17.
   - The worksheet `work-tracker/evidence/triage/triage-2026-09-28.md` is named in the paragraph.
   - The RV-679 clause now reads *"an act branch — `--done`, `--due` — once a Reviewer's verdict sits on it"*,
     which matches the code (closure 2).
2. **FM-031's RV-679 line — closed; true as written against the code (confidence 90 %).** The tool is byte-identical
   to main's.
   - `answered_at` looks for an answer commit with `git log -1 -G '^answer:' <head> ^<base> -- <tracker dir>`. It
     returns that commit only where `addenda_only` holds from it to the head; otherwise it returns the head.
   - `done_cmd` writes only `done:` (and `next: build` after an action's yes) plus a record under `## Acts`.
     `due_cmd` writes `due:` and drops `done:`. Neither touches an `answer:` line. So on an act branch with a verdict
     on top, the head is read, and `answer_reading` finds `reviewer@seat` and says *wait: not an answerer*.
   - An `--answer` commit writes `answer:` (line 1575), so it is found, and a verdict above it counts as an addendum.
   - `answered_at` first shipped in `62682c8`, and `git tag --contains` names `v0.18.4` first, so *since 0.18.4* holds.
   - The time in the same line is RV-720.
3. **FM-032's path-3 act and his quote — closed (confidence 90 %).**
   - The commit: `git show -s --format='%h %ci %G? %s' fe36cc0` prints `fe36cc0 2026-09-25 11:14:26 +0200 G
     work-tracker(TRIAGE): Updates after parley with Consigliere`, authored by holgo99.
   - It rewrites path 3 in TRIAGE.md and INDEX.md, adding *"a review of the Owner's own answers and TRIAGE lines
     reports and never blocks, until FM-007's hardware key signs them"*. That is the exception for his answer pull
     requests. Path 3 has not changed since: `ad9bf67` changed path 6 only.
   - The answer `97fa87a` is 2026-09-24 21:32:35, G. The ask was kind action, as the ship log says.
   - The record claims only that the exception was written and that the act's result is that commit, and both hold.
     Path 3's wording differs from the accepted option's (*"one Reviewer docs pass … the signature alone after"*),
     but the record does not claim they are the same.
   - **The quote:** I compared the words of his text (after *Question:*) with the words of the quote. There are 57
     each, in the same order, and one differs: *rationle* → *rationale*, a spelling. Everything else is punctuation:
     the dash after the first clause is a comma, the comma before *that* is gone, *run.* is *run?*, commas are added
     after *graded* and *then* and before *decided*, *forward fix* is hyphenated and *confidence-score* is not. The
     backticks around *READY WITH FINDINGS* and *no-fix* are dropped; I count those as typographic marks. The mark
     *"his two sentences after Question:; spelling and punctuation normalised, no word dropped or added"* is true.
4. **FM-024's paste — closed (confidence 95 %).**
   - The new line beside the paste gives the paste's own *≈06:55 CEST* as its writer's estimate and the relay's
     stamp as 06:48:37.
   - Two things corroborate it. The saved copy's mtime is 06:49:50, before 06:55. PortDive `d0c8c47f` (06:51:32)
     reads *"row 56 — his question timed 06:48:37"*.
   - The quoted blocks are unchanged. With `> ` removed they are byte-equal to the saved copies: FM-024's 8 lines are
     `88db73af…1c20` and FM-032's 13 lines are `06ea1596…5749`, both the hashes cited.
5. **FM-027's raise line — closed for the line (confidence 90 %). The worksheet row it feeds is RV-721.**
   - The line is in the tool's form: `- 2026-09-28 · Principal seat (8e509911), … · <fact> · source: … · … ·
     undermines: no signed rule (none names review ids)`.
   - Importing the tool in the scratch clone, `raise_lines` reads date `2026-09-28` and undermines `['no signed rule
     (none names review ids)']`.
   - `mark_raised` gives `[]`, `owed_a_pass` is False and `board` says `backlog`. The positive control, the same
     raise naming `path 3` on a tracker triaged 2026-09-24, gives True.
   - `--triage` on the scratch copy prints *"A triage pass — 0 trackers to judge"* and *"Applied nothing — no new
     filled rows"*, and the tree is unchanged. It lists no row as RAISED and applies nothing more.

## Findings

**RV-720 · P3 · confidence 85 % — FM-031's RV-679 line gives a time that is neither the act's nor the verdict's.**
The line reads *"on the Owner's own `--done BUG-327` act (PortDive `answer/bug-327`, 2026-09-27 20:52:39)"*.
- His act is `c502c7a4`, 20:21:18 (G). The Reviewer's verdict on it is `66884f5f`, 20:45:02.
- PR 866's forge timeline has exactly those two commits and then the merge (23:33:35Z). Nothing happened at 20:52:39.
- 20:52:39 is when the Principal's own `--queue` run read *wait: not an answerer (reviewer@seat)*. A Principal brief
  in this session's scratch folder (`brief-ledger-commit-25-draft.md`) records that run; it is not in the record.

As written, the line dates the act half an hour late.

**Fix forward:** *"(PortDive `answer/bug-327`: his act `c502c7a4` 20:21:18, the verdict `66884f5f` 20:45:02; `--queue`
read it so at 20:52:39)"*.

**RV-721 · P3 · confidence 75 % — the worksheet marks FM-027 RAISED, a mark the tool gives only to a raise that names a
signed rule.**
- FM-027's row in `triage-2026-09-28.md` has *"2026-09-28 · keep · RAISED (Parked since 2026-09-24; the raise of
  2026-09-28 under ## Raised)"* in its generated *keep test* cell.
- The worksheet defines the mark: *"a row marked RAISED carries a raise … naming a signed rule it undermines"*.
- The raise line now says *"undermines: no signed rule"*. `mark_raised` gives `[]`, and `--triage` finds 0 trackers
  to judge.
- FM-027 is Parked and owed no pass, so the row was added by hand, and the row does not say so.

`c730621` fixed the raise line and left the worksheet row as it was. That row was half of the interrupted seat's
candidate.

**Fix forward:** make the cell read *"2026-09-28 · keep · by hand — Parked since 2026-09-24, owed no pass; the raise of
2026-09-28 under ## Raised names no signed rule"*.

**Notes, not findings:**
- In FM-027's raise, *"The same evening"* covers 02:22 to about 06:20.
- The two times 02:00:26 and 02:06:06 now sit in the parenthetical about the briefs, although they are the two verdict
  commits (`e7d16b8`, `97fa9ada`). The *source:* field names those commits.

## Verdict

**READY WITH FINDINGS.** RV-720 and RV-721 are P3, to be fixed forward. The docs tier takes no re-pass.

The Owner lands this by merging; a merge rules nothing.
