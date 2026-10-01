# FM-006 — the Reviewer's code pass on `fm/006-what-a-stranger-meets-first` at 6f24273, part 1: the Builders' work

Verdict: **READY WITH FINDINGS** — four P3 on the slice (RV-2180 … RV-2183) and two P3 found on the way, not this slice's (RV-2184, RV-2185). Every ruled text stands word for word, every new line I tested is true against the tool at this tree, the site builds clean, and its three checks exit 0.
Reviewed: 6f242738a9f8d66dbe04538f13beaa54eac970d5 — `32780e5..6f24273`, eleven commits and one merge of the branch into itself (5b7ff41).
Reviewer: b3bdb000/reviewer-76 (claude-opus-5-5, max), `reviewer@seat` unsigned, worktree shoalmark-review-10, 08:24–08:48 CEST on 2026-10-01. Independence: the same session as the build (b3bdb000/implementer-70 and b3bdb000/implementer-71), so not independent.
Tier: code. `git diff --name-only origin/main...HEAD` lists `zensical.toml`, `overrides/main.html`, `scripts/check_site.py`, `scripts/llms_txt.py` and `scripts/test_check_site.py` beside the pages, the notes and the trackers.
Read: FM-006's section *What a stranger meets first — v0.19.0* (A as amended 2026-10-01, B, C, D, E), AGENTS.md, and `git diff 32780e5 6f24273` whole — implementer-71's 2d232e3, fe35efd and 3dbb582; implementer-70's 2039f7a, c7b5268, 5c561ef, 3790905, 26a59d3, 604cba2, 2f8ff3e and 6f24273. Not in this pass: the Designer's landing, preview image and render (part 2).

## Findings

- **RV-2180 · P3 · FM-031's record of the signed nine quotes rule 3 as the Owner did not sign it.**
  - FM-031:146 opens the list with *Signed as written, the nine:*. The Owner's signed answer `eef0c2e` (2026-09-24 21:29:12, signature good) accepted rule 3 reading *he said yes*. 3790905 rewrote FM-031:150 to *they said yes* with no mark, so the record now says the Owner signed words they did not sign.
  - The link 3790905 names is right: AGENTS.md:82–83 says the nine stand *in the words FM-031's body records them*, so AGENTS.md:86 (E) and FM-031:150 are one text in two places, and changing one alone would make AGENTS.md:83 false. What is missing is the mark. These records mark a quote they change (*spelling normalised*), and E keeps quoted records as history.
  - **Fix:** at FM-031:146, replace `Signed as written, the nine:` with `Signed as written, the nine — rule 3's example signed as *he said yes*, written *they said yes* since E of the Owner's ruling of 2026-09-30, filed in FM-006:`. AGENTS.md stays as 3790905 wrote it.
- **RV-2181 · P3 · The CHANGELOG bullet (CHANGELOG.md:9–13) misstates three things and overstates a fourth.**
  - *The Owner's ruling of 2026-09-30*: the one description, the link previews and both ledes come from A as amended on 2026-10-01 (FM-006, *What is true now*).
  - *one description and link previews serve every page*: the German start page has a description of its own (A2). Every other page previews with the one.
  - *the tagline, Get a better-performing human Owner., stands … in both notes*: `ADOPT.de.md` opens with *Euer Owner bremst. Tunen statt tauschen.* (B3).
  - *the last gendered pronouns on current pages are gone* holds only if quoted records are set aside, as E sets them aside. Two quotes remain: the landing's `WRECKS` titles, and the tool's output quoted from a run at `88c7b0c` on the triage pages (docs/triage.md:137–138 and docs/de/triage.md:170–171, *his* and *he*). The tool prints *their* today (shoalmark.py:5600, :5607).
  - **Fix:** CHANGELOG.md:9–13 read:

    ```
    - **What a stranger meets first (FM-006) — pages and wording, no product growth.** The Owner's ruling of 2026-09-30, its A amended on 2026-10-01,
      filed in FM-006: the landing leads with *The agents keep the work; the person keeps the word.* and one action, *Hand your agents the note* — the new
      English note, `ADOPT.md`; the German start page leads the same way, with a title and a description of its own; one description serves every other
      page, and every page carries a link preview; the tagline, *Get a better-performing human Owner.*, stands where agents read — the README, `llms.txt`
      and the English note, and the German note opens with *Euer Owner bremst. Tunen statt tauschen.*; the fleet has a section on the landing; the seats
      page says the Owner is not a seat; the last gendered pronouns on current pages are gone, quoted records aside.
    ```
