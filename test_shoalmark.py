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
        fm.vendor(dest)
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
with tempfile.TemporaryDirectory() as d:
    dest = Path(d).resolve() / "tools" / "shoalmark"
    with redirect_stdout(io.StringIO()):
        fm.vendor(dest)
    # FM-009: `--vendor` compares the consumer's VERSION file against our version. While the version was ALSO declared
    # as a constant beside that file the two could drift — and did, for two releases — so a consumer pinned at the
    # stale constant read as up to date and the changelog it was owed was suppressed.
    check("what `--vendor` copies is what it reports — the version that lands in the copy is the version named",
          (dest / "VERSION").read_text().strip() == fm.__version__)
    (dest / "VERSION").write_text("0.2.0\n")
    (dest / "PIN").write_text("\n".join(f"{fm.digest(dest / l.partition('  ')[2])}  {l.partition('  ')[2]}" for l in (dest / "PIN").read_text().splitlines()) + "\n")
    out = io.StringIO()
    with redirect_stdout(out):
        fm.vendor(dest)
    check("vendoring again says which version it replaces and what changed since", "(was 0.2.0)" in out.getvalue() and "## 0.3.0" in out.getvalue() and "## 0.2.0" not in out.getvalue())
    (dest / "shoalmark.py").write_text("# edited\n")
    err = io.StringIO()
    with redirect_stderr(err):
        code = fm.vendor(dest)
    check("vendoring never overwrites a copy that was edited in place", code == fm.EXIT_LINT and "edited in place" in err.getvalue() and (dest / "shoalmark.py").read_text() == "# edited\n")
check("related skips German stop words as it skips English ones", "und" in fm._STOP and "the" in fm._STOP)

# --- the board, seen: rendered in a real browser where one is installed -------------------------------------
_CHROME_FLAGS = ["--no-sandbox"] if sys.platform.startswith("linux") else []     # a CI container has no user namespace for the sandbox
_CHROME = next((c for c in ("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", r"C:\Program Files\Google\Chrome\Application\chrome.exe", r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe", "/usr/bin/chromium", "/usr/bin/chromium-browser", "/usr/bin/google-chrome") if os.path.exists(c)), None)
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
desc.triage: was die nächste Sichtung auflistet — in Arbeit und nicht oder vor über {0} Tagen bewertet, dazu neue Einträge
desc.triaged: bewertet am {0} — jeder steht auch in seinem eigenen Abschnitt
desc.triaged.none: noch keine Sichtung gelaufen
desc.backlog: wartet — P0 bis P3, dann ohne Stufe, dann geparkt
desc.done: ausgeliefert oder geschlossen
group.none: ohne {0}
count.trackers: Einträge
count.open: offen
count.around: rund um {0}
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
            fm.vendor(dest)
        check("C7 · the organisation's brand travels with --vendor and is pinned like the rest of the copy",
              (dest / "brand/theme.css").read_text() == ":root{--blue:#123456}" and "brand/theme.css" in (dest / "PIN").read_text() and "brand/labels.yaml" in (dest / "PIN").read_text())
        (base / "client/docs/work-tracker").mkdir(parents=True)
        (base / "client/docs/work-tracker/MSR-001-x.md").write_text('---\nid: MSR-001\nstatus: Proposed\nconsidered: none\nhook: "h"\n---\n\n# MSR-001 — x\n')
        (base / "client/shoalmark.toml").write_text('[kinds]\nMSR = "Work"\n'); (base / "client/docs/work-tracker/brand").mkdir(); (base / "client/docs/work-tracker/brand/labels.yaml").write_text("footer: ours\n")
        r = subprocess.run([sys.executable, str(dest / "shoalmark.py"), "--root", str(base / "client")], capture_output=True, text=True, encoding="utf-8", errors="replace", env=dict(_ENV, XDG_CONFIG_HOME=str(base / "nowhere")))
        cpage = (base / "client/docs/work-tracker/index.html").read_text(encoding="utf-8")
        check("C7 · …and the client overrides it beside its own trackers, without touching the pinned copy", r.returncode == 0 and '"footer": "ours"' in cpage and "--blue:#123456" in cpage)
        with redirect_stdout(io.StringIO()):
            fm.brand_report(str(base / "starter"))
        starter = fm.read_flat((base / "starter/labels.yaml").read_text(encoding="utf-8"))
        check("--brand DIR writes a starter a person can edit: every label in English, and a theme that names the nine variables",
              starter == {k: v for k, v in fm.LABELS.items()} and all(v in (base / "starter/theme.css").read_text() for v in ("--bg", "--ink", "--dim", "--mute", "--line", "--teal", "--coral", "--blue", "--yellow")))
    finally:
        shutil.rmtree(org, ignore_errors=True)
        if _xdg is None:
            os.environ.pop("XDG_CONFIG_HOME", None)
        else:
            os.environ["XDG_CONFIG_HOME"] = _xdg
fm.configure(HERE)

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
        for en, de in fm.DEFAULTS["headings"].items(): x = x.replace(f"## {de}\n", "## " + {"state": "Was jetzt gilt", "why": "Warum", "done": "Fertig, wenn", "log": "Verlauf", "intent": "Die Absicht", "path": "Der aktuelle Weg", "passes": "Durchgänge", "asks": "Fragen"}[en] + "\n")
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
    sig = subprocess.run(["git", "-C", str(root), "log", "-1", "--format=%G? %GS %an %s"], capture_output=True, text=True, env=_ENV).stdout.strip()
    on = subprocess.run(["git", "-C", str(root), "branch", "--show-current"], capture_output=True, text=True, env=_ENV).stdout.strip()
    remote = subprocess.run(["git", "-C", str(base / "origin.git"), "branch"], capture_output=True, text=True, env=_ENV).stdout
    fm.configure(root); t_ = next(t for t in fm.load_trackers() if t["id"] == "AP-070")
    check("--answer accept with a change: cuts answer/<id> from the ask's branch, writes the three lines, commits SIGNED under the answerer, pushes — the ask has left the queue",
          code == 0 and on == "answer/ap-070" and sig.startswith("G h@x holgo AP-070: accepted - count one week first") and "answer/ap-070" in remote
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
    fm.configure(root); t_ = next(t for t in fm.load_trackers() if t["id"] == "AP-072")
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
    check("8 · `--answer` refuses an `answer/<id>` that exists and does not carry the ask — it would write the answer where the question is not",
          code == fm.EXIT_LINT and "its tip does not carry this ask" in err and subprocess.run(["git", "-C", str(root), "branch", "--show-current"], capture_output=True, text=True, env=_ENV).stdout.strip() != "answer/ap-301")
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
        fm.configure(HERE); run(HERE, "--vendor", str(root / "tools/shoalmark")); fm.configure(root)
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
