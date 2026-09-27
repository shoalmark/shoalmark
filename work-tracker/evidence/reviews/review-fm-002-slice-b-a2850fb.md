# Review — FM-002 slice B, pass 2: items 3–5 and pass 1's fixes (2026-09-26, Reviewer, session `8e509911/reviewer-35`)

- **Date:** 2026-09-26, 20:42–21:25 CEST.
- **Seat:** Reviewer (Opus 5.5, highest effort), a sub-agent of Principal session `8e509911`.
- **Session:** `8e509911/reviewer-35`, the seat of pass 1 (`review-fm-002-slice-b-f11bc04.md`, `6bb2ab3`, NOT READY).
- **Worktree:** `shoalmark-review-5`, detached at the tip. The suites and the gates ran here, and the tree was clean
  after each run. Every build, render and vendoring ran in the session's scratchpad: one scratch clone at the tip, the
  tool exported at main and at the tip, and one consumer repository. The Owner's checkout, `shoalmark-gtm`, every other
  worktree and every folder of session `8b91dba2` stayed outside every command.
- **Tier:** *code*, the full loop (`13d70189`). **Not critical** (check 1), so the loop stays inline.
- **Independence:** same session — a sub-agent of 8e509911, reviewing its Implementer sub-agent's branch
  (`8e509911/implementer-37`). Reported as such, not independent.
- **The Owner's rule:** *the mocks are taken as-is, nothing changed or added.* An unmarked difference from a mock is a P2.
- **The machine's load, as the Principal set it (19:5x):** one interpreter at a time, each suite started at a 1-minute
  load under 6. Each render and build ran only after the four suite runs had finished.

**Reviewed:** `fm/002-slice-b-the-tool-ships-themes` at **`a2850fbc5de5c2ed0f3342882304ff537b2a7c14`** (committed
20:39:39, pushed 20:41:06; ls-remote 21:21:04). Two commits are new since pass 1 (`6bb2ab3`). **`d111ab1`** merges slice A
at `b9644b7e`: its tree is exactly `git merge-tree --write-tree 6bb2ab3 b9644b7e` (`3a019083`), so it carries no hand
edit. **`a2850fb`** carries items 3–5 and pass 1's R1, R2, R3 and R5 in one commit; the Principal waived one commit per
item on the load, and the body says so. No pull request is open for the branch or for slice A.

## The checks

