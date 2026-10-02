# v0.19.0 — the security ledger: the review at 593ebe1

Verdict: **READY**. No finding is open. RV-2321 onward are unused.
Reviewed: 593ebe1276f5f90d8bd2c1c46b2b38caae4e614e — `work-tracker/evidence/FM-006/security-ledger-v0.19.0.md` from its first commit, b5d5569, to 593ebe1, judged against FM-006's *The release bar*: *Evidence before the tag*, *The tests* and *Order*.
Reviewer: b3bdb000/reviewer-80 (claude-opus-5-5, xhigh), at the reviewer's bot address, unsigned, in worktree shoalmark-review-11, on 2026-10-02. Independence: this is the builds' session (b3bdb000), so not independent. Tier: critical.
Each head was read from the shared repository.

This change answers a private security report.

## The run the ledger reads

- **The run:** https://github.com/shoalmark/shoalmark/actions/runs/37009286728 (workflow_dispatch) on 26bcd97, green on all five jobs. The header's counts hold for each job, against the run's logs.
- **After it:** every commit after 26bcd97 is evidence or notes only — f526daa, b5d5569, 3bd36fc, 775d638 and 593ebe1.

## The checks

1. **b5d5569: the ledger, and CHANGELOG.md:45 narrowed.**
   - The scope is one commit and two files. Line 45 is narrowed word for word, and it is true at the head.
   - About 30 rows' CI columns were checked against the run's logs. Each ran, or was skipped, where and why the ledger says.
   - Controls re-run, each as recorded: T51's six cases, T7's stopped block, T76, T114 with its control at the head, and the fork checks by E8's method.
   - E1, re-run against b5d5569, gave the same counts and no new refusal. E4's method proves its claim.
   - **RV-2319 (P3):** section 1 lacked five security claims of the README and the notes: the rights gate, who may answer, the logo and the wordmark, no dependency and no network of the tool's own, and the seats' Apps.
2. **3bd36fc: C38–C42, X69–X79 and E9–E11, with T84–T86 corrected; the commit records the Owner's ruling.**
   - For each row: its cited lines, line numbers, the suite's names, the CI columns against the run, and the fix and control columns, earlier release or #145.
   - E9, E10 and E11 were repeated. E10: each of the seven seat Apps is owned by the organisation, with no permissions and no events.
   - **RV-2320 (P3):** C39 dropped "`owner` and" from the condition its cited line gives.
3. **775d638: the times.** Each time the ledger keeps was printed by its run. Where a run printed none, the commit is named instead (row 114's control at the head), or the time is gone (E8).
4. **593ebe1: RV-2320 fixed.** C39 reads "without `owner` and `[seats]`, the old `answerers` list", true against README.md:303 and CHANGELOG.md:20–21.

**Section 1** now holds every security claim the CHANGELOG's 0.19.0 section, the README and both notes make about the tool. CHANGELOG.md:128–129 and :136–137 take no row: they cover the project's own site and docs build.

**Left to the Order:** E2 and E3 are the Auditor's, and E6 is the notes' checksum, each added later as evidence.

**Disclosure:** there are no attack steps, and nothing of 0.19.1 beyond what FM-006 files.

Quality read: every claim names its evidence, and every test its jobs and its control. The corrections are each one commit, scoped to its finding. Clean.
Next: the Auditor's final-head checks.
