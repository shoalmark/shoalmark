---
id: FM-004
status: In Progress
considered: FM-003
tags: research
next: build
triaged: 2026-10-13
tier: P1
rank: 2
hook: "A first outside Owner will hand ADOPT.de.md to his agents mid-way through a 60-package plan. My guess was 35 % yes if asked cold, 70 % with a measurement instead of a pitch. A guess is not a number."
---

# FM-004 — Nobody knows whether another project's agents would recommend adopting the tool

## What is true now

**2026-10-18 — the release archive ships in v0.20.0, and FM-004 stays open.** Its answered ask is cleared, signed
`25dc9db`. Its *Done when* names the three outside reports, which v0.20.1's outside run is to give; the archive is not
that.

**2026-10-15 — how the carry meets #173's notice line is the Owner's to rule (the ask above).** On this branch,
`258cc3c` follows the carry as option (b): `--vendor`'s four refusals fold the notice into their one line, as
`--tsvn-hook`'s already do, and the notice still prints once on every Subversion run. With it the archive block passes
35 of 35 and `test_vcs_archive.py` 13 of 13 on Python 3.15 and 3.9.6; the prepared fix's development contrasts give 18
of 28 as written, their 10 success rows differing only by the notice line. (a) would change only the 11 checks; (c)
would drop the notice from `--vendor`. Proposed: (b), with the contrasts' success rows read without the notice line, in
the evidence only. The bounded verification reviews the carry with `258cc3c` on top; the answer gates only the merge.

**2026-10-15 — FM-004's answer carried onto main; 11 archive checks fail on #173's Subversion notice, a finding for the Owner.** Merge `9bed976` brings `fm/004-stage-integration` (`284a4e8`, final verdict `eabee22`) onto main `5f792d6` as git's own three-way result for every product file; `9d735ab` replaces `archive_source()` alone with the prepared fix of 13 October, recorded privately (its AST equal, every other definition's unchanged). On Python 3.15 and 3.9.6, `test_core.py` 321 ok (LF and a CRLF checkout), release.yml's 33 controls, every other block that names or calls `--vendor`, `test_vcs_cli.py`, py_compile, `--check` and two time-zone builds of identical bytes pass. 11 of the archive block's 35 checks fail, identically at the merge before the classification: #173 prints one Subversion notice line before each refusal those checks require to be one line; with it off, all 35 pass. The prepared fix's 28 development contrasts give 0 of 28 as written for the same reason, 28 of 28 with that line excluded. RV-3072 gets no third round.

**2026-10-13 — standalone archive accepted; archive/common integration HELD after its final review.**
Owner #168 preserves Part B's signed RV-2734 replacement and archived exchange; #170 records remain merged.
B1/final probe preparation stays allocated to v0.20.1, with Claude's site work tomorrow. The adoption result
remains 0 of 3 in the 21 September synthetic run, not a measured real-consumer recommendation.

Standalone archive critical READY `1ba6fc4`, Reviewed `79b17ba`, closes RV-3070 in round 2. Its current-main
records READY is `b2e5195`, Reviewed `f117209`; that exact untagged dry-run checksum belongs to f117209.
Common critical READY `ef77527`, Reviewed `b72b9ae`, closes RV-3085–RV-3088, COMMON SKELETON ONLY.
Accepted antecedents and their complete verdicts remain unchanged; neither accepts their later composition.

Archive/common final NOT READY `eabee22`, Reviewed `284a4e8`, closes RV-3071 and leaves RV-3072 P2 HELD,
second/final round exhausted. Actual CLI administrative exclusions now pass. Source nonrepository classification
still accepts loose diagnostic substrings: real Git with malformed global configuration named
`GIT_DISCOVERY_ACROSS_FILESYSTEM` returns 128, but vendoring succeeds and copies 19 payload files plus PIN.
Identical bad configuration under an ordinary name refuses; empty valid configuration retains the positive.
An unrelated successful source top and an inherited discovery ceiling also expose the same unfinished obligation.
Independent 302 core and 68 affected controls pass, but they do not override this reproduced product failure.
The exact corrective artifact evidence remains in the immutable verdict and is not relabeled to another head.

