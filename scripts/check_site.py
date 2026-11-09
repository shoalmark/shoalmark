"""Check migration-critical published pages before uploading the Pages artifact: `check_site.py [site [zensical.toml]]`."""
import datetime
from html.parser import HTMLParser
from pathlib import Path
import posixpath
import sys
import tinycss2
from urllib.parse import unquote, urlsplit

site = Path(sys.argv[1] if len(sys.argv) > 1 else "site")
for page in ("index.html", "de/index.html", "how-it-works.html", "de/how-it-works.html", "setup.html", "signing.html", "de/signing.html", "agents/index.html", "llms.txt",
             "index.md", "how-it-works/index.md", "de/index.md", "de/how-it-works/index.md", "blog/index.html"):
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
            if url.netloc == "shoalmark.tools":
                target = site / unquote(url.path.lstrip("/"))
            elif not url.scheme and not url.netloc and url.path:
                path = unquote(url.path)
                if path.startswith("/"):
                    target = site / path.lstrip("/")
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
        if url.netloc != "shoalmark.tools" or not url.path.startswith("/") \
                or not (site / unquote(url.path.lstrip("/"))).is_file():
            raise SystemExit(f"site check: link preview image not in the site, in {self.page}: {attrs.get('content')}")


for page in site.rglob("*.html"):
    PreviewImage(page.relative_to(site)).feed(page.read_text(encoding="utf-8"))

# Parse CSS syntax: font sources may be extensionless, escaped, or nested in at-rules.
def asset_target(page, value, kind):
    url = urlsplit(value)
    if url.scheme or url.netloc:
        raise SystemExit(f"site check: external {kind} in {page}: {value}")
    path = unquote(url.path)
    if path.startswith("/"):
        target = site / path.lstrip("/")
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
SITE_URL = "https://shoalmark.tools/"
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
LOADS = {"script": "src", "img": "src", "source": "src", "iframe": "src", "frame": "src", "audio": "src", "video": "src", "track": "src", "embed": "src",
         "object": "data", "form": "action"}
LOADING_RELS = {"stylesheet", "icon", "shortcut", "preload", "modulepreload", "prefetch", "prerender", "preconnect", "dns-prefetch", "manifest",
                "apple-touch-icon", "mask-icon"}
SVG_LOADS = {"image", "feimage", "use", "script"}
REQUEST_APIS = re.compile(r"\b(fetch|XMLHttpRequest|sendBeacon|WebSocket|EventSource|importScripts)\s*\(|\bimport\s*\(|new\s+Image\b")
STATIC_IMPORT = re.compile(r"\bimport\s*(?:[\w$*{},\s]+?\s*from\s*)?(['\"])(.+?)\1")
CSS_URL = re.compile(r"(?i)url\(\s*(?:(['\"])(.*?)\1|([^'\")\s][^)\s]*))\s*\)|@import\s+(['\"])(.*?)\4")
CSS_IMAGE_SET = re.compile(r"(?i)image-set\(((?:[^()]|\([^()]*\))*)\)")
LEGAL = {"en": ("imprint.html", "privacy.html"), "de": ("de/impressum.html", "de/datenschutz.html")}
TAPE_KINDS = {"tape", "tapebox", "flap", "taped", "taped-why", "is-taped"}
TWIN_PAD = ".door-again .btn.door"
PHONE_WIDTHS = (320, 360, 390, 700)


def css_parts(tokens):
    parts = [[]]
    for token in tokens:
        if token.type == "literal" and token.value == ",":
            parts.append([])
        elif token.type != "comment":
            parts[-1].append(token)
    return parts


def selector_items(tokens):
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token.type == "literal" and token.value in {".", ":"}:
            kind = "class" if token.value == "." else "pseudo"
            i += 1
            if i < len(tokens) and tokens[i].type == "literal" and tokens[i].value == ":":
                kind = "element"
                i += 1
            if i < len(tokens):
                yield kind, tokens[i]
        else:
            yield token.type, token
        i += 1


def weight(tokens):
    weights = []
    for part in css_parts(tokens):
        ids, classes, types = 0, 0, 0
        for kind, token in selector_items(part):
            if kind == "hash" and token.is_identifier:
                ids += 1
            elif kind in {"class", "[] block"}:
                classes += 1
            elif kind == "ident":
                types += 1
            elif kind == "pseudo":
                name = token.lower_name if token.type == "function" else token.value.lower()
                if name in {"is", "not", "has"} and token.type == "function":
                    extra = weight(token.arguments)
                    ids, classes, types = ids + extra[0], classes + extra[1], types + extra[2]
                elif name not in {"where", "before", "after", "first-line", "first-letter"}:
                    classes += 1
        weights.append((ids, classes, types))
    return max(weights)


def reaches_twin(tokens):
    tokens = [token for token in tokens if token.type != "comment"]
    while tokens and tokens[-1].type == "whitespace":
        tokens.pop()
    compound = []
    for token in tokens:
        if token.type == "whitespace" or (token.type == "literal" and token.value in {">", "+", "~", "||"}):
            compound = []
        else:
            compound.append(token)
    for kind, token in selector_items(compound):
        if kind == "hash" or (kind == "class" and token.value not in {"btn", "door"}) or (kind == "ident" and token.value.lower() != "a"):
            return False
    return True


def media_applies(tokens, width):
    for part in css_parts(tokens):
        terms = [t for t in part if t.type != "whitespace"]
        if terms and terms[0].type == "ident" and terms[0].lower_value == "only":
            terms = terms[1:]
        applies = True
        if terms and terms[0].type == "ident" and terms[0].lower_value in {"screen", "all", "print"}:
            applies = terms.pop(0).lower_value != "print"
            if terms:
                if terms[0].type != "ident" or terms.pop(0).lower_value != "and":
                    return True
        for i, term in enumerate(terms):
            if i % 2:
                if term.type != "ident" or term.lower_value != "and":
                    return True
            elif term.type == "() block":
                feature = [t for t in term.content if t.type not in {"whitespace", "comment"}]
                if (len(feature) == 3 and feature[0].type == "ident" and feature[0].lower_value in {"min-width", "max-width"}
                        and feature[1].type == "literal" and feature[1].value == ":"
                        and feature[2].type == "dimension" and feature[2].lower_unit == "px"):
                    applies = applies and (width >= feature[2].value if feature[0].lower_value == "min-width" else width <= feature[2].value)
            else:
                return True
        if applies:
            return True
    return False


def door_paddings(css):
    found = []

    def walk(rules, media):
        for rule in rules:
            if rule.type == "qualified-rule":
                selectors = [part for part in css_parts(rule.prelude) if reaches_twin(part)]
                for d in tinycss2.parse_declaration_list(rule.content, skip_comments=True, skip_whitespace=True):
                    if d.type != "declaration" or d.lower_name not in {"padding-left", "padding"}:
                        continue
                    values = [t for t in d.value if t.type not in {"whitespace", "comment"}]
                    if d.lower_name == "padding" and 1 <= len(values) <= 4:
                        values = [values[3] if len(values) == 4 else values[1] if len(values) > 1 else values[0]]
                    value = tinycss2.serialize(values).strip()
                    pixels = values[0].value if len(values) == 1 and values[0].type == "dimension" and values[0].lower_unit == "px" else None
                    for part in selectors:
                        selector = " ".join(tinycss2.serialize(part).split())
                        own = not media and selector == TWIN_PAD and d.lower_name == "padding-left" and pixels == 50
                        found.append((media, selector, value, pixels, d.important, weight(part), own))
            elif rule.type == "at-rule" and rule.lower_at_keyword == "media" and rule.content is not None:
                walk(tinycss2.parse_rule_list(rule.content, skip_comments=True, skip_whitespace=True), media + (rule.prelude,))
    walk(tinycss2.parse_stylesheet(css, skip_comments=True, skip_whitespace=True), ())
    return found


