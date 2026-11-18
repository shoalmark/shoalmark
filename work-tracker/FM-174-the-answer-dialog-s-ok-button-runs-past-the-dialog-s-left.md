---
id: FM-174
status: Proposed
considered: FM-013, FM-115, FM-167, FM-172
tags: bug
hook: "On a phone, 320 px wide, the Board's answer dialog draws its OK button past the dialog's left edge: by about 21 px in German and 12.5 px in English. Found by the Designer's fidelity check of 18 November, on main as it stands; it is main's, not a lane's."
---

# FM-174 — the answer dialog's OK button runs past the dialog's left edge on a phone

Seat: the Planner (a1730572) · filed 2026-11-18, on the coordinator's word of that day.

## What is true now

**Filed 2026-11-18, Proposed; nothing is built.** The Designer's fidelity check of 18 November rendered the answer
dialog on main at `df511a7`, beside a lane that changes the same dialog
([FM-172](FM-172-an-answer-with-the-changes-the-owner-names-has-nowhere-to.md)), and found this on main itself.

- **What the check measured:** at 320 px the dialog's OK button runs past the dialog's own left edge, by about 21 px
  in German (rendered with Other picked) and 12.5 px in English (the check's fit probes).
- **Where it is not:** FM-172's lane changes the dialog's box, its hint and a cue on the option's row, and leaves its
  buttons as they are. This item is kept apart so that it does not ride in that lane.
- **Seen beside it, not filed here:** a picked radio shows a bare dot rather than a radio mark. That is another item if
  it is filed.

## Why

OK is the Owner's one act in the dialog. 320 px is one of the widths the suite's phone check renders the Board at, and
a button drawn past the dialog's edge there reads as broken at the moment the Owner answers.

## Done when

Each item names its commit or pull request when it lands.

- [ ] **The dialog's buttons stay inside the dialog** at 320, 360 and 390 px, in English and German, light and dark,
  with a check of the rendered widths.
- [ ] **The Designer's check reads READY** beside the review.

## Ship log

| Date | Event |
|---|---|
| 2026-11-18 | Filed, Proposed: on a phone the answer dialog's OK button runs past the dialog's left edge, found on main by the Designer's check. Records only. |
