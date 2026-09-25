# Review — FM-035, 0.18.4's CI fix at df4c8ab

Reviewed: `df4c8abcac56b311d76613f2faf54661b8accf1d` on
`fm/035-ci-green-on-every-platform`, 2026-09-25.

**Tier: code. Verdict: NOT READY (R1 P2; R2 P3).**

## Seat and independence

A cold session started by the Owner under his path line 3. Reviewer session `01a0d87d`,
worktree `shoalmark-review-cold`; independent of building session `8e509911/implementer-20`.
The four cold-start answers: provide adversarial verification; guard against turning refutation
into identity; use passing controls and a deliberately broken renderer to test the objection;
hand this record to the Owner for the Principal and Implementer. The Reviewer changes only this
review file and does not fix or disposition the findings. The sealed session directory was untouched.

## What survives

- The fetched head is the requested head. The four commits, in chronological order, are
  `833d3c5`, `29dbd10`, `b6e2030`, `df4c8ab`. PR 73 supplied the filed and judged base.
  The first commit sets FM-035 In Progress before the builds and appends the filing review's
  R7/R8 corrections; the R6 times are corrected. Each fixing commit explains its proposed cause.
- The Owner's downloaded logs for run 36121290371 show both Ubuntu jobs finishing both suites
  with `all green`; both Windows jobs fail exactly the wordmark-size and RV-479 checks;
  macOS raises `TimeoutExpired` at `_, b83 = _rows("AP-080", _pick)` after 60 seconds.
  This is verification of the downloaded logs, not a new hosted matrix run.
- **Windows encoding:** using the repository's test prelude, `run_safe`, and unchanged RV-479
  block extracted from each commit, with `LC_ALL=en_US.ISO8859-1 PYTHONUTF8=0`, the parent
  `833d3c5` gives three passes and one failure (exit 1); `29dbd10` gives four passes (exit 0).
  The failed parent assertion is the merged answer/revoke ship-log comparison. Both probes
  use the head's unchanged tool behavior. The extraction imports `shutil`, normally imported
  earlier elsewhere in the old suite. This is a Latin-1 reproduction, not a native cp1252 runner.
  Naming UTF-8 for both changed `git show` readers is correct.
- **SVG size:** changing the tool is justified: a checkout's newline conversion should not decide
  whether an otherwise identical SVG is accepted. `brand_bytes` is called only by the logo and
  wordmark paths. Both now use its normalized bytes for counting and embedding; PNG bytes remain
  unchanged. `inline_svg` retains its own cap and validation. No other size reader is changed.
  An independent probe wrote an SVG containing 100,000 line feeds: LF size 100,046, CRLF physical
  size 200,046, normalized size 100,046; both returned identical bytes and were accepted by
  `inline_svg`. A PNG containing CRLF returned its original bytes and size. Rejecting files over
  twice the cap before reading is sound: CRLF replacement cannot reduce a file by more than half.
- The clipboard stub removes the real pasteboard dependency from the answer-dialog fixture.
  The existing second-screen tests also exercise an absent clipboard. All headless Chrome launches
  in this suite now use `_chrome_run`; its focused test verifies two timeout attempts and the raise.
- `VERSION` remains `0.18.3`; the changelog starts `Unreleased — 0.18.4`. `ci.yml` is unchanged,
  including `fetch-depth: 0`. It supports a release tag, `ready_for_review`, and manual dispatch;
  the brief's “runs on a tag” is not an exclusive description of its triggers.
- `python3 shoalmark.py --check`: exit 0, `INDEX.md is up to date — 35 trackers`, and
  `judged before build: on — 4 commit(s) on a detached HEAD since origin/main, every build commit
  under a judged In Progress tracker`. `--session-check`: exit 0. `lefthook run pre-commit`
  dispatches successfully; with nothing staged its commands skip. Commit-time dispatch is recorded below.

## Findings

### R1 — P2, high confidence: a broken renderer becomes a successful suite

`test_shoalmark.py:384–418`, the ten `_ChromeSlow` catch sites, and the final summary at
`3388–3394` turn any persistent browser timeout into a skip. A timeout does not establish that
this platform cannot run the test. The renderer under test can itself hang. The summary prints
`skipped here`, then `all green`, and returns 0 whenever the remaining checks passed.
The unchanged CI workflow accepts that exit status and has no skipped-test gate. The local
lefthook test command redirects successful suite output to `/dev/null`, hiding even the warning.

**Measured counterexample:** run the actual first browser block with its normal fixtures and
assertions, reducing only the helper timeout to five seconds. Control: both assertions pass,
zero skips, exit 0. Then wrap the test's `run` helper to prepend
`<script>while(true){}</script>` to its generated `index.html`. Real installed Chrome times out
twice; the same block prints:

```text
skip  the board, rendered in a browser — headless Chrome ran past 5 s twice on this machine
skipped here: 1 ['the board, rendered in a browser']
FAIL COUNT 0
```

