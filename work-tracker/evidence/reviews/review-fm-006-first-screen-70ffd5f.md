# FM-006 — the Reviewer's pass on `fm/006-what-a-stranger-meets-first` at 70ffd5f, part 2: the Designer's landing and render, and the fix round on part 1

Verdict: **READY WITH FINDINGS**. The fix round closes RV-2180 … RV-2183, each fix the text my verdict on 6f24273 gave. This pass finds three P3 on the slice (RV-2186 … RV-2188) and one P3 found on the way, older than the slice (RV-2189). The landing's ruled texts stand word for word, the link preview is as ruled, and the site's four checks exit 0.
Reviewed: 70ffd5f1c1ae26a57575168087248885d74360aa — `e9faf05..70ffd5f`, seven commits and three merges.
Reviewer: b3bdb000/reviewer-76 (claude-opus-5-5, max), `reviewer@seat` unsigned, worktree shoalmark-review-10, 08:54–09:15 CEST on 2026-10-01. Independence: the same session as the build (b3bdb000/designer-72, implementer-70 and implementer-71), so not independent.
Tier: code. `git diff --name-only origin/main...HEAD` lists `zensical.toml`, `overrides/main.html`, `overrides/landing.html` and `scripts/` beside the pages, the notes and the trackers.
Read: FM-006's section *What a stranger meets first — v0.19.0* (A as amended 2026-10-01, B, C, D, E) and its player-stats ruling for the *before it* row, my verdict on 6f24273, and `git diff e9faf05 70ffd5f` whole. That is implementer-70's 0e8d419, 44bc9b9 and a2a586e and implementer-71's 226996c (the fix round), designer-72's e14ab65, cf71a41 and 36cde21, and the merges 663ed5d, 09fc0a0 and 70ffd5f. The Owner judges the render's look in parallel, so this pass judges truth, language and code.

## The fix round on part 1 — RV-2180 … RV-2183 closed
A script compared each fix with my verdict's fix text, byte for byte; each matches.
- **RV-2180** (0e8d419): FM-031:146 marks rule 3's change since the signature. AGENTS.md is unchanged, and its *in the words FM-031's body records them* holds.
- **RV-2181** (44bc9b9): the CHANGELOG bullet is as given. With the landing in place, every clause is true at this tree.
- **RV-2182** (a2a586e): `PreviewImage` and the `LinkPreview` test are as given, and the closing line is updated. The tests pass (5 ok), `check_site.py` passes with `preview.png` in the site, and with the image removed from a build it exits 1, *link preview image not in the site, in index.html*.
- **RV-2183** (226996c): ADOPT.md:39–44 is as given. In a git working copy named `firmware-controller`, `--init` gives `FIRMW-001` and writes the board's two `.gitignore` lines.
- The three merges carry nothing of their own: `git show --remerge-diff` is empty, and no file differs from both parents.

## Findings
- **RV-2186 · P3 · The fleet section does not make plain that the gate enforces the rights.**
  - C's acceptance says the section *makes plain that the gate enforces the rights, that the tool knows three seats, and that everything else is practice the adopter writes — in the README's own words (§Seats) where a clause is needed*.
  - The section carries the second, D1's phrase, and the third, the charter line, which is README §*Seats*:340–341 verbatim. No line carries the first: *gate* appears only in the charter's *never by the gate*. README §*Seats* has the clause: *Four rights, each a front-matter transition the gate sees in a diff … anything else is open to every seat.*
  - **Fix:** at overrides/landing.html:392, between `<span><b>builder</b> none</span>.` and `</p>`, add ` <b>Four rights</b>, each a front-matter transition the gate sees in a diff; anything else is open to every seat.` These are README §*Seats*'s own words.
  - Tried on a scratch copy: the build and the four site checks pass, the sentence renders, and the first screen and the tiles are unchanged.
- **RV-2187 · P3 · One edit carries no mark.** The page's new head comment (:6–7) says each edit *is marked where it stands*. The 980 px rule at :285, `.stages,.seats{grid-template-columns:1fr 1fr}` (the tiles two to a row), has no mark. Every other hunk has one.
  - **Fix:** :285 ends `{# FM-006 v0.19.0 first screen: C, the fleet's tiles two to a row at 980px and less #}`. Tried: the build drops the comment.
