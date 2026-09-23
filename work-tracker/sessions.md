# Sessions

One row per session of a seat: who convened it, for what, in which worktree. `--session open` writes a row and
`--session close` dates its end; the gate refuses a seat's commit whose `Session:` trailer names no open row here, or
whose worktree is open under another session. An open row with no commit for a day is closed by the next triage pass,
which says so.

| Session | Seat | Convened by | Scope | Worktree | Started | Ended |
|---|---|---|---|---|---|---|
| 8d6537be | implementer | session 8e509911 (written *the Principal session a9* until 2026-09-23 18:20 — one name for a session) | build 0.17.6 | shoalmark-impl | 2026-09-23 16:23 | 2026-09-23 17:24 — re-opened as 8e509911/implementer-1: the parent's id was known |
| 8e509911/reviewer-1 | reviewer | session 8e509911 (written *the Principal session a9* until 2026-09-23 18:20 — one name for a session) | attack 0.17.6 | shoalmark-research | 2026-09-23 17:16 | — |
| 8e509911/implementer-1 | implementer | session 8e509911 | build 0.17.6 | shoalmark-impl | 2026-09-23 17:24 | 2026-09-23 18:47 |
| 8e509911/implementer-2 | implementer | session 8e509911 | build 0.17.7 | shoalmark-impl | 2026-09-23 18:47 | 2026-09-23 20:11 |
| 8e509911 | principal | the Owner, 2026-09-23 12:21 | the day's findings into the tool; releases 0.17.5-0.17.7, the first triage pass, FM-023/FM-024 | shoalmark-principal | 2026-09-23 19:14 | — |
| 8e509911/implementer-3 | implementer | session 8e509911 | build 0.17.8 | shoalmark-impl | 2026-09-23 20:11 | 2026-09-23 21:40 |
| 8e509911/implementer-4 | implementer | session 8e509911 | the human pages open from a file | shoalmark-impl | 2026-09-23 21:40 | — |
| ee61f1fe | gtm | the Owner, 2026-09-23 22:02 | screen the owner-facing claim | shoalmark-gtm | 2026-09-23 22:02 | 2026-09-23 22:12 |
| 2ab3afad | gtm | the Owner, 2026-09-23 22:24 | second pass: Owner vs Eigner, leistungsstärkeren vs besseren, the second claim beside the new bar (the harness session of ee61f1fe; an id is used once) | shoalmark-gtm | 2026-09-23 22:24 | 2026-09-23 22:33 |
| c1652143 | gtm | the Owner, 2026-09-23 22:40 | the Jev gate test: 17 lines x 6 gates, run twice | shoalmark-gtm | 2026-09-23 22:40 | 2026-09-23 22:52 |
| ad81b142 | gtm | the Owner, 2026-09-23 22:57 | the German claim re-provoked: twelve new German lines, no translations | shoalmark-gtm | 2026-09-23 22:57 | 2026-09-23 22:58 |
| d578f49e | gtm | the Owner, 2026-09-23 22:59 | the survivors re-read for the stated reader: a German tech investor, English-fluent | shoalmark-gtm | 2026-09-23 22:59 | 2026-09-23 22:59 |
| 63f5b126 | gtm | the Owner, 2026-09-23 23:06 | both readers per line, and what would be data | shoalmark-gtm | 2026-09-23 23:06 | 2026-09-23 23:06 |
| e0be0fa0 | gtm | the Owner, 2026-09-23 23:28 | the pitch on main verified; the mark: wordmark and icon screen | shoalmark-gtm | 2026-09-23 23:28 | 2026-09-23 23:46 |
| 8e509911/implementer-5 | implementer | session 8e509911 | the Pricke drawn to be looked at | shoalmark-impl-2 | 2026-09-23 23:59 | 2026-09-24 00:43 |
| 8e509911/implementer-6 | implementer | session 8e509911 | the site wears the Pricke | shoalmark-impl-2 | 2026-09-24 01:02 | 2026-09-24 01:14 |
