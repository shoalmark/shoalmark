"""FM-044 A caller continuation: differential VCS migration and honest SVN applicability.

Standalone controls; aggregate-suite wiring remains with P. The immutable accepted A
source is the comparison, while real process results establish behavior. No consumer
authority, protected acceptance or offline SVN history verification is claimed.
"""

import ast
from contextlib import redirect_stderr, redirect_stdout
import copy
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import time
from unittest.mock import patch

import test_vcs_shared as shared

HERE = Path(__file__).resolve().parent
BASE = "6fe35f5624ffba76490f11b15ed424973414b101"
# The board's settings this comparison sets aside before it holds a start's environment equal to the accepted source's: the hooks path and each emptied
# filter driver always, and the rest (`BOARD_KEYS`) where the read does not keep from fetching (`GIT_NO_LAZY_FETCH`). Set aside the same way on both sides,
# so every other difference in the environment still counts.
SETTING = re.compile(r"'(?:[^']|'\\'')*'")
EMPTIED = re.compile(r"'filter\..*\.(?:clean|smudge|process)='")
BOARD_KEYS = ("'log.showSignature=", "'core.fsmonitor=", "'gpg.program=", "'gpg.openpgp.program=", "'gpg.x509.program=")


def board_settings_undone(env):
    """`env` with the board's settings taken out: the hooks path and every emptied filter driver always, the others where the read does not keep from
    fetching (`GIT_NO_LAZY_FETCH`)."""
    if not isinstance(env, dict) or "GIT_CONFIG_PARAMETERS" not in env:
        return env
    kept = [s for s in SETTING.findall(env["GIT_CONFIG_PARAMETERS"]) if not s.startswith("'core.hooksPath=") and not EMPTIED.fullmatch(s)
            and (env.get("GIT_NO_LAZY_FETCH") == "1" or not s.startswith(BOARD_KEYS))]
    out = {key: value for key, value in env.items() if key != "GIT_CONFIG_PARAMETERS"}
    return dict(out, GIT_CONFIG_PARAMETERS=" ".join(kept)) if kept else out
OWNED = {"answer_refs", "built_on", "config_file_problem", "default_branch", "git_version", "head_commit",
         "install_copy", "install_hook", "last_worked_on", "on_their_way", "promisor_remotes", "recover_from_log",
         "repos_naming", "specs_unread", "svn_last_worked_on"}


def load(source):
    spec = importlib.util.spec_from_file_location("shared_caller_tool", source)
    fm = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(fm)
    return fm


def baseline_source(pin=BASE):
    folder = HERE / ".cache" / ("shared-callers-baseline" if pin == BASE else "shared-callers-baseline-" + pin[:8])
    import tarfile
    archive = subprocess.run(["git", "archive", pin], cwd=HERE, capture_output=True, check=True).stdout
    with tarfile.open(fileobj=io.BytesIO(archive)) as source:
        # Tracked repository files only; refuse absolute/parent paths on Python 3.9 too.
        members = source.getmembers()
        for member in members:
            parts = Path(member.name).parts
            if member.name.startswith("/") or ".." in parts or member.issym() or member.islnk():
                raise AssertionError("unsafe immutable source member")
        if not (folder / "shoalmark.py").exists():
            folder.mkdir(parents=True, exist_ok=True)
            source.extractall(folder)
        for member in members:
            if member.isfile():
                path = folder / member.name
                if path.is_symlink() or path.read_bytes() != source.extractfile(member).read():
                    raise AssertionError("cached comparison differs from accepted immutable source: " + member.name)
    return folder / "shoalmark.py"


def call(root, *argv):
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull, GIT_AUTHOR_NAME="fixture", GIT_AUTHOR_EMAIL="fixture@example.invalid",
               GIT_COMMITTER_NAME="fixture", GIT_COMMITTER_EMAIL="fixture@example.invalid", GIT_AUTHOR_DATE="2026-10-13T00:00:00+00:00", GIT_COMMITTER_DATE="2026-10-13T00:00:00+00:00")
    return subprocess.run(argv, cwd=root, env=env, capture_output=True, check=True, timeout=30).stdout


