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


## Round two — 4e4d63b, 2026-09-25

Reviewed: `4e4d63bbaacc1f8cba01234a0a2d39276185e5f8`, the one fixing commit after
`b730c29`, on the same branch. **Tier: code.** Same independent cold Reviewer session
`01a0d87d`, started by the Owner under his path line 3; the builder remains
`8e509911/implementer-20`. This pass verifies the fixes; the Principal receives the record.
The first pass above remains the record of what was true at `df4c8ab`.

### R1 — the blocking page-hang defect is verified fixed

I reran the real-browser counterexample against the new helper and the original board block,
with the five-second budget used in the first pass. The healthy page passes both assertions,
zero skips, exit 0. The same generated page with `<script>while(true){}</script>` now gives:

```text
  FAIL  the board, rendered in a browser — headless Chrome did not return index.html within 5 s, tried twice
skipped here: 0 checks — every check ran
FAIL COUNT 1
```

**Observed exit: 1.** The control passed before the product page was tried. `_hung` adds the
failure to `FAILS`, and the suite's actual final branch exits 1 for any such failure. All ten
former `_ChromeSlow` catch sites now use `_ChromeFailed` and `_hung`; none converts a product
page timeout to a skip. The branch also includes a regression using the real infinite-loop
page, a healthy page, and the absent-browser case. Its subprocess assertions check exit status.

For the independent probe, I extracted the unchanged test prelude, the helpers between
`_CHROME_FLAGS =` and `# the helpers themselves:`, and the board block ending immediately
before `# --- FM-035, its cold review's R1:`. The mutation is the same wrapper printed in the
first pass. The epilogue prints `skipped_line()` and `len(FAILS)`, then exits with `bool(FAILS)`.
Only the product-page timeout was reduced to five seconds; the control's timeout stays 60.

### Capability gaps — tested and accepted within the tracker’s skip policy

With `_CHROME = None`, the same board block skips by name, reports two checks omitted and
`this is NOT a full pass`, and exits 0. With only the blank-page subprocess made to raise
`TimeoutExpired`, it reports `Chrome started and did not render a blank page within 60 s here`,
the same two-check skip and partial-pass warning, and exits 0. All other subprocess calls in
that probe remain real.

Treating that control failure as a platform gap is acceptable under FM-035's explicit
permission for a check that cannot run to skip: the blank control has not loaded the product
page, so a product-page loop cannot cause this particular skip. A control timeout establishes
unavailability for this run, not permanent lack of browser support. It is cached for the run,
so a transient control failure can omit every browser block. Such a run must be read as partial;
it supplies no browser evidence and cannot alone establish the release's platform coverage.
This residual limitation is disclosed, rather than graded as another blocking page-hang defect.

### R2 — the cause claim is verified corrected

The Unreleased bullet, the comment above `_rows`, and the appended FM-035 ship-log row now
state what the log showed, call the clipboard explanation inferred, and say the hang itself
was not reproduced. The clipboard stub remains. This meets R2's correction condition without
claiming a new reproduction of the historical macOS incident. The old commit message remains
historical and is expressly corrected by the new ship-log row.

### R3 — P3, high confidence: the local hook still hides a partial run

