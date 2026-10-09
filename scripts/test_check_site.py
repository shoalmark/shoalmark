"""Regression controls for the published site's checks: font sources, link previews, and the landing in two languages with its launch state, How it
works, the Markdown twins and the requests a page makes; run with requirements-docs installed."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

CHECKER = Path(__file__).with_name("check_site.py")
SITE_URL = "https://shoalmark.github.io/shoalmark/"
PROMPT = 'Please check honestly whether shoalmark fits this project; the answer may be "no fit".\nI decide.\n'
LABELS = {"en": "Copy the prompt", "de": "Prompt kopieren"}
TWIN_TEXT = "# How it works\n\nTry it: the button \"Hand your agents the note\" leads to a note.\n\n```\nnext: owner\n```\n"


def landing(lang, probe, tag="v1.2.3", footer_tag=None):
    """A landing as the template builds it, as little of it as the checks read."""
    en = lang == "en"
    where, other = (SITE_URL, SITE_URL + "de/") if en else (SITE_URL + "de/", SITE_URL)
    label = LABELS[lang] if probe else ("Hand your agents the note" if en else "Agenten die Notiz geben")
    primary = (f'<a class="btn" id="probe-open" href="probe.txt" aria-haspopup="dialog">{label}</a>' if probe else
               f'<a class="btn" href="https://github.com/shoalmark/shoalmark/blob/main/ADOPT{"" if en else ".de"}.md">{label}</a>')
    dialog = (f'<dialog class="probe" id="probe" aria-labelledby="probe-h"><h2 id="probe-h">The probe prompt</h2>'
              f'<textarea id="probe-text" readonly>{PROMPT.replace(chr(34), "&#34;")}</textarea></dialog>') if probe else ""
    return (f'<!doctype html><html lang="{lang}"><head><title>{"The agents keep the work" if en else "Die Agenten tragen die Arbeit"}</title>'
            f'<meta name="description" content="{"A work tracker" if en else "Ein Arbeits-Tracker"}">'
            f'<link rel="canonical" href="{where}">'
            f'<link rel="alternate" hreflang="en" href="{SITE_URL}"><link rel="alternate" hreflang="de" href="{SITE_URL}de/">'
            f'<link rel="alternate" hreflang="x-default" href="{SITE_URL}">'
            f'<meta property="og:locale" content="{"en_GB" if en else "de_DE"}">'
            f'<meta property="og:image" content="{SITE_URL}assets/{"preview.png" if en else "preview-de.png"}">'
            f'<link rel="stylesheet" href="{"" if en else "../"}stylesheets/x.css"></head><body>'
            f'<a class="rel" href="https://github.com/shoalmark/shoalmark/releases/tag/{tag}">release<b>{tag}</b></a>'
            f'<a class="lang" href="{"de/index.html" if en else "../index.html"}" hreflang="{"de" if en else "en"}">{"DE" if en else "EN"}</a>'
            f'{primary}<a class="btn alt" href="{"" if en else "../"}{"" if en else "de/"}how-it-works.html">How</a>'
            f'<footer><a href="https://github.com/shoalmark/shoalmark/releases/tag/{footer_tag or tag}">{footer_tag or tag}</a></footer>'
            f'{dialog}<script>const a = 1; addEventListener("resize", () => a);</script></body></html>')


def good_site(site, probe=False):
    """A minimal site that passes every check; a control changes one thing in it."""
    files = {"index.html": landing("en", probe), "de/index.html": landing("de", probe),
             "setup.html": "Get a better-performing human Owner.", "signing.html": "", "de/signing.html": "",
             "agents/index.html": "Get a better-performing human Owner.",
             "how-it-works.html": '<html lang="en"><body>"%s" is the button.</body></html>' % (LABELS["en"] if probe else "Hand your agents the note"),
             "de/how-it-works.html": '<html lang="de"><body>„%s“ ist der Knopf.</body></html>' % (LABELS["de"] if probe else "Agenten die Notiz geben"),
             "how-it-works/index.md": TWIN_TEXT.replace("Hand your agents the note", LABELS["en"] if probe else "Hand your agents the note"),
             "de/how-it-works/index.md": '# So funktioniert\'s\n\n„%s“ ist der Knopf.\n' % (LABELS["de"] if probe else "Agenten die Notiz geben"),
             "de/index.md": "# shoalmark\n\n[Einrichtung](setup/index.md), [Vertrag](../agents/README/index.md), [Notiz](https://github.com/shoalmark/shoalmark/blob/main/ADOPT.de.md)\n",
             "de/setup/index.md": "# Einrichtung\n", "agents/README/index.md": "# README\n",
             "llms.txt": "- [How it works](how-it-works/index.md)\n- [shoalmark](de/index.md)\n- [So funktioniert's](de/how-it-works/index.md)\n",
             "stylesheets/x.css": "body{color:#fff}", "assets/preview.png": "png", "assets/preview-de.png": "png"}
    if probe:
        files["probe.txt"] = files["de/probe.txt"] = PROMPT
    for name, text in files.items():
        (site / name).parent.mkdir(parents=True, exist_ok=True)
        (site / name).write_bytes(text.encode("utf-8"))


def run(site, probe=False):
    toml = site.parent / ("zensical-%s.toml" % ("on" if probe else "off"))
    toml.write_text("[project]\nsite_name = \"x\"\n\n[project.extra]\nprobe = %s\n" % ("true" if probe else "false"), encoding="utf-8")
    return subprocess.run([sys.executable, str(CHECKER), str(site), str(toml)], capture_output=True, text=True)


class FontSources(unittest.TestCase):
    def check(self, css, expected, inline=False, imported=False):
        with tempfile.TemporaryDirectory() as tmp:
            site = Path(tmp) / "site"
            good_site(site)
            (site / "font").write_bytes(b"synthetic local asset")
            (site / "font.woff2").write_bytes(b"synthetic local asset")
            if inline:
                (site / "setup.html").write_text("<style>" + css + "</style>")
            elif imported:
                (site / "style.css").write_text('@import "nested";')
                (site / "nested").write_text(css)
            else:
                (site / "style.css").write_text(css)
            result = run(site)
            self.assertEqual(result.returncode == 0, expected, result.stdout + result.stderr)
            if not expected:
                self.assertIn("site check:", result.stderr)

    def test_local_sources(self):
        for source in ('url(font)', 'url("font.woff2")', 'local("Example"), url(font?revision=1)', 'url(/shoalmark/font)'):
            with self.subTest(source=source):
                self.check('@font-face {font-family: Example; src:' + source + ';}', True)

    def test_external_sources_regardless_of_suffix_or_css_spelling(self):
        for source in ('url(https://other.example/font)', 'url("https://other.example/font?id=1")',
                       'url(//other.example/font)', 'url(https://other.example/font.woff2)',
                       r'url("\68 ttps://other.example/font")', 'URL("https://other.example/font")',
                       'local("Example"), url(font), url(https://other.example/font)'):
            with self.subTest(source=source):
                self.check('@font-face {font-family: Example; src:' + source + ';}', False)

    def test_inline_nested_and_imported_sources(self):
        css = '@media screen { @font-face {src: url(https://other.example/font)} }'
        self.check(css, False)
        self.check(css, False, inline=True)
        self.check(css, False, imported=True)
        self.check('@font-face {src: url(font)}', True, inline=True)

    def test_missing_and_external_import(self):
        self.check('@font-face {src: url(missing)}', False)
        self.check('@import "https://other.example/styles";', False)
        self.check('/* @font-face { src: url(https://other.example/font) } */', True)


class LinkPreview(unittest.TestCase):
    def test_preview_image_is_a_file_of_the_site(self):
        for present in (True, False):
            with self.subTest(present=present), tempfile.TemporaryDirectory() as tmp:
                site = Path(tmp) / "site"
                good_site(site)
                if not present:
                    (site / "assets/preview.png").unlink()
                result = run(site)
                self.assertEqual(result.returncode == 0, present, result.stdout + result.stderr)
                if not present:
                    self.assertIn("link preview image not in the site", result.stderr)


class Landings(unittest.TestCase):
    """B1: each control changes one thing in a site that passes, and the check names it; the controls run in both launch states where they hold in both."""

    def refused(self, change, message, probe=False):
        with tempfile.TemporaryDirectory() as tmp:
            site = Path(tmp) / "site"
            good_site(site, probe)
            change(site)
            result = run(site, probe)
            self.assertNotEqual(result.returncode, 0, "the check passed what it must refuse: " + message)
            self.assertIn(message, result.stderr)

    def edit(self, name, old, new):
        def change(site):
            text = (site / name).read_text(encoding="utf-8")
            self.assertIn(old, text)
            (site / name).write_text(text.replace(old, new, 1), encoding="utf-8")
        return change

    def test_a_good_site_passes_in_both_launch_states(self):
        for probe in (False, True):
            with self.subTest(probe=probe), tempfile.TemporaryDirectory() as tmp:
                site = Path(tmp) / "site"
                good_site(site, probe)
                result = run(site, probe)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_the_german_landing_and_the_new_pages_are_there(self):
        for name in ("de/index.html", "how-it-works.html", "de/how-it-works.html", "de/how-it-works/index.md", "de/index.md"):
            self.refused(lambda site, name=name: (site / name).unlink(), f"missing {name}")

    def test_the_two_languages_name_each_other(self):
        self.refused(self.edit("de/index.html", '<link rel="alternate" hreflang="x-default" href="%s">' % SITE_URL, ""), "does not name its twin")
        self.refused(self.edit("index.html", 'hreflang="de" href="%sde/"' % SITE_URL, 'hreflang="de" href="%s"' % SITE_URL), "does not name its twin")
        self.refused(self.edit("index.html", '<a class="lang" href="de/index.html" hreflang="de">DE</a>', ""), "no language switch")
        self.refused(self.edit("de/index.html", 'hreflang="en">EN</a>', 'hreflang="de">EN</a>'), "no language switch")
        self.refused(self.edit("de/index.html", '<html lang="de">', '<html lang="en">'), "says lang='en'")
        self.refused(self.edit("de/index.html", "assets/preview-de.png", "assets/preview.png"), "link preview is not its language's")
        self.refused(self.edit("de/index.html", "Die Agenten tragen die Arbeit", "The agents keep the work"), "share a title")

    def test_the_second_button_leads_to_how_it_works_of_its_language(self):
        self.refused(self.edit("de/index.html", 'href="../de/how-it-works.html"', 'href="../how-it-works.html"'), "second button that leads to de/how-it-works.html")

    def test_the_release_is_one(self):
        self.refused(self.edit("index.html", '<a href="https://github.com/shoalmark/shoalmark/releases/tag/v1.2.3">v1.2.3</a>', '<a href="https://github.com/shoalmark/shoalmark/releases/tag/v1.2.4">v1.2.4</a>'),
                     "do not name one release")
        self.refused(self.edit("de/index.html", "release<b>v1.2.3</b>", "release<b>v1.2.4</b>"), "do not name one release")

    def test_the_switch_off_builds_no_probe(self):
        self.refused(lambda site: (site / "probe.txt").write_text(PROMPT), "probe.txt is built while the probe switch is off")
        self.refused(lambda site: (site / "de/probe.txt").write_text(PROMPT), "de/probe.txt is built while the probe switch is off")
        self.refused(self.edit("how-it-works/index.md", "Try it:", "Try it, or open probe.txt:"), "speaks of the probe's prompt")
        self.refused(self.edit("index.html", '<a class="btn" href="https://github.com/shoalmark/shoalmark/blob/main/ADOPT.md">', '<a class="btn" id="probe-open" href="https://github.com/shoalmark/shoalmark/blob/main/ADOPT.md">'),
                     "the probe switch is off, but the primary button")
        self.refused(self.edit("index.html", '<a class="btn" href="https://github.com/shoalmark/shoalmark/blob/main/ADOPT.md">', '<a class="btn" id="probe-open" href="probe.txt">'),
                     "broken link in index.html: probe.txt")
        self.refused(self.edit("de/index.html", "</body>", '<dialog id="probe"></dialog></body>'), "the probe switch is off, but the primary button")

    def test_the_switch_on_builds_the_prompt_the_dialog_shows(self):
        self.refused(lambda site: (site / "probe.txt").unlink(), "broken link in index.html: probe.txt", probe=True)
        self.refused(lambda site: (site / "de/probe.txt").write_text(PROMPT + " "), "de/probe.txt is missing or is not, byte for byte", probe=True)
        self.refused(self.edit("probe.txt", "I decide.", "I decide!"), "probe.txt is missing or is not, byte for byte", probe=True)
        self.refused(self.edit("index.html", ' aria-labelledby="probe-h"', ""), "not one labelled dialog", probe=True)
        self.refused(self.edit("de/index.html", '<textarea id="probe-text" readonly>', '<textarea id="other" readonly>'), "not one labelled dialog", probe=True)
        self.refused(self.edit("index.html", '<a class="btn" id="probe-open" href="probe.txt" aria-haspopup="dialog">', '<a class="btn" href="probe.txt">'), "does not copy the prompt", probe=True)

    def test_how_it_works_names_the_button_as_the_landing_labels_it(self):
        self.refused(self.edit("how-it-works.html", '"Hand your agents the note"', '"Run probe prompt"'), "does not name the primary button")
        self.refused(self.edit("de/how-it-works/index.md", "„Agenten die Notiz geben“", "„Probe-Prompt starten“"), "does not name the primary button")
        self.refused(self.edit("de/how-it-works.html", '„Prompt kopieren“', '„Probe-Prompt starten“'), "does not name the primary button", probe=True)
        self.refused(self.edit("de/how-it-works.html", '<html lang="de">', '<html lang="en">'), "says lang='en'")

    def test_the_twins_are_text(self):
        self.refused(self.edit("how-it-works/index.md", "```\nnext: owner\n```", '<figure class="week"><pre>next: owner</pre></figure>'), "carries raw HTML")
        self.refused(self.edit("de/how-it-works/index.md", "# So", '--8<-- "how-it-works.de.md"\n# So'), "carries raw HTML, an include or a state fence")
        self.refused(self.edit("how-it-works/index.md", "# How it works", "<!-- state: probe -->\n# How it works"), "carries raw HTML, an include or a state fence")
        self.refused(self.edit("de/index.md", "(setup/index.md)", "(../setup/index.md)"), "no German page's twin")
        self.refused(self.edit("de/index.md", "(setup/index.md)", "(../index.md)"), "no German page's twin")
        self.refused(self.edit("llms.txt", "- [So funktioniert's](de/how-it-works/index.md)\n", ""), "does not list the German start page and both How it works pages")

    def test_no_page_asks_another_host_for_anything(self):
        self.refused(self.edit("index.html", "</head>", '<script src="https://example.org/x.js"></script></head>'), "loads https://example.org/x.js (script), from outside the site")
        self.refused(self.edit("de/index.html", "</head>", '<link rel="stylesheet" href="//example.org/x.css"></head>'), "from outside the site")
        self.refused(self.edit("setup.html", "Get", '<img src="https://example.org/pixel.gif">Get'), "(img), from outside the site")
        self.refused(self.edit("index.html", "const a = 1;", 'fetch("https://example.org/");'), "an inline script of index.html can ask for something")
        self.refused(self.edit("de/index.html", "const a = 1;", "navigator.sendBeacon('/x');"), "an inline script of de/index.html can ask for something")
        self.refused(self.edit("setup.html", "Get", '<a data-md-component="source" href="https://github.com/shoalmark/shoalmark">x</a>Get'), 'data-md-component="source"')
        self.refused(lambda site: (site / "stylesheets/x.css").write_text("body{background:url(https://example.org/a.png)}"), "loads a stylesheet resource from outside the site")
        self.refused(self.edit("how-it-works.html", "<body>", '<body><iframe src="http://example.org/"></iframe>'), "(iframe), from outside the site")


if __name__ == "__main__":
    unittest.main()
