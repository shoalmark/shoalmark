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

**Built 2026-10-27.** Windows TortoiseSVN runs configure stdout and stderr with the Windows ANSI code page through Python's built-in `mbcs` codec (`CP_ACP`), replacing characters it cannot encode. Both entry-time configuration diagnostics and `main` use this choice. Other modes retain UTF-8 and LF, including `--print-written`. Byte controls simulate Windows with code pages 1252, 932 and 65001, and reject a UTF-8 hook mutant. The watchdog's direct stderr bytes use that configured encoding too, with a byte control and UTF-8 mutant. Hook fixture readers decode the captured output with `mbcs` on Windows and UTF-8 elsewhere. This is simulated evidence; TortoiseSVN dialog display still needs a Windows run. Critical review remains next.

Check limit found on the way: Python 3.9 source-binding controls report seven confinement failures on standard-library bytecode-cache reads outside the runtime directory. The second diagnostic attempt identifies the same cache reads; that predicate is left for a separate change.

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
| 2026-10-27 | Built ANSI hook output and byte controls, from a field report from a Windows working copy. |
