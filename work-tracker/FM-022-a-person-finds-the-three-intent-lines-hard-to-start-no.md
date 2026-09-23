---
id: FM-022
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
feature-sized example. `README.md` §6 says the same where it tells the Owner to write the intent. The examples do not count as an intent: `triage_home()` already strips italics before
it asks whether anything was said, so an untouched scaffold still reads as *none is written*.

| check | result |
|---|---|
| `--init`: the lead-in naming the whole repository and the three example lines are in `TRIAGE.md` | yes. On 0.17.4: no (fails, as it should) |
| the untouched scaffold, read by `triage_home()` | intent `""` |
| one line overwritten in the Owner's words | read as the intent |

**Not changed, on purpose:** the intent and current-path sections of shoalmark's own `work-tracker/TRIAGE.md`, which
the Owner is writing; `examples/de/TRIAGE.md`, the German example, which `--init` does not write; and
`docs/setup.md` §5 (EN and DE), the documentation site. A repository that ran `--init` before 0.17.5 keeps its file.
`--init` never overwrites it.

**What is left:** review, merge, the tag.

## Why

The intent is the first thing the Owner writes and the line every triage judgement is held against. A form that gives
no way in gets left empty, and while it is empty `--triage` has nothing to judge against.

## Done when

- `--init` writes a lead-in above the three lines, saying they describe the repository as a whole, and one short
  generic example per line, in italics, a whole product, for the person to overwrite. No PortDive or client content.
- `README.md` says the same where the intent is described.
- A scaffold check pins the lead-in (it names the whole repository) and the three example lines, and shows that the examples alone are not an intent.

## Ship log

| Date | Event |
|---|---|
| 2026-09-23 | Filed and built: a lead-in that names the repository as a whole and a whole-product example (the Owner's correction of a feature-sized first build) in the scaffold and the README; one check, shown to fail on 0.17.4. |
