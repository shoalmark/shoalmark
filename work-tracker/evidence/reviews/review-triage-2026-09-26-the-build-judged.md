# Review — the build judged before its first commit, FM-002 and FM-006 (2026-09-26, Reviewer, session `8e509911/reviewer-32`)

- **Date:** 2026-09-26, from 14:35 CEST.
- **Seat:** Reviewer (Opus 5.5, highest effort), a sub-agent of Principal session `8e509911`.
- **Session:** `8e509911/reviewer-32`.
- **Worktree:** `shoalmark-review-5`, detached at the tip. The `--triage` runs were made in two scratch clones in the
  session's scratchpad. The Owner's checkout, `shoalmark-gtm`, every other worktree and every folder of session
  `8b91dba2` stayed outside every command. The three word files in the Principal's scratchpad were read and hashed, not
  changed.
- **Tier:** docs, one pass. `git diff --name-only origin/main...HEAD` names 4 paths, all under `work-tracker/`: FM-006,
  INDEX.md, TRIAGE.md and the worksheet. No `shoalmark.py`, test, configuration, hook, key or signers file is among them.
  The one front-matter change is a `triaged:` value that `--triage` wrote, not a key. A P3 is fixed forward; a P2 sends
  it back.
- **Independence:** same session. This is 8e509911's own sub-agent, reviewing its Principal seat's commit
  (`Session: 8e509911`). Reported as such, not independent.

**Reviewed:** `tracker/triage-2026-09-26-the-build-judged` at `e2ccd04dde210a7501425aa5ba9b26a0dc910904`.
- One commit, the Principal seat's (`Worktree: shoalmark-principal-4`, unsigned), on `origin/main` `b3e9b6a` (PR 91's
  merge). No pull request is open for the branch.
- `origin/main` moved during the pass. PR 92 (FM-038's filing) merged at 14:40:47 as `2a9f7eb`, so the branch no longer
  fast-forwards. Check 11 covers both mains.
- It acts on the Owner's two signed answers: FM-002's `4e00f85` (13:54:50, PR 90) and FM-006's `8defe63` (13:55:58,
  PR 91). Both are `G` and on main.

## The checks

