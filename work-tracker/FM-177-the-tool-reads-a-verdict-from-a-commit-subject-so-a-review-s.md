---
id: FM-177
status: Proposed
considered: FM-087, FM-175, FM-176
tags: process
hook: "The tool takes a verdict from a commit's subject: its verdict word, beside a Reviewed: trailer. A review's file says the same in prose the tool does not read. On the Owner's word of 18 November, with v0.21.0 the tool reads the verdict from the review file's own data header: the verdict word, the commit it read and the finding ids, in a small header with a schema; the narrative below stays prose."
---

# FM-177 — the tool reads a verdict from a commit subject, so a review's own data header decides nothing

Seat: the Planner (a1730572) · filed 2026-11-18, on the coordinator's word of that day.

## What is true now

**Filed 2026-11-18, Proposed; nothing is built.** The Owner's word of 18 November:
- an evidence file's part a tool decides on (a verdict, the commit it read, its finding ids) is a small header with a
  schema, and the narrative below it stays prose;
- with v0.21.0, the tool reads the verdict from that header.

- **Today:** the verdict is read from a commit's subject and its `Reviewed:` trailer
  ([FM-176](FM-176-a-review-file-can-land-under-a-subject-the-tool-reads-no.md) checks the subject's word until then).
  The review file's own statement of its verdict is prose, and nothing decides from it.
- **With the tracker format** ([FM-175](FM-175-trackers-are-prose-the-gate-cannot-read-so-each-becomes-a.md)): a
  verdict check names its evidence, and decides from that evidence's header.

## Why

One record should decide. A subject line and a file can say two things; a header with a schema says one, in the file
the review writes, and travels with it.

## Decisions

1. **The header:** the verdict word, the commit it read, the tier and the finding ids, in the schema the tracker
   format ships, at the top of a review file; the prose below it is unchanged.
2. **The reader:** the gate, the queue and the tracker's verdict checks read the verdict from the header. A commit
   subject no longer decides; FM-176's hook stays until every reader has moved.
3. **The release:** v0.21.0, with the tracker format.

## Done when

Each item names its commit or pull request when it lands.

- [ ] **The header's schema** ships with the tracker format's, with its test.
- [ ] **Every reader of a verdict** reads it from the header, each with its test and mutant.
- [ ] **The review, at the tier the triage pass sets, is READY.**

## Ship log

| Date | Event |
|---|---|
| 2026-11-18 | Filed, Proposed: with v0.21.0 the tool is to read a verdict from the review file's data header, not a commit subject. Records only. |
