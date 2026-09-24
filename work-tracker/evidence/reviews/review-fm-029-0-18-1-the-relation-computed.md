# Review — release 0.18.1 at ad37f41 (2026-09-24 15:50 CEST, Reviewer, session `8e509911/reviewer-1`)

**Scope.** Branch `fm/029-0-18-1-the-relation-computed`, tip `ad37f41` (`ad37f41ec36629a443c1779c21ff2336bf1b1ad0`),
on `v0.18.0` = `origin/main` `095f1d3`. It is release **0.18.1**: `VERSION` says 0.18.1, and CHANGELOG §0.18.1 and
FM-029's ruled slice are the contract.
- **The ruling.** The Owner's signed answer is `140f799`, 14:24:00, `G holgoijo@gmail.com`: *"accepted - the relation
  only — no new verbs"*. That is candidate 1, the second option and not the proposal, so the answer is itself a case.
- **The commits:**
  - `4dfb999` code and tests, `4446b90` docs, VERSION and R9, and `68eeee6` FM-029's tracker, all by the Implementer
    under `8e509911/implementer-9` in `shoalmark-impl-2`. That is the id the 0.18.0 registry build used, which the
    report allows.
  - `ad37f41`, the principal seat's `--clear-ask FM-029 build`, under `8e509911`.
- **Tier: code.** The range includes `shoalmark.py`, both suites and the labels. The full loop applies.
- **Independence:** the same session root, `8e509911`. This is reported, not refused.

## What I ran, and what came back

**Gates and suites at `ad37f41`.**
- `--check` exits 0, with the freeze line: 16 open, at or above 8, only bug filings.
- `--session-check` exits 0.
- `python3 shoalmark.py` is idempotent: `git status --porcelain` stays empty.
- `test_shoalmark.py` is all green, 298 ok, on Python 3.14 and on `/usr/bin/python3` 3.9.6.
- `test_core.py` is all green, 148 ok, on both.
- 298 + 148 = 446, which is the count claimed.

**The relation, case by case.** I ran `answer_relation` and `relation_text` from the tip over 24 cases. The proposal
was `ship "the importer"  now`, with a double quote and a double space, and it was option 1 of three.

| Answer | Reads |
|---|---|
| `accepted` (bare) | accepted the proposal |
| `accepted - ship 'the importer' now` (as `--answer` writes it) | accepted the proposal |
| `accepted - ship "the importer"  now` (raw) | accepted the proposal |
| `accepted - wait for the audit` · `Accepted - …` | chose option 2: wait for the audit |
| `accepted - neither — split it` (an em dash inside the option) | chose option 3: neither — split it |
| `accepted - wait, but only a week` | accepted with a change |
| `accepted — wait for the audit` · `accepted — something else` (hand, em dash) | chose option 2 · accepted with a change |
| `rejected - <a 78-character reason>` · `rejected` | rejected: the question mixes two things, split it… · rejected |
| `revoked - the audit found a hole` | revoked: the audit found a hole |
| `accepted - do it`, no proposal and no options · `accepted`, options but no proposal | relation not computable |
| `accepted - wait for the audit`, no proposal, options | chose option 2 |
| `approved - …` · `accepted-…` · `accepted -` · `accepted: …` · `accepted – …` (en dash) | relation not computable |
| `accepted - Wait for the audit` (case differs from the option) | accepted with a change |
| no answer | nothing |

- Every case the CHANGELOG bullet names reads as it says, with `--answer`'s normalisation on both sides.
- Case is not normalised, and the CHANGELOG does not say it is.
- A form the parser does not know is never guessed.

**Where it prints.**
- **`--answered` here:**
  - FM-007 reads *accepted the proposal*.
  - Acted on: FM-029 in `ad37f41` reads *chose option 2: the relation only — no new verbs*. FM-031 in `fd6ddd2` and
    FM-032 in `4af2c9b` read *relation not computable*. On FM-032's commit, see R1.
