---
id: FM-008
status: In Progress
considered: FM-005, FM-007
tags: process
next: build
kind-of-problem: complicated
hook: "The ask/answer flow holds only while every agent has read AGENTS.md and chooses to obey it. Nothing in the tool refuses an ask with no recommendation, a paragraph with three questions in it, the same question filed twice, or an ask sent to the Owner by a seat that has no business sending one. The Owner, on the shadow week's first day: *without enforcing this kind of rules my gut feeling tells me that this process will break as soon as we let other CLI agents into the system.*"
---

# FM-008 — An ask reaches the Owner only through the gate

## What is true now

**The rules exist; only the prose holds them.** FM-005 built the queue and FM-007 built the answer — the dialog, the
options, the one command. Both assume the ask itself is well formed: one question, with a recommendation, asked once,
by a seat entitled to ask. Every one of those assumptions lives in `AGENTS.md` and in the habit of the agent that read
it. A second CLI agent, pointed at this repository with its own doctrine, keeps none of them.

**What is built here** is the same function in three layers — `lint`, which the pre-commit hook, `--check` and every
board build already run:

1. no ask without a recommendation (`ask:` `ask-kind:` `ask-since:` `ask-proposal:` with `next: owner`);
2. one question — one `?`, at the end, 300 characters; at most 5 options, 120 characters each, no duplicates;
3. no duplicate question — an exact normalised match against another open ask, naming the other id;
4. draft → review → owner: an `ask:` with `next: review` is a draft any seat may write and the Owner never sees;
5. seats, optional, config-driven — `[seats]` and `[rights]` in `shoalmark.toml`: four rights (`answer` · `ask` ·
   `close` · `triage`), four built-in names, the identity read from git or from Subversion's server, signed where the
   entry says `signed`;
6. clearing an ask keeps the record — the exchange moves into the body under `## Asks`, or the commit is refused;
7. the bottleneck line — past 5 asks, the board and `--owner` say so in the first line.

And the third layer: `owner_queue` lists only what passes, so a malformed ask that got in anyway is shown as *sent
back*, with its reason, and never as a question.

**Shipped in 0.17.0.** Nineteen mutations, every one caught; both suites green on 3.13 and 3.9; `--check` 0.36 s
against 0.37 s before. Rule 5 was redesigned by the Owner mid-build, from a flat list of who may ask into the four
rights — the tracker's `evidence/FM-008/gate.md` records the redesign, what follows from its shape and what is not
measured. **Open:** no repository runs `[seats]` yet, this one included; the badge and the container a signed seat's
key belongs in are FM-007's ruling to make first.

## Why

The seat that asks is the seat that wants an answer, so no seat polices its own asks. A rule the gate does not hold is
a rule the next agent does not have. FM-007's own ask is the first one rewritten to pass.

## Done when

Every rule above is in `lint` (and, for the queue, in `owner_queue`), each with a check in the suite that is shown to
fail once by mutation, recorded in `evidence/FM-008/gate.md`; `--check` on this repository is no slower than the
7.5 s the hook cost the repository it was cut from; and FM-007's ask passes the gate unchanged.

## Ship log

| Date | Event |
|---|---|
| 2026-09-22 | Filed from the Owner's word on the shadow week's first day; pre-registered in `evidence/FM-008/gate.md` before any code. |
| 2026-09-22 | Built and shipped as 0.17.0: the seven rules, `[seats]`/`[rights]`, `--clear-ask`, the bottleneck line, two `--answer` refusals. FM-005's and FM-007's asks rewritten to pass. |
