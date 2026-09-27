# The standup — one sitting a day

*Humans have office hours. Agents have budgets. Between the two sits one fixed sitting.*

Everything that needs you is on the board's first line and in one command:

```
python3 tools/shoalmark/shoalmark.py --standup
```

It prints the agenda of one sitting, by kind — **rulings** first (answer; a provisional answer is an answer), then what
only **your hands** can do, in the order that frees the most work, then what **evidence could settle** without you,
then **buttons**. Each item is one question, with how long it has waited and what it holds up. After the questions come
**your acts, with their time** — missed and overdue first, then what falls due, then what has no date yet.

## The invite

```
standup = "09:00"          # in shoalmark.toml — local time
standup_minutes = 15
python3 tools/shoalmark/shoalmark.py --standup standup.ics
```

Import the file into your calendar: weekdays, at that time. **Several repositories?** One slot each, and they must not
overlap — your calendar is the only place that sees all of them, which is why the invite is a calendar file.

## What agents do with it

Before the standup, every question to you is written as an `ask:` in its work item — one sentence you can answer.
Between standups nobody interrupts you except for what cannot be undone. A session's last message ends with
`--owner`: the same list, so it arrives without you opening anything.

## Answering

On the board each question carries **accept** and **reject**. Either opens a dialog with the question, its choices, the
one the agent recommends, and what it holds up; accept may carry your change, reject says why. OK gives you one
command — `python3 tools/shoalmark/shoalmark.py --answer AP-007 accept` — which writes the answer, signs it with your
key and pushes it. The answer is your own commit: [Your answer is your commit](signing.md).

## Your acts, with their time

Some answers are promises: *yes, I will read production at seven*. What follows is an act only you can do, and it has a
time — `due:` in its work item, and a window after it (`window:`, 60 minutes unless it says). The board lists your acts
under the questions, each **due**, **overdue** after its time, or **missed** once its window has passed with no result.
An act you promised reads as your promise — the option you took — with the question it answered below it, smaller.
Each carries two buttons: **done** asks where the result is and gives you
`python3 tools/shoalmark/shoalmark.py --done AP-007 "evidence/AP-007/read.md"`; **reschedule** asks for the new time and
gives you `--due AP-007 <time>`. Both are signed and pushed as an answer is.

Two reminders, if you want them. `--invite AP-007` writes the act as a calendar file — its time, its window, a reminder
30 minutes before — beside the work item's evidence; import it. `--notify` posts a system notification for every act
due within 30 minutes, overdue or missed, once each; schedule it yourself (the README has a cron and a launchd line).

## Which review was independent

Before work reaches you for a merge, a reviewer judges it, and the reviewer's verdict commit names the tip it judged
(`Reviewed: <sha>`). Every agent commit also names its session. So the board counts this week's verdicts:
**independent** — the reviewer ran in another session than the one that built the work — or **same session** — a
sub-agent of the builder's own session, which is a second opinion from the same run. A READY is worth what its count
says; you see it before you press merge.