TAPE_CSS = re.compile(r"@keyframes\s+tape-[\w-]*|\.btn\.door::after|\.(?:tape|tapebox|flap|taped|taped-why|is-taped)\b|\.btn\.taped\b|\.cue\s+\.(?:was|now)\b")


def srcset_urls(value):
    """The addresses of a srcset: each candidate's address runs to the first space, or ends at its own trailing comma."""
    urls, i = [], 0
    while i < len(value):
        while i < len(value) and (value[i].isspace() or value[i] == ","):
            i += 1
        start = i
        while i < len(value) and not value[i].isspace():
            i += 1
        url = value[start:i]
        if url.endswith(","):
            url = url.rstrip(",")
        else:
            depth = 0
            while i < len(value) and (value[i] != "," or depth):
                depth += {"(": 1, ")": -1}.get(value[i], 0)
                i += 1
        if url:
            urls.append(url)
    return urls


def leaves_site(url):
    """Whether a browser asks another host for `url`: it names a host, or a scheme other than data:, blob: or about:. Browsers drop tabs and line
    breaks anywhere in an address and spaces and control characters around it, read a backslash as a slash, and take the host after any run of
    slashes, so the address is read here as they read it."""
    url = re.sub(r"[\t\n\r]", "", url).strip("".join(chr(c) for c in range(0x21))).replace("\\", "/")
    parts = urlsplit(url)
    return bool(parts.netloc) or url.startswith("//") or parts.scheme not in ("", "data", "blob", "about")


def css_urls_of(css):
    """Every address a piece of CSS names: in url(), in an @import's string, and in each string of an image-set()."""
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    found = [m.group(2) if m.group(1) else m.group(3) if m.group(3) is not None else m.group(5) for m in CSS_URL.finditer(css)]
    found += [s for m in CSS_IMAGE_SET.finditer(css) for s in re.findall(r"['\"]([^'\"]*)['\"]", m.group(1))]
    return [url for url in found if url is not None]


def fail(message):
    raise SystemExit(f"site check: {message}")


