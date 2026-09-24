# Review — the raise at 0f0766e: FM-007 raised, FM-030 widened, FM-033's second ask (2026-09-24 18:17 CEST, Reviewer, session `8e509911/reviewer-1`)

**Scope.** `origin/main` `fcac7b6`…`0f0766e` (`0f0766ed3f65815c05e3a9c8a786da61f96406de`). Branch
`fm/033-a-raise-by-sourced-evidence` has one commit by the principal seat, under `8e509911`. It touches four files: FM-007,
FM-030, FM-033 and INDEX.
- **FM-007** gains a `## Raised` section and one ship-log row.
- **FM-030** gains one widening line and one ship-log row.
- **FM-033** has its answered exchange cleared with `--clear-ask FM-033 build`, a new ask set with `next: owner`, and
  a new `## Ship log`.

It is filed under the freeze: no new tracker, no command. Tier: docs, one pass. The ask exception applies: a defect in
the ask's text is P2.

**What I ran.**
- `shasum -a 256` on the Auditor's draft.
- A script that compares the raise line and the ask with the draft, after whitespace normalisation.
- A second script: `--clear-ask FM-033 build` run on a scratch copy of `fcac7b6`, compared with the tip.
- `ssh-keygen -lf` on `work-tracker/allowed_signers` and on the forge's published keys for holgo99; `%G?`/`%GF` on
  `65f37a4` and `7dd6ba6`.
- `--owner`, `--standup`, `--answered`, `--check`, `--session-check`, and `python3 shoalmark.py` twice.
- Both suites on Python 3.14.3, and `git merge-tree`.
- The parent project's ledger, read with the one `fetch` and `show` the brief allows. Its commit's time comes from the
  forge.

## Checked, and true

**The two hash-diffs against the draft.**
- ✓ The draft's hash begins `39690e54` (`39690e54ab3a198c…`), written 17:41.
- ✓ **The raise line.** The draft's text after *The raise line for FM-007:*, whitespace normalised to one line, equals
  FM-007's one `## Raised` item exactly (360 characters). The italic lead above it is the Principal's, and it names the
  draft by its hash.
- ✓ **The question.** `ask:` equals the draft's *"Does a sourced raise that names a signed rule it undermines trigger a
  same-day pass, as a now does?"*: 99 characters, one question, one `?`, at its end.
- ✓ **The options.** `ask-options:` is the draft's three options in order, each exact (104, 35 and 56 characters). None
  starts with *yes* or *no*.
- ✓ `ask-proposal` is option 1 word for word. `ask-kind: ruling`, `ask-since: 2026-09-24` and `next: owner`.

**The ledger row came first.**
- Its question equals `ask:` word for word. Its bold proposal is option 1, and its other two options are options 2 and
  3.
- On the forge its commit is 18:05:13 CEST, before this commit's 18:08:20.

**The clearing of FM-033's answered exchange is honest.**
- His answer (`65f37a4`, signed `G`, 16:29:09) was *a pass judges before the first build commit, the same day as a now,
  and a pass that finds it not ready asks you again*.
- The pass on FM-033 came 9 minutes later: `81dce10`, 16:38:28, *keep P2, next build*. `f4e7658` (17:38) ranked it #9.
  The Owner merged both in PR 56 (`fcac7b6`, 17:58:40), and TRIAGE.md's addendum records it.
- The pass kept FM-033, so the answer's *asks you again* is not owed.
- No commit on any ref names FM-033 outside `work-tracker/`, so nothing was built before the pass.
- The block is the tool's own output. On a scratch copy of `fcac7b6`, `--clear-ask FM-033 build` writes a body equal to
  the tip's body up to the new `## Ship log`, byte for byte.
- The front matter differs only by the new ask's five keys and `next: owner`, which replaces the `next: build` the
  clearing wrote.
- `## Ship log` is new, because the file had none, and its one row says what happened.

**FM-030's line.**
- It is marked as the Principal's (*the Principal's line on its proposal, item 3*) and names its occasion.
- Beyond the draft's item 3 (`--owner` and `--standup`), it names *the board*. FM-030 already reads the board as one of
  the person's lists (`:33`, `:69`), so this adds no scope.

