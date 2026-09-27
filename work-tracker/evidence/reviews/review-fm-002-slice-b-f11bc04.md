# Review — FM-002 slice B, pass 1 (items 1–2): the tool ships `monochrome` and `shoalmark`, and the board's three hooks (2026-09-26, Reviewer, session `8e509911/reviewer-35`)

- **Date:** 2026-09-26, 17:25–19:35 CEST.
- **Seat:** Reviewer (Opus 5.5, highest effort), a sub-agent of Principal session `8e509911`.
- **Session:** `8e509911/reviewer-35`.
- **Worktree:** `shoalmark-review-5`, detached at the tip. The suites and the gates ran here, and the tree was clean
  after each run. Every build, render, mutation and the npm download ran in the session's scratchpad: two scratch clones,
  and three tool exports (main, `f11bc04`, `9f2f525`). The Owner's checkout, `shoalmark-gtm`, every other worktree and
  every folder of session `8b91dba2` stayed outside every command.
- **Tier:** *code*, the full loop, as the judging pass gave slice B (`13d70189`, on main since PR 93). A P2 sends it back
  with the fix named. **Not critical** (check 1): no gate, hook or release change, so the loop stays inline.
- **Independence:** same session — a sub-agent of 8e509911, reviewing its Implementer sub-agent's branch
  (`8e509911/implementer-37`). Reported as such, not independent.
- **The Owner's rule for this build, as the Principal relays it:** *the mocks are taken as-is, nothing changed or added.*
  Every difference from the mocks is judged below. An unmarked one is a P2.

**Reviewed:** `fm/002-slice-b-the-tool-ships-themes` at **`9f2f52506ec9fe0e125d1be0d1267cae5c109565`** (committed
18:26:19, pushed 18:41, ls-remote 19:32:06). The pass began on `f11bc04` (17:25) and folds in `9f2f525` as the
Principal asked, so four commits on `origin/main` are judged: `919eb86` the three hooks, `cd1c33f` `brand/themes/`,
`f11bc04` the merge of main `bef2a1e`, and `9f2f525` the Principal's two rulings (the mock's stripes kept, with hook 3
left unused and named; `owner.title` *für den Eigner*). `9f2f525` changes no `shoalmark.py`, so checks 1, 4, 5, 8 and
10 hold for it unchanged. Checks 2, 6 and 9 were re-run on it. Items 3–5 (`--from`, `--vendor`, the README and CHANGELOG,
the record) are not built at this tip and are not judged here. No pull request is open for the branch.

## The checks

