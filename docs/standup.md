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

On the board each question carries **accept · accept with change · reject**. A click copies three lines and opens the
file under your login; you paste, commit, push. The answer is your own commit: [Your answer is your commit](signing.md).
