# Review — the Owner's answer to FM-006, at 8defe63

**Date:** 2026-09-26 14:17 CEST · **Seat:** Reviewer · **Session:** `8e509911/reviewer-30` · **Worktree:** `shoalmark-impl`
· **Tier:** docs, one pass. This is path 3 under his FM-032 answer, because FM-007's hardware key has not signed this
answer. A review of the Owner's own answer reports and never blocks.
**Independence:** same session. I am a sub-agent of Principal session `8e509911`, whose `8e509911/implementer-24` set this ask's
options and proposal (`fd7b4a6`). The answer is his.

**Reviewed:** `answer/fm-006` (PR 91) at `8defe63ac7533813c848dab397dd4708fc50913b`. It is one commit on `origin/main`
`86b78e355cb7c30e775545c124428afa5e68dd8b`.

## The checks

| # | Check | Result |
|---|-------|--------|
| 1 | The commit is his | ✓ Author and committer are `holgo99 <holgoijo@gmail.com>`, 2026-09-26 13:55:58 +0200. It has one parent, `86b78e3`, the tip of `origin/main`. On the forge, PR 91 has head `8defe63`, base `main`, one commit, author `holgo99`, and is open and not a draft. |
| 2 | Signed, and verified against the signers file | ✓ `%G? %GS %GK %GT`: `G holgoijo@gmail.com SHA256:uNcUULP20UyJ7Iyv3xImxOrg9cXTcRqIxbWsekBYzCQ fully`. It verifies against `origin/main:work-tracker/allowed_signers`, the default branch's file that the gate trusts (FM-037). That file is `[seats]`'s `owner = "holgoijo@gmail.com signed"`, one `ssh-ed25519` line, and the branch does not touch it. Negative control: with a missing signers file, `--check` exits 4 and names `FM-006 8defe63ac7`. The key is a file key, not an `sk-` key, so under his FM-032 answer this docs pass is still owed. |
| 3 | The diff is `--answer`'s and nothing else | ✓ 2 files, +4 −0. FM-006 gains three lines under `ask-proposal:`: `answer:`, `answered: 2026-09-26` and `answered-by: holgo99`. `next: owner` stands, because for an `action` the move stays `owner` (`ANSWER_MOVE`, `shoalmark.py:290`). There is no `due:`: `--answer` writes three lines only (`:1557`). `INDEX.md` gains one row in the acts table. The pre-commit `tracker-index` regeneration (`lefthook.yml`) writes that row, not a hand. The diff has no body line and does not touch `TRIAGE.md`, `shoalmark.toml` or the signers file. The subject, `FM-006: ` plus the first 60 characters of the answer, is exactly the form `--answer` writes (`:1568`). |
| 4 | The text is the first option and the proposal | ✓ `answer:` is `accepted - ` followed by the proposal, byte for byte (121 bytes, the U+2014 included). It is also option 1 of 3, byte for byte. |
| 5 | The relation | ✓ `--answered`: *FM-006 · answered 2026-09-26 by holgo99 … answer: accepted - this repository, client names and the parent's traces public, the port evidence deleted — after the scoring, gates held · relation: accepted the proposal* |
| 6 | The board's acts list | ✓ `--owner` and `--standup` both list the act under *ACTS — yours, with their time*: `FM-006 — When and how does shoalmark go public? · no date yet · promised 2026-09-26: accepted - …`. For an act without `due:`, *no date yet* is FM-030 E's rule, sorted last (`acts_lines`, `:1078`). The only ask left for him is FM-002. |
| 7 | `--check`, `--session-check` | ✓ Both exit 0. `--check` prints *work-tracker/INDEX.md is up to date — 37 trackers*, so INDEX.md is **not** stale after the commit. It also prints *the Owner's two sections: guarded … none changes them or his signers file*. |
| 8 | Both suites, by hand (Python 3.14.3) | ✓ `test_shoalmark.py`: 462 ok, *skipped here: 0 checks*, all green, exit 0, 11 min 05 s. `test_core.py`: 148 ok, all green, exit 0. |
| 9 | merge-tree against `origin/main` | ✓ The merge gives `176e0f1`, the branch's own tree, so the merge is a fast-forward. It is also clean with PR 90 (`answer/fm-002` `4e00f85`), giving `8cb8675`. That merged tree's INDEX.md regenerates to itself: outside git, only the no-git lint block differs, as it does for `8defe63` alone. |

**For the record, not judged.** FM-006's *Going public* section holds the act's four gates:
- CI green on all three platforms;
- the signing tier stated, or the hardware key live;
- a clean gitleaks scan;
- the port evidence deleted or moved, as ruled on 09-22.

At the flip, shoalmark's home is the organisation `shoalmark` (PR 87).

## Findings

**R1 · P3 forward · 95%.** `--answered` tells a seat to clear this action before his act. On the branch it prints
*→ act on it, then `python3 shoalmark.py --clear-ask FM-006 <next move>`* (`:1064`). A seat that follows it drops the act
from his board. I checked this in a scratch copy of `8defe63`, made with `git archive` outside any repository: after
`--clear-ask FM-006 build`, `--owner` no longer lists FM-006 under ACTS. The act owes no `due:` yet, so nothing else
holds it (`act_of`, `:3473`). This is FM-030's open *Done when* line (*`--answered` stops sending an accepted action ask
to a seat*; *clearing it records the act*), already carried on TRIAGE.md's 2026-09-26 pass. Nothing new to file. For the
seat: do not `--clear-ask FM-006` until the act is recorded.

**R2 · P3 · 99%.** The commit subject and PR 91's title stop mid-word at *…the parent's tr*. The cause is `--answer`'s
`answer[:60]` (`:1568`). The signed `answer:` line carries the whole text. FM-030's ship-log line of 2026-09-24
already carries this, and 0.18.4 does not fix it. It is a defect in the answer's form. It is reported and never
blocks.

**Not verifiable here:** who holds the key, since a signature proves the key and not the hand. Also, whether `--answer`
made the commit rather than a hand, although its shape is exactly what `--answer` writes.

## Verdict — READY WITH FINDINGS, 95%

The answer is his and signed, and it verifies against the default branch's signers file. It is the proposal and
option 1, byte for byte, and the tool computes *accepted the proposal*. The act stands on his board with no date yet.
The gate, the session check, both suites and the merge are green. Both findings are the tool's, not the answer's.

*The Owner lands this by merging, and a merge rules nothing (path 5).*
