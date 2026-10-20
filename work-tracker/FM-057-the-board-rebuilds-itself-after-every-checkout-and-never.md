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

**2026-10-19 — Built on `fm/057-refresh-hooks-back`:** `2e5ddb7` restores the three refresh hooks and their checks; `d855a1f` names the hooks and the fetch-only limit in English and German. The helper's callers, three fixtures and the README assertion follow the restored hooks; main at `be19828` is merged; the full non-browser run is clean; the critical-tier review is next.

**2026-10-19 — R11's hook half comes back in v0.20.1,** on the Owner's word of 19 October (recorded privately). The
hooks that rebuild the board after a checkout, a merge and a rebase are what make the board convenient to use, and
removing them left its users a worse experience.
- **v0.20.0 is unchanged:** it ships without the refresh hooks (`b417b3c`, #189), with R11's upgrade note.
- **v0.20.1 brings them back.** The other half stays: the board says what it read and when, with its rebuild command.
- **The case they must cover:** after #199 merged and a pull, the board did not show FM-037's owed act and its done
  button until `--html-only` ran by hand.

**2026-10-16 — READY at `2b57c02` by `01a1457e-86f9`:** R11 with Q4 (RV-3302: recorded privately). It rides on `fm/032-dbatch-into-production`, joined after FM-032's R22, R15 and R13 (`aa382dc`), for one pull request; CI runs once, on it.

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
- **Built** (`27f31560/builder-10`, `fm/045-r11-read-at`): `b417b3c` — R11: `--install-hook` writes no refresh hook, removes
  each one an earlier version wrote with a line, and keeps a person's own; `4344147` — the page and `view/built.json` say what the board
  read, and when, on git, on Subversion and with none. Critical tier: READY at `2b57c02` (above).

## Done when

- the page and `view/built.json` say what the board read and when, on git, on Subversion and with none (`4344147`,
  #189, in v0.20.0);
- in v0.20.1, `--install-hook` writes the refresh hooks after a checkout, a merge and a rebase again, in a clone that
  v0.20.0 cleaned of them and in one that never had them, keeping a person's own hook and naming it;
- after a pull that merges or rebases a change, the board shows it without `--html-only`, the case of 19 October
  included;
- the hooks' return is reviewed, critical tier, and merged into `release/v0.20.1`.

## Ship log

| Date | Event |
|---|---|
| 2026-10-19 | Refresh hooks restored on `fm/057-refresh-hooks-back` (`2e5ddb7`), with the setup words in both languages (`d855a1f`). Verification is incomplete; check limits recorded privately. Next: the critical-tier review. |
| 2026-10-19 | R11's hook half comes back in v0.20.1, on the Owner's word of 19 October (recorded privately). v0.20.0 ships as built, with R11's upgrade note; the read-at half stays. *Done when* restated for the hooks' return. |
| 2026-10-15 | Filed and judged: In Progress, P2, for v0.20.1, on `fm/045-r11-read-at`. |
| 2026-10-15 | Built by `27f31560/builder-10` on `fm/045-r11-read-at`: `b417b3c` — R11, the board-refresh hooks go and the explicit refresh stays; `4344147` — the board says what it read, and when. Next: the critical-tier review. |
| 2026-10-16 | Built by `27f31560/builder-10` on `fm/045-r11-read-at`: `db98190` — on the board's own run, `--html-only`, the read-at line says what is changed and not committed is not read, beside the time, the branch and the commit; `view/built.json` records no count there; a plain run counts it. RV-3302: recorded privately. |
| 2026-10-16 | **READY** at `2b57c02` by `01a1457e-86f9`, critical: R11 with Q4 (RV-3302: recorded privately). Joined on `fm/032-dbatch-into-production` by `aa382dc`, the fourth merge after FM-032's R22, R15 and R13, for one pull request. |
