# Review — FM-030's ask on the board, second pass at 43a56aa (2026-09-27 14:40 CEST, Reviewer, session `8e509911/reviewer-39`)

- **Branch:** `fm/030-the-board-reads-his-unmerged-acts-asked`, tip `43a56aa` (`43a56aa6f65a5784f68d942e46a2d51dc7d8e641`,
  confirmed by `git ls-remote`). It is one Principal commit (`principal@seat`, `Session: 8e509911`,
  `Worktree: shoalmark-principal-4`) on my first verdict `dd9a19e`. It was authored and committed 14:32:46; the brief's
  14:33:03 is most likely the push. It answers the first pass's R1, R3 and R4, and leaves R2 to the merger.
- **Tier: docs, one pass.** The commit touches four paths, all under `work-tracker/`: FM-030, INDEX, TRIAGE.md (the
  *Passes* section) and the day's worksheet. No `.py` has changed since `28e54bf`, so no suite was run.
- **Independence:** same session (`8e509911`), reported.
- **Verdict: NOT READY.** One P2 (N1): the pass's record describes the Owner's two raises wrongly, and dates one of them
  wrongly. Everything else holds.

## What I ran

| run | result |
|---|---|
| `git diff dd9a19e..HEAD` | FM-030: `triaged:` 09-25 → 09-27 (no other key); the design paragraph's *end where they started (on \`main\` for him)*; both new `## Raised` bullets end `· undermines: path 6`; the 13:57:50 quote marks its cuts `[…]`; one ship-log row. INDEX: FM-030's triaged date. TRIAGE.md: one paragraph at the top of *Passes*. Worksheet: one FM-030 row |
| `raise_lines`, the tool's parser, on FM-030 at the tip | 13:57:50 → `['path 6']`, 14:09:46 → `['path 6']`. At `03877b2` both gave `[]` |
| scratch clone at `43a56aa`, `--triage` | *0 trackers to judge*, *Applied nothing*, the tree unchanged |
| replay: that clone with FM-030's `triaged:` set back to 09-25 and `dd9a19e`'s worksheet, `--triage` | *1 trackers to judge*. The generated FM-030 row equals the tip's row in every cell up to Facts (*RAISED*, *FM-029 (20)*, the Now line). Facts differs only in size: *reads 4.1k* against the tip's *3.9k*, because the tracker grew after the row was generated |
| the replay with `43a56aa`'s worksheet restored, `--triage` | *Applied 1: FM-030: keep P1 #2 owner*. The tree then equals `43a56aa` (`git diff --quiet 43a56aa`), so the front matter and INDEX are the command's |
| a hand edit of the applied row's Reason, then `--triage` | *Applied nothing*. The edit survives the rewrite, so N1's cure is safe |
| `python3 shoalmark.py --check` | exit 0. *INDEX.md is up to date — 39 trackers*. *the Owner's two sections: guarded — … none changes them or his signers file* |
| `git diff -U0 dd9a19e..HEAD -- work-tracker/TRIAGE.md` | one hunk at line 29, under `## Passes` (line 25). *The intent* (6) and *The current path* (14) are untouched |
| `python3 shoalmark.py --session-check` | exit 0 |
| `--owner`; the board (rebuilt by the checkout hook) | *1 NEED THE OWNER*: FM-030, the ask word for word. On the board FM-030 is in section `progress`, `next` owner, triaged 09-27, with no problems. The waiting list is FM-030 alone |
| `git merge-tree --write-tree origin/main HEAD`, `origin/main` now `62b4a05` (PR 99, `answer/fm-024`) | clean (`0e18995`) |
| that merge made in the scratch clone, then `--check` | exit 0, *INDEX.md is up to date*. INDEX auto-merges and stays fresh |
| `git merge-tree 5e6d816 HEAD` | the same content conflict in FM-030's `## Raised` (R2, the merger's) |
| `git show -s 9e48ee8` and the merge after it | 2026-09-24 18:59:10 `G`, merged by PR 59 (`5bd3ad5`, 18:59:38), as TRIAGE.md cites |
| the transcript, user records 11:34–12:10Z | the *done*-dialog words at **11:38:30Z = 13:38:30** with *Screenshot … 13.35.40*; the board words at 13:57:50; *Option \`1\` …* at 14:09:46. His `--done FM-024` is `f8246fae`, 13:44:51 |

## The first pass's findings

- **R1 ✓.** Both bullets now parse as naming path 6. The raise rule fired, and the row was applied by the command:
  `keep P1 #2 owner`, `triaged: 2026-09-27`, rank 2, tier P1, `next: owner`. The replay reproduces the tip exactly.
