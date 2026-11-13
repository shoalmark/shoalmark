---
id: FM-167
status: Proposed
considered: FM-013, FM-029, FM-050, FM-115, FM-149, FM-160
tags: process
next: owner
hook: "The Owner's act on an ask has no fixed name, and the Board's answer dialog opens with Your decision is made. before the commit that records it exists. The imagery round of 13 November screened the words: answer and decision pass, while ruling, approval and sign-off fail. The act is called answer, the dialog says Your answer is ready., and the kind label is put to the Owner as FM-167-Q1, proposing to keep DECISION. No release is named."
ask-id: FM-167-Q1
ask: "Does the Board keep DECISION as the label of the ask kind ruling, or relabel it DIRECTION, with the kind key ruling kept as it is?"
ask-kind: ruling
ask-since: 2026-11-13
ask-options: "keep DECISION | DIRECTION"
ask-proposal: "keep DECISION"
---

# FM-167 — the Owner's act on an ask has no fixed name, so the Board says a decision is made before anything is recorded

Seat: the Planner (27f31560) · filed 2026-11-13, on the Auditor's word of that day.

## What is true now

**Filed 2026-11-13, Proposed, with FM-167-Q1 put; no release is named, and nothing is built.** It acts on the imagery
round of 13 November, whose record is
[FM-160's evidence](evidence/FM-160/go-to-market-round-imagery-and-the-owners-act-2026-11-13.md) (its Q3).

- **The base today:**
  - The Board's answer dialog opens with "Your decision is made." before the terminal runs its command:
    `answer.sign.intro`
    ([`shoalmark.py` L4725](https://github.com/shoalmark/shoalmark/blob/22ccfc83baea11cc78ae044f0f072abdb40ca136/shoalmark.py#L4725))
    and `answer.give.intro`
    ([L4743](https://github.com/shoalmark/shoalmark/blob/22ccfc83baea11cc78ae044f0f072abdb40ca136/shoalmark.py#L4743)).
    The German lines open "Deine Entscheidung steht."
    ([`examples/de/labels.yaml` L167 and L189](https://github.com/shoalmark/shoalmark/blob/22ccfc83baea11cc78ae044f0f072abdb40ca136/examples/de/labels.yaml#L167-L189)).
  - Until that command runs, nothing is recorded: "In the record, an answer counts only as a commit"
    ([`docs/index.md` L28](https://github.com/shoalmark/shoalmark/blob/22ccfc83baea11cc78ae044f0f072abdb40ca136/docs/index.md#L28)).
  - The ask kind `ruling` reads "a decision of intent" in the field table
    ([L1004](https://github.com/shoalmark/shoalmark/blob/22ccfc83baea11cc78ae044f0f072abdb40ca136/shoalmark.py#L1004)).
    The Board labels it DECISION (`ask.ruling`,
    [L4755](https://github.com/shoalmark/shoalmark/blob/22ccfc83baea11cc78ae044f0f072abdb40ca136/shoalmark.py#L4755)),
    beside YOUR HANDS, EVIDENCE COULD SETTLE IT and ONE CLICK. The design guide chose that word
    ([L276](https://github.com/shoalmark/shoalmark/blob/22ccfc83baea11cc78ae044f0f072abdb40ca136/brand/design-guide.md#L276)).
  - The public pages call the act "your answer". "Your decisions on record" names what answers settle
    ([`docs/index.md` L10](https://github.com/shoalmark/shoalmark/blob/22ccfc83baea11cc78ae044f0f072abdb40ca136/docs/index.md#L10)).
    No page under `docs/`, `README.md` or `overrides/` names the act a ruling, an approval or a sign-off.
- **What the round found** (its Q3):
  - **the recount:** 49 answers on record, 47 of them with a relation: 34 accepted the proposal, 9 accepted with a
    change, 3 chose another option, and 1 rejected. All 13 asks that state a kind state `ruling`;
  - **the words:** *answer* and *decision* pass both gates. *Ruling* fails as a court's word claiming finality,
    *approval* as the forge's merge approval and as mere consent to the seat's proposal, and *sign-off* as a typed
    trailer claiming a signature's proof. *Accept* passes only as the button's verb;
  - **the kinds need no split:** the act is the same on every kind, and the relation already records how each answer
    went.

## Why

The Owner's act on an ask is one act on every kind: an answer, and its relation records how it went. A word that claims
more misdescribes it: a court's ruling, a merge's approval, a signature's sign-off. A dialog that says the decision is
made before the commit exists says what the page cannot show.

## Decisions, for the Owner

1. **The Owner's act on an ask is called "answer"** on the public pages and on the Board.
2. **The dialog's first line:** "Your decision is made." becomes "Your answer is ready." in `answer.sign.intro` and
   `answer.give.intro`, and the sentences after it stay. The German line follows a native read.
3. **Words the public pages never use for the Owner's act:** ruling, approval and sign-off. *Accept* names only the
   button's verb. *Decision* stays for what an answer settles.
4. **The kind label,** put as FM-167-Q1:
   - **keep DECISION,** at no cost. This is the proposal;
   - **or DIRECTION,** at the record's count: the English label (`ask.ruling`, L4755), the `--standup` heading
     ([L2637](https://github.com/shoalmark/shoalmark/blob/22ccfc83baea11cc78ae044f0f072abdb40ca136/shoalmark.py#L2637)),
     the German label (`examples/de/labels.yaml` L153, after a native read), and five lines of the design guide (L257,
     L276, L336, L379 and L381), which change only by a signed answer.
5. **The kind key `ruling` is not renamed:** the trackers and the field table keep it.
6. **The kinds are not split.**

No release is named.

## Done when

Each item names its commit or pull request when it lands.

- [ ] **The Owner has answered FM-167-Q1.**
- [ ] **`answer.sign.intro` and `answer.give.intro` open "Your answer is ready.",** with the tests that hold the
  labels; the German lines after a native read.
- [ ] **The kind label reads as answered,** in English and German, on the Board and in `--standup`; with DIRECTION, the
  design guide's five lines by a signed answer.
- [ ] **No public page names the Owner's act a ruling, an approval or a sign-off,** checked across `docs/`,
  `README.md` and `overrides/`, the German pages included.
- [ ] **The review is READY.**

## Ship log

| Date | Event |
|---|---|
| 2026-11-13 | Filed, Proposed, with FM-167-Q1 put: the Owner's act is called answer, and the dialog's first line becomes Your answer is ready.; the kind label is asked, proposing to keep DECISION. No release. Records only. |
