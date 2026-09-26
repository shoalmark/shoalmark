# Review — shoalmark 0.18.4 release cut at df48d67, the second pass

Reviewed: `df48d67d00cb08285f804f3a75b095f05a9efbe9` on
`release/0.18.4`, completed 2026-09-26.

**Tier: code — a release, critical. Verdict: READY.**

## Seat and independence

A cold session started by the Owner under his path line 3. Reviewer session `12a3c0b2`, worktree
`shoalmark-review-release-0184` — the seat of the first pass (`f390baf`, `review-0.18.4-cut.md`,
which stays as it is). That pass's process ended after its verdict commit and before its push;
this session resumed it in the same worktree and seat, pushed `f390baf` unchanged as a fast-forward,
and ran this pass. Independent of the building session `8e509911/implementer-32` in
`shoalmark-impl-4`, which wrote both fix commits. I changed only this review file, fixed nothing
and dispositioned no other seat's finding. The sealed session directory `8b91dba2` was untouched
and outside every command and search scope.

## Scope

- `git fetch origin` resolved `origin/release/0.18.4` to `df48d67`; this worktree was detached
  there. `git diff --name-status 5e79607 df48d67` names only `CHANGELOG.md`, `docs/setup.md`,
  `docs/de/setup.md`, `test_shoalmark.py` and the first pass's review file: two commits,
  `3fe7e3a` (FM-006, R1) and `df48d67` (FM-030, R2), both by `8e509911/implementer-32`. The
  suite and the release make this the code tier.
- `git diff --name-only origin/main...HEAD` names `CHANGELOG.md`, `README.md`, `VERSION`,
  `docs/setup.md`, `docs/de/setup.md`, `docs/signing.md`, `docs/de/signing.md`, `shoalmark.py`,
  `test_shoalmark.py`, the FM-030, FM-031 and FM-037 trackers and `review-0.18.4-cut.md`.
- The first pass's reconciliation at `5e79607` — every 0.18.4 bullet against the commits since
  `v0.18.3`, the three Owner-word times, the pre-cut fixes against `review-0.18.4-fm030-52cfcc7.md`
  R7/R8 and `review-fm-037-the-triage-guard.md` R1/R2 with their suite cases — stands: nothing it
  read has changed except the two CHANGELOG edits below, which I read against their commits.

## The first pass's findings, verified closed

**R1 · P2 (first pass) — closed by `3fe7e3a`.** `docs/setup.md:8` and `docs/de/setup.md:8` now
clone `--branch v0.18.4`, with *the one this page ships with* / *das, mit dem diese Seite
erscheint* in place of *the newest tag*. `uvx zensical build` exits 0 (*No issues found*) and both
`site/setup.html` and `site/de/setup.html` read `git clone --branch v0.18.4`; no built page names
`v0.17.8`. The CHANGELOG gains the FM-006 bullet and the section head names FM-006.

The new suite case, run alone — its committed lines, executed against a scratch export of the tip
with the real `shoalmark.py` imported — on 3.14.3 and on 3.9.6 alike:

| Tree | Result |
|---|---|
| the tip as committed | true |
| English page set back to `v0.17.8` | false |
| German page set back to `v0.17.8` | false |
| German page's `--branch v0.18.4` removed (no tag) | false |
| `VERSION` 0.18.5, pages unchanged — the next cut forgetting them | false |
| a second, stale `--branch v0.17.8` line added to the English page | false |
| `VERSION` 1.0.0 and both pages `v1.0.0` | true |

That reproduces the Implementer's three cases and adds three: the check binds the pages to
`VERSION` in both directions, not just to today's string.

*The placement.* Right: `--check` runs in every consumer repository, which has no
`docs/setup.md`, so a release-consistency rule of this repository belongs beside the suite's two
existing ones (`__version__` is `VERSION`; the CHANGELOG's newest heading is `VERSION`). One
precision on where it bites, not a finding: the commit message says the suite runs *on every commit
through the hook*, but `lefthook.yml`'s `tests` step has `glob: "*.py"`, and a cut commit stages
only `VERSION` and `CHANGELOG.md` (`ac9eadb` did). At the next cut the case therefore fails first
at the Reviewer's suite run and at CI on the ready pull request (`ci.yml`:
`pull_request: {types: [ready_for_review]}`), both before the merge — which is what the binding
needs. The only other `git clone --branch` in the sources is `README.md:218`'s `vX.Y.Z`, a
placeholder. `ADOPT.de.md:27` names `v0.12.0` deliberately, pinned with the file's SHA-256 for a
measurement; it is not on the site and claims no *newest*.

**R2 · P3 (first pass) — closed by `df48d67`.** The case reads the README's `*/5 … --notify`
line, strips cron's five fields, and requires `mkdir -p "$HOME/.local/state/shoalmark" &&` —
derived from the line's own `>>` target — to lead it. Where `/bin/sh` exists it runs the line as
cron does: `/bin/sh -c`, `HOME` a fresh empty folder, `PATH` a stub `python3` first. Run alone it
saw `((0, 'reached: shoalmark.py --notify\n'), (1, None))`: the line writes `notify.log` and
reaches the tool; the line without its `mkdir -p` exits 1 and writes no log. That bare line is
byte for byte the README's cron command at `4efa5a0^` (compared by script), and run by hand under
`env -i` with an empty home it fails with *notify.log: No such file or directory*, exit 1.

