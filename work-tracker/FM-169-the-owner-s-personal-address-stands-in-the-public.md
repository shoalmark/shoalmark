---
id: FM-169
status: Proposed
considered: FM-015, FM-019, FM-024, FM-029, FM-037, FM-156, FM-166
tags: security, process
next: review
hook: "shoalmark.toml's top-level owner names the Owner's personal address beside the forge noreply address, and the signers file lists the Owner's two keys under the personal address alone, so every clone carries it. The proposal: the personal address leaves owner and the signers file, the keys are listed under the forge noreply address, and the Owner commits under it from then on. A design round comes first, and no ask is put until it closes. No release is named."
---

# FM-169 — the Owner's personal address stands in the public configuration and the signers file, so every clone carries it

Seat: the Planner (27f31560) · filed 2026-11-13, on the Auditor's word of that day.

## What is true now

**Filed 2026-11-13, Proposed; no release is named, no ask is put, and nothing is built.** A design round comes first
(`next: review`).

This tracker names the two identities only as "the Owner's personal address" and "the Owner's forge noreply address".
Neither is written out here, in a commit or in a message.

- **The configuration:** `shoalmark.toml`'s top-level `owner` lists both identities, each `signed`
  ([L2](https://github.com/shoalmark/shoalmark/blob/01a929b8c4b8128e4ca41d4049a89e2f9b7f956d/shoalmark.toml#L2)).
- **The signers file:** `work-tracker/allowed_signers` lists the Owner's two keys, each under the personal address
  alone ([L1–L2](https://github.com/shoalmark/shoalmark/blob/01a929b8c4b8128e4ca41d4049a89e2f9b7f956d/work-tracker/allowed_signers#L1-L2)). The signing page has each line start with "the email the
  key speaks for, then the key" ([`docs/signing.md` L151–L152](https://github.com/shoalmark/shoalmark/blob/01a929b8c4b8128e4ca41d4049a89e2f9b7f956d/docs/signing.md#L151-L152)).
- **The history,** counted at main `01a929b`:
  - 193 commits are committed under the personal address, from 21 September to 9 November 2026;
  - 264 merge commits are authored under the forge noreply address, and committed by the forge;
  - none is committed under the forge noreply address.

  History keeps them all, and no rewrite is proposed.
- **Where the tool reads them:**
  - `owners_of()` maps each identity of `owner` and `[seats]` that holds `answer` to whether it must sign
    ([`shoalmark.py` L9442–L9460](https://github.com/shoalmark/shoalmark/blob/01a929b8c4b8128e4ca41d4049a89e2f9b7f956d/shoalmark.py#L9442-L9460));
  - `owners_at()` reads them from the default branch's configuration, so a branch never names its own Owner
    ([L9462–L9490](https://github.com/shoalmark/shoalmark/blob/01a929b8c4b8128e4ca41d4049a89e2f9b7f956d/shoalmark.py#L9462-L9490));
  - the guard keeps the signers files: the one `gpg.ssh.allowedSignersFile` names, and the default branch's
    `allowed_signers` in the tracker folder ([L9340–L9350](https://github.com/shoalmark/shoalmark/blob/01a929b8c4b8128e4ca41d4049a89e2f9b7f956d/shoalmark.py#L9340-L9350)). For a commit that does not
    verify, the refusal says a key lands in that file first ([L6990](https://github.com/shoalmark/shoalmark/blob/01a929b8c4b8128e4ca41d4049a89e2f9b7f956d/shoalmark.py#L6990)).

## Why

A personal address in a public configuration and a public signers file is in every clone and fork, and on every page
that shows them. It is also an address a stranger can write to. The forge gives each account a noreply address for
this case, and the record needs to know the Owner by an identity, not by a personal address.

## Decisions, for the design round

1. **The change:**
   - the personal address leaves `owner`;
   - the Owner's keys are listed in the signers file under the forge noreply address, and the personal address leaves
     that file;
   - the Owner commits under the forge noreply address from then on.
2. **No rewrite:** earlier commits keep the personal address, and history is not rewritten.
3. **The design round answers four questions,** with evidence from the code and a probe:
   1. which checks read the Owner's identities and the signers file's principals, and for which commits: a branch's
      range, the recorded answers, the Board's answered-by, and
      [FM-029](FM-029-the-answer-says-accepted-when-the-person-picked-another.md)'s relations;
   2. whether earlier commits and signed answers under the personal address still verify, and still read as the
      Owner's, after the change;
   3. the order of the change, the keys listed again under the forge noreply address first and the personal address
      removed after, so that no check fails between the two steps;
   4. how it meets [FM-166](FM-166-seats-and-rights-are-kept-in-shoalmark-toml-s-own-tables.md): whether the top-level
      `owner` moves into the roster follows sealanes/1's shape (FM-166's decision 5), and the Owner's identities move
      with it.
4. **The probe runs in scratch only:** a throwaway repository with test keys. It never signs with the Owner's keys,
   never writes this repository's history, and never opens the Owner's own checkout.
5. **The review is critical:** it touches signing and identity.
6. **The ask** is drafted after the design round, and names the release.

**Where it meets other trackers:**

- [FM-024](FM-024-a-seat-s-commit-names-its-session-and-the-record-knows-the.md): a seat's identities, one or a list,
  and the Owner who is not a seat.
- [FM-037](FM-037-a-seat-can-change-the-owner-s-intent-and-current-path-in.md): the guard over the Owner's
  two sections and the signers file.
- [FM-015](FM-015-seats-silently-drops-a-signature-that-answerers-asked-for.md) and
  [FM-019](FM-019-a-merge-commit-is-judged-as-the-merger-s-own-change-and-main-s.md): how a signed identity and a merge
  are read.
- [FM-156](FM-156-the-seats-principal-and-implementer-the-former-names-of.md): the old seat names
  still read beside the new.

## Done when

Each item names its commit or pull request when it lands.

- [ ] **The design round** answers its four questions, with its evidence filed, and its critical review is READY.
- [ ] **The Owner has answered** the ask the design round drafts.
- [ ] **The change lands in the order the design round sets:** the Owner's keys listed under the forge noreply address,
  and the personal address in neither `owner` nor the signers file, with `--check` passing after each step.
- [ ] **Earlier commits and signed answers** under the personal address still verify and read as the Owner's, under a
  test, or the design round's finding says why not and what follows.
- [ ] **README and `docs/signing.md`,** with their German twins, say why the Owner's identity is the forge noreply
  address.
- [ ] **The critical review is READY.**

## Ship log

| Date | Event |
|---|---|
| 2026-11-13 | Filed, Proposed, with no release and no ask: the personal address leaves owner and the signers file, after a design round. Records only. |
