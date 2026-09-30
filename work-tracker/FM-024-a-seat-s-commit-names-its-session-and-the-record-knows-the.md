---
id: FM-024
status: In Progress
considered: FM-005, FM-007, FM-008
tags: research
kind-of-problem: complicated
triaged: 2026-09-25
rank: 9
tier: P2
done: "2026-09-27T13:44:37+02:00 · work-tracker/evidence/reviews/review-fm-029-0-18-3-fourth-pass.md"
next: build
ask: "Do the status-line scripts for Claude and Codex and the addressing rule ship with shoalmark, so a pinned copy carries them?"
ask-kind: ruling
ask-since: 2026-09-28
ask-options: "all three: --statusline, --install-statusline for Claude and Codex, and the AGENTS.md rule with --whoami | the status line only: --statusline and its install, no rule and no --whoami | the rule only: To: <session> <seat> (<worktree>) in AGENTS.md and --whoami, no status line"
ask-proposal: "all three: --statusline, --install-statusline for Claude and Codex, and the AGENTS.md rule with --whoami"
answer: "accepted - all three: --statusline, --install-statusline for Claude and Codex, and the AGENTS.md rule with --whoami"
answered: 2026-09-28
answered-by: holgo99
hook: "Two sessions of one seat are one author in git; a seat's commit must name its session, and the record must know what that session was convened for"
---

# FM-024 — a seat's commit names its session, and the record knows the session

Seat: Principal · filed 2026-09-23 on the Owner's question — *"every seat needs an id or a session id that we can track
and trace back to the record; what if I run a session in parallel with another Principal seat — how do we know which one
it was? Let us reason about how to solve this right from the start."* Written to be attacked.

## What is true now

**Slice 1 built 2026-09-23 on `fix/0.17.6-a-seats-commit-names-its-session-and-the-record-knows-the-session`, for
0.17.6, verified with findings closed; open for the merge, not merged.** S1–S8 as ruled below, one commit per row, then
one per review finding (R1–R7): `seat.session` and `--session new` (S1); the `prepare-commit-msg` hook and
`--session-trailer`, and `--session-check` on every commit (S2, R4); `sessions.md`, `--session open/close`, a
sub-agent's id derived from its parent's, a parent read only from a token in the session-id form (S3, R3, R6); the
gate's three refusals, the Owner exempt, and a seat never removing, dropping or re-opening a row of the registry it is
judged against (S4, R1); abandoned rows listed by `--check`, closed by `--triage` (S5); `Reviewed:` verdicts reported
*independent · same session · untraced · on trunk* over the branch's own commits — `<tip> ^<trunk> --no-merges`,
less verdicts; a branch the trunk has merged is read against the trunk before the merge that brought it (S6, R2); the
board's strip and the digest's line (S7). **15 FM-024 checks** (14 in `test_shoalmark.py`, 1 in `test_core.py`); each
fails on 0.17.5 except S4's control (an open row of the author's seat, the Owner, a commit from before the registry).

**The sessions the release's commits carry.** Row `8d6537be` (implementer, opened in the S3 commit) is closed —
*re-opened as 8e509911/implementer-1: the parent's id was known* (R3). The commits from S1+S2 to the release commit
(`89e0586` … `0743a45`) carry `Session: 8d6537be`; the fix commits from `3392b0a` on carry `Session:
8e509911/implementer-1`; the Reviewer's verdicts carry `8e509911/reviewer-1`. The Principal session is `8e509911` in
every row. So `--check` reads the verdict on `0743a45` as *independent* — its range names only `8d6537be`, a
measurement 0.17.6 cannot repair — and the verdict on `acec312` as *same session*, which is the truth: builder and
Reviewer are sub-agents of one session.

**Decided in the build, for the Reviewer to attack** — none widens the slice:
- **Adoption is the registry's existence.** A tree without `sessions.md` is not judged, and neither is any commit made
  before the file existed in its tree. Without this, every consumer with `[seats]` would be refused on vendoring, and
  every merge bringing a seat commit from before 0.17.6 would turn `--check` red on its trunk. **Once adopted, the
  registry is not the seat's to undo** (the Reviewer's R1): a seat's commit that removes it, drops a row or re-opens an
  ended one is refused and judged against its parent's registry; the Owner is exempt. No configuration switch.
