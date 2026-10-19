---
id: FM-059
status: Proposed
considered: FM-050, FM-007, FM-054, FM-058
tags: process
next: review
hook: "The Owner answers each ask in a Board view that holds only its dialog; a prepared run stops there, and signs and pushes only the line the Owner chose"
---

# FM-059 — the Owner answers each ask in a view of its own, and a prepared run signs only what they chose

## What is true now

**2026-10-19 — the design amended, and its ask withdrawn until the amended sections are re-checked.** The Owner
spot-checked the design with the Designer on 17 October (screen 14, `179bfc2c…`), and gave their position on open
question 3 on 19 October. The design now carries:
- *decide later* in the view (§2, §3, §5, §6);
- the view's own read-at words (§2, §6), with the one sentence G6 gains;
- no result hidden behind the next view (§2, §4);
- the seat's reasons from new record fields, with a fallback (§2);
- one verb, *pick* (§6);
- the Owner's positions on the open questions.

A signed answer the run pushes is out of the board's sight. That is filed as FM-064, and its fix lands with this build
(§4). The ask put on 2026-10-17 is withdrawn, and its record is under `## Asks`. It is filed again once a records
re-check finds the amended sections READY.

**Filed 2026-10-16 on the Owner's direction, with its ask. Its design started the same day, the Owner with the Designer;
nothing is built.** On the Owner's word of the same day it is quick win 11, in v0.20.1: the ask's first proposal, the
first release after v0.20.1, is withdrawn (its record is under `## Asks`), and the ask is filed again proposing v0.20.1.

- **What the Owner asks for:** a prepared run (today a run sheet) brings each branch that carries an ask, then stops at
  the answer and opens a Board view holding only that ask's dialog, with help text on what the answer signs and what
  follows it. The Owner reads it and chooses an option, or rejects. Only then does the run sign exactly the line they
  chose, push it, and go on to the next ask.
- **Until it ships:** a run sheet prepares and stops before any answer, and the Owner answers from the Board.
- **Two requirements for its design, recorded privately.** They go into its design brief.
- **Designed 2026-10-16** (`## The design`, below), by the Builder seat. Reviewed in round 1, not ready (`8ba48f6`),
  and in round 2 READY (`394ad4d`): its six findings are fixed below. Nothing is built. The design holds
  for either answer to the release ask. Its own ruling ask is put (2026-10-17): whether the Owner adopts the design and
  its seven proposals, the *Proposed* lines of its open questions.
- **The release ask is answered:** *accepted - v0.20.1*, the Owner's signed answer (`99b1708`), recorded under `## Asks`.
- **What it needs first:** R4's ask ids (FM-050), and FM-058's fix, so that a command a person runs has no time bound;
  FM-058 moves into v0.20.1 with it. The seat's confidence, *because* and *then* come from new record fields: quick
  win 11's S3, which stays in v0.20.1 (§2). An ask without them takes the fallback.

## The design

Every line number is `shoalmark.py` at `f65b1bb` (main). The design builds on FM-050's design at `03ef687`: R4's answer
commit (3a), how the gate binds it to its ask (3b), `--answer <ask-id>` (3c), the put ask (§1) and C5's reading of the
ids a branch proposes (§4). It needs FM-058's fix: a command a person runs has no time bound. Its links reuse R11's one
link helper (FM-057), built now, and the hooks' copy first records the tool's commit (§9). The view follows the guide on
`release/v0.20.1` at `f2359b3`: G5 (a diff for the change a command commits), G6 (the guided answer view) and G7 (its
one help line), pending the Owner's signed answer on FM-053. The approved screen is the quick-wins design of 16 October,
recorded privately. Requirements recorded privately bind it (item 7).

*The run* is `--guided`. *An ask* here is an open put ask with an id (FM-050 §1): `ask-id:`, `ask:`, `next: owner`,
and no `answer:`. *Its home* is the branch its answer is committed on (item 1). *The checkout* is the Owner's own.

### 1. The prepared run

- **What starts it:** the Owner runs `--guided`, or `--guided <ask-id> …`. A run sheet an agent prepares writes the
  second form: the asks it brings, in its order. With no id, the run brings every ask that `origin` carries.
- **Where it runs.** Checked in this order before any ask is read. Each refusal is one line that names what fixes it.
  Nothing is read or written, but for what item 5's fetch writes to the clone's git metadata:
  1. **git** (`vcs()`, `:193`), 2.36 or later, which has `git hook run` (item 4). Subversion and no version control:
     item 5.
  2. **a terminal on its input:** the run waits for a person's paste. With none (CI, an agent's shell, a pipe) it
     refuses. This keeps an unattended start out; it proves no hand (FM-007).
  3. **not the hooks' copy** (`HOOK_RUN`, `:59`): a hook's run of the copy is bounded, and writes only inside the
     repository.
  4. **who may answer, and that the answer is signed,** asked once, as `owner_change` asks it (`:3051–3081`): the
     default branch's `owners_at` (FM-050 3a); git's author equal to `user.name` (`:3077`); and an identity marked
     `signed` (`owner_change`'s `signed`, `:3065`), with a signing key (`:3071`). This build signs every answer, so an
     author-only identity is refused here, before any view, naming the signing page (`SIGNING_PAGE`, `:62`) and the
     configuration line that marks it `signed`. Other commands keep their author-only meaning. The Owner never reads a
     view they cannot sign.
  5. **one `git fetch origin --prune`,** the run's one read of the forge. Then the checkout: on the default branch
     (`default_trunk`, `:3261`), at `origin`'s tip, with no tracked change (`changed_paths`, `:3369`; `dirty_refusal`,
     `:3382`). The tool it runs from is that checkout's: the files `copy_files()` names (`:9587`) equal that tip's at
     their path, compared canonically. Each CRLF is read as LF, the line ending a text checkout writes (`core.autocrlf`,
     or a `text` attribute), and every other byte is kept, as `install_copy` hashes them (`:9625`) and
     `hooks_copy_drift` compares them (`:9717`). Where hooks are installed, the hooks' copy (`COPY_DIR`, `:9394`) holds
     the same files, as `hooks_copy_drift` compares them (`:9700`): an older copy would judge an answer commit by older
     rules. Its record names the commit it was taken from (§9's prerequisite). Otherwise it refuses, naming
     `--install-hook` on the default branch.
- **Configured once, from the checkout.** `configure` (`:799`) reads its `shoalmark.toml`; the labels and themes come
  from `brand()` (`:4673`); the signers file is the default branch's (`trusted_signers`, `:5751`). Every view in a run
  reads by one configuration, and who may answer and which keys verify are the default branch's, as FM-050 3a has it.
  Of each branch, the run reads its tracker files, as text, and nothing else. It is dispatched in `main` (`:10388`)
  before `load_trackers` (`:10482`), as `--queue` is (`:10467`): it reads its asks itself, from git.
- **What it reads, and how:**
  - **the branches:** one `git for-each-ref refs/remotes/origin/`, without `origin/HEAD`. Forks and local branches are
    not read;
  - **each branch's tracker directory** (the checkout's `tracker_dir`) at its tip: one `git ls-tree` per distinct tree,
    and the blobs that differ from the default branch's by one `cat_blobs` (`:7233`). A blob that many branches carry is
    read once;
  - **each file** is parsed as `extract` parses one (`:1404`), and its ask is held to `ask_problems` (`:1620`). A
    malformed ask is never brought, as `owner_queue` keeps it out of sight (`:1671`).
