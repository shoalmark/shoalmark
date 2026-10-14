---
id: FM-044
status: In Progress
considered: FM-003
tags: bug
next: owner
triaged: 2026-10-13
rank: 3
tier: P1
hook: "A Subversion team without git could not run the reviewed copy: every command but --session-check and --queue stopped with a traceback before it wrote anything."
ask: "Which disposition should the B readers take after RV-3092–RV-3094 exhausted their review rounds?"
ask-kind: ruling
ask-since: 2026-10-13
ask-proposal: "Keep the readers held; prepare structural XML validation for Owner disposition without a third review, while local components continue."
---

# FM-044 — shoalmark stops with a traceback where git is not installed, on Subversion too

## What is true now

**2026-10-14 — local P READY `2dbaa80`; Owner PR #173 CI stopped on two old suite fixtures; test-only correction built, independent critical review next.**
Current Owner main `80b60c8` includes R12 READY `246ccdf` and #171. This branch carries its exact
AGENTS and signed TRIAGE changes through ordinary merge `2f373a8`; it adds no Owner ruling or consumer authority.
RV-3040: recorded privately. Common READY `ef77527`, Reviewed `b72b9ae`, closes RV-3085–RV-3088;
dispatch records READY `84c8a6b` remain ancestry. RV-3057 P3 was fixed forward without a re-pass.

A1/A2 READY `6fe35f5`, Reviewed `a9a36d4`, closes RV-3089–RV-3091, BOUNDED BOARD/INIT/INSTALL ONLY.
A caller final READY `4ab9341`, Reviewed `7063dac`, closes RV-3096 P2 in its second/final round;
RV-3097 is unused. Its four inherited-dot corrections pass 119 component controls, 303 core checks and
22 independent actual-function observations. The ordinary local seat merge retains its exact fifteen
caller functions and runtime controls. C final READY `f59a1c1`, Reviewed `05e02ac`, closes RV-3095,
BOUNDED CLI/PRESENTATION/DOCUMENTATION ONLY. Closed component findings are not reopened.

P final READY `2dbaa80`, Reviewed `f3bcca0`, closes RV-3098 in its second/final round, BOUNDED LOCAL P
INTEGRATION ONLY: the installed tool validates its complete configuration chain against the affected
directory's consumer before metadata queries, PATH contents, tracker/proof reads or writes. P composes actual
main/preflight/Tortoise binding and the once-per-invocation limitation:
"Subversion: this local run cannot verify commit signatures or server-authenticated authors; protected SVN acceptance remains held."
Local board/init/install/refusals run with Git absent and the server unavailable. Ordinary legacy-history
index/check/triage controls explicitly use available file:// history; their untrusted account strings establish
no authentication or adoption. Recursive applied triage prints the limitation once. Git retains its actual
mixed-flag ordering, origin-selection probe, process options and cleaned foreign hook environment.
Production SHA-256 `344db0516be7876a796f19c40b3d4334208ae33524dee1a20b8dbdf489d9b1fe` passed compile,
unchanged core 303/303 and the stage runtime block 619/619 with zero skips; the whole `test_shoalmark.py`
had not run before CI. Component-only source assertions remain in their standalone accepted modules, and
unchanged core retains the production/every-parent history ratchet.

Owner PR #173 CI at `2dbaa80`, run 38523854934: all five suite jobs stopped with exit 4, no traceback,
right after the FM-006 tempfile check. The next block, FM-006's board run in Subversion, made a working copy
as an empty `.svn` and ran `--init` in process: accepted metadata validation refuses a `.svn` with no
`wc.db` or `entries` (exit 4), and the suite's in-process `run` captured that line, so the escaping exit
ended the suite silently. FM-045 C's Subversion case had the same fixture. Both, and FM-045's suite-end
runtime check, assumed the board's run starts no `svn`, where accepted A1 starts exactly one local
`svn status … --xml` in the working copy. FM-006's v0.19.1 `--tsvn-hook pre` check handed fake
TortoiseSVN paths, which P's accepted binding refuses before the gate.

The correction is test-only. Both fixtures are real file:// working copies, skipped by name without
svn/svnadmin (CI installs both). FM-006's check admits only that exact status in the working copy, with the
repository moved away; its stand-in opens its log before the run, as the tripwire refuses a file opened
inside the event. FM-045 C and the runtime check exclude only that argv; the `env git log` control stays.
The hook check gets a real path list, message file and working copy, as S2 does. Production, `ci.yml`,
list and ceiling are unchanged. On `2dbaa80` the two blocks exit 4 and the hook check fails; corrected,
all pass. The old tool's `svn blame` still fails FM-006's check; FM-045 C and the runtime check fail on the
status argv without their exclusion. FM-037's empty `.svn` guard block and the other old SVN blocks pass
unchanged. Independent critical review of this correction is next; native CI on the Owner's PR #173 push
is the first full-suite judgement.

