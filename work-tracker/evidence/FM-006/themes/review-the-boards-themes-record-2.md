# Review — FM-006: the board's themes record aligned, and the landing page — the second pass (PR 82)

**date** 2026-09-26 10:52 CEST · **seat** Reviewer · **session** `8e509911/reviewer-22` · **worktree** `shoalmark-review-4`
(branch `themes-review-2` at the tip) · **tier** docs, one pass (P3 fixed forward, P2 sends it back) · **independence**
same session — 8e509911's own sub-agent, reported.

The branch's sessions:
- `4ebd9569`: the GtM seat's `96aa05e`, `f3f994b` and the landing page `9704140`;
- `8e509911`: the merge `a680581`;
- `8e509911/gtm-3`: the re-made ask `7344a78`;
- `8e509911/reviewer-21`: the first pass `ed68f4a`;
- `8e509911/gtm-4`: the alignment `9467b83`.

**Reviewed:** `fm/006-the-board-s-themes` at `970414008bad13ce0e6c0bfb6f14d8635acbcb68`. The branch moved while I
reviewed. Its tip was `9467b83`, the header alignment. At 10:22:41 the GtM seat of `4ebd9569` pushed `9704140` on
top: the landing page. The Principal told me to review both in this one pass.

The words it acts on:
- the Owner's word in chat of 09:23:58, align both themes to the inline header (the Principal's verbatim file);
- his word of 07:41:00 through the Auditor seat: *merging lands the mockups and renders as FM-006's evidence; it rules
  nothing*;
- his landing-page word, quoted in the evidence.

`origin/main` is `a7e5291`: PR 86, 0.18.4, tagged `v0.18.4`. I fixed nothing. This file's findings number from R1; the
first pass's are cited as *pass 1's R1–R5* (`review-the-boards-themes-record.md`, beside this one). Main's
`shoalmark.toml` has no `[paths]`. A verdict's own `review*.md` counts anywhere under `work-tracker/evidence/` (0.18.4's
`--queue`, `own_review`).

## What I checked — the alignment (`9467b83`; `9704140` changes none of its files)

