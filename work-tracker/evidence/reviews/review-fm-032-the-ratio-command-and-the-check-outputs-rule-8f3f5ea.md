# Review — FM-032, the re-verification at 8f3f5ea (2026-09-30, Reviewer, session `8e509911/reviewer-59`)

Reviewed: 8f3f5eaaf378c01d990c46f05627b71ff4c833dd

- **Branch:** `fm/032-the-ratio-command-and-the-check-outputs-rule`, tip `8f3f5ea` = `origin/fm/032-…` (one `git fetch
  origin`, 10:56, no `--prune`); six commits on my verdict `13cdf7d` by the Implementer seat (`8e509911/implementer-59`,
  Sonnet 5.5): `186c589` merges `bd34852`, `8316a96` RV-726 and RV-727, `4ebb488` RV-728 (b)(c)(d), `5a812e9` RV-729,
  `aa561ab` and `c3e6f9f` the four numbers, `8f3f5ea` merges `2eb803b` (= `origin/main`). Both merges are clean:
  `git show --remerge-diff` prints nothing for either.
- **Tier: code**, the full loop's re-verification; the ids of the pass on `b52437a`, none new.
- **Independence: same session** — a sub-agent of Principal session 8e509911 (seat `reviewer-59`).
- **Verdict: READY WITH FINDINGS.** RV-726 (P2) and RV-727 are closed, each reproduced; RV-728 (b)(c)(d) and RV-729 (a)–(e)
  are closed. Open, both P3: RV-728 (a) — disclosed on FM-032, not applied at this tip; its commit is to follow this
  verdict — and one stale base in the page (RV-729 f).

## What I ran (all on `8f3f5ea`)