Composition preserves every parent's removal: 45 and 44 keys intersect to 29, and P's one migrated main call
removes the final exact key to 28. Common boundary/cache/source/history semantics, scanner, fixed ceiling,
digests and source-command options remain frozen. No held B reader or archive-source/check implementation is
imported.
RV-3099: recorded privately
RV-3003/RV-3004: recorded privately

B final NOT READY `99968f2`, Reviewed `eabbeef`, leaves RV-3092–RV-3094 P2 HELD after exhausted final rounds.
Structural XML text/tails can corrupt blame, pending Shipped status and log proof. The outside structural
validation proposal has 293/293 development checks versus 243/293 before, plus 538 real-read scenarios with
zero write opens. Its five reader changes and pure validator preserve the frozen common contract and forty
keys. The board asks for Owner disposition; no production repair, third verification or replacement finding.

Archive/common final NOT READY `eabee22`, Reviewed `284a4e8`, closes RV-3071 and leaves RV-3072 HELD after
its final round. The outside strict-classification proposal has 28/28 development checks versus 14/28 before,
changing only archive_source with the frozen command preserved. Unknown/translated diagnostics refuse;
native layout qualification remains due. Archive activation awaits Owner disposition. The earlier combined
`fm/044-stage-entry-integration` retains held archive ancestry and is not a local ready candidate.

Owner confirms no SVN consumer adoption proof exists. Full protected acceptance waits for an authenticating
consumer, recorded adoption and trial findings; held rulings return 20 October. Local CLI/board/init/install
continues without a policy anchor, authority substitute, new rights or blanket ordinary-operation refusal.
Native/full CI, protected-request/past-policy proof and actual release remain held or due. Claude covers
today's critical builds. Push DISABLED; Owner fetches, pushes and opens/merges PRs.

## Why

FM-003's S1 claims that a Subversion working copy "with no git at all" runs `--init`, `--new`, the gate, `INDEX.md`, the
board and `--triage`. Its check builds that working copy on a machine where `git` is installed, so the claim fails
exactly where a Subversion team has no `git`.

**Historical ruling, 2026-10-08.** The Owner ruled that Subversion and a plain folder are lanes of their own, and
neither ever needs `git`. The fix is a version-control abstraction layer, not one-line refusals, designed before
anything is built, and it comes before the probe's next version. Ruling 1's 'git required on every machine' is withdrawn
everywhere. R23 and FM-023's signed release allocation now bound the build to Subversion without git and the archive;
the older plain-folder and all-five-platform proof acceptance has been superseded by the D3/D4 holds.

## Done when

- **Stage 1's layer.** The tool reaches version control through one abstraction layer in `shoalmark.py`, dispatching
  Git and Subversion once per repository. Plain-folder scope remains held under D3.
- **Subversion never starts `git`.**
  - Shared tracker operations work in a Subversion working copy with no git installed.
  - Git-only operations, including signed answer branches and the pull-request queue, refuse in one line.
  - No supported Subversion run stops with a traceback or tells a person to install `git`.
- **No backend judges less.**
  - The write rule, the guard and the judgement of the tracker folder fail closed.
  - The board starts only read-only commands and asks no server on Subversion as on Git.
- **A ratchet check** finds every `git` or `svn` process started outside the layer and fails on any not on its list.
  The list may only shrink.
- **The bounded proof:**
  - Existing Git acceptance and all five code-suite CI jobs/check names are retained under R25.
  - Subversion acceptance establishes operation without git installed; D4 still holds the choice of platforms on
    which that proof must run, so this filing claims no completed platform trial.
  - FM-045's relevant board matrix covers Git and Subversion; plain-folder coverage waits for D3.
- **Fetching without `git`:** the release archive supplies the tool and archive vendoring with its SHA-256 and RELEASE
  manifest. The pending scoped archive re-review, stage-1 integration, release-script change and dry run remain due.
- **README and ADOPT** explain the supported Git/Subversion paths and the held plain-folder scope.

## Ship log

