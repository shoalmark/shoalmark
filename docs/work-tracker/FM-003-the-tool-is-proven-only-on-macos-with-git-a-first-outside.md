---
id: FM-003
status: In Progress
considered: FM-001, FM-002
tags: process
next: build
hook: "Every proof so far is macOS, git, one Owner. The first outside user works on Windows, with Subversion and TortoiseSVN, in German — and his agents will be asked whether the tool is worth adopting. Nothing of that has been run."
---

# FM-003 — The tool is proven only on macOS with git — a first outside user runs Windows and Subversion

## What is true now

**Opened 2026-09-21; pre-registered below, nothing built.** Held against FM-001 (the port: git only) and FM-002
(branding: macOS only). What git is used for, measured: the root marker (after `shoalmark.toml`), `git log` for a
pass's *last worked on*, submodule facts, `--install-hook`, `.gitignore` lines in `--init`. What is Unix-only,
measured: messages and hooks name `python3`; output carries `—` `→` `◐`, which a cp1252 console cannot encode; a
deriver is found by its executable bit; no CI exists.

## Done when — pre-registered claims

| # | Claim | Proof | Kills it if |
|---|---|---|---|
| W1 | **Both suites are green on Windows**, Python 3.9 and 3.12, beside macOS and Linux | a GitHub Actions matrix, run on the repository | a check has to be deleted rather than fixed or honestly skipped with a reason |
| W2 | **A cp1252 console does not crash a run** | a check that runs the tool with `PYTHONIOENCODING=cp1252` and reads its exit code | it needs a dependency |
| W3 | **Every message names a command that exists on the machine it ran on** | `python` on Windows, `python3` elsewhere; asserted in CI | — |
| S1 | **In a Subversion working copy with no git at all:** `--init`, `--new`, the gate, `INDEX.md`, the board and `--triage` facts work | a check that builds a `file://` repository with `svnadmin`, in CI on all three systems | the core needs a VCS abstraction of more than ~60 lines |
| S2 | **`--install-hook` on Subversion wires what Subversion has:** `tsvn:startcommithook` (write `INDEX.md` before the dialog lists files), `tsvn:precommithook` (refuse on a violation), `svn:ignore` for the board — and says plainly that command-line `svn commit` runs no hook | the properties read back with `svn propget` | — |
| S3 | **The contract `--init` writes says the true thing for the VCS it finds** — no "staged", no "branch" where there is none | read back in the S1 check | it needs a second contract text |

**Forecast:** W1 0.55 (path separators and the browser checks are where I expect red) · W2 0.85 · W3 0.9 · S1 0.75 ·
S2 0.8 · S3 0.8 · all six 0.3.

**Cannot be proven here, named now:** TortoiseSVN is a GUI — that it *runs* the two properties, shows its approval
dialog and keeps the commit dialog open on a refusal needs a person on Windows. The four-line property value
(command · `true` wait · `hide` · optional `enforce`) is from TortoiseSVN's source as remembered, not from its manual.

## Ship log

| Date | Event |
|---|---|
| 2026-09-21 | Filed; claims and forecast written before any code. |
