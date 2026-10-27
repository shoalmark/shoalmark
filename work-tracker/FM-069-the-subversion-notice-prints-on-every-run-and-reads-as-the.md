---
id: FM-069
status: In Progress
considered: FM-044, FM-068
tags: bug
next: build
triaged: 2026-10-27
tier: P2
hook: "the Subversion notice prints on every run and reads as the error in TortoiseSVN's refusal"
---

# FM-069 — the Subversion notice prints on every run and reads as the error in TortoiseSVN's refusal

## What is true now

**Filed and judged 2026-10-27: In Progress, P2, for v0.20.2, in FM-068's critical round, on the Owner's word as
relayed by the Auditor.** It comes from a field report from a Windows working copy, on v0.20.1.

The Subversion notice, which says what a local run cannot verify, prints on every run. In TortoiseSVN it is the first
line of the refusal dialog, so it reads as the error. 0.20.0's CHANGELOG says the tool says it once.

On Windows PowerShell 5.1, a native command's stderr under `2>&1` becomes an error record, so an agent's run looks failed
at exit 0. And its words, "protected SVN acceptance remains held", are the tool's internal language.

## Why

A notice that stands where the reason for a refusal should stand hides the reason. A notice on every run is noise that
an agent reads as a failure.

## Done when

- The notice prints once per `--init` and `--check`, after the violations, and never in `--tsvn-hook` output.
- Its new words go to the Owner, as the Board's words do (FM-053).
- A test pins where it prints and where it does not.

## Ship log

| Date | Event |
|---|---|
| 2026-10-27 | Filed and judged In Progress, P2, for v0.20.2, from a field report from a Windows working copy. |
