# Cold re-verification — FM-042 Stage 0 at 8ce8f8c

Reviewed: 8ce8f8c2748ae6b30b8f05267ca4f762ee7fbcff
Seat: independent reviewer; session 1640a2c7; isolated worktree shoalmark-fm042-cold; 2026-09-30.
Verdict: READY.
Scope: the three commits above 0e1949824b9fa83c21fb6e9689fdf2b82d153a62 against RV-2030–RV-2032's own fix texts; the prior cold review supplies the unchanged Stage 0 checks.
Tier: documentation under FM-032 S1; the overall branch remains critical under path line 3 because AGENTS.md rules changed. Rework: ADOPT.de.md and FM-042 only, +4 −4; no Python, toml, hook or test; no suites run.
Checkout: git fetch origin without prune, then git merge --ff-only origin/fm/042-a-requirements-layer-stage-0; fast-forward 0e19498 to 8ce8f8c.

## Findings re-verified

- RV-2030 · P2 · CLOSED — 13dc224 replaces the post-cd destination with `shoalmark.toml` and adds `Die Zielordner vorher anlegen.` before copying. Fresh scratch trial using the clone at v0.18.6: vendor exits 0; create destination folders, copy the four German files into the current probe directory, then --init --key AP exits 0. All four files remain byte-identical after init. The exact fix is present and works.
- RV-2031 · P3 · CLOSED — 8ce8f8c recounts after both content fixes, explicitly excluding the Reviewers' review files. Independent numstat f3d19dd..8ce8f8c, with requirements/ as records: 52 records added / 34 product added / 8 deleted; with requirements/ as product: 9 / 77 / 8. Both sets equal the row. The changed numbers follow the prior verdict's instruction to recount after further edits.
- RV-2032 · P3 · CLOSED — 771e3e7 uses `trackers cite ids in a body line (`Satisfies: REQ-001`), tests name them` in FM-042's current Stage 0 paragraph, exactly the requested correction; it agrees with the convention and the prior scratch schema probes.
- No new findings. RV-2033 onward unused.

## Verification

- The three commits carry Co-Authored-By, Session: 8e509911/implementer-60 and Worktree: shoalmark-impl-2; this reviewer has a different session root. No content fix made by this review.
- --check exits 0: 21 commits since origin/main, every build commit under a judged In Progress tracker; the Owner's guarded sections unchanged. --session-check exits 0. git diff --check exits 0.
- git merge-tree --write-tree origin/main 8ce8f8c exits 0, tree f377b47384ff41ab97dc4c0de79fcf5b5f1d203c.
- Scratch venv, pinned zensical 0.0.66 and tinycss2 1.4.0: zensical build --clean, scripts/llms_txt.py site and scripts/check_site.py site each exit 0. macOS run; no CI claim.
- --queue before this verdict: “branch fm/042-a-requirements-layer-sta… @ 8ce8f8c  wait: no pull request — no verdict on 8ce8f8c”; “5 waiting on you: 0 merge, 0 close, 2 wait, 3 pushed without a pull request”.
- The changed German instructions retain the file's plural ihr register, correct destinations and truthful tag contents. No new claim or identifying disclosure. The earlier hand claim screen stands for the unchanged entries; the scoring service was not called.

Quality read: the trial's setup is executable, and the canonical tracker now agrees with the convention and the measured diff. All three findings are closed; READY for the reviewed Stage 0 scope.

path 5 — a merge rules nothing.
