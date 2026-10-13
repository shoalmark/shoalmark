---
id: FM-046
status: Shipped
considered: FM-033, FM-037
tags: bug
triaged: 2026-10-12
tier: P1
hook: "A committed tracker's front matter is parsed only for LF line endings and not through one normalisation, so the same tracker can read two ways across line-endings and version-control layers"
---

# FM-046 — A committed tracker's front matter is parsed only for LF line endings and not through one normalisation, so the same tracker can read two ways across line-endings and version-control layers

## What is true now

**Shipped in v0.19.4, 2026-10-13:** built at `e948764` on `fm/046-text-boundary`, merged to main as
`39e5763` (#165), tagged `v0.19.4` on `39e5763`. Advisory `GHSA-xh54-c5jg-j4fp` is public.
Reviewed READY in critical round 2 at `51f333f`.
Parsed committed tracker text returns LF from `cat_blobs` for Git and `svn_run` for Subversion, with the rights check's
one-off normalisation removed. Physical Git lines, protected text and trusted signers explicitly request the Git
reader's `raw=True` mode. Binary reads, hashes and the batch's byte offsets are unchanged.

`test_tracker_text.py` writes and verifies actual committed LF and CRLF bytes in disposable Git and Subversion
repositories. Its 55 controls pass, with no skips: status/Shipped, answer/ask/triage/close, actual rights verdicts,
the guard's section reader, rendered index, answer gate, judgement, answer branches, staged trackers, and synthetic
SSH signatures with LF, CRLF and CR configuration/signers. They also exercise signed history through the gate,
each converted committed-text reader with LF, CRLF and missing snapshots, and local filtered clones.

Compile, all 158 core checks, 16 Owner-exemption tests, and 364 selected existing browser-free checks pass, with no FAIL or skip lines;
the full suite is left to CI under BRIEF-2.md when the Owner opens the pull request.

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
| 2026-10-13 | Built the shared committed-text boundaries and 28 explicit-byte controls; compile and 158 core checks pass. Review next. |
| 2026-10-13 | Local full-suite runs stopped after Chrome prompted the Owner for keychain access; BRIEF-2 replaces them with browser-free selected checks, with the full suite left to CI. |
| 2026-10-13 | Built explicit raw Git reads and persistent signed-history, converted-reader and filtered-clone controls. All 55 controls, 158 core checks, 16 Owner-exemption tests and 364 selected browser-free checks pass; compile passes. Review next. |
| 2026-10-13 | **Shipped in v0.19.4:** build `e948764` on `fm/046-text-boundary`, reviewed READY in round 2 (`51f333f`), merged to main as `39e5763` (#165); tagged `v0.19.4` on `39e5763`. Advisory `GHSA-xh54-c5jg-j4fp` is public. |
