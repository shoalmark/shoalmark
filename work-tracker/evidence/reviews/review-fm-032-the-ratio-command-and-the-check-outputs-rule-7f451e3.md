# Review — FM-032, this round's continuation at 7f451e3 (2026-09-30, Reviewer, session `8e509911/reviewer-59`)

Reviewed: 7f451e3bfe89a317caf2972fd5831abc3aac0869

- **Branch:** `fm/032-the-ratio-command-and-the-check-outputs-rule`, tip `7f451e3` = `origin/fm/032-…` (one `git fetch
  origin`, 14:08, no `--prune`); two commits on my verdict `28b7a38` by the Implementer seat (`8e509911/implementer-59`,
  Sonnet 5.5): `0d4bf34` merges `7e7c8ac`, `7f451e3` RV-728 (a) and RV-729 (f). `origin/main` is now `7380039`.
- **Tier: code**, the continuation of the re-verification on `8f3f5ea`; the same ids, none new.
- **Independence: same session** — a sub-agent of Principal session 8e509911 (seat `reviewer-59`).
- **Verdict: READY.** RV-728 (a) and RV-729 (f) are closed; RV-726, RV-727, RV-728 (b)(c)(d) and RV-729 (a)–(e) were closed
  on `8f3f5ea`. No finding is open.

## What I ran (on `7f451e3`)

| run | result |
|---|---|
| the merge `0d4bf34`, `git show --remerge-diff` | one file: FM-006's ship log, where both sides added a 2026-09-30 row at the top; both rows are kept (main's *Signals* row first, this branch's check-output row below it), nothing else changed; no other file differs from git's own merge |
| the deletion | `jev-gate-test-score-output-2026-09-23.txt` is gone from the tree; `git show 65d5d43:<path> \| shasum -a 256` = `a75fe8d1…d5ea`, `git rev-parse 65d5d43:<path>` = `e6fa25f8…c78c`, 44 lines — the block's `sha256`, `blob` and `held_at`, and the prose says which is which |
| a fresh scorer run, from its folder, on the two committed responses | exit 0 on 3.14.3 and on 3.9.6; both outputs are byte-identical to `65d5d43`'s file (sha256 equal); the first fatal gates per run, counted from the fresh output — run 1 G0 2 · G1 9 · G2 3 · G4 2 · survives 1, run 2 G0 6 · G1 6 · G2 2 · G4 1 · survives 2 — and the verdict line equal to the record's summary |
| the new check, lifted verbatim into a scratch harness, five trees | the tip's (block, no file): ok · no block: FAIL · main's shape (the file, no block): FAIL · a wrong `sha256` in the block: FAIL · the block and the file both: FAIL — never a traceback |
| `git diff --numstat origin/main...HEAD` (merge base `7e7c8ac`, also against `7380039`), 14:09:51 | **records +543 −33,575, product +547 −2, 1.0:1** — the page's four numbers; no binary, no rename |
| `--check`, 14:10:38 · `--session-check` | exit 0 — *INDEX.md is up to date — 42 trackers*, *judged before build … every build commit under a judged In Progress tracker*, *the Owner's two sections: guarded* · exit 0 |
| `git merge-tree --write-tree origin/main HEAD`, 14:11 | clean against `7380039` (`406f9988`): main's six new commits touch FM-006's tracker (changed on both sides, and it merges clean), its evidence, a review and two workflows — no second merge is needed, and `--queue` will read it clean |
| front matter · trailers | no line between the fences changes in `origin/main...HEAD`; `7f451e3` carries `Session: 8e509911/implementer-59`, `Worktree: shoalmark-impl-4`, `Co-Authored-By: Claude Sonnet 5.5`, the merge `Session:` and `Worktree:` |
| suites | **not re-run.** Since `8f3f5ea` the only code change is `test_shoalmark.py`'s new check (run above in isolation) and one reworded message; the merge brought no `.py`, and main since then only workflows. `test_shoalmark.py` parses on 3.14.3 and 3.9.6. My full runs on `8f3f5ea` (568 / 148 / 565 / 148, 11:53–12:28) and the Implementer's on this tip (569 with `SHOALMARK_REGENERATE=1` and 0 skipped / 148; 566 with 3 skipped loudly / 148) differ by exactly this check |

## The findings

**RV-728 (a) · P3 — closed.** The output is deleted and replaced, at the claim-screen record's scorer paragraph, by its
summary: the command, both Pythons, the per-gate counts per run, the controls, the repeat, the verdict, the file's sha256,
its git blob and the commit that holds it, and a JSON block. The always-on check re-runs the scorer with `sys.executable`
and compares the sha256; it fails without the block or with the file still present. FM-032's *What stays* now says the
ruling is applied *on the Owner's word of 11:3x*.

**RV-729 (f) · P3 — closed.** The page names `origin/main` and says its merge base is the last merge of main into the
branch. `origin/main` has moved past the `7e7c8ac` it names (to `7380039`), but the merge base is still `7e7c8ac`, and the
page's four numbers are exact against both.

## The quality read, this round

The commit is exact and closes both items as the fix texts asked. Its check is sound: planted, verified in isolation, and
failing in every wrong tree. Its body states what was wrong, what changed and the proof.

## Unproven here

CI (no pull request); Windows; a machine with no tz database. The Owner's word of 11:3x, which is not in git.

## For the record

This file adds 52 record lines, no product line: after it the change reads records +595 −33,575, product +547 −2.

path 5 — a merge rules nothing.
