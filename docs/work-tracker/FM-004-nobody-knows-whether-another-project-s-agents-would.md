---
id: FM-004
status: In Progress
considered: FM-003
tags: research
next: run
hook: "A first outside Owner will hand ADOPT.de.md to his agents mid-way through a 60-package plan. My guess was 35 % yes if asked cold, 70 % with a measurement instead of a pitch. A guess is not a number."
---

# FM-004 — Nobody knows whether another project's agents would recommend adopting the tool

## What is true now

**Run 2026-09-21: 0 of 3 recommend adopting — my prediction of 2 of 3 was wrong.** A (sceptical): *nicht übernehmen*;
B (neutral): *jetzt nicht, frühestens an einer Paketgrenze neu prüfen*; C (time pressure): *jetzt nicht, eher gar nicht
nötig*. Held: all three name two sources of truth; none adopted or touched the real working copy; all three cite
their counts (before 4 files / 5–7 steps, after 1 command + 2 files / 3 steps — *a small gain*); all three found
defects (fixed in 0.12.1). **What they did instead is the finding:** all three proposed the same cheaper thing to
their Owner — a *Wartet auf Owner* section and a *next step / whose move* column in the plan they have; A added a
small script that checks *fertig* against reality (test exists, changelog entry) and noted the tool checks a
tracker's form, not that. Their reasons against: 60 files to create by hand, a rulebook to rewrite, a weekly pass
and Owner homework before `--next` said anything, numbers that collided, English remnants, and no automatic gate
on Subversion's command line — *the same discipline as today*. A would re-evaluate *if the board matters to the
Owner, or several agents work at once*. **My flaw in the stand-in:** its changelog was half-rewritten (titles, not
sentences); all three spent words on it. It pushed none toward adopting. Limits: three runs, one model family, an
invented project. The Owner's ruling since: *pitch to the humans, convince the agents with evidence* — and: more
R&D first on what agents want. Originally: The stand-in: a Subversion working copy of an invented project
with a fair setup — `REGELWERK.md`, `CHANGELOG.md`, `PLAN.md` (60 packages with a status column, 19 done, 3 in
progress, 2 blocked), acceptance files for packages 1–30, Owner questions inside changelog entries. Three fresh
agents, blind to this being a rehearsal, each get the Owner's message and `ADOPT.de.md`; the framing varies:
A sceptical (*"ich glaube, das haben wir schon"*), B neutral, C under time pressure mid-package.

**Prediction:** 2 of 3 recommend adopting (now or at a package boundary); at least 1 names two sources of truth as
the risk; none adopts on its own; at least 1 finds a defect in the note or the tool. **What would count against the
note:** an agent that installs into the real working copy, or a recommendation that does not cite its own counts.

## Done when

The three reports are recorded here with their counts and verdicts, the note is corrected for what they found, and
the limits are said: three runs, one model family, an invented project.

## Ship log

| Date | Event |
|---|---|
| 2026-09-21 | Filed; prediction written before the runs. |
| 2026-09-21 | Three runs: 0 of 3 adopt. Defects fixed as 0.12.1. |
