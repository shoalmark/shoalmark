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

**2026-10-13 — the dispatched day's path.** v0.19.4 and its records close-out merged in #165/#166; R14 is shipped.
The release-allocation answer of 12 October is applied to today's briefs: R12 first, bounded stage 1/archive next,
and B1 with the final probe prompt and first outside-run needs in v0.20.1. This is an operational plan on the existing
parked planning tracker, not a build of its proposed planning feature. Trial blockers take precedence when evidenced.

The Owner's dispatch in the coordinating session, quoted as dispatch rather than a new signed policy answer:
"Push URL stays DISABLED. Tell me when a branch is ready; I fetch from your clone and push."
"R12's brief keeps SHOALMARK_CMD on the gate step (068c9e6) and adds a timeout to the Subversion install step."
"R12 is critical: its Reviewer gets a session of its own."
"Codex covers critical builds today, as ruled on 12 Oct; Claude takes over from tomorrow."
Review IDs allocated to this dispatch: RV-3040–RV-3099; RV-3035–RV-3039 remain with the Auditor.
Reservations: R12 3040–3054; records 3055–3069; archive 3070–3084; 3085–3099 reserve.

| Order | Work | Seat | Initial estimate | Stop condition / next available move |
|---|---|---|---|---|
| 1 | Apply signed answers and reconcile today's judgement | Planner; one records Reviewer pass | 20–30 min | A contradiction needs an Owner ruling; independent records work continues. |
| 2 | R12: Ubuntu/3.9 records gate, four truthful pass-throughs, retained command and bounded SVN installs | Codex Builder; separate root critical Reviewer | 1–2 h build; 30–45 min review | Unresolved critical findings or CI after the Owner pushes; advance the filing/archive meanwhile. |
| 3 | FM-044: fresh-main bounded filing, then build judgement | Records Builder; Reviewer; Planner; Owner merges | 45–75 min | Owner replacement merge precedes implementation; analysis and archive preparation continue. |
| 4 | Bounded SVN-without-git skeleton and dependent slices | Research/Planner brief; critical Builders; separate Reviewer | 45–60 min preparation; initial implementation estimate 4–8 h | Filing merge/judgement; no wider plain-folder or platform-proof scope inferred. |
| 5 | Release archive: scoped source port, controls and dry run | Critical Builder; separate root Reviewer | 1–2 h | Integration/review findings or actual release qualification; no local release claim. |
| 6 | Apply #154's signed RV-2734 wording and Part B allocation | Records Builder; Reviewer | 40–60 min | Records findings; signed wording is already supplied. |
| 7 | Recover FM-043's historical upgrade filing | Records Builder; Reviewer | 35–55 min | Freshly verified adopter need determines any later implementation. |
| 8 | B1 conflict inventory for v0.20.1 handoff | Planner/Research; Claude takes design/site implementation | 30–45 min preparation | Claude's next-day availability and stage/archive qualification; no site build today. |
| 9 | Final heads, branch checks and local fetch-ready lines | Planner | 20–30 min | Pending checks/verdicts; only the Owner pushes and merges. |

All estimates are seat time, excluding the Owner's merges and CI. No wait on an answer, verdict or merge stops another
movable item. Every new session configures its actual harness identity before committing; the interruption's existing
commits remain unchanged. Current local base: `e7ce074`; push URL remains `DISABLED`.

**2026-10-13 — preparation completed after restart.** The read-only [stage-1 inventory](evidence/stage-1-inventory-2026-10-13.md) covers current-main process launches and callers, the common skeleton, dependent slices and independent refusal controls. It revises row 4's initial 4–8 h build estimate to **6–10.5 Builder hours**, before archive integration and critical review; overlapping slices start only after the reviewed skeleton. The [B1 conflict handoff](evidence/b1-conflict-handoff-2026-10-13.md) identifies three paths/eight conflict groups and the retained security, CI and pin controls. It supplies Claude's next-day integration order, estimated **2–4 Builder hours** plus review and dependencies. Neither inventory executed runtime checks or built those features.

Stage-1 filing review and Owner merge are complete at #167 / `e6d1e27`; today's command judgement keeps FM-044 P1 #3 build before the [common-skeleton dispatch](evidence/stage-1-builder-brief-2026-10-13.md). Its independent critical review precedes dependent implementation. Its brief must settle the guard capability contract: current main's SVN guard reports unsupported protection, while the recovered acceptance requires refusal when authority cannot be proved. The proposed bounded design keeps current server-author history and legacy configuration semantics, refuses a protected change where its configured proof cannot be obtained, permits harmless local reads, and makes no SVN signature claim. A design that would change authority rights needs a signed Owner decision before that slice; this preparation supplies no such decision. D3/D4 remain held.

