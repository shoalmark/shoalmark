# FM-044 dependent-seat ownership — read-only Research handoff

Prepared 2026-10-13 by `stage_and_b1_inventory`, read-only Research support. This committed research allocation supports the canonical Builder brief; it is not implementation, a review verdict or a ready line. No repository code or test was executed, no repository file was changed, no worktree was created and no forge/network operation or new review ID was used.

## Provenance and limits

- Immutable production and existing tests: `4f1664ddad8471974ecee154e9b3b293d1a60cbb`. This commit supplies the behavior-preserving process boundary; it is not the final common skeleton and this handoff does not assert its acceptance.
- Canonical brief: `170985c928e9bc628908c9023a542e907fc4cdc9:work-tracker/evidence/stage-1-builder-brief-2026-10-13.md:13–19,21–37`, also present at `4f1664d`. The brief requires independently reviewed common work before dependent branches, one production file, separate HERE/ROOT, a shrinking ratchet and retained Git authority.
- Signed scope/path: `4f1664d:work-tracker/TRIAGE.md:18–21`; R23/R26 references and accepted filing are recorded in [the guard contract](svn-guard-contract-2026-10-13.md). D3 plain-folder and D4 required proof platforms stay held. The requirement contract is `4f1664d:requirements/README.md:3–5,29–32`; test expectations come from signed scope, not the new implementation.
- **Candidate captured before its commit:** `scratch/stage-skeleton-builder/test_vcs_launch_allowlist.json`, captured SHA256 `1da7caf437e6c782d03fdb556b8986fcc81125ac0dd9cc69950501ad11600347`, has **63 entries in 60 functions**. At capture, the accompanying scanner/dispatch changes, ceiling and evidence were uncommitted. They are now committed at `6f00764` and present unchanged in `6d0c239`; independent critical round 1 is NOT READY with four findings pending correction. The capture is historical context, not a verdict or an accepted exemption.
- Immutable `4f1664d` has 65 `subprocess.run` sites: 56 literal Git, 3 literal SVN, 5 non-boundary dynamic starts and the explicit `vcs_process` start. Thus 64 starts remain outside that boundary. The candidate removes `git_dirs`' direct start, giving its declared 63-entry list. These are static source counts, not executed coverage. The appendix inventories every direct start, every `git_out`/`svn_run` caller and both boundary wrappers.
- Push URL remains `DISABLED`. A final reviewed clean branch is reported for Owner fetch/push. Critical review takes its own independent root session. No B1 website build is allocated here; its signed next-release work belongs to Claude tomorrow.

## Planner dispatch clarification — 2026-10-13

(Planner) From: 01a13517 planner (repo) · gpt-6.1-sol · xhigh

The common prerequisite is accepted at independent critical READY `ef775278ce4983787d8d17853c4f9cb8ed05ab69`,
Reviewed `b72b9ae033d09308e569c88b04f16e25d91fe97b`, by dedicated ROOT Reviewer `01a1358b`.
RV-3085–RV-3088 are CLOSED in round 2; RV-3089–3099 remain unused. Ordinary main integration
`1fc12b08399a73aa00f196e9a611aa376c408bc0` has exactly the accepted product tree, current main `cab89ed`
in ancestry, a passing clean gate and 26 passing ratchet controls. A/B/C start their bounded implementation after
this dispatch commit, using that accepted API/ceiling/list and the ownership below. No further boundary digest,
ceiling expansion or new exemption is authorized. This remains COMMON SKELETON ONLY, not full Stage 1 acceptance.

The original proposed workflow left every allowlist reduction to later integration. That would prevent a migrating Builder from passing the required unchanged core/ratchet check. The corrected delegation permits A/B/C to remove only the exact keys for starts migrated in their own owned functions, in the same commit on their isolated worktrees. C retains exclusive ownership of scanner functions; no seat expands/rekeys the list, changes the fixed ceiling/boundary digests, or removes another seat's unmigrated key. P serially merges the code and combined removals, retaining all parent reductions. Each Builder supplies removed keys and actual local checks with its handoff.

Current task estimates are A **2.25–3.75 h**, B **4.5–7 h** with an initial **60–90 minute** proof-interface/refusal deliverable, C **1.5–2.5 h**, and P **0.5–1 h** serial wiring plus the separately allocated **1–2 h** archive allowance. Including the already completed common Builder allowance, this is **10.25–16.75 Builder seat hours** before archive/integrated review. They may overlap under the function reservations; no full-stage finish today is promised. RV-3003/RV-3004: recorded privately. Original private tasking is now supplied from `7356d6e`; the missing-source stop is removed. The common critical code-start gate is satisfied; separate private implementation/verification and integrated acceptance remain due.

## Seats and exclusive ownership

| Seat | Owns | Dependencies and stop | Estimate after reviewed common base |
|---|---|---|---|
| A, Critical Builder | Shared folder/write paths; board tripwire and bounded local SVN reads; shared report metadata; init/install and generated hook/property entry points. | Uses the reviewed metadata/process API and B's attribution results; no server operation in board mode. Cannot turn missing metadata/proof into empty success. Generated Git hooks must retain trusted-copy/root semantics. | 2.25–3.75 h: first local board slice60–90 min, init/install45–75 min, dependent controls30–60 min; excludes review/waits. |
| B, Critical Builder | History, server author, existing rights and legacy meanings; Git signing/default-policy/every-parent judgement; protected guard and refusal before writes. | [Guard contract](svn-guard-contract-2026-10-13.md) governs. Missing adopted committed consumer proof permits conservative refusal. A new adoption anchor, changed rights or signature substitution needs a signed decision. | 4.5–7 h for the full bounded guard, contingent on the existing authority contract; first 60–90 min isolates the view/proof interface and missing-proof refusal. |
| C, Critical Builder | CLI capability policy and Git-only refusals; parser/help; launch scanner and shrinking allowlist; printed-command helper; README/ADOPT. RV-3003/RV-3004: recorded privately. | Main wiring belongs to P. The critical common prerequisite is satisfied for the supplied private tasking. Quoting follows the supplied shell rule after that same prerequisite. No new flags/platform claims or legacy deletions inferred from routing work. | 1.5–2.5 h for routing/scanner/docs; separately scoped private tasking is outside this allowance. |
| P, Planner integration | `configure`, `main`, `lint`; the common root/metadata/process boundary; suite wiring; canonical FM-044 record; reviewed archive/source integration. | Integrates reviewed seat patches serially. Owns shared wiring and preserves existing Git behavior. Common-boundary changes require their own concrete review scope; no Builder silently changes the frozen candidate boundary. | 0.5–1 h wiring/reconciliation; the brief's 1–2 h archive/release integration allowance remains separate. |

