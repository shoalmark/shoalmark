---
id: FM-086
status: Proposed
considered: FM-006, FM-023, FM-081, FM-027, FM-083, FM-055
tags: process
epic: FM-089
hook: "Done here has meant a merged pull request, and a tracker has meant a theme, so trackers never finish: every later piece of work fits under a standing truth, and nothing asks it to end. When agents merge many pull requests a day, a done that matches one pull request or one tracker tells nothing. Done must be an outcome on the default branch, checked by the commits that met it."
---

# FM-086 — a tracker states one deliverable and closes when it ships, instead of collecting every later piece of work

## What is true now

**Filed 2026-10-29; nothing is built. Allocated to v0.20.3 on the Owner's word of 29 October, as the Auditor relays
it;** v0.20.3's allocation records it for the Owner's signed answer. **Its heart is shoalmark's definition of done.**
The Owner calls it the most valuable part of this work.

**The case, measured at main `d526547`:**
- [FM-006](FM-006-shoalmark-has-one-document-written-for-agents-the-humans-who.md) has been In Progress since
  22 September. It holds 1,249 lines (183 KB) and 72 ship-log rows: the site, the brand, the why page and the German
  rewrite all went in as parts of it. It ships at v0.20.2 for what it delivered, and stops growing.
- [FM-023](FM-023-a-plan-names-its-seats-their-estimates-and-when-the-person.md) is the same case for the plan: it
  holds every release's allocation, 40 KB in five tables.
- Of 80 trackers, 22 are In Progress. Five of them have been In Progress since 22 September.
- **The Owner's reason:** in a project where people ship, the merged pull request was the done. With agents it is not:
  they ship too fast, and repositories that merge a thousand pull requests a week show that done must not match a
  single pull request or a single tracker.

### The definition of done

1. **Done is an outcome, not a merge,** at three levels:
   - **a tracker** is done when every item of its *Done when* holds on the default branch;
   - **a lane** is done when it is merged;
   - **a pull request or a commit** is done when it is merged, and nobody counts them.
2. **The *Done when* is a checklist of observable states.**
   - Each item is met by the commit that met it, written `- [x] <state> · <sha>`. An open item is `- [ ] <state>`.
   - `--check` verifies that each named commit is on the default branch, so a false claim is refused. That is a check
     of a fact, not a limit.
3. **Many lanes per tracker, shown as progress.** The Board and `--next` show "Done when: 2 of 3 · 1 lane open", and
   never a count of pull requests.
4. **No reopening.** What comes back after a tracker shipped is a new tracker, naming the old one in `considered:`.
5. **A tracker is sized to a decision.**
   - What one pull request would finish in an hour is a task in a lane, not a tracker.
   - *Done* (every item met on the default branch) comes before *Shipped* (in a tagged release). Each release's closing
     pass turns *Done* into *Shipped*.

### How a tracker stays one deliverable

- **The reuse bound:** a part of an existing tracker only while that tracker is In Progress and its *Done when*
  already holds an item for the part. Anything else is a new tracker that names the old one in `considered:`. This
  repository's contract adds one condition: the part ships in the same release.
- **Themes are tags, not epics.** The site or the German line is a theme: `tags:` marks it. `epic:` stays for a story
  with a *Done when* of its own.
- **The closing pass:** at each release, before its tag, every tracker with a commit in the release's range ships or
  splits. This is the one hard rule.
  - **It ships** when it is done. Its *What is true now* ends in a short final state, and its history stays in its ship
    log and in git.
  - **It splits** when items are open: they become a new tracker that names the old one, and the old one ships for the
    items it met. Work already built ships under the tracker that built it, since its commits were judged under that
    one.
  - This repository's release run sheet stops on a touched tracker that does neither.

### The signals, never a refusal

The Board, `--triage` and `--next` raise one line where a tracker looks due for a move. Each signal has a default
trigger, kept as a key in `shoalmark.toml`. The ship log, which only grows, triggers none of them.

| Signal | What raises it, by default |
|---|---|
| **close, it's done** | every *Done when* item is met with a commit on the default branch, and no open branch or pull request names the tracker |
| **split** | its *Done when* holds items that ship in different releases, or its *What is true now* has grown past a size |
| **epic** | its parts each carry a *Done when* of their own |
| **close and new** | it has been In Progress past an age, counted from when it was judged, and its *Done when* has been rewritten since |
| **park** | no commit has named it for a while, and nothing it holds is blocked on someone else |

The triaging seat answers in one line: *done*, *split*, *epic*, *close and new*, *park* or *keep*, with its reason.
That line silences the signal until its cause changes. No signal ever refuses.

## Why

A record that can be read back is one that finishes. A done that is an outcome, met by named commits on the default
branch, keeps each tracker short, keeps *In Progress* true, and gives every release a list of what it delivered. It
also holds when agents merge more pull requests than anyone reads.

## Done when

- [ ] `--check` reads every tracker's *Done when* as a checklist, and refuses an item marked met whose commit is not on
  the default branch. A test shows the refusal and the way through.
- [ ] `--check` refuses a tracker judged In Progress whose *Done when* holds no item.
- [ ] The Board and `--next` show each tracker's progress, as in "Done when: 2 of 3 · 1 lane open", and no count of
  pull requests anywhere.
- [ ] A tracker whose every item is met reads as done on the Board, and the closing pass turns it to Shipped at the
  release that carries it.
- [ ] The Board, `--triage` and `--next` raise the five signals, each with its default key in `shoalmark.toml`.
  - A one-line answer (*done*, *split*, *epic*, *close and new*, *park*, *keep*) silences each signal until its cause
    changes.
  - Each signal has a test, and none refuses.
- [ ] The README and the agents' contract state the definition of done at its three levels, the checklist, no
  reopening, the reuse bound and themes as tags.
- [ ] v0.20.3's closing pass lists each tracker the release touched as shipped or split, and its run sheet stops on
  one that is neither.

## Ship log

| Date | Event |
|---|---|
| 2026-10-29 | Filed, on the Owner's word of 29 October, for v0.20.3. Records only. |
| 2026-10-29 | The definition of done, its heart, and the whole signal list, on the Owner's word of 29 October. Records only. |
