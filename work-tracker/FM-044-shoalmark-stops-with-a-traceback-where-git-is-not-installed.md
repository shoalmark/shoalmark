---
id: FM-044
status: Proposed
considered: FM-003
tags: bug
next: wait
hook: "A Subversion team without git cannot run the tool at all: every command but --session-check stops with a traceback before it writes anything."
---

# FM-044 — shoalmark stops with a traceback where git is not installed, on Subversion too

## What is true now

**Filed 2026-10-08, for 0.19.2; nothing is built.** Where `git` is not installed, every command except `--session-check`
stops with a Python traceback (`FileNotFoundError`) before it writes anything. That holds in a folder with no version
control and in a Subversion working copy alike. The first call to fail is `git_dirs()` (`shoalmark.py:273`), which a
command reaches when it judges the tracker folder. The tool runs `git` directly in 53 places and through `git_out` in
the rest, and none of them handles a missing `git`. CI installs `git` on every system, so no check runs without it.

## Why

FM-003's S1 claims that a Subversion working copy "with no git at all" runs `--init`, `--new`, the gate, `INDEX.md`, the
board and `--triage`. Its check builds that working copy on a machine where `git` is installed, so the claim fails
exactly where a Subversion team has no `git`.

The Owner's ruling of 2026-10-08: Subversion and a plain folder are lanes of their own, and neither ever needs `git`.
The fix is a version-control layer, designed before anything is built, and it comes before the probe's next version.

## Done when

- **One layer.** The tool reaches version control through one layer, a section of `shoalmark.py`. It has three
  backends, chosen once per repository: Git, Subversion, and None, a plain folder.
- **Neither Subversion nor None ever starts `git`.**
  - What all three backends share runs on each.
  - What only Git can do (signed answers, the pull-request queue, answer branches) is refused elsewhere in one line.
  - No run stops with a traceback or tells a person to install `git`.
- **No backend judges less.**
  - The write rule, the guard and the judgement of the tracker folder fail closed.
  - The board's run starts only read-only commands and asks no server, on Subversion as on Git.
- **A ratchet check** finds every `git` or `svn` process started outside the layer and fails on any not on its list. The
  list may only shrink.
- **The proof:**
  - the existing suite runs unchanged on Git;
  - the Subversion and None suites run with no `git` on `PATH`, on all five CI systems;
  - FM-045's board matrix runs on all three backends.
- **Fetching without `git`:** the tool and `--vendor` work from an archive attached to each release, with its SHA-256.
- **README and ADOPT** say what runs on each backend.

## Ship log

| Date | Event |
|---|---|
| 2026-10-08 | Filed, for 0.19.2. |
