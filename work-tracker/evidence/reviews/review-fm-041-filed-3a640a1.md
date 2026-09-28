# Review — FM-041 filed and FM-024's fold, at 3a640a1 (2026-09-28 09:36 CEST, Reviewer, session `8e509911/reviewer-45`)

- **Branch:** `fm/041-the-board-places-a-ranked-proposed-tracker-in-the-backlog`, tip `3a640a1`
  (`3a640a1819366aa68ba2e6685e3e7a7811a52eb1`, confirmed by `git ls-remote`). It is one Principal commit (`principal@seat`,
  `Session: 8e509911`, `Worktree: shoalmark-principal-4`, 09:20:20) on `origin/main` `eb00e96`, and it touches three
  files:
  - FM-041, new;
  - FM-024: a new `## Raised` section and a ship-log row;
  - INDEX.md, one new row and the count 40 → 41.
- **Tier: docs, one pass.** `git diff origin/main 3a640a1 -- shoalmark.py test_*.py lefthook.yml scripts/` is empty.
  The tool, suites and hook are main's, so no suite was run.
- **Independence:** same session — a sub-agent of 8e509911, reported.
- **Verdict: READY WITH FINDINGS.** There are two P3s, RV-724 and RV-725, from the range the Principal allocated.

## What I ran

| run | result |
|---|---|
| the paste | `owner-auditor-two-board-findings-paste.md` (the Principal's copy) hashes to `a375a843…18ac`, the sha256 both records cite. It has four lines: the *To: 8e509911* header, a lead line, point 1 and point 2. All four stand verbatim, lines 4–7, in the Owner's message of `2026-09-28T07:01:54.897Z` in the Principal's transcript (09:01:54 CEST, the time both records give). The lead line is quoted in neither record, and neither says it is |
| FM-041's quote | ✓ It is point 1 with its `1. ` removed, character for character, where the file's soft wraps are read as spaces (as Markdown renders them). *"four lines, saved word for word, sha256 …"* describes the saved copy, and *"The Auditor's line, word for word"* is the one line quoted |
| FM-024's quote | ✓ It is point 2 with its `2. ` removed, character for character, and it is marked *"its point 2 quoted here"* |
| the code claim, at `eb00e96b` | ✓ `board()` (739–747) returns `"progress" if t["status"] == "In Progress" else "backlog"` after its *done* and *triage* rules, so a ranked Proposed tracker (it carries `triaged:`) is *backlog*. `desc.progress` (2488) reads *"kept by triage — by rank, then tier"*. The Auditor's `:734` is that same `return` in PortDive's vendored 0.18.5. PortDive's INDEX at `8bdf1d18` ranks BUG-328 #3, PD-402 #4 and PD-401 #10, all Proposed |
| the filing under the freeze | ✓ `tags: bug`. `--check` reads *filing freeze: 22 open, at or above 8 — only bug filings* (21 before). FM-041 is a new filing on the board (`board` → *triage*, `is_new_filing` True), and its hook is 104 characters |
| `--related` on the title | FM-036 (3.3, Shipped), FM-002 (1.6, Shipped) and FM-021 (1.3, Shipped), then FM-033, the four in `considered:`. **Judgement: a filing was right (confidence 80 %).** The three Shipped ones are closed work: a worksheet's double rows, the brand, and the empty section's caption. FM-033 (In Progress, rank 10) is the nearest open one. Its *"`progress` lists only judged trackers"* is part of its diagnosis, but its scope is the judged-before-build rule. A slice there would put a placement fix under a build gate's tracker |
| FM-024's raise, `raise_lines` | Imported in a scratch clone at `3a640a1`: date `2026-09-28`, undermines `['no signed rule — a design line for the slice']`, and `mark_raised` gives `[]`. It is folded into the slice his signed answer of 08:11:26 (`4127dba`) opened |
| `--check` on `3a640a1` | exit 0. *INDEX.md is up to date — 41 trackers*; *judged before build: on — … every build commit under a judged In Progress tracker*; *the Owner's two sections: guarded* |
| `--session-check` | exit 0 |
| `git merge-tree --write-tree origin/main 3a640a1` | clean. Its tree `d26d910` is the branch's own, so the merge is a fast-forward. `git diff --check` is clean |
| `--queue` (the scratch clone, at `3a640a1`) | `branch fm/041-the-board-places-a-ranke… @ 3a640a1  wait: no pull request — no verdict on 3a640a1`, beside FM-030's two branches; *3 waiting on you: 0 merge, 0 close, 0 wait, 3 pushed without a pull request* |

## Findings

**RV-724 · P3 · confidence 85 % — FM-041 names one Reviewer pass for a code change.** Its design says *"Tier: the board's
placement and INDEX.md — code, not critical (no queue reader, no gate touched); one Reviewer pass, as the Auditor
counsels."*
- The fix changes `board()` in `shoalmark.py`, and its Done-when asks for a suite check.
- AGENTS.md's tier rule (FM-032 S1): *"Code keeps the full loop: pass, fix, verify, until READY."*
- Path 3 gives other code *"inline Reviewer passes"*. One Reviewer pass is the docs tier.

The Auditor's counsel may be quoted, but the record adopts it as the tier. A seat that builds from this line would
review code by the docs rule.

**Fix forward:** *"Tier: code, not critical — the full loop (AGENTS.md), inline Reviewer passes under path 3; the Auditor
counsels one pass because `board()` also writes INDEX.md."*

**RV-725 · P3 · confidence 70 % — FM-024's new ship-log row sits at the table's head, while the table's rows since
2026-09-24 are appended at its end.**
- FM-024's ship log runs 2026-09-23 newest first.
- Then its three 2026-09-24 rows are appended below, the last saying *"from here, a correction is an appended row"*.
- The 2026-09-28 *Folded* row went in above the 2026-09-23 rows. A reader looking for the newest event at the end, where
  the last three went, misses it.

This is the placement RV-722 fixed on FM-030 this morning.

**Fix forward:** move the row to the end, after *"The row of 20:24 above was edited in place …"*.

**Not findings:**
- The lead line of the four-line paste is saved and hashed but not quoted. Both records say which point they quote,
  so a reader knows what the hash covers.
- The commit body's *"filed word for word (four lines …)"* is a commit message, not the record.

## Verdict

**READY WITH FINDINGS.** RV-724 and RV-725 are P3, to be fixed forward. The docs tier takes no re-pass.

The Owner lands this by merging; a merge rules nothing.
