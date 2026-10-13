---
id: FM-004
status: In Progress
considered: FM-003
tags: research
next: review
triaged: 2026-10-13
tier: P1
rank: 2
hook: "A first outside Owner will hand ADOPT.de.md to his agents mid-way through a 60-package plan. My guess was 35 % yes if asked cold, 70 % with a measurement instead of a pitch. A guess is not a number."
---

# FM-004 — Nobody knows whether another project's agents would recommend adopting the tool

## What is true now

**2026-10-13 — archive/common wiring implemented locally; independent integration review remains due.**
Owner #168 preserves Part B's exact signed RV-2734 replacement and archived exchange; #170 planning records are
on main at `cab89ed`. B1/final probe preparation remain allocated to v0.20.1, with Claude's site work tomorrow.
The adoption result remains 0 of 3 in the 21 September synthetic run, not a measured real-consumer recommendation.

Archive critical READY `1ba6fc4` reviewed `79b17ba`, closed RV-3070 in round 2 and retained the earlier 85 independent
product controls. Current-main archive records are independently READY at `b2e5195`, Reviewed `f117209`.
The latter's local untagged dry-run checksum `e357518935af72527ffc803de11034cad51accd2579577f3315d17c4c87baa35`
belongs to exact `f117209`, not this integration. Common critical READY `ef77527` reviewed `b72b9ae`, COMMON
SKELETON ONLY, closing its four findings; exact-tree main integration `1fc12b0` and dispatch `c599d5c` follow it.
Common dispatch records READY `84c8a6b` reports one P3 status fix, RV-3057, corrected forward in this record.

Planner's serial `fm/004-stage-integration` starts from that dispatched common product, retains its boundary,
cache invalidation, metadata exclusions and history-aware scanner, and ordinarily merges archive READY `b2e5195`.
The only overlapping production function, `git_dirs`, stays exact to accepted common. The archive's existing
HERE top-level read now explicitly uses `source=True`; the four allowed source operations do not expand.
Every other archive function stays AST-identical to its accepted product. Release workflow/build script stay
byte-identical, and VERSION, CHANGELOG, signatures, legacy meanings and Git authority remain unchanged.

Positive acquisition controls now use real local SVN working copies prepared before the production PATH is emptied.
Git own/common-directory exclusions remain required as a subset of the expanded .git/.svn/ancestor/alias guards;
every discovered administrative path still refuses writes. Empty or unreadable metadata remains a refusal.
Changed Python compiles; unchanged core passes all 302 checks (approximately 71.5 s), and the exact existing
archive/workflow block passes 55 controls in 27.907 s, with zero skips. Those checks include real no-Git/no-SVN
acquisition, complete manifests, RV-3020/RV-3021, snapshot copying, raw bytes/PIN normalization, legacy Git path,
unsafe sources, workflow refusal controls and expanded administrative guards. They are Planner checks, not a new
independent verdict. The C-authored renamed-caller control `c974044` retains scanner assertions during migration.

Next: commit and clean-tree gate, exact-final-head deterministic dry run, then independent critical integration review.
An earlier archive checksum is never relabeled to a new head. Full SVN command/board/history/guard and P entry wiring,
consumer policy adoption/proof, required five-job CI, native qualification, Owner release-script adaptation and real
release workflow/publication remain due. D3/D4 remain held. This work supplies bounded acquisition/shared dispatch,
not full Stage 1 or shipped SVN support. Push stays DISABLED; Owner fetches, pushes and merges.

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

## Part B — the probe's next version, and onboarding through the agents (2026-10-08; wording updated 2026-10-13)

The Owner's work package after v0.19.1, in two lanes that meet at the landing page's dialog. **B1, the landing page,**
in English and German from one template: a primary button that copies a probe prompt and opens a dialog, built behind a
switch that stays off until the probe has passed; a secondary "How it works"; and figures generated from the repository
when the site is built. **The probe lane** rewrites ADOPT.md and ADOPT.de.md as an honest evaluation of fit that may end
in "no fit": prerequisites first (Python on every machine; git on Git; svn's command-line tools on Subversion, where from v0.20.0 git is not needed), the
human's yes before it runs, the working copy read-only within a time and file budget, the one first result that fits
where the project stands, a report of benefit and cost, the yes-path at a work-item boundary, an optional feedback
report the human sends, and the probe in the project's language. Nothing in it says or implies that shoalmark scans for
security problems or data leaks, and it fits one person in charge. Nothing goes outside before it passes a fixed rule:
a set number of consecutive clean end-to-end runs, from the landing page's button to the feedback file; any failure is
fixed, and the count restarts.

The Owner's signed 12 October FM-023 allocation puts B1, the probe's final prompt and what its first outside run needs
in v0.20.1; rows that put that release's date at risk move to v0.20.2. The prerequisite wording names the v0.20.0 target;
Subversion without git is not shipped yet.

## Done when

The three reports are recorded here with their counts and verdicts, the note is corrected for what they found, and
the limits are said: three runs, one model family, an invented project.

## Asks

**2026-10-12** · What exact replacement text do you want for RV-2734 in #154, removing the withdrawn requirement for git on every machine?
**answered** — accepted - with a change: in #154 the clause reads (Python on every machine; git on Git; svn's command-line tools on Subversion, where from v0.20.0 git is not needed) · holgo99
**relation** — accepted with a change
**signed** — adaec88 · G

## Ship log

| Date | Event |
|---|---|
| 2026-10-13 18:18 CEST | Serial archive/common wiring retains both independently accepted products: common `git_dirs` unchanged, existing archive HERE read marked source, real SVN positive fixtures and expanded administrative guards retained. Compile, 302 core and 55 scoped archive controls pass; exact-head artifact and separate critical integration review remain due. |
| 2026-10-13 17:24 CEST | **Owner #170 records integrated locally** from `cab89ed`, retaining archive critical READY `1ba6fc4` and its exact product/workflow/release-script blobs. Current command-applied judgement and signed Part B/exchanges remain; INDEX regenerated. Scoped records verification and Owner-pushed CI remain. |
| 2026-09-21 | Filed; prediction written before the runs. |
| 2026-09-21 | Three runs: 0 of 3 adopt. Defects fixed as 0.12.1. |
| 2026-09-21 | Second round: the brake is the Owner's latency, 3 of 3; a tool change alone flips nothing. |
| 2026-10-13 | Recovered Part B from `643ad4b` on current main, applied the exact signed RV-2734 prerequisite replacement and FM-023 release allocation; one records review pending, archive re-review and integration still owed. |
| 2026-10-13 | Release archive integrated onto current 0.19.4: refactor `3ac2e9d`, behavior `94f6bc2`, source `570a773..23e3f7a`; relevant local controls and a commit-pinned dry run pass. Independent critical review, Owner publication, CI and release integration remain owed. |
| 2026-10-13 | Final bounded archive qualification at `b62b341`: 158 core checks and 60 scoped controls pass; no-git missing-manifest refusal covered, deterministic checksum verified. Acquisition alone; independent critical review and release integration remain owed. |
| 2026-10-13 | RV-3070: ordinary local integration of main `ab7ed3f` reconciles its signed Part B/history with the archive records; product/test blobs retain reviewed `3c18008`. Independent review reports 85 passing local controls; its remaining critical round 2, CI and release integration remain owed. |
