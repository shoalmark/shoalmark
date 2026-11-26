---
id: FM-161
status: In Progress
considered: FM-033, FM-100, FM-166, FM-175, FM-187, FM-188, FM-189
tags: process
next: build
triaged: 2026-11-16
tier: P1
hook: "A team can only be one whole repository: a project whose shoalmark.toml sits below the top of its repository is not judged, since the gate reads each tracker at a revision by a path git takes from the top. The organisation's move of the teams' trackers into its own repository, each team a project in a folder of its own, needs this fixed. FM-161-Q2 accepted the fix: every gate reads the project's root and configuration, with its tests, and after the move a Shipped tracker names its team's code commit."
---

# FM-161 — a team can only be one whole repository, so a team in a folder or several teams in one repository is refused

Seat: the Planner (27f31560) · filed 2026-11-12, on the Auditor's word of that day.

## What is true now

**2026-11-26 — FM-161-Q4 answered with the Owner's signature: two landings, on two conditions; keep P1, In Progress,**
on the coordinator's word of that day.
- **The conditions:** each first landing carries only that team's `shoalmark.toml` and signers file, which the
  organisation's acceptance script checks; and the tool's README states two landings as the way a project is created
  inside a repository, in the cut's release. The README's sentence is a commit on this lane, which the critical
  review's second round reads.
- **The critical review's finding 3, as the lead answered it:** a folder is another project only once the default
  branch holds its configuration, so the project around it judges every commit of a branch that creates one. The lead
  accepted the cost: a team lands its configuration first, as the two landings do, or builds under the tracker of the
  project around it until that lands. Pass 5 built it on the lane (`62ecf714`).
- The answer is cleared into the record before the cut's rehearsal, so the import carries no standing answer.

**2026-11-25 — FM-161-Q4 put: by which state an import that creates its team's project verifies as the Owner's
there,** on the coordinator's word of that day.
- **Pass 3** (`be885a79`) builds decision 11's part (a): the project around a new project judges the commit that
  creates it. In the organisation's layout, the Owner's import passes the outer project's check and its hooks.
- **The team's own check still refuses it,** exit 4, by
  [FM-033](FM-033-work-is-built-on-trackers-no-pass-has-judged-and-the-board.md)'s build gate. The default branch names
  no Owner for a project the import creates, so the import is not the Owner's there.
  [FM-187](FM-187-the-gate-passes-a-project-below-the-git-top-unjudged-and-a.md)'s frozen rule and
  [FM-189](FM-189-an-import-brings-trackers-without-their-history-so-who-put.md)'s attestation read the same check, so
  neither holds for that project on the import's branch. Pass 3's lines are filed as
  [evidence/FM-161/team-half-pass-3.txt](evidence/FM-161/team-half-pass-3.txt), with the Builder's folder written
  `<workbench>`.
- **Proposed, two landings.** The Owner lands each team's `shoalmark.toml` and signers file on the default branch
  first, in a signed commit that the project around it judges by part (a), and merges it. Then the team's trackers are
  imported. The Owner's added acts: one more signed commit and merge per team. No code.
  - The organisation's acceptance checks, run on a scratch join of FM-187 and FM-161's pass 2, pass checks 1 to 3 for
    both teams this way. As the import is made today, the same join fails the import's hook and checks 2 and 2b:
    [evidence/FM-161/two-landings-runs.txt](evidence/FM-161/two-landings-runs.txt). The hook's refusal in the first
    run is pass 2's, which pass 3 ends.
- **The other way:** the new project's own check reads the commit that creates it by the Owner and signers of the
  project around it. It needs no added act of the Owner's, but it reads past decision 7, which judges a project below
  the top exactly as one at the top, and needs one more build pass and a critical review before the cut's candidate.
- **No, not now:** each team's check refuses its import on the import's branch, so the acceptance's checks 2 and 2b
  fail there.