| # | Check | How | Result |
|---|---|---|---|
| 1 | The history the brief gives is what the tree shows | the worksheet at the tip; `--triage` in a scratch clone at `e2ccd04`; a positive control in a second clone with the two new rows moved to the top of the table | The new rows are the table's last two. The four morning rows are byte-identical to main's, and the only change is 2 lines added at the bottom. At the tip, `--triage` names the morning row: *FM-002: `keep P2 #4 owner` — superseded on this sheet by the later row, `keep P2 #4 build`*. In the control, with the rows on top, the same run applies the morning row: *Applied 1: FM-002: keep P2 #4 owner*, and FM-002's `next: build` becomes `next: owner`. That is the first placement the brief describes. ✓ |
| 2 | FM-002's and FM-006's front matter against `origin/main` | `git diff`; sha256 of each front matter and each body at both commits | FM-002 is unchanged: front matter `51507121…`, body `06d21fb1…`. It reads `triaged: 2026-09-26`, `rank: 4`, `tier: P2`, `next: build`, and the answer's three lines. FM-006's body is unchanged (`2713f6a9…`). Its front matter changes in one line, `triaged: 2026-09-25` → `2026-09-26`, and keeps `rank: 6`, `tier: P2` and `next: owner`. ✓ |
| 3 | `--triage` on the tip applies nothing new | scratch clone at `e2ccd04`, `python3 shoalmark.py --triage` | *0 trackers to judge*, *Applied nothing — no new filled rows*, exit 0. The superseded line of check 1 is its only other output. The clone was clean after. ✓ |
| 4 | The Reasons: each slice's tier by the printed rules and his words | the rows against path line 3 as `--triage` prints it, AGENTS.md's two tiers, and the three word files (sha256 `34ee13d1…` 07:41:00, `21497e4d…` 09:23:58, `416d54ce…` 10:25:41, each matching the hash FM-002 cites) | Each slice's tier holds. The table below goes slice by slice. One sentence does not hold on this repository (R1), and one carry-over is narrowed (R2). ✓ with R1, R2 |
| 5 | Nothing decided that his answers do not decide | the same | The start page is marked *the seat's reading of* landing page, *his to strike*, as FM-006:25 marks it. The working order is the seat's to judge. A and B run in parallel, L follows A, and A's CSS is re-cut on B's hooks. His word gives the order to the pass (*unless the pass judges otherwise*), and its condition is met: FM-037's guard shipped in 0.18.4, and the tag is from 09:58. The markup hooks go to slice B, which the themes README leaves to *the pass*. ✓ with R1 (a timing his signed answer leaves open) |
| 6 | TRIAGE.md: changed only under *Passes*; the guarded sections | sha256 of the file above `## Passes`, of *The intent* and of *The current path*, at `origin/main` and the tip; the diff of the *Passes* section | All identical: above *Passes* `60579d25…`, the intent `74ff308a…`, the path `a100dbd4…`. The file gains one paragraph and one blank line, first under *Passes* (newest first). `--check`: *the Owner's two sections: guarded — 1 commit(s) … none changes them or his signers file*. ✓ |
| 7 | The *Passes* paragraph's facts | `gh pr view 90/91 --repo holgo99/shoalmark --json mergedAt,mergeCommit,headRefName`; `git log` of the merge and answer commits | PR 90 is `answer/fm-002`, merged `2026-09-26T12:24:52Z`. PR 91 is `answer/fm-006`, merged `12:25:12Z`. The paragraph's 14:25:12 matches. Its 14:24:51 is the merge commit's time (`485b533`, 14:24:51 +0200), one second before the forge's 14:24:52 (R4). *Option 2*, *the proposal*, the worksheet's path and the two verdicts match the rows. ✓ with R4 |
| 8 | INDEX.md as the tool writes it | `git diff`; `python3 shoalmark.py` at the tip, sha256 before and after | One row changes: FM-006's *Triaged*, 2026-09-25 → 2026-09-26. Regenerating leaves the file at `77f77a7c…`, and `--check` says *INDEX.md is up to date — 37 trackers*. ✓ |
| 9 | `--check`, `--session-check` | in this worktree at the tip | `--check` exits 0. It prints *judged before build: on — 1 commit(s) … every build commit under a judged In Progress tracker*, the guard line above, and *filing freeze: 19 open*. `--session-check` exits 0 and prints nothing. ✓ |
| 10 | Both suites by hand | `python3` (3.14.3) in this worktree; `/usr/bin/python3` (3.9.6) in the scratch clone at the tip | `test_core.py`: 148 ok, *all green*, on both. `test_shoalmark.py` on 3.9.6: 462 ok, *skipped here: 0 checks — every check ran*, *all green*, 8 min 04 s. On 3.14.3: 462 ok, *skipped here: 0 checks — every check ran*, *all green*, 9 min 16 s. Both trees were clean after. ✓ |
| 11 | merge-tree against `origin/main` | `git merge-tree --write-tree` against `b3e9b6a`, then against `2a9f7eb` at a second fetch; a scratch merge of `2a9f7eb` into `e2ccd04`, then `python3 shoalmark.py`, `--check` and `--triage` on it | Against `b3e9b6a`: clean, exit 0. The tree is `526b0c78…`, the tip's own, because `b3e9b6a` is the tip's parent. Against `2a9f7eb`: clean, exit 0, for the tip and for this verdict commit. INDEX.md auto-merges. On the scratch merge it regenerates to itself, *38 trackers*, and `--check` exits 0. `--triage` there applies nothing. It lists FM-038 as the one tracker to judge, a new filing no pass has read yet, which is not this branch's. ✓ |
| 12 | FM-033: nothing built before the pass | `git rev-list --count origin/main..<b>` over every branch on origin | Only this branch and `fm/038-…` are ahead of main. No FM-002 or FM-006 build commit exists. ✓ |

**Check 4, slice by slice.** Path line 3, as the pass prints it, gives three reviews:
- critical changes (a release, the gate or hooks, signing and rights, TRIAGE.md or AGENTS.md rules changed by a seat,
  anything tagged security or P1) get *a Reviewer from another independent session*;
- *other code* gets *inline Reviewer passes*;
- *documentation* gets *one Reviewer pass*.

AGENTS.md draws the line between code and documentation by path.

