"""FM-044 P support: actual Git entry/process differential controls.

Outside proposal only. No handler, boundary, subprocess result or outcome is
mocked. Does not repeat generic schema/new/index/board/check/triage/session-new
pairs. Exercises clean/dirty origin selection and actual mixed-flag priorities.
All commits/configuration/remote setup are disposable fixture preparation;
production starts are reads and local generation only, with no push/hooks.
"""
import argparse
import base64
import hashlib
import json
import os
from pathlib import Path
import runpy
import shutil
import stat
import subprocess
import sys
import tempfile
import time


HERE = Path(__file__).resolve().parent
MARKER = "__GIT_ENTRY_DIFFERENTIAL__"
PAYLOAD = ("VERSION", "NOTICE", "LICENSE-APACHE", "LICENSE-MIT", "CHANGELOG.md", "README.md", "vendor/marked-18.0.13.umd.js")
POISON_KEYS = ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_PREFIX", "GIT_LITERAL_PATHSPECS", "GIT_ICASE_PATHSPECS", "GIT_GLOB_PATHSPECS", "GIT_NOGLOB_PATHSPECS")


def remove_tree(path):
    """`shutil.rmtree` that makes a refused entry writable and removes it again. Git writes its object files read-only, and Windows
    refuses to delete a read-only file (PR #173's run 38589202689, RV-3234). The handler is `onexc` from Python 3.12, `onerror` before."""
    def writable(function, target, _error):
        os.chmod(target, os.lstat(target).st_mode | stat.S_IWRITE)
        function(target)
    if sys.version_info >= (3, 12):
        shutil.rmtree(path, onexc=writable)
    else:
        shutil.rmtree(path, onerror=writable)


def serial(value):
    if isinstance(value, os.PathLike):
        return {"pathlike": os.fspath(value)}
    if isinstance(value, bytes):
        return {"bytes_base64": base64.b64encode(value).decode()}
    if isinstance(value, (tuple, list)):
        return [serial(item) for item in value]
    if isinstance(value, dict):
        return {str(key): serial(item) for key, item in sorted(value.items())}
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    return {"type": type(value).__name__}


def observe(spec):
    """Runs the actual __main__ entry, passively auditing/profile-observing it."""
    tool = str(Path(spec["tool"]).resolve())
    starts, calls, writes, entries = [], [], [], []
    active = [True]
    pending = {}

    def stack(frame=None):
        frame = frame or sys._getframe(1)
        names = []
        while frame:
            if frame.f_code.co_filename == tool:
                names.append(frame.f_code.co_name)
            frame = frame.f_back
        return list(reversed(names))

    def audit(event, arguments):
        if not active[0]:
            return
        if event == "subprocess.Popen":
            executable, argv, cwd, env = arguments
            starts.append({"executable": serial(executable), "argv": serial(argv),
                           "cwd": str(Path(os.fsdecode(cwd)).resolve()) if cwd is not None else os.getcwd(),
                           "environment": serial(dict(os.environ) if env is None else env),
                           "explicit_environment": env is not None, "product_stack": stack()})
            if executable is None and isinstance(argv, str):        # Windows' audit shape (RV-3061): `invoke` reads its argv back
                starts[-1]["raw"] = argv
        elif event == "open":
            path, mode, flags = arguments
            if flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND):
                if isinstance(path, (str, bytes, os.PathLike)):
                    writes.append({"event": event, "path": os.path.abspath(os.fsdecode(path)), "flags": flags})
        elif event in ("os.mkdir", "os.remove", "os.rmdir", "os.rename", "os.symlink", "os.link", "os.chmod", "os.truncate"):
            row = {"event": event}
            for position in (0, 1) if event in ("os.rename", "os.symlink", "os.link") else (0,):
                raw = arguments[position]
                if isinstance(raw, (str, bytes, os.PathLike)):
                    row["path" if position == 0 else "destination"] = os.path.abspath(os.fsdecode(raw))
            writes.append(row)

    def profile(frame, event, result):
        if frame.f_code is subprocess.run.__code__:
            if event == "call":
                row = {"args": serial(frame.f_locals.get("popenargs")),
                       "options": serial(frame.f_locals.get("kwargs")),
                       "capture_output": frame.f_locals.get("capture_output"),
                       "timeout": frame.f_locals.get("timeout"),
                       "check": frame.f_locals.get("check"), "input": serial(frame.f_locals.get("input")),
                       "product_stack": stack(frame)}
                calls.append(row); pending[id(frame)] = row
            elif event == "return":
                row = pending.pop(id(frame), None)
                if row is not None:
                    row["result"] = ({"args": serial(result.args), "returncode": result.returncode,
                                      "stdout": serial(result.stdout), "stderr": serial(result.stderr)}
                                     if isinstance(result, subprocess.CompletedProcess) else {"type": type(result).__name__})
        if frame.f_code.co_filename == tool and frame.f_code.co_name == "main" and event == "return":
            entries.append({"result": serial(result), "ASK_ORIGIN": frame.f_globals.get("_ASK_ORIGIN"),
                            "WALK": frame.f_globals.get("_WALK"), "ROOT": str(frame.f_globals.get("ROOT")),
                            "COMMITTING": frame.f_globals.get("COMMITTING")})

    sys.addaudithook(audit)
    sys.setprofile(profile)
    sys.argv = [tool, *spec["argv"]]
    code = 0
    try:
        runpy.run_path(tool, run_name="__main__")
    except SystemExit as error:
        code = error.code if isinstance(error.code, int) else 1 if error.code else 0
    finally:
        sys.setprofile(None); active[0] = False
    report = {"starts": starts, "run_calls": calls, "writes": writes, "main_returns": entries}
    print(MARKER + json.dumps(report, ensure_ascii=True), file=sys.stderr)
    return code


