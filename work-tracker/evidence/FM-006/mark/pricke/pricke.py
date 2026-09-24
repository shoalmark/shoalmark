"""The Pricke drawn — every picture in the note comes from here; the geometry is constructed, not traced.

    python3 pricke.py sheet              # writes the SVGs; every variant at 16 px, one colour, light and dark, x8
    python3 pricke.py header SITE_DIR    # the built site's German start page, each variant in the logo slot, 1x and 2x,
                                         # light and dark, with the wordmark in IBM Plex Sans 600; then lockups.png
    python3 pricke.py pair SITE_DIR ID   # variant ID beside B1 (the GtM's isolated-danger beacon), same slot, same page
    python3 pricke.py site SITE_DIR      # the BUILT site as it is (logo, favicon, fonts, palette): site-header-*, the tab,
                                         # the fonts the browser used, and site-header-a-vs-d-2x.png for the Owner
    python3 pricke.py lockup SITE_DIR    # the header's lockup scaled whole (DPR 1, 2, 4) and d24 at 24 px: lockup-scale.png
    python3 pricke.py measure            # the facts the note states, read off the renders
    python3 pricke.py fonts              # proves IBM Plex Sans 600 loads in headless Chrome (header and pair check it first)

The model is the GtM seat's `marks.py` (FM-006, branch fm/006-gtm-mark-screen): headless Chrome at device-pixel-ratio 1
unless a file says 2x, enlargements nearest-neighbour (ImageMagick `-filter point`), so every pixel seen in them is a
pixel the browser drew. SITE_DIR is a built site from a scratch copy of the repository (`zensical build`), never `site/`.
"""
import math
import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).parent
OUT = HERE / "renders"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def n(v):
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def poly(*pts):
    """A closed polygon, always wound clockwise, so overlapping parts of one path never cancel under the nonzero rule."""
    if sum(x0 * y1 - x1 * y0 for (x0, y0), (x1, y1) in zip(pts, pts[1:] + pts[:1])) < 0:
        pts = pts[::-1]
    return "M" + "L".join(f"{n(x)} {n(y)}" for x, y in pts) + "Z"


def rect(x, y, w, h):
    return poly((x, y), (x + w, y), (x + w, y + h), (x, y + h))


def ray(fx, fy, deg, r1, w0, w1, down=False):
    """One twig: a tapered quadrilateral from the focus (fx, fy), at `deg` from the vertical, r1 long, w0 wide → w1."""
    a = math.radians(deg)
    dx, dy = math.sin(a), (math.cos(a) if down else -math.cos(a))
    nx, ny = -dy, dx
    p = lambda r, w, s: (fx + dx * r + s * nx * w / 2, fy + dy * r + s * ny * w / 2)
    return poly(p(0, w0, 1), p(r1, w1, 1), p(r1, w1, -1), p(0, w0, -1))


def pix(*rows):
    """Pixel-exact geometry on the grid: one string per row, '#' on; each horizontal run becomes one rectangle."""
    out = []
    for y, row in enumerate(rows):
        x = 0
        while x < len(row):
            if row[x] == "#":
                e = x
                while e < len(row) and row[e] == "#":
                    e += 1
                out.append(f"M{x} {y}h{e - x}v1h{x - e}Z")
                x = e
            else:
                x += 1
    return "".join(out)


def fan(k, spread, fx, fy, r1, w0, w1, down=False):
    """k twigs of one length, spread evenly over ±spread degrees from the focus: their tips lie on one arc."""
    return "".join(ray(fx, fy, -spread + 2 * spread * i / (k - 1), r1, w0, w1, down) for i in range(k))


def wave(cx, cy, half, amp, th, periods, steps=24):
    """A short water line: a cosine band, symmetric about the stake at cx, crest under the stake, thickness th."""
    xs = [cx - half + 2 * half * i / steps for i in range(steps + 1)]
    ys = [cy - amp * math.cos(math.pi * periods * (x - cx) / half) for x in xs]
    return poly(*([(x, y - th / 2) for x, y in zip(xs, ys)] + [(x, y + th / 2) for x, y in zip(xs, ys)][::-1]))


