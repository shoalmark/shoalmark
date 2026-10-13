(Research) Stage 1 — bounded SVN-without-git inventory and Builder handoff

Prepared 2026-10-13 by `stage_and_b1_inventory`, a read-only Research support agent. This committed research handoff supports the canonical tracker; it is not a signed decision, implementation or review verdict. Repository reads used immutable main `e7ce074ad0717f864067159365eb700b7a7a0a38` and recovered filing `6c03193`; concurrent working-tree tracker edits were not evidence for this inventory. No tests, browser runs, fetch, worktree creation, repository edits or forge/remotes mutations were performed.

## Authority and release boundary

- Read `AGENTS.md` and `requirements/README.md` before this inventory. The tracker remains canonical; a requirement changes only by the Owner's signed answer; acceptance expectations come from that text rather than the Builder's implementation. No new requirement IDs are introduced here.
- R23 authorizes stage 1 for SVN without git, including archive acquisition and its pending review. D3 plain-folder scope and D4 the required no-git proof platforms remain held. Sources: `e7ce074:work-tracker/evidence/rulings-2026-10-12.md:36,53–55,65`.
- R25 retains all five code-suite jobs/check names. R26 retains legacy spellings and historical interpretation through v0.20.0. Sources: the same file, `:38–39`; `e7ce074:.github/workflows/ci.yml:20–26,128–144`.
- FM-023 requires the current-main FM-044 filing, its records review, Owner merge and Planner judgement before stage-1 build. Skeleton precedes dependent branches; stage 1/archive belong to v0.20.0. Sources: `e7ce074:work-tracker/FM-023-a-plan-names-its-seats-their-estimates-and-when-the-person.md:33–37`; `6c03193:work-tracker/FM-044-shoalmark-stops-with-a-traceback-where-git-is-not-installed.md:14–19,41–61`.
- Codex may cover critical builds today under today's approved tasking; critical review is by another session. Push URL remains `DISABLED`; the Planner gives the Owner local ready branches to fetch and push.

## What main actually dispatches today

`find_root()` walks disk markers without a process; `vcs()` walks ROOT's ancestors on every call, checking `.git` before `.svn` (`shoalmark.py:157–178`). `configure()` establishes ROOT and resets per-repository caches (`:629–705`). There is no single retained backend object today. Nested/subdirectory working copies, a Git worktree's `.git` file and explicit `--root` must retain their existing meanings; ambiguity must not be solved by trying Git first in an SVN lane.

Static AST inventory on `e7ce074:shoalmark.py`: 57 literal `git` `subprocess.run` sites, four literal `svn` sites, 60 `git_out(...)` call sites and 66 total `subprocess.run` sites. These are syntax counts, not executions or claims that every site is reachable on SVN. The filing's 53-Git-site count is historical v0.19.1 evidence, not this current count. Dynamic argv/aliases need ratchet controls in addition to literal detection. Full site matrix follows below.

