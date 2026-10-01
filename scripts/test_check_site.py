"""Regression controls for published font sources; run with requirements-docs installed."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

CHECKER = Path(__file__).with_name("check_site.py")


class FontSources(unittest.TestCase):
    def check(self, css, expected, inline=False, imported=False):
        with tempfile.TemporaryDirectory() as tmp:
            site = Path(tmp)
            for name in ("index.html", "setup.html", "signing.html", "de/signing.html", "agents/index.html", "llms.txt"):
                p = site / name
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text("Get a better-performing human Owner.")
            (site / "font").write_bytes(b"synthetic local asset")
            (site / "font.woff2").write_bytes(b"synthetic local asset")
            if inline:
                (site / "index.html").write_text("<style>" + css + "</style>")
            elif imported:
                (site / "style.css").write_text('@import "nested";')
                (site / "nested").write_text(css)
            else:
                (site / "style.css").write_text(css)
            result = subprocess.run([sys.executable, str(CHECKER), str(site)], capture_output=True, text=True)
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


if __name__ == "__main__":
    unittest.main()
