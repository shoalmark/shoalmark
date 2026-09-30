# The records-to-product ratio — shoalmark's definition

Filed 2026-09-30 on the Owner's words, one line each, *normalised* (spelling and punctuation; times CEST). No other source.

- 06:54:04, the concern — *"The records-to-code ratio shall become our main concern now. These numbers must even out or invert."*
- 07:04:27, the definition — *"We shall track added lines vs deletions — so separately."*
- 07:04:27, the ruling — *"If a check output regenerates, keep only its summary; if it doesn't, it stays in git."*
- 07:14:05, the split — *"We split."* This repository is public: the rule lives here, with no other project's numbers or paths.
- 07:21:58, the go — *"Go, freeze excepted."* `--ratio` is their explicit exception to the filing freeze.
- 07:23:33, their ruling (2), in substance: `--ratio` and the check-output rule as ONE combined PR on FM-032, an explicit exception to
  the freeze; the public definition page folded into it; Implementer on Sonnet, Reviewer on Opus; report per Berlin day, judge on
  rolling seven-day sums; the page names the command as the reference.
- 19:16:21, the condition — *"An output is replaced by a summary and a check only where it is larger than the two together."*

## The rule

- **ratio = record lines added : product lines added**, per repository, per Europe/Berlin calendar day of the merge.
- **A merged pull request** is a merge commit on the default branch's first-parent line, compared with its first parent. **Its day** is the
  merge commit's committer date, in Europe/Berlin.
- **Deletions are tracked separately**, never netted. Deleting records offsets nothing.
- **A moved or renamed file counts as its lines deleted and added**: git's rename detection is a heuristic and a user setting, so the
  reference counts without it, and each side of a rename counts as its lines.
- **Aggregates are summed counts**, never averaged ratios. Zero product added: the counts, and no finite ratio (0:0 undefined).
- **Judged on rolling seven-day sums, reported per day.** Every plan states its expected records added, product added, record deletions,
  product deletions and ratio effect.
- *Product* is a measurement category: it asserts no delivered functionality. No code-volume target is implied.
- **shoalmark's records:** `work-tracker/`. **Product:** everything else. Submodule pointers are excluded; a binary file counts 0 lines.

**The reference is the command:** `python3 shoalmark.py --ratio` with the `[ratio]` section of `shoalmark.toml`. A difference between this
page and the command is a bug against this page: the page is the rule, the command is fixed to it, and an ambiguity in the page is fixed
by the Owner's word.

## Check outputs

The ruling above, applied. The summary kept of a regenerable output is: the command as run, the tested commit, the environment (Node,
Chrome, Zensical versions), the pass and fail counts and the failing check ids by the README's thresholds, the deleted file's sha256 and
the commit that still holds it (`git show <commit>:<path>` — history keeps every byte). A committed check proves regeneration: the test in
`test_shoalmark.py`, switched on by `SHOALMARK_REGENERATE=1`. No CI artifacts, no release assets. An output that does not regenerate from
git by a committed command stays, and counts.

**The condition, 19:16:21, the Owner's words, normalised:** *"an output is replaced by a summary and a check only where it is larger than the two
together."* The Jev scorer's output (`jev-gate-test-score-output-2026-09-23.txt`) stays on main as it is, by their word.

## The baseline — shadow week, 2026-09-22 to 2026-09-29

| | the baseline the Owner relayed, 07:04:27 | the command's own output at this branch's tip |
|---|---|---|
| records added : product added | 66,550 : 15,968 (4.2:1) | 65,711 : 15,713 (4.2:1) |
| records deleted / product deleted | 1,015 / 1,784 (relayed, not remeasured) | 972 / 1,764 |

The command's per-day lines for the window (`--ratio --since 2026-09-22 --until 2026-09-29`), 111 merges; the 09-27 day carries four check
outputs of two folders (`073f21f` and `9d10d08`, both 12:02). `test_shoalmark.py` asserts the window's four numbers above.

| day | records +added −deleted | product +added −deleted | ratio | merges |
|---|---|---|---|---|
| 09-22 | +441 −11 | +1,671 −167 | 0.3:1 | 10 |
| 09-23 | +9,373 −88 | +2,312 −207 | 4.1:1 | 12 |
| 09-24 | +6,459 −245 | +2,061 −533 | 3.1:1 | 33 |
| 09-25 | +4,248 −110 | +3,349 −476 | 1.3:1 | 18 |
| 09-26 | +4,348 −38 | +1,418 −92 | 3.1:1 | 12 |
| 09-27 | +36,778 −87 | +1,833 −83 | 20.1:1 | 9 |
| 09-28 | +2,831 −55 | +1,969 −145 | 1.4:1 | 14 |
| 09-29 | +1,233 −338 | +1,100 −61 | 1.1:1 | 3 |

## This change's own numbers

PR 131 as merged: the merge commit `c525a41` against its first parent `c97d6be` (`git diff --numstat --no-renames c525a41^1 c525a41`), classified by the rule (`work-tracker/` = records). The Reviewer's verdict files count as record lines and stay. The record deletions are the four regenerable check outputs (the Jev scorer's output stays, by the Owner's word of 19:16:21); deleting
records offsets nothing.

- records added 699 · product added 538 · 1.3:1
- record deletions 33,529 · product deletions 9
