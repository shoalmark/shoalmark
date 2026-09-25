# Review — the answer to FM-007, at 1034602 (2026-09-25 07:35 CEST, Reviewer, session `8e509911/reviewer-4`)

**Scope.** `answer/fm-007`: one commit, `1034602`, on `main` `1fe880a`. Docs tier, one pass (path 3, under his FM-032
answer). Verified, not ruled (path 5).

## The five checks

1. **The commit — true, 99%.** Author and committer `holgo99 <holgoijo@gmail.com>`, 07:29:54 +0200; one parent,
   `1fe880a`. `%G? %GK %GS`: `G SHA256:uNcUULP20UyJ7Iyv3xImxOrg9cXTcRqIxbWsekBYzCQ holgoijo@gmail.com`, the key
   `work-tracker/allowed_signers` trusts for that address (the branch does not touch it).
   Subject: `FM-007: accepted - after the scoring, once the key is delivered.`, which is 55 characters, so it is not
   cut.
2. **The diff — true, 99%.** Against `1fe880a`: one file, `work-tracker/FM-007-a-signature-proves-the-key-not-the-hand-an-agent-running-as.md`,
   3 lines added and none removed, under `ask-proposal:`: `answer: "accepted - after the scoring, once the key is
   delivered."`, `answered: 2026-09-25`, `answered-by: holgo99`. `next: owner` stands. No body line.
3. **The text — changed text, and a valid answer; 85%.**
   - After `answer_norm` the text is neither the proposal nor any of the three options. `--answered` prints
     *FM-007 · answered 2026-09-25 by holgo99 … relation: accepted with a change*.
   - **It answers the question.** The ask wants to know when the software key stops signing his answers. He answers
     with a condition, not a day: after the week's scoring on 09-29 (the only scoring the ask names), and only once
     the key is delivered.
   - All three options fall before 09-29, and the text declines each of them. It also says why no day can be named:
     the key is not in his hands yet.
   - This is what a changed-text answer is for. A `rejected` would have asked for the ask to be reworded, and this
     text needs no rewording to act on.
   - The 15% is the strict reading. *Which day* gets no day, and the day waits on the delivery.
4. **The gates — true, 99%.** `--check` exits 0 and `--session-check` exits 0. The signers file is configured, by
   the repository's shared config. Against this worktree's committed copy `--check` still exits 0. Against a missing
   file it exits 4, naming `1034602c96` twice (the answer's author, and the `answer` change), which shows the gate
   reads the signature.
5. **merge-tree — true, 99%.** `origin/main` with `1034602` gives `85a88ea`, the branch's own tree: a clean
   fast-forward.

## Verdict — READY, 90%

No finding. **Not verifiable here:** who holds the key. A signature proves the key, not the hand.

**For the seat that acts on it** (not a finding):
- *Accepted with a change* is the tool's word for text outside the options. In substance, this change moves the act
  past the week.
- The software key keeps signing his answers through the scoring of 09-29, and after it until delivery.
- FM-032's interim therefore stands that long: one Reviewer docs pass for each answer pull request.

**Independence.** I am a sub-agent of session `8e509911`, which set this ask (`3e0893b`). The answer is his.

*the Owner lands his answer by merging; a merge rules nothing (path 5) — the answer is the signed commit.*
