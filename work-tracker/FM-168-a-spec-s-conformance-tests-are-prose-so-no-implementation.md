---
id: FM-168
status: Proposed
considered: FM-042, FM-100, FM-153, FM-161, FM-165, FM-166
tags: process
next: owner
hook: "hail/1's first edition names its conformance tests in sentences, and its repository holds no case files. No implementation can run them, and a second one would learn the rules from the first. The Owner's words of 16, 20 and 21 November settled where the cases live: each spec's as plain files in a repository of their own, which the spec's repository holds pinned to the edition's commit, with a new case coming only through the spec. FM-168-Q2 asks the rest: every implementation runs the whole case set in its CI, the spec and its cases are the reference, and a private repository is named in public text, never linked. No release is named."
ask-id: FM-168-Q2
ask: "Do you take what is left of FM-168's decisions 3, 4 and 7: every implementation runs its edition's whole case set in CI and claims it only while every case passes; the spec and its cases are the reference, never an implementation; and a private repository is named in public text, never linked?"
ask-kind: ruling
ask-since: 2026-11-21
ask-options: "yes, as proposed | yes, with the changes I name | no, not now"
ask-proposal: "yes, as proposed"
---

# FM-168 — a spec's conformance tests are prose, so no implementation can run them and a second one would learn the rules from the first

Seat: the Planner (27f31560) · filed 2026-11-13, on the Auditor's word of that day.

## What is true now

**2026-11-21 — hail/1's cases get a repository of their own; FM-168-Q2 is put.** On the Owner's word of 21 November:
- hail/1's cases sit in a repository of their own, shaped as sealanes/1's: the cases as plain files, their schema, the
  refusal codes and a README. shoalmark/hail holds it at `conformance/` as a submodule pinned to the edition's commit
  (decisions 1 and 2, now for hail/1 too). It stays private until its setup is done.
- No signed file of hail/1's next edition changes for it, and that edition's publication does not wait for it.
- The cases the implementation in a second language holds for hail/1 move there, once a reader who did not write them,
  on another model, has read them against the edition's text. The set says which of §11's tests have no case yet.
