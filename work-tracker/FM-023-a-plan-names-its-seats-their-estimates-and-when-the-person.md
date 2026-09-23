---
id: FM-023
status: Proposed
considered: FM-004, FM-005, FM-006
tags: research
kind-of-problem: complex
next: review
hook: "A plan names its seats, their estimates and when the person is needed; it is updated as the work runs and recorded when done — so a person can plan what to take in, and when to be available"
---

# FM-023 — a plan names its seats, their estimates and when the person is needed, updated as it runs, recorded when done

Seat: Principal · filed 2026-09-23 on the Owner's requirement. Tagged `research`: written to be attacked before anything
is designed or built.

## What is true now

**Filed 2026-09-23; nothing is built.** A tracker today holds what and why, a `next:`, an ask and its answer, a ship log.
It holds no plan: which seat does which step, how long each is expected to take, and when the person in charge is
needed — before the work, updated while it runs, recorded when done. The board can say *what waits on you*; it cannot
say *when you will be needed, for what, for how long*.

**The Owner's requirement, 2026-09-23** *(spelling normalised at his request; the meaning unchanged)*: *"When this is
tracked and updated, we can communicate to a person in charge, or even a seat, when they are expected to be involved or
available. Better planning becomes possible only by giving an estimate before, then updating during, recording when
done. This feeds back into the system. What I especially liked in the initial estimate was a time window listing the
task splits with seats and their timing — having this available when planning what to take in or not, and when I have
to be available, would be awesome."*

**The instance that raised it (numbers only).** A release arc estimated at 12:55 as six seat steps and two Owner
windows: Research ≈ 13:05 · filings ≈ 13:30 · build ≈ 14:30 · review + one fix round ≈ 15:30 → window 1 ≈ 15:30–16:00
(open + merge, tag) · vendor + review ≈ 16:30 → window 2 ≈ 16:30–17:00 (the pin); three named things that would move it,
+1 h each. Observed: Research 13:00 · build 13:44 · first review 14:12 · two fix-and-verify rounds the estimate did not
have · window 1 not open at 15:15. The estimate lived in a chat message and one ship-log row; the update in another chat
message; nothing in the tracker could be read by a person or a seat as *when am I needed*.

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
- `<seat>` — a seat name from `[seats]`; several joined with `+`; `@A` names the session when more than one runs.
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
plan-by: principal 2026-09-23 12:55
plan: "1 · research · ≈13:05 · — | 2 · principal · ≈13:30 · — | 3 · implementer · ≈14:30 · — | 4 · reviewer+implementer · ≈15:30 · — | W1 · owner · 15:30–16:00 · — | 5 · implementer+reviewer · ≈16:30 · — | W2 · owner · 16:30–17:00 · —"
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
-plan: "1 · research · ≈13:05 · — | 2 · principal · ≈13:30 · — | 3 · implementer · ≈14:30 · — | 4 · reviewer+implementer · ≈15:30 · — | W1 · owner · 15:30–16:00 · — | 5 · implementer+reviewer · ≈16:30 · — | W2 · owner · 16:30–17:00 · —"
+plan: "1 · research · ≈13:05 · 13:00 | 2 · principal · ≈13:30 · 13:33 | 3 · implementer · ≈14:30 · 13:44 | 4 · reviewer+implementer · ≈15:30→15:40@14:38 · — | W1 · owner · 15:30–16:00→15:40–16:00@14:38 · — | 5 · implementer+reviewer · ≈16:30→16:40@14:38 · — | W2 · owner · 16:30–17:00→16:40–17:10@14:38 · —"
+plan-updated: principal 2026-09-23 14:38
```

The body table gains its notes in the same commit (*step 2: the pass deferred — waits for the release, the Owner's
word 14:40 · step 3: one more tracker taken in mid-flight · step 4: a second round the estimate did not have*).
*Who writes it:* the seat whose step finished writes its actual in its own report commit; only the seat named in
`plan-by:` re-estimates; a window moves only by a re-estimate. The board shows the newest window and, beside it, how
many times it moved (`→` count).

### c. The record of a finished tracker (closed the same evening)

```markdown
---
id: FM-0xx
status: Shipped
plan-by: principal 2026-09-23 12:55
plan-updated: principal 2026-09-23 15:12
plan-closed: principal 2026-09-23 17:05
plan: "1 · research · ≈13:05 · 13:00 | 2 · principal · ≈13:30 · 13:33 | 3 · implementer · ≈14:30 · 13:44 | 4 · reviewer+implementer · ≈15:30→15:40@14:38 · 15:52 | W1 · owner · 15:30–16:00→15:40–16:00@14:38 · 15:58–16:04 | 5 · implementer+reviewer · ≈16:30→16:40@14:38 · 16:41 | W2 · owner · 16:30–17:00→16:40–17:10@14:38 · 16:58–17:04"
---
```

*What the tool derives from a closed plan, per seat:* the estimate error (research −5 min · implementer −46, +11 ·
reviewer+implementer +22 on the re-estimate · owner 6 min at the keyboard per window against 30 estimated); the count of
re-estimates (1); the largest miss (step 4). Ten closed plans and the board can print a margin the record earned beside
every new *needed* line — that is the feedback the Owner asked for.

### d. An extract for a multi-session tracker — two sessions of one seat, one Owner

```markdown
---
id: FM-0xx
status: In Progress
plan-by: principal@A 2026-09-23 12:55
plan: "A1 · implementer+reviewer@A · ≈15:40 · 15:52 | W1 · owner · 15:40–16:00 · — | B1 · implementer+reviewer@B · ≈16:00 · 12:22 | B2 · principal@B · ≈12:30 · 12:12 | WB · owner · ~15m · — | A2 · implementer+reviewer@A · ≈16:40 · — | W2 · owner · 16:40–17:10 · —"
---

