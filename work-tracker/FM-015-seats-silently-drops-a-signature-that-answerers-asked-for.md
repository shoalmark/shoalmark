---
id: FM-015
status: Proposed
considered: FM-010, FM-007, FM-008
tags: bug, security
next: build
hook: "From 0.17.1 who may answer is read from `[seats]` alone wherever `[seats]` exists. A repository with `answerers = ['alice signed']` and `[seats] owner = 'alice'` now accepts Alice's unsigned answer, `--answer` stops signing, and the deprecation note tells that repository `answerers` still works — it is not read there at all."
---

# FM-015 — [seats] silently drops a signature that answerers asked for

## What is true now

**Filed 2026-09-23; nothing is built.** Found by a consumer's seat reading the tool before vendoring 0.17.3.

**0.17.1 made `[seats]` the one list.** `may_answer()` returns the seats that hold `answer` wherever `[seats]` exists,
and `answerers` only where it does not — the fix for a repository on `[seats]` that could not answer at all. What it
did not look at: a repository that carries **both**, where `answerers` says `signed` and the seat does not.

| `shoalmark.toml` | before 0.17.1 | from 0.17.1 |
|---|---|---|
| `answerers = ["alice signed"]`, `[seats] owner = "alice"` | Alice's answer must verify | **Alice's unsigned answer counts** |
| the same, `--answer` | commits `-S` | **commits unsigned** |
| the same, the deprecation note | — | *"`answerers` … still works"* — it is not read |

Nothing refuses, nothing warns, and the one line the repository does see tells it the key it relies on is still in
force. The signature requirement — the only thing that makes an answer the Owner's rather than a string anyone can
type (FM-007) — is dropped by an upgrade.

## Why

A signature the configuration asks for and the gate stops checking is a hole opened by an upgrade, in the one part of
the tool that decides whose ruling counts. The repositories that carry both keys are the ones part-way through the
migration FM-010's note asks for — exactly the ones reading that note.

## Done when

- Where `[seats]` exists and an `answerers` entry is `signed` while the seat holding `answer` for that identity is
  not, the gate **refuses** — naming both lines and the fix: add `signed` to the seat, or remove `answerers`. `--answer`
  refuses the same way before it touches anything.
- The deprecation note depends on the repository: with `[seats]` it says `answerers` is **not read for answers here** —
  `[seats]` decides — and can be removed; without `[seats]` it keeps today's words and its removal schedule anchored to
  0.17.3.
- One check per configuration: seats signed + answerers signed → clean · seats unsigned + answerers signed → refused ·
  no seats → today's note · seats and no answerers → silent.

## Ship log

| Date | Event |
|---|---|
| 2026-09-23 | Filed from a consumer seat's reading of 0.17.3 before vendoring it. |
