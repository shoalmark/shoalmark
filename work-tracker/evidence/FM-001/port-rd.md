# FM-001 — porting the origin onto the core: a full exploration before anyone commits to it

Principal, 2026-09-21. The Owner: *"let's explore the backport in full now."* Written **before** the work. The origin
is never written to: everything runs in a scratch copy of its 501 trackers. What comes out is a port that can be
copied in, a list of every visible change for the Owner to approve or strike, and measured numbers — not a merged port.

## Pre-registered: what the exploration has to show

| # | Claim | Proof | If it fails |
|---|---|---|---|
| Q1 | **Nothing of the origin's tracker is lost unnoticed** | every difference between the origin's `INDEX.md` / rendered board and the ported ones is on one list, each line either *kept by the port* or *a change for the Owner to rule on*; the list is produced by diffing, not by memory | an unlisted difference turns up later → the list method is wrong |
| Q2 | **The three things the spike left out are portable through the seam** | the *work packages* roll-up, the two header notes and the submodule override work in the scratch copy; the roll-up's table equals the origin's, row for row | one of them needs the core to know about releases |
| Q3 | **The origin's page keeps its look by convention** | a `theme.css` beside the trackers restores the origin's palette and fonts; with none, the page is the core's | the palette needs a setting |
| Q4 | **Its 157 checks are accounted for** | each is classified — *release axis, moves to the deriver's tests* · *core, already covered in fathom-mark* · *core, NOT covered: a gap to close here* · *obsolete* — by script, ambiguous ones read by hand | > 10 % cannot be classified |
| Q5 | **Every command an agent or a hook types today still works** | `scripts/gen-tracker-index.py` stays as a thin wrapper: same flags (`--check` `--print-written` `--related` `--triage` `--schema` `--html-only` `--allow-missing-submodules`), same exit codes (3 · 4 · 5); the 5 `agents/` pages, 50 trackers and `lefthook.yml` that name it need no edit | a flag or an exit code cannot be kept |
| Q6 | **Nothing else in the origin imports the generator** | grep of its scripts and tests | something does → it is part of the port |
| Q7 | **The triage rules an agent reads are the same, or every changed sentence is listed** | diff of the printed rules, origin against core | — |
| Q8 | **It is not slower where it hurts** | the commit hook and the post-checkout refresh, timed against today's | > 2× |

**Forecast, before the work:** Q1 0.70 (a diff finds what it finds; the risk is the page, which diffs badly) · Q2 0.85 ·
Q3 0.80 · Q4 0.75 · Q5 0.85 · Q6 0.90 · Q7 0.95 · Q8 0.85 · all eight 0.35.
**What I expect to find and cannot yet name:** at least two behaviours of the origin that live in neither the release
axis nor the core, because the core was cut by script from a file I read once.

## Outcome

