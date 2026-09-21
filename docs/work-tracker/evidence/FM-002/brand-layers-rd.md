# FM-002 — a board anyone can brand: R&D, pre-registered

Principal, 2026-09-21. The Owner asked how a user or an agent brands their board — a name, a logo, a colour scheme,
*what else* — and then named the real problem: **several kinds of user want that at once**, so configuration has a
global and an individual side. Ruled: both global layers exist (per person, and per organisation travelling with the
vendored copy) · files only, the page keeps no state · `labels.yaml`, not JSON · **do not over-engineer — the simple
solution wins** · the test bed is the origin, with its real logos, brand tokens and fonts.

**This file is written before the spike, so the bars cannot move to meet the result.** Branch
`rd/fm-002-brand-layers`; nothing merges until the Owner has read the outcome.

## The design to prove — one rule, three files, four places

**Three optional files, the same names everywhere:**

| File | What it carries |
|---|---|
| `theme.css` | colours and fonts — the nine variables the page already uses |
| `logo.svg` (or `logo.png`) | shown in the header, and as the favicon |
| `labels.yaml` | every word of the board's chrome — section names, legend, buttons, the viewer's words, how a status is *displayed*, `tagline`, `footer`, what the Owner is called. This is also how a German board happens. **YAML, not JSON (Owner):** flat `key: value` lines with `#` comments — the form every tracker's front matter already has, read by the reader the tool already has (`parse_frontmatter`); no YAML library, so no nesting, and the gate of C9 says none is needed. The deriver keeps JSON: that is a protocol between programs, not a file a person edits |

**Four places, nearest to the viewer wins:**

| # | Place | Who | Committed? |
|---|---|---|---|
| 4 | `~/.config/shoalmark/` (`$XDG_CONFIG_HOME`) | the person — every repository they open | never in any repository |
| 3 | `<tracker dir>/` — beside the trackers | the repository | yes |
| 2 | `tools/shoalmark/brand/` | the organisation — copied and pinned by `--vendor` | yes, as part of the pinned tool |
| 1 | built into the tool | defaults | — |

