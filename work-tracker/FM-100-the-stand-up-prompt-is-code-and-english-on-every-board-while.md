---
id: FM-100
status: Proposed
considered: FM-030, FM-031, FM-088, FM-095, FM-104, FM-121, FM-143, FM-149
tags: process
epic: FM-139
blocked-by: FM-104
next: review
hook: "The stand-up prompt is code, English on every board, and two prompts in one: the Owner's sitting and a planner's day. With a coordinator over several teams the two halves belong to different seats. The proposal, in its draft ask: it splits by seat into skills that speak the person's language, shipped as defaults that the Owner's own signed copy can replace."
ask: "Are FM-100's decisions taken, as its section Decisions, for the Owner sets them out (default skills under the Owner's signed copies, teams read from the roster spec, two stages in v0.20.3), superseding FM-149's decision 3, FM-023's B of 29 October and the STAND-UP.md design of 30 October?"
ask-kind: ruling
ask-options: "yes, as proposed | yes, with the changes I name"
ask-proposal: "yes, as proposed"
---

# FM-100 — the stand-up prompt is code and English on every board, while the Board's words come from the language pack

## What is true now

**2026-11-12 — revised after its design audit;** the findings are recorded privately.

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
   [`day_value_problem`, L5292–L5299](https://github.com/shoalmark/shoalmark/blob/ec8479c68ffceb8afb545a3a745c58b310781b63/shoalmark.py#L5292-L5299).
3. **An agenda across repositories exists; a sitting across them does not.** `--standup DIR …` reads one agenda across
   the repositories named, running nothing of theirs and writing nothing
   ([L10820–L10823](https://github.com/shoalmark/shoalmark/blob/ec8479c68ffceb8afb545a3a745c58b310781b63/shoalmark.py#L10820-L10823),
   [`test_standup_repos.py`](https://github.com/shoalmark/shoalmark/blob/ec8479c68ffceb8afb545a3a745c58b310781b63/test_standup_repos.py)).
4. **The prompts are English on every Board** ([README L320](https://github.com/shoalmark/shoalmark/blob/ec8479c68ffceb8afb545a3a745c58b310781b63/README.md#L320)). FM-149-Q1 took
   [FM-149](FM-149-the-docs-the-board-s-prompts-and-the-skills-have-no-one-rule.md)'s decisions: a skill's report and
   conversation follow the Board's `lang` (decision 2), and the close-out gets a file of its own, `CLOSE-OUT.md`
   (decision 3).
5. **The drift skills live in shoalmark/skills** and work in any git repository without shoalmark
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

The shipped skills are a suggestion to try. The rules live in the gate and the forge, not in a skill's text, so an
Owner who adapts the process cannot weaken them.

## Decisions, for the Owner

The ask, a draft until it is put as FM-100-Q2, asks for all of these at once. An answer of "yes, with the changes I
name" names each change by its number.

1. **Two skills replace the Board's stand-up prompt.**
   - **`standup`** is the planner's team stand-up. It runs `--standup`, `--triage` and, on a forge, `--queue` for its
     repository, and writes a team report: the open asks with their proposals, the blockers with proposals, the ranked
     path, and each wait on the Owner, marked. After the sitting it drives, as today's step 6 and within decision 8:
     builders, reviewers, a READY on each head, and merges batched for the Owner.
   - **Its two modes.** *Direct* is the Owner's sitting with one team: the planner holds it itself, as today's steps 0
     to 3, so the coordinator stays opt-in. *Report* sends the report to the coordinator in a hail/1 envelope, where
     decision 9 allows it.
   - **`standup-teams`** is the coordinator's. It asks each planner for its stand-up and collects the reports. It writes
     one page per team, and a section across the teams: conflicts, shared dependencies, a suggested order, and what
     each team needs of the Owner.
   - **What it reads, and from where.** `--standup DIR …` gives the open asks only. Who asked comes from each
     repository's own `--standup`, in the report. Pull requests' heads and CI are read from the forge, where there is
     one. Where a report and a read differ, the page shows both, marks the difference, and takes the read.
   - **The sitting, team by team.** `standup-teams` then takes the asks one at a time, each with the command that
     records the answer in that repository, which the skill never runs. It holds today's steps 0 to 3 once for each
     repository: the sync check, the sitting's branch, the check of each answer's commit, and the commands that push
     that branch. Then go, hold or change for each team, as decision 8 reads them. It hands each team's outcome to that
     team's planner, and gathers the merge-ready lines into batches.
   - **A team without a report.** A team whose report is not there after the wait the skill names is listed as *no
     report*, with its open asks from `--standup DIR …` alone and no path. The sitting goes on, and that team gets no
     go. The coordinator starts no session: the page tells the Owner which planner to start.
   - **Setups.** `standup` keeps today's five: a forge, git, a local repository, Subversion and a plain folder. The
     folder setup keeps no drive, as today. Report mode, and so `standup-teams`, needs git (decision 9).
2. **The close-out follows the same split.**
   - **`closeout`**, the planner's, keeps today's four steps for its repository. It reads the day back from `--owner`,
     `--answered` and the day's log. It names each verdict as the seat and session that gave it, never as proof the
     work is right, and says what it cannot show. It asks the Owner how many times they carried a message between
     sessions by hand, and writes the number nowhere.
   - **The handover is `closeout`'s:** what merged, what is ready, what waits on the Owner, and tomorrow's asks filed
     as asks. It leaves `standup`, whose day ends when every ranked item is merged, ready or waiting on the Owner.
   - **`closeout-teams`**, the coordinator's, asks each planner for its close-out and gives one consolidated handover,
     each item linked to its source. It asks the hand-carried count once, for the whole day.
   - **What a close-out writes:** nothing it reads back changes, and it writes, commits and pushes nothing in the
     Owner's checkout, as today. Its one act is the handover's: tomorrow's asks, filed by the planner in its own
     worktree. The handovers are filed as decision 10 says.
   - **Off git it stays refused, as today:** on Subversion and in a plain folder the close-out row refuses and names
     why.
   - This supersedes FM-149's decision 3, `CLOSE-OUT.md`.
3. **The Board's buttons copy one line:** the skill's name, its mode, and the values the tool already fills and checks:
   the name, path, command and branch, every value through today's checks, and the setup it already tells apart. The
   labels stay in `labels.yaml`. **Which line where, as I propose it:**
   - **The row follows `[seats]` on the default branch,** as the gate reads the Owner, never the working tree.
     `coordinator` becomes a name the tool knows, with no built-in right.
   - **Where `[seats]` names no coordinator,** the stand-up row copies `standup` in direct mode, with that
     repository's values.
   - **Where it names a coordinator,** the Owner's sitting is the coordinator's, so the row copies `standup-teams`, the
     skill's name alone: the coordinator reads its teams from the roster (decision 9). The planner's report-mode line
     is the coordinator's to send, never the Owner's to paste, so no Board offers it.
   - **A second, smaller row there** copies `standup` in direct mode for this repository. It is the Owner's to paste
     when the coordinator is away, or when they want this team alone. The planner's report then says the sitting was
     held direct, so the coordinator's next page names it.
   - **The close-out rows** follow the same rule, on git (decision 2).
   - **The Designer checks the rows,** in English and German.
4. **Translation, as FM-149's decision 2:**
   - each `SKILL.md` is one English source;
   - the language is found as FM-149's decision 2 finds it, with its limit. `standup-teams` takes it from the
     repository whose Board the Owner copied its line from, else the language they write in;
   - in direct mode, the planner's conversation and report are in that language. A report sent in report mode is a
     message between seats and is English, as hails are, with ids as written;
   - the coordinator's consolidation is the one place translation happens across the teams. A translated ask is shown
     with its text as written beside it, and its id;
   - this supersedes FM-023's B of 29 October, the tracker folder's `standup.md`, and the `STAND-UP.md` design of 30
     October.
5. **The skills come in two layers.**
   - **The defaults ship with the tool:** `skills/<name>/SKILL.md` in shoalmark's own repository; in an adopter, the
     vendored `tools/shoalmark/skills/`, under the vendoring pin and `--vendor`'s per-file SHA-256 check. Nobody
     writes to them.
   - **The repository's own copy** is `<tracker dir>/skills/<name>/SKILL.md`, and it wins over the default. Only the
     Owner's signed commit changes it: the gate refuses a seat's change, with a class test and its mutant. It records
     `based-on:`, the default's version and sha256. The Board says when the default has changed since, and shows the
     diff.
   - **There is no per-person layer.**
   - **An upgrade costs no extra commit:** the vendoring commit carries the new defaults.
   - **A seat proposes a change to the Owner's copy** as a tracker with a draft patch, and the Owner commits it.
   - [README L305](https://github.com/shoalmark/shoalmark/blob/ec8479c68ffceb8afb545a3a745c58b310781b63/README.md#L305)
     keeps shoalmark/skills for blocks that work in any git repository without shoalmark. These skills run the tool.
6. **Each harness reaches a skill through a stub.**
   - **Claude Code:** `.claude/skills/<name>/SKILL.md`, as [its docs](https://code.claude.com/docs/en/skills) give it.
   - **Codex:** `.agents/skills/<name>/SKILL.md`. [OpenAI's page](https://developers.openai.com/codex/skills) scans
     `.agents/skills` from the working directory up to the repository root; the user scope is `$HOME/.agents/skills`;
     two skills of the same name are not merged, and both can appear; changes are detected without a restart.
   - **Each stub says only:** run `shoalmark.py --skill <name>` and follow what it prints. The tool picks the Owner's
     copy, else the default. It checks each against its pin or its committed blob, refuses one that matches neither,
     and prints which one it is, with its sha256. The Board shows the same line.
   - **The stubs are the Owner's path too:** the Owner's sessions reach the skills through them, as the seats' do, and
     only the Owner's signed commit changes them.
   - **The limits, stated plainly.** A seat under the Owner's OS user can edit a file on disk, or put a skill of the
     same name in the user scope (`~/.claude/skills`, `$HOME/.agents/skills`), and Claude Code runs a personal skill
     over a project skill of the same name. The tool detects what it can: the hashes, and a read-only look for a
     folder of the same name in those two places, with a warning. It reads nothing inside them. This tracker says
     "detected", never "impossible".
7. **The guard is FM-121's, and the place is FM-104's.**
   - [FM-121](FM-121-a-seat-can-change-the-seat-definitions-and-the-skills-folder.md) already holds the gate's
     refusal of a seat's change to the skills folder, after a design round. One design round covers the guard for
     both: the Owner's copies and the stubs.
   - **FM-104 blocks this tracker again, as I propose it.** The Owner's copies are the person's own files, and where
     those live is [FM-104](FM-104-the-person-s-own-files-are-spread-over-the-repository-and.md)'s to rule.
     `<tracker dir>/skills/` is this tracker's proposal to it, beside `TRIAGE.md` and `allowed_signers`, which already
     sit in the tracker folder. Where FM-104 rules another home for the person's files, the Owner's copies move with
     them. `blocked-by: FM-104` stays. FM-104 ranks first when v0.20.3 starts, so it holds back stage 1 by its own
     ruling alone (decision 13).
8. **Authority.** A go grants nothing and is no instruction. It tells the planner that the sitting is over, and names
   which ranked items of its own report the Owner held. The planner drives only what its repository's record already
   allows: the Owner's current path and their signed answers. A hold is obeyed as received, because it can only hold
   work back. A change of scope, rank or allocation moves nothing until it is a signed answer in the team's
   repository. A message carries no Owner authority, in either skill.
9. **Teams, from the roster spec.**
   - **This tracker does not define the roster.** A standalone, shoalmark-wide roster spec defines it, in a new public
     spec repository beside [shoalmark/hail](https://github.com/shoalmark/hail). A later edition of hail/1 takes its
     roster from it, in place of its own definition.
   - **`standup-teams` reads its teams from that roster.** The roster holds no session and no machine path. A team's
     place is one or more places, each a repository or a folder inside one; the coordinator finds each checkout and
     checks that its origin matches. Teams that share one folder are the roster spec's matter, not this tracker's.
   - **Each team is one planner,** for now.
   - **`[seats]` and the roster must agree:** `standup-teams` refuses a rostered repository whose default branch names
     no coordinator, and says which; `standup` in report mode refuses a request where its own repository names none.
   - **hail/1:** report mode needs hail/1 in force in every rostered repository, in the edition that takes its roster
     from the roster spec, pinned by commit when it is out. Today's text is hail/1's first edition,
     [at `f5b1606`](https://github.com/shoalmark/hail/blob/f5b160698a180481240dbff5c8cc605aaab06121/spec/hail-1.md),
     not yet in force. Elsewhere only direct mode is offered: where hail/1 is not in force, and on Subversion and in a
     plain folder, where its transport across teams is not there.
   - **In hail/1's terms,** the coordinator is the principal of a team of its own, and each planner is its team's
     principal, so every report and every outcome crosses from a principal to a principal
     ([§8](https://github.com/shoalmark/hail/blob/f5b160698a180481240dbff5c8cc605aaab06121/spec/hail-1.md#8-who-may-hail-whom)).
   - **The dependency:** `standup-teams` and `closeout-teams` wait until the roster spec is in force; the rest does
     not (decision 13).
10. **Filing, against the relay's shadow.**
    - **Each team's report and its sitting outcome** travel in hail/1 envelopes, so they are filed as hail/1 files
      every hail, as written, with their sha256: in that team's own folder of the shared private repository
      ([§10](https://github.com/shoalmark/hail/blob/f5b160698a180481240dbff5c8cc605aaab06121/spec/hail-1.md#10-the-record)),
      where its planner and the Owner read them.
    - **The page across the teams** is filed in the coordinator's own folder there, sealed so that only the Owner and
      the coordinator read it, and never in a team's repository.
    - **Every consolidated item links its source.** A planner keeps driving ranked work while it waits, as today's
      step 6.4.
    - **Rule 4 of the nine holds**
      ([AGENTS.md L109](https://github.com/shoalmark/shoalmark/blob/ec8479c68ffceb8afb545a3a745c58b310781b63/AGENTS.md#L109)).
      Each rostered repository names the coordinator in its own `[seats]` (decision 9), so a report to it stays within
      the repositories it serves. No team's internal state reaches another team's session: the outcome a planner
      receives names its own team's items only, and the section across the teams names a shared matter by its tracker
      id and what it holds up.
11. **The text:** [`docs/standup.md`](https://github.com/shoalmark/shoalmark/blob/ec8479c68ffceb8afb545a3a745c58b310781b63/docs/standup.md) and [`docs/de/standup.md`](https://github.com/shoalmark/shoalmark/blob/ec8479c68ffceb8afb545a3a745c58b310781b63/docs/de/standup.md) are
    rewritten in the same lane, by FM-149's decision 1: the German as "du", and "Board" as it stands. Every text a person
    reads gets its German twin.
12. **The lane is critical:** it changes what a session is handed and runs, and it adds a path only the Owner may
    change. The Designer checks the Board's rows beside a critical review.
13. **Allocation: v0.20.3, a chapter of [FM-139](FM-139-v0-20-3-s-rows-sit-in-fm-023-fm-006-and-fm-053-so-no-one.md), in two
    stages, as I propose them.**
    - **Stage 1** waits on FM-104's ruling alone: `standup` in both modes and `closeout`, the two layers and
      `--skill`, the stubs, the guard with FM-121's design round, the Board's direct row, the docs, and the Board's
      stand-up prompt retired.
    - **Stage 2** waits until the roster spec is in force: `standup-teams`, `closeout-teams`, and the coordinator's row
      with the direct row beside it.
    - Where the roster spec is not in force when v0.20.3 is otherwise ready, stage 2 moves to the next release by a
      dated line here, and stage 1 ships alone.

**What the answer's commit also does:** it marks FM-149's decision 3 superseded and strikes its last *Done when* item,
and corrects FM-139, FM-104 and FM-023's row B. It adds to FM-121 that its design round covers the Owner's copies and
the stubs.

## Done when

Each item names its commit or pull request when it lands.

- [ ] **The Owner has answered the ask,** FM-100-Q2 once it is put.
- [ ] **Stage 1: `standup` and `closeout`** stand in `skills/`, one English source each, with one test and one eval
  each, as FM-149's decision 2 has it: `standup` in both modes and the five setups, `closeout` on git and refused off
  git. The Board's stand-up prompt is gone, and `test_day_prompts.py` keeps only what the rows still need: the values'
  checks.
- [ ] **The two layers:** the defaults ship under the vendoring pin and `--vendor`'s per-file check. The gate refuses a
  seat's change to an Owner's copy or a stub, with a class test and its mutant. A test shows the Board naming a default
  changed since an Owner's copy's `based-on:`, with the diff.
- [ ] **`--skill <name>`** picks the Owner's copy, else the default, refuses one that matches neither its pin nor its
  committed blob, and prints which it is with its sha256, as the Board does. A test covers each case, and one covers
  the same-name warning, run with a scratch home.
- [ ] **The stubs** for Claude Code and Codex say only the one line, and a test pins it.
- [ ] **The Board's rows copy one line each,** as decision 3 sets out. A class test holds that they copy only checked
  values and no prompt text, and that a change to `[seats]` off the default branch does not switch them. Their labels
  are in English and German.
- [ ] **Authority:** each skill's text holds decision 8, pinned by a test of its lines, and an eval shows a planner that
  does not start work a go names but the record does not allow.
- [ ] **Stage 2: `standup-teams` and `closeout-teams`** stand beside them, after the roster spec is in force. Tests
  hold that `standup-teams` never runs a command it prints; that it reads its teams from the roster, checks each
  checkout's origin, and refuses a rostered repository whose default branch names no coordinator; and that a team
  without a report is listed as *no report* and gets no go.
- [ ] **Filing:** each report, each sitting outcome and each page across the teams is filed as decision 10 says, with
  its sha256, and a test checks the sha256 against the filed bytes.
- [ ] **Language:** as decision 4, and a test pins the report's keys.
- [ ] **README L320's row** describes the skills in place of the prompts.
- [ ] **`docs/standup.md` and `docs/de/standup.md`** describe the skills, and their pair check passes.
- [ ] **The Designer's check and the critical review are READY.**

## Asks

**FM-100-Q1** · 2026-11-12 · Are FM-100's decisions taken, as its section Decisions, for the Owner sets out, superseding FM-149's decision 3 and the STAND-UP.md design of 30 October, with the lane in v0.20.3?
**withdrawn** — no answer was given

## Ship log

| Date | Event |
|---|---|
| 2026-11-12 | FM-100-Q1 withdrawn, no answer given; its changed question is drafted, with no id until it is put. Records only. |
| 2026-11-12 | Revised after its design audit; the findings are recorded privately. Records only. |
| 2026-11-12 | The ask is held back until its design audit is READY; the audit's findings are recorded privately. Records only. |
| 2026-11-12 | Rewritten on the Auditor's word: the stand-up and the close-out split by seat into skills, with FM-100-Q1, which supersedes FM-149's decision 3 and the `STAND-UP.md` design of 30 October. Records only. |
| 2026-11-04 | `epic: FM-139`: a chapter of v0.20.3's epic. Records only. |
| 2026-11-04 | Its open question, the close-out prompt's form, put to the Owner as FM-149's decision 3 (ask FM-149-Q1). Records only. |
| 2026-10-30 | Blocked by FM-104, which decides where the person's files live, on the Owner's word of 30 October. Records only. |
| 2026-10-30 | Filed for v0.20.3, on the Owner's word of 30 October. Records only. |
