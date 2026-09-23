# Review — 0.17.8, a vendor refuses what it cannot vouch for (FM-011)

- **Date:** 2026-09-23, 20:41 CEST (`date`)
- **Seat:** Reviewer (`reviewer@seat`) · **Session:** `8e509911/reviewer-1` (row still open) · **Model:** Claude Opus 5.5
- **Tip reviewed:** `0645690` on `fix/0.17.8-a-vendor-refuses-what-it-cannot-vouch-for`
- **Base:** `de1351c` (`origin/main`, v0.17.7)
- **Commits:** `1c10ec2` (FM-011, the build) and `0645690` (`VERSION`, `CHANGELOG.md`), both
  `Session: 8e509911/implementer-3`.

## Cold start

1. **What virtue do I bring?** Doubt. The rule is *a consumer runs a release, never a working copy*. It has to refuse
   what it should, accept a real release, and not break what already works — the suite's own vendoring included.
2. **How does it turn into blindness?** By calling the suite's `allow_untagged` edits a weakening without measuring
   what the old checks still prove, or by treating a parser that does not crash as a parser that warns.
3. **What would show that failure here?** The suite with the five edits undone, run on the 0.17.7 tool. Hand-edited
   PIN headers under the consumer's `--check`. A real tagged scratch clone vendored into a real scratch consumer and
   scanned by the consumer's detector.
4. **Who gets the record, independently of me?** The Principal seat, then the Owner. This file disposes of nothing.

## The departure — the suite's five edits

The five edits:
- five `vendor` calls in `test_shoalmark.py` gain `allow_untagged=True` / `--allow-untagged`: the licence check, the
  FM-009 pair, C7 (the brand) and the SVN hook check;
- one PIN rewrite skips `#` lines.

**They are the minimum, and they weaken nothing.**
- In a scratch copy I undid all five and ran the tip's suite on the **0.17.7 tool**: 260 ok, and exactly the **three
  new FM-011 checks fail**. Every older check passes unchanged.
- So the edits exist only because 0.17.8 refuses a working copy, and the old checks prove what they proved: the
  licence travels, the version lands, *(was 0.2.0)*, the brand is pinned, the SVN hook.
- The *edited in place* check still calls `vendor(dest)` without the flag, and still proves its refusal: that check
  runs before the provenance check.
- The default refusing path is covered by the three new checks, which vendor from a real tagged git source in a temp
  directory.

**What breaks, and for whom.**

| suite | tool | outcome |
|---|---|---|
| the unmodified 0.17.7 suite | 0.17.8 | stops with a **FileNotFoundError** after 38 checks: `vendor()` now refuses the untagged source, writes no PIN, and line 312 reads it |
| the tip's suite | 0.17.7 | stops with the **TypeError** (*unexpected keyword argument 'allow_untagged'*), also after 38 checks |

Neither reaches a consumer:
- `TOOL_FILES` carries no test file, so no vendored copy has the suite.
- The consumer's own test of its wrapper calls it with `--version` and `--check` only. Both read
  a manifest PIN, since `pin_problems` skips `#` lines.
- In the two client repositories, 0 files outside `tools/shoalmark` reference the suite or `vendor()` (a count only;
  nothing read).

## Attacks

### (1) The manifest parser on hand-edited headers

Consumer `--check`, from a copy vendored at a scratch tag. Every case exits 0 and **none crashes**.

| the PIN's first line | `--check` prints |
|---|---|
| as written | *pinned 0.17.8 from tag v0.17.8 (commit 0645690992), vendored 2026-09-23, complete* |
| extra spaces | the same — right |
| a `#` line before it | the same — right |
| the manifest after the hash lines | the same — right |
| `commit` field missing | *… from tag v0.17.8 (commit ), …* — no warning |
| `tag` field missing | *from untagged ,* plus the working-copy warning |
| `·` replaced by `-` | *pinned complete from untagged , vendored ?, complete* plus the warning |
| `# shoalmark ` and nothing | *pinned shoalmark from untagged , vendored ?* plus the warning |
| fields with no values | *pinned 0.17.8 from tag True (commit True), vendored True* — no warning |
| `# shoalmark` bare, or `#shoalmark …` | nothing, silently |
| manifest claims 0.17.9 over `VERSION` 0.17.8 | *pinned 0.17.9 from tag v0.17.9* — no warning |

See R1.

### (2) The source rules, in a scratch clone of this repository with a local tag `v0.17.8` (never the Owner's checkout)

