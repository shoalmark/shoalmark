# FM-005 — the Reviewer's verification of the fix round on `fm/005-a-shipped-tracker-names-its-commit` at 072c03b

Verdict: **READY WITH FINDINGS**. RV-2150 … RV-2159 are closed. Three new findings, all P3 (RV-2160, RV-2161, RV-2162), and none of them is a fault of the round's code.
Reviewed: 072c03b3ec6bcbd580fc5da41790eae1d7a502ce, the round `e18461c..072c03b` on top of the verdict of 6890292, which stands for everything below e18461c.
Reviewer: b3bdb000/reviewer-74 (claude-opus-5-5, max), `reviewer@seat` unsigned, worktree shoalmark-review-9, 02:06–02:59 CEST on 2026-10-01. Independence: the same session as the build (b3bdb000/implementer-73), so not independent.
Tier: code. Read: `git diff e18461c 072c03b` whole — 4324476 (RV-2150, and the corrections RV-2159 (a) and (b) asked for), a36cf2e (RV-2151), d6ed788 (RV-2156…2159), b3fbbc9 (RV-2152…2155) and 072c03b (FM-005).

## Closures (each falsifier re-run against 072c03b)
- **RV-2150 closed.** A working copy at the repository's root: a records-only revision is refused (exit 4) and the feature's revision passes. `/trunk` is unchanged.
- **RV-2151 closed.**
  - `AP-600-über.md` and `AP-601-say "hi".md` moved to `Shipped` are refused by the pre-commit run, by the installed hook and by `--check`, and so is a merge that brings the move.
  - Records-only commits under `say "hi".md`, a tab and an umlaut are each refused.
  - The rights now see these names: a seat without `close` closing `AP-600-über.md` is refused (exit 4), where e18461c let it through.
- **RV-2152 closed.** `git commit -a`, `git commit <path>`, and a move staged bare while the working tree names the feature are each refused by the hook, and no commit is made. The control (the index names the feature, the working tree does not) passes.
- **RV-2153 closed.** An old `Shipped` tracker renamed passes, and a rename that also moves a tracker to `Shipped` is refused. The departure, `ls-tree -z` split on NUL, is right: an old name `AP-600-über.md` renamed passes, where a newline split would read git's quoted name and refuse it.
- **RV-2154 closed.** A tracker linked from outside: exit 0, no traceback.
- **RV-2155 closed.** The full 64-character SHA-256 hash passes. Seven characters two commits share read *names more than one commit — write more of its hash*. Still one `cat-file` call, and the cost check counts three calls.
- **RV-2156 closed.** `way5_` was added to AP-520, AP-507, AP-513, AP-515, C5-003 (`err_s`) and C5-012, and the new checks assert the way through.
- **RV-2157 closed.** test_core.py:381, :394, :546 and shoalmark.py:2503, :3781, :3937 read as written, and `desc.ended` reads `ausgeliefert oder ohne Auslieferung geschlossen` in both places.
- **RV-2158 closed.** README §5's row has `(on Subversion `… no revision behind it`)` and the squash or rebase sentence.
- **RV-2159 closed.** 4324476's message states (a) and (b), and `svn_shipped_moves`'s docstring lists the calls as counted.

## New findings
- **RV-2160 · P3 · The CHANGELOG does not say what the round changed for a repository that upgrades.**
  - Before this round, the pre-commit run read `.git/index` and the working tree. So a `close` that a seat without the right made with `git commit -a` passed the hook, and only `--check` refused it (tested on e18461c: hook exit 0, commit made). Now the hook refuses it (exit 1, no commit), and the rights also read tracker names git quotes. The installed hook's own line changed too, and nothing rewrites an installed hook but `--install-hook`.
  - **Fix:** under `## Unreleased — 0.19.0`, after FM-005's bullet, add: *- **The pre-commit run judges the commit being made, every file name as it is (FM-005's review).** `git commit -a` and `git commit <path>` hand the hook an index of their own, and the gate read `.git/index` and the working tree, so the rights and the `Shipped` rule judged such a commit only in `--check`; a tracker whose file name git quotes (a non-ASCII byte, a `"`) was read by neither. Both are judged at commit time now. *On upgrade:* a `close`, `answer` or `triage` made that way is refused by the hook, where only `--check` refused it; run `--install-hook` again so the hook also runs the gate for a name git quotes.*