**The sensitive-data question.** The raise line holds nothing the intent's *never* forbids.
- **The fingerprint is public.** `SHA256:uNcUULP20UyJ7Iyv3xImxOrg9cXTcRqIxbWsekBYzCQ` is derivable from
  `work-tracker/allowed_signers`, committed since `216dd07`. The forge publishes the same key as holgo99's public and
  signing key. `65f37a4` and `7dd6ba6` are signed by it (`%GF`).
- **The configuration is only option names.** `AddKeysToAgent` and `UseKeychain` are stock option names, and
  `ssh-add -l` is a command. There is no secret, no key material, no host and no path beyond `~/.ssh/config`.
- **What it does disclose** is a weakness: the key that signs his answers can be used through the agent without a
  prompt. FM-007 has stated that class since 09-22, and the repository is private. If the repository is ever
  published, FM-007 as a whole carries that decision, not this line alone.

**The board.** `--owner` prints *1 NEED THE OWNER*: FM-033 · ruling, with the new question, and nothing else. FM-007
stays under *ANSWERED, NOT YET ACTED ON*.

**Gates at `0f0766e`.**
- `python3 shoalmark.py` rewrites nothing, and `git status --porcelain` stays empty. `--check` 0, with the freeze at
  17 open. `--session-check` 0.
- `test_shoalmark.py` 0 (298 ok, all green); `test_core.py` 0 (148 ok, all green).
- `origin/main` moved after this commit to `da2228e` (PR 52, 18:12:18), so the merge is no longer a fast-forward.
  `git merge-tree --write-tree origin/main 0f0766e` is clean and writes `5ba477d`, with no conflicted path.
- PR 52 does not touch INDEX or these three trackers. Regenerating the merged tree in a scratch copy with no history
  changes only the ledger-integrity lines, and the same copy of `main` alone shows those lines too.
- The commit message carries no pull-request number with the sign.

**The commit message's claims.**
- ✓ The draft's hash, the line word for word, *the Principal's* line, the clearing after PR 56, the three options with
  the first proposed, and the ledger first at 18:05:13.
- **Not verified:** *a software key in the shared agent, used by every seat push*. Its sources are `ssh-add -l` and
  `~/.ssh/config`, outside git. I did not read them, because this session's permissions refused that read. The raise
  line stands as the Auditor's sourced claim.

**Independence.** Same session `8e509911`, reported, not refused.

## Findings

**R1 · P3 · high · A consumer's commit hash is in FM-033's ship log.**
- The row ends *the parent project's ledger rows came first (`<its hash>`, 18:05:13)*, giving that project's commit
  hash, quoted here without it. FM-032's R2 applied the Owner's rule that consumer state does not enter shoalmark, though numbers may, and
  the hash was taken out then.
- FM-007's new row similarly carries the parent's ledger vocabulary: *kind B, before the sitting of 09-25*.
- Fix: *the parent project's ledger rows came first (18:05:13)*, and drop *kind B*.

**R2 · P3 · medium · Options 2 and 3 differ by a rule that is only in the draft.**
- The difference between *every raise waits for the next pass* and *a raise re-ranks nothing; the pass reads it when it
  runs* is the draft's item 2: *a tracker raised after its `triaged:` date is re-judged first at the next pass*.
- That matters here. FM-007's judgement is from 09-23, so under option 3 no pass is obliged to re-judge it.
- The record does not say this. FM-033's body says nothing of a raise, FM-007's lead only defines the line, and the
  draft lives outside the repository.
- Not P2: the ask is the draft's own text, and the options can be told apart on a careful reading, since *waits for*
  queues the tracker and *re-ranks nothing* does not.
- Fix, before he answers: one paragraph in FM-033's *What is true now*, marked as the Principal's. It states items 1
  and 2 of the raise rule and what each option makes the next pass do.

