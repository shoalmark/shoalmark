# Review — FM-029 and FM-030 on the replaced chain

- **Date:** 2026-09-24, 10:32 CEST (`date`)
- **Seat:** Reviewer (`reviewer@seat`) · **Session:** `e8e309df/reviewer-7` · **Model:** Claude Opus 5.5
- **Tip reviewed:** `97e9acc` on `fm/029-the-word-accepted-and-the-hands-still-owed`. The branch holds two commits on
  `main` `4b472cc`:
  - `137d9ba`: the Owner's commit. It is signed; `%G?` prints `G`, signer `holgoijo@gmail.com`. It holds the two
    trackers and INDEX.md.
  - `97e9acc`: the Principal's commit (`principal@seat`, session `e8e309df`). It holds the reference edits and the
    session row.
- **Main has moved** to `81d10f8`, which brings only TRIAGE.md and INDEX.md (PR 43). `git merge-tree --write-tree
  origin/main HEAD` exits 0, so the branch merges without conflict.
- **The code is unchanged.** `shoalmark.py` at the tip, at `4b472cc` and at `81d10f8` is byte-identical to `cdd6e3f`
  (`v0.17.8`, `62db9f8`), so every citation pinned to `cdd6e3f` also holds on today's `main`.
- **Independence:** this verdict counts as *same session* in `--check`'s weekly count, because this seat is a
  sub-session of `e8e309df`.
- **The removed detail:** some detail was taken out of the record when the earlier chain was replaced. This file calls
  it *the removed detail* and nothing else.

## The checks

### (a) No removed detail anywhere in the chain

- **What was searched:** every element of the removed detail, each case-insensitively and in each spelling I know of.
- **Where:**
  - `git log -p origin/main..HEAD`, with messages and full patches (264 lines);
  - both trackers, `sessions.md` and `INDEX.md` at the tip;
  - the two commit messages alone.
- **Result:** zero hits everywhere.
- **The sessions row:** 97e9acc adds `e8e309df` with *the Owner, 2026-09-24*, a date alone.
- **Outside the chain:** files that predate this chain still hold one of the three. See R18.

### (b) The text equals `1786ea2`'s apart from the redaction and the reference edits

The earlier tip `1786ea2` is still in this worktree's object store, so it could be compared directly.

**`137d9ba` against `1786ea2`:**
- FM-029 is byte-identical (`git diff --quiet` exits 0).
- FM-030 differs in one line, `:14`. The removed detail there became *morning*.

**`97e9acc` against `137d9ba`:** two places per tracker, nothing else.
- *What is true now*, `:15–16`: the pointer to the earlier review becomes *a first review ran on an earlier chain of
  this branch, which was replaced before its merge … it found R1–R16, and this text closes R1–R10*.
- The ship log's one row, `:84`: *… this text closes FM-0xx's share of R1–R10, and R11–R15 stay open*.

Both files stay 84 lines long, so every pointer below into them is unchanged.

**So:** R1–R10 stay closed as they were verified on `1786ea2` (restated below), and R11–R15 are open as the text
says. One part of R11 was closed by the reference edit itself (see R11).

### (c) Every line citation holds at `cdd6e3f`

- **The 28 code lines:** the trackers cite `:287 :291 :700–709 :708 :741–752 :756 :760 :780 :785 :839 :893 :945 :970
  :1008 :1264–1268 :1292 :1757–1763 :2803 :2855 :2859–2860`. A script read each line from `git show
  cdd6e3f:shoalmark.py` and matched the text the tracker says is there, for 28 lines in all. There were **0
  mismatches**.
- **The page lines:** `docs/signing.md:95`, `docs/de/signing.md:97` and `FM-023:171` also hold.
- **`:760`:** `--owner` dispatches straight to `owner_digest` (`:3734–3735`), and `:759–760` print *NOTHING NEEDS THE
  OWNER.* first whenever the queue is empty.

### (d) The tree and both suites

