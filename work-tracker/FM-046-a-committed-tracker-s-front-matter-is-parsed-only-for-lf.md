---
id: FM-046
status: In Progress
considered: FM-033, FM-037
tags: bug
triaged: 2026-10-12
next: build
tier: P1
hook: "A committed tracker's front matter is parsed only for LF line endings and not through one normalisation, so the same tracker can read two ways across line-endings and version-control layers"
---

# FM-046 — A committed tracker's front matter is parsed only for LF line endings and not through one normalisation, so the same tracker can read two ways across line-endings and version-control layers

## What is true now

2026-10-12 — In Progress at the Owner's request; no implementation is built under this tracker yet. Next: build the
shared normalisation of committed text for Git and Subversion, remove the earlier one-off, and verify the rules
listed in Done when.

A tracker's front matter is parsed only when its `---` fences end in `\n`. A tracker committed with CRLF (`\r\n`) line
endings — as a hand edit or an agent edit on a system whose editor or Git writes CRLF can produce — has `---\r\n`
fences, which the parser does not recognise, so the tool reads the tracker as having no front matter. The tool's own
writes are always LF, so it never produces such a tracker itself; the case arises only from an outside CRLF edit.

The reads of committed tracker text are not all routed through one normalisation: one path normalises CRLF before
parsing, others read the committed bytes raw. So the same tracker can be read two ways depending on which rule reads
it. A committed tracker must read identically regardless of its line endings and of the version-control layer (Git or
Subversion).

## Done when

- Line endings are normalised to LF at the single shared boundary where the tool reads tracker text from version
  control, for Git and for Subversion, so every rule downstream parses the same text (DRY: one place, the earlier
  one-off normalisation removed).
- Configuration and signers reads, which share that boundary, keep working; binary reads, which do not, are untouched.
- A test covers each rule that reads committed tracker text, under both line endings, for both version-control layers.

## Ship log

| Date | Event |
|---|---|
| 2026-10-12 | Filed. |