**R3 · P3 · medium · FM-030's widening comes after its judgement.**
- FM-030 was judged on 2026-09-24 (P2 #6, build) in the pass PR 50 merged. The widened case, rulings whose act is the
  Owner's, came at 18:08.
- His FM-033 answer of 16:29 says a pass judges before the first build commit. The row says *nothing built*, but not
  that the widened line waits for a pass.
- Fix: the row says the widening is judged at the next pass before any build on it.

**R4 · P3 · high · His receipt for the FM-033 answer does not reach `--standup`.**
- `acted_on()` skips a tracker that carries an `ask:`. This one change both clears the exchange and sets a new ask.
- So `--standup` lists FM-033 only as a new ruling, and *ACTED ON SINCE THE LAST STANDUP* names FM-029, FM-031 and
  FM-032 but not FM-033. The receipt is only in the body (`## Asks`, the ship log).
- This is a gap in the tool, not a defect of this filing. Under the freeze it goes as one line into the closest open
  tracker.
- Fix: one line in FM-030, the person's lists: *a tracker re-asked after its clear drops out of ACTED ON*.

**Verdict:** READY WITH FINDINGS. R1–R4 are P3. The ask carries no P2 defect, and the raise line holds no sensitive
data.

## AU-1, 21bd5e8 (2026-09-24 18:41 CEST, Reviewer, session `8e509911/reviewer-1`)

**Scope.** `21bd5e8` (`21bd5e82fd19e1cbdf4938980ec5b657afc2ec75`) is one commit by the principal seat, under
`8e509911`, on this verdict's `48a7178`. It is the Auditor's AU-1 on PR 57: the Owner's FM-033 rule goes into the
contract. `git diff 48a7178 21bd5e8 --name-only` names only `AGENTS.md`, with five lines in and one out.

That is docs tier. The tool does not read the house rules: `--init` rewrites only the block between its markers, and
this repository's `AGENTS.md` has none.

**The bullet against his answer** (`65f37a4`, signed `G`, 16:29:09: *accepted - a pass judges before the first build
commit, the same day as a now, and a pass that finds it not ready asks you again*).
- ✓ **The answer authorises but does not judge.** *A signed answer authorises the work; it does not judge it ready* is
  the *no* his accepted option gives to *Does a signed answer that says now count as the judgement?*.
- ✓ **The same day as a now.** *… the same day when the answer says *now**.
- ✓ **A pass that is not ready asks again.** *… a pass that finds it not ready asks the Owner again*. The answer's
  *you* becomes *the Owner*.
- ✓ **Before the first build commit.** The bullet says *before any code is built on it*; R5 is about that wording.
- ✓ **The date.** *ruled 2026-09-24 16:29:09 (`65f37a4`)* is the commit's time and hash.

**The form.**
- ✓ The bullet has a bold lead, `(FM-033)`, and *— ruled <date> <time> (`<sha>`)*, as FM-031's cap bullet does. It sits
  last, after *Seats never need the Owner's checkout*.
- ✓ The intro now names FM-033 (`65f37a4`, 16:29) beside FM-031 (`d20bc89`, 11:08) and FM-032 (`ffa63b8`, 11:07), in
  the same form.
- Note, not a finding: the intro line is now 146 characters and was not re-wrapped. The section's other lines run to
  125.

**Gates at `21bd5e8`.**
- `python3 shoalmark.py` rewrites nothing, and `git status --porcelain` stays empty. `--check` 0; `--session-check` 0.
- `test_shoalmark.py` 0 (298 ok, all green); `test_core.py` 0 (148 ok, all green).
- `git merge-tree --write-tree origin/main 21bd5e8` onto `da2228e` is clean, writes `08b9583`, and has no conflicted
  path. PR 52 does not touch `AGENTS.md`. The merge is not a fast-forward, because `main` moved at 18:12.
- The commit message carries no pull-request number with the sign.

**R5 · P3 · medium · *Before any code is built* narrows *the first build commit*.**
- FM-033's gate (`:65`) keys on *a commit that changes anything outside `work-tracker/`*. That includes README and
  `AGENTS.md`, which this very commit changes.
- The bullet reads to a seat as *code only*, the same line the two tiers draw where documentation is docs. So the
  contract and the gate FM-033 will build would disagree about a docs commit outside `work-tracker/`.
- His answer says *build commit* and does not define it.
- Fix: *before its first build commit (FM-033's gate: any change outside `work-tracker/`)*. Or say that where the line
  falls is FM-033's to settle.

**R6 · P3 · high · *Four pieces were built unjudged on 2026-09-24* is one day short.**
- FM-024's first build commit, `89e0586`, is 2026-09-23 16:16, as FM-033's own table says. The other three were built
  on 09-24.
- Fix: *on 2026-09-23 and 2026-09-24*.

**Verdict:** READY WITH FINDINGS. AU-1 is met: the FM-033 rule is in the contract, true to his answer in its three
clauses. R5 and R6 are P3, to be fixed forward. R1–R4 are carried.
