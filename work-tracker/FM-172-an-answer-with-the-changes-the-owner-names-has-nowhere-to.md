---
id: FM-172
status: Proposed
considered: FM-013, FM-029, FM-115, FM-167
tags: bug
next: owner
hook: "An ask's option can read yes, with the changes I name, but the Board's answer dialog opens its text box only for an answer outside the options, so the signed line records the option and no change. On 16 November an answer of that kind was given, and its change had to be recorded by a separate commit. The proposal, put to the Owner as FM-172-Q1: such an option opens the box and requires the changes, and the signed line carries both."
ask-id: FM-172-Q1
ask: "Do you take FM-172's fix into v0.20.3: an option that names changes opens the Board's text box and requires them, the answer's signed line records the option with the changes, and --answer takes them the same way?"
ask-kind: ruling
ask-since: 2026-11-16
ask-options: "yes, as proposed | no, not now"
ask-proposal: "yes, as proposed"
---

# FM-172 — an answer with the changes the Owner names has nowhere to name them, so the Board records the option alone

Seat: the Planner (a1730572) · filed 2026-11-16, on the coordinator's word of that day.

## What is true now

**Filed 2026-11-16, Proposed, with FM-172-Q1 put; nothing is built.** The Owner's word of 16 November, relayed by the
coordinator, asks for the fix: an answer "yes, with the changes I name" opens a box for the changes.

- **The dialog today** ([`shoalmark.py` L4366–L4381](https://github.com/shoalmark/shoalmark/blob/a409e829ed79d4597d266fdc18ebfea65d31a568/shoalmark.py#L4366-L4381)): each option of `ask-options:` is a radio
  button, and one more, "other:", stands for an answer outside them. The text box is enabled only for "other:", and the
  option picked goes into the command word for word. So an option that itself says the Owner names changes records
  that option, and the box for the changes is closed.
- **The command** (`--answer`, [L3366–L3378](https://github.com/shoalmark/shoalmark/blob/a409e829ed79d4597d266fdc18ebfea65d31a568/shoalmark.py#L3366-L3378)) takes one text after `accept`: an option, or a change
  of the Owner's own. It has no place for an option and its changes together.
- **How it reads** ([`answer_relation`, L1879–L1903](https://github.com/shoalmark/shoalmark/blob/a409e829ed79d4597d266fdc18ebfea65d31a568/shoalmark.py#L1879-L1903)): an option is read as "chose option N", a
  text that is no option as "accepted with a change". An option that names changes reads as chosen, with no change.
- **What it cost:** FM-166-Q3 was answered "yes, with the changes I name" on 16 November. The changes were in no
  signed line, so they were written into FM-166 by a separate commit, on the Owner's word confirmed in writing.

## Why

An answer is the Owner's signed word, and its changes are part of it. A dialog that lets the Owner pick "with the
changes I name" and then gives them nowhere to name them leaves the deciding part of the answer outside the signature.

## Decisions, for the Owner

All four are put as FM-172-Q1.

1. **The option that names changes:** an option of `ask-options:` that reads "with the changes I name" is such an
   option. Picking it opens the text box, and the dialog builds no command until the box holds the changes.
2. **The signed line:** the answer records the option and the changes together, as
   `accepted - <the option>: <the changes>`, in the one signed commit. The relation reads "chose option N", with the
   changes quoted after it.
3. **The command:** `--answer <id> accept "<the option>" "<the changes>"` takes the same two parts, and refuses such an
   option given without changes, naming why. Every other answer is written as today.
4. **The review:** critical, since it changes what the Owner's signed line records. The Board's labels change in
   English and German, and the Designer checks the dialog.

**Where it meets other trackers:**

- [FM-115](FM-115-the-owner-answers-each-ask-in-the-board-s-one-dialog-and-no.md) builds each ask's own view; that
  view takes this rule with it.
- [FM-167](FM-167-the-owner-s-act-on-an-ask-has-no-fixed-name-so-the-board.md) names the act and the dialog's first
  line; it does not touch the options.
- [FM-029](FM-029-the-answer-says-accepted-when-the-person-picked-another.md) computes each answer's relation; decision
  2 adds the quoted changes to it.
- [FM-013](FM-013-after-ok-the-answer-dialog-leaves-only-abort-and-says.md) holds the dialog's steps after OK, which
  are unchanged.

## Done when

Each item names its commit or pull request when it lands.

- [ ] **The Owner has answered FM-172-Q1.**
- [ ] **The dialog** opens the text box for an option that names changes and builds no command without them, with a
  test of the built command and the Designer's check, in English and German.
- [ ] **`--answer`** takes the option and the changes, writes them in the one signed line, and refuses the option
  alone, each with its test.
- [ ] **The relation** reads such an answer as the option chosen, with its changes quoted, with its test.
- [ ] **The critical review is READY.**

## Ship log

| Date | Event |
|---|---|
| 2026-11-16 | Filed, Proposed, with FM-172-Q1 put: an option that names changes opens the dialog's text box and requires them, and the signed line carries both. Records only. |