The function appendix assigns every existing top-level production function to exactly one seat. A/B/C assignments are ownership reservations, not a request to modify every listed helper. Other helpers remain with P and are frozen unless a concrete integration need is agreed. Two concurrent Builders never edit the same function. Function transfer, including a helper newly discovered to need adaptation, must be recorded before editing.

Module-level ownership follows those functions: P owns ROOT/backend/cache binding and source provenance wiring; A owns the board process classification and Git/TortoiseSVN generated hook templates; B owns policy/signers/guard/authority constants and retained Shipped classification; C owns parser/capability/printed-command declarations. Existing constants that need no change stay untouched. No concurrent seat edits `configure`, `main`, `lint`, the tracker or suite-global setup.

## Concrete first-build agreements — 17:42 CEST

A first builds the server-free tracked-board inventory and pure local predicate with the exact emitted argv
`svn status --verbose --no-ignore --ignore-externals --depth infinity . --xml`, validating real WC output and refusing
unavailable/malformed metadata before writes. `tracked_board_rels` retains its iterable consumer-relative path contract
and the existing `_TRACKED` cache; P owns reset/binding. A supplies `test_vcs_shared.py`; no shared suite edits.

B first retains `triage_guard() -> (refusals, report_line)` and supplies a narrow missing-proof SVN result/refusal adapter.
No adopted consumer policy baseline is established here. Candidate configuration can identify a proof obligation but
cannot prove its own authority or absence of older obligations. Ordinary unguarded/local rendering stays distinct.
Any new pure validated-policy extraction is P-owned and must be agreed before B needs it; no second grammar or global
binding of past revisions. B supplies `test_vcs_guard.py`; its first deliverable is60–90 min within4.5–7 h total.

C supplies pure `cli_operation(args)` and `cli_preflight(args, backend)`: selection follows retained main precedence;
preflight returns `(None, 0)` to continue existing proof or `(diagnostic, exit_code)` to refuse, with no discovery,
process, print or write. Selected SVN `--session-check` and `--commit-msg` get one-line exit4 Git-hook capability
refusals; internal non-Git `session_problems()` remains unchanged for normal SVN `--check`. P places preflight after
final consumer ROOT/backend/Tortoise normalization and before proof/message/tracker/deriver/write side effects.
A higher-priority selected shared/source command retains precedence over unused lower-priority flags. One printed-argument
helper follows the supplied PowerShell/other-shell rule; command prefixes remain prefixes. C supplies `test_vcs_cli.py`.
RV-3003/RV-3004: recorded privately.

Each seat refreshes the read-only first-build inventory against the actual accepted dispatch base, owns its functions
and standalone controls, removes only its own migrated exact keys in the same commit, and sends a clean exact handoff.
A/B/C do not edit P's main/configure/lint/common boundaries/tracker/suite globals. Shared edits stop for an explicit
recorded transfer or P integration; other owned work continues. Planner reviews and integrates seat patches serially,
including separately scoped critical acceptance; no branch helper pass means full Stage 1 READY. Public estimates remain
seat hours, not a promise of all work today; native/full CI and D3/D4 holds remain.

## Concrete adapter agreements — 18:08 CEST

The following messages are recorded before their serial integration. They agree implementation interfaces within the
existing signed scope; they grant no new authority, capability acceptance or ownership outside the reservations.

- B proposed: "svn_guard() -> (refusals, report_line)" with no argument, process, write, cache or adoption mechanism.
  P agrees the adapter always refuses an explicitly requested protected acceptance without adopted consumer proof,
  including the applicable signature limitation. B implements the standalone adapter and owned Git migrations.
  Its normal SVN `triage_guard` branch must not unconditionally call it: P still owns the actual protected-request
  predicate and placement before writes, preserving unguarded/scaffold/Passes/local reads. Adapter controls alone
  do not establish public-entry fail-closed acceptance. The past-policy reader remains held.
- A proposed: "svn_local_properties(rel)" through existing `svn_run('proplist', '--verbose', rel, xml=True)`.
  P agrees one confined, validated local WC target for init/install, with no URL/revision/server fallback; valid
  successful XML precedes a claim that a property is absent. Administrative/symlink paths and option/peg ambiguity
  must refuse. Add/propset results are checked. This is not admitted by the board tripwire, whose local SVN capability
  remains its exact agreed status tuple. A alone edits this adapter and its callers.
  A's actual fixture establishes that an absent property yields empty `<properties/>`; P agrees the refinement:
  local `svn info ./REL@ --xml` first validates a directory entry and consumer WC root, then proplist may return
  that empty shape or one matching target with unique property names. Both reads preserve confinement, require
  no operative revision/URL/server fallback, and preserve raw property text and the existing three-line hook format.
- C proposed: "on SVN return the empty presentation placeholder without starting Git" from `git_user`.
  P agrees empty presentation text supplies no WC/process/server author or authority; B retains actual attribution
  and missing-proof refusal. Git retains cached `user.name` through the existing boundary and configure invalidation.
  C controls extract's blank/placeholder presentation and unchanged real Git identity; selected Git-only answer/done
  entries still refuse before their authority handlers. P alone integrates the ordered `cli_preflight` in main.

Implementation, actual public-entry controls and independent critical acceptance remain due. A, B and C continue
other owned work while a dependent interface or review waits. RV-3003/RV-3004: recorded privately.

## Bounded API seams

