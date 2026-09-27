# Review — FM-024's exchange cleared, at 392eb74

**Date:** 2026-09-27 14:44 CEST · **Seat:** Reviewer (Opus 5.5) · **Session:** `8e509911/reviewer-36` · **Worktree:**
`shoalmark-review-2`, detached at the tip.
- I ran the reproduction, `--answered`, `--owner` and the board in scratch clones in the session's scratchpad, with no
  remote.
- The Owner's checkout, `shoalmark-gtm`, every other worktree and every folder of session `8b91dba2` stayed outside
  every command.

**Tier:** docs, one pass.
**Independence:** same session. The commit is the Principal's (`Session: 8e509911`), and this seat is its sub-agent.

**Reviewed:** `fm/024-the-act-done-the-exchange-cleared` at `392eb74eb91d0b95ca2dabfb46f12877cf11949d`. It is one
commit on `origin/main` `62b4a05`, which is PR 99, his act `f8246fa`, merged 14:34:18.

## The checks

| # | Check | Result |
|---|-------|--------|
| 1 | Scope | ✓ One path changes: FM-024's tracker. No `.py` file, so no suite runs: the tool is `main`'s. INDEX.md is unchanged; regenerated in scratch after the clear, it is byte-identical to `main`'s |
| 2 | The diff is exactly what the tool at `main` writes | ✓ In a scratch clone at `62b4a05`, `python3 shoalmark.py --clear-ask FM-024 build` makes FM-024 **byte-identical** to `392eb74`'s. The ask's eight keys leave the front matter; `next: build` and `done:` stay; a `## Asks` block is added after `## Acts` |
| 3 | The relation and the signed line | ✓ His answer commit `64f843e` (2026-09-24 21:27:24): `%G?` is `G`, by `SHA256:uNcUULP20UyJ7Iyv3xImxOrg9cXTcRqIxbWsekBYzCQ`, the one key in `main`'s signers file. The block reads *signed — 64f843e · G*. His answer, *accepted - a cold Reviewer session you start reviews 0.18.3*, is the proposal byte for byte, so the relation is *accepted the proposal* ✓ |
| 4 | `--answered` | ✓ At `main`: *5 ANSWERED, NOT YET ACTED ON*, FM-024 among them with *→ act on it, then … --clear-ask*. At the tip: 4, without FM-024. FM-024 now stands under *ACTED ON SINCE THE LAST STANDUP*: *acted on in `392eb74` · accepted the proposal* |
| 5 | `--owner` | ✓ Neither `main` nor the tip names FM-024: no ask and no act (*NO QUESTION FOR THE OWNER · 3 ACT(S) OWED*). The act left with PR 99 |
| 6 | The board | ✓ Rendered in Chrome, FM-024's tracker view shows *Acts*, *Asks* and *Ship log* as headings. The exchange is one block: question, *answered*, *relation* and *signed* |
| 7 | Gates | ✓ `--check` exit 0: *INDEX.md is up to date — 39 trackers*; *the Owner's two sections: guarded*. `--session-check` exit 0. `git merge-tree --write-tree origin/main HEAD` is clean, and its tree `946aacf` is the tip's own |

**Noted, not a finding.** The commit body says *the cold session 01a0e147/01a0d6e7 reviewed 0.18.3*. Session
`01a0d6e7` reviewed 0.18.3 (`e3aa64e`); `01a0e147` reviewed the 0.18.5 cut (`27072ef7`). The tracker carries no such
line — its text is the tool's.

## Verdict

**READY.** The diff is the tool's `--clear-ask FM-024 build`, byte for byte. The relation and the signed line are his
answer's. `--answered` counts it as acted on. His lists hold nothing for FM-024. The branch is tracker-only.

*The Owner lands this by merging; a merge rules nothing.*
