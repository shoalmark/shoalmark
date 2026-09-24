# Review — release 0.18.2 at 06d884e (2026-09-24 16:20 CEST, Reviewer, session `8e509911/reviewer-1`)

**Scope.** Branch `fm/006-0-18-2-the-board-wears-the-mark`, tip `06d884e`
(`06d884e56fbb4835684898087995853511453ee4`), on `v0.18.0` `095f1d3`. It is release **0.18.2**: `VERSION` says
0.18.2, and the CHANGELOG's §0.18.2 is the contract checked below, with FM-006's rulings (the mark at 16 px; the mark
takes the name's ink on dark; the German claim).
- `6fe9b11`, the tool: `inline_svg()`, the fourth brand file `wordmark.svg`, tests, README §9, `--help`, the starter,
  CHANGELOG, VERSION.
- `06d884e`, this repository's `work-tracker/brand/`, the generator `evidence/FM-006/mark/pricke/wordmark.py`, FM-006's
  line and ship-log row.
- Both by the Implementer under `8e509911/implementer-17`, worktree `shoalmark-impl-4`.
- **Tier: code.** `shoalmark.py` and `test_shoalmark.py` change. The full loop applies.
- **Independence:** the same session. The Reviewer is `8e509911/reviewer-1` and both commits are under the root
  `8e509911`. This is reported, not refused.
- 0.18.1 is not in this branch yet. VERSION and CHANGELOG will conflict when main is merged in; not reviewed here.

## What I ran, and what came back

**Gates and suites at `06d884e`.**
- `--check` exits 0. It prints `filing freeze: 16 open, at or above 8 — only bug filings`.
- `--session-check` exits 0.
- `python3 shoalmark.py` exits 0, prints no brand warning, and `git status --porcelain` stays empty. The board is
  git-ignored; a second run writes nothing.
- `test_shoalmark.py`: 298 ok on Python 3.14.3 (2:42) and on `/usr/bin/python3` 3.9.6. `test_core.py`: 148 ok on
  both. All green, as claimed. The runs were one after another, never in parallel.
- **The Chrome check ran, not skipped,** on both Pythons: *saw: light=rgb(1, 2, 3)/16px | dark=rgb(253, 252,
  251)/16px | auto=rgb(253, 252, 251)/16px*.
- `--brand` names `repository` for `theme.css`, `logo`, `wordmark` and `labels.yaml`; *labels changed: 2 of 124*.

**The header, with this repository's brand.** Built in a scratch clone at the tip, with `XDG_CONFIG_HOME` pointed at
an empty directory. `~/.config/shoalmark/` does not exist here and was not touched.
- The header is `<div id="H"><b class="wm" role="img" aria-label="shoalmark"><svg viewBox="0 0 130 16" width="130"
  height="16" fill="currentColor">…`. No `<img>` is in it and no `<b>shoalmark</b>` is on the page.
- `<title>shoalmark — work tracker</title>`. The favicon is `logo.svg` as a data URI. `tagline` and `footer` are in
  the labels.
- **In Chrome** (headless, a probe clicking `◐` three times):
  - the `<svg>` is 130 × 16;
  - light: fill `rgb(33, 33, 33)`, which is the theme's `--ink` `#212121`;
  - dark and auto: fill `rgb(255, 255, 255)`. The theme's `--ink` there is `#bbbdc2`, but its dark rule paints
    `#H b` white, and the wordmark sits in that `<b>`. This is FM-006's ruling: the mark takes the name's ink.
  - `◐` switches the theme's dark rule, `#H b{color:#fff}` included.
- **Without `wordmark.svg`** (moved away in the scratch clone), the header is byte-identical to the header that
  `v0.18.0`'s `shoalmark.py` builds from the same repository. The whole page differs in the CSS lines only: two lines
  out, three in.
- **Sizes.** With no `height`, the wordmark is 179 × 22: the logo's 22 px, as claimed. `height="2em"` gives 260 × 32.
  `width="50em" height="100%"` gives 800 × 98, and the header grows to 98 px. `viewBox="NaN -1e308 1e309 -5"` is
  ignored by the browser (300 × 16). None of these is a security issue. The docs ask for pixels, and the tool does
  not check.

**The brand.**
- `theme.css`, compared with Zensical's `modern` stylesheets (from the `zensical` package, `--md-hue: 225deg`),
  flattened onto their ground:

  | | ground | ink | dim, mute | line |
  |---|---|---|---|---|
  | default, light | `#fff` → `#ffffff` ✓ | `#000000de` → `#212121` ✓ | `#0000008c` → `#737373` ✓ | `#0000001f` → `rgba(0,0,0,.12)` ✓ |
  | slate, dark | hsl(225 15% 5%) → `#0b0c0f` ✓ | 90 % at .82 → `#bbbdc2` ✓ | at .56 → `#838589` ✓ | 95 % at .12 → `rgba(240,241,244,.12)` ✓ |

  `docs/stylesheets/shoalmark.css` sets no palette. Its one colour rule, slate's white for the logo, is the theme's
  `#H b{color:#fff}`.
- **Contrast** (`fm.contrast`). Ink on ground: 16.1 and 10.4. Secondary: 4.74 and 5.29. The tool prints no theme
  warning.
- **The four status colours keep the tool's shades.** Light on `#ffffff`: teal 4.97, coral 5.69, blue 5.47, yellow
  4.76. Dark on `#0b0c0f`: 10.2, 7.7, 7.3, 12.6. The claim of *4.7:1 or more* holds.
- **Fonts.** There are four `woff2` files, of 17 268, 22 924, 20 984 and 22 260 bytes. Each is byte-equal to IBM's
  `@ibm/plex-sans@1.1.0` or `@ibm/plex-mono@1.1.0` `fonts/split/woff2/…-Latin1.woff2`, fetched from jsdelivr. The
  `LICENSE.txt` beside them is byte-equal to both packages' OFL licence.
- **The `@font-face` rules** are written relative to `theme.css` (`fonts/…`), as §9 requires. The page re-bases them
  to `brand/fonts/…`, and all four files exist.
- **Nothing is fetched.** `theme.css` holds no `http`. The page's URL strings are marked's comments, the signing
  page's link text, and marked's `"http://"` autolink prefix. It has no `<link>` except the data-URI favicon, and its
  `url()`s are the four fonts and marked's `url(e)`. Opened in Chrome, the clean board made no request to a logging
  server.
- **`logo.svg`** is byte-equal to `docs/assets/favicon.svg`.
- **`wordmark.svg`:**
  - 130 × 16, 4 089 bytes (under 4 KiB);
  - one `currentColor`, no other fill or stroke;
  - no `<text>`: two paths. The first `d` equals `pricke.svg`'s;
  - the name is IBM Plex Mono **Medium** (500), the site's ruled weight.
- **The generator.** I downloaded the font from the URL in its docstring; its sha256 is `8c2c290c…19d5`, as pinned.
  `uv run --with fonttools --with brotli python3 wordmark.py IBMPlexMono-Medium.woff2`, run in the scratch clone,
  rewrites `wordmark.svg` and `logo.svg` **byte for byte**: `git status` stays empty.
- **The ink boxes.** I rendered the wordmark at 1x in Chrome and compared it with
  `renders/site-header-light-1x.png`. Both ink boxes are 129 × 16. The mark's pixels are identical, and 403 of the
  name's 415 ink pixels coincide. The rest is antialiasing: a path against the site's text rasteriser.
- **`labels.yaml`.** It sets `tagline` and `footer`, both labels. They are `docs/de/index.md`'s claim (line 5) and
  its D2 line (line 3). An added unknown key is warned in the build (`bogus.key is not a label`), not in `--check`.

**The diff as a whole** (`git diff v0.18.0 06d884e -- shoalmark.py`, +95 −19).
- Nothing beyond the brief.
- `BRAND_FILES` gains `wordmark.svg`. Because of that, `--vendor` also copies an organisation's `brand/wordmark.svg`
  beside the tool, and a loose `wordmark.svg` beside the trackers is warned about. Both are consistent with the other
  brand files. `work-tracker/brand/` is never vendored, as the CHANGELOG says.
- Every caller of `brand()` takes the sixth value.
- **Performance.** `inline_svg` takes 54 ms on a 192 kB one-path file, and 59 ms on a 173 kB file of 3 300 elements.
  The build was not timed against 0.18.0.

## The sanitiser, case by case

I called `inline_svg()` directly from a scratch clone. I then built boards there and opened them in headless Chrome
153.0.8010.53, with a logging HTTP server on `127.0.0.1:8765`. Positive control: an `<img>` to that server is fetched.
*Refused* means one warning and the header keeps the logo and the name. *Shown* means the markup is inlined.

| # | Case | Result | Rebuilt markup |
|---|---|---|---|
| 1 | `<script>` | refused: *it holds \<script>* | — |
| 2 | `<h:script>` in the XHTML namespace; `<script xmlns="">` | shown, the element dropped with its subtree | clean |
| 3 | `onload` on the root, `onclick` on a path, `ONLOAD`, `xlink:onload` | refused: *it holds a handler* | — |
| 4 | `<style>` | refused | — |
| 5 | `<foreignObject>`, `<image href>`, `<a href="javascript:">` | refused: *it holds \<…>* | — |
| 6 | `<use href="http://…">`, `xlink:href="javascript:"`, `HREF="javascript:"`, `href="data:…"` | refused: *it refers outside the file* | — |
| 7 | `<use href="#p">` and `xlink:href="#p"` of its own id | shown | `id="wm-p"`, `href="#wm-p"` ✓ |
| 8 | `fill="javascript:alert(1)"` | shown | the text passes as a paint value; it runs nothing |
| 9 | `fill="url(data:…)"`, `style="fill:url(http://…)"`, `image-set('http://…')`, `&#117;rl(http://…)` | refused | — |
| 10 | `<!DOCTYPE … <!ENTITY …>`, billion laughs, `<![CDATA[</svg><script>…]]>`, all in UTF-8 | refused: *it declares a DOCTYPE, an entity or CDATA* | — |
| 11 | `&lt;script&gt;` and `&quot; onmouseover=&quot;` in an attribute; `&lt;/svg&gt;&lt;script&gt;` in text | shown | re-escaped: `&lt;`, `&gt;`, `&quot;` ✓ |
| 12 | `viewBox` NaN, negative, 1e309 | shown | passed through; Chrome ignores it |
| 13 | `width="50em" height="100%"` | shown | 800 × 98 in the header |
| 14 | ids `H` and `s` | shown | `wm-H`, `wm-s`; the page has no `wm-` id ✓ |
| 15 | nested `<svg>` | shown | fine |
| 16 | `<animate>`, `<set attributeName="href">`, `<filter><feImage>`, `<marker>` | refused: *it holds \<…>* | — |
| 17 | `<pattern href="http://…">` · `<pattern href="#p">` | refused · shown with `#wm-p` | ✓ |
| 18 | `style="fill:url(#g)"` | shown | `url(#wm-g)` ✓ |
| 19 | **`style="background-image:u\72l(http://…)"` on the root; `fill="u\72l(http://…)"`; `style="fill:u\72l(…)"`, `mask:`, `clip-path:`, `-webkit-mask-image:` with the same escape; `u\rl(` too** | **shown** | **Chrome fetched 6 of 7 URLs with `\72` (not the `filter` attribute), and both with `\r` — R1** |
| 20 | `<use>` fanned out 10 × 10 × … six levels deep, 1.3 kB | **shown** | **Chrome does not render the board in 90 s; three levels render in 176 ms — R2** |
| 21 | UTF-16 file with `<!DOCTYPE … <!ENTITY a "…">` | **shown, the entity expanded** | the pre-check reads the bytes as ASCII — R3 |
| 22 | UTF-16, eight-level billion laughs, 1.1 kB | **3.9.6: shown, 30 MB inlined, 745 MB RSS, 2 s**; 3.14: refused by expat's amplification limit | R3 |
| 23 | UTF-16 external entity `SYSTEM "file:///etc/passwd"` | refused: *undefined entity* | — |
| 24 | UTF-16 `<script>`; UTF-16 plain; UTF-8 BOM | refused; shown; shown | ✓ |
| 25 | 1 000 nested `<g>` (7 kB) | **`RecursionError`: the build exits 1 with a traceback** | R4 |
| 26 | `style="position:fixed;inset:0;width:100vw;height:100vh;z-index:99;background:#fff"`, `autofocus tabindex="0"` on the root | **shown** | in Chrome it covers the whole board, and the wordmark takes the focus from `#q` — R5 |
| 27 | `xml:base="http://e.x/"` | shown | kept; references stay fragment-only, so nothing loads |
| 28 | Inkscape attributes; a `sodipodi:namedview` holding an SVG `<script>` | shown, both left out with their subtree | clean |
| 29 | `__ROWS__` in text and `__MARKED__` in `class` | shown | `&#95;&#95;ROWS&#95;&#95;` ✓ |
| 30 | a PI and a comment holding `</svg><script>` | shown, both dropped | clean |
| 31 | 192 kB · over 200 kB | shown in 54 ms · refused: *it is 200 kB — over 200 kB* | ✓ (R6 on the words) |

**What the rebuilt markup can hold.** No element outside `SVG_TAGS` reaches the page, and no text or attribute value
can break out of its context: `&`, `<`, `>` and `"` are re-escaped, and `_` is written `&#95;`. None of
`SVG_TAGS` makes the HTML parser leave foreign content. `<title>` and `<desc>` are HTML integration points, but only
`SVG_TAGS` can appear in them, and `title`'s RCDATA cannot close on an escaped `&lt;/title&gt;`. **Attributes have
no allow list.** Any name matching `[A-Za-z][A-Za-z0-9-]*` passes, except `on…`, and `href`/`src` unless they are
fragments. Its values are screened by one regular expression, and CSS escapes defeat it (R1). `style`, `autofocus`,
`tabindex` and `xml:base` all reach the page (R5).

## The CHANGELOG's claims, one by one

| # | Claim (§0.18.2) | |
|---|---|---|
| 1 | Where a place has `wordmark.svg`, the header shows it inline, in place of the logo and the name | ✓ |
| 2 | The name stays the `<title>` and is the wordmark's accessible name (`role="img"`, `aria-label`) | ✓ |
| 3 | The logo, where there is one, stays the browser tab's; the tagline and the footer stay labels | ✓ |
| 4 | The later place wins; `--brand` names the place | ✓ (the test's organisation → repository case; a refused later file leaves the earlier one) |
| 5 | Drawn in `currentColor`, it follows the theme's ink in light and dark and through `◐` | ✓ (Chrome; here the name's white on dark, as ruled) |
| 6 | It keeps the size its `<svg height>` gives, else the logo's 22 px | ✓ |
| 7 | A script, an `on…` handler, a `<style>`, a `<foreignObject>`, an image or a link refuses the file | ✓ |
| 8 | **A reference outside the file refuses it** | ✗ **CSS-escaped `url()` passes and Chrome fetches it (R1)** |
| 9 | Any element beyond shapes, text, gradients, masks and a `<use>` of its own ids refuses it | ✓ for elements. Attributes are not held to anything (R5). A `<use>` of its own ids can freeze the page (R2) |
| 10 | One warning that says why; the header keeps the logo and the name | ✓, except deep nesting: a traceback, and the build fails (R4) |
| 11 | Over 200 kB, the same | ✓ for the file. What is inlined is not bounded: 30 MB from 1.1 kB on 3.9 (R3) |
| 12 | An editor's own namespace is left out; every id is prefixed `wm-` | ✓ |
| 13 | Nothing to do on upgrade: without `wordmark.svg` the header is as it was | ✓ byte-identical to 0.18.0's |
| 14 | To draw your own: … `--brand DIR`'s starter says the same in a comment | ◐ the starter says `currentColor`, height, 22 px and the tab; it omits the `viewBox`, name-as-paths-or-`<text>`, the pixel grid and *shapes only* (R6) |
| 15 | shoalmark's own board: the Pricke beside the name in IBM Plex Mono, the tab icon, the site's palettes, IBM Plex from files beside the theme, the German claim | ✓ |
| 16 | It is this repository's place: `--vendor` never copies it | ✓ `--vendor` copies `brand/` beside the tool, never `work-tracker/brand/` |
| — | README §9 row, the `currentColor` paragraph, the layout row; `--help`; VERSION 0.18.2 | ✓; §9's *a reference outside the file refuses it whole* is false until R1 is fixed |
| — | FM-006's line and row: 16 px, Plex Mono 500, 16.1:1 / 10.4:1, 4.7:1 / 5.3:1, `6fe9b11`, the generator, the ink boxes, *nothing fetched from Google* | ✓; the row's time is off (R6) |

## Findings

**R1 · P1 · confidence high (Chrome, reproduced) · A CSS escape in a `style` or presentation attribute makes every
viewer's browser fetch a URL.**
- `far` looks for the literal `url(`, `src(`, `…image…(` and `cross-fade(`. CSS resolves escapes in a function's
  name, so `u\72l(http://…)` and `u\rl(http://…)` are a `url()` to the browser and invisible to the regex.
  `:1812` checks the XML-decoded value, which is right, but that value still holds the backslash.
- A `wordmark.svg` whose root carries `style="background-image:u\72l(http://127.0.0.1:8765/…)"` builds with no
  warning. The page holds the attribute verbatim, and Chrome requests it on load.
- In the same file, Chrome also requested the URL from a `fill` attribute, and from `fill`, `mask`, `clip-path` and
  `-webkit-mask-image` in `style`. Six of seven vectors fetched; only a `filter` attribute did not. A second file
  with `u\rl(` in the root's `style` and in a `fill` fetched both URLs.
- **The effect:** a brand file inlined into every viewer's page beacons out, with the viewer's IP and when they
  opened the board. This is what the sanitiser exists to stop. The tests never try an escape.
- **Fix:**
  - refuse any attribute value that holds `\` once decoded (`&#92;` decodes to one too);
  - better, pair it with the attribute allow list of R5;
  - add a test that refuses `u\72l(` and `u\rl(` in `style` on the root and in `fill` on a path.

**R2 · P2 · confidence high (Chrome) · A `<use>` of the file's own ids can fan out into millions of instances and
freeze the viewer's page.**
- `<g id="l0"><path/></g>`, then six groups, each holding ten `<use>`s of the one before, and one `<use>` of the
  last. That is 1.3 kB and 10⁶ instances. It is shown with no warning, and headless Chrome had not rendered the
  board after 90 s.
- The same file three levels deep renders in 176 ms. So does the real wordmark.
- The 200 kB cap does not bound this. Nor does a no-nesting rule: 5 000 `<use>`s of one 5 000-path group fit in
  200 kB.
- **Fix:**
  - count the instances the file expands to: each `<use>` costs its target's subtree, recursively;
  - refuse above a cap such as 10 000 elements, with one warning;
  - test it with the fan-out above.

**R3 · P2 · confidence high (measured on 3.9.6; the tenth level extrapolated, not run) · The DOCTYPE, ENTITY and
CDATA refusal is bypassed by encoding the file as UTF-16.**
- `re.search(rb"<!(?:DOCTYPE|ENTITY)|<!\[CDATA\[", data)` reads the raw bytes. In UTF-16 they are `<\0!\0D\0…`,
  and the regex never matches. `ET.fromstring` then decodes the file and expands its internal entities.
- On `/usr/bin/python3` (3.9.6, expat 2.2.8), an eight-level billion laughs of 1 106 bytes is **shown**:
  - 30 000 054 bytes are inlined into the header;
  - 745 MB RSS, in 2 s;
  - each level multiplies this by ten, and the classic ten levels is 1.3 kB.
- Python 3.14's expat 2.7.4 refuses it: *limit on input amplification factor*.
- The repository's own pre-commit hook runs both suites on `/usr/bin/python3`, and the suite reads this
  repository's brand (`fm.brand()` at `test_shoalmark.py:1216`). Such a file in `work-tracker/brand/` would exhaust
  memory on every `.py` commit on this machine.
- **Fix:**
  - decode strictly as UTF-8, after an optional BOM, and refuse anything else;
  - run the check on the text;
  - or, independent of encoding, give `ET.XMLParser().parser` a `StartDoctypeDeclHandler` and an
    `EntityDeclHandler` that raise;
  - test with a UTF-16 file that has a DOCTYPE.

**R4 · P3 · confidence high · A deeply nested file crashes the build instead of being refused.**
- `out()` recurses once per element. Nesting 1 000 `<g>`s (7 kB) raises `RecursionError`, which the
  `except ValueError` does not catch.
- `python3 shoalmark.py`, `--html-only`, `--print-written` and `--brand` then exit 1 with a traceback, on 3.14 and
  on 3.9.
- `--print-written` is the pre-commit hook's `tracker-index`. A commit that adds only the SVG passes the hooks,
  since its globs do not match. After that, every commit that touches a tracker fails in every clone until the file
  goes. `post-merge` fails silently (`|| true`). `--check` is unaffected.
- The failure is loud and the traceback names `inline_svg`, so this is P3. But it breaks §9's rule that a brand
  problem is a warning, never a failure, and that brand files never touch the gate's path.
- **Fix:** cap the depth, for example refusing past 64, or walk the tree iteratively. Catch `RecursionError` as a
  refusal. Add a test.

**R5 · P3 · confidence high (Chrome) · Attributes have no allow list: `style` can cover the whole board, and
`autofocus` takes the focus.**
- The CHANGELOG refuses `<style>` because it would restyle the board. A `style` attribute on the root can do the same
  to the viewer.
- `position:fixed;inset:0;width:100vw;height:100vh;z-index:99;background:#fff` blanks the page. In Chrome,
  `elementFromPoint` at the centre is the wordmark's `<text>`, which could say anything.
- `autofocus tabindex="0"` moves the focus from the search box (`<input id="q" autofocus>`) to the wordmark,
  because the wordmark comes first.
- `xml:base` is kept too, harmlessly.
- **Fix:** keep only the geometry, presentation, `id`/`class`, `href`, `viewBox`/`width`/`height`/
  `preserveAspectRatio`, `transform`, `xml:space` and `aria-*` attributes. For `style`, either refuse it (and say so
  in §9: export with presentation attributes) or keep only allowed properties. Drop `autofocus` and `tabindex`. This
  also narrows R1.

**R6 · P3 · confidence high · Where the words fall short.**
- **The starter** does not "say the same" as the CHANGELOG's *To draw your own*. It omits:
  - the `viewBox`;
  - the name as paths or as `<text>` in a font the theme loads;
  - the whole multiple of the pixel grid;
  - that anything beyond shapes and text refuses the file.
- **The size warning** reads *it is 200 kB — over 200 kB* for any file from 200 001 to 200 999 bytes, and the test
  asserts that sentence. Give the bytes, or round up.
- **FM-006's ship-log row** is stamped *2026-09-24 15:34 CEST*. Git has `6fe9b11` at 15:28:56 and the row's own
  commit `06d884e` at 15:42:39 (+0200). Earlier FM-006 reviews held the rows to git's times.
- **README §9's row** says *a reference outside the file refuses it whole*. That is untrue until R1 is fixed.

## What I could not verify

- **Other browsers.** Only Chrome was run. Firefox and Safari were not; Firefox also loads external SVG resources
  for `mask`, `clip-path` and `filter`.
- **R3 at full size.** The ten-level laughs were not run on 3.9, to keep the machine up. The eight-level run and the
  factor of ten per level are measured.
- **Interactive vectors.** A `cursor:u\72l(…)` fetch needs a hover, and was not driven.
- **Windows** was not run.

**Verdict:** NOT READY. R1 is P1; R2 and R3 are P2; R4, R5 and R6 are P3. **The Owner may not tag this tip after the
merge of main.** First: R1–R3 fixed in `inline_svg()`, each with a test that fails today, and a verification. R4 and
R5 are best fixed in the same pass, since the attribute allow list and the depth cap are a few lines each.

## Pass on 3f4b4a4 (2026-09-24 17:29 CEST, Reviewer, session `8e509911/reviewer-1`)

**Scope.** The merged tip `3f4b4a4` (`3f4b4a47e541c96a1ea325a78118a66a044fd3f0`) of
`fm/006-0-18-2-the-board-wears-the-mark`, on my verdict `552d6b4`.
- The Implementer's three commits, under `8e509911/implementer-17`:
  - `5622ff0`, the running line;
  - `a661c1d`, R1–R6;
  - `6f02499`, FM-006's rows.
- The Principal's merge of `origin/main` `86f7595` (v0.18.1 and PR 54), under `8e509911`.
- The same session root as before, reported.

### What I ran

- **Gates.** `--check` and `--session-check` exit 0. `python3 shoalmark.py` twice leaves `git status --porcelain`
  empty. `--brand` names `repository` for all four files; labels changed: 2 of 130.
- **Suites.** `test_shoalmark.py` is 336 ok and `test_core.py` 148 ok, on 3.14.3 and on `/usr/bin/python3` 3.9.6.
  All green, run one after another.
  - The branch claimed 323 before the merge. The merge brought main's 0.18.1 checks; I did not run `6f02499` alone.
  - Both Chrome checks ran: the wordmark's ink through `◐` (`light=rgb(1, 2, 3)/16px`, `dark=rgb(253, 252,
    251)/16px`), and the running line on both screens.
- **The brand.** `git diff 06d884e 3f4b4a4` is empty for `work-tracker/brand/`, the generator, `pricke.svg`, the
  favicon and the site's stylesheet, so the first pass's findings stand:
  - the palettes, fonts, licence and `logo.svg` are as the first pass found them;
  - the generator, re-run here, rewrites `wordmark.svg` byte for byte;
  - the new `inline_svg` gives this repository's wordmark the same markup as `06d884e`'s did;
  - without `wordmark.svg`, the header is still byte-identical to 0.18.0's.
- **Nothing is fetched by the page.** Before the first `<script>`, the only `src`/`href` to `http(s)` are the running
  line's two `<a>`. The page has no `<link>` but the data-URI favicon, and no `@import`.

### R1–R6 at `06d884e`

| | Grade then | Now | Evidence |
|---|---|---|---|
| R1 · CSS-escaped `url()` fetches | P1 | **closed** | `\` is banned in every value, including `&#92;` and `&#x5c;` once decoded. `style` is not an attribute any element takes. `fill` is only a colour or `url(#id)`. The first pass's attack file now builds with the warning *it holds style= on \<svg>*, and the page holds no `u\72l`. |
| R2 · `<use>` fan-out freezes the page | P2 | **open (R7)** | The 1.3 kB fan-out is refused. The same fan-out, with each id defined twice, is shown and freezes Chrome. Nested masks go around the count altogether. |
| R3 · UTF-16 skips the DOCTYPE refusal | P2 | **closed** | UTF-16 with a BOM, UTF-16 without one (*control character*), a UTF-8 BOM, and `<?xml encoding="UTF-16|US-ASCII|latin1">` are all refused before the parse. The parser is forced to UTF-8. A DOCTYPE in any case, an ENTITY and CDATA are refused. |
| R4 · deep nesting crashes the build | P3 | **closed** | The walk is iterative. Depth 32 passes and 33 is refused. 1,000 nested `<g>` give one warning, and the build and `--print-written` exit 0. |
| R5 · no attribute allow list | P3 | **closed** | A list per element. `style`, `class`, `autofocus`, `tabindex`, `xml:base`, `xml:lang`, `xlink:title` and `HREF` are refused, and so is `xlink:href` off `<use>`. |
| R6 · the words | P3 | **closed** | The starter states the whole rule. The size warning names the bytes (*200,001 bytes — over 200,000*; 200,000 exactly passes). FM-006's rows are at git's times: `06d884e` 15:42, `5622ff0` 16:23, `6f02499` 16:49. README §9 is rewritten. |

