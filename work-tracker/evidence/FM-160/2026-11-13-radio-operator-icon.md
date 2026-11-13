0b212e5310522f4e

Model and effort, read from this seat's own transcript: `"model":"claude-opus-5-5"` 7 times, `"effort":"xhigh"` 7 times, and no other value of either.

# The coordinator's icon, the radio operator: the Designer's hand-back

Written 2026-11-13 07:37:54 CET, as `date` printed it, by the Designer seat (designer-2). At the base
`15a94b609dde7b9e60dea72857504f96f38e197e`. Nothing committed, nothing pushed, no tracked file changed: `git status` in `wt/`
is empty at the end.

## The key list

`git config --worktree --list` in `wt/`, after setting `seat.harness`:

```
user.name=Designer seat
user.email=336431084+shoalmark-designer[bot]@users.noreply.github.com
gpg.ssh.allowedsignersfile=work-tracker/allowed_signers
```

The brief asks for this list here, and the list carries the seat's session and harness keys. Whoever makes this folder public
judges whether those two lines go with it.

## The drawing: `coordinator.svg`

12 lines, 905 bytes, sha256 `9fe4f6b8ead9411111b33bc036713492159ef8fe861fce4e45effa22d15859b6`. It is variant 2 below,
byte for byte.

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" shape-rendering="crispEdges">
<title>coordinator — the radio operator</title>
<rect width="20" height="20" fill="#15293d"/>
<path fill="#34546c" d="M4 17h3v1h-3ZM13 17h3v1h-3Z"/><!-- the water -->
<path fill="#bccd8f" d="M9 14h2v6h-2Z"/><!-- the stake -->
<path fill="#e8d4a0" d="M7 7h6v1h-6ZM6 8h8v6h-8ZM7 14h6v1h-6Z"/><!-- the head, ashore in the land's buff -->
<path fill="#5b83a3" d="M7 5h6v1h-6ZM5 6h2v1h-2ZM13 6h2v1h-2ZM5 7h1v1h-1ZM14 7h1v1h-1ZM4 8h1v1h-1ZM15 8h1v1h-1Z"/><!-- the headset's band, over the crown -->
<path fill="#5b83a3" d="M4 9h2v4h-2ZM14 9h2v4h-2Z"/><!-- its ear cups -->
<path fill="#5b83a3" d="M6 12h1v1h-1ZM7 13h2v1h-2Z"/><!-- its microphone, at the mouth -->
<path fill="#15293d" d="M7 10h1v2h-1ZM12 10h1v2h-1Z"/><!-- the eyes, on the channel -->
<path fill="#f38a80" d="M12 12h1v1h-1Z"/><!-- the blush -->
</svg>
```

As a grid (`h` head, `B` headset, `.` ground, `|` stake, `~` water, `c` blush):

```
    01234567890123456789
 5  .......BBBBBB.......
 6  .....BB......BB.....
 7  .....B.hhhhhh.B.....
 8  ....B.hhhhhhhh.B....
 9  ....BBhhhhhhhhBB....
10  ....BBh.hhhh.hBB....
11  ....BBh.hhhh.hBB....
12  ....BBBhhhhhchBB....
13  ......hBBhhhhh......
14  .......hhhhhh.......
15  .........||.........
17  ....~~~..||..~~~....
```

**What it shows.** A head, two level eyes, one blush, and a two-way headset:

- a one-unit band arcing over the crown, one unit clear of it all the way round;
- an ear cup on each side at eye level (rows 9 to 12), the same on both sides, so it listens as much as it speaks;
- a three-unit boom from the left cup's lower corner to the mouth, inside the head's outline.

Nothing is held out from the head. There is no cap, badge, peak, wheel, bag, flag, hand-held set, tower, mast or screen.

**Why the left side for the boom.** The right side is where the herald's horn and the reviewer's monocle and cord live. A boom
from the left cup keeps that side empty but for the mirrored cup.

**The head's colour: the land's buff (`#e8d4a0`).**

- None of the seven heads uses it.
- It is the land's colour, so it hints at *ashore*, while the icon still stands in the water like the seven. The words carry
  *ashore*.
- It is the lightest warm tone, so the headset separates from it and the eyes keep their contrast: 10.1:1 in colour.
- Variant B used it for its head. Nothing else of B is reused: no bag, no lashing, and none of its shapes. B's head sat to the
  right (x 9 to 15) with its eyes turned aside; this head is centred (x 6 to 13) and faces front.
- If the Owner wants B's colour kept apart too, variant 3 shows the other way, and what it costs.

