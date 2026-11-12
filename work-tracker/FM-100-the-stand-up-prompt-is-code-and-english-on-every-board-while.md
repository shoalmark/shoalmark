---
id: FM-100
status: Proposed
considered: FM-030, FM-031, FM-088, FM-095, FM-104, FM-143, FM-149
tags: process
epic: FM-139
blocked-by: FM-104
next: review
hook: "The stand-up prompt is code, English on every board, and two prompts in one: the Owner's sitting and a planner's day. With a coordinator over several teams the two halves belong to different seats. It splits by seat into skills that speak the person's language, on a path only the Owner changes."
ask-id: FM-100-Q1
ask: "Are FM-100's decisions taken, as its section Decisions, for the Owner sets out, superseding FM-149's decision 3 and the STAND-UP.md design of 30 October, with the lane in v0.20.3?"
ask-kind: ruling
ask-since: 2026-11-12
ask-options: "yes, as proposed | yes, with the changes I name"
ask-proposal: "yes, as proposed"
---

# FM-100 — the stand-up prompt is code and English on every board, while the Board's words come from the language pack

## What is true now

**2026-11-12 — the ask is held back until its design audit is READY;** the audit's findings are recorded privately.

**2026-11-12 — rewritten, with FM-100-Q1; nothing is built.** On the Auditor's word. The coordinator seat is coming:
each team is one planner, which owns its builders' work and checks it with reviewers, and the coordinator talks to every
planner. Read at main `ec8479c`:

