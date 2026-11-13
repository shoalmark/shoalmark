---
id: FM-139
status: Proposed
considered: FM-023, FM-089, FM-006, FM-053
tags: process
next: owner
hook: "v0.20.3's allocation in one place: the rows and trackers the release holds, which sat in FM-023, FM-006 and FM-053. It ships at v0.20.3's tag."
ask-id: FM-139-Q1
ask: "Do you take v0.20.3's scope as FM-139 proposes: every roster lane in; sealanes/1's first edition, its cases and validator, and hail's edition 3 public before the tag; FM-115, FM-086 and FM-169 in, FM-169's round first and its commits before the migrating commit; FM-118 and FM-076 to v0.20.4?"
ask-kind: ruling
ask-since: 2026-11-13
ask-options: "yes, as proposed | yes, with the changes I name | no, not now"
ask-proposal: "yes, as proposed"
---

# FM-139 — v0.20.3's rows sit in FM-023, FM-006 and FM-053, so no one tracker says what the release holds

## What is true now

**2026-11-03 — filed; it holds v0.20.3's allocation, and nothing is built.** On the Owner's word of 29 October, each
release's allocation from v0.20.3 on is a tracker of its own, which ships at that release's tag
([FM-023](FM-023-a-plan-names-its-seats-their-estimates-and-when-the-person.md)). Until now v0.20.3's rows sat in
FM-023, [FM-006](FM-006-shoalmark-has-one-document-written-for-agents-the-humans-who.md) and
[FM-053](FM-053-the-board-s-design-for-v0-20-1-is-the-owner-s-word.md). FM-023's and FM-006's rows of 1 November move
here. FM-053's are in [FM-123](FM-123-the-board-s-polish-that-v0-20-1-left-is-not-built-a-verdict.md). FM-023's dated
entries stay as the record of each ruling, and the rows they name are listed here.

**2026-11-04 — v0.20.3's epic, on the Owner's word in chat.** Said of shoalmark's list of epics with their
chapters, the Board's story view ([`shoalmark.py` L4487](https://github.com/shoalmark/shoalmark/blob/35158e3be3f9e110d2a5e1536e385fb01ca158cf/shoalmark.py#L4487)): "I want v0.20.3 to show in
that list, everything we decide goes under this." Then: "Everything allocated to v0.20.3, yes. Move the proposed
and the candidates in too, so that we can decide what goes in tomorrow."
- FM-139 is v0.20.3's epic.
- Its chapters are the trackers allocated to v0.20.3, and the proposed and the candidates, which are not placed.
- The Owner decides on 5 November which of the proposed and the candidates go in. A tracker not taken leaves the
  epic in the commit that records that decision.
- From then on, a tracker carries `epic: FM-139` from the commit that allocates it.
- FM-089's parts stay under FM-089, which is itself a chapter of FM-139, as FM-088 is a chapter of FM-089 and the
  epic of FM-130 to FM-133.

**2026-11-05 — v0.20.3's allocation sitting, on the Owner's word.** v0.20.3 takes FM-149, FM-150, FM-151 and FM-099,
which stay chapters of this epic. FM-095 to FM-098 are not taken: they leave the epic in this commit and stay filed for
v0.20.x.

**2026-11-12 — [FM-159](FM-159-a-session-can-be-resumed-from-the-board-only-for-24-hours.md) proposed for v0.20.3, with FM-159-Q1 open.** A
"sessions · this week" section beside "reviews · this week", each parent session of the last 7 days with its resume
command, and "the day" informational. It is a chapter of this epic until the Owner decides whether it goes in.

**2026-11-12 — [FM-160](FM-160-the-coordinator-seat-has-no-icon-so-its-session-row-keeps-an.md) proposed for v0.20.3, with FM-160-Q1 open.** The
coordinator seat's icon, variant B, with its README row and the words an eighth seat touches. It is built after the
seat's pull request merges, and it is a chapter of this epic until the Owner decides whether it goes in.

**2026-11-12 — [FM-100](FM-100-the-stand-up-prompt-is-code-and-english-on-every-board-while.md) rewritten, with FM-100-Q1 open.** The stand-up and
the close-out split by seat into skills, the Owner's sitting to the coordinator and each team's day to its planner, in
the person's language. Its ask places the lane in v0.20.3, and it stays a chapter of this epic.

**2026-11-12 — [FM-162](FM-162-the-acts-a-seat-must-never-do-are-held-only-as-prose-so-one.md) proposed for v0.20.3, with FM-162-Q1 open.** A
seat guard refuses five acts before they run, through each harness's own hooks, and names the rule and a safe
alternative. It is a chapter of this epic until the Owner decides whether it goes in.