| Seam | Producer / sole editor | Consumer / requirement |
|---|---|---|
| Configured consumer ROOT and chosen backend/administrative paths | P, from reviewed common skeleton. Candidate-only additions are `disk_marker`, `select_vcs`, `metadata_unreadable`, `readable_admin_dir`, `disk_admin_path`; P reserves all five if they survive review. | A/B/C query the selected backend, never rediscover from the source HERE or assume `.git` at ROOT. `configure` resets dispatch, metadata and proof caches together. |
| Explicit process invocation | P: `vcs_process`, `git_out`, `svn_run`. At `4f1664d:6309–6340,6498–6501`, executable and cwd are explicit; wrappers preserve current decoding/environment/error contracts. | Seats migrate only their owned calls. Consumer calls use ROOT; source provenance calls use HERE explicitly. Do not select all launches from the consumer backend: a tagged Git source can require Git while its target is SVN. An archive source must require no Git. |
| Local board capability | A: `read_only_git`, `split_cmdline`, `board_judge`, `board_tripwire`, `board_run` and narrowly bounded local SVN predicate if needed. | Only exact required working-copy metadata forms may be added. Reject remote flags, log/blame/cat/server reads, update/commit/propset/add, dynamic programs and network before launch. Preserve tracked-view exclusions and symlink/admin protections. A report that needs server history is omitted or expressly unavailable in local board mode, never fabricated. |
| Committed history / attribution / guard views | B: existing SVN helpers, `line_author`, policy projections, history/guard functions and new bounded adapters. | A consumes an explicit result/refusal, not working-copy labels. C/P route ordinary gate/history runs through B; those runs may contact the server and must refuse unreadable/missing-auth attribution. No pending username or credential becomes an authenticated author. |
| Pure configuration interpretation | P owns parsing/binding extraction from `read_config`/`configure`; B owns `seats_of`, `seat_identities`, `owners_of`, existing rights and committed-policy projection. | Agree the validated pure-policy seam before B's past-revision reader. Reuse current validation, duplicate-identity checks, legacy spelling and rights semantics. Do not add a second grammar or bind a past revision into global ROOT/configuration. |
| CLI capability and dispatch | C owns `parse_args` and a small declarative capability/preflight interface; P alone edits `main`. | C supplies ordered dispatch obligations: after final ROOT binding and before proof-dependent calls, hook/derived writes or process launch. Shared init/new/index/check/board/triage route to A/B as applicable; queue/session/ratio and any remaining Git-only act receive one-line refusal before writing or starting Git. The exact final shared list follows actual accepted implementations, never empty fallback. |
| Printed command arguments | C owns one new token-to-display helper; its public contract accepts one argument and returns the shell spelling under the supplied PowerShell/other-shell rule. | Each seat migrates printed command arguments only inside its own functions; P handles its own messages. Keep actual subprocess argv untouched. A configured `CMD`/`SHOALMARK_CMD` is a command prefix, not one argv token: do not quote the complete prefix as an executable or change its interpretation. This is a proposed seam, not an implementation or claim that the original failing-command list was found. |
| Aggregate gate integration | B provides history/rights/guard problems; P alone edits `lint` and early guard placement in `main`. | SVN signatures remain unavailable; legacy signed `answerers` also requires refusal, not downgrade. Bare-account author-only behavior retains all existing `answer` rights. Git signature/default-branch/every-parent, Owner exemptions and required CI authority stay intact. |
| Install / generated entry points | A: `init`, `install_hook`, `install_hook_svn`, `svn_ignore_board`, `install_copy` and filesystem/hook helpers; A owns HOOKS/COPY_HOOKS/TSVN_HOOKS and related templates. | Git hooks still run the installed trusted copy against their consumer ROOT; commit hooks fail closed and refresh hooks retain their existing result contract. C owns Git session CLI handlers; B owns gate/commit-message authority handlers. TortoiseSVN binds its installed tool HERE to the consumer before dispatch. SVN CLI has no client hook: instructions must retain explicit pre-commit generation and post-commit checking. Do not imply a server hook was installed. |
| Archive and pins | P reserves `changes_since`, `source_provenance`, `pin_manifest`, `pin_report`, `vendor` and reviewed archive additions for serial integration. | A consumes agreed install/copy results. C owns parser/help and README/ADOPT, so P passes exact reviewed archive flags/format requirements to C before reconciliation. No Archive Builder simultaneously edits C's parser or A's install functions. |
| Launch migration / shrink | A/B/C submit the exact retained keys removed by their source patches. C owns scanner functions and checks the delegated key reductions; P combines the seats' reductions in serial integration. | A/B may remove only their own migrated keys on their isolated branches so required pre-commit core/ratchet checks can pass; they submit the exact key reduction to C/P. No unrelated list/scanner edits are delegated. Each integrated migration preserves all earlier branch removals in the same integrated tree. Candidate hash keys cannot be renamed/altered into new exemptions. Dynamic non-VCS starts remain classified; the Git/SVN boundary must not be widened to `gh`, Python, deriver or notification programs. |

`4f1664d:board_judge:542–575` currently admits only bounded read-only Git. Existing `svn_last_worked_on:4684–4700` runs server history; it must not become an allowed board start. `tracked_board_rels:370–378` currently bypasses SVN; A must establish the actual local tracked-view exclusion instead of interpreting that empty list as safe proof. B's server-backed helpers are distinct from A's harmless working-copy metadata reads.

The existing TortoiseSVN branch in `4f1664d:main:9860–9867` calls `configure(HERE)` before reconstructing arguments. HERE may be the installed tool directory and must not be assumed to be the consumer project root. A supplies the concrete generated-entry consumer ROOT contract and its fixture; C owns any parser adaptation, while P alone integrates root binding in main. Test an installed tool below the consumer root as well as the direct entry point, preserving the source/consumer distinction.

## Guard contract carried forward

Use [svn-guard-contract-analysis.md](svn-guard-contract-2026-10-13.md), immutable `ab7ed3f` plus canonical `170985c`, unchanged as the contract. No extra authority is granted by this ownership map.

- Source HERE's release/configuration is unrelated to consumer ROOT's authority.
- Existing server-authenticated bare author policies can retain author-only semantics where their already established committed consumer policy is known. `signed` policies cannot pass on SVN, including the legacy answerers-only form. `owners_of` includes all configured identities with the existing `answer` right; it is not top-level-Owner-only.
- Use committed predecessor/candidate views, pending local status/schedule/copy metadata, and existing merge/copy attribution. Pending protected policy/text/deletion cannot acquire an authenticated committer before commit. Candidate configuration cannot grant itself rights, remove `signed`, move protected headings or declare a new trusted baseline.
- Current SVN helpers provide no adopted default-policy anchor. If that proof is absent, B implements explicit protected-change refusal and continues unguarded/local work. Supporting protected acceptance for a consumer lacking such an anchor stops for a signed determination of the consumer repository/path/committed revision and the existing policy establishing it. No `/trunk`, bootstrap trust, new CLI baseline setting or historical reinterpretation is invented.
- C may reduce `--ratio` routing by the separately signed optional deletion only if it yields a demonstrably smaller diff. B owns retained classification helpers and Shipped consumers; C cannot delete those with the command. This matrix does not require that optional deletion.

## Supplied C tasking and private source

The supplied shell-quoting rule remains independently available:

| Finding/source | Supplied rule | Limit |
|---|---|---|
| RV-3002, `f107a70:work-tracker/FM-023-a-plan-names-its-seats-their-estimates-and-when-the-person.md:34`; retained at `f198b58:63` | One shared printed-command quoting helper; PowerShell single quotes with embedded quote doubled; `shlex.quote` elsewhere. | Original finding body, affected command list and its exact controls were not found. C can implement the helper and migrate actual printed-command callers from this supplied shell rule. It must not invent the original finding's claimed failing commands or completion evidence; missing original failure details do not stop the quoting work. |

RV-3003/RV-3004: recorded privately. The Owner supplied original private tasking from `shoalmark-private` commit `7356d6e`, available under `inputs/private/`. Detailed findings and controls stay private; no detailed mapping is reproduced in this evidence. The missing-source stop is removed. C follows that private tasking after critical common READY and retains its exclusive ownership; broad B1 work remains with Claude tomorrow.

