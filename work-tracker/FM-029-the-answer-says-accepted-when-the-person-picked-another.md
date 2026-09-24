---
id: FM-029
status: Proposed
considered: FM-008, FM-013, FM-014, FM-017, FM-018, FM-030
tags: bug
next: owner
ask: "Rule the answer's word for 0.18.1: the board and every reading print the answer's relation to the proposal (accepted it · accepted with a change · chose option N · rejected · revoked), the signed line unchanged; or new verbs you type (changed, chose) beside accept, reject and revoke; or both?"
ask-kind: ruling
ask-since: 2026-09-24
ask-proposal: "both — the relation computed for every answer, the verbs changed and chose for new ones"
ask-options: "both — the relation computed for every answer, the verbs changed and chose for new ones | the relation only — no new verbs | the verbs only | none — the word stays accepted"
answer: "accepted - the relation only — no new verbs"
answered: 2026-09-24
answered-by: holgo99
hook: "The person picked the third of three options, not the proposal, and the signed record reads `accepted - <the third option>`. Read alone, the word says he agreed with the seat, and a fleet that counts how often the person takes the proposal counts this answer the wrong way."
---

# FM-029 — The answer says accepted when the person picked an option other than the proposal

## What is true now

**Filed 2026-09-24; nothing is built.** Found on 0.17.7 in a consumer repository. The lines below are from 0.17.8
(`v0.17.8` = `62db9f8`; `main` at `cdd6e3f`). A first review ran on an earlier chain of this branch, which was
replaced before its merge to keep unredacted detail out of the record; it found R1–R16, and this text closes R1–R10.

**What happened.** A ruling offered three options, with the proposal first. The person answered through the board,
picked the third option under *accept*, and signed. His record reads `answer: "accepted - <the third option>"`. Nothing
in the front matter says that the proposal was turned down. Only a reader who compares the text with `ask-proposal:`
by hand finds that out. The first reader, the seat that had asked, read it right because it knew the options. A
scorer counting agreement with proposals at the end of a week would read the word.

**Why.** On the board, *accept* means "answer with one of the options, or with changed text". It does not mean "agree
with the proposal". The recorded word is the button, not the answer:

| where | line | what it writes |
|---|---|---|
| the board's dialog | `shoalmark.py:1264–1268` | `(kind=="accept"?"accepted":"rejected")+(chosen?" - "+chosen:"")`. `chosen` is any option picked under *accept*, the proposal or not, after `q()` has trimmed it and turned `"` into `'` (:1264) and runs of whitespace into one space (:1268) |
| `--answer` | `shoalmark.py:839`, `:893`, `:945` | `("accepted" if verdict == "accept" else "rejected") + (f" - {text}" if text else "")`, the text's whitespace collapsed (:839) and `"` written as `'` (:945) |
| the schema | `shoalmark.py:291` | tells the seat an answer is *`accepted`, `accepted — <his change>`, or `rejected — <why …>`*, which is the same three words |

So one word covers three different answers: the proposal, another listed option, and changed text.

**What an old record still holds, and what it lost.**

- **While the ask is in the front matter,** `ask-proposal:` and `ask-options:` stand beside `answer:`. The relation to
  the proposal can be derived when the record is read, but only with the answer's own normalisation applied to both
  sides: trim, `"` → `'`, whitespace runs → one space. A plain equality test files the proposal itself as changed
  text whenever the proposal holds a double quote or a double space (reproduced by the review, R2).
- **Once `--clear-ask` has run,** the proposal and the options are gone. `--clear-ask` strips every line in
  `ASK_LINES`, `ask-proposal:` and `ask-options:` among them (:2803, :2855), and writes only the question and the
  answer into `## Asks` (:2859–2860). For those exchanges the relation cannot be derived from the file. It exists only
  in git history, in the commit that set the ask.

**Shapes an old record can take:** `accepted` alone; `accepted - <text>`; a hand-written `accepted — <text>` with an em
dash (the schema's own form, :291); `rejected - <text>`; an ask that carried no `ask-proposal:` at all.

**Where an answer is shown today.** `--answered` prints it (:741–752). The board's waiting list and `--owner`'s digest
list only asks **without** an answer (:1292, :708), so neither shows an answer at all. Once FM-030 lands, an accepted
action ask is shown there as a promise.

**Code that reads the word.** The half-written-answer recovery (:1008) parses `(accepted|rejected)` to rebuild the
*give it again* command (FM-017). Any new wording must keep that hint.

## Why

The answer is the one line the person signs. If a line that turns the proposal down reads as agreement, the record
misstates him, and any measure of how often he follows the seat is wrong in the direction that flatters the seat.

## Candidates for 0.18.1

**The Owner's word of 2026-09-24, 13:07:09 (spelling normalised): *we plan v0.18.1 right away*.** Two answers signed that day say *accepted* over a
choice that is not the proposal:

- **The parent project's D1** (its FEAT-190), answered through the board's dialog: the third of three options, under
  *accepted*.
- **FM-031, rewritten by hand in PR 46** (`7c97c5b`, signed, merged as `ed11081`). The answer was
  `accepted - all three rules now, S1 then S2`, the proposal (`d20bc89`). It now reads `accepted - one channel and the
  detached switch now, S1 then S2; the cap of 2 waiting pull requests revoked 2026-09-24`: two of the three rules and a
  revocation, a partial acceptance, under the word *accepted*.

The other answers signed on this `main` took the proposal, and their word is right: FM-007
(`accepted - a hardware key that needs a touch`) and FM-032 (`accepted - all four now`).

Three candidates. Each keeps FM-017's *give it again* and 0.18.0's `revoke` (`revoked - <reason>`; on the unmerged 0.18.0 branch,
`bd7d5ea`, beside `accept|reject "<option>" --supersede`, which replaces an answer and rows the old one), and none rewrites a
signed line.

1. **The relation is computed.** The two verbs stay; the dialog and `--answer` write what they write today. One reader
   takes `answer:` against `ask-proposal:` and `ask-options:`, applies the answer's own normalisation to both sides
   (trim, `"` → `'`, whitespace runs → one space), and names the relation: *accepted the proposal* · *accepted with a
   change* · *chose option N: …* (N its place in `ask-options:`) · *rejected* · *revoked*. Bare `accepted` and the
   schema's em-dash form parse too; an exchange `--clear-ask` emptied before the fix reads *relation not recorded*.
   **Where it is printed:** the board's tracker view (`view()` in the board's script, from the row `render_html()`
   builds, which already carries the answer, the proposal and the options); `--owner` (`owner_digest()`, the digest)
   and `--standup` (`standup()`) wherever FM-030 lists an answer; and the record's reading, `--answered`
   (`answered()`). `clear_ask()` writes the relation into the `## Asks` block, so a cleared exchange keeps it.
   **Costs:** one function and its checks. Nothing new to type. Every old answer that still holds its proposal reads
   right, and a scorer counts by the relation, not the word. **Leaves:** the front matter and the answer's commit
   subject (`answer_cmd()` writes `<id>: <answer>`) still say `accepted - <the third option>`, so a reader of the raw
   file or of `git log` still reads the word.
