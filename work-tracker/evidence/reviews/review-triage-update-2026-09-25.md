# Review — the Owner's TRIAGE.md update, at fe36cc0 (2026-09-25 11:37 CEST, Reviewer, session `8e509911/reviewer-10`)

**Scope.** PR 71, `docs/triage-update`: one commit, `fe36cc0` (`fe36cc08fbe9475774f16223b5b1cb247fff4153`), on
`ea630c1` (PR 69's merge). `origin/main` has moved since, to `c3cd54c` (PR 70) and then `8b4230e` (PR 72).
**Tier: docs, one pass.** `git diff --name-only origin/main...HEAD` names `work-tracker/INDEX.md` and
`work-tracker/TRIAGE.md`. There is no `shoalmark.py`, no test, no configuration, no hook and no front-matter key. Under
line 3 as this commit writes it, a review of the Owner's own TRIAGE lines reports and never blocks, so this verdict
reports. Verified, not ruled (path 5).

## What I ran

| run | result |
|---|---|
| `git show -s --format='%G? %GK %GS' fe36cc0` | `G SHA256:uNcUULP20UyJ7Iyv3xImxOrg9cXTcRqIxbWsekBYzCQ holgoijo@gmail.com`; the same against this worktree's committed `work-tracker/allowed_signers` (a `GIT_CONFIG_*` override) |
| `git show --stat fe36cc0` | `TRIAGE.md` 8 lines added and 8 removed; `INDEX.md` 5 added and 4 removed; nothing else |
| sha256 of TRIAGE.md from `## Passes` to the end, at `ea630c1`, `fe36cc0` and `origin/main` | identical, `ec7b2887…` |
| `python3 shoalmark.py --check` | exit 0; *INDEX.md is up to date — 34 trackers*; *filing freeze: 18 open* |
| `python3 shoalmark.py --session-check` | exit 0: the commit carries no `Session:`, and the Owner's seat is exempt |
| `--check` with the signers file pointed at a missing path (control) | exit 4, naming the four open answers' commits: the gate reads answer signatures. No gate reads the signature of a TRIAGE.md commit |
| `python3 shoalmark.py` | exit 0; `git status --short` empty |
| `--triage` in a scratchpad clone at `fe36cc0` | exit 0; *0 trackers to judge*; prints the three intent lines and the six path lines; tree clean |
| the same, with the path cut to a bare `1.` (control) | exit 4: *names no current path — tiers cannot be judged* |
| `git merge-tree --write-tree origin/main HEAD` | exit 0 (`42c3c48`); against `c3cd54c` also exit 0. The six paths main changed since the fork (both `index.md` pages, FM-006, FM-007, two reviews) do not overlap this branch's two |
| the merge with `8b4230e` replayed in the clone, then `--check` and `python3 shoalmark.py` | exit 0; INDEX up to date; tree clean |
| `test_shoalmark.py`, `test_core.py` | exit 0, 355 ok and 148 ok, on Python 3.14.3 and 3.9.6 |
| `python3 shoalmark.py --queue`, 11:34 | `PR 71  wait: no verdict on fe36cc0` (R2) |

## The checks

**1. The commit — his, signed; confidence 99%.**
- Author and committer `holgo99 <holgoijo@gmail.com>`: authored 10:37:13, committed 11:14:26 +0200. One parent,
  `ea630c1`, and no trailers.
- The key is the one `allowed_signers` trusts for his address, the same key that signed his answers. It is
  `ssh-ed25519`, a file key, not an `sk-` hardware key.
- **Outside TRIAGE.md:** `work-tracker/INDEX.md`. The change is its path section, reprinted word for word from
  TRIAGE.md. It is the generator's output: `python3 shoalmark.py` at the tip leaves it unchanged, and `--check` says
  it is up to date. Nothing else changed.

**2. The diff — the intent and the path in one hunk, *Passes* untouched; confidence 99%.**

The intent: all three lines are reworded, and none is added or removed. The two blank lines before *The current path*
are now one.
- **for**: adds *, their strength stated,* after *the signed decisions*.
- **so that**: *any release can be trusted.* → *any release can be trusted, at the least of their time the evidence
  allows.*
- **never**:
  - adds *a seat able to block the Owner's signed word;* as its second item;
  - *a merge without an independent party's review* → *a merge without a review by a party other than its author*;
  - *a failed intent because it was misunderstood* → *a failed intent because a potential misunderstanding was newer
    questioned*;
  - *leak sensible-data, non-redacted into records;* → *leak sensitive data, unredacted, into the record*.

The path: lines 1, 2, 3 and 5 are reworded, line 4 is unchanged, and line 6 is new. None is removed.
- **1.** *… and no failed run.* → *… and no failed command in the sitting.*
- **2.** *What a sitting finds is filed that day and fixed when it is small and ready; the rest is tracked.* → *What a
  sitting finds is filed that day, as a tracker or, under the freeze, as a line in the closest one; fixed when small
  and judged ready.*
- **3.** *A pull request without an independent review's evidence file cannot merge - checked, not asked.* → *A pull
  request merges only with a review's evidence file on its head: a Reviewer from another independent session for
  critical changes (critical = a release, the gate or hooks, signing and rights, TRIAGE.md or AGENTS.md rules changed
  by a seat, anything tagged security or P1); inline Reviewer passes on other code; one Reviewer pass for
  documentation; a review of the Owner's own answers and TRIAGE lines reports and never blocks, until FM-007's
  hardware key signs them. The Owner merges on a ready line, or over any other verdict with a signed reason.*
- **5.** adds *, the Owner's signed mandate,* after *An answer*.
- **6.** new: *What the Owner owes is on his board with one button; nothing owed to him lives only in a ledger, a
  tracker body or a chat.*

*Passes* is byte for byte the same at `ea630c1`, `fe36cc0` and `origin/main`, and so is the header above *The intent*.
No seat's paragraph is touched.

**3. Consequences, read against the record; confidence 85%.**

Fulfilled:
- **FM-032's answer is written into path 3.** The answer (`97fa87a`, 09-24 21:32:35) reads *one Reviewer docs pass
  until FM-007's hardware key signs your answers, the signature alone after — written into path 3*. Line 3 is the
  exception for answer pull requests that the answer owed. FM-030's raise of today named it as one of two acts owed
  to him with no button. He writes it with three changes, all his:
  - the pass *reports and never blocks*, where a docs pass under FM-032 S1 sends a P2 back;
  - it covers his TRIAGE lines as well as his answers;
  - *the signature alone after* is not restated (R3).

  Once this is merged the ask is acted on, and the seat that owns FM-032 clears it.
- **FM-032 S4 (the freeze) and FM-033's first answer are now on the path, in line 2.** FM-033's answer (`65f37a4`) is
  *a pass judges before the first build commit*; line 2 has *under the freeze, as a line in the closest one* and
  *judged ready*. AGENTS.md's freeze also allows *or waits*. For what a sitting finds, line 2's *filed that day*
  narrows that. A product defect is still filed as a tracker under the freeze (`--new --tags bug`), which line 2's *as
  a tracker or* admits.
- **FM-024's answer is generalised.** The answer (`64f843e`) is *a cold Reviewer session you start reviews 0.18.3*.
  Under line 3 every release, and every change tagged security or P1, needs a Reviewer from another independent
  session. PR 65's verdict (`e3aa64e`, session `01a0d6e7`) is one.
- **FM-030 is now line 6, nearly word for word.** Its P1 reason of today cites line 1's sitting and line 5. Line 1
  now says *no failed command in the sitting*, so line 6 is its direct anchor. Line 6 states a target, as line 1
  does. That FM-007's owed act, the key, still has no button on his board is FM-030's defect, P1 #3, not a
  contradiction in the line.
- **FM-031's one channel and rules 2 and 3 of the nine** are strengthened by line 6 (*nothing … only in … a chat*) and
  kept by line 5.
- **The *never* line's new item**, *a seat able to block the Owner's signed word*, matches two phrases of line 3:
  *reports and never blocks* and *over any other verdict with a signed reason*. FM-033's gate refuses a seat's build
  commit, not his word, and a pass that finds work not ready asks him again. So there is no conflict.

Superseded: his later signed word governs, and there is no contradiction in his text.
- **FM-032 S1's two tiers, as AGENTS.md records them.** There are now three: critical changes (another independent
  session), other code (inline passes) and documentation (one pass). On top come his own lines (a report) and his
  override (R1).
