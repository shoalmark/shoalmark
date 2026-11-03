---
id: FM-060
status: Shipped
considered: FM-050, FM-058, FM-030, FM-007, FM-004
tags: bug
next: wait
hook: "--answer's refusal record is committed unsigned under the Owner's name, and R14 then refuses every branch that carries it, the Owner's later signed answer included"
---

# FM-060 — the answer's refusal record is committed unsigned under the Owner's name, and R14 refuses every branch that carries it

## What is true now

**2026-11-03 — Shipped with v0.20.2, for R4's removal; item 1's test leaves as
[FM-105](FM-105-no-test-holds-that-a-refused-signature-then-a-signed-answer.md), and item 2 waits in
[FM-106](FM-106-eight-done-when-items-of-trackers-closed-at-v0-20-2-have-no.md).** R4 is built (`732d9fb`) and merged
with S1 into `release/v0.20.2-rebuilt` as `5be9df2` (#249): a refusal restores the file and records nothing, so no
refusal record is committed. The row this tracker names, a refusal at signing and then the Owner's signed answer on the
same branch, is not in the tests: on the Owner's word of 2 November it is FM-105's, for v0.20.3. Item 2, the rule for
the branches before R4, has no evidence in the record. It is evidence owed at v0.20.2's close.

**Filed 2026-10-16, defect 11; nothing is built.** R4 (FM-050) removes the refusal record, and with it this defect.

**Facts,** read at main `5f792d6`.
- **The record.** A command refused on `answer/<id>` leaves one line under `## Acts`, committed with `--no-gpg-sign`
  under whoever runs the command, and pushed (`record_refusal`, `shoalmark.py:3116–3147`, inside `owner_change`,
  `:3036`, which `--answer`, `--done`, `--due` and `--revoke` run). The command's next run on that tracker commits on top
  of it.
- **R14.** `owner_signature_problems` (`:5681`) refuses every commit in a branch's own history that a signed Owner
  identity authored and that carries no verified signature of the Owner's.
- **Together:** the record is the Owner's commit without a signature, so R14 refuses every branch that carries it, and
  the Owner's next signed answer is made on top of it.
- **The case.** FM-004's answer, 16 October: `0f61c45` on `answer/fm-004` is the record of the first, refused attempt
  (FM-058), and the signed answer `92ecdce` sits on it. Joined into FM-004's branch, `--check` refused the join:
  *carries no verified signature of the Owner's*. The join, `385bfda`, is kept on `fm/004-join-refused-385bfda`.
- **Until R4 lands:** the Owner re-signs the answer onto the branch without the record, `git cherry-pick -S -x <the
  answer>`, as FM-004's answer goes onto its branch.

**Fix: R4.** FM-050's design (on `fm/050-ask-id-design`, in review), §3c: `owner_change` loses `record_refusal`; a
refusal restores the file and records nothing under `## Acts`. Its §8 makes that R4's first commit: no cut, no push, no
switch, no refusal record.

**The test that shows it.** FM-050's class test, its commands rows (§6): after each `--answer`, no `answer/<id>` ref,
`origin`'s refs unchanged, the branch unchanged, and on a refusal the file restored. One row named here for it: an
`--answer` refused at signing, then the Owner's signed answer on the same branch. The branch holds no commit of the
Owner's without a signature, and `--check` passes R14.

## Done when

- [ ] R4 is built with that row, and the row passes.
  — R4 is built (`732d9fb`); the row is [FM-105](FM-105-no-test-holds-that-a-refused-signature-then-a-signed-answer.md)
- [ ] Until then, a branch that goes to CI carries no refusal record; the answer is re-signed onto it without the record.
  — evidence owed: [FM-106](FM-106-eight-done-when-items-of-trackers-closed-at-v0-20-2-have-no.md)

## Ship log

| Date | Event |
|---|---|
| 2026-10-16 | Filed, defect 11 (the Auditor's finding, relayed by the Owner). R4 removes the record. Nothing is built. |
| 2026-11-03 | **Shipped with v0.20.2:** R4 built in `732d9fb`, merged with S1 as `5be9df2` (#249). Item 1's row is filed as FM-105; item 2 waits in FM-106. Records only. |