## Test and scanner ownership

These are proposed ownership reservations, not tests already written or run. Expectations must be independent controls derived from the signed brief and guard contract. The immutable suites largely use top-level fixture blocks, so concurrent appended edits and shared counters would conflict even with different labels.

| File / exact functions or fixtures | Sole editor | Independent obligations / merge seam |
|---|---|---|
| `test_vcs_skeleton.py`: existing `caught`, `run_boundary_controls` at `4f1664d:14,22`; candidate `refusal`, `run_dispatch_controls` | P | Preserve the exact common-boundary argv/cwd/environment/output/error controls and accepted dispatch/refusal fixtures. A/B/C import stable helpers as needed but do not rewrite these functions. Candidate local `file:// --username` fixtures are mechanics, not deployed authentication proof. |
| Same file, candidate `normalized`, `ast_hash`, `launch_sites`, `ratchet_problems`, `previous_allowlists`, `run_ratchet_controls`, and scanner declarations | C after reviewed skeleton | Own every scanner synthetic source fixture, injected literal/alias/dynamic launch, renamed caller, mutated boundary, allowlist growth/resurrection and allowed migration control. Source-inspect all process APIs, not just literal Git. Use actual current/prior committed allowlists from source HERE, never consumer ROOT. Scanner currently covers production Python `shoalmark.py`; generated hooks, release scripts, fixtures and tooling need their separate existing controls. |
| `test_vcs_launch_allowlist.json` | C owns scanner contract; A/B own only removals of their migrated keys on isolated branches; P combines serially | Each changed-code branch must pass the unchanged ratchet before commit. Remove only its owned full keys in the same change, send the exact reduction to C/P, and leave ceiling/boundary digests unchanged. P combines branch removals without resurrecting any parent's removal; unrelated keys or scanner edits remain C-only. |
| `test_vcs_launch_ceiling.json`, `LAUNCH_CEILING_SHA256`, `BOUNDARY_SHA256` | P holds accepted immutable base; C checks, never expands | Candidate declarations are unreviewed. Once accepted, no shrink integration rewrites ceiling or boundary digest to admit new starts. A necessary boundary change stops for separately scoped review. |
| New bounded standalone `test_vcs_shared.py` with proposed `run_shared_controls` and its own fixtures | A | SVN root/subdirectory/reconfigure with Git absent; no-Git init/new/index/reports/install; Git linked/admin/symlink refusal controls; local board denies server/mutator/network while retaining tracked-view/tripwire protections. No D4 platform assertion. |
| New bounded standalone `test_vcs_guard.py` with proposed `run_guard_controls` and its own fixtures | B | Retained Git positive/refusal/every-parent/default-policy/signature behavior; SVN author/rights/legacy forms, unreadable/missing-auth and pending protected refusal, copy/merge/configuration boundaries. Protected acceptance positive controls must name the established trusted fixture policy; absent production adoption proof remains a refusal, not proof of completed adoption. |
| New bounded standalone `test_vcs_cli.py` with proposed `run_cli_controls` and its own fixtures | C | Table-driven real shared/Git-only dispatch, one-line refusal before any Git/write, exact quoted argv round-trip cases from the supplied shell rule, source/consumer distinction, documentation assertions for actual supported scope. These names are proposed additions, not existing implementations. |
| `test_core.py`: `check`, `run`, module globals/import/suite calls and existing top-level fixtures | P | Wire stable standalone control entry points once; avoid every seat editing the bottom of the suite. Retain required changed-Python/core checks in each Builder's actual workflow. |
| `test_shoalmark.py`: shared acceptance helpers, suite globals and top-level blocks | P for shared integration | R12/Archive acceptance helpers retain their allocated integration ownership until reviewed branches are incorporated. RV-3003/RV-3004: recorded privately. C supplies its privately recorded expectations after critical COMMON SKELETON ONLY READY; P applies any required shared edits serially. Preserve unrelated existing suite behavior. |
| Generated hook/property fixture controls | A, in A's new module | Actual installed entry-point/root/copy behavior; B supplies authority expectations and C supplies capability expectations without editing A's fixtures. Existing immutable Git trusted-copy/security controls remain retained by P. |
| `README.md` and `ADOPT.md` | C | Match actual accepted shared commands, known proof limits, archive source/manifest/PIN format and explicit SVN CLI hook limits. P reconciles reviewed Archive changes; no B1 template or release-claims migration is built here. |

The scanner's candidate `previous_allowlists` shells out to Git at source HERE for test-history checks. That is test infrastructure, not evidence that an SVN consumer requires Git. Local no-Git controls must constrain/monitor production process starts in the consumer and state separately any fixture/setup/source operations; a mocked launch count alone does not prove a runnable no-Git consumer.

## Exact safe starting order

1. P receives the final common head, exact candidate API/allowlist/ceiling and independent critical verdict. Until that exists, only read-only planning continues. Establish that reviewed common base for A/B/C; do not branch from this inventory's provisional `4f1664d` as though accepted.
2. P confirms sole function/test ownership and the validated-policy/result/capability seams above. Lock main/configure/lint/tracker/suite wiring to P and scanner contract to C; delegate only owned-key allowlist removals to each migrating seat. No seat relies on concurrently edited common source.
3. A starts the local/shared slice; B first isolates existing history/right positive/refusal controls and conservative missing-proof guard; C starts its capability table/scanner/docs in separate owned functions/modules. These can overlap from the same reviewed base. C has the supplied private tasking; B's new-authority subset stays held. Neither permits code before common READY or blocks another scoped slice thereafter.
4. P integrates A first, preserving A's exact corresponding allowlist reduction and all prior reductions in the same tree. Review/test actual local board/write/install behavior before reporting the shared functions covered. Publish the integration head internally so downstream patches use actual A results.
5. P integrates B's bounded completed portion next. Place guard/proof refusal before dependent writes in main/lint; do not claim full protected SVN acceptance if established consumer baseline/proof remains absent. Apply C's B-key reductions without restoring A's removals. Retain every Git authority control.
6. P integrates C's final preflight/dispatch/help/documentation and scanner changes against the A/B integration, plus quoting from the supplied shell rule. RV-3003/RV-3004: recorded privately. Apply only the supplied private tasking and keep its detailed record private. Reconcile shared parser changes with reviewed Archive requirements; never hand-reset the allowlist to one branch's earlier copy.
7. P serially integrates the separately reviewed Archive source/pin changes and A/C-owned entry/help adaptations; perform the final required dry run/actual focused checks through the responsible Builder seats. Independent critical Reviewer judges the exact integrated base/head with its actual controls and explicit missing proof/platform limits. Required CI qualification follows Owner fetch/push. No readiness or end-of-day completion is inferred from this plan.

