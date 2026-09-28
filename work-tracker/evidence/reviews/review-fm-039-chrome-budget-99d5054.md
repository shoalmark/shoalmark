# Review — FM-039, the Chrome budget follows a control, at 99d5054 (2026-09-28 04:32 CEST, Reviewer, session `8e509911/reviewer-40`)

- **Branch:** `fm/039-the-chrome-budget-follows-a-control`, tip `99d5054` (`99d50540af7d5409d02ac20424e044e906d7e0a6`,
  confirmed by `git ls-remote`). Off `origin/main` `bbbfc0b`, it carries:
  - `1dcc2a8`, FM-039 In Progress (tracker only);
  - `c0f9a86`, the build: `test_shoalmark.py` and the CHANGELOG;
  - `e4c4006`, the record;
  - `99d5054`, the merge of main `3bc0a51`.

  All four are the Implementer seat's (`8e509911/implementer-48`).
- **Tier: code — the suite; not critical.** `git diff origin/main...99d5054 -- lefthook.yml scripts/ .github/
  shoalmark.py` is empty: `shoalmark.py` is byte-identical to main's. What changed is `test_shoalmark.py` (the
  browser helpers `_chrome_probe` and `_chrome_run`, the helper test, `_block_run`, FM-035's case, and one new block),
  `CHANGELOG.md`, FM-039's tracker and `INDEX.md`.
- **Independence:** same session — a sub-agent of 8e509911, reported.
- **Verdict: READY WITH FINDINGS.** One P3, RV-693. It is numbered from the highest id I saw at 04:30. That is
  RV-692, on PortDive's `bug/327-sitting-one-fix-forward` at `c7b53202` (read through the forge's compare API, no
  fetch), taken by the Owner's other session. Shoalmark's highest is RV-691.

## What I ran

