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

**2026-10-13 — bounded common/A/C accepted; final caller correction and local entry composition continue.**
Current Owner main `3cac843` includes R12 READY `246ccdf`. Its CI/test/records changes are integrated on this
feature branch; the production tool, signed TRIAGE, AGENTS and configuration match cab89ed before seat merges.
RV-3040: recorded privately. Common READY `ef77527`, Reviewed `b72b9ae`, closes RV-3085–RV-3088. Dispatch
records READY `84c8a6b` remains ancestry; RV-3057 P3 was fixed forward without a re-pass. Accepted common
boundary/cache/source/history semantics, ceiling, digests and scanner remain frozen.

A1/A2 critical READY `6fe35f5`, Reviewed `a9a36d4`, closes RV-3089–RV-3091 in their final round, BOUNDED
BOARD/INIT/INSTALL ONLY. This ordinary seat merge incorporates its exact functions, shared controls and three
allowlist removals, 63 to 60; the later C composition reduces that to 45. The prior combined A merge passed compile, unchanged core 302 in 65.602 s and 152 A
controls in 42.777 s. This independent branch retains the same A product; its current-main checks are recorded
here: changed Python compiles in 0.475 s, and unchanged core passes in 46.861 s. A's separate caller verdict `26606d3`, Reviewed `43b5600`, is NOT READY: RV-3096 P2 OPEN in its first
round. Four new current-directory lookups fail before launch if that directory has been deleted. The Builder
replaces those four expressions with explicit inherited dot and adds real immutable-before/after controls.
The same independent ROOT Reviewer has one final verification left. This branch has not imported the caller
product; RV-3097 is unused and no closed A finding is reopened.

C critical READY `f59a1c1`, Reviewed `05e02ac`, closes RV-3095 in its final round, BOUNDED CLI/PRESENTATION/
DOCUMENTATION ONLY. Its actual callbacks and retained quoting checks pass. This ordinary seat merge incorporates the exact C product and controls: compile 0.251 s, unchanged
core 44.768 s, and all 16 C methods 3.162 s pass. Actual launch keys are 45, retaining both A and C reductions.
B final NOT READY `99968f2`, Reviewed `eabbeef`, leaves RV-3092–RV-3094 P2 OPEN/HELD after their
second/final rounds. Structural XML text/tails can become empty or credited blame, hide pending Shipped status,
and pass malformed logs as product proof. The full inline verdict contains actual-read evidence and exact
outstanding corrections; 232 scoped controls and 302 core passing cannot override those reproduced failures.
B's readers and twenty-three migrations are excluded from this local branch. A structural validation proposal
is complete outside production for Owner disposition: 50 proposed controls fail on exact eabbeef and all
293 pass on the candidate; a separate 538-scenario actual-read probe measures zero write opens. Its five
reader changes and pure validator preserve common/source/scanner/ceiling and all forty keys. These are
Builder development results, not another verdict, a READY line or permission to apply the held repair. No third verification or replacement finding is opened.
RV-3003/RV-3004: recorded privately.

Archive/common final NOT READY `eabee22`, Reviewed `284a4e8`, closes RV-3071 and leaves RV-3072 HELD with
its second/final round exhausted. The archive integration stays separate from local-stage acceptance; its
strict source-classification proposal is complete outside production for Owner disposition: 28/28 development
expectations pass versus 14/28 before. Its only changed function preserves the frozen source command. Unknown
and translated diagnostics refuse; native mount/layout qualification is pending. It is NOT ACCEPTED, with no third loop.
Standalone accepted archive/common antecedents remain intact. The earlier combined branch `fm/044-stage-entry-integration` retains that held ancestry. This separate
`fm/044-local-stage-current` starts at accepted A6fe35f5 and merges current main; it contains no archive_source
or archive_check production implementation. Its local-stage composition remains unreviewed.

Owner confirms no SVN consumer has adopted shoalmark. Full protected acceptance remains held for authenticating
consumer, recorded adoption and trial findings; held rulings return 20 October. Local CLI/board/init/install
continues. P must make actual entry say its signature/author verification limit once per run and claim nothing
more. Outside notice preview passes fourteen actual CLI cases. Tortoise preparation passes 58 expectations;
fourteen retain an explicitly labelled downstream history hold, and no-seam evidence names its server request.
Prepared helpers are neither production nor accepted complete entry behavior.

P owns main/configure/lint, aggregate suites, canonical records and serial composition under `1b48e22`.
Every parent allowlist reduction must survive composition. RV-3098–RV-3099 reserve P's independent critical
integration scope. Protected-request selection/past-policy proof, native/full CI and actual release remain
held or due; no policy baseline, authority substitute or changed rights is introduced. Codex covers today's
critical builds; Claude tomorrow. Push DISABLED; Owner fetches and pushes.

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
