"""FM-032, R15: the filing freeze goes; looking before filing and the ranking stay. With `freeze_at` set and trackers open,
`--new` files a tracker that is no defect, after the closest trackers, and one line names the key that is no longer read;
`--check` names it the same way and exits 0. A key the freeze read is named, never refused (R26) — a value the freeze
refused, too. Without the keys, no line. Also run by test_core.py.

Run alone: `python3 test_freeze_removed.py`. It tests the shoalmark.py beside this file, as a program, in a throwaway repository.
"""

import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
TRACKERS = "work-tracker"
_ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
_ENV.update(GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t", GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@t",
            SHOALMARK_CMD="python3 shoalmark.py", PYTHONIOENCODING="utf-8")
BASE = ('name = "freeze"\ntracker_dir = "work-tracker"\n{keys}[kinds]\nFEAT = "Features"\n'
        '[tags]\nbug = "something that does not work"\nprocess = "how the work is done"\n')
# The line R15 owes a configuration that sets a key of the freeze, spelled out here rather than read back from the tool.
TAIL = (" not read — R15, the Owner's ruling of 12 October, removed the filing freeze, so every filing is written; looking before "
        "filing (`--new` prints the closest trackers first, `--related`) and the ranking (`rank:`, `--triage`, `--next`) stay. Delete the line")
SAID = {("freeze_at",): "shoalmark.toml: `freeze_at` is" + TAIL, ("freeze_at", "freeze_tag"): "shoalmark.toml: `freeze_at` and `freeze_tag` are" + TAIL}


def _tracker(tid, status, extra=""):
    return (f'---\nid: {tid}\nstatus: {status}\nconsidered: none\n{extra}hook: "the export drops a row, {tid}"\n---\n\n# {tid} — x\n\n'
            "## What is true now\n\n**One thing is left.**\n\n## Done when\n\nit is.\n").encode("utf-8")