### The sanitiser, second pass

I called `inline_svg()` from a scratch clone at the tip, and built and opened boards in headless Chrome
153.0.8010.53.

| Case | Result |
|---|---|
| The first pass's cases, all re-run | every attack refused, or dropped with its subtree where it is in another namespace. Shown: `<use>` of its own id, text with escaped markup, a nested `<svg>`, editor namespaces dropped, a PI and a comment dropped, a 192 kB path in 17 ms |
| `url(#nope)`, an id the file lacks · `url(#H)`, `mask="url(#s)"`, `clip-path="url(#B)"`, the page's ids | shown as `url(#wm-nope)`, `url(#wm-H)`…. Harmless: the page has no `wm-` id, so they resolve to nothing. But the claim is *of its own id* (R9) |
| `url( #x)` · `url(#x) url(http://…)` · `URL(#x)` · `url('#x')` · `url(#x) red` | refused by the grammar |
| `&#92;` · `&#x5c;` in a value | decoded to `\`, refused |
| `&#117;rl(#x)` | decoded to `url(#x)`, shown as `url(#wm-x)`, the same as written |
| `&#x3c;` in `d` · `A` in `d` · `transform="url(#x)"` | refused |
| `width="١٢"` · `x="１"` | **shown**: `\d` matches any Unicode digit. The browser ignores the value, so this is harmless (R9) |
| `<use href="#H">`, the page's id · a `<use>` with no `href` · a dangling `href` | refused: *the file does not have* |
| self-cycle · mutual cycle · a `<use>` of the root's own id | refused: *a cycle* |
| a `<use>` chain 5 deep | refused: *deeper than 3* |
| **a `<use>` chain 7 deep, each id defined twice** (a real group, then an empty decoy) | **shown** — the cap sees the decoys (R7) |
| **the 6-level × 10 fan-out, each level followed by an empty duplicate id, 1,348 B** | **shown with no warning. Chrome does not render the board in 60 s; 3 levels render in 150 ms (R7)** |
| **nested masks: `<mask id="mK">` holding 10 `<rect mask="url(#mK-1)">`, 4.5 kB at 7 levels** | **shown. The screenshot takes 10 s at 6 levels and 79 s at 7, against 2 s for the clean board (R7)** |
| **`<text x="111 111 … 111 !">`, a failing value, 170 B** | **refused, after 186 s. Every number triples the time; 30 numbers (246 B) hang the build (R8)** |
| **`transform="scale(1)  scale(1) … !"`, 14 functions** | refused, after 1.1 s, and tripling per function (R8) |
| `width` = 20,000 digits and `!` | refused, after 12.9 s: quadratic. At 200 kB, about 20 minutes (R8) |
| `<g id="a">` of 1,000 paths and 11,000 `<use href="#a">`, 183 kB | refused after 11.2 s on 3.14 and 16.7 s on 3.9 (R9) |
| XHTML `<script>` · `<script xmlns="">` · an SVG `<script>` inside a foreign element · a foreign `e:onload` | dropped with their subtree, or left out |
| `<s:script>` in the SVG namespace | refused |
| `<title><title>&lt;/title&gt;&lt;img onerror…&gt;</title></title>` · `<desc><svg>` | shown, still escaped. The only names the parser can meet in an integration point are `SVG_ATTRS`' own, and an HTML `title`'s RCDATA holds text only. No way out of `<b class="wm">` |
| `font-family="'Evil', x"` | shown. It names a font, and fetches nothing unless the theme defines it |
| NUL · `\x0b` · `\x0c` | refused |
| DEL (U+007F) and C1 (U+0085) in text | **shown**. The rule says *no control character but tab and line ends*. Harmless (R9) |
| 200,000 bytes · 200,001 bytes | shown · refused, with the bytes |

