# v0.19.1 — B1, `--init` writes nothing before a refusal: the review at ef8cea4

Verdict: **READY**. RV-2343 (P2) and RV-2344 (P3) are closed. One P3 is parked by the Owner's ruling. RV-2346 onward are unused.
Reviewed: ef8cea4acbc5e3ed7334166626b7727998d5b02a — `git diff 1c4cb81 ef8cea4`: 485ae1d, a30fbdc and ef8cea4, to `shoalmark.py` and `test_shoalmark.py`, against the Owner's ruling of 2026-10-03.
Reviewer: b3bdb000/reviewer-85 (claude-opus-5-5, xhigh), at the reviewer's bot address, unsigned, in worktree shoalmark-review-9, on 2026-10-04. Not independent: this is the build's session. Tier: critical — code, so the full loop.

## What holds

- **485ae1d:** before the first file is written or a folder made, `--init` reads AGENTS.md and .gitignore under the reading rule and judges the tracker folder that Subversion's `svn:ignore` is set on. It puts the configuration, TRIAGE.md, AGENTS.md, CLAUDE.md and .gitignore under the write rule, each where it may write them. A file that is judged but left unwritten is a regular file the reading rule passed.
- **After the writes:** `configure()` reads back the configuration just written, and that text is judged before the first write (a30fbdc). Subversion's `svn add` and `svn propset` act on the tracker folder `--init` has just made; that folder is judged first, and neither step refuses.
- **a30fbdc (RV-2343):** the folder's name goes into the configuration as a string, its `"` and `\` escaped, and reads back as the folder's name. **ef8cea4 (RV-2344):** a name the configuration cannot hold on one line is refused in one line, exit 4, naming the folder's name and saying to rename the folder; nothing is written.
- **Probed in scratch on this macOS machine:**
  - refused with nothing written: a fresh git repository with AGENTS.md, CLAUDE.md or .gitignore a symlink; a Subversion working copy with AGENTS.md a symlink; folder names with a line feed, a carriage return or U+2028;
  - refused by the reading rule, whether or not it needs a change: an initialised repository whose AGENTS.md or .gitignore is a symlink;
  - initialised, the name reading back: folders named `q"repo`, `repo\` and `x\n`.
- **Windows:** the folder-name checks skip there, visibly, with their reason. The commit messages and test names say what is asserted.

## Findings

- **RV-2343 · P2, closed in a30fbdc:** the configuration's `name` is judged before the first write.
- **RV-2344 · P3, closed in ef8cea4:** the refusal's line and its exit.
- **RV-2345 · P3, parked by the Owner's ruling:** `--init`'s exit status where `svn add` fails.

## Commands and controls, as `date` printed them

- At ef8cea4: `py_compile` ok. `test_core.py`: 158 ok, all green, exit 0. `--check` and `--session-check` exit 0. 08:50:36–08:51:00 CEST.
- At ef8cea4, with `run-one-check.py`, every `--init` block exits 0, 08:50:28–08:52:35 CEST: B1's three checks, the folder's name (3), the scaffold, never overwrites, the contract's markers, the write rule before a folder is made and its control, and the Subversion working copy.
- B1's three checks exit 1 beside `1f73865`'s tool, and 0 at 485ae1d. 07:28:37–07:31:07 CEST.
- The two folder-name checks that initialise exit 1 beside `1f73865` and beside 485ae1d, and 0 at a30fbdc. 07:56:45–08:01:07 CEST.
- The line-break check exits 1 beside `1f73865` and beside a30fbdc, and 0 at ef8cea4. 08:50:28–08:52:35 CEST.
