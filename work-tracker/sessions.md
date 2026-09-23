# Sessions

One row per session of a seat: who convened it, for what, in which worktree. `--session open` writes a row and
`--session close` dates its end; the gate refuses a seat's commit whose `Session:` trailer names no open row here, or
whose worktree is open under another session. An open row with no commit for a day is closed by the next triage pass,
which says so.

| Session | Seat | Convened by | Scope | Worktree | Started | Ended |
|---|---|---|---|---|---|---|
| 8d6537be | implementer | the Principal session a9 | build 0.17.6 | shoalmark-impl | 2026-09-23 16:23 | — |
