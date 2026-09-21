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

*(written after the spike — below this line)*
