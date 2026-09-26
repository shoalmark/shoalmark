# Review — the same-day pass after v0.18.4, after the merge of main, second pass (2026-09-26, Reviewer, session `8e509911/reviewer-27`)

- **Date:** 2026-09-26, from 13:04 CEST.
- **Seat:** Reviewer (Opus 5.5, highest effort), a sub-agent of Principal session `8e509911`.
- **Session:** `8e509911/reviewer-27`.
- **Worktree:** `shoalmark-review-4`, detached at the tip. The `--triage` run was made in a scratch clone in the
  session's scratchpad. The Owner's checkout, `shoalmark-gtm`, every other worktree and every folder of session
  `8b91dba2` stayed outside every command. The three word files in the Principal's scratchpad were read and hashed, not
  changed.
- **Tier:** docs, one pass. `git diff --name-only origin/main...HEAD` names the same 9 paths as at the first pass, all
  under `work-tracker/`. No `shoalmark.py`, test, configuration, hook, key or signers file is among them. A P3 is fixed
  forward or left; a P2 sends it back.
- **Independence:** same session. This is 8e509911's own sub-agent, reviewing its Principal seat's branch
  (`Session: 8e509911`). Reported as such, not independent.

**Reviewed:** `tracker/triage-2026-09-26-the-brand-raised` at `3455f189a077f8623fb769277fd2104cd78d8999`.
- **Since this seat's first pass** (`9b4e341`, on `8f98103`: READY WITH FINDINGS, R1–R5 P3,
  `review-triage-2026-09-26-the-brand-raised.md`), the Principal seat made two commits (`Worktree: shoalmark-principal-3`,
  unsigned):
  - `c8c9106` merges `origin/main` `8725440` (PR 87) into the branch;
  - `3455f18` fixes forward R2, R1, R3a–d and R5a–c, and leaves R4 for a bug filing.
- `origin/main` is still `8725440` at a fresh fetch. No pull request is open for the branch.

## The checks

| # | Check | How | Result |
|---|---|---|---|
| 1 | The merge brings nothing of its own | `git show --remerge-diff c8c9106`; `git merge-tree 9b4e341 8725440`; `git diff origin/main c8c9106`, each of its paths against `9b4e341` | The remerge shows one file (FM-006) and two conflicts, at *What is true now* and at the ship log's head. The markers are dropped, a blank line separates the pass's line from main's paragraph, and the pass's row sits below the home row. No other byte changes. Against main the merge changes the branch's 9 paths and nothing else. 8 of them are byte-identical to `9b4e341`. ✓ |
| 2 | FM-006 against `origin/main`: only the pass's additions | `git diff -U0` of FM-006, `origin/main..c8c9106` against `a7e5291..9b4e341`, the `+`/`-` lines compared with `cmp` | 3 lines added, 0 removed, byte-identical to the pass's own 3: the landing-page line, its blank line, and its row. The front matter is main's. The tip adds one more line (R2, check 6). ✓ |
| 3 | Every row of main's FM-006, newest first | the rows' dates read top to bottom; commit times of the rows around the conflict | 44 rows: main's 43 in main's order, and the pass's row second. No date rises down the table. The order at the head is: the home row (`67532e3`, 11:15:48, his word of 11:05:27); the pass's (`c3bae92`, 10:36:01, his word of 10:25:41); PR 82's three — the landing mock (`9704140`, 10:22:41), the header (`9467b83`, 09:40:25) and the drafted ask (`7344a78`, 08:34:28). ✓ |
| 4 | `--triage` on the tip | a scratch clone at `3455f18`, `principal@seat`, `python3 shoalmark.py --triage` | *0 trackers to judge*, *Applied nothing — no new filled rows*, exit 0. The word *superseded* appears only in the printed rules; no row is named. The clone was clean after. ✓ |
| 5 | The worksheet since `8f98103`; FM-002's front matter since the pass | blob ids; sha256 of the front matter at `8f98103`, `9b4e341`, `c8c9106`, `3455f18` | The worksheet blob is `f0f6781b…` at `8f98103` and at the tip; no later commit touches it. FM-002's front matter is `ef20a22f…` at all four commits: `status: In Progress`, `next: owner`, the five ask lines, `triaged: 2026-09-26`, `rank: 4`, `tier: P2`. ✓ |
| 6 | `3455f18`: each P3 fix as described, nothing else | `git show --word-diff 3455f18`; the three word files hashed (`shasum -a 256`) and read | 3 files, +6 −4, and every hunk is one of the named fixes. Details below the table. |
| 7 | TRIAGE.md's guarded sections | sha256 of the file above `## Passes`, of the head, *The intent* and *The current path* (each from its heading to the next), at `origin/main` and the tip; `git diff origin/main HEAD` | Identical: above *Passes* `60579d25…`; the head `2f8d9d60…`; the intent `74ff308a…`; the path `a100dbd4…`. Against main the file gains one paragraph and one blank line under *Passes*, first. `--check`: *the Owner's two sections: guarded — 6 commit(s) … none changes them or his signers file*. ✓ |
| 8 | `--check`, `--session-check` | in this worktree at the tip | `--check` exits 0: *INDEX.md is up to date — 37 trackers*; *judged before build: on*; guarded; *filing freeze: 19 open*. It counts `9b4e341` as *same session*. `--session-check` exits 0. ✓ |
| 9 | Both suites by hand | `python3` (3.14.3) and `/usr/bin/python3` (3.9.6), `test_shoalmark.py` and `test_core.py` | All four exit 0. `test_shoalmark.py`: 462 ok on each, *skipped here: 0 checks — every check ran*, *all green*. `test_core.py`: 148 ok on each, *all green*. The tree was clean after. ✓ |
| 10 | merge-tree against `origin/main` | `git merge-tree --write-tree origin/main 3455f18` | Clean, exit 0. The tree `2e17afe8…` is the tip's own, since `8725440` is an ancestor of the tip. ✓ |
| 11 | The first pass's R4 | `git ls-tree` of `work-tracker/` on all 13 branches on origin | No bug filing, and no tracker above FM-037. The only carry is `3455f18`'s commit body (R4 below). |

