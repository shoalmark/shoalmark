# The themes the tool ships

Two starters for the board (FM-002). Nothing reads them here: `python3 shoalmark.py --brand DIR --from <theme>` copies
one — its `theme.css` and its `fonts/` — into DIR, the place you choose (`<tracker dir>/brand/` for the repository,
`~/.config/shoalmark/` for yourself), and that copy is yours to change. A board with no theme looks as it did.

- `monochrome` — the terminal cut: IBM Plex Mono for every word on one grid, boxes titled in their border, a muted nautical chart behind the board.
- `shoalmark` — shoalmark's own: monochrome in a sea chart's colours as ECDIS draws them, magenta for what is owed to the Owner.

Each theme carries the three cuts of IBM Plex Mono it loads — IBM's Latin-1 cuts from `@ibm/plex-mono` 1.1.0
(`fonts/split/woff2/`; the package's npm integrity `sha512-hpsdRxR3…`), unmodified, under the SIL Open Font License in
its `fonts/LICENSE.txt`:

| File | sha256 |
|---|---|
| `fonts/IBMPlexMono-Regular-Latin1.woff2` | `10d3c7fa7eaf48e78db24f317b64f008a75e00f63a68bb3c2afc6ef51e58674f` |
| `fonts/IBMPlexMono-SemiBold-Latin1.woff2` | `1ce95cff1c5056cb0fed049c2912823293b158b816e193a6f937f2d92b1e0f39` |
| `fonts/IBMPlexMono-Italic-Latin1.woff2` | `08c4566f535253ee314ea35e4d75384a7bb151b4ed8345353698d95b33516d3b` |
