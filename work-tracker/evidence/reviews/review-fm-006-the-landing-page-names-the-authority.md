# Review — the landing page names the authority, FM-006, at d20656d (2026-09-25 10:27 CEST, Reviewer, session `8e509911/reviewer-9`)

**NOT READY — one P2 (R1), two P3 (R2, R3).** Branch `fm/006-the-landing-page-names-the-authority`, tip `d20656d`
(`d20656d1696638ac2e74c8d7f9b8643c31484119`). Four commits on `1295c74` (PR 70's branch, READY), which `origin/main`
has since merged as `c3cd54c` at 09:59:12, so the fork point is now on `main`.
- `7fdbc01` 09:54:29, principal: FM-006's body. It holds the Owner's finding, his proposal and counter-fact, and the
  Auditor seat's assessment.
- `af5229e` 10:02:14, GtM seat (`8e509911/gtm-1`): `docs/index.md`.
- `50a39b7` 10:02:16, GtM seat: `docs/de/index.md`.
- `d20656d` 10:04:35, principal: the wording decision's ship-log row.

**Tier: docs, one pass.** `git diff --name-only origin/main...HEAD` names `docs/index.md`, `docs/de/index.md` and
FM-006. There is no `shoalmark.py`, no test, no configuration and no hook. A finding below P2 is fixed forward, and a
P2 sends the branch back.

**The FM-033 order holds.** The two page commits are outside `work-tracker/`. At each one's parent (`7fdbc01`,
`af5229e`), FM-006 reads `status: In Progress`, `triaged: 2026-09-23`, `tier: P2` and `rank: 5`. It already read In
Progress at the base.

**Independence:** this seat is a sub-agent of `8e509911`. Every commit on the branch is from that session: the
principal `8e509911` and the GtM seat `8e509911/gtm-1`. `--check` will count this verdict as *same session*. Reported,
not refused.

## What I ran

| run | result |
|---|---|
| The Principal's transcript: a Python filter on the `user` records stamped `2026-09-25T07:52:49`, nothing else read | one record, `07:52:49.332Z`, string content, one `<pasted_content id="4cc3">` |
| The paste's body against FM-006's block at the tip, as bytes | identical |
| `sha256` of the block with one trailing newline | `65980cd066b83e1f399c616c75c01d7e87da44209478d9d4103842620d5e41d2`, the value FM-006 states |
| `git show 50a90e8` | the *9 of 13* and *200 unread* lines came from *the consumer's record on its `main`*: another project's |
| `gh pr list` (70 pull requests) and `gh api …/pulls/N/commits` for 1–69; `git show --name-status` on each commit | 37 and 15 reproduce; 10 and 12 only under another method than the printed one (R1) |
| `gh api …/events` (the forge keeps 300; they reach back to 2026-09-24 05:18 UTC): each pull request's `opened` time against the pushes to its branch | the branch head at opening, for the pull requests opened since then (R3) |
| `grep` of both pages for *mandate*/*Mandat*, *9 of 13*, *200*, *unread*/*ungelesen*, *28 hours*, *our own*, PortDive, MSR | nothing |
| `uvx zensical build` in a scratchpad clone at `d20656d` | exit 0, *No issues found*, 0.49 s. *four tiers* renders `href="signing.html"` and *vier Stufen* renders `href="signing.html"` under `de/`: `site/signing.html` and `site/de/signing.html` exist |
| `python3 shoalmark.py --check` | exit 0; *INDEX.md is up to date — 34 trackers*; *filing freeze: 18 open* |
| `python3 shoalmark.py --session-check` | exit 0 |
| `python3 shoalmark.py` | exit 0; `git status --short` empty after it |
| `test_shoalmark.py`, `test_core.py` | exit 0, 355 ok and 148 ok, all green, on Python 3.14.3 and 3.9.6 |
| `git merge-tree --write-tree` against `origin/main` (`c3cd54c`), `origin/fm/006-the-site-rebuilt-after-every-pull` (`1295c74`) and `origin/fm/029-0-18-3-the-relation-recovered-the-authority-named-the-queue-tested` (`8c3c10b`) | exit 0, all three |

