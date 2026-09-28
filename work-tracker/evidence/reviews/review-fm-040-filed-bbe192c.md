# Review — FM-040 filed at bbe192c (2026-09-28 02:00 CEST, Reviewer, session `8e509911/reviewer-40`)

- **Branch:** `fm/040-the-hook-regenerates-the-board-in-26-seconds`, tip `bbe192c`
  (`bbe192cc05bf9681cfc6edac2e31a2a2d3c0c28e`, confirmed by `git ls-remote`). It is one Principal commit
  (`principal@seat`, `Session: 8e509911`, `Worktree: shoalmark-principal-4`, 01:52:44) on `origin/main` `bbbfc0b`. It
  adds `work-tracker/FM-040-…md` and a regenerated `INDEX.md`.
- **Tier: docs, one pass.** `git diff origin/main bbe192c -- shoalmark.py test_shoalmark.py test_core.py` is empty:
  the tool and both suites are byte-identical to main's, so no suite was run.
- **Independence:** same session — a sub-agent of 8e509911, reported.
- **Verdict: READY WITH FINDINGS.** Four P3s, RV-681–RV-684. They are numbered from the highest RV I saw: RV-680, on
  PortDive's origin refs at 01:59. Its live heads, by `ls-remote`, match the local refs, and shoalmark's highest is
  RV-630.

## What I ran

| run | result |
|---|---|
| `--new FM "<the title>" --tags bug` in a scratch copy of `bbbfc0b` (`git archive`) | it writes `FM-040-the-hook-s-board-regeneration-takes-26-s-on-shoalmark-and-15.md`, the same file name as the branch's. Its front matter is `id: FM-040`, `status: Proposed`, `considered:` (empty), `tags: bug`, and a `hook:` equal to the title. The filed front matter differs only in `considered:`, filled by hand. The body sections are the template's, filled in. No other origin ref carries an FM-040 |
| `--check` | exit 0. *INDEX.md is up to date — 40 trackers*; *filing freeze: 21 open, at or above 8 — only bug filings*. FM-040 carries `bug`, the freeze tag, so the freeze lets it through. *the Owner's two sections: guarded — 1 commit(s) … none changes them* |
| `--related "<the title>"` | FM-040 itself, then FM-018 3.8, FM-023 1.3, FM-034 1.3, FM-025 0.9, FM-027 0.8, FM-029 0.8, FM-024 0.7. `considered:` holds FM-018, FM-025 and FM-034, which are returned, and FM-035 and FM-039, which are not: RV-683 |
| `/usr/bin/time -p python3 shoalmark.py` in this worktree at `bbe192c` (40 trackers), once | **real 50.84 s, user 18.25 s, sys 29.50 s.** The 1-minute load was **150.02** at the start and **72.24** at the end; it was 206.85 three minutes before. The tree is clean after. The wall time is inflated by that load, and the CPU split matches the filing's claim: system time exceeds user time, as in its 42.7 / 16.8 / 24.3 on `bbbfc0b` |
| PortDive, read-only (`origin/main` `450c67ac`) | `tools/shoalmark/PIN` reads *0.18.5 · tag v0.18.5*; `INDEX.md` reads *507 trackers*; `scripts/gen-tracker-index.py` exists; `lefthook.yml` has `tracker-index` (`--print-written`, pre-commit) and `tracker-dashboard` (`--html-only`) |
| the hooks in this clone | `post-checkout`, a plain shoalmark hook: `--html-only`. `post-merge`, lefthook `tracker-board`: `--html-only`. `pre-commit`, lefthook `tracker-index`: `--print-written`, when a `work-tracker/*.md` is staged. See RV-681 |
| `--session-check` | exit 0 |
| `git merge-tree --write-tree origin/main HEAD` | clean (`f9b7c44`) |

**What this pass cannot see.** The Owner's 25.88 s and 14.48 s, and PortDive's 18.57 s at 01:47, are quoted from hook
output that the Reviewer cannot see. The 42.7 s run is the Principal's claim; mine above is the check on its shape. His
words come from a chat I cannot read. I judged the normalisation for form only: the quote is marked *(spelling
normalised, marked)* before it and *(normalised)* after, and it stands apart from the seat's text.

**No option or default is put to him.** The front matter has no `ask:`, `ask-options:`, `ask-proposal:` or `next:`. The
body says *the two routes, the Owner's, for his ruling once the profile is in*, and *the route after it is an ask to the
Owner, rowed first in the ledger, with the profile's numbers as its input and no default*. Slice 1, the profile, is
said to need no ruling.

## Findings

**RV-681 · P3 · confidence high — the filing names the wrong hook step, and the profile misses the commit's path.**
*"the hook runs `python3 shoalmark.py --html-only` on every checkout and commit (`lefthook.yml`, `tracker-board`)"* is
not what this repository runs:
- `tracker-board` is lefthook's **post-merge** step, `--html-only`. His 25.88 s summary is its line.
- A checkout runs the plain **post-checkout** hook, `--html-only`, which is not in `lefthook.yml`.
- A commit runs the pre-commit **`tracker-index`**, `--print-written`, and only when a tracker is staged.

PortDive's 18.57 s is also `tracker-index`, `--print-written`. Route a and Done-when profile `--html-only` only.

**Fix forward:** name the three steps as above, and profile `--print-written` beside `--html-only` on both
repositories.

**RV-682 · P3 · confidence high — two times are approximate.** *"the Owner's word of 2026-09-28 ~01:40"* and the
ship log's *"at 01:4x"* should read his message's exact time from the transcript, and the run's. The record corrected
FM-030's *13:3x* to 13:33:29, the time of his message, on the same ground (the pass's R8 on `647da17`).

**RV-683 · P3 · confidence high — two ids in `considered:` are not returned by `--related`.** FM-035 and FM-039 were
held from the seat's knowledge; `--related` on the title does not return them. The holding is sound: both are the 5 s
Chrome budget, not the regeneration. FM-023, FM-027, FM-029 and FM-024, which `--related` does return, are rightly
not held. Recorded as the rule asks; no change is needed beyond saying so if the filing is touched.

**RV-684 · P3 · confidence medium — the routes carry the seat's weighing.**
- Route a is called *"The cheap route; it keeps the single Python file every consumer vendors"*.
- Route b is called *"A product decision, his, not a performance fix"*, and its price is extended past his words:
  *"a build per platform, … the pin and the vendoring redone"*.

Nothing here is put to him as a default. When the ask is filed after the profile, keep the options in his words, and
state the weighing as the seat's counsel, disclosed, as PortDive's FEAT-187 ask disclosed its proposal as the Auditor
seat's counsel.

## Verdict

**READY WITH FINDINGS.** RV-681–RV-684 are P3, fixed forward in the next change on FM-040. The docs tier takes no
re-pass.

The Owner lands this by merging; a merge rules nothing.