# id: (the chart meaning, one line; grid; body; px in the header's logo slot). One colour: everything is currentColor.
# The header grid is 28 units, so at the slot's 28 px one unit is one pixel; the 16 px cut is 16 units, a pixel each.
STAKE = rect(13, 15, 2, 12)                            # 2 units wide: the wordmark's stem at 18 px is about 2 px
CROWN = fan(7, 36, 14, 15, 14, 2.0, 0.3)               # 7 twigs over ±36°, lashed at the stake's head, tapered to points
MARKS = {
    "a": ("Besen nach oben — the port-hand Pricke (Backbord, the red side): twigs lashed at their lower end, splayed "
          "upward (the blunt form); the one most used", 28, STAKE + CROWN, 28),
    "b": ("Besen nach unten — the starboard-hand Pricke (Steuerbord, the green side): twigs lashed at the top, bent "
          "apart below (the pointed form)", 28, rect(13, 1, 2, 26) + fan(7, 36, 14, 2, 13.5, 2.0, 0.3, down=True), 28),
    "c": ("(a) where it stands: a short water line under the stake — a picture of the mark, not a chart symbol", 28,
          rect(13, 14, 2, 10.5) + fan(7, 36, 14, 14, 13, 2.0, 0.3) + wave(14, 25.5, 7, 0.9, 1.5, 3), 28),
    "d": ("the 16 px cut of (a): the fan in four strokes (two at 45°, two at 1:2) on a 16-unit grid, the stake 2 px — "
          "for the browser tab", 16, pix(
              "....#......#....",
              "#...#......#...#",
              ".#...#....#...#.",
              "..#..#....#..#..",
              "...#..#..#..#...",
              "....#.#..#.#....",
              ".....#.##.#.....",
              "......####......",
              *[".......##......."] * 8), 32),   # in the header at 32 px, twice its grid, so every pixel stays square
}


# d24: `d` redrawn on a 24-unit grid for a 24 px header slot (the Owner: "we could try a 24 px variant") — the same four
# strokes and neck, the fan finer against its size, the stake still 2 px. Not in the sheet; `lockup` writes its SVG.
D24 = (24, pix(
    "......#..........#......",
    "......#..........#......",
    ".#.....#........#.....#.",
    "..#....#........#....#..",
    "...#....#......#....#...",
    "....#...#......#...#....",
    ".....#...#....#...#.....",
    "......#..#....#..#......",
    ".......#..#..#..#.......",
    "........#.#..#.#........",
    ".........#.##.#.........",
    "..........####..........",
    *["...........##..........."] * 12))


# B1 is the GtM seat's source, copied verbatim from fm/006-gtm-mark-screen (mark/marks.py), for the side-by-side only.
B1 = (16, '<circle cx="8" cy="2" r="2"/><circle cx="8" cy="7" r="2"/><rect x="7" y="8" width="2" height="8"/>')


def svg(i, size=None, color="currentColor"):
    grid, body = {"B1": B1, "d24": D24}.get(i) or MARKS[i][1:3]
    wh = f' width="{size}" height="{size}"' if size else ""
    inner = body if body.startswith("<") else f'<path d="{body}"/>'
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {grid} {grid}"{wh} fill="{color}">{inner}</svg>'


def chrome(html_path, png, w, h, dpr=1, dump=False, dark=None):
    """dark=True/False makes the browser prefer that scheme (Blink: 0 dark, 1 light), so a site with a palette picks it
    itself, as it does for a reader whose system is set so; None leaves the browser's default."""
    args = [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--force-device-scale-factor={dpr}",
            f"--window-size={w},{h}", "--virtual-time-budget=8000"]
    if dark is not None:
        args.append(f"--blink-settings=preferredColorScheme={0 if dark else 1}")
    if dump:
        return subprocess.run(args + ["--dump-dom", f"file://{html_path}"], check=True, capture_output=True, text=True).stdout
    subprocess.run(args + [f"--screenshot={png}", f"file://{html_path}"], check=True, capture_output=True)


