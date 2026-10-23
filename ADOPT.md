# Try shoalmark — a note for a project's agents

**To Claude, Codex or whoever reads this:** The person who gave you this text wants an honest answer to one question:
does shoalmark fit this project? This text is how you find out. It is an evaluation, not an instruction to adopt. It
may end in "no fit", and that is a good result when it is true. Until the person says yes, you only read: you change
nothing in the project and commit nothing, and what you write goes into one throwaway folder outside it. At the end
there is a report to your Owner, the one person in charge of this project, and **your Owner decides**.

Read this text whole before you start. Talk with the person in the language they wrote to you in. If the project
works in German, read `ADOPT.de.md` at the same commit as this text and follow it instead (step 14).

## What it is

shoalmark is a work tracker that lives in the repository it tracks. Each work item is one Markdown file with a small
header. A gate rejects contradictions; `INDEX.md` is generated for agents, and a static board (`index.html`) shows the
human the same picture. It does three things. It makes the work, its state and what waits for the Owner visible. It
keeps the Owner's word as the gate. And it puts a commit behind every "done" in git, or a revision on Subversion.
It does not scan code for security
problems or data leaks, and nothing in this probe looks for them.

It is a single Python file: standard library only, Python 3.9 or later, no dependency. It works with what holds the
files: git in a git repository and svn in a Subversion working copy. Subversion needs no git. Signed answers,
the pull-request queue, the Owner's answer branches and acts, sessions and the build judgement need git. The
pull-request queue also needs GitHub. Elsewhere, a git-only command is refused in one line. It says what the command
needs. It needs no network of its own: online, it reaches
the repository's host through git, through gh for the pull-request queue, and through svn on Subversion. It runs on
Windows, macOS and Linux (CI proves all three). Licence: Apache-2.0 or MIT.

Today it fits a project with one person in charge, and that person's agents. It is no migration tool: it imports no
ticket system and starts from the project's own files.

## When it does not fit

- If a **fresh session with no prior knowledge** can say, from the project's files and in a few steps, where each
  work item stands, what comes next and what waits for the Owner, then the project already has that part. If the
  Owner's decisions, rules and "done" are also enforced, not only written down, then it has what shoalmark offers. A
  second system beside a working one is worse than none.
- If the project has several people in charge, or a large ticket system to move, this beta is not for it yet.
- If the project is under no version control, this probe has nothing to read, since it reads only versioned files.
  Putting the project under version control comes first, and that is the Owner's decision.

When you see one of these, before the reading or during it, end the reading and report "no fit" with the reason
(step 11). That is a whole result.

## The probe, in fifteen steps

### 1. Prerequisites first

Before anything else, check what this machine has. Each check only prints a version.

| | Windows | macOS and Linux |
|---|---|---|
| Python 3.9 or later, always | `py -3 --version`; where there is no `py`, `python --version` | `python3 --version` |
| git, only in a git repository | `git --version` | `git --version` |

On Windows, `python` can be a stand-in that only points to the Microsoft Store and prints *Python was not found*:
that is no Python. Below, `<py>` is the command that printed the version: `py -3`, `python` or `python3`.

What holds the project's files decides the rest. Look in the project's folder and the folders above it:

- **A `.git` folder or file:** a git repository. It has git: check `git --version`. The probe reads the project
  through git.
- **A `.svn` folder:** a Subversion working copy. Read `ADOPT.svn.md` at the same commit as this text now. It adds
  svn's command-line tools to this list and says what differs in steps 4, 5, 9, 10 and 12. git is not needed there.
- **Neither:** see *When it does not fit*.

Never ask for git to be installed for the probe itself: the tool comes as an archive, and the throwaway folder is a
plain folder that needs no version control.

Where something is missing, say in one plain sentence, in the person's language, what to install, and stop. For
example: *"Python 3.9 or later is not installed: please install it from https://www.python.org/downloads/, then start
me again."* In a git repository whose `git --version` does not answer: *"This project is a git repository, but git is
not installed here: please install it from https://git-scm.com/downloads, then start me again."*

### 2. The person's yes, after one plain explanation

First choose the throwaway folder: beside the working copy, named after it with `-shoalmark-probe` added
(`projects/shop` gets `projects/shop-shoalmark-probe`). Where that would sit inside another working copy, or its parent
cannot be written, use the same name in the person's home folder. Where the name is taken, add `-2`.

