---
id: FM-184
status: Proposed
considered: FM-143, FM-163
tags: process
next: build
hook: "A change to a public skill can reach shoalmark/skills' main without the Owner's own signed commit. A required check there is to refuse any commit that touches a skill, or the check's own files, unless it is one."
---

# FM-184 — a change to a public skill can reach the skills repository's main without the Owner's own signed commit

Seat: the Planner (a1730572) · filed 2026-11-20, on the coordinator's word of that day.

## What is true now

**Filed 2026-11-20, Proposed; nothing is merged.** On the Owner's ruling of 20 November, a skill, or a change to one,
enters shoalmark/skills only by the Owner's own signed commit, which is its READY, after proof in our own use and an
eval with its numbers filed. The ruling names two means to hold it. The first is in force: by the Owner's signed
change to the organisation's roster of 20 November, no bot's push grant covers that repository, and each branch, pull
request and push there is the Owner's own act. The second is not: a required check on its main, to refuse any commit
that touches a skill unless it is the Owner's own signed commit. This tracker carries the check, whose lane started on
20 November, on the coordinator's word of that day.

- **Today,** at shoalmark/skills' main
  [`344ba36`](https://github.com/shoalmark/skills/commit/344ba36c0afec954260ce76d726512f255afe3c5): main takes
  changes only by pull request, merges them only by a merge commit, and requires the five `tests (…)` jobs. Nothing
  there checks who made or signed a commit, and the repository holds no signers file.

## Why

The public skills are where outsiders first meet this work and decide whether to trust it. A skill that reaches them
before it is proven costs more than any delay.

## The decision

1. **A required check on shoalmark/skills' main,** a lane of the tool team at the critical tier. In a pull request it
   refuses every commit that touches a protected path unless it is the Owner's own signed commit: authored and committed
   under the Owner's forge noreply address, and signed with a key that the base's signers file lists for it.
   - The protected paths: everything under `plugins/` and `.github/`, both marketplace files, and the check's own files.
   - The signers come from the base the request is judged against, never from its head. The judging code is the
     base's, and the head is read only as git objects.
2. **The change lands as one commit of the Owner's own,** signed. No bot makes a branch, a pull request or a push in
   shoalmark/skills. The Owner makes the check required after the merge.

## Done when

- [ ] The check's change is READY by its reader, and lands on shoalmark/skills' main as the Owner's own signed commit.
- [ ] The Owner makes the check required on that main.
- [ ] A pull request with an unsigned commit that touches a skill is refused by the check on the forge, measured once.

## Ship log

| Date | Event |
|---|---|
| 2026-11-20 | *What is true now* said neither of the ruling's two means was in force; the roster's had been since earlier that day, by the Owner's signed change, as the organisation's record has it. It now says so; the check is still to come. Records only. |
| 2026-11-20 | Renamed to the tool's slug of its title; *What is true now* says the two means are not in force yet, and where the lane's start is recorded. Records only. |
| 2026-11-20 | Filed, Proposed: the check that holds the Owner's ruling of 20 November on shoalmark/skills. Records only. |
