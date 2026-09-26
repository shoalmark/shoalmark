# FM-002 slice A — shoalmark's own board and site wear the `shoalmark` theme (the brand layer)

**Built on the Owner's signed answer** (`4e00f85`, PR 90, 2026-09-26 13:54:50): *the tool ships monochrome and shoalmark
as starters; shoalmark's own board and site wear the shoalmark theme.* This slice is the second half — this repository's
own board and site — and the brand layer only: no `shoalmark.py` change (slice B ships the themes and the markup hooks).
Judged before its first build commit by the pass at `13d70189` (`tracker/triage-2026-09-26-the-build-judged`, READY WITH
FINDINGS): keep P2 #4 build; slice A docs/brand tier, one Reviewer pass, the Owner sees the renders before the merge. The
Implementer seat, session `8e509911/implementer-36`, worktree `shoalmark-impl-4`, branch `fm/002-slice-a-the-brand-layer`
off `origin/main` at `2a9f7eb` (PR 92).

## The brand layer — what changed

| File | What it is now |
|---|---|
| `work-tracker/brand/theme.css` | FM-006's aligned mock (`evidence/FM-006/themes/`, `9467b83`, PR 82) under the one rule: its base `monochrome.css`, then `shoalmark.css`, in one file, every rule as the mock wrote it but one (the placeholder, below). The header — the mark, the name, the switch — inline inside the chart's top border, as his word of 09:23:58 draws it. It replaces 0.18.2's site-brand theme, whose rules the mock's own override whole |
| `work-tracker/brand/fonts/` | two cuts added beside the Regular — IBM Plex Mono SemiBold and Italic, Latin-1 |
| `docs/stylesheets/shoalmark.css` | the file `zensical.toml`'s `extra_css` already names: its own lines, then FM-006's `site-monochrome.css` and `site-shoalmark.css`, every rule as the mock wrote it but one (the foot's link, below); no template, no `zensical.toml` change |
| `work-tracker/brand/labels.yaml`, `logo.svg`, `wordmark.svg` | unchanged: no board word changed |

**The fonts** — IBM's own Latin-1 files of `@ibm/plex-mono` 1.1.0, unmodified, under the SIL Open Font License in
`fonts/LICENSE.txt` (the package's `LICENSE.txt`, byte-identical, sha256 `7e6b2818…`). The tarball `npm pack` fetched was
checked against the registry first: sha1 `5406e372e2807b3cc1e78be6b8ea64256135c12d`, sha512
`hpsdRxR3BRJkC6wGM4MZcUFD6C8M+mmK76RtAy/hlsfPro9FzpXVdIWC+G3jeQOXof109dxlUvmeKxpeKUG68A==`; its Regular is the
repository's own. sha256, as the Regular is hashed:

| File | sha256 |
|---|---|
| `IBMPlexMono-Regular-Latin1.woff2` (0.18.2, the Auditor seat's match) | `10d3c7fa7eaf48e78db24f317b64f008a75e00f63a68bb3c2afc6ef51e58674f` |
| `IBMPlexMono-SemiBold-Latin1.woff2` (new) | `1ce95cff1c5056cb0fed049c2912823293b158b816e193a6f937f2d92b1e0f39` |
| `IBMPlexMono-Italic-Latin1.woff2` (new) | `08c4566f535253ee314ea35e4d75384a7bb151b4ed8345353698d95b33516d3b` |

The three Plex Sans cuts beside them are 0.18.2's; this theme sets every word in Mono and does not load them.

**The font urls** are written relative to `theme.css` (`fonts/…`); the brand layer re-bases them onto the page as
`brand/fonts/…` (the record's R2: the mock's `brand/fonts/` would have become `brand/brand/fonts/`). The built board
names three, all `brand/fonts/…`.

**The site's fonts:** one `@import`, at the top of `docs/stylesheets/shoalmark.css` where browsers honour it — the
file's own, widened from Plex Mono 500 to 500 and 600. The mock's second import is not added: 400 and italic 400 are
Zensical's own load, so there is no second Google Fonts load. **The self-hosting item stands as it is** — FM-006's open
item before the site is ever published: the pages load IBM Plex from Google Fonts, as they did before this slice; self-host
Plex under `docs/assets/fonts/`, its own slice.

**Two rules that are not the mock's**, each added where the built files measured a text pair below 4.5:1 (`361336a`;
the check is below):
- the board's placeholder — the search's and the dialog's note — was the browser's own `#757575`, 3.63:1 on the night
  panel; `::placeholder{color:var(--mute);opacity:1}` reads 6.48:1 by day, 6.42:1 by night. The tool's default board has
  the same ink on its own night ground, 4.19:1 — the tool's, not this slice's;
- the site's foot: Zensical's `html .md-footer-meta.md-typeset a:not(:focus,:hover)` outranks the mock's foot rule and
  painted the "Zensical" link in the page's ink on the band, 1.12:1 by day; `.md-footer-meta{--md-default-fg-color:
  var(--bandink)}` makes the band's ink the page's inside the foot, 13.69:1.

## The workarounds kept for slice B

The mock works around three pieces of markup the board does not have; `theme.css` keeps them and marks each
`WORKAROUND n of 3` where it stands. Slice B places the hooks in `shoalmark.py`, and this file is re-cut on them.
1. **The owner's box title** is CSS content — `#p::before{content:"owed to the owner"}` — English whatever
   `labels.yaml` says, because a label cannot reach CSS `content:`. It is read aloud (it is the box's name, not a marker).
2. **One footer element** — the claim (`#f`) and the running line (`#r`) are two elements, so `#r` is lifted onto the
   claim's line (`#B:not([hidden]):has(#f:not(:empty)) ~ #r{margin-top:-21px}`, the claim keeping 26ch clear) and the
   foot's band is `#r`'s border image, outset above it (`body #f,body #r{margin-top:60px}`, `#r{border-image:…}`).
3. **A class on striped rows** — the zebra is `tr.t:nth-child(even)`, which a group row shifts.

A fourth, from the record's second pass (R2): the tracker view shows no header, because `#H` sits inside `#B`, which the
view hides — as on today's board. A header there would be markup too.

## The renders — before and after

The board as `python3 shoalmark.py --html-only` writes it and the site's start page as `zensical build` (0.0.65) writes
it: **before** from `origin/main` (`2a9f7eb`), **after** from this branch at `361336a`, built one after the other at
2026-09-26 15:36 CEST, so the two boards hold the same trackers. Each at 1440 × 1000 and 390 × 844, dark and light, the
viewport's top; 16 PNGs in `shots/`, named `<page>-<before|after>-<width>-<scheme>.png`.

| | before — dark | before — light | after — dark | after — light |
|---|---|---|---|---|
| the board, 1440 | ![](shots/board-before-1440-dark.png) | ![](shots/board-before-1440-light.png) | ![](shots/board-after-1440-dark.png) | ![](shots/board-after-1440-light.png) |
| the board, 390 | ![](shots/board-before-390-dark.png) | ![](shots/board-before-390-light.png) | ![](shots/board-after-390-dark.png) | ![](shots/board-after-390-light.png) |
| the site, 1440 | ![](shots/site-before-1440-dark.png) | ![](shots/site-before-1440-light.png) | ![](shots/site-after-1440-dark.png) | ![](shots/site-after-1440-light.png) |
| the site, 390 | ![](shots/site-before-390-dark.png) | ![](shots/site-before-390-light.png) | ![](shots/site-after-390-dark.png) | ![](shots/site-after-390-light.png) |

What they show:
- **The board, 1440:** the chart behind the page, the header inline inside its top border (the mark, the name, the
  `[ ◐ auto ]` switch), the search a `>` prompt, the owner's box in magenta with its title set into the border. Before:
  0.18.2's site-brand look, Plex Sans on the plain ground.
- **The board, 390:** the chart is off by design below 1040 px; the header stands on the plain ground, as today's. The
  board's table is wider than 390 px and the page scrolls sideways (FM-006 measured 505 px under `shoalmark`); a render
  shows the left 390 px. At this width the legend's marks can wrap apart from their words (`■` at a line's end,
  *blocked* on the next) — the mock's too; not fixed here.
- **The site, 1440:** the navy band with its drying line as the header, the chart between it and the foot, Mono for the
  name, the navigation and the headings with their `##` marks. **390:** Zensical's phone layout under the same palette;
  the chart is off below 1380 px.

**How they were made** — `render.mjs` here, FM-006's `render.mjs` method (`shot()` as it is there — the device metrics,
the scheme emulated through Chrome's DevTools protocol, a site page also told by its toggle's attribute) with this
slice's widths and three additions: it waits for the page's fonts, it serves the site from 127.0.0.1 (opened as a file,
Zensical hides its search, so a file is not the page a reader sees — the board is opened as a file, as its reader opens
it), and it logs every request that leaves the machine. **Offline:** Chrome resolves no host but 127.0.0.1 and the two
Google Fonts hosts the site's own pages load (the self-hosting item above) — without them the site would render in a
fallback face nobody sees. `shots/requests.json`, per render: every board reached no host; every site page reached
`fonts.googleapis.com` and `fonts.gstatic.com` and was refused `api.github.com` (the header's repository counter). It
lists the 8 mock renders too (below); those are not committed.

**Against the mock** — the same run rendered FM-006's `build-mocks.py` output, built from the *before* board and site
(`--plex` the same 1.1.0 files), at the same sizes. Pixel for pixel, after against mock:
- the board, all four: identical but the placeholder — the one rule this slice added — 401–419 pixels, all inside the
  search box (`(310, 90)–(410, 102)` at 1440, `(43, 66)–(143, 78)` at 390);
- the site, all four: identical, but for 293 pixels (0.02 %) in one word at 1440 by day — the navigation's *Deutsch*,
  the antialiasing of a Google-served glyph; two of five runs showed none. The foot's fix lies below the viewport.

## Rebuild

```sh
S=/tmp/slice-a && mkdir -p $S/before $S/after
git checkout origin/main -- work-tracker/brand/theme.css docs/stylesheets/shoalmark.css           # before
python3 shoalmark.py --html-only && uvx zensical build
cp work-tracker/index.html $S/before/board.html && cp -R work-tracker/brand work-tracker/view site $S/before/
python3 work-tracker/evidence/FM-006/themes/build-mocks.py $S/mock --plex <@ibm/plex-mono 1.1.0>/fonts/split/woff2
git checkout HEAD -- work-tracker/brand/theme.css docs/stylesheets/shoalmark.css                  # after
python3 shoalmark.py --html-only && uvx zensical build
cp work-tracker/index.html $S/after/board.html && cp -R work-tracker/brand work-tracker/view site $S/after/
node work-tracker/evidence/FM-002/slice-a/render.mjs $S work-tracker/evidence/FM-002/slice-a/shots
```

The boards' *sessions* line reorders with the clock: two boards built minutes apart differ there.

## Not verified

- Firefox and Safari; print; a real phone — 390 px is Chrome's device metrics, not a device.
- How the board reads over a long session, and the dialog's second screen (the command) under the theme — the checks
  below open the first.
- The site live: `docs.yml` deploys only while the repository is public, so the site is **built** at the next release
  tag and goes **live** at the go-public act (the pass's R1); nothing here publishes it.
