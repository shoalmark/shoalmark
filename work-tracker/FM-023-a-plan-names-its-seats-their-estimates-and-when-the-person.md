---
id: FM-023
status: Parked
considered: FM-004, FM-005, FM-006
tags: research
kind-of-problem: complex
next: build
triaged: 2026-09-24
tier: P3
hook: "A plan names its seats, their estimates and when the person is needed; it is updated as the work runs and recorded when done — so a person can plan what to take in, and when to be available"
---

# FM-023 — a plan names its seats, their estimates and when the person is needed, updated as it runs, recorded when done

Seat: Principal · filed 2026-09-23 on the Owner's requirement. Tagged `research`: written to be attacked before anything
is designed or built.

## What is true now

**2026-10-27 — v0.20.2's scope narrowed, and v0.20.3 named, on the Owner's word of 27 October, as relayed by the Auditor, for their signed answer.** The Owner said "leave them
for v0.20.3", then "I want to also add ASK ids to v0.20.2", on the Auditor's list just before. The ask above puts it to
them. The tables below stay as the record of what was allocated before.

| Release | Work | Depends on |
|---|---|---|
| v0.20.2 | In progress: the CI item (`test_plugin.py` in CI), FM-068, FM-024, FM-076, and S2 (READY at `ec5d19f`). | — |
| v0.20.2 | `/find-drift` and the plugin, in the lane; `/prune-drift` (READY at `9017ad8`), rebuilt onto the lane. | — |
| v0.20.2 | The suite's Chrome keychain flag: the suite starts Chrome with `--use-mock-keychain` and a fresh `--user-data-dir` itself. | — |
| v0.20.2 | Quick win 10: `--sessions` gains the harness and resume columns. | FM-024's round |
| v0.20.2 | S1: the ask ids with R4's answer commit (FM-050). | FM-076 |
| v0.20.2 | FM-063: the trailer step leaves a message that ends in bare links as it is (S), built in the `prepare-commit-msg` hook, so critical. | — |
| v0.20.2 | FM-065: the skill-call contract. Its design is READY WITH FINDINGS (`4dc1910`), and its first use is `/prune-drift` calling `/find-drift`. | `/prune-drift`'s rebuild |
| v0.20.3 | S3, who asked, the receipts and S4, from batch 3. | S1 |
| v0.20.3 | From 18 October's allocation: the prose prune of `shoalmark.py` with the comment ratchet, FM-037's guard, the five conversions, and the text fixes. | v0.20.2's tag |

- **FM-063 and FM-065 stay in v0.20.2,** on the Owner's word of 27 October: "both stay in v0.20.2".

**2026-10-27 — batch 3 and quick win 11's S2 move from v0.20.1 to v0.20.2, for the Owner's signed answer.** On 22
October, with the probe release, the Owner moved them to v0.20.2: batch 3 (S1 with the ask ids, S3, S4 the guided
answer, the receipts, and the sessions with `--sessions` and who asked) and quick win 11's S2. The record never said
so. This entry and the 15 October table's new row say it, and the ask above puts it to the Owner for a signed answer.
- **It amends** v0.20.2's allocation of 18 October (answered at `88bf707`).
- **Once it is answered,** FM-059's release answer of 16 October (*accepted - v0.20.1*, `99b1708`) is named as
  superseded by it.
- **What they need first** is unchanged: FM-050's ask ids and FM-059's guided answer are designed and reviewed, and
  their ruling asks are filed again on today's main.

**2026-10-21 — the tags of v0.20,** on the Owner's ruling of 20 October (recorded privately):
- v0.20.0 and v0.20.1 take lightweight tags, with no release run sheet;
- the last v0.20.x tag, the officially announced release, takes the run sheet, the signed tag and the announcement;
- each lane built on `be19828` takes main's site commits before its pull request.

**2026-10-19 — FM-063 goes to v0.20.2,** the Planner's call, which the Auditor's relay of 19 October left to the
Planner: a seat's commit message that ends in bare links has them rewritten by the trailer step. Until it ships, a seat
ends its message with a sentence. The 18 October table below has a v0.20.2 row for it.

**2026-10-19 — the skill-call contract goes to v0.20.2 (FM-065),** on the Owner's word of 19 October (recorded
privately): one skill calls another, external skills included, through a contract that pins what it calls and checks
what it gets back. It is prepared for from v0.20.2's first release, and no external skill runs in v0.20.2. The 18
October table below has a v0.20.2 row for it.

