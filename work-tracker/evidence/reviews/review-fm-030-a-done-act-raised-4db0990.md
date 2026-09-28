# Review — FM-030, a done act has no button for the next one, raised, at 4db0990 (2026-09-28 08:38 CEST, Reviewer, session `8e509911/reviewer-45`)

- **Branch:** `fm/030-a-done-act-has-no-button-for-the-next-raised`, tip `4db0990`
  (`4db0990e3384b822c92450467ee9f345a764ac91`, confirmed by `git ls-remote`). It sits on `origin/main` `02f3c5c` and
  carries two Principal commits (`principal@seat`, `Session: 8e509911`, `Worktree: shoalmark-principal-4`):
  - `4737eb8`, 08:25:38 — the raise line, the next slice under *What is true now*, and a ship-log row, with the
    paste's time left empty in all three;
  - `4db0990`, 08:27:25 — fills in 08:21:57. The first commit's subject still reads *"(the Auditor through the
    Owner, )"*, and the second commit's body discloses it.

  Together they change FM-030's file only: 9 lines in.
- **Tier: docs, one pass.** `git diff origin/main 4db0990 -- shoalmark.py test_*.py lefthook.yml scripts/` is empty.
  The tool, suites and hook are main's, so no suite was run.
- **Independence:** same session — a sub-agent of 8e509911, reported.
- **Verdict: READY WITH FINDINGS.** There are two P3s, RV-722 and RV-723, from the range the Principal allocated.

## What I ran

| run | result |
|---|---|
| the quoted sentence against the saved paste | `owner-auditor-keychain-hour-and-fm030-board-gap-paste.md` (the Principal's copy) hashes to `f7d230ae…b0fd`, the sha256 the line cites. It has three lines: the *To:* header, a point 1 and a point 2. The sentence in italics equals point 2 with its list marker `2. ` removed, character for character, and the header is named as the paste's heading. Point 1 is not in the tracker (RV-723). I quote nothing from the paste beyond what the tracker quotes |
| the time 08:21:57 against the Principal's transcript | ✓ The queued command that carries the paste is a `queue-operation` `enqueue` at `2026-09-28T06:21:57.975Z`, which is 08:21:57 CEST. Its text contains the saved paste's three lines byte for byte, as its lines 2–4; its line 1 and lines 5–7 are not in the saved copy, which fits *the part addressed to another session left out on his word* |
| the code claim, at `02f3c5c` | ✓ `act_of` (3684–3701) returns `None` when `t.get("done")`, and its docstring says *"`done:` closes it; closed work owes nothing"*. `due_cmd` (5325) says *"On a tracker whose act was done, it is a new act: `done:` leaves the front matter"*. The Auditor's own numbers, `:3509` and `:5063`, are PortDive's vendored 0.18.5 (`tools/shoalmark/shoalmark.py` at `60e6d1a7`): `def act_of` and that same docstring line |
| the raise line, `raise_lines` | Imported in a scratch clone at `4db0990`: date `2026-09-28`, and undermines `["no signed rule — a design gap of this tracker's board; built as its next slice", "not a new filing"]`. Neither names a signed rule, so `mark_raised` gives `[]`. FM-030 is owed a pass only as In Progress, by status, and its `triaged:` is 2026-09-27 |
| `--triage` (the scratch clone) | *"A triage pass — 0 trackers to judge"*; *"Applied nothing — no new filled rows"*; the tree is unchanged |
| the next slice | It sits under *What is true now*, as the commit says, and names the board branch it follows, `fm/030-the-board-reads-his-unmerged-acts` (`ada15c6` on the forge). It builds nothing and asks nothing |
| `--check` on `4db0990` | exit 0. *INDEX.md is up to date — 40 trackers*; *judged before build: on — 2 commit(s) … every build commit under a judged In Progress tracker*; *the Owner's two sections: guarded*; *filing freeze: 21 open* |
| `--session-check` | exit 0 |
| `git merge-tree --write-tree origin/main 4db0990` | clean. Its tree `5b42a56` is the branch's own, so the merge is a fast-forward |
| `git diff --check` | clean |
| `--queue` (the scratch clone) | `branch fm/030-a-done-act-has-no-button… @ 4db0990  wait: no pull request — no verdict on 4db0990` and `branch fm/030-the-board-reads-his-unme… @ ada15c6  wait: no pull request — no verdict on ada15c6`; *2 waiting on you: 0 merge, 0 close, 0 wait, 2 pushed without a pull request* |

## Findings

**RV-722 · P3 · confidence 90 % — the new ship-log row is first in a table that runs oldest first.** FM-030's ship log
goes from 2026-09-24 down to the 2026-09-27 row of the Reviewer's pass on `9c96f5b`. The 2026-09-28 row went in above
the first 2026-09-24 row. So the newest event reads as the oldest, and the next seat that appends at the end splits
the day.

**Fix forward:** move the row to the end of the table, after the 2026-09-27 row that begins *"The Reviewer's pass on
`9c96f5b`"*.

**RV-723 · P3 · confidence 80 % — "filed word for word, three lines" describes the saved paste, not what is filed.**
- The three lines and the sha256 `f7d230ae…` are those of the Principal's saved copy: the header, point 1 and point 2.
- The record quotes point 2 only, without its `2. `, and names the header.
- Point 1 is not in FM-030. It is not said where it went, or that it is not this tracker's.

So a reader cannot check the hash against anything in the record, and *filed word for word* is true of one of the
three lines.

**Fix forward:** make it read *"(his paste headed *To: …*, three lines, sha256 `f7d2…` of the three; its point 2 quoted
here word for word; its point 1 is not this tracker's and is not filed here; the part addressed to another session
left out on his word)"*.

**Not a finding:** `4737eb8`'s subject keeps its empty time, *"(the Auditor through the Owner, )"*. A pushed subject
cannot be changed without a rewrite, and `4db0990`'s body names the miss and gives the time.

## Verdict

**READY WITH FINDINGS.** RV-722 and RV-723 are P3, to be fixed forward. The docs tier takes no re-pass.

The Owner lands this by merging; a merge rules nothing.
