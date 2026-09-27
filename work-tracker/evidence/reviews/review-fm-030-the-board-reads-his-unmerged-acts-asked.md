# Review — FM-030's ask on the board, at 03877b2 (2026-09-27 14:25 CEST, Reviewer, session `8e509911/reviewer-39`)

- **Branch:** `fm/030-the-board-reads-his-unmerged-acts-asked`, tip `03877b2` (`03877b21f093892d5b680f209c8d529a778544b8`),
  one commit on `origin/main` `28e54bf` (PR 98's merge), by the Principal seat (`principal@seat`, `Session: 8e509911`,
  `Worktree: shoalmark-principal-4`), authored and committed 14:14:18. The brief's 14:14:36 is not the commit's time
  (the push, most likely); either way it is after the ledger row (below).
- **Tier: docs, one pass.** `git diff --stat origin/main..HEAD` names two paths: FM-030 (+10 −1) and INDEX (one row).
  No `.py`, test, configuration or hook changed, so no suite was run.
- **Independence:** this seat is a sub-agent of the branch's own session (`8e509911`). `--check` counts it as *same
  session*. Reported, not refused.
- **Verdict: READY WITH FINDINGS.** No P2. Four P3, carried forward.

## What I ran

| run | result |
|---|---|
| `git diff origin/main..HEAD`, front matter | exactly `next: build` → `next: owner` and five added lines: `ask:`, `ask-kind: ruling`, `ask-since: 2026-09-27`, `ask-options:` (three), `ask-proposal:`. No other key changes |
| the same diff, body | one paragraph under *What is true now* (*The ask of 2026-09-27 …*), two bullets under `## Raised` (13:57:50, 14:09:46) |
| INDEX.md | FM-030's row: Next `build` → `owner`, Kind `—` → `*complicated*`, Needs `intended, kind` → `intended`. It is the generated row: `--check` says INDEX is up to date |
| the ask's shape, measured | `ask:` 91 characters, one `?`, at the end. Options 119 · 81 · 26 characters, at most 120. None opens with yes or no. `ask-proposal:` equals option 1 byte for byte, and neither of the others |
| who set `next: owner` | `03877b2`, author `Principal seat <principal@seat>`, the seat `[seats]` names `principal` |
| `python3 shoalmark.py --check` | exit 0; *INDEX.md is up to date — 39 trackers*; no line on FM-030 |
| `python3 shoalmark.py --session-check` | exit 0 |
| `python3 shoalmark.py --owner` | *1 NEED THE OWNER*: *FM-030 · ruling · asked 0 day(s) ago*, the ask word for word |
| the board (`work-tracker/index.html`, rebuilt by the checkout hook, git-ignored) | FM-030's row: `next` owner, answer empty, problems none, three options, the proposal among them; the *waiting for you* filter (open, `next` owner, no answer, no problems) selects FM-030 and nothing else |
| positive control, scratch copy (`git archive` of the tip, a fresh repository): option 1 and the proposal lengthened to 121 characters, `--check` | the lint line *`ask-options:` — 'the board reads git: …' is 121 characters; a choice is at most 120*. The gate reads the shape |
| positive control, the same copy at its base commit (author not a seat) | `--check` 4: *`next: owner` puts a question in front of the Owner — `scratch@…` is not a seat*. The provenance rule runs; on the branch it passes |
| PortDive ledger, `git -C …/worktrees/principal-2 show 71a06fbe:docs/work-tracker/evidence/FEAT-190/asks.md` (fetched, read-only) | row 51 = the *New asks* table's last row, FM-030, 2026-09-27. `71a06fbe` authored and committed 14:12:51, on `origin/feat/190-day-six-the-ask-on-fm-030-the-board-reads-his-unmerged-acts` |
| the Principal's transcript (`8e509911…jsonl`), the user records at 11:57:50.602Z and 12:09:46.271Z, read alone | the Owner's two messages, 13:57:50 and 14:09:46 CEST, and the screenshot path *Screenshot 2026-09-27 at 13.45.18.png* |
| that screenshot | FM-024's act line with *no date yet*, **done** and **reschedule**, as the raise says |
| `git show -s f8246fae` | 13:44:51, `holgo99`, `G`, on `origin/answer/fm-024`, not on `origin/main`. The screenshot is 27 s later |
| `git merge-tree --write-tree origin/main HEAD` | clean (`f09c55e`) |
| `git merge-tree --write-tree 5e6d816 HEAD` — `fm/030-the-done-dialog-shows-the-question`, its tip from `git ls-remote` | **CONFLICT (content) in FM-030** (R2) |
| a scratch copy, FM-030's raise rewritten to `· undermines: path 6`, the board rebuilt | FM-030's section `progress` → `triage` (R1) |

## The checks

**1. The ask's shape ✓. Confidence high.** One sentence and one question. Each option is a phrase, not a yes or no,
and at most 120 characters (option 1 is 119). The proposal is option 1 byte for byte. `next:` was set by the Principal.
`--check` 0, and both positive controls show the gate reads length and provenance.

