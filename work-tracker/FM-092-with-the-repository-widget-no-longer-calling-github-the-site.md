---
id: FM-092
status: Proposed
considered: FM-006, FM-002
tags: process
hook: "Since v0.20.1, tagged on 23 October, the theme's repository widget calls no one, so the site shows no star or fork count and no latest version. Those numbers can come back, written into the page when the site is built, as the landing's facts are, and never fetched by a visitor."
---

# FM-092 — with the repository widget no longer calling GitHub, the site shows no star or fork count and no latest version

## What is true now

**Filed 2026-10-29 for v0.20.3; nothing is built.** On the Owner's word of 29 October, as the Auditor relays it:
"numbers written into the page at build time - with v0.20.3".

- **Why the numbers went:** 2ecdc16, of 9 October, draws the theme's repository link without its live component, so no
  visitor's browser calls GitHub's API. The site has carried it since v0.20.1, tagged on 23 October, the first release
  that holds it, and the star and fork counts and the latest version went with it. FM-091, merged into main by #242,
  holds that with its site check.
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
| 2026-10-29 | The hook and the first bullet date the widget's end to v0.20.1, tagged on 23 October, the first release to carry 2ecdc16 (RV-4055). Records only. |
| 2026-10-29 | The hook and the first bullet say the widget has called no one since 2ecdc16, which FM-091's site check holds (RV-4036). Records only. |
| 2026-10-29 | The hook and the first bullet say FM-091 is not merged yet (RV-3993). Records only. |
| 2026-10-29 | Filed for v0.20.3, on the Owner's word of 29 October. Records only. |
