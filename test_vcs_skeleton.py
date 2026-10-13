"""FM-044 common-skeleton controls, also run by test_core.py. Expectations come from the signed Builder brief.

These are boundary/metadata controls, not full shared-command no-Git or required-platform qualification.
"""

import ast
import collections
from contextlib import redirect_stderr, redirect_stdout
import hashlib
import io
import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from unittest.mock import patch


HERE = Path(__file__).resolve().parent


def caught(call, error):
    try:
        call()
    except error as e:
        return str(e)
    return None


def run_boundary_controls(fm, check):
    """FM-044: preserve git_out's and svn_run's argv, cwd, environment, outputs and refusals through the first refactor."""
    print("\nFM-044: transparent Git/SVN process boundary")
    result = subprocess.CompletedProcess([], 0, "result\n", "")
    with patch.object(fm.subprocess, "run", return_value=result) as start:
        with patch.dict(os.environ, {"GIT_DIR": "wrong", "GIT_WORK_TREE": "wrong", "GIT_INDEX_FILE": "wrong", "GIT_PREFIX": "wrong",
                                     **{k: "1" for k in fm.PATHSPEC_VARIABLES}}):
            said = fm.git_out("-c", "key=value", "show", "a path:with spaces", cwd=Path("source HERE"))
        args, kw = start.call_args
        check("FM-044: Git keeps exact argv, explicit source cwd and text decoding", said == "result\n" and args == (["git", "-c", "key=value", "show", "a path:with spaces"],)
              and kw["cwd"] == Path("source HERE") and {k: kw[k] for k in ("capture_output", "text", "encoding", "errors")} ==
              {"capture_output": True, "text": True, "encoding": "utf-8", "errors": "replace"})
        check("FM-044: Git strips hook-local and pathspec environment", all(k not in kw["env"] for k in
              ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_PREFIX", *fm.PATHSPEC_VARIABLES)))
        fm.git_out("version")
        check("FM-044: Git default cwd stays configured ROOT", start.call_args.kwargs["cwd"] == fm.ROOT)
    with patch.object(fm.subprocess, "run", return_value=subprocess.CompletedProcess([], 0, "", "")):
        check("FM-044: empty Git success remains empty text", fm.git_out("show") == "")
    with patch.object(fm.subprocess, "run", return_value=subprocess.CompletedProcess([], 128, "ignored", "failure")):
        check("FM-044: Git nonzero remains None", fm.git_out("show") is None)
    with patch.object(fm.subprocess, "run", side_effect=FileNotFoundError("missing git")):
        check("FM-044: Git launch errors still propagate to their caller", caught(lambda: fm.git_out("show"), OSError) == "missing git")

    with patch.object(fm.subprocess, "run", return_value=subprocess.CompletedProcess([], 0, b"a\r\nb\rc\xff", b"")) as start:
        said = fm.svn_run("cat", "a path@7")
        check("FM-044: SVN keeps bytes, exact argv/cwd, inherited env and LF text", said == "a\nb\nc\ufffd" and start.call_args.args == (["svn", "cat", "a path@7"],)
              and start.call_args.kwargs == {"cwd": fm.ROOT, "capture_output": True})
    with patch.object(fm.subprocess, "run", return_value=subprocess.CompletedProcess([], 0, b'<info><entry revision="7"/></info>', b"")) as start:
        said = fm.svn_run("info", "a path@7", xml=True)
        check("FM-044: SVN appends XML flag and parses output", said.find("entry").get("revision") == "7"
              and start.call_args.args == (["svn", "info", "a path@7", "--xml"],))
    cases = ((0, b" \r\n", b"", (), False, None),
             (1, b"", b"svn: E160006: revision missing", ("E160006",), False, None),
             (1, b"", b"svn: E160006: missing\nsvn: E999999: unreadable", ("E160006",), False, "E999999"),
             (1, b"", b"", (), False, "svn exited 1"),
             (0, b"<broken>", b"", (), True, "XML that could not be read"))
    for code, out, err, answers, xml, expected in cases:
        with patch.object(fm.subprocess, "run", return_value=subprocess.CompletedProcess([], code, out, err)):
            if expected is None:
                ok = fm.svn_run("info", xml=xml, answers=answers) is None
            else:
                error = caught(lambda: fm.svn_run("info", xml=xml, answers=answers), fm.SvnUnreadable)
                ok = error is not None and expected in error
        check(f"FM-044: SVN empty/accepted-error/refusal contract ({code}, xml={xml}, expected={expected})", ok)
    with patch.object(fm.subprocess, "run", side_effect=FileNotFoundError("missing svn")):
        check("FM-044: missing SVN remains SvnUnreadable", "svn could not be run: missing svn" in
              (caught(lambda: fm.svn_run("info"), fm.SvnUnreadable) or ""))
    if hasattr(fm, "vcs_process"):                         # same wrapper controls can prove the immutable pre-refactor implementation
        with patch.object(fm.subprocess, "run", return_value=result) as start:
            check("FM-044: boundary returns the original CompletedProcess", fm.vcs_process("git", "version", cwd=fm.ROOT, capture_output=True) is result)
            start.reset_mock()
            check("FM-044: boundary rejects an unknown executable before starting", caught(lambda: fm.vcs_process("sh", "-c", "git version"), ValueError)
                  is not None and not start.called)

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp).resolve() / "git-source"; root.mkdir()
        subprocess.run(["git", "init", "-q", str(root)], check=True, capture_output=True, env=fm.nested_git_env())
        check("FM-044: real Git source cwd is independent of configured consumer", Path(fm.git_out("rev-parse", "--show-toplevel", cwd=root).strip()) == root)
        check("FM-044: real Git missing revision returns None", fm.git_out("rev-parse", "--verify", "missing-revision", cwd=root) is None)

    if not (shutil.which("svn") and shutil.which("svnadmin")):
        print("  SKIP FM-044: local SVN boundary fixture needs svn and svnadmin")
        return
    previous = fm.ROOT
    try:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp).resolve() / "server"; root = repo.parent / "wc"
            subprocess.run(["svnadmin", "create", str(repo)], check=True, capture_output=True)
            subprocess.run(["svn", "checkout", "-q", repo.as_uri(), str(root)], check=True, capture_output=True)
            (root / "a path.txt").write_bytes(b"a\r\nb\rc\n")
            subprocess.run(["svn", "add", "a path.txt"], cwd=root, check=True, capture_output=True)
            subprocess.run(["svn", "commit", "-q", "-m", "boundary fixture", "--username", "fixture-author"], cwd=root, check=True, capture_output=True)
            fm.configure(root)
            check("FM-044: real SVN cat preserves LF boundary", fm.svn_run("cat", "a path.txt") == "a\nb\nc\n")
            info = fm.svn_run("info", "a path.txt", xml=True)
            check("FM-044: real SVN XML retains server revision/author", info.find("entry/commit").get("revision") == "1"
                  and info.findtext("entry/commit/author") == "fixture-author")
            check("FM-044: real SVN unreadable revision refuses", caught(lambda: fm.svn_run("cat", "a path.txt@999"), fm.SvnUnreadable) is not None)
    finally:
        fm.configure(previous)


