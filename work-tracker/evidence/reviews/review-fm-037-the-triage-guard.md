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
