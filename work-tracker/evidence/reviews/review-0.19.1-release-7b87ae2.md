# FM-006: v0.19.1, the release branch, the scoped review at 7b87ae2

Verdict: **READY**: no finding stands. Ids RV-2710 and RV-2711; RV-2712 to RV-2729 are unused.
Reviewed: 7b87ae29e2b79f93787eaef74539a9f8eeda0421. Scope: `git log 8031740..7b87ae2`: c7382a8, 6793551 and 7b87ae2. Tier: critical (security).

## What holds

- `cat_blobs` reads git's `<oid> submodule` header as a submodule: no text, the type `commit`, the next header read at once. A header it cannot read, or an object cut short, is no text and ends the read. A name holding a line break is never asked and has no text. Every other name gets its own answer: measured on 13 streams (the header first, last, between files, twice in a row, beside `missing` and `ambiguous`, a file whose text holds such a header, an empty file, an unreadable header, a cut object) and in a repository.
- A configuration that is a submodule is one the guard cannot read, through that header as through any other. The other `cat-file` readers read no size from a header, so none misreads a submodule's.
- `read_config` refuses, in one line, a `tracker_dir` that starts with `/` or any of whose parts is drive-shaped. The live run, `--init` and the guard read it there, so each refuses it alike, before any read or write. Measured on 1884 values, on Windows and POSIX roots: every value accepted is one folder inside the root, the same for the run and the guard. `[ratio]`'s default records are that folder.
- `--init` refuses an absolute `tracker_dir`, inside the repository or beside it, in that one line, exit 1, as the backslash rule does, naming the way through; nothing is written. The CHANGELOG's line holds, and no README or docs line contradicts it.
- The gate refuses a tracker whose file name holds a line break, in one line naming the file and the way through, exit 4. A seat's close of another tracker in the same commit is refused, as it is alone. Renaming the file passes; a rename with a close is refused. This repository's own `--check` passes.
- ADOPT.md and ADOPT.de.md name the SHA-256 of 7b87ae2's `shoalmark.py` (a731fe70…); nothing else in either changes.
- CodeQL's two alerts (`unmerged_advice`'s two prints, :2694 and :7812 at 7b87ae2): nothing sensitive is printed. The line names the branch, the trunk, the tracker, the command to run again, at most three of the person's own commits (short hash and subject, 60 characters at most) and `--queue`'s wait line, which names a commit as git records it. The name and email passed in are compared, never printed. No credential, token, URL, key or file content.

## Findings

- **RV-2710 · P2:** fixed at 6793551, measured.
- **RV-2711:** recorded privately.

## Commands and controls: 2026-10-07 and 2026-10-08, CEST, as `date` printed each

- At c7382a8: `py_compile` exit 0; `test_core.py` exit 0, all green (23:08:26–23:08:40); `--check` exit 0; `--session-check` exit 0 (23:08:45–23:08:55).
- At 7b87ae2: `py_compile` exit 0; `test_core.py` exit 0, all green (00:30:55–00:31:13); `--check` exit 0; `--session-check` exit 0 (00:31:13–00:31:25).
- run-one-check, two at a time, at c7382a8 and again at 7b87ae2: the FM-037 block (61 ok, 0 FAIL, the submodule, gitlink and drive-qualified checks in it), the `tracker_dir` check, the backslash check and the 7 `--init` cases; at 7b87ae2 the two line-break checks too. Each exit 0 (23:09:42–23:21:16; 00:25:41–00:34:15).
- Controls, run-one-check two at a time (23:09:42–23:18:17; 00:26:34–00:33:50): the submodule check, the drive-qualified guard check and the two `--init` absolute cases exit 1 beside 8031740; the `tracker_dir` check exits 1 beside 8031740 and beside c7382a8; the `cat_blobs` line-break check exits 1 beside c7382a8; the gate's line-break check exits 1 beside 6793551.

Quality read: the three commits' messages and check names say what is asserted; reads clean.
