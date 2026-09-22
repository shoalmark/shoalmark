# FM-008 — the gate that holds the ask rules: pre-registration

Written **before any code**, 2026-09-22, on `fm/008-an-ask-reaches-the-owner-only-through-the-gate`.

Each row below is a claim about behaviour that does not exist yet. For each: the rule, where it is enforced, the check
that proves it, and **the mutation** — the one edit to `shoalmark.py` that must make that check fail. A rule whose
check passes both with and without its code proves nothing, so every mutation is run and its failing assertion text is
recorded under *Outcome*. Nothing is recorded in advance.

## The three layers

All seven rules are one function, `lint`, which already runs in three places: the pre-commit hook (`--print-written`),
`--check` (CI), and every board build. The third layer is added here explicitly: **`owner_queue` lists only asks that
pass the ask rules.** A tracker that fails them is listed apart — the board shows *"N asks sent back — not for you"*
with the reason, `--owner` and `--standup` the same. The Owner never sees a malformed question as a question.

## The claims

| # | Claim | Where | Check | Mutation |
|---|---|---|---|---|
| 1 | `next: owner` without `ask:`, `ask-kind:`, `ask-since:` or `ask-proposal:` is refused, naming the id and the missing key | `ask_problems` via `lint` | `test_shoalmark.py`, FM-008 block | drop the missing-key loop from `ask_problems` |
| 2 | `ask:` carries exactly one `?`, at the end, ≤ 300 characters; `ask-options:` ≤ 5 options, ≤ 120 characters each, no duplicates | `ask_problems` via `lint` | same | drop the one-question test |
| 3 | An `ask:` whose normalised text (lower case, whitespace collapsed, trailing punctuation stripped) equals another OPEN tracker's is refused, naming the other id. Exact match only | `ask_problems` via `lint` | same | drop the duplicate test |
| 4 | An `ask:` with `next: review` is a draft: no proposal needed, and it never enters the Owner's queue | `owner_queue` | same | let `owner_queue` take `next in ("owner","review")` |
| 5 | **Redesigned mid-build — see below.** With `[seats]` in `shoalmark.toml`, the author of a change must be a seat holding the right for every transition it makes; the refusal names the seat, the right and the id. `signed` entries additionally require a verifying commit whose `%GS` principal is that seat's identity — the same verifier the answerers check uses. Absent `[seats]`, nothing changes. On Subversion the author is the server's (`svn blame --xml`) and a `signed` entry is refused as meaningless | `seat_problems` (the `ask` right, on the line) and `rights_problems` (`answer` · `close` · `triage`, on the change), via `lint` | same | let each return nothing where the seat does not hold the right |
| 6 | A commit that drops a tracker's `answer:` lines without the exchange in the body under `## Asks` is refused; `--clear-ask <id> <next>` does it correctly | `lint(committing=True)` + `clear_ask` | same | make the record test accept a missing `## Asks` heading |
| 7 | More than 5 asks in the queue and the board's first line and `--owner` append *"you are the bottleneck — N asks, M trackers held up"* | `owner_digest` + the page | same | raise `BOTTLENECK` above the fixture's count |
| 8 | `--answer` refuses an existing `answer/<id>` branch whose tip does not carry the ask (reported by the 0.16.0 Implementer) | `answer_cmd` | same | drop the tip test |
| 9 | `--answer` on a tracker whose `ask:` line is not in the front matter prints a refusal instead of raising (same report) | `answer_cmd` | same | restore the bare `next(...)` |

## The redesign of claim 5, 2026-09-22, mid-build

The pre-registration above was written against a flat `seats = ["principal@seat", …]` — a list of who may set
`next: owner`. The Owner replaced it **while the build was running**, after the list had been built and its checks
were green: `[seats]` names a seat and its identity, `[rights]` names what a seat of your own may change, and the
vocabulary is exactly four rights — `answer` · `ask` · `close` · `triage` — each one a front-matter transition the
gate can see in a diff. The claim is the same claim; what it is checked against grew from one transition to four.
The checks were converted, not re-registered, and every mutation below was run against the converted code. Two things
follow from the shape, and are recorded here because they were decided, not derived:

- **`ask` is judged on the line, the other three on the change.** The queue can drop an ask that reached the Owner
  another way only if it can ask *who set `next: owner`* — which is the line's history, not this commit's diff. The
  other three rights have no such reader, so they are judged on the change the commit makes.
- **A new tracker's `considered:` is not a triage verdict.** Filing is the one act every seat must be able to do, and
  the filing rule puts `considered:` on every new tracker. On a NEW file, `considered:` alone is not counted as
  `triage`; a `tier:`, a `rank:`, a `triaged:` or a `kind-of-problem:` on it is, and changing `considered:` later is.

