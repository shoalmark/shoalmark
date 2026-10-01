# Requirements — one text for developer and tester

## Why

The developer and the tester work from one ground truth: the requirements, in the repository, next to the code. The
tester tests the requirement as a contract — what it says, not what the implementation happens to do — because a test
plan written from the code only confirms the code, and a plan kept apart from the repository drifts.

## One line, one requirement

| id | shall | source | accept |
|---|---|---|---|
| REQ-PWR-007 | The unit shall enter sleep within 2 s of the last input. | a product lead | Input stops: asleep in < 2 s |

The line form — the four columns and what each holds — is written once, in
[`requirements/README.md`](https://github.com/shoalmark/shoalmark/blob/main/requirements/README.md).
This page does not restate it.

## The owner's part

A requirement changes only by the Owner's signed answer, through the board — never by a seat's edit. The id stays, the
line changes, git holds the history. A seat that finds a line wrong raises an ask. *Not applicable* is a signed answer
with its reason, never a seat's.

## A regulatory requirement

Cite the clause — standard, edition, clause number — and write the company's own *shall*, derived from it. Never copy a
standard's text into the repository. Never write that the project complies: a requirement met is a test passed, nothing
more.

## How the record cites it

A work item names what it satisfies in one line of its body: `Satisfies: REQ-PWR-007`. A test names the id in its name
or its docstring. The work item cites the id instead of restating the behaviour, so the requirement never has a third
copy.

## Not built yet

Each is an ask to the owner, and starts only on their go.

- **Stage 1**, after the trial and one more prospect: coverage and citation checks; stale-marking of what cites a
  requirement once it changes; `--trace REQ-<id>`; a traceability matrix per release, generated from git.
- **Stage 2:** a tester seat that reads the requirements and not the implementation.
