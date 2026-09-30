# FM-006 — fork-queue hardening, closure review

Date: 2026-09-30.
Reviewed: `d8782b4e8e150d53b7ee53e0b760edf9d4a5de21`, tree `bcc5ef444c8838ea42c4fdb2b961642eb858f24f`, branch `fm/006-fork-pull-requests-wait`.
Base: `297896b1c3215245111a0302e5dd9fd58189cb5d`, which is still `origin/main`. Prior verdict: `69a3c5e`
([review-fm-006-fork-queue-c2027d2.md](review-fm-006-fork-queue-c2027d2.md)), an ancestor of the tip.
Reviewer: `reviewer@seat`, unsigned. Session `e55ed3e1` (harness `e55ed3e1-08ce-4b91-a8b9-7061a9d5a6b8`), Opus 5.5. It is the
same seat as the prior pass. The fix commit is `01a0ec25`'s, so this session is independent of it; nothing spawned.
Worktree: `/private/tmp/shoalmark-review-fork-queue-c2027d2`.

**Tier: code, critical.** The one commit since the prior verdict touches `CHANGELOG.md`, `README.md`, `shoalmark.py`,
`test_core.py` and FM-006.

**Verdict: READY.** R1, R2 and R3 are closed, and there are no new findings. In `shoalmark.py` only one docstring line and
one help line changed, so queue behaviour is byte-for-byte the code the prior pass probed.

## Closure

- **R1 — closed.** All four places carry the text the prior verdict proposed:
  - `README.md:269` has the fork sentence before `` `merge` — ``.
  - The `--queue` help (`shoalmark.py:6045`) leads with `wait: from a fork, read it yourself (first)`. `--help` prints it,
    once the wrapped lines are joined.
  - The docstring (`shoalmark.py:1650`) now reads "same-repository pull requests' own and the pushed branches'".
  - `CHANGELOG.md:11` has the clause about a fork's base.
- **R2 — closed.** The two controls are byte-identical to the proposed fix text. I ran the tip's own FM-006 block in a
  focused harness, not the suite:
  - tip: 8 of 8 pass;
  - base `297896b`: 7 fail and the same-repository merge control passes;
  - the late-check mutant, rebuilt from the tip: passes the original six and fails both new ones.
- **R3 — closed as recorded.** FM-006's 2026-09-30 entry carries a follow-up line. It links the prior verdict and names
  all three hiding routes (name, containment, closed pull head), with the fix in a separate bug slice. The link resolves.

Witness not repeated: core 157 passed; syntax, hooks and `--check` green. Required PR CI is still due.

Hand-off, not a finding: FM-006's entry still ends *Critical review remains due.* The next move rewrites that sentence with
this verdict.

Quality read: clean. There are four wording edits and two tests, with no behaviour change. The rewritten docstring line
runs past its neighbours' width; that is cosmetic and not a finding.
