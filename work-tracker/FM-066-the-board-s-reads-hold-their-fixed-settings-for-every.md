---
id: FM-066
status: In Progress
considered: FM-045, FM-057, FM-010
tags: security
next: build
triaged: 2026-10-21
tier: P1
hook: "the board's reads hold their fixed settings for every program a configuration can name"
---

# FM-066 — the board's reads hold their fixed settings for every program a configuration can name

## What is true now

**Filed and judged 2026-10-21: In Progress, P1, for v0.20.1, on the Owner's word, which is recorded privately.**

RV-3529: recorded privately

The board's reads hold their fixed settings for every program a configuration names, and the class test `test_board_settings.py` holds it: a
byte-identical copy of the tool passes every row, and each mutant fails the one row designated to it. The digests' conflict preview is one of the
board's reads, reported as not read wherever a configured merge driver or filter driver could change the merge. `--check` and the plain run read the
trunk from the clone's cached refs and ask origin nothing; where `origin/HEAD` is absent and the cached `origin/main` and `origin/master` name different
commits, they refuse in one line. The queue's `fetch` and `ls-remote` contact origin under the person's own settings, and its `gh pr list` — the open
pull requests (`forge_prs`), and under `--queue` the last day's merged and closed (`forge_closed`) — is started with `nested_git_env()`, which in a
digest and under `--queue` carries the board's settings and git's own lazy-fetch default. No run of the tool calls `origin_default`.

Fix round 2 is built on this branch: the conflict preview runs only where neither driver list names a driver, before and after its `merge-tree`
(`514b736`), or, where a filter driver is configured, where `merge.renormalize` reads false, each filter emptied (`ced9450`); `--check` and the plain run refuse a trunk the cached refs cannot tell (`4d2ff97`); the class test holds the trunk read over three
transports (`9e85439`); and the comments, docstrings, labels and this tracker say what holds now (`1765e80`).

Fix round 3 is built on this branch: `--check` and the plain run refuse a trunk the cached refs cannot tell whatever the working tree holds
(`7f1c13e`), and the class test keeps its module docstring and its comments on git alone (`c66172c`). The review comes next.

- **Held against:** FM-045, whose fix keeps the board's refresh read-only; FM-057, which says what the board read and
  when; and FM-010. None of them owns this, so it is a tracker of its own.

**Every git process the tool starts, read or act.** One row for each, by the function in `shoalmark.py` that starts it. The board's reads run under
the board's settings — `BOARD_SETTINGS`, and where a read compares the working tree, every filter driver the configuration names emptied (`compared`)
— in every run but an act's; the trunk is read from the clone's cached refs, never from origin. An act runs git under the person's own settings, and so
does every read of a run that is an act (`ACT_RUNS`): `--answer`, `--done`, `--due`, `--revoke`, `--clear-ask`, `--vendor`, `--install-hook`, `--init`
and `--session-trailer`. `--owner` and `--standup` end with the queue, and `--queue` is the queue alone: it contacts origin for its pull requests and
branches, its `fetch` and `ls-remote` under the person's own settings, and its `gh pr list` — not a git, so no row below — with the board's settings, as
`nested_git_env()` gives them in those runs; the queue's conflict preview is one of the board's reads. Where `origin/HEAD` is absent and the cached
`origin/main` and `origin/master` name different commits, `--check` and the default run refuse in one line, whatever the working tree holds, which names
`git remote set-head origin --auto` as the person's own command. The last three rows are the git that the hooks `--install-hook` writes start
themselves, in the person's own commit.

