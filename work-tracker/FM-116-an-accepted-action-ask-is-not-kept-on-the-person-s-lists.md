---
id: FM-116
status: Proposed
considered: FM-030, FM-014, FM-029, FM-084
tags: bug
hook: "An action ask the person accepts asks for an act only their hands can do. It should stay on their lists, marked promised, until the act is done. FM-030's twelve items for it are unmet, and are restated here against what the default branch holds."
---

# FM-116 — an accepted action ask is not kept on the person's lists, marked promised, until its act is done

## What is true now

**2026-11-03 — filed; nothing is built.** It leaves FM-030 at its split, as the Owner's sweep words it.
- **What it takes:** FM-030's twelve *Done when* items, about promised acts. None is met.
- **They are restated against what the default branch holds,** not against FM-030's text of September:
  - the done dialog, merged as #103;
  - the acts board, merged as #113 (`fa9e9ac`);
  - and, at the release head, S1's change that the Board, `--owner` and `--standup` read no answer branch
    (`9f81c3e`).
- **Already shipped under FM-030:** part A, the stand-up prompt's built-in text. Its part B is
  [FM-100](FM-100-the-stand-up-prompt-is-code-and-english-on-every-board-while.md).

## Why

An act only the person's hands can do is the work most easily forgotten. A list that drops it when the answer is given
loses it exactly then.

## Done when

- [ ] FM-030's twelve items are restated against what the default branch holds, each as one checkable line.
- [ ] Each restated item is built, with its test.

## Ship log

| Date | Event |
|---|---|
| 2026-11-03 | Filed from FM-030's split. Records only. |
