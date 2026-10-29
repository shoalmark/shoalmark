"""Regression controls for the published site's checks: font sources, link previews, the landing in two languages with its launch state, How it
works, the Markdown twins and the requests a page makes, and fenced code; run with requirements-docs installed."""
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

CHECKER = Path(__file__).with_name("check_site.py")
SITE_URL = "https://shoalmark.tools/"
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
    short = SITE_URL + ("" if en else "de/") + "probe.txt"
    dialog = (f'<dialog class="probe" id="probe" aria-labelledby="probe-h"><h2 id="probe-h">The probe prompt</h2>'
              f'<textarea id="probe-text" readonly>{PROMPT.replace(chr(34), "&#34;")}</textarea>'
              f'<a href="{short}">{short.replace("https://", "").replace("/", "/<wbr>")}</a></dialog>') if probe else ""
    return (f'<!doctype html><html lang="{lang}"><head><title>{"The agents do the work" if en else "Die Agenten tragen die Arbeit"}</title>'
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
             "index.md": "# shoalmark\n\n**[%s](%s)**\n" % ((LABELS["en"], SITE_URL + "probe.txt") if probe else ("Hand your agents the note", "https://github.com/shoalmark/shoalmark/blob/main/ADOPT.md")),
             "de/index.md": "# shoalmark\n\n**[%s](%s)**\n\n[Einrichtung](setup/index.md), [Vertrag](../agents/README/index.md), [Notiz](https://github.com/shoalmark/shoalmark/blob/main/ADOPT.de.md)\n"
                            % ((LABELS["de"], SITE_URL + "de/probe.txt") if probe else ("Geben Sie Ihren Agenten die Notiz", "https://github.com/shoalmark/shoalmark/blob/main/ADOPT.de.md")),
             "de/setup/index.md": "# Einrichtung\n", "agents/README/index.md": "# README\n",
             "llms.txt": "- [How it works](how-it-works/index.md)\n- [shoalmark](de/index.md)\n- [So funktioniert's](de/how-it-works/index.md)\n",
             "stylesheets/x.css": "body{color:#fff}", "assets/preview.png": "png", "assets/preview-de.png": "png"}
    if probe:
        files["probe.txt"] = files["de/probe.txt"] = PROMPT
    for name, text in files.items():
        (site / name).parent.mkdir(parents=True, exist_ok=True)
        (site / name).write_bytes(text.encode("utf-8"))
    (site.parent / "docs").mkdir(parents=True, exist_ok=True)       # the docs folder beside the site, where zensical.toml's docs_dir points by default
    (site.parent / "docs/index.md").write_text("# shoalmark\n", encoding="utf-8")


LEGAL_PAGES = {"en": ("imprint.html", "privacy.html"), "de": ("de/impressum.html", "de/datenschutz.html")}


def footer(rel, links=None):
    """The footer of the page at `rel`: its language's imprint and privacy notice, linked from where the page stands, or the `links` given."""
    up = "../" * rel.count("/")
    links = links or [up + target for target in LEGAL_PAGES["de" if rel.startswith("de/") else "en"]]
    return "<footer>" + "".join(f'<a href="{href}">{href}</a>' for href in links) + "</footer>"


def footed(site):
    """The four legal pages, where they are missing, and every page of the site with its footer."""
    for lang, pair in LEGAL_PAGES.items():
        for rel in pair:
            if not (site / rel).is_file():
                (site / rel).parent.mkdir(parents=True, exist_ok=True)
                (site / rel).write_text(f'<html lang="{lang}"><body><h1>{rel}</h1></body></html>', encoding="utf-8")
    for page in sorted(site.rglob("*.html")):
        text = page.read_text(encoding="utf-8")
        foot = footer(page.relative_to(site).as_posix())
        page.write_text(text.replace("</body>", foot + "</body>", 1) if "</body>" in text else text + foot, encoding="utf-8")


def checked_site(site, toml):
    return subprocess.run([sys.executable, str(CHECKER), str(site), str(toml)], capture_output=True, text=True)


