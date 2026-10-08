From: unavailable — `--whoami` reported no `seat.session`; the review did not change that configuration.

# FM-045: v0.19.2, independent critical review at 9a7ed43

This pass ran in a session the Owner started, independent of the Planner's.

Verdict: **NOT READY**
Reviewed: 9a7ed4369b7e65961244a48dad0b263839660080.
Scope: `git diff 85a53ca 9a7ed43` and `git log 85a53ca..9a7ed43`; #150 and #151, already in the base, are excluded.
Tier: critical (release and board read-only gate). The scoped paths include product code and tests; this is a code pass.

## What holds

- **The original defect is fixed.** `READ_ONLY_GIT` gains only `ls-tree`; `read_only_git` itself is unchanged. The two tree-listing argv forms pass, while their `--output` and foreign `-c` variants are refused. The original shape passes all four combinations of origin/HEAD set/unset and in-process/program execution: exit 0, the board written, no stopped line, the answer shown on its way. With v0.19.1's tool, all four stop at `ls-tree` with exit 4 and the check fails.
- **The product diff is narrow.** All changed product lines were read. An AST comparison finds no changed function or class body. The new fourteen-entry `NEVER_IN_BOARD_RUN` table is used by tests, not product execution. `ls-remote` is in that table, and the board's default-branch lookup explicitly avoids asking origin.
- **Check A passes its supplied controls.** The current-source check finds 29 command names, fourteen classified as never started by the board, no overlap or unclassified command, and no unread form. All twelve supplied static controls pass. See RV-2780.
- **The runtime check passes its supplied control.** Its isolated run records 109 starts and detects `ls-tree` when temporarily classified as never started. See RV-2781.
- **Check B uses real operations and installed hooks.** Its fixtures install hooks only into disposable repositories. `git switch`, `git merge --no-ff`, and `git rebase` invoke them; Trace2 supplies hook exit codes. `--answer` reaches `board_after_act`, and the asserted message identifies the checkout-hook rebuild. Each event's shared judgment checks exit 0, the required hook and all observed hook exits, changed board bytes, the newly expected content, and absence of stopped/not-refreshed/traceback lines. Subversion performs real local `update` and `switch`, followed by `--html-only` as documented. The measured case counts and controls are below.
- **The matrix covers the listed shapes with synthetic data.** Its eight Git fixtures cover in-tree signers with generated signing keys, local and origin answer branches, a linked worktree, a moved tracker folder, origin/HEAD set and unset, 304 trackers, and a foreign hook runner. A ninth fixture covers Subversion. The new matrix has no Windows/macOS skip guard. Missing `svn` or `svnadmin` produces a named two-check skip and a final incomplete-pass summary. CI defines five jobs and installs Subversion; no remote CI result was consulted, so no cross-platform run result is claimed here.
- **The release pins and upgrade instructions agree.** Commit `09d5b31386d2764d331d740d23acc479500ed1b1` changes exactly VERSION, CHANGELOG.md, both ADOPT files, and both setup pages. VERSION is 0.19.2; both pins equal the reviewed `shoalmark.py` SHA-256, `5dfcbff1115b4aef67ddd4e280451dc17217d0ccd5b7403289082199c6660d2f`; both setup pages name v0.19.2. The changelog instructs another `--install-hook` on the default branch, then one `--check`. Its proposed date is not treated as a defect. The landing label and footer still name v0.19.1, so that release requirement is unmet; see RV-2782.
- **Claims and record scope.** The new changelog and FM-045 record correctly describe the original failure and its repair. Their classification/recording claims need the corrections identified above. The added prose was read for identifying private detail; none was found in the scoped additions. The requirements folder supplies the Stage 0 convention only, with no applicable requirement IDs to cite.

## Findings

- **RV-2780 · P2** · `test_shoalmark.py:1979` — **Blocks the tag.**
- **RV-2781 · P2** · `test_shoalmark.py:1660` — **Blocks the tag.**
- **RV-2782 · P3** · `overrides/landing.html:326` (also :525–526) — The release label, footer link, date, and release description still advertise v0.19.1. **Does not independently block the tag; fix forward.**
- RV-2783: recorded privately

## Commands and controls