def source_controls(fm, old, check):
    before, after = Path(old.__file__).read_text(), Path(fm.__file__).read_text()
    a = {n.name: n for n in ast.parse(before).body if isinstance(n, ast.FunctionDef)}
    b = {n.name: n for n in ast.parse(after).body if isinstance(n, ast.FunctionDef)}
    check("A callers: exactly the fifteen allocated functions change", {n for n in a if ast.dump(a[n]) != ast.dump(b[n])} == OWNED and a.keys() == b.keys())
    count = 0
    for name in sorted(OWNED):
        raw = [n for n in ast.walk(a[name]) if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and
               isinstance(n.func.value, ast.Name) and n.func.value.id == "subprocess" and n.func.attr == "run"]
        migrated = [n for n in ast.walk(b[name]) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "vcs_process"]
        check(f"A callers: {name} migrates every owned raw start", len(raw) == len(migrated) and not any(isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and isinstance(n.func.value, ast.Name) and n.func.value.id == "subprocess" and n.func.attr == "run" for n in ast.walk(b[name])))
        for n, (prior, current) in enumerate(zip(raw, migrated)):
            expected = [ast.dump(x) for x in prior.args[0].elts]
            actual = [ast.dump(x) for x in current.args]
            keywords = {k.arg: ast.dump(k.value) for k in prior.keywords}
            current_keywords = {k.arg: ast.dump(k.value) for k in current.keywords}
            if "cwd" not in keywords:
                # The real inherited-cwd controls establish effective identity;
                # this supporting AST check only requires an explicit cwd.
                has_cwd = current_keywords.pop("cwd", None) is not None
            else:
                has_cwd = True
            check(f"A callers: {name} argv/keywords/effective cwd remain exact {n}", expected == actual and has_cwd and keywords == current_keywords)
            count += 1
    check("A callers: exactly sixteen Git/SVN starts migrate", count == 16)
    previous = json.loads((Path(old.__file__).parent / "test_vcs_launch_allowlist.json").read_text())
    current = json.loads((HERE / "test_vcs_launch_allowlist.json").read_text())
    removed = [key for key in previous if key.split("|")[0] in OWNED]
    check("A callers: exact owned removals60→44 without restoration/rekey", len(previous) == 60 and len(current) == 44 and len(removed) == 16 and current == [k for k in previous if k not in removed])
    for name in ("board_after_act", "run_deriver", "vcs_process", "configure", "main", "lint", "board_judge", "svn_local_status", "svn_local_directory", "svn_local_properties"):
        check(f"A callers: accepted {name} remains unchanged", ast.dump(a[name]) == ast.dump(b[name]))


