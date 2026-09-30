# Review — FM-024, the seat Apps' run sheet, continuation: main merged in, planner and builder (f29b8fc)

Reviewed: f29b8fc3d0b7ca9455b275f02878950f20b181b4

- Seat: reviewer-64 (session 8e509911/reviewer-64), worktree shoalmark-review-2, 2026-09-30 16:35–16:40 CEST. Range: `6d715ec` … f29b8fc: the merge `2ec682a` (main `28852e2` into the branch) and `f29b8fc`, both by the go-to-market seat (`8e509911/gtm-2`, `shoalmark-gtm-2`).
- Tier: docs by FM-032 S1. `git diff --name-only origin/main...HEAD` lists the sheet, FM-024 and two verdict files (+177 −0); main's own content came in by the merge. One pass, no suite run. Independence: same session.
- Verdict: READY WITH FINDINGS — two P3 (RV-2096, RV-2097), fixed forward. RV-2094 and RV-2095 stand, forward.

## Checks

1. The merge. `git show --remerge-diff 2ec682a` touches one file, FM-024's ship log, and only at the conflict. Both sides' rows are kept, oldest first. The branch's rows of 15:06, 15:26 and 15:34 come first, then the icons' row from `28852e2` (15:39), then the auditor correction (15:51). The row counts are 19 (first parent) and 16 (second parent), and the merge has 20. `comm` finds no row of either side lost. INDEX.md equals both parents', and `--check` says *up to date — 42 trackers*, so it needed no regeneration.
2. The renames, against the Owner's words (normalised): the implementer seat becomes builder (*shoalmark builder*, `shoalmark-builder`) and the principal seat becomes planner (*shoalmark planner*, `shoalmark-planner`). The seven Apps are now planner, builder, reviewer, research, go-to-market, designer, auditor. Steps 1 and 2 name the planner, step 3 the builder, and §4's loop both. `[seats]` keeps `principal@seat` and `implementer@seat` until the switch (:106–108). Quotes stay verbatim (:6), and the live session name stays (:97). The two description lines are his text, unchanged, and pass as before. The correction row is appended last. No *he*, *him* or *his* is left. The sheet is 120 lines.
3. The slugs, re-run 16:37:46–16:37:51: `shoalmark-planner` and `shoalmark-builder` answer 404 on `/apps`, on `/users/<slug>%5Bbot%5D` and on `/users/<slug>`; the control answers 200.
4. Gates against the current `origin/main` `11dd6a9`, 16:38–16:39: `--check` 0 (19 commits, every build commit under a judged In Progress tracker), `--session-check` 0, `git merge-tree --write-tree origin/main HEAD` clean (`782715c`). `--queue` at 16:39:08: *PR 134 wait: no verdict on f29b8fc*. Both commits carry `Session: 8e509911/gtm-2`, `Worktree: shoalmark-gtm-2` and `Co-Authored-By`.

## Findings

- RV-2096 · P3 · 85 % — step 4 still points at the merged icons branch. `fm/024-the-seat-icons` merged as PR 135 (`28852e2`) and is gone from origin (`ls-remote` empty at 16:37). `origin/fm/024-the-seat-icons` resolves in a clone only through an unpruned ref (`269f5e3`), so its *READY verdict* condition is moot. Its export writes `principal-` and `implementer-` files. Main now ignores `brand/seats/out/`, so :95's *main does not ignore `out/` yet* is false. `planner.svg` and `builder.svg` are on `fm/024-the-builder-icon` (`ab6cd86`), with the same art as main's files (only the `<title>` differs). Fix, :89–95: "**The icons**, from `origin/fm/024-the-builder-icon` (`ab6cd86`) until it lands, then from main: `git fetch && git switch --detach origin/fm/024-the-builder-icon && rm -rf brand/seats/out && python3 brand/seats/export.py && open brand/seats/out` … that App's `<seat>-200.png` … Either way, `rm -rf brand/seats/out; git switch main`." Drop *at `28852e2` still …* and *main does not ignore `out/` yet*.
- RV-2097 · P3 · 70 % — the builder line names *a Reviewer*, but the builder row at :43 and the new FM-024 row say *no seat named in it*. Fix: "its own seat not named".

Quality read: the merge resolution is exact, and the renames follow his words everywhere a seat is named. The defects are RV-2096 and RV-2097. Unproven: the renames and his earlier words are relayed, not yet in the repository; `fm/024-the-builder-icon` has no verdict here; the rest stands as the verdict on 6ad47e4 says.

Path 5 — a merge rules nothing.
