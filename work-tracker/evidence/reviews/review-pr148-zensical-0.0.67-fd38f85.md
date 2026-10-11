# FM-006: PR 148, Dependabot's zensical 0.0.66 → 0.0.67, the site built both ways at fd38f85

Verdict: **READY WITH FINDINGS**: two P3s, both stale second copies, fixed forward off main; neither blocks the merge. Ids RV-2810 and RV-2811; RV-2812 to RV-2829 are unused.
Reviewed: fd38f8505fba82470581e516e27f94335fb60125, on base 85a53ca. Scope: `requirements-docs.txt` only, one line (`zensical==0.0.66` → `0.0.67`). Tier: code (configuration), read from `git diff --name-only origin/main...origin/dependabot/pip/zensical-0.0.67`.

## What the comparison shows

- docs.yml's four steps pass on both sides, Python 3.12.12, the other 12 packages resolved alike: `test_check_site.py` OK (5 tests); `zensical build --clean` "No issues found"; `llms_txt.py site` 14 pages, each with a twin; `check_site.py site` passed.
- The trees: 76 files each, the same set but for hashed names; `diff -r` lists 24. `index.html` is byte-identical (sha256 356d9546…), as is every file not listed, `llms.txt` and the Markdown twins among them. 14 pages differ, `setup.html`, `de/setup.html` and `agents/index.html` among them, each only in: the generator meta (`zensical-0.0.66` → `0.0.67`); three hashed names (`main.1502b751` → `main.4ae390e2`, `palette.812a03bb` → `palette.96d1a7e4`, `bundle.b7d3f789` → `bundle.67a597eb`); `role="status" aria-atomic="true"` on the dialog; a `clipboard.error` key in the page's translations; one blank line (not in `404.html`). All 14 normalise to equal. Five assets are renamed by hash: the modern and classic `main` and `palette` CSS (no page references classic) and the JS bundle.
- Upstream: zensical 0.0.67 (30 Sep) takes UI 0.0.34, whose change is the `content.action.copy` button, "Copy as Markdown": its CSS and JS, the `clipboard.error` string, and the blank line its new block in `partials/actions.html` leaves. With it come Preact 11 and re-minified CSS and JS of the same declarations (`z-index 0s` → `z-index`, `#ffd500` → `hsl(50,100%,50%)`). It adds native `social`, `llmstxt`, `exclude` and `github-admonitions` plugins. This site enables none of them; `scripts/llms_txt.py` writes `llms.txt` as before. On the German pages `clipboard.error` is English (UI 0.0.34 has no German string); only that button shows it, and this site does not enable it.
- Renders, headless Chrome 154: `index.html`, `setup.html`, `de/setup.html` at 1440×900 and 390×844, viewport and full page, light and dark: 24 pairs, each pixel-identical. The first light run differed in one pair, the landing's full page at 390 (rows 719–1017, the chart); today's side differed from its own rerun there too, and the rerun pair is identical.
- Search: "triage" 33 results on `setup.html`, "Antwort" 29 on `de/setup.html`, the same first three links on both sides.
- Console: no script error or exception on either side. One failed request, alike on both: `api.github.com/repos/shoalmark/shoalmark/releases/latest`, 404, as the repository has no published release; not from PR 148.
- Licence: zensical is MIT on both sides; `LICENSE.md` is byte-identical (sha256 ac044e6d…). The wheel's SBOM adds 69 Rust components (social cards: resvg, image; HTTP: ureq, rustls), all permissive: MIT, Apache-2.0, BSD, ISC, Zlib, CDLA-Permissive-2.0. Run with outbound network denied, 0.0.67 builds the same site byte for byte.

## Findings

- **RV-2810 · P3:** `overrides/main.html` line 3 still names "the pinned Zensical 0.0.66". The pin is 0.0.67, whose `base.html` also leaves `extrahead` empty, so the claim holds but names a stale version. Fix: replace `the pinned Zensical 0.0.66 leaves empty for it` with `the pinned Zensical (requirements-docs.txt) leaves empty for it`.
- **RV-2811 · P3:** `requirements-docs.txt` line 1, `# Verified with the organization migration site build.`, now stands above a pin that build never ran. Fix: replace it with `# Verified by building the site both ways with docs.yml's steps: work-tracker/evidence/reviews/review-pr148-zensical-0.0.67-fd38f85.md.`

## Commands: 2026-10-08, CEST, as `date` printed each

- `git fetch`: head fd38f85 on 85a53ca, one file (10:39:46). A Python 3.12.12 venv per side from its `requirements-docs.txt` (10:40:10–10:40:38).
- docs.yml's four steps, each exit 0: at 85a53ca 10:40:45–10:40:52; at fd38f85 10:40:52–10:40:59. `diff -r` of the two `site/` trees: 24 lines.
- Chrome renders and console 10:45:38–10:46:36, the rerun ending 10:49:16, dark ending 10:50:05; search 10:47:21–10:47:33; the offline 0.0.67 build at 10:50:19, `diff -r` against the online one empty.
- `--check` and `--session-check` before this commit, each exit 0 (10:53:45–10:53:54); after it, in the Reviewer's report.

Quality read: Dependabot's commit message names the bump and links its notes; the change reads clean but for RV-2810 and RV-2811.