- **R3 ✓, with a P3 (N3).** The ship-log row names the ledger row (`71a06fbe`, 14:12:51) and the ask commit (14:14:18).
  Both times are right.
- **R4 ✓.** The two cuts are marked: *not yet merged […]* and *right away […]*. The ellipsis is now `[…]`. *End where
  they started (on \`main\` for him)* matches the tool's *back on \`…\`*.
- **R2** is left to the merger. The cure is unchanged: both blocks, in time order.

## Findings

**N1 — P2 · the pass describes the Owner's two raises wrongly, and dates one of them wrongly.** Confidence in the facts:
95%, from the transcript and git. Confidence that this is P2 rather than P3: 75%. It puts his words at a time and in an
order he did not say them, in the record that justifies a pass under his signed rule.

The worksheet's Reason reads: *two raises of 2026-09-27 name path 6 — the \*done\* dialog shows the ask's question, not
his promise (13:57:50, after his \`--done FM-024\`), and the board rebuilt from main shows an act he just gave as still
open (13:57:50; his word 14:09:46)*. TRIAGE.md's paragraph says the same, without the times.

- The *done*-dialog observation is his message of **13:38:30**, with a screenshot of 13:35:40. That is **before** his
  `--done` (`f8246fae`, 13:44:51), not after it, and not at 13:57:50.
- The bullet that carries it is not on this branch. It is on `fm/030-the-done-dialog-shows-the-question` (`5e6d816`),
  where it reads `undermines line 6 (…)`, which the tool does not parse. So it is not one of the raises that fired the
  rule.
- The two bullets on this branch that name path 6 are 13:57:50 (the board still shows the act he just gave) and 14:09:46
  (his go-ahead).

*Cure:* make the Reason cell and the TRIAGE.md paragraph name the raises this branch carries. First, 13:57:50: after his
`--done FM-024` (13:44:51), the board, rebuilt from `main`, shows the act as still open. Second, 14:09:46 if it stays
a raise (N2). If the dialog observation is mentioned, it is 13:38:30 (screenshot 13:35:40), before his `--done`, and it
is the build branch's.

A hand edit to the Reason applies nothing (tested above). The ship-log row's *the two raises name path 6* is true of
the branch and can stay.

**N2 — P3 · the 14:09:46 bullet now claims to undermine path 6.** His *Go, file the ask on FM-030 with option 1 as
proposed* reports no fact against a rule; it is his go-ahead. The rule fires on the 13:57:50 bullet alone, so dropping
`· undermines: path 6` from 14:09:46 changes no verdict (one raise suffices). The alternative is to move that bullet
into the ship-log row, as the first pass's R3 offered.

**N3 — P3 · the new ship-log row is at the top of a table that runs oldest first.** The other rows go from 2026-09-24 to
2026-09-26, top to bottom. *Cure:* move the row to the bottom.

## Not checked

- `--queue`, which needs `gh`.
- The suites: no `.py` changed.
- The build branch `5e6d816` itself. It is outside this review, and its two new bullets have the unparsed `undermines
  line 6` form noted in the first pass.

The Owner lands this by merging. A merge rules nothing: his signed answer through the board rules the ask.