| git | Its function | Read or act | Settings |
|---|---|---|---|
| `--exec-path` | `include_targets` | an act — `--install-hook`: the includes the configuration names | the person's |
| `add` | `owner_change` and its `record_refusal` | an act — `--answer`, `--done`, `--due`, `--revoke`: its branch, its commit and its push, and its own reads before it writes | the person's |
| `branch` | `built_on` | one of the board's reads | the board's |
| `branch` | `install_copy` | an act — `--install-hook`: the hooks' copy and where it came from | the person's |
| `branch` | `owner_change` and its `record_refusal`, `undo` | an act — `--answer`, `--done`, `--due`, `--revoke`: its branch, its commit and its push, and its own reads before it writes | the person's |
| `branch` | `repos_naming` | one of the board's reads | the board's |
| `branch` | `revoke_cmd` | an act — `--revoke`: where the answer is, before it writes | the person's |
| `branch` | `standup_where` | one of the board's reads | the board's |
| `cat-file` | `cat_blobs` | one of the board's reads | the board's |
| `cat-file` | `git_ship_verdicts` | one of the board's reads | the board's |
| `cat-file` | `have_not` | one of the board's reads | the board's |
| `cat-file` | `resolve_commits` | one of the board's reads | the board's |
| `cat-file` | `signature_kind` | one of the board's reads | the board's |
| `check-attr` | `driver_paths` | one of the board's reads | the board's |
| `commit` | `owner_change` and its `record_refusal` | an act — `--answer`, `--done`, `--due`, `--revoke`: its branch, its commit and its push, and its own reads before it writes | the person's |
| `config` | `commit_msg_check` | one of the board's reads | the board's |
| `config` | `config_file_problem` | an act — `--install-hook`: every configuration file a worktree reads | the person's |
| `config` | `filter_drivers` | one of the board's reads | the board's |
| `config` | `forge_prs` | one of the board's reads | the board's |
| `config` | `git_user` | one of the board's reads | the board's |
| `config` | `harness_id` | one of the board's reads | the board's |
| `config` | `hooks_folder_problem` | an act — `--install-hook`: the hooks folder | the person's |
| `config` | `include_targets` | an act — `--install-hook`: the includes the configuration names | the person's |
| `config` | `merge_drivers` | one of the board's reads | the board's |
| `config` | `merge_renormalize` | one of the board's reads | the board's |
| `config` | `owner_change` | an act — `--answer`, `--done`, `--due`, `--revoke`: its branch, its commit and its push, and its own reads before it writes | the person's |
| `config` | `promisor_remotes` | one of the board's reads | the board's |
| `config` | `session_problems` | one of the board's reads | the board's |
| `config` | `session_trailer` | an act — `--session-trailer`, in the person's commit: the message's trailers | the person's |
| `config` | `trusted_signers` | one of the board's reads | the board's |
| `config` | `whoami` | one of the board's reads | the board's |
| `diff` | `pending_judgement` | one of the board's reads | the board's |
| `diff` | `read_changes` | one of the board's reads | the board's |
| `diff` | `staged_files` | one of the board's reads | the board's |
| `diff` | `staged_now` | one of the board's reads | the board's |
| `diff` | `tree_changes` | one of the board's reads | the board's |
| `diff` | `worktree_edits` | one of the board's reads — it compares the working tree (`compared`) | the board's, every configured filter driver emptied |
| `fetch` | `forge_prs` | an act — the queue's contact with origin, asking its pull requests and branches and writing their refs | the person's |
| `fetch` | `pushed_branches` | an act — the queue's contact with origin, asking its pull requests and branches and writing their refs | the person's |
| `for-each-ref` | `answer_refs` | one of the board's reads | the board's |
| `for-each-ref` | `commit_on_origin` | one of the board's reads | the board's |
| `interpret-trailers` | `session_trailer` | an act — `--session-trailer`, in the person's commit: the message's trailers | the person's |
| `log` | `acted_on` | one of the board's reads | the board's |
| `log` | `addenda_between` | one of the board's reads | the board's |
| `log` | `answer_branch_reading` | one of the board's reads | the board's |
| `log` | `answer_cmd`, in its `check_ask` | an act — `--answer`: where the ask was answered, before it writes | the person's |
| `log` | `answerer_of` | one of the board's reads | the board's |
| `log` | `commit_list` | one of the board's reads | the board's |
| `log` | `git_ship_verdicts` | one of the board's reads | the board's |
| `log` | `guard_verdicts` | one of the board's reads | the board's |
| `log` | `guard_walk` | one of the board's reads | the board's |
| `log` | `history_has_sessions` | one of the board's reads | the board's |
| `log` | `last_worked_on` | one of the board's reads | the board's |
| `log` | `line_author` | one of the board's reads | the board's |
| `log` | `on_their_way` | one of the board's reads | the board's |
| `log` | `owner_signature_problems` | one of the board's reads | the board's |
| `log` | `queue_actions` and its `read` | one of the board's reads | the board's |
| `log` | `read_changes` and its `brought` | one of the board's reads | the board's |
| `log` | `read_history` | one of the board's reads | the board's |
| `log` | `recover_from_log` | one of the board's reads | the board's |
| `log` | `repos_naming` | one of the board's reads | the board's |
| `log` | `result_facts` | one of the board's reads | the board's |
| `log` | `session_log` | one of the board's reads | the board's |
| `log` | `signed_line` | one of the board's reads | the board's |
| `log` | `stray_below` | one of the board's reads | the board's |
| `log` | `trailers_of` | one of the board's reads | the board's |
| `log` | `unmerged_advice` | an act — an act's refusal of a branch not merged | the person's |
| `log` | `unverified` | one of the board's reads | the board's |
| `log` | `verdict_reports` | one of the board's reads | the board's |
| `log` | `verified_as` | one of the board's reads | the board's |
| `log` | `verified_owner` | one of the board's reads | the board's |
| `ls-files` | `board_after_act` | an act — an act's rebuild of the board: whether git tracks the board | the person's |
| `ls-files` | `path_mode` | one of the board's reads | the board's |
| `ls-files` | `staged_files` | one of the board's reads | the board's |
| `ls-files` | `tracked_board_rels` | one of the board's reads | the board's |
| `ls-files` | `tree_changes` | one of the board's reads — it compares the working tree (`compared`) | the board's, every configured filter driver emptied |
| `ls-files` | `tree_paths` | one of the board's reads | the board's |
| `ls-remote` | `origin_default` | not reached — no run of the tool calls it; `default_trunk` reads the trunk from the clone's cached refs | the person's |
| `ls-remote` | `pushed_branches` | an act — the queue's contact with origin, asking its branches | the person's |
| `ls-tree` | `judge_commits` | one of the board's reads | the board's |
| `ls-tree` | `path_mode` | one of the board's reads | the board's |
| `ls-tree` | `shipped_moves` | one of the board's reads | the board's |
| `ls-tree` | `specs_unread` | one of the board's reads | the board's |
| `ls-tree` | `tree_paths` | one of the board's reads | the board's |
| `merge-base` | `done_cmd` | an act — `--done`: where the act is, before it writes | the person's |
| `merge-base` | `owner_change` | an act — `--answer`, `--done`, `--due`, `--revoke`: its branch, its commit and its push, and its own reads before it writes | the person's |
| `merge-base` | `owner_signature_problems` | one of the board's reads | the board's |
| `merge-base` | `pushed_branches` | one of the board's reads | the board's |
| `merge-base` | `queue_actions` | one of the board's reads | the board's |
| `merge-base` | `revoke_cmd` | an act — `--revoke`: where the answer is, before it writes | the person's |
| `merge-tree` | `queue_actions`, in its `conflicts` | one of the board's reads — the digests' conflict preview; it runs only where the merge drivers the configuration names are read as none and the filter drivers are read too, and, where a filter driver is configured, only where `merge.renormalize` reads false, with no `-X renormalize` and each filter driver emptied; the lists and `merge.renormalize` are read again after it, and an unread or changed one makes the preview not read. Its limit: a driver configured, or `merge.renormalize` turned on, between the first reads and the `merge-tree` takes effect in it, and the reads after it name the preview as not read without keeping a program from starting | the board's |
| `patch-id` | `queue_actions`, in its `read` | one of the board's reads | the board's |
| `push` | `owner_change` and its `record_refusal` | an act — `--answer`, `--done`, `--due`, `--revoke`: its branch, its commit and its push, and its own reads before it writes | the person's |
| `remote` | `forge_prs` | one of the board's reads | the board's |
| `restore` | `owner_change`, in its `record_refusal`, `undo` | an act — `--answer`, `--done`, `--due`, `--revoke`: its branch, its commit and its push, and its own reads before it writes | the person's |
| `rev-list` | `git_ship_verdicts` | one of the board's reads | the board's |
| `rev-list` | `queue_actions`, in its `read` | one of the board's reads | the board's |
| `rev-list` | `read_changes` | one of the board's reads | the board's |
| `rev-parse` | `archive_source` | an act — `--vendor`: whether the source is an unpacked release | the person's |
| `rev-parse` | `default_trunk` | one of the board's reads — the cached `origin/main`, and `origin/master` beside it for `--check` and the default run | the board's |
| `rev-parse` | `dirty_refusal` | an act — an act's refusal of a working tree that is not clean | the person's |
| `rev-parse` | `done_cmd` | an act — `--done`: where the act is, before it writes | the person's |
| `rev-parse` | `git_dirs` | one of the board's reads | the board's |
| `rev-parse` | `guard_walk` | one of the board's reads | the board's |
| `rev-parse` | `head_commit` | one of the board's reads | the board's |
| `rev-parse` | `install_copy` | an act — `--install-hook`: the hooks' copy and where it came from | the person's |
| `rev-parse` | `install_hook` | an act — `--install-hook` | the person's |
| `rev-parse` | `merge_heads` | one of the board's reads | the board's |
| `rev-parse` | `owner_change` and its `record_refusal`, `undo` | an act — `--answer`, `--done`, `--due`, `--revoke`: its branch, its commit and its push, and its own reads before it writes | the person's |
| `rev-parse` | `owners_at` | one of the board's reads | the board's |
| `rev-parse` | `pending_judgement` | one of the board's reads | the board's |
| `rev-parse` | `queue_actions` | one of the board's reads | the board's |
| `rev-parse` | `resolve_commits` | one of the board's reads | the board's |
| `rev-parse` | `revoke_cmd` | an act — `--revoke`: where the answer is, before it writes | the person's |
| `rev-parse` | `session_trailer` | an act — `--session-trailer`, in the person's commit: the message's trailers | the person's |
| `rev-parse` | `ship_records` | one of the board's reads | the board's |
| `rev-parse` | `source_provenance` | an act — `--vendor`: the tool's own source, its commit, its tag and whether it is clean | the person's |
| `rev-parse` | `standup_where` | one of the board's reads | the board's |
| `rev-parse` | `stray_below` | one of the board's reads | the board's |
| `rev-parse` | `tip_variants` | one of the board's reads | the board's |
| `rev-parse` | `triage_pending` | one of the board's reads | the board's |
| `rev-parse` | `triage_views` | one of the board's reads | the board's |
| `rev-parse` | `trunk_ref` | one of the board's reads | the board's |
| `rev-parse` | `unmerged_advice` | an act — an act's refusal of a branch not merged | the person's |
| `rev-parse` | `whoami` | one of the board's reads | the board's |
| `rev-parse` | `worktree_git_dirs` | one of the board's reads | the board's |
| `show` | `last_worked_on` | one of the board's reads | the board's |
| `show` | `refusal_record` | one of the board's reads | the board's |
| `status` | `changed_paths` | an act — an act's own read before it writes: whether the working tree is clean (`git status`) | the person's |
| `status` | `source_provenance` | an act — `--vendor`: the tool's own source, its commit, its tag and whether it is clean | the person's |
| `switch` | `owner_change` and its `undo` | an act — `--answer`, `--done`, `--due`, `--revoke`: its branch, its commit and its push, and its own reads before it writes | the person's |
| `symbolic-ref` | `default_trunk` | one of the board's reads | the board's |
| `tag` | `source_provenance` | an act — `--vendor`: the tool's own source, its commit, its tag and whether it is clean | the person's |
| `var` | `owner_change` | an act — `--answer`, `--done`, `--due`, `--revoke`: its branch, its commit and its push, and its own reads before it writes | the person's |
| `var` | `pending_author` | one of the board's reads | the board's |
| `version` | `git_version` | one of the board's reads | the board's |
| `worktree` | `worktree_git_dirs` | one of the board's reads | the board's |
| `worktree` | `worktree_tops` | one of the board's reads | the board's |
| `rev-parse` | the three hooks `--install-hook` writes: `--show-toplevel` and `--git-common-dir` | an act — the person's own commit's: its hook finds the copy | the person's |
| `diff` | the pre-commit hook: `--cached --name-only` | an act — the person's own commit's: whether its hook runs the copy's write | the person's |
| `add` | the pre-commit hook: `--pathspec-from-file=-` | an act — the person's own commit's: it stages what the copy's write printed | the person's |

