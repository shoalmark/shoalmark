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

## Re-check on af4644d (2026-09-28 02:26 CEST, the same seat)

**Scope.** A scoped re-check, not a new pass. `af4644d` (`af4644db4a5d0c65159542aeb8e341ef6ee73dff`, the Principal,
02:22:43, confirmed by `ls-remote`) is one tracker-only commit on `e7d16b8`. I read `git diff e7d16b8 af4644d`
whole: 22 lines in, 6 out, FM-040's file only.

**Gates.** The tool and both suites are still byte-identical to `origin/main` `bbbfc0b`, so no suite was run.
- `--check`: exit 0. *INDEX.md is up to date — 40 trackers*; *21 open … only bug filings*; the Owner's two sections
  guarded.
- `--session-check`: exit 0.
- `git merge-tree --write-tree origin/main HEAD`: clean (`9f4340c`).

**RV-681 — open in part.**
- **The hook steps: closed.** Checked against both files:
  - shoalmark's `lefthook.yml` line 22 is `tracker-board` under `post-merge:`, running `--html-only || true`. Its
    pre-commit `tracker-index` runs `--print-written` (line 10), and checkout is the plain hook.
  - PortDive's `lefthook.yml` (`origin/main`, read-only) runs `gen-tracker-index.py --print-written` at line 41,
    under `pre-commit:`. It runs `--html-only` at line 154, under `post-merge:`, and line 158, under
    `post-checkout:`.
  - `scripts/gen-tracker-index.py` line 9 runs `tools/shoalmark/shoalmark.py` through `subprocess.call`: the child
    process, as the text says.
  - The 27.82 s for the filing's own commit is hook output I cannot see.
- **The profile's scope: still open, P3.** Route a still reads *`cProfile` of `--html-only` on both repositories*.
  The commit's path, `--print-written`, is not in slice 1's plan, and that is the path of the 27.82 s, of PortDive's
  18.57 s, and of my verdict commit's 29.42 s. Fix forward: profile both commands.

**RV-682 — closed.** 01:42:26 (his word) and 01:44:16 (the start of the run) stand where *~01:40* and *01:4x* stood,
in the Why and in the first ship-log row. I take them as the Principal's claim from his transcript, which I cannot
read.

**RV-683 — closed.** *Held against (FM-035 and FM-039 by hand — `--related` does not return them)* is recorded.

**RV-684 — open in part.**
- **Route a: closed.** Its weighing now reads *"The Principal's counsel, disclosed as such: the cheaper route, …"*.
- **Route b: open, P3.** It still says *"A product decision, his, not a performance fix"*, and its price is still
  written past his words, with no counsel label. Fix forward: label it as counsel, or keep his words, when the ask is
  filed.

**The new paragraph, judged: it claims nothing as measured.**
- It is headed *Read, not measured*, gives *confidence about 55 % until profiled*, and calls its estimate *an
  unmeasured guess*.
- The one number that is a measurement, *0.4 s a file on a 3,755-commit repository*, is the tool's own docstring,
  cited as such.
- *137 verdicts this week* is `--check`'s own count.
- *~3,971 commits* is marked approximate; PortDive's `origin/main` counts 3,994 at `450c67ac`.
- *The profile itself did not run*, with the loads and the refusal, is a record of what did not happen.
- The second ship-log row matches my pass: *50.84 s real / 18.25 user / 29.50 sys at a 1-minute load of 150 falling to
  72*, and RV-681…684.

**RV-691 · P3 · confidence high — two imprecise pointers in the new paragraph.** (Numbered from RV-690, the highest id on either repository at 02:27. That is PortDive's `bug/327-sitting-one-corrections` at `9318ee1b`, read through the forge's compare API without a fetch; shoalmark's highest is RV-684. RV-685–690 are taken on PortDive.)
1. *"a seat's code reading of 2026-09-28 02:1x"* is an approximate time again, the kind RV-682 closed.
2. *"the docstring near line 996"* is at line 1012. It is `recover_relations`' docstring, about one `git log` per
   answer record, and not about `seat_problems`' per-ask pickaxe, which the sentence attaches it to. The pattern is
   alike, and the paragraph is marked as reading, so this is precision only.

Fix forward: the reading's exact time, and *line 1012, `recover_relations`' docstring, the same pattern per answer
record*.

**Re-check verdict:**
- RV-682 and RV-683 are closed.
- RV-681 and RV-684 are closed in part; their open halves are P3, fixed forward: the profile's scope covers
  `--print-written`, and route b's weighing is labelled or dropped.
- RV-691 is P3.
- The filing stays **READY WITH FINDINGS**.

The Owner lands this by merging; a merge rules nothing.

## Re-check on 170b7a5 (2026-09-28 02:36 CEST, the same seat)

**Scope.** `170b7a5` (`170b7a50a9353e55607605a2ac2c9daedcf184bf`, the Principal, 02:33:14, confirmed by `ls-remote`)
is one tracker-only commit on `fd43178`. I read `git diff fd43178 170b7a5` whole: FM-040's file only, 5 lines in and
4 out. Nothing moved beyond the four points and the new ship-log row.

**Gates.** The tool and both suites are still byte-identical to `origin/main` `bbbfc0b`, so no suite was run.
- `--check`: exit 0. *INDEX.md is up to date — 40 trackers*; *21 open … only bug filings*; the Owner's two sections
  guarded.
- `--session-check`: exit 0.
- `git merge-tree --write-tree origin/main HEAD`: clean (`668b118`).

**The findings:**
- **RV-681 — closed.** Route a now reads *`cProfile` of `--html-only` and of the commit's `--print-written` path on
  both repositories*.
- **RV-684 — closed.** Route b now reads *"The Principal's counsel, disclosed as such: a product decision, his, not a
  performance fix."* Both routes' weighing is labelled. His words stand apart in the quoted Why.
- **RV-691 — closed.** The reading is timed *reported 2026-09-28 02:03:03*, which I take as the Principal's transcript
  claim. The docstring is cited *at line 1012, in `recover_relations`*: the tool's text there, checked.
- **The new ship-log row** records the re-check `fd43178` and this fix, and matches both.

Nothing new is found, so nothing is minted.

**Verdict: READY WITH FINDINGS.** RV-681–684 and RV-691 are all closed. The docs tier takes no further pass.

The Owner lands this by merging; a merge rules nothing.