*Would it have failed at `4efa5a0^`?* Yes. Against the README at `4efa5a0^` the case is false
on 3.14.3 and 3.9.6, with `/bin/sh` and with its absence simulated (`os.path.exists("/bin/sh")`
false) — the `startswith` clause alone refuses it, and where `/bin/sh` exists the run refuses it
too. A third tree, whose line makes the wrong folder (`mkdir -p "$HOME/.local/state" &&`), is also
false on both. With `/bin/sh` absent the case on the tip is true and its name says *read, not run:
no /bin/sh here, cron's shell* (saw `None`) — the Windows runners' path, honestly named. The
launchd plist is left out with its reason, as `4efa5a0` recorded; I agree.

The CHANGELOG's FM-030 R3–R8 bullet gains the clause, matching the commit.

## Findings

None. Both of the first pass's findings are closed above; the two fix commits add nothing I would
row. The hook's `*.py` glob noted under R1's placement is an observation on where the check bites,
not a defect of this cut — the binding holds before every merge.

## The gate, the hooks, the trackers

- From the cut's parent `ac9eadb^` to `df48d67`, `shoalmark.py`, `lefthook.yml`, `shoalmark.toml`,
  `.github/workflows/ci.yml`, `.github/workflows/docs.yml`, `scripts/` and `zensical.toml` have
  identical blob ids: the cut and everything after it change no gate, hook or CI script.
- Against `origin/main`, `lefthook.yml`, `shoalmark.toml`, both workflows and `scripts/` are
  identical. `shoalmark.py` differs in exactly six top-level functions (by AST, function by
  function) — `answer_reading`, `queue_actions`, `owner_change`, `trusted_signers`, `signers_gap`,
  `unverified` — and the `DUE_SHAPE` constant, all from the three pre-cut commits `4efa5a0`,
  `56767f7`, `62682c8` the first pass verified. `judged_before_build`'s functions (`configure`,
  `build_judgement`, `commit_msg_check`, `parse_args` — the build walk included), the guard's walker
  `guard_walk` and its checks
  (`guarded_sections`, `section_changes`, `guard_verdicts`, `guard_proof`, `guard_why`,
  `guard_lines`, `guard_footer`, `triage_guard`) are byte-identical to main. The guard's signer
  root does pass through `trusted_signers`/`unverified`, changed by `56767f7` — that is the FM-037
  cold re-review's R2 (no signers file on the default branch verifies nothing), verified in the
  first pass with cases failing against the prior tool. `zensical.toml` differs from main only
  because main added the TRIAGE.md page to the nav in PR 85 after the branch; the merge brings it.
- No tracker is changed by either fix commit, and the cut changes no tracker's front matter by
  hand: the front matter of FM-030, FM-031, FM-037, FM-035, FM-036, FM-029 and FM-006 (all In
  Progress) and FM-028 (Proposed) is byte-identical to `origin/main`'s. Their `Shipped` flips are
  the tag's close-out, by the tool or the Owner; the cut manufactures none.
- `--check` reports *judged before build: on — 9 commit(s) … every build commit under a judged In
  Progress tracker*; FM-006 is In Progress, triaged 2026-09-25.

## Suites, gates and integration

The runs began at 09:16 CEST, outside FM-028's 00:00–02:00 CEST window, so no `TZ=UTC`
override was needed.

| Command | Exit | Result |
|---|---:|---|
| `python3 test_shoalmark.py` (3.14.3) | 0 | 462 ok, 0 skipped, all green |
| `python3 test_core.py` (3.14.3) | 0 | 148 ok, all green |
| `/usr/bin/python3 test_shoalmark.py` (3.9.6) | 0 | 462 ok, 0 skipped, all green |
| `/usr/bin/python3 test_core.py` (3.9.6) | 0 | 148 ok, all green |
| `python3 shoalmark.py --check` | 0 | branch gate green |
| `python3 shoalmark.py --session-check` | 0 | session gate green |
| `git diff --check origin/main...HEAD` | 0 | clean |
| `uvx zensical build` | 0 | `No issues found`; both setup pages clone `v0.18.4` |

A fresh clone from origin, detached at `df48d67`, with system and global git config disabled
(`GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=/dev/null`) has no `gpg.ssh.allowedSignersFile`:
`--check` exits 4 with exactly one checkout finding — *it is signed, but this clone cannot
verify*, naming four signed commits (FM-007, FM-024, FM-032, FM-033) — says `INDEX.md is up to
date`, and emits no `STALE`. 0.18.3's C holds.

`--queue` exits 0 and reads `release/0.18.4 @ df48d67  wait: no pull request — no verdict on
df48d67`, as expected before this commit. `origin/main` is `0c3b30d` (PR 85); `git merge-tree
--write-tree origin/main HEAD` exits 0 with tree `d2a0ecd92e8dbf3bfc2a701c71b8f196717fe9f1` —
the branch merges cleanly over PR 85's TRIAGE.md pages, whose one version each is history (*CI went
red on the release tag `v0.18.3`*), not an install path.

## Verdict and handoff

**Verdict: READY.** The first pass's R1 (P2) and R2 (P3) are closed, each with a suite case I ran
alone and saw fail on the defect it names — the pages set back, a tag removed, `VERSION` moved
without them; the cron line without its `mkdir -p`, byte for byte the line at `4efa5a0^` — and
all 1,220 checks are green on both Pythons at `df48d67`. The cut and its tail change no gate, hook
or CI script, and the branch merges cleanly over main at PR 85. The strongest counterfact is the
unrun five-job matrix: Linux runs the R7 case under its own `/bin/sh`, and Windows takes the
case's read-only path — neither is proven here, and the Owner left that proof to the tag.
Readiness reverses if that matrix is red. No pull request is open for `release/0.18.4`; the Owner
opens it, merges, and tags `v0.18.4`; the tag runs the five-job matrix and deploys the site, after
which the Auditor seat gives its final word on FM-037.

the Owner lands this by merging; a merge rules nothing.
