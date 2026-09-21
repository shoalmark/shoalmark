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

*(written after the work — below this line)*