**2026-11-25 — FM-161-Q3 answered "yes, as proposed", with the Owner's signature: every part of decisions 7 to 13 is
in the tracker cut's release; keep P1, In Progress,** on the coordinator's word of that day. None goes to a v0.20.4, so
[FM-188](FM-188-rulings-collide-unseen-an-ask-is-put-and-answered-without.md)-Q1's decision 7 stands. The answer is
cleared into the record before the cut's rehearsal, so the import carries no standing answer.

**2026-11-25 — FM-161-Q3 put, as a change to FM-161-Q2: where each part of decisions 7 to 13 ships,** on the
coordinator's word of that day.
- **Proposed:** every part in the tracker cut's release, none in a v0.20.4. Each part is built on the lane, in the
  Builder's passes 1 and 2, except decision 11's part (a), which pass 3 builds. Nothing of the lane is pushed or
  reviewed yet. The table under *Decisions*, *Put as FM-161-Q3*, gives each part's place, its agent hours, and what does
  not work until v0.20.4 if it goes there.
- **A part placed in v0.20.4** changes FM-161-Q2's answer, and reopens
  [FM-188](FM-188-rulings-collide-unseen-an-ask-is-put-and-answered-without.md)-Q1's decision 7, which put no v0.20.4.
- **Not put:** reading a commit that creates a project by the state of the project around it. It is put only if pass
  3 still refuses the Owner's import, with pass 3's output beside it.

**2026-11-25 — FM-033's gate in a code repository after the move,** for the records review of FM-161-Q2's filing.
- Decision 12, as FM-161-Q2's signed answer takes it, makes `judged_before_build` false in a code repository whose
  trackers live elsewhere. So [FM-033](FM-033-work-is-built-on-trackers-no-pass-has-judged-and-the-board.md)'s gate
  does not run there.
- Until the tool reads the team's tracker project at a pinned commit, nothing in the code repository holds that
  rule. The team project's daily read checks the ship-log row that names the code commit.
- [FM-175](FM-175-trackers-are-prose-the-gate-cannot-read-so-each-becomes-a.md)'s decision 9 moves the trackers only
  with v0.21.0, after that pinned read. [FM-188](FM-188-rulings-collide-unseen-an-ask-is-put-and-answered-without.md)-Q1 puts its amendment, so that the move comes first.

**2026-11-25 — FM-161-Q2 answered "yes, as proposed", with the Owner's signature; keep P1, In Progress,** on the
coordinator's word of that day. Decisions 7 to 13 stand as put. The build starts from main, from patches prepared
before the answer: the tool lead's first patch takes decisions 7, 9, 10 and 11, and a second the rest. Its review is
critical. Which release takes it is not decided: [FM-188](FM-188-rulings-collide-unseen-an-ask-is-put-and-answered-without.md)-Q1 puts it.

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
  which release takes this is not decided.

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

**Put as FM-161-Q3: where each part ships.** Pass 1 built decisions 7, 9, 10 and 11 as one patch, in about 5 agent
hours. Pass 2 built the rest in about 2 more.

| Part | Proposed | Built, and agent hours left | If in v0.20.4, what does not work until then |
|---|---|---|---|
| 7. One root for every gate | in the cut | pass 1; left: its review | Nothing below the top is judged, so the cut cannot be made: [FM-187](FM-187-the-gate-passes-a-project-below-the-git-top-unjudged-and-a.md) refuses every run in a team's folder. |
| 8. Hooks, once per project | in the cut | pass 2; left: its review | The commit hook judges only the top's project. A team's rules hold a commit only at `--check` on its branch and in CI. |
| 9. Signers from the top | in the cut | pass 1; left: its review | In a team's folder, the signers file's symlink, other-checkout and no-default-branch checks read a path that is not there. |
| 10. The records list from the project root | in the cut | pass 1, with its wording and the refusal of an entry written from the top in pass 2; left: its review | In a team project, `[ratio] records` is not matched against the paths git names, so a commit that changes only records counts, for the Shipped rule, as one that built something. |
| 11. Commits of another project | in the cut | pass 1; part (a), a path's project decided at the commit's parent, in pass 3, about 2 | The organisation's own check judges every team commit as its own, and its build gate refuses each one not built under an `In Progress` tracker of its own. Without part (a), a commit that creates a project passes the project around it unjudged. |
| 12. A Shipped tracker naming `<repository>@<commit>` | in the cut | pass 2; left: its review | No team tracker in the organisation's repository can move to `Shipped`, since its build commit is not in that history: it can only be `Closed`. |
| 12. A code repository whose trackers live elsewhere | in the cut | pass 2; left: its review | After the cut, `--check` and the commit hook in the code repository refuse every run, since its tracker folder is gone. |
| 13. Tests and size | in the cut | rows and mutants with each part; left: the critical review, two or three rounds, about 5, and the acceptance run, about 1 | — |

