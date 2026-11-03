---
id: FM-049
status: Shipped
epic: FM-006
considered: FM-006, FM-004, FM-026
tags: process
next: build
hook: "B1's probe dialog gives a visitor one opt-in line to say what their agent found"
---

# FM-049 — B1's probe dialog gives a visitor one opt-in line to say what their agent found

## What is true now

**2026-11-03 — Shipped in v0.20.1; it closes with FM-006 at v0.20.2.** The Owner ruled the line in (`54e6dd4`), and
FM-004's signed answer of 21 October chose one feedback channel, the landing's form, which settles where `{discuss}`
leads. B1's dialog carries `dlg_tell` in English and German (`b4dcc10`, with the ruled destination and text in
`f6f3660`). It is joined into v0.20.1 by `96ddaf4`, and the landing's re-check found it as ruled (`0fc30d2`).

**Filed 2026-10-14 as a chapter of FM-006; nothing is built.** The line is in B1's probe dialog, FM-006's subject.
FM-006's one ask carries the truth pass on B1's words, so this chapter carries the ask, to be answered before the
words freeze.

**2026-10-14 — one opt-in line after the probe dialog's third step.**
- A new key after `dlg_s3`, shown in the dialog and under the start section's coin lines:
  - EN `dlg_tell`: `Tried it? Tell us what your agent found, even "no fit": <a href="{discuss}">one line here</a>. The prompt never asks your agent to post.`
  - DE `dlg_tell`: `Ausprobiert? Sagen Sie uns, was Ihr Agent gefunden hat, auch „passt nicht“: <a href="{discuss}">eine Zeile hier</a>. Der Prompt bittet Ihren Agenten nie, etwas zu posten.`
- **Why:** the probe's agent reports only to its own Owner, never to shoalmark. Nothing on the page lets a visitor say
  what fitted or did not.
- **The last sentence states the prompt, not an agent's conduct.** The page can promise the prompt's words, not what
  an agent does. No probe file, adoption note or landing partial mentions posting at `4907071`.
- **`{discuss}` is part of the ruling:**
  - an issue form is a file in this repository, written and reviewed like any other;
  - a Discussions category is a repository setting only the Owner can change.
- **Offered, for the ruling:** whichever it leads to, the target is public. One more sentence would say so:
  `Leave out anything private.` / `Lassen Sie Privates weg.`
- **Confidence:** 70 % for the line; 55 % for the issue form over Discussions.
- **Holds up:** the dialog's words freeze, with FM-006's ask.
- **Source:** the go-to-market review of B1, recorded privately.

## Done when

- [x] The Owner has ruled whether the line is added and where `{discuss}` leads. · `54e6dd4`
- [x] If it is added: B1's integration carries `dlg_tell` in English and German before the words freeze, and the Reviewer
  finds both texts as ruled. · `b4dcc10`, `f6f3660`, `96ddaf4`, `0fc30d2`

## Asks

**2026-10-15** · Does B1's probe dialog gain one opt-in line after its third step, in English and German, asking a visitor to say in one line what their agent found, even no fit, and where does that line lead?
**answered** — accepted - yes, to an issue form in this repository · holgo99
**relation** — accepted the proposal
**signed** — 54e6dd4 · G

## Ship log

| Date | Event |
|---|---|
| 2026-10-14 | Filed. |
| 2026-11-03 | **Shipped in v0.20.1** (`b4dcc10`, joined by `96ddaf4`); closed with FM-006 at v0.20.2. Records only. |
