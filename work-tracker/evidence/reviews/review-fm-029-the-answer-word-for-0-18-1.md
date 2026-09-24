# Review — FM-029's ask on the answer's word for 0.18.1, at 37e48bb (2026-09-24 13:32 CEST, Reviewer, session `8e509911/reviewer-1`)

- **Branch:** `fm/029-the-answer-word-for-0-18-1`, tip `37e48bb` (`37e48bb34a7426aa17bdd8d927fd3c1e3dea1abb`), two
  commits on `origin/main` `ed11081`:
  - `9f9bbe8`: the Implementer (`implementer@seat`, `Session: 8e509911/implementer-17`). The draft: the ask, its kind,
    its day and its four options, `next: review`, *Candidates for 0.18.1*, a ship-log row, and the registry row.
  - `37e48bb`: the principal seat (`principal@seat`, `Session: 8e509911`). `ask-proposal:`, `next: owner`, and the
    ship-log row's *13:0x* made *13:07:09*. Nothing else (`git diff 9f9bbe8 37e48bb`: three lines).
- **Tier: docs, one pass.** `git diff --name-only origin/main...HEAD` names two files, the FM-029 tracker and
  `work-tracker/sessions.md`. There is no `shoalmark.py`, no test, no configuration and no hook. The change sets ask
  values the gate validates, but it adds no key and changes no schema, so it is not code under FM-032 S1's caveat. The
  rule is FM-032 S1, ruled today (`answer: "accepted - all four now"`). `AGENTS.md` on `origin/main` does not carry
  it yet. P3s are fixed forward with no re-pass. A defect in the ask's text that would make his answer ambiguous or
  wrong is P2.
- **Independence:** same session `8e509911`. Both authors are that session or its sub-session, and so is this seat.
  Reported, not refused. `--check` will count this verdict as *same session*.

## What I ran

| run | result |
|---|---|
| `python3 shoalmark.py --check` | exit 0 |
| `python3 shoalmark.py --session-check` | exit 0 |
| `python3 shoalmark.py` | 32 trackers, 0 unknown-status; `git status --porcelain` empty, so INDEX is the generated one |
| `python3 shoalmark.py --owner` | `1 NEED THE OWNER`: FM-029, ruling, the ask as written. Nothing else |
| `test_shoalmark.py` | exit 0, 264 ok, all green (Python 3.14.3) |
| `test_core.py` | exit 0, 148 ok, all green |
| `git merge-tree --write-tree origin/main HEAD` | clean. `origin/main` is an ancestor, so the merge is a fast-forward |
| the ask's shape, by script | see below |
| the parent project's ledger row, read-only `git show` of its `asks.md` on its FEAT-190 branch | `:61`; the question cell equals the `ask:` value byte for byte (229 = 229) |

The code claims were read at `ed11081`, where `shoalmark.py` is byte-identical to `cdd6e3f`. They were also read
at the 0.18.0 branch `fm/031-0-18-0-the-queue-in-one-view-and-the-freeze` (`636f56e`), because the candidates build on
0.18.0.

## Claims

**The ask's shape.** ✓ on every count the gate or the brief sets.
- `ask:` is **229** characters (`ASK_MAX` 300). It has one `?`, at its end, and asks one question with the three
  alternatives named: the relation, the verbs, both.
- The four options are 69, 34, 14 and 30 characters (`ASK_OPTION_MAX` 120). Each is a choice he can sign.
- `ask-proposal:` is option 1 verbatim.
- `ask-kind: ruling`, `ask-since: 2026-09-24` and `next: owner` are set.
- What the ask *says* is where R1 and R2 are.

**The facts in *Candidates for 0.18.1*.**
- ✓ FM-031's first answer, `accepted - all three rules now, S1 then S2`, is `d20bc89`. It is signed (`G`) and is the
  proposal.
- ✓ `7c97c5b` (signed, `G`, 12:39:56) rewrote the answer line to the text the body quotes, word for word. It changes
  one line and nothing else. Its subject is not `answer_cmd()`'s `<id>: <answer>`, so *by hand* holds.
- ✓ `ed11081` is PR 46's merge, and its second parent is `7c97c5b`. The body and the ship log write it as *PR 46*.
- ✓ The other answers on this `main` are FM-007 and FM-032. Each equals its proposal. FM-005's one cleared exchange
  is *withdrawn*, with no answer given. So the only two answers whose word and choice differ are D1 and FM-031.
- ✓ The parent project appears only as *the parent project's D1 (its FEAT-190)*, with the answer's shape, which is
  the finding itself. Of the hex tokens in the diff, only `8e509911`, the session root, does not resolve here. R7 is
  about a commit message.