**After the cut, can a tracker in the organisation's repository be moved to `Shipped`?** Under the proposal, yes:
- A tracker of the organisation's own project, at the top, as today: the commit that built it is in that history.
- A team's tracker, by decision 12: a ship-log row names `<repository>@<commit>` for a code repository the team's
  configuration names. The gate takes the row without reading that repository and says in one `--check` line how many
  moves rest on such rows; the team's daily read checks the commit. A repository the configuration does not name counts
  as no commit.
- If decision 12's ship-log row goes to v0.20.4, no: until then a team's tracker can only be `Closed`.
- The trackers the import brings already `Shipped` stay so, under FM-187's frozen rule, once the cut's release holds both
  lanes.

**Which gates below the top have run their tests?** Each gate ran its rows at the top and below it on pass 1's tool:
104 rows and 35 mutants, all green on Python 3.15.0 and 3.9.6. The two runs printed the same output byte for byte:
[evidence/FM-161/below-top-rows-pass-1.txt](evidence/FM-161/below-top-rows-pass-1.txt), sha256
`be53f14e753f25a4a36b6168edafff040d7ea24ddb38b35904db562c16209f7d`.
- **The rules:** the rights rule, for made commits and for the commit being made, the Shipped rule, `[ratio] records`,
  the ask rule, the answer rules, the ask-id rules, INDEX, the signers file, the queue's reads, the working tree and a
  partial clone.
- **Decision 11's skip,** for the build gate, the guard of the Owner's two sections and the signers file, and the
  Owner-commit signature rule.
- **The shapes of the organisation's acceptance checks 1 to 3.**
- **Not yet run:**
  - the rows of pass 2 (the hooks once per project, the ship-log row, trackers elsewhere) and of pass 3 (part (a)),
    whose hand-backs are not in;
  - CI's full suites on the lane;
  - the organisation's acceptance on one candidate that holds FM-187 and FM-161; until both merge, a scratch join of
    the two lanes stands in for that run.

## Done when

Each item names its commit or pull request when it lands.

- [ ] **The Owner has answered FM-161-Q1.**
- [ ] **sealanes/1 is in force,** and it says how teams that share one repository keep their work apart, and how their
  seats are named.
- [ ] **The tool serves a team whose root is a folder:** `--standup DIR …`, the gate and the hooks, each with its tests.
- [ ] **FM-100's `standup-teams` takes such a place** where it refused it, with a test.
- [ ] **The review at the tier its design sets is READY.**
- [x] **The Owner has answered FM-161-Q2.** · `453601f`, #330 (`c069017`)
- [x] **The Owner has answered FM-161-Q3.** · `e2c964b`, #335 (`72a8415`)
- [x] **The Owner has answered FM-161-Q4.** · `e7f58a2`, #339 (`62d5f15`)
- [ ] **The README states two landings** as the way a project is created inside a repository, in the cut's
  release.
- [ ] **A project below the git top is judged exactly as one at the top:** each gate, with its tests and mutants.
- [ ] **The hooks run the gate once for each project a staged path falls in, a relative signers file resolves from
  the top, and the records list is written from the project root,** each with its tests.
- [ ] **After the move:** a Shipped tracker names its team's code commit, and a code repository keeps its trackers
  elsewhere, each with its tests.
