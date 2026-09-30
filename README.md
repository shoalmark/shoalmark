# shoalmark

## How to get a better-performing human owner

Agents do not wait for tools. They wait for their human. Asked what slows them most, three independent agents gave
the same answer, by a wide margin: **the Owner's unanswered questions** — one question, open three days, held three
packages. And where the human does keep up, he keeps up by not reading: in the repository this tool came from,
**200 pull requests were merged in 22 days, 85 % of them less than a minute after opening, none with a review.**
Blocking and stamping have one root — a person asked for many small decisions in the middle of the work.

So the human is asked **once, earlier, and in writing**: what the work is for, what it must never do, what *done* has
to prove. He sees what waits for him, how long, and what it blocks — first, above everything else. The agents get what
they need to run start to finish: state that outlives a session, one source of truth, a gate that refuses a false
*done*. **Less work and distraction for the human; more throughput and less friction for the agents.**

**What exists today:** the tracker, the gate, the board with *waiting for you* on top, `next: owner`, a cold-start
answer in one command (`--next`) — on git and Subversion, on Windows, macOS and Linux, in any language.
**What is the direction, not yet built:** the signed mandate, questions that carry a default and a deadline,
evidence-checked *done*, the digest — explored, with what would kill each claim, in shoalmark's own tracker
(`FM-005`, `docs/work-tracker/evidence/FM-005/design.md` in its repository). Trust is earned there from the Owner's
own answers before anything runs unattended.

