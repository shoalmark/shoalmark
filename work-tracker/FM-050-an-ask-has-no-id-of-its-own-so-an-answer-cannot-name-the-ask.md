---
id: FM-050
status: In Progress
considered: FM-027, FM-008, FM-014, FM-016, FM-029, FM-030, FM-023
tags: process
next: build
triaged: 2026-10-27
tier: P2
hook: "An ask has no id of its own, so an answer, the stand-up and the receipts cannot name the ask they mean"
---

# FM-050 — an ask has no id of its own, so an answer cannot name the ask it answers

## What is true now

**2026-10-27 — adopted by the Owner, and judged In Progress, P2, critical, for v0.20.2.** The Owner's signed answer adopts the ask-id design and R4's answer commit; it is recorded under `## Asks`. It is batch 3's S1, and it builds on FM-076 in the v0.20.2 lane, since both change the gate's answer and rights paths.

**2026-10-27 — its ruling ask filed again, on today's main.** The design and its two review rounds come onto main from
`fm/050-ask-id-design`, unchanged. The records pass of 21 October that carried them was never pushed. What changed since
16 October:
- v0.20.1 shipped without ask ids and without R4's answer commit. In v0.20.1 an answer is the Owner's own commit, made
  in their terminal and signed only where the default branch asks for it (FM-054). The ask ids move to v0.20.2 with
  batch 3, on the Owner's word of 22 October, which FM-023's ask of 27 October puts to them for a signed answer.
- Since v0.20.1 the board's look and words follow `brand/design-guide.md` (FM-053), so §5's lines are read against the
  guide when they are built.
- The design's references into `shoalmark.py` (`:942` and the rest) name the tool's lines as they stood on 16 October.
  The build reads them again.

The ask stands as filed, at this commit. Its "no" now names a release after v0.20.2, the release it is proposed for.

**Filed 2026-10-15 as a design tracker. Designed 2026-10-15 (`## The design`, below); reviewed 2026-10-16 in two rounds,
not ready (`cc9e80b`) and then READY (`ed2c82b`); put to the Owner; not ruled; nothing built.**

- **Today:** a tracker holds at most one open ask, in its front matter. `--clear-ask` moves an answered exchange under
  `## Asks`, dated, with no id. An answer is tied to its ask only by its tracker and the ask's date.
- **Why now:** R4 makes an ordinary Owner-signed commit the canonical answer (FM-023's table of 2026-10-15: v0.20.1). That commit
  must name the ask it answers, so the id comes first. The receipts view counts asks too: the oldest waiting ask, the
  answers per sitting.
- **A case, 16 October:** the board hid FM-053's re-filed ask. The first answer's `answer/fm-053` was still on its way,
  and *on its way* is keyed on the tracker id, so the new ask did not show. The Owner read it from the tracker and
  answered by hand (`fee3874`). Ask ids fix it: an answer on its way is named by its ask's id, never by its tracker.
- **The Owner's word, 16 October:** *on their way* (FM-030; `on_their_way` and `WAY_TITLE` in `shoalmark.py`) is in the
  board's code, but in neither §1 nor §7 of `brand/design-guide.md` (found in A2's build check, recorded privately). It
  goes into FM-050: FM-050's design round places it in the guide, beside the case above. The ask filed at `03ef687`
  stands as filed.
- **The design** is below: the id, asks before ids, R4's answer commit and how the gate finds it, what the gate refuses,
  what the three readers print, the class test, what each backend can claim, and the build's order. Its open questions
  close it.
- **The ask** is put to the Owner (`next: owner`) by the Planner after round 2's READY, and filed at the commit that puts
  it, so the answer binds the reviewed body.
- **Tier: critical.** It decides which ask the Owner's verified word answers, so it is signing and rights. A critical
  Builder, a Reviewer in a session of its own, one CI run.
- **Order:** designed and reviewed, and ruled by the Owner, before R4 is built; R4 and the ids are built together.
- **Source:** an analysis of ask ids, recorded privately; the quick-wins design of 15 October, recorded privately.

## The design

Every line number is `shoalmark.py` at `5f792d6` (main). *The walk* is the gate's reading of a branch's changes, commit
by commit, a merge's own change against every parent (`read_changes`, `:6218`). *The default branch* is `origin`'s,
as `default_trunk` reads it (`:3261`).

### 1. The id

- **Form:** `<ITEM>-Q<n>`, as in `FM-050-Q2`. `<ITEM>` is the tracker's own id. `n` counts that tracker's asks put
  with an id, from 1, with no leading zero.
- **Never reused.** A withdrawn or replaced ask keeps its number in its record. The next ask takes one more than the
  highest number the tracker has used: in its front matter, in its records, and on git in the file's history.
- **Minted when the ask is put to the Owner** (`next: owner`), by the seat that puts it. A draft (`next: review`) has
  none: the Owner never sees a draft.
- **One put ask per id.** An answer binds the whole put ask: its question, its proposal, its options and its kind
  (`ask:`, `ask-proposal:`, `ask-options:`, `ask-kind:`). Each of them bears on the decision: a bare `accepted` takes
  the proposal, and a choice is read against the options. None of them changes under its id (C2, item 4).
