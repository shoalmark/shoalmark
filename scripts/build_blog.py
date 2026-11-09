"""The blog: shoalmark's own small site at shoalmark.tools/blog/, English only and dark-first, built from blog/ without the docs engine.

Usage: python3 scripts/build_blog.py [site]   (default: site; it writes site/blog/ and refuses when that folder is already there)

Standard library only. From blog/, it reads:
- posts/<slug>.md: a post, its front matter (`key: value` lines; a value in double quotes or brackets is JSON) and its Markdown;
- posts/<slug>.figures.json: each figure slot's files, the play-once GIFs' lengths in ms, and its alt text;
- posts/<slug>.hails.html: the hails shown as page text, each after a comment naming its place;
- posts/<slug>/: the files the post shows;
- templates/, css/base.css and css/m2.css, js/blog.js: the kit. The templates use two forms only: {{ slot }} and {% include "name" %};
- authors/: the pictures of the authors who are people; a seat's picture is its icon in brand/seats/.
It writes site/blog/: index.html, <slug>.html, <slug>.md (the post for agent readers), <slug>/ (its files), assets/blog.css and
assets/blog.js, assets/authors/ and assets/seats/ (the authors' pictures), fonts/ (the site's own latin subsets, under neutral names, with
their licences), feed.xml and llms.txt.
Every page links with relative addresses; the head's addresses are absolute. A post's body is its Markdown converted line by line into the
post's markup: the TL;DR as a dl with its band, each slot a figure with its stills and play-once GIFs, numbered for the reader by its place
among the post's figures, each marker section, the hails, the status paragraph, the quotation, the reference and the foot, each figure's
sources and <img> each after its WebP twin; then each heading gets its anchor, each hail its label, "written by" and the credits follow the
quotation, and the end links follow the foot. The head names the authors, and a share row opens the post and comes again after "written
by". The builder refuses whatever has a shape it does not expect.
"""
import datetime
import hashlib
import html
import json
import re
import shutil
import sys
import unicodedata
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "blog"
SITE_URL = "https://shoalmark.tools/"
GITHUB = "https://github.com/shoalmark/shoalmark"
SPEC = "https://github.com/shoalmark/hail/blob/main/spec/hail-1.md"   # the published spec's address: a post's band must link it, as written here
WPM = 230                                                  # the reading time: the words over 230 a minute, rounded up
VARIANT = "m2"
INDEX_INTRO = "How I build shoalmark with my agents, written from the record."
BLOG_NAME = "shoalmark blog"
LLMS_LINE = "Every post has a Markdown version beside it; the figures are linked as stills, each with its alt text."
UI = {"markdown": "read as Markdown", "contents": "on this page", "credits": "Acknowledgements", "all": "← all posts",
      "rss": "RSS", "read": "{n} min read", "stop": "stop", "share": "Share this article", "copy": "Copy link", "copied": "Link copied",
      "written": "Written by", "post_x": "Post on X"}
LINKS = {"‹link: why-shoalmark›": "why-shoalmark.html", "‹link: seats›": "seats/index.html"}     # a foot link's page, from the site's root
FONTS = {"IBM-Plex-Mono-normal-400-latin.woff2": ("mono-400.woff2", "c36f509c"), "IBM-Plex-Mono-normal-600-latin.woff2": ("mono-600.woff2", "ad4580d8"),
         "Silkscreen-normal-400-latin.woff2": ("pixel-400.woff2", "17bb6d80"), "Silkscreen-normal-700-latin.woff2": ("pixel-700.woff2", "30ad65d8"),
         "ibmplexmono-OFL.txt": ("OFL.txt", None), "silkscreen-OFL.txt": ("OFL-pixel.txt", None)}
MARKERS = ("INFORMATION", "ADVICE", "WARNING", "QUESTION", "ANSWER", "REQUEST", "STOP")


def refuse(message):
    raise SystemExit("build_blog: " + message)


# --- the post's source ------------------------------------------------------------------------------------------------------------------------
def front_matter(text, name):
    if not text.startswith("---\n") or "\n---\n" not in text:
        refuse(f"{name} has no front matter")
    head, body = text[4:].split("\n---\n", 1)
    meta = {}
    for line in head.split("\n"):
        key, sep, value = line.partition(": ")
        if not sep or not re.fullmatch(r"[a-z_]+", key):
            refuse(f"{name}: a front matter line is not 'key: value': {line[:60]!r}")
        meta[key] = json.loads(value) if value[:1] in '"[' else value
    for key in ("title", "slug", "date", "kicker", "dek", "card", "card_alt", "video", "hero", "authors", "credits"):
        if key not in meta:
            refuse(f"{name}: its front matter has no {key}")
    return meta, body.lstrip("\n")


