# FM-044 — bounded stage-1 skeleton and dependent seats

(Planner) From: 01a13517 planner (repo) · gpt-6.1-sol · xhigh

The Owner merged the independently reviewed filing in #167 at `e6d1e27`. The Planner judges FM-044 through today's triage worksheet before any stage-1 build commit. Signed R23 authorizes SVN without Git, including archive acquisition; D3 plain-folder scope and D4 required proof platforms remain held. Read FM-044, current Owner path, R23/R25/R26 and requirements/README.md. The current-main [inventory](stage-1-inventory-2026-10-13.md) is supporting evidence, not a new authority rule. All production stays in standard-library `shoalmark.py`.

Codex builds critical work today; Claude takes over tomorrow. Push remains `DISABLED`; the Owner fetches this clone and pushes. Builders spawn nothing and commit through installed hooks. No push, forge write, tag, amend, rebase or hook bypass. A critical Reviewer is an independent root session arranged by Planner. Stage-1 findings use RV-3085–3099; other reservations and Auditor IDs are untouched. Private material stays out of public records.

## Common skeleton — first Builder

Estimate: 1.5–2.5 Builder hours, then 30–60 minutes independent critical review. Scope is the common layer, not a claim that every shared SVN command already works without Git.

1. Inspect the actual production VCS launch sites and callers, propose the smallest boundary in this one file, and send its concrete API/caller inventory to Planner before broad migration. Choose Git/SVN once per configured ROOT; reset dispatch and repository caches on configure. Preserve ancestor marker handling, explicit root, subdirectories and linked Git worktrees. Source HERE and target ROOT are distinct; a tagged Git source may need Git even when the target is SVN, while reviewed archive acquisition must not.
2. Land a behavior-preserving refactor first: move the existing `git_out`/`svn_run` launch mechanics behind one explicit process boundary while retaining argv, cwd, nested-Git environment, error/return semantics and XML/error handling. Prove existing Git and SVN positive/refusal behavior unchanged before that commit. Do not move unrelated functions or introduce a general plugin/configuration system.
3. Add the bounded dispatch behavior in a separate commit. Route shared metadata discovery through the chosen backend so SVN does not start Git at that boundary. Retain Git own/common directory and all on-disk administrative metadata exclusions and symlink aliases. Do not return empty success when metadata cannot be read. Coordinate with the separately reviewed archive's small `git_dirs` dispatch patch; integrate its controls and preserve its acceptance rather than replacing its code wholesale.
4. Establish a production launch ratchet with a reviewed transitional allowlist of existing unmigrated starts. Keys must identify operation/function/normalized call, not source line numbers. It must detect new literal and aliased/dynamic launch escapes outside the boundary and reject an expanded allowlist; migration may only shrink it. Declare the scanner's production boundary explicitly. Do not silently exempt a renamed caller or test injected code by whitelisting it.
5. Add meaningful controls for root reconfiguration, argv/environment/error preservation, explicit-root and SVN-subdirectory dispatch with Git absent, and metadata refusal paths. State precisely which unmigrated shared commands remain; no supported full-tool no-Git completion or all-platform proof is claimed by the skeleton.

Before changed Python commits, compile the changed files and run `test_core.py`. Run relevant existing/new controls; complete suites belong to required CI after Owner push. First outside-tracker commit must have this judged In Progress tracker in its parent. Update FM-044's current state in place and append factual ship rows; no hand triage fields. Finish clean and report exact base/head/commits, actual checks/durations, remaining caller list and integration stops. Independent critical review of the common skeleton precedes dependent branches.

## Dependent seats after the reviewed skeleton

| Order | Seat and estimate | Bounded work | Stop |
|---|---|---|---|
| 2 | Critical Builder, 1.5–2.5 h | Shared folder/write/metadata and board/read paths; narrow server-free read-only SVN board capability, retain tripwire and tracked-view exclusions; init/install and shared reports. | Reviewed skeleton; any unreadable metadata/proof must refuse, board must start no server/mutator. |
| 3 | Critical Builder, 2–3.5 h | Existing SVN history/server-author attribution and rights; surviving Git signature/default-policy/every-parent judgement; protected-state guard. | Reviewed skeleton and settled guard capability contract; no invented signature or author proof. |
| 4 | Critical Builder, 1–2 h | Shared/Git-only CLI capability dispatch, shrinking ratchet, supplied printed-command quoting and pre-release pin/skip controls; README/ADOPT accurate scope. | Reviewed skeleton and supplied original finding texts; retained R25/R26 and archive format. |
| 5 | Archive Builder, 1–2 h integration allowance | Integrate independently reviewed archive source, manifest/pins and no-Git acquisition with final backend. | Archive critical verdict, final-tree dry run, release-script adaptation and actual qualification. |
| 6 | Independent critical Reviewer, 1–2 h initial pass | Judge the exact integrated head against FM-044 acceptance, real positive/refusal controls and retained Git authority. | Findings and required five-job CI; no completed proof-platform claim under held D4. |

The initial 4–8 h implementation estimate becomes 6–10.5 Builder hours before archive/review. Dependent work may overlap only from the reviewed common base with declared function ownership; two seats do not edit one shared function concurrently.

## Guard capability contract

Current SVN guard reports unsupported protection. The accepted filing requires refusal when authority cannot be established; moving the old empty success behind a backend does not satisfy it. The bounded proposal preserves existing server-authenticated author/history and legacy configuration meanings, refuses a protected change when the configured proof cannot be obtained, permits harmless local reads and makes no SVN signature claim. Missing server/login cannot become an author; a working-copy label cannot become a verified Owner decision. The design must identify the committed baseline, pending/copy/merge handling and actual refusal before writes. If satisfying it would change authority rights or historical interpretation, stop that slice and raise the exact proposed decision on the board for a signed Owner answer; other routing work continues.

Independent acceptance includes Git R14/default-branch trust and every-parent guards; SVN author/unreadable-history/copy/merge refusals; no-Git shared init/new/index/check/board/triage; one-line Git-only refusals before writes/processes; board no-network/no-mutation/tripwire controls; safe archive source validation before copying. Expectations come from the signed scope and recovered tracker, not Builder code. No plain-folder expansion or proof-platform assignment is authorized.
