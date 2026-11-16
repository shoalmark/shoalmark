---
id: FM-173
status: In Progress
considered: FM-024, FM-034, FM-037, FM-169
tags: bug
epic: FM-139
next: build
triaged: 2026-11-16
tier: P1
hook: "In a clone with no signers file set up, --check reads a signed answer it cannot verify as no answer at all: a ledger-integrity violation, exit 4, and --answer undoes the Owner's new answer. The ledger is sound; the clone is not set up. FM-034 made such a signature the checkout's own finding for the other signed checks, and the answer's reader was left out. The proposal, put to the Owner as FM-173-Q1: the checkout's finding for every reader of a signed answer, with a class test."
---

# FM-173 — a signed answer this clone cannot verify reads as a missing answer, a ledger violation, not as the checkout's own finding

Seat: the Planner (a1730572) · filed 2026-11-16, on the coordinator's word of that day.

## What is true now

**2026-11-16 — FM-173-Q1 answered "yes, as proposed", with the Owner's signature; judged before its first build commit,
keep P1, In Progress.** The fix is in v0.20.3, a chapter of
[FM-139](FM-139-v0-20-3-s-rows-sit-in-fm-023-fm-006-and-fm-053-so-no-one.md). It reads the same answer path that
[FM-169](FM-169-the-owner-s-personal-address-stands-in-the-public.md)'s lane changes, so it is built after that lane
lands.

**Filed 2026-11-16, Proposed, with FM-173-Q1 put; nothing is built.** The Owner met it on the Board, in another
repository of the organisation that vendors this tool at v0.20.2, and the coordinator reproduced it there: with the
clone's `gpg.ssh.allowedSignersFile` unset, `--check` exits 4 on a sound ledger; with it set, the same clone checks clean.

- **What the person sees:** `<id>: no commit answers <id>-Q<n>: an answer to an ask with an id is the Owner's ordinary
  commit that carries Answers: …, signed …`, as a ledger-integrity violation, exit 4. `--answer`, whose gate runs the
  same check, then undoes the answer it has just written. The line sends the Owner to mend a tracker that is sound.
- **Why:** `answer_commits` keeps a candidate only where `verified_as` holds
  ([`shoalmark.py` L2371](https://github.com/shoalmark/shoalmark/blob/599bcd4d92c6c980c1a4fc21c5f2505f259d5871/shoalmark.py#L2371)). `verified_as` is false both where the signature is wrong and where this clone has
  no signers file to check it against ([L6841–L6850](https://github.com/shoalmark/shoalmark/blob/599bcd4d92c6c980c1a4fc21c5f2505f259d5871/shoalmark.py#L6841-L6850), [`signers_args` L6966](https://github.com/shoalmark/shoalmark/blob/599bcd4d92c6c980c1a4fc21c5f2505f259d5871/shoalmark.py#L6966)). The two
  cases read alike, and the answer counts as missing.
- **What already holds elsewhere:** [FM-034](FM-034-a-fresh-clone-s-check-says-the-index-is-stale-the-header.md) made
  a signed commit this clone cannot verify the checkout's own finding, said on stderr and kept out of INDEX.md, by the
  words in `CHECKOUT_MARKS` ([L7008–L7014](https://github.com/shoalmark/shoalmark/blob/599bcd4d92c6c980c1a4fc21c5f2505f259d5871/shoalmark.py#L7008-L7014)). The guard over the Owner's two sections reads such a
  commit so. The answer's reader does not.
- **Where it meets [FM-169](FM-169-the-owner-s-personal-address-stands-in-the-public.md):** its drafted lane changes
  the same path, since a filed answer is checked against the signers file of the state it was filed in. Whether that
  alone clears this case is not shown. This tracker's test holds the class either way.

## Why

The Owner's answer is the record's deciding word. A check that cannot tell a clone that is not set up from an answer
that is not there refuses the Owner's word, and undoes it, for a reason that is the clone's.

## Decisions, for the Owner

All three are put as FM-173-Q1.

1. **One reading for every reader of a signed answer:** the answer's own reader, the records under `## Asks`, the
   relation and the Board. Where the signature cannot be checked here (no signers file, or one this clone cannot
   trust), the answer reads as the checkout's own finding, in `CHECKOUT_MARKS`' words, with the line that says how to
   set the clone up; never as a missing answer and never as a ledger-integrity violation.
2. **`--answer`** keeps the answer it wrote when the only finding is the checkout's own, and says so.
3. **A class test:** for every reader of a signed answer, a clone with no signers file gives the checkout's finding
   and exit status, and the same clone set up gives a clean check; with its mutant. The review is critical: it touches
   signing.

## Done when

Each item names its commit or pull request when it lands.

- [ ] **The Owner has answered FM-173-Q1.**
- [ ] **Every reader of a signed answer** gives the checkout's own finding where the signature cannot be checked here,
  with the class test and its mutant.
- [ ] **`--answer`** keeps its answer when the only finding is the checkout's own, with its test.
- [ ] **The critical review is READY.**

## Asks

**FM-173-Q1** · 2026-11-16 · Do you take FM-173's fix into v0.20.3: a signed answer whose signature this clone cannot check reads as the checkout's own finding, never as a missing answer, and a class test holds it for every reader of a signed answer?
**answered** — accepted - yes, as proposed · holgo99
**relation** — accepted the proposal
**signed** — 1a730bf · G

## Ship log

| Date | Event |
|---|---|
| 2026-11-16 | FM-173-Q1 answered, yes, as proposed; judged before its first build commit, keep P1, In Progress; a chapter of FM-139. Records only. |
| 2026-11-16 | Filed, Proposed, with FM-173-Q1 put: a signed answer this clone cannot verify reads as the checkout's own finding, never as a missing answer, with a class test. Records only. |