- **The board's tracker view,** rendered in headless Chrome from a temporary repository whose answer took option 2:
  - `— accepted - wait for the audit · chose option 2: wait for the audit · 2026-09-24 · Owner · supersedes 0a89cdd`.
  - With `examples/de/labels.yaml` as the brand's labels:
    `… · Option 2 gewählt: wait for the audit · … · ersetzt 0a89cdd`.
  - All six labels are in both tables.
- **`--clear-ask`** in that repository wrote `**relation** — chose option 2: wait for the audit` under `**answered** —`.
  After the commit, `--answered` named the clearing commit, with that relation.
- **`--owner` and `--standup`** print none. The ruled candidate 1 puts it there *wherever FM-030 lists an answer*.
  FM-030 is not built, so nothing lists one, and none is what the ruling asks for.

**The signed line is untouched.**
- `140f799`'s line was `accepted - the relation only — no new verbs`, and it moved into FM-029's `## Asks` record
  unchanged.
- `--answer` and the dialog write what they wrote before.
- The FM-029 record reads `**answered** — accepted - the relation only — no new verbs · holgo99`, then
  `**relation** — chose option 2: the relation only — no new verbs`.

**The em-dash reading is the ruling, not a deviation.**
- Candidate 1, the option the Owner signed, says *Bare `accepted` and the schema's em-dash form parse too*.
- *Done when*'s check list names *a hand-written em-dash answer*.
- Reading `accepted — x` as `accepted - x` does both.
- The schema's `answer` row now names ` - ` as the form and says that a hand's ` — ` reads as ` - `.

**The recovery.** In a temporary repository, a half-written `accepted - something new` over a committed answer gives
`… --answer FM-001 accept "something new" --supersede`. A half-written `revoked - the audit is late` gives
`… revoke "the audit is late"`, with no `--supersede`.

**R8 and R9 of 0.18.0.**
- **R8, closed.** In the queue test repository, with the owner seat given to another name:
  - the Owner's signed PR 9 and unsigned PR 10 both read `wait: not an answerer (owner@x)`;
  - with the email-keyed owner, they read `merge: your answer` and `wait: unsigned answer`;
  - with the signers file unset, PR 9 reads `wait: answer not verified here — …`.

  In the parent project's scratch clone, its two signed answers read `merge`, and a principal seat's commit reads
  `wait: not an answerer (principal@seat)`.
- **R9, closed:** *12:53:19* is now in every place, and a 15:17 row names both clocks. See R4 for how.
- **AGENTS.md's cap paragraph** says *merged 12:53:19*. That goes beyond the brief, but it is a fact, the forge's
  `mergedAt` 10:53:19Z, and it agrees with FM-031. Fine.

**The docs.**
- README's *the Owner's answer*, *acting on an answer* and *what to merge* rows name the relation, the `**relation** —`
  line and `wait: not an answerer`.
- §5 has a `wait: not an answerer (<author>)` row.
- `--schema`'s `answer` row lists the six readings.
- `--help` names the relation on `--answer`, `--answered` and `--clear-ask`, and the new wait on `--queue`.

**The diff as a whole.**
- **New code:** `answer_relation`, `relation_text`, `recorded_relation`, the row's twelfth field, the view's `<i>` span,
  `--answered`'s two lines, `clear_ask`'s record line, the recovery's third word and `--supersede`, and
  `answer_reading`'s early wait.
- Nothing else in `shoalmark.py` changed.
- `test_core.py` changes only the two row-shape patterns, for the new field.

## The CHANGELOG's claims, one by one

| # | Claim (§0.18.1) | |
|---|---|---|
| 1 | The relation computed from `answer:`, `ask-proposal:` and `ask-options:`, the answer's normalisation on both sides | ✓ |
| 2 | Its six readings, and a hand's `accepted — <text>` read as `accepted - <text>` | ✓ |
| 3 | Printed by `--answered` (both lines), the board's tracker view, and the `**relation** —` line `--clear-ask` writes | ✓ (R1: the acted-on line's commit) |
| 4 | A record written before reads *relation not computable*, never a guess | ✓ as written · R2 against the ruling's words |
| 5 | `--owner` and `--standup` print none | ✓, as the ruling asks |
| 6 | The signed line and the commit subject unchanged; `--answer` and the dialog write what they wrote | ✓ |
| 7 | `--queue`: `wait: not an answerer (<author>)`, signed or not; the other two waits for an author who may answer | ✓ |
| 8 | The recovery gives `revoked` again as `revoke`, and a replaced answer with `--supersede` | ✓ |
| 9 | Six labels, English built in, German in `examples/de/labels.yaml` | ✓ |
| 10 | Nothing to do on upgrade: no key, no hook line, no command changes | ✓ |

