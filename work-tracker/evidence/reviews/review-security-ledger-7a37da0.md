# v0.19.0 — the security ledger: the review at 7a37da0

Verdict: **READY**. One P3 goes to the E2/E3/E6 commit (below), and nothing holds READY. RV-2322 onward are unused.
Reviewed: 7a37da01d264ba8f7767ff3170ca101d755da2a9 — the ledger on CI run 37033610114, FM-006's filing of the cold review's F1 as amended, and `CHANGELOG.md:44`.
Reviewer: b3bdb000/reviewer-80 (claude-opus-5-5, xhigh), at the reviewer's bot address, unsigned, in worktree shoalmark-review-11, on 2026-10-02. Independence: this is the builds' session (b3bdb000), so not independent. Tier: critical.
Earlier checks of the ledger: `review-security-ledger-593ebe1.md`.

This change answers a private security report.

## What was checked

- **The scope:** one commit, three files — the ledger, FM-006's F1 filing, and `CHANGELOG.md:44`.
- **The header,** against run https://github.com/shoalmark/shoalmark/actions/runs/37033610114 on `6e2d689`:
  - On ubuntu and macOS: 863 ok, 158 ok, and 3 skipped in 1 block. On Windows: 854 ok, 158 ok, and 10 skipped in 6 blocks.
  - The three checks not run on Windows are as on main. Each job ends *all green*.
  - The runs before it, and every commit after `6e2d689`, are as the header says.
  - The controls line holds: the suite at `d443cf5` differs from the head's only in rows 114–115 and the F1 block.
- **T130 and T131:**
  - Both ran on all five jobs.
  - T130's run alone beside `df4f266` stopped with the AttributeError the row names, 18:28:47–18:29:59. At the head it passed.
  - T131 is the in-suite control and FAILS beside `df4f266`'s tool.
- **The other rows:**
  - T1–T129 are unchanged. 18 rows checked against the new run hold, the Windows rows among them.
  - The X rows' line numbers hold at the head: 12 checked.
- **The claims:**
  - C32 says what `CHANGELOG.md:44` now says, and names its evidence.
  - `CHANGELOG.md:44` and the F1 filing are the Owner's words.
  - The tool does what both say: a tracked view gets a page that loads nothing, a tracked page is left as committed, and nothing git tracks is written over.
- **The executed checks:**
  - E1, E4, E9 and E11 at `6e2d689`: each row's result and time are what its run printed.
  - E7 and E8: `SECURITY.md` is unchanged since `e0a21dd`, and `test_core.py` since `90abab9`.
- **Disclosure:** there are no attack steps and nothing of 0.19.1.

## The P3, to the E2/E3/E6 commit

- **RV-2321 · P3:** T131's fix column says more than its fix. It should read `d1661e3 — the cold review's F1`, as T130's does.

Quality read: every CI column comes from the one run the ledger names, and every time from its run's own output. Clean.
Next: the Auditor's final-head checks, then E2, E3 and E6.