| Date | Event |
|---|---|
| 2026-10-14 09:20 CEST | Owner PR #173 CI at `2dbaa80` stopped with exit 4 on old suite fixtures: an empty `.svn`, a board run assumed to start no `svn`, fake Tortoise paths. Four checks are corrected, test-only: their focused blocks fail on `2dbaa80` and pass corrected; unchanged core 303/303 passes. Independent critical review and native CI on the Owner's push remain due; earlier verdicts and holds stand. |
| 2026-10-13 22:21 CEST | P first critical NOT READY `62ecf9c`, Reviewed `de17860`; RV-3098 source-binding correction and real controls are built. Current runtime 619/619 and unchanged core 303/303 pass. Sole final verification remains; component verdicts and exhausted B/archive/protected holds stand. |
| 2026-10-13 21:30 CEST | A caller final READY `4ab9341` closes RV-3096; ordinary local composition retains its exact functions and all parent reductions, leaving 28 keys. Actual local runtime 527/527 and unchanged core 303/303 pass. P critical review remains next; exhausted B/archive and protected-consumer holds remain. |
| 2026-10-13 20:36 CEST | B final NOT READY `99968f2` leaves RV-3092–RV-3094 HELD with final rounds exhausted; disposition ask proposes holding the readers and preparing structural validation outside. A caller `43b5600` is in its separate critical review; C is locally composed. Archive final hold remains separate; local entry/notice work continues. |
| 2026-10-13 20:08 CEST | Archive final NOT READY `eabee22`: RV-3071 CLOSED, RV-3072 HELD after the final round; strict-classification disposition proposed on the board. A1/A2 accepted component merged locally; C bounded READY `f59a1c1`; B final review and A caller migration continue. Local stage work proceeds separately; protected acceptance remains held. |
| 2026-10-13 19:48 CEST | R12 merged on current main `3cac843`; local entry branch incorporates it with generated INDEX, compile/core and affected R14 gate passing. A1/A2 critical READY closes RV-3089–RV-3091; B and C corrections/final reviews and archive final review continue. P prepares actual preflight/once limitation/Tortoise entries; protected acceptance stays held under Owner clarification. |
| 2026-10-13 18:48 CEST | RV-3003/RV-3004: recorded privately |
| 2026-10-13 18:18 CEST | Accepted common dispatch records READY `84c8a6b` retained; RV-3057 P3 corrected forward. A/B/C first bounded commits are moving in exclusive branches; P archive integration retains common guards and source confinement, with compile/302 core/55 archive controls passing. Separate affected integration review and full Stage 1 remain due. |
| 2026-10-13 17:42 CEST | **Common critical READY and dependent dispatch:** independent `ef77527` closes RV-3085–RV-3088, COMMON SKELETON ONLY. Ordinary #170 merge `1fc12b0` preserves the exact product; clean gate and all 26 ratchet controls pass. A/B/C receive exclusive bounded tasking; Planner owns serial integration. Full Stage 1, protected SVN acceptance and CI remain due. |
| 2026-10-13 | Independent records verdict ce014e4 merged in Owner PR #167 at e6d1e27; command-applied triage keeps P1 #3 build, and the seat sets In Progress before the common skeleton. Bounded Builder/dependent-seat brief recorded, with guard contract and D3/D4 holds explicit; no implementation or proof claimed. |
| 2026-10-08 | Filed, for 0.19.2. |
| 2026-10-13 | Filing recovered from `99050b9` on current main; RV-2735–RV-2737 fixed, acceptance bounded to signed R23 and FM-023, records review next. |
| 2026-10-13 | FM-044 common-layer neutral refactor: only git_out/svn_run launch mechanics moved behind vcs_process. Immutable-parent/refactor wrapper contracts and real Git/SVN positive/refusal fixtures pass; compile and test_core pass; metadata dispatch, ratchet, independent critical review and dependent migrations remain due. |
| 2026-10-13 | FM-044 bounded skeleton dispatch built after neutral refactor 4f1664d: cached ROOT selection, no-process SVN metadata, fail-closed administrative paths and constrained target/source process requests. Compile and 243 core checks pass; 63 retained direct starts and exact scanner/proof limits declared. Independent critical review next; dependent migrations, archive integration, CI and platform decisions remain due. |
| 2026-10-13 | Integrated only immutable current-main #168 records at ab7ed3f by ordinary local merge before the critical handoff, retaining the exact 6f00764 product blobs, command-applied FM-004 judgement, main's signed records and FM-044 implementation evidence; INDEX regenerated. |
| 2026-10-13 | Fixed forward round-1 RV-3085–RV-3088 after released e511d57: node-identity/class-scoped scanner, pre-fallible repository invalidation, original-path/canonical-HERE source confinement and complete checked reachable parent transitions with deliberate proof failures. Compile and 302 core checks pass; 59 targeted controls contrast 17 pass/42 fail on immutable 6d0c239 with 59 pass on the fix. Ceiling/list unchanged; critical verification remains due and dependent code held. |
| 2026-10-13 | Integrated only independently READY planning records 6134fae after corrective product 049637c by ordinary local merge. Retained all product/control/list/ceiling blobs and signed records/judgements exactly; exclusive dependent function/test ownership and current holds retained; INDEX regenerated. No dependent code or acceptance verdict supplied. |
