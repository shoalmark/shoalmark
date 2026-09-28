---
id: FM-030
status: In Progress
considered: FM-008, FM-014, FM-016, FM-018, FM-023, FM-029
tags: bug
next: build
ask: "How does the board show an act or answer you just gave, before your merge lands it on main?"
ask-kind: ruling
ask-since: 2026-09-27
ask-options: "the board reads git: an unmerged `origin/answer/*` tip with a `done:` or `answer:` main lacks shows as done, on its way | a local pending file written by the command, cleared when main carries the change | the browser marks it on OK"
ask-proposal: "the board reads git: an unmerged `origin/answer/*` tip with a `done:` or `answer:` main lacks shows as done, on its way"
answer: "accepted - the board reads git: an unmerged `origin/answer/*` tip with a `done:` or `answer:` main lacks shows as done, on its way"
answered: 2026-09-27
answered-by: holgo99
triaged: 2026-09-27
rank: 2
tier: P1
hook: "At the person's morning sitting, `--standup` printed 0 items and `--owner` printed NOTHING NEEDS THE OWNER, yet two acts only his hands can do were owed that day. For an action ask the answer is a promise, not the act, and the tool drops the ask the moment the promise is signed. The rules it ships even steer the second kind away from him."
---

# FM-030 — An accepted action ask leaves the person's list before the act is done

## What is true now

**Filed 2026-09-24; built in part, and more on a branch not merged.** 0.18.3 and 0.18.4 shipped its first lines — an
answer writes the next move; the acts owed to the Owner on his board with their time, *done* and *reschedule*, an invite
and a notice per act — and `fm/030-the-done-dialog-shows-the-question` builds four lines more for 0.18.6, not merged
(the next paragraph; the ship log names each commit). Found on 0.17.7 in a consumer repository at its morning sitting.
The lines below are from 0.17.8 (`v0.17.8` = `62db9f8`; `main` at `cdd6e3f`). A first review ran on an earlier chain of
this branch, which was replaced before its merge to keep unredacted detail out of the record; it found R1–R16, and this
text closes R1–R10.

**Built for 0.18.6 on `fm/030-the-done-dialog-shows-the-question`, not merged, not released** — on the two raise lines
of 2026-09-27 (the Owner's word at 13:38:30, the E0 counter's row 20): an act that is a promise reads as what he
promised, the question below it, on the board, in its *done* and *reschedule* dialogs, `--owner`, `--standup`,
`--notify` and the invite (`a752c87`); an accepted action answer that names a full date with its hour seeds `due:` in
the answer's commit — a weekday alone is not read (`5f558f7`); an act command refused after its cut leaves one unsigned
line under `## Acts` on `answer/<id>`, pushed (`2935cf7`); and, on his word of 13:42:40 — the person gives the path, the
record gathers the facts — `--done`, and `--due` on an act that was done, write beside a path in the repository the
commit that added it and its date, and for a review the verdict of its last pass, that pass's `Reviewed:` sha and
`Session:`; a word that names no file there is recorded as given, *not in the repository* beside it (item 5, its sha in
the ship log). The Owner opens the pull request; code tier, the full loop is due. Not proven here: the notices on Linux
and Windows, and how a notifier shows a two-line body.

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

**For 0.18.4:** *the move after an answer follows the picked option, not the kind alone* — the Auditor seat, through the Owner, 17:23:39 on 2026-09-25: an action ask answered "not yet" must not read as the act begun.

**The ask of 2026-09-27 — the board and an act not yet merged.** The board is rebuilt by the checkout hook from `main`; an act or answer he just gave is a signed commit on `answer/<id>`, pushed, and `main` knows nothing of it until his merge. Option 1 keeps one truth: git. After the push the remote-tracking ref `origin/answer/<id>` holds the exact sha the tool committed; the board reads every such branch not merged into `main`, opens the tracker at its tip, and where it carries a `done:` or `answer:` that `main` lacks, renders the row as *done, on its way* — the branch, the sha, the push time, *your merge is next* — the buttons replaced by *revoke*; `--done`/`--answer` end where they started (on `main` for him), where the checkout hook rebuilds, so the page shows it at once. A stale branch from an earlier session is merged (ignored) or an unmerged answer (shown, with its date); a tip without the change is not shown; another machine sees it after a fetch. Option 2 (a local pending file) is a second truth beside git, per machine, drifting when a branch is rewritten. Option 3 (the browser marks it on OK) says done before anything is signed — against line 5. *Revoke*: the tool's revoke/supersede of an `answer:` (a new signed commit, never an overwrite) extended to `done:`.

