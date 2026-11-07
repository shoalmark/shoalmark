---
id: FM-154
status: Proposed
considered: FM-094, FM-153, FM-090
tags: bug
hook: "The blog's figures are written as HTML, and a page's Markdown twin keeps them with image paths one folder short, so an agent reading the twin finds no image. And the check that holds German prose to du reads docs/de/ one level deep, so the German blog is outside it."
---

# FM-154 — The Markdown twins lose the blog's figures, and the German du guard does not read the blog

## What is true now

**Filed 2026-11-08, before FM-153's pull request; nothing is built.** FM-153 builds the site's blog and its first
post, whose figures are HTML blocks. Its build, not yet committed, shows two gaps in tools the blog does not change.

- **The twins' figures:**
  - `scripts/llms_txt.py` writes a page's Markdown twin one folder deeper than the page: `blog/hail-1.md`'s twin
    stands at `blog/hail-1/index.md`.
  - It retargets Markdown links to other pages for that place, but not the image paths (`src`, `srcset`) of a figure
    written as HTML. So in the twin, `../assets/blog/hail-1/…` leads one folder short of the figures.
  - The twin also carries the figures as raw HTML, where How it works' figure is written as Markdown.
- **The German du guard:**
  - `test_shoalmark.py` reads German prose from `docs/de/*.md`, one level only. `docs/de/blog/` is outside it, so the
    German post and index are held neither to du nor to the retired terms.
  - Read with the guard's own patterns, the German post has four sentences that begin with "Sie" or "Ihr". Each
    refers back to a noun: none is formal address. It also has "Owner" five times, in quoted English.
  - A guard that reads the blog needs an allowed entry for each.

## Why

A reader of the twins should find what a reader of the site finds, figures included. The German blog is German prose
like every other page, and the same check should hold it.

**Held against** (`considered:`):
- [FM-094](FM-094-a-link-written-as-html-in-a-docs-page-does-not-lead-to-its.md) is not this work: it leads links
  written as HTML to their targets' twins. This is about the images an HTML figure loads, and the figure's form in the
  twin.
- [FM-153](FM-153-a-blog-for-the-site-and-its-first-post.md) is not this work: it builds the blog, and changes neither
  `llms_txt.py` nor the guard.
- [FM-090](FM-090-the-site-check-s-reading-of-markdown-has-edge-cases-no-page.md) is not this work: it collects
  `check_site.py`'s edge cases in reading Markdown. This is about the twins and a test's reach.

## Done when

- [ ] Each figure a docs page writes as HTML reads as Markdown in the page's twin, as How it works' figure does, and
  its image leads to the file from the twin's place; or the build refuses the page.
- [ ] The German du guard reads every German prose page under `docs/de/`, at any depth, with allowed entries only for
  what a page quotes in English or refers back to.
- [ ] A test holds both, with a mutant of each that is refused.

## Ship log

| Date | Event |
|---|---|
| 2026-11-08 | Filed, on the Auditor's word of 8 November, before FM-153's pull request. |
