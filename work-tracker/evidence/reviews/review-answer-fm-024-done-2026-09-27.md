# Review — the Owner's act on FM-024, `--done`, at f8246fa

**Date:** 2026-09-27 13:59 CEST · **Seat:** Reviewer (Opus 5.5) · **Session:** `8e509911/reviewer-36` · **Worktree:**
`shoalmark-review-2`, detached at the tip. I made the reproductions, `--owner` and `--standup` in scratch clones in the
session's scratchpad, with no remote. The Owner's checkout, `shoalmark-gtm`, every other worktree and every folder of
session `8b91dba2` stayed outside every command.
· **Tier:** docs, one pass. This is path 3 under his FM-032 answer, because FM-007's hardware key has not signed this
act. A review of the Owner's own change reports and never blocks.
**Independence:** same session. I am a sub-agent of Principal session `8e509911`. The act is his.

**Reviewed:** `answer/fm-024` at `f8246faedd98147df9296cdf01eb844c65f9ae01`. It is one commit on `origin/main`
`28e54bf21403798f51a25fa7af4f220ac247604c`. The tool deleted the earlier `answer/fm-024`, which was merged (PR 63; its
answer `64f843e` is on `main`), and cut a fresh branch from `main`. The push was a fast-forward of the remote branch. No
pull request is open for it yet.

## The checks

| # | Check | Result |
|---|-------|--------|
| 1 | The commit is his | ✓ Author and committer are `holgo99`, 2026-09-27 13:44:51 +0200, and the forge names `holgo99` as both. One parent, `28e54bf`, the tip of `origin/main`. The subject is `FM-024: done — work-tracker/evidence/reviews/review-fm-029-0-18-3`, the tool's own: `done_cmd` cuts the path at 50 characters |
| 2 | Signed, and verified against the signers file | ✓ With `origin/main:work-tracker/allowed_signers` as the signers file: `%G?` is `G`, the key is `SHA256:uNcUULP20UyJ7Iyv3xImxOrg9cXTcRqIxbWsekBYzCQ`, and the trust is `fully` — the one ed25519 key in that file. The forge's `verification` reads `verified: true`, reason `valid` |
| 3 | The diff is exactly what the pinned 0.18.5 `done_cmd` writes | ✓ 2 files. FM-024: `next: owner` → `build`; `done: "2026-09-27T13:44:37+02:00 · work-tracker/evidence/reviews/review-fm-029-0-18-3-fourth-pass.md"` after `answered-by:`; a new `## Acts` with the record line `**2026-09-27** · done — <path> · <the ask's question> · holgo99`. INDEX.md: FM-024's ranked row reads `build`, and its row leaves *Acts owed to the Owner*. **Reproduced byte for byte.** I ran `done_cmd` itself from `main`'s `shoalmark.py` in a scratch clone at `28e54bf`, with the clock fixed to 13:44:37 +02:00 and `owner_change` replaced by a stub that applies its `write` as `owner_change` does (no branch, no signature, no push). Then `--print-written` ran. FM-024 and INDEX.md are byte-identical to `f8246fa`'s, and the subject is the same |
| 4 | The path he gave | ✓ `work-tracker/evidence/reviews/review-fm-029-0-18-3-fourth-pass.md` exists at `f8246fa`. **The record's facts, gathered here because his input was the path alone** (his rule of 13:5x: the person gives the path, the record gathers the facts): it is the cold Reviewer session `01a0d6e7`'s verdict **READY** on 0.18.3 at `8c3c10b` (PR 65). Its commit is `e3aa64e`, 2026-09-25 10:29:27 +0200, *review: 0.18.3 at 8c3c10b — READY (0 findings)*, with trailers `Reviewed: 8c3c10b…`, `Session: 01a0d6e7`, `Worktree: shoalmark-review-cold`. `8c3c10b` is in `v0.18.3`. This is the act his accepted answer promised: *a cold Reviewer session you start reviews 0.18.3* |
| 5 | The act leaves his lists | ✓ At `28e54bf`, `--owner` reads *4 ACT(S) OWED* and `--standup` reads *4 act(s)*, each listing FM-024. At `f8246fa` they read 3, and FM-024 is in neither. Rendered in Chrome, the board's tracker view shows *Acts* and *Ship log* as headings, with the record line its own paragraph |
| 6 | `--check`, `--session-check` | ✓ Both exit 0. `--check`: *INDEX.md is up to date — 39 trackers*; *the Owner's two sections: guarded … none changes them or his signers file* |
| 7 | Both suites, once per interpreter at load under 6 | ✓ `test_shoalmark.py` 481 and `test_core.py` 148, green on 3.14.3 (14:04–14:13, starting at load 1.8) and 3.9.6 (14:13–14:21, starting at load 5.1), 0 skipped, exit 0. The tool is byte-identical to `main` and to `v0.18.5`: `git diff 28e54bf f8246fa` touches only FM-024 and INDEX.md, and `shoalmark.py` at `28e54bf` equals `b15c6d9`'s |
| 8 | merge-tree against `origin/main` | ✓ Clean. The tree `d3a743f` is the branch's own, so the merge is a fast-forward |

## Findings

**R1 · P3 forward · 95 % on the fact.** The act's record line reads the ask's question, not what he did:
- *The line:* *done — … · Who verifies 0.18.3 — a cold Reviewer session you start, this session's own sub-agent, or
  nobody until FM-024's slice 2 refuses a same-session verdict? · holgo99*.
- *What the act was:* his accepted option, *a cold Reviewer session you start reviews 0.18.3*. A reader of `## Acts`
  sees three options and no answer.
- *Where it comes from:* `done_cmd` records `act[0]`, the question. The *Done — where is the result?* dialog shows the
  same question.
- *Already filed:* this is his word of 13:35:40, filed as FM-030's raise on `fm/030-the-done-dialog-shows-the-question`
  (`5e6d816`, not merged), with the fix a build under FM-030 (P1 #2 `build`).
- The record is the tool's pinned output, and nothing here asks to change it by hand.

## Verdict

**READY WITH FINDINGS** — R1, P3, forward, already filed; nothing blocks.
- The act is his, signed and verified by the one key in the signers file.
- The diff is exactly the pinned 0.18.5 `done_cmd`'s output.
- The path he gave is the cold session's READY on 0.18.3.
- The act has left his lists.

*The Owner lands this by merging; a merge rules nothing.*
