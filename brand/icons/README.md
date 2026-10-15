# The UI icons (FM-053)

Four icons for the board, one family. Each stands beside its word, never alone: take the icon away and the word still says
what it means. What each means and where it stands is the [design guide](../design-guide.md)'s, §4; this file keeps their
rule. **The SVG is the source**: hand-written, a 12-unit grid (`viewBox="0 0 12 12"`) in whole-unit `<rect>`s only, filled
with `currentColor`, with `shape-rendering="crispEdges"`; no stroke, curve, path or transform. It is the Pricke's pixel style
and the seat icons' rule ([`brand/seats/README.md`](../seats/README.md)), so each rasterises crisp at 12, 24 and 48 px. Each
SVG is `aria-hidden="true"` and carries no `<title>`: an icon never stands alone, so its word is what is read.

| Icon | What it means | Where it stands |
|---|---|---|
| [`copy.svg`](copy.svg), two sheets | this button copies what it names; it never runs it | before the noun on every copy button: *stand-up prompt*, *close-out prompt*, *resume command*, *rebuild command*, *claude --resume*, *codex resume*, and *prompt* or *command* in a dialog |
| [`check.svg`](check.svg) | copied: the clipboard confirmed it | before *copied:*, and before *the prompt is on your clipboard* |
| [`cross.svg`](cross.svg) | not copied | before *not copied*, and before *copying did not work* |
| [`out.svg`](out.svg), an arrow leaving a box | a link that leaves the board | after the link's text: the running line's *shoalmark*, the signing page, the forge |

**Colour:** none of its own. An icon takes the colour of the text it stands in: grey in a button, ink under the pointer,
teal in *copied*, coral in *not copied*. It is never coloured on its own. **Size:** 12 px on the 14 px text, one unit below
the baseline, `.7ch` from its word.

**A new icon** joins the set only when a word cannot carry its meaning alone, and on the same grid, by the same rule.

**In the tool:** nothing reads these files yet. With the board's build they would become static constants, as `PRICKE` is.
