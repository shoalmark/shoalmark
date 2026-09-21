---
id: FM-002
status: Shipped
considered: FM-001
hook: "The board can carry a name in the browser tab and a theme.css — nothing else: no name on the page, no logo, English only. And several kinds of user want to brand it at once: several people looking at one repository's board, several repositories, an organisation shipping its house brand into every repository it sets up. One rule, three files, four places — to be proven before it is built."
---

# FM-002 — A board anyone can brand — the person, the repository, the organisation

## What is true now

**Shipped as 0.8.0 — merged by the Owner (#1) after the R&D; the origin's board wears its real brand from it.** Three optional files (`theme.css`, `logo.svg`,
`labels.yaml`) in three places plus the defaults — the vendored tool's `brand/`, beside the trackers, the person's
`~/.config/shoalmark/` — the later one winning, and **no setting**. Nine of eleven pre-registered claims held
outright, on the origin's real logo, brand tokens and fonts and on a German copy of the first client's board; one was
false as first built and fixed (a theme whose import is missing); the core grew more than its bar allowed. The
record, with what was found that nobody had named: [the R&D file](evidence/FM-002/brand-layers-rd.md).

## Why

The first client's staff read German. The origin has a brand. A consultancy setting a repository up for a client
wants its mark on it until the client's replaces it. And two people committing to one repository must never fight
over a generated file because their boards look different.

## Done when

Every pre-registered claim has an outcome under its forecast; the Owner has ruled on the merge; on merge, the
README explains the whole feature in one section of at most 25 lines.

## Ship log

| Date | Event |
|---|---|
| 2026-09-21 | **Merged (#1), released as 0.8.0.** First real use: the origin — an 8-line theme importing its brand tokens, its micro mark linked, two labels; looked at in a browser there in both schemes. The German labels wait for the first client's repository. |
| 2026-09-21 | Spiked on `rd/fm-002-brand-layers`: 9 of 11 claims held outright; 90 + 144 checks green on Python 3.14 and 3.9; the outcome is under the pre-registration. Not merged. |
| 2026-09-21 | Filed; the pre-registration committed before the spike. |
