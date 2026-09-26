# Review — FM-006: the page on his word in TRIAGE.md (2026-09-25 22:56 CEST, Reviewer, session `8e509911/reviewer-17`)

A new file: `review-fm-006-when-shoalmark-goes-public.md` reviews the go-public ask, and this branch files a different
subject, the site page on TRIAGE.md, under the same tracker.

## Verified: the page on his word filed, b025d98

**Scope.** `fm/006-the-page-on-his-word-in-triage-md`, tip `b025d98` (`b025d98e16f826ed865cb0697376c0b524c7eaf9`), one
commit by the principal seat (`Session: 8e509911`, 22:40:18) on `origin/main` `0d60d55` (PR 79's merge). It changes
FM-006 alone: 26 lines added, none removed. **Tier: docs, one pass.** A misquote of the filed text is P2; the rest is P3.
**Independence:** same session — 8e509911's own sub-agent, reported.

**What I ran.**
- **The paste.** The filed text after its opening bold line (FM-006 line 127) is lines 129–142, from *From the Auditor
  seat, on the Owner's word: …* to *- Worded by the GtM seat; …*: 14 lines, 1514 bytes, the last newline included.
  sha256 over exactly those lines: `be19a4100d73fc27f6d0015ac42a8c4ee152ebcfa751e9ec8fc523ac99933584`. It equals the
  brief's hash and the hash in the opening line, and `cmp` finds it byte-identical to the paste file ✓.
- **The Principal's text after it** (lines 144–146; two sentences over three lines, the second wrapped after *words
  it,*), against the paste and the record:
  - *the freeze (20 open)*: `--check` at `b025d98` prints *filing freeze: 21 open* (R1). That the freeze bars a new
    tracker is the paste's own word ✓.
  - *FM-022 (Shipped) left the site out on purpose*: FM-022 is `status: Shipped`, and its body says *Not changed, on
    purpose: … `docs/setup.md` §5 (EN and DE), the documentation site* ✓.
  - *this tracker holds the page*: the paste's *a line on FM-006* ✓.
  - *The build waits for FM-037's guard to merge*: FM-037 is In Progress, `next: build` on main, and its build branch
    `origin/fm/037-only-the-owner-changes-his-intent-and-his-path` (tip `a92a3cc`, ten commits) is not an ancestor of
    `origin/main`. So the build is pending ✓. *only you change it*, the tool's, with its tier-0 limit: the paste's second
    bullet, and FM-037's clause 6 ✓.
  - *the GtM seat words it, a Reviewer checks every claim against evidence before the merge*: the paste's last bullet ✓.
  - *the term stays* your signed word: the GtM seat's decision is FM-006's ship-log row of 2026-09-25 (line 156: *your
    signed word*, not *mandate*; `af5229e`, `50a39b7`) ✓. *Unless the Owner rules otherwise by an ask* shortens the
    paste's *rules "mandate" or "Person-in-charge" in by an ask*. It is not quoted, and it adds no power a ruling by ask
    lacks. Not a finding.
- **The three commits the paste names.** All three are on `origin/main`:
  - `fe36cc0` is the Owner's own signed commit (holgo99, `%G?` G, 10:37:13, *Updates after parley with Consigliere*).
    It rewrites the intent's three lines and the current path. Path line 3 is rewritten whole: a review's evidence file
    on the head, a Reviewer from another independent session for critical changes, inline passes on other code, one pass
    for documentation, and the Owner's own answers reported, never blocking. Lines 1, 2 and 5 are reworded, and line 6
    is added ✓. The independence count is the line `--check` prints: *99 verdict(s) · independent 8 · same session 86 ·
    untraced 5* ✓.
  - `42f4eca` is the principal seat's, unsigned, 12:15:38. *triage: FM-035 kept P1 #6 build the same day it was filed*.
    It sets FM-035's front matter to `tier: P1`, `rank: 6`, `next: build`, and its Passes paragraph cites path line 1
    cut, as *a failed command* ✓.
  - `c8939e3` is the principal seat's, 12:30:44, made on its Reviewer's R1–R5. It changes `tier: P1` to `tier: P2`, and
    quotes path line 1 whole: *the daily sitting runs on a tagged release with a signed answer and no failed command in
    the sitting* ✓.