- **The implementer's first id, `8d6537be` from `--session new`, was wrong** (the Reviewer's R3): the harness gave this
  sub-agent its parent's id (`CLAUDE_CODE_SESSION_ID` = `8e509911…`, with `CLAUDE_CODE_CHILD_SESSION=1`), which is
  exactly what S3's `<parent>/<seat>-<n>` needs. Row `8d6537be` is closed with that note, and the rest of the build
  runs as `8e509911/implementer-1`. The commits `89e0586` … `0743a45` keep `Session: 8d6537be`: trailers are not
  rewritten, so 0.17.6's own first verdict is no measurement of independence.
- **The reviewed range** (the Reviewer's R2, the Principal's ruling): the branch's own commits, `git rev-list <tip>
  ^<trunk> --no-merges` (`origin/main`, else `main`, else `master`), less other verdicts — what the branch merged in from
  the trunk is not its. **Beyond the ruling's formula, for the Principal to strike:** a tip the trunk has since merged is
  measured against the trunk as it stood before the merge that brought it (`^M^1`); by the formula alone every verdict of
  the week would read *on trunk* the moment its branch lands, and the week's count would empty. A tip on the trunk's own
  first-parent line reads *on trunk — not a branch verdict*. **A third word, *untraced*,** for a verdict or a range that
  names no session.
- **Where the gate runs** (the Reviewer's R4): the pre-commit hook — `--install-hook`'s and shoalmark's own lefthook —
  runs `--session-check`, the session rule alone, on every commit, a tracker staged or not; the full gate still runs
  when a tracker, the configuration or the tool is staged.
- **This worktree's hooks:** `core.hooksPath` (worktree setting) points at a private copy of lefthook's scripts, now
  with `prepare-commit-msg`, so the repository's shared `.git/hooks` were not changed. lefthook's own sync rewrote
  `.git/info/lefthook.checksum`. Another checkout gets the trailer after `lefthook install`.

**Filed 2026-09-23.** A seat commit carries one identity: the author (`principal@seat`), which is what
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

## Examples — how candidate 1 would look, on the Owner's ask (illustrative, nothing is built)

### a. A session starts — the worktree is the badge, the session is its second line

```bash
git worktree add ../principal-a9 -b feat/…            # one worktree per SESSION, never shared
git -C ../principal-a9 config --worktree user.email principal@seat      # the seat: who may
git -C ../principal-a9 config --worktree seat.session a9                # the session: which run (first 8 of the harness's id)
python3 shoalmark.py --session open a9 principal "the Owner, 2026-09-23 12:21" "the day's findings into the tool; 0.17.5" ../principal-a9
```

The last line writes the session's row (below) and is the session's first commit; the hook refuses any seat commit
before it. The Owner's own commits need none of this — his signature is his id.

### b. The commit, as git shows it — the trailer the hook appends

```text
commit 049a9ab…
Author: Principal seat <principal@seat>          ← the seat, read by the gate for rights
Date:   2026-09-23 15:21:07 +0200

    FM-023: the plan lives in the front matter — …

    Session: a9                                  ← appended by the commit-msg hook from seat.session; never typed
