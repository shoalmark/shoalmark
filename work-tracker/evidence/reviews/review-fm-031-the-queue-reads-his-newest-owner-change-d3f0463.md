# Review — FM-031, the RV-710 fix, at d3f0463 (2026-09-28 17:55 CEST, Reviewer, session `8e509911/reviewer-51`)

Reviewed: d3f0463656319dd534debc22bff7a4cbe0a0e3ef

- **Branch:** `fm/031-the-queue-reads-his-newest-owner-change`, tip `d3f0463` (`git fetch origin` at 17:27, no `--prune`:
  `origin/fm/031-…` = `d3f0463`, `origin/main` = `50c3a104`), no pull request. One commit on `d79ffa7b` (the cold verdict):
  `d3f0463` (2026-09-28 16:45:44, the Implementer seat, `8e509911/implementer-54`, pushed 17:25:31).
- **Tier: critical under path line 3** — the change IS the queue's reader of `answer/*` pull requests.
- **Independence: same session** — a sub-agent of Principal session 8e509911 (seat `reviewer-51`). This is the local pass
  before the Owner's cold re-check; that session's verdict counts.
- **Verdict: NOT READY.** The fix does what RV-710 asked wherever the reader can see the commits below his act — every
  shape the cold review and the brief name reads as intended, on both tools, and the suites are green. It does not err to
  a wait where it cannot see them: an `origin/<base>` this clone has not fetched reads *merge: your answer* over a seat's
  commit (RV-711, P2 — the brief's design point, reproduced in two clone shapes). The fix is one guard.

## What changed (d79ffa7 → d3f0463)

An AST diff with docstrings set aside changes `answer_reading`, `parse_args` (the `--queue` help) and `queue_actions`
(`answered_at` → `answer_action`, and its one caller), and adds `answerer_of` and `answers_as_him`; nothing else.

- `answer_action` (shoalmark.py:1420) finds the commit the pull request is read by exactly as `answered_at` did (the same
  `-G "^(answer|done|due):"` line, the same `addenda_only(at, head, None)` fall back to the head), then calls
  `answer_reading(at)`. **A reading that is a wait is returned untouched** (`if action[0] != "merge": return action`) —
  confirmed in the table: rows 4–7 and 14 print the same line on both tools.
- Only where that reading is *merge*: `git rev-list <at> ^origin/<base>` (:1437) lists the pull request's own commits
  below it, merges included, newest first; the first that is neither a review file's only (`addenda_only(c^, c, None)`)
  nor his (`answers_as_him`) turns the line into `wait: a seat's commit on your answer branch (<sha7>, <author>)` — the
  commit and its author (`answerer_of(c)[1]`, the email, else the name) named. The head's reading is not used.
- **The rights gate is the same test as for the head:** `answers_as_him(c)` = `answerer_of(c)`'s `may` (the seat matched
  on email or name, `holds(…, "answer")`; `answerers` by name without `[seats]`) **and** `verified_as(c, email or None)` —
  exactly what `answer_reading` applies to the commit it reads; `answer_reading` now takes `may` and the named author from
  the same `answerer_of`, and its three outcomes are unchanged (the refactor keeps `email or name or 'no author'`).
- One step past the brief, as the seat says: the rule applies to the head reading too — his signed head with a seat's commit
  below (rows 13 and 16) now waits; d79ffa7 read those *merge*. The seat's *the four seat-below checks fail on d79ffa7's
  tool* agrees with rows 8, 9, 10 and 13 (d79ffa7 reads each *merge*); I did not run the tip's test file against d79ffa7's tool.

## What I ran

