---
id: FM-142
status: In Progress
considered: FM-006, FM-023, FM-139
tags: process
next: build
triaged: 2026-11-03
tier: P1
hook: "FM-006 shipped with v0.20.2 at the sweep's close, and the gate builds only under a judged In Progress tracker. So v0.20.2's CHANGELOG section, its upgrade note, its release commit and the Owner's run sheet need a tracker of their own. This one holds them, and ships at v0.20.2's tag."
---

# FM-142 — v0.20.2's release text and release commit have no In Progress tracker to be built under, since FM-006 shipped

## What is true now

**2026-11-03 — filed and judged In Progress, P1, on the Owner's word of 3 November; it holds v0.20.2's release.**
[FM-006](FM-006-shoalmark-has-one-document-written-for-agents-the-humans-who.md) shipped with v0.20.2 at the sweep's
close. A commit that changes a path outside the tracker folder names the tracker it is built under, and the gate holds
that tracker judged and In Progress. So the release's own work had no tracker to name: its CHANGELOG section with the
upgrade note, its release commit, and the Owner's run sheet. This tracker holds them, and ships at v0.20.2's tag.
[FM-023](FM-023-a-plan-names-its-seats-their-estimates-and-when-the-person.md) keeps v0.20.x's allocation, and v0.20.3's
is [FM-139](FM-139-v0-20-3-s-rows-sit-in-fm-023-fm-006-and-fm-053-so-no-one.md).

## Why

A build commit under a closed tracker is refused, and one under a tracker it does not belong to makes a false record. A
release that is the person's to tag needs its own work held where its record can be read.

## Done when

- [ ] v0.20.2's CHANGELOG section, with its upgrade note, is committed, and every line in it is the Owner's read.
- [ ] The release commit is made: `VERSION` 0.20.2, both setup pages, and the landing's footer.
- [ ] The Owner's run sheet for v0.20.2 is committed, in v0.20.1's form.
- [ ] v0.20.2 is tagged, and this tracker ships with it.

## Ship log

| Date | Event |
|---|---|
| 2026-11-03 | Filed and judged In Progress, P1, on the Owner's word of 3 November, for v0.20.2's release: its CHANGELOG section, release commit and run sheet. Records only. |
