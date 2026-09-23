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

**Ruled 2026-09-23 ≈ 23:35, the Owner, in chat, after the GtM's claim and mark screens:** the German claim is *"Dein Eigner bremst. Tunen statt tauschen."* (the screen's survivor for both readers; applied to `docs/de/index.md` here); the typeface family is **IBM Plex** (sans for the pages, mono for the board — the board's Berkeley Mono is mono-only and commercially licensed; the site change is the next slice); the mark: one survivor of thirteen, **B1, the isolated-danger beacon** (two balls on a stake), held until two or three stand-in readers and one sailor have seen the header and the 16 px tab — never the investor; if they read an *i* first, it dies. The GtM's seven findings on the pitch stand open for the next slice: the adopt note still pins v0.12.0 (P1, first), an internal id on the pitch (P2), the tagline's *on the chart* where the mark stands in the water (P4, the Owner's words), the record-before → reset → record-since frame and *the rule* unexplained (P3, on his *go*), dashes (P5), the last-message line stated as enforced (P6), no dark mode; P7 is closed by the claim above.**

**Ruled 2026-09-23 22:5x, the Owner, in chat: the pitch has two readers — an outside Owner of a fleet (the first two are German, one on Windows and Subversion) and a German tech investor fluent in English, *"indeed one of my audiences I am in contact with"*. Every gate of the claim screen is read for both; where they pull apart, the page says which reader a line is for.** The measured sentence now states its size — *one project, our own, its first day* — until the week's count exists (the GtM's flag, the Principal's edit).

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

**One claim, the Owner's:** the pitch carries *Get a better-performing human Owner.* (DE: *Hol dir einen
leistungsstärkeren menschlichen Eigner.* — in German prose the person is *der Eigner*, on his word), his wording, sharpened from *How to get a better-performing human owner*. It
faces the fleet and provokes the owner at once, and the page below it proves it for both readers. The README keeps its
own section title: it is the agents' contract, not the pitch. A second, owner-facing claim is open for a GtM screen the
Owner convenes; no seat writes it.

## Done when

The site builds in CI from `docs/` and is served; the README is rendered there and not copied; `llms.txt` and the
`.md` twins exist; the human pages exist in English and German — set up · sign · standup · board · the first week; and
one outside Owner has followed the setup page without asking anything.

## Ship log

