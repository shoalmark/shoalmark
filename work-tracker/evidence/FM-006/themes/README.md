# The themes, for the board and the site — the GtM/Design seat, 2026-09-25 and 2026-09-26

**Candidates on the real board and the real site, CSS only. Nothing adopted, nothing built.** Two themes, `monochrome`
and `shoalmark`, each for the board and for the documentation site. Both draw a nautical chart behind the page:
`monochrome` muted, `shoalmark` in the chart's blue-grey. Each stylesheet is a `theme.css` layer under FM-002's one rule,
over the page the tool writes today and the pages Zensical writes today.

## What the Owner said — in chat, spelling normalised

His words, not a signed answer. The ask drafted at the end is how they become one.

2026-09-25:
- The start, on WebTUI (webtui.ironclad.sh): *"to give it that terminal feel and be the perfect companion to the
  codex/claude terminal sessions"*. The seat's answer: WebTUI's idiom, not the library. The library styles its own
  attributes, so it would mean rewriting the tool's markup and shipping someone else's CSS into every consumer's board.
- On the last line: *"move icon + shoalmark + version to the right; move the claim where it was before, left aligned;
  remove the top separator"*.
- *"All are keepers. My guess is that users might want a setting for a theme, a theme library and a way to make their
  own — that is what we tried with the branding anyway."*
- On the seat's cheapest step: *"I agree to this direction"*. The step was to ship the themes as files in the tool's
  `brand/themes/`, have `--brand DIR --from <theme>` write a starter from one, choose a theme by putting a file in a
  place, and keep the four-place rule with no setting.
- *"We need a `shoalmark` theme besides the `monochrome` theme. Seekarte is a nice start but too playful. We need a
  strong starter."*

2026-09-26:
- *"Only `monochrome` + `shoalmark + graticule` themes. The design must go also into `site/`."*
- *"The graticule must look more like on a real nautical chart and have also coordinates / degrees."*
- *"The monochrome site shall also get the graticule, but muted."*
- *"Move the claim, shoalmark and version outside the inner chart area into a footer"*, like the site's foot.
- What he singled out on the seat's review page: its top — the navy band ending at the drying line, the headline in
  Plex Mono over the graticule — and its boxes titled in their border, the magenta one holding the drafted ask. That page
  was a private artifact; he deleted it and asked that none be published. Nothing about the themes lives outside this
  folder.

The three further mockups of 2026-09-25 (`catkin`, `bagels`, `seekarte`) are dropped on his first line of 2026-09-26.
Their stylesheets and renders are in git at `96aa05e`.

**The Auditor seat's counsel, relayed by the Owner on 2026-09-25.** Its three fixes are in every file here:
- a marker's alt text is `""`, the chart's figures included;
- the owner's box holds 100ch of prose;
- the site parity is a choice within the ruled IBM Plex family — no signed answer binds the board's face to the site's.
  The site themes keep IBM Plex Sans for prose and set in Mono what is the tool's: the name, the navigation, the
  headings with their marks, tables and code.

Its hold ("file after v0.18.4 is tagged") was lifted by the Owner's *"You file this"*. v0.18.4 is not tagged.

## The files

| File | For | Base | What it is |
|---|---|---|---|
| `monochrome.css` | board | — | **The terminal cut.** The site's palette. IBM Plex Mono for every word, on one grid. Boxes are titled in their top border; the search is a `>` prompt; an action is a `[ bracketed ]` word; a group is a `// comment`; a tracker's view prints its `#` marks. The frame is 104ch, so the owner's box holds 100ch of prose. The last line — the claim on the left, the mark, the name and the version on the right — stands below the chart in a foot of its own: the raised surface under a rule, full width. The chart, muted: greys at a few per cent. |
| `shoalmark.css` | board | monochrome | **The brand's own, and the starter to make yours from.** A sea chart's colours as ECDIS draws them (IHO S-52): pastel by night, deepened to 4.5:1 by day. The name stands in a navy band, full width, which ends at a drying line in the Watt's green. The Watt's green carries headings, the prompt and the running mark. Land buff carries the record's header row and the ids. Magenta carries what is owed to the Owner and nothing else. Status marks take the buoyage's shapes: sphere, starboard cone, special mark's cross, port can. The chart in its blue-grey, between the navy band at the top and the navy band of the foot, under its own drying line, where the mark and the name take the drying line's green. Every rule names only tokens, so a fork changes two blocks. |
| `site-monochrome.css` | site | — | The terminal cut on Zensical's modern theme: the site's own palettes, a rule under the header, Mono for the name, the navigation (`>` marks the page you are on), the headings with their `##` marks, tables and code; tables and code boxed, square. The chart, muted. |
| `site-shoalmark.css` | site | site-monochrome | The board's `shoalmark` carried over: the navy band with its drying line as the header, and again as the foot; the chart in its blue-grey between the two; the Watt's green for the headings' marks and the page you are on; land buff across a table's head; links in the chart's blue. Magenta stays unused: on the board it marks what is owed to the Owner, and the site owes him nothing. |