| the source | outcome |
|---|---|
| detached HEAD at the tag, clean | **accepted** |
| at the tag, `README.md` changed | refused, exit 4, *the tree has changes: README.md*; nothing written |
| at the tag, an untracked `vendor/stray.js` | refused, exit 4, *the tree has changes: vendor/stray.js* |
| `stray.js` committed, tag moved onto it | vendored, and the copy's `vendor/` holds only `marked-18.0.13.umd.js` |
| tag `v0.17.8` on a commit whose `VERSION` says 0.17.9 | refused, exit 4, *HEAD 5645d8a831 is not at the tag v0.17.9 (it carries v0.17.8)* |

(5) `vendor/*` is not globbed, and that is fine. `TOOL_FILES` is the contract. An untracked stray makes the tree
dirty and is refused; a committed stray is part of the release but not of the tool.

### (3) The consumer's real copy (read-only)

- It is pinned at 0.17.7 and its PIN has no manifest line.
- 0.17.8's `pin_manifest()` gives `{}`, `pin_report()` gives `[]`, and `pin_problems()` gives `[]`.
- So `--check` says **nothing** about provenance, as the CHANGELOG says (*read as before*). That is acceptable for the
  pin that follows, which writes the line.
- A copy that is never re-pinned runs its own older tool, which does not read manifests anyway.

### (4) A release tarball (`git archive v0.17.8`, extracted outside any git repository)

| run | outcome |
|---|---|
| no flag | refused, exit 4, *… is not a git checkout — a release is vendored from a clone at its tag*; nothing written |
| `--allow-untagged` | vendors; PIN `# shoalmark 0.17.8 · untagged (no git) · vendored 2026-09-23 · complete` |
| `NOTICE` removed, `--allow-untagged` only | refused, *missing NOTICE* |
| `NOTICE` removed, with `--partial` | vendors 7 files; PIN `… · partial` plus `# missing: NOTICE` |

All as ruled.

### (6) The scratch release

- **The run:** a scratch clone at a local `v0.17.8`, vendored into a scratch consumer pinned at 0.17.7.
  - It exits 0 with *vendored shoalmark 0.17.8 from tag v0.17.8 … (was 0.17.7)* and prints **only `## 0.17.8`**.
  - The PIN's first line is `# shoalmark 0.17.8 · tag v0.17.8 · commit 06456909925332c952a99a491adacce8b251b10d ·
    vendored 2026-09-23 · complete`.
  - `shasum -c`: `OK` × 8.
- **The stage:** the pin stages `CHANGELOG.md`, `PIN`, `README.md`, `VERSION` and `shoalmark.py`, not `marked`. The
  consumer's detector on that stage (read-only): exit 0, 5 files, 0 findings.
  - `README.md` is staged this time and passes, although it still carries the `key=Session` example (0.17.7's R1,
    open).
- **The consumer's `--check`:** exit 0, *pinned 0.17.8 from tag v0.17.8 (commit 0645690992), vendored 2026-09-23,
  complete*, with no warning.

## Findings

### R1 · P3 · The PIN's manifest is read without validation — a malformed or incoherent header prints as a fact

- **What:** `pin_manifest()` (`shoalmark.py:3246`) splits on ` · ` and takes whatever it finds, and `pin_report()`
  (`:3260`) prints it. The table in (1) has the cases:
  - a header whose separators changed reports the version as *complete*;
  - fields with no value print Python's `True`;
  - a missing commit prints *(commit )*;
  - a header claiming a version the copy's `VERSION` contradicts reads *pinned 0.17.9 from tag v0.17.9*.

  None of these warns. The only warning is the working-copy one, and it fires only when the tag field is gone. A bare
  `# shoalmark` line is silently no manifest.
- **Cost:** A consumer's `--check` can state a provenance the copy does not have. The line is advisory; nothing else
  reads it, and it never crashes.
- **Confidence:** High (twelve cases).
- **What closes it:** Accept only the form `vendor()` writes:
  - the version equals the copy's `VERSION`;
  - `tag v<version> · commit <40 hex>`, or `untagged <sha | (no git)>[ (dirty)]`;
  - `vendored <ISO date>`;
  - `complete|partial`.

  Otherwise warn *the PIN's first line is not one --vendor writes — vendor again*. Optionally, one line for a PIN with
  no manifest: *vendored before 0.17.8 — where it came from is not recorded*.

## What survives the pass

- **The three refusals are exactly as ruled:** an incomplete source, a source that is no release, and a copy edited in
  place. Each is exit 4 with nothing written, and each message names the files or the HEAD.
  - `--partial` and `--allow-untagged` each say so in the PIN.
  - A detached checkout at the tag is accepted, so README §6's `git clone --branch vX.Y.Z` works.
- **The manifest is the first PIN line.** `pin_problems()` and the *edited in place* check skip `#` lines, and a PIN
  without one still verifies.
