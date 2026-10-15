"""FM-032, R21: INDEX.md merges cleanly. Two branches change different trackers on different days. Each regenerates and
commits. `git merge-tree --write-tree` reports no conflict in INDEX.md in either merge order, and `--check` on the merge
is clean. Also run by test_core.py.

Run alone: `python3 test_index_merges.py`. It tests the shoalmark.py beside this file, as a program, in a throwaway
repository, with the day patched for each run. It needs git 2.38 or later for `merge-tree --write-tree`.

Where git itself conflicts, the case is a named limit, and the test pins it: the conflict is in INDEX.md alone, and it
holds the two trackers' rows and nothing else. Git conflicts when both sides change adjacent lines, or insert at the same
place (L1 to L3 below).
"""

import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
TRACKERS = "docs/work-tracker"
INDEX = f"{TRACKERS}/INDEX.md"

# The tool as a program, on a given day: `datetime.date.today()` answers that day. The tool reads the day nowhere else.
_ON_DAY = (
    "import datetime, runpy, sys\n"
    "d = datetime.date.fromisoformat(sys.argv[1])\n"
    "class _Day(datetime.date):\n"
    "    @classmethod\n"
    "    def today(cls):\n"
    "        return cls(d.year, d.month, d.day)\n"
    "datetime.date = _Day\n"
    "sys.argv = sys.argv[2:]\n"
    "runpy.run_path(sys.argv[0], run_name='__main__')\n"
)
_ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
_ENV.update(GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t", GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@t",
            SHOALMARK_CMD="python3 shoalmark.py", PYTHONIOENCODING="utf-8")

BASE_DAY, MERGE_DAY, LATER_DAY = "2026-10-01", "2026-11-01", "2027-01-01"
# The base: two kinds' tables and the triage table. Features sort In Progress 006 005 004 003 002, Proposed 009 008 007,
# Shipped 001. Bugs sort 002, 003, 001. Triage ranks 1 FEAT-002, 3 FEAT-003, 5 FEAT-004, 7 FEAT-005, 9 BUG-002, 10 FEAT-006.
_RANKED = "triaged: 2026-01-05\ntier: P2\n"
BASE = {
    "FEAT-001": ("Shipped", ""), "FEAT-002": ("In Progress", _RANKED + "rank: 1\n"), "FEAT-003": ("In Progress", _RANKED + "rank: 3\n"),
    "FEAT-004": ("In Progress", _RANKED + "rank: 5\n"), "FEAT-005": ("In Progress", _RANKED + "rank: 7\n"),
    "FEAT-006": ("In Progress", _RANKED + "rank: 10\n"), "FEAT-007": ("Proposed", ""), "FEAT-008": ("Proposed", ""),
    "FEAT-009": ("Proposed", ""), "BUG-001": ("Shipped", ""), "BUG-002": ("In Progress", _RANKED + "rank: 9\n"),
    "BUG-003": ("Proposed", ""),
}


def _write(path, text):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def _read(path):
    with open(path, encoding="utf-8", newline="") as f:
        return f.read()


def _tracker(root, tid, status, extra="", hook=None):
    _write(root / TRACKERS / f"{tid}-x.md",
           f'---\nid: {tid}\nstatus: {status}\n{extra}hook: "{hook or "the hook of " + tid}"\n---\n\n# {tid} — x\n\n'
           "## What is true now\n\n**One thing is left.**\n\n## Done when\n\nit is.\n")


def _rehook(tid):
    def change(root):
        status, extra = BASE[tid]
        _tracker(root, tid, status, extra, hook=f"the hook of {tid}, changed on its branch")
    return change


def _rerank(tid, rank):
    def change(root):
        status, extra = BASE[tid]
        _tracker(root, tid, status, re.sub(r"rank: \d+", f"rank: {rank}", extra))
    return change


def _file(tid):
    return lambda root: _tracker(root, tid, "Proposed", "considered: none\n")


