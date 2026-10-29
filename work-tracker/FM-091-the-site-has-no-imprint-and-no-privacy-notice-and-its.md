---
id: FM-091
status: In Progress
considered: FM-006, FM-019, FM-051
tags: process
next: build
triaged: 2026-10-29
tier: P2
hook: "The site has no imprint and no privacy notice, though a German provider must have both, easy to find from every page. And the theme's repository widget calls GitHub's API from every visitor's browser, sending their address to GitHub before they do anything."
---

# FM-091 — the site has no imprint and no privacy notice, and its repository widget calls GitHub from every visitor's browser

## What is true now

**Filed 2026-10-29, and judged In Progress, P2, before the first build commit,** on the Owner's word of 29 October:
"bring those in now", on main, as with the landing page's update: a branch, the merge to main, and a deploy.
[FM-006](FM-006-shoalmark-has-one-document-written-for-agents-the-humans-who.md) ships at v0.20.2 and takes no more
work, so this is a tracker of its own.

- **The pages:** `imprint` and `privacy` in English, `de/impressum` and `de/datenschutz` in German. Their words follow
  the Owner's own pages of another project, with that project's specifics changed to shoalmark's. The German pages
  speak to the reader as *Sie*, as main's German pages do until v0.20.2's German rewrite reaches them.
- **The contacts:** `legal@shoalmark.tools` for the imprint and `privacy@shoalmark.tools` for the privacy notice, as
  plain `mailto:` links.
- **Every page links both legal pages of its language in its footer.**
- **The repository widget keeps its link but stops calling GitHub:** no element carries `data-md-component="source"`,
  so no browser calls `api.github.com` and nothing is written to `sessionStorage`. The live star and fork counts go.
- **The site check, class-wide:**
  - every built page links its language's imprint and privacy page;
  - no built page carries the source component;
  - no built page loads a script, stylesheet, font, image or frame from another host.
- **Out of scope:** no other word of the existing pages changes, and no analytics or consent banner is added.

## Why

The imprint and the privacy notice are owed to every visitor, and the site must also do what its privacy notice says.
A widget that sends each visitor's address to a third party before they act is one thing the notice would otherwise
have to explain.

## Done when

- [ ] The four pages are built and linked from every page's footer, each language to its own.
- [ ] No built page carries `data-md-component="source"`, and no browser of a visitor calls GitHub's API.
- [ ] The site check refuses a page without both footer links, a page with the source component, and a page that loads
  anything from another host. A mutant of each is refused.
- [ ] The Owner has given the word on the four final texts, and on both addresses delivering.
- [ ] The pages are live on shoalmark.tools after a deploy of main.

## Ship log

| Date | Event |
|---|---|
| 2026-10-29 | Filed, and judged In Progress, P2, before the first build commit, on the Owner's word of 29 October. Records only. |
