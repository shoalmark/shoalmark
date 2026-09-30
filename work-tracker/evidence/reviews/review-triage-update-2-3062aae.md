# Review — `triage/update-2` (PR 138), the Owner's current path, at 3062aae (2026-09-30 19:17 CEST)

- **Reviewed:** `3062aaedf210a06a79b5ded13f1589f52853225a` (tree `b9bf9ea97be2cb2b1d0cc0142d21fb011f0ad0c1`).
  **Base:** `c97d6be96bb009e6b486bf7ff92c9a0668bf3d76` (`origin/main`, and the merge base).
- **Range:** `086c3fc` (the Owner's, signed) and `3062aae` (his merge of main: unsigned, clean). Net change: `TRIAGE.md` and
  `INDEX.md`, each +2 −6. **Tier: records**, one pass (`git diff --name-only origin/main...HEAD`).
- **Seat:** Reviewer `01a0ec25/reviewer-11`, Opus, delegated under Principal 01a0ec25 from the same root, so **not** an
  independent-session verdict. Under line 3 as it stands on main, a review of the Owner's TRIAGE lines reports and never blocks.
- **Signature:** `git verify-commit 086c3fc` against the tracked `work-tracker/allowed_signers` at `c97d6be` (only the
  Owner's principal; unchanged since `792dbca`) gives a Good signature, ED25519 `SHA256:uNcU…zCQ`, exit 0. Limit: this
  proves the key, not the hand (FM-007). It is not a touch `-sk` key, so the never-blocks clause holds. `3062aae` is unsigned,
  but TRIAGE.md there is byte-identical to `086c3fc`, and main has not touched the file since `792dbca`.
- **Verdict: READY WITH FINDINGS.** One P2 and five P3s, reported, not blocking. The Owner decides.

## Findings

- **R1 (P2): line 1's baseline cannot be traced here.** *10.5:1* appears on no branch outside this PR. The one measured
  baseline for this repository is on PR 131's page (unmerged, `c7ac2db`): 4.2:1 for 2026-09-22 to 09-29. That page also
  rules *no other project's numbers*. Fix: replace `The shadow week stood at 10.5:1 here;` with `The shadow week
  (2026-09-22 to 2026-09-29) stood at 4.2:1 here;`, or name the source and window of 10.5:1.
- **R2 (P3): the link resolves only on PR 131.** `evidence/FM-032/records-to-product-ratio.md` is on neither `c97d6be` nor
  `3062aae`. Fix: merge PR 131 first, or replace `([definition](evidence/FM-032/records-to-product-ratio.md))` with
  `(its definition: FM-032, PR 131)`.
- **R3 (P3): the terms do not match the definition.** *Raptor 3* is defined nowhere. *records-to-code* conflicts with the
  page's *records-to-product*, where product is everything outside `work-tracker/`. Fix: replace `Raptor 3: records follow
  code. The records-to-code ratio` with `Records follow product. The records-to-product ratio`.
- **R4 (P3): line 2 describes more than the tool reads.** At `3062aae`, `--queue` takes a verdict from `Reviewed: <sha>` plus
  a verdict word in the subject (`shoalmark.py:1700–1709`). It covers a verdict that writes no file (`addenda_between`,
  `:1438`). Nothing reads `Base:`, `Tier:` or `Checks:`: only `Reviewed`, `Session` and `Worktree` are read. Nothing requires
  a critical change's evidence file or an independent session (`verdict_reports`, `:5416`, only reports). A fix-forward
  commit on the branch after the verdict leaves `wait: no verdict on <head>`. Fix: replace `as a Reviewed: line in the
  commit` with `as the verdict commit's trailers Reviewed:, Base:, Tier: and Checks:`, and `findings are fixed forward and
  named in the commit` with `findings are fixed forward in the next change and named in the verdict commit`.
- **R5 (P3): stale second copies.** `AGENTS.md:83` cites `(path 5)`, a line this change deletes. Fix: delete ` (path 5)`.
  `AGENTS.md:60–64` (FM-032 S1, `ffa63b8`) keeps `Code keeps the full loop: pass, fix, verify, until READY` and `a P2 or
  above sends it back`, which conflict with line 2. Fix: replace the first with `Other code takes one inline Reviewer pass;
  critical work keeps an independent session's evidence file (the current path, line 2).`, and state whether a P2 still
  sends a change back. Under line 2, a seat changing AGENTS.md rules is critical. The next triage pass re-judges tiers that
  cite old numbers (FM-037's *critical under path line 3*).
- **R6 (P3): the signed subject understates the change.** *Current path item 1 added* also rewrote old line 3 as line 2 and
  removed old lines 1, 2, 4, 5 and 6. Fix: say so in the merge commit's message. The signed history stays unamended.

## Checks and quality read

- `git diff --check c97d6be 3062aae`: exit 0. `python3 shoalmark.py --check` at `3062aae`: exit 0 (INDEX fresh; *the
  Owner's two sections: guarded — … 1 change them …, each his own commit*).
- INDEX's two path lines are byte-identical to TRIAGE's, with no other net INDEX change.
- `--check` on this file's tree, before the commit: exit 0.
- Not run: the core, integration, browser and build suites, which are CI's on PR 138.
- **Quality read:** R1–R6 are wording and cross-references. No product line changed; INDEX was regenerated faithfully.
  This pass: records +51, product +0.
