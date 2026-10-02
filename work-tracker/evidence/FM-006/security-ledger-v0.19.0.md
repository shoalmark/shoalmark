# v0.19.0 — the security ledger

FM-006, *The release bar* (the Owner's rulings filed there: *Evidence before the tag*, *The tests*, *Order*). One row per security claim in the
CHANGELOG, the README and the notes, each naming its test, an executed check, or *cut*; for each security test the CI jobs it ran on, and where it
skipped and why; each negative control, run once. Built by the Planner; checked by reviewer-80 and the Auditor. No attack steps: a test is named by
what it asserts.

- **The CI run it reads:** https://github.com/shoalmark/shoalmark/actions/runs/37009286728 — `workflow_dispatch`, dispatched by the Owner on draft pull request #146, on `26bcd9706279004f3bcb495693f943aa2e146964`. Five suite jobs —
  ubuntu 3.9, ubuntu 3.12, macOS 3.12, windows 3.9, windows 3.12 — each running `test_core.py` and `test_shoalmark.py`: green on all five, no check failed,
  and each suite ends *all green*. `test_core.py`: 158 ok on each. `test_shoalmark.py`: 861 ok on ubuntu and macOS, with 3 skipped in 1 block
  (the browser checks: `SHOALMARK_REGENERATE=1` is not set); 852 ok on Windows.
  Windows: 10 skipped in 6 blocks; 3 more not run on Windows, as on main.
- **The runs before it:** https://github.com/shoalmark/shoalmark/actions/runs/36998106048 on `90abab9` was red on both Windows jobs, and FM-006's *Windows round* answered it;
  https://github.com/shoalmark/shoalmark/actions/runs/37005430667 on `d443cf5` was green on all five; then RV-2318, test only (`26bcd97`), and this run.
- **Every commit after `26bcd97` is evidence or notes only** — this ledger's own commit carries one notes change the Owner ruled with it: `CHANGELOG.md:45` narrowed to *(the running tool's own files aside)*.
- **The negative controls:** run once, 2026-10-02 14:14–14:47 CEST, in a worktree at `d443cf5` — each check alone, with `work-tracker/evidence/FM-006/run-one-check.py`,
  whose suite at `d443cf5` differs from the head's only in rows 114–115's check (`26bcd97`, RV-2318); row 114's control ran again at the head, `26bcd97`.
  Each runs against the tool as it was before its fix (the commands are the tests' record's). The checkout and merge hooks' controls run against v0.18.6.
  A control that *FAILS* is the result wanted: the check catches what the fix fixed.
- **The report's findings:** each fixed here carries its tests below; its two remaining findings are 0.19.1's first work, in the private advisory
  set only.

## 1. The claims

