---
id: FM-159
status: Proposed
considered: FM-023, FM-024, FM-031, FM-078, FM-123, FM-139
tags: process
epic: FM-139
next: owner
hook: "The Board gives a resume command only to the sessions of the last 24 hours, so a session closed two days ago has no way back on it. Its paste check never asks whether the folder or the log is still there, so over a week a command could fail on paste."
ask-id: FM-159-Q1
ask: "Are FM-159's decisions taken, as its section Decisions, for the Owner sets out, with the lane in v0.20.3?"
ask-kind: ruling
ask-since: 2026-11-12
ask-options: "yes, as proposed | yes, in a release after v0.20.3 | no"
ask-proposal: "yes, as proposed"
---

# FM-159 — a session can be resumed from the Board only for 24 hours, and its command can name a folder that is gone

Seat: the Planner (27f31560) · filed 2026-11-12, on the Auditor's word of that day.

## What is true now

**2026-11-12 — filed, Proposed, with FM-159-Q1; nothing is built.** Read at main `ec8479c`:

1. **Only the day's sessions get a resume command.**
   - `board_sessions` reads the resume commands for the parents and members of the day's strip alone
     ([`shoalmark.py` L10067–L10087](https://github.com/shoalmark/shoalmark/blob/ec8479c68ffceb8afb545a3a745c58b310781b63/shoalmark.py#L10067-L10087)).
   - `session_groups` keeps a parent only where it or a sub-session committed in the last `SESSION_RECENT` seconds,
     86400 ([L8114](https://github.com/shoalmark/shoalmark/blob/ec8479c68ffceb8afb545a3a745c58b310781b63/shoalmark.py#L8114),
     [L10023–L10054](https://github.com/shoalmark/shoalmark/blob/ec8479c68ffceb8afb545a3a745c58b310781b63/shoalmark.py#L10023-L10054)).
   - So a session whose last commit is 25 hours old leaves the Board with its command, though its log and folder are
     still on the machine.
   - "reviews · this week" reads `triage_days`, 7 by default, the tool's one window
     ([L931–L932](https://github.com/shoalmark/shoalmark/blob/ec8479c68ffceb8afb545a3a745c58b310781b63/shoalmark.py#L931-L932),
     [L9945–L9955](https://github.com/shoalmark/shoalmark/blob/ec8479c68ffceb8afb545a3a745c58b310781b63/shoalmark.py#L9945-L9955)).
2. **The paste check never asks whether the folder is there.** `resume_folder_problem` refuses a folder that is
   relative, longer than `DAY_CAP` (200 characters), or holds a character outside the plain set, and passes any other
   ([L8408–L8419](https://github.com/shoalmark/shoalmark/blob/ec8479c68ffceb8afb545a3a745c58b310781b63/shoalmark.py#L8408-L8419),
   [L5289](https://github.com/shoalmark/shoalmark/blob/ec8479c68ffceb8afb545a3a745c58b310781b63/shoalmark.py#L5289)). A folder
   moved or removed since the session's first turn still gets a command, and it fails on paste. Over a day that is
   rare; over a week it is likelier.
3. **A log the harness has removed reads as no log.** `resume_commands` gives nothing for a session that no log on this
   machine starts with, "as one from another machine"
   ([L8433–L8473](https://github.com/shoalmark/shoalmark/blob/ec8479c68ffceb8afb545a3a745c58b310781b63/shoalmark.py#L8433-L8473)).
   The row then shows neither a command nor a reason. The Board reads the logs' file names alone, so it cannot tell a
   removed log from one on another machine.
4. **Codex's ids collide.** They start with the time, so their first 8 characters can match. `["two", n]` then says how
   many logs start with the id, and picks none
   ([L8455](https://github.com/shoalmark/shoalmark/blob/ec8479c68ffceb8afb545a3a745c58b310781b63/shoalmark.py#L8455)).
   Over 7 days such a collision is likelier than over one.
5. **The rule that holds:** the sessions are read from the commits' trailers alone, never from a transcript
   ([L10029](https://github.com/shoalmark/shoalmark/blob/ec8479c68ffceb8afb545a3a745c58b310781b63/shoalmark.py#L10029)).
   The resume command reads a log's file name and its first turn's folder, never what a session said
   ([FM-024](FM-024-a-seat-s-commit-names-its-session-and-the-record-knows-the.md), 23 October). A session that never
   committed here, such as a review or a go-to-market session, or one that committed in another repository, is not
   listed.
6. **Where the words and the design stand:**
   - the English labels of the day, its sessions and the resume command
     ([L4621–L4645](https://github.com/shoalmark/shoalmark/blob/ec8479c68ffceb8afb545a3a745c58b310781b63/shoalmark.py#L4621-L4645));
   - the German ones ([`examples/de/labels.yaml` L110–L122](https://github.com/shoalmark/shoalmark/blob/ec8479c68ffceb8afb545a3a745c58b310781b63/examples/de/labels.yaml#L110-L122),
     [L248](https://github.com/shoalmark/shoalmark/blob/ec8479c68ffceb8afb545a3a745c58b310781b63/examples/de/labels.yaml#L248),
     [L263](https://github.com/shoalmark/shoalmark/blob/ec8479c68ffceb8afb545a3a745c58b310781b63/examples/de/labels.yaml#L263));
   - the strip's script ([L4439–L4443](https://github.com/shoalmark/shoalmark/blob/ec8479c68ffceb8afb545a3a745c58b310781b63/shoalmark.py#L4439-L4443));
   - the design guide, which puts the sessions inside the day
     ([`brand/design-guide.md` §1, L19–L21](https://github.com/shoalmark/shoalmark/blob/ec8479c68ffceb8afb545a3a745c58b310781b63/brand/design-guide.md#L19-L21))
     and orders the Owner's box ([§7, L308](https://github.com/shoalmark/shoalmark/blob/ec8479c68ffceb8afb545a3a745c58b310781b63/brand/design-guide.md#L308)).
7. **What pins it:** [`test_resume_command.py`](https://github.com/shoalmark/shoalmark/blob/ec8479c68ffceb8afb545a3a745c58b310781b63/test_resume_command.py)
   is the resume command's class test, and
   [`test_git_entry_differential.py`](https://github.com/shoalmark/shoalmark/blob/ec8479c68ffceb8afb545a3a745c58b310781b63/test_git_entry_differential.py)
   pins the strip's script lines and the resume labels in English and German.
8. **The session rows' four Designer findings,** BF-110 to BF-113 in
   [FM-139](FM-139-v0-20-3-s-rows-sit-in-fm-023-fm-006-and-fm-053-so-no-one.md), are v0.20.3's too. Both they and this
   lane change the session row and its pins, so the lane's brief says how the two are ordered.

## Why

The Board is where a person finds the way back into a session. A session closed the day before yesterday has none
there, though its log and folder are still on the machine. And a command that fails on paste is worse than none: the
Board offers it as the way back.

## Decisions, for the Owner

1. **A section of its own, "sessions · this week",** after the day and beside "reviews · this week":
   - it lists each parent session with a commit in the last 7 days, rolling, whether the commit is its own or a
     sub-session's: `session_groups` over `triage_days`, the window "reviews · this week" reads, so *this week* is one
     window on the page;
   - each row carries the parent's resume command (`resume_commands`), or the reason it has none;
   - today's sessions are in it too, so there is one place to resume from.
2. **Sub-sessions get no row and no command there.** They appear only as text on the parent's row: the runs line,
   such as `builder 1–6 · reviewer 1–5, 7`, so a reader sees what the session worked on.
3. **"the day" becomes informational.** It keeps its 24-hour strip, with its rows and members, without a resume command.
   The digest (`--owner`) keeps its 24-hour list. No command goes into `--owner`, `--standup`, a view or a file git
   tracks, as today.
4. **Three states of their own,** each with its own words, and none of them a command that fails on paste:
   - **the folder is gone:** the first turn's folder is no folder on this machine when the Board is built, because it
     was moved or removed;
   - **not resumable here:** no log on this machine starts with the session's id. The row says so, and that the harness
     may have removed the log or the session ran elsewhere, since the Board cannot tell which;
   - **colliding ids:** `["two", n]` stays and never picks one. Where the logs are Codex's, its words say that Codex's ids
     start with the time.

   `resume_folder_problem` keeps its three refusals. The named limit stays: a folder that is there but holds another
   checkout is not seen. Each state holds at the moment the Board was built, which its read-at line names.
5. **The Board's rule holds:** sessions from trailers alone, never from transcripts. The section's help line says it
   lists the sessions that committed here, so one that never committed here, or committed elsewhere, is not missing by
   mistake.
6. **Words and tests:**
   - the new labels in English and German (du), with the label pins. The words are proposals until the Owner rules
     them, before the merge;
   - `test_resume_command.py` reads the week's section, and a class test holds each state, with a mutant that drops
     each one failing;
   - the differential's pinned lines change with the page;
   - the design guide's §1, §7 and §8 say where the sessions now stand.
7. **The build:** a rendered-surface lane, with the Designer's check of the page beside its review.
8. **Allocation:** v0.20.3, a chapter of FM-139.

## Done when

Each item names its commit or pull request when it lands.

- [ ] **"sessions · this week"** lists each parent session with a commit in the last 7 days, today's included, with
  its resume command or the reason it has none; sub-sessions appear only in the parent's runs line.
- [ ] **"the day"** keeps its 24-hour strip without a resume command, and `--owner` keeps its 24-hour list.
- [ ] **A folder that is gone, a session with no log here, and colliding ids** each have their own state and words,
  and none of them gives a command.
- [ ] **The labels** stand in English and German (du), pinned, in the Owner's words.
- [ ] **`test_resume_command.py` and a class test for each state** pass, and each state's mutant fails.
- [ ] **The design guide** says where the sessions stand, and the Designer's check and the review are READY.

## Ship log

| Date | Event |
|---|---|
| 2026-11-12 | Filed, Proposed, with FM-159-Q1, on the Auditor's word: `epic: FM-139`, under v0.20.3's epic until the Owner decides whether it goes in. Nothing is built. |