# Each change is one branch from the base, regenerated and committed on its own day, so any two are on different days.
CHANGES = {
    "FEAT-006's hook": _rehook("FEAT-006"), "FEAT-008's hook": _rehook("FEAT-008"), "FEAT-009's hook": _rehook("FEAT-009"),
    "FEAT-007's hook": _rehook("FEAT-007"), "BUG-003's hook": _rehook("BUG-003"), "FEAT-003's hook": _rehook("FEAT-003"),
    "FEAT-010 filed": _file("FEAT-010"), "FEAT-011 filed": _file("FEAT-011"), "BUG-004 filed": _file("BUG-004"),
    "FEAT-005 moved from rank 7 to rank 2": _rerank("FEAT-005", 2),
}
# (case, one branch, the other, None where the merge is clean, else the named limit it pins)
CASES = [
    ("one table, rows apart", "FEAT-006's hook", "FEAT-008's hook", None),
    ("one table, one row between", "FEAT-009's hook", "FEAT-007's hook", None),
    ("one table, adjacent rows", "FEAT-009's hook", "FEAT-008's hook",
     "L1: the two rows are adjacent lines in the Features table, and git conflicts on changes to adjacent lines"),
    ("two kinds' tables", "FEAT-007's hook", "BUG-003's hook", None),
    ("a filing and a change", "FEAT-010 filed", "FEAT-006's hook", None),
    ("two filings in two kinds' tables", "FEAT-010 filed", "BUG-004 filed", None),
    ("two filings in one table, the same status", "FEAT-010 filed", "FEAT-011 filed",
     "L2: both new rows sort to the head of the Proposed rows, so both branches insert at the same line"),
    ("a triage move and a change", "FEAT-005 moved from rank 7 to rank 2", "FEAT-006's hook", None),
    ("a triage move next to a changed row", "FEAT-005 moved from rank 7 to rank 2", "FEAT-003's hook",
     "L3: the moved row lands right above FEAT-003's, the row the other branch changed; the ranking places it there"),
]


def _ids(*changes):
    return {re.match(r"(?:FEAT|BUG)-\d+", c).group(0) for c in changes}


