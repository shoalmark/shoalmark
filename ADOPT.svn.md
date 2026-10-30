# Try shoalmark on Subversion — the part for a Subversion working copy

Read this only on a Subversion working copy: ADOPT.md's step 1 sends you here. It belongs to `ADOPT.md` at the same
commit. Follow ADOPT.md's fifteen steps, and where a step below is named, do what it says as well, or instead where
it says so.

## What holds on Subversion

shoalmark is made and tested on git with GitHub. Subversion passes the test suite, but it has not been used in real
work: it comes without a guarantee, and the report says so.

- shoalmark needs no git on Subversion. It comes as its release's archive (ADOPT.md, step 3), and it reads the
  working copy through svn. Never ask for git to be installed here.
- Signed answers, the pull-request queue, the Owner's acts, sessions and the build judgement need git. The
  queue also needs GitHub. Such a command is refused in one line here. It names what it needs. `--session new` still
  prints an id here, without the check against git's commit trailers that shows it unused.
- It reads its history from the server through svn. A check that needs the history, such as a move to `Shipped` or an
  answer, refuses where the server cannot be reached. It never passes such a change unread.
- The svn command line runs no hook: Subversion has none on the client. Run the tool before every `svn commit` and
  commit the `INDEX.md` it writes. `--check` after the commit is what judges it.
- TortoiseSVN runs the gate itself, through two hook properties that `--install-hook` sets. It asks once before it
  runs them.
- There is no gate on the server. A commit made on the command line, or by a client that runs no hook, reaches the
  repository; `--check` after it shows what it broke.
- The identity is the server account. Signed answers need git, so on Subversion the Owner's intent and current path
  are not guarded: nothing in a working copy can tell the Owner's commit from a seat's.
- After `svn update`, nothing rebuilds the board: run `--html-only`.

## Step 1: one more prerequisite

| | Windows | macOS and Linux |
|---|---|---|
| svn's command-line tools | `svn --version --quiet` | `svn --version --quiet` |

On Windows, TortoiseSVN brings them only where its installer's option *command line client tools* was chosen. Where
they are missing, say so in one plain sentence and stop, for example: *"svn's command-line tools are not installed:
please run the TortoiseSVN installer again, choose 'command line client tools', then start me again."*

TortoiseSVN's hooks call Python by the name `python`. On Windows, the TortoiseSVN step (step 5 below) and an adoption
with TortoiseSVN need `python --version` to print 3.9 or later; `py` alone is not enough there. Where it does not,
the probe still runs. The report names what is missing: the `python` command on the `PATH`, which the Python
installer offers to set up.

## Step 2: the explanation names two more approvals

Running svn to list the working copy's files and, only after a separate explicit yes, read its history from the
project's server; and running svnadmin to make a throwaway local repository inside the folder. On Windows, add: for
one step, the Owner commits through TortoiseSVN in that folder, at this machine, and sees what the gate does. Ask
whether they will be there; without them, the step is left out and the report says so.

## Step 4: listing without the server

```
svn status -v
```

It lists every versioned item, with its revision and last author, from the working copy alone; it contacts no server.
Leave out the lines that begin with `?`: those items are not versioned. Keep the first 5,000 lines. Take the sizes
from the files themselves. The history comes from the server. Ask the person for an explicit yes before contacting the
project's server to read history. Without that yes, skip `svn log`, mark the history not readable here, and continue.
With the yes:

```
svn log -l 200
```

Where that fails because the server is out of reach, the history is not readable here, and step 9 says so. Of the
repository's address, `svn info --show-item repos-root-url`, quote only its scheme: `file://`, `svn://`,
`svn+ssh://`, `http://` or `https://`.

In the working copy, run only `svn status -v`, `svn log`, `svn info`, and `svn export` with its output in `<probe>`
(step 5). Run no `svn update`, `svn cleanup` or `svn upgrade` there: each one writes into it. Where svn says the
working copy needs `svn upgrade`, it cannot be listed without a change. Stop there and report it.

## Step 5: the trial is a working copy of a throwaway repository

```
svnadmin create <probe>/svnrepo
svn checkout <address> <probe>/trial
```

