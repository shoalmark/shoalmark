# Review — FM-006, the GtM seat's claim screen

- **Date:** 2026-09-23, 23:15 CEST (`date`)
- **Seat:** Reviewer (`reviewer@seat`) · **Session:** `8e509911/reviewer-1` · **Model:** Claude Opus 5.5
- **Tip reviewed:** `a7a788a` on `fm/006-gtm-claim-screen`: 14 commits by `gtm@seat`. The branch is checked out in
  the GtM's own worktree, so this seat reviews it detached in its own.
- **Base:** it merges clean onto `origin/main` `2584705` (`git merge-tree --write-tree`: exit 0).
- **What it changes:**
  - `shoalmark.toml`: `gtm = "gtm@seat"`, added by `gtm@seat` itself in `809656e`;
  - `work-tracker/sessions.md`: six rows;
  - eleven files under `work-tracker/evidence/FM-006/`.

## Cold start

1. **What virtue do I bring?** Doubt, and credentials first. A branch that talked to an outside service is where a
   key lands in a file.
2. **How does it turn into blindness?** By treating one detector's silence as proof. So the files are also read by
   hand, and every version in the branch's history is scanned, not only the tip.
3. **What would show that failure here?** A key, token or `Authorization` header in any version of any file. A score
   that the committed code does not reproduce. A kill or a survivor missing from its ledger.
4. **Who gets the record, independently of me?** The Principal seat, then the Owner, who merges. This file disposes of
   nothing.

## 1 · Credentials — none

Every check below found no credential:

| scan | what was scanned | result |
|---|---|---|
| the consumer's secret-shape detector, read-only | scratch copies of the 12 changed files at the tip | exit 0, 12 files, 100 % coverage, **findings=0** |
| the same detector | **all 30 file versions** added across the 14 commits | exit 0, **findings=0** |
| a grep over the branch's whole patch history | *Authorization*, *Bearer*, *api_key*/*x-api-key*, *secret*, *password*, `sk-`, `ghp_`, `github_pat`, `xox[bp]-`, `AKIA`, `-----BEGIN`, *client_secret*, `"token"` | 0 hits |
| deletions on the branch | the 14 commits | none, so nothing was added and later hidden |

**Read by hand:**
- The `…-keys-…json` is an **answer key**, not a credential. It holds a seed, the word count per line, and a map
  `q001 … → {line, gate}` that un-shuffles the request's questions.
- The three response JSONs carry `model`, `answers`, `usage` (`input_tokens` / `output_tokens`, counts only), a
  `request_id` of the form `playground_…`, and `evaluation_time_ms`. No header, no key.
- The two scripts make no network call. `jev-gate-test-build.py` writes the request and the key file. The score
  script reads the two responses.
- The requests carry the page's lines and the pitch's facts. They carry no consumer's or client's name.

## 2 · The ledger

**Evidence classes.** Every row of the five screening tables carries one.

| table | rows | classes |
|---|---|---|
| `:71` | 13 | E 6, I 6, K 1 |
| `:255` | 4 | E 2, I 1, K 1 |
| `:688` | 2 | I 1, **F 1** |
| `:703` | 12 | K 4, I 7, E 1 |
| `:815` | 3 | I 3 |

See R1 on *F*. The reader table at `:883` has no class column; its cells are the seat's judgment, which the message
says (R2).

**Every kill and every survivor is in it.**
- **Pass one** (`:71`): G0 2, G1 2, G2 2, G3 2, G4 1, G5 1, three survive, 13 lines. That equals its summary at `:87`.
- **Pass three** (`:703`): G0 2 (and the control K2), G1 1, G3 3, G4 1, G5 2, three survive (N10, N11, N12), 12
  lines. That equals its summary at `:718`.

## 3 · The Jev runs

**Raw.** Each Jev file was added once and never touched again.

| file | added in |
|---|---|
| claim-screen request | `e1ef918` |
| claim-screen response | `47e049b` |
| gate-test request and keys | `e6518e8` |
| both gate-test responses and the score output | `65d5d43` |

**Rule first.**
- The gate test's rule is committed before either call, as code, in `e6518e8`: *the column counts only if all three
  controls hold and the repeat agrees within 0.1* (`:512`, `:547`).
- The claim screen's rule was written before its call (`:355`).

**Marked noise as ruled.**
- The claim screen: *C0 failed, so, by the rule written before the call, the column is read as noise* (`:435`).
- The gate test: *VERDICT … noise. The record blames the MODEL* (`:603`).

**Reproduced.**
- `jev-gate-test-build.py` rebuilt the request and the key file **byte-identical**.
- `jev-gate-test-score.py`, given both responses, printed output **identical** to the committed score file (whitespace
  aside): controls fail, the repeat fails on 12 of 17 first-fatal gates, **VERDICT: noise**.

## 4 · Sessions and gates

- All six GtM rows are closed, each with its end: `ee61f1fe`, `2ab3afad`, `c1652143`, `ad81b142`, `d578f49e`,
  `63f5b126`. The brief named two; the branch holds six.
- On the tip: `python3 shoalmark.py --check` exits 0, and `python3 shoalmark.py --session-check` exits 0.

## 5 · Names

`git diff origin/main...a7a788a` names no consumer and no client: 0 hits for either, for the consumer's tracker ids,
for `RV-` ids and for pull-request numbers. The outside service is named (*TypeSafe's Jev*); it is a vendor, not a
client.

## Findings

### R1 · P3 · The class *F* is used but not defined

- **What:** The ledger's legend (`:59–63`) defines **E**, **K** and **I**. Row K2 (`:691`) is classed **F**, *two
  adjectives before the noun (**F**)*.
- **What closes it:** Define *F* in the legend (a form count, done by eye or in code), or class the row **E** if the
  adjective count was executed.

### R2 · P3 · The per-reader table carries no evidence class

- **What:** `:883` assigns each line to *outside Owner*, *investor* or *both*. Every cell is the seat's judgment, as
  its message to the Owner says, but the table does not mark it.
- **What closes it:** A class column, **K**/**I**, as the other tables have.

### R3 · P3 · The score script reports *controls: all hold* when it is given no run

- **What:** `python3 jev-gate-test-score.py` with no arguments prints *controls: all hold* and *repeat: not run*. With
  zero responses loaded, the control check passes vacuously.
- **Cost:** The committed output was produced with both runs, and I reproduced it exactly, so no verdict is affected.
  But the decision rule's own code passes its controls on no data.
- **What closes it:** Refuse, with a non-zero exit, when fewer than the runs the rule needs are given.

## Observations for the Principal (not findings)

- **`gtm = "gtm@seat"` was added by the seat it names**, in its own first commit. `[seats]` gives an unlisted name no
  rights, and the GtM needs none, so the gate is untouched. The Owner's merge is the ratification, as the brief says.
- **This seat's verdicts count as *same session*** on this repository's report, as they are.

## Verdict

**READY WITH FINDINGS: R1, R2 and R3 (P3).**

- **No credential** in any file or any version on the branch. The detector and a hand read agree.
- The ledger's kills and survivors add up, and its Jev runs are raw and read as noise by rules committed first,
  reproduced here.
- The sessions are closed, the gates exit 0, and there are no names.
