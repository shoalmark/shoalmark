---
id: FM-006
status: In Progress
considered: FM-005, FM-003
tags: process
next: build
triaged: 2026-09-23
rank: 5
tier: P2
hook: "One README, written for the agent that has to use the tool, is the whole documentation. The people who own the repositories — the first two are German, one runs Windows and Subversion — have no page: not for setting up, not for signing an answer, not for what the first week looks like. And the README must stay the agents' contract, not become a website's copy."
---

# FM-006 — shoalmark has one document, written for agents — the humans who own the repositories have no page of their own

## What is true now

**Filed 2026-09-22 on the Owner's direction:** *"shoalmark has a human- and agent-user facing documentation designed to
the needs of each party."* Ruled the same day, after a trial build: **Zensical** (the successors of Material for MkDocs;
Python, MIT, TOML configuration like the tool's own, no Node, search and dark mode built in; young — 0.0.x) *"because our
product profits from valuing another vendor we seem to align with, early"*; Material for MkDocs is the fallback, and reads
the same configuration.

**The rule that keeps two audiences from drifting apart:** the agents' document is `README.md` — vendored into every
repository, pinned, routed by situation — and it is **never duplicated**: the site renders it as one page and links to it.
Human pages are those with no agent reader: setting up, signing an answer, the standup, the board, the first week. The
site is `docs/`, built by CI to GitHub Pages; `llms.txt` at its root is the agents' index of the same source. German is a
full second language from the first page, because the first two outside owners are German.

**The first human page is the one the day demanded — signing an answer — and it names the risk the Owner found:** a
signature proves which key, not which hand. On a machine agents use, `commit.gpgsign true` makes every agent commit
verify as the Owner. The page says: sign on demand (`-S`), never by default, on such a machine.

**The Owner's requirement for the site, 2026-09-23** (quoted, spelling normalised): *"The site is for humans, so this
one has to be designed like a pitch and sell the idea. Easy, convenient and a one-shot integration mostly done through
your agents."*

## Done when

The site builds in CI from `docs/` and is served; the README is rendered there and not copied; `llms.txt` and the
`.md` twins exist; the human pages exist in English and German — set up · sign · standup · board · the first week; and
one outside Owner has followed the setup page without asking anything.

## Ship log

| Date | Event |
|---|---|
| 2026-09-23 | **The next slice is the pitch**, on the Owner's requirement above: one page an Owner reads in five minutes — the measured claim, the one-shot setup his agents run, what he signs, what an answer costs him; German first. Not built tonight. The pages are eight releases stale (0.17.0 → 0.17.8), and Pages deploys only for a public repository (D5). |
| 2026-09-23 | **The human pages open from a file** (the Owner's finding: *"clicking links does not work currently because it tries to open files"*): `use_directory_urls = false` — links are `setup.html`, not `setup/` — and `navigation.instant` dropped, whose page fetches `file://` blocks. Built with Zensical 0.0.64: the start page's local links are all `.html` and 133 of 145 local links across the site resolve to files on disk (the 12 others are `404.html`'s absolute `/shoalmark/…` paths, for Pages); a click on *Set up* in headless Chrome from `file://…/site/index.html` opens `setup.html`. The setup pages (EN, DE) say how to open or serve the built site. The content refresh is the next slice. |
| 2026-09-22 | The site builds green in CI; Pages refuses a private repository (*"Upgrade or make this repository public"*). The deploy step waits for the public release, by condition in the workflow. **Ruled the same hour: CI runs only on a ready pull request and on a release tag — minutes are paid for; the site builds on a tag.** |
| 2026-09-22 | Filed; Zensical tried on a scratch build first (0.3 s, search and dark mode in, four anchor warnings from the README); the signing page written. |