Then tell the person what follows, in your own words and in their language, covering every point:

> I will check whether shoalmark fits this project. shoalmark is a work tracker: each piece of work is a file in the
> project's repository, so that you and your agents can see what stands where, and what waits for you.
> - I only read this project. I change nothing in it and commit nothing.
> - I write only into one new folder outside it: `<the folder>`. You can delete it afterwards.
> - I read at most 80 files, 600 KB in all, within 20 minutes. I never read databases, exports, credentials, or files
>   that may hold customer or personal data. The whole check takes at most 45 minutes.
> - You will be asked to approve: the network, to download the tool's release archive from GitHub; the system's
>   checksum command; writing into that folder; running Python there, to unpack and run the tool; and in a git
>   repository, running git, to list the project's files and read its history. These requests are expected. If the
>   project is already in use, I may also ask to run its code to reproduce a bug, never anything that writes data,
>   calls a live service or changes the project. Only at the end, and only on your yes, I may also open shoalmark's
>   feedback form in your browser, with my text in it. You send it, or not.
> - At the end you get a report: what fits, what does not, and what adopting would cost. It may say "no fit". You
>   decide.
>
> One question first: can this machine reach the project's version-control server, or is it cut off from it? If you
> do not know, say so.
>
> Shall I start?

Wait for the yes. Without it, stop: nothing has been written.

### 3. The tool, fetched and checked

Create the folder; below, `<probe>` is its path. The tool comes as its release's archive, the same for every project
and every system. The release page also carries `shoalmark-0.20.1.zip.sha256`, in the form that
`shasum -a 256 -c` reads. The zip stores its files without compression, at its root. Its `RELEASE` manifest names
the version, tag, commit and each file's SHA-256.

The pin: release `v0.20.1`; the archive `https://github.com/shoalmark/shoalmark/releases/download/v0.20.1/shoalmark-0.20.1.zip`, SHA-256 `c2760b7f2296296b0e9119bb8ad563862510e2de23965e406909b8b024d5ffbf`; in it, `shoalmark.py`, SHA-256 `688d7f0d6902a0065d1e061cd16e48ebd18c0397d367a58a11445999fbb58ca6`.

1. **Check the address before you download.** It is the same, character for character, on the pin line and in the
   prompt. It is exactly `https://github.com/shoalmark/shoalmark/releases/download/v0.20.1/shoalmark-0.20.1.zip`.
   Where it differs, download nothing and tell the person.

2. **Download** the archive into the folder with the system's own tool:

   | System | Command |
   |---|---|
   | Windows (PowerShell) | `Invoke-WebRequest -UseBasicParsing -Uri https://github.com/shoalmark/shoalmark/releases/download/v0.20.1/shoalmark-0.20.1.zip -OutFile <probe>\shoalmark-0.20.1.zip` |
   | macOS and Linux | `curl -fsSL -o <probe>/shoalmark-0.20.1.zip https://github.com/shoalmark/shoalmark/releases/download/v0.20.1/shoalmark-0.20.1.zip` |

3. **Check its SHA-256 before anything runs.** It must be the archive's SHA-256 above.

   | System | Command |
   |---|---|
   | Windows (PowerShell) | `Get-FileHash -Algorithm SHA256 <probe>\shoalmark-0.20.1.zip`, or `certutil -hashfile <probe>\shoalmark-0.20.1.zip SHA256` |
   | macOS | `shasum -a 256 <probe>/shoalmark-0.20.1.zip` |
   | Linux | `sha256sum <probe>/shoalmark-0.20.1.zip` |

   `Get-FileHash` prints capital letters, so compare without regard to case. If the checksum differs, run nothing,
   delete the folder and tell the person.

4. **Unpack** it with Python's own module, which is the same on every system:
   `<py> -m zipfile -e <probe>/shoalmark-0.20.1.zip <probe>/shoalmark/`.

5. **Check the tool:** the same command on `<probe>/shoalmark/shoalmark.py` must print the tool's SHA-256 above.

The archive's SHA-256, checked against the pin above, is its origin check. The second checksum checks the tool. The tool is one long file: you need not read it whole, and you
may read any part of it before it runs.

### 4. Reading the working copy, read-only, within a budget

