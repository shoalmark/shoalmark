---
id: FM-105
status: Proposed
considered: FM-060, FM-050, FM-015, FM-017
tags: bug
hook: "R4 removed the answer's refusal record, but no test runs the case FM-060 names: an answer refused at signing, then the Owner's signed answer on the same branch, with no unsigned Owner commit left and --check passing R14."
---

# FM-105 — no test holds that a refused signature, then a signed answer on the same branch, leaves no unsigned Owner commit

## What is true now

**Filed 2026-11-03 for v0.20.3; nothing is built.** It is FM-060's first *Done when* item, which leaves FM-060 as a
tracker of its own when FM-060 closes at v0.20.2, on the Owner's word of 2 November.
- **What is built:** R4 (FM-050's S1, `732d9fb`, merged with S1 as #249). `owner_change` no longer cuts a branch,
  pushes or records a refusal, and a refused write is restored.
- **What no test runs:** the one row FM-060 names. Nearby tests check a missing key, a wrong signer and a hook's
  rollback, and `test_proof.py` checks signed answers against the gate, each on its own. None runs the sequence.
- **This is a missing test, not a known defect.** Nothing shows the refusal record coming back.

## Why

FM-060's case broke every branch that carried the record. A row that runs it end to end keeps R4's removal from
coming back unseen.

## Done when

- [ ] One test runs the sequence on one branch: an `--answer` refused at signing; then the Owner's signed answer; then
  `--check`. The branch holds no commit of the Owner's without a signature, and `--check` passes R14.
- [ ] A mutant that records the refusal again fails that test.

## Ship log

| Date | Event |
|---|---|
| 2026-11-03 | Filed for v0.20.3 from FM-060's first item, on the Owner's word of 2 November. Records only. |
