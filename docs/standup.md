# The standup — whenever it suits you

*Humans have office hours. Agents have budgets. Between the two sits one sitting, whenever it suits you.*

Everything that needs you is on the board's first line and in one command:

```
python3 tools/shoalmark/shoalmark.py --standup
```

It prints the agenda of one sitting, by kind — **rulings** first (answer; a provisional answer is an answer), then what
only **your hands** can do, in the order that frees the most work, then what **evidence could settle** without you,
then **buttons**. Each item is one question, with how long it has waited and what it holds up. After the questions come
**your acts, with their time** — missed and overdue first, then what falls due, then what has no date yet.

## When

Whenever it suits you: the board's stand-up prompt is one click away, or run `--standup` yourself. A fixed slot is
optional:

```
standup = "09:00"          # in shoalmark.toml — local time; empty, the default, sets none
standup_minutes = 15
```

The agenda's first line carries the time, when one is set, and the length. A slot in your calendar, if you want one, is
yours to make: the tool writes no calendar file and posts no notification (R9). **Several repositories?** One sitting
can hold them: the next section.

## Several repositories, one sitting

```
python3 tools/shoalmark/shoalmark.py --standup ~/code/notes-app ~/work/client-site ~/code/side-project
```

One agenda, by kind, across the repositories you name — each item with its repository. Each is read as it stands: a
git repository with its branch and its commit, a Subversion working copy with its revision, a plain folder as it is. A
folder it cannot read is named with why and counted in nothing. Every count is a repository's own, then added: FM-001 in
two repositories is two items.

It runs nothing of theirs — no repository's own tool, deriver, hook or configured program, and no fetch — and writes
nothing, in a repository or anywhere else. It starts git and svn from PATH's absolute entries outside the repositories you
name; where none holds one, the folders that need it are named with why. It says what that leaves unread: whether a git working tree has changes,
which `git status` there tells; and what each repository's own `--standup` reads by those means — the pull-request
queue, and, where a repository has `[seats]`, who asked. You answer in each repository, as ever, and its own `--standup`
there tells the rest.

On the board, the box of what waits for you carries two buttons: **stand-up prompt**, before the sessions of the last day, and
**close-out prompt**, at its end. Each copies a fixed prompt for the session you use — Claude Code, Codex or another: one asks it
to hold your sitting from this agenda, one item at a time, then to put the blockers and the day's ranked plan to you, and on your
go to direct the builder and reviewer work under the agents' contract, every merge yours; the other, to read the day back from
the record and change nothing. Neither button runs anything, and a message is never an answer: you record each decision
yourself — on git with the command the session prints for you to run, on Subversion with the lines you write and commit, in a
plain folder with the lines you write.

## What agents do with it

Before the standup, every question to you is written as an `ask:` in its work item — one sentence you can answer.
Between standups nobody interrupts you except for what cannot be undone. A session's last message ends with
`--owner`: the same list, so it arrives without you opening anything.

## Answering

On the board each question carries **accept** and **reject**. Either opens a dialog with the question, its choices, the
one the agent recommends, and what it holds up; accept may carry your change, reject says why. OK gives you one
command — `python3 tools/shoalmark/shoalmark.py --answer AP-007-Q1 accept` — which writes your answer as a commit, signed
with your key once you turn signing on. The answer is your own commit: [Your answer is your commit](signing.md).

## Your acts, with their time

Some answers are promises: *yes, I will read production at seven*. What follows is an act only you can do, and it has a
time — `due:` in its work item, and a window after it (`window:`, 60 minutes unless it says). The board lists your acts
under the questions, each **due**, **overdue** after its time, or **missed** once its window has passed with no result.
An act you promised reads as your promise — the option you took — with the question it answered below it, smaller.
Each carries two buttons: **done** asks where the result is — the path is enough: the record adds what the repository
says of the file, who added it and when, and for a review its verdict — and gives you
`python3 tools/shoalmark/shoalmark.py --done AP-007 "evidence/AP-007/read.md"`; **reschedule** asks for the new time and
gives you `--due AP-007 <time>`. Both are signed as an answer is, and committed on the branch you stand on; nothing is
pushed.

## Where your answer lands

What you answer or do is one commit of yours, on the branch you stand on, signed with your key once you turn signing on:
`--answer`, `--done`, `--due` and `--revoke` cut no branch and push nothing. Each says what it committed, and where, and
rebuilds the board, so the page you come back to shows it at once on that branch: the question leaves *waiting for you*,
and an act done leaves *your acts*. It counts once that commit is on the default branch: push it, or merge the branch
that carries it. A checkout without that commit — the default branch before it lands, or another machine — still shows
it waiting.

To take back an answer, run `python3 tools/shoalmark/shoalmark.py --revoke AP-007-Q1 "<why>"`, with the id of the ask it
answered; to take back an act done, `--revoke AP-007 "<why>"`, with its work item's id. The board has no button for it.
Either is a new commit, never an overwrite: the answer it takes back goes into the work item's ship log; for an act
done, the revocation goes into its record under *Acts*, and the act is owed again.

Invites and notifications are gone (R9): `--invite`, `--notify` and `--standup FILE.ics` print one line saying so. Where
an earlier version left a calendar file, a schedule or its state on your machine, `--standup` and `--owner` name each
piece until you remove it, and the README says how.

## Which review was independent

Before work reaches you for a merge, a reviewer judges it, and the reviewer's verdict commit names the tip it judged
(`Reviewed: <sha>`). Every agent commit also names its session. So the board counts this week's verdicts:
**independent** — the reviewer ran in another session than the one that built the work — or **same session** — a
sub-agent of the builder's own session, which is a second opinion from the same run. A READY is worth what its count
says; you see it before you press merge.
