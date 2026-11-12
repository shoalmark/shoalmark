---
id: FM-163
status: Proposed
considered: FM-062, FM-083, FM-097, FM-117, FM-118, FM-119, FM-120, FM-143, FM-149, FM-162
tags: process
next: owner
hook: "find-drift and prune-drift name no form for the ids a report gives its rules, disagreements and obsolete text, though prune-drift works from those ids. find-drift reads hooks, but not the harness settings where a guard would sit, and the report counts breaks but not how far merged work holds. The proposal, put to the Owner as FM-163-Q1: shoalmark/skills 1.1.0."
ask-id: FM-163-Q1
ask: "Do you take FM-163's decisions as proposed: the id forms R-n, DR-n and O-n in both drift skills, harness settings read with a guard as a suggested promotion, three trust measures as lower bounds, a critical review, and shoalmark/skills 1.1.0?"
ask-kind: ruling
ask-since: 2026-11-12
ask-options: "yes, as proposed | yes, with the changes I name | no, not now"
ask-proposal: "yes, as proposed"
---

# FM-163 — the drift skills name no id forms, read no harness settings and measure no trust in merged work

Seat: the Planner (27f31560) · filed 2026-11-12, on the Auditor's word of that day.

## What is true now

**Filed 2026-11-12, Proposed, with FM-163-Q1 put; nothing is built.** It is the next release of
[shoalmark/skills](https://github.com/shoalmark/skills/tree/344ba36c0afec954260ce76d726512f255afe3c5), after its first
release of 5 November. The lane builds there; this tracker is the record. shoalmark's
[`skills-pin.json`](https://github.com/shoalmark/shoalmark/blob/7c93c835d6ac9842bb28a37118822f4a6b8a661b/skills-pin.json)
names the new tag in the shoalmark release that takes it, as FM-143-Q2's answer has it.

- **What the skills hold today, read at `344ba36c`:**
  - **Ids without a form.** find-drift gives each rule row "an id for references"
    ([step 3, L29](https://github.com/shoalmark/skills/blob/344ba36c0afec954260ce76d726512f255afe3c5/plugins/shoalmark/skills/find-drift/SKILL.md#L29))
    and tells the person "each disagreement and each obsolete text by id"
    ([step 11, L62](https://github.com/shoalmark/skills/blob/344ba36c0afec954260ce76d726512f255afe3c5/plugins/shoalmark/skills/find-drift/SKILL.md#L62)).
    prune-drift works from the report's disagreements and obsolete text
    ([step 8, L46](https://github.com/shoalmark/skills/blob/344ba36c0afec954260ce76d726512f255afe3c5/plugins/shoalmark/skills/prune-drift/SKILL.md#L46))
    and lists them "by id"
    ([step 11, L64](https://github.com/shoalmark/skills/blob/344ba36c0afec954260ce76d726512f255afe3c5/plugins/shoalmark/skills/prune-drift/SKILL.md#L64)).
    Neither names a form, so two runs, or the two skills, can number them differently.
  - **Harness settings unread.** find-drift's sources take "hooks with the scripts and configuration they run"
    ([step 2, L22–L23](https://github.com/shoalmark/skills/blob/344ba36c0afec954260ce76d726512f255afe3c5/plugins/shoalmark/skills/find-drift/SKILL.md#L22-L23)).
    They do not name the harness settings where an agent's tool call can be refused before it runs, as
    [FM-162](FM-162-the-acts-a-seat-must-never-do-are-held-only-as-prose-so-one.md) cites them.
  - **Breaks, not trust.** Breaks are counted as lower bounds, "with their definition and the query or record that
    gives them"
    ([step 8, L45–L46](https://github.com/shoalmark/skills/blob/344ba36c0afec954260ce76d726512f255afe3c5/plugins/shoalmark/skills/find-drift/SKILL.md#L45-L46)).
    Nothing measures how far merged work holds.
  - **What the tests pin**
    ([`test_plugin.py`](https://github.com/shoalmark/skills/blob/344ba36c0afec954260ce76d726512f255afe3c5/test_plugin.py)):
    the seven section keys in order and the keys prune-drift reads (L60–L62, L658–L692); the language sentence;
    each skill's description and compatibility as written (L44, L520–L531); and one version across both plugin
    manifests, the CHANGELOG's newest heading and the READMEs' install pins (L456–L487, L595–L602).

## Why

A report is read twice: by the person, and by prune-drift. Ids of one form let both, and the next run, name the same
finding. A rule whose break is a single act is better refused before the act than counted after it, and a harness's
settings are where that refusal lives. A count of breaks shows where prose failed; it does not show how far the work
that passed has held. Three measures, each a lower bound with its query, show that without grading anyone.

## Decisions, for the Owner

The ask, FM-163-Q1, asks for all of these at once. An answer of "yes, with the changes I name" names each change by
its number.

1. **The id forms, the same in both skills:** `R-n` for a rule row, `DR-n` for a disagreement and `O-n` for obsolete
   text, numbered from 1 in each report. prune-drift cites them as find-drift's report gives them. They never
   translate, as FM-149's decision 1 has it for identifiers. A test pins the three forms in both skills' text.
2. **Harness settings as sources, and a guard as a suggested promotion.**
   - **Step 2's defaults** add Claude Code's project settings, `.claude/settings.json`, and Codex's project hooks and
     rules, `.codex/hooks.json`, `.codex/config.toml` and `.codex/rules/`, as their own pages place them
     ([Claude Code](https://code.claude.com/docs/en/hooks), [Codex hooks](https://developers.openai.com/codex/hooks),
     [Codex rules](https://developers.openai.com/codex/rules)). A person's own settings outside the repository are
     listed as unreadable, as step 2 already does for a place outside the repository; a skill never reads the
     person's home folder (FM-149's decision 2).
   - **Step 4** counts a hook or rule there as enforcement, where it runs being the harness, before the tool call.
   - **Step 5** places a harness guard in layer 2, beside a local hook: it refuses before the act, and can be
     bypassed as a local hook can. The layers stay five, in both skills.
   - **Step 9:** where a rule's break is a single act that a guard could refuse, the ranking suggests a guard as its
     promotion. It is a suggestion; the skill still rules on nothing.
3. **Three measures of trust in merged work, each a lower bound with its definition and query.** find-drift never
   uses the network, so each query reads git and the repository's own records.
   - **Reverts:** merged changes on the default branch that a later commit reverts and names by git's "This reverts
     commit" line, from `git log --first-parent` on the default branch.
   - **Findings after merge:** review findings and trackers that cite a merged pull request or commit and were raised
     after its merge, from the records' references and the merge dates.
   - **READY verdicts that held:** each READY on a merged head, set against the two counts above. The READYs they
     contradict are a lower bound; the rest are not proven to have held, and the report says so.
   - They are counted by rule and by area, never by author, seat or reviewer: a suggestion of where a check would
     help, never a grade of anyone.
4. **The section keys stay,** as FM-149's decision 2 has them. The measures sit in `## breaks`, and the guard
   suggestions in `## ranking`. The seven keys, their order, the keys prune-drift reads, and each skill's description
   and compatibility do not change. Both READMEs, English and German, describe the new parts and keep their pair
   check (FM-149's decision 1). `test_plugin.py` extends to the id forms, the new sources, the layer wording and the
   measures' place.
5. **The review is critical:** prune-drift acts on what find-drift reports.
6. **The release is 1.1.0.** New behaviour takes a minor number under
   [semantic versioning](https://semver.org/). Both plugin manifests carry it, the CHANGELOG's heading is
   `## 1.1.0 — <date>`, the READMEs pin `shoalmark/skills@v1.1.0` and say how to upgrade, and the tag is the
   Owner's.

**The limits, stated plainly.**
- **The measures read git and the repository's own records.** A revert not named as one, a finding kept outside the
  repository, and anything only the forge holds are not counted.
- **A guard is only suggested.** shoalmark's own seat guard is decided in FM-162.
- **Out of this release:** [FM-117](FM-117-find-drift-does-not-read-decisions-against-git-find-stranded.md)'s next round
  (decisions as sources, the record against git, stranded work, an evidence chain),
  [FM-097](FM-097-find-drift-does-not-audit-the-owner-s-rulings-whether-each.md)'s audit of the Owner's rulings, and
  [FM-083](FM-083-nothing-measures-how-well-a-skill-does-its-work-only-its.md)'s measure of how well a skill does its
  work stay their own trackers.

## Done when

Each item names its commit or pull request when it lands.

- [ ] **The Owner has answered the ask,** FM-163-Q1.
- [ ] **The id forms:** both SKILL.md files name `R-n`, `DR-n` and `O-n` the same way, and a test pins them in both.
- [ ] **The harness settings:** find-drift's step 2 lists them, step 4 counts them, layer 2 names a harness guard in
  both skills, and step 9 suggests a guard where a break is a single act; a test pins each.
- [ ] **The measures:** the three sit in `## breaks`, each with its definition and query as a lower bound, counted by
  rule and area and never by person or seat; a test pins their place and that sentence.
- [ ] **Unchanged:** the seven section keys, their order, the keys prune-drift reads, and the descriptions, as
  `test_plugin.py` pins them.
- [ ] **README.md and README.de.md** describe the new parts, and their pair check passes.
- [ ] **1.1.0:** both plugin manifests, the CHANGELOG's heading and the READMEs' pins, with `test_plugin.py`'s version
  checks passing; the tag is the Owner's.
- [ ] **shoalmark's `skills-pin.json`** names the tag in the shoalmark release that takes it.
- [ ] **The critical review is READY.**

## Ship log

| Date | Event |
|---|---|
| 2026-11-12 | Filed, Proposed, with FM-163-Q1 put: shoalmark/skills 1.1.0, with id forms, harness settings read and three measures of trust. Records only. |
