# Cold review — FM-042 Stage 0 at 72daac8

Reviewed: 72daac8387c51315c1574d1a08735eff7cdc5827
Seat: independent reviewer; session 1640a2c7; isolated worktree shoalmark-fm042-cold; 2026-09-30.
Verdict: NOT READY.
Tier: documentation by FM-032 S1; critical under path line 3 because AGENTS.md rules changed. Diff: 11 files, +196 −9; no Python, toml, hook or test; no suites run.

## Checks

- The primary convention covers stable id / shall / source / acceptance, body citations, test names, signed changes, clause-derived company obligations, signed non-applicability, no standard text or compliance claim, later Stage 1/2 asks, and replacement of restated behaviour. Entry summaries refer to it.
- Scratch clone at target with its tracked allowed_signers configured: front-matter `satisfies: REQ-001` makes --check exit 4 with unknown-key lint; body `Satisfies: REQ-001` makes --check exit 0.
- Re-verification: RV-2000's four-entry citation fix and RV-2001's absolute link are present; RV-2002's independence condition is met by this session. RV-2003/2004's signed non-applicability and German derivation/signiert fixes are present. RV-2005 points to main rather than the old clone; RV-2006's premature completion claim is removed, but its counts are stale again.
- Claim screen applied by hand; the scoring service was not called. G0: these are convention/trial entries, not twelve-word pitch slots; jargon is explained and REQ ids are the necessary syntax. G1: readable English and native German plural ihr/euer register (Legt), Anforderung / Nachweis / Abnahmekriterium; no native human reader. G2: README convention-only claim stands; German section stands, but step 3 fails below. G3: no flattery or rubber-stamping. G4: one text tells developer/tester what changes and signed changes preserve the Owner's decision. G5: a concrete contract adds evidence beyond the bar.
- Controls: the screen's C0 dies at G0 (third-person addressee); invented compliant-project English/German controls die at G2. Compliance grep: requirements/README.md:38 and AGENTS.md:40 are prohibitions; ADOPT.de.md:79 uses “erfülle die Norm”, also a prohibition, missed by literal “erfüllt die Norm”. No positive claim.
- Scratch venv: zensical 0.0.66, tinycss2 1.4.0; zensical build --clean, scripts/llms_txt.py site, scripts/check_site.py site each exit 0. macOS run, no CI claim.
- FM-006 signal is generic and anonymised; Signals precedes Acts and the signal's ship-log row is first. Newly authored convention lines disclose no named prospect or external incident. The worksheet's FM-041 Now cell and prior review reproduce pre-existing names/relay/hash: a literal “every added line” anonymity rule is not met; no new disclosure inferred.
- v0.18.6 shoalmark.py SHA-256 is 5330ee0679ee9937a88c91ae3b36a9416f7003c706983ff0bd4e2a0bbfa971ee, matching step 2. Tag examples/de/ contains TEMPLATE.md, TRIAGE.md, labels.yaml, shoalmark.toml, tafel.png; four setup files exist and their descriptions match.
- FM-042: triaged 2026-09-30, rank 10, tier P2, next build, In Progress; f3d19dd changes only tracker/INDEX. Worksheet: FM-042 keep P2 #10 build; FM-041 keep P3 build. FM-033 differs only by removal of rank: 10. The Owner's go is one marked normalised line at 10:19:57, with no relay/hash in that record; original transcript/time not independently available here.
- Numstat f3d19dd..72daac8: all files Owner 93 records / 34 product / 7 deleted, ratio 50 / 77 / 7; excluding the prior review as the row specifies: Owner 51 / 34 / 7, ratio 8 / 77 / 7.
- --check exits 0: 17 commits, every build commit under a judged In Progress tracker; --session-check exits 0; merge-tree origin/main 72daac8 exits 0, tree 45d538d7f284145d42138be8f79872f802b3f57e.
- --queue: “branch fm/042-a-requirements-layer-sta… @ 72daac8  wait: no pull request — no verdict on 72daac8”; “5 waiting on you: 0 merge, 0 close, 2 wait, 3 pushed without a pull request”.
- All 17 commits carry Session, Worktree and Co-Authored-By: two principal, fourteen implementer, one same-session reviewer; this review's session has a different root.

## Findings

- RV-2030 · P2 — ADOPT.de.md:38 sends shoalmark.toml to probe/shoalmark.toml after :35 cd probe, a nonexistent nested destination. Exact fix: replace the destination `probe/shoalmark.toml` with `shoalmark.toml`; add `Die Zielordner vorher anlegen.` before the copy instructions. Scratch clone at v0.18.6: vendor exits 0; literal destination raises FileNotFoundError; corrected destination plus created folders lets --init exit 0.
- RV-2031 · P3 — FM-042's ship-log row has stale counts. Exact fix: `51 records added, 34 product added, 7 deleted` and `8 records added, 77 product added, 7 deleted`, preserving its explicit exclusion of the prior review; recount after any further edits.
- RV-2032 · P3 — FM-042's current Stage 0 paragraph still says `trackers cite ids (`satisfies:`)`, contrary to the corrected convention. Exact fix: `trackers cite ids in a body line (`Satisfies: REQ-001`), tests name them`.

Quality read: the convention is clear; the trial has a concrete path defect and the canonical tracker lags the rework. No content fixes made by this review.

path 5 — a merge rules nothing.
