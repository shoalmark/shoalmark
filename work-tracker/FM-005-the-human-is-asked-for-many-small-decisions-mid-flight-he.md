---
id: FM-005
status: In Progress
considered: FM-004, FM-001
tags: research
next: build
triaged: 2026-09-25
tier: P1
rank: 5
hook: "Measured: 200 pull requests merged in 22 days, 85 % under a minute after opening, none reviewed — and in a rehearsal three agents named the Owner's unanswered questions as their top brake. Blocking and stamping have one root: a human asked for many small decisions mid-flight. The direction: sign once, then the road is clear."
---

# FM-005 — The human is asked for many small decisions mid-flight — he either blocks the agents or stamps without reading

## What is true now

**2026-09-30 — evidence-checked done, its first slice: a shipped tracker names its commit (v0.19.0).** The Owner's ruling is
filed below, in *A shipped tracker names its commit — v0.19.0*. It is built on `fm/005-a-shipped-tracker-names-its-commit`,
cut from main `1197e80`, by one Builder; one Reviewer judges the pushed tip at code tier; the Owner opens the pull request and
merges at 9/9. Next: build.

**Explored and pre-registered 2026-09-21; nothing is built.** The Owner's direction: *how to get a better-performing
human owner* — less work and distraction for humans, more throughput and less friction for agents; workflows the human
signs off **once**; no rubber-stamping; never again the incident; and his requirement: **trust in the process, or
nothing gets signed.** The exploration, start to finish, is [`evidence/FM-005/design.md`](evidence/FM-005/design.md):
the measurements · the principle (*on the loop, not in it*) · the mandate, asks with defaults and deadlines,
evidence-checked done with teardown, the digest, audit by sampling, the ratchet and the stop word · seven mechanisms
against stamping · trust earned in a **shadow week** from the Owner's own answers, with stop and revert drills ·
the agents' eleven requirements, named by one · the Owner's page designed to his Zero-Noise rules · what the incident
demands · five delivery phases, cheapest first · eight claims with what kills each. A mock of the Owner's page —
looked at, desktop and a true 390 px — is [`owner-page-mock.html`](evidence/FM-005/owner-page-mock.html); looking at
it found two defects before anyone else did: a one-click default on an *irreversible* ask, and a phone view that showed
everything.

**P0a is prepared in the origin (2026-09-21, the Owner's go-ahead):** its `FEAT-190` on branch
`feat/190-the-owners-queue-shadow-week` — the ask ledger of the six real items, classed, and a one-page shadow mandate
whose three intent lines are empty and whose pre-mortem is owed by an independent seat. Reading the real queue changed
the design (§3.7): four kinds of waiting, of which a default helps one and a half of six.

**What "complete and verify" can mean, said plainly:** complete today — the exploration, the mock, the claims, the
first mandate and ledger, each through its gates. **Not completable in a session:** claims M1–M8 need the Owner's
shadow week and then two weeks of trial; they are verified by his calendar, not by my effort. Nothing here is marked
done before that.

**Next is the Owner's:** rule whether phase P0a — the shadow week, in the origin, on one narrow arc, no code — starts;
and whether the origin's rule *the Owner opens the pull requests* may be lifted for a mandate once trust is earned.
Until he rules, that rule stands.

## Done when

The eight claims in the design are each held or killed with their numbers, in the origin, and the Owner has ruled
from that record whether mandates go live.

## A shipped tracker names its commit — v0.19.0

**The Owner's ruling, 2026-09-30 — a must for v0.19.0.** shoalmark claims *a gate that refuses a false done* (README.md:13–14,
overrides/landing.html:361). At `1197e80` that is untrue: a tracker marked `Shipped` whose body says *nothing is built*, with an
empty *Done when* and only *Filed.* in its ship log, commits through the installed hook and passes `--check`, exit 0 —
reproduced by the Planner in a scratch repository on 2026-09-30. Evidence-checked done is this tracker's; the fix is filed here.

- **The rule.** A commit that moves a tracker to `Shipped` is refused unless the tracker's ship log names a commit that is in
  the history and changes at least one path outside the records.
- **Where it is judged.** Only on the commit that changes the status, so nothing shipped before breaks. It applies to every
  author, the Owner included, on git and on Subversion. `Closed` is not a done. The refusal names the way through.
- **Tests, with controls.** Refused with no commit named, with a commit not in the history, and with a commit that touches only
  records; passes with a real one; an untouched old `Shipped` tracker and a `Closed` one pass; the same on Subversion.
- **The claim, in the same pull request.** README.md:13–14 and overrides/landing.html:361 read *a gate that refuses a done
  without a commit behind it*. The README's table of refusals gains the new one with its way through, and the CHANGELOG gains
  it under *Unreleased — 0.19.0*. If Subversion misses the cut, the claim says *on git*.
- **How it is built.** One Builder in its own worktree from main `1197e80`, which pushes and stops; one Reviewer at code tier on
  the pushed tip; no screen round. The Owner opens the pull request and merges at 9/9.
- **From the merge, this repository obeys it:** every tracker moved to `Shipped` at the cut names its commit.

*The Planner's reading, for the Reviewer to judge:* a commit is named by its git hash (seven hex characters or more) or its
Subversion revision (`r123`); *in the history* means an ancestor of the commit being judged; *the records* are the
`[ratio] records` prefixes where that section is set, else the tracker directory; a status is `Shipped` as the tool classifies
it, so a new tracker filed as `Shipped` moves to it.

## Asks

**2026-09-22** · Will you write the three intent lines of the shadow mandate in the origin (its FEAT-190) and sign it, or does the shadow week not start?
**withdrawn** — no answer was given

## Ship log

| Date | Event |
|---|---|
| 2026-09-21 | Filed; the exploration, the mock and the claims written before any code. |
| 2026-09-21 | P0a prepared in the origin (its FEAT-190); the real queue read — four kinds of waiting (§3.7). |
| 2026-09-30 | **A shipped tracker names its commit — filed** by the Planner on the Owner's ruling of that day, a must for v0.19.0: the claim *a gate that refuses a false done* is untrue at `1197e80` (a `Shipped` tracker with nothing built passes the hook and `--check`, reproduced in a scratch repository), so a move to `Shipped` is refused unless the ship log names a commit in the history that changes a path outside the records — every author, git and Subversion, judged on the commit that changes the status. |
