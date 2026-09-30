# The seat icons (FM-024)

One family for the seven seats, in the site's master design. Every seat stands on the Pricke's stake in the Watt's green
(`#bccd8f`), at the same place (x 9–10, down to the edge) and in the same water, on the site's night ground (`#15293d`):
a head, two eyes, a blush, and the one thing its job holds. The shape carries the seat; its colour, from the site's
palette, is never the only carrier. **The SVG is the source**: hand-written, a 20-unit grid in whole-unit rectangles, at
most 40 lines; nothing but the stake's foot and the water leaves the safe circle (radius 8 of 20, 10 % inside the crop).

| Seat | Its character, and why it fits the job | At 20 px, grey included — the Designer's judgment |
|---|---|---|
| principal | the skipper: a captain's cap, a level gaze — it plans the passage; the course is the Owner's | the flat, banded cap: clear |
| implementer | the builder: a yellow hard hat on the stake's own green — it builds what the plan says | dome and brim: clear; in grey the brim carries it |
| reviewer | the inspector: a monocle, the other eye squinting — it attacks a tip and believes what survives | the ring at the right edge: the clearest of the seven |
| research | the tide gauge: a graduated staff, eyes wide — it checks and measures, the marks, not the mood | the tall, narrow body: clear; its marks are one pixel |
| go-to-market | the herald: a horn, eyes open on the stranger — it announces only what passed its screen | the horn out to the right: clear |
| designer | the painter: a tilted beret on a pear of a head — it draws the chart, the marks and these seven | the pear's narrow top: told from the principal's cap by outline |
| auditor | the owl: spectacles and ear tufts, wide awake — it seals its plan first, then checks what was missed | tufts and two rings: clear |

**Export:** `python3 brand/seats/export.py` writes `out/<seat>-20.png`, `-200.png` and `-400.png` (`out/` is git-ignored).
The standard library only: it rasterises the grid itself, after checking the rule above (exit 1 names the breach). An SVG
it cannot rasterise — a curve, a circle, a transform — exits 2 and prints the `rsvg-convert` and `cairosvg` commands for
it; neither tool is installed where this was made. Its 21 PNGs equal headless Chrome's rendering of each SVG, 0 pixels apart.

**Upload:** GitHub takes *"a PNG, JPG, or GIF file under 1 MB"*, recommends *"an image dimension of 200 pixels by 200 pixels"*,
and draws a badge as *"a square image inside a circular background"* ([custom badge](https://docs.github.com/en/apps/creating-github-apps/registering-a-github-app/creating-a-custom-badge-for-your-github-app));
Marketplace asks for *"at least 200 pixels x 200 pixels"* ([logos](https://docs.github.com/en/apps/github-marketplace/listing-an-app-on-github-marketplace/writing-a-listing-description-for-your-app#guidelines-for-logos)); both read 2026-09-30.
Upload `out/<seat>-200.png` and set the badge background colour to `#15293d`, the icons' own ground.

**The proof:** [`preview.html`](preview.html) shows the seven at 20 and 200 px, circle-cropped by CSS, on the night, on the
paper and without colour; its renders are `work-tracker/evidence/FM-024/seat-icons-preview-2026-09-30*.png`.
