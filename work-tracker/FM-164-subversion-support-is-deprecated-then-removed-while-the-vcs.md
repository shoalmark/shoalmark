---
id: FM-164
status: Proposed
considered: FM-003, FM-004, FM-005, FM-006, FM-007, FM-008, FM-014, FM-023, FM-027, FM-030, FM-031, FM-032, FM-035, FM-037, FM-044, FM-045, FM-046, FM-050, FM-054, FM-057, FM-058, FM-059, FM-068, FM-069, FM-070, FM-074, FM-100, FM-129, FM-151
tags: process
next: owner
hook: "shoalmark supports Git, Subversion and the plain folder, so every change touching history, the gate or the hooks is built and proven twice. With one version-control system and the plain folder, every lane is simpler. The proposal, put to the Owner as FM-164-Q1: Subversion is deprecated with a release's notice, then removed, and the VCS layer stays, with Git, the plain folder and a test double behind it."
ask-id: FM-164-Q1
ask: "Do you take FM-164's decisions as proposed: Subversion deprecated in v0.20.3 and removed in v0.21.0, the VCS layer kept with Git, the plain folder as it is today and a test double, and the notice as worded?"
ask-kind: ruling
ask-since: 2026-11-12
ask-options: "yes, as proposed | yes, with the changes I name | no, Subversion stays"
ask-proposal: "yes, as proposed"
---

# FM-164 — Subversion support is deprecated, then removed, while the VCS layer stays

Seat: the Planner (27f31560) · filed 2026-11-12, on the Auditor's word of that day.

## What is true now

**Filed 2026-11-12, Proposed, with FM-164-Q1 put; nothing is built.** Every place below was found by reading main at
`7c93c835`.

