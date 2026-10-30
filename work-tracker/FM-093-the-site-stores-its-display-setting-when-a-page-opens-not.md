---
id: FM-093
status: Proposed
considered: FM-091, FM-006
tags: bug
hook: "The site's theme stores the visitor's colour palette in their browser as soon as any docs page opens, not only when they use the switch. The Owner wants it stored only after the visitor's own switch, which is what they asked for."
---

# FM-093 — the site stores its display setting when a page opens, not only after the visitor switches it

## What is true now

**Filed 2026-10-29 for v0.20.3; nothing is built.** On the Owner's ruling of 29 October, as the Auditor relays it: the
display setting is saved only after a switch, never on a page's opening.

- **What the build does:** the theme's bundle mounts its palette component at startup, and the component's stream
  begins with the current scheme. So the palette key is written to `localStorage` when any docs page opens, and again
  on each switch. [FM-091](FM-091-the-site-has-no-imprint-and-no-privacy-notice-and-its.md)'s build found it.
- **What the privacy notice says:** FM-091's notice, section 3, says what the build does, in both languages.
- **The way:** a theme override or a small script of the site's own stores the key only after the visitor's switch. A
  page that opens reads a stored key, and writes none.

## Why

Storage on a visitor's device needs their consent unless it is strictly necessary for what they asked for. A setting
written only after they switch it is what they asked for.

## Done when

- [ ] Opening a built page writes nothing to the browser's storage. The visitor's switch writes the palette key, and a
  page opened after it reads the key.
- [ ] A browser check in CI holds both, with a mutant that writes on opening and is refused.
- [ ] The privacy notice's section 3 says the setting is saved only after a switch, in both languages, on the Owner's
  word.

## Ship log

| Date | Event |
|---|---|
| 2026-10-29 | Filed for v0.20.3, on the Owner's ruling of 29 October. Records only. |
