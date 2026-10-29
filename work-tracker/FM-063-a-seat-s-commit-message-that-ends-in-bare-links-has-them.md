---
id: FM-063
status: In Progress
considered: FM-024, FM-057, FM-040
tags: bug
next: build
triaged: 2026-10-29
tier: P2
hook: "a seat's commit message that ends in bare links has them rewritten by the trailer step"
---

# FM-063 — a seat's commit message that ends in bare links has them rewritten by the trailer step

## What is true now

**2026-10-29 — built in `ec5432a`:** the hook inserts missing seat trailers into the original bytes, using Git to read existing keys and locate the insertion; the base reproduction is red, the 34 regression controls and core suite are green on Python 3.15, and four mutants are red. Next: standard review, critical review and CI across its Git versions; the Planner removes the sentence-ending rule from the common files after merge.

**2026-10-29 — judged In Progress, P2, critical, for v0.20.2, before the first build commit.** It is built on the
release branch's head with main joined, on the Owner's word of 29 October that it goes to a Builder on Codex. The step
runs in the prepare-commit-msg hook, so its review is critical.

**Filed 2026-10-19; nothing is built.** The Auditor reproduced it with git 2.50.1. It goes to v0.20.2, the Planner's
call, which the Auditor's relay of 19 October left to the Planner. Its row is in FM-023's v0.20.2 table, under *What is
true now*.

- **What happens:** in a worktree with `seat.session`, the prepare-commit-msg hook's trailer step (`session_trailer`,
  `shoalmark.py` line 7825 at `6bfec9f`) adds the seat's trailers with `git interpret-trailers --in-place`.
  - Where the message ends in a paragraph whose lines read as `token: value`, git takes that paragraph as the
    message's trailer block. A `Sources:` line over bare links is one such paragraph.
  - Git adds the seat's trailers to that paragraph, and writes each of its lines back as a trailer, so `https://…`
    becomes `https: //…`.
  - `02fa59a` shows it.
- **What it does not touch:**
  - a commit without `seat.session`, such as a person's own: the step returns before git runs;
  - a message that ends in a trailer block, such as a `Co-Authored-By:` line: the seat's trailers join it, as intended.
- **History stays as it is.** No commit is rewritten.
- **Until it ships,** a seat ends its message with a sentence, never with bare links.
- **Why v0.20.2:** the rule above holds meanwhile, the damage is limited to the text of seat commits, and v0.20.1's
  critical path is full.
- **Why it is filed apart:** the trailer step came with FM-024's first slice. It is filed on its own so that FM-024's
  v0.20.1 work does not grow.
- **Size:** S. The step runs in the prepare-commit-msg hook, so it is reviewed as the hooks are.

## Why

A commit message is the record a seat leaves, and the Owner reads it back; a link with a space in it no longer opens.
The tool adds its trailers, and must change nothing a seat wrote.

## Done when

- The trailer step adds the seat's trailers and changes no other byte of the message, including a message that ends
  in bare links, with or without a `Sources:` line over them.
- `%(trailers)` still reads the seat's `Session:`, `Worktree:`, `Model:` and `Effort:` from the commit, so the gate
  finds them as now.
- A message that ends in a trailer block still gets the seat's trailers in that block, and a trailer it carries
  already is left alone, as now.
- A test with `02fa59a`'s shape fails on today's step and passes on the fix, on the oldest and the newest git that CI
  runs.
- The rule that a seat ends its message with a sentence leaves the common files.

## Ship log

| Date | Event |
|---|---|
| 2026-10-29 | Judged In Progress, P2, critical, for v0.20.2, before the first build commit. Records only. |
| 2026-10-19 | Filed from the Auditor's reproduction with git 2.50.1, as a bug; v0.20.2, the Planner's call; nothing is built. |
| 2026-10-29 | Built in `ec5432a`: removed the in-place message rewrite; retained byte-preserving insertion and regression controls. Review and the Planner's post-merge rule deletion remain. |
