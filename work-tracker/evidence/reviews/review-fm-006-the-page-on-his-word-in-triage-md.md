# Review — FM-006: the page on his word in TRIAGE.md (2026-09-25 22:56 CEST, Reviewer, session `8e509911/reviewer-17`)

A new file: `review-fm-006-when-shoalmark-goes-public.md` reviews the go-public ask, and this branch files a different
subject, the site page on TRIAGE.md, under the same tracker.

## Verified: the page on his word filed, b025d98

**Scope.** `fm/006-the-page-on-his-word-in-triage-md`, tip `b025d98` (`b025d98e16f826ed865cb0697376c0b524c7eaf9`), one
commit by the principal seat (`Session: 8e509911`, 22:40:18) on `origin/main` `0d60d55` (PR 79's merge). It changes
FM-006 alone: 26 lines added, none removed. **Tier: docs, one pass.** A misquote of the filed text is P2; the rest is P3.
**Independence:** same session — 8e509911's own sub-agent, reported.

**What I ran.**
- **The paste.** The filed text after its opening bold line (FM-006 line 127) is lines 129–142, from *From the Auditor
  seat, on the Owner's word: …* to *- Worded by the GtM seat; …*: 14 lines, 1514 bytes, the last newline included.
  sha256 over exactly those lines: `be19a4100d73fc27f6d0015ac42a8c4ee152ebcfa751e9ec8fc523ac99933584`. It equals the
  brief's hash and the hash in the opening line, and `cmp` finds it byte-identical to the paste file ✓.
- **The Principal's text after it** (lines 144–146; two sentences over three lines, the second wrapped after *words
  it,*), against the paste and the record:
  - *the freeze (20 open)*: `--check` at `b025d98` prints *filing freeze: 21 open* (R1). That the freeze bars a new
    tracker is the paste's own word ✓.
  - *FM-022 (Shipped) left the site out on purpose*: FM-022 is `status: Shipped`, and its body says *Not changed, on
    purpose: … `docs/setup.md` §5 (EN and DE), the documentation site* ✓.
  - *this tracker holds the page*: the paste's *a line on FM-006* ✓.
  - *The build waits for FM-037's guard to merge*: FM-037 is In Progress, `next: build` on main, and its build branch
    `origin/fm/037-only-the-owner-changes-his-intent-and-his-path` (tip `a92a3cc`, ten commits) is not an ancestor of
    `origin/main`. So the build is pending ✓. *only you change it*, the tool's, with its tier-0 limit: the paste's second
    bullet, and FM-037's clause 6 ✓.
  - *the GtM seat words it, a Reviewer checks every claim against evidence before the merge*: the paste's last bullet ✓.
  - *the term stays* your signed word: the GtM seat's decision is FM-006's ship-log row of 2026-09-25 (line 156: *your
    signed word*, not *mandate*; `af5229e`, `50a39b7`) ✓. *Unless the Owner rules otherwise by an ask* shortens the
    paste's *rules "mandate" or "Person-in-charge" in by an ask*. It is not quoted, and it adds no power a ruling by ask
    lacks. Not a finding.
- **The three commits the paste names.** All three are on `origin/main`:
  - `fe36cc0` is the Owner's own signed commit (holgo99, `%G?` G, 10:37:13, *Updates after parley with Consigliere*).
    It rewrites the intent's three lines and the current path. Path line 3 is rewritten whole: a review's evidence file
    on the head, a Reviewer from another independent session for critical changes, inline passes on other code, one pass
    for documentation, and the Owner's own answers reported, never blocking. Lines 1, 2 and 5 are reworded, and line 6
    is added ✓. The independence count is the line `--check` prints: *99 verdict(s) · independent 8 · same session 86 ·
    untraced 5* ✓.
  - `42f4eca` is the principal seat's, unsigned, 12:15:38. *triage: FM-035 kept P1 #6 build the same day it was filed*.
    It sets FM-035's front matter to `tier: P1`, `rank: 6`, `next: build`, and its Passes paragraph cites path line 1
    cut, as *a failed command* ✓.
  - `c8939e3` is the principal seat's, 12:30:44, made on its Reviewer's R1–R5. It changes `tier: P1` to `tier: P2`, and
    quotes path line 1 whole: *the daily sitting runs on a tagged release with a signed answer and no failed command in
    the sitting* ✓.