- **RV-2182 · P3 · The site check reads none of the tags the override adds, and the image they name is not in the site at this tree.**
  - Falsifier: on a build of 6f24273, all 14 pages the theme renders carry `og:image` `https://shoalmark.github.io/shoalmark/assets/preview.png`. `site/assets/preview.png` does not exist (`docs/assets/` holds `favicon.svg` and the fonts), yet `check_site.py site` exits 0.
  - The image is the Designer's (part 2). The docs workflow at the tag is this check's only run, so a missing or misnamed image would deploy unseen in every link preview.
  - **Fix:** in `scripts/check_site.py`, after the `Links` loop (:47–48):

    ```python
    class PreviewImage(HTMLParser):
        """FM-006: the image a page's link preview names is a file of the site."""
        def __init__(self, page):
            super().__init__()
            self.page = page

        def handle_starttag(self, tag, attrs):
            attrs = dict(attrs)
            if tag != "meta" or attrs.get("property") != "og:image":
                return
            url = urlsplit(attrs.get("content") or "")
            if url.netloc != "shoalmark.github.io" or not url.path.startswith("/shoalmark/") \
                    or not (site / unquote(url.path[len("/shoalmark/"):])).is_file():
                raise SystemExit(f"site check: link preview image not in the site, in {self.page}: {attrs.get('content')}")


    for page in site.rglob("*.html"):
        PreviewImage(page.relative_to(site)).feed(page.read_text(encoding="utf-8"))
    ```

    Its closing line then reads `site check: entry pages, contract inclusion, landing/contract destinations, link preview images and public URLs passed`. In `scripts/test_check_site.py`, two blank lines before `if __name__ == "__main__":`, add:

    ```python
    class LinkPreview(unittest.TestCase):
        def test_preview_image_is_a_file_of_the_site(self):
            meta = '<meta property="og:image" content="https://shoalmark.github.io/shoalmark/assets/preview.png">'
            for present in (True, False):
                with self.subTest(present=present), tempfile.TemporaryDirectory() as tmp:
                    site = Path(tmp)
                    for name in ("index.html", "setup.html", "signing.html", "de/signing.html", "agents/index.html", "llms.txt"):
                        p = site / name
                        p.parent.mkdir(parents=True, exist_ok=True)
                        p.write_text(meta + "Get a better-performing human Owner.")
                    if present:
                        (site / "assets").mkdir()
                        (site / "assets/preview.png").write_bytes(b"synthetic image")
                    result = subprocess.run([sys.executable, str(CHECKER), str(site)], capture_output=True, text=True)
                    self.assertEqual(result.returncode == 0, present, result.stdout + result.stderr)
                    if not present:
                        self.assertIn("link preview image not in the site", result.stderr)
    ```
  - Tried on a scratch copy: 5 tests ok. On the build of this tip, the check exits 1 with *link preview image not in the site, in signing.html: …*. With an image at `docs/assets/preview.png`, it exits 0. Until the Designer's image lands, the site check fails on this branch, and that failure is the point: it runs only at the tag.
- **RV-2183 · P3 · ADOPT.md:39–43: the id prefix is not the folder's name in general, and inside a git working copy `--init` writes a fifth file.**
  - The tool takes the first word of the directory's name and cuts it to five characters (shoalmark.py:7263, the same at v0.18.6). `probe` gives `PROBE`, as the note says. But the note's *If the Owner says yes* runs `--init` in the real directory, and there `firmware-controller` gives `FIRMW`.
  - Inside a git working copy, `--init` also writes `.gitignore` with the board's two lines (`vcs()` looks up through the parent folders).
  - **Fix:** ADOPT.md:39–43 read:

    ```
    Nothing needs copying before `--init`: its defaults are English — every entry carries the sections *What is true now*,
    *Why*, *Done when* and *Ship log*, and the board is English. The id prefix is the first word of the folder's name, cut
    to five characters, so in `probe/` the first entry is `PROBE-001` (`--key` would choose another). Then
    `python tools/shoalmark/shoalmark.py --init`; it overwrites nothing. It writes `shoalmark.toml`,
    `docs/work-tracker/TRIAGE.md`, the agents' contract in `AGENTS.md` and a `CLAUDE.md` router, and inside a git working
    copy the board's two lines in `.gitignore`.
    ```

