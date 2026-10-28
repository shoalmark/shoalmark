"""The class test of the board page's placeholders: no value the page puts in is read as a placeholder, whichever value it is, and the page's
data reads back as it went in.

- The placeholders are read from `HTML_PAGE` itself, by this file's own pattern, so a new one joins the test on its own; the tool's
  `PLACEHOLDER_RE` must find each of them.
- A fixture repository puts the names of all the placeholders into each value an input can reach, in runs of names short enough for every
  input's limits, one fixture per run: `shoalmark.toml` (`name`, `tracker_dir`, `blob`, `[headings] acts`), the repository's `labels.yaml`, a
  brand file the board no longer reads, the branch, `SHOALMARK_CMD`, `TRIAGE.md`, a tracker, a deriver's column, a commit's `Worktree:`
  trailer, and the folder of a harness log's first turn in the fixture's home folder.
- Its page is built by the tool's explicit run, with HOME that folder, and read with no browser: the page is cut back into the template's
  own text and the value in each place, so each value is read from its own place. Each script value parses back to what went in, each HTML
  text unescapes back to it, and the vendored renderer is in the page byte for byte.
- `UNREACHED` names each value no input can reach, with why; with the values the fixture reaches, it is every placeholder.

Run: `python3 test_page_placeholders.py` — exit 1 on a failure. `SHOALMARK_PLACEHOLDER_TOOL=<path>` runs it against another copy of the tool,
and `python3 test_page_placeholders.py --mutants` runs it against each of `MUTANTS`, each of which must fail it. test_shoalmark.py runs both.
"""

import contextlib
import html
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

from test_vcs_shared import fixture_saw


HERE = Path(__file__).resolve().parent
PLACEHOLDER = re.compile(r"__[A-Za-z0-9]+(?:_[A-Za-z0-9]+)*__")     # this file's own reading of a placeholder, wider than the tool's
RUN = 60                       # characters of names in one run: a run goes into a folder's name, a branch and a path, inside Windows' path limit
SID, UUID = "abcd1234", "abcd1234-1111-4222-8333-444455556666"

# Each value no input can reach, and why: the tool's own text, or an input it puts in only in a form that holds no `_`.
UNREACHED = {
    "__KINDS__": "the id prefixes of `kinds`, refused unless they are upper-case letters and digits",
    "__COLSPAN__": "a count",
    "__PROOF__": "the tool's own words for how the configuration asks an answer to be proved",
    "__LANG__": "the labels' `lang`, put in only where it is a language tag (letters, digits and hyphens), else `en`",
    "__FAVICON__": "a logo, as base64 under the tool's own media type",
    "__RUNNING__": "the tool's own link, mark and VERSION",
    "__ICONS__": "the tool's own icons",
    "__PALETTE__": "`[palette]`, refused unless it is #rrggbb colours under the tool's own words",
    "__MARKED__": "the vendored renderer",
    "__DAYS__": "`triage_days`, a whole number",
    "__BOTTLE__": "the tool's own number",
}

