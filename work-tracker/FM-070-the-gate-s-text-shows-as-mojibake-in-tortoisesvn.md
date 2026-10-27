---
id: FM-070
status: In Progress
considered: FM-068, FM-069
tags: bug
next: build
triaged: 2026-10-27
tier: P3
hook: "the gate's text shows as mojibake in TortoiseSVN"
---

# FM-070 — the gate's text shows as mojibake in TortoiseSVN

## What is true now

**Filed and judged 2026-10-27: In Progress, P3, for v0.20.2, in FM-068's critical round, on the Owner's word as
relayed by the Auditor.** It comes from a field report from a Windows working copy, on v0.20.1.

In `--tsvn-hook` mode, the gate's text shows as mojibake in TortoiseSVN's dialog: an em dash becomes three other
characters. The hook writes UTF-8, and TortoiseSVN reads the ANSI code page.

## Why

A refusal a person cannot read is a refusal they cannot act on.

## Done when

- In `--tsvn-hook` mode the hook writes the ANSI code page with errors replaced, or ASCII alone.
- A test pins the bytes the hook writes for a line with an em dash.

## Ship log

| Date | Event |
|---|---|
| 2026-10-27 | Filed and judged In Progress, P3, for v0.20.2, from a field report from a Windows working copy. |
