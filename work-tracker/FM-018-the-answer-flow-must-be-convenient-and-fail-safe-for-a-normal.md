---
id: FM-018
status: Proposed
considered: FM-012, FM-013, FM-016, FM-017, FM-007, FM-005
tags: bug
next: wait
triaged: 2026-09-23
rank: 3
tier: P1
hook: "Answering takes a normal user through branch switches, a checkout a seat's worktree may hold, an older pinned tool on the wrong branch, leftovers from a failed run, a silent minute, a board that offers an answered ask again and a dialog ending in abort. The Owner: *\"Normal\" users won't like this — we have to make this convenient and fail-safe.* The requirement: he answers from wherever he stands, and his checkout is never switched, dirtied or left behind."
---

# FM-018 — The answer flow must be convenient and fail-safe for a normal user

## What is true now

**Filed 2026-09-23; nothing is built as this tracker, and no design is chosen — the Owner rules.** Four of its parts are
filed on their own: [FM-012](FM-012-a-load-spawns-git-once-per-tracker-and-answer-is-silent-for.md) (the silent
minute), [FM-013](FM-013-after-ok-the-answer-dialog-leaves-only-abort-and-says.md) (the dialog that ends in abort),
[FM-016](FM-016-an-answered-ask-still-shows-as-unanswered-on-the-branch-the.md) (the answered ask offered again) and
[FM-017](FM-017-a-failed-answer-leaves-its-writes-behind-and-the-next-answer.md) (the leftovers of a failed run). FM-012,
FM-013 and FM-017 are built for 0.17.4; FM-016 waits for a ruling. What none of them changes is the shape underneath:
`--answer` works **in the Owner's own checkout**, so it must switch his branch, it runs his checkout hook, and whatever it
writes lands in his tree.

The Owner, in his words: *"Keep in mind that "Normal" users won't like this - We have to make this convenient and
fail-safe."*

**One morning's evidence, as he met it:**

1. he had to switch branches by hand to reach the branch that carries the ask;
2. a seat's worktree held that branch, so his switch failed;
3. he answered from the wrong branch, running an older pinned copy of the tool, and the gate refused the answer;
4. the failed run's leftovers blocked his next answer, and he cleaned them up by hand (FM-017);
5. each answer ran about a minute with no output (FM-012);
6. the board on his main branch offered an ask he had already answered (FM-016);
7. the dialog's last button was *abort* (FM-013).

**Open, from [FM-013](FM-013-after-ok-the-answer-dialog-leaves-only-abort-and-says.md) (shipped in 0.17.4):** the
dialog's second screen is not proven with a real clipboard in the Owner's browser, at phone width, or against the live
signing page, which is served only once the documentation site is public.

**The Principal's candidate, NOT chosen:** `--answer` finds the branch that carries the ask, commits in a **temporary
`git worktree`** of that branch — signed, with the Owner's identity and key — pushes `answer/<id>`, and removes the
worktree whether it succeeded or failed. No switch, no checkout hook in his tree, nothing left behind; and a branch a
seat's worktree holds is no obstacle, because the answer never checks it out.

## Why

An answer is the Owner's one act in the whole flow, and every step above is a place where a normal user stops and
concludes the tool is broken. A process he has to nurse through git is a process he will route around — and an answer
routed around the gate is the one thing the gate exists to prevent.

## Done when

- The Owner has ruled on the design — the candidate above or another — and it is recorded here.
- He answers from whichever branch he stands on, and his checkout is never switched, never dirtied and never left
  behind, whether the answer succeeds or fails.
- The seven points above are each either gone or named here with why they remain.

## Merged in from FM-016 — the answered ask offered again (2026-09-23, the first triage pass)

*FM-016's state when merged:*

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

## Ship log

| Date | Event |
|---|---|
| 2026-09-23 | **FM-016 merged in by the first triage pass** — its open scope (part b: the answered ask still offered on the branch the Owner returns to) lives here now; E0 at the 09-24 sitting decides whether any of the flow is built. |
| 2026-09-23 | FM-013's three unproven points joined the open items (R9). |
| 2026-09-23 | Filed from the Owner's morning and his words; FM-012, FM-013, FM-016 and FM-017 named as its parts. The design is his to rule. |