# The page's fill as it stands at 58d3dd3: a chain of `str.replace` calls, each reading the page the calls before it wrote. The first mutant
# puts it back, and with it the read-at line's `_` written as a character reference.
OLD_CHAIN = r'''    page = (HTML_PAGE.replace("__KINDS__", "|".join(sorted(KINDS, key=len, reverse=True))).replace("__NAME__", html_escape(CONFIG["name"] or ROOT.name))
            .replace("__COLHEADS__", "".join(f'<th class="x">{html_escape(c.lower())}' for c in BOARD_COLUMNS)).replace("__COLSPAN__", str(4 + len(BOARD_COLUMNS))).replace("__BCOLS__", script_json(BOARD_COLUMNS)).replace("__COLS__", script_json(DERIVED_COLUMNS)).replace("__HOME_PATH__", script_json(html_escape(str((TRACKER_DIR / "TRIAGE.md").relative_to(ROOT).as_posix())))[1:-1]).replace("__CMD__", script_json(CMD)[1:-1])
            .replace("__ACTS_HEAD__", script_json(HEAD["acts"])[1:-1]).replace("__PROOF__", script_json(proof_page())))
    logo, labels, _src, warnings, gone = brand()
    for w in warnings:
        print(f"  brand: {w}", file=sys.stderr)
    page = page.replace("__LANG__", labels["lang"] if re.fullmatch(r"[A-Za-z]{2,3}(-[A-Za-z0-9]{1,8})*", labels["lang"]) else "en")
    for path, instead, _key in gone:
        print(f"  brand: {path} is no longer read — {instead}", file=sys.stderr)
    said = lambda key, *a: html_escape(re.sub(r"\{(\d)\}", lambda m: a[int(m.group(1))] if int(m.group(1)) < len(a) else "", labels[key]))
    page = page.replace("__GONE__", f'<p id="w" class="m">{said("brand.gone", " · ".join(f"{path} → {labels[key]}" for path, _i, key in gone))}</p>' if gone else "")
    page = page.replace("__READAT__", read_at_html(read, labels))
    name = html_escape(CONFIG["name"] or ROOT.name)
    page = page.replace("__HEADMARK__", (f'<img alt="" src="{logo[1]}">' if logo else "") + f"<b>{name}</b>")
    page = page.replace("__FAVICON__", f'<link rel="icon" href="{logo[1]}">' if logo else "")
    v = html_escape(__version__)
    page = page.replace("__RUNNING__", f'<p id="r" class="m"><a href="{TOOL_PAGE}" target="_blank" rel="noopener" aria-label="shoalmark on GitHub">'
                        '<svg viewBox="0 0 16 16" width="16" height="16" fill="currentColor" shape-rendering="crispEdges" aria-hidden="true">'
                        f'<path d="{PRICKE}"></path></svg>shoalmark{icon("out")}</a> · <a href="{TOOL_PAGE}/releases/tag/v{v}" target="_blank" rel="noopener" '
                        f'aria-label="release v{v}">v{v}</a></p>')
    page = page.replace("__LABELS__", script_json(labels)).replace("__ICONS__", script_json({k: icon(k) for k in ICONS})).replace("__PALETTE__", palette_css(PALETTE))
    day, day_text = day_html(labels)
    page = page.replace("__DAY__", day.replace("_", "&#95;")).replace("__DAYTEXT__", script_json(day_text).replace("_", "\\u005f"))
    return page.replace("__MARKED__", MARKED.read_text(encoding="utf-8")).replace("__DAYS__", str(TRIAGE_DAYS)).replace("__BOTTLE__", str(BOTTLENECK)).replace("__HOME__", script_json(home)).replace("__REG__", script_json(board_sessions())).replace("__BLOB__", script_json(board_blob())).replace("__BRANCH__", script_json(read.get("branch") or "")).replace(
        "__ROWS__", ",\n".join(rows)
    )
'''
FILL_START = "    # each placeholder's value, read in this order; `fill_page` puts them into the page in one pass\n"
FILL_END = "    return fill_page(HTML_PAGE, values)\n"
ESC = ("    esc = html_escape\n", '    esc = lambda text: html_escape(text).replace("_", "&#95;")\n')


def chain_as_it_stood(src):
    if src.count(FILL_START) != 1 or src.count(FILL_END) != 1 or src.count(ESC[0]) != 1:
        return None
    a, b = src.index(FILL_START), src.index(FILL_END) + len(FILL_END)
    return (src[:a] + OLD_CHAIN + src[b:]).replace(*ESC)


def one_before(name):
    """The mutant that puts one value in before the pass, where the pass reads it."""
    return lambda src: src.replace(FILL_END, f'    return fill_page(HTML_PAGE.replace("{name}", values.pop("{name}")), values)\n') if src.count(FILL_END) == 1 else None


MUTANTS = (
    ("fills the page by the replace chain as it stands at 58d3dd3", chain_as_it_stood),
    ("puts one value in a script's JSON, the branch, in before the pass", one_before("__BRANCH__")),
    ("puts one value in HTML text, the name, in before the pass", one_before("__NAME__")),
)


def tool_path():
    return Path(os.environ.get("SHOALMARK_PLACEHOLDER_TOOL") or HERE / "shoalmark.py").resolve()