def git_controls(fm, old, check):
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp).resolve(); call(root, "git", "init", "-q", "--initial-branch=main")
        folder = shared.corpus(root); tracker = folder / "WORK-001-local.md"
        original = tracker.read_text(); original = original.replace('hook: "local content"', 'hook: "local content"\nask: proceed\nask-kind: ruling\nask-since: 2026-10-13')
        tracker.write_text(original)
        call(root, "git", "add", "."); call(root, "git", "-c", "core.hooksPath=/dev/null", "-c", "commit.gpgsign=false", "commit", "-qm", "WORK-001 initial")
        trunk = call(root, "git", "rev-parse", "HEAD").decode().strip()
        tracker.write_text(original.replace("ask: proceed", "ask: proceed\nanswer: accepted - fixture choice"))
        call(root, "git", "add", "."); call(root, "git", "-c", "core.hooksPath=/dev/null", "-c", "commit.gpgsign=false", "commit", "-qm", "WORK-001 historical answer")
        answer = call(root, "git", "rev-parse", "HEAD").decode().strip()
        tracker.write_text(original)
        call(root, "git", "add", "."); call(root, "git", "-c", "core.hooksPath=/dev/null", "-c", "commit.gpgsign=false", "commit", "-qm", "WORK-001 local continuation")
        call(root, "git", "update-ref", "refs/remotes/origin/main", trunk)
        call(root, "git", "symbolic-ref", "refs/remotes/origin/HEAD", "refs/remotes/origin/main")
        call(root, "git", "update-ref", "refs/remotes/origin/answer/WORK-001", answer)
        module = root / "module"; module.mkdir(); call(module, "git", "init", "-q", "--initial-branch=main")
        (module / "work").write_text("work"); call(module, "git", "add", "."); call(module, "git", "-c", "core.hooksPath=/dev/null", "-c", "commit.gpgsign=false", "commit", "-qm", "WORK-001 submodule work")
        (root / ".gitmodules").write_text('[submodule "module"]\n path = module\n')
        process = subprocess.run
        def measured(tool, operation, prepare=None):
            tool.configure(root)
            if prepare:
                prepare(tool)
            records = []
            def run(argv, **kwargs):
                normalized = copy.deepcopy(kwargs); normalized["cwd"] = os.path.abspath(normalized.get("cwd") or ".")
                if "env" in normalized:
                    normalized["env"] = board_settings_undone(normalized["env"])
                # Each source's own unavailable signature program follows its real __file__.
                def normalize(value):
                    if isinstance(value, dict):
                        return {k: normalize(v) for k, v in value.items()}
                    if isinstance(value, (str, os.PathLike)):
                        return str(value).replace(tool.NO_SIGNATURE_PROGRAM, "<source-no-signature-program>")
                    return value
                normalized = normalize(normalized)
                records.append([list(map(str, argv)), normalized])
                return process(argv, **kwargs)
            with patch.object(subprocess, "run", side_effect=run):
                value = operation(tool)
            return value, records
        def pair(name, operation, prepare=None):
            a, ar = measured(old, operation, prepare); b, br = measured(fm, operation, prepare)
            check(f"A callers: real Git {name} result equals accepted source", a == b)
            check(f"A callers: real Git {name} process argv/options/environment equal accepted source", ar == br)
            return b
        for name in ("git_version", "built_on", "head_commit", "default_branch", "answer_refs", "promisor_remotes", "repos_naming", "config_file_problem"):
            pair(name, lambda tool, name=name: getattr(tool, name)())
        pair("last_worked_on", lambda tool: tool.last_worked_on(tracker))
        pair("on_their_way", lambda tool: tool.on_their_way([tool.extract(tracker, original)]))
        def relations(tool):
            need = {tracker.relative_to(root).as_posix(): {"asks_recovered_all": {("proceed", "accepted - fixture choice"): None}}}
            tool.recover_from_log(need)
            return need
        pair("recover_from_log", relations)
        def partial(tool):
            tool.lazy_fetch_off(); tool._PARTIAL = ["origin"]
        pair("specs_unread", lambda tool: tool.specs_unread([f"HEAD:{tracker.relative_to(root).as_posix()}", "HEAD:missing", "0" * 40 + ":lost"]), partial)
        call(root, "git", "config", "remote.origin.promisor", "true")
        check("A callers: real promisor config retains named partial remote", pair("promisor configured", lambda tool: tool.promisor_remotes()) == ["origin"])
        evil = root / "branch-owned.conf"; evil.write_text('[core]\n hooksPath = hooks-from-tree\n')
        call(root, "git", "config", "include.path", str(evil))
        refusal = pair("config include refusal", lambda tool: tool.config_file_problem())
        check("A callers: actual inside-tree config include refuses hook/copy installation", bool(refusal) and "inside the working tree" in refusal)
        call(root, "git", "config", "--unset", "include.path")
        for name, expected in (("git_version", None), ("built_on", ""), ("head_commit", ""), ("answer_refs", (None, "")),
                               ("default_branch", None), ("promisor_remotes", []), ("install_copy", (4, [f"--install-hook: {root} has no git directory to keep the hooks' copy in"]))):
            outcomes = []
            for tool in (old, fm):
                tool.configure(root)
                with patch.object(subprocess, "run", return_value=subprocess.CompletedProcess([], 1, "", "injected unavailable metadata")):
                    outcomes.append(getattr(tool, name)())
            check(f"A callers: failed Git {name} preserves deliberate result contract", outcomes == [expected, expected])
        outcomes = []
        for tool in (old, fm):
            tool.configure(root)
            with patch.object(subprocess, "run", return_value=subprocess.CompletedProcess([], 2, "", "injected unreadable configuration")):
                outcomes.append(tool.promisor_remotes())
        check("A callers: unreadable promisor configuration remains unknown rather than empty", outcomes == [None, None])
        outcomes = []
        for tool in (old, fm):
            tool.configure(root)
            with patch.object(subprocess, "run", side_effect=FileNotFoundError("Git is unavailable")):
                try:
                    tool.git_version(); outcomes.append("unexpected success")
                except OSError as error:
                    outcomes.append(type(error).__name__)
        check("A callers: missing Git launch preserves its existing OSError contract", outcomes == ["FileNotFoundError", "FileNotFoundError"])
        for tool in (old, fm):
            tool.configure(root); output, error = io.StringIO(), io.StringIO()
            with redirect_stdout(output), redirect_stderr(error):
                code = tool.install_hook()
            trusted = root / ".git" / tool.COPY_DIR
            check(f"A callers: real Git hook/copy install succeeds for {'accepted' if tool is old else 'migrated'} source", code == 0 and (trusted / "shoalmark.py").read_bytes() == Path(tool.__file__).read_bytes())
            check(f"A callers: real Git installed session/gate/message hooks retain templates for {'accepted' if tool is old else 'migrated'} source", all((root / ".git" / "hooks" / name).read_text().startswith("#!/bin/sh\n") for name in tool.HOOKS))
        # Rebinding makes applicable Git helpers read the new consumer, not stale ROOT.
        other = root / "other"; other.mkdir(); call(other, "git", "init", "-q", "--initial-branch=another")
        shared.corpus(other)                         # nearest configuration defines the consumer, including nested repositories
        fm.configure(other)
        check("A callers: actual rebind clears HEAD/default branch and reads new branch", fm.built_on() == "another" and fm.head_commit() == "" and fm.default_branch() is None)