**The headset's colour: `#5b83a3`, the planner's cap band.** It is the darkest tone in the palette that still shows on the
night ground (3.69:1 in colour). In grey it is the same tone as the planner's band, but here it is an arc and two cups, not a
straight bar between a light crown and a black peak.

## The variants, and why not the others

All three are in the folder, each passes `export.py`'s rule, and all have the same title.

| Variant | What differs | Verdict |
|---|---|---|
| 1 | the band lies on the crown, hugging the head's outline; the cups sit outside the head at x 3–4 and x 15–16; the boom runs along row 13 | **not chosen.** At 200 px the hugging band reads as hair or a helmet's rim, the nearest thing to a cap. The cups reach x 16, the herald's horn's reach, and x 3, the owl's width. The boom on row 13 reads as a jaw or mouth line |
| 2 | the band one unit clear of the crown; the cups at x 4–5 and x 14–15, beside an 8-wide head; the boom stepping from the left cup to the mouth | **chosen.** It reads as headphones at 200 px and keeps every part inside x 4–15. In the board's grey the gap under the band shows the board's own ground, so the band never reads as a mass on the head |
| 3 | variant 2's shapes, with a `#5b83a3` head and a `#d9e4ec` headset | **not chosen.** The headset is the brightest part, and in grey on the dark board it is `#e1e1e1`, the planner's crown tone, over the head. The face drops to the middle tone, with the eyes only 3.69:1 against it in colour. The cold blue head loses the shore's hint |

## The tell-apart checks, at 20 px, in grey, without the ground

Read from the row page's renders: by eye from `board-row-20px-*-1x.png`, and by the unit-by-unit readback in
`renders/row-readback.txt`. All 40 icon readbacks (10 icons, 4 renders) are crisp: each unit is one flat colour.

| Against | The check | Result |
|---|---|---|
| the skipper's cap | the band one unit, the head showing around it | **passes.** The band is one unit, stands one unit clear of the crown, and the board's ground shows in the gap. The cap is two rows of the lightest tone, plus a band and a peak, flat and 10 wide on the head. Nothing light sits over the coordinator's head |
| the owl's ear tufts and spectacles | the cups at the sides must not read as either | **passes.** The cups are solid 2×4 blocks at eye level, in the middle tone, darker than the face. The tufts stand at the top corners (rows 4–5) in the head's own tone. The spectacles are dark rings round light eyes inside the face; the coordinator's eyes are plain dark 1×2 strokes |
| the herald's horn (x 13–16) | the boom inside the head and short; nothing out to the right | **passes.** Nothing passes x 15. The right cup mirrors the left, and the boom is on the left, inside the head (x 6–8). The horn is the lightest tone, on one side only, out to x 16 |
| the reviewer's monocle and cord | nothing reads as a ring and cord | **passes.** There is no ring anywhere, and nothing at x 15 below row 12, where the cord hangs. The monocle is still the one closed light ring among the eight, so the README's "the clearest of the eight" holds |

**The closest of the seven:**

- **by outline, the builder.** Both have a rounded top over a head of the same height. The coordinator is told apart by the gap
  under its band, and by being widest at the cups (rows 9–12) where the builder is widest at its brim (row 7).
- **by width, the auditor.** Both are framed at eye level. The coordinator's face is the light tone with plain eyes; the owl's
  is mid-grey, with light eyes in dark rings, and has tufts.

## Contrast in grey

The board's own filter, read back from the 1x renders.

| | dark board (`#0e0e0e`) | light board (`#f7f7f5`), inverted |
|---|---|---|
| the head against the board | `#d3d3d3`, 12.90:1 | `#2c2c2c`, 13.02:1 |
| the headset against the board | `#7c7c7c`, 4.62:1 | `#838383`, 3.53:1 |
| the headset against the head | 2.79:1 | 3.68:1 |
| the eyes against the head | `#262626`, 10.11:1 | `#d9d9d9`, 9.89:1 |

- The weakest pair is the headset on the light board, at 3.53:1. That is above 3:1, and the planner's band is the same tone.
- For comparison, on the dark board: the planner's head is 14.76:1, the herald's 7.21:1 and the owl's 6.13:1.
- In colour on the night ground, for the avatar: the head is 10.14:1 and the headset 3.69:1.

## The rule, as `export.py` reported it

- **`export.py`,** run inside `scratch/brand/seats/`, the copy of `wt/brand/seats/` with `coordinator.svg` added: **exit 0 for
  all eight, 24 PNGs written, no refusal.** `export.py` prints only breaches, so exit 0 means the safe circle, the stake, the
  ground, the palette and the 40-line rule all hold.
