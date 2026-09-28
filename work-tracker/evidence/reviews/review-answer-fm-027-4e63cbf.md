# Review — the Owner's answer on FM-027, `--answer accept`, at 4e63cbf

- **Date:** 2026-09-28 08:25 CEST · **Seat:** Reviewer (Opus 5.5) · **Session:** `8e509911/reviewer-45` ·
  **Worktree:** `shoalmark-review-2`, detached at the tip.
- **Scratch:** the replay ran in a GitHub clone in this session's scratchpad (`review-pass-0928/r45/clone`), at
  `origin/main` `02f3c5c`. The Owner's checkout, every other worktree and every folder of session `8b91dba2` stayed
  outside every command.
- **Tier:** docs, one pass. This is path 3 under his signed FM-032 answer (`97fa87a`): one Reviewer docs pass on his
  answer pull request until FM-007's hardware key signs. A review of the Owner's own answer reports and never blocks.
- **Independence:** same session — a sub-agent of 8e509911, which put the ask. The answer is his.

**Reviewed:** `answer/fm-027` at `4e63cbf2fc758374810e7202b64ec75aa83ba8c6`. It is one commit on `origin/main` `02f3c5c` (PR 107, which carried the
ask, the night's filings). No pull request is open for it (`gh pr list --head answer/fm-027`: none open).

## The checks

| # | Check | Result |
|---|-------|--------|
| 1 | The commit is his | ✓ Author and committer are `holgo99 <holgoijo@gmail.com>`, 2026-09-28 08:13:09 +0200. It has one parent, `02f3c5c`, the tip of `origin/main` |
| 2 | Signed, and verified against the signers file | ✓ Verified with `origin/main:work-tracker/allowed_signers` as the signers file. That file has one entry, `holgoijo@gmail.com`, ed25519, and `ssh-keygen -lf` gives `SHA256:uNcUULP20UyJ7Iyv3xImxOrg9cXTcRqIxbWsekBYzCQ`. `%G?` is `G`, `%GS` is `holgoijo@gmail.com`, the key is that fingerprint and the trust is `fully`. The forge's `verification` reads `verified: true`, reason `valid` |
| 3 | The diff is exactly what the pinned 0.18.5 `answer_cmd` writes | ✓ 1 file. FM-027: `next: owner` → `build`, and the three lines after `ask-proposal:`: `answer: "accepted - <option 1>"`, `answered: 2026-09-28`, `answered-by: holgo99`. **Reproduced byte for byte:** in the scratch clone at `02f3c5c` I ran `answer_cmd(["FM-027", "accept", <ask-proposal>])` from `main`'s `shoalmark.py`. `owner_change` was a stub that keeps its `how`, and I applied `how["write"]` to `main`'s FM-027 as `owner_change` does, with no branch, no signature and no push. The file is byte-identical to `4e63cbf`'s, and so is `how["subject"]`. The move is `build`, from `ANSWER_MOVE` for a ruling |
| 4 | INDEX.md | ✓ Not in the diff, and none is owed, so it is not stale. FM-027 is Parked and unranked, and INDEX.md's Work table (*ID · Tier · Hook · Status · Board · Triaged*) has no *Next* column. A change of `next:` alone moves nothing there. `--check` at the tip reads *INDEX.md is up to date — 40 trackers*. |
| 5 | The text | ✓ `answer:` equals `"accepted - "` + `ask-proposal` byte for byte, and `ask-proposal` is option 1 of 3 byte for byte (120 characters). `--answered` at the tip prints *"FM-027 · answered 2026-09-28 by holgo99 … answer: accepted - a block per session, claimed on the server in the review folder: FM-027's design for tracker ids, extended to review ids … relation: accepted the proposal"*, and hands it to the seat with *"act on it, then `--clear-ask FM-027 <next move>`"* |
| 6 | The record under `## Asks` | None written, which is right. `answer_cmd` writes only the front matter; the record moves under `## Asks` when the seat's `--clear-ask` acts on it |
| 7 | The ask leaves his list | ✓ At `02f3c5c`, `--owner` reads *3 NEED THE OWNER* (FM-024, FM-027, FM-032). At `4e63cbf` it reads *2 NEED THE OWNER*, FM-024 and FM-032: FM-027 has left it |
| 8 | `--check`, `--session-check` | ✓ Both exit 0. `--check`: *INDEX.md is up to date — 40 trackers*; *judged before build: on — 1 commit(s) … every build commit under a judged In Progress tracker*; *the Owner's two sections: guarded — … none changes them or his signers file*; *filing freeze: 21 open* |
| 9 | The tool | ✓ `git diff origin/main 4e63cbf` touches no `shoalmark.py`, test, `lefthook.yml` or `scripts/`, and `VERSION` reads 0.18.5. **No suite was run**: nothing they test changed |
| 10 | merge-tree against `origin/main` | ✓ Clean. The tree `93b8414` is the branch's own, so the merge is a fast-forward. `git diff --check` is clean |

## What the queue reads for the branch

- **`--queue`** (the scratch clone, at `4e63cbf`) does not list `answer/fm-027`. `pushed_branches` leaves out `answer/*` by its
  rule, and no pull request is open for it.
- It prints one branch, `fm/030-the-board-reads-his-unme… @ ada15c6  wait: no pull request — no verdict on ada15c6`,
  with *1 waiting on you: 0 merge, 0 close, 0 wait, 1 pushed without a pull request*.
- Once a pull request is opened on this branch, `answer_reading` reads it at his answer commit. This verdict commit
  touches only its own review file, so `answered_at` passes over it (FM-031, 0.18.4).

## Findings

None of this pass's. RV-722 onward stay unminted.

*A known line, not a finding here:* the commit subject is `answer[:60]`, which here ends at a word boundary, *"…claimed on the server in the"*, with no ellipsis. It is recorded on FM-030's ship log
(2026-09-24, *"`--answer` cuts the commit subject at 60 characters"*) and in the CHANGELOG, and it is still open in
0.18.5. The signed `answer:` line is whole.

## Verdict

**READY.**
- The answer is his, signed and verified by the one key in `main`'s signers file and by the forge.
- The diff is exactly the pinned 0.18.5 `answer_cmd`'s output.
- The text is the proposal, option 1, byte for byte: *accepted the proposal*.

*The Owner lands this by merging; a merge rules nothing.*
