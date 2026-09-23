"""The mark screen's renders — every picture in the ledger comes from here, nothing is drawn by hand.

    python3 marks.py sheet                      # every candidate at 16 px, one colour, light and dark ground
    python3 marks.py header SITE_DIR ID FONT [en|de] [default|slate] [dpr]   # the built site's header and claim, ID and FONT injected
    python3 marks.py type                       # renders/type-sheet.html (a committed source): the typefaces and the wordmarks

Sources are the SVGs in this folder (written by `sheet`). Rendering is headless Chrome at device-pixel-ratio 1, so a
16 px icon is 16 device pixels; the enlargements are nearest-neighbour (ImageMagick `-filter point`), so every pixel
seen in them is a pixel the browser drew.
"""
import pathlib
import re
import shutil
import subprocess
import sys

HERE = pathlib.Path(__file__).parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# id: (label, viewBox, body) — one colour: everything is currentColor
MARKS = {
    "K0": ("control: a filled square (pipeline check)", 16, '<rect x="2" y="2" width="12" height="12"/>'),
    "K1": ("control: the site's placeholder (lucide book-open)", 24,
           '<path fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
           'd="M12 5v16M20.001 19A2 2 0 0 0 22 17V5a2 2 0 0 0-1.999-2L16 3.002A5 5 0 0 0 12 5a5 5 0 0 0-4-2H4a2 2 0 0 0-2 2v12a2 2 0 0 0 1.999 2H8a5 5 0 0 1 4 2 5 5 0 0 1 4-2z"/>'),
    "K2": ("control: a lighthouse", 16, '<path d="M6.5 5h3l1.5 10.5h-6z"/><rect x="6" y="2.5" width="4" height="2"/><path d="M5.5 2.5 8 .5l2.5 2z"/>'),
    "A1": ("1 chart beacon: north cardinal (two cones up)", 16, '<path d="M8 .5l3.5 4h-7zM8 5l3.5 4h-7z"/><rect x="7" y="9" width="2" height="6.5"/>'),
    "A2": ("1 chart beacon: west cardinal (cones point to point)", 16, '<path d="M4.5 .5h7L8 4.5zM8 4.5l3.5 4h-7z"/><rect x="7" y="8.5" width="2" height="7"/>'),
    "A3": ("1 chart beacon as drawn: position circle, stake, topmark", 16,
           '<circle cx="8" cy="13.5" r="1.75" fill="none" stroke="currentColor" stroke-width="1"/><rect x="7.5" y="5.5" width="1" height="6.25"/>'
           '<circle cx="8" cy="1.5" r="1.25"/><circle cx="8" cy="4.25" r="1.25"/>'),
    "A4": ("1 chart danger symbol: dotted danger line around a cross", 16,
           '<circle cx="8" cy="8" r="6.5" fill="none" stroke="currentColor" stroke-width="1.5" stroke-dasharray="1.6 1.8"/>'
           '<rect x="7.25" y="4.5" width="1.5" height="7"/><rect x="4.5" y="7.25" width="7" height="1.5"/>'),
    "A5": ("1 the German Pricke: a withy stake with its twigs", 16,
           '<rect x="7.5" y="6" width="1" height="9.5"/><path fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" '
           'd="M8 7L3.5 1M8 7L5.5.5M8 7V.5M8 7l2.5-6.5M8 7l4.5-6"/>'),
    "A6": ("1 chart beacon as drawn, pixel-aligned: position circle, stake, two balls", 16,
           '<circle cx="8" cy="1.5" r="1.5"/><circle cx="8" cy="5.5" r="1.5"/><rect x="7" y="6" width="2" height="5"/>'
           '<circle cx="8" cy="13" r="2.25" fill="none" stroke="currentColor" stroke-width="1.5"/>'),
    "B1": ("2 isolated danger: two balls on a stake", 16, '<circle cx="8" cy="2" r="2"/><circle cx="8" cy="7" r="2"/><rect x="7" y="8" width="2" height="8"/>'),
    "B2": ("2 isolated danger: two balls on a stake, a water line", 16,
           '<circle cx="8" cy="2.5" r="2"/><circle cx="8" cy="7.5" r="2"/><rect x="7" y="9" width="2" height="6.5"/><rect x="2" y="13" width="12" height="1"/>'),
    "B3": ("2 isolated danger: the pillar buoy with its topmark", 16,
           '<circle cx="8" cy="1.6" r="1.4"/><circle cx="8" cy="4.4" r="1.4"/><rect x="7.5" y="5.5" width="1" height="4"/>'
           '<path d="M6 9.5h4l.35 2h-4.7zM5.4 13h5.2l.4 2.5H5z"/>'),
    "B4": ("2 isolated danger: the two balls alone", 16, '<circle cx="8" cy="4.5" r="3"/><circle cx="8" cy="11.5" r="3"/>'),
    "C2": ("3 typographic: the l as a stake through the water line (its 16 px form)", 16,
           '<rect x="7" y="1" width="2" height="14.5"/><rect x="1" y="10" width="14" height="1.5"/>'),
}
# C1's 16 px form is B1's glyph (the wordmark's l with the topmark); C1b's is the wordmark's i-like cut — see the ledger.

