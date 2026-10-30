---
id: FM-103
status: Proposed
considered: FM-033, FM-041, FM-053
tags: bug
hook: "An In Progress tracker that no pass has judged within the triage window sits under triage, still showing In Progress, and nothing on its row says why. The rule is right, but a person reads it as a bug. The Board should say on the row that it waits to be judged again, and since when."
---

# FM-103 — the Board doesn't say why an In Progress tracker sits in triage, so it reads as a bug

## What is true now

**Filed 2026-10-30 for v0.20.x; nothing is built.** On the Owner's word of 30 October, from their own Board: the
progress section held only three trackers, and triage held several that show their status as In Progress. "The reason
behind this is sound. We just have to work on how this is communicated to the user, so that they don't think it is a
bug and not a feature."

- **What happens:** an In Progress tracker that no pass has judged within `triage_days`, 7 by default, is listed under
  triage, with its status still "In Progress".
- **What's missing:** nothing on its row says that it waits to be judged again, or since when.
- **The rule stays.** Only its telling changes.
- **Open, for its design:** the mark on the triage row; or every In Progress tracker under progress, with the mark, and
  counted in triage.

## Why

A Board that shows a tracker in the wrong-looking place, with nothing to say why, teaches the person to distrust it.
The rule is sound, so the Board should tell it plainly.

## Done when

- [ ] Every In Progress row that the window moved says why, on its own row: that it waits to be judged again, and the
  date it was last judged.
- [ ] The progress and triage captions say the rule in a person's words, in English and German.
- [ ] The Owner's word on the words (FM-053), and the Designer's look on the rows.
- [ ] A class test: a tracker judged 8 days ago shows the mark, and one judged today doesn't. Its mutant is red.

## Ship log

| Date | Event |
|---|---|
| 2026-10-30 | Tagged `bug`, on the Owner's word of 30 October. Records only. |
| 2026-10-30 | Filed for v0.20.x, on the Owner's word of 30 October. Records only. |
