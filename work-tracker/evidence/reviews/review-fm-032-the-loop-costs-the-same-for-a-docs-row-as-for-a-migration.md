# Review — FM-032 filed, at db15a31 (2026-09-24 09:46 CEST, Reviewer, session `8e509911/reviewer-1`)

**Scope.** `origin/main`…`db15a31`: four commits.
- `4af2c9b` and `af3adab`: the Implementer, under `8e509911/implementer-14`, which is opened and closed.
- `53e0456`: the principal seat's merge of `main` `4b472cc`, under `8e509911`.
- `db15a31`: the principal seat sets the proposal. This commit changes only the tracker: `next: owner`,
  `ask-proposal` and a ship-log row.

## Checked, and true

**The ask.**
- It is 298 characters and has one `?`, at its end.
- It has four options, and `ask-proposal: "all four now"` is option 1.

**The facts marked as re-derived are re-derived here from git.**
- **The three merges of `main` on PR 35.** `git merge-tree` on each merge's two parents gives:
  - `64f7b99` (08:58, the Implementer): `sessions.md` and `INDEX.md` conflict.
  - `f8ccf60` (09:07, the principal seat): `sessions.md` conflicts.
  - `3131e8c` (09:21, the principal seat): `sessions.md` and `INDEX.md` conflict.

  This is the table exactly, with the verdict that came before each merge. `5dcc854` (09:24) is PR 35's third
  verdict.
- **PR 35 itself:** 11 commits (6 Implementer, 3 Reviewer, 2 principal seat) and four files (the tracker, its review,
  `INDEX.md` and `sessions.md`).
- **The two code lines, at `9bde71f`:** `:2621` is `now_by_id = {r["id"]: r for r in rows}`, and `:2626` is the
  re-open test. My own FM-028 review cited `:2620` for the first of them, and `:2621` is right.
- **The session ids:**
  - `-12` has five commits, 08:57–09:00: an open, three of work (one of them the merge) and a close.
  - `-13` has three commits, 08:50–08:56.
  - `-14` is this filing, 09:31 and 09:35.
  - The principal seat's merges carry `8e509911`.
- **The open count.** 15 trackers were open before this filing, across `main` `9bde71f` and the heads of PR 34 and
  PR 35 (PR 34 is the only other open pull request). Their tags: 4 `bug` (FM-018, FM-028, FM-029, FM-030), 7
  `research`, 2 `process`, 1 `security`, 1 untagged.
- **The parent project's pull request 807, from the forge (read-only):**
  - 29 commits; all 10 of its files are under its `docs/work-tracker/`; merged at 08:50 CEST.
  - 11 of the commits are the Reviewer's: 8 on its own work, 7 of them before the last READY, and 3 on a second
    tracker.

**What is marked *reported* stays marked.** That covers:
- the seven passes;
- the two docs-only branches: the four token counts sum to 803K, which is "about 800K";
- the Principal's answer and its four catches.

**`considered:` holds.**
- The FM-031 paragraph describes FM-031's S1 and S2 as FM-031 has them. It says openly that S2 here replaces FM-031's
  S1.
- FM-024 keeps its core, the trailer. FM-027 becomes moot only under S2, and the body says so. FM-005 is only the
  channel.
