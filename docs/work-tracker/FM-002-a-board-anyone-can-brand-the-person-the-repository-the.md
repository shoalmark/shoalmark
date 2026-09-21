---
id: FM-002
status: In Progress
considered: FM-001
next: run
hook: "The board can carry a name in the browser tab and a theme.css — nothing else: no name on the page, no logo, English only. And several kinds of user want to brand it at once: several people looking at one repository's board, several repositories, an organisation shipping its house brand into every repository it sets up. One rule, three files, four places — to be proven before it is built."
---

# FM-002 — A board anyone can brand — the person, the repository, the organisation

## What is true now

**Pre-registered, not built.** The design to prove — three optional files (`theme.css`, `logo.svg`, `labels.yaml`),
looked for in four places (the person's home, beside the trackers, the vendored tool's `brand/`, the tool's own
defaults), the nearest to the viewer winning — and eleven claims with what would kill each are in
[the R&D record](evidence/FM-002/brand-layers-rd.md), written before any code. What is left is the run: the spike
on `rd/fm-002-brand-layers`, measured on a scratch copy of the origin with its real logo, brand tokens and fonts.

## Why

The first client's staff read German. The origin has a brand. A consultancy setting a repository up for a client
wants its mark on it until the client's replaces it. And two people committing to one repository must never fight
over a generated file because their boards look different.

## Done when

Every pre-registered claim has an outcome under its forecast; the Owner has ruled on the merge; on merge, the
README explains the whole feature in one section of at most 25 lines.

## Ship log

| Date | Event |
|---|---|
| 2026-09-21 | Filed; the pre-registration committed before the spike. |