- **Each ask's home,** by C5's reading (FM-050 §4):
  - **the branch that proposes it:** its copy holds the id, and its copy at its merge base with the default branch does
    not (one `git merge-base` per such branch);
  - **else the default branch,** where its copy holds the ask (item 4 says where that answer goes);
  - **not brought,** each named on the first line with its reason: an id that two branches propose; an id that some
    branch holds answered (an answer on its way); an id with a local `guided/<id>` branch, signed and not pushed
    (item 4); an id the default branch holds with another put ask; an ask before ids, answered from the board as today
    (FM-050 §2).
- **The order:** the ids as named. Else the oldest `ask-since:` first, then the tracker id, as `--owner` lists them.
- **Before a pick, never:** a signature, a commit, a worktree, a push, a written answer, or a write in any working
  tree. The one exception is the clone's git metadata, which item 5's fetch writes: objects, `FETCH_HEAD`, and
  `origin`'s remote-tracking refs, added, moved or pruned. Beyond that the run writes only its views and its log, in a
  folder of its own outside every repository (item 2).
- **The terminal:** its first line says what the run read and when. Then it prints one line per ask as that ask ends.
  Its last line always says what it waits for. The output of its own steps (the fetch, the worktree, the gate) is held
  back in the run's log and printed only on a failure: its last lines, and the log's path.

### 2. The view

- **What it is:** one HTML file per ask, written by `render_guided` (new) for that ask and nothing else of the board.
  It takes the board's page head: the tokens, the themes and the labels, read once from the checkout. `render_html`'s
  head (`:4670–4690`) is factored, so that both pages write one head. Its script is small: a pick shows its lines, and
  the reply button copies. **The view signs and runs nothing** (R5), and loads nothing.
- **Where it is written:** in the run's folder, made by `tempfile.mkdtemp` (mode 700) in the system's temporary
  folder, outside every repository; each file is mode 600. The run opens it with `webbrowser.open` on its `file:` URL.
  Where no browser opens, the terminal prints the path.
- **What it holds,** as G6 draws it:
  - **the header:** the name, and why it opened (*your answer is needed · 2 of 3 in the run you started*, the first
    words amber); the read-at line, *written once, for this ask: it does not change while you answer*, with the home,
    its commit and the time, and the tool's commit (both linked, below); the limits, folded: the ask as filed at that
    commit, and nothing else of the board; whether the run still waits is not known here;
  - **the view never reloads:** a reload would lose the pick and the typed text while the Owner pastes in the terminal.
    So the view carries neither the board's line (*it reads its file again when you come back to it*) nor *this page
    does not update itself*. G6 gains one sentence: *a view's read-at line is not the board's: a view is written once,
    for one ask, and never reloads*;
  - **before this,** in the header from a run's second ask on: how the ask before it ended, as *before this: 1 of 2 ·
    <ask id> · signed <sha> · verified · pushed*;
  - **one window,** titled *your answer · <ask-id>*: the question, then its state: its kind, who put it, how long it
    has waited, what it holds up (`held_up_by`), and its tracker;
  - **`## your choice`,** on a `--secbg` band: one row per choice, with a radio, a letter and the words. **A** is the
    proposal, labelled PROPOSED. The other options follow in their filed order, as the board's dialog orders them
    (`act`, `:3711`). Then *in your own words* and *reject the question*, each with its typed box, three lines high.
    Under *or, not now:*, one more choice, *decide later*, signs nothing (item 5). Nothing is picked;
  - **the seat's reasons,** from the record's new fields (A32), which quick win 11's S3 builds in v0.20.1:
    - on the proposal, its confidence: a number for how sure the seat is;
    - under each option, its *because* (the rationale) and its *then* (what follows if it is picked);
    - where an option lacks one, that line reads *not stated*.

    **An ask with none at all** shows the choices alone. Its line links the tracker at the commit it was read from,
    through R11's link helper, which says why where there is no link, and the help line says the reasons are there;
  - **the record's new fields** (A32; the Planner's, at 70 %). They sit in the front matter beside the ask, so that the
    gate reads them as it reads the ask:
    - `ask-confidence:` a whole number from 0 to 100, the seat's percent for its proposal;
    - `ask-because:` and `ask-then:`: one entry per option, in `ask-options:`'s order and separated by ` | ` as it is,
      each at most 120 characters. An empty entry reads *not stated*;
    - **the gate refuses:** a confidence that is not a whole number from 0 to 100; an entry list whose length is not the
      options'; an entry over 120 characters or with a control character; any of the three on a tracker with no put
      ask (`ask:`), open or answered; and `ask-because:` or `ask-then:` without `ask-options:`;
    - **they live as long as the ask:** they stand beside the put ask through its answer, accepted or rejected, as every
      `ask-` line does (FM-050 3a). An answer writes its lines below them and changes none of them, and `--clear-ask`
      then moves them under `## Asks` with the exchange. The board's dialog does not show them in this build. With ask
      ids (FM-050), each entry's place is its option's while the ask stands;
  - **what follows any answer** stands once, in the lines: the `next:` that `ANSWER_MOVE` gives the ask's kind
    (`:942`), the same for every answer, and who moves next: the seat that asked, or for an action the Owner's hands;
  - **the one help line** (G7): inside the window, under *your choice*, pending FM-053's signed answer. Without it,
    the line stands above the window;
  - **`## where you sign`,** on a `--secbg` band: empty until a pick. A pick shows the change as a diff (G5): the
    tracker's path, the home, `+n −m`, and every line the commit writes, in full. Below it, `INDEX.md` is named as the
    index the commit's hook regenerates from it. Then *how you sign* in three steps, and at the window's foot the
    *reply* copy button, filled, with its copy feedback.