## Cost — pre-registered, measured both ways

`lint` with `git log -S` per answered tracker cost the repository this tool was cut from **7.5 s** in its pre-commit
hook. Rules 5 and 6 add `git log -S` and `git show HEAD:<file>` calls. **Claim:** they run only for trackers whose
file is in `git diff --cached --name-only` during a pre-commit run (`committing=True`), and once for all in `--check`;
with `seats` absent, rule 5 makes no call at all. `time python3 shoalmark.py --check` is recorded below, before and
after, on this repository.

## Outcome

Every rule is in `lint`; the queue rules are also in `owner_queue`. **Nineteen mutations were run, one per claim (and
one per sub-rule of claim 2), each against the whole suite; every one was caught.** What a mutation costs is recorded
as the suite printed it — the check's own text, or, where the mutation restores a crash, the exception.

| Mutation | What it undid | What failed |
|---|---|---|
| M1 `missing = []` | claim 1 | *1 · an ask with no recommendation is refused, naming the id and the key that is missing…* and *1 · all three lines are named at once…* |
| M2 the one-`?` test → `if False` | claim 2 | *2 · one question: an ask with two of them, or with prose after the question mark, is refused…* |
| M3 the length test → `if False` | claim 2 | *2 · an ask longer than 300 characters is refused…* |
| M4 the five-choices test → `if False` | claim 2 | *2 · more than five choices is refused…* |
| M5 `long_ = []` | claim 2 | *2 · a choice longer than 120 characters is refused…* |
| M6 `twice = []` | claim 2 | *2 · the same choice offered twice is refused…* |
| M7 `same = []` | claim 3 | *3 · the same question filed twice is refused, naming the other tracker…* |
| M8 the queue takes `review` too | claim 4 | *a DRAFT — an `ask:` with `next: review` — needs no recommendation and never enters the Owner's queue…* |
| M9 the `ask`-right test → `if False` | claim 5 | *5 · the implementer holds no `ask` right…*, then `KeyError: None` at `SEATS[seat][1]` — the guard the mutation removed |
| M9b the test keeps only the no-right half | claim 5 | the same crash, earlier: the *not a seat* branch is load-bearing on both systems |
| M18 `svn blame` made unreadable | claim 5, Subversion | *S4 · under Subversion the seat is the server's account…* — and nothing else: the git path does not touch it |
| M10 the rights test on the change → `if False` | claim 5 | *5 · closing work is a right of its own…* |
| M11 the seat's signature test → `elif False` | claim 5 | *5 · a `signed` seat, and the ask signed by a throwaway key the signers file does not tie to it…* |
| M12 the `[rights]` vocabulary test → `if False` | claim 5 | *5 · there are four rights and no others — a fifth word in `[rights]` is refused, naming it* |
| M13 the svn `signed` refusal → `if False` | claim 5, Subversion | *S4 · `signed` under Subversion is refused as meaningless…* |
| M14 `if not t.get("asks_block")` → `if False` | claim 6 | *6 · an answer removed from the front matter and written nowhere else is refused…* |
| M15 `BOTTLENECK = 50` | claim 7 | *7 · past five asks the first line says whose problem the queue is…* |
| M16 the branch-tip test → `if False` | claim 8 | *8 · `--answer` refuses an `answer/<id>` that exists and does not carry the ask…* |
| M17 the bare `next(...)` restored | claim 9 | no assertion at all — the suite **dies**: `StopIteration` at `at = next(i for i, l in enumerate(lines) if l.startswith("ask:"))`. That crash is the defect; the check exists to turn it into a refusal |

Suites, both Pythons, at the end: `python3 test_shoalmark.py && python3 test_core.py` → **all green**;
`/usr/bin/python3` (3.9.6) → **all green**. `python3 shoalmark.py --check` → 0.

## Cost — measured

`time python3 shoalmark.py --check`, this repository, 8 trackers, best of three:

| | real |
|---|---|
| 0.16.0 (`git show 80424fa:shoalmark.py`, same corpus) | **0.37 s** |
| 0.17.0, no `[seats]` — what this repository runs | **0.36 s** |
| 0.17.0 with `[seats]` opted in, 2 open asks | **0.71 s** |

The claim holds: with `[seats]` absent the new rules make no version-control call and cost nothing measurable. Opted
in, the price is one `git log -S` per open ask plus one read of the change under review — here +0.35 s for two asks,
and in a pre-commit run only the trackers the commit stages are asked about at all. Nothing approaches the 7.5 s the
origin's hook paid. **Not measured:** a corpus the size of the origin's (500+ trackers) with `[seats]` set — the rule
is per *open ask*, not per tracker, so it should not scale with the corpus, but that is an argument, not a measurement.
