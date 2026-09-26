# Changelog

What a repository takes on when it vendors again. Newest first; `--vendor` prints the sections that are new to it.

## Unreleased — 0.18.5

- **The tool ships two themes as starters, `monochrome` and `shoalmark`** (FM-002, slice B; the Owner's signed answer of
  2026-09-26, `4e00f85`, PR 90). **What a vendoring repository receives:** `brand/themes/` in its copy — each theme a
  `theme.css` with the three IBM Plex Mono cuts it loads (Latin-1, `@ibm/plex-mono` 1.1.0, their SIL OFL) and a README
  listing them by sha256 — pinned like the rest. **Nothing changes until it chooses:** no board reads `brand/themes/`,
  and a board with no theme looks byte for byte as it did. `--brand DIR --from monochrome|shoalmark` copies a theme's
  files into a brand place, never over a file there; an unknown name is refused with the two; `--from` alone is refused.
  `--schema` says no key chooses the look; `--brand` marks a place that holds no brand file. Each theme is FM-006's mock
  as he took it (`9467b83`), every edit marked in the file. **Three hooks in the board** a theme styles, none seen
  without one: the Owner's box's title, a label (`owner.title`, `#p>.pt`, wherever the box is drawn); the last line's
  one element, `<footer id="F">` — the claim `#f`, now outside the board `#B`, and the running line `#r`; the class
  `zebra` on every other row of a group. *On upgrade:* a theme that placed the running line by the board's sibling (`#B
  … ~ #r`) or reached the claim through `#B` reaches both through `#F` now. The German board names the Owner *Eigner*
  throughout.
- **shoalmark's own board and site wear the `shoalmark` theme** (FM-002, slice A; the Owner's signed answer of
  2026-09-26, `4e00f85`, PR 90: *the tool ships monochrome and shoalmark as starters; shoalmark's own board and site
  wear the shoalmark theme*). This repository's brand layer only — `work-tracker/brand/theme.css`, two IBM Plex Mono
  cuts beside the Regular, `docs/stylesheets/shoalmark.css`. No `shoalmark.py` change and nothing new that `--vendor`
  copies: a consumer's board looks as it did. The site is built at the release tag and goes live when the repository
  is public. The starters for every consumer are slice B.
- **The site's start page is the landing page** (FM-006, slice L; the Owner's word in chat of 2026-09-26 10:25:41, not a
  signed answer: *for the v0.18.5 release we also add a landing page requirement, alongside the restyle and rebrand of
  shoalmark's brand identity*). The GtM/Design mock as it is — an arcade's attract screen over a pixel chart of the German
  Wadden coast whose wrecks are this repository's defects — through `overrides/landing.html`, which `docs/index.md`
  selects; every other page keeps the site's chrome. Documentation only: no `shoalmark.py` change, nothing new that
  `--vendor` copies. The site is built at the release tag and goes live when the repository is public.

## 0.18.4 — 2026-09-26

**What the Owner owes has a time and a button, only he changes his intent and his current path, and the three CI failures
of the v0.18.3 tag are fixed** (FM-030, FM-037, FM-035 — with FM-036, FM-029, FM-031 and FM-006).