`lefthook.yml` is unchanged: each successful suite is run with `>/dev/null`, and output is
shown only after a nonzero exit. The explicitly allowed capability skips return 0. Therefore
both the named skip and `this is NOT a full pass` disappear when this path runs through the
local hook. Direct suite output also still finishes with `all green` after the partial-pass
warning (`test_shoalmark.py`'s last line).

The Implementer raised the hook limitation in the brief; this pass confirms it against the
actual command and the observed zero-exit capability probes. It is **P3**, not the old R1 P2:
a hanging product page now fails, the CI workflow prints the suite output directly, and the
tracker explicitly allows capability skips. The remaining defect is the local report's loss
of the qualification that the new summary was designed to convey.

**Closure/falsifier:** preserve a successful suite's skip summary in hook output, and qualify
the final success line when checks were omitted. Prove it with an unavailable-browser fixture:
the hook must display the named skips or their explicit partial-run summary even with exit 0.
Do not change the now-working nonzero exit for a broken page. This is a nonblocking finding;
the Principal owns its disposition.

### Verification and handoff

Each suite's exit status was captured directly. On local macOS:

| Command | Exit | Passing checks | Browser skips |
|---|---:|---:|---:|
| `python3 test_shoalmark.py` (3.14.3) | 0 | 399 | 0 |
| `python3 test_core.py` (3.14.3) | 0 | 148 | 0 |
| `/usr/bin/python3 test_shoalmark.py` (3.9.6) | 0 | 399 | 0 |
| `/usr/bin/python3 test_core.py` (3.9.6) | 0 | 148 | 0 |

The expected `FAIL` text inside the passing infinite-loop regression's quoted subprocess
output is its negative-control evidence, not a failed top-level check. The suite ends
`skipped here: 0 checks — every check ran` and `all green`.

`python3 shoalmark.py --check`: exit 0, INDEX up to date (35 trackers), six commits since
`origin/main`, every build under a judged In Progress tracker. `--session-check`: exit 0.
With the review staged, `lefthook run pre-commit` exits 0: session and tracker-index pass;
the Python hook has no matching staged files. The full suites above were run explicitly.
The generated INDEX is unchanged.

The encoding and SVG implementation are unchanged from the first pass: `shoalmark.py` has no
round-two diff, and neither changed UTF-8 reader nor the CRLF fixture was altered. The first
pass's locale and normalized-byte evidence still applies, alongside the rerun full suites.
`VERSION` is still 0.18.3 and the head remains `Unreleased — 0.18.4`. The CI workflow is unchanged.

The strongest counterfact to readiness is that an unavailable browser still produces an exit-0
partial run, and the local hook conceals its qualification (R3). The product-hang counterexample
now fails as required. **The five-job hosted matrix has not been rerun by this Reviewer**;
native Windows 3.9/3.12 and hosted macOS 3.12 remain unverified. The Owner's future v0.18.4 tag,
after FM-030's deadline work, must supply the remaining release evidence; this is readiness of
the reviewed fix, not a claim that FM-035's five-green-jobs Done when is already satisfied.

**Verdict on 4e4d63b: READY WITH FINDINGS (R3 P3).** R1's blocking behavior is fixed and R2's
claim corrected. The Principal receives the remaining finding; the Owner alone lands and tags.

the Owner lands this by merging; a merge rules nothing.


## Verified again on a911722 — the merge of main

Reviewed: `a911722547f5b194385d99db5892f903ce26c085`, 2026-09-25 18:18 CEST — the Principal seat's merge of
`origin/main` `8b267b4` (PR 76) into this branch (session `8e509911`, worktree `shoalmark-principal`).
**Tier: code — the merge only; the substance's verdict is the cold session's `1af6b0b` on `4e4d63b`.**
**Independence: same session — `8e509911`'s own sub-agent (`8e509911/reviewer-11`, worktree `shoalmark-review-2`),
reported; the Owner may have his cold session verify the merge instead.** The two passes above stand as written.

### What I ran

- `git fetch origin`: `origin/fm/035-ci-green-on-every-platform` is `a911722`, `origin/main` is `8b267b4`;
  `git switch --detach a911722`. Its parents are `1af6b0b` (the cold verdict) and `8b267b4`; the merge base is `d86973f`.
- **Only the branch's seven files differ from main.** `git diff origin/main...HEAD --stat` and
  `git diff 8b267b4...1af6b0b --stat` print the same seven files, 737 insertions and 220 deletions each: CHANGELOG.md,
  shoalmark.py, test_shoalmark.py, the FM-035 tracker, INDEX.md, TRIAGE.md and this file. `git diff 8b267b4 a911722`
  names those seven and no other path, and for each one its changed lines hash the same as the branch's own
  (`d86973f..1af6b0b`). Five are byte-identical to `1af6b0b`'s blobs — CHANGELOG.md, shoalmark.py, test_shoalmark.py,
  the FM-035 tracker and this file, so the cold sections above are unchanged by the merge. `git diff --name-only
  4e4d63b a911722` holds no path outside `.md`: the code here is the code the cold session read.
- **The conflict is the one the merge's message names.** `git merge-tree --write-tree 1af6b0b 8b267b4`, the merge
  redone, conflicts in INDEX.md and TRIAGE.md only; its tree differs from `a911722`'s in those two files alone.
- **TRIAGE.md.** No conflict marker, here or anywhere in the tree (`git grep` for marker lines is empty). The
  2026-09-25 paragraphs run newest first — FM-030's second raise (13:31:26), FM-035's new filing (12:11:44), FM-030's
  raise (07:06:48) — the two same-day passes of the conflict once each. The second-raise paragraph is main's byte for
  byte; the FM-035 paragraph is `1af6b0b`'s byte for byte, and main's with `12:11:44` for `12:1x`; every other line is main's.
- **INDEX.md** differs from main in FM-035's row alone: 10:03 for 10:02, In Progress for Proposed, moved from backlog to
  progress. `python3 shoalmark.py` wrote INDEX.md (36 trackers) and `git status --porcelain` stayed empty. Ranks 1–10,
  no two trackers sharing one.
- `python3 shoalmark.py --check` 0 (INDEX up to date, 36 trackers; 7 commits since `origin/main`, every build commit
  under a judged In Progress tracker; the filing freeze holds, 20 open); `--session-check` 0; both 0 again under
  `/usr/bin/python3`.
- The suites, one at a time, each exit captured:

| Command | Exit | Passing checks | Browser skips | Last line |
|---|---:|---:|---:|---|
| `python3 test_shoalmark.py` (3.14.3) | 0 | 399 | 0 | `all green` |
| `python3 test_core.py` (3.14.3) | 0 | 148 | — | `all green` |
| `/usr/bin/python3 test_shoalmark.py` (3.9.6) | 0 | 399 | 0 | `all green` |
| `/usr/bin/python3 test_core.py` (3.9.6) | 0 | 148 | — | `all green` |

  The counts are round two's on `4e4d63b`, check for check.
- `git merge-tree --write-tree origin/main HEAD` exits 0 with HEAD's own tree (`df9de5c`); `origin/main` is an
  ancestor, so the merge to main is a fast-forward.

### R4 — P3, medium confidence: the merge's message reports a verification that had not yet run

`a911722`'s message, committed 18:02:30, ends *the substance is unchanged — verified again on this tip*. No
verification of `a911722` existed then: this pass is that verification, and it began at 18:04. Read as the plan, the
line is true now; read as a report, it ran ahead of its evidence. Medium, because the first reading is open. It cost
nothing — the claim holds — and git is its record, not rewritten. **Fix forward:** a merge's message says *to be
verified on this tip*; the verification's commit says *verified*.

### Not proven here

The five-job hosted matrix has not run on `a911722`: native Windows 3.9/3.12 and hosted macOS 3.12 remain unverified,
as round two records; CI runs when the pull request is marked ready and on the tag. R3 (P3) is carried unchanged — the
merge touched neither `lefthook.yml` nor either suite.

**Verdict on a911722: READY WITH FINDINGS (R4 P3).** The merge brought main's changes and the branch's own, nothing
else; the substance is unchanged, and the cold session's READY WITH FINDINGS (R3 P3) on `4e4d63b` stands for it. The
Principal receives R4; the Owner alone lands and tags.

the Owner lands this by merging; a merge rules nothing.