| Check | What I ran | Result |
|---|---|---|
| The alignment against his word | Read `shoalmark.css`. Rebuilt the mocks from the tip and measured the header through Chrome's DevTools protocol (`getBoundingClientRect`, computed styles, 1300 px, both schemes emulated) | `#H` is 874 × 18 at (213, 48) in both themes and both schemes, on the board and behind the dialog; the switch is at (999, 48). The tracker view starts at (213, 62) in both. That is `monochrome`'s layout. In `shoalmark`: the root's `background-image` is `none`, `--chart-top` is 22 px, `--bandink` is empty; the name is in `--ink`, the switch in `--dim`, its brackets in `--mute`. Pixels at the renders' top: ground `#fbfbf7` / `#0d1720`, name `#10202e` / `#d9e4ec`. The site stylesheets, `site-*.png`, `monochrome-*.png`, `monochrome.css` and both scripts are byte-identical to `ed68f4a` and to `f3f994b` ✓ |
| The re-made renders against a fresh rebuild | Ran `python3 shoalmark.py --html-only`, `build-mocks.py --plex` and `render.mjs` into the worktree's ignored `build/`. Chrome could reach no host but 127.0.0.1. The fonts came from the GtM seat's `@ibm/plex-mono-1.1.0.tgz`, checked first: its sha1 `5406e37…` and sha512 `hpsdRxR3…` equal the npm registry's for 1.1.0, and its Regular is `10d3c7fa…`, the repository's own | 6 of `shoalmark`'s 8 renders are byte-identical: the dialog, the foot and the tracker view, both schemes. The two boards differ in 4 % of pixels, all in the *sessions · 25 in the last day* line, which reorders with the clock. The labels match, and no PNG carries metadata ✓ |
| The header's contrast | The tool's `contrast()` on the committed tokens. A meridian is `--grat` composited on the ground | By day / by night:<br>– name and mark 15.96 / 14.01<br>– the switch's word 8.28 / 9.16<br>– its brackets 6.25 / 6.94<br>– hovered: word 14.16 / 10.92, brackets 5.54 / 5.41<br>– on a meridian: at least 5.55 / 6.18<br><br>The lowest of the ten pairs is 5.41 ✓ |
| Pass 1's R1, R3 and R4 | Same function; the harness at 390 × 800; searched the wording | **R1:** 4.504, 4.742 and 4.742 (`#0000008c` on white) match the README's corrected numbers ✓<br>**R3:** at 390 px the page is 503 px wide under `monochrome`, 505 px under `shoalmark` and 905 px on today's board; the tracker view is 390 px in all three ✓<br>**R4:** *wear at most one theme; the ask says which, or none* and *a starter to make yours from if the tool ships themes* ✓ |
| Pass 1's R2 and R5 | Read the README and the tracker | **R2:** noted as the build's in the README's *Not verified*, but not in the tracker's slice A line.<br>**R5:** **still open.** The tracker has neither item 3's order nor item 4's carry-overs, and the commit leaves them to the FM-033 pass. The order's precondition, the 0.18.4 tag, is now met |
| Markers and figures never read (AU-16) | `Accessibility.getFullAXTree` on the fresh mocks. **Control:** the same pages with every `/ ""` alt text removed | `shoalmark`'s switch is named `◐ auto`, with 0 figures and no marker. The control reads `[ ◐ auto ]`, 168 figure strings and the markers. The tracker view reads 0 figures against the control's 168 ✓ |
| The tracker after the alignment | Compared the quote with the Principal's file; hashed the ask blocks | The Owner's word is filed as said in chat at 09:23:58, marked *spelling normalised*; the seat's reading is marked, and it is not an answer. The ask blocks are byte-identical before and after (sha256 `82695957…`, `3b4dd50e…`). The ask is 258 characters; its options are 85, 108 and 84 ✓ |

## What I checked — the landing page (`9704140`)