| run | result |
|---|---|
| `--ratio --since 2026-09-22 --until 2026-09-29`, 10:57:58–10:58:07 | exit 0; `trunk origin/main` (this clone's `origin/HEAD` names it); every day, the window and the eight sums byte-equal to `b52437a`'s output, which equalled my own numstat |
| the `--ratio` block of the tip's tests (lines 5433–5588) in my scratch harness, 10:58–10:59 | 14 ok on `8f3f5ea`'s tool; on `792dbca`'s, 10 FAIL and a crash |
| mutations of `8f3f5ea`'s tool | no `--first-parent`: 3 FAIL (the planted branch-with-its-own-merge among them); default window a day longer: 1 FAIL (*the seven Berlin days ending today*); `records` hard-wired to `work-tracker/`: 2 FAIL; `isinstance(value, str)` for the list test: the scalar check's `TypeError` stops the run; `trunk_ref()` alone: 1 FAIL (`origin/HEAD` → `origin/develop`). Each named in `8316a96`'s body |
| RV-726 reproduced again, a scratch repository with no `tracker_dir` key, `[ratio]` alone | the header says `records: docs/work-tracker/`; the merge reads `records +2 −0 product +1 −0 2.0:1` (was `+0 … +3 … 0.0:1`); with no `[ratio]` the refusal advises `records = ["docs/work-tracker/"]`, exit 2 |
| RV-727 (a) | `exclude = 5`, `= true`, `= "x/"`: one line on stderr each, exit 2, no traceback |
| `git diff --numstat origin/main...HEAD` (merge base `2eb803b`), 10:57:34 | **records +432 −33,529, product +536 −2, 0.8:1** — the page's four numbers; no binary, no rename |
| `--check`, 11:00:14–11:00:53 | exit 0 — *INDEX.md is up to date — 41 trackers*; *judged before build: on — 11 commit(s) … every build commit under a judged In Progress tracker*; *the Owner's two sections: guarded* |
| `--session-check` · `git merge-tree --write-tree origin/main HEAD` | exit 0 · clean against `2eb803b` (`756b418e`) |
| front matter · trailers | no line between the fences changes in `origin/main...HEAD`; the five fix commits carry `Session: 8e509911/implementer-59`, `Worktree: shoalmark-impl-4`, `Co-Authored-By: Claude Sonnet 5.5`, the merges `Session:` and `Worktree:` |
| `SHOALMARK_REGENERATE=1 python3` 3.14.3 `test_shoalmark.py` (11:53:27–12:12:43) | **568 ok / 0 FAIL**, *skipped here: 0 checks — every check ran*, exit 0; slice A's `checks.json` regenerated as **24 checks, none failing**, the start page's as 18 with the same three ids, `checks-r3-before.json` as 4 with the same 68 |
| `python3` 3.14.3 `test_core.py` (12:12:43–12:12:48) | **148 ok / 0 FAIL**, exit 0 |
| `/Library/Developer/CommandLineTools/usr/bin/python3.9` 3.9.6 `test_shoalmark.py` (12:12:48–12:28:28) | **565 ok / 0 FAIL**, exit 0; *skipped here: 3 check(s)* — the browser block, *SHOALMARK_REGENERATE=1 is not set* |
| the same 3.9.6 `test_core.py` (12:28:28–12:28:33) | **148 ok / 0 FAIL**, exit 0 |
| the guards | one runner at a time: other loops' suites held the machine and mine waited, 11:01–11:53; before each run the `pgrep` pattern printed nothing and the 1-minute load was 2.59, 2.54, 2.49, 2.52; HEAD `8f3f5ea`, the tree clean |

`--queue` was not run: it fetches `origin`, and this pass had one fetch.

## The findings, re-checked

**RV-726 · P2 — closed.** `ratio_defaults()` (shoalmark.py:4729) gives `records` = the configured `tracker_dir` with a
trailing slash; the refusal prints it with `json.dumps`; `CONFIG_KEYS`, `--schema` and README say *the tracker
directory*; `shoalmark.toml` keeps `records = ["work-tracker/"]` explicitly. Two new checks, and the reproduction above.

**RV-727 · P3 — closed.** (a) `ratio_paths` tests `isinstance(value, list)` and raises a `ValueError` that `ratio_cmd` prints
as one line, exit 2. (b) The trunk is `default_trunk(git) or trunk_ref()` — the resolution `--answer` and the gate already use
(`origin/HEAD`'s target, else `origin/main`, `origin/master`), with the file's own `git` lambda (as at :1151, :4297): better
than the fix I proposed, which wrote a second resolution. README and the refusal name the order. (c) The first-parent line
(a branch carrying its own `--no-ff` merge, that day `(1 merge)`, 15 lines once) and the default window (a merge dated
seven days back left out, one six days back in) are planted; the mutations above fail them.

**RV-728 · P3 — (b)(c)(d) closed, (a) open and disclosed.** (b) FM-032's *What stays* names the six `jev-*` exchange
files, the two `requests.json` (no committed check regenerates them; they stay until one does) and `demo.out` /
`demo-de.out` (fresh keys and times) with their reasons. (c) `_derive_board` counts the ten controls (contrast pipeline at
4.542 ± 0.01, the dialog open, the alt-text-removed tree reading figures and markers on three pages, both schemes); slice
A's block says 24; a planted check derives `(16, [])` and, with three controls broken, exactly their three ids — and my
`SHOALMARK_REGENERATE=1` run derived slice A's fresh output as 24 checks, none failing. (d) The start page's table reads
*checks · failing checks · failing texts* (`18 · 2 · 3`, `4 · 4 · 68`, *no verdict: 24 wrecks*), and the facts block says
`"wrecks": 24`; the key check requires one of `checks` or `wrecks`, never both. **(a) stays open:**
`jev-gate-test-score-output-2026-09-23.txt` is still in the tree, still regenerates byte for byte, and FM-032's section now
says so — *the ruling reaches it … not yet applied here*, the replacement and its check *the next change's*. Judged as it
stands: disclosed, not hidden; the fix text of my first pass stands.

**RV-729 · P3 — (a)–(e) closed, (f) open.** (a) *07:23:33, his ruling (2), in substance:*, not styled as a quotation; (b)
reflowed; (c) *Its day is the merge commit's committer date, in Europe/Berlin* and *a moved or renamed file counts as its
lines deleted and added*; (d) D1 *is not yet asked*; (e) *four check outputs of two folders (`073f21f` and `9d10d08`)*.
**(f), new in `aa561ab`:** the page's own-numbers paragraph says the range is *against `origin/main` at `bd34852`*; the tip
merged `2eb803b`, and at `bd34852` the three-dot range now reads records +456, product +558 (it takes in `2eb803b`'s
merge). The four numbers are right against `2eb803b`, the merge base. **Fix:** *(the three-dot range against `origin/main`;
its merge base is the last merge of main — `2eb803b` at this tip)*.

## The quality read, this round

The fix round meets this week's Opus builds: it reused `default_trunk` and the file's `git` lambda and `DEFAULTS` pattern
rather than writing the second resolution I proposed; each commit body says what was wrong, what changed, and the mutation
each new check kills (the five of `8316a96` confirmed above); and it disclosed the one item it could not do. Residue, not graded: each
fix commit's body repeats `Session: 8e509911/implementer-59` above its trailer block, the CHANGELOG bullet's added line runs
to 209 characters, and the regeneration check's own line still reads *18 checks, 3 failing* where the table now says
2 failing checks on 3 texts.

## Unproven here

CI (no pull request); Windows; a machine with no tz database. The Owner's decision on RV-728 (a).

## For the record

This file adds 87 record lines, no product line: after it the change reads records +519 −33,529, product +536 −2.

path 5 — a merge rules nothing.
