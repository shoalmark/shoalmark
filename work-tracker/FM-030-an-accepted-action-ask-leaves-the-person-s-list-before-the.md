---
id: FM-030
status: In Progress
considered: FM-008, FM-014, FM-016, FM-018, FM-023, FM-029
tags: bug
next: build
triaged: 2026-09-25
rank: 3
tier: P1
hook: "At the person's morning sitting, `--standup` printed 0 items and `--owner` printed NOTHING NEEDS THE OWNER, yet two acts only his hands can do were owed that day. For an action ask the answer is a promise, not the act, and the tool drops the ask the moment the promise is signed. The rules it ships even steer the second kind away from him."
---

# FM-030 — An accepted action ask leaves the person's list before the act is done

## What is true now

**Filed 2026-09-24; nothing is built.** Found on 0.17.7 in a consumer repository at its morning sitting. The lines below
are from 0.17.8 (`v0.17.8` = `62db9f8`; `main` at `cdd6e3f`). A first review ran on an earlier chain of this branch, which was
replaced before its merge to keep unredacted detail out of the record; it found R1–R16, and this text closes R1–R10.

**What happened.** `--standup` printed *0 item(s) — nothing needs the Owner today* and `--owner` printed *NOTHING NEEDS
THE OWNER*. Two acts only the person could do were owed that day:

1. **An accepted action ask.** Asked: will you take one prepared sitting for the acts only your hands can do? Answered
   the day before: *accepted, one sitting this week*. The sitting had not happened.
2. **A read on production with a deadline.** It was due before a fixed hour that same day, and filed as `next: run`.
   The field says a run is next. It does not say whose hands the run needs.

Reproduced by the review on a scratch copy: `--owner` and `--standup` show nothing for an accepted action ask, and
`--answered` hands it to a seat.

**Why the first one disappears.** `owner_queue()` (`shoalmark.py:700–709`) keeps an ask only while
`not t.get("answer")`. `--owner` (`owner_digest`, :756) and `--standup` (:785) read that queue. So does the board's
waiting list, which filters on the same condition (:1292). For a **ruling**, the answer is the act. For an **action**
(*hands only the Owner has*, `ask-kind` at :287), the answer is a promise and the act is still his. `--standup` has a
heading for the kind, *YOUR HANDS — one sitting, in this order* (:780), but it is empty from the moment he says yes.
`--owner` has no such heading at all. It lists asks, and its first line reads *NOTHING NEEDS THE OWNER* whenever that
queue is empty (:760).

**Where it goes instead.** `--answered` (:741) lists the ask as *answered, not yet acted on* and tells a **seat**: *act on
it, then `--clear-ask`*. A seat cannot do the act, because the act is his. So the promise sits on a list the person does
not read, addressed to someone who cannot keep it. Four texts tell him so in advance: `--answer`'s last line *it has
left your queue* (:970), the schema (:291), `docs/signing.md:95` and `docs/de/signing.md:97`.

**Why the second one is invisible: a shipped rule sends it away from him.** The triage rules the tool ships
(:1757–1763) test the moves in order and take the first that fits. `run` comes before `owner` and reads *a run nobody
has made yet … **even where the Owner must attend it***. So a production read that only his credentials can make is
filed as `run`, as instructed, and never reaches his list. The rule is right for a run he only watches, and wrong for a
run only his hands can make.

**A related design, not this defect.** FM-023's worked example puts *the hands sitting* in its own slot, outside the
standup budget (FM-023:171). That is a planning view. This tracker is about the lists telling him nothing is owed.

**Widened 2026-09-24 on the Auditor seat's raise of FM-007 (the Principal's line on its proposal, item 3):** the person's lists —
`--owner`, `--standup`, the board — also show a `next: owner` tracker whose act is the Owner's own, a ruling he gave whose hands are
his, under *YOUR HANDS — raised* with its raise line, whether its ask is open, answered or absent. As filed, this tracker covered
accepted *action* asks only; FM-007 is the case it would still miss.