Stops that can block final FM-044 completion are the reviewed common base, unresolved authority needed for the exact promised protected behavior, private C implementation/verification, archive final-tree integration and required independent review/CI. None authorizes new rights/platforms or prevents another ranked bounded item moving.

## Function and launch appendix

The following tables are generated by parsing immutable source as text, without importing or executing it. References `function@line` point to `4f1664d:shoalmark.py`; call-site lines are also immutable. Candidate operation/digest fragments identify the allowlist rows captured before their commit. A function has one owner even when its caller belongs to another seat. The reservation covers the existing function as a whole; new adapters stay with the producer named above.

### Exclusive production function reservations

Every immutable top-level function is listed once below. P's otherwise unallocated helpers are retained unchanged; the reservation does not expand the task.

| Owner | Exact functions at immutable source line |
|---|---|
| A | `tree_write@185`, `write_rule@192`, `refuse_tree_write@203`, `guard_write@212`, `put@219`, `_norm@251`, `in_tree@255`, `real_inside@261`, `write_problem@293` |
| A | `left_alone@307`, `board_isfile@317`, `board_text@334`, `refuse_tree_file@342`, `tracker_folder_problem@351`, `tracked_board_rels@370`, `tracked_board_files@381`, `tracked_board_line@389`, `tracked_board_page@398` |
| A | `unwritable@405`, `board_write@416`, `read_only_git@464`, `split_cmdline@494`, `board_tripwire@529`, `board_judge@542`, `board_target@578`, `arm_tripwire@587`, `digest@598` |
| A | `tracker_folder@623`, `lazy_fetch_off@1089`, `lazy_fetch_back@1097`, `promisor_remotes@1103`, `git_version@1127`, `lazy_fetch_problem@1134`, `specs_unread@1170`, `recover_from_log@1686`, `answer_refs@1775` |
| A | `on_their_way@1787`, `board_after_act@3035`, `triage_home@4245`, `owners_intent@4259`, `view_dir_refused@4275`, `write_views@4283`, `latest_verdicts@4316`, `built_on@4330`, `head_commit@4347` |
| A | `board_basis@4357`, `write_built@4387`, `board_basis_line@4396`, `say_board_basis@4419`, `board_blob@4431`, `html_escape@4440`, `script_json@4444`, `render_html@4451`, `identity_problems@4506` |
| A | `related_trackers@4554`, `last_worked_on@4662`, `svn_last_worked_on@4684`, `repos_naming@4703`, `triage_worksheet@4722`, `verdict_reports@7952`, `result_facts@8203`, `deriver_env@8726`, `no_derived@8743` |
| A | `run_deriver@8751`, `svn_ignore_board@9153`, `install_hook_svn@9175`, `copy_files@9205`, `default_branch@9210`, `install_copy@9218`, `copy_record@9275`, `tree_tool_dir@9289`, `tool_here@9298` |
| A | `tree_bytes@9303`, `hooks_copy_drift@9314`, `worktree_tops@9336`, `worktree_git_dirs@9347`, `config_file_unreadable@9372`, `hooks_folder_problem@9387`, `tree_holding@9405`, `git_dir_holding@9423`, `fs_identity@9441` |
| A | `fs_chain@9450`, `fs_fold@9465`, `config_file_problem@9471`, `include_targets@9513`, `install_hook@9540`, `init@9574`, `slug_of@9637`, `next_up@9643`, `filing_freeze@9681` |
| A | `freeze_unpassable@9689`, `new_tracker@9697`, `board_run@9749`, `board_watchdog@9825` |
| B | `default_trunk@3071`, `origin_default@3107`, `svn_new@5156`, `svn_merged@5176`, `svn_tracker_new@5193`, `svn_blame@5201`, `blame_refusal@5254`, `line_regex@5267`, `frontmatter_keys@5283` |
| B | `guarded_key_problems@5317`, `guarded_line@5335`, `exact_line_regex@5340`, `line_author@5346`, `unattributed@5431`, `pending_author@5448`, `owner_policy@5459`, `owner_author@5470`, `pending_owner@5475` |
| B | `verified_owner@5480`, `owner_signature_problems@5490`, `signature_kind@5533`, `verified_as@5545`, `trusted_signers@5560`, `symlink_in_checkout@5619`, `signers_home@5642`, `signers_rel@5658`, `signers_args@5670` |
| B | `signers_gap@5676`, `signature_gap@5683`, `unverified@5691`, `pending_finding@5725`, `checkout_finding@5731`, `checkout_lines@5735`, `index_env@5750`, `staged_now@5756`, `in_this_commit@5766` |
| B | `refuse_signed_name@5777`, `seat_identities@5785`, `seats_of@5796`, `seat_of@5827`, `seat_mode@5832`, `signed_identity@5839`, `answerer_identity@5848`, `at_top@5858`, `holds@5864` |
| B | `may_answer@5869`, `answerers_problems@5881`, `no_seat@5911`, `seat_problems@5926`, `asks_records@5964`, `cleared@5975`, `transitions@5988`, `merge_heads@6006`, `changes_under_review@6017` |
| B | `read_changes@6027`, `staged_absent@6100`, `worktree_edited@6112`, `walk_problems@6119`, `line_break_problems@6130`, `rights_problems@6142`, `is_shipped@6239`, `ship_log_rows@6245`, `commits_named@6252` |
| B | `ship_records@6257`, `git_ship_verdicts@6267`, `svn_entry@6343`, `svn_shipped_moves@6349`, `svn_ship_verdicts@6385`, `shipped_moves@6399`, `ship_problems@6433`, `ratio_paths@6580`, `ratio_class@6592` |
| B | `ratio_merge@6598`, `ratio_zone@6618`, `ratio_line@6627`, `trailers_of@6881`, `history_has_sessions@6886`, `session_names@6896`, `session_problems@6911`, `sessions_before@6942`, `outside_sessions@6964` |
| B | `session_check@6972`, `branch_tracker@6988`, `named_trackers@6995`, `commit_list@7004`, `cat_blobs@7015`, `judge_commits@7056`, `build_judgement@7115`, `build_problems@7152`, `pending_judgement@7156` |
| B | `message_subject@7171`, `literal_subject@7181`, `commit_msg_check@7187`, `guarded_sections@7263`, `tree_paths@7279`, `path_mode@7290`, `config_not_file@7304`, `guard_config@7310`, `view_label@7325` |
| B | `triage_views@7330`, `section_changes@7374`, `unwritten@7410`, `kept_changes@7422`, `signers_paths@7435`, `did_words@7448`, `guard_touched@7457`, `variant_changes@7469`, `tree_variants@7482` |
| B | `guard_changes@7493`, `guard_walk@7513`, `owners_of@7537`, `owners_at@7557`, `guard_verdicts@7587`, `guard_proof@7622`, `guard_why@7628`, `unread_why@7634`, `unread_lines@7640` |
| B | `unread_refusal@7646`, `guard_lines@7652`, `triage_pending@7666`, `staged_files@7712`, `commit_msg_hook@7725`, `guard_footer@7743`, `tip_variants@7749`, `triage_guard@7770`, `resolve_commits@7915` |
| B | `read_history@7937`, `trunk_ref@7944`, `record_problems@8089`, `signed_line@8154` |
| C | `forge_prs@2022`, `pushed_branches@2054`, `have_not@2091`, `answerer_of@2100`, `answers_as_him@2107`, `review_addendum@2114`, `addenda_between@2126`, `refusal_record@2147`, `refusal_record_in_place@2198` |
| C | `stray_below@2247`, `answer_branch_reading@2279`, `answer_reading@2307`, `triage_reading@2326`, `queue_actions@2357`, `queue_lines@2477`, `forge_closed@2490`, `queue_cmd@2508`, `queue_section@2521` |
| C | `answer_step@2529`, `answer_cmd@2537`, `seed_said@2630`, `unmerged_advice@2644`, `ics_text@2676`, `ics_fold@2681`, `invite_cmd@2696`, `state_dir@2738`, `notice_text@2752` |
| C | `notify_env@2757`, `notify_argv@2763`, `post_notice@2778`, `notify_cmd@2791`, `owner_change@2849`, `board_stamp@3026`, `refusal_reason@3061`, `git_user@5142`, `sessions_file@6504` |
| C | `session_log@6508`, `session_rows@6521`, `sessions_cmd@6545`, `ratio_defaults@6573`, `ratio_cmd@6635`, `session_cmd@6712`, `harness_id@6742`, `harness_logs@6748`, `log_lines_newest_first@6755` |
| C | `read_harness_log@6769`, `harness_reading@6799`, `whoami@6816`, `session_trailer@6842`, `trailer_values@6871`, `sessions_report@7987`, `collapse_runs@8003`, `session_groups@8015`, `group_line@8049` |
| C | `group_counts@8054`, `board_sessions@8059`, `sessions_digest@8076`, `clear_ask@8119`, `append_record@8169`, `act_record@8182`, `done_cmd@8272`, `due_cmd@8316`, `revoke_cmd@8349` |
| C | `acted_on@8394`, `last_standup@8420`, `parse_args@8611` |
| P | `read_config@125`, `find_root@157`, `vcs@170`, `git_dirs@269`, `in_git_dir@280`, `in_git_dir_on_disk@286`, `configure@629`, `front_matter_schema@799`, `current_truth@875` |
| P | `orphan_rows@932`, `tier_match@961`, `parse_frontmatter@968`, `classify_status@983`, `nested_git_env@1010`, `board_settings@1060`, `board_diff_args@1065`, `unread_here@1151`, `note_unread@1157` |
| P | `read_out@1163`, `unread_line@1189`, `strip_md@1199`, `norm_dash@1203`, `answer_fields@1209`, `extract@1223`, `raise_lines@1355`, `is_new_filing@1380`, `owed_a_pass@1386` |
| P | `board@1394`, `blocked_now@1408`, `held_up_by@1417`, `ask_key@1427`, `stated_ask@1434`, `ask_problems@1439`, `asks_by_key@1481`, `owner_queue@1490`, `malformed_asks@1502` |
| P | `bottleneck@1514`, `sent_back@1520`, `answer_norm@1542`, `first_words@1549`, `answer_relation@1554`, `relation_text@1581`, `record_spans@1589`, `newest_record@1601`, `record_answer@1608` |
| P | `recorded_relation@1618`, `unrelated_answer@1629`, `record_key@1636`, `unrelated_records@1646`, `recover_relations@1652`, `record_relation@1724`, `answered@1734`, `acts_lines@1754`, `way_lines@1880` |
| P | `owed_now@1895`, `owner_digest@1903`, `standup@1937`, `digest_read@1982`, `github_remote@2014`, `ref_name@3127`, `ship_log_table@3136`, `ship_log_row@3153`, `superseded@3168` |
| P | `changed_paths@3179`, `dirty_refusal@3192`, `ready_needs@3225`, `kind_of@3235`, `needs_of@3241`, `intent_of@3248`, `render@3253`, `status_cell@3269`, `mark_blocked@3275` |
| P | `mark_raised@3282`, `render_triage@3305`, `_svg_number@3824`, `_svg_value@3843`, `brand_bytes@3926`, `inline_svg@3939`, `brand_places@4059`, `read_flat@4070`, `contrast@4082` |
| P | `brand@4092`, `shipped_themes@4149`, `theme_files@4156`, `brand_report@4164`, `set_front@4779`, `sheet_rows@4797`, `apply_verdict@4819`, `apply_worksheet@4860`, `schema_problems@4908` |
| P | `parse_due@4943`, `local_time@4974`, `answer_due@4980`, `promise_of@5031`, `act_of@5041`, `act_state@5061`, `act_words@5071`, `shape_words@5078`, `render_schema@5129` |
| P | `vcs_process@6309`, `svn_run@6317`, `git_out@6498`, `lint@8431`, `board_link@8600`, `drift_normalize@8605`, `load_trackers@8816`, `pin_problems@8828`, `changes_since@8857` |
| P | `source_provenance@8866`, `pin_manifest@8887`, `pin_report@8915`, `vendor@8936`, `main@9839` |

