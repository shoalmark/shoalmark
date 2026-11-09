---
id: FM-153
status: Shipped
considered: FM-143, FM-152
next: build
triaged: 2026-11-08
tier: P2
hook: "The site has no place for posts, and its first post needs one in both languages, with animated figures that stay small, and still for readers who turn motion off."
---

# FM-153 — A blog for the site, and its first post

## What is true now

**2026-11-09 — Shipped: merged to main as #280 (`cd76d0a`), and live.** The blog stands at `shoalmark.tools/blog/`: its
index, opened by one statement, with the newest post leading, and its first post, on hail/1's first edition and dated
2026-11-09.

- **The review:** a standard review and eleven bounded re-checks, one verdict each, the last READY at `f34f311`. The
  twelve verdicts join the records with this change. The Designer checked each revision's built pages beside them, as
  recorded privately.
- **Live:** a request for the post's MP4 with `Range: bytes=0-99` answers 206 with `Content-Range`, from the Worker.
- **The share preview:** the Owner checked it in iMessage on 9 November, and it shows the post's video. Every Done
  when item is met.

**2026-11-08 — the blog is built under FM-153-Q3's answer, and its first post's authors wait for the Owner's
ruling, FM-153-Q4.** The blog, its first post and the Blog button are built on a branch from main, not merged.
FM-153-Q4 asks whether the post names the Owner among its authors:

- **The Owner first:** under the Owner's X account, linked, with the Owner's portrait in a round frame.
- **Then the six seats:** Go-to-market, Designer, Planner, Builder, Reviewer and Auditor, each with its icon from
  [`brand/seats/`](../brand/seats/) and a one-line role. Research is thanked, not listed.
- **Where:** in the post's head, under the reading time, and again at its end as "Written by".
- **Until its answer,** no commit that names the Owner's account or carries the portrait is pushed. The rest of the
  build goes on under FM-153-Q3's answer.

**2026-11-08 — the blog is to leave the docs site, and FM-153 waits for the Owner's ruling, FM-153-Q3.** The blog
and its first post were built inside the docs site, under FM-153-Q2's answer, on `planner/blog-build`. It is not
merged, and no pull request is open. FM-153-Q3 asks for another plan:

- **Its own site:** `shoalmark.tools/blog/`, built in the same job as the docs and deployed with them, by a small
  builder of the repository's own, with its own templates and CSS and no docs engine. The docs engine builds the docs
  only.
- **English only:** no German index and no German post.
- **Dark-first,** like the figures and the board.
- **The start page:** no line under the hero. Blog becomes a button in the start page's header and in the docs'
  header, in both languages, leading to the English blog.
- **What carries over:** the first post's English words and its figures, from the checked folder (recorded
  privately), and the figure checks.
- **No build commit lands under this plan before its answer:** FM-153-Q2's answer covered the blog inside the docs
  (FM-033).

**2026-11-08 — judged before its first build commit: keep P2, In Progress.** A partial triage pass, on the Owner's
signed answer to FM-153-Q2 (`aa19b0c`), judged this row alone ([worksheet](evidence/triage/triage-2026-11-08.md)).
Unranked. The build follows on a branch from main, reviewed with the Designer's check beside the review.

**2026-11-08 — the site has no blog, and FM-153 waits for the Owner's ruling, FM-153-Q2.** No work outside this
tracker is committed under it before the answer: a pass judges before the first build commit (FM-033), and a signed
answer authorises the work.

- **Built, not committed:** a blog index in English and German, each in its language's nav, the first post,
  and a check that holds every figure to its alt text, its still and 1,000,000 bytes.
- **The first post:** its words and figures come from a checked folder, recorded privately.
- **Not built yet:** one line on each language's start page, linking straight to the post. FM-153-Q2 adds it to
  FM-153-Q1's question, which is withdrawn unanswered.
- **After a yes:** a triage pass judges FM-153, then the work is committed, reviewed with the Designer's check beside
  the review, and run by CI.

## Why

The site has nowhere to put a post. Its first post needs a page in each language, and figures that stay small, and
still for readers who turn motion off.

**Held against** (`considered:`):
- [FM-143](FM-143-installing-two-skills-clones-all-of-shoalmark.md) is not this work: it moves the two skills into
  their own repository and gives them a Skills page, and builds no place for posts.
- [FM-152](FM-152-an-x-post-image-the-agents-never-answer-for-you-the-software.md) is not this work: it is an X post
  image for the Owner to judge, kept in its evidence, and puts nothing on the site.

## Done when

- [x] The blog at `shoalmark.tools/blog/`, with its index: built by the repository's own builder, with its own
  templates and CSS and no docs engine, in the same job as the site and deployed with it.
  · `246e8f9`, `f61814e`, `411a0cb`, merged in `cd76d0a`
