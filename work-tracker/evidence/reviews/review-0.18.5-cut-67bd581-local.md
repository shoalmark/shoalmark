# Review — the 0.18.5 cut at 67bd581, the same-session pass extended to the fixes of R1–R5 (2026-09-27, Reviewer, session `8e509911/reviewer-37`)

- **Date:** 2026-09-27, 00:50–01:32 CEST.
- **Seat:** Reviewer (Opus 5.5, highest effort), a sub-agent of Principal session `8e509911`; the seat of the pass on
  `0612dfe` (`review-0.18.5-cut-0612dfe-local.md`, `35f67aa`, READY WITH FINDINGS).
- **Session:** `8e509911/reviewer-37`.
- **Worktree:** `shoalmark-review-3`, detached at the tip; the suites and the gates ran here, the tree clean after each.
  Builds and renders ran in the session's scratchpad (the scratch clone of `origin` moved to the tip, and the stages of
  the pass on `0612dfe`). The Owner's checkout, `shoalmark-gtm`, every other worktree and every folder of session
  `8b91dba2` stayed outside every command.
- **Tier:** *code — a release, critical*, the full loop: NOT READY on any P2, with the fix named.
- **Independence:** *same session — a sub-agent of 8e509911; the cold session follows*. The two commits are
  `8e509911/implementer-39`'s. Reported as such, not independent.
- **Clock:** between 00:00 and 02:00 CEST, so the gates and both suites ran with `TZ=UTC` (FM-028), and the verdict
  commit is made with it.

**Reviewed:** `release/0.18.5` at **`67bd581f6bb8bc8f8393548ac1f5d19648d0764e`** (pushed 00:49:22; ls-remote 00:50),
two commits on this seat's verdict `35f67aa`: `69552ed` (the release's day; R1, R2, R3, R5) and `67bd581` (R4).
`origin/main` is `bef2a1e`, an ancestor. No pull request is open.

## The findings of the pass on 0612dfe

