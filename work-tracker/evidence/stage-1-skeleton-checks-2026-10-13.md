# FM-044 — common skeleton checks and caller inventory, 2026-10-13

(Builder) From: 01a13517/builder-4 builder (stage-skeleton-builder) · gpt-6.1-sol · xhigh

Canonical state/acceptance: [FM-044](../FM-044-shoalmark-stops-with-a-traceback-where-git-is-not-installed.md),
[Builder brief](stage-1-builder-brief-2026-10-13.md), requirements/README.md and retained signed R14/R23/R25/R26.
This evidence supplies no Reviewer verdict, full-tool no-Git completion or D4 platform qualification.

## Commit boundary and API

Base `170985c928e9bc628908c9023a542e907fc4cdc9` already carries today's In Progress/P1 #3 judgement.
Neutral commit `4f1664ddad8471974ecee154e9b3b293d1a60cbb` moves only `git_out`/`svn_run` launch mechanics.
The separate dispatch commit adds cached `select_vcs`/`vcs`, cache reset, fail-closed `git_dirs` metadata, admin path
exclusions and the initial launch ratchet. Production stays in the standard-library `shoalmark.py`.

`vcs_process(program, *args, cwd=None, source=False, **options)` returns the unchanged CompletedProcess.
`git_out` retains text/UTF-8/replace/nested_git_env and None on process failure. `svn_run` retains captured bytes,
accepted history error codes, SvnUnreadable, LF normalization and XML handling. Git requests for an SVN consumer
refuse before launch (one line, exit 4). Only `source=True` at exact HERE with one of the four existing source-provenance
argv tuples can request source Git independently. The separately reviewed archive's future `archive_source`
rev-parse call must pass `source=True`; its parser, manifest, pins and release acquisition were not imported here.

## Completed checks

| Tree/control | Result | Measured duration |
|---|---|---|
| Immutable base wrappers, including real Git and local SVN positive/refusal fixtures | 19 pass | not timed |
| Neutral compile of changed Python files | pass | 0.594 s |
| Neutral test_core.py | 179 pass | 15.877 s |
| Neutral FM-045 AST classification | 30 commands; no unread/unclassified starts; both deriver forms retained | 2.265 s |
| Neutral selected R14 tests: Owner signatures in ordinary history, trusted policy/signers, main/nested merges | 3 pass | 150.218 s |
| Dispatch final compile | pass | 0.617 s |
| Dispatch final test_core.py | 243 pass | 33.044 s |
| Dispatch FM-045 classification and new-boundary/git_out injection controls | pass; same 30 commands | 4.994 s |
| Dispatch selected R14 tests: same signature/default-policy/every-parent controls | 3 pass | 150.797 s |
| Dispatch pre-commit branch --check | pass (judged pending edits against HEAD) | 4.459 s |

The local environment was macOS x86_64, Python 3.14.8, Git 2.50.1 (Apple Git-155) at /usr/bin/git, and SVN 1.14.5 at /usr/local/bin/svn.
No-Git controls create a PATH holding SVN only, verify Git cannot be found, and monitor every process attempt.
They test explicit root and SVN subdirectory metadata dispatch, actual --root --schema probes, a harmless tree path,
admin tracker/write refusals, Git target refusal and arbitrary-cwd refusal. They are not the full init/new/index/check/
board/triage chain or an assigned D4 platform proof. Metadata failures include failed/empty/incomplete Git answers,
missing Git for a Git worktree, missing/unreadable SVN directory/marker, and missing/empty/non-regular/symlink/unreadable records.
An unreadable marker refuses instead of selecting an empty lane; a refused reconfiguration clears old dispatch/metadata.
The existing nested-Git environment, byte/text and error contracts run independently of the new dispatch controls.

## Remaining direct process sites

