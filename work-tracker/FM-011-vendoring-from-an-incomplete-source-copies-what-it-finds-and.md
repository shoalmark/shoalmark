---
id: FM-011
status: In Progress
considered: FM-009
tags: bug
next: review
kind-of-problem: obvious
triaged: 2026-09-23
rank: 1
tier: P1
hook: "`vendor()` skips a source file that is not there — `if not src.exists(): continue` — so vendoring from an incomplete source copies what it finds, pins only that, and reports success. From a lone `shoalmark.py` it writes one file and a one-entry PIN, leaves the consumer's old `VERSION` on disk, and the integrity check then covers a single file while appearing to cover the copy."
---

# FM-011 — Vendoring from an incomplete source copies what it finds and pins only that, instead of refusing

## What is true now

**Built 2026-09-23 on `fix/0.17.8-a-vendor-refuses-what-it-cannot-vouch-for`, for 0.17.8; open for review, not
merged.** On the Owner's *"proceed"*, the first triage pass's #1. `vendor()` now checks before it writes anything:

| the source | at 0.17.7 | now |
|---|---|---|
| a file of `TOOL_FILES` missing | copied the rest, a short PIN, success | refused, exit 4, the missing files named, nothing written; `--partial` copies it and the PIN names what is missing |
| not a git checkout at `v<VERSION>`, or a changed tree | vendored | refused, exit 4, naming the HEAD and the changed paths; `--allow-untagged` vendors and the PIN says `untagged <sha>` |
| a clean clone at its release tag | vendored | vendored; the PIN's first line: `# shoalmark <version> · tag <vX.Y.Z> · commit <sha> · vendored <date> · complete` |

The consumer's `--check` reads that line and prints *pinned <version> from tag …*, with a warning for an untagged or
partial copy. The brand files stay optional. The required set is `TOOL_FILES` — the tool, the renderer, `VERSION`,
`NOTICE`, both licences, `README.md`, `CHANGELOG.md`. **Settled here:** `__version__` keeps `"unknown"` when
`VERSION` is absent. Importing must not raise, and `--vendor` can no longer produce a copy without `VERSION` unless
`--partial` was asked for and the PIN says so.

**What changed in the existing suite, and why:** the suite vendors from its own working copy, which is by definition no
release. Its five vendor calls now say `allow_untagged=True` / `--allow-untagged`, and the one check that rewrites a
PIN line by line skips the manifest line. No assertion changed.

Raised in review of FM-009 (PR #10) and reproduced here.

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
| 2026-09-23 | R1: `--check` accepts only the manifest line `--vendor` writes, cross-checks tag, version and the pinned `VERSION`, and otherwise warns naming what is wrong and calls the copy *unverified*; no manifest reads *pinned before 0.17.8*. One check, the Reviewer's five hand-edited headers and the good one. |
| 2026-09-23 | Built for 0.17.8: an incomplete source and one that is no release are refused before anything is written; `--partial`, `--allow-untagged`; the PIN's manifest line; the consumer's `--check` reads it. Three checks, each failing on 0.17.7. |
| 2026-09-22 | Filed. Raised by the reviewer of PR #10; reproduced from a lone-file source, and the reporting half traced to FM-009's version derivation rather than to the pre-existing skip. |
