---
id: FM-037
status: In Progress
considered: FM-008, FM-033, FM-007, FM-019, FM-022, FM-014
tags: bug
triaged: 2026-09-25
rank: 1
next: build
tier: P1
hook: "a seat can change the Owner's intent and current path in TRIAGE.md, and the gate lets it through"
---

# FM-037 — a seat can change the Owner's intent and current path in TRIAGE.md, and the gate lets it through

## What is true now

**Filed 2026-09-25 at the Owner's word; nothing is built.** A seat can commit a change to the text under `## The intent` or
`## The current path` in `work-tracker/TRIAGE.md` — unsigned, under any identity — and `--check` and `--session-check` exit 0. Every
real change to those two sections on shoalmark's main is the Owner's signed commit (6 with `%G?` G, `45198d5` … `ad9bf67`; `ae1f05e`
is a move with no text change). The gate judges *what* is built against judged trackers (FM-033); it does not yet judge *who* may
change the Owner's own two sections. The site's claim that only the Owner changes them is, until this is built, a written rule (FM-006).

## Why

**The Owner's word, through the Auditor seat, as pasted at 18:58:54 on 2026-09-25 (sha256 `12e77e729474720ac28bf4b8af55e0663b1fea490654c7f86e5044e69b1c74bf`):**

The Owner's word (through the Auditor seat, 2026-09-25): "stop a seat from editing your TRIAGE.md — let's fix this first." A bug filing (the freeze admits it); the finding is the Auditor seat's AU-12.
Title: a seat can change the Owner's intent and current path in TRIAGE.md, and the gate lets it through.
Evidence: a local probe on shoalmark main b336a53 (never pushed): an unsigned commit by a made-up identity rewrote path line 4; --check asked only for INDEX to be regenerated, then --check and --session-check exited 0. History: every real change to the two sections on shoalmark main is the Owner's signed commit (6 G, 45198d5 … ad9bf67; ae1f05e is a move with no text change). PortDive's two sections were last changed unsigned on 09-20 (f99ebdbb, 70fa4fa1), before signing existed.
Done when:
1. --check refuses a commit, among the branch's own commits (not on its base), that changes the text under "## The intent" or "## The current path" — or renames or removes those headings, deletes or moves TRIAGE.md, or points the tracker directory elsewhere — unless it is the owner's signed commit: %G? G and the signer principal = the author's email = the owner's (the test --answer uses). A merge is checked for a section text neither parent had.
2. The refusal names the commit and the section, and the way through: the Owner commits it signed; a seat proposes the change as an ask.
3. The Passes section stays open to seats; the scaffold --init writes is accepted.
4. --queue reads such a pull request as wait: TRIAGE.md changed unsigned.
5. Where the owner's seat is not marked signed, and on Subversion, the refusal says what it can prove (the author only) — or Subversion is stated out of scope.
6. Its limit, stated in the message and the docs: a commit signed with the Owner's key passes; at tier 0 any process on his account holds that key (FM-007).
7. Tests: synthetic cases for each clause, and the real history (the 6 G commits and ae1f05e accepted).
Tier: the gate — critical under path line 3; the Owner's cold session reviews it. The Auditor verifies after, against a plan sealed at 18:57:38 (its hash is with the Owner).
Then the site page on FM-006 can say "only you change it" as enforced by the tool, with its tier-0 limit.

The finding is the Auditor seat's AU-12; the filing is the Principal's, at the Owner's word (*let's fix this first*), read as: before
the 0.18.4 release is cut, this guard is in it. Held against FM-008 (the ask reaches the Owner only through the gate — the same class of
enforcement, for asks), FM-033 (the judged-before-build gate — the walker this guard joins), FM-007 (the tier-0 limit the message must
state), FM-019 (a merge is never judged as the merger's own change — the merge clause here), FM-022 (the intent lines' form — untouched), FM-014 (the rights gate — the seat rights this guard reads).

## Done when

The seven clauses of the Owner's word above, as written, each with its synthetic test and the real history accepted (clause 7).
**Tier: the gate — critical under path line 3; the Owner's cold session reviews it; the Auditor seat verifies after, against its plan
sealed at 18:57:38.** Then FM-006's site page may say *only you change it* as enforced by the tool, with its tier-0 limit stated.

## Ship log

| Date | Event |
|---|---|
| 2026-09-25 | Correcting the filing's attribution: the Owner's own words, at 18:55:33 to the Auditor seat, were `stop a seat from editing your TRIAGE.md` - let's fix this first then (spelling normalised). The part in backticks quotes the Auditor seat's line of the minute before; the relay of 18:58:54 wrote the two as one, as the Owner's word. His order stands as filed. |
| 2026-09-25 | In Progress — 0.18.4 builds it on its own branch after this pass lands; the status set here, on the pass branch, before the first build commit (the Auditor seat's AU-20). |
| 2026-09-25 | Filed at the Owner's word (*stop a seat from editing your TRIAGE.md — let's fix this first*), through the Auditor seat at 18:58:54; the filing text is the paste word for word, its hash above. Judged the same day: P1, rank 1, build (the pass of 2026-09-25, the triage guard). |
