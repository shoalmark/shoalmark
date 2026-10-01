# What a stranger meets first — the landing's render for v0.19.0 (FM-006)

**Rendered** from release builds (Zensical 0.0.66, tinycss2 1.4.0, the docs workflow's steps): `start-1440.png` from this
README's commit (its text capped at about 80 characters), `start-390.png` from `b2683f2` (In this beta); `phone-360-first.png`
and `phone-390-first.png` from `affd09f` (RV-2189); the rest and `docs/assets/preview.png` from `ac63619`. At this commit the
first screens and the preview are the same byte for byte; the full pages predate RV-2186's line, RV-2189's HUD and the beta box.
Round one: `36cde21`. **Made with** `node render.mjs SITE OUT [PREVIEW]` (this folder): Chrome 154.0.8037.58 headless, Node
26.7.0, 127.0.0.1 only, dark, scale 1, 3 s after load, motion allowed; 2026-10-01, 09:07–10:15 CEST.

| File | Width × height | What it shows |
|---|---|---|
| `phone-390-first.png` | 390 × 844 | the first screen: the HUD; the wordmark and its claim; the H1 in Silkscreen 700, 24 px, four lines (266–382 px); the job line, full form (396–575); the one action, the row's width, its bottom edge at 650 px; the chart's top edge at 719 px, 125 px above the fold |
| `phone-360-first.png` | 360 × 780 | the first screen at 360: no sideways scroll (scrollWidth 360); the H1, the full job line and the action above the fold, its bottom edge at 630 px; the chart's top edge at 658 px |
| `phone-390-full.png` | 390 × 12577 | the page: the chart, its console, then *The fleet* (2074–3422 px), then *Two players, one record* |
| `desktop-1440-first.png` | 1440 × 900 | the chart in the first screen (56–876 px), the title over the sea: the H1 in two lines, broken at its semicolon; the job line; the action (449–486 px) |
| `desktop-1440-full.png` | 1440 × 6393 | the page, *The fleet* at 1332–1927 px; the agents' card headed *For agents* |
| `docs/assets/preview.png` | 1200 × 630 | the link preview: the chart's north-west at the page's scale, 4 CSS px to a chart pixel, rendered at 1280 px under reduced motion; the title's texts hidden, the wordmark alone, no HUD; the wreck labels kept and no wreck selected |
| `start-390.png`, `start-1440.png` | 390 × 2308, 1440 × 962 | the start section alone, its heading through its last line: *In this beta:* and its three lines where the FM-026 line stood, then the stages, the costs and the coins; at 1440 the box fitted to its text, about 80 characters a line |

**Placements.** The fleet is the first section after the chart and its console; *The fleet* heads it alone. The three anchors
left the page; the HUD's nav keeps their destinations at 981 px and wider. First-screen links: at 390 the HUD's *shoalmark* and
*Docs*, the action and six wrecks on the chart's edge; at 1440 the HUD's, the wrecks' and the action.

**Checks.** `check_site.py` exit 0 on each build, link preview images included; `test_check_site.py` and `llms_txt.py` exit 0.
No script error and no console entry; no sideways scroll: scrollWidth equals the window at 360, 375, 390 and 1440 px (RV-2189).
Contrast by slice L's `checks.mjs`, run unchanged on the same build (`node ../landing/start-page/checks.mjs SITE OUT.json`),
reduced motion: the lowest new text 5.69 (the footer's fine print, `#8ea3b6` on `#15293d`); the H1 14.7, the job line 9.6, the
action 10.6, the fleet 9.1 and up; nothing on the page below 4.5. Nothing overflows: the tiles at 390 (text 12 px and up), the
beta box at 360, 390 and 1440. Each inlined badge's drawing equals its `brand/seats/` source. **Not verified:** Firefox, Safari
(and `svh` under a phone's toolbars), a screen reader, print, a real phone, a link preview as a service draws it.
