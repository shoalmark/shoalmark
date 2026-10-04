# FM-006 — the board's refresh: the critical verdict at e477638

Verdict: **READY**. Every finding of this build is fixed in it. RV-2318 onward are unused.
Reviewed: e477638ea82e27885f500c91dad9a4c4683c0834. The whole change is `d9c154b..e477638`, at critical tier, judged against FM-006's *The fix round after the critical review* and every line filed under it, up to cb7bdb8.
Reviewer: b3bdb000/reviewer-80 (claude-opus-5-5, xhigh), at the reviewer's bot address, unsigned, in worktree shoalmark-review-11, on 2026-10-02.
Independence: this is the builds' session (b3bdb000), so not independent. Tier: critical.
Each head was read from the shared repository, never from the Builder's worktree.

This change answers a private security report.

## The passes and their findings

1. **The critical review at 1b65331** found RV-2304 … RV-2308, all P3.
   - RV-2304, AGENTS.md's *Checks* line: fixed in 3b7a360. It is now the Owner's filed text, word for word, and nothing else in the file changed.
   - RV-2308, checks that compared a filed line with the tool's own constant: fixed in 634dfc9. The lines are now written out.
   - RV-2305, RV-2306 and RV-2307 are 0.19.1's, as FM-006 files them.
2. **The scoped check at ee6c28a** found RV-2309 … RV-2313, two at P2 and three at P3. Each is fixed in this build:
   - RV-2309, the calendar files: 6ff2a33.
   - RV-2310, `--brand DIR --from` and `--vendor DIR`: d0bbcb4.
   - RV-2311, `--triage`'s worksheet folder: e889500.
   - RV-2312, a folder named `derive`: e3ef17e.
   - RV-2313, every include setting's target: 6884bc2.
   - **Correction:** that check called the reading rule clean, and it was not. `--vendor` did not yet read only the files it copies. That is RV-2314, found at f88546f.
3. **The scoped check at f88546f** found two P3s:
   - RV-2314: `--vendor` reads only the files it copies, each under the reading rule. Fixed in 957d625.
   - RV-2315: the configuration check judges the settings each worktree reads, its own configuration included. Fixed in d488cae.
4. **The scoped check at 4087e23** found RV-2316 (P3): the gate reads only the files a PIN names inside the copy. Fixed in c3b8296.
   Two more commits answer the same rule: 7e56b7a, for submodule paths in `--triage`, and e8d2eea, for destinations a person names.
5. **The scoped check at e8d2eea** found RV-2317 (P3): `--brand DIR` without `--from` judges each file as named and as resolved. Fixed in e477638.
6. **This check, `e8d2eea..e477638`:**
   - RV-2317 is as filed in cb7bdb8: both files are judged as named and under the resolved folder, before the folder is made.
   - The test adds one row to the destinations table, and its assertion is unchanged.

## What the build covers, as checked

- **The reading rule.** In every run, a tracker, the configuration and every file of the tree are read only as a regular file inside the repository, following no symlink.
  - The board's refresh leaves such a file with its line. Every other run refuses in one line naming it, exit 4, never a traceback.
  - `--vendor` and the gate read only the files a PIN names inside the copy.
- **The write rule.** Every run writes a file of the tree only as a regular file inside the repository, never through a symlink, and asks the rule before a folder is made.
  - A destination a person names (`--vendor`, `--brand`, `--brand --from`, `--standup FILE.ics`) is resolved once, where it is named. Each file under it is then judged as named and as resolved.
- **The deriver.** A deriver that is a symlink is refused in one line and nothing starts. A folder named `derive` is no deriver.
- **`--install-hook`.** It refuses in one line, writing nothing, where a setting any working tree reads comes from a file inside a working tree. The target of every include setting is judged the same way, whatever its condition and whether or not it exists yet.
- **`--triage`.** It starts no git in a submodule path that resolves outside the repository.
- **The texts.**
  - AGENTS.md's *Checks* line is the Owner's text.
  - The checks assert the filed lines as literal text.
  - The tool's comments say they/them for the Owner. The syntax tree without docstrings is unchanged, and so are the printed strings.

## Tests and runs

- **Controls.** Each new check of the fix round fails beside its older tool (1b65331, ee6c28a, f88546f or 4087e23) and passes at its fix, run with the commands in the tests' record.
  - At this head, the destinations row fails beside 4087e23's tool and beside e8d2eea's, and passes at e477638.
- **`python3 -u test_core.py`** at e477638: 158 ok, all green, exit 0.
- **Full runs read:**
  - ee6c28a: 830 ok, 0 failed.
  - f88546f: 846 ok, 0 failed.
  - The Builder's run at e477638: 857 ok, 0 failed, 12:18:30–12:47:40 CEST; `--check` and `--session-check` exit 0.
  - Each skipped 3 checks, FM-032's browser regeneration. CI's dispatched run on the draft is the independent run on the exact head.
- **Disclosure and pronouns:** clean in the commit messages, test names and comments across the change.

Quality read: each fix is the smallest change that meets its filed line, and each comes with its test and a control that fails beside the older tool. Clean.
Next: the Owner opens the draft PR and dispatches CI by hand on this verdict's head.