- **What is true now** (line 22) matches the section: a page for people on what TRIAGE.md holds, the intent and the
  current path, and what an edit there does. It is owed on the Owner's word (22:38:24), built after FM-037 merges, and
  the line is filed below ✓. It is a summary, not a quote.
- **The ship-log row** is at the top, dated 2026-09-25, and no row below it changed. Every clause is the paste's: English
  and German, the intent and the path and what an edit does, each claim labelled, worded by the GtM seat, every claim
  checked, built after FM-037 with FM-007's tier-0 limit. It gives the hash as `be19a410…` and states no open count ✓.
- **Front matter.** Byte-identical to `origin/main`'s (the diff's first hunk is at line 22). `ask:`, `ask-kind: action`,
  `ask-since:`, `ask-options:`, `ask-proposal:` and `next: owner` are untouched ✓.
- **Gates.**
  - `python3 shoalmark.py --check` 0: *INDEX.md is up to date — 37 trackers*, the freeze line *21 open, at or above 8 —
    only bug filings*, and every build commit under a judged In Progress tracker.
  - `--session-check` 0.
  - The suites as `lefthook.yml` runs them: `test_shoalmark.py` 0 (438 ok, no check skipped) and `test_core.py` 0 (148
    ok), on 3.14.3 and on `/usr/bin/python3` 3.9.6.
  - `git diff --name-only origin/main...HEAD` lists FM-006 only. INDEX.md was not regenerated, and it needed no
    regeneration ✓.
  - `git merge-tree --write-tree origin/main HEAD` is clean (`9acf9a5`). `origin/main` is still `0d60d55` after a fresh
    fetch.

**R1 · P3 · confidence 95% · *the freeze (20 open)* is out of date: `--check` says 21.**
- At `b025d98` and at its base `0d60d55`, `--check` prints *filing freeze: 21 open, at or above 8*. By status, 15 are In
  Progress, 4 Parked and 2 Proposed.
- 20 was right at the addendum's re-make, whose line 97 on main still reads *(`--check`: 20 open, only bug filings)*.
  Then FM-037 was filed at 19:03:56 and made it 21. The added sentence takes the older number.
- The substance holds: the freeze holds at 21 as at 20, and the paste gives no number.
- **Fix forward, or leave:** *(21 open)*, or no number. Line 97 is of its own time and is not this branch's.

**R2 · P3 · confidence 60% (the times are exact; whether the heading should say so is the question) · The heading
dates the filing to the paste's minute.**
- The heading reads *filed 2026-09-25 at 22:38:24*. That is when the Auditor seat's line came through the Owner: the
  opening bold line and the ship-log row both say *through him at 22:38:24*. The filing commit is 22:40:18.
- The file's other dated heading gives the time of the word, not of the filing (*the Owner's finding of 2026-09-25
  09:52:49*).
- **Fix forward, or leave:** *— through the Owner 2026-09-25 at 22:38:24*.

**Verdict on b025d98: READY WITH FINDINGS (R1, R2 P3).**
- The filed paste equals the paste: 14 lines, sha256 `be19a410…`.
- The Principal's added text rests on the paste and the record, except for its open count (R1).
- The three commits exist on main and show what the paste says of them.
- The What-is-true-now line and the ship-log row match the section.
- The front matter and the ask are untouched, and the gates are green.
- Tier: *docs, one pass*. Independence: *same session — 8e509911's own sub-agent, reported*.

The Owner lands this by merging; a merge rules nothing.

## The page built: verified at 59febae