def run(site, probe=False, foot=True):
    if foot:
        footed(site)
    toml = site.parent / ("zensical-%s.toml" % ("on" if probe else "off"))
    toml.write_text("[project]\nsite_name = \"x\"\n\n[project.extra]\nprobe = %s\n" % ("true" if probe else "false"), encoding="utf-8")
    return checked_site(site, toml)


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
        for source in ('url(font)', 'url("font.woff2")', 'local("Example"), url(font?revision=1)', 'url(/font)'):
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
        for name in ("de/index.html", "how-it-works.html", "de/how-it-works.html", "de/how-it-works/index.md", "de/index.md", "index.md"):
            self.refused(lambda site, name=name: (site / name).unlink(), f"missing {name}")

    def test_the_two_languages_name_each_other(self):
        self.refused(self.edit("de/index.html", '<link rel="alternate" hreflang="x-default" href="%s">' % SITE_URL, ""), "does not name its twin")
        self.refused(self.edit("index.html", 'hreflang="de" href="%sde/"' % SITE_URL, 'hreflang="de" href="%s"' % SITE_URL), "does not name its twin")
        self.refused(self.edit("index.html", '<a class="lang" href="de/index.html" hreflang="de">DE</a>', ""), "no language switch")
        self.refused(self.edit("de/index.html", 'hreflang="en">EN</a>', 'hreflang="de">EN</a>'), "no language switch")
        self.refused(self.edit("de/index.html", '<html lang="de">', '<html lang="en">'), "says lang='en'")
        self.refused(self.edit("de/index.html", "assets/preview-de.png", "assets/preview.png"), "link preview is not its language's")
        self.refused(self.edit("de/index.html", "Die Agenten tragen die Arbeit", "The agents do the work"), "share a title")

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
        self.refused(self.edit("index.html", ">shoalmark.tools/<wbr>probe.txt</a>", ">probe.txt</a>"), "second step does not link to", probe=True)
        self.refused(self.edit("de/index.html", ">shoalmark.tools/<wbr>de/<wbr>probe.txt</a>", ">https://shoalmark.tools/de/probe.txt</a>"), "second step does not link to", probe=True)
        self.refused(self.edit("de/index.html", ">shoalmark.tools/<wbr>de/<wbr>probe.txt</a>", ">shoalmark.tools/<wbr>probe.txt</a>"), "second step does not link to", probe=True)
        self.refused(self.edit("index.html", '<a href="https://shoalmark.tools/probe.txt">', '<a href="https://example.org/probe.txt">'), "second step does not link to", probe=True)

    def test_how_it_works_names_the_button_as_the_landing_labels_it(self):
        self.refused(self.edit("how-it-works.html", '"Hand your agents the note"', '"Run probe prompt"'), "does not name the primary button")
        self.refused(self.edit("de/how-it-works/index.md", "„Agenten die Notiz geben“", "„Probe-Prompt starten“"), "does not name the primary button")
        self.refused(self.edit("de/how-it-works.html", '„Prompt kopieren“', '„Probe-Prompt starten“'), "does not name the primary button", probe=True)
        self.refused(self.edit("de/how-it-works.html", '<html lang="de">', '<html lang="en">'), "says lang='en'")

    def test_the_start_pages_twins_lead_with_the_pages_own_action(self):
        note = "https://github.com/shoalmark/shoalmark/blob/main/ADOPT.md"
        self.refused(self.edit("index.md", "](%s)" % note, "](%s)" % (SITE_URL + "probe.txt")), "does not lead with the page's own action")
        self.refused(self.edit("index.md", "](%s)" % note, "](setup/index.md)"), "does not lead with the page's own action")
        self.refused(self.edit("de/index.md", "](https://github.com/shoalmark/shoalmark/blob/main/ADOPT.de.md)**", "](https://github.com/shoalmark/shoalmark/blob/main/ADOPT.md)**"), "does not lead with the page's own action")
        self.refused(self.edit("de/index.md", "Einrichtung", "Einrichtung, probe.txt"), "does not lead with the page's own action")
        self.refused(self.edit("index.md", "](%sprobe.txt)" % SITE_URL, "](%s)" % note), "does not lead with the page's own action", probe=True)
        self.refused(self.edit("de/index.md", "](%sde/probe.txt)" % SITE_URL, "](https://github.com/shoalmark/shoalmark/blob/main/ADOPT.de.md)"), "does not lead with the page's own action", probe=True)

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


