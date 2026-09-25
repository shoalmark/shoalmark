# Review — FM-006's ask, when and how shoalmark goes public, at 4899353 (2026-09-25 16:39 CEST, Reviewer, session `8e509911/reviewer-6`)

- **Branch:** `fm/006-when-shoalmark-goes-public`, tip `4899353` (`48993534af7f4681f477d83697bc853069672d5a`), one commit
  on `origin/main` `8b267b4` (PR 76's merge), by the principal seat (`Session: 8e509911`), 16:29:05.
- **Tier: docs, one pass.** Two paths: FM-006 and INDEX. A defect in an ask's text is P2, because an ask cannot be
  fixed after he answers.
- **Independence:** a sub-agent of the branch's own session (`8e509911`); `--check` counts it *same session*. Reported.

## What I ran

- **The paste:** the user record at `2026-09-25T14:26:24.954Z` (16:26:24 CEST), read alone. Its fenced ```` ```Auditor ````
  block (480 bytes) equals the body's italic quote byte for byte ✓.
- **The earlier ask:** the user record at `14:22:12.928Z` (16:22:12), read alone. Its options carry five gates: a license
  chosen, CI green, the signing tier or the key, gitleaks clean, the client names ruled on. The section's *five gates, a
  license among them* is right ✓. `git log --all -S'go public'` finds only `4899353`, so the earlier ask never reached
  the board ✓.
- **The ask** against `ask_problems` and `--schema`:
  - one question, one `?`, at the end, 38 characters ✓;
  - three options of 111, 112 and 7 characters, each at most 120, all distinct ✓;
  - `ask-proposal:` is option 1, verbatim ✓. Options 2 and 3 are the Auditor's, verbatim. Option 1 is the Auditor's
    181-character first option, compressed to fit, and the body says so ✓;
  - `ask-since: 2026-09-25` and `next: owner` ✓;
  - `--owner` lists *FM-006 · ruling* with the question. The kind: R1.
- **"not yet"** passes the rule that no option opens with *yes* or *no*. It opens with *not*. To a *when* question it
  is a when, not a reply: picked, it is signed `accepted - not yet`, which reads as what he chose, and 0.18.1's relation
  names the option. It is the Auditor's wording. Confidence 75%.
- **The gates** against the counsel: the same three in substance ✓, but not word for word (R2).
- **Facts in the body:**
  - FM-007's answer reads *accepted - after the scoring, once the key is delivered.* ✓
  - FM-035's fix branch `fm/035-ci-green-on-every-platform` came back NOT READY at 14:23:59, and fixes followed at
    14:50:06, so *in review* ✓.
  - The parent project's ledger commit `17daad27` is 16:27:17, before `4899353` (16:29:05), so it came first ✓.
- **Gates:**
  - `--check` 0 (*20 open*), `--session-check` 0, the generator leaves no diff.
  - `merge-tree` against `origin/main` is clean (the tip's own tree). `origin/fm/030-the-acts-owed-to-him-on-his-board`
    does not exist (`git ls-remote`).
  - `test_shoalmark.py` 0 (394 ok), `test_core.py` 0 (148 ok).

## Findings

**R1 · P2 · confidence 70% · The ask is `ruling`, but a yes needs the Owner's hands.**
- `--schema`: *An ask whose yes needs the Owner's hands is `action`, whatever else it decides.* This is AU-22's rule.
- A yes to option 1 is a visibility switch on the forge. A yes to option 2 is a new public repository. Either happens on
  his account, at a tag after 09-29. Only *not yet* needs nothing of him.
- As a ruling, 0.18.3's `--answer` writes `next: build`, and the ask leaves `--owner` and `--standup`. The act would
  then sit on no list of his: FM-030's defect, and path line 6, *nothing owed to them lives only in … a tracker body*.
  FM-030's fix keeps accepted **action** asks on his lists, so the kind is what would keep this one there.
- The Auditor's paste says *(ruling)*. The schema's rule is the Auditor's own.
- The same class as FM-032's ask, graded P2 by the evening pass of 09-24 (its R3).
- **Fix:** `ask-kind: action`, with the ledger row to match. `--owner` then lists it as action.

**R2 · P3 · confidence high · The gates are called *word for word from the counsel*, and each adds words.**
- The counsel: *CI green on all three platforms, the signing tier stated or the hardware key live, and a gitleaks scan
  clean*.
- The body: *… on the tag that goes public*, *stated on the site*, *a `gitleaks` scan of the whole history*.
- The additions make explicit what the counsel implies, so the substance holds. But the label is false. The parent's
  ledger row gives the counsel's words and says the body has them word for word, so the two records differ.
- Option 1 points at these lines (*the three gates named in the body held*), so they are what he answers.
- **Fix:** in the same re-make, before his answer, either quote the counsel's clauses as the gates or mark the additions
  as the seat's.

**R3 · P3 · confidence medium · The proposal's condition is not on the board.**
- The body discloses it: *the first, if the client names may be public; if not, the second*.
- The dialog shows the ask, the proposal and the tracker's title (`t[6]`), so neither the condition nor the gates reach
  it.
- Option 1's *as it is*, set against option 2's *the client names removed*, is the only trace.
- **Fix:** in the same re-make, carry the condition in option 1's own words within 120 characters, for example *this
  repository as it is, client names and all, at the first tag after the 09-29 scoring, the three gates held* (110).

## Verdict

**NOT READY — R1 is P2.** R2 and R3 are P3. Take them into the same re-make: the ask cannot change after he answers.

What holds:
- The paste, quoted byte for byte.
- The earlier ask, rightly described and never on the board.
- One question, the proposal verbatim, the options distinct and within 120 characters.
- *not yet* passes.
- The facts in the body, and the ledger first.
- The gates are green.

The Owner lands this by merging; a merge rules nothing (path 5).

## Pass on 1dea28b (2026-09-25 16:58 CEST, Reviewer, session `8e509911/reviewer-6`)

**Scope.** `1dea28b` (`1dea28b7adcf31e81aa39d40d5222d240e90f012`): one commit by the principal seat (16:50:04) on the
verdict above (`92c65a0`). It changes FM-006 alone. **Tier: docs, one pass.** **Independence:** same session, reported.

**What I ran.**
- **The ask:** `ask-kind: action`. Three options of 115, 112 and 7 characters, all distinct. The proposal is option 1,
  verbatim. `--owner` lists *FM-006 · action*.
- **The body:**
  - The quote of the 14:26:24Z paste is still byte-identical.
  - Each gate is now the counsel's own clause in italics, found verbatim in the paste, with the seat's gloss in
    brackets: *CI green on all three platforms*, *the signing tier stated or the hardware key live*, *a gitleaks scan
    clean*.
  - The ship log gains one row, and no row is edited.
- **The parent ledger**, read-only (`git ls-remote`, then `git show` in `worktrees/reviewer-2`): branch
  `feat/190-day-four-the-thirteenth-hour-row-47-re-made-and-row-46-answered` is at `671e1259`, 16:50:39. Its appended
  clause carries option 1 exactly as the board has it. Options 2 and 3 stand unchanged in the row's merged cells. So the
  board and the ledger carry the same option text ✓.
- **Gates:**
  - `--check` 0, `--session-check` 0, the generator leaves no diff.
  - `merge-tree` against `origin/main` (`8b267b4`) is clean. No `fm/030*` head exists on origin.
  - `test_shoalmark.py` 0 (394 ok), `test_core.py` 0 (148 ok).

**The findings of the first pass.**
- **R1 ✓ closed.** The kind is `action`, and the body says why: *a yes switches the repository's visibility or creates
  a new one on his account*.
- **R2 ✓ closed.** The gates are in the counsel's words, and the gloss stands apart.
- **R3 ✓ closed.** The condition now stands in the option he reads before he signs.

**R4 · P3 · confidence 60% · Option 1 says *if*; his pick decides it.**
- Signed, option 1 reads `accepted - this repository as it is, if its client names may be public — …`.
- The *if* is decided by his choice between option 1 and option 2 (*the client names removed*). A seat reads a pick of
  option 1 as his judgement that the names may be public, which is sound.
- But the line itself keeps a condition. A declarative *client names and all* would leave none.
- The option also drops *09-29* and *named in the body*. *the scoring* is his own phrase, from FM-007's answer, and the
  gates are named in the body's heading.
- **Not blocking.** Change it only if the ask is touched again before the board.

Noted, not graded (the parent's record): the clause says *re-made with the board at 16:49*. The board's commit is
16:50:04 and the clause's own is 16:50:39, so the ledger followed the board by 35 seconds.

**Verdict on 1dea28b: READY WITH FINDINGS (R4 P3).** R1–R3 are closed. The ask meets every form rule, and its kind now
keeps the act on his board.

The Owner lands this by merging; a merge rules nothing (path 5).