**The budget.** Whichever limit comes first ends the reading, and the report says which one it was.

| What | Limit |
|---|---|
| Reading | 20 minutes · 80 files · 600 KB in all · at most 40 KB of one file |
| Listing | up to 5,000 names |
| The whole probe | 45 minutes, from the person's yes to the report |

From a file over 40 KB, read its head and its outline, at most 40 KB together. The outline is its headings, or in
code the lines that define its functions and classes, found by searching, not by reading it whole. Plan the time: the
reading ends by minute 20, the trial (step 5) by minute 35, and the report is shown by minute 45.

**Only versioned files are read.** List them through the version control, never with the file system. In a git
repository (on Subversion, `ADOPT.svn.md` says how):

```
git -c core.quotePath=false ls-tree -r -l --full-tree HEAD
```

It prints each file's size and path. Keep the first 5,000 lines: add `| head -n 5000`, or `| Select-Object -First 5000`
in PowerShell. Where it stopped at 5,000, the listing was cut, and the report says so. The history counts as one file
of the 80:

```
git log -n 200 --date=short --format="%h %ad %G? %ae %s"
```

Read code, plans and docs: the README and the documentation first, then the plan wherever it is kept, then the
code's outline.

**What is never read.** Skip a file when any of these holds, and list it as skipped, with the reason:

- *By kind:*
  - databases: `.db .sqlite* .mdb .accdb .mdf .ldf .fdb .dbf`;
  - dumps and backups: `.sql .dump .dmp .bak .bson .rdb`;
  - archives, never unpacked: `.zip .tar .gz .tgz .7z .rar` and the like;
  - spreadsheets and exports of records: `.csv .tsv .xls* .ods .parquet .jsonl`, and any JSON or XML file over 100 KB;
  - environment and credential files: `.env*`, keys and certificates (`.pem .key .p12 .pfx .crt .cer .jks .ppk` and
    the like), `.kdbx`, `id_*`, `.npmrc .pypirc .netrc`, `*.tfstate*`;
  - mail (`.eml .msg .pst .mbox`) and logs (`.log`);
  - images, audio, video and other binary files.
- *By name:* a file or folder whose name contains secret, credential, password, token, Passwort or geheim, case
  aside. The rule goes by the name, so `tokenizer.py` is skipped too.
- *By folder:* a folder anywhere in the path whose name is, contains or compounds one of these words, singular or
  plural, case aside: export, backup, dump, data, Daten, db, Datenbank, Sicherung, customer, Kunden, personal,
  uploads, attachments, logs, secrets, `.ssh`, `.aws`, invoices, contracts, hr, personnel, Rechnungen, Verträge,
  Personal. `db` and `hr` count only as words of their own: `db/` and `hr-files/` are skipped, `chrome/` is read.
  Build output and dependencies are skipped too: `node_modules/`, `dist/`, `build/`, `target/`, `.venv/` and the like.
- *Office documents and PDFs* (`.doc* .odt .ppt* .odp .pdf .rtf`) are read only from folders that look like
  documentation or plans (`docs/`, `Dokumentation/`, `plans/`, `Planung/`, `spec/`, `design/`, `adr/` and the like),
  and only where your own tools read them without installing anything.
- *In doubt,* skip the file and list it as skipped.

**Never** open a database, read the values of environment variables, or quote a file that turns out to hold records
of people. Stop reading such a file and list it as skipped. The rule decides what you read. It is no search for such
data, and the report never claims that the project's files hold any, or none.

Keep a reading log in `<probe>/read.md`: each file read, each file skipped with its reason, the counts, and the limit
that ended the reading.

**Five questions, before.** While you read, answer them from the project's files alone, not from this session's
memory, and count the files and steps each answer took. (a) Where does an open work item in the middle of the plan
stand? (b) What is its next step, and whose is it? (c) What waits for the Owner right now? (d) What is blocked, and
by what? (e) How can you tell that a finished item is done?

### 5. The first result that fits where the project stands

Judge where the project stands from what you read, and say why in one sentence:

- *in planning:* a plan, and little or no code that runs;
- *in building:* code written against a plan, not yet in use;
- *in production:* in use, with releases or deployments, and bugs reported.

