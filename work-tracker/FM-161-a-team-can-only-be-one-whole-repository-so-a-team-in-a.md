---
id: FM-161
status: In Progress
considered: FM-033, FM-100, FM-166, FM-175, FM-187
tags: process
next: build
triaged: 2026-11-16
tier: P1
hook: "A team can only be one whole repository: a project whose shoalmark.toml sits below the top of its repository is not judged, since the gate reads each tracker at a revision by a path git takes from the top. The organisation's move of the teams' trackers into its own repository, each team a project in a folder of its own, needs this fixed. FM-161-Q2 puts the fix: every gate reads the project's root and configuration, with its tests, and after the move a Shipped tracker names its team's code commit."
ask-id: FM-161-Q2
ask: "Do you take FM-161's fix as proposed, or as changed under other: a project below the git top judged exactly as one at the top, every gate reading the project's root and configuration, with its tests, and after the move a Shipped tracker naming <repository>@<commit> of its team's code?"
ask-kind: ruling
ask-since: 2026-11-25
ask-options: "yes, as proposed | no, not now"
ask-proposal: "yes, as proposed"
answer: "accepted - yes, as proposed"
answered: 2026-11-25
answered-by: holgo99
---

# FM-161 — a team can only be one whole repository, so a team in a folder or several teams in one repository is refused

Seat: the Planner (27f31560) · filed 2026-11-12, on the Auditor's word of that day.

## What is true now

**2026-11-25 — FM-161-Q2 put: a project below the git top judged exactly as one at the top,** on the coordinator's
word of that day.
- **Why now:** the organisation is moving the teams' trackers out of the code repositories into its own repository.
  Each team becomes a project in a folder of its own, with its own `shoalmark.toml`, so this fix is part of the move
  whatever its size.
- **What fails today:** the tool reads a tracker at a revision as `<rev>:<path>`, with the path written from the
  project's root, and git reads it from the top of the repository. Below the top it finds nothing, so the rights rule,
  the Shipped rule and every rule that compares a tracker before and after a commit pass without judging.
  [FM-187](FM-187-the-gate-passes-a-project-below-the-git-top-unjudged-and-a.md) refuses such a run until this lands.
- **What is put:** decisions 7 to 13 below, as FM-161-Q2.
- **What stands:** decisions 1 to 5, as FM-161-Q1 answered them. Decision 6's release left v0.20.3 on 20 November, and
  the release ask names where this ships.

**2026-11-20 — out of v0.20.3, on the Owner's word of 18 November:** "A small v0.20.3: FM-172 and FM-169, nothing else."
The Owner's words of 19 and 20 November widened v0.20.3 to four items
([FM-139](FM-139-v0-20-3-s-rows-sit-in-fm-023-fm-006-and-fm-053-so-no-one.md)), and this lane is not among them. It
leaves the epic and keeps P1 and In Progress; which release takes it is not decided.

**2026-11-16 — FM-161-Q1 answered "yes, as proposed", with the Owner's signature; judged before its first build commit,
keep P1, In Progress.** The lane is in v0.20.3, a chapter of
[FM-139](FM-139-v0-20-3-s-rows-sit-in-fm-023-fm-006-and-fm-053-so-no-one.md), beside FM-166's lanes and built against
their contract: it starts once FM-166's contract lane is READY.

**2026-11-16 — the design, and FM-161-Q1 put,** on the coordinator's word of 15 November. The organisation's trackers
are to live in one repository, each team's in a tracker folder of its own beside the organisation's. sealanes/1's text
says how teams in one repository keep their work apart: a tracker folder per team, or a shared folder with a `team-key`
and id ranges that do not overlap; and it names each bot `<team>.<name>`. So the spec's side of this tracker is settled
by the text, and the tool's side is designed below. The lane enters v0.20.3 only by this ask's signed answer, as
FM-139's item 8 says.

**2026-11-12 — its scope reads "tracker folders":** a team's place is a tracker folder, in its own repository or as a
folder inside a shared one. A team that shares a repository's tracker folder today is kept apart, near term, by a team
key on its trackers and reserved id ranges. Each team's seats need their own identities, since two teams' seats under
one bot address are told apart only by their `Session:` trailer.

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

## Decisions, for the Owner

All six are put as FM-161-Q1.

1. **Places from the roster.** Where a roster is in force, in place or by its lock, the tool serves every place the
   roster gives this repository: each tracker folder with its prefixes and its `new` prefix, its own INDEX, and each
   team's record folder. With no roster, `tracker_dir` and `[kinds]` serve as today.
2. **A shared tracker folder.** Each tracker carries its team's `team-key`. `--new` takes the next free id in its
   team's range, or in its bot's range where the bot has one. `--check` names a tracker in a shared folder that has
   no team key, or whose id lies outside its team's ranges.
3. **Whose work.** The session's bot, `<team>.<name>` as `--whoami` prints it, names the team, and `--new` writes
   into that team's folder.