## The checks

**1. The Auditor seat's block is the Owner's paste, word for word — ✓; confidence high (99%).**
- **The block.** It runs from *Yes, it's missing · 80%.* to *… Fix or source the "9 of 13" line in the same change.*
  It equals the body of the 07:52:49Z record's `<pasted_content id="4cc3">`, byte for byte.
- **The hash.** With one trailing newline, the hash is `65980cd0…5e41d2`, as FM-006 states.
- **His own words.**
  - The finding is quoted with only the capital changed (*the landing page in `site/` fails to name the product's
    core selling point now*). The paragraph's lead marks it *(spelling normalised)*.
  - The English proposal is verbatim. The German proposal gets the closing quotation mark the paste lacks.
  - The counter-fact, *in his words*, has its punctuation normalised: a full stop becomes a semicolon, and the two
    parentheses become italics joined by ·. The paragraph's mark covers this.
- **Not verifiable from the record.** The proposal came in a fence labelled *Proposal for the GTM* and names no
  author. FM-006 reads it as his, which is plausible.

**2. Every claim on the two pages is what v0.18.2 enforces — ✓ with one qualification (R2); confidence high (90%).**
The tool on `origin/main` is v0.18.2: `VERSION` is `0.18.2`, and `shoalmark.py` and both suites are unchanged since
the tag.
- ***An answer counts only as a commit signed by a key you trust.*** `verified_as` (`shoalmark.py:2943`) asks for
  `%G?` = `G`, a good signature under a trusted key. It also asks that the principal the key is trusted for is the
  identity claimed. The answer rule calls it at `:3680`.
  - Test 1457: `answerers = ["holgo signed"]`, and an unsigned answer is refused.
  - Test 1462: signed under a trusted key, it passes. Test 1464: the right key under another identity is refused.
  - Test 1931: `[seats] owner = "… signed"`, and unsigned does not count.
  - These support the sentence where the owner's seat says `signed` (R2).
- ***The gate refuses an unsigned one.*** The same tests cover it, under the same condition (R2).
- ***A merge is not an answer.***
  - Test 1996: an answer that reached the trunk through a merge belongs to the commit that wrote it, never to the
    merge.
  - Test 2250: an unsigned answer that a merge brings in is refused, and the refusal names that commit, not the
    merge.
  - A merge neither authors an answer nor launders one. Both tests support the sentence.
- ***A click is not an answer.*** The board is *one static page* (`render_html`, `:2362`). Its accept and reject
  dialog (`:1696`) builds `--answer ID accept|reject "…"`. The second screen (`:1722`) only copies that command
  (`navigator.clipboard.writeText`, `:1733`) and tells the Owner to run it in a terminal. Tests 1488 and 1531 pin the
  dialog and the command. This supports the sentence.
- ***A line in chat is not an answer.*** The gate reads only the tracker files and the version control system.
- ***Four tiers, from a key anything on your account can use to one that needs your touch.*** This is tier 0 to
  tier 3 of `signing.md`.
- ***Every signature names the key that made it.*** This is true of git's SSH and GPG signatures (`%GK`,
  `--show-signature`), not of anything shoalmark prints. The signing page says that today the tool *says only whether
  an answer's signature verifies*. The clause does not say that the record states the tier. It replaces the
  Auditor's *the record says which*, which v0.18.2 could not back. Held.
- **What the pages leave out, as they should.** They say nothing about a build gate (the Owner's *no build before a
  judged mandate* is not used, and v0.18.3 is not tagged). They say nothing about seats reading a click, nothing about
  a rulings log, and nothing about the record stating the tier. *Your agents move on your word* is framing. The claim
  is *only your signed word counts*, and the next sentence places that *in the record*. It does not say the tool
  stops an agent from acting on a click.

**3. The wording — ✓; confidence high (85%).**
- ***Your signed word*, not *mandate*.** Neither page has *mandate* or *Mandat*. The English is *Your agents move on
  your word — and only your signed word counts.* The German is *Ihre Agenten handeln auf Ihr Wort hin — und es gilt
  nur Ihr signiertes Wort*, built on *Ihr Wort gilt*.
