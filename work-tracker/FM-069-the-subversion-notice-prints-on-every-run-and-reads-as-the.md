---
id: FM-069
status: Shipped
considered: FM-044, FM-068
tags: bug
next: build
triaged: 2026-10-27
tier: P2
hook: "the Subversion notice prints on every run and reads as the error in TortoiseSVN's refusal"
---

# FM-069 — the Subversion notice prints on every run and reads as the error in TortoiseSVN's refusal

## What is true now

**2026-11-03 — Shipped with v0.20.2.** The Subversion notice prints once, at the end of `--init` and `--check`, after
the violations, and never in TortoiseSVN's output (`246aa26`). It was built in FM-068's critical round, which is READY,
and is merged into `release/v0.20.2-rebuilt` with it, as `43ac2f1` (#246). On the Owner's word of 30 October, its new
words are approved.

**Built 2026-10-27.** The Subversion notice is emitted once at the end of a selected `--init` or `--check`, after any violations, and is absent from all TortoiseSVN results and other modes. The old unconditional output and vendor-specific stderr capture are removed. Real local Subversion controls cover success, binding refusal and gate refusal; mutants omit either selected mode, duplicate the notice, move it before violations or leak it into hooks. Proposed words for the Owner: “Subversion: this local run cannot verify commit signatures or server-authenticated author identities.” Critical review and the wording ruling remain next.

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

- [x] The notice prints once per `--init` and `--check`, after the violations, and never in `--tsvn-hook` output.
  · `246aa26`
- [x] Its new words go to the Owner, as the Board's words do (FM-053).
  · `246aa26`, approved on the Owner's word of 30 October
- [x] A test pins where it prints and where it does not. · `246aa26`

## Ship log

| Date | Event |
|---|---|
| 2026-10-27 | Filed and judged In Progress, P2, for v0.20.2, from a field report from a Windows working copy. |
| 2026-10-27 | Built notice placement and its real-entry controls and mutants, from a field report from a Windows working copy. |
| 2026-11-03 | **Shipped with v0.20.2:** merged into `release/v0.20.2-rebuilt` with FM-068, as `43ac2f1` (#246); its words approved on the Owner's word of 30 October. Each item is met by `246aa26`. Records only. |