- **The commits, linked,** as the Owner ruled on 16 October. Three commits are named: in the header, and again in
  the result, the tool's as its TOOL row. The Designer draws both views:
  - **the ask's:** the home and the head the ask was read from (`<home> @ <sha>`);
  - **the answer's:** in the result, the commit the run made, pushed or not;
  - **the tool's:** the commit of the tool the run runs (item 1), read as data:
    - **a pinned tool:** the PIN's manifest line (`MANIFEST_RE`, `:9159`; `pin_manifest`, `:9163`): its tag and its
      full commit, or `untagged` with its full commit and `(dirty)` (§9). A PIN written before records ten
      characters, or `(no git)`: the row names it as written, and says that it is incomplete;
    - **a tool run from the working tree:** the checkout's full HEAD, and whether the tool's files equal it. At the
      run's start they do (item 1);
    - **the hooks' copy,** which runs the commit's hooks: the commit its record names (§9's prerequisite), and that its
      files equal the run's (item 1).
- **Their links,** as ruled, each made by R11's one link helper (FM-057), which the view reuses:
  - **a commit of this repository** links only through its own forge configuration, the checkout's. `blob` (`:74`;
    `board_blob`, `:4621`) gives the commit URL: `…/blob/<ref>/…` gives `…/commit/<full sha>`, and GitLab's
    `/-/blob/` gives `/-/commit/`. Where a forge's prefix gives none, the one key R11 adds gives it. No link is ever
    derived from a remote URL alone: the tool never guesses whether a remote is public;
  - **the tool's commit** links to the public shoalmark repository (`TOOL_PAGE`, `:63`) where it is a release's
    commit: a pinned, tagged copy. A working-tree tool's commit is the repository's own, so it links as the
    repository's commits do, and only if pushed;
  - **no link, with a few words of why,** for: a commit not yet pushed, in no remote-tracking ref of `origin` (the
    answer's commit before its push, or after a check that stopped the run); no forge (`blob` empty); and Subversion
    without a viewer, which the run never reaches (item 5). Nothing guesses whether a remote is public, so an untagged
    pinned copy, which is no release, shows no link either, and says why.
- **The lines are the run's:** it computes them once per choice, with the function `--answer` writes with (item 4), and
  writes them into the page. The script only shows the ones picked. For *in your own words* and *reject*, the page
  holds the lines with the text left out, and the script puts the typed text in, normalised as `answer_norm`
  normalises it (`:1723`). The run computes them again from the reply (item 3).
- **The result view** is a new file. It opens only on a failure that ends the run (a check that stops it) and at the
  run's end, with the whole run under `## this run`: one row per ask, as it ended. Between asks no result view opens,
  and the next ask's header says how the last one ended (*before this*, above). Its read-at line reads *written once, at
  the run's end: it does not change*. For each answer it shows the change as signed, then COMMIT (its sha, the home, pushed or not), SIGNER (the key's fingerprint, as the signers file lists
  it), SIGNATURE (*verified*, with its meaning, on `--okbg`, or *not verified*, with git's letter, on `--failbg`) and
  TOOL (the tool's commit, and the hooks' copy's where it ran the commit's hooks), each commit linked as above. Where
  nothing was pushed, the result says the ask still waits, and what happened.

### 3. The hand-back: a pasted reply

**Decided: a pasted reply, and no server.**
- **Why:**
  1. The view stays a page that signs nothing and runs nothing, with one button that copies (R5).
  2. The Owner is at the run's terminal anyway: the key asks there, and the terminal prints the lines again before it
     signs. The paste happens next to what it causes.
  3. Nothing listens on the machine: no port, no process to stop, and no request to tell apart from another program's.
- **The cost:** one copy and one paste per ask. A local server would spare the paste, at the price of a background
  process that any program on the machine could talk to.

**The reply** is one line: `<ask-id> <choice> [<text>] run:<code>`. For example:
- `FM-059-Q1 A run:e3b71f`;
- `FM-059-Q1 D 'a later release: v0.21.0' run:e3b71f`;
- `FM-059-Q1 reject 'ask again once FM-058 has shipped' run:e3b71f`;
- `FM-059-Q1 later run:e3b71f`.

**Its parts:**
- **the choice:** a letter as the view letters it (A, the proposal; the other options after it; *in your own words*
  the next letter), or `reject`, or `later` (the view's *decide later*), which takes no text;
- **the text,** for *in your own words* and `reject` only: the box's words as `answer_norm` leaves them (`:1723`:
  trimmed, every run of whitespace one space, `"` written as `'`), single-quoted as the board quotes a command today
  (`sq`, `:3705`);
- **the code, last,** so that a reply cut anywhere loses it.

**The code:**
- six lowercase hex characters (`secrets.token_hex(3)`), one per ask in each run. It is written into that ask's view
  and kept in the run's memory;
- it is good for that ask's wait in this run. It is spent when the run takes a reply for that ask, a `later` reply
  among them, when the Owner types `later`, and when the run ends. No clock bounds it (FM-058).

**What the run accepts.** The run reads the line from its terminal itself, never through a shell, and splits it into
words as a POSIX shell would (`shlex`). It accepts the reply only when all of these hold:
- the id is the ask it waits on, and the code is the one it wrote for that ask in this run;
- the choice is one the view offered;
- a text stands exactly where the choice takes one: not empty, with no control character, and unchanged by
  `answer_norm`;
- nothing follows the code.

Anything else is refused in one line that says what the reply was (*from FM-050-Q2's view*, *from another run*, *a
choice FM-059-Q1 does not offer*, *cut: its code is missing*) and that nothing was signed. The run waits again at the
same ask, with the same code.

**A long reply.** The run reads its line through `readline` where Python has it, so a paste longer than the
terminal's canonical line limit (`MAX_CANON`, 1024 bytes in macOS's `sys/syslimits.h`) is not stopped by that limit.
That a plain read would stop one is a guess, at 75 %. A reply cut anyway has lost its code, and is refused.

