# The drift skills

*Two agent skills from shoalmark, in their own repository, [shoalmark/skills](https://github.com/shoalmark/skills),
packaged as one plugin for Claude Code and Codex.*

## What they do

- **find-drift** reads the repository and finds where an agent could drift off track: rules kept only as prose, sources
  that disagree, and obsolete text that still reads as live. It ranks what can become a check. It writes one report and
  its hash, and commits nothing.
- **prune-drift** works on a new branch, from find-drift's report. It prunes recorded history from comments and unread
  docstrings in tracked code, with a proof that the code stays the same, and records missing reasons first. The proof
  covers Python; a file it cannot cover is left unchanged and named.

## What they need

Any git repository, its working tree clean apart from earlier reports. shoalmark is not needed: neither skill runs it.
Where the repository has a `shoalmark.toml`, they use it, and the reports go to the tracker folder's `evidence/drift/`;
without one, find-drift asks where to write. Neither uses the network or runs your tests.

## Install

Each install is pinned to a release tag of shoalmark/skills.

**Claude Code:**

```text
/plugin marketplace add shoalmark/skills@v1.0.0
/plugin install shoalmark@shoalmark
```

**Codex:**

```text
codex plugin marketplace add shoalmark/skills@v1.0.0
```

Then restart the ChatGPT desktop app, open the Plugins Directory, choose the shoalmark marketplace and install
shoalmark from it.

If you installed the plugin from shoalmark 0.20.2, its marketplace is also named shoalmark. In Claude Code, the add
command above replaces it in place. In Codex, first remove it with the command below, then add the marketplace as
above.

```text
codex plugin marketplace remove shoalmark
```

## Use

In Claude Code, the plugin's skills are `/shoalmark:find-drift` and `/shoalmark:prune-drift`. In Codex, type `$` to
mention a skill: `$find-drift` and `$prune-drift`.

### find-drift

**Ask** before a release, or before pruning prose: `/shoalmark:find-drift`, or `$find-drift` in Codex. After one rule
or ruling changes, ask for a scoped run on the sources it touches.

**Back comes** one report, `<tracker folder>/evidence/drift/<date>-<short sha>.md`, with its sha256 beside it in
`<file>.sha256`: the rules it found, each graded by how it is enforced, the ten to promote first, the disagreements and
the obsolete text. Its last message names each disagreement and each obsolete text in one line, asks whether to file
them as asks, and names the next step, prune-drift.

### prune-drift

**Ask** after find-drift, or when you want prose pruned: `/shoalmark:prune-drift`, or `$prune-drift` in Codex. It needs
a report whose sources have not changed since; where none is fresh, it runs find-drift first.

**Back comes** a new branch, never your default branch: the missing reasons recorded first, in a commit of their own;
one commit that deletes the agreed history, with the proof's output in its message; obsolete text fixed in separate
commits, only where a later source settles it. Its report, `<date>-<short sha>-prune.md`, and its sha256 go to the same
folder. Its last message lists what needs your decision, asks whether to file it as asks, and asks whether to run your
repository's tests and CI: it runs none of them itself.

## The report's language

The report's prose and the conversation follow your language: the Board's language, `lang` in the repository's
`<tracker dir>/brand/labels.yaml`, where that file sets it, otherwise the language you write in. A `lang` that fails
shoalmark's own check counts as not set. The report's section keys and its file names stay as they are, so prune-drift
reads what find-drift wrote. **Limit:** the Board reads `labels.yaml` in three places, the later winning: the vendored
copy's `brand/`, the repository's `<tracker dir>/brand/`, and your `~/.config/shoalmark/`. A skill reads only the
repository's, so where the Board takes `lang` from the vendored copy's file or from yours, the report's language can
differ from the Board's.

## The way to shoalmark

The skills come from shoalmark, a work tracker that lives in the repository it tracks and puts what needs you first.

- [Why shoalmark?](why-shoalmark.md)
- [Set up in ten minutes](setup.md)
- [The feedback form](https://shoalmark.tools/feedback), for what the skills found or what got in the way. What you send
  there is public, under your GitHub name.
