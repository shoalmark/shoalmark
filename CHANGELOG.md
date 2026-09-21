# Changelog

What a repository takes on when it vendors again. Newest first; `--vendor` prints the sections that are new to it.

## 0.12.0 — 2026-09-21

- **Runs on Windows, and with Subversion — proven in CI** on Windows, Linux and macOS (Python 3.9 and 3.12), both
  suites, Subversion installed on each, the board rendered in a browser on each.
- **Subversion:** the root is found by `.svn` too; a pass's *last worked on* comes from one `svn log`; `--init` sets
  `svn:ignore` for the board (no `.gitignore`) and writes a contract that says the true thing — **run the tool before
  `svn commit`**: Subversion's command line has no client-side hook. `--install-hook` sets `tsvn:startcommithook`
  and `tsvn:precommithook`, so **TortoiseSVN** writes `INDEX.md` before its commit dialog lists the files and
  refuses a violation (it asks the user once). For a gate nobody can skip: `--check` from the server's pre-commit hook.
- **Windows:** messages, hooks and the contract say `python`, not `python3`; a cp1252 console no longer crashes a
  run; every written file is UTF-8 with `\n` on every system; `--print-written` prints `\n` and forward slashes (a
  git hook on Windows fed `git add` a name ending in a carriage return); a deriver is run by this interpreter.
