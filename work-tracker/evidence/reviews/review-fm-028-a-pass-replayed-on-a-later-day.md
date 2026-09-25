# Review — two lines for 0.18.4, at d5507a0 (2026-09-25 15:46 CEST, Reviewer, session `8e509911/reviewer-11`)

- **Branch:** `fm/028-a-pass-replayed-on-a-later-day`, tip `d5507a0` (`d5507a082b164d3f67ed5585631fc7e60a1ab8a2`). It is one
  commit by the principal seat (`Session: 8e509911`, `Worktree: shoalmark-principal-3`, 15:38:32), stacked on `9899363`,
  the FM-030 branch's last verdict. PR 74 has since merged that verdict into `origin/main` (`44f908b`), so only the new
  commit is reviewed.
- **Tier: docs, one pass.** `git diff --name-only origin/main...HEAD` names two paths: FM-028 and FM-029. Each gains one
  ship-log row. No front matter changes, and there is no code, test, configuration or hook.
- **Independence:** this seat is a sub-agent of the branch's own session (`8e509911`). `--check` counts it as *same
  session*. Reported.

## What I ran

| run | result |
|---|---|
| the Principal's transcript, searched for *Auditor → Principal, through the Owner* | the user record (`origin: human`) at `2026-09-25T13:34:27.395Z` (15:34:27 CEST). It has three items; item 2 is read here |
| item 2 against the two rows | FM-028: *a pass cannot be replayed on a later day — --triage reads the machine's date only (shoalmark.py:5043) — proposed: an explicit day for --triage and a suite case replaying a pass the next day*. Then: *plus one real-history relation case for FM-032's pre-0.18.1 record (ffa63b8 → accepted the proposal). FM-007's double answer is already in the suite (test_shoalmark.py:3260–3270).* Both rows carry it faithfully (R2 on where the second half went) |
| `shoalmark.py:5043` | `today = datetime.date.today().isoformat()` inside `--triage`. The sheet's name and every date it applies come from that line, and the command has no flag to override it ✓ |
| `test_shoalmark.py:3260–3270` | exactly FM-007's case: the comment *answered twice, word for word, on 09-22 — `63e72b4` … `7521116`*, then the check *FM-007's real double answer … reads relation not computable* ✓ |
| `ffa63b8` | 2026-09-24 11:07:43 `G`, holgo99, *FM-032: accepted - all four now* ✓ |
| FM-032's `## Asks` record, read by 0.18.3 (`recover_relations`) | the record alone reads *relation not computable*; recovered from the commit, it is `('accepted the proposal', 'ffa63b8')` ✓. No check in the suite names `ffa63b8` yet, which is what the line asks for ✓ |
| order | FM-028's ship log is oldest first, and the row is appended last ✓. FM-029's is newest first, and the row is inserted first, above *2026-09-25 06:52 CEST* ✓. No row is edited |
| `--check` · `--session-check` | exit 0 (*86 verdict(s)*; *filing freeze: 20 open*) · exit 0 |
| `python3 shoalmark.py` | the tree is clean after it |
| `git merge-tree --write-tree` | clean against `origin/main` and against `9899363` (the FM-030 branch, now merged and deleted on origin); tree `8fe9b14` |
| `origin/fm/035-ci-green-on-every-platform` (`4e4d63b`) | conflicts in INDEX.md and TRIAGE.md, exactly as it does against `origin/main`. This commit adds no conflict |
| `test_shoalmark.py` · `test_core.py` | exit 0, 394 ok · exit 0, 148 ok |

## Findings

**R1 · P3 · confidence high · The relay's time is approximated in one row and missing from the other.**
- FM-028 reads *(15:3x — the relay's time is in the parent project's ledger)*. FM-029's row carries no time.
- The Owner's paste is the transcript's user record at 13:34:27.395Z, which is **15:34:27 CEST**.
- By today's grading this is not acceptable as it stands. *12:1x* and *13:3x* were P3 (FM-035's review, R6; FM-030's
  review, R8), and the record should carry its own time rather than point to another project's ledger.
- **Fix, forward, on the next touch:** 15:34:27 in both rows.

**R2 · P3 · confidence medium · The Auditor's item named FM-028 for both lines; the seat placed the second in FM-029 and
does not say so.**
- Item 2 opens *FM-028, a line* and puts the FM-032 relation case in it (*plus one real-history relation case …*).
- The row in FM-029 reads *on the Auditor seat's item 2 through the Owner*, as if the Auditor had named FM-029.
- FM-029 is the relation's own tracker, so the placement is sound (rule 6, the closest open tracker).
- `--day` as the flag's name and *reaches the same tree* are also the seat's wording of the Auditor's *an explicit day*.
  They sit under *Proposed*, which is fair.
- **Fix, forward:** *placed here by the Principal seat, the relation's tracker*, or a word to the same effect.

## Verdict

**READY WITH FINDINGS (R1, R2 P3).**
- Both rows are appended in their logs' orders.
- Their facts hold: line 5043, lines 3260–3270, `ffa63b8` → *accepted the proposal*.
- The gates, the generator and both suites are green, and merge-tree is clean against `origin/main` and the FM-030
  branch.
- R1 and R2 are fixed forward under the docs tier.

The Owner lands this by merging; a merge rules nothing.
