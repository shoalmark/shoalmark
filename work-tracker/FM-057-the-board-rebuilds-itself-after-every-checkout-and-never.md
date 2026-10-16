---
id: FM-057
status: In Progress
considered: FM-045, FM-030, FM-023
tags: process
next: build
triaged: 2026-10-15
tier: P2
hook: "The board rebuilds itself after every checkout, merge and rebase, and never says what it read or when"
---

# FM-057 — the board rebuilds itself after every checkout, and never says what it read, or when

## What is true now

**Filed and judged 2026-10-15: In Progress, P2.** It carries R11 and the quick win beside it into v0.20.1 (FM-023's
table of 2026-10-15).
- **R11,** the Owner's ruling of 12 October (`work-tracker/evidence/rulings-2026-10-12.md`): the global board-refresh
  hooks go; the explicit refresh, the immediate visibility of committed acts, and the revision and freshness evidence
  stay.
- **Today** `--install-hook` writes `post-checkout`, `post-merge` and `post-rewrite`, which rebuild the git-ignored
  board from the hooks' copy after each (near `shoalmark.py:9393–9425` at `5f792d6`). `view/built.json` records what
  the board was built from (FM-045); the page does not say when it was built, or from what.
- **The quick win beside it:** the page names its own moment (when it was built; on git, the commit, the branch and
  whether the tree had changes; on Subversion, the working copy's revision; with none, the folder) and the command that
  rebuilds it. It never says *current*, *live* or *up to date*.
- **Built, not yet reviewed** (`27f31560/builder-10`, `fm/045-r11-read-at`): `b417b3c` — R11: `--install-hook` writes no refresh hook, removes
  each one an earlier version wrote with a line, and keeps a person's own; `4344147` — the page and `view/built.json` say what the board
  read, and when, on git, on Subversion and with none. Critical tier: the review is next.

## Done when

- `--install-hook` writes no refresh hook, and removes only the ones an earlier version wrote, each with a line,
  keeping a person's own;
- the page and `view/built.json` say what the board read and when, on git, on Subversion and with none;
- both are reviewed, critical tier, and merged into `release/v0.20.1`.

## Ship log

| Date | Event |
|---|---|
| 2026-10-15 | Filed and judged: In Progress, P2, for v0.20.1, on `fm/045-r11-read-at`. |
| 2026-10-15 | Built by `27f31560/builder-10` on `fm/045-r11-read-at`: `b417b3c` — R11, the board-refresh hooks go and the explicit refresh stays; `4344147` — the board says what it read, and when. Next: the critical-tier review. |
| 2026-10-16 | Built by `27f31560/builder-10` on `fm/045-r11-read-at`: `db98190` — on the board's own run, `--html-only`, the read-at line says what is changed and not committed is not read, beside the time, the branch and the commit; `view/built.json` records no count there; a plain run counts it. RV-3302: recorded privately. |