**2026-11-13 — FM-139-Q1 put: v0.20.3's scope, on the coordinator's word of that day.** sealanes/1's design went through its
audit on 13 November. Below are the proposal and the plan's dates. The lists below this entry change only with the answer: a
tracker not taken leaves the epic in the commit that records that decision.

**The proposal:**
1. **Every roster lane in v0.20.3:**
   - [FM-166](FM-166-seats-and-rights-are-kept-in-shoalmark-toml-s-own-tables.md) is built as ten lanes from one
     contract cut from sealanes/1's final design, instead of as one lane. [FM-165](FM-165-a-tracker-can-only-be-closed-by-hand-so-its-open-asks-where.md)
     follows its list of acts.
   - sealanes/1's first edition, its conformance cases and its file-only validator are public before the tag, and
     hail's edition 3 is public with them, as [FM-168](FM-168-a-spec-s-conformance-tests-are-prose-so-no-implementation.md) proposes.
   - The validator is a program of the spec's own in shoalmark/sealanes (not yet public). It uses Python's standard
     library only, and a seat that builds no tool lane writes it.
   - FM-166's changed question is put once this ask is answered, naming v0.20.3.
2. **[FM-115](FM-115-the-owner-answers-each-ask-in-the-board-s-one-dialog-and-no.md) and [FM-086](FM-086-a-tracker-states-one-deliverable-and-closes-when-it-ships.md) stay in v0.20.3.**
3. **[FM-169](FM-169-the-owner-s-personal-address-stands-in-the-public.md) joins v0.20.3, in this order:**
   1. its design round, from day 1;
   2. the ask that round drafts, answered by the Owner;
   3. its lane;
   4. the Owner's own signed commits, in the order the round sets. FM-169's decision 3 proposes two: first the keys
      listed under the forge noreply address, then the personal address removed from `owner` and the signers file.

   The plan places those commits before the release pull request. So they land before shoalmark's migrating commit,
   the commit that replaces its `[seats]` and `[rights]` with the roster, and the address never enters a roster.
4. **[FM-118](FM-118-shoalmark-py-s-prose-is-not-pruned-and-nothing-holds-code.md) and [FM-076](FM-076-a-seat-s-work-that-only-another-seat-can-push-is-refused-or.md) move to v0.20.4.**
5. **FM-088 and FM-130 to FM-133 leave v0.20.3** for shoalmark/chart (not yet public), as their lines of 13 November
   say. They close with `--close --moved-to` once FM-165 lands.
6. **The rest stays as listed below:**
   - FM-089 with FM-087;
   - FM-104, FM-120, FM-140, FM-119 and FM-121;
   - FM-123, and BF-110 to BF-113 with [FM-159](FM-159-a-session-can-be-resumed-from-the-board-only-for-24-hours.md) on the same session rows;
   - FM-099, FM-105, FM-106, FM-101, FM-102 and FM-141;
   - FM-143, FM-149, FM-150 and FM-151;
   - FM-160, FM-162, [FM-164](FM-164-subversion-support-is-deprecated-then-removed-while-the-vcs.md) and [FM-167](FM-167-the-owner-s-act-on-an-ask-has-no-fixed-name-so-the-board.md);
   - [FM-163](FM-163-the-drift-skills-name-no-id-forms-read-no-harness-settings.md)'s shoalmark/skills 1.1.0, whose tag v0.20.3 pins;
   - FM-100's stage 1;
   - [FM-083](FM-083-nothing-measures-how-well-a-skill-does-its-work-only-its.md) and [FM-084](FM-084-queue-does-not-show-a-pull-request-s-ci-so-a-failing-check.md), which the Owner's answers of 28 October
     allocated to v0.20.3, on the list below from 13 November;
   - the rows.
7. **FM-100's stage 2** needs the roster in force in shoalmark. That comes with the Owner's commits in person after the
   tag, so stage 2 ships in the next release, by FM-100's own fallback. FM-100-Q2 is withdrawn, and its changed
   question is put after this answer.
8. No tracker enters v0.20.3 after this answer but by another signed answer of the Owner's. Main is frozen from the
   release pull request to the tag.

**The plan's dates:**
- Counted in working days from 13 November, with twelve lanes in flight, for the scope above with the validator.
- S is the day FM-166's changed question gets its signed answer.
- Slower assumptions are in brackets.