The address is `file://` followed by the repository's absolute path: `file:///Users/…/svnrepo` on macOS,
`file:///home/…/svnrepo` on Linux, and on Windows, with forward slashes, `file:///C:/…/svnrepo`. Then follow
ADOPT.md's step 5 in `<probe>/trial`. On a working copy, `--init` also sets `svn:ignore` for the board. Commit the
trial into the throwaway repository: run the tool first, then `svn add --force .` and `svn commit -m "…"`.

- **A reproduction's copy** comes from the working copy, with no server asked:
  `svn export <path> <probe>/copy/<path>`. Create the destination's parent folders first.
- **Finished items stay out of the trial.** Their gate checks a revision against the throwaway repository's history,
  which does not hold the project's revisions. Name them in the plan's tracker with the revision that built each one
  (`svn log` shows it). They become `Shipped`, with that `r<N>` in the ship log, when they move into the project
  (step 12).
- **The TortoiseSVN step, on Windows, with the Owner present.** In the trial, run
  `<py> tools/shoalmark/shoalmark.py --install-hook`. It sets `tsvn:startcommithook` and `tsvn:precommithook` on the
  folder. Run `svn update`, then commit the property change on the command line. Then the Owner, at this machine:
  1. Prepares one change you name, such as a line in a tracker's *What is true now*. In Explorer they right-click the
     trial folder, choose *SVN Commit…*, and read and allow the hook scripts TortoiseSVN asks about. The commit goes
     through.
  2. Tries a change the gate refuses: a tracker moved to `Shipped` with no revision in its ship log. TortoiseSVN
     refuses the commit and shows the gate's line. Then `svn revert` it.

  Record what the Owner saw. No human has yet seen, on Windows, TortoiseSVN run the two hook properties as described;
  only the command line is checked in CI. Where it differs, that is a finding, and the report and the feedback say so.
  On macOS and Linux there is no TortoiseSVN: the step is left out.

## Step 9: the server

On Subversion the gate reads the history through svn. Without the server, a check that needs the history refuses, in
TortoiseSVN's hook and in `--check` alike. Such checks are a move to `Shipped` and an answer. Filing and editing
trackers still works, as do `INDEX.md`, the board, `--next` and a `--check` on changes that need no history.

A repository inside the machine (`file://`) is always within reach; step 10 says what it costs.

## Step 10: identity on Subversion

The identity is the server account that committed. `signed` is refused on Subversion, since Subversion supplies
no commit signature.

- **`file://` authenticates nobody.** Every commit carries the name of the operating-system account that made it. The
  rights checks then catch mistakes, but they cannot tell the Owner's commits from an agent's.
- **One seat is one svn account** whose credentials exist only in that seat's environment: a container, or a Windows
  user of its own. The Owner's cached credentials stay out of reach. Subversion keeps them for the operating-system
  account, in `~/.subversion/auth` or, under Windows, in the account's credential store. Anything that runs under that
  account can read them, so you need not look to know it, and you never do.
- **Moving to git.** Where the repository exists only for the agents' work, the report may name moving it to git as
  one option, with its cost:
  - the history moved;
  - the tools the team uses changed;
  - the Owner's signed answers and the guarded intent gained in return.

  It never presses for it.

## Step 12: if the Owner says yes, on Subversion

The same steps as in ADOPT.md, in the project's working copy, run from its root (`svn info --show-item wc-root`):

- `--vendor`, the files copied from the trial, and `--init --key <KEY>` with the same key. On a working copy, `--init`
  sets `svn:ignore` for the board.
- Copy the trackers in. Finished items now become `Shipped`, each with its `r<N>` in the ship log; the gate checks
  them here.
- Run the tool until it exits 0, then `svn add` the new files.
- **Ask before the first commit.** Before every `svn commit`, run the tool and commit the `INDEX.md` with it. Where
  Subversion calls the directory out of date, run `svn update` first.
- `--install-hook` sets the TortoiseSVN hook properties on the working copy's root; ask first, then commit the property
  change. Run it again after each upgrade, then `<py> tools/shoalmark/shoalmark.py --check` once after the commit.
  TortoiseSVN asks each person once before it runs them.
- **Way back on Subversion:** first `svn propdel tsvn:startcommithook .` and `svn propdel tsvn:precommithook .`,
  committed. Then delete what ADOPT.md's way back names.