def hails_of(path):
    """The hails as page text: each pre.ex block, byte for byte, after the comment that names its place."""
    pairs = re.findall(r"<!-- (.+?) -->\n(<pre class=\"ex(?: lit-ex)?\"><code>.*?</code></pre>)\n", path.read_text(encoding="utf-8"), re.S)
    if not pairs or len({p for p, _ in pairs}) != len(pairs):
        refuse(f"{path.name} holds no hails, or names a place twice")
    return dict(pairs)


def lines_of(block):
    """A hail's lines as text, one per .ln span, its markup and entities taken out."""
    return [html.unescape(re.sub(r"<[^>]+>", "", s)) for s in re.findall(r'<span class="ln[^"]*">(.*?)</span>(?=<span class="ln|</code>)', block)]


def size(path):
    """A PNG's or a GIF's width and height, read from its header."""
    data = path.read_bytes()[:32]
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        return int.from_bytes(data[16:20], "big"), int.from_bytes(data[20:24], "big")
    if data[:6] in (b"GIF87a", b"GIF89a"):
        return int.from_bytes(data[6:8], "little"), int.from_bytes(data[8:10], "little")
    refuse(f"{path.name} is no PNG or GIF")


def codecs(path):
    """The codec string of an MP4's video track, as its own header gives it: the track whose handler is vide, its first sample entry, and
    that entry's avcC or hvcC box, so that the page never names a profile or a level the file does not carry. An H.264 file must say avc1
    and an HEVC file hvc1, its parameter sets in the header; any other entry, hev1 among them, is refused."""
    data = path.read_bytes()

    def boxes(start, end):
        i = start
        while i + 8 <= end:
            size, kind, head = int.from_bytes(data[i:i + 4], "big"), data[i + 4:i + 8], 8
            if size == 1:
                size, head = int.from_bytes(data[i + 8:i + 16], "big"), 16
            elif size == 0:
                size = end - i
            if size < head or i + size > end:
                refuse(f"{path.name}: a box runs past its parent")
            yield kind, i + head, i + size
            i += size

    def child(span, kind):
        found = [(s, e) for k, s, e in boxes(*span) if k == kind]
        if not found:
            refuse(f"{path.name}: no {kind.decode('latin-1')} box where an MP4 has one")
        return found[0]

    for kind, start, end in boxes(*child((0, len(data)), b"moov")):
        if kind != b"trak":
            continue
        mdia = child((start, end), b"mdia")
        hdlr = child(mdia, b"hdlr")
        if data[hdlr[0] + 8:hdlr[0] + 12] != b"vide":
            continue
        stsd = child(child(child(mdia, b"minf"), b"stbl"), b"stsd")
        entry, s, e = next(boxes(stsd[0] + 8, stsd[1]))
        if entry not in (b"avc1", b"hvc1"):
            refuse(f"{path.name}: its video's sample entry is {entry.decode('latin-1')}, not avc1 or hvc1")
        c = data[slice(*child((s + 78, e), b"avcC" if entry == b"avc1" else b"hvcC"))]
        if entry == b"avc1":
            return f"avc1.{c[1]:02X}{c[2]:02X}{c[3]:02X}"
        compatible = int(f"{int.from_bytes(c[2:6], 'big'):032b}"[::-1], 2)
        constraints = list(c[6:12])
        while constraints and constraints[-1] == 0:
            constraints.pop()
        return (f"hvc1.{('', 'A', 'B', 'C')[c[1] >> 6]}{c[1] & 31}.{compatible:X}.{'LH'[(c[1] >> 5) & 1]}{c[12]}"
                + "".join(f".{x:X}" for x in constraints))
    refuse(f"{path.name}: no video track")


# --- the body ---------------------------------------------------------------------------------------------------------------------------------
def attr(text):
    return html.escape(text, quote=True).replace("&#x27;", "'")