def snapshot(root):
    """Consumer bytes, symlinks and stable Git administrative state; no index-stat cache."""
    files = {}
    for path in root.rglob("*"):
        rel = path.relative_to(root).as_posix()
        if rel.startswith(".git/") and not (rel in (".git/config", ".git/HEAD", ".git/packed-refs") or rel.startswith((".git/refs/", ".git/hooks/"))):
            continue
        if path.is_symlink():
            files[rel] = {"symlink": os.readlink(path)}
        elif path.is_file():
            files[rel] = hashlib.sha256(path.read_bytes()).hexdigest()
    return files


def clean_environment(top, git):
    # Controlled fixture environment; no inherited tokens or credential variables.
    home, temporary = top / "home", top / "temporary"
    home.mkdir(); temporary.mkdir()
    env = {key: os.environ[key] for key in ("SystemRoot", "WINDIR", "COMSPEC", "PATHEXT") if key in os.environ}
    paths = [str(Path(git).parent), str(Path(sys.executable).parent)]
    if os.name != "nt":
        paths += ["/usr/bin", "/bin"]
    env.update(PATH=os.pathsep.join(dict.fromkeys(paths)), HOME=str(home), USERPROFILE=str(home),
               TMPDIR=str(temporary), TMP=str(temporary), TEMP=str(temporary),
               LANG="C.UTF-8", LC_ALL="C.UTF-8", TZ="UTC", PYTHONDONTWRITEBYTECODE="1",
               GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull, GIT_TERMINAL_PROMPT="0",
               GIT_AUTHOR_NAME="fixture-only", GIT_AUTHOR_EMAIL="fixture@example.invalid",
               GIT_COMMITTER_NAME="fixture-only", GIT_COMMITTER_EMAIL="fixture@example.invalid",
               GIT_AUTHOR_DATE="2026-10-13T08:00:00+00:00", GIT_COMMITTER_DATE="2026-10-13T08:00:00+00:00",
               SHOALMARK_CMD="shoalmark")
    return env


def invoke(tool, root, flags, cwd, env):
    spec = {"tool": str(tool), "argv": ["--root", str(root), *flags]}
    before = snapshot(root)
    result = subprocess.run([sys.executable, "-B", str(Path(__file__).resolve()), "--observe", json.dumps(spec)],
                            cwd=cwd, env=env, capture_output=True, text=True, encoding="utf-8", errors="strict", timeout=45)
    lines = result.stderr.splitlines(keepends=True)
    markers = [line[len(MARKER):] for line in lines if line.startswith(MARKER)]
    if len(markers) != 1:
        raise AssertionError("actual observer did not complete: " + result.stderr[-1800:])
    report = json.loads(markers[0])
    if any("raw" in row for row in report["starts"]):
        from test_vcs_entry import read_back                        # the suite's reading of a Windows line (`fm.split_cmdline`), here in the parent
        for row in report["starts"]:
            if "raw" in row:
                row["argv"] = read_back(row["raw"])
    report.update(status=result.returncode, stdout=result.stdout,
                  stderr="".join(line for line in lines if not line.startswith(MARKER)), before=before, after=snapshot(root),
                  source_sha256=hashlib.sha256(tool.read_bytes()).hexdigest(), flags=flags,
                  invocation_cwd=str(cwd), consumer=str(root), invocation_environment=serial(env))
    return report