- **RV-2188 · P3 · The render's `render.mjs` repeats slice L's `checks.mjs` for the contrast: 61 of its 162 lines.**
  - Falsifier: slice L's `checks.mjs` (`../landing/start-page/`), run unchanged on this tip's build, gives every number the render README states. It finds the H1 at 14.7–14.8, the job line at 9.6–9.7, the action at 10.57, the fleet at 9.08 and up, the footer's fine print at 5.69 (`#8ea3b6` on `#15293d`), and nothing below 4.5.
  - Slice L's `render.mjs`, run unchanged with `page/` set to this build, renders both first screens byte for byte as committed, and the full pages at the committed sizes.
  - New code is needed only for the preview clip and for the first-screen and tile measurements. Slice L's scripts could not take those on, because evidence is append-only. So the new script is needed, but not its contrast half.
  - **Fix:** in `render.mjs`, delete :19 (`import {inflateSync} from "node:zlib";`), :34–60 (the PNG decoder and the colour helpers) and :107–136 (`COLLECT` and `contrast()`). Replace :145–147 with `  summary.widths[w] = {...parts, tiles};`. Lines :10–13 then read:

    ```
    // It prints a JSON summary: each first-screen part's box at both widths (document px; the fold is the window's height), the
    // links in each first screen, script errors and the hosts asked, the page's sideways scroll and the fleet's tiles at 390. The
    // contrast of every text run is slice L's checks.mjs's (../landing/start-page/), run unchanged on the same SITE.
    ```

    In the render README, :24–27, from *Contrast by slice L's* to *nothing on the page below 4.5.*, reads: ``Contrast by slice L's `checks.mjs`, run unchanged on the same build (`node ../landing/start-page/checks.mjs SITE OUT.json`), reduced motion: the lowest new text 5.69 (the footer's fine print, `#8ea3b6` on `#15293d`); the H1 14.7, the job line 9.6, the action 10.6, the fleet 9.1 and up; nothing on the page below 4.5.``
  - Tried on a scratch copy: the cut script, 101 lines, makes `preview.png` byte for byte as committed, the two first screens byte for byte, and the same first-screen boxes, tiles and errors.

**Found on the way, older than this slice — the Designer's to take, now or after the tag:**
- **RV-2189 · P3 · At 360 and 375 px the landing is 390 px wide,** so a phone of either width, first screen included, can scroll sideways by 30 or 15 px.
  - The HUD's *Docs* link ends at 390 px. The part-1 landing measures the same (`scrollWidth` 390 at 360 and 375). On both trees, the action stays above the fold at 360 × 740 and 375 × 667.
  - Tried on a scratch copy: `@media (max-width:400px){.hud .wrap{gap:12px;padding-inline:14px}}`, placed before the reduced-motion block, removes the sideways scroll at 360, 375, 390 and 414 and leaves the first screen otherwise as it was. It is a visible change to the HUD.

## What holds
1. **The landing's ruled texts, word for word.**
   - The H1; the `<title>` *shoalmark — the agents keep the work; the person keeps the word*; the one description in the meta and in `og:description`; the job line in full form, with `<em>done</em>` as the agents' card sets it.
   - *Hand your agents the note* links `ADOPT.md`, and the coin reads *note for trying it* (`ADOPT.md`) with *(Deutsch)* (`ADOPT.de.md`).
   - C's definition, and the four tiles' lines as ruled. The characters (*the skipper*, *the shipwright*, *the inspector*) come from `brand/seats/README.md`. *Specialists* carries *(customizable)* in the character's place.
   - *All seats* → `https://shoalmark.github.io/shoalmark/seats/`.
   - E: *before the Owner's signed answer* (:465), and the footer's *the Owner … their merge … their done: and due: … theirs* (:517). The only *he* or *his* left are `:3` and `WRECKS` (:524), and both are as they were at 32780e5.
   - The section subtitle that said the H1 is gone. The agents' card (*a gate that refuses a <em>done</em> without a commit behind it*) is unchanged.
2. **Every line true at this tree.**
   - The fleet's rights line is D1's phrase, and it matches `BUILTIN_RIGHTS`. The charter line is README §*Seats*:340–341 verbatim. *Name your own in `[seats]`, with the rights `[rights]` gives them* is how the tool reads `[seats]` and `[rights]`.
   - The rights line is not yet README §*Seats*'s own words: the README reads *Four names carry theirs built in — owner all four …* until FM-024's switch writes D1's phrase there. It holds once the switch merges (a carry, below).
3. **The link preview.**
   - The landing's head carries each ruled tag once: the canonical, `og:type` website, `og:site_name`, `og:locale` en_GB, `og:url`, `og:title` (the H1), `og:description`, `og:image` with its width, height and the ruled alt, and `twitter:card` summary_large_image. So do the 14 theme pages, as in part 1.
   - `docs/assets/preview.png` is a 1200 × 630 RGB PNG: the chart's north-west with the wordmark. It has no headline and none of the HUD's or the scores' numbers. The large numbers on it are the chart's depth soundings (`SOUND`), not counts.
   - The wrecks' tracker labels are not counts either: the ruled alt text names the wrecks (*defects from shoalmark's own tracker lying on the flats as wrecks*), and a label is how the page draws a wreck. So *no counts* holds.
   - The Designer's script, rerun on this build, makes `preview.png` byte for byte.
