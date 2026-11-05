---
id: FM-152
status: Proposed
considered: none
next: wait
hook: "go-to-market asked, for the Owner, for a light revision of the software-factory X post image: new headline, plain-words stand-up, and BOARD cards that read as agents asking. An earlier version of this image was made outside this repository; this tracker holds the revision."
---

# FM-152 — An X post image: the agents never answer for you — the software-factory loop

## What is true now

**Filed 2026-10-27. A render exists in `evidence/FM-152/`; the Owner has not judged it; it is not final.**

- **The render:** `work-tracker/evidence/FM-152/shoalmark-software-factory-x.svg`, written by `build-sf.py`, and its export
  `shoalmark-software-factory-x.png`, 1600 × 900, by headless Chrome (the README's export method). Same four-station loop as the earlier
  version of this image, made outside this repository, with three Owner-approved changes only:
  1. Headline: *the agents never answer for you.* (Owner's choice of the stricter line, via go-to-market; was *the agents never make your calls.*, before that *shoalmark is a software factory.*)
  2. STAND-UP: *you answer,* / *one at a time* in plain words, two centred lines (was `--answer <id>` / *one at a time*). *your commit*,
     *signed if configured*, *you run it* kept.
  3. BOARD: the ask cards read *waiting for you* (top) / *waiting…* (rest); *↑ oldest first* and *next: owner* kept.
  Loop, crew (planner · builder · reviewer · auditor with seat words), colours, return arrow (*the answer → next: build*),
  Pricke + wordmark, embedded Plex Mono 600, 8-bit swell, *shoalmark.tools*, and no logos but shoalmark's own: unchanged.
- **Accuracy, checked against this repository (tool at `915cc57`, `shoalmark.toml`):**
  - *answer:* is written by the Owner in their own commit; seats cannot write it (`--schema`). Only the Owner holds
    `answer`. So the headline, for Owner answers, is true here.
  - The Owner is named and marked `signed` (the `owner` line in `shoalmark.toml`). `--answer` therefore signs
    (`git commit -S`). *signed if configured* stays as written (true of the tool; here it is configured).
  - `next: owner` and oldest-first ask order hold: `owner_queue` sorts by `ask-since:`, oldest first; `--standup` groups
    by kind then frees-the-most then oldest (so *oldest first* stays the BOARD's label).
  - Seats do make other calls of a kind: planner holds `ask` · `close` · `triage`, reviewer holds `triage` — they judge
    worksheets, close work, and write asks. The Owner chose the stricter headline *the agents never answer for you.*
    (relayed via go-to-market); the earlier brief's *never make your calls* is superseded.
  - TRIAGE.md's two sections are the Owner's (AGENTS.md; FM-037 is guarded here because the Owner is named).
- **The font is the embedded one:** IBM Plex Mono 600 from `brand/social/repository-card.svg`, under a family name only
  the embed defines; with the embed removed, 54 088 pixels change.
- **Safe zone:** lockup, words, stations and crew within x 112–1488, y 96–812, inside the 80 px inset (80–1520 × 80–820);
  a centred 2 : 1 (y 50–850) or 1.91 : 1 (y 31–869) crop keeps them (`check-safe-zone.png`).
- **Checked small and in grey:** `check-400x225.png`, `check-grey.png`, `check-grey-400x225.png`.

## Why

This image is not a chapter of FM-147 (*Shoalmark on Grok Bot*). go-to-market briefed the designer seat, for the Owner.

## Done when

The Owner has judged the render.

## Ship log

| Date | Event |
|---|---|
| 2026-10-27 | Filed under an earlier id that another seat's tracker already held; refiled onto FM-072. |
| 2026-10-27 | First render, on a local branch that was never pushed — three Owner-approved changes to the software-factory loop. |
| 2026-10-27 | STAND-UP: split *you answer, one at a time* onto two centred lines so it fits inside the panel. |
| 2026-10-27 | Headline set to *the agents never answer for you.* — the Owner's choice of the stricter line, relayed via go-to-market. |
| 2026-10-27 | Evidence moved with the tracker; PNG and SVG kept byte-identical. |
| 2026-11-04 | Re-filed from FM-072 to FM-152 on main `35158e3`: main's FM-072 is the Planner's (`2f9895d`). The Owner's call, relayed via the Auditor; evidence byte-identical to the earlier, unpushed version. |
| 2026-11-04 | Pre-review fixes: Why names FM-147; private ids, unpushed branches, host paths, an outside project id, the Owner's address, and a past deadline removed; `build-sf.py` reads its sources relative to the repository. Render byte-identical. |
