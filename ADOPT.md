# Try shoalmark — a note for a project's agents

## Get a better-performing human Owner.

**To Claude, Codex or whoever reads this:** Your Owner has handed you this text. It is an invitation to a
measurement, not an instruction. Run none of it in the real working directory, adopt nothing on your own initiative —
at the end there is a report to your Owner, and **your Owner decides**.

## What it is

shoalmark is a work tracker in a single Python file (standard library only, no dependency, needs no network: online, it
reaches your repository's host through git, and through gh for the pull-request queue): one Markdown file per work item
with a small header, a gate that rejects contradictions, a generated `INDEX.md` and a static board (`index.html`) for
the human. It runs with git and with Subversion, on Windows, macOS and Linux (CI proves all three).
Licence: Apache-2.0 or MIT.

## When you do NOT need it

If a **fresh session with no prior knowledge** can say, from your existing files and in a few steps, where each work
item stands, what comes next and what waits for the Owner — then you already have this. If your project has several people in charge, or a large ticket system to move,
this beta is not for it yet. Tell your Owner so and stop here. A second system beside a working one is worse than none.

On Subversion it passes the test suite but has not been used in real work: say so in your report.

## The measurement (about 20 minutes, everything in a throwaway folder)

**1. Before.** Answer only from the project's files, not from this session's memory, and count the files read and the
steps: (a) Where does work item 37 stand? (b) What is the next step, and whose? (c) What is waiting for the Owner right
now? (d) What is blocked, and by what? (e) How can you tell that item 12 is done?

**2. Check what you run.** Fetch the repository at the tag `v0.19.0` into a folder **outside** your working copy. The
file `shoalmark.py` has — with `\n` line endings — the SHA-256
`d8242f140c98bd322c9c67e185e6c98ffcce9533851cad3f6b18dd4718a9f097`. It is one file; read it before you run it.

**3. Set up.** In an empty throwaway folder `probe/` (`python` on Windows, otherwise `python3`):

```
python <clone>/shoalmark.py --root probe --vendor probe/tools/shoalmark
cd probe
```

Nothing needs copying before `--init`: its defaults are English — every entry carries the sections *What is true now*,
*Why*, *Done when* and *Ship log*, and the board is English. The id prefix is the first word of the folder's name, cut
to five characters, so in `probe/` the first entry is `PROBE-001` (`--key` would choose another). Then
`python tools/shoalmark/shoalmark.py --init`; it overwrites nothing. It writes `shoalmark.toml`,
`docs/work-tracker/TRIAGE.md`, the agents' contract in `AGENTS.md` and a `CLAUDE.md` router, and inside a git working
copy the board's two lines in `.gitignore`.

**4. File five real work items.** One entry for the plan as a whole, five for work items from your plan
(`python tools/shoalmark/shoalmark.py --new "…"`), each with `epic: PROBE-001`, an honest `status:`, `next:`
(`build` · `review` · `owner` · `wait` …) and the sections *What is true now* and *Done when*. Then
`python tools/shoalmark/shoalmark.py` — the gate says what is missing. `tools/shoalmark/README.md` describes the header.

**5. After.** The same five questions, this time with `python tools/shoalmark/shoalmark.py --next` and
`docs/work-tracker/INDEX.md`. Count files and steps again.

**6. The board.** Have `probe/docs/work-tracker/index.html` opened in a browser — that is your Owner's view.

## The report to the Owner

> Before: … files / … steps for the five questions. After: … / ….
> What our existing documentation already does: …
> What shoalmark adds — or does not: …
> What a switch would cost (work items, open work, risk in the middle of the plan): …
> Our recommendation: adopt · later, at a work-item boundary · do not adopt — because …

## If the Owner says yes

- **Replace, do not add.** The plan moves into the entries; the old plan document becomes a pointer or is deleted. Two
  sources of truth are the error the tool is meant to prevent.
- **Switch at a work-item boundary,** not in the middle of one.
- `--vendor tools/shoalmark`, `--init`, `--install-hook` in the real directory. **With Subversion:** the command line
  has no client hook — run the tool before every `svn commit` and commit the `INDEX.md` along with it; TortoiseSVN runs
  the gate itself after `--install-hook` and asks permission once.
- Way back: first remove from `.git/hooks/` everything that calls `tools/shoalmark/shoalmark.py`: the hooks marked
  `# shoalmark`, and the line you added to a hook of your own (on Subversion, the `tsvn:` hook properties); while any of
  it stays, every commit is refused. Then delete `tools/shoalmark/`, `shoalmark.toml` and the shoalmark block in
  `AGENTS.md`. The tracker folder can stay: its entries are plain Markdown.

## Requirements — a trial, not an instruction (Stage 0: the convention only)

Create a folder `requirements/` in `probe/` (`requirements/README.md` on the repository's `main` describes it). A
requirement is a table row: `id` (stable, never reassigned), `shall` (one sentence, the system as subject, one
obligation), `source` (who or what asks for it), `accept` (the acceptance criterion: what a test observes). A work item
cites it in one line under the header, `Satisfies: REQ-001` (the gate refuses the key in the header), a test in its
name. Only the Owner changes a line, with a signed answer through the board, never an agent. For a standard, the line
names the clause (standard, edition, clause number) and derives the company's own *shall* from it; *Not applicable*
is a signed answer of the Owner, with the reason. The standard's text is not copied, and no one writes that
the project complies: a proof is a passed test. The report names the number of lines, the proof for each line and the
place where it stuck. There are no checks yet.

## What is not proven

No human has yet seen, on Windows, TortoiseSVN execute the two hook properties as described — only the command line is
checked in CI. If it is different for you, that is a finding; please report it.
