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

**2026-10-13 — bounded common skeleton built; independent critical review is next.**
On `fm/044-stage-1-skeleton`, the neutral refactor `4f1664d` follows the judged parent `170985c` (Owner filing #167 at
`e6d1e27`). Its 19 wrapper controls also pass against that immutable parent; the refactor retains Git argv/cwd/environment,
return/error and SVN byte/LF/XML semantics. The separate dispatch change selects Git/SVN once per configured ROOT,
resets repository/dispatch caches on reconfiguration, and routes administrative-path discovery through that selection.
SVN metadata starts no process; missing, empty, non-regular, symlinked or unreadable working-copy records refuse in one
line with exit 4. Git own/common and linked-worktree directories, ancestor/nested disk metadata and symlink/filesystem
aliases remain excluded. A Git request at the layer for an SVN target refuses before launch; arbitrary cwd cannot bypass
it. Source HERE uses `source=True` only for the four fixed existing provenance reads; source acquisition/parsing is unchanged.

Final compile and all 243 `test_core.py` checks pass (33.044 s for core), including real local SVN with its executable
available and Git absent, actual `--root --schema` metadata probes at the working-copy root/subdirectory, root-cache reset,
linked-Git/admin positive/refusal cases and 26 ratchet controls. Existing FM-045 Git command classification retains 30
commands with no unresolved/unclassified start, and its injected boundary/`git_out` calls are detected. Three selected R14
signature/default-policy/every-parent controls pass on both the refactor and final dispatch (150.797 s for the latter), as recorded in the
[check/caller evidence](evidence/stage-1-skeleton-checks-2026-10-13.md). Full suites and the retained five-job code matrix
remain CI work after Owner push; no platform trial is claimed under D4.

The transitional launch ratchet scans **Python process references in `shoalmark.py`**. Its initial ceiling and mutable
allowlist identify function/operation/API/normalized call, preserve occurrence counts and compare prior list revisions;
new literal, renamed, aliased/dynamic starts and list growth/resurrection fail, while migration can shrink the list.
There are still **63 direct starts: 55 Git, 3 SVN and 5 non-VCS/dynamic**; all are declared in the
[initial ceiling](../test_vcs_launch_ceiling.json) and [caller evidence](evidence/stage-1-skeleton-checks-2026-10-13.md).
The scanner excludes generated hook shell, release scripts, fixtures and documentation tooling, whose existing controls
remain. It is a static process-API ratchet, not proof against arbitrary Python obfuscation. Administrative-path discovery
checks local file accessibility and guards paths; it supplies no SVN database integrity, history/author or protected-state
proof. Shared commands, board read-only SVN capability, rights/guard and CLI migration remain dependent work: full-tool
SVN without Git is **not** complete. The unresolved committed consumer policy anchor cannot be replaced by Source HERE;
protected acceptance must conservatively refuse in its later guard slice. Archive source at `3c18008` remains separate;
its non-Git `git_dirs` integration is preserved semantically, and eventual `archive_source` must explicitly use
`source=True`. The [Builder brief](evidence/stage-1-builder-brief-2026-10-13.md), D3/D4 holds and R14/R25/R26 remain
retained. Dependent seats start only after independent critical skeleton review; this Builder supplies no verdict.

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
| 2026-10-13 | Independent records verdict ce014e4 merged in Owner PR #167 at e6d1e27; command-applied triage keeps P1 #3 build, and the seat sets In Progress before the common skeleton. Bounded Builder/dependent-seat brief recorded, with guard contract and D3/D4 holds explicit; no implementation or proof claimed. |
| 2026-10-08 | Filed, for 0.19.2. |
| 2026-10-13 | Filing recovered from `99050b9` on current main; RV-2735–RV-2737 fixed, acceptance bounded to signed R23 and FM-023, records review next. |
| 2026-10-13 | FM-044 common-layer neutral refactor: only git_out/svn_run launch mechanics moved behind vcs_process. Immutable-parent/refactor wrapper contracts and real Git/SVN positive/refusal fixtures pass; compile and test_core pass; metadata dispatch, ratchet, independent critical review and dependent migrations remain due. |
| 2026-10-13 | FM-044 bounded skeleton dispatch built after neutral refactor 4f1664d: cached ROOT selection, no-process SVN metadata, fail-closed administrative paths and constrained target/source process requests. Compile and 243 core checks pass; 63 retained direct starts and exact scanner/proof limits declared. Independent critical review next; dependent migrations, archive integration, CI and platform decisions remain due. |