| Date | Event |
|---|---|
| 2026-09-23 | **The German claim ruled and applied** — *Dein Eigner bremst. Tunen statt tauschen.* — and IBM Plex ruled as the typeface family; the mark screen's survivor B1 held for the stand-in readers; the pitch's seven findings queued (P1 first). The GtM's ledgers: `evidence/FM-006/gtm-claim-screen-2026-09-23.md`, `gtm-mark-screen-2026-09-23.md` (branch `fm/006-gtm-mark-screen`, the Owner's PR). |
| 2026-09-23 | **Two readers ruled by the Owner** (an outside Owner; a German tech investor fluent in English) after the GtM's second pass screened for the investor without a ruling; the measured sentence cut to its real size in both languages — *one project, our own, its first day*. The GtM's ledger on `fm/006-gtm-claim-screen` (0d22563, ba43112): the current German claim fails its own G0 (two adjectives, HR German, mirrored order); two candidates survive every gate of the screen as the seat's judgment (its correction of this row's first wording, which said *G3 unrun* — the seat ran G3, the Owner's *never*; what is unrun is a search for existing use of the slogan, which the ladder never had as a gate, and any real reader); the reader question and *bremst* as provocation or insult are the Owner's to rule. Its third pass (f1e525a) says which reader each line works for and hands the Owner a reader test: five seconds on the top of the page, one claim each rotated, three questions the next day, the kill rules fixed before anyone reads. |
| 2026-09-23 | **Eigner for the person in German, on the Owner's word:** the seven German uses of *Owner* for the person — the claim (*Hol dir einen leistungsstärkeren menschlichen Eigner.*), the owner's block, the measured line, *start here*, two in `setup`, one in `signing` — now say *Eigner*; the seat name `owner`, the `[seats]` key, commands and quoted refusals stay English. |
| 2026-09-23 | **The claim sharpened on the Owner's word, his wording:** *Get a better-performing human Owner.* / *Hol dir einen leistungsstärkeren menschlichen Owner.* — in both pitches and the site's description; the line under it keeps *owner*; the README's title stays the agents'. |
| 2026-09-23 | R7: the span of the count is *just over a day* / *gut einem Tag* (27 h 50 min, the ruling to the count's tip), not a day and a half. R8: the English signing page says shoalmark lower-cases the branch it creates and git keeps the case it is given. |
| 2026-09-23 | R6: the German pages read natively — the Reviewer's sixteen rewordings, and one word each: *Standup* for the Owner's daily sitting, *Session* for an agent's run, never *Sitzung* for both. The board's German labels (`sessions.open`, `reviews.week`) still say *Sitzung*: aligning them is a tool change for the next release. |
| 2026-09-23 | R5: the signing pages name the answer branch as the tool cuts it, `answer/ap-007`. Proved on a scratch answer (`--answer AP-007 accept`, SSH-signed, pushed to a bare remote): `git log -1 --format=%G? answer/ap-007` prints `G` loose and after `git pack-refs --all`; `answer/AP-007` then fails, *unknown revision*. |
| 2026-09-23 | **Withdrawn on the Owner's word:** the seat's claim candidates are out; his line stands alone — *How to get a better-performing human owner.* (`589d328`); a second claim is a GtM screen he convenes. The row *The pitch built* below is restored as `76d1872` wrote it (R4): the ship log is append-only. |
| 2026-09-23 | R3: the pitch's measured paragraph cites what the consumer's record on its `main` holds — before, the last 200 pull requests merged unread, none reviewed; after, in a day and a half, 9 of 13 carried a Reviewer's file before they were opened — and no longer says *independent*: the board reports it, and git cannot yet prove it. |
| 2026-09-23 | **The pitch built**, on the Owner's ask (*"Can we get the site all pumped up for a pitch to somebody?"*): `index.md` in German first and English — the name, the line under it (*ein Zeichen auf der Karte, das die Flotte vom Grund fernhält* / *a mark on the chart that keeps the fleet off the shoal*), two claims side by side, *to the fleet* — *How to get a better-performing human owner.* — and *to the owner* — *Your agents are faster than you. Good. Now stop being the queue.*; the three measured numbers (no consumer named); the one-shot setup the agents run; what a day costs; what it is not; where to start. `setup`, `signing`, `standup` brought to 0.17.8 (`[seats]`, sessions, `--answer`, the verdict count), `de/standup.md` added. **The alternates, the Owner's to choose:** to the fleet — *Your owner is the slowest thing in the fleet, and the only one who may decide. Keep the second, fix the first.* · *Stop waiting for your human. Put what needs him first, and make his answer one command.*; to the owner — *Sign once. Read the digest. Press nothing you did not ask for.* · *Fifteen minutes a day, one signature, no stamping — and a record that shows who did what.* |
| 2026-09-23 | **The next slice is the pitch**, on the Owner's requirement above: one page an Owner reads in five minutes — the measured claim, the one-shot setup his agents run, what he signs, what an answer costs him; German first. Not built tonight. The pages are eight releases stale (0.17.0 → 0.17.8), and Pages deploys only for a public repository (D5). |
| 2026-09-23 | **The human pages open from a file** (the Owner's finding: *"clicking links does not work currently because it tries to open files"*): `use_directory_urls = false` — links are `setup.html`, not `setup/` — and `navigation.instant` dropped, whose page fetches `file://` blocks. Built with Zensical 0.0.64: the start page's local links are all `.html` and 133 of 145 local links across the site resolve to files on disk (the 12 others are `404.html`'s absolute `/shoalmark/…` paths, for Pages); a click on *Set up* in headless Chrome from `file://…/site/index.html` opens `setup.html`. The setup pages (EN, DE) say how to open or serve the built site. The content refresh is the next slice. |
| 2026-09-22 | The site builds green in CI; Pages refuses a private repository (*"Upgrade or make this repository public"*). The deploy step waits for the public release, by condition in the workflow. **Ruled the same hour: CI runs only on a ready pull request and on a release tag — minutes are paid for; the site builds on a tag.** |
| 2026-09-22 | Filed; Zensical tried on a scratch build first (0.3 s, search and dark mode in, four anchor warnings from the README); the signing page written. |