| run | result |
|---|---|
| `python3 shoalmark.py` | INDEX.md with 31 trackers, 0 unknown-status |
| `python3 shoalmark.py --check` | exit 0 (notes only) |
| `test_shoalmark.py` | all green, 264 checks, on Python 3.14.3 and on `/usr/bin/python3` 3.9.6 |
| `test_core.py` | all green, 148 checks, on the same two |

**Re-run first-hand this session** on the scratch copy from the first review (a fresh `git init` with a copy of the
same `shoalmark.py`, byte-identical by `cmp`):
- An accepted action ask is still absent from `--owner` (*NOTHING NEEDS THE OWNER.*) and from `--standup` (*0 item(s)
  — nothing needs the Owner today.*).
- `--answered` still lists it for a seat.
- A tracker set to `next: owner` with no ask lines still fails `--check` with 2 violations (R15).

## The earlier findings, restated for the record

The trackers name R1–R16. The file that defined them went with the earlier chain, so they are restated here, without
the removed detail. The pointers are into the current files.

### Closed (verified on `1786ea2`; the text is unchanged since)

| R | was | what it was | closed by |
|---|---|---|---|
| R1 | P2 | FM-029 claimed no migration, but `--clear-ask` strips `ask-proposal:` / `ask-options:` (`:2803`, `:2855`), so a cleared exchange loses the proposal | FM-029 `:41–44`, and Done when `:66–70` |
| R2 | P2 | a plain equality test reads the proposal as changed text, because the writers rewrite `"` and whitespace (`:1264`, `:839`, `:945`) | FM-029 `:37–40`, and the check at `:75–78`; the remainder is R12 |
| R3 | P2 | the board and the digest show no answered ask (`:1292`, `:708`), yet FM-029 required both to label one | FM-029 `:49–51` and `:71–72` |
| R4 | P3 | the recovery at `:1008` and the schema text at `:291` read the word; FM-017 was not considered | FM-029 `:53–54`, `:73–74`, and `considered:` |
| R5 | P2 | FM-030 blamed a missing sentence, but a shipped triage rule sends the run away (`:1760–1761`) | FM-030 `:42–46` and `:73–75`; the wording is R13 and R15 |
| R6 | P2 | nothing required the first lines to stop saying *nothing*; `--owner` has no heading; the board was left out | FM-030 `:59–64`; the remainder is R12 |
| R7 | P3 | four texts say an answer leaves his queue (`:970`, `:291`, both signing pages) | FM-030 `:39–40` and `:71–72` |
| R8 | P3 | one bullet held four requirements, one of them a new `--clear-ask` argument left implicit | FM-030 `:59–66` |
| R9 | P3 | FM-023 was not considered | FM-030 `considered:` and `:48–49` |
| R10 | P3 | the removed detail was in the session row and in FM-030 | the replaced chain |
| R16 | P3 | the removed detail was still in the earlier chain's history | the replaced chain: this chain holds none of it (check a) |

### Carried open

#### R11 · P3 · FM-029 says `--clear-ask` writes *only the question and the answer*

- **What:** `FM-029…md:42–43`. `--clear-ask` also writes the date and `answered-by` (`:2859–2860`).
- **Already closed:** R11's other half, a miscount in FM-029's ship log, was closed by `97e9acc`'s rewrite of that row.
- **What closes it:** *only the date, the question, the answer and who answered*.

#### R12 · P3 · Three edge cases have no expected reading, and a promised item keeps its answer buttons

- **FM-029 (`:75–78`):** the check lists bare `accepted`, a hand-written em-dash answer and an ask with no proposal,
  but not what each must read as. So the check cannot fail for them.
- **FM-030 (`:61`):** a promised item stays on the board's waiting list. That list draws *accept* / *reject* on every
  row with an ask (`:1290`), and a second `--answer` is refused (`:844–846`).