class EveryPage(unittest.TestCase):
    """Three rules every built page keeps: its footer links its language's imprint and privacy notice, none of its elements carries the theme's
    source component, and nothing it loads comes from another host. A site that passes, and controls that each change one thing in it."""

    def checked(self, change=None):
        with tempfile.TemporaryDirectory() as tmp:
            site = Path(tmp) / "site"
            good_site(site)
            for rel, text in (("seats/index.html", '<html lang="en"><body><h1>Seats</h1></body></html>'),
                              ("404.html", '<html lang="en"><body><h1>404</h1></body></html>')):
                (site / rel).parent.mkdir(parents=True, exist_ok=True)
                (site / rel).write_text(text, encoding="utf-8")
            footed(site)
            if change:
                change(site)
            toml = Path(tmp) / "zensical.toml"
            toml.write_text('[project]\nsite_name = "x"\n\n[project.extra]\nprobe = false\n', encoding="utf-8")
            return checked_site(site, toml)

    def put(self, name, old, new):
        def change(site):
            text = (site / name).read_text(encoding="utf-8")
            self.assertIn(old, text)
            (site / name).write_text(text.replace(old, new, 1), encoding="utf-8")
        return change

    def rows(self, passing, refused):
        for name, change in passing:
            with self.subTest(name):
                result = self.checked(change)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        for name, change, message in refused:
            with self.subTest(name):
                result = self.checked(change)
                self.assertNotEqual(result.returncode, 0, "the check passed what it must refuse: " + name)
                self.assertIn(message, result.stderr)

    def test_a_good_site_passes(self):
        result = self.checked()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("site check: each of the 14 pages links its language's imprint and privacy notice in its footer", result.stdout)

    def test_each_footer_links_its_languages_imprint_and_privacy_notice(self):
        self.rows(
            (("root-relative links, as the 404 page writes them", self.put("404.html", footer("404.html"), footer("404.html", ["/imprint.html", "/privacy.html"]))),
             ("the site's own address, and a link with a fragment", self.put("de/signing.html", footer("de/signing.html"),
                                                                             footer("de/signing.html", ["https://shoalmark.tools/de/impressum.html", "datenschutz.html#rechte"])))),
            (("an English page's footer without its privacy link", self.put("setup.html", '<a href="privacy.html">privacy.html</a>', ""), "setup.html lacks privacy.html"),
             ("a German page's footer with the English pair", self.put("de/signing.html", footer("de/signing.html"), footer("de/signing.html", ["../imprint.html", "../privacy.html"])),
              "de/signing.html lacks de/impressum.html, de/datenschutz.html"),
             ("the links outside the footer", self.put("how-it-works.html", footer("how-it-works.html"), footer("how-it-works.html").replace("footer>", "p>")),
              "how-it-works.html lacks imprint.html, privacy.html"),
             ("a page in a folder without its footer", self.put("seats/index.html", footer("seats/index.html"), ""), "seats/index.html lacks imprint.html, privacy.html"),
             ("a link to a page of the same name in the page's own folder", self.put("seats/index.html", '<a href="../privacy.html">', '<a href="privacy.html">'),
              "seats/index.html lacks privacy.html"),
             ("the German landing's footer without the links", self.put("de/index.html", footer("de/index.html"), ""), "de/index.html lacks de/impressum.html, de/datenschutz.html"),
             ("a footer link to another host's imprint", self.put("setup.html", '<a href="imprint.html">', '<a href="https://example.org/imprint.html">'), "setup.html lacks imprint.html"),
             ("the imprint without its own footer", self.put("imprint.html", footer("imprint.html"), ""), "imprint.html lacks imprint.html, privacy.html"),
             ("the German privacy notice not built, and no page linking it", self.unbuilt("de/datenschutz.html"), "missing de/datenschutz.html, which every page's footer links")))

    def unbuilt(self, rel):
        def change(site):
            (site / rel).unlink()
            for page in site.rglob("*.html"):
                text = page.read_text(encoding="utf-8")
                page.write_text(re.sub(r'<a href="[^"]*%s">[^<]*</a>' % re.escape(rel.rsplit("/", 1)[-1]), "", text), encoding="utf-8")
        return change

    def test_no_element_carries_the_source_component(self):
        self.rows(
            (("the repository link drawn without it", self.put("setup.html", "Get", '<a href="https://github.com/shoalmark/shoalmark" title="Go to repository" class="md-source">'
                                                                                   '<div class="md-source__repository">shoalmark/shoalmark</div></a>Get')),
             ("another component", self.put("setup.html", "Get", '<form class="md-header__option" data-md-component="palette"></form>Get')),
             ("its name shown in code", self.put("setup.html", "Get", "<code>data-md-component=&quot;source&quot;</code>Get"))),
            (("double-quoted, on an English page", self.put("setup.html", "Get", '<a class="md-source" data-md-component="source" href="https://github.com/shoalmark/shoalmark">x</a>Get'),
              "setup.html lets the theme's script ask api.github.com"),
             ("single-quoted, on a German page", self.put("de/signing.html", "<footer>", "<a class='md-source' data-md-component='source' href='https://github.com/shoalmark/shoalmark'>x</a><footer>"),
              "de/signing.html lets the theme's script ask api.github.com"),
             ("unquoted, on a page in a folder", self.put("seats/index.html", "<h1>", "<div data-md-component=source></div><h1>"),
              "seats/index.html lets the theme's script ask api.github.com")))

    def test_nothing_loads_from_another_host(self):
        local = ('<img src="assets/a.png" srcset="assets/a.png 1x, /assets/a@2x.png 2x"><img src="data:image/png;base64,AAAA"><svg><use href="#pricke"/></svg>'
                 '<iframe src="about:blank"></iframe><p style="background:url(&quot;data:image/svg+xml;utf8,&lt;svg xmlns=\'http://www.w3.org/2000/svg\'/&gt;&quot;)">x</p>Get')
        elsewhere = ('<a href="https://github.com/shoalmark/shoalmark">repo</a><link rel="canonical" href="https://shoalmark.tools/setup.html">'
                     '<meta http-equiv="refresh" content="0; url=https://github.com/shoalmark/shoalmark/issues/new">Get')
        put = lambda markup: self.put("setup.html", "Get", markup + "Get")
        self.rows(
            (("relative and root-relative loads, a data: image, the mark's own symbol and a blank frame", self.put("setup.html", "Get", local)),
             ("a link, the canonical address and a forward to another host, none of them a load", self.put("setup.html", "Get", elsewhere))),
            (("a script", put('<script src="https://example.org/x.js"></script>'), "setup.html loads https://example.org/x.js (script), from outside the site"),
             ("a stylesheet by a protocol-relative address, its rel capitalised", put('<link rel="Stylesheet" href="//example.org/x.css">'), "loads //example.org/x.css (link)"),
             ("a connection opened ahead", put('<link rel="preconnect" href="https://fonts.example.org">'), "loads https://fonts.example.org (link)"),
             ("an image's second srcset candidate", put('<img src="a.png" srcset="a.png 1x,https://example.org/b.png 2x">'), "loads https://example.org/b.png (img)"),
             ("a picture's source", put('<picture><source srcset="https://example.org/c.webp"><img src="c.png"></picture>'), "loads https://example.org/c.webp (source)"),
             ("a video's poster", put('<video poster="https://example.org/p.jpg"></video>'), "loads https://example.org/p.jpg (video)"),
             ("a frame", put('<frame src="https://example.org/">'), "(frame), from outside the site"),
             ("an iframe whose address a tab splits", put('<iframe src="/&#9;/example.org/"></iframe>'), "(iframe), from outside the site"),
             ("an image addressed with backslashes", put('<img src="\\\\example.org\\x.png">'), "(img), from outside the site"),
             ("an SVG image", put('<svg><image href="https://example.org/i.png"/></svg>'), "loads https://example.org/i.png (image)"),
             ("an SVG symbol from another file", put('<svg><use xlink:href="https://example.org/s.svg#a"/></svg>'), "loads https://example.org/s.svg#a (use)"),
             ("an image button", put('<input type="image" src="https://example.org/go.png">'), "loads https://example.org/go.png (input)"),
             ("a base address", put('<base href="https://example.org/">'), "loads https://example.org/ (base)"),
             ("an image from the site's own host by its absolute address", put('<img src="https://shoalmark.tools/assets/x.png">'), "loads https://shoalmark.tools/assets/x.png (img)"),
             ("a style attribute's background", put('<p style="background:url(https://example.org/a.png)">x</p>'), "setup.html loads a stylesheet resource from outside the site"),
             ("an image-set's second image in a style element", put('<style>body{background:image-set("a.png" 1x, "https://example.org/b.png" 2x)}</style>'),
              "setup.html loads a stylesheet resource from outside the site: https://example.org/b.png"),
             ("an image-set in a stylesheet", lambda site: (site / "stylesheets/x.css").write_text("body{background:-webkit-image-set(url(a.png) 1x, 'https://example.org/b.png' 2x)}"),
              "stylesheets/x.css loads a stylesheet resource from outside the site: https://example.org/b.png"),
             ("an inline module's import", put('<script type="module">import {a} from "https://example.org/m.js";</script>'),
              "an inline script of setup.html imports https://example.org/m.js, from outside the site")))


