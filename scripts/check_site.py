"""Check migration-critical published pages before uploading the Pages artifact."""
from html.parser import HTMLParser
from pathlib import Path
import sys
from urllib.parse import unquote, urlsplit

site = Path(sys.argv[1] if len(sys.argv) > 1 else "site")
for page in ("index.html", "setup.html", "signing.html", "de/signing.html", "agents/index.html", "llms.txt"):
    if not (site / page).is_file():
        raise SystemExit(f"site check: missing {page}")
contract = (site / "agents/index.html").read_text(encoding="utf-8")
if "How to get a better-performing human owner" not in contract or "--8" in contract:
    raise SystemExit("site check: agents' contract include did not render")

class Links(HTMLParser):
    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key != "href" or not value:
                continue
            url = urlsplit(value)
            if url.netloc == "shoalmark.github.io" and url.path.startswith("/shoalmark/"):
                relative = unquote(url.path[len("/shoalmark/"):])
                target = site / relative
                if not target.is_file() and not (target / "index.html").is_file():
                    raise SystemExit(f"site check: broken landing link {value}")

Links().feed((site / "index.html").read_text(encoding="utf-8"))
for page in site.rglob("*"):
    if page.is_file() and page.suffix in {".html", ".txt", ".md", ".xml"}:
        text = page.read_text(encoding="utf-8")
        if "https://holgo99.github.io/shoalmark" in text or "https://github.com/holgo99/shoalmark" in text:
            raise SystemExit(f"site check: old public URL in {page}")
print("site check: entry pages, contract inclusion, landing destinations and public URLs passed")
