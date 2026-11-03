---
id: FM-109
status: Proposed
epic: FM-107
considered: FM-006, FM-021, FM-043
tags: process
hook: "The release workflow creates each release's draft with empty notes. The CHANGELOG holds the release's section already, and nothing carries it into the release."
---

# FM-109 — a release's draft has empty notes, not its CHANGELOG section

## What is true now

**2026-11-03 — filed; nothing is built.** It is one of FM-006's checks after the v0.19.0 tag, kept on the Owner's word
of 2 November.
- `.github/workflows/release.yml` creates the draft with `gh release create "$TAG" --draft --verify-tag --title
  "$TAG" --notes ""`. No step reads `CHANGELOG.md`.
- The archive and its checksum are attached already.

## Why

A release page is where an adopter reads what changed. Empty notes send them elsewhere for what the CHANGELOG already
says.

## Done when

- [ ] A release's draft carries the CHANGELOG's section for its version as its notes.

## Ship log

| Date | Event |
|---|---|
| 2026-11-03 | Filed as a child of FM-107, on the Owner's word of 2 November. Records only. |