Times are literal `date` outputs; none is estimated. Runs that need commits, branches, hook installation, or deliberate mutations use disposable repositories outside the reviewed worktree. Test subprocesses after the initial core/check batch run with network denied; nothing was installed, fetched from a network service, pushed, tagged, or committed in the reviewed repository.

- `Thu Oct  8 10:44:48 CEST 2026`: read the brief and verify its SHA-256 (`090ee9d524ff11735b47e0bb0ef0986e2da18c16be897dbd40a424c891f86116`); `git rev-parse HEAD` matches the full reviewed SHA.
- `Thu Oct  8 10:44:57 CEST 2026`: `--next`, `--whoami`, initial `git status --short`, AGENTS.md, requirements, review example, scope/log and check discovery. Initial status is empty; `--whoami` cannot print a seat identity because `seat.session` is absent. No identity configuration was written.
- Source and acceptance reads: `Thu Oct  8 10:45:13 CEST 2026` (FM-045, requirements, scoped product diff, log and single-check runner); `Thu Oct  8 10:45:26 CEST 2026` (read-only guard and recorder); `Thu Oct  8 10:45:50 CEST 2026` and `Thu Oct  8 10:45:56 CEST 2026` (the static reader and its controls); `Thu Oct  8 10:46:05 CEST 2026` and `Thu Oct  8 10:46:16 CEST 2026` (matrix, runtime check and platform skips).
- Release/claim reads: `Thu Oct  8 10:46:46 CEST 2026` (documentation/record diff, release commit and source hash); `Thu Oct  8 10:47:02 CEST 2026` and `Thu Oct  8 10:47:46 CEST 2026` (landing/workflow discovery and board-after-act); `Thu Oct  8 10:48:37 CEST 2026` (actual workflows, landing labels and local `git help ls-tree`). The local Git manual was read without network access.
- `Thu Oct  8 10:52:08 CEST 2026`: `git diff --check 85a53ca 9a7ed43`, exit 0; focused results and control outputs read.
- `Thu Oct  8 10:59:21 CEST 2026` to `Thu Oct  8 10:59:22 CEST 2026`: AST comparison of product functions/classes against the base (no changed body), both pin hashes, both setup tags, and `git diff-tree` of the release commit verified; status still empty.
- `Thu Oct  8 11:01:57 CEST 2026`: scoped record additions checked again for identifying paths and addresses; the classification table has no product-code consumer.

| Command | Start (`date`) | End (`date`) | Result |
|---|---|---|---|
| `python3 -m py_compile shoalmark.py test_shoalmark.py test_core.py` | Thu Oct  8 10:45:45 CEST 2026 | Thu Oct  8 10:45:46 CEST 2026 | exit 0 |
| `python3 -u test_core.py` | Thu Oct  8 10:45:46 CEST 2026 | Thu Oct  8 10:46:23 CEST 2026 | exit 0; 158 checks, all green |
| `python3 shoalmark.py --check` | Thu Oct  8 10:46:23 CEST 2026 | Thu Oct  8 10:46:32 CEST 2026 | exit 0; index current, judgment and Owner-section gates pass |

The focused runs use `python3 -u work-tracker/evidence/FM-006/run-one-check.py`; its current-head checks run against the reviewed tool in a temporary clone. The v0.19.1 control uses `--tool v0.19.1`.

| Focused block | Start (`date`) | End (`date`) | Result |
|---|---|---|---|
| read-only list | Thu Oct  8 10:47:38 CEST 2026 | Thu Oct  8 10:47:52 CEST 2026 | exit 0; 1 passed, 0 failed |
| static classification and controls | Thu Oct  8 10:47:52 CEST 2026 | Thu Oct  8 10:48:26 CEST 2026 | exit 0; 2 passed, 0 failed |
| original shape | Thu Oct  8 10:48:26 CEST 2026 | Thu Oct  8 10:48:45 CEST 2026 | exit 0; 1 passed, 0 failed |
| v0.19.1 negative control | Thu Oct  8 10:48:45 CEST 2026 | Thu Oct  8 10:49:03 CEST 2026 | exit 1; 0 passed, 1 failed (expected negative control) |
| runtime classification and control | Thu Oct  8 10:49:03 CEST 2026 | Thu Oct  8 10:50:16 CEST 2026 | exit 0; 1 passed, 0 failed |

