---
id: FM-034
status: Proposed
considered: FM-024, FM-019, FM-011
tags: bug
hook: "A fresh clone without the Owner's allowedSignersFile runs --check and reads two findings where there is one: the missing signers file, and `INDEX.md is STALE`. The index is not stale — the generated header carries the clone's own finding as a ledger-integrity line, so the committed INDEX and the one this clone would write differ by exactly that line."
---

# FM-034 — A fresh clone's `--check` says the INDEX is stale: the header carries the clone's own finding

## What is true now

**Filed 2026-09-24 at the Auditor seat's check 20 on v0.18.2, through the Owner; nothing is built.** Found in a fresh `gh` clone
of this repository without the Owner's `gpg.ssh.allowedSignersFile` configured. There `--check` names the missing signers file —
which is right, and what 0.18.0's R6 fixed — and then also says `work-tracker/INDEX.md is STALE — a tracker changed without
regenerating`. No tracker changed.

**Why.** The generator builds the INDEX header from `pin_problems() + lint(...)`: every ledger-integrity problem it finds
becomes a `> - …` line under *❌ N ledger-integrity violation(s)* in the generated body. A finding that belongs to the checkout —
a signers file this clone has not got, a pin this clone cannot read — lands in the body too, so the body this clone generates
differs from the committed one by that line, and the drift test (`drift_normalize(on_disk) != drift_normalize(body)`) reports
STALE. Two messages for one fact, and the second is false: a person reading it regenerates, commits the clone's finding into the
INDEX, and the next clone with the file configured sees STALE the other way.

**What is left.** A finding that is the checkout's, not the trackers', is reported on stderr and never written into the
generated body; the drift test is not widened to hide anything. The committed INDEX then reads the same in every clone.

## Why

The Owner's path, line 1: the sitting runs on a tagged release with no failed run. A fresh clone is how every consumer, the
Auditor's verification and a new seat meet the tool; a `--check` that says STALE on a clean clone is a failed run to each of them.

## Done when

- A fresh clone without `allowedSignersFile` runs `--check` and prints exactly one finding, the signers file, and no STALE.
- A clone with it configured prints none, and the committed INDEX is byte-identical to what either clone generates.
- A test makes such a clone and asserts both.

## Ship log

| Date | Event |
|---|---|
| 2026-09-24 | Filed, from the Auditor seat's check 20 as the Owner pasted it; `--related` held it against FM-024, FM-019 and FM-011 — none owns the INDEX header. |