**The port is feasible and nearly mechanical — and the exploration found the thing that matters more than the port:
the core was cut out with its code and without most of its tests.** Seven of eight claims held; Q4's method failed
its own bar and was replaced by a better one. The origin was never written to (0 changed files after every run).
The original port artifacts are preserved in [the historical `port/` tree](https://github.com/shoalmark/shoalmark/tree/80d0811974a1d39b679cfd374c80109ddd62acce/work-tracker/evidence/FM-001/port): the deriver (161 lines), the wrapper (12), the theme (5), the
configuration (15), and the runner that executes the origin's test file against the core.

| # | Forecast | Outcome | Measured |
|---|---|---|---|
| Q1 | 0.70 | **held** | **`INDEX.md`:** every differing line falls in four classes — 205 tracker rows and 7 ranked rows differ in the *Hook* cell only, and only by its quotation marks · the header text · the roll-up (moved) · one count label (`3 align` → `3 alignment (android parity)`). **The board, rendered in a real browser, all 506 rows: 0 differ.** Story view: 4 group headers carry the same releases and surfaces in a different order. A tracker's page: the facts strip labels its release values (`target …` · `surface …` · `release → …`) where the origin printed one bare value |
| Q2 | 0.85 | **held** | the roll-up is `PACKAGES.md`, generated through `_files`: **33 rows, identical**; both header notes carry the origin's counts (206 · 1); the submodule override is an environment variable the wrapper sets from the old flag — exit 5 without, 0 with |
| Q3 | 0.80 | **held** | `theme.css` beside the trackers, 5 lines: the origin's palette and fonts, seen side by side in screenshots; none → the core's neutral page |
| Q4 | 0.75 | **the method failed; a better one replaced it** | classifying by script left 69 of 173 checks unplaced — 40 %, the bar was 10 %: they drive the command line, not functions. So the origin's **own test file was run against the core + deriver, statement by statement: 159 of 167 checks pass unchanged.** The other 26 (8 fail, 18 lost to crashed statements) are all accounted for: 21 call release functions that now live in the deriver (`derive_live`, `surface_tags`, `render_suite_roster`, `suite_roster_updates`, the three release lints called through `gti.lint`) · 3 pin a string or a constant the port changes on purpose (the row layout, `CONSIDERED_FROM`, a *STALE* wording) · 2 are my fixture's fault, not the core's |
| Q5 | 0.85 | **held** | the wrapper keeps every flag and exit code — 0 · 3 · 4 · 5 · the override; `--print-written` stages 11 paths (INDEX, PACKAGES, 9 rosters); with `FATHOM_MARK_CMD` every message names `scripts/gen-tracker-index.py`, so the 5 `agents/` pages, 50 trackers and `lefthook.yml` need no edit |
| Q6 | 0.90 | **held, with one** | `scripts/test_targets.py` borrows one constant (`EXACT_VERSION_RE`) — it moves with the deriver |
| Q7 | 0.95 | **held** | 4 of 69 rule lines differ: three say *harm to people who use it today* for *harm in production*; one says *the board* for *the generated suite rosters* |
| Q8 | 0.85 | **held** | commit hook 1.46–1.52 s against 1.30–1.52 s; post-checkout refresh 1.38 s against 1.09 s (1.27×) |

**All eight: forecast 0.35 — seven held.** The miss is mine and instructive: I predicted *what* would be hard (the
page) and was wrong — the page came out at 0 of 506; the tests, which I gave 0.75, were the real finding.

## What the exploration found that nobody had named

1. **The coverage gap — the finding that outranks the port.** The origin carries 173 checks; about 145 of them test
   behaviour that now lives in the core. fathom-mark's own suite has 64, and roughly 25 of those overlap. Dangling
   links and *did you mean*, duplicate ids, the nested-git environment, *`--check` writes nothing*, stdout carrying
   only paths, the page's invariants (no external request, embedded HTML escaped, the colour rules), the worksheet
   keeping its rows across re-runs, the 7-day window, `merge`, a verdict on a new filing, orphan table rows — **all
   of it runs in the core today, none of it is checked here.** The good news is measured: 159 of those checks pass
   against the core as it is. **The real work of the port is moving that test file into this repository** — it
   reads the origin's live corpus as its fixture (`_live`), so it needs a synthetic one.
2. **A deriver could not say what a tracker still *needs*.** The origin shows *Needs: target* on ranked work whose plan
   never named its release target. Added: a per-tracker `_needs`. *(The pre-registration's expected "behaviour that
   lives in neither" — one.)*
3. **Messages named the vendored tool's path**, not the command every page in the origin teaches. Added:
   `FATHOM_MARK_CMD`. *(Two.)*
4. **One model, two renderings — really.** The origin's `INDEX.md` prints `Suite · Target · Ver · Live`; its board
   prints `surface · release`, and a release cell reads `→ rs-server 0.16.x` or `0.16.4 ✓`. B′'s *every value is a
   column* put five columns on the board and wrapped every title. Added, all in the deriver's output, none in the
   configuration: `_index` and `_board` (default: everything), a value as a pair `[value, display]`, `_notes` for the
   header, and a convention on the page — a group header sums its rows up by the board's columns.
5. **A latent behaviour, in the origin too:** a same-day `--triage` re-applies the day's worksheet, so a rank taken
   off by hand on the day of the pass comes back on the next run. It happened in the scratch copy to FEAT-180. The
   worksheet is the record, so this is arguably right — but it is nowhere written down.
6. **The header lost two links** — to the origin's tracker reference and its versioning page. `_notes` can carry them.

## The seam is growing — said plainly

B′ was ruled as *columns · `_keys` · `_problems` · exit code*. It is now ten things: those four, `_files`, `_notes`,
`_index`, `_board`, the `[value, display]` pair and `_needs` — plus two conventions outside the deriver (`theme.css`,
`FATHOM_MARK_CMD`). Every one was forced by a measured difference and none runs foreign code inside the core, but
ten is where candidate A's nine hook points stood when I called it *a framework designed from one consumer*. The
core grew 15 lines for all of it (1,767 → 1,782), which is the honest counterweight. **The Owner should rule on this
list as a list**, not inherit it item by item.

## The port, as a plan — nothing here is done in the origin

1. **Here first:** merge this branch (the seam additions, 64 checks green on Python 3.14 and 3.9); then move the
   origin's core checks into this suite on a synthetic corpus — the gap above. *This is most of the work.*
2. **In the origin, one branch, after its second triage pass** (so that pass tests the rule sentences on the
   instrument they were written for): vendor the core · add `docs/work-tracker/derive`, `theme.css`,
   `fathom-mark.toml` · `scripts/gen-tracker-index.py` becomes the 12-line wrapper · its test file shrinks to the
   ~21 release-axis checks, re-pointed at the deriver · `test_targets.py` imports its constant from the deriver.
   **Deleted: ~1,900 lines of generator, ~150 checks that now live here.**
3. **Proof at the port:** `INDEX.md` differs only in the four classes above, by script · the rendered board 0 of 506 ·
   the 19 roster files and the roll-up's 33 rows byte-identical · every exit code · the origin's gates green.
4. **The project-key ids (`PD`, from 400)** ride the same branch: configuration, not seam.

## For the Owner to approve or strike — every visible change, nothing else changes

| Change | Why | Can it be kept as it was? |
|---|---|---|
| hooks in `INDEX.md` lose their quotation marks (212 rows) | the core prints the hook, not its YAML quoting | yes, one line — I would not |
| the *work packages* table leaves `INDEX.md` for `PACKAGES.md` | the core knows no releases | only by giving the seam an *include* — not recommended |
| `INDEX.md`'s header is shorter and loses two reference links | core header + the deriver's notes | the links: yes, via `_notes` |
| three tier sentences say *harm to people who use it today* | the core serves repositories with no production | no — the rules are the core's; the origin's 13 rehearsals ran on the old wording |
| a tracker page labels its release facts | every derived value is a labelled fact | cosmetic |
| story headers list surfaces before releases | the header convention | cosmetic |
| the viewer's link reads *forge*, not *github* | the core names no vendor | cosmetic |

## Unproven

The release view was compared before the display form and the header convention went in, not after. The deriver
ran under Python 3.14 only. The test move (step 1) is estimated, not tried: my guess is one session, and the
synthetic corpus is where it can go wrong. No second consumer exists. Nothing was run in the origin itself.
