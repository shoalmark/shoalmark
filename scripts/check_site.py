"""Check migration-critical published pages before uploading the Pages artifact: `check_site.py [site [zensical.toml]]`."""
from html.parser import HTMLParser
from pathlib import Path
import posixpath
import sys
import tinycss2
from urllib.parse import unquote, urlsplit

site = Path(sys.argv[1] if len(sys.argv) > 1 else "site")
for page in ("index.html", "de/index.html", "how-it-works.html", "de/how-it-works.html", "setup.html", "signing.html", "de/signing.html", "agents/index.html", "llms.txt",
             "index.md", "how-it-works/index.md", "de/index.md", "de/how-it-works/index.md"):
    if not (site / page).is_file():
        raise SystemExit(f"site check: missing {page}")
contract = (site / "agents/index.html").read_text(encoding="utf-8")
if "Get a better-performing human Owner." not in contract or "--8" in contract:
    raise SystemExit("site check: agents' contract include did not render")

class Links(HTMLParser):
    def __init__(self, page):
        super().__init__()
        self.page = page

    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key != "href" or not value:
                continue
            url = urlsplit(value)
            if url.netloc == "github.com" and url.path.startswith("/shoalmark/shoalmark/blob/main/"):
                relative = unquote(url.path[len("/shoalmark/shoalmark/blob/main/"):])
                target = Path(__file__).resolve().parent.parent / relative
                if not target.is_file():
                    raise SystemExit(f"site check: broken repository link in {self.page}: {value}")
                continue
            if url.netloc == "shoalmark.github.io" and url.path.startswith("/shoalmark/"):
                target = site / unquote(url.path[len("/shoalmark/"):])
            elif not url.scheme and not url.netloc and url.path:
                path = unquote(url.path)
                if path.startswith("/shoalmark/"):
                    target = site / path[len("/shoalmark/"):]
                elif path.startswith("/"):
                    raise SystemExit(f"site check: link outside project in {self.page}: {value}")
                else:
                    target = (site / self.page).parent / path
            else:
                continue
            if not target.is_file() and not (target / "index.html").is_file():
                raise SystemExit(f"site check: broken link in {self.page}: {value}")

for page in ("index.html", "de/index.html", "how-it-works.html", "de/how-it-works.html", "agents/index.html"):
    Links(page).feed((site / page).read_text(encoding="utf-8"))


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

# Parse CSS syntax: font sources may be extensionless, escaped, or nested in at-rules.
def asset_target(page, value, kind):
    url = urlsplit(value)
    if url.scheme or url.netloc:
        raise SystemExit(f"site check: external {kind} in {page}: {value}")
    path = unquote(url.path)
    if path.startswith("/shoalmark/"):
        target = site / path[len("/shoalmark/"):]
    elif path.startswith("/"):
        raise SystemExit(f"site check: {kind} outside project in {page}: {value}")
    else:
        target = page.parent / path
    if not target.resolve().is_relative_to(site.resolve()) or not target.is_file():
        raise SystemExit(f"site check: missing {kind} in {page}: {value}")
    return target


def css_urls(tokens):
    for token in tokens:
        if token.type == "error":
            raise SystemExit("site check: malformed CSS font source")
        if token.type == "url":
            yield token.value
        elif token.type == "function" and token.lower_name == "url":
            args = [t for t in token.arguments if t.type not in {"comment", "whitespace"}]
            if len(args) != 1 or args[0].type != "string":
                raise SystemExit("site check: malformed CSS URL")
            yield args[0].value


checked_css = set()


def check_css(page, css):
    def walk(rules):
        for rule in rules:
            if rule.type == "error":
                raise SystemExit(f"site check: malformed CSS in {page}")
            if rule.type == "at-rule" and rule.lower_at_keyword == "import":
                tokens = [t for t in rule.prelude if t.type not in {"comment", "whitespace"}]
                values = [tokens[0].value] if tokens and tokens[0].type == "string" else list(css_urls(tokens))
                for value in values:
                    check_css_file(asset_target(page, value, "stylesheet"))
            elif rule.type == "at-rule" and rule.lower_at_keyword == "font-face":
                for declaration in tinycss2.parse_blocks_contents(rule.content or []):
                    if declaration.type == "declaration" and declaration.lower_name == "src":
                        for value in css_urls(declaration.value):
                            asset_target(page, value, "font")
            elif getattr(rule, "content", None) is not None:
                walk(tinycss2.parse_blocks_contents(rule.content))
    walk(tinycss2.parse_stylesheet(css, skip_comments=True, skip_whitespace=True))