- **Measured with `export.py`'s own rasteriser,** in a scratch script that imports it:
  - the farthest drawn cell is 6.71 of the safe circle's 8 (the cups' outer bottom corners);
  - 12 lines of 40;
  - no colour outside the seven's palette.

## Option 2's lines: today → proposed

Every line number is at the base. The Owner rules every word with FM-160-Q2.

1. **The README's family line** (`brand/seats/README.md` L3, a paragraph running to L7):
   - *today:* "One family for the seven seats, in the site's master design. Every seat stands on the Pricke's stake …"
   - *proposed:* "One family for the eight seats, in the site's master design. **One fleet, in two settings: at sea, and in the yard,
     where a ship's own crew repairs and refits it.** Every seat stands on the Pricke's stake …"
   - The rest is unchanged, rewrapped to L3–L8.
   - The record's example ends "where its own crew repairs and refits the ship", where *its* comes before any ship is named.
     *A ship's own crew … it* says the same.
2. **The builder's row:**
   - **README L12.** *today:* "… plank by plank, as a yard builds the fleet". *proposed:* "… plank by plank, **as a crew refits
     its own ship in the yard**".
   - **`preview.html` L71.** *today:* "… plank by plank, as a yard builds the fleet." *proposed:* "… plank by plank, **as a crew
     refits its own ship in the yard**."
   - It reads as a refit, not new-building, and *its own* carries the crew's own ship from Addendum 1.
3. **The landing line** (`overrides/partials/landing/en.html` L73). It is carried by the **existing key `fleet_def`**: the same
   sentence follows the definition (`diffs/en.html.diff`).
   - *today:* "A seat is a role an agent takes, with its duties and its rights written down."
   - *proposed:* "A seat is a role an agent takes, with its duties and its rights written down. **One fleet, in two settings: at
     sea, and in the yard, where a ship's own crew repairs and refits it.**"
   - **Why not a new key:** the landing's test refuses any key that only one language holds (`test_shoalmark.py` L6499,
     `set(en) ^ set(de)`; its control "a key missing in German", L6571). A new key would need a German value, and the German
     waits for a native read.
   - The existing key lands the English alone, and `de.html` L72 stays as it is. The screened definition stays first and word
     for word. The other order, the settings first under the heading *The fleet*, is the Owner's to prefer.
   - The scratch copy still parses as the words dict, 209 keys.
4. **The coordinator's README row,** after the auditor's (base L17), and the preview's row before `</tbody>` (base L87):
   - **The second column** is the record's words, unchanged: "the radio operator: a two-way headset, the microphone at its
     mouth. Ashore, it sends and receives the word between the fleet's vessels; it informs and advises, and instructs none of
     them". **They fit the drawing:** the boom ends at the mouth, and *ashore* is in the words. No change is proposed.
   - **The third column,** my judgment from the render: "the band clear of the crown, a cup at each side: clear; the boom is three
     pixels, read only up close".
   - **The preview's job line** "informs and advises" is my proposal, from decision 1. The record gives no job line, and the
     seats page has no coordinator row yet.
5. **The other words an eighth seat touches** (decision 5), applied to the scratch README and preview only
   (`diffs/README.md.diff`, `diffs/preview.html.diff`):
   - **README:**
     - L3 "seven seats" becomes "eight seats";
     - L13 "the clearest of the seven" becomes "of the eight", and the judgment holds in the row page;
     - L16 "these seven" becomes "these eight";
     - L22 becomes "The seven's 21 PNGs equal headless Chrome's rendering of each SVG, 0 pixels apart; the coordinator's three
       are not yet compared.";
     - L29 "shows the seven" becomes "shows the eight".
   - **`preview.html`:**
     - the L7 comment, the L56 label and the L60 caption say eight;
     - the coordinator's image is added to the three strips (L57–L59);
     - L83 "these seven" becomes "these eight";
     - the L89 footer becomes "The sources are the eight SVGs beside this page; … The seven are the family the Owner approved on
       2026-09-30, with the changes they asked for; the coordinator's stands on the Owner's answer." It names no ask, because
       no line gains an id.
   - **Found while reading, for the lane:**
     - Decision 6 says `export.py` will say eight, but at the base `export.py` holds no count at all, so it has nothing to change.
     - README L30 still names FM-024's renders of the seven. It is left as it is, since no line gains an id.
     - The preview's own family paragraph (L51–L54) names no setting, and decision 4 does not list it, so it is unchanged.
     - `shoalmark.py` L4195 and L4903 and the design guide's L110 and L118 are outside this brief's scratch copies, and are
       untouched.