```

```bash
git log --format='%h %ae %(trailers:key=Session,valueonly)'      # 049a9ab principal@seat a9
```

### c. The registry — `work-tracker/sessions.md`, one row per session

```markdown
| Session | Seat | Convened by | Scope (one line) | Worktree | Started | Ended |
|---|---|---|---|---|---|---|
| d8 | principal | the Owner, 2026-09-23 07:28 | the product items: the negative control, the hands run sheet | worktrees/principal | 2026-09-23 07:28 | — |
| a9 | principal | the Owner, 2026-09-23 12:21 | the day's findings into the tool; 0.17.5 | worktrees/principal-2 | 2026-09-23 12:21 | — |
| a9/reviewer-1 | reviewer | session a9 | attack a tip | worktrees/reviewer-2 | 2026-09-23 12:36 | 2026-09-23 13:31 |
| a9/implementer-1 | implementer | session a9 | build 0.17.5 | shoalmark-impl | 2026-09-23 13:10 | — |
| b0 | principal | the Owner, 2026-09-22 16:06 | (no scope given) | a client repository | 2026-09-22 16:06 | closed by the pass of 2026-09-24 — no commit since 09-22 19:36 |
```

- **A collision, as the registry shows it:** two open rows naming one worktree —

```markdown
| d8 | principal | the Owner, 07:28 | … | worktrees/principal | 07:28 | — |
| a9 | principal | the Owner, 09:16 | … | worktrees/principal | 09:16 | — |      ← the gate: "worktrees/principal is open under d8 — one worktree per session"
```

- **A sub-agent** carries its parent's id and its own hand (`a9/reviewer-1`); *convened by* is the session, not a person —
  the person is one row up.

### d. A verdict commit under the independence rule

```text
commit 5e1f0a2c
Author: Reviewer seat <reviewer@seat>
    the consumer's count tracker: the Reviewer pass on 3a7d1e0b — NOT READY (16 findings)
    Reviewed: 3a7d1e0b                           ← the tip judged; the branch's head at that moment
    Session: a9/reviewer-1                       ← a sub-agent of a9 — the author's session
```

```text
gate: verdict 5e1f0a2c on 3a7d1e0b — the reviewed range was authored under session a9; the verdict's session is a9/reviewer-1.
      Recorded as: NOT INDEPENDENT (same session). The count on the board says so; the verdict itself stands.
