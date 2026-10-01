"""llms.txt (https://llmstxt.org) for the built site: an index of the same source, plus a Markdown twin beside every
page so an agent reads what a person reads. No plugin, no dependency — the source pages are already Markdown."""
import pathlib, re, shutil, sys

site = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "site")
docs = pathlib.Path("docs")
pages = []
for md in sorted(docs.rglob("*.md")):
    rel = md.relative_to(docs)
    if rel.parts[0] == "work-tracker":
        continue
    text = md.read_text(encoding="utf-8")
    if text.strip().startswith("--8<--"):                    # an inclusion: the twin is the included file itself
        text = pathlib.Path(re.search(r'"([^"]+)"', text).group(1)).read_text(encoding="utf-8")
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