LLMS = Path(__file__).with_name("llms_txt.py")
FIGURE = ('<figure class="week" markdown="0">\n<div class="week-card"><h3 class="t">FM-024</h3><p class="src">work-tracker/FM-024-….md · 2026-09-28</p>\n'
          '<pre lang="en">next: owner\nask: "x"</pre></div>\n<p class="week-arrow" aria-hidden="true">↓</p>\n'
          '<div class="week-card board"><h3 class="t">board</h3>\n<div class="wk-board" lang="en"><p><i>##</i> <b class="hot">waiting for you: 3</b></p>\n'
          '<p><span class="id">FM-024</span> a question · a ruling <span class="chip">accept</span><span class="chip">reject</span></p></div></div>\n'
          '<p class="week-arrow" aria-hidden="true">↓</p>\n<div class="week-card"><h3 class="t">4127dba</h3><p class="src">git commit</p>\n'
          '<pre lang="en"><span class="del">-next: owner</span>\n<span class="add">+next: build</span></pre></div>\n'
          '<figcaption>One question, a signed commit that sets <code>next</code> to <code>build</code>.</figcaption>\n</figure>')


class Taped(unittest.TestCase):
    """The taped state: the probe switch off and the tape on. The primary button is a taped, aria-disabled button described by its reason line; each control
    changes one thing in a taped site that passes, and the check names it."""

    def taped_site(self, site):
        good_site(site)
        for name, en in (("index.html", True), ("de/index.html", False)):
            note = "https://github.com/shoalmark/shoalmark/blob/main/ADOPT%s.md" % ("" if en else ".de")
            old = '<a class="btn" href="%s">%s</a>' % (note, "Hand your agents the note" if en else "Agenten die Notiz geben")
            new = ('<button type="button" class="btn taped" aria-disabled="true" aria-describedby="taped-why">%s<span class="tape" aria-hidden="true">%s</span></button>'
                   % (LABELS["en" if en else "de"], "not yet" if en else "noch nicht"))
            why = '<p class="taped-why" id="taped-why">%s <a href="%s">%s</a>.</p>' % ("Not open yet. Until then, hand your agents" if en else "Noch nicht offen. Bis dahin geben Sie Ihren Agenten",
                                                                                     note, "the note" if en else "die Notiz")
            text = (site / name).read_text(encoding="utf-8")
            self.assertIn(old, text)
            (site / name).write_text(text.replace(old, new).replace("<footer>", why + "<footer>"), encoding="utf-8")
        for name, old, new in (("how-it-works.html", "Hand your agents the note", LABELS["en"]), ("how-it-works/index.md", "Hand your agents the note", LABELS["en"]),
                               ("de/how-it-works.html", "Agenten die Notiz geben", LABELS["de"]), ("de/how-it-works/index.md", "Agenten die Notiz geben", LABELS["de"])):
            text = (site / name).read_text(encoding="utf-8")       # How it works names the taped button, as the taped state's words do
            self.assertIn(old, text)
            (site / name).write_text(text.replace(old, new), encoding="utf-8")

    def checked(self, change=None, probe=False):
        with tempfile.TemporaryDirectory() as tmp:
            site = Path(tmp) / "site"
            self.taped_site(site)
            if change:
                change(site)
            footed(site)
            toml = Path(tmp) / "zensical-taped.toml"
            toml.write_text("[project]\nsite_name = \"x\"\n\n[project.extra]\nprobe = %s\ntaped = true\n" % ("true" if probe else "false"), encoding="utf-8")
            return subprocess.run([sys.executable, str(CHECKER), str(site), str(toml)], capture_output=True, text=True)

    def edit(self, old, new):
        def change(site):
            text = (site / "index.html").read_text(encoding="utf-8")
            self.assertIn(old, text)
            (site / "index.html").write_text(text.replace(old, new, 1), encoding="utf-8")
        return change

    def test_a_taped_site_passes(self):
        result = self.checked()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_each_control_is_refused(self):
        for name, change, probe, message in (
                ("the tape left off", self.edit('<span class="tape" aria-hidden="true">not yet</span>', ""), False, "carries no tape hidden from screen readers"),
                ("a dialog built", self.edit("<footer>", '<dialog id="probe" aria-labelledby="h"><h2 id="h">x</h2></dialog><footer>'), False, "a dialog is built"),
                ("a click handler on the button", self.edit('aria-disabled="true"', 'aria-disabled="true" onclick="copy()"'), False, "with no id, link or handler"),
                ("a script that handles the button", self.edit("</body>", '<script>document.querySelector(".taped").addEventListener("click", () => 0)</script></body>'), False,
                 "a script handles the taped button"),
                ("aria-describedby missing", self.edit(' aria-describedby="taped-why"', ""), False, "is not described by the line that says why"),
                ("the button a link", self.edit('<button type="button" class="btn taped"', '<a href="https://github.com/shoalmark/shoalmark/blob/main/ADOPT.md" class="btn">x</a><button type="button" class="btn taped"'), False,
                 "does not lead to how-it-works.html alone"),
                ("the switch on with the tape", None, True, "the two exclude each other")):
            with self.subTest(name):
                result = self.checked(change, probe)
                self.assertNotEqual(result.returncode, 0, "the check passed what it must refuse: " + name)
                self.assertIn(message, result.stderr)


