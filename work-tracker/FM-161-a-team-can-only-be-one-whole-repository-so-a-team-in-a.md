---
id: FM-161
status: Proposed
considered: FM-100
tags: process
hook: "A team can only be one whole repository: FM-100's standup-teams refuses a team in a folder of a monorepo, or several teams in one repository, though sealanes/1, the roster spec, may name such places. Lifting that needs the tool's side and the roster spec's side, and waits until sealanes/1 is in force."
---

# FM-161 — a team can only be one whole repository, so a team in a folder or several teams in one repository is refused

Seat: the Planner (27f31560) · filed 2026-11-12, on the Auditor's word of that day.

## What is true now

**Filed 2026-11-12, Proposed, with no release yet; nothing is built.** It waits until sealanes/1, the roster spec in
shoalmark/sealanes, is in force. `blocked-by:` names trackers and the Owner only, so the wait is written here.

- **Where it comes from:** [FM-100](FM-100-the-stand-up-prompt-is-code-and-english-on-every-board-while.md)'s
  decision 9, as proposed. The roster may give a team's place as one or more places, each a repository or a folder
  inside one. For now a team is one repository, whole, and `standup-teams` refuses any other place and names it.
- **What a repository holds today:** one tracker folder, `tracker_dir` in its `shoalmark.toml`, and one `[seats]`
  table ([`shoalmark.toml` L3 and L7](https://github.com/shoalmark/shoalmark/blob/7c93c835d6ac9842bb28a37118822f4a6b8a661b/shoalmark.toml#L3-L7)).
  `--install-hook` wires that repository's hooks
  ([README L312](https://github.com/shoalmark/shoalmark/blob/7c93c835d6ac9842bb28a37118822f4a6b8a661b/README.md#L312)),
  and `--standup DIR …` reads one agenda across the repositories it is given
  ([README L315](https://github.com/shoalmark/shoalmark/blob/7c93c835d6ac9842bb28a37118822f4a6b8a661b/README.md#L315)).
- **What it must cover:**
  1. **The tool's side:** `--standup DIR …`, the gate and the hooks, for a team whose root is a folder inside a
     repository, and for a team whose place is more than one repository.
  2. **The roster spec's side:** how each team's work is kept apart, by a team key on trackers or a tracker folder per
     team, and whether seat names take `<team>.<seat>`.
  3. **FM-100's side:** its refusal lifts once both are in.

## Why

A monorepo can hold several teams' work, and a roster that names a folder as a team's place promises what the tool
cannot serve yet. Until both sides agree, FM-100 refuses such a place rather than serve it in part.

## Done when

Each item names its commit or pull request when it lands.

- [ ] **sealanes/1 is in force,** and it says how teams that share one repository keep their work apart, and how their
  seats are named.
- [ ] **The tool serves a team whose root is a folder:** `--standup DIR …`, the gate and the hooks, each with its tests.
- [ ] **FM-100's `standup-teams` takes such a place** where it refused it, with a test.
- [ ] **The review at the tier its design sets is READY.**

## Ship log

| Date | Event |
|---|---|
| 2026-11-12 | Filed, Proposed, with no release yet: FM-100's one-repository rule lifts here once sealanes/1 is in force. Records only. |