- **A PIN survives line-end conversion** (git's `autocrlf`, `svn:eol-style`): hashes are taken over `\n` text.
  Vendor again to get a PIN made this way.

## 0.11.0 — 2026-09-21

- **A repository that is not in English: `[headings]` in `shoalmark.toml`** names the seven sections the tool reads
  and writes — `state`, `why`, `done`, `log` in a tracker; `intent`, `path`, `passes` in `TRIAGE.md`. `--new` and
  `--init` write them; the gate and the triage pass read them. The English names stay understood, so a repository
  can change language a file at a time. They are configuration and not a label because the gate depends on them —
  what the gate says stays a function of the repository alone. **No table, no change.**
- A pass under *Passes* is a paragraph that carries its date (it always was, by the contract) — the template's notes
  are told apart by that, not by their English words.

## 0.10.0 — 2026-09-21

- **The board has a light / dark button**, in the header: `◐ auto` → `light` → `dark`. It switches every theme's
  `@media (prefers-color-scheme: …)` rule on or off by hand, so **a brand needs no change** — provided its dark colours
  sit under that rule, as the starter's do. The choice is kept in the viewer's browser (the board still works where
  storage is refused); printing is always light. Three new labels: `scheme.auto`, `scheme.light`, `scheme.dark`.

## 0.9.0 — 2026-09-21

- **A repository's brand has a folder of its own: `<tracker dir>/brand/`** — the same name the organisation's place
  has (`tools/shoalmark/brand/`). **Move `theme.css`, `logo.svg` / `logo.png` and `labels.yaml` there**: left loose
  beside the trackers they are no longer read, and a warning says so.
- **A path in a `theme.css` is written relative to that file**, as an editor resolves it, and the tool re-bases it onto
  the page — so `url("fonts/mine.woff2")` finds `brand/fonts/mine.woff2`, and an `@import` or a font now works from the
  organisation's and the person's place too. **If your theme imports something, its path changes** (one `../` more,
  from inside `brand/`).

## 0.8.0 — 2026-09-21

- **A board anyone can brand — three optional files, no setting** (README §9). `theme.css` (colours, fonts),
  `logo.svg` or `logo.png` (the header and the browser tab), `labels.yaml` (every word of the board, flat
  `key: value` — a German board is this file). The same names in three places, the later one winning:
  `tools/shoalmark/brand/` (the organisation — `--vendor` copies and pins it), beside the trackers (the repository),
  `~/.config/shoalmark/` (the person). **Only the git-ignored board reads them** — `INDEX.md` and the gate are the same
  whoever runs them.
- `--brand` says which place gave the board its theme, logo and labels; `--brand DIR` writes a commented starter.
- The board shows the repository's `name`, a `tagline` and a `footer` (both labels, both empty by default), and
  prints in the light palette.
- **If you already have a `theme.css`:** it is now its own stylesheet instead of being appended to the tool's, so
  `@import` and `@font-face` work in it — and a theme whose `@import` is missing is left out whole, with a warning,
  because a colour mapped onto a missing variable is invalid, not the default.
- A theme that is hard to read, an oversized logo and a mistyped label are warnings, never failures.

## 0.7.1 — 2026-09-21

Found by an independent review of the first port onto this tool. **If you have a deriver, read the first item.**

- **A deriver no longer sees the environment, and is told things on stdin.** It now receives `mode`
  (`write` · `check` · `board` · `read`) and `flags` — whatever was typed as the new `--derive-flag NAME` on that
  run — and runs with `PATH`, `HOME` and the locale only. A deriver that took an override from an environment
  variable let a stray `export` in the committing shell rewrite derived cells and stage them, exit 0. **Move any
  such switch to `flags`.** `mode: board` is how a deriver knows it may stand a guard down: nothing that run
  produces can be committed.
- A deriver that does not answer within 60 s is refused; it used to hang the gate for as long as it liked.
- **A vendored copy whose `PIN` was deleted is refused.** It used to pass, silently, with its integrity check off.
  Messages about the pin name a repository-relative path.
- `--help` names the command the repository teaches (`SHOALMARK_CMD`). The write log says how many trackers are
  `In Progress` and how many files the deriver generated.
- Two behaviours the hook contract rests on have checks again: `--print-written` still names its paths under a lint
  while exiting 4; `--check --print-written` writes and prints nothing.

## 0.7.0 — 2026-09-21

- **Licensed under `Apache-2.0 OR MIT`, at your option.** It was *proprietary, no licence chosen*. `LICENSE-APACHE`,
  `LICENSE-MIT` and `NOTICE` ship in the vendored copy, pinned like the rest. A repository that vendors shoalmark may
  use, change and redistribute it under either licence; a copy edited in place still refuses itself — that is the
  tool's own integrity check, not a licence term: re-vendor, or write a new `PIN`.
- `--next` prints the links in the current path as their labels.

## 0.6.1 — 2026-09-21

- **Fixed: `epic <ID>` and `merge <ID>` verdicts were refused in a repository whose ids are not `FEAT-`/`BUG-`.** One
  pattern in the verdict parser still named that pair; it reads the configured prefixes now. Found by checking the
  README's verdict table against the tool.
- **`README.md` is written for the agent that uses the tool, and ships in the vendored copy** (pinned like the rest):
  start · file · stop · triage · what to do when the gate refuses · install · the deriver's JSON · working on the tool.

## 0.6.0 — 2026-09-21

- **The tool is called `shoalmark`** — it was `fathom-mark` until here. The file is `shoalmark.py`, the configuration
  `shoalmark.toml`, the vendored directory `tools/shoalmark/`, the environment variable `SHOALMARK_CMD`.
  **To move a repository:** vendor into `tools/shoalmark/`, delete `tools/fathom-mark/`, rename `fathom-mark.toml` to
  `shoalmark.toml`, run `--init` and `--install-hook` — a contract block and hooks written under the old name are
  recognised and replaced, never left stranded. Tracker ids do not change: an id never does.

## 0.5.0 — 2026-09-21

What the exploration of the first real port forced — each item answers a measured difference
(`docs/work-tracker/evidence/FM-001/port-rd.md`). All of it is the deriver's output or a convention; no setting.

- **One model, two renderings.** `_index` and `_board` say which derived values `INDEX.md` prints and which the board
  shows — default: all. Every derived value stays a view, a fact and a search word on the board.
- **A value may be a pair, `[value, display]`.** The value groups, sorts, searches and is what `INDEX.md` prints; the
  display form is for the board's cells (`→ 0.16.x`, `0.16.4 ✓`).
- **`_notes`** — paragraphs for `INDEX.md`'s header. **`_needs`** (per tracker) — what open work still needs, shown
  with the core's own marks on the ranked table and the board.
- **A group header on the board sums its rows up by the board's columns.**
- **`theme.css` beside the trackers** is appended to the page's style — a repository's own palette and fonts.
- **`FATHOM_MARK_CMD`** — a repository that wraps the tool is named by its own command in every message.

## 0.4.0 — 2026-09-21

- **One seam, by convention — a deriver.** If `<tracker dir>/derive` exists and is executable, the core runs it first,
  on every run: every tracker's id, status, file and front matter go in as JSON on stdin; JSON comes back on stdout.
  `{"<ID>": {"Column": "value"}}` adds columns to `INDEX.md` and the board, and each is also a view on the board ·
  `_keys` adds front-matter keys to the schema gate (never redefines one) · `_problems` are counted with the core's ·
  `_files: {path: text}` are other generated files — the deriver has no side effects; the core writes them, lists them
  under `--print-written` and counts them as drift under `--check`. A non-zero exit — a crash included — **refuses the
  run before anything is written**. Nothing derived is stored, so nothing derived can be stale. No setting.
- **A repository without a deriver pays nothing**: same `INDEX.md`, byte for byte.
- Proven before it was merged, against a 501-tracker corpus: `docs/work-tracker/evidence/FM-001/seam-bprime-rd.md`.

## 0.3.0 — 2026-09-21

- **Runs on Python 3.9** — the Python that ships with macOS. The configuration is read without `tomllib`; the
  subset is what `--init` writes (`[table]`, `key = "text"`, numbers, `true`/`false`, comments).
- **`--init` writes the agent contract** into `AGENTS.md`, between markers it owns (your text outside them is
  kept), and a three-line `CLAUDE.md` router if there is none. Run `--init` again after vendoring to refresh it.
- **`--next`** — the cold-start question: the ranked work in order, each with its next move and what is true now.
- **`--install-hook`** — plain git hooks; no hook runner needed. A hook that is not fathom-mark's is left alone.
- **`--vendor` refuses to overwrite a copy that was edited in place**, and prints what changed since the
  version it replaces.
- `--related` skips German stop words. The triage rules say *harm to people who use it today* where they said
  *harm in production*. The board's palette is neutral.

## 0.2.1 — 2026-09-21

- An unfilled `TRIAGE.md` is no longer printed as if it were a path. An INDEX row shows the hook without its
  quotation marks. A filename's slug ends on a word, is capped at 60 characters and transliterates umlauts.
  `--related` reads words in any alphabet. A tracker's own id in its own heading no longer links to itself.

## 0.2.0 — 2026-09-21

- **One id space per repository, keyed by the project** (`--init --key MSR` → `MSR-001`). `--new "title"` needs
  no prefix where there is one. `bug` joins the tag vocabulary. Branch names may carry ids of any length.

## 0.1.0 — 2026-09-21

- The core: a front-matter schema and its gate, a filing looks first, the triage pass, the read-only board.
