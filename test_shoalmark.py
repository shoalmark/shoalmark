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
import sys
import tempfile
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

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


def run(root, *argv):
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        code = fm.main(["--root", str(root), *argv])
    return code, out.getvalue(), err.getvalue()


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
          and hashlib.sha256((dest / "LICENSE-APACHE").read_bytes()).hexdigest().startswith("cfc7749b96f63bd3"))
    check("--vendor copies the tool and its one vendored renderer, and pins each by sha256",
          (dest / "shoalmark.py").exists() and (dest / "vendor/marked-18.0.13.umd.js").exists()
          and hashlib.sha256((dest / "shoalmark.py").read_bytes()).hexdigest() in pin)
    tracker(root, "FEAT-001", status="Proposed")
    tool = [sys.executable, str(dest / "shoalmark.py"), "--root", str(root)]
    ok = subprocess.run(tool, capture_output=True, text=True, env=_ENV)
    (dest / "shoalmark.py").write_text((dest / "shoalmark.py").read_text() + "\n# edited in place\n")
    bad = subprocess.run(tool, capture_output=True, text=True, env=_ENV)
    check("a vendored copy runs from where it sits — and one edited in place is refused by its own gate",
          ok.returncode == 0 and bad.returncode == fm.EXIT_LINT and "differs from its PIN" in bad.stderr)

# --- 0.3.0: what a second repository taught ---------------------------------------------------------------
check("the configuration is read without a library — the subset --init writes, a refusal by line for anything else",
      fm.read_config('name = "a # b"  # c\nn = 7\nflag = true\n[kinds]\nMSR = "Work" # x\n') == {"name": "a # b", "n": 7, "flag": True, "kinds": {"MSR": "Work"}}
      and (lambda: [True for _ in [0] if not _try(lambda: fm.read_config('x = [1, 2]\n'))])())
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
    tracker(root, "MSR-001", extra="rank: 1\ntier: P1\nnext: owner\n"); tracker(root, "MSR-002", extra="rank: 2\ntier: P1\nnext: build\n")
    code, out, _ = run(root, "--next")
    check("--next lists the ranked work in order with each move and what is true now, and starts a seat on the first move that is its own",
          code == 0 and out.index("#1 MSR-001") < out.index("#2 MSR-002") and "One thing is left." in out and "START WITH: MSR-002" in out and "MSR-002 first" in out and "](" not in out)
    code, out, _ = run(root, "--install-hook")
    hook = root / ".git/hooks/pre-commit"
    check("--install-hook writes plain, executable git hooks that stage exactly what the command wrote",
          code == 0 and hook.exists() and os.access(hook, os.X_OK) and "--print-written" in hook.read_text() and (root / ".git/hooks/post-merge").exists())
    git(root, "add", "-A"); git2 = subprocess.run(["git", "-C", str(root), "-c", "commit.gpgsign=false", "commit", "-qm", "x"], capture_output=True, text=True, env=_ENV)
    check("the installed hook runs on a real commit and stages the regenerated INDEX", git2.returncode == 0
          and "INDEX.md" in subprocess.run(["git", "-C", str(root), "show", "--name-only", "--format=", "HEAD"], capture_output=True, text=True, env=_ENV).stdout)
    hook.write_text("#!/bin/sh\n# somebody else's hook\n")
    code, _, err = run(root, "--install-hook")
    check("a hook that is not shoalmark's is never overwritten — it is named, with the line to add", code == fm.EXIT_LINT and "left alone" in err and "somebody else" in hook.read_text())
fm.configure(HERE)
with tempfile.TemporaryDirectory() as d:
    dest = Path(d).resolve() / "tools" / "shoalmark"
    with redirect_stdout(io.StringIO()):
        fm.vendor(dest)
    (dest / "VERSION").write_text("0.2.0\n")
    (dest / "PIN").write_text("\n".join(f"{hashlib.sha256((dest / l.partition('  ')[2]).read_bytes()).hexdigest()}  {l.partition('  ')[2]}" for l in (dest / "PIN").read_text().splitlines()) + "\n")
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
_CHROME = next((c for c in ("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "/usr/bin/chromium", "/usr/bin/chromium-browser", "/usr/bin/google-chrome") if os.path.exists(c)), None)
if _CHROME:
    with tempfile.TemporaryDirectory() as d:
        root = Path(d).resolve()
        run(root, "--init", "--key", "msr")
        tracker(root, "MSR-001", title="Stock is booked per warehouse"); tracker(root, "MSR-002", status="Shipped", title="A shipped one")
        run(root)
        dom = lambda frag: subprocess.run([_CHROME, "--headless=new", "--disable-gpu", "--virtual-time-budget=4000", "--dump-dom",
                                           f"file://{root}/docs/work-tracker/index.html{frag}"], capture_output=True, text=True, timeout=60).stdout
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
tags = set(subprocess.run(["git", "-C", ask["root"], "tag", "--list"], capture_output=True, text=True).stdout.split())
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
    (root / "docs/work-tracker/theme.css").write_text(":root{--bg:#123456}")
    code, _, err = run(root)
    index, page = (root / "docs/work-tracker/INDEX.md").read_text(), (root / "docs/work-tracker/index.html").read_text()
    check("one model, two renderings: the deriver says which values INDEX.md prints and which the board shows — every one stays a view",
          code == 0 and "| Triaged | Ver |" in index and "Release |" not in index and 'COLS=["Ver", "Release"],BCOLS=["Release"]' in page and '<th class="x">release<th>title' in page)
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
    check("a repository's own look is a convention, not a setting: `theme.css` beside the trackers is appended to the page's style", "--bg:#123456}</style>" in page)
    os.environ["SHOALMARK_CMD"] = "python3 scripts/tracker.py"
    try:
        fm.configure(root); (root / "docs/work-tracker/INDEX.md").write_text("stale"); code, _, err = run(root, "--check")
    finally:
        del os.environ["SHOALMARK_CMD"]
    check("a repository that wraps the tool is named by its own command in every message", code == fm.EXIT_DRIFT and "Run: python3 scripts/tracker.py" in err)
    if _CHROME:
        run(root)
        body = subprocess.run([_CHROME, "--headless=new", "--disable-gpu", "--virtual-time-budget=4000", "--dump-dom", f"file://{root}/docs/work-tracker/index.html"], capture_output=True, text=True, timeout=60).stdout
        shown = re.sub(r"<[^>]+>", " ", body[body.find("<tbody"):body.find("</tbody>")])
        check("the board's cell shows the display form, rendered", "→ 1.3.x" in shown)
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
      hashlib.sha256((HERE / "vendor/marked-18.0.13.umd.js").read_bytes()).hexdigest().startswith("b147274a9ce27d17"))
check("the schema prints every key with who writes it", all(k in fm.render_schema() for k in ("`considered:`", "`kind-of-problem:`", "`blocked-by:`")) and "`target:`" not in fm.render_schema())

print()
if FAILS:
    print(f"FAILED: {len(FAILS)} — {', '.join(FAILS)}")
    sys.exit(1)
print("all green")