def load(tool):
    spec = importlib.util.spec_from_file_location("placeholder_fm_" + str(abs(hash(str(tool)))), tool)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def names_of(template):
    """The template's placeholders, each once, in the order the page first names them."""
    return list(dict.fromkeys(PLACEHOLDER.findall(template)))


def runs(names):
    """The names, joined by `-`, in runs of at most RUN characters: every name is in one run."""
    out = []
    for name in names:
        if out and len(out[-1]) + 1 + len(name) <= RUN:
            out[-1] += "-" + name
        else:
            out.append(name)
    return out


def cut(template, page):
    """{placeholder: [the text in each of its places]}: `page` cut at the template's own text between the placeholders, in order — None where
    the page is not the template with a text in each place, or two placeholders stand side by side with no text to cut at."""
    parts = re.split("(" + PLACEHOLDER.pattern + ")", template)
    if not page.startswith(parts[0]) or not page.endswith(parts[-1]) or any(not t for t in parts[2:-1:2]):
        return None
    at, end, got = len(parts[0]), len(page) - len(parts[-1]), {}
    for i in range(1, len(parts), 2):
        name, text = parts[i], parts[i + 1]
        stop = end if i + 2 == len(parts) else page.find(text, at)
        if stop < 0 or stop > end:
            return None
        got.setdefault(name, []).append(page[at:stop])
        at = stop + len(text)
    return got if at == len(page) else None


def git(cwd, *a, env):
    return subprocess.run(["git", *a], cwd=str(cwd), capture_output=True, text=True, encoding="utf-8", errors="replace", env=env, check=True).stdout


def fixture(area, c, env):
    """A repository and a home folder whose inputs each hold the run of names `c`. Returns (root, home, what each input was given)."""
    root, home, tdir = area / "repo", area / "home", area / "repo" / "docs" / f"T-{c}"
    given = {"run": c, "name": f"N-{c}", "blob": f"https://example.invalid/{c}/blob/main/", "acts": f"A-{c}", "branch": f"p/{c}", "cmd": f"python3 C-{c}",
             "column": f"X-{c}", "cell": f"V-{c}", "title": f"the work W-{c}", "hook": f"h-{c}", "path": f"H-{c}", "worktree": f"WT-{c}",
             "folder": f"F-{c}", "triage": f"docs/T-{c}/TRIAGE.md", "gone": f"docs/T-{c}/brand/theme.css → GT-{c}",
             "labels": {"tagline": f"L-{c}", "brand.gone": f"G-{c} {{0}}", "brand.gone.theme": f"GT-{c}", "read.self": f"R-{c}", "read.about": f"RA-{c}",
                        "read.git.branch": f"RB-{c} {{0}} @ {{1}} at {{2}}", "day.standup.title": f"D-{c}"}}
    (tdir / "brand").mkdir(parents=True)
    git(root, "init", "-q", env=env)
    git(root, "symbolic-ref", "HEAD", f"refs/heads/{given['branch']}", env=env)
    for k, v in (("user.name", "planner"), ("user.email", "planner@seat"), ("commit.gpgsign", "false"), ("core.hooksPath", os.devnull)):
        git(root, "config", k, v, env=env)
    (root / "shoalmark.toml").write_text(f'name = "{given["name"]}"\ntracker_dir = "docs/T-{c}"\nblob = "{given["blob"]}"\n[kinds]\nAP = "Work"\n'
                                         f'[headings]\nacts = "{given["acts"]}"\n', encoding="utf-8")
    (tdir / "AP-001-x.md").write_text(f'---\nid: AP-001\nstatus: In Progress\nconsidered: none\nhook: "{given["hook"]}"\n---\n\n# AP-001 — {given["title"]}\n\n'
                                      "## What is true now\n\n**One thing is left.**\n\n## Done when\n\nit is.\n", encoding="utf-8")
    (tdir / "TRIAGE.md").write_text(f"# Triage\n\n## The current path\n\n{given['path']}\n", encoding="utf-8")
    (tdir / "brand" / "labels.yaml").write_text("".join(f'{k}: "{v}"\n' for k, v in given["labels"].items()), encoding="utf-8")
    (tdir / "brand" / "theme.css").write_text("/* a file the board no longer reads */\n", encoding="utf-8")
    derive = tdir / "derive"
    derive.write_text(f"#!{sys.executable}\nimport json, sys\njson.load(sys.stdin)\n"
                      f"print(json.dumps({{'AP-001': {{{given['column']!r}: {given['cell']!r}}}}}))\n", encoding="utf-8")
    derive.chmod(0o755)
    git(root, "add", "-A", env=env)
    git(root, "commit", "-qm", "the work", env=env)
    git(root, "commit", "-q", "--allow-empty", "-m", f"a step\n\nSession: {SID}\nWorktree: {given['worktree']}", env=env)
    log = home / ".claude" / "projects" / "-fixture" / f"{UUID}.jsonl"
    log.parent.mkdir(parents=True)
    log.write_text(json.dumps({"type": "user", "cwd": str(home / given["folder"]), "message": {"role": "user", "content": "x"}}) + "\n", encoding="utf-8")
    return root, home, tdir, given


