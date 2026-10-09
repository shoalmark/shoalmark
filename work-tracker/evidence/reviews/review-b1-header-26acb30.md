# FM-006: B1's header, the review at 26acb30

Verdict: **READY WITH FINDINGS**. One P3, RV-2913, is fixed forward; no P1 or P2 stands. RV-2911 is closed, and RV-2912 is stated in 26acb30's message. RV-2914 to RV-2919 are unused.
Reviewed: 26acb303856554fe93b23d53e0ec47afbce62b55, `git diff 989f3c6 26acb30`. The scope is three commits by implementer-126: 5050bb2 (the header and its checks), c44e679 (FM-006's records and RV-2910's fix) and 26acb30 (RV-2911's fix). Tier: code, since the diff names test_shoalmark.py and scripts/check_landing_browser.mjs.

## What holds
- **The template.** 5050bb2's template is the approved round-6 patch on 989f3c6, byte for byte, and it holds the Owner's word on the header:
  - a separator between start and Docs that goes with the anchors;
  - Docs (Doku) as the sand button with its arrow out of a box;
  - the switch as the same button in outline, with a globe before the other language's name;
  - both icons as one path in the button's ink, `aria-hidden` and not focusable;
  - below 526 px, only the word beside the mark yields.
- **Accessibility.** The tree is identical to 989f3c6's at 1440, 1000, 525, 390 and 360 px, in English and German: the names, Docs and Doku, the switch's `hreflang`, `lang`, `aria-label`, `title` and `href`, and the mark's `aria-label` below 526 px.
- **The bar.** With 888/888, at every whole width from 360 to 1920 px, in both languages and both states, nothing overlaps, wraps, is cut or scrolls sideways. The anchors and the separator first show at 1208 and 1273 px, and both buttons' focus rings stand whole inside the window and the bar at 360, 390 and 1440 px.
- **The checks.** The source check has 14 controls and the browser check 3 more, and `wraps` now aims at the new rule; each fails at 989f3c6. RV-2910 is fixed exactly as given.

## Findings
- **RV-2911 · P2:** closed in 26acb30. Its 40 lines are 989f3c6's twenty entries word for word, between "wraps" and "bar-docs"; nothing else changes. The block holds 32 controls.
- **RV-2912 · P3:** 5050bb2's message. The anchors moved 78 px in English and 77 in German, and 888/888 is the widest three-digit hi-score. 26acb30's message records both, and the history stays as it is.
- **RV-2913 · P3 · `test_shoalmark.py:12709`.** The browser block's "not blind" check asserts that each control it holds fails, but never counts them. It passed on 12 while naming 32, which is how RV-2911 got through.
  - Fix: in `f"(saw {_found})", all(code == 1 and`, insert `len(_controls) == 32 and ` before `all(`, as the source checks pin `len(...) == N`.

## Commands: 2026-10-09, CEST, as `date` printed each
- **At c44e679:**
  - py_compile (3.14 and 3.9), test_core, `--check`, `--session-check` and test_check_site.py (20 tests): each exit 0 (18:13:43–18:14:17);
  - both states built in a scratch clone, with check_site.py and `--check site` exit 0 (18:14:38–18:14:57);
  - check_landing_browser.mjs: interim 90 checks and probe 302, none failing (18:19:47–18:23:08);
  - run-one-check on the header check and its controls: exit 0 at the head, and exit 1 against 989f3c6 (18:15:19–18:19:00);
  - the new browser checks on 989f3c6's page: exit 1 (18:23:30–18:24:09).
- **At 26acb30:**
  - `--check`, `--session-check` and py_compile: exit 0 (18:44:08–18:44:18).
  - The browser block under SHOALMARK_REGENERATE=1 (18:44:07–19:00:53): exit 0. All 32 controls exit 1 on the check they name.

Quality read: apart from RV-2913, the round reads clean.