**A convention, Stage 0:** a [`requirements/`](https://github.com/shoalmark/shoalmark/blob/main/requirements/README.md) folder holds one line per requirement — id, *shall*,
source, acceptance criterion — one text for developer and tester; a tracker cites the id. shoalmark has the
convention only: checks and traceability are later.

*A shoal mark is a mark set to show shallow water — a stake or a buoy. It tells a shoal where not to run aground.*

---

A work tracker that lives in the repository it tracks: one Markdown file per work item, one Python file that reads
them all, a gate on every commit. No server, no database, no dependency beyond Python 3.9.
**This page is written for the agent that has to use it.** Find your situation, do what it says.

| You are… | Go to |
|---|---|
| starting a session in a repository that has `tools/shoalmark/` | [§1 Start](#1-start--what-do-i-work-on) |
| about to file something | [§2 File](#2-file--look-first) |
| stopping, with work left | [§3 Stop](#3-stop--leave-the-fix) |
| asked to run a triage pass | [§4 Triage](#4-triage--you-judge-the-command-applies) |
| blocked by the gate | [§5 The gate refused me](#5-the-gate-refused-me) |
| adding it to a repository | [§6 Install](#6-install-and-upgrade) |
| a seat starting a session, or reading who ran what | [§6 Sessions](#sessions) |
| making it know about releases, deploys, anything of the repository's own | [§7 The deriver](#7-the-one-seam-a-deriver) |
| changing shoalmark itself | [§8 Working on shoalmark](#8-working-on-shoalmark) |
| giving the board a name, a logo, colours, another language | [§9 Branding](#9-branding-the-board) |

`<cmd>` below is `python3 tools/shoalmark/shoalmark.py` in a repository that vendors it — or whatever command that
repository's own messages name. Every command finds the repository by itself: the nearest `shoalmark.toml`, else the
git toplevel.

## The five rules

1. **The tracker is canonical.** Spec, state and record of a piece of work live in its tracker — never in a side
   plan, a chat or a TODO comment. *What is true now* is rewritten in place; only the ship log is append-only.
2. **Look before you file.** The default is a slice of a tracker that exists, not a new one.
3. **An id never changes and says nothing that can.** `MSR-012` — the kind of work is a tag, a story is a field.
4. **The seat judges, the command applies.** Never hand-edit `triaged:` `tier:` `rank:` or a park.
5. **Close out by asking what this made obsolete — and delete it in the same change.**

## 1. Start — what do I work on?

```bash
<cmd> --next
```

Prints the Owner's current path, then the ranked work in order — each with its next move, what it still needs, and
the opening of its *What is true now* — and ends with `START WITH: <id>`: the first ranked tracker whose move is
yours (`review` · `run` · `script` · `build`), not the Owner's (`owner`) and not a wait. Read that tracker. Work on
a branch that carries the id: `feat/msr-012-slug`, `fix/msr-013-slug`.

Nothing ranked? It says how many trackers wait for a triage pass. No path written? Only the Owner writes it
(`<tracker dir>/TRIAGE.md`) — ask; do not invent one.

## 2. File — look first

```bash
<cmd> --new "what is wrong, in one sentence"
<cmd> --new "what is wrong, in one sentence" --tags bug     # the kind of work, written into `tags:` as it is filed
```

It prints the closest existing trackers **before** it writes the file. Open the top hits. If one of them already
owns this, add a slice to it and delete the new file. Otherwise fill the front matter:

```yaml
---
id: MSR-014                 # written for you; equals the filename and the first heading
status: Proposed            # Proposed · In Progress · Parked · Reserved · Shipped · Closed
considered: MSR-003, MSR-009   # what you held this against — or: none. REQUIRED: the gate refuses the file without it
tags: bug                   # at most 3, from [tags] in shoalmark.toml — a closed vocabulary
epic: MSR-003               # optional: the story this is a chapter of
hook: "The problem as filed, in two or three sentences — this is the INDEX row."
---
```

Then the body: `# MSR-014 — title` · `## What is true now` · `## Why` · `## Done when` · `## Ship log`.
`<cmd> --schema` prints every key, its shape and **who may write it**.

**The filing freeze.** Where `shoalmark.toml` sets `freeze_at`, and that many trackers or more are open, only a product
defect is filed — a filing that carries `tags: bug`, as `--new "…" --tags bug` writes it. Anything else goes as one line
into the closest open tracker's body (the ones `--new` prints first), or waits. `--new` refuses the rest, exit 4, with the
count and the line; `--check` says the freeze holds in one line and exits as it would have. `--tags` takes a
comma-separated list from `[tags]`, at most three, case aside; a tag outside the vocabulary is refused before anything
is written, and `--tags` without `--new` is refused. The tag that passes is `freeze_tag` — `bug` unless the
configuration names another; where `[tags]` does not carry it, the freeze refuses nothing and `--check` says so in one
line.

## 3. Stop — leave the fix

The next session starts cold. Before you stop:

- Rewrite **What is true now** so its opening says what is left — one remainder, stated plainly.
- Set **`next:`** to the next move: `review` (built, a branch waits to merge) · `run` (built, a real run is owed) ·
  `wait` (a date or an event) · `owner` (the Owner's act alone) · `script` (mechanical) · `build` (anything else).
- On a `build`, with the tracker open, set **`kind-of-problem:`** — `obvious` (a script could do it) ·
  `complicated` (found by reading) · `complex` (found only by running) · `chaos` (harm now).
- Waiting on something? **`blocked-by: MSR-009, Owner — the ruling awaited`**. *Blocked* is derived and clears itself.
- Done? `status: Shipped` (merged — not deployed) and remove `rank:`. **A story stays open while a chapter is.**

## 4. Triage — you judge, the command applies

```bash
<cmd> --triage        # writes <tracker dir>/evidence/triage/triage-<today>.md and prints the rules
```

Fill the **Verdict** and **Reason** cells, row by row, from the row. Run the same command again — every ten rows
or so, and at the end: it applies what you filled, refreshes `INDEX.md`, keeps your rows, lists what is left.

| Verdict | Means | The command writes |
|---|---|---|
| `keep P1 #2 build` | worked on in the last 7 days, or the current path names it, or it is P0/P1 today | `triaged:` `tier:` and — if given — `rank:` (1–10, one tracker each) and `next:` |
| `epic MSR-003 P2` | a keep that is a chapter of a story | the same, plus `epic:` |
| `park P3` | fails the keep test; a real remainder, nobody on it. **P2 or P3 only — harm is never parked** | `status: Parked` `tier:` `triaged:` |
| `merge MSR-003` · `close` · `fix` | its scope belongs elsewhere · retired · its status is simply wrong | `triaged:` only — **you finish these by hand**, as the rules say |

**A raise** is one line under a tracker's `## Raised` — `- <date> · <who> · <fact> · <source> · undermines: <what>`. Dated
after the tracker's `triaged:` and naming a signed rule it undermines — `path N` of the current path, or `<ID>'s answer`
of a tracker he answered — it puts an open tracker under *triage* and on the next worksheet, marked RAISED, with the raise
in its Now cell: *a raise naming a signed rule re-judges the tracker the same day; any other raise waits for the next
pass* (the Owner's answer, FM-033). A day decides: a raise written after the same day's pass is re-judged by that seat's
own re-run. **One tracker, two rows**: the re-judgement is a second filled row below the first, and the LAST filled row
in the file is applied; the earlier is left as it is — the record of the first judgement — and every run names it,
*superseded on this sheet by the later row* (FM-036). Never strike it to make the other apply.

Never write a note into a tracker during a pass; the reason lives in the worksheet. Never touch the current path.
The pass is the seat's judgement, dated by its commit; the Owner lands it by merging; a row he disagrees with is
re-made by the seat on his word, or ruled by his signed answer — a merge rules nothing: an answer is written and
signed, and a merge is not one.

## 5. The gate refused me

`<cmd>` regenerates `INDEX.md`; `<cmd> --check` only looks. Exit codes: **0** green · **3** drift — a tracker
changed and nothing regenerated: run `<cmd>` · **4** a violation — *fix the tracker; regenerating will not clear
it* · any other code comes from the repository's deriver (§7) and its message says why.

| It says | Do |
|---|---|
| `a new tracker says what it was held against` | run `--related <id>`, open the hits, fill `considered:` |
| `` `xyz:` is not a front-matter key — did you mean … `` | fix the typo; anything else belongs in the body |
| `` `key:` is <meaning> — <shape> — got … `` | the value does not fit the key's shape; `--schema` shows it |
| `dangling link -> FILE (did you mean …?)` | the id is right and the slug moved: use the file it names |
| `duplicate tracker id` · `identity drift` · `H1 drift` | filename, `id:` and the first heading must carry one id; renumber the later filing — nothing is ever deduplicated for you |
| `` `rank:` … remove it when the tracker ships, parks or closes `` | do that |
| `` `next: owner` without `ask-proposal:` `` | an ask carries the move the seat would make: write it, with `ask-kind:` and `ask-since:` |
| `` `ask:` is ONE question `` | one `?`, at the end, 300 characters; the context goes in the body |
| `` `ask:` is the same question as <id> `` | ask on that tracker, or say in `considered:` why this one differs |
| `the answer is being removed and the exchange is nowhere in the body` | `--clear-ask <id> <next move>` — it keeps the record |
| `--answer: the working tree has changes … Changed: …` | commit or stash what is yours; where it says *a failed earlier `--answer`*, run the one command it prints — it restores only the tool's leftovers — then the answer command it prints |
| `` `answerers = ["x signed"]` asks for a signed answer, and `[seats] …` … is not signed `` | add `signed` to that seat, or remove `answerers` — with `[seats]` it is not read for answers |
| `` `x@seat` is … the seat `y`, which does not hold `z` `` | that change needs a right this seat has not got: `[rights]`, §6 |
| `wait: not an answerer (<author>)` (`--queue`) | the `answer/*` pull request's answer, `done:` or `due:` commit — its head, or the newest that wrote one of those lines where only review files follow it — is by someone who may not answer — signed or not, it is not the Owner's answer: do not merge it, and find out who pushed it |
| `wait: a seat's commit on your answer branch (<sha>, <author>)` (`--queue`) | the `answer/*` pull request carries, below his answer, `done:` or `due:` commit, a commit that is not his signed one and touches more than review files — `--answer`, `--done` and `--due` cut `answer/<id>` from the branch he stands on, so an act given on a seat's unmerged branch carries its commits, and a merge would take them in as his: do not merge it. The seat's commit lands on the default branch first, by its own pull request — the branch it came from (`git branch -r --contains <sha>`), else a branch the seat pushes at it — and then this one reads `merge: your answer`, your act as you signed it; nothing of yours is deleted (FM-030 C). `--answer`, `--done` and `--due` on that tracker say the same while it waits |
| `wait: an unverified commit in your name on your answer branch (<sha>)` (`--queue`) | below your act is a commit in your name that does not verify as you — unsigned, or signed with a key the default branch's signers file does not hold for you. The tool's own refusal record (`<ID>: --<act> refused — …`, one line under `## Acts`, unsigned by design) is not one: it is read as a review file's commit is. A seat can write your name: do not merge it; find out who made the commit, and let it land on the default branch by its own pull request first, as the row above says — and the tool's own refusal record is admitted only where the tracker's text proves it: one line under `## Acts`, nothing else changed (RV-715) |
| `wait: the base <base> is not fetched here — fetch it; the commits below <sha> are unread` (`--queue`) | this clone has not fetched the pull request's base — a single-branch clone fetches one branch — so it cannot see the commits below your act and says no merge: `git fetch origin <branch>:refs/remotes/origin/<branch>`, then `--queue` again |
| `wait: answer not verified here — <why>` (`--queue`) | the Owner's `answer/*` pull request is signed, and this clone cannot check it — the same cause, the same cure as the next row |
| `it is signed, but not with a key <file> on <default branch> holds for that identity` | the commit is signed with a key the gate does not trust for that email — it reads the default branch's copy of the signers file (§5). A new key lands there first: the Owner's signed commit to the file, merged — then the same commit verifies, nothing re-signed; `--answer` left it on `answer/<id>`, unpushed: push that branch |
| `it is signed, but this clone cannot verify: …` | the commit is signed; this clone cannot check it. Set `gpg.ssh.allowedSignersFile` to the repository's signers file (SSH), or import the key (GPG) — the signing page says how. The exit is the same until it verifies |
| `carries no Session: trailer` · `a session id is eight hex characters` · `names the seat …` | set `seat.session` in your worktree: the harness's id, or `<parent>/<seat>-<n>` for a sub-agent of your own seat (§6 *Sessions*) |
| `--new: filing freeze — N open, at or above M` | only a product defect is filed now: `--new "…" --tags bug`; add the rest as one line to the closest open tracker, or wait until fewer than `freeze_at` are open |
| `--answer: X is answered already` | an answer is never overwritten in place: `--answer X revoke "<reason>"` takes it back, `--answer X accept\|reject "<option>" --supersede` replaces it — the old one moves into the ship log |
| `` `answer/x` exists and is not merged `` | the refusal says what is on it. Your commits: merge it first — or, where it names the act open there, `git switch answer/x` and run `--done`/`--due` on it. Nothing of yours: `git branch -D answer/x`, the one case it names. Nothing unmerged is deleted for you |
| `` refused: commit … changes the text under `## The intent` `` · `## The current path` · `renames or removes the heading` · `deletes or moves …/TRIAGE.md` · `points the tracker directory elsewhere` · `brings a text … that no parent had` (FM-037) | the two sections are the Owner's, and only his signed commit changes them. Every commit of the branch is judged, so a revert does not clear it — the revert changes the text too: carry the work onto a fresh branch without that commit (never force a pushed one), and put the change to him as an ask — `ask:` in its tracker, one sentence, `ask-kind: ruling`, `ask-since:`, `next: owner`. He commits it himself, signed. Below the table |
| `changes the signers file …` (FM-037, AU-19) | the keys his signature is verified against are his too: a seat proposes a key as an ask, and he commits it, signed |
| `wait: TRIAGE.md changed unsigned` (`--queue`) | a commit on that branch changes his intent or current path and is not his signed commit — the refusal above, read on the pull request: do not merge it |
| `names no tracker` · `not judged` · `Parked` · `not In Progress` (`judged_before_build`) | a commit that changes a path outside the tracker directory is built under a tracker a pass has kept `In Progress` — at the commit's parent. Name it: the id in the subject, or a branch `<kind>/<NNN>-…`; ask for the pass if it is not judged. Never write `triaged:` by hand, and never build first and judge after |
| `A story is open while a chapter is` | keep the story `In Progress` with `next: wait`, or move the chapters first |
| `… differs from its PIN` | someone edited the vendored tool in place. Never do that: change it upstream, vendor again |

**Only the Owner changes his intent and his current path** (FM-037, his word of 2026-09-25). `--check` walks the
branch's own commits — `HEAD` less `origin`'s default branch, merges included — and reads, for each, what a pass reads
as his: the text under `## The intent` and `## The current path` of `TRIAGE.md` (the repository's `[headings]` names, or
the English ones), from its heading line to the next `## `, each commit under its own `shoalmark.toml` — its
`tracker_dir` names the file. Byte for byte: **whitespace counts**, since the text is printed as written and a comparison
with nothing normalised has nothing to slip past. A text that differs from the parent's is a change — a heading renamed or
removed, `TRIAGE.md` deleted, moved away from its name or out from under the tracker directory, `tracker_dir` pointed at a
directory whose `TRIAGE.md` reads otherwise or not at all; a merge's change is only a text no parent had (FM-019), what it
carries having been judged on the commit that made it. A change is refused, exit 4, unless it is **the Owner's signed
commit**: `%G?` `G`, the signer principal (`%GS`) the author's email, and the author the seat holding `answer` in the
**default branch's** `[seats]` — never the branch's own, so a branch that names a seat the Owner, or drops `signed` from
his, does not judge itself. **Nor its keys** (the Auditor seat's AU-19): a signature is verified against the *default
branch's* copy of the signers file `gpg.ssh.allowedSignersFile` names, where that file sits in a checkout of this
repository — never the branch's own — so a branch that appends its own key under his email vouches for nothing; the
answer gate and `--queue` verify the same way. The signers file itself — that one, and `<tracker dir>/allowed_signers` —
is kept like the two sections: a change to it is refused unless it is his signed commit. Its first version therefore
lands on the default branch by his own hand: a branch cannot prove a key the default branch does not hold — until it
is there, no SSH signature verifies against a signers file in a checkout (the cold re-review's R2), and a new key
verifies once it is merged there: `--answer` asks the same test before it pushes (R1). `## Passes`
and the rest of the file stay open to seats; a scaffold where there was none is accepted — any whose words the readers
know (`--init`'s, the German one, 0.1.0's bare lines: AU-20). *The reading of a move* (the pass's R7): the guard judges what the tool reads, so a move of
the whole tracker together with its key that leaves both sections byte-identical is no change — `ae1f05e`, the tracker's
move out of `docs/`, is accepted on its text, not by its date; refusing every move and exempting that one by date was
the alternative, not taken, because it keys a hole to a calendar and refuses a move that leaves every word of his as he
wrote it. **The commit-msg hook** refuses a seat's such commit before it is made; it sees the author only — git signs
after its hooks run — so the Owner's own passes it on his name and `--check` on the branch, the gate, judges the
signature. `--queue` reads such a branch `wait: TRIAGE.md changed unsigned`. Where his seat is not `signed`, it proves
**the author only**, and says so. **Subversion is out of scope**: its working copy carries no signature, so nothing there
can tell his commit from a seat's. **Its limit** (FM-007): a commit signed with the Owner's key passes; at tier 0 any
process on his account holds that key.

Never `--no-verify`. Never hand-edit `INDEX.md` — it is generated.

## 6. Install and upgrade

```bash
git clone --branch vX.Y.Z <shoalmark-url> /tmp/shoalmark           # a release: a clean clone at its tag
python3 /tmp/shoalmark/shoalmark.py --vendor <repo>/tools/shoalmark  # a pinned, self-contained copy + PIN (sha256)
cd <repo>
python3 tools/shoalmark/shoalmark.py --init --key MSR               # shoalmark.toml · TRIAGE.md · .gitignore · the contract in AGENTS.md · a CLAUDE.md router
python3 tools/shoalmark/shoalmark.py --install-hook                 # plain git hooks; a hook that is not shoalmark's is never overwritten
```

Then **the Owner** writes the intent and the current path in `<tracker dir>/TRIAGE.md`. Nobody else edits those two
sections. The intent is three lines in his own words about the repository as a whole, never one feature of it: what
this repository, all of it, is for · what is true when it works · what no pass or seat may do to get there. `--init`
writes an example in italics, a whole product, for him to overwrite:

```markdown
- **for** — *e.g. a village library's lending, all of it: members, loans, returns and the shelf in one record the librarian trusts*
- **so that** — *e.g. a member finds a book and a librarian finds a member in one look, and nothing on loan is lost*
- **never** — *e.g. lend what the catalogue does not hold, or drop a member's record before their last loan is back*
```

A pass reads everything he writes under the intent and leaves out only the scaffold's own lead-in and examples,
recognised by their exact text, never by italics, bold or length: an example with one word changed is his.

**`--vendor` vouches for what it copies.** It refuses — exit 4, nothing written — a source that is not the whole tool
(it names the missing files), a source that is no release (a git checkout whose HEAD is exactly at `v<VERSION>`, with
a clean tree — it names the HEAD and the changed paths), and a copy in the target that was edited in place. A consumer
runs a release, never a working copy. `--partial` copies an incomplete source anyway and `--allow-untagged` a working
copy; each says so in the PIN. The PIN's first line is the manifest —
`# shoalmark X.Y.Z · tag vX.Y.Z · commit <sha> · vendored <date> · complete` — and the consumer's `--check` checks it
(that exact form, the tag against the version, the version against the copy's `VERSION`) before it prints where the
copy came from, with a warning for an untagged or partial one; any other line is named, and the copy called
*unverified*.

Upgrade: `--vendor` again from the new release's clone (it names the tag, prints what changed since the version it
replaces, and refuses a copy that was edited in place), then `--init` again to refresh the contract between its markers
— your text outside them is kept.

What lives where, by convention — no setting names any of it:

| Path | What |
|---|---|
| `shoalmark.toml` | optional. `name` · `tracker_dir` (default `docs/work-tracker`) · `blob` (forge URL prefix) · `triage_days` (7) · `freeze_at` (0, off — the filing freeze, §2) · `freeze_tag` (`bug`, the tag that passes it) · `judged_before_build` (false — a pass judges before the first build commit, §5) · `[paths]` `reviews` (`evidence/reviews/` — where the Reviewer's files sit, a glob allowed; `--queue` reads it) · `[ratio]` `records` (the tracker directory, `tracker_dir` — the prefixes `--ratio` counts as records; a trailing slash is a directory, a plain path a file) and `exclude` (`[]` — prefixes left out of both sides); without the section `--ratio` has nothing to count · `[kinds]` id prefix → INDEX section · `[considered_from]` · `[tags]` · `[seats]` · `[rights]` (§*Seats*) · `[headings]` the ten section names the tool reads and writes (`state` `why` `done` `log` `asks` `raised` `acts` in a tracker, `intent` `path` `passes` in `TRIAGE.md`) — for a repository that is not in English; the English names stay understood |
| git · Subversion · Windows | `--install-hook` wires what the system has: git hooks, or on Subversion the TortoiseSVN hook properties and `svn:ignore`. **`svn commit` on the command line runs no hook — run the tool first.** On Windows the command is `python`. CI proves all three systems |
| what an ask must be | ONE question — one `?`, at the end, at most 300 characters — with `ask-kind:`, `ask-since:` and `ask-proposal:`, and never the same question as another open tracker's. At most five `ask-options:`, 120 characters each. The gate refuses the rest, and the board shows what got in anyway as *N asks sent back — not for you* |
| drafting an ask | an `ask:` with `next: review` is a **draft**: any seat writes one (the question and its `ask-options:`), it needs no proposal and the Owner never sees it. The Principal rewrites it, orders the options, sets `ask-proposal:`, `ask-since:` and `next: owner` — that is what puts it in front of him |
| what needs the Owner | `ask:` (one sentence he can answer) · `ask-kind:` ruling · action · determination · ceremony · `ask-since:` — with `next: owner`. The board leads with them; `--owner` is the digest a session ends its last message with; `--standup` is the agenda of his one sitting and `--standup FILE.ics` its calendar invite (`standup = "09:00"` in `shoalmark.toml`). Both list, after the asks, *ACTS — yours, with their time*: missed and overdue first, then what falls due, then *no date yet*, each with its `due:` and what it is |
| what to merge | **`--queue`** — the open pull requests, read from GitHub with `gh` (`origin` fetched once), ONE action each, in the order to take them: what he can act on first, then what waits, the oldest first inside each. A pull request from a fork — GitHub's `isCrossRepository` — reads `wait: from a fork, read it yourself` before every other rule: its commits supply no verdict and no carry-over, for it or for any other pull request. `merge` — a verdict names its head, or a head that only review addenda follow (commits touching nothing but the review folder — `[paths] reviews` in `shoalmark.toml`, `evidence/reviews/` by default, a glob such as `evidence/*/` allowed — and `sessions.md`; the verdict commit's own `review*.md` counts wherever it sits under `<tracker dir>/evidence/`, so a head that IS the verdict is covered), and `git merge-tree` merges it clean · `closes with PR N` — its head is inside N's · `close: carried into PR N` — every commit of its own is on N's branch, as the commit or as the same patch · `wait: conflict in <paths>` · `wait: TRIAGE.md changed unsigned` — a commit of its own changes the Owner's intent or current path and is not his signed commit (§5, FM-037; `wait: TRIAGE.md change not verified here — <why>` where it is signed and this clone cannot check it) · `wait: no verdict on <sha>` · `wait: NOT READY (<verdict>)`. An `answer/*` pull request is the Owner's own answer, `done:` or `due:`, and needs no verdict, and is read by his answer, `done:` or `due:` commit — the newest of its own that changed an `answer:`, `done:` or `due:` line, where only review files follow it (a Reviewer's docs pass on the answer: the review folder, `sessions.md`, a `review*.md` anywhere under `<tracker dir>/evidence/`), else its head: `merge: your answer` when that commit's author may answer (the seat matched as the gate matches it, email or name) and the commit verifies, and every commit of its own below that one is his too, by the same test, a review file's only, or the tool's own refusal record — else `wait: a seat's commit on your answer branch (<sha>, <author>)`, or for a commit in his name that does not verify `wait: an unverified commit in your name on your answer branch (<sha>)`, the first such below his: a merge would carry it, and `--answer`, `--done` and `--due` cut the branch from the one he stands on; where the pull request's base is not fetched here, `wait: the base <base> is not fetched here — …`, never a merge it cannot see; `wait: not an answerer (<author>)` when the author may not answer, signed or not; for an author who may, `wait: answer not verified here — <why>` when it is signed and this clone cannot check it, else `wait: unsigned answer`. After the pull requests, each branch on `origin` that none carries — not the default branch, not `answer/*`, not a head a pull request ever had, not one already merged or inside an open pull request or another such branch — as `branch <name> @ <sha>  wait: no pull request — …`, read the same way: `no verdict on <sha>`, `verdict <sha> READY …: open it`, `NOT READY (<sha>)`, `conflict in <paths>`, `TRIAGE.md changed unsigned (<sha>)`. A head the clone's fetch does not cover is fetched by its ref; one that still is not here reads `not fetched here`, on its line alone. A last line counts them: *N waiting on you: a merge, b close, c wait, n pushed without a pull request*. Then *MERGED OR CLOSED IN THE LAST 24 HOURS*: each pull request the forge merged or closed in the last day, with its time — so a seat's *still open* is checked against the forge in the same turn. Without `gh`, offline, or with no GitHub `origin`, it says so in one line, exit 3 — a view fails nothing. `--owner` and `--standup` end with it where the forge can be read, and leave it out where not |
| what the records cost against the product | **`--ratio [--since YYYY-MM-DD] [--until YYYY-MM-DD]`** (FM-032, the Owner's concern of 2026-09-30) — read from git alone: per Europe/Berlin day of the merge, for the merge commits on the default branch's first-parent line (`origin/HEAD`'s target, else `origin/main`, `origin/master`, `main`, `master`), each against its first parent, the lines **added and deleted** in *records* (the `[ratio] records` prefixes) and in *product* (every other path) — counted apart, never netted; the ratio is records added : product added, or `no finite ratio` where no product was added; a submodule pointer is no line and a binary file 0 lines. Then a total for the window and the rolling seven-day sums, each day with the six before it. The window is the seven Berlin days ending today; `--since` and `--until` move it. A repository without `[ratio]` has no ratio: it says so, exit 2. The rule is filed on its own page, `work-tracker/evidence/FM-032/records-to-product-ratio.md`; this command is its reference |
| what the ask offers | `ask-options:` — the choices as ONE line, `a \| b \| c`; `ask-proposal:` is the one the seat **recommends** — offered first and marked, and where options are named it must be one of them. A proposal alone is a list of one |
| an act owed to the Owner | `due:` — when it falls due, an ISO time with its zone (`2026-09-26T07:30:00+02:00`); `window:` — the minutes after it in which it can still be done (60 where absent); `done:` — its result, `<time> · <where it is>`. The seat that schedules the act writes `due:`, with the action ask or when its time is set; `--answer` writes it with an accepted action answer whose promise names a date with its hour — `2026-09-26 09:00`, `2026-09-26T09:00+02:00`, or the weekday with its month and day, `Sat 09-26 09:00 CEST`, the weekday checked — in the zone it names, else the machine's own, and says so; a weekday alone, a month and day with neither year nor weekday, a zone name the machine does not carry, a word after the time that is no zone as written (`cest`), a 12-hour time (`9:00 PM`), a fraction of a second (`09:00:00.000Z`), or two times are not read — nothing rather than a wrong hour — and a `due:` already set is left (FM-030, the E0 counter's row 20); `--clear-ask` leaves it, because the answer to an action ask is a promise and the act is still owed. The gate refuses a time that is not one, or has no zone. An act is owed where an action ask was accepted or a `due:` is set, until `done:` is written: the Owner's board lists it after the questions, under *your acts, with their time* — *no date yet*, *due*, *overdue* after its time, *missed* once its window has passed with no result, by the page's clock — and INDEX.md lists it with its time as written, which no minute changes. An act that is a promise reads as what he promised — the text his accepted answer carries, the option he took or his change, else the proposal a bare `accepted` took — with the question it answered below it, smaller, as context: on the board and in its two dialogs, in `--owner` and `--standup`, in `--notify`'s notice and the invite (FM-030, his word of 2026-09-27 13:38:30); a `due:` beside a question he has not answered keeps its own line. Each act on the board has two buttons, **done** and **reschedule**: one asks where the result is, the other the new time, and OK gives one command on the answer's second screen — **`--done <id> "<where the result is>"`** writes `done:` (the time, and where) — the person gives the path; the record gathers the facts: for a file in the repository (from its root, or from the tracker directory; a line anchor after it, `file.md:12` or `#L1-L9`, kept as given), the commit that added it and its date, and for a review — a file that states a verdict, `Verdict: READY` or a bold `**NOT READY**` opening its line — the verdict of its last pass: the last line that states one, that pass's `Reviewed:` sha and `Session:` from its own lines, else the trailers of the newest commit that touched the file, with *last pass in* that commit where it is not the one that added it; a word that names no file there is recorded as given with *not in the repository* beside it, words as given, nothing guessed, nothing refused; a later `--due` on the done act keeps it in its record —, sets `next: build` where the answer left `next: owner`, and records the act under `## Acts`; **`--due <id> <time>`** writes the new `due:` and records the old one there. Both are made as `--answer` makes his answer — on `answer/<id>`, signed where his seat is `signed`, pushed — and refused from a seat without the `answer` right. Refused on `answer/<id>`, after its cut — the commit refused, the file not written — `--done`, `--due` and `--answer` undo their change and leave one line under `## Acts` there, `**<date> <time>** · <the command> refused — <why>`, committed unsigned — it changes no key and records no act, so no right is read in it — and pushed; the next run on that tracker names the branch. Refused before the cut — a tree with changes, no signing key — they print only (FM-030, the E0 counter's row 20) |
| an act's invite and its notification | **`--invite <id>`** writes `<tracker dir>/evidence/<id>/<id>-act.ics` — RFC 5545: the act's `due:` in UTC, a DURATION of its `window:`, a reminder 30 minutes before — and prints its path; after a `--due`, write it again: its SEQUENCE counts the act's records, so importing it replaces the event. **`--notify`** posts one system notification for each act that falls due within 30 minutes, is overdue or was missed — macOS `osascript`, Linux `notify-send`, Windows PowerShell's toast, else it prints — and says what it posted. Once per act per state: it remembers what it posted in `$XDG_STATE_HOME/shoalmark/notified.json` (else `~/.local/state/shoalmark/`, on Windows `%LOCALAPPDATA%\shoalmark\`), never in the repository; a new `due:` posts again. The tool installs no schedule — §*An act's reminder* |
| his act or answer on its way | **The board reads git** (FM-030, his signed answer `920970b7`, 2026-09-27 14:56:15). `--answer`, `--done` and `--due` commit on `answer/<id>` and push, and the default branch knows nothing of it until his merge. The board, `--owner` and `--standup` read every `origin/answer/<id>` this clone holds that is not merged into `origin`'s default branch — the tool's own push leaves that ref, a fetch brings another machine's; nothing is fetched to read it and nothing is written to remember it — and where its tip carries a `done:`, an `answer:` or a `due:` the default branch lacks, the ask leaves *waiting for you*, the act leaves *your acts*, and both are listed under *on their way: n*: his promise or his answer first, then *answered, on its way*, *done, on its way — <where>* or *rescheduled, on its way — due <time>* (`--due` is his act as `--done` and `--answer` are, and a `--due` after a done act opens a new one — never *done revoked*), *revoked, on its way — <why>* and *done revoked, on its way* only where `--revoke` made the change, the branch, the commit that wrote it — read from the branch's commits, so a Reviewer's verdict on top is no act — its time, whether it verifies (`--queue`'s own reading of an answer commit), and *your merge is next* — or, where `--queue` waits on the branch for more than that commit's own signature (a seat's commit below his act, a head past it, a base not fetched here), *your merge waits: <that wait>*, the queue's own line. A merged branch, or one whose tip carries no such change, changes none of the board's rows and nothing of the rendered board. Right after the act the page shows it: put back on the branch he started on, the checkout hook `--install-hook` writes has rebuilt the board; where the board's file did not change between the push and the switch back — no such hook — the command rebuilds it itself (`--html-only`), and says which. An answer or an act done on its way has one button, **revoke** (a reschedule has none — `--due` again, on its branch): **`--revoke <id> "<why>"`** takes back what he last did, as a new signed commit, never an overwrite — on an act done, `done:` leaves the front matter, the revocation is recorded under `## Acts` and the act is owed again; else his answer, as `--answer <id> revoke` takes it. Where `answer/<id>` is not merged, it commits on top of it there — one branch per exchange; merged, it is cut fresh and the revocation is on its way in its turn. The seats that hold `answer` may run it |
| the Owner's answer | on the board: **accept** or **reject** opens a dialog with the question, the choices and what it holds up — one radio per option, the recommended one first, and *Other:* with a box. OK opens a second screen: the one command, where to run it (the branch the board was built from), what it does, what success looks like, how to check the signature, the signing page for when it fails — and **Done**. **`--answer <id> accept\|reject ["text"]`** cuts `answer/<id>` from the ask's branch, writes the three lines and the next move — `next: build` after a ruling, a determination or a ceremony, the seat's move; `next: owner` kept for an action, whose act is still his — commits signed, pushes — naming each step on stderr as it starts — and goes back to the branch it started on. An `answer/<id>` left from an earlier answer is deleted and cut fresh when it is merged into `origin`'s default branch, and refused when it is not — naming his commits on it, and `git branch -D answer/<id>` only where nothing of his is there: nothing unmerged is deleted for him. An answer is never overwritten in place: **`--answer <id> revoke "<reason>"`** takes it back (`revoked - <reason>`), and **`--answer <id> accept\|reject "<option>" --supersede`** replaces it; either moves the answer it replaces into the ship log — `\| <date> \| Answer of <answered> superseded: *"<answer>"* (<sha>) — revoked: <reason> \|`, or `— replaced by: *"<answer>"*` — and the board shows the answer with *supersedes <sha>*. **The word he signs is the button's** — under `accepted` the dialog and `--answer` write the proposal, another option and changed text alike — **and every reading names its relation to the proposal beside it**, computed from `answer:` against `ask-proposal:` and `ask-options:` with the answer's own normalisation on both sides (trimmed, whitespace runs one space, `"` as `'`): *accepted the proposal* · *chose option N: <its first words>* (N its place in `ask-options:`) · *accepted with a change* · *rejected: <reason>* · *revoked: <reason>* · *relation not computable* where there is no proposal to compare it with. The board's tracker view, `--answered` and the record `--clear-ask` writes print it; the signed line is never rewritten, and a hand-written `accepted — <text>` reads as `accepted - <text>`. A failure after it has written anything undoes all of it — the paths restored, back on the starting branch, an empty `answer/<id>` deleted — and prints what refused it, the answer, and the command that gives it again; on `answer/<id>` the refusal is recorded there under `## Acts`, as an act command's is. `--answered` is what he answered and no seat has acted on |
| acting on an answer | `--clear-ask <id> <next move>` — moves the exchange into the body under `## Asks` (date · question · answer · answered-by, a `**relation** —` line with the answer's relation to the proposal, which leaves the front matter with the ask, and a `**signed** — <sha> · <G\|N\|U>` line naming the commit that wrote the answer and what git says of its signature, `%G?`; newest last), clears the ask and answer lines, sets the move. Under `[seats]` that is the **`ask`** right's move — the principal's, not the owner's. The gate refuses a commit that drops an answer without that record, and `--answered` reports what was acted on since the last standup, by commit, with the relation its record carries. A record written before 0.18.1 has no `**relation** —` line: `--answered` and the board's tracker view — under each such record, not only the newest — read its relation from the commit that wrote its answer — the one commit that adds that `answer:` line under the record's question (its `ask:` at that revision), its `ask-proposal:` and `ask-options:` there — and name that commit; where no commit in the checkout holds both, or more than one does, *relation not computable*, never a guess |
| who may answer | the seats that hold `answer` in `[seats]` (§*Seats*) — `owner = "you@example.org signed"`. Without `[seats]`, the old key: `answerers = ["name"]` or `["name signed"]`, git author names. The gate reads the answer's committer from git or Subversion; under `signed` the commit must verify and the key's identity must be the author's email. Empty = nobody may answer. With `[seats]`, `answerers` is not read for answers — and a `signed` entry beside an unsigned seat that answers for it is refused, not dropped. Setup for a human: the signing page, `docs/signing.md` |
| `<tracker dir>/<ID>-<slug>.md` | the trackers — one flat directory, the id in the filename |
| `<tracker dir>/TRIAGE.md` | the Owner's intent and current path; one paragraph per pass |
| `<tracker dir>/sessions.md` | gone since 0.18.0 — the registry of seat sessions is a report, `--sessions` (§*Sessions*); delete a file left from before, history keeps its rows |
| `<tracker dir>/INDEX.md` | generated, committed — what an agent reads |
| `<tracker dir>/index.html`, `view/` | generated, git-ignored — the read-only board the Owner reads |
| `<tracker dir>/evidence/` | worksheets and pass records — append-only, never on a reader's path |
| `<tracker dir>/derive` | optional, executable — the repository's own axis (§7) |
| `<tracker dir>/brand/` | optional — the repository's `theme.css`, `logo.svg`, `wordmark.svg`, `labels.yaml`, fonts (§9) |

### An act's reminder

`--notify` is meant to run every few minutes, on the Owner's own machine; nothing installs it. It exits 1 when a notice
could not be posted, so keep what it says in a log. With cron on Linux — cron gives `notify-send` no session bus, so the
line names it; and the shell opens the log before the tool runs, so the line makes the log's folder first:

```
*/5 * * * * mkdir -p "$HOME/.local/state/shoalmark" && cd /path/to/repo && DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/$(id -u)/bus python3 shoalmark.py --notify >> "$HOME/.local/state/shoalmark/notify.log" 2>&1
```

With launchd on macOS, `~/Library/LaunchAgents/app.shoalmark.notify.plist`, then `launchctl load` it:

```xml
<plist version="1.0"><dict>
  <key>Label</key><string>app.shoalmark.notify</string>
  <key>WorkingDirectory</key><string>/path/to/repo</string>
  <key>ProgramArguments</key><array><string>/usr/bin/python3</string><string>shoalmark.py</string><string>--notify</string></array>
  <key>StartInterval</key><integer>300</integer>
  <key>StandardOutPath</key><string>/Users/you/Library/Logs/shoalmark-notify.log</string>
  <key>StandardErrorPath</key><string>/Users/you/Library/Logs/shoalmark-notify.log</string>
</dict></plist>
```

### Seats

Who is at the keyboard, and what that seat may change. **Four rights**, each a front-matter transition the gate sees in
a diff: `answer` (the three answer lines) · `ask` (`next: owner`, and clearing an answered ask with its record) · `close` (a terminal status) · `triage`
(`considered:`, `kind-of-problem:`, tier, rank); anything else is open to every seat. Four names carry theirs built in —
**owner** all four · **principal** ask, close, triage · **reviewer** triage · **implementer** none — any other name says
so in `[rights]`, in the same diff as anything it would allow. Absent `[seats]`, nothing of this is enforced. A **merge**
is judged by what it changes itself — the files where it differs from every parent — under the merger, and every commit
it brings against its own parent, under that commit's own author and signature: a clean merge adds nothing, and never
launders a commit that was made without the hook.

```toml
[seats]                                 # a name you choose -> the identity version control reports
principal   = "principal@seat signed"   # `signed`: the commit must verify under a key trusted for that identity
implementer = "implementer@seat"
[rights]
chef = ["answer", "close"]              # only for a name that is not one of the four
```

**The badge:** `git config extensions.worktreeConfig true` once, then `git config --worktree user.email principal@seat`
in each seat's worktree. A signed seat's key belongs where only that seat runs — a container, later; the Owner's key is
never in a seat's environment. This catches an agent that does not know the rule, **not one that lies**: that is
FM-007's class, and nothing moves work except the Owner's signed answer. **On Subversion** the identity is the server
account and `signed` is refused — the server authenticated the commit, and the gate reads the author it recorded
(`svn blame --xml`, as the answer gate does). One seat = one SVN account whose credentials exist only in that seat's
environment (a container, or its own Windows user), never the Owner's cached ones (`~/.subversion/auth`, the Windows
credential store); the svn command line runs no hook, so the server's own `pre-commit` hook running `<cmd> --check` is
the layer that refuses and the board's *sent back* group is the backstop. A seat's **charter** — how it thinks, a bold
Principal against a steady one — is `<tracker dir>/seats/<name>.md`, read by the agent at start, never by the gate.

### Sessions

The seat says **who may**; it cannot say **which run**: two sessions of one seat are one author in git. So a seat's
worktree carries a second setting beside its badge, and every commit made there names its session.

```bash
git config --worktree user.email principal@seat      # the seat — read by the gate for rights
git config --worktree seat.session a9f3c2d1          # the session — the harness's session id, its first eight hex characters;
                                                     # a sub-agent derives its id from its parent's: a9f3c2d1/reviewer-1;
                                                     # a session with no parent and a harness with no id: `<cmd> --session new`
```

**The trailers:** `--install-hook` writes a `prepare-commit-msg` hook that appends `Session: <seat.session>` and
`Worktree: <the checkout's directory>` to every commit made in that worktree — never typed, and a trailer the message
carries already is left alone. A repository with no `seat.session` (the Owner's checkout) gets nothing appended: his
signature is his id. Read them back with `git log --format='%h %ae %(trailers:key=Session,valueonly)'`. A repository
with its own hook runner adds three entries — with lefthook, the session rule on every commit, the trailers, and the
judgement of the commit with its message:

```yaml
pre-commit:
  commands:
    session:                     # the session rule on EVERY commit, a tracker staged or not
      run: python3 tools/shoalmark/shoalmark.py --session-check
prepare-commit-msg:
  commands:
    session:
      run: python3 tools/shoalmark/shoalmark.py --session-trailer {1}
commit-msg:
  commands:
    judged:                      # where `judged_before_build` is on: the commit judged with its subject (FM-033)
      run: python3 tools/shoalmark/shoalmark.py --commit-msg {1}
```

**The commit hook is best-effort. The gate is `--check` on the branch, and it must be green on the pull request's head
before merge. A bypass of the hook alone, which `--check` catches, is P3.** Git's `--no-verify` skips any hook by
design; what protects the default branch is `--check` on the branch.

**The registry is a report:** `<cmd> --sessions` prints it from the trailers of the checkout's history — one row
per session id: its seat (the author through `[seats]`), its first and last commit, how many commits carry it, and its
worktree. Nothing is opened, closed or kept in a file, so two branches that land never conflict on it: a session is
what its commits say, and it ends at its last one. An id seen in two worktrees is named under the table.

```text
| Session | Seat | First commit | Last commit | Commits | Worktree |
|---|---|---|---|---|---|
| a9f3c2d1 | principal | 2026-09-24 07:28 · 049a9ab | 2026-09-24 11:02 · 5e1f0a2 | 9 | principal-a9 |
| a9f3c2d1/reviewer-1 | reviewer | 2026-09-24 09:40 · 7c2d8e1 | 2026-09-24 09:52 · 3a7d1e0 | 2 | reviewer-2 |
```

Until 0.18.0 the registry was `<tracker dir>/sessions.md`, written by `--session open` and `--session close` and read
by the gate. Both commands are gone — each says so and exits 2 — and `--check` warns in one line where the file is
left: delete it; history keeps its rows.

**The gate** holds one rule. A commit by a seat `[seats]` names — never the Owner's, never an author outside
`[seats]` — must carry a `Session:` of the shape `<8 hex>` or `<8 hex>/<seat>-<n>`, and where it names a seat, that is
the author's seat. Exit 4, and one of three lines:

```text
refused: this commit by principal@seat carries no Session: trailer — set `git config --worktree seat.session <id>` in its worktree: …
refused: this commit by principal@seat carries `Session: q7` — a session id is eight hex characters, or `<id>/<seat>-<n>` for a sub-agent
refused: this commit by principal@seat is the seat principal, and its Session: a9f3c2d1/reviewer-1 names the seat reviewer
```

The pre-commit hook `--install-hook` writes runs it on every commit — `--session-check`, the session rule alone, a
tracker staged or not. It judges what the rights are judged on: the commit being made (by its worktree's
`seat.session`, the trailer its hook will write), the commit at HEAD by its trailer, and every commit a merge brings,
each by its own. A repository adopts the rule with its first `Session:`: a commit whose history carries none is not
judged, so a repository that never set `seat.session` is not refused when it vendors.

**Verdicts:** a review commit names the tip it judged — the Reviewer types this trailer: `Reviewed: <sha>`. `--check`
reports each verdict of the last `triage_days` days. The reviewed range is the branch's own commits —
`git rev-list <tip> ^<trunk> --no-merges` (`origin/main`, else `main`, else `master`), less other verdicts; for a tip
the trunk has since merged, the trunk as it stood before that merge — so what the branch merged in from the trunk is
not its, and the report does not change when it lands. The verdict is **independent** when its session's root (`a9` of
`a9/reviewer-1`) is none of the range's sessions' roots, **same session** when it is one of them — a Reviewer run as a
sub-agent of the author's session is not independent — **untraced** when either side names no session, and **on
trunk — not a branch verdict** when the tip is on the trunk's own first-parent line. A count, not a refusal: the refusal is a later slice, after a week of counts. `--queue` reads a
verdict's word from its commit's subject — `READY`, `READY WITH FINDINGS`, `READY TO TAG` or `NOT READY`: a verdict
commit says one of them.

**Seen:** the board's first lines carry the strip — *sessions · 2 in the last day — a9f3c2d1 principal
(principal-a9) · a9f3c2d1/reviewer-1 reviewer (reviewer-2)* — and *reviews this week · independent n · same session
m*; `--owner`, the digest, carries one line, the sessions of the last day by seat, each with its worktree, and ends with
the queue where `gh` reads the forge (*what to merge*, above). Four labels, `sessions.recent`
and `reviews.*` (§9).

## 7. The one seam: a deriver

The core knows nothing about releases, deploys or product areas. A repository that needs them puts one executable
at **`<tracker dir>/derive`**. The core runs it first, on **every** run — so keep it fast — with this on stdin:

```json
{ "root": "/abs/path", "mode": "write", "flags": [], "trackers": [ { "id": "MSR-012", "status": "Shipped", "file": "MSR-012-x.md", "fm": { "version": "1.2.0" } } ] }
```

and reads this from stdout:

```json
{ "MSR-012": { "Ver": "1.2.0", "Release": ["1.2.0", "1.2.0 ✓"], "_needs": [] },
  "_keys":     { "version": { "shape": "\\d+\\.\\d+\\.\\d+", "says": "the release it shipped in", "who": "the ship commit" } },
  "_problems": [ "MSR-014: version on work that has not shipped" ],
  "_index":    [ "Ver" ],
  "_board":    [ "Release" ],
  "_notes":    [ "**Ver** = the release it shipped in." ],
  "_files":    { "docs/RELEASES.md": "…the whole file…" } }
```

- Each value key is a **column** in `INDEX.md` and on the board, and a **view**, a fact and a search word on the
  board. `_index` / `_board` narrow which goes where (default: all). A value may be `[value, display]`: the value
  groups, sorts and is printed in `INDEX.md`; the display form is for the board's cells.
- `_keys` join the schema gate — add a key, never redefine one. `_problems` fail the commit like the core's own.
  `_needs` (per tracker) are shown beside the core's own marks. `_notes` go into `INDEX.md`'s header.
- `_files` are written, drift-checked (`--check`) and staged (`--print-written`) **by the core**. A deriver has no
  side effects, and nothing derived is ever stored — so nothing derived can be stale.
- **A non-zero exit refuses the run before anything is written** — a crash included, and silence past 60 s. Say
  why on stderr.
- `mode` is `write` · `check` · `board` (only the git-ignored page is produced — a guard that protects committed
  output may stand down) · `read`. `flags` are what was typed as `--derive-flag NAME` on **this** run.
- **A deriver is told things on stdin and never reads the environment** — the core runs it with `PATH`, `HOME`,
  the locale and nothing else. A git hook inherits whatever the shell that ran `git commit` had exported; a deriver
  that listened to that would let a stray variable decide what gets staged.
- A wrapper script may set `SHOALMARK_CMD` so every message names the repository's own command.

## 9. Branding the board

Four optional files, the same names in every place — the board is built from the places in order, **the later one
wins**: `tools/shoalmark/brand/`, the organisation's that set the repository up (`--vendor` copies and pins it) ·
`<tracker dir>/brand/`, the repository's, never loose among the trackers · `~/.config/shoalmark/`, the person's, in
every repository. Only the git-ignored board reads them: `INDEX.md` and the gate are the same whoever runs them.

| File | Carries |
|---|---|
| `theme.css` | colours and fonts. Each place's file is its own stylesheet, so one variable changes one colour; `@import` and `@font-face` work, **with paths written relative to the `theme.css` they are in** — a font goes in `brand/fonts/`. A theme whose import is missing is left out whole |
| `logo.svg` / `logo.png` | the header and the browser tab; at most 200 kB; a script inside an SVG cannot run |
| `wordmark.svg` | the mark and the name drawn as one, **inline** in the header in place of the logo and the name — the logo stays the tab's, the name the page's title and the wordmark's accessible name. At most 200 kB of UTF-8; shapes, text, gradients, masks and a `<use>` of its own ids, each attribute from a fixed list with a fixed grammar — colours `#hex`, `currentColor`, `none` or a plain name, numbers as `-?digits(.digits)?` with one space or comma between, every id once, never `style`. Anything else refuses it whole, with a warning |
| `labels.yaml` | every word of the board — flat `key: value` lines, `tagline` and `footer` among them. A German board is this file |

- **`--brand`** says which place gave the board its theme, logo, wordmark and labels; `--brand DIR` writes a commented
  starter. The name is `name` in `shoalmark.toml`. A theme hard to read is a warning; status colours keep their meaning.
- **Two themes ship as starters** in the tool's `brand/themes/`, `monochrome` and `shoalmark`, each a `theme.css` with
  its fonts; `--vendor` copies and pins them, so a vendoring repository receives both. None is worn until
  `--brand DIR --from <theme>` copies it into a place: a board that chooses none looks as it did. A theme styles three
  hooks: the Owner's box's title `#p>.pt` (label `owner.title`), the last line `#F` (`#f`, `#r`), `tr.zebra`.
- **Light and dark:** dark colours go under `@media (prefers-color-scheme:dark)`; `◐` (auto → light → dark) switches
  that rule for any theme and remembers the choice in the browser; paper stays light. A wordmark in `currentColor`
  takes the page's ink, at its `height`, else 22 px. Every page ends in the tool's line: its mark, name and version.
- **Another language:** `labels.yaml` for the board's words; `[headings]` in `shoalmark.toml` for the gate's sections.

## 8. Working on shoalmark

```bash
python3 test_shoalmark.py && python3 test_core.py          # every check builds its own throwaway repository
/usr/bin/python3 test_shoalmark.py                         # the oldest Python promised: 3.9, the one macOS ships
```

Where Chrome or Chromium is installed the board is rendered and read back. `test_core.py` pins the core's
behaviour on a synthetic corpus; `test_shoalmark.py` pins what was built here. A change ships with its check, and
the check is shown to fail without the change. Every consumer-visible change gets a `CHANGELOG.md` entry —
`--vendor` prints it to the repository that upgrades. This repository tracks itself: `python3 shoalmark.py --next`.
How a change here is reviewed, what a miss costs, and how the Owner is spoken to are this repository's house rules — the
Owner's signed answers of 2026-09-24, in [`AGENTS.md`](https://github.com/shoalmark/shoalmark/blob/main/AGENTS.md).

## Licence

`Apache-2.0 OR MIT`, at your option — [LICENSE-APACHE](https://github.com/shoalmark/shoalmark/blob/main/LICENSE-APACHE), [LICENSE-MIT](https://github.com/shoalmark/shoalmark/blob/main/LICENSE-MIT), [NOTICE](https://github.com/shoalmark/shoalmark/blob/main/NOTICE).
The one bundled file, `vendor/marked-18.0.13.umd.js`, is MIT. All three ship in a vendored copy.

What it is not, on purpose: no sprint, no estimate, no assignee, no comment thread, no editing in the board.
A viewer, not a Jira.