| Point | S on day 2 | S on day 4 |
|---|---|---|
| sealanes/1's text ready | 3.1 (3.8) | 3.1 (3.8) |
| hail's edition 3 ready | 4.8 (6.2) | 4.8 (6.2) |
| The cases ready | 5.5 (7.2) | 5.5 (7.2) |
| The publication, the Owner's act | 7.8 (11.0) | 7.9 (10.8) |
| FM-169's commits, the Owner's | 7.5 (9.1) | 6.1 (8.5) |
| FM-166's lanes joined | 10.0 (13.0) | 12.1 (14.9) |
| FM-100's stage 1 ready | 10.6 (13.0) | 10.6 (13.7) |
| **v0.20.3's tag** | **11.6 (14.3)** | **13.1 (16.1)** |
| After the tag: the Owner's commits in person that put the roster in force | 14.2 (17.6) | 15.6 (19.5) |
| FM-100's stage 2 ready, for the next release | 16.9 (21.1) | 18.4 (23.0) |

- **FM-169's round** is ready about day 2.1 (2.7), and its ask is answered about day 3. Its lane is ready about day 5.6
  to 7.0 (7.9 to 8.5).
- **What sets the tag:**
  - with S on day 2 or before, FM-104's chain: its round, the Owner's sitting, the layout, then FM-100's stage 1;
  - with S after about day 2, FM-166's lanes. From day 4 on, each later day of S moves the tag by about 0.9 days.
- **Built as one lane** instead of ten, FM-166 would put the tag at 14.3 with S on day 2, and 16.4 with S on day 4.
- **With the roster in v0.20.4 instead,** and the rest as proposed, v0.20.3's tag would come at about 11.5. Keeping the
  roster in v0.20.3 costs about 0.1 days with S on day 2, and 1.5 days with S on day 4.
- **Confidence,** with S within four days: 50 % that the tag comes within 13 working days, and 80 % within 16.

**The chapter, and the trackers filed for v0.20.3:**
- [FM-089](FM-089-agentic-seamanship-v0-20-3.md), Agentic seamanship, with its parts [FM-086](FM-086-a-tracker-states-one-deliverable-and-closes-when-it-ships.md), [FM-087](FM-087-evidence-comes-in-three-classes-what-decides-stays-with-the.md) and [FM-088](FM-088-the-team-s-lessons-live-only-in-each-harness-s-local-memory.md). FM-088's four
  trackers are [FM-130](FM-130-the-team-s-and-each-seat-s-memory-is-not-in-the-repository.md), [FM-131](FM-131-a-session-starts-without-the-team-s-memory.md), [FM-132](FM-132-nothing-moves-a-lesson-out-of-a-harness-s-memory.md) and [FM-133](FM-133-a-memory-entry-is-never-tested-or-retired.md).
  [FM-095](FM-095-the-owner-s-rulings-live-in-chat-memories-and-briefs-not-in.md) to [FM-098](FM-098-nothing-leads-from-a-commit-to-the-conversation-behind-it.md), filed for v0.20.x as the chapter's candidates, were not taken on 5 November.
- [FM-104](FM-104-the-person-s-own-files-are-spread-over-the-repository-and.md): the person's own files in one home, rank 1 when v0.20.3 starts.
- [FM-120](FM-120-the-rule-files-hold-the-disagreements-and-obsolete-text-that.md): a fresh `/find-drift` run on shoalmark and the `/prune-drift` run that fixes what it finds, v0.20.3's
  first lane.
- [FM-100](FM-100-the-stand-up-prompt-is-code-and-english-on-every-board-while.md): the stand-up prompt from the language pack, with FM-030's B.
- [FM-115](FM-115-the-owner-answers-each-ask-in-the-board-s-one-dialog-and-no.md): S3 and S4 of FM-059's design.
- [FM-118](FM-118-shoalmark-py-s-prose-is-not-pruned-and-nothing-holds-code.md), [FM-119](FM-119-five-rules-held-only-as-prose-are-not-checks.md) and [FM-121](FM-121-a-seat-can-change-the-seat-definitions-and-the-skills-folder.md): the prose prune with its ratchet, the five conversions, and FM-037's
  guard.
