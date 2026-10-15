---
id: FM-053
status: In Progress
considered: FM-002, FM-023, FM-024, FM-031, FM-006
tags: process
next: build
triaged: 2026-10-15
tier: P2
hook: "The board's design for v0.20.1 is the Owner's word in a design sitting, and a Builder acts only on a signed word"
---

# FM-053 — the board's design for v0.20.1 is the Owner's word in a sitting, not yet a signed answer

## What is true now

**Filed and judged 2026-10-15: In Progress, P2.** The next commit adds `brand/design-guide.md` and `brand/icons/`
under this tracker, and files the ask that adopts them; nothing in them is built into the board.
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
- Until the answer, no Builder builds to the guide.
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

## Ship log

| Date | Event |
|---|---|
| 2026-10-15 | Filed and judged on `release/v0.20.1`: In Progress, P2. The guide and its icons are built under it, with its ask. |
