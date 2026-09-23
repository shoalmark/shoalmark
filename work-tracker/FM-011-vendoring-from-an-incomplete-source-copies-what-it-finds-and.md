---
id: FM-011
status: Proposed
considered: FM-009
tags: bug
next: build
kind-of-problem: obvious
triaged: 2026-09-23
rank: 1
tier: P1
hook: "`vendor()` skips a source file that is not there — `if not src.exists(): continue` — so vendoring from an incomplete source copies what it finds, pins only that, and reports success. From a lone `shoalmark.py` it writes one file and a one-entry PIN, leaves the consumer's old `VERSION` on disk, and the integrity check then covers a single file while appearing to cover the copy."
---

# FM-011 — Vendoring from an incomplete source copies what it finds and pins only that, instead of refusing

## What is true now

**Filed 2026-09-22; nothing is built.** Raised in review of FM-009 (PR #10) and reproduced here.

**`--vendor` treats a missing source file as nothing to do.** `shoalmark.py:2557-2564` walks `TOOL_FILES` plus the
brand files and skips whatever is absent:

```python
for rel in TOOL_FILES + tuple(f"brand/{n}" for n in BRAND_FILES):
    src = HERE / rel
    if not src.exists():
        continue
```

Nothing downstream notices. `PIN` is written from the files that *were* copied, so it is complete with respect to
itself and silent about the rest, and the run reports success. Vendoring from a directory holding only
`shoalmark.py`, into a copy pinned at `0.9.9`:

```
vendored shoalmark unknown into …/dest — 1 files, pinned in PIN (was 0.9.9)
--- dest now holds: PIN  shoalmark.py  VERSION
--- VERSION on disk: 0.9.9          (the consumer's old one, never replaced)
--- PIN entries: 1                  (shoalmark.py alone)
```

Three consequences, none of them announced:

1. **The copy is not the tool.** `NOTICE`, the licences, `CHANGELOG.md`, `README.md` and the pinned renderer are all
   absent, and the run says only `1 files`.
2. **`PIN` now attests to one file.** The next `--vendor` compares digests for the entries it finds
   (`shoalmark.py:2550-2555`), so the edit-in-place refusal — the guard that stops a consumer's local changes being
   overwritten — covers `shoalmark.py` and silently ignores everything else the copy carries.
3. **The copy reports the consumer's own stale version.** `VERSION` was not among the sources, so the old file
   survives, and the vendored `shoalmark.py` reads its version from the file beside it.

**Point 3 is partly FM-009's doing, and that is the honest accounting.** The skip is long-standing; what the version
derivation changed is what the incomplete copy then *says*:

| lone-file source | the vendored copy reports |
|---|---|
| before FM-009 | `0.17.0` — the source's own version, carried in the constant |
| after FM-009 | `0.9.9` — **the consumer's stale file, read back to them** |

Deriving the version from `VERSION` is right, and FM-009 holds: it is what makes `--vendor`'s comparison correct for
every complete source, which is every supported one. But it removes the constant that used to paper over an
incomplete source, and that turns a quiet gap into a wrong answer. The review that raised this read the skip as
wholly pre-existing; the reporting half is not.

**Reachability.** A tag or a clone is always complete, so no supported path hits this. It is reached by vendoring
from a copy of the script alone — which is how somebody who has only ever seen `shoalmark.py` would expect the tool
to work, given it is distributed as one file.

## Why

`--vendor` exists so a consumer can take the tool and later prove the copy is unmodified. Both halves fail quietly
here: what lands is not the tool, and what `PIN` attests to is a fraction of it while reading as the whole. A guard
that silently narrows its own scope is worse than no guard — the consumer's next `--vendor` will report nothing
wrong.

`"unknown"` as the version fallback was chosen in FM-009 to degrade safely rather than raise at import. That is the
right call for import; it is the wrong call for `--vendor`, which can check before it writes anything.

## Done when

- `--vendor` **refuses an incomplete source** and names what is missing, before it copies or writes `PIN` — the loud
  failure, not a short `PIN`. `TOOL_FILES` is the tool's definition of itself; a source missing any of it is not a
  source.
- The brand files keep their optional status if that is what they are — the refusal distinguishes what is required
  from what is not, rather than requiring everything present.
- A copy is never left half-written: the check runs before the first `shutil.copyfile`.
- A test vendors from a source with a file removed and holds the refusal, naming the file.
- Whether `__version__` should also refuse rather than read `"unknown"` when `VERSION` is absent is settled here,
  once `--vendor` can no longer produce that state.

## Ship log

| Date | Event |
|---|---|
| 2026-09-22 | Filed. Raised by the reviewer of PR #10; reproduced from a lone-file source, and the reporting half traced to FM-009's version derivation rather than to the pre-existing skip. |