**Check 6, fix by fix.**

- **R3b ✓.** The 09:23:58 word now carries `21497e4d…`, the file's hash (`21497e4dbd26…`).
- **R3c ✓.** The file's verbatim line reads *go — raise FM-002 as propsed. FM-006 i will answer after v0.18.4 has
  landed. for the `v0.18.5` release …*. The *…* stands exactly where the dropped sentence was.
  - The quote also drops *, that goes* before *alongside*. That falls under the normalisation the line declares.
- **R3d ✓.** The paste's AU-16 line: every `::before`/`::after` marker has empty alt text; *the chart's coordinate
  labels stay hidden from screen readers, as the refile tested*. Both clauses now stand in *What is true now* and in
  the new *Done when*.
- **R3a ✓ as described.** The three hashes are the files' (`34ee13d103b1…`, `21497e4dbd26…`, `416d54ce7808…`), and the
  line now says whose files they are. The words themselves remain outside the repository (R2 below).
- **R1 ✓, but for two edges (R3 below).** A paragraph *The themes, raised 2026-09-26 — done when:* follows the 0.8.0
  paragraph. Every line the first pass asked for is in it:
  - the named theme worn from `work-tracker/brand/theme.css` and `docs/stylesheets/`;
  - the two cuts, hashed;
  - the header inline, per his 09:23:58 word;
  - no `shoalmark.py` change;
  - renders in both schemes at both widths, seen by him before the merge;
  - AU-16 whole and AU-18;
  - contrast re-measured on the built files;
  - one Reviewer pass;
  - live at the next tag;
  - slice B only on his ruling, with the suites, the CHANGELOG and the consumer's default;
  - both slices judged by a pass before their first build commit (FM-033).

  The paragraph agrees with FM-002's *What is true now* and with FM-006's slices.
- **R2 ✓ as described, not whole (R1 below).** One bullet now precedes FM-006's drafted-ask block: *Moved to FM-002
  on 2026-09-26 … this tracker keeps its one ask, going public. The draft below is the record of the wording it took*.
  Its facts hold: the *go* of 10:25:41, and the worksheet path, which exists.
