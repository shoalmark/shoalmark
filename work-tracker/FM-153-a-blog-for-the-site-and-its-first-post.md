---
id: FM-153
status: Proposed
considered: FM-143, FM-152
next: build
hook: "The site has no place for posts, and its first post needs one in both languages, with animated figures that stay small, and still for readers who turn motion off."
ask-id: FM-153-Q2
ask: "Shall FM-153 build a blog for shoalmark's site, an index in English and German in each language's nav, and its first post, the article whose checked words and figures the Auditor holds (recorded privately), linked from each language's start page?"
ask-kind: ruling
ask-since: 2026-11-08
ask-options: "yes, as proposed | the blog only: the first post waits | no"
ask-proposal: "yes, as proposed"
answer: "accepted - yes, as proposed"
answered: 2026-11-08
answered-by: holgo99
---

# FM-153 — A blog for the site, and its first post

## What is true now

**2026-11-08 — the site has no blog, and FM-153 waits for the Owner's ruling, FM-153-Q2.** No work outside this
tracker is committed under it before the answer: a pass judges before the first build commit (FM-033), and a signed
answer authorises the work.

- **Built, not committed:** a blog index in English and German, each in its language's nav, an empty first post,
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

- [ ] A blog index in English and German, each in its language's nav.
- [ ] The first post in English and German, every word and figure from the checked folder.
- [ ] One line on the start page in each language, linking straight to the post, in the same pull request as the
  post. It goes where the site renders the start page (`overrides/landing.html`,
  `overrides/partials/landing/en.html`, `overrides/partials/landing/de.html`) and into the start page's source
  (`docs/index.md`, `docs/de/index.md`).
- [ ] Every figure with alt text and a still, and each at most 1,000,000 bytes, held by `check_site.py`.
- [ ] The German page says in one line that the figures carry English labels.
- [ ] `docs.yml`'s build passes on the pull request.
- [ ] A standard review's READY, with the Designer's check of the rendered page beside it.

## Asks

**FM-153-Q1** · 2026-11-08 · Shall FM-153 build a blog for shoalmark's site, an index in English and German in each language's nav, and its first post, the article whose checked words and figures the Auditor holds (recorded privately), ready to merge on 8 November?
**withdrawn** — no answer was given

## Ship log

| Date | Event |
|---|---|
| 2026-11-08 | Done when: the start-page line also goes where the site renders the start page, its landing template and partials. |
| 2026-11-08 | Asked the Owner again: FM-153-Q2 adds a line on each start page linking to the post; FM-153-Q1 withdrawn unanswered. |
| 2026-11-07 | Asked the Owner: FM-153-Q1, a ruling on building the blog and its first post. |
| 2026-11-07 | Filed. |