class Page(HTMLParser):
    """What the checks below need of a page: its language, title and meta tags, its links, each anchor with its text, the text of each element that has
    an id, the textareas, the dialogs, the inline scripts, the references that make a browser load something, and its text outside scripts and styles."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.lang = self.title = None
        self.meta, self.links, self.anchors, self.texts, self.textareas, self.dialogs, self.scripts, self.loads = {}, [], [], {}, {}, [], [], []
        self.components, self.styles = [], []
        self.text, self.stack = "", []
        self.tapes, self.doors, self.coins, self.cues = [], [], [], []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        kinds = (a.get("class") or "").split()
        if "gcoin" in kinds:
            holder = next((el for el in reversed(self.stack) if el["tag"] in ("a", "button")), None)
            in_door = bool(holder) and holder["tag"] == "a" and "door" in (holder["attrs"].get("class") or "").split()
            self.coins.append((holder["attrs"] if in_door else None, a.get("aria-hidden")))
        if TAPE_KINDS & set(kinds) or a.get("id") == "taped-why":
            self.tapes.append(".".join([tag] + kinds))
        if "door" in kinds:
            self.doors.append((tag, a, any(up["attrs"].get("id") == "start" for up in self.stack)))
        if "cue-t" in kinds:
            self.cues.append(kinds)
        if tag == "html":
            self.lang = a.get("lang")
        elif tag == "meta" and (a.get("name") or a.get("property")):
            self.meta[a.get("name") or a.get("property")] = a.get("content")
        elif tag == "link":
            self.links.append(a)
            if set((a.get("rel") or "").lower().split()) & LOADING_RELS:
                self.loads += [(tag, a["href"])] if a.get("href") else []
                self.loads += [(tag, url) for url in srcset_urls(a.get("imagesrcset") or "")]
        elif tag == "dialog":
            self.dialogs.append(a)
        if tag in LOADS and a.get(LOADS[tag]):
            self.loads.append((tag, a[LOADS[tag]]))
        if tag in ("img", "source"):
            self.loads += [(tag, url) for url in srcset_urls(a.get("srcset") or "")]
        if tag == "video" and a.get("poster"):
            self.loads.append((tag, a["poster"]))
        if tag == "input" and (a.get("type") or "").lower() == "image" and a.get("src"):
            self.loads.append((tag, a["src"]))
        if tag in SVG_LOADS:
            self.loads += [(tag, a[key]) for key in ("href", "xlink:href") if a.get(key)]
        if tag == "base" and a.get("href"):
            self.loads.append((tag, a["href"]))
        if a.get("style"):
            self.styles.append(a["style"])
        if "data-md-component" in a:
            self.components.append(a["data-md-component"])
        if tag not in VOID:
            self.stack.append({"tag": tag, "attrs": a, "text": "", "name": ""})

    def handle_endtag(self, tag):
        if tag in VOID or not any(el["tag"] == tag for el in self.stack):
            return
        while self.stack:
            el = self.stack.pop()
            if el["attrs"].get("id"):
                self.texts[el["attrs"]["id"]] = el["text"]
            if el["tag"] == "a":
                self.anchors.append({"attrs": el["attrs"], "text": " ".join(el["name"].split()), "footer": any(up["tag"] == "footer" for up in self.stack),
                                     "start": any(up["attrs"].get("id") == "start" for up in self.stack)})
            elif el["tag"] == "style":
                self.styles.append(el["text"])
            elif el["tag"] == "textarea" and el["attrs"].get("id"):
                self.textareas[el["attrs"]["id"]] = el["text"]
            elif el["tag"] == "title":
                self.title = el["text"].strip()
            elif el["tag"] == "script":
                self.scripts.append(el["text"])
            if el["tag"] == tag:
                break

    def handle_data(self, data):
        for i, el in enumerate(self.stack):
            el["text"] += data
            if not any(inner["attrs"].get("aria-hidden") == "true" for inner in self.stack[i + 1:]):
                el["name"] += data          # the text a screen reader reads as the element's name: what is aria-hidden inside it is left out
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
    if url.netloc == "shoalmark.tools":
        path = path.lstrip("/")
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
    # what each launch state draws: with the probe on, the primary link is the coin door, lit, with its one coin in it, hidden from screen readers, and #start
    # holds its twin, with a coin of its own, leading where the door leads, in the door's words; with the probe off, neither door nor coin; and in both, no
    # tape over a button, no taped button or line that says why, no second line in the cue and no style for any of them
    styled = TAPE_CSS.search(" ".join(p.styles))
    if p.tapes or len(p.cues) > 1 or any({"was", "now"} & set(kinds) for kinds in p.cues) or styled:
        fail(f"{rel}: the landing draws a tape, the taped state or a second cue line, or styles one: {(p.tapes + [' '.join(k) for k in p.cues[1:]] + ([styled.group(0)] if styled else []))[:3]}")
    if probe_on:
        hero, twins = [a for tag, a, start in p.doors if tag == "a" and not start], [a for tag, a, start in p.doors if tag == "a" and start]
        if (len(p.doors) != 2 or len(hero) != 1 or len(twins) != 1 or hero[0].get("id") != "probe-open" or len(p.coins) != 2
                or any(sum(holder is door for holder, _ in p.coins) != 1 for door in hero + twins)):
            fail(f"{rel}: the probe switch is on, but the primary link is not the coin door with its one coin in it, or #start does not hold the door's twin with its own")
        if any(hidden != "true" for _, hidden in p.coins):
            fail(f"{rel}: the probe switch is on, but the door's coin is read by screen readers")
        door = next(a for a in p.anchors if a["attrs"].get("id") == "probe-open")
        twin = [a for a in p.anchors if a["start"] and "door" in classes(a)]
        if (len(twins) != 1 or twins[0].get("id") or len(twin) != 1 or leads_to(rel, twin[0]["attrs"].get("href") or "") != leads_to(rel, door["attrs"].get("href") or "")
                or twin[0]["attrs"].get("aria-haspopup") != "dialog" or twin[0]["text"] != door["text"]):
            fail(f"{rel}: the probe switch is on, but the door's twin in #start does not lead where the door leads, to the same dialog, in the door's words")
        pads = door_paddings(" ".join(p.styles))
        own = any(pad[6] for pad in pads)
        for width in PHONE_WIDTHS:
            candidates = [(pad[4], pad[5], order, pad) for order, pad in enumerate(pads) if all(media_applies(media, width) for media in pad[0])]
            winner = max(candidates)[3] if candidates else None
            if not own or winner is None or winner[3] is None or winner[3] < 50:
                selector, value = (winner[1], winner[2] + (" !important" if winner[4] else "")) if winner else ("none", "unset")
                fail(f"{rel}: the probe switch is on, but the door's twin does not keep its own padding-left of 50px at every width, so on a phone its label starts "
                     f"on the slot (width: {width}px; winning selector: {selector}; value: {value}; top-level own rule: {own})")
    elif p.doors or p.coins:
        fail(f"{rel}: the probe switch is off, but the coin door or its coin is built")
    buttons = [a for a in p.anchors if "btn" in classes(a) and not a["start"]]
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
        short = SITE_URL + ("de/" if lang == "de" else "") + "probe.txt"
        step2 = [a for a in p.anchors if a["attrs"].get("href") == short]
        if len(step2) != 1 or step2[0]["text"] != short.replace("https://", ""):
            fail(f"{rel}: the dialog's second step does not link to {short} with that address, without its scheme, as the link's text")
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
    label = [a["text"] for a in pages[landing].anchors if "btn" in classes(a) and "alt" not in classes(a) and not a["start"]][0]
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

def source_component(rel, page):
    """The theme's script asks api.github.com for the repository's facts from every element whose data-md-component is "source", and keeps them
    in sessionStorage."""
    if "source" in page.components or 'data-md-component="source"' in (site / rel).read_text(encoding="utf-8"):
        fail(f"{rel} lets the theme's script ask api.github.com for the repository's facts (data-md-component=\"source\")")


def other_hosts(rel, page):
    for tag, url in page.loads:
        if leaves_site(url):
            fail(f"{rel} loads {url} ({tag}), from outside the site")
    for script in page.scripts:
        for found in STATIC_IMPORT.finditer(script):
            if leaves_site(found.group(2)):
                fail(f"an inline script of {rel} imports {found.group(2)}, from outside the site")
    for css in page.styles:
        for url in css_urls_of(css):
            if leaves_site(url):
                fail(f"{rel} loads a stylesheet resource from outside the site: {url[:80]}")
    for found in re.finditer(r"url\(\s*['\"]?\s*((?:[a-zA-Z][\w+.-]*:)?//[^'\")\s]*)", re.sub(r"/\*.*?\*/", "", (site / rel).read_text(encoding="utf-8"), flags=re.S)):
        if leaves_site(found.group(1)):
            fail(f"{rel} loads a stylesheet resource from outside the site: {found.group(1)[:80]}")


def footer_links(parsed):
    """Each page's footer links the imprint and the privacy notice of its language: German under de/, English elsewhere."""
    for target in [target for pair in LEGAL.values() for target in pair]:
        if not (site / target).is_file():
            fail(f"missing {target}, which every page's footer links")
    lacking = {}
    for rel, page in sorted(parsed.items()):
        linked = {in_site(rel, a["attrs"].get("href") or "") for a in page.anchors if a.get("footer")}
        want = LEGAL["de" if rel.startswith("de/") else "en"]
        if not set(want) <= linked:
            lacking[rel] = [target for target in want if target not in linked]
    if lacking:
        fail("a page's footer does not link its language's imprint and privacy notice: "
             + "; ".join(f"{rel} lacks {', '.join(targets)}" for rel, targets in sorted(lacking.items())))


def in_site(rel, href):
    """The file of the site that `href`, on the page `rel`, leads to, relative to the site; None where it leads to another host."""
    url = urlsplit(href)
    if url.netloc == "shoalmark.tools" and url.scheme == "https":
        path = unquote(url.path).lstrip("/")
    elif not url.scheme and not url.netloc:
        path = unquote(url.path)
        path = path.lstrip("/") if path.startswith("/") else posixpath.normpath(posixpath.join(posixpath.dirname(rel), path))
    else:
        return None
    return path + "index.html" if path.endswith("/") or path == "" else path


# no request to any other host: nothing a page loads is from outside the site, no inline script can ask for one, the theme's call to GitHub's API is not built in
parsed = {}
for rel in sorted(path.relative_to(site).as_posix() for path in site.rglob("*.html")):
    page = parsed[rel] = pages.get(rel) or parse(rel)
    other_hosts(rel, page)
    styled = TAPE_CSS.search(" ".join(page.styles))      # every page, the pitch pages among them: no style of the tape-off ceremony or the taped state
    if styled:
        fail(f"{rel} styles the tape-off ceremony or the taped state: {styled.group(0)}")
    for script in page.scripts:
        if REQUEST_APIS.search(script):
            fail(f"an inline script of {rel} can ask for something: {REQUEST_APIS.search(script).group(0)}")
    source_component(rel, page)
for css in site.rglob("*.css"):
    for url in css_urls_of(css.read_text(encoding="utf-8")):
        if leaves_site(url):
            fail(f"{css.relative_to(site)} loads a stylesheet resource from outside the site: {url[:80]}")
print("site check: the landings in two languages, their launch state, How it works, the Markdown twins and requests to no other host passed")
footer_links(parsed)
print(f"site check: each of the {len(parsed)} pages links its language's imprint and privacy notice in its footer")


