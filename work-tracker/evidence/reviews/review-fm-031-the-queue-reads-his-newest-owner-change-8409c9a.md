# Review — FM-031, the queue reads his newest owner change, at 8409c9a (2026-09-28 14:10 CEST, Reviewer, session `8e509911/reviewer-47`)

Reviewed: 8409c9a6908558ecff0534d7de32200c56d0fc5d

- **Branch:** `fm/031-the-queue-reads-his-newest-owner-change`, tip `8409c9a` (confirmed by `git ls-remote` at 13:45:40),
  no pull request. One commit off `02f3c5c9`: `8409c9a` (2026-09-28 09:12:42, the Implementer seat, `8e509911/implementer-51`).
  At my fetch (12:43:50) `origin/main` was `9e9fcb33` (PRs 108–112): `shoalmark.py`, `test_shoalmark.py`, `test_core.py`,
  `lefthook.yml` and `vendor/` are byte-identical between `02f3c5c` and `9e9fcb3` (`git diff --quiet` and the blob ids) —
  main had moved by 13 tracker and review files only, none in this review's code scope. **Since 13:35:21 `origin/main` is
  `fa9e9ac`, PR 113 — the board build** (`fm/030-the-board-reads-his-unmerged-acts` @ `6e566c1`; `shoalmark.py` +309,
  `test_shoalmark.py` +337): this branch now conflicts with main in `CHANGELOG.md` — the known conflict, the second to land
  merges main — so its merge of main is a new head (below, *Main moved*).
- **Tier: critical under path line 3** — the change IS the queue's reader: `answered_at`, nested in `queue_actions`.
- **Independence: same session** — a sub-agent of Principal session 8e509911 (seat `reviewer-47`), resuming the paused
  draft of `reviewer-43` (09:43). This is the local pass before the Owner's cold session; that session's verdict counts.
- **Verdict: READY WITH FINDINGS.** Two P3s, both forward: RV-735 (not introduced here) and RV-739 (a test gap). No P2.

## What changed

