# v0.19.0 — the scoped check of the private security report's fix, at 0cfaf35

Verdict: **READY** — no open finding. The texts this check found untrue are fixed in the second round and in 0cfaf35. RV-2280 … RV-2289 unused.
Reviewed: 0cfaf35500af16f3b77f26b3b6c1ecb6f95df0c2 — `git diff fec3413 0cfaf35`: afa1a11 (the fix and its tests), f55b4fb (the CHANGELOG line, README.md:514), c5ccdae (the checksum), 40f369e and 750f370 (the second round), 0cfaf35 (README.md:284, `.gitignore:1`); the Planner's filings fec3413, 94189db and 3be27e1 are records.
Reviewer: b3bdb000/reviewer-80 (claude-opus-5-5, xhigh), the reviewer's bot address, unsigned, worktree shoalmark-review-11, 18:00–18:15 CEST on 2026-10-01. Independence: the builds' session (b3bdb000), so not independent.
Tier: code. Spec: the Owner's rulings filed in FM-006 at fec3413 (*A private security report, P1, fixed before the tag*), 94189db (*its second round*) and 3be27e1.

## The fix, at c5ccdae
1. **The checkout case holds, run by hand in scratch repositories with their own hooks,** as the ruled test sets it up: a deriver that leaves a marker. After c5ccdae's `--install-hook` re-run, none of these starts it: a switch there, a switch back, `merge --no-ff`, `git checkout <file>`, `git pull` (fast-forward and with a merge commit), a clone with its own hooks, and `--html-only`. The default run does (the control), so the marker is a real test.
2. **The re-run holds.** It removes the `post-checkout` and `post-merge` an older copy wrote, one line each, and keeps three hooks. A `post-checkout` that is not shoalmark's stays byte for byte.
3. **No other path.** The deriver runs only from `main`'s two calls. The per-commit flags (`--session-trailer`, `--session-check`, `--commit-msg`) return before them; `board_after_act` rebuilds with `--html-only`; `answer_cmd` and the TortoiseSVN properties run on the person's own commands. The deriver still runs where it always did: the default run, and the pre-commit hook on a commit that stages a tracker.
4. **The tests.** The five changed or new checks — the hook count, the checkout case, the re-run, the deriver block's *board's run* and FM-030's act test — fail beside fec3413's tool and pass at the tip. Each tests what it says: the checkout case by a real marker and its control; the *board's run* by the processes started (`argv_of`); FM-030 by the command's own rebuild and the board's *on its way*.
5. **The CHANGELOG line** is FM-006's text word for word, the flags as code; README.md:514 lists `write · check · read`. The checksum: `git show c5ccdae:shoalmark.py | shasum -a 256` is `22cd0e9e…57ad7c`, once in each note; `e9c4e4ee` is gone; afa1a11 is the last commit to touch `shoalmark.py`.
6. **The code's comments** stay as the Owner ruled them: each says in one sentence why the code refuses. **Nothing else changed:** the texts, `no_derived`, the two hooks out, the removal loop, and `main`'s skip.

## The second round, at 750f370, and the two lines, at 0cfaf35
7. docs/setup.md:75 and docs/de/setup.md:76 drop *and checkout* / *und Checkout*. lefthook.yml loses only its `post-merge` block (4 lines). The CHANGELOG line is FM-006's text with 94189db's tail, word for word. `shoalmark.py` and both notes are byte-identical to c5ccdae, and the checksum still stands once in each.
8. README.md:284 reads as 3be27e1 files it: *…the board is rebuilt by the command itself (`--html-only`) where nothing else rebuilt it, and the command says which.* It is true against `board_after_act` and FM-030's test. `.gitignore:1` names *the board*. 0cfaf35 changes only those two files. `--check` and `--session-check` exit 0 at the tip.
9. **The search for texts the fix made untrue** covered README, `docs/` in English and German, both notes, AGENTS.md, the contract `--init` writes and `--help`. It found README.md:284 and the two setup lines, besides `.gitignore:1`; all are fixed here. `--help` for `--install-hook` and `--html-only` follows the fix.

## Controls
- Each setup: clean; one fetch per head; detached at the head, equal to `ls-remote`. Every scratch run under the session's temporary directory, with its own hooks folder; no tag created.

Quality read: the fix is the smallest that holds — two hooks fewer, one loop that removes what an older copy wrote, and one branch in `main` that keeps `--html-only` away from the deriver, with the texts that described the old behaviour corrected. `HOOK_LINES.get(name, '--html-only')`'s fallback can no longer be reached and may go after the tag. The rest reads clean.
Next: the Planner's final full run on 0cfaf35, then the Owner marks the pull request ready.
