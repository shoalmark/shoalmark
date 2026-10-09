# FM-006: PR 150, the landing label, the review as merged at f84ad4a

Verdict: **READY WITH FINDINGS**: five P3s, RV-2750 to RV-2754; no P1, no P2.
Reviewed: f84ad4a302677e358bd0cf0e4a92864249b0e181, `git diff 1ee8d42 f84ad4a`: three commits, 20cd853, d0679ad and 046ec78, against the Owner's rulings of 8 October 2026. Tier: code (`git diff --name-only`: `overrides/landing.html`, `test_shoalmark.py`). Scope: the top bar, the footer's link, the footer's line, their template comments and the check that pins them.

## What holds

- The top bar reads `release<b>v0.19.1</b>`; the footer's link is `releases/tag/v0.19.1` and reads v0.19.1. The footer's line is the Owner's words byte for byte, and "The release: read at its cut" is gone. The top bar's hi-score 71/82, wrecks 27 and open 10 are 1ee8d42's. No v0.19.0 stands outside a template comment.
- The check at `test_shoalmark.py:3541` (strings `:3546–3547`) pins the footer's line whole.
- 8 October 2026 is the CHANGELOG heading's day (`## 0.19.1 — 2026-10-08`, `CHANGELOG.md:5`). `releases/tag/v0.19.1` resolves: tag at 1ee8d421, published 2026-10-08T03:08:45Z. "run --install-hook again on your default branch" is the CHANGELOG's upgrade line (`CHANGELOG.md:92`); "then --check once" is the 0.19.1 lead's (`:7`).
- The template's facts: the tag is 1ee8d421; 7b87ae2 is its ancestor, with VERSION and CHANGELOG.md the same blobs at both; 5ae97b7 is the ruling's commit; the setup page's clone tag is v0.19.1 (`docs/setup.md:8`).
- The live page's three lines equal f84ad4a's. f84ad4a's tree is 046ec78's (2137990), on which CI run 37723667636 passed all five suites.

## Findings

- **RV-2750 · P3 · tests:** the check pins the footer's line only; no check pins the top bar's version or the footer's link (the control below). Fix: end `test_shoalmark.py:3547` with `and "Counted on 1 October 2026 with <code>gh</code>" in _rd("overrides/landing.html") and '<div role="listitem">release<b>v0.19.1</b></div>' in _rd("overrides/landing.html") and 'releases/tag/v0.19.1" style="color:#b4c3d1">v0.19.1</a>' in _rd("overrides/landing.html"))`.
- **RV-2751 · P3 · template comment, `landing.html:526`:** "the wrecks and the headline from evidence/FM-006/landing/start-page/facts.mjs" names a headline that the line no longer carries. Fix: "the wrecks and the headline from" → "the wrecks from".
- **RV-2752 · P3 · template comment, `landing.html:526`:** it opens "the release re-read at the v0.19.1 cut 7b87ae2" and ends "No reading was made at 0.19.1's cut". Fix: "the release re-read at the v0.19.1 cut 7b87ae2 (the tag v0.19.1 is 1ee8d421; VERSION and CHANGELOG.md are the same at both)" → "the release v0.19.1 (the tag is 1ee8d421; VERSION and CHANGELOG.md are the same there as at the cut commit 7b87ae2)".
- **RV-2753 · P3 · template comment, `landing.html:329`:** "the top bar, the board excerpt, the high scores, the wrecks and the footer as the Auditor read them at the cut c830470" covers the top bar's release and the footer's release, which now read v0.19.1. Fix: "the top bar, the board excerpt, the high scores, the wrecks and the footer as" → "the top bar's hi-score, wrecks and open, the board excerpt, the high scores, the wrecks and the footer's reading, as".
- **RV-2754 · P3 · records, a second copy:** `CHANGELOG.md:7` and the release page that the footer links to read "upgrade, then run `--check` once."; the footer and `--install-hook`'s help (`shoalmark.py:8158`) also say to re-run `--install-hook` after upgrading. Fix: in `CHANGELOG.md:7`, replace the lead with "**0.19.1 is a security release: upgrade, run `--install-hook` again on your default branch, then run `--check` once.**", and change the release page's first line to match.

## Commands and controls: 2026-10-08, CEST, as `date` printed each

- `test_shoalmark.py:3539–3547`, verbatim from f84ad4a, run against f84ad4a's tree: ok, exit 0 (09:58:47). Control: the same lines against f84ad4a's tree with 1ee8d42's `overrides/landing.html` in place: FAIL, exit 1 (09:58:47). Control: against f84ad4a's tree with only the top bar and the footer's link at v0.19.0: ok, exit 0 (10:05:18, RV-2750).
- `gh release view v0.19.1`: exit 0 (10:00:04). `curl -s https://shoalmark.github.io/shoalmark/`: HTTP 200; its top bar, footer link and footer line equal f84ad4a's and the Owner's words (10:00:18).
- `--check` exit 0 and `--session-check` exit 0, with this file in place, before the commit (10:07:17–10:07:23).

Quality read: the defects are RV-2750 to RV-2754; the rest reads clean.
