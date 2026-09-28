# Re-check — FM-041 filed and FM-024's fold, at 3af1428 (2026-09-28 09:44 CEST, Reviewer, session `8e509911/reviewer-45`)

- **Scope.** `3af1428` (`3af1428e5130e73eb14536c1c567a917fc9bfd3e`, the Principal, 09:38:48; `git ls-remote` showed it
  after my fetch) is one tracker-only commit on my verdict `38dc205`. `git diff 38dc205 3af1428` changes 2 files:
  - FM-041's tier sentence, 1 line out and 2 in;
  - FM-024's *Folded* row, taken out at the table's head and put in at its end.

  My first review file is untouched.
- **Tier: docs — a scoped re-check.** `git diff origin/main 3af1428 -- shoalmark.py test_*.py lefthook.yml scripts/` is
  empty, so no suite was run.
- **Independence:** same session — a sub-agent of 8e509911, reported.
- **Verdict: READY.** RV-724 and RV-725 are closed and there is nothing new. No id was minted.

## Gates

| run | result |
|---|---|
| `--check` on `3af1428` | exit 0. *INDEX.md is up to date — 41 trackers*; *judged before build: on — … every build commit under a judged In Progress tracker*; *the Owner's two sections: guarded*; *filing freeze: 22 open, at or above 8 — only bug filings* |
| `--session-check` | exit 0 |
| `git merge-tree --write-tree origin/main 3af1428` | clean. Its tree `6fe2c3b` is the branch's own, so the merge is a fast-forward onto `eb00e96`. `git diff --check` is clean |
| `--queue` (the scratch clone, at `3af1428`) | `branch fm/041-the-board-places-a-ranke… @ 3af1428  wait: no pull request — no verdict on 3af1428`, among 4 branches pushed without a pull request |

## The closures

**RV-724 — closed (confidence 85 %).** The tier now reads *"code, not critical (no queue reader, no gate touched):
AGENTS.md's code loop — NOT READY on any P2 until READY, same-session Reviewers; the Auditor counselled one pass, and a
clean first pass is where the loop ends"*.
- That matches AGENTS.md: *"Code keeps the full loop: pass, fix, verify, until READY."*
- *Same-session Reviewers* is path 3's *inline Reviewer passes on other code*.
- The Auditor's one pass now stands as counsel, and only a clean pass ends the loop. So the record no longer puts the
  build on the docs tier.

**RV-725 — closed.** FM-024's 2026-09-28 *Folded* row is now the last row of the ship log, after *"The row of 20:24 above
was edited in place …"*. It is byte-identical to the row taken out, and it appears once.

## Verdict

**READY.**

The Owner lands this by merging; a merge rules nothing.
