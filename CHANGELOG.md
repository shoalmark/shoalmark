# Changelog

What a repository takes on when it vendors again. Newest first; `--vendor` prints the sections that are new to it.

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
