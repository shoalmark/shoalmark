"""FM-032, R13: the ratio command goes; the records classification a move to `Shipped` reads stays. `--ratio`, `--since` and
`--until` each print one line that R13 removed them and that no counting view replaces them until the receipts ship, and
exit 2; `--help` names none of them. A move to `Shipped` tells a commit behind the change from a records-only one as it did
at b84b8af: a records-only merge is not behind it, a product merge is, and a path `[ratio] exclude` names is product to it, as
it always was. A `[ratio]` key nothing reads is named by `--check`, never refused (R26). Also run by test_core.py.

Run alone: `python3 test_ratio_removed.py`. It tests the shoalmark.py beside this file, as a program, in throwaway
repositories. `run_records_class_controls(tool, check)` runs the classification half against any copy of the tool.
"""

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
_ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
_ENV.update(GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t", GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@t",
            SHOALMARK_CMD="python3 shoalmark.py", PYTHONIOENCODING="utf-8")
# The lines R13 owes each flag, spelled out here rather than read back from the tool.
SAID = {flag: f"{flag}: R13, the Owner's ruling of 12 October, removed it{'' if flag == '--ratio' else ' with --ratio'} — "
              "no counting view replaces it until the receipts ship" for flag in ("--ratio", "--since", "--until")}
# Shipped's verdicts, as the tool at b84b8af gives them: "" is a commit behind the change.
VERDICTS = {"records-only": "changes nothing outside the records (work-tracker/)", "product": "", "excluded": ""}
_VERDICTS_PY = (
    "import importlib.util, json, sys\n"
    "spec = importlib.util.spec_from_file_location('fm', sys.argv[1]); fm = importlib.util.module_from_spec(spec); spec.loader.exec_module(fm)\n"
    "fm.configure(sys.argv[2]); names = json.loads(sys.argv[3])\n"
    "records = fm.ship_records()\n"
    "print(json.dumps({'records': records, 'verdicts': fm.git_ship_verdicts(list(names.values()), ['HEAD'], records)}))\n"
)


def _repo(top, name, config):
    root = Path(top) / name
    (root / "work-tracker").mkdir(parents=True)

    def git(*a):
        return subprocess.run(["git", "-C", str(root), "-c", "commit.gpgsign=false", "-c", "core.hooksPath=" + os.devnull, *a],
                              check=True, capture_output=True, env=_ENV).stdout.decode("utf-8").strip()

    git("init", "-q", "-b", "main")
    git("config", "core.autocrlf", "false")
    (root / "shoalmark.toml").write_bytes(config.encode("utf-8"))
    (root / ".gitignore").write_bytes(b"work-tracker/index.html\nwork-tracker/view/\n")
    (root / "README.md").write_bytes(b"start\n")
    git("add", "-A")
    git("commit", "-q", "-m", "start")
    return root, git


def _merge(git, root, name, files):
    """A pull request as the forge merges it: one commit on a branch, then `--no-ff` into main. Returns the merge."""
    git("switch", "-q", "-c", name, "main")
    for rel, data in files.items():
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        (root / rel).write_bytes(data)
    git("add", "-A")
    git("commit", "-q", "-m", name)
    git("switch", "-q", "main")
    git("merge", "-q", "--no-ff", "-m", "Merge " + name, name)
    return git("rev-parse", "HEAD")


def run_records_class_controls(tool, check, label="FM-032 · R13"):
    """Shipped's records classification, on a records-only merge, a product merge and a path `[ratio] exclude` names — with `[ratio]`
    set and without it. The verdicts are b84b8af's (VERDICTS)."""
    tool = Path(tool).resolve()
    with tempfile.TemporaryDirectory() as top:
        for name, folder, config, records in (
                ("with [ratio]", "with-ratio", 'name = "r"\ntracker_dir = "work-tracker"\n\n[ratio]\nrecords = ["work-tracker/"]\nexclude = ["vendor/"]\n', ["work-tracker/"]),
                ("without [ratio]", "without-ratio", 'name = "r"\ntracker_dir = "work-tracker"\n', ["work-tracker/"])):
            root, git = _repo(top, folder, config)
            merges = {"records-only": _merge(git, root, "records", {"work-tracker/a.md": b"a record\n"}),
                      "product": _merge(git, root, "product", {"src/a.py": b"print(1)\n"}),
                      "excluded": _merge(git, root, "excluded", {"vendor/x.js": b"x\n"})}
            r = subprocess.run([sys.executable, "-c", _VERDICTS_PY, str(tool), str(root), json.dumps(merges)], capture_output=True, env=_ENV)
            out = r.stdout.decode("utf-8", errors="replace")
            got = json.loads(out) if r.returncode == 0 and out.strip() else {}
            seen = {kind: got.get("verdicts", {}).get(sha) for kind, sha in merges.items()}
            check(f"{label} · Shipped's records classification, {name}: the records are {records}; a records-only merge "
                  f"changes nothing outside them, a product merge is behind the change, and a path `exclude` names is product to it — "
                  f"as at b84b8af (saw {got.get('records')}, {seen}; {r.stderr.decode('utf-8', 'replace').strip()[-300:]!r})",
                  got.get("records") == records and seen == VERDICTS)


