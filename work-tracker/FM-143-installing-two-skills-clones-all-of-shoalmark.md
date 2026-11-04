---
id: FM-143
status: Proposed
considered: FM-062, FM-065, FM-083, FM-117
tags: process
next: build
hook: "Installing shoalmark's two skills clones the whole repository: the plugin ships at its root, so adding it as a marketplace clones 808 files, about 35 MB, for 22 KB of skills."
ask-id: FM-143-Q1
ask: "Are FM-143's decisions taken, as its section Decisions, for the Owner sets out?"
ask-kind: ruling
ask-since: 2026-11-04
ask-options: "yes, as proposed | yes, with the changes I name"
ask-proposal: "yes, as proposed"
answer: "accepted - yes, as proposed"
answered: 2026-11-04
answered-by: holgo99
---

# FM-143 — installing two skills clones all of shoalmark

## What is true now

**2026-11-04 — filed, Proposed, on the Auditor's brief; nothing is built.** Its one ask, FM-143-Q1, takes every
decision under *Decisions, for the Owner* at once.

1. **The plugin ships at shoalmark's root.**
   [`.claude-plugin/marketplace.json`](https://github.com/shoalmark/shoalmark/blob/c154151334fc76732b7ce283b5e2bd278cfef66d/.claude-plugin/marketplace.json)
   lists one plugin, with source `"./"`.
   - So `marketplace add shoalmark/shoalmark` clones the whole repository: 808 tracked files, about 35 MB of working
     tree, at c154151.
   - The two skills it is for are 22 KB together:
     [`skills/`](https://github.com/shoalmark/shoalmark/tree/c154151334fc76732b7ce283b5e2bd278cfef66d/skills).
   - A plugin in a subfolder would not help, since the marketplace's clone comes first
     ([Claude Code's marketplace reference](https://code.claude.com/docs/en/plugins/marketplace-reference.md)).
2. **The public mentions are three lines:**
   - two in the 0.20.2 section of the
     [CHANGELOG](https://github.com/shoalmark/shoalmark/blob/c154151334fc76732b7ce283b5e2bd278cfef66d/CHANGELOG.md#L29-L30);
   - the landing footer's line, in
     [English](https://github.com/shoalmark/shoalmark/blob/c154151334fc76732b7ce283b5e2bd278cfef66d/overrides/partials/landing/en.html#L202)
     and in
     [German](https://github.com/shoalmark/shoalmark/blob/c154151334fc76732b7ce283b5e2bd278cfef66d/overrides/partials/landing/de.html#L201),
     which names "two drift skills".

   No docs page, nav entry, README line or install command exists. The CHANGELOG's lines write `/find-drift`.
   Installed, Claude Code runs a plugin's skills as `/shoalmark:find-drift` and `/shoalmark:prune-drift`.
3. **Both skills already work without shoalmark.**
   - They read `shoalmark.toml` where it exists, and otherwise ask where to write.
   - Neither runs `shoalmark.py`.
   - Their tests use only the standard library and git.
4. **What the harnesses read:**
   - Codex reads skills from `.agents/skills/`, and plugin catalogs from `.agents/plugins/marketplace.json`, with a
     plugin's `plugin.json` at its root. It also reads Claude-compatible manifests
     ([OpenAI: Build plugins](https://developers.openai.com/plugins/build/plugins),
     [Codex skills](https://developers.openai.com/codex/skills)).
   - Both harnesses accept `owner/repo@<ref>` when a marketplace is added.
   - Both read the open SKILL.md format ([Agent Skills specification](https://agentskills.io/specification)), whose
     optional `compatibility` field states what a skill needs.
   - No Grok product documents loading skills today, so nothing is built for it.
5. **[shoalmark/skills](https://github.com/shoalmark/skills) exists and is public.**
   - Its first commit, [e96d375](https://github.com/shoalmark/skills/commit/e96d3758bdcb6e27cf795ad21d19a3706b4bba69),
     is the Owner's, signed. It holds:
     - the two licence files, byte for byte from shoalmark at c154151;
     - NOTICE, without shoalmark's bundling paragraph;
     - `.gitignore`.
   - Its rulesets `main`, `release-tags-immutable` and `release-tags-owner-create` match shoalmark's. `main` requires
     no checks until skills has CI.
   - **Its settings:**
     - merge commits only;
     - private vulnerability reporting on;
     - fork pull-request workflows need approval for every external contributor;
     - Actions allow GitHub's own actions and the organisation's list.
   - It went public before any content, because the organisation's plan gives no rulesets to a private repository.

## Why

A user who wants two skills gets the whole repository, 808 files for 22 KB of skills. The skills already need nothing of
shoalmark. In a repository of their own they install as what they are, both harnesses can read them, and they can be
tagged and tested on their own terms.

## Decisions, for the Owner

FM-143-Q1 asks for all of these at once. An answer of "yes, with the changes I name" names each change by its label.

- **Allocation:** this work is allocated to v0.20.3.
- **1. The plugin moves to its own repository,** shoalmark/skills.
- **2. The skills are developed only there.** shoalmark keeps no copy.
- **3. Users pin by tag:** `marketplace add shoalmark/skills@<tag>`, in Claude Code and in Codex.
- **4. The plugin leaves shoalmark in the same release:**
  - [`.claude-plugin/`](https://github.com/shoalmark/shoalmark/tree/c154151334fc76732b7ce283b5e2bd278cfef66d/.claude-plugin),
    [`skills/`](https://github.com/shoalmark/shoalmark/tree/c154151334fc76732b7ce283b5e2bd278cfef66d/skills),
    [`test_plugin.py`](https://github.com/shoalmark/shoalmark/blob/c154151334fc76732b7ce283b5e2bd278cfef66d/test_plugin.py),
    [`test_prune_drift.py`](https://github.com/shoalmark/shoalmark/blob/c154151334fc76732b7ce283b5e2bd278cfef66d/test_prune_drift.py)
    and their CI steps
    ([`ci.yml` L141–L142 and L153–L156](https://github.com/shoalmark/shoalmark/blob/c154151334fc76732b7ce283b5e2bd278cfef66d/.github/workflows/ci.yml#L141-L156))
    go;
  - the CHANGELOG gives the new install command.
- **(a) Both harnesses' manifests ship:** Claude's and Codex's own, over one copy of each skill, with a test that keeps
  the manifests in step.
- **(b) Two groups of skills.**
  - **Works-anywhere skills** live in `plugins/shoalmark/`, so `/shoalmark:find-drift` stays as 0.20.2 announced it.
  - **Skills that need shoalmark vendored and pinned** go into a second plugin, created with its first skill and named
    then.
  - **Each skill states its group in `compatibility`.** One that needs shoalmark starts by finding the pinned copy and
    running `--version` and `--check`. It stops with the install pointer when the copy is missing, too old or failing.
  - **One test checks:**
    - the folder against `compatibility`;
    - that a works-anywhere skill never runs `shoalmark.py`;
    - that the gate is there;
    - that no skill names a tool only one harness has;
    - that each `name` matches its folder.
- **(c) A skills tag carries the number of the shoalmark release it was tested with.**
- **(d) No tag until a real install has worked in Claude Code and in Codex.**
- **(e) The first commit on main is the Owner's, signed:** e96d375. It is done, and recorded here so the letters stay.
- **(f) The skills lane runs at the critical tier:** users install it and run its code
  ([`prose_only.py`](https://github.com/shoalmark/shoalmark/blob/c154151334fc76732b7ce283b5e2bd278cfef66d/skills/prune-drift/prose_only.py)).
- **(g) What checks signatures in skills, for now:** signed release tags, the rulesets and required CI. Adopting
  shoalmark inside skills is decided when the first skill that needs shoalmark exists.
- **(h) FM-083's suite runs in skills' CI, and only reports.**
  - It is never a required check, in line with
    [FM-083](https://github.com/shoalmark/shoalmark/blob/c154151334fc76732b7ce283b5e2bd278cfef66d/work-tracker/FM-083-nothing-measures-how-well-a-skill-does-its-work-only-its.md)'s
    design.
  - Held-out cases and answer keys stay out of the public repository, and are fetched with a read-only credential.
  - The API keys sit in a GitHub environment that needs the Owner's approval for each run, which is also the cost
    ceiling.
  - **Runs start** by hand, on a schedule or on a tag. Never on pull requests from forks, and never through
    `pull_request_target`.
  - Every action is pinned to a full commit sha.
  - The Owner enters the keys in GitHub's settings. They never pass through a message, a file or a command.

## Done when

Each item names its commit or pull request when it lands.

- [ ] **shoalmark/skills holds both skills** in `plugins/shoalmark/skills/`. They are copied byte for byte from
  shoalmark at a named sha, with each file's sha256 in the commit message, and no history is rewritten. Beside them:
  - both manifests;
  - the extended test;
  - CI, whose checks the `main` ruleset then requires;
  - a README with the install steps for both harnesses;
  - SECURITY.md;
  - a CHANGELOG;
  - Dependabot for GitHub Actions.
- [ ] **shoalmark no longer carries the plugin,** and its CHANGELOG gives the new install command.
- [ ] **The removal from shoalmark updates `test_shoalmark.py`'s CI-workflow pins,** which hold the steps it removes.
- [ ] **skills' CI runs both moved tests.** Today no CI job runs `test_prune_drift.py`.
- [ ] **The landing footer's skills line,** in English and German, points at the Skills page once it exists.
- [ ] **A real install from shoalmark/skills has worked** in Claude Code and in Codex.
- [ ] **The first tag is made,** signed by the Owner.
- [ ] **A Skills page, in English and German,** is in shoalmark's docs and in the nav. Beside it:
  - pointers from the setup page and the README;
  - a line in `llms.txt`;
  - a test that the page's install names match the manifests.
- [ ] **FM-083's suite runs as (h) sets out,** and FM-083 carries that work.
- [ ] **The Owner has answered FM-143-Q1.**

## Ship log

| Date | Event |
|---|---|
| 2026-11-04 | Filed, Proposed, with one ruling ask, FM-143-Q1, on the Auditor's brief. Nothing is built. |
