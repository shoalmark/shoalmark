---
id: FM-141
status: Proposed
considered: FM-050, FM-006
tags: bug
epic: FM-139
hook: "S1's docs round left three gaps, each incomplete rather than untrue: eight ask-id refusals have no row in README section 5, the German example's [headings] has no asks, and the German signing page names ## Passes."
---

# FM-141 — the README's refusal table lacks S1's ask-id refusals, and the German docs name two English headings

## What is true now

**2026-11-03 — filed for v0.20.3; nothing is built.** S1, the ask ids of
[FM-050](FM-050-an-ask-has-no-id-of-its-own-so-an-answer-cannot-name-the-ask.md), added nine refusals. Its docs round
left three gaps, each incomplete rather than untrue. The lines are those at this filing, and each string is quoted from
the tool, with its values shown as `<…>`.
- **README's refusal table, section 5,** has no row for eight of the nine. The ninth, `no commit answers <id>`
  (`shoalmark.py:2385`), has its row. The eight:
  1. `shoalmark.py:2050`: `` <ITEM>: <…>puts an ask with no `ask-id:` — it <…>, and an ask put to the Owner carries its own id: write `ask-id: <next id>` on the line above `ask:` ``
  2. `shoalmark.py:2054`: `` <ITEM>: <…>changes the put ask under <ask id> — its <…> — and a put ask never changes under its id: withdraw it (`<cmd> --clear-ask <ask id> owner` writes its record) and put the changed ask as <next id> ``
  3. `shoalmark.py:2058`: `` <ITEM>: <…>removes <ask id> with no record under `## <asks heading>` that carries it — `<cmd> --clear-ask <ask id> <next move>` writes the record ``
  4. `shoalmark.py:2062`: `` <ITEM>: <…>puts <ask id>, and its number is not above every number <ITEM> has used — the highest is <ITEM>-Q<n>: put it as <next id> ``
  5. `shoalmark.py:2291`: `` <ITEM>: <ask id> is taken on <default branch> — <…> — so a merge would make one number two asks: renumber this branch's ask as <next id>, its put ask unchanged; <default branch> keeps its number ``
  6. `shoalmark.py:2310`: `` wait: <ask id> is taken on <base> — renumber ``
  7. `shoalmark.py:2390`: `` <ask id> has <n> answers, on branches that do not hold each other (<commits>) — one answer must replace the other (`--answer <ask id> … --supersede`) on a branch that holds both ``
  8. `shoalmark.py:3407`: `` --answer: <ITEM>'s ask carries its id, <ask id> — name the ask you read: `<cmd> --answer <ask id> <verdict>` ``

  The sixth is a `--queue` line, and section 6's `--queue` row names it; section 5 does not.
- **`examples/de/shoalmark.toml`'s `[headings]`** (line 10) has no `asks`. So a German repository's ask records sit
  under `## Asks`, the heading the third message names.
- **`docs/de/signing.md:253`** writes "Der Abschnitt der Durchgänge (`## Passes`)", the English heading, where a German
  repository shows `## Durchgänge`. It was there before S1.

## Why

A refusal the table does not list leaves the person with the tool's words alone, and a German page that names an English
heading points them to a heading their repository does not show.

## Done when

- [ ] Section 5's table has a row for each of the eight, its cure the one the string names.
- [ ] `examples/de/shoalmark.toml`'s `[headings]` names `asks`.
- [ ] `docs/de/signing.md` names the heading a German repository shows.

## Ship log

| Date | Event |
|---|---|
| 2026-11-03 | Filed for v0.20.3, from S1's docs round. Records only. |
| 2026-11-04 | `epic: FM-139`: a chapter of v0.20.3's epic. Records only. |