### The running line

Chrome probe on the board, on FM-033's view and on FM-007's view:
- **Where it sits.** `<p id="r" class="m">` is in the page between `</article>` and `<dialog>`, after `#B` and
  outside `#v`. It shows on the board (`#B` shown, `#v` hidden) and in both tracker views (`#B` hidden, `#v`
  shown). It sits below the footer and below the view.
- **The mark.** An inline `<svg>` of 16 × 16, `fill="currentColor"`, `aria-hidden="true"`. Its fill and the text are
  `rgb(131, 133, 137)`, which is the theme's dark `--mute` `#838589`. The line is 11 px in IBM Plex Mono.
- **The links.** Two `<a>`, both with `target="_blank"`, `rel="noopener"`, and an `aria-label` (*shoalmark on
  GitHub*, *release v0.18.2*). The first holds the mark and the name. ` · ` stands between them as plain text. They
  point to `https://github.com/holgo99/shoalmark` and `…/releases/tag/v0.18.2`.
- **A vendored copy links its own version.** I ran `--vendor --allow-untagged` from the scratch clone into a
  consumer, and set the copy's `VERSION` to 0.17.4. `--init` and `--html-only` then give `…/releases/tag/v0.17.4` and
  `v0.17.4`.
- **The constants.** `TOOL_PAGE` is at `:52`, beside `SIGNING_PAGE` at `:51`. `PRICKE` equals `pricke.svg`'s `d`.
- **test_core's positive control works.** The check skips `<a ` only. I planted `<img alt="" src="https://…">`
  after `__RUNNING__`, then an `<a>` holding `<img\nsrc="https://…">`; in both cases *no external request of any
  kind* fails. The check's built-in control, an `<img>` that must match, holds.

