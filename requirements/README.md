# requirements/ — one ground truth for developer and tester

A requirements folder holds what the system shall do, in the repository, so that the developer and the tester work from
the same text. A requirement is tested as a contract — by what it says, not by reading the implementation — because
test plans drift and a plan written from the code only confirms the code.

## The line form

One line per requirement, in a Markdown table with four columns:

| Column   | What it holds |
|----------|---------------|
| `id`     | Never reused, never renumbered. `REQ-<area>-<nnn>` or `REQ-<nnn>`, fixed once chosen. |
| `shall`  | One sentence, the system as subject, one obligation. |
| `source` | Who or what asks for it: a person's role, a document, a clause. |
| `accept` | The acceptance criterion: what a test observes to call it met. |

| id | shall | source | accept |
|---|---|---|---|
| REQ-WDG-001 | The watchdog shall reset the unit after a 500 ms stall. | a lead | Stall forced: reset in 600 ms |
| REQ-LOG-002 | The system shall log a reset's cause, once. | `<std> <ed> §<n>` | Reset forced: one line names it |

## How the record cites it

A tracker names what it satisfies in one line of its body: `Satisfies: REQ-001, REQ-004`. The gate refuses a front-matter
key it does not know; a `satisfies:` key is Stage 1's ask. A test names the id in its name or docstring. A requirement replaces a restated behaviour: the
tracker cites the id instead of repeating the sentence, never a third copy.

## Who changes one

A requirement changes only by the Owner's signed decision — an answer through the board — never by a seat's edit.
The id stays, the line changes, git holds the history.

## Regulatory requirements

Cite the clause — standard, edition, clause number — and write the company's own *shall* derived from it.
*Not applicable* is a signed answer with its reason. Never copy a standard's text into the repository. Never write that
the project complies: a requirement met is a test passed, nothing more.

## Not here yet

Later, an ask: Stage 1 — coverage and citation checks, stale-marking on a changed requirement, `--trace REQ-<id>`, a
traceability matrix per release from git. Stage 2 — a spec-only tester seat.
