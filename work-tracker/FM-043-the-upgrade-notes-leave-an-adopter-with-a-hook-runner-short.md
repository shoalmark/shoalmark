---
id: FM-043
status: Proposed
considered: FM-006, FM-038, FM-040
tags: bug
hook: "the upgrade notes leave an adopter with a hook runner short of 0.19.0"
---

# FM-043 — the upgrade notes leave an adopter with a hook runner short of 0.19.0

Seat: Planner · filed 2026-10-02 on the Owner's ruling: the gaps an adopter's upgrade to 0.19.0 met are one public
0.19.1 docs item.

## What is true now

**Filed 2026-10-02; nothing is built.** An adopter that runs its hooks through a hook runner (lefthook) and has a
deriver upgraded to 0.19.0 from the public notes alone — the CHANGELOG's 0.19.0 section and its *On upgrade* clauses,
the README, `ADOPT.md` — and the tool's refusal lines. Where they were not enough:

1. `--vendor` refuses while the configuration holds what 0.19.0 refuses, one key per refusal; the notes do not say to
   fix the configuration first, nor list what it must lose in one place.
2. The CHANGELOG says to keep `[seats] owner` beside the top-level `owner` while older copies read the configuration;
   it does not say when a repository with one copy, upgraded at once, may drop it.
3. The README's hook-runner entries are short of what `--install-hook`'s own hooks do: the trailer entry passes the
   message file alone where the tool's hook passes the message file and its source, and there is no entry for the
   commit's gate and the board, nor for the board's refresh after a checkout and a merge.
4. A runner entry that stages what `--print-written` names fails where it names nothing — an empty list given to
   `git add` — and the notes do not say how to guard it.
5. A board that a hook refreshes runs no deriver, so it carries none of the deriver's columns until a run by hand;
   the notes do not say so.
6. README.md:250 says CI's `--check`, which runs the deriver, holds the derived files. That holds only where CI runs
   `--check`; the notes do not say what an adopter without it does.
7. The notes do not say to land the configuration change on the default branch first, before other work on the
   upgrade.
8. A session label in a seat's new name is refused while `[seats]` still spells the seat by its former name; the notes
   do not say to rename the seats' keys before the labels.
9. `--install-hook` has no way to show what it would write and refuse before it writes; an adopter learns its
   effects only by running it.

## Why

The notes are the whole of what an adopter has. Each gap above cost a probe, a refusal or a question; one of them (3)
leaves a runner's trailer entry short of the tool's own hook.

## Done when

Each gap above is answered in the public notes — the README's hook-runner section, the CHANGELOG's *On upgrade*
clauses, or `ADOPT.md` — or the tool's refusal line says it, each with a check where the suite can hold the text;
item 9 is answered or refused by the Owner.

## Ship log

| Date | Event |
|---|---|
| 2026-10-02 | Filed. |