- **Against his counter-fact.** He warned that *mandate* reads bureaucratic and political in German, and that *your
  signed word* is the warmer fallback. The pages take the fallback. *Beleg* and *Stufen* are the German signing
  page's own words.
- **Stated once, high, before the mechanics.** The bold sentence comes right after *To the owner* and before
  *Measured*, the set-up steps and *What a day costs you*. The old *every answer is your own signed commit* has left
  that paragraph in both languages, so the consequence is not said twice. Within the paragraph, the consequence comes
  first and what enforces it follows.
- **The Auditor's three conditions.**
  - (1) Claim only what the tool enforces: yes, within R2.
  - (2) Pair it with the tiers: the four tiers are linked to `signing.md`, which builds to `signing.html`, and tier 0
    is named honestly.
  - (3) The GtM seat wrote the copy (`gtm@seat`, `8e509911/gtm-1`) under FM-006, In Progress, and this pass checks
    it.
  - His fourth point, the *9 of 13* line fixed or sourced in the same change: it is fixed, with the method not yet
    right (R1).

**4. The measured numbers — ✗ (R1); confidence high on the facts (measured).**
- **Gone.** *9 of 13* and *200 merged unread* are on neither page. `50a90e8` (2026-09-23 22:10, the Implementer seat)
  sourced both to *the consumer's record on its `main`*, another project's. Nothing from another repository remains.
  *AP-007*, in an unchanged line, is the tool's example id.
- **The split.** `ffa63b8` is the Owner's signed answer (`G`, `holgoijo@gmail.com`), 2026-09-24 11:07:43 +0200. It is
  FM-032's *all four now*. Its first measure is the review tiers: every change gets a Reviewer pass, docs one, code
  the full loop (`AGENTS.md`, `fbc2697`). Before it, `AGENTS.md` had no review rule, so *the review rule (every change
  gets a Reviewer's pass)* is a fair gloss. The page claims no cause.
- **The denominators reproduce.** Pull requests 1–69, merged, without `answer/*`, split at 09:07:43Z: 37 before and
  15 after.
- **The numerators do not, by the printed method** (R1).
- **The weakness** is stated only implicitly (R3).

**5. The German says what the English says — ✓; confidence high (90%).** Sentence by sentence:
- the owner's paragraph without the old clause;
- the bold claim;
- *Im Beleg … eine unsignierte lehnt das Gate ab*;
- click, merge and chat;
- the tiers, with the same two ends and the same closing clause;
- the repository line, both bullets and the method, with the same numbers, the same *adding* (*anlegt*, so R1 is in
  both) and 11:07 *MESZ*.

The owner is *Sie* throughout.

**6. Gates — ✓; confidence high.**
- `uvx zensical build` is clean.
- `--check` and `--session-check` both exit 0, and the generator is clean.
- `merge-tree` is clean against all three branches.
- Both suites pass on two Pythons.

**7. Times are sourced — ✓; confidence high.**
- *09:52:49* is the record's 07:52:49Z plus two hours.
- *09-24 11:07* and *11:07 CEST* are `ffa63b8`'s author and committer time.
- `af5229e`, `50a39b7` and `50a90e8` are the commits the rows name.
- Both new rows sit at the top of a newest-first log. The diff deletes no line of FM-006, and no added line carries
  `≈`.

## Findings

**R1 · P2 · confidence high on the fact (measured), about 70% on the grade · The method printed on both pages is not
the method that gives 10 of 37 and 12 of 15.**
- **By the printed method** (*a commit adding a file under `work-tracker/evidence/reviews/` … dated before the pull
  request was opened*), the count is **9 of 37 and 9 of 15**. The PRs that count are 16, 17, 18, 20, 21, 28, 30, 33
  and 37 before, and 47, 49, 53, 57, 60, 64, 66, 68 and 69 after.
- **10 and 12 come back only** when a commit that adds *or changes* a review file counts, with merge commits set
  aside. Author date and committer date give the same result.
- **The four it adds** are PRs 26, 55, 56 and 58. Each carried a second verdict appended to an existing review file.
  For example, `27e67d2` is PR 58's own NOT READY in `review-fm-006-0-18-2-the-board-wears-the-mark.md`. These are
  real verdicts, so the method used is the better one, and the printed one is wrong.
- **Merges.** Counted against their first parent, merges bring in `main`'s review files and give 12 or 13 of 37. The
  page does not say that merges are set aside.
- **Why P2.** The section is headed *Measured, not promised*. The Auditor's condition was a cited method, so that the
  number can be checked. A reader who follows the printed method gets 9 of 15 (60%), not 12 of 15 (80%). That is the
  defect this branch exists to fix: a public number that does not come back from its source. FM-006's top row repeats
  *method printed on the page*.
- **Fix, both languages and the row:**
  - either print the method used: *a commit adding or changing a file under `work-tracker/evidence/reviews/` (merge
    commits aside) is dated before the pull request was opened* (*… anlegt oder ändert (Merge-Commits nicht
    mitgezählt) …*);
  - or recount by the printed method and print 9 of 37 and 9 of 15.

**R2 · P3 · confidence high on the fact, 70% on the grade · The authority sentence holds as the set-up page configures
it, under git, and the page says neither.**
- **Where `verified_as` applies.** The gate asks it only of a seat or answerer marked `signed` (`shoalmark.py:3677`).
  Without that mark, an unsigned answer passes with a note: tests 1452 and 1936, and `signing.md`'s own table (*it
  works, and it proves nothing*). `--init` writes no `[seats]`. Step 4 of `setup.md` writes
  `owner = "you@example.org signed"`.