| run | result |
|---|---|
| the rule, read (`test_shoalmark.py` 426–478, 515–527, 874–905) | `_chrome_probe` times its `about:blank` run into `_CONTROL_S`. `_chrome_run` runs each attempt with `timeout=own + timeout` and raises *"did not return {page} within {timeout} s beyond Chrome's own {own:.1f} s, tried twice"*. FM-035's block gets its 5 s through `_parts`' rewrite of the default, so the board's budget is **control + 5 s**, the ruling's rule. A control past 60 s is unchanged (*"Chrome started and did not render a blank page within 60 s here"*): it skips by name. The retry is kept. The control runs once per interpreter (`_PROBED`) and never per attempt: RV-693 |
| both suites, one interpreter at a time, started at load 3.60 / 3.25 / 3.15 / 4.05, with no user-activity assertion (the display's sleep is part of what is tested) | `test_shoalmark.py` **507 ok / 0 FAIL**, *skipped here: 0 checks — every check ran*, on 3.14.3 and 3.9.6. `test_core.py` **148 ok / 0 FAIL** on both. All four exit 0. The Implementer's counts are reproduced. In the suite, FM-035's hang line read *within 5 s beyond Chrome's own 6.0 s* (3.14) and *6.2 s* (3.9), and the new FM-039 case's control was 11.1 s on both |
| FM-035's case and FM-039's new case, built exactly as the suite builds `_block_run`, from the tip's test file and from `origin/main`'s (`git archive 3bc0a51`), 04:26–04:28, load 3.6–4.7; Chrome alone on `about:blank` 6.36 s and 6.17 s just before | **tip**: the healthy board passes (exit 0, 19.0 s, control 6.2 s, so the budget printed is 11.2 s). The hang FAILS by name (exit 1, 29.0 s): *"headless Chrome did not return index.html within 5 s beyond Chrome's own 6.1 s, tried twice"*. The slow start passes (exit 0, 33.7 s, control 11.0 s). **main's suite**: the healthy board FAILS (*within 5 s, tried twice*, 16.9 s), and so does the slow start (21.6 s). The tool is the same file on both sides, so *the branch's suite against main's tool* is the branch's run above |
| the helper test | `saw [6.5, 6.5]`: both attempts ran with the control's 5.5 s plus the 1 s asked. The failure text names both numbers |
| the stub | it patches `subprocess.run` inside the block's own interpreter. It sleeps 5 s before every Chrome run, the control's included, and charges it to the run's timeout. A 5 s wall-clock budget therefore dies before the page begins (main: FAIL), and control + 5 passes (tip). It is the same test as a slow executable, as far as the budget is concerned |
| `--check` | exit 0. *INDEX.md is up to date — 40 trackers*. *judged before build: on — 3 commit(s) on a detached HEAD since origin/main, every build commit under a judged In Progress tracker*. The one build commit, `c0f9a86`, was read at its parent `1dcc2a8`: FM-039 is `status: In Progress`, `triaged: 2026-09-27`, P2, rank 7. `1dcc2a8` and `e4c4006` change the tracker directory only, so they are not judged. *The Owner's two sections: guarded — 4 commit(s) … none changes them* |
| `--session-check` | exit 0 |
| `--queue` | `branch fm/039-the-chrome-budget-follow… @ 99d5054  wait: no pull request — no verdict on 99d5054` |
| `git merge-tree --write-tree origin/main HEAD` | clean (`a96dbd0`). The merge `99d5054`: `git diff 3bc0a51 99d5054` holds exactly the branch's four files. INDEX.md was regenerated and differs from main's only in FM-039's rows |
| CHANGELOG and tracker | `## Unreleased — 0.18.6` has a bullet naming FM-039 and FM-035. `VERSION` is still 0.18.5. FM-039's *What is true now* names `c0f9a86`, and its ship-log rows name `1dcc2a8` and `c0f9a86`. Both say what is not proven: a load of 20, and the board's own cost beyond the control at that load |

## The Implementer's claims

- **`next: review` set by hand — not a finding.** `--schema` gives `next:`'s writers as *"the seat that ends work;
  `--answer`, with the answer; a pass only where none was left"*, and its values as *review · run · wait · owner ·
  script · build*. The Implementer ended its work and wrote the move that follows, a Reviewer's pass: the schema's own
  writer and one of its values. The FEAT-180 rule, *verdicts through the command, never hand-edited*, is PortDive's.
  As I read it, it is about a triage pass's verdicts (`tier`, `rank`, `triaged`), not a build seat's closing move, and
  shoalmark's schema names this writer. `--check` exits 0 on it.
- **The wider rule, 60 s beyond the control for every other browser check — the same honest rule, not scope creep.**
  It lives in the one helper every browser check uses. Two rules would be the odd outcome: a page's cost for the board
  and Chrome's start for the rest. The CHANGELOG and *What is true now* disclose it. Its cost is small: a real hang
  elsewhere is failed about twice the control later (about 12 s here), and a control is capped at 60 s by the probe.
- **The control runs once per block:** true for FM-035's case, whose block runs in its own interpreter and times
  Chrome just before the board. In the full suite it runs once per run, at the first browser block (`strip`, line
  744): RV-693.
- **The before/after:** reproduced. `origin/main`'s suite fails the healthy board at a load under 5; the branch passes
  it, fails the hang by name, and passes the slow start.
- **The counts:** 507/507 and 148/148 on both Pythons, 0 skipped. Reproduced from my own runs, not from the
  Implementer's overwritten 3.14 output, which it disclosed.
- **Not proven, as it says:** the Done-when's load of 20 or more. My runs saw a 1-minute load of 3.2–11.2. The branch
  proves this: at this machine's own Chrome start, 5.4–6.4 s tonight, the healthy run passes and the hang fails by
  name; and a Chrome made 5 s slower still passes. It does not prove that the board's own cost beyond the control stays
  under 5 s at load 20.

## Findings

**RV-693 · P3 · confidence high — the control is timed once per run, not per block, and the CHANGELOG says "before a
browser block".** `_browser` caches the probe in `_PROBED`, so a full suite times Chrome once, at its first browser
block. Every later block's budget, 60 s beyond, counts from that first control, minutes earlier. FM-035's case, the
one the ruling is about, is not affected: each of its runs is a fresh interpreter, and the control is timed just
before the board. With a 60 s margin the stale control changes nothing here. Only the wording claims more:
*"The suite already runs Chrome on a blank page before a browser block"* (CHANGELOG).

**Fix forward:** *once per run, before its first browser block*. Or re-time the control per block, if the rule is
meant per block.

## Verdict

**READY WITH FINDINGS.** RV-693 is P3, fixed forward. The Done-when's load of 20 stays unproven, as the record says.

The Owner lands this by merging; a merge rules nothing.