**Before it signs,** the run prints the lines again, with the prepared commit's full message and `INDEX.md`'s changed
lines, and then asks the key (item 4).
Where the lines it would sign now differ from those the view showed for that reply (the date turned during the wait,
or an action's `due:` is read from typed words), it signs nothing until the Owner types `yes` under the new lines.
Anything else signs nothing, and the run waits again.

### 4. The signing and the push

- **The commit is R4's answer commit** (FM-050 3a): one parent. In the ask's tracker it writes `answer:`,
  `answered:`, `answered-by:` and `next:`, and `due:` where R4 seeds it; it leaves the put ask as its parent has it. Its
  subject is `<ask-id>: <the answer, cut between two words>`, and its trailer `Answers: <ask-id>`.
- **The line each choice writes,** each option's words as filed, through `answer_norm`:

  | The choice | The line |
  |---|---|
  | A, the proposal | `answer: "accepted - <the proposal>"` |
  | another option | `answer: "accepted - <that option>"` |
  | in your own words | `answer: "accepted - <the typed text>"` |
  | reject | `answer: "rejected - <the typed reason>"` |

  `answer_relation` (`:1735`) reads them as it does today: *accepted the proposal*, *chose option n*, *accepted with a
  change*, *rejected*.
- **One function writes the lines.** `answer_cmd`'s write (`:2785–2806`, and the answer's text at `:2766`) becomes
  `answer_lines`, a pure function. `--answer`, the view (item 2) and the commit all call it, so the view, the terminal
  and the commit hold one text.
- **Where it commits:** in a worktree of the run's own, added only after a reply is accepted:
  `git worktree add --detach <the run's folder>/<ask-id> <the home's tip>`. The tip is `origin`'s, as the run read it,
  or as its own last push to that home left it. Before it adds the worktree, one `git ls-remote origin <home>`: a home
  that moved since the read signs nothing, and the ask is named for the next run.
  - **The identity** is read from the checkout (`user.name`, `user.email`, `user.signingkey`, `gpg.format`), passed to
    the commit with `-c`, and checked in the worktree as `owner_change` checks it (`:3077`). Git copies the checkout's
    `config.worktree` into a worktree added from it (git 2.50.1, probed on 16 October); the run relies on that for
    nothing.
  - **The hooks** are the checkout's: `core.hooksPath` as the checkout resolves it, passed to each hook the run
    starts. Shoalmark's own run the hooks' copy (`:9390–9412`), checked at the start (item 1).
  - **R4's core supplies the checks:** `owner_change`'s who may answer, its key and its author (`:3051–3081`),
    factored after R4 so that the working tree is a parameter. `--answer` passes the checkout; the run passes its
    worktree.
- **The prepared commit.** The run prepares the commit unsigned, with every hook's output in it:
  1. it writes the lines into the tracker in the worktree, and stages it;
  2. it runs the commit's hooks itself, in the worktree, as `git commit` runs them: `git hook run pre-commit`, then
     `prepare-commit-msg` and `commit-msg` on a message file that holds the subject and the trailer. The index takes
     what the pre-commit hook stages (`INDEX.md`, `:9403–9407`);
  3. it writes the prepared tree (`git write-tree`), and reads the message file as the hooks left it.
- **The comparison, before the key,** of the prepared tree and message:
  1. against the home's tip, the tracker's change is the lines shown, byte for byte, read as blobs;
  2. any other path that changes is one the hooks' copy names as written (`--print-written`, `:10657–10659`):
     `INDEX.md`;
  3. the message is the subject and one `Answers: <ask-id>`, with at most the `Session:` trailer that
     `prepare-commit-msg` adds where the checkout sets `seat.session` (FM-024).

  Any difference is refused, and the key is never asked. The run removes its worktree, writes the result view, and
  ends: nothing was signed.
- **The signature.** The terminal prints the lines again, with the full message and `INDEX.md`'s changed lines (item
  3), then the go-to-market seat's line (item 6). The run then signs that tree with that message:
  `git commit-tree -S -p <the home's tip> -F <the message> <the tree>`. `git commit-tree` runs no hook, so the commit
  signed is the one compared.
- **The checks after the signature, before the push,** every one, on the signed commit:
  1. its parent is the home's tip;
  2. its tree is the prepared tree, so its change is the one compared;
  3. its message is the prepared message;
  4. the signature: `verified_as` (`:5736`) for the answering identity, against the default branch's signers file;
  5. the binding: R4's `answer_commit` (FM-050 3b) names this commit as the one head for the id, and the put ask at
     the commit, at its parent and in the file is one.
- **A check that fails:** nothing is pushed. The run removes its worktree, and the commit, on no branch, stays only in
  this clone's objects until git prunes it: nothing left this machine. The run writes the result view, prints what
  failed, and ends: nothing more is signed in that run.
- **The push is the run's own named step:** `git push origin <sha>:refs/heads/<home>`, the one commit, fast-forward
  only, never forced. FM-050's open question 1 proposes that `--answer` does not push; the run pushes, and only here.
  - **A seat's branch takes the Owner's commit on top.** The seat fetches before it pushes again. A seat that rewrites
    its branch drops the commit: the ask is open again, or, where the lines stay without their commit, the gate
    refuses them (FM-050 3b).
  - **Where the home is the default branch,** the run pushes to a branch of its own instead: `answers/<date>-<code>`,
    cut from the default branch's tip at the run's first such answer, each later one on top. That makes one pull
    request per sitting, which `--queue` reads `merge: yours — signed` (FM-050 3c). It lands by a merge or a
    fast-forward, never a squash (FM-050 3b). Here, seats never push to `main`, and the Owner merges pull requests
    (AGENTS.md). Open question 2.
    - **Its destination** is that branch, not the home. Each later answer goes on top of the last one pushed there, and
      a commit a refused push kept (below) is never in a later push's ancestry. Where the branch's first push was
      refused, the next such answer is cut again from the default branch's tip.
  - **A refused push** (the home moved, a protected branch, the forge down): nothing is forced and nothing retried.
    This is the Owner's position of 19 October, open question 3.
    - **The signed commit is kept** on a local branch of the run's own, `guided/<ask-id>`.
    - **The run goes on** to the next ask, but not as `later` leaves one: this ask is signed, and not pushed.
    - **Its end names the ask so,** with its branch and the one command that pushes it,
      `git push origin guided/<ask-id>:refs/heads/<destination>`, fast-forward only. The destination is the ask's
      home, or the run's own `answers/<date>-<code>` for an ask the default branch holds.
    - **The next answer** to the same destination goes on top of the last commit pushed there, never on the kept one.
    - **No run brings that ask again** while that branch exists.
    - **Where the destination moved,** that push is refused too. Deleting the branch lets the next run bring the ask
      again, from the new tip.