class Ceremony(unittest.TestCase):
    """The tape-off ceremony beside the taped state. With the probe on, the primary link is the coin door: its tape and its coin stand in it, hidden from
    screen readers, and the site passes; the taped state's tape, on its taped button, is refused with the probe on, and the ceremony's door is refused with
    the probe off, taped or not."""

    TAPE = {"en": "not yet", "de": "noch nicht"}

    def door(self, lang, href, extra=""):
        return ('<span class="cue" aria-hidden="true"><span class="cue-t was">— x —</span><span class="cue-t now">— y —</span></span>'
                '<a class="btn door"%s href="%s" aria-haspopup="dialog">%s<span class="gcoin" aria-hidden="true"><svg class="cab cab-coin" aria-hidden="true"></svg></span>'
                '<span class="tape" aria-hidden="true">%s</span></a>' % (extra, href, LABELS[lang], self.TAPE[lang]))

    def checked(self, probe, taped=False, change=None):
        with tempfile.TemporaryDirectory() as tmp:
            site = Path(tmp) / "site"
            if taped:
                Taped.taped_site(self, site)
            else:
                good_site(site, probe)
            for name, lang in (("index.html", "en"), ("de/index.html", "de")):
                text = (site / name).read_text(encoding="utf-8")
                if probe:
                    old = '<a class="btn" id="probe-open" href="probe.txt" aria-haspopup="dialog">%s</a>' % LABELS[lang]
                    self.assertIn(old, text)
                    text = text.replace(old, self.door(lang, "probe.txt", ' id="probe-open"'))
                (site / name).write_text(text, encoding="utf-8")
            if change:
                change(site)
            footed(site)
            toml = Path(tmp) / "zensical-ceremony.toml"
            toml.write_text("[project]\nsite_name = \"x\"\n\n[project.extra]\nprobe = %s\ntaped = %s\n" % ("true" if probe else "false", "true" if taped else "false"), encoding="utf-8")
            return subprocess.run([sys.executable, str(CHECKER), str(site), str(toml)], capture_output=True, text=True)

    def put(self, old, new, name="index.html"):
        def change(site):
            text = (site / name).read_text(encoding="utf-8")
            self.assertIn(old, text)
            (site / name).write_text(text.replace(old, new, 1), encoding="utf-8")
        return change

    def test_the_ceremony_with_the_probe_and_the_taped_tape_without_it(self):
        taped_button = '<button type="button" class="btn taped" aria-disabled="true" aria-describedby="taped-why">%s<span class="tape" aria-hidden="true">not yet</span></button>' % LABELS["en"]
        note = '<a class="btn" href="https://github.com/shoalmark/shoalmark/blob/main/ADOPT.md">Hand your agents the note</a>'
        rows = (
            ("the probe build with the ceremony", dict(probe=True), None),
            ("the taped tape beside the door, with the probe on", dict(probe=True, change=self.put('<a class="btn alt"', taped_button + '<a class="btn alt"')),
             "the taped state's tape is built"),
            ("the door's tape moved onto a taped button, with the probe on", dict(probe=True, change=self.put('<span class="tape" aria-hidden="true">not yet</span></a>', '</a>' + taped_button)),
             "the taped state's tape is built"),
            ("the door's tape read by screen readers, with the probe on", dict(probe=True, change=self.put('<span class="tape" aria-hidden="true">not yet</span>', '<span class="tape">not yet</span>')),
             "the ceremony's tape or coin is read by screen readers"),
            ("the ceremony's door with the probe off", dict(probe=False, change=self.put(note, self.door("en", "https://github.com/shoalmark/shoalmark/blob/main/ADOPT.md"))),
             "the probe switch is off, but the tape-off ceremony's door, its coin or its tape is built"),
            ("the ceremony's coin in the taped state", dict(probe=False, taped=True, change=self.put('<span class="tape" aria-hidden="true">not yet</span></button>',
                                                                                                 '<span class="tape" aria-hidden="true">not yet</span><span class="gcoin" aria-hidden="true"></span></button>')),
             "the probe switch is off, but the tape-off ceremony's door, its coin or its tape is built"))
        for name, args, message in rows:
            with self.subTest(name):
                result = self.checked(**args)
                if message is None:
                    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                else:
                    self.assertNotEqual(result.returncode, 0, "the check passed what it must refuse: " + name)
                    self.assertIn(message, result.stderr)


