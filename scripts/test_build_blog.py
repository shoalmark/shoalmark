"""The blog's builder, scripts/build_blog.py: what it emits from the repository's blog/, and what it refuses.

Run: python3 scripts/test_build_blog.py. Each test copies what the builder reads (blog/, the four font subsets and their licences, the mark,
main.html, the seats' icons and the builder itself) into a scratch root, changes one thing where it tests a refusal, and runs the builder there."""
import datetime
import hashlib
import html
import json
import importlib.util
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

ROOT = Path(__file__).resolve().parent.parent
READS = ["blog", "docs/assets/fonts", "overrides/.icons/shoalmark/pricke.svg", "overrides/main.html", "brand/seats", "scripts/build_blog.py"]
SEATS = ["go-to-market", "designer", "planner", "builder", "reviewer", "auditor"]
CANONICAL = "https://shoalmark.tools/blog/hail-1.html"
_spec = importlib.util.spec_from_file_location("build_blog", ROOT / "scripts/build_blog.py")
BB = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(BB)
DATE = re.search(r"^date: (\S+)$", (ROOT / "blog/posts/hail-1.md").read_text(encoding="utf-8"), re.M).group(1)
AFTER = lambda days: (datetime.date.fromisoformat(DATE) + datetime.timedelta(days=days)).isoformat()      # a day after the post's own, never tied with it
READ_IT = re.search(r"^- \*\*Read it:\*\* .+$", (ROOT / "blog/posts/hail-1.md").read_text(encoding="utf-8"), re.M).group(0)   # the band, as the post writes it


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
                "fonts/mono-600.woff2", "fonts/pixel-400.woff2", "fonts/pixel-700.woff2", "fonts/OFL.txt", "fonts/OFL-pixel.txt",
                "assets/authors/owner.jpg", "assets/authors/owner-52.jpg"} | {f"assets/seats/{k}.svg" for k in SEATS}
        got = {p.relative_to(self.blog).as_posix() for p in self.blog.rglob("*") if p.is_file() and not p.relative_to(self.blog).as_posix().startswith("hail-1/")}
        self.assertEqual(got, want)

    def test_the_posts_files_are_its_sources(self):
        src = sorted(p.name for p in (ROOT / "blog/posts/hail-1").iterdir())
        self.assertEqual(sorted(p.name for p in (self.blog / "hail-1").iterdir()), src)
        self.assertEqual(len(src), 129)
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
        for s in ('<span class="label">PROTOCOL</span>', '<p class="dek">A small protocol for agent seats: they hail each other, and asks only you can answer come to you.</p>',
                  "<span>12 min read</span>", '<a href="hail-1.md" type="text/markdown">read as Markdown</a>', '<nav class="toc" aria-label="on this page">',
                  '<a href="index.html">← all posts</a>', '<a href="feed.xml" type="application/rss+xml">RSS</a>',
                  '<h2 class="ct" id="credits-t">Acknowledgements</h2>', '<meta property="og:video:type" content="video/mp4">',
                  '<meta property="og:image" content="https://shoalmark.tools/blog/hail-1/card.png">', '<link rel="canonical" href="https://shoalmark.tools/blog/hail-1.html">'):
            self.assertIn(s, self.page)
        self.assertEqual(self.page.count('<aside class="credits"'), 1)
        box = re.findall(r'<aside class="credits".*?</aside>', self.page, re.S)[0]
        self.assertEqual(len(box.split("<p>")) - 1, 6)
        self.assertIn('<p>Article fact review: an independent reviewer, in <span class="nw">twenty-two</span> rounds, with design and reader critiques.</p>', box)
        self.assertTrue(box.endswith("<p>With thanks to the Research seat.</p></aside>"))

    def test_two_places_kept_whole_on_their_line(self):
        """The post's "every failure." keeps its two words together through the one no-break space in its source, U+00A0 itself, which the page
        and the Markdown version carry; the credits' "twenty-two" stays whole in the one wrap the credits have, its hyphen plain."""
        source = (ROOT / "blog/posts/hail-1.md").read_text(encoding="utf-8")
        md = (self.blog / "hail-1.md").read_text(encoding="utf-8")
        self.assertEqual(source.count(" "), 1)
        self.assertIn("tokens and every failure.\n", source)
        self.assertRegex(self.page, "tokens and every( |&nbsp;)failure\\.")
        self.assertNotIn("every failure", self.page + md)
        self.assertIn("tokens and every failure.\n", md)
        self.assertNotIn("&nbsp;", md)
        box = re.findall(r'<aside class="credits".*?</aside>', self.page, re.S)[0]
        self.assertEqual(re.findall(r'<span class="nw">(.*?)</span>', box), ["twenty-two"])
        self.assertEqual(box.count("<span"), 1)
        self.assertIn('in twenty-two rounds', source)                      # the credits are front matter: the Markdown version doesn't carry them
        for name, text in (("the source", source), ("the page", self.page), ("the Markdown version", md)):
            self.assertNotRegex(text, "[‑⁠]", name)

    def test_the_four_touches(self):
        anchors = re.findall(r'<(h[23]) id="([^"]+)"><a class="hm" href="#\2" aria-hidden="true" tabindex="-1"></a>', self.page)
        self.assertEqual(len(anchors), len(re.findall(r'<h[23] id="', self.page)))
        self.assertEqual(len(anchors), 17)
        self.assertEqual(len(re.findall(r'data-label="hail · [A-Z]+"', self.page)), 10)
        self.assertRegex(self.page, r'<section class="ending".*?</section>\n<section class="written".*?</section>\n    <div class="share share-end">.*?'
                                    r'</span></div>\n<aside class="credits"')
        self.assertRegex(self.page, r'<p class="foot">.*?</p>\n<nav class="end" aria-label="blog">')

    def test_the_contents_leave_out_the_tab_and_the_credits(self):
        toc = re.search(r'<nav class="toc"[^>]*>(.*?)</nav>', self.page, re.S).group(1)
        self.assertNotIn("#tldr", toc)
        self.assertNotIn("#credits-t", toc)
        self.assertNotIn("#written-t", toc)
        self.assertEqual(toc.count("<a href="), 17)
        self.assertIn('<li><a href="#who-decides">Who decides</a></li><li><a href="#when-a-seat-needs-you">When a seat needs you</a></li>', toc)

    def test_the_authors_in_the_head_and_at_the_end(self):
        head = re.search(r'<p class="meta">.*?</p>\n    <div class="by">(.*?)</div>\n  </header>', self.page, re.S)
        end = re.search(r'<section class="written" aria-labelledby="written-t"><h2 class="wt" id="written-t">Written by</h2><ul>(.*?)</ul></section>', self.page)
        self.assertTrue(head and end)
        roles = [("@holgo99", "Owner"), ("Go-to-market", "Drafted the words"), ("Designer", "Figures and page design"), ("Planner", "Runs the blog lane"),
                 ("Builder", "Builds the blog"), ("Reviewer", "Independent fact review"), ("Auditor", "Drafted the spec")]
        for part, size in ((head.group(1), (48, 40)), (end.group(1), (60, 60))):
            self.assertEqual(re.findall(r"<b>([^<]+)</b><i>([^<]+)</i>", part), roles)
            self.assertEqual(re.findall(r'<img src="(assets/[^"]+)" width="(\d+)"', part),
                             [("assets/authors/owner.jpg", str(size[0]))] + [(f"assets/seats/{k}.svg", str(size[1])) for k in SEATS])
            self.assertEqual(part.count('href="https://x.com/holgo99"'), 1)

    def test_every_author_picture_has_an_empty_alt(self):
        pictures = re.findall(r'<img src="assets/(?:authors|seats)/[^"]+"[^>]*>', self.page)
        self.assertEqual(len(pictures), 14)
        for img in pictures:
            self.assertEqual(re.findall(r'\balt="([^"]*)"', img), [""], img)

    def test_the_authors_pictures_are_their_sources(self):
        self.assertEqual((self.blog / "assets/authors/owner.jpg").read_bytes(), (ROOT / "blog/authors/owner.jpg").read_bytes())
        for k in SEATS:
            self.assertEqual((self.blog / f"assets/seats/{k}.svg").read_bytes(), (ROOT / f"brand/seats/{k}.svg").read_bytes(), k)

    def test_the_card_and_the_video_in_the_head_and_the_hero(self):
        alt = re.search(r'^card_alt: "(.*)"$', (ROOT / "blog/posts/hail-1.md").read_text(encoding="utf-8"), re.M).group(1).replace("\\\"", '"')
        shown = alt.replace("&", "&amp;").replace('"', "&quot;").replace("'", "&#x27;")
        for s in (f'<meta property="og:image:alt" content="{shown}">', f'<meta name="twitter:image:alt" content="{shown}">', f'aria-label="{shown}"><source',
                  '<meta property="og:image" content="https://shoalmark.tools/blog/hail-1/card.png">', '<meta property="og:image:width" content="1200">',
                  '<meta property="og:video" content="https://shoalmark.tools/blog/hail-1/hail-1.mp4">', '<meta property="og:video:type" content="video/mp4">',
                  '<meta property="og:video:width" content="1200">', '<meta property="og:video:height" content="630">',
                  'poster="hail-1/card.png"'):
            self.assertIn(s, self.page)

    def test_each_figures_webp_twins(self):
        pictures = re.findall(r"<picture>(.*?)</picture>", self.page)
        self.assertEqual(len(pictures), 16)
        twins = 0
        for pic in pictures:
            tags = re.findall(r"<(?:source|img) [^>]*>", pic)
            self.assertEqual(len(tags) % 2, 0, pic[:120])
            for twin, tag in zip(tags[::2], tags[1::2]):
                twins += 1
                self.assertTrue(twin.startswith('<source type="image/webp" '), twin)
                self.assertNotIn('type="image/webp"', tag)
                want = re.sub(r'(hail-1/[A-Za-z0-9._-]+)\.(?:png|gif)"', r'\1.webp"', tag)
                if tag.startswith("<source "):
                    self.assertEqual(twin, want.replace("<source ", '<source type="image/webp" ', 1))
                else:
                    a = dict(re.findall(r'([\w-]+)="([^"]*)"', want))
                    self.assertEqual(twin, f'<source type="image/webp" srcset="{a["src"]}"'
                                     + "".join(f' {k}="{a[k]}"' for k in ("width", "height", "data-still", "data-once", "data-ms") if k in a) + ">")
                for name in re.findall(r'hail-1/([A-Za-z0-9._-]+\.webp)"', twin):
                    self.assertTrue((self.blog / "hail-1" / name).is_file(), name)
        self.assertEqual(twins, 62)
        imgs = re.findall(r"<picture>.*?(<img [^>]*>)</picture>", self.page)
        self.assertEqual([re.search(r'loading="(\w+)"', i).group(1) for i in imgs], ["eager"] + ["lazy"] * 15)
        self.assertTrue(all(re.search(r'src="hail-1/[^"]+\.png"', i) for i in imgs))
        self.assertNotRegex(" ".join(imgs), r"\.webp")

    def test_the_figures_in_the_posts_order(self):
        """The figures stand as the post reads its slots, F16's after F13's. Each figure is found by its slot, through the file its <img> shows: its
        alt is its slot's, its sizes are its files', F13's and F16's as drawn, and each play time, in its twin too, is its slot's, the phone's on
        the narrow source and the desktop's on the <img>."""
        figures = json.loads((ROOT / "blog/posts/hail-1.figures.json").read_text(encoding="utf-8"))
        slot_of = {name: key for key, f in figures.items() for name in f.get("stills", [f.get("name", "") + "-780-still.png"])}
        figs = re.findall(r'<figure id="f\d+">(.*?)</figure>', self.page)
        slots = []
        for fig in figs:
            img = re.search(r'<img src="hail-1/([^"]+)"[^>]*\balt="([^"]*)"', fig)
            key = slot_of[img.group(1)]
            slots.append(key)
            self.assertEqual(html.unescape(img.group(2)), figures[key]["alt"], key)
            ms = figures[key].get("ms")
            self.assertEqual([int(m) for m in re.findall(r'data-ms="(\d+)"', fig)], [ms[0], ms[0], ms[1], ms[1]] if ms else [], key)
        self.assertEqual(slots, [f"F{n}" for n in [*range(1, 14), 16, 14, 15]])
        for key, (narrow, wide) in (("F13", ((1092, 1140), (1572, 1076))), ("F16", ((1092, 1712), (1572, 1556)))):
            sizes = [tuple(map(int, s)) for s in re.findall(r'width="(\d+)" height="(\d+)"', figs[slots.index(key)])]
            self.assertEqual(sizes, [narrow] * 2 + [wide] * 2 + [narrow] * 2 + [wide] * 2, key)

    def test_the_figures_numbered_by_their_place(self):
        """The reader sees each figure numbered by its place among the post's figures, 1 to 16 in page order: in its anchor, its caption and its
        control, which the roster, a still figure, does not have. The slot still finds the files, so the relay's stand under the figure shown as
        F14, sign-and-seal's under F15 and filed's under F16."""
        figs = re.findall(r'<figure id="f(\d+)">(.*?)</figure>', self.page)
        self.assertEqual([int(n) for n, _fig in figs], list(range(1, 17)))
        for n, fig in figs:
            self.assertEqual(re.findall(r'<span class="fn">F(\d+)</span>', fig), [n])
            self.assertEqual(re.findall(r'data-f="F(\d+)"', fig), [] if n == "3" else [n])
        shows = {n: re.search(r'<img src="hail-1/([a-z0-9-]+?)(?:-780)?(?:-still)?\.png"', fig).group(1) for n, fig in figs}
        self.assertEqual([shows["13"], shows["14"], shows["15"], shows["16"]], ["f13-authority", "f16-relay", "f14-sign-seal", "f15-filed"])

    def test_the_heros_two_page_sources(self):
        video = re.search(r'<figure class="hero">\n    (<video [^>]*>.*?</video>)', self.page).group(1)
        self.assertEqual(re.findall(r'<source src="([^"]+)" type=\'([^\']+)\'>', video),
                         [("hail-1/hail-1-page.hevc.mp4", 'video/mp4; codecs="hvc1.1.6.L153.B0"'), ("hail-1/hail-1-page.mp4", 'video/mp4; codecs="avc1.64001F"')])
        self.assertNotIn("hail-1/hail-1.mp4", video)
        self.assertEqual(re.findall(r'<meta property="og:video(?::secure_url)?" content="([^"]+)">', self.page),
                         ["https://shoalmark.tools/blog/hail-1/hail-1.mp4"] * 2)
        self.assertNotRegex(self.page, r'<meta [^>]*hail-1-page')

    def test_the_share_rows(self):
        rows = re.findall(r'<div class="share( share-end)?"><p class="share-t">Share this article</p><div class="sh-row">(.*?)</div>'
                          r'<span class="vh" role="status" aria-live="polite"></span></div>', self.page)
        self.assertEqual([end for end, _row in rows], ["", " share-end"])
        self.assertIn('<article class="post">\n    <div class="share"><p class="share-t">', self.page)
        self.assertEqual(self.page.count('role="status" aria-live="polite"'), 2)
        for _end, row in rows:
            links = re.findall(r'<a class="sh" href="([^"]+)" target="_blank" rel="noopener noreferrer"><span class="sh-w">([^<]+)</span>'
                               r'<svg viewBox="0 0 7 7" aria-hidden="true" focusable="false">', row)
            self.assertEqual([word for _href, word in links], ["Post on X", "LinkedIn"])
            for href, word in links:
                url = urlsplit(href.replace("&amp;", "&"))
                self.assertEqual(url.scheme + "://" + url.netloc + url.path,
                                 {"Post on X": "https://x.com/intent/post", "LinkedIn": "https://www.linkedin.com/sharing/share-offsite/"}[word])
                self.assertEqual(parse_qs(url.query)["url"], [CANONICAL], word)
            self.assertRegex(row, f'<button type="button" class="sh sh-copy" data-url="{re.escape(CANONICAL)}" data-done="Link copied" hidden>'
                                  r'<svg viewBox="0 0 7 8" aria-hidden="true" focusable="false">.*?</svg><span class="sh-w">Copy link</span></button>$')
            self.assertNotIn("‹", row)
        self.assertNotRegex(self.page.lower(), r"facebook|new tab|<script(?![^>]*\bsrc=)")

    def test_the_band_links_the_one_page_then_the_spec(self):
        """The TL;DR's last row: the one page's button, then the spec's, each at its constant's address and before its own sentence, as the post
        writes them."""
        self.assertEqual(BB.ONE_PAGE, "https://github.com/shoalmark/hail/blob/main/QUICKSTART.md")
        self.assertEqual(BB.SPEC, "https://github.com/shoalmark/hail/blob/main/spec/hail-1.md")
        one_href, one, spec_href, spec = re.fullmatch(r"- \*\*Read it:\*\* \[Read the one page →\]\((\S+)\) (.+?) \[Read the spec →\]\((\S+)\) (.+)",
                                                      READ_IT).groups()
        self.assertEqual((one_href, spec_href), (BB.ONE_PAGE, BB.SPEC))
        row = re.search(r'<div class="try"><dt>Read it:</dt><dd>(.*?)</dd></div>', self.page).group(1)
        self.assertEqual(row, f'<span class="go"><a href="{html.escape(BB.ONE_PAGE, quote=True)}">Read the one page</a></span> {html.escape(one, quote=False)} '
                              f'<span class="go"><a href="{html.escape(BB.SPEC, quote=True)}">Read the spec</a></span> {html.escape(spec, quote=False)}')
        self.assertNotIn("‹link: spec›", self.page + (self.blog / "hail-1.md").read_text(encoding="utf-8"))
        self.assertIn(f'<p class="kicker"><time datetime="{DATE}">{DATE}</time>', self.page)

    def test_the_github_links_lead_to_the_organization(self):
        """Every blog page the build writes, the index and each post, links "GitHub" twice, in its header's a.bh-gh and in its footer, and both
        lead to the organization's page, never to the shoalmark repository."""
        self.assertEqual(BB.GITHUB, "https://github.com/shoalmark")
        pages = sorted(p.name for p in self.blog.glob("*.html"))
        self.assertEqual(pages, ["hail-1.html", "index.html"])
        for name in pages:
            text = (self.blog / name).read_text(encoding="utf-8")
            self.assertEqual(re.findall(r'<a class="bh-gh" href="([^"]*)">GitHub</a>', text), [BB.GITHUB], name)
            foot = re.search(r'<p class="bf-links">(.*?)</p>', text).group(1)
            self.assertEqual(re.findall(r'<a href="([^"]*)">GitHub</a>', foot), [BB.GITHUB], name)
            self.assertEqual(re.findall(r'href="([^"]*)">GitHub</a>', text), [BB.GITHUB, BB.GITHUB], name)
            self.assertNotIn('href="https://github.com/shoalmark/shoalmark">GitHub</a>', text, name)

    def test_no_inline_script(self):
        self.assertEqual(re.findall(r"<script(?![^>]*\bsrc=)", self.page), [])

    def test_the_markdown_version(self):
        md = (self.blog / "hail-1.md").read_text(encoding="utf-8")
        self.assertTrue(md.startswith(f'---\ntitle: "⌜hail/1⌟: agents message each other; the final word stays yours"\ndate: {DATE}\n'))
        self.assertIn(f"\n{READ_IT}\n", md)
        self.assertNotIn("<!--", md)
        self.assertEqual(len(re.findall(r"^!\[[^\]]+\]\(hail-1/[a-z0-9-]+\.png\)$", md, re.M)), 16)
        self.assertIn("\n## Who decides\n", md.split("\n## When a seat needs you\n", 1)[0])
        self.assertIn("\n![", md.split("\n## When a seat needs you\n", 1)[1].split("\n## ", 1)[0])
        self.assertIn("(https://shoalmark.tools/why-shoalmark.html)", md)

    def test_the_feed_and_llms(self):
        feed = (self.blog / "feed.xml").read_text(encoding="utf-8")
        self.assertIn("<title>shoalmark blog</title>", feed)
        self.assertIn("<guid>https://shoalmark.tools/blog/hail-1.html</guid>", feed)
        self.assertIn(f"<pubDate>{BB.pub_date(DATE)}</pubDate>", feed)
        self.assertTrue((self.blog / "llms.txt").read_text(encoding="utf-8").startswith("# shoalmark blog\n\n> How I build shoalmark with my agents"))