### The merge

- `3f4b4a4^2` is `origin/main` `86f7595` (v0.18.1 at `1251f84`, then PR 54). `VERSION` is 0.18.2.
- **The CHANGELOG** runs 0.18.2, then 0.18.1, then 0.18.0. The 0.18.2 section equals the branch's. The 0.18.1 section
  and everything from 0.18.0 down equal main's, and so does the preface.
- **The branch's side survives whole.** For `shoalmark.py`, both suites and README, `git diff 86f7595 3f4b4a4` has
  exactly the lines that `git diff 095f1d3 6f02499` has.
- **0.18.1's relation is still on the board, next to the running line.** FM-033's view reads *the Owner's answer —
  accepted - a pass judges … · **accepted the proposal** · 2026-09-24 · holgo99*, and FM-007's reads *… · accepted
  the proposal*, with `shoalmark · v0.18.2` below. The six `relation.*` labels are in the page.

### Findings, second pass

**R7 · P2 · confidence high (Chrome, reproduced) · R2 is not closed: the expansion cap counts a different graph from
the one the browser draws.**
- `ids[v] = e` keeps the **last** element with an id, but the browser resolves `href="#wm-x"` to the **first**.
- Define every level twice, a real group and then an empty `<g id="lK"/>`. `drawn()` then sees a 1-deep graph that
  draws a handful of elements, while Chrome draws 10⁶.
