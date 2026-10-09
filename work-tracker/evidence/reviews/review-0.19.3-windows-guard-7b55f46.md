# FM-030: 0.19.3's Windows guard, its critical verdict at 7b55f46

Verdict: **READY WITH FINDINGS**. RV-2942 and RV-2943 (P3) stand, fixed forward. RV-2944 to RV-2949 are unused.
Reviewed: 7b55f46227a98bdc42cfc398dfd5e9d8f4dafef8. Scope: `git diff 6828dba 7b55f46`, one commit. Tier: critical.

## What holds

- On Windows, `notify_argv` names no program for any input: the suite's 28 vectors, and 2,000 random inputs in a scratch probe. `--notify` starts no process while a notice is posted, and every program its run starts is read-only git. Each notice is printed, its line ending "printed — no notice is posted on Windows". A notice of hostile text is printed with the others, and the run exits 0.
- macOS and Linux: `notify_argv`'s two branches, `notice_text`, `notify_cmd` and `post_notice`'s path with a notifier are byte for byte as at 6828dba. Only docstrings and the status where no program is named changed.
- The Windows code is removed: `notify_argv`'s PowerShell branch, Check A's PowerShell pin, the Windows argv check and the real PowerShell run. Check A reads the tool clean: 30 commands, nothing unread, the deriver's sites met once each, and no PowerShell start. Code handed to PowerShell inside `notify_argv`, literal or not, or anywhere else, is not read.
- README's `--notify` row says what each system does.
- The commit message carries no id and says nothing of the notice's earlier code.
- The two Chrome renders the build skipped show board views this commit does not touch. Nothing in scope depends on them.

## Findings

- **RV-2942 · P3:** on Windows the summary line counts each printed notice as posted ("--notify: 3 posted · …") above lines that end "printed — no notice is posted on Windows". It reads as on a system with no notifier, but the two lines contradict each other. Fix: on Windows the summary's two counts read "printed" and "printed before".
- **RV-2943 · P3 (records):** FM-030's What is true now says `--notify` hands Windows PowerShell fixed code, "on every platform". At the guard it starts no program there. Fix, with Tuesday's merge: "… on Linux they are `notify-send`'s own arguments, after `--`; on Windows it starts no program and prints each notice."

## Commands and controls: 2026-10-09, CEST, as `date` printed each

- At 7b55f46: `py_compile` exit 0, under Python 3.14 and 3.9.6. `test_core.py` exit 0, all green. `--check` exit 0 and `--session-check` exit 0 (21:45:13–21:45:52).
- run-one-check, two at a time, at 7b55f46, each exit 0 (21:45:14–22:07:18): 18 FM-030 blocks (94 checks), the notice and D blocks among them, and Check A's block (7 checks). The 3 FM-030 blocks that read an earlier statement's names exit 0 with it (5 checks, 22:07:20–22:09:32).
- Controls beside 6828dba, each exit 1: the notice block (its 4 Windows checks fail), the D block (1 of 7) and Check A's block (2 of 7).

Quality read: the commit message, check names and comments say what is asserted.
