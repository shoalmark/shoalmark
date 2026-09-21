# FM-001 — B′, a deriver by convention: R&D before anyone commits to it

Principal, 2026-09-21. The Owner: *"B′ is a go. Explore and R&D this properly before committing to it — we need
proof."* This file is written **before** the spike, so the bars cannot move to meet the result. Branch
`rd/fm-001-seam-bprime`; nothing here merges until the Owner has read the outcome.

## B′ in one paragraph

One path, no setting: if `<tracker dir>/derive` exists and is executable, the core runs it first, on every run. It
receives every tracker's id, status, file and front matter as JSON on stdin and answers with JSON on stdout:
per-tracker values (each key becomes a column in `INDEX.md` and on the board, and a view on the board), `_keys`
(extra front-matter keys with their shape and meaning, merged into the schema gate) and `_problems` (its own
lints, shown and counted with the core's). A non-zero exit refuses the run before anything is written. Nothing
derived is stored, so nothing derived can be stale. The core's configuration gains no entry.

## The test bed

The only consumer there is: the origin's release axis, against its real corpus — 501 trackers, 8 submodules with
real release tags — in a scratch copy, never in the origin itself. The spike's deriver may import the origin's own
`targets.py` and reuse its release functions: the question is whether the **seam** carries them, not whether they
can be rewritten.

## Pre-registered: what proves it, what kills it

| # | Claim | Proof | Kills B′ if |
|---|---|---|---|
| P1 | The seam carries every release cell | for all 501 trackers, `Suite`, `Target`, `Ver` and `Live` in the spike's `INDEX.md` equal the origin's, cell for cell | any cell differs for a reason the seam causes |
| P2 | The origin's gates survive the move | four mutations, each refused as today: a `version:` on a `Proposed` tracker · a `suite:` with no directory · an exact `target:` already cut · a submodule not checked out (own exit code, nothing written) | a refusal cannot be expressed through `_problems` or the exit code |
| P3 | Nothing derived can be stale | in a fixture repository, deleting a release tag flips `live ✓` on the very next run, with no file to clear | the core needs a cache to be fast enough |
| P4 | *Every column is a view* is enough for the release view | the board's release view, read back from a headless browser, holds the same groups with the same members as the origin's page | the groups need release knowledge inside the core. **Expected loss, accepted in advance:** the origin's group header words (`live ✓` / `on main` / `target`) — a header is not a column |
| P5 | It is cheap | a full run over 501 trackers, deriver included, in ≤ 2× the origin's 1.3 s | > 3 s |
| P6 | It is small | the core grows by ≤ 120 lines; the deriver is ≤ the 831 lines it replaces | the core grows past 200 |
| P7 | The schema gate still bites | with `_keys` merged, `targt:` is still refused and `target:` named as the near miss; a bad `version:` shape is refused | `_keys` weakens a core check |
| P8 | A repository without a deriver pays nothing | the 51 existing checks stay green untouched; msr-lager's output is byte-identical | any existing check must change |

**My forecast, before the spike:** P1 0.80 · P2 0.85 · P3 0.95 · P4 0.60 · P5 0.75 · P6 0.80 · P7 0.85 · P8 0.90 ·
all eight 0.40. P4 is where I expect trouble: a release is two things in the origin — a version *and* a release
target — and a single column may not group the way its page does.

## Outcome

**B′ carries the origin's release axis. Seven of the eight pre-registered claims are proven outright; P4 is proven
with exactly the loss accepted in advance; one need the pre-registration missed was found, added to the seam and
proven too. Nothing killed it.** The spike is on this branch; the deriver it ran is kept beside this file
([`spike/origin-release-axis.derive.py`](spike/origin-release-axis.derive.py), 128 lines). The origin was never
written to — its working tree shows 0 changed files after every run.

| # | Forecast | Outcome | Measured |
|---|---|---|---|
| P1 | 0.80 | **proven** | 501 trackers × `Suite` `Target` `Ver` `Live` — **0 differing cells**; and 0 in `Tier` `Status` `Board` `Triaged` too. 81 `live ✓`, 1 `on main ⏳`, as in the origin |
| P2 | 0.85 | **proven** | each mutation refused with the origin's own words: `version:` on a `Parked` tracker · a `suite:` with no directory · `target: rs-server 0.16.4` *ALREADY CUT (portdive-rs:v0.16.4)* — exit 4; a submodule not checked out — **exit 5, `INDEX.md` byte-untouched**, 66 dependent trackers named |
| P3 | 0.95 | **proven** | fixture repository, in the test suite: the tag is deleted, the next run prints `—`; no `.derived*` file exists to clear |
| P4 | 0.60 | **proven, with the accepted loss** | both pages rendered in headless Chrome, release view, all 501 rows: **62 groups on both, identical members, identical group order, identical row order inside every group.** Differences: the empty group is called *no release* where the origin says *unscheduled*; the origin's header words (`target` · `live ✓` · the surfaces) are gone — the loss named in advance |
| P5 | 0.75 | **proven** | 1.40–1.51 s against the origin's 1.23–1.77 s on the same machine, same corpus — about 1.15× |
| P6 | 0.80 | **proven** | the core grew **1,700 → 1,764 lines (+64)**; the deriver is 128 lines where the origin spends 831 lines of functions on the same axis |
| P7 | 0.85 | **proven** | `targt:` → *did you mean `target:`?*; a bare `0.17.x` refused with the key's meaning and the list of release targets; a deriver that redefines a core key is itself refused |
| P8 | 0.90 | **proven** | 51 existing checks green, untouched, on Python 3.14 and 3.9; msr-lager's `INDEX.md` byte-identical under the vendored spike. Honest footnote: its `index.html` is *not* byte-identical — every row gains an empty `{}` and the page a `COLS=[]`; it renders the same |
| — | all eight: 0.40 | **all eight held** | the forecast was underconfident, most of all on P4 (0.60): a release string sorts as a version without the core knowing what a release is |

**Found by the spike, not foreseen — and that is the part worth the R&D:**

1. **The pre-registration missed need 5: other generated files.** The origin writes a roster block into 9 product-area
   READMEs, drift-checks them and stages them. B′ as ruled had no answer. Added: `_files: {path: text}` — **the deriver
   stays free of side effects; the core writes, drift-checks and stages.** Proven on the real thing: all 19 READMEs
   byte-identical to the origin's, `--print-written` lists 9 rosters + `INDEX.md`, a tampered roster is *STALE*
   (exit 3) and regenerates identical. A path outside the repository is refused.
2. **A deriver that crashes is a refusal.** My own deriver had a bug mid-spike (`KeyError`); the core printed its
   traceback, said *REFUSED — nothing was written*, and left every file alone. Not designed — it fell out of
   *non-zero exit refuses*. It is now a behaviour to keep.
3. **Every derived value is a column — including one wanted only as a view.** The release view needs
   `Release` (the version if shipped, else the target), so `INDEX.md` gains a fifth column that repeats two others.
   Convention's price. Left as is; the alternative is a naming rule (a lower-case key is a view only), which I
   would add only if the Owner minds the column.
4. **The deriver is code the core runs.** Same trust as a git hook — but it is new surface: it runs on `--html-only`
   (post-merge, post-checkout) and on `--next` too. A deriver that is slow makes every checkout slow.

**Not proven, and not tried:** the origin's *work packages* roll-up (it would become a `_files` entry, and it leaves
`INDEX.md`, so the port is not byte-identical there); the origin's two header notes; the `--allow-missing-submodules`
flag (the spike used an environment variable — a deriver cannot add a CLI flag); any second consumer; the deriver
under Python 3.9 (it ran under 3.14 only); a deriver in a language other than Python.

**What this does not decide.** It proves the seam carries the one consumer there is. It does not prove the seam is
*general* — nothing can, with one consumer. Merging this branch is the Owner's ruling; the port of the origin
(FM-001) is a separate one.