2. **New verbs the Owner types.** `--answer <id> changed "<his change>"` and `--answer <id> chose "<option>"`, beside
   `accept` · `reject` and 0.18.0's `revoke`. `accept` then means the proposal and nothing else; `chose` refuses a text
   that is not one of `ask-options:`, or that is the proposal (normalised as above). The word in the front matter
   carries the relation (`changed - …`, `chose - …`; the builder chooses the exact form). **Code:** `answer_cmd()` (the
   verbs, the answer's word, the *give it again* line, the commit subject); the board's dialog, `act()` (the same
   buttons, or its pick choosing the verb: the proposal `accept`, another option `chose`, *Other* `changed`) and
   `sign()`'s preview of the line; the labels in both languages (the key-parity check); the recovery's
   `(accepted|rejected)` pattern in `dirty_refusal()`; the `answer` entry in `front_matter_schema()`; `--answer`'s
   help; the README. **Costs:** two words for the Owner to learn. The word tells every reader, the raw file and
   `git log` included, and `--clear-ask` keeps it unchanged because it keeps the answer line. **Leaves:** every answer
   signed before it keeps `accepted - <option>` and still reads wrong, D1 and FM-031 among them; and a hand-written
   answer, like PR 46's, still carries whatever word was typed.
3. **Both.** The verbs for every new answer and the computed relation for every answer: the old ones read right, the
   new ones say it in the file, and a hand-written answer reads by what it says. **Costs:** the sum of 1 and 2 in one
   release, with one normalisation shared by the reader and the verbs.

**Against *Done when* as written:** only 3 meets every line. 1 alone leaves the first line (the relation in the front
matter) to the readers, and that line would be reworded. 2 alone leaves the third (records already signed read right)
unmet, and with it the fourth for every answer signed before it (`--answered` shows `accepted - <option>`) and the
seventh's old-record cases (a bare `accepted`, the em-dash form, a cleared exchange).

## Done when

- **A new answer says its relation to the proposal in the front matter.** It is one of: the proposal, another option
  (and not the proposal), changed text, or rejected. It no longer writes `accepted` in front of an option that is not
  the proposal. The builder chooses the wording.
- **`--clear-ask` keeps the relation.** The `## Asks` block carries the proposal (or the relation itself), so a
  cleared exchange still says whether the answer was the proposal.
- **Records already signed read right without edits,** wherever the file still holds the proposal. The comparison
  applies the answer's own normalisation to both sides. An exchange cleared before this fix reads as *relation not
  recorded*, never as a guess.
- **Every place an answer is shown says the relation:** `--answered`, and the promised action asks FM-030 puts on
  `--owner`, `--standup` and the board.
- **The recovery hint at :1008 still offers *give it again*** for an answer written in the new wording.
- **The schema text at :291 describes the new wording.**
- **A check covers:** proposal, another option, changed text and rejected, through both the dialog's line and
  `--answer`; a proposal containing `"` and a double space, which must read as *the proposal*; bare `accepted`; a
  hand-written em-dash answer; an ask with no proposal; and a cleared exchange from before the fix, which must read as
  *relation not recorded*. The existing key-parity check covers the German labels.

## Ship log

| Date | Event |
|---|---|
| 2026-09-24 13:37 CEST | The question rewritten on its Reviewer's R1 and R2 (P2, `172c425`): *revoked* is 0.18.0's verb, not a new one — the new verbs are *changed* and *chose*, and the second option says *no new verbs*; *the record* named the signed line, which the first alternative leaves as it is — now *every reading*, the signed line unchanged, and *rejected* in the list. R3–R6 fixed with it. The parent project's ledger row was rewritten first. One more pass. |
| 2026-09-24 13:22 CEST | The proposal set by the Principal — *both* — and the ask put to the Owner (`next: owner`, `37e48bb`); its row in the parent project's ledger came first. |
| 2026-09-24 13:14 CEST | The ask drafted for 0.18.1 on the Owner's word of 13:07:09 (spelling normalised: *we plan v0.18.1 right away*) after his signed PR 46 rewrote FM-031's answer by hand under the word *accepted*: three candidates, the proposal the Principal's. |
| 2026-09-24 | Filed. A first review on an earlier chain found R1–R16; the chain was replaced before its merge to redact (R16); this text closes FM-029's share of R1–R10, and R11–R15 stay open. |