## The chart

The page is a Mercator sheet of Neuwerk's Watt, where the Pricken stand: the claim's own water. The top left corner of
the chart is 53°57'N 8°24'E.

- **The graticule.** A parallel every minute of latitude, 100.8px apart; a meridian every two minutes of longitude,
  118.8px apart. At 53.9°N two minutes of longitude are 1.18 minutes of latitude long, so the cells are as wide as a
  Mercator chart draws them there.
- **The border.** As a chart's: an outer line, a 5px band of alternate minutes, the neatline inside it, the tenths of a
  minute ticked on its inner edge (fifths along the top).
- **The figures.** Outside the border, 11px Plex Mono: latitude down both sides, the full figure at the top and at every
  ten minutes (`53°57'N`, `56'` … `53°50'`); longitude along the top every two minutes (`8°24'E`, `26'` … `8°30'`), each
  centred on its line. A longitude cell is 18ch, so it is the meridians' spacing exactly. The figures fade out before the
  frame's right edge, where a meridian's figure may be cut.
- **How it is drawn.** Behind the page, by pseudo-elements, with no markup: on the board the root's and the body's
  (`html::before` the frame, `html::after` and `body::after` the latitudes, `body::before` the longitudes); on the site
  the body's and `.md-container`'s, because Zensical positions the body, grows it with the page and sets the scheme as
  an attribute on it. The site's header and foot cover the chart.
- **The foot.** On the board the last line leaves the chart for a band of its own, full width, as the site's foot: the
  running line paints it, a border image outset 24px above it and out to the page's sides and end, so it holds a claim
  that wraps, shows in the tracker view too and adds no scroll. The chart ends 12px above it; the latitude figures fade
  out before its end.
- **Where it shows.** Only where the margins hold it: the board from 1040px, the site from 1380px. A narrower window
  shows today's plain ground and today's last line. Never in print.
- **What it is not.** The figures are a drawing, not a position: the page is not a chart.

## How it was made and checked

- **The pages are the real ones.** `build-mocks.py` injects the stylesheets into `work-tracker/index.html` as
  `python3 shoalmark.py --html-only` writes it, and into every page of `site/` as `zensical build` writes it (0.0.65,
  installed in a throwaway virtualenv), after the site's own `stylesheets/shoalmark.css`. Nothing else changes.
  `render.mjs` renders them in Chrome with the colour scheme emulated; a site page is also told by its toggle's
  attribute, because Zensical remembers the last scheme.
- **Fonts.** On the board, Plex Mono SemiBold and Italic come from `@ibm/plex-mono` 1.1.0's split Latin-1 cuts, the
  release whose Regular the repository already carries (sha256 `10d3c7fa…`, identical). Every drawn character is
  Latin-1: `°` and `'` included, no box-drawing glyph. The site loads Mono 600 from Google Fonts, as its
  `shoalmark.css` already loads 500.
- **Contrast, both schemes.** Every text pair a rule uses measures 4.5:1 or more, and every status mark 3:1 or more. The
  board's palettes are unchanged since 2026-09-25: `shoalmark` 29 text pairs and 8 mark pairs, `monochrome` the 7 pairs
  its rules add. New on 2026-09-26, 27 pairs: the chart's figures on each ground, board and site (4.75:1, `monochrome`'s
  muted figures by day, to 6.94:1); the board's foot — the claim and the version on the band (8.2:1), the mark and the
  name in the drying line's green (6.06:1 by day), `monochrome`'s on its raised surface (4.84:1 by day); and the site's
  own — its navigation, links, inline code, header and foot, table heads, prose and heading marks (5.76:1 to 16.6:1). The chart's lines, its border and the boxes' borders are
  decorative and sit below 3:1.
- **Markers are drawn, never read.** In Chrome's accessibility tree the buttons are named `accept`, `reject`, `done`,
  `reschedule`, `OK — give me the command` and `abort` (2026-09-25). No chart figure is in the tree, on the board or the
  site, in either theme (2026-09-26). The controls: without the alt text, the board read `[ accept ]` and exposed `## `
  ×4, `// ` ×5 and `[ ` ×9; the chart's three strings — all 64 latitudes and 40 longitudes — are read in full.