| # | Check | How | Result |
|---|---|---|---|
| 1 | Not critical | `git diff origin/main...9f2f525 -- lefthook.yml scripts/ .github/`; the `shoalmark.py` hunks against the functions they sit in | The gate paths: empty. `shoalmark.py` changes in 5 hunks, all in `HTML_PAGE` (the CSS, the markup and `draw()`) and in `LABELS` (one key). No `def` line is touched. These are unchanged: `triage_reading`, `build_judgement` and `commit_msg_check` (`judged_before_build`), `guard_walk`, `triage_pending`, `commit_msg_hook` and `triage_guard` (FM-037's guard and walker), `lint` (`--check`), and `queue_actions`, `queue_lines` and `queue_cmd` (`--queue`). `test_core.py` is unchanged. ✓ |
| 2 | Each `theme.css` against its mock, byte for byte, at `9f2f525` | `git show 9467b83:…/FM-006/themes/{monochrome,shoalmark}.css`, the same blobs as main's and the tip's (`580a1d99`, `62713a71`); the starter with its own header (`/* THE STARTER …*/`) removed; `diff` against monochrome.css, and against monochrome.css + `\n` + shoalmark.css (build-mocks.py's order) | **monochrome:** 7 hunks. **shoalmark:** the same 7, plus hook 1's magenta line and one comment. Each is marked `SLICE B` on its own line or in the comment right above it: (a) the two cuts' urls `brand/fonts/` → `fonts/`, and the Regular's `@font-face` added; (b) `::placeholder{color:var(--mute);opacity:1}`, *not the mock's*, which is slice A's rule; (c) hook 1, `#p::before{content:…}` → `#p>.pt{display:block;…}`, and in shoalmark its magenta line; (d) hook 2, the lift `#B:not([hidden]):has(#f:not(:empty)) ~ #r{margin-top:-21px}` → `#B:not([hidden])~#F{display:grid}` and the grid, plus one mock comment line with `(SLICE B: …)` added; (e) in shoalmark, a comment above the mock's `tr.t:nth-child(even)` rule, which is now kept verbatim, naming hook 3 as unused. The rest of each mock is verbatim, its headers included. `9f2f525` changes monochrome's starter header only; its rules are byte-identical to `f11bc04`'s. **Unmarked differences in the text: 0.** The suite pins this exactly (the `_EDITS` table: header + mock + the listed edits, 6 and 8 `SLICE B` marks), and fails on a one-character change (check 5). ✓ |
| 3 | The fonts, the licence, the README | the npm tarball of `@ibm/plex-mono` 1.1.0, downloaded into the scratchpad; sha1 against the registry's `dist`; sha256 of `fonts/split/woff2/*-Latin1.woff2`; the blobs against slice A's | Tarball sha1 `5406e372…`, the registry's. **Regular `10d3c7fa…`, SemiBold `1ce95cff…`, Italic `08c4566f…`**: the package's, the same blobs as slice A's `work-tracker/brand/fonts/`, identical in both themes. `LICENSE.txt` equals the package's (`7e6b2818…`). `brand/themes/README.md` has one sentence each, and the three files by name and sha256. `labels.yaml` is untouched. ✓ |
| 4 | **The default board renders as before** | main's tool and this tool, each exported whole, built on one scratch clone of this repository (`--html-only`, the person's place empty). Three boards: this repository's own (its brand), no brand at all, and a claim only (`labels.yaml` with `footer:`). Four views: the board, a search (`#FM-00`), a tracker (`#=FM-002`), and the acts dialog. 1300 and 390 px, light and dark, full page, through Chrome's DevTools protocol. The pages' tool paths made equal. `cmp`, then `compare -metric AE` | **48 of 48 pairs byte-identical.** No clock line differed. The pages differ only in the three hooks, the default CSS line and the label table. The generated `view/` is identical. A hidden `.pt` as `#p`'s only child adds no pixel either: `#p` was set to it on a search view, 8 of 8 renders byte-identical. The suite's own check agrees: a board with the themes in the tool's `brand/` is byte for byte the board of a copy with no `brand/`. ✓ |
| 5 | The new checks fail without what they guard | a scratch clone at `f11bc04`, with `919eb86`'s `shoalmark.py` hunk reverse-applied and one character of an unmarked monochrome rule changed (`#p>b` weight 600 → 700); `test_shoalmark.py` on 3.14 | **9 FAIL**, each by name: the three FM-002 hook checks (the markup; *no visible change*, where the undo finds no hooks; *a theme styles each hook*); *each starter is FM-006's mocks …* (from the one character); the two 0.18.2 running-line checks, which read it inside `#F`; the two C4 German checks, since `owner.title` is no longer a label. The ninth, FM-035's *healthy page* half, is load: it has a 5 s Chrome budget, and it overlapped my renders. It passed in every clean run (check 9). ✓ |
| 6 | The hooks with a theme: each starter against its mock | FM-006's `build-mocks.py` (unchanged since `9467b83`) on main's build of this repository's board, `--plex` the npm cuts; each `9f2f525` starter worn from the person's place (`XDG_CONFIG_HOME`), built by this tool on the same clone. The mock pages' data line (`HOME`) was taken from the starter pages' build, so the sessions list, which the clock re-orders, is the same on both. Five views: the board, search, tracker, the acts dialog, and group-by (`#g` clicked once, *by story*). 1300, 1000 and 390 px, light and dark, full page | **Every page height is equal. Tracker view: 12 of 12 identical.** Board: 313–420 px in each theme, all in the search box: the placeholder (b). The dialog adds its note's placeholder (1,620–2,161 px in total). **The stripes are the mock's: 0 px** (at `f11bc04`, `tr.zebra` differed by 266,939–364,075 px; R4). The foot is identical: hook 2 puts the claim and the running line on one line, as the lift did. **Search and group-by views: the Owner's box's title,** 834–1,268 px (monochrome) and 3,148–3,651 px (shoalmark): R2. |
| 7 | The starters on a board with no brand | the bare board, each starter from the person's place, 1300 px, viewed beside the mock | `shoalmark` sets every token it uses in both schemes. It reads as the mock, except the header, which shows the name where this repository has its wordmark. `monochrome` adds tokens only and keeps the board's palette (its header: *lines added to …/theme.css*). On a board with no brand that is the tool's default grey, not the site's palette of the mock's page. As-is, it is a mock written that way. Noted, not rowed. |
| 8 | **Slice A and slice B together** | `git merge-tree --write-tree` against `origin/main` and against `origin/fm/002-slice-a-the-brand-layer` (`b9644b7`); then slice A's `work-tracker/brand/` (theme.css and its two cuts) on the scratch clone, built by main's tool (= slice A's; it changes no code) and by this tool, rendered as in check 4, plus a probe of `#f` and `#r` | merge-tree is **clean both ways**. The rendering is not: R1. With slice A's theme, the board and search pages grow 41–81 px at every width and in both schemes. Above the chart's lower edge, the page is identical: slice A's title and its `nth-child` rows still render. The tracker view is identical (6 of 6). |
| 9 | Gates, at `9f2f525` | this worktree at the tip; `uptime` logged around each suite | At `f11bc04`: `test_shoalmark.py` **470 ok** and `test_core.py` **148 ok** on **3.14.3** and on **3.9.6**, *skipped here: 0 checks*, *all green*. At `9f2f525`: 3.9.6 **470 + 148**, all green, 0 skipped. 3.14.3 **148**, and **469 of 470** twice (1-minute load 5–7 and 6–9): the one failure is FM-035's healthy-board case, whose Chrome budget is 5 s. That case, run alone as the suite builds it, fails the same way on `main` and on `f11bc04` at load 12–20, and passes at a 60 s budget. **Re-run at load 3.9, it passed 2 of 2 on this tip.** Its code and `shoalmark.py` are byte-identical between `f11bc04` and `9f2f525`. Counted green. The worktree was clean after every run. `--check` 0 (*judged before build: on*, every build commit under a judged In Progress tracker; *the Owner's two sections: guarded*). `--session-check` 0. `--queue`: `fm/002-slice-b-… @ 9f2f525  wait: no pull request — no verdict on 9f2f525`. merge-tree clean against `origin/main` (`bef2a1e`) and against slice A (`b9644b7`). ✓ |
| 10 | The suite's fix | `test_shoalmark.py`'s FM-002 block, main against the tip | At main, the organisation checks wrote into the tool's `brand/` and removed it whole (`shutil.rmtree(org)`). With `brand/themes/` committed there, every suite run, and so every commit's hook, would have deleted the themes. Now `_org_clear()` unlinks exactly `BRAND_FILES`, the only names `board_with()` writes (`org_<file>`). The `finally` does the same, and it removes the folder only if the run created it and left it empty. Every suite run here left `git status` empty and `brand/themes/` whole. **Sound.** ✓ |

## Findings

**R1 · P2 · confidence 90% · Slice A and slice B together break shoalmark's own board's foot. The claim falls off the
band onto the chart, at 1.74:1 by day.**
- *The gap:* slice A (`b9644b7`, READY WITH FINDINGS, waiting to land with this one) dresses this repository's board with
  the shoalmark mock as `work-tracker/brand/theme.css`, and keeps its three workarounds *for slice B's hooks*. Hook 2 moves
  `#f` out of `#B` into `<footer id="F">`, so workaround 2, `#B:not([hidden]):has(#f:not(:empty)) ~ #r{margin-top:-21px}`,
  matches nothing. The running line is no longer lifted onto the claim's line.
- *Seen:* slice A's theme with slice A's tool puts `#f` and `#r` both at y 2639–2660 on the band. With this tool,
  `#f` stays at 2639–2660, in `#F`, on the chart's ground, in `--footink` `rgb(180,195,209)`. That is **1.74:1 on
  `#fbfbf7` by day** (10.05:1 by night). `#r` drops to 2720–2741, alone on the band. The page grows 81 px at 1300 and
  41 px at 1000 and 390, in both schemes, on the board and on a search. Workarounds 1 and 3 still render.
- *Why it matters:* the Owner approved slice A's renders at 16:06. The two land together, and in either order the second
  merge changes his board's foot, and one of its texts falls below 4.5:1. merge-tree cannot see it.
- *What closes it:* in this branch, with slice A merged in (its tip, or main once it lands), the repository's own theme
  takes hooks 1 and 2. Replace slice A's `WORKAROUND 1 of 3` and `2 of 3` rules in `work-tracker/brand/theme.css` with the
  starter's hook rules, keeping workaround 3's `nth-child` as the starter now does, so it renders as
  `brand/themes/shoalmark/` does. Re-render its foot against slice A's approved renders, and add a check that the
  repository's theme lifts nothing. Also: the 0.18.5 CHANGELOG line (item 4) says the claim moved out of `#B` into `#F`, so
  a consumer's theme that placed the running line by `#B`'s sibling knows.

**R2 · P2 · confidence 70% · Hook 1 changes the mocks off the board view: the Owner's box stands untitled on a search
and on any grouping but the board.**
- *The gap:* `draw()` writes `<span class="pt">` only when `gname=="board"&&!q`. On a search or a grouping by story or
  status, `#p` is empty, but both mocks still draw it as a box (`padding:18px 2ch 12px;border:1px solid`). The mock's
  `#p::before` titled it *owed to the owner* wherever it stood. The starter's box has no title, and in shoalmark it is an
  empty magenta frame.
- *Seen:* 12 of 12 search and group-by renders per theme, all at `#p`'s top border. This is not marked, and not in
  `cd1c33f`'s or `9f2f525`'s lists of differing pixels. Their renders were the board, a tracker, the dialog and a board
  with no claim.
- *What closes it:* write the `.pt` span wherever `#p` is drawn: move it out of the `gname=="board"&&!q?` condition, one
  line in `draw()`. The default is unchanged: check 4 renders a lone hidden `.pt` byte-identical. Add a render check on a
  search view. If the Owner would rather have no box there, that is his ruling, not the mock.

**R3 · P3 · confidence 85% · `--brand` now reports an organisation place that holds nothing.**
- *The gap:* `brand_places()` takes a place when it is a directory. `brand/themes/` makes the tool's `brand/` one. In this
  repository `--brand` now prints `organisation  <tool>/brand` above the repository (main: the repository alone), while
  every source line still says `repository`. Once item 4 vendors `brand/themes/`, every consumer that chose nothing reads
  an organisation place in its report. The board is unchanged (check 4).
- *What closes it:* the report lists a place only when it holds one of `BRAND_FILES`, or marks it *nothing here*. Fixed
  with items 3–5.

**R4 · P2 at `f11bc04`, closed by `9f2f525` · confidence 95% · The shoalmark starter's stripes were not the mock's.**
- At `f11bc04`, `tr.zebra` striped every other row of a group, while the mock's `tr.t:nth-child(even)` tints every row of a
  group or none. The difference was 266,939–364,075 px on every board, search and dialog render. `9f2f525` keeps the
  mock's rule verbatim, with a marked comment naming hook 3's one line. Check 6 shows 0 px of stripe difference. The class
  stays in the markup, and the hooks check still styles it with its own fixture theme. **Closed.**

**R5 · P3 · confidence 70% · The German board now names the Owner two ways: *für den Eigner* in the box's title,
*Auftraggeber* in three of its other labels.**
- *The gap:* `9f2f525` takes `owner.title: für den Eigner` from the German site (*Für den Eigner.*, `docs/de/triage.md:3`,
  `docs/de/signing.md:3`). `docs/de/` says *Eigner* on 21 lines, and the German claim carries it: *Dein Eigner bremst*, which FM-006
  records the Owner ruling in chat on 2026-09-23. `examples/de/labels.yaml` says *Auftraggeber* on lines 47, 67 and 70 (`waiting.detail`,
  `viewer.intent.missing`, `viewer.answer`). That predates this slice, and those lines render on the same board as the
  new title. `ADOPT.de.md` and `examples/de/TRIAGE.md` say *Owner*.
- *My recommendation:* the board's labels should agree with each other before they agree with the site, since a German
  Owner reads them on one screen. Of the two words, *Eigner* has the site and the claim FM-006 records him ruling behind it, and *Auftraggeber*
  only an earlier seat's translation. So keep *für den Eigner*, and in this slice's item 5 (the German labels) move the
  three *Auftraggeber* lines to *Eigner* (*beim Eigner*, *der Eigner nennt sie*, *die Antwort des Eigners*), with the
  fixture in `test_shoalmark.py`. The file then has one word for the Owner, the site's. If the Principal holds that a
  slice changes no word it did not bring, the consistent alternative is `owner.title: für den Auftraggeber`, with the
  board-and-site split as one line in FM-002 for the Owner. Either way, not the split this tip ships. Fixed with items 3–5.

Noted, not findings:
- `brand/themes/README.md` and each starter's header name `--brand DIR --from`, which is item 3 and not built at this tip.
  That is right once items 3–5 land in the same pull request.
- `.pt` is a real element now, so a screen reader reads the box's title where a theme shows it. With no theme it is
  `display:none` and read by none. `<footer>` adds one contentinfo landmark and no pixel.
- Hook 3 (`zebra`) ships in the markup with no shipped theme using it, as the Principal's ruling says. The shoalmark
  starter names its one line.

## Not verified

- Items 3–5: `--brand DIR --from`, `--vendor` carrying `brand/themes/`, the README's brand section (≤ 25 lines), the
  CHANGELOG, the ship-log row and FM-002's clause. None is built at this tip. The board *with `--from shoalmark`* was
  emulated by the person's place (check 6), not run.
- The answer dialog under a theme: no ask is open on today's board, so the acts dialog stood in.
- Firefox and Safari; print; a real phone (390 px is Chrome's device metrics); a screen reader.
- Independence: same session, not independent.

## Verdict

**NOT READY** — R1 and R2 are P2, each with its fix named above. R4 was P2 at `f11bc04` and is closed by `9f2f525`. R3 and
R5 are P3, fixed with items 3–5. Tier *code*, the full loop. Independence *same session — a sub-agent of 8e509911*.

The Owner lands this by merging; a merge rules nothing.
