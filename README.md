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
python3 tools/fathom-mark/fathom_mark.py --init              # fathom-mark.toml · docs/work-tracker/TRIAGE.md · .gitignore
# the Owner writes the intent and the current path in TRIAGE.md
python3 tools/fathom-mark/fathom_mark.py --new FEAT "what is wrong, in a sentence"
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

## A vendored copy is pinned

`--vendor` writes a `PIN` of sha256 hashes beside the copy. A copy edited in place is refused by its own
gate: change fathom-mark here, run `--vendor` again. Two repositories never run two tools under one name.

## What it is not

No release targets, no deploy axis, no product areas — a repository that needs them adds them around the
core. No sprint, no estimate, no assignee, no comment thread.

## Develop

`python3 test_fathom_mark.py` — every check builds its own throwaway repository.
