---
id: FM-044
status: Proposed
considered: FM-003
tags: bug
next: review
hook: "A Subversion team without git could not run the reviewed copy: every command but --session-check and --queue stopped with a traceback before it wrote anything."
---

# FM-044 — shoalmark stops with a traceback where git is not installed, on Subversion too

## What is true now

**2026-10-13 — filing recovered on current main; no stage-1 build is supplied.** This replacement carries the filing
reviewed at `99050b9`, with RV-2735–RV-2737 corrected. The signed 12 October R23 lifts the hold for stage 1:
Subversion with no git installed, including the release archive and its pending scoped re-review. FM-023 allocates
that bounded stage and archive to v0.20.0. Plain-folder scope (D3) and where the no-git proof runs (D4) remain held
until trial findings and the 20 October review; this recovery supplies no platform trial or implementation evidence.
The records pass, Owner merge and Planner judgement precede stage-1 build.

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
| 2026-10-08 | Filed, for 0.19.2. |
| 2026-10-13 | Filing recovered from `99050b9` on current main; RV-2735–RV-2737 fixed, acceptance bounded to signed R23 and FM-023, records review next. |