- [FM-123](FM-123-the-board-s-polish-that-v0-20-1-left-is-not-built-a-verdict.md): the board's polish, with v0.20.3's design rows of 1 November.
- [FM-099](FM-099-the-index-names-the-command-of-the-system-that-wrote-it-so-a.md): placed in v0.20.3 on 5 November.
- [FM-076](FM-076-a-seat-s-work-that-only-another-seat-can-push-is-refused-or.md): moved to v0.20.3, on the Owner's word of 29 October.
- Filed on this records branch for v0.20.3: [FM-105](FM-105-no-test-holds-that-a-refused-signature-then-a-signed-answer.md), [FM-106](FM-106-eight-done-when-items-of-trackers-closed-at-v0-20-2-have-no.md), [FM-140](FM-140-a-root-test-file-can-sit-outside-ci-run-by-no-job-and-named.md), [FM-101](FM-101-nothing-holds-that-the-suite-keeps-a-runner-s-own-sigterm.md),
  [FM-102](FM-102-the-stand-up-and-queue-disagree-on-an-origin-that-an.md) and [FM-141](FM-141-the-readme-s-refusal-table-lacks-s1-s-ask-id-refusals-and.md).
- Since 4 November: [FM-143](FM-143-installing-two-skills-clones-all-of-shoalmark.md)'s work, allocated to v0.20.3 by its decision
  *Allocation*, which the answer to FM-143-Q1 took ([#260](https://github.com/shoalmark/shoalmark/pull/260)); and
  [FM-149](FM-149-the-docs-the-board-s-prompts-and-the-skills-have-no-one-rule.md),
  [FM-150](FM-150-the-gate-passes-an-ask-without-next-owner-and-it-reaches-no.md) and
  [FM-151](FM-151-a-records-only-pull-request-waits-for-a-macos-runner-that.md), placed in v0.20.3 on 5 November, FM-150 and FM-151
  each by its decision *Allocation*.
- On this list from 13 November: [FM-083](FM-083-nothing-measures-how-well-a-skill-does-its-work-only-its.md), the suite for skills, and
  [FM-084](FM-084-queue-does-not-show-a-pull-request-s-ci-so-a-failing-check.md), the check word in `--queue`, which the Owner's answers of 28 October
  allocated to v0.20.3.

**The rows FM-023's entries name for v0.20.3:**

| Row | Ruled | Tracker |
|---|---|---|
| S3, who asked, the receipts and S4, from batch 3; after S1. | 27 October | FM-115 holds S3 and S4 |
| From 18 October's allocation: the prose prune of `shoalmark.py` with the comment ratchet, FM-037's guard, the five conversions, and the text fixes; after v0.20.2's tag. | 27 October | FM-118, FM-121, FM-119; the text fixes have none |
| B: the Board copies the tracker folder's `standup.md`, guarded like the Owner's two sections, and names the text it copied (FM-030). | 29 October | FM-100 |
| The CI class fix, whole, with its three findings. | 29 October | FM-140 |
| FM-076, relayed commits. | 29 October | FM-076 |
| The stand-up agenda's "· 15 min ·" in code. | 30 October | — |

**Moved here from FM-023, its rows of 1 November, from 30 and 31 October:**
- `--check` prints "(none)", on the Owner's yes of 30 October.
- The help lines' hide mark, on the Owner's yes of 30 October.
- RV-4233: recorded privately.
- RV-4192: recorded privately.
- RV-4193: recorded privately.

**Moved here from FM-006, its site and gate rows of 1 November, from 30 and 31 October:**
- The twin padding gate in `check_site.py`: its why-comment and `door_paddings`' docstring came out in `5b87cc2`,
  and the new helpers have no docstrings.
- `weight()` counts pseudo-classes: done in `5b87cc2`; this row is closed.
- `scripts/test_check_site.py` on Python 3.9: five `write_text(newline=)` errors.
- The Cloudflare gate, on the Owner's yes of 30 October.

**Moved here from FM-006, its German rows of 1 November, from 30 October:**
- C4 on the shipped German table.
- *Bestätigung* / *Freigabe* for the meaning pass.

**New rows:**
- Quick win 10: `--sessions` gains the harness and resume columns. FM-023's entry of 29 October moves it to v0.20.3
  unless READY by 29 October, 20:00, and it is not in v0.20.2's release branch.
- From the check of the drift skills' five-part change (#252), on the Owner's word of 1 November:
  - the stand-up names a waiting drift report and its open decisions;
  - the person's yes files the open drift decisions as asks, on the Board and in the stand-up;
  - the probe's "already adopted" path points to the upgrade.
- The open German term T1: "Forge" or "Ablage" on the Board's labels, for the glossary.
- Descriptions of their own for the other German pages, under the Translator's v0.20.3 pass (FM-006's close).
- On the Owner's word of 5 November, three rows from the test suite:
  - a check that copies the tool or a fixture into a temp folder of its own removes the copy when it is done;
  - the pinned-zones block pins the tool's day in a way Python 3.15 honours, so it runs there instead of
    skipping;
  - a timeout in the CI install check is recorded as one FAIL line, naming the step and its limit, and the run
    goes on. The landing block's mutant helper records a missing target as a problem, instead of stopping the
    run.

**Four Designer findings on the Board's session rows, for v0.20.3,** on the Owner's word of 2 November:

| Row | What v0.20.3 does |
|---|---|
| BF-110 | A session row that wraps on the Board goes on under its id, not under the open-and-close marker, at 390 px and at 1280. |
| BF-111 | The reason a session row gives when the paste check declines a folder is drawn grey, like every other reason. Drop the `hot` class in `rsm` and the `.rw:not(.hot)` rule. |
| BF-112 | The read-at line keeps its time whole at 390 px. Today it breaks at the date's hyphen, wherever the folder name puts it. No fix has been measured. |
| BF-113 | A session row's worktree name moves to the next line whole at 390 px, as BF-11's rule already has it for names in rows. No fix has been measured. Any fix changes the row prefix that `test_resume_command.py` pins. |

- **BF-110's measured fix:** CSS only, in the Board's style in `shoalmark.py`. Each old string is found once:
  1. old `details.grp>summary{padding:3px 0}`; new
     `details.grp>summary{padding:3px 0 3px 2ch;text-indent:-2ch}details.grp>summary>*,details.grp>summary:before{text-indent:0}`
  2. old `details.grp .subs{display:block;padding-left:2ch;color:var(--dim)}`; new
     `details.grp .subs{display:block;padding-left:0;color:var(--dim)}`
  3. old `details.grp .rsc:not([hidden]){display:block;padding-left:2ch;user-select:all;overflow-wrap:anywhere}`; new
     `details.grp .rsc:not([hidden]){display:block;padding-left:0;user-select:all;overflow-wrap:anywhere}`
  4. old `details.grp .rsc:not([hidden])+.said{display:block;margin-left:0;padding-left:2ch}`; new
     `details.grp .rsc:not([hidden])+.said{display:block;margin-left:0;padding-left:0}`
- **What was measured,** on built copies at 390 and 1280:
  - each row's lines after the first start under the id, and a wrapped button 9 px further in;
  - every row's height is unchanged;
  - the help line and the members' lines don't move;
  - there is no overflow.
- **The tests that change with it:** the pinned page lines in `test_git_entry_differential.py`, which are the session
  summary's line and the resume page lines.

## Why

A release whose rows are spread over three trackers has no one place that says what it holds, so a row is easy to miss
at its allocation sitting and at its tag.

## Done when

- [ ] v0.20.3's allocation sitting places each row and tracker here, and this tracker records it.
- [ ] At v0.20.3's tag, each row and tracker here has shipped, or has moved by the Owner's word, with its line here.

## Ship log

| Date | Event |
|---|---|
| 2026-11-03 | Filed as v0.20.3's allocation, with FM-023's and FM-006's rows of 1 November moved in. Records only. |
| 2026-11-04 | FM-143's allocation joins the list, and FM-149, FM-150 and FM-151 join it as proposed. Records only. |
| 2026-11-04 | v0.20.3's epic, on the Owner's word in chat, logged under *What is true now*. Records only. |
| 2026-11-05 | v0.20.3's allocation sitting: FM-149, FM-150, FM-151 and FM-099 are taken, and FM-095 to FM-098 leave the epic. Records only. |
| 2026-11-05 | Three test-suite rows placed in v0.20.3, on the Owner's word. Records only. |
| 2026-11-12 | FM-159 proposed for v0.20.3 with FM-159-Q1, a chapter of this epic until the Owner decides. Records only. |
| 2026-11-12 | FM-160 proposed for v0.20.3 with FM-160-Q1, a chapter of this epic until the Owner decides. Records only. |
| 2026-11-12 | FM-100 rewritten with FM-100-Q1: the stand-up and the close-out as skills by seat. Records only. |
| 2026-11-12 | FM-162 proposed for v0.20.3 with FM-162-Q1, a chapter of this epic until the Owner decides. Records only. |
| 2026-11-13 | FM-139-Q1 put: v0.20.3's scope with the plan's dates and the cut-off, FM-169 joining it. FM-083 and FM-084 join the list, as the Owner's answers of 28 October allocated them. Records only. |