| run | result |
|---|---|
| `git diff --check d79ffa7b d3f0463` | clean, exit 0 |
| AST diff, docstrings aside (reviewer-47's script) | `answer_reading`, `answerer_of`, `answers_as_him`, `parse_args`, `queue_actions`, `queue_actions.answer_action` / `.answered_at` — nothing else |
| the reproduction (below), 17:47:14–17:51:17 | 17 pull requests, three reader clones, d79ffa7's and d3f0463's tools and a one-guard sketch. A first build (17:32:52) had a defect in my harness's row 6 — its seat helper overwrote the tracker it had just edited; fixed and rebuilt, every row read again; the tables are the rebuild's |
| the PortDive replay (below), 17:38:40–17:38:46 | PR 892 and PR 876, with main's (`50c3a10`), d79ffa7's and d3f0463's tools |
| `python3` 3.14.3 `test_shoalmark.py` (17:30:53–17:42:13, 680 s) | **516 ok / 0 FAIL**, *skipped here: 0 checks — every check ran*, exit 0 — the six `RV-710` checks and the three `RV-679` checks among them |
| `python3` 3.14.3 `test_core.py` (17:42:13–17:42:17, 4 s) | **148 ok / 0 FAIL**, exit 0 |
| `/usr/bin/python3` 3.9.6 `test_shoalmark.py` (17:42:17–17:52:13, 596 s) | **516 ok / 0 FAIL**, *skipped here: 0 checks — every check ran*, exit 0 |
| `/usr/bin/python3` 3.9.6 `test_core.py` (17:52:14–17:52:16, 2 s) | **148 ok / 0 FAIL**, exit 0 |
| the suites' guards | one interpreter at a time; before each run `pgrep -fl '[Pp]ython[0-9.]* [^ ]*test_(shoalmark\|core)\.py'` printed nothing and the 1-minute load was under 6 (3.16, 5.06, 5.06, 4.70), the HEAD `d3f0463` and the tree clean; each output whole in the Reviewer's scratch folder. My rebuilt reproduction (17:47:14–17:52:46) ran beside run 3's last five minutes and run 4 — load only; both green |
| `python3 shoalmark.py --check` (17:53:10–17:53:43) | exit 0 — *INDEX.md is up to date — 40 trackers*; *judged before build: on — 4 commit(s) on a detached HEAD since origin/main, every build commit under a judged In Progress tracker*; *the Owner's two sections: guarded — … none changes them or his signers file*; *filing freeze: 21 open* |
| `python3 shoalmark.py --session-check` (17:53:43) | exit 0 |
| `git merge-tree --write-tree origin/main HEAD` (`50c3a104`, 17:40:02) | exit 1 — **CONFLICT in `CHANGELOG.md` only** (both add under `## Unreleased — 0.18.6`), the known one; `README.md`, `shoalmark.py`, `test_shoalmark.py` auto-merge; the merged `shoalmark.py` compiles and keeps `answer_action` |
| `--queue` (the tip's tool, live, 17:53:50–17:53:56, exit 0) | `branch fm/031-the-queue-reads-his-newe… @ d3f0463  wait: no pull request — conflict in CHANGELOG.md` |

## The reproduction — a scratch repository, a bare `origin`, `gh` stubbed, his commits SSH-signed

reviewer-47's harness, widened to 17 pull requests (`mk51.py` in the Reviewer's scratch folder; it rebuilds in 15 s).
`--queue` read in a **full clone** of the scratch `origin` with d79ffa7's tool (= 8409c9a's `shoalmark.py`) and d3f0463's,
each extracted with `git archive`. Row 15 is made by the tool itself (below, RV-712).

| PR | branch shape (oldest first) | d79ffa7 | d3f0463 |
|---|---|---|---|
| 1 | his signed `answer:` + review | merge: your answer, signed be91e1f | the same |
| 2 | his signed `done:` + review (RV-679) | merge: your answer, signed 13d9b0d | the same |
| 3 | his signed `due:` + review (RV-679) | merge: your answer, signed 2fb9437 | the same |
| 4 | his `done:` + a seat's code **above** it | wait: not an answerer (impl@seat) — the head | the same |
| 5 | his `done:` + a review quoting `done:` at a line start | wait: not an answerer (reviewer@seat) | the same |
| 6 | his `done:` + review + a seat's body change + review | wait: not an answerer (reviewer@seat) — the head | the same |
| 7 | a seat's `done:` + review | wait: not an answerer (impl@seat) | the same |
| 8 | **a seat's code, his signed `done:`, review — the cold review's shape** | **merge: your answer, signed 8d13f46** | **wait: a seat's commit on your answer branch (4eb6ace, impl@seat)** |
| 9 | a seat's code, his signed `answer:`, review (RV-735) | **merge: your answer, signed cb352ad** | **wait: … (3fd2961, impl@seat)** |
| 10 | a seat's code, his signed `due:`, review | **merge: your answer, signed ea9f15d** | **wait: … (c4d5525, impl@seat)** |
| 11 | his `--due`, then his `--done`, review | merge: your answer, signed 80a71c5 (the `done:`) | the same |
| 12 | a review file's commit **below** his `done:`, review | merge: your answer, signed ac25fc6 | the same |
| 13 | a seat's code, his signed `done:` as the head | **merge: your answer, signed 14f49de** | **wait: … (181fa71, impl@seat)** |
| 14 | a seat's code below **and** above his `done:` | wait: not an answerer (s@s) — the head | the same |
| 15 | **the tool's own refusal record (his, unsigned), his signed `due:`, review** | merge: your answer, signed b33d898 | **wait: a seat's commit on your answer branch (0fe5b10, owner@x)** — RV-712 |
| 16 | stacked on a seat's pushed branch `fm/seat-base`: a seat's code, his signed `done:` as the head | **merge: your answer, signed 32d11b8** | **wait: … (89e6277, impl@seat)** |
| 17 | a seat's code, his signed `done:`, review (row 8's twin, for the second single-branch reader) | **merge: your answer, signed a046929** | **wait: … (c0e971a, impl@seat)** |

