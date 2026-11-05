"""Builds shoalmark-software-factory-x.svg (1600 x 900): the loop a repository under shoalmark runs, as four stations on a
game screen — COURSE (TRIAGE.md, the Owner's), CREW (four seat icons, each with its word), BOARD (asks, oldest first),
STAND-UP (the Owner answers one at a time). Parts, byte for byte: the seat icons (shoalmark brand/seats/*.svg, whole);
the repository card's wordmark lockup and embedded Plex Mono 600, its face renamed to a family only the embed defines,
so the render itself proves the embed. No logo but shoalmark's own."""
import re, os
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')   # the repository
SEATS = os.path.join(ROOT, 'brand', 'seats', '')
card = open(os.path.join(ROOT, 'brand', 'social', 'repository-card.svg')).read()
FAM = 'Shoalmark Plex Mono Embed'
style = re.search(r'<style>.*?</style>', card, re.S).group(0).replace('font-family:"IBM Plex Mono"', f'font-family:"{FAM}"')
assert FAM in style
if os.environ.get('NOEMBED'): style = '<style></style>'
groups = re.findall(r'<g transform="translate\(([\d.]+) ([\d.]+)\) scale\(3.84615\)">(.*?)</g>', card, re.S)
assert len(groups) == 3
def seat(name):                       # the icon whole: its ground, water, stake and face
    s = open(SEATS + name + '.svg').read()
    return ''.join(re.findall(r'<(?:rect|path) [^>]*/>', s))

W, H, U = 1600, 900, 5
def px(cells, fill, u=U):
    return f'<path fill="{fill}" d="' + ''.join(f'M{x*u} {y*u}h{w*u}v{h*u}h{-w*u}Z' for x, y, w, h in cells) + '"/>'
out, words = [], []
A = out.append
def T(x, y, s, fill, txt, anchor='start'):
    words.append(f'<text x="{x}" y="{y}" font-family="{FAM}" font-weight="600" font-size="{s}" fill="{fill}" text-anchor="{anchor}">{txt}</text>')

AG, OW, DOM, INK, MUTE = '#bccd8f', '#e8d4a0', '#b8c98c', '#d9e4ec', '#8595a2'
A(f'<rect width="{W}" height="{H}" fill="#07111b"/>')
A(px([(5, 5, 310, 2), (5, 171, 310, 2), (5, 7, 2, 164), (313, 7, 2, 164)], '#34546c'))
A(px([(9, 9, 2, 2), (309, 9, 2, 2), (9, 167, 2, 2), (309, 167, 2, 2)], '#5b83a3'))

# --- the four stations: panels 300 x 360 at y 264
PY, PH, PW = 264, 360, 300
PX = [112, 470, 828, 1188]
def panel(x, edge):
    A(f'<rect x="{x}" y="{PY}" width="{PW}" height="{PH}" fill="#0d1d2c"/>')
    A(f'<path fill="{edge}" d="M{x} {PY}h{PW}v5h-{PW}ZM{x} {PY+PH-5}h{PW}v5h-{PW}ZM{x} {PY}h5v{PH}h-5ZM{x+PW-5} {PY}h5v{PH}h-5Z"/>')
    A(f'<path fill="#07111b" d="M{x} {PY}h5v5h-5ZM{x+PW-5} {PY}h5v5h-5ZM{x} {PY+PH-5}h5v5h-5ZM{x+PW-5} {PY+PH-5}h5v5h-5Z"/>')   # pixel corners
