# Review — FM-002 slice A, the brand layer: shoalmark's own board and site wear `shoalmark` (2026-09-26, Reviewer, session `8e509911/reviewer-34`)

- **Date:** 2026-09-26, 16:03–16:55 CEST.
- **Seat:** Reviewer (Opus 5.5, highest effort), a sub-agent of Principal session `8e509911`.
- **Session:** `8e509911/reviewer-34`.
- **Worktree:** `shoalmark-review-4`, detached at the tip. The board and the site were rebuilt here, the before files
  checked out from `2a9f7eb` and restored, and the tree was clean after. Every render, measure and the `npm pack` ran in
  the session's scratchpad. The Owner's checkout, `shoalmark-gtm`, every other worktree and every folder of session
  `8b91dba2` stayed outside every command.
- **Tier:** docs/brand, one pass, as the judging pass gave slice A (`13d70189`, READY WITH FINDINGS; on main since PR 93).
  A P3 is fixed forward; a P2 sends it back.
- **Independence:** same session — a sub-agent of 8e509911, reviewing its Implementer sub-agent's branch
  (`8e509911/implementer-36`). Reported as such, not independent.
- **The Owner's rule for this build, as the Principal relays it:** *the mock as-is, nothing changed or added.* Every
  difference from the mock is judged below; two rules differ, each forced by his 4.5:1 rule.

**Reviewed:** `fm/002-slice-a-the-brand-layer` at `70fedd3bf3e2554877918da777d7b013fdee4752` (ls-remote, 16:53), six
commits on `2a9f7eb`: `349fbe8` the board, `73ea047` the site, `361336a` the two contrast rules, `5ff3539` the renders,
`11faa03` the checks, `70fedd3` the record. No pull request is open for the branch. `origin/main` moved to `bef2a1e`
(PR 93) during the build; check 12 covers it.

## The checks

