# FM-006 — fork-queue hardening, independent review

Date: 2026-09-30.
Reviewed: `c2027d2bfde2bb8449c5bdea49c08c8a82c2e961`, tree `c744e797b22d1e84283d25251575059932e8ef91`, branch `fm/006-fork-pull-requests-wait`.
Base: `297896b1c3215245111a0302e5dd9fd58189cb5d`. `shoalmark.py` and `test_core.py` are byte-identical at `2c00aba`.
Reviewer: `reviewer@seat`, unsigned. Session `e55ed3e1` (harness `e55ed3e1-08ce-4b91-a8b9-7061a9d5a6b8`), Opus 5.5. The session
began on Sonnet 5.5 for the clone and the SHA check and moved to Opus before the diff was read; every judgement here is Opus's.
Worktree: `/private/tmp/shoalmark-review-fork-queue-c2027d2`, a fresh clone. Not the implementation session `01a0ec25`, not its
child; nothing spawned.

**Tier: code, critical.** `git diff --name-only origin/main...HEAD`: `CHANGELOG.md`, `shoalmark.py`, `test_core.py`, FM-006.

**Verdict: READY WITH FINDINGS.** All five claims hold on the diff. There are three P3 findings and none at P2: R1 and R2 are
fixed forward on this branch, and R3 is one line in FM-006 (rule 6). The queue is advice; it enforces no merge permission.
Same-repository verdict-author validation is out of scope, and that includes a fork commit a member has merged into a
same-repository branch.

## The claims, checked

1. **The flag reaches `queue_actions`.** `QUEUE_FIELDS` asks for `isCrossRepository`, and gh 2.87.3 lists it as a `gh pr list
   --json` field. `forge_prs` returns gh's rows unchanged to both call sites (`queue_cmd`, `queue_section`). The control builds
   gh's answer from the requested fields only, so it holds `QUEUE_FIELDS` itself. A gh without the field fails `gh pr list`
   and `--queue` exits 3 with no advice, so it fails closed.
2. **Every fork waits.** The fork row is built before any git read, and forks leave `prs` before `siblings`, `within`,
   `absent`, `heads` and `bases` are computed. Probe at tip, with the base's reading in brackets: a contained fork waits
   (`closes with PR 2`), a conflicting fork waits (`wait: conflict in base.txt`), a conflicting `answer/*` fork waits (the
   same), a clean self-READY fork waits (`merge`).
3. **Fork commits supply nothing to another PR.** At the tip, no fork SHA is in the verdict walk or the carry-over tests.
   Probe: a same-repository PR cherry-picked into a fork reads `wait: no verdict` (`close: carried into PR 5`). There is a
   further effect the brief does not name: a fork based on a same-repository branch excluded that branch from the walk and
   hid its PR's own READY. That PR now reads `merge` (`wait: no verdict`). This is correct, and R1 records it.
4. **Same-repository behaviour is unchanged.** With the flag false or absent, `queue_actions` at the base and at the tip gave
   identical rows over every probe PR and the pushed branches. With a fork open, a same-repository PR reads as it would
   with no fork open. `pushed_branches` did not change; R3 covers a pre-existing gap there.
5. **Tests and documentation.** The witness claim is reproduced in a focused harness (the FM-006 block only, not the
   suite): 5 controls fail at the base, the same-repository merge control passes, and all 6 pass at the tip. The
   controls miss one ordering (R2), and the documentation's second copies lag the code (R1).

Witness not repeated: core suite 155 passed; `--check` exit 0; `git diff --check` exit 0; syntax on two files. Required PR
CI remains due.

## R1 — P3: the action list's second copies miss the fork rule

`README.md:269` and the `--queue` help (`shoalmark.py:6045`) list every action except `wait: from a fork, read it yourself`.
The docstring's verdict sentence (`shoalmark.py:1650`) still says "among the pull requests' own". The CHANGELOG omits the
verdict hidden through a fork's base (claim 3). The tool prints the wait itself, so no wrong action follows.
**Falsifier:** `grep -n "from a fork" README.md` and `python3 shoalmark.py --help | grep "from a fork"` each print a line.
At `c2027d2` both print nothing. **Fix text:**
- `README.md:269`, between `the oldest first inside each.` and `` `merge` — ``: ``A pull request from a fork — GitHub's
  `isCrossRepository` — reads `wait: from a fork, read it yourself` before every other rule: its commits supply no verdict
  and no carry-over, for it or for any other pull request.``