- **FM-024 slice 2.** Its #8 reason (09-24) is *the refusal of a same-session verdict, … the Owner's path line 3*.
  Line 3 now accepts inline passes on non-critical code and on documentation, so a refusal fits only the critical
  tier. The next pass re-judges it.
- **The *never*'s *an independent party's review*** becomes *a party other than its author*. The count of *same
  session* verdicts in `--check` stays a report.

For the next pass, not this review: every `tier:` in the tree was judged against the old five lines. FM-007 is now
named by line 3, since its key ends the interim. FM-033's gate enforces line 2's *judged ready*. FM-030 sits on
line 6.

Path 5 as applied this week holds: every answer was a signed `--answer` commit. The new words make the answer the
mandate, which the intent's *so that* promises each seat. His signed TRIAGE lines are not written through the board.
Line 3 and the *never* line still treat them, with his answers, as his signed word.

The landing page (PR 72) chose *your signed word*, not *mandate*, as the GtM seat's decision for a public page. Line
5's *signed mandate* is his own word in his own path. They do not conflict.

**4. Gates — true; confidence 99%.** See the table: `--check` and `--session-check` exit 0; `--triage` reads the
current path and still refuses a bare `1.`; the generator leaves the tree clean; merge-tree is clean; both suites are
green on two Pythons.