- **Then the next ask:** only after git reports the push done, or after a refused push's commit is kept (above), the
  run removes the worktree and prints the ask's line: signed, verified, and pushed to its destination or not pushed. Then it
  opens the next ask's view, whose header says how this one ended. No result view opens between asks.
- **The end:** it says, in the terminal and in the result view, which holds the whole run:
  - how many were answered;
  - each ask left, with why: left for later, moved, or not brought;
  - each ask signed and not pushed, with its branch and the one command that pushes it;
  - the run's own branch, if it has one, with the pull request to open;
  - how the board shows each pushed answer: *answered, on its way* until its branch lands on the default branch, then
    answered (FM-050 3c). That holds only with FM-064's fix, which lands with this build. An answer kept unpushed reads
    *signed, not pushed*, with its branch and its command, and the board still shows its ask as waiting. An ask left
    for later reads *nothing signed*.

  The run does not rebuild the checkout's board: the checkout did not change.

### 5. The ways out

- **Not now: decided, in the view and in the terminal.** The Owner approved it on 17 October.
  - **In the view:** *decide later* stands under *or, not now:* as one more choice. Picked, *where you sign* says
    *nothing is signed: you leave <ask id> for later*, with two steps, and its reply (`<ask-id> later run:<code>`) is
    accepted like the others.
  - **At the prompt:** `later` typed does the same.
  - **Either way,** nothing is signed, the ask's code is spent, the run goes on, and the last line names the ask. The
    view keeps one act, the reply button (G6).
- **A view closed before a pick: decided.** The run does not see a tab close, and waits. `open` at the prompt opens the
  same view again, with nothing picked. The waiting line also prints its path.
- **Reject** is a choice like the others, with its reason. It writes `rejected - <reason>` and the same `next:` as any
  answer of the ask's kind. A reworded question is a new ask, under the next id (FM-050 §1).
- **An interrupt, or the terminal closed:** before a reply is accepted, nothing is signed. Between the commit and the
  push, the commit is on no branch and nothing is pushed. The run removes its worktree on the way out. Where it could
  not (it was killed), the next run removes what it left: `git worktree prune`, and the worktrees in its old folders.
- **Subversion: decided, refused in this build.** `--guided` joins the git-only commands (`CLI_GIT_ONLY`, `:8835`),
  beside `--answer` (`:8843`), and is refused before anything is read. The run commits through R4's answer commit,
  which is git's; Subversion's answer is a revision under the server login, which no command makes today. The refusal
  names how an answer is given there today, and says nothing of signing. Open question 4.
- **No version control:** refused the same way. There is no commit to make, and nothing to push.

### 6. The words: drafts

The words a signer reads are the go-to-market seat's. Three come from that seat (16 October); the rest are drafts for
it, handed to it with this design. The German comes after the native read, through `labels.yaml`.

- **From the go-to-market seat:**
  - *how you sign*, step 3: *confirm, if your key asks — the run asks it to sign one commit: this change*;
  - the terminal, before it signs: *asking your key to sign this commit — the lines above: confirm if it asks*. The
    commit's full message is printed above it (that seat's addition of the subject line, at 60 %, taken whole);
  - a Subversion form, should a run work there: step 3 *commit, under your server login — Subversion signs nothing;
    the server names the author*, and the terminal *committing under your server login: nothing is signed*.
- **From the guide** (G6, and the guide's rows for copy feedback and the page's limits): the header, the window's
  title, `## your choice`, *not signed yet*, *in your own words*, *reject the question*, `## where you sign`, *reply*,
  COMMIT, SIGNER and SIGNATURE, and *the key asks you to confirm, and only if it asks*. The view leaves out *this page
  does not update itself*, which is retired, and the board's reload line (§2).
- **Drafts, one per place.** Each is this seat's, for the go-to-market seat to keep, change or replace. The verb is
  *pick* throughout: the view says *pick*, and so do these drafts and the terminal.

  | Where | Draft |
  |---|---|
  | `## your choice`, its state | *pick one · none is picked for you* |
  | `## your choice`, the way out | *or, not now:* · *decide later* |
  | the reject row | *your reason goes into the record with it; to ask again, the seat puts a new ask* |
  | the help line (G7) | *each choice's words are the ask's, as filed · a pick shows its lines under where you sign* |
  | the help line, no reasons filed | *the seat's reasons are in its tracker, linked above* |
  | a reason not filed | *not stated* |
  | `## where you sign`, empty | *nothing picked yet: there is nothing to sign* |
  | `## where you sign`, decide later | *nothing is signed: you leave {ask id} for later* |
  | the header, read-at | *written once, for this ask: it does not change while you answer* |
  | the header, before this | *before this: {i} of {n} · {ask id} · signed {sha} · verified · pushed* |
  | the result, read-at | *written once, at the run's end: it does not change* |
  | above the diff | *one commit, on {home}, changes {ITEM}'s tracker:* |
  | below the diff | *and `INDEX.md`, which the commit's hook writes from these lines* |
  | *how you sign*, step 1 | *copy the reply, with the button below* |
  | *how you sign*, step 2 | *paste it where the run waits: it prints these lines again* |
  | copied | *copied: {reply} · this page cannot know whether the run still waits* |
  | not copied | *not copied: this page has no clipboard here · the reply is selected: copy it yourself* |
  | the result, verified | *verified: it verifies against a key the signers file lists* |
  | the result, not verified | *not verified: git reads {letter} · nothing was pushed · the ask still waits for you* |
  | the result, not pushed | *committed, not pushed: {why} · the ask still waits for you* |
  | the result, its limit | *a signature proves the key, not the hand* (FM-007's words) |
  | the terminal, first line | *read {n} asks on {k} branches of origin at {YYYY-MM-DD HH:MM}* |
  | not brought | *not brought: {ask id}: {why}* |
  | each ask, done | *{ask id} · {i} of {n} · signed {sha}, verified · pushed to {home}* |
  | waiting | *{ask id} · {i} of {n} · waiting for your answer · its view: {path}* |
  | the prompt | *paste the reply here · later: leave this ask · open: its view again* |
  | a refused reply | *refused: a reply from {id}'s view* · *from another run* · *{ask id} offers no choice {x}* · *cut: its code is missing*; each then *· nothing was signed* |
  | the lines again | *you picked {choice}: this commit goes on {home}:*, the lines, and the subject |
  | the lines changed | *these lines are not the view's: {why} · type yes to sign them; anything else signs nothing* |
  | the end | *{k} of {n} answered · left: {each id, with why}*, and the run's own branch, with *open its pull request* |
  | the end, not pushed | *{ask id} · signed {sha}, verified · not pushed: {why} · kept on {branch} · to push it: {command} · the board shows it waiting until then* |
  | the end, left for later | *{ask id} · nothing signed: left for later* |
  | the end, the board | *each pushed answer reads answered, on its way on the board until its branch is merged* |
  | the header, the tool's commit | *run by shoalmark {version} @ {sha}* |
  | the result, TOOL | *shoalmark {version} @ {sha}: {the PIN's release v{version} / this repository's commit, its files unchanged} · the hooks ran the same files, installed from {sha}* |
  | no link: not pushed | *no link: not pushed yet* |
  | no link: no forge | *no link: shoalmark.toml names no forge (`blob`)* |
  | no link: untagged tool | *no link: an untagged copy, not a release* |
  | the result, TOOL incomplete | *incomplete: vendored before whole commits were recorded · vendor again to record it* |
  | an author-only identity, at the start | *your answers here are not signed, and this run signs every answer: mark your identity signed in shoalmark.toml (the signing page: {url}) · nothing was read* |
- **Two shipped strings still say *touch*:** `--answer`'s step 3 (`:3187`) and the dialog's `answer.sign.step.commit`
  (`:3929`; German, `examples/de/labels.yaml:154`). This build gives them the go-to-market seat's words, so that one
  flow never says both.

### 7. The requirements recorded privately

Requirements recorded privately bind this design. How it meets them, and the class test's rows for them, go to the
Reviewer privately. This text does not state them.

### 8. The class test

- **The program:** `test_guided_answer.py`, standalone, run on its own and from `test_shoalmark.py` as
  `test_owner_exemption.py` is. **No browser:** the opener is a recorder that keeps each path it is handed. The reply
  is read through the run's one reader, which the test feeds; one row drives it on a pseudo-terminal where the system
  has one.
- **The fixture:** FM-050's (a bare `origin` with `main` as its default branch; the Owner's SSH key in the default
  branch's signers file; a seat's identity). On top of it: shoalmark's hooks installed from `main`, in the fixture
  only; two seat branches, one proposing one ask and one proposing two; one ask on `main`; and a clock the test sets.
