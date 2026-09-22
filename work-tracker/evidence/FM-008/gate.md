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
| 5 | With `seats = [...]` in `shoalmark.toml`, an ask whose `next: owner` line was committed by an author outside the list is refused, naming the seat. `signed` entries additionally require a verifying commit whose `%GS` principal is that seat's identity — the same code path the answerers check uses. Absent the key, nothing changes. On Subversion the author is the server's (`svn blame --xml`) and a `signed` entry is refused as meaningless | `seat_problem` via `lint` | same | let `seat_problem` return nothing when the author is unknown to `seats` |
| 6 | A commit that drops a tracker's `answer:` lines without the exchange in the body under `## Asks` is refused; `--clear-ask <id> <next>` does it correctly | `lint(committing=True)` + `clear_ask` | same | make the record test accept a missing `## Asks` heading |
| 7 | More than 5 asks in the queue and the board's first line and `--owner` append *"you are the bottleneck — N asks, M trackers held up"* | `owner_digest` + the page | same | raise `BOTTLENECK` above the fixture's count |
| 8 | `--answer` refuses an existing `answer/<id>` branch whose tip does not carry the ask (reported by the 0.16.0 Implementer) | `answer_cmd` | same | drop the tip test |
| 9 | `--answer` on a tracker whose `ask:` line is not in the front matter prints a refusal instead of raising (same report) | `answer_cmd` | same | restore the bare `next(...)` |

## Cost — pre-registered, measured both ways

`lint` with `git log -S` per answered tracker cost the repository this tool was cut from **7.5 s** in its pre-commit
hook. Rules 5 and 6 add `git log -S` and `git show HEAD:<file>` calls. **Claim:** they run only for trackers whose
file is in `git diff --cached --name-only` during a pre-commit run (`committing=True`), and once for all in `--check`;
with `seats` absent, rule 5 makes no call at all. `time python3 shoalmark.py --check` is recorded below, before and
after, on this repository.

## Outcome

*Filled in after the build — nothing here is written in advance.*