| Slice | The row's tier | The rule | His words | Holds |
|---|---|---|---|---|
| A: the brand layer | docs/brand, one pass, *the Owner sees the renders before the merge* | `work-tracker/brand/` and `docs/stylesheets/`, no `shoalmark.py`. The gate never reads the brand files (`brand_places`: *INDEX.md, the gate and the deriver are functions of the repository alone*) | 07:41:00 item 3: *No shoalmark.py change. One Reviewer pass, unless the pass rules otherwise*. Item 4: *He sees them before the merge*. 09:23:58: the inline header, for every board | ✓ The contrast carry-over drops *in both schemes* (R2) |
| B: the tool ships both themes | code, inline passes, the full loop | `shoalmark.py`, tests, the CHANGELOG, the README. Not critical: no release, no signing, no rule text; FM-002 is P2 and untagged. The *markup hooks* are the board's HTML, not git hooks. `--vendor` pins more files, and `pin_problems` reads whatever the PIN lists, unchanged | 07:41:00 item 3: *Code tier, inline passes, tests, CHANGELOG, a line on what vendoring consumers receive. The default look … stays*. The answer, option 2: *the tool ships monochrome and shoalmark as starters* | ✓ |
| L: the landing page | docs/site, one pass, after A | `docs/`, the way FM-006's earlier site slices went (the nav lines of `59febae` included) | 10:25:41: *for the v0.18.5 release we also add a landing page requirement*. The start page is the seat's reading, marked, his to strike. The pasted report put where it ships to him: *(the site's start page or a page of its own), is your call* | ✓ The row is silent on the fonts its mock loads (R1) |

## Findings

**R1 · P3 · confidence 95% on the facts, 65% on the grade · *The site goes live at the next release tag (0.18.5)*
does not hold while the repository is private. Neither row names the one open item FM-006 dates *before the site is
ever published*.**
- *The gap:*
  - `.github/workflows/docs.yml` builds the site on a tag. It deploys only `if: github.event.repository.private ==
    false`, and its comment says so: *deploys on the day the repository goes public*.
  - `gh api repos/holgo99/shoalmark/pages` answers 404. No Pages site exists.
  - The FM-006 row of this same pass puts going public after the scoring, *with no date yet*. So the site goes live
    at 0.18.5 only if his act comes before the tag.
  - The sentence is his own word of 07:41:00 (item 4: *the new site goes live with the next tag*), repeated by the
    seat. The premise under it is the workflow's.
- *Why it matters:*
  - The Owner reads that the site goes live at 0.18.5, and so does the release plan. The Principal's 0.18.5 plan,
    which is in its scratchpad and not in the record, ends *Merge, tag → the site live with the new look*.
  - If he did go public first, FM-006:41's open item would come due before 0.18.5. That item says *the pages load IBM
    Plex from Google Fonts … the fix is to self-host Plex under `docs/assets/fonts/`, its own slice*.
  - Slice L's mock loads Plex Mono and Silkscreen from Google Fonts (`landing/index.html:11`, its README's line 4).
    Slice L's line does not say whether its build keeps them, and neither row names the self-hosting slice.
  - Merging this publishes nothing. That is why the grade is P3.
- *What closes it:*
  - The FM-002 line reads *built into the 0.18.5 site; live at the first tag after the repository is public
    (`docs.yml`)*.
  - The Google Fonts item is named for slice L, as the Principal's brief names it for slice A, or as a gate of going
    public.
  - The ready line puts the premise to him. It is P2 if he means to go public before 0.18.5 for the site's sake.

**R2 · P3 · confidence 99% on the facts, 70% on the grade · Both trackers still read as they did before his answers.
The previous pass's R1 and R3, which that pass said were *due before FM-002's build pass*, are still open at the tip,
and this is that pass.**
- *The gap:*
  - `FM-002:24`, the opening a pass's *Now* cell shows, still says *Slice B, only if he rules it*. It also still says
    *nothing is built before his answer and a pass's judgement*. He has answered option 2, and this sheet is the
    judgement.
  - `FM-002:44`, *Done when*, still reads *every text pair at 4.5:1 re-measured on the built files*. His 07:41:00 item
    4 says *in both schemes*. This row repeats the narrowing: *contrast at 4.5:1 on the built files*.
  - The 0.8.0 paragraph (`:41`) is still unmarked.
  - `FM-006:25` still says going public is the ask *he answers now that v0.18.4 has landed*. `:27` still says the
    themes' ask *waits for the going-public ask to be answered*. Both asks are answered.
- *Why it matters:*
  - The tracker is canonical (AGENTS.md rule 1).
  - The two build seats and their Reviewers test the *Done when*. A measurement in one scheme passes it as written.
  - A cold seat that reads FM-002's opening meets a slice B that is still conditional.