- **The rows:**
  - **nothing signed before a pick:** a seat pushes a new ask to `origin` after the clone's last fetch, so the run's
    first fetch brings it. The baseline is taken right after that fetch: every ref, local and remote-tracking, the
    clone's objects, and every working tree. From then until a reply, after each view is written, none of it changes:
    no commit, no worktree, no ref, no object. The new ask is brought. In the view's file, no radio is set, no lines
    show and no button is filled;
  - **a reply from another ask, or from another run:** ask 1's reply at ask 2's prompt; ask 2's id with ask 1's code;
    ask 2's id with an earlier run's code. Each is refused, its line asserted, nothing is signed, and the run still
    waits at ask 2;
  - **a choice not offered:** a letter past the list; `reject` with no reason; *own words* with no text; a text with a
    control character; words after the code; a reply cut before its code. Each is refused, and nothing is signed;
  - **exactly the chosen line signed:** for A, another option, own words and reject, on an ask whose proposal is not
    its first option. The commit's change is the view's lines for that choice, byte for byte; its `answer:` line is
    item 4's; and `answer_relation` reads it as item 4 says;
  - **the lines changed since the view:** the clock turns a day between the view and the reply. Nothing is signed
    without `yes`; with `no`, nothing is signed; with `yes`, the new lines are signed;
  - **a signature that does not verify:** the Owner's key only in the branch's signers file, and the key absent from
    the default branch's. Each: nothing pushed, `origin` unchanged, the result view says so, and the run ends. With no
    signing key set, the run refuses at its start;
  - **a hook that changes the prepared commit:** a fixture hook that stages one more file, and one that adds a line to
    the message. Each is refused before the key: zero calls to the signing program, no commit made, nothing pushed;
  - **a refused push:** the home moves on `origin` after the `ls-remote`, and a pre-receive hook on the bare `origin`
    refuses. Each time:
    - nothing is forced, and `origin` holds only what the other side pushed;
    - the signed commit is on `guided/<ask-id>`, and the run goes on to the next ask;
    - its end names the ask, its branch and the push command;
    - a second run does not bring that ask while the branch exists;
  - **the next ask:** after a push, the next view opens, and no result view opens between them. The next view's header
    says how the last ask ended, and the end's result view holds every ask. The branch with two asks takes the second
    answer on top of the first. The ask on `main` lands on the run's own branch, and a second such ask lands on top of
    it;
  - **the board after a push:** an answer pushed to a seat's branch, and one pushed to `answers/<date>-<code>`, each
    read *answered, on its way* on the board until the merge (FM-064);
  - **a refused push to the run's own branch, then another answer:** the first answer to an ask on `main` is refused
    at its push, and a second such answer follows. Each time:
    - the kept commit's command names `answers/<date>-<code>`, never `main`;
    - the second answer is cut from the default branch's tip, or from the last commit pushed to that branch, and no
      pushed commit has the kept one in its ancestry;
    - a second run does not bring the first ask;
    - the end reads *signed, not pushed* for the first and *answered, on its way* for the second;
  - **the seat's reasons:** an ask with all three fields shows them; an option whose *because* is empty reads *not
    stated*; an ask with none shows the fallback link and help line;
  - **the reasons' lifetime** (S3's rows, built with S3): an answer to an ask with all three fields, accepted and
    rejected, passes the gate with the fields unchanged; `--clear-ask` moves them under `## Asks`; a field on a
    tracker with no `ask:` is refused;
  - **not brought:** an id two branches propose; an ask answered on a branch not yet merged; an ask before ids; a
    malformed ask. None is brought, and each is named on the first line;
  - **the ways out:** `later` typed, and *decide later* as a reply, accepted only with its code (each: nothing signed,
    the code spent, the next ask, named at the end); `open` (the recorder gets the same path again); an interrupt at the prompt, and between the commit and the push (nothing pushed, no worktree left);
  - **where it runs:** Subversion and a plain folder, refused before anything is read; no terminal; the hooks' copy;
    an author-only identity, refused before any view is written, naming the signing page; a checkout on a seat's
    branch, behind `origin`, or with a change; a hooks' copy that is not the checkout's tool. Each is refused before an
    ask is read;
  - **a text checkout's line endings:** a clean checkout with `core.autocrlf=true` passes the start check, and the
    hooks' copy's record reads `files: equal`. Its control, one changed byte of content in the tool: refused, and
    `files: changed`;
  - **the commits and their links:** with `blob` in GitHub's form and in GitLab's, the head's, the answer's and the
    tool's links are the derived commit URLs. With `blob` empty, there is no link, and each says why. The answer's
    commit after a check that stopped the run has no link (not pushed). A pinned, tagged tool links to `TOOL_PAGE`; an
    untagged one has no link, and says why. A tool run from the working tree is named by the full HEAD, its files
    equal, and links through `blob` only once that commit is on `origin`;
  - **the requirements recorded privately:** their rows, listed with them.
