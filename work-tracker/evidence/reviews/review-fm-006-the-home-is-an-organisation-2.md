# Review — FM-006: the home at the flip after the merge of main, second pass (2026-09-26, Reviewer, session `8e509911/reviewer-25`)

- **Date:** 2026-09-26, from 12:15 CEST.
- **Seat:** Reviewer (Opus 5.5, highest effort), a sub-agent of Principal session `8e509911`.
- **Session:** `8e509911/reviewer-25`.
- **Worktree:** `shoalmark-review-5`, on the local branch `home-review` at the tip. Nothing else of this repository was
  touched; the sealed session `8b91dba2`, the Owner's checkout, `shoalmark-gtm` and every other worktree stayed outside
  every command. The paste file in the Principal's scratchpad was read, not changed.
- **Tier:** docs, one pass. `git diff --name-only origin/main...HEAD` holds the FM-006 tracker and this seat's first
  verdict file; no `shoalmark.py`, test, configuration or hook. A P3 is fixed forward or left; a P2 sends it back.
- **Independence:** same session — 8e509911's own sub-agent reviewing the Principal seat's three commits
  (`Session: 8e509911`) on `8e509911/implementer-34`'s filing. Reported, not independent.

**Reviewed:** `fm/006-the-home-is-an-organisation` at `ceb0810dd64f7a0d2fa82c8858dcbe00554452cd`. Since this seat's
first pass (`7cf4eb5`, on `67532e3`: READY WITH FINDINGS, R1 and R2 P3), three commits by the Principal seat
(`Worktree: shoalmark-principal`, unsigned): `f681fa2` (11:58:45) merges `origin/main` `5169398` (PR 82) into the
branch; `93a790a` (12:11:07) and `ceb0810` (12:14:36) fix forward. `origin/main` is still `5169398` at a fresh fetch.

**The source.** The paste file `auditor-fm006-organisation-home-paste.md` in the Principal's scratchpad: 8 lines,
735 bytes, sha256 `19ca39d1794c67cf15e26399667d392cadc65fdb1c5c5d22fe44993277ad4ec5`, as at the first pass.

## The checks