**5. Names and other repositories — clean; confidence 95%.**
- The new text names no person but the Owner and no repository but this one (*FM-007*). It gives no other
  repository's state: *a ledger* is generic.
- The commit subject names *Consigliere*. The record holds that word nowhere, and `[seats]` does not list it. The
  name is outside the TRIAGE text. The change's authority is his signature, not the parley (rules 2, 3 and 6 of the
  nine).

## Findings

**R1 · P3 · confidence high (95%) on the fact, 85% on the grade · AGENTS.md and the tool's printed rules trail line 3.**
- AGENTS.md's *Two tiers of review* has no critical tier, and says of every docs change *a P2 or above sends it
  back*. Line 3 now makes a review of his own answers and TRIAGE lines a report, and lets him merge over any verdict
  with a signed reason.
- In `TRIAGE_RULES`, the move `review` says *an independent review is owed first*. Line 3 wants one only for critical
  changes.
- Step 4 says *The Owner rules by merging the pull request*. Path 5, before and after this commit, says a merge is no
  answer. Line 3 now puts the ruling in the signed reason.
- Line 3 is his later signed word and governs.
- **Fix forward:**
  - A seat rewrites the AGENTS.md bullet from line 3. That is itself a critical change (*AGENTS.md rules changed by a
    seat*), so its Reviewer comes from another independent session.
  - The tool's two phrases go as one line under the freeze in FM-032, the closest tracker.

**R2 · P3 · confidence 99% on the fact, 80% on the grade · `--queue` reads his TRIAGE-lines pull request by a verdict.**
- At 11:34 it printed `PR 71  wait: no verdict on fe36cc0`. After a NOT READY it would print `wait: NOT READY`.
- An `answer/*` pull request reads `merge: your answer` on his signature (`answer_reading`). A pull request of his own
  signed TRIAGE lines instead waits on a review that line 3 says never blocks.
- `--queue` has no reading either for *over any other verdict with a signed reason*, and line 3 does not name where
  that reason is written.
- It is a view and refuses nothing.
- **Fix forward:** a line under the freeze in FM-031, whose S2 is `--queue`.

**R3 · P3 · confidence 70% that the reading is open · Line 3 bounds the interim, not what follows it.**
- The line says *… reports and never blocks, until FM-007's hardware key signs them*. FM-032's answer ruled *the
  signature alone after*.
- Read alone, the clause lapses when the key comes. His answers, and now his TRIAGE lines, then fall under *one
  Reviewer pass for documentation*. Read with the answer, the signature is enough on its own.
- Nothing turns on it before the key. His FM-007 answer (`1034602`) puts the key after the 09-29 scoring, once it
  is delivered.
- This is his to settle, and no seat picks a reading: his *never* now says *a potential misunderstanding …
  questioned*.

**R4 · P3 · confidence 70% that the reading is open · Line 6's *owed to him*.**
- Line 6 says *What the Owner owes is on his board with one button; nothing owed to him lives only in a ledger, a
  tracker body or a chat.*
- The second clause may repeat the first from the other side: what is owed **by** him. It may instead be a wider
  rule: what a seat owes him (a report, a verdict, an answer to his question) must be on his board too.
- The two readings lead to different builds under FM-030. This is his to settle, through the board, as line 6 itself
  asks.

**His wording, not findings:** *newer questioned* reads as *never questioned*, and the *never* line ends on a
trailing space with no full stop. Nothing reads either one, and no seat edits them.

## Verdict — READY WITH FINDINGS (P3), 85%

**READY WITH FINDINGS.** There is no P2. Where a line departs from a rule he signed, this signed commit supersedes
that rule; no line contradicts one. No seat's paragraph is touched. R1 and R2 are fixed forward by seats; R3 and R4
are his to settle.

Not verifiable here:
- Who holds the key: a signature proves the key, not the hand. The key is a file key.
- That the hook, not a hand, wrote INDEX.md. Its content is the generator's.
- What *Consigliere* is. The parley is not in the record.

**Independence.** I am a sub-agent of session `8e509911`, the Principal that set FM-032's ask and wrote today's pass.
The commit is the Owner's and carries no `Session:`, so `--check` will count this verdict *untraced*.

*the Owner lands his own change by merging; a merge rules nothing — the ruling is his signed commit.*
