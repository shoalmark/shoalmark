# The records-to-product ratio — shoalmark's definition

Filed 2026-09-30 on the Owner's words, one line each, *normalised* (spelling and punctuation; times CEST). No other
source.

- 06:54:04, the concern — *"The records-to-code ratio shall become our main concern now. These numbers must even out or
  invert."*
- 07:04:27, the definition — *"We shall track added lines vs deletions — so separately."*
- 07:04:27, the ruling — *"If a check output regenerates, keep only its summary; if it doesn't, it stays in git."*
- 07:14:05, the split — *"We split."* This repository is public: the rule lives here, with no other project's numbers or
  paths.
- 07:21:58, the go — *"Go, freeze excepted."* `--ratio` is his explicit exception to the filing freeze.
- 07:3x, his ruling (2) — *`--ratio` and the check-output rule as ONE combined PR on FM-032, an explicit exception to
  the freeze;
  the public definition page folded into it; Implementer on Sonnet, Reviewer on Opus; report per Berlin day, judge on
rolling
  seven-day sums; the page names the command as the reference.*

## The rule

- **ratio = record lines added : product lines added**, per repository, per Europe/Berlin calendar day of the merge.
- **A merged pull request** is a merge commit on the default branch's first-parent line, compared with its first parent.
- **Deletions are tracked separately**, never netted. Deleting records offsets nothing.
- **Aggregates are summed counts**, never averaged ratios. Zero product added: the counts, and no finite ratio (0:0
  undefined).
- **Judged on rolling seven-day sums, reported per day.** Every plan states its expected records added, product added,
  record
  deletions, product deletions and ratio effect.
- *Product* is a measurement category: it asserts no delivered functionality. No code-volume target is implied.
- **shoalmark's records:** `work-tracker/`. **Product:** everything else. Submodule pointers are excluded; a binary file
  counts 0 lines.

**The reference is the command:** `python3 shoalmark.py --ratio` with the `[ratio]` section of `shoalmark.toml`. A
difference
between this page and the command is a bug against this page: the page is the rule, the command is fixed to it, and an
ambiguity in the page is fixed by the Owner's word.

## Check outputs

The ruling above, applied. The summary kept of a regenerable output is: the command as run, the tested commit, the
environment
(Node, Chrome, Zensical versions), the pass and fail counts and the failing check ids by the README's thresholds, the
deleted
file's sha256 and the commit that still holds it (`git show <commit>:<path>` — history keeps every byte). A committed
check
proves regeneration: the test in `test_shoalmark.py`, switched on by `SHOALMARK_REGENERATE=1`. No CI artifacts, no
release
assets. An output that does not regenerate from git by a committed command stays, and counts.

## The baseline — shadow week, 2026-09-22 to 2026-09-29

| | the baseline the Owner relayed, 07:04:27 | the command's own output at this branch's tip |
|---|---|---|
| records added : product added | 66,550 : 15,968 (4.2:1) | to be filled from the command, as it lands |
| records deleted / product deleted | 1,015 / 1,784 (relayed, not remeasured) | to be filled from the command, as it lands |

The per-day table, 09-22 to 09-29 (the 09-27 day carries the two check outputs), is the command's own and is filled with
it.

## This change's own numbers

Records added, product added, record deletions and product deletions of `git diff --numstat origin/main...HEAD`,
classified by
the rule: to be filled last.
