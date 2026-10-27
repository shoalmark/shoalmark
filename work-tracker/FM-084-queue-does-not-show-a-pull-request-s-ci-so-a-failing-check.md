---
id: FM-084
status: Proposed
considered: FM-031, FM-082
tags: process
next: owner
hook: "--queue does not show a pull request's CI, so a failing check is found on the forge by hand"
ask: "Is FM-084's check word in --queue allocated to v0.20.3, as FM-084's section The allocation, for the Owner sets out?"
ask-kind: ruling
ask-since: 2026-10-27
ask-options: "yes, v0.20.3 | no: a later release"
ask-proposal: "yes, v0.20.3"
---

# FM-084 — --queue does not show a pull request's CI, so a failing check is found on the forge by hand

## What is true now

**Filed 2026-10-27, Proposed, as a quick win for v0.20.3, on the Owner's word of 27 October as relayed by the Auditor;
nothing is built.** `--queue` (FM-031's S2) lists every open pull request with one action, the pull requests merged or
closed in the last day, and the pushed branches that have no pull request. `--owner` and `--standup` end with the same
queue. Its query to the forge, `QUEUE_FIELDS` (`shoalmark.py:2604` at `6782cda`), asks for no check status. So the
queue can offer *merge* for a pull request whose CI is failing, and the person finds that on the forge by hand.

It is filed on its own, not as a slice of FM-031, so that it can be allocated to v0.20.3 alone. FM-031 owns the queue
as built.

## The fix, as proposed

1. **Ask for the checks:** add `statusCheckRollup` to the fields `--queue` reads for its open pull requests.
2. **One word per open pull request:** failing, running, passing, or none.
3. **A failing check changes its one action,** so that pull request is not offered as next to merge.
4. **Where the forge does not answer,** `--queue` says so in one line, as it does today.
5. **No Board change, and no new contact with a remote:** `--queue` already reads the forge. A check's name, if it is
   printed at all, is cleaned the same way as a title.
6. **A class test with mutants,** and every new or changed string, EN and DE, in the words list.

## Why

The queue is where the person decides what to merge next. A failing check it cannot see sends them back to the forge
to read each pull request by hand, which is what `--queue` was built to end.

## Done when

- `--queue` prints one check word for each open pull request, and a failing check turns *merge* into a wait.
- The class test refuses a mutant for each word and for the changed action.
- The strings are in the words list, EN and DE.

## The allocation, for the Owner

- **The question:** is the check word in `--queue` allocated to v0.20.3?
- **The proposal:** yes. It is small, reads nothing new from the network, and changes no Board.
- **The options:** yes, v0.20.3; or no, a later release.

## Ship log

| Date | Event |
|---|---|
| 2026-10-27 | Filed, Proposed, a quick win for v0.20.3 on the Owner's word of 27 October, with one ruling ask: its allocation to v0.20.3. |
