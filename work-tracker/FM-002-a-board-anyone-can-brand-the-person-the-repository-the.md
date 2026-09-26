---
id: FM-002
status: In Progress
considered: FM-001
next: build
ask: "Which theme do shoalmark's own board and site wear — the brand layer and the site's stylesheet, no tool change — and, separately, does the tool ship themes: `brand/themes/` and `--brand DIR --from <theme>`, code whose files every vendoring consumer receives?"
ask-kind: ruling
ask-since: 2026-09-26
ask-options: "shoalmark's own board and site wear the shoalmark theme; the tool ships no themes yet | the tool ships monochrome and shoalmark as starters; shoalmark's own board and site wear the shoalmark theme | not yet — shoalmark's own board and site keep today's look; the tool ships no themes"
ask-proposal: "shoalmark's own board and site wear the shoalmark theme; the tool ships no themes yet"
answer: "accepted - the tool ships monochrome and shoalmark as starters; shoalmark's own board and site wear the shoalmark theme"
answered: 2026-09-26
answered-by: holgo99
triaged: 2026-09-26
rank: 4
tier: P2
hook: "The board can carry a name in the browser tab and a theme.css — nothing else: no name on the page, no logo, English only. And several kinds of user want to brand it at once: several people looking at one repository's board, several repositories, an organisation shipping its house brand into every repository it sets up. One rule, three files, four places — to be proven before it is built."
---

# FM-002 — A board anyone can brand — the person, the repository, the organisation

## What is true now

**Raised 2026-09-26 on the Owner's word, re-opened for the brand's themes, and ruled by his signed answer of 13:54:50 (`4e00f85`, PR 90, option 2, not the proposal): *the tool ships monochrome and shoalmark as starters; shoalmark's own board and site wear the shoalmark theme* — both slices in; the build judged the same day before its first build commit (FM-033; the worksheet `evidence/triage/triage-2026-09-26.md`, `keep P2 #4 build`).** What shipped as 0.8.0 stands. The themes are mocked as FM-006's evidence (`evidence/FM-006/themes/` — the aligned board at `9467b83`, PR 82): `monochrome` and `shoalmark`, each for the board and the site. **Slice A**, the brand layer only: shoalmark's own board and site wear the `shoalmark` theme — `work-tracker/brand/theme.css` from it, two Plex Mono cuts (SemiBold, Italic; Latin-1 from `@ibm/plex-mono` 1.1.0, hashed as the Regular is), the site's `docs/stylesheets/`; no `shoalmark.py` change. **Slice B**, ruled in by the answer: the tool ships both as starters (`brand/themes/`, `--brand DIR --from <theme>`; code tier; a line on what vendoring consumers receive; the default look of a consumer that chooses nothing stays), with the three markup hooks the mocks used, where the pass placed them. A and B are built in parallel, each on its own branch, A's `theme.css` re-cut on B's hooks after B lands; nothing was built before his answer and the pass's judgement (FM-033), and the order is after the `v0.18.4` tag (made today, 09:58). Carried into the build: AU-16 (every `::before`/`::after` marker with empty alt text, and the chart's coordinate labels hidden from screen readers), AU-18 (the Owner's box at about 100 characters of prose per line), contrast at 4.5:1 on every pair in both schemes re-measured on built files, real renders before and after in both schemes at desktop and phone width seen by the Owner before the merge, the site built at the next release tag and live only at the go-public act (`docs.yml` deploys only while the repository is public; FM-006). **The tier is today's pass's: P2** — TRIAGE.md's current path does not name the restyle and nobody is harmed today; it is P1 the day the Owner writes it into his current path by his own signed commit, which FM-037's guard alone admits.

**Slice A built — 2026-09-26, on `fm/002-slice-a-the-brand-layer`, not merged:** shoalmark's own board wears the `shoalmark` theme from `work-tracker/brand/theme.css` — the aligned mock, the header inline inside the chart — with Plex Mono SemiBold and Italic beside the Regular (sha256 `1ce95cff…`, `08c4566f…`), and the site from `docs/stylesheets/shoalmark.css` (one Google Fonts import; FM-006's self-hosting item stands); two rules are not the mock's, added where the built files measured a text pair below 4.5:1; AU-16, AU-18 and every text pair at 4.5:1 or more in both schemes are measured on the built files (lowest 5.76:1 by day, 5.98:1 by night), and the renders before and after, both schemes, 1440 and 390 px, are in [`evidence/FM-002/slice-a/`](evidence/FM-002/slice-a/README.md) — for the Owner to see before the merge, with one Reviewer pass due; the three markup workarounds stay until slice B's hooks; the site is built at the next release tag and live at the go-public act.

**Shipped as 0.8.0 — merged by the Owner (#1) after the R&D; the origin's board wears its real brand from it.** Three optional files (`theme.css`, `logo.svg`,
`labels.yaml`) in three places plus the defaults — the vendored tool's `brand/`, beside the trackers, the person's
`~/.config/shoalmark/` — the later one winning, and **no setting**. Nine of eleven pre-registered claims held
outright, on the origin's real logo, brand tokens and fonts and on a German copy of the first client's board; one was
false as first built and fixed (a theme whose import is missing); the core grew more than its bar allowed. The
record, with what was found that nobody had named: [the R&D file](evidence/FM-002/brand-layers-rd.md).