- **Only the Owner changes his intent and his current path** (FM-037, the Auditor seat's AU-12; the Owner's word of
  2026-09-25 18:55:33 on its line *stop a seat from editing your TRIAGE.md*: *let's fix this first then* — the
  attribution as AU-13 corrected it in the tracker's ship log). (1) `--check` walks the
  branch's own commits, merges included, and refuses one that changes what a pass reads as his — the text under
  `## The intent` or `## The current path`, byte for byte, whitespace counted, each commit under its own
  `shoalmark.toml`: a heading renamed or removed, `TRIAGE.md` deleted or moved away, `tracker_dir` re-pointed — unless it
  is his signed commit: `%G?` G, the signer principal the author's email, the author the seat holding `answer` in the
  default branch's `[seats]`; a merge only for a text no parent had. A move of the whole tracker with its key, the text
  unchanged, is no change (`ae1f05e`; the reading is in the README, §5). (2) The refusal, exit 4, names the commit, its
  subject and the section, and the way through: he commits it signed; a seat proposes it as an `ask:`. The commit-msg
  hook refuses a seat's such commit before it is made — it sees the author, and says `--check` on the branch judges the
  signature. (3) `## Passes` stays open to seats; the scaffold `--init` writes is accepted. (4) `--queue` reads such a
  pull request `wait: TRIAGE.md changed unsigned`. (5) Where his seat is not `signed` it proves the author only and says
  so; Subversion is out of scope, in one line. (6) The refusal's last line, and `docs/signing.md`: a commit signed with
  his key passes; at tier 0 any process on his account holds that key (FM-007). (7) A synthetic test for each, and one
  that walks this repository's main to 0d60d55: the six signed commits `45198d5` … `ad9bf67` accepted, `ae1f05e` no
  change. The Auditor seat's AU-19: every signature — this guard's, the answer gate's, `--queue`'s — is verified against
  the default branch's copy of the signers file `gpg.ssh.allowedSignersFile` names, never a branch's own, and a change
  to that file (or `<tracker dir>/allowed_signers`) is refused unless it is his signed commit: a branch could vouch for
  itself. AU-20: a scaffold of any version the readers know is accepted where there was none. *On upgrade:* where the
  default branch's `[seats]` names the Owner, a seat's change to his two sections or his signers file fails `--check`;
  with no seat holding `answer` there, `--check` says it is not guarded; a first signers file lands on the default
  branch by his own hand.
- **`--answer` verifies as the gate does; no signers file on the default branch verifies nothing** (FM-037, the cold
  re-review's R1 and R2 on `b0d863e`). R1: `--answer`'s own check before it pushes read the clone's signers file, so mid
  key rotation — his new key only on his branch's copy — it said *pushed*, and `--check` then refused the answer and
  told him to sign a commit he had signed. It now asks `verified_as`, the gate's test against the default branch's file,
  and pushes nothing that fails it; and neither it nor the gate says *sign it* to an SSH-signed commit whose key that
  file does not hold for the identity: each names the file, and that a new key verifies once his signed commit to it is
  merged. R2: where `gpg.ssh.allowedSignersFile` names a file in a checkout and the default branch does not carry it,
  nothing verifies against it — the checkout's copy is whatever branch is checked out, and a checkout on a branch that
  writes one let `--queue` read another pull request's change, signed with that branch's key, as clean. Every SSH-signed
  commit then reads *`<file>` is not on <default branch>: commit its first version there, signed*. *On upgrade: where
  the signers file sits in the repository and its default branch does not carry it yet, no SSH signature verifies until
  it does.*
- **An act owed to the Owner has a time** (FM-030; his line 6: *what the Owner owes is on their board with one button*).
  New front-matter keys: `due:` — an ISO time with its zone, `2026-09-26T07:30:00+02:00`, written by the seat that
  schedules the act (with the action ask, or when its time is set); `window:` — minutes after it in which the act can
  still be done, 60 where absent; `done:` — its result, written by the Owner's `--done`. `--clear-ask` leaves `due:`:
  the answer to an action ask is a promise, and the act is still owed. The gate refuses a time that is not a real one
  or has no zone. *Nothing to do on upgrade.*
- **The acts owed to the Owner are on his board with their time** (FM-030). An act is owed where an action ask was
  accepted — his answer a promise of his hands — or a `due:` is set, until `done:` is written; closed work owes none.
  His board lists them after the questions, under *your acts, with their time*: *no date yet*, *due*, *overdue* after
  its time, *missed* once `window:` minutes have passed with no result — by the page's clock, its second rule beside
  the triage freshness. INDEX.md lists them in a table with their time as written: no due, overdue or missed, so no
  minute passing changes a committed file. The board has six new labels, `acts.*`; `examples/de/labels.yaml` carries
  the German.
- **Done and Reschedule on each act, as copied commands** (FM-030). Two buttons on the act's row open a small dialog —
  where the result is, or the new time — and OK gives one command on the answer's second screen, titled *Sign your act*:
  `--done <id> "<where the result is>"` writes `done:` (the time, and where the result is), hands an action's move
  back to the seat (`next: build`), and records the act under a new `## Acts` section; the act leaves his list.
  Only where his accepted action answer left `next: owner` does `--done` move it: a `due:` beside a question he has not
  answered keeps `next: owner`, and the question stays on his list (the pass's R1).
  `--due <id> <time>` writes the new `due:` and records the old one there, newest last; on a done act it is a new act.
  Both are the Owner's own change, made as `--answer` makes his answer — `answer/<id>`, signed where his seat is
  `signed`, pushed, undone on failure — and refused from a seat without the `answer` right. The dialog's time is the
  browser's, sent with its zone. An unmerged `answer/<id>` is never cleared over his commits: where the act is open on
  it, the refusal names the command on that branch; otherwise merge it first; `git branch -D` is named only where
  nothing of his is on it — for `--answer` too, so RV-479's check changed with it: it had expected `git branch -D`
  over his own unmerged answer. `[headings]` gains `acts` (German `Handlungen`); eight new labels. *Nothing to do on
  upgrade.*
- **An invite and a notification per act** (FM-030; the Owner's word of 2026-09-25 13:33:29: *Better than only invites
  would be invites + notifications*). `--invite <id>` writes `<tracker dir>/evidence/<id>/<id>-act.ics`, RFC 5545 as the
  standup's invite is: the act's `due:` in UTC, a DURATION of its `window:`, an alarm 30 minutes before, CRLF, folded at
  75 octets, the same bytes for the same act; its SEQUENCE counts the act's records, so the file written after a `--due`
  replaces the event. `--notify` posts one system notification per act due within 30 minutes, overdue or missed —
  `osascript`, `notify-send`, PowerShell's toast, else a printed line — once per act per state, remembered in
  `$XDG_STATE_HOME/shoalmark/notified.json` (`~/.local/state/shoalmark/`, `%LOCALAPPDATA%\shoalmark\` on Windows), never
  in the repository; a notice that could not be posted is tried again. The README has a cron and a launchd line; the
  tool installs nothing. *Nothing to do on upgrade; schedule `--notify` if you want it.*
- **`--standup` and `--owner` list the acts** (FM-030's first line: *`--standup` lists due and overdue acts, not
  just asks*). After the asks, *ACTS — yours, with their time*: missed and overdue first, then what falls due, soonest
  first, then what has no date yet — an accepted action with no `due:`, such as FM-007's hardware key, promised after
  the scoring — each with its `due:`, what it is and the promise it came from, in the board's words. With no question
  and acts owed, neither says nothing needs him: `--owner` leads with *NO QUESTION FOR THE OWNER · N ACT(S) OWED*, and
  the standup's head counts the acts. *Nothing to do on upgrade.*
- **A sheet's newest row wins** (FM-036). Two filled rows for one tracker on one sheet — a same-day re-judgement,
  the raise rule's normal case — were both applied in order, so on 2026-09-25 FM-030's rank read 1, then 3, then 1,
  each run printing *Applied 1*. `apply_worksheet` now applies the LAST filled row in the file; the earlier is left
  as it is, the record of the first judgement, claims no rank, and each run names it: *superseded on this sheet by
  the later row*. The second run applies nothing. `--triage` prints the rule, *ONE TRACKER, TWO ROWS*. *Nothing to do
  on upgrade; a seat that struck the earlier row may leave it in from now on.*
- **The record names the answer's signing commit** (FM-029; the Auditor seat's AU-29). `--clear-ask`'s record
  under `## Asks` gains `**signed** — <sha> · <G|N|U>`: the commit that wrote the `answer:` line and what git says of
  its signature where the record is written (`%G?` — G good, U good from a key not trusted here, N none). An answer
  not yet committed says `not committed · N`; under Subversion there is no line. The key's tier is not printed yet
  (FM-007). *Nothing to do on upgrade; records written before keep what they have.*
- **The pass's R3–R8 on FM-030's build** (FM-030; the Reviewer's passes on `52cfcc7` and `647da17`). R3: `--done` where
  the act is on an unmerged `answer/<id>` names that branch and his commits on it, as `--due` does, instead of *owes the
  Owner no act*. R4: the dialogs' copied command single-quotes what he typed — `--answer <id> accept '<text>'`, `--done
  <id> '<where>'`, a `'` written `'\''` — so a backtick or a `$` in it is inert; in `"…"` a shell ran and expanded them
  into what he signs. R5: an hour of 24 is refused in `due:` and `done:` on every Python; 3.14 read `T24:00` as the next
  midnight and 3.9 refused it, so the gate's word depended on the interpreter. R6: `--notify` exits 1 when a notice
  could not be posted and says *nothing remembered* when nothing is; the README's cron line names Linux's session bus
  for `notify-send` and keeps its output in a log, and the launchd plist keeps its output too. R7: that cron line starts
  with `mkdir -p "$HOME/.local/state/shoalmark" &&` — the shell opens the log before the tool runs, and on a fresh home
  its folder did not exist, so `--notify` never ran; a suite case runs the line as cron does, with an empty home, and
  without its `mkdir -p`, where it fails (the cold review's R2). R8: `due:` and `done:` bound a zone's minutes to
  00–59 — `fromisoformat` read `+05:99` as `+06:39` on both Pythons, and the gate passed it.
- **`--queue` reads a head that is the verdict commit itself** (FM-031; seen in the parent project on the pinned 0.18.3,
  2026-09-25 18:25:56). PR 851's head was the Reviewer's verdict (`Reviewed:` its parent, READY), its file
  `evidence/PD-400/review-….md`; the project's review gate read the head as covered — *1 commit past the reviewed tip,
  all the verdict's own review files* — and `--queue` said *wait: no verdict*: it counted review addenda only under
  `evidence/reviews/`. Both fixes: the verdict commit's own `review*.md` counts wherever it sits under
  `<tracker dir>/evidence/`, as the gate reads it; and the review folder is `[paths] reviews` in `shoalmark.toml`
  (`evidence/reviews/` by default, a glob such as `evidence/*/` allowed), for the addenda after a verdict. *Nothing to
  do on upgrade; a repository that files reviews beside each tracker's evidence may set `reviews = "evidence/*/"`.*
- **`--queue` reads an answer branch by its answer commit, not its head** (FM-031; seen in the parent project's pinned
  queue at 21:24:12 on 2026-09-25 and its PR 855 cold review, RV-573, 00:44 on 2026-09-26). An answer branch whose head
  is the Reviewer's docs-pass commit on the answer read *wait: not an answerer (reviewer@seat)* — its PRs 836, 849 and
  853. An `answer/*` pull request is now read by the newest commit of its own that changed an `answer:` line, where every
  commit past it touches review files only — the review folder, `sessions.md`, a `review*.md` anywhere under
  `<tracker dir>/evidence/` — and the line names that commit, `signed <sha>`; anything else past it, and the head is
  read, as before. Built in 0.18.4. *Nothing to do on upgrade.*
- **macOS: a browser check that hangs fails; one that cannot run here is skipped by name** (FM-035, the v0.18.3 tag's
  CI on macos-latest 3.12). What is known: the log shows the suite dying at `subprocess.TimeoutExpired`, 60 s into the
  answer dialog's check, on the page where OK opens the second screen — which copies the command at once. What is
  inferred: the pasteboard is the one unstubbed call on that path; the check now stubs it, as the second screen's own
  checks did. The hang itself was not reproduced here. Every headless Chrome run now goes through one helper: Chrome
  absent or unable to start — its control run on a blank page failing — skips the block by name, with the reason and
  its number of checks; Chrome present and a page not returning within 60 s, twice, FAILS the check and the suite
  exits 1. The run always ends with `skipped here: N checks`, zero or not, and says a run with skips is not a full
  pass. A test-only change. *Open, for the release after* (the CI fix's review, R3): the pre-commit hook runs each suite
  with its output to `/dev/null`, so on a run that exits 0 a skipped block's name and *this is NOT a full pass* are not
  shown locally; CI prints the suites whole.
- **Windows: a brand SVG's line ends are counted as committed** (FM-035, the v0.18.3 tag's CI on windows-latest 3.9 and
  3.12). The size cap counted `wordmark.svg` and `logo.svg` as the checkout wrote them: a Windows checkout
  (`core.autocrlf`) writes `\r\n`, one byte more per line, and a file near the cap was refused there and shown
  everywhere else. An SVG is now read, counted and inlined with `\r\n` as `\n`; a PNG as it is.
- **Windows: the suite reads git's output as UTF-8** (FM-035, the v0.18.3 tag's CI on windows-latest 3.9 and 3.12). The
  RV-479 check read `git show`'s blob in the locale's encoding — cp1252 on Windows — and the em dash in the ship-log
  row it compares came out as three other characters. The tool names UTF-8 on every read; the test now does too. No
  change to the tool.
- **`--queue` also prints the last day's merged and closed pull requests** (FM-030, widened; the Auditor seat, through
  the Owner, 2026-09-25 18:25:16). After the queue, *MERGED OR CLOSED IN THE LAST 24 HOURS*: each pull request `gh pr list
  --state merged` and `--state closed` return with a merge or close time in the last day, newest first, with its time in
  UTC and its branch — so a seat's *still open* line is checked against the forge in the same turn. *Nothing to do on
  upgrade.*
- **The setup pages clone the release they ship with** (FM-006; the cold review's R1 on the 0.18.4 cut). `docs/setup.md`
  and its German page cloned `--branch v0.17.8` and called it the newest tag; the site built from them said the same.
  Both now clone `v0.18.4`, and a suite case fails when a `--branch v…` in either page is not `v<VERSION>`, or a page
  has none — a cut changes them with `VERSION`. The site is built from them at the tag. *Nothing to do on upgrade.*

*Named for 0.18.4 and not in it* — each stays a line on its tracker: FM-033's `--queue` and board marks on a pushed branch
whose commits name an unjudged tracker, and the board's activity beside judgement (named in the 0.18.3 section); FM-028's
`--triage --day`, with the INDEX's `Generated` date, and its verdict-commit date line — after midnight the pre-commit
hook writes INDEX.md's new date into a verdict commit and the parent's review gate flags it (*0.18.4 or the release
after*, filed 00:47:31 on 2026-09-26, PR 84); FM-030's move after an answer following the picked option, and
`--answer`'s commit subject cut between words; FM-031's own answer branches pushed without a pull request, in `--queue`;
FM-029's real-history relation case for FM-032's record; FM-007's link to the signing page (`…/signing/`, which the built
site serves as `signing.html`) and the key's tier in what the tool says; FM-006's local site rebuilt after every pull, and
`docs.yml`'s first line.

*On upgrade:* new front-matter keys `due:`, `window:` and `done:`, and one optional configuration key, `[paths] reviews`;
`--notify` runs only where you schedule it. Where the default branch's `[seats]` names the Owner, a seat's change to his
two sections or his signers file now fails `--check`; where the signers file sits in the repository, it verifies
from the default branch's copy, and from nothing until that copy exists.

## 0.18.3 — 2026-09-24

**Every reading prints the relation, an answer writes the next move, and no build commit comes before a judgement**
(FM-029, FM-030, FM-031, FM-033, FM-034 — the Auditor seat's checks on v0.18.2).

- **A record `--clear-ask` wrote before 0.18.1 prints its relation too** (FM-029; the Auditor seat's check 9). Such a
  record has no `**relation** —` line, and `--answered` read it as *relation not computable* — FM-031's and FM-032's
  among them. The commit that wrote the answer still holds `ask-proposal:` and `ask-options:`. A record is matched to
  it by its answer AND its question: a commit whose diff adds that `answer:` line, read back, whose `ask:` is the
  question on the record's `**<date>** · <question>` line — its lines then go through the reader a live answer goes
  through. Where one text answered two questions, each record gets its own commit; where no commit, or more than one,
  holds both — one question answered twice word for word, as FM-007's was on 09-22 — *relation not computable*, never
  a guess. `--answered`'s acted-on lines and the board's tracker view print it and name that commit — *accepted with a
  change, read from the answer's commit `7c97c5b`* — the view under every such record, an older one's too when a newer
  record follows it, and the file is not touched. Where no commit in the checkout wrote
  that answer (a hand-written record, a shallow clone), *relation not computable*, as before. It costs one `git log` for
  all such records and one `git show` for each one found, spent where the relation is printed, never on a load.
- **An answer writes the next move** (FM-030; the Auditor seat's check 24). `--answer` wrote the three lines and left
  `next: owner` — the Owner's move after his move was made. It now writes `next:` in the same commit: `build` for a
  ruling, a determination or a ceremony, the seat's move (`run` stays for something built that waits for its run);
  `next: owner` kept for an action, whose yes is a promise of his own hands, not the act. `revoke` and `--supersede` key
  on the answer being there, so they work after the move is written. `--schema` says what an answer writes, and that an
  ask whose yes needs the Owner's hands is `action`, whatever else it decides; the board's second screen names the move.
- **A fresh clone's `--check` no longer says the INDEX is stale** (FM-034; the Auditor seat's check 20). A finding that
  is the checkout's, not the ledger's — a signed commit this clone cannot verify (no `gpg.ssh.allowedSignersFile`, a key
  not in the keyring), a pinned file this checkout has not got — was written into the generated INDEX's header, so the
  INDEX a clone generated differed from the committed one by that line and `--check` said *STALE* beside the finding.
  It is now said on stderr only, once per cause — `checkout: it is signed, but this clone cannot verify: … — N signed
  commit(s) it could not check: …`, each commit counted and named once — and the run still fails; the drift test is not widened. In every clone the
  committed INDEX and the one it generates are the same under `drift_normalize` — the `Generated` date aside, which a
  clone generating it on another day writes anew — and `--check` reads them so.
- **The 0.18.0 bullet on revoke and supersede names its authority** (FM-031; the Auditor seat's check 14): the Owner's
  word of 2026-09-24 that revoking or changing a given answer needs a path the person can choose, and his signed
  revocation of the cap (PR 46, `7c97c5b`) in FM-031's ship log.
- **A raise naming a signed rule re-judges the tracker the same day** (FM-033, the Owner's second answer; the Auditor
  seat's AU-16). A raise is one line under a tracker's `## Raised` (`raised` in `[headings]`):
  `- <date> · <who> · <fact> · <source> · undermines: <what>`, read by its date and its `undermines:` token. Dated after
  the tracker's `triaged:` and naming a line of the current path (`path 5`) or a tracker's signed answer (`FM-033's
  answer`), it makes an open tracker owed a pass: under *triage* on the board and in INDEX.md, and on the next worksheet
  however fresh its judgement, marked RAISED with the raise in its Now cell. Any other raise waits for the next pass. A
  day decides: a raise written after the same day's pass is re-judged by the seat's own re-run that day, as this
  evening's was. `--triage` prints the rule in the Owner's words.
- **No build commit before a judgement** (FM-033; the Auditor seat's check 26). With `judged_before_build = true` in
  `shoalmark.toml` — off by default, on in this repository — a commit that changes a path outside the tracker directory
  names a tracker, the ids in its subject or else its branch `<kind>/<NNN>-…`, that at the commit's parent carries
  `triaged:`, is not Parked and is `In Progress`; a commit that names none is refused too. At commit time the
  commit-msg hook (`--commit-msg`, which `--install-hook` writes; with lefthook, a `commit-msg` entry) judges the commit
  being made once its message exists — its subject's ids, else its branch, as the history is judged — and refuses it
  before it is made, with the line `--check` prints of it. It reads the message before git's cleanup, so it judges every
  subject git could keep: the first line left once comment lines are stripped (`core.commentChar`) — none left is
  *names no tracker* — and, where git keeps comment lines (`-m`, `--cleanup=verbatim`), the literal first line too, so
  `-m '# FM-007: …'` is judged as FM-007's. `--check` judges each commit of the branch since `origin`'s default branch —
  a merge by the commits it carries, never as the merger's own change — and says in one line whether the gate is on.
  **The commit hook is best-effort. The gate is `--check` on the branch, and it must be green on the pull request's
  head before merge. A bypass of the hook alone, which `--check` catches, is P3** (the Principal's ruling: git's
  `--no-verify` skips any hook by design). On the default branch nothing is judged; on a detached HEAD the subject must name the
  tracker. Judged at their own parents, the four builds of FM-033's table and the fifth are each refused. What FM-033
  also names — `--queue` and the board marking a pushed branch whose commits name an unjudged tracker, and the board
  showing activity beside judgement — is 0.18.4. *To turn it on: `judged_before_build = true`, then `--install-hook`
  again for the `commit-msg` hook (or add the `commit-msg` entry to your own hook runner, §6); build on a branch
  `<kind>/<NNN>-…` whose tracker a pass has kept In Progress, and name the tracker in the subject.*
- **The suite runs `--queue` itself on a branch pushed without a pull request** (FM-031; the Auditor seat's check 8):
  `gh` stubbed, `origin` a local bare repository, it reads `branch <name> @ <sha>  wait: no pull request — no verdict
  on <sha>` and the count. A check, not a change.
- **The tool's rule 4** (FM-033; the Auditor seat's AU-7 and AU-21): `--triage`'s printed rules and README §4 read *the
  pass is the seat's judgement, dated by its commit; the Owner lands it by merging; a row he disagrees with is re-made by
  the seat on his word, or ruled by his signed answer — a merge rules nothing: an answer is written and signed, and a
  merge is not one*. They said the Owner rules by merging and can strike any row.

*Nothing to do on upgrade: one new configuration key, `judged_before_build`, off by default.*

## 0.18.2 — 2026-09-24

**A fourth brand file, `wordmark.svg`: the mark and the name drawn as one** (FM-006), for a brand whose name is part
of its mark.

- **Where a place has `wordmark.svg`, the header shows it inline**, in place of the logo and the name. The name stays
  the page's `<title>` and is the wordmark's accessible name (`role="img"`, `aria-label`); the logo, where there is
  one, stays the browser tab's; the tagline and the footer stay labels. The later place wins, as for the other files,
  and `--brand` names the place.
- **Inline, it takes the page's ink:** drawn in `currentColor` it follows the theme's `--ink` in light and dark and
  through `◐`, the mark and the name in one colour. It keeps the size its `<svg height>` gives, else the logo's 22 px.
- **Shapes and text only, held to a grammar.** The elements are shapes, text, gradients, masks and a `<use>` of the
  file's own ids; each takes only the attributes its row in the tool names, and each value is read whole, in one pass,
  as that attribute's kind — ASCII; colours as `#hex`, `currentColor`, `none` or a plain name; a paint, mask or clip
  only as `url(#id)` of its own; and numbers written plainly, `-?digits(.digits)?`, one space or one comma between
  two — stricter than SVG itself: no `.5`, no `1e3`, no `+`, no `1-2`, so a minifier's compact output is refused.
  No `style` attribute, no `class`, no handler. The file is UTF-8 without a byte-order mark, with no control character,
  no DOCTYPE or entity; at most 32 deep; every id defined once; every reference — a `<use>`, a mask, a clip, a paint —
  to an id it has, at most 3 deep, never in a cycle, and at most 2,000 elements painted with every reference followed
  (a mask used ten times paints ten times). Anything else — a `<script>`, a `<style>`, an image, a link, a reference
  outside the file, a CSS escape — and the file is not shown, with one warning that says why; the header keeps the
  logo and the name. Over 200,000 bytes, the same, and checking never takes more than a bounded number of steps. What
  an editor adds in its own namespace (Inkscape's, Sketch's) is left out, and every id is prefixed `wm-`, so none
  shadows one of the page's. *Export with presentation attributes, not CSS, and without minifying the numbers.*
- *Nothing to do on upgrade: without `wordmark.svg` the header is as it was.* To draw your own: one `<svg>` with a
  `viewBox`, a `height` in pixels, `fill="currentColor"` (and `stroke="currentColor"` where it strokes); the name as
  paths (outline the text in your editor), or as `<text>` in a font your `theme.css` loads. A pixel mark shown at a
  whole multiple of its grid stays sharp. `--brand DIR`'s starter says the same in a comment.
- **Every page names the tool and the version it runs: `<mark> shoalmark · v0.18.2`** — one small line at the bottom
  left, below the footer, in the muted ink, on the board and in a tracker's view alike: the Pricke at 16 px, the
  smallest size its 16-unit grid stays sharp at, and the name in the mono at 11 px, linking to the tool's repository;
  then the version from the copy's own `VERSION`, linking to that release's page — a vendored copy names the version
  it was vendored at. Both open in a new tab. It is the tool's line, in every repository, brand or none: not a label,
  never translated. *Nothing to do.*

**shoalmark's own board wears the site's brand**, from `work-tracker/brand/`: the Pricke beside the name in IBM Plex
Mono as the wordmark, the site's tab icon as the logo, the site's light and dark palettes, IBM Plex from files beside
the theme, and the German claim as the tagline. It is this repository's place: `--vendor` never copies it.

## 0.18.1 — 2026-09-24

**Every reading names the answer's relation to the proposal; the signed line is unchanged** (FM-029, the Owner's
ruling: the relation only, no new verbs). Under `accepted` the board's dialog and `--answer` write the proposal, another
listed option and changed text alike, and a reader counting how often the Owner took the proposal counted all three.

- **The relation is computed where the answer is read**, from `answer:` against `ask-proposal:` and `ask-options:`,
  with the answer's own normalisation on both sides (trimmed, whitespace runs one space, `"` as `'`): *accepted the
  proposal* · *chose option N: <its first words>* (N its place in `ask-options:`) · *accepted with a change* ·
  *rejected: <reason>* · *revoked: <reason>* · *relation not computable* — an accepted answer with no proposal to
  compare it with, or a word that is none of the three. A hand-written `accepted — <text>` reads as `accepted - <text>`.
- **Where it is printed:** `--answered`, beside each answer and on each acted-on line; the board's tracker view, beside
  the answer; and the record `--clear-ask` writes under `## Asks`, as a `**relation** —` line after `**answered** —`,
  because the proposal and the options leave with the ask. A record written before reads as it is: *relation not
  computable*, never a guess. `--owner` and `--standup` list no answered ask yet, so they print none.
- **The signed line is not touched:** `answer:` and the answer's commit subject still say `accepted - <text>`, and
  `--answer` and the dialog write what they wrote.
- **`--queue`:** an `answer/*` pull request whose head's author may not answer reads `wait: not an answerer
  (<author>)`, signed or not. It read `wait: unsigned answer`, which a signed commit by someone else is not.
  `wait: unsigned answer` and `wait: answer not verified here — <why>` stay for an author who may answer.
- **A half-written answer** left by a failed `--answer` is given again for `revoked - <reason>` too, as
  `--answer <id> revoke "<reason>"`; an answer that replaced a committed one is given again with `--supersede`.

*Nothing to do on upgrade: no key, no hook line and no command changes. The board has six new labels —
`relation.proposal` · `relation.option` · `relation.changed` · `relation.rejected` · `relation.revoked` ·
`relation.unknown` — in English until a `labels.yaml` translates them; `examples/de/labels.yaml` carries the German.*

## 0.18.0 — 2026-09-24

**The session registry is a report, generated from the commit trailers** (FM-032 S2, which is FM-031's S1). It was a
file every seat wrote and the gate read: it conflicted whenever two branches landed, and a row once closed never
re-opened, so every return to a branch cost a new id. The trailer rule stays; the rows go.

- **Delete `<tracker dir>/sessions.md`** (`git rm`); history keeps its rows. Nothing reads or writes it any more:
  `--check` warns in one line while it is there, and passes.
- **`--sessions` is the registry**: one row per `Session:` id in the checkout's history — its seat (the author
  through `[seats]`), its first and last commit, how many commits carry it, its worktree — Markdown on stdout,
  written nowhere.
- **`--session open` and `--session close` are gone**: each prints one line and exits 2. *Drop them from a seat's
  instructions and from any script.* `--session new` stays and prints an id no commit carries.
- **The gate keeps one rule**: a seat's commit — never the Owner's, never an author outside `[seats]` — carries a
  `Session:` of the shape `<8 hex>` or `<8 hex>/<seat>-<n>`, and its seat part is the author's seat. Gone: the open
  row, one worktree per session, the refusal to remove the registry, drop a row or re-open one, and abandoned rows
  (`--check` no longer lists them, `--triage` no longer closes them). As before, a commit whose history carries no
  `Session:` at all is not judged.
- **A `Worktree:` trailer**, the checkout's directory name, is appended beside `Session:` by the same hook; commits
  from before carry none, and the report shows `—`. *The hook lines are unchanged: nothing to install again, nothing
  to change in your own hook runner.*
- **The board's strip and the digest's line** name the sessions with a commit in the last day, with their worktree,
  where they named the open rows. Labels: `sessions.recent` is new; `sessions.open` and `sessions.abandoned` are
  gone, and a `labels.yaml` that still sets them is told they are not labels.

**The queue in one view, the filing freeze, and an answer that can be taken back** (FM-031 S2, FM-032 S4, and two
defects of `--answer` found the same day).

- **`--queue`, the open pull requests in one view** (FM-031 S2): read from GitHub with `gh`, `origin` fetched once,
  ONE action each — `merge` · `closes with PR N` · `close: carried into PR N` · `wait: conflict in <paths>` ·
  `wait: no verdict on <sha>` · `wait: NOT READY (<verdict>)` — what can be acted on first, oldest first, then a
  count. A verdict is a commit carrying `Reviewed: <sha>`, its word read from its subject. Without `gh`, offline or
  with no GitHub `origin`: one line, exit 3. `--owner` and `--standup` end with it where the forge can be read.
  *Nothing to do, as long as each verdict's subject says READY, READY WITH FINDINGS, READY TO TAG or NOT READY.*
- **The filing freeze** (FM-032 S4): `freeze_at` in `shoalmark.toml` — at that many open trackers or more, `--new`
  refuses a filing without `tags: bug`, exit 4; `--new KIND "title" --tags bug,process` writes `tags:` as it files
  (comma-separated, deduplicated, each from `[tags]`, case aside); `--check` says the freeze holds in one line, its
  exit unchanged; `--schema` lists the key. `freeze_tag` (default `bug`) is the tag that passes it: where your `[tags]`
  does not carry it, the freeze refuses nothing and `--check` says so in one line. `--tags` without `--new`, and
  `--supersede` without `--answer`, are refused in one line, exit 2. *Off (0) until you set it; if your `[tags]` has no
  `bug`, set `freeze_tag` to the tag a product defect carries.*
- **`--answer` after an earlier answer**: a local `answer/<id>` merged into `origin`'s default branch is deleted and
  cut fresh; one not merged is refused, naming `git branch -D answer/<id>`, and nothing unmerged is deleted. After
  the push it goes back to the branch it started on.
- **An answer is revoked or superseded, never overwritten:** `--answer <id> revoke "<reason>"`, or
  `--answer <id> accept|reject "<option>" --supersede`. The answer it replaces moves into the ship log with the
  commit that wrote it, and the board's tracker view shows the answer and *supersedes <sha>*.
  Built on the Owner's word of 2026-09-24 that revoking or changing a given answer needs a path the person can
  choose; FM-031's ship log records his signed revocation of the cap (PR 46, `7c97c5b`), written by hand before
  0.18.0's `--supersede` existed.
- **`--queue` sees what waits beyond the open pull requests.** Each branch on `origin` that no pull request carries —
  not the default branch, not `answer/*`, not already merged, not inside an open pull request or another such
  branch — follows as `branch <name> @ <sha>  wait: no pull request — no verdict on <sha>` · `— verdict <sha> READY …:
  open it` · `— NOT READY (<sha>)` · `— conflict in <paths>`, and the count line adds *n pushed without a pull
  request*. A head your clone's fetch does not cover (a single-branch clone) is fetched by its ref; one that still is
  not there reads `not fetched here` on its own line. An `answer/*` pull request is the Owner's own answer and needs no
  verdict: `merge: your answer` when its head's author may answer — the seat matched as the gate matches it, email or
  name — and the commit verifies; `wait: answer not verified here — <why>` when it is signed and your clone cannot
  check it; `wait: unsigned answer` when not.
- **A signed commit this clone cannot verify is no longer told to sign.** With `gpg.ssh.allowedSignersFile` unset or
  missing, or a GPG key not in the keyring, `--check` says *it is signed, but this clone cannot verify: <why> — see
  the signing page*; an unsigned commit is still asked to sign, and the exit is unchanged. *Nothing to do in a clone
  that verifies today; in a fresh clone, set `gpg.ssh.allowedSignersFile` as the signing page shows.*

## 0.17.8 — 2026-09-23

**A vendoring vouches for what it copies** (FM-011). `--vendor` used to skip a missing source file, pin what it found
and report success — from a lone `shoalmark.py` it wrote a PIN of one line and left your old `VERSION` in place.

- **An incomplete source is refused**, exit 4, naming the missing files — nothing is written. `--partial` copies it
  anyway and names the missing files in the PIN.
- **A source that is no release is refused**: it must be a git checkout whose HEAD is exactly at `v<VERSION>`, with a
  clean tree; the refusal names the HEAD and the changed paths. `--allow-untagged` vendors a working copy anyway, and
  the PIN says `untagged <sha>`. *Vendor from a clean clone at the release tag — `git clone --branch vX.Y.Z` — as
  README §6 now shows.*
- **The PIN's first line is a manifest**: `# shoalmark <version> · tag <vX.Y.Z> · commit <sha> · vendored <date> ·
  complete|partial`. Your `--check` checks it — the exact form `--vendor` writes, its tag against its version, its
  version against the copy's `VERSION` — then prints one line, *pinned 0.17.8 from tag v0.17.8*, and warns when the
  copy is untagged or partial. A line in any other form is named in a warning and the copy called *unverified*. A PIN
  without the line (from 0.17.7 or older) says *no manifest — pinned before 0.17.8* and verifies as before.
- The message on success names the tag, and still prints the sections new to your copy.

## 0.17.7 — 2026-09-23

- **A consumer's secret-shape gate read the trailer query as a credential** and refused the vendored `shoalmark.py`:
  the tool asked git to filter trailers by key, a `<name>=<value>` shape in the source. It now reads git's plain
  trailer block and picks `Session:` and `Reviewed:` in Python — the same values, in the same order.
- Nothing to do: no setting, label or command changed.

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
