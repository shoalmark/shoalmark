# Review — FM-040, the Auditor's measurement filed, at ed0768a (2026-09-28 05:33 CEST, Reviewer, session `8e509911/reviewer-40`)

- **Branch:** `fm/040-the-auditors-measurement-568-git-calls`, tip `ed0768a` (`ed0768a0f198f5ed8036e02845969fbfcf4cda12`,
  confirmed by `git ls-remote`). It is one Principal commit (`principal@seat`, `Session: 8e509911`,
  `Worktree: shoalmark-principal-4`, 05:28:02) on `origin/main` `24c26f27`, FM-039 merged. It changes FM-040's file
  only.
- **Tier: docs, one pass.** `git diff origin/main ed0768a -- shoalmark.py test_shoalmark.py test_core.py` is empty:
  the tool and both suites are main's, so no suite was run.
- **Independence:** same session — a sub-agent of 8e509911, reported.
- **Verdict: READY WITH FINDINGS.** Two P3s, RV-694 and RV-695. They are numbered from the highest id I saw at 05:31.
  That is RV-693 on shoalmark (my own, FM-039); PortDive's `main` `7d30ae5b` reads RV-692 at most, through the
  forge's compare API with no fetch.

## What I ran

| run | result |
|---|---|
| `shasum -a 256` of the paste file `auditor-fm040-measurement-paste.md` (the Principal's copy of the Owner's relay: I cannot see his chat, and the Auditor's folder is sealed and was not read) | `a6cb201bc20cfb7f64503ddddcf4d670a1efa098969e99bcc8b1f764fe4d7ebe`: the sha256 the body cites |
| the quoted block against the paste, the `> ` prefix removed | 6 lines against 6; every line is equal, and the joined block is byte-equal to the file, its last newline included. The block's own sha256 is the same |
| `considered:` | it gained FM-012 and FM-024; both exist. `git log -1 294a368`: *"FM-024 S6: each verdict reported — independent or same session — from its Reviewed: trailer and the reviewed range's sessions"*. Its diff adds `verdict_reports`, and `v0.17.6` is the first tag that contains it. So FM-024 S6 is where the cost comes from, as point 3 says. `--related` on the title returns FM-024 (0.7) and not FM-012: RV-695 |
| the seat's earlier reading | kept, headed *"Superseded by the Auditor's measurement below … — kept as the record of a reading that was wrong"*, and it names what the profile puts where instead: 92–96 % in `board_sessions → verdict_reports`. Its old text follows unchanged |
| the fix and the ask, against the Auditor's points 4 and 5 | slice (a) *"the pre-commit's `--print-written` writes INDEX.md without building the HTML board"* is point 4(a). Slice (b) *"`verdict_reports` cached per verdict sha under `.git/` or read in one batched `git` call"* is point 4(b). *"hook code — the full loop, a cold Reviewer"* is its *"Hook code, so the full loop"*. *"Route b is not this bug's … not asked here. The route ask this tracker foresaw is therefore not filed"* is point 4's last two sentences and point 5. No option or default is put to the Owner: the front matter has no `ask:`, `ask-options:`, `ask-proposal:` or `next: owner`. But two older lines still say the ask comes: RV-694 |
| Done-when | *"… run in a wall-clock time the Owner sets or accepts — proposed by the build with its own measurement, before and after, at a stated load — and the board it writes is byte-identical to today's"*. The number is still his; none is set here |
| the ship log | the new row is last (oldest first). It names the measurement's time and load, his relay at 05:24:00, the hash's head, the struck reading, the two added ids, the two slices and the ask not filed |
| `--check` | exit 0. *INDEX.md is up to date — 40 trackers*; *filing freeze: 21 open … only bug filings*; the Owner's two sections guarded |
| `--session-check` | exit 0 |
| `git merge-tree --write-tree origin/main HEAD` | clean (`0435fc3`) |

## Findings

**RV-694 · P3 · confidence high — two older lines still say the route ask is coming, beside the clause that says it
is not filed.**
- The routes' heading still reads *"**The two routes, the Owner's, for his ruling once the profile is in:**"*.
- The paragraph directly after the new clause still reads *"… the route after it is an ask to the Owner, rowed first
  in the ledger, with the profile's numbers as its input and no default."*

The new bold clause, the Done-when and the ship log all say the ask is not filed. A seat that reads the paragraph
could file the ask this commit withdrew. The Owner, reading it, could expect an ask that will not come.

**Fix forward:** put both in the past, for example *"were held for his ruling once the profile was in; the measurement
answered route a, and route b is his separate product question"*. Strike the sentence *"the route after it is an ask
…"*, as the reading was struck.

**RV-695 · P3 · confidence high — FM-012 is held by hand and not said so.** `--related` on the title returns FM-024
and not FM-012, which was added on the Auditor's point 3. The *Held against* line names neither addition. Its
by-hand note, RV-683's closure, still names only FM-035 and FM-039.

**Fix forward:** add FM-012 (*the same kind of cost, its batching fix*, point 3) and FM-024 S6 to *Held against*, with
FM-012 marked as held by hand.

## Verdict

**READY WITH FINDINGS.** RV-694 and RV-695 are P3, fixed forward in the next change on FM-040. The docs tier takes no
re-pass.

The Owner lands this by merging; a merge rules nothing.

## Re-check on 006e8c8 (2026-09-28 05:39 CEST, the same seat)

**Scope.** `006e8c8` (`006e8c855340dbcafe26ec4fd7b0d1c32fb97123`, the Principal, 05:37:08, confirmed by `ls-remote`)
is one tracker-only commit on `cb17819`. I read `git diff cb17819 006e8c8` whole: FM-040's file only, 7 lines in
and 5 out, in four places — the *Held against* line, the routes' heading, the closing paragraph, and a new ship-log
row, last. Nothing else moved. The quoted block still hashes to `a6cb201b…`.

**Gates.** The tool and both suites are still byte-identical to `origin/main` `24c26f27`, so no suite was run.
- `--check`: exit 0. *INDEX.md is up to date — 40 trackers*; the Owner's two sections guarded.
- `--session-check`: exit 0.
- `git merge-tree --write-tree origin/main HEAD`: clean (`c39ea21`).

**RV-694 — closed.** Neither line announces a route ask any more:
- the heading reads *"The two routes, the Owner's, as they stood before the profile (the measurement below chose
  route a for this bug; route b stays his separate question)"*;
- the closing paragraph reads *"the route ask it foresaw is not filed — the measurement chose (see the clause above),
  and the Rust port remains the Owner's separate product question, asked on its own tracker if he wants it tracked"*.

Both agree with the clause and the Done-when. No option or default is put to him.

**RV-695 — closed.** *Held against* now opens *"(FM-035, FM-039 and FM-012 by hand — `--related` does not return
them; FM-024 on the Auditor's word)"*. It names what each was held for: FM-012 *"the same kind of cost — its
batching fix — a design, not this bug's time"*, and FM-024 *"S6, `294a368`, v0.17.6 — where `verdict_reports` and its
cost came from"*.

Nothing new is found, so nothing is minted.

**Verdict: READY WITH FINDINGS.** RV-694 and RV-695 are closed; the docs tier takes no further pass.

The Owner lands this by merging; a merge rules nothing.