def magick(*a):
    subprocess.run(["magick", *map(str, a)], check=True)


FONT = ('<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@600&display=block" rel="stylesheet">'
        '<style>.md-header__ellipsis>.md-header__topic:first-child .md-ellipsis,.md-typeset h1{font-family:"IBM Plex Sans",'
        'sans-serif;font-weight:600;letter-spacing:-.01em}</style>')


def fonts():
    """IBM Plex Sans 600 must be the face the header renders use, not a fallback: the browser says which it has."""
    page = OUT / "_fonts.html"
    page.write_text("<!doctype html><meta charset=utf-8>" + FONT + '<p id=r>?</p><script>document.fonts.load('
                    '\'600 18px "IBM Plex Sans"\').then(f=>{document.getElementById("r").textContent='
                    '"loaded:"+f.length+" check:"+document.fonts.check(\'600 18px "IBM Plex Sans"\')})</script>', encoding="utf-8")
    dom = chrome(page, None, 400, 200, dump=True)
    page.unlink()
    got = dom.split('<p id="r">')[1].split("<")[0]
    print("IBM Plex Sans 600 —", got)
    return got.startswith("loaded:1") and got.endswith("true")


def header_page(site, i, scheme):
    """The built site's German start page (the GtM's B1 renders use the same), candidate I in the logo slot."""
    site = pathlib.Path(site)
    page = site / "de/index.html"
    s = page.read_text(encoding="utf-8")
    start = s.index('class="md-header__button md-logo"')
    a0, a1 = s.index(">", start) + 1, s.index("</a>", start)
    px = 28 if i == "B1" else MARKS[i][3]   # B1 at the GtM's 1.4rem; each variant at the height its grid is drawn for
    s = s[:a0] + svg(i) + s[a1:]
    s = s.replace("</head>", FONT + f"<style>.md-header__button.md-logo svg{{height:{px}px;width:{px}px}}</style></head>", 1)
    if scheme == "slate":   # main configures no palette, so the built page has no dark scheme; this previews Zensical's own
        pal = sorted((site / "assets/stylesheets/modern").glob("palette.*.min.css"))[0].relative_to(site)
        s = s.replace("</head>", f'<link rel="stylesheet" href="../{pal}"></head>', 1)
    s = s.replace("</body>", f'<script>document.body.setAttribute("data-md-color-scheme","{scheme}")</script></body>', 1)
    out = page.with_name(f"_pricke-{i}-{scheme}.html")
    out.write_text(s, encoding="utf-8")
    return out


def board(cells, cols, name, bg="#c8c8c8"):
    """A labelled board of images, screenshotted at DPR 1: each image is shown at its own pixel size, so an
    enlargement made with -filter point stays nearest-neighbour. cells: (image path, caption)."""
    figs = "".join(f'<figure><img src="{pathlib.Path(p).name}"><figcaption>{c}</figcaption></figure>' for p, c in cells)
    page = OUT / f"_{name}.html"
    page.write_text(f"<!doctype html><meta charset=utf-8><style>body{{margin:12px;background:{bg};font:13px/1.3 system-ui;"
                    f"display:grid;grid-template-columns:repeat({cols},max-content);gap:12px 14px;align-items:end}}"
                    "figure{margin:0}img{display:block;image-rendering:pixelated}figcaption{margin-top:4px;color:#222}"
                    "</style>" + figs, encoding="utf-8")
    png = OUT / f"{name}.png"
    chrome(page, png, 2400, 1600)
    magick(png, "-trim", "+repage", "-bordercolor", bg, "-border", "12", png)
    page.unlink()
    print(png.name)