| # | Check | How | Result |
|---|---|---|---|
| 1 | Scope | `git diff --name-status origin/main...70fedd3` | 27 paths: `work-tracker/brand/theme.css` and the two new `.woff2`, `docs/stylesheets/shoalmark.css`, 23 files under `evidence/FM-002/slice-a/`, FM-002, `CHANGELOG.md`. No `shoalmark.py`, `brand/themes/`, `lefthook.yml`, `.github/`, test or `labels.yaml`. Every subject names FM-002. `--vendor` copies `TOOL_FILES` and the root `brand/`, never `work-tracker/brand/`, so the CHANGELOG's *nothing new that `--vendor` copies* holds. ✓ |
| 2 | The board's theme against the aligned mock | `diff` of `theme.css` against main's `FM-006/themes/monochrome.css` + `shoalmark.css`, concatenated; 0.18.2's theme, which the file replaces, read rule by rule | Rules that differ: **(a)** the `::placeholder` rule, marked *not the mock's* — deviation 1 below. **(b)** The two cuts' urls, `brand/fonts/…` → `fonts/…`: the brand layer re-bases a path from the file it is in (`brand()`), so the mock's would have been `brand/brand/fonts/` (the record's R2). **(c)** The Regular's `@font-face`, declared here: the mock sat on 0.18.2's theme, which declared it; this file replaces that theme. **(d)** 0.18.2's rules gone — Plex Sans, its palette, its dark `#fff` headings. Each is overridden by a mock rule of the same specificity later in the mock's own stack, so the mock never showed them. The rest is comments: the header, three `WORKAROUND n of 3` markers, one mock comment line de-duplicated, and one rule line split in two. (b)–(d) change no pixel (check 6). ✓ |
| 3 | The site's stylesheet against the mock | `diff` against main's `docs/stylesheets/shoalmark.css` + `site-monochrome.css` + `site-shoalmark.css` | Rules that differ: **(a)** `.md-footer-meta{--md-default-fg-color:var(--bandink)}`, marked *not the mock's* — deviation 2 below. **(b)** The file's `@import` is widened from Mono 500 to 500;600, and the mock's second `@import` (400, 500, 600, italic 400) is not added. Zensical's own link loads Mono 400, 400i, 700 and 700i; I read it in every built page. So the page loads the same faces, from one `@import` as before plus Zensical's link: **no second Google Fonts load**. The rest is comments. (b) changes no pixel (check 6). ✓ |
| 4 | The fonts | `npm pack @ibm/plex-mono@1.1.0` in the scratchpad; the tarball against `npm view … dist`; sha256 of `fonts/split/woff2/*-Latin1.woff2` and `LICENSE.txt` | Tarball sha1 `5406e372…`, sha512 `hpsdRxR3…UG68A==`: both are the registry's. **SemiBold `1ce95cff1c5056cb…1e0f39`, Italic `08c4566f535253ee…516d3b`, Regular `10d3c7fa…`** — the repository's three equal the package's, and `LICENSE.txt` equals it too (`7e6b2818…`). The hashes are in `349fbe8`'s body, the evidence README and FM-002's clause. ✓ |
| 5 | The font urls resolve where the brand layer serves them | built board (`python3 shoalmark.py --html-only`); Chrome with every host unresolvable; `document.fonts`, the network log | The page names three urls, all `brand/fonts/…`, all three requested and `loaded` in both schemes. 0 failed requests; no host reached. `--brand`: theme, logo, wordmark and labels from `repository`, no warning. ✓ |
| 6 | The renders are real; the build is the mock | Rebuild as the README's *Rebuild* says (checkout from `2a9f7eb`, `--html-only`, `uvx zensical@0.0.65 build`, `build-mocks.py --plex` on the npm files); the committed `render.mjs` three times; a full-page renderer of mine, FM-002's `shot()` taken to the page's full height, over the board, its tracker view (`#=FM-002`), the acts dialog and the 11 site pages, 1440 and 390 px, both schemes, mock against after; ImageMagick `compare -metric AE` | **Committed PNGs:** 16, each 1440×1000 or 390×844, 8-bit RGB. Chunks IHDR, IDAT and IEND only, so no metadata. Mine against them: 11 of 16 are 0 px. The two board *after* 1440 differ by 1,298/1,302 px in one band at y 988–1000, and the two *before* 1440 by 40,520/40,814 px (y 845–1000). Both are the *sessions* line, re-ordered by the clock (seen). The site *after* 1440 by day differs by 342 px, run noise, below. **After against mock, every run:** the board 411–419 px, all inside the search box — the placeholder. The full pages add the dialog's note placeholder (2,115–2,155 px). The tracker view is 0 px. The board's foot, band and running line are 0 px outside the placeholder. The site by night is 0 px on every page at 1440. By day the foot's *Zensical* link is 265 px on every page — the foot rule. (`404.html` loads its assets from `/shoalmark/…`, so it rendered unstyled, and identical, on both sides here.) **Noise that moves between runs, neither side's:** the nav's *Deutsch* re-antialiased (0, 318 and 342 px in three runs; one run also 8 px at the search box's corners). Zensical's floating contents button at 390 px, caught mid-fade on either side at random (2,570 px; gone on re-render, then elsewhere). ✓ |
| 7 | AU-16 | the committed `checks.mjs` re-run on the rebuilt stage; my own probe of `Accessibility.getFullAXTree`; the `content:` strings counted | Board, tracker view, dialog and site, both schemes: 0 chart figures and 0 markers read. Buttons are named `◐ auto`, `by board`, `done`, `reschedule`, `OK — give me the command`, `abort`, never `[ … ]`. The control, with the alt text stripped (14 in the board, 5 in the site), reads 261 figure nodes and 37/18/21 markers. `theme.css`: 12 strings carry `/ ""` — 10 markers after their fallbacks, and the 2 figure strings. One string is read on purpose: *owed to the owner*, the box's name (workaround 1). The site: 5 of 5. ✓ |
| 8 | AU-18 | the same | Content box 838 px; Plex Mono 14 px advances 8.4 px, so **99.8 characters**. The longest line holds 99, of 55. ✓ |
| 9 | Contrast, both schemes, on the built files | **(a)** The committed `checks.mjs` re-run: pixel grounds, its #767676-on-white control at 4.542:1. **(b)** A second method of mine: every visible text node's computed colour against its ancestors' background colours, on all 11 site pages at 1440 and 390, the board at 1440 and 390, two tracker views, the dialog. **(c)** The acts dialog driven to its second screen (the command). **(d)** `checks.mjs` on the mock, for the deviations' *before* | (a) 787 measurements a scheme on today's board (746 at 361336a; the board grew), 0 below 4.5:1, 30/32 pairs. (b) 6,562 a scheme: by night, none below 4.5:1 on any page. By day, the only ones are the foot's texts on the board (`#f`, `#r`). My method cannot see a band drawn as a sibling's border image; (a) measures them on the band at 6.06 and 8.25. (c) The command screen: lowest 6.48 by day, 6.42 by night. **Lowest pair by day: 5.76:1**, the Watt's green `#526214` on shallow water `#e3eff7` (a group's `//`, the site's page-you-are-on); under a chart line, 5.30:1. **By night: 5.98:1**, a row's tags `#90a3b1` on the zebra `#152535`. (d) On the mock exactly the two deviations' pairs fall below 4.5:1, and nothing else does. ✓ |
| 10 | His word of 09:23:58, the tracker view | the board at 1440, both schemes | The header box `#H` is at (283, 48), inside the chart's top border (22 px, the neatline 6 px in), in both schemes. The tracker view has no header, as today's board. It starts at (283, 62), 874 px wide, its first heading at (283, 420), after = mock. ✓ |
| 11 | The site | `uvx zensical@0.0.65 build`, before and after, in the worktree and in scratch exports | Green, *No issues found*. `extra_css` still names `stylesheets/shoalmark.css`, the file that changed, and every page links it once. Its one `@import` is the first rule. Every page has one Google Fonts `<link>` (Zensical's) and one `@import`, as before. The self-hosting item is named in the CSS, the README, the commit and FM-002. ✓ |
| 12 | Gates | this worktree at the tip; merge-tree; a local unreferenced merge commit of `bef2a1e` + `70fedd3` (with trailers), checked out detached, then back | `--check` 0 (*INDEX.md is up to date — 38 trackers*, *judged before build: on*, the Owner's two sections guarded). `--session-check` 0. `test_shoalmark.py` 462 ok and `test_core.py` 148 ok, *skipped here: 0 checks*, *all green*, on 3.14.3 and on 3.9.6. `git merge-tree --write-tree origin/main 70fedd3`: clean. On the local merge, `--check` 0, INDEX.md up to date, and `--session-check` 0. FM-002 reads whole there — main's opening, then the slice-A clause. ✓ |
| 13 | The record | FM-002 and CHANGELOG diffs | FM-002 has the ship-log row, newest first, naming the five build commits, and one *What is true now* clause, *not merged*. CHANGELOG has `## Unreleased — 0.18.5` with one bullet naming FM-002, his answer (`4e00f85`, PR 90) and slice A. FM-002's numbers — 5.76 / 5.98, 99.8, 3.63 and 1.12 — are the ones I re-measured; its *746 a scheme* is 361336a's count. ✓ |

## The deviations from the mock — two, each forced by the 4.5:1 rule

| # | Rule, marked in the file | Pair it fixes | By day, mock → after | By night, mock → after |
|---|---|---|---|---|
| 1 | `theme.css`: `::placeholder{color:var(--mute);opacity:1}` — the search's and the dialog's note's placeholder, which no mock rule styles (Chrome's own `#757575`) | placeholder on the panel | `#757575` on `#ffffff` **4.61** → `#51606c` **6.48** | `#757575` on `#111f2c` **3.63** → `#90a3b1` **6.42** |
| 2 | `docs/stylesheets/shoalmark.css`: `.md-footer-meta{--md-default-fg-color:var(--bandink)}` — Zensical's `html .md-footer-meta.md-typeset a:not(:focus,:hover)` outranks the mock's foot rule | the foot's *Zensical* link on the band | `#10202e` on `#15293c` **1.12** → `#f3f6f9` **13.69** | `#d9e4ec` on `#15293d` **11.48** → **11.48** (the two inks are one; 0 px changed) |

I measured all eight numbers with the committed pipeline, on the mock and on the build. There is no deviation beyond
these two. The source differences of checks 2(b)–(d) and 3(b) are what the brand layer and the brief require. They
render pixel for pixel as the mock, in every view and on every page I rendered (check 6).

**The workarounds kept for slice B** are marked where they stand: 1, the owner's box title as CSS content; 2, the foot's
band hung from the running line lifted onto the claim's line (`#f`, `#r` and the lift rule); 3, the zebra by
`nth-child`. They are the mock's rules, unchanged.

## Findings

**R1 · P3 · confidence 90% · The README's *Rebuild* takes *before* from `origin/main`, which after the merge is the
*after*.**
- *The gap:* `evidence/FM-002/slice-a/README.md`, *Rebuild*, its first checkout, runs `git checkout origin/main -- work-tracker/brand/theme.css
  docs/stylesheets/shoalmark.css` to get *before*. Today main still holds the pre-slice files, so it works; I ran it
  from `2a9f7eb`. Once the Owner merges, `origin/main` holds this slice's files, and the recipe builds *after* twice.
- *Why it matters:* the renders are evidence the Owner is meant to be able to rebuild. After the merge, the *before*
  column could no longer be rebuilt from the recipe.
- *What closes it:* `git checkout 2a9f7eb -- …`, the base the README already names. Fixed forward.

**R2 · P3 · confidence 70% · The site's one deviation from the mock is in no committed render.**
- *The gap:* the renders are each page's top 1000 or 844 px. The site foot's link (deviation 2) lies below that, as the
  README says. The Owner sees the renders before the merge under his *mock as-is* rule. He can find deviation 1 in the
  board renders' search box, but deviation 2 only as a sentence.
- *What closes it:* the site's foot by day, mock and after, as FM-006's `render.mjs` already shoots a foot (its
  `foot` shot). Or this file's table carries it to him. Fixed forward.

Noted, not findings:
- The board sets text at weight 700 (`<b>`, `strong`) and carries no 700 cut, so Chrome sets it in the 600 face. The
  mock does the same, pixel for pixel.
- The README's pair list is 361336a's (746 measurements, 29/31 pairs). Today's board gives 787 measurements and adds
  two link pairs at 6.29 and 7.72. The lowest ratios are unchanged.
- The README's *site identical but one word* is right for the viewport renders. The full pages show the run noise of
  check 6.

## Not verified

- Firefox and Safari; print; a real phone (390 px is Chrome's device metrics); a screen reader.
- The answer dialog under the theme: no ask is open on today's board.
- Hovered states only through the committed pipeline's forced `:hover`; my second method measures the page at rest.
- The site live: `docs.yml` deploys only while the repository is public. Nothing here publishes it.
- Independence: same session, not independent.

## Verdict

**READY WITH FINDINGS** — R1 and R2, P3, fixed forward. Tier *docs/brand*, one pass. Independence *same session — a
sub-agent of 8e509911*.

The Owner lands this by merging; a merge rules nothing.
