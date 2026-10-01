# FM-005 — the Reviewer's verification of 6e05612 on `fm/005-a-shipped-tracker-names-its-commit` (PR 143)

Verdict: **READY WITH FINDINGS**. The one commit is right, and it brings no new finding. RV-2160, RV-2161 and RV-2162, all P3 from the verdict on dcf8606, stay open as recorded there.
Reviewed: 6e056122527986b384dbb351e1dd0d24579e06e3, one commit on dcf8606.
Reviewer: b3bdb000/reviewer-74 (claude-opus-5-5, max), `reviewer@seat` unsigned, worktree shoalmark-review-9, 07:43–07:52 CEST on 2026-10-01. Independence: the same session as the build (b3bdb000/implementer-73), so not independent.
Tier: code. Read: `git show 6e05612` whole — test_shoalmark.py:183 and :1236–1237, test_core.py:369, and one sentence in FM-005.

**My miss, said once.** My first pass ran the story and German browser blocks, but not the board block, FM-035 or FM-039. My grep for *done* (RV-2157) read check names, not the patterns at test_shoalmark.py:183 and :1237. So both stale expectations went past me. CI run 36816934141 found the one at :1237, and the one at :183 passed vacuously.

## What holds
1. **The three expectations read what they claim.** I tested each on two built pages: this tree's, and 1197e80's, whose fifth key is still *done*.
   - **The two `BOARD=` patterns** (`[^}]*`, test_shoalmark.py:183 and test_core.py:369). On this tree they match. On the *done* page they do not.
   - **The old greedy pattern** (`.*done:`, re.S) matches both pages. On this tree it lands 14,053 characters past `BOARD=`, inside an act dialog's ``sign(… `done: ${w}` …)``. So it passed vacuously, as reported.
   - **The rendered check** (`backlog.*?ended`). On this tree it matches, and the match ends on the `▸ ended` header. On the *done* page it does not match. The old `backlog.*?done` fails here, as in CI. The headers render in order (progress, triage, triaged, backlog, ended); *A shipped one* is folded, and *2 trackers* is said.
   - *intended* is nowhere in the shown text, and the board's rows and headers cannot show it: it appears only in a tracker view's hand-over logic, where it is filtered out. So the substring `ended` reads the header.
2. **No other check reads the fifth section as *done*.** `git grep -n -E 'backlog.{0,12}done' -- 'test_*.py'` finds only test_shoalmark.py:1784, C4's list of English words that must not show on the German board (*done* and *ended* both). A wider grep finds only checks that *done* labels are absent, and an act's kind.
3. **The browser blocks.**
   - The board block, FM-035 and FM-039 at 6e05612: 5 ok, 0 failed.
   - On dcf8606's test file, with the same tool: 2 ok, 3 failed — the board check, FM-035 and FM-039, the three CI failed.
   - No full local run of my own: the verdict commit adds only this file (the Owner's ruling). The Builder's full run on this tip (651 ok) is its report, and I did not repeat it.
4. **FM-005** gains one sentence: CI's three failures, the fifth section's word, and that no seat had run that check before the push. Nothing else in the tracker changed, and the commit touches three files.

## Controls, one line each
- Setup, 07:43:07: `git status --short` empty; one fetch; detached at 6e05612, which equals `ls-remote`. `--whoami`: `To: b3bdb000/reviewer-74 reviewer (shoalmark-review-9) · claude-opus-5-5 · max`.
- The board block, FM-035 and FM-039 (test_shoalmark.py:1224–1292, built from the file's own markers), Chrome installed: 6e05612 07:44:21–07:45:51, 5 ok and 0 failed; dcf8606's test file 07:45:51–07:47:21, 2 ok and 3 failed.
- The patterns on built pages (this tree's tool; 1197e80's, fifth key *done*): new page-source pattern match / no match; old greedy pattern match / match; rendered new match / no match; rendered old no match / match.
- test_core.py at the tip, 07:49:11–07:49:19: 158 ok, all green. The block holding :183 (110–190), 07:49:20–07:49:22: 17 ok, 0 failed.

Quality read: a one-commit fix that names the cause truly, including the vacuous greedy pattern that hid the second copy. Scoping both page-source patterns to the object (`[^}]*`) is the right correction, not just a word swap. The rest reads clean.
Four numbers for this verdict: records +31, product 0.
Next: the Owner's PR 143 runs its final CI on this verdict's head; RV-2160 … RV-2162 (P3) are fixed forward as the Owner rules.