R12 is locally READY at `8b7f7f141ad3f4620091591e78a257cc34be53d3`: dedicated independent root Reviewer `01a13544` verified `7af848f`, with current main integrated. RV-3040: recorded privately. Owner fetch/push and required CI remain due. Archive source integration at `3c18008` passed 85 independent local controls, but RV-3070 P2 requires current-main records reconciliation before its final critical round; Builder integration is underway. The Owner merged combined Part B/upgrade records in #168 at `ab7ed3f`, retaining both READY verdicts. Main has the FM-044 filing and those records; it does not yet contain stage-1 implementation. The skeleton and next-day B1 handoff advance while other verdicts and acts wait.

The completed [SVN guard contract analysis](evidence/svn-guard-contract-2026-10-13.md) preserves bare-account author-only and existing rights while refusing unavailable proof. The supplied records establish no consumer policy adoption baseline. The bounded proposal refuses protected acceptance without one and continues unguarded local operations; any new authority/adoption rule needs a signed decision before that case is accepted. Guard work is now estimated at **4.5–7 Builder hours plus 1–2 hours review**, with an initial **60–90 minute** contract/control/refusal deliverable. Full stage implementation is **8.5–14 Builder hours** before archive/integrated review; dependent seats may overlap only from the independently reviewed skeleton with separate function ownership. These seat-time estimates do not promise full stage completion today.

**2026-10-13 — dependent seats prepared while common review runs.** The [ownership handoff](evidence/stage-dependent-ownership-2026-10-13.md) assigns each function once and reserves shared integration to Planner. The common final head `6d0c239` integrates main `ab7ed3f` and is under separate root critical review `01a1358b`; no dependent code has begun. Revised A/B/C/Planner allowances total **10–16.5 Builder seat hours**, including the completed common allowance but excluding archive/integrated review. B first supplies a 60–90 minute proof-interface/refusal portion; new authority remains held. Each isolated branch removes only its own migrated ratchet keys so required unchanged core controls can pass; combined integration retains every parent reduction. The original RV-3003/RV-3004 bodies and individual mapping are missing from local refs and have been requested. Only those fixes wait; other scoped work continues. The archive is now locally READY at `1ba6fc4`, with RV-3070 closed in critical round 2 and an exact-head dry run; required CI, stage integration and release acts remain due.

**2026-10-12 — release allocation for the Owner's sitting.** This proposal replaces the earlier dated release allocation; it adds no planning feature or process. The product proposal on this Parked tracker remains parked. R14's first priority and v0.20.0 inclusion come from the Owner's update, not from an unanswered Planner proposal. Signed scope is in [the rulings](evidence/rulings-2026-10-12.md); only the remaining allocations are offered for their decision. S/M are scope sizes. The known requirement is Subversion without git; no other trial scope is inferred.

