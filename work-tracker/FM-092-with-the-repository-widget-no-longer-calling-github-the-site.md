---
id: FM-092
status: Proposed
considered: FM-006, FM-002
tags: process
hook: "FM-091 stops the theme's repository widget from calling GitHub in every visitor's browser, so the site no longer shows the repository's stars, forks or latest version. Those numbers can come back, written into the page when the site is built, as the landing's facts are, and never fetched by a visitor."
---

# FM-092 — with the repository widget no longer calling GitHub, the site shows no star or fork count and no latest version

## What is true now

**Filed 2026-10-29 for v0.20.3; nothing is built.** On the Owner's word of 29 October, as the Auditor relays it:
"numbers written into the page at build time - with v0.20.3".

- **Why the numbers go:** FM-091, on main for the site's imprint and privacy notice, keeps the theme's repository link
  but drops its live widget. That widget called GitHub's API from each visitor's browser and sent their address to
  GitHub before they did anything. So the star and fork counts and the latest version go with it.
- **How they come back:** the build reads them once, as `scripts/landing_facts.py` reads the landing's facts, and
  writes them into the page. No visitor's browser fetches anything for them, and the privacy notice stays true.

## Why

The numbers say something true about the project, and a reader may look for them. Written at build time, they cost the
reader nothing and tell no one that the reader came.

## Done when

- [ ] The build writes the repository's stars, forks and latest version into the site's header, read once at build
  time.
- [ ] No built page loads anything from another host, and FM-091's site check holds that.
- [ ] Where the build cannot read them, offline for one, the page shows the link without numbers, and the build says
  so in one line.

## Ship log

| Date | Event |
|---|---|
| 2026-10-29 | Filed for v0.20.3, on the Owner's word of 29 October. Records only. |
