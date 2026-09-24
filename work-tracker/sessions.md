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
| 8e509911/implementer-4 | implementer | session 8e509911 | the human pages open from a file | shoalmark-impl | 2026-09-23 21:40 | 2026-09-24 07:41 |
| ee61f1fe | gtm | the Owner, 2026-09-23 22:02 | screen the owner-facing claim | shoalmark-gtm | 2026-09-23 22:02 | 2026-09-23 22:12 |
| 2ab3afad | gtm | the Owner, 2026-09-23 22:24 | second pass: Owner vs Eigner, leistungsstärkeren vs besseren, the second claim beside the new bar (the harness session of ee61f1fe; an id is used once) | shoalmark-gtm | 2026-09-23 22:24 | 2026-09-23 22:33 |
| c1652143 | gtm | the Owner, 2026-09-23 22:40 | the Jev gate test: 17 lines x 6 gates, run twice | shoalmark-gtm | 2026-09-23 22:40 | 2026-09-23 22:52 |
| ad81b142 | gtm | the Owner, 2026-09-23 22:57 | the German claim re-provoked: twelve new German lines, no translations | shoalmark-gtm | 2026-09-23 22:57 | 2026-09-23 22:58 |
| d578f49e | gtm | the Owner, 2026-09-23 22:59 | the survivors re-read for the stated reader: a German tech investor, English-fluent | shoalmark-gtm | 2026-09-23 22:59 | 2026-09-23 22:59 |
| 63f5b126 | gtm | the Owner, 2026-09-23 23:06 | both readers per line, and what would be data | shoalmark-gtm | 2026-09-23 23:06 | 2026-09-23 23:06 |
| e0be0fa0 | gtm | the Owner, 2026-09-23 23:28 | the pitch on main verified; the mark: wordmark and icon screen | shoalmark-gtm | 2026-09-23 23:28 | 2026-09-23 23:46 |
| 8e509911/implementer-5 | implementer | session 8e509911 | the Pricke drawn to be looked at | shoalmark-impl-2 | 2026-09-23 23:59 | 2026-09-24 00:43 |
| 8e509911/implementer-6 | implementer | session 8e509911 | the site wears the Pricke | shoalmark-impl-2 | 2026-09-24 01:02 | 2026-09-24 01:14 |
| 8e509911/implementer-7 | implementer | session 8e509911 | the lockup at 1×, 2×, 4× | shoalmark-impl-2 | 2026-09-24 07:11 | 2026-09-24 07:18 |
| 8e509911/implementer-8 | implementer | session 8e509911 | the dark-ink fix on the site slice | shoalmark-impl-2 | 2026-09-24 07:34 | 2026-09-24 07:35 |
| 6cecddb3 | gtm | the Owner, 2026-09-24 07:35 | the mark screen's outcome recorded; the tagline with the Pricke drafted | shoalmark-gtm | 2026-09-24 07:35 | 2026-09-24 07:36 |
| 8e509911/implementer-6 | implementer | session 8e509911 | file FM-028 (the clock); FM-011 to Shipped. id guessed on a branch — the same id names the session *the site wears the Pricke* in PR #33/#37 (FM-027's class); recorded, not renamed: the registry is append-only (FM-024); f9a7e49's trailer carries it; closed by the Principal's ruling so the merged registry reads closed → closed | shoalmark-impl | 2026-09-24 07:41 | 2026-09-24 08:49 |
| 8e509911/implementer-9 | implementer | session 8e509911 | the tagline D2 as its own slice | shoalmark-impl-2 | 2026-09-24 07:48 | — |
| 0cbdba3f | gtm | the Owner, 2026-09-24 07:50 | the tagline's English ruled: D2 with Pricke | shoalmark-gtm | 2026-09-24 07:50 | 2026-09-24 07:50 |
| 8e509911/implementer-10 | implementer | the Owner, 2026-09-24 08:24, in session 8e509911 | filing: can the Owner keep up with parallel streams | shoalmark-impl-3 | 2026-09-24 08:24 | 2026-09-24 08:26 |
| 8e509911/implementer-11 | implementer | session 8e509911 | FM-031 adopted by the Principal: the ask drafted, the slices named | shoalmark-impl-3 | 2026-09-24 08:32 | 2026-09-24 08:36 |
| 8e509911/implementer-12 | implementer | session 8e509911 | PR #35: FM-028's R1 (the collided session id) and R2; main merged in | shoalmark-impl-4 | 2026-09-24 08:33 | 2026-09-24 09:00 |
| 8e509911/implementer-13 | implementer | session 8e509911 | FM-031 NOT READY at 3c72e84: the Reviewer's R1-R4 fixed | shoalmark-impl-3 | 2026-09-24 08:50 | 2026-09-24 08:56 |
| e8e309df | principal | the Owner, 2026-09-24 | file FM-029 and FM-030 on the replaced chain; its review | shoalmark-principal-2 | 2026-09-24 10:19 | — |
| e8e309df/reviewer-7 | reviewer | session e8e309df | review the replaced FM-029/FM-030 chain at 97e9acc | shoalmark-review-e8 | 2026-09-24 10:22 | — |
