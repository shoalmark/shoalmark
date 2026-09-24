# Review — FM-031 ruled at b61c171: the answer cleared, the nine stand, two lines for 0.18.4 (2026-09-24 22:08 CEST, Reviewer, session `8e509911/reviewer-5`)

**Scope.** `fm/031-the-nine-rules-ruled-and-the-answer-cleared` at `b61c171` (`b61c171feae0f3449ce6c6e367c56c2477f394ae`),
on `main` `a77798b` (PRs 61–63 merged). **One commit**, by the Principal seat under `8e509911`, 21:53:38 — not two: the
clear and the hand edits are folded into it (check 1). `git diff --name-only origin/main...HEAD`: FM-030 and FM-031 under
`work-tracker/`, nothing else. **Tier: docs, one pass** (FM-032's tiers): below P2 fixed forward, a P2 sends it back. The
front-matter lines it removes are `--clear-ask`'s own work on one tracker's values, not a key the gate reads — the tier
the raise at `0f0766e` was reviewed under for its `--clear-ask FM-033 build`.

**What I ran.** `--clear-ask FM-031 wait` on a scratch copy of `a77798b` (a `git archive` in the scratchpad), `diff -u`
against the tip; a script comparing the nine rules and the ship logs of `a77798b` and `b61c171`; `git show` on `eef0c2e`,
`a3ff174`, `97fa87a`, `636f56e`; `gh pr list` and the forge's event feed; `--check`, `--session-check`,
`python3 shoalmark.py`, `--print-written`, `git merge-tree --write-tree`, both suites.

## The five checks

1. **The clear — true, 97%.** There is no first commit: the branch is `b61c171` alone. The replay of `--clear-ask FM-031
   wait` on `a77798b` matches the tip byte for byte in everything the tool writes: the eight lines `ask:` `ask-kind:`
   `ask-since:` `ask-options:` `ask-proposal:` `answer:` `answered:` `answered-by:` gone, `next: owner` → `next: wait`,
   and under `## Asks`, newest last: *2026-09-24 · Which rules hold … you stopped?* / *answered — accepted - the nine hold
   as written · holgo99* / *relation — accepted the proposal*. What differs is only the hand's work, below: the heading,
   the section's first and last sentence, two ship-log rows (and FM-030's row, a file the tool does not touch). Not a
   finding: no house rule gives the generator its own commit (`fd6ddd2` and `8eaff7d` folded a clear into other work;
   `ad37f41` did not), and the replay separates the two exactly.
2. **The ruling's text and the rows — true, 95%.**
   - *## Open — …* is now *## Ruled — the rules for a message between two sessions*, opening *Ruled 2026-09-24 21:29:12
     by the Owner's signed answer `eef0c2e` (PR 62): the nine hold as written — the proposal, the first of two.*
     `git show eef0c2e`: holgo99, 21:29:12 +0200, a good signature (`G`, `SHA256:uNcUULP2…`), three lines added under
     `ask-proposal: "the nine hold as written"`, options *the nine hold as written | until one is ruled, …* — option 1
     of 2. PR 62 is `answer/fm-031`: `eef0c2e` then the Reviewer's `1fcc1dc` (READY, 21:47:07), merged `a77798b`.
   - **The nine rules are unchanged:** the numbered list from *1.* to the end of rule 9 is identical in `a77798b` and
     `b61c171` (1,215 characters; nine items). Only *None is signed. As proposed, for the Owner's ruling — the ask
     above:* became *Signed as written, the nine:*.
   - **Two rows appended to FM-031's ship log, none edited:** its 11 rows on `main` are the first 11 of 13 on the tip,
     unchanged and in order. Row 12, the ruling. Row 13, the queue: `pushed_branches` on `main` (`shoalmark.py:977–1011`)
     drops every head with `name.startswith("answer/")` (`:1002`), named in its docstring and in `636f56e`'s message —
     by design, as the row says. With no pull request open, three `answer/*` heads read as nothing, so the count line is
     *0 waiting on you: …* (`queue_lines`, `:1159`) — consistent with the code, not observed (below).
   - **One row appended to FM-030's ship log**, the only line FM-030 changes. The code cuts at 60: `-m f"{tid}:
     {answer[:60]}"` (`:1335`). PR 61's subject is cut mid-word: *FM-032: accepted - one Reviewer docs pass until
     FM-007's hardware ke*, while `answer:` carries all 129 characters. Two precisions: R1 and R2.
