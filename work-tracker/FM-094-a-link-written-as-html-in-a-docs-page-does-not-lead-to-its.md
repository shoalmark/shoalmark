---
id: FM-094
status: Proposed
considered: FM-091, FM-006
tags: bug
hook: "A docs page's llms twin keeps a link only when the page writes it in Markdown. A link written as HTML, as the legal pages' language links were for one build, no longer leads to its twin, and nothing checks for it."
---

# FM-094 — a link written as HTML in a docs page does not lead to its target's twin in the page's llms twin

## What is true now

**Filed 2026-10-29 for v0.20.3; nothing is built.** On the Auditor's word of 29 October that the Designer's BF-103 (P4)
leaves [FM-091](FM-091-the-site-has-no-imprint-and-no-privacy-notice-and-its.md). The Owner knows.

- **What happened:**
  - BF-103 asked that the legal pages' language links carry `hreflang` and `lang`.
  - A Markdown link takes no attributes here, so FM-091's build wrote them as HTML `<a>` links.
  - `scripts/llms_txt.py` retargets only Markdown links. So in the four llms twins those links no longer led to the
    other twin.
  - FM-091 took them back to Markdown.
- **Two things are open:**
  - a language link that says its language, as BF-103 asks;
  - `llms_txt.py`'s handling of links written as HTML.

## Why

A reader of the llms twins follows the same links as a reader of the site. A language link that names its language
helps a screen reader say it right.

## Done when

- [ ] Each docs page's link to its twin in the other language carries `hreflang` and `lang` in the built page.
- [ ] Every link in a docs page, Markdown or HTML, leads in the page's llms twin to its target's twin, or the build
  refuses the page.
- [ ] A test holds both, with a mutant of each that is refused.

## Ship log

| Date | Event |
|---|---|
| 2026-10-29 | Filed for v0.20.3, on the Auditor's word of 29 October. Records only. |