- **The mutants:** each is a patched copy of one function in the imported module, and each must turn at least one row
  red:
  - **one code per run, not per ask:** ask 2's id with ask 1's code passes;
  - **the code not checked:** another run's reply passes;
  - **the letters read from `ask-options:` in its order,** not the view's: A writes the first option;
  - **the proposal written as a bare `accepted`:** the exact-line row turns red;
  - **the commit made when the view is written:** the row for nothing before a pick turns red;
  - **no `verified_as` before the push:** an unverified commit is pushed;
  - **the push forced:** the moved home is overwritten;
  - **the comparison made after the signature:** the signing program is called for the extra file;
  - **the lines not computed again at the reply:** the turned date is signed unasked;
  - **the run going on after a failed check:** a second ask is signed;
  - **the signing precondition skipped:** the author-only row writes a view;
  - **the tool's files compared raw:** the clean CRLF row is refused;
  - **a link derived from `origin`'s URL with `blob` empty:** a link appears;
  - **an unpushed commit linked:** the stopped commit links;
  - **the tool's commit read from the hooks' copy's record alone:** a copy installed from another commit names the
    wrong tool;
  - **a refused push's ask brought again:** a second run brings it while `guided/<ask-id>` exists;
  - **the reasons allowed on an open ask only:** the answered ask with its fields is refused;
  - **the recovery command aimed at the home:** a kept answer to an ask on `main` names `refs/heads/main`;
  - **a kept commit in a later push's ancestry:** the second answer's push carries the first;
  - **a result view opened between asks:** the recorder gets two paths for one ask;
  - **the board reading `origin/answer/` only:** the pushed answer reads *waiting for you* (FM-064).
- **What each backend can claim:**
  - **git:** the commit holds the lines the view showed for the choice; its signature verifies against a key the
    default branch's signers file lists; it is bound to the put ask it answers (FM-050 3b); and it is pushed,
    fast-forward, to its home, counting once that lands on the default branch. It cannot claim who answered the key's
    prompt, or that anyone read the lines (FM-007). A link is the configured forge's address for a commit, not proof
    that the page exists or that anyone can read it;
  - **Subversion and no version control:** nothing. The run refuses there.

### 9. The build

- **What it needs first:** R4 and the ask ids, built (FM-050's build: the answer commit, `--answer <ask-id>`,
  `put_ask`, `answer_commit` and C5's reading); FM-058's fix, with the hooks' copy's record below; R11's link helper
  (FM-057), which the view reuses; FM-053's signed answer for G5, G6 and G7; and S3's record fields (A32). Without
  FM-053's answer, the help line stands above the window and the diff carries no tints. FM-064's fix lands on this
  branch, and this build's Reviewer checks it.
- **The prerequisite: the PIN and the hooks' copy record the tool's full commit.** It is critical, and built with
  FM-058, before the view.
  - **Today:** `--vendor` writes an untagged source's commit as ten characters (`:9247`), and `pin_manifest` returns
    no full commit for that form (`:9163–9188`). `install_copy` (`:9602`) writes `COPY` (`:9640–9642`) with the
    installing repository's short HEAD (`:9632`), its branch, and no word of changes.
  - **After it:** `--vendor` writes the source's full commit, tagged or untagged (`untagged <full commit>`, with
    `(dirty)` where it is), a form `MANIFEST_RE` already accepts. A pinned copy's `COPY` records the PIN's full
    commit. A working-tree copy's records HEAD's full commit, and `files: equal` or `files: changed`: whether each
    copied file (`copy_files()`, `:9587`) equals its blob at HEAD, compared canonically, as item 1 compares.
  - **A record written before it keeps its meaning** (R26): a PIN's ten characters or `(no git)`, and a `COPY`'s short
    commit, are read as written and named as incomplete. The next run that meets one names what records it whole
    (`--vendor` again, or `--install-hook`), and `--check` never fails on it alone. A short commit is never expanded
    against the adopter's own history, which does not hold the tool's.
  - **Its rows:** each record, for a tagged source, an untagged one with its full commit, and a working tree; a
    changed file, read as `files: changed`; a clean CRLF checkout, read as `files: equal`; and a PIN and a `COPY`
    recorded before the change, named incomplete and not refused, also where the adopter's history holds a commit
    with the same ten characters.
  - **Its mutants:** the untagged commit cut to ten characters; `files: equal` written without the comparison; the
    comparison made raw; a short commit expanded with `git rev-parse` in the adopter's repository. Each turns a row
    red.
- **Tier: critical,** for signing and rights. A critical Builder, a Reviewer in a session of its own, and CI on the
  pull request.
- **One branch** (`fm/059-guided-answer`). Each code commit carries its own rows:
  1. **`answer_lines`,** lifted from `answer_cmd`'s write; the choices' order and their normalisation, lifted from the
     dialog (`act`, `:3711`, `:3722–3726`) into one place that the board and the view share; the two *touch* strings.
     The board and `--answer` write what they wrote before;
  2. **`--guided`'s start and its reading:** the checks, the fetch, the refs, the asks and their homes, and the first
     line. Here the run stops before any view: a stopping point a run sheet can use alone;
  3. **the view:** `render_guided`, its script, its labels in English (German after the native read) and the opener;
     the commits in the header, linked through R11's helper; *before this*; the seat's reasons and their fallback; the
     prompt, the code and the reply's checks; *decide later*, `later` and `open`;
  4. **the signing:** the worktree, the prepared commit and its comparison, `git commit-tree -S`, the five checks
     after it, the push, a refused push's kept branch, the run's own branch, the result view with its TOOL row, and the
     end. The browser is the
     run's one new process start: a new entry in
     `test_vcs_launch_ceiling.json`, with its hash in `test_vcs_skeleton.py` (`:129`);
  5. **`test_guided_answer.py`'s mutants,** and its wiring into `test_shoalmark.py`;
  6. **FM-064's fix:** the board reads an answer the run pushes (FM-064);
  7. **docs:** the README's row, `docs/signing.md` and `docs/index.md` with their German pages, the run sheet's answer
     step, the command's help, G6's one sentence after the Owner's signed answer, and the CHANGELOG.
