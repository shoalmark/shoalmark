# What a stranger meets first — the landing's render for v0.19.0 (FM-006)

**Rendered:** `cf71a41`, the landing's tip (`e14ab65` the page, `cf71a41` its preview image), built as the release builds it —
a venv, Zensical 0.0.66, tinycss2 1.4.0, `zensical build --clean`, `scripts/llms_txt.py site`, `scripts/check_site.py site`;
`663ed5d` (`cf71a41` with the shared branch's `6f24273` merged) builds the same `site/index.html`, byte for byte. **Made with**
`node render.mjs SITE OUT [PREVIEW]` (this folder): Chrome 154.0.8037.58 headless, Node 26.7.0, served from 127.0.0.1, every
other host unresolvable (none asked), a dark preference, device scale 1, 3 s after load, motion allowed; 2026-10-01, 08:44 CEST.

| File | Width × height | What it shows |
|---|---|---|
| `phone-390-first.png` | 390 × 844 | the first screen: the HUD; the wordmark and its claim; the H1 in Silkscreen 700, 24 px, four lines; the job line, full form; the one action, the row's width — its bottom edge at 684 px. The chart begins at 844, the fold |
| `phone-390-full.png` | 390 × 12702 | the page: the chart, its console, then *The fleet* (2199–3547 px), then *Two players, one record* |
| `desktop-1440-first.png` | 1440 × 900 | the chart in the first screen (56–876 px), the title over the sea: the H1 in two lines, broken at its semicolon; the job line; the action (449–486 px) |
| `desktop-1440-full.png` | 1440 × 6393 | the page, *The fleet* at 1332–1927 px |
| `docs/assets/preview.png` | 1200 × 630 | the link preview: the chart's north-west at the page's scale, 4 CSS px to a chart pixel, rendered at 1280 px under reduced motion, the title's texts hidden — the wordmark alone, no HUD |

**Placements.** The fleet is the first section after the chart and its console. The three anchors (*1P for agents*, *2P
for people*, *press start*) left the page; the HUD's nav keeps their destinations at 981 px and wider. The first screen's
links and buttons: at 390 the HUD's *shoalmark* and *Docs* and the action; at 1440 the HUD's, the wrecks' and the action.
Two headings read *The fleet*: the section's h2 and the agents' card's h3 (in both full renders).

**Checks.** `check_site.py` exit 0 on `663ed5d`'s build; on `cf71a41`'s it fails on the link to `ADOPT.md`, which the merge
brings. `llms_txt.py` exit 0. No script error at either width; the console's one entry is the browser's own request for
`/favicon.ico`, 404: the landing links no icon, before this change as after it. No sideways scroll. Contrast by slice L's
flat method (`../landing/start-page/checks.mjs`), reduced motion: 48 new text runs at each width, the lowest 5.69 (the
footer's fine print, `#8ea3b6` on `#15293d`); the H1 14.7, the job line 9.6, the action 10.6, the fleet 9.1 and up; nothing
on the page below 4.5. The tiles at 390: 350 px wide, 178–208 px tall, no text under 12 px, nothing overflowing. Each
inlined badge's drawing equals its `brand/seats/` source, rect and paths verbatim. **Not verified:** Firefox, Safari (and
`svh` under a phone's toolbars), a screen reader, print, a real phone, a link preview as a service draws it.
