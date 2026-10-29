---
id: FM-086
status: Proposed
considered: FM-006, FM-023, FM-081, FM-027, FM-083
tags: process
hook: "A tracker here states a standing truth about the product, so every later piece of work fits under it and none of it ends it. Nothing makes a tracker finish: its Done when may be open-ended, reusing it is always the cheaper filing, and no point in a release asks it to ship or split."
---

# FM-086 — a tracker states one deliverable and closes when it ships, instead of collecting every later piece of work

## What is true now

**Filed 2026-10-29; nothing is built. Allocated to v0.20.3 on the Owner's word of 29 October, as the Auditor relays
it;** v0.20.3's allocation records it for the Owner's signed answer.

**The case, measured at main `d526547`:**
- [FM-006](FM-006-shoalmark-has-one-document-written-for-agents-the-humans-who.md) has been In Progress since
  22 September. It holds 1,249 lines (183 KB) and 72 ship-log rows: the site, the brand, the why page and the German
  rewrite all went in as parts of it. It ships at v0.20.2 for what it delivered, and stops growing.
- [FM-023](FM-023-a-plan-names-its-seats-their-estimates-and-when-the-person.md) is the same case for the plan: it
  holds every release's allocation, 40 KB in five tables.
- Of 80 trackers, 22 are In Progress. Five of them have been In Progress since 22 September.

**What it costs:** an agent that reads such a tracker spends its budget on history, and the Board's *In Progress*
says little about what is moving. The intent names "work that circles instead of finishing" among what the work must
never become.

**The design, on the Owner's word of 29 October:**
1. **A finite *Done when*.** Every tracker already has the section. Judging a tracker In Progress needs that section
   filled with observable states, and the release's closing pass reads it.
2. **A bound on reuse:** a part of an existing tracker only while that tracker is In Progress and its *Done when*
   already covers the part. Anything else is a new tracker that names the old one in `considered:`. This repository's
   contract adds one more condition: the part ships in the same release.
3. **Themes are tags, not epics.** The site or the German line is a theme: `tags:` marks it. `epic:` stays for a
   story that has its own *Done when*.
4. **The closing pass:** at each release, before its tag, every tracker with a commit in the release's range ships or
   splits.
   - **It ships** when its *Done when* holds, and its *What is true now* ends in a short final state. Its history stays
     in its ship log and in git.
   - **It splits** when work is left: the open part becomes a new tracker that names the old one, and the old one
     ships for what it delivered. Work already built ships under the tracker that built it, since its commits were
     judged under that one.
   - This repository's release run sheet stops on a touched tracker that does neither.
5. **Soft signals, never a refusal.**
   - The Board, `--triage` and `--next` raise one line where a tracker looks due to:
     - be split;
     - become an epic;
     - be closed and refiled as a new tracker;
     - or be parked.
   - Each signal has a default trigger, kept as a key in `shoalmark.toml`. Examples: *What is true now* past a size,
     In Progress past an age counted from when it was judged, many parts with no shipped one. The ship log, which only
     grows, triggers nothing.
   - The triaging seat answers in one line, *split*, *epic*, *close and new*, *park* or *keep*, with its reason. That
     line silences the signal until its cause changes.

## Why

A record that can be read back is one that finishes. Trackers that close keep each one short enough to read, keep
*In Progress* true, and give every release a list of what it delivered.

## Done when

- `--check` refuses a tracker judged In Progress with an empty *Done when*, and its test shows the refusal and the way
  through.
- The README's filing section states the reuse bound, and the contract states this repository's release condition.
- `--triage`, `--next` and the Board raise the soft signals with their default keys.
  - A one-line answer silences each signal, with its reason recorded, and each signal has a test.
  - No size or age ever refuses.
- v0.20.3's closing pass runs by these rules, and its records commit lists each touched tracker as shipped or split.

## Ship log

| Date | Event |
|---|---|
| 2026-10-29 | Filed, on the Owner's word of 29 October, for v0.20.3. Records only. |