**Scope.** `fm/006-the-page-on-his-word-in-triage-md-built`, tip `59febae` (`59febae83eee5dfd189dc9a00319518067b085f7`),
two commits by the GtM seat (`Session: 8e509911/gtm-2`) on `origin/main` `88c7b0c` (PR 84's merge):
- `c897443` (02:03:17): the filing review's R1 and R2.
- `59febae` (02:04:25): `docs/triage.md` and `docs/de/triage.md`, one nav line each in `zensical.toml`, FM-006's rows,
  and `evidence/FM-006/triage-page/` (`demo.sh`, `demo-de.sh` and their `.out`).

Reviewer session `8e509911/reviewer-20`, 2026-09-26 from 02:06 CEST. **Tier:** *docs, every claim against evidence*. A
claim that is unlabelled, that has the wrong label, or that misstates the record is P2 (the filing's rule).
**Independence:** *same session — 8e509911's own sub-agent, reported*.

**What I ran.** It was 00:06 UTC and 02:06 CEST, so FM-028's window was open. Every suite, `--check` and demo ran with
`TZ=UTC`.
- **The pages.** I read both pages whole, and every commit, tracker, review file and line of `shoalmark.py` a claim
  rests on (the table below).
- **The site.** `uvx zensical build` (0.0.65) printed *No issues found*. It wrote `site/triage.html` and
  `site/de/triage.html`, and `site/index.html` and `site/de/index.html` link both pages from the nav.
- **The refusal.** `git archive 88c7b0c` gave me the tool in a scratch directory. I ran `demo.sh` and `demo-de.sh`
  against it. Both outputs equal the committed `.out` files except for the commit ids, which are new on every run
  (7-hex ids normalised). The three refusal lines on each page (EN l.129–131, DE l.159–161) are byte-equal to the
  committed `.out` files.
- **The guard in the suite.** `test_shoalmark.py` includes FM-037's checks: clause 1 (the refusal, and `--check` exits
  4), clauses 2 and 6 (the message, the way through and the limit), clause 3 (`## Passes` stays open), clause 4
  (`--queue`), the hook, and merges. All are green (below).
- **The independence line.** `--check` at `88c7b0c` (checked out detached, then back to `59febae`) printed
  `reviews this week · 104 verdict(s) · independent 10 · same session 89 · untraced 5`, the page's line word for word.
- **Gates at `59febae`.**
  - `--check` 0. INDEX up to date, 37 trackers, *filing freeze: 21 open*. The guard line: *none changes them or his
    signers file*.
  - `--session-check` 0.
  - The suites as `lefthook.yml` runs them. On 3.14.3, `test_shoalmark.py` 0 (456 ok, all green) and `test_core.py`
    0 (148 ok). On `/usr/bin/python3` 3.9.6: `test_shoalmark.py` 0 (456 ok) and `test_core.py` 0 (148 ok).
  - `git merge-tree --write-tree origin/main HEAD` is clean (`801b648`). `origin/main` was still `88c7b0c` after a
    fresh fetch. No release branch is on origin. The local `release/0.18.4` (`41dcc56`, another session's, only read
    here) also merges clean (`d4e6140`).

**Every claim and its evidence.** EN and DE line numbers are given where they differ. ✓ holds, ✗ a finding.

| # | Claim (EN l. / DE l.) | Label | Evidence | Holds? |
|---|---|---|---|---|
| 1 | The page is in `docs/` and `docs/de/`, in the nav, and the site builds | — | `zensical.toml` +2; the build above | ✓ |
| 2 | *Only your signed word changes them* (7 / 9) | the tool | FM-037's guard (`GUARDED`, `guard_verdicts`); demo runs 1 and 2 | ✓ |
| 3 | `TRIAGE.md` is in the tracker directory, `docs/work-tracker/` by default (23 / 24) | — | `DEFAULTS["tracker_dir"]` | ✓ |
| 4 | The intent: three lines about the whole repository, never one feature; the path; *Passes* (26–30 / 27–33) | none (R7) | `INTENT_LEAD`, `PATH_SCAFFOLD`, `TRIAGE_RULES` step 5; `TRIAGE.md` on main | ✓ as description |
| 5 | The village-library example as `--init` writes it (EN), or as `examples/de/TRIAGE.md` carries it and is copied before `--init` (DE); FM-022's reason (32–38 / 39–47) | — | `INTENT_EXAMPLES` / `_DE` byte-equal to the quotes; `examples/de/TRIAGE.md` l.15–17; `docs/de/setup.md` §2; FM-022 l.23–25: *his own first draft came out feature-sized after a seat's feature-sized example* | ✓ |
| 6 | A pass reads all he writes, less the lead-in and untouched examples (42 / 51) | the tool | `owners_intent()` against `INTENT_SCAFFOLD` | ✓ |
| 7 | German headings `Die Absicht`, `Der aktuelle Weg`, `Durchgänge`; raises under `## Einwände` (DE 35–37, 69) | — | `examples/de/shoalmark.toml` `[headings]` | ✓ |
| 8 | `--next` prints the path before the ranked work; `INDEX.md` carries it word for word near its top; the board shows it below what waits for him (50 / 59) | the tool | `--next` run at the tip; `INDEX.md` from l.19; the board script puts *waiting for you*, then the acts, then `path.title` | ✓ |
| 9 | `--triage` prints the intent above its rules and the path below them, and refuses to start with no path; the three quotes (52–54 / 61–64) | the tool | `TRIAGE_RULES`; `main()` returns `EXIT_LINT` on *names no current path — tiers cannot be judged; the Owner writes it first*. The English page adds a closing full stop inside two of the quotes that the tool does not print; the words are the tool's. Not a finding. | ✓ |
| 10 | *The next pass keeps and tiers every open tracker against your new words* (55 / 65) | review | `triage_worksheet` and `owed_a_pass`: a sheet lists In Progress work not judged in 7 days, new filings and raised trackers. Older Proposed, Parked and Reserved work is backlog. Nothing reads a change to the path. | ✗ R5 |
| 11 | A raise dated after the last judgement, naming a line the path has, puts the tracker on the sheet marked RAISED; *the one place a check acts on your path* (58–61 / 68–72) | the tool | `mark_raised` (the path's line numbers), `board()`, `TRIAGE_RULES` *RAISED* | ✓ mechanism; R6 |
| 12 | `fe36cc0`, 25 September 10:37, `%G?` G: line 3 rewritten; lines 1, 2 and 5 reworded; line 6 added; before and after quoted (65–76 / 78–90) | — | `holgo99`, G, 10:37:13; the diff; both quotes byte-equal to `fe36cc0^` and `fe36cc0` | ✓ |
| 13 | The seats sorted their work by the new line that day: *the Owner's line 3 names a release critical, so its fix's review is the cold session's* (`42f4eca`) (78–80 / 96–98) | review | the reason in `42f4eca`'s worksheet row, quoted exactly; `review-fm-035-ci-red-filed.md` reads the tier against line 3 | ✓ |
| 14 | FM-037 was reviewed in two other sessions before it merged, and `--check` lists both as *independent* (80–81 / 98–99) | review | `--check` at `88c7b0c`: verdict `b4fbc98` (session 74b23bf5) and `8185a5c` (01a0da10), both *independent*, the branch's `8e509911/implementer-28`; PR 83 merged at `fa58260`, 01:34, after both | ✓ |
| 15 | The independence line at `88c7b0c`: 104 · 10 · 89 · 5. *A report, not a gate*; FM-024's second slice is not built (82–85 / 100–104) | the tool | my run gave the same line; `sessions_report`/`verdict_reports`: *a report, never a refusal (slice 2 refuses…)*; `--check` exits 0 with 89 same-session verdicts; FM-024's ask names slice 2 unbuilt | ✓ **label right** |
| 16 | FM-035: P1 at `42f4eca` 12:15 (quote); its Reviewer found the quotation cut; line 1 whole; re-made at `c8939e3` 12:30, P2 (quote) (87–94 / 106–115) | review | 12:15:38 and 12:30:44; both reasons quoted exactly from the worksheet rows; line 1 byte-equal to main; `review-fm-035-ci-red-filed.md` R1 | ✓ |
| 17 | FM-007's raise, 24 September, by the Auditor seat; *the line ended "undermines: TRIAGE.md path 5"* (96–98 / 117–120) | — | FM-007 `## Raised` (from `0f0766e`, 18:08, to main): *… · undermines: TRIAGE.md path 5, FM-033's answer* | ✗ R3 |
| 18 | The same evening `29466fc`; re-made on its Reviewer's findings at `c5696c5`: P1, with the quote (98–100 / 120–123) | review | 19:47:27 and 20:24:50; `c5696c5`'s row reason, quoted exactly (its italics dropped); `review-tracker-triage-2026-09-24-evening.md` R4 | ✓ |
| 19 | *The same day* is his rule, his signed answer on FM-033, kept by a pass that runs (102–103 / 125–126) | the text alone | `9e48ee8`: `holgo99`, G, 18:59:10, *a raise naming a signed rule re-judges the tracker the same day*. Nothing refuses or flags a raised tracker left unjudged past the day: `mark_raised` has no clock, and `build_judgement` reads `triaged:` only. | ✓ **label right** |
| 20 | Since 0.18.3 the tool puts a raised tracker under *triage*; on 24 September the seat wrote the row by hand (104–105 / 127–129) | the tool | `mark_raised` since `172a2ad`, in `v0.18.3`; CHANGELOG 0.18.3; `29466fc`'s row *written by hand because the tool cannot yet list a raised tracker* | ✓ |
| 21 | The reason for the tier is the seat's; its Reviewer checks it against the line (106 / 130–131) | review | the evening review's R4 (*the rows do not judge two tiers against the path*), closed at `c5696c5` | ✓ |
| 22 | On a branch `--check` refuses a change under either section (a word, a line, whitespace), a renamed or removed heading, a deleted or moved `TRIAGE.md`, a moved `tracker_dir`. The exception: his signed commit (G, the signer his email, the author the seat holding `answer` in the default branch's `[seats]`). A merge is judged only on text no parent had (110–114 / 135–140) | the tool | `section_changes`, `owners_at(trunk)`, `owners_of`, `guard_verdicts`, `signer_is`; the suite's clause 1 checks | ✓ |
| 23 | The hook refuses a seat's commit before it is made; `--queue` reads *wait: TRIAGE.md changed unsigned* (115–116 / 141–142) | the tool | demo run 2 (commit exit 1, HEAD unchanged); `triage_reading`; the suite's clause 4 | ✓ |
| 24 | The keys come from the default branch's signers file, never the branch's (117–118 / 143–145) | the tool | `trusted_signers`, `signers_paths`, `kept_changes` (AU-19) | ✓ |
| 25 | *Passes* stays open to seats (119 / 146) | the tool | `GUARDED = ("intent", "path")`; the suite's clause 3 | ✓ |
| 26 | The scratch run: `--check` exits 4, and the refusal is quoted as printed (121–132 / 148–162) | the tool | the demos above: byte-equal, and re-run identical but for the ids | ✓ |
| 27 | With the hooks installed, the seat's change was not made, and the hook added the *proves the author only* line (134–136 / 164–167) | the tool | demo run 2; `commit_msg_hook` | ✓ |
| 28 | The way through: the ask form the refusal names; `git commit -S`; `%G? %GS %ae` is the signing page's check (138–141 / 169–173) | the tool | `GUARD_WAY`; `docs/signing.md` l.200 and l.226 | ✓ |
| 29 | The limit, in the filing's words, printed after every refusal (143–144 / 175–178) | the tool | FM-006's paste, second bullet, word for word; `GUARD_LIMIT`, `guard_footer`, `commit_msg_hook` | ✓ |
| 30 | At tier 0 the Owner's key without a passphrase passed `--check` like his own (146–148 / 180–182) | the tool | demo run 4, exit 0 | ✓ |
| 31 | *A passphrase at every signature (tier 2) or a hardware key (tier 3) makes the key yours alone* (147–148 / 182–183) | (the tool's bullet) | `docs/signing.md`, tier 2: *Not by accident … An agent that means harm can fake the prompt and catch it*; l.54–55 | ✗ R4 |
| 32 | An unsigned seat proves the author only, and the tool says so; Subversion is out of scope, in one line (150–153 / 184–187) | the tool | `GUARD_AUTHOR_ONLY` in `guard_proof` and the guard line; `GUARD_SVN` | ✓ |
| 33 | An edit changes no check; `--queue` asks for a verdict on the head because its code does (157–160 / 191–195) | the tool | `queue_actions` (*wait: no verdict on …*), which reads no `TRIAGE.md` | ✓ |
| 34 | The tool writes tier and rank and refuses a seat without `triage`; *that no seat edits them by hand* (161–163 / 196–198) | the tool / the text alone | `RIGHTS`, `rights_problems`; `TRIAGE_RULES` step 2, *Do not make those edits by hand*. Nothing compares a hand edit by a seat that holds `triage` with a worksheet row. | ✓ **label right** |
| 35 | `--answer` answers, signed; an edit, a merge or a click answers nothing; *that no seat reads one as your answer* is path line 5 (164–167 / 199–202) | the tool / the text alone | `--answer` commits signed; path line 5 on main. The tool holds only the recorded answer (the `answer` right, his signed commit), and the page labels that the tool. | ✓ **label right** |
| 36 | An edit does not reach an older branch; it rewrites no past pass (168–171 / 203–207) | the tool | `TRACKER_DIR` of the checkout; `triage-{today}.md` | ✓ |
| 37 | The term *your signed word* / *Ihr signiertes Wort*; no *mandate* or *Person-in-charge* | — | grep on both pages: only the term. His own path line 5 says *mandate* and is not quoted. | ✓ |
| 38 | Nothing of the parent project's state or a client's | — | grep of pages and evidence for the parent's name, its tracker ids, local paths, people and clients: none. The demos invent an Owner (`you@` / `du@example.org`). | ✓ |
| 39 | German: a page in its own right; the labels consistent; `labels.yaml` | — | Recast sentences. Glosses under each English quote. Its own template, setup step and headings paragraph. The labels are *Das Werkzeug · Das Review · Nur der Text*, bullet for bullet as in English. The terms are the other DE pages' (Eigner, Arbeitspaket, Tafel, Sitz). No board word changed, and `labels.yaml` is untouched. | ✓ |
| 40 | The filing review's R1 and R2 | — | FM-006 l.144 *(21 open)*, and `--check` says 21. The heading reads *the paste of 22:38:24, committed 22:40:18* (`b025d98` is 22:40:18). The paste's lines 129–142 still hash to `be19a410…`. | ✓ |

**The evidence links.** Both pages link to `github.com/holgo99/shoalmark/tree/main/work-tracker/evidence/FM-006/triage-page`,
which resolves only after the merge. **Acceptable, not a finding (80%):**
- `docs.yml` builds the site on a release tag only and deploys it only once the repository is public, so no reader
  meets the page before its commit is on main.
- `docs/index.md` and `docs/setup.md` link to `main` in the same way.
- The evidence is outside the go-public act, which covers `FM-001/port/` only.
- The one weakness is general and not this branch's: a site built from a tag links to `main`, so a later move of the
  evidence would break the link.

**R3 · P2 · confidence 95% · FM-007's raise is quoted cut short (EN l.97–98, DE l.119–120).**
- The page says the line *ended "undermines: TRIAGE.md path 5"*. From `0f0766e` (24 September, 18:08) to main, it ends
  *undermines: TRIAGE.md path 5, FM-033's answer*.
- The raise named two signed rules. The same page shows a cut quotation of line 1 moving a tier.
- **Fix:** quote the end whole. Or: *it named TRIAGE.md path 5 (and FM-033's answer) as undermined*.

**R4 · P2 · confidence 90% · Tier 2 is said to make the key his alone (EN l.147–148, DE l.182–183).**
- *A passphrase at every signature (tier 2) or a hardware key (tier 3) makes the key yours alone* contradicts the
  signing page this bullet links to. There tier 2 is *Not by accident … An agent that means harm can fake the prompt
  and catch it*, and *Tier 2 stops the agent that signs by mistake; tier 3 also stops the one that means to*.
- FM-007's answer is the hardware key. The limit is what the page must not overstate.
- **Fix:** *a passphrase at every signature (tier 2) stops the accident; only a hardware key (tier 3) makes the key
  yours alone*. The same in German.

**R5 · P2 · confidence 85% · *The next pass keeps and tiers every open tracker against your new words* (EN l.55, DE
l.65).**
- A pass's sheet lists In Progress work not judged in 7 days, new filings and raised trackers (`triage_worksheet`,
  `owed_a_pass`). Older Proposed, Parked and Reserved work is backlog, *the current path restarts it, not a clock*.
- Nothing reads a change to the path. So a tracker judged this week keeps its tier through the next pass, unless a
  raise names a line of his path.
- *What an edit does not do* repeats it: *they move at the next pass … until that pass, your board shows the old
  judgement* (EN l.161–163, DE l.196–198). The Owner who edits his path would expect every tier to follow at the next
  pass.
- **Fix:** *the next pass judges the trackers on its sheet (work in progress not judged this week, new filings, raised
  ones) against your new words. A tracker judged this week keeps its tier until then, or until a raise names a line of
  your path.* The same in German, and in *What an edit does not do*.

**R6 · P3 · confidence 65% · *That is the one place a check acts on your path* (EN l.60, DE l.71).**
- Two other checks act on the path. `--triage` refuses to start without one (the bullet above says so), and FM-037's
  guard compares its bytes.
- The sense meant, that no check reads what a line says, is stated rightly under *What an edit does not do*.
- **Fix:** *the one place a check reads your lines, and it reads the line's number, not what it says*.

**R7 · P3 · confidence 60% (whether a lead-in needs its own label is the question) · Three lead-in sentences carry no
label.**
- The three sentences:
  - *Your agents hold every judgement against them* (EN l.7, DE l.8).
  - *A pass judges every tier against it* (EN l.28–29, DE l.30–31).
  - *Once your commit is in, your agents work to the new words from their next command* (EN l.47, DE l.56).
- Each is restated by a labelled bullet below it: review for the judgement, the tool for what is printed. None is
  unlabelled in substance.
- **Fix forward, or leave:** a label after each, or *(below)*.

**Verdict on 59febae: NOT READY (R3, R4, R5 P2; R6, R7 P3).**
- Held: the pages, the nav and the build. The refusal is quoted byte for byte, and my re-runs match it. The examples
  from `fe36cc0`, `42f4eca`, `c8939e3`, `29466fc` and `c5696c5` match the record, and so does FM-022's.
- The four labels the GtM seat chose hold: the independence line *the tool, a report, not a gate*, and *the text
  alone* for the same day, for no hand edits and for no click read as an answer.
- Also held: the term, the German page, and the filing review's R1 and R2. No trace of the parent or a client. The
  gates are green.
- Three examples or claims misstate the record: a cut quote, tier 2's strength, and what the next pass reads. Each is
  a fix of a sentence in both languages. Then one more pass on the fix.
- Tier: *docs, every claim against evidence*. Independence: *same session — 8e509911's own sub-agent, reported*.

The Owner lands this by merging; a merge rules nothing.