# --- fenced code: every fenced block of the docs, and of what their includes bring in, builds to a code block, and no page shows a fence as text ----------
# The pages are read where zensical.toml puts them: its docs_dir, its snippets' base_path for each include, in its one-line or its block form, and
# use_directory_urls for the page each one builds to. Both languages are pages of the same docs folder.
project = tomllib.loads(config_path.read_text(encoding="utf-8"))["project"]
docs_dir = config_path.parent / project.get("docs_dir", "docs")
snippets = ((project.get("markdown_extensions") or {}).get("pymdownx") or {}).get("snippets") or {}
snippet_bases = [config_path.parent / base for base in (snippets.get("base_path") or ["."])]
directory_urls = project.get("use_directory_urls", True)
INCLUDE = re.compile(r"""^([ \t]*)(;*)-+8<-+[ \t]+(["'])(.+?)\3$""")
INCLUDE_BLOCK = re.compile(r"^[ \t]*(;*)-+8<-+$")
SECTION_MARK = re.compile(r"(?i)^.*?(;*)-+8<-+[ \t]+\[[ \t]*(start|end)[ \t]*:[ \t]*([a-z][-_0-9a-z]*)[ \t]*\].*$")
PART = re.compile(r"(?i)(.*?)(?:((?::-?[0-9]*){1,2}(?:(?:,(?=[-0-9:])-?[0-9]*)(?::-?[0-9]*)?)*)|(:[a-z][-_0-9a-z]*))?$")
QUOTE = re.compile(r"^[ \t]{0,3}(?:>[ \t]?)+")
FENCE = re.compile(r"^([ \t]*)(`{3,}(?=[^`]*$)|~{3,})")
FENCE_TEXT = ("```", "~~~")
if not docs_dir.is_dir() or not any(docs_dir.rglob("*.md")):
    fail(f"zensical.toml's docs_dir, {docs_dir}, holds no page: the fenced blocks are read from it")


def section_of(lines, name, page, include):
    """The lines between a file's `--8<-- [start:name]` and `--8<-- [end:name]`, as snippets extracts them: another section's markers left out, an
    escaped marker kept with one `;` taken off."""
    picked, inside, found = [], False, False
    for line in lines:
        mark = SECTION_MARK.match(line)
        if mark and inside and mark.group(1):
            line = line[:mark.start(1)] + line[mark.start(1) + 1:]
        elif mark and mark.group(3) == name:
            if not inside and mark.group(2) == "start":
                inside = found = True
                continue
            if inside and mark.group(2) == "start":
                continue
            break
        elif mark and inside:
            continue
        if inside:
            picked.append(line)
    if not found:
        fail(f"{page} includes {include}, and that file holds no section {name}")
    return picked


def included(name, page):
    """What an include brings in: (the file, its lines, whether they are a section). A trailing `:start:end` (or several, by commas) or `:name` is
    split off before the file is looked for in the base paths, and only those lines or that section are taken, as snippets takes them."""
    part = PART.match(name.strip())
    file, ranges, section = part.group(1).strip(), part.group(2), part.group(3)
    found = next((base / file for base in snippet_bases if file and (base / file).is_file()), None)
    if found is None:
        fail(f"{page} includes {name}, which none of the snippets' base paths {[str(base) for base in snippet_bases]} holds")
    lines = found.read_text(encoding="utf-8").expandtabs(4).split("\n")
    if ranges:
        picked = []
        for span in (piece.split(":") for piece in ranges[1:].split(",")):
            start = int(span[0]) if span[0] else None
            start = start if start is None or start < 0 else max(0, start - 1)
            end = int(span[1]) if len(span) > 1 and span[1] else None
            start = min(max(len(lines) + start, 0), len(lines)) if start and start < 0 else start
            end = min(max(len(lines) + 1 + end, 0), len(lines)) if end and end < 0 else end
            picked += lines[start:end]
        return found, picked, False
    if section:
        return found, section_of(lines, section[1:], page, name), True
    return found, lines, False


def expanded(name, page, depth):
    found, lines, section = included(name, page)
    return source_lines(found, page, depth + 1, lines, section)


def source_lines(path, page, depth=0, lines=None, section=False):
    """A page's lines as the build reads them: each include, a `--8<-- "name"` line or a block of names between two `--8<--` lines, replaced by the lines
    it brings in at its indentation; an include marker escaped with `;` kept as text with one `;` taken off, inside a block of names too; outside a section,
    a section's marker lines left out, as snippets leaves them out."""
    if lines is None:
        lines = path.read_text(encoding="utf-8").expandtabs(4).split("\n")
    out, names = [], False
    for line in lines:
        m, block = INCLUDE.match(line), INCLUDE_BLOCK.match(line)
        if m and m.group(2) or block and block.group(1):
            out.append(line.replace(";", "", 1))
            continue
        if names:
            if block:
                names = False
            elif not m and not line.strip():
                out.append("")
            elif not m and not line.strip().startswith(";") and depth < 8:
                out += [line[:len(line) - len(line.lstrip())] + inner for inner in expanded(line.strip(), page, depth)]
            continue
        if block:
            names = True
            continue
        if m and depth < 8:
            out += [m.group(1) + inner for inner in expanded(m.group(4).strip(), page, depth)]
            continue
        mark = None if section else SECTION_MARK.match(line)
        if mark and not mark.group(1):
            continue
        out.append(line[:mark.start(1)] + line[mark.start(1) + 1:] if mark else line)
    return out


def trimmed(lines):
    """A block's lines as a reader compares them: no trailing spaces, no blank line before the first or after the last."""
    lines = [line.rstrip() for line in lines]
    while lines and not lines[0]:
        lines.pop(0)
    while lines and not lines[-1]:
        lines.pop()
    return tuple(lines)


def unquoted(line, depth):
    """`line` with `depth` blockquote markers taken off, as its blockquote hands it on; None where the line holds none, so the quote has ended."""
    if not depth:
        return line
    m = re.match(r"^[ \t]{0,3}(?:>[ \t]?){%d}" % depth, line)
    return line[m.end():] if m else "" if not line.strip() else None


def fenced_blocks(lines):
    """The body of each fenced block, in a blockquote or not, with its quote's markers and its fence's own indentation taken off; a fence that is never
    closed runs to the end of the page, or of its blockquote."""
    blocks, i = [], 0
    while i < len(lines):
        quote = QUOTE.match(lines[i])
        depth = quote.group(0).count(">") if quote else 0
        m = FENCE.match(lines[i][quote.end():] if quote else lines[i])
        if not m:
            i += 1
            continue
        indent, fence = len(m.group(1)), m.group(2)
        close = re.compile(r"^[ \t]*%s{%d,}[ \t]*$" % (re.escape(fence[0]), len(fence)))
        body, j = [], i + 1
        while j < len(lines):
            inner = unquoted(lines[j], depth)
            if inner is None or close.match(inner):
                break
            body.append(inner)
            j += 1
        blocks.append(trimmed(line[indent:] if not line[:indent].strip() else line.lstrip() for line in body))
        i = j + 1 if j < len(lines) and unquoted(lines[j], depth) is not None else j
    return blocks


def built_page(rel):
    if rel.name in ("index.md", "README.md"):
        return (rel.parent / "index.html").as_posix()
    return (rel.with_suffix("") / "index.html").as_posix() if directory_urls else rel.with_suffix(".html").as_posix()