def run_freeze_removed_controls(fm, check):
    """FM-032, R15: no freeze refuses a filing; a configuration's freeze key is named in one line, never refused."""
    print("\nFM-032 · R15: the filing freeze is gone — `--new` files, a freeze key is named in one line, never refused")
    tool = Path(fm.__file__).resolve()
    with tempfile.TemporaryDirectory() as tmp:
        root, hooks = Path(tmp).resolve() / "repo", Path(tmp).resolve() / "no-hooks"
        folder = root / TRACKERS
        folder.mkdir(parents=True)
        hooks.mkdir()

        def git(*a):
            subprocess.run(["git", "-C", str(root), *a], check=True, capture_output=True, env=_ENV)

        def run(*argv):
            r = subprocess.run([sys.executable, str(tool), "--root", str(root), *argv], capture_output=True, env=_ENV, cwd=str(root))
            return r.returncode, r.stdout.decode("utf-8", errors="replace"), r.stderr.decode("utf-8", errors="replace")

        def config(keys):
            (root / "shoalmark.toml").write_bytes(BASE.format(keys=keys).encode("utf-8"))

        def filed(code, out):
            """The tracker `--new` wrote, given `considered: none` so the gate takes it, and INDEX.md regenerated — or None."""
            m = re.search(r"wrote (work-tracker/FEAT-\d+-[^ ]+\.md)", out)
            if code != 0 or not m:
                return None
            path = root / m.group(1)
            path.write_bytes(path.read_bytes().replace(b"considered:\n", b"considered: none\n", 1))
            run()
            return path

        git("init", "-q")
        for key, value in (("core.hooksPath", str(hooks)), ("core.autocrlf", "false"), ("commit.gpgsign", "false")):
            git("config", key, value)
        (root / ".gitignore").write_bytes(f"{TRACKERS}/index.html\n{TRACKERS}/view/\n".encode("utf-8"))
        (folder / "FEAT-001-x.md").write_bytes(_tracker("FEAT-001", "In Progress", "triaged: 2026-10-01\ntier: P2\nrank: 1\n"))
        (folder / "FEAT-002-x.md").write_bytes(_tracker("FEAT-002", "Proposed"))
        (folder / "TRIAGE.md").write_bytes("# Triage\n\n## The intent\n\n- **for** — freeze\n\n## The current path\n\n"
                                           "1. [FEAT-001](FEAT-001-x.md) to its end.\n\n## Passes\n\nNewest first.\n\n*None yet.*\n".encode("utf-8"))
        config("freeze_at = 1\n")
        written = run()
        git("add", "-A")
        git("commit", "-qm", "the base")

        code, out, err = run("--related", "the export drops a row")
        check(f"FM-032 · R15 · looking before filing stays: `--related` lists the closest trackers (saw {code}: {out.strip()[:200]!r})",
              code == 0 and "FEAT-001" in out and "FEAT-002" in out)

        # Two open trackers, `freeze_at = 1`: the freeze would have refused any filing without `bug`.
        code, out, err = run("--new", "FEAT", "the export drops a row: a process change, no defect", "--tags", "process")
        path = filed(code, out)
        check(f"FM-032 · R15 · `freeze_at = 1`, two trackers open: `--new … --tags process` files the tracker, exit 0, after the closest trackers, "
              f"and one line names the key (saw {code}: {err.strip()!r})",
              written[0] == 0 and code == 0 and path is not None and "tags: process" in path.read_text(encoding="utf-8")
              and "the closest trackers that exist" in out and err.splitlines().count(SAID[("freeze_at",)]) == 1)
        code, out, err = run("--new", "FEAT", "another change, with no tag")
        path = filed(code, out)
        check(f"FM-032 · R15 · …and a filing with no tag at all is written too, the key named once (saw {code}: {err.strip()!r})",
              code == 0 and path is not None and err.splitlines().count(SAID[("freeze_at",)]) == 1)
        code, out, err = run("--check")
        check(f"FM-032 · R15 · `--check` exits 0 and names the key in the same one line, and nothing of a freeze holding (saw {code}: {(out + err).strip()[-500:]!r})",
              code == 0 and (out + err).splitlines().count(SAID[("freeze_at",)]) == 1 and "filing freeze:" not in out + err)

        # Never refused (R26): both keys, and values the freeze itself refused — each named, the run as it is without them.
        for n, (keys, which) in enumerate((('freeze_at = 8\nfreeze_tag = "bug"\n', ("freeze_at", "freeze_tag")), ("freeze_at = -1\n", ("freeze_at",)),
                                           ('freeze_at = "many"\nfreeze_tag = ""\n', ("freeze_at", "freeze_tag")))):
            config(keys)
            code, out, err = run("--check")
            code_n, out_n, err_n = run("--new", "FEAT", f"a filing, case {n + 1}")
            check(f"FM-032 · R15 · {keys.strip()!r}: never refused — `--check` exits 0 and `--new` files, each naming {which} in one line "
                  f"(saw {code}, {code_n}: {(err + err_n).strip()[-400:]!r})",
                  code == 0 and code_n == 0 and (out + err).splitlines().count(SAID[which]) == 1 and err_n.splitlines().count(SAID[which]) == 1)
            filed(code_n, out_n)

        # Without the keys: no line.
        config("")
        code, out, err = run("--new", "FEAT", "a filing, the last case", "--tags", "process")
        filed(code, out)
        code_c, out_c, err_c = run("--check")
        check(f"FM-032 · R15 · without either key, `--new` and `--check` say nothing of them (saw {code}, {code_c}: {(err + out_c + err_c).strip()[-300:]!r})",
              code == 0 and code_c == 0 and "freeze" not in out + err + out_c + err_c)
        code, out, _ = run("--schema")
        check("FM-032 · R15 · `--schema` documents neither key, and `--help` names no freeze",
              code == 0 and "freeze_at" not in out and "freeze_tag" not in out and "freeze" not in run("--help")[1])


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

    run_freeze_removed_controls(_fm, _check)
    print(f"\n{'FAILED: ' + str(len(_fails)) if _fails else 'all green'}")
    sys.exit(1 if _fails else 0)
