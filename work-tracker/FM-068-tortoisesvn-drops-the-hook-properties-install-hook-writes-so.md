---
id: FM-068
status: In Progress
considered: FM-003, FM-044
tags: bug
next: build
triaged: 2026-10-27
tier: P1
hook: "TortoiseSVN drops the hook properties --install-hook writes, so no TortoiseSVN commit is gated"
---

# FM-068 — TortoiseSVN drops the hook properties --install-hook writes, so no TortoiseSVN commit is gated

## What is true now

**Built 2026-10-27.** The installer writes type/quoted-command/true/hide values, upgrades its former three-line values and preserves other properties. A real scratch Subversion installer test applies the 1.14.9 parser's token and quoted-path rules; its three-line installer mutant fails the same contract. Both adoption guides record what a field report from a Windows working copy showed. Quoting is source-based and has not been tried on Windows.

For the 0.20.2 CHANGELOG: TortoiseSVN hook properties now include their type and quote the script path; run `--install-hook` again after upgrading.

**Filed and judged 2026-10-27: In Progress, P1, critical tier, for v0.20.2, on the Owner's word as relayed by the
Auditor.** It comes from a field report from a Windows working copy, on v0.20.1. With FM-069 and FM-070 it is one
critical round, after FM-024's.

TortoiseSVN 1.14 reads a hook property as four lines: the hook's type (`start_commit_hook`, `pre_commit_hook`), the
command, whether to wait, and whether to show or hide its window. A value with no fourth line is dropped, without a word.
`--install-hook` on Subversion writes three lines and no type line, so TortoiseSVN runs neither property, and no commit
made through it is gated.

The field report shows it. With the four-line value set by hand, TortoiseSVN asked for approval, and the start-commit
hook refused a tracker moved to Shipped with no revision.

## Why

FM-003 named what only a person on Windows could prove: that TortoiseSVN runs the two properties. Their format was taken
from TortoiseSVN's source as remembered, not from its manual. The field report is that proof, and the remembered format
was wrong. The gate a person relies on in TortoiseSVN has not run.

## Done when

- `--install-hook` writes each property with its type line first, and quotes the script's path, so a path with a space
  stays one argument.
- The format's basis is TortoiseSVN's own parser (`src/Utils/Hooks.cpp`, `CHooks::ParseAndInsertProjectProperty`). What
  is read from that source and not tried on Windows is said to be so.
- A test applies TortoiseSVN's rule to the value `--install-hook` writes, and fails on the three-line value.
- The upgrade note says to run `--install-hook` again.
- `ADOPT.svn.md`'s line that no person has yet seen it on Windows (and its German twin) says what the field report showed.

## Ship log

| Date | Event |
|---|---|
| 2026-10-27 | Filed and judged In Progress, P1, critical tier, for v0.20.2, from a field report from a Windows working copy. |
| 2026-10-27 | Built the hook-property correction and its parser-based installer control; critical review remains next. |