# FM-044's production scanner covers Python process APIs in shoalmark.py only. It deliberately includes non-VCS/dynamic starts: an opaque argv can name
# Git or SVN. Emitted hook shell, release scripts, fixtures and documentation tooling are outside this scanner, under their existing separate controls.
PROCESS_APIS = {
    "subprocess": {"run", "Popen", "call", "check_call", "check_output", "getoutput", "getstatusoutput"},
    "os": {"system", "popen", "startfile", "fork", "forkpty", "posix_spawn", "posix_spawnp",
           *("exec" + n for n in ("v", "ve", "vp", "vpe", "l", "le", "lp", "lpe")),
           *("spawn" + n for n in ("v", "ve", "vp", "vpe", "l", "le", "lp", "lpe"))},
    "asyncio": {"create_subprocess_exec", "create_subprocess_shell"},
    "asyncio.subprocess": {"create_subprocess_exec", "create_subprocess_shell"},
    "pty": {"spawn"}, "webbrowser": {"open", "open_new", "open_new_tab", "get"},
    "_winapi": {"CreateProcess"}, "_posixsubprocess": {"fork_exec"}, "multiprocessing": {"Process", "Pool"},
}
PROCESS_METHODS = set().union(*PROCESS_APIS.values()) - {"get", "open"}     # ordinary mapping/file methods; webbrowser's resolved APIs are still checked
LAUNCH_CEILING_SHA256 = "1eabbea359cde1c65db4a688c3ff609d6acda0a33e38bc0b84021f9fde9bf6a0"
BOUNDARY_SHA256 = "e2cd4c40729a6bbdc95ac0f9037600df5002b3e5fdee0e7774277d2fa57f732f"
ALLOWLIST_PATH = "test_vcs_launch_allowlist.json"
CEILING_PATH = "test_vcs_launch_ceiling.json"


