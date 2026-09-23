# Review — FM-006, the Pricke drawn to be looked at

- **Date:** 2026-09-24, 00:48 CEST (`date`)
- **Seat:** Reviewer (`reviewer@seat`) · **Session:** `8e509911/reviewer-1` · **Model:** Claude Opus 5.5
- **Tip reviewed:** `c428b5e` on `fm/006-the-pricke-drawn-to-be-looked-at`: two commits by `implementer@seat`, session
  `8e509911/implementer-5`.
- **Base:** `origin/main` `b9bcd00`.
- **Committed with `TZ=UTC`,** as the builder did. The brief reports that the pre-commit suite refuses commits between
  00:00 and 02:00 CEST, so this commit's date is in UTC.

## The checks

**The SVGs are hand geometry.**

| file | bytes | colour | raster |
|---|---|---|---|
| `a.svg` | 431 | one, `currentColor` | none (no `<image>`, no `data:`, no base64) |
| `b.svg` | 433 | one, `currentColor` | none |
| `c.svg` | 1,002 | one, `currentColor` | none |
| `d.svg` | 523 | one, `currentColor` | none |

- `a`–`c` are constructed paths: a stake and seven tapered twigs.
- `d` is a pixel grid of 1-unit rectangles on 16 × 16.
- `pricke.py sheet`, run on a scratch copy, **regenerated all four SVGs byte-identical**.

**The renders come from the browser at true size.** They are made the GtM's way: headless Chrome with
`--force-device-scale-factor`, and enlargements by ImageMagick `-filter point`.

| render | size |
|---|---|
| the 16 px files | 16 × 16 |
| the headers | 1440 × 330 at 1x, 2880 × 660 at 2x |

Regenerated in scratch and compared (`magick compare -metric AE`), with **0 differing pixels** each:
- the 16 px renders: `a`, `b`, `c` and `d` light, `a` and `d` dark, and B1;
- both sheets;
- the headers `a` light 1x and 2x, `b` dark 1x and `d` light 1x, rebuilt from a scratch build of `b9bcd00` (Zensical
  0.0.64, *No issues found*);
- `lockups.png`.

**`pricke.py measure` reproduces the note's numbers.**
- *41–50 grey levels, 52–57 part-inked*: printed a 44/52, b 41/54, c 50/57.
- The fan rows: a 2, b 1, c 1.
- `d`: 2 levels, 0 part-inked, and 4 strokes on its widest row.
- B1: 4 levels and 22 part-inked.
- The header: each stake is full ink, 2 px at 1x and 4 px at 2x. The crowns show 6, 5 and 6 strokes at 1x and 7 at 2x.
- The wordmark's ink runs from row 18 to row 31, `a`'s from 15 to 38, and `b`'s top is at row 13.
- Dark: the mark's brightest grey is 189 and the wordmark's 255.

See R1 for the exceptions.

**The chart meanings hold.** de.wikipedia, *Pricke* (raw text fetched at review time) says:
- **Backbord:** *an deren oberen Ende unten zusammengebundene Zweige … (stumpfe Form)*, with a red reflector. These are
  twigs bound at the bottom that splay upward, the *upside-down broom* of the *Besenstraße*. So `a`, fan up, is port.
- **Steuerbord:** *oben zusammengebundene Zweige, die unten auseinandergebogen sind (spitze Form)*, with a green
  reflector, the *Tannen*. So `b`, fan down, is starboard.
- *Es werden überwiegend Backbordpricken verwendet.*

The note quotes all of this correctly.

**The ruling.** The FM-006 row quotes the Owner as *relayed, spelling normalised*, and it is marked. Its meaning is
the note's reading: the meaning gate is waived, and his eye is the gate.

**What is not touched.** Nothing under `site/` in the diff, no consumer or client name or id, and no change to
`docs/`, `zensical.toml` or the theme.

**Gates.**
- `python3 shoalmark.py --check`: exit 0.
- `--session-check` in this worktree judges this seat's own commit: exit 0, because `8e509911/reviewer-1` is open.
- Run as the builder (`GIT_AUTHOR_EMAIL=implementer@seat`, `seat.session=8e509911/implementer-5`), it refuses: *Session:
  8e509911/implementer-5 has no open row*, exit 4. That is expected: the builder closed that row in `c428b5e`.

## Finding

### R1 · P3 · *Every number below is printed by `pricke.py measure`* is not quite true

- **Not printed by `measure`:**
  - the stake's *1.14 px*, which is derived from 2 units at 16/28;
  - the wordmark's stems, *2 px plus a soft edge at 1x*;
  - *pushes the name 4 px to the right*;
  - B1's centre column, *ink without a break from row 21 to row 39*.

  These are unrefuted, but they are not reproduced by the command the note names.
- **Misdescribed:** the note gives *two grey columns (108 of 255)* for the stakes of `a`, `b` and `c`. `measure`
  prints `c`'s stake at row 13 as `[207, 110, 110, 207]`, which is four columns.
- **What closes it:** Have `measure` print these four numbers, or narrow the sentence. Correct `c`'s stake.

## Verdict

**READY WITH FINDINGS: R1 (P3).**

- The SVGs are hand geometry, under 4 KB, one colour, with no raster.
- Every render I regenerated from the browser is pixel-identical to the committed file.
- The chart meanings match the cited source.
- The branch is evidence only and ready for the Owner's eye.