- **RV-2161 · P3 · The RV-2152 check's three attempts share one history.** test_shoalmark.py:3255–3257 reset with a bare `git reset -q --hard`. On a tool that lets the `-a` commit through, the commit stays, and the next two attempts find nothing to commit. On e18461c's tool the check reads *(saw 0, 1, 1)*, and the 1s are not the rule's. The check still fails there, but its tuple misreports. **Fix:** in those three lines, `git(root, "reset", "-q", "--hard", head_)`.
- **RV-2162 · P3 · Found on the way, outside this change: with the tool's root below the repository's top, the installed hook never runs the gate.**
  - `install_hook` writes `{dir}`, `{config}` and `{tool}` relative to the tool's root (`dir=TRACKER_DIR.relative_to(ROOT)`). `git diff --cached --name-only` names paths from the top. So with the root at `proj/`, the reproduction commits through the installed hook as a plain commit, with `-a` and with `<path>` (exit 0, commit made), and `--check` refuses it (exit 4). The hook line is the same at 1197e80.
  - **Fix:** one line in FM-005's *Known, not fixed here* (AGENTS.md rule 6): *the pre-commit hook `--install-hook` writes names the tracker directory, the configuration and the tool from the tool's root, and git names staged paths from the repository's top: where the root is below the top, the hook never runs the gate and `--check` judges; older than this branch.* If the Planner wants it fixed, it is a `tags: bug` filing: the three paths prefixed by `git rev-parse --show-prefix`.

## The Builder's two lines — READY holds with both
- (a) **`--amend` dropping the named row passes the hook, and `--check` refuses it (exit 4, tested).** RV-2152's fix text itself left the amend to `--check`, because the hook cannot tell an amend and FM-033's hook reads it the same way. It is a hook-only miss: P3 by AGENTS.md, and recorded.
- (b) **`rights_problems`' `relative_to(ROOT)` traceback** for a tracker linked from outside with `[seats]` set exits 1 with a `ValueError` at this tip and at 1197e80 alike (tested). It is older than the branch, outside the change, and recorded.

## What the round itself changed, attacked
- **The rights on plain names read exactly as before.** I ran the 26 blocks that name `[seats]`, `seat.session` or a right, in nine groups of one process each: 168 ok, 0 failed at the tip, and the same 168 beside e18461c's tool. Run as one process, out of the suite's order, a block before FM-008's inherits state and both tools fail alike: a runner artifact.
- **The hook's index.** A plain commit, `-a` and `<path>` behave right in a linked worktree. git exports `GIT_INDEX_FILE=.git/index`, relative, for a plain commit, and absolute for `-a` and `<path>`. The relative one resolves from a subdirectory, because git moves to the top before it reads the index (tested).
- **The rename lookup.** A non-ASCII old or new name passes. A rename with a move to `Shipped`, and a new tracker filed as `Shipped`, are refused.
- **The hook's grep** (`core.quotePath=false`, `^"?`): plain names are matched as before, and the installed hook now refuses the move of `AP-600-über.md`.
- FM-005 says what was fixed and what is known, with `next: review`. No status line changes on the branch, and `--check` here exits 0.

## Controls, one line each
- Setup, 02:06:16: `git status --short` empty; one fetch; detached at 072c03b, which equals `ls-remote`. `--whoami`: `To: b3bdb000/reviewer-74 reviewer (shoalmark-review-9) · claude-opus-5-5 · max`.
- The FM-005 blocks (git, the working copy below the top, S, the story rendered) and the suite's Subversion part, nine blocks, the tip's tool, 02:13:59–02:16:26: 74 ok, 0 failed, 0 skipped.
- The same beside e18461c's tool, with RV-2154's crash recorded so the run goes on, 02:18:50–02:21:17: 64 ok, 10 failed. The failures are every new refused case: RV-2151 ×4, RV-2152, RV-2153, RV-2154, RV-2155 ×2, and RV-2150 on Subversion. The two new controls pass on both tools.
- The seat and rights blocks, nine groups: 168 ok, 0 failed at the tip (02:31:52–02:38:18), and 168 ok, 0 failed beside e18461c's tool (02:38:32–02:45:03).
- The `ended` blocks (the board, the German board, FM-033's raise): 91 ok, 0 failed at the tip and beside e18461c's tool (02:50:56–02:53:08).
- test_core.py at the tip, 02:53:08–02:53:19: 158 ok, all green, exit 0.
- No rendered check failed, and the window of FM-028's clocks was past.

Quality read: the round is the verdict's fix texts, applied exactly, with one well-judged departure (`ls-tree -z`) and two checks it was not asked for that earn their place (the RV-2152 control, and the merge that brings a quoted name). `index_env()` names the hook's index once, but `pending_judgement` (:5521) and `triage_pending` (:5856) still write the same expression inline. That is one fact in three places, for a later refactor and not a defect. The rest reads clean.
Four numbers for this verdict: records +54, product 0.
Next: the Builder fixes RV-2160 and RV-2161 and writes RV-2162's line, the Reviewer verifies, and then the Owner opens the pull request.