- ✗ *0.18.0's `revoke`* has no source on this branch. See R3.

**The code the candidates name.** ✓ for every function, at `ed11081` and on the 0.18.0 branch:
`view()` (`:1314`), `render_html()` (`:1612`), `owner_digest()` (`:756`), `standup()` (`:785`), `answered()`
(`:741`), `clear_ask()` (`:2836`), `answer_cmd()` (`:829`), `act()` (`:1248`), `sign()` (`:1274`),
`dirty_refusal()` (`:987`, whose pattern is at `:1008`) and `front_matter_schema()` (`:275`, whose `answer` entry is
at `:291`).
- ✓ The row `render_html()` builds carries the answer, the proposal and the options (`t[29][4..6]`, `:1628`).
  `view()` does not print them today, so candidate 1's *where it is printed* is a change, as it is written.
- ✓ `act()` builds `--answer <id> accept|reject "<chosen>"`, and `sign()` previews the word (`:1266–1268`). So
  *its pick choosing the verb* describes a real seam.
- ✓ `clear_ask()` writes `**answered** — <answer>` into `## Asks` (`:2859–2860`). So under 2, the word survives a
  clear.
- ✓ The key-parity check exists: `test_shoalmark.py:1140`, *C4 · the German table the tool SHIPS … carries every
  label*.
- ✓ with a nit: the commit subject is `f"{tid}: {answer[:60]}"` (`:954`), the first 60 characters. The word comes
  first, so *Leaves* holds.

**The *Done when* reading.** ✓ *Only 3 meets every line* is true as *Done when* is written.
- 1 fails line 1 and meets the rest. Line 6 is vacuous under 1, because 1 brings no new wording.
- 2 fails line 3, as the text says. It also fails part of line 4 and part of line 7 (R6).
- 3 is the union of the two, and meets every line.

**The ship-log row.** ✓ in part.
- It is dated 13:14 CEST. The draft's commit is 13:17:27, so the row is not later than the work.
- It cites *PR 46*. The time 13:07:09 is the principal seat's, from the transcript; I cannot see the transcript.
- ✗ The Owner's word is not marked *normalised* (R4).

**The registry row** (`sessions.md:39`). ✓
- It reads `8e509911/implementer-17 | implementer | session 8e509911 | … | shoalmark-impl-4 | 2026-09-24 13:10 | —`.
  The row is open.
- The worktree `shoalmark-impl-4` exists and is at `9f9bbe8` on this branch.
- `9f9bbe8`'s trailer is `Session: 8e509911/implementer-17`. `-16` is on the 0.18.0 branch, and no id is used twice
  across the remote branches.

**The scope.** ✓ Nothing outside FM-029 and `sessions.md` changed. INDEX is unchanged, and it regenerates the same.
Neither commit message carries a pull-request number with the sign.

## Findings

**R1 · P2 · confidence high · The ask counts 0.18.0's `revoke` as a new verb he rules, and the verbs as two.**
- **What:** `:7` says *(changed, chose, revoked)* are the *new verbs you type* (alternative 2). It also says that
  under alternative 1 the relation, *revoked* among it, is printed *from the two verbs*. Option 2 reads *the relation
  only — two verbs stay*.
- **The body says otherwise.** `:81` reads *Each keeps … 0.18.0's `revoke`*, and `:97–98` puts the new verbs
  *beside `accept` · `reject` and 0.18.0's `revoke`*. On the 0.18.0 branch, `--answer` has three verbs
  (`answer_cmd`: `("accept", "reject", "revoke")`), and `revoked - <reason>` comes from the third. The parent's ledger
  row says the same: *0.18.0 ships revoke and supersede meanwhile*.
- **Why it matters:** read as written, the answer *the relation only — two verbs stay* rules `revoke` out, and so
  does *none*. *The verbs only* rules it in as if it were new. The body says every candidate keeps it. So two of his
  four signable answers would contradict 0.18.0, and the signed line could not say which one stands. That is the
  finding FM-029 files, a signed word that misstates him, repeated in its own ask.
- **Fix:** take *revoked* out of the new verbs: *new verbs you type (changed, chose)*. Say *from the verbs you type
  today*, not *from the two verbs*. Make option 2 *the relation only — no new verbs*. The ask stays under 300. The
  parent's ledger row must then be re-rowed word for word.

