# shoalmark

*A shoal mark is a mark set to show shallow water — a stake or a buoy. It tells you where not to run aground.*

A work tracker that lives in the repository it tracks. Markdown files with a small front matter, one Python
file that reads them all, no server, no database, no dependency beyond Python 3.9 — the one that ships with macOS.

Built for repositories worked by agents under one Owner: **the seat judges, the command applies.**

## What it does

| | |
|---|---|
| **A gate, not a convention** | every tracker's front matter is checked against one schema (`--schema`); an unknown key, a bad value, a duplicate id, a dangling link or a story closed over open chapters refuses the commit |
| **A filing looks first** | `--new KIND "title"` prints the trackers closest to the words before it writes the file, and the gate refuses the file until `considered:` names what it was held against — or `none` |
| **Triage is one command** | `--triage` writes a worksheet of the work in progress and the new filings, prints the Owner's intent and current path above the rules, and on every re-run *applies* the verdicts the seat filled in: `keep` · `park` · `epic` · `merge` · `close` · `fix`, a tier, at most ten ranks, a next move |
| **One model, two renderings** | `INDEX.md` (what an agent reads, committed) and `index.html` (what the Owner reads, git-ignored) say the same thing from the same functions: the path, the ranked work, the board — progress · triage · triaged · backlog · done |
| **A contract for agents** | `--init` writes the rules that make the tool bite into `AGENTS.md`, between markers it owns: the tracker is canonical · look before you file · the seat judges, the command applies · leave the fix for the next session · close out by deleting what you made obsolete |
| **A cold start** | `--next` answers what a session asks first: what do I work on, in what order, and what is true now of each |
| **Read-only board** | search, a story view, each tracker rendered in the page. A viewer, not a Jira: no editing, no state, no server |

## Start

```bash
python3 shoalmark.py --vendor <repo>/tools/shoalmark     # a pinned, self-contained copy
cd <repo>
python3 tools/shoalmark/shoalmark.py --init --key MSR    # shoalmark.toml · docs/work-tracker/TRIAGE.md · .gitignore
# the Owner writes the intent and the current path in TRIAGE.md
python3 tools/shoalmark/shoalmark.py --new "what is wrong, in a sentence"     # becomes MSR-001
python3 tools/shoalmark/shoalmark.py                     # regenerate; exit 4 on a violation
```

Hooks — plain git hooks, no runner needed; a hook that is not shoalmark's is never overwritten:

```bash
python3 tools/shoalmark/shoalmark.py --install-hook      # pre-commit stages the regenerated INDEX.md; a violation refuses the commit
```

Upgrade: `python3 <shoalmark>/shoalmark.py --vendor <repo>/tools/shoalmark` prints what changed since the
version it replaces ([CHANGELOG](CHANGELOG.md)) and refuses a copy that was edited in place; then run `--init`
again to refresh the contract in `AGENTS.md`.

## Ids, files and branches

- **One id space per repository, keyed by the project** — `MSR-012`, not `BUG-012`. The id is the routing key
  (filename = front matter = first heading, and every link, `considered:` and `epic:` names it), so it encodes
  nothing that can change: the kind of work is a tag (`tags: bug`), being a story is a field (`epic:`). A project
  key also keeps `MSR-001` and `FM-001` apart when two repositories are talked about in one place.
  `--init --key MSR` writes it; several prefixes are still possible under `[kinds]`.
- **One flat directory, the id in the filename** — `docs/work-tracker/MSR-012-stock-is-booked-twice.md`. No
  folder per kind: a number would name three files, every link would cross directories, and re-classifying
  a tracker would be a move that breaks them.
- **The work type lives on the branch**, where it is cheap and may change: `feat/msr-012-booking`,
  `fix/msr-013-double-count`. The tool finds a tracker's work from branch and commit text.

## One seam, by convention: a deriver

The core knows nothing about releases, deploys, product areas or whatever else a repository tracks beside its
work. A repository that needs that puts one executable at **`<tracker dir>/derive`** — no setting names it. The core
runs it first, on every run, with every tracker's id, status, file and front matter as JSON on stdin, and reads JSON
back:

```json
{ "MSR-012": { "Ver": "1.2.0", "Live": "live ✓" },
  "_keys":     { "version": { "shape": "\\d+\\.\\d+\\.\\d+", "says": "the release it shipped in" } },
  "_problems": [ "MSR-014: version on work that has not shipped" ],
  "_files":    { "docs/RELEASES.md": "…the whole file…" } }
```

Each value key becomes a column in `INDEX.md` and on the board — and a view on the board. `_index` and `_board` narrow
which goes where; a value may be `[value, display]`; `_notes` explain the columns in `INDEX.md`'s header; a per-tracker
`_needs` says what open work is missing. A `theme.css` beside the trackers restyles the page. `_keys` join the schema gate.
`_problems` fail the commit like the core's own. `_files` are written, drift-checked and staged by the core, so a
deriver has no side effects. **A non-zero exit refuses the run before anything is written** — a crash included.
Nothing derived is stored, so nothing derived can be stale. It runs on every run, the post-checkout refresh too: keep it fast.

## A vendored copy is pinned

`--vendor` writes a `PIN` of sha256 hashes beside the copy. A copy edited in place is refused by its own
gate: change shoalmark here, run `--vendor` again. Two repositories never run two tools under one name.

## What it is not

No release targets, no deploy axis, no product areas — a repository that needs them adds them with a deriver. No sprint, no estimate, no assignee, no comment thread.

## Develop

`python3 test_shoalmark.py` and `python3 test_core.py` — 210 checks. `test_core.py` pins the core's behaviour on a
synthetic corpus (the checks the tracker carried in the repository it was cut from); `test_shoalmark.py` pins what
was built here. Every check builds its own throwaway repository; where Chrome or Chromium is
installed the board is rendered and read back. Run it under the oldest Python you promise: `/usr/bin/python3 test_shoalmark.py`.