- **Under Subversion.** `signed` is refused (`:3631`), and the server authenticates the committer instead. The same
  page says *Runs on git and Subversion*, and FM-006 names an outside owner on Subversion. For him, *signed by a key
  you trust* is not what the tool checks.
- **The substance holds in both cases:** only a commit authenticated as you counts.
- **Fix forward:** *Under git, set up as [the set-up page](setup.md) says, an answer counts only as a commit signed by
  a key you trust …; under Subversion, only as a commit the server authenticated as you.* Both languages.

**R3 · P3 · confidence high on the fact, 60% on the grade · The measure is a commit's date, the bullets say *when
they were opened*, and the page does not name the gap.**
- **The gap.** A commit's date is set where the commit is made, not when it is pushed. *Carried when opened* means the
  branch head at opening.
- **Checked where the forge still keeps the pushes.** The events reach back to 2026-09-24 05:18 UTC. For each of the
  14 pull requests counted in that window (33, 37 and all 12 after the rule), the counting commit was in the branch
  head at opening. PR 69's `d042ec2` was dated before its opening and pushed after it, and PR 69 counts anyway through
  `cdb465b`.
- **Not checkable.** The 8 counted before the window (PRs 16–30) cannot be checked this way.
- **So** the after number holds on the stronger reading. The page's *dated* is honest about what was measured, but it
  leaves the gap unsaid.
- **Fix forward:** one clause, e.g. *dated, not pushed; from 24 September 05:18 UTC the forge's push events confirm
  each*.

## Verdict — NOT READY (R1 P2), 70%

**NOT READY.** R1 is the one P2, and it is two words and a parenthesis in each language, plus the row. The rest holds:
- The Auditor seat's block is the paste, byte for byte, under the hash FM-006 states.
- The Owner's words are quoted normalised and marked.
- *Your signed word* replaces *mandate*, and the German rests on *Ihr Wort gilt*.
- The consequence is stated once, high, and first.
- The tiers are linked.
- Every sentence about answers is backed by the tool at v0.18.2, within R2.
- Nothing is claimed about the build gate, clicks read by seats, a rulings log or the tier on the record.
- The other project's numbers are gone.
- The German says what the English says.
- The build, the gate, the generator, merge-tree and both suites are clean.

R2 and R3 are P3, fixed forward under the docs tier. The pass on the fix need only recount by the method it prints.

Not verified:
- The Auditor seat's own record (sealed, and barred by the brief).
- Whether the proposal fence is the Owner's own text or one he relayed.
- The branch heads at opening before 2026-09-24 05:18 UTC.