- The R2 fan-out rebuilt this way is 1,348 bytes. It builds with no warning, and Chrome had not rendered the board
  after 60 s. The same file at 3 levels renders in 150 ms.
- **The `<use>` depth cap falls the same way:** a 7-deep chain with decoys is shown.
- **Masks go around the count entirely.** `mask="url(#…)"` is allowed on shapes inside a `<mask>`, so 7 levels of 10
  (4.5 kB) take 79 s to paint, where the clean board takes 2 s. `drawn()` counts `<use>` only. `clip-path` inside
  `<clipPath>` has the same shape; I did not time it.
- The CHANGELOG's *2,000 elements with its `<use>`s expanded, `<use>`s at most 3 deep* does not hold.
- **Fix:**
  - refuse a second element with the same id (one line where `ids[v]` is set);
  - refuse `mask` and `clip-path` on anything inside a `<mask>` or `<clipPath>`, or count each `url(#…)` reference
    as an expansion in `drawn()` with the same chain and depth caps;
  - add a test with the decoy fan-out and the mask chain.

**R8 · P2 · confidence high (measured on 3.14 and 3.9) · The value grammar backtracks exponentially: a 246-byte
wordmark hangs every command that builds the board.**
- **The numbers.** `_N = [+-]?(?:\d+\.?\d*|\.\d+)…` splits the digit run `111` three ways: `\d+` 1–3, `\d*` the rest.
  `x`, `y`, `dx` and `dy` repeat `_N`, so a failing value is tried in every combination.
  - Measured on 3.14: 14 numbers take 2.1 s, and 18 numbers (170 B) take 186 s.
  - On 3.9, ×3 per number: 0.24 s, 2.05 s, 18.7 s at 12, 14 and 16.
