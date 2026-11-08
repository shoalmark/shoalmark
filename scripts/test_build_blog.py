"""The blog's builder, scripts/build_blog.py: what it emits from the repository's blog/, and what it refuses.

Run: python3 scripts/test_build_blog.py. Each test copies what the builder reads (blog/, the four font subsets and their licences, the mark,
main.html and the builder itself) into a scratch root, changes one thing where it tests a refusal, and runs the builder there."""
import hashlib
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
READS = ["blog", "docs/assets/fonts", "overrides/.icons/shoalmark/pricke.svg", "overrides/main.html", "scripts/build_blog.py"]


def scratch(tmp):
    root = Path(tmp) / "repo"
    for rel in READS:
        src, dst = ROOT / rel, root / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        (shutil.copytree if src.is_dir() else shutil.copyfile)(src, dst)
    return root


def build(root):
    return subprocess.run([sys.executable, str(root / "scripts/build_blog.py"), str(root / "site")], capture_output=True, text=True, encoding="utf-8")


class Built(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.root = scratch(cls.tmp.name)
        cls.result = build(cls.root)
        cls.blog = cls.root / "site/blog"
        cls.page = (cls.blog / "hail-1.html").read_text(encoding="utf-8") if cls.result.returncode == 0 else ""

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_it_builds(self):
        self.assertEqual(self.result.returncode, 0, self.result.stderr)

    def test_the_tree(self):
        want = {"index.html", "hail-1.html", "hail-1.md", "feed.xml", "llms.txt", "assets/blog.css", "assets/blog.js", "fonts/mono-400.woff2",
                "fonts/mono-600.woff2", "fonts/pixel-400.woff2", "fonts/pixel-700.woff2", "fonts/OFL.txt", "fonts/OFL-pixel.txt"}
        got = {p.relative_to(self.blog).as_posix() for p in self.blog.rglob("*") if p.is_file() and not p.relative_to(self.blog).as_posix().startswith("hail-1/")}
        self.assertEqual(got, want)

    def test_the_posts_files_are_its_sources(self):
        src = sorted(p.name for p in (ROOT / "blog/posts/hail-1").iterdir())
        self.assertEqual(sorted(p.name for p in (self.blog / "hail-1").iterdir()), src)
        self.assertEqual(len(src), 60)
        for name in src:
            self.assertEqual((self.blog / "hail-1" / name).read_bytes(), (ROOT / "blog/posts/hail-1" / name).read_bytes(), name)

    def test_the_fonts_are_the_sites_own_under_neutral_names(self):
        for name, neutral in (("IBM-Plex-Mono-normal-400-latin.woff2", "mono-400.woff2"), ("Silkscreen-normal-700-latin.woff2", "pixel-700.woff2"),
                              ("silkscreen-OFL.txt", "OFL-pixel.txt")):
            self.assertEqual((self.blog / "fonts" / neutral).read_bytes(), (ROOT / "docs/assets/fonts" / name).read_bytes())
        self.assertNotRegex((self.blog / "assets/blog.css").read_text(encoding="utf-8"), r"(?i)plex|silkscreen")

    def test_the_stylesheet_is_base_then_m2(self):
        self.assertEqual((self.blog / "assets/blog.css").read_text(encoding="utf-8"),
                         (ROOT / "blog/css/base.css").read_text(encoding="utf-8") + "\n" + (ROOT / "blog/css/m2.css").read_text(encoding="utf-8"))

    def test_the_title_draws_its_wordmark(self):
        h1 = re.search(r"<h1>(.*?)</h1>", self.page, re.S).group(1)
        self.assertEqual(h1, '<span><span class="hf">hail/1</span>: agents message each other;</span> <span>the final word stays yours</span>')
        self.assertIn("<title>⌜hail/1⌟: agents message each other; the final word stays yours</title>", self.page)

    def test_the_head_and_the_words(self):
        for s in ('<span class="label">PROTOCOL</span>', '<p class="dek">A small protocol for agent seats: one frame, seven messages, four receipts, no authority.</p>',
                  "<span>8 min read</span>", '<a href="hail-1.md" type="text/markdown">read as Markdown</a>', '<nav class="toc" aria-label="on this page">',
                  '<a href="index.html">← all posts</a>', '<a href="feed.xml" type="application/rss+xml">RSS</a>',
                  '<h2 class="ct" id="credits-t">Authors &amp; acknowledgements</h2>', '<meta property="og:video:type" content="video/mp4">',
                  '<meta property="og:image" content="https://shoalmark.tools/blog/hail-1/card.png">', '<link rel="canonical" href="https://shoalmark.tools/blog/hail-1.html">'):
            self.assertIn(s, self.page)
        self.assertEqual(self.page.count('<aside class="credits"'), 1)
        self.assertEqual(len(re.findall(r'<aside class="credits".*?</aside>', self.page, re.S)[0].split("<p>")) - 1, 5)

    def test_the_four_touches(self):
        anchors = re.findall(r'<(h[23]) id="([^"]+)"><a class="hm" href="#\2" aria-hidden="true" tabindex="-1"></a>', self.page)
        self.assertEqual(len(anchors), len(re.findall(r'<h[23] id="', self.page)))
        self.assertEqual(len(anchors), 16)
        self.assertEqual(len(re.findall(r'data-label="hail · [A-Z]+"', self.page)), 10)
        self.assertRegex(self.page, r'</section>\n<aside class="credits"')
        self.assertRegex(self.page, r'<p class="foot">.*?</p>\n<nav class="end" aria-label="blog">')

    def test_the_contents_leave_out_the_tab_and_the_credits(self):
        toc = re.search(r'<nav class="toc"[^>]*>(.*?)</nav>', self.page, re.S).group(1)
        self.assertNotIn("#tldr", toc)
        self.assertNotIn("#credits-t", toc)
        self.assertEqual(toc.count("<a href="), 16)

    def test_no_inline_script(self):
        self.assertEqual(re.findall(r"<script(?![^>]*\bsrc=)", self.page), [])

    def test_the_markdown_version(self):
        md = (self.blog / "hail-1.md").read_text(encoding="utf-8")
        self.assertTrue(md.startswith('---\ntitle: "⌜hail/1⌟: agents message each other; the final word stays yours"\ndate: 2026-11-08\n'))
        self.assertNotIn("<!--", md)
        self.assertEqual(len(re.findall(r"^!\[[^\]]+\]\(hail-1/[a-z0-9-]+\.png\)$", md, re.M)), 15)
        self.assertIn("(https://shoalmark.tools/why-shoalmark.html)", md)

    def test_the_feed_and_llms(self):
        feed = (self.blog / "feed.xml").read_text(encoding="utf-8")
        self.assertIn("<title>shoalmark blog</title>", feed)
        self.assertIn("<guid>https://shoalmark.tools/blog/hail-1.html</guid>", feed)
        self.assertIn("<pubDate>Sun, 08 Nov 2026 00:00:00 +0100</pubDate>", feed)
        self.assertTrue((self.blog / "llms.txt").read_text(encoding="utf-8").startswith("# shoalmark blog\n\n> How I build shoalmark with my agents"))


class Refuses(unittest.TestCase):
    """Each control changes one thing the builder reads, and the builder refuses it, naming why."""

    def refused(self, change, reason):
        with tempfile.TemporaryDirectory() as tmp:
            root = scratch(tmp)
            change(root)
            r = build(root)
            self.assertNotEqual(r.returncode, 0, "the builder built what it must refuse")
            self.assertIn(reason, r.stderr)

    def edit(self, rel, old, new):
        def change(root):
            text = (root / rel).read_text(encoding="utf-8")
            self.assertIn(old, text)
            (root / rel).write_text(text.replace(old, new, 1), encoding="utf-8")
        return change

    def test_each_control(self):
        post, hails = "blog/posts/hail-1.md", "blog/posts/hail-1.hails.html"
        for name, change, reason in (
                ("a front matter without its dek", self.edit(post, 'dek: "', 'deck: "'), "its front matter has no dek"),
                ("a slug that is not the file's name", self.edit(post, "slug: hail-1", "slug: hail-2"), "is not its file's name"),
                ("a title that is not the post's # line", self.edit(post, 'title: "⌜hail/1⌟: agents', 'title: "⌜hail/1⌟: seats'), "its # line is not the title"),
                ("a hail at a place the post does not have", self.edit(hails, "<!-- after F13 -->", "<!-- after F99 -->"), "do not match its files"),
                ("the reference's hail not its fence", self.edit(post, "Work in your own worktree.", "Work in a worktree."), "the reference's fence is not its hail"),
                ("a mark the blog does not carry", self.edit(post, "A missing first response", "A *missing* first response"), "a mark the blog does not carry"),
                ("the band's link without its placeholder", self.edit(post, "(‹link: spec›)", "(spec.html)"), "does not open with the spec's link"),
                ("a font of another subset", lambda root: shutil.copyfile(root / "docs/assets/fonts/IBM-Plex-Mono-normal-400-latin-ext.woff2",
                                                                         root / "docs/assets/fonts/IBM-Plex-Mono-normal-400-latin.woff2"), "is not the latin subset"),
                ("a figure with no entry", self.edit("blog/posts/hail-1.figures.json", '"F15"', '"F16"'), "F15 has no entry"),
                ("site/blog already there", lambda root: (root / "site/blog").mkdir(parents=True), "is already there"),
                ("a template's slot with no value", self.edit("blog/templates/post.html", "{{ dek }}", "{{ deck }}"), "no value for deck")):
            with self.subTest(name):
                self.refused(change, reason)


if __name__ == "__main__":
    unittest.main()