- From then on a new case comes through the spec, never from what an implementation does (decision 4's last part).
- A plan comes to the Owner before anything is built or moved.

FM-168-Q2 asks what no word has settled: decision 3, the first two parts of decision 4, and decision 7. Decision 6's
open parts are not in it, as that word names the ask, and they stay open.

**2026-11-20 — FM-168-Q1 withdrawn, with no answer given.** Later words of the Owner's settled part of what it asked:
- **16 November:** sealanes/1's cases sit in a repository of their own, which the spec's repository holds pinned to
  the edition's commit (decisions 1 and 2).
- **20 November:** the implementation in a second language keeps no copies of the specs, and reads the filed editions
  at a named commit (decision 5).
- **20 November, by a signed answer:** the edition of hail/1 that rests on sealanes/1 is published no earlier than
  sealanes/1's first edition is public (decision 6).

On the Owner's word of 20 November, an ask a later word has overtaken is withdrawn, and is not put again as it stands. A
new ask will cover what no later word settled: decisions 3, 4 and 7, and when chart is public.

**Filed 2026-11-13, Proposed; no release is named, and nothing is built.** Its ask, FM-168-Q1, put its decisions to the
Owner.

- **hail/1 today:**
  - Its first edition is public and not yet in force
    ([`spec/hail-1.md` L3](https://github.com/shoalmark/hail/blob/f5b160698a180481240dbff5c8cc605aaab06121/spec/hail-1.md#L3)).
  - "§11's tests are how conformance is checked" ([L24](https://github.com/shoalmark/hail/blob/f5b160698a180481240dbff5c8cc605aaab06121/spec/hail-1.md#L24)).
  - [§11](https://github.com/shoalmark/hail/blob/f5b160698a180481240dbff5c8cc605aaab06121/spec/hail-1.md#L963) is headed "codebase and static analysis, not prose". It lists what `hail check` checks, and
    numbers its tests, each a sentence ([its first tests](https://github.com/shoalmark/hail/blob/f5b160698a180481240dbff5c8cc605aaab06121/spec/hail-1.md#L1015-L1017)).
  - No file holds a case's input, its expected accept or refuse, or a reason code. The repository holds the spec, a
    README, a quickstart and its licences.
  - How hail/1's tools are built is open
    ([L1013](https://github.com/shoalmark/hail/blob/f5b160698a180481240dbff5c8cc605aaab06121/spec/hail-1.md#L1013)).
- **sealanes/1:** the roster spec, in shoalmark/sealanes, not yet public.
  [FM-100](FM-100-the-stand-up-prompt-is-code-and-english-on-every-board-while.md)'s decision 9 names it, and
  [FM-166](FM-166-seats-and-rights-are-kept-in-shoalmark-toml-s-own-tables.md) waits on its table's shape. A later
  edition of hail/1 takes its roster from it.
- **chart:** in shoalmark/chart, not yet public.
  [FM-088](FM-088-the-team-s-lessons-live-only-in-each-harness-s-local-memory.md) and its four trackers move there,
  by their dated lines of 2026-11-13.

## Why

A spec whose tests only an implementation can run is that implementation's spec. A second implementation then learns
the rules by reading the first, and where the two differ no one can say which is right. Cases kept as plain files,
versioned with the edition, let anyone check an implementation against the text. A spec that a release reads must be
public before that release, or an adopter cannot read the rules the tool holds them to.

## Decisions, for the Owner

1. **Conformance cases, as plain files:**
   - each spec, hail/1 and sealanes/1, ships its conformance cases as plain files in its own repository;
   - each case holds its input, the expected result, accept or refuse, and the reason code of a refusal.

   Settled for both specs, sealanes/1 on 16 November and hail/1 on 21 November: the cases sit in a repository of their
   own, which the spec's repository holds at `conformance/`, pinned to the edition's commit.
2. **Versioned with the edition:** a case set belongs to one edition of its spec. A new edition ships its own.
   Settled with decision 1.
3. **Run by every implementation in CI:** an implementation runs the whole case set of the edition it claims, in its
   CI, and claims that edition only while every case passes. Asked in FM-168-Q2.
4. **The reference:**
   - the spec and its cases are the reference, never one implementation;
   - where an implementation and a case differ, the implementation is fixed, or the spec is changed by its own rule;
   - a missing case is added through the spec, in its repository, never taken from what an implementation does.

   The last part is settled, on 21 November: a new case reaches the cases' repository through the spec. The first two
   are asked in FM-168-Q2.
5. **An implementation in a second language:**
   - it targets the edition of hail/1 that takes its roster from sealanes/1, directly, not the first edition;
   - it builds the frame, the grammar, the markers and the receipts first;
   - it builds the roster once sealanes/1 has settled the table's shape.

   Settled on 20 November: it reads the filed editions at a named commit and keeps no copies of the specs.
6. **When each spec is public:**
   - sealanes/1 is public at its first edition, and before any shoalmark release that reads `[roster]`;
   - the edition of hail/1 that takes its roster from sealanes/1 is public with it;
   - chart is public at chart/1's first edition.

   Its hail/1 part is settled, on 20 November, by a signed answer: the edition of hail/1 that rests on sealanes/1 is
   published no earlier than sealanes/1's first edition is public. The rest, sealanes/1 before a release that reads
   `[roster]` and when chart is public, stays open, and no ask carries it now.
7. **A private repository in public text:** it is named, never linked, and called "not yet public" until it is
   public. Asked in FM-168-Q2.

No release is named.

**Where it meets other trackers:**

- [FM-166](FM-166-seats-and-rights-are-kept-in-shoalmark-toml-s-own-tables.md) reads `[roster]`. If its lane ships
  in v0.20.3, decision 6 puts sealanes/1's first edition in public before v0.20.3's tag.
- [FM-165](FM-165-a-tracker-can-only-be-closed-by-hand-so-its-open-asks-where.md)'s `--moved-to` names a tracker in
  another repository, and its first use is shoalmark/chart. Its record follows decision 7: the repository is named,
  not linked.
- [FM-042](FM-042-requirements-in-the-repository-tested-as-a-contract-a-layer-for.md), parked, asks the same of an
  adopter's requirements: tested as a contract, not by reading the implementation.
- [FM-161](FM-161-a-team-can-only-be-one-whole-repository-so-a-team-in-a.md) waits on sealanes/1 to be in force.
- [FM-153](FM-153-a-blog-for-the-site-and-its-first-post.md)'s first post links hail/1's published first edition.

## Done when

Each item names its commit or pull request when it lands.

- [ ] **The Owner has answered FM-168-Q2,** on what is left of decisions 3, 4 and 7.
- [ ] **hail/1's cases are plain files** in a repository of their own, which shoalmark/hail holds at `conformance/`
  pinned to the edition's commit, each with its input, its expected accept or refuse, and the reason code of a refusal.
- [ ] **sealanes/1's first edition ships with its cases.**
- [ ] **Each implementation's CI runs the whole case set** of the edition it claims.
- [ ] **sealanes/1 and the edition of hail/1 that takes its roster from it are public** before the first shoalmark
  release that reads `[roster]`.
- [ ] **chart is public** at chart/1's first edition.
- [ ] **Decision 7 is in the agents' contract,** `AGENTS.md`.

## Asks

**FM-168-Q1** · 2026-11-20 · Do you take FM-168's decisions as proposed: plain-file conformance cases for each spec, run in CI by every implementation, the spec and its cases as the reference, a second implementation aimed at a later edition of hail/1, and sealanes/1 and chart public at their first editions?
**withdrawn** — no answer was given

## Ship log

| Date | Event |
|---|---|
| 2026-11-21 | On the Owner's word of 21 November, hail/1's cases get a repository of their own, which shoalmark/hail holds at `conformance/` pinned to the edition's commit; decisions 1 and 2 now hold for hail/1 too, and decision 4's last part is settled. FM-168-Q2 is put on what is left of decisions 3, 4 and 7; decision 6's open parts stay open; `next: owner`. Records only. |
| 2026-11-20 | FM-168-Q1 withdrawn, with its record under *Asks*: the Owner's words of 16 and 20 November settled decisions 1, 2, 5 and 6. The hook and *Done when* say so, and a new ask will cover decisions 3, 4 and 7 and chart; `next: build`. Records only. |
| 2026-11-13 | Filed, Proposed, with FM-168-Q1 put: plain-file conformance cases for each spec, the spec and its cases as the reference, a second implementation's target, and when each spec goes public. No release. Records only. |