- **Subversion is supported today,** without git, since v0.20.0. The README says it "passes the test suite but has not
  been used in real work"
  ([README L29](https://github.com/shoalmark/shoalmark/blob/7c93c835d6ac9842bb28a37118822f4a6b8a661b/README.md#L29)).
  v0.20.1 and v0.20.2 changed it by fixes only, among them
  [FM-068](FM-068-tortoisesvn-drops-the-hook-properties-install-hook-writes-so.md),
  [FM-069](FM-069-the-subversion-notice-prints-on-every-run-and-reads-as-the.md) and
  [FM-070](FM-070-the-gate-s-text-shows-as-mojibake-in-tortoisesvn.md); it has had no new features since.
- **The VCS layer** is one selector: `select_vcs` finds the nearest `.git` or `.svn` marker, and `vcs()` returns
  `"git"`, `"svn"` or `""`, the plain folder
  ([`shoalmark.py` L180–L191](https://github.com/shoalmark/shoalmark/blob/7c93c835d6ac9842bb28a37118822f4a6b8a661b/shoalmark.py#L180-L191)).
  The tool branches on its value: 41 times on `"svn"` and 61 times on `"git"`. It grew from
  [FM-044](FM-044-shoalmark-stops-with-a-traceback-where-git-is-not-installed.md), which made the tool run where git is
  not installed.
- **Where Subversion lives:**
  - **The tool:** 30 functions of its own, from `svn_local_status`
    ([L444](https://github.com/shoalmark/shoalmark/blob/7c93c835d6ac9842bb28a37118822f4a6b8a661b/shoalmark.py#L444))
    to `tsvn_arguments`
    ([L12624](https://github.com/shoalmark/shoalmark/blob/7c93c835d6ac9842bb28a37118822f4a6b8a661b/shoalmark.py#L12624)).
    They cover the gate's history reads, ship-log proof, ids, the board's read line, `--install-hook`'s TortoiseSVN
    properties (`install_hook_svn`, L11861), the hidden `--tsvn-hook` (L10882), the guard (`svn_guard`, L9675),
    and the stand-up prompt's Subversion form
    ([L5236](https://github.com/shoalmark/shoalmark/blob/7c93c835d6ac9842bb28a37118822f4a6b8a661b/shoalmark.py#L5236)).
    The Board's words for it are in the language packs, `read.svn` among them (`examples/de/labels.yaml` L130–L225).
  - **The adoption probe:** `ADOPT.svn.md` and `ADOPT.svn.de.md`, which `ADOPT.md` and `ADOPT.de.md` point to
    ([`ADOPT.md` L63–L64](https://github.com/shoalmark/shoalmark/blob/7c93c835d6ac9842bb28a37118822f4a6b8a661b/ADOPT.md#L63-L64)),
    and the site's facts script reads them (`scripts/landing_facts.py` L588).
  - **The documents:** the README (L28–L41, L72, L204, L235, L267, L312), `docs/setup.md`, `docs/signing.md`,
    `docs/standup.md`, `docs/triage.md`, `docs/how-it-works.md` and their German twins, `docs/index.md` and
    `docs/de/index.md`, `CONTRIBUTING.md` L15, the landing's partials in English and German, the probe's
    `how-it-works` pages, and `brand/design-guide.md` L335–L338.
  - **The tests:** `test_vcs_skeleton.py`, `test_vcs_shared.py`, `test_vcs_entry.py`, `test_vcs_guard.py`,
    `test_tsvn_hooks.py` and `test_tsvn_source_binding.py`, and Subversion cases in `test_shoalmark.py`,
    `test_proof.py`, `test_standup_repos.py`, `test_day_prompts.py`, `test_tracker_text.py`, `test_run_bounds.py`,
    `test_git_entry_differential.py` and `test_core.py`.
  - **CI:** Subversion is installed on all three systems, and a step checks that it is really there
    ([`ci.yml` L117–L134](https://github.com/shoalmark/shoalmark/blob/7c93c835d6ac9842bb28a37118822f4a6b8a661b/.github/workflows/ci.yml#L117-L134)).
  - **The records** under `work-tracker/evidence/` and the CHANGELOG's history stay as they are: they are history.
- **Open trackers this touches:** [FM-074](FM-074-the-docs-do-not-name-two-subversion-limits-first-no-gate-on.md)
  and [FM-129](FM-129-no-real-windows-run-has-yet-shown-the-gate-s-text-in.md) are about Subversion alone;
  [FM-100](FM-100-the-stand-up-prompt-is-code-and-english-on-every-board-while.md)'s stage 1 tests `standup` in five
  setups, Subversion among them; [FM-151](FM-151-a-records-only-pull-request-waits-for-a-macos-runner-that.md) plans
  CI's jobs with Subversion in them; [FM-004](FM-004-nobody-knows-whether-another-project-s-agents-would.md) holds the
  probe's record. `TRIAGE.md`'s current path names Subversion without git in its line for v0.20.0
  ([L18](https://github.com/shoalmark/shoalmark/blob/7c93c835d6ac9842bb28a37118822f4a6b8a661b/work-tracker/TRIAGE.md#L18)):
  that text is the Owner's.

## Why

Every change that touches history, the gate, the hooks or the Board is built, tested and reviewed for Git and for
Subversion, on three systems. With one version-control system and the plain folder, every lane is simpler. The VCS
layer stays, so that another system can plug in later through the same seam.

## Decisions, for the Owner

The ask, FM-164-Q1, asks for all of these at once. An answer of "yes, with the changes I name" names each change by
its number.

1. **The deprecation is in v0.20.3.** Its CHANGELOG and the README announce it, and the adoption notes, the setup page
   and the landing say it where they name Subversion. Subversion keeps working in v0.20.3, unchanged. This part is
   records and docs only.
2. **The removal is in v0.21.0,** its own lane. It takes out the Subversion implementation, `ADOPT.svn.md` and
   `ADOPT.svn.de.md`, Subversion's parts of the documents and the landing, its tests, and CI's Subversion steps.
   Adopters on Subversion get one release's notice: v0.20.3. Its review is critical, since it touches the gate.
3. **The VCS layer stays.**
   - `select_vcs` and `vcs()` keep their place, with Git and the plain folder behind them.
   - A test double, a third system that exists only in the tests, plugs in through the same seam. Its tests hold that
     each place that branches on the system still asks the layer, so the seam stays honest after the removal.
   - The removal leaves no Subversion branch behind. A `.svn` folder is then a plain folder to the tool, which says
     so once.
4. **The plain folder keeps what it does today, and nothing more:** the trackers, `INDEX.md`, the Board, `--new` and
   `--standup`. It has no history, so it holds no rights, signed answers or ship-log proof, as today
   ([`ADOPT.md` L219–L221](https://github.com/shoalmark/shoalmark/blob/7c93c835d6ac9842bb28a37118822f4a6b8a661b/ADOPT.md#L219-L221)).
5. **The notice, as worded,** the same in the CHANGELOG and the README, with its German twin where the page has one:
   > **Subversion support is deprecated.** It keeps working in 0.20.3 and is removed in 0.21.0. From then on,
   > shoalmark supports Git and the plain folder: one version-control system, so every change is simpler to build and
   > prove. A Subversion working copy can stay on 0.20.3, move to Git, or run as a plain folder, without history.
6. **The open trackers follow the removal.** FM-074 and FM-129 close as superseded when it ships. FM-100's stage 1
   drops Subversion from its setups if the removal lands first. FM-151 plans CI without it.

## Done when

Each item names its commit or pull request when it lands.

- [ ] **The Owner has answered the ask,** FM-164-Q1.
- [ ] **v0.20.3, the deprecation:** the notice in the CHANGELOG and the README, and in the adoption notes, the setup
  page and the landing where they name Subversion, in English and German, with the pair checks passing. Subversion
  still passes the suites.
- [ ] **v0.21.0, the removal:** the Subversion implementation, its documents, its tests and CI's steps are gone, and
  a `.svn` folder reads as a plain folder, with a test.
- [ ] **The seam:** the test double plugs into `select_vcs` and `vcs()`, and its tests fail where a place branches on
  the system without asking the layer; a mutant shows it.
- [ ] **The plain folder** does what decision 4 says, held by the existing tests and one for the `.svn` case.
- [ ] **The open trackers** are closed or changed as decision 6 says, each in its own commit.
- [ ] **The removal's critical review is READY.**

## Ship log

| Date | Event |
|---|---|
| 2026-11-12 | Filed, Proposed, with FM-164-Q1 put: Subversion deprecated in v0.20.3 and removed in v0.21.0, as proposed. Records only. |