- **What is true now** (line 22) matches the section: a page for people on what TRIAGE.md holds, the intent and the
  current path, and what an edit there does. It is owed on the Owner's word (22:38:24), built after FM-037 merges, and
  the line is filed below ✓. It is a summary, not a quote.
- **The ship-log row** is at the top, dated 2026-09-25, and no row below it changed. Every clause is the paste's: English
  and German, the intent and the path and what an edit does, each claim labelled, worded by the GtM seat, every claim
  checked, built after FM-037 with FM-007's tier-0 limit. It gives the hash as `be19a410…` and states no open count ✓.
- **Front matter.** Byte-identical to `origin/main`'s (the diff's first hunk is at line 22). `ask:`, `ask-kind: action`,
  `ask-since:`, `ask-options:`, `ask-proposal:` and `next: owner` are untouched ✓.
- **Gates.**
  - `python3 shoalmark.py --check` 0: *INDEX.md is up to date — 37 trackers*, the freeze line *21 open, at or above 8 —
    only bug filings*, and every build commit under a judged In Progress tracker.
  - `--session-check` 0.
  - The suites as `lefthook.yml` runs them: `test_shoalmark.py` 0 (438 ok, no check skipped) and `test_core.py` 0 (148
    ok), on 3.14.3 and on `/usr/bin/python3` 3.9.6.
  - `git diff --name-only origin/main...HEAD` lists FM-006 only. INDEX.md was not regenerated, and it needed no
    regeneration ✓.
  - `git merge-tree --write-tree origin/main HEAD` is clean (`9acf9a5`). `origin/main` is still `0d60d55` after a fresh
    fetch.

**R1 · P3 · confidence 95% · *the freeze (20 open)* is out of date: `--check` says 21.**
- At `b025d98` and at its base `0d60d55`, `--check` prints *filing freeze: 21 open, at or above 8*. By status, 15 are In
  Progress, 4 Parked and 2 Proposed.
- 20 was right at the addendum's re-make, whose line 97 on main still reads *(`--check`: 20 open, only bug filings)*.
  Then FM-037 was filed at 19:03:56 and made it 21. The added sentence takes the older number.
- The substance holds: the freeze holds at 21 as at 20, and the paste gives no number.
- **Fix forward, or leave:** *(21 open)*, or no number. Line 97 is of its own time and is not this branch's.

**R2 · P3 · confidence 60% (the times are exact; whether the heading should say so is the question) · The heading
dates the filing to the paste's minute.**
- The heading reads *filed 2026-09-25 at 22:38:24*. That is when the Auditor seat's line came through the Owner: the
  opening bold line and the ship-log row both say *through him at 22:38:24*. The filing commit is 22:40:18.
- The file's other dated heading gives the time of the word, not of the filing (*the Owner's finding of 2026-09-25
  09:52:49*).
- **Fix forward, or leave:** *— through the Owner 2026-09-25 at 22:38:24*.

**Verdict on b025d98: READY WITH FINDINGS (R1, R2 P3).**
- The filed paste equals the paste: 14 lines, sha256 `be19a410…`.
- The Principal's added text rests on the paste and the record, except for its open count (R1).
- The three commits exist on main and show what the paste says of them.
- The What-is-true-now line and the ship-log row match the section.
- The front matter and the ask are untouched, and the gates are green.
- Tier: *docs, one pass*. Independence: *same session — 8e509911's own sub-agent, reported*.

The Owner lands this by merging; a merge rules nothing.
