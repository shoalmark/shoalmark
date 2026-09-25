# Review — FM-037, the triage guard at 0be4f20

Reviewed: `0be4f206b67918b5eab2a326fba4fd846d6d1a16` on
`fm/037-only-the-owner-changes-his-intent-and-his-path`, completed 2026-09-26.

**Tier: code — the gate, critical. Verdict: READY.**

## Seat and independence

A cold session started by the Owner under his path line 3. Reviewer session `01a0da10`,
worktree `shoalmark-review-cold`; independent of building session
`8e509911/implementer-28` in `shoalmark-impl`. The four cold-start answers: provide
adversarial pressure; guard against making refutation the result; use the seven runnable
clauses, their negative controls and the real history to expose that shadow; hand this record
to the Owner for the Principal and then the independently planned Auditor pass. I changed
only this review file, fixed nothing and did not disposition another seat's finding. The
sealed session directory `8b91dba2` was untouched and outside every command and search scope.

## What I reviewed

- `git fetch origin` resolved the required branch head and local detached `HEAD` to
  `0be4f206b67918b5eab2a326fba4fd846d6d1a16`. The branch contains eleven commits over its
  merge base `0d60d552b3c6322cc463d5caf427a7df1fea9a00`, including the clean merge of PR 79.
- `git diff --name-only origin/main...HEAD` named exactly: `CHANGELOG.md`, `README.md`,
  `docs/de/signing.md`, `docs/signing.md`, `shoalmark.py`, `test_shoalmark.py`,
  `work-tracker/FM-037-a-seat-can-change-the-owner-s-intent-and-current-path-in.md`, and
  `work-tracker/INDEX.md`. That makes this the code tier: tool, gate and tests changed.
- The Owner's seven clauses in FM-037, the Implementer's brief and every branch commit body
  were read. The filed Owner text remains in the tracker with sha256 prefix `12e77e72`; the
  attribution correction is an additive ship-log row, not a rewrite of that filed paste.
- `python3.14 shoalmark.py --schema` adds no FM-037 key. The guard is derived from the existing
  `tracker_dir`, `[headings]`, `[seats]` and rights. The README, English signing page, German
  signing page and the `Unreleased — 0.18.4` changelog bullet state the implemented rule,
  fallback, Subversion boundary and tier-0 limit consistently.

## Verification against the seven clauses

1. **Protected changes and signed positive control.** The synthetic suite changes each section,
   renames a heading, deletes and renames `TRIAGE.md`, re-points `tracker_dir`, forges the
   Owner's author email without a signature, uses the Owner's key under a seat author, and uses
   a seat key under the Owner author. Every negative case is refused. A commit with `%G?` `G`,
   signer identity equal to its author email and that author holding `answer` in the default
   branch passes. A merge carrying a parent's accepted text passes; a merge resolution that
   creates text no parent had is refused as the merge's own change.
2. **Refusal content.** The observed refusal names the seven-character commit, subject,
   protected section and operation. It gives both routes: the Owner commits it signed; a seat
   puts one ruling ask before him with `ask:`, `ask-since:` and `next: owner`.
3. **Open seat area and scaffold.** A `## Passes` edit passes silently. The exact `--init`
   scaffold is accepted where no prior sections existed, while a seat filling its own intent
   into that scaffold is refused.
4. **Queue.** The synthetic pull request with an unsigned intent change reads
   `wait: TRIAGE.md changed unsigned`; a pushed branch without a pull request says the same and
   names the commit. Signed-owner and Passes-only controls continue to the normal verdict
   reading. A stacked branch cannot appoint itself Owner: queue reads the Owner from the
   origin default branch, as `--check` does.
5. **Weaker proof and Subversion.** With an unsigned Owner seat, a different author is refused
   and the text says it proves the author only; the matching author passes under that explicitly
   weaker rule. The Subversion probe emits one line saying the guard is out of scope because the
   working copy carries no signature.
6. **Limit.** The refusal's last substantive line says that a commit signed with the Owner's key
   passes and that, at tier 0, any process on his account holds that key (FM-007). README and
   both signing pages say the same.
