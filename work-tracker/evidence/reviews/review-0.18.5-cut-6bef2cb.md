# Review — the 0.18.5 cut at `6bef2cb` (2026-09-27, Reviewer, cold session `01a0e147`)

- **Reviewed:** `release/0.18.5` at `6bef2cb0fc9120c36a8065380e341b5918e12090`.
- **Tier:** *code — a release, critical*; the full loop, with NOT READY on any P2.
- **Independence:** *a cold session started by the Owner under his path line 3*. Session `01a0e147`, Reviewer seat,
  worktree `shoalmark-review-cold`; none of the branch's build sessions authored this pass. The sealed directory of
  session `8b91dba2`, the Owner's checkout and every other worktree stayed outside every command.
- **Reviewer's cold start:** the necessary virtue was adversarial verification. Its shadow was needing the cut to fail;
  a finding therefore needed a first-hand failing control, not severity by assertion. The Owner receives this record.
- **Clock:** the suites ran 10:40–10:56 CEST, outside 00:00–02:00, so they ran in local CEST rather than with `TZ=UTC`.
  Each long suite began with load under 5 and no other seat's suite running.

## What I ran and what survived

| Check | Result |
|---|---|
| Full suites, one interpreter at a time | Python 3.9.6: `test_shoalmark.py` **481**, `test_core.py` **148**; Python 3.14.3: **481 + 148**. Exit 0, **0 skipped**, all green. Starts at load 1.62 and 2.41; the 3.14 core ended with load 2.58. FM-035's healthy-board case passed on both. |
| Gates and branch state | `--check` 0; `--session-check` 0; INDEX current, judgement on, Owner sections guarded. `--queue` reads `release/0.18.5 @ 6bef2cb` as *no pull request — verdict 6bef2cb READY: open it*. The remote tip remained `6bef2cb`; `origin/main` `bef2a1e` is its ancestor. |
| Fresh-clone negative control | A new full clone, detached at the tip, run from its own root with `GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null`: exit 4, one checkout finding naming six signed commits, `INDEX.md is up to date`, **no STALE**. With the signers configuration present, this worktree's gate is 0. |
| Site build | `uvx zensical build` 0, *No issues found*. The built start page names v0.18.5 three times; setup pages clone `v0.18.5`; no built page names v0.18.4. |
| Consumer choosing nothing | Fresh `acme` repositories vendored from `v0.18.4` and the untagged tip, then `--init` and `--html-only`: 1440 px Chrome renders differ in **48 pixels**, only the running-line digit `4` → `5`. No theme is selected implicitly. |
| Starters and refusal | `--from shoalmark` and `--from monochrome` copied their five files byte-for-byte and each rendered. `--from catkin` exited 2, named the two themes, and wrote nothing. The shipped CSS uses `#p>.pt` and `#F`; the old active title/footer workarounds are gone. Hook 3 remains in markup while both shipped themes deliberately keep the ruled mock's `nth-child` stripes. |
| shoalmark board and site | Slice A's `checks.mjs` re-run on the pinned before/after sources: 746 text measures per scheme, **0 below 4.5:1**; lowest 5.76 light and 5.98 dark, pipeline control 4.542. AU-16: 0 figures and 0 markers read in board, tracker, dialog and site; the negative control reads 261 figures and 37/18/21 markers. AU-18: 838 px / 8.4 px = 99.8 characters; longest line 99. |
| Landing page | It is `site/index.html`. Its committed checker re-run on the release build: 24 focusable wrecks, canvas described, 0 figures/names in the accessibility tree, no script error, no failed request, no sideways scroll at 1440/1024/390, reduced-motion captures identical, light/dark preference identical. Uncovered chart text bottoms at 4.80:1; other text at 5.14:1. The two west-edge figures under the title reproduce the slice's disclosed covered case (3.99/1.30), not a new finding. |
| Landing evidence | Rebuilt `9307cf8`, `ab69afb` and `69552ed`, then re-ran `render.mjs`: all four R3 chart images and all three reduced-motion images are byte-identical to the committed renders; `start-390.png` is identical. Motion-enabled differences are confined to the moving wreck/convoy/ticker pixels; hosts and script-error records match. `facts.mjs bef2a1e` reads the same 24 bug/security trackers and every report remains the required prefix of its tracker hook. |
| Release reconciliation | `VERSION`, newest CHANGELOG heading, setup clone tags, board running line, landing HUD/link/fine print all say 0.18.5; the release day is 2026-09-27 in the two ruled places. I read `git log v0.18.4..6bef2cb --no-merges` against every 0.18.5 bullet. The cut changes no existing tracker's front matter by hand: FM-039 is the new `--new` filing; INDEX/evidence are derived records; no status is flipped. |
| Gate and hooks | The cut after `631a8bc` changes no `shoalmark.py`, suite, `shoalmark.toml`, `lefthook.yml`, hook script or workflow. Against v0.18.4, changed top-level functions are only `brand_report`, `render_schema`, `parse_args`, `vendor`, `main`, plus new `shipped_themes` and `theme_files`; markup/CSS constants also change. `build_judgement`, `commit_msg_check`, `commit_msg_hook`, `judge_commits`, all FM-037 guard functions, `lint`, `pin_problems`, signature readers, `queue_actions`, `session_check` and `install_hook` are byte-identical. Merge-tree with `origin/main` is clean. |
| Whitespace control | `git diff --check origin/main...HEAD` exits 2 only for the two CRLF `brand/themes/*/fonts/LICENSE.txt` files, IBM's verbatim OFL files. No finding. |

