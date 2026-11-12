---
id: FM-149
status: Proposed
considered: FM-062, FM-100, FM-104, FM-143
tags: process
epic: FM-139
next: build
hook: "shoalmark speaks English and German, but no one rule says which texts ship with a German twin, which words never translate, or what language a skill's report is in; the Skills page and the skills' German README need one now."
ask-id: FM-149-Q1
ask: "Are FM-149's decisions taken, as its section Decisions, for the Owner sets out?"
ask-kind: ruling
ask-since: 2026-11-04
ask-options: "yes, as proposed | yes, with the changes I name"
ask-proposal: "yes, as proposed"
answer: "accepted - yes, as proposed"
answered: 2026-11-04
answered-by: holgo99
---

# FM-149 — the docs, the Board's prompts and the skills have no one rule for English and German

## What is true now

**2026-11-04 — filed, Proposed, on the Auditor's brief; nothing is built.** Its one ask, FM-149-Q1, takes every
decision under *Decisions, for the Owner* at once.

1. **The docs:** each page in the nav's English section has a German twin under
   [`docs/de/`](https://github.com/shoalmark/shoalmark/tree/c02ca26ffdf8fa24781a4943148725880552703f/docs/de), except
   [the seats page](https://github.com/shoalmark/shoalmark/blob/c02ca26ffdf8fa24781a4943148725880552703f/docs/seats/index.md)
   and the agents' contract
   ([`zensical.toml` L15–L36](https://github.com/shoalmark/shoalmark/blob/c02ca26ffdf8fa24781a4943148725880552703f/zensical.toml#L15-L36)).
   - The German prose speaks as "du". A guard holds it there
     ([`test_shoalmark.py` L10800](https://github.com/shoalmark/shoalmark/blob/c02ca26ffdf8fa24781a4943148725880552703f/test_shoalmark.py#L10800)).
   - No check compares a twin pair's structure. `ADOPT.md` and `ADOPT.de.md` are compared only on their pin line
     ([`test_shoalmark.py` L18980](https://github.com/shoalmark/shoalmark/blob/c02ca26ffdf8fa24781a4943148725880552703f/test_shoalmark.py#L18980)).
2. **The Board:** its words come from `labels.yaml`, and a German Board is that file, with `lang: de`
   ([README L679](https://github.com/shoalmark/shoalmark/blob/c02ca26ffdf8fa24781a4943148725880552703f/README.md#L679),
   [`examples/de/labels.yaml` L3](https://github.com/shoalmark/shoalmark/blob/c02ca26ffdf8fa24781a4943148725880552703f/examples/de/labels.yaml#L3)).
   The repository's place for it is `<tracker dir>/brand/`
   ([README L331](https://github.com/shoalmark/shoalmark/blob/c02ca26ffdf8fa24781a4943148725880552703f/README.md#L331)).
   `shoalmark.toml` holds no language, only the gate's `[headings]`.
3. **The prompts the Board hands over:** the stand-up prompt is code, and English on every Board. FM-100 moves it into
   the pack as `STAND-UP.md`, and leaves open whether the close-out prompt takes the same form
   ([FM-100 L31](https://github.com/shoalmark/shoalmark/blob/c02ca26ffdf8fa24781a4943148725880552703f/work-tracker/FM-100-the-stand-up-prompt-is-code-and-english-on-every-board-while.md#L31)).
4. **The skills:** both SKILL.md files and the README of
   [shoalmark/skills](https://github.com/shoalmark/skills/tree/06784be51991cd4d6accc20bb3cdfd5cdd577476) are English
   only, and neither skill says what language its report is in.

**2026-11-12 — [FM-100](FM-100-the-stand-up-prompt-is-code-and-english-on-every-board-while.md)'s ask, FM-100-Q1, proposes to supersede decision 3.** The
close-out would become two skills, `closeout` and `closeout-teams`, in place of `CLOSE-OUT.md`. Decision 3 stands until
that answer.

**2026-11-05 — placed in v0.20.3** at its allocation sitting, on the Owner's word. It stays a chapter of
[FM-139](FM-139-v0-20-3-s-rows-sit-in-fm-023-fm-006-and-fm-053-so-no-one.md), v0.20.3's epic.

## Why

shoalmark ships in two languages, and its next texts reach people in both: the Skills page, the skills' German README
and their reports. Without one rule, each change decides alone what gets a German twin and which words stay as written,
and no check can hold a rule that was never set.

## Decisions, for the Owner

FM-149-Q1 asks for all of these at once. An answer of "yes, with the changes I name" names each change by its number.

1. **English source, German twin.**
   - English is the source and the fallback.
   - Every text a person reads ships with its German twin in the same change: the docs pages, the Board, the prompts
     the Board hands over, and the skills' reports (as decision 2 sets out). The German voice is "du", and "Board"
     stays "Board".
   - Identifiers never translate: `/find-drift` and `/prune-drift`, file names, front-matter keys, trailers, report
     section keys, tracker ids.
   - A test checks that each pair agrees: the headings, the code blocks byte for byte, and the install commands.
2. **The skills: one source, the report in the person's language.**
   - SKILL.md stays one English source, so there is one test and one eval, and nothing for two copies to drift apart.
   - The report's prose and the conversation follow the person's language: the Board's language, `lang` in the
     repository's `<tracker dir>/brand/labels.yaml`, where that file sets `lang`; else the language the person writes
     in. A `lang` that fails shoalmark's own check counts as not set. A skill reads only the repository, never the
     person's home folder.
   - The section keys prune-drift reads from find-drift's report, and the file names, stay fixed.
   - **A limit:** the Board reads `labels.yaml` in three places, the later winning: the vendored copy's `brand/`, the
     repository's `<tracker dir>/brand/`, and the person's `~/.config/shoalmark/`
     ([README L658–L661](https://github.com/shoalmark/shoalmark/blob/c02ca26ffdf8fa24781a4943148725880552703f/README.md#L658-L661)). A skill reads only the second.
     Where the repository's file sets no `lang` and the vendored copy's does, or where the person's sets one, the Board
     can show another language than the skill's report.
3. **The close-out prompt takes the stand-up prompt's form:** `CLOSE-OUT.md` beside FM-100's `STAND-UP.md`.
   - It is in the pack's language, with English as the fallback.
   - It is the person's own file, changed only by their signed commit; the gate refuses a seat's change.
   - Where both files live still waits on
     [FM-104](FM-104-the-person-s-own-files-are-spread-over-the-repository-and.md), which ranks first when v0.20.3
     starts ([FM-139 L26](https://github.com/shoalmark/shoalmark/blob/c02ca26ffdf8fa24781a4943148725880552703f/work-tracker/FM-139-v0-20-3-s-rows-sit-in-fm-023-fm-006-and-fm-053-so-no-one.md#L26)).
4. **The path to shoalmark is on the page, not in the output.**
   - The Skills page and the skills' README end with the way to shoalmark ([*Why shoalmark?*](https://github.com/shoalmark/shoalmark/blob/c02ca26ffdf8fa24781a4943148725880552703f/docs/why-shoalmark.md),
     [the setup](https://github.com/shoalmark/shoalmark/blob/c02ca26ffdf8fa24781a4943148725880552703f/docs/setup.md)) and a link to
     [the feedback form](https://github.com/shoalmark/shoalmark/blob/c02ca26ffdf8fa24781a4943148725880552703f/docs/feedback/index.html).
   - The skills' own output carries no promotion.

## Done when

Each item names its commit or pull request when it lands.

- [x] **The Owner has answered FM-149-Q1.** · `32cb089`, #263 (`7f0136e`)
- [ ] **Every docs page a person reads has its German twin,** the seats page included, and a test checks each pair as
  decision 1 says.
- [ ] **The skills follow decision 2:** the report's language, the fixed section keys, and a test that pins the keys
  in both skills.
- [ ] **The skills' README has its German twin,** with the same pair check, and it ends as decision 4 says.
- [ ] **The Skills page, in English and German** (FM-143), ends as decision 4 says.
- [ ] **FM-100 carries decision 3** into its design, once FM-104 has placed the person's files.

## Ship log

| Date | Event |
|---|---|
| 2026-11-12 | FM-100-Q1 proposes to supersede decision 3, the close-out as two skills in place of `CLOSE-OUT.md`. Records only. |
| 2026-11-05 | Placed in v0.20.3 at its allocation sitting, on the Owner's word. Records only. |
| 2026-11-04 | `epic: FM-139`: under v0.20.3's epic until the Owner decides whether it goes in. Records only. |
| 2026-11-04 | Done when: the Owner's answer to FM-149-Q1 (#263). Records only. |
| 2026-11-04 | Filed, Proposed, with one ruling ask, FM-149-Q1, on the Auditor's brief. Nothing is built. |