def svn_probe(source, root, mode):
    """One child with Git absent; record actual starts and preserved server-log behavior."""
    events = []; active = [False]
    def audit(event, args):
        if active[0] and event == "subprocess.Popen":
            if args[0] is None and isinstance(args[1], str):        # Windows' audit shape (RV-3061): no program, one command line
                argv = split(args[1])                               # Windows starts its first word; the raw line is kept for exact checks
                events.append([argv[0] if argv else "", argv, str(args[2]), args[1]])
            else:
                events.append([str(args[0]), list(map(str, args[1])), str(args[2])])
    sys.addaudithook(audit)
    split = load(HERE / "shoalmark.py").split_cmdline               # the suite's reading of a Windows line (`_watch_git`); the baselines have none
    tool = load(source); tool.configure(root); tempfile.gettempdir()
    output, error = io.StringIO(), io.StringIO(); active[0] = True
    try:
        with redirect_stdout(output), redirect_stderr(error):
            if mode == "metadata":
                results = {"answer_refs": tool.answer_refs(), "git_version": tool.git_version(), "default_branch": tool.default_branch(),
                           "built_on": tool.built_on(), "head_commit": tool.head_commit(), "promisor_remotes": tool.promisor_remotes(),
                           "specs_unread": tool.specs_unread(["HEAD:missing"]), "on_their_way": tool.on_their_way([{"id": "WORK-001"}]),
                           "repos_naming": tool.repos_naming(), "config_file_problem": tool.config_file_problem(), "install_copy": tool.install_copy()[0]}
                need = {}; tool.recover_from_log(need); results["recover_from_log"] = need; code = 0
            elif mode == "history":
                results = {"first": tool.last_worked_on(tool.TRACKER_DIR / "WORK-001-local.md")}
                results["cached"] = tool.last_worked_on(tool.TRACKER_DIR / "WORK-001-local.md")
                results["starts_before_rebind"] = len(events)
                tool.configure(root)
                results["after_rebind"] = tool.last_worked_on(tool.TRACKER_DIR / "WORK-001-local.md"); code = 0
            elif mode == "install":
                results = {}; code = tool.install_hook()
            elif mode == "board":
                results = {}; code = tool.board_run(root)
            else:
                results = {}; code = tool.main(["--root", str(root), "--init"])
    except BaseException as e:
        code = e.code if isinstance(e, SystemExit) else -1; results = {"exception": type(e).__name__, "detail": str(e)}
    finally:
        active[0] = False
    print(json.dumps({"code": code, "results": results, "events": events, "out": output.getvalue(), "err": error.getvalue(), "git_absent": shutil.which("git") is None}))