ROW, X_LIGHT, X_DARK, X_BIG = 72, 340, 380, 430


def svg(i, size=None, color="currentColor"):
    _, vb, body = MARKS[i]
    wh = f' width="{size}" height="{size}"' if size else ""
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {vb} {vb}"{wh} fill="{color}" style="color:{color}">{body}</svg>'


def chrome(html_path, png, w, h, dpr=1):
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--force-device-scale-factor={dpr}",
                    f"--window-size={w},{h}", "--virtual-time-budget=6000", f"--screenshot={png}", f"file://{html_path}"],
                   check=True, capture_output=True)


def sheet():
    out = HERE / "renders"
    out.mkdir(exist_ok=True)
    for i in MARKS:
        (HERE / f"{i}.svg").write_text(svg(i) + "\n", encoding="utf-8")
    rows = []
    for n, i in enumerate(MARKS):
        y = 16 + n * ROW
        rows.append(f'<div class=l style="top:{y + 8}px">{i} · {MARKS[i][0]}</div>'
                    f'<div class=c style="left:{X_LIGHT - 8}px;top:{y}px;background:#fff">{svg(i, 16, "#000")}</div>'
                    f'<div class=c style="left:{X_DARK - 8}px;top:{y}px;background:#000">{svg(i, 16, "#fff")}</div>'
                    f'<div class=b style="left:{X_BIG}px;top:{y - 16}px">{svg(i, 64, "#000")}</div>')
    h = 32 + len(MARKS) * ROW
    page = HERE / "renders" / "sheet.html"
    page.write_text("<!doctype html><meta charset=utf-8><style>body{margin:0;background:#eee;font:13px system-ui}"
                    ".l{position:absolute;left:12px;width:310px}.c{position:absolute;width:32px;height:32px}"
                    ".c svg{position:absolute;left:8px;top:8px}.b{position:absolute}</style>" + "".join(rows), encoding="utf-8")
    png = out / "sheet-16px.png"
    chrome(page, png, 520, h)
    crops = []
    for n, i in enumerate(MARKS):
        y = 16 + n * ROW + 8
        for tag, x in (("light", X_LIGHT), ("dark", X_DARK)):
            c = out / f"{i}-16px-{tag}.png"
            subprocess.run(["magick", str(png), "-crop", f"16x16+{x}+{y}", "+repage", str(c)], check=True)
            crops.append(c)
    # the enlargement: every 16 px crop shown x8 with image-rendering: pixelated (nearest-neighbour), labelled by id
    cells = "".join(f'<figure><img src="{c.name}"><figcaption>{c.stem.replace("-16px", "")}</figcaption></figure>' for c in crops)
    big = out / "sheet-16px-x8.html"
    big.write_text("<!doctype html><meta charset=utf-8><style>body{margin:8px;background:#bbb;font:13px system-ui;display:grid;"
                   "grid-template-columns:repeat(6,144px);gap:8px}figure{margin:0}img{width:128px;height:128px;image-rendering:pixelated;"
                   "display:block;border:1px solid #888}</style>" + cells, encoding="utf-8")
    chrome(big, out / "sheet-16px-x8.png", 6 * 152 + 16, ((len(crops) + 5) // 6) * 158 + 16)
    print(f"{len(MARKS)} marks · {png} · {out / 'sheet-16px-x8.png'}")


def header(site, i, font, lang="en", scheme="default", dpr="1"):
    """The built site's own start page, with candidate I and FONT injected — not a mockup.

    I = an icon id: the icon goes in the logo slot, the name stays plain. I = "C1": no separate icon (direction 3); the
    name itself carries the topmark on its l, in the header and in the page's H1."""
    site = pathlib.Path(site)
    page = site / ("de/index.html" if lang == "de" else "index.html")
    s = page.read_text(encoding="utf-8")
    start = s.index('class="md-header__button md-logo"')
    a0, a1 = s.index(">", start) + 1, s.index("</a>", start)
    s = s[:a0] + ("" if i == "C1" else svg(i)) + s[a1:]
    css = (f'<link href="https://fonts.googleapis.com/css2?family={font.replace(" ", "+")}:wght@600&display=block" rel="stylesheet">'
           f'<style>.md-header__ellipsis>.md-header__topic:first-child .md-ellipsis,.md-typeset h1{{font-family:"{font}",sans-serif;'
           'font-weight:600;letter-spacing:-.01em}.md-header__button.md-logo svg{height:1.4rem;width:1.4rem}'
           '.wl{position:relative;display:inline-block;line-height:1}.wl i,.wl b{position:absolute;left:50%;width:.2em;height:.2em;'
           'margin-left:-.1em;border-radius:50%;background:currentColor}.wl i{top:-.37em}.wl b{top:-.14em}'
           + ('.md-header__button.md-logo{display:none}.md-header__ellipsis,.md-header__topic,.md-header__topic .md-ellipsis{overflow:visible}' if i == "C1" else "") + '</style>')
    s = s.replace("</head>", css + "</head>", 1)
    if i == "C1":
        mark = 'shoa<span class="wl">l<i></i><b></b></span>mark'
        s = re.sub(r'(<div class="md-header__topic">\s*<span class="md-ellipsis">\s*)shoalmark', lambda m: m.group(1) + mark, s, count=1)
        s = s.replace('<h1 id="shoalmark">shoalmark<', f'<h1 id="shoalmark">{mark}<', 1)
    if scheme == "slate":   # main configures no palette, so the built page has no dark scheme; this previews Zensical's own
        pal = sorted((site / "assets/stylesheets/modern").glob("palette.*.min.css"))[0].relative_to(site)
        s = s.replace("</head>", f'<link rel="stylesheet" href="{"../" if lang == "de" else "./"}{pal}"></head>', 1)
    s = s.replace("</body>", f'<script>document.body.setAttribute("data-md-color-scheme","{scheme}")</script></body>', 1)
    out = page.with_name(f"_mark-{i}-{lang}-{scheme}.html")
    out.write_text(s, encoding="utf-8")
    png = HERE / "renders" / f"header-{i}-{font.split()[0].lower()}-{lang}-{scheme}{'' if dpr == '1' else '-dpr' + dpr}.png"
    chrome(out, png, 1440, 330, dpr)   # the logo slot shows from 1220 px up
    print(png.name)


if __name__ == "__main__":
    if sys.argv[1] == "sheet":
        sheet()
    elif sys.argv[1] == "type":
        chrome(HERE / "renders" / "type-sheet.html", HERE / "renders" / "type-sheet.png", 900, 420)
    else:
        header(*sys.argv[2:])
