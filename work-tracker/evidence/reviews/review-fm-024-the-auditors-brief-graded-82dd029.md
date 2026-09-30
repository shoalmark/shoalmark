# Review — FM-024, the Auditor's change brief of 2026-09-30 graded and filed (82dd029)

Reviewed: 82dd0296b407d7f38e49c238636afbffc9fc9d49

- Seat: reviewer-57 (session 8e509911/reviewer-57), worktree shoalmark-review-4, 2026-09-30 06:52–06:58 CEST.
- Range: `origin/main` 792dbca … 82dd029, two commits (a9f19e8, 82dd029).
- Tier: docs (the diff is one tracker body plus the generated INDEX.md date line; no `.py`, `docs/`, `vendor/`). One pass.
- Independence: same session — the Reviewer is a sub-agent of the Principal session that authored the branch.
- Verdict: READY WITH FINDINGS — three P3, RV-717 to RV-719, fixed forward.

## Checks

1. Word for word. Ran `sha256sum` on the Principal's saved paste: `8e8f77ce…2c12`, five lines. Took lines 261–265 of the tracker, stripped `> `, and
   `cmp` against the paste: identical (same sha256). The hash is quoted in the section, the Raised line, and as `8e8f77ce…` in the ship-log row. The
   Raised line's and ship-log row's summaries carry no quote marks that pass as the Auditor's words. The Owner's word is marked normalised. Seen in this
   session's transcript, reading only `type`, `timestamp`, text: one `user` line, `2026-09-30T04:38:10.522Z` = 06:38:10 CEST, text *"lets file this. Work is
   postponed after another task that is waiting for you"* — matches the normalised form. The paste's stamp: one line with `04:11:21.648Z` (= 06:11:21) exists
   (count 1). Not seen: that line's content, so that it is the paste itself is taken from the stamp and the brief, not from the line.
2. Measured facts. Ran the measurement script at 06:53:40 (load 3.9 to 4.6). Main log: `cwd` takes exactly two values, the session's launch directory
   (15,175 turns) and one relaunch directory (158; filed 110), neither a seat worktree (the relaunch is the Owner's checkout). `message.model` 5,604 =
   `perTurnEffort` 5,604 (filed 5,587). Sub-agent logs 156 (filed 155); 68,904 turns carry the launch directory, as filed, plus 41 newer turns carry the
   relaunch directory (see RV-718). Sub-agent `message.model` fields 30,924. Codex rollouts 388 (filed 387); the newest carries `session_meta` 2 and
   `turn_context` 8, with model and effort. Every count is at or above the filed one. The inference holds: no log carries a seat worktree's `cwd`, so a
   worktree match finds nothing; the launch directory is carried by the parent and every sub-agent, so it finds all. The launch directory is not named in the
   tracker (grep of the file for the parent project: 0).
3. The table's claims. `git grep` finds `def board_sessions` at `origin/main:shoalmark.py:5462`. S1 (`seat.session`), S3 (`<parent>/<seat>-<n>`), S6
   (*independent* / *same session*) match slice 1's table. RV-724 on FM-041 says a code change was given one Reviewer pass and refuses it, as the cell says.
   AGENTS.md's two tiers name `shoalmark.py`, tests, configuration and hooks as code. The folded raise of 2026-09-28 asked for grouping without model and
   effort. `CODEX_THREAD_ID` is in the Asks record's point 3 (line 313). The cost line and *Postponed* are marked the Principal's.
4. The forms. The section sits at line 255, immediately before `## Raised` (headings otherwise unchanged). The Raised line has the form of the 2026-09-28
   line and ends `undermines: no signed rule`. `--triage` on a `cp -R` copy in scratch does not list FM-024. The ship-log row is the last row. Front matter
   is untouched (no diff hunk before line 252); FM-024 stays `In Progress`, `next: build`. The second commit's rewording is disclosed in its message and agrees
   with the ship-log row.
5. Gates. `--check` 0 (*judged before build: on — 2 commit(s) … every build commit under a judged In Progress tracker*; *guarded — 2 commit(s) … none
   changes them*); `--session-check` 0; `git merge-tree --write-tree origin/main HEAD` clean (exit 0). `--queue` at 06:55:20: the branch is "wait: no pull
   request — no verdict on 82dd029" (this verdict answers it). Both commits carry `Session: 8e509911`, `Worktree: shoalmark-principal-4`, `Co-Authored-By`.
   No suite was run: no `.py` change.

## Findings

- RV-717 · P3 · 90 % — the diff also holds `work-tracker/INDEX.md` (one line, `Generated 2026-09-29` to `2026-09-30`), a generated file the hook rewrites
  on the date change. The brief expected only the tracker; it is harmless and gates nothing. Fix forward: none needed; note it in the merge.
- RV-718 · P3 · 80 % — the cell says the sub-agents' turns all carry the parent's launch directory. Now 41 sub-agent turns carry the relaunch directory,
  the Owner's checkout, not a seat worktree. The inference and the P1 stand; the sentence is right for 06:4x and slightly loose after. Fix forward: say
  *the parent's launch or relaunch directory*.
- RV-719 · P3 · 60 % — the freeze's line is *one line into the closest open tracker's body*; a 30-line section is more than one line. It is a fold of one
  brief with the Owner's words and the grade beside them, disclosed as a fold, and adds no tracker or ask. A wording point: state in the section that it is
  the one place the brief is kept, so the freeze is read as met.

READY WITH FINDINGS. RV-717 to RV-719 are P3 and go forward; the docs tier takes no re-pass.

Path 5 — a merge rules nothing.