| # | Check | How | Result |
|---|---|---|---|
| 1 | The merge brings nothing of its own | `git show --remerge-diff f681fa2`: one file, the one conflict at the ship log's top; `git diff f681fa2^2 f681fa2` | The resolution is the branch's row, then main's three, the markers dropped, no other byte. Against main the merge adds only the branch's 16 lines and the first verdict file ✓ |
| 2 | Main's FM-006 kept whole | `git diff --numstat origin/main HEAD` on FM-006; the hunks read | 16 added, 0 removed. Three hunks: the What-is-true-now line (l.28, +2), the end of *Going public* (l.131–143, +13), the top of the ship log (l.270, +1). All of PR 82's 104 lines stand: its two What-is-true-now paragraphs, the themes and landing sections, its five ship-log rows (three were in the conflict, two merged without one) ✓ |
| 3 | The ship log, newest first | the rows counted and their dates read, top to bottom | 43 rows at the tip: main's 42 in main's order, the home row first. No date rises down the table. The home filing (`67532e3`, 11:15:48) is later than PR 82's newest row (the landing page, `9704140`, 10:22:41) ✓ |
| 4 | The paste, word for word | FM-006 l.133–140 (l.129–136 at the first pass; PR 82's two paragraphs above add 4 lines): after the heading (l.131) and a blank line, before a blank line and the gloss (l.142). sha256 over exactly those lines; `cmp` against the paste file | 8 lines, 735 bytes, `19ca39d1…ad4ec5`; byte-identical ✓ |
| 5 | The first pass's R1, fixed | l.28, set beside the heading (l.131) and the row (l.270) | *— the Owner's word of 2026-09-26 through the Auditor seat, as pasted by him at 11:05:27, sha256 `19ca39d1…ad4ec5`* (all 64 hex digits): the day goes to his word, the minute to the paste, and the hash is there. It agrees with the heading and the row ✓. Fixed by `ceb0810` (one line), not by `93a790a`: this file's R1 |
| 6 | The first pass's R2, fixed | l.142; `git grep -i "parent projects"` at the tip | *… are PortDive's and the two clients' own slices at the flip …*. *The parent projects* is gone from FM-006; the plural stands only in the first verdict file, which quotes it. *The two clients* meets the ask's own term, *client names*. FM-002 calls the German board it tested on *the first client's* (l.15), and its evidence names that copy msr-lager's (`evidence/FM-002/brand-layers-rd.md` l.62). fb-sondermasch as a client stands on the seat's word, inside the marked gloss. Fixed by `93a790a` ✓ |
| 7 | The front matter is byte-identical to `origin/main`'s | `cmp` of l.1–16; sha256 of both | `69f8d577…` both, the same as at the first pass ✓ |
| 8 | The files | `git diff --name-only origin/main...HEAD` | FM-006 and `evidence/reviews/review-fm-006-the-home-is-an-organisation.md`, the first pass, unchanged since `7cf4eb5`. `INDEX.md` unchanged and up to date. The brief expected the tracker alone; the second file is that verdict ✓ |
| 9 | `--check` | at the tip | exit 0: *INDEX.md is up to date — 37 trackers*; judged before build on (4 commits); the Owner's two sections guarded (5 commits); *filing freeze: 21 open* ✓ |
| 10 | `--session-check` | at the tip | exit 0 ✓ |
| 11 | Both suites by hand, as `lefthook.yml` runs them | `test_shoalmark.py`, `test_core.py` on 3.14.3 and on `/usr/bin/python3` 3.9.6 | exit 0 on both. `test_shoalmark.py`: 462 ok, *skipped here: 0 checks — every check ran*, *all green*. `test_core.py`: 148 ok, *all green* ✓ |
| 12 | Merges clean | `git merge-tree --write-tree origin/main HEAD` after a fresh fetch | clean, `b3c3799`, the tip's own tree: `origin/main` is an ancestor of the tip ✓ |
| 13 | PR 87 | `gh pr view 87 --repo holgo99/shoalmark` | open, not a draft, head `ceb0810`, *MERGEABLE*, *CLEAN*; no status checks reported ✓ |

## Findings

**R1 · P3 · confidence 95% · `93a790a`'s subject claims R1 and R2 fixed; its diff fixes R2 alone.**
- **Why it matters.** The subject reads *the home line's pass R1 and R2 fixed forward — the What-is-true-now line names
  the paste's time and hash; the gloss says PortDive's and the two clients' slices, not the parent projects'*. Its diff
  is one line, the gloss. It leaves l.28 as it was. A reader of `git log --oneline` takes R1 as fixed there.
- **The record.** `ceb0810` fixes R1 three and a half minutes later, and its subject says what was wrong: *the previous
  commit's subject claimed R1 and had fixed R2 only*. Under FM-032 S3 (`AGENTS.md`), a seat's own error that cost the
  Owner no command or decision is fixed, and the fixing commit's message says what was wrong: git is its record. The
  branch is unmerged; the overclaim cost him nothing.
- **What closes it.** Nothing more. A pushed commit is not rewritten, and `ceb0810`'s subject is the correction.
  Nothing is left to fix forward.

## Verdict on ceb0810: READY WITH FINDINGS (R1 P3)

- The merge of `origin/main` keeps main's FM-006 whole and brings nothing of its own. The one conflict is resolved as
  the home row first and PR 82's three rows after, and the ship log runs newest first.
- The filed paste still equals the paste: now l.133–140, 8 lines, 735 bytes, sha256 `19ca39d1…ad4ec5`.
- The first pass's R1 and R2 are fixed at the tip. `93a790a`'s subject overclaims R1, and `ceb0810` corrects the
  record (R1 here, P3, nothing left to do).
- The front matter is byte-identical. The diff is the tracker and the first verdict, the gates are green, it merges
  clean, and PR 87 is mergeable.

*The Owner lands this by merging, and a merge rules nothing (path 5).*
