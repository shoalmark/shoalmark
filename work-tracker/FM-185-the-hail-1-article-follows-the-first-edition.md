---
id: FM-185
status: Proposed
considered: FM-153, FM-168
tags: process
next: wait
hook: "The hail/1 article on the site follows hail/1's first edition, and both pages shoalmark/hail publishes send readers to it. On the Owner's answer to FM-185-Q1, the article is not tied to the edition: the next edition is published without waiting for it, and the article is revised after that publication, on a day the Owner names. Until then it waits."
---

# FM-185 — the hail/1 article follows the first edition

Seat: the Planner (a1730572) · filed 2026-11-20, on the coordinator's word of that day.

## What is true now

**2026-11-21 — FM-185-Q1 answered: the article is not tied to the edition.** By the Owner's answer, hail/1's next
edition is published without waiting for the article. The article is revised after that publication, on a day the Owner
chooses. Until that day is named, nothing is built for it, and FM-185 waits. On the day the edition is published, one
dated line at the top of the article says that it describes the first edition and that a revised article will follow; on
the coordinator's word, the publication's own sheet carries that line. When a day is named, a new ask is put on the
edition published then. The record is under *Asks*.

**Filed 2026-11-20, Proposed, with FM-185-Q1 put; nothing is built.** Read at main `77fa329`:

- **The article,** `shoalmark.tools/blog/hail-1.html`, is built from
  [`blog/posts/hail-1.md`](https://github.com/shoalmark/shoalmark/blob/77fa329ac6e005a55c6dfb42e1da4691e9b7caa1/blog/posts/hail-1.md), its example hails
  and its 16 figures with their alt text. [FM-153](FM-153-a-blog-for-the-site-and-its-first-post.md) built it, and is Shipped.
- **It follows the first edition.** Its source says the facts are "from the hail/1 spec, first edition"
  ([L15](https://github.com/shoalmark/shoalmark/blob/77fa329ac6e005a55c6dfb42e1da4691e9b7caa1/blog/posts/hail-1.md#L15)), and its two status lines say
  "First edition, not yet signed into force"
  ([L24](https://github.com/shoalmark/shoalmark/blob/77fa329ac6e005a55c6dfb42e1da4691e9b7caa1/blog/posts/hail-1.md#L24),
  [L43](https://github.com/shoalmark/shoalmark/blob/77fa329ac6e005a55c6dfb42e1da4691e9b7caa1/blog/posts/hail-1.md#L43)).
- **Both of shoalmark/hail's pages send readers to it:** its README
  ([L17](https://github.com/shoalmark/hail/blob/f5b160698a180481240dbff5c8cc605aaab06121/README.md#L17)) and its one page
  ([QUICKSTART L48](https://github.com/shoalmark/hail/blob/f5b160698a180481240dbff5c8cc605aaab06121/QUICKSTART.md#L48)), at main `f5b1606`, which publishes
  the first edition.

## Why

The article is where most readers meet hail/1, and both of hail's own pages send them there. If the next edition is
published while the article still describes the first, a reader meets two descriptions with no word between them.
Revised before the publication, the article and the edition say the same.

## Decisions, for the Owner

FM-185-Q1 asked for all of these at once. The Owner's answer, above, unties the article from the edition, so decision 6
reads as answered. The others are a proposal for the revision, put again in the new ask when a day is named.

1. **Every claim holds against the next edition.** Each claim of the article, its example hails and its figures' alt
   text is read against that edition's text, and is rewritten or cut where the text does not hold it. Each claim's
   section is recorded for the review.
2. **The status lines** name the edition, and say only what is true of the author's own teams on the day of the merge.
3. **The terms are the next edition's,** in the words, the example hails and the alt text. The example hails pass the
   check binary at that edition.
4. **The figures.** Alt text changes with the words. A figure whose drawn words change is an edit of its own source,
   by the tool team's Designer. A figure that would need a new drawing is listed, and comes to the coordinator before
   anyone draws it.
5. **Nothing else changes:** not the post's structure, its figures' order, or its look. A line that stays true stays as
   it is.
6. **Not tied to the publication** (the Owner's answer to FM-185-Q1). The next edition is published without waiting for
   the article; on that day, one dated line at its top says that it describes the first edition and that a revised
   article will follow. The revision comes after the publication, on a day the Owner names, and no branch is made
   before then.
7. **The review:** a reader on another model checks every claim against the edition's text. The Designer's check of the
   rendered page and of every changed figure sits beside it, never in its place.

## Done when

Each item names its commit or pull request when it lands.

- [x] **The Owner has answered the ask,** FM-185-Q1. · `07ca64d`, #321 (`c288d92`)
- [ ] **On the day the next edition is published,** one dated line at the top of the article says that it describes the
  first edition and that a revised article will follow.
- [ ] **A day is named** by a later signed answer, and a new ask is put on the edition published then.
- [ ] **Every claim** of the article, its example hails and its alt text holds against the next edition, each with its
  section, and the review is READY.
- [ ] **The figures:** each whose drawn words change is redrawn from its source, and the Designer's check of the
  rendered page is READY.
- [ ] **The revision lands:** the blog's tests and the build pass, its pull request's CI is green, and the Owner merges
  it.

## Asks

**FM-185-Q1** · 2026-11-21 · Is the hail/1 article revised for hail/1's next edition before that edition's publication, as FM-185's decisions set out, its branch local until the publication's sitting?
**answered** — accepted - The article is not tied to the edition. hail/1's next edition is published without waiting for the article. The article is revised after that publication, on a day I choose. Until I name that day, nothing is built for it and FM-185 waits. On the day the edition is published, one dated line at the top of the article says that it describes the first edition and that a revised article will follow. · holgo99
**relation** — accepted with a change
**signed** — 07ca64d · G

## Ship log

| Date | Event |
|---|---|
| 2026-11-21 | FM-185-Q1 cleared, with its record under *Asks*: the article is not tied to the edition, and is revised after the publication on a day the Owner names. The hook, decision 6 and *Done when* say so; `next: wait`, where the answer had set `build`. Records only. |
| 2026-11-20 | Filed, Proposed, with FM-185-Q1 put: the article revised before hail/1's next edition is published, its branch local until the publication's sitting. Records only. |
