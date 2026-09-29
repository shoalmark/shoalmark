"""Check migration-critical published pages before uploading the Pages artifact."""
from html.parser import HTMLParser
from pathlib import Path
import sys
import re
from urllib.parse import unquote, urlsplit

site = Path(sys.argv[1] if len(sys.argv) > 1 else "site")
for page in ("index.html", "setup.html", "signing.html", "de/signing.html", "agents/index.html", "llms.txt"):
    if not (site / page).is_file():
        raise SystemExit(f"site check: missing {page}")
contract = (site / "agents/index.html").read_text(encoding="utf-8")
if "How to get a better-performing human owner" not in contract or "--8" in contract:
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
# Font requests must stay on this site. Check emitted CSS, not merely configuration.
for page in site.rglob("*.css"):
    css = page.read_text(encoding="utf-8")
    for value in re.findall(r"url\(\s*['\"]?([^)'\"\s]+)", css):
        url = urlsplit(value)
        if url.path.lower().endswith((".woff", ".woff2", ".ttf", ".otf")):
            if url.scheme or url.netloc:
                raise SystemExit(f"site check: external font in {page}")
            target = page.parent / unquote(url.path)
            if not target.is_file():
                raise SystemExit(f"site check: missing font in {page}: {value}")
for page in site.rglob("*"):
    if page.is_file() and page.suffix in {".html", ".txt", ".md", ".xml", ".css"}:
        text = page.read_text(encoding="utf-8")
        if page.suffix in {".html", ".css"} and (
            "fonts.googleapis.com" in text or "fonts.gstatic.com" in text
        ):
            raise SystemExit(f"site check: external Google Fonts reference in {page}")
        if "https://holgo99.github.io/shoalmark" in text or "https://github.com/holgo99/shoalmark" in text:
            raise SystemExit(f"site check: old public URL in {page}")
print("site check: entry pages, contract inclusion, landing/contract destinations and public URLs passed")