class CodeBlocks(HTMLParser):
    """A built page's code blocks, each <pre>'s text, and the fences it shows as text: outside every <pre> and <code>, script, style and textarea."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.pres, self.fences = [], [], []

    def handle_starttag(self, tag, attrs):
        if tag == "pre":
            self.pres.append([])
        if tag not in VOID:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag in VOID or tag not in self.stack:
            return
        while self.stack and self.stack.pop() != tag:
            pass

    def handle_data(self, data):
        if "pre" in self.stack and self.pres:
            self.pres[-1].append(data)
        elif not {"code", "script", "style", "textarea"} & set(self.stack) and any(f in data for f in FENCE_TEXT):
            self.fences.append(" ".join(data.split())[:60])


def code_blocks(rel):
    found = CodeBlocks()
    found.feed((site / rel).read_text(encoding="utf-8"))
    found.close()
    return found


lost, shown, held = {}, {}, 0
for md in sorted(docs_dir.rglob("*.md")):
    rel = md.relative_to(docs_dir)
    if md.name == "README.md" and (md.parent / "index.md").is_file():
        continue                                              # the folder's index.md is its page; the build leaves this README out
    blocks = fenced_blocks(source_lines(md, rel.as_posix()))
    if not blocks:
        continue
    page = built_page(rel)
    if not (site / page).is_file():
        fail(f"{rel.as_posix()} holds {len(blocks)} fenced block(s), and no {page} is built from it")
    pres = [trimmed("".join(text).split("\n")) for text in code_blocks(page).pres]
    for body in blocks:
        if body in pres:
            pres.remove(body)
        else:
            lost.setdefault(page, []).append(body[0] if body else "(an empty block)")
    held += len(blocks)
for path in sorted(site.rglob("*.html")):
    fences = code_blocks(path.relative_to(site).as_posix()).fences
    if fences:
        shown[path.relative_to(site).as_posix()] = fences
if lost or shown:
    fail("; ".join(
        [f"{page}: {len(firsts)} fenced block(s) do not build to a code block, the first opening {firsts[0][:60]!r}" for page, firsts in sorted(lost.items())]
        + [f"{page} shows a fence as text: {fences[0]!r}" for page, fences in sorted(shown.items())]))
print(f"site check: the {held} fenced block(s) of the docs, in both languages, build to code blocks, and no page shows a fence as text")


# --- the blog: its own English site under blog/, its pages' figures with alt text and a still for readers who turn motion off, its files small ------
# A figure is an <img> inside a <picture>. It may show a GIF as the <img> itself, in a <picture> whose <source media="(prefers-reduced-motion: reduce)">
# names the GIF's still, the PNG beside it named <name>-still.png. A <picture> may offer a GIF in a <source> too, for a narrower screen: a browser takes
# the first <source> that matches, so a <source> for reduced motion that names that GIF's still must stand before it. A figure the blog's script plays
# once shows its still, and names its play-once GIF in a data-once and the still it comes to rest on in a data-still: that still is the GIF's own, and the
# <picture> names it for a reader who turns motion off, by the same two rules. A play-once copy, <name>-once.gif, rests on its figure's still,
# <name>-still.png. A <source> after its picture's <img> is never selected, so it counts for nothing. Every src, srcset, data-once and data-still is a
# file of the site. The blog is English only, with no language pair: each of its pages says lang="en" and carries no hreflang, and each post names its
# Markdown version beside it. Its script, a file of its own, asks for nothing, as an inline script may not. Every file under blog/ is read.
# An animated WebP, told by its own header, holds to the GIF rules, and its still is a WebP: <name>-still.webp, as a GIF's is a PNG.
# Every still these rules name, beside a GIF or an animated WebP, in a data-still, in a srcset of a <source> for reduced motion or as a <video>'s
# poster, which a reader who turns motion off sees in the video's place, is a still by its own bytes, as a browser reads them and not by its name:
# a .png starts with the PNG signature and holds no acTL chunk, and a .webp is a RIFF WEBP file that holds no ANIM chunk and whose VP8X sets no
# animation flag; the chunks are walked, never searched. A still named neither .png nor .webp is refused, but a GIF, which the GIF rules read; and
# a poster must not move at all, as the GIF rules never read a poster.
# Each blog post's ids follow the spec's first edition. Its page's text outside <script> and <style>, every alt and its Markdown version hold no
# ‹yyyymmdd›- and no id that ends in a three-digit counter, and every full id there, a sender's prefix (<team>.<seat>, the seat perhaps with its own
# -<n>, or owner) and -<8 digits>, is <prefix>-<yyyymmdd>T<hhmm>Z-<key>: a real UTC date and minute and a key of 6 characters of lower-case Crockford
# base32. An alt or a hail block holds no three-digit ending standing alone, as in "supersedes -001"; other text may, as code can show "head -100".
# A hail block is a <pre> whose lines, its .ln spans or else its newlines, run from hail/1 to end hail/1, and its own id is its id: line's. Two hail
# blocks with the same own id show the same lines: the same hail may be shown twice, two hails never share an id.
# The blog's index has one <h1>, its opening, and its description and og:description are that heading's words as plain text (its tags dropped,
# its entities read, a no-break space read as a space). Every <img> on it has a width, a height and an alt; the first card's image, the first
# inside a <picture>, loads at once (loading="eager", fetchpriority="high"), and every other image lazily. Every image, srcset entry and
# stylesheet it names is a file of the build, and it holds no "SAMPLE" and no samples/ path: a sample page never ships.
# Every image has alt text but an author's picture, an <img> outside any <picture> whose file is in blog/assets/authors/ or blog/assets/seats/:
# its alt is empty, as the author's name stands beside it as text. The GIF rules hold for every image. A file under blog/ holds at most
# 1,000,000 bytes, but the share video, the one MP4 of the site a post's one og:video names, at most 2,000,000.
BLOG = "blog"
BLOG_LIMIT = 1_000_000
SHARE_VIDEO_LIMIT = 2_000_000                               # the share video's own cap: the file a post's og:video names
AUTHOR_PICTURES = (BLOG + "/assets/authors/", BLOG + "/assets/seats/")
REDUCED_MOTION = "(prefers-reduced-motion:reduce)"          # the media query with its whitespace taken out, as it is compared


def still_of(path):
    """The still of the GIF or the animated WebP at `path`, a path relative to the site: the still beside it, named for it with -still, a PNG
    for a GIF and a WebP for a WebP, so neither format's still stands in for the other's; a play-once copy, named for its figure with -once,
    rests on its figure's still."""
    folder, name = posixpath.split(path)
    stem, suffix = posixpath.splitext(name)
    still = "-still.webp" if suffix.lower() == ".webp" else "-still.png"
    return posixpath.join(folder, (stem[:-len("-once")] if stem.endswith("-once") else stem) + still)


def motion(path):
    """What moves at `path`, a path relative to the site: "GIF" for a .gif, and "animated WebP" for a .webp whose own header says so (the
    RIFF WEBP file's VP8X chunk with its animation flag); None for anything else, a still WebP among them, and for no path."""
    if path is None:
        return None
    if path.lower().endswith(".gif"):
        return "GIF"
    if path.lower().endswith(".webp") and (site / path).is_file():
        head = (site / path).read_bytes()[:21]
        if head[:4] == b"RIFF" and head[8:12] == b"WEBP" and head[12:16] == b"VP8X" and len(head) == 21 and head[20] & 0x02:
            return "animated WebP"
    return None


PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def sniffed(data):
    """What a browser that sniffs `data` takes it for, by its first bytes: "PNG", "GIF" or "WebP"; None for anything else."""
    if data[:8] == PNG_SIGNATURE:
        return "PNG"
    if data[:6] in (b"GIF87a", b"GIF89a"):
        return "GIF"
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        return "WebP"
    return None


def still_problem(path):
    """Why the still at `path`, a path relative to the site, is no still by its own bytes; None when it is one. A still named neither .png nor
    .webp is refused, but one that motion() names, a GIF, which is left to the GIF rules and their own words. A .png still starts with the PNG signature, so a browser that sniffs it finds no GIF or WebP, and
    none of its chunks, walked from the signature to IEND, is acTL, the chunk that makes a PNG move. A .webp still is a RIFF WEBP file: none of
    its chunks, walked to the end its RIFF header gives, is ANIM, and its VP8X, where it has one, sets no animation flag. The chunks are walked by
    their lengths, never searched for the four letters, which compressed data can hold by chance; a chunk that runs past the file is refused."""
    data, name = (site / path).read_bytes(), path.lower()
    if name.endswith(".png"):
        kind = sniffed(data)
        if kind != "PNG":
            return f"its bytes are a {kind}'s, not a PNG's" if kind else "its bytes do not start with the PNG signature"
        i = len(PNG_SIGNATURE)
        while i + 12 <= len(data):
            length, chunk = int.from_bytes(data[i:i + 4], "big"), data[i + 4:i + 8]
            if i + 12 + length > len(data):
                break
            if chunk == b"acTL":
                return "it holds an acTL chunk, so it is an animated PNG"
            if chunk == b"IEND":
                return None
            i += 12 + length
        return "its chunks do not run whole to IEND"
    if name.endswith(".webp"):
        kind = sniffed(data)
        if kind != "WebP":
            return f"its bytes are a {kind}'s, not a WebP's" if kind else "its bytes are not a RIFF WEBP file"
        end, i = 8 + int.from_bytes(data[4:8], "little"), 12
        while i < end:
            length, chunk = int.from_bytes(data[i + 4:i + 8], "little"), data[i:i + 4]
            if end > len(data) or i + 8 + length > end:
                return "its chunks do not run whole to the end its RIFF header gives"
            if chunk == b"ANIM":
                return "it holds an ANIM chunk, so it is an animated WebP"
            if chunk == b"VP8X" and length and data[i + 8] & 0x02:
                return "its VP8X chunk sets the animation flag, so it is an animated WebP"
            i += 8 + length + (length & 1)
        return None
    return None if motion(path) else "it is named neither .png nor .webp, so it is no still these rules read"


class BlogPage(HTMLParser):
    """What the blog's check needs of a page: every address a src, a srcset, a data-once or a data-still names, with its element and attribute, each
    image with its attributes and the sources of the <picture> it stands in, None outside one, the sources of each <picture>, in their order, and each
    element that names a play-once GIF, with its attributes, the sources of its <picture> (None outside one) and, for a <source>, its place among them.
    A browser never selects a <source> that comes after its <picture>'s <img>, so such a source joins neither the picture's sources nor the plays.
    And every still it names: each data-still, each address in the srcset of a <source> for reduced motion, wherever that source stands, and each
    <video>'s poster."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.addresses, self.images, self.pictures, self.source_lists, self.plays = [], [], [], [], []
        self.shown = []                                 # per open <picture>: whether its <img> has come
        self.lang, self.hreflang, self.markdown, self.videos = None, [], [], []
        self.stills = []
        self.text, self.alts, self.pres = [], [], []    # its text outside <script> and <style>, its alts, and each <pre>'s lines
        self.h1, self.in_h1 = [], 0                     # each <h1>'s text, and how deep in one
        self.descs, self.stylesheets = [], []           # each description and og:description, as (which, content); each stylesheet's href
        self.skip, self.pre = 0, None                   # how deep in <script> or <style>; the <pre> being read: its spans, its lines, its text

    def handle_starttag(self, tag, attrs):
        a = {key: value or "" for key, value in attrs}
        if tag in ("script", "style"):
            self.skip += 1
        if tag == "h1":
            self.h1.append("")
            self.in_h1 += 1
        if tag == "meta" and (a.get("name") == "description" or a.get("property") == "og:description"):
            self.descs.append(("description" if a.get("name") == "description" else "og:description", a.get("content", "")))
        if tag == "link" and "stylesheet" in a.get("rel", "").lower().split():
            self.stylesheets.append(a.get("href", ""))
        if "alt" in a:
            self.alts.append(a["alt"])
        if tag == "pre":
            self.pre = {"spans": [], "lines": [], "text": []}
        elif tag == "span" and self.pre is not None:
            line = "ln" in a.get("class", "").split() and not any(self.pre["spans"])
            self.pre["spans"].append(line)
            if line:
                self.pre["lines"].append("")
        if "data-still" in a:
            self.stills.append((tag, "data-still", a["data-still"]))
        if tag == "video" and a.get("poster"):
            self.stills.append((tag, "poster", a["poster"]))
        if tag == "source" and REDUCED_MOTION in re.sub(r"\s+", "", a.get("media", "").lower()):
            self.stills += [(tag, "srcset", url) for url in srcset_urls(a.get("srcset", ""))]
        if tag == "html":
            self.lang = a.get("lang")
        if "hreflang" in a:
            self.hreflang.append(a["hreflang"])
        if tag == "link" and a.get("rel") == "alternate" and a.get("type") == "text/markdown":
            self.markdown.append(a)
        if tag == "meta" and a.get("property") == "og:video":
            self.videos.append(a.get("content", ""))
        if "src" in a:
            self.addresses.append((tag, "src", a["src"]))
        if "srcset" in a:
            self.addresses += [(tag, "srcset", url) for url in srcset_urls(a["srcset"])]
        self.addresses += [(tag, key, a[key]) for key in ("data-once", "data-still") if key in a]
        after_img = tag == "source" and bool(self.shown) and self.shown[-1]
        if tag == "picture":
            self.pictures.append([])
            self.source_lists.append(self.pictures[-1])
            self.shown.append(False)
        elif tag == "source" and self.pictures and not after_img:
            self.pictures[-1].append(a)
        elif tag == "img":
            self.images.append((a, self.pictures[-1] if self.pictures else None))
            if self.shown:
                self.shown[-1] = True
        if "data-once" in a and not after_img:
            sources = self.pictures[-1] if self.pictures else None
            self.plays.append((tag, a, sources, len(sources) - 1 if tag == "source" and sources is not None else None))

    def handle_endtag(self, tag):
        if tag == "picture" and self.pictures:
            self.pictures.pop()
            self.shown.pop()
        if tag in ("script", "style") and self.skip:
            self.skip -= 1
        if tag == "h1" and self.in_h1:
            self.in_h1 -= 1
        if tag == "span" and self.pre is not None and self.pre["spans"]:
            self.pre["spans"].pop()
        if tag == "pre" and self.pre is not None:
            self.pres.append(self.pre["lines"] or "".join(self.pre["text"]).split("\n"))
            self.pre = None

    def handle_data(self, data):
        if not self.skip:
            self.text.append(data)
        if self.in_h1:
            self.h1[-1] += data
        if self.pre is not None:
            self.pre["text"].append(data)
            if any(self.pre["spans"]):
                self.pre["lines"][-1] += data


FULL_ID = re.compile(r"(?<![\w.‹›-])((?:owner|[a-z][a-z0-9]*\.[a-z][a-z0-9-]*?)-(\d{8}|‹yyyymmdd›))([^\s<>\"'`,;()\[\]{}]*)")
LONE_COUNTER = re.compile(r"(?<![^\s…(“\"'\[])-\d{3}(?![\w-])")       # -001 standing alone, as an id's short ending
KEY = re.compile(r"[0-9a-hjkmnp-tv-z]{6}")                    # lower-case Crockford base32: no i, l, o or u
ID_FORM = "<team>.<seat>-<yyyymmdd>T<hhmm>Z-<key>"


def id_problem(text, where, alone=False):
    """The first id in `text` that the spec's first edition does not allow, in the words the check fails with; None where there is none. With
    `alone`, as in an alt or a hail block, a three-digit ending standing alone is refused too."""
    if "‹yyyymmdd›-" in text:
        return f"{where} holds ‹yyyymmdd›-, the counter form of an id"
    for m in FULL_ID.finditer(text):
        head, day, rest = m.groups()
        if re.match(r"-\d{3}(?![0-9A-Za-z])", rest):
            return f"{where} holds the counter id {head + rest[:4]!r}, where an id of the spec's first edition is {ID_FORM}"
        form = re.match(r"T(\d{2})(\d{2})Z-([0-9A-Za-z]+)", rest)
        found = head + (form.group(0) if form else rest)
        if not form or not day.isdigit():
            return f"{where} holds the id {found!r}, which is not {ID_FORM}"
        try:
            datetime.datetime(int(day[:4]), int(day[4:6]), int(day[6:]), int(form.group(1)), int(form.group(2)))
        except ValueError:
            return f"{where} holds the id {found!r}, whose date and minute are no UTC minute"
        if not KEY.fullmatch(form.group(3)):
            return f"{where} holds the id {found!r}, whose key is not 6 characters of lower-case Crockford base32"
        if re.match(r"[-_]\d{3}(?![0-9A-Za-z])", rest[form.end():]):
            return f"{where} holds the counter id {found + rest[form.end():form.end() + 4]!r}, where an id of the spec's first edition is {ID_FORM}"
    lone = LONE_COUNTER.search(text) if alone else None
    return f"{where} holds {lone.group(0)!r}, a three-digit counter's ending standing alone" if lone else None


def one_heading(rel, page, raw):
    """The index's one <h1>, with its description and og:description in its words."""
    plain = lambda text: text.replace("\xa0", " ").strip()
    if len(page.h1) != 1:
        return f"{rel} has {len(page.h1)} <h1>, where the index has one, its opening"
    heading = plain(page.h1[0])
    for name in ("description", "og:description"):
        said = [plain(content) for which, content in page.descs if which == name]
        if said != [heading]:
            return f"{rel}'s {name} reads {said[0] if said else None!r}, not the words of its <h1>, {heading!r}"
    return None


