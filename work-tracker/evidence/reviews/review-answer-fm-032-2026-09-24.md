# Review — the answer to FM-032, at 97fa87a (2026-09-24 21:45 CEST, Reviewer, session `8e509911/reviewer-4`)

**Scope.** `answer/fm-032`: one commit, `97fa87a`, on `main` `8cb389d`. Docs tier, one pass: path 3 as this answer
itself words it, since FM-007's hardware key has not signed it. Verified, not ruled (path 5).

## The five checks

1. **The commit — true, 99%.** Author and committer `holgo99 <holgoijo@gmail.com>`, 21:32:35 +0200; one parent,
   `8cb389d`. `%G? %GK %GS`: `G SHA256:uNcUULP20UyJ7Iyv3xImxOrg9cXTcRqIxbWsekBYzCQ holgoijo@gmail.com`, the key
   `work-tracker/allowed_signers` trusts for that address (unchanged since `216dd07`; the branch does not touch it).
   Subject: `FM-032: accepted - one Reviewer docs pass until FM-007's hardware ke`. It is cut at 60 characters of
   the answer, mid-word, by 0.18.2's `--answer` itself (`shoalmark.py:1335`, `answer[:60]`). The signed
   `answer:` line carries the whole text. This is an observation on the tool, not a finding on the answer.
2. **The diff — true, 99%.** Against `8cb389d`: one file, `work-tracker/FM-032-the-loop-costs-the-same-for-a-docs-row-as-for-a-migration.md`,
   3 lines added and none removed, under `ask-proposal:`: `answer: "accepted - one Reviewer docs pass until FM-007's
   hardware key signs your answers, the signature alone after — written into path 3"`, `answered: 2026-09-24`,
   `answered-by: holgo99`. `next: owner` stands. No body line.
3. **The text — true, 99%.** It is `accepted - ` plus the proposal, byte for byte (the `—` and the `'` included)
   before `answer_norm`, and equal after it. The proposal is option 1 of 3. `--answered` prints: *FM-032 · answered 2026-09-24 by holgo99 … relation: accepted the proposal*.
4. **The gates — true, 99%.** `--check` exits 0 and `--session-check` exits 0. The signers file is configured, by the
   repository's shared config, which names the Owner's checkout's `work-tracker/allowed_signers`. Against this
   worktree's committed copy (a `GIT_CONFIG_*` override) `--check` still exits 0. Against a missing file it exits 4,
   naming `97fa87a5d9`, which shows the gate reads the signature.
5. **merge-tree — true, 99%.** `origin/main` with `97fa87a` gives `f68d8c4`, the branch's own tree: a clean
   fast-forward. It is also clean with `answer/fm-024` and with `answer/fm-031`.

## Verdict — READY, 97%

No finding. **Not verifiable here:**
- Who holds the key. A signature proves the key, not the hand.
- That `--answer` made the commit, not a hand. Its shape, the 60-character subject included, is exactly what
  0.18.2's `--answer` writes.

The key is `ssh-ed25519`, a file key, not an `sk-` hardware key: by this answer's own terms, the pass is still owed.

**Independence.** I am a sub-agent of session `8e509911`, which set this ask (`a3ff174`). The answer is his.

*the Owner lands his answer by merging; a merge rules nothing (path 5) — the answer is the signed commit.*