- *What closes it:* a tracker-only commit before slice A's first build commit:
  - FM-002's opening names the answer (`4e00f85`, PR 90, option 2) and this sheet's judgement;
  - the contrast line says *in both schemes*, and the 0.8.0 paragraph is marked *(met, 0.8.0)*;
  - FM-006's two sentences say that both asks are answered (`8defe63`, PR 91; `4e00f85`, PR 90).

**R3 · P3 · confidence 90% on the facts, 50% on the grade · FM-006's row says it is *no re-judgement of the
tracker*, but to the tool it is one.**
- *The gap:*
  - `--triage` re-dates FM-006 to `triaged: 2026-09-26`. That is the branch's only front-matter change. It stamps
    `keep P2 #6 owner` again, and the row gives no reason for P2 or for #6 today.
  - Printed rule 1 says *every keep carries a tier judged today … an inherited tier is no judgement*.
  - The RANK rule puts nothing that *waits for a date, or for another tracker's run* ahead of what can be worked on.
    The row itself says the act waits for the scoring and slice L waits for slice A. Meanwhile #8 (FM-028) and #10
    (FM-033) are builds.
- *Why it matters:* the board and INDEX.md now show FM-006 as judged today at #6. The 7-day clock restarts on a
  judgement the row says it did not make.
- *What closes it:* either of these:
  - the next pass judges FM-006's tier, rank and move, with reasons;
  - the row's opening says it re-dates the kept verdict in order to record slice L.

**R4 · P3 · confidence 99% on (a), 80% on (b) · The *Passes* paragraph.**
- *(a)* It gives PR 90's merge as *14:24:51*. That is the merge commit's time (`485b533`). The forge's `mergedAt` is
  `12:24:52Z`, which is 14:24:52 CEST. PR 91's 14:25:12 agrees with both.
- *(b)* The one reading that is *his to strike*, the landing page as the site's start page, is in the row and in
  FM-006's body. It is not in the paragraph he reads on TRIAGE.md.
- *Why it matters:*
  - (a) is small: a time should name its source.
  - (b): a reading he is to strike has to reach him. The intent's *never* list includes *a potential misunderstanding
    never questioned*.
- *What closes it:* the time with its source, at the paragraph's next touch; the start-page reading in the ready line.

**Noted, not graded.**
- Slice B stays inline-pass code only while its build leaves `pin_problems`, `lint`, `--check` and `lefthook.yml`
  alone. If it touches any of them it is *the gate or hooks*, and path line 3 then wants an independent session. The row
  does not name that condition, and the build's Reviewer reads the tier from the diff.
- Slice L stays docs tier if its statuses are re-read by hand, as the mock's were. A generator script or a `docs.yml`
  change would make it code. *The 23 statuses* becomes 24 when FM-038, filed as a bug on `fm/038-…`, merges. *Read
  from the record* covers that.
- Slice L sits under a tracker whose move is `owner`, so `--next` does not route a seat to it. The board shows the
  row's reason (`latest_verdicts` takes the last row). After slice A, FM-006's `next:` is the seat's to set.
- The FM-002 answer reads `accepted - <option 2>`, which is FM-029's defect. The row reads it right: *option 2*.
- Not this branch's: `FM-006:31` still calls the TRIAGE.md page *built, in review*. `docs/triage.md` is on main
  (`7c5d423`).

## Verdict — READY WITH FINDINGS (R1–R4, all P3), 85%

**READY WITH FINDINGS.**
- The tree shows the history the brief gives, and the control shows the first placement's flip.
- The morning row is reported superseded. FM-002 reads `triaged: 2026-09-26 · tier: P2 · rank: 4 · next: build`, as
  on main. FM-006 changes in `triaged:` alone, to `rank: 6 · tier: P2 · next: owner`.
- `--triage` on the tip applies nothing.
- Each slice's tier stands by path line 3 and by his words. The one reading beyond them is marked his to strike.
- TRIAGE.md changes only under *Passes*, and its guarded sections are byte-identical to main's.
- INDEX.md is the tool's.
- `--check` and `--session-check` exit 0, the suites are green by hand, and merge-tree is clean on `b3e9b6a` and on `2a9f7eb`.
- Nothing here needs a re-make before the merge. R1 goes in the ready line, and to FM-002 before slice A's first build
  commit. R2 is due in the same place. R3 is due at the next pass, and R4 at the paragraph's next touch.

*The Owner lands this by merging, and a merge rules nothing (path 5).*