| # | Check | How | Result |
|---|---|---|---|
| 1 | Not critical | `git diff origin/main...a2850fb -- lefthook.yml scripts/ .github/`; every `shoalmark.py` hunk against the function it sits in | The gate paths: empty. The new hunks since pass 1 are in `HTML_PAGE` (`draw()`, one expression), `brand_report` (plus two new functions beside it, `shipped_themes` and `theme_files`), `render_schema` (a closing paragraph), `parse_args` (`--from`, `--vendor`'s help), `vendor` (one tuple term), and `main` (the flag table, one call). These are unchanged: `triage_reading`, `build_judgement`, `commit_msg_check`, `guard_walk`, `triage_pending`, `commit_msg_hook`, `triage_guard`, `lint`, `pin_problems`, `source_provenance` and the `--queue` readers. `test_core.py` is unchanged. ✓ |
| 2 | **R1 — this repository's foot, as the Owner approved it** | `git diff b9644b7 a2850fb -- work-tracker/brand/theme.css`. **Before:** slice A's theme at `b9644b7e` on main's tool (= slice A's; it changes no code). **After:** the re-cut theme on this tool. Both built from one scratch clone at `a2850fb`, rendered in place; board, search (`#FM-00`), story view (`#g` once), tracker (`#=FM-002`) and the acts dialog; 1440, 1000 and 390 px; light and dark; full page | The re-cut changes only what hooks 1 and 2 replace: `#p::before{content:…}` → `#p>.pt`, and in shoalmark its magenta line; the lift → `#B:not([hidden])~#F{display:grid}` and the grid; plus comments, each marked `SLICE B`. Workaround 3, `tr.t:nth-child(even)`, stays, kept and marked. **30 of 30 pairs byte-identical.** I measured the claim's ink on the band myself: `#b4c3d1` on `#15293c` **8.25:1** by day and on `#15293d` **8.24:1** by night (1.74:1 on the chart at pass 1's tip). The committed `evidence/FM-002/slice-b/shots/`: five 1440×320 PNGs, IHDR/IDAT/IEND only; *before* and *after* byte-identical in both schemes. The *without the re-cut* shot shows pass 1's defect. ✓ |
| 3 | **R2 — the box's title wherever the box is drawn** | `draw()` read; FM-006's `build-mocks.py` (`--plex` the npm cuts) on main's build of this repository's board, against each starter from the person's place on this tool, the data line made equal; board, search, story, tracker, dialog; 1300, 1000 and 390 px; light and dark | `#p` now always begins with `<span class="pt">`, and the queue follows only on the board view. **monochrome and shoalmark:** search **0 px** (12 of 12 identical; pass 1: 834–3,651 px), tracker **0 px**. Board and story: 313–419 px each, all in the search box's 112×23 px at (234, 84): the placeholder, the one marked rule not the mock's. Dialog: that box plus the note's placeholder, 1,619–2,161 px. **No other pixel differs from the mocks.** ✓ |
| 4 | **The default board renders as before** | main's tool against this tool, one snapshot, the person's place empty; a board with no brand, and one with a claim only (`footer:`); board, search, story, tracker, dialog; 1300 and 390 px; light and dark | **40 of 40 byte-identical**, the story view included, which now carries the hidden title. The two pages differ only in the three hooks, the default CSS line and the label table. `view/` is identical across every build. ✓ |
| 5 | Each `theme.css` against its mock | `git diff 9f2f525 a2850fb -- brand/` | **Empty**, so pass 1's byte-for-byte result stands: 0 unmarked differences. ✓ |
| 6 | **Item 3 — `--brand DIR --from`** | a consumer repository (`git init`, `--init`) on a fresh vendored copy of this tip; the command run, then `diff -r`, a board build, and the refusals | `--brand docs/work-tracker/brand --from shoalmark`: *the shoalmark theme — a starter from …*, five `wrote` lines, exit 0. The copy is `diff -r`-equal to the theme's folder. The board wears it from the repository's place with three `brand/fonts/…` urls, each a file. A second `--from monochrome` keeps all five files, each named *kept … delete it to start from monochrome*. `--from catkin` exits 2: *the tool ships no such theme — monochrome or shoalmark; nothing was written*, and no DIR is created. `--from` alone and `--brand --from` exit 2: *--from goes with --brand DIR — `--brand DIR --from monochrome\|shoalmark`*. `--help` and `--schema` name both themes, and `--schema` ends *No key chooses the board's look*. A board built from a `--from` copy in the person's place is byte-identical to one built from the theme folder, paths aside. ✓ |
| 7 | **Item 4 — `--vendor`** | `--vendor … --allow-untagged` from a clean clone at the tip into the consumer; every PIN line checked with the tool's own digest (sha256, CRLF read as LF) and `cmp` against the source; the consumer's `--check`; one pinned theme file edited | *19 files, pinned*: 8 of the tool's and **all 11 files under `brand/themes/`**, every hash matching and every file equal to its source. (The two `LICENSE.txt` are CRLF, as npm ships them, so a raw `shasum` differs by design.) The consumer's board, choosing none, wears none (no `<style data-from`). `--brand` there marks the copy's `brand/` *— no brand file here: its themes/ are starters, worn only once --from copies one*, every source *built in* (R3). `--check`: 0. With one line appended to a vendored `theme.css`: 4, *differs from its PIN*. ✓ |
| 8 | Item 4 — README, CHANGELOG | `## 9. Branding the board` read and counted (the suite's own cut); `## Unreleased — 0.18.5` | The section is **24 lines** plus its closing blank (25 by the check's count, the Done-when's ceiling). It names the three places, the starters, `--from`, *a vendoring repository receives both*, *looks as it did*, and the three hooks. The CHANGELOG's slice B bullet heads `## Unreleased — 0.18.5`, above slice A's. It names FM-002, `4e00f85` (PR 90), both themes, what a vendoring repository receives, `--from` and its refusals, the three hooks, the upgrade note on `#B … ~ #r` and `#F`, and *Eigner*. ✓ |
| 9 | Item 5 and R5 — the record, the German words | FM-002's diff; `examples/de/labels.yaml`; a grep over `examples/`, `docs/`, the tool and the suites | FM-002 has one ship-log row on top, naming the build's commits by sha (this one as *one commit*), and one *What is true now* clause after slice A's. Nothing else in the file changes. `labels.yaml` lines 44, 47, 67 and 70 say *Eigner*, and *Auftraggeber* is gone from everything shipped. The German fixture follows, and C4 (every label German, none unknown) passes. ✓ |
| 10 | The hook incident (19:50:55), disclosed in the body: is the tree whole? | the commit's content against pass 1's tip; the named checks; the suites | `a2850fb` carries no conflict marker and no `.orig`, `.rej`, patch or backup file. `brand/themes/` is unchanged since `9f2f525`. The suite's diff since `9f2f525` removes only the three German fixture lines it replaces, and adds 11 `check(` calls (443 → 454). Every check the body names exists (the 25-line README, the re-cut theme, R2's three views, R3's report, `--from`'s copy/keep/refusals, `--vendor`'s 11 files), and all pass (check 12). **Whole.** Noted, not fixed. ✓ |
| 11 | Merges | `git merge-tree --write-tree` | Against `origin/main` (`bef2a1e`): clean. Against slice L, `fm/006-the-landing-page` at `dd88edc`: clean. Slice L's `work-tracker/brand/theme.css` is slice A's (same blob), so the merged tree carries this branch's re-cut. The merged CHANGELOG reads slice B, then slice A, then slice L under `0.18.5`. Slice A (`b9644b7`) is an ancestor of the tip. ✓ |
| 12 | Gates | this worktree at the tip, one interpreter at a time | `test_shoalmark.py` **481 ok** and `test_core.py` **148 ok**, *skipped here: 0 checks — every check ran*, *all green*: on **3.14.3** (started at load 3.20, ended 3.94) and on **3.9.6** (started at 3.95, ended 3.13). No FM-035 failure. `--check` 0 (*INDEX.md is up to date — 38 trackers*; *judged before build: on*, every build commit under a judged In Progress tracker; *the Owner's two sections: guarded*, 14 commits). `--session-check` 0. `--queue`: `fm/002-slice-b-… @ a2850fb  wait: no pull request — no verdict on a2850fb`. `git status` empty after every run. ✓ |

## Pass 1's findings

| # | Pass 1 | Now |
|---|---|---|
| R1 | P2 — slice A and B together dropped the claim off the band, 1.74:1 | **Closed** — check 2: 30 of 30 identical to slice A's approved state; 8.25 / 8.24:1 |
| R2 | P2 — the box untitled off the board view | **Closed** — check 3: search and tracker 0 px against the mocks, board and story the placeholder only |
| R3 | P3 — `--brand` listed an empty organisation place | **Closed** — check 7, and the suite's R3 check |
| R4 | P2 at `f11bc04` — the stripes | Closed at `9f2f525`; `brand/themes/` unchanged since |
| R5 | P3 — *Eigner* once, *Auftraggeber* three times | **Closed** — check 9, *Eigner* throughout |

## Findings

None at P2 or P3.

Noted, not findings:
- `theme_files()` takes every file under `brand/themes/` except dot files. A git-ignored file there, such as an editor's
  `theme.css~` (`*~` is in `.gitignore`), would be vendored and pinned. `--vendor` only runs from a clean clone at a
  tag, where no such file exists. `git ls-files` would close it, if the tool ever vendors from elsewhere.
- The README numbers *9. Branding the board* before *8. Working on shoalmark*. That is main's order, not this slice's.
- monochrome's mock header, kept verbatim, still says *no markup changes, no change to shoalmark.py*. The starter's own
  header above it says what changed. As-is.
- FM-002's clause ends *pass 2 is due*. The landing record updates it.
- Hook 3 (`zebra`) ships in the markup and no shipped theme uses it, as ruled at `9f2f525`. The suite's hooks check styles
  it with a fixture theme.

## Not verified

- Firefox and Safari; print; a real phone (390 px is Chrome's device metrics); a screen reader.
- A release-tag vendoring: the vendored copy came from an untagged clean clone (`--allow-untagged`). The tag is the
  Owner's act after the merge.
- The answer dialog under a theme: no ask is open on today's board, so the acts dialog stood in.
- A mutation run of `a2850fb`'s new checks: read, not run. Pass 1 ran one on the hooks' and the starters' checks.
- Independence: same session, not independent.

## Verdict

**READY** — pass 1's R1 and R2 (P2) and R3 and R5 (P3) are closed, each shown by a render or a run, and no finding is
open. Tier *code*, the full loop, pass 2. Independence *same session — a sub-agent of 8e509911*. Slice A (`b9644b7`,
READY WITH FINDINGS) is merged into this branch, so this pull request carries both.

The Owner lands this by merging; a merge rules nothing.
