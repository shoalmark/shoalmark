---
id: FM-091
status: In Progress
considered: FM-006, FM-019, FM-051
tags: process
next: build
triaged: 2026-10-29
tier: P2
hook: "The site has no imprint and no privacy notice, though a German provider must have both, easy to find from every page. And nothing checks that the site keeps to what such a notice says: that no page loads anything from another host, and that the theme's repository widget, which once called GitHub from every visitor's browser, stays off."
---

# FM-091 — the site has no imprint and no privacy notice, and its check does not hold the site to what such a notice says

## What is true now

**2026-10-29 — the texts take the Owner's rulings, both addresses deliver, and two findings move to v0.20.3.** On the
Owner's rulings of 29 October, as the Auditor relays them, db88e34 sets the four texts:
- **Email:** the privacy notice gains a section on contact by email, in categories only.
- **Licence:** the imprint's copyright section gives way to the licence, Apache-2.0 or MIT at the reader's option.
- **GitHub Pages:** it redirects the site's former address to shoalmark.tools. GitHub stays named as a recipient, as a
  controller in its own right.
- **The right to object:** a paragraph of its own.
- **The addresses:** both deliver, on the Owner's word.
- **The display setting:** the theme writes it when a page opens, not only after a switch. The notice says what the
  build does. In v0.20.3, [FM-093](FM-093-the-site-stores-its-display-setting-when-a-page-opens-not.md) makes it
  wait for the switch.
- **The language links:** the Designer's BF-103 asks them to carry `hreflang` and `lang`, which takes HTML links, and
  the llms twins then lose them. They are Markdown again. In v0.20.3,
  [FM-094](FM-094-a-link-written-as-html-in-a-docs-page-does-not-lead-to-its.md) takes both.
- **A second contact channel** in the imprint is not filed. The Owner decides it later.
- **A correction:** this tracker's filing said the theme's repository widget calls GitHub from every visitor's browser.
  It has called no one since 2ecdc16, on 9 October. This lane's site check holds that now, and the hook, the title and
  the bullet below say so.

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
- **The repository widget keeps its link and calls no one:** no element has carried `data-md-component="source"` since
  2ecdc16, so no browser calls `api.github.com` and nothing is written to `sessionStorage`. The site check holds that.
- **The site check, class-wide:**
  - every built page links its language's imprint and privacy page;
  - no built page carries the source component;
  - no built page loads a script, stylesheet, font, image or frame from another host.
- **Out of scope:** no other word of the existing pages changes, and no analytics or consent banner is added.

## Why

The imprint and the privacy notice are owed to every visitor, and the site must also do what its privacy notice says.
A widget that sent each visitor's address to a third party before they acted, as the theme's once did, is one thing the
notice would otherwise have to explain.

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
| 2026-10-29 | The texts take the Owner's rulings (db88e34), and both addresses deliver. The hook and title are corrected: the widget has called no one since 9 October. FM-093 and FM-094 are filed for v0.20.3. Records only. |
