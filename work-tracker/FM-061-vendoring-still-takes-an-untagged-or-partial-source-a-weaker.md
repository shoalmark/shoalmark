---
id: FM-061
status: In Progress
considered: FM-011, FM-009, FM-004, FM-023
tags: security
next: build
triaged: 2026-10-16
tier: P2
hook: "vendoring still takes an untagged or partial source, a weaker trusted pin than R17 allows"
---

# FM-061 — vendoring still takes an untagged or partial source, a weaker trusted pin than R17 allows

## What is true now

**Rebuilt for public history 2026-10-21 on `fm/061-r17-public`, from `1148114`:** the reviewed tree is made again on this branch in commits 1 and 2, `91ede4a` and `968e82a`, but for three lines of this record, which now name their findings only as recorded privately. The review rounds' own commits stay on a private record, and the commits FM-061 names below are on that record.

**Built 2026-10-16 on `fm/061-r17`, `0856fc6` (D3); fixed 2026-10-17 at `29097fb` (RV-3364: recorded privately) and `0d5ccee`; round 2, 2026-10-17, on `fm/061-r17-round2` at `7a7f1f7` (RV-3365: recorded privately), `f77ce01` (RV-3366: recorded privately), `1187b8b` (RV-3367: recorded privately) and `8cb047f` (RV-3368: recorded privately); round 3 on the same branch at `f6c7b9f` (RV-3369: recorded privately) and `e2c1d25` (RV-3376: recorded privately), for the round-3 review:** `--partial` and `--allow-untagged`, given, before or after `--help` and `--version` too, are each refused in one line naming R17, exit 2; `--vendor` refuses an untagged source and a partial one, exit 4, and offers no flag; from a Git source a vendored copy holds the tag's own bytes, read from the tag's tree with no replacement object and no graft, whatever the configuration says — a file that differs on disk, line ends judged by git's own checkout rules, is named and the run refused, with the release's unpacked archive named as the other way, and a path the tag does not hold is named and never copied; a copy vendored through either flag before runs as pinned, and `--check` (exit 0) and the next `--vendor` name it with what to do. The class test, `test_vendor_release.py` (49 checks, run by `test_shoalmark.py`), passes on Python 3.15 and 3.9.6, and its 17 mutants and the tool before R17 each fail it.

**Filed and judged 2026-10-16: In Progress, P2. Built on `fm/061-r17` at `0856fc6`; NOT READY at `e87c073`, which stays on `fm/061-r17` as the record; round 2, on `fm/061-r17-round2`, was NOT READY at `693b1b7`; round 3, the last, is on the same branch, and its review is next.** It carries R17 into v0.20.1 (FM-023's table of
15 October: "R17: partial and untagged vendoring go"). The ruling is the Owner's, signed on 12 October: *"Do you remove
partial/untagged bypasses from trusted vendoring?"*, answered *yes*, to *"prevent agents choosing a weaker trusted pin;
retain verified source and completeness"* (`work-tracker/evidence/rulings-2026-10-12.md`, row R17).

- **Before D3:** `--vendor` took `--partial`, which copied what a Git source had although files were missing, and
  `--allow-untagged`, which permitted a working copy that was not at its release tag or not clean. Either way, a seat
  could pin a weaker source as the trusted one.
- **The build (D3):**
  - both flags go, with every path in `--vendor` that only they open;
  - each flag, when given, prints one line saying that R17 removed it, and exits 2;
  - a configuration or a vendored pin made with either is named by the next `--vendor` and `--check` that meet it,
    with what to do, and `--check` never fails on that alone;
  - the verified source, the completeness checks and the pin stay.

  It is built on `fm/061-r17` from main at `1148114`, after FM-004's carry (#184), since both touch `--vendor`.
- **Tier: critical** (vendoring is the trusted pin). It needs a Builder, a Reviewer in a session of its own (which takes
  R10b too), and one CI run.
- **Its home:** FM-011, the vendoring tracker, is Shipped, and FM-033 refuses a build commit under a tracker not judged
  In Progress. So R17 has a tracker of its own.

## Why

The Owner's ruling R17: no seat may choose a weaker trusted pin than a tagged, verified, complete release.

## Done when

- `--vendor` takes only a tagged, verified, complete release.
- Each of the two flags is refused in one line, with exit 2.
- A copy vendored earlier through either flag is named, never broken.
- The class test holds, and each of its mutants fails it.
- The Reviewer's verdict is READY, and CI is green.

## Ship log

| Date | Event |
|---|---|
| 2026-10-16 | Filed and judged In Progress, P2, by the Planner for v0.20.1's build (D3, R17), before the first build commit. |
| 2026-10-16 | Built by the Builder seat (D3) on `fm/061-r17`, `0856fc6`: both flags refused, exit 2; an untagged or partial source refused; an earlier bypass copy named, never broken. Class test and mutants green on 3.15 and 3.9.6. |
| 2026-10-17 | RV-3364: recorded privately. Fixed by the Builder seat at `29097fb`. `0d5ccee`: `r17_removed` reads both flags by name, as FM-044's launch ratchet requires. Class test (28 checks) and its 11 mutants green on 3.15 and 3.9.6. |
| 2026-10-17 | Round 2 by the Builder seat on `fm/061-r17-round2`, cut at `1aa9d63` (`fm/061-r17` stays at `e87c073`, NOT READY): RV-3365: recorded privately (`7a7f1f7`); RV-3366: recorded privately (`f77ce01`); RV-3367: recorded privately (`1187b8b`); RV-3368: recorded privately (`8cb047f`). Class test (42 checks) and its 14 mutants green on 3.15 and 3.9.6. |
| 2026-10-17 | Round 3 by the Builder seat on `fm/061-r17-round2`, from `693b1b7` (NOT READY): RV-3369: recorded privately (`f6c7b9f`); RV-3376: recorded privately (`e2c1d25`). Class test (49 checks) and its 17 mutants green on 3.15 and 3.9.6. |
| 2026-10-21 | Rebuilt for public history on `fm/061-r17-public`, from `1148114`: the record by the Planner seat at `91ede4a`, and the build by the Builder seat at `968e82a`, as one commit. The tree is the one READY after round 3, but for three lines of this record, which now name their findings only as recorded privately; the review rounds' own commits stay on a private record. |
