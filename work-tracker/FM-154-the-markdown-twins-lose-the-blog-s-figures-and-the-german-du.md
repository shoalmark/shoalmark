---
id: FM-154
status: Proposed
considered: FM-094, FM-153, FM-090
tags: bug
next: owner
hook: "The blog's figures are written as HTML, and a page's Markdown twin keeps them with image paths one folder short, so an agent reading the twin finds no image. And the check that holds German prose to du reads docs/de/ one level deep, so the German blog is outside it."
ask-id: FM-154-Q1
ask: "Shall FM-154 be built as its Done when says, with llms.txt naming a page whose title is written as HTML by its front matter title, so that the blog's first post is no longer listed by its file name?"
ask-kind: ruling
ask-since: 2026-11-08
ask-options: "yes, as proposed | the twins and the guard only: llms.txt's names wait | no"
ask-proposal: "yes, as proposed"
---

# FM-154 — The Markdown twins lose the blog's figures, and the German du guard does not read the blog

## What is true now

**Filed 2026-11-08, before FM-153's pull request; nothing is built, and FM-154 waits for the Owner's ruling,
FM-154-Q1.** FM-153 builds the site's blog and its first post, whose title and figures are HTML blocks. Its build
shows three gaps in tools the blog does not change.

- **The twins' figures:**
  - `scripts/llms_txt.py` writes a page's Markdown twin one folder deeper than the page: `blog/hail-1.md`'s twin
    stands at `blog/hail-1/index.md`.
  - It retargets Markdown links to other pages for that place, but not the image paths (`src`, `srcset`) of a figure
    written as HTML. So in the twin, `../assets/blog/hail-1/…` leads one folder short of the figures.
  - The twin also carries the figures as raw HTML, where How it works' figure is written as Markdown.
- **The names in `llms.txt`:**
  - `scripts/llms_txt.py` names each page by its first `# ` line, or by its file name where it has none.
  - The first post writes its title as an HTML `h1`, so `llms.txt` lists it as `hail-1`, in both languages.
  - Its front matter's `title:` holds the title. Taking that title where a page has no `# ` line names the two
    posts, and no other page's name changes.
- **The German du guard:**
  - `test_shoalmark.py` reads German prose from `docs/de/*.md`, one level only. `docs/de/blog/` is outside it, so the
    German post and index are held neither to du nor to the retired terms.
  - Read with the guard's own patterns, the German post has one sentence that begins with "Ihre", in its opening
    paragraph and in the description drawn from it. It refers back to the agents: it is not formal address. The post
    also has "Owner" six times, each in English: quoted in its prose, twice in F13's alt text, and in a hail.
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
- [ ] `llms.txt` names a page whose title is written as HTML by its front matter's `title:`, and every other page as
  before.
- [ ] A test holds each, with a mutant of each that is refused.

## Ship log

| Date | Event |
|---|---|
| 2026-11-08 | Asked the Owner: FM-154-Q1, whether to build FM-154 as its Done when says, with llms.txt naming a page whose title is HTML by its front matter's title. |
| 2026-11-08 | Filed, on the Auditor's word of 8 November, before FM-153's pull request. |