- **The transforms.** `_TRANSFORM` puts `\s*` both before and after each function. The spaces between two functions
  can be split between them, so a failing value tries every split: tripling per function.
- **Long numbers.** A single long number is quadratic: 20,000 digits take 12.9 s.
- **What hangs.** With `x="111 " × 30 + "!"` (246 bytes) in `work-tracker/brand/`, `--print-written` (the
  pre-commit hook) and `--brand` were killed at 60 s. So is `python3 shoalmark.py`, and `--html-only`, which the
  `post-merge` hook runs, so `git pull` hangs in every clone. So does the suite, which reads this repository's brand.
  `--check` is unaffected.
- A hang says nothing, where R4's traceback at least named `inline_svg`. So this is worse than R4 was.
- **Fix, tested here:**
  - `_N = [+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?`, which is unambiguous, with `[0-9]`, not `\d`;
  - `_TRANSFORM = \s*F(?:[\s,]*F)*\s*`, with `F` one function;
  - with these, the 121-character `x`, a 200,000-digit number and 5,000 failing transforms refuse in 0.4 ms, 23 ms
    and 1.6 ms, and `1 2.5px,3%`, `translate(1,2) scale(2)` and `translate(1,2)scale(2)` still pass;
  - cap each value's length, for example 1,000 characters except `d` and `points`;
  - add a test that a failing 300-character `x` and `transform` refuse in under 0.1 s.

