# Review — shoalmark 0.18.4 release cut at 5e79607

Reviewed: `5e796075ac7a7f8cfa01e8f4eee06f73de26141c` on
`release/0.18.4`, completed 2026-09-26.

**Tier: code — a release, critical. Verdict: NOT READY.**

## Seat and independence

A cold session started by the Owner under his path line 3. Reviewer session `12a3c0b2`,
worktree `shoalmark-review-release-0184`; independent of building session
`8e509911/implementer-31` in `shoalmark-impl-4`. The four cold-start answers: provide
adversarial pressure; guard against making severity the result; use the release's runnable
claims, negative cases and source-to-changelog reconciliation to expose that shadow; hand this
record to the Owner. I changed only this review file, fixed nothing and dispositioned no other
seat's finding. The sealed session directory `8b91dba2` was untouched and outside every command
and search scope.

## Scope and reconciliation

- `git fetch origin` resolved both detached `HEAD` and `origin/release/0.18.4` to
  `5e796075ac7a7f8cfa01e8f4eee06f73de26141c`. `git diff --name-only
  origin/main...HEAD` named `CHANGELOG.md`, `README.md`, `VERSION`, both signing pages,
  `shoalmark.py`, `test_shoalmark.py`, and the FM-030, FM-031 and FM-037 trackers. The tool,
  tests and release artifact make this the code tier.
- I read the non-tracker history from `v0.18.3` through the tip and reconciled it to every
  0.18.4 bullet. The section names FM-030 A–G and R1 plus R3–R8, FM-036 F, FM-029 G,
  FM-031's verdict/addenda and answer-commit queue fixes, FM-035's three CI fixes and open R3,
  FM-037's seven clauses, AU-19/AU-20 and cold-review R1/R2, and FM-028 in the closing list.
  The three Owner-word times are present exactly: 13:33:29, 18:25:16 and 18:55:33.
- `VERSION` and the release heading both read `0.18.4`. `python3 shoalmark.py
  --html-only` renders the board and tracker views with the running line `v0.18.4`, linking to
  the matching release tag. The documentation site is the exception recorded as R1.
- The cut commit `ac9eadb` changes only `CHANGELOG.md` and `VERSION`; it changes no tracker
  front matter by hand. The later merge `5828d90` brings FM-028's already-reviewed tracker
  evidence from main, and `5e79607` changes only the closing changelog line. The bundled
  trackers therefore remain in their existing states on the cut; their eventual `Shipped`
  transitions are not manufactured by this commit and remain the tag/Owner close-out step.
- Byte for byte from `ac9eadb^` to `ac9eadb`, and again from `ac9eadb` to the reviewed tip,
  `shoalmark.py`, `test_shoalmark.py`, `lefthook.yml`, `.github/workflows/ci.yml` and
  `shoalmark.toml` are identical. Thus the cut and its tail alter neither
  `judged_before_build`, the commit walker, FM-037's guard checks nor any hook or CI script.

## Pre-cut fixes

- `4efa5a0` closes FM-030 R7 in the README: the cron entry creates
  `$HOME/.local/state/shoalmark` before the shell opens `notify.log`. It closes R8 in code:
  the offset-minute pattern is `[0-5]\d`; `+05:99` and `-00:60` are refused while `+05:59`
  and `-00:30` pass. The suite has the R8 case. R7's missing case is R2 below.
- `56767f7` closes the FM-037 cold review's R1 and R2. The suite proves that `--answer`
  verifies against the default branch's signers file and does not push a key-rotation answer
  before that file lands; it also proves that, where main has no signers file, a checkout on a
  vouching branch cannot make another branch verify. Both cases fail against the prior tool.
- `62682c8` makes an answer branch read the commit that wrote `answer:` where only review files
  follow it. Its suite case covers both that positive path and a non-review commit after the
  answer, which continues to be read by its head.
- `python3 shoalmark.py --schema` exits 0 and shows the release's `due:`, `window:`, `done:`
  and `[paths] reviews` entries. The English and German signing pages state FM-037's default-
  branch root of trust and tier-0 limit consistently.

