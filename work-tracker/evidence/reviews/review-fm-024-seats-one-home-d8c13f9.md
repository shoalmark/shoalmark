# FM-024 — the Reviewer's docs pass on the seats' one home, d8c13f9

Verdict: NOT READY — two P2 (RV-2080, RV-2081): the second commit's list of departures from the credo is not complete.
Reviewed: d8c13f9e2fd7dc8790bc490c3ffbd81b07712f1c (a074ffc, f34446e, and the rename d8c13f9 pushed during the pass); base origin/main 297896b.
Reviewer: 8e509911/reviewer-65, the branch's own session — not independent. Tier: docs (seats/index.md; zensical.toml's nav, unread by the gate); no suite.
(1) The Owner's rulings 1–6 and four fixes (normalised) hold: seven seats, the Owner not one, a seat "it", the research type line, English
names and German *Sie*, the auditor's may-not in the credo's words, a linkless practice line each, the designer's brief — but RV-2083, RV-2084.
(2) Against `git show HEAD:agents/CREDO.md` (the parent project's, read only): principal, implementer, reviewer, auditor match or are listed.
RV-2080, P2, high: go-to-market takes "a public line" for "copy"; its signs add "the survivors, and why the rest died"; *(Owner-convened)*,
*(the default seat)* and "(the SOUL's seat)" go; the seat column adds the icon names. Fix, the missing line for the next commit's message:
`(8) go-to-market takes "a public line" for "copy" and signs "the survivors, and why the rest died" beside the screen record; the seat
cells drop the credo's Owner-convened and default-seat notes and add each icon's name.`
RV-2081, P2, high: (2) says research's takes and signs "merge both rows", its practice "joins both"; but the takes are the type line's
words, and "a tracker tagged research, after the Reviewer's attack on it" goes — a gate the parent project loses on linking here; "the
count" stands for "the power arithmetic"; the practice drops "build nothing" and the planted-fixture-and-empty-database query rule. Fix: `(9)
research takes the type line's two questions, not the credo's, and "after the Reviewer's attack on it" goes; it signs "the count" for
"the power arithmetic"; its practice drops "build nothing" (a may-not) and the planted-fixture clause.`
RV-2082, P3, high: (7) "the words stay" is untrue as worded; the edits are generic, meaning kept, as the fix asked ("`P<n>` amendments …
locked docs" → "amendments … a locked text", "platform build" → "build", "rigor" → "rigour", "a PR" → "a pull request", third person).
Fix: `(7) Doctrine links are dropped; the rest is made generic and third-person, meaning kept.`
RV-2083, P3, high: the Owner's fix links README §Seats; line 4 leaves it unlinked. Fix: `(README §*Seats*)` → `([README §*Seats*](../agents/README.md#seats))`;
a scratch build renders ../agents/index.html#seats, `id="seats"` present, check_site 0.
RV-2084, P3, medium: `BUILTIN_RIGHTS` (shoalmark.py:186) gives `implementer` no right, as README §Seats says; "any other seat" makes `owner`
a seat, which line 3 denies; "as it likes" calls the adopter, a person, "it". The Owner's wording — the Principal puts it to the Owner: `The
tool itself knows four names and the rights each holds built in — owner all four, principal ask, close and triage, reviewer triage,
implementer none (README §Seats, linked); any other name in [seats] is the adopter's choice, its rights in [rights].`
RV-2085, P3, high: (4) "each virtue carries the approved icon character" — the designer's has none, the auditor's is the credo's own,
go-to-market's reads "the gates" for "its screen". Fix: `(4) Five virtues carry the approved icon character; the auditor's is the credo's, the designer's has none.`
(3) No other project's path or number; they/them for persons, "it" for seats but RV-2084; no German twin, by the Owner's word, and de/index.md
names no development seat (its "Sitz" is the Owner's own [seats] entry). seats/index.html is built; /agents/ 200, /setup/ 404 today: /seats/ holds.
(4) Zensical 0.0.66, scratch venv, `git archive d8c13f9`: build --clean 0, llms_txt.py 0, check_site.py 0; nav Requirements, The seats, For agents.
Quality read: tight, three tables, nothing made obsolete. (5) --check 0, --session-check 0, diff --check 0; merge-tree origin/main d8c13f9 0,
tree 0cf0dbd; Session: 8e509911, Worktree: shoalmark-principal-4 on all three. Four numbers: product +47, records +0, deletions 0, 0; this file +35.
Queue: `branch fm/024-the-seats-one-home @ d8c13f9  wait: no pull request — no verdict on d8c13f9` · `6 waiting on you: 1 merge, 0 close, 0 wait, 5 pushed without a pull request`
path 5 — a merge rules nothing.
