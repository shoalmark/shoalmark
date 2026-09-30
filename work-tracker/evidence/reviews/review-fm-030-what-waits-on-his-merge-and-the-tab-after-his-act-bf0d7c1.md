# Review — FM-030, the Owner's two raises of 2026-09-30: what waits on his merge, and the tab after his act (bf0d7c1)

Reviewed: bf0d7c172767ffa3bd3078b2ec536072c9cc0640

- Seat: reviewer-58 (session 8e509911/reviewer-58), worktree shoalmark-review-4, 2026-09-30 08:38–08:50 CEST. Range: `origin/main` 792dbca … bf0d7c1, one commit.
- Tier: docs, one pass, no suite run: FM-030's body (+3) and INDEX.md's generated date line (+1 −1), no `.py`, no front matter. Independence: same session.
- Verdict: READY WITH FINDINGS — three P3, RV-747 to RV-749, fixed forward; the docs tier takes no re-pass.

## Checks

1. His words, from this session's transcript (`type`, `timestamp` and text only). *It shows up on GitHub…* is a `queue-operation` enqueue plus a `queued_command`
   attachment at `06:26:03.846Z`: typed mid-turn, his prompt and not a relay, though not `user` as the brief expected. *This only shows…* is `user` at
   `06:30:15.168Z`; *file it* is `user` at `06:31:39.894Z`. Plus 2 h gives 08:26:03, 08:30:15 and 08:31:39, as filed. Quote 1 changes: *Board*/*A user*
   lowercased, `-` → `—`, `[Image #10]` dropped. Quote 2 changes: *User*/*Dialog* lowercased, the quote marks around *Done* dropped, *what* → *, which*,
   `-right` → ` — right`. No word of substance changed (quote 2's opening: RV-747). D3 holds: the added lines carry no relay citation and no hash (the one
   *auditor* is in the branch name `fm/024-the-auditor-s-…`), and each raise rests on one marked quotation of his.
2. The facts. The origin reflog shows `eedee1d` pushed at 06:56:16, with commit date 06:55:52. `origin/answer/fm-006` is `ff3e85a` (08:15:17, `%G?` G), PR 122's
   head. `shoalmark.py` equals main's. At the tip, `--owner` prints FM-006 under *ON THEIR WAY* as *done, on its way*; the acts filter
   `T.filter(t=>t[30].length&&!(t[31]&&!t[31][11]))` is at `shoalmark.py:2785`. The board's script has no `fetch`, `location.reload` or `setInterval`, so the
   open tab is stale by construction. The CHANGELOG's 0.18.6 section has *Right after the act, the page shows it* (line 119). The `--queue` row of 08:17:30
   cannot be reproduced now: he opened PR 123 at 08:23:44 (RV-748). *Cannot fetch* is confirmed in headless Chrome 154: a `file://` page's `fetch` of a sibling
   fails with TypeError, while a `<script src>` of a sibling loads, which is the slice's mechanism. Safari and Firefox were not tried.
3. The forms. Both raise lines take the 2026-09-28 form, ending *undermines: no signed rule —* a slice for 0.18.7, nothing built. They sit right after the
   12:43:02 line. `--triage` on a `cp -R` copy in scratch lists only FM-041, so FM-030 owes no pass. The ship-log row is the last row (oldest to newest). The
   front matter is byte-identical to main (`In Progress`, `next: build`). No other project's path or number is in the added lines. The freeze holds (`--check`:
   22 open). Two lines and one row meet its *one line* per raise; the row is the tracker's log, not a filing.
4. Gates. `--check` 0, `--session-check` 0, `git merge-tree --write-tree origin/main HEAD` clean (`23c4311`). `--queue` at 08:39:40 reads *branch fm/030-… @
   bf0d7c1 · wait: no pull request — no verdict on bf0d7c1*. The trailers are `Session: 8e509911`, `Worktree: shoalmark-principal-4` and `Co-Authored-By`. By
   the ratio rule: records +4 −1, product +0 −0. The −1 is INDEX's generated date line (the brief expected 0). This verdict adds records only.

## Findings

- RV-747 · P3 · 70 % — The 08:30:15 line drops his opening *True: [Image #11] - but* unmarked (an elision, not a normalisation) and says *two screenshots*
  where that message carries one (08:21:34's came at 08:26:03). The substance holds: *on their way: 1* carries his *True*. Fix forward: *in chat with a
  screenshot (taken 08:28:13; the one of 08:21:34 came at 08:26:03)*, and after the quotation *(normalised; his opening "True: … but" left out)*.
- RV-748 · P3 · 60 % — The 08:26:03 line reads as if `fm/024-…` still had no pull request. He opened PR 123 at 08:23:44 (holgo99, `createdAt` 06:23:44Z), after
  his screenshot and before his words. The gap holds, because the owed section has no pull-request row either. Fix forward: after *not on his board*, add
  *(he opened PR 123 from the forge at 08:23:44; the board carries no pull request either)*.
- RV-749 · P3 · 70 % — Neither 0.18.7 slice is in *Done when* or *What is true now*; the 12:43:02 raise got a Done-when bullet and 08:21:57's got a paragraph.
  A session reading what is left (AGENTS.md rule 5) misses them, and a close against *Done when* could leave them. Fix forward, two bullets under *Done when*:
  *The owed section carries what waits on his merge: the queue's rows that wait on him, a pull request to merge or a branch pushed without one, each with its
  verdict's word, as `--queue` prints them.* and *The open tab follows his act: the dialog's last step reloads the page, and a git-ignored stamp beside the
  board, loaded as a script every ten seconds, reloads it when it changes.*

Path 5 — a merge rules nothing.