def sheet():
    """Every variant (and B1, for reference) at exactly 16 px, one colour, black on white and white on black; the
    16 px crops enlarged x8. The true-size page is kept too, with each variant at its header size beside."""
    ids = list(MARKS) + ["B1"]
    for i in MARKS:
        (HERE / f"{i}.svg").write_text(svg(i) + "\n", encoding="utf-8")
    ROW, XL, XD = 64, 300, 340
    rows = []
    for k, i in enumerate(ids):
        y = 16 + k * ROW
        label = f"B1 · the GtM seat's isolated-danger beacon (reference)" if i == "B1" else f"{i} · {MARKS[i][0].split(' — ')[0]}"
        big = 28 if i == "B1" else MARKS[i][3]
        rows.append(f'<div class=l style="top:{y + 8}px">{label}</div>'
                    f'<div class=c style="left:{XL - 8}px;top:{y}px;background:#fff">{svg(i, 16, "#000")}</div>'
                    f'<div class=c style="left:{XD - 8}px;top:{y}px;background:#000">{svg(i, 16, "#fff")}</div>'
                    f'<div class=b style="left:390px;top:{y - 6}px;background:#fff">{svg(i, big, "#000")}</div>'
                    f'<div class=b style="left:440px;top:{y - 6}px;background:#000">{svg(i, big, "#fff")}</div>')
    page = OUT / "_sheet.html"
    page.write_text("<!doctype html><meta charset=utf-8><style>body{margin:0;background:#eee;font:13px system-ui}"
                    ".l{position:absolute;left:12px;width:270px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}"
                    ".c{position:absolute;width:32px;height:32px}.c svg{position:absolute;left:8px;top:8px}"
                    ".b{position:absolute;padding:4px}.b svg{display:block}</style>" + "".join(rows), encoding="utf-8")
    raw = OUT / "sheet-16px.png"
    chrome(page, raw, 500, 32 + len(ids) * ROW)
    page.unlink()
    cells = []
    for k, i in enumerate(ids):
        y = 16 + k * ROW + 8
        for tag, x in (("light", XL), ("dark", XD)):
            c = OUT / f"{i}-16px-{tag}.png"
            magick(raw, "-crop", f"16x16+{x}+{y}", "+repage", c)
            x8 = OUT / f"_x8-{i}-{tag}.png"
            magick(c, "-filter", "point", "-resize", "800%", x8)
            cells.append((x8, f"{i} · {tag} · 16 px ×8"))
    board(cells, 4, "sheet-16px-x8")
    for p in OUT.glob("_x8-*.png"):
        p.unlink()


LOCK = (110, 0, 220, 48)   # x, y, w, h at 1x: the logo slot and the wordmark, nothing else


def header(site, ids):
    for i in ids:
        for scheme, tag in (("default", "light"), ("slate", "dark")):
            page = header_page(site, i, scheme)
            for dpr in (1, 2):
                chrome(page, OUT / f"header-{i}-{tag}-{dpr}x.png", 1440, 330, dpr)
            page.unlink()
        print("header", i)


def crop(i, tag, dpr, k):
    """The lockup cut out of a header render: at 1x enlarged k times nearest-neighbour, at 2x likewise."""
    x, y, w, h = LOCK
    c = OUT / f"_lk-{i}-{tag}-{dpr}.png"
    magick(OUT / f"header-{i}-{tag}-{dpr}x.png", "-crop", f"{w * dpr}x{h * dpr}+{x * dpr}+{y * dpr}", "+repage",
           "-filter", "point", "-resize", f"{k * 100}%", c)
    return c