def images_loaded(rel, page, raw):
    """Every image on the index with its width, height and alt; the first card's image at once, every other lazily."""
    first = next((i for i, (_attrs, sources) in enumerate(page.images) if sources is not None), None)
    for i, (attrs, _sources) in enumerate(page.images):
        src = attrs.get("src", "")
        missing = [key for key in ("width", "height", "alt") if key not in attrs]
        if missing:
            return f"{rel} shows the image {src!r} without its {' and '.join(missing)}"
        if i == first and (attrs.get("loading") != "eager" or attrs.get("fetchpriority") != "high"):
            return f'{rel} shows its first card\'s image {src!r} without loading="eager" and fetchpriority="high"'
        if i != first and attrs.get("loading") != "lazy":
            return f'{rel} shows the image {src!r} without loading="lazy", and only the first card\'s image loads at once'
    return None


def files_there(rel, page, raw):
    """Every image, srcset entry and stylesheet the index names, a file of the build."""
    named = ([("image", attrs.get("src", "")) for attrs, _sources in page.images] + [("srcset entry", url) for _tag, key, url in page.addresses if key == "srcset"]
             + [("stylesheet", href) for href in page.stylesheets])
    for kind, url in named:
        target = in_site(rel, url)
        if target is None or not (site / target).resolve().is_relative_to(site.resolve()) or not (site / target).is_file():
            return f"{rel} names the {kind} {url!r}, and that is no file of the build"
    return None


def no_sample(rel, page, raw):
    """No sample page's mark on the index."""
    for mark in ("SAMPLE", "samples/"):
        if mark in raw:
            return f"{rel} holds {mark!r}, the mark of a sample page, which the blog never ships"
    return None


INDEX_GUARDS = (one_heading, images_loaded, files_there, no_sample)


def ids_problem(rel, page, markdown):
    """The first id the blog post page `rel`, with its Markdown version, shows against the spec's first edition, or two hail blocks that share an
    id; None where there is none."""
    hails = []
    for lines in page.pres:
        lines = [line.rstrip() for line in lines]
        while lines and not lines[0]:
            lines.pop(0)
        while lines and not lines[-1]:
            lines.pop()
        if lines and lines[0].strip() == "hail/1" and lines[-1].strip() == "end hail/1":
            hails.append(lines)
    for lines in hails:
        problem = id_problem("\n".join(lines), f"a hail block on {rel}", alone=True)
        if problem:
            return problem
    for alt in page.alts:
        problem = id_problem(alt, f"an alt on {rel}", alone=True)
        if problem:
            return problem
    md = rel[:-len(".html")] + ".md"
    for text, where in (("\n".join(page.text), f"{rel}'s text"), (markdown, md)):
        problem = id_problem(text, where)
        if problem:
            return problem
    for alt in re.findall(r"!\[([^\]]*)\]\(", markdown):
        problem = id_problem(alt, f"an alt in {md}", alone=True)
        if problem:
            return problem
    shown = {}
    for lines in hails:
        own = [l.strip()[len("id:"):].strip() for l in lines if l.strip().startswith("id:")]
        if own and shown.setdefault(own[0], lines) != lines:
            return f"{rel} shows two different hail blocks with the same id, {own[0]}"
    return None