def check_css_file(page):
    key = page.resolve()
    if key not in checked_css:
        checked_css.add(key)
        check_css(page, page.read_text(encoding="utf-8"))


class InlineStyles(HTMLParser):
    def __init__(self, page):
        super().__init__()
        self.page, self.in_style, self.parts = page, False, []

    def handle_starttag(self, tag, attrs):
        if tag == "style":
            self.in_style, self.parts = True, []

    def handle_data(self, data):
        if self.in_style:
            self.parts.append(data)

    def handle_endtag(self, tag):
        if tag == "style" and self.in_style:
            check_css(self.page, "".join(self.parts))
            self.in_style = False


for page in site.rglob("*.css"):
    check_css_file(page)
for page in site.rglob("*.html"):
    InlineStyles(page).feed(page.read_text(encoding="utf-8"))
for page in site.rglob("*"):
    if page.is_file() and page.suffix in {".html", ".txt", ".md", ".xml", ".css"}:
        text = page.read_text(encoding="utf-8")
        if page.suffix in {".html", ".css"} and (
            "fonts.googleapis.com" in text or "fonts.gstatic.com" in text
        ):
            raise SystemExit(f"site check: external Google Fonts reference in {page}")
        if "https://holgo99.github.io/shoalmark" in text or "https://github.com/holgo99/shoalmark" in text:
            raise SystemExit(f"site check: old public URL in {page}")
print("site check: entry pages, contract inclusion, landing/contract destinations, link preview images and public URLs passed")


# --- B1: the landing in two languages, its launch state, How it works, the Markdown twins, and no request to any other host ----------------------------
try:
    import tomllib
except ImportError:                                           # Python before 3.11: the one zensical itself needs
    import tomli as tomllib
import html
import re

config_path = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(__file__).resolve().parent.parent / "zensical.toml"
probe_on = bool((tomllib.loads(config_path.read_text(encoding="utf-8"))["project"].get("extra") or {}).get("probe"))
SITE_URL = "https://shoalmark.github.io/shoalmark/"
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
LOADS = {"script": "src", "img": "src", "source": "src", "iframe": "src", "audio": "src", "video": "src", "embed": "src", "object": "data", "form": "action"}
LOADING_RELS = {"stylesheet", "icon", "shortcut", "preload", "modulepreload", "prefetch", "manifest", "apple-touch-icon", "mask-icon"}
REQUEST_APIS = re.compile(r"\b(fetch|XMLHttpRequest|sendBeacon|WebSocket|EventSource|importScripts)\s*\(|\bimport\s*\(|new\s+Image\b")


def fail(message):
    raise SystemExit(f"site check: {message}")