@contextlib.contextmanager
def home_of(path):
    saved = {k: os.environ.get(k) for k in ("HOME", "USERPROFILE")}
    os.environ["HOME"] = os.environ["USERPROFILE"] = str(path)
    try:
        yield
    finally:
        for k, v in saved.items():
            os.environ.pop(k, None) if v is None else os.environ.__setitem__(k, v)


def text(fragment):
    """An HTML fragment's text: its tags dropped, its references read."""
    return html.unescape(re.sub(r"<[^>]+>", "", fragment))


def string(inside):
    """A JSON string's inside, as the page's script reads it."""
    return json.loads('"' + inside + '"')


def reads_back(got, given, resume):
    """{placeholder: (it reads back as it went in, what was seen)} for each value the fixture reaches."""
    one = lambda name: got[name][0]
    seen = {}

    def say(name, ok, saw):
        seen[name] = (bool(ok), saw)

    def safely(name, fn, every=False):
        try:
            ok, saw = fn(got[name] if every else one(name))
        except (ValueError, TypeError, KeyError, IndexError, AttributeError, StopIteration) as error:
            ok, saw = False, f"{type(error).__name__}: {error}"
        say(name, ok, saw)

    m = lambda pattern, v: re.fullmatch(pattern, v, re.S)
    safely("__NAME__", lambda v: (html.unescape(v) == given["name"], v))
    safely("__HEADMARK__", lambda v: (m(r"<b>(.*)</b>", v) and html.unescape(m(r"<b>(.*)</b>", v)[1]) == given["name"], v))
    safely("__COLHEADS__", lambda v: (m(r'<th class="x">(.*)', v) and html.unescape(m(r'<th class="x">(.*)', v)[1]) == given["column"].lower(), v))
    safely("__BCOLS__", lambda v: (json.loads(v) == [given["column"]], v))
    safely("__COLS__", lambda v: (json.loads(v) == [given["column"]], v))
    safely("__HOME_PATH__", lambda v: (html.unescape(string(v)) == given["triage"], v))
    safely("__ACTS_HEAD__", lambda v: (string(v) == given["acts"], v))
    safely("__CMD__", lambda vs: (len(vs) > 1 and all(string(v) == given["cmd"] for v in vs), vs), every=True)
    safely("__LABELS__", lambda v: (all(json.loads(v).get(k) == w for k, w in given["labels"].items()), {k: json.loads(v).get(k) for k in given["labels"]}))
    safely("__GONE__", lambda v: (m(r'<p id="w" class="m">(.*)</p>', v) and text(v).startswith(f"G-{given['run']} ") and given["gone"] in text(v), v))

    def read_at(v):
        facts = [text(f).replace("\xa0·", "") for f in re.findall(r'<span class="fact">(.*?)</span>(?= <span class="fact">|</span>)', v, re.S)]
        rc = re.search(r'<code id="rc" hidden>(.*?)</code>', v, re.S)
        summary = re.search(r"<summary>(.*?)</summary>", v, re.S)
        ok = (len(facts) == 2 and facts[0].startswith(f"RB-{given['run']} {given['branch']} @ ") and facts[1] == given["labels"]["read.self"]
              and rc and html.unescape(rc[1]) == given["cmd"] + " --html-only" and summary and html.unescape(summary[1]) == given["labels"]["read.about"])
        return ok, v
    safely("__READAT__", read_at)

    def day(v):
        row = re.search(r'<template id="day-row-standup"><span>(.*?)</span>', v, re.S)
        pre = re.search(r'<template id="day-standup">.*?<pre class="cmd">(.*?)</pre>', v, re.S)
        prompt = json.loads(one("__DAYTEXT__"))["standup"]
        return row and html.unescape(row[1]) == given["labels"]["day.standup.title"] and pre and html.unescape(pre[1]) == prompt and given["cmd"] in prompt, v[:300]
    safely("__DAY__", day)
    safely("__DAYTEXT__", lambda v: (given["cmd"] in json.loads(v)["standup"], v))
    safely("__HOME__", lambda v: (json.loads(v)["path"] == given["path"], v))

    def reg(v):
        data = json.loads(v)
        group = next(g for g in data["groups"] if g[0] == SID)
        return group[2] == given["worktree"] and data["resume"] == resume and given["folder"] in json.dumps(resume), v
    safely("__REG__", reg)
    safely("__BLOB__", lambda v: (json.loads(v) == given["blob"], v))
    safely("__BRANCH__", lambda v: (json.loads(v) == given["branch"], v))

    def rows(v):
        row = next(r for r in json.loads("[" + v + "]") if r[0] == "AP-001")
        return row[6] == given["title"] and row[7] == given["hook"] and row[27] == {given["column"]: given["cell"]}, row[:8] + row[27:28]
    safely("__ROWS__", rows)
    return seen


