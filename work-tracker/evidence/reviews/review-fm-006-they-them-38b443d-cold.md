# FM-006 — cold review of ac4b9ac: they/them and English seat names

Verdict: NOT READY.
Reviewed: ac4b9ac344795abb0bcccd9b498dda7af4b3b0bc
Reviewer: 01a0f303, independent of 8e509911; own clone shoalmark-cold-they-them-38b443d; 2026-09-30.
Tier: code, critical — origin/main...HEAD includes shoalmark.py, assertions and an AGENTS.md rule; full review loop.
Base: origin/main c97d6be96bb009e6b486bf7ff92c9a0668bf3d76; 16 commits, 16 files, +152/-140 with rename detection.

RV-2041 · P2 · docs/triage.md:137–138 and docs/de/triage.md:170–171 rewrite historical output attributed to 88c7b0c and the recorded scratch commits.
The linked work-tracker/evidence/FM-006/triage-page/demo.out:10–11 and demo-de.out:7–8 still contain the old words: the claimed quotation is false, contrary to the record-preservation brief.
Exact fix in those two code blocks only: `their intent and their current path` → `his intent and his current path`; `they can answer` → `he can answer`; `their account` → `his account`. Closure: both blocks match their linked output verbatim.
RV-2042 · P3 · docs/seats/index.md:14 still says `**builder** — the builder`; PR 137 on main names the character in brand/seats/README.md:12 and builder.svg.
Exact fix: `**builder** — the shipwright`; closure: the seat table agrees with the shipped character.
RV-2044 · P3 · docs/de/triage.md:43,48 drops who received the example and whose last loan must be returned; line 48 also ceases to quote examples/de/TRIAGE.md verbatim.
Exact fixes: `weil ein Agent dem Eigner zuvor ein Beispiel dieser Größe gezeigt hatte`; restore `bevor seine letzte Ausleihe zurück ist` inside the quoted scaffold. Closure: the recipient and the member's loan remain explicit, and the source quotation matches.
RV-2045 · P3 · shoalmark.py:2785 introduces `what they owes` in the emitted script comment. Exact fix: `what they owe`; closure: grammatical agreement restored.

Quality read: the findings above are the exceptions to subject/meaning preservation; other changed sentences preserve person/seat/tool roles. Owner quotations remain verbatim.
AGENTS.md:102 is an observable person-versus-seat rule; read with the Owner's explicit quotation/history exception, it contradicts no rule in force. The quoted nine rules remain unchanged.
Rename census: README/docs leftovers are keys, addresses, printed examples, the historical attribution in seats/index.md:46, or the technical SSH term `signer principal`; there are no remaining old seat names in .claude. No separate implementer report was supplied; the census was repeated directly.
All six seat-table row names changed; German retains English seat names and formal Sie in direct address. shoalmark.toml changes one comment only; all keys/addresses are identical.
Records: the only work-tracker change is FM-006's appended row. CHANGELOG adds seven unreleased lines explicitly saying rewording, not product growth; all existing sections are byte-identical.
Recount: FM-006's row correctly records its scoped 11dd6a9..77f7722 slice: product +140/-136, records +8/-0, tool/test +62/-62. The four-line follow-up makes the reviewed total product +144/-140, records +8/-0.
Follow-up: git diff -M 38b443d ac4b9ac is exactly implementer.md → builder.md plus name, description, body opening, and reviewer description: four lines, +4/-4. Model, effort and every other line are unchanged.
AST comparison: shoalmark.py and test_shoalmark.py are identical after replacing string values; exactly ten test string constants changed, with no assertion logic change. Embedded script changes read as comments only.
Golden at 38b443d on the same checkout, base versus reviewed code (both tool blobs unchanged at ac4b9ac): --check changes one line (`his signers file` → `their signers file`); --owner, --queue and --standup are byte-identical; all exit 0. The clone uses the tracked public allowed_signers file.
Suites: test_core.py 157/157 and test_shoalmark.py 548/548 on both Python 3.9.6 and 3.14.3, all exit 0; full suites report zero skips. Launched at 38b443d; tool, suites and their inputs are byte-identical at ac4b9ac.
Gate at ac4b9ac: --check exits 0. First 15 commits: Session: 8e509911/implementer-66; ac4b9ac: Principal seat, Session: 8e509911. --session-check and git diff --check exit 0.
Merge: git merge-tree --write-tree HEAD origin/main exits 0; tree de3b2babca8484a5000523043281e141488a870e.
Queue quoted at reviewed head: `branch fm/006-they-them-and-english-se… @ ac4b9ac  wait: no pull request — no verdict on ac4b9ac`.
Queue quoted: `3 waiting on you: 0 merge, 0 close, 1 wait, 2 pushed without a pull request`.
Next: builder restores the historical quotations and fixes the wording, then Reviewer verifies the new head. No artifact is made obsolete by this evidence-only review.
path 5 — an answer is written and signed through the board; this verdict is no answer, and a merge rules nothing.