4. **One install per repository.** The hooks and the gate read every folder. A commit's trackers are found by id in
   any folder, and the rule that a pass judges before the first build commit reads each tracker in its own folder.
5. **The stand-up and the Board.** `--standup DIR …` reads each team's agenda from its own folder, and the Owner's
   view holds every team of the repository.
   [FM-100](FM-100-the-stand-up-prompt-is-code-and-english-on-every-board-while.md)'s `standup-teams` takes a folder
   place, which it refuses today.
6. **The lane.** In v0.20.3, beside [FM-166](FM-166-seats-and-rights-are-kept-in-shoalmark-toml-s-own-tables.md)'s
   lanes: built against their contract, and joined with them. Its review is critical, since it changes
   `shoalmark.py`.

Decisions 7 to 13 are put as FM-161-Q2.

7. **One root for every gate.** The project root is the nearest `shoalmark.toml`, as today.
   - Every read of a file at a revision names its path from that root, as git reads `<rev>:./<path>`, and every list
     of changed paths is taken from it.
   - The rights rule, the Shipped rule, the answer and ask rules, the signers, INDEX and every `--check` rule then judge
     a project below the top exactly as one at the top.
8. **Hooks.** One install per clone. The pre-commit hook runs the gate once for each project a staged path falls in.
9. **Signers.** A relative `gpg.ssh.allowedSignersFile` resolves from the top of the repository, as git resolves it.
10. **The records list.** `[ratio] records` is written from the project root.
11. **Commits of another project.** A project's check skips a commit whose every path lies in another project below it.
    That project's own check judges it.
12. **After the move.**
    - Until the tool reads a team's code repository at a pinned commit, a move to Shipped in a team project names
      `<repository>@<commit>` in a ship-log row, for a code repository its configuration names. The team's daily read
      checks that row, not the gate.
    - A code repository's configuration may say that its trackers live elsewhere. `--check` then says so and passes,
      `--init`, `--new` and the Board refuse there, and `judged_before_build` is false there.
13. **Tests and size.**
    - Each gate's rule classes run again in a project below the top, each with its mutant.
    - The organisation's acceptance checks for the move run against the build before its pull request, each reported
      with its output.
    - Size: about 16 agent hours of build (12 to 24) and 4 of fixes, with a critical review of two or three rounds, so
      about 2.5 working days from the answer. The move waits on it, and v0.21's format migration follows the move, so
      v0.21 moves by about the same.

## Done when

Each item names its commit or pull request when it lands.

- [ ] **The Owner has answered FM-161-Q1.**
- [ ] **sealanes/1 is in force,** and it says how teams that share one repository keep their work apart, and how their
  seats are named.
- [ ] **The tool serves a team whose root is a folder:** `--standup DIR …`, the gate and the hooks, each with its tests.
- [ ] **FM-100's `standup-teams` takes such a place** where it refused it, with a test.
- [ ] **The review at the tier its design sets is READY.**
- [ ] **The Owner has answered FM-161-Q2.**
- [ ] **A project below the git top is judged exactly as one at the top:** each gate, with its tests and mutants.
- [ ] **Hooks, signers and the records list** read from the project root, each with its tests.
- [ ] **After the move:** a Shipped tracker names its team's code commit, and a code repository keeps its trackers
  elsewhere, each with its tests.
- [ ] **The organisation's acceptance checks for the move** pass on the build, each reported with its output.

## Asks

**FM-161-Q1** · 2026-11-16 · Do you take FM-161's decisions as proposed: the tool serves every tracker folder the roster gives a repository, each team's with its prefixes and a shared one by team key and id ranges, in --check, the gate, the hooks, --new and --standup, with the lane in v0.20.3 beside FM-166's?
**answered** — accepted - yes, as proposed · holgo99
**relation** — accepted the proposal
**signed** — 832a472 · G

## Ship log

| Date | Event |
|---|---|
| 2026-11-25 | FM-161-Q2 put: a project below the git top judged exactly as one at the top, every gate reading the project's root and configuration, with its tests; after the move, a Shipped tracker names its team's code commit. Records only. |
| 2026-11-20 | `epic: FM-139` removed: v0.20.3's scope is four items, on the Owner's word of 18 to 20 November, and this tracker is not among them (FM-139). Records only. |
| 2026-11-16 | FM-161-Q1 answered, yes, as proposed; judged before its first build commit, keep P1, In Progress; a chapter of FM-139. Records only. |
| 2026-11-16 | The design, and FM-161-Q1 put: each team's tracker folder, and a shared one by team key and id ranges, served by --check, the gate, the hooks, --new and --standup; the lane in v0.20.3 beside FM-166's. Records only. |
| 2026-11-12 | Filed, Proposed, with no release yet: FM-100's one-repository rule lifts here once sealanes/1 is in force. Records only. |
| 2026-11-12 | Its scope reads tracker folders: near term, a team key and reserved id ranges keep teams in one tracker folder apart, and each team's seats need their own identities. Records only. |