def svn_controls(fm, old, check):
    if not (shutil.which("svn") and shutil.which("svnadmin")):
        print("SKIP A caller real SVN fixtures: svn/svnadmin required"); return
    with tempfile.TemporaryDirectory() as temp:
        base = Path(temp).resolve(); server = base / "server"; root = base / "wc"; init = base / "init"; search = base / "bin"
        call(base, "svnadmin", "create", str(server)); call(base, "svn", "checkout", "-q", server.as_uri(), str(root))
        shared.corpus(root); call(root, "svn", "add", "shoalmark.toml", "work-tracker"); call(root, "svn", "commit", "-qm", "local fixture")
        call(base, "svn", "checkout", "-q", server.as_uri(), str(init))
        module = root / "module"; module.mkdir(); call(module, "git", "init", "-q")
        (root / ".gitmodules").write_text('[submodule "module"]\n path = module\n')
        shared.svn_only(search)
        toolfile = root / "tools" / "shoalmark" / "shoalmark.py"; toolfile.parent.mkdir(parents=True); toolfile.write_bytes(Path(fm.__file__).read_bytes())
        server.rename(base / "server-unavailable")
        env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}; env.update(PATH=str(search), PYTHONDONTWRITEBYTECODE="1")
        observations = []
        def probe(mode, source=fm.__file__, target=root):
            done = subprocess.run([sys.executable, "-B", str(Path(__file__).resolve()), "--svn-probe", str(source), str(target), mode], env=env, capture_output=True, text=True, encoding="utf-8", timeout=30)
            if done.returncode:
                raise AssertionError(done.stderr)
            value = json.loads(done.stdout); observations.append({"mode": mode, "source": str(source), "result": value}); return value
        got = probe("metadata")
        check("A callers: real no-Git SVN metadata bypasses every Git-only helper without a process attempt", got["code"] == 0 and got["git_absent"] and not got["events"])
        check("A callers: SVN presentation/not-applicable results are explicit and carry no authority", got["results"] == {"answer_refs": [None, ""], "git_version": None, "default_branch": None, "built_on": "", "head_commit": "", "promisor_remotes": [], "specs_unread": [], "on_their_way": {}, "repos_naming": {}, "config_file_problem": "", "install_copy": 4, "recover_from_log": {}})
        prior = probe("metadata", old.__file__)
        check("A callers: immutable accepted caller baseline really attempts unavailable Git on ordinary SVN", prior["code"] == -1 and prior["git_absent"] and prior["results"].get("exception") == "FileNotFoundError" and prior["events"] and prior["events"][0][1][0] == "git")
        got = probe("board")
        from test_vcs_entry import same_start                       # an exact start: Windows' raw line against list2cmdline, POSIX's list
        exact = lambda e, argv: same_start(e[1], e[3] if len(e) > 3 else None, argv)
        check("A callers: real board remains server-free with no Git", got["code"] == 0 and got["git_absent"] and len(got["events"]) == 1 and exact(got["events"][0], shared.STATUS))
        got = probe("install")
        check("A callers: install selects real SVN properties before any Git attempt", got["code"] == 0 and got["git_absent"] and got["events"] and all(e[0] == "svn" for e in got["events"]))
        got = probe("init", target=init)
        check("A callers: real SVN init remains local with no Git and unavailable server", got["code"] == 0 and got["git_absent"] and all(e[0] == "svn" for e in got["events"]))
        a, b = probe("history", old.__file__), probe("history")
        check("A callers: unavailable-server SVN date preserves accepted placeholder/cache/rebind results", a["results"] == b["results"] == {"first": "—", "cached": "—", "starts_before_rebind": 1, "after_rebind": "—"})
        effective = lambda events: [[e[0], e[1], os.getcwd() if e[2] in ("None", ".") else e[2]] for e in events]
        check("A callers: date helper honestly retains one server log then one after rebind; no Git", effective(a["events"]) == effective(b["events"]) and len(b["events"]) == 2 and all(exact(e, ["svn", "log", "-v", "--xml", str(root / "work-tracker")]) for e in b["events"]))
        # Existing controlled local-metadata refusal remains before scaffold or property writes.
        (init / ".svn" / "wc.db").write_bytes(b"not a working copy database")
        got = probe("init", target=init)
        check("A callers: damaged local metadata retains controlled exit4", got["code"] == 4 and "nothing is written" in got["err"])
        folder = HERE / ".cache"; folder.mkdir(exist_ok=True)
        (folder / "shared-callers-svn-observations.json").write_text(json.dumps(observations, indent=2) + "\n")


