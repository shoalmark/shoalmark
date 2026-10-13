---
id: FM-023
status: Parked
considered: FM-004, FM-005, FM-006
tags: research
kind-of-problem: complex
next: wait
triaged: 2026-09-24
tier: P3
hook: "A plan names its seats, their estimates and when the person is needed; it is updated as the work runs and recorded when done — so a person can plan what to take in, and when to be available"
---

# FM-023 — a plan names its seats, their estimates and when the person is needed, updated as it runs, recorded when done

Seat: Principal · filed 2026-09-23 on the Owner's requirement. Tagged `research`: written to be attacked before anything
is designed or built.

## What is true now

**2026-10-13 — critical common READY; dependent implementation dispatched.** Owner #167 filing, #168 PartB/FM043
and #170 planning records are merged, current main `cab89ed`. R14 and v0.19.4 are shipped. R12's new control follow-up
is locally READY at `246ccdf1995fa416e8757682dcef3784d231c044`, retaining the completed separate critical re-check
and exact unchanged workflow. RV-3040: recorded privately. Native Windows/full CI await Owner fetch/push/rerun.
Archive critical READY `1ba6fc4` closed RV3070 in round2; #170 records integration `f117209` retains every product blob,
passes its clean gate and has an exact-commit deterministic dry run. Its scoped records verification is running.

Common independent critical READY `ef77527` accepts `b72b9ae`, closing RV3085–RV3088 in round2, COMMON SKELETON ONLY.
Ordinary main merge `1fc12b0` retains that exact product tree, passes its clean gate and26history-aware ratchet controls.
A/B/C start the scoped implementation below after this dispatch commit; P alone integrates shared functions and suites.
The [ownership/API record](evidence/stage-dependent-ownership-2026-10-13.md) and [Builder brief](evidence/stage-1-builder-brief-2026-10-13.md)
are the canonical tasking. No full Stage1, new consumer authority, plain-folder expansion or platform proof is accepted.

The Owner's dispatch in the coordinating session, quoted as dispatch rather than a new signed policy answer:
"Push URL stays DISABLED. Tell me when a branch is ready; I fetch from your clone and push."
"R12's brief keeps SHOALMARK_CMD on the gate step (068c9e6) and adds a timeout to the Subversion install step."
"R12 is critical: its Reviewer gets a session of its own."
"Codex covers critical builds today, as ruled on 12 Oct; Claude takes over from tomorrow."
Review IDs allocated to this dispatch: RV-3040–RV-3099; RV-3035–RV-3039 remain with the Auditor.
Reservations: R12 3040–3054; records 3055–3069; archive 3070–3084; stage3085–3099 (3085–3088 now CLOSED in their final common verification round).

| Rank / step | Work and seat | Estimate | What can stop it / next movable work |
|---|---|---|---|
| 1 | R12 locally READY; Owner fetch/push and native CI | Owner/CI execution time | Native Windows/full CI failures; archive and stage seats continue. |
| 2 | Archive accepted product plus current-main records; records Reviewer then P serial common/archive integration | records20–30 min; integration90–120 Builder min plus45–60 critical review | Actual integration/control findings or CI/release qualification; A/B/C move in owned functions. |
| 3a | A Critical Builder: server-free local SVN tracked-board inventory/tripwire, then honest init/install and dependent controls | first60–90 min; full2.25–3.75 Builder h plus review/waits | Unreadable local metadata, shared function transfer or P/B seams hold affected controls. |
| 3b | B Critical Builder: explicit missing-consumer-proof refusal/result first, then bounded history/rights/guard | first60–90 min; full4.5–7 Builder h plus1–2 review h | Missing adopted committed consumer baseline refuses protected acceptance; new authority needs a signed decision. Other local work continues. |
| 3c | C Critical Builder: pure ordered CLI capability/refusals, quoting, controls and accurate docs | first30–45 min; full1.5–2.5 Builder h, private tasking separate | Actual A/B/P entry wiring, private fix verification or unavailable native shell proof; owned helper/control work continues. RV-3003/RV-3004: recorded privately. |
| 4 | P serial integration/reconciliation and independent critical exact-head review |0.5–1 Builder h wiring plus archive allowance above;1–2 review h | Concrete integration findings, incomplete public-entry proof or required CI; preserve every parent allowlist reduction. |
| 5 | B1 conflict inventory complete; Claude takes design/site next day | future2–4 Builder h plus review/dependencies | Claude next-day availability and stage/archive qualification; no site code today. |

