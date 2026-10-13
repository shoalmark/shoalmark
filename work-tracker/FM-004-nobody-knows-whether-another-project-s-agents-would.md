---
id: FM-004
status: In Progress
considered: FM-003
tags: research
next: review
triaged: 2026-09-23
tier: P3
hook: "A first outside Owner will hand ADOPT.de.md to his agents mid-way through a 60-package plan. My guess was 35 % yes if asked cold, 70 % with a measurement instead of a pitch. A guess is not a number."
ask: "What exact replacement text do you want for RV-2734 in #154, removing the withdrawn requirement for git on every machine?"
ask-kind: ruling
ask-since: 2026-10-12
ask-proposal: "Use: 'Target v0.20.0: shoalmark runs on Subversion with no git installed; this is not shipped yet.'"
answer: "accepted - with a change: in #154 the clause reads (Python on every machine; git on Git; svn's command-line tools on Subversion, where from v0.20.0 git is not needed)"
answered: 2026-10-12
answered-by: holgo99
---

# FM-004 — Nobody knows whether another project's agents would recommend adopting the tool

## What is true now

**2026-10-12 — #154 and the release archive.** #154's RV-2734 fix text remains the Owner's to give; the front-matter proposal is draft wording for their signed acceptance or replacement. **Confidence 98%:** it states only the authorized v0.20.0 requirement and does not claim it shipped. After the answer, a Records Builder replaces the withdrawn sentence and one Reviewer pass follows. Probe draft 3 runs in its separate session.

**2026-10-13 — release archive integrated; independent critical review owed.** Local branch `fm/004-archive-current`, based on current main `e7ce074`, carries the source archive range `570a773..23e3f7a` as the unchanged inventory refactor `3ac2e9d` and behavior integration `94f6bc2`, with the missing-manifest refusal at `b62b341`. RV-3020's complete vendored set, RV-3021's ASCII-only build refs and all five probe files survive. The archive checks exact manifest bytes before copying only the 19 tool files; its PIN retains legacy line-end normalization. Malformed manifests, changed or missing listed entries and unsafe source symlinks refuse before writing. A missing RELEASE when Git is unavailable also refuses before writing; the existing Git-present partial/untagged path remains retained. The bounded shared `git_dirs` change avoids Git discovery for non-Git acquisition destinations, retaining Git/common-worktree and disk `.git` guards; stage 1 must integrate this point, and the separate critical Reviewer must judge it. Current 0.19.4 authority/security behavior, legacy interpretation and all five code CI jobs are retained. This supplies acquisition alone: no Subversion backend or gate operation is claimed.

Local checks passed: changed-Python compilation, 158 core checks (14.99 s) and 60 scoped vendoring/archive workflow properties and controls (29.85 s), zero scoped skips. A commit-pinned dry run of `b62b341`, without creating a tag, built a 25-entry zip whose RELEASE hashes all 24 shipped entries, including the five probe files at their paths. Rebuilding under UTC and Pacific/Kiritimati gave identical bytes; the checksum verified. SHA-256: `9632e27f2ef02d8d352000ecde4280e3c19507527e574a0b59a19fe2084e5e60`. With no Git binary on PATH, default vendoring refused the untagged dry run, explicit `--allow-untagged` copied only the complete tool, and a changed source refused without writes. This is a local proof at the current version, not a release artifact. Next: separate-session critical review, Owner fetch/push and complete CI; stage-1/candidate integration, the Owner's release-script change and real release workflow qualification remain owed. The push URL stays `DISABLED`.

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

## Done when

The three reports are recorded here with their counts and verdicts, the note is corrected for what they found, and
the limits are said: three runs, one model family, an invented project.

## Ship log

| Date | Event |
|---|---|
| 2026-09-21 | Filed; prediction written before the runs. |
| 2026-09-21 | Three runs: 0 of 3 adopt. Defects fixed as 0.12.1. |
| 2026-09-21 | Second round: the brake is the Owner's latency, 3 of 3; a tool change alone flips nothing. |
| 2026-10-13 | Release archive integrated onto current 0.19.4: refactor `3ac2e9d`, behavior `94f6bc2`, source `570a773..23e3f7a`; relevant local controls and a commit-pinned dry run pass. Independent critical review, Owner publication, CI and release integration remain owed. |
| 2026-10-13 | Final bounded archive qualification at `b62b341`: 158 core checks and 60 scoped controls pass; no-git missing-manifest refusal covered, deterministic checksum verified. Acquisition alone; independent critical review and release integration remain owed. |