| Release / order | Work and replacement | Owner | Size | Dependencies | Confidence and reason |
|---|---|---|---|---|---|
| First; main as soon as ready; v0.20.0 | R14: Owner authorship exemption in hooks, verified Owner signature in CI; replaces application of seat rules to the Owner. | Critical Builder; independent Reviewer; Owner merges and reinstalls hooks | M | Signed R14; FM-033; staffing ask FM-031; trusted policy/signers; actual hook and CI checks | 99%: Owner reports two refusals; never blocking their signed word governs. |
| Second; main as soon as ready, independently of stage 1 | R12: one Ubuntu/3.9 records gate, four truthful pass-through results; replaces five repeated records checks. | Critical Builder; independent Reviewer; Owner merges | S | Signed R12/R25; FM-032; preserve R14 enforcement if already merged | 97%: workflow read confirms repetition; Windows incident is reported, not reproduced. |
| Before stage-1 build | New branch from current main carrying FM-044 as reviewed at 99050b9, RV-2735 to RV-2737 fixed, without RV-3023's sentence; INDEX.md regenerated by the tool. The Owner closes #152 with a pointer to the replacement, merges the new PR; Planner judges FM-044 In Progress through triage. | Records Builder; Reviewer; Owner closes/merges; Planner triages | S | Current main; fresh records pass; process PR already ancestral to edfa73b | 98%: Owner reports GitHub conflict and 137 commits behind; new base avoids the stale INDEX merge. |
| v0.20.0 | Stage 1: Subversion with no git installed; backend dispatch replaces shared paths that assume git. | Builders 1–3; independent critical Reviewer | M | #152 replacement merged and triage; skeleton then dependent branches; R23; D3/D4 boundaries; staffing | 98%: signed scope is explicit; no stage-1 build commit is supplied. |
| v0.20.0 | RV-3002: one printed-command quoting helper replaces inconsistent quoting. | Builder 3; independent Reviewer | S | PowerShell single quotes with doubled embedded quote; shlex.quote elsewhere | 98%: supplied Owner ruling resolves the shell choice. |
| Before v0.20.0 release commit | RV-3003/RV-3004: the release-before-tag pin check and the missing-bash skip count, corrected. | Builder 3; independent Reviewer | S | fm/044-stage-1-ratchet | 97%: fixes follow the supplied ruling; no acceptance run made here. |
| v0.20.0 | Release archive: zip/checksum, RELEASE manifest and archive vendoring replace the git-only acquisition requirement. | Builder 4; separate critical Reviewer; Owner releases | M | Local 23e3f7a; scoped RV-3020/RV-3021 review, 6379acd..23e3f7a; stage-1 target integration; dry run; Owner release-script change | 98%: bundle verified; prior READY is reported, pending re-review stays open. |
| Before v0.20.0 tag | R24: one privately chosen, independently verified credential minimum; replaces the expanded prerelease boundary programme. | Owner chooses/establishes; independent Auditor verifies | S | FM-037 ask; private evidence; retained authority checks | 99%: signed ruling makes this a bounded release condition. |
| v0.20.0 qualification; planned tag 23 October | Candidate, final pins, relevant Mac checks and required CI; replaces repeated full local suites. | Release Builder; Reviewer; Owner dispatches/merges/tags | M | Accepted scope/reviews; first dispatch then separate fixes; final changed tree checked; archive dry run; R24 | 96%: R3 retains CI; required checks validate the final candidate revision. |
| Records when answered | #154 RV-2734: Owner-supplied replacement wording; replaces withdrawn git-on-every-machine wording. | Owner supplies text; Records Builder; Reviewer | S | FM-004 ask; one records pass | 98%: fix text remains the Owner's, not the Planner's ruling. |
| Now, policy | R1/R18/R19 cancel replacement programme, server IDs and compulsory trial reporting; R2–R4 replace mandatory review files/local suites/answer transactions as policy. | Owner's signed rulings; Planner and seats apply | S | 2d62fa1; keep Owner-allocated IDs, full review evidence and signed answers | 98%: these decisions are signed; residual product code is not thereby deleted. |
| Done on current main | R15 switch: #162 / 4685efa sets freeze_at=0; replaces the active intake limit in current main configuration. | Owner | S | 4685efa is present and ancestral to e7ce074; current shoalmark.toml reads freeze_at=0 | 99%: verified in this clone; the separately allocated code deletion is not claimed. |
| v0.20.1 | R15 removes freeze code; replaces obsolete intake refusals while retaining look-before-filing and prioritization. | Builder; Reviewer | S | Reported #162; relevant regressions; trial findings take priority | 95%: configuration switch already removes the operational limit. |
| v0.20.1 | R13 removes ratio command/reporting; retain records classification used by Shipped. | Builder; Reviewer | S | Signed R13; inventory of Shipped consumers | 96%: classification has a surviving authority consumer. |
| Optional earlier, v0.20.0 stage 1 | R13 command deletion only if it reduces stage 1's own routing/refusal work; replaces implementing that command's backend path. | Stage-1 Builder; independent Reviewer | S | FM-023 release-map answer; demonstrated smaller diff; retained Shipped classification; no schedule gate | 85%: --ratio appears in Builder 3's planned git-only refusal list. |
| v0.20.1 | R17 removes partial/untagged trusted-vendor bypasses; replaces weaker source acceptance. | Critical Builder; independent Reviewer | S | Archive merged; verified-source/completeness acceptance; R26 history retained | 92%: archive source rules must settle before changing surviving vendor options. |
| v0.20.1 | R21 removes generated date from committed INDEX and keeps deterministic content checking. | Builder; Reviewer | S | Signed R21; R12; preserve forge-readable index | 94%: source already normalizes the date during checking; Windows cause stays separate. |
| v0.20.1, P2 | R22 repairs Windows drift and displays bounded published-content differences on STALE. | Builder; independent Reviewer where gate changes | M | R12 availability; R21 baseline; real Windows reproduction | 97% in priority/diagnostics; cause remains unverified. |
| v0.21.0 | R5 removes executable producers from trusted core; validated data-only views replace core execution. | Critical Builder; independent Reviewer | M | Signed R5; surviving producer/view consumers inventoried | 94%: removes an authority-crossing surface; safe views still need acceptance. |
| v0.21.0 | R9 removes invitation/notification channels and scheduler state; owed acts/due/completion/history remain. | Builder; Reviewer | S | Signed R9; retained act cases | 86%: prompting weakens, but visible owed work must survive. |
| v0.21.0 | R10 removes runtime branding, fonts and theme copying; static mark, labels and semantic headings remain. | Builder; Reviewer | M | Signed R10; archive manifest/vendor adjustment; localized-heading checks | 91%: theme removal affects the archive's required file set. |
| v0.21.0 | R11 removes global refresh hooks; explicit safe refresh, immediate act visibility and revision/freshness evidence replace triggers. | Critical Builder; independent Reviewer | M | Signed R11; retained act/refresh cases; stage-1 integration complete | 91%: implicit triggers cannot be removed without preserving visible committed results. |
| v0.21.0 | R4 residual transaction-code removal; ordinary signed repository answers replace answer-branch choreography. | Critical Builder; independent Reviewer | M | R14; exact answer/act history and historical readers retained | 94%: signed canonical answers are already policy; code cleanup is separate. |
| v0.21.0, after v0.20.0 | Broader R24 boundary work replaces the expanded release gate with follow-up scope. | Owner; independent Auditor; scoped Builders | M | Verified minimum; independently scoped execution/policy/review/stop controls | 99%: signed R24 explicitly defers this wider programme. |
| v0.21.1, after deletions | R28: pytest modules, parallel workers and isolated template repositories replace surviving monolithic suite setup. | Builder; independent Reviewer | M | Deletions complete; independent expectations; five code jobs; measured comparison | 90%: gains remain unmeasured; test dependency only, no release gate. |
| Held; review 20 October, no release assigned | D3 plain-folder scope; D4 where no-git proof runs; any additional Subversion work. | Owner decides from findings; Planner records | S | Actual trial findings; fresh signed scope; only known requirement is Subversion without git | 98%: R23 lifts stage 1/archive only and explicitly keeps these holds. |
| Held; return 20 October, no automatic deletion | R6 sessions, R7 queue, R8 site, R16 sequencing, R20 configuration/history keys. | Owner and independent Reviewer | S | Attribution; usable queue substitute; arrival/guidance evidence; post-R14 sequencing comparison; bounded compatibility evidence | 98%: each held row has a named evidence condition and needs a fresh signed ruling. |
| Retained through v0.20.0 | R25 five code jobs/names; R26 legacy interpretation; R27 name/mark/headline and truthful claims. | Builders and Reviewers | S | Signed R25–R27; surviving coverage and history | 98%: explicit retained scope prevents incidental deletion. |

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
| 2026-10-13 | Stage-1 and B1 read-only preparation recorded with immutable-ref evidence; stage-1 build re-estimated from 4–8 h to 6–10.5 Builder hours before archive/review, and its guard capability contract remains a brief dependency. B1 has three conflicted paths/eight groups and a 2–4 h next-day integration estimate. R15 configuration switch verified on current main; no feature build, platform proof or publication claimed. |
| 2026-09-23 | **Updated as if FM-024 had landed, on the Owner's word:** every seat step carries its session id (`@a9`, `@d8`), `plan-by:` and the updates name seat and session, the gate matches a step's session to the commit's `Session:` trailer, and the multi-session extract uses the registry's ids and rows. |
| 2026-09-23 | **Four worked examples added on the Owner's ask, then reworked on his second word — *it must be visual on the board, so it must be in the front matter to be parseable*:** the plan is one `plan:` line (pipe-separated steps, fixed field order, re-estimates appended), *needed* is derived from the owner's rows, the body table holds only step texts; the estimate as filed, an update, the finished record with per-seat error, a multi-session extract, and what the parser needs. Illustrative; nothing built. |
| 2026-09-23 | Filed on the Owner's requirement, tagged `research`, with the instance that raised it as its first evidence. Held against FM-004 (adoption), FM-005 (the person asked mid-flight), FM-006 (a page for the humans). Not built this week — the current path's line 2: tracked, not built. |
| 2026-10-13 | Owner #168 merged combined Part B/FM-043 records at ab7ed3f. R12 independent critical verdict is locally READY at 8b7f7f1; RV-3040: recorded privately. Archive RV-3070 current-main integration is being reconciled. Guard analysis records conservative proof refusal and revises seat-time estimates; no new authority or stage completion claimed. |
| 2026-10-13 | Prepared exclusive dependent function/control ownership while common critical review runs at 6d0c239. Corrected ratchet participation so each migrated branch passes required controls; no ceiling expansion, authority rule or code built by this record. Original RV-3003/RV-3004 source requested; other scoped work stays movable. |