## Why

The first client's staff read German. The origin has a brand. A consultancy setting a repository up for a client
wants its mark on it until the client's replaces it. And two people committing to one repository must never fight
over a generated file because their boards look different.

## Done when

Every pre-registered claim has an outcome under its forecast; the Owner has ruled on the merge; on merge, the
README explains the whole feature in one section of at most 25 lines. *(Met, 0.8.0, 2026-09-21: merged by the Owner, #1, and released — the ship log's row; `3339b79` set it Shipped, and its README's section 9, Branding the board, is 21 lines.)*

**The themes, raised 2026-09-26 — done when:** slice A: shoalmark's own board and site wear the `shoalmark` theme, as the Owner's answer names it, from `work-tracker/brand/theme.css` and `docs/stylesheets/`, the two Plex Mono cuts (SemiBold, Italic) hashed beside the Regular, the board's header inline inside the graticule as his word of 09:23:58 draws it, no `shoalmark.py` change; the renders before and after, both schemes, desktop and phone width, seen by him before the merge; AU-16 (markers and the chart's coordinate labels silent to screen readers) and AU-18 (the Owner's box at about 100 characters of prose per line) held, every text pair at 4.5:1 in both schemes, re-measured on the built files; one Reviewer pass on the branch; the site built at the next release tag and live at the go-public act (FM-006). Slice B, ruled in by his answer (option 2): `brand/themes/` holds both starters, `--brand DIR --from <theme>` writes one, the suites cover it, the CHANGELOG names it and what a vendoring consumer receives; the default look of a consumer that chooses nothing unchanged. Both judged by a pass before their first build commit (FM-033) — the pass of 2026-09-26, `keep P2 #4 build`.

## Raised

*One sourced line per raise — the date, who raised it, the fact, its source, what it undermines; no counts.*

- 2026-09-26 · the Owner — *proceed with the board's themes and bring the mockups into the dashboard and the site* (07:41:00, through the Auditor seat; his paste of 07:55:40, sha256 `34ee13d1…`); *for the dashboard I prefer the inline header … align for both; all dashboards aligned over all themes; the site's renderings are excluded* (09:23:58, in chat, spelling normalised; sha256 `21497e4d…`); *go — raise FM-002 as proposed; … for the v0.18.5 release we also add a landing page requirement alongside the restyle and rebrand of shoalmark's brand identity* (10:25:41, in chat, normalised; sha256 `416d54ce…`; the three hashes are the Principal's paste files', reported for the Auditor seat's match — the words themselves stand in the Principal's transcript at the times named, and the three files filed whole, byte for byte, each under a 3-line head: `evidence/FM-002/owner-words-2026-09-26-0741.md`, `evidence/FM-002/owner-words-2026-09-26-0923.md`, `evidence/FM-002/owner-words-2026-09-26-1025.md`) · the fact: two themes are mocked for the board and the site (FM-006's evidence) and the brand layer this tracker shipped carries none; the restyle is his line for 0.18.5 · undermines no signed rule — it widens this tracker's shipped scope, so the same-day pass is the seat's choice on his word, not the raise rule's.

## Ship log

| Date | Event |
|---|---|
| 2026-09-26 | **Slice A built** — the brand layer, no `shoalmark.py` change, by the Implementer seat (`8e509911/implementer-36`) on `fm/002-slice-a-the-brand-layer` off `2a9f7eb`, judged before its first build commit by the pass at `13d70189`: the board's theme and the two Plex Mono cuts (`349fbe8`), the site's stylesheet (`73ea047`), two text pairs the built files measured below 4.5:1 fixed — the board's placeholder 3.63:1, the site foot's link 1.12:1 (`361336a`), the renders before and after (`5ff3539`), the checks carried — AU-16 with its control, AU-18 at 99.8 characters, 746 contrast measurements a scheme, none below 4.5:1, the tracker view aligned as the mock (`11faa03`). Not merged: the Owner sees the renders first; one Reviewer pass. |
| 2026-09-26 | **Raised on the Owner's word and re-opened for the brand's themes** — status In Progress by the Principal seat; the themes' ask on the board (a ruling: which theme shoalmark's own board and site wear, and, apart, whether the tool ships themes; three options of 85, 108 and 84 characters; the proposal the GtM seat's, disclosed — the cheap step first), moved here from FM-006's body, where it was re-made on AU-24 (`7344a78`) because FM-006 holds its one ask (going public) and the freeze bars a new tracker; the slices, the carry-overs and the tier's reason in *What is true now*; judged by today's pass (its worksheet and TRIAGE.md's *Passes*). Nothing built. |
| 2026-09-21 | **Merged (#1), released as 0.8.0.** First real use: the origin — an 8-line theme importing its brand tokens, its micro mark linked, two labels; looked at in a browser there in both schemes. The German labels wait for the first client's repository. |
| 2026-09-21 | Spiked on `rd/fm-002-brand-layers`: 9 of 11 claims held outright; 90 + 144 checks green on Python 3.14 and 3.9; the outcome is under the pre-registration. Not merged. |
| 2026-09-21 | Filed; the pre-registration committed before the spike. |