All matrix blocks use the same runner with `--block` selecting the corresponding fixture in `test_shoalmark.py` and check-name filter `FM-045 · the board matrix`. Each removal-control check passes only when the matrix's own judgment fails for the missing hook.

| Matrix block | Start (`date`) | End (`date`) | Result |
|---|---|---|---|
| signers | Thu Oct  8 10:51:03 CEST 2026 | Thu Oct  8 10:52:39 CEST 2026 | exit 0; 4 passed |
| answer branches | Thu Oct  8 10:52:39 CEST 2026 | Thu Oct  8 10:54:32 CEST 2026 | exit 0; 4 passed |
| linked worktree | Thu Oct  8 10:54:32 CEST 2026 | Thu Oct  8 10:56:27 CEST 2026 | exit 0; 4 passed |
| moved tracker folder | Thu Oct  8 10:56:27 CEST 2026 | Thu Oct  8 10:58:12 CEST 2026 | exit 0; 4 passed |
| origin HEAD set | Thu Oct  8 10:58:12 CEST 2026 | Thu Oct  8 10:59:53 CEST 2026 | exit 0; 4 passed |
| origin HEAD unset | Thu Oct  8 10:59:53 CEST 2026 | Thu Oct  8 11:01:28 CEST 2026 | exit 0; 4 passed |
| 304 trackers | Thu Oct  8 11:01:28 CEST 2026 | Thu Oct  8 11:03:04 CEST 2026 | exit 0; 4 passed |
| foreign hook runner | Thu Oct  8 11:03:04 CEST 2026 | Thu Oct  8 11:04:35 CEST 2026 | exit 0; 5 passed |
| Subversion | Thu Oct  8 11:04:35 CEST 2026 | Thu Oct  8 11:05:48 CEST 2026 | exit 0; 2 passed |
| removed hook controls | Thu Oct  8 11:05:48 CEST 2026 | Thu Oct  8 11:07:06 CEST 2026 | exit 0; 3 passed |

Matrix total: 35 positive checks across all nine shapes, plus three hook-removal controls; 38 passed, none skipped. With `post-checkout` or `post-merge` removed, the corresponding board does not change; with `post-rewrite` removed, the rebase still has its earlier checkout refresh but lacks the expected post-replay content. All three fail the matrix judgment as required.

| Independent control | Start (`date`) | End (`date`) | Result |
|---|---|---|---|
| Temporary-copy classifier probes | Thu Oct  8 10:49:35 CEST 2026 | Thu Oct  8 10:52:08 CEST 2026 | detailed evidence recorded privately |
| Matrix recorder probe | Thu Oct  8 10:56:22 CEST 2026 | Thu Oct  8 10:57:59 CEST 2026 | all four event judgments pass; Trace2 sees 11 tree listings; detailed evidence recorded privately |
| Missing-Subversion simulation (execute the suite's actual skip branch with `_SVN=None`) | Thu Oct  8 11:06:42 CEST 2026 | Thu Oct  8 11:06:43 CEST 2026 | named two-check skip and explicit incomplete-pass summary |

RV-2783: recorded privately

The full `python3 -u test_shoalmark.py` was attempted from `Thu Oct  8 10:46:36 CEST 2026` to `Thu Oct  8 11:09:39 CEST 2026`, under `sandbox-exec -p '(version 1)(allow default)(deny network*)'`. It exited 1 at the existing loopback-server fixture, `test_shoalmark.py:6935`: binding a local socket raised `PermissionError: [Errno 1] Operation not permitted`. At that point 643 checks had passed and no check assertion had failed; 16 browser-block skip notices named 39 checks because the browser could not launch. The suite did not reach its end, so this is an incomplete run, not a full-suite pass or an asserted patch regression. The FM-045 matrix and runtime block were run separately, as recorded above. No network exception was made to complete the broader suite.

Final verification at `Thu Oct  8 11:11:52 CEST 2026`: `git rev-parse HEAD` is the reviewed SHA; `git status --short` is empty. The worktree is clean. No tracked-file restoration was necessary.

Record effect: one public verdict prepared and the required private finding; no product or repository file changed. This is review evidence, not a claim of reducing the records-to-code ratio.
