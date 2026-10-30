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
taped_on = bool((tomllib.loads(config_path.read_text(encoding="utf-8"))["project"].get("extra") or {}).get("taped"))
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
        self.buttons, self.tapes, self.button_texts, self.tape_texts = [], [], [], []
        self.tape_holders, self.doors, self.coins = [], [], []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "tape" in (a.get("class") or "").split() or "gcoin" in (a.get("class") or "").split():
            holder = next((el for el in reversed(self.stack) if el["tag"] in ("a", "button")), None)
            kinds = (holder["attrs"].get("class") or "").split() if holder else []
            where = ("door" if holder["tag"] == "a" and "door" in kinds and holder["attrs"].get("id") == "probe-open"
                     else "taped" if holder["tag"] == "button" and "taped" in kinds else "elsewhere") if holder else "elsewhere"
            (self.tape_holders if "tape" in (a.get("class") or "").split() else self.coins).append((where, a.get("aria-hidden")))
        if "door" in (a.get("class") or "").split():
            self.doors.append((tag, a))
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
        if tag == "button" or "tape" in (a.get("class") or "").split():
            (self.buttons if tag == "button" else self.tapes).append(a)
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
                self.anchors.append({"attrs": el["attrs"], "text": " ".join(el["name"].split()), "footer": any(up["tag"] == "footer" for up in self.stack)})
            elif el["tag"] == "style":
                self.styles.append(el["text"])
            elif el["tag"] == "textarea" and el["attrs"].get("id"):
                self.textareas[el["attrs"]["id"]] = el["text"]
            elif el["tag"] == "title":
                self.title = el["text"].strip()
            elif el["tag"] == "script":
                self.scripts.append(el["text"])
            elif el["tag"] == "button" or "tape" in (el["attrs"].get("class") or "").split():
                (self.button_texts if el["tag"] == "button" else self.tape_texts).append(el["text"])
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
if taped_on and probe_on:
    fail("the probe switch is on and the tape too: the two exclude each other")
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
    # the tape-off ceremony, with the probe on alone: its tape and its coin stand in the primary link, the door, hidden from screen readers
    if probe_on:
        if any(where != "door" for where, _ in p.tape_holders + p.coins) or any(tag != "a" or a.get("id") != "probe-open" for tag, a in p.doors):
            fail(f"{rel}: the probe switch is on, but a tape or a coin stands outside the ceremony's door: the taped state's tape is built")
        if any(hidden != "true" for _, hidden in p.tape_holders + p.coins):
            fail(f"{rel}: the probe switch is on, but the ceremony's tape or coin is read by screen readers")
    elif p.doors or p.coins or any(where == "door" for where, _ in p.tape_holders):
        fail(f"{rel}: the probe switch is off, but the tape-off ceremony's door, its coin or its tape is built")
    if taped_on:
        # the taped state: the primary button is a button, not a link — shown, taped over (the tape hidden from screen readers), aria-disabled, named
        # by its reason line through aria-describedby, with no handler; no dialog is built, the second button leads to How it works, the reason line
        # hands the agents the note, and the Markdown twin leads with that note
        taped = [b for b in p.buttons if "btn" in (b.get("class") or "").split()]
        links = [a for a in p.anchors if "btn" in classes(a)]
        note = "https://github.com/shoalmark/shoalmark/blob/main/" + adopt
        if (len(taped) != 1 or "taped" not in (taped[0].get("class") or "").split() or taped[0].get("type") != "button" or taped[0].get("aria-disabled") != "true"
                or taped[0].get("id") or taped[0].get("href") or any(k.startswith("on") for k in taped[0])):
            fail(f"{rel}: the tape is on, but the primary button is not one button, aria-disabled, with no id, link or handler")
        if [t.get("aria-hidden") for t in p.tapes] != ["true"]:
            fail(f"{rel}: the tape is on, but the button carries no tape hidden from screen readers")
        if taped[0].get("aria-describedby") != "taped-why" or not p.texts.get("taped-why", "").strip():
            fail(f"{rel}: the tape is on, but the button is not described by the line that says why")
        if p.dialogs or "probe-text" in p.textareas or any("taped" in script for script in p.scripts):
            fail(f"{rel}: the tape is on, but a dialog is built or a script handles the taped button")
        if len(links) != 1 or "alt" not in classes(links[0]) or leads_to(rel, links[0]["attrs"].get("href") or "") != how or not any(a["attrs"].get("href") == note for a in p.anchors):
            fail(f"{rel}: the tape is on, but the second button does not lead to {how} alone, or no link hands the agents the note ({adopt})")
        releases = [a["attrs"]["href"].rsplit("/", 1)[1] for a in p.anchors if (a["attrs"].get("href") or "").startswith("https://github.com/shoalmark/shoalmark/releases/tag/")]
        label_of = [a["text"] for a in p.anchors if "rel" in classes(a)]
        if len(releases) != 2 or len(set(releases)) != 1 or len(label_of) != 1 or not label_of[0].endswith(releases[0]):
            fail(f"{rel}: the top bar's release label and its link and the footer's link do not name one release")
        first_link = re.search(r"\]\(([^)\s]+)\)", (site / ("index.md" if lang == "en" else "de/index.md")).read_text(encoding="utf-8"))
        if not first_link or first_link.group(1) != note:
            fail(f"{rel}'s Markdown twin does not lead with the note, the action the taped page hands the agents ({note})")
        continue
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

if taped_on:   # the taped page's primary button is a button: the check below reads its label, the tape's words left out, beside the page's links
    for landing in ("index.html", "de/index.html"):
        label = " ".join(pages[landing].button_texts[0].replace(pages[landing].tape_texts[0], " ").split()) if pages[landing].button_texts and pages[landing].tape_texts else ""
        pages[landing].anchors.append({"attrs": {"class": "btn taped"}, "text": label})
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