| # | where | the claim | its evidence |
|---|---|---|---|
| C1 | CHANGELOG.md:42; README.md:244–245 | Every hook `--install-hook` writes runs a copy of the tool kept in the git directory, never the tool a branch brings. | T1, T17–T19, T30–T34, T51–T52, T75; the texts: T53, T56, T57 |
| C2 | CHANGELOG.md:42; README.md:249–250 | No hook runs the repository's deriver; where there is one, the commit's hook leaves INDEX.md and the derived files as staged, with one line. | T41–T43, X1 |
| C3 | CHANGELOG.md:42; README.md:250–251 | `--install-hook` refuses a hooks folder inside the working tree — a `core.hooksPath` there, or a symlink into it — and writes no hook and no copy. | T44–T48 |
| C4 | README.md:245–247 | The checkout, merge and rewrite hooks run the copy's `--html-only`: it reads the tree, writes the board, and starts nothing but read-only git. | T5–T10, T14–T16, T17, T20–T24 |
| C5 | README.md:247–248 | A commit's hook writes only inside the repository, outside its git directory, and through no symlink. | T35–T37 |
| C6 | README.md:248–249 | A commit's hook fails closed: where the copy is missing, refuses, or runs past 35 s, the commit is refused with one line naming `SHOALMARK_BOARD_SECONDS`. | T38–T40 |
| C7 | README.md:251–252 | Only `--install-hook` writes the copy — from a pinned copy that passes its PIN, else the working tree's tool — and it says which commit and branch. | T25–T28, T22, T36 |
| C8 | README.md:252–253 | Where the tree's tool differs from the copy, a hook judges with the copy and says so in one line. | T21, T33–T34 |
| C9 | README.md:256–257 | A cherry-pick, a revert, `git am`, `reset --hard` and `stash pop` run no hook that writes the board; on Subversion nothing refreshes it. | T55 (the text); T51's `git am` case |
| C10 | README.md:425–450 | A hook runner's entries run the copy; where the copy is missing each entry fails and the runner refuses the commit; a runner reads its configuration from the tree. | T58 (the entries, as the installed hooks invoke the copy); E5 (a missing file: `python3 -I` exits 2) |
| C11 | CHANGELOG.md:43; README.md:342 | A `signed` identity is an email address; it verifies by SSH only, the signature read from the commit itself, good under the default branch's signers file, its principal equal to the email exactly — never a principal that contains it, never the author standing in. | T60–T61, T69–T73; E1 (the history replay) |
| C12 | CHANGELOG.md:43; README.md:342, :188 | A `signed` identity that is not an email is refused when the configuration is read, exit 1, in one line with the way to migrate. | T66–T67; must stay accepted: T68 |
| C13 | CHANGELOG.md:43; README.md:342, :187 | A GPG or X.509 signature on a signed line is refused with `sign with SSH; GPG returns with a fingerprint binding`. | GPG: T62–T65. X.509: E4 |
| C14 | CHANGELOG.md:17–19; README.md:342 | Top-level `owner` and `[seats] owner` that differ are refused at configuration, and so is an `owner` key inside another table. | X24, X25 |
| C15 | CHANGELOG.md:63–66; README.md:382 | An identity listed under two seats, or twice under one, is refused at configuration. | X26, X27 |
| C16 | CHANGELOG.md:28 | A session label that is another seat's own name, or that two seats claim, passes for none. | X28 |
| C17 | CHANGELOG.md:89–99; README.md:415 | `--whoami` reads only top-level fields of the harness's log and only a one-word value, so a transcript cannot add a trailer; two logs for one id are refused. | X29, X30 |
| C18 | CHANGELOG.md:36 | The pre-commit run judges the commit being made — `git commit -a`, `git commit <path>` — and every file name as it is, a name git quotes included. | X8–X12 |
| C19 | CHANGELOG.md:30–33 | A move to `Shipped` is refused unless its ship log names a commit in the change's history that changes a path outside the records. | X2–X7 |
| C20 | CHANGELOG.md:33; ADOPT.md:23; ADOPT.de.md:23 | On Subversion the history is read from the server: where it cannot be read, the gate refuses and says why — never passes unread. | X13–X23 |
| C21 | CHANGELOG.md:54–57 | Fork pull requests wait for the Owner's reading: a fork's own READY, its verdicts and its contents cannot recommend, promote or close; a same-repository pull request reads as with no fork open. | X56–X63 |
| C22 | README.md:342–345 | A merge is judged by what it changes itself, and every commit it brings against its own parent; a clean merge never launders a commit made without the hook. | X31, X32; T51 (a merge brings nothing that runs) |
| C23 | README.md:358–360 | On Subversion `signed` is refused. | X33, X34 |
| C24 | README.md:205–230 | The TRIAGE.md guard: a change to the intent or the current path is refused, exit 4, unless it is the Owner's signed commit, judged by the default branch's configuration and signers file; the signers file is kept the same way; the commit-msg hook refuses a seat's such commit before it is made; Subversion is out of scope. | X35–X46; E1 (the guard's history walk) |
| C25 | README.md:272–279 | `--vendor` refuses a source that is not the whole tool or no release, and a target copy edited in place; the consumer's `--check` checks the PIN's manifest. | X47–X52; this build: T109–T110 (`--vendor` reads only what it copies), T114–T115 (the gate reads only what the PIN names inside the copy) |
| C26 | README.md:536–541 | A deriver's non-zero exit, crash or silence past its bound refuses the run before anything is written; a deriver never reads the environment. | X53–X55 |
| C27 | README.md:309 | The board is generated and git-ignored — the read-only board. | T5, T14 |
| C28 | ADOPT.md:76–79; ADOPT.de.md:75–78 | The way back: remove what calls the copy, then the copy; deleting the copy first means commits are refused. | T59 (the text); T39 (a missing copy refuses the commit) |
| C29 | ADOPT.md:32–34; ADOPT.de.md:33–35 | Check what you run: the SHA-256 of `shoalmark.py` at the tag. | E6 — the notes' checksum, set last, after the cold review |
| C30 | CHANGELOG.md:138 | Security reporting is provided. | E7 (`SECURITY.md` at the head) |
| C31 | README.md:180–186 | `--queue` reads an answer branch as a wait where its answer is by someone who may not answer, where a seat's commit or an unverified commit in the Owner's name lies below it, where the base is not fetched, and where this clone cannot verify the signature. | X64–X68 |
| C32 | CHANGELOG.md:44 | Everything the board renders from a tracker or the configuration is escaped for its place, and a link or an image is http(s), mailto or relative; a `blob` that is not an http(s) URL makes no forge link, and the run says so. | T2–T4; T17's case 4 |
| C33 | CHANGELOG.md:45 | Every run reads and writes a file of the tree — a tracker, the configuration, a theme, the board — only as a regular file inside the repository, never through a symlink (the running tool's own files aside); such a file is refused in one line, exit 4, and the board's refresh leaves it and names it. | reading: T76–T82, T88, T122–T124, T127–T128; writing: T89–T90, T93–T100, T107–T108; the board's run: T11–T16; a deriver that is a symlink, and a folder named `derive`: T91–T92, T101–T102 |
| C34 | CHANGELOG.md:45 | A destination a person names (`--vendor`, `--brand`, `--standup FILE.ics`) is judged where it resolves. | T118–T120 |
| C35 | CHANGELOG.md:45 | A vendored copy's PIN is read only for the copy's own files. | T109–T110, T114–T115 |
| C36 | CHANGELOG.md:45 | `--triage` runs no git in a submodule path outside the repository. | T116–T117 (with T125) |
| C37 | CHANGELOG.md:45 | `--install-hook` refuses, writing nothing, where git reads a setting, or an include's target, from a file inside a working tree. | T83–T87, T103–T106, T111–T113 |
| C38 | README.md:339–341, :179; CHANGELOG.md:75–79 | Four rights — `answer`, `ask`, `close`, `triage` — and no others; a change that needs a right its seat does not hold is refused, naming the seat and the right. The built-in seats hold theirs — `planner` ask, close and triage, `reviewer` triage, `builder` none — and any other name holds what `[rights]` gives it; a repository's own `planner` gains ask, close and triage on upgrade, and `[rights] planner = []` keeps it as it was. | X69–X73; the built-in seats' rights and `[rights] planner = []`: E11 |
| C39 | README.md:303, :178 | Who may answer: the Owner and any seat `[rights]` gives `answer`; without `owner` and `[seats]`, the old `answerers` list, and with nobody named nobody answers. Where `answerers` asks for a signature that the seat answering for it lacks, the configuration is refused, naming both lines. | X74–X77 |
| C40 | README.md:568–569 | A script inside a logo's SVG cannot run; a wordmark is drawn inline only within a fixed grammar, and anything else refuses it whole, with a warning. | X78, X79 |
| C41 | README.md:40; ADOPT.md:11–12, :23–24; ADOPT.de.md:11–12, :23–24 | No dependency beyond Python's standard library, and no network of its own: online, the tool reaches the repository's host through git, through gh for the pull-request queue, and through svn in a Subversion working copy. | E9 |
| C42 | README.md:369–372 | Per seat, one GitHub App owned by the organisation, with no permissions, its webhook inactive, no private key and no client secret: nothing can act through it. | E10 |

Every security fix of this build is claimed by one of these lines; none rests on a test alone.

## 2. The tests

### 2a. This build's security tests — the tests' record, rows 1–120

A row that is itself a control runs the old tool inside the suite. *Ran on* counts the job's `ok` lines for the check's name; a check built from a
table counts one per case.

| # | the check (its name in the suite, cut) | fix | CI: ran on | negative control |
|---|---|---|---|---|
| T1 | `--install-hook` replaces the `post-checkout` and `post-merge` an older copy wrote — they ran the working tree's  | df57a47 — the trusted copy and its checkout and merge hooks | all five | FAILS beside `v0.18.6` |
| T2 | a tracker's text — its title, its hook, the Markdown of its body — and the configuration's name and `blob` reach  | 186fd5e — everything rendered from a tracker is escaped | all five | FAILS beside `186fd5e~1` |
| T3 | the page's own code refuses what it must: a link or an image of a kind other than http(s), mailto or a relative p | 186fd5e — everything rendered from a tracker is escaped | all five | FAILS beside `186fd5e~1` |
| T4 | rendered, a tracker's Markdown makes no script and no unsafe link: its tags stand as text (no element carries `o | 186fd5e — everything rendered from a tracker is escaped | all five | FAILS beside `186fd5e~1` |
| T5 | the board's run writes the board and nothing else: its page and its `view/<ID>.js`, inside the tracker folder, a | 434d8fc — the read-only board run | all five | must stay accepted — a property, no control: the board's run wrote the board and nothing else before 434d8fc too — it passes there |
| T6 | `--html-only` stands alone, with `--root`: another run named beside it is refused, one line, exit 2, nothing writ | 434d8fc — the read-only board run | all five | FAILS beside `434d8fc~1` |
| T7 | the board's run starts read-only git and nothing else: the calls it makes pass, and `fetch`, `gh`, `svn`, a write | 434d8fc — the read-only board run | all five | cannot run beside `434d8fc~1`: its block stops with an AttributeError before the check — that tool has nothing of what it tests (the feature is new with the fix) |
| T8 | the tripwire holds the run where Python does the thing: `svn`, `gh`, `git fetch`, a shell, a write that is no bo | 434d8fc — the read-only board run | all five | cannot run beside `434d8fc~1`: its block stops with an AttributeError before the check — that tool has nothing of what it tests (the feature is new with the fix) |
| T9 | the tripwire, armed in a process that has not used `tempfile`, lets the signers' temporary file be made and remov | 434d8fc — the read-only board run | all five | FAILS beside `434d8fc~1` |
| T10 | in a Subversion working copy the board's run starts no `svn`: with a seat to check and an ask to place, it writes | 434d8fc — the read-only board run | all five | FAILS beside `434d8fc~1` |
| T11 | the board's run reads no symlink: a tracker, the Owner's page, a theme, the labels, a wordmark and a triage works | 434d8fc — the read-only board run | all five | FAILS beside `434d8fc~1` |
| T12 | the configuration that is a symlink to a file outside the repository is not read — its `name` is not the board's, | 434d8fc — the read-only board run | all five | FAILS beside `434d8fc~1` |
| T13 | the tracker folder must resolve inside the repository: named outside by the configuration, or a symlink to a fold | 434d8fc — the read-only board run | all five | FAILS beside `434d8fc~1` |
| T14 | a page git tracks is not written over, nor its views: the files stay as committed, the tree is clean, one line sa | 434d8fc — the read-only board run | all five | FAILS beside `434d8fc~1` |
| T15 | a page that is a symlink is not written through: the file it points to outside the repository is untouched, the v | 434d8fc — the read-only board run | all five | FAILS beside `434d8fc~1` |
| T16 | `view/` that is a symlink to a folder outside is not written into: nothing appears there, the page is written and | 434d8fc — the read-only board run | all five | FAILS beside `434d8fc~1` |
| T17 | case {…}: {…} — checked out, left, and merged with the copy's hooks in place, it runs nothing, writes nothing out | df57a47 — the trusted copy and its checkout and merge hooks | all five (8 cases each) | 8 of 8 cases FAIL beside `v0.18.6` — one per case, against v0.18.6, whose checkout and merge hooks ran the tree's tool |
| T18 | case {…}, the control: with the tool as it was and its own hooks — which run the working tree's tool after a chec | df57a47 — the trusted copy and its checkout and merge hooks | all five (8 cases each) | — (a control: it runs the old tool itself) |
| T19 | case 2, the control with the tool vendored now: the hooks pointed at the working tree's tool instead of the copy  | df57a47 — the trusted copy and its checkout and merge hooks | all five | — (a control: it runs the old tool itself) |
| T20 | a copy that hangs is bounded: a copy whose main thread waits 25 s is stopped by its own bound (2 s here, 35 s by  | df57a47 — the trusted copy and its checkout and merge hooks | all five | no earlier version: the trusted copy came with df57a47, so before it there is no copy to run this against — the feature is new (the copy's own bound) |
| T21 | a version drift: where the repository pins another version than the copy's own, the hook still refreshes the boar | df57a47 — the trusted copy and its checkout and merge hooks | all five | no earlier version: the trusted copy came with df57a47, so before it there is no copy to run this against — the feature is new |
| T22 | a re-run of `--install-hook` replaces the copy — a changed file, a missing marker and a missing theme file are as | df57a47 — the trusted copy and its checkout and merge hooks | all five | no earlier version: the trusted copy came with df57a47, so before it there is no copy to run this against — the feature is new |
| T23 | two worktrees share one copy: the worktree made with the hooks running had its board from it, its git directory i | df57a47 — the trusted copy and its checkout and merge hooks | all five | no earlier version: the trusted copy came with df57a47, so before it there is no copy to run this against — the feature is new |
| T24 | a copy that fails prints one line and the checkout still succeeds — exit 0, on the branch asked for (saw {…}); a  | df57a47 — the trusted copy and its checkout and merge hooks | all five | no earlier version: the trusted copy came with df57a47, so before it there is no copy to run this against — the feature is new |
| T25 | `--install-hook` says which commit and branch it took the copy from; where the default branch cannot be told it s | df57a47 — the trusted copy and its checkout and merge hooks | all five | no earlier version: the trusted copy came with df57a47, so before it there is no copy to run this against — the feature is new |
| T26 | `--install-hook` on a branch that is not the default branch warns, names it and the default branch, and still ins | df57a47 — the trusted copy and its checkout and merge hooks | all five | no earlier version: the trusted copy came with df57a47, so before it there is no copy to run this against — the feature is new |
| T27 | …and on the default branch it says which commit and branch, and warns of nothing | df57a47 — the trusted copy and its checkout and merge hooks | all five | must stay accepted — a property, no control: on the default branch nothing is warned |
| T28 | a pinned copy whose file differs from its PIN is refused: exit 4, the hooks' copy is not written, and no hook — e | 621fabb — every hook runs the copy: none without it | all five | FAILS beside `621fabb~1` |
| T29 | `core.hooksPath` is respected: the checkout and merge hooks are written where it points, outside the repository,  | df57a47 — the trusted copy and its checkout and merge hooks | all five | no earlier version: the trusted copy came with df57a47, so before it there is no copy to run this against — the feature is new |
| T30 | RV-2300 · every hook `--install-hook` writes — `pre-commit`, `prepare-commit-msg`, `commit-msg`, `post-checkout`, | 621fabb — every hook runs the copy | all five | FAILS beside `621fabb~1` |
| T31 | RV-2300 · …the control: beside {…}'s tool the same check FAILS — its commit hooks run the working tree's tool (sa | 621fabb — every hook runs the copy | all five | — (a control: it runs the old tool itself) |
| T32 | RV-2300 · a commit's hooks run the copy, never the tree's tool: a commit that brings a changed tool runs nothing  | 621fabb — every hook runs the copy | all five | FAILS beside `621fabb~1` |
| T33 | RV-2300 · where the tree's tool differs from the copy, each commit hook judges with the copy and says so once: `{ | 621fabb — every hook runs the copy | all five | FAILS beside `621fabb~1` |
| T34 | RV-2300 · …the control: beside {…}'s tool both checks FAIL — its commit hooks run the changed tool (saw marker {… | 621fabb — every hook runs the copy | all five | — (a control: it runs the old tool itself) |
| T35 | RV-2300 · what a commit's hook writes stays inside the repository and never goes through a symlink: INDEX.md comm | 621fabb — every hook runs the copy | all five | FAILS beside `621fabb~1` |
| T36 | RV-2300 · no hook writes the copy: a configuration whose tracker folder is inside the git directory refuses the c | 621fabb — every hook runs the copy | all five | FAILS beside `621fabb~1` |
| T37 | RV-2300 · …the control: beside {…}'s tool both checks FAIL — its commit hook writes through the link (the file be | 621fabb — every hook runs the copy | all five | — (a control: it runs the old tool itself) |
| T38 | RV-2300 · the 35-second bound covers a commit's hooks too, and there it fails closed: a copy whose main thread wa | 621fabb — every hook runs the copy | all five | FAILS beside `621fabb~1` |
| T39 | RV-2300 · a commit's hook whose copy is not in the git directory refuses the commit with one line naming `--insta | 621fabb — every hook runs the copy | all five | FAILS beside `621fabb~1` |
| T40 | RV-2300 · …the control: beside {…}'s tool both checks FAIL — its commit hooks run the tree's tool, so the commit  | 621fabb — every hook runs the copy | all five | — (a control: it runs the old tool itself) |
| T41 | no deriver in hooks · {…}: in a repository with a deriver, no hook starts it, and INDEX.md is left as staged (saw | c17f693 — No deriver in hooks | all five (5 cases each) | 2 of 2 cases FAIL beside `c17f693~1` — the commit and the conflicted merge, against c17f693's parent, whose commit hook ran an accepted deriver: a clean merge, a cherry-pick and a rebase run no `pre-commit`: no hook ever started a deriver there — must stay accepted — a property, no control |
| T42 | no deriver in hooks · …the control: {…} beside {…}'s tool FAILS — its commit hook ran the deriver it had accepted | c17f693 — No deriver in hooks | all five (2 cases each) | — (a control: it runs the old tool itself) |
| T43 | no deriver in hooks · the line a commit's hook says where it starts no deriver names the tool's command and CI's  | c17f693 — No deriver in hooks | all five | the filed line written out (since the literal-lines commit): this check holds the test's own text; row 41's commit case shows the tool prints it — no control of its own |
| T44 | no deriver in hooks · `--install-hook` refuses a `core.hooksPath` inside the working tree, with one line naming t | c17f693 — No deriver in hooks | all five | FAILS beside `c17f693~1` |
| T45 | no deriver in hooks · …and a hooks folder outside the repository that is a symlink into the working tree, resolve | c17f693 — No deriver in hooks | all five | FAILS beside `c17f693~1` |
| T46 | no deriver in hooks · …and {…}: judged against every working tree, refused (saw {…}) | c17f693 — No deriver in hooks | all five (2 cases each) | 2 of 2 cases FAIL beside `c17f693~1` |
| T47 | no deriver in hooks · the default `.git/hooks` is written, and so is a linked worktree's, the common git director | c17f693 — No deriver in hooks | all five | must stay accepted — a property, no control: the default `.git/hooks`, and a linked worktree's, are written |
| T48 | no deriver in hooks · …the control: beside {…}'s tool a `core.hooksPath` inside the working tree is written into  | c17f693 — No deriver in hooks | all five | — (a control: it runs the old tool itself) |
| T49 | no deriver in hooks · the off-main warning names a PIN only where the repository pins one (saw {…} and {…}) | c17f693 — No deriver in hooks | all five | FAILS beside `c17f693~1` |
| T50 | no deriver in hooks · …the control: beside {…}'s tool the unpinned warning names a PIN (saw {…}) | c17f693 — No deriver in hooks | all five | — (a control: it runs the old tool itself) |
| T51 | RV-2300 · {what_}: it brings a changed tool and a changed deriver, and nothing of the tree runs, no hook writes | 1bcb5be — RV-2300's operations; git am and the next commit since 307d6cf | all five (6 cases each) | 6 of 6 cases FAIL beside `79be49d` — one per operation, against 621fabb's parent (79be49d), whose commit hooks ran the tree's tool |
| T52 | RV-2300 · …the control: {…} beside {…}'s tool FAILS — its commit hooks run what the branch brought (saw tool ran  | 621fabb — every hook runs the copy | all five (6 cases each) | — (a control: it runs the old tool itself) |
| T53 | the CHANGELOG's line — every hook `--install-hook` writes runs a copy of the tool kept in the git directory, whic | 8fd049a — the texts, followed since | all five | FAILS beside `8fd049a~1` |
| T54 | the setup pages say the board is rebuilt on every commit, and with git on every checkout and merge — and that on  | 8fd049a — the texts, followed since | all five | FAILS beside `8fd049a~1` |
| T55 | the README's hooks section says in one line what writes no board — a cherry-pick, a revert, `git am`, `reset --ha | 307d6cf — what writes no board | all five | FAILS beside `307d6cf~1` |
| T56 | the README and `--help` name the copy: where it is kept, who writes it, what it runs, and that `--install-hook` i | 8fd049a — the texts, followed since | all five | FAILS beside `8fd049a~1` |
| T57 | RV-2300 · the README's hooks section and `--help` say every hook runs the copy — the commit's hooks too, failing  | fc5f197 — RV-2300's texts | all five | FAILS beside `fc5f197~1` |
| T58 | the README's entries for a repository with its own hook runner run the copy with the installed hooks' invocation, | 8d638de — the hook-runner advice | all five | FAILS beside `8d638de~1` |
| T59 | both notes' way back removes what calls the copy, then the copy in the git directory (RV-2300), and the rest of i | 8fd049a — the texts, followed since | all five | FAILS beside `8fd049a~1` |
| T60 | the signed identity · {…}: the exact principal passes; another trusted signer's key under an author that carries  | 7258d8e — the signed identity | all five (3 cases each) | 3 of 3 cases FAIL beside `7258d8e~1` |
| T61 | the signed identity · …the control: {…} beside {…}'s tool FAILS — it let the author stand in, or took a principal | 7258d8e — the signed identity | all five (3 cases each) | — (a control: it runs the old tool itself) |
| T62 | the signed identity · a commit whose signature header is PGP-armoured, written with git's plumbing, is refused on | 7258d8e — the signed identity | all five | FAILS beside `7258d8e~1` |
| T63 | the signed identity · …the control: beside {…}'s tool the PGP header gets no such line | 7258d8e — the signed identity | all five | — (a control: it runs the old tool itself) |
| T64 | the signed identity · a trusted GPG key whose user ID carries the Owner's email signs the answer: refused with ex | 7258d8e — the signed identity | ran on ubuntu 3.9, ubuntu 3.12, macOS 3.12; skipped on windows 3.9 and windows 3.12: gpg made no key here | FAILS beside `7258d8e~1` |
| T65 | the signed identity · …the control: beside {…}'s tool that GPG-signed answer passes (saw exit {…}) | 7258d8e — the signed identity | ran on ubuntu 3.9, ubuntu 3.12, macOS 3.12; skipped on windows 3.9 and windows 3.12: gpg made no key here | — (a control: it runs the old tool itself) |
| T66 | the signed identity · a name-only `signed` identity under {…} is refused when the configuration is read — exit 1, | 7258d8e — the signed identity | all five (3 cases each) | 3 of 3 cases FAIL beside `7258d8e~1` |
| T67 | the signed identity · …the control: beside {…}'s tool that configuration is read (saw exit {…}) | 7258d8e — the signed identity | all five (3 cases each) | — (a control: it runs the old tool itself) |
| T68 | FM-024 · the signed identity · an identity without `signed` stays as it is, a name included (saw exit {…}) | 7258d8e — the signed identity | all five | must stay accepted — a property, no control: an identity without `signed` stays as it is |
| T69 | the signed identity · `--queue`'s reading of an answer, the board's and `--owner`'s *signed* (`on_their_way`) and | 7258d8e — the signed identity | all five | FAILS beside `7258d8e~1` |
| T70 | the signed identity · `--owner` shows only the exact principal's answer as signed | 7258d8e — the signed identity | all five | FAILS beside `7258d8e~1` |
| T71 | the signed identity · …the control: beside {…}'s tool those readings take the others too (saw {…}, {…}, {…}) | 7258d8e — the signed identity | all five | — (a control: it runs the old tool itself) |
| T72 | the signed identity · `--answer` committed under the Owner's email as its name with another trusted signer's key: | 7258d8e — the signed identity | all five | FAILS beside `7258d8e~1` |
| T73 | the signed identity · …the control: beside {…}'s tool that answer is pushed (saw exit {…}) | 7258d8e — the signed identity | all five | — (a control: it runs the old tool itself) |
| T74 | the signed identity · the texts: README §Seats and its `answerers` and refusal rows, both signing pages (SSH only | 7258d8e — the signed identity | all five | FAILS beside `7258d8e~1` |
| T75 | an act with the copy's hooks installed finishes, and the hook's run ends: `--answer` switches branches with the c | df57a47 — the trusted copy: an act with its hooks installed ends (the hang) | all five | must stay accepted — a property, no control: an act with the copy's hooks installed ends — the copy came with df57a47, so no earlier version has it |
| T76 | the reading rule · a commit's hook meets a tracker that is a symlink: the commit is refused in one line naming it,… | 9c69638 — the reading rule | all five | FAILS beside `1b65331` |
| T77 | the reading rule · `--check` by hand meets it: refused in one line naming it, exit 4 | 9c69638 — the reading rule | all five | FAILS beside `1b65331` |
| T78 | the reading rule · the board's refresh meets it: skipped with its line, the board refreshed without it | 434d8fc — the read-only board run | all five | must stay accepted — a property, no control: the board's refresh skipped it before this round too (434d8fc) |
| T79 | the reading rule · the configuration, and TRIAGE.md in the folder it names, each a symlink: `--check` is refused in… | 9c69638 — the reading rule | all five | FAILS beside `1b65331` |
| T80 | the reading rule · …the control: beside 1b65331's tool the commit's hook check FAILS | 9c69638 — the reading rule | all five | — (a control: it runs the old tool itself) |
| T81 | the reading rule · …the control: beside 1b65331's tool the checks of `--check`, the configuration and TRIAGE.md FAIL | 9c69638 — the reading rule | all five | — (a control: it runs the old tool itself) |
| T82 | the reading rule · with 1b65331's tool the board's refresh skips it as well — a property, no control | 434d8fc — the read-only board run | all five | must stay accepted — a property, no control |
| T83 | the git configuration's files · a value from a configuration file inside the working tree: `--install-hook` refuses… | f1e8368 — the configuration's files | all five | FAILS beside `1b65331` |
| T84 | the git configuration's files · …the control: beside 1b65331's tool this check FAILS | f1e8368 — the configuration's files | all five | — (a control: it runs the old tool itself) |
| T85 | the git configuration's files · a value from a configuration file inside another worktree's tree: `--install-hook`… | f1e8368 — the configuration's files | all five | FAILS beside `1b65331` |
| T86 | the git configuration's files · …the control: beside 1b65331's tool this check FAILS | f1e8368 — the configuration's files | all five | — (a control: it runs the old tool itself) |
| T87 | the git configuration's files · the default configuration is accepted — `.git/config` sits in the git directory | f1e8368 — the configuration's files | all five | must stay accepted — a property, no control |
| T88 | FM-005 · RV-2154 · a tracker that is a symlink is refused in one line naming it, exit 4, by every run but the board… | 9c69638 — the reading rule (RV-2154's check follows it) | ran on ubuntu 3.9, ubuntu 3.12, macOS 3.12; not run on windows 3.9 and windows 3.12, as on main | FAILS beside `1b65331` |
| T89 | the write rule · a run by hand meets an INDEX.md that is a symlink: refused in one line naming it, exit 4, nothing… | 42f69d4 + b1731dc — the write rule | all five | FAILS beside `1b65331` |
| T90 | the write rule · …the control: beside 1b65331's tool this check FAILS | 42f69d4 + b1731dc — the write rule | all five | — (a control: it runs the old tool itself) |
| T91 | a deriver that is a symlink · a run by hand refuses it in one line naming it, exit 4, and starts nothing | ee6c28a — a deriver that is a symlink | all five | FAILS beside `1b65331` |
| T92 | a deriver that is a symlink · …the control: beside 1b65331's tool this check FAILS | ee6c28a — a deriver that is a symlink | all five | — (a control: it runs the old tool itself) |
| T93 | the write rule · `--standup FILE.ics` at a calendar file that is a symlink: refused in one line naming the file, ex… | 6ff2a33 — the calendar files under the write rule (83eb0dc: its folder symlink made as one) | all five | FAILS beside `1b65331` |
| T94 | the write rule · `--invite <id>` where the evidence folder is a symlink: refused in one line naming the file, exit… | 6ff2a33 — the calendar files under the write rule (83eb0dc: its folder symlink made as one) | all five | FAILS beside `1b65331` |
| T95 | the write rule · `--standup FILE.ics` at a calendar file that is a symlink · …the control: beside 1b65331's tool th… | 6ff2a33 — the calendar files under the write rule | all five | — (a control: it runs the old tool itself) |
| T96 | the write rule · `--invite <id>` where the evidence folder is a symlink · …the control: beside 1b65331's tool this… | 6ff2a33 — the calendar files under the write rule | all five | — (a control: it runs the old tool itself) |
| T97 | the write rule · `--brand DIR --from THEME` and `--vendor DIR` into a folder of the tree that is a symlink: each is… | d0bbcb4 — the copies judged before the first is copied (83eb0dc: its folder symlinks made as such) | all five | FAILS beside `1b65331` |
| T98 | the write rule · the copies · …the control: beside 1b65331's tool this check FAILS | d0bbcb4 — the copies judged before the first is copied | all five | — (a control: it runs the old tool itself) |
| T99 | the write rule · `--triage` where the evidence folder is a symlink: refused in one line naming the worksheet, exit… | e889500 — `--triage` asks the rule before its worksheet's folder is made (83eb0dc: its folder symlink made as one) | all five | FAILS beside `1b65331` |
| T100 | the write rule · the triage worksheet · …the control: beside 1b65331's tool this check FAILS | e889500 — `--triage` asks the rule before its worksheet's folder is made | all five | — (a control: it runs the old tool itself) |
| T101 | a folder named `derive` is no deriver: a run by hand goes on, exit 0, and no line names it | e3ef17e — a folder named `derive` | all five | FAILS beside `ee6c28a` |
| T102 | a folder named `derive` · …the control: beside ee6c28a's tool this check FAILS | e3ef17e — a folder named `derive` | all five | — (a control: it runs the old tool itself) |
| T103 | every include setting's target · a conditional include into the tree, its condition not holding: `--install-hook` r… | 6884bc2 — RV-2313, every include setting's target (83eb0dc: paths compared as the tool prints them) | all five | FAILS beside `ee6c28a` |
| T104 | every include setting's target · a conditional include into the tree, its condition not holding · …the control: bes… | 6884bc2 — RV-2313, every include setting's target | all five | — (a control: it runs the old tool itself) |
| T105 | every include setting's target · an include into the tree whose target does not exist yet: `--install-hook` refuses… | 6884bc2 — RV-2313, every include setting's target (83eb0dc: paths compared as the tool prints them) | all five | FAILS beside `ee6c28a` |
| T106 | every include setting's target · an include into the tree whose target does not exist yet · …the control: beside ee… | 6884bc2 — RV-2313, every include setting's target | all five | — (a control: it runs the old tool itself) |
| T107 | the write rule · `--brand DIR` and `--init` through a folder of the tree that is a symlink: each is refused in one… | c648908 — every write of the tree asks the rule before its folder is made (83eb0dc: its folder symlinks made as such) | all five | FAILS beside `1b65331` |
| T108 | the write rule · before a folder is made · …the control: beside 1b65331's tool this check FAILS | c648908 — every write of the tree asks the rule before its folder is made | all five | — (a control: it runs the old tool itself) |
| T109 | `--vendor` reads only what it copies · a file the PIN names that it does not copy is never opened, and the run goes… | 957d625 — RV-2314, `--vendor` reads only the files it copies | ran on ubuntu 3.9, ubuntu 3.12, macOS 3.12; skipped on windows 3.9 and windows 3.12: this system makes no symlink or no FIFO here | FAILS beside `f88546f` |
| T110 | `--vendor` reads only what it copies · …the control: beside f88546f's tool this check FAILS | 957d625 — RV-2314 | ran on ubuntu 3.9, ubuntu 3.12, macOS 3.12; skipped on windows 3.9 and windows 3.12: this system makes no symlink or no FIFO here | — (a control: it runs the old tool itself) |
| T111 | every worktree's configuration · an include in a linked worktree's own configuration, pointing into a working tree:… | d488cae — RV-2315, the settings every worktree reads | all five | FAILS beside `f88546f` |
| T112 | every worktree's configuration · …the control: beside f88546f's tool this check FAILS | d488cae — RV-2315 | all five | — (a control: it runs the old tool itself) |
| T113 | every worktree's configuration · beside a worktree marked `prunable` — its folder gone — `--install-hook` succeeds:… | d488cae — RV-2315 (the Owner's ruling on a prunable worktree) | all five | must stay accepted — a property, no control: f88546f's tool, which reads one worktree, passes it too |
| T114 | the PIN's names · a name outside the copy: `--check` refuses it in one line, exit 4, and the file it names is never… | c3b8296 — RV-2316, the PIN's names (seen by an audit hook in a `sitecustomize`) | all five | FAILS beside `4087e23` |
| T115 | the PIN's names · …the control: beside 4087e23's tool this check FAILS | c3b8296 — RV-2316 | all five | — (a control: it runs the old tool itself) |
| T116 | `--triage` and the submodules · a `.gitmodules` path that resolves outside the repository is skipped: no git is sta… | 7e56b7a — `--triage` skips a submodule path outside the repository (seen by an audit hook in a `sitecustomize`) | all five | FAILS beside `4087e23` |
| T117 | `--triage` and the submodules · …the control: beside 4087e23's tool this check FAILS | 7e56b7a | all five | — (a control: it runs the old tool itself) |
| T118 | destinations a person names · `--vendor DIR`, `--brand DIR --from`, `--brand DIR` and `--standup FILE.ics`, named t… | e8d2eea — a named destination resolved once, the write rule under it; e477638 — RV-2317, `--brand DIR` (its row) | all five | FAILS beside `4087e23` |
| T119 | destinations a person names · …the control: beside 4087e23's tool this check FAILS | e8d2eea | all five | — (a control: it runs the old tool itself) |
| T120 | destinations a person names · RV-2317 · `--brand DIR` without `--from`, a row of row 118's check: named through a f… | e477638 — RV-2317, `--brand DIR` | with row 118's check: all five | row 118's command: FAILS beside `4087e23` |
| T121 | amends row 23 · two worktrees share one copy — failed on Windows: the test named the copies with the system's separ… | a7d790a — the copies named with `/` on every system; the tool unchanged | the check of T23 — see that row | passes at the head |
| T122 | amends row 79 · the configuration, and TRIAGE.md, each a symlink — failed on Windows: the configuration's refusal i… | 9b69d0d — the output is UTF-8 from the start | the check of T79 — see that row | as row 79 |
| T123 | the reading rule · the configuration a symlink, the console's code page cp1252: the one line is said in UTF-8, exit… | 9b69d0d — the output is UTF-8 from the start | all five | FAILS beside `90abab9` |
| T124 | the reading rule · the configuration in cp1252 · …the control: beside 90abab9's tool this check FAILS | 9b69d0d | all five | — (a control: it runs the old tool itself) |
| T125 | amends rows 116 and 117 · `--triage` and the submodules — the control passed on Windows: there the audit hook gets… | 9375e0e — the watch reads a Windows command line, and proves itself | the check of T116 and T117 — see those rows | as rows 116 and 117 |
| T126 | amends rows 62 and 63 · the PGP-armoured commit object — the suite stopped on Windows: the object went to `git hash… | 90eee04 — the object written as bytes | the check of T62 and T63 — see those rows | as rows 62 and 63 |
| T127 | the reading rule · `--check` reports a vendored copy's PIN under the rule: its VERSION a symlink, refused in one li… | 5126178 — `pin_report` under the reading rule | all five | FAILS beside `90abab9` |
| T128 | the reading rule · the copy's PIN and VERSION · …the control: beside 90abab9's tool this check FAILS | 5126178 | all five | — (a control: it runs the old tool itself) |
| T129 | amends rows 114 and 115 · the PIN's names — RV-2318: the check leaned on the watch for *never opened* without provi… | 26bcd97 — the open proved before the check | the check of T114 and T115 — see those rows | as rows 114 and 115 |

### 2b. The earlier fixes' tests, and the tests of the older claims

v0.19.0's earlier fixes came with #145; their controls are run here once, as this build's are. A claim from an earlier release names its tests; its
control was its own release's.

| # | where | what it asserts | fix | CI: ran on | negative control |
|---|---|---|---|---|---|
| X1 | test_shoalmark.py:3455 | `--html-only` starts no deriver; nothing a hook starts executes a file a branch brought | afa1a11 (#145, the report's P1) | all five | FAILS beside `afa1a11~1` |
| X2 | test_shoalmark.py:5187 | a move to `Shipped` with nothing built behind it is refused at commit time by the installed hook | 5562476 (#145, FM-005) | all five | FAILS beside `5562476~1` |
| X3 | test_shoalmark.py:5190 | …and by `--check`, exit 4 | 5562476 (#145, FM-005) | all five | FAILS beside `5562476~1` |
| X4 | test_shoalmark.py:5198 | a commit not in the history is refused | 5562476 (#145, FM-005) | all five | the rule is new with 5562476 — X2 is its control |
| X5 | test_shoalmark.py:5201 | a commit that exists nowhere is refused | 5562476 (#145, FM-005) | all five | the rule is new with 5562476 — X2 is its control |
| X6 | test_shoalmark.py:5204 | a commit that changes only the records is refused | 5562476 (#145, FM-005) | all five | the rule is new with 5562476 — X2 is its control |
| X7 | test_shoalmark.py:5208 | a real commit named passes, in `--check` and at commit time — must stay accepted | 5562476 (#145, FM-005) | all five | must stay accepted — a property, no control |
| X8 | test_shoalmark.py:5217 | a tracker whose name git quotes, moved to `Shipped` with nothing named, is refused by the hook and by `--check` | a36cf2e (#145, RV-2151) | all five (2 cases; 1 on Windows, as on main) | FAILS beside `a36cf2e~1` (its block stops after it, with a ValueError, at a part that tool cannot run) |
| X9 | test_shoalmark.py:5222 | a commit whose only path git quotes changes nothing outside the records | a36cf2e (#145, RV-2151) | ran on ubuntu 3.9, ubuntu 3.12, macOS 3.12; not run on windows 3.9 and windows 3.12, as on main | FAILS beside `a36cf2e~1` (its block stops after it, with a ValueError, at a part that tool cannot run) |
| X10 | test_shoalmark.py:5231 | the hook judges the commit being made: `git commit -a`, `git commit <path>`, and the bare index | b3fbbc9 (#145, RV-2152) | all five | FAILS beside `b3fbbc9~1` (its block stops after it, with a ValueError, at a part that tool cannot run) |
| X11 | test_shoalmark.py:5235 | the commit being made is the index: where it names the feature, the hook passes it — must stay accepted | b3fbbc9 (#145, RV-2152) | all five | FAILS beside `b3fbbc9~1` (seen in X10's run: the hook read the working tree, not the index) |
| X12 | test_shoalmark.py:5300 | a merge that brings such a move is refused, naming that commit | a36cf2e (#145, RV-2151) | all five | FAILS beside `a36cf2e~1` (its block stops after it, with a ValueError, at a part that tool cannot run) |
| X13 | test_shoalmark.py:5564 | on Subversion, a `Shipped` move the history cannot be read for is refused, never passed (exit 4, not 0) | ce5f305 (#145, F1) | all five | FAILS beside `ce5f305~1` |
| X14 | test_shoalmark.py:5572 | a real revision passes connected and is refused, not passed, unreachable | ce5f305 (#145, F1) | all five | FAILS beside `ce5f305~1` |
| X15 | test_shoalmark.py:5593 | the same with a real server, connected and stopped | ce5f305 (#145, F1) | all five | FAILS beside `ce5f305~1` |
| X16 | test_shoalmark.py:5623 | on Subversion, where `svn blame` cannot be read the rights check refuses (exit 4, not 0) | a1d839a (#145, the second fail-open) | all five | FAILS beside `a1d839a~1` |
| X17 | test_shoalmark.py:5629 | a seat without the right is refused connected and unreachable | a1d839a (#145, the second fail-open) | all five | FAILS beside `a1d839a~1` |
| X18 | test_shoalmark.py:5648 | the same with a real server, connected and stopped | a1d839a (#145, the second fail-open) | all five | FAILS beside `a1d839a~1` |
| X19 | test_shoalmark.py:5658 | an answer is refused as unread when the history cannot be read | a1d839a (#145, the second fail-open) | all five | FAILS beside `a1d839a~1` |
| X20 | test_shoalmark.py:5681 | where the newest revision cannot be read, `--check` refuses (exit 4, not 0), nothing pending | 28816ed (#145, RV-2267) | all five | FAILS beside `28816ed~1` |
| X21 | test_shoalmark.py:5689 | a pending change is judged offline from BASE — must stay accepted | 28816ed (#145, RV-2267) | all five | must stay accepted — passes beside `28816ed~1` too, by design: a pending change was judged offline before the fix |
| X22 | test_shoalmark.py:5695 | a working copy behind HEAD with a false move at HEAD is refused, connected and unreachable | 28816ed (#145, RV-2267) | all five | FAILS beside `28816ed~1` |
| X23 | test_shoalmark.py:5714 | the same with a real server, connected and stopped | 28816ed (#145, RV-2267) | all five | FAILS beside `28816ed~1` |
| X24 | test_shoalmark.py:1015 | top-level `owner` and `[seats] owner` that differ are refused at configuration, exit 1 | #145, FM-024 | all five (2 cases each) | —, the rule is new in 0.19.0's FM-024 build |
| X25 | test_shoalmark.py:1036 | an `owner` key inside another table is refused at configuration, exit 1 | #145, FM-024 | all five | —, the rule is new in 0.19.0's FM-024 build |
| X26 | test_shoalmark.py:811 | an identity under two seats is refused at configuration, exit 1 | #145, FM-024 | all five | —, the rule is new in 0.19.0's FM-024 build |
| X27 | test_shoalmark.py:815 | an identity twice under one seat is refused | #145, FM-024 | all five | —, the rule is new in 0.19.0's FM-024 build |
| X28 | test_shoalmark.py:973 | a session label that is another seat's own name, or that two seats claim, passes for neither | #145, FM-024 | all five | —, the rule is new in 0.19.0's FM-024 build |
| X29 | test_shoalmark.py:1374 | a transcript's content puts nothing into what `--whoami` prints or the hook writes; a value with a line break is no value | #145, FM-024 | all five | —, the feature is new in 0.19.0 |
| X30 | test_shoalmark.py:1393 | two logs for one id: `--whoami` refuses, exit 2; the hook writes no trailer and the commit goes on | #145, FM-024 | all five | —, the feature is new in 0.19.0 |
| X31 | test_shoalmark.py:7590 | every commit a merge carries is judged, by `--check` and at commit time | earlier release (FM-033) | all five | —, an earlier release's |
| X32 | test_shoalmark.py:5079 | a merge's own change is judged under the merger | earlier release (FM-019) | all five | —, an earlier release's |
| X33 | test_shoalmark.py:5456 | `signed` under Subversion is refused at configuration | earlier release (S4) | all five | —, an earlier release's |
| X34 | test_shoalmark.py:5460 | …and so is a top-level `owner` with `signed` | #145, FM-024 | all five | —, the rule is new in 0.19.0's FM-024 build |
| X35 | test_shoalmark.py:7730 | a seat's unsigned change to the intent or the path, a renamed heading, a deleted or moved TRIAGE.md is refused | earlier release (FM-037) | all five | —, an earlier release's |
| X36 | test_shoalmark.py:7764 | the Owner's signed commit passes; their email unsigned, or their key on a seat's commit, is refused | earlier release (FM-037) | all five | —, an earlier release's |
| X37 | test_shoalmark.py:7777 | a merge is judged by a text no parent had | earlier release (FM-037) | all five | —, an earlier release's |
| X38 | test_shoalmark.py:7794 | the commit-msg hook refuses a seat's such commit before it is made | earlier release (FM-037) | all five | —, an earlier release's |
| X39 | test_shoalmark.py:7805 | …and a merge being made that brings one | earlier release (FM-037) | all five | —, an earlier release's |
| X40 | test_shoalmark.py:7814 | `--queue` reads such a branch `wait: TRIAGE.md changed unsigned` | earlier release (FM-037) | all five | —, an earlier release's |
| X41 | test_shoalmark.py:7828 | the Owner is read from the default branch's configuration, never the branch's | earlier release (FM-037) | all five | —, an earlier release's |
| X42 | test_shoalmark.py:7846 | under Subversion the guard says it is out of scope | earlier release (FM-037) | all five | —, an earlier release's |
| X43 | test_shoalmark.py:7866 | a key a branch adds to the signers file vouches for nothing; the default branch's file is read | earlier release (FM-037, AU-19) | all five | —, an earlier release's |
| X44 | test_shoalmark.py:7873 | the Owner's real key verifies against the default branch's file; their signed change to it is accepted | earlier release (FM-037, AU-19) | all five | —, an earlier release's |
| X45 | test_shoalmark.py:7893 | `--answer` verifies as the gate does, against the default branch's signers file | earlier release (FM-037) | all five | —, an earlier release's |
| X46 | test_shoalmark.py:7906 | while the default branch has no signers file, nothing verifies against a checkout's copy | earlier release (FM-037) | all five | —, an earlier release's |
| X47 | test_shoalmark.py:350 | a vendored copy without its PIN is refused | earlier release (FM-011) | all five | —, an earlier release's |
| X48 | test_shoalmark.py:352 | a vendored copy edited in place is refused by its own gate | earlier release (FM-011) | all five | —, an earlier release's |
| X49 | test_shoalmark.py:1447 | `--vendor` refuses a target copy edited in place | earlier release (FM-011) | all five | —, an earlier release's |
| X50 | test_shoalmark.py:1464 | a release is pinned with its manifest, and the consumer's `--check` checks it | earlier release (FM-011) | all five | —, an earlier release's |
| X51 | test_shoalmark.py:1480 | a source that is no release is refused; `--allow-untagged` and `--partial` say so in the PIN | earlier release (FM-011) | all five | —, an earlier release's |
| X52 | test_shoalmark.py:1498 | a hand-edited manifest is named and the copy called unverified | earlier release (FM-011) | all five | —, an earlier release's |
| X53 | test_shoalmark.py:3424 | a deriver's non-zero exit refuses the run, nothing written | earlier release | all five | —, an earlier release's |
| X54 | test_shoalmark.py:3452 | a deriver never reads the environment | earlier release | all five | —, an earlier release's |
| X55 | test_shoalmark.py:3462 | a deriver past its bound is refused | earlier release | all five | —, an earlier release's |
| X56 | test_core.py:730 | `--queue` reads GitHub's fork flag | 12b7ea8 (#145, FM-006) | all five | FAILS beside `12b7ea8~1` (test_core.py from the head, run against that tool) |
| X57 | test_core.py:734 | a fork's own READY is a wait | 12b7ea8 (#145, FM-006) | all five | FAILS beside `12b7ea8~1` (test_core.py from the head, run against that tool) |
| X58 | test_core.py:738 | an answer-named fork waits for the Owner's reading | 12b7ea8 (#145, FM-006) | all five | FAILS beside `12b7ea8~1` (test_core.py from the head, run against that tool) |
| X59 | test_core.py:742 | a fork cannot tell the Owner to close another pull request | 12b7ea8 (#145, FM-006) | all five | FAILS beside `12b7ea8~1` (test_core.py from the head, run against that tool) |
| X60 | test_core.py:749 | a fork's verdict cannot promote another pull request | 12b7ea8 (#145, FM-006) | all five | FAILS beside `12b7ea8~1` (test_core.py from the head, run against that tool) |
| X61 | test_core.py:755 | a fork inside another pull request's head waits | 12b7ea8 (#145, FM-006) | all five | FAILS beside `12b7ea8~1` (test_core.py from the head, run against that tool) |
| X62 | test_core.py:736 | a same-repository pull request reads as it would with no fork open — must stay accepted | 12b7ea8 (#145, FM-006) | all five | must stay accepted — passes beside `12b7ea8~1` too |
| X63 | test_core.py:762 | a conflicting fork waits for the Owner's reading | 12b7ea8 (#145, FM-006) | all five | FAILS beside `12b7ea8~1` (test_core.py from the head, run against that tool) |
| X64 | test_shoalmark.py:8159 | a signed answer commit by someone who may not answer reads `wait: not an answerer`, the author named | earlier release | all five | —, an earlier release's |
| X65 | test_shoalmark.py:8048 | a seat's commit below the Owner's signed answer reads `wait: a seat's commit on your answer branch` | earlier release (FM-031) | all five | —, an earlier release's |
| X66 | test_shoalmark.py:8132 | a commit in the Owner's name that does not verify as them reads `wait: an unverified commit in your name on your answer branch` | earlier release (FM-031) | all five | —, an earlier release's |
| X67 | test_shoalmark.py:8077 | a clone that has not fetched the base waits, the commits below unread | earlier release (FM-031) | all five | —, an earlier release's |
| X68 | test_shoalmark.py:8161 | a signed answer this clone cannot verify is refused as unverifiable, naming the setting; the queue waits | earlier release | all five | —, an earlier release's |
| X69 | test_shoalmark.py:4697 | four rights and no others: a fifth word in `[rights]` is refused, naming it | earlier release | all five | —, an earlier release's |
| X70 | test_shoalmark.py:4685 | a seat without `ask` is refused for the ask it committed, naming the seat, the right and the id | earlier release | all five | —, an earlier release's |
| X71 | test_shoalmark.py:4707 | a seat without `close` is refused before the commit exists, naming `close` | earlier release | all five | —, an earlier release's |
| X72 | test_shoalmark.py:891 | `planner`, and `principal` its former name, hold ask, close and triage and not answer, with no `[rights]` line, and the ask each makes passes | #145, FM-024 | all five | —, the rule is new in 0.19.0's FM-024 build |
| X73 | test_shoalmark.py:868 | `builder`, and `implementer` its former name, hold none of the four rights, and the ask each makes is refused, naming the seat and the right | #145, FM-024 | all five | —, the rule is new in 0.19.0's FM-024 build |
| X74 | test_shoalmark.py:4806 | with `[seats]`, an answer from a seat without `answer` is refused, naming the seat and the right | earlier release | all five | —, an earlier release's |
| X75 | test_shoalmark.py:4339 | with the old key, an answer by an author `answerers` does not name is refused | earlier release | all five | —, an earlier release's |
| X76 | test_shoalmark.py:4341 | with the old key and nobody named, nobody answers | earlier release | all five | —, an earlier release's |
| X77 | test_shoalmark.py:4768 | where `answerers` asks for a signature and the seat that answers for it is not signed, the configuration is refused, naming both lines and the two ways out | earlier release (FM-015) | all five | —, an earlier release's |
| X78 | test_shoalmark.py:3762 | a logo shows in the header and as the favicon, and a script inside the SVG does nothing | earlier release | all five | —, an earlier release's |
| X79 | test_shoalmark.py:3864 | a wordmark outside the grammar is refused whole, each case naming why | earlier release (0.18.2) | all five (31 cases each) | —, an earlier release's |

## 3. The executed checks

| # | the check | how, and where | result |
|---|---|---|---|
| E1 | the history replay: every judgement of a signed line or a signature on `main`'s history, by the tool before the signed identity's change (`79be49d`) and by the head | `python3 work-tracker/evidence/FM-006/signed-history-replay.py --main origin/main --before 79be49d --after d443cf5d38c0f65d0e85f2ead2ab80a55b6be70c`, 2026-10-02 14:15 CEST, macOS, Python 3.14 (the same at `90abab9`, 13:09) | `origin/main` at `d9c154b`: 1248 commits, 171 signed — 142 PGP (all committed by GitHub), 29 SSH. The lint at the tip: 0 signature lines before, 0 after. `answer_reading`: 171 judged, 29 passed before and after. FM-037's guard: 8 judged, 8 passed before and after. **No new refusal**; exit 0 |
| E2 | the common security scanners on the final head, every hit triaged | the Auditor's, at the final head | the Auditor's result is added here as evidence |
| E3 | the re-run of the report's reproductions on the final head | the Auditor's, at the final head | the Auditor's result is added here as evidence |
| E4 | an X.509 signature on a signed line (C13) | T62's check, run once with `run-one-check.py` against the head, in a scratch clone at `d443cf5` whose suite writes the commit's signature header with an X.509 armour (an inert, invalid block) in place of the PGP one; 2026-10-02 14:17 CEST, macOS (and once before at `90abab9`, the same result) | refused on the signed line with exactly `sign with SSH; GPG returns with a fingerprint binding`, exit 4 — the check passes. The tool tells the kind from the commit's own header (`signature_kind`: ssh, pgp, x509, other) and refuses every kind but SSH on a signed line |
| E5 | a hook runner's entry where the copy is missing (C10) | `python3 -I <a path that does not exist> --root . --session-check`, macOS, Python 3.14 | `can't open file …: [Errno 2] No such file or directory`, exit 2 — a non-zero exit, so the runner refuses the commit |
| E6 | the notes' checksum (C29) | set last, after the cold review, on the final head (the Order) | the SHA-256 both notes name is added here as evidence, with the Auditor's recomputation |
| E7 | security reporting (C30) | `SECURITY.md` at `d443cf5` (unchanged since `e0a21dd`) | present: reports go privately through GitHub's vulnerability reporting form; no credentials, private records or exploit details in public |
| E8 | the negative controls of the fork checks (X56–X63), which live in `test_core.py`, where `run-one-check.py` does not reach | `test_core.py` from `90abab9` — unchanged at `d443cf5` — run once against the tool at `12b7ea8~1` (`2c00aba`) in a scratch clone, macOS | the seven fork checks FAIL there; X62, the same-repository pull request, passes there — it must stay accepted |
| E9 | no dependency, and no network of the tool's own (C41) | `shoalmark.py` at `3bd36fc` (the tool as at `d443cf5`): its imports read with Python's `ast` against `sys.stdlib_module_names`, and every program it starts read from its `subprocess` calls; 2026-10-02 15:44 CEST, macOS, Python 3.14 | every import is the standard library's; of its network modules only `urllib.parse`, which parses a path (`shoalmark.py:48`, used at `:5431`) — no `socket`, `ssl`, `http` or `urllib.request`. The programs that reach the repository's host are git and gh, and svn in a Subversion working copy; the others it starts are itself (`--html-only`), the repository's deriver and the system's own notification command |
| E10 | the seats' GitHub Apps (C42) | GitHub's public record of each seat App `shoalmark.toml` names — planner, builder, reviewer, go-to-market, designer, auditor, research — read with `gh api /apps/<slug>`, 2026-10-02 15:41 CEST | each is owned by the organisation `shoalmark`, with no permissions and no events |
| E11 | the built-in seats' rights, and `[rights] planner = []` (C38) | the tool at `3bd36fc` (as at `d443cf5`), loaded in a scratch repository with an inert configuration naming `owner`, `planner`, `reviewer` and `builder` at example addresses; `holds()` read for each seat and right, once with no `[rights]` line and once with `[rights] planner = []`; 2026-10-02 15:44 CEST, macOS, Python 3.14 | with no line: the Owner answer · ask · close · triage, `planner` ask · close · triage, `reviewer` triage, `builder` none. With `[rights] planner = []`: `planner` none, the others unchanged — a repository's own `planner` kept as it was |