def normalized(node):
    """AST identity without source positions or version-added empty type_params (Python 3.9 and later)."""
    if isinstance(node, ast.AST):
        return [type(node).__name__, [[name, normalized(value)] for name, value in ast.iter_fields(node)
                                      if name != "type_params" or value]]
    if isinstance(node, list):
        return [normalized(value) for value in node]
    return node


def ast_hash(node):
    return hashlib.sha256(json.dumps(normalized(node), ensure_ascii=True, separators=(",", ":")).encode()).hexdigest()


def launch_sites(source):
    """Stable function/API/normalized-call keys; aliases/opaque module access and dynamic boundary selectors are refusals, never an exemption."""
    tree = ast.parse(source)
    parents = {c: n for n in ast.walk(tree) for c in ast.iter_child_nodes(n)}
    modules, imported = {}, {}
    for n in ast.walk(tree):
        if isinstance(n, ast.Import):
            for alias in n.names:
                if any(alias.name == m or alias.name.startswith(m + ".") for m in PROCESS_APIS) or alias.name in {"importlib", "builtins", "sys"}:
                    modules[alias.asname or alias.name.split(".")[0]] = alias.name if alias.asname else alias.name.split(".")[0]
        elif isinstance(n, ast.ImportFrom) and n.module in set(PROCESS_APIS) | {"importlib", "builtins", "sys"}:
            for alias in n.names:
                if alias.name == "*":
                    imported["*"] = n.module
                else:
                    imported[alias.asname or alias.name] = n.module + "." + alias.name

    def path_of(n):
        if isinstance(n, ast.Name):
            return imported.get(n.id, modules.get(n.id, ""))
        if isinstance(n, ast.Attribute):
            base = path_of(n.value)
            return base + "." + n.attr if base else ""
        return ""

    def function(n):
        names = []
        while n in parents:
            n = parents[n]
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
                names.append(n.name)
        return ".".join(reversed(names)) or "<module>"

    def operation(call):
        argv = call.args[0] if call.args else None
        if not isinstance(argv, ast.List) or not argv.elts or not isinstance(argv.elts[0], ast.Constant):
            return "<dynamic>"
        words = argv.elts; program = str(words[0].value); i = 1
        while i < len(words):
            word = words[i]
            if isinstance(word, ast.Constant) and word.value in ("-c", "-C"):
                i += 2
            elif isinstance(word, ast.Constant) and isinstance(word.value, str) and word.value.startswith("--git-dir="):
                i += 1
            elif isinstance(word, ast.JoinedStr) and word.values and isinstance(word.values[0], ast.Constant) and str(word.values[0].value).startswith("--git-dir="):
                i += 1
            else:
                break
        command = str(words[i].value) if i < len(words) and isinstance(words[i], ast.Constant) else "<forwarded>"
        return program + "/" + command

    sites, problems = [], []
    boundaries = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "vcs_process"]
    if len(boundaries) != 1 or ast_hash(boundaries[0]) != BOUNDARY_SHA256:
        problems.append("the reviewed vcs_process boundary changed or is missing/duplicated")
    if "*" in imported:
        problems.append("a process module was imported by wildcard")
    for n in ast.walk(tree):
        p = parents.get(n); canonical = path_of(n)
        module, _, api = canonical.rpartition(".")
        if module in PROCESS_APIS and api in PROCESS_APIS[module]:
            if isinstance(p, ast.Call) and p.func is n:
                if function(p) == "vcs_process":
                    continue                            # the entire boundary's AST is frozen above, not its name alone
                fn = function(p); op = operation(p); key = fn + "|" + op + "|" + canonical + "|" + ast_hash(p)
                sites.append({"key": key, "function": fn, "operation": op, "call": ast.unparse(p)})
            else:
                problems.append(function(n) + ": aliased process API " + canonical)
        if isinstance(n, (ast.Name, ast.Attribute)) and ((module == "subprocess" and api not in PROCESS_APIS[module] | {"TimeoutExpired", "CompletedProcess", "list2cmdline"})
                                                        or (module in PROCESS_APIS and api.startswith("__")) or canonical in {"sys.modules", "sys.__dict__"}):
            problems.append(function(n) + ": opaque process-module attribute " + canonical)
        if isinstance(n, ast.Attribute) and not canonical and n.attr in PROCESS_METHODS:
            problems.append(function(n) + ": dynamic process-method reference " + n.attr)
        if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load) and n.id in modules:
            if isinstance(p, ast.Attribute) and p.value is n:
                continue
            if (isinstance(p, ast.Call) and isinstance(p.func, ast.Name) and p.func.id == "getattr" and p.args and p.args[0] is n
                    and len(p.args) >= 2 and isinstance(p.args[1], ast.Constant) and isinstance(p.args[1].value, str)
                    and not p.args[1].value.startswith("__") and p.args[1].value not in PROCESS_APIS.get(modules[n.id], set())):
                continue                                # existing fixed os flags, never a process API or a dynamic attribute
            problems.append(function(n) + ": opaque/aliased process module " + modules[n.id])
        if (isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load) and n.id in {"__import__", "__builtins__", "eval", "exec", "compile", "globals", "locals"}
                or canonical in {"importlib.import_module", "builtins.__import__", "builtins.eval", "builtins.exec", "builtins.compile"}):
            problems.append(function(n) + ": dynamic import/evaluation escape")
        if (isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "getattr" and len(n.args) >= 2
                and (not isinstance(n.args[1], ast.Constant) or n.args[1].value in PROCESS_METHODS)):
            problems.append(function(n) + ": dynamic process-attribute lookup")
        if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load) and n.id == "vcs_process":
            if not (isinstance(p, ast.Call) and p.func is n and p.args and isinstance(p.args[0], ast.Constant) and p.args[0].value in ("git", "svn")):
                problems.append(function(n) + ": aliased/dynamic VCS boundary request")
    return sorted(sites, key=lambda s: s["key"]), sorted(set(problems))


