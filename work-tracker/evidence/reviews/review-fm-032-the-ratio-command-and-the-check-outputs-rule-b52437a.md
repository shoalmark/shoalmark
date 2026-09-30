# Review — FM-032, `--ratio` and the check-output ruling, at b52437a (2026-09-30, Reviewer, session `8e509911/reviewer-59`)

Reviewed: b52437a7b925e64cdd65b6f49eda862d92aeb41b

- **Branch:** `fm/032-the-ratio-command-and-the-check-outputs-rule`, tip `b52437a` = `origin/fm/032-…` (my two `git fetch
  origin`, 08:43:20 and 08:44:38, no `--prune`), five commits on the base `792dbca` by the Implementer seat
  (`8e509911/implementer-58`, Sonnet 5.5), 07:36:35–07:52:53: `991f978` the page and FM-032's section, `3deafb9` `--ratio`,
  `c819cde` four outputs replaced by summaries, `c3d56ec` the regeneration check, `b52437a` the change's own numbers. No
  pull request. `origin/main` moved to `ffeb2e6` at 08:47 (another worktree's fetch — refs are shared; six commits of
  FM-024 and FM-006, no code; FM-006's tracker and `INDEX.md` changed on both sides, and they merge clean); the merge
  base is still `792dbca`.
- **Tier: code** — `git diff --name-only origin/main...HEAD` names `shoalmark.py`, `test_shoalmark.py` and
  `shoalmark.toml`. The full loop.
- **Independence: same session** — a sub-agent of Principal session 8e509911 (seat `reviewer-59`).
- **Verdict: NOT READY.** The numbers are right: my own first-parent numstat equals `--ratio` on every line of the shadow
  week, the change's four numbers equal my count, every new `--ratio` check fails on `origin/main`'s tool, the four
  replaced outputs' hashes and holding commits verify, and `facts.mjs` and the browser checks regenerate the READMEs'
  results. One P2 sends it back: `[ratio]`'s default and the refusal's own advice count a repository's records as product
  wherever the tracker is not at `work-tracker/` — the tool's own default layout included (RV-726). Three P3s beside it.

## What I ran

| run | result |
|---|---|
| setup | `git status --short` clean; 08:43:24 `git switch` refused (the branch held by `shoalmark-impl-4`), reported; the Principal detached it at 08:44; 08:44:38 the second fetch, switch, HEAD = `b52437a…`, `seat.session` = `8e509911/reviewer-59` |
| my own numstat (`mycount.py` in the Reviewer's scratch folder), 08:47:24 | `git rev-list --first-parent --merges origin/main`, `git diff --numstat M^1 M` per merge, `work-tracker/` = records, mode `160000` from `--raw` dropped, `-` = a binary, 0 lines, the committer time in `Europe/Berlin` (`zoneinfo`); run twice, `--no-renames` and `-M` |
| `python3 shoalmark.py --ratio --since 2026-09-22 --until 2026-09-29`, 08:47 | exit 0; **equal to mine on all 17 lines** — the eight days' four numbers, merges and binaries, the window (records +65,711 −972, product +15,713 −1,764, 4.2:1, 111 merges, 190 binary) and the eight seven-day sums (the 22nd's reaches back to the 16th: 13 merges). `-M` changes nothing: no merge on the trunk's first-parent line has ever carried a rename (116 merges read, to `ffeb2e6`), and no path is a submodule |
| the new `--ratio` checks against `origin/main`'s tool, 08:51:32–08:51:45 | a harness in scratch: the tip's test header, `fm` loaded from `git show 792dbca:shoalmark.py`, then the tip's `--ratio` block (lines 5433–5519), an unknown flag a failed check. **8 of 8 FAIL on `792dbca`'s tool, 8 of 8 ok on `b52437a`'s** |
| mutations of the tip's tool, the same harness, 08:52 | no `--first-parent`: only the reproduction on this repository fails (CI skips it); the default window one day longer: **every check ok**; `-M` for `--no-renames`: the planted a.md → b.md pair is read as a rename and `ratio_merge` crashes (pinned, by chance); no thousands separator: only the reproduction fails; `exclude` ignored: 3 FAIL |
| `--ratio` edges, a scratch repository | no tz database simulated (`ratio_zone` → `(None, False)`): the header says *NOT: no time zone database here, so each day is the merge's own UTC offset*, exit 0; `records = 5` and `records = true`: a `TypeError` traceback, exit 1; `records = [""]`: the message, exit 1; `--since 2026-9-1`: *days, YYYY-MM-DD*, exit 2; no `[ratio]`: the message, exit 2; no `tracker_dir` key (the default `docs/work-tracker`) and `[ratio]` alone: RV-726 |
| `sha256` of the deleted outputs, `git show <commit>:<path> \| shasum -a 256` | all four equal the READMEs' (`92ab6696…`, `02122dec…`, `6726f85d…`, `b76a1d93…`); each the file's bytes, not git's blob id (`281da087…`, `243f5254…`, `4cd3c576…`, `08877e72…`); each file's only commit is the named one, and `792dbca` holds the same bytes |
| the originals, derived by the test's own `_derive_board` / `_derive_landing` | slice A's `checks.json` (14, []) with 746/746 measured, 29 and 31 pairs, AU-18 99 of 99.8 on 56 lines — the README's *original* row; the start page's `checks.json` (18, the three ids of the block) and `checks-r3-before.json` (4, the 68 ids of the block, equal as sorted lists) |
| `node facts.mjs bef2a1e …/landing/index.html` (v26.7.0), 08:49:02–08:49:06 | exit 0; every field equal to `08798a8`'s `facts.json` but `read`; the fingerprint equals the README's block: `sha` `bef2a1e2…`, release 0.18.4, counts 5/3/15/1, 24 wrecks, `sha256_without_read` `0ed4effe…` |
| `jev-gate-test-score.py run1 run2`, from its folder | exit 0; **byte-identical** to the committed `jev-gate-test-score-output-2026-09-23.txt` (RV-728) |
| greps (the brief's point 1) | other projects' paths in the diff's **added** lines: one, `docs/work-tracker` — the tool's own default `tracker_dir`, already in the same README row on `792dbca`; the rest are context or the deleted files' lines. Relay citations in added lines: none — the `sha256` hits are the deleted files' hashes and the facts fingerprint; no *paste*, no *Auditor* |
| front matter | `git diff origin/main...HEAD -- 'work-tracker/FM-*.md'` changes no line between the fences |
| `python3 shoalmark.py --check`, 08:53:52–08:54:30 | exit 0 — *INDEX.md is up to date — 41 trackers*; *judged before build: on — 5 commit(s) … every build commit under a judged In Progress tracker*; *the Owner's two sections: guarded*; *filing freeze: 22 open* |
| `--session-check` | exit 0 |
| `git merge-tree --write-tree`, 08:54:49 | against `792dbca`: clean (`dfe1e5a5`); against `origin/main` = `ffeb2e6`: clean (`df34a56d`) |
| `--queue`, 08:55:04–08:55:13 (its own fetch of `origin`, no `--prune`) | exit 0 — `branch fm/032-the-ratio-command-and-th… @ b52437a  wait: no pull request — no verdict on b52437a` |
| `SHOALMARK_REGENERATE=1 python3` 3.14.3 `test_shoalmark.py` (08:55:24–09:15:17, 1,193 s) | **561 ok / 0 FAIL**, *skipped here: 0 checks — every check ran*, exit 0 — the 14 FM-032 checks among them: the eight `--ratio` checks; the summary blocks; the derivation; `facts.mjs bef2a1e` (the block's fields and `sha256_without_read` equal); **the start page's `checks.json` (18, the same three ids), `checks-r3-before.json` (4, the same 68 ids) and slice A's `checks.json` (14, []) regenerated in Chrome 154.0.8037.58 with `uvx zensical@0.0.65`** |
| `python3` 3.14.3 `test_core.py` (09:15:34–09:15:40) | **148 ok / 0 FAIL**, exit 0 |
| `/Library/Developer/CommandLineTools/usr/bin/python3.9` 3.9.6 `test_shoalmark.py` (09:15:49–09:31:36, 947 s) | **558 ok / 0 FAIL**, exit 0 — the eight `--ratio` checks, the blocks, the derivation and `facts.mjs` ran; *skipped here: 3 check(s) in 1 block(s) … FM-032 · the browser checks reproduce their summaries (3): SHOALMARK_REGENERATE=1 is not set* — loud, counted, as designed |
| the same 3.9.6 `test_core.py` (09:32:54–09:32:59) | **148 ok / 0 FAIL**, exit 0 |
| the guards | one runner at a time; before each run `pgrep -fl '[Pp]ython[0-9.]* [^ ]*test_(shoalmark\|core)\.py'` printed nothing and the 1-minute load was under 6 (2.52, 2.86, 2.89, 2.78), HEAD `b52437a`, the tree clean; each output whole in the Reviewer's scratch folder |

`test_shoalmark.py` takes no `-k`: it is a script, and the committed regeneration check ran inside the full runs — the
facts part on every run, the browser part in the 3.14 run under `SHOALMARK_REGENERATE=1`.

## The page, `work-tracker/evidence/FM-032/records-to-product-ratio.md`

The rule is complete on every point the brief lists: records added : product added; per repository; per Europe/Berlin
day of the merge; merge commits on the default branch's first-parent line against their first parent; deletions apart,
never netted; aggregates as summed counts; zero product added → the counts and no finite ratio; judged on rolling
seven-day sums, reported per day; every plan states the four numbers and the effect; *product* a measurement category.
shoalmark's categories, the command as the reference and the bug rule are there. The baseline table keeps the relayed
figures apart (*relayed, not remeasured*) beside the command's own; the per-day table equals the command. The change's
four numbers — records +219 −33,530, product +435 −2, 0.5:1 — equal my count of `git diff --numstat origin/main...HEAD`
(no binary, no rename). Two points the page leaves to the command, and the ruling (2) line's time: RV-729.

## `--ratio`, read

`ratio_cmd` (shoalmark.py:4784) reads only the configuration and git, through `git_out` (a list, no shell); `ratio_merge`
two diffs per merge, `--raw -z` for the pointers and `--numstat -z`, both `--no-renames`. I judge `--no-renames` right
for the reference command — rename detection is a heuristic and a user setting (`diff.renames`), so a moved file counts
as its lines deleted and added, which the rule's *lines added* reads literally; the page should say so (RV-729). The
day is `%cI` converted to Berlin; the fallback without a tz database is loud and exit 0. Thousands separators, `no
finite ratio`, exit 0 and 2 as documented. `--schema` lists `[ratio] records` and `[ratio] exclude`. The trunk is the
file's `trunk_ref()` — `origin/main`, `main`, `master` — reused rather than rewritten; it never reads `origin/master` or
`origin/HEAD` (RV-727).

## The ruling applied

Each of the four deleted outputs has, in its README, the command as run, the tested commit, both environments, the
original's and the fresh run's counts and failing ids, the file's sha256 (verified; the file's bytes) and the holding
commit, and a JSON block the test reads. The READMEs no longer say `checks.json` *holds* anything in the present tense
(slice A: *held … until 2026-09-30*, *had … (at `11faa03`)*; the start page: *held every measurement until
2026-09-30*). The ship-log rows sit at the top of FM-002's and FM-006's newest-first tables.

**The Implementer's open point — FM-002's output regenerated by verdicts, not by measure counts.** I judge the summary
faithful, not a P2: the board writes the clock (the owner's box holds what is owed *now*), so a rebuild of `361336a`
days later measures a different page — 740 texts, not 746 — and the thresholds' verdicts are the result the ruling and
the Principal's precision (i) judge. The README states both runs' measurement counts side by side and why they moved,
and the committed check will fail when a verdict moves. Two things are missing, both RV-728: the README's own checks
carry **controls** (the contrast pipeline's `#767676` on `#ffffff` at 4.542:1; AU-16's run with the alt texts removed,
which must read figures and markers — *so the check can see what it reports as absent*) and the dialog opened, and
neither `_derive_board` nor the summary counts them, so a fresh run whose controls fail still reads *14 checks, 0
failing*; and the summaries' *checks · failing* mixes units.

**What stays**, FM-032's section: `browser-fonts.json`, `results.json`, `scanned-refs.txt` and *the `jev-*` files*.
One of those regenerates byte for byte, and four outputs are not named (RV-728).

## FM-032's section and row, the CHANGELOG, the README

The section quotes the Owner's five lines of 06:54:04–07:21:58, one each, normalised and marked, times as the brief
gives them; the decisions are marked as decisions. The ship-log row (`2026-09-30 07:5x CEST`) sits at the top and names
each commit. `## Unreleased — 0.18.7` follows the file's form (`## Unreleased — 0.18.6`, `a7d0f52`), the two bullets on
top; `VERSION` stays 0.18.6. README: the `--ratio` row and the `[ratio]` keys in the `shoalmark.toml` row, true to the
code but for the trunk (RV-727). The fifth commit (`b52437a`) is justified: the change's own numbers can only be stated
at its last tip, and it touches the page and the row alone.

## Findings

**RV-726 · P2 · confidence 95% on the mechanism (reproduced), ~75% on the grade — `[ratio]`'s default counts a
repository's records as product wherever its tracker is not `work-tracker/`, and the refusal advises exactly that.**
`ratio_paths` (shoalmark.py:4729) defaults `records` to `["work-tracker/"]` — shoalmark's own layout — though the tool's
own default `tracker_dir` is `docs/work-tracker` (`DEFAULTS`, :61), which `--init` writes (:6541); and the exit-2 message
tells such a repository to add `records = ["work-tracker/"]`. Reproduced in a scratch repository with no `tracker_dir`
key, one merge adding two lines to `docs/work-tracker/FM-1.md` and one to `src/x.py`, `[ratio]` alone: `records +0 −0
product +3 −0 0.0:1` — every record line counted as product, silently. This is the tool doing the wrong thing for the
person using it, in the measurement the Owner named his main concern, in every repository at the default layout.
**Fix:** in `ratio_paths`, the default is the tracker directory:
`for key, default in (("records", [str(CONFIG["tracker_dir"]).strip("/") + "/"]), ("exclude", [])):`; the refusal
suggests `records = ["<tracker_dir>/"]` with the configured directory; `CONFIG_KEYS["[ratio] records"]` and README's
`shoalmark.toml` row say *the tracker directory* where they say `["work-tracker/"]`; a check plants a
repository without `tracker_dir`, `[ratio]` with no keys, a merge into `docs/work-tracker/` and `src/`, and asserts the
tracker's lines are records.

**RV-727 · P3 · confidence 95% — `--ratio`'s edges and its tests.** (a) `records = 5` or `records = true` (the
configuration reader accepts both) crashes in `ratio_paths` with a `TypeError` traceback, not the message: the check is
`isinstance(value, str) or not all(…)` — **fix:** `if not isinstance(value, list) or not all(isinstance(v, str) and
v.strip() for v in value):`. (b) The trunk: `trunk_ref()` never reads `origin/master` or `origin/HEAD`, so a clone whose
default branch is `master` reads its local `master`, which may be behind, and a default named otherwise has no ratio;
README says *`origin/main`, else `main`* while the code and the message also try `master` — **fix:** in `ratio_cmd` only
(leave `trunk_ref`'s other callers), `trunk = (git_out("symbolic-ref", "-q", "--short", "refs/remotes/origin/HEAD") or
"").strip() or next((r for r in ("origin/main", "origin/master", "main", "master") if git_out("rev-parse", "--verify",
"--quiet", r + "^{commit}")), None)`, and README's row names that order. (c) Tests: the first-parent line and the default
window are not planted — without `--first-parent`, or with a default window a day longer, every planted check stays ok,
and only the reproduction on this repository (skipped where `origin/main` is absent, as in CI) catches the first —
**fix:** plant a branch that carries a merge of its own (a side branch merged `--no-ff` into it inside the window) before
it merges into `main`, and assert that day's line says `(1 merge)` with only the first-parent diff; and run `--ratio`
with no dates, asserting the header's `<today in Berlin − 6> to <today>`.

**RV-728 · P3 · confidence 95% on the facts, ~70% on the grade — the ruling's application is incomplete.** (a)
`work-tracker/evidence/FM-006/jev-gate-test-score-output-2026-09-23.txt` (44 lines, sha256 `a75fe8d1…`, added in
`65d5d43`, cited by `gtm-claim-screen-2026-09-23.md:587`) **regenerates byte for byte** from git by a committed command —
`python3 jev-gate-test-score.py jev-gate-test-response-run1-2026-09-23.json jev-gate-test-response-run2-2026-09-23.json`
in its folder — while FM-032's section says the `jev-*` files *do not regenerate from git*. Under the ruling it is
replaced by its summary (the command, the two inputs, the verdict line *noise — the record blames the MODEL*, sha256
`a75fe8d11bcbc2d209bccc2a6c6f2b083b1b7fe33dd68f376938024f8849d5ea`, held at `65d5d43`) at line 587 of that page, with a
check in `test_shoalmark.py` that re-runs the scorer and compares its sha256; and the section's sentence becomes *the six
`jev-*` request, response and key files (an external service's exchange)*. (b) Four outputs of committed commands are
neither replaced nor named: `FM-002/slice-a/shots/requests.json` and `FM-006/landing/start-page/shots/requests.json`
(`render.mjs`'s hosts reached and refused, a Chrome run) and `FM-006/triage-page/demo.out` and `demo-de.out` (`demo.sh`
makes fresh keys and times, so its ids never repeat; `docs/triage.md` quotes it) — the section names each with its
reason, or replaces it. (c) Slice A's controls — `control["contrast light"|"contrast dark"]` at 4.542, `control["dialog
open light"|"dialog open dark"]`, and the six `control["ax <page> <scheme>"]` with figures and markers above 0 — are
part of the README's checks and are not in `_derive_board` or the summary: add them (`n += 1` each, a failing id
`control <key>`), and the block's `checks` becomes 24. (d) *checks · failing* counts checks on the left and failing
**texts** on the right: `checks-r3-before.json` reads *4 · 68* (all four checks fail, on 68 texts), the start page's
*18 · 3* is 2 failing checks on 3 texts, and `facts.json`'s block says `"checks": 24` for a reading with 24 wrecks and no
thresholds — the table says *checks · failing checks · failing texts* (`18 · 2 · 3`, `4 · 4 · 68`) and the facts block
drops `checks` for `wrecks`, the test's `_KEYS` following.

**RV-729 · P3 · confidence 90% — the page's and the section's words.** (a) The page times ruling (2) *07:3x*; the brief
gives **07:23:33**, and the line is a paraphrase in italics where the page's head promises *the Owner's words, one line
each* — **fix:** *07:23:33, his ruling (2), in substance:* and the text as it stands, not styled as a quotation. (b)
The page wraps mid-sentence in five places (lines 13–17, 26–28, 33–35, 40–48, 57–58: *rolling* / *record* /
*difference* / *environment* … alone on a line) — reflow to the file's width. (c) The page leaves two readings to the
command: that a merge's day is its **committer** date, and that a moved or renamed file counts as its lines deleted and
added (`--no-renames`) — add both to *The rule*, the second as *git's rename detection is a heuristic and a user
setting, so the reference counts without it*. (d)
FM-032's section says D1 *waits as an ask on this tracker*; the tracker's one `ask:` is the answered S5 question of
2026-09-28 — *waits for an ask, not filed here* (the front matter stays untouched on this branch). (e) *the 09-27 day
carries the two check outputs* — it carries four, of two folders (`073f21f`, `9d10d08`, both 12:02).

## The quality read — the first code build by a Sonnet Implementer here

Against the file's conventions, the tests and the messages, beside two Opus builds of this week read for the
comparison: `8409c9a` (FM-031, RV-679, implementer-51) and `1d9cc0c` (FM-030, RV-730, implementer-52).

- **Correctness of the core: no regression.** The numbers are exact on 17 lines against an independent count; the
  change's own numbers are exact; the four hashes and holding commits are exact; the regeneration check does what it
  claims (all three browser outputs regenerated in my 3.14 run, the same checks and ids). The Implementer surfaced its
  own open point (FM-002's moving counts) and its deviations without being asked.
- **Reuse: the file's own helpers**, as `8409c9a` reuses `addenda_only`: `git_out`, `trunk_ref`, `vcs()`, `CONFIG_NAME`,
  `CONFIG_KEYS` for `--schema`, the `main()` dispatch comment, the argparse help voice, the one-line docstrings.
- **The file's own patterns, missed (P2/P3 above).** `DEFAULTS` (:59) holds every configuration default with its reason,
  and `configure()` validates each with a message (`freeze_at`, `freeze_tag`, `judged_before_build`, `[headings]`); the
  new code inlines its defaults in `ratio_paths`, validates at command time, and its type check crashes on a scalar
  (RV-727 a) — and the inlined default is shoalmark's layout, not the tool's (RV-726). The escapes `\u2014`, `\u00b7`,
  `\u2212` appear 7 times in the new code; `792dbca`'s `shoalmark.py` has none and 1,149 lines with a literal em dash.
  Not graded.
- **Tests: strong where planted, thin where not.** Exact lines asserted; the Berlin midnight, a plain-path record, an
  `exclude`, a submodule pointer, a binary, a deletion, a zero-product day and sums reaching back are planted, not
  narrated; each fails on `792dbca`'s tool. Unplanted: the first-parent line and the default window (mutations survive,
  RV-727 c); the tz fallback exists only as its skip branch. The regeneration derivation leaves out slice A's controls
  (RV-728 c).
- **Commit messages: less evidence than this week's Opus builds.** `8409c9a`'s body gives the reproduction on main's
  tool and on the branch's, the checks *510 (main 507, +3)*, and the gates; `1d9cc0c`'s gives three reader cases before
  → after. `3deafb9`'s says *Tests plant the trunk* with no count and no line from main's tool; `991f978`'s ends with a
  note to itself (*The baseline and per-day tables are filled once the command lands*). `c819cde` and `c3d56ec` are
  precise about what regenerated and how.
- **The record's facts: two misses** — a ruling timed *07:3x* where the brief gives 07:23:33 (RV-729 a), and a *does not
  regenerate* that one run of a committed script disproves (RV-728 a).

**Judgment: correct in its core, a regression at its edges** — the numbers, hashes and regeneration are exact and every
new tool check fails on main's tool, but the defaults and validation skip the file's own `DEFAULTS`/`configure()`
pattern (RV-726, RV-727 a), two mutations survive the planted tests (RV-727 c), and the commit bodies carry no
main-versus-branch evidence where `8409c9a` and `1d9cc0c` do.

## Unproven here

- CI (no pull request); Windows; a machine with no tz database (simulated only, by replacing `ratio_zone`).
- The FM-002 fresh run's measurement counts (740, 32 pairs by night, AU-18 98 on 34 lines): the committed check compares
  verdicts only and does not print them; my run's verdicts are above.
- That the Owner relayed *66,550 : 15,968* and *1,015 / 1,784* at 07:04:27, the Owner's lines and their times, D9 and D1
  as his decisions: none is in git; I checked the page's quotations against the brief only.

## For the record

This verdict adds 215 record lines (this file) and no product line: after it the change reads records
+434 −33,530, product +435 −2.

path 5 — a merge rules nothing.
