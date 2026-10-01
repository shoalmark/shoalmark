# FM-006 — the Reviewer's scoped check of the fix rounds since part 2, at affd09f

Verdict: **READY**. Every item since 70ffd5f is closed, RV-2185 … RV-2189 with them, and this check finds nothing new.
Reviewed: affd09f45e2b4dd895e0b68708c552af1b756931 — `70ffd5f..affd09f`, a scoped check by the Owner's word.
Reviewer: b3bdb000/reviewer-76 (claude-opus-5-5, max), `reviewer@seat` unsigned, worktree shoalmark-review-10, 09:33–09:37 CEST on 2026-10-01. Independence: the same session as the build, so not independent.
Tier: code (`overrides/`, `scripts/`). Not re-read: what parts 1 and 2 closed. No full local run: the bundle's tip gets one.

## Items, one line each
- **ac63619, after the Owner's judgment filed in c4f3d47.**
  - The chart's top edge shows 125 px at 390 × 844 and 122 px at 360 × 780, with the H1, the full lede and the action above the fold. At 375 × 667 the content fills the screen and the edge shows 7 px; the action still ends above the fold (632 of 667), which the ruling puts first.
  - The agents' card reads *For agents*, so *The fleet* now heads the new section alone.
  - The icon is `./assets/favicon.svg`, a file of the site, and the `/favicon.ico` 404 is gone. Closed.
- **6f13d7a, the re-render.** `preview.png` selects no wreck (`wrecksSelected` 0; FM-037 is drawn as the others are). The script, rerun on this tip's build, makes the preview and every first screen byte for byte. Closed.
- **69e8c6a, RV-2185.** Lines 3–6 of `overrides/partials/language.html` are my text verbatim, under a comment the build drops. The six pages under `de/` say `lang="de"`; the rest say `en`. Closed.
- **275ce44, RV-2186.** README §*Seats*'s clause stands after *builder none.*, as written. Closed.
- **82b5d17, RV-2187.** The 980 px rule carries its mark, as written. Closed.
- **c3fa119, RV-2188**, read by content, because 6f13d7a had moved the lines. The header and the README sentence are my text; the decoder, `COLLECT` and `contrast()` are gone; the summary line is in. Closed.
- **affd09f, RV-2189, by the Owner's ruling filed in 27d5160.**
  - My rule stands, marked, before the reduced-motion block.
  - `scrollWidth` equals the window's width at 360, 375, 390 and 1440 px.
  - `phone-360-first.png` is 360 × 780, byte for byte on a rerun. Closed.
- **The site's checks at affd09f**, 09:34:17–09:34:20: `test_check_site.py` 5 ok, the build reports no issues, `llms_txt.py site` 14 pages, `check_site.py site` exit 0.

Four numbers for this verdict: records +25, product 0.
Next: nothing goes back. The bundle's tip gets the full local run and CI. Two carries from part 2 stand: the rights line becomes README §*Seats*'s words with FM-024's switch, or takes the fallback text as c4f3d47 rules; and `preview.png` keeps the wrecks read at bef2a1e unless the cut re-renders it. RV-2184 (`--key`'s help) stays the Planner's to place.