**2026-10-19 — R11's hook half comes back in v0.20.1,** on the Owner's word of 19 October (recorded privately): the
hooks that rebuild the board after a checkout, a merge and a rebase. v0.20.0 ships as built, with R11's upgrade note.
The 15 October table below has a v0.20.1 row for it, and FM-057 holds the case it must cover.

**2026-10-18 — v0.20.0 is cut from main as it stands.** This is the Owner's ruling of 18 October (recorded privately).
Beside the 12 October allocation and R21, v0.20.0 holds what #189 and #193 merged:
- **#189:** R22, R15, R13, and R11 with what the board read;
- **#193:** R9 with the stand-up and close-out prompts, one stand-up across the repositories you name, and FM-045's fix.

Their rows in the 15 October table below now read v0.20.0. The receipts, and R17 with defect 5's class fix, are not
built and stay in v0.20.1. As the current path's line 3 says, v0.20 is one milestone: v0.20.0 to v0.20.2, as this
tracker allocates them.

**2026-10-18 — v0.20.2: shoalmark's first two skills, in one Claude plugin, for the Owner's ruling.** These are the
Owner's rulings of 18 October. `/find-drift` is the first skill. The second, `/prune-drift`, builds on it; its name is
the Owner's word of 18 October (recorded privately). Both ship in v0.20.2 as a Claude plugin. This table builds nothing.

| Release | Work | Deletion beside it | Depends on |
|---|---|---|---|
| v0.20.2 | `/find-drift`, shoalmark's first skill. It finds where an agent could drift off track, and ranks what can become a check. It looks for three things: a rule held only as prose, two sources that disagree, and obsolete text that still reads as live. It reads, and it changes nothing but its report. Its spec is corrected by a second run, on a codebase shoalmark did not shape. | — | Its first run, on shoalmark at `5dcdcc5` (recorded privately) |
| v0.20.2 | `/prune-drift`, the second skill, built on `/find-drift`. It reads the newest report, and runs `/find-drift` first where no report is fresh. It moves history to the record and rules to checks; only an external quirk stays as prose. | — | `/find-drift` |
| v0.20.2 | The prune of `shoalmark.py`'s prose, proven prose-only, made on v0.20.1's tagged head. Beside it goes the ratchet that holds code comments to external quirks. | A comment that holds a tracker id, a review id, a date or a ruling: its reason is in the commit log and the trackers. | v0.20.1's tag |
| v0.20.2 | FM-037's guard over the seat definitions (`.claude/agents/`) and the skills folder: a change to either must be the Owner's signed commit. | — | A design round first |
| v0.20.2 | Five small conversions, each a rule made a check: the ship log only grows; triage rows only grow; no line of a commit message begins with `---`; the allowed test runner; no home folder's path in public text. | The prose each one replaces | v0.20.1's tag |
| v0.20.2 | The text fixes `/find-drift`'s first run found, in the rule files: sources that disagree, and obsolete text. The seat definitions are the Owner's to type. | The obsolete text | The second skill |
| v0.20.2 | The suite's Chrome keychain flag: on macOS, the suite starts Chrome with `--use-mock-keychain`. | — | v0.20.1's head |
| v0.20.2 | FM-063: the trailer step adds a seat's trailers and changes nothing else in the message, where it ends in bare links (S). | The rule that a seat ends its message with a sentence | — |
| v0.20.2 | FM-065: the skill-call contract (M): its six parts, a registration format and a check, proven by synthetic child skills, and first used by `/prune-drift` calling `/find-drift`. No external skill runs. | — | A design round, then the Owner's ruling |
| After v0.20.2 | R5; defects 1, 3 and 4; the four larger conversions; the broader R24 boundary work. | — | The Owner's allocation |

- **When:** the work may start now.
  - It lands only after v0.20.0 and v0.20.1 are merged, and it merges cleanly onto v0.20.1's head.
  - It never takes a review slot from v0.20.1.
  - A branch that no longer merges cleanly is built again from that head.
- **This row replaces:** the harness plugin of the 15 October table's row *After v0.20.1*. The rest of that row moves
  to *After v0.20.2*.
- **Sizes and seats:** S or M each, on seats of v0.20.2's own, on either harness.
- **Confidence:** 60 % that v0.20.2 is tagged within a week after v0.20.1's tag.

