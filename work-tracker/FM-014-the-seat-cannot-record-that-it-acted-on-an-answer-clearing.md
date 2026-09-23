---
id: FM-014
status: In Progress
considered: FM-008, FM-005
tags: bug
next: review
hook: "`--clear-ask` moves an answered exchange into the body and removes `answer:` `answered:` `answered-by:` from the front matter. The rights gate reads any change to those three lines as the `answer` transition, which only the owner seat holds — so the seat that holds `ask`, the one whose job clearing is, is refused. Acted-on answers stay in the front matter, and `--answered` lists them as not acted on, for ever."
---

# FM-014 — The seat cannot record that it acted on an answer: clearing is refused as an answer change

## What is true now

**Built 2026-09-23 on `fix/0.17.4-the-answer-says-what-it-does`; merged 2026-09-23 (#12), released as 0.17.4.**
`transitions()` now tells the clearing move from an answer: the three answer lines leave the front matter **and** the
body gains a record under `## Asks` holding the same question, the same answer and the same answered-by (one more such
record than the file had before) — that is `clear`, and `rights_problems` judges it under the **`ask`** right, with its
own words: *this change clears an answered ask*. Removing the lines without the record, or editing the answer's text,
is still `answer`. Five checks in a scratch repository with `[seats]`: the principal's `--clear-ask` passes in the
pre-commit run and in `--check` on the commit; the implementer's is refused naming `ask`; the answer removed with no
record is refused as `answer` and as a ruling gone from the record; the answer's text edited by the principal is
refused as `answer`. Under Subversion nothing changes: the gate reads lines there, and a cleared answer has none.
**What is left:** nothing.

Met by a consumer's principal seat clearing answers the Owner had given.

**Two of FM-008's rules meet head on.** Rule 6 says clearing an ask keeps the record: `--clear-ask <id> <move>` writes
the exchange under `## Asks` (date · question · answer · answered-by) and drops the ask and answer lines. Rule 5's
`transitions()` then reads the same commit:

```python
if any(changed(k) for k in ("answer", "answered", "answered-by")):
    got.add("answer")
```

Removing a line is a change, so clearing is classified as **`answer`** — the owner's right. Under `[seats]` the seat
that asks, acts and clears (`principal`: `ask` · `close` · `triage`) is refused with *this change is a `answer`*. Only
the Owner could clear his own answers, which is the one thing the exchange was designed so he never has to do.

**What follows downstream.** The answers stay in the front matter. `--answered` lists every one of them under
*answered, not yet acted on*, whatever was done about it, and the Owner's view of what his answers became is wrong in
the direction that costs him a sitting.

**Found on the way, not in this tracker's scope:** on a clean tree `--check` judged HEAD against its first parent, so a
merge commit was read as the merger's own change — `--check` on `main` at 0.17.3 is red, refusing FM-007's answer as an
`answer` made by the forge's merge identity. Filed and built as
[FM-019](FM-019-a-merge-commit-is-judged-as-the-merger-s-own-change-and-main-s.md).

## Why

An answer is the Owner's ruling; clearing it is the seat's receipt for acting on it. The gate is right to refuse an
answer written, edited or deleted by a seat — and wrong to treat the receipt as any of those, when the receipt carries
the ruling verbatim into the body.

## Done when

- A change that **removes** the three answer lines **and adds** the matching `## Asks` record — the same question, the
  same answer, the same answered-by — is the clearing move, and is classified under the **`ask`** right.
- Removing the answer **without** its record stays refused; **editing** the answer's text stays `answer`.
- Checks, in a scratch repository with `[seats]`: the principal clears with `--clear-ask` → passes; the implementer
  clears → refused, naming `ask`; the answer removed without its record → refused; the answer's text edited by the
  principal → refused as `answer`.

## Ship log

| Date | Event |
|---|---|
| 2026-09-23 | Merged (#12), released as 0.17.4. |
| 2026-09-23 | Built: the clearing move — lines gone, record added — is judged under `ask`; anything else touching the answer stays `answer`. Five checks. |
| 2026-09-23 | Filed. Reproduced from the rules as shipped in 0.17.0: `--clear-ask` by the principal seat is refused as an `answer` change. |
