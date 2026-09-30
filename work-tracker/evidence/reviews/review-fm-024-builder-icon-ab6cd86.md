# FM-024 — the Reviewer's pass on the builder's and the planner's icons at ab6cd86

Verdict: READY.
Reviewed: ab6cd868290d6bd6dda1f04d3ed7a622034d3ffe
Reviewer: 8e509911/reviewer-66 (Opus), worktree shoalmark-review-4, 2026-09-30 16:36–16:41 CEST. Independence: same session as the build (8e509911/designer-1) — not independent.
Tier: docs (FM-032 S1), one pass, no suite run: `git diff --name-only origin/main...HEAD` is brand/seats/ (two SVGs renamed, preview.html, README.md), one PNG under evidence/FM-024/ and the FM-024 file — no shoalmark.py, test, toml or hook.
Scope: four commits aa15edd..ab6cd86 on 28852e2 (origin/main 11dd6a9 is one merge ahead); `git diff -M --stat`: 6 files, +21 −19.
The Owner's rulings, relayed by the Principal, normalised, words and not signed answers: *"the implementer seat is renamed builder … the icon (builder.svg; the character needs a new name, the Designer's call)"* and *"the principal seat is renamed planner … the icon (planner.svg; the skipper character stays)"*.
Renames: implementer.svg → builder.svg and principal.svg → planner.svg show as renames (similarity 94 %); `git diff -M` on each is the <title> line alone ("builder — the shipwright", "planner — the skipper"); without the title each file hashes the same as on main.
Export: ran 16:38:15 CEST, exit 0; it writes out/builder-{20,200,400}.png and out/planner-{20,200,400}.png beside the other five; all 21 equal my headless Chrome render of their SVGs, 0 pixels apart, and builder/planner equal the pass-1 Chrome renders of implementer/principal, 0 apart (control: planner against builder at 20 px, 96 apart). out/ stays ignored.
Preview and README: both name planner and builder, with no principal or implementer left in brand/seats/; the README is 30 lines; the designer's row now tells the pear from "the planner's cap".
The shipwright: "a yellow hard hat on the stake's own green — it builds what the plan says, plank by plank, as a yard builds the fleet" fits the seat's job and agrees in substance with docs/seats/index.md's builder row on main ("it builds what the plan says"), which the wording pass will rename.
Render: seat-icons-preview-2026-09-30-renamed.png, 1440 × 2000, 264,186 B (under 300 KB), sha256 290a3c84…6f26a, as 03a62bc states; re-rendered here from the tip, it differs only on anti-aliased text and circle edges; the 14 icon interiors are equal. The two renders on main are untouched; nothing under work-tracker/ is renamed against main.
RV-2022 closed: the README's rule carries "Borrowed from the marks looked at: a face of two eyes, one object per character — nothing of their drawing." word for word, and the file is still 30 lines.
RV-2021 closed: the builder row, not the d72b8e0 row (the log is append-only), says designer@seat was not in `[seats]`, so the session rule judged none of the Designer's commits, this branch's included. `[seats]` on main 11dd6a9 still lacks designer; `designer = "designer@seat"` is on the unpushed identities branch (fm/024-a-seat-has-several-identities, ec305f7). I read this branch's four trailers: `Session: 8e509911/designer-1`, `Worktree: shoalmark-impl-2`, and Co-Authored-By on each.
Ship log: two rows appended, the earlier rows unchanged. The builder row's `…-builder.png` does not exist at the tip; the planner row says it was moved to `…-renamed.png` and re-rendered in 03a62bc, which is the right fix in an append-only log. At the tip: records +2, product +19 −19, one PNG, matching `--numstat`. No he/his/she/her on any added line.
Gates: --check exit 0; --session-check exit 0; git diff --check exit 0; git merge-tree --write-tree origin/main HEAD against 11dd6a9 exit 0, tree fb82a5b4…; queue: `branch fm/024-the-builder-icon @ ab6cd86  wait: no pull request — no verdict on ab6cd86`.
Findings: none. Quality read: clean — the smallest change that carries both renames, and both earlier P3s are closed in their own words.
A note carried from the pass on d72b8e0: the run sheet (f29b8fc) now names planner and builder but still does not set GitHub's badge background colour; the README says `#15293d`.
Four numbers for this verdict: records +21, product 0.
path 5 — a merge rules nothing.
