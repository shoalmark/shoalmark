---
id: FM-004
status: In Progress
considered: FM-003
tags: research
next: wait
triaged: 2026-09-23
tier: P3
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

## Second round — the Owner's question: *what do agents want, and how do we get a better-performing human owner?*

The same three agents, resumed, asked four open questions in the Owner's voice. **Predicted before they answered:**
the top brake is the Owner's decision latency; their asks are answer-in-one-place, priorities, a definition of
done; what flips the verdict is *no migration* plus *the Owner uses it*, not a feature.

| | Result |
|---|---|
| Top brake | **held, 3 of 3, by a wide margin:** unanswered Owner questions — one question open since three days holds three packages; *"rund ein Drittel unserer aktuellen Arbeit"*; it also caused three half-finished packages. Bookkeeping was named by none. |
| Asks of the Owner | **held, 3 of 3:** answer within one working day, provisionally if need be (*"vorläufig X"*) · in writing — a phone answer does not exist for a session without memory · name ONE priority · really look at finished screens · two sentences of *"gut ist es, wenn …"* per coming package. New: say what matters with each answer, so similar questions need no asking (B: halves the questions); never rewrite history, append a correction (C); rule once how many packages may run in parallel (C). A: three of five brakes are the agents' own discipline. |
| What flips the verdict | **half held.** 3 of 3: a change to the tool alone flips nothing — *"sie erzeugen keinen Bedarf"*, *"das Werkzeug ist nicht der Engpass"*. The flip is in the situation: several agents at once, so one plan table becomes a conflict (A); or the Owner would look at a board daily but does not open `PLAN.md` (B, C). *No migration* only makes it cheaper. |
| What no file and no board does | 3 of 3, unprompted: *"Eine Datei ruft Sie nicht an, und eine Tafel müssen Sie auch erst öffnen."* — nothing **pushes**, and nothing **enforces**: the gate checks a tracker's form, not that the test it names exists. |
| Their protocol | two to four weeks with twenty lines in the plan they have (*Wartet auf Owner*: question, date, what it blocks, *our proposal if no answer comes*); if the median age of open Owner questions stays above one working day **and** the Owner prefers a page in the browser — switch at a package boundary, keeping their numbers. Measures offered: median age of open Owner questions · packages in progress at once · minutes to a fresh session's first useful move · overwritten status lines per week. |

## Part B — the probe's next version, and onboarding through the agents (2026-10-08)

The Owner's work package after v0.19.1, in two lanes that meet at the landing page's dialog. **B1, the landing page,**
in English and German from one template: a primary button that copies a probe prompt and opens a dialog, built behind a
switch that stays off until the probe has passed; a secondary "How it works"; and figures generated from the repository
when the site is built. **The probe lane** rewrites ADOPT.md and ADOPT.de.md as an honest evaluation of fit that may end
in "no fit": prerequisites first (Python and git on every machine, and svn's command-line tools on Subversion), the
human's yes before it runs, the working copy read-only within a time and file budget, the one first result that fits
where the project stands, a report of benefit and cost, the yes-path at a work-item boundary, an optional feedback
report the human sends, and the probe in the project's language. Nothing in it says or implies that shoalmark scans for
security problems or data leaks, and it fits one person in charge. Nothing goes outside before it passes a fixed rule:
a set number of consecutive clean end-to-end runs, from the landing page's button to the feedback file; any failure is
fixed, and the count restarts.

## Done when

The three reports are recorded here with their counts and verdicts, the note is corrected for what they found, and
the limits are said: three runs, one model family, an invented project.

## Ship log

| Date | Event |
|---|---|
| 2026-09-21 | Filed; prediction written before the runs. |
| 2026-09-21 | Three runs: 0 of 3 adopt. Defects fixed as 0.12.1. |
| 2026-09-21 | Second round: the brake is the Owner's latency, 3 of 3; a tool change alone flips nothing. |