class Twins(unittest.TestCase):
    """llms_txt.py writes each page's Markdown twin as the page reads: includes expanded, the picture as Markdown, links to twins, probe.txt only while the switch is on."""

    def written(self, probe, landing_has_prompt=True, how=None):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        files = {"docs/index.md": "---\ntemplate: landing.html\n---\n# shoalmark\n--8<-- \"start.en.md\"\n[Set up](setup.md)\n",
                 "docs/de/index.md": "---\ntemplate: landing.html\n---\n# shoalmark\n--8<-- \"start.de.md\"\n[Einrichtung](setup.md), [Vertrag](../agents/README.md), [Notiz](https://github.com/shoalmark/shoalmark/blob/main/ADOPT.de.md)\n",
                 "launch/%s/start.en.md" % ("probe" if probe else "interim"): "**[Copy the prompt](https://x.example/probe.txt)**\n" if probe else "**[Hand your agents the note](https://x.example/ADOPT.md)**\n",
                 "launch/%s/start.de.md" % ("probe" if probe else "interim"): "**[Prompt kopieren](https://x.example/de/probe.txt)**\n" if probe else "**[Geben Sie Ihren Agenten die Notiz](https://x.example/ADOPT.de.md)**\n",
                 "docs/how-it-works.md": how or "# How it works\n\n" + FIGURE + "\n\n## Try it\n\n--8<-- \"how-it-works.en.md\"\n\n[Set up](setup.md)\n",
                 "docs/de/how-it-works.md": "# So funktioniert's\n\n--8<-- \"how-it-works.de.md\"\n\n[Einrichtung](setup.md)\n",
                 "docs/setup.md": "# Set up\n", "docs/de/setup.md": "# Einrichtung\n", "docs/agents/README.md": '--8<-- "README.md"\n', "README.md": "# README\n",
                 "launch/%s/how-it-works.en.md" % ("probe" if probe else "interim"): "The button \"Copy the prompt\" copies it.\n" if probe else "The button leads to the note.\n",
                 "launch/%s/how-it-works.de.md" % ("probe" if probe else "interim"): "Der Knopf kopiert.\n" if probe else "Der Knopf führt zur Notiz.\n",
                 "zensical.toml": '[project]\n[project.extra]\nprobe = %s\n[project.markdown_extensions]\npymdownx.snippets.base_path = [".", "launch/%s"]\n' % ("true" if probe else "false", "probe" if probe else "interim"),
                 "site/index.html": '<textarea id="probe-text">Say &quot;no fit&quot;.\nI decide.\n</textarea>' if landing_has_prompt else "<p>no prompt</p>",
                 "site/de/index.html": '<textarea id="probe-text">Sagen Sie „passt nicht“.\n</textarea>' if landing_has_prompt else "<p>no prompt</p>"}
        for name, text in files.items():
            (root / name).parent.mkdir(parents=True, exist_ok=True)
            (root / name).write_text(text, encoding="utf-8", newline="")
        result = subprocess.run([sys.executable, str(LLMS), "site"], cwd=str(root), capture_output=True, text=True)
        return root / "site", result

    def test_a_twin_reads_as_its_page_does(self):
        site, result = self.written(probe=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        twin = (site / "how-it-works/index.md").read_text(encoding="utf-8")
        self.assertIn("The button leads to the note.", twin)
        self.assertNotIn("--8<--", twin)
        self.assertNotRegex(twin, r"</?[a-zA-Z][a-zA-Z0-9]*[\s/>]")
        for wanted in ("**FM-024** · work-tracker/FM-024-….md · 2026-09-28", "```\nnext: owner\nask: \"x\"\n```", "↓", "a ruling [accept] [reject]", "**4127dba** · git commit",
                       "-next: owner\n+next: build", "*One question, a signed commit that sets `next` to `build`.*"):
            self.assertIn(wanted, twin)
        self.assertIn("](../setup/index.md)", twin)
        self.assertIn("](setup/index.md)", (site / "de/index.md").read_text(encoding="utf-8"))
        self.assertIn("](../agents/README/index.md)", (site / "de/index.md").read_text(encoding="utf-8"))
        self.assertIn("https://github.com/shoalmark/shoalmark/blob/main/ADOPT.de.md", (site / "de/index.md").read_text(encoding="utf-8"))
        self.assertIn("](de/how-it-works/index.md)", (site / "llms.txt").read_text(encoding="utf-8"))

    def test_only_the_launch_states_words_are_in_a_twin(self):
        for probe, kept, other in ((False, "leads to the note", "copies it"), (True, "copies it", "leads to the note")):
            with self.subTest(probe=probe):
                site, result = self.written(probe)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn(kept, (site / "how-it-works/index.md").read_text(encoding="utf-8"))
                self.assertNotIn(other, (site / "how-it-works/index.md").read_text(encoding="utf-8"))
                start, other_start = (("ADOPT.md", "probe.txt"), ("probe.txt", "ADOPT.md"))[probe]
                self.assertIn("](https://x.example/" + start + ")", (site / "index.md").read_text(encoding="utf-8"))
                self.assertNotIn(other_start, (site / "index.md").read_text(encoding="utf-8"))
                self.assertIn(start.replace("ADOPT.md", "ADOPT.de.md").replace("probe.txt", "de/probe.txt"), (site / "de/index.md").read_text(encoding="utf-8"))

    def test_probe_txt_is_the_prompt_the_dialog_shows_and_only_while_the_switch_is_on(self):
        site, result = self.written(probe=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse((site / "probe.txt").exists() or (site / "de/probe.txt").exists())
        site, result = self.written(probe=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((site / "probe.txt").read_bytes(), 'Say "no fit".\nI decide.\n'.encode("utf-8"))
        self.assertEqual((site / "de/probe.txt").read_bytes(), "Sagen Sie „passt nicht“.\n".encode("utf-8"))
        site, result = self.written(probe=True, landing_has_prompt=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("shows no prompt", result.stderr)

    def test_the_controls_see_what_they_refuse(self):
        """The twin's check would pass a twin that still carried the picture's HTML, an include or a state fence if the twin could: here it does."""
        site, result = self.written(probe=False, how="# How it works\n\n<figure class=\"week-x\"><pre>next</pre></figure>\n\n--8<-- \"how-it-works.en.md\"\n")
        self.assertEqual(result.returncode, 0, result.stderr)
        twin = (site / "how-it-works/index.md").read_text(encoding="utf-8")
        self.assertRegex(twin, r"</?[a-zA-Z][a-zA-Z0-9]*[\s/>]")
        site, result = self.written(probe=False, how='# How it works\n\n--8<-- "missing.md"\n')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("none of the snippet base paths", result.stderr)


# a fenced block in a list item, one with a blank line inside, inline code that holds a fence, a German page with a block in a blockquote and one in a list
# inside it, a block an include brings in from the second folder of the snippets' base path, and one each through snippets' block form, a line range and a
# section of a file that holds a block outside both; that file also included whole, with section markers inside its blocks, escaped and not
FENCED_DOCS = {
    "signing.md": "# Signing\n\n1. Turn it on:\n\n    ```\n    git config gpg.format ssh\n    git config user.signingkey ~/.ssh/signing.pub\n    ```\n\n"
                  "2. Name your seats:\n\n```toml\n[seats]\n\nplanner = \"planner@seat\"\n```\n\nWrite ` ``` ` to open a block.\n",
    "de/signing.md": "# Signieren\n\n```\ngit config gpg.format ssh\ngit config user.signingkey ~/.ssh/signing.pub\n```\n\n"
                     "> Prüfen:\n>\n> ```\n> git status\n> ```\n>\n> - In einer Liste:\n>\n>     ```\n>     git log -1\n>     ```\n",
    "agents/README.md": '--8<-- "README.md"\n',
    "names.md": "# Names\n\n--8<--\nnames-a.md\n--8<--\n",
    "range.md": '# Range\n\n--8<-- "inc.md:3:5"\n',
    "section.md": '# Section\n\n--8<-- "inc.md:example"\n',
    "whole.md": '# Whole\n\n--8<-- "inc.md"\n',
}
FENCED_INCLUDED = {"launch/x/README.md": "# README\n\n~~~bash\nshoalmark --next\n~~~\n", "launch/x/names-a.md": "~~~\nseats: 3\n~~~\n",
                   "inc.md": "# Inc\n\n```\ninc line\n```\n\n--8<-- [start:example]\n~~~\nsection line\n--8<-- [start:other]\n;--8<-- [end:x]\n~~~\n--8<-- [end:example]\n\n```\nneither\n--8<-- [end:other]\n;--8<-- [start:y]\n```\n"}
TWO_LINES = '<div class="highlight"><pre><span></span><code>git config gpg.format ssh\ngit config user.signingkey ~/.ssh/signing.pub\n</code></pre></div>'
SEATS = ('<div class="highlight"><pre><span></span><code><span class="k">[seats]</span>\n\n<span class="n">planner</span><span class="w"> </span>=<span class="w"> </span>'
         '<span class="s2">"planner@seat"</span>\n</code></pre></div>')
NEXT = '<div class="highlight"><pre><span></span><code>shoalmark<span class="w"> </span>--next\n</code></pre></div>'
PRE = '<div class="highlight"><pre><span></span><code>%s\n</code></pre></div>'
STATUS, LOG, SEATS3, INC, SECTION, NEITHER = (PRE % "git status", PRE % "git log -1", PRE % "seats: 3", PRE % "inc line", PRE % "section line\n--8<-- [end:x]",
                                              PRE % "neither\n--8<-- [start:y]")
FENCED_PAGES = {
    "signing.html": ('<html lang="en"><body><h1 id="signing">Signing</h1><ol><li><p>Turn it on:</p>' + TWO_LINES + '</li><li><p>Name your seats:</p></li></ol>'
                     + SEATS + "<p>Write <code>```</code> to open a block.</p></body></html>"),
    "de/signing.html": ('<html lang="de"><body><h1 id="signieren">Signieren</h1>' + TWO_LINES + "<blockquote><p>Prüfen:</p>" + STATUS
                        + "<ul><li><p>In einer Liste:</p>" + LOG + "</li></ul></blockquote></body></html>"),
    "agents/index.html": "Get a better-performing human Owner." + NEXT,
    "names.html": '<html lang="en"><body><h1 id="names">Names</h1>' + SEATS3 + "</body></html>",
    "range.html": '<html lang="en"><body><h1 id="range">Range</h1>' + INC + "</body></html>",
    "section.html": '<html lang="en"><body><h1 id="section">Section</h1>' + SECTION + "</body></html>",
    "whole.html": '<html lang="en"><body><h1 id="whole">Whole</h1>' + INC + SECTION + NEITHER + "</body></html>",
}
# snippets' escape: an include marker after `;` is text, shown with one `;` taken off, at the top level and inside a block of names
ESCAPED = {"docs/escaped.md": '# Escaped\n\n```\n;--8<-- "inc.md"\n;--8<--\n```\n',
           "docs/escaped-names.md": '# Escaped names\n\n--8<--\nopen.md\n;--8<-- "inc.md"\nclose.md\n--8<--\n',
           "launch/x/open.md": "```\n", "launch/x/close.md": "```\n",
           "site/escaped.html": '<html lang="en"><body><h1 id="escaped">Escaped</h1>' + PRE % '--8<-- "inc.md"\n--8<--' + "</body></html>",
           "site/escaped-names.html": '<html lang="en"><body><h1 id="escaped-names">Escaped names</h1>' + PRE % '--8<-- "inc.md"' + "</body></html>"}


class FencedBlocks(unittest.TestCase):
    """Fenced code: each fenced block of the docs, and of what an include brings in, builds to a <pre> that holds its text, and no built page shows a fence
    as text, in English and in German. The docs folder, the snippets' base path and the pages' addresses are read from zensical.toml. Each control changes
    one thing in a site that passes, and the check names the page."""

    def checked(self, change=None, docs="docs", named="docs", bases='[".", "launch/x"]'):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            site = root / "site"
            good_site(site)
            for name, text in [*((docs + "/" + n, t) for n, t in FENCED_DOCS.items()), *FENCED_INCLUDED.items(), *(("site/" + n, t) for n, t in FENCED_PAGES.items())]:
                (root / name).parent.mkdir(parents=True, exist_ok=True)
                (root / name).write_text(text, encoding="utf-8")
            if change:
                change(site)
            footed(site)
            toml = root / "zensical-fenced.toml"
            toml.write_text('[project]\nsite_name = "x"\ndocs_dir = "%s"\nuse_directory_urls = false\n\n[project.extra]\nprobe = false\n\n'
                            "[project.markdown_extensions]\npymdownx.superfences = {}\npymdownx.snippets.base_path = %s\n" % (named, bases), encoding="utf-8")
            return subprocess.run([sys.executable, str(CHECKER), str(site), str(toml)], capture_output=True, text=True)

    def put(self, name, old, new):
        def change(site):
            text = (site / name).read_text(encoding="utf-8")
            self.assertIn(old, text)
            (site / name).write_text(text.replace(old, new, 1), encoding="utf-8")
        return change

    def test_a_good_site_passes(self):
        for docs in ("docs", "pages"):
            with self.subTest(docs=docs):
                result = self.checked(docs=docs, named=docs)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertIn("the 12 fenced block(s) of the docs, in both languages, build to code blocks", result.stdout)

    def test_an_escaped_include_marker_is_text(self):
        def add(site):
            for name, text in ESCAPED.items():
                (site.parent / name).parent.mkdir(parents=True, exist_ok=True)
                (site.parent / name).write_text(text, encoding="utf-8")
        result = self.checked(change=add)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("the 14 fenced block(s) of the docs, in both languages, build to code blocks", result.stdout)

    def test_each_control_is_refused(self):
        collapsed = "<p><code>git config gpg.format ssh\ngit config user.signingkey ~/.ssh/signing.pub</code></p>"
        rows = (
            ("an English block built as inline code in a paragraph", dict(change=self.put("signing.html", TWO_LINES, collapsed)),
             ["signing.html: 1 fenced block(s) do not build to a code block, the first opening 'git config gpg.format ssh'"]),
            ("a German block built as inline code in a paragraph", dict(change=self.put("de/signing.html", TWO_LINES, collapsed)),
             ["de/signing.html: 1 fenced block(s) do not build to a code block, the first opening 'git config gpg.format ssh'"]),
            ("an English block split at its blank line, a fence shown in each half",
             dict(change=self.put("signing.html", SEATS, '<p>```toml\n[seats]</p>\n<p>planner = "planner@seat"\n```</p>')),
             ["signing.html: 1 fenced block(s) do not build to a code block, the first opening '[seats]'", "signing.html shows a fence as text: '```toml [seats]'"]),
            ("an English fence shown as a heading, every block built", dict(change=self.put("signing.html", "</body>", '<h2 id="yaml">```yaml</h2></body>')),
             ["signing.html shows a fence as text: '```yaml'"]),
            ("a German fence shown as text, every block built", dict(change=self.put("de/signing.html", "</body>", "<p>~~~</p></body>")),
             ["de/signing.html shows a fence as text: '~~~'"]),
            ("a German block's text cut short in its code block", dict(change=self.put("de/signing.html", "ssh\ngit config user.signingkey ~/.ssh/signing.pub\n", "ssh\n")),
             ["de/signing.html: 1 fenced block(s) do not build to a code block"]),
            ("the included block not built", dict(change=self.put("agents/index.html", NEXT, "<p><code>bash\nshoalmark --next</code></p>")),
             ["agents/index.html: 1 fenced block(s) do not build to a code block, the first opening 'shoalmark --next'"]),
            ("the included file in no folder of the base path zensical.toml names", dict(bases='["."]'),
             ["includes README.md, which none of the snippets' base paths"]),
            ("the docs folder zensical.toml names holds no page", dict(docs="pages", named="docs-elsewhere"), ["docs_dir", "holds no page"]),
            ("the docs read from the folder zensical.toml names, a block there not built", dict(docs="pages", named="pages", change=self.put("signing.html", TWO_LINES, collapsed)),
             ["signing.html: 1 fenced block(s) do not build to a code block"]),
            ("a German block in a blockquote built as inline code in it", dict(change=self.put("de/signing.html", STATUS, "<p><code>git status</code></p>")),
             ["de/signing.html: 1 fenced block(s) do not build to a code block, the first opening 'git status'"]),
            ("a German block in a list inside a blockquote built as inline code", dict(change=self.put("de/signing.html", LOG, "<p><code>git log -1</code></p>")),
             ["de/signing.html: 1 fenced block(s) do not build to a code block, the first opening 'git log -1'"]),
            ("the block the include's block form brings in not built", dict(change=self.put("names.html", SEATS3, "<p><code>seats: 3</code></p>")),
             ["names.html: 1 fenced block(s) do not build to a code block, the first opening 'seats: 3'"]),
            ("the block a line range brings in not built", dict(change=self.put("range.html", INC, "<p><code>inc line</code></p>")),
             ["range.html: 1 fenced block(s) do not build to a code block, the first opening 'inc line'"]),
            ("the block a section brings in not built", dict(change=self.put("section.html", SECTION, "<p><code>section line</code></p>")),
             ["section.html: 1 fenced block(s) do not build to a code block, the first opening 'section line'"]),
            ("a section the file does not hold", dict(change=self.put("../docs/section.md", "inc.md:example", "inc.md:absent")),
             ["section.md includes inc.md:absent, and that file holds no section absent"]),
            ("the whole file's blocks not built", dict(change=self.put("whole.html", NEITHER, "<p><code>neither\n--8<-- [start:y]</code></p>")),
             ["whole.html: 1 fenced block(s) do not build to a code block, the first opening 'neither'"]),
        )
        for name, args, messages in rows:
            with self.subTest(name):
                result = self.checked(**args)
                self.assertNotEqual(result.returncode, 0, "the check passed what it must refuse: " + name)
                for message in messages:
                    self.assertIn(message, result.stderr)


if __name__ == "__main__":
    unittest.main()
