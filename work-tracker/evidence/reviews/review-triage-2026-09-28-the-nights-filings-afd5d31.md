# Re-check — the pass of the night's filings, at afd5d31 (2026-09-28 07:55 CEST, Reviewer, session `8e509911/reviewer-45`)

- **Scope.** `afd5d31` (`afd5d31bf3d17500fc18d416268cd90ddfba5c93`, the Principal, 07:51:44; `git ls-remote` showed it
  after my fetch) is one tracker-only commit on my verdict `49d1575`. `git diff 49d1575 afd5d31` changes 3 lines in
  3 files: FM-027's raise, FM-031's RV-679 line, and FM-027's row in `evidence/triage/triage-2026-09-28.md`. Nothing
  else moved; my first review file is untouched.
- **Tier: docs — a scoped re-check.** `git diff 49d1575 afd5d31 -- shoalmark.py test_*.py lefthook.yml scripts/` is
  empty. The tool, suites and hook are still main's, so no suite was run.
- **Independence:** same session — a sub-agent of 8e509911, reported.
- **Verdict: READY.** RV-720 and RV-721 are closed, the note on FM-027's two times is taken, and there is nothing
  new. No id was minted.

## Gates

| run | result |
|---|---|
| `--check` on `afd5d31` | exit 0. *INDEX.md is up to date — 40 trackers*; *judged before build: on — 6 commit(s) … every build commit under a judged In Progress tracker*; *the Owner's two sections: guarded — … none changes them or his signers file*; *filing freeze: 21 open, at or above 8 — only bug filings* |
| `--session-check` | exit 0 |
| `git merge-tree --write-tree origin/main afd5d31` | clean (`b250835`) |
| `git diff --check` | clean against `origin/main` and against `49d1575` |
| `--queue` (the scratch clone, at `afd5d31`) | `branch tracker/triage-2026-09-28-the-n… @ afd5d31  wait: no pull request — no verdict on afd5d31`, and *1 waiting on you: 0 merge, 0 close, 0 wait, 1 pushed without a pull request* |

## The closures

**RV-720 — closed.** The parenthetical now reads *"(PortDive `answer/bug-327`: his `--done` c502c7a4 at 2026-09-27
20:21:18, the verdict 66884f5f at 20:45:02)"*. I checked both against the objects in PortDive, read-only:
- `c502c7a4` has author and committer dates of 2026-09-27 20:21:18 +0200, `%G?` G, holgo99;
- `66884f5f` has author and committer dates of 2026-09-27 20:45:02 +0200, Reviewer seat.

Neither 20:52:39 nor the queue run is left in the line. The rest of the line is unchanged and still true against the
code, as the first pass found.

**RV-721 — closed.** FM-027's *keep test* cell now reads *"2026-09-28 · keep · by hand — Parked since 2026-09-24, owed
no pass; the raise of 2026-09-28 under ## Raised names no signed rule"*, the words my file gave.
- I compared the two FM rows cell by cell at `49d1575` and `afd5d31`. Each row still has 10 cells.
- The Verdict and Reason cells are byte-identical: FM-040 *keep P2 #4 build*, FM-027 *keep P3 owner*.
- Every other cell except FM-027's keep test is byte-identical too.
- The tool still reads the raise the same way: `raise_lines` gives date `2026-09-28` and undermines `['no signed rule
  (none names review ids)']`, `mark_raised` gives `[]`, and `owed_a_pass` is False.

**The note — taken.** FM-027's raise now puts `e7d16b8` (02:00:26) and `97fa9ada` (02:06:06) each beside its own
time, and both times match the commit dates. *"Six minutes apart"* is left with the briefs, as before. *"The same
evening"* is unchanged, and it stays a note.

## Verdict

**READY.**

The Owner lands this by merging; a merge rules nothing.