| Area | Existing paths / source evidence | Builder handoff |
|---|---|---|
| Root, metadata and folder/write guards | `git_dirs:269–277` starts Git unconditionally. `in_git_dir*`, `write_problem`, `tracker_folder_problem:280–364` depend on it. | Put backend selection and metadata-directory discovery in the skeleton. Preserve Git common-dir/worktree protection; protect SVN administrative metadata and all aliases/symlinks through the existing fail-closed rules. Missing tools or unreadable metadata must not become empty success. |
| Board and local reads | `tracked_board_rels:370–378` returns none outside Git. `read_only_git:464–491`, `board_judge:542–550` permit only Git processes. `board_run:9741–9787` arms the audit hook. `built_on/head_commit/board_basis:4330–4408` deliberately omit Git facts on SVN. | Give backend processes a narrow read-only/local capability. Board cannot contact an SVN server, start mutating SVN, run producers or bypass its tripwire. Preserve the current unsupported/freshness limits explicitly rather than invent SVN branch/commit facts. Test tracked SVN board/view files before choosing whether to leave them unwritten. |
| SVN history and rights | `svn_new:5156–5170`, `svn_blame:5201–5343`, SVN arm of `line_author:5369–5385`, `rights_problems:6152–6193`, `svn_run:6309–6332`, `svn_shipped_moves/ship_verdicts:6341–6390`. | Preserve their revision/server-author attribution, copied/merged-line treatment, new-tracker limits and refusal on unreadable history. Move process starting behind the layer; do not replace those rules with empty values. Normal gate/history runs may require the server; board runs may not. |
| Git authority and judgement | `owner_policy:5459–5467`, `owner_signature_problems:5490–5523`, `trusted_signers:5560–5616`, `read_changes:6027–6097`, `build_judgement:7107–7141`, `triage_guard:7762–7801`. | Preserve R14, exact line provenance, trusted default-branch policy, signature verification, every-parent history and pending-commit judgement in the Git adapter. Retain R26 legacy readers/configuration; routing is not authority cleanup. |
| Shared reports, acts and session commands | `main:9876–9949`; Git-only queue `forge_prs:2022–2051`; acts `answer_cmd:2570–2584`, `done/due/revoke:8264–8383`; sessions `:6490–6547,6734–6931`; `last_worked_on:4662–4700`. | Classify every CLI entry before it can call a Git path. Shared init/new/check/index/board/triage and owner/standup work in SVN. Git-only answer branches, queue, Git-trailer/session operations and ratio need capability refusals: one line, truthful reason, no Git subprocess or partial writes. Keep established SVN act/history readers. |
| SVN init/install writes | `svn_ignore_board:9145–9164`, `install_hook_svn:9167–9194`, `install_hook:9532–9563`, `init:9584–9626`. Three SVN launch paths besides `svn_run` use direct subprocesses. | Route through the layer with separate write permission; preserve svn:ignore and TortoiseSVN property behaviour and the explicit command-line-no-client-hook limitation. Do not treat property readback as proof of TortoiseSVN GUI execution. |
| Vendoring source vs target | `source_provenance:8858–8871` uses Git in HERE, not target ROOT; archive work is a separate dependency. | Keep source acquisition/provenance separate from target backend selection. An archive source must verify its SHA-256/RELEASE manifest without Git; a tagged Git source retains its checks. Never infer the source's VCS from the consumer's ROOT. Integrate the reviewed archive rather than duplicating its parser. |

## A design gap to resolve in the brief

The recovered filing requires the guard, folder judgement and write rule to fail closed, and a server-free read-only board (`6c03193:FM-044:49–51`). Current main's SVN `triage_guard()` returns no refusals and the historical warning that the Owner-section guard is outside its scope (`shoalmark.py:7250–7251,7773–7775`). Merely moving that return behind a backend does not meet the filing's guard acceptance.

The Builder/Planner brief must state which supported SVN operation can prove the guard and how an operation that cannot prove it refuses without blocking harmless reads. It must preserve existing server-author rights attribution without claiming Git-style signature verification from an SVN working copy. If resolving the gap would introduce a new authority guarantee or change a retained historical meaning, raise that exact decision to the Owner before building it. Research has not chosen such a policy or declared the implementation ready.

## Skeleton then dependent slices

All production code remains in the standard-library `shoalmark.py`. The names below are proposed interfaces, not existing APIs. Avoid moving the whole file or renaming surviving public commands.

