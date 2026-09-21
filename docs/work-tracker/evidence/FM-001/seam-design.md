# FM-001 — the extension seam: a design to rule on, no code

> **Ruled and superseded, 2026-09-21.** The Owner asked for *convention over configuration*, which neither candidate
> below honours; candidate B was reworked into **B′ — a deriver by convention**, proven in
> [seam-bprime-rd.md](seam-bprime-rd.md) and merged as 0.4.0. This page is kept for the seven needs it reads out of
> the origin and for the reasons A was not taken.

Principal, 2026-09-21. One consumer exists — the origin's release axis — so the seam is designed against that
and nothing else. **Two candidates; a recommendation; what each costs. Nothing here is built.**

## What the origin's release axis actually needs from a seam

Read from its generator, not guessed — 18 functions, 831 lines:

| # | Need | Today, in the origin |
|---|---|---|
| 1 | three more front-matter keys with shapes — `suite:` `target:` `version:`; the shapes depend on a registry of release targets | `FRONT_MATTER`, `_WHERE`, `targets.py` |
| 2 | values **derived** per tracker, never typed — `Live` (does the release tag exist in that submodule?), `surface` | `derive_live`, `surface_tags`, git calls, cached |
| 3 | three lints, and one **refusal before anything is written** with its own exit code and an override flag (submodules not checked out → every `Live` cell would silently become `—`) | `lint`, `absent_live_submodules`, exit 5 |
| 4 | four more INDEX columns, a roll-up section (*open work by target × suite*), header paragraphs and two header notes | `render`, `render_packages`, `main` |
| 5 | **other generated files** — a roster block inside each `docs/features/<suite>/README.md` — drift-checked by `--check`, staged via `--print-written` | `suite_roster_updates` |
| 6 | on the page: five row fields, a third view (*by release*, version-sorted, header says `live ✓` / `on main` / `target`), two columns, facts-strip entries, search words | `HTML_PAGE`, row slots 3·4·9·10·11 — left as `—` in the core on purpose |
| 7 | one more *needs* mark (`target` where the plan never named its release target) | `needs_of` |

## Candidate A — hooks: the configuration names a Python module, the core calls it

`extension = "scripts/tracker_release_axis.py"`. The module may define `keys()`, `extract(fm, body)`, `guard(trackers, args)`,
`lint(trackers)`, `needs(t)`, `index(trackers)` (columns · sections · header), `files(trackers)`, `page()` (row fields + a JS
snippet that registers a view, columns and facts on a small `FM.` registry), `args(parser)`. Nine hook points — one per need.

- **For:** covers all seven needs; the origin's `INDEX.md` can stay **byte-identical**, which is the proof its sweeps have always used.
- **Against:** nine hook points is a framework, designed from one consumer. The core loads and runs code named in a
  configuration file. It ties the seam to Python for good — a Rust core could only call it through a subprocess shim.
  The page half means refactoring the core's page around registries: the largest and least testable piece.

## Candidate B — declared columns and a sidecar: no code crosses the seam

The core learns two declarative things and nothing else:

```toml
[keys.target]                      # an extra front-matter key: shape, who writes it, what it says
shape = "…"                        # a regular expression, as every core key has
says  = "the PLAN — <release target> <version>"
[columns]                          # extra columns, in INDEX.md and on the board, in this order
Suite = "suite"                    # a front-matter key …
Live  = "derived.live"             # … or a value from the sidecar
[views.release]                    # an extra board view: group by a column, sorted as versions
by = "derived.release"; sort = "version"
```

**The sidecar** is `docs/work-tracker/.derived.json` — `{ "FEAT-180": { "live": "live ✓", "release": "rs-server 0.16.4" } }` —
git-ignored, written by **the origin's own script, which runs before the core in the same hook**. That script keeps
everything that is the origin's business: the target registry, the git-tag lookups, the submodule refusal (it exits 5
and the hook stops — the core never runs), its three lints (it fails the commit itself), the rosters and the roll-up,
which moves out of `INDEX.md` into a file that script owns.

- **For:** the seam is data — two config tables and one JSON file — so it survives a rewrite of either side in any
  language, runs no foreign code, and is small: my estimate is ~90 lines in the core against ~250 for A. The core
  stays ignorant of releases, which is what *core only* meant. Needs 1, 2, 4 (columns), 6 and 7 are covered by
  declaration; 3 and 5 stay wholly in the origin, where they are already tested.
- **Against:** `INDEX.md` is **not** byte-identical after the port — the roll-up section leaves it. The proof
  becomes *same rows, same columns, same cell values*, checked by script, plus the rendered board read back in a
  headless browser (possible since 0.3.0). Two tools run in one hook, in a fixed order; a sidecar that is stale or
  missing must be *visible* — the core prints `—` and says the sidecar is absent, never a stale `live ✓`. The header
  paragraphs that explain `Live` have to come from configuration text.

## Recommendation — B, with one condition

**B.** A is the seam that fits today's code; B is the seam that fits what fathom-mark is for — a small core other
repositories can trust, in whatever language it ends up. The condition: before any code, I write the sidecar's
staleness rule as a failing test, because a derived `live ✓` that outlives its tag is the one way B can lie, and A cannot.

**What would change my mind:** the Owner needs the roll-up *inside* `INDEX.md` (then A, or B plus one declared
`include =` of a generated fragment); or a second consumer turns up whose extension is logic, not columns.

## What neither candidate touches

The project-key ids (`PD`, from 400 — ruled, parked) ride the same port but are configuration, not seam. The origin's
840-line test file splits either way: core checks live here already; release-axis checks stay there.

## Unproven

Both size estimates are read from the code, not measured. B's claim that needs 6 and 7 reduce to declared columns
and one declared view has not been tried against the origin's page. No second consumer exists to test generality.