def lockups(ids):
    """Every variant's lockup, one row each: light 1x (x2), light 2x, dark 1x (x2), dark 2x — all at the same scale."""
    cells = []
    for i in ids:
        for tag in ("light", "dark"):
            cells += [(crop(i, tag, 1, 2), f"{i} · {tag} · 1x, shown ×2"), (crop(i, tag, 2, 1), f"{i} · {tag} · 2x")]
    board(cells, 4, "lockups")
    for p in OUT.glob("_lk-*.png"):
        p.unlink()


def pair(site, i):
    """Variant I beside B1, the same page, the same slot: B1 at the GtM's 1.4rem, the variant at its own height."""
    header(site, ["B1"])
    cells = []
    for tag in ("light", "dark"):
        for dpr, k in ((1, 2), (2, 1)):
            for j in ("B1", i):
                cells.append((crop(j, tag, dpr, k), f"{j} · {tag} · {dpr}x{', shown ×2' if dpr == 1 else ''}"))
    board(cells, 2, f"pair-B1-{i}")
    for p in OUT.glob("_lk-*.png"):
        p.unlink()
    for p in OUT.glob("header-B1-*.png"):   # the GtM's own B1 headers are on its branch; only the pair is kept here
        p.unlink()


def grey(png, x, y, w, h):
    """The rectangle's pixels as rows of 0–255 grey values (0 = full ink on the light ground), read by ImageMagick."""
    txt = subprocess.run(["magick", str(png), "-crop", f"{w}x{h}+{x}+{y}", "+repage", "-colorspace", "gray", "-depth", "8",
                          "txt:-"], check=True, capture_output=True, text=True).stdout.splitlines()[1:]
    g = [[255] * w for _ in range(h)]
    for line in txt:
        xy, rest = line.split(":", 1)
        cx, cy = map(int, xy.split(","))
        g[cy][cx] = int(rest.split("(")[1].split(")")[0].split(",")[0].split(".")[0].rstrip("%"))
    return g


def runs(row, dark=False, cut=128):
    """How many separate strokes a scanline crosses: runs of ink below (or, on the dark ground, above) the cut."""
    ink = [(v > cut) if dark else (v < cut) for v in row]
    return sum(1 for k, on in enumerate(ink) if on and (k == 0 or not ink[k - 1]))


def measure_site():
    """The built site's header: the mark's pixels and the wordmark's stems, read off site-header-*.png."""
    for tag in ("light", "dark"):
        for dpr in (1, 2):
            g = grey(OUT / f"site-header-{tag}-{dpr}x.png", 120 * dpr, 4 * dpr, 30 * dpr, 40 * dpr)   # the logo slot
            ink = (lambda v: v < 128) if tag == "light" else (lambda v: v > 128)
            rows = [r for r in range(len(g)) if any(ink(v) for v in g[r])]
            cols = [c for c in range(len(g[0])) if any(ink(g[r][c]) for r in rows)]
            box = [g[r][c] for r in range(rows[0], rows[-1] + 1) for c in range(cols[0], cols[-1] + 1)]
            levels = sorted(set(box))
            stake = [v for v in g[rows[-1]] if ink(v)]
            w = grey(OUT / f"site-header-{tag}-{dpr}x.png", 160 * dpr, 12 * dpr, 120 * dpr, 24 * dpr)   # the wordmark
            wr = [r for r in range(len(w)) if any(ink(v) for v in w[r])]
            full = [c for c in range(len(w[0])) if sum(ink(w[r][c]) for r in wr) >= 0.85 * len(wr)]
            runs = []
            for c in full:
                runs.append([c]) if not runs or c != runs[-1][-1] + 1 else runs[-1].append(c)
            print(f"  site {tag} {dpr}x: the mark {cols[-1] - cols[0] + 1}×{rows[-1] - rows[0] + 1} device px, "
                  f"{len(levels)} grey levels in its box {levels}; stake {len(stake)} px; the wordmark's full-height "
                  f"stems {[len(r) for r in runs]} px at 50 % ink")