def text_node(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def inline(md):
    """A line's Markdown as HTML: code spans, links and bold, the only marks a post uses; any other mark is refused."""
    out, i = [], 0
    for m in re.finditer(r"`([^`]+)`|\[([^\]]+)\]\(([^)\s]+)\)|\*\*([^*]+)\*\*", md):
        out.append(text_node(md[i:m.start()]))
        if m.group(1) is not None:
            out.append(f"<code>{text_node(m.group(1))}</code>")
        elif m.group(2) is not None:
            out.append(f'<a href="{attr(m.group(3))}">{inline(m.group(2))}</a>')
        else:
            out.append(f"<strong>{inline(m.group(4))}</strong>")
        i = m.end()
    out.append(text_node(md[i:]))
    joined = "".join(out)
    if re.search(r"[*`]", re.sub(r"<code>.*?</code>", "", joined)):
        refuse(f"a line holds a mark the blog does not carry: {md[:80]!r}")
    return joined


def plain(md):
    return md.replace("**", "").replace("`", "")


def slug_of(value):
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[-\s]+", "-", re.sub(r"[^\w\s-]", "", value).strip().lower())


def blocks(lines):
    """The Markdown as blocks: blank lines part them, and a fence is one block, blank lines and all."""
    out, cur, fence = [], [], False
    for line in lines:
        if line.startswith("```"):
            fence = not fence
            cur.append(line)
            if not fence:
                out.append(cur)
                cur = []
        elif fence:
            cur.append(line)
        elif line == "":
            if cur:
                out.append(cur)
            cur = []
        else:
            cur.append(line)
    if fence:
        refuse("a fence is not closed")
    return out + ([cur] if cur else [])


class Post:
    def __init__(self, path):
        self.path, self.name = path, path.stem
        self.meta, self.markdown = front_matter(path.read_text(encoding="utf-8"), path.name)
        self.slug = self.meta["slug"]
        if self.slug != self.name or not re.fullmatch(r"[a-z0-9-]+", self.slug):
            refuse(f"{path.name}: its slug {self.slug!r} is not its file's name")
        self.files = path.parent / self.slug
        self.figures = json.loads((path.parent / f"{self.slug}.figures.json").read_text(encoding="utf-8"))
        self.hails = hails_of(path.parent / f"{self.slug}.hails.html")
        lines = self.markdown.rstrip("\n").split("\n")
        if not (lines[0].startswith("<!-- ") and lines[0].endswith(" -->") and lines[1] == ""):
            refuse(f"{path.name}: its first line is not one comment for the record")
        self.lines = lines[2:]
        if self.lines[0] != "# " + self.meta["title"]:
            refuse(f"{path.name}: its # line is not the title of its front matter")
        self.used = set()

    # the title: the wordmark ⌜name⌟ drawn by CSS, the claim and the promise in two spans
    def title_html(self):
        m = re.fullmatch(r"⌜([^⌟]+)⌟(: [^;]+;) (.+)", self.meta["title"])
        if not m:
            refuse(f"{self.name}: the title is not '⌜name⌟: claim; promise'")
        return f'<span><span class="hf">{text_node(m.group(1))}</span>{text_node(m.group(2))}</span> <span>{text_node(m.group(3))}</span>'

    def hail(self, place):
        if place not in self.hails:
            refuse(f"{self.name}: no hail for the place {place!r}")
        self.used.add(place)
        return self.hails[place]

    def twins(self, picture):
        """Before each <source> and the <img> of a figure's <picture>, its WebP twin: the same media, sizes and data, its files .webp and its
        type image/webp. A browser that reads WebP takes the twin; any other skips it and takes the PNG or GIF, which stay as they were."""
        slug = re.escape(self.slug)

        def twin(m):
            tag = m.group(0)
            webp = re.sub(rf'({slug}/[A-Za-z0-9._-]+)\.(?:png|gif)"', r'\1.webp"', tag)
            for name in re.findall(rf'{slug}/([A-Za-z0-9._-]+\.webp)"', webp):
                if not (self.files / name).is_file():
                    refuse(f"{self.name}: {name}, a WebP twin's file, is not among its files")
            if tag.startswith("<source "):
                return webp.replace("<source ", '<source type="image/webp" ', 1) + tag
            a = dict(re.findall(r'([\w-]+)="([^"]*)"', webp))
            keep = "".join(f' {k}="{a[k]}"' for k in ("width", "height", "data-still", "data-once", "data-ms") if k in a)
            return f'<source type="image/webp" srcset="{a["src"]}"{keep}>' + tag
        return re.sub(r"<(?:source|img) [^>]*>", twin, picture)

    def figure(self, n, place, caption):
        """A figure slot: its <picture>, every source and its <img> each after its WebP twin, and its caption. Slot n finds its entry in the figures
        file; the reader sees its place among the post's figures, 1 for the first, in its anchor, its caption and its control."""
        return re.sub(r"<picture>.*?</picture>", lambda m: self.twins(m.group(0)), self.figure_png_gif(n, place, caption))

    def figure_png_gif(self, n, place, caption):
        f = self.figures.get(f"F{n}")
        if not f:
            refuse(f"{self.name}: F{n} has no entry in its figures file")
        src, alt = f"{self.slug}/", f' alt="{attr(f["alt"])}"'
        wh = lambda name: 'width="%d" height="%d"' % size(self.files / name)
        if "stills" in f:
            small, wide = sorted(f["stills"], key=lambda s: size(self.files / s)[0])
            return (f'<figure id="f{place}"><picture><source media="(max-width: 640px)" srcset="{src}{small}" {wh(small)}>'
                    f'<img src="{src}{wide}" {wh(wide)}{alt} loading="lazy" decoding="async"></picture>'
                    f'<figcaption><span class="fn">F{place}</span>{text_node(caption)}</figcaption></figure>')
        b = f["name"]
        s540, s780, o540, o780 = f"{b}-still.png", f"{b}-780-still.png", f"{b}-once.gif", f"{b}-780-once.gif"
        load = 'loading="eager" fetchpriority="high"' if place == 1 else 'loading="lazy"'
        return (f'<figure id="f{place}"><picture>'
                f'<source media="(prefers-reduced-motion: reduce) and (max-width: 640px)" srcset="{src}{s540}" {wh(s540)}>'
                f'<source media="(prefers-reduced-motion: reduce)" srcset="{src}{s780}" {wh(s780)}>'
                f'<source media="(max-width: 640px)" srcset="{src}{s540}" {wh(s540)} data-still="{src}{s540}" data-once="{src}{o540}" data-ms="{f["ms"][0]}">'
                f'<img src="{src}{s780}" {wh(s780)}{alt} {load} decoding="async" data-still="{src}{s780}" data-once="{src}{o780}" data-ms="{f["ms"][1]}">'
                f'</picture><figcaption><span class="fn">F{place}</span>{text_node(caption)} <button type="button" class="again" data-f="F{place}" hidden>'
                f'{UI["stop"]}</button></figcaption></figure>')

    def table(self, rows, cls):
        head = [c.strip() for c in rows[0].strip("|").split(" | ")]
        if not re.fullmatch(r"\|(?:-+\|)+", rows[1]):
            refuse(f"{self.name}: a table's second line is not its rule")
        body = []
        for row in rows[2:]:
            cells = [c.strip() for c in row[2:-2].split(" | ")]
            if len(cells) != len(head):
                refuse(f"{self.name}: a table row has {len(cells)} cells, not {len(head)}")
            body.append("<tr>" + "".join(f'<td data-h="{attr(h)}">{inline(c)}</td>' for h, c in zip(head, cells)) + "</tr>")
        return (f'<table class="{cls}"><thead><tr>' + "".join(f"<th>{text_node(h)}</th>" for h in head) + "</tr></thead><tbody>"
                + "".join(body) + "</tbody></table>")

    def body(self):
        bl = blocks(self.lines[2:])
        if bl[0] != ["**TL;DR:**"]:
            refuse(f"{self.name}: the TL;DR's lead-in is not where the post has it")
        rows = []
        for item in bl[1]:
            m = re.fullmatch(r"- \*\*([^*]+)\*\* (.+)", item)
            if not m:
                refuse(f"{self.name}: a TL;DR item is not '- **Label:** words'")
            rows.append((m.group(1), m.group(2)))
        label, words = rows[-1]
        band = re.match(r"\[([^\]]+) →\]\(" + re.escape(SPEC) + r"\) (.+)", words)
        if not band:
            refuse(f"{self.name}: the TL;DR's last item does not open with the spec's link and its arrow")
        dl = "".join(f"<div><dt>{text_node(l)}</dt><dd>{inline(w)}</dd></div>" for l, w in rows[:-1])
        dl += (f'<div class="try"><dt>{text_node(label)}</dt><dd><span class="go"><a href="{attr(SPEC)}">{text_node(band.group(1))}</a></span> '
               f"{inline(band.group(2))}</dd></div>")
        out = [f'<section class="tldr" aria-labelledby="tldr"><h2 class="t" id="tldr">TL;DR:</h2><dl>{dl}</dl></section>']
        seen, marker, in_ref, tables, state, i = [], 0, False, 0, False, 2
        self.description = " ".join(re.split(r"(?<=\.) ", plain(bl[2][0]))[:2])
        while i < len(bl):
            block, first = bl[i], bl[i][0]
            slot = re.fullmatch(r"\[F(\d+) · ([^\]]+)\]", first)
            if slot:
                n = int(slot.group(1))
                cap = re.fullmatch(r"\*([^*]+)\*", block[1]) if len(block) == 2 else None
                if not cap:
                    refuse(f"{self.name}: slot F{n} is not a slot line and an italic caption")
                out.append(self.figure(n, len(seen) + 1, cap.group(1)))
                seen.append(n)
                if f"after F{n}" in self.hails:
                    out.append(self.hail(f"after F{n}"))
            elif first.startswith("### "):
                name, nxt = first[4:], bl[i + 1:i + 3]
                fig = re.fullmatch(r"\[F(\d+) · [^\]]+\]", nxt[0][0]) if len(nxt) == 2 else None
                if len(block) != 1 or not fig or len(nxt[0]) != 2 or len(nxt[1]) != 1:
                    refuse(f"{self.name}: the marker {name} is not a heading, a slot and one paragraph")
                n, marker = int(fig.group(1)), marker + 1
                out.append(f'<section class="mk" aria-label="{attr(name)}"><h3 id="{slug_of(name)}">{text_node(name)}</h3>'
                           + self.figure(n, len(seen) + 1, re.fullmatch(r"\*([^*]+)\*", nxt[0][1]).group(1)) + f"<p>{inline(nxt[1][0])}</p>"
                           + self.hail(f"in {name}") + "</section>")
                seen.append(n)
                i += 3
                continue
            elif first.startswith("## "):
                if any(b[0].startswith("```") for b in bl[i + 1:i + 4]) and not any(b[0].startswith("## ") for b in bl[i + 1:]):
                    in_ref = True
                    out.append(f'<section class="ref" aria-labelledby="ref-h"><h2 id="ref-h">{text_node(first[3:])}</h2>')
                else:
                    out.append(f'<h2 id="{slug_of(first[3:])}">{text_node(first[3:])}</h2>')
            elif first.startswith("```"):
                block_html = self.hail("for the reference's fence")
                if not in_ref or block[0] != "```text" or block[1:-1] != lines_of(block_html):
                    refuse(f"{self.name}: the reference's fence is not its hail, line for line")
                out.append(block_html)
            elif first.startswith("| "):
                tables += 1
                cls = "ba" if tables == 1 else "markers"
                out.append(self.table(block, cls))
                state = cls == "ba"
                i += 1
                continue
            elif first.startswith("> "):
                if not (len(block) == 3 and block[1] == ">" and block[2].startswith("> — ")):
                    refuse(f"{self.name}: the quotation is not a paragraph, a blank quote line and its attribution")
                out.append(f'<section class="ending" aria-label="ending"><figure class="said"><blockquote><p>{inline(first[2:])}</p></blockquote>'
                           f"<figcaption>{text_node(block[2][2:])}</figcaption></figure></section>")
            elif i == len(bl) - 1:
                last = first
                for old, page in LINKS.items():
                    if last.count(f"({old})") != 1:
                        refuse(f"{self.name}: the last line does not hold {old} once")
                    last = last.replace(f"({old})", f"(../{page})")
                if in_ref:
                    out.append("</section>")
                out.append(f'<p class="foot">{inline(last)}</p>')
            else:
                if len(block) != 1:
                    refuse(f"{self.name}: a paragraph runs over two lines")
                out.append(f'<p class="state">{inline(first)}</p>' if state else f"<p>{inline(first)}</p>")
            state = False
            i += 1
        if len(seen) != len(set(seen)) or set(seen) != {int(k[1:]) for k in self.figures} or marker != len(MARKERS) or self.used != set(self.hails):
            refuse(f"{self.name}: the slots {seen}, the {marker} markers or the hails used do not match its files")
        end = authors(*self.authors(), end=True) + "\n" + share(f"{SITE_URL}blog/{self.slug}.html", self.meta["title"], end=True)
        return touches("\n".join(out), self.meta["credits"], end)

    def authors(self):
        """The post's authors from its front matter: first the Owner, a person with a link, a picture in blog/authors/ and a role line; then
        the seats, each with its name, its role line and its icon in brand/seats/."""
        people = self.meta["authors"]
        if not isinstance(people, list) or len(people) < 2:
            refuse(f"{self.name}: its authors are not the Owner and the seats")
        owner, seats = people[0], people[1:]
        if (not isinstance(owner, dict) or set(owner) != {"name", "href", "picture", "role"} or not owner["href"].startswith("https://")
                or not (SRC / "authors" / owner["picture"]).is_file()):
            refuse(f"{self.name}: its first author is not a person with a name, a link, a picture in blog/authors/ and a role")
        for seat in seats:
            if not isinstance(seat, dict) or set(seat) != {"seat", "name", "role"} or not (ROOT / "brand/seats" / f"{seat['seat']}.svg").is_file():
                refuse(f"{self.name}: an author is not a seat with a name, a role and its icon in brand/seats/: {str(seat)[:80]}")
        return owner, seats

    def words(self):
        """The reading time's count: the words, without the TL;DR, the figure slots, the title and the comment."""
        keep, tl = [], False
        for ln in self.lines:
            if ln.startswith("**TL;DR:**"):
                tl = True
                continue
            if tl and (ln.startswith("- ") or not ln.strip()):
                continue
            tl = False
            if re.match(r"^\[F\d+ · ", ln) or ln.startswith("# "):
                continue
            keep.append(ln)
        return len(re.findall(r"[\w’'⌜⌟/.-]+", "\n".join(keep)))

    def markdown_version(self):
        """The post for agent readers: its Markdown as written, each figure slot an image of its widest still, with the page's alt text."""
        def still(m):
            f = self.figures[f"F{m.group(1)}"]
            name = sorted(f["stills"], key=lambda s: size(self.files / s)[0])[-1] if "stills" in f else f["name"] + "-780-still.png"
            return f"![{f['alt']}]({self.slug}/{name})"
        md, n = re.subn(r"^\[F(\d+) · [^\]]*\]$", still, "\n".join(self.lines) + "\n", flags=re.M)
        if n != len(self.figures):
            refuse(f"{self.name}: {n} slots, not {len(self.figures)}")
        for old, page in LINKS.items():
            md = md.replace(f"({old})", f"({SITE_URL}{page})")
        return (f'---\ntitle: "{self.meta["title"]}"\ndate: {self.meta["date"]}\ncanonical: {SITE_URL}blog/{self.slug}.html\n'
                f'description: "{self.description}"\n---\n\n' + md)


def authors(owner, seats, end=False):
    """The authors: in the head, the Owner's line, then the seats in a row; at the end, "written by", one list of them all. Every picture's alt
    is empty, as its name stands beside it as text."""
    so, ss = (60, 60) if end else (48, 40)
    o = (f'<a class="au au-owner" href="{attr(owner["href"])}"><img src="assets/authors/{attr(owner["picture"])}" width="{so}" height="{so}" alt="">'
         f'<span><b>{text_node(owner["name"])}</b><i>{text_node(owner["role"])}</i></span></a>')
    row = "".join(f'<li class="au"><img src="assets/seats/{attr(s["seat"])}.svg" width="{ss}" height="{ss}" alt=""><span><b>{text_node(s["name"])}</b>'
                  f'<i>{text_node(s["role"])}</i></span></li>' for s in seats)
    if end:
        return (f'<section class="written" aria-labelledby="written-t"><h2 class="wt" id="written-t">{UI["written"]}</h2><ul>'
                f'<li class="au-owner">{o.replace(" au-owner", "", 1)}</li>{row}</ul></section>')
    return f'    <div class="by">\n      {o}\n      <ul class="au-seats">{row}</ul>\n    </div>'


EXT = ('<svg viewBox="0 0 7 7" aria-hidden="true" focusable="false"><path shape-rendering="crispEdges" d="M4 0h3v1h-3ZM5 1h2v1h-2ZM0 2h3v1h-3ZM4 2h1v1h-1Z'
       'M6 2h1v1h-1ZM0 3h1v1h-1ZM3 3h1v1h-1ZM0 4h1v1h-1ZM2 4h1v1h-1ZM5 4h1v1h-1ZM0 5h1v1h-1ZM5 5h1v1h-1ZM0 6h6v1h-6Z"/></svg>')    # the start page's Docs arrow, "opens elsewhere"
COPY = ('<svg viewBox="0 0 7 8" aria-hidden="true" focusable="false"><path shape-rendering="crispEdges" d="M0 0h5v1h-5ZM0 1h1v1h-1ZM0 2h1v1h-1ZM2 2h5v1h-5Z'
        'M0 3h1v1h-1ZM2 3h1v1h-1ZM6 3h1v1h-1ZM0 4h1v1h-1ZM2 4h5v1h-5ZM0 5h1v1h-1ZM2 5h1v1h-1ZM6 5h1v1h-1ZM2 6h5v1h-5ZM2 7h5v1h-5Z"/></svg>')   # the start page's copy mark


def share(url, title, end=False):
    """The share row, under the hero and again at the end: its label, then X and LinkedIn as plain links to their share pages, opened in a
    new tab, and the copy button, which the script shows only where the browser has a clipboard. Each word is in its own span, each pixel
    mark is hidden from screen readers, and each row has its own live region for what the copy button says."""
    q = lambda s: quote(s, safe="")
    return (f'    <div class="share{" share-end" if end else ""}"><p class="share-t">{UI["share"]}</p><div class="sh-row">'
            f'<a class="sh" href="https://x.com/intent/post?url={q(url)}&amp;text={q(title)}" target="_blank" rel="noopener noreferrer">'
            f'<span class="sh-w">{UI["post_x"]}</span>{EXT}</a>'
            f'<a class="sh" href="https://www.linkedin.com/sharing/share-offsite/?url={q(url)}" target="_blank" rel="noopener noreferrer">'
            f'<span class="sh-w">LinkedIn</span>{EXT}</a>'
            f'<button type="button" class="sh sh-copy" data-url="{attr(url)}" data-done="{UI["copied"]}" hidden>{COPY}<span class="sh-w">{UI["copy"]}</span></button>'
            f'</div><span class="vh" role="status" aria-live="polite"></span></div>')


def touches(b, credits, written):
    """Each heading's drawn mark becomes its anchor; each hail with a marker line gets its label; "written by", the end's share row and the
    credits follow the quotation; the end links follow the foot."""
    b = re.sub(r'<(h[23]) id="([^"]+)">', r'<\1 id="\2"><a class="hm" href="#\2" aria-hidden="true" tabindex="-1"></a>', b)

    def label(m):
        mk = re.search(r'<span class="k">marker:</span> <span class="v">([A-Z]+)', m.group(2))
        return f'<pre class="{m.group(1)}" data-label="hail · {mk.group(1)}">' + m.group(2) if mk else m.group(0)
    b = re.sub(r'<pre class="(ex(?: lit-ex)?)">(.*?</pre>)', label, b, flags=re.S)
    box = (f'<aside class="credits" aria-labelledby="credits-t"><h2 class="ct" id="credits-t">{UI["credits"]}</h2>'
           + "".join(f"<p>{text_node(x)}</p>" for x in credits) + "</aside>")
    i = b.index('<section class="ending"')
    j = b.index("</section>", i) + len("</section>")
    b = b[:j] + "\n" + written + "\n" + box + b[j:]
    end = f'\n<nav class="end" aria-label="blog"><a href="index.html">{UI["all"]}</a><a href="feed.xml" type="application/rss+xml">{UI["rss"]}</a></nav>'
    i = b.index('<p class="foot">')
    j = b.index("</p>", i) + 4
    return b[:j] + end + b[j:]


def contents(body):
    """The contents: each h2 but the TL;DR's tab, the credits' title and "written by", each h3 after it in a list nested inside it."""
    items = []
    for m in re.finditer(r'<h([23])((?: [a-z-]+="[^"]*")*)>(.*?)</h\1>', body, re.S):
        level, attrs, text = m.groups()
        if re.search(r'class="(t|ct|wt)"', attrs):
            continue
        hid, label = re.search(r'id="([^"]+)"', attrs).group(1), re.sub(r"<[^>]+>", "", text)
        a = f'<a href="#{hid}">{label}</a>'
        if level == "2":
            items.append([a, []])
        elif items:
            items[-1][1].append(a)
    return "".join(f"<li>{a}" + (f"<ol>{''.join(f'<li>{x}</li>' for x in sub)}</ol>" if sub else "") + "</li>" for a, sub in items)


# --- the pages --------------------------------------------------------------------------------------------------------------------------------
def render(name, ctx):
    s = (SRC / "templates" / name).read_text(encoding="utf-8")
    s = re.sub(r'\{%\s*include\s+"([^"]+)"\s*%\}', lambda m: render(m.group(1), ctx).rstrip("\n"), s)

    def slot(m):
        if m.group(1) not in ctx:
            refuse(f"{name}: no value for {m.group(1)}")
        return str(ctx[m.group(1)])
    return re.sub(r"\{\{\s*([a-z_]+)\s*\}\}", slot, s)


def pub_date(day):
    """A post's date as RSS writes it, at midnight on the day, in the site's own time zone."""
    try:
        from zoneinfo import ZoneInfo
        zone = ZoneInfo("Europe/Berlin")
    except Exception:                                          # no time zone data: midnight UTC
        zone = datetime.timezone.utc
    return datetime.datetime.combine(datetime.date.fromisoformat(day), datetime.time(), zone).strftime("%a, %d %b %Y %H:%M:%S %z")


def build(site):
    out = site / "blog"
    if out.exists():
        refuse(f"{out} is already there")
    posts = sorted((Post(p) for p in sorted((SRC / "posts").glob("*.md"))), key=lambda p: p.meta["date"], reverse=True)
    if not posts:
        refuse("blog/posts holds no post")
    (out / "assets").mkdir(parents=True)
    (out / "fonts").mkdir()
    (out / "assets/seats").mkdir()
    (out / "assets/authors").mkdir()
    (out / "assets/blog.css").write_text((SRC / "css/base.css").read_text(encoding="utf-8") + "\n" + (SRC / "css/m2.css").read_text(encoding="utf-8"),
                                         encoding="utf-8")
    shutil.copyfile(SRC / "js/blog.js", out / "assets/blog.js")
    for name, (neutral, prefix) in FONTS.items():
        source = ROOT / "docs/assets/fonts" / name
        if prefix and not hashlib.sha256(source.read_bytes()).hexdigest().startswith(prefix):
            refuse(f"{name} is not the latin subset the blog was drawn with")
        shutil.copyfile(source, out / "fonts" / neutral)
    pricke = re.search(r' d="([^"]+)"', (ROOT / "overrides/.icons/shoalmark/pricke.svg").read_text(encoding="utf-8")).group(1)
    preview_alt = html.unescape(re.search(r'assets/preview\.png">\n\s*<meta property="og:image:width" content="1200">\n\s*<meta property="og:image:height" '
                                          r'content="630">\n\s*<meta property="og:image:alt" content="([^"]+)">',
                                          (ROOT / "overrides/main.html").read_text(encoding="utf-8")).group(1))
    common = {"variant": VARIANT, "pricke": pricke, "root": "", "site_root": "../", "url_start": "../index.html", "url_blog": "index.html",
              "url_docs": "../setup.html", "url_github": GITHUB, "url_imprint": "../imprint.html", "url_privacy": "../privacy.html"}
    rows, items, llms = [], [], []
    for post in posts:
        slug, meta = post.slug, post.meta
        (out / slug).mkdir()
        for f in sorted(post.files.iterdir()):
            shutil.copyfile(f, out / slug / f.name)
        hero = meta["hero"]
        kinds = [codecs(post.files / f).split(".")[0] for f in hero] if isinstance(hero, list) else []
        if kinds != ["hvc1", "avc1"]:
            refuse(f"{post.name}: its hero's page files are not an HEVC file, then an H.264 one")
        if size(post.files / meta["card"]) != (1200, 630):
            refuse(f"{post.name}: its card is not 1200 x 630, the size the head's og:image and og:video name")
        body = post.body()
        owner, seats = post.authors()
        shutil.copyfile(SRC / "authors" / owner["picture"], out / "assets/authors" / owner["picture"])
        for seat in seats:
            shutil.copyfile(ROOT / "brand/seats" / f"{seat['seat']}.svg", out / "assets/seats" / f"{seat['seat']}.svg")
        minutes = -(-post.words() // WPM)
        card = f"{SITE_URL}blog/{slug}/{meta['card']}"
        video = meta.get("video")
        tags = "".join(f'<meta property="{k}" content="{v}">\n' for k, v in (
            ("og:video", f"{SITE_URL}blog/{slug}/{video}"), ("og:video:secure_url", f"{SITE_URL}blog/{slug}/{video}"), ("og:video:type", "video/mp4"),
            ("og:video:width", "1200"), ("og:video:height", "630"))) if video else ""
        title_html = post.title_html()
        ctx = dict(common, title_text=html.escape(meta["title"]), description=html.escape(post.description), canonical=f"{SITE_URL}blog/{slug}.html",
                   date_iso=meta["date"], date_text=meta["date"], title_html=title_html, toc=contents(body), body=body, card_abs=card,
                   card_alt=html.escape(meta["card_alt"]), video_tags=tags, here_blog="", current_blog="", kicker_label=text_node(meta["kicker"]),
                   dek=text_node(meta["dek"]), reading_time=UI["read"].format(n=minutes), md_href=f"{slug}.md", ui_markdown=UI["markdown"],
                   ui_contents=UI["contents"], hero_poster=f"{slug}/{meta['card']}", hero_alt=html.escape(meta["card_alt"]),
                   hero_video_hevc=f"{slug}/{hero[0]}", hero_codec_hevc=codecs(post.files / hero[0]),
                   hero_video_page=f"{slug}/{hero[1]}", hero_codec_page=codecs(post.files / hero[1]),
                   authors=authors(owner, seats), share=share(f"{SITE_URL}blog/{slug}.html", meta["title"]))
        (out / f"{slug}.html").write_text(render("post.html", ctx), encoding="utf-8")
        (out / f"{slug}.md").write_text(post.markdown_version(), encoding="utf-8")
        rows.append(render("_index-row.html", {"href": f"{slug}.html", "title_html": title_html, "date_iso": meta["date"], "date_text": meta["date"],
                                               "kicker_label": text_node(meta["kicker"])}).rstrip("\n"))
        items.append(f"<item>\n<title>{html.escape(meta['title'])}</title>\n<link>{SITE_URL}blog/{slug}.html</link>\n<guid>{SITE_URL}blog/{slug}.html</guid>\n"
                     f"<pubDate>{pub_date(meta['date'])}</pubDate>\n<description>{html.escape(post.description)}</description>\n</item>\n")
        llms.append(f"- [{meta['title']}]({SITE_URL}blog/{slug}.md): {post.description}\n")
        print(f"blog/{slug}.html: {len(post.figures)} figures, {len(post.hails)} hails, {post.words()} words, {minutes} min at {WPM} a minute")
    ictx = dict(common, title_text="Blog · shoalmark", description=html.escape(INDEX_INTRO), canonical=f"{SITE_URL}blog/", index_intro=html.escape(INDEX_INTRO),
                rows="\n".join(rows), card_abs=f"{SITE_URL}assets/preview.png", card_alt=html.escape(preview_alt), here_blog=" is-here",
                current_blog=' aria-current="page"')
    (out / "index.html").write_text(render("index.html", ictx), encoding="utf-8")
    (out / "feed.xml").write_text(
        '<?xml version="1.0" encoding="utf-8"?>\n<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">\n<channel>\n'
        f"<title>{BLOG_NAME}</title>\n<link>{SITE_URL}blog/</link>\n<description>{html.escape(INDEX_INTRO)}</description>\n<language>en</language>\n"
        f'<atom:link href="{SITE_URL}blog/feed.xml" rel="self" type="application/rss+xml"/>\n' + "".join(items) + "</channel>\n</rss>\n", encoding="utf-8")
    (out / "llms.txt").write_text(f"# {BLOG_NAME}\n\n> {INDEX_INTRO}\n\n{LLMS_LINE}\n\n## Posts\n\n" + "".join(llms), encoding="utf-8")
    print(f"blog/: {len(posts)} post(s), the index, feed.xml, llms.txt, assets/blog.css and blog.js, and {len(FONTS)} font files")
    return out


if __name__ == "__main__":
    build(Path(sys.argv[1] if len(sys.argv) > 1 else "site"))