**2. The Owner's words: they agree with the transcript. The ledger row came first. Confidence high.**
- **14:09:46.** Transcript: *Option \`1\` is the only valid one and holds to the single-source of truth. Go, file the ask
  on FM-030 with option 1 as proposed.* Row 51 quotes it byte for byte and marks it *(verbatim)*. The tracker drops the
  backticks and the hyphen and marks it *(spelling normalised)*. They agree.
- **13:57:50.** Row 51 does **not** quote these words. It paraphrases only his two ways forward. So I checked the
  tracker's quote against the transcript itself. *Dasboards* → *dashboard's*, *was is* → *is*, *consitent* →
  *consistent*, *want care* → *won't care*. The ellipsis stands for *Users "could" think … See: [Image #96]*. The meaning
  is his, and the change is marked. Two small cuts are not marked (R4).
- **His two ways forward.** The tracker has *verify by sha that the act answered is the one on the pushed branch before
  marking it, and keep a button to answer again or revoke*. Row 51 has *check by the shas that the command's branch was
  pushed before a row is marked answered*. His text asks for both: that request was the one answered, **and** the
  branch was pushed. Each is a fair half, and both are paraphrases, not quotes.
- **Order.** The ledger row `71a06fbe` is 14:12:51. The ask commit is 14:14:18, 1 min 27 s later. The row came first.

**3. The options against row 51 ✓. Confidence high.**
- The ask's sentence and the kind (ruling) are identical.
- Options 2 and 3 are byte-identical.
- Option 1 is the row's long form cut to 119 characters: *every `origin/answer/*` branch not merged into main whose
  tracker tip carries a `done:` or `answer:` that main lacks renders the row as done, on its way*. The details the cut
  drops (branch, sha, push time; the buttons replaced by *revoke*) are in the design paragraph.
- The proposal, *the first*, is option 1.

**4. The design paragraph ✓, with one imprecision (R4).** Its claims check out. The board is rebuilt from `main` by
the checkout hook. The act is on `answer/fm-024` until his merge (`f8246fae`, not on main). Option 3 is against path
line 5.

## Findings

**R1 — P3 · the raise names line 6 in a form the tool does not read, so the raise rule does not fire.**
`raise_lines` keys on `\bundermines:`. The 13:57:50 bullet says `· undermines line 6: the button's result …`, and the
tool's own parser returns `undermines: []` for it and for the 14:09:46 bullet. `mark_raised` then sees no raise on a
signed rule. FM-030 (`triaged: 2026-09-25`) stays under *progress*, where the Owner's raise rule (FM-033's answer,
`9e48ee8`) puts a tracker under *triage* the same day. In a scratch copy, the tool's form (below) moves FM-030 from
`progress` to `triage` on the board.

*Cure:* end the bullet `… · the button's result is not on his board after the press · undermines: path 6`. The
alternative is that the Principal rules the same-day pass not owed, and says so. The build branch's two new bullets
(`5e6d816`) use the same `undermines line 6` form. They are outside this review, and the same cure applies.

**R2 — P3 · FM-030 conflicts with the build branch.** `fm/030-the-done-dialog-shows-the-question` at `5e6d816` (the
Principal, 13:40:30, an Implementer on it) adds two bullets under `## Raised`, after the second 2026-09-25 raise. This
branch adds its two bullets at the same place, so `git merge-tree` reports a content conflict in FM-030. Nothing else
conflicts.

*Cure:* whichever merges second keeps both blocks, in time order: 13:35:40, the E0 counter's line (dated
2026-09-27), 13:57:50, 14:09:46. The front matter does not conflict, and `next: owner` survives the merge. The build
gate (`judge_commits`) keys on `triaged:` and `In Progress`, not on `next:`, so the Implementer's commits under FM-030
are not refused by it.

**R3 — P3 · no ship-log row for the ask, and the 14:09:46 bullet is not a raise.** The last three asks the Principal
filed each wrote a ship-log row: FM-006 (`4899353`, *Asked: …*), FM-007 (`3e0893b`) and FM-002 (`4527ca1`). This one
writes none. `## Raised` reads *one sourced line per raise*, but the 14:09:46 bullet is his go-ahead to file the ask.
It names no fact against a rule.

*Cure:* one ship-log row, *2026-09-27 | Asked: how the board shows an act or answer he just gave before his merge —
a ruling, the proposal option 1, on his words of 13:57:50 and 14:09:46; ledger row 51 first (71a06fbe, 14:12:51)*.
Whether the 14:09:46 bullet moves there is the Principal's call.

**R4 — P3 · two small precision points.**
- (a) The 13:57:50 quote cuts *into \`main\`* after *not yet merged* and *after the act* at its end, and renders
  *shows consistent* as *is consistent*. The only marks are *(spelling normalised)* and the one ellipsis. The meaning
  is intact, so this is not a misquote.
- (b) The paragraph's *`--done`/`--answer` end on `main`* holds only when he starts on `main`. The tool puts him back
  on the branch he started on (*back on `…`*), and the board's *Where* line tells him to run it *on the branch that
  carries the ask*.

## Not checked

- The `--queue` tail of `--owner`, which needs `gh`.
- The suites: no `.py` changed.
- `71a06fbe`'s own review, which is PortDive's Reviewer's (`72e0b5f8`, READY WITH FINDINGS).

The Owner lands this by merging. A merge rules nothing: his signed answer through the board rules the ask.