**Found on the way, not this slice's — for the Planner to place:**
- **RV-2184 · P3 · `--key`'s help says *default: the directory name's first word*** (shoalmark.py:6800), but `init` cuts that word to five characters (:7263): `shoalmark` gives `SHOAL`. **Fix:** the help ends `default: the directory name's first word, cut to five characters`. This is product text, and this slice grows no product.
- **RV-2185 · P3 · The German pages declare `<html lang="en">`.** The theme's language is site-wide (`zensical.toml`: `language = "en"`). So a screen reader or a browser takes every page under `de/` for English, while the override now writes `og:locale` de_DE there. **Fix**, tried on a scratch copy — `overrides/partials/language.html`:

  ```
  {% set language = "de" if (page and page.url and page.url[:3] == "de/") else (config.theme.language | d("en", true)) %}
  {% import "partials/languages/" ~ language ~ ".html" as lang %}
  {% import "partials/languages/en.html" as fallback %}
  {% macro t(key) %}{{ lang.t(key) or fallback.t(key) or key }}{% endmacro %}
  ```

  With it, the pages under `de/` get `lang="de"`, the others keep `en`, and the site check passes. It also makes the theme's own strings under `de/` German: a visible change, so the Owner's to rule.

## What holds
1. **Every ruled text, word for word.** A script took each text from FM-006's section, not my eye, and found it in its file:
   - A1's H1, job line and action in `docs/index.md`; the description in `zensical.toml`; the `og:image:alt` text.
   - A2's lead, job line, `title:` and `description:`.
   - B1's README heading (:3); B2's `llms.txt` line (the build prints `> Get a better-performing human Owner. …`); B3's claim atop `ADOPT.de.md` (:3) and line 5's fix, now :7 (`und **euer Owner entscheidet**`); B4's opening and `**your Owner decides**`.
   - C's definition and *as the adopter chooses*.
   - D1's phrase stands on one line (docs/seats/index.md:5), with `planner`, `reviewer` and `builder` in code spans, as the page set its keys before. A grep for the plain phrase misses it.
2. **True against the tool at this tree.** D1's rights are `BUILTIN_RIGHTS` (shoalmark.py:190–191), `principal` and `implementer` included. The ledes' gate clause holds in a scratch git repository: a move to `Shipped` whose ship log names no commit is refused by `--check` (exit 4, *moved to `Shipped` with no commit behind it*); one that names the feature's commit passes (exit 0).
3. **The German reads natively.** The lede and the job line are as ruled. *Geben Sie Ihren Agenten die Notiz* is idiomatic, with the *Sie* imperative and the dative plural right. The person is *Sie* throughout, and the fleet is *ihr*, as the note addresses the agents. In `ADOPT.de.md`, the claim and *euer Owner entscheidet* read natively in the note's *ihr*. No German pronoun on a current page stands for the Owner.
4. **ADOPT.md is a faithful translation.** It has the same sections in the same order, the same steps and commands, the same tag and the same checksum: `git show v0.18.6:shoalmark.py | shasum -a 256` = `5330ee06…`, with no CR.
   - Its departures, each run at v0.18.6 and at this tree in a folder outside version control: there is nothing to copy, because the defaults are English; `--init` writes the four files the note names and announces `PROBE-001`.
   - `--new` gives `PROBE-001` with the sections *What is true now*, *Why*, *Done when* and *Ship log*; `epic: PROBE-001` passes the gate; INDEX.md and the board land under `docs/work-tracker/`.
   - *the company's own shall* (:80) renders *einen eigenen Satz* in AGENTS.md's English words.
