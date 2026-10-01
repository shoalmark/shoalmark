To: 01a0f6d1 reviewer (shoalmark-cold-switch) · gpt-6-astra · xhigh

# FM-024 — READY WITH FINDINGS: independent cold review of the whole switch

Verdict: **READY WITH FINDINGS** — two P3 findings, RV-2240–2241; no P2 or above found. RV-2240 extends RV-2207.
Reviewed: c3fd46ad0497d8be0c1129443ed677b455569916
Base: ea70e5ef55707b0ce1e57ce8f9da96bf71510cc7 (`origin/main` and the merge base at review).
Tier: **critical code** — the whole `git diff origin/main...c3fd46a`, including configuration, rights, sessions and both languages.
Spec: the Owner's ruling filed in FM-024, *The `[seats]` switch — v0.19.0*, and FM-006's D at `3fd5063` (`origin/fm/006-what-a-stranger-meets-first`).
Independent session: `01a0f6d1`, distinct from the build's `b3bdb000/implementer-77`; identity, model and effort read by `--whoami`.

**RV-2240 · P3 · Alias ownership is ambiguous even without another seat of that name** (`shoalmark.py:5372–5377`).
With `[seats] builder = "build@seat"` and `research = "implementer@seat"`, both authors pass `--session-check` with `Session: 1111aaaa/implementer-1` (exit 0).
The label is the Builder's built-in former name and the Research seat's address alias. It identifies two seats, contrary to the rule that it names its own seat alone.
RV-2207's proposed subtraction of other `[seats]` keys still accepts both: neither key is `implementer`. Its canonical-name collisions also reproduce.
Fix: make alias ownership unambiguous across seats, and test alias-to-alias collisions as well as aliases matching another seat's key; retain unambiguous old labels.
Controls: unknown labels and another seat's unshared former name exit 4; `gtm` passes for `go-to-market` and fails for `research`. This changes attribution, not rights.

**RV-2241 · P3 · The triage pages narrow the documented authorization incorrectly** (`docs/triage.md:121`, `docs/de/triage.md:150`).
The changed text says the exception is the author named by `owner`. `owners_of` also admits seats explicitly granted `answer`, as README already says.
Reproduced with a real SSH-signed commit: top-level `owner="owner@x signed"`, seat `deputy="deputy@x signed"`, `[rights] deputy=["answer"]` on `origin/main`.
A `deputy@x` commit changing the intent passes `triage_guard`: one guarded change, zero refusals. The Owner and deputy are different identities.
Fix both pages to include the explicitly delegated `answer` right, following README; the existing delegation behavior needs no change.

Checks and limits:
- History replay against `25adb57`'s tool/configuration: `6debda1` has 1,102 commits, 813 seat sessions, zero identity/right/signing-mode/session violations; the Builder's counts reproduce.
- At `c3fd46a`: 1,105 commits, 816 seat sessions; including fetched origin branches: 1,186 commits, 897 seat sessions. Zero violations in both ranges after the three intended seat renames.
- All seven bot IDs match live `gh api /users/shoalmark-<seat>%5Bbot%5D` responses and FM-024; seven lists retain the old addresses, and `gtm@seat` belongs to `go-to-market`.
- D2: old/new/both-equal configurations agree; differing Owners, misplaced keys and duplicate identities refuse; Owner rights and the separate refusal wording hold. `b269cdc`'s tool reads the overlap's signed Owner and all four rights.
- Signed `--answer` and `--done`, pushed to disposable local remotes, succeed under old/new/both spellings; all six queue results are `merge: your answer`.
- A real merge bringing an `implementer@seat` commit with its old session label passes after the rename; unrelated labels remain refused.
- Subversion's focused cases cover server identities, refusal of `signed` for seats and a top-level Owner, and the guard's stated exclusion.
- `test_shoalmark.py`: 128 focused checks passed, zero failed (session/identity/D2, seat rights, merges, Subversion, guard and queue blocks); `test_core.py`: 158 passed, zero failed. The full 671-check suite and browser rendering were not rerun.
- `--check`, `--session-check` and `git diff --check` pass at the reviewed tree after worktree setup.
- README, CHANGELOG, `--schema` and changed English/German pages read against the implementation; RV-2241 and RV-2208 identify the remaining text corrections.

The peer report at `74fdb36` is evidence only and changes none of the reviewed product; RV-2208 and RV-2209 remain tracked there. RV-2206 remains recorded in FM-024.
Obsolete: no product path removed by this review; superseded wording belongs in the fixes, and the overlap Owner line stays until older branches have merged main.
Next: fix the session collisions and text findings, resolve RV-2209's evidence line, verify the fixes, then the Owner marks #144 ready; final-head CI and the Planner's gate precede their merge. The v0.19.0 tag is due after the release merge, by the Owner.
Four numbers: records +40, records deletions 0, product additions 0, product deletions 0.
