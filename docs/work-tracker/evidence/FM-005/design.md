# FM-005 — sign once, then the road is clear: the exploration, start to finish

Written 2026-09-21, before any code. The Owner's direction: *"How to get a better performing human owner"* —
**less work and distraction for humans, more throughput and less friction for agents**; *"the worst a human can be
dragged to is push buttons in accord … better we build agent workflows that the user signs off on once and the road is
unblocked for a set of agents to perform the tasks start-to-finish."* And: *deliver this without rubber-stamping, and
without failing like the incident.*

## 1. What is measured, not assumed

| Observation | Number | Source |
|---|---|---|
| The origin's last 200 merged pull requests, 22 days | **85 % merged under one minute after opening · median 0 min · 0 of 200 with a review or a comment · 93,516 lines · 51 on the busiest day** | the forge, read 2026-09-21 |
| Three blind agents on a fair stand-in, asked what brakes them | **3 of 3: the Owner's unanswered questions, by a wide margin** — one question open three days held three packages and caused three half-finished ones | FM-004, second round |
| The same agents, asked what a tool lacks | 3 of 3, unprompted: **nothing pushes, nothing enforces** — *"eine Datei ruft Sie nicht an, und eine Tafel müssen Sie auch erst öffnen"*; the gate checks a tracker's form, not the test it names | FM-004 |
| The origin's incident | rehearsal runs materialised real credentials and a restored production database as files agents could read; **nothing ever ended a run**; the first inventory was never written anywhere durable; no sign-off caught any of it | the origin's incident ledger |

Two failures, one root. **Blocking** (the stand-in) and **stamping** (the origin) both come from asking a human for
many small, low-context decisions in the middle of the work. A gate a person cannot operate is worse than no gate: it
costs his attention, adds latency, and launders responsibility.

## 2. The principle

**The human is on the loop, not in it.** His decisions move to the *start* and *up* a level. He is asked for exactly
three things: **sign a mandate** · **rule on a real exception** · **read a sample, from a budget he sets.**
Everything else runs start to finish without him — and is *provably* inside what he signed.

## 3. The parts

