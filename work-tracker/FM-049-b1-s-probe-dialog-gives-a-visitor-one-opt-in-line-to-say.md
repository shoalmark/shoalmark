---
id: FM-049
status: Proposed
epic: FM-006
considered: FM-006, FM-004, FM-026
tags: process
next: owner
ask: "Does B1's probe dialog gain one opt-in line after its third step, in English and German, asking a visitor to say in one line what their agent found, even no fit, and where does that line lead?"
ask-kind: ruling
ask-since: 2026-10-14
ask-options: "yes, to an issue form in this repository | yes, to a Discussions category, which you turn on | not now"
ask-proposal: "yes, to an issue form in this repository"
hook: "B1's probe dialog gives a visitor one opt-in line to say what their agent found"
---

# FM-049 — B1's probe dialog gives a visitor one opt-in line to say what their agent found

## What is true now

**Filed 2026-10-14 as a chapter of FM-006; nothing is built.** The line is in B1's probe dialog, FM-006's subject.
FM-006's one ask carries the truth pass on B1's words, and FM-004's slot holds the archive ruling until 20 October,
so this chapter carries the ask, to be answered before the words freeze.

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

- The Owner has ruled whether the line is added and where `{discuss}` leads.
- If it is added: B1's integration carries `dlg_tell` in English and German before the words freeze, and the Reviewer
  finds both texts as ruled.

## Ship log

| Date | Event |
|---|---|
| 2026-10-14 | Filed. |