class Index(unittest.TestCase):
    """The blog's index: its opening statement as its one heading, the newest post as its lead, the earlier ones as cards, newest first, and ten
    posts at most. With the one post, the index is the design's page but for the name set as code in the opening, the two descriptions'
    words and the GitHub links' address: its SHA-256 is pinned here over the page with the post's date written as YYYY-MM-DD, so the date can
    move in its one line; the pin changes with the post's title, dek, card, kicker, reading time or authors, or with the templates or GITHUB."""

    INDEX_SHA256 = "ee3ae2f9586e9316f619fd00e51682acca2aec53f3344a3a761ddbe0e23c6b79"

    @staticmethod
    def posts(root, dates, folders=True):
        """More posts beside hail-1, each a copy of it under a slug and a date of its own: hail-2 on the first date, hail-3 on the next."""
        src = root / "blog/posts"
        for n, day in enumerate(dates, 2):
            slug = f"hail-{n}"
            text = (src / "hail-1.md").read_text(encoding="utf-8").replace("\nslug: hail-1\n", f"\nslug: {slug}\n", 1)
            (src / f"{slug}.md").write_text(text.replace(f"\ndate: {DATE}\n", f"\ndate: {day}\n", 1), encoding="utf-8")
            for part in ("figures.json", "hails.html"):
                shutil.copyfile(src / f"hail-1.{part}", src / f"{slug}.{part}")
            if folders:
                shutil.copytree(src / "hail-1", src / slug)

    def test_the_index_of_one_post_is_the_designs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = scratch(tmp)
            r = build(root)
            self.assertEqual(r.returncode, 0, r.stderr)
            index = (root / "site/blog/index.html").read_bytes()
        page = index.decode("utf-8")
        self.assertEqual(re.findall(r"<h1>(.*?)</h1>", page), [BB.INDEX_STATEMENT])
        self.assertTrue(BB.INDEX_STATEMENT.startswith("I build <code>shoalmark.tools</code> with my agents: "))
        statement = "I build shoalmark.tools with my agents: they do the work, I have the final word. Here is how, written from the record."
        self.assertIn(f'<meta name="description" content="{statement}">', page)
        self.assertIn(f'<meta property="og:description" content="{statement}">', page)
        self.assertIn("<title>Blog · shoalmark</title>", page)
        self.assertIn('<a class="ix-lead" href="hail-1.html"', page)
        self.assertIn('<source type="image/webp" srcset="hail-1/card.webp"><img class="ix-img" src="hail-1/card.png"', page)
        self.assertIn('title="by @holgo99 and six seats"><img class="ix-owner" src="assets/authors/owner-52.jpg"', page)
        self.assertNotIn("ix-earlier", page)
        self.assertNotIn("\n\n", page)
        self.assertEqual(index.count(DATE.encode()), 2, "the post's date stands on the index in its lead's kicker alone, as its datetime and its text")
        self.assertEqual(hashlib.sha256(index.replace(DATE.encode(), b"YYYY-MM-DD")).hexdigest(), self.INDEX_SHA256)

    def test_several_posts_the_newest_leads(self):
        for dates, count in (([AFTER(1)], "<b>1</b> earlier post</h2>"), ([AFTER(1), AFTER(2)], "<b>2</b> earlier posts</h2>")):
            with self.subTest(posts=len(dates) + 1), tempfile.TemporaryDirectory() as tmp:
                root = scratch(tmp)
                self.posts(root, dates)
                r = build(root)
                self.assertEqual(r.returncode, 0, r.stderr)
                page = (root / "site/blog/index.html").read_text(encoding="utf-8")
                newest = f"hail-{len(dates) + 1}"
                self.assertEqual(re.findall(r'<a class="ix-lead" href="([^"]+)"', page), [f"{newest}.html"])
                self.assertIn(count, page)
                cards = re.findall(r'<li><a class="ix-card" href="([^"]+)".*?<img [^>]*loading="(\w+)"', page)
                self.assertEqual(cards, [(f"hail-{n}.html", "lazy") for n in range(len(dates), 0, -1)])
                self.assertEqual(page.count('loading="eager"'), 1)
                self.assertNotIn("ix-more", page)
                self.assertNotIn("\n\n", page)

    def test_eleven_posts_are_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = scratch(tmp)
            self.posts(root, [AFTER(n) for n in range(1, 11)], folders=False)
            r = build(root)
            self.assertNotEqual(r.returncode, 0, "the builder built an index of eleven posts")
            self.assertIn("blog/posts holds 11 posts, and the index shows 10 at most: the page after it is not built yet", r.stderr)