def run_git_entry_differentials(candidate, baseline, *, payload, check=None, report_path=None):
    """Portable proposed helper: returns evidence and boolean controls; P owns composition."""
    started = time.monotonic()
    git = shutil.which("git")
    if not git:
        raise RuntimeError("actual Git CLI differential controls require Git")
    candidate, baseline, payload = Path(candidate).resolve(), Path(baseline).resolve(), Path(payload).resolve()
    immutable = {"baseline": hashlib.sha256(baseline.read_bytes()).hexdigest(), "candidate": hashlib.sha256(candidate.read_bytes()).hexdigest()}
    rows, checks = [], []
    from test_vcs_entry import same_start                           # an exact start: Windows' raw line against list2cmdline, POSIX's list

    def assert_control(label, passed):
        checks.append({"name": label, "pass": bool(passed)})
        if check:
            check(label, bool(passed))

    cases = (
        ("clean-check-origin", ["--check"], "clean", True, True),
        ("dirty-check-fallback", ["--check"], "dirty", False, True),
        ("clean-default-origin", [], "clean", True, False),
        ("dirty-default-fallback", [], "dirty", False, False),
        ("schema-check-priority", ["--schema", "--check"], "clean", False, True),
        ("session-before-schema-new", ["--session-check", "--schema", "--new", "WORK", "ignored later title"], "pending-session", False, True),
        ("session-before-ratio-window", ["--session-check", "--since", "2026-10-01", "--schema"], "pending-session", False, True),
        ("check-print-written-priority", ["--check", "--print-written"], "clean", False, True),
        ("html-only-standalone-priority", ["--html-only", "--check"], "clean", False, True),
        ("ratio-window-before-queue", ["--since", "2026-10-01", "--queue"], "clean", False, True),
        ("check-ratio-window-before-queue", ["--check", "--since", "2026-10-01", "--queue"], "clean", False, True),
        ("related-check-before-origin", ["--related", "WORK-001", "--check"], "clean", False, True),
    )
    with tempfile.TemporaryDirectory(prefix="git-entry-", dir=HERE) as directory:
        top = Path(directory).resolve()
        env = clean_environment(top, git)
        root, source_home, launch = top / "consumer", top / "source", top / "launch"
        root.mkdir(); source_home.mkdir(); launch.mkdir()
        (launch / "shoalmark.toml").write_text('name = "decoy launch; never the consumer"\n')
        for name in PAYLOAD:
            target = source_home / name; target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(payload / name, target)
        tool = source_home / "shoalmark.py"
        tool.write_bytes(baseline.read_bytes())

        def setup(*args, cwd=root):
            return subprocess.run([git, *args], cwd=cwd, env=env, capture_output=True, check=True).stdout.decode()

        setup("-c", "init.templateDir=", "init", "-q", "--initial-branch=main")
        for key, value in (("user.name", "fixture-only"), ("user.email", "fixture@example.invalid"),
                           ("commit.gpgsign", "false"), ("core.autocrlf", "false"), ("seat.session", "12345678/builder-1")):
            setup("config", key, value)
        folder = root / "work-tracker"; folder.mkdir()
        config = 'name = "Git entry differential fixture"\ntracker_dir = "work-tracker"\n[seats]\nbuilder = "fixture@example.invalid"\n[kinds]\nWORK = "Work"\n'
        (root / "shoalmark.toml").write_text(config)
        (folder / "WORK-001-local.md").write_text('---\nid: WORK-001\nstatus: Proposed\nconsidered: none\nhook: "entry origin selection"\n---\n\n# WORK-001 — local\n\n## What is true now\n\nRead current local work.\n\n## Done when\n\nOrigin and local edits select the correct change.\n')
        (folder / "TRIAGE.md").write_text('# Triage\n\n## The intent\n\nRead local records.\n\n## The current path\n\nPrepare local entry behavior.\n')
        (root / "product.txt").write_text("product\n")
        (root / ".gitignore").write_text("work-tracker/index.html\nwork-tracker/view/\n")
        setup("add", "-A")
        setup("commit", "-qm", "WORK-001: fixture baseline\n\nSession: 12345678/builder-1")
        prepared = invoke(tool, root, [], launch, env)
        assert prepared["status"] == 0, prepared["stderr"]
        setup("add", "work-tracker/INDEX.md")
        setup("commit", "-qm", "WORK-001: generated fixture index\n\nSession: 12345678/builder-1")
        origin = top / "local-origin.git"
        setup("clone", "--bare", "-q", str(root), str(origin), cwd=top)
        setup("remote", "add", "origin", str(origin))
        setup("update-ref", "refs/remotes/origin/main", "HEAD")
        # Deliberately absent origin/HEAD requires a real local ls-remote on a clean walk.
        assert setup("status", "--porcelain", "--untracked-files=all") == ""
        saved = top / "saved-consumer"
        shutil.copytree(root, saved)

        # A real foreign repository supplies inherited hook context. All eight
        # contamination keys are present only during measured entry runs; setup
        # remains clean. If any survive nested_git_env, they redirect repository
        # reads or conflict over pathspec semantics instead of being inert labels.
        foreign = top / "foreign-hook-context"
        foreign.mkdir()
        setup("-c", "init.templateDir=", "init", "-q", "--initial-branch=foreign", cwd=foreign)
        setup("config", "commit.gpgsign", "false", cwd=foreign)
        (foreign / "foreign.txt").write_text("foreign repository; never the consumer\n")
        setup("add", "-A", cwd=foreign)
        setup("commit", "-qm", "disposable foreign hook context", cwd=foreign)
        poisoned_env = dict(env, GIT_DIR=str(foreign / ".git"), GIT_WORK_TREE=str(foreign),
                            GIT_INDEX_FILE=str(foreign / ".git" / "index"), GIT_PREFIX="foreign/",
                            GIT_LITERAL_PATHSPECS="1", GIT_ICASE_PATHSPECS="1",
                            GIT_GLOB_PATHSPECS="1", GIT_NOGLOB_PATHSPECS="1")
        foreign_before = snapshot(foreign)

        for label, flags, condition, ask, readonly in cases:
            pair = []
            for version, chosen in (("baseline", baseline), ("candidate", candidate)):
                remove_tree(root); shutil.copytree(saved, root)
                tool.write_bytes(chosen.read_bytes())
                if condition == "dirty":
                    (root / "product.txt").write_text("product local edit\n")
                elif condition == "pending-session":
                    (root / "product.txt").write_text("pending product edit\n")
                    setup("add", "product.txt"); setup("config", "seat.session", "malformed")
                initial_status = setup("status", "--porcelain", "--untracked-files=all")
                assert bool(initial_status) == (condition != "clean"), (label, initial_status)
                entry_env = poisoned_env if label in ("clean-check-origin", "dirty-check-fallback", "clean-default-origin", "dirty-default-fallback") else env
                observed = invoke(tool, root, flags, launch, entry_env)
                observed.update(case=label, version=version, initial_git_status=initial_status,
                                foreign_before=foreign_before, foreign_after=snapshot(foreign))
                rows.append(observed); pair.append(observed)
            before, after = pair
            label_prefix = "Git entry " + label + ": "
            assert_control(label_prefix + "actual stdout/stderr/status match immutable baseline",
                           (before["status"], before["stdout"], before["stderr"]) == (after["status"], after["stdout"], after["stderr"]))
            strip_stack = lambda entries: [{key: value for key, value in row.items() if key != "product_stack"} for row in entries]
            assert_control(label_prefix + "all actual process argv/effective cwd/env match", strip_stack(before["starts"]) == strip_stack(after["starts"]))
            assert_control(label_prefix + "run options and actual process results match", strip_stack(before["run_calls"]) == strip_stack(after["run_calls"]))
            assert_control(label_prefix + "consumer byte/symlink/ref/config/hook snapshots match", before["before"] == after["before"] and before["after"] == after["after"])
            assert_control(label_prefix + "actual main state/result and selected origin policy match", before["main_returns"] == after["main_returns"]
                           and bool(after["main_returns"]) and after["main_returns"][-1]["ASK_ORIGIN"] is ask)
            assert_control(label_prefix + "Git entry emits no SVN limitation", "protected SVN acceptance" not in before["stdout"] + before["stderr"] + after["stdout"] + after["stderr"])
            assert_control(label_prefix + "production writes confined to disposable fixture", all(Path(value).is_relative_to(top)
                           for observed in pair for write in observed["writes"] for key, value in write.items() if key in ("path", "destination")))
            assert_control(label_prefix + "foreign hook repository bytes/refs/config remain unchanged", all(observed["foreign_before"] == observed["foreign_after"] for observed in pair))
            if readonly:
                assert_control(label_prefix + "read-only entry leaves consumer snapshot identical", all(observed["before"] == observed["after"] for observed in pair))
            if label in ("clean-check-origin", "dirty-check-fallback", "clean-default-origin", "dirty-default-fallback"):
                main_probe = lambda observed: [row for row in observed["starts"] if same_start(row["argv"], row.get("raw"), ["git", "diff", "--name-only", "--relative", "--ignore-submodules=none", "HEAD"])
                                              and "main" in row["product_stack"] and "worktree_edited" in row["product_stack"]
                                              and "read_changes" not in row["product_stack"]]
                probes = [main_probe(observed) for observed in pair]
                assert_control(label_prefix + "converted main probe actually runs once at consumer cwd", all(len(probe) == 1 and probe[0]["cwd"] == str(root) for probe in probes))
                assert_control(label_prefix + "converted probe drops all eight actual hook/pathspec contamination keys", all(set(POISON_KEYS).issubset(observed["invocation_environment"])
                               and len(probe) == 1 and not set(POISON_KEYS).intersection(probe[0]["environment"]) for observed, probe in zip(pair, probes)))
                assert_control(label_prefix + "candidate routes that probe through common boundary", all("vcs_process" in row["product_stack"] for row in probes[1])
                               and all("vcs_process" not in row["product_stack"] for row in probes[0]))
                if condition == "dirty":
                    assert_control(label_prefix + "dirty tree selects uncommitted fallback", all(observed["main_returns"][-1]["WALK"] == "uncommitted" for observed in pair))
                if label == "clean-default-origin":
                    assert_control(label_prefix + "clean default actually reads local origin once", all(sum(same_start(row["argv"], row.get("raw"), ["git", "ls-remote", "--symref", "origin", "HEAD"]) for row in observed["starts"]) == 1 for observed in pair))
                if label == "dirty-default-fallback":
                    assert_control(label_prefix + "dirty default asks no origin", all(not any(row["argv"][1:2] == ["ls-remote"] for row in observed["starts"]) for observed in pair))
    assert immutable == {"baseline": hashlib.sha256(baseline.read_bytes()).hexdigest(), "candidate": hashlib.sha256(candidate.read_bytes()).hexdigest()}
    report = {"kind": "outside proposed Git entry differential evidence; no review/READY", "sources": immutable,
              "checks": checks, "cases": rows, "seconds": round(time.monotonic() - started, 3),
              "case_count": len(cases), "actual_entry_runs": len(rows), "actual_process_starts": sum(len(row["starts"]) for row in rows),
              "host": sys.platform, "python": sys.version, "git": subprocess.check_output([git, "--version"]).decode().strip(),
              "snapshot_scope": "all consumer non-administrative files/symlinks plus Git refs/config/HEAD/hooks; excludes Git object/index-stat caches"}
    if report_path:
        Path(report_path).write_text(json.dumps(report, indent=2) + "\n")
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--observe")
    parser.add_argument("--baseline", type=Path, default=HERE / "baseline.py")
    parser.add_argument("--candidate", type=Path, default=HERE / "candidate.py")
    parser.add_argument("--payload", type=Path, default=HERE / "payload")
    parser.add_argument("--report", type=Path, default=HERE / "differential-results.json")
    args = parser.parse_args()
    if args.observe:
        return observe(json.loads(args.observe))
    def check(label, passed):
        print(("ok   " if passed else "FAIL ") + label, flush=True)
    report = run_git_entry_differentials(args.candidate, args.baseline, payload=args.payload, check=check, report_path=args.report)
    print("%d/%d scoped Git entry controls passed; %d actual entry runs in %.3fs" %
          (sum(row["pass"] for row in report["checks"]), len(report["checks"]), report["actual_entry_runs"], report["seconds"]))
    return int(not all(row["pass"] for row in report["checks"]))


if __name__ == "__main__":
    raise SystemExit(main())