**Set up the trial.** The trial is a plain folder. There the tool cannot tell who changed a line or what a change
shipped, and it says nothing about it. With `owner signed` or `[seats]` in its configuration, it refuses every line a
right guards, an ask among them, since nothing there is committed. Keep them out of the trial's configuration.
Create the folder `<probe>/trial/` first. Then:

```
<py> <probe>/shoalmark/shoalmark.py --root <probe>/trial --vendor <probe>/trial/tools/shoalmark
cd <probe>/trial
<py> tools/shoalmark/shoalmark.py --init --key <KEY>
```

`<KEY>` is the key the project already uses for its work items (`AP-12` gives `AP`), else two to five capital
letters from its name. Every id carries it, so the trackers keep their ids when they move into the project
(step 12). The report names the key, and the Owner may choose another before anything moves. `--vendor` checks that the manifest's version equals `VERSION` and every file of the set matches its SHA-256.
Otherwise it refuses in one line and writes nothing. The PIN's first line names only these checks, for example:
`# shoalmark 0.20.1 · vendored from an archive whose manifest names v0.20.1, commit <sha>, every file matched · <date>`.
`--init` writes
`shoalmark.toml`, `docs/work-tracker/TRIAGE.md`, the agents' contract in `AGENTS.md` and a `CLAUDE.md` router; it
overwrites nothing. Set `name` in `shoalmark.toml` to the project's name. For a German project, step 14 comes before
`--init`.

**File the result** with `<py> tools/shoalmark/shoalmark.py --new "…"`. File one tracker for the plan as a whole, and
at most four for what the stage calls for, the open work first: at most five trackers in all. Each gets:

- `considered:`, the ids it was held against, or `none`;
- `epic:`, naming the plan's tracker;
- an honest `status:`;
- `next:` (`build` · `review` · `owner` · `wait` …);
- the sections *What is true now* and *Done when*.

`tools/shoalmark/README.md` describes the header.

- *In planning:* the plan's work items as trackers, and what waits for the Owner. Each such item is `next: owner`,
  with one question in `ask:` (one `?`, at the end, at most 300 characters), `ask-kind:`, `ask-since:`, and in
  `ask-proposal:` the move you would recommend.
- *In building:* the work items with their status, what blocks them (`blocked-by:`), and the next step.
  - A finished item is `Shipped` only with the commit that built it named in its ship log; `git log` shows it.
  - The trial folder is no repository, so the gate cannot judge a `Shipped` there. It judges it when the trackers move
    into the project.
  - Where you cannot name the commit, leave the item out and name it in the plan's tracker.
- *In production:* bugs, each filed with `--tags bug`, and each only with a reproduction you ran: its command and its
  output, quoted in *What is true now*.
  - A reproduction never writes data, calls a live service or changes the working copy.
  - It runs on a copy outside the working copy, with nothing installed beyond what is there. In a git repository:
    `git archive --format=zip --output=<probe>/copy.zip HEAD <paths>`, then
    `<py> -m zipfile -e <probe>/copy.zip <probe>/copy/`.
  - Ask the person before you run the project's code. Where a reproduction would need more, describe the bug and mark
    it "not reproduced".

Then run `<py> tools/shoalmark/shoalmark.py`: the gate says what is missing. Fix the trackers until it exits 0.
`<py> tools/shoalmark/shoalmark.py --next` says what to work on. The board is
`<probe>/trial/docs/work-tracker/index.html`; give the person its path to open in a browser. That is your Owner's
view.

### 6. It writes only into the throwaway folder

Until the Owner's yes (step 12), everything goes into `<probe>`: the archive and the tool, the trial, the reading
log, the report, and the copy for a reproduction. Nothing goes into the working copy: no file, no build output, no
cache. In a git repository, run there only the read-only commands this text names: `git ls-tree`, `git log`,
`git config --name-only --get-regexp`, `git rev-parse`, `git remote`, and `git archive` with its output in `<probe>`. `git fetch`,
`git pull`, `git status`, a checkout, a build, an install and a test run can each write into the working copy or its
`.git`. None of them runs there. On Subversion, `ADOPT.svn.md` names its own.

### 7. Visibility and enforcement

Measure both.

**Visibility.** Ask the five questions of step 4 again, now with `--next`, `docs/work-tracker/INDEX.md` and the board
in the trial. Count the files and steps again.