for x, e in zip(PX, ('#5b83a3', '#34546c', '#34546c', '#5b83a3')): panel(x, e)
for i, (x, t, c) in enumerate(zip(PX, ('COURSE', 'CREW', 'BOARD', 'STAND-UP'), (OW, AG, AG, OW))):
    T(x + PW // 2, PY + 46, 30, c, t, 'middle')

# arrows between stations: pixel chevrons
def chev(cx, cy, col, d=1):
    A(px([(cx // U + (k if d > 0 else -k), cy // U - 3 + k, 1, 7 - 2 * k) for k in range(4)], col))
for x in PX[:-1]:
    cx = x + PW + 22
    A(px([(cx // U - 2, (PY + 170) // U, 3, 1)], AG)); chev(cx + 5, PY + 170, AG)

# 1 COURSE: the Owner's sheet, TRIAGE.md, a heading drawn on it
cx = PX[0]
A(px([(cx // U + 9, 340 // U, 42, 42)], '#e8d4a0'))                      # the sheet
A(px([(cx // U + 9, 340 // U, 42, 6)], '#c9b47e'))                       # its head band
A(px([(cx // U + 13, 372 // U + 3, 22, 1), (cx // U + 13, 372 // U + 7, 30, 1)], '#8a7a52'))   # the intent, as lines
A(px([(cx // U + 13, 372 // U + 13, 4, 2), (cx // U + 17, 372 // U + 16, 5, 2), (cx // U + 22, 372 // U + 19, 6, 2), (cx // U + 28, 372 // U + 22, 6, 2), (cx // U + 34, 372 // U + 25, 4, 2)], '#34546c'))   # the current path, a course line
A(px([(cx // U + 38, 372 // U + 24, 2, 4), (cx // U + 40, 372 // U + 25, 1, 2)], '#34546c'))
T(cx + PW // 2, 334 + 22, 20, '#07111b', 'TRIAGE.md', 'middle')
T(cx + PW // 2, 596, 20, OW, 'the Owner’s', 'middle')

# 2 CREW: four seat icons, whole, at 3x, each with its word below
cx = PX[1]
for i, name in enumerate(('planner', 'builder', 'reviewer', 'auditor')):
    gx, gy = cx + 35 + (i % 2) * 150, 318 + (i // 2) * 146
    A(f'<g transform="translate({gx} {gy}) scale(4)" shape-rendering="crispEdges">{seat(name)}</g>')
    T(gx + 40, gy + 108, 20, AG, name, 'middle')

# 3 BOARD: asks waiting, oldest on top
cx = PX[2]
for i in range(4):
    y = 322 + i * 54
    col = '#34546c' if i else '#5b83a3'
    A(f'<rect x="{cx + 30}" y="{y}" width="240" height="40" fill="{col}"/>')
    A(f'<rect x="{cx + 30}" y="{y}" width="6" height="40" fill="{OW if i == 0 else "#15293d"}"/>')
    T(cx + 48, y + 27, 18 if i else 20, INK if i == 0 else MUTE, 'waiting for you' if i == 0 else 'waiting…')
T(cx + PW // 2, 560, 20, AG, '↑ oldest first', 'middle')
T(cx + PW // 2, 596, 20, AG, 'next: owner', 'middle')

# 4 STAND-UP: one item, the Owner's command, their commit
cx = PX[3]
A(f'<rect x="{cx + 30}" y="322" width="240" height="40" fill="#5b83a3"/>')
A(f'<rect x="{cx + 30}" y="322" width="6" height="40" fill="{OW}"/>')
T(cx + 48, 349, 20, INK, 'ask:'); A(px([((cx + 112) // U, (322 + 17) // U, 22, 1)], INK))
A(px([((cx + 150) // U, 368 // U, 1, 4)] + [((cx + 150) // U - 2 + k, 388 // U + k, 5 - 2 * k, 1) for k in range(3)], OW))
T(cx + PW // 2, 424, 20, OW, 'you answer,', 'middle')
T(cx + PW // 2, 452, 20, OW, 'one at a time', 'middle')
# a commit: a node on a line
A(px([((cx + 40) // U, 495 // U, 44, 1)], '#5b83a3'))
A(px([((cx + 145) // U, 485 // U, 2, 1), ((cx + 140) // U, 490 // U, 4, 3), ((cx + 145) // U, 505 // U, 2, 1), ((cx + 140) // U + 0, 490 // U, 1, 3)], OW))
A(px([((cx + 145) // U, 490 // U, 2, 3)], '#07111b'))
T(cx + PW // 2, 540, 20, OW, 'your commit', 'middle')
T(cx + PW // 2, 568, 18, MUTE, 'signed if configured', 'middle')
T(cx + PW // 2, 596, 20, OW, 'you run it', 'middle')

# the answer goes back to the crew: a route under the stations, STAND-UP to CREW
RY = 664
A(px([((PX[3] + 150) // U, (PY + PH) // U, 1, (RY - PY - PH) // U), ((PX[1] + 150) // U, RY // U, (PX[3] - PX[1]) // U + 1, 1), ((PX[1] + 150) // U, (PY + PH + 10) // U, 1, (RY - PY - PH - 10) // U)], OW))
A(px([((PX[1] + 150) // U - 3 + k, (PY + PH) // U + 2 + (3 - k) * 0, 7 - 2 * k, 1) for k in range(0)], OW))
A(px([((PX[1] + 150) // U - k, (PY + PH) // U + 2 + k, 1 + 2 * k, 1) for k in range(4)], OW))           # arrowhead up into CREW
T((PX[1] + PX[3] + PW) // 2, RY - 12, 20, OW, 'the answer → next: build', 'middle')

# --- the sea, 8-bit, along the bottom
def crests(y, col, phase, step=16):
    c = []
    for x0 in range(7 - step + phase, 313, step):
        for (dx, dy, w) in [(0, 2, 4), (4, 1, 2), (6, 0, 3), (9, 1, 2), (11, 2, 5)]:
            x, ww = x0 + dx, w
            if x < 7: ww -= 7 - x; x = 7
            if x + ww > 313: ww = 313 - x
            if ww > 0: c.append((x, y + dy, ww, 1))
    return px(c, col)
A(f'<rect x="{7*U}" y="{146*U}" width="{306*U}" height="{9*U}" fill="#0d1d2c"/>')
A(crests(141, '#5b83a3', 0)); A(crests(146, '#34546c', 8)); A(crests(151, '#34546c', 3))

# --- HUD, headline, domain
T(1488, 132, 26, OW, 'PLAYER ONE: OWNER', 'end')
T(800, 132, 26, AG, 'STAGE: THE LOOP', 'middle')
T(800, 222, 52, AG, 'the agents never answer for you.', 'middle')
T(800, 812, 34, DOM, 'shoalmark.tools', 'middle')
S, LX, LY = 3.0, 112, 96
off = S / 3.84615
lock = ''.join(f'<g transform="translate({LX + d * off:.2f} {LY + d * off:.2f}) scale({S})">{body}</g>' for (tx, ty, body), d in zip(groups, (8, 4, 0)))
if os.environ.get('MEASURE'):
    out = [o for o in out if 'scale(4)' in o]          # the crew alone, with the words and the lockup
svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">\n<defs>{style}</defs>\n<g shape-rendering="crispEdges">\n' + '\n'.join(out) + '\n</g>\n' + lock + '\n' + '\n'.join(words) + '\n</svg>\n'
open(os.environ.get('OUT', 'shoalmark-software-factory-x.svg'), 'w').write(svg)
print('ok', len(svg))
