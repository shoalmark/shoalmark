"""Export the seat icons to PNG — the standard library only (FM-024).

    python3 brand/seats/export.py            # every <seat>.svg here -> out/<seat>-20.png, -200.png, -400.png

Each icon is drawn on a 20-unit grid in whole-unit rectangles, so this script rasterises it itself: 20 px is one pixel a
unit, 200 and 400 px are exact multiples. Before it writes a file it checks the family's rule and refuses an icon that
breaks it (exit 1). An icon it cannot rasterise itself — an element other than <rect> and <path>, a curve, a transform —
needs a renderer outside the standard library: it prints the command and exits 2."""
import math, pathlib, re, struct, sys, zlib
import xml.etree.ElementTree as ET

HERE = pathlib.Path(__file__).resolve().parent
SIZES = (20, 200, 400)
GRID, SAFE = 20, 8          # the grid; the safe circle's radius — 10 % of the side inside the circle a crop cuts
GROUND, WATER, STAKE = "#15293d", "#34546c", "#bccd8f"
PALETTE = {GROUND, WATER, STAKE, "#d9e4ec", "#e8d4a0", "#8fb9f3", "#f38a80", "#7fd9bf", "#f1d47a", "#8595a2",
           "#5b83a3", "#07111b"}   # the site's night palette: overrides/landing.html and work-tracker/brand/theme.css
NS = "{http://www.w3.org/2000/svg}"


class External(Exception):
    pass


def cells(d):
    """The grid cells a path's outlines cover — each `M x y`, then whole-unit `h` and `v` steps, then `Z`."""
    if re.sub(r"[MhvZ\s\d-]", "", d):
        raise External(f"path data beyond M, h, v and Z: {d!r}")
    rings, ring, x, y, tokens = [], [], 0, 0, iter(re.findall(r"[MhvZ]|-?\d+", d))
    for t in tokens:
        if t == "M":
            x, y = int(next(tokens)), int(next(tokens))
            ring = [(x, y)]
        elif t in "hv":
            x, y = (x + int(next(tokens)), y) if t == "h" else (x, y + int(next(tokens)))
            ring.append((x, y))
        elif t == "Z":
            rings.append(ring)
        else:
            raise External(f"a bare number in {d!r}")
    inside = lambda px, py, r: sum((a[1] > py) != (b[1] > py) and px < a[0] for a, b in zip(r, r[1:] + r[:1])) % 2
    return {(cx, cy) for cx in range(GRID) for cy in range(GRID) if any(inside(cx + .5, cy + .5, r) for r in rings)}


def raster(svg):
    """The icon as a 20 x 20 grid of colours, painted in document order."""
    root = ET.parse(svg).getroot()
    if root.get("viewBox") != f"0 0 {GRID} {GRID}":
        raise ValueError(f"viewBox is {root.get('viewBox')!r}, not '0 0 {GRID} {GRID}'")
    grid = [[None] * GRID for _ in range(GRID)]
    for el in root:
        tag, fill = el.tag.replace(NS, ""), (el.get("fill") or "").lower()
        if tag == "title":
            continue
        if tag not in ("rect", "path") or set(el.attrib) - {"fill", "d", "width", "height"}:
            raise External(f"<{tag}> with {sorted(el.attrib)}")
        if fill not in PALETTE:
            raise ValueError(f"{fill or 'no fill'} is not in the palette")
        area = cells(el.get("d")) if tag == "path" else {(x, y) for x in range(int(el.get("width"))) for y in range(int(el.get("height")))}
        for x, y in area:
            grid[y][x] = fill
    return grid


def rule(svg, grid):
    """The family's rule, as refusals: ground to the edge, the stake in its place, nothing outside the safe circle but the
    stake's foot and the water below row 16, 40 lines at most."""
    out = [] if all(all(row) for row in grid) and grid[0][0] == GROUND else ["the ground does not fill the square"]
    if any(grid[y][x] != STAKE for x in (9, 10) for y in range(16, GRID)):
        out.append("the stake does not stand at x 9-10 to the bottom edge")
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            far = max(math.hypot(px - GRID / 2, py - GRID / 2) for px in (x, x + 1) for py in (y, y + 1))
            if c != GROUND and far > SAFE and not (y >= 16 and c in (STAKE, WATER)):
                out.append(f"cell {x},{y} ({c}) is outside the safe circle")
    if len(svg.read_text(encoding="utf-8").splitlines()) > 40:
        out.append("more than 40 lines")
    return out


def png(path, grid, k):
    rows = b"".join(b"\0" + bytes.fromhex("".join(c[1:] * k for c in row)) for row in grid for _ in range(k))
    chunk = lambda t, b: struct.pack(">I", len(b)) + t + b + struct.pack(">I", zlib.crc32(t + b))
    n = GRID * k
    path.write_bytes(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", n, n, 8, 2, 0, 0, 0))
                     + chunk(b"IDAT", zlib.compress(rows, 9)) + chunk(b"IEND", b""))


def main():
    out, bad = HERE / "out", 0
    out.mkdir(exist_ok=True)
    for svg in sorted(HERE.glob("*.svg")):
        try:
            grid = raster(svg)
        except External as e:
            print(f"{svg.name}: {e} — needs a renderer outside the standard library, e.g.\n"
                  f"  rsvg-convert -w 200 -h 200 -o {out / svg.stem}-200.png {svg}\n"
                  f"  \"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome\" --headless --window-size=200,200 "
                  f"--screenshot={out / svg.stem}-200.png {svg.as_uri()}", file=sys.stderr)
            return 2
        except ValueError as e:
            problems = [str(e)]
        else:
            problems = rule(svg, grid)
        if problems:
            bad += 1
            print(f"{svg.name}: refused — " + "; ".join(problems), file=sys.stderr)
            continue
        for size in SIZES:
            png(out / f"{svg.stem}-{size}.png", grid, size // GRID)
        print(f"{svg.name}: {', '.join(f'out/{svg.stem}-{s}.png' for s in SIZES)}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