**One rule:** the board is built from 1 → 4 and the later place wins — `theme.css` files are simply concatenated in
that order (CSS already cascades, so a person's file with one variable changes one colour); `labels.yaml` files are
merged key by key; the logo is the last one found. **No new key in `shoalmark.toml`** — `name` stays where it is.

**One invariant, and it is the point of the R&D:** *only the git-ignored board reads places 2–4's brand files.*
`INDEX.md`, the gate's verdict, `--check`, `--print-written` and the deriver are functions of the repository
alone — otherwise two people's commits would fight over a generated file.

**One new flag:** `--brand` prints, for the theme, the logo and the labels, which places contributed — the answer
to *"why is my board blue?"*. `--brand DIR` writes a commented starter there: a `theme.css` naming the nine
variables with their meaning and the light/dark pair, and a `labels.yaml` with every key in English.

Small things that ride along because they are a few lines each: the name and `tagline` shown in the page header ·
the logo inlined as a data URI (one code path for every place; a script inside an SVG cannot run in an image) ·
a print style that forces the light palette · a **warning** (never a failure — the board is not committed) when
the effective theme's text-on-background contrast is below 4.5 : 1.

## Cut on purpose — the Owner's *do not over-engineer*

A per-person-per-repository layer · anything remembered by the browser · translations shipped inside the tool and a
`language` setting (a repository commits its `labels.yaml`; msr-lager's German one is the worked example) · a check
that status colours stay distinguishable · a font loader (fonts by installed name; a font file only beside the
trackers) · a theme editor · any setting for any of it. Each can be added when a real user asks twice.

## Pre-registered claims — written before the spike

| # | Claim | Proof | Kills the design if |
|---|---|---|---|
| C1 | **Committed output ignores every brand layer** | with a hostile person folder and a hostile organisation folder present (a `labels.yaml` renaming statuses, a `theme.css`, a logo): `INDEX.md` byte-identical, `--check` and `--print-written` identical — in shoalmark, a copy of msr-lager and the scratch copy of PortDive's 502 trackers | one committed byte moves |
| C2 | **One rule explains every outcome** | eight cases (which places hold which file) → predicted result equals the rendered board, and equals what `--brand` reports | a case needs a second rule |
| C3 | **Nothing present, nothing changes** | no brand file anywhere, `HOME` unset or unreadable (a hook, CI, an agent): the board renders; it differs from 0.7.0's only by the header element and the print style | a run fails, or differs elsewhere |
| C4 | **A German board** | msr-lager copy with a German `labels.yaml`: the rendered chrome of the board and of one tracker page holds **0 English words** (tracker text, ids and the words an agent types aside); search still finds a status by its English *and* its displayed word | statuses cannot be shown translated without touching the logic that compares them |
| C5 | **A logo, safely** | `svg` and `png` shown in header and favicon; an SVG carrying a script does nothing; a file over 200 KB is skipped with a warning | the page has to reference a path outside the repository |
| C6 | **The contrast warning** fires on an unreadable theme, names the two colours and the place they came from, exits 0 | it needs a colour library |
| C7 | **The organisation layer travels** | `--vendor` copies `brand/` and lists its files in `PIN`; the client repository overrides each file beside its trackers without touching `tools/` | the pin makes a client's override impossible |
| C8 | **Cheap and small** | the post-checkout refresh on PortDive's corpus within +10 % of today's 1.38 s; the core grows ≤ 120 lines; still one file, Python 3.9, no dependency | > +25 % or > 200 lines |
| C9 | **Simple enough to explain** | the whole feature is one README section of ≤ 25 lines with one table, and `shoalmark.toml` gains no key | it needs more — then something is cut, not explained |

**Forecast:** C1 0.85 · C2 0.85 · C3 0.90 · C4 0.60 · C5 0.85 · C6 0.85 · C7 0.80 · C8 0.80 · C9 0.70 · all nine 0.30.
C4 is where I expect trouble: status words are data the page's logic compares (`"In Progress"`), and the board's
chrome has more strings than I have counted.

## The test bed is PortDive, with its real assets (Owner)

Read, not assumed — `the origin's public web assets (`portdive-com/public/`)`:

| Asset | What it lets the R&D test for real |
|---|---|
| `logo/portdive-logo-micro.svg` — 4.7 KB, `viewBox 0 0 16 16`, fixed fills, no script | the header logo and the favicon. **It has no `currentColor` and no dark variant** — whether it survives the board's dark scheme is a finding waiting to happen |
| `portdive-logo-primary.svg` — 80 KB, `1024 × 1024` | the size cap, and what a full logo does to a one-line header |
| `brand/portdive-brand-tokens.css` — the Chalk / Deep palette, teal and coral, as `--pd-*` variables | **the source of truth for the colours.** Today PortDive's `theme.css` would copy eleven hex values out of it — two places to change a colour. The test: `theme.css` *imports* the tokens and only maps them (`--bg: var(--pd-deep-ground)`) |
| `fonts/Geist-*.woff2`, `GeistMono-*.woff2` | real `@font-face` from files that live in a **submodule**, not beside the trackers — and the board must still render when that submodule is not checked out |

This forces one refinement of the rule, and it makes it simpler, not bigger: **each place's `theme.css` becomes its
own `<style>` element, in order 1 → 4**, instead of one concatenated block — because `@import` and `@font-face`
only work at the top of a stylesheet. Nothing else changes.

Two more pre-registered claims, from real assets:

| # | Claim | Proof | Kills it if |
|---|---|---|---|
| C10 | **PortDive's board wears its real brand from its own source of truth** | a `theme.css` of ≤ 15 lines beside the trackers imports `portdive-brand-tokens.css`, loads Geist from the submodule's files, and the micro mark sits in the header and the tab — rendered in headless Chrome in **both** colour schemes and looked at; with `portdive-com` not checked out the board still renders, in fallback fonts and built-in colours, with one warning | relative URLs from the git-ignored page into a submodule do not resolve from disk |
| C11 | **The logo is legible on both grounds** | the micro mark against Chalk and against Deep, measured by eye and by the same contrast function on its dominant fill | it is not — then the convention gains `logo-dark.svg`, *or* the finding goes to the Owner as a brand-asset gap; decided by what the render shows |

**Forecast:** C10 0.65 · C11 0.45 — a 16-pixel mark with fixed fills on a near-black ground is the likeliest failure here.

The organisation layer is tested with a neutral made-up house brand vendored into the msr-lager copy — PortDive is
a product's brand, not the consultancy's, and it must not leak into a client repository by accident.

## Outcome

**The design holds: one rule, three files, four places — and no setting. Nine of eleven claims held outright; one held
after the spike found it false as first built (C10); one bar was missed without killing anything (C8's size). The
two claims I feared most were the two I was most wrong about.** Spike on `rd/fm-002-brand-layers`; the origin was
never written to — everything ran in scratch copies. Worked examples kept beside this file:
[the origin's theme](examples/origin.theme.css) (8 lines) and [a German board](examples/german.labels.yaml).

| # | Forecast | Outcome | Measured |
|---|---|---|---|
| C1 | 0.85 | **held** | a hostile person folder (a magenta ground, statuses renamed, a logo) laid over three beds — this repository, a copy of msr-lager, a copy of the origin's 502 trackers: `INDEX.md` **hash-identical** in all three, `--check` 0 → 0, `--print-written` 1 · 1 · 11 paths, while the person's theme *did* reach each board. In the suite too, with a hostile organisation folder on top |
| C2 | 0.85 | **held** | the places are read organisation → repository → person and the later wins: each theme its own stylesheet in that order, labels merged key by key, the last logo found; `--brand` reports the same chain. Reordering the places fails a check |
| C3 | 0.90 | **held** | no brand file, `HOME` and `XDG_CONFIG_HOME` both unset: exit 0, no theme element, no image, English words |
| C4 | **0.60** | **held — cleanly** | 70 labels. A German `labels.yaml` of 69 lines; rendered in headless Chrome, the chrome of the board and of a tracker page holds **0** of 26 English words probed; search finds a status by its English word *and* its German one. The page's logic was not touched: it compares `"In Progress"`, it *shows* `In Arbeit` |
| C5 | 0.85 | **held** | svg and png inlined as data URIs, in the header and as the favicon; an SVG with a `<script>` did nothing (it sits in an image); a file over 200 kB is skipped with a warning |
| C6 | 0.85 | **held** | `#888888` on `#777777` → *contrast 1.3:1 — below 4.5:1*, names the two colours and whose file, exit 0. The WCAG formula is eight lines |
| C7 | 0.80 | **held** | `--vendor` copies `brand/*` and lists it in `PIN`; a client's `labels.yaml` beside its trackers overrides the organisation's footer while the organisation's colour still applies — without touching the pinned copy |
| C8 | 0.80 | **half** | cost **held at the edge**: 1.46–1.52 s against 1.38 s, +6…10 % (bar: +10 %). Size **missed its bar, not its kill**: the core grew 1,812 → ~1,990 lines, about +175 (bar ≤ 120, kill > 200) — 70 labels are 35 of them, the starter 18 |
| C9 | 0.70 | **held on lines and keys, missed on tables** | README §9 is 20 lines (bar ≤ 25) and `shoalmark.toml` gained no key — but it needs **two** tables (files · places), not one |
| C10 | 0.65 | **false as first built — then held** | with the tokens imported and Geist loaded from the origin's submodule, its board wears its real brand in both schemes from an **8-line** `theme.css` — relative URLs from the git-ignored page into a submodule *do* resolve from disk. **But with that submodule absent the first spike rendered white on black with its status squares gone:** a variable mapped onto a missing import is *invalid*, it does not fall back to the previous place. Fixed in the tool: a theme whose `@import` is not there is left out whole, with one warning — and a second render showed *that* fix had also dropped the repository's tagline, because it skipped the whole place. Both caught by looking at the screenshot, neither by a check; both have checks now |
| C11 | **0.45** | **held — I was simply wrong** | the origin's micro mark is teal, and teal reads on Chalk and on Deep alike. No `logo-dark.svg` is needed; the convention does not grow |

**All eleven: forecast 0.30.** Nine held outright. My two lowest forecasts — the German board (0.60) and the logo on
a dark ground (0.45) — were the cleanest results; the claim I was comfortable with (C10, 0.65) was the one that was
false. The record's pattern, again: I fear the visible risk and miss the mechanical one.

## Found that nobody had named

1. **A mapped theme is all-or-nothing.** Importing the brand tokens instead of copying them is the right design —
   one place to change a colour — and it means a missing import cannot degrade gracefully by itself. The tool now
   decides that, not the stylesheet.
2. **Looking found what checking did not — twice.** The white-on-black board and the vanished tagline both passed
   every check that existed. The suite renders the board; it does not *look* at it. Nothing here fixes that.
3. **A mistyped label was silently taken.** A mutation showed no check covered it: `tagine:` is now named in a
   warning and never reaches the page.
4. **The logo can be a symlink** into a submodule (`logo.svg → ../../portdive-com/public/logo/…`): one source of
   truth for the mark too, and it disappears quietly — not loudly — when the submodule is absent.
5. **`Status` is German.** The English-word probe needed the word list edited, not the board.

## Unproven

Only one real logo was tried, and it happens to suit both grounds. Fonts were loaded from the repository's own
files only — a font in the person's or the organisation's place is documented as *installed fonts only* and was not
tested. The organisation layer was exercised with a made-up brand, never with a real consultancy's. No person other
than this seat has written a `labels.yaml`; whether 70 flat keys are pleasant to translate is a guess. The
contrast warning reads hex colours only — the origin's theme, which maps variables, gets no warning either way.
Windows paths and `%APPDATA%` were not considered.

## For the Owner to rule

1. **Merge as 0.8.0?** Then: the origin takes the 8-line theme, the symlinked mark and a tagline on its next
   `--vendor`; msr-lager takes the German labels.
2. **The one rule lets a person's theme override a client's brand on that person's own machine.** I would keep it —
   it is their screen — but it is the Owner's call.
3. **The size:** +175 lines for branding in a ~1,800-line tool. The labels could live in a file beside the tool
   instead of inside it (−35 lines, one more file to vendor). I would leave them inside.