def ratchet_problems(source, allowed, ceiling, previous=()):
    sites, problems = launch_sites(source)
    actual, permitted, maximum = (collections.Counter(keys) for keys in ([s["key"] for s in sites], allowed, ceiling))
    if permitted - maximum:
        problems.append("the transitional launch allowlist grew beyond its reviewed ceiling")
    for old in previous:
        if permitted - collections.Counter(old):
            problems.append("the transitional launch allowlist grew since an earlier revision")
    if actual - permitted:
        problems.append("production starts outside the boundary/allowlist: " + ", ".join(sorted((actual - permitted).keys())))
    if permitted - actual:
        problems.append("the transitional launch allowlist holds removed/renamed starts; shrink it")
    return problems


def previous_allowlists(fm):
    """The current committed list and every parent of its last change: resurrection fails before commit and after later records-only commits."""
    def git(*args):
        r = subprocess.run(["git", *args], cwd=HERE, capture_output=True, text=True, encoding="utf-8", errors="replace", env=fm.nested_git_env())
        return r.stdout.strip() if r.returncode == 0 else ""

    previous = []
    current = git("show", "HEAD:" + ALLOWLIST_PATH)
    if current:
        previous.append(json.loads(current))
    changed = git("log", "-1", "--format=%H", "--", ALLOWLIST_PATH)
    if changed:
        for parent in git("rev-list", "--parents", "-n", "1", changed).split()[1:]:
            old = git("show", parent + ":" + ALLOWLIST_PATH)
            if old:
                previous.append(json.loads(old))
    return previous