class OneEdit(unittest.TestCase):
    """The spec's address lives in the builder's SPEC alone, and the one page's in ONE_PAGE alone; the post's band must link each as written
    there: either changed alone, the build refuses the post; each changed with its link in the band, every place that links it takes the new
    address. The post's date lives in one place: one edit of it reaches every place that shows it."""

    def edited(self, root, spec=None, band=None, date=None, one_page=None, one_band=None):
        builder, post = root / "scripts/build_blog.py", root / "blog/posts/hail-1.md"
        text = builder.read_text(encoding="utf-8")
        self.assertEqual(text.count(f'SPEC = "{BB.SPEC}"'), 1)
        self.assertEqual(text.count(f'ONE_PAGE = "{BB.ONE_PAGE}"'), 1)
        if spec:
            text = text.replace(f'SPEC = "{BB.SPEC}"', f'SPEC = "{spec}"')
        if one_page:
            text = text.replace(f'ONE_PAGE = "{BB.ONE_PAGE}"', f'ONE_PAGE = "{one_page}"')
        builder.write_text(text, encoding="utf-8")
        words = post.read_text(encoding="utf-8")
        for old, new in ((BB.SPEC, band), (BB.ONE_PAGE, one_band)):
            if new:
                self.assertEqual(words.count(f"]({old})"), 1)
                words = words.replace(f"]({old})", f"]({new})")
        if date:
            words = words.replace(f"\ndate: {DATE}\n", f"\ndate: {date}\n", 1)
        post.write_text(words, encoding="utf-8")
        return build(root)

    def test_the_spec_changed_alone_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            r = self.edited(scratch(tmp), spec="https://example.org/spec.html")
            self.assertNotEqual(r.returncode, 0, "the builder built a post whose band links another address than SPEC")
            self.assertIn("the TL;DR's last item does not follow the one page's sentence with the spec's link and its arrow", r.stderr)

    def test_the_one_page_changed_alone_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            r = self.edited(scratch(tmp), one_page="https://example.org/one.html")
            self.assertNotEqual(r.returncode, 0, "the builder built a post whose band links another address than ONE_PAGE")
            self.assertIn("the TL;DR's last item does not open with the one page's link and its arrow", r.stderr)

    def test_one_edit_of_the_spec_with_its_band_or_of_the_date(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = scratch(tmp)
            r = self.edited(root, spec="https://example.org/spec.html", band="https://example.org/spec.html", date="2027-01-15",
                            one_page="https://example.org/one.html", one_band="https://example.org/one.html")
            self.assertEqual(r.returncode, 0, r.stderr)
            page = (root / "site/blog/hail-1.html").read_text(encoding="utf-8")
            md = (root / "site/blog/hail-1.md").read_text(encoding="utf-8")
            feed = (root / "site/blog/feed.xml").read_text(encoding="utf-8")
            self.assertIn('<dd><span class="go"><a href="https://example.org/one.html">', page)
            self.assertLess(page.index('<dd><span class="go"><a href="https://example.org/one.html">'),
                            page.index('<span class="go"><a href="https://example.org/spec.html">'))
            self.assertIn("](https://example.org/one.html)", md)
            self.assertIn("](https://example.org/spec.html)", md)
            self.assertNotIn(BB.SPEC, page + md)
            self.assertNotIn(BB.ONE_PAGE, page + md)
            self.assertIn('<time datetime="2027-01-15">2027-01-15</time>', page)
            self.assertIn("\ndate: 2027-01-15\n", md)
            self.assertIn("<pubDate>Fri, 15 Jan 2027 00:00:00 +0100</pubDate>", feed)
            self.assertNotIn(DATE, page.split("<main", 1)[1].split("</header>", 1)[0])


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

    def row(self, make):
        """The band rewritten from its two parts, the one page's link with its sentence and the spec's link with its: make(one, spec) gives the
        row's words."""
        def change(root):
            post = root / "blog/posts/hail-1.md"
            text = post.read_text(encoding="utf-8")
            m = re.search(r"^- \*\*Read it:\*\* (\[[^\]]+\]\(" + re.escape(BB.ONE_PAGE) + r"\) .+?) (\[[^\]]+\]\(" + re.escape(BB.SPEC) + r"\) .+)$", text, re.M)
            self.assertIsNotNone(m)
            post.write_text(text[:m.start(1)] + make(m.group(1), m.group(2)) + text[m.end(2):], encoding="utf-8")
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
                ("the band linking the old placeholder", self.edit(post, f"]({BB.SPEC})", "](‹link: spec›)"),
                 "does not follow the one page's sentence with the spec's link"),
                ("the band linking another address", self.edit(post, f"]({BB.SPEC})", "](https://github.com/shoalmark/hail/blob/main/spec/hail-2.md)"),
                 "does not follow the one page's sentence with the spec's link"),
                ("the band without the one page's link", self.row(lambda one, spec: spec), "does not open with the one page's link and its arrow"),
                ("the one page's link after the spec's", self.row(lambda one, spec: f"{spec} {one}"), "does not open with the one page's link and its arrow"),
                ("the one page's link to another address", self.edit(post, f"]({BB.ONE_PAGE})", "](https://github.com/shoalmark/hail/blob/main/README.md)"),
                 "does not open with the one page's link and its arrow"),
                ("the band without the spec's link", self.row(lambda one, spec: one), "does not follow the one page's sentence with the spec's link"),
                ("a third link in the band", self.row(lambda one, spec: f"{one} {spec} [More →](https://example.org/more) More words."),
                 "holds a link beside the one page's and the spec's"),
                ("a third link in the one page's sentence", self.row(lambda one, spec: f"{one} [More →](https://example.org/more) More words. {spec}"),
                 "holds a link beside the one page's and the spec's"),
                ("a font of another subset", lambda root: shutil.copyfile(root / "docs/assets/fonts/IBM-Plex-Mono-normal-400-latin-ext.woff2",
                                                                         root / "docs/assets/fonts/IBM-Plex-Mono-normal-400-latin.woff2"), "is not the latin subset"),
                ("a figure with no entry", self.edit("blog/posts/hail-1.figures.json", '"F15"', '"F16"'), "F15 has no entry"),
                ("a figure's slot twice", self.edit(post, "\n## When a seat needs you\n", "\n[F14 · again]\n*Again.*\n\n## When a seat needs you\n"),
                 "do not match its files"),
                ("site/blog already there", lambda root: (root / "site/blog").mkdir(parents=True), "is already there"),
                ("a template's slot with no value", self.edit("blog/templates/post.html", "{{ dek }}", "{{ deck }}"), "no value for deck"),
                ("a seat with no icon in brand/seats/", self.edit(post, '{"seat": "auditor"', '{"seat": "research-lab"'), "its icon in brand/seats/"),
                ("the Owner's picture not in blog/authors/", self.edit(post, '"picture": "owner.jpg"', '"picture": "nobody.jpg"'),
                 "a picture in blog/authors/"),
                ("a front matter without its authors", self.edit(post, "authors: [", "people: ["), "its front matter has no authors"),
                ("a card of another size than the head names", lambda root: shutil.copyfile(root / "blog/posts/hail-1/f1-courier-still.png",
                                                                                            root / "blog/posts/hail-1/card.png"), "its card is not 1200 x 630"),
                ("an HEVC page file that says hev1", lambda root: (root / "blog/posts/hail-1/hail-1-page.hevc.mp4").write_bytes(
                    (root / "blog/posts/hail-1/hail-1-page.hevc.mp4").read_bytes().replace(b"hvc1", b"hev1", 1)), "its video's sample entry is hev1, not avc1 or hvc1"),
                ("a figure's WebP twin with no file", lambda root: (root / "blog/posts/hail-1/f14-sign-seal-780-once.webp").rename(root / "f14-sign-seal-780-once.webp.moved"),
                 "f14-sign-seal-780-once.webp, a WebP twin's file, is not among its files"),
                ("a card with no WebP twin", lambda root: (root / "blog/posts/hail-1/card.webp").rename(root / "card.webp.moved"),
                 "its card card.png has no lossless WebP twin, card.webp, beside it"),
                ("the Owner's picture with no 52 px one", lambda root: (root / "blog/authors/owner-52.jpg").rename(root / "owner-52.jpg.moved"),
                 "the Owner's picture owner.jpg has no 52 px one, owner-52.jpg, in blog/authors/"),
                ("the hero's page files in the other order", self.edit(post, 'hero: ["hail-1-page.hevc.mp4", "hail-1-page.mp4"]', 'hero: ["hail-1-page.mp4", "hail-1-page.hevc.mp4"]'),
                 "not an HEVC file, then an H.264 one")):
            with self.subTest(name):
                self.refused(change, reason)


if __name__ == "__main__":
    unittest.main()
