# FM-006: B1, the landing in English and German: the release at e8ec559

Verdict: **READY WITH FINDINGS**. One P3, RV-2865, is fixed forward; there is no P1 and no P2. RV-2860 to RV-2864 are closed. RV-2866 to RV-2879 are unused.
Reviewed: e8ec559e550e340d4860e1e04c507fc17e918b6c, `git diff origin/main...e8ec559` (ceb21b8..e8ec559: 51 commits, 6 of them merges, 40 files). Tier: code; the diff names test_shoalmark.py, scripts/, zensical.toml and .github/workflows/docs.yml. shoalmark.py, ci.yml and gate.yml are unchanged.

## Reviewed by others, by sha
- **The figures, pins and docs.yml.** implementer-127's work is READY at c426698, critical tier, by reviewer-129 (9496d83, [its verdict](review-b1-facts-and-pins-c426698.md)). The merges 30427cf, 2615231 and 345bb08 each re-merge from their parents to the same tree. They bring 885c358, 7e39d20 and 9496d83 and nothing else, and the facts branch's own files are the same at e8ec559 as at 9496d83.
- **The records, by reviewer-121.** FM-045's move to Shipped and INDEX.md: READY WITH FINDINGS at 6bc37e8 (f5af671), its RV-2851 fixed in 47196ba. FM-032's two rulings, with that fix: READY at 9e37ea1 (467e860).
- **The three verdicts merged.** fe4024f brings PR 148's (6b299e6), 923d1e5 PR 150's (7d2b88a) and a86667f PR 151's (d486de5).
  - Fixed on this branch: RV-2810 at 2a87d52, RV-2811 at e9b07cf, RV-2755 at e727bdc, and RV-2750 by the release check of implementer-127's script. The comments of RV-2751 to RV-2753 were rewritten when the figures became generated.
  - RV-2754 (CHANGELOG.md) is outside this branch.

## What holds
- **Built as the Owner's revised word and the Planner's rulings give it:** one template with its words per language; the German landing, the language switch, `hreflang` and a link preview per language; §3.1–§3.3; How it works (So funktioniert's) in both languages; the dialog in three steps behind `probe`, the only switch, which is off; §13's header.
- **The held git lines are main's.** README.md, both setup pages and both start pages' beta lists are unchanged; How it works' git sentence stands on its own line.
- **facts.html's four additions render as ruled.** `hiscore_last` and `read.date_en`/`read.date_de` go in through the words' slots. `excerpt` gives its two counts and its act, the line printed once as the script escaped it. `counts` stands in the top bar's HTML. Built at e8ec559 today: 28 wrecks, 10 open, 76/91 to #156, and the excerpt as `--owner` prints it, dated 9 October 2026 (9. Oktober 2026).
- **Claims.** On both launch states' built pages and twins, "security" and "Sicherheit" stand only in ruling 7's line under the chart and in the negated line of *What shoalmark does not do*. "one person in charge" and "Standup" stay, and How it works says what ruling 11 allows.
- **German.** Every German string is go-to-market's row verbatim (rounds 1, 2, 2b and 2c), or the probe lane's hand-over byte for byte. Two have no row: the picture's card title *Tafel*, and the register's date range, which Intl writes. English on the German pages is marked `lang="en"`.
- **The records.** FM-006's new paragraph and ship-log row say only what holds at e8ec559; FM-045 and FM-032 are as reviewed.

## Findings
- **RV-2860 to RV-2864** (P3s at 9fbf185) are closed as given. e45fdd6 renders the excerpt, so the footer holds; 655c768 prints `counts`; bd2b696 corrects three comments and shows the anchors from 1130 px and 1196 px; a03b6a0 makes the start pages' twins follow the launch state.
- **RV-2865 · P3 · `overrides/landing.html:390`, `scripts/check_landing_browser.mjs:5–6` and `:133`.** These lines call 888/888 "the widest figure the bar can print" and "the widest hi-score the bar can print", but the hi-score's shape allows four digits a side once the counted range reaches 1,000 pull requests.
  - Fix: at :390, "the widest figure the bar can print, 888/888" → "the widest three-digit hi-score, 888/888"; in check_landing_browser.mjs, "the widest hi-score the bar can print" → "the widest three-digit hi-score".

## Commands: 2026-10-09, CEST, as `date` printed each
- **At e8ec559:** test_core all green (08:53:22–08:53:42); `--check` and `--session-check` exit 0 (to 08:53:55); test_check_site.py, 20 tests, OK (to 08:54:06); py_compile exit 0 (08:54:12).
- **run-one-check:** the landing's source check and its 12 controls (08:54:47–08:57:43), and the launch check and its controls (08:57:48–09:00:49), each exit 0.
- **The browser block under SHOALMARK_REGENERATE=1** (08:54:42–09:01:06), exit 0: the interim state 66 checks and the probe state 150, none failing. Its nine controls fail as named, and so do the excerpt check's two.
- **A clean export of e8ec559, built with the real script:** landing_facts.py, Zensical 0.0.67, llms_txt.py, check_site.py and `--check site`, each exit 0, interim (09:01:03–09:01:21) and probe (09:01:31–09:01:34). With the switch on the script stops at pins check 1, as built, so the probe build takes the switch-off figures, as the suite's builds do.
- **Before this commit:** `--check` and `--session-check` exit 0 (09:04:39–09:04:52).

Quality read: apart from RV-2865, the release reads clean.