## Findings

**R1 · P3 · confidence high · *acted on in <sha>* can name a commit that did not clear the ask.** The coordinator asked
about this line, which 0.18.1 now prints the relation on. `acted_on` (`:3270`, `:3286`) takes
`git log -1 --full-history -G '^ask:'`. That is the newest commit **whose own diff** touches an `ask:` line, and it
fails in two ways:
- **An uncommitted clear.** At `68eeee6` with `--clear-ask FM-029 build` run and not yet committed, `--answered` says
  *FM-029 — acted on in `3c1c334`*. That is the 13:37 rewrite of the question, 46 minutes before the Owner answered.
  This is the reading the coordinator saw. At `ad37f41`, where the clear is committed, it names `ad37f41`, which is
  right.
- **A clear made inside a merge.** FM-032's ask was cleared by the merge `8eaff7d`: both parents carry `ask:` and the
  merge does not. `-G` does not look at a merge's own change, so the line says *acted on in `4af2c9b`*, which is
  FM-032's filing at 09:35.
- The code predates this release (FM-008, `7bd728d`), but the line now carries the relation, so it states what the
  Owner's answer became against the wrong commit.
- **Fix.**
  - Where the working tree's tracker differs from HEAD's, say *acted on, not committed yet*.
  - Otherwise, name the first commit on HEAD's history whose tree lacks the `ask:` line while its parent's had it. That
    includes a merge that removes it against every parent.
  - Add a check for both.

**R2 · P3 · confidence high · A record from before the fix says *not computable*, where the ruling says *not
recorded*.**
- Candidate 1, as signed, says: *an exchange `--clear-ask` emptied before the fix reads *relation not recorded**.
  *Done when* says the same twice.
- The build gives such a record the same words as an answer with no proposal: *relation not computable*.
- Those are two different causes. In one, the proposal was never there. In the other, the proposal was there and the
  record dropped it.
- **Fix:** a seventh reading, `relation.unrecorded`: *relation not recorded*, for a record with no `**relation** —`
  line, in both label tables. Or, if one reading is wanted, *Done when* says so.

**R3 · P3 · confidence high · FM-029's record is behind its own tip.**
- ***What is true now*** (`:14`) still says *the ask waits to be cleared by the seat that holds `ask`*. `ad37f41`
  cleared it.
- **The ship log has no row for that clear.** FM-032's clear has one, at 12:45.
- ***Done when*'s first line** (`:116`) still asks that *a new answer says its relation to the proposal in the front
  matter* and *no longer writes `accepted` in front of an option that is not the proposal*.
  - The ruling excludes that: no new verbs, and the signed line unchanged.
  - The tracker's own *Against Done when* (`:110`) said that under candidate 1 *that line would be reworded*, and it was
    not.
  - As written, FM-029 can never close.
- **Fix:** rewrite *What is true now*, add one row for `ad37f41`, and reword the first *Done when* line to the ruling:
  every reading names the relation, and the signed line is unchanged.

**R4 · P3 · confidence high · R9's fix rewrote an append-only row.**
- FM-031's 12:55 ship-log row said *merged 12:53:18* at `37c73d0`, and now says *12:53:19*.
- AGENTS.md rule 1: *only the ship log is append-only*. The new 15:17 row says the row was changed, but the row itself
  no longer reads as written.
- 12:53:18 was also true, since it is `ed11081`'s commit time.
- **Fix:** restore the 12:55 row's *12:53:18*. The 15:17 row already names both clocks, and *What is true now* and
  AGENTS.md may keep the forge's 12:53:19.

**Verdict:** READY WITH FINDINGS. R1–R4 are all P3, fixed forward. The Owner may tag this tip.
