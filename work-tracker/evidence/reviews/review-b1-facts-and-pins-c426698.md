# FM-006: B1's figures, the probe prompt's pins and docs.yml, the review at c426698

Verdict: **READY**. The six findings of the first pass, RV-2880 to RV-2885, are closed, and no P1, P2 or P3 stands.
Reviewed: c426698477dbe14cc1782de2d0ab8986efcec714, `git diff a86667f c426698`. It holds 14 commits by implementer-127: `scripts/landing_facts.py` with its recorded pull requests, docs.yml and its check, `.gitignore`, CONTRIBUTING.md, requirements-docs.txt and the suite's site builds. Tier: critical, the full loop. It is code: `git diff --name-only origin/main...c426698` names `.github/workflows/docs.yml`, `scripts/landing_facts.py` and `test_shoalmark.py`. Two passes: 885c358, then c426698.

## What holds
- **The figures.** The release is v0.19.2, with its day in English and German. There are 28 wrecks, 10 of them open, and the counts are wrecks_json's own. The 27 earlier wrecks are byte for byte the design preview's, and FM-045 is the one new wreck. The high scores are 71/82 to #144 and 10/37 from the recorded response. Read live with no token sent, they are 76/91 to #156. The recorded list equals the API's up to #144, and a pull-request build writes the same file as a local build.
- **The release by event.** All 9 of the Builder's controls hold, and no event deploys a release other than the tagged one VERSION names. The github-pages environment admits only `main` and `v*`.
- **docs.yml.** There is no `pull_request_target`. The workflow grants nothing of its own; the build holds `contents: read` and `pull-requests: read`, and the deploy holds `pages: write` and `id-token: write`. The deploy runs only where the repository is public and the event is not a pull request. No `${{ }}` stands inside a `run:`, the checkout keeps no token, and only the deploy is in the `pages` group.
- **The pins.** With the switch off, nothing pinned reaches the site and probe.txt is not built. With it on, checks 1–5 and 7 run, plus 6 and 9 on a deploy build, and a stand-in left stops the build at check 1. The archive address is one plain file name in the tag's download folder of the repository that zensical.toml names.
- **The placement.** Measured in Chrome at 1280–2560 by 720–1200 px, in both languages and both launch states, no wreck's button falls under the hero's text (14, 9, 164, 120.71).
- **What the script runs.** It starts only git, and the commit's own `--owner` in a throwaway clone that it then removes. shoalmark.py, ci.yml and gate.yml are unchanged.

## The sinks, probed with tracker text from any author (titles, hooks, act lines, file names), rendered through the landing's template and read in headless Chrome
- **The inline script's `const WRECKS`.** js_string leaves no `</`, no `<!--`, no brace inside a string and no raw U+2028 or U+2029. node reads the literal back to facts.html's values.
- **Titles and reports in innerHTML, and the wreck buttons' names.** They are held by the template's `esc` and `code`; no element or handler came from them.
- **The wreck's link.** It is the repository's own address, with the file name percent-encoded.
- **The board excerpt's act line, which the template prints raw.** The script HTML-escapes it once and writes it as `\uXXXX` into its Jinja literal. It renders escaped once, with its braces literal.
- **release, hiscore, read, pins and counts.** Each is checked against its shape before facts.html is written.

## Findings of the first pass, at 885c358, and how each was closed
- **RV-2880 · P2 · 21a2ec8.** Pins check 2 now takes only `https://github.com/<repository>/releases/download/<tag>/<one file name>`, and the pins table's two new rows stop at check 2. Against 885c358's script, the row with dot segments fails. Of 16 address forms probed, only the plain file name passes.
- **RV-2881 · P3 · c6b34c7.** The check pins every escape of wrecks_json: dropping any one of them fails it. It allows the braces of the JSON's own objects, which cannot form a Jinja delimiter.
- **RV-2882 · P3 · 0a91bdd.** The trackers are listed with `-z`, and the links are percent-encoded. Its check fails against 885c358's script.
- **RV-2883 and RV-2884 · P3 · 8fed2cf.** The history property requires `persist-credentials: false`, and its control row fails. docs.yml's comment and the property's name say "the scripts in scripts/ that the build runs".
- **RV-2885 · P3 · c426698.** requirements-docs.txt resolves tzdata 2026.5 for Windows alone. A Python with no time-zone path reads Europe/Berlin with it.

## Commands and controls: 2026-10-09, CEST, as `date` printed each
- **First pass, at 885c358.** py_compile under 3.14.8 and 3.9.6 (07:20:34–07:20:36). test_core all green (07:20:42–07:21:05). `--check` and `--session-check` exit 0 (to 07:21:16). test_check_site.py OK (07:21:51–07:21:53). The script live, from the recorded list and as a pull-request build (07:22:34–07:23:07). A site build through the landing's template at 30427cf (07:24:20–07:24:37). The hostile renderings and the Chrome measures (07:26:09–07:51:13). run-one-check two at a time on every block, all passing, the FM-032 rebuild with `SHOALMARK_REGENERATE=1` among them (07:32:11–07:44:23).
- **Second pass, at c426698, the checks.** py_compile under both (08:17:24–08:17:26). test_core all green (08:17:26–08:17:47). `--check` and `--session-check` exit 0 (08:17:47–08:17:58). test_check_site.py OK (08:17:58–08:18:00).
- **Second pass, run-one-check.** RV-2882 (08:18:06–08:19:48). RV-2881 and the reading block, 9 checks (08:19:56–08:21:42). The pins, 14 checks, and RV-2750, 15 checks (08:21:48–08:23:31). docs.yml, 28 checks, and RV-2882 against 885c358, which FAILED as its control should (08:23:41–08:25:24). The new pins rows against 885c358, where the row with dot segments FAILED (08:25:29–08:27:19).
- **Second pass, the builds and probes.** The script live, from the recorded list and as a pull-request build (08:28:04–08:28:34). A site build through c426698 merged into the landing's branch at 5b0139a (08:28:42–08:28:55). The hostile rendering (08:29:21). The address forms (08:30:07–08:30:17). The requirements resolved per platform, and the escapes dropped one at a time (08:31:08–08:31:09).
- `--check` and `--session-check` exit 0 with this file in place, before the commit (08:33:19–08:33:30).

Quality read: the comments, docstrings, check names, CONTRIBUTING's lines and commit messages claim only what holds.
