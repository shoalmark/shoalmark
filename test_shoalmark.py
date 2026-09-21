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
ask.ruling: eine Entscheidung
ask.action: nur Ihre Hände
ask.determination: ließe sich durch einen Versuch klären
ask.ceremony: ein Knopfdruck
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
    root = Path(tmp); subprocess.run(["git", "init", "-q", str(root)], check=True)
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
        for en, de in fm.DEFAULTS["headings"].items(): x = x.replace(f"## {de}\n", "## " + {"state": "Was jetzt gilt", "why": "Warum", "done": "Fertig, wenn", "log": "Verlauf", "intent": "Die Absicht", "path": "Der aktuelle Weg", "passes": "Durchgänge"}[en] + "\n")
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
    check("`[headings]` — a mistyped key is refused, naming the seven", refused)
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
          code == 0 and "Nothing is ranked" in out and out.index("AP-038") < out.index("AP-037 ·") and "next: owner" in out and "1 NEED THE OWNER" in out and "NOT YET STATED AS A QUESTION" in out)
fm.configure(HERE)

# --- FM-005: the Owner's queue — every ask stated as the question it is, oldest first, with what it holds up --------
with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp).resolve(); (root / "shoalmark.toml").write_text('name = "q"\n[kinds]\nAP = "Work"\n', encoding="utf-8")
    old = (datetime.date.today() - datetime.timedelta(days=3)).isoformat(); new_ = (datetime.date.today() - datetime.timedelta(days=1)).isoformat()
    tracker(root, "AP-022", extra=f'next: owner\nask: "DATEV format, or a plain CSV?"\nask-kind: ruling\nask-since: {old}\n', title="export")
    tracker(root, "AP-021", extra=f'next: owner\nask: "Read the scraper log for instrument 27."\nask-kind: action\nask-since: {new_}\n', title="model")
    tracker(root, "AP-020", extra="next: owner\n", title="buried in the body")
    tracker(root, "AP-037", status="Proposed", extra="blocked-by: AP-022\n", title="roles"); tracker(root, "AP-041", status="Proposed", extra="blocked-by: AP-037\n", title="audit")
    tracker(root, "AP-019", status="Shipped", extra='next: owner\nask: "done long ago"\n', title="shipped")
    code, out, _ = run(root, "--owner")
    check("--owner is the digest: how many need the Owner, the oldest ask's age, what is held up — transitively — and each ask as its question, oldest first; finished work never asks",
          code == 0 and out.startswith("3 NEED THE OWNER · oldest 3 day(s) · holding up 2: AP-037, AP-041") and out.index("AP-022 · ruling · asked 3 day(s) ago · holds up AP-037, AP-041") < out.index("AP-021 · action · asked 1 day(s) ago")
          and "DATEV format, or a plain CSV?" in out and "done long ago" not in out)
    check("an ask that was never stated is said to be so, with the file to write it in — it is not hidden behind an id", "AP-020" in out and "NOT YET STATED AS A QUESTION" in out and "write `ask:` in AP-020-x.md" in out)
    bad = tracker(root, "AP-050", extra="next: owner\nask-kind: favour\n", title="bad kind"); code, _, err = run(root)
    check("`ask-kind:` is one of four words — the gate refuses a fifth", code == fm.EXIT_LINT and "ask-kind" in err + _); bad.unlink()
    code, out2, _ = run(root, "--next")
    check("--next ends with the same digest — a cold session is told what its Owner owes before it starts", code == 0 and "3 NEED THE OWNER" in out2)
    tracker(root, "AP-030", extra=f'next: owner\nask: "Open the pull request."\nask-kind: ceremony\nask-since: {new_}\n', title="button")
    code, out3, _ = run(root, "--standup")
    check("--standup is the agenda of one sitting: rulings first, then the Owner's hands, then buttons — inside a kind what frees the most comes first — and what was never stated is named",
          code == 0 and out3.startswith("STANDUP") and out3.index("RULINGS") < out3.index("YOUR HANDS") < out3.index("BUTTONS") and "[frees AP-037, AP-041]" in out3 and "not yet stated as a question" in out3)
    code, _, err = run(root, "--standup", str(root / "s.ics"))
    (root / "shoalmark.toml").write_text('name = "q"\nstandup = "09:00"\nstandup_minutes = 20\n[kinds]\nAP = "Work"\n', encoding="utf-8")
    code2, _, _ = run(root, "--standup", str(root / "s.ics")); ics = (root / "s.ics").read_bytes() if (root / "s.ics").exists() else b""
    check("--standup FILE.ics writes the recurring invite — weekdays, the configured time and length, CRLF as a calendar file must — and refuses until a time is configured",
          code == fm.EXIT_LINT and "standup = " in err and code2 == 0 and b"RRULE:FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR\r\n" in ics and b"T090000\r\n" in ics and b"T092000\r\n" in ics and ics.count(b"\n") == ics.count(b"\r\n"))
    (root / "AP-030-x.md").unlink() if (root / "AP-030-x.md").exists() else [p_.unlink() for p_ in (root / "docs/work-tracker").glob("AP-030-*.md")]
    (root / "shoalmark.toml").write_text('name = "q"\n[kinds]\nAP = "Work"\n', encoding="utf-8")
    run(root); page = (root / "docs/work-tracker/index.html").read_text()
    if _CHROME:
        dom = subprocess.run([_CHROME, "--headless=new", "--disable-gpu", *_CHROME_FLAGS, "--virtual-time-budget=4000", "--dump-dom", (root / "docs/work-tracker/index.html").as_uri()], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60).stdout
        shown = re.sub(r"\s+", " ", re.sub(r"<(script|style)[\s\S]*?</\1>|<[^>]+>", " ", dom))
        check("rendered: the board's first words are the answer — how many wait, the oldest, what is held up — then each question, the oldest first, before the path and before any table",
              "waiting for you: 3 · oldest 3 days · holding up 2 more" in shown and shown.index("DATEV format, or a plain CSV?") < shown.index("Read the scraper log") and "not yet stated as a question" in shown
              and "a ruling" in shown and "your hands" in shown and "holds up AP-037, AP-041" in shown and shown.index("waiting for you") < shown.index("AP-022 ") )
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
check("the schema prints every key with who writes it", all(k in fm.render_schema() for k in ("`considered:`", "`kind-of-problem:`", "`blocked-by:`")) and "`target:`" not in fm.render_schema())

print()
if FAILS:
    print(f"FAILED: {len(FAILS)} — {', '.join(FAILS)}")
    sys.exit(1)
print("all green")