One expression. `answered_at` (shoalmark.py:1412) reads an `answer/*` pull request by
`git log -1 --format=%H -G <needle> <head> ^<base> -- <tracker dir>`, where only review addenda follow the commit it finds, else
by the head; the needle goes from `"^answer:"` to `"^(answer|done|due):"`. An AST diff with docstrings set aside changes
`answered_at` alone. The rest is words: the docstrings of `answer_reading`, `queue_actions` and `answered_at`; README §5's
`wait: not an answerer` row and its *what to merge* row; a CHANGELOG bullet under `## Unreleased — 0.18.6`; FM-031's RV-679
paragraph and a ship-log row (newest first, as FM-031's table runs); and three checks in `test_shoalmark.py`. The `--queue`
help and `--schema` name no answer commit; `docs/` and `docs/de/` say nothing of the reading — nothing left unwidened.
git compiles a `-G` needle as an extended regex (`REG_EXTENDED | REG_NEWLINE`) and matches it against each added or removed
line after its `+`/`-`: `^` anchors at the line's start, the alternation reads as intended, and `answered:` and
`answered-by:` do not match.

## What I ran

| run | result |
|---|---|
| `git log --oneline origin/main..8409c9a` | one commit, `8409c9a`, off `02f3c5c9` |
| byte identity `02f3c5c` → `9e9fcb3` | identical: shoalmark.py `ed2cf2b`, test_shoalmark.py `786226d`, test_core.py `b07d78c`, lefthook.yml `0adc040`, vendor/ tree `697ffcc` |
| `git merge-tree --write-tree origin/main 8409c9a` (`9e9fcb33`) | clean, tree `e76e650`, exit 0. Against `fm/030-the-board-reads-his-unmerged-acts` @ `6e566c1`: a conflict in `CHANGELOG.md` only, both adding under `## Unreleased — 0.18.6` — known, not a finding; the second to land merges main |
| `git diff --check 02f3c5c9 8409c9a` | clean |
| `python3 shoalmark.py --check` (12:49:40–12:50:36 on `9e9fcb3`; again 14:07:30–14:08:02 on `fa9e9ac`) | exit 0 both times — *INDEX.md is up to date — 40 trackers*; *judged before build: on — 1 commit(s) on a detached HEAD since origin/main, every build commit under a judged In Progress tracker*; *the Owner's two sections: guarded — … none changes them or his signers file*; *filing freeze: 21 open* |
| `python3 shoalmark.py --session-check` (12:50:36; 14:08:02) | exit 0 both times |
| `git merge-tree --write-tree fa9e9ac 8409c9a` (the new main, 13:45) | CONFLICT in `CHANGELOG.md` only; `shoalmark.py`, `test_shoalmark.py` and `README.md` auto-merge |
| the nine-row reproduction (below), main's tool and the tip's, 12:51:45 and 12:51:55 | as the table; identical to `reviewer-43`'s run of 09:40 |
| the PortDive replay (below), 12:48:46–12:49:07 | the two shapes as expected |
| `python3` 3.14.3 `test_shoalmark.py` (13:29:33–13:40:37, 664 s) | **510 ok / 0 FAIL**, *skipped here: 0 checks — every check ran*, exit 0 — the three `0.18.6 · RV-679` checks among them |
| `python3` 3.14.3 `test_core.py` (13:49:39–13:49:42, 3 s) | **148 ok / 0 FAIL**, exit 0 |
| `/usr/bin/python3` 3.9.6 `test_shoalmark.py` (13:49:42–14:01:40, 718 s) | **510 ok / 0 FAIL**, *skipped here: 0 checks — every check ran*, exit 0 |
| `/usr/bin/python3` 3.9.6 `test_core.py` (14:06:41–14:06:44, 3 s) | **148 ok / 0 FAIL**, exit 0 |
| the suites' guards | one interpreter at a time; before each run no Python process running a suite file (`pgrep -fl '[Pp]ython[0-9.]* [^ ]*test_(shoalmark\|core)\.py'`) and a 1-minute load under 6, else `sleep 60` and re-check. Run 1's last 92 s overlapped a suite the Principal's pre-commit hook started at 13:39:05 in `shoalmark-review-2`, on a merge of main into another branch (killed at 13:44); run 1 is green regardless, and only its time is affected. Each output is kept whole in the Reviewer's scratch folder |
| `--queue` (the tip's tool, live, 14:07:02–14:07:10) | `branch fm/031-the-queue-reads-his-newe… @ 8409c9a  wait: no pull request — conflict in CHANGELOG.md` — the conflict with `fa9e9ac`; no pull request yet |

## The reproduction — a scratch repository, `gh` stubbed, a bare `origin`, SSH-signed owner commits

`--queue` by main's `shoalmark.py` (`9e9fcb3`) and by the tip's (`8409c9a`), each extracted with `git archive`:

| PR | branch shape | main | tip |
|---|---|---|---|
| 1 | his signed `answer:` + a Reviewer's review-file commit | merge: your answer, signed c8a2362 | the same |
| 2 | his signed `done:` + review (RV-679) | **wait: not an answerer (reviewer@seat)** | **merge: your answer, signed e6d0be2** |
| 3 | his signed `due:` + review | **wait: not an answerer (reviewer@seat)** | **merge: your answer, signed 1b93462** |
| 4 | his signed `done:` + a seat's code commit on top | wait: not an answerer (impl@seat) — the head | the same |
| 5 | his signed `done:` + a review whose file quotes `done: "…"` at a line start | wait: not an answerer (reviewer@seat) | the same — the review commit is the newest match: a wait, never a false merge |
| 6 | his `done:` + review + a seat's tracker-body change + review | wait: not an answerer (reviewer@seat) — the head | the same |
| 7 | a seat's `done:` (not his) + review | wait: not an answerer (reviewer@seat) | wait: not an answerer (**impl@seat**) — the act's author named |
| 8 | a seat's code commit, THEN his signed `done:`, + review | wait: not an answerer (reviewer@seat) | **merge: your answer, signed f41fe64** — RV-735 |
| 9 | a seat's code commit, THEN his signed `answer:`, + review | merge: your answer, signed 47aaa84 | the same — RV-735, since 0.18.4 |

Rows 2 and 3 are the fix; rows 1, 4, 6 and 9 do not move; row 7 names a different non-answerer, still a wait.

## The PortDive replay — read-only, no fetch in PortDive

A `git clone --shared --no-checkout` of `/Users/hf./Documents/portdive/worktrees/principal-2` in scratch; its `origin`
repointed to a scratch bare repository whose `objects/info/alternates` names PortDive's object store, its refs set with
`update-ref` from the objects — no push, no fetch from PortDive. `gpg.ssh.allowedSignersFile` set as PortDive's clone sets it
(`docs/work-tracker/allowed_signers`; the tool reads the default branch's copy). The tools: shoalmark's own `shoalmark.py`
and `vendor/` from `9e9fcb3` and from `8409c9a`, run with `--root <the clone> --queue` through a five-line driver that sets
`github_remote` true (the scratch `origin` is a local path), `gh` a stub printing the one open pull request, the clone's own
`shoalmark.toml` (PortDive's `[seats]`). PortDive pins 0.18.5; its vendored tool ran once, as a control.

- **PR 876's shape** — his `--due` `5f307d34` (2026-09-28 08:25:42, signed, `%G?` G) with the Reviewer's verdict `28808f42`
  on top, as `gh pr view 876 --json commits` lists them; `main` at `f5bc3a6b` (the merge's first parent); a local
  `answer/bug-327` at `28808f42`:
  - main's tool: `PR 876  wait: not an answerer (reviewer@seat)  answer/bug-327 @ 28808f4`
  - the tip's: `PR 876  merge: your answer  answer/bug-327 @ 28808f4  signed 5f307d3`
- **PR 866's shape, the RV-679 case itself** — his `--done` `c502c7a4` (2026-09-27 20:21:18, signed) under the verdict
  `66884f5f` (20:45:02); `main` at `6eff0822` (the merge's first parent, 20:48:08):
  - main's tool: `PR 866  wait: not an answerer (reviewer@seat)  answer/bug-327 @ 66884f5`
  - the tip's: `PR 866  merge: your answer  answer/bug-327 @ 66884f5  signed c502c7a`
  - PortDive's pinned 0.18.5: `PR 866  wait: not an answerer (reviewer@seat)  answer/bug-327 @ 66884f5` — RV-679 as filed.

Neither verdict file carries a line starting `answer:`, `done:` or `due:`, so row 5's edge does not bite either branch.

## Main moved — what the merge of main brings

`fa9e9ac` (PR 113) makes four callers of `owner_change`: `--answer`, `--done`, `--due`, and the new `--revoke`, which drops
`done:` (or, as `--answer … revoke`, changes `answer:`). `-G` matches removed lines as well as added ones, so the needle
`^(answer|done|due):` covers all four after the merge; nothing on main calls for a wider one. The board's own reader of
`answer/*` branches (`fa9e9ac` ≈1168) takes the newest commit per key with `-G line_regex(key)`, scoped to **the tracker's
own file**; the queue's `answered_at` is scoped to **the whole tracker directory**. So row 5's edge exists in the queue's
reading only. Scoping it to the tracker file would remove the edge, and that is a forward option, not a finding here. The
merge of main this branch needs is a new head. It brings the board build's code under this reader, so it takes a scoped
re-check with both suites on both Pythons before it lands.

## Findings

**RV-735 · P3 · forward, not introduced here; its fix its own slice · confidence high (~90%) on the mechanism.** An
`answer/*` pull request is read by ONE commit — his newest `answer:` (now also `done:` or `due:`) commit where only review
addenda follow it, else the head — and never by the commits below it. A seat's commit under his signed commit reads *merge:
your answer* on main today for `answer:` with a review on top (row 9, since 0.18.4), and for any act whose head is his
commit; this branch brings `done:`/`due:` with a review on top into the same reading (row 8, where main's *wait* came from
reading the Reviewer's head). The route is real: `owner_change` cuts `answer/<id>` from the branch he stands on (`git switch
-c` from the current branch, shoalmark.py ≈1918), so an act run on a seat's unmerged branch carries its commits, and nothing
in the rights gate refuses a seat's commit on `answer/<id>`. A seat's own `--done` is refused before the cut, so the tool's
unsigned refusal records under his commit are his own. **Fix, forward:** read an `answer/*` pull request as *merge: your
answer* only where every commit of its own below his is his too, or a review addendum; else *wait: a seat's commit on your
answer branch (<sha>)*.

**RV-739 · P3 · forward — a test gap on the two edges the widening creates · confidence high (~90%).** The three new checks
pin rows 2, 3 and 4. No check pins row 5 (a verdict that quotes `done:` at a line start is the newest match and reads a
wait, never a merge) or row 7 (a seat's `done:` under a verdict is now the commit read, and it names the seat where main named
the Reviewer). Row 7 is the impostor on the new path; `answer_reading`'s R8 check pins the impostor only as a head. **Fix:**
two checks in the same harness — `act31_` and `verdict31_` already build both shapes.

No P2 or P1 found.

## For the Owner's cold session

- **The one expression:** `answered_at`, shoalmark.py:1412 — `-G "^answer:"` becomes `-G "^(answer|done|due):"`. The scope
  (`-- <tracker dir>`), the `addenda_only(at, head, None)` test, and the fall back to the head are unchanged; so is
  `answer_reading`, which decides merge or wait on the commit it is given.
- **The `-G` scope is the whole tracker directory**, not the trackers alone: a review file, an evidence file or `INDEX.md`
  under it can be the newest match. Whatever it finds is read by the author and signature test, so a wrong find errs to a
  wait: a seat's match names the seat (row 7), and a non-review commit after the match sends the reading to the head (rows 4
  and 6).
- **Row 5's edge:** a verdict whose file quotes `done: "…"`, `due:` or `answer:` at a line start is itself the newest match,
  and the branch reads *wait: not an answerer (reviewer@seat)*. That is a wait, never a false merge; 0.18.4 had the same
  edge for `answer:`. It is rare: no evidence file on PortDive's `origin/main` (`a42ac134`) carries such a line, and one on
  shoalmark's (`work-tracker/evidence/FM-005/design.md`) does, which is not a review.
- **Rows 8 and 9 (RV-735):** row 8 is the one line where this branch turns a *wait* into a *merge* over a seat's commit
  below his signed `done:`. Main's wait there was an accident of reading the Reviewer's head; `answer:` has read row 9 as
  *merge* since 0.18.4. I grade it P3, forward. Judge whether you agree that it is not blocking.
- **Ten minutes to reproduce:** (1) `git show 8409c9a -- shoalmark.py` — one code line; (2) `python3 test_shoalmark.py`
  — the three `0.18.6 · RV-679` checks `ok` (the whole run is minutes); (3) the replay above: a `--shared` scratch clone of
  any PortDive checkout, a bare scratch `origin` with alternates to PortDive's objects, `main` `f5bc3a6b`, `answer/bug-327`
  and `refs/pull/876/head` `28808f42`, `gh` stubbed to PR 876 open, `--queue --root <clone>` with `9e9fcb3`'s and `8409c9a`'s
  `shoalmark.py` (`github_remote` patched true): main *wait: not an answerer (reviewer@seat)*, tip *merge: your answer …
  signed 5f307d3*.

## Verdict

**READY WITH FINDINGS** on `8409c9a`. The change is one needle, and it does what RV-679 asked: both of PortDive's cases
(PR 876's `--due`, PR 866's `--done`) read *merge: your answer* by the tip and *wait: not an answerer (reviewer@seat)* by
main. Every reading it changes is a wait turned into a merge on his signed act, or one wait naming a different non-answerer.
The suites are green on both Pythons, 510 + 148, 0 skipped. RV-735 and RV-739 are P3 and forward, each its own slice. It
lands after its merge of main (the `CHANGELOG.md` conflict with PR 113), and that merge takes its own scoped re-check.

Confidence that the Owner's cold session finds nothing blocking: **~80%**. The one expression, the replays and the suites leave little room in the change
itself. The residual is mostly RV-735's row 8: a cold reader may weigh the one wait this branch turns into a merge over a
seat's commit below his `done:` as P2 rather than P3 (~15%). The rest (~5%) is what a cold reading finds that a same-session
one does not.

Path 5 — a merge rules nothing; the Owner's cold session's verdict counts.