def run_checks(mutants=False, *, results=None):
    """[(label, ok, detail)]. With `mutants`, each of MUTANTS is run instead, and must fail."""
    results = [] if results is None else results
    add = lambda label, ok, detail="": results.append((label, bool(ok) if ok is not None else None, detail))
    if mutants:
        return run_mutants(add, results)
    tool = tool_path()
    fm = load(tool)
    names = names_of(fm.HTML_PAGE)
    theirs = set(fm.PLACEHOLDER_RE.findall(fm.HTML_PAGE))
    add(f"page · the placeholders are read from the page's template: {len(names)}, and the tool's own pattern finds each of them and no other "
        f"(saw {sorted(set(names) ^ theirs) or 'the same'})", names and set(names) == theirs)
    parts = re.split("(" + PLACEHOLDER.pattern + ")", fm.HTML_PAGE)
    add("page · no two placeholders stand side by side in the template, so the page can be cut back into the template and its values",
        all(parts[2:-1:2]))
    marked = (tool.parent / "vendor").glob("marked-*.js")
    marked = next(iter(sorted(marked)), None)
    env = {k: v for k, v in os.environ.items() if not k.startswith(("GIT_", "SHOALMARK_", "XDG_")) and k != "CODEX_THREAD_ID"}
    env.update(GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1", GIT_TERMINAL_PROMPT="0", PYTHONIOENCODING="utf-8")
    seen, unreached, built = {}, [], []
    for c in runs(names):
        with tempfile.TemporaryDirectory(prefix="shoalmark-ph-") as tmp:
            try:
                root, home, tdir, given = fixture(Path(tmp).resolve(), c, env)
                run_env = dict(env, HOME=str(home), USERPROFILE=str(home), SHOALMARK_CMD=given["cmd"])
                r = subprocess.run([sys.executable, str(tool), "--root", str(root)], cwd=str(root), capture_output=True, text=True, encoding="utf-8",
                                   errors="replace", env=run_env, timeout=300)
                page = (tdir / "index.html").read_text(encoding="utf-8") if (tdir / "index.html").is_file() else ""
                with home_of(home):
                    resume = fm.resume_commands([SID])
            except Exception as error:
                add(f"page · the fixture for the names {c[:40]}…: a fixture step failed", False, fixture_saw(error))
                continue
            got = cut(fm.HTML_PAGE, page)
            built.append((c, r.returncode, got is not None, r.stderr.strip()[-300:]))
            if got is None:
                continue
            for name, (ok, saw) in reads_back(got, given, resume).items():
                seen.setdefault(name, []).append((c, ok, saw))
            unreached.append(got["__MARKED__"] == [marked.read_text(encoding="utf-8")] if marked else False)
            unreached.append(got["__KINDS__"] == ["AP", "AP"] and got["__LANG__"] == ["en"] and got["__FAVICON__"] == [""]
                             and all(v.isdigit() for v in got["__DAYS__"] + got["__COLSPAN__"] + got["__BOTTLE__"])
                             and json.loads(got["__ICONS__"][0]).keys() == fm.ICONS.keys() and "state" in json.loads(got["__PROOF__"][0])
                             and got["__PALETTE__"][0].startswith(":root{") and "shoalmark" in got["__RUNNING__"][0])
    add(f"page · each fixture's explicit run builds its page, and the page is the template with a value in each place (saw "
        f"{[(c[:24], code, cut_, err[-120:]) for c, code, cut_, err in built if code or not cut_]})",
        built and len(built) == len(runs(names)) and all(code == 0 and cut_ for _c, code, cut_, _e in built))
    for name in names:
        if name in UNREACHED:
            continue
        rows = seen.get(name, [])
        add(f"page · {name} reads back as it went in, with the name of every placeholder in it, in {len(rows)} fixture(s)",
            rows and len(rows) == len(runs(names)) and all(ok for _c, ok, _s in rows), next((f"{c[:30]}…: {str(s)[:400]}" for c, ok, s in rows if not ok), ""))
    add(f"page · the values no input can reach are in their places as the tool writes them, the vendored renderer byte for byte; they and the values "
        f"the fixture reaches are every placeholder (saw unnamed {sorted(set(names) - set(UNREACHED) - set(seen))}, named twice "
        f"{sorted(set(UNREACHED) & set(seen))}, not in the page {sorted(set(UNREACHED) - set(names))})",
        unreached and all(unreached) and set(names) == set(UNREACHED) | set(seen) and not set(UNREACHED) & set(seen))
    return results


def run_mutants(add, results):
    """Each of MUTANTS, as a copy of the tool beside its VERSION and vendored renderer, run under this test: each must fail it."""
    source = (HERE / "shoalmark.py").read_text(encoding="utf-8")
    for name, change in MUTANTS:
        with tempfile.TemporaryDirectory(prefix="shoalmark-ph-mutant-") as tmp:
            tool = Path(tmp).resolve() / "tool" / "shoalmark.py"
            (tool.parent / "vendor").mkdir(parents=True)
            shutil.copy(HERE / "VERSION", tool.parent / "VERSION")
            for f in (HERE / "vendor").glob("marked-*.js"):
                shutil.copy(f, tool.parent / "vendor" / f.name)
            mutant = change(source)
            if mutant is not None:
                tool.write_text(mutant, encoding="utf-8")
            r = subprocess.run([sys.executable, str(HERE / "test_page_placeholders.py")], cwd=str(HERE), capture_output=True, text=True, encoding="utf-8",
                               errors="replace", env=dict(os.environ, SHOALMARK_PLACEHOLDER_TOOL=str(tool)), timeout=900) if mutant is not None else None
            failed = [line.strip()[len("FAIL  "):][:90] for line in (r.stdout.splitlines() if r else []) if line.strip().startswith("FAIL  ")]
            add(f"page · the mutant that {name} fails the test (saw {'its text not once in the tool' if mutant is None else f'exit {r.returncode}, failing: {failed}'})",
                mutant is not None and r.returncode == 1 and failed)
    return results


if __name__ == "__main__":
    failed = 0
    for label, ok, detail in run_checks("--mutants" in sys.argv[1:]):
        print(("  ok    " if ok else "  skip  " if ok is None else "  FAIL  ") + label + ("" if ok else f"\n        {detail}" if detail else ""))
        failed += ok is False
    print(f"FAILED: {failed}" if failed else "all green")
    sys.exit(1 if failed else 0)
