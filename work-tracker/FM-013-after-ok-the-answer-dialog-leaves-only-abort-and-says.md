---
id: FM-013
status: In Progress
considered: FM-007, FM-008
tags: bug
next: review
hook: "In the board's answer dialog, OK copies the command, prints one line of instruction above it and disables itself — the one button left is abort, which reads as undoing what was just decided. Nothing says where to run the command, what it does, what success looks like or what to do when signing fails. The Owner: a second screen that explains how to sign, and only a Done button."
---

# FM-013 — After OK the answer dialog leaves only abort, and says nothing about signing

## What is true now

**Built 2026-09-23 on `fix/0.17.4-the-answer-says-what-it-does`; merged 2026-09-23 (#12), released as 0.17.4.** OK now
replaces the dialog's content with a second screen: *Sign your answer* · the command in a monospace block with *Copy
again* · where (a terminal, this repository, the branch that carries the ask — named: the board now knows the branch it
was built from) · what it does, four steps, and that it prints each and may take a while · what success looks like —
the two lines the command ends with, with this answer's words in them · how to check (`git log -1 --format=%G?
answer/<id>` prints `G`) · if it fails, the signing page. **Done** is the only button in its menu; Esc closes the dialog
as before. *Copied* appears only when `navigator.clipboard.writeText` resolved; otherwise it says to select and copy.
Every string is a label, in English and in the shipped German table; the old `answer.run` label is gone with the line it
drove. **Proven in a headless browser by the suite**: OK pressed, screen two read as rendered, Done clicked and the
dialog closed, the clipboard stubbed present and absent. **Not proven:** a real clipboard in the Owner's browser, a
phone-width layout, and the signing page itself, which is served only once the documentation site is public. **What is
left:** his eye on the three points not proven.

Reported by the Owner after answering from the board.

**What the dialog did at 0.17.3.** `accept` or `reject` opens a `<dialog>` with the question, the choices and the box.
OK (*"OK — give me the command"*) runs `f.onsubmit`: it writes the command to the clipboard, sets one paragraph to
*"Copied. Run this in the repository; …"* plus the command, and **disables OK**. What is left is one enabled button —
**abort**. After a decision, *abort* reads as *take it back*; the dialog has no way to say *I am done here*.

It also says *Copied* whether or not anything was copied: `navigator.clipboard?.writeText(line)` is not awaited, and a
board opened from `file://` may have no clipboard at all. And nothing tells him where to run the command, what it will
do, how long it takes, what the end looks like or what to do when it fails for want of a signing key.

**The Owner's design, in his words:** *"After the accept a new screen in the dialog opens that shows / explains the User
how to sign the answer … you have also more room in the dialog, so can be more detailed. Only a "Done" button to close
the dialog."*

## Why

The dialog is where the Owner decides; the terminal is where he signs. The hand-over between them is the one moment
the flow depends on him following instructions he has never read — and today the instructions are one line, and the
only button left looks like a way to undo the decision.

## Done when

- Screen one is unchanged: the ask, its choices, OK and abort.
- OK switches the dialog to **screen two**:
  - a heading — *Sign your answer*;
  - the exact command in a monospace block, with **Copy again**; the dialog says *Copied* only when
    `navigator.clipboard.writeText` resolved, and otherwise tells him to select and copy it;
  - **where** to run it: a terminal, in this repository, on the branch that carries the ask — named, when the board
    knows the branch it was built from;
  - **what it does**, step by step: cuts `answer/<id>` from the current branch · writes `answer:` `answered:`
    `answered-by:` · commits signed with his key · pushes — and that it prints each step and may take a while;
  - **what success looks like**: `<id> answered: …`, then `signed, on answer/<id>, pushed`;
  - **how to check**: `git log -1 --format=%G? answer/<id>` prints `G`;
  - **if it fails** for want of a signing key: the signing page.
  - One button, **Done**, which closes the dialog; Esc closes it too.
- Every new string goes through the board's labels and into every language table the tool ships (English built in,
  German in `examples/de/labels.yaml`).
- The built board carries screen two's strings and exactly one button on it; where the suite can open the board in a
  headless browser, it drives OK and reads screen two as rendered.

## Ship log

| Date | Event |
|---|---|
| 2026-09-23 | Merged (#12), released as 0.17.4. |
| 2026-09-23 | Built: the second screen, Done alone in its menu, *Copied* only when it was; labels in English and German. Driven in a headless browser by the suite. |
| 2026-09-23 | Filed from the Owner's report and his design for the second screen. |
