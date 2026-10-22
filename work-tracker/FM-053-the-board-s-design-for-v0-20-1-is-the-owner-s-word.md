---
id: FM-053
status: In Progress
considered: FM-002, FM-023, FM-024, FM-031, FM-006
tags: process
next: build
triaged: 2026-10-15
tier: P2
hook: "The board's design for v0.20.1 is the Owner's word in a design sitting, and a Builder acts only on a signed word"
ask: "Do you adopt the guide's wording of 16 October for the board's reload, as brand/design-guide.md states it at the commit that last filed this ask: it reads its file again when you come back to it, and nothing polls?"
ask-kind: ruling
ask-since: 2026-10-16
ask-options: "yes | yes, with the change I name | no: §2.8 and the read-at line stay as answered at fee3874"
ask-proposal: "yes"
answer: "accepted - yes"
answered: 2026-10-16
answered-by: holgo99
---

# FM-053 — the board's design for v0.20.1 is the Owner's word in a sitting, not yet a signed answer

## What is true now

**The polish's fix round (2026-10-22), after its review NOT READY at `4c1441e`:** the switch drawn as a track and a knob (BF-68) and the pressed-button rule gone (RV-3660) — `b7c91c7`; one space between a day row's state and its warning (BF-69) — `8b91b91`; the German table takes the go-to-market seat's words rows, revision 3, G1 and G3 to G41, its §3's two changes, F1 to F7, F9 and F10 — `cf81e41`, not F8; the reviews' fold takes its row, G2 (RV-3663) — `b8ec2ae`, so `b4901a5` stays in v0.20.1; the lane's narrating comments go (RV-3662) — `53815d7`; a branch's merge id links where the forge holds it (RV-3664) — `372c089`; and BF-62 is recorded as layout only (RV-3661) — `068de48`.

**The board's polish for v0.20.1, built on `fm/053-board-polish` from main after #183 (2026-10-22):** the header's search on one line and its count in the toolbar (BF-50), light or dark as one switch (BF-51), the toolbar's radios (BF-52), the box in the story view (BF-53), the logo by the board's scheme (BF-54), each work row stacked on a phone (BF-55) — `cb35bce`, `2bcab37`; the footer, the claim removed and the running line alone at the right — `c89fa3f`; and the riders BF-29, BF-56 and BF-57 — `172e2eb`. The reviews section's BF-61, BF-62 — its layout only — and BF-64, begun before the Designer's triage (recorded privately), stand at `b4901a5` for the Designer's check and the review to decide; BF-62's state labels are not built, and go with BF-65 to v0.20.2. The triage moves the rest to v0.20.2: BF-30 with BF-49, BF-58, BF-62's state labels, BF-63, BF-65 to BF-67, and the seat icons.

PR C - RV-3593: block 150 checks the short read-at line and its limits
fold, retains the no-count record check, and rejects the changed-path-read
mutant. Its header was cut to the block's title under the comment rule;
executable code, docstrings and page bytes are unchanged.

**Filed and judged 2026-10-15: In Progress, P2.** `brand/design-guide.md` and `brand/icons/` were added under this
tracker in `ef33598`. The ask was filed at `2876287`, filed again at `fbf6ef0` with the label `viewer.handover`
("handover") in the guide's §10, and is filed again at the commit that sets the light `--mute` and `--teal` to reach
4.5:1 against `--raise`, so that the answer adopts the guide with them, and with its §4 the icons, as they stand
there.

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

**2026-10-16 — the reload, said as it is.** The board reloads its file when its tab is visible again (FM-006, `3db8375`), and the
Owner keeps that. §2.8's *nothing refreshes itself* and the read-at line's *this page does not update itself* said
otherwise. Both now say *it reads its file again when you come back to it; nothing polls*, and this tracker's ask
adopts that wording. The Designer checks it.

