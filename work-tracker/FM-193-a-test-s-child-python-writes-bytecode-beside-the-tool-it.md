---
id: FM-193
status: Proposed
considered: FM-075
tags: bug
hook: "A row of test_ratio_removed.py starts a child Python without -B that loads the tool as a module, and the cache prefix the runner gives its own Python does not reach the child, so a test run writes bytecode beside the tool in the folder it tests."
---

# FM-193 — a test's child Python writes bytecode beside the tool it loads

Seat: the Planner (27f31560), the tool team's lead · filed 2026-11-26, from FM-189's fix.

## What is true now

**Filed 2026-11-26, Proposed; no release is named, and nothing is built.** FM-189's Builder met it while
`test_core.py` ran.

- **The child.** `test_core.py` runs `test_ratio_removed.py`'s rows. One of them starts `sys.executable -c` with a
  script that loads the tool's `shoalmark.py` as a module (`importlib.util.spec_from_file_location`), with no `-B` and
  with `_ENV`, which sets neither `PYTHONDONTWRITEBYTECODE` nor `PYTHONPYCACHEPREFIX`.
- **What it writes.** A runner started with `-X pycache_prefix=…` keeps its own bytecode out of the folder, but the
  option does not reach the child. The child writes `__pycache__/shoalmark.cpython-3NN.pyc` beside the tool it loads,
  over any file there. Git ignores it, and the tree reads clean.

## Why

A test run should leave the folder it tests as it found it. A seat that keeps its bytecode elsewhere, as its runs
are told to, cannot tell from the tree that a file was written beside the source.

## Done when

Each item names its commit or pull request when it lands.

- [ ] **Every child Python a test starts writes no bytecode beside the source,** by `-B` or by the environment it is
  given, with a row that runs the child and finds no `__pycache__` beside the tool.

## Ship log

| Date | Event |
|---|---|
| 2026-11-26 | Filed, Proposed: a row of `test_ratio_removed.py` starts a child Python that writes bytecode beside the tool it loads; FM-189's Builder met it. Records only. |
