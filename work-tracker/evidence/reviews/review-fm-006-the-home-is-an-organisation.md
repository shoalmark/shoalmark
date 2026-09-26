# Review — FM-006: the home at the flip is a GitHub organisation (2026-09-26, Reviewer, session `8e509911/reviewer-24`)

- **Date:** 2026-09-26, from 11:19 CEST.
- **Seat:** Reviewer (Opus 5.5, highest effort), a sub-agent of Principal session `8e509911`.
- **Session:** `8e509911/reviewer-24`.
- **Worktree:** `shoalmark-review-5`, detached at the tip. Nothing else of this repository was touched; the sealed
  session `8b91dba2` and every folder of the Auditor seat's stayed outside every command.
- **Tier:** docs, one pass. A P3 is fixed forward or left; a P2 sends it back. A misquote of the filed text is P2.
- **Independence:** same session — 8e509911's own sub-agent reviewing `8e509911/implementer-34`'s commit. Reported, not
  independent.

**Reviewed:** `fm/006-the-home-is-an-organisation` at `67532e35d54ea954c59d3112487bf034a3f83647`. One commit by the
Implementer seat (`Session: 8e509911/implementer-34`, `Worktree: shoalmark-impl-4`, 11:15:48, unsigned) on `origin/main`
`a7e5291` (PR 86's merge). It adds 16 lines to FM-006 and removes none.

**The source.** The paste file in the Principal's scratchpad, `auditor-fm006-organisation-home-paste.md`: 8 lines,
735 bytes, sha256 `19ca39d1794c67cf15e26399667d392cadc65fdb1c5c5d22fe44993277ad4ec5`, the brief's hash.

## The checks

| # | Check | How | Result |
|---|---|---|---|
| 1 | The paste, word for word | FM-006 l.129–136: after the opening bold line (l.127) and a blank line, before a blank line and the gloss (l.138). 8 lines, 735 bytes, the last newline included. sha256 over exactly those lines; `cmp` against the paste file. The method of the TRIAGE paste of 22:38:24 (`review-fm-006-the-page-on-his-word-in-triage-md.md`) | `19ca39d1…ad4ec5`, equal to the brief's and the header's; byte-identical ✓ |
| 2 | The header names the time and the full hash | l.127 | *as pasted at 11:05:27 (sha256 `19ca39d1…ad4ec5`)*, all 64 hex digits ✓ |
| 3 | The gloss is in brackets and marked as not his word | l.138 | *[The seat's gloss, not his word: …]* ✓ |
| 4 | The gloss says nothing beyond its three points | l.138, clause by clause | (a) *the transfer is the mechanism of the ask's first option (this repository … public) and changes no option's text*: the quote is a faithful elision of option 1, and no option changed (check 6) ✓. (b) *the consumers' pins (PortDive PD-400, msr-lager, fb-sondermasch) are the parent projects' own slices at the flip* ✓: PD-400 is the PortDive tracker that holds the shoalmark pin (its ship log, 2026-09-25: *the pin of shoalmark 0.18.3 is this tracker's next build*, read-only). The term, R2. (c) *nothing moves before his answer to the ask* ✓. One clause beyond the three: *named here so none is forgotten*. It gives the seat's reason for naming them. It states no fact of the plan and rules nothing. Not a finding. |
| 5 | The What-is-true-now line and the ship-log row state the same facts, with the time and the hash | l.24; l.171 | The row: the paste's facts in its order, *as pasted at 11:05:27*, the full hash. It leaves out only *(free for a public repository)*. *The ask and its options are unchanged* holds (check 6) ✓. The What-is-true-now line: the organisation, *nothing moves before the flip*, filed in *Going public* ✓. It dates the word, not the paste, to 11:05:27, and it gives no hash: R1. |
| 6 | The front matter is byte-identical to `origin/main`'s | `cmp` of l.1–16; sha256 of both `69f8d577…` | ✓ `ask:`, `ask-kind: action`, `ask-since:`, `ask-options:`, `ask-proposal:` and `next: owner` untouched |
| 7 | No other section or row changed | `git diff --numstat origin/main...HEAD`: 16 added, 0 removed. Three hunks: the What-is-true-now line (+2), the end of *Going public* before the TRIAGE page's heading (+13), the top of the ship log (+1) | ✓ |
| 8 | The tracker only | `git diff --name-only origin/main...HEAD` | FM-006 alone. `INDEX.md` unchanged, and `--check` finds it up to date ✓ |
| 9 | `--check` | at the tip, detached | exit 0: *INDEX.md is up to date — 37 trackers*; judged before build on; the Owner's two sections guarded; *filing freeze: 21 open* ✓ |
| 10 | `--session-check` | at the tip | exit 0 ✓ |
| 11 | Both suites by hand, as `lefthook.yml` runs them | `test_shoalmark.py`, `test_core.py` on 3.14.3 and on `/usr/bin/python3` 3.9.6 | exit 0 on both. `test_shoalmark.py`: 462 ok, *skipped here: 0 checks — every check ran*, *all green*. `test_core.py`: 148 ok, *all green* ✓ |
| 12 | Merges clean | `git merge-tree --write-tree origin/main HEAD` after a fresh fetch; `origin/main` still `a7e5291` | clean, `f0fb55b` ✓ |

## Findings

**R1 · P3 · confidence 90% on the facts, 55% that it should change · The What-is-true-now line dates the word, not the
paste, to 11:05:27, and it carries no hash.**
- **Why it matters.** The section's header, the ship-log row and the commit body all say *as pasted at 11:05:27* and give
  the hash. The What-is-true-now line (l.24) says *the Owner's word of 2026-09-26, 11:05:27, through the Auditor seat*.
  The paste dates his word to the day only (*On the Owner's word (2026-09-26)*), and 11:05:27 is when he pasted the
  Auditor seat's line. A reader of that line alone takes 11:05:27 as the time of his word. The commit subject says the
  same (*the Owner's word of 11:05:27*); a subject is not rewritten.
- **The gap.** The two lines this pass sets side by side give the time differently, and only one gives the hash.
- **Against it.** `b025d98`'s What-is-true-now line had the same form (*owed on the Owner's word (22:38:24)*) with no
  hash, and its review passed that line. That review's R2 found a neighbouring one: a heading that gave the paste's
  minute to the filing.
- **What closes it.** *— the Owner's word of 2026-09-26, through the Auditor seat, as pasted at 11:05:27 (sha256
  `19ca39d1…`); …*. Or leave it.

**R2 · P3 · confidence 60% · The gloss calls the three consumers *the parent projects*; in this file *the parent* is
one project.**
- **Why it matters.** In FM-006, *the parent project* and *the parent's traces* name one project, the origin (the
  correction of 17:37:17: *the redaction wrote "the origin" and "the parent project"*). The ask's options keep *client
  names* and *the parent's traces* apart. The gloss (l.138) puts msr-lager and fb-sondermasch with PortDive under *the
  parent projects*. Read against the options, a client's name could be taken for one of *the parent's traces*. The
  plural stands nowhere else on `origin/main` (`git grep -i "parent projects"`: none).
- **Against it.** The brief's own words are *the parents' own slices*, and the seat followed them.
- **The gap.** A term the ask depends on is used in a second sense in the same section.
- **What closes it.** *each consumer's own slice at the flip*, or *the consuming repositories' own slices*. Or leave it.

## Verdict on 67532e3: READY WITH FINDINGS (R1, R2 P3)

- The filed paste equals the paste: 8 lines, 735 bytes, sha256 `19ca39d1…ad4ec5`.
- The header gives the time and the full hash. The gloss is bracketed, marked, and within its three points, plus one
  clause of reason.
- The ship-log row states the paste's facts with the time and the hash. The What-is-true-now line states the same facts,
  but gives the paste's minute to the word and no hash (R1).
- The front matter is byte-identical. Nothing else changed. The diff is the tracker alone, the gates are green, and it
  merges clean.

## For the Owner — ungraded

- **The client names.** The paste names msr-lager and fb-sondermasch, which the going-public options treat as a term
  (*client names … public* / *removed*). On `origin/main`'s tree, msr-lager already stands in two R&D evidence files:
  `work-tracker/evidence/FM-001/seam-bprime-rd.md` (l.34, 57) and `work-tracker/evidence/FM-002/brand-layers-rd.md`
  (l.51, 59, 62, 97, 110, 151). fb-sondermasch stands nowhere in the tree. In main's history it stood once, in
  `review-fix-0.17.5-one-id-one-row-and-an-empty-bucket-says-why.md` (a quoted grep pattern): added at `5a9779d` and taken
  out at `3bf6591`. Merged, this branch makes FM-006 the only file on main's tree that names fb-sondermasch, and the third
  that names msr-lager. No rule on main forbids a client name in a tracker, so this is not a finding; his pick decides.
  Under option 1 both names go public; under option 2 the snapshot removes them.
- **The parent's names.** The paste names PortDive, which already stands in 9 files on main's tree, FM-006 among them.
  The gloss adds PD-400, the parent's tracker id, which already stands on main in `CHANGELOG.md` (l.112) and
  `review-0.18.4-fm030-52cfcc7.md` (l.219).
- **The organisation, read on the forge** (`gh api`, read-only, about 11:30 CEST). `shoalmark` exists, an organisation created
  2026-09-26 at 09:08:34 UTC (11:08:34 CEST, three minutes after the paste), with no repository. Its one member is
  `holgo99`, role admin, active. The filing claims none of this; it agrees with *He creates it (free, empty) now*.
- **Option 2.** The paste does not say where option 2's snapshot is created. The gloss reads the transfer as option 1's
  mechanism only. His answer settles it, and nothing filed contradicts either option.

*The Owner lands this by merging, and a merge rules nothing (path 5).*
