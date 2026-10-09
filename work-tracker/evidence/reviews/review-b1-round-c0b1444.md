# FM-006: B1's round of 2026-10-09, the review at c0b1444

Verdict: **READY WITH FINDINGS**. One P3, RV-2910, is fixed forward; there is no P1 and no P2. RV-2865 is closed. RV-2911 to RV-2919 are unused.
Reviewed: c0b1444bddcdc2da4229129ae5d7ce0d4a2925bc, `git diff 86b2ee8 c0b1444`. The scope is eight commits by implementer-126: 765f8f5, b6add63, 5c3449a, 12a0897, 95a472c, 0f83093, 3c0f4ff and the records commit. Tier: code, since the diff names test_shoalmark.py and scripts/. shoalmark.py, ci.yml, gate.yml and docs.yml are unchanged.

## What holds
- **The dialog, the box.** The prompt stands in step 1 under Copy again, in the first design's box with its label and tag. Closed, it shows two lines and a fade that takes no pointer and stays clear of the button. Show all (Alles anzeigen) is a real button with `aria-expanded` and `aria-controls`; Enter opens the box and Space folds it.
- **The dialog, opened.** Opened by Show all or by a failed copy, the box grows to the window, keeps its three-line floor and follows a resize. On a turned phone (844×390) it sits at its floor while the dialog scrolls, and it is 273 px again when the phone turns back.
- **The dialog, copying.** A failed copy selects the whole text and focuses it. Every way of copying it — the button, Copy again, Ctrl+C on the whole selection — gives probe.txt's bytes: the prompt's own line ending, with no empty line after it. Steps 2 and 3, the approvals fold and every other word are as they were, except where the Owner's words name them.
- **The words.**
  - Each changed line is the Owner's text, word for word, in its file's markup: *draft* (*Entwurf*); step 2's address, taken from the link's own `href`; the git lines 1–9 and README:40 as item 6 rules them; "of its own" in all six places.
  - The German queue clause is 0f83093's, which the Owner accepted. The withdrawn opening sentence and ADOPT's lines stay out.
- **The cue.** 3c0f4ff is the approved round-5 patch applied to 0f83093, byte for byte.
  - Only the cue's icon and words animate: four blinks of 1 s, then lit. Under reduced motion the page has no animation.
  - All three icons and the strip are `aria-hidden`, and the buttons' and labels' names are unchanged. The joystick and the coin show in both states.
  - The strip is as wide as Copy the prompt and centred on it, or over the stacked buttons on a phone. Its nearest chart label is 28 px away (German, 1440 px), and nothing scrolls sideways.
- **The texts and the records.** The comments, check names and commit messages claim what holds, and their control counts match the code. FM-006's paragraph says what the branch holds and the Owner's ruling that B1 goes live with the probe switch on; it names no unfixed item.

## Findings
- **RV-2865 · P3** (the verdict at e8ec559): closed in 765f8f5 as asked. "the widest three-digit hi-score" stands at `overrides/landing.html:400` and in check_landing_browser.mjs.
- **RV-2910 · P3 · FM-006's ship-log row of this round (line 905).** The row restates the seven commits, each with what it does, almost word for word as *What is true now* gives them, so the record carries the same list twice.
  - Fix: replace the row's text from "`765f8f5` the prompt stands" through "…on the players and start labels." with "`765f8f5`…`3c0f4ff`, seven commits named in *What is true now*; RV-2865 is fixed in `765f8f5`." Keep its last two sentences.

## Controls and commands: 2026-10-09, CEST, as `date` printed each
- **At c0b1444:** py_compile under 3.14 and 3.9.6 (15:54:20–15:54:22); test_core all green (to 15:54:41); `--check` and `--session-check` exit 0 (to 15:54:54); test_check_site.py, 20 tests, OK (to 15:55:05).
- **A scratch clone at c0b1444.**
  - Switch off: landing_facts.py, Zensical 0.0.67, llms_txt.py, check_site.py and `landing_facts.py --check site`, each exit 0 (15:55:24–15:55:43). Switch on: the same steps on the switch-off figures, as the suite builds it, each exit 0 (to 15:55:47).
  - check_landing_browser.mjs: interim 82 checks and probe 294, none failing (15:55:53–15:58:48).
- **The browser block under SHOALMARK_REGENERATE=1** (15:55:53–16:11:51): exit 0. Its 28 controls each exit 1 on the check they name.
- **run-one-check** (16:00:03–16:17:31): the landing, git-wording, no-server and cue checks and their four control checks each exit 0 at c0b1444; against 86b2ee8 the four checks fail, each exit 1.
- **Controls on 86b2ee8's probe build:** c0b1444's check_site.py exits 1 on step 2's address (16:02:16), and its check_landing_browser.mjs exits 1 with 11 checks failing (16:12:05–16:13:31).
- **Before this commit:** `--check` and `--session-check` exit 0 (16:19:11–16:19:25).

Quality read: apart from RV-2910, the round reads clean.