**3.1 The mandate — one page per story, never per task.**
`for · so that · never` (the Owner's own words — the tool leaves these three lines empty; an agent drafts everything
else) · **scope**: paths and trackers it covers · **may touch**: the capabilities it grants — and by default it grants
*no* secret, *no* production data, *no* outward-facing action, *no* history rewrite · **done proves**: the named checks
that must be green · **ends with**: what a finished run leaves behind — nothing, shown by an inventory before and after ·
**budget**: days, packages in progress at once · **values**: what matters when a question is close (*"the accountant
must be able to read it without asking"*) — so similar questions need no asking · **escalates**: the list that always
comes back · **expires**: a date or a budget, never open-ended. Its text is hashed at signing; an edit needs a new
signature; the gate refuses work outside a live mandate.

**3.2 A question cannot block forever.** An ask carries: the question · **the agents' proposed default** · a deadline ·
a reversibility class. *Reversible* and the deadline passes → the agents proceed with the default, record it, and it
stays revertible until a stated date. *Irreversible* → it stays blocked, and it is the only kind that reaches the human.
The Owner sets the **floor** of each class's deadline — an agent cannot slip a decision through with a short one. A
provisional answer (*"vorläufig X"*) is an answer.

**3.3 Done is evidence, and every run ends.** A package closes only when the checks its mandate names are green — run by
the tool through the deriver seam, not asserted in prose — and a *different* seat has reviewed it. **Teardown is part of
done:** the run's inventory (files, containers, volumes, processes it created) is written into the repository before
and after, and the difference must be empty or named. This is the incident's lesson turned into a check.

**3.4 The digest — it arrives; a board has to be opened.** Ten lines at the Owner's cadence, as the *last message of a
session* (no infrastructure): what needs you (irreversible only, oldest first, what each blocks) · what was decided by
default and until when you can revert it · what shipped, with its evidence · the budget · anything off course.

**3.5 Audit by sampling.** The Owner sets an attention budget — say thirty minutes a week. The tool spends it: the
riskiest change (by what it touched) and one at random. He reads those; the rest merged under the mandate.

**3.6 A ratchet and a stop word.** A first mandate is narrow. It may widen when few defaults were reverted and few
defects escaped — the renewal shows that record. One word revokes a mandate; everything under it pauses.

## 4. Against rubber-stamping — the question the Owner asked

Stamping moves up a level unless the design prevents it. Seven mechanisms, cheapest first:

1. **Fewer, earlier, bigger.** One page per story replaces dozens of mid-flight clicks. There is time to read one page.
2. **Friction where reading matters.** The three intent lines are the Owner's to *write*, not to click. A mandate whose
   `never` is empty is unsigned.
3. **He reads the risks, not the plan.** Before signing, an independent adversary seat attaches a pre-mortem of at most
   five lines: *how does this mandate reproduce the incident?* That is what is put in front of him.
4. **Blast radius decides whether a human is needed at all.** Reversible, no secrets, no outward action: a light
   signature. The dangerous classes cannot be mandated in bulk — each is its own exception, with two keys (the Owner
   and an independent seat).
5. **Nothing is eternal.** Mandates expire. Renewal is a decision from a record, not a habit.
6. **Honest numbers, for him only.** The tool shows how long each signature took against the page's length — the same
   measurement that showed 85 % under a minute. No trap, no planted defect: a mirror.
7. **The default is no.** No live mandate, no autonomous work. Silence never widens anything.

## 4b. Trust — the Owner's requirement: *"we need trust in the process, otherwise we will not sign off on any of this"*

Trust is not asked for; it is earned from the Owner's own data, before anything runs unattended.

1. **Shadow first.** For the first week a mandate decides nothing. The agents record the default they *would* have
   taken on every ask; the Owner answers as he always has. At the end he sees his answers beside theirs. **The
   agreement rate is the trust number — his, about his own work** — and it decides which classes of ask he delegates.
2. **Start where nothing can go badly wrong.** The first live mandate is reversible work only. Trust widens by class,
   on the record, never by default.
3. **Drills on day one.** *Stop* is pulled once, on purpose, and everything is seen to pause. One default is *reverted*
   once, on purpose, and is seen to come back clean. A control that was never exercised is not a control.
4. **Every autonomous act names the line that allowed it.** *"AP-023 · took the default · allowed by: mandate §values,
   line 2."* Nothing happens that cannot be traced to something he wrote or signed.
5. **Refusals are shown.** What the gate refused — an agent reaching for a file outside scope, a check that was red —
   is on the Owner's page. A process that shows its own near-misses is one he can believe when it is quiet.
6. **It reports its own failures first.** A reverted default, an escaped defect, a missed deadline lead the digest;
   they are never found by him.
7. **The reviewing seat is really independent** — another session, where possible another model family, never the
   author grading itself.

## 4c. What the agents need — named by one of them

The Owner: *"you can name the agent requirements yourself."* These are mine, from the session that wrote this file —
each with the moment that taught it.

1. **A boundary I can point to, so I need not ask *may I?* mid-flight.** A clear *no* makes me faster, not slower: in
   this session the standing rule *push and stop* cost no time because it was unambiguous; every unclear edge cost a
   question.
2. **An answer — or a default I am allowed to take — by a time.** Never an open-ended wait. Waiting is the only state
   in which I produce nothing and cannot say when that ends.
3. **State that outlives me.** I start cold; this session itself was compacted half-way and continued from a summary.
   *What is true now* and the next move, in the tracker, are the only memory I can rely on.
4. **One source of truth, and rules that do not contradict.** In the rehearsal a rulebook sent an agent to package 24
   while three lay half-finished. A contradiction is a decision each session makes differently.
5. **A done I can check before I claim it.** I would rather be refused by a gate than be wrong in front of the Owner.
   A gate stopped me twice today — a secret-shaped file, and a commit over a syntax error — and both times it was right.
6. **An independent second seat, with the power to block.** I cannot grade my own work: the reviewer of the port found
   a P1 that I had introduced and proven green.
7. **Not to hold what I should not hold.** Do not hand me a secret I do not need; the incident found forty-three
   tokens in agent transcripts. A capability I lack is a mistake I cannot make.
8. **A run that is expected to end,** with the teardown in the budget — so that leaving nothing behind is part of the
   work and not a courtesy.
9. **The Owner's values, written down.** When a default of mine is reverted, the *why* belongs in the mandate: I will
   not remember it, the next session must. That section is my memory of his judgement.
10. **Errors that are cheap to admit.** I reported my own several times today. That stays stable only where a reported
    error costs less than a hidden one.
11. **A budget I can see** — time, tokens, packages in progress — so that stopping is a decision and not an accident.

None of these asks for more of the human. Each asks for something *once, earlier, and in writing*.

## 5. The human's page — designed to the Owner's own Zero-Noise rules

*Epicentre:* **"The Owner comes here to unblock, and to stop."** Everything else is demoted.

- **Top, one line, answer first:** `2 need you · oldest 3 days · blocking 3 packages` — or `nothing needs you`.
- **Then one verdict strip per mandate:** on course · off course · stopped — with budget used and the expiry.
- **Then what ran without him:** decided by default (revertible until…), shipped with evidence.
- The table of all work is *below the fold*, collapsed — it is the agents' page, not his.
- **At most two accent colours in the viewport;** coral means *needs you and is risky* and nothing else. A tag such
  as `#security` earns its place because it changes what he does — the MSR-005 row is the proof that one small,
  semantic mark gets a human to act. Marks are scarce on purpose.
- **Five-second test:** strip colour and icons — what needs him must still be obvious.
- **Phone:** the count, the oldest, one action. Nothing else.

## 6. What the incident demands of this design

| What went wrong | The rule here |
|---|---|
| real credentials in files an agent could read | a mandate grants capabilities explicitly; secrets and production data are never grantable in bulk |
| nothing ever ended a run | teardown is part of done; an inventory before and after, committed |
| the inventory was never written anywhere durable | evidence lives in the repository, or it does not count |
| an unversioned estate became the handoff channel | the tracker is the only handoff; scope names paths, and work outside them is refused |
| sign-offs caught nothing | the human is not the detector: checks and an independent seat are; he rules on exceptions and samples |

## 7. How it is delivered — cheapest proof first

| Phase | What | Proves | Costs |
|---|---|---|---|
| **P0a — shadow** | one week: the agents record the default they would have taken on every ask; the Owner answers as always; nothing is decided for him | the agreement rate, per class of ask — and whether he would sign at all | a week; no code |
| **P0 — paper** | one real mandate for one real, narrow arc in the origin (docs and tracker work only), written by hand, run with the tools that exist; asks with defaults and the digest done by contract, no code | whether one page can actually carry an arc start to finish, and what the Owner's week looks like | a day; no code |
| **P1 — the gate** | `mandates/` beside the trackers; the gate refuses work outside a live one; hash and expiry; `--ask`, `--digest` | the mechanics, in the suites, on three systems | the tool |
| **P2 — evidence and teardown** | `done proves` run through the deriver; the before/after inventory | the incident's lesson as a check, mutation-witnessed | a deriver |
| **P3 — the Owner's page** | the epicentre redesign of the board | the five-second test, looked at, on a phone width too | the page |
| **P4 — the trial** | two weeks in the origin against the 200-pull-request baseline | the claims below | the Owner's two weeks |

## 8. Pre-registered claims

| # | Claim | Kills it if |
|---|---|---|
| M1 | The Owner's minutes per shipped package fall by more than half against the baseline, with his reading *real* (sampled items read for longer than their length implies a skim) | they do not fall, or fall only because reading stopped |
| M2 | No question to the Owner blocks work longer than its class's floor; the median age of open asks stays under one working day | an irreversible ask sits unseen for a week — then nothing pushed |
| M3 | Fewer than one in ten default decisions is later reverted | more — then the agents' defaults are not good enough to delegate to |
| M4 | No escaped defect of the incident's classes (a secret in a readable file, a run that did not end, work outside scope) | one does — then the capability bounds are decoration |
| M5 | The Owner can say what each live mandate allows, unprompted, a week after signing it | he cannot — then it was stamped |
| M6 | Agents' throughput rises: packages shipped per week up, packages in progress at once down | neither moves |
| M8 | **Trust is earned before it is used:** after the shadow week the agents' defaults agree with the Owner's own answers on at least four in five reversible asks, the stop and revert drills both worked, and he says he would sign a first mandate | agreement is low, a drill fails, or he would not sign — then nothing goes live, and that is the right outcome |
| M7 | The whole of it still explains in one README section and one page per mandate | it needs more — then something is cut, not explained |

**Forecast:** M8 0.6 · M1 0.6 · M2 0.7 · M3 0.55 · M4 0.75 · M5 0.5 · M6 0.6 · M7 0.6 · all eight 0.08. M5 is where I expect the
truth to hurt: a signature is easy to give.

## 9. What this does not solve, said now

A person who does not read one page will not be saved by a page. · Agents grading agents is only as good as the
independence of the seats. · Defaults shift real decisions to agents — M3 measures whether that is safe here, and the
answer may be *not yet*. · The origin's standing rule — *push and stop; the Owner opens the pull requests* — is
reversed by this design for mandated work; that is the Owner's ruling to make, per mandate, and until it is made the
rule stands. · Three agents, one model family and one Owner are the whole evidence base.
