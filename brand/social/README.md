# Social images

shoalmark's images for profiles and link previews, made of the site's own parts. **Each SVG is the source**; the PNG or
JPEG beside it is its export.

| Files | Size | Use |
|---|---|---|
| `profile-header.svg`, `.jpg` (in use), `.png` | 1500 × 500 (3 : 1) | a profile's header |
| `repository-card.svg`, `.png` | 1280 × 640 (2 : 1) | the repository's social preview |
| `link-preview-en.svg`, `.png`; `link-preview-de.svg`, `.png` | 1200 × 630 | the site's link preview, English and German; the site serves them as `assets/preview.png` and `preview-de.png` |

- **The wordmark:** the landing hero's lockup, lowercase *shoalmark* with the Pricke in the Watt's green (`#bccd8f`),
  and the hero's two shadows.
- **The words:** *A workbench for your agents.* in the Watt's green, the agents' colour, and *Your decisions on record.*
  in the land's sand (`#e8d4a0`), the person's: the landing's two players. The German cards say *Eine Werkbank für deine
  Agenten.* / *Deine Entscheidungen belegt.* Then shoalmark.tools, in the drying line's green (`#b8c98c`).
- **The chart:** a strip of the landing's own chart, its canvases exported as the page draws them, at the page's own
  scale (4 px a chart pixel). The wreck sprites stand where the page draws them, in the key's colours. The header shows
  the record of 9 October 2026, and the cards the record of 21 October 2026: pictures of the chart, not counts.
- **Safe zones:** every word stands inside the band a profile header's crop keeps, clear of the profile photo, and on the
  repository card inside its 80 px border.
- **The font:** each SVG embeds `docs/assets/fonts/IBM-Plex-Mono-normal-600-latin.woff2` byte for byte, © 2017 IBM
  Corp., under the SIL Open Font License 1.1, as `docs/assets/fonts/ibmplexmono-OFL.txt` gives it.
- **Export:** a browser engine that reads WOFF2 in SVG renders each SVG at its size; these were WebKit's. The profile
  header's JPEG is quality 100 without chroma subsampling, so the pixel art keeps its colours.

They carry no figure and no release number, so nothing on them goes stale; the chart is a picture of the record on the dates above.
