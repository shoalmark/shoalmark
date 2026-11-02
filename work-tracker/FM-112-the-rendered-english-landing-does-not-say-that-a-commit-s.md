---
id: FM-112
status: Proposed
epic: FM-107
considered: FM-006, FM-111
tags: process
hook: "The docs' start page says a commit's date is when it was made, not when it was pushed, and how far the forge's push events confirm the count. The rendered English landing uses its own words, and they leave that out."
---

# FM-112 — the rendered English landing does not say that a commit's date is not when it was pushed

## What is true now

**2026-11-03 — filed; nothing is built.** It is the one of Slice L's three qualifiers that is still open, kept on the
Owner's word of 2 November, for the rendered English landing.
- `docs/index.md` says it: a commit's date is when it was made, not when it was pushed, and the forge's push
  events confirm the counted pull requests from 24 September 2026, 05:18 UTC on. Its Markdown twin has it too.
- The landing renders its own words. Its note, `board_small` in `overrides/partials/landing/en.html`, says how a
  pull request counts, and nothing of push time.
- The German landing's note leaves it out too. The German docs page has it.

## Why

A count that rests on commit dates is only as good as its reader's idea of what a date proves. The limit belongs where
the count is read.

## Done when

- [ ] The rendered English landing's note says that a commit's date is when it was made, not when it was pushed, and how far the push events confirm the count.

## Ship log

| Date | Event |
|---|---|
| 2026-11-03 | Filed as a child of FM-107, on the Owner's word of 2 November. Records only. |