Proposal: keep `fm/004-stage-integration` held. Prepare complete diagnostic matching and checked source-root
relationships outside production for Owner disposition; open no third verification or replacement finding.
The signed current path permits at most two rounds per finding and requires a signed reason to merge over
another verdict. Local CLI/board/init/install work proceeds separately from this held archive integration.
Required CI/native qualification, consumer adoption/authentication/trial proof, release-script adaptation,
actual tagged release and publication remain due. Push DISABLED; Owner fetches, pushes and merges.

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

**2026-10-15** · Which disposition should the archive/common integration take after RV-3072 exhausted its review rounds?
**answered** — accepted - Take the prepared strict classification into production now, as its own change, with one bounded verification: the diff is the prepared fix, its checks pass, nothing else changes; no new finding below P1. RV-3072 gets no third round. · holgo99
**relation** — accepted with a change
**signed** — fcff753 · G

**2026-10-16** · The carried archive fails 11 of its checks on main: #173 prints a Subversion notice before each refusal those checks pin to one line. Which way do you take it?
**answered** — accepted - b: 258cc3c — --vendor's refusals fold the notice into their one line, as --tsvn-hook's do · holgo99
**relation** — accepted the proposal
**signed** — 25dc9db · G

## Ship log

| Date | Event |
|---|---|
| 2026-10-18 | The answered ask cleared (`25dc9db` · G). The archive (#184, `1148114`) ships in v0.20.0; FM-004 stays open for its three outside reports. |
| 2026-10-15 | Ask filed: how the carried archive meets #173's Subversion notice line; option (b), `258cc3c`, on this branch after the carry. |
| 2026-10-15 19:50 CEST | FM-004 carried as answered: merge `9bed976` (integration `284a4e8`, verdict `eabee22`) and `9d735ab` (`archive_source()` from the prepared fix of 13 October, recorded privately). Core 321, release.yml 33, the other `--vendor` blocks, `--check` and reproducible builds pass on 3.15 and 3.9.6; 11 of 35 archive checks fail on #173's Subversion notice line, a finding for the Owner. |
| 2026-10-13 20:08 CEST | Archive final NOT READY `eabee22`: RV-3071 CLOSED, RV-3072 HELD after the final round; strict-classification disposition proposed on the board. A1/A2 accepted component merged locally; C bounded READY `f59a1c1`; B final review and A caller migration continue. Local stage work proceeds separately; protected acceptance remains held. |
| 2026-10-13 18:18 CEST | Serial archive/common wiring retains both independently accepted products: common `git_dirs` unchanged, existing archive HERE read marked source, real SVN positive fixtures and expanded administrative guards retained. Compile, 302 core and 55 scoped archive controls pass; exact-head artifact and separate critical integration review remain due. |
| 2026-10-13 17:24 CEST | **Owner #170 records integrated locally** from `cab89ed`, retaining archive critical READY `1ba6fc4` and its exact product/workflow/release-script blobs. Current command-applied judgement and signed Part B/exchanges remain; INDEX regenerated. Scoped records verification and Owner-pushed CI remain. |
| 2026-09-21 | Filed; prediction written before the runs. |
| 2026-09-21 | Three runs: 0 of 3 adopt. Defects fixed as 0.12.1. |
| 2026-09-21 | Second round: the brake is the Owner's latency, 3 of 3; a tool change alone flips nothing. |
| 2026-10-13 | Recovered Part B from `643ad4b` on current main, applied the exact signed RV-2734 prerequisite replacement and FM-023 release allocation; one records review pending, archive re-review and integration still owed. |
| 2026-10-13 | Release archive integrated onto current 0.19.4: refactor `3ac2e9d`, behavior `94f6bc2`, source `570a773..23e3f7a`; relevant local controls and a commit-pinned dry run pass. Independent critical review, Owner publication, CI and release integration remain owed. |
| 2026-10-13 | Final bounded archive qualification at `b62b341`: 158 core checks and 60 scoped controls pass; no-git missing-manifest refusal covered, deterministic checksum verified. Acquisition alone; independent critical review and release integration remain owed. |
| 2026-10-13 | RV-3070: ordinary local integration of main `ab7ed3f` reconciles its signed Part B/history with the archive records; product/test blobs retain reviewed `3c18008`. Independent review reports 85 passing local controls; its remaining critical round 2, CI and release integration remain owed. |
