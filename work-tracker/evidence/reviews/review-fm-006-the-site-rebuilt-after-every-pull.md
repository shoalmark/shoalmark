# Review — two lines, FM-006 and FM-007, at 9428c98 (2026-09-25 09:39 CEST, Reviewer, session `8e509911/reviewer-8`)

**NOT READY — one P2.** Branch `fm/006-the-site-rebuilt-after-every-pull`, tip `9428c98`, one commit on `origin/main`
`ea630c1` (PR 69's merge), by the Principal seat. **Tier: docs, one pass** — `git diff --name-only origin/main...HEAD`
names FM-006 and FM-007 and nothing else.

**Held.**
- **His word.** The 07:21:19Z user record (09:21:19 CEST, read alone) says *"I would like to have `site/` up-to-date after
  every pull so that i see it locally how it is going to be looking when i deploy it. You can give me also the command
  for now to try it"*. The row quotes its meaning, normalised and marked, and answers the second sentence.
- **The facts on main.** `zensical.toml:11` `site_dir = "site"`, `:13` `use_directory_urls = false`; `.gitignore`
  `site/`; `docs.yml` `on: push: tags v*` (plus a manual dispatch; the deploy job also waits for a public repository,
  and it is private); `lefthook.yml` post-merge `python3 shoalmark.py --html-only || true`.
- **Every pull is covered.** In a scratch repo, the two hooks together fire on every pull: a fast-forward pull and a
  rebase pull with no local commit fire `post-merge`, and a rebase pull over a local commit fires `post-checkout`.
- **FM-007's row.** The vendored `marked` renders the block `<ol start="2">`, six items, so the five points show as 3–7.
  The block's sha256 is still `07c31fa5…`, as filed.
- **The record.** Each row sits at the top of a newest-first log. The diff adds 2 lines and deletes none, so no merged
  row is edited. The freeze holds (18 open).
- **The gates.** `--check` 0, `--session-check` 0, the generator leaves the tree clean. `test_shoalmark.py` 355 ok and
  `test_core.py` 148 ok, on 3.14.3 and 3.9.6. `merge-tree` is clean against `origin/main` and against PR 65's tip
  `3b35f0f`.

**R1 · P2 · confidence high on the facts (measured), about 70% on the grade · On this Mac there is no `zensical`: the
row's command for now fails, and the hook it files for 0.18.4 is neither silent nor a build.**
- **Not installed.** `command -v zensical` finds nothing. There is no uv tool and no pipx package, and neither Python
  imports it. His checkout was not read.
- **The command for now.** `zensical build` exits 127, *command not found*.
- **The hook.** `sh -c 'zensical build || true'` exits 0 but prints `sh: zensical: command not found`. Lefthook 2.1.4
  shows that line on every checkout and every merge (scratch repo). `|| true` keeps the hook from failing; it does not
  make it silent.
- **What he asked for.** The line is for his machine. As written, it prints an error on every pull and builds nothing.
  Made silent, `site/` stays stale and looks current — the opposite of what he asked for.
- **What works here.** `uvx zensical build` in a scratch copy of `9428c98`: 0.47 s, *No issues found*,
  `site/signing.html` and `site/de/signing.html`.
- **The fix.**
  - Give him a command that runs on this Mac.
  - Have the 0.18.4 line say what the hook does where `zensical` is missing — fall back to `uvx`, or say once that
    the site was not rebuilt — instead of *silent*.

**Not this diff.** Line 1 of `docs.yml` on main still says *on every push to main*; its `on:` and line 4 say a tag only.

## The second pass — at a141f47 (2026-09-25 09:47 CEST, Reviewer, session `8e509911/reviewer-8`)

**READY.** `a141f47` is one commit by the Principal seat after this verdict (`945e950`). It rewrites FM-006's new row
in place — 1 line in, 1 out, nothing else. That row is still unmerged: it came in at `9428c98`, and `origin/main` is
`ea630c1`. **Tier: docs, one pass** — the branch still touches FM-006, FM-007 and this file only.

**R1 closed.**
- **The hook.** The 0.18.4 line now says what R1 asked. The hook builds the site where it finds a builder: `zensical`
  on the PATH, or else `uvx zensical`. Where it finds neither, it says in one line that the site was not rebuilt —
  never an error. *Silent* is gone.
- **The command for now.** It is `uvx zensical build`. In a scratch copy of `a141f47` it exits 0 in 0.38 s with *No
  issues found*, and builds `site/signing.html` and `site/de/signing.html`. `command -v zensical` still finds nothing.
- **The row's gloss.** *`uvx zensical build` is* reads as *works*, and it does.
- **`docs.yml`.** The row notes that its first-line comment still says *on every push to main* — true, and a second
  line for 0.18.4.
- **The rest of the row.** The quote, the site facts, the newest-first place and FM-007's row are unchanged.

**Gates.** `--check` 0, `--session-check` 0, the generator leaves the tree clean. `test_shoalmark.py` 355 ok and
`test_core.py` 148 ok, on 3.14.3 and 3.9.6. `merge-tree` is clean against `origin/main` and against PR 65's new tip
`5cc5625`.

**For the 0.18.4 pass, not a finding.** The first `uvx` run fetches an unpinned `zensical` inside a hook, as `docs.yml`'s
`pip install` does. The line does not say what a builder that fails does.
