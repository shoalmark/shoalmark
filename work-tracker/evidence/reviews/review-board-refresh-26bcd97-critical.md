# FM-006 — the board's refresh: the critical verdict at 26bcd97

Verdict: **READY**. Every finding of this build is fixed in it. RV-2319 onward are unused.
Reviewed: 26bcd9706279004f3bcb495693f943aa2e146964. The whole change is `d9c154b..26bcd97`, at critical tier, judged against FM-006's *The fix round after the critical review*, its *Windows round*, and every line filed under it.
Reviewer: b3bdb000/reviewer-80 (claude-opus-5-5, xhigh), at the reviewer's bot address, unsigned, in worktree shoalmark-review-11, on 2026-10-02.
Independence: this is the builds' session (b3bdb000), so not independent. Each head was read from the shared repository, never from the Builder's worktree.
This verdict replaces the one at e477638, which this head contains.

This change answers a private security report.

## The passes and their findings

1. **The critical review at 1b65331** found RV-2304 … RV-2308, all P3.
   - RV-2304 was fixed in 3b7a360: AGENTS.md's *Checks* line is the Owner's text.
   - RV-2308 was fixed in 634dfc9: the checks hold the filed lines as literal text.
   - RV-2305, RV-2306 and RV-2307 are 0.19.1's, as FM-006 files them.
2. **The scoped check at ee6c28a** found RV-2309 … RV-2313 (two P2, three P3), each fixed in this build:
   - RV-2309: 6ff2a33.
   - RV-2310: d0bbcb4.
   - RV-2311: e889500.
   - RV-2312: e3ef17e.
   - RV-2313: 6884bc2.
   - **Correction:** that check called the reading rule clean, and it was not. `--vendor` did not yet read only the files it copies; that is RV-2314.
3. **The scoped check at f88546f** found two P3s:
   - RV-2314: `--vendor` reads only the files it copies. Fixed in 957d625.
   - RV-2315: the configuration check judges every worktree's settings. Fixed in d488cae.
4. **The scoped check at 4087e23** found RV-2316 (P3): the gate reads only the files a PIN names inside the copy. Fixed in c3b8296, with 7e56b7a and e8d2eea of the same rule.
5. **The scoped check at e8d2eea** found RV-2317 (P3): `--brand DIR` judges each file as named and as resolved. Fixed in e477638.
6. **The Windows round, `90abab9..d443cf5`,** answers CI run 36998106048, which was red on both Windows jobs. Each fix says whether the tool or the test was wrong, and that is true:
   - a7d790a, the test: two worktrees' copies are compared in one form.
   - 9b69d0d, the tool: what is said while the configuration is read is UTF-8 from the start, as everything after it was. It has a new check and its control.
   - 9375e0e, the test: the watch reads a Windows command line and proves it sees a start before a check relies on it.
   - 90eee04, the test: the commit object is written as bytes, and the control needs the commit.
   - 5126178, the tool: `--check` reads a vendored copy's PIN and VERSION under the reading rule.
   - d443cf5, the notes: the commits bullet says what AGENTS.md:52 says, and 0.19.0's two security lines are the Owner's, word for word.
   - No assertion is weakened.
7. **The scoped check at d443cf5** found RV-2318 (P3). Fixed in 26bcd97, test-only, with the assertions unchanged: the PIN names check proves that the watch sees an open before it relies on one. No other check relies on the watch without such a proof.

## What the build covers, as checked

- **The reading rule.** In every run, a tracker, the configuration and every file of the tree are read only as a regular file inside the repository, following no symlink. The board's refresh leaves such a file with its line, and every other run refuses in one line, exit 4. `--vendor`, the gate and `--check`'s report read only what a vendored copy's PIN names inside the copy.
- **The write rule.** Every write of the tree is a regular file inside the repository, never through a symlink, and the rule is asked before a folder is made. A destination a person names is resolved once, then judged as named and as resolved.
- **The deriver.** A deriver that is a symlink is refused in one line, and a folder named `derive` is no deriver.
- **`--install-hook`.** It refuses in one line, writing nothing, where a setting a working tree reads, or an include setting's target, comes from a file inside a working tree.
- **`--triage`.** It starts no git in a submodule path that resolves outside the repository.
- **Output.** The tool's output is UTF-8 from its first line.
- **Texts.** AGENTS.md's *Checks* line, literal filed lines in the checks, and they/them for the Owner in the tool's comments.

## Tests and runs

- **Controls.** Each new or changed check fails beside its older tool and passes at its fix, run with the commands in the tests' record. At this head, the PIN names row fails beside 4087e23's tool and passes, and the submodules rows pass.
- **`python3 -u test_core.py`** at 26bcd97: 158 ok, all green, exit 0.
- **Runs read:**
  - The Builder's full run at d443cf5: 861 ok, 0 failed, 3 skipped (FM-032's browser regeneration).
  - CI run 37005430667 at d443cf5: success on all five jobs.
  - The Owner's CI run on this head: https://github.com/shoalmark/shoalmark/actions/runs/37009286728 (workflow_dispatch), green on all five jobs. ubuntu 3.9 and 3.12 and macOS 3.12: 1019 ok, 0 FAIL, 3 skipped in 1 block; windows 3.9 and 3.12: 1010 ok, 0 FAIL, 10 skipped in 6 blocks. Every job ends "all green".
- **Disclosure and pronouns:** clean in the commit messages, test names and comments across the change.

Quality read: each fix is the smallest one that meets its filed line, and each comes with its test and a control that fails beside the older tool. Clean.
Next: the ledger, which names the Owner's CI run on this verdict's head; then the Auditor's final-head checks.