The initial ceiling enumerates every retained Python start by function, operation, API and normalized call; keys do not
use source line numbers. It covers the 5 non-VCS/dynamic sites as well, because opaque argv could start Git/SVN.
There are 55 direct Git, 3 direct SVN and 5 non-VCS/dynamic starts. The 60 git_out call sites and 9 svn_run call sites
now pass through the boundary but their domain callers are not thereby migrated or accepted for SVN.

| Function | Retained direct starts |
|---|---|
| `acted_on` | 1 |
| `addenda_between` | 1 |
| `answer_refs` | 1 |
| `board_after_act` | 1 |
| `build_judgement` | 1 |
| `built_on` | 1 |
| `cat_blobs` | 1 |
| `commit_msg_check` | 1 |
| `config_file_problem` | 1 |
| `default_branch` | 1 |
| `done_cmd` | 1 |
| `forge_closed` | 1 |
| `forge_prs` | 2 |
| `git_ship_verdicts` | 1 |
| `git_user` | 1 |
| `git_version` | 1 |
| `have_not` | 1 |
| `head_commit` | 1 |
| `install_copy` | 1 |
| `install_hook` | 1 |
| `install_hook_svn` | 1 |
| `last_worked_on` | 2 |
| `line_author` | 1 |
| `main` | 1 |
| `merge_heads` | 1 |
| `on_their_way` | 1 |
| `origin_default` | 1 |
| `owner_change` | 1 |
| `owner_policy` | 1 |
| `owner_signature_problems` | 1 |
| `path_mode` | 1 |
| `pending_author` | 1 |
| `pending_judgement` | 1 |
| `post_notice` | 1 |
| `promisor_remotes` | 1 |
| `queue_actions` | 1 |
| `ratio_cmd` | 1 |
| `read_changes` | 1 |
| `recover_from_log` | 1 |
| `refusal_record` | 2 |
| `repos_naming` | 1 |
| `resolve_commits` | 1 |
| `revoke_cmd` | 1 |
| `run_deriver` | 1 |
| `session_trailer` | 1 |
| `specs_unread` | 1 |
| `staged_files` | 1 |
| `staged_now` | 1 |
| `stray_below` | 1 |
| `svn_ignore_board` | 1 |
| `svn_last_worked_on` | 1 |
| `tracked_board_rels` | 1 |
| `tree_paths` | 1 |
| `triage_guard` | 1 |
| `triage_pending` | 1 |
| `triage_reading` | 1 |
| `trunk_ref` | 1 |
| `trusted_signers` | 1 |
| `verified_as` | 1 |
| `walk_problems` | 1 |

The three direct SVN functions still pending are svn_last_worked_on, svn_ignore_board and install_hook_svn.
Shared board/tracked views, init/install, history/rights/protected guard, CLI capability/report/session paths remain
separate dependent slices. Git authority semantics/default branch/signers/every parent, all five R25 code jobs and R26
legacy interpretation remain unchanged.

## Scanner and integration limits

The scanner covers Python process APIs/references in shoalmark.py, including common imports/assignments, module/API
aliases, dynamic argv/getattr/import/module-dictionary access, and changed or aliased boundary requests. Its whole
boundary AST is frozen; added launches inside that function cannot hide behind its name. New names/normalized calls,
additional occurrences, allowlist growth beyond the immutable SHA-256 ceiling and resurrection relative to committed
list history fail. Removing a call requires removing its allowlist entry. The synthetic migration control has explicit
imports and does not whitelist injected production code. Ordinary mapping get/file open methods are distinct from
resolved webbrowser process APIs, preventing the scanner from treating them as launches.

This is a static process-API control, not arbitrary-Python/FFI obfuscation proof. Generated hook shell, release scripts,
fixtures and documentation tooling remain outside this scanner and retain their existing controls. The metadata layer
protects administrative paths and checks directory/file readability; it does not verify SVN database integrity, history,
server author, signatures or the committed protected-policy baseline. Source HERE cannot supply consumer authority.
Archive 3c18008's non-Git metadata integration point survives; source/archive code, final release dry run/pins and
combined integration are still separate. Independent root critical review must precede dependent branches.
