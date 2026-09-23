---
id: FM-010
status: Shipped
considered: FM-008, FM-005
tags: bug
kind-of-problem: obvious
hook: "The note that tells a repository `answerers` is going away is guarded by `if ANSWERERS and SEATS:` — it fires only where both keys are present. A repository still wholly on `answerers`, which is the entire population the deprecation is aimed at, is never told. The key is advertised for removal in the next release, so removing it on that promise breaks exactly the repositories that were never warned."
---

# FM-010 — The `answerers` deprecation warning never reaches the repositories still on `answerers` alone

## What is true now

**Built 2026-09-22 on `fix/0.17.3-version-drift-and-the-silent-deprecation`; merged 2026-09-22 (#10), released as 0.17.3.**
Found by an outside consumer the day their repository became the affected population, and reproduced here. The
guard is now `ANSWERERS` alone, and the note no longer repeats a removal date that was never served: `answerers` is
removed no sooner than the release after 0.17.3, said in those words in the note, the CHANGELOG and here. Three checks, one per
configuration; the two that matter fail against the restored guard. **What is left:** nothing here;
`answerers` is removed no sooner than the release after 0.17.3.

**The guard is inverted.** `shoalmark.py:2271`:

```python
if ANSWERERS and SEATS:
    print("  note: `answerers` is the old name for the `answer` right and still works — … it goes in the release after this one")
```

The `and` means the note reaches only a repository holding *both* keys — one that has already begun migrating. A
repository on `answerers` with no `[seats]` at all hears nothing. Confirmed by running the gate against both
configurations:

| `shoalmark.toml` | deprecation note |
|---|---|
| `answerers` only, no `[seats]` | **silent** |
| `answerers` + `[seats]` | fires |

The warning is being shown to the repositories that need it least and withheld from the ones it exists for.

**The removal promise is what makes it sharp.** The note's own words are *"it goes in the release after this one"*, and
it first shipped in 0.17.0. Nothing in the trackers schedules the removal independently — that sentence is the whole
schedule. So the timetable is being announced only to the population it does not apply to. Drop `answerers` on that
promise and the silent repositories break cold, having been told nothing: `may_answer()` falls back to
`dict(ANSWERERS)` where there are no seats (`shoalmark.py:2026-2028`), so with the key gone every answer is refused
and `--answer` — the only supported route — stops working.

**Not visible from inside this repository.** `shoalmark.toml` here carries `[seats]` and no `answerers`, so the gate
is silent for us under either behaviour and we would never have surfaced it from our own runs.

**A note for whoever builds this:** `read_config` scopes a bare key into whichever `[table]` is open
(`shoalmark.py:112`), so a test configuration must put `answerers` *above* every table header. Appending it to the end
of an `--init` config silently makes it `[tags].answerers` and the case reads as a false negative.

## Why

A deprecation that does not reach the deprecated is not a deprecation — it is a removal with a grace period nobody was
served. The cost is paid entirely by outside adopters: this repository cannot see the fault, and the consumer who
found it did so only by moving onto `answerers` and noticing the silence.

## Done when

- The note fires for **any** repository configured with `answerers`, whether or not `[seats]` is present — the guard
  drops to `ANSWERERS` alone.
- A repository on `[seats]` with no `answerers` stays silent; the fix adds no new false warning.
- Tests cover all three configurations — `answerers` alone, both keys, `[seats]` alone — with `answerers` placed above
  any table header so the case is real.
- **The removal clock restarts: `answerers` is removed no sooner than the release after 0.17.3** — the first release
  whose warning reaches the affected repositories. The schedule is stated in exactly those words in all three places
  that carry it — the note, the CHANGELOG and this tracker — and is anchored to the version, never to *"this
  release"*: the note prints unchanged in every later release, so a floating anchor restarts the countdown forever.
  **The length of that grace is the Owner's to rule on; one release is what the original promise offered, and this
  restores it to repositories that were never served it.**
- Ships as **0.17.3**, alongside FM-009.

## Ship log

| Date | Event |
|---|---|
| 2026-09-22 | Merged (#10), released as 0.17.3. |
| 2026-09-22 | Built: the guard drops to `ANSWERERS`, the note's removal wording corrected, three checks. Both suites green (200 checks). Open for review. |
| 2026-09-22 | Filed. Reported by an outside consumer against their own `answerers`-only repository; both configurations reproduced here. |