## Findings

**R1 · P3 · confidence 95% on the facts, 75% on the grade · Slice L's three lost English facts remain unfixed.**

The landing page replaces `docs/index.md`, but its visible copy and linked English pages still do not carry: (1) that a
commit's date is when it was made rather than pushed, with the forge-push qualifier behind the score; (2) that the
independence count is a report rather than proof because git cannot yet show it; (3) that every signature names the key
that made it. All three remain only in `docs/index.md`, whose body the override hides (and in the German/agent artefacts
described by the slice review). The release note correctly discloses this as open.

**What survives:** the page's scores, claims and linked setup/signing/standup explanations are otherwise present, and
the loss does not falsify the release's functional claims. **What closes it:** restore each qualifier where its claim is
visible or on a linked English page, or the Owner explicitly accepts those three sentences as removed.

**R2 · P3 · confidence 95% on the facts, 70% on the grade · The start page still leaves a local build for absolute,
pre-publication addresses and carries no favicon.**

The built page's six documentation/agent links and its `llms.txt` alternate still point to
`https://holgo99.github.io/shoalmark/...`, which serves nothing until the go-public act; `overrides/landing.html` is
another address to change at that act. The standalone override emits no favicon link, and Chrome requests none of the
site's `favicon.svg`. The release note correctly discloses the links and missing favicon as open.

**What survives:** the destinations are the intended public pages and the site is intentionally not deployed before the
go-public act. **What closes it:** use site-relative documentation/`llms.txt` links and add the site's favicon, or add
this override explicitly to the go-public address-change act.

## Verdict

**READY WITH FINDINGS** — R1 and R2 are the two still-open slice-L P3s, re-verified and re-raised as the cold brief
requires. There is no P2. The strongest counterfact is that the page intentionally follows the approved mock and the
release notes already disclose both gaps; the unresolved unknowns are the tag's five-job CI matrix, Windows, Firefox,
Safari, print, a real phone, a screen reader and the not-yet-live site. A reproducible P2, a failed tag matrix, or a
change after this verdict reverses READY; the named fixes close the P3s forward. This Reviewer neither fixes nor
dispositions them.

The Owner lands this by merging; a merge rules nothing.