The same 17 read by clones that have **not fetched a base** (RV-711) — each a `git clone --single-branch` of the scratch
`origin`, whose `remote.origin.fetch` covers its one branch, exactly as `forge_prs` then fetches it:

| reader | PR | d79ffa7 | d3f0463 | the one-guard sketch |
|---|---|---|---|---|
| `--single-branch -b main` — `origin/fm/seat-base` never fetched | 16 (base `fm/seat-base`) | merge: your answer, signed 32d11b8 | **merge: your answer, signed 32d11b8** — over 89e6277 (impl@seat) | wait: origin/fm/seat-base is not here — the commits below 32d11b8 unread |
| the same | the other 16 | as the full clone | as the full clone | as the full clone |
| `--single-branch -b fm/seat-base` — `origin/main` never fetched | 13 (base `main`) | merge: your answer, signed 14f49de | **merge: your answer, signed 14f49de** — over 181fa71 (impl@seat) | wait: origin/main is not here — the commits below 14f49de unread |
| the same | 16 (its base fetched here) | merge: your answer, signed 32d11b8 | wait: … (89e6277, impl@seat) | the same |
| the same | 1–12, 14, 15, 17 | read by the head (the `-G` log fails): wait: not an answerer (reviewer@seat), (impl@seat) on 4, (s@s) on 14 | the same | the same |

The sketch — `rev-list`'s exit read, a wait where it is not 0 — moves no row in the full clone.

## The words