def cwd_probe(source, root, launch, operation, deleted):
    """Real functions/processes; preserve unnamed cwd by inode, never os.getcwd()."""
    tool = load(source); tool.configure(root)
    split = load(HERE / "shoalmark.py").split_cmdline               # the suite's reading of a Windows line (`_watch_git`); 43b5600 has none
    starts, reads, writes = [], [], []; active = [False]
    original = os.getcwd(); os.chdir(launch)
    identity = tuple((getattr(os.stat("."), key)) for key in ("st_dev", "st_ino"))
    if deleted:
        launch.rmdir()
    def environment(env):
        values = board_settings_undone(dict(os.environ if env is None else env))
        return hashlib.sha256(json.dumps(values, sort_keys=True).encode()).hexdigest()
    def audit(event, args):
        if not active[0]:
            return
        if event == "subprocess.Popen":
            cwd = args[2] if args[2] is not None else "."
            stat = os.stat(cwd); inherited = (stat.st_dev, stat.st_ino) == identity
            frame = sys._getframe()
            while frame and not (frame.f_code.co_name == "run" and frame.f_globals.get("__name__") == "subprocess"):
                frame = frame.f_back
            options = dict(frame.f_locals["kwargs"]) if frame else {}
            options.pop("env", None); options.pop("cwd", None)
            windows = args[0] is None and isinstance(args[1], str)  # Windows' audit shape (RV-3061): the raw line kept, its argv read back
            starts.append({"argv": split(args[1]) if windows else list(map(str, args[1])), "cwd_raw": str(cwd),
                           "cwd": "<inherited launch cwd>" if inherited else str(cwd),
                           "inherited": inherited, "env_mode": "inherited" if args[3] is None else "explicit",
                           "environment_sha256": environment(args[3]), "options": options, **({"raw": args[1]} if windows else {})})
        elif event == "open":
            mode, flags = args[1:3]
            write = (isinstance(mode, str) and any(c in mode for c in "wax+")) or (isinstance(flags, int) and bool(flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND)))
            if write and isinstance(args[0], (str, bytes, os.PathLike)):
                writes.append(os.fsdecode(args[0]))
            elif isinstance(args[0], (str, bytes, os.PathLike)):
                reads.append(os.fsdecode(args[0]))
        elif event in ("os.mkdir", "os.remove", "os.rmdir", "os.rename", "os.chmod"):
            if isinstance(args[0], (str, bytes, os.PathLike)):
                writes.append(os.fsdecode(args[0]))
    sys.addaudithook(audit)
    out, err = io.StringIO(), io.StringIO(); active[0] = True; error = None
    try:
        with redirect_stdout(out), redirect_stderr(err):
            result = tool.svn_last_worked_on(root / "work-tracker" / "WORK-001-local.md") if operation == "svn_last_worked_on" else getattr(tool, operation)()
    except BaseException as exception:
        result = None; error = type(exception).__name__
    finally:
        active[0] = False; os.chdir(original)
    copied = root / ".git" / tool.COPY_DIR / "shoalmark.py"
    installed = error is None and (operation not in ("install_copy", "install_hook") or (copied.is_file() and copied.read_bytes() == source.read_bytes()))
    print(json.dumps({"result": result, "exception": error, "starts": starts, "reads": reads, "writes": writes,
                      "installed_source_exact": installed, "out": out.getvalue(), "err": err.getvalue(),
                      "removed_launch": deleted, "identity_preserved": all(not s["inherited"] or s["cwd"] == "<inherited launch cwd>" for s in starts)}))


# A pinned copy takes its commit from its PIN, so `install_copy`, and `install_hook` through it, no longer start `git rev-parse --short HEAD`: their
# expected starts are the baseline's without that one, counted here for that change, while the baseline itself stays as it is.
DROPPED_START = ["git", "rev-parse", "--short", "HEAD"]
STARTS_AFTER = {"install_copy": 6, "install_hook": 13}