- [x] Dark-first.
  · `246e8f9`
- [x] The first post, every word and figure from the checked folder.
  · `d1400f9`, `49022d6`, `65108f3`
- [x] The first post's head carries its share video (`og:video`) and a matching social card.
  · `4221152`, `52f6cf7`
- [x] The first post lists its authors as FM-153-Q4's answer rules, the six seats with their icons among them.
  · `0fd16fc`
- [x] The post's spec link points at the published spec.
  · `1eeaff1`, `65108f3`
- [x] A Blog button in the start page's header and in the docs' header, in both languages, leading to the English
  blog. No line under the start page's hero.
  · `631d2fd`, `af74799`
- [x] Every figure with alt text and a still, and each at most 1,000,000 bytes, held by a check that runs in the
  site's build.
  · `9461fd3`, `b5f8eea`, `3760593`
- [x] `docs.yml`'s build passes on the pull request.
  · #280's docs run, 9 November
- [x] A standard review's READY, with the Designer's check of the rendered pages beside it.
  · READY at `f34f311`; the Designer's check as recorded privately
- [x] After the deploy, a request for the post's MP4 with `Range: bytes=0-99` answers 206 with `Content-Range`.
  · checked on `shoalmark.tools`, 9 November
- [x] The Owner's check of the post's share preview in iMessage.
  · the Owner, 9 November, on the Auditor's word

## Asks

**FM-153-Q1** · 2026-11-08 · Shall FM-153 build a blog for shoalmark's site, an index in English and German in each language's nav, and its first post, the article whose checked words and figures the Auditor holds (recorded privately), ready to merge on 8 November?
**withdrawn** — no answer was given

**FM-153-Q2** · 2026-11-08 · Shall FM-153 build a blog for shoalmark's site, an index in English and German in each language's nav, and its first post, the article whose checked words and figures the Auditor holds (recorded privately), linked from each language's start page?
**answered** — accepted - yes, as proposed · holgo99
**relation** — accepted the proposal
**signed** — aa19b0c · G

**FM-153-Q3** · 2026-11-08 · Shall FM-153 build the blog as its own English site at shoalmark.tools/blog/, built and deployed with the site by the repository's own builder, dark-first and with no docs engine, with its first post, and a Blog button in the start page's and the docs' header instead of FM-153-Q2's start-page line?
**answered** — accepted - yes, as proposed · holgo99
**relation** — accepted the proposal
**signed** — d3333fa · G

**FM-153-Q4** · 2026-11-08 · Shall FM-153's first post list the Owner among its authors, under the Owner's X account with a link to it and with the Owner's portrait, before the six seats with their icons, in the post's head and again at its end, as FM-153's *What is true now* entry on the first post's authors sets it out?
**answered** — accepted - yes, as proposed · holgo99
**relation** — accepted the proposal
**signed** — d0bb49f · G

## Ship log

| Date | Event |
|---|---|
| 2026-11-09 | Shipped: the Owner checked the post's share preview in iMessage, and every Done when item is met. |
| 2026-11-09 | Merged to main as #280 (cd76d0a), and live: the blog, its index and its first post; FM-153-Q4 cleared, its record under Asks; the review's twelve verdicts join the records; the Owner's share-preview check is open. |
| 2026-11-08 | Asked the Owner again: FM-153-Q4, the Owner among the first post's authors, under the Owner's X account and with the Owner's portrait; FM-153-Q3 cleared, its record under Asks. |
| 2026-11-08 | Asked the Owner again: FM-153-Q3, the blog as its own English site at shoalmark.tools/blog/, dark-first, with a Blog button in the start page's and the docs' header; FM-153-Q2 cleared, its record under Asks. |
| 2026-11-08 | Judged keep P2 by a partial triage pass on the Owner's signed answer to FM-153-Q2 (aa19b0c); In Progress. Records only. |
| 2026-11-08 | RV-4425 and RV-4426 fixed forward, from #275's verdict: FM-153 was filed In Progress with next: build on 2026-11-07, before any pass judged it, and set back to Proposed with next: owner when FM-153-Q1 was asked, the same day, with nothing outside the records committed under it; What is true now lists the first post as built, not an empty one. |
| 2026-11-08 | Done when: the start-page line also goes where the site renders the start page, its landing template and partials. |
| 2026-11-08 | Asked the Owner again: FM-153-Q2 adds a line on each start page linking to the post; FM-153-Q1 withdrawn unanswered. |
| 2026-11-07 | Asked the Owner: FM-153-Q1, a ruling on building the blog and its first post. |
| 2026-11-07 | Filed. |