## Findings

**R1 · P2 · confidence 99% — the published setup pages install 0.17.8 as “the newest tag”.**

`docs/setup.md:8` and `docs/de/setup.md:8` both say to clone `--branch v0.17.8`, and label it
the newest tag. `uvx zensical build` succeeds but reproduces those exact stale commands in
`site/setup.html` and `site/de/setup.html`. Zero source or built documentation pages contain
`v0.18.4`; only the generated tracker board does. A person following the release site's
ten-minute setup therefore installs a release four cuts behind the one this branch publishes.
That contradicts the cut's version claim and the brief's required site running version.

*Fix named:* update both setup pages to `v0.18.4`, rebuild the site, and add a release check
that binds both advertised clone tags to `VERSION`, so the next cut cannot pass while the
installation command remains stale. Close when both source and built pages name `v0.18.4` and
the check fails when either is changed back.

**R2 · P3 · confidence 99% — FM-030 R7 has no suite case.**

The brief requires a suite case for each pre-cut finding fix. `4efa5a0` changes README,
`shoalmark.py`, `test_shoalmark.py` and FM-030, but its only added `check(...)` is explicitly
FM-030 R8. A scoped search of both suites finds no `mkdir -p`, `notify.log`, cron-line or R7
case. The commit message records a one-time manual empty-`HOME` probe, so the corrected line is
credible, but no regression witness ships with it.

*Fix named:* add a suite case that takes the documented cron command's state/log preparation,
runs it with a fresh empty `HOME`, and proves the log is created and the notification command is
reached; make the same case fail when the `mkdir -p` precondition is removed.

## Suites, gates and integration

The runs began at 07:26 CEST, outside FM-028's 00:00–02:00 CEST window, so no `TZ=UTC`
override was needed.

| Command | Exit | Passing checks | Browser skips |
|---|---:|---:|---:|
| `python3 test_shoalmark.py` (3.14.3) | 0 | 460 | 0 |
| `python3 test_core.py` (3.14.3) | 0 | 148 | — |
| `/usr/bin/python3 test_shoalmark.py` (3.9.6) | 0 | 460 | 0 |
| `/usr/bin/python3 test_core.py` (3.9.6) | 0 | 148 | — |
| `python3 shoalmark.py --check` | 0 | branch gate green | — |
| `python3 shoalmark.py --session-check` | 0 | session gate green | — |
| `git diff --check origin/main...HEAD` | 0 | clean | — |
| `uvx zensical build` | 0 | `No issues found` | — |

Every suite ended `all green`; both functional runs ended `skipped here: 0 checks — every
check ran`. A fresh full clone checked out at the release tip with system and global git config
disabled had no `gpg.ssh.allowedSignersFile`: `--check` exited 4 with exactly one checkout
finding naming four signed commits, said `INDEX.md is up to date`, and emitted no `STALE`.

`--queue` exits 0 and reads `release/0.18.4 @ 5e79607` as pushed without a pull request and
without a verdict, as expected before this commit. Origin main advanced after the brief through
PR 85 to `0c3b30d`; `git merge-tree --write-tree origin/main HEAD` exits 0 and produces tree
`ff3e3d1d215325fb766b3c877e1a0b156d7768be`, so the reviewed tip still merges cleanly.

## Verdict and handoff

**Verdict: NOT READY.** R1 is a P2 release defect, so the code-tier full loop must return to the
Implementer. The strongest counterfact is that the executable artifact, generated board,
gates and all 1,216 checks are green and the changelog reconciles; the published install path
still sends a new user to 0.17.8, and the explicit R7 regression witness is absent. The unresolved
environmental unknown is the five-job CI matrix deliberately left to the eventual tag. Readiness
reverses when R1 and R2 are fixed, the complete local matrix remains green, and an independent
Reviewer verifies the new tip. The Owner alone opens and merges the pull request and tags
`v0.18.4`; the tag runs the five-job matrix and deploys the site, after which the Auditor gives
its final FM-037 word.

the Owner lands this by merging; a merge rules nothing.
