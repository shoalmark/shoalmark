---
id: FM-019
status: In Progress
considered: FM-014, FM-008, FM-007, FM-017
tags: bug
next: review
hook: "On a clean tree the rights gate judges HEAD against HEAD~1. For a merge commit that is everything the pull request carried — every answer, close and verdict in it — attributed to whoever merged. The forge's merge identity is no seat, and GitHub signs merges with its own key, so `--check` on a trunk goes red on every merge that carries a status change; shoalmark's own `main` is red this way at 0.17.3."
---

# FM-019 — A merge commit is judged as the merger's own change, and main's --check goes red on every merge

## What is true now

**Built 2026-09-23 on `fix/0.17.4-the-answer-says-what-it-does`; merged 2026-09-23 (#12), released as 0.17.4.** It blocked
the 0.17.4 tag. Found while building FM-014 (a line there) and reproduced by the Principal on a local no-ff merge of a
branch carrying three signed answers and a close: 0.17.3 and the first 0.17.4 build both exit 4, naming the forge's
merge identity as the author of every answer and the close.

**A merge is now two kinds of change, and neither is the merger's alone** (`changes_under_review()`):

1. **Each commit it brings** — every non-merge commit reachable from it and not from its first parent, read in one
   `git log` — judged against its own parent, under its own author and its own signature, with the same rights logic a
   single commit gets. A commit made without the hook (`--no-verify`, a clone with no hook installed, the forge's
   editor) was never judged, so a merge is not assumed to have laundered it; a refusal names *that* commit.
2. **Its own change** — the tracker files where the result differs from **every** parent (a conflict resolved, an edit
   made in the merge), and only a transition it makes against every parent — judged under the merger. A clean merge
   adds nothing of its own.

The same holds for a merge being committed now — HEAD and `MERGE_HEAD` are its parents: in the pre-commit run, in the
line reader (an answer the merge brings in no longer reads as *not committed yet*), and in the record rule (a merge
loses an answer only if every parent had it). The commits a merge brings are read only when there is a merge.

| check | result |
|---|---|
| (a) a clean merge by a non-seat of a branch carrying an answer, a close and a triage verdict | no rights problem |
| (b) a conflict resolution that closes a tracker, merged by the implementer | refused as its `close`, pre-commit and `--check`; by the principal, passes; the answer the branch brought is not attributed |
| (e) a merge bringing an unsigned answer under the signed owner's identity | refused, naming that commit, not the merge |
| (f) a merge bringing a close made by a seat without `close` | refused, naming that commit and its seat |
| a merge bringing 20 commits | `--check` 1.62 s, in the suite |
| (d) shoalmark's own `origin/main` at `f0fa261`, the forge's merge of `answer/fm-007` (signers file configured as in the Owner's checkout) | 0.17.3: exit 4 · now: exit 0, 0.92 s — the two answer commits it brings are the owner's, signed, and verify |

Two mutation witnesses: reading the first parent alone fails (a), (b), (e), (f); not reading the brought commits fails
(e) and (f). The FM-014 and FM-017 checks pass unchanged. **What is left:** nothing.

## Why

Merging a pull request with a merge commit is the only method that keeps the Owner's signed answer commits — a rebase or
a squash re-creates them unsigned. A gate that goes red on every such merge is a gate the trunk learns to ignore; and a
fix that simply stopped reading the merge would let an unjudged commit ride in under it.

## Done when

- A merge commit is judged by its own changes under the merger, and every commit it brings under its own author and
  signature; a clean merge of judged work passes.
- The same rule wherever the gate reads the change at HEAD — the pre-commit run of a merge, the line reader, the
  record rule.
- Checks (a), (b), (e), (f) in the suite; FM-014 and FM-017 unchanged; `--check` passes on shoalmark's own `origin/main`.

## Ship log

| Date | Event |
|---|---|
| 2026-09-23 | Merged (#12), released as 0.17.4. |
| 2026-09-23 | Filed and built: a merge judged by its own change, each commit it brings by its own author; six checks; `origin/main` passes `--check`. |