These are seat hours, excluding Owner waits/CI. The updated common/A/B/C/P allowance is10.25–16.75 Builder seat hours
before archive/integrated review; completed preparation and later critical corrections are stated separately. No full-stage
finish today is promised. Source process starts remain63 transitional sites until actual owned migrations shrink them.
A/B/C each remove only their migrated exact allowlist keys in the same commit; C owns scanner behavior, fixed ceiling and
accepted boundary stay frozen, and P serially retains every parent's removals. No two seats edit the same shared function.

The [guard contract](evidence/svn-guard-contract-2026-10-13.md) preserves existing bare-account author/answer-right/legacy
meanings. No adopted committed consumer policy baseline is supplied; required protected acceptance conservatively refuses.
Source HERE/archive provenance never provides consumer authority. B's first result/refusal adapter changes no rights or
signature meaning. Selected SVN Git-hook CLI entries refuse with exit4; normal SVN `--check` remains its separate proof route.
P places C's pure ordered preflight after final consumer binding/Tortoise normalization and before proof/message/deriver/write
side effects. D3/D4 remain held; native/full CI and actual release qualification remain owed.

RV-3003/RV-3004: recorded privately. Owner supplied original texts/controls from immutable private commit `7356d6e`;
the missing-source stop is removed. Full tasking and proof stay private. The [inventory](evidence/stage-1-inventory-2026-10-13.md)
and [B1 handoff](evidence/b1-conflict-handoff-2026-10-13.md) remain supporting preparation, not runtime acceptance.
All reports use actual harness identities. Earlier stale trailers remain unchanged. Push URL stays DISABLED; Owner fetches,
pushes, opens/merges PRs and eventually tags/releases. This updates the operational dispatch on the parked planning tracker,
not its proposed planning feature. A wait never stops another ranked movable item.

## Why

A person plans a day around windows, not around seats' work. An estimate written before, updated during and closed with
the actual is what makes a plan a prediction the record can check — per seat, per step — and what lets a person decide
what to take in. Without it, the same information is typed into chat twice a day and lost.

## Candidates — to be attacked, none chosen

1. **A `plan:` line in the front matter the tool parses** (pipe-separated steps: step · seat · estimate · actual, the
   `ask-options:` idiom) plus a `## Plan` table in the body for the step texts; *needed* derived from the owner's rows and
   drawn on the board and in `--owner`; a seat's report writes its actual. The examples below. Cost: a parser (~40 lines),
   a board strip (~15), one label pair. Risk: a plan nobody updates becomes a stale promise — the gate's append-only rule
   for estimates makes the staleness visible, not impossible.
2. **Front matter only:** `plan-next: owner 2026-09-23 15:30–16:00 "open + merge, tag"` — one line the board reads; the
   split stays prose. Cheapest; carries one window, not the split.
3. **Ship-log rows by convention** (`estimate:` / `actual:` prefixes a scorer greps). No code; nothing prints *when you
   are needed*.
4. **Drop it:** the estimate stays in chat and the ship log, as today.

## What would decide it