## Plan

*Two Principal sessions run today by the Owner's design — A on the day's findings and the tool, B on the product items.
A session writes only the steps that carry its `@` mark; the owner's `W` rows are anyone's to read and one session's
to move — the one named in `plan-by:`. A window without a clock (`~15m`) is the Owner's own slot.*

| # | Step | Note |
|---|---|---|
| A1 | Build, review, tag the release | |
| W1 | **Tag the release** | A reports |
| B1 | The negative-control build, its review, the pre-registration | early; waits on B2 |
| B2 | The run sheet for the Owner's hands — four reads, one command each | |
| WB | **The hands sitting — its own slot, outside the standup budget** | B reports; not a standup item |
| A2 | Vendor the tag into the consumer; review | |
| W2 | **Open + merge the pin PR** | A reports; before 07:30 |
```

*What the board draws:* **needed: owner 15:40–16:00 — tag (A) · your own slot ~15 min — the hands sitting (B) ·
16:40–17:10 — the pin PR (A)** — every session's windows in one strip, in clock order, slots without a clock last.
*The rule the extract carries:* a session never edits another session's step; two sessions writing one step is a
finding, not an update.

### What the parser needs (for the Reviewer to attack)

One key, one regex per field, no YAML: split on `|`, then on `·`; step `^(W?[A-Z]?\d+)$`; seats `^[a-z]+(\+[a-z]+)*(@[A-Z])?$`
against `[seats]`; estimate `^(≈\d\d:\d\d|\d\d:\d\d–\d\d:\d\d|~\d+[mh])(→…@\d\d:\d\d)*$`; actual `^(—|\d\d:\d\d(–\d\d:\d\d)?)$`.
The gate refuses a `plan:` whose seat is not in `[seats]`, whose `W` row's seat is not the owner, or whose estimate was
edited rather than appended (the previous commit's value must be a prefix of the new one). About 40 lines and one label
pair; the board's strip about 15 lines of the template. Unproven: whether a person reads a 200-character line — the body
table is the readable copy, and the gate can check the two agree on the step keys.

## Done when

The Owner has ruled which candidate, if any; the chosen one prints *who is needed, when, for what* on the board and in
the digest, from a plan written before the work, updated by each seat's report and closed with the actual; and one full
arc has run on it with its estimate–actual gap in the record.

## Ship log

| Date | Event |
|---|---|
| 2026-09-23 | **Four worked examples added on the Owner's ask, then reworked on his second word — *it must be visual on the board, so it must be in the front matter to be parseable*:** the plan is one `plan:` line (pipe-separated steps, fixed field order, re-estimates appended), *needed* is derived from the owner's rows, the body table holds only step texts; the estimate as filed, an update, the finished record with per-seat error, a multi-session extract, and what the parser needs. Illustrative; nothing built. |
| 2026-09-23 | Filed on the Owner's requirement, tagged `research`, with the instance that raised it as its first evidence. Held against FM-004 (adoption), FM-005 (the person asked mid-flight), FM-006 (a page for the humans). Not built this week — the current path's line 2: tracked, not built. |