def measure():
    """The facts the note states, read off the committed renders — nothing here is judged by eye."""
    print("16 px, light ground (0 = ink, 255 = paper):")
    for i in list(MARKS) + ["B1"]:
        g = grey(OUT / f"{i}-16px-light.png", 0, 0, 16, 16)
        flat = [v for r in g for v in r]
        part = sum(1 for v in flat if 25 < v < 230)
        stake = [v for v in g[13] if v < 230]
        twigs = max(runs(g[r]) for r in range(0, 8))
        print(f"  {i}: {len(set(flat))} grey levels, {part} part-inked pixels; stake at row 13 = {stake}; "
              f"most strokes on one fan row = {twigs}")
    x0, y0, w, h = 128, 10, 36, 36   # the logo slot at 1x (the slot's svg starts at x 130, y 12)
    for i in MARKS:
        for dpr in (1, 2):
            g = grey(OUT / f"header-{i}-light-{dpr}x.png", x0 * dpr, y0 * dpr, w * dpr, h * dpr)
            rows = [r for r in range(h * dpr) if min(g[r]) < 128]
            cols = [c for c in range(w * dpr) if min(g[r][c] for r in range(h * dpr)) < 128]
            top, bot = rows[0] + y0 * dpr, rows[-1] + y0 * dpr
            mid = (rows[0] + rows[-1]) // 2
            stake_row = next(r for r in range(rows[-1], 0, -1) if runs(g[r]) == 1 and r < rows[-1] - 3 * dpr)
            stake = [v for v in g[stake_row] if v < 230]
            fanrows = rows[: int(len(rows) * 0.55)]   # the crown: the upper part of the figure, never the water line
            best = max((runs(g[r]), r) for r in fanrows)
            print(f"  header {i} {dpr}x light: ink rows {top}–{bot} (device px), {len(cols)} px wide; stake {stake}; "
                  f"most separate strokes on one crown row = {best[0]} (row {best[1] + y0 * dpr})")
    g = grey(OUT / "header-a-light-1x.png", 170, 0, 150, 48)
    t = [r for r in range(48) if min(g[r]) < 128]
    print(f"  the wordmark at 1x, light: ink rows {t[0]}–{t[-1]} (ascender top to baseline)")
    for i in list(MARKS):
        s = grey(OUT / f"header-{i}-dark-1x.png", 130, 12, 32, 32)
        w = grey(OUT / f"header-{i}-dark-1x.png", 170, 16, 160, 18)
        print(f"  dark header {i}: the mark's brightest grey {max(v for r in s for v in r)}, the wordmark's "
              f"{max(v for r in w for v in r)} (255 = white)")