1. **The stand-up prompt is two prompts in one**
   ([`DAY_STANDUP`, `shoalmark.py` L5211–L5226](https://github.com/shoalmark/shoalmark/blob/ec8479c68ffceb8afb545a3a745c58b310781b63/shoalmark.py#L5211-L5226)):
   - steps 0 to 3 hold the Owner's sitting: the sync, the agenda one item at a time, the command that records each
     answer, and the sitting's branch;
   - steps 4 to 6 are a planner's day: the blockers, the day's path, and driving it on a go, with builders, reviewers,
     a READY on each head, and merges batched for the Owner.

   With one team, one session does both. With several, the first half spans the teams and is the coordinator's, and
   the second stays with each planner.
2. **Five setups, and four values.** The prompt has a form for a forge, git, a local repository, Subversion and a plain
   folder ([`DAY_STANDUP_BY` and `day_standup`, L5229–L5272](https://github.com/shoalmark/shoalmark/blob/ec8479c68ffceb8afb545a3a745c58b310781b63/shoalmark.py#L5229-L5272)); the close-out is one prompt
   ([`DAY_PROMPTS`, L5275–L5286](https://github.com/shoalmark/shoalmark/blob/ec8479c68ffceb8afb545a3a745c58b310781b63/shoalmark.py#L5275-L5286)). Four values fill them, the repository's name, its path,
   the tool's command and the default branch, each through
   [`day_value_problem`, L5287–L5300](https://github.com/shoalmark/shoalmark/blob/ec8479c68ffceb8afb545a3a745c58b310781b63/shoalmark.py#L5287-L5300).
3. **An agenda across repositories exists; a sitting across them does not.** `--standup DIR …` reads one agenda across
   the repositories named, running nothing of theirs and writing nothing
   ([L10820–L10823](https://github.com/shoalmark/shoalmark/blob/ec8479c68ffceb8afb545a3a745c58b310781b63/shoalmark.py#L10820-L10823),
   [`test_standup_repos.py`](https://github.com/shoalmark/shoalmark/blob/ec8479c68ffceb8afb545a3a745c58b310781b63/test_standup_repos.py)).
4. **The prompts are English on every Board** ([README L320](https://github.com/shoalmark/shoalmark/blob/ec8479c68ffceb8afb545a3a745c58b310781b63/README.md#L320)). FM-149-Q1 took
   [FM-149](FM-149-the-docs-the-board-s-prompts-and-the-skills-have-no-one-rule.md)'s decisions: a skill's report and
   conversation follow the Board's `lang` (decision 2), and the close-out gets a file of its own, `CLOSE-OUT.md`
   (decision 3).
5. **The drift skills live in shoalmark/skills,** because they work in any git repository without shoalmark
   ([README L305](https://github.com/shoalmark/shoalmark/blob/ec8479c68ffceb8afb545a3a745c58b310781b63/README.md#L305)). A stand-up runs the tool.
6. **This tracker's earlier design,** on the Owner's word of 30 October, is `STAND-UP.md` in each language pack, the
   person's own file, changed only by their signed commit, waiting on
   [FM-104](FM-104-the-person-s-own-files-are-spread-over-the-repository-and.md) for where it lives. The entries below
   stay as its record.

**2026-11-04 — its open question has a tracker:
[FM-149](FM-149-the-docs-the-board-s-prompts-and-the-skills-have-no-one-rule.md).** Whether the close-out prompt takes
the stand-up prompt's form is FM-149's decision 3, put to the Owner with FM-149-Q1: `CLOSE-OUT.md` beside
`STAND-UP.md`, in the pack's language with English as the fallback, and the person's own file. Where both files live
still waits on FM-104. Nothing is built.

**2026-10-30 — where this tracker's files go comes from
[FM-104](FM-104-the-person-s-own-files-are-spread-over-the-repository-and.md).** It waits on that decision, on the
Owner's word of 30 October, and nothing of it is built before it.

**Filed 2026-10-30 for v0.20.3; nothing is built.** On the Owner's word of 30 October: the stand-up prompt is localised
to the Board's language, with English as the fallback, and the German pack takes it as `STAND-UP.md`.

- **What is true today:**
  - The stand-up prompt is code, and English on every board.
  - The Board's words already come from the language pack: `examples/de/` holds `labels.yaml`, `TEMPLATE.md` and
    `TRIAGE.md`.
  - ADOPT has its language twins.
- **Where this comes from:** the stand-up prompt's growth in v0.20.2, part A, ships in English as built. Its part B, the
  prompt in the Board's language, moves here.
- **STAND-UP.md is the person's own:** the Owner of the repository edits it freely, with their own signed commit, as
  they sign an answer; the gate refuses a change any seat makes. "The Owner" here is the product's role, the person
  in charge of a repository.
- **Open, for its design:** whether the close-out prompt takes the same form, and what it is called.

## Why

A prompt that holds two seats' work cannot follow a team's shape. With a coordinator, the Owner's sitting spans the
teams, while each planner drives its own repository. A skill for each seat carries each half to the seat that runs it,
in the person's language wherever a person reads it. And words the Board hands into a session are words a seat could
plant, so only the Owner changes them.

## Decisions, for the Owner

FM-100-Q1 asks for all of these at once. An answer of "yes, with the changes I name" names each change by its number.

1. **Two skills replace the Board's stand-up prompt.**
   - **`standup`** is the planner's team stand-up. It runs `--standup` and `--triage` for its repository and writes a
     team report: the open asks with their proposals, the blockers with proposals, the ranked path, and each wait on
     the Owner, marked. On a go it drives, as today's step 6: builders, reviewers, a READY on each head, and merges
     batched for the Owner.
   - **Its two modes.** *Direct* is for one team without a coordinator: the planner holds the Owner's sitting itself,
     as today's steps 0 to 3, so the coordinator stays opt-in. *Report* sends the report to the coordinator in a hail/1
     envelope.
   - **`standup-teams`** is the coordinator's. It asks each planner for its stand-up and collects the reports. It checks
     what it can: the pull requests' heads, CI, and the open asks through `--standup DIR …`. It writes one page per
     team, and a section across the teams: conflicts, shared dependencies, a suggested order, and what each team needs
     of the Owner.
   - **The sitting, team by team.** `standup-teams` then takes the asks one at a time, each with the command that
     records the answer in that repository, which the skill never runs; then go, hold or change for each team. It hands
     each go to that team's planner, and gathers the merge-ready lines into batches.
   - **Each skill keeps today's five setups:** a forge, git, a local repository, Subversion and a plain folder.
2. **The close-out follows the same split:** `closeout`, the planner's, and `closeout-teams`, the coordinator's, which
   give one consolidated handover. This supersedes FM-149's decision 3, `CLOSE-OUT.md`.
3. **The Board's buttons copy one line:** the skill's name, its mode, and the values the tool already fills and checks:
   the name, path, command and branch, each through `day_value_problem`, and the setup it already tells apart. The
   labels stay in `labels.yaml`. **Which line where, as I propose it:**
   - **A repository's Board serves its own planner.** Where `[seats]` names no coordinator, its stand-up row copies
     `standup` in direct mode, with that repository's values.
   - **Where `[seats]` names a coordinator,** the Owner's sitting is the coordinator's, so the row copies
     `standup-teams`, the skill's name alone: the coordinator reads its repositories from its own roster (decision 7).
     The planner's report-mode line is the coordinator's to send, never the Owner's to paste, so no Board offers it.
   - **The close-out rows** follow the same rule.
   - **The Designer checks both rows,** in English and German.
4. **Translation, as FM-149's decision 2:**
   - each `SKILL.md` is one English source, and the conversation and the report follow the Board's `lang`;
   - messages between seats, hails and team reports, stay in English, with ids as written;
   - everything the Owner reads is in their language. The coordinator's consolidation is the one place translation
     happens; in direct mode, it is the planner's conversation and report;
   - this supersedes the `STAND-UP.md` design of 30 October.
5. **Where the skills live:** in shoalmark/shoalmark, versioned with the tool.
   - README L305 keeps shoalmark/skills for blocks that work in any git repository without shoalmark. These skills run
     the tool.
   - The tool installs them from its own version into each harness's project skill folder, Claude Code's and Codex's
     alike.
   - The installed copies are the Owner's path: the gate refuses a seat's change, with a class test and its mutant.
     This carries this tracker's rule that no seat can plant words the Board hands on.
   - **FM-104, as I propose it:** it no longer blocks this tracker. The skills sit where the harnesses look, which
     FM-104's own principles keep ("harness files stay where harnesses look"), and this tracker adds no file to the
     person's home. FM-104's inventory lists the installed copies among the files the tool writes. The `blocked-by:`
     line goes in the commit that records the answer.
6. **Authority.** A go is the coordinator's own instruction, and the coordinator answers for it. Rulings, scope and
   allocation stay the Owner's signed answers in the team's repository, which the planner reads from the record. A
   message carries no Owner authority, in either skill.
7. **Teams:** one planner per repository, for now. The coordinator reads a roster (repository, planner session,
   transport) in hail/1's roster form, kept in its own workspace, because setup facts stay private. Direct mode needs
   no roster.
8. **Against the relay's shadow:** each team report is filed as written, with its sha256, and every consolidated item
   links its source. A planner keeps driving ranked work while it waits, as today's step 6.4.
9. **The text:** [`docs/standup.md`](https://github.com/shoalmark/shoalmark/blob/ec8479c68ffceb8afb545a3a745c58b310781b63/docs/standup.md) and [`docs/de/standup.md`](https://github.com/shoalmark/shoalmark/blob/ec8479c68ffceb8afb545a3a745c58b310781b63/docs/de/standup.md) are
   rewritten in the same lane, by FM-149's decision 1: the German as "du", and "Board" as it stands. Every text a person
   reads gets its German twin.
10. **The lane is critical:** it changes what a session is handed and runs, and it adds a path only the Owner may
    change. The Designer checks the Board's rows beside a critical review.
11. **Allocation:** v0.20.3, a chapter of [FM-139](FM-139-v0-20-3-s-rows-sit-in-fm-023-fm-006-and-fm-053-so-no-one.md).

## Done when

Each item names its commit or pull request when it lands.

- [ ] **The Owner has answered FM-100-Q1.**
- [ ] **`standup` and `standup-teams`** stand in shoalmark/shoalmark, one English source each, in both of `standup`'s
  modes and the five setups, and the Board's stand-up prompt is gone.
- [ ] **`closeout` and `closeout-teams`** do the same for the close-out, and give one consolidated handover.
- [ ] **The Board's rows copy one line each,** as decision 3 sets out, every value through `day_value_problem`, their
  labels in English and German.
- [ ] **The tool installs the skills** from its own version into each harness's project skill folder, and the gate
  refuses a seat's change to an installed copy, with a class test and its mutant.
- [ ] **A skill's conversation and report follow the Board's `lang`,** messages between seats stay in English, and a
  test pins the report's keys.
- [ ] **Each team report is filed with its sha256,** and each consolidated item links its source.
- [ ] **`docs/standup.md` and `docs/de/standup.md`** describe the skills, and their pair check passes.
- [ ] **The Designer's check and the critical review are READY.**

## Ship log

| Date | Event |
|---|---|
| 2026-11-12 | The ask is held back until its design audit is READY; the audit's findings are recorded privately. Records only. |
| 2026-11-12 | Rewritten on the Auditor's word: the stand-up and the close-out split by seat into skills, with FM-100-Q1, which supersedes FM-149's decision 3 and the `STAND-UP.md` design of 30 October. Records only. |
| 2026-11-04 | `epic: FM-139`: a chapter of v0.20.3's epic. Records only. |
| 2026-11-04 | Its open question, the close-out prompt's form, put to the Owner as FM-149's decision 3 (ask FM-149-Q1). Records only. |
| 2026-10-30 | Blocked by FM-104, which decides where the person's files live, on the Owner's word of 30 October. Records only. |
| 2026-10-30 | Filed for v0.20.3, on the Owner's word of 30 October. Records only. |