**Widened 2026-09-24 a second time, on the Auditor seat's check 24 on v0.18.2 (P3), through the Owner:** after `--answer` the front matter still reads `next: owner` — the record says the Owner's move after his move is made (FM-033 read so from 18:59 until the evening pass re-applied its verdict). For a ruling, a determination or a ceremony the seat's move follows, and 0.18.3 writes `next: build` with the answer — the move the rules give unbuilt work, as this evening's pass gave FM-033 (the Reviewer's R5); for an action ask — one whose *yes* needs the Owner's hands — `next: owner` stays, because the act is still his (this tracker's own line: the answer is a promise, not the act), and `--schema` says that an ask whose yes needs his hands is `action`, whatever else it decides (the Auditor's AU-12 and AU-22). `revoke` and `--supersede` key on the answer's presence, not on `next: owner`.

## Why

The digest is what a session's last message leads with, and the standup is the person's one sitting. *Nothing needs
you* on a morning his hands are due tells him the opposite of the truth. If he believes the tool, the act slips, and the
acts this kind covers are the ones the design reserves for him because they carry risk.

## Raised

*One sourced line per raise — the date, who raised it, the fact, its source, what it undermines; no counts. The Auditor seat's
line as the Owner pasted it on 2026-09-25 at 07:06:48, word for word.*

- 2026-09-25 · Auditor (8b91dba2), through the Owner · two acts owed to the Owner have no button on his board: FM-007's hardware key (answered 09-22) and path 3's exception (FM-032, answered 2026-09-24 21:32:35, 97fa87a); --owner prints NOTHING NEEDS THE OWNER · undermines: FM-032's answer ("until FM-007's hardware key" has no route to happen), TRIAGE.md path 1

## Done when

- **An accepted action ask stays on `--standup`** under *YOUR HANDS*, marked **promised**, until a seat clears it.
- **It stays on `--owner`** under its own heading for promised acts of his hands.
- **It stays on the board's waiting list,** marked promised.
- **The mark shows the answer's date and his answer, quoted.**
- **The first lines count it.** `--owner` no longer prints *NOTHING NEEDS THE OWNER*, and `--standup` no longer prints
  *0 item(s) — nothing needs the Owner today*, while a promised act is open.
- **Clearing it records the act.** `--clear-ask` on a promised action ask records where the act's record is. That is a
  new argument or field of `--clear-ask`, and the builder chooses its form.
- **A rejected action ask leaves every list, as today.** Rulings, determinations and ceremonies are unchanged: their
  answer removes them at once.
- **`--answered` stops sending an accepted action ask to a seat.** It says the act is the person's and waits for its
  record.
- **The texts say it too.** For an action ask, `--answer`'s last line (:970), the schema (:291) and both signing pages
  no longer say the ask *leaves your queue*.
- **The shipped triage rule is split.** A run the Owner only attends stays `run`. A run only his hands can make (his
  credentials, his machine, his production) is `owner`, carried as an `action` ask. The rule text at :1757–1763
  changes, and `owner` is tested before `run` for that case.
- **A check:** an accepted action ask appears in all three lists and in both first lines, and is gone after
  `--clear-ask`. A rejected one never appears. A ruling's answer still removes it at once. The triage prompt text
  carries the split.

## Ship log

| Date | Event |
|---|---|
| 2026-09-24 | Widened by one line to rulings whose act is the Owner's (FM-007), on the Auditor seat's raise; nothing built. |
| 2026-09-24 | Filed. A first review on an earlier chain found R1–R16; the chain was replaced before its merge to redact (R16); this text closes FM-030's share of R1–R10, and R11–R15 stay open. |
| 2026-09-24 | Widened a second time, on the Auditor seat's check 24: `next: owner` after an answer; 0.18.3 builds this line (ruling · determination · ceremony → `next: build`; action stays `owner`). |
| 2026-09-24 | In Progress — 0.18.3 builds its second widening — `next:` after an answer (the Auditor seat's check 24); the status set here, on the pass branch, before the first build commit (the Auditor's AU-20). |
| 2026-09-24 | A line under the freeze for 0.18.4, the answer flow's: `--answer` cuts the commit subject at 60 characters, so PR 61's subject reads *…FM-007's hardware ke* while the signed `answer:` line is whole (the Reviewer's observation on the answer branches, 21:4x); a subject is cut between words, with an ellipsis, or not at all. |
| 2026-09-25 | **Raised** by the Auditor seat through the Owner (07:06:48), the line above word for word from his paste: two acts owed to him have no button — FM-007's key, FM-032's path 3 — and `--owner` prints NOTHING NEEDS THE OWNER; it names FM-032's answer and path 1 as undermined, so this tracker is re-judged the same day (his raise rule, `9e48ee8`). |
