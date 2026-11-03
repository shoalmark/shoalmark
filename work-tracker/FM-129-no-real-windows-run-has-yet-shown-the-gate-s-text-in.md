---
id: FM-129
status: Proposed
considered: FM-070, FM-068, FM-003
tags: bug
hook: "The gate's text in TortoiseSVN's dialog is proven on simulated code pages only. The first real run of the dialog on Windows, with a line that holds an em dash, recorded with what the dialog showed."
---

# FM-129 — no real Windows run has yet shown the gate's text in TortoiseSVN's dialog

## What is true now

**2026-11-03 — filed; nothing is built.** It leaves FM-070 at its split, as the Owner's sweep words it.
- **What it takes:** the first real run of TortoiseSVN's dialog on Windows, with a line that holds an em dash,
  recorded with what the dialog showed.
- **Already shipped under FM-070:** the hook's output in the ANSI code page, with byte controls for 1252, 932 and 65001.

## Why

A byte test proves what the hook writes, not what a person sees in the dialog.

## Done when

- [ ] A real TortoiseSVN dialog on Windows shows a gate line that holds an em dash, and the record says what it
  showed.

## Ship log

| Date | Event |
|---|---|
| 2026-11-03 | Filed from FM-070's split. Records only. |
