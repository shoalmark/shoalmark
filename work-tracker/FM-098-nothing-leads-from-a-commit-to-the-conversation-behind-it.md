---
id: FM-098
status: Proposed
considered: FM-024, FM-078, FM-088, FM-096, FM-097
tags: seamanship
hook: "A commit names the session that made it, but nothing leads from the commit to the conversation behind it. Zed's DeltaDB now keeps edits linked to their conversation; one decision, on the Owner's signed answer, picks whether shoalmark links a commit's session to its transcript, and how."
---

# FM-098 — nothing leads from a commit to the conversation behind it

## What is true now

**Filed 2026-10-29 for v0.20.x, as a decision; nothing is built.** On the Owner's word of 29 October: a tracker of its
own, for agentic seamanship, so that it is revisited in more detail with its own Planner session. It is considered for
every v0.20 release and pulled into one when it fits. [FM-089](FM-089-agentic-seamanship-v0-20-3.md), v0.20.3's chapter,
names it as a candidate, not a part.

- **The first case:** Zed launched DeltaDB on 29 October 2026 (delta.dev).
  - It is a version control for agent context. It keeps every edit between commits linked to the conversation that
    made it.
  - It syncs through a Claude Code plugin. Codex and Pi are announced.
- **What shoalmark has:** shoalmark's commits name their session
  ([FM-024](FM-024-a-seat-s-commit-names-its-session-and-the-record-knows-the.md)), but nothing leads from a commit to
  the conversation behind it, wherever a person keeps it.
- **A session's material can be private.** shoalmark never uploads it. Whether a person sends it to a hosted service is
  that person's choice.
- **It is a decision tracker, sized to one decision.** A build, if one is chosen, is a tracker of its own.

## Why

A reviewer, an auditor or the person in charge may need to read why a change was made, not only what it changed. The
session's name says who made it. The conversation says why.
[FM-078](FM-078-model-and-effort-have-no-harness-neutral-record.md) and
[FM-088](FM-088-the-team-s-lessons-live-only-in-each-harness-s-local-memory.md) hold other parts of what a session
leaves behind, and [FM-096](FM-096-nothing-measures-whether-a-session-follows-the-rules-and.md) and
[FM-097](FM-097-find-drift-does-not-audit-the-owner-s-rulings-whether-each.md) would read a link if there were one.

## Done when

- [ ] A study by this tracker's own Planner session: what DeltaDB stores and where, under which terms, its interplay
  with Git, its signing and retention, and which harnesses it supports by then.
- [ ] The options set out:
  - no link;
  - an optional link from a commit's session to its transcript that works on any harness, resolved where the person
    keeps the transcript, and never uploaded by shoalmark;
  - an integration with one product.
- [ ] The Owner's signed answer picks one.
- [ ] If a link is chosen, its build tracker is filed, and names this one.

## Ship log

| Date | Event |
|---|---|
| 2026-10-29 | Filed for v0.20.x as a decision, on the Owner's word of 29 October. Records only. |