**Enforcement.** Take the Owner's decisions, the project's rules and its "done" in turn. For each, say whether
something enforces it, and what, or whether it is only written down.

- Look in versioned files: CI configuration (`.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile` …), hook
  configuration (`.pre-commit-config.yaml`, `lefthook.yml`, `.husky/` …), `CODEOWNERS`, the contribution rules, and
  decision records.
- Of the local hooks, read only the names of the files in the folder `git rev-parse --git-path hooks` names, never
  their contents.
- Settings kept on the server, such as protected branches or required reviews, cannot be seen from a working copy.
  Say "not visible from here".

What shoalmark would enforce, and no more:

- A move to `Shipped` with no commit behind it is refused (on Subversion, no revision).
- The Owner's intent and current path change only by the Owner's signed commit (git only).
- An answer counts only when it is the Owner's: signed, on git.
- Each seat's rights hold, where seats are set up. Step 10 says what that can and cannot tell apart.

The commit hook is best-effort. The gate that holds is `--check` on the branch, in CI, before a merge.

A project that already shows where everything stands, and enforces its rules and its "done", has what shoalmark
offers. Say so plainly.

### 8. Data rules as requirements

Where the project handles personal or otherwise sensitive data, and the team has already written rules for it (in a
policy, a decision or a document), the report may show how two or three of those rules become requirement rows. Each
row comes with the test that would prove it.

A requirement is one table row:

- `id`: stable, never reassigned;
- `shall`: one sentence, the system as subject, one obligation;
- `source`: who or what asks for it;
- `accept`: what a test observes.

A tracker cites it in one line of its body, `Satisfies: REQ-001`; the gate refuses the key in the header. A test
cites it in its name. Only the Owner changes a row. On git, they give a signed answer through the board. For a
standard, the row names the clause (standard, edition, clause number) and derives the company's own *shall* from it.
*Not applicable* is the Owner's answer, with its reason; on git it is signed. `requirements/README.md` in `<probe>/shoalmark/`
describes the convention.

Use only rules the team wrote down; invent none. Say plainly in the report that the convention has no automated
checks yet, and that shoalmark checks nothing about data. Never write that the project complies with anything: a
requirement met is a test passed, nothing more.

### 9. A server out of reach

Use the person's answer from step 2. Apart from the Subversion history read explicitly approved in ADOPT.svn.md step
4, do not try to reach the project's server yourself, since that would use the person's credentials. Where the
working copy cannot reach its server, in an isolated sandbox for example, the report says what works there and what
does not. In a git repository:

- *Works without the server:* the trackers, the gate on a commit, `INDEX.md`, the board, `--next`, `--owner` and
  `--standup`.
- *Needs the server:* `--queue`, which reads pull requests from GitHub through `gh`, and the Owner's answer, which
  `--answer` commits and pushes.
- *Needs one setting:* `--check` must know the default branch. Where `origin/HEAD` is not set, it refuses. Run
  `git remote set-head origin <default branch>` once; it needs no network.
- *On Subversion,* the history is read from the server. Offline, a check that needs it refuses: a move to
  `Shipped`, or an answer (`ADOPT.svn.md`).

Then name the options honestly, each with its cost: work where the server answers; keep a repository inside the
sandbox for the agents' work, which the Owner carries over by hand; or adopt nothing until the setup changes. Prefer
none of them without a reason from this project.

Nothing posts a notice: `--standup`, `--owner` and the board list each act owed, with its time. Acts need git.

### 10. Identity

In a git repository, read what the working copy says, and never look for a credential:

- `git config --name-only --get-regexp '^user[.]name$'` and `git config --name-only --get-regexp '^user[.]email$'`: whether the local
  commit identity is set;
- the history's authors, from step 4's log: how many there are, and whether the agents' commits carry the Owner's
  name. Count them, and quote no address;
- signing: whether commits are signed (`%G?` in the log), and whether signing is set up here
  (`git config --name-only --get-regexp '^commit[.]gpgsign$'`, `git config --name-only --get-regexp '^gpg[.]format$'`,
  `git config --name-only --get-regexp '^user[.]signingkey$'`): only whether each is set;
- whether a credential helper is set (`git config --name-only --get-regexp '^credential[.]helper$'`).