**R2 · P2 · confidence medium · Under alternative 1 the ask says *the record* prints the relation, and candidate 1
leaves the signed line saying *accepted*.**
- **What:** `:7` reads *the board and the record print its relation to the proposal*. In this tracker, *the record*
  is the signed line: see the hook (*the signed record reads `accepted - <the third option>`*), `:24` (*His record
  reads `answer: …`*) and `:64`. Candidate 1's *Leaves* (`:94–96`) says the opposite: the front matter and `git log`
  still say `accepted - <the third option>`. Only `--answered` and a cleared `## Asks` carry the relation.
- **Why it matters:** whether the signed line itself says the relation is the one thing that separates option 2 from
  options 1 and 3. It is also *Done when*'s first line. The ask he signs says option 2 does it. `--owner` shows him
  the ask and nothing else, and the dialog adds only the proposal and the options, never the body. So *the relation
  only* could be chosen on a premise the body contradicts.
- **Also:** the parenthesis lists four relations and leaves out *rejected*, which candidate 1 names (`:87`).
- **Fix:** name what prints and what does not, for example *the board, `--owner` and `--answered` print its relation
  (the proposal · with a change · option N · rejected · revoked); the file keeps accepted*. Fold it into R1's
  rewrite. The whole must stay ≤ 300 characters, with one `?`.

**R3 · P3 · *0.18.0's `revoke`* is cited with no source, and 0.18.0's `--supersede` is not named.**
- **What:** `:81` and `:97–98`. On this branch's base (`VERSION` 0.17.8), `shoalmark.py` has no `revoke`, and no
  tracker on `main` mentions it. It lives on the unmerged 0.18.0 branch (`bd7d5ea`, *an answer is revoked or
  superseded, never overwritten*). That branch also adds `accept|reject "<option>" --supersede`, and candidate 2's
  new verbs would sit beside it too.
- **Fix:** one clause giving where 0.18.0's `revoke` and `--supersede` live, and naming `--supersede` in
  candidate 2's list.
- **Note, not a finding here:** on 0.18.0, `dirty_refusal()` still parses only `(accepted|rejected)` (`:1333`
  there). So a half-written `revoke` gets no *give it again* line. That is for 0.18.0's review. Candidate 2 touches
  that pattern anyway.

**R4 · P3 · The Owner's word is not marked normalised.**
- **What:** `:68` and `:140` quote *we plan v0.18.1 right away* in italics, with no quotation marks and no mark. The
  parent's ledger row quotes the same line as *his word normalised: "We plan v0.18.1 right away."*. The house form
  is *(spelling normalised)*, as in FM-006 `:39`, FM-023 `:23`, FM-031 `:58` and FM-032 `:86`.
- **Fix:** *(spelling normalised)* at both places, with the quotation marks, as the ledger has it.

**R5 · P3 · The ship log has no row for the ask put to him.**
- **What:** the one new row (13:14) records the draft and ends *the proposal the Principal's*. `37e48bb` (13:22) set
  the proposal to *both* and `next: owner`, and it has no row. FM-032's R10 is the precedent.
- **Fix:** one row at 13:22 saying the proposal was set, the ask was put to the Owner, and the parent's ledger row
  came first.

**R6 · P3 · The *Done when* tally for 2 names one unmet line, and there are more.**
- **What:** `:114–115` say *2 alone leaves the third … unmet*. 2 also leaves:
  - line 4 for every answer signed before it, because `--answered` shows `accepted - <option>`;
  - line 7's old-record cases: bare `accepted`, the em-dash answer, and a cleared exchange that reads *relation not
    recorded*. Without a reader these have nothing to test.
- **The conclusion stands.** Only 3 meets every line.
- **Fix:** *2 alone leaves the third unmet, and with it the old-record half of the fourth and the seventh.*

**R7 · P3 · A commit message names a branch of the parent project.**
- **What:** `37e48bb`'s body names the parent's branch in full. That is more of the parent project than its tracker
  id, and the brief allows only the id. FM-032's R2 is the precedent: a consumer's commit hash in a shoalmark file
  was graded P3.
- **Fix:** a pushed message is not rewritten. From now on, *the parent's ledger row (its FEAT-190)* is enough.

## Verdict

**NOT READY: R1 and R2 are P2.** Both are in the ask's text, which he signs as written. R3–R7 are P3. Under the docs
tier they are fixed forward. R4 and R5 can ride with the ask's rewrite.

What holds:
- The gates are green, both suites pass, and INDEX is the generated one.
- `--owner` lists FM-029 alone.
- The facts about PR 46, FM-031, FM-007 and FM-032 are true.
- Every function the candidates name exists and does what they say.
- *Only 3 meets every line* is true.
- The parent's ledger row equals the ask word for word. After R1 and R2 it has to be re-rowed.

Not verified: the Owner's words and their time (13:07:09) against the transcript, and D1's answer in the parent
project beyond its ledger row.