- `shoalmark.py:6045`: `ONE action each — merge · ` → `ONE action each — wait: from a fork, read it yourself (first) · merge · `
- `shoalmark.py:1650`: `A verdict is a commit among the pull requests' own` → `A verdict is a commit among the
  same-repository pull requests' own and the pushed branches'`
- `CHANGELOG.md:11`, after `work carried into that fork.`: ` Nor can a fork's base hide another pull request's verdict: a
  same-repository pull request reads as it would with no fork open.`

## R2 — P3: no control holds the fork rule ahead of `closes with`, `carried` and a conflict

Claim 2 names contained and conflicting forks, but the six controls exercise only the clean and `answer/*` cases.
**Falsifier:** a mutant keeps forks out of `siblings`, `heads` and `bases` and tests the flag just after `elif paths:`.
It passes all six controls, then reads a contained fork `closes with PR 3` and a conflicting fork `wait: conflict in
base.txt`. The two controls below pass at the tip and fail on both the base and the mutant (harness run above).
**Fix text:** in `test_core.py`, before the closing `gti.configure(ROOT)` of the FM-006 block:

```python
    _qgit("checkout", "-q", "-b", "wraps-fork", _qh)
    (_qr / "own.txt").write_text("own\n"); _qgit("add", "-A"); _qgit("commit", "-qm", "own work on the fork's head")
    _qrows = {p["number"]: (kind, action) for p, kind, action, _ in gti.queue_actions(
        [dict(_qpr, headRefOid=_qh), dict(_qown, number=3, headRefOid=_qgit("rev-parse", "HEAD"))])}
    check("FM-006: a fork inside another PR's head waits for the Owner, never closes with it", _qrows[1] == ("wait", _qwait))
    _qgit("checkout", "-q", "-b", "conflict-fork", _qb)
    (_qr / "base.txt").write_text("fork\n"); _qgit("add", "-A"); _qgit("commit", "-qm", "fork edits base")
    _qcf = _qgit("rev-parse", "HEAD")
    _qgit("checkout", "-q", "--detach", _qb)
    (_qr / "base.txt").write_text("main\n"); _qgit("add", "-A"); _qgit("commit", "-qm", "main edits base")
    _qgit("update-ref", "refs/remotes/origin/main", _qgit("rev-parse", "HEAD"))
    check("FM-006: a conflicting fork waits for the Owner's reading, not on its conflict",
          gti.queue_actions([dict(_qpr, headRefOid=_qcf)])[0][1:3] == ("wait", _qwait))
```

## R3 — P3, pre-existing, outside the diff: a fork still hides a same-repository pushed branch

`pushed_branches` (`shoalmark.py:1389`, `:1397`) is passed every PR, forks included. A fork hides a member's pushed branch
from `--queue` in three ways:
- by giving its own head ref the branch's name;
- by containing the branch's head;
- after the fork PR is closed, when its `refs/pull/N/head` is the branch's SHA. This hide is permanent, because `pulled`
  keeps every PR head ever pushed.

The probe reproduces all three. Each removes only a `branch … wait: no pull request — …` line and never yields merge or
close advice, so this is P3 and not a side-fix for this slice. **Falsifier:** at the tip, with a fork open under the name
`fm/010-pushed`, `pushed_branches` still returns `fm/010-pushed`; it returns only `fm/011-pushed`.
**Fix text:** add one line to FM-006's 2026-09-30 fork-queue entry in *What is true now*: `Left (review R3, pre-existing):
pushed_branches still reads forks — a fork hides a same-repository pushed branch by its head ref's name or by containing
its head, and a closed fork whose refs/pull head is that SHA hides it for good; the fix reads the fork flag there too,
closed pull requests included — its own tags: bug tracker when built.`

## Quality read

The product change is clean. It adds three lines and one filter at the only entry point, before any git read, so nothing
downstream can see a fork SHA. There is no second code path. `rows = forks` then appends to the fork list; that is harmless
and not a finding. The controls sit in `test_core.py`, which runs on every Python commit, and that is the right home for a
security boundary. The forge control fakes gh at the process boundary instead of stubbing `forge_prs`, and that is sound.
R1 and R2 are this slice's only defects; R3 predates it.
