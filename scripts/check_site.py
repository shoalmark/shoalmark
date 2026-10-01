"""Check migration-critical published pages before uploading the Pages artifact."""
from html.parser import HTMLParser
from pathlib import Path
import sys
import tinycss2
from urllib.parse import unquote, urlsplit

site = Path(sys.argv[1] if len(sys.argv) > 1 else "site")
for page in ("index.html", "setup.html", "signing.html", "de/signing.html", "agents/index.html", "llms.txt"):
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

for page in ("index.html", "agents/index.html"):
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
