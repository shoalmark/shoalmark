"""shoalmark's gate, pinned. Run: `python3 test_shoalmark.py` — no dependency, so a git hook can run it.

Every check builds what it needs in a throwaway repository; nothing here reads a real corpus. main() is called
in-process with an argv list, so a non-zero exit is observable without a subprocess.
"""

import hashlib
import importlib.util
import io
import os
import re
import subprocess
import datetime
import sys
import tempfile
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

# The SUITE reads and writes UTF-8 whatever the machine's locale is (a Windows runner's is cp1252). The TOOL never
# relies on this: it names its encoding on every read and write — a check below holds it to that.
for _s in (sys.stdout, sys.stderr):
    _s.reconfigure(encoding="utf-8", errors="replace")
_rt, _wt = Path.read_text, Path.write_text
Path.read_text = lambda self, encoding="utf-8", errors=None: _rt(self, encoding=encoding, errors=errors)
Path.write_text = lambda self, data, encoding="utf-8", errors=None: _wt(self, data, encoding=encoding, errors=errors)


HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("fm", HERE / "shoalmark.py")
fm = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(fm)

FAILS = []


def check(name, ok):
    print(("  ok    " if ok else "  FAIL  ") + name)
    if not ok:
        FAILS.append(name)


def _try(f):
    try:
        f()
        return True
    except SystemExit:
        return False


def rm_git(root):
    """Remove a scratch .git — Windows refuses to delete git's read-only objects unless they are made writable first."""
    import stat
    shutil.rmtree(root / ".git", onerror=lambda f, p, e: (os.chmod(p, stat.S_IWRITE), f(p)))


def run(root, *argv, git_env=None):
    """The tool, in process. The ambient `GIT_*` variables are stripped for the call — git exports them into every hook,
    so the suite run by the pre-commit hook would otherwise answer for the repository being committed to, not for the
    scratch one it just built (`_ENV` strips them for the same reason). `git_env` puts chosen ones back, on purpose."""
    out, err = io.StringIO(), io.StringIO()
    saved = {k: os.environ.pop(k) for k in [k for k in os.environ if k.startswith("GIT_")]}
    os.environ.update(git_env or {})
    try:
        with redirect_stdout(out), redirect_stderr(err):
            code = fm.main(["--root", str(root), *argv])
    finally:
        for k in git_env or {}:
            os.environ.pop(k, None)
        os.environ.update(saved)
    return code, out.getvalue(), err.getvalue()


def argv_of(f):
    """Every command line `f` hands a subprocess — what the tool actually SENDS, not what its source suggests it sends.
    A regex the tool builds is a string git's own engine reads, and which engine that is differs by platform, so the
    pattern itself is pinned here rather than the answer it happened to give on the machine the suite ran on."""
    seen, real = [], subprocess.run
    subprocess.run = lambda *a, **k: (seen.append(list(a[0]) if a else []), real(*a, **k))[1]
    try:
        f()
    finally:
        subprocess.run = real
    return seen


_ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
_ENV.update(GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t", GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@t")


def git(cwd, *a, day=None):
    env = dict(_ENV, **({"GIT_COMMITTER_DATE": day + "T12:00:00", "GIT_AUTHOR_DATE": day + "T12:00:00"} if day else {}))
    subprocess.run(["git", "-C", str(cwd), "-c", "commit.gpgsign=false", "-c", "core.hooksPath=/dev/null", *a],
                   check=True, capture_output=True, env=env)


def tracker(root, tid, status="In Progress", extra="", body="## What is true now\n\n**One thing is left.**\n\n## Done when\n\nit is.\n", title="t"):
    d = root / "docs" / "work-tracker"
    d.mkdir(parents=True, exist_ok=True)
    p = d / f"{tid}-x.md"
    p.write_text(f'---\nid: {tid}\nstatus: {status}\nconsidered: none\n{extra}hook: "h of {tid}"\n---\n\n# {tid} — {title}\n\n{body}', encoding="utf-8")
    return p


# --- a fresh repository: init, file, gate ---------------------------------------------------------------
with tempfile.TemporaryDirectory() as d:
    root = Path(d).resolve()
    git(root, "init", "-q")
    code, out, _ = run(root, "--init", "--key", "msr")
    check("--init scaffolds the configuration with ONE id space keyed by the project, the triage home and the ignore lines",
          code == 0 and 'MSR = "Work"' in (root / "shoalmark.toml").read_text() and "MSR-001" in out and (root / "docs/work-tracker/TRIAGE.md").exists()
          and "docs/work-tracker/index.html" in (root / ".gitignore").read_text() and "next:" in out)
    home_md = root / "docs/work-tracker/TRIAGE.md"; home_text = home_md.read_text(); fm.configure(root)
    unsaid, unpathed = fm.triage_home()["intent"], fm.triage_home()["path"]
    home_md.write_text(re.sub(r"- \*\*for\*\* — \*e\.g\. [^*]*\*", "- **for** — the stock we sell", home_text))
    said = fm.triage_home()["intent"]; home_md.write_text(home_text)
    lead = re.sub(r"\s+", " ", home_text)
    check("FM-022 · the scaffolded intent starts with a lead-in that names the repository as a whole, and one example per line, in italics; a fresh scaffold has no intent and no path; one line in the Owner's words is the intent, exactly that line — never the lead-in or the examples left around it",
          "*Three lines in your own words about the repository as a whole, never one feature of it: what this repository, all of it, is for · what is true when it works · what no pass or seat may do to get there." in lead
          and all(f"- **{w}** — *e.g. " in home_text for w in ("for", "so that", "never")) and unsaid == "" and unpathed == "" and said == "- **for** — the stock we sell")
    # R11: only the scaffold's exact text is left out — never a line of the Owner's for its italics, its bold or its length
    # the three example lines as the scaffold writes them — read from the tool, else spelled out, so a run of these
    # checks on a tool without the tuple fails them instead of stopping the suite
    ex = getattr(fm, "INTENT_EXAMPLES", ("- **for** — *e.g. a village library's lending, all of it: members, loans, returns and the shelf in one record the librarian trusts*",
                                         "- **so that** — *e.g. a member finds a book and a librarian finds a member in one look, and nothing on loan is lost*",
                                         "- **never** — *e.g. lend what the catalogue does not hold, or drop a member's record before their last loan is back*"))
    cases = {
        "(b) three real lines": ([(ex[0], "- **for** — the stock we sell"), (ex[1], "- **so that** — an order is never promised twice"), (ex[2], "- **never** — a number typed in by hand")],
                                 "- **for** — the stock we sell\n- **so that** — an order is never promised twice\n- **never** — a number typed in by hand"),
        "(c) a line wholly in italics": ([(ex[2], "- **never** — *sell what we lack*")], "- **never** — *sell what we lack*"),
        "(c) a line in bold alone": ([(ex[2], "- **never** — **sell what we lack**")], "- **never** — **sell what we lack**"),
        "(d) a short line": ([(ex[0], "- **for** ok")], "- **for** ok"),
        "(e) the example with one word changed": ([(ex[1], ex[1].replace("finds a book", "finds a film"))], ex[1].replace("finds a book", "finds a film")),
    }
    read_as = {}
    for name, (swaps, _) in cases.items():
        t = home_text
        for a, b in swaps:
            t = t.replace(a, b)
        home_md.write_text(t); read_as[name] = fm.triage_home()["intent"]
    home_md.write_text(home_text)
    wrong = {n: read_as[n] for n, (_, want) in cases.items() if read_as[n] != want}
    check(f"R11 · the intent reader leaves out only the scaffold's exact text: (a) untouched, nothing; (b) three real lines, exactly those; (c) a line in italics or in bold, (d) a short line, (e) an example with one word changed — each read (wrong: {wrong})",
          unsaid == "" and unpathed == "" and not wrong and set(ex) <= set(getattr(fm, "INTENT_SCAFFOLD", ())) and getattr(fm, "INTENT_LEAD", "\0") in home_text and getattr(fm, "INTENT_NOTE", "\0") in home_text)
    before = (root / "shoalmark.toml").read_text()
    (root / "shoalmark.toml").write_text(before + "\n# mine\n")
    run(root, "--init")
    check("--init never overwrites", (root / "shoalmark.toml").read_text().endswith("# mine\n"))
    code, out, _ = run(root, "--new", "Stock is booked per warehouse")
    made = sorted((root / "docs/work-tracker").glob("MSR-*.md"))
    check("--new needs no id prefix where the repository has one: the next free id from the title, and nothing related yet",
          code == 0 and [p.name for p in made] == ["MSR-001-stock-is-booked-per-warehouse.md"] and "Nothing related" in out)
    code, _, err = run(root)
    check("a new tracker without `considered:` is refused — a filing looks first", code == fm.EXIT_LINT and "held against" in err)
    made[0].write_text(made[0].read_text().replace("considered:\n", "considered: none\n"))
    code, out, _ = run(root, "--print-written")
    check("with `considered: none` the gate is green, and --print-written names exactly the INDEX", code == 0 and out.strip() == "docs/work-tracker/INDEX.md")
    check("--check is green on what was just written, and writes nothing", run(root, "--check")[0] == 0)
    made[0].write_text(made[0].read_text().replace("status: Proposed", "status: In Progress"))
    check("--check reports drift with its own exit code", run(root, "--check")[0] == fm.EXIT_DRIFT)
    run(root)
    code, out, _ = run(root, "--new", "Warehouse stock is booked twice")
    de = [dict(id="MSR-00%d" % n, file="MSR-00%d-x.md" % n, hook_full=h, state="") for n, h in ((1, "Mindestbestände je Lager prüfen"), (2, "Fotos verkleinern"))]
    check("related reads words with umlauts whole", [t["id"] for _s, t in fm.related_trackers(de, "Mindestbestände")][:1] == ["MSR-001"])
    check("the second filing is shown the first — the tracker that already owns the words", "MSR-001" in out and "looks first" in out
          and (root / "docs/work-tracker/MSR-002-warehouse-stock-is-booked-twice.md").exists())
    index = (root / "docs/work-tracker/INDEX.md").read_text()
    check("an unfilled triage home is not a path: INDEX.md says none is written, and a hook is shown without its quotation marks",
          "No current path is written" in index and "only the Owner changes it" not in index and '| "' not in index
          and '"path": ""' in (root / "docs/work-tracker/index.html").read_text())
    check("a slug ends on a word and speaks more than ASCII",
          fm.slug_of("Bestände für Stück und Größe — " + "sehr " * 20) == "bestaende-fuer-stueck-und-groesse-sehr-sehr-sehr-sehr-sehr"
          and not fm.slug_of("x " * 80).endswith("-") and len(fm.slug_of("word " * 40)) <= 60)
    code, _, err = run(root, "--triage")
    check("--triage refuses while the Owner has written no current path", code == fm.EXIT_LINT and "names no current path" in err)
    page = (root / "docs/work-tracker/index.html").read_text()
    check("the board is one static page: no unfilled placeholder, the configured kinds in its id patterns, five sections in order",
          not re.search(r"__[A-Z_]+__", page) and "(?:MSR)-" in page
          and re.search(r"BOARD=\{progress:.*triage:.*triaged:.*backlog:.*done:", page, re.S) is not None
          and 'untriaged=t=>t[19]=="triage"||t[2]=="In Progress"&&!fresh(t)' in page and "(7+1)*864e5" in page)
    check("one rendered view per tracker sits beside the page", (root / "docs/work-tracker/view/MSR-001.js").exists())
    second = root / "docs/work-tracker/MSR-002-warehouse-stock-is-booked-twice.md"
    second.write_text(second.read_text().replace("considered:\n", "considered: MSR-001\n"))
    made[0].write_text(made[0].read_text().replace("considered: none\n", "considered: none\ntags: bug\n"))
    check("the kind of work is a tag — `bug` is in the vocabulary, a synonym is refused", run(root)[0] == 0
          and (made[0].write_text(made[0].read_text().replace("tags: bug", "tags: defect")) or run(root)[0] == fm.EXIT_LINT))

# --- configuration: kinds are the repository's own ------------------------------------------------------
with tempfile.TemporaryDirectory() as d:
    root = Path(d).resolve()
    (root / "shoalmark.toml").write_text('name = "lager"\ntracker_dir = "tracker"\n[kinds]\nTASK = "Tasks"\n[considered_from]\nTASK = 5\n')
    (root / "tracker").mkdir()
    (root / "tracker" / "TASK-001-a.md").write_text('---\nid: TASK-001\nstatus: Proposed\nhook: "h"\n---\n\n# TASK-001 — a\n')
    code, _, err = run(root)
    index = (root / "tracker" / "INDEX.md").read_text()
    check("kinds, the tracker directory and the first id owing `considered:` come from shoalmark.toml",
          code == 0 and "## Tasks" in index and "[TASK-001]" in index and "<title>lager — work tracker</title>" in (root / "tracker/index.html").read_text())
    (root / "tracker" / "TASK-001-a.md").write_text('---\nid: TASK-001\nstatus: Proposed\nstaus: x\nhook: "h"\n---\n\n# TASK-001 — a\n')
    code, _, err = run(root)
    check("an unknown front-matter key is refused, and the near miss is named", code == fm.EXIT_LINT and "did you mean `status:`" in err)
    (root / "tracker" / "TASK-001-a.md").write_text('---\nid: TASK-002\nstatus: Proposed\nhook: "h"\n---\n\n# TASK-001 — a\n')
    code, _, err = run(root)
    check("identity drift refuses before anything is written", code == fm.EXIT_LINT and "identity drift" in err)
fm.configure(HERE)

# --- the board, the story rule, the apply layer ---------------------------------------------------------
with tempfile.TemporaryDirectory() as d:
    root = Path(d).resolve()
    fm.configure(root)
    base = dict(id="FEAT-001", num=1, kind="FEAT", status="Proposed", triaged="")
    b = lambda **kw: fm.board(dict(base, **kw))
    check("one board definition: `triage` is exactly what the next pass lists — work in progress and new filings; older undated work is backlog",
          [b(status="Shipped"), b(status="In Progress"), b(status="In Progress", triaged="2026-01-01"), b(status="Parked", triaged="2026-01-01"), b()]
          == ["done", "triage", "progress", "backlog", "triage"]
          and fm.board(dict(base, kind="OLD")) == "backlog")
    row = lambda i, **kw: {**dict(id=i, num=int(i[-1]), kind="FEAT", file=f"{i}-x.md", status="In Progress", links=[], considered=["none"], tags=[], blocked_by=[]), **kw}
    check("a story is open while a chapter is — a done tracker that open work names in `epic:` is refused",
          any("A story is open" in p for p in fm.lint([row("FEAT-001", status="Shipped"), row("FEAT-002", epic="FEAT-001")]))
          and not any("A story is open" in p for p in fm.lint([row("FEAT-001", status="Shipped"), row("FEAT-002", status="Shipped", epic="FEAT-001")])))
    check("a rank names one tracker, on open work only",
          any("also on" in p for p in fm.lint([row("FEAT-001", rank=1), row("FEAT-002", rank=1)]))
          and any("remove it when" in p for p in fm.lint([row("FEAT-001", status="Shipped", rank=1)])))
    check("a blocker is another tracker or the Owner; a tracker cannot block itself",
          any("blocked-by" in p for p in fm.lint([row("FEAT-001", blocked_by=["FEAT-001"])]))
          and not any("blocked-by" in p for p in fm.lint([row("FEAT-001", blocked_by=["Owner — the ruling"]), row("FEAT-002")])))
    for n in (1, 2, 3):
        tracker(root, f"FEAT-00{n}", extra="rank: 1\n" if n == 1 else "")
    (root / "docs/work-tracker/FEAT-004-x.md").write_text("# FEAT-004 — no front matter\n\n---\n\nbody\n")
    tk = [dict(id=f"FEAT-00{n}", file=f"FEAT-00{n}-x.md", rank=1 if n == 1 else 0, triaged="", status="In Progress") for n in (1, 2, 3, 4)]
    hd = "| Tracker | Tier | Verdict | Reason |\n|---|---|---|---|\n"
    sheet = lambda i, v, r="r": f"| [{i}](../../{i}-x.md) — t | P2 | {v} | {r} |\n"
    rd = lambda i: (root / f"docs/work-tracker/{i}-x.md").read_text()
    l1, e1 = fm.apply_worksheet(hd + sheet("FEAT-002", "merge FEAT-003", "keep P3 | see FEAT-003"), True, tk, "2026-01-10")
    check("a `|` typed into the Reason is refused by name — a fragment of the reason never becomes the verdict", not l1 and len(e1) == 1 and "FEAT-002" in e1[0])
    l2, e2 = fm.apply_worksheet(hd + sheet("FEAT-002", "keep #1 run"), True, tk, "2026-01-10")
    check("a verdict that does not stand takes no rank from its holder", e2 and "rank: 1\n" in rd("FEAT-001"))
    l3, e3 = fm.apply_worksheet(hd + sheet("FEAT-002", "keep P1 #2 run") + sheet("FEAT-003", "keep P1 #2 build"), True, tk, "2026-01-10")
    check("one rank names one row on a sheet", len(e3) == 1 and "already claimed by FEAT-002" in e3[0])
    l4, e4 = fm.apply_worksheet(hd + sheet("FEAT-004", "keep P2"), True, tk, "2026-01-10")
    check("a tracker with no front matter is refused and left byte for byte", len(e4) == 1 and rd("FEAT-004").startswith("# FEAT-004 — no front matter"))
    l5, e5 = fm.apply_worksheet(hd + sheet("FEAT-003", "keep P1 #1 build"), True, tk, "2026-01-10")
    check("a rank that moves is freed from its holder, and the move is logged",
          any("rank #1 freed" in l for l in l5) and "rank:" not in rd("FEAT-001") and "rank: 1\n" in rd("FEAT-003") and "next: build\n" in rd("FEAT-003"))
    l6, e6 = fm.apply_worksheet(hd + sheet("FEAT-002", "park P3"), True, tk, "2026-01-10")
    check("a park is applied by the command: status, tier and the date — never by hand", "status: Parked\n" in rd("FEAT-002") and "tier: P3\n" in rd("FEAT-002") and "triaged: 2026-01-10\n" in rd("FEAT-002"))
    l7, e7 = fm.apply_worksheet(hd + sheet("FEAT-001", "keep P1 #3"), True, [dict(t, status="Shipped") if t["id"] == "FEAT-001" else t for t in tk], "2026-01-10")
    check("a tracker that shipped since its verdict is left alone by a same-day re-run", not l7 and not e7)
    fm.configure(root); (root / "shoalmark.toml").write_text('[kinds]\nMSR = "Work"\n'); fm.configure(root)
    _doc = '---\nid: MSR-009\nstatus: In Progress\nhook: "h"\n---\n\n# MSR-009 — t\n'
    check("`epic` and `merge` verdicts read the repository's own id prefix, not a fixed pair",
          "epic: MSR-001\n" in fm.apply_verdict(_doc, "epic MSR-001 P2", "2026-01-10", {"MSR-001"})[0] and not fm.apply_verdict(_doc, "merge MSR-001", "2026-01-10", {"MSR-001"})[2]
          and fm.apply_verdict(_doc, "epic MSR-404 P2", "2026-01-10", {"MSR-001"})[2])
    (root / "shoalmark.toml").unlink(); fm.configure(root)
    check("a P0 or P1 is never parked", fm.apply_verdict(rd("FEAT-003"), "park P1", "2026-01-10", set())[2])

# --- a whole pass, end to end -----------------------------------------------------------------------------
with tempfile.TemporaryDirectory() as d:
    root = Path(d).resolve()
    git(root, "init", "-q")
    run(root, "--init", "--key", "FEAT")
    home = root / "docs/work-tracker/TRIAGE.md"
    home.write_text(home.read_text().replace("1.\n", "1. FEAT-001 to its end.\n").replace("- **never** —", "- **never** — a Jira clone"))
    tracker(root, "FEAT-001"); tracker(root, "FEAT-002"); tracker(root, "FEAT-003", status="Proposed")
    git(root, "add", "-A"); git(root, "commit", "-qm", "file three", day="2020-01-01")
    code, out, _ = run(root, "--triage")
    sheets = sorted((root / "docs/work-tracker/evidence/triage").glob("triage-*.md"))
    text = sheets[0].read_text() if sheets else ""
    check("--triage writes the worksheet, prints the Owner's intent and path above the rules, and lists work in progress and new filings",
          code == 0 and "a Jira clone" in out and "FEAT-001 to its end" in out and "3 trackers to judge" in out
          and "FAILS" in text and "NEW FILING" in text and "ends with fewer" not in out and "BY TODAY'S JUDGEMENT" in out)
    filled = re.sub(r"(\| \[FEAT-001\].*?)\| \| \|\n", r"\1| keep P1 #1 build | the path names it |\n", text)
    filled = re.sub(r"(\| \[FEAT-002\].*?)\| \| \|\n", r"\1| park P3 | nobody is on it; the Owner ranks it |\n", filled)
    sheets[0].write_text(filled)
    code, out, err = run(root, "--triage")
    t1, t2 = (root / "docs/work-tracker/FEAT-001-x.md").read_text(), (root / "docs/work-tracker/FEAT-002-x.md").read_text()
    check("a re-run applies what the seat filled, refreshes the INDEX, and lists what is left",
          "rank: 1\n" in t1 and "next: build\n" in t1 and "status: Parked\n" in t2 and "Applied 2" in out and "1 trackers to judge" in out
          and "| 1 | P1 | build |" in (root / "docs/work-tracker/INDEX.md").read_text())

# --- git-derived facts: the keep test stands on these -----------------------------------------------------
with tempfile.TemporaryDirectory() as d:
    root = Path(d).resolve()
    git(root, "init", "-q")
    fm.configure(root)
    wt = root / "docs/work-tracker"; wt.mkdir(parents=True)
    names = [f"BUG-{n:03d}-x.md" for n in range(1, 11)]
    for n in names:
        (wt / n).write_text("a\n")
    git(root, "add", "-A"); git(root, "commit", "-qm", "file ten", day="2026-01-01")
    (wt / names[0]).write_text("b\n"); git(root, "commit", "-qam", "fix: real work", day="2026-02-02")
    for n in names:
        (wt / n).write_text("c\n")
    git(root, "commit", "-qam", "touch all ten", day="2026-03-03")
    (wt / names[0]).write_text("d\n"); git(root, "commit", "-qam", "repair [sweep]", day="2026-04-04")
    sub = root / "parts" / "service"; sub.mkdir(parents=True); git(sub, "init", "-q"); (sub / "f").write_text("x")
    git(sub, "add", "-A"); git(sub, "commit", "-qm", "fix(BUG-7): named here, and feat/123-slug too, and fix/bug-1204-four-digits", day="2026-01-01")
    (root / "gone").mkdir()
    (root / ".gitmodules").write_text('[submodule "a"]\n\tpath = parts/service\n[submodule "b"]\n\tpath = gone\n')
    check("last worked on is the last commit ABOUT the tracker — a `[sweep]` commit and one touching more than eight trackers say nothing",
          fm.last_worked_on(wt / names[0]) == "2026-02-02")
    check("a tracker only ever swept falls back to its oldest commit; one git never saw has no date",
          fm.last_worked_on(wt / names[1]) == "2026-01-01" and fm.last_worked_on(wt / "BUG-999-none.md") == "—")
    check("repos naming a tracker come from the submodules' subjects and branches; one not checked out is skipped",
          fm.repos_naming() == {"BUG-007": ["service"], "FEAT-123": ["service"], "BUG-1204": ["service"]})

# --- a vendored copy is pinned -----------------------------------------------------------------------------
with tempfile.TemporaryDirectory() as d:
    root = Path(d).resolve()
    dest = root / "tools" / "shoalmark"
    out = io.StringIO()
    with redirect_stdout(out):
        fm.vendor(dest, allow_untagged=True)                 # the suite's own tree is a working copy, not a release (0.17.8)
    pin = (dest / "PIN").read_text()
    check("a vendored copy carries its licence: both texts, the notice, and the SPDX line in the tool",
          all((dest / f).exists() and f in pin for f in ("LICENSE-APACHE", "LICENSE-MIT", "NOTICE"))
          and "Apache License" in (dest / "LICENSE-APACHE").read_text() and "Apache-2.0 OR MIT" in (dest / "shoalmark.py").read_text().split("\n")[1]
          and fm.digest(dest / "LICENSE-APACHE").startswith("cfc7749b96f63bd3"))
    check("--vendor copies the tool and its one vendored renderer, and pins each by sha256",
          (dest / "shoalmark.py").exists() and (dest / "vendor/marked-18.0.13.umd.js").exists()
          and fm.digest(dest / "shoalmark.py") in pin)
    tracker(root, "FEAT-001", status="Proposed")
    tool = [sys.executable, str(dest / "shoalmark.py"), "--root", str(root)]
    ok = subprocess.run(tool, capture_output=True, text=True, encoding="utf-8", errors="replace", env=_ENV)
    (dest / "shoalmark.py").write_text((dest / "shoalmark.py").read_text() + "\n# edited in place\n")
    bad = subprocess.run(tool, capture_output=True, text=True, encoding="utf-8", errors="replace", env=_ENV)
    (dest / "shoalmark.py").write_text((dest / "shoalmark.py").read_text().replace("\n# edited in place\n", ""))
    (dest / "PIN").rename(dest / "PIN.gone")
    nopin = subprocess.run(tool, capture_output=True, text=True, encoding="utf-8", errors="replace", env=_ENV)
    (dest / "PIN.gone").rename(dest / "PIN")
    check("a vendored copy whose PIN was deleted is refused — the integrity check cannot be switched off silently, and the message names a path a reader can use",
          nopin.returncode == fm.EXIT_LINT and "tools/shoalmark/PIN is missing" in nopin.stderr and str(root) not in nopin.stderr)
    check("a vendored copy runs from where it sits — and one edited in place is refused by its own gate",
          ok.returncode == 0 and bad.returncode == fm.EXIT_LINT and "differs from its PIN" in bad.stderr)

# --- 0.3.0: what a second repository taught ---------------------------------------------------------------
check("the configuration is read without a library — the subset --init writes, a refusal by line for anything else",
      fm.read_config('name = "a # b"  # c\nn = 7\nflag = true\n[kinds]\nMSR = "Work" # x\n') == {"name": "a # b", "n": 7, "flag": True, "kinds": {"MSR": "Work"}}
      and (lambda: [True for _ in [0] if not _try(lambda: fm.read_config('x = [1, 2]\n'))])()
      and fm.read_config('who = ["holgo", "a b"]\nnone = []\n') == {"who": ["holgo", "a b"], "none": []})
with tempfile.TemporaryDirectory() as d:
    root = Path(d).resolve()
    git(root, "init", "-q")
    (root / "AGENTS.md").write_text("# mine\n\nkeep this.\n")
    run(root, "--init", "--key", "msr")
    a1 = (root / "AGENTS.md").read_text()
    (root / "AGENTS.md").write_text(a1.replace("Look before you file", "LOOK"))
    run(root, "--init")
    a2 = (root / "AGENTS.md").read_text()
    check("--init writes the agent contract between its own markers — the repository's text is kept, the section is refreshed, a CLAUDE.md router appears once",
          a1.startswith("# mine\n\nkeep this.\n") and "Look before you file" in a2 and "LOOK" not in a2 and a2.count(fm.CONTRACT_BEGIN) == 1
          and "MSR-012" in a2 and "feat/msr-012-slug" in a2 and "AGENTS.md" in (root / "CLAUDE.md").read_text())
    home = root / "docs/work-tracker/TRIAGE.md"
    code, out, _ = run(root, "--next")
    check("--next says so when no path is written and nothing is ranked", code == 0 and "none is written" in out and "Nothing is ranked" in out)
    home.write_text(home.read_text().replace("1.\n", "1. [MSR-002](MSR-002-x.md) first.\n"))
    fm.configure(root)
    tracker(root, "MSR-001", extra='rank: 1\ntier: P1\nnext: owner\nask: "Shall the launcher ship before the importer?"\n'
            'ask-kind: ruling\nask-since: 2026-09-20\nask-proposal: "the launcher first"\n'); tracker(root, "MSR-002", extra="rank: 2\ntier: P1\nnext: build\n")
    code, out, _ = run(root, "--next")
    check("--next lists the ranked work in order with each move and what is true now, and starts a seat on the first move that is its own",
          code == 0 and out.index("#1 MSR-001") < out.index("#2 MSR-002") and "One thing is left." in out and "START WITH: MSR-002" in out and "MSR-002 first" in out and "](" not in out)
    code, out, _ = run(root, "--install-hook")
    hook = root / ".git/hooks/pre-commit"
    check("--install-hook writes plain, executable git hooks that stage exactly what the command wrote",
          code == 0 and hook.exists() and os.access(hook, os.X_OK) and "--print-written" in hook.read_text() and (root / ".git/hooks/post-merge").exists())
    git(root, "add", "-A"); git2 = subprocess.run(["git", "-C", str(root), "-c", "commit.gpgsign=false", "commit", "-qm", "x"], capture_output=True, text=True, encoding="utf-8", errors="replace", env=_ENV)
    said = "" if git2.returncode == 0 else " — git said: " + repr((git2.stderr + git2.stdout)[-400:])
    check("the installed hook runs on a real commit and stages the regenerated INDEX" + said, git2.returncode == 0
          and "INDEX.md" in subprocess.run(["git", "-C", str(root), "show", "--name-only", "--format=", "HEAD"], capture_output=True, text=True, encoding="utf-8", errors="replace", env=_ENV).stdout)
    hook.write_text("#!/bin/sh\n# somebody else's hook\n")
    code, _, err = run(root, "--install-hook")
    check("a hook that is not shoalmark's is never overwritten — it is named, with the line to add", code == fm.EXIT_LINT and "left alone" in err and "somebody else" in hook.read_text())
fm.configure(HERE)


# the browser that renders the board, where one is installed — read here, before the first check that renders one
_CHROME_FLAGS = ["--no-sandbox"] if sys.platform.startswith("linux") else []     # a CI container has no user namespace for the sandbox
_CHROME = next((c for c in ("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", r"C:\Program Files\Google\Chrome\Application\chrome.exe", r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe", "/usr/bin/chromium", "/usr/bin/chromium-browser", "/usr/bin/google-chrome") if os.path.exists(c)), None)


def run_safe(root, *argv, git_env=None):
    """`run`, but a flag this copy of the tool does not know is a failed check, not a stopped suite — what a check that
    must fail on an older tool needs."""
    try:
        return run(root, *argv, git_env=git_env)
    except SystemExit as e:
        return (e.code if isinstance(e.code, int) else 2), "", ""


# --- FM-024 S1+S2: a seat's commit names its session — the trailer the hook appends, and an id when a harness has none --
with tempfile.TemporaryDirectory() as d:
    root = Path(d).resolve()
    git(root, "init", "-q"); _, init_out, _ = run(root, "--init", "--key", "msr"); code, _, _ = run(root, "--install-hook")
    pcm = root / ".git/hooks/prepare-commit-msg"
    commit_ = lambda msg: subprocess.run(["git", "-C", str(root), "-c", "commit.gpgsign=false", "commit", "-q", "--allow-empty", "-m", msg], capture_output=True, text=True, encoding="utf-8", errors="replace", env=_ENV)
    body = lambda: subprocess.run(["git", "-C", str(root), "log", "-1", "--format=%B"], capture_output=True, text=True, encoding="utf-8", errors="replace", env=_ENV).stdout
    c0 = commit_("a person's commit"); plain = body()
    subprocess.run(["git", "-C", str(root), "config", "seat.session", "a9"], env=_ENV, check=True)
    c1 = commit_("a seat's commit"); stamped = body()
    c2 = commit_("typed by hand\n\nSession: k3"); typed = body()
    check(f"FM-024 S2 · --install-hook writes a prepare-commit-msg hook: a commit where seat.session is set carries `Session: <id>`, one where it is not carries none, one that has one keeps it (saw {stamped!r})",
          code == 0 and pcm.exists() and os.access(pcm, os.X_OK) and '--session-trailer "$1"' in pcm.read_text()
          and all(c.returncode == 0 for c in (c0, c1, c2)) and "Session:" not in plain and "\nSession: a9\n" in stamped and typed.count("Session:") == 1 and "Session: k3" in typed)
    check(f"FM-032 S2 · the hook writes `Worktree: <the checkout's directory>` beside `Session:` — never where there is no session, and beside one typed by hand (saw {stamped!r} {typed!r})",
          stamped.rstrip().endswith(f"Session: a9\nWorktree: {root.name}") and typed.rstrip().endswith(f"Session: k3\nWorktree: {root.name}")
          and "Worktree:" not in plain and typed.count("Worktree:") == 1)
    # 0.17.7: the trailers are read in Python from git's plain trailer block — the same values, and no filter shape in the source
    subprocess.run(["git", "-C", str(root), "-c", "commit.gpgsign=false", "-c", "core.hooksPath=/dev/null", "commit", "-q", "--allow-empty", "-m",
                    "a planted commit\n\nits body, line one\nNote: this line sits in the body, not in the trailer block\nline three\n\n"
                    "Session: a9\nReviewed: 0123abcd\nsession: b7\nCo-Authored-By: someone <someone@example.org>"], env=_ENV, check=True)
    planted = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"], capture_output=True, text=True, env=_ENV).stdout.strip()
    fm.configure(root)
    got_ = {k: fm.trailers_of(planted, k) for k in ("Session", "Reviewed", "Note", "Co-Authored-By")}
    check(f"0.17.7 · trailers_of() reads a planted commit with two keys and a body of several lines as before: every value of the key, in order, the key's case aside, nothing from the body (saw {got_})",
          got_ == {"Session": ["a9", "b7"], "Reviewed": ["0123abcd"], "Note": [], "Co-Authored-By": ["someone <someone@example.org>"]})
    _forms = set(re.findall(r"%\(trailers:([^)]*)\)", (HERE / "shoalmark.py").read_text(encoding="utf-8")))
    check(f"0.17.7 · the tool asks git for the plain trailer block alone and picks the key in Python — no filter in the format, the shape a consumer's secret gate reads as a credential (saw {sorted(_forms)})",
          _forms == {"only,separator=%x03"})
    git(root, "commit", "-q", "--allow-empty", "-m", "a session that ran before\n\nSession: a9a9a9a9")
    import secrets
    _hex, _seq = secrets.token_hex, iter(["a9a9a9a9", "0b0b0b0b"])
    secrets.token_hex = lambda n=4: next(_seq)
    try:
        code, out, _ = run_safe(root, "--session", "new")
    finally:
        secrets.token_hex = _hex
    fresh = run_safe(root, "--session", "new")[1].strip()
    check(f"FM-024 S1 · `--session new` prints an id no commit's `Session:` carries — eight hex characters, for a harness with none of its own; `--init` names `seat.session` beside `user.email` (saw {out.strip()!r}, {fresh!r})",
          code == 0 and out.strip() == "0b0b0b0b" and re.fullmatch(r"[0-9a-f]{8}", fresh) is not None and "seat.session" in init_out and "user.email" in init_out)

# --- FM-032 S2: the registry is a report — generated from the `Session:` and `Worktree:` trailers, kept in no file ------
AS = lambda who: {"GIT_AUTHOR_NAME": who, "GIT_AUTHOR_EMAIL": who, "GIT_COMMITTER_NAME": who, "GIT_COMMITTER_EMAIL": who}
SEATS_TOML = '\n[seats]\nowner = "owner@example.org"\nprincipal = "principal@seat"\nimplementer = "implementer@seat"\nreviewer = "reviewer@seat"\n'


def commit_as(root, who, msg, when=None):
    """A commit past every hook, by `who`, at `when` (an ISO time) — what a seat's commit looks like once made."""
    env = dict(_ENV, **AS(who), **({"GIT_AUTHOR_DATE": when, "GIT_COMMITTER_DATE": when} if when else {}))
    subprocess.run(["git", "-C", str(root), "-c", "commit.gpgsign=false", "-c", "core.hooksPath=/dev/null", "commit", "-q", "--allow-empty", "-m", msg], env=env, check=True)
    return subprocess.run(["git", "-C", str(root), "rev-parse", "--short", "HEAD"], capture_output=True, text=True, env=_ENV).stdout.strip()


with tempfile.TemporaryDirectory() as d:
    root = Path(d).resolve()
    git(root, "init", "-q"); run(root, "--init", "--key", "msr")
    (root / "shoalmark.toml").write_text((root / "shoalmark.toml").read_text() + SEATS_TOML)
    tracker(root, "MSR-001"); run(root); git(root, "add", "-A")
    commit_as(root, "owner@example.org", "the Owner's commit carries no session", "2026-09-19T09:00:00")
    p1 = commit_as(root, "principal@seat", "the Principal begins\n\nSession: 1111aaaa\nWorktree: wt-p", "2026-09-20T09:00:00")
    i1 = commit_as(root, "implementer@seat", "built before 0.18.0: no Worktree:\n\nSession: 1111aaaa/implementer-1", "2026-09-20T10:00:00")
    x1 = commit_as(root, "someone@example.org", "an author outside [seats]\n\nSession: 2222bbbb\nWorktree: wt-x", "2026-09-20T11:00:00")
    r1 = commit_as(root, "reviewer@seat", "a verdict\n\nSession: 3333cccc/reviewer-1\nWorktree: wt-r1", "2026-09-21T09:00:00")
    i2 = commit_as(root, "implementer@seat", "the fixes\n\nSession: 1111aaaa/implementer-1\nWorktree: wt-i", "2026-09-21T10:00:00")
    r2_ = commit_as(root, "reviewer@seat", "the same id, guessed elsewhere\n\nSession: 3333cccc/reviewer-1\nWorktree: wt-r2", "2026-09-21T11:00:00")
    p2 = commit_as(root, "principal@seat", "the Principal again, a day on\n\nSession: 1111aaaa\nWorktree: wt-p", "2026-09-22T09:00:00")
    code, said, _ = run_safe(root, "--sessions")
    table = [[c.strip() for c in l.strip().strip("|").split("|")] for l in said.splitlines() if l.startswith("| ") and not l.startswith("| Session ")]
    at = lambda iso, sha: f"{datetime.datetime.fromisoformat(iso).strftime('%Y-%m-%d %H:%M')} · {sha}"
    want = [["1111aaaa", "principal", at("2026-09-20T09:00:00", p1), at("2026-09-22T09:00:00", p2), "2", "wt-p"],
            ["1111aaaa/implementer-1", "implementer", at("2026-09-20T10:00:00", i1), at("2026-09-21T10:00:00", i2), "2", "wt-i"],
            ["2222bbbb", "someone@example.org", at("2026-09-20T11:00:00", x1), at("2026-09-20T11:00:00", x1), "1", "wt-x"],
            ["3333cccc/reviewer-1", "reviewer", at("2026-09-21T09:00:00", r1), at("2026-09-21T11:00:00", r2_), "2", "wt-r1, wt-r2"]]
    check(f"FM-032 S2 · `--sessions` prints the registry from the trailers — one row per id, oldest first commit first: its seat through [seats] (an author outside them as they are), first and last commit, how many, its worktrees (saw {table})",
          code == 0 and table == want and "| Session | Seat | First commit | Last commit | Commits | Worktree |" in said and "owner" not in said.split("|---")[-1])
    commit_as(root, "principal@seat", "a session from before the trailer had a worktree\n\nSession: 4444dddd", "2026-09-22T10:00:00")
    code2, said2, _ = run_safe(root, "--sessions")
    row4 = next((l for l in said2.splitlines() if l.startswith("| 4444dddd ")), "")
    check(f"FM-032 S2 · an id whose commits carry no `Worktree:` reads `—`; one id in two worktrees is named under the table; nothing is written (saw {row4!r})",
          code2 == 0 and row4.rstrip().endswith("| 1 | — |") and "- one id, 2 worktrees: 3333cccc/reviewer-1 (wt-r1, wt-r2)" in said2
          and not (root / "docs/work-tracker/sessions.md").exists()
          and subprocess.run(["git", "-C", str(root), "status", "--porcelain"], capture_output=True, text=True, env=_ENV).stdout.strip() == "")
    quiet = run_safe(root, "--owner")[1]
    now_ = commit_as(root, "implementer@seat", "at work now\n\nSession: 5555eeee/implementer-2\nWorktree: wt-now")
    busy = run_safe(root, "--owner")[1]
    check(f"FM-032 S2 · the digest names the sessions with a commit in the last day, by seat — none of the older ones (saw {quiet.strip()[-60:]!r} · {busy.strip()[-80:]!r})",
          "SESSIONS" not in quiet and "SESSIONS IN THE LAST DAY · implementer 1 (5555eeee/implementer-2 in wt-now)" in busy and "1111aaaa" not in busy)
    opened, closed = run_safe(root, "--session", "open", "6666ffff", "principal", "the Owner", "x"), run_safe(root, "--session", "close", "1111aaaa")
    gone = "--session open/close are gone since 0.18.0: the registry is a report — run --sessions"
    check(f"FM-032 S2 · `--session open` and `--session close` are gone: one line, exit 2, nothing written (saw {opened[0]}, {closed[0]}, {opened[2].strip()!r})",
          opened[0] == 2 and closed[0] == 2 and opened[2].strip() == gone and closed[2].strip() == gone
          and not (root / "docs/work-tracker/sessions.md").exists())
    (root / "docs/work-tracker/sessions.md").write_text("| Session | Seat | Convened by | Scope | Worktree | Started | Ended |\n|---|---|---|---|---|---|---|\n"
                                                         "| 1111aaaa | principal | the Owner | the tool | wt-p | 2026-09-20 09:00 | — |\n")
    git(root, "add", "-A"); commit_as(root, "owner@example.org", "a consumer's registry, left from 0.17")
    kept = (root / "docs/work-tracker/sessions.md").read_text()
    left = run_safe(root, "--check")
    run_safe(root); run_safe(root, "--session", "new"); run_safe(root, "--sessions")
    check(f"FM-032 S2 · a `sessions.md` left in the tree is not read: `--check` passes with one warning line, and no command writes it (saw {left[0]}, {left[1].strip()[-120:]!r})",
          left[0] == 0 and left[1].count("sessions.md") == 1
          and "warning: docs/work-tracker/sessions.md is a report since 0.18.0 — delete it; --sessions prints it" in left[1]
          and (root / "docs/work-tracker/sessions.md").read_text() == kept)

# --- FM-032 S2: the gate keeps one rule — a seat's commit carries a `Session:` of its own seat ------------------------
with tempfile.TemporaryDirectory() as d:
    root = Path(d).resolve()
    git(root, "init", "-q"); run(root, "--init", "--key", "msr")
    (root / "shoalmark.toml").write_text((root / "shoalmark.toml").read_text() + SEATS_TOML)
    tracker(root, "MSR-001"); run(root); git(root, "add", "-A")
    base = commit_as(root, "someone@example.org", "the start: no session anywhere yet")
    session = lambda sid: subprocess.run(["git", "-C", str(root), "config", *(["seat.session", sid] if sid else ["--unset", "seat.session"])], env=_ENV)
    session(""); before = run_safe(root, "--session-check", git_env=AS("principal@seat"))
    adopted = commit_as(root, "principal@seat", "the first session\n\nSession: 1111aaaa\nWorktree: wt-p")
    seen = {}
    for name, sid, who in (("no trailer", "", "principal@seat"), ("wrong seat", "1111aaaa/reviewer-1", "principal@seat"), ("bad shape", "a9", "principal@seat"),
                           ("upper hex", "1111AAAA", "principal@seat"), ("own id", "1111aaaa", "principal@seat"), ("own hand", "1111aaaa/principal-2", "principal@seat"),
                           ("sub-agent", "1111aaaa/reviewer-1", "reviewer@seat"), ("the Owner", "", "owner@example.org"), ("outside", "", "someone@example.org")):
        session(sid); seen[name] = run_safe(root, "--session-check", git_env=AS(who))
    session("")
    say = {k: v[2] for k, v in seen.items()}
    check(f"FM-032 S2 · the gate refuses a seat's commit with no Session:, with one of another shape than `<8 hex>[/<seat>-<n>]`, or whose seat part is another seat (saw exits { {k: v[0] for k, v in seen.items()} })",
          all(seen[k][0] == fm.EXIT_LINT for k in ("no trailer", "wrong seat", "bad shape", "upper hex"))
          and "this commit by principal@seat carries no Session: trailer — set `git config --worktree seat.session <id>`" in say["no trailer"]
          and "is the seat principal, and its Session: 1111aaaa/reviewer-1 names the seat reviewer" in say["wrong seat"]
          and "carries `Session: a9` — a session id is eight hex characters, or `<id>/<seat>-<n>` for a sub-agent" in say["bad shape"])
    check(f"FM-032 S2 · …and passes a session of the author's own seat — an id used before, no row to open — the Owner's commit and an author outside [seats] with none, and a seat's commit in a history that no `Session:` has reached yet (saw {before[0]}, {say['own id']!r})",
          all(seen[k][0] == 0 for k in ("own id", "own hand", "sub-agent", "the Owner", "outside")) and before[0] == 0
          and not any("open row" in v or "one worktree per session" in v for v in say.values()))
    made = commit_as(root, "principal@seat", "made past the hook\n\nSession: 1111aaaa/reviewer-1")
    at_head = run_safe(root, "--check")
    check(f"FM-032 S2 · on a clean tree the commit at HEAD is judged by its own trailer (saw {at_head[2].strip()[:160]!r})",
          at_head[0] == fm.EXIT_LINT and f"commit {made}" in at_head[2] and "names the seat reviewer" in at_head[2])
    git(root, "reset", "-q", "--hard", adopted)
    trunk = subprocess.run(["git", "-C", str(root), "branch", "--show-current"], capture_output=True, text=True, env=_ENV).stdout.strip()
    git(root, "checkout", "-q", "-b", "old", base); commit_as(root, "principal@seat", "a seat's commit from before the first session")
    git(root, "checkout", "-q", "-b", "new", adopted); commit_as(root, "principal@seat", "a seat's commit after it, past the hook")
    git(root, "checkout", "-q", trunk)
    merged = lambda branch: (subprocess.run(["git", "-C", str(root), "-c", "commit.gpgsign=false", "-c", "core.hooksPath=/dev/null", "merge", "-q", "--no-ff", "-m", f"the Owner merges {branch}", branch],
                                            env=dict(_ENV, **AS("owner@example.org")), check=True), run_safe(root, "--check"))[1]
    old_, new_ = merged("old"), merged("new")
    check(f"FM-032 S2 · a merge's commits are each judged by their own trailer — one from before the history's first `Session:` is not, one after it is (saw {old_[0]}, {new_[0]})",
          old_[0] == 0 and new_[0] == fm.EXIT_LINT and "which the merge brings" in new_[2] and "carries no Session: trailer" in new_[2] and "the merge brings" not in old_[2])

# --- R4: the pre-commit hook judges the session on EVERY commit — a seat's code-only commit included -----------------
with tempfile.TemporaryDirectory() as d:
    root = Path(d).resolve()
    git(root, "init", "-q"); run(root, "--init", "--key", "msr")
    (root / "shoalmark.toml").write_text((root / "shoalmark.toml").read_text() + '\n[seats]\nowner = "owner@example.org"\nimplementer = "implementer@seat"\n')
    tracker(root, "MSR-001")
    run(root); git(root, "add", "-A"); git(root, "commit", "-qm", "the first session's commit\n\nSession: 0a0a0a0a"); run(root, "--install-hook")
    code_only = lambda msg: (subprocess.run(["git", "-C", str(root), "add", "app.py"], env=_ENV),
                             subprocess.run(["git", "-C", str(root), "-c", "commit.gpgsign=false", "commit", "-qm", msg], capture_output=True, text=True, encoding="utf-8", errors="replace", env=dict(_ENV, **AS("implementer@seat"))))[1]
    (root / "app.py").write_text("print('one')\n"); refused_ = code_only("code only, no session")
    subprocess.run(["git", "-C", str(root), "config", "seat.session", "0a0a0a0a/implementer-1"], env=_ENV, check=True)
    passed_ = code_only("code only, with its session")
    trailer_ = fm.trailer_values(subprocess.run(["git", "-C", str(root), "log", "-1", f"--format={fm.TRAILERS}"], capture_output=True, text=True, env=_ENV).stdout.strip("\n"), "Session")
    check(f"FM-024 R4 · the installed pre-commit hook refuses a seat's code-only commit with no session — no tracker staged — and lets it through with its session (saw {refused_.returncode}, {passed_.returncode}, {trailer_!r})",
          refused_.returncode != 0 and "carries no Session: trailer" in refused_.stderr + refused_.stdout and passed_.returncode == 0 and trailer_ == ["0a0a0a0a/implementer-1"])

# --- FM-024 S6: each verdict reported as independent or same session — the reviewed range's sessions against its own --
with tempfile.TemporaryDirectory() as d:
    root = Path(d).resolve()
    git(root, "init", "-q"); run(root, "--init", "--key", "msr"); tracker(root, "MSR-001"); run(root)
    git(root, "add", "-A"); git(root, "commit", "-qm", "the trunk")
    git(root, "checkout", "-q", "-b", "feat")
    head = lambda: subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"], capture_output=True, text=True, env=_ENV).stdout.strip()
    git(root, "commit", "-q", "--allow-empty", "-m", "the build\n\nSession: a9"); git(root, "commit", "-q", "--allow-empty", "-m", "more of it\n\nSession: a9/implementer-1"); built = head()
    git(root, "commit", "-q", "--allow-empty", "-m", f"review: READY\n\nReviewed: {built}\nSession: a9/reviewer-1"); v_same = head()
    git(root, "commit", "-q", "--allow-empty", "-m", f"review: READY\n\nReviewed: {built}\nSession: k3"); v_ind = head()
    git(root, "commit", "-q", "--allow-empty", "-m", f"review: READY\n\nReviewed: {built}"); v_none = head()
    git(root, "commit", "-q", "--allow-empty", "-m", f"review of the reviews\n\nReviewed: {v_none}\nSession: k3"); v_late = head()
    said = run_safe(root, "--check")[1]
    word = lambda v: (re.search(rf"verdict {v[:10]} on \w+: ([a-z ]+) —", said) or [None, "?"])[1]
    check(f"FM-024 S6 · each verdict is reported: a sub-agent of the author's session is *same session*, another root *independent*, no session *untraced* — and a verdict inside a range is not its author (saw {[word(v) for v in (v_same, v_ind, v_none, v_late)]})",
          [word(v) for v in (v_same, v_ind, v_none, v_late)] == ["same session", "independent", "untraced", "independent"]
          and "reviews this week · 4 verdict(s) · independent 2 · same session 1 · untraced 1" in said and run_safe(root, "--check")[0] == 0)

# --- R2: the reviewed range is the branch's own commits — never the trunk it merged in; a tip on the trunk is no branch verdict
    with tempfile.TemporaryDirectory() as d2:
        r2 = Path(d2).resolve()
        git(r2, "init", "-q"); run(r2, "--init", "--key", "msr"); tracker(r2, "MSR-001"); run(r2)
        git(r2, "add", "-A"); git(r2, "commit", "-qm", "the trunk")
        sha = lambda ref="HEAD": subprocess.run(["git", "-C", str(r2), "rev-parse", ref], capture_output=True, text=True, env=_ENV).stdout.strip()
        trunk_name, t0 = subprocess.run(["git", "-C", str(r2), "branch", "--show-current"], capture_output=True, text=True, env=_ENV).stdout.strip(), sha()
        git(r2, "checkout", "-q", "-b", "n"); git(r2, "commit", "-q", "--allow-empty", "-m", "release N's docket\n\nSession: P")
        git(r2, "checkout", "-q", trunk_name); git(r2, "merge", "-q", "--no-ff", "-m", "the Owner merges N", "n")
        git(r2, "checkout", "-q", "-b", "n1", t0); git(r2, "commit", "-q", "--allow-empty", "-m", "N+1 built\n\nSession: I")
        git(r2, "merge", "-q", "--no-ff", "-m", f"the trunk merged in\n\nSession: I", trunk_name); tip = sha()
        git(r2, "commit", "-q", "--allow-empty", "-m", f"review\n\nReviewed: {tip}\nSession: P/reviewer-1"); v_sib = sha()
        git(r2, "commit", "-q", "--allow-empty", "-m", f"review\n\nReviewed: {tip}\nSession: I/reviewer-1"); v_own = sha()
        words = lambda said, vs: [(re.search(rf"verdict {v[:10]} on \w+: ([a-z ]+?) —", said) or [None, "?"])[1] for v in vs]
        on_branch = words(run_safe(r2, "--check")[1], (v_sib, v_own))
        git(r2, "checkout", "-q", trunk_name); git(r2, "merge", "-q", "--no-ff", "-m", "the Owner merges N+1", "n1")
        landed = words(run_safe(r2, "--check")[1], (v_sib, v_own))
        git(r2, "commit", "-q", "--allow-empty", "-m", "work on the trunk itself\n\nSession: K"); w = sha()
        git(r2, "commit", "-q", "--allow-empty", "-m", f"review\n\nReviewed: {w}\nSession: J"); v_trunk = sha()
        on_trunk = run_safe(r2, "--check")[1]
        check(f"FM-024 R2 · a sibling whose session authored only a commit the branch merged in from the trunk is independent of the branch — before and after the branch lands; the branch's own session is not; a tip on the trunk is no branch verdict (saw {on_branch}, {landed})",
              on_branch == ["independent", "same session"] and landed == ["independent", "same session"]
              and f"verdict {v_trunk[:10]} on {w[:10]}: on trunk — not a branch verdict" in on_trunk and "on trunk 1" in on_trunk)

    # --- FM-024 S7, FM-032 S2: the board's strip and the digest's line — who committed in the last day; how independent the week was
    digest_ = run_safe(root, "--owner")[1]
    strip_ = ""
    if _CHROME:
        run_safe(root, "--html-only")
        pdom = subprocess.run([_CHROME, "--headless=new", "--disable-gpu", *_CHROME_FLAGS, "--virtual-time-budget=4000", "--dump-dom", (root / "docs/work-tracker/index.html").as_uri()],
                              capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60).stdout
        strip_ = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", (re.search(r'<p id="p"[^>]*>([\s\S]*?)</p>', pdom) or [None, ""])[1]))
    check(f"FM-024 S7 · the board's strip names the sessions with a commit in the last day, with seat and worktree, and counts the week's verdicts; the digest's line groups them by seat (saw {strip_[-200:]!r} · {digest_.strip()[-80:]!r})",
          "SESSIONS IN THE LAST DAY · t@t 4 (a9, a9/implementer-1, a9/reviewer-1, k3)" in digest_ and (not _CHROME or (
              "sessions · 4 in the last day — a9 t@t (—) · a9/implementer-1 t@t (—) · a9/reviewer-1 t@t (—) · k3 t@t (—)" in strip_
              and "reviews this week · independent 2 · same session 1 · untraced 1" in strip_)))
fm.configure(HERE)
with tempfile.TemporaryDirectory() as d:
    dest = Path(d).resolve() / "tools" / "shoalmark"
    with redirect_stdout(io.StringIO()):
        fm.vendor(dest, allow_untagged=True)
    # FM-009: `--vendor` compares the consumer's VERSION file against our version. While the version was ALSO declared
    # as a constant beside that file the two could drift — and did, for two releases — so a consumer pinned at the
    # stale constant read as up to date and the changelog it was owed was suppressed.
    check("what `--vendor` copies is what it reports — the version that lands in the copy is the version named",
          (dest / "VERSION").read_text().strip() == fm.__version__)
    (dest / "VERSION").write_text("0.2.0\n")
    (dest / "PIN").write_text("\n".join(f"{fm.digest(dest / l.partition('  ')[2])}  {l.partition('  ')[2]}" for l in (dest / "PIN").read_text().splitlines() if not l.startswith("#")) + "\n")
    out = io.StringIO()
    with redirect_stdout(out):
        fm.vendor(dest, allow_untagged=True)
    check("vendoring again says which version it replaces and what changed since", "(was 0.2.0)" in out.getvalue() and "## 0.3.0" in out.getvalue() and "## 0.2.0" not in out.getvalue())
    _heads = re.findall(r"^## (\d+\.\d+\.\d+)", (HERE / "CHANGELOG.md").read_text(), re.M)
    check(f"a consumer one release behind ({_heads[1]}) is shown exactly the section it lacks — the newest, which is this version's",
          _heads[0] == fm.__version__ and fm.changes_since(_heads[1]).startswith(f"## {fm.__version__} — ") and fm.changes_since(_heads[1]).count("\n## ") == 0)
    (dest / "shoalmark.py").write_text("# edited\n")
    err = io.StringIO()
    with redirect_stderr(err):
        code = fm.vendor(dest)
    check("vendoring never overwrites a copy that was edited in place", code == fm.EXIT_LINT and "edited in place" in err.getvalue() and (dest / "shoalmark.py").read_text() == "# edited\n")

# --- FM-011, 0.17.8: a vendoring vouches for what it copies — the whole tool, from a release — and the PIN says where from --
import shutil
with tempfile.TemporaryDirectory() as d:
    base = Path(d).resolve(); src = base / "source"; src.mkdir()
    for rel in fm.TOOL_FILES:
        (src / rel).parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(HERE / rel, src / rel)
    ver = (src / "VERSION").read_text().strip()
    g = lambda *a: subprocess.run(["git", "-C", str(src), "-c", "commit.gpgsign=false", "-c", "core.hooksPath=/dev/null", *a], capture_output=True, text=True, encoding="utf-8", errors="replace", env=_ENV)
    g("init", "-q"); g("add", "-A"); g("commit", "-qm", "the release"); g("tag", f"v{ver}"); tagged = g("rev-parse", "HEAD").stdout.strip()
    vend = lambda dest, *flags: subprocess.run([sys.executable, str(src / "shoalmark.py"), "--vendor", str(dest), *flags], cwd=str(base), capture_output=True, text=True, encoding="utf-8", errors="replace", env=_ENV)
    cons = base / "consumer"; cons.mkdir()
    ok_ = vend(cons / "tools/shoalmark"); pin_ = (cons / "tools/shoalmark/PIN").read_text() if (cons / "tools/shoalmark/PIN").exists() else ""
    tool_ = [sys.executable, str(cons / "tools/shoalmark/shoalmark.py"), "--root", str(cons)]
    subprocess.run(tool_ + ["--init", "--key", "msr"], capture_output=True, env=_ENV); subprocess.run(tool_, capture_output=True, env=_ENV)
    said_ = subprocess.run(tool_ + ["--check"], capture_output=True, text=True, encoding="utf-8", errors="replace", env=_ENV)
    check(f"FM-011 · from a clean clone at its release tag the copy is pinned with its manifest — version, tag, commit, date, complete — and the consumer's --check says where it came from (saw {pin_.splitlines()[:1]}, {said_.stdout.strip().splitlines()[-1:]})",
          ok_.returncode == 0 and f"from tag v{ver}" in ok_.stdout
          and pin_.startswith(f"# shoalmark {ver} · tag v{ver} · commit {tagged} · vendored {datetime.date.today().isoformat()} · complete\n")
          and len([l for l in pin_.splitlines() if not l.startswith("#")]) == len(fm.TOOL_FILES)
          and said_.returncode == 0 and f"pinned {ver} from tag v{ver} (commit {tagged[:10]})" in said_.stdout and "warning" not in said_.stdout)
    (src / "NOTICE").unlink(); gone_ = vend(base / "c2/tools/shoalmark")
    g("checkout", "-q", "--", "NOTICE"); (src / "README.md").write_text((src / "README.md").read_text() + "\na local change\n"); dirty_ = vend(base / "c3/tools/shoalmark")
    check(f"FM-011 · a source missing a file of the tool is refused, naming it; a source with a change is refused, naming the path — exit 4, nothing written (saw {gone_.stderr.strip()[:90]!r} · {dirty_.stderr.strip()[:90]!r})",
          gone_.returncode == fm.EXIT_LINT and "missing NOTICE" in gone_.stderr and not (base / "c2").exists()
          and dirty_.returncode == fm.EXIT_LINT and "the tree has changes: README.md" in dirty_.stderr and not (base / "c3").exists())
    g("commit", "-qam", "past the tag"); moved = g("rev-parse", "HEAD").stdout.strip()
    refused_ = vend(base / "c4/tools/shoalmark"); allowed_ = vend(cons / "tools/shoalmark", "--allow-untagged")
    upin_ = (cons / "tools/shoalmark/PIN").read_text(); subprocess.run(tool_, capture_output=True, env=_ENV)
    uwarn_ = subprocess.run(tool_ + ["--check"], capture_output=True, text=True, encoding="utf-8", errors="replace", env=_ENV)
    (src / "NOTICE").unlink(); part_ = vend(base / "c5/tools/shoalmark", "--partial", "--allow-untagged")
    ppin_ = (base / "c5/tools/shoalmark/PIN").read_text() if (base / "c5/tools/shoalmark/PIN").exists() else ""
    check(f"FM-011 · HEAD past the tag is refused, naming it; --allow-untagged vendors and the PIN says `untagged <sha>`, which the consumer's --check warns of; --partial names what is missing (saw {upin_.splitlines()[:1]}, {ppin_.splitlines()[:2]})",
          refused_.returncode == fm.EXIT_LINT and f"HEAD {moved[:10]} is not at the tag v{ver} (it carries" not in refused_.stderr and f"HEAD {moved[:10]} is not at the tag v{ver}" in refused_.stderr
          and allowed_.returncode == 0 and upin_.startswith(f"# shoalmark {ver} · untagged {moved[:10]} · vendored ")
          and uwarn_.returncode == 0 and f"pinned {ver} from untagged {moved[:10]}" in uwarn_.stdout and "warning: this copy was vendored from a working copy, not a release" in uwarn_.stdout
          and part_.returncode == 0 and "· partial" in ppin_.splitlines()[0] and "# missing: NOTICE" in ppin_ and "PARTIAL: missing NOTICE" in part_.stdout)
    # R1: the manifest is checked, not displayed — the form --vendor writes, and agreeing with the pinned VERSION
    body_ = "\n".join(l for l in (cons / "tools/shoalmark/PIN").read_text().splitlines() if not l.startswith("#"))
    good_ = f"# shoalmark {ver} · tag v{ver} · commit {tagged} · vendored 2026-09-23 · complete"
    heads_ = {"good": good_, "dashes": good_.replace(" · ", " - "), "an empty field": good_.replace(f"tag v{ver}", "tag "),
              "no commit": good_.replace(f" · commit {tagged}", ""), "a version over VERSION": good_.replace(ver, "9.9.9"), "a # line first": "# a note\n" + good_}
    read_ = {}
    for name_, head_ in heads_.items():
        (cons / "tools/shoalmark/PIN").write_text(head_ + "\n" + body_ + "\n")
        r_ = subprocess.run(tool_ + ["--check"], capture_output=True, text=True, encoding="utf-8", errors="replace", env=_ENV)
        read_[name_] = (r_.returncode, [l for l in r_.stdout.splitlines() if "manifest" in l or l.startswith("pinned")])
    (cons / "tools/shoalmark/PIN").write_text(body_ + "\n")
    bare_ = subprocess.run(tool_ + ["--check"], capture_output=True, text=True, encoding="utf-8", errors="replace", env=_ENV).stdout
    says_ = lambda k, word: read_[k][0] == 0 and len(read_[k][1]) == 1 and read_[k][1][0].startswith("warning: the PIN's manifest ") and word in read_[k][1][0] and "unverified" in read_[k][1][0]
    check(f"FM-011 R1 · a hand-edited manifest is never believed: separators changed, an empty field, no commit — not the line --vendor writes; a version over VERSION — named; a # line first — not the first line; each unverified, the good one read as before (saw {read_})",
          read_["good"][1] == [f"pinned {ver} from tag v{ver} (commit {tagged[:10]}), vendored 2026-09-23, complete"]
          and all(says_(k, "is not the line --vendor writes") for k in ("dashes", "an empty field", "no commit"))
          and says_("a version over VERSION", f"says 9.9.9, and the pinned VERSION is {ver}") and says_("a # line first", "is not the PIN's first line")
          and "no manifest — pinned before 0.17.8" in bare_)
check("related skips German stop words as it skips English ones", "und" in fm._STOP and "the" in fm._STOP)

# --- the board, seen: rendered in a real browser where one is installed -------------------------------------
if _CHROME:
    with tempfile.TemporaryDirectory() as d:
        root = Path(d).resolve()
        run(root, "--init", "--key", "msr")
        tracker(root, "MSR-001", title="Stock is booked per warehouse"); tracker(root, "MSR-002", status="Shipped", title="A shipped one")
        run(root)
        dom = lambda frag: subprocess.run([_CHROME, "--headless=new", "--disable-gpu", *_CHROME_FLAGS, "--virtual-time-budget=4000", "--dump-dom",
                                           (root / "docs/work-tracker/index.html").as_uri() + frag], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60).stdout
        board_dom, view_dom = dom(""), dom("#=MSR-001")
        shown = re.sub(r"<[^>]+>", " ", board_dom[board_dom.find("<tbody"):board_dom.find("</tbody>")])     # what is rendered, not the data rows in the script
        check("the board renders in a browser: five sections in order, the open tracker under `triage`, the done one folded away",
              re.search(r"progress.*?triage.*?triaged.*?backlog.*?done", shown, re.S) is not None
              and "Stock is booked per warehouse" in shown and "A shipped one" not in shown and "2 trackers" in board_dom)
        check("a tracker opens rendered in the page: its facts, its hand-over, its markdown as HTML",
              "<h2" in view_dom and "What is true now" in view_dom and "One thing is left." in view_dom and "hand-over" in view_dom)
else:
    print("  skip  no browser found — the board was not rendered")

# --- FM-020: a whole id searched is that tracker alone — not every row whose body links to it ----------------------
if _CHROME:
    with tempfile.TemporaryDirectory() as d:
        root = Path(d).resolve()
        run(root, "--init", "--key", "msr")
        tracker(root, "MSR-001", title="Stock is booked per warehouse")
        tracker(root, "MSR-002", title="Stock is counted per shelf", body="## What is true now\n\nIt needs [MSR-001](MSR-001-x.md) first.\n\n## Done when\n\nit is.\n")
        tracker(root, "MSR-003", status="Shipped", title="A shipped one")
        run(root)

        def found(frag):
            """The rows a query typed into the box leaves on the board (the URL hash is typed there), and the counter."""
            d_ = subprocess.run([_CHROME, "--headless=new", "--disable-gpu", *_CHROME_FLAGS, "--virtual-time-budget=4000", "--dump-dom",
                                 (root / "docs/work-tracker/index.html").as_uri() + frag], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60).stdout
            rows = re.findall(r'<tr class="t[^"]*"><td class="m"><i class="q[^"]*"></i><a href="#=(MSR-\d+)">', d_[d_.find("<tbody"):d_.find("</tbody>")])
            return rows, (re.search(r'id="n"[^>]*>([^<]*)<', d_) or [None, ""])[1]
        whole, low, hood, part, word = (found(f) for f in ("#MSR-001", "#msr-001%20", "#~MSR-001", "#MSR-00", "#stock"))
        check(f"FM-020 · a whole id searched shows that tracker alone — not the tracker whose body links to it (saw {whole}, {low[0]})",
              whole[0] == ["MSR-001"] and whole[1].startswith("1 tracker · MSR-001 ·") and low[0] == ["MSR-001"])
        check(f"FM-020 · ~ID still shows the neighbourhood, a partial id and a word still match by substring (saw {hood[0]}, {part[0]}, {word[0]})",
              sorted(hood[0]) == ["MSR-001", "MSR-002"] and sorted(part[0]) == ["MSR-001", "MSR-002", "MSR-003"] and sorted(word[0]) == ["MSR-001", "MSR-002"])
        # a view with open/all (every view but the board), *open* pressed, a closed tracker searched by its id: it is shown,
        # and the counter names it — it never counts it as open (R1)
        probe = '<script>{gi=GROUPS.findIndex(g=>g[0]=="epic");all=false;$("q").value="MSR-003";draw();document.body.dataset.probe=$("n").textContent+"|"+[...document.querySelectorAll("#b tr.t")].map(r=>r.querySelector("a").textContent).join(",")}</script>'
        wt_ = root / "docs/work-tracker"
        (wt_ / "probe.html").write_text((wt_ / "index.html").read_text(encoding="utf-8").replace("</script></html>", "</script>" + probe + "</html>"), encoding="utf-8")
        pdom = subprocess.run([_CHROME, "--headless=new", "--disable-gpu", *_CHROME_FLAGS, "--virtual-time-budget=4000", "--dump-dom", (wt_ / "probe.html").as_uri()],
                              capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60).stdout
        seen = (re.search(r'data-probe="([^"]*)"', pdom) or [None, ""])[1]
        check(f"FM-020 · a shipped tracker searched by its id in the story view with *open* pressed is shown and counted as itself, never as open (saw: {seen!r})",
              seen.startswith("1 tracker · MSR-003 ·") and seen.endswith("|MSR-003") and " open" not in seen)
        # the placeholder fits the box at its CSS minimum (200 px) — measured with the box's own font, not by a window —
        # in both shipped languages, and the whole help is the box's title (R6, R12)
        import html as _html, json as _json
        probe = '<script>{const i=$("q"),c=document.createElement("canvas").getContext("2d");c.font=getComputedStyle(i).font;document.body.dataset.probe=JSON.stringify({min:parseFloat(getComputedStyle(i).minWidth),need:Math.ceil(c.measureText(i.placeholder).width),title:i.title})}</script>'
        fits = {}
        for lang, labels in (("en", None), ("de", HERE / "examples/de/labels.yaml")):
            if labels:
                (wt_ / "brand").mkdir(exist_ok=True); (wt_ / "brand/labels.yaml").write_text(labels.read_text(encoding="utf-8"), encoding="utf-8"); run(root)
            (wt_ / "probe.html").write_text((wt_ / "index.html").read_text(encoding="utf-8").replace("</script></html>", "</script>" + probe + "</html>"), encoding="utf-8")
            pdom = subprocess.run([_CHROME, "--headless=new", "--disable-gpu", *_CHROME_FLAGS, "--window-size=500,900", "--virtual-time-budget=4000", "--dump-dom", (wt_ / "probe.html").as_uri()],
                                  capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60).stdout
            fits[lang] = _json.loads(_html.unescape((re.search(r'data-probe="([^"]*)"', pdom) or [None, "{}"])[1]) or "{}")
        want = {"en": fm.LABELS.get("search.help"), "de": fm.read_flat((HERE / "examples/de/labels.yaml").read_text(encoding="utf-8")).get("search.help")}
        check(f"R12 · the search placeholder fits the box at its 200 px minimum, in English and in German, measured in Chrome with the box's font; the whole help is the box's title (saw need/min: { {k: (v.get('need'), v.get('min')) for k, v in fits.items()} })",
              len(fits) == 2 and all(v.get("min") == 200 and v.get("need") and v["need"] <= v["min"] and want[k] and v.get("title") == want[k] for k, v in fits.items()))

# --- FM-021: the progress section says why it is empty, while no pass has run — and only then --------------------
if _CHROME:
    with tempfile.TemporaryDirectory() as d:
        root = Path(d).resolve()
        run(root, "--init", "--key", "msr")
        tracker(root, "MSR-001", title="Stock is booked per warehouse"); tracker(root, "MSR-002", title="Stock is counted per shelf")

        def progress_line():
            run(root)
            d_ = subprocess.run([_CHROME, "--headless=new", "--disable-gpu", *_CHROME_FLAGS, "--virtual-time-budget=4000", "--dump-dom",
                                 (root / "docs/work-tracker/index.html").as_uri()], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60).stdout
            shown = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", d_[d_.find("<tbody"):d_.find("</tbody>")]))
            progress_line.triaged = (re.search(r"[▾▸] triaged · \d+ · (.*?) [▾▸] backlog", shown) or [None, ""])[1].strip()
            return (re.search(r"▾ progress · 0 · ([^▾▸]*?) ▾ triage", shown) or [None, ""])[1].strip()
        before = progress_line()
        tracker(root, "MSR-003", status="Parked", extra="triaged: 2026-09-20\ntier: P3\n", title="A parked one")
        after = progress_line()
        check(f"FM-021 · work in progress and no pass run: the empty progress section says why, and names the command (saw: {before!r})",
              before == "empty until a first triage pass has run — --triage")
        check(f"FM-021 · …and once one tracker carries a pass's date, the line is its usual one again (saw: {after!r})",
              after == "kept by triage — by rank, then tier")
        (root / "docs/work-tracker/MSR-003-x.md").unlink()
        home = root / "docs/work-tracker/TRIAGE.md"
        home.write_text(home.read_text(encoding="utf-8").replace("*None yet.*", "2026-09-20 — a pass judged one tracker; worksheet `evidence/triage/triage-2026-09-20.md`."), encoding="utf-8")
        passed = progress_line()
        check(f"FM-021 · …and so it is when TRIAGE.md records a pass, though no tracker carries its date any more (saw: {passed!r})",
              passed == "kept by triage — by rank, then tier")
        check(f"R4 · in that state the triaged line agrees — it names the pass TRIAGE.md records, never 'no triage pass has run yet' (saw: {progress_line.triaged!r})",
              progress_line.triaged.startswith("judged 2026-09-20 — each also sits in its own section") and "no triage pass" not in progress_line.triaged)

# --- B′: a deriver by convention (R&D, FM-001) -------------------------------------------------------------
DERIVER = """#!/usr/bin/env python3
import json, subprocess, sys, os
ask = json.load(sys.stdin)
if os.path.exists(os.path.join(ask["root"], "REFUSE")):
    print("refusing: the precondition is not met", file=sys.stderr); sys.exit(5)
if os.path.exists(os.path.join(ask["root"], "GARBLE")):
    print("not json"); sys.exit(0)
tags = set(subprocess.run(["git", "-C", ask["root"], "tag", "--list"], capture_output=True, text=True, encoding="utf-8", errors="replace").stdout.split())
out = {"_keys": {"version": {"shape": r"\\d+\\.\\d+\\.\\d+", "says": "the release it shipped in"}}, "_problems": []}
if os.path.exists(os.path.join(ask["root"], "REDEFINE")):
    out["_keys"]["status"] = {"says": "mine now"}
for t in ask["trackers"]:
    v = t["fm"].get("version", "")
    out[t["id"]] = {"Ver": v or "—", "Live": "live" if v and "v" + v in tags else "—"}
    if v and t["status"] != "Shipped":
        out["_problems"].append(t["id"] + ": version on work that has not shipped")
json.dump(out, sys.stdout)
"""
with tempfile.TemporaryDirectory() as d:
    root = Path(d).resolve()
    git(root, "init", "-q"); run(root, "--init", "--key", "msr")
    tracker(root, "MSR-001", status="Shipped", extra="version: 1.2.0\n"); tracker(root, "MSR-002", status="Proposed")
    before_code, _, before_err = run(root)
    check("without a deriver an extension key is refused — the schema is closed", before_code == fm.EXIT_LINT and "`version:` is not a front-matter key" in before_err)
    exe = root / "docs/work-tracker/derive"; exe.write_text(DERIVER); exe.chmod(0o755)
    git(root, "add", "-A"); git(root, "commit", "-qm", "x"); git(root, "tag", "v1.2.0")
    code, _, err = run(root)
    index = (root / "docs/work-tracker/INDEX.md").read_text(); page = (root / "docs/work-tracker/index.html").read_text()
    check("a deriver at the one conventional path adds its keys to the schema and its values as columns — in INDEX.md and on the board, where each is also a view",
          code == 0 and "| Triaged | Ver | Live |" in index and "| 1.2.0 | live |" in index and 'COLS=["Ver", "Live"],BCOLS=["Ver", "Live"]' in page
          and '<th class="x">ver<th class="x">live' in page and "`version:`" in fm.render_schema())
    git(root, "tag", "-d", "v1.2.0")
    run(root)
    check("nothing derived is stored, so nothing derived is stale: the tag goes, and the very next run says so",
          "| 1.2.0 | — |" in (root / "docs/work-tracker/INDEX.md").read_text() and not list((root / "docs/work-tracker").glob(".derived*")))
    t2 = root / "docs/work-tracker/MSR-002-x.md"; t2.write_text(t2.read_text().replace("considered: none\n", "considered: none\nversion: 9.9\n"))
    code, _, err = run(root)
    check("the deriver's keys are gated like the core's, and its problems are counted with the core's",
          code == fm.EXIT_LINT and "`version:` is the release it shipped in" in err and "version on work that has not shipped" in err)
    t2.write_text(t2.read_text().replace("version: 9.9\n", ""))
    (root / "REFUSE").write_text(""); stamp = (root / "docs/work-tracker/INDEX.md").read_text()
    (root / "docs/work-tracker/MSR-001-x.md").write_text((root / "docs/work-tracker/MSR-001-x.md").read_text().replace("h of MSR-001", "changed"))
    code, _, err = run(root)
    check("a deriver that exits non-zero refuses the run with its own code, and nothing is written",
          code == 5 and "the precondition is not met" in err and (root / "docs/work-tracker/INDEX.md").read_text() == stamp)
    (root / "REFUSE").unlink(); (root / "GARBLE").write_text("")
    check("a deriver that does not answer in JSON is a refusal, not a traceback", run(root)[0] == fm.EXIT_LINT)
    (root / "GARBLE").unlink(); (root / "REDEFINE").write_text("")
    code, _, err = run(root)
    check("a deriver may add a key, never redefine one of the core's", code == fm.EXIT_LINT and "never redefine" in err)
# --- what an independent review of the first port found (the origin's RV-251 … RV-264) ------------------------
TOLD = """#!/usr/bin/env python3
import json, os, sys, time
ask = json.load(sys.stdin)
if "sleep" in ask["flags"]:
    time.sleep(5)
if "refuse" in ask["flags"] or os.environ.get("STRAY_EXPORT"):
    print("refused", file=sys.stderr); sys.exit(5)
json.dump({"_problems": [], "_notes": ["mode=" + ask["mode"] + " flags=" + ",".join(ask["flags"])]}, sys.stdout)
"""
with tempfile.TemporaryDirectory() as d:
    root = Path(d).resolve()
    git(root, "init", "-q"); run(root, "--init", "--key", "msr"); tracker(root, "MSR-001", status="Proposed")
    exe = root / "docs/work-tracker/derive"; exe.write_text(TOLD); exe.chmod(0o755)
    run(root, "--derive-flag", "b", "--derive-flag", "a")
    check("a deriver is told the mode and the flags typed on THIS run — on stdin", "mode=write flags=a,b" in (root / "docs/work-tracker/INDEX.md").read_text())
    os.environ["STRAY_EXPORT"] = "1"
    try:
        stray = run(root)[0]
    finally:
        del os.environ["STRAY_EXPORT"]
    check("what is exported in the shell that ran the commit never reaches a deriver — a stray variable cannot change what is staged",
          stray == 0 and run(root, "--derive-flag", "refuse")[0] == 5)
    check("the board's run says so: a deriver may skip a guard there, because nothing it produces can be committed",
          run(root, "--html-only")[0] == 0 and "mode=board" not in (root / "docs/work-tracker/INDEX.md").read_text())
    _t, fm.DERIVE_TIMEOUT = fm.DERIVE_TIMEOUT, 1
    try:
        code, _, err = run(root, "--derive-flag", "sleep")
    finally:
        fm.DERIVE_TIMEOUT = _t
    check("a deriver that hangs does not hang the gate: it is refused after a bounded wait, and says what ran long", code == fm.EXIT_LINT and "did not answer within 1 s" in err)
    exe.unlink()
    broken = root / "docs/work-tracker/MSR-002-x.md"; broken.write_text('---\nid: MSR-002\nstatus: Proposed\nnope: 1\nhook: "h"\n---\n\n# MSR-002 — t\n')
    code, out, _ = run(root, "--print-written")
    check("under a lint --print-written still names the paths while exiting 4 — a hook's `&&` is what keeps them unstaged", code == fm.EXIT_LINT and out.strip() == "docs/work-tracker/INDEX.md")
    broken.unlink(); run(root)
    code, out, _ = run(root, "--check", "--print-written")
    check("--check --print-written writes nothing and prints nothing", code == 0 and out.strip() == "")
fm.configure(HERE)

# --- the seam, after the origin's port was explored (FM-001) --------------------------------------------------
PORT_DERIVER = """#!/usr/bin/env python3
import json, sys
ask = json.load(sys.stdin)
out = {"_index": ["Ver"], "_board": ["Release"], "_notes": ["**Ver** = the release it shipped in."],
       "_keys": {"version": {"says": "the release"}, "target": {"says": "the plan"}}}
for t in ask["trackers"]:
    v, g = t["fm"].get("version", ""), t["fm"].get("target", "")
    out[t["id"]] = {"Ver": v or "—", "Release": [v, v + " ✓"] if v else [g, "→ " + g] if g else "—",
                    "_needs": [] if v or g else ["target"]}
json.dump(out, sys.stdout)
"""
with tempfile.TemporaryDirectory() as d:
    root = Path(d).resolve()
    git(root, "init", "-q"); run(root, "--init", "--key", "msr")
    home = root / "docs/work-tracker/TRIAGE.md"; home.write_text(home.read_text().replace("1.\n", "1. MSR-002 first.\n")); fm.configure(root)
    tracker(root, "MSR-001", status="Shipped", extra="version: 1.2.0\n"); tracker(root, "MSR-002", extra="target: 1.3.x\nrank: 1\ntier: P1\nnext: run\n")
    tracker(root, "MSR-003", extra="rank: 2\ntier: P2\nnext: run\n")
    exe = root / "docs/work-tracker/derive"; exe.write_text(PORT_DERIVER); exe.chmod(0o755)
    (root / "docs/work-tracker/brand").mkdir(); (root / "docs/work-tracker/brand/theme.css").write_text(":root{--bg:#123456}")
    code, _, err = run(root)
    index, page = (root / "docs/work-tracker/INDEX.md").read_text(), (root / "docs/work-tracker/index.html").read_text()
    check("one model, two renderings: the deriver says which values INDEX.md prints and which the board shows — every one stays a view",
          code == 0 and "| Triaged | Ver |" in index and "Release |" not in index and 'COLS=["Ver", "Release"],BCOLS=["Release"]' in page and '<th class="x">release<th data-l="col.title">' in page)
    check("a derived value may carry a display form — the value groups, sorts and is what INDEX.md prints; the form is for the board's cells",
          '{"Ver": "—", "Release": "1.3.x"}, {"Release": "→ 1.3.x"}' in page and '{"Release": "1.2.0 ✓"}' in page and "→" not in index.split("## Work")[1])
    check("a deriver may say what open work still needs, and explain its columns in INDEX.md's header",
          "| run | *complex* | intended, target | [MSR-003]" in index and "| run | *complex* | intended | [MSR-002]" in index and "> **Ver** = the release it shipped in." in index)
    exe.write_text(PORT_DERIVER.replace('json.dump(out, sys.stdout)', 'out["_files"] = {"docs/RELEASES.md": "# Releases\\n\\n1.2.0\\n", "../outside.md": "x"} if ask["root"].endswith("ESCAPE") else {"docs/RELEASES.md": "# Releases\\n\\n1.2.0\\n"}\njson.dump(out, sys.stdout)'))
    code, out, _ = run(root, "--print-written"); rel = root / "docs/RELEASES.md"
    wrote_ok = code == 0 and rel.read_text() == "# Releases\n\n1.2.0\n" and out.split() == ["docs/work-tracker/INDEX.md", "docs/RELEASES.md"]
    rel.write_text("tampered"); drift = run(root, "--check")[0]; run(root)
    check("a deriver has no side effects: the files it wants are written, staged and drift-checked by the core",
          wrote_ok and drift == fm.EXIT_DRIFT and rel.read_text() == "# Releases\n\n1.2.0\n")
    exe.write_text(PORT_DERIVER)
    check("a repository's own look is a convention, not a setting: `brand/theme.css` beside the trackers becomes a stylesheet of its own, after the tool's",
          '<style data-from="repository">:root{--bg:#123456}</style>' in page and page.index('data-from="repository"') > page.index("@media print"))
    os.environ["SHOALMARK_CMD"] = "python3 scripts/tracker.py"
    try:
        fm.configure(root); (root / "docs/work-tracker/INDEX.md").write_text("stale"); code, _, err = run(root, "--check")
    finally:
        del os.environ["SHOALMARK_CMD"]
    check("a repository that wraps the tool is named by its own command in every message", code == fm.EXIT_DRIFT and "Run: python3 scripts/tracker.py" in err)
    if _CHROME:
        run(root)
        body = subprocess.run([_CHROME, "--headless=new", "--disable-gpu", *_CHROME_FLAGS, "--virtual-time-budget=4000", "--dump-dom", (root / "docs/work-tracker/index.html").as_uri()], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60).stdout
        shown = re.sub(r"<[^>]+>", " ", body[body.find("<tbody"):body.find("</tbody>")])
        check("the board's cell shows the display form, rendered", "→ 1.3.x" in shown)
fm.configure(HERE)

# --- FM-002: a board anyone can brand — three files, four places, the nearest to the viewer wins -------------
GERMAN = """# ein deutsches Board
tagline: Lagerverwaltung
search: Suche — Id, Stufe, Status, Wörter
search.help: Eine ganze Id zeigt diesen Eintrag.
view.by: nach {0}
view.board: Tafel
view.epic: Vorhaben
view.open: offen
view.all: alle
scheme.auto: automatisch
scheme.light: hell
scheme.dark: dunkel
waiting.oldest: älteste seit {0} Tagen
waiting.holds: hält {0} weitere auf
waiting.days: seit {0} Tagen
waiting.holds.ids: hält auf: {0}
waiting.unasked: noch nicht als Frage gestellt
waiting.bottleneck: "du bist der Engpass — {0} Fragen, {1} Vorgänge warten"
waiting.malformed: "{0} Fragen zurückgegeben — nicht für Sie"
acts.title: Ihre Handlungen, mit ihrer Zeit
acts.promised: "zugesagt {0}: {1}"
acts.due: fällig {0}
acts.overdue: überfällig — fällig {0}
acts.missed: "versäumt — fällig {0}, und {1} Minuten ohne Ergebnis verstrichen"
acts.nodate: noch kein Termin
sessions.recent: Sitzungen · {0} am letzten Tag
reviews.week: Prüfungen dieser Woche · unabhängig {0} · gleiche Sitzung {1}
reviews.untraced: ohne Spur {0}
reviews.trunk: auf dem Stamm {0}
ask.ruling: eine Entscheidung
ask.action: nur Ihre Hände
ask.determination: ließe sich durch einen Versuch klären
ask.ceremony: ein Knopfdruck
answer.accept: annehmen
answer.reject: ablehnen
answer.proposal: "der Vorschlag der Sitzung:"
answer.other: "Andere:"
answer.recommended: empfohlen
answer.change.hint: "Ihre Änderung, in einer Zeile — mehr gehört in den Text des Eintrags"
answer.reject.hint: "warum, und wie die Frage neu gestellt werden soll (Pflicht)"
answer.ok: "OK — den Befehl geben"
answer.abort: abbrechen
answer.sign.title: Ihre Antwort signieren
answer.sign.intro: "Ihre Entscheidung steht. Ein Browser kann sie nicht signieren — Ihr Terminal tut es, mit Ihrem Schlüssel. Diesen Befehl ausführen:"
answer.sign.copy: nochmals kopieren
answer.sign.copied: Kopiert.
answer.sign.nocopy: "Nicht kopiert — diese Seite hat hier keine Zwischenablage (eine aus einer Datei geöffnete Tafel hat oft keine). Den Befehl markieren und kopieren."
answer.sign.where: Wo
answer.sign.where.text: "In einem Terminal, in diesem Repository, auf dem Zweig, der die Frage trägt."
answer.sign.where.branch: "In einem Terminal, in diesem Repository, auf dem Zweig, der die Frage trägt — {0}, dem Zweig, aus dem diese Tafel gebaut wurde."
answer.sign.does: Was er tut
answer.sign.step.cut: "legt {0} vom aktuellen Zweig an"
answer.sign.step.write: "schreibt die drei Zeilen — {0} {1} {2}"
answer.sign.step.commit: "committet sie, signiert mit Ihrem Schlüssel — ein Hardware-Schlüssel wartet auf Ihre Berührung"
answer.sign.step.push: pusht den Zweig
answer.sign.slow: "Er meldet jeden Schritt, sobald er beginnt, und kann eine Weile dauern: Zweigwechsel und Commit lassen jeweils die Prüfung über alle Einträge laufen."
answer.sign.success: Wenn es geklappt hat
answer.sign.check: Zur Kontrolle
answer.sign.check.text: "{0} gibt {1} aus — eine gültige Signatur, mit einem Schlüssel, dem dieses Repository vertraut."
answer.sign.fail: Wenn es scheitert
answer.sign.fail.text: "Kein Signierschlüssel gesetzt, oder die Signatur lässt sich nicht prüfen: den Schlüssel einmal einrichten — {0}."
answer.sign.page: "die Seite „Ihre Antwort ist Ihr Commit“"
answer.sign.url: "https://holgo99.github.io/shoalmark/de/signing/"
answer.done: Fertig
col.id: Id
col.tier: Stufe
col.status: Status
col.title: Titel
status.Proposed: Vorgeschlagen
status.In Progress: In Arbeit
status.Parked: Geparkt
status.Reserved: Reserviert
status.Shipped: Ausgeliefert
status.Closed: Geschlossen
status.Blocked: Blockiert
section.progress: in Arbeit
section.triage: zu sichten
section.triaged: gesichtet
section.backlog: Vorrat
section.done: erledigt
desc.progress: von der Sichtung behalten — nach Rang, dann Stufe
desc.progress.none: leer, bis eine erste Sichtung gelaufen ist — --triage
desc.triage: was die nächste Sichtung auflistet — in Arbeit und nicht oder vor über {0} Tagen bewertet, dazu neue Einträge
desc.triaged: bewertet am {0} — jeder steht auch in seinem eigenen Abschnitt
desc.triaged.none: noch keine Sichtung gelaufen
desc.backlog: wartet — P0 bis P3, dann ohne Stufe, dann geparkt
desc.done: ausgeliefert oder geschlossen
group.none: ohne {0}
count.trackers: Einträge
count.open: offen
count.around: rund um {0}
count.id: Eintrag · {0}
count.in_progress: in Arbeit
count.blocked: blockiert
count.untriaged: ungesichtet
path.title: der aktuelle Kurs
waiting.title: wartet auf Sie
waiting.detail: offene Arbeit, deren nächster Schritt beim Auftraggeber liegt
story.chapter: Kapitel
story.chapters: Kapitel
story.done: erledigt
story.open: offen
story.parked: geparkt
word.triaged: gesichtet
word.needs: braucht
word.blocked_by: blockiert durch
word.reads: Umfang
word.story: Vorhaben
word.missing: fehlt
word.stated: benannt
viewer.board: ← Tafel
viewer.neighbours: Nachbarn
viewer.file: Datei
viewer.forge: Ablage
viewer.no_copy: keine gerenderte Fassung von {0} — bitte {1} ausführen
viewer.intent: Absicht
viewer.from: aus {0}
viewer.intent.missing: fehlt — der Auftraggeber nennt sie am Eintrag oder am Vorhaben
viewer.verdict: Urteil
viewer.verdict.none: noch keines — keine Sichtung hat ihn bewertet
viewer.answer: die Antwort des Auftraggebers
viewer.supersedes: ersetzt {0}
relation.proposal: den Vorschlag angenommen
relation.changed: mit einer Änderung angenommen
relation.option: Option {0} gewählt
relation.rejected: abgelehnt
relation.revoked: zurückgenommen
relation.unknown: Bezug zum Vorschlag nicht bestimmbar
viewer.stale: veraltet — älter als {0} Tage, gilt wieder als ungesichtet
viewer.handover: Übergabe
viewer.next: nächster Schritt
viewer.kind: Art
viewer.from_move: aus dem Schritt
viewer.true_now: was jetzt gilt
viewer.no_move: ohne benannten Schritt
viewer.none_in_progress: nichts in Arbeit
"""
_SVG = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16"><script>document.title="PWNED"</script><rect width="16" height="16" fill="#0a7"/></svg>'
# a wordmark as a person draws one: the mark stroked, the name filled, both in the page's ink; an id the page also uses
_WORDMARK = ('<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
             'viewBox="0 0 40 16" height="16" fill="currentColor"><defs><path id="b" d="M0 0h4v4h-4Z"/></defs>'
             '<path d="M2 2v12" stroke="currentColor" stroke-width="2" fill="none"/><use xlink:href="#b" x="8"/><text x="14" y="13">Repo __ROWS__</text></svg>')
with tempfile.TemporaryDirectory() as d:
    base = Path(d).resolve(); root = base / "repo"; home = base / "home" / "shoalmark"; org = HERE / "brand"
    root.mkdir(); home.mkdir(parents=True)
    git(root, "init", "-q"); run(root, "--init", "--key", "msr"); fm.configure(root)
    tracker(root, "MSR-001", title="Bestand je Lager"); tracker(root, "MSR-002", status="Shipped", title="Erledigtes")
    wt = root / "docs/work-tracker"
    _xdg = os.environ.get("XDG_CONFIG_HOME")
    def board_with(**files):
        """files: place_file=text — place is org | repo | me. Returns (INDEX.md bytes, page, --brand report)."""
        for place in (org, home):
            shutil.rmtree(place, ignore_errors=True)
        shutil.rmtree(wt / "brand", ignore_errors=True)
        for f in fm.BRAND_FILES:
            (wt / f).unlink(missing_ok=True)
        for key, text in files.items():
            place, _, name = key.partition("_")
            d_ = {"org": org, "repo": wt / "brand", "me": home, "loose": wt}[place]; d_.mkdir(parents=True, exist_ok=True)
            (d_ / name.replace("_", ".")).write_text(text, encoding="utf-8")
        os.environ["XDG_CONFIG_HOME"] = str(base / "home")
        code, _, err = run(root)
        _, report, _ = run(root, "--brand")
        return (wt / "INDEX.md").read_bytes(), (wt / "index.html").read_text(encoding="utf-8"), report, err, code
    import shutil
    try:
        plain_index, plain_page, _, _, _ = board_with()
        hostile = dict(me_theme_css=":root{--bg:#ff0000}", me_labels_yaml="status.Shipped: LIVE\nstatus.Parked: GONE\n", me_logo_svg=_SVG,
                       org_theme_css=":root{--ink:#00ff00}", org_labels_yaml="status.Proposed: MAYBE\n")
        h_index, h_page, h_report, _, h_code = board_with(**hostile)
        check("C1 · committed output ignores every brand layer: with a hostile person and a hostile organisation present, INDEX.md is byte-identical and the gate's verdict unchanged",
              h_index == plain_index and h_code == 0 and run(root, "--check")[0] == 0 and run(root, "--print-written")[1].strip() == "docs/work-tracker/INDEX.md")
        i_org, i_repo, i_me = (h_page.find(f'<style data-from="{w}">') for w in ("organisation", "repository", "person"))
        check("C2 · one rule — every place's theme is its own stylesheet, in order, the person's last; labels merge key by key; the last logo found wins; --brand says the same",
              0 < i_org < i_me and i_repo == -1 and '"status.Shipped": "LIVE"' in h_page and '"status.Proposed": "MAYBE"' in h_page and '"status.Closed": "Closed"' in h_page
              and "theme.css     organisation → person" in h_report and "logo          person" in h_report and "labels changed: 3 of" in h_report)
        _, p2, r2, _, _ = board_with(org_theme_css="a{}", repo_theme_css="b{}", repo_labels_yaml="tagline: from the repo\n", org_labels_yaml="tagline: from the org\nfooter: set up by X\n")
        check("C2 · the repository beats the organisation, key by key — and what only the organisation says survives",
              '"tagline": "from the repo"' in p2 and '"footer": "set up by X"' in p2 and "theme.css     organisation → repository" in r2)
        board_with()                                          # every place emptied
        del os.environ["XDG_CONFIG_HOME"]; _h = os.environ.pop("HOME", None)
        try:
            shutil.rmtree(org, ignore_errors=True); nohome = run(root)[0]; no_page = (wt / "index.html").read_text(encoding="utf-8")
        finally:
            if _h is not None:
                os.environ["HOME"] = _h
        check("C3 · nothing present, no HOME at all — a hook, CI, an agent — and the board still renders, with no theme, no logo and the English words",
              nohome == 0 and "<style data-from" not in no_page and "<img" not in no_page.split("<script>")[0] and '"status.Shipped": "Shipped"' in no_page)
        _, de_page, _, de_err, _ = board_with(repo_labels_yaml=GERMAN)
        check("C4 · a German board needs no code: every label has a German value, none is unknown, and what the page's logic compares is untouched",
              set(fm.read_flat(GERMAN)) == set(fm.LABELS) - {"footer"} and "is not a label" not in de_err and 't[2]=="In Progress"' in de_page and '"status.In Progress": "In Arbeit"' in de_page)
        _shipped_de = fm.read_flat((HERE / "examples/de/labels.yaml").read_text(encoding="utf-8"))
        check("C4 · the German table the tool SHIPS (examples/de/labels.yaml) carries every label and none that is not one — a new word of the chrome lands in every language at once",
              set(fm.LABELS) - set(_shipped_de) <= {"footer", "tagline"} and not set(_shipped_de) - set(fm.LABELS))
        if _CHROME:
            dom = lambda frag: subprocess.run([_CHROME, "--headless=new", "--disable-gpu", *_CHROME_FLAGS, "--virtual-time-budget=4000", "--dump-dom", (wt / "index.html").as_uri() + frag], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60).stdout
            text = lambda d_: re.sub(r"\s+", " ", re.sub(r"<(script|style)[\s\S]*?</\1>|<[^>]+>", " ", d_))
            chrome = lambda d_: d_[:d_.find('<div class="md">')] if '<div class="md">' in d_ else d_        # a tracker's own text is the repository's, not the board's
            shown = text(dom("")) + " " + text(chrome(dom("#=MSR-001")))
            english = sorted({w for w in ("open", "all", "title", "tier", "progress", "triage", "triaged", "backlog", "done", "trackers", "proposed", "shipped",
                                          "closed", "parked", "blocked", "board", "neighbours", "file", "intent", "verdict", "missing", "stated", "hand-over", "untriaged", "waiting", "kept")
                              if re.search(rf"(?<![\w-]){w}(?![\w-])", shown.replace("docs/work-tracker", ""), re.I)})
            check(f"C4 · rendered in a browser, the German board's chrome holds no English word (found: {english})", not english and "In Arbeit" in shown and "Lagerverwaltung" in shown)
            _, _, _, _, _ = board_with(repo_logo_svg=_SVG)
            ldom = dom("")
            check("C5 · a logo is shown in the header and as the favicon — and a script inside the SVG does nothing", "<title>repo — work tracker</title>" in ldom and ldom.count("data:image/svg+xml;base64,") >= 2 and "PWNED" not in text(ldom))
            # the scheme button: clicked for real, three times round — whatever the machine's own setting is
            (wt / "brand/theme.css").write_text(":root{--bg:#010203}\n@media screen and (prefers-color-scheme:dark){:root{--bg:#040506}}\n", encoding="utf-8"); run(root)
            probe = '<script>{const o=[];for(let i=0;i<3;i++){$("s").click();o.push($("s").dataset.scheme+"="+getComputedStyle(document.body).backgroundColor)}document.body.dataset.probe=o.join("|")}</script>'
            (wt / "probe.html").write_text((wt / "index.html").read_text(encoding="utf-8").replace("</script></html>", "</script>" + probe + "</html>"), encoding="utf-8")
            pdom = subprocess.run([_CHROME, "--headless=new", "--disable-gpu", *_CHROME_FLAGS, "--virtual-time-budget=4000", "--dump-dom", (wt / "probe.html").as_uri()], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60).stdout
            seen = (re.search(r'data-probe="([^"]*)"', pdom) or [None, ""])[1]
            check(f"the scheme button switches any theme's light and dark by hand — a brand needs to know nothing about it (saw: {seen})",
                  "light=rgb(1, 2, 3)" in seen and "dark=rgb(4, 5, 6)" in seen and seen.count("auto=") == 1)
            (wt / "probe.html").unlink(); (wt / "brand/theme.css").unlink()
        (wt / "brand").mkdir(exist_ok=True); (wt / "brand/logo.png").write_bytes(b"\x89PNG" + b"0" * (fm.LOGO_MAX + 1)); (wt / "brand/logo.svg").unlink(missing_ok=True)
        code, _, err = run(root)
        check("C5 · a logo past the size cap is skipped with a warning, never inlined", code == 0 and "not shown" in err and "data:image/png" not in (wt / "index.html").read_text(encoding="utf-8"))
        # --- 0.18.2 (FM-006): a fourth brand file, wordmark.svg — the mark and the name as one drawing, inline in the header
        head = lambda page: page[page.index('<div id="H">'):page.index('<button id="s">')]
        _, w_page, w_report, w_err, w_code = board_with(repo_wordmark_svg=_WORDMARK, repo_logo_svg=_SVG.replace("<script>document.title=\"PWNED\"</script>", ""))
        w_head = head(w_page)
        check("0.18.2 · a wordmark is inlined in the header in place of the logo and the name; the name stays the page's title and the wordmark's accessible name; the logo stays the tab's",
              w_code == 0 and w_head.startswith('<div id="H"><b class="wm" role="img" aria-label="repo"><svg viewBox="0 0 40 16" height="16" fill="currentColor">')
              and "<img" not in w_head and "<b>repo</b>" not in w_page and "<title>repo — work tracker</title>" in w_page and '<link rel="icon" href="data:image/svg+xml;base64,' in w_page)
        check("0.18.2 · the wordmark keeps currentColor, fill and stroke — it takes the page's ink — and is written out again from what was read: its ids and their references prefixed, no placeholder of the page's spelled in it",
              '<path d="M2 2v12" stroke="currentColor" stroke-width="2" fill="none"></path>' in w_head and '<path id="wm-b" d="M0 0h4v4h-4Z"></path>' in w_head
              and '<use xlink:href="#wm-b" x="8"></use>' in w_head and "Repo &#95;&#95;ROWS&#95;&#95;</text>" in w_head and w_page.count('id="b"') == 1 and "<?xml" not in w_page)
        check("0.18.2 · --brand lists the wordmark's place like the other files", "wordmark      repository" in w_report and "logo          repository" in w_report)
        _, n_page, n_report, _, _ = board_with(repo_logo_svg=_SVG)
        check("0.18.2 · without a wordmark nothing changes: the logo, then the name", head(n_page).startswith('<div id="H"><img alt="" src="data:image/svg+xml;base64,') and head(n_page).endswith('"><b>repo</b><span data-l="tagline"></span>')
              and "wordmark      built in" in n_report)
        refused = {why: board_with(repo_wordmark_svg=svg, repo_logo_svg=_SVG) for why, svg in (
            ("it holds <script>", _SVG), ("it holds onload= on <svg>, which a wordmark may not carry", _WORDMARK.replace('height="16"', 'height="16" onload="document.title=1"')),
            ('its href="https://example.org/w.svg#b" on <use> is not what href takes', _WORDMARK.replace('xlink:href="#b"', 'xlink:href="https://example.org/w.svg#b"')),
            ("it holds <style>", _WORDMARK.replace("<defs>", "<style>body{display:none}</style><defs>")),
            ("it holds <foreignObject>", _WORDMARK.replace("<defs>", '<foreignObject><p xmlns="http://www.w3.org/1999/xhtml">x</p></foreignObject><defs>')))}
        check("0.18.2 · a wordmark holding a script, a handler, an outside reference, a <style> or a foreignObject is refused whole, with a warning that says why — the header keeps the logo and the name",
              all(code_ == 0 and f"repository's wordmark.svg is not shown: {why}" in err_ and "the header keeps the logo and the name" in err_ and 'class="wm"' not in page_
                  and "<b>repo</b>" in page_ and "PWNED" not in page_ for why, (_, page_, _, err_, code_) in refused.items()))
        _, c_page, _, c_err, c_code = board_with(repo_wordmark_svg=_WORDMARK.replace("</svg>", "<desc>" + "x" * fm.LOGO_MAX + "</desc></svg>"))
        check("0.18.2 · a wordmark past the size cap is skipped with a warning that names its bytes, never inlined",
              c_code == 0 and f"wordmark.svg is not shown: it is {len(_WORDMARK) + 13 + fm.LOGO_MAX:,} bytes — over 200,000" in c_err and 'class="wm"' not in c_page)
        _, o_page, o_report, o_err, _ = board_with(org_wordmark_svg=_WORDMARK, repo_wordmark_svg=_SVG)
        check("0.18.2 · a later place's wordmark wins, and one that is refused leaves the earlier one standing",
              "wordmark      organisation" in o_report and 'aria-label="repo"><svg viewBox="0 0 40 16"' in o_page and "the header keeps the wordmark before it" in o_err)
        # --- 0.18.2, the Reviewer's R1–R5: a wordmark is held to a grammar — one check per refusal, each case the Reviewer's
        _W = lambda body, root="": (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 10 10"{root}>'
                                    f'{body}</svg>').encode("utf-8")
        _fan = ('<defs><g id="l0"><path d="M0 0h1v1h-1Z"/></g>' + "".join(f'<g id="l{i}">' + f'<use href="#l{i - 1}"/>' * 10 + "</g>" for i in range(1, 7))
                + '</defs><use href="#l6"/>')                  # 1.3 kB, a million instances
        _chain = '<defs><path id="l0" d="M0 0h1v1h-1Z"/>' + "".join(f'<g id="l{i}"><use href="#l{i - 1}"/></g>' for i in range(1, 6)) + '</defs><use href="#l5"/>'
        _decoy = ('<defs><g id="l0"><path d="M0 0h1v1h-1Z"/></g><g id="l0"/>'
                  + "".join(f'<g id="l{i}">' + f'<use href="#l{i - 1}"/>' * 10 + f'</g><g id="l{i}"/>' for i in range(1, 7)) + '</defs><use href="#l6"/>')
        _masks = lambda el, attr: (f'<defs><{el} id="m0"><rect width="1" height="1" fill="white"/></{el}>'
                                   + "".join(f'<{el} id="m{k}">' + f'<rect width="1" height="1" fill="white" {attr}="url(#m{k - 1})"/>' * 10 + f'</{el}>' for k in range(1, 8))
                                   + f'</defs><rect width="10" height="10" {attr}="url(#m7)"/>')
        _mask_used = lambda n: '<defs><mask id="m">' + '<rect width="1" height="1" fill="white"/>' * 100 + '</mask></defs>' + '<rect width="1" height="1" mask="url(#m)"/>' * n
        _laughs = ('<?xml version="1.0" encoding="UTF-16"?><!DOCTYPE svg [<!ENTITY a "aaaaaaaaaa"><!ENTITY b "&a;&a;&a;&a;&a;&a;&a;&a;&a;&a;">]>'
                   '<svg xmlns="http://www.w3.org/2000/svg"><text>&b;</text></svg>')
        for case, svg, why in (
                ("a CSS escape \\72 in fill", _W('<path d="M0 0" fill="u\\72l(http://127.0.0.1:8765/a)"/>'), 'its fill="u\\72l(http://127.0.0.1:8765/a)" on <path> is not what fill takes'),
                ("a CSS escape \\r in fill", _W('<path d="M0 0" fill="u\\rl(//127.0.0.1:8765/a)"/>'), 'its fill="u\\rl(//127.0.0.1:8765/a)" on <path> is not what fill takes'),
                ("a CSS escape \\0072 in stroke", _W('<path d="M0 0" stroke="u\\0072l(//127.0.0.1:8765/a)"/>'), 'its stroke="u\\0072l(//127.0.0.1:8765/a)" on <path> is not what stroke takes'),
                ("a CSS escape \\u in mask", _W('<path d="M0 0" mask="\\u0075rl(//127.0.0.1:8765/a)"/>'), 'its mask="\\u0075rl(//127.0.0.1:8765/a)" on <path> is not what mask takes'),
                ("the escape's backslash as &#92;", _W('<path d="M0 0" fill="u&#92;72l(//127.0.0.1:8765/a)"/>'), 'its fill="u\\72l(//127.0.0.1:8765/a)" on <path> is not what fill takes'),
                ("a style attribute", _W('<path d="M0 0"/>', ' style="background-image:u\\72l(http://127.0.0.1:8765/a)"'), "it holds style= on <svg>, which a wordmark may not carry"),
                ("an unknown attribute", _W('<path d="M0 0"/>', ' autofocus="" tabindex="0"'), "it holds autofocus= on <svg>, which a wordmark may not carry"),
                ("a class", _W('<path class="m" d="M0 0"/>'), "it holds class= on <path>, which a wordmark may not carry"),
                ("xml:base", _W('<path d="M0 0"/>', ' xml:base="http://e.x/"'), "it holds xml:base= on <svg>, which a wordmark may not carry"),
                ("a UTF-16 file with a DOCTYPE and entities", _laughs.encode("utf-16"), "it is not UTF-8 without a byte-order mark"),
                ("the same UTF-16, no byte-order mark", _laughs.encode("utf-16-le"), "it holds a control character"),
                ("a UTF-8 byte-order mark", b"\xef\xbb\xbf" + _W('<path d="M0 0"/>'), "it is not UTF-8 without a byte-order mark"),
                ("another encoding declared", b'<?xml version="1.0" encoding="ISO-8859-1"?>' + _W('<path d="M0 0"/>'), "its <?xml?> names the encoding ISO-8859-1, not UTF-8"),
                ("the Reviewer's 1.3 kB <use> fan-out", _W(_fan), "its references nest deeper than 3"),
                ("a <use> chain five deep", _W(_chain), "its references nest deeper than 3"),
                ("a <use> cycle", _W('<g id="a"><use href="#a"/></g>'), "its references form a cycle"),
                ("a <use> of an id it does not have", _W('<use href="#nope"/>'), "it refers to #nope, which the file does not have"),
                ("1,000 nested <g>", _W("<g>" * 1000 + '<path d="M0 0"/>' + "</g>" * 1000), "it nests deeper than 32"),
                # the second pass: R7 — the graph the browser draws; R9 — the rule's letter; R8's grammar, stricter
                ("R7 · the fan-out with every id defined twice, a decoy after each", _W(_decoy), "the id l0 is defined twice"),
                ("R7 · masks nested 7 deep, ten a level", _W(_masks("mask", "mask")), "its references nest deeper than 3"),
                ("R7 · clip-paths nested 7 deep, ten a level", _W(_masks("clipPath", "clip-path")), "its references nest deeper than 3"),
                ("R7 · a mask of 100 used 30 times — it paints 30 times", _W(_mask_used(30)), "it paints over 2,000 elements once its references are followed"),
                ("R9 · url(#id) of an id it does not have", _W('<path d="M0 0" fill="url(#nope)"/>'), "it refers to #nope, which the file does not have"),
                ("R9 · Unicode digits", _W('<rect width="\u0661\u0662"/>'), 'its width="\u0661\u0662" on <rect> is not what width takes'),
                ("R9 · a full-width digit", _W('<rect x="\uff11"/>'), 'its x="\uff11" on <rect> is not what x takes'),
                ("R9 · DEL", _W("<text>a\x7fb</text>"), "it holds a control character"),
                ("R9 · a C1 control", _W("<text>a\x85b</text>"), "it holds a control character"),
                ("R8 · two numbers in a path without a separator", _W('<path d="M1-2"/>'), 'its d="M1-2" on <path> is not what d takes'),
                ("R8 · a number with no digit before its point", _W('<rect width=".5"/>'), 'its width=".5" on <rect> is not what width takes'),
                ("R8 · an exponent", _W('<rect width="1e3"/>'), 'its width="1e3" on <rect> is not what width takes'),
                ("R8 · two separators in a transform's list", _W('<path d="M0 0" transform="translate(1, 2)"/>'), 'its transform="translate(1, 2)" on <path> is not what transform takes')):
            check(f"0.18.2 · R1–R5 · {case} is refused: {why}", fm.inline_svg(svg) == ("", why))
        _ok = fm.inline_svg(_W('<defs><linearGradient id="g" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#123456"/></linearGradient></defs>'
                               '<path d="M0 0h1v1h-1Z" fill="url(#g)" transform="translate(1,2) scale(2)"/><path d="M1 1" stroke="navy" stroke-width="1.5px"/>'
                               '<text x="1 2.5px,3%" y="4" transform="translate(1,2)scale(2)">a</text>'))[0]
        check("0.18.2 · what a drawing needs still passes: a gradient by url(#id) of its own, a transform, a named colour, a list of lengths — and a mask of 100 used 10 times",
              'fill="url(#wm-g)" transform="translate(1,2) scale(2)"' in _ok and '<linearGradient id="wm-g" gradientUnits="userSpaceOnUse">' in _ok and 'stroke="navy"' in _ok
              and '<text x="1 2.5px,3%" y="4" transform="translate(1,2)scale(2)">a</text>' in _ok and fm.inline_svg(_W(_mask_used(10)))[1] == "")
        # R8: one pass of a scanner, never a regex — the Reviewer's backtracking cases at 10 kB, timed; R9: the count stops early
        import time as _time
        _slow = (("the Reviewer's `x=\"111 111 … !\"`", _W('<text x="' + "111 " * 2500 + '!">a</text>'), 0.05),
                 ("a transform of 1,100 functions and a `!`", _W('<path d="M0 0" transform="' + "scale(1) " * 1100 + '!"/>'), 0.05),
                 ("the same with two spaces between", _W('<path d="M0 0" transform="' + "scale(1)  " * 1000 + '!"/>'), 0.05),
                 ("a width of 20,000 digits and a `!`", _W('<rect width="' + "1" * 20000 + '!"/>'), 0.05),
                 ("800 paths drawn by 10,000 <use>s, 179 kB — refused by the count as it goes", _W('<defs><g id="a">' + '<path d="M0 0h1v1h-1Z"/>' * 800 + '</g></defs>' + '<use href="#a"/>' * 10000), 1.0))
        for case, svg, limit in _slow:
            _t0 = _time.perf_counter(); _why = fm.inline_svg(svg)[1]; _ms = (_time.perf_counter() - _t0) * 1000
            check(f"0.18.2 · R8/R9 · {case} ({len(svg):,} bytes) is refused in under {limit * 1000:.0f} ms (took {_ms:.1f} ms): {_why}", _why and _ms < limit * 1000)
        _, x_page, _, x_err, x_code = board_with(repo_wordmark_svg=_W('<text x="' + "111 " * 30 + '!">a</text>').decode(), repo_logo_svg=_SVG)
        check("0.18.2 · R8 · the Reviewer's 246-byte wordmark that hung the build is a warning: the build and --print-written exit 0",
              x_code == 0 and "wordmark.svg is not shown: its x=" in x_err and "<b>repo</b>" in x_page and run(root, "--print-written")[0] == 0)
        _, d_page, _, d_err, d_code = board_with(repo_wordmark_svg="<svg xmlns=\"http://www.w3.org/2000/svg\">" + "<g>" * 1000 + "</g>" * 1000 + "</svg>", repo_logo_svg=_SVG)
        check("0.18.2 · R4 · a wordmark nested 1,000 deep is a warning, not a traceback: the build and --print-written exit 0",
              d_code == 0 and "wordmark.svg is not shown: it nests deeper than 32" in d_err and "<b>repo</b>" in d_page and run(root, "--print-written")[0] == 0)
        # --- 0.18.2: the running line — the tool's mark, name and version, on every page, whatever the brand
        _ver = (HERE / "VERSION").read_text(encoding="utf-8").strip()
        _run = lambda page: (re.search(r'</article>\n(<p id="r" class="m">.*?</p>)\n<dialog', page) or [None, ""])[1]
        _links = lambda line: re.findall(r'<a href="([^"]+)" target="_blank" rel="noopener" aria-label="([^"]+)">', line)
        check("0.18.2 · the running line ends every page — no brand, a hostile one, a German one, a wordmark, a logo — outside the board and the tracker view: two links, the tool and its release at VERSION, the ' · ' between them plain",
              all(_links(_run(pg)) == [("https://github.com/holgo99/shoalmark", "shoalmark on GitHub"), (f"https://github.com/holgo99/shoalmark/releases/tag/v{_ver}", f"release v{_ver}")]
                  and _run(pg).endswith(f'shoalmark</a> · <a href="https://github.com/holgo99/shoalmark/releases/tag/v{_ver}" target="_blank" rel="noopener" aria-label="release v{_ver}">v{_ver}</a></p>')
                  for pg in (plain_page, h_page, de_page, w_page, n_page)))
        check("0.18.2 · the running line's mark is the Pricke inline, in currentColor, at 16 px — its own grid, so sharp — inside the first link, and it is the site's mark",
              f'aria-label="shoalmark on GitHub"><svg viewBox="0 0 16 16" width="16" height="16" fill="currentColor" shape-rendering="crispEdges" aria-hidden="true"><path d="{fm.PRICKE}"></path></svg>shoalmark</a>' in _run(plain_page)
              and fm.PRICKE == re.search(r' d="([^"]+)"', (HERE / "overrides/.icons/shoalmark/pricke.svg").read_text(encoding="utf-8")).group(1))
        if _CHROME:
            board_with(repo_wordmark_svg=_WORDMARK, repo_theme_css=":root{--ink:#010203}\n@media (prefers-color-scheme:dark){:root{--ink:#fdfcfb}}\n")
            probe = ('<script>{const o=[],p=document.querySelector("#H .wm svg path[stroke]");for(let i=0;i<3;i++){$("s").click();'
                     'o.push($("s").dataset.scheme+"="+getComputedStyle(p).stroke+"/"+getComputedStyle(document.querySelector("#H .wm svg")).height)}document.body.dataset.probe=o.join("|")}</script>')
            (wt / "probe.html").write_text((wt / "index.html").read_text(encoding="utf-8").replace("</script></html>", "</script>" + probe + "</html>"), encoding="utf-8")
            pdom = subprocess.run([_CHROME, "--headless=new", "--disable-gpu", *_CHROME_FLAGS, "--virtual-time-budget=4000", "--dump-dom", (wt / "probe.html").as_uri()], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60).stdout
            seen = (re.search(r'data-probe="([^"]*)"', pdom) or [None, ""])[1]
            check(f"0.18.2 · in a browser the wordmark's stroke is the theme's ink, light and dark, through the ◐ switch, at the height it declares (saw: {seen})",
                  "light=rgb(1, 2, 3)/16px" in seen and "dark=rgb(253, 252, 251)/16px" in seen)
            shown = []
            for frag in ("", "#=MSR-001"):                   # the board, then a tracker's view: every screen a viewer can be on
                probe = '<script>document.body.dataset.probe=[$("B").hidden,$("v").hidden,$("r").offsetHeight>0,$("r").textContent].join("|")</script>'
                (wt / "probe.html").write_text((wt / "index.html").read_text(encoding="utf-8").replace("</script></html>", "</script>" + probe + "</html>"), encoding="utf-8")
                pdom = subprocess.run([_CHROME, "--headless=new", "--disable-gpu", *_CHROME_FLAGS, "--virtual-time-budget=4000", "--dump-dom", (wt / "probe.html").as_uri() + frag], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60).stdout
                shown.append((re.search(r'data-probe="([^"]*)"', pdom) or [None, ""])[1])
            check(f"0.18.2 · in a browser the running line is shown on the board and on a tracker's view (saw: {shown})",
                  shown == [f"false|true|true|shoalmark · v{_ver}", f"true|false|true|shoalmark · v{_ver}"])
            (wt / "probe.html").unlink()
        _, _, _, c_err, c_code = board_with(me_theme_css=":root{--bg:#777777;--ink:#888888}")
        check("C6 · an unreadable theme is a warning that names the two colours and whose file it is — never a failure", c_code == 0 and "person's theme.css: text #888888 on ground #777777" in c_err and "below 4.5:1" in c_err)
        check("C6 · contrast is the WCAG ratio", round(fm.contrast("#000000", "#ffffff")) == 21 and fm.contrast("#777777", "#888888") < 1.5)
        _, i_page, _, i_err, i_code = board_with(repo_theme_css='@import url("../../gone/tokens.css");\n:root{--bg:var(--x)}', repo_labels_yaml="tagline: still here\n", me_theme_css=":root{--mute:#123123}")
        check("C10 · a theme whose import is missing is left out whole — the board keeps its colours, says so once, and the other places still apply",
              i_code == 0 and "imports ../../gone/tokens.css, which is not there" in i_err and "var(--x)" not in i_page and "--mute:#123123" in i_page and '"tagline": "still here"' in i_page)
        (wt / "brand/fonts").mkdir(parents=True, exist_ok=True); (wt / "brand/fonts/mine.woff2").write_bytes(b"x"); (home / "tokens.css").parent.mkdir(parents=True, exist_ok=True)
        _, u_page, _, u_err, _ = board_with(repo_theme_css='@font-face{font-family:"Mine";src:url("fonts/mine.woff2")}\na{background:url(https://example.org/x.png)}',
                                            me_theme_css='@import url("tokens.css");\n:root{--mute:#abcabc}', me_tokens_css=":root{--x:1}")
        (wt / "brand/fonts").mkdir(parents=True, exist_ok=True); (wt / "brand/fonts/mine.woff2").write_bytes(b"x"); run(root)
        u_page = (wt / "index.html").read_text(encoding="utf-8")
        check("a path in a theme is written relative to the file it is in, and re-based onto the page — so a font beside the theme, and an import in the person's own folder, both resolve; an absolute URL is left alone",
              'src:url("brand/fonts/mine.woff2")' in u_page and "url(https://example.org/x.png)" in u_page
              and re.search(r'@import url\("(\.\./)+.*home/shoalmark/tokens\.css"\)', u_page) is not None and "is not there" not in u_err)
        _, l_page, _, l_err, l_code = board_with(loose_theme_css=":root{--bg:#010203}", loose_labels_yaml="tagline: old place\n")
        check("brand files left loose beside the trackers are not read — and the warning says where they belong",
              l_code == 0 and "--bg:#010203" not in l_page and "old place" not in l_page and "theme.css, labels.yaml beside the trackers are not read" in l_err and "docs/work-tracker/brand/" in l_err)
        _, t_page, _, t_err, t_code = board_with(repo_labels_yaml="tagine: a typo\nstatus.Shipped: Live\n")
        check("a mistyped label is named in a warning and never reaches the page — the rest of the file still applies",
              t_code == 0 and "labels.yaml: tagine is not a label" in t_err and '"tagine"' not in t_page and '"status.Shipped": "Live"' in t_page)
        board_with(org_theme_css=":root{--blue:#123456}", org_labels_yaml="footer: set up by X with shoalmark\n")
        dest = base / "client" / "tools" / "shoalmark"
        with redirect_stdout(io.StringIO()):
            fm.vendor(dest, allow_untagged=True)
        check("C7 · the organisation's brand travels with --vendor and is pinned like the rest of the copy",
              (dest / "brand/theme.css").read_text() == ":root{--blue:#123456}" and "brand/theme.css" in (dest / "PIN").read_text() and "brand/labels.yaml" in (dest / "PIN").read_text())
        (base / "client/docs/work-tracker").mkdir(parents=True)
        (base / "client/docs/work-tracker/MSR-001-x.md").write_text('---\nid: MSR-001\nstatus: Proposed\nconsidered: none\nhook: "h"\n---\n\n# MSR-001 — x\n')
        (base / "client/shoalmark.toml").write_text('[kinds]\nMSR = "Work"\n'); (base / "client/docs/work-tracker/brand").mkdir(); (base / "client/docs/work-tracker/brand/labels.yaml").write_text("footer: ours\n")
        r = subprocess.run([sys.executable, str(dest / "shoalmark.py"), "--root", str(base / "client")], capture_output=True, text=True, encoding="utf-8", errors="replace", env=dict(_ENV, XDG_CONFIG_HOME=str(base / "nowhere")))
        cpage = (base / "client/docs/work-tracker/index.html").read_text(encoding="utf-8")
        check("C7 · …and the client overrides it beside its own trackers, without touching the pinned copy", r.returncode == 0 and '"footer": "ours"' in cpage and "--blue:#123456" in cpage)
        (dest / "VERSION").write_text("0.0.1-vendored\n", encoding="utf-8")
        r = subprocess.run([sys.executable, str(dest / "shoalmark.py"), "--root", str(base / "client"), "--html-only"], capture_output=True, text=True, encoding="utf-8", errors="replace", env=dict(_ENV, XDG_CONFIG_HOME=str(base / "nowhere")))
        check("0.18.2 · a vendored copy's running line names the version IT runs — its own VERSION, its own release page",
              r.returncode == 0 and '<a href="https://github.com/holgo99/shoalmark/releases/tag/v0.0.1-vendored" target="_blank" rel="noopener" aria-label="release v0.0.1-vendored">v0.0.1-vendored</a></p>'
              in (base / "client/docs/work-tracker/index.html").read_text(encoding="utf-8"))
        with redirect_stdout(io.StringIO()):
            fm.brand_report(str(base / "starter"))
        starter = fm.read_flat((base / "starter/labels.yaml").read_text(encoding="utf-8"))
        check("--brand DIR writes a starter a person can edit: every label in English, and a theme that names the nine variables",
              starter == {k: v for k, v in fm.LABELS.items()} and all(v in (base / "starter/theme.css").read_text() for v in ("--bg", "--ink", "--dim", "--mute", "--line", "--teal", "--coral", "--blue", "--yellow")))
        check("0.18.2 · the starter's theme states the whole drawing rule in a comment — viewBox and height, currentColor, the name as paths or <text>, the pixel grid, shapes only, never style, the logo stays the tab's (R6)",
              all(w in (base / "starter/theme.css").read_text() for w in ("wordmark.svg", 'fill="currentColor"', "the browser tab", "viewBox", "the name as paths",
                                                                           "whole multiple of its grid", 'never style="…"', "refuses it whole")))
    finally:
        shutil.rmtree(org, ignore_errors=True)
        if _xdg is None:
            os.environ.pop("XDG_CONFIG_HOME", None)
        else:
            os.environ["XDG_CONFIG_HOME"] = _xdg
fm.configure(HERE)

# --- 0.18.2 (FM-006): this repository's own board wears the site's brand — its brand files, held to their sources ------
_rb, _xdg = HERE / "work-tracker/brand", os.environ.get("XDG_CONFIG_HOME")
with tempfile.TemporaryDirectory() as _nowhere:
    os.environ["XDG_CONFIG_HOME"] = _nowhere                 # the person's own place stays out of it
    try:
        fm.configure(HERE); _themes, _logo, _labels, _src, _warn, _wm = fm.brand()
    finally:
        os.environ.pop("XDG_CONFIG_HOME", None) if _xdg is None else os.environ.update(XDG_CONFIG_HOME=_xdg)
_given, _css = fm.read_flat((_rb / "labels.yaml").read_text(encoding="utf-8")), (_rb / "theme.css").read_text(encoding="utf-8")
check("0.18.2 · this repository's labels.yaml is valid — every key a label — with no tagline (the claim speaks to agents; the Owner, 2026-09-24) and the English footer he ruled",
      set(_given) <= set(fm.LABELS) and "tagline" not in _given and _given.get("footer") == "A Pricke on the Wadden flats keeps the fleet in the channel." and _labels["footer"] == _given["footer"])
check("0.18.2 · this repository's theme.css loads as its own stylesheet with no warning — ink on ground set for light and dark and readable in both — and every font it names is on disk, with its licence",
      _src["theme.css"] == ["repository"] and not _warn and len(re.findall(r"--bg\s*:\s*#[0-9a-f]{6}", _css)) == len(re.findall(r"--ink\s*:\s*#[0-9a-f]{6}", _css)) == 2
      and "prefers-color-scheme:dark" in _css and all((_rb / u).is_file() for u in re.findall(r'url\("([^"]+)"\)', _css)) and "SIL Open Font License" in (_rb / "fonts/LICENSE.txt").read_text(encoding="utf-8"))
_wsrc = (_rb / "wordmark.svg").read_text(encoding="utf-8")
check("0.18.2 · this repository's wordmark is the site's mark at the ruled 16 px beside the name, in one ink: inlined, drawn in currentColor only, the mark's path the site's own",
      _src["wordmark"] == ["repository"] and _wm and 'height="16"' in _wm[1] and 'fill="currentColor"' in _wm[1] and not re.search(r'(?:fill|stroke)="(?!currentColor|none)', _wsrc)
      and re.search(r' d="([^"]+)"', (HERE / "overrides/.icons/shoalmark/pricke.svg").read_text(encoding="utf-8")).group(1) in _wsrc)
check("0.18.2 · R1–R5 · this repository's own wordmark.svg passes the grammar, as the file is", fm.inline_svg((_rb / "wordmark.svg").read_bytes())[1] == "" and _wm and _wm[1] == fm.inline_svg((_rb / "wordmark.svg").read_bytes())[0])
check("0.18.2 · this repository's logo — the tab's — is the site's tab icon, byte for byte", _src["logo"] == ["repository"] and (_rb / "logo.svg").read_bytes() == (HERE / "docs/assets/favicon.svg").read_bytes())

# --- R10: the German triage home an adopter copies before --init has the same way in, in the form a pass drops ------
with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    (root / "shoalmark.toml").write_text((HERE / "examples/de/shoalmark.toml").read_text(encoding="utf-8"), encoding="utf-8")
    (root / "docs/work-tracker").mkdir(parents=True)
    de_home = (HERE / "examples/de/TRIAGE.md").read_text(encoding="utf-8")
    (root / "docs/work-tracker/TRIAGE.md").write_text(de_home, encoding="utf-8")
    fm.configure(root); untouched = fm.triage_home()
    (root / "docs/work-tracker/TRIAGE.md").write_text(re.sub(r"- \*\*für\*\* — \*z\. B\. [^*]*\*", "- **für** — die Ausleihe unserer Bücherei", de_home), encoding="utf-8")
    one = fm.triage_home()["intent"]
fm.configure(HERE)
check("R10 · the German triage home carries the lead-in (the repository as a whole) and one example per line, in italics — a pass reads none of it, and one line of the Owner's as exactly that line",
      "über das Repository als Ganzes" in de_home and all(f"- **{w}** — *z. B. " in de_home for w in ("für", "damit", "niemals"))
      and all(x in de_home for x in (getattr(fm, "INTENT_NOTE_DE", "\0"), getattr(fm, "INTENT_LEAD_DE", "\0"), *getattr(fm, "INTENT_EXAMPLES_DE", ("\0",))))
      and untouched["intent"] == "" and untouched["path"] == "" and one == "- **für** — die Ausleihe unserer Bücherei")

# --- a repository in another language: the section names the GATE reads live in shoalmark.toml, not in a brand ---
with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp); subprocess.run(["git", "init", "-q", str(root)], check=True, env=_ENV)
    (root / "shoalmark.toml").write_text('name = "lager"\n[kinds]\nMSR = "Arbeit"\n[headings]\nstate = "Was jetzt gilt"\nwhy = "Warum"\ndone = "Fertig, wenn"\nlog = "Verlauf"\n'
                                         'intent = "Die Absicht"\npath = "Der aktuelle Weg"\npasses = "Durchgänge"\n', encoding="utf-8")
    run(root, "--init"); wt = root / "docs/work-tracker"
    run(root, "--new", "Mengen werden gerundet")
    made = next(wt.glob("MSR-001-*.md")); body = made.read_text(encoding="utf-8")
    home = (wt / "TRIAGE.md").read_text(encoding="utf-8")
    check("`[headings]` — `--new` and `--init` write the repository's own section names",
          all(f"## {h}\n" in body for h in ("Was jetzt gilt", "Warum", "Fertig, wenn", "Verlauf")) and "What is true now" not in body
          and all(f"## {h}\n" in home for h in ("Die Absicht", "Der aktuelle Weg", "Durchgänge")))
    made.write_text(body.replace("considered:", "considered: none").replace("## Fertig, wenn\n", "## Fertig, wenn\n\nEine Länge behält ihre Nachkommastellen.\n")
                    .replace("nothing is built.**", "nothing is built.** Gebucht wird gerundet."), encoding="utf-8")
    (wt / "TRIAGE.md").write_text(home.replace("1.\n", "1. MSR-001 zuerst, dann der Rest.\n").replace("*None yet.*", "**2026-09-21 — der erste Durchgang.** Alles gesichtet."), encoding="utf-8")
    for f_ in (made, wt / "TRIAGE.md"):                     # German whatever the templates wrote — this check is about READING
        x = f_.read_text(encoding="utf-8")
        for en, de in fm.DEFAULTS["headings"].items(): x = x.replace(f"## {de}\n", "## " + {"state": "Was jetzt gilt", "why": "Warum", "done": "Fertig, wenn", "log": "Verlauf", "intent": "Die Absicht", "path": "Der aktuelle Weg", "passes": "Durchgänge", "asks": "Fragen", "raised": "Einwände"}[en] + "\n")
        f_.write_text(x, encoding="utf-8")
    home = (wt / "TRIAGE.md").read_text(encoding="utf-8").replace("1. MSR-001 zuerst, dann der Rest.\n", "1.\n")
    fm.configure(root); now = made.read_text(encoding="utf-8"); th = fm.triage_home()
    check("`[headings]` — the gate and the pass READ them: a German tracker is stated and provable, a German TRIAGE.md gives its path and its newest pass",
          "Gebucht wird gerundet" in fm.current_truth(now) and "## Was jetzt gilt" in now and fm.DONE_RE.search("## Fertig, wenn") and not fm.DONE_RE.search("## Verlauf") and "MSR-001 zuerst" in th["path"] and th["last"].startswith("**2026-09-21") and not th["intent"])
    (wt / "TRIAGE.md").write_text(home.replace("## Der aktuelle Weg", "## The current path").replace("1.\n", "1. english heading still read.\n"), encoding="utf-8")
    check("`[headings]` — the English names stay understood, so a repository can change language a file at a time", "english heading still read" in fm.triage_home()["path"])
    (root / "shoalmark.toml").write_text('[headings]\nstaet = "x"\n', encoding="utf-8")
    try: fm.configure(root); refused = False
    except SystemExit as e: refused = "headings" in str(e)
    check("`[headings]` — a mistyped key is refused, naming them all", refused)
fm.configure(HERE)

# --- FM-004: what three outside agents found on their first twenty minutes --------------------------------------
with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp).resolve(); (root / "shoalmark.toml").write_text('name = "w"\n[kinds]\nAP = "Arbeit"\n[headings]\nstate = "Was jetzt gilt"\n', encoding="utf-8")
    code, out, _ = run(root, "--init")
    check("outside version control --init writes no .gitignore — and the contract names the repository's own heading, not the English one",
          not (root / ".gitignore").exists() and "*Was jetzt gilt*" in (root / "AGENTS.md").read_text() and "What is true now" not in (root / "AGENTS.md").read_text())
    code, _, _ = run(root, "--new", "AP-037", "Rechnung Teil 2"); taken = run(root, "--new", "ap-037", "noch einmal")
    run(root, "--new", "der nächste")
    names = sorted(p_.name[:6] for p_ in (root / "docs/work-tracker").glob("AP-*.md"))
    check("`--new KEY-037 title` takes a free id of the repository's choosing, refuses one that exists, and counting goes on after it", code == 0 and names == ["AP-037", "AP-038"] and taken[0] == fm.EXIT_LINT and "never reused" in taken[2])
    (root / "docs/work-tracker/TEMPLATE.md").write_text('---\nid: {id}\nstatus: Proposed\nconsidered:\nhook: "{title}"\n---\n\n# {id} — {title}\n\n## {state}\n\n**Angelegt am {today}; nichts ist gebaut.**\n\n## {done}\n', encoding="utf-8")
    run(root, "--new", "mit Hausvorlage"); made = next((root / "docs/work-tracker").glob("AP-039-*.md")).read_text()
    check("`<tracker dir>/TEMPLATE.md` is the template when there is one — a repository's language and sections, by convention", "Angelegt am" in made and "nothing is built" not in made and "## Was jetzt gilt" in made)
    for f_ in (root / "docs/work-tracker").glob("AP-03*.md"):
        f_.write_text(f_.read_text().replace("considered:\n", "considered: none\n" + ("next: owner\n" if "AP-037" in f_.name else "")).replace("status: Proposed", "status: In Progress" if "AP-038" in f_.name else "status: Proposed"))
    code, out, _ = run(root, "--next")
    check("--next answers before any pass has run: open work, work in progress first, whose move each is — and what waits for the Owner",
          code == 0 and "Nothing is ranked" in out and out.index("AP-038") < out.index("AP-037 ·") and "next: owner" in out
          and "NOTHING NEEDS THE OWNER" in out and "1 ASK(S) SENT BACK" in out and "not yet stated as a question" in out)
fm.configure(HERE)

# --- FM-005: the Owner's queue — every ask stated as the question it is, oldest first, with what it holds up --------
with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp).resolve(); (root / "shoalmark.toml").write_text('name = "q"\n[kinds]\nAP = "Work"\n', encoding="utf-8")
    old = (datetime.date.today() - datetime.timedelta(days=3)).isoformat(); new_ = (datetime.date.today() - datetime.timedelta(days=1)).isoformat()
    tracker(root, "AP-022", extra=f'next: owner\nask: "DATEV format, or a plain CSV?"\nask-kind: ruling\nask-since: {old}\nask-proposal: "DATEV"\n', title="export")
    tracker(root, "AP-021", extra=f'next: owner\nask: "Will you read the scraper log for instrument 27?"\nask-kind: action\nask-since: {new_}\nask-proposal: "read it before Friday"\n', title="model")
    tracker(root, "AP-020", extra="next: owner\n", title="buried in the body")
    tracker(root, "AP-037", status="Proposed", extra="blocked-by: AP-022\n", title="roles"); tracker(root, "AP-041", status="Proposed", extra="blocked-by: AP-037\n", title="audit")
    tracker(root, "AP-019", status="Shipped", extra='next: owner\nask: "done long ago"\n', title="shipped")
    code, out, _ = run(root, "--owner")
    check("--owner is the digest: how many need the Owner, the oldest ask's age, what is held up — transitively — and each ask as its question, oldest first; finished work never asks",
          code == 0 and out.startswith("2 NEED THE OWNER · oldest 3 day(s) · holding up 2: AP-037, AP-041") and out.index("AP-022 · ruling · asked 3 day(s) ago · holds up AP-037, AP-041") < out.index("AP-021 · action · asked 1 day(s) ago")
          and "DATEV format, or a plain CSV?" in out and "done long ago" not in out)
    # FM-008: an ask that is not a question he can answer is not shown to him AS one — it is sent back, with the reason,
    # for the seat that wrote it. `next: owner` and no `ask:` at all is the first of those.
    check("an ask that was never stated is sent back, not listed as a question — with the reason and the file to write it in",
          "AP-020" in out and "SENT BACK" in out and "not yet stated as a question" in out and "write `ask:` in AP-020-x.md" in out
          and out.index("2 NEED THE OWNER") < out.index("SENT BACK"))
    bad = tracker(root, "AP-050", extra="next: owner\nask-kind: favour\n", title="bad kind"); code, _, err = run(root)
    check("`ask-kind:` is one of four words — the gate refuses a fifth", code == fm.EXIT_LINT and "ask-kind" in err + _); bad.unlink()
    code, out2, _ = run(root, "--next")
    check("--next ends with the same digest — a cold session is told what its Owner owes before it starts", code == 0 and "2 NEED THE OWNER" in out2)
    tracker(root, "AP-030", extra=f'next: owner\nask: "Shall I open the pull request?"\nask-kind: ceremony\nask-since: {new_}\nask-proposal: "open it"\n', title="button")
    code, out3, _ = run(root, "--standup")
    check("--standup is the agenda of one sitting: rulings first, then the Owner's hands, then buttons — inside a kind what frees the most comes first — and what was sent back is named after, never as an item",
          code == 0 and out3.startswith("STANDUP") and out3.index("RULINGS") < out3.index("YOUR HANDS") < out3.index("BUTTONS") and "[frees AP-037, AP-041]" in out3
          and out3.index("BUTTONS") < out3.index("SENT BACK") and "AP-020" in out3.split("SENT BACK")[1])
    code, _, err = run(root, "--standup", str(root / "s.ics"))
    (root / "shoalmark.toml").write_text('name = "q"\nstandup = "09:00"\nstandup_minutes = 20\n[kinds]\nAP = "Work"\n', encoding="utf-8")
    code2, _, _ = run(root, "--standup", str(root / "s.ics")); ics = (root / "s.ics").read_bytes() if (root / "s.ics").exists() else b""
    check("--standup FILE.ics writes the recurring invite — weekdays, the configured time and length, CRLF as a calendar file must — and refuses until a time is configured",
          code == fm.EXIT_LINT and "standup = " in err and code2 == 0 and b"RRULE:FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR\r\n" in ics and b"T090000\r\n" in ics and b"T092000\r\n" in ics and ics.count(b"\n") == ics.count(b"\r\n"))
    for p_ in (root / "docs/work-tracker").glob("AP-0[23]0-*.md"):
        p_.unlink()                                      # AP-030 has been shown; AP-020 is malformed, and the gate refuses it — the answer checks below want a green ledger
    (root / "shoalmark.toml").write_text('name = "q"\n[kinds]\nAP = "Work"\n', encoding="utf-8")
    # the Owner answers: three lines in the ask's tracker, HIS OWN COMMIT — the ask leaves his queue, the seat sees it under --answered
    (root / "shoalmark.toml").write_text('name = "q"\nanswerers = ["holgo"]\n[kinds]\nAP = "Work"\n', encoding="utf-8")
    subprocess.run(["git", "init", "-q", str(root)], check=True, env=_ENV); git(root, "add", "-A"); git(root, "commit", "-qm", "before", "--author=seat <s@x>")
    ans = tracker(root, "AP-060", extra=f'next: owner\nask: "Move the merge to the Principal?"\nask-kind: ruling\nask-since: {old}\nanswer: "accepted — count one week first"\nanswered: {new_}\nanswered-by: holgo\n', title="answered")
    code, _, err = run(root)
    check("an answer that is not committed is refused — the commit is the record, the file is the label", code == fm.EXIT_LINT and "not committed yet" in err + _)
    code, out_, err = run(root, "--print-written")
    check("…but in the pre-commit run — --print-written — it is PENDING, not refused: the commit does not exist yet, and the Owner's first answer must be committable", code == 0 and "being committed now" in err and "not committed yet" not in err)
    ans.write_text(ans.read_text().replace("answered-by: holgo\n", "answered-by: <you>\n"), encoding="utf-8")
    git(root, "config", "user.name", "holgo"); fm.configure(root)
    check("`answered-by: <you>` — or left empty — is filled from git config user.name; the Owner types no name", next(t_ for t_ in fm.load_trackers() if t_["id"] == "AP-060")["answered_by"] == "holgo")
    ans.write_text(ans.read_text().replace("answered-by: <you>\n", "answered-by: holgo\n"), encoding="utf-8")
    git(root, "add", "-A"); git(root, "commit", "-qm", "seat forges an answer", "--author=seat <s@x>"); code, _, err = run(root)
    check("an answer committed by someone other than `answered-by:` is refused — the pre-mortem's rule, checked against the version control system", code == fm.EXIT_LINT and "author of the answer is `seat`" in err + _)
    git(root, "commit", "-q", "--amend", "--no-edit", "--author=holgo <h@x>"); code, out4, _ = run(root); q_ = run(root, "--owner")[1]; a_ = run(root, "--answered")[1]
    check("an answer committed by the answerer passes: the ask leaves the Owner's queue and appears under --answered, with the question, the answer and who answered",
          code == 0 and "AP-060" not in q_ and "1 ANSWERED, NOT YET ACTED ON" in a_ and "answer: accepted — count one week first" in a_ and "by holgo" in a_)
    # `signed`: a git author is a string; the commit must VERIFY. A throwaway SSH key, trusted by the repository alone.
    (root / "shoalmark.toml").write_text('name = "q"\nanswerers = ["holgo signed"]\n[kinds]\nAP = "Work"\n', encoding="utf-8")
    code, _, err = run(root)
    check("`answerers = [\"holgo signed\"]`: an unsigned answer is refused even though its author string is right — a git author is only a string", code == fm.EXIT_LINT and "does not verify" in err + _)
    key = root / "k"; subprocess.run(["ssh-keygen", "-q", "-t", "ed25519", "-N", "", "-f", str(key)], check=True, capture_output=True)
    (root / "signers").write_text("h@x " + key.with_suffix(".pub").read_text(), encoding="utf-8")
    git(root, "config", "gpg.format", "ssh"); git(root, "config", "user.signingkey", str(key)); git(root, "config", "gpg.ssh.allowedSignersFile", str(root / "signers"))
    git(root, "commit", "-q", "--amend", "--no-edit", "-S", "--author=holgo <h@x>"); code, _, err = run(root)
    check("a signed answer under a key the repository trusts verifies and passes", code == 0 and "does not verify" not in err)
    git(root, "commit", "-q", "--amend", "--no-edit", "-S", "--author=holgo <other@x>"); code, _, err = run(root)
    check("signed by the key, but as an identity the signers file does not tie to it — refused: the key and the name must agree", code == fm.EXIT_LINT and "does not verify" in err + _)
    git(root, "commit", "-q", "--amend", "--no-edit", "-S", "--author=holgo <h@x>")
    (root / "shoalmark.toml").write_text('name = "q"\nanswerers = ["holgo"]\n[kinds]\nAP = "Work"\n', encoding="utf-8")
    ans.write_text(ans.read_text().replace("answered-by: holgo\n", "answered-by: intruder\n"), encoding="utf-8"); code, _, err = run(root)
    check("an answerer not on the `answerers` list is refused, whoever committed", code == fm.EXIT_LINT and "not in `answerers`" in err + _)
    (root / "shoalmark.toml").write_text('name = "q"\n[kinds]\nAP = "Work"\n', encoding="utf-8"); code, _, err = run(root)
    check("with no `answerers` named, every answer is refused with that message — nobody answers by default", code == fm.EXIT_LINT and "names nobody" in err + _)
    ans.write_text(ans.read_text().replace("answered-by: intruder\n", ""), encoding="utf-8"); (root / "shoalmark.toml").write_text('name = "q"\nanswerers = ["holgo"]\n[kinds]\nAP = "Work"\n', encoding="utf-8"); code, _, err = run(root)
    check("an answer is three lines — one missing and the gate says so", code == fm.EXIT_LINT and "an answer is three lines" in err + _)
    ans.write_text(ans.read_text().replace('ask: "Move the merge to the Principal?"\n', "") + "answered-by: holgo\n", encoding="utf-8"); code, _, err = run(root)
    check("an answer with no question is refused", code == fm.EXIT_LINT and "`answer:` with no `ask:`" in err + _); ans.unlink(); rm_git(root)
    (root / "shoalmark.toml").write_text('name = "q"\n[kinds]\nAP = "Work"\n', encoding="utf-8")
    tracker(root, "AP-020", extra="next: owner\n", title="buried in the body")      # back for the board: what a malformed ask looks like to the Owner
    run(root); page = (root / "docs/work-tracker/index.html").read_text()
    if _CHROME:
        dom = subprocess.run([_CHROME, "--headless=new", "--disable-gpu", *_CHROME_FLAGS, "--virtual-time-budget=4000", "--dump-dom", (root / "docs/work-tracker/index.html").as_uri()], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60).stdout
        shown = re.sub(r"\s+", " ", re.sub(r"<(script|style)[\s\S]*?</\1>|<[^>]+>", " ", dom))
        check("rendered: the board's first words are the answer — how many wait, the oldest, what is held up — then each question, the oldest first, before the path and before any table",
              "waiting for you: 2 · oldest 3 days · holding up 2 more" in shown and shown.index("DATEV format, or a plain CSV?") < shown.index("read the scraper log") and "not yet stated as a question" in shown
              and "a ruling" in shown and "your hands" in shown and "holds up AP-037, AP-041" in shown and shown.index("waiting for you") < shown.index("AP-022 ") )
        check("what is not a question he can answer is shown apart — `N asks sent back — not for you`, with the reason, after the queue and never as a question",
              "1 asks sent back — not for you" in shown and shown.index("AP-022 ") < shown.index("asks sent back") < shown.index("AP-020")
              and "write `ask:` in AP-020-x.md" in shown)
        check("each stated ask carries two actions — accept · reject — and a dialog that shows the ask, its proposal and its context before anything is decided; an unstated one carries none",
              dom.count('>accept</button>') == 2 and dom.count('>reject</button>') == 2 and "ACT(T.find(x=>x[0]=='AP-020')" not in dom and '<dialog id="dlg">' in dom and 'name="how" value="${i}" required' in page and 'value="other" required' in page and '--answer ${id} ${kind}' in page)
        # the dialog's head is one line of ` · `-separated parts: the id ran straight into its first mark ("AP-022 a ruling"),
        # and an ask with no kind, no age and holding nothing left a dangling separator behind the id
        check("the dialog's head separates the id from its marks the way the rest of the line is separated, and carries none when there are no marks",
              '<a href="#=${id}">${id}</a>${meta?` · <span class="m">${meta}</span>`:""}</h3>' in page)
fm.configure(HERE)

# --- FM-007: an ask offers CHOICES — one radio each, the recommended one first, Other last -------------------------
with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp).resolve()
    (root / "shoalmark.toml").write_text('name = "q"\n[kinds]\nAP = "Work"\n', encoding="utf-8")
    tracker(root, "AP-080", extra=f'next: owner\nask: "Welches Format?"\nask-kind: ruling\nask-since: {old}\nask-options: "a | b | c"\nask-proposal: "b"\n', title="three choices")
    tracker(root, "AP-081", extra=f'next: owner\nask: "Move the merge?"\nask-kind: ruling\nask-since: {old}\nask-proposal: "count one week first"\n', title="one recommendation")
    # a DRAFT: an `ask:` with `next: review` — any seat may write one, it needs no recommendation, and the Owner never sees it
    tracker(root, "AP-082", extra=f'next: review\nask: "What should it say?"\nask-since: {old}\n', title="no choices at all")
    code, _, err = run(root)
    check("an ask may name its choices: `ask-options:` is one line, and a proposal that is one of them passes the gate", code == 0)
    check("a DRAFT — an `ask:` with `next: review` — needs no recommendation and never enters the Owner's queue: the Principal turns it into an ask",
          "AP-082" not in run(root, "--owner")[1] and "AP-082" not in run(root, "--standup")[1] and [t_["id"] for t_, _a, _h in fm.owner_queue(fm.load_trackers())] == ["AP-080", "AP-081"])
    if _CHROME:
        page = (root / "docs/work-tracker/index.html").read_text(encoding="utf-8")
        def _rows(tid, then=""):
            """the dialog's radio rows, in order, as the Owner reads them — opened in the browser, not inferred."""
            p_ = root / "docs/work-tracker" / f"dlg-{tid}.html"
            p_.write_text(page + f'<script>setTimeout(()=>{{ACT(T.find(x=>x[0]=="{tid}"),"accept");{then}}},50)</script>', encoding="utf-8")
            d_ = subprocess.run([_CHROME, "--headless=new", "--disable-gpu", *_CHROME_FLAGS, "--virtual-time-budget=4000", "--dump-dom", p_.as_uri()],
                                capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60).stdout
            p_.unlink()
            body = d_.split('<dialog id="dlg"')[1].split("</dialog>")[0]      # the rendered dialog only — the script below it carries the same template
            return [re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", m)).strip() for m in re.findall(r'<label class="dl">(.*?)</label>', body, re.S)], body
        r80, _b80 = _rows("AP-080")
        check("the choices are radios in the order given, except the recommended one — it is offered FIRST and marked — and Other comes last",
              r80 == ["b — recommended", "a", "c", "Other:"])
        r81, _b81 = _rows("AP-081")
        check("a proposal with no options named is a list of one: the recommendation, then Other", r81 == ["count one week first — recommended", "Other:"])
        r82, b82 = _rows("AP-082")
        other_, box_ = re.search(r'<input [^>]*value="other"[^>]*>', b82).group(0), re.search(r"<textarea[^>]*>", b82).group(0)
        check("an ask that offers nothing shows only Other, checked, and its box is the answer — required, not disabled",
              r82 == ["Other:"] and "checked" in other_ and "required" in box_ and "disabled" not in box_)
        # OK yields ONE command, and what the Owner picked is what the tracker will record — the option's own words
        _pick = 'const D=document.getElementById("dlg"),R=D.querySelectorAll("[name=how]")[2];R.checked=true;R.dispatchEvent(new Event("change"));D.querySelector("button.go").click();'
        _, b83 = _rows("AP-080", _pick)
        check("OK gives one command carrying the chosen option VERBATIM — not an index, not the recommendation",
              '--answer AP-080 accept "c"' in re.sub(r"<[^>]+>", "", b83))
    (root / "docs/work-tracker/AP-080-x.md").write_text((root / "docs/work-tracker/AP-080-x.md").read_text(encoding="utf-8").replace('ask-proposal: "b"', 'ask-proposal: "z"'), encoding="utf-8")
    code, _, err = run(root)
    check("a recommendation that is not one of the options is refused — the Owner is never shown a recommendation he cannot pick",
          code == fm.EXIT_LINT and "AP-080: `ask-proposal:` recommends 'z'" in err + _ and "a | b | c" in err + _)
fm.configure(HERE)

# --- FM-013: after OK, a second screen — how to sign it, where, what it does, the end, the check, and one way out ------
# OK used to disable itself and leave one enabled button, abort, which read as taking the decision back; and it said
# *Copied* whether or not anything was. The Owner: "Only a "Done" button to close the dialog."
with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp).resolve()
    subprocess.run(["git", "init", "-q", str(root)], check=True, env=_ENV); git(root, "checkout", "-q", "-b", "fix/ap-090")
    (root / "shoalmark.toml").write_text('name = "q"\n[kinds]\nAP = "Work"\n', encoding="utf-8")
    tracker(root, "AP-090", extra=f'next: owner\nask: "Welches Format?"\nask-kind: ruling\nask-since: {old}\nask-options: "a | b | c"\nask-proposal: "b"\n', title="three choices")
    run(root); page = (root / "docs/work-tracker/index.html").read_text(encoding="utf-8")
    two_ = page.split("const sign=")[1].split('d.querySelector(".copy")')[0]
    menus_ = re.findall(r"<menu>(.*?)</menu>", two_)
    check("FM-013 · the built board carries the second screen: its words in the labels, the branch the board was built from, and exactly one button in its menu — Done",
          '"answer.sign.title": "Sign your answer"' in page and 'BRANCH="fix/ap-090",T=[' in page and len(menus_) == 1 and menus_[0].count("<button") == 1
          and 'value="done"' in menus_[0] and 'l("answer.done")' in menus_[0] and all(f'"{k}"' in page for k in fm.LABELS if k.startswith("answer.sign.")))
    check("FM-013 · what the second screen replaced is gone — no disabled OK, no `answer.run` line that said Copied before anything was",
          '"answer.run"' not in page and ".disabled=true" not in page and "answer.run" not in fm.LABELS)
    if _CHROME:
        def _sign(clip):
            """OK pressed in the browser, the second screen read as rendered — with the clipboard there, or with none."""
            stub = {"yes": 'Object.defineProperty(navigator,"clipboard",{value:{writeText:()=>Promise.resolve()}});',
                    "none": 'Object.defineProperty(navigator,"clipboard",{value:undefined});'}[clip]
            go = ('const D=document.getElementById("dlg"),R=D.querySelectorAll("[name=how]")[0];R.checked=true;R.dispatchEvent(new Event("change"));'
                  'D.querySelector("button.go").click();setTimeout(()=>{const B=document.body.dataset;B.menu=[...D.querySelectorAll("menu button")].map(b=>b.textContent).join("|");'
                  'B.said=D.querySelector(".said").textContent;B.buttons=D.querySelectorAll("button").length;D.querySelector("menu button").click();B.open=String(D.open)},300);')
            p_ = root / "docs/work-tracker" / f"s2-{clip}.html"
            p_.write_text(page + f'<script>{stub}setTimeout(()=>{{ACT(T.find(x=>x[0]=="AP-090"),"accept");{go}}},50)</script>', encoding="utf-8")
            d_ = subprocess.run([_CHROME, "--headless=new", "--disable-gpu", *_CHROME_FLAGS, "--virtual-time-budget=4000", "--dump-dom", p_.as_uri()],
                                capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60).stdout
            p_.unlink()
            body = d_.split('<dialog id="dlg"')[1].split("</dialog>")[0]
            said = {k: (re.search(rf'data-{k}="([^"]*)"', d_) or [None, None])[1] for k in ("menu", "said", "buttons", "open")}
            return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", body)), body, said
        s2_, b2_, yes_ = _sign("yes")
        check("FM-013 · OK opens the second screen, as rendered: the heading, the command in a monospace block, where to run it — naming the branch — what it does step by step, that it prints each step, what success looks like, how to check it, where to go when it fails",
              "Sign your answer" in s2_ and re.search(r'<pre class="cmd">[^<]*--answer AP-090 accept "b"</pre>', b2_) is not None and "Copy again" in s2_
              and "In a terminal, in this repository, on the branch that carries the ask — fix/ap-090, the branch this board was built from." in s2_
              and "cuts answer/ap-090 from the branch you are on" in s2_ and "writes the three lines — answer: answered: answered-by:" in s2_
              and "commits them, signed with your key" in s2_ and "pushes the branch" in s2_ and "It prints each step as it starts" in s2_
              and "AP-090 answered: accepted - b signed, on `answer/ap-090`, pushed" in s2_ and "git log -1 --format=%G? answer/ap-090 prints G" in s2_
              and f'href="{fm.SIGNING_PAGE}"' in b2_ and "give me the command" not in s2_ and "abort" not in s2_)
        check(f"FM-013 · …with ONE way out — Done, the only button in its menu, closes the dialog; the only other control is Copy again (saw: {yes_})",
              yes_["menu"] == "Done" and yes_["buttons"] == "2" and yes_["open"] == "false")
        _n0, _n1, none_ = _sign("none")
        check("FM-013 · it says Copied only when the clipboard said so — with no clipboard (a board opened from a file), it says to select and copy instead",
              yes_["said"] == "Copied." and none_["said"] == fm.LABELS["answer.sign.nocopy"] and "Copied" not in none_["said"])
    rm_git(root)
fm.configure(HERE)

# --- FM-007: the Owner's one command — --answer cuts the branch, writes, signs, pushes ------------------------------
with tempfile.TemporaryDirectory() as tmp:
    base = Path(tmp).resolve(); root = base / "wc"; root.mkdir()
    subprocess.run(["git", "init", "-q", "--bare", str(base / "origin.git")], check=True, env=_ENV); subprocess.run(["git", "init", "-q", str(root)], check=True, env=_ENV)
    key = base / "k"; subprocess.run(["ssh-keygen", "-q", "-t", "ed25519", "-N", "", "-f", str(key)], check=True, capture_output=True)
    (root / "signers").write_text("h@x " + key.with_suffix(".pub").read_text(), encoding="utf-8")
    for k_, v_ in (("user.name", "holgo"), ("user.email", "h@x"), ("gpg.format", "ssh"), ("user.signingkey", str(key)), ("gpg.ssh.allowedSignersFile", str(root / "signers")), ("commit.gpgsign", "false")):
        git(root, "config", k_, v_)
    git(root, "remote", "add", "origin", str(base / "origin.git"))
    (root / "shoalmark.toml").write_text('name = "q"\nanswerers = ["holgo signed"]\n[kinds]\nAP = "Work"\n', encoding="utf-8")
    # the tracker discusses its own keys, as FM-007 itself does: "an `answer:` counts only from the account it is filed
    # from" is the sentence the pre-mortem's rule is written in, and it sits in the body of the very tracker it governs
    ap70_ = tracker(root, "AP-070", extra=f'next: owner\nask: "Move the merge to the Principal?"\nask-kind: ruling\nask-since: {old}\nask-proposal: "count one week first"\n', title="the ask",
                    body="## What is true now\n\n**One thing is left.**\n\nAn `answer:` counts only from the account it is filed from.\n\n## Done when\n\nit is.\n")
    tracker(root, "AP-071", extra="next: build\n", title="asks nothing")
    for id_, q_ in (("AP-072", "Move the merge?"), ("AP-073", "Move the release?")):
        tracker(root, id_, extra=f'next: owner\nask: "{q_}"\nask-kind: ruling\nask-since: {old}\nask-proposal: "wait a week"\n', title="another ask")
    run(root); git(root, "add", "-A"); git(root, "commit", "-qm", "the ask", "--author=seat <s@x>"); git(root, "push", "-q", "-u", "origin", "HEAD:pd/070")
    code, _, err = run(root, "--answer", "AP-071", "accept")
    check("--answer refuses a tracker that asks the Owner nothing", code == fm.EXIT_LINT and "asks the Owner nothing" in err)
    code, _, err = run(root, "--answer", "AP-070", "reject")
    check("--answer refuses a rejection without its reason", code == fm.EXIT_LINT and "carries its reason" in err)
    (root / "dirty.txt").write_text("x"); git(root, "add", "dirty.txt"); code, _, err = run(root, "--answer", "AP-070", "accept"); git(root, "rm", "-q", "-f", "dirty.txt")
    check("--answer refuses a dirty tree — an answer is one commit with nothing else in it", code == fm.EXIT_LINT and "working tree has changes" in err)
    start_ = subprocess.run(["git", "-C", str(root), "branch", "--show-current"], capture_output=True, text=True, env=_ENV).stdout.strip()
    code, out, err = run(root, "--answer", "AP-070", "accept", "count one week first")
    # FM-012: silent until its last line, the command was stopped by an Owner who took it for hung. Each step is said as
    # it STARTS — the waits are the checkout hook and the pre-commit gate, and both come after the line that names them
    steps_ = [err.find(s) for s in ("answering AP-070 — 1/4 reading the trackers …", f"answering AP-070 — 2/4 cutting `answer/ap-070` from `{start_}`",
                                    "answering AP-070 — 3/4 committing, signed", "answering AP-070 — 4/4 pushing to `origin` …")]
    check("FM-012 · --answer names each step as it starts, in order — reading the trackers · cutting answer/<id> from the branch it is on · committing, signed · pushing — and its last lines are unchanged",
          -1 not in steps_ and steps_ == sorted(steps_) and out.startswith("AP-070 answered: accepted - count one week first\n  signed, on `answer/ap-070`, pushed\n"))
    on = subprocess.run(["git", "-C", str(root), "branch", "--show-current"], capture_output=True, text=True, env=_ENV).stdout.strip()
    remote = subprocess.run(["git", "-C", str(base / "origin.git"), "branch"], capture_output=True, text=True, env=_ENV).stdout
    git(root, "switch", "-q", "answer/ap-070"); sig = subprocess.run(["git", "-C", str(root), "log", "-1", "--format=%G? %GS %an %s"], capture_output=True, text=True, env=_ENV).stdout.strip()
    fm.configure(root); t_ = next(t for t in fm.load_trackers() if t["id"] == "AP-070")
    check("--answer accept with a change: cuts answer/<id> from the ask's branch, writes the three lines, commits SIGNED under the answerer, pushes — the ask has left the queue — and goes back to the branch it started on",
          code == 0 and on == start_ and f"\n  back on `{start_}`" in out and sig.startswith("G h@x holgo AP-070: accepted - count one week first") and "answer/ap-070" in remote
          and t_["answer"] == "accepted - count one week first" and t_["answered_by"] == "holgo" and "AP-070" not in run(root, "--owner")[1] and run(root, "--check")[0] == 0)
    # and the body keeps being written after the answer lands, by a seat that is not the answerer and does not sign:
    # by substring that commit becomes the author of the answer, and the gate refuses the Owner's own signed answer
    ap70_.write_text(ap70_.read_text() + "\nAnd an `answer:` is one line — `answered-by:` is the label, the commit is the record.\n", encoding="utf-8")
    git(root, "add", "-A"); git(root, "commit", "-qm", "the body, edited by a seat", "--author=seat <s@x>")
    code2_, _o2, err2_ = run(root, "--check")
    check("the answer still verifies after another seat commits a sentence about `answer:` into the same tracker — a signed answer is not unsigned by prose written around it",
          code2_ == 0 and "does not verify" not in err2_ and "the git author of the answer" not in err2_)
    code, _, err = run(root, "--answer", "AP-070", "reject", "no")
    check("an answer is never overwritten — a second --answer on the same ask is refused", code == fm.EXIT_LINT and "answered already" in err)
    # the answer is ONE front-matter line: a newline in the text closes it, and the fragment after it is read as another
    # key — `status: Shipped` in a rejection silently shipped the tracker, and the answer itself parsed off
    git(root, "switch", "-q", "pd/070"); code, _, err = run(root, "--answer", "AP-072", "reject", "no\nstatus: Shipped\n\nand why")
    git(root, "switch", "-q", "answer/ap-072"); fm.configure(root); t_ = next(t for t in fm.load_trackers() if t["id"] == "AP-072")
    check("an answer is ONE line: a newline in the text would be read as the next front-matter key — every run of whitespace collapses to one space",
          code == 0 and t_["answer"] == "rejected - no status: Shipped and why" and t_["status"] == "In Progress" and run(root, "--check")[0] == 0)
    # `answered-by:` is `user.name`; the commit's author is what git will actually write, and the environment overrides
    # the configuration. The gate reads the author, so the two disagreeing is an answer filed from an account that did not give it
    git(root, "switch", "-q", "pd/070")
    code, _, err = run(root, "--answer", "AP-073", "accept", git_env={"GIT_AUTHOR_NAME": "mallory"})
    check("the environment's author disagreeing with `answered-by:` is refused before anything is touched — no branch cut",
          code == fm.EXIT_LINT and "would author this commit as `mallory`" in err
          and subprocess.run(["git", "-C", str(root), "branch", "--show-current"], capture_output=True, text=True, env=_ENV).stdout.strip() == "pd/070")
    # a good signature under a trusted key still says nothing about whose name is on the commit: the gate asks that the
    # principal the key is trusted FOR is the author's email, and so must the command — or it pushes what the gate refuses
    (base / "other").write_text("other@x " + key.with_suffix(".pub").read_text(), encoding="utf-8")
    git(root, "config", "gpg.ssh.allowedSignersFile", str(base / "other")); code, _, err = run(root, "--answer", "AP-073", "accept")
    git(root, "config", "gpg.ssh.allowedSignersFile", str(root / "signers"))
    check("a signature trusted for someone else does not verify as the answerer — the gate's own rule, and the answer is NOT pushed",
          code == fm.EXIT_LINT and "does not verify as `holgo`" in err
          and "answer/ap-073" not in subprocess.run(["git", "-C", str(base / "origin.git"), "branch"], capture_output=True, text=True, env=_ENV).stdout)
    git(root, "switch", "-q", "pd/070"); git(root, "config", "--unset", "user.signingkey"); code, _, err = run(root, "--answer", "AP-070", "accept")
    check("--answer refuses before touching anything when it cannot end in a verified answer — no signing key, no branch cut", code == fm.EXIT_LINT and "no `user.signingkey`" in err
          and subprocess.run(["git", "-C", str(root), "branch", "--show-current"], capture_output=True, text=True, env=_ENV).stdout.strip() == "pd/070")
    rm_git(root)
fm.configure(HERE)

# --- FM-012: reading the trackers asks git who is typing only where an answer needs the name, and at most once -------
# `answered-by:` empty or `<you>` is filled from `git config user.name` — and the test was *the key is empty*, true of
# every tracker with no answer at all. One git process per tracker: 504 of them, 15.2 s of a 16.8 s load, on a
# 505-tracker corpus, and `--answer` reads the corpus about four times.
with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp).resolve()
    subprocess.run(["git", "init", "-q", str(root)], check=True, env=_ENV); git(root, "config", "user.name", "holgo")
    (root / "shoalmark.toml").write_text('name = "l"\n[kinds]\nAP = "Work"\n', encoding="utf-8")
    for n_ in range(500, 520):
        tracker(root, f"AP-{n_}", title="asks nothing")
    asked_ = lambda: sum(1 for c in argv_of(fm.load_trackers) if c[:3] == ["git", "config", "user.name"])
    fm.configure(root); none_ = asked_(); ts0_ = {t_["id"]: t_ for t_ in fm.load_trackers()}
    for n_ in (520, 521, 522):
        tracker(root, f"AP-{n_}", extra=f'next: owner\nask: "Shall {n_} ship?"\nask-kind: ruling\nask-since: {old}\nask-proposal: "ship it"\n'
                                          f'answer: "accepted"\nanswered: {new_}\nanswered-by: <you>\n', title="answered by hand")
    fm.configure(root); several_ = asked_(); ts_ = {t_["id"]: t_ for t_ in fm.load_trackers()}
    check("FM-012 · a load where no tracker carries an answer asks git for no name — it asked once per tracker",
          none_ == 0 and ts0_["AP-500"]["answered_by"] == "")
    check("FM-012 · a load with three `answered-by: <you>` asks git once, and fills all three",
          several_ == 1 and all(ts_[f"AP-{n_}"]["answered_by"] == "holgo" for n_ in (520, 521, 522)) and ts_["AP-500"]["answered_by"] == "")
    rm_git(root)
fm.configure(HERE)

# --- FM-017: a failed --answer leaves nothing behind — and a leftover from one is named, with the command that undoes it -
# What the Owner met: the gate refused the commit, and the run returned with his answer staged, INDEX.md rewritten by the
# hook and an empty `answer/<id>` checked out. His next `--answer`, on another ask, said only "the working tree has changes".
with tempfile.TemporaryDirectory() as tmp:
    base = Path(tmp).resolve(); root = base / "wc"; root.mkdir()
    subprocess.run(["git", "init", "-q", "--bare", str(base / "origin.git")], check=True, env=_ENV); subprocess.run(["git", "init", "-q", str(root)], check=True, env=_ENV)
    for k_, v_ in (("user.name", "holgo"), ("user.email", "h@x"), ("commit.gpgsign", "false"), ("core.hooksPath", str(root / ".git" / "hooks"))):
        git(root, "config", k_, v_)
    git(root, "remote", "add", "origin", str(base / "origin.git"))
    (root / "shoalmark.toml").write_text('name = "f"\n[kinds]\nAP = "Work"\n[seats]\nowner = "h@x"\n', encoding="utf-8")
    for id_, q_ in (("AP-500", "Shall the launcher ship first?"), ("AP-501", "Shall the importer ship first?")):
        tracker(root, id_, extra=f'next: owner\nask: "{q_}"\nask-kind: ruling\nask-since: {old}\nask-proposal: "yes"\n', title="an ask")
    (root / "notes.txt").write_text("the Owner's own file\n", encoding="utf-8")
    run(root); git(root, "add", "-A"); git(root, "commit", "-qm", "the asks", "--author=holgo <h@x>")
    sh_ = lambda *a: subprocess.run(["git", "-C", str(root), *a], capture_output=True, text=True, encoding="utf-8", errors="replace", env=_ENV).stdout.strip()
    start_ = sh_("branch", "--show-current")
    hook_ = root / ".git" / "hooks" / "pre-commit"; hook_.parent.mkdir(parents=True, exist_ok=True)
    hook_.write_bytes(b'#!/bin/sh\necho "regenerated by the hook" >> docs/work-tracker/INDEX.md\necho "gate: AP-500 refused - the reason the Owner must read" >&2\nexit 1\n')
    hook_.chmod(0o755)
    code, out, err = run(root, "--answer", "AP-500", "accept", "count one week first")
    check("FM-017 · a commit the gate refuses leaves NOTHING behind: the tree is clean — the tracker and the INDEX.md the hook rewrote restored — the run is back on the branch it started on, and the answer/<id> it cut is gone",
          code == fm.EXIT_LINT and sh_("status", "--porcelain", "--untracked-files=no") == "" and sh_("branch", "--show-current") == start_
          and sh_("branch", "--list", "answer/ap-500") == "" and "answer:" not in (root / "docs/work-tracker/AP-500-x.md").read_text().split("---")[1]
          and "restored docs/work-tracker/AP-500-x.md, docs/work-tracker/INDEX.md" in err and "`answer/ap-500` deleted" in err)
    check("FM-017 · …and it says what refused it — the hook's own words, not git's last line — and the answer, with the command that gives it again: no answer is lost",
          "gate: AP-500 refused - the reason the Owner must read" in err and "your answer, not lost: accepted - count one week first" in err
          and 'to give it again: ' in err and '--answer AP-500 accept "count one week first"' in err)
    # the leftover 0.17.3 left: the answer staged, INDEX.md rewritten — and a file of the Owner's own changed beside them
    p5_ = root / "docs/work-tracker/AP-500-x.md"
    p5_.write_text(p5_.read_text().replace('ask-proposal: "yes"\n', f'ask-proposal: "yes"\nanswer: "accepted - count one week first"\nanswered: {new_}\nanswered-by: holgo\n'), encoding="utf-8")
    git(root, "add", str(p5_)); (root / "docs/work-tracker/INDEX.md").write_text((root / "docs/work-tracker/INDEX.md").read_text() + "x\n", encoding="utf-8")
    (root / "notes.txt").write_text("the Owner's own change\n", encoding="utf-8")
    code, out, err = run(root, "--answer", "AP-501", "accept")
    undo_ = "git restore --staged --worktree -- docs/work-tracker/AP-500-x.md docs/work-tracker/INDEX.md"
    check("FM-017 · the dirty-tree refusal names the paths — and a tracker carrying an answer that was never committed is called what it looks like, a failed earlier `--answer`, with ONE command that undoes it and the answer to give again",
          code == fm.EXIT_LINT and "working tree has changes" in err and all(p_ in err.split("Changed:")[1].split("\n")[0] for p_ in ("docs/work-tracker/AP-500-x.md", "docs/work-tracker/INDEX.md", "notes.txt"))
          and "AP-500 carries an answer that was never committed" in err and "failed half-way" in err and undo_ in err
          and '--answer AP-500 accept "count one week first"' in err and "commit or stash it: notes.txt" in err)
    subprocess.run(undo_.split()[:1] + ["-C", str(root)] + undo_.split()[1:], check=True, capture_output=True, env=_ENV)
    check("FM-017 · the command it gives undoes exactly what the tool left — the Owner's own change stays", sh_("status", "--porcelain", "--untracked-files=no") == "M notes.txt")
    rm_git(root)
fm.configure(HERE)

# --- FM-008: an ask reaches the Owner only through the gate — form, no duplicate, the bottleneck ---------------------
with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp).resolve()
    (root / "shoalmark.toml").write_text('name = "g"\n[kinds]\nAP = "Work"\n', encoding="utf-8")
    ask_ = lambda tid, q, extra="", move="owner": tracker(root, tid, extra=f'next: {move}\nask: "{q}"\nask-kind: ruling\nask-since: {old}\nask-proposal: "wait a week"\n{extra}', title="an ask")
    gone = lambda *ids: [p_.unlink() for id_ in ids for p_ in (root / "docs/work-tracker").glob(f"{id_}-*.md")]
    bad = tracker(root, "AP-101", extra=f'next: owner\nask: "Shall we ship on Friday?"\nask-kind: ruling\nask-since: {old}\n', title="no recommendation")
    code, _, err = run(root)
    check("1 · an ask with no recommendation is refused, naming the id and the key that is missing — the seat that asks has already done the thinking",
          code == fm.EXIT_LINT and "AP-101: `next: owner` without `ask-proposal:`" in err and "moves the decision and none of the work" in err)
    bad.write_text(bad.read_text().replace(f"ask-since: {old}\n", ""), encoding="utf-8"); code, _, err = run(root)
    check("1 · all three lines are named at once — an agent told one key at a time comes back three times",
          code == fm.EXIT_LINT and "`ask-since:`" in err and "`ask-proposal:`" in err and err.count("AP-101: `next: owner` without") == 1)
    gone("AP-101")
    two = ask_("AP-102", "Do we ship on Friday, or do we wait? Say which.")
    code, _, err = run(root)
    check("2 · one question: an ask with two of them, or with prose after the question mark, is refused — a paragraph gets one answer",
          code == fm.EXIT_LINT and "AP-102: `ask:` is ONE question" in err and "exactly one `?`, at the end" in err)
    two.write_text(two.read_text().replace("Do we ship on Friday, or do we wait? Say which.", "A" * fm.ASK_MAX + "?"), encoding="utf-8")
    code, _, err = run(root)
    check(f"2 · an ask longer than {fm.ASK_MAX} characters is refused — what he answers in a sitting is a sentence, not a briefing",
          code == fm.EXIT_LINT and f"`ask:` is {fm.ASK_MAX + 1} characters" in err)
    gone("AP-102")
    opts = ask_("AP-103", "Which one?", extra='ask-options: "a | b | c | d | e | f"\n')
    code, _, err = run(root)
    check("2 · more than five choices is refused — past a radio list the Owner reads once, it is a design review, not a question",
          code == fm.EXIT_LINT and "AP-103: `ask-options:` offers 6 choices" in err)
    opts.write_text(opts.read_text().replace("a | b | c | d | e | f", "wait a week | " + "z" * (fm.ASK_OPTION_MAX + 1)), encoding="utf-8")
    code, _, err = run(root)
    check(f"2 · a choice longer than {fm.ASK_OPTION_MAX} characters is refused — a choice is a phrase; its rationale is the proposal's",
          code == fm.EXIT_LINT and f"is {fm.ASK_OPTION_MAX + 1} characters" in err)
    opts.write_text(opts.read_text().replace("wait a week | " + "z" * (fm.ASK_OPTION_MAX + 1), "wait a week | ship | wait a week"), encoding="utf-8")
    code, _, err = run(root)
    check("2 · the same choice offered twice is refused — a radio list with one option written twice cannot be picked from",
          code == fm.EXIT_LINT and "AP-103: `ask-options:` names 'wait a week' twice" in err)
    gone("AP-103")
    ask_("AP-104", "Shall the launcher ship first?")
    dup = ask_("AP-105", "shall the launcher   ship first")
    code, _, err = run(root)
    check("3 · the same question filed twice is refused, naming the other tracker — normalised by case, spacing and trailing punctuation, and nothing else",
          code == fm.EXIT_LINT and "AP-105: `ask:` is the same question as AP-104" in err and "say why this is different in `considered:`" in err)
    dup.write_text(dup.read_text().replace("shall the launcher   ship first", "Shall the importer ship first?"), encoding="utf-8")
    code, _, err = run(root)
    check("3 · a question that differs by a word is not a duplicate — the match is exact, never fuzzy: a gate that guesses is a gate people route around",
          code == 0 and "same question" not in err)
    dup.write_text(dup.read_text().replace("status: In Progress", "status: Shipped").replace("Shall the importer ship first?", "Shall the launcher ship first?"), encoding="utf-8")
    code, _, err = run(root)
    check("3 · a question closed work once asked is not a duplicate — only an OPEN, unanswered ask holds the question", code == 0 and "same question" not in err)
    gone("AP-104", "AP-105")
    for n_ in range(110, 115):
        ask_(f"AP-{n_}", f"Shall we do the {n_} thing?")
    code, out, _ = run(root, "--owner")
    check("7 · five asks is a queue; six is a finding — under the Owner's count, no line", code == 0 and "bottleneck" not in out and "5 NEED THE OWNER" in out)
    ask_("AP-116", "Shall we do the 116 thing?", extra="\n")
    tracker(root, "AP-117", status="Proposed", extra="blocked-by: AP-116\n", title="held up")
    code, out, _ = run(root, "--owner"); page = (root / "docs/work-tracker/index.html").read_text(encoding="utf-8")
    check("7 · past five asks the first line says whose problem the queue is — `you are the bottleneck`, with the asks and the trackers held up, in --owner and on the board",
          code == 0 and out.startswith("6 NEED THE OWNER") and "you are the bottleneck — 6 asks, 1 trackers held up" in out
          and 'w.length>5?" · "+l("waiting.bottleneck",w.length,held.length)' in page and '"waiting.bottleneck": "you are the bottleneck' in page)
fm.configure(HERE)

# --- FM-008: seats — who may make which change, read from the version control system --------------------------------
with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp).resolve()
    subprocess.run(["git", "init", "-q", str(root)], check=True, env=_ENV)
    for k_, v_ in (("user.name", "impl"), ("user.email", "implementer@seat"), ("commit.gpgsign", "false")):
        git(root, "config", k_, v_)
    plain = 'name = "s"\n[kinds]\nAP = "Work"\n'
    seats = plain + '[seats]\nowner = "holgo99"\nprincipal = "principal@seat"\nimplementer = "implementer@seat"\n'
    (root / "shoalmark.toml").write_text(plain, encoding="utf-8")
    t_ = tracker(root, "AP-200", extra=f'next: owner\nask: "Shall the launcher ship first?"\nask-kind: ruling\nask-since: {old}\nask-proposal: "the launcher"\n', title="an ask")
    run(root); git(root, "add", "-A"); git(root, "commit", "-qm", "the ask", "--author=impl <implementer@seat>")
    code, _, err = run(root)
    check("5 · with no `[seats]` table, nothing is enforced — a repository that never asked for this is not refused by it", code == 0 and "not a seat" not in err)
    (root / "shoalmark.toml").write_text(seats, encoding="utf-8")
    code, out, err = run(root)
    check("5 · the implementer holds no `ask` right: the ask it committed is refused, naming the seat, the right and the id — and it never reaches the Owner's queue",
          code == fm.EXIT_LINT and "AP-200: `next: owner` puts a question in front of the Owner" in err and "`implementer@seat` is the seat `implementer`, which does not hold `ask`" in err
          and run(root, "--owner")[1].startswith("NOTHING NEEDS THE OWNER") and "AP-200" in run(root, "--owner")[1].split("SENT BACK")[1])
    (root / "shoalmark.toml").write_text(seats + '[rights]\nimplementer = ["ask"]\n', encoding="utf-8")
    code, _, err = run(root)
    check("5 · `[rights] implementer = [\"ask\"]` gives a name of your own its rights, in the same diff as anything it would allow", code == 0 and "does not hold" not in err)
    (root / "shoalmark.toml").write_text(seats + '[rights]\nimplementer = ["ask", "merge"]\n', encoding="utf-8")
    try:
        fm.configure(root); said = ""
    except SystemExit as e_:
        said = str(e_)
    (root / "shoalmark.toml").write_text(seats, encoding="utf-8"); fm.configure(root)
    check("5 · there are four rights and no others — a fifth word in `[rights]` is refused, naming it",
          "'merge' is not a right" in said and "answer · ask · close · triage" in said)
    git(root, "commit", "-q", "--amend", "--no-edit", "--author=mallory <mallory@nowhere>"); code, _, err = run(root)
    check("5 · an author the table does not name at all is refused with the seats there are — the badge is `git config --worktree user.email`",
          code == fm.EXIT_LINT and "`mallory@nowhere` is not a seat" in err and "principal (principal@seat)" in err and "--worktree user.email" in err)
    git(root, "commit", "-q", "--amend", "--no-edit", "--author=p <principal@seat>"); code, _, err = run(root)
    check("5 · the principal holds `ask` — the same commit from the seat that may ask passes", code == 0 and "does not hold" not in err)
    # a `close` is a right of its own, judged on the change the commit makes, not on the line
    t_.write_text(t_.read_text().replace("status: In Progress", "status: Shipped"), encoding="utf-8"); git(root, "add", "-A")
    code, _, err = run(root, "--print-written")
    check("5 · closing work is a right of its own: the implementer at the keyboard is refused before the commit exists, naming `close`",
          code == fm.EXIT_LINT and "AP-200: this change is a `close`" in err and "does not hold `close`" in err)
    (root / "shoalmark.toml").write_text(seats + '[rights]\nimplementer = ["close"]\n', encoding="utf-8")
    code, _, err = run(root, "--print-written")
    check("5 · given `close`, the same change passes — no hierarchy, no wildcard: a name either holds a right or it does not", code == 0 and "does not hold" not in err)
    t_.write_text(t_.read_text().replace("status: Shipped", "status: In Progress"), encoding="utf-8")
    # `signed`: a git author is a string. The commit must verify AND the key must be the one the repository trusts for that seat
    key = root / "k"; subprocess.run(["ssh-keygen", "-q", "-t", "ed25519", "-N", "", "-f", str(key)], check=True, capture_output=True)
    other = root / "o"; subprocess.run(["ssh-keygen", "-q", "-t", "ed25519", "-N", "", "-f", str(other)], check=True, capture_output=True)
    (root / "signers").write_text("principal@seat " + key.with_suffix(".pub").read_text(), encoding="utf-8")
    git(root, "config", "gpg.format", "ssh"); git(root, "config", "gpg.ssh.allowedSignersFile", str(root / "signers"))
    (root / "shoalmark.toml").write_text(plain + '[seats]\nprincipal = "principal@seat signed"\n', encoding="utf-8")
    git(root, "config", "user.signingkey", str(other))
    git(root, "commit", "-q", "--amend", "--no-edit", "-S", "--author=p <principal@seat>"); code, _, err = run(root)
    check("5 · a `signed` seat, and the ask signed by a throwaway key the signers file does not tie to it — refused, naming the seat: a signature proves the key, not the hand",
          code == fm.EXIT_LINT and "does not verify as the seat `principal`" in err)
    git(root, "config", "user.signingkey", str(key))
    git(root, "commit", "-q", "--amend", "--no-edit", "-S", "--author=p <principal@seat>"); code, _, err = run(root)
    check("5 · signed by the key the repository trusts for that seat, the same ask passes — one verifier, the answer's", code == 0 and "does not verify" not in err)
    (root / "shoalmark.toml").write_text('name = "s"\nanswerers = ["holgo99"]\n[kinds]\nAP = "Work"\n[seats]\nprincipal = "principal@seat"\n', encoding="utf-8")
    code, _, err = run(root)
    check("5 · `answerers` beside `[seats]` is a note, never a refusal — and since `[seats]` alone decides there, the note says it is not read for answers (FM-015), never that it still works",
          code == 0 and "`answerers` is the old name for the `answer` right" in err and "here it is not read for answers" in err and "still works" not in err)
    # FM-010: the note was guarded on `answerers` AND `[seats]`, so the only repositories told were the ones already
    # migrating. A repository wholly on the old key — the entire population the deprecation is for — heard nothing,
    # while the note promised removal in the next release. `answerers` must go ABOVE any table header: a bare key is
    # read into whichever `[table]` is open, so appending it makes it `[tags].answerers` and the case reads as a pass.
    (root / "shoalmark.toml").write_text('name = "s"\nanswerers = ["holgo99"]\n[kinds]\nAP = "Work"\n', encoding="utf-8")
    code, _, err = run(root)
    check("5 · a repository wholly on `answerers`, with no `[seats]` at all, is told the key is going — the deprecation reaches the population it is for",
          code == 0 and "`answerers` is the old name for the `answer` right" in err)
    # it stays a NOTE for them too. FM-010 widened who sees this line, so a regression turning it into a refusal would
    # now stop every repository still on `answerers` — the exact population the fix was written to reach.
    check("5 · and it stays a note for them — never a refusal: widening who is warned must not widen what is refused", code == 0)
    check("5 · the note carries the version it starts from, not `this release` — it prints unchanged in every release after",
          code == 0 and "the release after 0.17.3" in err and "the clock starts at 0.17.3" in err)
    (root / "shoalmark.toml").write_text('name = "s"\n[kinds]\nAP = "Work"\n[seats]\nprincipal = "principal@seat"\n', encoding="utf-8")
    code, _, err = run(root)
    check("5 · a repository on `[seats]` with no `answerers` is never warned about a key it does not use",
          code == 0 and "is the old name for the `answer` right" not in err)
    rm_git(root)
fm.configure(HERE)

# --- FM-015: `[seats]` must not silently drop a signature `answerers` asked for ---------------------------------------
# From 0.17.1 `[seats]` alone says who may answer, so `answerers = ["alice signed"]` beside `[seats] owner = "alice"`
# accepted Alice's unsigned answer, `--answer` stopped signing, and the note said `answerers` "still works". `answerers`
# goes ABOVE every table header, or it is read as `[tags].answerers` and the case passes for the wrong reason.
with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp).resolve()
    subprocess.run(["git", "init", "-q", str(root)], check=True, env=_ENV)
    for k_, v_ in (("user.name", "alice"), ("user.email", "alice@x"), ("commit.gpgsign", "false")):
        git(root, "config", k_, v_)
    cfg_ = lambda answerers, seats: (root / "shoalmark.toml").write_text('name = "a"\n' + (f"answerers = {answerers}\n" if answerers else "")
                                                                      + '[kinds]\nAP = "Work"\n' + (f'[seats]\n{seats}\nprincipal = "p@seat"\n' if seats else ""), encoding="utf-8")
    cfg_("", "")
    tracker(root, "AP-700", extra=f'next: owner\nask: "Shall the launcher ship first?"\nask-kind: ruling\nask-since: {old}\nask-proposal: "the launcher"\n', title="an ask")
    run(root); git(root, "add", "-A"); git(root, "commit", "-qm", "the ask", "--author=p <p@seat>")     # asked by the principal, which signs nothing
    cfg_('["alice signed"]', 'owner = "alice signed"'); code_a, _, err_a = run(root, "--check")
    check("FM-015 · `answerers` signed and the seat that answers for it signed — clean, and told `answerers` is not read here and can go",
          code_a == 0 and "answerers" in err_a and "here it is not read for answers" in err_a and "is not signed" not in err_a)
    cfg_('["alice signed"]', 'owner = "alice"'); code_b, _, err_b = run(root, "--check")
    check("FM-015 · `answerers` signed and the seat that answers for it NOT signed — REFUSED, naming both lines and the two ways out",
          code_b == fm.EXIT_LINT and '`answerers = ["alice signed"]` asks for a signed answer' in err_b and '`[seats] owner = "alice"`' in err_b
          and 'Add `signed` to the seat (`owner = "alice signed"`), or remove `answerers`' in err_b)
    code_c, _, err_c = run(root, "--answer", "AP-700", "accept")
    check("FM-015 · …and `--answer` refuses the same way before it touches anything — it would have committed unsigned",
          code_c == fm.EXIT_LINT and '`[seats] owner = "alice"`' in err_c and "answering AP-700 — 2/4" not in err_c
          and subprocess.run(["git", "-C", str(root), "branch", "--list", "answer/ap-700"], capture_output=True, text=True, env=_ENV).stdout.strip() == "")
    cfg_('["alice signed"]', 'owner = "alice@x"'); code_d, _, err_d = run(root, "--check")
    check("FM-015 · where no seat is spelled like the `answerers` entry — a name there, an email here — the seats holding `answer` stand in for it, and an unsigned one is refused",
          code_d == fm.EXIT_LINT and '`[seats] owner = "alice@x"`' in err_d and "no seat is spelled `alice`" in err_d)
    cfg_('["alice signed"]', ""); code_e, _, err_e = run(root, "--check")
    check("FM-015 · no `[seats]` — `answerers` is read, and the note is today's, with its removal anchored to 0.17.3",
          code_e == 0 and "and still works" in err_e and "the release after 0.17.3" in err_e and "is not signed" not in err_e)
    cfg_("", 'owner = "alice"'); code_f, _, err_f = run(root, "--check")
    check("FM-015 · `[seats]` and no `answerers` — silent: no note, no refusal", code_f == 0 and "answerers" not in err_f)
    rm_git(root)
fm.configure(HERE)

# --- who may answer is ONE list: the seats that hold `answer`, and `answerers` only where there are no seats ---------
# `answerers` is documented as the old name for the owner seat's `answer` right, but the answer gate read `ANSWERERS`
# alone: a repository that had moved to `[seats]` got "an answer, but `answerers` names nobody" for every answer.
with tempfile.TemporaryDirectory() as tmp:
    base = Path(tmp).resolve(); root = base / "wc"; root.mkdir()
    subprocess.run(["git", "init", "-q", "--bare", str(base / "origin.git")], check=True, env=_ENV)
    subprocess.run(["git", "init", "-q", str(root)], check=True, env=_ENV)
    key = base / "k"; subprocess.run(["ssh-keygen", "-q", "-t", "ed25519", "-N", "", "-f", str(key)], check=True, capture_output=True)
    (root / "signers").write_text("holgoijo@x " + key.with_suffix(".pub").read_text(), encoding="utf-8")
    for k_, v_ in (("user.name", "holgo"), ("user.email", "holgoijo@x"), ("gpg.format", "ssh"), ("user.signingkey", str(key)),
                   ("gpg.ssh.allowedSignersFile", str(root / "signers")), ("commit.gpgsign", "false")):
        git(root, "config", k_, v_)
    (root / "shoalmark.toml").write_text('name = "w"\n[kinds]\nAP = "Work"\n[seats]\nowner = "holgoijo@x signed"\nimplementer = "implementer@seat"\n', encoding="utf-8")
    tracker(root, "AP-400", extra=f'next: owner\nask: "Shall the launcher ship first?"\nask-kind: ruling\nask-since: {old}\nask-proposal: "the launcher"\n'
                                  f'answer: "accepted - the launcher"\nanswered: {new_}\nanswered-by: holgo\n', title="answered")
    git(root, "add", "-A"); git(root, "commit", "-qm", "the answer", "-S", "--author=holgo <holgoijo@x>")
    code, _, err = run(root)
    check("with `[seats]` and no `answerers`, the seats holding `answer` ARE the answerers — the owner's signed answer passes, where the gate used to say `answerers` names nobody",
          code == 0 and "names nobody" not in err and "not in `answerers`" not in err)
    git(root, "commit", "-q", "--amend", "--no-edit", "-S", "--author=impl <implementer@seat>"); code, _, err = run(root)
    check("the same answer from a seat that does not hold `answer` is refused, naming the seat and the right — one reader for who may answer, and it is the seats table",
          code == fm.EXIT_LINT and "an answer counts only from a seat that may give one" in err and "`implementer@seat` is the seat `implementer`, which does not hold `answer`" in err)
    git(root, "commit", "-q", "--amend", "--no-edit", "-S", "--author=mallory <mallory@nowhere>"); code, _, err = run(root)
    check("an answer from an author the seats table does not name at all is refused with the seats there are",
          code == fm.EXIT_LINT and "`mallory@nowhere` is not a seat" in err)
    # `signed` on the seat is the gate's own verifier: a good signature under the key the repository trusts FOR it
    git(root, "commit", "-q", "--amend", "--no-edit", "--no-gpg-sign", "--author=holgo <holgoijo@x>"); code, _, err = run(root)
    check("`[seats] owner = \"… signed\"` asks the answer's commit to verify as that seat — unsigned, the answer does not count",
          code == fm.EXIT_LINT and "does not verify as `holgoijo@x`" in err and "`[seats]` asks this seat for a signed answer" in err)
    # and with `[rights]`, a name of your own may answer — the same one reader
    (root / "shoalmark.toml").write_text('name = "w"\n[kinds]\nAP = "Work"\n[seats]\nowner = "nobody@x"\nimplementer = "implementer@seat"\n[rights]\nimplementer = ["answer"]\n', encoding="utf-8")
    git(root, "commit", "-q", "--amend", "--no-edit", "--author=holgo <implementer@seat>"); code, _, err = run(root)
    check("a seat given `answer` in `[rights]` may answer, unsigned — the list is the rights table, not a second one",
          code == 0 and "does not hold `answer`" not in err and "names nobody" not in err)
    (root / "shoalmark.toml").write_text('name = "w"\n[kinds]\nAP = "Work"\n[seats]\nimplementer = "implementer@seat"\n', encoding="utf-8")
    code, _, err = run(root)
    check("`[seats]` with no seat holding `answer` says exactly that — never `answerers` names nobody, which there is no longer a way to fix",
          code == fm.EXIT_LINT and "no seat in `[seats]` holds the `answer` right" in err and "`answerers`" not in err.split("no seat in")[1])
    # the Owner's one command reads the same list: on a repository with `[seats]` and no `answerers` it used to refuse
    # every answer before it cut the branch — `--answer` is the only way in, so the queue could not be emptied at all
    (root / "shoalmark.toml").write_text('name = "w"\n[kinds]\nAP = "Work"\n[seats]\nowner = "holgoijo@x signed"\nimplementer = "implementer@seat"\n', encoding="utf-8")
    for p_ in (root / "docs/work-tracker").glob("AP-400-*.md"):
        p_.unlink()
    git(root, "remote", "add", "origin", str(base / "origin.git"))
    tracker(root, "AP-401", extra=f'next: owner\nask: "Shall the launcher ship first?"\nask-kind: ruling\nask-since: {old}\nask-proposal: "the launcher"\n', title="an ask")
    run(root); git(root, "add", "-A"); git(root, "commit", "-qm", "the ask", "-S", "--author=holgo <holgoijo@x>"); git(root, "push", "-q", "-u", "origin", "HEAD:pd/401")
    code, out, err = run(root, "--answer", "AP-401", "accept")
    sig = subprocess.run(["git", "-C", str(root), "log", "-1", "--format=%G? %GS %ae"], capture_output=True, text=True, env=_ENV).stdout.strip()
    check("`--answer` reads the same list: the owner seat answers on a repository that has no `answerers` at all — signed, and the gate it just wrote for accepts it",
          code == 0 and "not in `answerers`" not in err and sig.startswith("G holgoijo@x holgoijo@x") and run(root, "--check")[0] == 0)
    (root / "shoalmark.toml").write_text('name = "w"\n[kinds]\nAP = "Work"\n[seats]\nowner = "someone@else"\nimplementer = "holgoijo@x"\n', encoding="utf-8")
    tracker(root, "AP-402", extra=f'next: owner\nask: "And the second thing?"\nask-kind: ruling\nask-since: {old}\nask-proposal: "the launcher"\n', title="an ask")
    run(root); git(root, "add", "-A"); git(root, "commit", "-qm", "another ask", "--author=p <someone@else>")
    code, _, err = run(root, "--answer", "AP-402", "accept")
    check("`--answer` from a seat that does not hold `answer` is refused before the branch is cut, naming the seat and the right",
          code == fm.EXIT_LINT and "an answer is an `answer` change" in err and "does not hold `answer`" in err
          and subprocess.run(["git", "-C", str(root), "branch", "--show-current"], capture_output=True, text=True, env=_ENV).stdout.strip() != "answer/ap-402")
    rm_git(root)
fm.configure(HERE)

# --- line_author: the seat that set the line, across a merge that restores what was already there --------------------
# Git's default history simplification follows ONE parent of a merge it is TREESAME to. A branch that moves a line away
# and back (owner -> review -> owner) merges to a file byte-identical to main's, so the whole branch is pruned and the
# pickaxe answers with the commit BEFORE it — the board then reads a re-asked tracker as sent back by the wrong seat.
with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp).resolve()
    subprocess.run(["git", "init", "-q", str(root)], check=True, env=_ENV)
    for k_, v_ in (("user.name", "a"), ("user.email", "a@seat"), ("commit.gpgsign", "false")):
        git(root, "config", k_, v_)
    (root / "shoalmark.toml").write_text('name = "m"\n[kinds]\nAP = "Work"\n', encoding="utf-8")
    t_ = tracker(root, "AP-300", extra=f'next: owner\nask: "Shall the launcher ship first?"\nask-kind: ruling\nask-since: {old}\nask-proposal: "the launcher"\n', title="an ask")
    git(root, "add", "-A"); git(root, "commit", "-qm", "A: the ask", "--author=a <a@seat>", day="2026-01-01")
    trunk = subprocess.run(["git", "-C", str(root), "branch", "--show-current"], capture_output=True, text=True, env=_ENV).stdout.strip()
    git(root, "switch", "-q", "-c", "br")
    t_.write_text(t_.read_text().replace("next: owner", "next: review"), encoding="utf-8")
    git(root, "commit", "-qam", "B: sent back", "--author=b <b@seat>", day="2026-01-02")
    t_.write_text(t_.read_text().replace("next: review", "next: owner"), encoding="utf-8")
    git(root, "commit", "-qam", "B: re-asked", "--author=b <b@seat>", day="2026-01-03")
    b_ = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"], capture_output=True, text=True, env=_ENV).stdout.strip()
    git(root, "switch", "-q", trunk); git(root, "merge", "-q", "--no-ff", "br", "-m", "the merge", day="2026-01-04")
    merge_ = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"], capture_output=True, text=True, env=_ENV).stdout.strip()
    fm.configure(root); name_, email_, how_, rev_ = fm.line_author(t_, "next: owner")
    check("the line belongs to the seat whose commit set it, even when the merge restored a file byte-identical to the one before the branch — `--full-history`, or git prunes the branch and answers with the commit before it",
          how_ == "git" and rev_ == b_ and email_ == "b@seat" and name_ == "b")
    # ...and never the merge itself: a merge carries no diff of its own, so the seat that merged a line is not the seat
    # that wrote it. `-m` would split the merge against each parent and name the merger — which is why it is not there.
    t_.write_text(t_.read_text().replace("hook:", "answer: accepted - ship it\nanswered-by: holgo\nhook:"), encoding="utf-8")
    git(root, "switch", "-q", "-c", "br2"); git(root, "commit", "-qam", "C: the answer", "--author=c <c@seat>", day="2026-01-05")
    c_ = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"], capture_output=True, text=True, env=_ENV).stdout.strip()
    git(root, "switch", "-q", trunk); git(root, "merge", "-q", "--no-ff", "br2", "-m", "the answer merged", day="2026-01-06")
    merge2_ = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"], capture_output=True, text=True, env=_ENV).stdout.strip()
    fm.configure(root); who_, _e2, how2_, rev2_ = fm.line_author(t_, "answer:")
    check("an `answer:` that reached the trunk through a merge is the answerer's commit, never the merge's — the one reader answers for both lines",
          how2_ == "git" and rev2_ == c_ and rev2_ not in (merge_, merge2_) and who_ == "c")
    rm_git(root)
fm.configure(HERE)

# --- line_author: a tracker's own prose about its keys is not its front matter ---------------------------------------
# What the Owner's first real answer hit. FM-007's body carries the sentence "an `answer:` counts only from the account
# it is filed from"; the reader looked for the SUBSTRING `answer:` and found the commit that wrote that sentence, and
# the "is it committed yet" test was a substring of the same kind, so a line staged and never committed read as
# committed — by somebody else, unsigned. The gate then refused the Owner's own answer. Both tests anchor to the line.
with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp).resolve()
    subprocess.run(["git", "init", "-q", str(root)], check=True, env=_ENV)
    for k_, v_ in (("user.name", "a"), ("user.email", "a@seat"), ("commit.gpgsign", "false")):
        git(root, "config", k_, v_)
    (root / "shoalmark.toml").write_text('name = "m"\n[kinds]\nAP = "Work"\n', encoding="utf-8")
    prose_ = ("## What is true now\n\n**One thing is left.**\n\nAn `answer:` counts only from the account it is filed from, and\n"
              "`next: owner` puts a question in front of the Owner.\n\n## Done when\n\nit is.\n")
    t_ = tracker(root, "AP-310", extra="next: build\n", body=prose_, title="a tracker that discusses its own keys")
    git(root, "add", "-A"); git(root, "commit", "-qm", "A: the prose", "--author=a <a@seat>", day="2026-01-01")
    t_.write_text(t_.read_text().replace("hook:", 'answer: "accepted — ship it"\nanswered-by: holgo\nhook:'), encoding="utf-8")
    git(root, "add", "-A")                               # staged, not committed — the Owner's tree at the moment the gate ran
    fm.configure(root); who_, _e1, how_, rev_ = fm.line_author(t_, "answer:")
    git(root, "commit", "-qm", "B: the answer", "--author=b <b@seat>", day="2026-01-02")
    b_ = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"], capture_output=True, text=True, env=_ENV).stdout.strip()
    fm.configure(root); who2_, e2_, how2b_, rev2b_ = fm.line_author(t_, "answer:")
    check("an `answer:` staged and not committed reads as uncommitted, though the body's sentence about `answer:` was committed long ago — and once committed the line belongs to the commit that SET it, not to the one that wrote the sentence",
          how_ == "uncommitted" and rev_ == "" and who_ is None and how2b_ == "git" and rev2b_ == b_ and who2_ == "b" and e2_ == "b@seat")
    # the other line the same reader serves: prose naming the key was committed before it was set, and again after
    t_.write_text(t_.read_text().replace("next: build", "next: owner"), encoding="utf-8")
    git(root, "add", "-A"); git(root, "commit", "-qm", "C: the ask", "--author=c <c@seat>", day="2026-01-03")
    c2_ = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"], capture_output=True, text=True, env=_ENV).stdout.strip()
    t_.write_text(t_.read_text() + "\nAnd `next: owner` is what the board reads, so the ask reaches him.\n", encoding="utf-8")
    git(root, "add", "-A"); git(root, "commit", "-qm", "D: the body, edited", "--author=d <d@seat>", day="2026-01-04")
    d_ = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"], capture_output=True, text=True, env=_ENV).stdout.strip()
    fm.configure(root); who3_, e3_, how3_, rev3_ = fm.line_author(t_, "next: owner")
    check("`next: owner` belongs to the seat whose commit set the line, not to the seat that later edited a sentence naming it — by substring the newest mention of the key wins, and the board names the wrong asker",
          how3_ == "git" and rev3_ == c2_ and rev3_ != d_ and who3_ == "c" and e3_ == "c@seat")
    # the pattern itself, not the answer it gave here: `-G` compiles a POSIX EXTENDED regular expression, and git
    # carries a different engine on each platform. `re.escape` would write the space as `\ ` and a hyphen as `\-`,
    # and a backslash before an ordinary character is undefined in ERE — one platform reads a literal, another need not
    fm.configure(root)
    sent_ = [c for c in argv_of(lambda: fm.line_author(t_, "next: owner")) if "-G" in c]
    check("the pattern handed to git is the plain anchored key — `^next: owner`, the space unescaped — and the keys that carry a hyphen are plain too: an ERE escape of an ordinary character is undefined, and the gate must answer the same on every platform's regex engine",
          len(sent_) == 1 and sent_[0][sent_[0].index("-G") + 1] == "^next: owner" and "--full-history" in sent_[0]
          and fm.line_regex("answer:") == "^answer:" and fm.line_regex("kind-of-problem:") == "^kind-of-problem:"
          and fm.line_regex("a.b[c]:") == "^a\\.b\\[c\\]:")
    rm_git(root)
fm.configure(HERE)

# --- acted_on: prose about `ask:` is not the commit that cleared the ask ----------------------------------------------
# `--answered` names the commit that removed the `ask:` line. Trackers discuss `ask:` in their prose all the time, so by
# substring any later edit of the body became "acted on" — a tracker cleared months ago reappears at today's standup.
with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp).resolve()
    subprocess.run(["git", "init", "-q", str(root)], check=True, env=_ENV)
    for k_, v_ in (("user.name", "holgo"), ("user.email", "h@x"), ("commit.gpgsign", "false")):
        git(root, "config", k_, v_)
    (root / "shoalmark.toml").write_text('name = "r"\nanswerers = ["holgo"]\n[kinds]\nAP = "Work"\n', encoding="utf-8")
    t_ = tracker(root, "AP-320", extra=f'next: owner\nask: "Shall the launcher ship first?"\nask-kind: ruling\nask-since: {old}\n'
                 f'ask-proposal: "the launcher"\nanswer: "accepted — the launcher"\nanswered: {new_}\nanswered-by: holgo\n', title="answered")
    git(root, "add", "-A"); git(root, "commit", "-qm", "the ask and its answer", day="2026-01-01")
    body_ = t_.read_text().split("---\n", 2)[2]
    t_.write_text(f'---\nid: AP-320\nstatus: In Progress\nconsidered: none\nnext: build\nhook: "h of AP-320"\n---\n{body_}'
                  f'\n## Asks\n\n{new_} · Shall the launcher ship first? · accepted — the launcher · holgo\n', encoding="utf-8")
    git(root, "add", "-A"); git(root, "commit", "-qm", "AP-320 acted on", day="2026-01-02")   # long before any standup
    cleared_ = subprocess.run(["git", "-C", str(root), "log", "-1", "--format=%h"], capture_output=True, text=True, env=_ENV).stdout.strip()
    t_.write_text(t_.read_text() + "\nAn `ask:` reaches the Owner only through the gate, and carries its `ask-kind:`.\n", encoding="utf-8")
    git(root, "add", "-A"); git(root, "commit", "-qm", "the body, edited today")              # today, after the last standup
    fm.configure(root); trackers_ = fm.load_trackers()
    sent_ = [c for c in argv_of(lambda: fm.acted_on(trackers_)) if "-G" in c]
    acted_ = fm.acted_on(trackers_); code, out, _ = run(root, "--answered")
    check("a sentence about `ask:` committed today is not the commit that cleared the ask — the ask left months ago, and nothing a later body edit says puts the tracker back on today's agenda",
          acted_ == [] and code == 0 and "AP-320" not in out and cleared_ not in out)
    check("`--answered` asks git the same way the one reader does — `-G ^ask:` and `--full-history`, so an ask cleared on a branch that merged back to identical content is not walked past",
          len(sent_) == 1 and sent_[0][sent_[0].index("-G") + 1] == "^ask:" and "--full-history" in sent_[0])
    rm_git(root)
fm.configure(HERE)

# --- FM-008: clearing an ask keeps the record, and what --answer could not say ---------------------------------------
with tempfile.TemporaryDirectory() as tmp:
    base = Path(tmp).resolve(); root = base / "wc"; root.mkdir()
    subprocess.run(["git", "init", "-q", "--bare", str(base / "origin.git")], check=True, env=_ENV); subprocess.run(["git", "init", "-q", str(root)], check=True, env=_ENV)
    for k_, v_ in (("user.name", "holgo"), ("user.email", "h@x"), ("commit.gpgsign", "false")):
        git(root, "config", k_, v_)
    git(root, "remote", "add", "origin", str(base / "origin.git"))
    (root / "shoalmark.toml").write_text('name = "r"\nanswerers = ["holgo"]\n[kinds]\nAP = "Work"\n', encoding="utf-8")
    t_ = tracker(root, "AP-300", extra=f'next: owner\nask: "Shall the launcher ship first?"\nask-kind: ruling\nask-since: {old}\nask-proposal: "the launcher"\n'
                 f'answer: "accepted — the launcher, and count a week"\nanswered: {new_}\nanswered-by: holgo\n', title="answered")
    run(root); git(root, "add", "-A"); git(root, "commit", "-qm", "the answer")
    was = t_.read_text()
    t_.write_text("".join(l + "\n" for l in was.split("\n") if not l.startswith(("ask", "answer"))).replace("next: owner", "next: build"), encoding="utf-8")
    git(root, "add", "-A"); code, _, err = run(root, "--print-written")
    check("6 · an answer removed from the front matter and written nowhere else is refused — the ruling would be gone, and the next seat would ask it again",
          code == fm.EXIT_LINT and "AP-300: the answer is being removed and the exchange is nowhere in the body" in err and "--clear-ask AP-300" in err)
    t_.write_text(was, encoding="utf-8"); git(root, "add", "-A")
    code, out, _ = run(root, "--clear-ask", "AP-300", "build")
    kept = t_.read_text()
    check("6 · `--clear-ask <id> <next move>` does it correctly: the exchange goes into the body under `## Asks` — date · question · answer · answered-by — the lines leave the front matter, and the move is the one given",
          code == 0 and "## Asks" in kept and "Shall the launcher ship first?" in kept.split("## Asks")[1] and "accepted — the launcher, and count a week" in kept.split("## Asks")[1]
          and "holgo" in kept.split("## Asks")[1] and new_ in kept.split("## Asks")[1] and "next: build" in kept and "ask:" not in kept.split("---")[1] and "answer:" not in kept.split("---")[1])
    git(root, "add", "-A"); code, _, err = run(root, "--print-written")
    check("6 · with the record in the body, the same removal passes the gate", code == 0 and "nowhere in the body" not in err)
    git(root, "commit", "-qm", "AP-300 acted on"); short = subprocess.run(["git", "-C", str(root), "log", "-1", "--format=%h"], capture_output=True, text=True, env=_ENV).stdout.strip()
    code, out, _ = run(root, "--answered")
    check("6 · --answered says what a seat has acted on since the last standup, by the commit that cleared the ask — the Owner reads what his answer became",
          code == 0 and "ACTED ON SINCE THE LAST STANDUP" in out and f"AP-300 — acted on in `{short}`" in out)
    # what the 0.16.0 implementer reported: --answer switched to an `answer/<id>` that does not carry the ask, and raised on an ask that is not its own line
    t2 = tracker(root, "AP-301", extra=f'next: owner\nask: "Shall the importer ship first?"\nask-kind: ruling\nask-since: {old}\nask-proposal: "the importer"\n', title="second ask")
    run(root); git(root, "add", "-A"); git(root, "commit", "-qm", "a second ask")
    git(root, "switch", "-q", "-c", "answer/ap-301"); git(root, "switch", "-q", "-")
    code, _, err = run(root, "--answer", "AP-301", "accept", "the importer")
    check("8 · `--answer` refuses an `answer/<id>` that exists and is not merged — it may hold work, and nothing unmerged is deleted for him; the refusal names the one command that clears it",
          code == fm.EXIT_LINT and "`answer/ap-301` exists and is not merged into `origin`" in err and "`git branch -D answer/ap-301`" in err and subprocess.run(["git", "-C", str(root), "branch", "--show-current"], capture_output=True, text=True, env=_ENV).stdout.strip() != "answer/ap-301")
    git(root, "branch", "-q", "-D", "answer/ap-301")
    t2.write_text(t2.read_text().replace('\nask: "Shall', '\n ask: "Shall'), encoding="utf-8")
    git(root, "add", "-A"); git(root, "commit", "-qm", "the ask, indented")      # --answer wants a clean tree; the ask still parses
    code, _, err = run(root, "--answer", "AP-301", "accept", "the importer")
    check("9 · an ask that parsed but is not its own line gets a refusal, not a traceback out of `next(...)`",
          code == fm.EXIT_LINT and "has no `ask:` line" in err and "Traceback" not in err)
    rm_git(root)
fm.configure(HERE)

# --- FM-014: clearing an answered ask WITH its record is the `ask` right's move, not an `answer` --------------------------
# `--clear-ask` drops the three answer lines and writes the exchange under `## Asks`. The rights gate read ANY change to
# those lines as `answer` — the owner's alone — so the seat that acts on answers could never record that it had.
with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp).resolve()
    subprocess.run(["git", "init", "-q", str(root)], check=True, env=_ENV)
    for k_, v_ in (("user.name", "holgo"), ("user.email", "h@x"), ("commit.gpgsign", "false")):
        git(root, "config", k_, v_)
    (root / "shoalmark.toml").write_text('name = "c"\n[kinds]\nAP = "Work"\n[seats]\nowner = "h@x"\nprincipal = "principal@seat"\nimplementer = "implementer@seat"\n', encoding="utf-8")
    for n_ in (600, 601, 602, 603):
        tracker(root, f"AP-{n_}", extra=f'next: owner\nask: "Shall {n_} ship first?"\nask-kind: ruling\nask-since: {old}\nask-proposal: "ship it"\n'
                                         f'answer: "accepted - ship it, and count a week"\nanswered: {new_}\nanswered-by: holgo\n', title="answered")
    run(root); git(root, "add", "-A"); git(root, "commit", "-qm", "the answers", "--author=holgo <h@x>")
    wt_ = root / "docs/work-tracker"
    def _as(seat_email, change):
        """the seat at the keyboard makes `change`, stages it, and the pre-commit run judges it; then it is put back"""
        git(root, "config", "user.email", seat_email); change(); git(root, "add", "-A")
        r_ = run(root, "--print-written"); git(root, "reset", "-q", "--hard"); return r_
    code, _, err = _as("principal@seat", lambda: run(root, "--clear-ask", "AP-600", "build"))
    check("FM-014 · the principal clears an answered ask with `--clear-ask` — the record written, the lines gone — and the gate passes it: a clear is the `ask` right's",
          code == 0 and "does not hold" not in err and "nowhere in the body" not in err)
    git(root, "config", "user.email", "principal@seat"); run(root, "--clear-ask", "AP-600", "build"); run(root); git(root, "add", "-A")
    git(root, "commit", "-qm", "AP-600 acted on", "--author=p <principal@seat>"); code, _, err = run(root, "--check")
    check("FM-014 · …and committed, `--check` reads the same commit the same way", code == 0 and "does not hold" not in err)
    code, _, err = _as("implementer@seat", lambda: run(root, "--clear-ask", "AP-601", "build"))
    check("FM-014 · the implementer, which holds no `ask`, is refused the same clear — naming the move and the right",
          code == fm.EXIT_LINT and "AP-601: this change clears an answered ask" in err and "which does not hold `ask`" in err)
    strip_ = lambda n_: (lambda p_: p_.write_text("".join(l + "\n" for l in p_.read_text().split("\n")[:-1] if not l.startswith("answer")), encoding="utf-8"))(next(wt_.glob(f"AP-{n_}-*.md")))
    code, _, err = _as("principal@seat", lambda: strip_(602))
    check("FM-014 · the answer removed WITHOUT its record is refused — as an `answer`, the Owner's, and as a ruling gone from the record",
          code == fm.EXIT_LINT and "AP-602: this change is a `answer`" in err and "does not hold `answer`" in err and "AP-602: the answer is being removed and the exchange is nowhere in the body" in err)
    edit_ = lambda: (lambda p_: p_.write_text(p_.read_text().replace("ship it, and count a week", "ship it"), encoding="utf-8"))(next(wt_.glob("AP-603-*.md")))
    code, _, err = _as("principal@seat", edit_)
    check("FM-014 · the answer's text edited by the principal is refused as an `answer` — only the Owner writes his words",
          code == fm.EXIT_LINT and "AP-603: this change is a `answer`" in err and "clears an answered ask" not in err)
    rm_git(root)
fm.configure(HERE)

# --- FM-019: a merge is judged by its own change — never by everything its branch carried ------------------------------
# On a clean tree the gate read HEAD against HEAD~1. For a merge that is the whole pull request, every answer and close
# in it attributed to whoever merged — the forge's merge identity, no seat — so `--check` on a trunk went red on the first
# merge that carried one. A merge's own change is what differs from EVERY parent: a conflict resolved, an edit in the merge.
with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp).resolve()
    subprocess.run(["git", "init", "-q", str(root)], check=True, env=_ENV)
    for k_, v_ in (("user.name", "holgo"), ("user.email", "principal@seat"), ("commit.gpgsign", "false")):
        git(root, "config", k_, v_)
    (root / "shoalmark.toml").write_text('name = "m"\n[kinds]\nAP = "Work"\n[seats]\nowner = "h@x"\nprincipal = "principal@seat"\nimplementer = "implementer@seat"\n', encoding="utf-8")
    ask19_ = lambda n_, q_: tracker(root, f"AP-{n_}", extra=f'next: owner\nask: "{q_}"\nask-kind: ruling\nask-since: {old}\nask-proposal: "yes"\n', title="an ask")
    ask19_(800, "Shall the launcher ship first?"); ask19_(811, "Shall the importer ship first?")
    tracker(root, "AP-801", title="to close"); tracker(root, "AP-802", title="to judge")
    tracker(root, "AP-810", body="## What is true now\n\n**One thing is left.**\n\nleft: the first thing\n\n## Done when\n\nit is.\n", title="both sides edit")
    (root / "notes.txt").write_text("trunk\n", encoding="utf-8")
    run(root); git(root, "add", "-A"); git(root, "commit", "-qm", "the trackers", "--author=p <principal@seat>")
    trunk_ = subprocess.run(["git", "-C", str(root), "branch", "--show-current"], capture_output=True, text=True, env=_ENV).stdout.strip()
    edit19_ = lambda n_, a_, b_: (lambda p_: p_.write_text(p_.read_text().replace(a_, b_), encoding="utf-8"))(next((root / "docs/work-tracker").glob(f"AP-{n_}-*.md")))
    answer19_ = lambda n_: edit19_(n_, 'ask-proposal: "yes"\n', f'ask-proposal: "yes"\nanswer: "accepted - yes"\nanswered: {new_}\nanswered-by: holgo\n')
    merged19_ = lambda *a: subprocess.run(["git", "-C", str(root), "-c", "core.hooksPath=/dev/null", "-c", "commit.gpgsign=false", *a], capture_output=True, text=True,
                                          env=dict(_ENV, GIT_AUTHOR_NAME="GitHub", GIT_AUTHOR_EMAIL="noreply@github.com", GIT_COMMITTER_NAME="GitHub", GIT_COMMITTER_EMAIL="noreply@github.com"))
    # (a) a branch carrying an answer (the owner's), a close and a triage verdict (the principal's) — each by the seat that may
    git(root, "switch", "-q", "-c", "pr/a")
    answer19_(800); git(root, "commit", "-qam", "AP-800: accepted", "--author=holgo <h@x>")
    edit19_(801, "status: In Progress", "status: Shipped"); git(root, "commit", "-qam", "AP-801 shipped", "--author=p <principal@seat>")
    edit19_(802, "considered: none\n", "considered: none\ntier: P1\n"); run(root); git(root, "add", "-A"); git(root, "commit", "-qm", "AP-802 judged", "--author=p <principal@seat>")
    git(root, "switch", "-q", trunk_); (root / "notes.txt").write_text("trunk moved on\n", encoding="utf-8"); git(root, "commit", "-qam", "meanwhile", "--author=p <principal@seat>")
    mg_ = merged19_("merge", "--no-ff", "-q", "pr/a", "-m", "Merge pull request from pr/a")
    code, _, err = run(root, "--check")
    check("FM-019 · (a) a clean merge by the forge's identity, no seat, of a branch carrying an answer, a close and a triage verdict — no rights problem: it made none of them",
          mg_.returncode == 0 and code == 0 and "not a seat" not in err and "this change is a" not in err)
    # (b) a conflict the merger resolves, and in resolving it closes the tracker: THAT is the merge's own, and its seat's
    git(root, "switch", "-q", "-c", "pr/b"); answer19_(811); git(root, "commit", "-qam", "AP-811: accepted", "--author=holgo <h@x>")
    edit19_(810, "left: the first thing", "left: the branch's thing"); git(root, "commit", "-qam", "AP-810 on the branch", "--author=p <principal@seat>")
    git(root, "switch", "-q", trunk_); edit19_(810, "left: the first thing", "left: the trunk's thing"); git(root, "commit", "-qam", "AP-810 on the trunk", "--author=p <principal@seat>")
    conflict_ = merged19_("merge", "--no-ff", "-q", "pr/b", "-m", "Merge pull request from pr/b")
    p810_ = next((root / "docs/work-tracker").glob("AP-810-*.md"))
    p810_.write_text(re.sub(r"<<<<<<<[^\n]*\n.*?>>>>>>>[^\n]*\n", "left: both things\n", p810_.read_text(), flags=re.S).replace("status: In Progress", "status: Shipped"), encoding="utf-8")
    git(root, "config", "user.email", "implementer@seat"); git(root, "add", "-A"); run(root); git(root, "add", "-A")
    code_pre, _, err_pre = run(root, "--print-written")
    check("FM-019 · (b) the merge being committed: a conflict resolution that closes a tracker is the merger's `close`, judged under the seat at the keyboard — and the answer the branch brought in is not",
          conflict_.returncode != 0 and code_pre == fm.EXIT_LINT and "AP-810: this change is a `close`" in err_pre and "which does not hold `close`" in err_pre and "AP-811: this change" not in err_pre)
    git(root, "config", "user.email", "principal@seat"); run(root); git(root, "add", "-A")        # the INDEX.md the hook would stage, without the refusal's banner
    git(root, "commit", "-q", "--no-edit", "--author=impl <implementer@seat>"); code, _, err = run(root, "--check")
    check("FM-019 · (b) …and committed, `--check` reads the merge the same way: its own close, the implementer's, refused — nothing the branch carried",
          code == fm.EXIT_LINT and "AP-810: this change is a `close`" in err and "`implementer@seat` is the seat `implementer`" in err and "AP-811: this change" not in err and "AP-811: in `" not in err)
    git(root, "commit", "-q", "--amend", "--no-edit", "--author=p <principal@seat>"); code, _, err = run(root, "--check")
    check("FM-019 · (b) the same resolution merged by the principal, which holds `close`, passes", code == 0 and "this change is a" not in err)
    rm_git(root)
fm.configure(HERE)

# --- FM-019: …and a merge does not launder what it brings: every commit it brings is read, under its own author --------
# A commit made without the hook — `--no-verify`, a clone with none installed, the forge's editor — was never judged. The
# merge's own change is the merger's; each commit it brings is judged against its own parent, under its own signature.
with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp).resolve()
    subprocess.run(["git", "init", "-q", str(root)], check=True, env=_ENV)
    for k_, v_ in (("user.name", "p"), ("user.email", "principal@seat"), ("commit.gpgsign", "false")):
        git(root, "config", k_, v_)
    (root / "shoalmark.toml").write_text('name = "l"\n[kinds]\nAP = "Work"\n[seats]\nowner = "h@x signed"\nprincipal = "principal@seat"\nimplementer = "implementer@seat"\n', encoding="utf-8")
    for n_ in range(920, 940):
        tracker(root, f"AP-{n_}", title="worked on")
    tracker(root, "AP-900", extra=f'next: owner\nask: "Shall the launcher ship first?"\nask-kind: ruling\nask-since: {old}\nask-proposal: "yes"\n', title="an ask")
    tracker(root, "AP-901", title="to close")
    (root / "notes.txt").write_text("trunk\n", encoding="utf-8")
    run(root); git(root, "add", "-A"); git(root, "commit", "-qm", "the trackers", "--author=p <principal@seat>")
    trunk_ = subprocess.run(["git", "-C", str(root), "branch", "--show-current"], capture_output=True, text=True, env=_ENV).stdout.strip()
    sha_ = lambda rev="HEAD": subprocess.run(["git", "-C", str(root), "rev-parse", rev], capture_output=True, text=True, env=_ENV).stdout.strip()
    move_ = lambda text: ((root / "notes.txt").write_text(text, encoding="utf-8"), git(root, "commit", "-qam", "meanwhile", "--author=p <principal@seat>"))
    # the cost: a merge that brings twenty commits, each working on a tracker — read only because HEAD is a merge
    git(root, "switch", "-q", "-c", "pr/twenty")
    for n_ in range(920, 940):
        p_ = next((root / "docs/work-tracker").glob(f"AP-{n_}-*.md")); p_.write_text(p_.read_text() + f"\nWorked on in commit {n_}.\n", encoding="utf-8")
        git(root, "commit", "-qam", f"AP-{n_}: worked on", "--author=i <implementer@seat>")
    git(root, "switch", "-q", trunk_); move_("trunk moved\n"); git(root, "merge", "-q", "--no-ff", "pr/twenty", "-m", "Merge twenty")
    import time as _time
    t0_ = _time.perf_counter(); code, _, err = run(root, "--check"); took_ = _time.perf_counter() - t0_
    check(f"FM-019 · a merge that brings twenty commits is read commit by commit — `--check` passed in {took_:.2f} s", code == 0 and "this change is a" not in err)
    # (f) a close made by a seat that holds no `close`, without the hook, brought in by the principal's merge — which holds it
    git(root, "switch", "-q", "-c", "pr/f")
    p_ = next((root / "docs/work-tracker").glob("AP-901-*.md")); p_.write_text(p_.read_text().replace("status: In Progress", "status: Shipped"), encoding="utf-8")
    run(root); git(root, "add", "-A"); git(root, "commit", "-qm", "AP-901 shipped, no hook", "--author=i <implementer@seat>"); f_ = sha_()
    git(root, "switch", "-q", trunk_); move_("trunk moved again\n"); git(root, "merge", "-q", "--no-ff", "pr/f", "-m", "Merge pr/f")
    code, _, err = run(root, "--check")
    check("FM-019 · (f) a merge brings a close made by a seat without `close` — refused, naming THAT commit and its seat, not the merge that brought it",
          code == fm.EXIT_LINT and f"AP-901: in `{f_[:10]}` (implementer@seat), which the merge brings" in err and "which does not hold `close`" in err and sha_()[:10] not in err)
    # (e) an unsigned answer whose author is the signed owner's identity — a string anyone can type — brought in by a merge
    git(root, "switch", "-q", "-c", "pr/e")
    p_ = next((root / "docs/work-tracker").glob("AP-900-*.md"))
    p_.write_text(p_.read_text().replace('ask-proposal: "yes"\n', f'ask-proposal: "yes"\nanswer: "accepted - yes"\nanswered: {new_}\nanswered-by: holgo\n'), encoding="utf-8")
    git(root, "commit", "-qam", "AP-900: accepted, unsigned", "--author=holgo <h@x>"); e_ = sha_()
    git(root, "switch", "-q", trunk_); move_("and again\n"); git(root, "merge", "-q", "--no-ff", "pr/e", "-m", "Merge pr/e")
    code, _, err = run(root, "--check")
    check("FM-019 · (e) a merge brings an UNSIGNED answer under the signed owner's identity — refused, and the refusal names that commit, not the merge",
          code == fm.EXIT_LINT and f"the commit `{e_[:10]}` making a `answer` change does not verify as the seat `owner`" in err and sha_()[:10] not in err)
    rm_git(root)
fm.configure(HERE)

# --- FM-003: Windows, and Subversion with no git anywhere ---------------------------------------------------------
_TOOL = [sys.executable, str(HERE / "shoalmark.py")]
with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp).resolve(); (root / "shoalmark.toml").write_text('name = "w"\n[kinds]\nW = "Work"\n', encoding="utf-8")
    tracker(root, "W-001", title="a dash — an arrow → a half moon ◐")
    r = subprocess.run(_TOOL + ["--root", str(root), "--next"], capture_output=True, env={**os.environ, "PYTHONIOENCODING": "cp1252"})
    check("W2 · a console that cannot encode `—` `→` `◐` (cp1252, the Windows default) does not crash a run", r.returncode == 0 and b"Traceback" not in r.stderr)
    fm.configure(root)
    check("W3 · every message names an interpreter that exists where it ran — `python` on Windows, `python3` elsewhere — and a path it can be pasted with",
          fm.CMD.split()[0] == ("python" if os.name == "nt" else "python3") and "\\" not in fm.CMD.split()[0] and fm.PY == fm.CMD.split()[0])
fm.configure(HERE)

_src = (HERE / "shoalmark.py").read_text()
check("W1 · the tool names its encoding on every read, write and subprocess that returns text — a locale never decides what it reads",
      not re.search(r"\.read_text\(\)|\.write_text\(", _src) and all("encoding=" in c for c in re.findall(r"subprocess\.run\([^\n]*text=True[^\n]*(?:\n[^\n]*){0,1}", _src)))
_SVN = shutil.which("svn") and shutil.which("svnadmin")
if not _SVN:
    print("  skip  S1–S3 · Subversion is not installed here — these run in CI")
else:
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp).resolve(); svn = lambda *a, cwd=None: subprocess.run(["svn", *a], cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace")
        subprocess.run(["svnadmin", "create", str(base / "repo")], check=True)
        url = (base / "repo").as_uri()
        svn("mkdir", "-m", "layout", url + "/trunk"); svn("checkout", url + "/trunk", str(base / "wc")); root = base / "wc"
        run(root, "--init", "--key", "c2"); run(root, "--new", "Arbeitspaket 1")
        made = next((root / "docs/work-tracker").glob("C2-001-*.md")); made.write_text(made.read_text(encoding="utf-8").replace("considered:", "considered: none"), encoding="utf-8")
        code, _, _ = run(root)
        svn("add", "--force", ".", cwd=root); svn("commit", "-m", "C2-001", cwd=root)
        listed = svn("ls", "-R", url + "/trunk").stdout
        check("S1 · in a Subversion working copy with no git: init, a new tracker, the gate and INDEX.md work — and the first `svn add` already leaves the board out",
              code == 0 and not (root / ".git").exists() and not (root / ".gitignore").exists() and fm.vcs() == "svn" and "INDEX.md" in listed and "index.html" not in listed
              and (root / "docs/work-tracker/index.html").exists())
        contract = (root / "AGENTS.md").read_text(encoding="utf-8")
        check("S3 · the contract says the true thing for Subversion: run the tool before `svn commit` — its command line has no hook", "before every `svn commit`" in contract and "gate on every\ncommit" not in contract)
        svn("update", cwd=root); code, out, _ = run(root, "--install-hook")
        props = {p_: svn("propget", p_, ".", cwd=root).stdout for p_ in fm.TSVN_HOOKS}
        again = run(root, "--install-hook")[1]
        check("S2 · --install-hook wires what Subversion has: the two TortoiseSVN properties, by repository URL, four-line form — says the command line runs no hook, and is idempotent",
              code == 0 and all(v.startswith("python %REPOROOT%/trunk/") and f"--tsvn-hook {k}\ntrue\nhide" in v.replace("\r", "") for (p_, k), v in zip(fm.TSVN_HOOKS.items(), props.values()))
              and "runs no hook" in out and "set tsvn" not in again)
        svn("propset", "tsvn:precommithook", "wscript theirs.js\ntrue\nhide\n", ".", cwd=root)
        code, _, err = run(root, "--install-hook")
        check("S2 · a TortoiseSVN hook that is not ours is left alone, with the line to add", code == fm.EXIT_LINT and "left alone" in err and "theirs.js" in svn("propget", "tsvn:precommithook", ".", cwd=root).stdout)
        hook = lambda kind: subprocess.run([sys.executable, str(root / "tools/shoalmark/shoalmark.py"), "--tsvn-hook", kind, "C:/t/paths", "3", "C:/t/msg", "C:/wc"], cwd=tmp, capture_output=True, text=True, encoding="utf-8")
        fm.configure(HERE); run(HERE, "--vendor", str(root / "tools/shoalmark"), "--allow-untagged"); fm.configure(root)
        hook("start")                                           # the vendored copy names its own command in INDEX.md — it writes it first
        ok = hook("pre"); made.write_text(made.read_text(encoding="utf-8").replace("status: Proposed", "status: Bogus"), encoding="utf-8"); bad = hook("pre")
        made.write_text(made.read_text(encoding="utf-8").replace("status: Bogus", "status: In Progress"), encoding="utf-8"); start = hook("start")
        check("S2 · called as TortoiseSVN calls it — from anywhere, with its own arguments — `pre` refuses a violation and `start` writes the INDEX.md the dialog will list",
              ok.returncode == 0 and bad.returncode == fm.EXIT_LINT and "status" in bad.stdout + bad.stderr and start.returncode == 0 and "INDEX.md" in svn("status", cwd=root).stdout)
        svn("propdel", "tsvn:precommithook", ".", cwd=root); svn("commit", "-m", "in Arbeit", cwd=root); svn("update", cwd=root); fm._SVN_LOG = None
        check("S1 · a pass's *last worked on* comes from `svn log` — one call for the whole directory", fm.last_worked_on(made) == datetime.date.today().isoformat() or re.fullmatch(r"\d{4}-\d\d-\d\d", fm.last_worked_on(made)))
        # FM-008 · S4 · seats under Subversion: no signature to give and no client hook to run — the identity is the
        # SERVER'S, read from `svn blame`, and the layer that refuses is the server's own pre-commit hook
        wt_ = root / "docs/work-tracker"
        for id_, who_, q_ in (("C2-002", "stranger", "Soll der Starter zuerst?"), ("C2-003", "principal", "Soll der Import zuerst?")):
            (wt_ / f"{id_}-x.md").write_text(f'---\nid: {id_}\nstatus: In Progress\nconsidered: none\nnext: owner\nask: "{q_}"\n'
                                             f'ask-kind: ruling\nask-since: 2026-09-20\nask-proposal: "ja"\nhook: "h von {id_}"\n---\n\n'
                                             f'# {id_} — eine Frage\n\n## Was jetzt gilt\n\n**Offen.**\n\n## Fertig, wenn\n\nbeantwortet.\n', encoding="utf-8")
            run(root); svn("add", "--force", ".", cwd=root); svn("commit", "-m", id_, "--username", who_, cwd=root); svn("update", cwd=root)
        cfg = (root / "shoalmark.toml").read_text(encoding="utf-8")
        (root / "shoalmark.toml").write_text(cfg + '\n[seats]\nprincipal = "principal"\n', encoding="utf-8")
        code, _, err = run(root)
        check("S4 · under Subversion the seat is the server's account: the ask committed by an account that is no seat is refused, naming it — and the one from the seat that holds `ask` passes",
              code == fm.EXIT_LINT and "C2-002: `next: owner` puts a question in front of the Owner" in err and "`stranger` is not a seat" in err
              and "--worktree user.email" not in err and "C2-003" not in err)
        (root / "shoalmark.toml").write_text(cfg + '\n[seats]\nprincipal = "principal signed"\n', encoding="utf-8")
        code, _, err = run(root)
        check("S4 · `signed` under Subversion is refused as meaningless — the server authenticated the commit; name the account alone",
              code == fm.EXIT_LINT and "asks for a signature, and Subversion has none to give" in err and "Name the SVN account alone" in err)
        (root / "shoalmark.toml").write_text(cfg, encoding="utf-8")
        for id_ in ("C2-002", "C2-003"):
            (wt_ / f"{id_}-x.md").unlink()
        svn("delete", "--force", str(wt_ / "C2-002-x.md"), str(wt_ / "C2-003-x.md"), cwd=root); run(root)
    fm.configure(HERE)

# --- the rename: what the tool wrote under its old name is still its own ---------------------------------------
with tempfile.TemporaryDirectory() as d:
    root = Path(d).resolve()
    git(root, "init", "-q")
    (root / "AGENTS.md").write_text("# mine\n\n<!-- BEGIN fathom-mark: the work-tracker contract — regenerated by --init, edit outside these markers -->\nold rules\n<!-- END fathom-mark -->\n\nkept.\n")
    (root / ".git/hooks").mkdir(parents=True, exist_ok=True)
    (root / ".git/hooks/pre-commit").write_text("#!/bin/sh\n# fathom-mark — old hook\npython3 tools/fathom-mark/fathom_mark.py --print-written\n")
    run(root, "--init", "--key", "msr"); code, _, _ = run(root, "--install-hook")
    agents, hook = (root / "AGENTS.md").read_text(), (root / ".git/hooks/pre-commit").read_text()
    check("a contract block and a hook written under the old name are replaced, not stranded — the repository's own text is kept",
          code == 0 and "old rules" not in agents and "fathom-mark" not in agents and agents.count(fm.CONTRACT_BEGIN) == 1 and "kept." in agents and agents.startswith("# mine")
          and "fathom" not in hook and "shoalmark.py --print-written" in hook)
fm.configure(HERE)

# --- FM-031 S2: the queue in one view — every open pull request, ONE action, in the order the Owner takes them -------
def _no_git_env(f):
    """a direct call into the tool with the hook's `GIT_*` variables out of the way, as `run` does for main()"""
    saved = {k: os.environ.pop(k) for k in [k for k in os.environ if k.startswith("GIT_")]}
    try:
        return f()
    finally:
        os.environ.update(saved)


with tempfile.TemporaryDirectory() as d:
    root = Path(d).resolve()
    git(root, "init", "-q"); run(root, "--init", "--key", "msr")
    sha = lambda ref="HEAD": subprocess.run(["git", "-C", str(root), "rev-parse", ref], capture_output=True, text=True, env=_ENV).stdout.strip()
    def commit_(msg, files):
        for name, text in files.items():
            (root / name).parent.mkdir(parents=True, exist_ok=True); (root / name).write_text(text)
        git(root, "add", "-A"); git(root, "commit", "-q", "--allow-empty", "-m", msg)
        return sha()
    reviews_ = "docs/work-tracker/evidence/reviews/"
    base0 = commit_("the trunk", {"shared.txt": "one\n", "a.txt": "a\n"})
    git(root, "checkout", "-q", "-b", "r1"); w1 = commit_("the ready slice", {"a.txt": "a1\n"})
    v1 = commit_(f"review: the ready slice at {w1[:7]} — READY WITH FINDINGS (R1 P3)\n\nReviewed: {w1[:7]}", {reviews_ + "r.md": "R1\n"})
    h1 = commit_("session closes", {"docs/work-tracker/sessions.md": "| a | b |\n"})             # an addendum after the verdict
    git(root, "checkout", "-q", "-b", "r3", base0); c3 = commit_("the carried slice", {"c.txt": "c\n"})
    git(root, "checkout", "-q", "-b", "r5", base0); git(root, "cherry-pick", "-x", c3); h5 = commit_("more on top", {"e.txt": "e\n"})
    git(root, "checkout", "-q", "-b", "r4", base0); h4 = commit_("the conflicting slice", {"shared.txt": "four\n"})
    git(root, "checkout", "-q", "-b", "r6", base0); w6 = commit_("the refused slice", {"f.txt": "f\n"})
    h6 = commit_(f"review: at {w6[:7]} — NOT READY (R1 P2)\n\nReviewed: {w6}", {reviews_ + "r6.md": "R1\n"})
    git(root, "checkout", "-q", "-b", "r7", base0); w7 = commit_("the slice worked on after its verdict", {"g.txt": "g\n"})
    commit_(f"review: at {w7[:7]} — READY TO TAG\n\nReviewed: {w7}", {reviews_ + "r7.md": "ok\n"}); h7 = commit_("a fix after the verdict", {"g.txt": "g2\n"})
    git(root, "checkout", "-q", "-b", "trunk-now", base0); main_now = commit_("the trunk moved", {"shared.txt": "main\n"})
    git(root, "update-ref", "refs/remotes/origin/main", main_now)
    pr = lambda n, branch, head, at: {"number": n, "title": branch, "headRefName": branch, "headRefOid": head, "baseRefName": "main",
                                      "mergeable": "UNKNOWN", "mergeStateStatus": "UNKNOWN", "createdAt": f"2026-09-24T{at}:00Z"}
    prs = [pr(1, "fm/001-the-ready-slice-with-a-long-name-that-is-cut", h1, "08:00"), pr(2, "fm/002-inside", w1, "07:00"), pr(3, "fm/003-carried", c3, "07:30"),
           pr(5, "fm/005-carrier", h5, "06:00"), pr(4, "fm/004-conflict", h4, "05:00"), pr(6, "fm/006-refused", h6, "09:00"), pr(7, "fm/007-worked-on", h7, "04:00"),
           pr(9, "fm/009-twin", h6, "09:30")]
    fm.configure(root)
    rows_ = _no_git_env(lambda: fm.queue_actions(prs)) if hasattr(fm, "queue_actions") else []
    got_ = [(p_["number"], a_) for p_, _k, a_, _d in rows_]
    check(f"FM-031 S2 · each open pull request gets ONE action — merge on a READY verdict that only addenda follow · closes with the one whose head holds it · carried by patch · a conflict · NOT READY · no verdict on a head worked past its verdict · a twin closes with the older — actionable first, oldest first (saw {got_})",
          got_ == [(2, "closes with PR 1"), (3, "close: carried into PR 5"), (1, "merge"), (9, "closes with PR 6"),
                   (7, f"wait: no verdict on {h7[:7]}"), (4, "wait: conflict in shared.txt"), (5, f"wait: no verdict on {h5[:7]}"), (6, f"wait: NOT READY ({h6[:7]})")]
          and rows_[2][3] == f"verdict {v1[:7]} READY WITH FINDINGS")
    lines_ = fm.queue_lines(rows_) if hasattr(fm, "queue_lines") else [""]
    starts_ = {l_.index("fm/") for l_ in lines_[:-1]}
    check(f"FM-031 S2 · the queue prints one line per pull request, its columns aligned — `PR n  action  branch @ head  verdict` — a long branch cut, and one summary line last (saw {lines_[0]!r}, {lines_[-1]!r})",
          len(lines_) == len(prs) + 1 and len(starts_) == 1 and lines_[-1] == "8 waiting on you: 1 merge, 3 close, 4 wait, 0 pushed without a pull request"
          and re.fullmatch(r"PR 1 +merge +" + re.escape(prs[0]["headRefName"][:getattr(fm, "QUEUE_BRANCH_MAX", 32) - 1] + "…") + f" @ {h1[:7]} +verdict {v1[:7]} READY WITH FINDINGS", lines_[2]) is not None
          and re.fullmatch(rf"PR 2 +closes with PR 1 +fm/002-inside @ {w1[:7]}", lines_[0]) is not None)
    # the forge is never called here: no `origin`, a local `origin`, a GitHub `origin` and no `gh` — each one line, exit 3
    calls_ = argv_of(lambda: (run_safe(root, "--queue"), run(root, "--owner")))
    code, _, err = run_safe(root, "--queue")
    git(root, "remote", "add", "origin", str(root / "nowhere.git")); code2, _, err2 = run_safe(root, "--queue"); owner_ = run(root, "--owner")[1]
    git(root, "remote", "set-url", "origin", "git@github.com:someone/somewhere.git")
    real_which = fm.shutil.which; fm.shutil.which = lambda name, *a, **k: None if name == "gh" else real_which(name, *a, **k)
    try:
        calls_ += argv_of(lambda: run(root, "--owner")); code3, _, err3 = run_safe(root, "--queue")
    finally:
        fm.shutil.which = real_which
    check(f"FM-031 S2 · without the forge `--queue` says so in one line and exits 3 — no `origin`, an `origin` that is not GitHub, no `gh` — and `--owner` leaves the section out; `gh` is never called (saw {err.strip()!r}, {err2.strip()!r}, {err3.strip()!r})",
          (code, code2, code3) == (3, 3, 3) and "`origin` is not set" in err and "not on GitHub" in err2 and "no `gh` on PATH" in err3
          and all(len(e_.strip().splitlines()) == 1 for e_ in (err, err2, err3)) and "PULL REQUESTS" not in owner_ and not any(c_ and c_[0].endswith("gh") for c_ in calls_)
          and hasattr(fm, "github_remote") and fm.github_remote("git@github.com:holgo99/shoalmark.git") and fm.github_remote("https://github.com/a/b") and fm.github_remote("git@github-work:a/b.git")
          and not fm.github_remote("/tmp/github/b.git") and not fm.github_remote("ssh://git@gitlab.com/a/b") and not fm.github_remote(""))
fm.configure(HERE)

# --- FM-032 S4: the filing freeze — at `freeze_at` open trackers or more, `--new` files only a product defect ----------
with tempfile.TemporaryDirectory() as d:
    root = Path(d).resolve()
    git(root, "init", "-q"); run(root, "--init", "--key", "msr")
    cfg_ = root / "shoalmark.toml"; cfg_.write_text(cfg_.read_text().replace("triage_days = 7\n", "triage_days = 7\nfreeze_at = 2\n"))
    wt_ = root / "docs/work-tracker"
    tracker(root, "MSR-001"); tracker(root, "MSR-002", status="Shipped"); run(root)
    code, out, err = run(root, "--new", "a first thing that is not a defect")
    below_ = code == 0 and (wt_ / "MSR-003-a-first-thing-that-is-not-a-defect.md").exists()
    (wt_ / "MSR-003-a-first-thing-that-is-not-a-defect.md").unlink(); tracker(root, "MSR-003"); run(root)
    before_ = sorted(p_.name for p_ in wt_.glob("MSR-*.md"))
    code, out, err = run(root, "--new", "a second thing that is not a defect")
    check(f"FM-032 S4 · below the line `--new` files anything; at the line it refuses a filing without `bug` — exit 4, the count, the line, the rule's words — after the closest trackers, and writes nothing (saw {err.strip()!r})",
          below_ and code == fm.EXIT_LINT and "filing freeze — 2 open, at or above 2" in err
          and "only product defects are filed; anything else goes as one line into the closest open tracker's body, or waits" in err
          and "carries no `bug` tag" in err and sorted(p_.name for p_ in wt_.glob("MSR-*.md")) == before_ and ("closest trackers" in out or "Nothing related" in out))
    code_c, out_c, _ = run(root, "--check")
    (wt_ / "TEMPLATE.md").write_text(fm.TRACKER_TEMPLATE.replace("considered:\n", "considered:\ntags: bug\n"))
    code_b, _, _ = run(root, "--new", "the export drops the last row")
    (wt_ / "TEMPLATE.md").unlink()
    check(f"FM-032 S4 · `--check` says the freeze holds in one line, its exit unchanged; a filing that carries `tags: bug` passes the freeze (saw {code_c}, {code_b})",
          code_c == 0 and "filing freeze: 2 open, at or above 2 — only bug filings" in out_c and code_b == 0
          and "tags: bug" in next(wt_.glob("MSR-004-*.md")).read_text())
    before_ = sorted(p_.name for p_ in wt_.glob("MSR-*.md"))
    code_nb, _, err_nb = run_safe(root, "--new", "a process change", "--tags", "process")
    code_uk, _, err_uk = run_safe(root, "--new", "the importer drops a row", "--tags", "bug,defect")
    unwritten_ = sorted(p_.name for p_ in wt_.glob("MSR-*.md")) == before_
    code_tb, _, _ = run_safe(root, "--new", "the importer drops a row", "--tags", "bug, process,bug")
    tagged_ = next(iter(wt_.glob("MSR-005-*.md")), None)
    check(f"FM-032 S4 · `--new … --tags bug,process` writes `tags:` into the new tracker, deduplicated — a bug filing passes the freeze; a filing tagged `process` only is refused, and a tag outside [tags] is refused, before anything is written (saw {code_nb}, {code_uk}, {code_tb})",
          code_nb == fm.EXIT_LINT and "carries no `bug` tag" in err_nb and "--tags bug" in err_nb and code_uk == fm.EXIT_LINT and "defect not in the vocabulary" in err_uk
          and unwritten_ and code_tb == 0 and tagged_ is not None and fm.parse_frontmatter(tagged_.read_text())[0].get("tags") == "bug, process"
          and "--tags bug" in fm.render_schema())
    cfg_.write_text(cfg_.read_text().replace("freeze_at = 2\n", "freeze_at = 0\n")); code0, _, _ = run(root, "--new", "anything at all"); check0 = run(root, "--check")[1]
    cfg_.write_text(cfg_.read_text().replace("freeze_at = 0\n", "freeze_at = -1\n")); refused_ = not _try(lambda: fm.configure(root))
    cfg_.write_text(cfg_.read_text().replace("freeze_at = -1\n", ""))
    check("FM-032 S4 · `freeze_at = 0` is off, whatever is open; a negative number is refused by name; `--schema` documents the key",
          code0 == 0 and "filing freeze" not in check0 and refused_ and "`freeze_at`" in fm.render_schema() and "only a product defect" in fm.render_schema())
fm.configure(HERE)

# --- R4, R6: the freeze passes `freeze_tag`, and a `[tags]` without it freezes nothing; lone flags are refused -----
with tempfile.TemporaryDirectory() as d:
    root = Path(d).resolve()
    git(root, "init", "-q"); run(root, "--init", "--key", "msr")
    cfg_ = root / "shoalmark.toml"; base_cfg = cfg_.read_text()
    wt_ = root / "docs/work-tracker"
    cfg_.write_text(re.sub(r'(?m)^bug = .*\n', "", base_cfg).replace("triage_days = 7\n", "triage_days = 7\nfreeze_at = 1\n"))
    tracker(root, "MSR-001"); run(root)
    said_ = run(root, "--check")[1]; code_free, _, _ = run(root, "--new", "a process change while nothing can pass")
    cfg_.write_text(cfg_.read_text().replace("freeze_at = 1\n", 'freeze_at = 1\nfreeze_tag = "defect"\n') + 'defect = "the tool does wrong for the person using it"\n'); run(root)
    code_no, _, err_no = run(root, "--new", "another process change")
    code_yes, _, _ = run_safe(root, "--new", "the export drops a row", "--tags", "Defect")
    wrote_ = next(iter(wt_.glob("MSR-003-*.md")), None)
    check(f"R4 · with `freeze_at` set and no `freeze_tag` in [tags], `--check` says so in one line and the freeze refuses nothing; with `freeze_tag = \"defect\"` in [tags] the freeze holds and `--tags Defect` passes it, written as [tags] spells it (saw {said_.strip()[-160:]!r})",
          "filing freeze: off — `freeze_tag` 'bug' is not in [tags]" in said_ and code_free == 0
          and code_no == fm.EXIT_LINT and "carries no `defect` tag" in err_no and "--tags defect" in err_no
          and code_yes == 0 and wrote_ is not None and fm.parse_frontmatter(wrote_.read_text())[0].get("tags") == "defect"
          and "`freeze_tag`" in fm.render_schema())
    code_t, _, err_t = run_safe(root, "--tags", "bug"); code_s, _, err_s = run_safe(root, "--supersede"); code_e, _, err_e = run_safe(root, "--new", "x", "--tags", " , ")
    check(f"R6 · `--tags` without `--new` and `--supersede` without `--answer` are refused in one line, exit 2; an empty `--tags` says no tag was given (saw {err_t.strip()!r}, {err_s.strip()!r})",
          (code_t, code_s) == (2, 2) and len(err_t.strip().splitlines()) == 1 and len(err_s.strip().splitlines()) == 1
          and "--tags goes with --new" in err_t and "--supersede goes with --answer" in err_s and code_e == fm.EXIT_LINT and "no tag was given" in err_e)
fm.configure(HERE)

# --- RV-479: a spent `answer/<id>` is cut fresh, an unmerged one is never deleted; the run goes back where it started;
#     an answer is revoked or superseded, never overwritten in place, and the one it replaces moves into the ship log ---
with tempfile.TemporaryDirectory() as tmp:
    base = Path(tmp).resolve(); root = base / "wc"; root.mkdir()
    subprocess.run(["git", "init", "-q", "--bare", str(base / "origin.git")], check=True, env=_ENV); subprocess.run(["git", "init", "-q", str(root)], check=True, env=_ENV)
    for k_, v_ in (("user.name", "holgo"), ("user.email", "h@x"), ("commit.gpgsign", "false")):
        git(root, "config", k_, v_)
    git(root, "remote", "add", "origin", str(base / "origin.git"))
    (root / "shoalmark.toml").write_text('name = "s"\nanswerers = ["holgo"]\n[kinds]\nAP = "Work"\n', encoding="utf-8")
    since_ = (datetime.date.today() - datetime.timedelta(days=2)).isoformat()
    ask_ = lambda q: f'next: owner\nask: "{q}"\nask-kind: ruling\nask-since: {since_}\nask-proposal: "yes"\n'
    ap80 = tracker(root, "AP-080", extra=ask_("Ship the importer first?"), title="the ask",
                   body="## What is true now\n\n**One thing is left.**\n\n## Done when\n\nit is.\n\n## Ship log\n\n| Date | Event |\n|---|---|\n| 2026-09-20 | Filed. |\n")
    run(root); git(root, "add", "-A"); git(root, "commit", "-qm", "the ask"); git(root, "push", "-q", "-u", "origin", "HEAD:main")
    here_ = lambda: subprocess.run(["git", "-C", str(root), "branch", "--show-current"], capture_output=True, text=True, env=_ENV).stdout.strip()
    at_ = lambda ref, path="docs/work-tracker/AP-080-x.md": subprocess.run(["git", "-C", str(root), "show", f"{ref}:{path}"], capture_output=True, text=True, env=_ENV).stdout
    trunk_ = here_()
    code1, out1, _ = run(root, "--answer", "AP-080", "accept", "the importer")
    first_ = subprocess.run(["git", "-C", str(root), "rev-parse", "answer/ap-080"], capture_output=True, text=True, env=_ENV).stdout.strip()
    code2, _, err2 = run(root, "--answer", "AP-080", "accept", "again")
    check(f"RV-479 · after the push `--answer` goes back to the branch it started on; a second one while `answer/<id>` is not merged is refused — exit 4, the branch named with the one command that clears it — and the branch is kept (saw {err2.strip()[:200]!r})",
          code1 == 0 and here_() == trunk_ and f"back on `{trunk_}`" in out1 and code2 == fm.EXIT_LINT and "`answer/ap-080` exists and is not merged into `origin/main`" in err2
          and "`git branch -D answer/ap-080`" in err2 and subprocess.run(["git", "-C", str(root), "rev-parse", "answer/ap-080"], capture_output=True, text=True, env=_ENV).stdout.strip() == first_
          and here_() == trunk_)
    git(root, "merge", "-q", "--no-ff", "-m", "the Owner merges his answer", "answer/ap-080"); git(root, "push", "-q", "origin", f"{trunk_}:main"); git(root, "fetch", "-q", "origin")
    # he takes it back: revoke, on the tracker that carries the answer — the spent branch is cut fresh, the old answer kept
    code3, out3, err3 = run(root, "--answer", "AP-080", "revoke", "the importer waits for the audit")
    after_ = at_("answer/ap-080"); fm_after = fm.parse_frontmatter(after_)[0]
    row_ = f'| {datetime.date.today().isoformat()} | Answer of {datetime.date.today().isoformat()} superseded: *"accepted - the importer"* ({first_[:7]}) — revoked: the importer waits for the audit |'
    check(f"RV-479 · a merged `answer/<id>` left from an earlier answer is deleted and cut fresh, said in one line; `revoke \"<reason>\"` writes `revoked - <reason>` and moves the answer it replaces into the ship log, newest on top, with the commit that wrote it (saw {err3.strip()[:160]!r})",
          code3 == 0 and "`answer/ap-080` was left by an earlier answer and is merged into `origin/main` — deleted, and cut fresh" in err3 and here_() == trunk_
          and fm_after.get("answer") == '"revoked - the importer waits for the audit"' and after_.count("\nanswer:") == 1 and after_.count("\nanswered:") == 1
          and after_.split("|---|---|\n")[1].startswith(row_ + "\n| 2026-09-20 | Filed. |"))
    git(root, "merge", "-q", "--no-ff", "-m", "the revocation merged", "answer/ap-080"); git(root, "push", "-q", "origin", f"{trunk_}:main"); git(root, "fetch", "-q", "origin")
    revoked_ = subprocess.run(["git", "-C", str(root), "log", "-1", "--format=%h", "answer/ap-080"], capture_output=True, text=True, env=_ENV).stdout.strip()[:7]
    code4, _, err4 = run(root, "--answer", "AP-080", "reject", "not this quarter")
    code5, out5, _ = run_safe(root, "--answer", "AP-080", "accept", "the exporter instead", "--supersede")
    git(root, "switch", "-q", "answer/ap-080"); fm.configure(root); t_ = next(t for t in fm.load_trackers() if t["id"] == "AP-080"); gate_ = run(root)[0]
    page_ = (root / "docs/work-tracker/index.html").read_text(encoding="utf-8") if run(root, "--html-only")[0] == 0 else ""
    check(f"RV-479 · without `--supersede` an answered ask is refused, naming both forms; `--supersede` replaces the answer, the replaced one in the ship log, and the board's row says which commit it supersedes (saw {t_.get('supersedes')!r}, {revoked_!r})",
          code4 == fm.EXIT_LINT and "answered already" in err4 and "revoke" in err4 and "--supersede" in err4
          and code5 == 0 and t_["answer"] == "accepted - the exporter instead" and t_.get("supersedes") == revoked_ and gate_ == 0
          and f'superseded: *"revoked - the importer waits for the audit"* ({revoked_}) — replaced by: *"accepted - the exporter instead"*' in ap80.read_text()
          and f'"accepted - the exporter instead", "yes", [], [], "{datetime.date.today().isoformat()}", "holgo", "{revoked_}", ["changed", 0, ""]]' in page_ and 'l("viewer.supersedes"' in page_)
    git(root, "switch", "-q", trunk_)
    tracker(root, "AP-081", extra=ask_("Ship the exporter?"), title="unanswered"); run(root); git(root, "add", "-A"); git(root, "commit", "-qm", "a second ask")
    code7, _, err7 = run(root, "--answer", "AP-081", "revoke", "nothing to take back"); code8, _, err8 = run_safe(root, "--answer", "AP-081", "accept", "--supersede")
    check("RV-479 · `revoke` and `--supersede` on an ask with no answer are refused — there is nothing to replace; a revocation without its reason too",
          code7 == fm.EXIT_LINT and "carries no answer to revoke" in err7 and code8 == fm.EXIT_LINT and "carries no answer to supersede" in err8
          and run(root, "--answer", "AP-080", "revoke")[0] == fm.EXIT_LINT)
    rm_git(root)
fm.configure(HERE)

# --- FM-030, 0.18.3 (the Auditor seat's check 24): the answer writes the next move — `build` after a ruling, a
#     determination or a ceremony; `owner` kept for an action, whose act is still his; revoke and supersede still work --
with tempfile.TemporaryDirectory() as tmp:
    base = Path(tmp).resolve(); root = base / "wc"; root.mkdir()
    subprocess.run(["git", "init", "-q", "--bare", str(base / "origin.git")], check=True, env=_ENV); subprocess.run(["git", "init", "-q", str(root)], check=True, env=_ENV)
    for k_, v_ in (("user.name", "holgo"), ("user.email", "h@x"), ("commit.gpgsign", "false")):
        git(root, "config", k_, v_)
    git(root, "remote", "add", "origin", str(base / "origin.git"))
    (root / "shoalmark.toml").write_text('name = "s"\nanswerers = ["holgo"]\n[kinds]\nAP = "Work"\n', encoding="utf-8")
    since_ = (datetime.date.today() - datetime.timedelta(days=1)).isoformat()
    ask_ = lambda q, kind: f'next: owner\nask: "{q}"\nask-kind: {kind}\nask-since: {since_}\nask-proposal: "yes"\n'
    log_ = "## What is true now\n\n**One thing is left.**\n\n## Done when\n\nit is.\n\n## Ship log\n\n| Date | Event |\n|---|---|\n| 2026-09-20 | Filed. |\n"
    tracker(root, "AP-095", extra=ask_("Ship the importer first?", "ruling"), title="a ruling", body=log_)
    tracker(root, "AP-096", extra=ask_("Will you rotate the key this week?", "action"), title="an action", body=log_)
    tracker(root, "AP-097", extra=ask_("Is the read on production clean?", "determination"), title="a determination", body=log_)
    run(root); git(root, "add", "-A"); git(root, "commit", "-qm", "the asks"); git(root, "push", "-q", "-u", "origin", "HEAD:main")
    trunk_ = subprocess.run(["git", "-C", str(root), "branch", "--show-current"], capture_output=True, text=True, env=_ENV).stdout.strip()
    def land_(tid):                                        # the Owner merges his answer, and origin has it
        git(root, "merge", "-q", "--no-ff", "-m", f"the Owner merges {tid}", f"answer/{tid.lower()}"); git(root, "push", "-q", "origin", f"{trunk_}:main"); git(root, "fetch", "-q", "origin")
    front_ = lambda tid: fm.parse_frontmatter((root / f"docs/work-tracker/{tid}-x.md").read_text())[0]
    said_, diff_ = {}, {}
    for tid_ in ("AP-095", "AP-096", "AP-097"):
        said_[tid_] = run(root, "--answer", tid_, "accept")
        diff_[tid_] = subprocess.run(["git", "-C", str(root), "show", "--format=", f"answer/{tid_.lower()}"], capture_output=True, text=True, env=_ENV).stdout
        land_(tid_)
    after_ = {tid_: front_(tid_) for tid_ in said_}
    check(f"FM-030 · the answer writes the next move in its own commit — a ruling and a determination read `next: build`, the seat's move; an action keeps `next: owner`, the act still his — and the run says which (saw {[a_.get('next') for a_ in after_.values()]})",
          all(c_ == 0 for c_, _o, _e in said_.values()) and after_["AP-095"].get("next") == "build" and after_["AP-097"].get("next") == "build"
          and after_["AP-096"].get("next") == "owner" and all(a_.get("answer") == '"accepted"' for a_ in after_.values())
          and "\n  next: build — the seat's move follows" in said_["AP-095"][1] and "\n  next: owner — an action: the act is still yours" in said_["AP-096"][1]
          and "+next: build" in diff_["AP-095"] and "-next: owner" in diff_["AP-095"] and '+answer: "accepted' in diff_["AP-095"]
          and "next:" not in diff_["AP-096"] and '+answer: "accepted' in diff_["AP-096"] and "+next: build" in diff_["AP-097"])
    code_r, _o, err_r = run(root, "--answer", "AP-095", "revoke", "the audit comes first"); land_("AP-095")
    code_s, _o, err_s = run_safe(root, "--answer", "AP-096", "accept", "next week", "--supersede"); land_("AP-096")
    code_n, _o, err_n = run(root, "--answer", "AP-097", "accept", "again")
    r95_, r96_ = front_("AP-095"), front_("AP-096")
    check(f"FM-030 · revoke and --supersede key on the answer being there, not on `next: owner` — both work after the move is written, and keep it; an answered ask without either is still refused (saw {err_r.strip()[-160:]!r}, {err_s.strip()[-160:]!r})",
          code_r == 0 and r95_.get("answer") == '"revoked - the audit comes first"' and r95_.get("next") == "build"
          and code_s == 0 and r96_.get("answer") == '"accepted - next week"' and r96_.get("next") == "owner"
          and code_n == fm.EXIT_LINT and "answered already" in err_n and run(root)[0] == 0 and run(root, "--check")[0] == 0)      # INDEX.md lists the accepted action (FM-030 B): regenerated, as the hook does
    tracker(root, "AP-098", extra='ask: "A question nobody put to him?"\nask-kind: ruling\nnext: build\n', title="not asked", body=log_)
    git(root, "add", "-A"); git(root, "commit", "-qm", "an ask line with another move")
    code_a, _o, err_a = run(root, "--answer", "AP-098", "accept"); code_b, _o, err_b = run(root, "--answer", "AP-099", "accept")
    check(f"FM-030 · an unanswered `ask:` whose move is not `owner` is not the Owner's to answer, and says so; no `ask:` at all still reads *asks the Owner nothing* (saw {err_a.strip()!r})",
          code_a == fm.EXIT_LINT and "carries an `ask:` and `next: build`" in err_a and code_b == fm.EXIT_LINT and "asks the Owner nothing" in err_b)
    schema_ = fm.render_schema()
    check("FM-030 · `--schema`: `next:` says what an answer writes, and `ask-kind:` that an ask whose yes needs the Owner's hands is `action`, whatever else it decides",
          "`--answer` writes it with the answer: `build` for a ruling, a determination or a ceremony" in schema_ and "`owner` kept for an action" in schema_
          and "An ask whose yes needs the Owner's hands is `action`, whatever else it decides" in schema_)
    rm_git(root)
fm.configure(HERE)

# --- FM-033's second answer, 0.18.3 (AU-16): a raise naming a signed rule re-judges the tracker the same day ---------------
# A raise is a line under `## Raised`, dated, naming what it undermines. Dated after the tracker's judgement and naming a
# line of the current path or a signed answer, it puts the tracker under triage and on the next worksheet, marked RAISED.
with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp).resolve()
    git(root, "init", "-q")
    (root / "shoalmark.toml").write_text('name = "r"\n[kinds]\nAP = "Work"\n', encoding="utf-8")
    d_ = lambda n: (datetime.date.today() - datetime.timedelta(days=n)).isoformat()
    wt_ = root / "docs/work-tracker"; wt_.mkdir(parents=True)
    (wt_ / "TRIAGE.md").write_text("# Triage\n\n## The intent\n\n- **for** people who build with agents\n\n## The current path\n\n1. The sitting runs on a tagged release.\n"
                                   "2. What a sitting finds is filed that day.\n3. A review's evidence is checked, not asked.\n4. Trust is earned first.\n"
                                   "5. An answer is written and signed through the board.\n\n## Passes\n\nNewest first.\n", encoding="utf-8")
    raise_ = lambda day, what: f"## Raised\n\n- {day} · Auditor (8b91dba2), through the Owner · the key signs without a touch — ssh-add -l · undermines: {what}\n\n"
    judged_ = lambda day, status="Proposed": f"triaged: {day}\ntier: P2\n"
    body_ = lambda raised: "## What is true now\n\n**One thing is left.**\n\n" + raised + "## Done when\n\nit is.\n"
    tracker(root, "AP-210", status="Proposed", extra="next: build\n" + judged_(d_(3)), title="answered",      # his answer, cleared into the record
            body=body_(f"## Asks\n\n**{d_(3)}** · Which key signs?\n**answered** — accepted - a hardware key · holgo\n**relation** — accepted the proposal\n\n"))
    tracker(root, "AP-201", status="Proposed", extra=judged_(d_(1)), title="FM-007's shape", body=body_(raise_(d_(0), "TRIAGE.md path 5, AP-210's answer")))
    tracker(root, "AP-202", status="Proposed", extra=judged_(d_(1)), title="no signed rule", body=body_(raise_(d_(0), "the shadow week")))
    tracker(root, "AP-203", status="Proposed", extra=judged_(d_(1)), title="raised before", body=body_(raise_(d_(2), "path 5")))
    tracker(root, "AP-204", status="Proposed", extra=judged_(d_(0)), title="the same day", body=body_(raise_(d_(0), "path 5")))
    tracker(root, "AP-205", status="Proposed", extra=judged_(d_(1)), title="no such rule", body=body_(raise_(d_(0), "path 9, AP-299's answer")))
    tracker(root, "AP-206", status="Shipped", extra=judged_(d_(1)), title="done", body=body_(raise_(d_(0), "path 5")))
    tracker(root, "AP-207", status="In Progress", extra=judged_(d_(1)), title="the token mid-line",
            body=body_(f"## Raised\n\n- {d_(0)} · undermines: path 1 · Auditor · the release was\n  not tagged · git tag -l\n\n"))
    run(root)
    fm.configure(root); by_ = {t["id"]: t for t in fm.load_trackers()}
    boards_ = {k: fm.board(t) for k, t in by_.items()}
    index_ = (wt_ / "INDEX.md").read_text(encoding="utf-8")
    check(f"FM-033 · a raise dated after the judgement that names a signed rule — a line of the current path, a tracker's answer — makes the tracker owed a pass and puts it under triage, INDEX.md too (saw {boards_})",
          fm.owed_a_pass(by_["AP-201"]) and boards_["AP-201"] == "triage" and re.search(r"^\| \[AP-201\].*\| triage \|", index_, re.M) is not None
          and [r_["undermines"] for r_ in by_["AP-201"]["raises"]] == [["TRIAGE.md path 5", "AP-210's answer"]])
    check("FM-033 · and nothing else does: a raise naming no signed rule, one dated before the judgement, one on the judgement's own day (a day decides), a path line or an answer that is not there, a raise on done work",
          all(not fm.owed_a_pass(by_[k]) for k in ("AP-202", "AP-203", "AP-204", "AP-205")) and boards_["AP-202"] == boards_["AP-203"] == boards_["AP-204"] == boards_["AP-205"] == "backlog"
          and boards_["AP-206"] == "done" and not by_["AP-206"]["raised"])
    check("FM-033 · the raise line is keyed on its date and its `undermines:` token wherever it sits — never on a count of fields — and a wrapped bullet is read whole",
          boards_["AP-207"] == "triage" and by_["AP-207"]["raises"][0]["undermines"] == ["path 1"] and by_["AP-207"]["raises"][0]["line"].endswith("not tagged · git tag -l"))
    code_, out_, _ = run(root, "--triage")
    sheet_ = (wt_ / "evidence/triage" / f"triage-{d_(0)}.md").read_text(encoding="utf-8")
    row_ = next((l for l in sheet_.splitlines() if l.startswith("| [AP-201]")), "")
    check(f"FM-033 · `--triage` lists the raised tracker, judged yesterday, with RAISED in its keep-test cell and the raise in its Now cell — and prints the rule in the Owner's words (saw {row_[:220]!r})",
          code_ == 0 and "· RAISED |" in row_ and f"| {d_(0)} · Auditor (8b91dba2), through the Owner · the key signs without a touch — ssh-add -l · undermines: TRIAGE.md path 5, AP-210's answer |" in row_
          and not any(l.startswith(f"| [{k}]") for l in sheet_.splitlines() for k in ("AP-202", "AP-203", "AP-204", "AP-205", "AP-206"))
          and "a raise naming a signed rule re-judges the tracker the same day; any" in out_ and "other raise waits for the next pass" in out_)
    (wt_ / "evidence/triage" / f"triage-{d_(0)}.md").write_text(sheet_.replace(row_, row_[: -len(" | | |")] + " | keep P2 | re-judged on the raise |") if row_.endswith(" | | |") else sheet_, encoding="utf-8")
    code2_, _o, err2_ = run(root, "--triage")
    fm.configure(root); t201_ = next(t for t in fm.load_trackers() if t["id"] == "AP-201")
    check(f"FM-033 · the pass that re-judges it dates it today, and the raise no longer re-opens it (saw {t201_.get('triaged')!r}, {err2_.strip()[-160:]!r})",
          code2_ == 0 and t201_.get("triaged") == d_(0) and not t201_["raised"] and fm.board(t201_) == "backlog")
    rm_git(root)
fm.configure(HERE)

# --- FM-030, 0.18.4 A: an act owed to the Owner has a time — `due:`, an ISO time with its zone; `window:` in minutes -------
with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp).resolve()
    git(root, "init", "-q")
    (root / "shoalmark.toml").write_text('name = "a"\nanswerers = ["holgo"]\n[kinds]\nAP = "Work"\n', encoding="utf-8")
    since_ = (datetime.date.today() - datetime.timedelta(days=1)).isoformat()
    act_ = f'next: owner\nask: "Will you read production at seven?"\nask-kind: action\nask-since: {since_}\nask-proposal: "yes, at seven"\n'
    good_ = tracker(root, "AP-400", extra=act_ + "due: 2026-09-26T07:30:00+02:00\nwindow: 90\n", title="a read at seven")
    tracker(root, "AP-401", extra="next: run\ndue: 2026-09-26T05:30Z\n", title="UTC, no seconds")
    code_ok, _o, err_ok = run(root)
    bad_ = {v: None for v in ("tomorrow", "2026-09-26 07:30", "2026-09-26T07:30", "2026-13-01T07:30+02:00", "2026-09-26T07:30Z+02:00")}
    for v in bad_:
        tracker(root, "AP-402", extra=f"next: build\ndue: {v}\n", title="a bad time")
        code_, _o, err_ = run(root)
        bad_[v] = (code_, err_)
    tracker(root, "AP-402", extra='next: build\nwindow: an hour\ndone: "yesterday · somewhere"\n', title="a bad window and a bad done")
    code_w, _o, err_w = run(root)
    check(f"FM-030 · A · `due:` is an ISO time with its zone — with or without seconds, `Z` for UTC — and `window:` minutes: the gate passes them (saw {err_ok.strip()[-160:]!r})",
          code_ok == 0 and fm.parse_due("2026-09-26T05:30Z") == datetime.datetime(2026, 9, 26, 5, 30, tzinfo=datetime.timezone.utc))
    check(f"FM-030 · A · the gate refuses a malformed `due:` — a word, a space for the T, no zone, a month that is not, two zones — and a `window:` or `done:` that is not its shape (saw {[e_.strip()[-90:] for _c, e_ in bad_.values()]})",
          all(c_ == fm.EXIT_LINT and "AP-402: `due:`" in e_ for c_, e_ in bad_.values())
          and "names no real time" in bad_["2026-13-01T07:30+02:00"][1] and "names no real time" in bad_["2026-09-26T07:30"][1]
          and code_w == fm.EXIT_LINT and "AP-402: `window:`" in err_w and "AP-402: `done:`" in err_w)
    tracker(root, "AP-402", extra="next: build\n", title="fixed")
    good_.write_text(good_.read_text().replace('ask-proposal: "yes, at seven"\n', f'ask-proposal: "yes, at seven"\nanswer: "accepted"\nanswered: {since_}\nanswered-by: holgo\n'))
    git(root, "add", "-A"); git(root, "commit", "-qm", "an act owed, answered")
    code_c, _o, _e = run(root, "--clear-ask", "AP-400", "wait")
    front_ = fm.parse_frontmatter(good_.read_text())[0]
    schema_ = fm.render_schema()
    check("FM-030 · A · `--clear-ask` leaves `due:` and `window:`: the answer was a promise, the act is still owed; `--schema` says who writes each and what it means",
          code_c == 0 and front_.get("due") == "2026-09-26T07:30:00+02:00" and front_.get("window") == "90" and "answer" not in front_
          and all(f"| `{k}:` |" in schema_ for k in ("due", "window", "done")) and "the Owner's `--due` moves it" in schema_ and "the Owner's `--done`" in schema_)
    rm_git(root)
fm.configure(HERE)

# --- FM-030, 0.18.4 B: the acts owed to the Owner are on his board with their time — due, overdue, missed — and in INDEX.md
#     as written, with no clock -------------------------------------------------------------------------------------------
with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp).resolve()
    git(root, "init", "-q")
    (root / "shoalmark.toml").write_text('name = "b"\nanswerers = ["holgo"]\n[kinds]\nAP = "Work"\n', encoding="utf-8")
    now_ = datetime.datetime.now(datetime.timezone.utc).astimezone().replace(microsecond=0)
    at_ = lambda minutes: (now_ + datetime.timedelta(minutes=minutes)).isoformat()
    since_ = (datetime.date.today() - datetime.timedelta(days=1)).isoformat()
    ask_ = lambda q, kind, answer: (f'next: owner\nask: "{q}"\nask-kind: {kind}\nask-since: {since_}\nask-proposal: "yes"\n'
                                   + (f'answer: "{answer}"\nanswered: {since_}\nanswered-by: holgo\n' if answer else ""))
    tracker(root, "AP-410", extra=ask_("Will you set up the key this week?", "action", "accepted - after the scoring"), title="promised, no date")
    tracker(root, "AP-411", extra=f"next: run\ndue: {at_(24 * 60)}\n", title="a read tomorrow")
    tracker(root, "AP-412", extra=f"next: run\ndue: {at_(-10)}\nwindow: 60\n", title="a read ten minutes ago")
    tracker(root, "AP-413", extra=f"next: run\ndue: {at_(-120)}\nwindow: 30\n", title="a read two hours ago")
    tracker(root, "AP-414", extra=ask_("Will you rotate the token?", "action", "rejected - not this quarter"), title="refused")
    tracker(root, "AP-415", extra=ask_("Which week?", "ruling", "accepted"), title="a ruling")
    tracker(root, "AP-416", extra=f'next: run\ndue: {at_(-120)}\ndone: "{at_(-100)} · evidence/AP-416/read.md"\n', title="done")
    tracker(root, "AP-417", status="Shipped", extra=f"due: {at_(-120)}\n", title="shipped")
    run(root); git(root, "add", "-A"); git(root, "commit", "-qm", "the acts", "--author=holgo <h@x>")
    code_, _o, err_ = run(root)
    fm.configure(root); by_ = {t["id"]: t for t in fm.load_trackers()}
    acts_ = {k: fm.act_of(t) for k, t in by_.items()}
    check(f"FM-030 · B · an act is owed where an action ask was accepted or a `due:` is set — not after a rejection, not for a ruling, not once `done:` is written, not on closed work (saw {sorted(k for k, a in acts_.items() if a)})",
          code_ == 0 and sorted(k for k, a in acts_.items() if a) == ["AP-410", "AP-411", "AP-412", "AP-413"]
          and acts_["AP-410"] == ("Will you set up the key this week?", "accepted - after the scoring", since_, "", 60) and acts_["AP-413"][4] == 30)
    index_ = (root / "docs/work-tracker/INDEX.md").read_text(encoding="utf-8")
    run(root); again_ = (root / "docs/work-tracker/INDEX.md").read_text(encoding="utf-8")
    check("FM-030 · B · INDEX.md lists the acts with their time as written — no due, overdue or missed, which need a clock — so a minute passing changes nothing committed",
          "### Acts owed to the Owner — with their time" in index_ and f"| [AP-412](AP-412-x.md) | a read ten minutes ago | — | {at_(-10).replace('T', ' ')} | 60 min |" in index_
          and f"| [AP-410](AP-410-x.md) | Will you set up the key this week? | {since_}: accepted - after the scoring | no date yet | 60 min |" in index_
          and "AP-414" not in (table_ := index_.split("### Acts owed")[1].split("\n## ")[0]) and not re.search(r"^\|.*\b(overdue|missed)\b", table_, re.M)
          and fm.drift_normalize(again_) == fm.drift_normalize(index_))
    page_ = (root / "docs/work-tracker/index.html").read_text(encoding="utf-8")
    check("FM-030 · B · the page carries each act in its row and the second clock rule beside the first, in the words of its labels — English built in, German in the table the tool ships",
          f'["Will you set up the key this week?", "accepted - after the scoring", "{since_}", "", 60]]' in page_ and "actstate=a=>" in page_
          and '"acts.missed": "missed — due {0}, and {1} minutes passed with no result"' in page_
          and "acts.missed" in fm.read_flat((HERE / "examples/de/labels.yaml").read_text(encoding="utf-8")))
    if _CHROME:
        dom_ = subprocess.run([_CHROME, "--headless=new", "--disable-gpu", *_CHROME_FLAGS, "--virtual-time-budget=4000", "--dump-dom", (root / "docs/work-tracker/index.html").as_uri()],
                              capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60).stdout
        shown_ = re.sub(r"\s+", " ", re.sub(r"<(script|style)[\s\S]*?</\1>|<[^>]+>", " ", dom_))
        acts_shown_ = shown_[shown_.find("your acts"):shown_.find(" id tier status ")]
        check(f"FM-030 · B · rendered, his board lists his acts after the questions: no date yet, due, overdue, missed — each by the clock, each with its time (saw {shown_[shown_.find('your acts'):][:420]!r})",
              "your acts, with their time: 4" in shown_ and "AP-410 Will you set up the key this week? · promised " + since_ + ": accepted - after the scoring · no date yet" in shown_
              and f"AP-411 a read tomorrow · due {at_(24 * 60).replace('T', ' ')}" in shown_ and f"AP-412 a read ten minutes ago · overdue — due {at_(-10).replace('T', ' ')}" in shown_
              and f"AP-413 a read two hours ago · missed — due {at_(-120).replace('T', ' ')}, and 30 minutes passed with no result" in shown_
              and "AP-414" not in acts_shown_ and "AP-415" not in acts_shown_ and "AP-416" not in acts_shown_ and "AP-417" not in acts_shown_)
    rm_git(root)
fm.configure(HERE)

# --- FM-031: a branch pushed without a pull request is in the queue too, read the same way — no `gh` needed for it ---
with tempfile.TemporaryDirectory() as tmp:
    base = Path(tmp).resolve(); root = base / "wc"; root.mkdir()
    subprocess.run(["git", "init", "-q", "--bare", str(base / "origin.git")], check=True, env=_ENV); subprocess.run(["git", "init", "-q", str(root)], check=True, env=_ENV)
    git(root, "remote", "add", "origin", str(base / "origin.git")); run(root, "--init", "--key", "msr")
    sha = lambda ref="HEAD": subprocess.run(["git", "-C", str(root), "rev-parse", ref], capture_output=True, text=True, env=_ENV).stdout.strip()
    def commit_(msg, files):
        for name, text in files.items():
            (root / name).parent.mkdir(parents=True, exist_ok=True); (root / name).write_text(text)
        git(root, "add", "-A"); git(root, "commit", "-q", "--allow-empty", "-m", msg)
        return sha()
    t0 = commit_("the trunk", {"shared.txt": "one\n"}); git(root, "branch", "-q", "-M", "main")
    subprocess.run(["git", "--git-dir", str(base / "origin.git"), "symbolic-ref", "HEAD", "refs/heads/main"], check=True, env=_ENV)
    branch_ = lambda name, msg, files, frm="main": (git(root, "checkout", "-q", "-b", name, frm), commit_(msg, files))[1]
    merged = branch_("b-merged", "merged work", {"m.txt": "m\n"}); git(root, "checkout", "-q", "main"); git(root, "merge", "-q", "--ff-only", "b-merged")
    ans = branch_("answer/msr-001", "an answer", {"a.txt": "a\n"})
    in_pr = branch_("b-pr", "the open pull request's work", {"p.txt": "p\n"}); inner = sha("HEAD")
    pr_head = commit_("more on the open pull request", {"p.txt": "p2\n"})
    git(root, "checkout", "-q", "-b", "b-inside", inner)
    none_ = branch_("b-none", "work nobody opened", {"n.txt": "n\n"}); git(root, "branch", "b-inner", none_)
    none_ = commit_("more work nobody opened", {"n.txt": "n2\n"}); git(root, "branch", "b-twin", none_)     # R2: inside b-none, and b-none's twin
    w_ = branch_("b-ready", "reviewed work", {"r.txt": "r\n"})
    ready = commit_(f"review: at {w_[:7]} — READY WITH FINDINGS (R1 P3)\n\nReviewed: {w_}", {"docs/work-tracker/evidence/reviews/r.md": "R1\n"})
    clash = branch_("b-conflict", "conflicting work", {"shared.txt": "two\n"}, frm=t0)
    git(root, "checkout", "-q", "main"); commit_("the trunk moves", {"shared.txt": "three\n"})
    git(root, "push", "-q", "origin", "main", "b-merged", "answer/msr-001", "b-pr", "b-inside", "b-none", "b-inner", "b-twin", "b-ready", "b-conflict"); git(root, "fetch", "-q", "origin")
    prs = [{"number": 7, "title": "b-pr", "headRefName": "b-pr", "headRefOid": pr_head, "baseRefName": "main", "mergeable": "UNKNOWN", "mergeStateStatus": "UNKNOWN", "createdAt": "2026-09-24T08:00:00Z"}]
    fm.configure(root)
    found_ = _no_git_env(lambda: fm.pushed_branches(prs)) if hasattr(fm, "pushed_branches") else []
    lines_ = _no_git_env(lambda: fm.queue_lines(fm.queue_actions(prs, found_))) if found_ else [""]
    check(f"FM-031 · a branch on `origin` that no pull request carries is in the queue after the pull requests — `branch <name> @ <sha>  wait: no pull request — …` read as a pull request is: no verdict, a READY verdict (open it), a conflict — never the default branch, `answer/*`, a pull request's branch, a merged head or one inside an open pull request; and the count says how many (saw {lines_})",
          [b_["name"] for b_ in found_] == ["b-conflict", "b-none", "b-ready"]
          and lines_[1:] == [f"branch b-conflict @ {clash[:7]}  wait: no pull request — conflict in shared.txt",
                             f"branch b-none @ {none_[:7]}  wait: no pull request — no verdict on {none_[:7]}",
                             f"branch b-ready @ {ready[:7]}  wait: no pull request — verdict {ready[:7]} READY WITH FINDINGS: open it",
                             "4 waiting on you: 0 merge, 0 close, 1 wait, 3 pushed without a pull request"]
          and lines_[0].startswith("PR 7  wait: no verdict on"))
    # R3: a single-branch clone fetches one head; the queue fetches the others it lists, and a head still missing is
    # one line's `not fetched here` — never every verdict gone
    subprocess.run(["git", "clone", "-q", "--single-branch", "--branch", "main", str(base / "origin.git"), str(base / "sb")], check=True, capture_output=True, env=_ENV)
    fm.configure(base / "sb")
    single_ = _no_git_env(lambda: fm.pushed_branches([])) if hasattr(fm, "pushed_branches") else []
    ghost_ = [{"name": "b-ghost", "sha": "f" * 40, "base": "main", "here": False}]
    sb_lines_ = _no_git_env(lambda: fm.queue_lines(fm.queue_actions([], single_ + ghost_))) if single_ else [""]
    check(f"R2, R3 · a pushed head inside another pushed branch, or its twin, is no line of its own; in a single-branch clone the listed heads are fetched and read — a READY verdict survives — and a head that cannot be had reads `not fetched here` on its own line (saw {sb_lines_})",
          [b_["name"] for b_ in single_] == ["b-conflict", "b-none", "b-pr", "b-ready"] and all(b_["here"] for b_ in single_)
          and f"branch b-ready @ {ready[:7]}  wait: no pull request — verdict {ready[:7]} READY WITH FINDINGS: open it" in sb_lines_
          and "branch b-conflict @ " + clash[:7] + "  wait: no pull request — conflict in shared.txt" in sb_lines_
          and "branch b-ghost @ fffffff  wait: no pull request — not fetched here" in sb_lines_)
    rm_git(root)
fm.configure(HERE)

# --- FM-031, 0.18.3 (the Auditor seat's check 8): `--queue` ITSELF, `gh` stubbed — a branch pushed without a pull request --
# The check above reads that case through `pushed_branches` and `queue_actions`; this one runs `--queue` as the Owner does.
# `gh pr list` is answered by a stub (no pull request open); `origin` is a local bare repository the scratch clone pushed to,
# which the forge's URL check is told is GitHub; git runs for real — the fetch, `ls-remote`, the verdicts — and no real
# remote is touched.
with tempfile.TemporaryDirectory() as tmp:
    base = Path(tmp).resolve(); root = base / "wc"; root.mkdir(); bare_ = base / "origin.git"
    subprocess.run(["git", "init", "-q", "--bare", str(bare_)], check=True, env=_ENV); subprocess.run(["git", "init", "-q", str(root)], check=True, env=_ENV)
    git(root, "remote", "add", "origin", str(bare_)); run(root, "--init", "--key", "msr")
    (root / "shared.txt").write_text("one\n"); git(root, "add", "-A"); git(root, "commit", "-qm", "the trunk"); git(root, "branch", "-q", "-M", "main")
    subprocess.run(["git", "--git-dir", str(bare_), "symbolic-ref", "HEAD", "refs/heads/main"], check=True, env=_ENV)
    git(root, "checkout", "-q", "-b", "fm/002-pushed"); (root / "w.txt").write_text("w\n"); git(root, "add", "-A"); git(root, "commit", "-qm", "work pushed, no pull request opened")
    pushed_ = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"], capture_output=True, text=True, env=_ENV).stdout.strip()
    git(root, "checkout", "-q", "main"); git(root, "push", "-q", "origin", "main", "fm/002-pushed")
    asked_, real_run, real_which, real_forge = [], subprocess.run, fm.shutil.which, fm.github_remote
    def gh_stub_(*a, **k):
        if a and list(a[0])[:1] == ["gh-stub"]:                  # the forge: no pull request is open
            asked_.append(list(a[0]))
            return subprocess.CompletedProcess(a[0], 0, "[]", "")
        return real_run(*a, **k)
    subprocess.run, fm.shutil.which = gh_stub_, (lambda name, *a, **k: "gh-stub" if name == "gh" else real_which(name, *a, **k))
    fm.github_remote = lambda url: url.strip() == str(bare_) or real_forge(url)
    try:
        code_, out_, err_ = run_safe(root, "--queue")
    finally:
        subprocess.run, fm.shutil.which, fm.github_remote = real_run, real_which, real_forge
    check(f"FM-031 · `--queue` itself, `gh` stubbed and `origin` a local bare repository: a branch pushed without a pull request reads `branch <name> @ <sha>  wait: no pull request — no verdict on <sha>`, and the count names it (saw {out_!r}, {err_!r})",
          code_ == 0 and out_.splitlines() == [f"branch fm/002-pushed @ {pushed_[:7]}  wait: no pull request — no verdict on {pushed_[:7]}",
                                               "1 waiting on you: 0 merge, 0 close, 0 wait, 1 pushed without a pull request"]
          and [c_[1:3] for c_ in asked_] == [["pr", "list"]])
    rm_git(root)
fm.configure(HERE)

# --- FM-033, 0.18.3 (the Auditor seat's check 26, AU-14): no build commit before a judgement ---------------------------
# The Owner's rule: a pass judges before the first build commit. A commit that changes a path outside the tracker directory
# names a tracker — the ids in its subject, else its branch `<kind>/<NNN>-…` — that at the commit's PARENT carries
# `triaged:`, is not Parked and is In Progress. Keyed on the work, not on the status: a status gate would have missed three
# of the four builds FM-033 rows.
with tempfile.TemporaryDirectory() as tmp:
    base = Path(tmp).resolve(); root = base / "wc"; root.mkdir()
    subprocess.run(["git", "init", "-q", "--bare", str(base / "origin.git")], check=True, env=_ENV); subprocess.run(["git", "init", "-q", str(root)], check=True, env=_ENV)
    git(root, "remote", "add", "origin", str(base / "origin.git"))
    (root / "shoalmark.toml").write_text('name = "g"\njudged_before_build = true\n[kinds]\nAP = "Work"\n', encoding="utf-8")
    day_ = datetime.date.today().isoformat()
    tracker(root, "AP-001", status="Proposed", title="unjudged")
    tracker(root, "AP-002", status="Parked", extra=f"triaged: {day_}\ntier: P3\n", title="judged, parked")
    tracker(root, "AP-003", status="Proposed", extra=f"triaged: {day_}\ntier: P2\n", title="judged, proposed")
    tracker(root, "AP-004", status="In Progress", extra=f"triaged: {day_}\ntier: P2\n", title="judged, in progress")
    (root / "src.txt").write_text("one\n")
    run(root); git(root, "add", "-A"); git(root, "commit", "-qm", "the trunk"); git(root, "branch", "-q", "-M", "main")
    git(root, "push", "-q", "-u", "origin", "main"); git(root, "remote", "set-head", "origin", "main")
    sha_ = lambda ref="HEAD": subprocess.run(["git", "-C", str(root), "rev-parse", ref], capture_output=True, text=True, env=_ENV).stdout.strip()
    def build_(branch, subject, files, frm="main"):        # a branch cut from `frm`, one commit on it — made without the hook
        git(root, "switch", "-q", "-c", branch, frm)
        for name, text in files.items():
            (root / name).parent.mkdir(parents=True, exist_ok=True); (root / name).write_text(text)
        git(root, "add", "-A"); git(root, "commit", "-qm", subject)
        return sha_()
    def judged_(branch=None):                              # `--check`'s judgement on the branch checked out, read afresh
        if branch:
            git(root, "switch", "-q", branch)
        fm.configure(root)
        return _no_git_env(fm.build_judgement)
    def hooked_(branch, subject, files, frm="main"):       # the installed hooks on a real `git commit` — then --check on that commit
        git(root, "switch", "-q", "-c", branch, frm) if branch else git(root, "switch", "-q", "--detach", frm)
        for name, text in files.items():
            (root / name).parent.mkdir(parents=True, exist_ok=True); (root / name).write_text(text)
        git(root, "add", "-A"); before_ = sha_()
        r_ = subprocess.run(["git", "-C", str(root), "-c", "commit.gpgsign=false", "commit", "-q", "-m", subject], capture_output=True, text=True,
                            encoding="utf-8", errors="replace", env=_ENV)
        made_ = sha_() != before_
        if not made_:
            git(root, "commit", "-qm", subject)                # the same commit, made without the hooks: what --check then says of it
        said_ = judged_()[0]
        git(root, "switch", "-q", "--detach", "main")
        return made_, [l_.strip() for l_ in r_.stderr.splitlines() if l_.strip().startswith("refused:")], said_
    c1_ = build_("ap/001-build", "the importer", {"src.txt": "two\n"}); r1_ = judged_()
    c2_ = build_("ap/002-build", "the importer", {"src.txt": "two\n"}); r2_ = judged_()
    c3_ = build_("ap/003-build", "the importer", {"src.txt": "two\n"}); r3_ = judged_()
    c4_ = build_("ap/004-build", "the importer", {"src.txt": "two\n"}); r4_ = judged_()
    check(f"FM-033 · `--check` refuses a build commit under an unjudged tracker, a judged Parked one and a judged Proposed one — naming the commit, the tracker and what was missing — and passes it under a judged In Progress one (saw {r1_[0]!r})",
          len(r1_[0]) == 1 and r1_[0][0].startswith(f'refused: commit {c1_[:7]} "the importer" changes src.txt outside docs/work-tracker/ — AP-001: not judged, not In Progress (Proposed) — a pass judges before the first build commit (FM-033)')
          and len(r2_[0]) == 1 and "AP-002: Parked" in r2_[0][0] and len(r3_[0]) == 1 and "AP-003: not In Progress (Proposed)" in r3_[0][0]
          and r4_[0] == [] and r4_[1] == "judged before build: on — 1 commit(s) on `ap/004-build` since origin/main, every build commit under a judged In Progress tracker")
    git(root, "switch", "-q", "ap/001-build")
    code_, out_, err_ = run(root, "--check")
    check(f"FM-033 · end to end: `--check` exits 4 on the refusal and says the gate is on in one line (saw {err_.strip()[-200:]!r})",
          code_ == fm.EXIT_LINT and f"refused: commit {c1_[:7]}" in err_ and "judged before build: on — 1 commit(s) on `ap/001-build` since origin/main, 1 refused" in out_)
    t1_ = build_("ap/001-notes", "AP-001: a note", {"docs/work-tracker/AP-001-x.md": (root / "docs/work-tracker/AP-001-x.md").read_text() + "\nA note.\n"}); rt_ = judged_()
    cn_ = build_("docs/tidy", "tidy the readme", {"README.md": "tidy\n"}); rn_ = judged_()
    cs_ = build_("docs/tidy-2", "AP-004: tidy the readme", {"README.md": "tidy\n"}); rs_ = judged_()
    cw_ = build_("ap/004-wrong", "AP-001: the importer, under another tracker's branch", {"src.txt": "three\n"}); rw_ = judged_()
    check(f"FM-033 · a commit that touches only the tracker directory is not judged; one that names no tracker is refused as such; the subject's ids decide before the branch's (C1) — a judged one passes on any branch, an unjudged one is refused on a judged branch (saw {rn_[0]!r})",
          rt_[0] == [] and len(rn_[0]) == 1 and f"refused: commit {cn_[:7]} \"tidy the readme\" changes README.md outside docs/work-tracker/ — names no tracker: no AP-N in its subject, and its branch `docs/tidy` names none" in rn_[0][0]
          and rs_[0] == [] and len(rw_[0]) == 1 and "AP-001: not judged" in rw_[0][0])
    git(root, "switch", "-q", "--detach", "ap/004-build"); rd_ = judged_()
    git(root, "switch", "-q", "--detach", "docs/tidy-2"); rd2_ = judged_()
    check(f"FM-033 · on a detached HEAD the subject must name the tracker (C3): a subject without an id is `names no tracker`, one with a judged id passes (saw {rd_[0]!r})",
          len(rd_[0]) == 1 and "names no tracker" in rd_[0][0] and rd2_[0] == [] and "on a detached HEAD since origin/main" in rd2_[1])
    # a merge: its own change is never the merger's; the commits it carries are judged, at their own parents
    side_ = build_("side/import", "AP-001: the importer on the side", {"side.txt": "s\n"})
    git(root, "switch", "-q", "ap/004-build"); git(root, "merge", "-q", "--no-ff", "-m", "merge the side", "side/import")
    rm_ = judged_()
    git(root, "switch", "-q", "-c", "ap/004-merge-now", "ap/004-build~1"); git(root, "merge", "-q", "--no-ff", "--no-commit", "side/import")
    (root / "merge-msg").write_text("Merge side/import\n"); codem_, _o, errm_ = run(root, "--commit-msg", str(root / "merge-msg"))
    git(root, "merge", "--abort"); (root / "merge-msg").unlink(); git(root, "switch", "-q", "main")
    check(f"FM-033 · a merge commit is skipped and every commit it carries is judged — by `--check`, and at commit time on a merge being made (saw {rm_[0]!r}, {errm_.strip()[-160:]!r})",
          len(rm_[0]) == 1 and rm_[0][0].startswith(f'refused: commit {side_[:7]} "AP-001: the importer on the side"') and "merge the side" not in " ".join(rm_[0])
          and codem_ == fm.EXIT_LINT and f"refused: commit {side_[:7]}" in errm_)
    # main moves under a commit nobody judged; a judged branch that merges main carries none of it into its range
    git(root, "switch", "-q", "main"); (root / "main.txt").write_text("m\n"); git(root, "add", "-A"); git(root, "commit", "-qm", "the trunk moves")
    git(root, "push", "-q", "origin", "main"); git(root, "fetch", "-q", "origin")
    git(root, "switch", "-q", "-c", "ap/004-uptodate", "ap/004-build~1"); git(root, "merge", "-q", "--no-ff", "-m", "main merged in", "origin/main")
    ru_ = judged_(); git(root, "switch", "-q", "main"); rmain_ = judged_()
    check("FM-033 · a merge of `origin`'s default branch brings none of its commits into the judged range; on the default branch itself nothing is judged",
          ru_[0] == [] and rmain_[0] == [] and rmain_[1] == "judged before build: on — `main` is the default branch: nothing on it is judged")
    # AT COMMIT TIME (the cold review's R1): the installed commit-msg hook judges the commit being made with its SUBJECT, as the
    # history is judged — its ids, else its branch — and refuses it before it is made, with the line --check prints of it made.
    # The pre-commit stage has no message: judged there by its branch, `FM-007: …` on a judged branch passed the hook, and failed --check.
    run(root, "--install-hook"); git(root, "switch", "-q", "--detach", "main")
    note_ = (root / "docs/work-tracker/AP-001-x.md").read_text() + "\nA note at commit time.\n"
    table_ = [("ap/004-probe", "AP-001: gate probe"),                 # the Reviewer's probe: a judged branch, an unready tracker in the subject
              ("ap/001-probe", "AP-004: gate probe, the inverse"),    # an unjudged branch, a judged tracker in the subject
              ("ap/001-hook", "the importer"), ("ap/002-hook", "the importer"), ("ap/003-hook", "the importer"), ("ap/004-hook", "the importer"),
              ("docs/hook", "the importer"), ("docs/hook-2", "AP-004: the importer"), (None, "the importer, detached"), (None, "AP-004: detached")]
    seen_ = {}
    for n_, (branch_, subject_) in enumerate(table_):
        seen_[(branch_, subject_)] = hooked_(branch_, subject_, {"src.txt": f"hook {n_}\n"})
    seen_["notes"] = hooked_("ap/001-hook-notes", "AP-001: a note", {"docs/work-tracker/AP-001-x.md": note_})
    tail_ = lambda l_: l_.split(" changes ", 1)[1] if " changes " in l_ else l_
    agree_ = all(made_ == (not said_) and [tail_(l_) for l_ in hook_] == [tail_(l_) for l_ in said_] and all(l_.startswith("refused: this commit \"") for l_ in hook_)
                 for made_, hook_, said_ in seen_.values())
    verdicts_ = {k_: v_[0] for k_, v_ in seen_.items()}
    check(f"FM-033 · R1 · the commit-msg hook judges the commit being made with its subject and refuses it before it is made: the Reviewer's probe — a judged branch, an unready tracker in the subject — is refused, no commit made; the inverse passes (saw {seen_[('ap/004-probe', 'AP-001: gate probe')][1]!r})",
          verdicts_[("ap/004-probe", "AP-001: gate probe")] is False and verdicts_[("ap/001-probe", "AP-004: gate probe, the inverse")] is True
          and seen_[("ap/004-probe", "AP-001: gate probe")][1] == ['refused: this commit "AP-001: gate probe" changes src.txt outside docs/work-tracker/ — AP-001: not judged, not In Progress (Proposed) — ' + fm.BUILD_WHY])
    check(f"FM-033 · R1 · the hook and --check agree on every case of the table — refused or made, and the same reasons — Parked, Proposed, unjudged, no tracker named, a detached HEAD, the subject before the branch, a tracker-only commit (saw {verdicts_})",
          agree_ and [verdicts_[(b_, s_)] for b_, s_ in table_[2:]] == [False, False, False, True, False, True, False, True] and verdicts_["notes"] is True)
    # a subject that starts with `#` (the cold second pass's R1): `-m` keeps it, an editor strips it — the hook judges what git keeps
    def commented_(branch, *args):                         # through the installed hooks; then --check on the same commit, made without them
        git(root, "switch", "-q", "-c", branch, "main"); (root / "src.txt").write_text(branch + "\n"); git(root, "add", "-A"); before_ = sha_()
        r_ = subprocess.run(["git", "-C", str(root), "-c", "commit.gpgsign=false", "commit", "-q", *args], capture_output=True, text=True, encoding="utf-8", errors="replace", env=_ENV)
        made_ = sha_() != before_
        if not made_:
            subprocess.run(["git", "-C", str(root), "-c", "commit.gpgsign=false", "-c", "core.hooksPath=/dev/null", "commit", "-q", *args], check=True, capture_output=True, env=_ENV)
        said_ = judged_()[0]; git(root, "switch", "-q", "--detach", "main")
        return made_, [l_.strip() for l_ in r_.stderr.splitlines() if l_.strip().startswith("refused:")], said_
    hash_ = commented_("ap/004-hash", "-m", "# AP-001: comment subject probe")          # the Reviewer's exact case
    verb_ = commented_("ap/004-verbatim", "--cleanup=verbatim", "-m", "# AP-001: comment subject probe")
    two_ = commented_("ap/004-two", "-m", "# AP-001: hidden", "-m", "AP-004: shown")
    none_ = commented_("ap/004-none", "-m", "# nothing but a comment")
    check(f"FM-033 · R1 (second pass) · a subject that starts with `#`: `-m` and `--cleanup=verbatim` keep it, and the hook judges it — refused before it is made, with the reason --check gives it; a `#` line above a named subject too (saw {hash_[1]!r})",
          all(not r_[0] and r_[1] and [l_.split(" changes ", 1)[1] for l_ in r_[1]] == [l_.split(" changes ", 1)[1] for l_ in r_[2]] for r_ in (hash_, verb_, two_))
          and "AP-001: not judged, not In Progress (Proposed)" in hash_[1][0] and hash_[1][0].startswith('refused: this commit "# AP-001: comment subject probe"'))
    check(f"FM-033 · R1 (second pass) · a message whose every line is a comment keeps no subject once stripped: refused as naming no tracker — the hook is best-effort and errs this way (saw {none_[1]!r})",
          not none_[0] and len(none_[1]) == 1 and "names no tracker: every line of its message is a comment, which git strips" in none_[1][0]
          and fm.message_subject("; a\nFM-7: x\n", ";") == "FM-7: x" and fm.literal_subject("\n# FM-7: x\nmore\n") == "# FM-7: x")
    git(root, "switch", "-q", "main"); (root / "src.txt").write_text("on main\n"); git(root, "add", "-A")
    main_ = subprocess.run(["git", "-C", str(root), "-c", "commit.gpgsign=false", "commit", "-q", "-m", "the trunk, by hand"], capture_output=True, text=True, env=_ENV)
    git(root, "reset", "-q", "--hard", "origin/main")      # main as origin has it: the checks below measure from it
    git(root, "switch", "-q", "-c", "ap/004-merge-hook", "ap/004-build~1")
    merged_ = subprocess.run(["git", "-C", str(root), "-c", "commit.gpgsign=false", "merge", "-q", "--no-ff", "--no-edit", "side/import"], capture_output=True, text=True, encoding="utf-8", errors="replace", env=_ENV)
    merging_ = (root / ".git/MERGE_HEAD").exists(); git(root, "merge", "--abort") if merging_ else None
    empty_ = run(root, "--commit-msg", str(root / "no-such-message"))[0]; (root / "blank-msg").write_text("# only a comment\n\n")
    blank_ = run(root, "--commit-msg", str(root / "blank-msg"))[0]; (root / "blank-msg").unlink()
    check(f"FM-033 · R1 · on the default branch the hook judges nothing; a merge the hook refuses is not made, its carried commit named; an empty message is git's to refuse (saw {merged_.stderr.strip()[-160:]!r})",
          main_.returncode == 0 and merged_.returncode != 0 and merging_ and f"refused: commit {side_[:7]}" in merged_.stderr
          and empty_ == fm.EXIT_LINT and blank_ == 0 and fm.message_subject("# c\n\n  FM-7: x \nbody\n") == "FM-7: x"
          and fm.message_subject("# ------------------------ >8 ------------------------\nFM-7: x\n") == "")
    git(root, "switch", "-q", "main")
    # the tracker made In Progress and judged in the SAME commit as the build: the parent is what counts
    git(root, "switch", "-q", "-c", "ap/001-all-at-once", "main")
    tracker(root, "AP-001", status="In Progress", extra=f"triaged: {day_}\ntier: P2\n", title="unjudged"); (root / "src.txt").write_text("at once\n")
    git(root, "add", "-A"); git(root, "commit", "-qm", "AP-001: judged and built at once"); ra_ = judged_()
    tracker(root, "AP-001", status="In Progress", extra=f"triaged: {day_}\ntier: P2\n", title="unjudged", body="## What is true now\n\n**Built.**\n\n## Done when\n\nit is.\n")
    (root / "src.txt").write_text("after\n"); git(root, "add", "-A"); git(root, "commit", "-qm", "AP-001: the next build commit"); ra2_ = judged_()
    check(f"FM-033 · a tracker set In Progress and judged in the same commit as its first build is refused — the judgement is read at the commit's parent — and the next build commit passes (saw {ra_[0]!r})",
          len(ra_[0]) == 1 and "AP-001: not judged" in ra_[0][0] and len(ra2_[0]) == 1 and "judged and built at once" in ra2_[0][0])
    # off: silent
    git(root, "switch", "-q", "ap/001-build"); (root / "shoalmark.toml").write_text('name = "g"\n[kinds]\nAP = "Work"\n', encoding="utf-8")
    ro_ = judged_(); codeo_, _o, erro_ = run(root, "--session-check"); (root / "shoalmark.toml").write_text('name = "g"\njudged_before_build = 1\n[kinds]\nAP = "Work"\n', encoding="utf-8")
    try:
        fm.configure(root); bad_ = ""
    except SystemExit as e:
        bad_ = str(e)
    git(root, "checkout", "-q", "--", "shoalmark.toml")
    check(f"FM-033 · the key off (the default), nothing is judged and `--check` says so; the key is `true` or `false`, and `--schema` prints it (saw {bad_!r})",
          ro_ == ([], "judged before build: off — `judged_before_build = true` in shoalmark.toml turns it on") and codeo_ == 0
          and "`judged_before_build` is true or false" in bad_ and "| `judged_before_build` | `true` or `false` (the default) |" in fm.render_schema())
    rm_git(root)
fm.configure(HERE)
# FM-033's five, judged at their own parents in this repository's history — by their subjects, their branches not being in
# the record. CI checks out the whole history for this (`fetch-depth: 0`); the seat that built them was not this one.
_five = ["89e0586", "3c0754f", "90d3d6f", "bd7d5ea", "4dfb999"]
_judged5 = _no_git_env(lambda: fm.judge_commits(fm.commit_list("--no-walk", *_five), ""))
check(f"FM-033 · the four builds of FM-033's table and the fifth are each refused, judged at their own parents: FM-024 not judged, FM-032, FM-031 and FM-029 not judged and Proposed, and bd7d5ea names no tracker (saw {[l_[:60] for l_ in _judged5]})",
      len(_judged5) == 5 and all(any(l_.startswith(f"refused: commit {c_}") for l_ in _judged5) for c_ in _five)
      and any(l_.startswith("refused: commit 89e0586") and "FM-024: not judged —" in l_ for l_ in _judged5)
      and all(any(l_.startswith(f"refused: commit {c_}") and f"{t_}: not judged, not In Progress (Proposed)" in l_ for l_ in _judged5)
              for c_, t_ in (("3c0754f", "FM-032"), ("90d3d6f", "FM-031"), ("4dfb999", "FM-029")))
      and any(l_.startswith("refused: commit bd7d5ea") and "names no tracker" in l_ for l_ in _judged5))
_own = ["cba97b6", "b9f8a29", "6f54242", "3c3e02f", "172a2ad", "f44e7f9"]
check("FM-033 · and 0.18.3's own build commits pass the same judgement — each under FM-029, FM-030, FM-031 or FM-033, judged and In Progress at its parent",
      _no_git_env(lambda: fm.judge_commits(fm.commit_list("--no-walk", *_own), "")) == [] and len(fm.commit_list("--no-walk", *_own)) == len(_own))

# --- FM-031 · an `answer/*` pull request is the Owner's signed answer, not a Reviewer's; RV: a signed commit this clone
#     cannot verify is said to be that — never "sign it" ---------------------------------------------------------------
with tempfile.TemporaryDirectory() as tmp:
    base = Path(tmp).resolve(); root = base / "wc"; root.mkdir()
    subprocess.run(["git", "init", "-q", str(root)], check=True, env=_ENV)
    key = base / "k"; subprocess.run(["ssh-keygen", "-q", "-t", "ed25519", "-N", "", "-f", str(key)], check=True, capture_output=True)
    (base / "signers").write_text("t@t " + key.with_suffix(".pub").read_text(), encoding="utf-8")
    for k_, v_ in (("gpg.format", "ssh"), ("user.signingkey", str(key)), ("gpg.ssh.allowedSignersFile", str(base / "signers"))):
        git(root, "config", k_, v_)
    run(root, "--init", "--key", "msr")
    cfg_ = root / "shoalmark.toml"; cfg_.write_text(cfg_.read_text().replace("[kinds]", 'answerers = ["t signed"]\n\n[kinds]', 1))
    sha = lambda ref="HEAD": subprocess.run(["git", "-C", str(root), "rev-parse", ref], capture_output=True, text=True, env=_ENV).stdout.strip()
    since_ = (datetime.date.today() - datetime.timedelta(days=2)).isoformat()
    tr_ = tracker(root, "MSR-001", extra=f'next: owner\nask: "Ship it?"\nask-kind: ruling\nask-since: {since_}\nask-proposal: "yes"\n')
    run(root); git(root, "add", "-A"); git(root, "commit", "-qm", "the ask"); git(root, "branch", "-q", "-M", "main"); t0 = sha()
    git(root, "update-ref", "refs/remotes/origin/main", t0)
    tr_.write_text(tr_.read_text().replace('ask-proposal: "yes"\n', f'ask-proposal: "yes"\nanswer: "accepted"\nanswered: {datetime.date.today().isoformat()}\nanswered-by: t\n'))
    git(root, "checkout", "-q", "-b", "answer/msr-001"); git(root, "add", "-A"); git(root, "commit", "-q", "-S", "-m", "MSR-001: accepted")
    run(root); git(root, "add", "-A"); git(root, "commit", "-q", "--amend", "-S", "--no-edit"); signed_ = sha()      # the INDEX as the hook would stage it
    git(root, "checkout", "-q", "-b", "answer/msr-002", t0); (root / "x.txt").write_text("x"); git(root, "add", "-A"); git(root, "commit", "-q", "-m", "MSR-002: unsigned"); unsigned_ = sha()
    git(root, "checkout", "-q", "-b", "answer/msr-003", t0); (root / "y.txt").write_text("y"); git(root, "add", "-A")
    git(root, "commit", "-q", "-S", "--author=mallory <m@m>", "-m", "MSR-003: signed, and not by an answerer"); impostor_ = sha()
    prs = [{"number": n_, "title": b_, "headRefName": b_, "headRefOid": h_, "baseRefName": "main", "mergeable": "UNKNOWN", "mergeStateStatus": "UNKNOWN", "createdAt": f"2026-09-24T0{n_}:00:00Z"}
           for n_, b_, h_ in ((1, "answer/msr-001", signed_), (2, "answer/msr-002", unsigned_), (3, "answer/msr-003", impostor_))]
    fm.configure(root)
    read_ = lambda: [a_ for _p, _k, a_, _d in _no_git_env(lambda: fm.queue_actions(prs))]
    trusted_ = read_()
    plain_cfg = cfg_.read_text(); cfg_.write_text(plain_cfg.replace('answerers = ["t signed"]\n', "") + '\n[seats]\nowner = "t signed"\n'); fm.configure(root)
    by_name_ = read_(); cfg_.write_text(plain_cfg); fm.configure(root)
    check(f"R1 · with `[seats]` naming the Owner by his git name, as the gate matches a seat (email or name), his signed answer reads `merge: your answer` (saw {by_name_})",
          by_name_ == ["merge: your answer", "wait: unsigned answer", "wait: not an answerer (m@m)"])
    git(root, "checkout", "-q", "answer/msr-001"); ok_ = run(root, "--check")[0]
    git(root, "config", "gpg.ssh.allowedSignersFile", ""); fm.configure(root)          # empty here, whatever the machine's own config says
    untrusted_ = read_(); code_, _, err_ = run(root, "--check")
    check(f"FM-031 · an `answer/*` pull request whose head the Owner signed and this clone verifies reads `merge: your answer`; an unsigned one `wait: unsigned answer` — no Reviewer verdict is asked of either (saw {trusted_})",
          trusted_[:2] == ["merge: your answer", "wait: unsigned answer"] and ok_ == 0)
    check(f"R8 · a SIGNED `answer/*` commit by someone who may not answer reads `wait: not an answerer (<author>)` — not *unsigned*: the impostor is named (saw {trusted_})",
          trusted_[2] == "wait: not an answerer (m@m)" and bool(subprocess.run(["git", "-C", str(root), "log", "-1", "--format=%GK", impostor_], capture_output=True, text=True, env=_ENV).stdout.strip()))
    check(f"RV · with `gpg.ssh.allowedSignersFile` unset, a SIGNED answer is refused as unverifiable here, naming the setting and the signing page — never 'sign it'; the exit is unchanged, and the queue says the same (saw {err_.strip()[-220:]!r}, {untrusted_})",
          code_ == fm.EXIT_LINT and "it is signed, but this clone cannot verify: `gpg.ssh.allowedSignersFile` is not set — see " + fm.SIGNING_PAGE in err_
          and "sign it (`git commit -S`)" not in err_ and untrusted_[0] == "wait: answer not verified here — `gpg.ssh.allowedSignersFile` is not set")
    git(root, "commit", "-q", "--amend", "--no-edit", "--no-gpg-sign"); code2_, _, err2_ = run(root, "--check")
    check("RV · an answer committed with no signature at all is still asked to be signed",
          code2_ == fm.EXIT_LINT and "sign it (`git commit -S`)" in err2_ and "cannot verify" not in err2_)
    rm_git(root)
fm.configure(HERE)

# --- FM-034, 0.18.3 (the Auditor seat's check 20): a fresh clone's `--check` — the checkout's own finding is said once, on
#     stderr, and never written into INDEX.md; the committed INDEX and the one any clone generates are the same under
#     `drift_normalize` — the `Generated` date aside, which a clone generating it the next day writes anew (the cold R2) ----
with tempfile.TemporaryDirectory() as tmp:
    base = Path(tmp).resolve(); root = base / "wc"; root.mkdir()
    subprocess.run(["git", "init", "-q", str(root)], check=True, env=_ENV)
    key = base / "k"; subprocess.run(["ssh-keygen", "-q", "-t", "ed25519", "-N", "", "-f", str(key)], check=True, capture_output=True)
    (base / "signers").write_text("t@t " + key.with_suffix(".pub").read_text(), encoding="utf-8")
    for k_, v_ in (("gpg.format", "ssh"), ("user.signingkey", str(key)), ("gpg.ssh.allowedSignersFile", str(base / "signers"))):
        git(root, "config", k_, v_)
    run(root, "--init", "--key", "msr")
    cfg_ = root / "shoalmark.toml"; cfg_.write_text(cfg_.read_text().replace("[kinds]", 'answerers = ["t signed"]\n\n[kinds]', 1))
    since_ = (datetime.date.today() - datetime.timedelta(days=2)).isoformat()
    ask_ = lambda q: f'next: owner\nask: "{q}"\nask-kind: ruling\nask-since: {since_}\nask-proposal: "yes"\n'
    trs_ = [tracker(root, "MSR-001", extra=ask_("Ship the importer?")), tracker(root, "MSR-002", extra=ask_("Ship the exporter?"))]
    run(root); git(root, "add", "-A"); git(root, "commit", "-qm", "the asks")
    signed_ = []
    for tr_ in trs_:                                       # the Owner's answers, each his own signed commit, the INDEX as the hook stages it
        tr_.write_text(tr_.read_text().replace('ask-proposal: "yes"\n', f'ask-proposal: "yes"\nanswer: "accepted"\nanswered: {datetime.date.today().isoformat()}\nanswered-by: t\n'))
        git(root, "add", "-A"); git(root, "commit", "-q", "-S", "-m", f"{tr_.name[:7]}: accepted")
        run(root); git(root, "add", "-A"); git(root, "commit", "-q", "--amend", "-S", "--no-edit")
        signed_.append(subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"], capture_output=True, text=True, env=_ENV).stdout.strip())
    ok_code, ok_out, ok_err = run(root, "--check")
    fresh_ = base / "fresh"; subprocess.run(["git", "clone", "--quiet", str(root), str(fresh_)], check=True, capture_output=True, env=_ENV)
    git(fresh_, "config", "gpg.ssh.allowedSignersFile", "")      # empty here, whatever the machine's own config says
    index_ = (fresh_ / "docs/work-tracker/INDEX.md").read_text(encoding="utf-8")
    code_, out_, err_ = run(fresh_, "--check")
    said_ = [l_ for l_ in err_.splitlines() if "cannot verify" in l_]
    wcode_, _o, _e = run(fresh_)
    status_ = subprocess.run(["git", "-C", str(fresh_), "status", "--porcelain"], capture_output=True, text=True, env=_ENV).stdout
    tomorrow_ = re.sub(r"Generated \d{4}-\d{2}-\d{2}", "Generated 2999-01-01", index_)     # the same INDEX, generated another day
    generated_ = (fresh_ / "docs/work-tracker/INDEX.md").read_text(encoding="utf-8")
    (fresh_ / "docs/work-tracker/INDEX.md").write_text(tomorrow_, encoding="utf-8"); later_ = run(fresh_, "--check")[1]
    check(f"FM-034 · a fresh clone without the signers file: `--check` prints ONE finding, the signers file, naming the answers it could not check — and no STALE; the INDEX it writes is the committed one under `drift_normalize` — the date aside, so on another day too — and `--check` reads it so (saw {err_.strip()!r})",
          code_ == fm.EXIT_LINT and len(said_) == 1 and "STALE" not in out_ + err_ and "INDEX.md is up to date" in out_
          and said_[0] == f"  checkout: it is signed, but this clone cannot verify: `gpg.ssh.allowedSignersFile` is not set — see {fm.SIGNING_PAGE} — 2 signed commit(s) it could not check: MSR-001 `{signed_[0][:10]}`, MSR-002 `{signed_[1][:10]}`"
          and "FAILED: this checkout's own finding — the ledger is sound" in err_ and "ledger-integrity" not in err_
          and fm.drift_normalize(generated_) == fm.drift_normalize(index_) and "INDEX.md is up to date" in later_
          and fm.drift_normalize(tomorrow_) == fm.drift_normalize(index_) and tomorrow_ != index_
          and "cannot verify" not in index_ and status_ in ("", " M docs/work-tracker/INDEX.md\n"))
    check("FM-034 · the clone with the signers file configured: no finding, exit 0",
          ok_code == 0 and "cannot verify" not in ok_err and "checkout:" not in ok_err)
    rm_git(root)
    shutil.rmtree(fresh_ / ".git", onerror=lambda f, p, e: (os.chmod(p, __import__("stat").S_IWRITE), f(p)))
fm.configure(HERE)
# …and each commit once (the cold second pass's R4): on a merge, the answer rule and the rights rule both ask of one answer's
# commit, and the line counted 8 signed commits where 5 were meant
_gap = "it is signed, but this clone cannot verify: `gpg.ssh.allowedSignersFile` is not set — see " + fm.SIGNING_PAGE
_twice = [f"FM-007: the answer's commit `1034602c96` does not verify as `o@x` — {_gap}",
          f"in `1034602c96` (o@x), which the merge brings — FM-007: the commit `1034602c96` making a `answer` change does not verify as the seat `owner` — {_gap}",
          f"FM-024: the answer's commit `64f843ef3a` does not verify as `o@x` — {_gap}",
          f"FM-024: the commit `64f843ef3a` making a `answer` change does not verify as the seat `owner` — {_gap}"]
check(f"FM-034 · R4 · the checkout line counts each commit it could not check once, and names it once (saw {fm.checkout_lines(_twice)!r})",
      fm.checkout_lines(_twice) == [f"  checkout: {_gap} — 2 signed commit(s) it could not check: FM-007 `1034602c96`, FM-024 `64f843ef3a`"])
# …and a pinned file this checkout has not got is the checkout's finding too — said, never written into the INDEX
with tempfile.TemporaryDirectory() as d:
    root = Path(d).resolve(); dest = root / "tools" / "shoalmark"
    with redirect_stdout(io.StringIO()):
        fm.vendor(dest, allow_untagged=True)
    tracker(root, "FEAT-001", status="Proposed")
    (dest / "LICENSE-MIT").unlink()
    gone_ = subprocess.run([sys.executable, str(dest / "shoalmark.py"), "--root", str(root)], capture_output=True, text=True, encoding="utf-8", errors="replace", env=_ENV)
    index_ = (root / "docs/work-tracker/INDEX.md").read_text(encoding="utf-8")
    check(f"FM-034 · a pinned file the checkout has not got is said on stderr as the checkout's, and INDEX.md carries no line of it (saw {gone_.stderr.strip()[-200:]!r})",
          gone_.returncode == fm.EXIT_LINT and "  checkout: tools/shoalmark/LICENSE-MIT: the PIN names it, and this checkout cannot read it" in gone_.stderr
          and "LICENSE-MIT" not in index_ and "ledger-integrity" not in index_)
fm.configure(HERE)

# --- FM-029: the answer's relation to the proposal — computed by every reading, the signed line untouched ---------------
# One word covered three answers: under `accepted` the board's dialog and `--answer` write the proposal, another listed
# option and changed text alike, and a reader counting how often the Owner took the proposal counted all three. The
# relation is read from `answer:` against `ask-proposal:` and `ask-options:`, the answer's own normalisation on both sides.
rel_ = lambda answer, proposal="", options=(): fm.answer_relation({"answer": answer, "ask_proposal": proposal, "ask_options": list(options)})
opts_ = ["ship the importer", "ship the exporter", "ship neither"]
check("FM-029 · the proposal, by its text or by a bare `accepted`; another option by its place in `ask-options:`, from 1; changed text; a rejection and a revocation with their reasons",
      rel_("accepted - ship the importer", "ship the importer", opts_) == ("proposal", 0, "")
      and rel_("accepted", "ship the importer", opts_) == ("proposal", 0, "")
      and rel_("accepted - ship neither", "ship the importer", opts_) == ("option", 3, "ship neither")
      and rel_("accepted - ship the importer, and count a week first", "ship the importer", opts_) == ("changed", 0, "")
      and rel_("rejected - not this quarter", "ship the importer", opts_) == ("rejected", 0, "not this quarter")
      and rel_("revoked - the audit comes first", "ship the importer", opts_) == ("revoked", 0, "the audit comes first")
      and rel_("rejected", "ship the importer") == ("rejected", 0, "") and rel_("Accepted - ship the importer", "ship the importer") == ("proposal", 0, ""))
check("FM-029 · the answer's own normalisation on BOTH sides: a proposal holding a double quote and a double space reads as the proposal, not as changed text — and an option as that option",
      rel_("accepted - ship 'the importer' first", 'ship "the importer"  first', ['ship "the importer"  first', "wait  a week"]) == ("proposal", 0, "")
      and rel_('accepted -   wait a   week ', 'ship "the importer"  first', ['ship "the importer"  first', "wait  a week"]) == ("option", 2, "wait a week"))
check("FM-029 · the schema's hand-written em-dash form reads as the dash `--answer` writes; with no proposal an option still reads as its option and other text as a change",
      rel_("accepted — ship neither", "ship the importer", opts_) == ("option", 3, "ship neither")
      and rel_("rejected — the audit first", "ship the importer") == ("rejected", 0, "the audit first")
      and rel_("accepted - ship the exporter", "", opts_) == ("option", 2, "ship the exporter") and rel_("accepted - ship both", "", opts_) == ("changed", 0, ""))
check("FM-029 · *relation not computable*, never a guess: a bare `accepted` on an ask with no proposal, accepted text with neither a proposal nor options, a word that is none of the three; no answer, no relation",
      rel_("accepted") == ("unknown", 0, "") and rel_("accepted", "", opts_) == ("unknown", 0, "") and rel_("accepted - ship it") == ("unknown", 0, "")
      and rel_("yes - ship it", "ship it") == ("unknown", 0, "") and rel_("accepted: ship it", "ship it") == ("unknown", 0, "") and rel_("") is None
      and fm.relation_text(rel_("accepted")) == "relation not computable" and fm.relation_text(None) == "")
long_ = "keep the importer, the exporter and the reconciliation in one release, then measure a week"
check("FM-029 · the relation quotes an option's or a reason's first words, cut between two words",
      fm.relation_text(rel_(f"accepted - {long_}", "ship the importer", ["ship the importer", long_])) == "chose option 2: keep the importer, the exporter and the…"
      and fm.relation_text(rel_("accepted - ship neither", "ship the importer", opts_)) == "chose option 3: ship neither"
      and fm.relation_text(rel_("rejected - not this quarter")) == "rejected: not this quarter")
# the Owner's own three, as synthetic trackers carrying their lines — nothing here reads a real corpus
FM029_ = ('ask: "Rule the answer\'s word for 0.18.1: the board and every reading print the answer\'s relation to the proposal (accepted it · accepted with a change · chose option N · rejected · revoked), the signed line unchanged; or new verbs you type (changed, chose) beside accept, reject and revoke; or both?"\n'
          'ask-kind: ruling\nask-since: {since}\nask-proposal: "both — the relation computed for every answer, the verbs changed and chose for new ones"\n'
          'ask-options: "both — the relation computed for every answer, the verbs changed and chose for new ones | the relation only — no new verbs | the verbs only | none — the word stays accepted"\n')
FM031_ = ('ask: "Rule the three house rules — at most 2 pull requests waiting on you per repository, your rulings only to the coordinating session, `git switch --detach origin/<branch>` to look at a seat\'s branch — and the build order, S1 the registry off the conflict path then S2 the queue in one view?"\n'
          'ask-kind: ruling\nask-since: {since}\nask-options: "all three rules now, S1 then S2 | the rules now, build nothing yet | S1 only, rules later | none — keep the current fan-out"\n'
          'ask-proposal: "all three rules now, S1 then S2"\n')
D1_ = ('ask: "Which week does the shadow run take?"\nask-kind: ruling\nask-since: {since}\nask-proposal: "this week, as planned"\n'
       'ask-options: "this week, as planned | next week, after the release | a week of your choosing, "shadow" only on weekdays"\n')
with tempfile.TemporaryDirectory() as tmp:
    base = Path(tmp).resolve(); root = base / "wc"; root.mkdir()
    subprocess.run(["git", "init", "-q", "--bare", str(base / "origin.git")], check=True, env=_ENV); subprocess.run(["git", "init", "-q", str(root)], check=True, env=_ENV)
    for k_, v_ in (("user.name", "holgo"), ("user.email", "h@x"), ("commit.gpgsign", "false")):
        git(root, "config", k_, v_)
    git(root, "remote", "add", "origin", str(base / "origin.git"))
    (root / "shoalmark.toml").write_text('name = "r"\nanswerers = ["holgo"]\n[kinds]\nAP = "Work"\n', encoding="utf-8")
    since_ = (datetime.date.today() - datetime.timedelta(days=1)).isoformat(); today_ = datetime.date.today().isoformat()
    ask_ = lambda lines: "next: owner\n" + lines.format(since=since_)
    answered_ = lambda answer: f'answer: "{answer}"\nanswered: {today_}\nanswered-by: holgo\n'
    d1_ = tracker(root, "AP-290", extra=ask_(D1_), title="D1 by shape")
    f31_ = tracker(root, "AP-291", extra=ask_(FM031_) + answered_("accepted - one channel and the detached switch now, S1 then S2; the cap of 2 waiting pull requests revoked 2026-09-24"), title="FM-031 as PR 46 left it")
    f29_ = tracker(root, "AP-292", extra=ask_(FM029_) + answered_("accepted - the relation only — no new verbs"), title="FM-029 as 140f799 left it")
    q_ = tracker(root, "AP-293", extra=ask_('ask: "Which ships first?"\nask-kind: ruling\nask-since: {since}\nask-proposal: ship "the importer"  first\n'), title="a quoted proposal")
    r_ = tracker(root, "AP-294", extra=ask_('ask: "Shall the exporter ship?"\nask-kind: ruling\nask-since: {since}\nask-proposal: "yes"\n'), title="to reject")
    run(root); git(root, "add", "-A"); git(root, "commit", "-qm", "the asks", "--author=holgo <h@x>"); git(root, "push", "-q", "-u", "origin", "HEAD:main")
    trunk_ = subprocess.run(["git", "-C", str(root), "branch", "--show-current"], capture_output=True, text=True, env=_ENV).stdout.strip()
    # the board's dialog: OK gives `--answer <id> accept "<q(option)>"`, q() trimming and writing `"` as `'` — option 3 of three
    dialog_ = lambda o: o.strip().replace('"', "'")
    d1_opt3 = fm.parse_frontmatter(d1_.read_text())[0]["ask-options"].strip('"').split(" | ")[2]
    codes_ = [run(root, "--answer", "AP-290", "accept", dialog_(d1_opt3))[0], run(root, "--answer", "AP-293", "accept", 'ship "the importer"  first')[0],
              run(root, "--answer", "AP-294", "reject", "not this quarter — the audit comes first")[0]]
    for id_ in ("ap-290", "ap-293", "ap-294"):
        git(root, "merge", "-q", "--no-ff", "-m", f"the Owner merges {id_}", f"answer/{id_}")
    fm.configure(root); by_ = {t["id"]: t for t in fm.load_trackers()}
    rels_ = {k: fm.answer_relation(by_[k]) for k in ("AP-290", "AP-291", "AP-292", "AP-293", "AP-294")}
    check(f"FM-029 · the Owner's own three: D1's shape — the third of three options, picked in the dialog — reads *chose option 3*; FM-031's line as PR 46 left it reads *accepted with a change*; FM-029's own answer of 14:24:00 reads *chose option 2* (saw {rels_})",
          codes_ == [0, 0, 0] and rels_["AP-290"][:2] == ("option", 3) and rels_["AP-291"] == ("changed", 0, "")
          and rels_["AP-292"] == ("option", 2, "the relation only — no new verbs"))
    check(f"FM-029 · through `--answer`: a proposal typed with a double quote and a double space reads *the proposal*; a rejection reads *rejected* with its reason — and the signed lines are what `--answer` wrote, word unchanged",
          rels_["AP-293"] == ("proposal", 0, "") and rels_["AP-294"] == ("rejected", 0, "not this quarter — the audit comes first")
          and "\nanswer: \"accepted - ship 'the importer' first\"\n" in q_.read_text() and "\nanswer: \"accepted - a week of your choosing, 'shadow' only on weekdays\"\n" in d1_.read_text()
          and '\nanswer: "rejected - not this quarter — the audit comes first"\n' in r_.read_text())
    _, said_, _ = run(root, "--answered"); run(root, "--html-only"); page_ = (root / "docs/work-tracker/index.html").read_text(encoding="utf-8")
    check("FM-029 · `--answered` prints the relation beside each answer",
          "   answer: accepted - a week of your choosing, 'shadow' only on weekdays\n   relation: chose option 3: a week of your choosing, 'shadow' only…\n" in said_
          and "   relation: accepted with a change\n" in said_ and "   relation: chose option 2: the relation only — no new verbs\n" in said_
          and "   relation: accepted the proposal\n" in said_ and "   relation: rejected: not this quarter — the audit comes first\n" in said_)
    check("FM-029 · the board's tracker view carries the relation next to the answer, in the words of its labels — English built in, German in the table the tool ships",
          '"accepted - the relation only — no new verbs"' in page_ and '["option", 2, "the relation only — no new verbs"]]' in page_ and '["changed", 0, ""]]' in page_
          and 'l("relation."+r[0],r[1])' in page_ and '"relation.option": "chose option {0}"' in page_ and '"relation.unknown": "relation not computable"' in page_)
    run(root); git(root, "add", "-A"); git(root, "commit", "-qm", "the answers merged", "--author=holgo <h@x>")
    code_, out_, _ = run(root, "--clear-ask", "AP-292", "build"); body_ = f29_.read_text()
    run(root); git(root, "add", "-A"); git(root, "commit", "-qm", "AP-292 acted on", "--author=holgo <h@x>")
    fm.configure(root); t292_ = next(t for t in fm.load_trackers() if t["id"] == "AP-292"); _, said2_, _ = run(root, "--answered")
    check(f"FM-029 · `--clear-ask` writes the relation into the record under `## Asks` — the proposal and the options leave with the ask, the relation stays — and `--answered` names it on the acted-on line (saw {said2_.strip()[-160:]!r})",
          code_ == 0 and "**answered** — accepted - the relation only — no new verbs · holgo\n**relation** — chose option 2: the relation only — no new verbs\n" in body_
          and "ask-options:" not in body_.split("---")[1] and t292_["asks_relation"] == "chose option 2: the relation only — no new verbs"
          and "AP-292 — acted on in `" in said2_ and "` · chose option 2: the relation only — no new verbs" in said2_ and run(root, "--check")[0] == 0)
    rm_git(root)
fm.configure(HERE)
old_record_ = "# X-1 — t\n\n## Asks\n\n**2026-09-20** · Ship it?\n**answered** — accepted - ship it, S1 first · holgo\n\n## Ship log\n"
new_record_ = old_record_.replace("· holgo\n", "· holgo\n**relation** — accepted with a change\n")
withdrawn_ = "## Asks\n\n**2026-09-20** · Ship it?\n**withdrawn** — no answer was given\n"
check("FM-029 · read from the body alone, a record `--clear-ask` wrote before 0.18.1 says *relation not computable* — its proposal left with the ask, and the body guesses nothing; its answer is what the readings find the answer's commit by (below); a withdrawn one has no relation",
      fm.recorded_relation(old_record_) == "relation not computable" and fm.recorded_relation(new_record_) == "accepted with a change"
      and fm.recorded_relation(withdrawn_) == "" and fm.recorded_relation("# no asks\n") == ""
      and fm.unrelated_answer(old_record_) == "accepted - ship it, S1 first" and fm.unrelated_answer(new_record_) == ""
      and fm.unrelated_answer(withdrawn_) == "" and fm.unrelated_answer("# no asks\n") == "")

# --- FM-029, 0.18.3 (the Auditor seat's check 9): a record written before 0.18.1 prints the relation of its answer's commit -
# FM-031 and FM-032 on main were cleared by a tool that wrote no `**relation** —` line, and `--answered` printed *relation not
# computable* for both. The commit that wrote the answer still holds the proposal and the options: every reading reads them
# there — found by the answer's text, never guessed — and where no commit wrote that answer, it still says not computable.
with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp).resolve()
    subprocess.run(["git", "init", "-q", str(root)], check=True, env=_ENV)
    for k_, v_ in (("user.name", "holgo"), ("user.email", "h@x"), ("commit.gpgsign", "false")):
        git(root, "config", k_, v_)
    (root / "shoalmark.toml").write_text('name = "r"\nanswerers = ["holgo"]\n[kinds]\nAP = "Work"\n', encoding="utf-8")
    today_ = datetime.date.today().isoformat()
    q31_, q32_ = "Rule the three house rules and the build order?", "Rule the deregulation?"
    ask31_ = (f'next: owner\nask: "{q31_}"\nask-kind: ruling\nask-since: 2026-09-23\n'
              'ask-options: "all three rules now, S1 then S2 | the rules now, build nothing yet | S1 only, rules later"\nask-proposal: "all three rules now, S1 then S2"\n')
    ask32_ = f'next: owner\nask: "{q32_}"\nask-kind: ruling\nask-since: 2026-09-23\nask-options: "all four now | the review tier only | none"\nask-proposal: "all four now"\n'
    said_ = lambda a: f'answer: "{a}"\nanswered: {today_}\nanswered-by: holgo\n'
    changed_ = "accepted - one channel and the detached switch now, S1 then S2; the cap of 2 waiting pull requests revoked"
    # the clear as a tool before 0.18.1 made it: the ask lines gone, the exchange under `## Asks` with no relation line
    cleared_ = lambda tid, q, a, relation="": tracker(root, tid, extra="next: build\n", body=f"## Asks\n\n**{today_}** · {q}\n**answered** — {a} · holgo\n{relation}\n## Ship log\n")
    f310_ = tracker(root, "AP-310", extra=ask31_); tracker(root, "AP-311", extra=ask32_); tracker(root, "AP-312", extra=ask32_); tracker(root, "AP-313", extra=ask31_)
    git(root, "add", "-A"); git(root, "commit", "-qm", "the asks")
    # FM-031's history: the proposal answered first, then rewritten with changed text — the record holds the NEWER answer
    tracker(root, "AP-310", extra=ask31_ + said_("accepted - all three rules now, S1 then S2")); git(root, "commit", "-qam", "AP-310: accepted - the proposal")
    tracker(root, "AP-310", extra=ask31_ + said_(changed_)); tracker(root, "AP-311", extra=ask32_ + said_("accepted - all four now")); tracker(root, "AP-313", extra=ask31_ + said_(changed_))
    git(root, "commit", "-qam", "the answers")
    answer_sha_ = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"], capture_output=True, text=True, env=_ENV).stdout.strip()
    cleared_("AP-310", q31_, changed_); cleared_("AP-311", q32_, "accepted - all four now")
    cleared_("AP-312", q32_, "accepted - all four now, the freeze at 8")                   # an answer no commit ever wrote
    cleared_("AP-313", q31_, changed_, "**relation** — accepted with a change\n")        # a record from 0.18.1 on: its own line
    git(root, "commit", "-qam", "the asks acted on, cleared as a tool before 0.18.1 cleared them")
    fm.configure(root)
    load_calls_ = argv_of(fm.load_trackers)
    by_ = {t["id"]: t for t in fm.load_trackers()}
    batch_calls_ = argv_of(lambda: fm.recover_relations(list(by_.values())))
    got_ = {k: fm.record_relation(by_[k]) for k in ("AP-310", "AP-311", "AP-312", "AP-313")}
    t313_ = next(t for t in fm.load_trackers() if t["id"] == "AP-313"); line_calls_ = argv_of(lambda: fm.record_relation(t313_))
    check(f"FM-029 · 0.18.3 · a record written before 0.18.1 prints the relation of the commit that wrote its answer: FM-031's shape — the proposal answered, then changed text — reads *accepted with a change* from the NEWER answer's commit; FM-032's shape *accepted the proposal*; an answer no commit wrote *relation not computable*; a record with its line, that line (saw {got_})",
          got_["AP-310"][0] == "accepted with a change" and len(got_["AP-310"][1]) >= 7 and answer_sha_.startswith(got_["AP-310"][1])
          and got_["AP-311"][0] == "accepted the proposal" and answer_sha_.startswith(got_["AP-311"][1]) and len(got_["AP-311"][1]) >= 7
          and got_["AP-312"] == ("relation not computable", "") and got_["AP-313"] == ("accepted with a change", "")
          and "**relation**" not in f310_.read_text())
    check("FM-029 · 0.18.3 · its cost: a load spends no git call on it; a reading spends ONE `git log` for all the records that lack the line, and one `git show` per record whose commit was found — and a record that carries its line calls no git at all",
          not any(fm.line_regex("answer:") in c for c in load_calls_)
          and [c for c in batch_calls_ if "log" in c and fm.line_regex("answer:") in c] == [c for c in batch_calls_ if "log" in c] and len([c for c in batch_calls_ if "log" in c]) == 1
          and len([c for c in batch_calls_ if "show" in c]) == 2 and len(batch_calls_) == 3 and line_calls_ == [])
    _, said_out_, _ = run(root, "--answered")
    acted_ = dict(re.findall(r"^  (AP-31\d) — acted on in `[0-9a-f]+` · (.*)$", said_out_, re.M))
    check(f"FM-029 · 0.18.3 · `--answered` prints it on each acted-on line and names the answer's commit it was read from (saw {acted_})",
          acted_.get("AP-310") == f"accepted with a change, read from the answer's commit `{got_['AP-310'][1]}`"
          and acted_.get("AP-311") == f"accepted the proposal, read from the answer's commit `{got_['AP-311'][1]}`"
          and acted_.get("AP-312") == "relation not computable" and acted_.get("AP-313") == "accepted with a change")
    run(root, "--html-only")
    import json
    view_ = lambda tid: (lambda s: json.loads(s[s.index(",") + 1: s.rindex(")")]))((root / f"docs/work-tracker/view/{tid}.js").read_text(encoding="utf-8"))
    check("FM-029 · 0.18.3 · the board's tracker view prints it under the record's `**answered** —`, where a record from 0.18.1 on carries its own line, and names the commit — the file itself is not touched",
          f"**answered** — {changed_} · holgo\n**relation** — accepted with a change · read from the answer's commit `{got_['AP-310'][1]}`\n\n## Ship log" in view_("AP-310")
          and f"**answered** — accepted - all four now · holgo\n**relation** — accepted the proposal · read from the answer's commit `{got_['AP-311'][1]}`\n" in view_("AP-311")
          and "**answered** — accepted - all four now, the freeze at 8 · holgo\n**relation** — relation not computable\n" in view_("AP-312")
          and view_("AP-313") == fm.parse_frontmatter((root / "docs/work-tracker/AP-313-x.md").read_text())[1] and view_("AP-313").count("**relation**") == 1
          and "**relation**" not in f310_.read_text())
    rm_git(root)
fm.configure(HERE)

# --- FM-029, 0.18.3 (the cold second pass's R2): EVERY record without its relation line prints the recovered one, not the
#     newest alone — FM-031's older answer lost its relation once a newer exchange, recorded with its line, came after it ---
with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp).resolve()
    subprocess.run(["git", "init", "-q", str(root)], check=True, env=_ENV)
    for k_, v_ in (("user.name", "holgo"), ("user.email", "h@x"), ("commit.gpgsign", "false")):
        git(root, "config", k_, v_)
    (root / "shoalmark.toml").write_text('name = "r"\nanswerers = ["holgo"]\n[kinds]\nAP = "Work"\n', encoding="utf-8")
    day_ = datetime.date.today().isoformat()
    ask_ = lambda q, proposal, options: f'next: owner\nask: "{q}"\nask-kind: ruling\nask-since: 2026-09-23\nask-options: "{options}"\nask-proposal: "{proposal}"\n'
    said_ = lambda a: f'answer: "{a}"\nanswered: {day_}\nanswered-by: holgo\n'
    rec_ = lambda q, a, line="": f"**{day_}** · {q}\n**answered** — {a} · holgo\n{line}"
    q1_, q2_ = "Ship the importer first?", "Which week does the exporter take?"
    a1_, a2_ = "accepted - the importer, and the audit first", "accepted - next week"
    shas_ = {}
    for tid_ in ("AP-320", "AP-321"):                     # AP-320: two records without the line · AP-321: the old one, then one with it (FM-031's shape)
        tracker(root, tid_, extra=ask_(q1_, "the importer", "the importer | the exporter")); git(root, "add", "-A"); git(root, "commit", "-qm", f"{tid_}: asked")
        tracker(root, tid_, extra=ask_(q1_, "the importer", "the importer | the exporter") + said_(a1_)); git(root, "commit", "-qam", f"{tid_}: answered")
        shas_[(tid_, 1)] = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"], capture_output=True, text=True, env=_ENV).stdout.strip()
        tracker(root, tid_, extra=ask_(q2_, "next week", "this week | next week"), body=f"## Asks\n\n{rec_(q1_, a1_)}\n## Ship log\n")
        git(root, "commit", "-qam", f"{tid_}: cleared before 0.18.1, and asked again")
        tracker(root, tid_, extra=ask_(q2_, "next week", "this week | next week") + said_(a2_), body=f"## Asks\n\n{rec_(q1_, a1_)}\n## Ship log\n")
        git(root, "commit", "-qam", f"{tid_}: answered again")
        shas_[(tid_, 2)] = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"], capture_output=True, text=True, env=_ENV).stdout.strip()
        second_ = rec_(q2_, a2_, "**relation** — accepted the proposal\n" if tid_ == "AP-321" else "")
        tracker(root, tid_, extra="next: build\n", body=f"## Asks\n\n{rec_(q1_, a1_)}\n{second_}\n## Ship log\n")
        git(root, "commit", "-qam", f"{tid_}: cleared")
    fm.configure(root)
    by_ = {t["id"]: t for t in fm.load_trackers()}
    calls_ = argv_of(lambda: fm.recover_relations(list(by_.values())))
    run(root, "--html-only")
    import json
    view_ = lambda tid: (lambda s: json.loads(s[s.index(",") + 1: s.rindex(")")]))((root / f"docs/work-tracker/view/{tid}.js").read_text(encoding="utf-8"))
    v320_, v321_ = view_("AP-320"), view_("AP-321")
    line_ = lambda a, rel, sha: f"**answered** — {a} · holgo\n**relation** — {rel} · read from the answer's commit `{sha}`"
    s1_ = lambda tid: by_[tid]["asks_recovered_all"][(fm.answer_norm(q1_), fm.answer_norm(a1_))][1]
    check(f"FM-029 · R2 · every record under `## Asks` without its relation line prints the recovered one in the board's tracker view — two old records, each from its own answer's commit (saw {by_['AP-320'].get('asks_recovered_all')})",
          line_(a1_, "accepted with a change", s1_("AP-320")) in v320_ and shas_[("AP-320", 1)].startswith(s1_("AP-320"))
          and line_(a2_, "accepted the proposal", by_["AP-320"]["asks_recovered"][1]) in v320_ and shas_[("AP-320", 2)].startswith(by_["AP-320"]["asks_recovered"][1])
          and v320_.count("**relation** —") == 2)
    check("FM-029 · R2 · FM-031's shape — an old record, then one with its line: the old one prints its recovered relation, the newer keeps its own, nothing doubled; the newest-only reading (`--answered`) says the newest's",
          line_(a1_, "accepted with a change", s1_("AP-321")) in v321_ and v321_.count("**relation** —") == 2
          and f"**answered** — {a2_} · holgo\n**relation** — accepted the proposal\n" in v321_ and fm.record_relation(by_["AP-321"]) == ("accepted the proposal", ""))
    check("FM-029 · R2 · still one `git log` for every file, and one `git show` per record whose answer's commit is found — three here",
          len([c_ for c_ in calls_ if "log" in c_]) == 1 and len([c_ for c_ in calls_ if "show" in c_]) == 3 and len(calls_) == 4)
    rm_git(root)
fm.configure(HERE)

# --- FM-029, 0.18.3 (the cold third pass's R1): the same answer text closing two exchanges — each record is matched to ITS
#     answer's commit by its question; where the question cannot tell them apart, *relation not computable*, never a guess --
with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp).resolve()
    subprocess.run(["git", "init", "-q", str(root)], check=True, env=_ENV)
    for k_, v_ in (("user.name", "holgo"), ("user.email", "h@x"), ("commit.gpgsign", "false")):
        git(root, "config", k_, v_)
    (root / "shoalmark.toml").write_text('name = "r"\nanswerers = ["holgo"]\n[kinds]\nAP = "Work"\n', encoding="utf-8")
    day_ = datetime.date.today().isoformat()
    ask_ = lambda q, proposal: f'next: owner\nask: "{q}"\nask-kind: ruling\nask-since: 2026-09-22\nask-proposal: "{proposal}"\n'
    said_ = lambda a: f'answer: "{a}"\nanswered: {day_}\nanswered-by: holgo\n'
    rec_ = lambda q, a: f"**{day_}** · {q}\n**answered** — {a} · holgo\n"
    head_ = lambda: subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"], capture_output=True, text=True, env=_ENV).stdout.strip()
    def two_(tid, q1, p1, q2, p2):                         # two exchanges answered `accepted - yes`, each cleared as a tool before 0.18.1 cleared it
        shas = []
        tracker(root, tid, extra=ask_(q1, p1)); git(root, "add", "-A"); git(root, "commit", "-qm", f"{tid}: asked")
        tracker(root, tid, extra=ask_(q1, p1) + said_("accepted - yes")); git(root, "commit", "-qam", f"{tid}: accepted - yes"); shas.append(head_())
        tracker(root, tid, extra=ask_(q2, p2), body=f"## Asks\n\n{rec_(q1, 'accepted - yes')}\n## Ship log\n"); git(root, "commit", "-qam", f"{tid}: cleared, asked again")
        tracker(root, tid, extra=ask_(q2, p2) + said_("accepted - yes"), body=f"## Asks\n\n{rec_(q1, 'accepted - yes')}\n## Ship log\n")
        git(root, "commit", "-qam", f"{tid}: accepted - yes, again"); shas.append(head_())
        tracker(root, tid, extra="next: build\n", body=f"## Asks\n\n{rec_(q1, 'accepted - yes')}\n{rec_(q2, 'accepted - yes')}\n## Ship log\n")
        git(root, "commit", "-qam", f"{tid}: cleared")
        return shas
    sa_ = two_("AP-330", "Ship the importer?", "yes", "Ship the exporter this week?", "no")        # the Reviewer's case: two questions
    sb_ = two_("AP-331", "Ship the importer?", "yes", "Ship the importer?", "yes")                 # the same question, twice, the same answer
    fm.configure(root)
    by_ = {t["id"]: t for t in fm.load_trackers()}
    calls_ = argv_of(lambda: fm.recover_relations(list(by_.values())))
    run(root, "--html-only")
    import json
    view_ = lambda tid: (lambda s: json.loads(s[s.index(",") + 1: s.rindex(")")]))((root / f"docs/work-tracker/view/{tid}.js").read_text(encoding="utf-8"))
    got_ = by_["AP-330"]["asks_recovered_all"]
    k_ = lambda q: (fm.answer_norm(q), fm.answer_norm("accepted - yes"))
    check(f"FM-029 · R1 (third pass) · one answer text closing two exchanges: each record is matched to its own answer's commit by its question — the first *accepted the proposal*, the second *accepted with a change*, each naming its own commit (saw {got_})",
          got_[k_("Ship the importer?")][0] == "accepted the proposal" and sa_[0].startswith(got_[k_("Ship the importer?")][1]) and len(got_[k_("Ship the importer?")][1]) >= 7
          and got_[k_("Ship the exporter this week?")][0] == "accepted with a change" and sa_[1].startswith(got_[k_("Ship the exporter this week?")][1])
          and f"**answered** — accepted - yes · holgo\n**relation** — accepted the proposal · read from the answer's commit `{got_[k_('Ship the importer?')][1]}`" in view_("AP-330")
          and f"**answered** — accepted - yes · holgo\n**relation** — accepted with a change · read from the answer's commit `{got_[k_('Ship the exporter this week?')][1]}`" in view_("AP-330"))
    check(f"FM-029 · R1 (third pass) · the same answer to the same question, twice: the question cannot tell the commits apart — *relation not computable* under both records, no commit named (saw {by_['AP-331']['asks_recovered_all']})",
          by_["AP-331"]["asks_recovered_all"] == {k_("Ship the importer?"): ("relation not computable", "")}
          and view_("AP-331").count("**relation** — relation not computable\n") == 2 and "read from the answer's commit" not in view_("AP-331")
          and len([c_ for c_ in calls_ if "log" in c_]) == 1 and len([c_ for c_ in calls_ if "show" in c_]) == 4)
    rm_git(root)
fm.configure(HERE)
# …and FM-007 in this repository: answered twice, word for word, on 09-22 — `63e72b4` at 16:48 and `7521116` at 19:36, the same
# question. Its record, read without its relation line, is not computable: which of the two is its answer, nothing can say.
_f007 = next(p_ for p_ in (HERE / "work-tracker").glob("FM-007-*.md"))
_q007 = "Which closure for the signing doorway do you want first, knowing that the first two are enforcement and the third only a tripwire?"
_a007 = "accepted - a hardware key that needs a touch"
_writers = subprocess.run(["git", "-C", str(HERE), "log", "--full-history", "--format=%h", "-G", "^answer: \"" + _a007, "--", _f007.relative_to(HERE).as_posix()],
                          capture_output=True, text=True, env=_ENV).stdout.split()
_t007 = {"id": "FM-007", "file": _f007.name, "asks_answers": [(fm.answer_norm(_q007), fm.answer_norm(_a007))], "asks_key": (fm.answer_norm(_q007), fm.answer_norm(_a007))}
_no_git_env(lambda: fm.recover_relations([_t007]))
check(f"FM-029 · R1 (third pass) · FM-007's real double answer in this repository's history — 63e72b4 and 7521116, one question, one text — reads *relation not computable*, never the newer one's (saw {_writers}, {_t007['asks_recovered_all']})",
      {"63e72b4", "7521116"} <= {w_[:7] for w_ in _writers} and _t007["asks_recovered"] == ("relation not computable", ""))

# --- FM-029: the half-written answer's *give it again* knows all three words, and a superseding answer's flag ----------
with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp).resolve()
    subprocess.run(["git", "init", "-q", str(root)], check=True, env=_ENV)
    for k_, v_ in (("user.name", "holgo"), ("user.email", "h@x"), ("commit.gpgsign", "false")):
        git(root, "config", k_, v_)
    (root / "shoalmark.toml").write_text('name = "h"\nanswerers = ["holgo"]\n[kinds]\nAP = "Work"\n', encoding="utf-8")
    since_ = (datetime.date.today() - datetime.timedelta(days=1)).isoformat()
    lines_ = lambda q: f'next: owner\nask: "{q}"\nask-kind: ruling\nask-since: {since_}\nask-proposal: "yes"\n'
    a_ = tracker(root, "AP-296", extra=lines_("Ship the importer?") + f'answer: "accepted - yes"\nanswered: {since_}\nanswered-by: holgo\n')
    b_ = tracker(root, "AP-297", extra=lines_("Ship the exporter?") + f'answer: "accepted - yes"\nanswered: {since_}\nanswered-by: holgo\n')
    c_ = tracker(root, "AP-298", extra=lines_("Ship the reports?"))
    run(root); git(root, "add", "-A"); git(root, "commit", "-qm", "answered", "--author=holgo <h@x>")
    a_.write_text(a_.read_text().replace('answer: "accepted - yes"', 'answer: "revoked - the audit comes first"'), encoding="utf-8")
    b_.write_text(b_.read_text().replace('answer: "accepted - yes"', 'answer: "rejected - not this quarter"'), encoding="utf-8")
    code_, _, err_ = run(root, "--answer", "AP-298", "accept")
    check(f"FM-029 · the half-written-answer recovery reads `revoked` too — its *give it again* is `revoke \"<reason>\"` — and an answer that replaced a committed one is given again with `--supersede` (saw {err_.strip()[-300:]!r})",
          code_ == fm.EXIT_LINT and '--answer AP-296 revoke "the audit comes first"' in err_ and '--answer AP-296 revoke "the audit comes first" --supersede' not in err_
          and '--answer AP-297 reject "not this quarter" --supersede' in err_)
    rm_git(root)
fm.configure(HERE)

check("the vendored renderer is the pinned one — an update is a deliberate act",
      fm.digest(HERE / "vendor/marked-18.0.13.umd.js").startswith("b147274a9ce27d17"))
check("the version is the `VERSION` file and nothing else — one source of truth, so a release cannot ship a stale constant beside it",
      fm.__version__ == (HERE / "VERSION").read_text().strip() and re.fullmatch(r"\d+\.\d+\.\d+", fm.__version__) is not None)
check("the schema prints every key with who writes it", all(k in fm.render_schema() for k in ("`considered:`", "`kind-of-problem:`", "`blocked-by:`")) and "`target:`" not in fm.render_schema())

print()
if FAILS:
    print(f"FAILED: {len(FAILS)} — {', '.join(FAILS)}")
    sys.exit(1)
print("all green")
