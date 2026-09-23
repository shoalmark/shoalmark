# The standup — one sitting a day

*Humans have office hours. Agents have budgets. Between the two sits one fixed sitting.*

Everything that needs you is on the board's first line and in one command:

```
python3 tools/shoalmark/shoalmark.py --standup
```

It prints the agenda of one sitting, by kind — **rulings** first (answer; a provisional answer is an answer), then what
only **your hands** can do, in the order that frees the most work, then what **evidence could settle** without you,
then **buttons**. Each item is one question, with how long it has waited and what it holds up.

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

## Which review was independent

Before work reaches you for a merge, a reviewer judges it, and the reviewer's verdict commit names the tip it judged
(`Reviewed: <sha>`). Every agent commit also names its session. So the board counts this week's verdicts:
**independent** — the reviewer ran in another session than the one that built the work — or **same session** — a
sub-agent of the builder's own session, which is a second opinion from the same run. A READY is worth what its count
says; you see it before you press merge.