- **The size, a guess at 70 % confidence: M–L.** About 520 lines join `shoalmark.py` (the reading 120, the view and its
  script 180, the commits and their links 40, the reply 60, the prepared commit, the signing and the push 120), and
  about 30 change. About 680 lines join the class test. The commits are an S addition on R11's helper; without that
  helper, the view would need its own, and the addition would be M. The PIN's and the hooks' copy's records are about
  40 lines and 80 of rows, in FM-058's build.

### Open questions, for the Reviewer and the Owner

1. **A checkout that is behind `origin`.**
   - **Proposed:** the run refuses, and names `git pull --ff-only`.
   - **The alternative:** the run fast-forwards the checkout itself, when the checkout has no change.
   - **The Owner's position, 17 October: as proposed.** The run refuses, with one line that gives the command to run.
     Round 2 settled that nothing is written to the checkout before a pick (RV-3332). A fast-forward would break that,
     and need review again.
2. **The answer to an ask the default branch holds.**
   - **Proposed:** one branch of the run's own, `answers/<date>-<code>`: one pull request per sitting.
   - **The alternative:** a push to the default branch itself, refused wherever the default branch is protected.
   - **The Owner's position, 17 October: as proposed,** with FM-064: the board must read the run's branch (item 4).
3. **A refused push.**
   - **Proposed:** the run ends.
   - **The alternative:** the ask is left, as `later` leaves it, and the run goes on to asks on other branches.
   - **The Owner's position, 19 October: the alternative, but not as `later`.** The run goes on to the next ask. Its
     end names the ask as signed and not pushed, with its branch and the one command that pushes it, and no run brings
     that ask again while that branch exists (item 4).
4. **Subversion.**
   - **Proposed:** refused in this build.
   - **The alternative:** a run there, committing under the server login, with the go-to-market seat's Subversion
     words. It needs an answer command on Subversion, which R4 does not build.
   - **Outside the Owner's check of 17 October,** which was the view's: the proposal stands for the ruling.
5. **The lines changed during the wait** (a turned date, or an action's `due:` read from typed words).
   - **Proposed:** the Owner types `yes` under the new lines.
   - **The alternative:** the run writes a new view, with a new code.
   - **The Owner's position, 17 October: as proposed.**
6. **`INDEX.md` in the signed commit.**
   - **Proposed:** the view names it and does not show its lines; the terminal prints them before the key, and the
     prepared commit may change no other path.
   - **The alternative:** the view shows its changed rows too, as the hook will write them.
   - **The Owner's position, 17 October: as proposed.**
7. **A hooks' copy taken from another commit, with equal files.**
   - **Proposed:** the TOOL row names the run's tool commit, and says that the hooks ran the same files, installed from
     the commit the copy records.
   - **The alternative:** the run refuses unless the copy's recorded commit is the run's own.
   - **Outside the Owner's check of 17 October:** the proposal stands for the ruling.

## Done when

- Its design is reviewed, and the Owner's signed answer here names the release that builds it.
- Built in that release, and reviewed.

## Asks

**2026-10-17** · Do you adopt the guided answer design and its seven proposals as FM-059's body states them in the commit that last filed this ask?
**withdrawn** — no answer was given; the design is amended first, on the Owner's positions of 17 and 19 October

**2026-10-16** · Which release builds the dedicated answer view: the Board view that holds only one ask's dialog, opened by a prepared run that signs what you chose?
**withdrawn** — no answer was given

**2026-10-16** · Which release builds the guided answer view: the Board view that holds only one ask's dialog, opened by a prepared run that signs what you chose?
**answered** — accepted - v0.20.1 · holgo99
**relation** — accepted the proposal
**signed** — 99b1708 · G

## Ship log

| Date | Event |
|---|---|
| 2026-10-16 | Filed on the Owner's direction (relayed by the Auditor), with its ask. Nothing is designed or built. |
| 2026-10-16 | Its design started, the Owner with the Designer; the ask now asks only which release builds it. |
| 2026-10-16 | Quick win 11 in v0.20.1, on the Owner's word: the first proposal withdrawn, the ask filed again proposing v0.20.1. |
| 2026-10-16 | Designed by the Builder seat (`27f31560/builder-16`): `## The design`, the guided run, its view, the pasted reply, the signing and the push, the ways out, the words as drafts, the class test and the build, with six open questions. The release ask stays as filed; the design's own ask is drafted for the Planner. Records only. |
| 2026-10-16 | The commits, linked, added to the design on the Owner's word (relayed by the Auditor), by the Builder seat: the ask's head, the answer's commit and the tool's, in the header and a TOOL row, through R11's link helper (FM-057); the hooks' copy records the tool's commit first, built with FM-058; a seventh open question. Records only. |
| 2026-10-16 | The Owner's rulings on the commits folded in (relayed by the Auditor), by the Builder seat: the view names the tool's commit and links the commits as ruled; a release's commit links to the public repository, and a working-tree tool's commit links as the repository's commits do, only if pushed. Records only. |
| 2026-10-16 | RV-3328 and RV-3333 (recorded privately) fixed in the design, by the Builder seat. Records only. |
| 2026-10-16 | RV-3329 to RV-3332 fixed in the design, by the Builder seat: the tool's files compared with each CRLF read as LF; the PIN and the hooks' copy record full commits, and older records are named incomplete (R26); an author-only identity is refused before any view; the fetch's metadata is named as the one write before a pick, and the class row's baseline is taken after it. Records only. |
| 2026-10-17 | Main joined (`6336355`), and the release ask's exchange recorded under `## Asks`: accepted - v0.20.1, signed `99b1708`. By the Planner seat. Records only. |
| 2026-10-17 | Its design's own ruling ask put, by the Planner seat, as the Builder seat drafted it: whether the Owner adopts the design and its seven proposals. Records only. |
| 2026-10-19 | The design amended by the Planner seat, on the Owner's positions of 17 October (through the Designer) and of 19 October on open question 3 (through the Auditor): *decide later* in the view, the view's read-at words, no result between asks, the seat's reasons with their fallback and the record's new fields, one verb. FM-064 filed. The ask withdrawn until a records re-check. Records only. |