def inherited_cwd_controls(fm, check, operations=("repos_naming", "install_copy", "install_hook", "svn_last_worked_on"), record=True):
    """RV-3096: actual immutable-before and fixed-after unrelated/deleted cwd."""
    before = baseline_source("43b560037a6d0297578dc5f7f9a7cf6caa02f0ef")
    if os.name == "nt":
        print("SKIP RV-3096 deleted launch cwd: Windows prevents deleting an in-use cwd; native qualification remains separate")
        return
    with tempfile.TemporaryDirectory() as temp:
        base = Path(temp).resolve(); root = base / "consumer"; root.mkdir()
        call(root, "git", "init", "-q", "--initial-branch=main"); shared.corpus(root)
        call(root, "git", "add", "."); call(root, "git", "-c", "core.hooksPath=/dev/null", "-c", "commit.gpgsign=false", "commit", "-qm", "WORK-001 local fixture")
        dep = root / "dep"; dep.mkdir(); call(dep, "git", "init", "-q")
        (dep / "file").write_text("local work\n"); call(dep, "git", "add", ".")
        call(dep, "git", "-c", "core.hooksPath=/dev/null", "-c", "commit.gpgsign=false", "commit", "-qm", "WORK-021 dep work")
        (root / ".gitmodules").write_text('[submodule "dep"]\n path = dep\n')
        target = root / "tools" / "shoalmark"; target.mkdir(parents=True)
        for name in fm.TOOL_FILES:
            if name != "shoalmark.py":
                path = target / name; path.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(HERE / name, path)
        tool = target / "shoalmark.py"; rows = []
        def probe(operation, chosen, deleted, consumer=root):
            tool.write_bytes(Path(chosen).read_bytes())
            (target / "PIN").write_text("".join(hashlib.sha256((target / rel).read_bytes().replace(b"\r\n", b"\n")).hexdigest() + "  " + rel + "\n" for rel in fm.TOOL_FILES))
            if consumer == root:
                copy_dir = root / ".git" / fm.COPY_DIR
                if copy_dir.exists():
                    shutil.rmtree(copy_dir)
                for hook in fm.HOOKS:
                    path = root / ".git" / "hooks" / hook
                    if path.exists():
                        path.unlink()
            launch = base / "unrelated"; launch.mkdir(exist_ok=True)
            env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
            env.update(PYTHONDONTWRITEBYTECODE="1", GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull)
            if operation == "svn_last_worked_on":
                env["PATH"] = str(search)
            done = subprocess.run([sys.executable, "-B", str(Path(__file__).resolve()), "--cwd-probe", str(tool), str(consumer), str(launch), operation, str(int(deleted))], env=env, capture_output=True, text=True, encoding="utf-8", timeout=30)
            if done.returncode:
                raise AssertionError(done.stderr)
            got = json.loads(done.stdout); got.update(operation=operation, source_pin="43b5600" if chosen == before else "fixed working source", root=str(consumer)); rows.append(got)
            return got
        def effective(got):
            return [{k: v for k, v in record.items() if k not in ("cwd_raw", "inherited")} for record in got["starts"]]
        for operation in operations:
            if operation == "svn_last_worked_on":
                server = base / "server"; wc = base / "wc"
                call(base, "svnadmin", "create", str(server)); call(base, "svn", "checkout", "-q", server.as_uri(), str(wc))
                shared.corpus(wc); call(wc, "svn", "add", "shoalmark.toml", "work-tracker"); call(wc, "svn", "commit", "-qm", "local history fixture")
                server.rename(base / "server-unavailable")
                search = base / "svn-only"; search.mkdir(); (search / "svn").symlink_to(shutil.which("svn"))
                consumer = wc
            else:
                consumer = root
            old_healthy = probe(operation, before, False, consumer)
            old_deleted = probe(operation, before, True, consumer)
            new_healthy = probe(operation, fm.__file__, False, consumer)
            new_deleted = probe(operation, fm.__file__, True, consumer)
            check("RV-3096: " + operation + " immutable43 really fails before launch after cwd deletion", old_deleted["exception"] == "FileNotFoundError" and not old_deleted["starts"] and not old_deleted["writes"])
            expected = {"WORK-021": ["dep"]} if operation == "repos_naming" else "—" if operation == "svn_last_worked_on" else 0
            result = lambda got: got["result"][0] if operation == "install_copy" and got["exception"] is None else got["result"]
            check("RV-3096: " + operation + " healthy and deleted cwd keep the real accepted result", all(g["exception"] is None and result(g) == expected for g in (old_healthy, new_healthy, new_deleted)))
            kept = [start for start in effective(old_healthy) if operation not in STARTS_AFTER or start["argv"] != DROPPED_START]
            check("RV-3096: " + operation + " keeps full argv/environment/options and effective cwd", kept == effective(new_healthy) == effective(new_deleted)
                  and len(kept) == STARTS_AFTER.get(operation, len(kept)) and new_deleted["starts"] and new_deleted["starts"][0]["cwd_raw"] == "." and new_deleted["starts"][0]["inherited"])
            check("RV-3096: " + operation + " mutations stay in the disposable consumer", all(all(path == str(consumer) or path.startswith(str(consumer) + os.sep) for path in g["writes"]) and g["installed_source_exact"] for g in (old_healthy, new_healthy, new_deleted)))
            permitted = (str(root), str(consumer), str(Path(os.__file__).parent))
            check("RV-3096: " + operation + " reads only fixture data and trusted Python runtime", all(all(any(path == prefix or path.startswith(prefix + os.sep) for prefix in permitted) for path in g["reads"]) for g in (old_healthy, new_healthy, new_deleted)))
            if operation in ("repos_naming", "svn_last_worked_on"):
                check("RV-3096: " + operation + " remains read-only", all(not g["writes"] for g in (old_healthy, new_healthy, new_deleted)))
        if record:
            (HERE / ".cache" / "shared-callers-cwd-observations.json").write_text(json.dumps(rows, indent=2) + "\n")


