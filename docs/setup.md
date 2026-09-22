# Set up in ten minutes

*For the person who owns the repository. Python 3.9 or newer is the only requirement.*

## 1. Put the tool in the repository

```
git clone https://github.com/holgo99/shoalmark ~/shoalmark      # once, anywhere
cd <your repository>
python3 ~/shoalmark/shoalmark.py --vendor tools/shoalmark
```

`tools/shoalmark/` is now a pinned copy: eight files and a `PIN` of their hashes. It never updates itself; you run
`--vendor` again when you want a newer one, and it prints what changed. On Windows the command is `python`, not `python3`.

## 2. Initialise

```
python3 tools/shoalmark/shoalmark.py --init --key AP
```

`AP` is your id prefix — work items become `AP-001`, `AP-002` … Choose something short that names the project, not a
kind of work. This writes `shoalmark.toml`, `docs/work-tracker/TRIAGE.md`, the agents' contract into `AGENTS.md`, and
a `CLAUDE.md` router. Nothing is overwritten.

**In German?** Copy the four files from `examples/de/` first — `shoalmark.toml` (section names in German),
`TEMPLATE.md`, `TRIAGE.md`, `brand/labels.yaml` — and the board and every new work item come out German.

## 3. Wire the gate

```
python3 tools/shoalmark/shoalmark.py --install-hook
```

- **git:** plain hooks — the index is regenerated and checked on every commit; a work item that contradicts itself is refused.
- **Subversion:** the TortoiseSVN hook properties and `svn:ignore` for the board. Subversion's command line runs no
  client-side hook, so the contract tells agents to run the tool before `svn commit`. For a gate nobody can skip, call
  `--check` from your server's `pre-commit` hook.

## 4. Say who answers

In `shoalmark.toml`:

```
answerers = ["yourname signed"]     # git — see "Your answer is your commit"
answerers = ["yourname"]            # Subversion — the server authenticates you already
```

## 5. Write two things only you can

Open `docs/work-tracker/TRIAGE.md`. **The intent** — *for · so that · never*, in your words — and **the current path**:
what comes first. Agents read both before every judgement. Leave everything else to them.

## 6. Open the board

`docs/work-tracker/index.html` — it is git-ignored and rebuilt on every commit and checkout. Its first line is what
needs you. Set `standup = "09:00"` in `shoalmark.toml` and run `--standup calendar.ics` for the invite: see
[The standup](standup.md).

That is all. The agents file the work; you answer what only you can.
