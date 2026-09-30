# Review — FM-032, the Windows fixes at 503ce7b, the loop's last step (2026-09-30, Reviewer, session `8e509911/reviewer-59`)

Reviewed: 503ce7bddab2d8ccd937250031a92c1fd13891a0

- **Branch:** `fm/032-the-ratio-command-and-the-check-outputs-rule`, PR 131, tip `503ce7b` = `origin/fm/032-…` (one `git
  fetch origin`, 18:46, no `--prune`): three commits on my verdict `7c5be43` by the Implementer seat
  (`8e509911/implementer-59`, Sonnet 5.5, `shoalmark-impl-5`): `7dee740` the three checks that failed on Windows,
  `3a0b98d` merges main `11dd6a9`, `503ce7b` a backslash out of an f-string for 3.9. `origin/main` is `c97d6be`.
- **Tier: code**; the same ids, none new. **Independence: same session** — a sub-agent of Principal session 8e509911.
- **Verdict: READY WITH FINDINGS.** The three test changes are faithful, and the merge loses nothing. One P3 goes forward:
  the page's own-numbers paragraph is stale by two merges (RV-729 g).

## What I ran (on `503ce7b`)

| run | result |
|---|---|
| `git diff 7c5be43..503ce7b -- test_shoalmark.py shoalmark.py` | `test_shoalmark.py` only, from `7dee740` and `503ce7b`; `shoalmark.py` and `test_core.py` change exactly as main's own change (`3feaf28..11dd6a9`) |
| the `--ratio` fallback expectation | where `zoneinfo` has Europe/Berlin, the 22nd's expected line and the separate Berlin-day check (23:30 UTC on the 22nd is the 23rd) are unchanged; without it the 22nd expects both merges, `records +9 −3 product +12 −0 0.8:1 (2 merges, 1 binary)` — the planted data by the merge's own offset, and exactly what the documented fallback prints. The tip's `--ratio` block in my harness: 14 ok with the zone; with `ratio_zone` replaced by `(None, False)`, 13 ok, 0 FAIL, and the Berlin day and the reproduction skipped loudly — a faithful test, not a weaker one |
| the Jev check's CRLF normalisation | `stdout.replace(b"\r\n", b"\n")`, then the exact sha256: the committed bytes with CRLF line ends hash equal after it; one changed character still differs, and a lone `\r` stays — content compared, line ends aside. `503ce7b` moves the expression into `_jev_sha`; the file parses on 3.14.3 and 3.9.6 |
| the `facts.mjs` skip | `_regen_skip(…, 1, "no tz database for Europe/Berlin here (…)")` where `_zone_ok` is false — printed as `skip`, counted in *skipped here* (*NOT a full pass*); where the zone exists (here), the check runs as before |
| the merge `3a0b98d`, `--remerge-diff` | one file, README: the conflict takes main's newer `--queue` row and keeps the branch's `--ratio` row, byte-equal to `7dee740`'s; every other file equals main's change |
| `--check`, 18:47:19 · `--session-check` | exit 0 — *INDEX.md is up to date — 42 trackers*, *judged before build … every build commit under a judged In Progress tracker*, *the Owner's two sections: guarded* · exit 0 |
| `git merge-tree --write-tree origin/main HEAD` | clean against `c97d6be` (`7bff2850`) |
| `gh pr checks 131 -R shoalmark/shoalmark`, 18:48:32 | head `503ce7b`; CodeQL and the three Analyze jobs pass; `suites (windows-latest, 3.9)` and `(windows-latest, 3.12)` **pending**, as are macOS and both Ubuntu jobs |
| suites | **not re-run** (one gate pass per tip): the Implementer's on this tree — 3.14.3 570 / 157, 3.9.6 567 / 157, green, 18:08–18:44 |

## The findings

RV-726 to RV-728 stay closed. **RV-729 (g) · P3 — forward:** the page's own-numbers paragraph names `origin/main` *which
is `7e7c8ac`* and reads records +543 −33,575, product +547 −2; two merges of main later (`3feaf28`, `11dd6a9`) and after my
three later verdicts, `git diff --numstat origin/main...HEAD` (merge base `11dd6a9`) reads **records +640 −33,575, product
+548 −9**. **Fix forward:** name no commit (*the merge base of `origin/main` and the tip*) and state the four numbers at the
merge.

## Unproven here

The Windows jobs (pending at 18:48). The cause of the `facts.mjs` difference on Windows (the Implementer's guess: `TZ=Europe/Berlin`
reaching git with no zone database); the skip keys on Python's `zoneinfo`, so a Windows runner with `tzdata` installed would run
the check again.

## For the record

This file adds 45 record lines, no product line: after it the change reads records +685 −33,575, product +548 −9.

The commit of this file, `92daa68`, carries `Session: 8e509911/reviewer-65`: another seat set this worktree's `seat.session` at
15:44 and I did not re-read it before committing. The verdict is `8e509911/reviewer-59`'s.

path 5 — a merge rules nothing.