def run_ratchet_controls(fm, check):
    """FM-044: reject added, renamed, aliased and dynamic production starts and an expanded allowlist; admitted migration only shrinks."""
    print("\nFM-044: production Python launch ratchet")
    ceiling_bytes = (HERE / CEILING_PATH).read_bytes(); ceiling_rows = json.loads(ceiling_bytes)
    ceiling = [s["key"] for s in ceiling_rows]; allowed = json.loads((HERE / ALLOWLIST_PATH).read_text(encoding="utf-8"))
    source = Path(fm.__file__).read_text(encoding="utf-8")
    check("FM-044: immutable reviewed launch ceiling is unchanged", hashlib.sha256(ceiling_bytes).hexdigest() == LAUNCH_CEILING_SHA256)
    problems = ratchet_problems(source, allowed, ceiling, previous_allowlists(fm))
    check("FM-044: all production launch references are the boundary or retained starts: " + repr(problems), not problems)
    injections = {
        "literal Git": 'def escaped():\n    return subprocess.run(["git", "gc"])\n',
        "literal SVN": 'def escaped():\n    return subprocess.run(["svn", "update"])\n',
        "dynamic argv": 'def escaped(argv):\n    return subprocess.run(argv)\n',
        "assigned API alias": 'def escaped():\n    start = subprocess.run\n    return start(["git", "gc"])\n',
        "imported API alias": 'from subprocess import run as start\ndef escaped():\n    return start(["svn", "update"])\n',
        "imported module alias": 'import subprocess as launch\ndef escaped():\n    return launch.run(["git", "gc"])\n',
        "fixed getattr": 'def escaped():\n    return getattr(subprocess, "run")(["git", "gc"])\n',
        "dynamic getattr": 'def escaped(name):\n    return getattr(subprocess, name)(["svn", "update"])\n',
        "module dictionary": 'def escaped():\n    return subprocess.__dict__["run"](["git", "gc"])\n',
        "imported dictionary alias": 'from subprocess import __dict__ as apis\ndef escaped():\n    return apis["run"](["git", "gc"])\n',
        "module registry": 'def escaped():\n    return sys.modules["subprocess"].run(["git", "gc"])\n',
        "dynamic method": 'def escaped(module):\n    return module.run(["svn", "update"])\n',
        "OS shell": 'def escaped():\n    return os.system("git gc")\n',
        "asyncio": 'import asyncio\ndef escaped():\n    return asyncio.create_subprocess_exec("svn", "update")\n',
        "dynamic import": 'def escaped():\n    return __import__("subprocess").run(["git", "gc"])\n',
        "imported import alias": 'from importlib import import_module as load\ndef escaped():\n    return load("subprocess").run(["git", "gc"])\n',
        "imported builtin alias": 'from builtins import __import__ as load\ndef escaped():\n    return load("subprocess").run(["git", "gc"])\n',
        "boundary alias": 'def escaped():\n    start = vcs_process\n    return start("git", "gc")\n',
        "dynamic boundary selector": 'def escaped(program):\n    return vcs_process(program, "gc")\n',
    }
    for name, extra in injections.items():
        check("FM-044: ratchet rejects " + name, bool(ratchet_problems(source + "\n" + extra, allowed, ceiling)))
    renamed = source.replace("def tracked_board_rels(", "def renamed_board_rels(")
    check("FM-044: renaming a retained caller grants no exemption", bool(ratchet_problems(renamed, allowed, ceiling)))
    modified = source.replace('if program not in ("git", "svn"):', 'if program not in ("git", "svn", "sh"):')
    check("FM-044: changing the boundary cannot hide extra programs", bool(ratchet_problems(modified, allowed, ceiling)))
    extra_sites, _ = launch_sites(source + "\n" + injections["literal Git"])
    enlarged = [s["key"] for s in extra_sites]
    check("FM-044: allowlisting an injected start still fails", bool(ratchet_problems(source + "\n" + injections["literal Git"], enlarged, ceiling)))
    check("FM-044: a removed entry cannot be restored from the ceiling", bool(ratchet_problems(source, allowed, ceiling, [allowed[1:]])))
    # Synthetic migration control uses the same frozen boundary and one caller; no injected caller is added to the real allowlist.
    boundary = next(n for n in ast.parse(source).body if isinstance(n, ast.FunctionDef) and n.name == "vcs_process")
    small = 'import subprocess, os, sys\n' + ast.unparse(boundary) + '\ndef retained():\n    return subprocess.run(["git", "version"])\n'
    small_sites, small_problems = launch_sites(small); small_keys = [s["key"] for s in small_sites]
    moved = 'import subprocess, os, sys\n' + ast.unparse(boundary) + '\ndef retained():\n    return vcs_process("git", "version")\n'
    check("FM-044: migration succeeds by shrinking its list", not small_problems and not ratchet_problems(small, small_keys, small_keys)
          and not ratchet_problems(moved, [], small_keys, [small_keys]))