def blog_problem(rel, page):
    """The first thing the blog page `rel` shows that the blog refuses, in the words the check fails with; None where there is none."""
    for tag, attr, url in page.addresses:
        target = in_site(rel, url)
        if target is None or not (site / target).resolve().is_relative_to(site.resolve()) or not (site / target).is_file():
            return f"{rel} names {url!r} ({tag} {attr}), and that is no file of the site"
    for attrs, sources in page.images:
        src = attrs.get("src", "")
        author = sources is None and (in_site(rel, src) or "").startswith(AUTHOR_PICTURES)
        if author and attrs.get("alt") != "":
            return f"{rel} shows the author's picture {src!r} without an empty alt, though the name beside it says who it is"
        if not author and not attrs.get("alt", "").strip():
            return f"{rel} shows the image {src!r} without alt text"
        kind = motion(in_site(rel, src))
        if not kind:
            continue
        if sources is None:
            return f"{rel} shows the {kind} {src!r} outside a <picture>, so a reader who turns motion off gets no still"
        still = still_of(in_site(rel, src))
        if not any(re.sub(r"\s+", "", source.get("media", "").lower()) == REDUCED_MOTION and any(in_site(rel, url) == still for url in srcset_urls(source.get("srcset", "")))
                   for source in sources):
            return f'{rel} shows the {kind} {src!r} in a <picture> with no <source media="(prefers-reduced-motion: reduce)"> whose srcset names its still, {still}'
    for sources in page.source_lists:
        for i, source in enumerate(sources):
            for url in srcset_urls(source.get("srcset", "")):
                kind = motion(in_site(rel, url))
                if not kind:
                    continue
                still = still_of(in_site(rel, url))
                if not any(REDUCED_MOTION in re.sub(r"\s+", "", earlier.get("media", "").lower())
                           and any(in_site(rel, other) == still for other in srcset_urls(earlier.get("srcset", ""))) for earlier in sources[:i]):
                    return (f'{rel} offers the {kind} {url!r} in a <source> with no <source> for reduced motion before it whose srcset names its still, '
                            f'{still}')
    for tag, attrs, sources, place in page.plays:
        once, rest = attrs["data-once"], attrs.get("data-still", "")
        still, kind = still_of(in_site(rel, once)), motion(in_site(rel, once)) or "GIF"
        if in_site(rel, rest) != still:
            return f"{rel} plays the {kind} {once!r} and rests on {rest!r}, which is not its still, {still}"
        if sources is None:
            return f"{rel} plays the {kind} {once!r} outside a <picture>, so a reader who turns motion off gets no still"
        names_still = [source for source in (sources if place is None else sources[:place])
                       if any(in_site(rel, url) == still for url in srcset_urls(source.get("srcset", "")))]
        if place is None and not any(re.sub(r"\s+", "", source.get("media", "").lower()) == REDUCED_MOTION for source in names_still):
            return f'{rel} plays the {kind} {once!r} in a <picture> with no <source media="(prefers-reduced-motion: reduce)"> whose srcset names its still, {still}'
        if place is not None and not any(REDUCED_MOTION in re.sub(r"\s+", "", source.get("media", "").lower()) for source in names_still):
            return f"{rel} plays the {kind} {once!r} from a <source> with no <source> for reduced motion before it whose srcset names its still, {still}"
    return None


blog_pages = sorted(path.relative_to(site).as_posix() for path in (site / BLOG).glob("*.html")) if (site / BLOG).is_dir() else []
blog_parsed = {}
for rel in blog_pages:
    blog_parsed[rel] = BlogPage()
    blog_parsed[rel].feed((site / rel).read_text(encoding="utf-8"))
    blog_parsed[rel].close()
for rel, page in blog_parsed.items():
    if len(page.videos) > 1:
        fail(f"{rel} names {len(page.videos)} share videos in og:video, not one")
    for url in page.videos:
        target = in_site(rel, url)
        if target is None or not target.endswith(".mp4") or not (site / target).is_file():
            fail(f"{rel} names {url!r} in og:video, and that is no MP4 file of the site")
share_videos = {in_site(rel, url) for rel, page in blog_parsed.items() for url in page.videos}
blog_files = sorted(path for path in (site / BLOG).rglob("*") if path.is_file()) if (site / BLOG).is_dir() else []
stills = {}                                     # each still the figure rules name, and who names it
for path in blog_files:
    rel = path.relative_to(site).as_posix()
    if motion(rel) and (site / still_of(rel)).is_file():
        stills.setdefault(still_of(rel), f"the still of {rel}")
for rel, page in blog_parsed.items():
    for tag, attr, url in page.stills:
        target = in_site(rel, url)
        if target is not None and (site / target).resolve().is_relative_to(site.resolve()) and (site / target).is_file():
            if attr == "poster" and motion(target):
                fail(f"{rel} shows the {motion(target)} {url!r} as a <video>'s poster: a poster must not move, and the GIF rules never read one")
            stills.setdefault(target, f"a still {rel} names ({tag} {attr})")
for still, named in sorted(stills.items()):
    problem = still_problem(still)
    if problem:
        fail(f"{still}, {named}, is not a still by its own bytes: {problem}")
for path in blog_files:
    rel = path.relative_to(site).as_posix()
    if rel in share_videos and path.stat().st_size > SHARE_VIDEO_LIMIT:
        fail(f"{rel} is {path.stat().st_size:,} bytes, more than the {SHARE_VIDEO_LIMIT:,} a share video, the file a post's og:video names, may hold")
    elif rel not in share_videos and path.stat().st_size > BLOG_LIMIT:
        fail(f"{rel} is {path.stat().st_size:,} bytes, more than the {BLOG_LIMIT:,} a file under {BLOG}/ may hold")
    if motion(rel) and not (site / still_of(rel)).is_file():
        fail(f"{rel} has no still beside it, {still_of(rel)}, for a reader who turns motion off")
    if path.suffix == ".js" and REQUEST_APIS.search(path.read_text(encoding="utf-8")):
        fail(f"{rel}, the blog's script, can ask for something: {REQUEST_APIS.search(path.read_text(encoding='utf-8')).group(0)}")
figures = 0
for rel in blog_pages:
    page = blog_parsed[rel]
    problem = blog_problem(rel, page)
    if problem:
        fail(problem)
    if page.lang != "en" or page.hreflang:
        fail(f"{rel} is not an English page alone: it says lang={page.lang!r}" + (f" and carries hreflang {page.hreflang[0]!r}" if page.hreflang else ""))
    if rel == f"{BLOG}/index.html":
        raw = (site / rel).read_text(encoding="utf-8")
        for guard in INDEX_GUARDS:
            problem = guard(rel, page, raw)
            if problem:
                fail(problem)
    if rel != f"{BLOG}/index.html":
        twin = [a.get("href", "") for a in page.markdown]
        if len(twin) != 1 or in_site(rel, twin[0]) != rel[:-len(".html")] + ".md" or not (site / rel[:-len(".html")]).with_suffix(".md").is_file():
            fail(f"{rel} does not name its Markdown version beside it, {rel[:-len('.html')]}.md, in one <link rel=\"alternate\" type=\"text/markdown\">")
        problem = ids_problem(rel, page, (site / rel[:-len(".html")]).with_suffix(".md").read_text(encoding="utf-8"))
        if problem:
            fail(problem)
    figures += len({id(sources) for _attrs, sources in page.images if sources is not None})         # a figure is a <picture> that shows an image
print(f"site check: the {len(blog_pages)} blog page(s) and their {figures} figure(s) passed: each figure has alt text and a still, each author's picture "
      f"an empty alt, each page is English "
      f"alone and each post names its Markdown version, the blog's script asks for nothing, and each of the {len(blog_files)} file(s) under {BLOG}/ "
      f"is within {BLOG_LIMIT:,} bytes" + (f", but its {len(share_videos)} share video(s), the file(s) og:video names, within {SHARE_VIDEO_LIMIT:,}"
                                             if share_videos else ""))