3. **Path 5 — true, 97%.** The ruling cited is the signed commit at its own clock (21:29:12), never the merge
   (21:51:42). PR 62 is named as its carrier. *Waits on his press* in row 13 is landing, not ruling. Nothing reads a
   merge, a chat or a pull request as an answer. The *Principal's word in chat* in row 13 is a fact about when the pull
   requests were opened, not a ruling.
4. **The gates — true, 99%.** On `b61c171`: `--check` 0 (INDEX up to date, 34 trackers; the freeze holds at 18 open),
   `--session-check` 0. `python3 shoalmark.py` and `--print-written` leave `git status --porcelain` empty.
   `git merge-tree --write-tree origin/main HEAD` writes `e4e649e`, `b61c171`'s own tree: a clean fast-forward (the
   merge base is `a77798b`). `test_shoalmark.py` 0 (355 ok), `test_core.py` 0 (148 ok). The commit message names *PR 62*
   without the sign.
5. **Times — true but one, 95%.** Each time is sourced:
   - *21:29:12* is `eef0c2e`'s clock.
   - *19:53* is `a3ff174`, 19:53:41, the commit that recorded the nine as open.
   - *21:27–21:32* are the three answers' clocks: `64f843e` 21:27:24, `eef0c2e` 21:29:12, `97fa87a` 21:32:35.
     `--answer` pushes in the same run, and the forge made `answer/fm-024` at 21:27:33.
   - *21:44* is the forge's `createdAt` for PRs 61, 62 and 63: 21:44:29, 21:44:36 and 21:44:43.

   One is approximated: *21:4x* (R1).

## Findings

**R1 · P3 · 95% · FM-030's new row approximates a time that has a source.** *(the Reviewer's observation on the answer
branches, 21:4x)*. The observation is in `review-answer-fm-032-2026-09-24.md`, whose header says 21:45 CEST. Its commit
`9cf97f0` is 21:47:39. Fix forward: *21:47:39 (`9cf97f0`)*.

**R2 · P3 · 90% · The same row says `--answer` cuts *the commit subject* at 60 characters. It cuts the answer.** The
line is `f"{tid}: {answer[:60]}"` (`shoalmark.py:1335`). PR 61's subject is 68 characters: `FM-032: ` and 60 of the
answer. The observation the row cites says it right: *cut at 60 characters of the answer*. The mid-word cut and the
whole `answer:` line are true as written. Fix forward: *cuts the answer at 60 characters in the commit subject*.

**R3 · P3 · 70% · *What is true now* does not say that the nine now stand.** Its first paragraph still ends *so two
rules stand: one channel, and the detached switch … What is left: a week of parallel streams read against Done when*.
After this ruling, the nine also stand, and the summary names them nowhere. AGENTS.md lists FM-031's other ruled rules
(*Ruled by his signed answers to FM-031 (`d20bc89`, 11:08) …*) and does not carry these, so a seat that reads the
contract never meets them. Held at 70%: the body's *Ruled —* section states them, and the tracker is canonical
(rule 1). What is stale is the summary. Fix forward: one sentence in *What is true now*. Whether the nine also go into
AGENTS.md is the Principal's decision, not a defect here.

**Notes, not findings.**
- Line 95, the ruled section's first line, is one line of about 400 characters inside a paragraph wrapped near 125. It
  renders the same.
- The two new lines are rule 6's *one line in the tracker* for a defect found on the way. The freeze would have let
  both be filed as bugs; filing them as lines is allowed too.

## Verdict — READY WITH FINDINGS (P3), 93%

R1–R3 are P3, fixed forward in the next change, with no re-pass (docs tier). There is no P2.

**Not verifiable here:**
- That `--queue` printed *0 waiting on you* between 21:32 and 21:44. The three `answer/*` heads are gone from `origin`
  (it now holds `main` and this branch only). No pull request was open then: PR 60 merged 21:20:46, and PRs 61–63 were
  opened 21:44:29–21:44:43. With `answer/*` excluded, the code gives 0. That is consistent, not observed.
- The push times of `answer/fm-031` and `answer/fm-032`: the forge's event feed carries only `answer/fm-024`'s.
- *On the Principal's word in chat*: a chat is not in git.

**Independence.** I am a sub-agent (`8e509911/reviewer-5`) of session `8e509911`. That is the same session whose
Principal seat made `b61c171`, and which set this ask (`a3ff174`, with its options at `cb1d05e`). This is a same-session
pass, not an independent one. The answer is the Owner's.

*the Owner lands this by merging; a merge rules nothing (path 5).*