class Page(HTMLParser):
    """What the checks below need of a page: its language, title and meta tags, its links, each anchor with its text, the text of each element that has
    an id, the textareas, the dialogs, the inline scripts, the references that make a browser load something, and its text outside scripts and styles."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.lang = self.title = None
        self.meta, self.links, self.anchors, self.texts, self.textareas, self.dialogs, self.scripts, self.loads = {}, [], [], {}, {}, [], [], []
        self.text, self.stack = "", []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html":
            self.lang = a.get("lang")
        elif tag == "meta" and (a.get("name") or a.get("property")):
            self.meta[a.get("name") or a.get("property")] = a.get("content")
        elif tag == "link":
            self.links.append(a)
            if set((a.get("rel") or "").split()) & LOADING_RELS and a.get("href"):
                self.loads.append((tag, a["href"]))
        elif tag == "dialog":
            self.dialogs.append(a)
        if tag in LOADS and a.get(LOADS[tag]):
            self.loads.append((tag, a[LOADS[tag]]))
        if tag not in VOID:
            self.stack.append({"tag": tag, "attrs": a, "text": ""})

    def handle_endtag(self, tag):
        if tag in VOID or not any(el["tag"] == tag for el in self.stack):
            return
        while self.stack:
            el = self.stack.pop()
            if el["attrs"].get("id"):
                self.texts[el["attrs"]["id"]] = el["text"]
            if el["tag"] == "a":
                self.anchors.append({"attrs": el["attrs"], "text": " ".join(el["text"].split())})
            elif el["tag"] == "textarea" and el["attrs"].get("id"):
                self.textareas[el["attrs"]["id"]] = el["text"]
            elif el["tag"] == "title":
                self.title = el["text"].strip()
            elif el["tag"] == "script":
                self.scripts.append(el["text"])
            if el["tag"] == tag:
                break

    def handle_data(self, data):
        for el in self.stack:
            el["text"] += data
        if not any(el["tag"] in ("script", "style") for el in self.stack):
            self.text += data


def parse(rel):
    page = Page()
    page.feed((site / rel).read_text(encoding="utf-8"))
    page.close()
    return page


def classes(anchor):
    return (anchor["attrs"].get("class") or "").split()


def leads_to(page, href):
    """The file of the site that `href`, written on the page `page`, leads to, as a path relative to the site."""
    url = urlsplit(href)
    path = unquote(url.path)
    if url.netloc == "shoalmark.github.io" and path.startswith("/shoalmark/"):
        path = path[len("/shoalmark/"):]
    elif not url.scheme and not url.netloc:
        path = posixpath.normpath(posixpath.join(posixpath.dirname(page), path))
    else:
        return None
    return path + "index.html" if path.endswith("/") or path == "" else path


pages = {rel: parse(rel) for rel in ("index.html", "de/index.html", "how-it-works.html", "de/how-it-works.html")}
for rel, lang, other, canonical, image, adopt, how in (
        ("index.html", "en", "de/index.html", SITE_URL, "preview.png", "ADOPT.md", "how-it-works.html"),
        ("de/index.html", "de", "index.html", SITE_URL + "de/", "preview-de.png", "ADOPT.de.md", "de/how-it-works.html")):
    p = pages[rel]
    if p.lang != lang:
        fail(f"{rel} says lang={p.lang!r}, not {lang!r}")
    if [l.get("href") for l in p.links if l.get("rel") == "canonical"] != [canonical]:
        fail(f"{rel} does not name itself its canonical address, {canonical}")
    if {l.get("hreflang"): l.get("href") for l in p.links if l.get("rel") == "alternate" and l.get("hreflang")} != {"en": SITE_URL, "de": SITE_URL + "de/", "x-default": SITE_URL}:
        fail(f"{rel} does not name its twin: rel=alternate with hreflang en, de and x-default (English the default) is missing or wrong")
    switch = [a for a in p.anchors if "lang" in classes(a)]
    if len(switch) != 1 or switch[0]["attrs"].get("hreflang") != ("de" if lang == "en" else "en") or leads_to(rel, switch[0]["attrs"].get("href") or "") != other:
        fail(f"{rel} has no language switch to {other}, named by its hreflang")
    if p.meta.get("og:image") != SITE_URL + "assets/" + image or p.meta.get("og:locale") != ("en_GB" if lang == "en" else "de_DE") or not (p.title and p.meta.get("description")):
        fail(f"{rel}'s link preview is not its language's: image {image}, its locale, title and description")
    buttons = [a for a in p.anchors if "btn" in classes(a)]
    primary, second = [a for a in buttons if "alt" not in classes(a)], [a for a in buttons if "alt" in classes(a)]
    if len(primary) != 1 or len(second) != 1 or leads_to(rel, second[0]["attrs"].get("href") or "") != how:
        fail(f"{rel} has not one primary button and one second button that leads to {how}")
    button = primary[0]
    if probe_on:
        label = p.texts.get(p.dialogs[0].get("aria-labelledby") or "", "").strip() if len(p.dialogs) == 1 else ""
        if button["attrs"].get("id") != "probe-open" or leads_to(rel, button["attrs"].get("href") or "") != ("de/" if lang == "de" else "") + "probe.txt":
            fail(f"{rel}: the probe switch is on, but the primary button does not copy the prompt and lead to probe.txt")
        if not label or not p.textareas.get("probe-text", "").strip():
            fail(f"{rel}: the probe switch is on, but its dialog is not one labelled dialog that shows the prompt")
    else:
        if button["attrs"].get("href") != "https://github.com/shoalmark/shoalmark/blob/main/" + adopt or button["attrs"].get("id") or p.dialogs or "probe-text" in p.textareas:
            fail(f"{rel}: the probe switch is off, but the primary button is not the note's ({adopt}) alone, or a dialog is built")
    releases = [a["attrs"]["href"].rsplit("/", 1)[1] for a in p.anchors if (a["attrs"].get("href") or "").startswith("https://github.com/shoalmark/shoalmark/releases/tag/")]
    label_of = [a["text"] for a in p.anchors if "rel" in classes(a)]
    if len(releases) != 2 or len(set(releases)) != 1 or len(label_of) != 1 or not label_of[0].endswith(releases[0]):
        fail(f"{rel}: the top bar's release label and its link and the footer's link do not name one release")
    twin_text = (site / ("index.md" if lang == "en" else "de/index.md")).read_text(encoding="utf-8")
    goes = button["attrs"].get("href") if not probe_on else SITE_URL + ("de/" if lang == "de" else "") + "probe.txt"
    first_link = re.search(r"\]\(([^)\s]+)\)", twin_text)
    if not first_link or first_link.group(1) != goes or (not probe_on and "probe.txt" in twin_text):
        fail(f"{rel}'s Markdown twin does not lead with the page's own action: its first link is {goes}, and there is no probe.txt while the switch is off")
if pages["index.html"].title == pages["de/index.html"].title or pages["index.html"].meta.get("description") == pages["de/index.html"].meta.get("description"):
    fail("the two landings share a title or a description")

# the launch state: probe.txt exists while the switch is on, holds what the dialog shows, and is nowhere, nor is anything of the dialog, while it is off
for rel, short in (("index.html", "probe.txt"), ("de/index.html", "de/probe.txt")):
    if probe_on:
        if not (site / short).is_file() or (site / short).read_bytes() != pages[rel].textareas["probe-text"].encode("utf-8"):
            fail(f"{short} is missing or is not, byte for byte, the prompt the dialog of {rel} shows")
    elif (site / short).exists():
        fail(f"{short} is built while the probe switch is off")
if not probe_on:
    for found in site.rglob("*"):
        if found.is_file() and found.suffix in {".html", ".md", ".txt", ".json", ".xml"} and ("probe.txt" in found.read_text(encoding="utf-8") or "probe-open" in found.read_text(encoding="utf-8")):
            fail(f"the probe switch is off, but {found.relative_to(site)} speaks of the probe's prompt")

# How it works: each language's page is in its language and names the primary button as its landing labels it; its twin carries no raw HTML and no include
for rel, landing, twin, lang, quote in (("how-it-works.html", "index.html", "how-it-works/index.md", "en", '"%s"'), ("de/how-it-works.html", "de/index.html", "de/how-it-works/index.md", "de", "„%s“")):
    label = [a["text"] for a in pages[landing].anchors if "btn" in classes(a) and "alt" not in classes(a)][0]
    if pages[rel].lang != lang:
        fail(f"{rel} says lang={pages[rel].lang!r}, not {lang!r}")
    text = (site / twin).read_text(encoding="utf-8") if (site / twin).is_file() else fail(f"missing {twin}")
    if quote % label not in " ".join(pages[rel].text.split()) or quote % label not in text:
        fail(f"{rel} or its twin does not name the primary button as the landing labels it, {label!r}")
    if re.search(r"</?[a-zA-Z][a-zA-Z0-9]*[\s/>]", text) or "--8<--" in text or "<!-- state" in text:
        fail(f"{twin} carries raw HTML, an include or a state fence")
# the German start page's twin points to the German pages: every link in it leads to a file of the site, in de/ or the contract
twin_dir = "de"
for target in re.findall(r"\]\(([^)\s#]+)", (site / "de/index.md").read_text(encoding="utf-8")):
    if "://" in target or target.startswith("/"):
        continue
    found = posixpath.normpath(posixpath.join(twin_dir, target))
    if not (site / found).is_file() or not (found.startswith("de/") or found.startswith("agents/")):
        fail(f"the German start page's twin links to {target}, which is no German page's twin of the site")
listed = (site / "llms.txt").read_text(encoding="utf-8")
if not all(f"]({twin})" in listed for twin in ("how-it-works/index.md", "de/index.md", "de/how-it-works/index.md")):
    fail("llms.txt does not list the German start page and both How it works pages")

# no request to any other host: nothing a page loads is from outside the site, no inline script can ask for one, the theme's call to GitHub's API is not built in
for rel in sorted(path.relative_to(site).as_posix() for path in site.rglob("*.html")):
    page = pages.get(rel) or parse(rel)
    for tag, url in page.loads:
        parts = urlsplit(url)
        if parts.scheme in ("http", "https") and not (parts.netloc == "shoalmark.github.io" and parts.path.startswith("/shoalmark/")) or url.startswith("//"):
            fail(f"{rel} loads {url} ({tag}), from outside the site")
    for script in page.scripts:
        if REQUEST_APIS.search(script):
            fail(f"an inline script of {rel} can ask for something: {REQUEST_APIS.search(script).group(0)}")
    if 'data-md-component="source"' in (site / rel).read_text(encoding="utf-8"):
        fail(f"{rel} lets the theme's script ask api.github.com for the repository's facts (data-md-component=\"source\")")
for css in [*site.rglob("*.css"), *site.rglob("*.html")]:
    if re.search(r"url\(\s*['\"]?(?:https?:)?//", re.sub(r"/\*.*?\*/", "", css.read_text(encoding="utf-8"), flags=re.S)):
        fail(f"{css.relative_to(site)} loads a stylesheet resource from outside the site")
print("site check: the landings in two languages, their launch state, How it works, the Markdown twins and requests to no other host passed")
