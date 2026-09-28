# Review — FM-018, FM-030, FM-040: his three pastes of 12:43–12:50 recorded, at 3a417db (2026-09-28 13:17 CEST, Reviewer, session `8e509911/reviewer-48`)

Reviewed: 3a417dbe2e29a5e83969860e1b424005a8e61b9c
Session: 8e509911/reviewer-48

- **Scope.** `3a417db` is one commit on main `9e9fcb33`, on `fm/018-his-two-dashboard-requirements-meet-the-freeze`. It was
  committed by the Principal at 12:59:13 +0200 (the commit object's date). My fetch at 13:03:19 showed the branch at that sha,
  and HEAD in `shoalmark-review-2` was the same. It changes three tracker files, +25/−1: FM-018, FM-030 and FM-040. It changes
  no `.py` file, nothing in `vendor/` or `docs/`, and not INDEX.md.
- **Tier: docs.** No suite was run, because no `.py` file changed: `git diff --name-only origin/main...HEAD` lists only the
  three `work-tracker/*.md` files.
- **Independence:** same session. I am a sub-agent of 8e509911, the session that wrote the commit.
- **Verdict: NOT READY.** There is one P2, RV-755, which is in the ask he answers. RV-756 to RV-759 are P3. I used the ids
  RV-755…759, the range the Principal allocated.

## Checks

| check | what I ran | result |
|---|---|---|
| The pastes' hashes | `shasum -a 256` on the Principal's three saved copies, beside the brief | `4a6f20c8…a7a` (6 lines), `dd56f6a2…946` (7 lines), `436b4c6a…4d0` (2 lines). Each equals the sha256 the trackers cite |
| The quotes, byte for byte | `grep -F` of each quoted span, with its italics markers, in the tracker that carries it. A span that runs over several lines of a paste is joined with one space per line break | Every span is found. **FM-018 12:43:02:** the *To:* line; *The Owner's requirements for the dashboard*; his normalised sentence with its quotation marks; lines 4–6 as one span (526 bytes). **FM-018 12:50:35:** the *To:* line; line 2 whole. **FM-030:** the *To:* line; line 3 (item 1) whole; *File and rank them your way.* **FM-040:** the *To:* line; lines 2–7 as one span (948 bytes, the em dashes included). Apart from the joined line breaks, nothing differs |
| What is quoted and what is only hashed (RV-723's lesson) | Read against the pastes | Each line says which part it quotes. FM-018: *items 2 and 3 and his last line*, and it quotes the header and his sentence. FM-030: *item 1 alone*. FM-040 and FM-018 12:50:35: *quoted whole*, with the *To:* line given as the heading. FM-018 marks his sentence as the Auditor's normalisation. RV-758 covers two places where the Owner's and the Auditor's words are not kept apart |
| The stamps 12:43:02, 12:49:43, 12:50:35 | Not checkable | I cannot see the transcript's enqueue lines. The saved copies' mtimes are 12:44:49, 12:51:33 and 12:51:34, each after its stamp. That fits the stamps but does not prove them |
| `act.done.hint`, main `9e9fcb33` | `git show 9e9fcb33:shoalmark.py`, line 2506 | *the path to the result, or where it is* ✓ |
| `changed_paths`, `dirty_refusal` at `9e9fcb33` | The same file, `grep -n` | The facts hold: `git status --porcelain -z --untracked-files=no`; `dirty_refusal` lists every changed path; no line in either names a submodule or its fix. The line numbers do not hold: see **RV-756** |
| `shoalmark.toml` line 4; `shoalmark.py` :69–75; :365 | `git show 9e9fcb33:…` | line 4 is `freeze_at = 8`, and its comment names FM-032 S4 and *all four now* ✓. At :69–75, the freeze's comment, `"freeze_at": 0` and `"freeze_tag": "bug"` ✓. At :365, *`<ISO time> · <a path or a pointer>`* ✓ |
| PortDive's pinned copy | `git show a42ac134:tools/shoalmark/shoalmark.py` in `worktrees/principal-2`, without a fetch; its VERSION is 0.18.5 | :2417 *a path in the repository, or where the result is* ✓. :5024 `tid, where = words[0].upper(), " ".join(" ".join(words[1:]).split())…`, the `where` join ✓ |
| FM-032 S4's authority; FM-032's exchange is occupied | FM-032 on this branch | `## Asks`: *answered — accepted - all four now · holgo99* (2026-09-24, `ffa63b8`, PR 44) ✓. Front matter: `answer:` accepted S5, `answered: 2026-09-28`, `next: build` ✓ |
| The related trackers named in FM-018's raise line | `grep` of their front matter | FM-013 is Shipped, FM-002 is Shipped, and FM-004 is In Progress with `tags: research` ✓. I did not re-run `--related`, so its scores are unproven |
| PR 103 | `git log` on main | `bbbfc0b Merge pull request #103 from holgo99/fm/030-the-done-dialog-shows-the-question` ✓ |
| The raise lines' form | Read; `raise_lines` at :700 | Each line is `- <date> <time> · <who> · <fact> · <source> · undermines: no signed rule — …`, as FM-030's earlier lines are ✓ |
| None owed a pass | `python3 shoalmark.py --triage` on a scratch copy of 3a417db (13:11:27–13:11:56, load 3.67), never in the worktree | No row is marked RAISED. FM-018 and FM-030 are not on the worksheet. FM-040 is there only as its earlier NEW FILING row. `mark_raised` (:2121) needs `path N` or `<ID>'s answer`, and none of the four `undermines:` values names either. The command exited 4 because the copy cannot verify signatures (its allowed-signers file is unset). **It applied one verdict**, which is noted below under *Outside this diff* |
| The ask's fields (FM-018) | `sed`/`awk` on the front matter | `ask-kind: ruling`, `ask-since: 2026-09-28`, `next: owner`. `ask-options:` holds three options split by ` \| ` (*lift*, *fold*, *hold*), and none opens with yes or no. `ask-proposal:` equals option 1 byte for byte ✓ |
| Ship-log placement | Read | FM-018's table is newest first, and the row is at the top ✓. FM-030's and FM-040's tables run oldest to newest, and each row is appended last ✓ |
| New sections | Read, each file whole | FM-018: a Done-when bullet after the seven-points bullet, and `## Raised` before `## Ship log` ✓. FM-040: `## Raised` after *Done when* ✓. FM-030: the Done-when slice is appended last ✓ |
| `--check` | `python3 shoalmark.py --check` in the worktree (13:10:33–13:11:05, load 4.95) | Exit 0. *INDEX.md is up to date — 41 trackers*; *filing freeze: 22 open, at or above 8 — only bug filings*; judged before build and the Owner's two sections are both guarded. The tree was clean afterwards |
| `--session-check` | Same place (13:11:05–13:11:06) | Exit 0, no output |
| Merge | `git merge-tree --write-tree origin/main HEAD` | Clean. Its tree `1415ec6` is HEAD's own, and origin/main is an ancestor, so the merge is a fast-forward. `git diff --check` is clean |
| `--queue` | The scratch copy, started 13:13:25 at load 5.04 | *branch fm/018-his-two-dashboard-requir… @ 3a417db  wait: no pull request — no verdict on 3a417db* |
| The commit | `git log -1` | `Session: 8e509911` and `Worktree: shoalmark-review-2`. The body discloses the worktree: *committed from shoalmark-review-2 while shoalmark-principal-4 runs the board build's suites* ✓ |

## Findings

**RV-755 · P2 · confidence 75 % — the ask does not say what each option does to his rule, and option 1 reads narrower than it
is.**
- The freeze as built, his S4, already names two routes for a filing that is not a bug. `--new`'s refusal (:6229–6231) and
  `--schema` (:3731–3734) both say *anything else goes as one line into the closest open tracker's body, or waits*. Options 2
  (*fold*) and 3 (*hold*) are those two routes, but the ask does not say that they are his rule as written.
- Option 1 is the only option that changes his rule, and its words make the change sound smaller than it is:
  - `filing_freeze` (:6183–6188) compares the open count with `freeze_at` and nothing else. The raise line itself says the
    freeze *checks no identity*. With `freeze_at` at 24 and 22 open, any feature filing from any seat passes until 24 are open,
    not only these two.
  - The number stays at 24 after both are filed. Once trackers close, features can be filed again up to 24, so his 8 is gone
    until he sets it back.
  - *Lift for them* and *the freeze holds again at 24* say neither of these things. Read quickly, they sound like a one-time
    exception.
- **Fix, in the Principal's words:**
  - Option 1 says that it moves his number from 8 to 24 until he sets it back, and that any feature passes while fewer than 24
    are open. Or it names how the number returns to 8, for example `freeze_at = 8` in the commit after the two filings.
  - Options 2 and 3 say that they are the freeze's own two routes.
  - The proposal may stay option 1. The ask is re-put before he answers.

**RV-756 · P3 · confidence 99 % — the line numbers in FM-018's 12:50:35 line are another commit's.** The line says *checked
by the Principal at `9e9fcb33`: `changed_paths` (:2196) … `dirty_refusal` (:2209)*.
- At `9e9fcb33`, `changed_paths` is at :2018, with its `git status` call at :2021, and `dirty_refusal` is at :2031.
- :2196 and :2209 are the same two functions at `6e566c14`, the tip of `origin/fm/030-the-board-reads-his-unmerged-acts`. I
  checked all 15 remote branches, and that is the only one where `changed_paths` sits at 2196.
- The facts are right; only the anchors are wrong. **Fix:** :2018 (:2021) and :2031, or name `6e566c14`.

**RV-757 · P3 · confidence 70 % — FM-040: the build's order and its Done when disagree.**
- The raise line's reading and the new ship-log row say the build *takes points 2 and 3 first*, with point 1 measured before
  it.
- The body (the clause after the measurement) and *Done when* still define the fix as two slices:
  - **(a)** the pre-commit writes INDEX.md without building the HTML board;
  - **(b)** `verdict_reports` is cached, or read in one batch.
- Point 2 is (b). Point 3 is neither: running `--html-only` in the background with a temp-file rename is not (a). Point 3 is
  not in *Done when*, and the new lines do not mention slice (a).
- A builder cannot tell whether point 3 joins the fix, replaces (a), or is relief outside *Done when*. **Fix:** one clause
  that says which.

**RV-758 · P3 · confidence 60 % — two places where the Owner's words and the Auditor's are not kept apart.**
- **(a) The paste's last line.** FM-018 (*his last line*) and FM-030 (*his closing line*) give *File and rank them your
  way.* to the Owner.
  - The paste is the Auditor's message to the Principal: its *To:* line says so, it speaks of *The Owner's requirements* in
    the third person, and it addresses *your way* to the Principal. The only words it marks as his are the normalised
    sentence.
  - Who wrote the last line cannot be read from the paste. "The paste's last line" says only what is known.
- **(b) His words in FM-040's quote.** The quote carries his words, *"`waiting: tracker-dashboard` is painful"*, inside the
  Auditor's text. Nothing marks them as the Auditor's rendering, as FM-018 marks his sentence (*as the Auditor normalised
  them*).
- **Fix:** *the paste's last line*; and in FM-040, *his words in it as the Auditor gives them*.

**RV-759 · P3 · confidence 70 % — after his answer, FM-018's `next:` becomes `build`, and the record does not say what it
returns to.**
- Before this commit, FM-018 read `next: wait`. Its own design is unruled (*the Owner rules*; the first bullet of *Done
  when*).
- `--answer` on a ruling writes `next: build` whichever option he takes: `ANSWER_MOVE` (:290), written at :1577.
- Under *lift* and *hold*, nothing on FM-018 is buildable, and only *fold* gives it work. The ask and the ship-log row do not
  say what the seat sets afterwards.
- **Fix:** one clause, for example: *after his answer, `next: wait` again, or `build` for the folded slices*.

**Notes, no id.**
- The quotes keep the pastes' raw `<ID>`, `<id>` and `<path>` inside italics. A Markdown renderer that strips unknown tags
  hides them. The body's merged FM-016 text does the same (*because <id> shows*), and the bytes must stay as pasted.
  Confidence 60 %.
- The Principal's spawn message gives the commit time as 13:00:19. The commit object says 12:59:13 +0200.

**Outside this diff (no id minted; for the Principal to route), confidence 80 %.** On the scratch copy of `3a417db`, `--triage`
printed *Applied 1: FM-027: keep P3 owner*.
- It rewrote FM-027's `next: build`, which was written by the Owner's signed answer `4e63cbf` at 08:13:09, back to
  `next: owner`.
- The 2026-09-28 worksheet row re-applies over the answer that came after it. This branch touches neither FM-027 nor the
  worksheet, so any seat that runs `--triage` today in a real checkout would do the same.

**A disclosure of my own.** My first `--queue` attempt started at 13:12:37 at a 1-minute load of 6.93, which is over the brief's
6. It ran 2 s and failed on an https fetch in the copy. At about 13:17 I also started an empty `python3 -` by mistake; it had no script. Every other Python run waited for a load under 6.

## Verdict

**NOT READY.** RV-755 (P2) needs the ask's options fixed before he answers. RV-756 to RV-759 are P3, to be fixed forward or
closed in the re-check.

path 5 — a merge rules nothing.
