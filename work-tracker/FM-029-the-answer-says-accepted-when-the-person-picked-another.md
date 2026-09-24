---
id: FM-029
status: Proposed
considered: FM-008, FM-013, FM-014, FM-017, FM-018, FM-030
tags: bug
next: review
hook: "The person picked the third of three options, not the proposal, and the signed record reads `accepted - <the third option>`. Read alone, the word says he agreed with the seat, and a fleet that counts how often the person takes the proposal counts this answer the wrong way."
---

# FM-029 — The answer says accepted when the person picked an option other than the proposal

## What is true now

**Filed 2026-09-24; nothing is built.** Found on 0.17.7 in a consumer repository. The lines below are from 0.17.8
(`v0.17.8` = `62db9f8`; `main` at `cdd6e3f`). Reviewed at `10d5895`, NOT READY (R1–R10, the review file under
`evidence/reviews/`); this text closes them.

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
| 2026-09-24 | Filed. Reviewed at `10d5895`: NOT READY, R1–R10 (two of them FM-030's alone); this text closes R1–R4 and R10's share here. |
