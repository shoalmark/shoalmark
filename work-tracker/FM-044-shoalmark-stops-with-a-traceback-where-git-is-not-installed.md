---
id: FM-044
status: In Progress
considered: FM-003
tags: bug
next: review
triaged: 2026-10-13
rank: 3
tier: P1
hook: "A Subversion team without git could not run the reviewed copy: every command but --session-check and --queue stopped with a traceback before it wrote anything."
---

# FM-044 — shoalmark stops with a traceback where git is not installed, on Subversion too

## What is true now

**2026-10-13 — independent critical READY, COMMON SKELETON ONLY; dependent seats dispatched.**
The dedicated independent ROOT Reviewer `01a1358b` accepted exact `b72b9ae` at empty verdict `ef77527`, closing
RV-3085–RV-3088 in their second and final verification round. The same-round addendum remains RV-3088 evidence.
Independent controls reproduce the original defects and pass the corrections: 302 core checks, 52 scanner/cache/source
checks, 43 history assertions, six restricted-PATH checks, retained FM-045 and three R14 controls. Post-verdict gate passes.
Ordinary local merge `1fc12b0` integrates Owner #170 main `cab89ed` with exactly the accepted product tree; its clean gate
passes in 4.524 s and 26 history-aware ratchet controls pass in 13.778 s. The critical READY remains inside its ancestry.
A, B and C start their bounded slices from this accepted common product under the exclusive ownership below; Planner
alone integrates shared functions and suites. This dispatch does not accept the full Stage 1 chain or new consumer authority.

The scanner exempts descendants of the one digest-validated top-level boundary **by AST node identity** and includes
class scope in launch keys. All repository caches/configuration bindings clear before fallible root discovery or metadata,
configuration and policy reads; process/write enforcement remains. Source requests resolve the original path before
lexical cancellation, require actual source HERE, launch canonical HERE and permit only capture/text/UTF-8/replace and
the existing sanitized nested-Git environment. Executable, shell, input and other process/context overrides refuse before
any attempted launch. The four existing source reads and supported wrapper semantics remain usable. Source HERE cannot
substitute for consumer ROOT authority. A Git request for an SVN target still refuses in one line before launch.

The ratchet checks the unfiltered reachable graph and **every applicable child/parent multiset transition**, including
merges equal to a stale parent and records-only descendants. Checked batches reuse identical commit/tree/blob objects,
validate original object hashes and parent/tree evidence, and explicitly disable Git replacements. A graft-hidden parent,
shallow or unavailable history, failed Git/object reads, invalid revision/JSON/UTF-8 evidence, historical growth or deletion
after introduction deliberately fails the outer gate. Readable pre-introduction absence, genuine root introduction,
explicit empty lists and valid shrink/merge remain supported. The native source-history proof checked 1,621 commits and
1,486 distinct root trees in 0.333 s; that measures this checkout, not a general bound on all consumer histories.

Changed-Python compile passes, and **302 core checks pass (72.568 s)**, including all 59 new review controls. Running
those 59 controls against immutable `6d0c239` yields 17 passes and 42 failures (37.850 s), including real Git shrink,
merge-resurrection/later-shrink graphs, unavailable metadata/objects, symlink-parent escape and launch-option overrides.
FM-045 retains all 30 classified Git commands with no unread/unclassified start; its boundary/`git_out` injections refuse.
The three selected R14 signature/default-policy/signers/every-parent tests pass (163.704 s). The
[check/caller evidence](evidence/stage-1-skeleton-checks-2026-10-13.md) records exact control/hash limits. Full suites and the unchanged five-job R25 matrix remain CI work after Owner push; D4 assigns no platform
trial from this one native observation. R14 trust/signers/default-branch/every-parent rules and R26 legacy remain retained.

