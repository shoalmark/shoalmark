# FM-024 — the Reviewer's scoped check of D2's fix round, at b58fe45

Verdict: **READY**. RV-2200 … RV-2206 are closed, and this check finds nothing new. The tool, the tests and the pages are the fixes tried at the pass on 87e2e1b, byte for byte, except for the three deviations the Builder names. Each of those stands.
Reviewed: b58fe4587ae984c84e9e900947a5e38547e79f56 — `8488f56..b58fe45`, a scoped check of the fix round on the verdict at 8488f56.
Reviewer: b3bdb000/reviewer-78 (claude-opus-5-5, max), `reviewer@seat` unsigned, worktree shoalmark-review-11, 10:06–10:13 CEST on 2026-10-01. Independence: the same session as the build (b3bdb000/implementer-77), so not independent.
Tier: code (shoalmark.py, test_shoalmark.py, shoalmark.toml). Not re-read: what the pass at 87e2e1b held. No full local run: it comes after phase 2.

## Items, one line each
- **4105114, RV-2200, RV-2203, RV-2204, RV-2205.** Diffed against the scratch copy of the pass, `shoalmark.py` is the tried fix byte for byte:
  - the six lines name `owner` for an Owner at the top;
  - the guard says *is refused here, so it names nobody — <why>*;
  - a tag named `owner` is told to take another name;
  - `--schema`'s two rows read as written.
  The tests match the tried ones except for one check name. All four closed.
- **Deviation 1, a check name** (test_shoalmark.py:5644): FM-037's clause 5 now reads *their own unsigned change passes on their name*. It stands: the line moved with its pin, and a person is they (AGENTS.md). The other check names keep their words.
- **Deviation 2, the CHANGELOG clause.** The bullet (e570b5d) is the verdict's text, plus *— this repository does, until the branches open at the merge have merged main*. It stands. It is true at this tree, and *this repository* means shoalmark's own, as the CHANGELOG's other bullets use it.
- **Deviation 3, RV-2205 (a).** The row ends on *The tool knows the Owner, and three seats with their rights built in — `planner` ask · close · triage, `reviewer` triage, `builder` none*. That is D1's phrase as filed in FM-006, the seat names in code marks as README §*Seats* and FM-006's seats page carry them. It stands.
- **9f2aac5, RV-2201.** README's six lines, the triage pages and the index pages, English and German, read as the verdict wrote them. The tip merges clean with `fm/006-what-a-stranger-meets-first` at 3fd5063 (`git merge-tree`). Closed.
- **e570b5d, RV-2202.**
  - `shoalmark.toml` keeps `[seats] owner` beside the top-level line, the same. Its comment says why, and until when.
  - Read in process, three pairs give the same seats, rights, `may_answer()` and `owners_of`: b269cdc's tool with b269cdc's configuration, b269cdc's tool with this tip's configuration, and this tip's tool with its own. So an older copy still reads the Owner through the overlap. Closed.
- **b58fe45, RV-2202 and RV-2206**, in FM-024's *What is true now*: the overlap, and until when; and RV-2206's line as the verdict wrote it. Closed.
- **One count.** 4105114's message says five new or moved checks fail beside 87e2e1b's tool. Six do, the S4 check included. Git is its record, and this line corrects it.

## Controls
- Setup, 10:06:50: one fetch; detached at b58fe45, which equals `ls-remote`; clean. `--whoami`: `To: b3bdb000/reviewer-78 reviewer (shoalmark-review-11) · claude-opus-5-5 · max`.
- The seat, owner and guard blocks at the tip in this worktree, ended 10:10:52: 117 ok, 0 failed. These are test_shoalmark.py 1–108, 399–600, 692–993, 2829–3197, 3546–3625 (with S4), 3724–3730 and 5492–5737 (FM-037, with the real history).
- The identity and D2 blocks on Python 3.9.6, 10:11:38: 34 ok.
- The same tests beside 87e2e1b's tool, ended 10:10:51: 110 ok, 1 skipped, and 6 failed — the four new checks and the two moved pins.
- test_core.py, 10:11:14: 158 ok, exit 0.
- `--check` (10:08:55), `--session-check`, and `--owner` (10:09:04) exit 0 each. The guard reads origin/main and guards.

Four numbers for this verdict: records +34, product 0.
Next: nothing goes back. Phase 2 comes after 11:00 (the key rename, the bot addresses, `gtm`); then this Reviewer and the Owner's cold session take its tip, and the full local run comes before ready. The `[seats] owner` line goes once the open branches have merged main, as FM-024 says.
