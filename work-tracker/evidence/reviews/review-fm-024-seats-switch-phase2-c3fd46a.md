# FM-024 — the Reviewer's pass on the switch's phase 2, at c3fd46a

Verdict: **READY WITH FINDINGS** — three P3 (RV-2207 … RV-2209), no P2. The switch is built as the Owner's ruling filed in FM-024 has it:
- the keys are `planner` and `builder`;
- each seat's bot address stands beside its old one, and every id equals what GitHub's API returns;
- `gtm` is an address of `go-to-market`;
- both `owner` lines stay.

The history reads as before. `session_names` is needed, and sound for this repository, but it lets a seat's session name another seat (RV-2207). Each fix below was tried on a scratch copy of this tip.
Reviewed: c3fd46ad0497d8be0c1129443ed677b455569916 — `25adb57..c3fd46a`, phase 2, in parallel with the Owner's cold session on the same tip.
Reviewer: b3bdb000/reviewer-78 (claude-opus-5-5, max), `reviewer@seat` unsigned, worktree shoalmark-review-11, 11:08–11:30 CEST on 2026-10-01. Independence: the same session as the build (b3bdb000/implementer-77), so not independent.
Tier: code (shoalmark.py, test_shoalmark.py, shoalmark.toml). Read: the ruling's section in FM-024 and `git diff 25adb57 c3fd46a` whole: b366241 (the Planner's bullet), then implementer-77's 6debda1, 1923f5c, df5a80b and c3fd46a.

## Findings
- **RV-2207 · P3 · `session_names` lets a seat's session name another seat of the same `[seats]`.** Its docstring and the CHANGELOG both say *no other seat's name does*. Run on this tip:
  - With both spellings as two seats, a configuration slice 2's check supports, `planner@seat` with `Session: 1111aaaa/principal-1` passes `--session-check` (exit 0), and so does `builder@seat` with `…/implementer-1`. The reverse is refused.
  - With `reviewer = ["reviewer@seat", "builder@seat"]` beside a seat `builder`, `reviewer@seat` with `…/builder-1` passes.
  - Cause: the former names and the `<name>@seat` names are added whether or not that name is a seat itself (:5377).
  - **Fix:** `` names = {seat, *FORMER_NAMES.get(seat, ())} | {who[:-len("@seat")] for who, _mode in SEATS.get(seat, ()) if who.endswith("@seat")} `` and then `` return names - (set(SEATS) - {seat})   # a name that is another seat of this `[seats]` stays that seat's ``. In the switch block, add a check that both cases above are refused, each naming the other seat, while each seat's own name still passes.
  - Tried: the attacks are refused. The session, identity and switch blocks pass (51), and the new check fails beside this tip's tool. test_core.py passes (158), and the history replay still finds nothing.
- **RV-2208 · P3 · Two lines the switch made untrue.**
  - shoalmark.toml:8 reads *seats commit unsigned as <seat>@seat*. Neither `planner@seat` nor `builder@seat` is an identity here: an ask from either reads *not a seat*. **Fix:** `# who sits where — a seat commits unsigned under an identity its list gives: the old address, or its GitHub App's bot address, whose icon the forge shows (README, *Seat icons on the forge*);`
  - CHANGELOG.md:33 points to *their bot identities (the FM-024 bullet below)*, but the switch is in the bullet on the Owner, above. **Fix:** *(The switch, in the FM-024 bullet on the Owner)*.
- **RV-2209 · P3 · The record does not show the Auditor's check that the ruling names.** The ruling filed in FM-024 has the Auditor check all seven bot ids against GitHub's API before any address changes, and report. FM-024 shows the Planner's read (b366241, 10:39) and the Builder's (before 1923f5c), and no Auditor's report. The ids themselves are right: this pass read all seven at 11:09:52. **Fix:** one line in FM-024's switch section saying who read the ids and when (the Planner at 10:39, the Builder before `1923f5c`, the Reviewer at 11:09:52), and whether the Auditor's report is in or was waived.

## What holds
1. **The configuration** reads as ruled.
   - There are eight seats, `owner` among them; no `gtm`, `principal` or `implementer` key remains.
   - `gtm@seat` sits under `go-to-market` and `datascientist@seat` under `research`. Each list puts the old address first and the bot's beside it.
   - Both `owner` lines are there, and they are the same.
   - `gh api /users/shoalmark-<seat>%5Bbot%5D` returns a `Bot` for each of the seven, and each id equals `[seats]` and b366241's bullet.
2. **The history reads as before.** I replayed it in process, 25adb57's tool and configuration against this tip's, over HEAD and every `origin` branch: 1185 commits, of which 946 are by a seat and 896 carry a Session. Every author maps to the seat it had, renamed, with the rights it held, and every Session passes under the new names as under the old. The Builder's count (1102 and 813) is the same history at 6debda1.
3. **`session_names`, judged hard.**
   - It is needed: beside b366241's tool the two session checks fail. That tool refuses `<id>/implementer-<n>` and `<id>/gtm-<n>`, which are the sessions of the worktrees in flight and of the commits a merge brings.
   - It widens nothing in this repository: none of the names it adds is a seat here. The gap is RV-2207's.
4. **The texts** (df5a80b) are true at this tree, in English and German, apart from RV-2208 and the claim RV-2207 makes true:
   - README §*Seats*, §*Seat icons on the forge*, and §*Sessions* (badge, row, rule and refusals);
   - the setup pages' example and their sentence on the keys;
   - the CHANGELOG's *The switch* and its two older bullets.
   The lines the Builder left are rightly left.
5. **FM-024** says what is built and what follows. PR #144 is open, a draft, at c3fd46a.

## Controls
- Setup, 11:08:43: one fetch; detached at c3fd46a, which equals `ls-remote`; clean. `--whoami`: `To: b3bdb000/reviewer-78 reviewer (shoalmark-review-11) · claude-opus-5-5 · max`.
- GitHub's API, 11:09:52: all seven ids match.
- The history replay, 11:10:36: 0 differences. Again with RV-2207's fix, 11:13:29: 0.
- The session, seat and owner blocks at this tip in this worktree, ended 11:24:25: 149 ok, 0 failed. These are test_shoalmark.py 1–108, 399–1026, 1085–1308, 2862–3230, 3579–3658, 3757–3763 and 5525–5770.
  - Two earlier runs of mine each failed the same 18 checks. My block selection skipped the FM-005 block where the suite rebinds `old`, which the whoami block reuses. The fault was my runner's, not the tip's.
- The identity and switch blocks beside b366241's tool, 11:13:16: 34 ok, 2 failed (the two session checks).
- test_core.py, 11:24:43: 158 ok. `--check` (11:24:46), `--session-check` and `--owner` (11:24:55) exit 0 each.
- RV-2207's fix on the scratch copy, 11:25:42–11:26:29: 51 ok; 1 failed beside this tip's tool; test_core 158.

Quality read: the switch is small and well placed, with one commit for the configuration, one for the texts, and one function for the session rule. `FORMER_NAMES` is a second copy of the former names that `BUILTIN_RIGHTS` already carries; a single table that both read would keep the two from drifting. The rest reads clean.
Four numbers for this verdict: records +55, product 0.
Next: the Builder fixes RV-2207 and RV-2208 on this branch, and the Planner writes RV-2209's line. Then the Reviewer's scoped check, the full local run on the final tip, and the Owner's merge.