## Why

The board's fixed settings promise that no read of the board's starts a program that a configuration names, other than
the SSH signature check its `%G?` asks for: the comment above `BOARD_SETTINGS` in `shoalmark.py`.

## Done when

- Every git process the tool starts is listed, and each is named as one of the board's reads or as an act.
- Each of the board's reads keeps that promise, under a class test whose fixture configures every such program and
  whose mutants each fail it.
- The Reviewer's verdict is READY, and CI is green.

## Ship log

| Date | Event |
|---|---|
| 2026-10-21 | Filed and judged In Progress, P1, by the Planner for v0.20.1, before the first build commit. |
| 2026-10-21 | Built by the Builder seat (`27f31560/builder-18`): `6327661` — every git the tool starts is one of the board's reads, under the board's settings in every run but an act's, or an act, under the person's; each read that compares the working tree runs with every configured filter driver emptied, and what rests on it is right or not read; the class test `test_board_settings.py` and its fifteen mutants. `fc4433d` — the list of every git process the tool starts. The review comes next. |
| 2026-10-21 | The one full run at `72d28ae`, by the Builder seat (`27f31560/builder-18`): 2205 ok and 5 FAIL, its browser checks skipped. The five, in `test_vcs_shared_callers.py`, were fixed at `96188eb` and pass in their blocks. `96188eb`'s message gives 2160 for that run's other checks, where the count is 2205. The review comes next. |
| 2026-10-21 | Fix round 1 built by the Builder seat (`27f31560/builder-18`): `9a10ebf` — the class test runs a byte-identical clean control and kills each mutant by its designated row; `c17a7cf` — the digests' conflict preview is one of the board's reads, reported as not read where a configured merge driver could change the merge; `4581b20` — `--check` and the plain run read the trunk from the clone's cached refs and ask origin nothing, the queue's `fetch` and `ls-remote` still contacting origin under the person's own settings; `7eb55fa` — the comparison controls and the tracker say only what holds now. The review comes next. |
| 2026-10-21 | Fix round 1 forward: the queue's merged-and-closed read (`forge_closed`, `--queue`'s) is started with `nested_git_env()`, and the FM-044 launch allowlist matches its start. |
| 2026-10-21 | Fix round 1 forward: each mutant's designated text names exactly one row of the class test, qualified by its fixture, and a mutant is killed only when that one row is green in the clean control and red under it. |
| 2026-10-21 | Fix 1c: the queue's open-pull-request read (`forge_prs`'s `gh pr list`) is started with `nested_git_env()`, as `forge_closed`'s is; in a digest and under `--queue`, whose reads are the board's, that carries the board's settings and git's own lazy-fetch default, while the queue's `git fetch` and `git ls-remote` run under the person's own settings. The comment above `BOARD_SETTINGS` and the list say so. |
| 2026-10-21 | Fix 1d, text only: the comments and docstrings around the trunk read say only what the head does — every reader gets `origin/HEAD`, else the cached `origin/main`, else `origin/master`, and no run asks origin. Kept and unreached: `default_trunk`'s `ask` parameter and the `ask=` its callers pass, `_ASK_ORIGIN`, `_TRUNK_UNTOLD` with its readers and the line it carries, and `origin_default` with `_ORIGIN_DEFAULT`. No code line changed. |
| 2026-10-21 | Fix round 2 built by the Builder seat (`27f31560/builder-22`): `514b736` — the digests' conflict preview reads the merge drivers and the filter drivers before and after its `merge-tree`, runs only where both lists are read as none, and is reported as not read otherwise; `4d2ff97` — where `origin/HEAD` is absent and the cached `origin/main` and `origin/master` name different commits, `--check` and the default run on a clean tree refuse in one line, and the origin-discovery block uses an origin whose default branch is `master` with the branch's tip pushed as `main`; `9e85439` — the class test holds the trunk read over a local origin, SSH and a localhost HTTP server; `1765e80` — the comments, docstrings, labels and this tracker say what holds now. The review comes next. |
| 2026-10-22 | Fix round 3 built by the Builder seat (`27f31560/builder-22`): `7f1c13e` — where `origin/HEAD` is absent and the cached `origin/main` and `origin/master` name different commits, `--check` and the default run refuse in one line whatever the working tree holds, the edited tree a row of the class test with its mutant; `c66172c` — the class test keeps its module docstring, which states the conflict preview's rule, and its comments on git alone. The review comes next. |