- README §5, the refusals table: a row for `wait: a seat's commit on your answer branch (<sha>, <author>)` (`--queue`) right
  after `wait: not an answerer (<author>)` — what it means and *do not merge it; close it, and give the act again from the
  default branch* (RV-713 on that last clause). The *what to merge* row: *`merge: your answer` when … the commit verifies,
  and every commit of its own below that one is his too, by the same test, or a review file's only — else `wait: a seat's
  commit …`, the first such below his*. Both true to the code.
- `--queue`'s help (shoalmark.py:5630) lists the new wait between *not an answerer* and *unsigned answer*.
- CHANGELOG, under `## Unreleased — 0.18.6`: one bullet naming RV-710 (*the Owner's cold review of `3bb53ec`, P1, `d79ffa7`
  at 14:59:48*) and RV-735 (*the local pass's*); true to the code, save *an `answer/*` pull request that now waits carries
  a commit that is not his* (RV-712) and its way out (RV-713).
- FM-031: the RV-710 paragraph under *Open lines*, after RV-679's; the ship-log row `2026-09-28 16:45 CEST` sits at the top
  of the newest-first table, above RV-679's 09:12 row. `docs/` and `docs/de/` name no queue reading — nothing left unwidened.

## The PortDive replay — read-only, no fetch in PortDive

As reviewer-47's: `git clone --shared --no-checkout` of `/Users/hf./Documents/portdive/worktrees/principal-2` into scratch,
its `origin` repointed to a scratch bare repository whose `objects/info/alternates` names PortDive's object store, its refs
set with `update-ref` (the remote-tracking refs the clone brought deleted first), checked out detached at the merge's first
parent, `gpg.ssh.allowedSignersFile` = `docs/work-tracker/allowed_signers`; the tools run with `--root <clone> --queue`
through the five-line driver (`github_remote` true, `gh` a stub printing the one pull request).

- **PR 892** — `gh pr view 892 --repo holgo99/portdive-monorepo --json commits` (17:37:24): his signed `--answer PD-404`
  `8dd509a7` (12:00:30Z), then three of the other session's commits ABOVE it: `0d4a77e1` and `bcf89df0` (principal@seat),
  `f1fc0c0c` (reviewer@seat, the head, a review file only); `main` at `78f8114c` (the merge's first parent):
  - main's tool (`50c3a10`): `PR 892  wait: not an answerer (principal@seat)  answer/pd-404 @ f1fc0c0`
  - d79ffa7's: the same · d3f0463's: the same.
  It is **not read by the head**: `-G` matches removed lines too, and `bcf89df0` — the Principal's commit that moved the
  exchange under `## Asks` — removed his `answer:` line; it is the newest match, only the review `f1fc0c0c` follows it, so
  all three tools read `bcf89df0` and wait on its author. A wait before the new rule is reached; nothing changes.
- **PR 876** — his signed `--due` `5f307d34` under the verdict `28808f42`; `main` at `f5bc3a6b`:
  - main's tool (`50c3a10`): `PR 876  wait: not an answerer (reviewer@seat)  answer/bug-327 @ 28808f4`
  - d79ffa7's: `PR 876  merge: your answer  answer/bug-327 @ 28808f4  signed 5f307d3`
  - d3f0463's: `PR 876  merge: your answer  answer/bug-327 @ 28808f4  signed 5f307d3` — unchanged from reviewer-47's replay.

## Findings

**RV-711 · P2 · confidence 99% on the mechanism (reproduced in two clone shapes), ~80% on the grade — the reader errs to
*merge* where it cannot see the commits below his act.** `answer_action` lists them with `git rev-list <at>
^origin/<base>` (shoalmark.py:1437) and reads only its stdout. Where `origin/<base>` does not resolve, git exits 128
(`fatal: bad revision '^origin/fm/seat-base'`), stdout is empty, `below` is `[]`, and the line stays *merge: your answer*;
the `-G` log fails the same way, so `at` is the head, and a head that is his signed act over a seat's commit reads merge
(PR 16 and PR 13 above). **The base can be unresolvable when `gh` reported the pull request:** `forge_prs` fetches the
clone's configured refspecs and each `refs/pull/N/head`, nothing more — a single-branch clone's refspec covers one branch,
as `pushed_branches` says in its own words (*a single-branch clone fetches one*), and `queue_actions` already drops bases
that do not resolve from its verdict walk (`bases`, :1395). The seat's grading — *the same leniency `own()` already has* —
does not hold here: `own()`'s empty list errs to *not carried* (a close line not printed); this one errs to a merge, in the
critical reader. Not introduced relative to d79ffa7 (which read the head, merge), but the fix's own contract — *merge only
where every commit below is his* — is void, silently, exactly where the reader is blind. Rare in this estate (his clone is
full, his answer pull requests target `main`), which is why P2 and not P1. **Fix, one guard, in the same slice:** where
that `rev-list` does not exit 0, return a wait — e.g. `wait: origin/<base> is not here — the commits below <sha7> unread`;
reproduced as a sketch in scratch (never committed): PR 16 and PR 13 wait in the single-branch readers, no other row moves
in any reader. Plus one check: a pull request whose `baseRefName` the clone has not fetched, his signed act over a seat's
commit, reads a wait.

**RV-712 · P3 · confidence 99% on the mechanism (the tool made the shape), ~65% on the grade — the tool's own refusal
record under his act now reads as "a seat's commit", naming him.** `record_refusal` (FM-030, the E0 counter's row 20,
:1898) commits ONE line under `## Acts` on `answer/<id>` — unsigned by design (`--no-gpg-sign`), authored by him — and
pushes it; `unmerged_advice` then sends his next act onto that branch: *it commits on top*. Row 15 was made by the tip's
own `--due`, refused once after the cut by a scratch pre-commit hook: `0fe5b10` (Owner <owner@x>, `%G?` N), then the same
`--due` again on `answer/ap-015`, signed `b33d898`, a verdict on top. d79ffa7: `merge: your answer … signed b33d898`;
d3f0463: `wait: a seat's commit on your answer branch (0fe5b10, owner@x)`. `answers_as_him` rightly refuses an unsigned
commit (a seat can write his name), so the reading errs to a wait — the safe side — but it is introduced here, in a flow
the tool designs, and it misnames his own record as a seat's; the CHANGELOG bullet's *carries a commit that is not his* is
false for it. Graded P3: no refusal record exists in PortDive's history yet (`git log --all -E --grep='^[A-Z]+-[0-9]+:
--(due|done|answer) refused'`: none). **Fix, same round:** at least name it — an author who may answer, unsigned: `wait: an
unsigned commit of yours on your answer branch (<sha>)`; or admit a commit exactly as `record_refusal` writes it (his author,
one added `## Acts` line `… refused — …`, no front-matter key) — the design the Principal's; one check either way.

**RV-713 · P3 · confidence 99% on the mechanism, ~60% on the grade — the new wait's way out cannot be followed.** README's
new row and the CHANGELOG say: *do not merge it; close it, and give the act again from the default branch*. From `main`,
the tip's `--done AP-008 evidence/x.md` refuses: *`answer/ap-008` exists and is not merged into `origin/main` — it carries
your commit(s) — … merge it first (its pull request), then `--done …`; or `git switch answer/ap-008` and run it there*; its
`--due AP-010 …`: *`git switch answer/ap-010`, then `--due …` — it commits on top* (17:51:42). Run there, the seat's commit
stays below and the line still waits; *merge it first* is the very merge the wait refuses. The only way out — deleting
`answer/<id>` on `origin` and locally — no line names. **Fix, same round:** the README row and the CHANGELOG name it
(`git push origin --delete answer/<id>` · `git branch -D answer/<id>`, then the act again from the default branch), and
`unmerged_advice` stops saying *merge it first* for a branch that carries a commit not his (the same `answers_as_him` test).

**RV-714 · P2 against the merge of main — not this tip · confidence 99% on the mechanism, ~75% on the grade — after the
merge, the board says *your merge is next* where `--queue` waits.** Main's board build (PR 113, `on_their_way`) says what
`--queue` reads of an unmerged `answer/*` branch by `answer_reading(commit)[1]` alone. With the auto-merged `shoalmark.py`
(tree `a075a00`, 17:52:14), `--owner` in the full-clone reader prints, in ONE output, *AP-008 … · signed · your merge is
next* above its own queue line *PR 8  wait: a seat's commit on your answer branch (4eb6ace, impl@seat)* — the same for
AP-013, AP-015, AP-016, AP-017. On main today (`50c3a10`) the board says *your merge is next* there too, and main's queue
reads PR 13 and PR 16 *merge: your answer* — RV-710's false merge in the Owner's other surface, unreleased (0.18.6). **Fix:**
the merge of main this branch needs carries the rule into `on_their_way` (one reader: the `said` from `answer_action`'s
test, or the same below-walk against `origin/<default>`), with a check; the merge's scoped re-check runs row 8 on the board.

No P1 found. RV-715…719 not used.

## For the Owner's cold re-check

- **What changed since d79ffa7:** one commit, `d3f0463`. `answered_at` became `answer_action` (shoalmark.py:1420): the
  same commit is found and read; only a *merge* reading is then checked against every commit of the pull request's own
  below it (`git rev-list <at> ^origin/<base>`, :1437) — each must be his (`answers_as_him`: may answer and verifies as
  him, the gate's one test) or a review file's only, else `wait: a seat's commit on your answer branch (<sha>, <author>)`.
  A wait is never changed. Six checks, a README row and the *what to merge* row, the `--queue` help, a CHANGELOG bullet,
  FM-031's RV-710 line and a ship-log row (the table is newest first; the row sits at its top).
- **Ten minutes to reproduce:** (1) `git diff d79ffa7b d3f0463 -- shoalmark.py` — read :1432–1439; (2) `python3
  test_shoalmark.py | grep RV-710` — six `ok` (the whole run ≈11 minutes); (3) RV-711: in any scratch repository with a
  bare `origin`, push a seat's branch `fm/x`, cut `answer/y` from it, a seat's commit and his signed `done:` on top, push;
  `git clone --single-branch -b main <origin> r`; `gh` stubbed to one pull request `answer/y` with `baseRefName` `fm/x`;
  `--root r --queue` prints `merge: your answer … signed <his>`; a full clone prints `wait: a seat's commit …`. My harness
  (`mk51.py`, `drv.py`, `ghbin/` in the Reviewer's scratch folder) builds all 17 rows and three readers in 15 s.
- **Judge:** whether RV-711 is P2 (my grade: the error's direction in the critical reader outweighs its rarity) and whether
  RV-712/RV-713 belong in the same round (my advice: yes, they are small and on the same line).

## Verdict

**NOT READY** on `d3f0463`. RV-710's shape — a seat's commit, his signed `done:` or `due:`, a verdict on top — now waits and
names the seat's commit, as do the `answer:` twin (RV-735's row 9) and his signed act as the head; his stacked acts, a review
below his act, and both RV-679 cases still read *merge: your answer*; every wait is unchanged; PortDive's PR 876 reads
merge and PR 892 waits (on `bcf89df0`'s author), on d79ffa7 and d3f0463 alike. The suites are green on both Pythons, 516 +
148, 0 skipped. But the reader still errs to *merge* where it cannot see below his act (RV-711, P2): one guard and one
check. RV-712 and RV-713 are P3 and belong in the same round; RV-714 is the merge of main's to close.

Confidence that the Owner's cold session finds nothing blocking: **~40% on `d3f0463` as it stands** — RV-711 is the kind of
failure-direction point the cold review of 3bb53ec found; **~80% once RV-711's guard and check land** — the residual a cold
reader grading RV-712 or RV-713 up (~12%) and what a cold reading finds that a same-session one does not (~8%).

Path 5 — a merge rules nothing.
