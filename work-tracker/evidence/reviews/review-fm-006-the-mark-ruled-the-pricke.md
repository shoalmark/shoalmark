# Review — FM-006, the mark ruled, at 86f8e02 (2026-09-24 01:05 CEST, Reviewer, session `8e509911/reviewer-1`)

**READY TO TAG. Committed with `TZ=UTC`.**
- **Only FM-006 moved:** 4 lines.
- **The quotes are his meaning**, as relayed: *"agreed. a + d lock"* and *"my read is that IBM Plex Mono is the one"*
  are verbatim and so need no *normalised* mark. *Running text Plex Sans* follows the earlier Plex ruling, *sans for
  the pages*.
- **The sources exist:** `a.svg` and `d.svg` are on `fm/006-the-pricke-drawn-to-be-looked-at`, and `a` is the port
  Pricke, fanned up.
- **The timezone bug is reproduced:** at 01:0x CEST, `test_shoalmark.py` fails one check (*rendered: the board's first
  words …*), exit 1. Under `TZ=UTC` it passes, exit 0.
- **Gates under `TZ=UTC`:** `--check` exits 0, and `--session-check` exits 0.
