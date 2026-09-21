# shoalmark

*A shoal mark is a mark set to show shallow water — a stake or a buoy. It tells you where not to run aground.*

A work tracker that lives in the repository it tracks: one Markdown file per work item, one Python file that reads
them all, a gate on every commit. No server, no database, no dependency beyond Python 3.9.
**This page is written for the agent that has to use it.** Find your situation, do what it says.

| You are… | Go to |
|---|---|
| starting a session in a repository that has `tools/shoalmark/` | [§1 Start](#1-start--what-do-i-work-on) |
| about to file something | [§2 File](#2-file--look-first) |
| stopping, with work left | [§3 Stop](#3-stop--leave-the-fix) |
| asked to run a triage pass | [§4 Triage](#4-triage--you-judge-the-command-applies) |
| blocked by the gate | [§5 The gate refused me](#5-the-gate-refused-me) |
| adding it to a repository | [§6 Install](#6-install-and-upgrade) |
| making it know about releases, deploys, anything of the repository's own | [§7 The deriver](#7-the-one-seam-a-deriver) |
| changing shoalmark itself | [§8 Working on shoalmark](#8-working-on-shoalmark) |
| giving the board a name, a logo, colours, another language | [§9 Branding](#9-branding-the-board) |

`<cmd>` below is `python3 tools/shoalmark/shoalmark.py` in a repository that vendors it — or whatever command that
repository's own messages name. Every command finds the repository by itself: the nearest `shoalmark.toml`, else the
git toplevel.

## The five rules

1. **The tracker is canonical.** Spec, state and record of a piece of work live in its tracker — never in a side
   plan, a chat or a TODO comment. *What is true now* is rewritten in place; only the ship log is append-only.
2. **Look before you file.** The default is a slice of a tracker that exists, not a new one.
3. **An id never changes and says nothing that can.** `MSR-012` — the kind of work is a tag, a story is a field.
4. **The seat judges, the command applies.** Never hand-edit `triaged:` `tier:` `rank:` or a park.
5. **Close out by asking what this made obsolete — and delete it in the same change.**

## 1. Start — what do I work on?

```bash
<cmd> --next
```

Prints the Owner's current path, then the ranked work in order — each with its next move, what it still needs, and
the opening of its *What is true now* — and ends with `START WITH: <id>`: the first ranked tracker whose move is
yours (`review` · `run` · `script` · `build`), not the Owner's (`owner`) and not a wait. Read that tracker. Work on
a branch that carries the id: `feat/msr-012-slug`, `fix/msr-013-slug`.

Nothing ranked? It says how many trackers wait for a triage pass. No path written? Only the Owner writes it
(`<tracker dir>/TRIAGE.md`) — ask; do not invent one.

## 2. File — look first

```bash
<cmd> --new "what is wrong, in one sentence"
```

It prints the closest existing trackers **before** it writes the file. Open the top hits. If one of them already
owns this, add a slice to it and delete the new file. Otherwise fill the front matter:

```yaml
---
id: MSR-014                 # written for you; equals the filename and the first heading
status: Proposed            # Proposed · In Progress · Parked · Reserved · Shipped · Closed
considered: MSR-003, MSR-009   # what you held this against — or: none. REQUIRED: the gate refuses the file without it
tags: bug                   # at most 3, from [tags] in shoalmark.toml — a closed vocabulary
epic: MSR-003               # optional: the story this is a chapter of
hook: "The problem as filed, in two or three sentences — this is the INDEX row."
---
```

Then the body: `# MSR-014 — title` · `## What is true now` · `## Why` · `## Done when` · `## Ship log`.
`<cmd> --schema` prints every key, its shape and **who may write it**.

## 3. Stop — leave the fix

The next session starts cold. Before you stop:

- Rewrite **What is true now** so its opening says what is left — one remainder, stated plainly.
- Set **`next:`** to the next move: `review` (built, a branch waits to merge) · `run` (built, a real run is owed) ·
  `wait` (a date or an event) · `owner` (the Owner's act alone) · `script` (mechanical) · `build` (anything else).
- On a `build`, with the tracker open, set **`kind-of-problem:`** — `obvious` (a script could do it) ·
  `complicated` (found by reading) · `complex` (found only by running) · `chaos` (harm now).
- Waiting on something? **`blocked-by: MSR-009, Owner — the ruling awaited`**. *Blocked* is derived and clears itself.
- Done? `status: Shipped` (merged — not deployed) and remove `rank:`. **A story stays open while a chapter is.**

## 4. Triage — you judge, the command applies

```bash
<cmd> --triage        # writes <tracker dir>/evidence/triage/triage-<today>.md and prints the rules
```

Fill the **Verdict** and **Reason** cells, row by row, from the row. Run the same command again — every ten rows
or so, and at the end: it applies what you filled, refreshes `INDEX.md`, keeps your rows, lists what is left.

| Verdict | Means | The command writes |
|---|---|---|
| `keep P1 #2 build` | worked on in the last 7 days, or the current path names it, or it is P0/P1 today | `triaged:` `tier:` and — if given — `rank:` (1–10, one tracker each) and `next:` |
| `epic MSR-003 P2` | a keep that is a chapter of a story | the same, plus `epic:` |
| `park P3` | fails the keep test; a real remainder, nobody on it. **P2 or P3 only — harm is never parked** | `status: Parked` `tier:` `triaged:` |
| `merge MSR-003` · `close` · `fix` | its scope belongs elsewhere · retired · its status is simply wrong | `triaged:` only — **you finish these by hand**, as the rules say |

Never write a note into a tracker during a pass; the reason lives in the worksheet. Never touch the current path.
The Owner rules by merging the pass's pull request, striking any row first.

## 5. The gate refused me

`<cmd>` regenerates `INDEX.md`; `<cmd> --check` only looks. Exit codes: **0** green · **3** drift — a tracker
changed and nothing regenerated: run `<cmd>` · **4** a violation — *fix the tracker; regenerating will not clear
it* · any other code comes from the repository's deriver (§7) and its message says why.

| It says | Do |
|---|---|
| `a new tracker says what it was held against` | run `--related <id>`, open the hits, fill `considered:` |
| `` `xyz:` is not a front-matter key — did you mean … `` | fix the typo; anything else belongs in the body |
| `` `key:` is <meaning> — <shape> — got … `` | the value does not fit the key's shape; `--schema` shows it |
| `dangling link -> FILE (did you mean …?)` | the id is right and the slug moved: use the file it names |
| `duplicate tracker id` · `identity drift` · `H1 drift` | filename, `id:` and the first heading must carry one id; renumber the later filing — nothing is ever deduplicated for you |
| `` `rank:` … remove it when the tracker ships, parks or closes `` | do that |
| `A story is open while a chapter is` | keep the story `In Progress` with `next: wait`, or move the chapters first |
| `… differs from its PIN` | someone edited the vendored tool in place. Never do that: change it upstream, vendor again |

Never `--no-verify`. Never hand-edit `INDEX.md` — it is generated.

## 6. Install and upgrade

```bash
python3 <shoalmark>/shoalmark.py --vendor <repo>/tools/shoalmark     # a pinned, self-contained copy + PIN (sha256)
cd <repo>
python3 tools/shoalmark/shoalmark.py --init --key MSR               # shoalmark.toml · TRIAGE.md · .gitignore · the contract in AGENTS.md · a CLAUDE.md router
python3 tools/shoalmark/shoalmark.py --install-hook                 # plain git hooks; a hook that is not shoalmark's is never overwritten
```

Then **the Owner** writes the intent and the current path in `<tracker dir>/TRIAGE.md`. Nobody else edits those two
sections. Upgrade: `--vendor` again (it prints what changed since the version it replaces and refuses a copy that
was edited in place), then `--init` again to refresh the contract between its markers — your text outside them is kept.

What lives where, by convention — no setting names any of it:

| Path | What |
|---|---|
| `shoalmark.toml` | optional. `name` · `tracker_dir` (default `docs/work-tracker`) · `blob` (forge URL prefix) · `triage_days` (7) · `[kinds]` id prefix → INDEX section · `[considered_from]` · `[tags]` |
| `<tracker dir>/<ID>-<slug>.md` | the trackers — one flat directory, the id in the filename |
| `<tracker dir>/TRIAGE.md` | the Owner's intent and current path; one paragraph per pass |
| `<tracker dir>/INDEX.md` | generated, committed — what an agent reads |
| `<tracker dir>/index.html`, `view/` | generated, git-ignored — the read-only board the Owner reads |
| `<tracker dir>/evidence/` | worksheets and pass records — append-only, never on a reader's path |
| `<tracker dir>/derive` | optional, executable — the repository's own axis (§7) |
| `<tracker dir>/theme.css` | optional — appended to the board's style |

## 7. The one seam: a deriver

The core knows nothing about releases, deploys or product areas. A repository that needs them puts one executable
at **`<tracker dir>/derive`**. The core runs it first, on **every** run — so keep it fast — with this on stdin:

```json
{ "root": "/abs/path", "mode": "write", "flags": [], "trackers": [ { "id": "MSR-012", "status": "Shipped", "file": "MSR-012-x.md", "fm": { "version": "1.2.0" } } ] }
```

and reads this from stdout:

```json
{ "MSR-012": { "Ver": "1.2.0", "Release": ["1.2.0", "1.2.0 ✓"], "_needs": [] },
  "_keys":     { "version": { "shape": "\\d+\\.\\d+\\.\\d+", "says": "the release it shipped in", "who": "the ship commit" } },
  "_problems": [ "MSR-014: version on work that has not shipped" ],
  "_index":    [ "Ver" ],
  "_board":    [ "Release" ],
  "_notes":    [ "**Ver** = the release it shipped in." ],
  "_files":    { "docs/RELEASES.md": "…the whole file…" } }
```

- Each value key is a **column** in `INDEX.md` and on the board, and a **view**, a fact and a search word on the
  board. `_index` / `_board` narrow which goes where (default: all). A value may be `[value, display]`: the value
  groups, sorts and is printed in `INDEX.md`; the display form is for the board's cells.
- `_keys` join the schema gate — add a key, never redefine one. `_problems` fail the commit like the core's own.
  `_needs` (per tracker) are shown beside the core's own marks. `_notes` go into `INDEX.md`'s header.
- `_files` are written, drift-checked (`--check`) and staged (`--print-written`) **by the core**. A deriver has no
  side effects, and nothing derived is ever stored — so nothing derived can be stale.
- **A non-zero exit refuses the run before anything is written** — a crash included, and silence past 60 s. Say
  why on stderr.
- `mode` is `write` · `check` · `board` (only the git-ignored page is produced — a guard that protects committed
  output may stand down) · `read`. `flags` are what was typed as `--derive-flag NAME` on **this** run.
- **A deriver is told things on stdin and never reads the environment** — the core runs it with `PATH`, `HOME`,
  the locale and nothing else. A git hook inherits whatever the shell that ran `git commit` had exported; a deriver
  that listened to that would let a stray variable decide what gets staged.
- A wrapper script may set `SHOALMARK_CMD` so every message names the repository's own command.

## 9. Branding the board

Three optional files, the same names in every place — the board is built from the places in order, **the later one
wins**. Only the git-ignored board reads them: `INDEX.md` and the gate are the same whoever runs them.

| File | Carries |
|---|---|
| `theme.css` | colours and fonts. Each place's file is its own stylesheet, so one variable changes one colour; `@import` and `@font-face` work. A theme whose import is missing is left out whole |
| `logo.svg` / `logo.png` | the header and the browser tab; at most 200 kB; a script inside an SVG cannot run |
| `labels.yaml` | every word of the board — flat `key: value` lines. A German board is this file |

| Place | Whose |
|---|---|
| `tools/shoalmark/brand/` | the organisation that set the repository up — `--vendor` copies and pins it |
| `<tracker dir>/` | the repository |
| `~/.config/shoalmark/` | the person, on their own machine, in every repository |

The name is `name` in `shoalmark.toml`; `tagline` and `footer` are labels. `--brand` says which place gave the
board its theme, logo and labels; `--brand DIR` writes a commented starter there. A theme that is hard to read gets
a warning, never a failure. The four status colours keep their meaning whatever their shade.

## 8. Working on shoalmark

```bash
python3 test_shoalmark.py && python3 test_core.py          # 210 checks; every one builds its own throwaway repository
/usr/bin/python3 test_shoalmark.py                         # the oldest Python promised: 3.9, the one macOS ships
```

Where Chrome or Chromium is installed the board is rendered and read back. `test_core.py` pins the core's
behaviour on a synthetic corpus; `test_shoalmark.py` pins what was built here. A change ships with its check, and
the check is shown to fail without the change. Every consumer-visible change gets a `CHANGELOG.md` entry —
`--vendor` prints it to the repository that upgrades. This repository tracks itself: `python3 shoalmark.py --next`.

## Licence

`Apache-2.0 OR MIT`, at your option — [LICENSE-APACHE](LICENSE-APACHE), [LICENSE-MIT](LICENSE-MIT), [NOTICE](NOTICE).
The one bundled file, `vendor/marked-18.0.13.umd.js`, is MIT. All three ship in a vendored copy.

What it is not, on purpose: no sprint, no estimate, no assignee, no comment thread, no editing in the board.
A viewer, not a Jira.
