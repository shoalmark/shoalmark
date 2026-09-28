# Review — the docs pass on the 0.18.6 cut at `59096f1` (2026-09-28, Reviewer, session `8e509911/reviewer-55`)

- **Reviewed:** `59096f1969fefc65a81be29e4f4b9f522c8bd256` (branch `release/v0.18.6`, `origin/main` `74124296` +
  `ce200c4b` + `59096f1`).
- **Tier:** *docs — a release cut*; findings only at P3, else NOT READY.
- **Independence:** same session — a sub-agent of `8e509911`, Reviewer seat, worktree `shoalmark-review-4`, detached at
  the reviewed sha. The Owner's checkout, every other worktree and every folder of session `8b91dba2` stayed outside
  every command.
- **Clock:** started 2026-09-28 22:40 CEST; suite ran 22:44–22:59 CEST (load 1.88 at start, under 2.6 throughout, no
  other suite running — `pgrep -fl '[Pp]ython[0-9.]* [^ ]*test_(shoalmark|core)\.py'` empty before the run).

## What I ran and what survived

**(1) File set and form mirror the 0.18.5 cut.** `3826a039` (VERSION, CHANGELOG heading, the two setup pages) +
`522db92` (`overrides/landing.html`: HUD badge, footer link+text, fine print + its Jinja comment) on main changed
`{CHANGELOG.md, VERSION, docs/de/setup.md, docs/setup.md, overrides/landing.html}`, 4×1-line + 3-line hunks, 7
insertions/7 deletions total. `ce200c4b` + `59096f1` on `release/v0.18.6` change the identical five files, the
identical hunk shapes (CHANGELOG heading only; `VERSION` whole-file; setup pages' `--branch v…` line, comment
untouched; landing.html's HUD line, footer mk line, fine print), `git diff --stat origin/main HEAD`: 7
insertions/7 deletions — exact numeric match. No file either cut touched that the other did not. **No finding.**

**(2) `git grep -n -E 'v?0\.18\.5' -- ':!CHANGELOG.md' ':!work-tracker' ':!test_shoalmark.py' ':!shoalmark.py'`** at
the tip: one hit, `overrides/landing.html:466`, inside the Jinja comment `{# FM-006 slice L, edit (a), the release
re-read at the 0.18.5 cut: … #}` (build-dropped; `git log -S'edit (a), the release re-read'` shows it was written
once, in `522db92`, and untouched since, including by `ce200c4b`/`59096f1`). It names the cut *at which the edit (a)
convention was established*, not a claim about the running release — the same shape as the test/tool labels this
check already exempts (naming the release a behaviour was built in, not the release this is). Judged not stale.
**No finding**, noted below.

**(3) CHANGELOG.** Exactly one `## 0.18.6 — 2026-09-28` heading, at the top; no `## Unreleased` remains (`grep -n
'^## '` / `'## Unreleased'`). `git diff origin/main HEAD -- CHANGELOG.md` touches only the heading line — every
bullet under it is main's, byte for byte. The fine print's two facts (*the board reads git — his act or answer shows
on its way before his merge*, FM-030; ***--queue** reads his `done:`/`due:` as his answer and admits no commit not
his*, FM-031) each match a 0.18.6 bullet and claim nothing else — `ce200c4b`'s first cut of the sentence also named
the hook's board-build measurement and the freeze ask, neither shipped in 0.18.6; `59096f1` is the Principal's
correction dropping both, confirmed by reading `59096f1`'s diff. No German twin of the landing/fine-print text exists
(`overrides/` holds only `landing.html`; `docs/de/` holds no landing/start-page file) — nothing to check there.
**No finding.**

**(4)** `git diff --stat origin/main HEAD -- shoalmark.py test_shoalmark.py test_core.py` — empty: the tool and both
suites are main's, byte for byte, so this docs cut carries no code of its own to test. Ran `python3 test_shoalmark.py`
once at the tip, Python 3.14.3, 22:44–22:59 CEST, guard clean (`pgrep` empty, load 1.88 at start). **547 ok, 0
skipped, exit 0.** Last two lines: *skipped here: 0 checks — every check ran* / *all green*. The release-consistency
case itself: *ok FM-006 · the setup pages clone the release they ship with — every `--branch v…` in the English and
the German page is v<VERSION>, and each has one (saw {'docs/setup.md': ['v0.18.6'], 'docs/de/setup.md':
['v0.18.6']}, VERSION 0.18.6)*. The suite's own literal FAIL/FAILED strings that appear inside several `ok` lines'
*(saw …)* tuples are fixtures the case asserts the tool prints — not suite failures; no line starts with FAIL or
ERROR, and no traceback appears anywhere in the 550-line log. **No finding.**

**(5) Gates.** `python3 shoalmark.py --check` → 0 (`INDEX.md is up to date — 41 trackers`; judged-before-build on;
Owner's two sections guarded; filing freeze 22 open, bug filings only). `--session-check` → 0. `git merge-tree
--write-tree origin/main HEAD` → clean tree `57b6aa6f28a3eb8bb82f2537331cde57528b13b3`. `--queue` at 2026-09-28
22:55:04 CEST: `branch release/v0.18.6 @ 59096f1  wait: no pull request — no verdict on 59096f1` / `1 waiting on you:
0 merge, 0 close, 0 wait, 1 pushed without a pull request`.

## Noted, not findings

- The Jinja comment at `overrides/landing.html:466` still reads *the release re-read at the 0.18.5 cut* — correct as
  a historical marker of when the *edit (a)* annotation convention began (check 2); it is not bumped at each cut and
  should not be read as the running line.

## Findings

None. No id of RV-747…749 is used.

## Verdict

**READY** — checks (1)–(5) all held with no P3 or above: the file set and every hunk's form exactly mirror the 0.18.5
cut (same five files, same 7/7 line count); no stale `0.18.5` running line remains; the CHANGELOG carries exactly one
current heading with its bullets untouched and the landing sentence's two facts each trace to a 0.18.6 bullet; the
tool and both suites are main's byte for byte and `test_shoalmark.py` is 547 ok, 0 skipped, all green; `--check`,
`--session-check` and `merge-tree` are all clean, and `--queue` (22:55:04 CEST) shows only this branch pushed, no
verdict yet — which this commit now gives it.

path 5 — a merge rules nothing
