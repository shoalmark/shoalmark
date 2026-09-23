---
id: FM-024
status: Proposed
considered: FM-005, FM-007, FM-008
tags: research
kind-of-problem: complicated
next: review
hook: "Two sessions of one seat are one author in git; a seat's commit must name its session, and the record must know what that session was convened for"
---

# FM-024 — a seat's commit names its session, and the record knows the session

Seat: Principal · filed 2026-09-23 on the Owner's question — *"every seat needs an id or a session id that we can track
and trace back to the record; what if I run a session in parallel with another Principal seat — how do we know which one
it was? Let us reason about how to solve this right from the start."* Written to be attacked.

## What is true now

**Filed 2026-09-23; nothing is built.** A seat commit carries one identity: the author (`principal@seat`), which is what
the gate reads for rights (`[seats]`). It says *who may*; it cannot say *which run*. On 2026-09-23 two Principal sessions
ran by the Owner's design and collided in one worktree; in git their commits are one author. A Reviewer seat run as a
sub-agent of a Principal session commits under `reviewer@seat` and is, in git, as independent as one run by anyone —
the record cannot tell (the consumer's finding on its count of reviewed pull requests).

## The model — two facts, two fields

- **Seat = author.** Unchanged: the gate's rights, the badge per worktree.
- **Session = a trailer on every seat commit**, appended by the hook from the worktree's configuration so no seat can
  forget it: `Session: a9`. Written once at worktree setup (`git config --worktree seat.session <id>`); read with
  `git log --format='%(trailers:key=Session)'`. The Owner's own commits carry none — his signature is his id.
- **The registry, in the record:** `work-tracker/sessions.md`, one row per session — `id · seat · convened by · scope
  (one line) · worktree · started · ended`. A session's first commit adds its row; the gate refuses a seat commit whose
  `Session:` is not an open row; a row is closed by the session's last commit or by the next pass.

## The collision is worse for the seats that build and judge — the Owner's question

A Principal's collision costs a stray commit. An **Implementer's** costs a build: two sessions in one worktree put both
their half-written trees under one branch, and a suite run there proves nothing about either. A **Reviewer's** costs a
false READY: a verdict committed from the author's worktree or session, which the record today cannot tell from an
independent one, and a *verified tip* that keeps moving while the author commits after the last verification. Hence
the second rule the gate would hold, beside the registry: **a verdict commit's session must differ from every session
that authored the reviewed range**, and the review file names the tip it judged; a verdict on a tip that is not the
branch's head is not a verdict on the branch.

## What it gives

1. **Tracing:** any commit → its session → who convened it, for what, in which worktree.
2. **The collision is visible:** two open rows naming one worktree.
3. **Independence becomes a measurement, today:** a review is independent when its `Session:` differs from the author's.
   A Reviewer sub-agent of the Principal's session carries the Principal's id — and is counted as *not independent*.
   The seat's own key (a container per seat, the Owner's 09-22 direction) is the stronger proof and comes later, as a
   second field, not instead of this one.
4. FM-023's `@session` mark is this id; the Owner's intent line *the current state of where seats are authorised to be
   working* is the registry's open rows.

## Open — the Owner's reasoning goes here

- **The id's source per harness.** Each agent harness has a session id of its own; the worktree configuration takes any
  string. Proposal: the harness's id, first eight characters, else a generated one; uniqueness is checked against the
  registry, nothing else.
- **Sub-agents:** carry the parent's id alone (`a9`), or parent and agent (`a9/reviewer-1`)? The first keeps the
  independence measure simple; the second traces the hand.
- **A row nobody closes:** a session that ends without a last commit. Proposal: the next triage pass closes open rows
  older than a day and says so.
- **The Owner's sessions** (he starts seats from his checkout): the worktree rule already moves them out; their row's
  *convened by* is him.

## Candidates — to be attacked

1. **The trailer + registry above** (~60 lines: a `commit-msg` hook line, a registry parser, one gate check; the board's
   open-sessions strip ~10 lines) **plus the independence rule** for verdict commits (~15 lines: the reviewed range's
   sessions against the verdict's).
2. **The session in the author name** (`Principal seat (a9)`): no hook, but the gate's `[seats]` maps one identity per
   seat and the Owner ruled out wildcards; the registry would still be needed.
3. **The session in the e-mail** (`principal+a9@seat`): the same objection, plus a `[seats]` entry per session.
4. **Drop it:** the worktree is the badge; the collision rule (*one worktree per session*) stands as doctrine only.

## What would decide it

- Over one week: how many seat commits could not be traced to a convening word without the registry (today: all).
- Whether the independence count changes a verdict on 09-29 — if every review is a sub-agent of the author's session,
  the count says so and the container question moves up.

## Done when

The Owner has ruled the candidate; a seat commit without a registered open session is refused by the gate; the board
shows the open sessions with their scope; FM-023's plan marks steps by this id; and one week's commits trace, each, to a
row.

## Ship log

| Date | Event |
|---|---|
| 2026-09-23 | Filed on the Owner's question, written to be attacked; held against FM-005 (the person asked mid-flight), FM-007 (a signature proves the key, not the hand), FM-008 (an ask reaches the Owner only through the gate); FM-023 (the plan's `@session`, on its own branch) is the consumer of this id. Not built this week — the path's line 2. |