The original neutral refactor `4f1664d` follows the judged `170985c` parent (Owner filing #167 at `e6d1e27`); its 19 wrapper
controls also pass against that immutable parent. The separate dispatch `6f00764` selects Git/SVN once per configured
ROOT and routes administrative-path discovery through that selection. SVN metadata starts no process; missing, empty,
non-regular, symlinked or unreadable working-copy records refuse in one line with exit 4. Git own/common and linked-worktree
directories, ancestor/nested disk metadata and symlink/filesystem aliases remain excluded. Current-main #168 records at
`ab7ed3f` are already integrated by ordinary local merge `6d0c239`, retaining signed records and command-applied FM-004
judgement; no dependent product branch is integrated. The independently READY tasking records at
`6134fae65103c44482babffc2322c229f3aa76f0` are integrated by an ordinary local records merge after the corrective
product commit `049637c`. All product/control/list/ceiling blobs remain exact, signed records and command-applied
judgements remain, and INDEX is regenerated. The exclusive dependent function/test allocation and conservative guard
hold are current; the critical common prerequisite is now satisfied for their scoped implementation.

There remain **63 direct starts: 55 Git, 3 SVN and 5 non-VCS/dynamic**, declared in the unchanged
[initial ceiling](../test_vcs_launch_ceiling.json) and caller evidence. The 60 `git_out` and 9 `svn_run` domain callers
are not thereby accepted for SVN. The scanner covers Python process references in `shoalmark.py`; generated hook shell,
release scripts, fixtures and documentation tooling retain their separate controls. This static ratchet supplies no
arbitrary Python/FFI obfuscation proof. Metadata guard checks local accessibility/path confinement, not SVN database
integrity, author/history or protected-state proof. Full-tool SVN without Git remains incomplete. Shared commands, board,
rights/guard and CLI are dependent work now dispatched from the accepted common base. The committed consumer
policy anchor remains unresolved and protected acceptance must conservatively refuse in its later guard slice. Archive
source `3c18008` stays separate; its non-Git `git_dirs` integration point survives semantically, while eventual
`archive_source` must use the corrected narrow `source=True` read. Source acquisition/parsing is unchanged. The
[Builder brief](evidence/stage-1-builder-brief-2026-10-13.md), signed path and D3/D4 holds remain the acceptance sources.

**2026-10-13 — filing recovered; no stage-1 build was supplied by the recovery.** This replacement carries the filing
reviewed at `99050b9`, with RV-2735–RV-2737 corrected. The signed 12 October R23 lifts the hold for stage 1:
Subversion with no git installed, including the release archive and its pending scoped re-review. FM-023 allocates
that bounded stage and archive to v0.20.0. Plain-folder scope (D3) and where the no-git proof runs (D4) remain held
until trial findings and the 20 October review; this recovery supplies no platform trial or implementation evidence.
The records pass, Owner merge and Planner judgement preceded the stage-1 dispatch; implementation acceptance remains due.

**Recorded failure, 2026-10-08, reviewed on v0.19.1.** Where `git` is not installed, every command except
`--session-check` and `--queue`, which refuses in one line, stops with a Python traceback (`FileNotFoundError`) before
it writes anything. The review observed this in a folder with no version control and in a Subversion working copy.
Its first failing call was `git_dirs()` (`shoalmark.py:273`), reached when a command judges the tracker folder.
The filing counted direct `git` calls in 53 places and `git_out` in the rest; only `git fetch` and `git ls-remote`
catch a missing `git`. Every CI runner carries `git`, so no check ran without it. These are the filing and review's
observations, not a fresh claim about v0.19.4.

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
| 2026-10-13 17:42 CEST | **Common critical READY and dependent dispatch:** independent `ef77527` closes RV-3085–RV-3088, COMMON SKELETON ONLY. Ordinary #170 merge `1fc12b0` preserves the exact product; clean gate and all 26 ratchet controls pass. A/B/C receive exclusive bounded tasking; Planner owns serial integration. Full Stage 1, protected SVN acceptance and CI remain due. |
| 2026-10-13 | Independent records verdict ce014e4 merged in Owner PR #167 at e6d1e27; command-applied triage keeps P1 #3 build, and the seat sets In Progress before the common skeleton. Bounded Builder/dependent-seat brief recorded, with guard contract and D3/D4 holds explicit; no implementation or proof claimed. |
| 2026-10-08 | Filed, for 0.19.2. |
| 2026-10-13 | Filing recovered from `99050b9` on current main; RV-2735–RV-2737 fixed, acceptance bounded to signed R23 and FM-023, records review next. |
| 2026-10-13 | FM-044 common-layer neutral refactor: only git_out/svn_run launch mechanics moved behind vcs_process. Immutable-parent/refactor wrapper contracts and real Git/SVN positive/refusal fixtures pass; compile and test_core pass; metadata dispatch, ratchet, independent critical review and dependent migrations remain due. |
| 2026-10-13 | FM-044 bounded skeleton dispatch built after neutral refactor 4f1664d: cached ROOT selection, no-process SVN metadata, fail-closed administrative paths and constrained target/source process requests. Compile and 243 core checks pass; 63 retained direct starts and exact scanner/proof limits declared. Independent critical review next; dependent migrations, archive integration, CI and platform decisions remain due. |
| 2026-10-13 | Integrated only immutable current-main #168 records at ab7ed3f by ordinary local merge before the critical handoff, retaining the exact 6f00764 product blobs, command-applied FM-004 judgement, main's signed records and FM-044 implementation evidence; INDEX regenerated. |
| 2026-10-13 | Fixed forward round-1 RV-3085–RV-3088 after released e511d57: node-identity/class-scoped scanner, pre-fallible repository invalidation, original-path/canonical-HERE source confinement and complete checked reachable parent transitions with deliberate proof failures. Compile and 302 core checks pass; 59 targeted controls contrast 17 pass/42 fail on immutable 6d0c239 with 59 pass on the fix. Ceiling/list unchanged; critical verification remains due and dependent code held. |
| 2026-10-13 | Integrated only independently READY planning records 6134fae after corrective product 049637c by ordinary local merge. Retained all product/control/list/ceiling blobs and signed records/judgements exactly; exclusive dependent function/test ownership and current holds retained; INDEX regenerated. No dependent code or acceptance verdict supplied. |