### Every retained start and wrapper caller

`start` is a raw `subprocess.run` call. `git_out` / `svn_run` / `vcs_process` name the existing wrapper called; the first positional argument is shown for those wrappers. Dynamic starts include the frozen boundary and five existing non-VCS starts; their owners retain the relevant board/CLI refusal controls. Candidate hash prefixes are for locating the full keys in the SHA256-identified candidate file, not replacement allowlist entries.

| Production function / definition line | Owner | Immutable starts and wrapper call sites | Candidate retained operation at capture : hash prefix |
|---|---|---|---|
| `git_dirs@269` | P | `start git/rev-parse@274` | Candidate migration; not accepted |
| `tracked_board_rels@370` | A | `start git/ls-files@376` | `git/ls-files : 0f3a5765b6` |
| `promisor_remotes@1103` | A | `start git/config@1109` | `git/config : 9be89450a4` |
| `git_version@1127` | A | `start git/version@1129` | `git/version : 7641bc59b7` |
| `specs_unread@1170` | A | `start git/ls-tree@1182` | `git/ls-tree : 35975d7861` |
| `recover_from_log@1686` | A | `start git/<forwarded>@1689` | `git/<forwarded> : a2ce46f2c7` |
| `answer_refs@1775` | A | `start git/<forwarded>@1779` | `git/<forwarded> : 6880e1b376` |
| `on_their_way@1787` | A | `start git/<forwarded>@1818` | `git/<forwarded> : 6880e1b376` |
| `forge_prs@2022` | C | `git_out 'remote'@2028`; `start <dynamic>@2036`; `git_out 'config'@2043`; `start git/fetch@2045` | `<dynamic> : 976adc4d44`; `git/fetch : 46f2a85a04` |
| `pushed_branches@2054` | C | `git_out 'ls-remote'@2061`; `git_out 'merge-base'@2076`; `git_out 'fetch'@2082` | No retained candidate entry (wrapper-only) |
| `have_not@2091` | C | `start git/cat-file@2095` | `git/cat-file : d46b638251` |
| `answerer_of@2100` | C | `git_out 'log'@2103` | No retained candidate entry (wrapper-only) |
| `addenda_between@2126` | C | `start git/log@2131` | `git/log : 608dec9080` |
| `refusal_record@2147` | C | `start git/show@2158`; `start git/show@2188` | `git/show : 14d39cc451`; `git/show : 5e20e6df13` |
| `stray_below@2247` | C | `git_out 'rev-parse'@2257`; `start git/log@2258`; `git_out 'rev-parse'@2260` | `git/log : 6225a79ea7` |
| `answer_branch_reading@2279` | C | `git_out 'log'@2293` | No retained candidate entry (wrapper-only) |
| `triage_reading@2326` | C | `start git/<forwarded>@2336` | `git/<forwarded> : 6880e1b376` |
| `queue_actions@2357` | C | `start git/<forwarded>@2386` | `git/<forwarded> : 60714ee7d2` |
| `forge_closed@2490` | C | `start <dynamic>@2498` | `<dynamic> : 701c1899a6` |
| `answer_cmd@2537` | C | `git_out 'log'@2594` | No retained candidate entry (wrapper-only) |
| `post_notice@2778` | C | `start <dynamic>@2785` | `<dynamic> : 3ae315fd35` |
| `owner_change@2849` | C | `start git/<forwarded>@2876` | `git/<forwarded> : 6880e1b376` |
| `board_after_act@3035` | A | `git_out 'ls-files'@3048`; `start <dynamic>@3052` | `<dynamic> : 3683c9f05d` |
| `origin_default@3107` | B | `start git/ls-remote@3114` | `git/ls-remote : dd69314126` |
| `built_on@4330` | A | `start git/branch@4336` | `git/branch : 113b4c8494` |
| `head_commit@4347` | A | `start git/rev-parse@4352` | `git/rev-parse : 2f1e90ebdf` |
| `last_worked_on@4662` | A | `start git/log@4668`; `start git/show@4674` | `git/log : 9c7b988b38`; `git/show : 00b2889504` |
| `svn_last_worked_on@4684` | A | `start svn/log@4690` | `svn/log : 33003eb6ae` |
| `repos_naming@4703` | A | `start git/<forwarded>@4715` | `git/<forwarded> : c945f88d83` |
| `git_user@5142` | C | `start git/config@5147` | `git/config : 0be762f29a` |
| `svn_new@5156` | B | `svn_run 'info'@5165` | No retained candidate entry (wrapper-only) |
| `svn_merged@5176` | B | `svn_run 'info'@5181`; `svn_run 'log'@5185` | No retained candidate entry (wrapper-only) |
| `svn_blame@5201` | B | `svn_run 'blame'@5219`; `svn_run 'log'@5233` | No retained candidate entry (wrapper-only) |
| `line_author@5346` | B | `start git/log@5414` | `git/log : 6f45505246` |
| `pending_author@5448` | B | `start git/var@5451` | `git/var : 5cc560fadc` |
| `owner_policy@5459` | B | `start git/<forwarded>@5463` | `git/<forwarded> : 6880e1b376` |
| `verified_owner@5480` | B | `git_out 'log'@5484` | No retained candidate entry (wrapper-only) |
| `owner_signature_problems@5490` | B | `start git/<forwarded>@5494` | `git/<forwarded> : 6880e1b376` |
| `signature_kind@5533` | B | `git_out 'cat-file'@5536` | No retained candidate entry (wrapper-only) |
| `verified_as@5545` | B | `start git/<forwarded>@5552` | `git/<forwarded> : 1f63236273` |
| `trusted_signers@5560` | B | `git_out 'config'@5577`; `start git/<forwarded>@5594` | `git/<forwarded> : 6880e1b376` |
| `unverified@5691` | B | `git_out *signers_args()@5704` | No retained candidate entry (wrapper-only) |
| `staged_now@5756` | B | `start git/diff@5761` | `git/diff : 032956e6d1` |
| `merge_heads@6006` | B | `start git/rev-parse@6008` | `git/rev-parse : 004036aff2` |
| `read_changes@6027` | B | `start git/<forwarded>@6050` | `git/<forwarded> : 6880e1b376` |
| `walk_problems@6119` | B | `start git/<forwarded>@6126` | `git/<forwarded> : 6880e1b376` |
| `ship_records@6257` | B | `git_out 'rev-parse'@6263` | No retained candidate entry (wrapper-only) |
| `git_ship_verdicts@6267` | B | `start git/<forwarded>@6271` | `git/<forwarded> : 87281152e0` |
| `vcs_process@6309` | P | `start <dynamic>@6314` | Frozen boundary, excluded by scanner |
| `svn_run@6317` | P | `vcs_process 'svn'@6324` | No retained candidate entry (wrapper-only) |
| `svn_entry@6343` | B | `svn_run 'log'@6345` | No retained candidate entry (wrapper-only) |
| `svn_shipped_moves@6349` | B | `svn_run *args@6358`; `svn_run 'status'@6362` | No retained candidate entry (wrapper-only) |
| `svn_ship_verdicts@6385` | B | `svn_run 'info'@6389` | No retained candidate entry (wrapper-only) |
| `shipped_moves@6399` | B | `git_out 'ls-tree'@6426` | No retained candidate entry (wrapper-only) |
| `git_out@6498` | P | `vcs_process 'git'@6500` | No retained candidate entry (wrapper-only) |
| `session_log@6508` | C | `git_out 'log'@6511` | No retained candidate entry (wrapper-only) |
| `ratio_merge@6598` | B | `git_out 'diff'@6601`; `git_out 'diff'@6603` | No retained candidate entry (wrapper-only) |
| `ratio_cmd@6635` | C | `start git/<forwarded>@6651`; `git_out 'log'@6668` | `git/<forwarded> : 6880e1b376` |
| `harness_id@6742` | C | `git_out 'config'@6745` | No retained candidate entry (wrapper-only) |
| `whoami@6816` | C | `git_out 'config'@6823`; `git_out 'config'@6827`; `git_out 'config'@6827`; `git_out 'rev-parse'@6828` | No retained candidate entry (wrapper-only) |
| `session_trailer@6842` | C | `git_out 'config'@6848`; `git_out 'rev-parse'@6851`; `start git/interpret-trailers@6858` | `git/interpret-trailers : 870fbe3a5f` |
| `trailers_of@6881` | B | `git_out 'log'@6883` | No retained candidate entry (wrapper-only) |
| `history_has_sessions@6886` | B | `git_out 'log'@6890` | No retained candidate entry (wrapper-only) |
| `session_problems@6911` | B | `git_out 'config'@6926` | No retained candidate entry (wrapper-only) |
| `commit_list@7004` | B | `git_out 'log'@7007` | No retained candidate entry (wrapper-only) |
| `cat_blobs@7015` | B | `start git/cat-file@7028` | `git/cat-file : 634bd4ceb6` |
| `judge_commits@7056` | B | `git_out 'ls-tree'@7072` | No retained candidate entry (wrapper-only) |
| `build_judgement@7115` | B | `start git/<forwarded>@7134` | `git/<forwarded> : 6880e1b376` |
| `pending_judgement@7156` | B | `start git/diff@7166` | `git/diff : fe580f2cb5` |
| `commit_msg_check@7187` | B | `start git/<forwarded>@7207`; `git_out 'config'@7211`; `git_out 'config'@7213` | `git/<forwarded> : 6880e1b376` |
| `tree_paths@7279` | B | `start git/<forwarded>@7285` | `git/<forwarded> : 29217f76ed` |
| `path_mode@7290` | B | `start git/<forwarded>@7298` | `git/<forwarded> : 29217f76ed` |
| `triage_views@7330` | B | `git_out 'rev-parse'@7345` | No retained candidate entry (wrapper-only) |
| `guard_walk@7513` | B | `git_out '-c'@7520`; `git_out 'rev-parse'@7526` | No retained candidate entry (wrapper-only) |
| `owners_at@7557` | B | `git_out 'rev-parse'@7566` | No retained candidate entry (wrapper-only) |
| `guard_verdicts@7587` | B | `git_out *signers_args()@7593` | No retained candidate entry (wrapper-only) |
| `triage_pending@7666` | B | `start git/<forwarded>@7678`; `git_out 'rev-parse'@7686` | `git/<forwarded> : 6880e1b376` |
| `staged_files@7712` | B | `start git/<forwarded>@7715` | `git/<forwarded> : a631b6fc99` |
| `tip_variants@7749` | B | `git_out 'rev-parse'@7755` | No retained candidate entry (wrapper-only) |
| `triage_guard@7770` | B | `start git/<forwarded>@7784` | `git/<forwarded> : 6880e1b376` |
| `resolve_commits@7915` | B | `start git/cat-file@7922`; `git_out 'rev-parse'@7933` | `git/cat-file : 03b2d22b68` |
| `read_history@7937` | B | `git_out 'log'@7941` | No retained candidate entry (wrapper-only) |
| `trunk_ref@7944` | B | `start git/<forwarded>@7948`; `git_out 'rev-parse'@7949` | `git/<forwarded> : 6880e1b376` |
| `verdict_reports@7952` | A | `git_out 'log'@7959` | No retained candidate entry (wrapper-only) |
| `signed_line@8154` | B | `git_out 'log'@8165` | No retained candidate entry (wrapper-only) |
| `result_facts@8203` | A | `git_out 'log'@8247` | No retained candidate entry (wrapper-only) |
| `done_cmd@8272` | C | `start git/<forwarded>@8280` | `git/<forwarded> : 6880e1b376` |
| `revoke_cmd@8349` | C | `start git/<forwarded>@8369` | `git/<forwarded> : 6880e1b376` |
| `acted_on@8394` | C | `start git/log@8410` | `git/log : 636c61e65d` |
| `run_deriver@8751` | A | `start <dynamic>@8778` | `<dynamic> : bda0932600` |
| `source_provenance@8866` | P | `git_out 'rev-parse'@8870`; `git_out 'rev-parse'@8873`; `git_out 'tag'@8874`; `git_out 'status'@8875` | No retained candidate entry (wrapper-only) |
| `svn_ignore_board@9153` | A | `start svn/<forwarded>@9157` | `svn/<forwarded> : 1d0b50665a` |
| `install_hook_svn@9175` | A | `start svn/<forwarded>@9178` | `svn/<forwarded> : 1d0b50665a` |
| `default_branch@9210` | A | `start git/<forwarded>@9213` | `git/<forwarded> : 6880e1b376` |
| `install_copy@9218` | A | `start git/rev-parse@9224`; `git_out 'rev-parse'@9246`; `git_out 'branch'@9247` | `git/rev-parse : b160a313dc` |
| `worktree_tops@9336` | A | `git_out 'worktree'@9340` | No retained candidate entry (wrapper-only) |
| `worktree_git_dirs@9347` | A | `git_out 'rev-parse'@9351`; `git_out 'worktree'@9352` | No retained candidate entry (wrapper-only) |
| `hooks_folder_problem@9387` | A | `git_out 'config'@9394` | No retained candidate entry (wrapper-only) |
| `config_file_problem@9471` | A | `start git/config@9484` | `git/config : a0958c0659` |
| `include_targets@9513` | A | `git_out '--exec-path'@9526`; `git_out 'config'@9536` | No retained candidate entry (wrapper-only) |
| `install_hook@9540` | A | `start git/rev-parse@9545` | `git/rev-parse : 2e1e0d1c0e` |
| `main@9839` | P | `start git/<forwarded>@10007` | `git/<forwarded> : 6880e1b376` |

Static allocation check: 403 existing top-level functions assigned once; 102 functions contain at least one direct start or VCS-wrapper call; all 65 immutable raw starts covered, with 64 outside the common boundary; all 63 candidate retained rows covered. This checks the allocation's completeness only, not behavior or acceptance.

## P history-control adapter agreement — 13 October 20:23 CEST

From: 01a13517 planner (repo) · gpt-6.1-sol · xhigh
To: 01a1362e builder (stage-shared-corrector) · gpt-6.1-sol · xhigh

P owns the test-only adapter for `run_review_history_controls`. Its fixed graph fixture uses the immutable
c599d5c git_version definition with one original ceiling call and the actual frozen boundary. It no longer
requires a live production VCS call to remain unconverted. Every original reachable-history, every-parent
merge, shrink, resurrection, missing-object and malformed-history obligation is retained. The production
scanner, ceiling, source tuples, boundary digests and test_core are unchanged. A may apply only P's exact
committed test fixture patch to its caller branch after receiving the pin, then run compile and unchanged core.
This is narrow permission to carry P-authored control code; it transfers no main/configure/lint/scanner ownership.
P retains the same adapter in final composition. New caller review remains separate from closed A findings.