4. **The Designer's changes beyond the ruled texts.**
   - The desktop H1 is capped at 24 px and balanced: two lines broken at the semicolon at 1440 px.
   - At 700 px and narrower the title fills the first screen. At 390 × 844 the H1 (Silkscreen 700, 24 px, loaded) sits at 301–416, the job line at 430–609 and the action at 639–684, and the chart starts at 844, the fold. At 375 × 667, 360 × 740 and 414 × 896 the action stays above the fold.
   - The id `seats` is sound: `fleet` is the boats' canvas (:339, read at :662), and nothing links to `#seats`.
   - The three anchors left with their CSS, and the `blink` keyframes still serve the wrecks. At 981 px and wider, the HUD's nav keeps the destinations. On a phone, the HUD shows *shoalmark* and *Docs*, and the sections are reached by scrolling. That follows from the ruled one action, and it breaks no link: no finding.
   - Two headings read *The fleet*: the Owner's to judge.
5. **The page's quality.** Slice L's `checks.mjs`, run unchanged on this build:
   - no text run below 4.5 at 1440, 1024 or 390 px (the lowest is 5.14, the register's FM-035 link, as before);
   - no script error and no host but the page's own;
   - all 24 wrecks focusable, and no chart figure read;
   - reduced motion still, with two captures identical;
   - the same pixels under a light and a dark preference.

   The two chart figures under the title at 1440 px measure 4.0 and 1.3, as they did at 6f24273 (3.99 and 1.3): slice L's known pair, covered by design. The seven inlined badges' drawings equal `brand/seats/*.svg`, rect and paths verbatim, in the ruled order. Each edit carries its Jinja mark but one (RV-2187).
6. **The evidence.** The render README's claims hold on a rerun:
   - cf71a41's build and this tip's give the same `index.html`, byte for byte;
   - the first-screen boxes and the tiles match;
   - the one console entry is `/favicon.ico` 404, as before;
   - the README states what is not verified.

   The script's contrast half is RV-2188.
7. **The site's checks at this tip**, on a clean clone in the docs workflow's order: `test_check_site.py` 5 ok; `zensical build --clean` no issues; `llms_txt.py site` 14 pages; `check_site.py site` exit 0.
8. **The records rule**: the seven commit messages cite the Owner's ruling filed in FM-006 or my verdict's finding, and none quotes a conversation.

## Controls, one line each
- Setup, 08:54:16: `git status --short` empty; one fetch; detached at 70ffd5f, equal to `ls-remote`. `--whoami`: `To: b3bdb000/reviewer-76 reviewer (shoalmark-review-10) · claude-opus-5-5 · max`.
- Site, 08:58:52–08:58:55: the four workflow steps, each exit 0.
- Slice L's `checks.mjs` on this tip's build, 08:59:02–08:59:58, exit 0; on 6f24273's build, 09:00:27–09:01:21, exit 0, for the chart comparison.
- Slice L's `render.mjs` on this tip's build, 09:01:33–09:02:04: no errors, no outside host.
- The Designer's `render.mjs` on this tip's build, 09:04:01–09:04:22: the preview and the first screens byte for byte; the full pages differ by motion.
- The cut `render.mjs` and the measurements at 360, 375, 390 and 414 px; the RV-2186, RV-2187 and RV-2189 fixes: scratch copies only, none in this commit.

Quality read: the Designer's work is careful and well documented.
- Each edit is marked and explained; the badges are verbatim; the first screen is measured at the fold, not just drawn.
- The render README is honest about what was not verified, and the preview reproduces byte for byte.
- The fix round took each fix exactly as written and proved it.
- The weak spots are small: the rights section names the gate only to say what the gate does not read; the render script copies a measurement that slice L's tools already make; one edit is unmarked.

Four numbers for this verdict: records +105, product 0.
Next:
- RV-2186 and RV-2187 go back to designer-72, and RV-2188 to designer-72 for its own evidence. I verify the fix round. RV-2189 is the Designer's, and the Owner's, to take now or after the tag.
- Carries:
  - The fleet's rights line and the seats page's D1 sentence become README §*Seats*'s own words only when FM-024's switch merges. If D2 misses the tag, D1's fallback line covers the seats page, and the landing's rights line needs the same.
  - At the cut, the player stats update `WRECKS`, but `preview.png` is not on the cut's list and keeps the wrecks read from bef2a1e. A re-render is one command (`render.mjs`, byte-reproducible); the Owner says which.
  - The two headings *The fleet* are the Owner's to judge.
