"""The board's brand files drawn from the site's (FM-006, 0.18.2) — `work-tracker/brand/wordmark.svg` and `logo.svg`.

    uv run --with fonttools --with brotli python3 wordmark.py IBMPlexMono-Medium.woff2

FONT is IBM Plex Mono Medium as IBM publishes it — @ibm/plex-mono 1.1.0, fonts/complete/woff2/IBMPlexMono-Medium.woff2
(https://cdn.jsdelivr.net/npm/@ibm/plex-mono@1.1.0/fonts/complete/woff2/IBMPlexMono-Medium.woff2, sha256 below): the
face the site sets its name in (docs/stylesheets/shoalmark.css, 500). The board has no font of its own to set the name
in, so its outlines become paths; the SVG then carries the name's shape, not a font. fontTools reads it; the tool never.

The site has no lockup file — its header composes the mark and the name. The wordmark is that composition, read off
the built header at 1x (renders/site-header-light-1x.png) and the theme's CSS, one unit = one CSS pixel:

- the mark: the site's own `overrides/.icons/shoalmark/pricke.svg` (`d`, the 16-unit grid) at 16 px, the ruled size,
  at x 0-16, y 0-16 — hard-edged (`crispEdges`), as the site draws it;
- the name: "shoalmark" at 18 px (.9rem), letter-spacing -0.025em (the theme's `.md-header__title`), its pen at x 36
  (the logo's 8 px padding + 4 px margin + the title's 8 px margin after the 16 px mark) and its baseline at y 14: in the
  render the ascenders of h, l, k start on the mark's top row and the baseline sits 2 px above the stake's foot;
- one colour, `currentColor`, for both — the page's ink, light or dark (the GtM's finding: the mark takes the name's ink).

logo.svg is the site's tab icon, `docs/assets/favicon.svg`, byte for byte: the mark alone, ink #1a1a1a, white where the
browser is dark. test_shoalmark.py holds both files to their sources.
"""
import hashlib
import pathlib
import re
import sys

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

FONT_SHA256 = "8c2c290cbd998fa1f647e4572aca6ebbd72589551b0f3f9f8bb8628fbb8219d5"   # the run prints the one it read
REPO = pathlib.Path(__file__).resolve().parents[5]
MARK = REPO / "overrides/.icons/shoalmark/pricke.svg"
TAB = REPO / "docs/assets/favicon.svg"
BRAND = REPO / "work-tracker/brand"
NAME, SIZE, TRACKING, PEN_X, BASELINE, HEIGHT = "shoalmark", 18, -0.025, 36, 14, 16


def num(v):
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def main(font_path):
    data = pathlib.Path(font_path).read_bytes()
    print(f"font {font_path} sha256 {hashlib.sha256(data).hexdigest()}")
    font = TTFont(font_path)
    glyphs, cmap, hmtx = font.getGlyphSet(), font.getBestCmap(), font["hmtx"]
    scale = SIZE / font["head"].unitsPerEm
    pen = SVGPathPen(glyphs, ntos=num)
    x, right = PEN_X, 0.0
    for ch in NAME:
        g = cmap[ord(ch)]
        glyphs[g].draw(TransformPen(pen, (scale, 0, 0, -scale, x, BASELINE)))
        x += hmtx[g][0] * scale + TRACKING * SIZE
        right = x - TRACKING * SIZE
    mark = re.search(r' d="([^"]+)"', MARK.read_text(encoding="utf-8")).group(1)
    width = int(-(-right // 1))
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {HEIGHT}" width="{width}" height="{HEIGHT}" '
           f'fill="currentColor"><path shape-rendering="crispEdges" d="{mark}"/><path d="{pen.getCommands()}"/></svg>\n')
    BRAND.mkdir(parents=True, exist_ok=True)
    (BRAND / "wordmark.svg").write_text(svg, encoding="utf-8")
    (BRAND / "logo.svg").write_bytes(TAB.read_bytes())
    print(f"wrote {BRAND / 'wordmark.svg'} ({len(svg)} bytes, {width} x {HEIGHT}) and {BRAND / 'logo.svg'}")


if __name__ == "__main__":
    main(sys.argv[1])