7. **Synthetic and real history.** The full suite walked all 572 commits through `0d60d55` as
   the branch gate walks them. Exactly `45198d5`, `c755d31`, `8d14b6b`, `7dd6ba6`, `fe36cc0`
   and `ad9bf67` change the protected text after the root; each verifies `G` with signer and
   author email `holgoijo@gmail.com` and is accepted. The unsigned root `a680fdf` is identified
   as a historical refusal. `ae1f05e` is present and produces no protected-text change.

The commit-msg hook was also exercised. It refuses a seat's staged protected change before the
commit exists, permits an Owner-authored commit with a note that its signature is still to be
judged, and `--check` then refuses that commit when unsigned. It refuses a merge being made when
the merge brings an earlier seat change. This is the correct boundary: the hook can prove the
author only because signing happens after hooks; `--check` on the branch is the gate.

## R7 — the move reading

The strongest counterfact is the apparent conflict between clause 1's refusal of a moved
`TRIAGE.md` and clause 7's required acceptance of `ae1f05e`. I agree with the Implementer's
reading and would not rule otherwise. The protected object is what a pass reads as the Owner's
intent and current path. Moving `TRIAGE.md` away from the configured tracker directory, renaming
it there, or re-pointing `tracker_dir` so those bytes read differently or disappear is refused.
Moving the whole tracker and its key together while both sections remain byte-identical changes
neither protected object; that is `ae1f05e`.

The alternative—refuse every move and re-point, then exempt `ae1f05e` by date or commit—is
weaker: it creates a permanent historical bypass and rejects a relocation that preserves every
word the Owner wrote. The chosen rule is stated in the design commit, README and changelog and
proved by both the synthetic whole-tracker move and the real-history walk. The Owner's word
would settle a different intended reading; no technical contradiction remains for the Auditor.

## Findings

No R finding is minted. I found no P2 defect requiring the code-tier loop and no P3 defect to
carry forward.

## Suites, gates and integration

| Command | Exit | Passing checks | Browser skips |
|---|---:|---:|---:|
| `python3.14 test_shoalmark.py` (3.14.3) | 0 | 454 | 0 |
| `python3.14 test_core.py` (3.14.3) | 0 | 148 | 0 |
| `/usr/bin/python3 test_shoalmark.py` (3.9.6) | 0 | 454 | 0 |
| `/usr/bin/python3 test_core.py` (3.9.6) | 0 | 148 | 0 |

Every suite ended `all green`; both integration runs ended `skipped here: 0 checks — every
check ran`. `python3.14 shoalmark.py --check` exited 0: INDEX up to date, every build commit
under a judged In Progress tracker, and eleven branch commits inspected with none changing the
Owner's protected sections. `python3.14 shoalmark.py --session-check` exited 0.
`git diff --check origin/main...HEAD` exited 0.

PR 79 landed before this review and is already merged into the branch as `3aeb4e5`; the branch's
merge base is its resulting main tip `0d60d55`. Origin/main has since advanced through PR 81 to
`87ee09e`. `git merge-tree --write-tree origin/main HEAD` exited 0 and produced tree
`adeee1b99911abdf91440d4dd63d87c11f7b2f99`: clean. No pull request currently exists for this
branch. Any later merge of main or other non-review commit voids this verdict and needs another
verification.

The strongest counterfact was R7's literal move wording; it survives as the explicit,
tested text-protection rule above. The unresolved environmental unknown is the tracker's own:
the real-history SSH verification has not been witnessed on Windows runners; both local promised
Python versions did verify it. Readiness reverses if a protected byte change can pass without the
Owner's qualifying commit, or if any post-verdict non-review commit changes the head. The Auditor
independently verifies next against its sealed plan. Only the Owner opens and merges the pull
request; this review neither rules his intent nor lands the branch.

**Verdict: READY.**

the Owner lands this by merging; a merge rules nothing.

## Verified again on b0d863e — AU-19 and AU-20

Reviewed: `b0d863e3e3eab8103cfbfc2000469ab42842ab5e`, the branch's tip, completed 2026-09-26.
This pass covers that one commit on top of the verdict `8185a5c` (READY on `0be4f20`), which
stands on its own. **Tier: code — the gate, critical.**

