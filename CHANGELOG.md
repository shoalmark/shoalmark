# Changelog

What a repository takes on when it vendors again. Newest first; `--vendor` prints the sections that are new to it.

## 0.17.6 — 2026-09-23

**A seat's commit names its session, and the record knows the session** (FM-024, slice 1). The seat says who may; it
could not say which run — two sessions of one seat are one author in git, and a Reviewer run as a sub-agent of the
author's session looked as independent as any other.

- **`seat.session`, a second per-worktree setting beside the badge.** `git config --worktree seat.session <id>` — the
  harness's session id, its first eight hex characters; `--session new` prints one no row carries. `--init` names
  both settings.
- **The trailer.** `--install-hook` now also writes a `prepare-commit-msg` hook that appends `Session: <id>` to every
  commit made in a worktree with `seat.session` — nothing where it is unset (the Owner's checkout), nothing when the
  message carries one. *A repository with its own hook runner calls `--session-trailer "$1"` from its
  prepare-commit-msg hook; README §6 gives the lefthook line. Run `--install-hook` again to get the hook.*
- **The registry, `<tracker dir>/sessions.md`.** `--session open <id> <seat> "<convened by>" "<scope>" [<worktree>]`
  writes a row and stages it; `--session close <id>` dates its end. A sub-agent's id is `<parent>/<seat>-<n>`:
  when *convened by* carries a session id (eight hex characters, or `<id>/<seat>-<n>`), `--session open` refuses an id
  that does not derive from it — a plain word never names a parent. An id
  is used once; a worktree an open row holds is refused to a second session.
- **The gate, where the registry exists.** A seat's commit — never the Owner's — must carry a `Session:` whose row is
  open and names the author's seat, in a worktree no earlier open row holds; exit 4 otherwise, with one of three
  lines. Judged on the commit being made, the commit at HEAD and every commit a merge brings, each against the
  registry in its own tree. A seat's commit that removes the registry, drops a row or re-opens an ended one is refused
  and judged against its parent's registry: only the Owner removes it. *Nothing changes for your repository until it opens its first session: a tree without
  `sessions.md` is not judged, and neither is any commit made before the file existed.* The pre-commit hook runs the
  session rule on every commit, a tracker staged or not (`--session-check`, cheap: no tracker is read). *With your own
  hook runner, add that line to its pre-commit as well; README §6 has both lines.*
- **Abandoned rows.** An open row with no commit for a day: `--check` lists it, the next `--triage` closes it —
  *closed by the pass of <date>* — and prints it for the pass's paragraph.
- **Verdicts reported, not refused.** A review commit names the tip it judged with `Reviewed: <sha>`. `--check`
  reports each verdict of the last `triage_days` days as *independent*, *same session* (its session root is one of the
  reviewed branch's own commits' — never what the branch merged in from the trunk), *untraced*, or *on trunk* for a
  tip on the trunk's first-parent line. The refusal of a same-session verdict is a later slice, after a week of counts.
- **Seen.** The board's first lines name the open sessions (seat, scope, an abandoned one marked) and count the week's
  verdicts; `--owner` ends with the open sessions by seat. **Labels:** five new — `sessions.open`,
  `sessions.abandoned`, `reviews.week`, `reviews.untraced`, `reviews.trunk` — in English and in `examples/de/labels.yaml`.

## 0.17.5 — 2026-09-23

**One id finds one row, and an empty section says why.** Two things an Owner read as defects on his board, and the
intent he found hard to start.

- **A whole id in the board's search shows that tracker alone.** The search matched each word as a substring of
  about thirty fields of a row, the ids its body links to among them. So an id found its own row **and every row
  that links to it**: `FM-005` showed itself and every row that links to it, on a large board most of the list. A
  query that is exactly one known id (trimmed, any case) now shows that tracker alone, whether or not it is open. A
  partial id (`FM-00`) and a query of several words still match by substring. The full help is the search box's
  tooltip; the placeholder, `search · ~ID`, fits the box at its 200 px minimum. *What links to an id is `~ID`: what its body links to and what links to it, by Markdown link only.
  A story's chapters are the story view. A chapter's `epic:`, a `blocked-by:` or an id in plain text is in neither.*
- **The empty `progress` section says why.** `progress` holds only what a triage pass kept, so until a first pass
  has run it reads 0 beside work in progress. While no tracker carries `triaged:` and `TRIAGE.md` records no pass,
  its line now reads *empty until a first triage pass has run — --triage*. The rule is unchanged. `INDEX.md`,
  `--triage` and the board still agree on what is owed a pass.
- **`--init` gives the intent a way in.** The three lines were bare: `for —` · `so that —` · `never —`. The scaffold
  now opens them with a lead-in: they describe the repository as a whole, what all of it is for, what is true when
  it works, and what no pass or seat may do to get there. Each line carries an example in italics, a whole product
  to overwrite. **The intent a pass prints is what the Owner wrote — only the scaffold's own lead-in and examples
  are left out**, recognised by their exact text, never by italics, bold or length. So an untouched scaffold is no
  intent, one line of his own is that line alone, and an example with one word changed is his. *`--triage` no
  longer prints the template's italic note above your intent. A `TRIAGE.md` you already have is never rewritten;
  README §6 carries the lead-in and the example, and `examples/de/TRIAGE.md` carries them in German.*
- **Labels:** three new labels, `desc.progress.none`, `count.id` (the counter over an id searched alone:
  *1 tracker · <id>*) and `search.help` (the search box's tooltip: the whole help), and `search` shortened to fit
  the box at its 200 px minimum. All in English and in `examples/de/labels.yaml`. *A `labels.yaml` of your own that sets
  `search` keeps its old hint. One without the new labels shows the English words.*

## 0.17.4 — 2026-09-23

**The answer says what it does** — the Owner's one command, and everything around it, met by an Owner on one morning.

- **A load no longer spawns git once per tracker.** `answered-by:` empty or `<you>` is filled from
  `git config user.name` — and the test was *the key is empty*, true of every tracker with no answer at all. On a
  505-tracker corpus that was 504 git processes and 15.2 s of a 16.8 s load; `--answer` pays for a load about four
  times (itself, the checkout hook, the pre-commit gate). The name is now read only where a tracker carries an
  `answer:`, and at most once per run. Measured on the same corpus before and after: **16.4 s → 0.80 s, 504 → 0 calls.**
  Every run that reads the trackers is faster — the gate in your pre-commit hook above all.
- **`--answer` says each step as it starts**, on stderr, flushed: `answering <id> — 1/4 reading the trackers` ·
  `2/4 cutting answer/<id> from <branch>` · `3/4 committing, signed` (your key may ask for a touch; the gate runs) ·
  `4/4 pushing to origin`. Silent until its last line, it was stopped by an Owner who took it for hung. Its last lines
  are unchanged.
- **A failed `--answer` leaves nothing behind.** When the gate refuses the commit — or anything fails after the run has
  written — it restores every tracked path it changed (it begins only on a tree with none), goes back to the branch it
  started on, deletes an `answer/<id>` it cut that carries no commit, and prints what refused it (the hook's own
  output, not git's last line), the answer, and **the command that gives it again**. At 0.17.3 it left the answer
  staged, INDEX.md rewritten and the empty branch checked out, and the next `--answer` refused as a dirty tree.
- **The dirty-tree refusal names the paths.** Where one is a tracker carrying an answer that was never committed — what a
  failed 0.17.3 run left — it says so, prints one command that restores only the tool's leftovers, and the answer to
  give again. *If you have such a leftover from 0.17.3, the refusal tells you what to run.*
- **The board's answer dialog has a second screen.** OK used to disable itself and leave one enabled button, *abort*,
  which read as taking the decision back — and it said *Copied* whether or not anything was. Now OK opens *Sign your
  answer*: the command with *Copy again*, where to run it (the board names the branch it was built from — one
  `git branch --show-current` per board build), what it does in four steps, what success looks like, how to check the
  signature (`git log -1 --format=%G? answer/<id>` prints `G`), the signing page for when it fails — and **Done**, the
  one way out; Esc too. *Copied* appears only when the clipboard said so.
- **Labels:** 22 new — `answer.sign.*` and `answer.done`, in English and in `examples/de/labels.yaml`. **`answer.run` is
  gone** with the line it drove: a `labels.yaml` that sets it is now told it is not a label — delete the line.
  `answer.sign.url` is the signing page the dialog links to; point it at your own if you have one.
- **The seat that acts on an answer can record that it did.** `--clear-ask` drops the three answer lines and writes the
  exchange under `## Asks`; under `[seats]` the gate read any change to those lines as `answer` — the owner's right — and
  refused the principal. A change that removes the lines **and** adds the matching record (same question, answer and
  answered-by) is now the **`ask`** right's move. Removing the answer without its record, or editing its text, is
  still `answer`. *Answers your seat could not clear are still in the front matter: clear them now.*
- **`[seats]` no longer drops a signature `answerers` asked for.** From 0.17.1 `[seats]` alone decides who may answer,
  so `answerers = ["alice signed"]` beside `[seats] owner = "alice"` accepted Alice's unsigned answer and `--answer`
  stopped signing — while the note said `answerers` *still works*. **The gate now refuses that configuration**, naming
  both lines: add `signed` to the seat, or remove `answerers`. Where no seat is spelled like the entry (a name there,
  an email here), every seat holding `answer` stands in for it. `--answer` refuses the same way before it touches
  anything. *A repository with both keys may turn red on vendoring this — that is the point; the fix is one line.*
- **The deprecation note says what is read.** With `[seats]`: `answerers` *is not read for answers here — `[seats]`
  decides … It can be removed.* Without `[seats]`: unchanged, and `answerers` is still removed no sooner than the release
  after 0.17.3.
- **A merge commit is no longer the merger's.** On a clean tree the gate judged HEAD against HEAD~1 — for a merge,
  everything the pull request carried, every answer and close in it attributed to whoever merged. The forge's merge
  identity is no seat and signs with its own key, so `--check` on a trunk went red on every merge that carried a status
  change; shoalmark's own `main` was red this way at 0.17.3. Now a merge is judged by its **own** change — the tracker
  files where it differs from every parent, under the merger — and **each commit it brings** against its own parent,
  under its own author and signature, so a commit made with `--no-verify` or in the forge's editor is still read, and a
  refusal names that commit. The same rule in the pre-commit run of a merge, and when asking whether an answer a merge
  brings in is committed. The brought commits are read only when HEAD is a merge — one `git log`; a merge bringing 20
  commits checks in about 1.6 s. *Merging with a merge commit is what keeps the Owner's signed answers: keep doing it.*
- **Known, not in this release:** an ask the Owner has answered is still offered on the branch he returns to, until the
  merge brings the answer there — and answering it again is refused with advice to delete the branch that carries the
  first answer. Don't. Filed; the way forward is the Owner's to rule, with the rest of the answer flow's shape.

## 0.17.3 — 2026-09-22

- **A consumer one release behind was told nothing had changed.** The version was declared twice — `VERSION`, which
  ships to the copy, and `__version__`, a constant beside it — and 0.17.1 and 0.17.2 moved the file and left the
  constant at `0.17.0`. Both tags shipped that way, so `--version` under-reported on each of them.
- Where that stopped being cosmetic is `--vendor`. It reads `had` from the **consumer's** `VERSION` file and compares
  it against **our constant**: `if had and had != __version__ and changes_since(had)`. A copy pinned at exactly
  0.17.0 satisfied `had == __version__`, so the guard was false and the line that exists to say *what a repository
  takes on by vendoring again* never ran. The copy received 0.17.2's files, was told they were 0.17.0's, and was
  shown neither the `(was …)` clause nor a single changelog section — while the two it was owed were the answer
  gate's correctness fixes. A repository further behind was saved by accident: `had != __version__` held for it, and
  the changelog printed. Being one release behind is what hid it.
- **The version is now the `VERSION` file and nothing else**, read at import. `VERSION` already ships in
  `TOOL_FILES`, so a vendored copy carries it, and the comparison is then between the consumer's file and ours — the
  artifact actually being copied — rather than between a file and a constant that happened to agree with it. Two
  checks pin it: that the version named is the version that lands in the copy, and that the file and `__version__`
  cannot disagree. v0.17.2 is not re-cut; the fix goes forward.
- **The `answerers` deprecation never reached the repositories it was for.** The note was guarded on
  `ANSWERERS and SEATS`, so it spoke only where *both* keys were present — a repository already part-way through the
  migration. One still wholly on `answerers`, which is the entire population the deprecation addresses, heard
  nothing, and the note it never saw was the only thing scheduling the key's removal. Dropping `answerers` on that
  promise would have broken exactly the repositories that were never warned: with no `[seats]`, `may_answer()` falls
  back to `answerers`, so the key's removal refuses every answer and takes `--answer` with it.
- The guard is now `ANSWERERS` alone — any repository carrying the key is told, whether or not it has `[seats]`; one
  on `[seats]` with no `answerers` is still never warned about a key it does not use. **The removal clock restarts:
  `answerers` is removed no sooner than the release after 0.17.3.** That is the first release whose note reaches the
  affected repositories, so the clock starts there — and the note carries the version rather than *"the release after
  this one"*, which prints unchanged in 0.18 and every release after it and would restart the countdown each time it
  was read. Three checks, one per configuration.
- Both were reported by an outside repository vendoring the tool — the first found by reading `--vendor`'s guard, the
  second on the day that repository moved onto `answerers` and noticed the silence. Neither is visible from inside
  this one: it has `[seats]` and no `answerers`, and it is never its own consumer.

## 0.17.2 — 2026-09-22

- **The gate refused an answer as somebody else's unsigned commit — the answerer's own.** Who set a front-matter line
  is read from the version control system, and under git the reader asked `git log -S <key>:`, a **substring** search
  over the whole patch. A tracker's body discusses its own keys: the sentence *"an `answer:` counts only from the
  account it is filed from"* is written into the very tracker that rule governs. The pickaxe found the commit that
  wrote that **sentence** and named its author as the one who filed the answer.
- The second test had the same shape. *"Is this line committed yet?"* was `key not in <the file at HEAD>` — and with
  the sentence in the body at HEAD, a line that was staged and had never been committed read as committed. Together:
  the answer was attributed to the prose commit, and then judged as if that commit were the answer's.
- **The reader anchors to the line.** Git's `-G` runs its regex over each changed line with the `+`/`-` stripped, so
  `^<key>:` matches only a commit that changed the front-matter line itself; `--full-history` stays (0.17.1), and `-m`
  stays out. The committed test is now *"no line at HEAD starts with the key"*. A commit that rewrote the line's text
  still counts — the setter is whoever wrote the line the file carries now.
- **`--answered` had it too.** The commit that cleared an ask was found with `-S "ask:"`, so any later edit of a body
  that mentions `ask:` became *"acted on"* and put a tracker cleared long ago back on today's agenda. Same anchor.
- **The pattern is the same one on every platform.** `-G` compiles a POSIX *extended* regular expression, and git
  carries a different engine depending on where it was built. Escaping the key with Python's `re.escape` would send
  the space in `next: owner` as `\ ` and the hyphens in `kind-of-problem:` as `\-` — and a backslash before an
  ordinary character is *undefined* in ERE: every engine happens to read it as the literal today, none of them
  promises to. `line_regex()` builds the pattern for both readers and escapes only what ERE actually reserves, so git
  is handed exactly `^next: owner`. Two checks pin the command line the tool sends, not the answer it gave on the
  machine the suite ran on.
- `--answered` gets **`--full-history`** as well, for the reason the one reader has it: an ask cleared, re-asked and
  cleared again on a branch merges to a file byte-identical to one the trunk already had, and git's default
  simplification walks past the whole branch.
- Under Subversion nothing changes: `svn blame` was always line-wise. Four checks pin the anchoring, each shown to
  fail when the substring search is put back.

## 0.17.1 — 2026-09-22

- **Two asks the Principal had re-asked were shown to the Owner as *"sent back — not for you"*.** The seat that sets
  a line is read from the version control system, and `line_author` asked git for it with `git log -1 -S` — which runs
  under git's **default history simplification**: a merge TREESAME to its first parent is followed down that parent
  alone, and the branch it merged is never walked.
- Why it bit here: a branch that moves a line away and back — `next: owner` → `review` → `owner` — merges to a file
  byte-identical to the one the trunk already had. Git skipped the branch and answered with the commit *before* it, so
  the gate read the re-asked trackers as authored by a seat that holds no `ask` right, and the queue hid them.
- The one reader now passes **`--full-history`**, which follows every parent of a merge. Not `-m`: that splits a merge
  against each parent, and a line that arrived only through a branch would then match on the merge itself and name the
  merger as the seat that wrote it. Both are pinned by a check. Under Subversion nothing changes — `svn blame` names
  the revision that last touched the line and never simplified anything.
- **A repository that had moved to `[seats]` could not answer at all.** 0.17.0 says `answerers` is the old name for
  the owner seat's `answer` right, but the answer gate and `--answer` still read `answerers` alone: with `[seats]` and
  no `answerers`, every answer was refused as *"an answer, but `answerers` names nobody"* — and `--answer`, the only
  way in, refused before it cut the branch. **Who may answer is now read in one place, `may_answer()`:** with
  `[seats]` it is every seat that holds `answer` (the built-in `owner`, or any name `[rights]` gives it), matched on
  the identity the version control system reports and asked to sign where the seat says `signed`; `answerers` is
  consulted only where there is no `[seats]`, and its deprecation note is unchanged. A `[seats]` table with no
  `answer` right now says *that*, instead of naming a key the repository no longer has.

## 0.17.0 — 2026-09-22

**An ask reaches the Owner only through the gate** — the Owner, on the shadow week's first day: *"without enforcing
this kind of rules my gut feeling tells me that this process will break as soon as we let other CLI agents into the
system."* Everything the ask flow assumed an agent had read in `AGENTS.md` is now held by `lint`, which the pre-commit
hook, `--check` and every board build already run — and by the Owner's queue itself, which lists only what passes:

- **No ask without a recommendation.** `next: owner` wants `ask:`, `ask-kind:`, `ask-since:` and `ask-proposal:`; the
  refusal names the id and every key that is missing. A question with no recommendation moves the decision and none of
  the work.
- **One question.** One `?`, at the end, at most 300 characters. At most five `ask-options:`, 120 characters each, none
  of them twice. **No duplicate question:** an ask whose text matches another open one — lower case, whitespace
  collapsed, trailing punctuation dropped, and *exactly*, never fuzzily — is refused, naming the other id.
- **Draft → review → owner.** An `ask:` with `next: review` is a draft: any seat writes it, it needs no proposal, and
  the Owner never sees it. The Principal rewrites it, orders the options and sets the proposal, the date and
  `next: owner`.
- **The third layer: `owner_queue` lists only asks that pass.** One that got in another way — a merge, `--no-verify`,
  an agent that never ran the gate — is shown apart on the board and in `--owner`/`--standup` as *"N asks sent back —
  not for you"*, with the reason. The Owner never reads a malformed question as a question.
- **`[seats]` and `[rights]`: who is at the keyboard, and what that seat may change.** Four rights, each a front-matter
  transition the gate sees in a diff — `answer` · `ask` · `close` · `triage`; four built-in names — owner, principal,
  reviewer, implementer; any other name says so in `[rights]`, and a fifth right word is refused by name. The identity
  is the version control system's, never the file's: git's author email (with `signed`, the commit must verify under a
  key trusted for it — the answerers' own verifier, not a second one), or on Subversion the account its server
  authenticated, where `signed` is refused as meaningless. Absent `[seats]`, nothing changes. `answerers` keeps working
  as the old name for the owner's `answer` right — a deprecation line in the gate's output, never a refusal; it goes in
  the release after this one.
- **Clearing an ask keeps the record.** A commit that drops an answer without the exchange in the body is refused;
  **`--clear-ask <id> <next move>`** moves it under `## Asks` (date · question · answer · answered-by, newest last),
  clears the lines and sets the move. `--answered` now also reports what a seat acted on since the last standup, by the
  commit that cleared the ask.
- **The bottleneck line.** Past five asks, the board's first line and `--owner` say *"you are the bottleneck — N asks,
  M trackers held up"*. Not a tracker's problem: his.
- **Two things `--answer` could not say:** an `answer/<id>` branch that exists and does not carry the ask is refused
  instead of switched to, and an ask that is not its own front-matter line gets a refusal instead of a traceback.
- The standup's *not said which kind* group is gone — `ask-kind:` is now one of the four lines an ask carries, so such
  an ask never reaches a sitting. `[headings]` gains `asks`, the body section an exchange is moved into.
- **Cost:** the rules that need a version-control call are asked only of what a commit stages (`--check` asks them of
  everything), and with `[seats]` absent they make no call at all.
- **Every git call the tool makes about its own root is now immune to the hook's environment.** Git exports `GIT_DIR`,
  `GIT_WORK_TREE`, `GIT_INDEX_FILE` and `GIT_PREFIX` into a hook and they override `cwd`, so a pre-commit run answered
  for the repository being committed to: *last worked on* read the wrong log, and the suite built its scratch
  repositories inside the wrong repository. `nested_git_env()` existed for this and was used on two calls; it is on all
  of them now.

## 0.16.0 — 2026-09-22

**The answer, redesigned by the Owner** — *"human users reject any friction"*:

- **Two buttons, accept · reject, and a dialog.** It shows the whole ask with its context — the question, the seat's
  proposal, what it holds up, how long — so the Owner can look and abort. *Accept* offers **the ask's options**, one
  radio each, and last **Other:** with a box; *reject* requires the reason and how to reword. OK yields **one command**.
- **`--answer <id> accept|reject ["text"]`** — the Owner's one command: it cuts `answer/<id>` from the branch that
  carries the ask, writes the three lines with his git name, commits **signed**, pushes, and reports. It refuses before
  touching anything when it cannot end in a verified answer: no signing key, a dirty tree, a rejection without a reason,
  an ask that is answered already, an author the environment would impose over `user.name` — and after the commit, a
  signature the gate would refuse is never pushed. A browser cannot sign; the dialog decides, the terminal signs.
- **The answer is ONE front-matter line.** Every run of whitespace in the text collapses to one space: a newline would
  close the line and the fragment after it would be read as the next key. A long answer goes in the body, as before.
- **`ask-options:` · `ask-proposal:`** — an ask offers its choices as one line, `a | b | c`, and the proposal is the one
  the seat **recommends**: it is offered first and marked, and where options are named the gate refuses a recommendation
  that is not one of them. A proposal alone is a list of one. Whatever is picked goes into the command verbatim.
- The board no longer opens a forge editor, needs no forge, and has no `accept with change` button.

## 0.15.1 — 2026-09-22

What the Owner's first real answer found, in order:

- **The pre-commit run refused every first answer** — it checked "is the answer committed?" before the commit
  existed. Now the pre-commit run reports the answer as *pending*; author and signature are verified on the commit,
  by the next run and by `--check`.
- **`answered-by:` need not be typed:** left empty or as `<you>`, it is the committer's `git config user.name`.
- **The board shows how to answer with each row, before any click** — which file, which branch, which commit.
  Any dash after `accepted` / `rejected` is fine; a long answer goes in the body under a heading, one line in front.
- Named, not yet built: `--answer <id> accept|reject [text]` — one command that cuts the answer branch, writes the
  lines, commits signed and pushes. The Owner: *"human users reject any friction."*

## 0.15.0 — 2026-09-22

**An answer counts only from the account that gave it** — the pre-mortem's rule, enforced:

- **`answerers = ["name"]` in `shoalmark.toml`** names who may answer. Empty, nobody may: every answer is refused with
  that message. A seat cannot add itself unseen — the change is in the same diff as anything it would allow.
- **The gate reads who committed the `answer:` line from the version control system**, never from the file: git's
  author, or Subversion's server-authenticated one (`svn blame`). Uncommitted, or committed by someone else: refused.
- **A git author is only a string — `"name signed"` makes the commit prove it.** The commit that carries the answer
  must verify (`%G?` = G, GPG or SSH) *and* the identity the key is trusted for must be the author's email: a good
  signature under a trusted key still says nothing about whose name is on the commit. Name-only entries under git get
  a note that the identity is unverified. Subversion needs no signature: its server already authenticated the commit.
- The configuration reader learned one shape: `key = ["a", "b"]`, strings only.
- The board's answer buttons: GitLab's editor too (`/-/edit/`); with no forge configured, the file name and the commit
  command are shown instead.

## 0.14.0 — 2026-09-22

**The Owner answers an ask in his own commit** — chat is a conversation, git is the record:

- **`answer:` · `answered:` · `answered-by:`** in the ask's tracker, written by the Owner: `accepted`, `accepted — <his
  change>`, or `rejected — <why, and how to reword the ask>`. The commit's author is the proof; the field is the label.
  The gate wants all three lines, and a question to answer. An answered ask leaves his queue.
- **On the board, each stated ask carries three actions — accept · accept with change · reject.** A click copies the
  three lines to the clipboard and opens the file in the forge's editor under the viewer's own login (`blob` names the
  forge; nothing else is needed — no server, no token, and the seat that asked is nowhere in the path).
- **`--answered`** — the seat's side: what the Owner answered and nobody has acted on yet.
- Four labels (`answer.*`); `examples/de/labels.yaml` has them.

## 0.13.0 — 2026-09-21

**What needs the Owner comes first** (FM-005; three outside agents and one real queue agreed on this and on little else):

- **`ask:` · `ask-kind:` · `ask-since:`** — what is asked of the Owner, as one sentence he can answer; its kind
  (`ruling` · `action` — hands only he has · `determination` — evidence could settle it · `ceremony` — a button);
  and since when. With `next: owner`. Optional: nothing that exists turns red.
- **The board's first words are the answer:** *waiting for you: 2 · oldest 3 days · holding up 2 more*, then each
  question — oldest first, with its kind, its age and what it holds up, transitively — above the path and the table.
  An ask never stated is shown as exactly that.
- **`--owner`** — the same as a digest; `--next` ends with it. **The contract asks a session to end its last message
  with it:** a board has to be opened, a message arrives.
- **`--standup`** — humans have office hours, agents have budgets: the agenda of the Owner's one sitting, by kind,
  and inside a kind what frees the most first. **`--standup FILE.ics`** writes the recurring calendar invite
  (weekdays at `standup = "09:00"`, for `standup_minutes`).
- Nine new labels (`waiting.*`, `ask.*`); `examples/de/labels.yaml` has them in German.

## 0.12.1 — 2026-09-21

What three outside agents hit in their first twenty minutes (FM-004):

- **`--next` answers before any pass has run:** open work, work in progress first, whose move each is, and what
  waits for the Owner. A pass adds the order; it is no longer the price of being told anything.
- **`--new KEY-037 "title"` takes a free id of your choosing** — a project that already numbers its work keeps its numbers.
- **`<tracker dir>/TEMPLATE.md`, if there is one, is the template** — a repository's language and sections.
- The contract names the repository's own `[headings] state`; `--init` writes no `.gitignore` outside git;
  `--new` files one tracker and its help says so.
- `examples/de/`: a complete German start — `shoalmark.toml`, `TEMPLATE.md`, `TRIAGE.md`, `labels.yaml`, and a picture of the board.

## 0.12.0 — 2026-09-21

- **Runs on Windows, and with Subversion — proven in CI** on Windows, Linux and macOS (Python 3.9 and 3.12), both
  suites, Subversion installed on each, the board rendered in a browser on each.
- **Subversion:** the root is found by `.svn` too; a pass's *last worked on* comes from one `svn log`; `--init` sets
  `svn:ignore` for the board (no `.gitignore`) and writes a contract that says the true thing — **run the tool before
  `svn commit`**: Subversion's command line has no client-side hook. `--install-hook` sets `tsvn:startcommithook`
  and `tsvn:precommithook`, so **TortoiseSVN** writes `INDEX.md` before its commit dialog lists the files and
  refuses a violation (it asks the user once). For a gate nobody can skip: `--check` from the server's pre-commit hook.
- **Windows:** messages, hooks and the contract say `python`, not `python3`; a cp1252 console no longer crashes a
  run; every written file is UTF-8 with `\n` on every system; `--print-written` prints `\n` and forward slashes (a
  git hook on Windows fed `git add` a name ending in a carriage return); a deriver is run by this interpreter.
- **A PIN survives line-end conversion** (git's `autocrlf`, `svn:eol-style`): hashes are taken over `\n` text.
  Vendor again to get a PIN made this way.

## 0.11.0 — 2026-09-21

- **A repository that is not in English: `[headings]` in `shoalmark.toml`** names the seven sections the tool reads
  and writes — `state`, `why`, `done`, `log` in a tracker; `intent`, `path`, `passes` in `TRIAGE.md`. `--new` and
  `--init` write them; the gate and the triage pass read them. The English names stay understood, so a repository
  can change language a file at a time. They are configuration and not a label because the gate depends on them —
  what the gate says stays a function of the repository alone. **No table, no change.**
- A pass under *Passes* is a paragraph that carries its date (it always was, by the contract) — the template's notes
  are told apart by that, not by their English words.

## 0.10.0 — 2026-09-21

- **The board has a light / dark button**, in the header: `◐ auto` → `light` → `dark`. It switches every theme's
  `@media (prefers-color-scheme: …)` rule on or off by hand, so **a brand needs no change** — provided its dark colours
  sit under that rule, as the starter's do. The choice is kept in the viewer's browser (the board still works where
  storage is refused); printing is always light. Three new labels: `scheme.auto`, `scheme.light`, `scheme.dark`.

## 0.9.0 — 2026-09-21

- **A repository's brand has a folder of its own: `<tracker dir>/brand/`** — the same name the organisation's place
  has (`tools/shoalmark/brand/`). **Move `theme.css`, `logo.svg` / `logo.png` and `labels.yaml` there**: left loose
  beside the trackers they are no longer read, and a warning says so.
- **A path in a `theme.css` is written relative to that file**, as an editor resolves it, and the tool re-bases it onto
  the page — so `url("fonts/mine.woff2")` finds `brand/fonts/mine.woff2`, and an `@import` or a font now works from the
  organisation's and the person's place too. **If your theme imports something, its path changes** (one `../` more,
  from inside `brand/`).

## 0.8.0 — 2026-09-21

- **A board anyone can brand — three optional files, no setting** (README §9). `theme.css` (colours, fonts),
  `logo.svg` or `logo.png` (the header and the browser tab), `labels.yaml` (every word of the board, flat
  `key: value` — a German board is this file). The same names in three places, the later one winning:
  `tools/shoalmark/brand/` (the organisation — `--vendor` copies and pins it), beside the trackers (the repository),
  `~/.config/shoalmark/` (the person). **Only the git-ignored board reads them** — `INDEX.md` and the gate are the same
  whoever runs them.
- `--brand` says which place gave the board its theme, logo and labels; `--brand DIR` writes a commented starter.
- The board shows the repository's `name`, a `tagline` and a `footer` (both labels, both empty by default), and
  prints in the light palette.
- **If you already have a `theme.css`:** it is now its own stylesheet instead of being appended to the tool's, so
  `@import` and `@font-face` work in it — and a theme whose `@import` is missing is left out whole, with a warning,
  because a colour mapped onto a missing variable is invalid, not the default.
- A theme that is hard to read, an oversized logo and a mistyped label are warnings, never failures.

## 0.7.1 — 2026-09-21

Found by an independent review of the first port onto this tool. **If you have a deriver, read the first item.**

- **A deriver no longer sees the environment, and is told things on stdin.** It now receives `mode`
  (`write` · `check` · `board` · `read`) and `flags` — whatever was typed as the new `--derive-flag NAME` on that
  run — and runs with `PATH`, `HOME` and the locale only. A deriver that took an override from an environment
  variable let a stray `export` in the committing shell rewrite derived cells and stage them, exit 0. **Move any
  such switch to `flags`.** `mode: board` is how a deriver knows it may stand a guard down: nothing that run
  produces can be committed.
- A deriver that does not answer within 60 s is refused; it used to hang the gate for as long as it liked.
- **A vendored copy whose `PIN` was deleted is refused.** It used to pass, silently, with its integrity check off.
  Messages about the pin name a repository-relative path.
- `--help` names the command the repository teaches (`SHOALMARK_CMD`). The write log says how many trackers are
  `In Progress` and how many files the deriver generated.
- Two behaviours the hook contract rests on have checks again: `--print-written` still names its paths under a lint
  while exiting 4; `--check --print-written` writes and prints nothing.

## 0.7.0 — 2026-09-21

- **Licensed under `Apache-2.0 OR MIT`, at your option.** It was *proprietary, no licence chosen*. `LICENSE-APACHE`,
  `LICENSE-MIT` and `NOTICE` ship in the vendored copy, pinned like the rest. A repository that vendors shoalmark may
  use, change and redistribute it under either licence; a copy edited in place still refuses itself — that is the
  tool's own integrity check, not a licence term: re-vendor, or write a new `PIN`.
- `--next` prints the links in the current path as their labels.

## 0.6.1 — 2026-09-21

- **Fixed: `epic <ID>` and `merge <ID>` verdicts were refused in a repository whose ids are not `FEAT-`/`BUG-`.** One
  pattern in the verdict parser still named that pair; it reads the configured prefixes now. Found by checking the
  README's verdict table against the tool.
- **`README.md` is written for the agent that uses the tool, and ships in the vendored copy** (pinned like the rest):
  start · file · stop · triage · what to do when the gate refuses · install · the deriver's JSON · working on the tool.

## 0.6.0 — 2026-09-21

- **The tool is called `shoalmark`** — it was `fathom-mark` until here. The file is `shoalmark.py`, the configuration
  `shoalmark.toml`, the vendored directory `tools/shoalmark/`, the environment variable `SHOALMARK_CMD`.
  **To move a repository:** vendor into `tools/shoalmark/`, delete `tools/fathom-mark/`, rename `fathom-mark.toml` to
  `shoalmark.toml`, run `--init` and `--install-hook` — a contract block and hooks written under the old name are
  recognised and replaced, never left stranded. Tracker ids do not change: an id never does.

## 0.5.0 — 2026-09-21

What the exploration of the first real port forced — each item answers a measured difference
(`docs/work-tracker/evidence/FM-001/port-rd.md`). All of it is the deriver's output or a convention; no setting.

- **One model, two renderings.** `_index` and `_board` say which derived values `INDEX.md` prints and which the board
  shows — default: all. Every derived value stays a view, a fact and a search word on the board.
- **A value may be a pair, `[value, display]`.** The value groups, sorts, searches and is what `INDEX.md` prints; the
  display form is for the board's cells (`→ 0.16.x`, `0.16.4 ✓`).
- **`_notes`** — paragraphs for `INDEX.md`'s header. **`_needs`** (per tracker) — what open work still needs, shown
  with the core's own marks on the ranked table and the board.
- **A group header on the board sums its rows up by the board's columns.**
- **`theme.css` beside the trackers** is appended to the page's style — a repository's own palette and fonts.
- **`FATHOM_MARK_CMD`** — a repository that wraps the tool is named by its own command in every message.

## 0.4.0 — 2026-09-21

- **One seam, by convention — a deriver.** If `<tracker dir>/derive` exists and is executable, the core runs it first,
  on every run: every tracker's id, status, file and front matter go in as JSON on stdin; JSON comes back on stdout.
  `{"<ID>": {"Column": "value"}}` adds columns to `INDEX.md` and the board, and each is also a view on the board ·
  `_keys` adds front-matter keys to the schema gate (never redefines one) · `_problems` are counted with the core's ·
  `_files: {path: text}` are other generated files — the deriver has no side effects; the core writes them, lists them
  under `--print-written` and counts them as drift under `--check`. A non-zero exit — a crash included — **refuses the
  run before anything is written**. Nothing derived is stored, so nothing derived can be stale. No setting.
- **A repository without a deriver pays nothing**: same `INDEX.md`, byte for byte.
- Proven before it was merged, against a 501-tracker corpus: `docs/work-tracker/evidence/FM-001/seam-bprime-rd.md`.

## 0.3.0 — 2026-09-21

- **Runs on Python 3.9** — the Python that ships with macOS. The configuration is read without `tomllib`; the
  subset is what `--init` writes (`[table]`, `key = "text"`, numbers, `true`/`false`, comments).
- **`--init` writes the agent contract** into `AGENTS.md`, between markers it owns (your text outside them is
  kept), and a three-line `CLAUDE.md` router if there is none. Run `--init` again after vendoring to refresh it.
- **`--next`** — the cold-start question: the ranked work in order, each with its next move and what is true now.
- **`--install-hook`** — plain git hooks; no hook runner needed. A hook that is not fathom-mark's is left alone.
- **`--vendor` refuses to overwrite a copy that was edited in place**, and prints what changed since the
  version it replaces.
- `--related` skips German stop words. The triage rules say *harm to people who use it today* where they said
  *harm in production*. The board's palette is neutral.

## 0.2.1 — 2026-09-21

- An unfilled `TRIAGE.md` is no longer printed as if it were a path. An INDEX row shows the hook without its
  quotation marks. A filename's slug ends on a word, is capped at 60 characters and transliterates umlauts.
  `--related` reads words in any alphabet. A tracker's own id in its own heading no longer links to itself.

## 0.2.0 — 2026-09-21

- **One id space per repository, keyed by the project** (`--init --key MSR` → `MSR-001`). `--new "title"` needs
  no prefix where there is one. `bug` joins the tag vocabulary. Branch names may carry ids of any length.

## 0.1.0 — 2026-09-21

- The core: a front-matter schema and its gate, a filing looks first, the triage pass, the read-only board.