You run under the operating-system account of whoever started you. If that is the Owner's account, you can reach
whatever it can reach: its cached credentials and its signing key. You need not look for them to know this, and you
never do.

Where commits are not authenticated per seat, or the Owner's credentials or signing key are within the agents' reach,
the report says so plainly. Not authenticated per seat means, for example, one account shared by everyone, or agents
that commit under the Owner's name. In both cases shoalmark's rights checks catch mistakes, but they cannot tell the
Owner's commits from an agent's.

The report then names what enforcement needs: one authenticated account per seat, and the Owner's credentials out of
the agents' reach. On one machine, that means an operating-system user of the agents' own. The agents can set this up
after the Owner's yes. `ADOPT.svn.md` adds what holds on Subversion.

### 11. The report

Write it into `<probe>/report.md`, in the project's language, and show it to the person in full. It follows this
outline:

```
Where the project stands: planning · building · production — because …
What I read: … files, … KB, … minutes; … skipped (listed in read.md). The reading ended by: time · files · size · listing · nothing left to read.
The first result: … trackers in <probe>/trial, key <KEY>. The board: <probe>/trial/docs/work-tracker/index.html
Visibility, before → after: … files / … steps → … files / … steps.
Enforcement: enforced, and by what: … Only written down: … Not visible from here: …
Identity: …
The server: reachable · not reachable · not known. What works here, and what does not: …
Data rules as requirements: … (or: none written down). The test for each: … The convention has no automated checks yet.
The benefit shown: …
What adopting requires: the switch: … The setup: … The Owner's part each week: …
The transition cost: work items to carry: … Open work: … Risk in the middle of the plan: …
The result: adopt now · later, at a work-item boundary · no fit — because …
The Owner decides.
```

The Owner's part each week, in shoalmark, is this:

- answering the questions that wait for them on the board;
- writing the intent and the current path once, and changing them when they change;
- the standup: one sitting with what waits for them (`--standup`);
- the merges.

Estimate it from what waits for the Owner in the trial. Name no number of minutes that the probe did not show.

Where the cost outweighs the benefit, or nothing fits, that is the result: say it plainly. Argue for nothing.

### 12. If the Owner says yes

The trial's trackers move into the project at a work-item boundary. You ask before the first commit.

- **Replace, do not add.** The plan moves into the trackers; the old plan document becomes a pointer or is deleted,
  as the Owner says. Two sources of truth are the error the tool is meant to prevent.
- **Switch at a work-item boundary,** not in the middle of one. Propose the moment; the Owner names it.
- **In the project's working copy,** on a branch of its own where the project works with branches:
  1. Check the archive's checksum again (step 3). Then, from the working copy's root, run
     `<py> <probe>/shoalmark/shoalmark.py --vendor tools/shoalmark`.
  2. Copy from the trial what was set up before `--init`: `shoalmark.toml`, and for German also
     `docs/work-tracker/TEMPLATE.md`, `docs/work-tracker/TRIAGE.md` and `docs/work-tracker/brand/labels.yaml`. Then run
     `<py> tools/shoalmark/shoalmark.py --init --key <KEY>`, with the same key. It overwrites nothing: it adds its
     block to an existing `AGENTS.md`, between markers, and leaves an existing `CLAUDE.md` as it is.
  3. Copy the trackers, `<probe>/trial/docs/work-tracker/<KEY>-*.md`, into `docs/work-tracker/`, and bring each one up
     to date with what changed since the probe. Their ids stay.
  4. Run `<py> tools/shoalmark/shoalmark.py` until it exits 0, then `--check`.
  5. **Ask before the first commit.** Show the person the files and the commit message, and commit only on their yes.
  6. After the merge, run `<py> tools/shoalmark/shoalmark.py --install-hook` on the default branch, and again after
     each upgrade. Then run `<py> tools/shoalmark/shoalmark.py --check` once. The hook command changes the repository's
     hooks folder, so ask first.
- Then **the Owner** writes the intent and the current path in `docs/work-tracker/TRIAGE.md`. Nobody else edits those
  two sections.