| Order | Seat / estimate | Files and functions | Concrete acceptance / stop |
|---|---|---|---|
| 0 | Planner, 20–40 min | FM-044 brief/judgement; resolve the guard capability contract above | Filing reviewed and merged, triage judges it buildable. Stop on missing merge/judgement or an unresolved authority policy choice. |
| 1 | Critical Builder 1, 1.5–2.5 h | `shoalmark.py`: `configure`, `vcs`, `git_dirs`, `git_out`, `svn_run`; introduce one backend selection per ROOT and one process boundary with separate Git/SVN adapters. | Switching configured roots resets dispatch/caches; SVN cannot start Git; Git adapters preserve argv/env/return and failure semantics. Independently reviewed skeleton commit is the common base. |
| 2 | Critical Builder 1, 1.5–2.5 h | Shared metadata/read/write paths: folder checks, tracked board paths, `read_only_git`/`board_judge`, `board_run`, init/install, reports/last-worked-on | Folder/metadata/symlink refusals before writes; board process controls deny network and mutations. Depends on 1. |
| 3 | Critical Builder 2, 2–3.5 h | Rights/history/guard paths: SVN attribution/Shipped helpers, Git signature/default-trunk/judgement adapters, protected state and pending-commit readers | Independent fixtures prove surviving Git authority rules and SVN attribution/unreadable-history refusal. Depends on 1 and an agreed guard contract; coordinate exact shared edits with 2. |
| 4 | Critical Builder 3, 1–2 h | CLI capability table in `main`/command helpers; subprocess ratchet and printed-command quoting in `test_shoalmark.py`/`test_core.py`; README/ADOPT guidance | Git-only SVN calls refuse before process/write; ratchet fails injected literal and aliased subprocess escapes. Follow only the supplied RV dispositions below. Depends on 1; final integration follows 2–3. |
| 5 | Archive Builder, 1–2 h integration allowance | Reviewed archive vendoring/source path plus release workflow/script, final manifest/pins | Current archive review, bounded dry run and release-script change are separate prerequisites. No fake release tag or placeholder checksum. |
| 6 | Separate critical Reviewer, 1–2 h initial pass + findings | Combined exact head; relevant local controls and retained five-job CI | Review must judge the integrated head, include every authority boundary and report limits. Findings and CI can extend the estimate. Owner fetches/pushes/merges from local-ready branches. |

Planning estimate: 6–10.5 Builder hours for slices 1–4 before archive integration/review, with overlap only after the common skeleton. This static count suggests the earlier 4–8 h estimate needs re-estimation after the skeleton; it is not a promise of a same-day ready release. No build starts from this Research handoff alone.

## Contract-led controls to prepare independently

These expectations come from FM-044's recovered acceptance, FM-003's original shared-operation contract, R25/R26 and the retained guard rules. Research did not execute them and assigns no required proof platform under D4.

1. An SVN fixture with Python/SVN usable and Git genuinely absent from the tool's executable search path: init → new → index → check → board → triage. A process monitor must fail every attempted Git start, including one caught by the tool. Include explicit-root and SVN subdirectory runs. State the actual environment if run; do not call this an all-platform proof.
2. Negative controls: missing/unreadable SVN metadata, tracker directory inside administrative metadata, outside ROOT, symlink/junction aliases, protected-state changes with no proven author, unreadable blame/history and empty/unattributed history. Refuse with the existing exit contract and no partial write; dropping the guard or swallowing the error must fail a control.
3. Board control matrix for Git and SVN: no server/network, producer/import, mutating command, tracked page/view overwrite or metadata write. Preserve the interpreter-level tripwire. Independently attempt each forbidden class; the SVN board must not switch to online history because a normal gate uses it.
4. SVN revision/rights controls: genuine author versus wrong seat; copied and merged protected lines; new/unversioned tracker; Shipped backed by a product revision rather than records-only history; pending revision versus newest committed server revision. Preserve truthful offline refusal for ordinary history checks.
5. Git controls retain R14 Owner authorship exemption and signature refusal, exact-front-matter-line attribution, all merge parents, judged-before-build, protected policy/signers/sections and historical spelling interpretation. A routing patch that skips any one is rejected even if SVN passes.
6. CLI capability controls: every Git-only command in the classified table on SVN gives its one-line refusal before subprocess/write; shared owner/standup skip unavailable queue rather than failing the digest. Do not expand held plain-folder behaviour to make a test green.
7. Ratchet controls: enumerate launch sites by stable function/operation, not fragile line numbers; fail a new literal Git/SVN launch, aliased launch or expanded allowlist. The transitional allowlist may shrink only. Test fixtures and documentation build tooling are not silently treated as production backend code; the brief must declare the scanner boundary.
8. Archive acceptance: reviewed source manifest/checksum, completeness and safe extraction/vendoring; consumer works without Git; corruption, missing/extra unsafe paths and mismatched manifest fail before writes. Release dry run verifies the actual final changed tree/pins.