**Seat and independence.** A cold session started by the Owner under his path line 3. Reviewer
session `74b23bf5`, worktree `shoalmark-review-cold`; independent of building session
`8e509911/implementer-28` in `shoalmark-impl`. I changed only this review file and fixed
nothing. The sealed session directory `8b91dba2` was untouched and outside every command and
search scope. The suites ran with `TZ=UTC`: the run began at 01:16 CEST, inside FM-028's known
00:00–02:00 CEST failure window for one rendered-board check, which is unrelated to this branch.
`TZ=UTC` is the documented workaround.

**The commit is what it says.** `b0d863e` is the Implementer's `21a07be` (on `0be4f20`),
cherry-picked onto `8185a5c`. Both give `git patch-id --stable` `0aace8895db3`, so nothing was
rewritten. Against `0be4f20`, the diff is this commit's seven files plus this review file. In
`shoalmark.py` the diff holds only three kinds of change:
- the signers handling: `trusted_signers`, `signers_args`, `signers_gap`, `signers_paths`,
  `kept_changes` and `guard_why`; `verified_as` and `signature_gap` routed through it; `keys=`
  passed through `guard_walk`, `triage_guard`, `triage_pending` and `triage_reading`; and
  `signature_gap` moved ahead of `%G?` in `guard_verdicts`;
- AU-20's `unwritten` and `PATH_SCAFFOLD`;
- the guard's summary words and a trailing-space trim in `did_words`.

No other guard rule changed, and `--schema` has no new key. The docs lines (README §5, a row in
the refusal table, `docs/signing.md` and its German twin, which I read against each other), the
CHANGELOG bullet and FM-037's state and ship-log row say what the code does.

**AU-19: what I ran.** I built a repro of my own, apart from the suite. It is one throwaway
repository, run with the tool at `0be4f20` and at `b0d863e`. Main carries the Owner's key in
`docs/work-tracker/allowed_signers`, signed, and the clone verifies against the checkout's own
copy of that file, which is `docs/signing.md`'s setup.

| Case on a seat's branch | `0be4f20` | `b0d863e` |
|---|---|---|
| 1 · the seat appends its key under `h@x`, then signs a path change as `h@x` with it | **accepted**: "1 change them, each his own commit" (the hole, reproduced; the checkout reads `G h@x`) | both commits refused: the path commit's "signature does not verify (`%G?` U)"; the key commit "changes the signers file … only the Owner changes the keys his signature is verified against" |
| `verified_as(HEAD, "h@x")` on case 1 (the answer gate) | `True` | `False` |
| 2 · both commits authored as `h@x`, both signed with the seat's key | accepted | both refused, `%G?` U |
| 3 · the key brought in by a seat's hand-resolved merge | not seen | refused: "brings a text into the signers file … that no parent had" |
| 4 · the seat deletes the signers file | not seen | refused: "deletes or moves the signers file" |
| 5 · the Owner's signed change to the file (a new principal), then to the path | accepted | accepted, "each his own commit" |

Every `0be4f20` run, and the `b0d863e` run on case 5, exits 3. That is INDEX drift from my
unregenerated repro commits, not the guard; every `b0d863e` refusal exits 4. The suite's two new AU-19 checks agree with the repro:
- the vouching branch is refused in the guard (two lines) and in the answer gate (`--check`
  exits 4 with "the answer's commit … does not verify as `h@x`");
- the Owner's real key is accepted, for his change to the signers file and for his change to
  the path.

The bootstrap case: where main carries no signers file, a branch that writes one fails
`--check` with a checkout finding (exit 4). That holds for the seat's key and for the Owner's
own, which matches the docs' "its first version lands on the default branch by his own hand".

The file now at the root of trust: main's `work-tracker/allowed_signers` came in with `216dd07`,
a `principal@seat` commit, unsigned and on main since before the guard existed. Its one key matches the
Owner's configured `user.signingkey` (I compared the key type and the key).

**AU-20: the commit accepts the historical scaffolds; it did not move the test's base.** The new
`unwritten` recognises a scaffold by exact text, whitespace aside, and only where no parent had
the section:
- the intent: `owners_intent` over `INTENT_SCAFFOLD` must leave nothing;
- the path: every line must come from `PATH_SCAFFOLD`, which holds the English note, the German
  note from `examples/de/TRIAGE.md` and a bare `1.`.

`a680fdf`'s `TRIAGE.md` holds exactly the bare `- **for** —` lines, the path note and `1.`. The
real-history check keeps its base `0d60d55`. It now asserts that `a680fdf` is walked and that
the changed set is exactly the six signed commits. It is green on 3.14 and 3.9.