def site(site_dir):
    """The built site itself — `zensical build` from the branch, its own logo, favicon, fonts and palette — rendered
    unmodified: the browser prefers light or dark, and the theme picks its scheme from that, as for a reader."""
    page = pathlib.Path(site_dir).resolve() / "de/index.html"
    for tag in ("light", "dark"):
        for dpr in (1, 2):
            chrome(page, OUT / f"site-header-{tag}-{dpr}x.png", 1440, 330, dpr, dark=tag == "dark")
    print("site-header-{light,dark}-{1x,2x}.png")
    # what the browser says it used — read on a scratch copy with one script added, never on the rendered page
    probe = page.with_name("_probe.html")
    probe.write_text(page.read_text(encoding="utf-8").replace("</body>", """<script>document.fonts.ready.then(()=>{
      const w=document.querySelector('.md-header__ellipsis>.md-header__topic:first-child .md-ellipsis'),b=document.querySelector('.md-typeset p'),
      c=getComputedStyle(w),i=document.querySelector('link[rel=icon]');
      document.body.insertAdjacentHTML('beforeend','<pre id=probe>wordmark: '+c.fontFamily+' '+c.fontWeight+' '+c.fontSize+
      ' | loaded: '+document.fonts.check('500 18px "IBM Plex Mono"')+' | body: '+getComputedStyle(b).fontFamily+' loaded: '+
      document.fonts.check('400 16px "IBM Plex Sans"')+' | icon: '+i.getAttribute('href')+'</pre>')})</script></body>""", 1),
                     encoding="utf-8")
    dom = chrome(probe, None, 1440, 330, dump=True)
    probe.unlink()
    print(dom.split('<pre id="probe">')[1].split("</pre>")[0].replace("&quot;", '"'))
    # the tab: the icon the built page links, read back from its <link rel="icon">, drawn at 16 px as a tab draws it
    href = page.read_text(encoding="utf-8").split('<link rel="icon" href="')[1].split('"')[0]
    icon = (page.parent / href).resolve()
    cells = []
    for tag, bg in (("light", "#ffffff"), ("dark", "#35363a")):
        tab = OUT / "_tab.html"
        tab.write_text(f'<!doctype html><body style="margin:0;background:{bg}"><img src="{icon.as_uri()}" width=16 height=16 '
                       'style="position:absolute;left:8px;top:8px">', encoding="utf-8")
        png = OUT / f"_tab-{tag}.png"
        chrome(tab, png, 64, 64, 1, dark=tag == "dark")
        magick(png, "-crop", "16x16+8+8", "+repage", "-filter", "point", "-resize", "800%", png)
        cells.append((png, f"the tab icon ({href}) · {tag} tab · 16 px ×8"))
        tab.unlink()
    board(cells, 2, "site-tab-16px-x8")
    for p_ in OUT.glob("_tab-*.png"):
        p_.unlink()


def swapped(site_dir, what):
    """A scratch copy of the built German start page with one thing changed for the comparison, beside the original:
    `a` puts the drawn Pricke in the logo slot at its 28 px; `d32` shows the site's own mark at twice its size."""
    page = pathlib.Path(site_dir).resolve() / "de/index.html"
    s = page.read_text(encoding="utf-8")
    start = s.index('class="md-header__button md-logo"')
    a0, a1 = s.index(">", start) + 1, s.index("</a>", start)
    px = 28 if what == "a" else 32
    if what == "a":
        s = s[:a0] + svg("a") + s[a1:]
    s = s.replace("</head>", f"<style>.md-header__button.md-logo svg{{width:{px}px;height:{px}px}}</style></head>", 1)
    out = page.with_name(f"_compare-{what}.html")
    out.write_text(s, encoding="utf-8")
    return out


def compare(site_dir):
    """The Owner's comparison at 2x: `a` as drawn for the header, the site's `d` at 16 px (the stems' weight), and `d` at
    32 px (twice that) — light and dark, each cut from the site's own header, nothing else changed."""
    x, y, w, h = 110, 0, 240, 48
    cells, tmp = [], []
    for tag in ("light", "dark"):
        for what, label in (("a", "a · 28 px, as drawn for the header"), ("d", "d · 16 px — the site"),
                            ("d32", "d · 32 px, twice its grid")):
            page = pathlib.Path(site_dir).resolve() / "de/index.html" if what == "d" else swapped(site_dir, what)
            png = OUT / f"_cmp-{what}-{tag}.png"
            chrome(page, png, 1440, 330, 2, dark=tag == "dark")
            magick(png, "-crop", f"{w * 2}x{h * 2}+{x * 2}+{y * 2}", "+repage", png)
            cells.append((png, f"{label} · {tag} · 2x"))
            tmp.append(png)
            if what != "d":
                page.unlink()
    board(cells, 3, "site-header-a-vs-d-2x")
    for p in tmp:
        p.unlink()


def stems(g, ink):
    """Full-height vertical strokes in a crop: runs of columns inked over 85 % of the inked rows, their widths."""
    rows = [r for r in range(len(g)) if any(ink(v) for v in g[r])]
    full = [c for c in range(len(g[0])) if sum(ink(g[r][c]) for r in rows) >= 0.85 * len(rows)]
    runs = []
    for c in full:
        runs.append([c]) if not runs or c != runs[-1][-1] + 1 else runs[-1].append(c)
    return [len(r) for r in runs]