def run_ratio_removed_controls(fm, check):
    """FM-032, R13: the three flags are named and exit 2; --help names none of them; a [ratio] key nothing reads is named."""
    print("\nFM-032 · R13: `--ratio`, `--since` and `--until` are named and exit 2; Shipped's records classification is as it was")
    tool = Path(fm.__file__).resolve()
    with tempfile.TemporaryDirectory() as top:
        root, git = _repo(top, "flags", 'name = "r"\ntracker_dir = "work-tracker"\n\n[ratio]\nrecords = ["work-tracker/"]\n')

        def run(*argv):
            r = subprocess.run([sys.executable, str(tool), "--root", str(root), *argv], capture_output=True, env=_ENV, cwd=str(root))
            return r.returncode, r.stdout.decode("utf-8", errors="replace"), r.stderr.decode("utf-8", errors="replace")

        before = sorted(p.relative_to(root).as_posix() for p in root.rglob("*") if ".git" not in p.parts)
        for argv, flags in ((["--ratio"], ["--ratio"]), (["--since", "2026-10-01"], ["--since"]), (["--until", "2026-10-14"], ["--until"]),
                            (["--ratio", "--since", "2026-09-22", "--until", "2026-09-29"], ["--ratio", "--since", "--until"]),
                            (["--until", "2026-10-14", "--queue"], ["--until"])):
            code, out, err = run(*argv)
            check(f"FM-032 · R13 · `{' '.join(argv)}`: exit 2, and one line for each of {flags} — R13 removed it, no counting view "
                  f"replaces it until the receipts ship (saw {code}: {err.strip()!r})",
                  code == 2 and out == "" and err.splitlines() == [SAID[f] for f in flags])
        after = sorted(p.relative_to(root).as_posix() for p in root.rglob("*") if ".git" not in p.parts)
        check(f"FM-032 · R13 · the three flags read nothing and write nothing (saw {sorted(set(after) ^ set(before))})", after == before)
        code, out, _ = run("--help")
        check("FM-032 · R13 · `--help` names none of `--ratio`, `--since`, `--until`",
              code == 0 and "--check" in out and not any(f in out for f in ("--ratio", "--since", "--until")))
        for backend in ("svn", "git"):
            said = fm.cli_preflight(fm.parse_args(["--ratio", "--until", "2026-10-14"]), backend)
            check(f"FM-032 · R13 · under {backend}, the flags are named before anything is read, exit 2 (saw {said!r})",
                  said == (SAID["--ratio"] + "\n" + SAID["--until"], 2))

        # `--check` names a [ratio] key nothing reads, and `exclude`, which nothing counts with now — never a refusal (R26)
        run()
        git("add", "-A")
        git("commit", "-q", "-m", "the index")
        code, out, err = run("--check")
        check(f"FM-032 · R13 · `[ratio]` with `records` alone: `--check` exits 0 and names nothing of it (saw {code}: {(out + err).strip()[-300:]!r})",
              code == 0 and "[ratio]" not in out + err)
        (root / "shoalmark.toml").write_bytes(b'name = "r"\ntracker_dir = "work-tracker"\n\n[ratio]\nrecords = ["work-tracker/"]\nexclude = ["vendor/"]\ndays = 7\n')
        code, out, err = run("--check")
        check(f"FM-032 · R13 · `[ratio]` with `exclude` and a key nothing reads: `--check` exits 0 and names each, once (saw {code}: {(out + err).strip()[-500:]!r})",
              code == 0 and (out + err).count("shoalmark.toml: `[ratio]` `days` is not read — `[ratio]` holds `records` and `exclude`; R13 removed the ratio it counted") == 1
              and (out + err).count("shoalmark.toml: `[ratio] exclude` is kept as written, but nothing counts with it since R13 removed `--ratio`") == 1)
        code, out, _ = run("--schema")
        check("FM-032 · R13 · `--schema` still lists both `[ratio]` keys, and says what a move to `Shipped` reads",
              code == 0 and "`[ratio] records`" in out and "`[ratio] exclude`" in out and "a move to `Shipped`" in out)
    run_records_class_controls(tool, check)


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

    run_ratio_removed_controls(_fm, _check)
    print(f"\n{'FAILED: ' + str(len(_fails)) if _fails else 'all green'}")
    sys.exit(1 if _fails else 0)