def run_index_merge_controls(fm, check):
    """FM-032, R21: INDEX.md holds no line that changes with the day or with another tracker, so tracker branches merge."""
    print("\nFM-032 · R21: INDEX.md merges cleanly — two branches, different trackers, different days, both merge orders")
    tool = Path(fm.__file__).resolve()
    with tempfile.TemporaryDirectory() as tmp:
        root, hooks = Path(tmp).resolve() / "repo", Path(tmp).resolve() / "no-hooks"
        (root / TRACKERS).mkdir(parents=True)
        hooks.mkdir()

        def git(*a, ok=(0,)):
            r = subprocess.run(["git", "-C", str(root), *a], capture_output=True, text=True, encoding="utf-8", errors="replace", env=_ENV)
            if r.returncode not in ok:
                raise RuntimeError(f"git {' '.join(a)}: exit {r.returncode}: {r.stderr.strip()[:300]}")
            return r

        def run(day, *argv):
            r = subprocess.run([sys.executable, "-c", _ON_DAY, day, str(tool), "--root", str(root), *argv],
                               capture_output=True, text=True, encoding="utf-8", errors="replace", env=_ENV, cwd=str(root))
            return r.returncode, r.stdout, r.stderr

        def index():
            return _read(root / INDEX)

        git("init", "-q")
        for key, value in (("core.hooksPath", str(hooks)), ("core.autocrlf", "false"), ("commit.gpgsign", "false"),
                           ("merge.conflictStyle", "merge"), ("user.name", "t"), ("user.email", "t@t")):
            git("config", key, value)
        git("symbolic-ref", "HEAD", "refs/heads/base")
        _write(root / "shoalmark.toml", 'name = "merges"\n[kinds]\nFEAT = "Features"\nBUG = "Bugs"\n[considered_from]\nFEAT = 10\nBUG = 4\n')
        _write(root / ".gitignore", f"{TRACKERS}/index.html\n{TRACKERS}/view/\n")
        _write(root / TRACKERS / "TRIAGE.md", "# Triage\n\n## The intent\n\n- **for** — merges\n\n## The current path\n\n"
                                              "1. [FEAT-002](FEAT-002-x.md) to its end.\n\n## Passes\n\nNewest first.\n\n*None yet.*\n")
        for tid, (status, extra) in BASE.items():
            _tracker(root, tid, status, extra)
        written = run(BASE_DAY)
        git("add", "-A")
        git("commit", "-qm", "the base")
        base, base_index = git("rev-parse", "HEAD").stdout.strip(), index()
        green = run(BASE_DAY, "--check")
        check(f"FM-032 · R21 · the fixture's base: written and `--check` green (saw {written[0]}, {green[0]}: {(written[2] + green[2]).strip()[:300]!r})",
              written[0] == green[0] == fm.EXIT_OK and "STALE" not in green[2])

        # No line changes with the day: the same trackers, generated on another day, give the same bytes.
        run(LATER_DAY)
        check("FM-032 · R21 · INDEX.md generated on another day is the same, byte for byte — no line holds the date",
              index() == base_index and "Generated" not in base_index)

        # The STALE check: the previous version's dated, counted line is not drift; a real difference still is.
        old_line = "\n>\n> Generated 2026-09-30 · 12 trackers (9 features, 3 bugs)."
        old_index = base_index.replace("\n\n## Triage", old_line + "\n\n## Triage", 1)
        feat7 = next(l for l in base_index.splitlines() if l.startswith("| [FEAT-007]("))
        rank3 = next(l for l in base_index.splitlines() if l.startswith("| 3 | "))
        edits = {
            "a row changed by hand": base_index.replace(feat7, feat7.replace("the hook of FEAT-007", "the hook, edited"), 1),
            "a row missing": base_index.replace(feat7 + "\n", "", 1),
            "a row added": base_index.replace(feat7 + "\n", feat7 + "\n" + feat7.replace("FEAT-007", "FEAT-077") + "\n", 1),
            "a triage row changed by hand": base_index.replace(rank3, rank3.replace("| 3 |", "| 4 |"), 1),
            "the previous version's line beside a row changed by hand":
                old_index.replace(feat7, feat7.replace("the hook of FEAT-007", "the hook, edited"), 1),
        }
        _write(root / INDEX, old_index)
        upgraded = run(MERGE_DAY, "--check")
        run(MERGE_DAY)
        dropped = index()
        check(f"FM-032 · R21 · an INDEX.md the previous version wrote, with its dated, counted line, is not STALE, and the next run "
              f"drops the line (saw {upgraded[0]}: {upgraded[2].strip()[:200]!r})",
              old_index != base_index and upgraded[0] == fm.EXIT_OK and "STALE" not in upgraded[2] and "up to date" in upgraded[1] + upgraded[2]
              and dropped == base_index)
        for name, text in edits.items():
            _write(root / INDEX, text)
            code, _out, err = run(MERGE_DAY, "--check")
            check(f"FM-032 · R21 · {name}: STALE, exit {fm.EXIT_DRIFT} (saw {code})", text != base_index and code == fm.EXIT_DRIFT and "STALE" in err)
        _write(root / INDEX, base_index)

        heads = {}
        for n, (key, change) in enumerate(CHANGES.items()):
            git("checkout", "-q", "-B", f"change-{n}", base)
            change(root)
            day = f"2026-10-{n + 2:02d}"
            code, _out, err = run(day)
            git("add", "-A")
            git("commit", "-qm", key)
            heads[key] = git("rev-parse", "HEAD").stdout.strip()
            if code != fm.EXIT_OK:
                check(f"FM-032 · R21 · the branch `{key}` regenerates green on {day} (saw {code}: {err.strip()[:300]!r})", False)

        for case, one, other, limit in CASES:
            ids, seen, good = _ids(one, other), [], True
            for ours, theirs in ((one, other), (other, one)):
                r = git("merge-tree", "--write-tree", "--name-only", "--no-messages", heads[ours], heads[theirs], ok=(0, 1))
                tree, conflicted = r.stdout.splitlines()[0], r.stdout.splitlines()[1:]
                if limit is None:
                    merged = git("commit-tree", tree, "-p", heads[ours], "-p", heads[theirs], "-m", f"merge: {case}").stdout.strip()
                    git("checkout", "-q", "--detach", merged)
                    code, out, err = run(MERGE_DAY, "--check")
                    good = good and r.returncode == 0 and not conflicted and code == fm.EXIT_OK and "STALE" not in err and "up to date" in out + err
                    seen.append(f"{r.returncode}, {conflicted}, --check {code}{': ' + err.strip()[:200] if code else ''}")
                else:
                    text = git("cat-file", "-p", f"{tree}:{INDEX}").stdout.splitlines()
                    held, inside = [], False
                    for line in text:
                        if line.startswith(("<<<<<<< ", ">>>>>>> ")):
                            inside = line.startswith("<")
                        elif inside and line != "=======":
                            held.append(line)
                    good = (good and r.returncode == 1 and conflicted == [INDEX] and bool(held)
                            and all(line.startswith("| ") and any(f"[{i}](" in line for i in ids) for line in held))
                    seen.append(f"{r.returncode}, {conflicted}, the conflict holds {held}")
            if limit is None:
                check(f"FM-032 · R21 · {case} — `{one}` and `{other}`: no conflict in either merge order, and `--check` on the merge is clean "
                      f"(saw {seen})", good)
            else:
                check(f"FM-032 · R21 · the named limit, {case} — `{one}` and `{other}`: git conflicts in INDEX.md alone, on those "
                      f"trackers' rows and nothing else, in both orders. {limit} (saw {seen})", good)
        git("checkout", "-q", "--detach", base)


if __name__ == "__main__":
    import importlib.util
    for _s in (sys.stdout, sys.stderr):
        _s.reconfigure(encoding="utf-8", errors="replace")
    _spec = importlib.util.spec_from_file_location("fm", HERE / "shoalmark.py")
    _fm = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(_fm)
    _fails = []

    def _check(name, ok):
        print(("  ok    " if ok else "  FAIL  ") + name)
        if not ok:
            _fails.append(name)

    run_index_merge_controls(_fm, _check)
    print(f"\n{'FAILED: ' + str(len(_fails)) if _fails else 'all green'}")
    sys.exit(1 if _fails else 0)