| Check | What I ran | Result |
|---|---|---|
| Scope | `git diff --name-status 9467b83 9704140`, and the branch against main | 7 paths, all under `work-tracker/`: the tracker, `landing/README.md`, `landing/index.html` and four renders. The branch now has 33 paths, all under `work-tracker/`. The tool, `brand/`, `docs/`, the suites, `CHANGELOG.md` and `VERSION` are untouched ✓ |
| The renders are real | Rendered the committed page in Chrome at 1440 × 900, 1024 × 900, 390 × 1500 and 1440 full page. Google's two font hosts could be reached, every other host could not | Sizes match, and the full page is 5736 px tall in both. 0.21–0.95 % of pixels differ, and a diff mask puts every one at a moving part: the convoys, the open wrecks' shuffle frame, the *press start* cursor, the ticker. The labels are the widths. There is no metadata. No script error at any width, and no sideways scroll ✓ |
| Contrast, as specified | The 49 flat pairs from the CSS (the HUD, panels, register, buttons at 75 % opacity, the foot). The 79 chart texts at 1440 px and 60 at 1024 px against the rendered chart, with text made transparent to get the ground, the CRT layer removed | The flat pairs are at least 5.14 (raised wrecks on the register's zebra), as the README says. Every chart name and figure is at least 4.65 at its median pixel. The water names pass without their halo ✓. As drawn, see R3 |
| The 23 wrecks against `origin/main` | Parsed the page's `WRECKS`. Compared each one with `a7e5291`'s front matter and `# ` line, and with `git log --diff-filter=A` (Europe/Berlin) | The 23 are exactly the trackers tagged `bug` or `security`, out of 37. For every wreck, status, incident ID (the filing commit), filing day and link match main. The statuses are 12 Shipped, 8 In Progress, 2 Proposed and 1 Closed, and the counts 10 / 12 / 1 hold ✓. One title is capitalised, and some reports are condensed (R4) |
| `v0.18.4` | The HUD, the foot's link, the fine print, the README's source row | The fine print is `CHANGELOG.md`'s 0.18.4 headline. `v0.18.4` is a lightweight tag on `a7e5291` (09:58:57) ✓ |
| The page's other facts | `docs/index.md`, `README.md`, `labels.yaml` and `zensical.toml` on main | Each fact matches its source:<br>– 12/15 and 10/37, with their counting note and the answer of 11:07<br>– 200 pull requests in 22 days, 85 % within a minute, none reviewed; the three agents<br>– `--answer AP-007 accept`, FM-026 and *ten minutes*<br>– `llms.txt`, which `scripts/llms_txt.py` writes at the site's root<br>– the links' `.html` form (`use_directory_urls = false`)<br>– the claim, which is `labels.yaml`'s footer ✓<br><br>The Owner's words are marked as chat, normalised, and not an answer. They are not in the repository, so their fidelity is unverified |
| Reading and motion | The accessibility tree; two full-page captures 7 s apart under reduced motion | 23 wrecks are focusable buttons, each named with its number, status and title. The canvas carries its description. No figure is in the tree. Under reduced motion the page does not move: the two captures are identical, across the console's 6 s cycle ✓ |
| Secret screen | The diff's text by hand | The only hosts are `github.com/holgo99/shoalmark` and `holgo99.github.io`, both in `zensical.toml`, and Google Fonts, which the README discloses. There is no email, key, path, address, parent name or client name ✓ |
| The tracker's additions | Read them; diffed against `origin/main` | They are one line in *What is true now*, a section, and a ship-log row, which sits on top. They are marked as chat words, and say nothing is built and nothing is asked, consistent with the one-ask rule. Front-matter lines 1–17 are identical to `a7e5291`'s. Against main the tracker only gains lines. INDEX.md is main's ✓ |
| Gates on `9704140` | 10:39–10:51 CEST, no `TZ=UTC` | – `--check`: exit 0 (*INDEX.md is up to date — 37 trackers*, freeze *21 open*, the Owner's two sections guarded)<br>– `--session-check`: exit 0<br>– suites: `test_shoalmark.py` 456 and `test_core.py` 148, green on 3.14.3 and 3.9.6, 0 skipped<br>– `git merge-tree --write-tree origin/main HEAD`: clean, tree `ad95c4a`, which is main plus the 33 paths<br>– main's own `--check` on that tree, exported without git: output byte-identical to main's own export (the control) ✓ |

## Findings

**R1 (P3) — *v0.18.4 is not tagged* is no longer true, and the tracker now contradicts itself.**
- *Why it matters:* the record states it in the present tense, and the tag is the build's precondition: his word of
  07:41:00 orders the build *after FM-037 and the 0.18.4 tag* (pass 1's R5).
- *The gap:* the sentence stands in the README's *Auditor seat's counsel* and in the tracker's bullet of that name.
  Meanwhile the landing section of the same tracker says *The release is v0.18.4*. `v0.18.4` is on origin at
  `a7e5291` (PR 86, 09:58:57), later than the alignment commit (09:40:25).
- *What closes it:* in both places, *not tagged when filed; tagged at `a7e5291` (PR 86)*.
- *Confidence:* 95 %.

**R2 (P3) — the seat's reading says *every board view*; the tracker view shows no header.**
- *Why it matters:* the brief asks whether this squares with *all dashboards aligned over all themes*. It squares with
  *aligned*: the two themes lay out every view alike, and today's board hides the header there too, because `#H` sits
  inside `#B`, which the view hides (measured). It does not square with every view carrying the inline header.
- *The gap:* the reading in the tracker and in the README says *in both themes and every board view*. Only the
  ship-log row says the tracker view shows no header. A header there would be markup (`#H` out of `#B`, a
  `shoalmark.py` hook) and is in neither slice.
- *What closes it:* the reading and the README's header bullet say so, and name that hook for the FM-033 pass.
- *Confidence:* 45 %. His later chat line, *"9467b83 - perfect"*, suggests he is content. It is a chat word and not an
  answer (path 5), and the record's wording stays the seat's.

**R3 (P3) — the landing page's contrast claim holds for the specified colours, not as the page draws them.**
- *Why it matters:* the README and the tracker say every text pair is at least 4.5:1 *on the ground it sits on*,
  including *the chart's names and figures*. His later chat word adds a landing page requirement to v0.18.5, so its
  build will lean on this claim.
- *The gap:* the CRT layer (`.crt`, z-index 6) lies over the chart's names (z-index 4) and figures (z-index 5). Its
  vignette, up to 45 % black at the corners, and its scanlines darken the text and its ground alike. Measured
  pixel-true (the layer's darkening taken from the ground with and without it):
  - at 1440 px, 12 of the chart's names and figures fall below 4.5 at their median pixel;
  - the figures near the corners read 2.68–4.43;
  - `OSTFRIESLAND`, `BUTJADINGEN`, `LAND WURSTEN`, `DITHMARSCHEN` and `Norddeich` read 3.54–4.41;
  - at 1024 px, 5 fall below;
  - two more cases: `54°10'N` lies under the title's backdrop at 1.2, and `53°50'N` on the east edge crosses the
    coastline.

  The wreck labels (z-index 7) and the title (z-index 8) sit above the layer and pass.
- *What closes it:* the README and the tracker say the pairs are the specified colours and name the overlay's effect.
  Or the page lifts the names and figures above the layer, and they are re-measured.
- *Confidence:* 80 %. The method is mine; the numbers at the median pixel are robust.

**R4 (P3) — the wrecks' reports are condensed, not cut.**
- *Why it matters:* the README's source table says *the tracker's `hook:`, cut to its first sentence or two, code spans
  kept*, and a reader takes a cut as the tracker's own words.
- *The gap:* five reports drop clauses inside a sentence with no mark:
  - FM-014 drops *moves an answered exchange into the body and*;
  - FM-021 drops its middle sentence;
  - FM-033 drops its lead;
  - FM-035 is condensed;
  - FM-036 turns *for FM-030 — …* into *for one tracker*.

  FM-037's title and report are capitalised against main's `# ` line. Each keeps its meaning.
- *What closes it:* *condensed from its `hook:`*, or the cuts marked `…`.
- *Confidence:* 65 %.

**Still open from pass 1:**
- **R5.** The 07:41:00 word's order and carry-overs are not in the tracker. It is left to the FM-033 pass.
- **R2.** It is carried to the build from the README only.

Not findings:
- The register's 23 *on the chart* buttons share one name. The key's five sprites are unnamed images. The README says
  a screen reader was not tested.
- The dark brackets pair is 6.9448: the README gives it as 6.95 for the brackets and as *to 6.94* for the figures.
- The commit message's *109 figure strings*: my control reads 168. It is not in the record.
- *The board's palettes are unchanged since 2026-09-25* while `--bandink` is gone. The sentence is qualified by
  *counted with its header on the band*.

## Verdict

**READY WITH FINDINGS** — R1–R4, all P3, fixed forward; no P2.

- The alignment is what his word asks. `shoalmark`'s renders match a fresh offline rebuild, and the header's pairs are
  5.41:1 or more.
- The landing page stays inside `work-tracker/`, and its renders are the committed page's.
- Its 23 wrecks match main, and its `v0.18.4` is right.
- Its pairs hold as specified. As drawn under the CRT layer, 12 chart texts do not (R3).
- The ask, the front matter and main's text are unchanged.

*The Owner lands this by merging, and a merge rules nothing (path 5).*