**Raised 2026-09-28, this tracker's next slice after `fm/030-the-board-reads-his-unmerged-acts` lands:** a tracker whose act is
done keeps a *schedule the next act* button on the acts board (and its line in `--owner`/`--standup`), which runs `--due <id> <time>`
as his own change — today the command exists and the board shows nothing for a done act, so the Owner had no button for BUG-327's
sitting two (the Auditor's line under *Raised*). Design: the acts board lists a done tracker once, under a *done — next?* heading,
for as long as its status is open; the button opens the `--due` dialog with the last act's line as context; a tracker with no act
history shows no such row. No `--triage` change; docs and code tier as the board build's.

## Why

The digest is what a session's last message leads with, and the standup is the person's one sitting. *Nothing needs
you* on a morning his hands are due tells him the opposite of the truth. If he believes the tool, the act slips, and the
acts this kind covers are the ones the design reserves for him because they carry risk.

## Raised

*One sourced line per raise — the date, who raised it, the fact, its source, what it undermines; no counts. The Auditor seat's
line as the Owner pasted it on 2026-09-25 at 07:06:48, word for word.*

- 2026-09-25 · Auditor (8b91dba2), through the Owner · two acts owed to the Owner have no button on his board: FM-007's hardware key (answered 09-22) and path 3's exception (FM-032, answered 2026-09-24 21:32:35, 97fa87a); --owner prints NOTHING NEEDS THE OWNER · undermines: FM-032's answer ("until FM-007's hardware key" has no route to happen), TRIAGE.md path 1

- 2026-09-25 · Auditor (8b91dba2), through the Owner · a consumer's P0 production read, owed by the Owner's hands at a fixed hour on two consecutive days, was missed both times: it was named only in chat and a run sheet, --standup and --owner showed no item (next: run), no calendar invite was written, and the next day's standup did not notice · undermines: TRIAGE.md path 6, path 1
- 2026-09-27 13:38:30 · the Owner, in chat with a screenshot (taken 13:35:40), on pressing *done* for FM-024 · the *Done — where is the result?* dialog repeats the ask's question — *Who verifies 0.18.3 — a cold Reviewer session you start, this session's own sub-agent, or nobody until …?* — where the act is his accepted option; his words (spelling normalised): *for a user here the confusion might come from* [the question] *because this repeats the question; an answer with "a cold Reviewer session you start" might have been given, because the request for the result points to that one, not the other two options — right?* · source: the board's dialog, `act.done.title`/`act.done.hint`, the act's line built from `ask:`; the acts list on the board and `--owner`/`--standup` read the same · undermines: path 6
- 2026-09-27 13:42:40 · the Owner, in chat, on the Principal's `--done FM-024` line, which carried the path with the review's facts written out · the command a person composes who fills in the path: `python3 shoalmark.py --done FM-024 'work-tracker/evidence/reviews/review-fm-029-0-18-3-fourth-pass.md'`; his words (spelling normalised): *this is a more realistic answer a person might give than yours … because we expect the person in charge to be too lazy to gather all the data points your answer is giving — that would require more than three clicks for the person to complete — right?* · source: the board's *done* dialog, one field; `done_cmd` recorded the words as given and read nothing · the rule the record follows: the person gives the path, the record gathers the facts — item 5 of this branch's build
- 2026-09-27 · the E0 counter (row 20, PR 859), through the Principal · his BUG-327 promise *accepted - Sat 09-26 09:00 CEST* (09-25 15:14:03) showed on his board as *no date yet* for 5 h 24 min after the promised hour, because the hour lived only in `answer:` and no `due:` was seeded from it; and one `--due` run of his was refused after its cut (14:19:27 → 14:20:28, the undo shape) with no record of why · source: `e0-row-pr859.md`'s count (his clone's reflog, the forge) · undermines: path 6
- 2026-09-27 13:57:50 · the Owner, in chat with a screenshot (taken 13:45:18), after his `--done FM-024` (f8246fae) · the board, rebuilt from `main`, still showed the act with its *done* and *reschedule* buttons — his act lives on `answer/fm-024` until his merge; his words (spelling normalised): *when the user presses done in the dashboard's dialog, they return to the board page, but the act is not marked as answered — this is confusing and might look like a bug […] the state is rendered from main and is consistent; the answer was pushed on a branch not yet merged […], but a user won't care: they pushed the button, did the answer and expect the page to display that state right away […]* — his two ways forward: verify by sha that the act answered is the one on the pushed branch before marking it, and keep a button to answer again or revoke · source: the board's acts list reads the checkout's `main`; `--queue` already reads `answer/*` heads (`answer_reading`) · the button's result is not on his board after the press · undermines: path 6
- 2026-09-27 14:09:46 · the Owner, in chat, on the Principal's three options · *Option 1 is the only valid one and holds to the single source of truth. Go, file the ask on FM-030 with option 1 as proposed.* (spelling normalised) · the ask above; his signed answer rules it.
- 2026-09-28 08:21:57 · Auditor (8b91dba2), through the Owner (his paste headed *To: 8e509911 principal (shoalmark-principal-4)*, two points — point 1 the keychain hour, point 2 this gap; the whole paste to this seat, three lines, is saved word for word, sha256 `f7d230aeb135ce2e55166593f50f08719516d944fd85f3546a4957f11133b0fd`, with the part addressed to another session left out on his word; point 2 alone is quoted here) · *Board gap for FM-030 (your lane), 95%: a tracker whose act is done shows nothing on the board (tools/shoalmark/shoalmark.py:3509, act_of), yet --due on it opens a new act (:5063). The Owner had no button to schedule BUG-327's sitting two. Fold it into FM-030's acts board rather than a new filing.* — checked by the Principal in the tool at `02f3c5c9`: `act_of` returns None for any tracker with `done:` ("closed work owes nothing"), `due_cmd`'s own words make `--due` on such a tracker a new act; the command exists, the button does not · source: the paste; `shoalmark.py` 3684–3701 and 5325 at `02f3c5c9` · undermines: no signed rule — a design gap of this tracker's board; built as its next slice, not a new filing

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
| 2026-09-25 | **Raised a second time** by the Auditor seat through the Owner (13:31:26), the line above word for word from his paste: a consumer's P0 production read owed by the Owner's hands at a fixed hour on two consecutive days was missed both times — named only in chat and a run sheet, no board item (`next: run`), no invite, the next day's standup silent; it names path 6 and path 1, so this tracker is re-judged the same day: #1. The Auditor's product line: a due time on every act owed to the Owner; the board renders due and overdue; *Done* (result attached) and *Reschedule*; an `.ics` per act; a *missed* flag when a window passes with no result; `--standup` lists due and overdue acts — first in 0.18.4. |
| 2026-09-25 | The Owner's word at 13:33:29 on the product line above (spelling as given): *Better than only invites would be invites + notifications.* — a line under the freeze for 0.18.4's build of this tracker: every act owed to him gets its invite (`.ics`, with an alarm before the window) **and** a notification when it falls due and when its window passes with no result — a `--notify` the person schedules (launchd or cron) that reads the acts' due times from the board's data and posts a system notification; the `.ics` alarm is the first notification, on every device his calendar reaches. |
| 2026-09-25 | Correcting the rows above (the pass's Reviewer, R7, R8, R11 and R15): the product line in the 13:33:29 row — an `.ics` with an alarm per act and a scheduled `--notify` — is the seat's design on the Owner's word, not his words; the raise row read 13:31:26 from the start; the word's row first read 13:3x and was corrected in place while unmerged to 13:33:29, the record's time of his message. |
| 2026-09-25 | A line for 0.18.4 under this tracker's widening, from the Auditor seat through the Owner (18:25:16): `--queue` also prints the last day's merged and closed pull requests with their times — `gh pr list --state merged` and `--state closed`, the last 24 hours — so a seat's *still open* line is checked against the forge in the same turn. Built on `fm/030-the-acts-owed-to-him-on-his-board`, its own commit. |
| 2026-09-26 | The pass's R7 and R8 on `647da17` (`a112fbd`, P3), fixed forward before the 0.18.4 cut: R7 — the README's cron line starts with `mkdir -p "$HOME/.local/state/shoalmark" &&`, so the log's folder exists before the shell opens the redirect (the launchd plist's arguments redirect nothing; its log is `~/Library/Logs`, which macOS makes); R8 — `DUE_SHAPE` bounds a zone's minutes to 00–59, so `+05:99` and `-00:60`, which `fromisoformat` reads as `+06:39` and `-01:00`, are refused on 3.9 and 3.14, with a suite case. A line, not fixed here: `--schema` prints the `due:` and `done:` shapes raw in its Markdown table, and R5's hour group carries the alternation bar, which splits their rows there. |
| 2026-09-27 | **Asked on the board — how the board shows an act or answer he just gave, before his merge lands it** (ruling; three options; the proposal: the board reads git — an unmerged `origin/answer/*` tip with a `done:` or `answer:` main lacks shows as *done, on its way*, the buttons replaced by *revoke*), by the Principal seat at 14:14:18 on his words of 13:57:50 and 14:09:46, the ledger row first (PortDive `feat/190-day-six-the-ask-on-fm-030-the-board-reads-his-unmerged-acts` @ `71a06fbe`, 14:12:51); the two raises name path 6, so FM-030 was re-judged the same day (`triage-2026-09-27.md`: keep P1 #2 owner). |
| 2026-09-27 | Built on `fm/030-the-done-dialog-shows-the-question` for 0.18.6, not merged — on the Owner's word of 13:38:30 (his screenshot 13:35:40) and the E0 counter's row 20, the two raise lines of the day: the act's line is his promise, the question below it (`a752c87`); an accepted action answer's full date with its hour seeds `due:` (`5f558f7`); a refused act command leaves one unsigned line under `## Acts` on `answer/<id>` (`2935cf7`). The first raise line's time corrected to his message's, 13:38:30 — 13:35:40 is the screenshot's (the Principal). CHANGELOG `## Unreleased — 0.18.6`. |
| 2026-09-27 | Item 4 on `fm/030-the-done-dialog-shows-the-question`, the build in the record (`a7d0f52`): CHANGELOG `## Unreleased — 0.18.6` with one bullet per item built, the row above naming `a752c87`, `5f558f7` and `2935cf7`, and the *What is true now* clause; the first raise line's time corrected to 13:38:30, his message's, and the same time in four comments of `shoalmark.py`, the suite's block heading and the README's act row. This row added after the Reviewer's pass on `9c96f5b` found none naming `a7d0f52` (R5). |
| 2026-09-27 | Item 5 built on `fm/030-the-done-dialog-shows-the-question` for 0.18.6, not merged (`a7f26ae`) — on the Owner's word of 13:42:40, *the person gives the path; the record gathers the facts*: `--done <id> "<where>"`, and `--due` on an act that was done, write beside a path in the repository the commit that added it and its date, and for a review — a file that states a verdict — its word, the `Reviewed:` sha and the `Session:`, from its own lines, else the adding commit's trailers; a word that names no file there is recorded as given, *not in the repository* beside it, never refused; nothing outside the repository is read, nothing guessed. The *done* dialog stays one field; `--schema` says it under `done:`. The raise line of 13:42:40 and a CHANGELOG bullet in the same commit. |
| 2026-09-27 | The Reviewer's pass on `9c96f5b` (reviewer-40, `d18c9ba`): NOT READY — R1 a P2, R2–R5 P3, all accepted by the Principal. R1–R4 fixed in `2f84d47`: `--done` records a review's last pass — the last stated verdict, that pass's `Reviewed:` and `Session:`, else the newest commit's trailers, and *last pass in* where a later commit wrote it (the last stated verdict is the newest verdict commit's in 77 of 77 review files, the first in 55); only the time shapes `--schema` states seed `due:`; a path's line anchor is kept as given; the question under a promise wraps in its own column. R5 in this commit: the row for `a7d0f52` and the lead. The fix loop comes back to a Reviewer. |
| 2026-09-28 | **Raised by the Auditor through the Owner (08:21:57):** a done act's tracker shows nothing on the acts board while `--due` on it opens a new act — the Owner had no button to schedule BUG-327's sitting two. Checked in the tool; recorded under *Raised* and as the next slice under *What is true now*; no new filing, on the Auditor's counsel. Tracker-only. |
