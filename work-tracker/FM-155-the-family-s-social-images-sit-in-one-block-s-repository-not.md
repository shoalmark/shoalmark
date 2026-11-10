---
id: FM-155
status: Shipped
considered: FM-006, FM-104, FM-152
tags: process
next: build
triaged: 2026-11-09
tier: P2
hook: "shoalmark.tools is a family of building blocks with a public press kit, shoalmark/brand, but the family's social images, the profile header, the repository card and the link previews, still sit in brand/social/ of one block's repository."
---

# FM-155 — The family's social images sit in one block's repository, not in the press kit

## What is true now

**2026-11-10 — Shipped: merged to main as #283 (`6ee9702`).** `brand/social/` holds one README, which points to
the press kit's `social/` and names shoalmark/brand's `070a4dd`. The ten files left this repository in `d24fe5e`,
and the German du test's list no longer names `link-preview-de.svg`. Every Done when item is met.

- **The site:** no build step reads `brand/social/`. Built as `docs.yml` builds it, before and after the move, it
  holds the same 258 files, byte for byte: the Planner's builds at `611cfa0` and `d24fe5e`, the review's at
  `1bcc81d` and `d24fe5e`.
- **The review:** a standard review, READY at `d24fe5e` with no finding (`8c6c6d9`), merged with #283.

**2026-11-09 — the Owner accepted FM-155-Q1, and FM-155 is judged before its first build commit: keep P2, In
Progress.** The Owner's signed answer (`ee8aa9a`) accepts the move as proposed; its exchange stands under Asks. A
partial triage pass judged this row alone ([worksheet](evidence/triage/triage-2026-11-09.md)). Unranked. The move
follows on a branch from main, with a standard review.

**Filed 2026-11-09; nothing is built, and FM-155 waits for the Owner's ruling, FM-155-Q1.** No build commit lands
before its signed answer: the move changes a public repository.

- **Where they are:** [`brand/social/`](../brand/social/) holds ten files: the SVG sources of the profile header,
  the repository card and the two link previews, their PNG and JPEG exports, and a README.
- **Where they go:** shoalmark/brand, the organization's public press kit, holds the same ten files byte for byte
  since its main `070a4dd`, beside the logos, the seat icons and the terms for using the marks.
- **What stays:** `brand/design-guide.md`, `brand/icons/` and `brand/seats/`, which the tool, the start page and the
  tests read.
- **What reads them:** `test_shoalmark.py` lists `brand/social/link-preview-de.svg` among the German prose sources
  held to du. No build step reads `brand/social/`: the site serves its own copies of the link previews,
  `docs/assets/preview.png` and `preview-de.png`.
- **The trackers that cite `brand/social/`** (FM-006, FM-023, FM-152) are history, and their text stays.

## Why

The social images belong to the family, not to one block. In the press kit they sit with the family's other marks,
where anyone who shares a shoalmark.tools block finds them, and the shoalmark repository keeps only what it reads.

**Held against** (`considered:`):
- [FM-006](FM-006-shoalmark-has-one-document-written-for-agents-the-humans-who.md) is not this work: it gave the
  people who own the repositories a page of their own, and filed the social images in `brand/social/` on 21 October.
  This moves them out.
- [FM-104](FM-104-the-person-s-own-files-are-spread-over-the-repository-and.md) is not this work: it gathers the
  person's own files. The social images are the family's.
- [FM-152](FM-152-an-x-post-image-the-agents-never-answer-for-you-the-software.md) is not this work: it is an X post
  image for the Owner to judge, kept in its evidence, and puts nothing on the site.

## Done when

- [x] `brand/social/` holds one README, which points to the press kit's `social/` and names the commit, `070a4dd`,
  that holds the ten files.
  · `d24fe5e`, merged in `6ee9702`
- [x] `test_shoalmark.py`'s German prose list no longer names `link-preview-de.svg`, whose text now lives in
  shoalmark/brand.
  · `d24fe5e`
- [x] No build step reads `brand/social/`, and the built site is unchanged.
  · 258 files, byte for byte, before and after `d24fe5e`, in the Planner's builds and the review's
- [x] A standard review's READY.
  · READY at `d24fe5e`, `8c6c6d9`

## Asks

**FM-155-Q1** · 2026-11-09 · Shall FM-155 move brand/social/'s ten files out of the shoalmark repository, leaving one README that points to the press kit's social/ at shoalmark/brand's 070a4dd, take link-preview-de.svg out of the German du test's list, and keep the built site unchanged, as FM-155's *What is true now* sets out?
**answered** — accepted - yes, as proposed · holgo99
**relation** — accepted the proposal
**signed** — ee8aa9a · G

## Ship log

| Date | Event |
|---|---|
| 2026-11-10 | Shipped: merged to main as #283 (6ee9702). brand/social/'s ten files moved to the press kit (d24fe5e), the review READY (8c6c6d9), and every Done when item is met. |
| 2026-11-09 | FM-155-Q1 accepted by the Owner (ee8aa9a), cleared by the tool's move; judged keep P2 by a partial triage pass; In Progress. Records only. |
| 2026-11-09 | Asked the Owner: FM-155-Q1, a ruling on moving brand/social/ to the press kit, shoalmark/brand. |
| 2026-11-09 | Filed, on the Auditor's word of 9 November, after #280 merged. |