- [ ] **The organisation's acceptance checks for the move** pass on the build, each reported with its output.

## Asks

**FM-161-Q1** · 2026-11-16 · Do you take FM-161's decisions as proposed: the tool serves every tracker folder the roster gives a repository, each team's with its prefixes and a shared one by team key and id ranges, in --check, the gate, the hooks, --new and --standup, with the lane in v0.20.3 beside FM-166's?
**answered** — accepted - yes, as proposed · holgo99
**relation** — accepted the proposal
**signed** — 832a472 · G

**FM-161-Q2** · 2026-11-25 · Do you take FM-161's fix as proposed, or as changed under other: a project below the git top judged exactly as one at the top, every gate reading the project's root and configuration, with its tests, and after the move a Shipped tracker naming <repository>@<commit> of its team's code?
**answered** — accepted - yes, as proposed · holgo99
**relation** — accepted the proposal
**signed** — 453601f · G

**FM-161-Q3** · 2026-11-25 · Do you place FM-161-Q2's decisions 7 to 13 as proposed, every part in the tracker cut's release and none in a v0.20.4, or as changed under other, where a part in v0.20.4 changes FM-161-Q2's answer and reopens FM-188-Q1's decision 7?
**answered** — accepted - yes, as proposed · holgo99
**relation** — accepted the proposal
**signed** — e2c964b · G

**FM-161-Q4** · 2026-11-26 · How does an import that creates its team's project verify as yours there: as proposed, you land each team's shoalmark.toml and signers file first, then its trackers, or the tool reads that commit by the Owner and signers of the project around it?
**answered** — accepted - other: yes, two landings, on two conditions: (1) each first landing carries only that team's shoalmark.toml and signers file, checked by the acceptance script; (2) the tool's README states two landings as the way a project is created inside a repository, in the cut's release. · holgo99
**relation** — accepted with a change
**signed** — e7f58a2 · G

## Ship log

| Date | Event |
|---|---|
| 2026-11-26 | FM-161-Q4 answered: two landings, on two conditions; the answer cleared into the record; the critical review's finding 3 recorded as the lead answered it; keep P1, In Progress. Records only. |
| 2026-11-25 | FM-161-Q3 answered, yes, as proposed: every part of decisions 7 to 13 in the cut; the answer cleared into the record; keep P1, In Progress. Records only. |
| 2026-11-25 | FM-161-Q3 put, as a change to FM-161-Q2: each part of decisions 7 to 13 in the tracker cut's release or in a v0.20.4, every part proposed for the cut; pass 1's rows below the top filed as evidence. Records only. |
| 2026-11-25 | The records reviews' findings fixed forward: FM-033's gate in a code repository after the move, the first patch's order named as the lead's, the release FM-188-Q1's, and the hooks, signers and records list item worded as decisions 8 to 10. Records only. |
| 2026-11-25 | FM-161-Q2 answered, yes, as proposed; keep P1, In Progress; the build starts. Records only. |
| 2026-11-25 | FM-161-Q2 put: a project below the git top judged exactly as one at the top, every gate reading the project's root and configuration, with its tests; after the move, a Shipped tracker names its team's code commit. Records only. |
| 2026-11-20 | `epic: FM-139` removed: v0.20.3's scope is four items, on the Owner's word of 18 to 20 November, and this tracker is not among them (FM-139). Records only. |
| 2026-11-16 | FM-161-Q1 answered, yes, as proposed; judged before its first build commit, keep P1, In Progress; a chapter of FM-139. Records only. |
| 2026-11-16 | The design, and FM-161-Q1 put: each team's tracker folder, and a shared one by team key and id ranges, served by --check, the gate, the hooks, --new and --standup; the lane in v0.20.3 beside FM-166's. Records only. |
| 2026-11-12 | Filed, Proposed, with no release yet: FM-100's one-repository rule lifts here once sealanes/1 is in force. Records only. |
| 2026-11-12 | Its scope reads tracker folders: near term, a team key and reserved id ranges keep teams in one tracker folder apart, and each team's seats need their own identities. Records only. |