## The renders, by name

All are in `2026-11-13-radio-operator-icon/`. Every image is the SVG files drawn by `export.py`, or drawn by `wkrender` from a
page that loads them.

| File | Surface | Size | Scheme | Scale |
|---|---|---|---|---|
| `renders/board-row-20px-light-1x.png` | the board's session row, the eight and variants 1 and 3 | 20 px, grey, without the ground | light | 1x |
| `renders/board-row-20px-light-2x.png` | the same | the same | light | 2x |
| `renders/board-row-20px-dark-1x.png` | the same | the same | dark | 1x |
| `renders/board-row-20px-dark-2x.png` | the same | the same | dark | 2x |
| `renders/preview-avatar-light-2x.png` | the eight-row `preview.html` | 200 px and 20 px, night, paper and grey | light | 2x |
| `renders/preview-avatar-dark-2x.png` | the same | the same | dark | 2x |
| `export/coordinator-20.png` | `export.py`'s own PNG | 20 px | — | — |
| `export/coordinator-200.png` | the same | 200 px | — | — |
| `export/coordinator-400.png` | the same | 400 px | — | — |

**How the row page was made** (`row/row.html`, with its icons in `row/noground/`):

- It uses the board's `.seat` rule from `shoalmark.py` L4196–L4199, word for word.
- It uses the board's palette tokens: monochrome, the default, generated the way `palette_css` writes them.
- It uses the board's body type, and its section and fold rules, copied.
- Each row is the board's session-row markup: id, seat slot, seat word, worktree.
- Each icon is its file but for the ground square's line. The seven copies equal `SEAT_ICONS` byte for byte, checked against
  the tool's source read with `ast`.
- A word outside the eight shows the empty slot.

**Each render's `.log.json`:** no page error, and `res` empty in all six.

- WebKit lists no `file:` loads in `res`, so the loads were checked from the DOM after each script ran: every image complete,
  and every source under `scratch/`. The row page has 10 images per render, the preview 56.
- Nothing on either page names a network address.
- The renderer ran six final jobs in 11 s. All rendering together took well under the brief's 30 minutes.

`renders/row-readback.txt` is each icon read back unit by unit from the four row renders, with every tone's contrast against the
board.

## What I could not see, and why

- **The preview's own face.** `wkrender` lets a page read only from its grandparent folder. `preview.html` loads Plex Mono from
  `../../docs/`, above that folder, so both faces report `error`, and the preview renders in the system monospace. The icons
  are unaffected; text wraps differently from a checkout opened in a browser.
- **A dark preview.** `preview.html` has no colour-scheme rule, so its light and dark renders are byte-identical.
- **A true 1x screen.**
  - The renderer has no scale setting and draws at this screen's 2x. The 1x renders set `zoom: 0.5` on the root from the
    render job, so one CSS pixel is one device pixel; the icons read back at one device pixel a unit, crisp.
  - At that zoom the text measures slightly differently: the second heading wraps, and the image's bottom edge cuts 3 px of
    padding.
- **The board itself.** The row page copies the board's rules, tokens and row markup; the tool was not run.
  - The board inlines each icon as a `data:` image; the page loads files with the same bytes.
  - The board's first face, Berkeley Mono, is not installed here, so both fall back to the system monospace.
- **README L22's comparison.** Headless Chrome's rendering of the coordinator was not compared, because no other browser may
  run. The proposed line says so.
- **The landing.** It is not rendered, by the brief; the line is a diff.
- **The forge badge's circle.** The preview's CSS circle crop stands in for it.

## Renders made outside the named set, and the folders moved to the Trash

To learn the renderer's scale, I made one probe render of a blank page with a 20-px black square; it showed the 2x. The other
renders outside the named set:

- working renders of the row page and the preview before the final set;
- `export.py`'s PNGs of the three variants, run in a separate scratch copy, to view them at 200 px;
- a copy of the preview's two font files in `scratch/docs/`, made to test whether the renderer would load them. It would not.

None of these is in the hand-back. Moved to the Trash:

- `scratch/test` → `designer-radio-operator-2026-11-13-scratch-test`
- `scratch/work` → `designer-radio-operator-2026-11-13-scratch-work`
- `scratch/docs` → `designer-radio-operator-2026-11-13-scratch-docs`
- `scratch/variants/out` → `designer-radio-operator-2026-11-13-scratch-variants-out`

While it runs, `wkrender` writes its rule folder beside itself in `inputs/` and removes it at exit. `inputs/SHA256SUMS` still
passes at the end, and nothing else is in `inputs/`.

No secret or security weakness was met.