- **Defects found in the mocks, and fixed there:**
  - At 104ch the group rows forced the table to 993px, past an 874px frame: `td.m` never wraps. They wrap now.
  - `shoalmark`'s band covered the tracker view's first line. The view now starts below the chart's top border.
  - The rightmost longitude figure was cut in half at the frame's edge. The figures now fade out before it.
  - On the site, the figures ran on over the foot while the frame stopped under it. The foot now covers both.
  - On the site, `monochrome` marked the page you are on in Zensical's lavender. It is the raised surface now.
  - The foot's margins lost to the last line's own rules, later in the file, and the board's last rows ran over the
    chart's bottom border. The foot's rule is the more specific now.
- **Not verified:** a phone's width (the chart is off there by design; headless Chrome will not go below about 500px),
  Firefox and Safari, and print.

## What the build is — not done

It is code and documentation outside `work-tracker/`, so a pass judges it first (FM-033) and the full review loop
follows:
- `brand/themes/monochrome.css` and `shoalmark.css` in the tool, with the two fonts beside them.
- `--brand DIR --from <theme>`, writing the starter from a theme.
- In the board's markup:
  - the owner's box title as a label, because `labels.yaml` cannot reach CSS `content:`;
  - one footer element, because lifting the running line onto the claim's line is a CSS workaround — the foot's band
    hangs from the lifted line;
  - a class on striped rows, because group rows break `nth-child`.
- The site: the theme it wears, as lines in `docs/stylesheets/shoalmark.css`. The site wears one; it has no picker.

The one rule and "no setting" stay. The tool's default look stays for every consumer: a theme is a file someone puts
in a place.

## The ask, drafted

It is raised when FM-006's open ask (going public) is answered, because a tracker holds one ask.

> **ask:** Does shoalmark ship two themes — monochrome and shoalmark, each drawing a nautical chart behind the page, as
> files in the tool's brand/themes/ that `--brand DIR --from <theme>` starts from — and which do its own board and site
> wear?
> **options:** both, the board and the site wear shoalmark | both, the board and the site wear monochrome | not yet —
> the board and the site keep today's look · **proposal:** both, the board and the site wear shoalmark — the brand's
> own, and the starter the library is made from

## Renders

`shots/`: each theme's board, its foot, its answer dialog and its site's start page, dark and light; `shoalmark`'s
tracker view. The board at 1300px, the site at 1440px.

| | dark | light |
|---|---|---|
| monochrome — the board | ![](shots/monochrome-dark.png) | ![](shots/monochrome-light.png) |
| monochrome — the foot | ![](shots/monochrome-foot-dark.png) | ![](shots/monochrome-foot-light.png) |
| monochrome — the dialog | ![](shots/monochrome-dialog-dark.png) | ![](shots/monochrome-dialog-light.png) |
| monochrome — the site | ![](shots/site-monochrome-dark.png) | ![](shots/site-monochrome-light.png) |
| shoalmark — the board | ![](shots/shoalmark-dark.png) | ![](shots/shoalmark-light.png) |
| shoalmark — the foot | ![](shots/shoalmark-foot-dark.png) | ![](shots/shoalmark-foot-light.png) |
| shoalmark — the dialog | ![](shots/shoalmark-dialog-dark.png) | ![](shots/shoalmark-dialog-light.png) |
| shoalmark — a tracker | ![](shots/shoalmark-tracker-dark.png) | ![](shots/shoalmark-tracker-light.png) |
| shoalmark — the site | ![](shots/site-shoalmark-dark.png) | ![](shots/site-shoalmark-light.png) |

## Rebuild

```sh
python3 shoalmark.py --html-only
zensical build                      # the site: pip install zensical
python3 work-tracker/evidence/FM-006/themes/build-mocks.py /tmp/themes --plex <@ibm/plex-mono 1.1.0>/fonts/split/woff2
node work-tracker/evidence/FM-006/themes/render.mjs /tmp/themes work-tracker/evidence/FM-006/themes/shots
open /tmp/themes/shoalmark.html /tmp/themes/site-shoalmark/index.html
```

To see a theme on your own board today, put it in your own place, `~/.config/shoalmark/theme.css`: `monochrome.css`
first, then `shoalmark.css` for that theme. The fonts are not there, so the browser synthesises the bold and the italic.
