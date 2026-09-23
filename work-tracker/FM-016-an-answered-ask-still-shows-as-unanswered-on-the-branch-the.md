---
id: FM-016
status: Closed
considered: FM-008, FM-012, FM-014, FM-005
tags: bug
next: wait
triaged: 2026-09-23
hook: "After `--answer` the Owner switches back to his main branch, and that branch's board still shows the ask with accept and reject: the answer lives on `answer/<id>` and on the ask's branch until a merge brings it to main. Clicking again sends him to a second `--answer`, which is refused with advice to delete the branch that carries his answer."
---

# FM-016 — An answered ask still shows as unanswered on the branch the Owner returns to

Closed — merged into [FM-018](FM-018-the-answer-flow-must-be-convenient-and-fail-safe-for-a-normal.md), 2026-09-23

## What is true now

**Filed 2026-09-23; nothing is built, and no way forward is chosen — the Owner rules later.**

**What he sees.** `--answer <id>` cuts `answer/<id>` from the branch that carries the ask, commits the answer there and
pushes it. The Owner then goes back to his main branch. The board there is built from main's trackers, where the ask
has no answer yet — so `<id>` is still in *waiting for you*, with accept and reject, until a merge brings the answer
in. The Owner, in his words: *"A user would now be confused because <id> shows as unanswered while they just have
answered in the last step — this is something we have to figure out later."*

**What a second click does, reproduced here on 0.17.3** in a scratch repository — answer from the ask's branch, switch
to `main`, answer again:

```
--answer: `answer/ap-001` exists and its tip does not carry this ask — it was cut from another branch or the ask has
changed since. Delete it (`git branch -D answer/ap-001`) or answer from the branch that carries the ask
```

The refusal is right to stop, and wrong in what it says: the branch **does** carry the ask, and the advice is to delete
the branch holding the answer he just gave. One line on the way: the tip test compares the tip's raw `ask:` value,
quotes included, with the tracker's unquoted one, so a quoted ask never reads as carried — every existing
`answer/<id>` is refused this way, whichever branch it was cut from.

**Candidates, none chosen:**

- **(a)** the board reads the `answer/*` branches, local and remote-tracking, and in place of the buttons shows
  *answered on `answer/<id>`, not merged yet*;
- **(b)** `--answer` refuses when `answer/<id>` already exists and says what it is — an answer given and not yet
  merged — instead of advising its deletion;
- **(c)** the answer lands where the board is read.

## Why

The board is where the Owner decides, and it is the first thing he sees after answering. An answer he has just given
shown back to him as a question is an invitation to answer twice, and the command he would then run tells him to
destroy the first answer.

## Done when

The Owner has ruled which of (a) · (b) · (c), or another, and it is built: on the branch he returns to after
answering, an ask he has answered is not offered to him again as unanswered, and a second `--answer` on it never
advises deleting the branch that carries the first.

## Ship log

| Date | Event |
|---|---|
| 2026-09-23 | **Closed — merged into FM-018 by the first triage pass:** its whole open scope (the answered ask offered again on the branch the Owner returns to) is FM-018's part (b); the scope moved there. |
| 2026-09-23 | Filed from the Owner's report; the second click reproduced on 0.17.3 in a scratch repository. Not built — the Owner rules. |