- `--related FM-032` ranks FM-019 first. That tracker is shipped (a merge is judged as the merger's change), so it is
  not a home.
- The case for a tracker of its own is made honestly. What it measures is the cost of the loop per change, not the
  fan-out.

**No name of the parent project or of any consumer** is in the three files. Only two hex tokens in them do not resolve
in this repository: `8e509911` (the session root the registry already uses) and the one in R2.

**The merge `53e0456` brought only `main`'s files, the registry and INDEX.**
- FM-028's tracker and its review are byte-identical to `4b472cc`.
- The registry has 26 ids in 27 rows. The id set is the union of the two parents, in opened order, and no row is
  altered. Both closed `-6` rows stand.
- INDEX differs from `main`'s only by FM-032's row and the count.
- Replayed, this merge is clean: it is the one merge of `main` this morning that did not conflict.

**Gates at `db15a31`.**
- `--check` 0; `--session-check` 0; `test_shoalmark.py` 0 (264 ok); `test_core.py` 0 (148 ok).
- `origin/main` `4b472cc` is an ancestor, so the merge is a fast-forward.
- No commit message carries a pull-request number with the sign.

## Findings

**R1 · P3 · The follow-up that needed `-15` is not in the body.**
- The Implementer reports that after `-14` had closed, a one-merge follow-up needed a new id, `-15`. That session was
  made locally, dropped and never pushed.
- No remote ref carries `-15`, and the tracker does not mention it. It is the cleanest instance of *every return to a
  branch costs a new id*.
- It belongs under that bullet, marked *reported*, because only the Implementer saw it.

**R2 · P3 · A consumer's commit hash is in a shoalmark file.**
- `:29` names the parent project's last READY by its hash.
- The Owner's rule is that consumer state does not enter shoalmark, though numbers may. *The last READY* says the same
  without the pointer.

**R3 · P3 · The ask's freeze and S4 set different lines.**
- The ask says *until the open count falls*. S4 says *at or above a number the Owner sets*, and *each takes effect on
  the Owner's answer, never on a default*.
- So the proposal, *all four now*, sets no number, and S4 could not take effect without a second question.
- Either the ask names the line (15 before this filing), or S4 says that the count at the ruling is the line.

**R4 · P3 · Two open asks put the registry to the Owner in two designs.**
- FM-031's ask (`next: owner`) still proposes *S1 then S2*. Its S1 is one file per session with a committed,
  generated table.
- This tracker's S2 replaces that design, and argues that a committed generated file still conflicts.
- The body says so (*if both are ruled, they are one build*), but FM-031's ask does not. Answering both proposals would
  rule both designs.
- One line on FM-031, or in its ask, should say that its S1 waits on this ruling.

**R5 · P3 · A reported comparison mixes two windows.**
- *A filing rate inflated by a third (FM-031's first 16.4 a day, re-derived as 11.0)*: the 16.4 counted all 31
  filings over the 1.89-day window.
- Like for like, that window gives 13.8 (26 filings), so the inflation was about a fifth. The 11.0 is the 2.82-day
  window.
- It is marked *reported*, so this is wording, but the section's point is rigor.

**Verdict:** READY WITH FINDINGS. R1–R5 are all P3.

## Re-verified at 48f926e (2026-09-24 09:52 CEST)

**Scope.** `48f926e` is one commit by the principal seat, under `8e509911`. Against `4264e5c` it changes only the
FM-032 tracker. INDEX is unchanged, and `--check` agrees.
- The ask, its options and the proposal are unchanged: 298 characters and one `?`.
- The commit message carries no `#N`.
- No consumer name and no foreign hash is added.

**Closed.**
- **R1:** the `-15` instance is in the body, marked *reported by that Implementer*. R6 is about where it sits.
- **R2:** the parent's hash is gone, and *the last READY* stands in for it.
- **R3:** S4 names the line: **8**, half of today's 16. *All four now* carries it, and he may name another.
  - Note, not a finding: the ask he presses still does not show 8. It stands at 298 characters against `ASK_MAX`
    300 (`shoalmark.py:267`), so *below 8* would need a trim somewhere else in it.
- **R5:** *a fifth, like for like* (16.4 against 13.8 in the same window, 11.0 over the full window). 16.4 / 13.8 =
  1.19.
- **R4** is closed in part. The body now says how the two asks meet. R7 is what remains.

**Gates at `48f926e`.**
- `--check` 0; `--session-check` 0; `test_shoalmark.py` 0 (264 ok); `test_core.py` 0 (148 ok).
- `origin/main` `4b472cc` is an ancestor, so the merge is a fast-forward.

**R6 · P3 · The `-15` bullet sits outside the list it belongs to.**
- It is a top-level `- ` item, placed between the `-13` sub-item and the paragraph that continues the bullet *A
  closed row never re-opens* (*This filing is `-14` …*). In Markdown that paragraph now continues the `-15` bullet,
  and `-15` reads before `-14`.
- It is also the only top-level bullet there without a bold lead.
- The fix is to make it a third sub-item, after the `-14` sentence or with it.
- The new body lines, 54, 94 and 153, are not wrapped at 120 as the rest of the file is.

**R7 · P3 · R4's remainder: an answer to FM-031 is read as a ruling on this S2.**
- The sentence *builds S2 if FM-031's S1 is ruled* would build this tracker's S2 on an answer to FM-031's ask. That S2
  is a report from the trailers, without `--session open`/`close` and without two refusals, while FM-031's S1 is
  per-session files.
- FM-031's own text is unchanged, so the reading lives only here.
- If he then answers this ask *the registry later* or *none*, the text does not say which answer stands.
- Either FM-031 gets one line saying that its S1 waits on this ruling, or the clause goes, so that a ruled FM-031 S1
  waits for this ask.

**Verdict:** READY WITH FINDINGS. R6 and R7 are P3. R1, R2, R3 and R5 are closed, and R4 is closed in part.

**Correction to R6 (2026-09-24 09:52 CEST).** The unwrapped new body lines are 54, 75, 94 and 149, not *54, 94 and 153*. I wrote the
numbers before I measured them. The verdict is unchanged.