### Findings

**R1 · P3 · confidence 90%, reproduced.** `--answer`'s pre-push self-check
(`owner_change`, `shoalmark.py:1856`) still reads `%G?`/`%GS` against the clone's own signers
file. The gate it promises to mirror (its comment says "the gate's own rule, asked here so the
change is never pushed under one the gate will refuse") now reads the default branch's copy, in
`verified_as`. This commit introduced the split; before it, both read the same file.

Reproduced mid key-rotation:
1. The Owner's signed commit (first key) adds his second key on `ap/rotate`.
2. `--answer AP-050 accept "yes"`, signed with the second key, printed "signed, on
   `answer/ap-050`, pushed", and origin holds the branch.
3. `--check` on it exits 4 with "the answer's commit … does not verify as `h@x` … sign it
   (`git commit -S`)". That tells him to sign a commit he signed, and it never names the way
   through: land the key on the default branch first.

No seat gets past the gate. The cost is an answer pushed that the gate refuses, and a wrong way
through. *Fix named:* call `verified_as("HEAD", email)` there, and where a commit is signed but
its key is not in the default branch's file, have the answer gate's refusal say so.

**R2 · P3 · confidence 95% on the mechanism (reproduced), 70% on the tier.** Where the default
branch carries no signers file at the path that `gpg.ssh.allowedSignersFile` names inside a
checkout, `trusted_signers` falls back to the working copy's file, that is, whatever branch is
checked out. `signers_gap` then sets aside only the commits whose own tree carries the file.
So a checkout on a branch that writes the file vouches for *another* branch's commits.

The repro is a PR whose one commit changes the path, signed as `h@x` with the seat's key.
`triage_reading`, which gives `--queue`'s word, returns:
- with the checkout on main: `wait: TRIAGE.md change not verified here`;
- with the checkout on the vouching branch: `None`, a clean pull request.

The vouching branch itself still fails `--check`. This is narrower than AU-19, and not reachable
in shoalmark, whose main carries the file. It needs the setup window before the Owner's first
signers file lands on the default branch, and a gate run from a checkout on the offending
branch. *Fix named:* where that path sits in a checkout and the default branch does not carry
the file, verify nothing. Every SSH-signed commit then gets the gap: "`<path>` is not on
<trunk>: commit its first version there, signed", in the docs' own words, "a branch cannot prove
a key the default branch does not hold".

No P2. Neither finding lets a branch vouch for itself where the default branch holds the file,
which is AU-19's case and the documented setup.

### Suites, gates and integration

| Command (`TZ=UTC`) | Exit | Passing checks | Skips |
|---|---:|---:|---:|
| `python3.14 test_shoalmark.py` (3.14.3) | 0 | 456 | 0 |
| `python3.14 test_core.py` (3.14.3) | 0 | 148 | 0 |
| `/usr/bin/python3 test_shoalmark.py` (3.9.6) | 0 | 456 | 0 |
| `/usr/bin/python3 test_core.py` (3.9.6) | 0 | 148 | 0 |

Every suite ended `all green`, and both integration runs ended `skipped here: 0 checks — every
check ran`.

The integration suite gained two checks since `0be4f20` (454 → 456), the two AU-19 cases. Other
runs on the tip:
- `python3.14 shoalmark.py --check` exits 0. It read 13 commits on the branch since origin/main,
  and none changes the two sections or his signers file.
- `--session-check` exits 0, and `git diff --check origin/main...HEAD` exits 0.
- Origin/main is at `87ee09e` (PR 81, FM-006's filing), which the branch does not carry.
  `git merge-tree --write-tree origin/main HEAD` exits 0 with tree
  `388b906eb4863147dee2c5bfd39b9b9aa864c53d`: clean.
- The forge has no pull request for this branch.

Unproven: the five-job matrix, and on Windows in particular the temporary signers file passed
through `-c` and removed at exit. CI runs on a tag.

Readiness reverses if, where the default branch holds the signers file, a commit signed with a
key that file does not hold passes `--check`, `--queue` or the answer gate. It also reverses if
any non-review commit lands after this one.

the Owner lands this by merging; a merge rules nothing.

**Verdict: READY WITH FINDINGS (P3 only).**