def refusal(call, fm):
    err = io.StringIO()
    with redirect_stderr(err):
        code = caught(call, SystemExit)
    return code == str(fm.EXIT_LINT) and len(err.getvalue().splitlines()) == 1


def run_dispatch_controls(fm, check):
    """FM-044: one configured root choice, no-Git metadata, retained linked-worktree/admin exclusions and fail-closed metadata."""
    print("\nFM-044: configured backend and administrative metadata")
    previous = fm.ROOT
    real_run = subprocess.run

    def git(root, *args):
        return real_run(["git", "-C", str(root), "-c", "commit.gpgsign=false", "-c", "core.hooksPath=" + os.devnull, *args],
                        capture_output=True, check=True, env={**fm.nested_git_env(), "GIT_AUTHOR_NAME": "Fixture", "GIT_AUTHOR_EMAIL": "fixture@example.invalid",
                                                             "GIT_COMMITTER_NAME": "Fixture", "GIT_COMMITTER_EMAIL": "fixture@example.invalid"})

    try:
        with tempfile.TemporaryDirectory() as tmp:
            area = Path(tmp).resolve(); root = area / "git"; root.mkdir()
            git(root, "init", "-q"); (root / "file").write_text("fixture\n", encoding="utf-8")
            git(root, "add", "file"); git(root, "commit", "-qm", "fixture")
            linked = area / "linked"; git(root, "worktree", "add", "-q", "--detach", str(linked))
            fm.configure(linked)
            dirs = fm.git_dirs(); own = Path(git(linked, "rev-parse", "--absolute-git-dir").stdout.decode().strip())
            check("FM-044: linked Git worktree protects its marker, own and common directories", all(fm.in_git_dir_on_disk(p) for p in
                  (linked / ".git", own / "config.worktree", root / ".git" / "hooks" / "copy.py")) and fm._norm(own) in dirs)
            sub = linked / "sub"; sub.mkdir(); (sub / "shoalmark.toml").write_text('name = "explicit subroot"\n', encoding="utf-8")
            with patch.object(fm, "select_vcs", wraps=fm.select_vcs) as select:
                fm.configure(sub)
                check("FM-044: explicit configured subroot retains its ancestor Git worktree", fm.ROOT == sub and fm.vcs() == "git" and fm._VCS[1] == linked)
                for _ in range(5):
                    fm.vcs()
                check("FM-044: repeated vcs reads do not rediscover markers", select.call_count == 1)
            check("FM-044: Git metadata is cached after one successful read", fm.git_dirs() is fm.git_dirs())
            nested = sub / "nested" / ".svn"; nested.mkdir(parents=True)
            check("FM-044: on-disk nested SVN metadata is excluded on Git", fm.in_git_dir_on_disk(nested / "entries"))
            if os.name != "nt":
                alias = sub / "alias"; alias.symlink_to(root / ".git", target_is_directory=True)
                check("FM-044: a symlink alias of Git common metadata is excluded", fm.in_git_dir_on_disk(alias / "hooks" / "copy.py"))
            for result in (subprocess.CompletedProcess([], 128, "", "failed"), subprocess.CompletedProcess([], 0, "", ""),
                           subprocess.CompletedProcess([], 0, str(own) + "\n", "")):
                fm.configure(sub)
                with patch.object(fm.subprocess, "run", return_value=result):
                    check("FM-044: failed/empty/incomplete Git metadata refuses", refusal(fm.git_dirs, fm) and fm._GIT_DIRS is None)
            fm.configure(sub)
            with patch.object(fm.subprocess, "run", side_effect=FileNotFoundError("missing Git")):
                check("FM-044: absent Git for a Git working copy is a controlled metadata refusal", refusal(fm.git_dirs, fm))

            if not (shutil.which("svn") and shutil.which("svnadmin")):
                print("  SKIP FM-044: SVN metadata controls need svn and svnadmin")
                return
            server = area / "server"; wc = area / "svn"
            real_run(["svnadmin", "create", str(server)], capture_output=True, check=True)
            real_run(["svn", "checkout", "-q", server.as_uri(), str(wc)], capture_output=True, check=True)
            child = wc / "sub"; child.mkdir(); (child / "shoalmark.toml").write_text('name = "SVN explicit subroot"\n', encoding="utf-8")
            real_run(["svn", "add", "sub"], cwd=wc, capture_output=True, check=True)
            real_run(["svn", "commit", "-q", "-m", "SVN subroot fixture", "--username", "fixture-author"], cwd=wc, capture_output=True, check=True)
            fm._GIT_DIRS = ["stale Git metadata"]; fm._LINE_AUTHOR["stale"] = "old-root"
            fm.configure(child)
            check("FM-044: reconfigure clears dispatch/metadata/line-author caches", fm.vcs() == "svn" and fm._VCS[1] == wc
                  and fm._GIT_DIRS is None and not fm._LINE_AUTHOR)
            binary = area / "bin"; binary.mkdir()
            if os.name != "nt":
                (binary / "svn").symlink_to(shutil.which("svn"))
            starts = []

            def monitor(argv, **options):
                starts.append(argv)
                if Path(str(argv[0])).name.lower() in ("git", "git.exe"):
                    raise AssertionError("SVN metadata attempted Git")
                return real_run(argv, **options)

            with patch.dict(os.environ, {"PATH": str(binary)}), patch.object(fm.subprocess, "run", side_effect=monitor):
                check("FM-044: Git is genuinely absent from the fixture executable search path", shutil.which("git") is None)
                if os.name != "nt":
                    check("FM-044: SVN remains executable while Git is absent", fm.svn_run("info", xml=True).tag == "info")
                starts.clear()
                for selected in (wc, child):
                    fm.configure(selected)
                    dirs = fm.git_dirs()
                    check("FM-044: no-Git metadata handles explicit root and SVN subdirectory", fm.vcs() == "svn" and fm._norm(wc / ".svn") in dirs
                          and fm.write_problem(fm.ROOT / "ordinary.md") == "")
                    check("FM-044: SVN administrative tracker/write paths refuse", fm.in_git_dir_on_disk(wc / ".svn" / "wc.db")
                          and (fm.ROOT != wc or "administrative directory" in fm.write_problem(wc / ".svn" / "wc.db")))
                    with redirect_stdout(io.StringIO()):
                        code = fm.main(["--root", str(selected), "--schema"])
                    check("FM-044: actual --root metadata dispatch works with Git absent", code == fm.EXIT_OK and fm.ROOT == selected and fm.vcs() == "svn")
                check("FM-044: SVN metadata starts no process", not starts)
                before = len(starts)
                check("FM-044: Git target request refuses before launch", refusal(lambda: fm.git_out("status"), fm) and len(starts) == before)
                check("FM-044: arbitrary cwd cannot bypass SVN target refusal", refusal(lambda: fm.git_out("rev-parse", "HEAD", cwd=root), fm)
                      and len(starts) == before)
            fm.configure(wc)
            old_tracker = fm.TRACKER_DIR
            try:
                fm.TRACKER_DIR = wc / ".svn" / "trackers"
                check("FM-044: administrative tracker directory is refused before reads/writes", "Subversion administrative directory" in fm.tracker_folder_problem())
            finally:
                fm.TRACKER_DIR = old_tracker
            if os.name != "nt":
                alias = wc / "admin-alias"; alias.symlink_to(wc / ".svn", target_is_directory=True)
                check("FM-044: symlink alias of SVN administrative metadata is excluded", fm.in_git_dir_on_disk(alias / "wc.db"))
                renamed = wc / ".SVN"
                if renamed.exists():
                    check("FM-044: filesystem case alias of SVN metadata is excluded", fm.in_git_dir_on_disk(renamed / "wc.db"))
            for error in (PermissionError("metadata denied"), FileNotFoundError("metadata missing")):
                fm.configure(wc)
                with patch.object(fm.os, "scandir", side_effect=error):
                    check("FM-044: missing/unreadable SVN metadata refuses without cached success", refusal(fm.git_dirs, fm) and fm._GIT_DIRS is None)
            fm.configure(wc)
            real_open = open

            def deny_metadata(path, *args, **kwargs):
                if Path(path).name == "wc.db":
                    raise PermissionError("working-copy record denied")
                return real_open(path, *args, **kwargs)

            with patch("builtins.open", side_effect=deny_metadata):
                check("FM-044: unreadable working-copy records refuse", refusal(fm.git_dirs, fm) and fm._GIT_DIRS is None)
            broken = area / "broken"; admin = broken / ".svn"; admin.mkdir(parents=True)
            for state in ("missing", "empty", "directory"):
                record = admin / "wc.db"
                if state == "empty":
                    record.write_bytes(b"")
                elif state == "directory":
                    record.unlink(); record.mkdir()
                fm.configure(broken)
                with patch.object(fm.subprocess, "run") as start:
                    check("FM-044: " + state + " working-copy records refuse without processes", refusal(fm.git_dirs, fm) and fm._GIT_DIRS is None and not start.called)
            if os.name != "nt":
                record.rmdir(); record.symlink_to(wc / ".svn" / "wc.db")
                fm.configure(broken)
                check("FM-044: a symlinked working-copy record refuses", refusal(fm.git_dirs, fm) and fm._GIT_DIRS is None)
            fm.configure(wc)
            with patch.object(fm.subprocess, "run", return_value=subprocess.CompletedProcess([], 0, "source-result", "")) as start:
                check("FM-044: fixed source Git provenance remains distinct from SVN target", fm.git_out("rev-parse", "HEAD", cwd=fm.HERE, source=True) == "source-result"
                      and start.call_args.args == (["git", "rev-parse", "HEAD"],) and start.call_args.kwargs["cwd"] == fm.HERE)
                start.reset_mock()
                check("FM-044: source flag cannot bypass its fixed cwd/operation limits", refusal(lambda: fm.git_out("rev-parse", "HEAD", cwd=root, source=True), fm)
                      and refusal(lambda: fm.git_out("fetch", cwd=fm.HERE, source=True), fm) and not start.called)
            expected_source = real_run(["git", "rev-parse", "HEAD"], cwd=fm.HERE, capture_output=True, check=True, env=fm.nested_git_env()).stdout.decode().strip()
            check("FM-044: actual Git source provenance remains usable with an SVN consumer", fm.source_provenance()[1] == expected_source)
            fm._GIT_DIRS = ["old root"]
            with patch.object(fm.os, "lstat", side_effect=PermissionError("marker denied")):
                check("FM-044: unreadable marker cannot select empty success or retain old dispatch", refusal(lambda: fm.configure(wc), fm)
                      and fm._VCS == ("", None) and fm._GIT_DIRS is None)
            fm.configure(wc)
            (wc / ".git").mkdir()
            check("FM-044: disk marker changes do not switch an already configured backend", fm.vcs() == "svn")
            fm.configure(wc)
            check("FM-044: reconfigure retains Git priority for two same-folder markers", fm.vcs() == "git")
    finally:
        fm.configure(previous)