- How often a plan is updated once it exists (candidate 1's risk): updates per plan over one week, with the
  estimate–actual gap per seat and step. Plans written once and never updated → candidate 2 or 3.
- Whether a person acts on *needed at ≈ hh:mm*: was the window used, or did the person wait in chat anyway.
- The estimate's error per seat over ten arcs — the number that turns *what to take in* into arithmetic.

## Examples — how candidate 1 would look, on the Owner's ask (illustrative, nothing is built)

**The Owner's requirement for the examples:** the plan is drawn on the board, so it must live in the front matter, where
the tool parses it. The shape below keeps the tool's own idiom — one key, pipe-separated items, a fixed field order inside
each item (as `ask-options:` does) — so today's line parser reads it without a YAML library:

```
plan: "<step> · <seat[+seat][@session]> · <estimate> · <actual> | <step> · … "
```

- `<step>` — a number for seat work, `W<n>` for a window of the person; the body's `## Plan` table carries each step's
  text and notes under the same key.
- `<seat>` — a seat name from `[seats]`; several joined with `+`; `@<session>` is the session id of FM-024 (the registry's
  row, the commit trailer's value) — required on every seat step once FM-024 has landed, and the gate checks it against
  an open row. A sub-agent's hand is in the registry (`a9/reviewer-1`); the plan carries the session root (`@a9`).
- `<estimate>` — a clock time `≈15:30`, a range `15:30–16:00`, or a duration `~15m`; a re-estimate is **appended**, never
  overwritten: `≈15:30→15:40@14:38`. `<actual>` — a clock time or range once done, `—` until then.
- `plan-by:` who estimated and when · `plan-updated:` the newest update · `plan-closed:` when every actual is in.
- **Nothing else is written for the board:** *needed* is **derived** — the owner's `W` rows in clock order, the next one
  first — and printed on the board and in `--owner` as *needed: owner 15:40–16:00 — tag*.

### a. The estimate, as filed before the work (12:55)

```markdown
---
id: FM-0xx
status: In Progress
next: build
plan-by: principal@a9 2026-09-23 12:55
plan: "1 · research@a9 · ≈13:05 · — | 2 · principal@a9 · ≈13:30 · — | 3 · implementer@a9 · ≈14:30 · — | 4 · reviewer+implementer@a9 · ≈15:30 · — | W1 · owner · 15:30–16:00 · — | 5 · implementer+reviewer@a9 · ≈16:30 · — | W2 · owner · 16:30–17:00 · —"
---

## Plan

*Moves it: a P1 from the Reviewer (+1 h) · the search fix being template surgery rather than a filter (+1 h) · the
triage pass finding more than the two issues worth fixing today (the rest is filed, not built).*

| # | Step | Note |
|---|---|---|
| 1 | Research: the triage state, the two board issues | |
| 2 | Filings for the two issues; the first triage pass | |
| 3 | Build the release on a branch | |
| 4 | Review, one fix round, verification of the final tree | |
| W1 | **Open + merge the release PR, tag** | |
| 5 | Vendor the tag into the consumer as its own pin PR; review | |
| W2 | **Open + merge the pin PR** | before 07:30 |
```

*What the board draws from it:* one lane per seat, each step a bar from its estimate; the owner's rows as a strip at the
top — **needed: owner 15:30–16:00 — tag · 16:30–17:00 — the pin PR**; the digest prints the next window only.

### b. An update while it runs (14:38) — the two lines that change

```diff
-plan: "1 · research@a9 · ≈13:05 · — | 2 · principal@a9 · ≈13:30 · — | 3 · implementer@a9 · ≈14:30 · — | 4 · reviewer+implementer@a9 · ≈15:30 · — | W1 · owner · 15:30–16:00 · — | 5 · implementer+reviewer@a9 · ≈16:30 · — | W2 · owner · 16:30–17:00 · —"
+plan: "1 · research@a9 · ≈13:05 · 13:00 | 2 · principal@a9 · ≈13:30 · 13:33 | 3 · implementer@a9 · ≈14:30 · 13:44 | 4 · reviewer+implementer@a9 · ≈15:30→15:40@14:38 · — | W1 · owner · 15:30–16:00→15:40–16:00@14:38 · — | 5 · implementer+reviewer@a9 · ≈16:30→16:40@14:38 · — | W2 · owner · 16:30–17:00→16:40–17:10@14:38 · —"
+plan-updated: principal@a9 2026-09-23 14:38
```

The body table gains its notes in the same commit (*step 2: the pass deferred — waits for the release, the Owner's
word 14:40 · step 3: one more tracker taken in mid-flight · step 4: a second round the estimate did not have*).
*Who writes it:* the seat whose step finished writes its actual in its own report commit — and the gate checks that the
commit's `Session:` trailer matches the step's `@session` (a session writes only its own steps); only the seat and session
named in `plan-by:` re-estimate; a window moves only by a re-estimate. The board shows the newest window and, beside it, how
many times it moved (`→` count).

### c. The record of a finished tracker (closed the same evening)

```markdown
---
id: FM-0xx
status: Shipped
plan-by: principal@a9 2026-09-23 12:55
plan-updated: principal@a9 2026-09-23 15:12
plan-closed: principal@a9 2026-09-23 17:05
plan: "1 · research@a9 · ≈13:05 · 13:00 | 2 · principal@a9 · ≈13:30 · 13:33 | 3 · implementer@a9 · ≈14:30 · 13:44 | 4 · reviewer+implementer@a9 · ≈15:30→15:40@14:38 · 15:52 | W1 · owner · 15:30–16:00→15:40–16:00@14:38 · 15:58–16:04 | 5 · implementer+reviewer@a9 · ≈16:30→16:40@14:38 · 16:41 | W2 · owner · 16:30–17:00→16:40–17:10@14:38 · 16:58–17:04"
---
```

*With FM-024 the closed plan also says, per step, which session's hands did it — and the registry says who convened that
session and for what. What the tool derives from a closed plan, per seat:* the estimate error (research −5 min · implementer −46, +11 ·
reviewer+implementer +22 on the re-estimate · owner 6 min at the keyboard per window against 30 estimated); the count of
re-estimates (1); the largest miss (step 4). Ten closed plans and the board can print a margin the record earned beside
every new *needed* line — that is the feedback the Owner asked for.

### d. An extract for a multi-session tracker — two sessions of one seat, one Owner (FM-024's ids)

```markdown
---
id: FM-0xx
status: In Progress
plan-by: principal@a9 2026-09-23 12:55
plan: "1 · implementer+reviewer@a9 · ≈15:40 · 15:52 | W1 · owner · 15:40–16:00 · — | 3 · implementer+reviewer@d8 · ≈16:00 · 12:22 | 4 · principal@d8 · ≈12:30 · 12:12 | W3 · owner · ~15m · — | 2 · implementer+reviewer@a9 · ≈16:40 · — | W2 · owner · 16:40–17:10 · —"
---

## Plan

*Two Principal sessions run today by the Owner's design — `a9` on the day's findings and the tool, `d8` on the product
items; both are open rows in `sessions.md` with their scope and who convened them. A session writes only the steps that
carry its `@` mark (the gate matches the commit's `Session:` trailer); the owner's `W` rows are anyone's to read and one
session's to move — the one named in `plan-by:`. A window without a clock (`~15m`) is the Owner's own slot.*

| # | Step | Note |
|---|---|---|
| 1 | Build, review, tag the release | a9 |
| W1 | **Tag the release** | a9 reports |
| 3 | The negative-control build, its review, the pre-registration | d8; early, waits on 4 |
| 4 | The run sheet for the Owner's hands — four reads, one command each | d8 |
| W3 | **The hands sitting — its own slot, outside the standup budget** | d8 reports; not a standup item |
| 2 | Vendor the tag into the consumer; review | a9 |
| W2 | **Open + merge the pin PR** | a9 reports; before 07:30 |
```

*What the board draws:* **needed: owner 15:40–16:00 — tag (a9) · your own slot ~15 min — the hands sitting (d8) ·
16:40–17:10 — the pin PR (a9)** — every session's windows in one strip, in clock order, slots without a clock last; a
click on `a9` opens the registry's row (convened by, scope, worktree). *The rule the extract carries:* a session never
edits another session's step — with FM-024 the gate refuses it; two sessions writing one step is a finding, not an update.

### What the parser needs (for the Reviewer to attack)

One key, one regex per field, no YAML: split on `|`, then on `·`; step `^(W?[A-Z]?\d+)$`; seats `^[a-z]+(\+[a-z]+)*@[a-z0-9]{2,8}$`
against `[seats]` and the session against FM-024's open rows; estimate `^(≈\d\d:\d\d|\d\d:\d\d–\d\d:\d\d|~\d+[mh])(→…@\d\d:\d\d)*$`; actual `^(—|\d\d:\d\d(–\d\d:\d\d)?)$`.
The gate refuses a `plan:` whose seat is not in `[seats]`, whose `W` row's seat is not the owner, or whose estimate was
edited rather than appended (the previous commit's value must be a prefix of the new one). About 40 lines and one label
pair; the board's strip about 15 lines of the template. Unproven: whether a person reads a 200-character line — the body
table is the readable copy, and the gate can check the two agree on the step keys.

## Done when

The Owner has ruled which candidate, if any; the chosen one prints *who is needed, when, for what* on the board and in
the digest, from a plan written before the work, updated by each seat's report and closed with the actual; and one full
arc has run on it with its estimate–actual gap in the record.

## Asks

**2026-10-12** · Do you accept the release allocation below: R14 first and in v0.20.0, then R12, the bounded stage-1/archive release, and the named follow-up releases?
**answered** — accepted - with a change: B1, the landing, ships with v0.20.1, so that the probe starts from the published site; v0.20.1 carries B1, the probe's final prompt and what its first outside run needs; rows that put its date at risk move to v0.20.2 · holgo99
**relation** — accepted with a change
**signed** — adaec88 · G

## Ship log

| Date | Event |
|---|---|
| 2026-10-13 17:42 CEST | **Dependent dispatch from critical common READY:** `ef77527` closes the four common findings; current-main merge `1fc12b0` retains its exact product and passes gate/ratchet. A first local board slice60–90 min (2.25–3.75 h total), B first missing-proof refusal60–90 min (4.5–7 h total), C first capability/control slice30–45 min (1.5–2.5 h plus private tasking). P owns serial shared/archive integration. RV-3003/RV-3004: recorded privately. |
| 2026-10-13 | Stage-1 and B1 read-only preparation recorded with immutable-ref evidence; stage-1 build re-estimated from 4–8 h to 6–10.5 Builder hours before archive/review, and its guard capability contract remains a brief dependency. B1 has three conflicted paths/eight groups and a 2–4 h next-day integration estimate. R15 configuration switch verified on current main; no feature build, platform proof or publication claimed. |
| 2026-09-23 | **Updated as if FM-024 had landed, on the Owner's word:** every seat step carries its session id (`@a9`, `@d8`), `plan-by:` and the updates name seat and session, the gate matches a step's session to the commit's `Session:` trailer, and the multi-session extract uses the registry's ids and rows. |
| 2026-09-23 | **Four worked examples added on the Owner's ask, then reworked on his second word — *it must be visual on the board, so it must be in the front matter to be parseable*:** the plan is one `plan:` line (pipe-separated steps, fixed field order, re-estimates appended), *needed* is derived from the owner's rows, the body table holds only step texts; the estimate as filed, an update, the finished record with per-seat error, a multi-session extract, and what the parser needs. Illustrative; nothing built. |
| 2026-09-23 | Filed on the Owner's requirement, tagged `research`, with the instance that raised it as its first evidence. Held against FM-004 (adoption), FM-005 (the person asked mid-flight), FM-006 (a page for the humans). Not built this week — the current path's line 2: tracked, not built. |
| 2026-10-13 | Owner #168 merged combined Part B/FM-043 records at ab7ed3f. R12 independent critical verdict is locally READY at 8b7f7f1; RV-3040: recorded privately. Archive RV-3070 current-main integration is being reconciled. Guard analysis records conservative proof refusal and revises seat-time estimates; no new authority or stage completion claimed. |
| 2026-10-13 | Prepared exclusive dependent function/control ownership while common critical review runs at 6d0c239. Corrected ratchet participation so each migrated branch passes required controls; no ceiling expansion, authority rule or code built by this record. Original RV-3003/RV-3004 source requested; other scoped work stays movable. |
| 2026-10-13 | Common critical round 1 and addendum are NOT READY with RV-3085–RV-3088 open; fixforward and one remaining verification round precede dependent code. RV-3003/RV-3004: recorded privately. Owner supplied the original private inputs; the missing-source stop is removed. |