INHERITED_MUTANTS = (
    ("the short HEAD start back", '    if pin.exists():\n        manifest, _ = pin_manifest(',
     '    sha = (git_out("rev-parse", "--short", "HEAD") or "").strip() or "no commit yet"\n    if pin.exists():\n        manifest, _ = pin_manifest('),
    ("another git start in install_copy", '    branch = (git_out("branch", "--show-current") or "").strip()\n    default = default_branch()',
     '    git_out("rev-parse", "HEAD")\n    branch = (git_out("branch", "--show-current") or "").strip()\n    default = default_branch()'),
)


def inherited_cwd_mutants(fm, check):
    """Each mutant of `install_copy`'s git starts turns the exact comparison of the starts red, for `install_copy` and for `install_hook`."""
    if os.name == "nt":
        print("SKIP RV-3096 deleted launch cwd mutants: Windows prevents deleting an in-use cwd; native qualification remains separate")
        return
    source = Path(fm.__file__).read_text(encoding="utf-8")
    for name, old, new in INHERITED_MUTANTS:
        if source.count(old) != 1:
            check("RV-3096 mutant · " + name + " · its mutation site exists once", False)
            continue
        seen = {}
        with tempfile.TemporaryDirectory() as temp:
            mutant = Path(temp) / "shoalmark.py"
            mutant.write_text(source.replace(old, new, 1), encoding="utf-8")
            inherited_cwd_controls(load(mutant), lambda label, ok: seen.__setitem__(label, bool(ok)), operations=("install_copy", "install_hook"), record=False)
        rows = [seen.get("RV-3096: " + operation + " keeps full argv/environment/options and effective cwd") for operation in ("install_copy", "install_hook")]
        check("RV-3096 mutant · " + name + " · the starts row fails for install_copy and for install_hook", rows == [False, False])


def run_shared_caller_controls(fm, check, baseline=None):
    old = load(baseline or baseline_source())
    source_controls(fm, old, check)
    git_controls(fm, old, check)
    svn_controls(fm, old, check)
    inherited_cwd_controls(fm, check)
    inherited_cwd_mutants(fm, check)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--cwd-probe":
        cwd_probe(Path(sys.argv[2]), Path(sys.argv[3]), Path(sys.argv[4]), sys.argv[5], bool(int(sys.argv[6])))
    elif len(sys.argv) > 1 and sys.argv[1] == "--svn-probe":
        svn_probe(Path(sys.argv[2]), Path(sys.argv[3]), sys.argv[4])
    else:
        rows = []; started = time.monotonic()
        def check(name, result):
            rows.append({"name": name, "pass": bool(result)}); print(("ok   " if result else "FAIL ") + name, flush=True)
        run_shared_caller_controls(load(HERE / "shoalmark.py"), check)
        proof = {"base": BASE, "seconds": time.monotonic() - started, "checks": rows}
        (HERE / ".cache" / "shared-callers-controls-proof.json").write_text(json.dumps(proof, indent=2) + "\n")
        print(f"{sum(row['pass'] for row in rows)}/{len(rows)} caller controls passed in {proof['seconds']:.3f}s")
        raise SystemExit(not all(row["pass"] for row in rows))