## Earlier RV IDs — only supplied scope

`e7ce074:FM-023:35–36` supplies exactly these dispositions: RV-3002 is one printed-command quoting helper, PowerShell single quotes with embedded quotes doubled and `shlex.quote` elsewhere; RV-3003/RV-3004 concern the release-before-tag pin check and missing-bash skip count, corrected before the v0.20.0 release commit. Their original findings/branch are not present among this clone's refs, so this handoff does not invent their line-level patches, individual ID-to-fix mapping or prior verification. Obtain their supplied finding text/current code before allocating a concrete fix. Preserve main's already landed tag-versus-head ADOPT controls (`e7ce074:test_shoalmark.py:13433–13482`) and update expectations only for the reviewed archive format.

No review-ID from RV-3040–3099 is consumed by this inventory. RV-3035–3039 remain outside the team's block.

## Static production launch/caller matrix
Every line below is from immutable `e7ce074:shoalmark.py`. The function range makes the launch site findable; it is not a stable ratchet key. `git_out` callers are listed separately from direct starts, so these columns must not be added as an execution count. Other subprocesses (forge, notifier, board child, producer) are outside this VCS-only table and remain subject to their existing safety controls.
| Function / range | literal Git start sites | literal SVN start sites | git_out caller sites |
|---|---|---|---|
| `git_dirs` 269–277 | 274 | — | — |
| `tracked_board_rels` 370–378 | 376 | — | — |
| `promisor_remotes` 1103–1124 | 1109 | — | — |
| `git_version` 1127–1131 | 1129 | — | — |
| `specs_unread` 1170–1186 | 1182 | — | — |
| `recover_from_log` 1686–1721 | 1689 | — | — |
| `answer_refs` 1775–1784 | 1779 | — | — |
| `on_their_way` 1787–1872 | 1818 | — | — |
| `forge_prs` 2022–2051 | 2045 | — | 2028, 2043 |
| `pushed_branches` 2054–2088 | — | — | 2061, 2076, 2082 |
| `have_not` 2091–2097 | 2095 | — | — |
| `answerer_of` 2100–2104 | — | — | 2103 |
| `addenda_between` 2126–2140 | 2131 | — | — |
| `refusal_record` 2147–2195 | 2158, 2188 | — | — |
| `stray_below` 2247–2273 | 2258 | — | 2257, 2260 |
| `answer_branch_reading` 2279–2304 | — | — | 2293 |
| `triage_reading` 2326–2354 | 2336 | — | — |
| `queue_actions` 2357–2474 | 2386 | — | — |
| `check_ask` 2586–2596 | — | — | 2594 |
| `owner_change` 2849–3023 | 2876 | — | — |
| `board_after_act` 3035–3058 | — | — | 3048 |
| `origin_default` 3107–3121 | 3114 | — | — |
| `built_on` 4330–4337 | 4336 | — | — |
| `head_commit` 4347–4354 | 4352 | — | — |
| `last_worked_on` 4662–4678 | 4668, 4674 | — | — |
| `svn_last_worked_on` 4684–4700 | — | 4690 | — |
| `repos_naming` 4703–4719 | 4715 | — | — |
| `git_user` 5142–5149 | 5147 | — | — |
| `line_author` 5346–5428 | 5414 | — | — |
| `pending_author` 5448–5453 | 5451 | — | — |
| `owner_policy` 5459–5467 | 5463 | — | — |
| `verified_owner` 5480–5487 | — | — | 5484 |
| `owner_signature_problems` 5490–5523 | 5494 | — | — |
| `signature_kind` 5533–5542 | — | — | 5536 |
| `verified_as` 5545–5554 | 5552 | — | — |
| `trusted_signers` 5560–5616 | 5594 | — | 5577 |
| `unverified` 5691–5709 | — | — | 5704 |
| `staged_now` 5756–5763 | 5761 | — | — |
| `merge_heads` 6006–6011 | 6008 | — | — |
| `read_changes` 6027–6097 | 6050 | — | — |
| `walk_problems` 6119–6127 | 6126 | — | — |
| `ship_records` 6257–6264 | — | — | 6263 |
| `git_ship_verdicts` 6267–6296 | 6271 | — | — |
| `svn_run` 6309–6332 | — | 6316 | — |
| `shipped_moves` 6391–6422 | — | — | 6418 |
| `git_out` 6490–6493 | 6492 | — | — |
| `session_log` 6500–6510 | — | — | 6503 |
| `ratio_merge` 6590–6607 | — | — | 6593, 6595 |
| `ratio_cmd` 6627–6701 | 6643 | — | 6660 |
| `harness_id` 6734–6737 | — | — | 6737 |
| `whoami` 6808–6831 | — | — | 6815, 6819, 6819, 6820 |
| `session_trailer` 6834–6854 | 6850 | — | 6840, 6843 |
| `trailers_of` 6873–6875 | — | — | 6875 |
| `history_has_sessions` 6878–6882 | — | — | 6882 |
| `session_problems` 6903–6931 | — | — | 6918 |
| `commit_list` 6996–7004 | — | — | 6999 |
| `cat_blobs` 7007–7045 | 7020 | — | — |
| `judge_commits` 7048–7101 | — | — | 7064 |
| `build_judgement` 7107–7141 | 7126 | — | — |
| `pending_judgement` 7148–7160 | 7158 | — | — |
| `commit_msg_check` 7179–7215 | 7199 | — | 7203, 7205 |
| `tree_paths` 7271–7279 | 7277 | — | — |
| `path_mode` 7282–7293 | 7290 | — | — |
| `triage_views` 7322–7363 | — | — | 7337 |
| `guard_walk` 7505–7526 | — | — | 7512, 7518 |
| `owners_at` 7549–7576 | — | — | 7558 |
| `guard_verdicts` 7579–7611 | — | — | 7585 |
| `triage_pending` 7658–7701 | 7670 | — | 7678 |
| `staged_files` 7704–7714 | 7707 | — | — |
| `tip_variants` 7741–7759 | — | — | 7747 |
| `triage_guard` 7762–7801 | 7776 | — | — |
| `resolve_commits` 7907–7926 | 7914 | — | 7925 |
| `read_history` 7929–7933 | — | — | 7933 |
| `trunk_ref` 7936–7941 | 7940 | — | 7941 |
| `verdict_reports` 7944–7976 | — | — | 7951 |
| `signed_line` 8146–8158 | — | — | 8157 |
| `result_facts` 8195–8261 | — | — | 8239 |
| `done_cmd` 8264–8305 | 8272 | — | — |
| `revoke_cmd` 8341–8383 | 8361 | — | — |
| `acted_on` 8386–8409 | 8402 | — | — |
| `source_provenance` 8858–8871 | — | — | 8862, 8865, 8866, 8867 |
| `svn_ignore_board` 9145–9164 | — | 9149 | — |
| `install_hook_svn` 9167–9194 | — | 9170 | — |
| `default_branch` 9202–9207 | 9205 | — | — |
| `install_copy` 9210–9261 | 9216 | — | 9238, 9239 |
| `worktree_tops` 9328–9336 | — | — | 9332 |
| `worktree_git_dirs` 9339–9361 | — | — | 9343, 9344 |
| `hooks_folder_problem` 9379–9394 | — | — | 9386 |
| `config_file_problem` 9463–9499 | 9476 | — | — |
| `include_targets` 9505–9529 | — | — | 9518, 9528 |
| `install_hook` 9532–9563 | 9537 | — | — |
| `main` 9831–10105 | 9999 | — | — |
