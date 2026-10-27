---
id: FM-075
status: Proposed
considered: FM-044
tags: bug
hook: "seven source-binding controls fail on Apple's Python 3.9.6, whose bytecode cache is redirected"
---

# FM-075 — seven source-binding controls fail on Apple's Python 3.9.6, whose bytecode cache is redirected

## What is true now

**Filed 2026-10-27, Proposed, from RV-3903 of FM-068's critical review.** It comes after v0.20.2; nothing is built.

On Apple's `/usr/bin/python3` 3.9.6, seven source-binding controls of `test_tsvn_source_binding.py` fail, at `f08ef2b` and
at `b65b817` alike, and at v0.20.1. That Python sets `sys.pycache_prefix` to a folder under the home folder's
`Library/Caches`, so a refusal that imports a module reads its bytecode from outside the one library folder the check
allows. Python 3.15 on the same Mac, and CI's 3.9, set no prefix, and pass.

## Why

A control that fails on one common Python for a reason outside the tool hides a real failure behind a known one.

## Done when

- The check allows the bytecode cache folder that `sys.pycache_prefix` names, and nothing wider, or says it cannot judge there.
- The seven controls pass on Apple's 3.9.6.

## Ship log

| Date | Event |
|---|---|
| 2026-10-27 | Filed, Proposed, from RV-3903 of FM-068's critical review; after v0.20.2. |