- **Documentation:** README §6, `--help` (`--vendor`, `--partial`, `--allow-untagged`), `CHANGELOG.md` `## 0.17.8`
  (first, dated today) and FM-011's *What is true now*, including the suite's edits, say what shipped.
- **Version:** `VERSION` = `__version__` = `0.17.8`.

## Gates on 0645690

| Gate | Result |
|---|---|
| `python3 test_shoalmark.py` (3.14.3) | exit=0 · 263 ok |
| `python3 test_core.py` (3.14.3) | exit=0 · 148 ok |
| `/usr/bin/python3 test_shoalmark.py` (3.9.6) | exit=0 · 263 ok |
| `/usr/bin/python3 test_core.py` (3.9.6) | exit=0 · 148 ok |
| Chrome | ran; no skip line |
| `python3 shoalmark.py --check` | exit=0 |
| `python3 shoalmark.py --html-only` | exit=0 |
| `python3 -m py_compile` (the three `.py` files) | exit=0 each |
| the tip's suite on the 0.17.7 tool | exit=1: the TypeError, and with the five call edits undone, exactly the three FM-011 checks fail (260 ok) |
| the scratch release into a scratch 0.17.7 consumer | exit=0 · only `## 0.17.8` · PIN `OK` × 8 · the consumer's detector on the stage exit=0, 0 findings |

- **Not run:** CI on Linux and Windows.

## Verdict

**READY WITH FINDINGS: R1 (P3).**

- The vendoring rules hold on every source I could build.
- The suite's edits are minimal and weaken nothing.
- No consumer runs the suite.
- R1 is a display that believes a hand-edited header.

## Delta on 984113b

2026-09-23, 21:00 CEST. **READY WITH FINDINGS: R2 (P3). R1 is closed.**

**R1 · closed.** `MANIFEST_RE` accepts only the line `--vendor` writes. `pin_manifest()` then cross-checks the date,
the tag against the version, the version against the pinned `VERSION`, and a partial copy's `# missing:` line. The
consumer's `--check` in a scratch copy vendored at a scratch `v0.17.8`, every case exit 0:

| the PIN's first line | `--check` says |
|---|---|
| the good header | *pinned 0.17.8 from tag v0.17.8 (commit 984113b971), vendored 2026-09-23, complete* |
| extra spaces | *warning: … is not the line --vendor writes — this copy is unverified* |
| commit missing | the same warning |
| `·` replaced by `-` | the same warning |
| fields with no values | the same warning |
| bare `# shoalmark` | the same warning |
| a commit hash of 6 characters | the same warning |
| the date `2026-9-3` | the same warning |
| the date `2026-13-45` | *… (its date is no date)* |
| a `#` line before it | *… is not the PIN's first line* |
| 0.17.9 over `VERSION` 0.17.8 | *… says 0.17.9, and the pinned VERSION is 0.17.8* |
| tag v0.17.7 for 0.17.8 | *… names the tag v0.17.7 for the version 0.17.8* |
| partial with no `# missing:` line | *… says partial and names nothing missing* |
| a PIN with no header | *no manifest — pinned before 0.17.8; where the copy came from is not recorded* |
| the consumer's real 0.17.7 copy (read-only) | the same *no manifest* line; `pin_problems()` is empty |

**R2 · P3 · A manifest moved below the hash lines reads as *no manifest — pinned before 0.17.8*.**
- **What:** `pin_manifest()` returns `({}, "")` whenever the first line does not start with `#`
  (`shoalmark.py:3257`), so a 0.17.8 manifest placed after the hashes is reported as a PIN from before 0.17.8, not
  flagged.
- **What closes it:** Ask the same question the `#`-first branch asks: when a later line is a manifest, warn *is not
  the PIN's first line*.
- **Cost:** A misstatement only, reached only by hand-editing a PIN.

**The scratch release:**
- A scratch clone of `984113b` with the local tag `v0.17.8`, vendored into a scratch 0.17.7 consumer: exit 0, only
  `## 0.17.8`, PIN `OK` × 8.
- The pin stages `CHANGELOG.md`, `PIN`, `README.md`, `VERSION` and `shoalmark.py`. The consumer's detector on that
  stage: exit 0, 0 findings.
- The consumer's `--check`: the good line, and no warning.

**Gates:**

| Gate | Result |
|---|---|
| `test_shoalmark.py` | exit 0 on Python 3.14.3 and 3.9.6 · 264 ok |
| `test_core.py` | exit 0 on both · 148 ok |
| `--check` · `--html-only` | exit 0 each |
| `py_compile` (the three files) | exit 0 each |
| `VERSION` | 0.17.8 |
| the tip's suite on the 0.17.7 tool, the five edits undone | 260 ok; exactly the four FM-011 checks fail, R1's new check included |