- On Subversion, `ADOPT.svn.md` says what differs.
- Way back: first remove from your hooks folder (`.git/hooks/`, or the one `core.hooksPath` names) everything that calls
  the copy of the tool in the git directory: the hooks marked `# shoalmark`, and the line you added to a hook of your own
  (on Subversion, the `tsvn:` hook properties, which call `tools/shoalmark/shoalmark.py`). Delete the copy — on
  Subversion, the tool — before that, and commits are refused. Then delete
  `tools/shoalmark/`, `shoalmark.toml`, the shoalmark block in `AGENTS.md` and the copy in the git directory
  (`shoalmark-trusted/`; `git rev-parse --git-common-dir` names the directory). The tracker folder can stay: its entries
  are plain Markdown.

### 13. Feedback

At the very end, after the report and the person's decision on it, whatever it was, offer feedback to shoalmark, once.

1. **Fill in the text** from your report, in the person's language, with this template. Its first line is the result;
   the other lines are optional, and an empty one goes.

   ```
   Outcome: adopted · declined · no fit — <one sentence why>
   What was unclear: …
   What was missing, or would make it better: …
   Where the probe stuck: …
   Setup: git · Subversion — Windows · macOS · Linux — Claude Code · Codex · other — <kind of stack, a few words> — team: 1 · 2–5 · 6–20 · more than 20 — <minutes> minutes
   ```

2. **Check it.** Reread the text for these, and take each one out:
   - code;
   - paths, file names, host names and addresses (web, mail, server);
   - the contents of files or trackers, quoted or paraphrased, and command output, logs and error messages;
   - tracker ids and the project's key;
   - the names of the project, the company, people or customers, and the person's own name or handle;
   - credentials of any kind;
   - commit hashes, branch and tag names, and commit messages.

   The kind of stack stays generic, the team a band, and the time the probe's own. The text in the form is the text you
   show, word for word: the link carries nothing you did not show.

3. **Write it** to `<probe>/feedback.md`. The whole link in step 6 stays under 2,000 characters. Where it would not,
   shorten the optional lines first, then the first line's sentence. The text you write and show is the text in the
   link.

4. **Show,** in this order:
   - the text, exactly as it will stand in the form;
   - where it goes, in one line: shoalmark's public issue form on GitHub, which anyone can read, under the person's
     GitHub name once they send it;
   - what the check took out, in one line, by kind and count, for example *took out 2 file names and 1 tracker id*.
     Show the items themselves only if the person asks; they never go into the text.

5. **Ask once,** in the person's language:

   > That is the feedback for shoalmark, exactly as their public form would show it, under your GitHub name. It holds
   > no names, paths or code from this project; I checked. Shall I open the form with it filled in? You can change it
   > there, then send it or close it.

6. **On yes,** open the form in the person's browser with the system's own command; where you cannot, give them the
   link. On no, you are done.

   ```
   https://github.com/shoalmark/shoalmark/issues/new?template=what-your-agent-found.yml&found=<the text>
   ```

   `<the text>` is exactly the text you showed, encoded as UTF-8. Percent-encode every byte outside RFC 3986's unreserved ASCII set: A–Z, a–z, 0–9, hyphen, period, underscore and tilde. In particular, an apostrophe is `%27`; a double quote `%22`; a backtick `%60`; `$` is `%24`; `;` is `%3B`; `&` is `%26`; a space `%20`; and a line feed `%0A`. The completed link contains no raw apostrophe. For example, Python's `urllib.parse.quote(text, safe="")` does this.

   | System | Command |
   |---|---|
   | Windows (PowerShell) | `Start-Process '<the link>'` |
   | macOS | `open '<the link>'` |
   | Linux | `xdg-open '<the link>'` |

The person reads it there, changes it and sends it, or not. You never send it, and you never post anything. For a
person, shoalmark's one feedback address is https://shoalmark.tools/feedback.

### 14. The language

The probe follows the language the project works in: its documents, its plan and its commit messages.

- **German:** read `ADOPT.de.md` and follow it. You talk, report and file trackers in German, and you set up the
  German headings and board before `--init`.
- **Another language:** talk, report and file the trackers in that language. The tool's section headings and board
  stay English in the probe (`tools/shoalmark/README.md`, §9, says how a project changes them), and the report says
  so.

### 15. Subversion

On a Subversion working copy, `ADOPT.svn.md` at the same commit as this text is part of the probe; read it at step 1.
It covers svn's command-line tools, the listing without the server, a throwaway local repository, the TortoiseSVN step
with the Owner present, and the limits.
