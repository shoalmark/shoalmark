# FM-006 — independent publication-gates re-verification

Date: 2026-09-29.
Reviewed: `c0e50be0a8a2e161d5c41354472bc109e9029db9`.
Branch: `fm/006-publication-gates` (fetched remote head verified).
Base: `origin/main`, `b041cb2dca136623ee9160d74ae5b39b0f1a7ba2`.
Merge base: `80d0811974a1d39b679cfd374c80109ddd62acce`.
Reviewer: `reviewer@seat`, session `01a0edae`.
Review branch: `fm/006-review-publication-a9703d9`.
Worktree: `/private/tmp/shoalmark-review-publication-a9703d9`.

**Tier: code, critical. Verdict: READY. R1 is closed; no open review findings.**

This is independent review clearance for the implementation. Required PR CI
must pass on the final revision before the Owner merges. It is not certification
of the after-scoring publication condition, live disclosure or deployment.

## Range and independence

The tier remains critical code from `git diff --name-only origin/main...HEAD`:
deployment validator, tests, requirements and Pages workflow, with site assets,
configuration and signing disclosure. I reviewed every follow-up hunk since
`a9703d9`, including the new parser, its dependency pin, regression suite,
workflow step and tracker/evidence updates.

Git confirms that `c0e50be` contains fix `6a68850` and the original independent
NOT READY verdict `7660ba2`, preserving both. Implementation session `01a0ec25`
differs from Reviewer root `01a0edae`; the earlier verdict is review evidence,
not implementation by this Reviewer. The original finding and initial
verification remain in
[`review-fm-006-publication-gates-a9703d9.md`](review-fm-006-publication-gates-a9703d9.md).

## R1 verification

The obsolete filename-suffix heuristic is removed. The validator now parses
`@font-face` source declarations with pinned **tinycss2 1.4.0**, validates their
URLs regardless of suffix, and checks destinations within the built site.
It follows local imports with cycle protection and checks nested rules and
inline style elements. The dependency is installed before the new regression
step and site validation in the Pages workflow.

Installed the updated `requirements-docs.txt` in an isolated Python 3.14.3
environment; installed the same parser pin in a separate Python 3.9.6
environment for compatibility verification. The Zensical build uses 3.14;
no claim is made that Zensical itself supports 3.9.

- `scripts/test_check_site.py -v`: **all four methods, covering 18 scenarios,
  pass on both interpreters**. These cover extensionless/local sources,
  external and protocol-relative sources, escapes, URL casing, fallback lists,
  nesting, inline styles, imported styles, missing files and commented examples.
- **Independent old-versus-fixed controls:** appended each original R1 source
  to the real generated fonts stylesheet in a disposable site copy:
  `https://example.invalid/font?id=plex` and
  `../assets/fonts/missing-font`. On both interpreters, the checker from
  `a9703d9` returns **0**; the checker at `c0e50be` returns **1** with the
  corresponding external-font or missing-font diagnostic. The old checker was
  executed with its repository location preserved so repository-link validation
  remained meaningful.
- **76 independent checks pass** across both interpreters: those eight
  old/fixed comparisons; removal of each of the 28 font assets separately;
  nested layer/supports font rules; escaped declaration/function spelling;
  Google import; a font path escaping to an existing file outside the artifact;
  an extensionless local stylesheet import cycle; and the restored site.
  The import cycle terminates and passes, while each negative case is refused.
- **Clean build:** Zensical **0.0.66**, `zensical build --clean`, exits 0 with
  no issues. `scripts/llms_txt.py site` produces 11 Markdown twins. Both
  interpreters accept the unmodified generated site.
- **Browser:** Chromium again renders landing, setup, EN/DE signing and agents
  contract under `/shoalmark/`. All font requests remain local; seven loaded
  faces on landing, eight on each documentation page. No local HTTP failures,
  script errors or Google font requests. The expected signing paragraphs are
  present. The unchanged GitHub version lookup still returns the disclosed
  `releases/latest` 404; no zero-network claim is made.

Font bytes, stylesheets, template, signing prose, Zensical configuration and
the original scan/browser data files are byte-identical to the first reviewed
head. Their upstream font/license provenance and captured-history scan remain
supported by the first independent pass; this follow-up does not claim a new
whole-history census or repeat the historical tag's CI as branch CI.

## Gates and next move

At `c0e50be`, `python3 shoalmark.py --check` exits **0**, including build
judgement and the Owner-section guard. `git diff --check a9703d9..HEAD` exits
0. Merge simulation against the fetched base is clean, tree
`9d70f4ec63dae6023679e5608b3afd1e85d937bd`. No tool implementation changed in
the follow-up; validation was concentrated on the changed site gate and build.
No new full tool-suite run is claimed.

The remote branch has no PR at this pre-commit observation. On the Owner's
latest instruction, include this READY verdict on the publication branch,
then open its PR so required CI can run once on the reviewed revision with
evidence included. The Owner merges after those checks; deployment and live
verification follow separately. The after-scoring condition and signed
publication act remain open. No release tag is due from this review.

No merge into main, deployment, tag or repository-setting change was made.