The probe exits **0** despite a deliberately broken page. The shorter budget only accelerates
this reproduction; an infinite loop also outlives 60 seconds. A complete-suite timeout injection
is recorded below as a separate check of the final summary and exit.

**Strongest counterfact:** the tracker explicitly asks for named skips where a check cannot run;
these skips are named and repeated at the end, and a completed browser run with a false assertion
still fails. That supports skipping a demonstrated missing capability. It does not distinguish a
page hang from an unavailable browser, so the current rule weakens the release's evidence.

**Closure/falsifier:** retain named reasons and retry if useful, but demonstrate that a working
browser plus a hanging product page yields a nonzero release-suite result. Separately demonstrate
that a genuinely unavailable capability follows the explicitly permitted skip policy. A healthy
control page can help distinguish those cases; a CI requirement for browser checks is another
possible implementation. The deliberate page-hang probe must stop passing, and the healthy
control must continue to pass. The Implementer chooses the fix; this review does not implement it.

### R2 — P3, high confidence: the clipboard diagnosis is stated more strongly than its evidence

The first Unreleased changelog bullet and the comment above `_rows` say the runner's real
clipboard never answered. The log establishes the call site and timeout, but contains no
clipboard instrumentation. `b6e2030` itself says the cause was not reproduced and reports another
local timeout at `_rows("AP-081")`, where no clipboard was involved. The prior CI run died before
reaching the later FM-013 checks, so that run cannot show those later checks survived because of
their stub. Stubbing the clipboard is sensible isolation; it does not prove the historical cause.

**Closure/falsifier:** label the historical cause as suspected and state the observed timeout and
removed dependency precisely, or supply a controlled reproduction that isolates the pasteboard
as the cause. The record should not claim a verified platform root cause from the stack alone.
This is a claim-quality finding, not an objection to the stub.

## Reproducing the real-browser counterexample

Run from the reviewed checkout. This executes the original fixture and assertions without
editing the repository. It requires the installed Chrome used by the suite.

```python
import pathlib, subprocess
s = pathlib.Path("test_shoalmark.py").read_text()
prefix = s[:s.index("# --- a fresh repository:")]
helper = s[s.index("_CHROME_FLAGS ="):s.index("_tries, _real_run =")]
helper = helper.replace("timeout=60", "timeout=5")
block = s[s.index("# --- the board, seen:"):s.index("# --- FM-020: a whole id")]
injection = """
_real_test_run = run
def run(root, *args, **kwargs):
    result = _real_test_run(root, *args, **kwargs)
    page = root / 'docs/work-tracker/index.html'
    if page.exists():
        page.write_text('<script>while(true){}</script>' + page.read_text())
    return result
"""
for name, mutation in (("control", ""), ("page-hang", injection)):
    code = ("__file__=" + repr(str(pathlib.Path("test_shoalmark.py").resolve()))
            + "\n" + prefix + helper + mutation + block
            + '\nprint("skipped here:",len(SKIPS),SKIPS);'
              'print("FAIL COUNT",len(FAILS));sys.exit(bool(FAILS))\n')
    result = subprocess.run(["python3", "-u", "-c", code])
    print(name, "exit", result.returncode)
```

## Suite results and handoff

On macOS, subprocess return codes were captured directly, with stdout/stderr retained per run:

| Command | Exit | Passed checks | Browser skips |
|---|---:|---:|---:|
| `python3 test_shoalmark.py` (3.14.3) | 0 | 396 | 0 |
| `python3 test_core.py` (3.14.3) | 0 | 148 | 0 |
| `/usr/bin/python3 test_shoalmark.py` (3.9.6) | 0 | 396 | 0 |
| `/usr/bin/python3 test_core.py` (3.9.6) | 0 | 148 | 0 |

Each completed normal suite ends `all green`. The complete-suite adversarial run replaces only
Chrome subprocess calls with `TimeoutExpired` after the helper's own self-test; git, the tool,
all other checks and the final summary are unchanged. Result: **exit 0, 369 passing checks,
10 named browser-block skips, final line `all green`**. Thus 27 assertions disappear from the
396-check normal run without changing the success status. This synthetic run establishes the
whole-suite exit behavior; the real Chrome/infinite-loop control above establishes that a
product defect can reach the same path.

With this review staged, `lefthook run pre-commit` exits 0: session and tracker-index pass;
the Python hook skips because no Python file is staged. The generated INDEX remains unchanged.
The four full suites above were run explicitly against the reviewed code.

The five-job hosted matrix has **not** been run on this branch by this Reviewer. Native Windows
3.9/3.12 and hosted macOS 3.12 remain unverified; local Python versions are 3.14.3 and 3.9.6.
The Owner's planned v0.18.4 tag follows FM-030's deadline work. This review does not declare
FM-035 Done when satisfied or the unreleased version proven across platforms. The next move is
the Principal's Implementer fixing R1, followed by an independent verification pass under the
code tier; R2 needs correction or evidence. Only the Owner lands and tags the release.

**Verdict: NOT READY.**

the Owner lands this by merging; a merge rules nothing.
