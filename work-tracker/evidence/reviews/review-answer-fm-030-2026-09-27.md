# Review — the Owner's answer on FM-030, `--answer accept`, at 920970b

**Date:** 2026-09-27 15:05 CEST · **Seat:** Reviewer (Opus 5.5) · **Session:** `8e509911/reviewer-39` · **Worktree:**
`shoalmark-review-4`, detached at the tip. I made the reproductions in a scratch clone in the session's scratchpad
(`review-ask-030/`), with no remote. The Owner's checkout, `shoalmark-gtm`, every other worktree and every folder of
session `8b91dba2` stayed outside every command. The tool reads its signers file as the default branch's blob, not
the file its configured path names in his checkout.
· **Tier:** docs, one pass. This is path 3 under his FM-032 answer, because FM-007's hardware key has not signed this
answer. A review of the Owner's own answer reports and never blocks.
· **Independence:** same session. I am a sub-agent of Principal session `8e509911`, which put the ask. The answer is his.

**Reviewed:** `answer/fm-030` at `920970b7bf2df5ae5bd6d074e3a39da2c9b52351`. It is one commit on `origin/main`
`eaacbc96618217518e6b2a26cf9f37327ff1bf02` (PR 101, which carried the ask, merged 14:53:43). No pull request is open for
it yet (`gh pr list --head answer/fm-030 --state all`: none).

## The checks

| # | Check | Result |
|---|-------|--------|
| 1 | The commit is his | ✓ Author and committer `holgo99 <holgoijo@gmail.com>`, 2026-09-27 14:56:15 +0200. One parent, `eaacbc9`, the tip of `origin/main`. The subject is `FM-030: accepted - the board reads git: an unmerged \`origin/answer/*`: the tool's own `f"{tid}: {answer[:60]}"`, reproduced in check 3 (R1) |
| 2 | Signed, and verified against the signers file | ✓ With `origin/main:work-tracker/allowed_signers` (one entry, `holgoijo@gmail.com`, ed25519) as the signers file: `%G?` is `G`, the trust is `fully`, the key is `SHA256:uNcUULP20UyJ7Iyv3xImxOrg9cXTcRqIxbWsekBYzCQ`, the fingerprint of that entry. The forge's `verification` reads `verified: true`, reason `valid` |
| 3 | The diff is exactly what the pinned 0.18.5 `answer_cmd` writes | ✓ 2 files. FM-030: `next: owner` → `build`, and the three lines after `ask-proposal:`: `answer: "accepted - <option 1>"`, `answered: 2026-09-27`, `answered-by: holgo99`. INDEX.md: FM-030's ranked row, `owner · *complicated* · intended` → `build · — · intended, kind`. **Reproduced byte for byte.** In a scratch clone at `eaacbc9` I ran `answer_cmd(["FM-030", "accept", <ask-proposal>])` from `main`'s `shoalmark.py`. `owner_change` was replaced by a stub that keeps its `how`, and I applied `how["write"]` to `main`'s FM-030 as `owner_change` does (no branch, no signature, no push). The file is byte-identical to `920970b`'s, and so is `how["subject"]`. INDEX.md regenerated over it is byte-identical except for the scratch's own five-line block, which flags an uncommitted answer by a non-seat author. At the tip in that clone `--check` says *INDEX.md is up to date* |
| 4 | The text | ✓ `answer:` equals `"accepted - " + ask-proposal` byte for byte, and `ask-proposal` equals option 1 byte for byte (119 characters). `--answered` reads *relation: accepted the proposal* |
| 5 | The ask leaves his list | ✓ At `eaacbc9`, `--owner` reads *1 NEED THE OWNER*, FM-030. At `920970b` it reads *NO QUESTION FOR THE OWNER · 3 ACT(S) OWED*. `--answered` hands FM-030 to the seat: *act on it, then \`--clear-ask FM-030 <next move>\`* |
| 6 | `--check`, `--session-check` | ✓ Both exit 0. `--check`: *INDEX.md is up to date — 39 trackers*; *the Owner's two sections: guarded … none changes them or his signers file* |
| 7 | The tool | ✓ `git diff origin/main 920970b` touches only FM-030 and INDEX.md. `shoalmark.py` and both suites are byte-identical to `main`, and `VERSION` reads 0.18.5. **No suite was run**: nothing they test changed |
| 8 | merge-tree against `origin/main` | ✓ Clean. The tree `6dae5b1` is the branch's own, so the merge is a fast-forward |

## What the board reads for the branch

- **`--queue`** does not list `answer/fm-030`. `pushed_branches` leaves out `answer/*` by its rule. The one branch it
  names as pushed without a pull request is `fm/030-the-done-dialog-shows-the-question` @ `5e6d816`, *conflict in
  FM-030* (R2 of the ask's first pass, the merger's). An `answer/*` branch reaches the queue only as a pull request,
  read by `answer_reading`.
- **His board** is rebuilt from `main`. Until his merge it still shows FM-030's ask with *accept* and *reject*. That is
  the case this answer rules, and its build is option 1's; nothing here asks to change it.

## Findings

**R1 · P3 forward · 95 % on the fact.** The commit subject is cut mid-token. It ends *an unmerged \`origin/answer/\**:
the closing backtick is lost, and there is no ellipsis.
- *Where it comes from:* the pinned tool's `answer[:60]`, reproduced in check 3.
- *Already recorded:* FM-030's ship-log row of 2026-09-24 (*a subject is cut between words, with an ellipsis, or not at
  all*), a line under the freeze for 0.18.4, still open in 0.18.5.
- The signed `answer:` line is whole, and nothing here asks to change the commit.

## Verdict

**READY WITH FINDINGS** — R1, P3, forward, already recorded; nothing blocks.
- The answer is his, signed and verified by the one key in `main`'s signers file and by the forge.
- The diff is exactly the pinned 0.18.5 `answer_cmd`'s output.
- The text is the proposal, option 1, byte for byte.

*The Owner lands this by merging; a merge rules nothing.*
