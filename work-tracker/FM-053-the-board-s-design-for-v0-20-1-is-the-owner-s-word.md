---
id: FM-053
status: In Progress
considered: FM-002, FM-023, FM-024, FM-031, FM-006
tags: process
next: owner
triaged: 2026-10-15
tier: P2
hook: "The board's design for v0.20.1 is the Owner's word in a design sitting, and a Builder acts only on a signed word"
ask: "Do you adopt the guide's amendment of 16 October, G1 to G8 (three colour meanings, section and state surfaces with their dividers, the guided answer view with its links and signing words), as brand/design-guide.md states it at the commit that last filed this ask?"
ask-kind: ruling
ask-since: 2026-10-16
ask-options: "yes | yes, with the change I name | no: the guide stays as its first answer adopted it"
ask-proposal: "yes"
---

# FM-053 — the board's design for v0.20.1 is the Owner's word in a sitting, not yet a signed answer

## What is true now

**Filed and judged 2026-10-15: In Progress, P2.** `brand/design-guide.md` and `brand/icons/` were added under this
tracker in `ef33598`. The ask was filed at `2876287`, filed again at `fbf6ef0` with the label `viewer.handover`
("handover") in the guide's §10, and is filed again at the commit that sets the light `--mute` and `--teal` to reach
4.5:1 against `--raise`, so that the answer adopts the guide with them, and with its §4 the icons, as they stand
there. Nothing in them is built into the board.

**2026-10-16 — answered, then amended.** The Owner's signed answer adopts the guide as it stood at `82b8c15` (accepted,
`1281a75`; its record is under `## Asks`). The same day, in a design sitting, the Owner approved the board with surfaces
and three colour meanings, and the guided answer view; neither is signed. G1 to G8 are written into the guide at the
commit that files this tracker's new ask:
- G1, three meanings, one colour each: teal for done or success, amber for a warning, coral for a failure. `[palette]`'s
  keys `heed` and `go` become `fail` and `ok`, and `warn` is added; `[palette]` has never shipped, so no migration is
  needed;
- G2, surfaces: a band behind each section heading of the box, and tints for a state the tool computed;
- G3, a verdict's row on its meaning's tint, its word in its colour;
- G4, rows that line up, the id in a column of its own;
- G5, a diff for the change a command commits;
- G6, the guided answer view, a new component;
- G7, its one help line, inside the dialog's window;
- G8, each band's top edge a 1px `--box` rule, so that the band is the divider; none above the first band.
- On 15 October the Owner decided how the board looks and reads: one look, `monochrome`, on the board's own tokens, in
  the system's monospace, with no chart behind it; a box only for an action; type, state and action told apart; what
  waits for you first. The guide is the public form of those decisions, the v0.20.x rules only.
- It lands in v0.20.1 with B1 (FM-023's table of 2026-10-15). With it, R10's look half: theme layering, the font files,
  theme copying and the inline wordmark go, and a palette by name or by a few tokens in `shoalmark.toml` takes their
  place, refused below a set contrast. Every board build names each brand file it no longer reads, with the setting that
  replaces it.
- **No choice is left in it.** The box keeps its titled frame. A board's palette defaults to `monochrome`, and the
  nautical chart leaves every board. `shoalmark` stays the palette of the public pages, the landing and the docs.
- **This answer replaces FM-002's answer of 26 September for the board:** this repository's board wears `monochrome`, not
  `shoalmark`. Its `work-tracker/brand/theme.css` goes as a leftover, as for any adopter, and no `[palette]` is set here.
- The board build builds to the guide as answered, and to G1 to G5 of the amendment; the amendment's answer gates its
  merge.
- **Not in this answer:** R6, held to 20 October; whether the board's run reads the harness folders' file names, which
  copy-to-resume needs (R6's look); the receipts' definitions (FM-055); whether a harness id may sit in a board's file;
  the README's picture. Each is its own ask.

## The public homes

- **`brand/design-guide.md`**: the board's design, the v0.20.x rules only. It is what this tracker's ask adopts, as it
  stands at the commit that files the ask. A rule there changes only by the Owner's signed answer.
- **`brand/icons/`**: the board's four UI icons (copy, check, cross, out) and a README of their family rule, as
  `brand/seats/README.md` has for the seat icons.
- **`examples/sample-board/README.md`**: the sample repository the README's picture of the board is rendered from,
  with its caption and alt text. It lands with the first board build, with its images. `examples/de/tafel.png` becomes
  `examples/de/board.png`, rendered from the v2 board.
- **Images:** every public image of the board is a real render of the shipped board from the sample; design mockups
  are not published.
- **AGENTS.md**, one line after the generated block's end marker, with the first board build: *Board work — the board's
  look, its words, and its sections' command-line output — follows `brand/design-guide.md`; a rule there changes only
  by the Owner's signed answer.*

## Done when

- The Owner's signed answer stands here, and the board build's brief cites it.
- The board build's review checks the board against the guide's acceptance tests (§11).

## Asks

**2026-10-16** · Do you adopt brand/design-guide.md, as it stands at the commit that last filed this ask, as the design and the words the v0.20.1 board is built to?
**answered** — accepted - yes · holgo99
**relation** — accepted the proposal
**signed** — 1281a75 · G

## Ship log

| Date | Event |
|---|---|
| 2026-10-15 | Filed and judged on `release/v0.20.1`: In Progress, P2. The guide and its icons are built under it, with its ask. |
| 2026-10-15 | `brand/design-guide.md` and `brand/icons/` (four SVGs and the README of their rule) added under this tracker, `ef33598`. |
| 2026-10-15 | The ask filed: it adopts the guide as it stands at this commit. Nothing is built into the board. |
| 2026-10-15 | The ask filed again, at the commit that adds the label `viewer.handover` ("handover") to the guide's §10. |
| 2026-10-16 | The light `--mute` becomes `#6a6a6a` and the light `--teal` `#187953`, so that every text colour reaches 4.5:1 against `--raise`, as the guide's own contrast rule requires. The ask filed again at that commit. |
| 2026-10-16 | The first answer recorded under `## Asks` (accepted, signed `1281a75`); next: build. |
| 2026-10-16 | The guide's amendment, G1 to G7, written in, with the ask that adopts it (`next: owner`). |
| 2026-10-16 | The section band's token is `--secbg`: `--band` is already the `shoalmark` theme's navy band, on which every section heading would read at about 1.2:1. The ask filed again with it. |
| 2026-10-16 | G6 takes the go-to-market seat's words for what a key's confirmation is and is not; the ask filed again with them. |
| 2026-10-16 | The Designer's full pass folded in: G8, each band's top edge a 1px `--box` rule, none above the first band, and its wording of G1 to G7. G6 keeps the go-to-market seat's signing words. The ask filed again with it. |
| 2026-10-16 | The Designer's fidelity check fixed forward: a consequence stays amber in §8 *Help*; a verdict's word at weight 600; the dialog's teal rule in test 2; the palette's surfaces; `commit_url` before `blob`; one wrap. The ask filed again with them. |
