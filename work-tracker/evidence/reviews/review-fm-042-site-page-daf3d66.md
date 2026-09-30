# Review — FM-042, the requirements page on the site, the rework of RV-2050 to RV-2052 (daf3d66)

Reviewed: daf3d66c471736d3e2260be6fd3ec73755a53eef

- Seat: reviewer-63 (session 8e509911/reviewer-63), worktree shoalmark-review-4, 2026-09-30 14:02–14:05 CEST. Range: ca584e3 (the verdict NOT READY on 141542e) … daf3d66, three commits by the Implementer (Sonnet 5.5 at medium), all in `docs/de/requirements.md`, +9 −9.
- Tier: docs by FM-032 S1; a re-pass, no suite run. Independence: same session.
- Verdict: READY — the two P2 and the P3 are fixed as written; no new finding.

## Checks

1. RV-2050 (73ba1f9). :14 now matches the fix text byte for byte: *Das Gerät muss spätestens 2 s nach der letzten Eingabe in den Ruhezustand wechseln.* with the accept *Eingabe endet: im Ruhezustand nach < 2 s*. It states one obligation and an upper bound, as the English and its own accept do.
2. RV-2051 (e4a6041). At :42–44, *was eine Anforderung nennt, wird als veraltet markiert, sobald sie sich ändert*: FM-042's stale-marking, no date, the three other items unchanged.
3. RV-2052 (daf3d66). :40 reads *Jede Stufe*. :8 reads *entfernt sich mit der Zeit vom Code*. :28–30 say *Fundstelle — Norm, Ausgabe, Abschnitt*, *die eigene Pflicht des Unternehmens … als Satz in der Spalte `shall`*, *erfülle die Norm*. The Principal chose *Fundstelle*/*Abschnitt*, the words ADOPT.de.md uses, over the brief's *Klausel*.
4. The German page re-read whole: *Sie*/*Ihr*, the site's words (*Sitz*, *Tafel*, *Frage*, *Id*, *Arbeitspaket*), native throughout; the same facts as the English, the same absolute link.
5. The claim screen, by hand, on the nine changed lines and the page around them; the scoring service was not called. G0–G5 pass. The compliance-word grep has the same four hits as before: :29–30 are the prohibition and the definition (a met requirement is a passed test), :34 is *satisfies* for a requirement. There is no claim and no standard's text. The control (*Mit shoalmark erfüllt Ihr Projekt die Norm.*) still dies at G2.
6. The site, as the release builds it, 14:03 CEST: the pins are unchanged (zensical 0.0.66, tinycss2 1.4.0). `zensical build --clean`, `llms_txt.py site` (13 pages) and `check_site.py site` exit 0. `site/de/requirements.html` renders the new row, the rule and Stufe 1, with `<` escaped. The nav reads *The standup* → *Requirements* → *For agents — the contract* and *Der Standup* → *Anforderungen*. The German llms twin is byte-identical to its source.
7. Gates. `--check` 0 at 14:03: *8 commit(s) … every build commit under a judged In Progress tracker*. `--session-check` 0. `git merge-tree --write-tree origin/main HEAD` against 7380039 is clean (`b118995`). `--queue` at 14:03:52: *branch fm/042-the-requirements-page-on… @ daf3d66 wait: no pull request — no verdict on daf3d66*. The three commits carry `Session: 8e509911/implementer-63`, `Worktree: shoalmark-impl-2` and `Co-Authored-By`. The ship-log row's counts still hold on the net diff: 45 + 43 + 2 = 90 product added, 1 record added, 0 deleted.

Quality read (the build: Sonnet 5.5 at medium): clean — each fix is the fix text, nothing else moved. Unproven: the site was built on macOS with Python 3.14, not CI's Ubuntu with 3.12. G1 rests on this runtime's reading, with no native reader.

Path 5 — a merge rules nothing.
