---
id: FM-009
status: Shipped
considered: FM-006
tags: bug
kind-of-problem: obvious
hook: "`__version__` in `shoalmark.py` says 0.17.0; `VERSION` and the CHANGELOG say 0.17.2. Two tags shipped that way. `--vendor` compares the consumer's `VERSION` file against our source constant, so a consumer sitting on exactly 0.17.0 is told nothing changed and never sees the 0.17.1 and 0.17.2 sections — the repositories that most need those two fixes are the ones the comparison silences."
---

# FM-009 — `__version__` has drifted from `VERSION`, and `--vendor` suppresses the changelog because of it

## What is true now

**Built 2026-09-22 on `fix/0.17.3-version-drift-and-the-silent-deprecation`; merged 2026-09-22 (#10), released as 0.17.3.**
Reported by an outside consumer upgrading from 0.11.0, and verified here. `__version__` is now read from the
`VERSION` file at import and declared nowhere else, so the two cannot drift; `--vendor`'s comparison is between
the consumer's `VERSION` and ours. A consumer pinned at 0.17.0 re-vendoring now gets `(was 0.17.0)` and the
0.17.1, 0.17.2 and 0.17.3 sections — reproduced end to end. Two checks pin it, both shown to fail when the
declared constant is put back. **What is left:** nothing; the section below records
the state that made it necessary.

**Two sources of truth, and they disagree.** `shoalmark.py:42` carries `__version__ = "0.17.0"`; `VERSION` and the
CHANGELOG's top section say `0.17.2`. Every release through 0.16.0 moved the two together — `git log -L42,42:shoalmark.py`
is an unbroken chain of paired bumps — and then 0.17.1 and 0.17.2 bumped `VERSION` and the CHANGELOG and left the
constant behind. The drift is in the tags, not just the working tree:

| tag | `VERSION` | `__version__` |
|---|---|---|
| v0.17.0 | 0.17.0 | 0.17.0 |
| v0.17.1 | 0.17.1 | **0.17.0** |
| v0.17.2 | 0.17.2 | **0.17.0** |

`python3 shoalmark.py --version` on a tree at v0.17.2 prints `0.17.0`. That half is cosmetic.

**The half that is not: `--vendor` stops telling a consumer what it is taking on.** `vendor()` reads `had` from the
*destination's* `VERSION` file (`shoalmark.py:2549`) and compares it against our *source constant*
(`shoalmark.py:2565-2566`). The guard is `if had and had != __version__ and changes_since(had)`. A consumer sitting on
exactly 0.17.0 has `had == __version__`, the guard is false, and the whole point of the line — *the CHANGELOG sections
newer than `version`; what a consumer takes on by vendoring again* — never runs. Reproduced against a copy pinned at
0.17.0:

```
vendored shoalmark 0.17.0 into …/consumer — 8 files, pinned in PIN
$ cat consumer/VERSION
0.17.2
```

Three failures in one line: the version reported is wrong, the `(was …)` clause is missing, and the changelog is
silent. The consumer receives 0.17.2's files and is told they are 0.17.0's.

**Who it hits is the sharp part.** The suppression triggers on `had == 0.17.0` exactly. A repository further behind —
the reporter came from 0.11.0 — has `had != __version__` by accident and gets the full changelog. Being far behind
insulates you from the bug; being one release behind is what hides it. The two sections withheld are 0.17.1 (a
repository on `[seats]` could not answer at all) and 0.17.2 (answers misattributed to the prose commit) — the two
nobody should upgrade past unread.

**Nothing guards the pair.** `grep __version__ test_shoalmark.py test_core.py` returns nothing: no test asserts that
`VERSION` and `__version__` agree, which is how two releases walked past it.

## Why

Consumers vendor from a tag, and `--vendor`'s changelog line is the only place the tool tells them what a re-vendor
changes. While that line is guarded by a comparison between a file and a constant, it is correct only while the two
happen to agree — and they no longer do. Fixing the constant alone restores the output but leaves the comparison
resting on the same coincidence.

The cost of leaving it: every repository that vendored v0.17.0 and re-vendors before this ships upgrades blind past two
correctness fixes in the answer gate.

## Done when

- `__version__` is **derived from `VERSION`**, not declared beside it — one source of truth, so the two cannot drift
  again. `VERSION` already ships in `TOOL_FILES` (`shoalmark.py:2518`), so the vendored copy carries what it needs.
- `--vendor`'s comparison is then between the consumer's `VERSION` and ours — the artifact actually being copied —
  and is correct by construction rather than by coincidence.
- A consumer pinned at 0.17.0 re-vendoring gets the `(was 0.17.0)` clause and the 0.17.1, 0.17.2 and 0.17.3 sections.
- A test asserts `VERSION` and `__version__` agree — a regression net, not the mechanism.
- `--version` prints the tag's version.
- Ships as **0.17.3**. v0.17.2 is already tagged carrying the wrong constant and consumers vendor from tags, so the
  only way out is forward; 0.17.2 is not re-cut.

## Ship log

| Date | Event |
|---|---|
| 2026-09-22 | Merged (#10), released as 0.17.3. |
| 2026-09-22 | Built: version derived from `VERSION`, two checks, CHANGELOG 0.17.3, `VERSION` bumped. Both suites green (200 checks); the two new checks fail against the restored defect. Open for review. |
| 2026-09-22 | Filed. Reported by an outside consumer; drift confirmed present in tags v0.17.1 and v0.17.2, and the `--vendor` suppression reproduced against a copy pinned at 0.17.0. |