**2026-10-15 — v0.20.1 ships complete, for the Owner's ruling: B1, the board's design, the probe's final prompt, the
eleven quick wins beside the deletions that can ship with them, and R13, R15, R17 and R22.** This is the Owner's direction
of 15 October (recorded privately), set out here for their signed answer. It replaces the allocation of 12 October for
the releases after v0.20.0. The current path's line 5 (`fd44d86`) pairs each deletion with the quick win that takes its
place, and within a release deleting comes first. This table builds nothing, and the planning feature this tracker
proposes stays parked. The rows that read v0.20.0 moved there on 18 October, by the entry above.

| Release | Work | Deletion beside it | Depends on |
|---|---|---|---|
| v0.20.0 | As allocated on 12 October: Subversion without git and the release archive, with the answers of 15 October on FM-004 and FM-044. R21 (#179) lands before the cut. | — | R24's minimum, confirmed and verified before the tag |
| v0.20.0 | The stand-up prompt and the close-out prompt (S each). Each copies a fixed prompt and runs nothing; each is a run sheet for the Owner, so critical. | R9: invitation and notification channels and their scheduler state; owed acts, due, done and their history stay. | — |
| v0.20.0 | What the board read, and when, with its rebuild command (S). | R11: the global refresh hooks; explicit refresh stays. | — |
| v0.20.0 | One stand-up across the repositories you name (M). It runs no repository's deriver, queue or hook. | None in v0.20.0: R5 needs a format for validated data-only views first, a design round, and keeps its own row. | — |
| v0.20.0 | R13's deletion, ahead of the receipts. | R13: the ratio command goes; Shipped's records classification stays. | — |
| v0.20.0 | R15: the filing freeze's code goes, look-before-filing and ranking stay. R22: STALE shows the differing published lines. | — | — |
| v0.20.1 | B1, the landing, integrated as FM-006's answer of 15 October; FM-049's opt-in line, to an issue form here; FM-026's placement in every word. | — | v0.20.0's tag, for its pins |
| v0.20.1 | The probe's final prompt, and what its first outside run needs. | — | v0.20.0's archive |
| v0.20.1 | The board's design, its look and its words, as FM-053's answer adopts `brand/design-guide.md`. | R10's look half: theme layering, the font files, theme copying and the inline wordmark go. A palette by name or by a few tokens in `shoalmark.toml` takes their place, refused below a set contrast. Every board build names each brand file it no longer reads, with the setting that replaces it: never a silent loss. | FM-053 |
| v0.20.1 | Ask ids (M); how this repository proves an answer, said before *accept* (S–M), with defect 8. | R4: an ordinary Owner-signed commit is the canonical answer, and the answer-branch code goes; exact answer and act history are kept. Critical. | FM-050, designed, reviewed and ruled first |
| v0.20.1 | The session list with copy-to-resume (M), the same list in `--sessions` (S), and who asked (S–M), after the fixes of defects 6 and 7 (FM-056, FM-024). | R10's places half: the logo and the labels become settings, the organisation's brand place goes, and `--vendor` stops copying `brand/`. | R6's look, 20 October, for the harness and resume columns; without it they read *not known* and the rest stands |
| v0.20.1 | Receipts, read from git (M): counts the record holds, each with its definition, never a total in a heading. | — (R13 went ahead, in v0.20.0) | R4; FM-055's definitions |
| v0.20.1 | R17: partial and untagged vendoring go. Defect 5's class fix. | — | — |
| v0.20.1 | R11's hook half comes back: the hooks that rebuild the board after a checkout, a merge and a rebase (FM-057), on the Owner's word of 19 October (recorded privately). | — | v0.20.0's tag |
| v0.20.2 | Moved from v0.20.1 on the Owner's word of 22 October, with the probe release: batch 3 (S1 with the ask ids, S3, S4 the guided answer, the receipts, and the sessions with `--sessions` and who asked) and quick win 11's S2. Their v0.20.1 rows above stay as the record of where they were. | — | This tracker's ask of 27 October; FM-050 and FM-059 ruled first |
| After v0.20.1 | R5; defects 1, 3 and 4; the harness plugin; broader R24 boundary work. | — | As on 12 October |
| v0.21.x | Research and complex work, each from a round the Owner allocates, as line 6 says. | — | The Owner's allocation |
| Unchanged | The held rows R6, R7, R8, R16, R20, D3 and D4, looked at on 20 October; R25–R27 kept; #154's prerequisite wording as replaced by the Owner's signed answer of 12 October in adaec88 (#168). | — | As on 12 October |

- **Sizes** are S or M, never L, from the quick-wins design of 15 October, recorded privately, checked in the code at
  `272e374`.
- **Tiers:** every v0.20.1 row is critical but the board's look and words and the receipts, which are code.
- **Order:** B1, the board's design and the probe's prompt are never held up by a quick win. Each quick win builds on
  its own branch and joins the release's integration branch when its review is READY.
- **Confidence:** 70 % that every row is READY in time for one release; the risk is R4, critical and on the longest
  path.

**2026-10-13 — R12 merged; bounded components accepted; P first review NOT READY; correction goes to final verification.**
Owner main `80b60c8` includes #167/#168/#170/#171 and R12 READY `246ccdf`; native/full CI is not inferred
from ancestry. RV-3040: recorded privately. Common READY `ef77527` closes RV-3085–RV-3088; A1/A2 READY
`6fe35f5`, Reviewed `a9a36d4`, closes RV-3089–RV-3091. A caller final READY `4ab9341`, Reviewed `7063dac`,
closes RV-3096; RV-3097 is unused. C final READY `f59a1c1` closes RV-3095. Their acceptance is bounded to
the named common, board/init/install, caller and CLI component scopes, not full Stage 1.

The Owner's coordinating-session dispatch remains:
"Push URL stays DISABLED. Tell me when a branch is ready; I fetch from your clone and push."
"R12's brief keeps SHOALMARK_CMD on the gate step (068c9e6) and adds a timeout to the Subversion install step."
"R12 is critical: its Reviewer gets a session of its own."
"Codex covers critical builds today, as ruled on 12 Oct; Claude takes over from tomorrow."
Review IDs RV-3040–RV-3099 are allocated here; RV-3035–RV-3039 stay with the Auditor.
Reservations remain R12 3040–3054, records 3055–3069, archive 3070–3084 and stage 3085–3099.
P first critical verdict `62ecf9c`, Reviewed `de17860`, requires the RV-3098 consumer-binding correction.
The correction is built; the same independent ROOT owes the one remaining final verification.
RV-3099: recorded privately
No exhausted finding receives a third round.

| Rank / step | Work and seat | Estimate | What stops it / next movable work |
|---|---|---|---|
| 1 | R12 READY `246ccdf` merged; Owner/CI supplies qualification evidence | evidence wait | Actual remaining CI failure; local stage work continues. |
| 2 | Archive standalone READY `b2e5195`; common integration HELD RV-3072 at final NOT READY `eabee22`; outside strict-classification proposal complete | Owner disposition wait | Exhausted rounds; no third verification or production repair. Local work continues. |
| 3a | A1/A2 and callers READY `6fe35f5` / `4ab9341`; ordinary local composition complete | complete | Component scopes remain bounded; P entry review is next. |
| 3b | B readers HELD RV-3092–RV-3094 at final NOT READY `99968f2`; outside structural proposal complete | Owner disposition wait | Exhausted rounds; local entry work continues. |
| 3c | C bounded CLI READY `f59a1c1`; actual main/preflight/Tortoise wiring assembled by P | build complete | Independent P review and native qualification remain due. |
| 4 | P commits the first-pass correction, then the same independent ROOT performs final verification | 10–20 Planner min; 30–60 Reviewer min | New concrete integration findings or required CI; keep every parent reduction and all held scopes. |
| 5 | B1 read-only conflict inventory complete; Claude takes design/site tomorrow | future 2–4 Builder h plus review | Next-day staffing and stage/archive dependencies; no site code today. |

These are seat estimates excluding Owner/CI waits, not a full-stage finish promise. The first P verdict
is NOT READY. The corrected local source `344db0516be7876a796f19c40b3d4334208ae33524dee1a20b8dbdf489d9b1fe` passes
compile 0.782 s, unchanged core 303/303 in 52.394 s and the exact new aggregate wiring
619/619 with zero skips in 151.345 s. Seven required source-binding refusal controls
fail before the three-line correction and pass after; current wiring includes 92 binding controls.
Every parent's allowlist removal remains, leaving 28 starts. Boundary/scanner/ceiling/source/history
proof limits remain frozen; held B and archive implementations stay excluded. These build checks are
neither final P READY nor full CI. Component verdicts and their limits remain unchanged.
RV-3003/RV-3004: recorded privately

Owner confirms no SVN consumer has adopted shoalmark. Full protected acceptance waits for authenticating
consumer proof, recorded adoption and trial findings; held rulings return 20 October. Local entry says its
signature/author verification limit once. Ordinary legacy-history-dependent controls explicitly use file://
history without treating supplied account strings as authenticated authority. No new policy baseline, rights,
source-HERE authority or blanket ordinary-operation refusal is introduced.

Archive and B outside proposals are development evidence for existing board disposition asks, not verdicts
or authority to apply the held repairs. The canonical [ownership/API record](evidence/stage-dependent-ownership-2026-10-13.md)
and [Builder brief](evidence/stage-1-builder-brief-2026-10-13.md) remain the tasking. Protected-request/past-policy
proof, native/full CI and release qualification remain held or due. All reports use actual identities; old
stale trailers remain unchanged. Owner fetches/pushes/opens/merges and eventually tags; a wait never stops
another ranked item that can move. This records operational dispatch on the parked planning tracker, not its
proposed planning feature.

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

**2026-10-17** · Do you allocate v0.20.1 and the releases after it as this tracker's table of 2026-10-15 sets out: v0.20.1 complete, with B1, the board's design, the probe's final prompt and the ten quick wins beside their deletions?
**answered** — accepted - yes but it is eleven quick wins to my count including guided-answer · holgo99
**relation** — accepted with a change
**signed** — 8a13e8c · G

**2026-10-18** · Do you allocate v0.20.2 as the table of 2026-10-18 sets out: /find-drift and the second skill in one Claude plugin; the prune of shoalmark.py's prose, proven prose-only; the comment ratchet; FM-037's guard on agents and skills; five conversions; the text fixes; the suite's Chrome keychain flag?
**answered** — accepted - yes · holgo99
**relation** — accepted the proposal
**signed** — 88bf707 · G

**2026-10-27** · Do you amend v0.20.2's allocation of 18 October as FM-023's What is true now (27 October) sets out: batch 3 (S1 with the ask ids, S3, S4 the guided answer, the receipts, and the sessions with --sessions and who asked) and quick win 11's S2 move from v0.20.1 to v0.20.2, as you said on 22 October?
**answered** — accepted - yes · holgo99
**relation** — accepted the proposal
**signed** — 3996506 · G

**2026-10-27** · Do you amend v0.20.2's allocation as FM-023's What is true now (27 October, the scope) sets out: v0.20.2 keeps the work in progress and adds the Chrome flag, quick win 10, S1, FM-063 and FM-065; v0.20.3 takes S3, who asked, the receipts, S4 and the rest of 18 October's allocation?
**answered** — accepted - yes - but also with FM-076, with ask ids quick-win 3, S2 and the /find-drift and /prune-drift skills · holgo99
**relation** — accepted with a change
**signed** — 62ac263 · G

## Ship log

| Date | Event |
|---|---|
| 2026-10-27 | The Owner's signed answer to the scope ask (`62ac263`, #217): "accepted - yes - but also with FM-076, with ask ids quick-win 3, S2 and the /find-drift and /prune-drift skills". Every item it names is already in v0.20.2's scope, so no new allocation follows; the ask is cleared. Records only. |
| 2026-10-27 | FM-063 and FM-065 stay in v0.20.2, on the Owner's word of 27 October: two rows and the ask amended. Records only. |
| 2026-10-27 | v0.20.2's scope narrowed and v0.20.3 named, on the Owner's word of 27 October: a table of both, and the ask for their signed answer that amends v0.20.2's allocation. Records only. |
| 2026-10-27 | Batch 3 and quick win 11's S2 recorded as moved from v0.20.1 to v0.20.2, on the Owner's word of 22 October, with a row of the 15 October table; the ask filed for the Owner's signed answer, amending v0.20.2's allocation of 18 October. Records only. |
| 2026-10-21 | The tags of v0.20, on the Owner's ruling of 20 October (recorded privately): lightweight for v0.20.0 and v0.20.1; the run sheet, the signed tag and the announcement for the last v0.20.x. |
| 2026-10-19 | FM-065, the skill-call contract, allocated to v0.20.2 on the Owner's word of 19 October (recorded privately): one v0.20.2 row; nothing is designed or built. |
| 2026-10-19 | FM-063 filed, a bug, and allocated to v0.20.2, the Planner's call: one v0.20.2 row; nothing is built. |
| 2026-10-19 | R11's hook half comes back in v0.20.1, on the Owner's word of 19 October (recorded privately): one v0.20.1 row; v0.20.0 unchanged. |
| 2026-10-18 | v0.20.0 cut from main as it stands, on the Owner's ruling of 18 October (recorded privately): R22, R15, R13, R11, R9 and the stand-up across repositories move from v0.20.1, with the two prompts, what the board read and FM-045's fix. The second skill is named `/prune-drift`, the Owner's word of 18 October. |
| 2026-10-18 | v0.20.2's allocation ask filed: shoalmark's first two skills in one Claude plugin, on the Owner's rulings of 18 October. The answer of 17 October recorded under the asks, and v0.20.1's count of quick wins made the Owner's eleven, the guided answer among them. |
| 2026-10-15 | The allocation ask filed: v0.20.1 complete, on the Owner's direction of 15 October (recorded privately). |
| 2026-10-13 22:21 CEST | P first critical NOT READY `62ecf9c`, Reviewed `de17860`; RV-3098 source-binding correction and real controls are built. Current runtime 619/619 and unchanged core 303/303 pass. Sole final verification remains; component verdicts and exhausted B/archive/protected holds stand. |
| 2026-10-13 20:08 CEST | Archive final NOT READY `eabee22`: RV-3071 CLOSED, RV-3072 HELD after the final round; strict-classification disposition proposed on the board. A1/A2 accepted component merged locally; C bounded READY `f59a1c1`; B final review and A caller migration continue. Local stage work proceeds separately; protected acceptance remains held. |
| 2026-10-13 19:48 CEST | Current-main fetch confirms R12 READY merged at `3cac843`; A1/A2 independently READY `6fe35f5`. B/C corrections and archive final verification continue; local P/Tortoise entry work proceeds through those waits. No adopted SVN consumer exists; protected acceptance/trial holds return20Oct. |
| 2026-10-13 18:18 CEST | RV-3057 P3 fixed forward: archive records READY `b2e5195` replaces the stale running-review paragraph and rank-2 row; inherited common records READY `84c8a6b` needs no re-pass. Serial integration and CI/release holds remain. |
| 2026-10-13 17:42 CEST | **Dependent dispatch from critical common READY:** `ef77527` closes the four common findings; current-main merge `1fc12b0` retains its exact product and passes gate/ratchet. A first local board slice60–90 min (2.25–3.75 h total), B first missing-proof refusal60–90 min (4.5–7 h total), C first capability/control slice30–45 min (1.5–2.5 h plus private tasking). P owns serial shared/archive integration. RV-3003/RV-3004: recorded privately. |
| 2026-10-13 | Stage-1 and B1 read-only preparation recorded with immutable-ref evidence; stage-1 build re-estimated from 4–8 h to 6–10.5 Builder hours before archive/review, and its guard capability contract remains a brief dependency. B1 has three conflicted paths/eight groups and a 2–4 h next-day integration estimate. R15 configuration switch verified on current main; no feature build, platform proof or publication claimed. |
| 2026-09-23 | **Updated as if FM-024 had landed, on the Owner's word:** every seat step carries its session id (`@a9`, `@d8`), `plan-by:` and the updates name seat and session, the gate matches a step's session to the commit's `Session:` trailer, and the multi-session extract uses the registry's ids and rows. |
| 2026-09-23 | **Four worked examples added on the Owner's ask, then reworked on his second word — *it must be visual on the board, so it must be in the front matter to be parseable*:** the plan is one `plan:` line (pipe-separated steps, fixed field order, re-estimates appended), *needed* is derived from the owner's rows, the body table holds only step texts; the estimate as filed, an update, the finished record with per-seat error, a multi-session extract, and what the parser needs. Illustrative; nothing built. |
| 2026-09-23 | Filed on the Owner's requirement, tagged `research`, with the instance that raised it as its first evidence. Held against FM-004 (adoption), FM-005 (the person asked mid-flight), FM-006 (a page for the humans). Not built this week — the current path's line 2: tracked, not built. |
| 2026-10-13 | Owner #168 merged combined Part B/FM-043 records at ab7ed3f. R12 independent critical verdict is locally READY at 8b7f7f1; RV-3040: recorded privately. Archive RV-3070 current-main integration is being reconciled. Guard analysis records conservative proof refusal and revises seat-time estimates; no new authority or stage completion claimed. |
| 2026-10-13 | Prepared exclusive dependent function/control ownership while common critical review runs at 6d0c239. Corrected ratchet participation so each migrated branch passes required controls; no ceiling expansion, authority rule or code built by this record. Original RV-3003/RV-3004 source requested; other scoped work stays movable. |
| 2026-10-13 | Common critical round 1 and addendum are NOT READY with RV-3085–RV-3088 open; fixforward and one remaining verification round precede dependent code. RV-3003/RV-3004: recorded privately. Owner supplied the original private inputs; the missing-source stop is removed. |
