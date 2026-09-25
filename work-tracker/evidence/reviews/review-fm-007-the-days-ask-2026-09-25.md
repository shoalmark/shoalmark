# Review — FM-007's ask, at 3e0893b (2026-09-25 07:16 CEST, Reviewer, session `8e509911/reviewer-4`)

**Scope.** `fm/007-the-day-of-the-key-asked-on-the-board`: two commits by the Principal seat (`8e509911`) on `main`
`a77798b`. Docs tier, one pass.

## Checked, and true

- **`f0a0ad3` is `--clear-ask FM-007 wait`'s own output.** I replayed it on a scratch clone of `a77798b` and ran the
  generator. The tracker and `INDEX.md` came out byte for byte as the commit has them (`cccf4dc`, `335f194`).
  - The 09-22 exchange moved under `## Asks`, with *relation — accepted the proposal*.
  - The eight ask and answer lines left the front matter, and `next: wait` replaced them.
- **`3e0893b` sets the ask, and nothing else in the tracker.** It changes `next: owner`, adds the five ask lines, and
  adds one ship-log row at the top of the log (FM-007's log is newest first). Its INDEX row is the generator's own.
- **The ask (the P2 exception).** Every rule holds.
  - It is 179 characters (≤ 300), with one `?`, at its end.
  - It has 3 options (36, 10 and 55 characters). They are distinct, and none opens with yes or no.
  - The proposal is option 1, verbatim.
  - `action` is the right kind: the schema's *hands only the Owner has*.
  - Its premise holds here. The signing key is `ssh-ed25519`, a software key. `ssh-add -l` in this sub-agent's shell
    lists it (`SHA256:uNcU…`), so it is in the shared agent.
- **The queue.** `--owner` lists FM-007 alone: *action · asked 0 day(s) ago*. At `a77798b` it printed *NOTHING NEEDS
  THE OWNER*.
- **The gates.** `--check` exits 0, and says *INDEX.md is up to date*, so the generator is clean. `--session-check`
  exits 0. Both suites are green (355 and 148). `merge-tree` with `origin/main` gives `a5687b1`, a clean
  fast-forward.
- **The ship-log row.** Its facts are true:
  - His answer stands in the record and the act is open.
  - The slot held an answered exchange, which `--owner` never shows (`owner_queue` requires no answer).
  - The parent project's ledger commit `9c9b5bbc` (07:03:02) came before `3e0893b` (07:05:45).
  - *07:00:34* is the parent project's record of his words (reported).

## Findings — P3, the Principal's to fix forward or not

- **R1. The row does not say the exchange was cleared, or why that was the only way.**
  - `--clear-ask` is defined as *the seat has acted on the answer*. At `f0a0ad3`, `--answered` printed *FM-007 —
    acted on in `f0a0ad3`*, and the `## Asks` record reads like any acted-on one.
  - The tip hides this only because a new ask holds the slot.
  - Clearing was the only way, and I verified each step:
    - A tracker has one ask slot.
    - An answered ask never reaches `--owner`.
    - The gate refuses an answer removed without its record.
    - The filing freeze (18 open, ≥ 8) bars a new tracker that is not a bug.
  - The row says *the ask slot held that exchange* and leaves the rest implied. One clause would make it explicit:
    moved by `--clear-ask` only to free the slot, and nothing was acted on.
- **R2. The row credits the slot with more than it did.** Its *so … FM-007 sat under* backlog gives the slot a part
  in that placement. `board()` places FM-007 by its status (Proposed, triaged), and it is still under *backlog* on
  the tip. The slot caused only *nothing to answer*.

**Merge note.** PR 65 (`d79949f`) also adds a top row to FM-007's ship log, so those two conflict. The resolution is
the order: this 09-25 row goes above its 09-24 correction. The merge with PR 64 is clean.

## Verdict — READY WITH FINDINGS, 93%

R1 and R2 are P3. The ask itself is clean.

**Independence.** Same session: I am a sub-agent of `8e509911`, which made both commits.
