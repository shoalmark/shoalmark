---
id: FM-022
kind-of-problem: complicated
status: In Progress
considered: FM-005, FM-006, FM-009, FM-010, FM-018
tags: bug
next: review
hook: "A person finds the three intent lines hard to start: there is no beginning, and no example. *for* reads as if something came before it."
---

# FM-022 — A person finds the three intent lines hard to start — no beginning, no example

## What is true now

**Built 2026-09-23 on `fix/0.17.5-one-id-one-row-and-an-empty-bucket-says-why`, for 0.17.5; open for review, not
merged.** The Owner named it the same day, while writing his own lines. At 0.17.4, `--init` (`TRIAGE_HOME` in
`shoalmark.py`) scaffolded the intent as three bare lines, `- **for** —`, `- **so that** —`, `- **never** —`, under
one italic note about who owns them. Nothing said what each line is for, and there was no example.

**Now the scaffold has** a lead-in in italics that names the repository as a whole (*Three lines in your own words
about the repository as a whole, never one feature of it: what this repository, all of it, is for · what is true when
it works · what no pass or seat may do to get there. The example is a whole product; overwrite it.*) and one generic
example per line, in italics: a village library's whole lending system, not one feature of it. The Owner corrected the
first build, whose example was feature-sized, because his own first draft came out feature-sized after a seat's
feature-sized example. `README.md` §6 says the same where it tells the Owner to write the intent. **The intent is what he wrote**
(`triage_home()`, R5): a paragraph wholly in italics and an example standing alone after a line's dash are the
template's and are dropped, and so is a line with nothing of his left. An untouched scaffold reads as *none is
written*; one line of his reads as exactly that line.

| check | result |
|---|---|
| `--init`: the lead-in naming the whole repository and the three example lines are in `TRIAGE.md` | yes. On 0.17.4: no (fails, as it should) |
| the untouched scaffold, read by `triage_home()` | intent `""` |
| one line overwritten in the Owner's words | read as the intent, exactly that line — not the lead-in or the two examples left (R5; at `8402732` all of them were printed) |

**The German example home** (`examples/de/TRIAGE.md`, which a German adopter copies before `--init`) carries the same
lead-in and a whole-product example in German, in the form a pass drops (R10).

**Not changed, on purpose:** the intent and current-path sections of shoalmark's own `work-tracker/TRIAGE.md`, which
the Owner is writing; and `docs/setup.md` §5 (EN and DE), the documentation site. A repository that ran `--init` before 0.17.5 keeps its file.
`--init` never overwrites it.

**What is left:** review, merge, the tag.

## Why

The intent is the first thing the Owner writes and the line every triage judgement is held against. A form that gives
no way in gets left empty, and while it is empty `--triage` has nothing to judge against.

## Done when

- `--init` writes a lead-in above the three lines, saying they describe the repository as a whole, and one short
  generic example per line, in italics, a whole product, for the person to overwrite. No consumer's or client's content.
- `README.md` says the same where the intent is described.
- A scaffold check pins the lead-in (it names the whole repository) and the three example lines, and shows that the examples alone are not an intent.

## Ship log

| Date | Event |
|---|---|
| 2026-09-23 | R10: `examples/de/TRIAGE.md` gets the lead-in and the whole-product example in German, in the form a pass drops; one check reads it through `triage_home()`. |
| 2026-09-23 | R5: the intent is what the Owner wrote — the lead-in, the examples left in italics and empty lines are not read; the scaffold check now asserts a fresh scaffold has no intent and no path, and one written line is exactly that line. |
| 2026-09-23 | Filed and built: a lead-in that names the repository as a whole and a whole-product example (the Owner's correction of a feature-sized first build) in the scaffold and the README; one check, shown to fail on 0.17.4. |