- **What closes it:**
  - FM-029: *bare → the proposal; em dash → read like ` - `; no proposal → the builder's word, stated*.
  - FM-030: *a promised item carries no answer buttons*.

#### R13 · P3 · The triage split omits the `owner` line and prescribes an ordering

- **The `owner` line:** `FM-030…md:42–46` quotes the `run` line (`:1760–1761`), not the `owner` line (`:1763`),
  which already lists *a read of production*. The rules claim the case twice, and first-fit order picks `run`.
- **The ordering:** *`owner` is tested before `run` for that case* (`:75`) asks for a per-case order that a
  first-fit list cannot have. What matters is the outcome: the `run` line excludes a run only his hands can make.
- ***his production*** (`:74`) is wider than *only his hands can make*.
- **What closes it:**
  - Quote `:1763`.
  - State the outcome, not the order.
  - Drop *his production*, or narrow it.

#### R14 · P3 · FM-029 requires cleared exchanges to read *relation not recorded*, but no surface shows them

- **What:** `FM-029…md:69–70` and `:77–78` require it. `--answered` lists only uncleared answers (`:744`), and its
  *acted on* lines give an id and a commit (`:752`).
- **Why it matters:** The check forces a reader of `## Asks` that no output uses.
- **What closes it:** Reword it as a constraint on any surface that shows a cleared exchange. Take it out of the check
  until such a surface exists.

#### R15 · P3 · A triage pass cannot apply the split: the gate refuses `next: owner` without the ask lines

- **What:** `apply_verdict` writes `next:` and no ask line (`:1975–1976`). `next: owner` without `ask:`, `ask-kind:`,
  `ask-since:` and `ask-proposal:` is refused (`ask_problems`, `:660–667`, applied in lint at `:2945`).
- **Reproduced again** this session (check d).
- **What closes it:** One sentence on who writes the `action` ask when a triage pass is the classifier.

## New findings

### R17 · P3 · The trackers name R1–R16 but not where they are recorded

- **What:** `FM-029…md:15–16` and `FM-030…md:15–16` and both ship logs say *a first review … found R1–R16* and
  *R11–R15 stay open*. They do not name a file, and the file that defined them was removed with the earlier chain.
- **Why it matters:** Until this file lands, five open items point at nothing in the record. The Owner's *never*
  line in TRIAGE.md includes *nothing that is not in the record*. The text also still says R11–R15 stay open, although
  half of R11 is now closed.
- **What closes it:** Point both trackers at this file
  (`evidence/reviews/review-fm-029-the-word-accepted-and-the-hands-still-owed.md`), which restates R1–R16 above.

### R18 · P3 · Outside this chain: older evidence on `main` still holds one element of the removed detail

- **What:** an element of the removed detail appears in six files that predate this chain and are already on `main`:
  - `work-tracker/evidence/FM-001/port/build-test-core-from-the-origin.py`;
  - `work-tracker/evidence/FM-001/port/shoalmark.toml`;
  - `work-tracker/evidence/FM-001/port/theme.css`;
  - `work-tracker/evidence/FM-001/seam-bprime-rd.md`;
  - `work-tracker/evidence/FM-002/brand-layers-rd.md`;
  - `work-tracker/evidence/FM-002/examples/origin.theme.css`.
- **Why it matters:** The Owner's *never* line now forbids non-redacted data in records.
- **Not held against this verdict:** this branch adds none of it.
- **What closes it:** A redaction tracker, or a ruling that this evidence is exempt. That is the Principal's call.

## Verdict

**READY WITH FINDINGS on `97e9acc`: R11–R15 carried open, and R17–R18 new, all P3.**

- The chain carries none of the removed detail.
- The tracker text is `1786ea2`'s, except for the redaction and the reference edits.
- R1–R10 and R16 are closed.
- Every citation holds at `cdd6e3f`, and the code is unchanged on today's `main`.
- `--check` is clean, and both suites are green on both Pythons.
- The branch merges cleanly onto `81d10f8`.