**R9 · P3 · confidence high · Smaller gaps between the rule and the code.**
- **The counter.** `drawn()` checks the cap only after an element's children are summed. Its docstring says *it stops
  as soon as the count passes the cap*. A 183 kB file of one 1,000-path group and 11,000 `<use>`s of it costs 11 s on
  3.14 and 17 s on 3.9 per build before it is refused. Fix: pass the running total down and raise the moment it
  passes the cap.
- **`url(#id)` of an id the file lacks is shown.** The code comment and the CHANGELOG say *of the file's own id*. It
  is harmless, since `wm-` matches no id on the page. Fix: check `url(#…)` targets against `ids`, as `<use>` is
  checked.
- **Unicode digits pass** (`width="١٢"`), because `\d` is Unicode in a `str` pattern. Harmless. The R8 fix's `[0-9]`
  closes it.
- **DEL and the C1 controls pass,** against *no control character but tab and line ends*. Add `\x7f-\x9f` to the
  class.

### Not verified

- Firefox and Safari; Windows.
- The `clip-path` chain was not timed.
- The R8 hang was ended at 60 s and 186 s; the longer times are extrapolated from the growth measured.

**Verdict:** NOT READY. R1, R3, R4, R5 and R6 are closed. R7 (R2 not closed: duplicate ids and nested masks) is P2.
R8 (the grammar's backtracking hangs the build and the hooks) is P2. R9 is P3. The running line and the merge are
confirmed. **The Owner may not tag this tip.** First: R7 and R8 fixed, each with a test that fails today, and a
verification.