- **To change a put ask, the seat withdraws it and puts the changed ask under the next number.** `--clear-ask` writes
  the old id's record: `**withdrawn**`, or `**answered**` with the answer where one was given. The answer stays in the
  record of the id it was given to. It never moves to the changed ask, which waits unanswered under its own id.
- **The put ask is one reader,** `put_ask(t)`: those four lines, each through `answer_norm` (`:1723`), and the options
  as their list. C2 and the binding (3b) both compare through it, so one comparison decides both.
- **`ask-since:` is outside the put ask.** It says how long the ask has waited and decides nothing, so C2 and the
  binding do not read it, and a change to it changes no put ask. A changed ask put under the next number keeps the
  `ask-since:` of the ask it replaces: the age the Owner sees is how long they have been asked for this decision, and a
  change the seat makes must not make that wait look shorter (FM-029's lesson: a measure must not flatter the seat). A
  new question that replaces no ask writes the day it is put.
- **Where it is written:**
  - the open ask's front matter, `ask-id:`, on the line above `ask:`;
  - the cleared exchange under `## Asks`, in place of the date's bold:
    `**FM-050-Q2** · <date> · <question>`, then `**answered** —`, `**relation** —` and `**signed** —` as today, or
    `**withdrawn** — no answer was given` (the two records `clear_ask` writes today, `:8362–8364`).
- **The ask's lines** (`ASK_LINES` and its relatives):
  - `ASK_LINES` (`:8304`) gains `ask-id:`, so `--clear-ask` strips it with the rest (`:8356`);
  - `front_matter_schema` (`:978`) gains `ask-id` beside the ask keys (`:989–994`): its shape, who writes it, and what each
    backend can claim (item 7);
  - `GUARDED_KEYS` (`:790`) gains `ask-id`: the gate judges on it, so it is read from one line, in lower case
    (`guarded_key_problems`, `:5508`);
  - `extract` (`:1404`; the ask keys at `:1497`) reads `ask_id`, and the ids of the records under `## Asks` beside
    `asks_relation` (`:1521`);
  - `answer_cmd`'s write skips every `ask-` line after `ask:` already (`:2793–2794`), so the answer lands where it does
    today;
  - `record_key` (`:1817`) learns the record's id form; a record with an id always carries its `**relation** —` line or
    is withdrawn, so `recover_relations` (`:1833`) is never asked about one.
- **The next number** is one reader, `ask_numbers(t)`: the front matter's id, the records' ids, and on git
  `git log --full-history -G '^ask-id:' -p HEAD -- <file>`. A line added or removed there both mean the number was
  used. No commit is credited with anything, so FM-056's defect does not touch this read. No new command: the gate's
  refusal (item 4, C1 and C4) and `--clear-ask`'s last line name the next id.

### 2. Asks already cleared, and asks open before ids

- **Read as *asked before ask ids*.** Their records keep `**<date>** · <question>`. No id is added, and no commit
  is rewritten.
- **They answer as today (R26).** Their relation and signed lines read as today: `recorded_relation` (`:1799`),
  `recover_relations` (`:1833`) and `record_relation` (`:1906`).
- **An ask open without an id when the build lands** is read the same way. At `b84b8af` these are:
  - answered, not yet cleared: FM-004, FM-006, FM-026, FM-044 and FM-049;
  - waiting: FM-023, FM-037 and FM-055.
- **This tracker's own ask** is a draft (`next: review`), not yet put: at `b84b8af`, FM-050 had `next: wait` and no
  ask. Put to the Owner before the build, it is an ask before ids, read as those above are.
- **How such an ask is answered and checked:**
  - `--answer <ITEM>` answers it by tracker id;
  - the gate verifies the answer as today (`lint`, `:8693–8738`, through `line_author`);
  - its record carries no id.
- **The id is asked only of a new put** (C1, item 4). An ask before ids that is taken back to `review` and put again
  is a new put, and takes `Q1`.
- **Ids start at `Q1` on every tracker,** whatever records it holds. Numbering old records by their position would give
  signed records ids they never carried, and a position is not a record.
- **The old check keeps its defect.** It rests on `line_author`, and carries FM-056's defect until FM-056 is fixed.
  This design does not widen it, and the path with ids does not use it.

### 3. R4's answer commit

**3a. What it contains.** An ordinary commit: one parent. A merge never answers.

- **In the tracker of each ask it answers,** it sets these front-matter lines and no others:
  - `answer:`, `answered:` and `answered-by:`;
  - `next:` (`ANSWER_MOVE`, `:942`): `build`, or `owner` kept for an action;
  - `due:`, only where an accepted action names its hour and none is set (the seed, `:2771`);
  - a revocation or a replacement replaces the three lines and adds the ship-log row, as today (`:2789–2805`).
- **It leaves the ask as its parent has it:** `ask-id:`, `ask:` and the other `ask-` lines. The put ask it answers, its
  question, proposal, options and kind, is the one at its parent.
- **Its message:** the subject `<ask-id>: <the answer, cut between two words>`, and one trailer per ask it answers,
  `Answers: <ask-id>`. A hand-made commit of the Owner's may answer several asks, with one trailer each. `--answer` makes
  one per ask.
- **Its author and signature:**
  - the author is an identity the default branch's configuration lets answer (`owners_at(<default branch>)`, `:7775`):
    the `owner` line, and any name its `[rights]` gives `answer`;
  - it is signed with SSH where that identity is `signed`;
  - it verifies against the default branch's signers file (`verified_as`, `:5736`; `trusted_signers`, `:5752`). A
    branch's own configuration or signers file never vouches for it.

```
--- the tracker, after ---               --- the commit message ---
ask-id: FM-050-Q2       (as before)      FM-050-Q2: accepted
ask: "…?"               (as before)
ask-kind: ruling        (as before)      Answers: FM-050-Q2
ask-since: …            (as before)
ask-options: "…"        (as before)
ask-proposal: "yes"     (as before)
answer: "accepted"      (set)
answered: <date>        (set)
answered-by: <name>     (set)
next: build             (set)
```

**3b. How the gate finds and verifies it — by the id, never by the line.** `line_author` (`:5537`) names a setter with
`git log -1 --full-history -G <the line>` (`:5605`). A merge carries no diff there, and the pickaxe can name a commit
that removed the line (FM-056). The design does not rely on it. It needs the id in the commit, and the commit's own change:

- **One reader, `answer_commit(t)`,** for every tracker whose `answer:` sits beside an `ask-id:`:
  - one `git log HEAD` for all such ids at once, with a `--grep` prefilter, printing each commit's hash, its parents
    and `%(trailers:key=Answers,valueonly)`;
  - no path limit, so no history simplification skips a side branch.
- **The candidates** it keeps, for an id:
  - ordinary commits: one parent;
  - a trailer value equal to the id, read by git's own trailer parser. A prefix such as `FM-050-Q21` never matches
    `FM-050-Q2`;
  - verified as an answerer: the author per `owners_at(<default branch>)`, and the signature per `verified_as` where
    the identity is `signed`. This is the reading `guard_verdicts` (`:7805`) gives the triage guard. A commit that
    carries the trailer and does not verify is not a candidate;
  - its own change writes that tracker's `answer:` line: the tracker at the commit and at its parent, one `cat_blobs`
    for all candidates, carry different `answer:` lines;
  - its own change leaves the put ask as its parent has it: `ask-id:` and `put_ask` are equal at the commit and at its
    parent. The put ask the Owner answered is the one at the parent, and the commit carries that same one.
- **The head:** the candidates no other candidate descends from (`git merge-base --independent`, asked only where an
  id has more than one candidate). There must be exactly one.
- **What the head must hold:**
  - the tracker at the head carries `ask-id:` equal to the id, and the `answer:` line the file carries now, byte for
    byte;
  - the put ask at the head, which equals its parent's, equals the file's (`put_ask` on both sides, item 1: the
    question, the proposal, the options and the kind). The parent, the head and the file hold one put ask;
  - `answered-by:` equals the head's author name, as the gate asks today (`:8722`).
- **What a merge can do:** nothing. It is never a candidate. Its resolution can only change the file, and the file must
  still match the one head. The reading holds across merges without FM-056's fix.
- **Where the reader runs:**
  - `lint`'s answer gate (`:8693–8738`), in place of `line_author` for an answer beside an id;
  - `signed_line` (`:8372`), which names the head in the record `--clear-ask` writes;
  - `answer_cmd`'s `replaced` (`:2780–2782`), which names it in the ship-log row of a revocation or a replacement.
- **On the branch, change by change** (the walk, beside `rights_problems`, `:6333`): an `answer` change (`transitions`,
  `:6179`) on a tracker with an `ask-id:` is refused unless its commit is ordinary, carries `Answers:` naming that id,
  and changes no line of that tracker's put ask.
- **After the answer, the put ask is fixed with it.** A later change to its proposal, its options or its kind, by any
  author, is refused twice: by C2 on the change, and by the binding, because the head no longer holds the put ask the
  file shows. The signed acceptance is never read as accepting a changed ask: a changed ask is withdrawn, the answer
  stays in its record, and the changed ask is put again under the next number.
- **In the pre-commit run** the commit does not exist yet. It is judged on the commit, by the next run, as today
  (`:8712`). `--answer` runs the reader on its own commit before it says it is done.
- **Squash and rebase merges** rewrite the commit and lose the Owner's signature. The gate refuses that answer, as it
  does today. An answer lands by a merge or a fast-forward.
- **Cost per run:** one `git log` for every standing answer with an id, one `cat_blobs`, one read of the signatures
  (as `guard_verdicts` makes it), and `merge-base` only where an id has two candidates.
- **Where no default branch is known,** `owners_at(None)` reads the checkout's configuration (`:7783`) and
  `trusted_signers` the clone's file, as they do today, and `walk_problems` says so in `--check`.

**3c. The commands and the board's dialog.** Nothing cuts `answer/<id>`, pushes or switches branch any more.

- **`--answer <ask-id> accept|reject|revoke ["text"] [--supersede]`:**
  - an ask before ids is answered by `<ITEM>`, as today;
  - it writes the lines in the tracker on the branch the Owner stands on, and refuses a tree with changes, as today
    (`dirty_refusal`, `:3382`);
  - it commits, signed, with the trailer;
  - it checks the signature (`verified_as`, as `:3194` does) and the binding (3b);
  - it rebuilds the board with `--html-only`, except where git tracks the board (`board_after_act`'s own branch,
    `:3225`). This is R11's explicit refresh;
  - it prints: `FM-050-Q2 answered: accepted` · `signed, committed on <branch> as <sha>` · `it counts once this commit is
    on origin/main: push it, or merge the branch that carries it`.
- **An answer given on a seat's branch** (a board built from it) is on that branch, and counts once that branch lands
  on the default branch, with its own verdict.
- **A refusal:** before the commit, nothing is written; after writing, the file is restored (FM-017; `undo`, `:3092`,
  with no branch to delete). It records nothing under `## Acts`.
- **`owner_change`** (`:3036`) keeps who may answer (`:3051`), the tree check (`:3067`), the signing key (`:3071`), the
  author check (`:3077`), the write, the commit and its verification (`:3187–3200`). It loses:
  - the switch onto an unmerged branch (`:3149–3157`);
  - the cut (`:3158–3175`);
  - the push and the switch back (`:3201–3209`);
  - `record_refusal` (`:3116–3147`);
  - `unmerged_advice` (`:2831`), which goes whole.
- **`--done <ITEM> "<where>"` and `--due <ITEM> <time>`:** the same commit, on the branch the Owner stands on. The front
  matter and the `## Acts` record stay as today (`done_cmd`, `:8490`; `due_cmd`, `:8534`). `done_cmd`'s check for an act
  on an unmerged `answer/<id>` goes (`:8499–8508`). An act is the tracker's, and carries no ask id.
- **`--revoke <ask-id|ITEM> "<why>"`:**
  - an answer is revoked by its id, as `--answer <ask-id> revoke` does;
  - a done act is revoked by its tracker;
  - `revoke_cmd`'s reading of an unmerged branch goes (`:8587–8593`).
- **`--clear-ask <ask-id|ITEM> <move>`:** an ask id must be the one the tracker holds; the record carries it.
- **The board's dialog:**
  - its first screen reads `accept · FM-050-Q2` (`act`, `:3706`);
  - the second reads `sign your answer · FM-050-Q2` (`sign`, `:3732`), with the command
    `--answer FM-050-Q2 accept '…'`;
  - *where:* the branch the board was built from;
  - *what it does:* writes the three lines and `next:`; commits them, signed, naming `FM-050-Q2`; it counts once that
    commit is on the default branch;
  - `sign` loses its `answer/<id>` and its two steps `answer.sign.step.cut` and `answer.sign.step.push` (`:3928–3930`).
    The acts' dialogs (`owe`, `:3750`) change the same way.
- **What reads answer branches goes:**
  - `answer_refs` (`:1957`) and `on_their_way` (`:1971`);
  - `WAY_TITLE`, `REVOKE_DONE_SUBJECT`, `way_lines` and `owed_now` (`:2059–2085`), and their calls in `owner_digest`
    (`:2090`) and `standup` (`:2147`);
  - in `render_html`, the 32nd cell (`:4649–4651`, `:4665`); in the page, the revoke dialog (`rev`, `:3765`) and the
    rows on their way (`:3789`); the `way.*` labels;
  - `board_basis`'s read of answer refs (`:4571`);
  - in `--queue`:
    - the `answer/*` reading (`queue_actions`, `:2642–2643`), with `answer_branch_reading` (`:2463`), `answer_reading`
      (`:2491`), `stray_below` and `STRAY_WAITS` (`:2431–2460`), `answerer_of` and `answers_as_him` (`:2284–2296`),
      and `refusal_record` (`:2331–2430`);
    - `pushed_branches`' exception for `answer/*` (`:2263`).
- **In the queue's place:** a pull request whose own commits are all the Owner's verified commits (`verified_owner`,
  `:5671`), and change only the tracker directory, reads `merge: yours — signed`, with no verdict. This is the current
  path's line 2: a review of the Owner's own answers reports and never blocks.

**3d. Answers and acts already on answer branches stay valid; their history is kept exactly.**

- **Every answer branch this clone holds is merged:** `origin/answer/fm-004`, `fm-006`, `fm-007`, `fm-026`, `fm-044`
  and `fm-049`. `git for-each-ref --no-merged=refs/remotes/origin/main refs/remotes/origin/answer/`, read in this
  worktree, printed none.
- **Their commits are in main's history as the Owner signed them.** Nothing is rebased, re-signed or rewritten. Their
  answers are asks before ids, and are verified as today. The records' `**signed** — <sha> · G` lines keep naming them.
- **The `## Acts` lines stay as written,** the unsigned refusal lines among them. `--done`, `--due` and `--revoke` keep
  their front-matter writes, so `act_of` (`:5230`) reads every act as before.
- **The merged refs** may be deleted on the forge after the build: deleting a merged ref deletes no commit. That is not
  this design's to do.
- **An unmerged answer branch in another repository at its upgrade:** the upgrade note says to merge it first, on the
  old version. Afterwards it is an ordinary branch of the Owner's. The walk judges its signed commit as theirs
  (`rights_problems`), and `--queue` reads it `merge: yours — signed`.

### 4. What the gate refuses

**Every backend reads these rules from the file** (`ask_problems`, `:1620`, which `lint`, the Owner's queue
(`owner_queue`, `:1671`) and the board share):
- **F1:** the value is `<this tracker's id>-Q<n>`, `n` from 1 with no leading zero; the key stands on one line, spelled
  in lower case. Refused: `FM-002-Q1` in FM-001, `FM-001-Q0`, `FM-001-Q01`, `Ask-Id:`, and two `ask-id:` lines.
- **F2:** an `ask-id:` without an `ask:`.
- **F3, a reused number in one copy:** the front matter's id is also a record's id; or two records carry one id.
- **Duplicate archived ids** are two records under `## Asks` that carry one id. Defined apart from the answer, which
  plays no part here: a record carries no standing answer.
  - **Refused wherever they can still be stopped:** on a branch, where the default branch's copy does not hold both
    records, by F3 and, before the merge, by C5.
  - **Kept where both have landed on the default branch:** only a merge made against C5 and `--queue`'s wait, or a
    commit made past the hook, can bring them there. Each record names its answer's commit by its sha (`**signed** —`),
    so neither is rewritten once it has landed. `--check` notes them, naming both records with their dates and the merge
    that brought the second; every reader names such a record by its id and its date (`FM-050-Q2 of <date>`); and the
    next number is above both.

**On git, the walk reads these rules from each change; on Subversion, from the uncommitted change.** They are judged
for every author, the Owner included: a reused number is not a right. `changes_under_review` (`:6208`) feeds them, beside
`rights_problems`:
- **C1, a put without an id:** a change that sets `next: owner` (the `ask` move, `transitions`, `:6179`), or that
  writes a new `ask:` text where `next: owner` stands, on a tracker whose `ask:` has no `ask-id:`. The refusal names the
  next number. An ask before ids that no change touches stays as it is.
- **C2, a put ask changed under its id:** its question, its proposal, its options or its kind (`put_ask`, item 1),
  answered or not. The change that passes is a withdrawal and a new put: the old id's record written by `--clear-ask`,
  the changed ask under the next number. `ask-since:` is not read.
- **C3, an id gone without its record.** `--clear-ask` writes the record.
- **C4, a new id not above every number used:** the front matter, the records, and on git the file's history. The
  refusal names the next number.

**The answer rules** (`lint`, `:8693–8738`):
- **An unknown id:** an `Answers:` trailer that names an id its tracker does not carry at that commit is refused.
  `--answer FM-050-Q9` refuses before writing: `FM-050 has no ask FM-050-Q9: it holds FM-050-Q2, open; FM-050-Q1 is
  in its record`.
- **An id already answered:**
  - `--answer` refuses as today (`:2751`), and names revoke and `--supersede`;
  - an id answered and cleared is in the record, and `--answer` says so;
  - the gate refuses two heads for one id (3b) until one answer replaces the other, on a branch that holds both.
- **A reused number:** F3, C2, C4 and C5.
- **An answer that names an ask its tracker no longer holds open:** `--answer FM-050-Q2` while the tracker holds
  `FM-050-Q3` refuses before writing: `FM-050 holds another ask now: FM-050-Q3, since <date>: "<question>".
  FM-050-Q2 was withdrawn and is in FM-050's record. Nothing was written. Read FM-050-Q3, then answer it by its id.` The
  gate refuses what such an answer becomes:
  - an answer beside an id no head names (3b): a merge that left the answer under `FM-050-Q3`;
  - an answer under an id that the record shows withdrawn (F3).
- **The Owner names the ask they read.** `--answer FM-050` on an ask that carries an id refuses, and names the id.
- **Two branches that each mint the same number for one tracker** (FM-027's lesson): **C5**, on git.
  - **The ids a branch proposes:** those its copy of a tracker holds, open or in a record, that the copy at its merge
    base with the default branch does not hold (one `git merge-base`; the copies read by one `cat_blobs`). An id the
    merge base already held is the default branch's own, carried by the branch, and the merge brings its later state
    (an answer, a clearing) in step.
  - **The default branch's numbers:** its copy's open ask, and every record under its `## Asks`, answered or withdrawn.
  - **A proposed id passes** where it is above every number of the default branch's copy, or where the default branch's
    open ask holds it with an equal put ask (`put_ask`): one ask put on both branches, as by a cherry-pick.
  - **Every other proposed id is refused on the branch,** and the refusal names what holds it:
    - the default branch's open ask with another put ask;
    - or a record of the default branch, whatever its question. An id the default branch has archived, held open or
      archived again on the branch, comes back beside that record after the merge. A record keeps only the question,
      so the refusal quotes it for the seat to see whether it is the same ask; the id decides.
  - **The refusal names the next number** above both copies. The default branch keeps its number, as the first to merge
    does for tracker ids.
  - **Where:**
    - in `lint`, by the pre-commit hook where the clone holds the default branch, and by CI on the branch's pull request;
    - in `--queue`, the same reading of each pull request's head against its base, beside `triage_reading` (`:2640`):
      `wait: FM-050-Q2 is taken on origin/main — renumber`. The Owner's merge view says it even where the branch's last
      check ran before the other branch merged.
  - **Where both open asks reach one merge:**
    - git's conflict on the front matter stops it;
    - a resolution that keeps one put ask with the other's answer is refused (3b: the put ask is not the one
      answered);
    - the put ask the resolution drops is the merger's to put again, under the next number.
  - **Where a stale check let an open ask in beside a record with its id:** F3 refuses on the default branch. The open
    ask is renumbered to the next number, its put ask unchanged. This is the one change that moves an id without a
    record of its own: the record that holds the id is the other ask's, and a second record would make duplicate
    archived ids. An answer the open ask carried does not follow, since its commit names the old id: the Owner answers
    again under the new number.

### 5. What the board, `--standup` and `--owner` print

**The id is part of *what it is*** (the design guide's §6: the row reads *what it is* · TYPE · state · action).
- **An ask with an id:** the id, linked to its tracker, then the question.
- **An ask before ids:** its tracker's id, then the question, with `asked before ask ids` in the state.
- **The words follow the design guide's §6 and §10:** lowercase labels, the age as `2 days`, and a full date in a
  command's output. The kinds' words (DECISION for `ruling`, ONE CLICK for `ceremony`) and the headings are the guide's
  label change, made with it; this build adds the id.
- **One new label:** `ask.legacy`, *asked before ask ids*, in English and German, under the key-parity check.

- **The board** (`render_html`, `:4641`):
  - *waiting for you* (`:3775–3776`): `FM-050-Q2 Do you adopt …?` · DECISION · `2 days · holds up <ITEM>` ·
    **accept** **reject**;
  - the row's ask cell (`:4661`) gains the id as its 13th item;
  - the dialog reads `accept · FM-050-Q2`, then `sign your answer · FM-050-Q2` (3c);
  - the tracker view shows each record with its id;
  - the search (`:3670`) reads `FM-050-Q2` as its tracker, FM-050.
- **`--owner`** (`owner_digest`, the ask lines `:2100–2101`):
  ```
  FM-050-Q2 · decision · 2 days · holds up <ITEM>
     Do you adopt the ask-id design and R4's answer commit …?
  FM-023 · decision · 2 days · asked before ask ids
     Do you allocate v0.20.1 …?
  ```
- **`--standup`** (`:2153–2156`):
  ```
  DECISIONS
    1. FM-050-Q2 — Do you adopt the ask-id design …?  [2 days]  [frees <ITEM>]
    2. FM-023 — Do you allocate v0.20.1 …?  [2 days · asked before ask ids]
  ```
- **`--answered`** (`:1916`) heads each answer with its id, `FM-050-Q2 · answered <date> by <name>`, and points to
  `--clear-ask FM-050-Q2 <next move>`. Its acted-on lines name the record's id.

### 6. The class test the build carries

- **The program:** `test_ask_ids.py`, standalone, run on its own and from `test_shoalmark.py` as `test_owner_exemption.py`
  is (`test_shoalmark.py:14694–14695`). Locally it runs on its own; CI runs it inside the suite.
- **The fixture:**
  - a bare `origin`, with `main` as its default branch;
  - the Owner's SSH key in the default branch's signers file, and a seat's identity;
  - two branches cut from one commit;
  - each row builds its history and states its verdict: refused, with the refusal's words, or accepted.
- **The rows:**
  - **Form, F1–F2:** an id naming another tracker; `Q0`; a leading zero; a capitalised key; two `ask-id:` lines; an id
    with no question.
  - **Minting and reuse, C1–C4 and F3:**
    - a put with no id, whose refusal names the next number; an ask before ids reworded in place, refused the same way;
    - a question, a proposal, the options or the kind changed under its id, each refused; the same, withdrawn and put
      as the next number, accepted;
    - an id dropped with no record; the same through `--clear-ask`, accepted;
    - a new id equal to a record's;
    - a new id below the highest number in the records;
    - a number written and removed in the file's history: refused on git, and accepted in the plain-folder fixture,
      with its limit line;
    - two records with one id: refused where they are new on the branch; a note where both have landed on the default
      branch, with the next number above both.
  - **Two branches, C5:**
    - both mint `Q2` and A merges: B refused by `--check` and in `--queue`; B renumbered `Q3`, accepted;
    - A answers and clears `Q2`, and B's open `Q2` merges clean beside A's record: refused on B before the merge,
      because C5 reads the default branch's records, by `--check` and in `--queue`; and by F3 after a merge made without
      the check;
    - A and B each clear a `Q2` of their own: duplicate archived ids, refused on B by C5 and F3; after a merge made
      against the gate, a note on the default branch naming both, and the next number above both;
    - B carries `Q2` from its merge base while A answers and clears it: not proposed, accepted, and the merge brings A's
      record in step;
    - B proposes `Q2` while the default branch's highest is `Q3`, and holds no `Q2`: refused, naming `Q4`;
    - both open: the conflict, and a resolution that keeps A's question with B's answer, refused;
    - one ask cherry-picked to both branches: accepted.
  - **The answer's binding, 3b:**
    - the Owner's signed commit with `Answers:`, accepted on its branch, and on `main` after a merge commit made by
      another identity. This is FM-056's case: no `line_author`;
    - no trailer;
    - a trailer naming another id;
    - `Answers: FM-001-Q12` against `FM-001-Q1`;
    - a seat's unsigned answer;
    - the Owner's key added to the branch's own signers file only;
    - a seat's commit that restores an answer the Owner revoked;
    - two Owner answers to one id on two branches, refused; then one replaces the other, accepted;
    - an answer commit that also rewrites the question;
    - the Owner's **signed** bare acceptance (`--answer <ask-id> accept`, no words), then a seat's **unsigned** edit of
      its proposal, of its options, and of its kind: each refused twice, by C2 on the seat's change and by the binding
      on the standing answer, and the row asserts both refusals; a seat's edit of its `ask-since:` alone, accepted;
    - `answered-by:` not the head's author;
    - a squash merge of the answer.
  - **The commands, 3c:**
    - `--answer` with an unknown id;
    - an id the tracker no longer holds open, whose words are the refusal above;
    - a tracker id where the ask has an id;
    - an id already answered, then `--supersede`;
    - after each `--answer`: no `answer/<id>` ref, `origin`'s refs unchanged, the branch unchanged, and on a refusal
      the file restored.
  - **Asks before ids, item 2:**
    - an open ask without an id, answered by its tracker's id and verified as today;
    - its record, which reads *asked before ask ids*;
    - the board, `--owner` and `--standup` lines of both kinds.
- **The mutants:** each is a patched copy of one function in the imported module, and each must turn at least one row
  red. Each one undoes one rule:
  - **the head found by `line_author`:** the reader goes back to the line;
  - **a trailer matched by its prefix:** `Q12` answers `Q1`;
  - **the question left out of the binding:** an answer can sit under another question;
  - **the binding compares the question alone** (`put_ask` without the proposal, the options and the kind): in the
    signed bare acceptance row, the binding's refusal goes missing, so the row turns red;
  - **no check for two heads:** two answers to one id both stand;
  - **C4 without the history read:** a number lost from the file is minted again;
  - **C5 against the branch's own base:** the default branch is not compared;
  - **C5 without the default branch's records** (its open ask alone): the row where A answers and clears `Q2` and B's
    open `Q2` would merge beside it passes on B, so the row turns red;
  - **signers read from the checkout:** a branch's key vouches for itself;
  - **the next number from the front matter alone:** the records are not counted;
  - **`--answer` by tracker id on an ask with an id:** the Owner can answer an ask they did not name;
  - **C2 off:** a put ask changes under its id.

### 7. What *never reused* can claim on each backend

- **Git:** never reused as far as these show: the file, its history reachable from `HEAD`, and the default branch's copy,
  its open ask and its records (C5). A number minted on a branch this clone has not fetched is not seen until it is fetched; C5 refuses it on the
  branch, and `--queue` waits on it, once it is.
- **Subversion:**
  - **what it reads:** the file, and the log of its path (`svn log --xml <file>`). The log's messages are read for
    `<ITEM>-Q<n>`. The build's README tells seats there to name the id in the message that puts the ask; the gate
    cannot hold them to it, because Subversion runs no hook on the machine that commits.
  - **what it cannot show:** a number written and removed in revisions whose messages do not name it. The log holds no
    line's text, and reading each revision's diff costs one server call per revision, which the design does not make.
  - **the answer:** the server-authenticated committer of the answer line, as today (`line_author`'s Subversion branch,
    `:5560–5576`), and that revision's message must carry `Answers: <ask-id>`. A server login is the proof, not a key.
- **No version control:**
  - **what it reads:** the file alone, its front matter and its records;
  - **what it cannot show:** a number removed without its record, and two copies of the folder that each mint a number;
  - **the answer:** nobody is shown as having answered (*no author*).
- **Where each says it:**
  - `--schema`'s `ask-id` row;
  - on Subversion and with no version control, `--check` prints one note per run where a tracker carries an id:
    `note: ask ids are checked against the file and its log` (or `the file alone`), followed by the limit above.

### 8. The build: size, tier, order of commits

- **Tier: critical,** for signing and rights. A Reviewer in a session of its own; CI on the pull request.
- **One branch** (`fm/050-r4-ask-ids`), with R4's deletion first and the ids after it: within a release, deleting comes
  before adding (the current path's line 5). The last commit of R4's part is a stopping point that can be reviewed on
  its own and released alone. Its answers are all asks before ids, verified as today.
- **The size, a guess at 70 % confidence:**
  - **R4 is M–L:** about 550 lines leave `shoalmark.py` and about 60 change. 221 lines of `test_shoalmark.py` name
    `answer/`, so the tests that leave are the larger part.
  - **The ids are M:** about 300 lines join `shoalmark.py`, and about 450 join the class test.
- **The order of commits.** Each code commit carries its own tests, and docs follow in their own commits:
  - **R4's part:**
    1. `owner_change` commits on the branch the Owner stands on: no cut, no push, no switch, no refusal record, no
       `unmerged_advice`. `--done`, `--due` and `--revoke` lose their branch readings.
    2. The board, `--owner` and `--standup` stop reading answer branches: `answer_refs`, `on_their_way`, the way lines,
       the 32nd cell, the revoke dialog, `board_basis`'s refs. `--answer` rebuilds the board itself.
    3. `--queue` reads every pull request alike, and the Owner's own commits read `merge: yours — signed`. The
       answer-branch readers leave.
    4. The dialog's second screen and its labels, in English and German.
    5. Docs: the README's rows; `docs/index.md`, `docs/signing.md` and `docs/standup.md` with their German pages;
       `--schema`; the CHANGELOG.
  - **The ids:**
    6. `ask-id:`: the schema, `ASK_LINES`, `GUARDED_KEYS`, `extract`, and F1–F3.
    7. C1–C4 in the walk, and `ask_numbers`, on all three backends.
    8. C5: one reading of proposed ids against the default branch's open ask and records, in `lint` and in `--queue`.
    9. The answer commit: `--answer <ask-id>`, the trailer, the refusals, `answer_commit`. `line_author` leaves the answer
       gate for asks with ids, `signed_line` and `answer_cmd`'s `replaced`.
    10. `--clear-ask` writes the id. The board's row, dialog and search; `--owner`, `--standup` and `--answered`.
    11. `test_ask_ids.py`, its rows and its mutants, wired into `test_shoalmark.py`.
    12. Docs: the README's ask rows, `--schema`, the signing page, and the CHANGELOG.

### Open questions, for the Reviewer and the Owner

1. **Where the answer lands.**
   - **Proposed:** `--answer` commits where the Owner stands and does not push. Landing it is ordinary git.
   - **The alternative:** one command that also pushes the branch it committed on.
2. **Who may answer.**
   - **Proposed:** the default branch's `owners_at`: the `owner` line and any name its `[rights]` gives `answer`, as the
     triage guard reads it.
   - **The narrower reading:** the `owner` line alone.
3. **`--queue`'s `merge: yours — signed`.** Is it R4's replacement for the `answer/*` reading, or does every pull
   request take a verdict, with the Owner merging their own by hand?
4. **C2's strictness.** Under it, any change to a put ask, its question, proposal, options or kind, costs a number.
   The looser rule allows changes until it is answered: the binding would still keep an answer to the put ask it was
   given to, but the record would no longer show the first one as withdrawn.
5. **The `ask` right.** Who may put an ask is still read through `line_author` (`seat_problems`, `:6117`, at `:6131`),
   and FM-056 holds that. The ids do not change it.
6. **What C5 does not see.** C5 compares copies: the default branch's open ask and its records. A number the default
   branch used and lost without any record after the branch was cut is not seen by C5. C3 refuses that loss on the
   default branch itself, and C4's history read covers what the branch's own history holds.

## Done when

- The design is written here, reviewed by an independent Reviewer, and ruled by the Owner.
- Built: every ask carries its id on the board and in `--standup` and `--owner`; an answer commit names it; the gate
  refuses an unknown, answered or reused id, and a put ask changed under its id. One test covers the class: every way
  an id could be reused or mismatched, across two branches included.

## Asks

**2026-10-27** · Do you adopt the ask-id design and R4's answer commit as FM-050 states them under The design in the commit that last filed this ask?
**answered** — accepted - yes · holgo99
**relation** — accepted the proposal
**signed** — b7b9cac · G

## Ship log

| Date | Event |
|---|---|
| 2026-10-15 | Designed by the Builder seat (`27f31560/builder-5`): `## The design`, the ask-id design with R4's answer commit, and its open questions; the ask drafted (`next: review`) for the Planner to put to the Owner. Records only. |
| 2026-10-15 | Filed. |
| 2026-10-16 | Reviewed, not ready (`cc9e80b`): two findings go back to the Builder; the base's list of waiting asks is corrected forward by the Planner. |
| 2026-10-16 | RV-3284 (recorded privately) fixed in the design, by the Builder seat (`27f31560/builder-5`), from the Planner's draft. |
| 2026-10-16 | RV-3285 fixed in the design, by the Builder seat: C5 compares the ids a branch proposes with the default branch's open ask and its records, answered or withdrawn, in `lint` and in `--queue`; duplicate archived ids are defined; a row and a mutant cover the records. |
| 2026-10-16 | Round 2: READY (`ed2c82b`). The ask put to the Owner by the Planner (`next: owner`), filed at this commit so the answer binds the reviewed body. |
| 2026-10-16 | A case recorded: the board hid FM-053's re-filed ask while the first answer's `answer/fm-053` was on its way; ask ids fix it. |
| 2026-10-16 | The Owner's word: *on their way* (FM-030), in the board's code but in neither §1 nor §7 of the guide, goes into FM-050; its design round places it in the guide, beside the case of FM-053's hidden ask. |
| 2026-10-27 | Its ruling ask filed again by the Planner seat, on today's main, with what changed since 16 October; the design unchanged. Records only. |
| 2026-10-27 | The Owner's signed answer adopts the design; its ask cleared; judged In Progress, P2, critical, for v0.20.2 as batch 3's S1. Records only. |