5. **The theme override.** I built the site with Zensical 0.0.66 (a venv, `requirements-docs.txt`).
   - Each of the 14 pages the theme renders carries each tag once: `og:type`, `og:site_name`, `og:locale`, `og:url` (equal to the canonical), `og:title`, `og:description`, `og:image` with its width, height and alt, and `twitter:card`. The six pages under `de/` say `de_DE`; the others say `en_GB`.
   - Each page has one canonical, and it is the theme's (base.html:21–22). The Builder's reading holds.
   - The 404 has no canonical and no `og:url`. Its title is the site's name and its description the site's.
   - The German start page takes its `title:` and `description:`. Other pages take their nav title; the German start page without front matter would read *Start*.
   - The guard, on scratch pages: front matter without a title, a German page without front matter and `title: ""` each fall back cleanly.
   - Escaping: a title `A "quoted" <b>bold</b> & title` comes out escaped once in `og:title`, while the theme's own description meta prints it raw. So the comment's *does not escape on its own* is true, and `| e` is needed.
   - Every claim in the override's comment matches the theme's base.html.
6. **The site's own checks**, run in the docs workflow's order on a clean clone at 6f24273: `test_check_site.py` 4 ok; `zensical build --clean` no issues; `llms_txt.py site` 14 pages; `check_site.py site` exit 0. The new marker bites: with the README's old heading, the check exits 1 with *agents' contract include did not render*.
7. **The seats page and E.**
   - The seats page has 21 table rows before and after: the same rows, in the same order inside each group, now under *The core seats* and *Specialists*.
   - E: README:269 reads *theirs*. docs/requirements.md:39 reads *their go*, and its German twin says *mit Ihrem Wort*. AGENTS.md:86 and FM-031:150 read *they said yes* (see RV-2180).
   - No link points at the README's old anchor. `grep -c '^## Unreleased' CHANGELOG.md` = 1.
8. **The records rule**: the eleven commit messages cite the Owner's ruling filed in FM-006, and none quotes a conversation.

## Controls, one line each
- Setup, 08:24: `git status --short` empty; one fetch; detached at 6f24273, which equals `origin/fm/006-what-a-stranger-meets-first`. `--whoami`: `To: b3bdb000/reviewer-76 reviewer (shoalmark-review-10) · claude-opus-5-5 · max`.
- ADOPT.md steps 3–4, on clones at v0.18.6 (`1c344ed`) and 6f24273 (the untagged tip vendored with `--allow-untagged`), 08:27–08:31: the same results at both.
- Site build, 08:32:27–08:32:33: the four workflow steps, each exit 0. Heads read by hand from setup.html, de/index.html, de/signing.html and 404.html, and from every page by script.
- Escaping and the guard: four scratch pages in one build. The marker's negative control: one build.
- The gate clause: a scratch git repository with this tree's tool — no commit named, refused (exit 4); the feature named, passes (exit 0).
- RV-2182's and RV-2185's fixes were tried on a scratch copy; neither is in this commit.

Quality read: the commits are small and well cut. Each names its ruling and what it leaves to FM-024. The Builders ran the tool at both trees for ADOPT.md's departures, and built the site before claiming it. The override is minimal, and its comment is true line by line. The weak spots are the records around the change: FM-031's signed text altered without a mark, a CHANGELOG bullet looser than the ruling, and new page tags no check reads.
Four numbers for this verdict: records +153, product 0.
Next:
- RV-2180, RV-2181 and RV-2182 go back to implementer-70 (3790905, 604cba2, 26a59d3), and RV-2183 to implementer-71 (3dbb582). I verify the fix round. RV-2184 and RV-2185 are the Planner's to place.
- Part 2, the Designer's landing, carries:
  - the landing's `<title>` and description, still the old ones (overrides/landing.html:11–12), and its head tags;
  - `docs/assets/preview.png`;
  - its note link to `ADOPT.md` with *(Deutsch)* (:448);
  - E's :411 and :463;
  - the short form of the job line, if the phone render needs it (then `docs/index.md` and `docs/de/index.md` follow);
  - the CHANGELOG's landing clauses.
- The seats page's D1 sentence holds at the tag only if FM-024's D2 is merged; otherwise D1's fallback line goes in. Until then, README §*Seats* says *Four names carry theirs built in — owner all four …*.
- C's definition on the seats page breaks across lines 3–4, so grep for it with the two lines joined.
