# fathom-mark

A work tracker that lives in the repository it tracks. Markdown files with a small front matter, one Python
file that reads them all, no server, no database, no dependency beyond Python 3.11.

Built for repositories worked by agents under one Owner: **the seat judges, the command applies.**

## What it does

| | |
|---|---|
| **A gate, not a convention** | every tracker's front matter is checked against one schema (`--schema`); an unknown key, a bad value, a duplicate id, a dangling link or a story closed over open chapters refuses the commit |
| **A filing looks first** | `--new KIND "title"` prints the trackers closest to the words before it writes the file, and the gate refuses the file until `considered:` names what it was held against — or `none` |
| **Triage is one command** | `--triage` writes a worksheet of the work in progress and the new filings, prints the Owner's intent and current path above the rules, and on every re-run *applies* the verdicts the seat filled in: `keep` · `park` · `epic` · `merge` · `close` · `fix`, a tier, at most ten ranks, a next move |
| **One model, two renderings** | `INDEX.md` (what an agent reads, committed) and `index.html` (what the Owner reads, git-ignored) say the same thing from the same functions: the path, the ranked work, the board — progress · triage · triaged · backlog · done |
| **Read-only board** | search, a story view, each tracker rendered in the page. A viewer, not a Jira: no editing, no state, no server |

## Start

```bash
python3 fathom_mark.py --vendor <repo>/tools/fathom-mark     # a pinned, self-contained copy
cd <repo>
python3 tools/fathom-mark/fathom_mark.py --init --key MSR    # fathom-mark.toml · docs/work-tracker/TRIAGE.md · .gitignore
# the Owner writes the intent and the current path in TRIAGE.md
python3 tools/fathom-mark/fathom_mark.py --new "what is wrong, in a sentence"     # becomes MSR-001
python3 tools/fathom-mark/fathom_mark.py                     # regenerate; exit 4 on a violation
```

Pre-commit (lefthook shown; any hook runner works — the command prints exactly what it wrote):

```yaml
pre-commit:
  commands:
    tracker-index:
      glob: "docs/work-tracker/*.md"
      run: written=$(python3 tools/fathom-mark/fathom_mark.py --print-written) && printf '%s\n' "$written" | git add --pathspec-from-file=-
post-merge:
  commands:
    tracker-board:
      run: python3 tools/fathom-mark/fathom_mark.py --html-only || true
```

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

## A vendored copy is pinned

`--vendor` writes a `PIN` of sha256 hashes beside the copy. A copy edited in place is refused by its own
gate: change fathom-mark here, run `--vendor` again. Two repositories never run two tools under one name.

## What it is not

No release targets, no deploy axis, no product areas — a repository that needs them adds them around the
core. No sprint, no estimate, no assignee, no comment thread.

## Develop

`python3 test_fathom_mark.py` — every check builds its own throwaway repository.