```

An independent verdict differs in its session root (`k3/…` on a range authored under `a9`), and the strongest form —
a seat key in its own container — is FM-007's line, a second field later, not this one's replacement.

### e. What the board prints, and what the gate refuses

```text
sessions · 3 open — d8 principal (the product items) · a9 principal (the tool, 0.17.5) · a9/implementer-1 (build 0.17.5)
reviews this week · 6 verdicts · independent 1 · same session 5
```

```text
refused: commit by principal@seat carries no Session: trailer — set `git config --worktree seat.session <id>` and open the row (--session open)
refused: Session: q7 has no open row in work-tracker/sessions.md
refused: worktrees/principal is open under session d8 — one worktree per session
```

### f. The plan's mark (FM-023) is this id

```markdown
plan: "A1 · implementer+reviewer@a9 · ≈15:40 · 15:52 | W1 · owner · 15:40–16:00 · — | B2 · principal@d8 · ≈12:30 · 12:12"
```

## Slice 1 — 0.17.6, the Owner's word 2026-09-23 15:40: *"FM-024 has to land as a prerequisite … land this in a v0.17.6 before tomorrow"*

The design choices below are the Principal's, recorded so the Owner can strike any of them; none is an ask.

| # | Built in 0.17.6 | Decided |
|---|---|---|
| S1 | `seat.session` — a per-worktree git configuration value; `--init` and the README say so beside `user.email`. The id: the harness's session id, first eight hex characters, else `python3 shoalmark.py --session new` prints one. Uniqueness is checked against the registry only. | the id's source |
| S2 | The trailer `Session: <id>` appended by a `prepare-commit-msg` hook the tool installs (`--install-hook` writes it beside the pre-commit hook); a consumer with its own hook runner gets one line to call `python3 shoalmark.py --session-trailer "$1"`. Never typed by hand; a commit that carries one already is left alone. | |
| S3 | The registry `work-tracker/sessions.md`: `--session open <id> <seat> "<convened by>" "<scope>" [<worktree>]` writes a row and stages it; `--session close <id>` dates *ended*. A sub-agent's id is `<parent>/<seat>-<n>` (`a9/reviewer-1`): parent and hand, *convened by* = the parent session. The cost of breaking it, measured on this release: the implementer registered from `--session new` as `8d6537be`, and the independence report called the Reviewer's verdict *independent* of the builder though both were sub-agents of session `8e509911` — so `--session open` now refuses a session convened by a session unless its id derives from the parent's (R3). | sub-agents carry parent and hand |
| S4 | The gate (`--check`, the pre-commit): a commit by a seat named in `[seats]` must carry a `Session:` whose row is open and whose seat is the author's; the Owner's commits are exempt; a worktree already open under another session is refused (*one worktree per session*). Exit 4 with the three messages of example e. | |
| S5 | Abandoned rows: `--triage` and `--check` list open rows with no commit for more than a day; the next pass closes them and says so in its paragraph. Nothing closes silently. | who closes an abandoned row |
| S6 | Verdicts: a review commit names the tip it judged with a `Reviewed: <sha>` trailer (the Reviewer types this one); `--check` computes the reviewed range's sessions (merge-base with `main` → tip) and **reports** each verdict as *independent* or *same session*; the board's line *reviews · independent n · same session m*. **A report, not a refusal** in 0.17.6 — the refusal is slice 2, after one week of counts. | count first, refuse later |
| S7 | The board's strip: *sessions · n open — id seat (scope)*; the digest one line: open sessions by seat. | |
| S8 | Tests: the trailer appended and left alone; a seat commit without a row refused; a collision refused; the Owner exempt; the registry's parser on a planted file; a sub-agent id; the independence report on a planted range; the abandoned-row listing. Each fails against 0.17.5. | |

Not in slice 1: the seat key in a container (FM-007's line, a second identity later); the refusal of same-session
verdicts (slice 2); FM-023's plan marks (its own release, after it is ripe).

## Open items

- **The Reviewer's R6 residue.** An 8-character all-hex token in *convened by* that is not a session id (an 8-digit
  date such as 20260923, an 8-character commit hash) is read as a parent and refuses a top-level session; loud,
  avoidable by wording; a 7-character hash or upper-case hex passes unread. Fix: read a parent only from a token that
  is a registered session id, or require a letter a–f. 0.17.8 or later.

## What would decide it

- Over one week: how many seat commits could not be traced to a convening word without the registry (today: all).
- Whether the independence count changes a verdict on 09-29 — if every review is a sub-agent of the author's session,
  the count says so and the container question moves up.

## The Auditor's change brief of 2026-09-30, graded — the strip grouped by parent, model and effort from the harness's logs

**2026-09-30 06:11:21** (the transcript's stamp) · the Auditor (8b91dba2), through the Owner — his paste headed *To: 8e509911
principal (shoalmark-principal-4)*, five lines, saved word for word, sha256 `8e8f77ce3ec60e8b09efb94095c1dc4651665a9fcfbd8312c76cc39a7ad82c12`,
quoted here whole:

> To: 8e509911 principal (shoalmark-principal-4)
> The Auditor — the open relay of 2026-09-28 09:01:54 (folded into FM-024 under Raised; not built at main 792dbca, board_sessions shoalmark.py:5462), now with the Owner's addition: each session's model and reasoning effort. A change brief, yours to grade:
> 1. Group the sessions strip by parent: one line per parent, "<parent> <seat> (<worktree>) · implementer 1–6 · reviewer 1–5, 7", header "sessions · <parents> in the last day (<all> with their sub-sessions)"; each sub-session's worktree, model and effort on expand; a parent without a commit of its own still gets its line; the plain-text line groups the same way.
> 2. Model and effort come from the harness logs, never self-report: Claude Code transcripts (~/.claude/projects/<slug>/<id>.jsonl, sub-agents under <id>/subagents/) record message.model, perTurnEffort and cwd per turn; Codex rollouts (~/.codex/sessions/…) record session_meta id+cwd and turn_context model+effort. --whoami finds the live log whose cwd is the committing worktree (unique under one worktree per session; two matches → refuse) and the seat's commit carries git trailers Session:, Model:, Effort: (parsed with git interpret-trailers). The board reads the trailers; it never reads transcripts. The reader takes those fields only, never message content.
> Done when: fixtures of a Claude parent with sub-agents and a Codex session yield the right trailers; an ambiguous cwd refuses; a commit without trailers shows "—"; 3 parents with 25 sub-sessions render 3 lines; the board suites stay green. Scope: FM-024's answered slice; no new ask. One Reviewer pass.

Graded by the Principal the same morning and reported to the Owner; filed on his word of 06:38:10 — *"Let's file this. Work
is postponed after another task that is waiting for you."* (normalised). **Nothing is built.** FM-024 stays *In Progress*,
`next: build`; the brief widens the slice his answer of 2026-09-28 opened (all three: `--statusline`, `--install-statusline`,
the AGENTS.md rule with `--whoami`) and extends the raise of 2026-09-28 09:01:54 under *Raised*.

| The brief's point | Grade | Confidence | Why |
|---|---|---|---|
| 1 — the strip grouped by parent: one line per parent with its sub-sessions' seats and numbers, each sub-session's worktree, model and effort on expand, a parent without a commit of its own still on the strip, the plain-text line grouped the same way | accept | 90 % | derivable from the `Session:` trailers the strip already reads (`<parent>/<seat>-<n>`, S3); the folded raise of 2026-09-28 asked the same without model and effort |
| 2 — model and effort from the harness's logs, never self-report; the seat's commit carries `Model:` and `Effort:` beside `Session:`; the board reads trailers only, never a transcript; the reader takes those fields only, never message content | accept the principle | 85 % | the fields exist, measured 2026-09-30 06:5x on this machine (the logs grow): this session's Claude Code transcript carries `message.model` and `perTurnEffort` on 5,587 turns each; 387 Codex rollouts sit under `~/.codex/sessions/`, the newest with `session_meta` and `turn_context` naming model and effort, as the brief says |
| 2 — the mechanism: `--whoami` finds the live log whose `cwd` is the committing worktree; two matches refuse | **reject — P1 on the brief** | 99 % | measured on this session's own transcript: `cwd` is the directory the session was launched in, on every turn — 15,175 turns carry that one directory (a parent project's checkout), 110 the directory of a relaunch, none a seat worktree, though this session committed in several; the 155 sub-agent logs under `<id>/subagents/` carry the parent's launch directory on all 68,904 of their turns while those seats committed in their own worktrees. For a commit in a seat worktree the match finds no log at all; for a commit in the launch directory it finds the parent's log and every sub-agent's, and *two matches → refuse* refuses it whenever one sub-agent has run. Either way no seat commit gets its trailers |
| the fix — the Principal's, for the build | proposal | 85 % | match by the harness's own ids, never by a path: the harness names a sub-agent's log `agent-<id>.jsonl` and returns that id to the spawning session, so the Principal writes it into the seat worktree's configuration beside `seat.session` (S1), and `--whoami` opens exactly `<root>.jsonl` or `<root>/subagents/agent-<id>.jsonl` and reads the newest `message.model` and `perTurnEffort` — no search, nothing to disambiguate; for Codex, `CODEX_THREAD_ID` names the rollout. A suite check plants a transcript whose message content is a sentinel and asserts the reader's output never carries it |
| *one Reviewer pass* | the code loop | 90 % | the change is to `shoalmark.py`, its tests and the hook's trailer — the code tier's full loop by AGENTS.md (the Reviewer's RV-724 on FM-041 refused one pass for a code change); same-session Reviewers, their independence reported by S6 as every verdict's is |

Cost, if the Owner says go: about two hours on Sonnet seats — a build, the hook's suites, the loop, the Principal's gate.
Postponed on his word of 06:38:10; the task he named as waiting comes first.

## Raised

*One sourced line per raise — the date, who raised it, the fact, its source, what it undermines.*

- 2026-09-28 09:01:54 · Auditor (8b91dba2), through the Owner (his paste headed *To: 8e509911 principal (shoalmark-principal-4)*, four lines, saved word for word, sha256 `a375a843e12228c9229076e9af8b0f6ff22516f16f31156d67f0a75a870118ac`; its point 2 quoted here) · *"The sessions strip, 80%: group the sub-sessions under their parent, e.g. "8e509911 principal (principal-2) · implementer 41, 42, 45 · reviewer 33, 38, 41, 42, 44"; each sub's worktree on expand. Fits FM-024. Yours to file or fold."* — folded here as a line of the slice his answer of 08:11:26 opened (all three: `--statusline`, `--install-statusline`, the AGENTS.md rule with `--whoami`): the sessions strip groups the sub-sessions under their parent session, each sub's worktree on expand · source: the paste; the strip as `board_sessions` renders it at main `eb00e96b` · undermines: no signed rule — a design line for the slice
- 2026-09-30 06:11:21 · Auditor (8b91dba2), through the Owner (his paste headed *To: 8e509911 principal (shoalmark-principal-4)*, five lines, saved word for word, sha256 `8e8f77ce3ec60e8b09efb94095c1dc4651665a9fcfbd8312c76cc39a7ad82c12`; quoted whole in the section above) · a change brief for the answered slice: the strip grouped by parent (the line of 2026-09-28 above, extended), each session's model and reasoning effort from the harness's logs as `Model:` and `Effort:` trailers, `--whoami` matching the live log by its `cwd` · graded by the Principal the same morning, the section above: the grouping and the principle accepted, the `cwd` match rejected on a measured fact (a match by the harness's ids proposed), the code loop not one pass; nothing built, postponed on the Owner's word of 06:38:10 · source: the paste; the strip as `board_sessions` renders it at main `792dbca` · undermines: no signed rule — a design brief for the slice
- 2026-09-30 09:12:44 · the Owner, in chat · *"Version `.claude/agents/implementer.md` (and a `reviewer.md`) in both repositories. Currently these are excluded by .gitignore."* (normalised) — this repository had no `.claude/` and no ignore rule for it; the two seat definitions now ship in `.claude/agents/` (the Implementer on Sonnet at effort xhigh, the Reviewer on Opus — his words of 08:5x), a project-level definition the harness ranks above a user's own; the parent project's side — its ignore exception and the same two files — is its own Principal's to commit, one author per repository · source: his word; the harness's subagents page (frontmatter `model`, `effort`) · undermines: no signed rule — a slice of the answered slice (the harness's settings ship with the tool); a seat definition carries the prompt every seat follows and can grant tools, so its review is critical tier: an independent session's Reviewer, never one same-session docs pass

## Done when

The Owner has ruled the candidate; a seat commit without a registered open session is refused by the gate; the board
shows the open sessions with their scope; FM-023's plan marks steps by this id; and one week's commits trace, each, to a
row.

## Acts

**2026-09-27** · done — work-tracker/evidence/reviews/review-fm-029-0-18-3-fourth-pass.md · Who verifies 0.18.3 — a cold Reviewer session you start, this session's own sub-agent, or nobody until FM-024's slice 2 refuses a same-session verdict? · holgo99
## Asks

**2026-09-24** · Who verifies 0.18.3 — a cold Reviewer session you start, this session's own sub-agent, or nobody until FM-024's slice 2 refuses a same-session verdict?
**answered** — accepted - a cold Reviewer session you start reviews 0.18.3 · holgo99
**relation** — accepted the proposal
**signed** — 64f843e · G

**2026-09-28 — the ask of this pass (PortDive ledger row 56 first, 06:50:17):** the Owner's question, relayed 06:48:37 with the Auditor's counsel (normalised): *"How can we integrate these scripts for Claude and Codex settings and the rule from project memory into the shoalmark repo, so that this ships together and users can use it too when they pin a version of shoalmark?"* The paste, word for word (sha256 of the filed text `88db73aff8fed3fb87fe469ef7fb38e08090e2b1e27090d4eb2ac49d21401c20`):

> To: 8e509911 principal (shoalmark-principal-4)
> From the Owner, with the Auditor's counsel (2026-09-28 ≈06:55 CEST). His question: "How can we integrate these scripts for Claude and Codex settings and the rule from project memory into the shoalmark repo so that this ships together and users can use it too when they pin a version of shoalmark?" (normalised)
> Proposal — a slice on FM-024 (the freeze holds at 21; FM-024's problem is the one that bit today: two sessions of one seat), citing FM-031:
> 1. `shoalmark.py --statusline`: reads Claude Code's JSON on stdin, prints `<session> <seat> (<worktree>) · <branch>` from the tool's own [seats] and the sessions strip's trailer reader (newest `Session: <id>` or `<id>/<seat>` commit; a sub-agent's `<id>/<seat>-<n>` excluded; before the first commit the worktree badge marked `?`), cached under .git/. No board, no tracker load (FM-040). Prototype on his machine: ~/.claude/statusline.sh.
> 2. `--install-statusline` beside `--install-hook`: merges a statusLine entry into the repo's .claude/settings.json pointing at the pinned copy (merge, never replace, print only what it adds); the Codex [tui] lines (status_line = ["thread-title","git-branch","model-with-reasoning","context-remaining"], terminal_title = ["thread-title","git-branch"]) into a project .codex/config.toml if Codex 0.157 reads one there, else printed. Codex shows id (while the thread is untitled) and branch, never the seat — say so.
> 3. AGENTS.md, as his rule: a message a person carries between sessions names its target as the tool prints it, `To: <session> <seat> (<worktree>)`; a seat's report opens with its own; `--whoami` prints it (seat.session or CODEX_THREAD_ID, [seats], the worktree folder).
> To settle in the build: PortDive ignores .claude/ except output styles (an exception there, or a --user install form); which cwd a project statusLine command runs in (test from a subfolder and a worktree).
> Process: an ask on FM-024, rowed first — options: all three · the status line only · the rule only; no default. Code tier, full loop. The Auditor seals its verification plan before the build.

The paste's own stamp, *≈06:55 CEST*, is its writer's estimate, kept as written; it reached this session at 06:48:37 (the transcript's stamp), the time this record and the ledger's row 56 use.

The Principal's counsel, disclosed as such: the first option — all three, as a slice on this tracker (its problem is the one that bit on 2026-09-28: two sessions of one seat are one author); to settle in the build, as the Auditor names them: PortDive ignores `.claude/` except output styles, and the cwd a project statusLine command runs in. Code tier, the full loop; the Auditor seals its verification plan before the build. Nothing is built before his answer and the pass that judges the slice.

## Ship log

| Date | Event |
|---|---|
| 2026-09-23 | R6: a parent is read from *convened by* only in the session-id form; the registry names the Principal session `8e509911` in every row. R7: *What is true now* says what shipped — 15 checks, *on trunk*, the landed-branch rule, the sessions the commits carry. |
| 2026-09-23 | R5: the worked examples carry no client's or consumer's state — a client repository's name, the consumer's tracker and review ids and two of its commit hashes are generic now; the numbers stay. |
| 2026-09-23 | R4: `--session-check` — the session rule alone, no tracker read — runs from the pre-commit hook on every commit; a seat's code-only commit without a session is refused. One check. |
| 2026-09-23 | R2: the reviewed range is the branch's own commits (`<tip> ^<trunk> --no-merges`, less verdicts; a landed tip against the trunk before its merge); a tip on the trunk reads *on trunk — not a branch verdict*; label `reviews.trunk`. The Reviewer's planted sibling reads *independent*, before and after the branch lands. One check. |
| 2026-09-23 | R3: a sub-agent's id derives from its parent's — `--session open` refuses otherwise; row `8d6537be` closed, this build re-opened as `8e509911/implementer-1`. R1: a seat's commit that removes the registry, drops a row or re-opens an ended one is refused, against its parent's registry; a session's own closing commit passes. Two checks. |
| 2026-09-23 | **Slice 1 built** for 0.17.6: S1+S2, S3, S4, S5, S6, S7 each in its own commit, with its checks (eleven: ten fail on 0.17.5, one is a control); the release's own registry holds its first row, and its commits carry `Session: 8d6537be`. |
| 2026-09-23 | **Slice 1 fixed for 0.17.6 on the Owner's word** (*a prerequisite; before tomorrow*): S1–S8 above — the trailer, the registry, the gate's three refusals, the independence *report* (a count, not yet a refusal), the board's strip, eight checks. Design choices recorded, none asked; the Owner may strike. FM-023 waits until it is ripe — agreed. The Reviewer's attack on the filing is folded into its attack on the build, a departure from the research chain, said here. |
| 2026-09-23 | **Worked examples added on the Owner's ask** — the worktree setup, the commit with its trailer, the registry with a collision and a sub-agent row, a verdict under the independence rule, the board's and the gate's lines, the plan's mark. Illustrative; nothing built. |
| 2026-09-23 | Filed on the Owner's question, written to be attacked; held against FM-005 (the person asked mid-flight), FM-007 (a signature proves the key, not the hand), FM-008 (an ask reaches the Owner only through the gate); FM-023 (the plan's `@session`, on its own branch) is the consumer of this id. Not built this week — the path's line 2. |
| 2026-09-24 | Asked, kind action: who verifies 0.18.3 — slice 2 (a same-session verdict refused) is unbuilt and 55 of this week's 57 verdicts are one session's own sub-agents (the Auditor seat's AU-17); the parent project's ledger row came first. |
| 2026-09-24 | Correcting the row above (the Reviewer's R6): the 55 of 57 are *same session* as `--check` counts them — each verdict by its own branch's session, 54 of them this session's sub-agents and one another's — not one session's. |
| 2026-09-24 | The row of 20:24 above was edited in place before the branch merged (the pass Reviewer's R10); from here, a correction is an appended row. |
| 2026-09-28 | **Folded:** the Auditor's sessions-strip line through the Owner (09:01:54; sha256 `a375a843…`) — group the sub-sessions under their parent, each sub's worktree on expand — a line of the answered slice, under *Raised*; nothing built. |
| 2026-09-30 | **Graded, not built:** the Auditor's change brief through the Owner (06:11:21; sha256 `8e8f77ce…`) — the strip grouped by parent (accepted), model and effort from the harness's logs as trailers (the principle accepted; its `cwd` match rejected, P1 on a measured fact: a transcript's `cwd` is the session's launch directory on every turn, sub-agents included; a match by the harness's ids proposed), the code loop instead of one pass. Postponed on the Owner's word of 06:38:10; the build comes after the task he named. |
| 2026-09-30 | **The seat definitions ship** (the Owner's word, 09:12:44): `.claude/agents/implementer.md` (Sonnet, xhigh) and `reviewer.md` (Opus) added; nothing else changed. Critical tier — an independent session's review before the merge. |
| 2026-09-30 | **The seat Apps' run sheet** (GtM, `8e509911/gtm-2`), `evidence/FM-024/seat-apps-owner-run-sheet-2026-10-01.md`: the seven slugs `shoalmark-<seat>` checked free by read-only GETs (14:51 CEST; the display name stays `shoalmark <seat>`, the slug's source); seven one-line descriptions, playful as the Owner asked, through the claim screen's six gates by hand — all seven pass, both controls die; the Owner's dry run for 2026-10-01 before 11:00, with his pre-decision (a bot id that does not resolve: install on `shoalmark`, that repository only, permissions none). Nothing created on the forge. Records +121 −0, product +0 −0. |
| 2026-09-30 | Correcting the row above (the Reviewer's RV-2091): at `b07e610` the gtm line, *I put every public line through six gates …*, failed G2 on *every*. No record shows every public line going through this seat, and FM-042's pages went through a Reviewer. So six of seven lines passed, not all seven. The line now reads *I put public lines through six gates and hand the Owner the survivors. Most lines don't make it. I pick none.* (109) and passes. |
| 2026-09-30 | Correcting the rows above on the Owner's rulings on seats (15:29, relayed): the seven Apps are principal, implementer, reviewer, research, go-to-market, designer and auditor. `shoalmark-research` replaces `shoalmark-datascientist`, since the Data Scientist folds into research. `shoalmark-go-to-market` replaces `shoalmark-gtm`, and the seat keeps `gtm@seat`. Both new slugs are free by the three GETs, 15:32:44–15:32:47 CEST. |