**2026-10-16 — A2, the board's v2 look and words, is built** on `fm/053-board-v2`: R10's look half (theme layering, the
font files, theme copying and the inline wordmark go; `[palette]` takes their place, refused below the set contrast, and
each brand file the board no longer reads is named), the board to the guide as answered and to G1 to G5 and G8 of the
amendment, and B1's signing words. Its first review was NOT READY at `2c8d041` (`76c1ccd`): the header row on a phone, a
palette name that is a list, this tracker's line that nothing was built, and a review row's branch. Round 1 fixes the
four on the branch, and with them the Designer's build findings on `2c8d041`: the work table's group line and the
header's count inside the frame, *you* for `next: owner`, a heading's marker on a phone, a review row's sessions and its
heading's counts, *shipped or closed* for *ended*, and a count past 14 asks. The reload stays, as the Owner ruled. What
remains:
- the second review round and the Designer's build check, on round 1's head;
- CI: its browser checks (among them the header row at 375, 640 and 880 px), the documentation build and
  `scripts/check_site.py`, which run there and not on the build's machine;
- integration into `release/v0.20.1` with the board's other builds, where its CHANGELOG and ADOPT lines are written.

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

**2026-10-16** · Do you adopt the guide's amendment of 16 October, G1 to G8 (three colour meanings, section and state surfaces with their dividers, the guided answer view with its links and signing words; every stated ratio measured), as brand/design-guide.md states it at the commit that last filed this ask?
**answered** — accepted - yes · holgo99
**relation** — accepted the proposal
**signed** — fee3874 · G

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
| 2026-10-16 | The docs pass's two ratio findings fixed forward: the dark `--box` ratio is 2.1, and §13's help ratios are 6.4:1 and 9.0:1. The ask filed again with them. |
| 2026-10-16 | The amendment's answer recorded under `## Asks` (accepted, signed `fee3874`); next: build. |
| 2026-10-16 | The reload's wording amended in §2.8 and the read-at line, with the ask that adopts it (`next: owner`). |
| 2026-10-16 | A2 built on `fm/053-board-v2`: the v2 look and words, R10's look half and B1. Its first review NOT READY at `2c8d041` (`76c1ccd`), four findings. Round 1 on the branch: a palette name that is a list refused in one line (`8597bd7`), a review row's branch (`319ac53`), the header row on a phone (`db21666`), and this record. |
| 2026-10-16 | The Designer's build findings fixed in round 1: the work table's group line wraps (`4b425b0`); the header's count stands clear of the scheme's button (`5e38e08`); `next: owner` reads *you* (`f37b5b5`); a heading's marker keeps its space on a phone (`cbb49c3`); a review row names the branch's oldest session (`5bb4fb7`); its heading's counts put the number first (`eeacb1c`); *shipped or closed* for *ended* (`e6031e5`); a count past 14 asks (`8ee3602`). The reload stays, as ruled. |
| 2026-10-22 | The board's polish built on `fm/053-board-polish`: BF-50 to BF-55 (`cb35bce`, `2bcab37`), the footer (`c89fa3f`) and the riders BF-29, BF-56, BF-57 (`172e2eb`); BF-61, BF-62 and BF-64 (`b4901a5`) wait for the Designer's check and the review; the rest moves to v0.20.2. |
| 2026-10-22 | Correction (RV-3661): `b4901a5`'s message says it closes BF-62; it builds BF-62's layout only, a verdict's second line that flows as text. BF-62's state labels are not built, and go with BF-65 to v0.20.2. The rows above stand as written. |
| 2026-10-22 | The polish's fix round on `fm/053-board-polish`: BF-68 and RV-3660 (`b7c91c7`), BF-69 (`8b91b91`), the German of revision 3 (`cf81e41`), RV-3663 with G2 (`b8ec2ae`), RV-3662 (`53815d7`), RV-3664 (`372c089`) and RV-3661 (`068de48`); `b4901a5` stays in v0.20.1. |