The Owner lands this by merging; a merge rules nothing.

## The second pass — at eaf0e63 (2026-09-25 10:40 CEST, Reviewer, session `8e509911/reviewer-9`)

**READY.** Three commits by the GtM seat (`8e509911/gtm-1`) after this verdict (`c68de13`):
- `78b10da` 10:31:03: `docs/index.md`.
- `9fd7837` 10:31:05: `docs/de/index.md`.
- `eaf0e63` 10:31:16: FM-006's wording-decision row, rewritten in place. It is still unmerged: it came in at
  `d20656d`, which `origin/main` (`c3cd54c`) does not hold.

**Tier: docs, one pass.** The branch touches the two pages, FM-006 and this file. The FM-033 order holds: at the
parents of `78b10da` and `9fd7837`, FM-006 reads `status: In Progress`.

**R1 closed · confidence high (measured).** Both pages now print the method that was used: *a commit adding or
changing a file under `work-tracker/evidence/reviews/`, merge commits excluded, dated before the pull request was
opened* (*… anlegt oder ändert (Merge-Commits nicht mitgezählt) …*).
- **Inputs.** I fetched the pull request list again: 1–69 are unchanged. I also re-fetched the commit lists of PRs 16,
  26, 55, 56, 58 and 69, and they are unchanged.
- **Recount.** By the printed method it is **10 of 37** (PRs 16, 17, 18, 20, 21, 26, 28, 30, 33, 37) and **12 of 15**
  (PRs 47, 49, 53, 55, 56, 57, 58, 60, 64, 66, 68, 69). These are the pages' numbers, by author date or committer
  date alike.
- **The row.** FM-006's row states the same method and numbers. It says the first print gave 9 of 37 and 9 of 15, and
  it names the fixing commits.

**R2 closed · confidence high (90%).**
- **On git.** The refusal now reads *on git, once your seat is marked `signed`, as the set-up page does it*. This is
  `shoalmark.py:3677` → `verified_as`. The link renders `setup.html` in both languages.
- **Under Subversion.** The pages say *it counts only as a commit the server authenticated as you*. This matches the
  code:
  - `line_author` (`:2888`) reads the answer line's author from `svn blame` (`svn_blame`, `:2853`). That is the
    revision's `svn:author`, which the tool treats as the server-authenticated account, and it has no email.
  - The answer rule then asks that this author holds `answer` (`:3664`) and is `answered-by:` (`:3666`).
  - `signed` is refused as a configuration problem (`:3631`, test S4).
  - Tests S4 run the same reader and seat check for an ask under Subversion. No test runs an *answer* under
    Subversion; the path is the same function. Not a finding.
- **The assumption.** `svn:author` is authenticated only where the server authenticates. A `file://` repository or an
  open revision-property hook would not. The tool's own docstring and `setup.md` assume the same, so the page claims
  no more than the tool.

**R3 closed · confidence high.** Both pages say that a commit's date is when it was made, not when it was pushed. They
say the forge's push events confirm the counted pull requests from 2026-09-24 05:18 UTC on, and no longer list older
ones. That is what I found: all 14 counted in that window were confirmed, and the events stop at 05:18:24Z.

**The German says what the English says.** Sentence for sentence:
- the qualified refusal, with *Sitz*, the German set-up page's word;
- the Subversion sentence;
- the method, with *anlegt oder ändert* and *Merge-Commits nicht mitgezählt*;
- the date-and-push sentence and 05:18 UTC.

**Gates.**
- `uvx zensical build` in a scratchpad clone at `eaf0e63`: exit 0, *No issues found*, 0.40 s.
- `--check` 0 (*INDEX.md is up to date — 34 trackers*), `--session-check` 0, and the generator leaves the tree clean.
- `test_shoalmark.py` 355 ok and `test_core.py` 148 ok, on Python 3.14.3 and 3.9.6.
- `merge-tree` is clean against `origin/main` (`c3cd54c`) and against PR 65's branch at its new tip, `e3aa64e`.

The Owner lands this by merging; a merge rules nothing.
