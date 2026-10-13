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
refuse before launch (one line, exit 4). `source=True` resolves the original cwd, requires actual HERE, launches canonical HERE
and admits only the four fixed provenance argv tuples with capture/text/UTF-8/replace and the sanitized nested-Git environment.
Executable/shell/input/other process or environment overrides refuse before any attempted start. The separately reviewed archive's future `archive_source`
rev-parse call must pass `source=True`; its parser, manifest, pins and release acquisition were not imported here.

## Round-1 correction and current proof

The independent inline NOT READY verdict `05a95eb9711a009b8290d7ff79f085e8ebc0e863` and addendum
`e511d57d45762e5972909a0dd6a88e32606b2bf0` review immutable `6d0c2399112c74d0109df72cbd1867709d909547`.
RV-3085–RV-3088 remain for independent verification. The original passing checks below did not prove same-named class
identity, all caches after refused configuration, original source-path/context confinement or every reachable historical
parent transition. Earlier assertions of those boundaries were too broad; the current controls address their reproductions.

The correction exempts only descendants of the digest-validated top-level boundary node, includes class scope in keys,
invalidates all per-repository bindings/caches before the first fallible operation, validates the original source path and
launches canonical HERE with bounded kwargs, and checks every applicable reachable child/parent list multiset transition.
History proof explicitly disables replacements, hashes checked commit/tree/blob batches, validates original commit parent/
tree headers against the full graph, distinguishes verified absent pre-introduction paths from failed reads, and rejects
unavailable/shallow/grafted/invalid evidence deliberately at the outer ratchet gate. Later shrinking and records-only
commits cannot hide an earlier growing merge transition. Git proof does not fetch missing objects.

| Fix/control | Result | Measured duration |
|---|---|---|
| Changed Python compile (`shoalmark.py`, `test_core.py`, `test_vcs_skeleton.py`) | pass | 0.303 s |
| Current test_core.py | 302 pass, including all 59 review controls | 72.568 s |
| Same 59 review controls on immutable `6d0c239` production/scanner | 17 pass / 42 fail; negative prior-state contrast | 37.850 s |
| Retained FM-045 classification plus boundary/git_out injections | same 30 commands; no unread/unclassified start; 2 injections detected | 5.841 s |
| Retained selected R14 signature/default-policy/signers/every-parent controls | 3 pass | 163.704 s |
| Checked reachable-history proof with source HEAD `e511d57` | 1,621 commits / 1,486 distinct root trees / 1 distinct list | 0.333 s |

Core ran alongside the immutable-baseline and retained focused checks; these are observed native durations. The history
reader uses one pinned graph and checked unique-object batches, rather than one process per unchanged historical path.
The working allowlist SHA-256 remains `1da7caf437e6c782d03fdb556b8986fcc81125ac0dd9cc69950501ad11600347`;
the ceiling remains `1eabbea359cde1c65db4a688c3ff609d6acda0a33e38bc0b84021f9fde9bf6a0`, byte-equal to `6d0c239`.
The necessary frozen boundary digest changes only for RV-3087 confinement from
`e2cd4c40729a6bbdc95ac0f9037600df5002b3e5fdee0e7774277d2fa57f732f` to
`86d6d728c50b5803dfd53a3f6aa2a4948e104db716d3a7684fb43598237c6602`; no injected start or new key is admitted.

The 59 controls include sync/async/nested same-name class methods; Git A to real SVN B validation/parsing/policy/marker/
root-discovery refusals with every prior-root cache seeded, plus successful reconfiguration and retained write/process
flags; four actual source reads, canonical source aliases/direct environment, lexical-HERE/actual-foreign symlink-parent
escape, unresolved paths and pre-start option/context refusals; and real Git initial introduction, 63-to-62 migration,
working resurrection, stale-parent merge/later shrink/records descendants, valid shrinking merge, actual unavailable Git/
list/tree/parent objects, invalid historical JSON/UTF-8/shape/keys, explicit empty lists, duplicate growth, list deletion,
armed command/revision faults, actual replace/graft hidden history, genuine root introduction and shallow history.
The unavailable-Git fixture also invokes the actual outer gate and requires an explicit failing history check; an incidental
exception is not its expected refusal. These controls do not accept injected launches by changing the list or ceiling.

## Original completed checks

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
An unreadable marker refuses instead of selecting an empty lane. The original control cleared dispatch/metadata only;
RV-3086 now proves all repository caches clear before refused discovery/configuration as described above.
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
boundary AST is frozen; only the validated top-level node's descendants are exempt, and class-qualified methods keep
separate keys. New names/normalized calls, additional occurrences, allowlist growth beyond the immutable SHA-256 ceiling
and growth across any applicable reachable parent transition refuse. Working resurrection also refuses relative to every
read historical list. Removing a call requires removing its allowlist entry. The synthetic migration has explicit imports
and does not whitelist injected production code. Ordinary mapping get/file open remain distinct from resolved webbrowser
process APIs. Failed required history is an explicit outer failing check, never an empty prior-list success.

This is a static process-API control, not arbitrary-Python/FFI obfuscation proof. Generated hook shell, release scripts,
fixtures and documentation tooling remain outside this scanner and retain their existing controls. The metadata layer
protects administrative paths and checks directory/file readability; it does not verify SVN database integrity, history,
server author, signatures or the committed protected-policy baseline. Source HERE cannot supply consumer authority.
Archive 3c18008's non-Git metadata integration point survives; source/archive code, final release dry run/pins and
combined integration are still separate. Independent root critical review must precede dependent branches.

## Current tasking integration

Corrective product `049637c7b94e74cb2c00e8bb2d9f0383e72f03e8` follows released addendum `e511d57`.
Only independently READY planning records `6134fae65103c44482babffc2322c229f3aa76f0` are merged locally after it.
All 118 non-work-tracker mode/blob/path entries, including production/control/list/ceiling files, remain identical to
that tested corrective product. Current signed path/Part B and command-applied judgement fields remain; only canonical
implementation truth is reconciled and INDEX regenerated. Exclusive function/test ownership is in the canonical brief
and its linked allocation. No dependent product code starts and no critical READY is inferred from the records verdict.
