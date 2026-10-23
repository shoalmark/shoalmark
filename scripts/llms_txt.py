"""llms.txt (https://llmstxt.org) for the built site: an index of the same source, plus a Markdown twin beside every
page so an agent reads what a person reads. No plugin, no dependency — the source pages are already Markdown.

A twin is its page's source with three things done to it, so that it reads as the page does:
- a line `--8<-- "name"` is replaced by the file it names, found in the snippet base paths of zensical.toml as the site's build finds it
  ("How it works" says the words of its launch state this way);
- the picture on "How it works", a figure drawn in HTML, is written as Markdown, so the twin carries no raw HTML;
- a link to another page's source (`setup.md`) leads to that page's twin, wherever the two stand.
While the probe switch of zensical.toml is on, the prompt its dialog shows is also written as probe.txt beside each landing
(probe.txt, de/probe.txt); while it is off, no such file is written."""
import html, os, pathlib, posixpath, re, shutil, sys

try:
    import tomllib
except ImportError:                                           # Python before 3.11: the one zensical itself needs
    import tomli as tomllib

site = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "site")
docs = pathlib.Path("docs")
config = tomllib.loads(pathlib.Path("zensical.toml").read_text(encoding="utf-8"))["project"]
probe_on = bool((config.get("extra") or {}).get("probe"))
snippet_bases = config["markdown_extensions"]["pymdownx"]["snippets"].get("base_path") or ["."]

INCLUDE = re.compile(r'(?m)^--8<-- "([^"]+)"[ \t]*$')
LINK = re.compile(r"(\]\()([^)\s#]+\.md)(#[^)\s]*)?(\))")
WEEK = re.compile(r'<figure class="week"[^>]*>.*?</figure>', re.S)
WEEK_PIECES = re.compile(r'<div class="week-card[^"]*">(?P<card>.*?)</div>(?=\s*<(?:p class="week-arrow"|figcaption))'
                         r'|(?P<arrow><p class="week-arrow"[^>]*>.*?</p>)|<figcaption[^>]*>(?P<caption>.*?)</figcaption>', re.S)


def snippet(name):
    for base in snippet_bases:
        found = pathlib.Path(base) / name
        if found.is_file():
            return found.read_text(encoding="utf-8")
    raise SystemExit(f"llms.txt: a page includes {name}, which none of the snippet base paths {snippet_bases} holds")


def plain(fragment):
    """A fragment of the figure as text: a chip as [chip], code as `code`, every other tag dropped, entities read."""
    fragment = fragment.replace('</span><span class="chip">', '</span> <span class="chip">')
    fragment = re.sub(r'<span class="chip">(.*?)</span>', r"[\1]", fragment, flags=re.S)
    fragment = re.sub(r"<code>(.*?)</code>", r"`\1`", fragment, flags=re.S)
    return html.unescape(re.sub(r"<[^>]+>", "", fragment))


def week_as_markdown(figure):
    """The picture on "How it works" — three cards (a tracker's lines, the board, a commit's diff) and the caption — as Markdown: a bold title,
    the card's lines in a fenced block, an arrow between two cards, the caption in italics."""
    out = []
    for piece in WEEK_PIECES.finditer(figure):
        if piece.group("card") is not None:
            card = piece.group("card")
            title = plain(re.search(r"<h3[^>]*>(.*?)</h3>", card, re.S).group(1)).strip()
            src = re.search(r'<p class="src">(.*?)</p>', card, re.S)
            pre = re.search(r"<pre[^>]*>(.*?)</pre>", card, re.S)
            body = plain(pre.group(1)) if pre else "\n".join(plain(p).strip() for p in re.findall(r"<p>(.*?)</p>", card, re.S))
            out.append(f"**{title}**" + (f" · {plain(src.group(1)).strip()}" if src else "") + "\n\n```\n" + body.strip("\n") + "\n```")
        elif piece.group("arrow") is not None:
            out.append(plain(piece.group("arrow")).strip())
        else:
            out.append("*" + plain(piece.group("caption")).strip() + "*")
    return "\n\n".join(out)


def twin_path(rel):
    """Where the Markdown twin of the source page `rel` (a path under docs/) stands, relative to the site."""
    rel = pathlib.PurePosixPath(rel)
    return rel.parent / "index.md" if rel.name == "index.md" else rel.with_suffix("") / "index.md"


def retarget(text, rel):
    """A relative link to another page's source (`setup.md`) leads to that page's twin, seen from this page's twin."""
    here = posixpath.dirname(twin_path(rel).as_posix()) or "."

    def fix(m):
        if "://" in m.group(2) or m.group(2).startswith("/"):
            return m.group(0)
        target = posixpath.normpath(posixpath.join(posixpath.dirname(rel.as_posix()), m.group(2)))
        if not (docs / target).is_file():
            return m.group(0)
        return m.group(1) + os.path.relpath(twin_path(target).as_posix(), here).replace(os.sep, "/") + (m.group(3) or "") + m.group(4)
    return LINK.sub(fix, text)


pages = []
for md in sorted(docs.rglob("*.md")):
    rel = md.relative_to(docs)
    if rel.parts[0] == "work-tracker":
        continue
    text = md.read_text(encoding="utf-8")
    if text.strip().startswith("--8<--"):                    # an inclusion: the twin is the included file itself
        text = snippet(re.search(r'"([^"]+)"', text).group(1))
    else:
        text = INCLUDE.sub(lambda m: snippet(m.group(1)).rstrip("\n"), text)
        text = WEEK.sub(lambda m: week_as_markdown(m.group(0)), text)
        text = retarget(text, pathlib.PurePosixPath(rel.as_posix()))
    out = site / rel.with_suffix("") / "index.md" if rel.name != "index.md" else site / rel.parent / "index.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
    title = (re.search(r"(?m)^# (.+)$", text) or [None, rel.stem])[1]
    pages.append((rel, title, out.relative_to(site).as_posix()))
lines = ["# shoalmark", "", "> Get a better-performing human Owner. A work tracker that lives in the repository it tracks and puts what needs the Owner first. "
         "The agents' contract is the README; the pages here are for the people who own the repositories.", "", "## The contract for agents", ""]
lines += [f"- [{t}]({p}): the README — vendored into every repository as tools/shoalmark/README.md" for rel, t, p in pages if rel.parts[0] == "agents"]
lines += ["", "## For the Owner", ""] + [f"- [{t}]({p})" for rel, t, p in pages if rel.parts[0] not in ("agents", "de")]
lines += ["", "## Optional", "", "- Deutsch:"] + [f"  - [{t}]({p})" for rel, t, p in pages if rel.parts[0] == "de"]
(site / "llms.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"llms.txt — {len(pages)} pages, each with a Markdown twin")

if probe_on:                                                  # the short address: the prompt each landing's dialog shows, as plain text
    for landing, short in (("index.html", "probe.txt"), ("de/index.html", "de/probe.txt")):
        prompt = re.search(r'<textarea[^>]*\bid="probe-text"[^>]*>(.*?)</textarea>', (site / landing).read_text(encoding="utf-8"), re.S)
        if not prompt:
            raise SystemExit(f"llms.txt: the probe switch is on, but {landing} shows no prompt")
        with open(site / short, "w", encoding="utf-8", newline="") as f:      # as it stands, whatever the system's line ending
            f.write(html.unescape(prompt.group(1)))
    print("probe.txt, de/probe.txt — the prompt, as each landing's dialog shows it")
