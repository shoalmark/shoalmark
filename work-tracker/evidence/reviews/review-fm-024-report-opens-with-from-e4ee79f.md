# FM-024 — the Reviewer's code pass on `fm/024-a-report-opens-with-from` at e4ee79f

Verdict: **READY WITH FINDINGS** — two P3 (RV-2170, RV-2171). Both fixes were tried on a scratch copy of this tip, where the FM-024 checks (11) and test_core.py (157) pass.
Reviewed: e4ee79f3d1d7de403ebf5331c884dcb9d5d8821e, on origin/main 1197e80, which is its merge base.
Reviewer: b3bdb000/reviewer-74 (claude-opus-5-5, max), `reviewer@seat` unsigned, worktree shoalmark-review-9, 01:37–01:47 CEST on 2026-10-01, after its verdict e18461c on FM-005's done fix. Independence: the same session as the build (b3bdb000/implementer-75), so not independent.
Tier: code. `git diff --name-only origin/main...HEAD` lists shoalmark.py, test_shoalmark.py, AGENTS.md, README.md, CHANGELOG.md, FM-024 and INDEX.md.
Read: FM-024's section *A report opens with From: — v0.19.0* (the Owner's ruling), AGENTS.md, and `git diff 1197e80...e4ee79f` whole. That is d19a673 (the Planner's filing), then 544aac6, 3648319 and e4ee79f (implementer-75).

## Findings
- **RV-2170 · P3 · Two texts say something untrue about the line.**
  - (a) FM-024:46, the *What is true now* paragraph on PR 139's build, still says `--whoami` (`To: <session> <seat> (<worktree>) · <model> · <effort>`). That paragraph is tracker body, not an append-only record: the Owner's ruling that merged records stay verbatim, as 48708c6 records it, covers the ship log and `evidence/`. It is the one hit of the brief's grep that says what `--whoami` prints and is not a message's target or a record.
  - (b) 544aac6's message says *the four whose names said `To:` say `From:`*. Three check names said it: test_shoalmark.py:1081, :1126 and :1136 at 1197e80.
  - **Fix:**
    - (a) At FM-024:46, write `--whoami` (`To: <session> <seat> (<worktree>) · <model> · <effort>` as PR 139 built it; `From: …` since the fix above).
    - (b) The next fixing commit's message states it, since git is its record (AGENTS.md).
- **RV-2171 · P3 · `--help` explains the line after the `To:` clause.**
  - The inserted *; a message's target is the same identity after `To:`* now stands between the line and *— the session from `seat.session`, the seat from `[seats]`, …*. That clause explains the line, but rendered it reads as if it explained the target. The docstring starts a new sentence there and reads right.
  - **Fix** (shoalmark.py:6577–6580): the four strings become `"`From: <session> <seat> (<worktree>) · <model> · <effort>` — the session from `seat.session`, the seat from `[seats]`, the "`, `"worktree's folder, and the model and effort from the harness's own log, found by the id in `seat.harness` "`, `"(`—` where there is none); a message's target is the same identity after `To:`. "` and `"Reads top-level fields of the log, never its messages; exit 2 where two logs carry the id")`.
  - Tried: it renders as one reading, no check pins the help text, and 11 and 157 pass.

## What holds
1. **The line.** `whoami()` changes one word, `To:` → `From:`, in its one print (shoalmark.py:5050). The identity, the model, the effort, the second line (the log read from), the exit 4 without `seat.session` and the exit 2 for two logs are as they were. The docstring says what it prints and that a message's target is the same identity after `To:`, and reads right (the help: RV-2171).
2. **Rule 8, one text.**
   - AGENTS.md:26–28 and the template's item 9 (shoalmark.py:6908–6910) are equal, number and command aside. I checked this by `--init` in a scratch repository at this tip, with its block diffed against AGENTS.md's.
   - The rule says a report opens with `From:`, as the tool prints it, with the model and effort from the harness's log and never the seat's own word. It says a message names its target with `To:` and the same identity. These are the ruling's words.
   - The new check extracts that rule from both texts and compares them. It fails on 1197e80's tool, and on one word changed in either place.
   - Judged enough for this change. The rest of the block drifted long before it: the template's `ask:` rule (its 7) arrived in 0.13.0 (f4726d3) and never reached AGENTS.md, and the opening's wrap dates to 0.3.0 (7ca0b4d). Closing the drift puts the `ask:` rule into this repository's contract, which is a decision for the Owner, not a side-fix. So the line the Builder wrote into FM-024 (rule 6; the filing freeze, 23 open, admits only bugs) is the right record, and not a finding here. When the drift closes, a check on the whole block can replace this one.
3. **What follows.**
   - README:281 (the table row) and :394 (the example) print `From: …`.
   - The two Unreleased bullets are edited in place (CHANGELOG.md:56, :63–67), under the one `## Unreleased — 0.19.0` heading.
   - Every `To:` left names a message's target: AGENTS.md:28, CHANGELOG.md:66, README.md:281, the docstring, `--help`, the template and the new check.
   - The brief's grep finds, besides these, only records: the Auditor's pastes and raises headed *To: 8e509911 …*, the answered ask, the ruling's own account of the bug (FM-024:313), ship-log rows and `evidence/`. The one exception is RV-2170 (a).
   - `--schema`'s `seat.harness` row, `--init`'s last line and the seat definitions in `.claude/agents/` do not state the line. The tool prints no other `To:` line.
4. **Records already written stay.** Nothing under `evidence/` changed. In FM-024 the branch removed one line, `next: build`, and everything else is added: the ruling, the new paragraph and two ship-log rows at the end. No other tracker changed, and INDEX.md changed only its date and FM-024's Next.
5. **The tests bite** (the controls below): 4 checks fail on 1197e80's tool and all 11 pass at the tip.
6. **The commit messages** cite the Owner's ruling filed in FM-024. 3648319 says truly that the rule's wording is the Planner's pick, for the Reviewer to judge.

## Controls, one line each
- Setup, 01:37:44: `git status --short` empty; one fetch; detached at e4ee79f, which equals `ls-remote`. `--whoami`: `From: b3bdb000/reviewer-74 reviewer (shoalmark-review-9) · claude-opus-5-5 · max`.
- The `--whoami` block and the rule-8 check (test_shoalmark.py:1014–1157), the tip's lines beside the tip's tool, 01:41:39–01:41:45: 11 ok, 0 failed.
- The same lines beside 1197e80's tool, 01:41:45–01:41:49: 7 ok, 4 failed. They are the three whole-line checks (the four identities, the canary, an id with no log) and the rule-8 check, which is the Builder's count of 4.
- test_core.py at the tip, 01:41:58–01:42:08: 157 ok, all green, exit 0.
- `--init` at this tip in a scratch repository, its block diffed against AGENTS.md's: rule 8 equal apart from number and command; the rest differs by the `ask:` rule and the opening's wrap.
- The two fixes, on a scratch copy of the tip: 11 ok, and test_core.py 157 ok.

Quality read: the change is the smallest that does what the ruling says. One word changes in the print; the rule is written once, in the template, and spliced into AGENTS.md; and a check keeps the two equal. The Builder measured the older drift and recorded it rather than widening the change. Its defects are RV-2171, a clause out of order, and RV-2170, a stale paragraph and a miscount; the rest reads clean.
Four numbers for this verdict: records +48, product 0.
Next: the Builder fixes RV-2170 and RV-2171 on this branch; the Reviewer verifies the fixes; then the Owner opens the pull request.