def lockup(site_dir):
    """The header's lockup — `d` and the wordmark in IBM Plex Mono 500, the theme's own gap — scaled as a whole: the
    unmodified built page at device-pixel ratio 1, 2 and 4, so the mark is 16, 32 and 64 device px and the name 18, 36
    and 72, drawn by the browser at that size (nothing is enlarged after the fact). Then `d24` in the same slot at 24 px,
    at 1x and 2x, on a scratch copy of the page. Prints stake width against the name's stems for each."""
    (HERE / "d24.svg").write_text(svg("d24") + "\n", encoding="utf-8")
    page = pathlib.Path(site_dir).resolve() / "de/index.html"
    s = page.read_text(encoding="utf-8")
    start = s.index('class="md-header__button md-logo"')
    a0, a1 = s.index(">", start) + 1, s.index("</a>", start)
    alt = page.with_name("_d24.html")
    alt.write_text((s[:a0] + svg("d24").replace('fill="currentColor"', 'fill="currentColor" shape-rendering="crispEdges"') + s[a1:])
                   .replace("</head>", "<style>.md-header__button.md-logo svg{width:24px;height:24px}</style></head>", 1),
                   encoding="utf-8")
    x, y, w, h = 120, 0, 190, 48
    cells, tmp = [], []
    print("| lockup | scale | mark (device px) | stake | the name's stems | grey levels in the mark |")
    print("|---|---|---|---|---|---|")
    for mark, src, scales in (("d", page, (1, 2, 4)), ("d24", alt, (1, 2))):
        for k in scales:
            for tag in ("light", "dark"):
                png = OUT / f"_lk-{mark}-{k}-{tag}.png"
                chrome(src, png, 1440, 330, k, dark=tag == "dark")
                magick(png, "-crop", f"{w * k}x{h * k}+{x * k}+{y * k}", "+repage", png)
                tmp.append(png)
                size = 16 if mark == "d" else 24
                cells.append((png, f"{mark} · ×{k} · mark {size * k} px, name {18 * k} px · {tag}"))
                g = grey(png, 0, 0, w * k, h * k)
                ink = (lambda v: v < 128) if tag == "light" else (lambda v: v > 128)
                m = [row[: (size + 14) * k] for row in g]              # the mark's columns: the slot, not the name
                mr = [r for r in range(len(m)) if any(ink(v) for v in m[r])]
                mc = [c for c in range(len(m[0])) if any(ink(m[r][c]) for r in mr)]
                box = {m[r][c] for r in range(mr[0], mr[-1] + 1) for c in range(mc[0], mc[-1] + 1)}
                stake = sum(1 for v in m[mr[-1]] if ink(v))
                name = stems([row[(size + 16) * k:] for row in g], ink)
                if tag == "light":
                    print(f"| {mark} | ×{k} | {mc[-1] - mc[0] + 1} × {mr[-1] - mr[0] + 1} | {stake} px | {name} px | {len(box)} |")
    alt.unlink()
    board(cells, 2, "lockup-scale")
    for p_ in tmp:
        p_.unlink()


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "sheet":
        sheet()
    elif cmd == "site":
        site(sys.argv[2])
        compare(sys.argv[2])
    elif cmd == "lockup":
        lockup(sys.argv[2])
    elif cmd == "measure":
        measure()
        measure_site()
    elif cmd == "fonts":
        sys.exit(0 if fonts() else 1)
    elif cmd in ("header", "pair"):
        if not fonts():
            sys.exit("IBM Plex Sans did not load — no header render is made on a fallback face")
        if cmd == "header":
            header(sys.argv[2], list(MARKS))
            lockups(list(MARKS))
        else:
            pair(sys.argv[2], sys.argv[3])