- **R5 ✓.**
  - *Passes* now names `evidence/triage/triage-2026-09-26.md`, and no double blank line is left in the file.
  - **FM-029**: *a ship-log line carried (FM-032's real-history relation case) and the acts' relation not shown*.
    The second is real. FM-029's *Done when* reads *Every place an answer is shown says the relation: `--answered`,
    and the promised action asks FM-030 puts on `--owner`, `--standup` and the board*. `shoalmark.py:1086` and the
    board's `:2320` print *promised {date}: {answer}* without `relation_text`.
  - **FM-030**'s three are *Done when* bullets, each unmet on the tip:
    - `--answered` (`:1064`) sends every answered open tracker to a seat, *→ act on it, then `… --clear-ask <id>
      <next move>`*, with no branch for an accepted action;
    - `--answer`'s last line (`:1570`) still says *it has left your queue*, and so does `docs/signing.md:219`;
    - the run/owner triage rule is unsplit (the first pass, check 6).
  - The *A check* bullet's clause *the triage prompt text carries the split* is unmet too. It follows from the third,
    so it is noted, not graded.
- **Nothing else.** The FM-002 hunks are the carry-over's AU-16 words, the Raised line and the *Done when* paragraph.
  The FM-006 hunk is the one bullet. The TRIAGE.md hunk is the paragraph, less one blank line.

## Findings

**R1 · P3 · confidence 99% on the facts, 75% on the grade · FM-006 still says in two places that the themes' work
waits on the going-public ask. The first pass's R2 is closed in the drafted-ask block only.**
- *The gap:*
  - `FM-006:24`, main's paragraph, which the merge kept whole, still says the drafted ask *waits for the going-public
    ask to be answered*. That is the sentence the first pass quoted. Two lines above it, the pass's line says *the
    themes' ask now stands on FM-002*. The section contradicts itself.
  - The slices bullet (`:219–220`) says *A pass judges the build … and it waits for the answer*, with no word that
    the slices are now FM-002's. FM-002's *What is true now* and its new *Done when* state them too, so the slices have
    two homes.
  - The evidence README (`evidence/FM-006/themes/README.md:164`), a record, says the same: *raised when FM-006's open
    ask (going public) is answered*.
- *Why it matters:* the risk is the one the first pass named. After he answers going public, a seat that reads the
  paragraph could raise the ask a second time, or build the slices from FM-006. Two things lower it: the new bullet
  sits right above the draft, and the section's first line, the one `--next` shows, is right.
- *What closes it:* the paragraph's sentence says the ask moved to FM-002 on 2026-09-26, and the slices bullet points
  to FM-002. Tracker-only; it can land with FM-006's next touch.

**R2 · P3 · confidence 99% on the facts, 70% on the grade · The raise's words are still outside the repository, and
the hashes cover the Principal's own framing. The first pass's R3a is closed by disclosure, not by filing.**
- *The gap:* each file holds more than his words:
  - a header line of the Principal's;
  - in the 09:23:58 and 10:25:41 files, the seat's normalised reading;
  - in the 10:25:41 file, the other session's pasted report.

  So nobody can rebuild `21497e4d…` or `416d54ce…` from his words or from the transcript, only from the file itself.
  *Reported for the Auditor seat's match* works only if the files reach it, and the line says neither where they are
  nor that they will be sent.
- *House practice:* FM-006's word of 11:05:27 is filed word for word, with its full hash, in *Going public*.
- *Why it matters:* the build's pass and its Reviewer read the tracker. Most of the substance is now in FM-002: the
  07:41:00 word's slices and carry-overs are lines there and in its *Done when*. What stays outside is the proof that
  the quotes are his.
- *What closes it:* the three words filed verbatim in an `evidence/FM-002/` file, beside the Principal's framing
  (which the hashes cover as they stand); or the line names where the files are kept for the match.

**R3 · P3 · confidence 99% on the facts, 60% on the grade · FM-002's *Done when* leaves the 0.8.0 paragraph unmarked,
and its contrast line is narrower than *What is true now*'s. The first pass's R1 is closed but for these two edges.**
- *The gap:*
  - `FM-002:38–39`, the 0.8.0 lines, stand unmarked above the new paragraph. The first pass's close named *the 0.8.0
    lines marked as met*.
  - The new contrast line reads *every text pair at 4.5:1 re-measured on the built files*. *What is true now* (`:21`)
    carries *on every pair in both schemes*. The renders line keeps *both schemes*.
- *Why it matters:* little. The new paragraph's label keeps a cold reader from taking the old lines as today's
  condition. But a build pass that tests the *Done when* alone could measure one scheme.
- *What closes it:* *(met, 0.8.0)* on the first paragraph, and *in both schemes* in the contrast line.

**R4 · P3 · confidence 99% on the fact, 70% on the grade · The first pass's R4 is open, and its only carry is
`3455f18`'s commit body.**
- *The gap:* no bug filing on any branch on origin. FM-035's line on a Shipped tracker is unchanged.
- *Why it matters:* a commit body is no more a queue than a Shipped tracker. The intent's *never* includes a fix that
  is forgotten.
- *What closes it:* the bug filing (the freeze admits it), or a line on FM-028, with FM-035's line pointing to it.
  It does not gate this merge.

**Noted, not graded.**
- FM-002 gains no ship-log row for its new *Done when*. Main's text-only fix-forwards (`93a790a`, `ceb0810`) add none
  either.
- The new FM-006 bullet is one 300-character line in a section wrapped at 120.
- Not this branch's: FM-006:216, main's text from PR 82, still says *v0.18.4 is not tagged*. It was tagged at 09:58.

## Verdict — READY WITH FINDINGS (R1–R4, all P3), 85%

**READY WITH FINDINGS.**
- The merge brings nothing of its own. It resolves two conflicts, both in FM-006, by keeping each side whole, the
  pass's line first and the pass's row under the home row. Against main, FM-006 gains exactly the pass's three lines,
  and main's 43 rows stand newest first.
- `--triage` applies nothing and names nothing superseded.
- The worksheet and FM-002's front matter are as the pass left them.
- Each fix in `3455f18` is the one its subject names, and no other byte moved. R1, R3b–d and R5 close their findings.
  R2 and R3a close them in part (R1, R2 here).
- TRIAGE.md's guarded sections are byte-identical to main's.
- `--check` and `--session-check` exit 0, both suites are green on both Pythons, and merge-tree is clean on `8725440`.
- Nothing here needs a re-make before the merge. R1 and R3 are due before FM-002's build pass; R2 whenever the
  Principal next files for FM-002; R4 with the bug filing.

*The Owner lands this by merging, and a merge rules nothing (path 5).*