| # | Finding | How I checked it | Now |
|---|---|---|---|
| R1 | Two of his chat words quoted altered, unmarked | the CHANGELOG's two quotes against `owner-words-2026-09-26-0923.md` and `-1025.md`, word by word | **09:23:58:** *For the Dashboard i prefer this "inline header" (Soalmark logo + light/dark switch) variant … over this variant used in the dar mode, where the header sits outside the graticule. … Align for both.* — the file's words and spelling exactly, *used in the dar mode* included; the two `[Image #86]`, `[Image #87].` cut at `…`, and the quote says so (*verbatim, the two screenshots' references cut at `…`*). It ends at *Align for both.*, a whole sentence. **10:25:41:** marked *spelling normalised*; *requirment → requirement*, *re-style → restyle*, *re-brand → rebrand*, *`shoalmark`s → `shoalmark`'s*; *that goes* restored, the backticks kept. **Closed.** |
| R2 | FM-033 in *Trackers touched* | the list against `git diff --name-status v0.18.4 67bd581 -- 'work-tracker/*.md'` and `git log` on each file | The list now reads FM-002 and FM-006 built; FM-031, FM-038, FM-039 open lines; FM-034, FM-035, FM-036 *by the passes' `fix` rows only*. The trackers changed since `v0.18.4` are exactly these eight; FM-034 to FM-036 by `8f98103` alone, the same-day pass's `fix` rows. FM-033 is named once, in *Also since*, as the rule the pass applied. **Closed.** |
| R3 | Slice A's R1 and R2 unfixed | the *Rebuild*'s pins against the blobs; the new `foot` mode read; the foot re-rendered with the committed `render.mjs … foot` from this pass's own stage built at `361336a` | *Before* is `2a9f7eb`, *after* `70fedd3`, both in a clone at `361336a`: `70fedd3`'s two files are `361336a`'s blobs (`eb66694f`, `2be1a93a`), and the release carries `docs/stylesheets/shoalmark.css` byte for byte (`2be1a93a`). The earlier pass rebuilt the 16 committed renders this way (12 identical, 4 in the clock's band or one antialiased word). **The two foot renders re-render at 0 px** (1440×240, both schemes), IHDR/IDAT/IEND only; seen: *Made with Zensical*, its link in the band's ink, by day and by night. `requests.json` gains their two lines, the rest kept. The mock's foot is not rendered; its measure stands in slice A's table (1.12 → 13.69:1) — what the finding named as enough. **Closed.** |
| R4 | The start page as it ships in no committed render; its README read v0.18.4 | `uvx zensical build` at `67bd581` (its `docs/` and `overrides/` are `69552ed`'s); slice L's committed `render.mjs` on it; the nine page renders compared | **Reduced motion, 1440/1024/390: 0 px.** First screens with motion: 1440 and 1024 0 px, 390 79 px (moving parts). Whole pages: 1440 0 px; 1024 and 390 one 8-px band each (4,904 and 2,310 px, y 6263 and 10686: the ticker). Heights equal: 5837, 6459, 11025. IHDR/IDAT/IEND only. The README's row (a) reads v0.18.5, *released 27 September 2026*, naming `522db92` and `69552ed`; the renders' section names `69552ed` and the heights; *Checked* says `checks.json` is `cb49101`'s and not re-run — the earlier pass's run at `0612dfe` read the same summary but the height. **Closed.** |
| R5 | `NOTICE` silent on the Plex fonts | `NOTICE` read; its words against `brand/themes/*/fonts/LICENSE.txt` and the themes' README | *This product bundles IBM Plex Mono (brand/themes/\*/fonts/, the Latin-1 cuts of @ibm/plex-mono 1.1.0, unmodified), Copyright 2017 IBM Corp., with Reserved Font Name "Plex", under the SIL Open Font License 1.1 — the licence is in each brand/themes/\*/fonts/LICENSE.txt*: the licence file's first line, the package and version the README pins, in the form of the `marked` line above it. `NOTICE` is one of `TOOL_FILES`, so every vendored copy carries it. **Closed.** |

## The rest of the extension

| Check | How | Result |
|---|---|---|
| The release's day, in both places and in no third | `git grep` for `2026-09-27`, `27 September`, `released 2[67] September` and `## 0.18.5` over the repository, then the trackers | `CHANGELOG.md:5` `## 0.18.5 — 2026-09-27` and `overrides/landing.html:466` *released 27 September 2026*; the built page carries it once. No third place names the release's day: the other 26 September lines are facts of that day (his words and answer, the finding, the passes, *the release: read at its cut, 26 September 2026*, the wrecks' reading), and the mock and `cb49101`'s `checks.json` under `evidence/` keep what they recorded. ✓ |
| What the two commits change | `git diff --name-only 0612dfe 67bd581` outside `work-tracker/evidence/` | `CHANGELOG.md`, `NOTICE`, `overrides/landing.html` — nothing else. The word diff of the three shows only the date, R1, R2 and R5. ✓ |
| The tool and the suites | `git diff --stat 9704145 67bd581 -- shoalmark.py test_shoalmark.py test_core.py lefthook.yml scripts .github shoalmark.toml brand` | Empty: byte-identical to slice B's verdict tip; `VERSION` is the cut's 0.18.5. ✓ |
| Gates, under `TZ=UTC` | `--check`, `--session-check`, `--queue` | `--check` **0** (*INDEX.md is up to date — 39 trackers*; *judged before build: on*, 28 commits; *the Owner's two sections: guarded*, 32 commits). `--session-check` **0**. `--queue`: `release/0.18.5 @ 67bd581  wait: no pull request — no verdict on 67bd581`. ✓ |
| The site | `uvx zensical build` (0.0.65) here and in the scratch clone at the tip | *No issues found*; the start page names `v0.18.5` three times and *released 27 September 2026*; no built page names `v0.18.4`. ✓ |
| merge-tree | `git merge-tree --write-tree origin/main 67bd581` | Clean, exit 0 (`db72f56d`). ✓ |
| Both suites, `TZ=UTC`, one interpreter at a time, each started at load < 6 with no other suite running | `/usr/bin/python3` then `python3`, each `test_shoalmark.py` then `test_core.py`; `uptime` logged | **3.9.6** (01:11–01:20, load 3.65 → 3.66): `test_shoalmark.py` **481 ok**, `test_core.py` **148 ok**. **3.14.3** (01:20–01:30, load 3.60 → 3.25): **481 ok**, **148 ok**. Each run *skipped here: 0 checks — every check ran*, *all green*, exit 0; FM-035's healthy-board case *ok* on both. Before them another session's suites in `shoalmark-principal-4` ran, and I waited until none was running. `git status` empty after each. ✓ |

## Findings

None at P2 or P3. R1–R5 of the pass on `0612dfe` are closed, each shown by its source, a render or a run.

Noted, not findings:
- Slice L's *Rebuild* now stages `69552ed`'s site as the page, so re-running its `checks.mjs` line writes the release's
  `checks.json`, not the committed `cb49101` one; the README says the committed file is `cb49101`'s.
- The fine print reads *released 27 September 2026* beside *the release: read at its cut, 26 September 2026*: both true
  if the Owner tags today. A tag on a later day moves the same two lines again.
- `git diff --check` still flags only the two CRLF `LICENSE.txt` files, IBM's verbatim.

## Not verified

- The tag's five-job CI matrix, Windows in particular; a vendoring from the `v0.18.5` tag.
- Firefox, Safari, print, a real phone (390 px is Chrome's device metrics), a screen reader; the site live.
- Independence: same session, not independent.

## Verdict

**READY** — tier *code — a release, critical*; independence *same session — a sub-agent of 8e509911; the cold session
follows*. Every item of the cold checklist held at `0612dfe` (`35f67aa`), and the two commits since change only the
release's day, the five findings' text, `NOTICE` and evidence, each verified above; the tool, the suites, the gates and
the hooks are byte-identical.

**Confidence that the cold session finds no P2: 80%.** For: every checklist item ran and held; the board he approved at
16:06 renders byte for byte; the starters and a consumer's board differ from their references only by the marked
placeholder and the version digit; the committed renders re-render at the tip; the day matches a tag made today; both
suites green on both Pythons. Against: what no local run proves — the CI matrix on Windows and macOS, other browsers;
a cold reading of *nothing changed or added* against the landing page's four marked edits, which the record shows and
the Principal's brief allowed, R3 marked his to strike, none of them ruled by him; the two west-edge figures under the title at 1440 px
(1.30 by the seat's method), which slice L's pass judged covered, decorative text; and a tag on another day than today.

The Owner lands this by merging; a merge rules nothing.
