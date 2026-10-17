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
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from types import SimpleNamespace
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
BOUNDARY_SHA256 = "b1a5334b2d5e3d34028f287dd897b1795ed4c9ecf61231fd68af3c9d7925cb05"
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
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
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
    boundary_nodes = set(ast.walk(boundaries[0])) if len(boundaries) == 1 and ast_hash(boundaries[0]) == BOUNDARY_SHA256 else set()
    if "*" in imported:
        problems.append("a process module was imported by wildcard")
    for n in ast.walk(tree):
        p = parents.get(n); canonical = path_of(n)
        module, _, api = canonical.rpartition(".")
        if module in PROCESS_APIS and api in PROCESS_APIS[module]:
            if isinstance(p, ast.Call) and p.func is n:
                if p in boundary_nodes:
                    continue                            # only this validated top-level AST node's descendants are exempt
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


class RatchetHistoryError(ValueError):
    """Required source history is unavailable/invalid, or contains an expanded parent transition."""


def previous_allowlists(fm):
    """Verify every reachable child/parent multiset transition; absent pre-introduction paths are not failed reads.

    One unfiltered commit walk and checked tree/blob batches keep records-only history practical. The root-level
    allowlist is looked up in actual tree objects; no path-history simplification can hide a merge or a retired key.
    """
    env = fm.nested_git_env()
    env["GIT_NO_LAZY_FETCH"] = "1"                    # a missing local proof is not an invitation to fetch it

    def fail(label):
        raise RatchetHistoryError("launch history: " + label)

    def git(*args, data=None):
        try:
            r = subprocess.run(["git", "--no-replace-objects", *args], cwd=HERE, capture_output=True, input=data, env=env)
        except OSError:
            fail("Git could not start for " + args[0])
        if r.returncode:
            fail(args[0] + " could not read required proof")
        return r.stdout

    def oid(value):
        return re.fullmatch(r"(?:[0-9a-f]{40}|[0-9a-f]{64})", value) is not None

    def text(data):
        try:
            return data.decode("utf-8")
        except UnicodeError:
            fail("invalid UTF-8 metadata")

    def batch(objects, kind):
        objects = sorted(set(objects))
        if not objects:
            return {}
        raw = git("cat-file", "--batch", data=("\n".join(objects) + "\n").encode("ascii"))
        values, at = {}, 0
        for wanted in objects:
            end = raw.find(b"\n", at)
            if end < 0:
                fail("truncated " + kind + " batch header")
            header = text(raw[at:end]).split()
            if len(header) != 3 or header[:2] != [wanted, kind] or not header[2].isdigit():
                fail("unavailable or invalid " + kind + " object")
            size = int(header[2]); at = end + 1
            value = raw[at:at + size]; at += size
            if len(value) != size or raw[at:at + 1] != b"\n":
                fail("truncated " + kind + " object")
            at += 1
            digest = hashlib.sha1 if len(wanted) == 40 else hashlib.sha256
            if digest(kind.encode("ascii") + b" " + str(size).encode("ascii") + b"\0" + value).hexdigest() != wanted:
                fail("invalid " + kind + " object hash")
            values[wanted] = value
        if at != len(raw):
            fail("extra " + kind + " batch data")
        return values

    head = text(git("rev-parse", "--verify", "HEAD^{commit}")).strip()
    if not oid(head):
        fail("invalid HEAD revision")
    if git("rev-parse", "--is-shallow-repository").strip() != b"false":
        fail("source history is shallow or cannot establish its roots")
    graph = {}
    for row in text(git("log", "--reverse", "--topo-order", "--format=%H %P %T", head)).splitlines():
        fields = row.split()
        if len(fields) < 2 or not all(oid(value) and len(value) == len(head) for value in fields):
            fail("invalid commit/parent/tree revisions")
        commit, parents, tree = fields[0], fields[1:-1], fields[-1]
        if commit in graph or any(parent not in graph for parent in parents):
            fail("duplicate commit or unavailable/out-of-order parent")
        graph[commit] = (parents, tree)
    if head not in graph or next(reversed(graph), None) != head:
        fail("required reachable commit graph is incomplete")

    commits = batch(graph, "commit")
    for commit, raw in commits.items():
        headers = raw.split(b"\n\n", 1)[0].splitlines()
        actual_tree = headers[0][5:] if headers and headers[0].startswith(b"tree ") else b""
        actual_parents = [row[7:] for row in headers if row.startswith(b"parent ")]
        parents, tree = graph[commit]
        if actual_tree != tree.encode("ascii") or actual_parents != [parent.encode("ascii") for parent in parents]:
            fail("commit object disagrees with required tree/parent graph")

    trees = batch((tree for _, tree in graph.values()), "tree")
    tree_lists = {}
    width = len(head) // 2
    for tree, raw in trees.items():
        at, found, names = 0, None, set()
        while at < len(raw):
            space, nul = raw.find(b" ", at), raw.find(b"\0", at)
            if space < at or nul <= space or nul + 1 + width > len(raw):
                fail("invalid root tree entry")
            mode, name = raw[at:space], raw[space + 1:nul]
            if mode not in (b"40000", b"100644", b"100755", b"120000", b"160000") or not name or b"/" in name or name in names:
                fail("invalid root tree mode/name")
            names.add(name)
            value = raw[nul + 1:nul + 1 + width].hex(); at = nul + 1 + width
            if name == ALLOWLIST_PATH.encode("ascii"):
                if mode not in (b"100644", b"100755"):
                    fail("historical allowlist is not a regular blob")
                found = value
        tree_lists[tree] = found                       # verified absent path, not a failed object lookup
    blobs = batch((value for value in tree_lists.values() if value is not None), "blob")
    lists = {}
    for sha, raw in blobs.items():
        try:
            values = json.loads(text(raw))
        except (ValueError, TypeError):
            fail("invalid historical allowlist JSON")
        if not isinstance(values, list) or not all(isinstance(value, str) and value for value in values):
            fail("historical allowlist is not a list of keys")
        lists[sha] = values
    try:
        ceiling = (HERE / CEILING_PATH).read_bytes()
        maximum = collections.Counter(row["key"] for row in json.loads(ceiling))
    except (OSError, ValueError, TypeError, KeyError):
        fail("immutable ceiling cannot be read")
    if hashlib.sha256(ceiling).hexdigest() != LAUNCH_CEILING_SHA256:
        fail("immutable ceiling changed")
    states = {commit: (collections.Counter(lists[tree_lists[tree]]) if tree_lists[tree] is not None else None)
              for commit, (_, tree) in graph.items()}
    for commit, (parents, _) in graph.items():
        current = states[commit]
        if current is not None and current - maximum:
            fail("historical allowlist exceeds its ceiling at " + commit[:7])
        for parent in parents:
            old = states[parent]
            if old is not None and (current is None or current - old):
                fail("allowlist grew or disappeared from parent " + parent[:7] + " to " + commit[:7])
    return list(lists.values())


def run_ratchet_controls(fm, check):
    """FM-044: reject added, renamed, aliased and dynamic production starts and an expanded allowlist; admitted migration only shrinks."""
    print("\nFM-044: production Python launch ratchet")
    ceiling_bytes = (HERE / CEILING_PATH).read_bytes(); ceiling_rows = json.loads(ceiling_bytes)
    ceiling = [s["key"] for s in ceiling_rows]; allowed = json.loads((HERE / ALLOWLIST_PATH).read_text(encoding="utf-8"))
    source = Path(fm.__file__).read_text(encoding="utf-8")
    check("FM-044: immutable reviewed launch ceiling is unchanged", hashlib.sha256(ceiling_bytes).hexdigest() == LAUNCH_CEILING_SHA256)
    try:
        history = previous_allowlists(fm)
    except RatchetHistoryError as error:
        check("FM-044: required production launch history is readable and monotonic: " + str(error), False)
    else:
        problems = ratchet_problems(source, allowed, ceiling, history)
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
    # Use a real retained caller: a legitimate migration can remove tracked_board_rels
    # (or any other fixed function) from this shrinking list.
    retained = next((row["function"] for row in ceiling_rows if row["key"] in allowed), None)
    renamed = source.replace(f"def {retained}(", f"def renamed_retained_{retained}(", 1) if retained else source
    check("FM-044: renaming a retained caller grants no exemption", retained is not None and renamed != source
          and bool(ratchet_problems(renamed, allowed, ceiling)))
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


def run_review_controls(fm, check, scanner=None):
    """RV-3085–3088: independently reproduced class, refused-root, source-context and reachable-history failures."""
    scanner = scanner or sys.modules[__name__]
    print("\nFM-044: critical round-1 regression controls")
    source = Path(fm.__file__).read_text(encoding="utf-8")
    allowed = json.loads((HERE / ALLOWLIST_PATH).read_text(encoding="utf-8"))
    ceiling = [row["key"] for row in json.loads((HERE / CEILING_PATH).read_text(encoding="utf-8"))]
    for name, extra in {
        "same-named class method": 'class ExtraLauncher:\n    def vcs_process(self):\n        return subprocess.run(["git", "gc"])\n',
        "same-named async class method": 'class ExtraLauncher:\n    async def vcs_process(self):\n        return subprocess.run(["git", "gc"])\n',
        "nested class method": 'class Outer:\n    class Inner:\n        def vcs_process(self):\n            return subprocess.run(["svn", "update"])\n',
        "function-nested class method": 'def outer():\n    class ExtraLauncher:\n        def vcs_process(self):\n            return subprocess.run(["git", "gc"])\n',
    }.items():
        check("RV-3085: rejects " + name, bool(scanner.ratchet_problems(source + "\n" + extra, allowed, ceiling)))
    run_review_root_controls(fm, check)
    run_review_history_controls(fm, check, scanner, source, allowed, ceiling)


def run_review_root_controls(fm, check):
    """RV-3086/3087: two real roots, original symlink/parent resolution, and pre-start execution-context refusals."""
    previous = fm.ROOT
    real_run = subprocess.run
    none = ("_GIT_DIRS", "_TRACKED", "_SVN_LOG", "_GIT_USER", "_STAGED", "_BUILD", "_CHANGES", "_GUARD", "_SIGNERS",
            "_OWNER_POLICY", "_WALK", "_WALK_FAILED", "_ORIGIN_DEFAULT", "_TRUNK_UNTOLD", "_PARTIAL")
    maps = ("_LINE_AUTHOR", "_SVN_BLAME", "_OWNER_COMMITS", "_MODES", "_TREES", "_VIEWS", "_SVN_NEW", "_WALK_COMMITS", "_HAS_SESSIONS", "DERIVED_FILES")
    lists = ("BOARD_UNREAD", "DERIVED_COLUMNS", "DERIVED_NOTES", "INDEX_COLUMNS", "BOARD_COLUMNS")
    flags = ("COMMITTING", "_ASK_ORIGIN", "LAZY_OFF", "DERIVER_LEFT")

    def seed():
        for name in none:
            setattr(fm, name, "old Git A")
        for name in maps:
            getattr(fm, name).clear(); getattr(fm, name)["old Git A"] = "cached"
        for name in lists:
            getattr(fm, name)[:] = ["old Git A"]
        for name in flags:
            setattr(fm, name, True)
        fm._BLAME_REFUSED.add("old Git A")
        fm.ANSWERERS["old Git A"] = "signed"; fm.SEATS["old Git A"] = []; fm.SEAT_RIGHTS["old Git A"] = {"answer"}

    def cleared():
        return (all(getattr(fm, name) is None for name in none) and all(not getattr(fm, name) for name in (*maps, *lists, *flags))
                and not fm._BLAME_REFUSED and all("old Git A" not in getattr(fm, name) for name in ("ANSWERERS", "SEATS", "SEAT_RIGHTS")))

    try:
        with tempfile.TemporaryDirectory(prefix="fm044-root-review-") as tmp:
            area = Path(tmp).resolve(); source = area / "source"; foreign = area / "foreign"
            for root in (source, foreign):
                root.mkdir()
                real_run(["git", "init", "-q", str(root)], capture_output=True, check=True, env=fm.nested_git_env())
                real_run(["git", "config", "user.name", "Fixture"], cwd=root, capture_output=True, check=True)
                real_run(["git", "config", "user.email", "fixture@example.invalid"], cwd=root, capture_output=True, check=True)
                real_run(["git", "config", "commit.gpgsign", "false"], cwd=root, capture_output=True, check=True)
                (root / "note.txt").write_text(root.name + "\n", encoding="utf-8")
                real_run(["git", "add", "note.txt"], cwd=root, capture_output=True, check=True, env=fm.nested_git_env())
                real_run(["git", "commit", "-qm", "source fixture"], cwd=root, capture_output=True, check=True, env=fm.nested_git_env())
            if not (shutil.which("svn") and shutil.which("svnadmin")):
                print("  SKIP RV-3086/3087: real SVN consumer controls need svn and svnadmin")
                return
            server, target = area / "server", area / "svn"
            real_run(["svnadmin", "create", str(server)], capture_output=True, check=True)
            real_run(["svn", "checkout", "-q", server.as_uri(), str(target)], capture_output=True, check=True)
            config = target / "shoalmark.toml"
            for label, text in (("configuration validation", "judged_before_build = \"yes\"\n"), ("configuration parsing", "this is not configuration\n"),
                                ("policy validation", '[seats]\nbuilder = ["same", "same"]\n')):
                fm.configure(source); seed(); config.write_text(text, encoding="utf-8")
                refused = caught(lambda: fm.configure(target), SystemExit) is not None
                check("RV-3086: " + label + " refusal clears every old-root cache", refused and cleared())
            config.unlink()
            fm.configure(source); seed()
            with patch.object(fm.os, "lstat", side_effect=PermissionError("fixture marker denied")):
                check("RV-3086: denied marker clears every old-root cache", refusal(lambda: fm.configure(target), fm) and cleared())
            fm.configure(source); seed(); observed = []

            def denied_root(_root):
                observed.append(cleared() and fm._VCS == ("", None) and fm.CONFIG == {} and fm.ROOT is None)
                raise SystemExit("fixture root discovery denied")

            with patch.object(fm, "find_root", side_effect=denied_root):
                check("RV-3086: all invalidation precedes fallible root discovery", caught(lambda: fm.configure(target), SystemExit) is not None and observed == [True] and cleared())
            with patch.object(fm, "SAFE_WRITES", True), patch.object(fm, "_TRIPWIRE", True):
                fm.configure(target)
                check("RV-3086: successful reset retains process/write enforcement", fm.SAFE_WRITES and fm._TRIPWIRE and cleared() and fm.vcs() == "svn")
            fm.configure(source)
            check("RV-3086: Git reconfiguration succeeds after refused SVN roots", cleared() and fm.vcs() == "git" and fm.git_user() == "Fixture")
            fm.configure(target)
            starts = []

            def monitor(argv, **options):
                starts.append((argv, options))
                return real_run(argv, **options)

            with patch.object(fm, "HERE", source), patch.object(fm.subprocess, "run", side_effect=monitor):
                for args in (("rev-parse", "--show-toplevel"), ("rev-parse", "HEAD"), ("tag", "--points-at", "HEAD"),
                             ("status", "--porcelain", "--untracked-files=all")):
                    before = len(starts); result = fm.git_out(*args, cwd=source, source=True)
                    check("RV-3087: real fixed source read " + " ".join(args), result is not None and len(starts) == before + 1
                          and starts[-1][1]["cwd"] == source and starts[-1][1]["env"] == fm.nested_git_env()
                          and starts[-1][1]["capture_output"] and starts[-1][1]["text"] and starts[-1][1]["encoding"] == "utf-8" and starts[-1][1]["errors"] == "replace")
                check("RV-3087: real source provenance still reports canonical source", fm.source_provenance()[1] == fm.git_out("rev-parse", "HEAD", cwd=source, source=True).strip())
                before = len(starts)
                result = fm.vcs_process("git", "rev-parse", "HEAD", cwd=source, source=True, capture_output=True)
                check("RV-3087: direct fixed read supplies the sanitized source environment", result.returncode == 0 and len(starts) == before + 1
                      and starts[-1][1]["cwd"] == source and starts[-1][1].get("env") == fm.nested_git_env())
                wrong = foreign / "a" / "b" / "c"; wrong.mkdir(parents=True)
                if os.name != "nt":
                    source_alias = area / "source-alias"; source_alias.symlink_to(source, target_is_directory=True)
                    before = len(starts)
                    try:
                        with redirect_stderr(io.StringIO()):
                            result = fm.git_out("rev-parse", "HEAD", cwd=source_alias, source=True)
                    except SystemExit:
                        result = None
                    check("RV-3087: legitimate source alias launches canonical HERE", result is not None and len(starts) == before + 1 and starts[-1][1]["cwd"] == source)
                    alias = source / "a" / "b" / "c"; alias.parent.mkdir(parents=True)
                    alias.symlink_to(wrong, target_is_directory=True)
                    escape = str(alias) + "/../../.."
                    before = len(starts)
                    check("RV-3087: symlink/parent escape refuses before any attempted process", refusal(lambda: fm.git_out("rev-parse", "--show-toplevel", cwd=escape, source=True), fm) and len(starts) == before)
                    loop = source / "loop"; loop.symlink_to(loop)
                    before = len(starts)
                    check("RV-3087: unresolved source path refuses before any attempted process", refusal(lambda: fm.git_out("rev-parse", "HEAD", cwd=loop, source=True), fm) and len(starts) == before)
                for label, options in (("executable", {"executable": sys.executable}), ("shell", {"shell": True}),
                                       ("process context", {"start_new_session": True}), ("input", {"input": "override"}),
                                       ("foreign environment", {"env": {**fm.nested_git_env(), "GIT_DIR": str(foreign / ".git")}}),
                                       ("inherited environment override", {"env": None})):
                    before = len(starts)
                    check("RV-3087: " + label + " refuses before any attempted process",
                          refusal(lambda: fm.vcs_process("git", "rev-parse", "HEAD", cwd=source, source=True, capture_output=True, text=True, **options), fm) and len(starts) == before)
                before = len(starts)
                check("RV-3087: target/arbitrary cwd requests still refuse before start", refusal(lambda: fm.git_out("rev-parse", "HEAD"), fm)
                      and refusal(lambda: fm.git_out("rev-parse", "HEAD", cwd=foreign), fm) and len(starts) == before)
    finally:
        fm.configure(previous)


def run_review_history_controls(fm, check, scanner, original, allowed, ceiling):
    """RV-3088: real reachable graphs, historical transitions, unavailable objects, and the actual outer gate."""
    real_run = subprocess.run
    # Historical graph fixtures must survive retirement of every production VCS
    # start. Use one fixed original ceiling call with the actual frozen boundary;
    # current production source/list/history are independently checked above.
    boundary = next(n for n in ast.parse(original).body
                    if isinstance(n, ast.FunctionDef) and n.name == "vcs_process")
    historical_version = 'def git_version():\n    """The git this run starts, as (major, minor) — one read-only call, `git version` — or None where its answer names no version."""\n    r = subprocess.run(["git", "version"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", env=nested_git_env())\n    m = re.search(r"(\\d+)\\.(\\d+)", r.stdout) if r.returncode == 0 else None\n    return (int(m.group(1)), int(m.group(2))) if m else None\n'
    original = "import subprocess, os, sys\n" + ast.unparse(boundary) + "\n" + historical_version
    initial_sites, initial_errors = scanner.launch_sites(original)
    allowed = [site["key"] for site in initial_sites]
    check("RV-3088: fixed historical fixture retains one original ceiling start",
          not initial_errors and len(allowed) == 1 and allowed[0] in ceiling)

    class MigrateVersion(ast.NodeTransformer):
        def visit_FunctionDef(self, node):
            if node.name != "git_version":
                return node
            for call in ast.walk(node):
                if isinstance(call, ast.Call) and isinstance(call.func, ast.Attribute) and ast.unparse(call.func) == "subprocess.run":
                    call.func = ast.Name(id="vcs_process", ctx=ast.Load()); call.args = call.args[0].elts + call.args[1:]
            return node

    smaller = ast.unparse(ast.fix_missing_locations(MigrateVersion().visit(ast.parse(original)))) + "\n"
    sites, errors = scanner.launch_sites(smaller); small_keys = [site["key"] for site in sites]
    check("RV-3088: fixed version migration removes exactly one original ceiling key", not errors and len(small_keys) == len(allowed) - 1
          and len(collections.Counter(allowed) - collections.Counter(small_keys)) == 1
          and not scanner.ratchet_problems(smaller, small_keys, ceiling, [allowed]))
    with tempfile.TemporaryDirectory(prefix="fm044-history-review-") as tmp:
        root = Path(tmp).resolve()
        ceiling_bytes = (HERE / CEILING_PATH).read_bytes()
        env = fm.nested_git_env(); env["GIT_CEILING_DIRECTORIES"] = str(root.parent)
        fixture = SimpleNamespace(__file__=str(root / "shoalmark.py"), nested_git_env=lambda: dict(env))

        def git(*args):
            return real_run(["git", *args], cwd=root, capture_output=True, check=True, env=env).stdout.decode("utf-8").strip()

        def write(source, keys):
            (root / "shoalmark.py").write_text(source, encoding="utf-8")
            (root / ALLOWLIST_PATH).write_text(json.dumps(keys) + "\n", encoding="utf-8")
            (root / CEILING_PATH).write_bytes(ceiling_bytes)

        def commit(message):
            git("add", "."); git("commit", "-qm", message); return git("rev-parse", "HEAD")

        refused = [""]                                 # what the last read of history refused with, for the check's own line

        def passes(source, keys):
            try:
                history = scanner.previous_allowlists(fixture)
            except scanner.RatchetHistoryError as error:   # that type only: the check fails on its own line with its text (RV-3251)
                refused[0] = f" (refused: {error})"
                return False
            refused[0] = ""
            return not scanner.ratchet_problems(source, keys, ceiling, history)

        def proof_refuses():
            try:
                scanner.previous_allowlists(fixture)
            except Exception as error:
                return type(error).__name__ == "RatchetHistoryError"
            return False

        git("init", "-q"); git("config", "user.name", "History fixture"); git("config", "user.email", "fixture@example.invalid")
        git("config", "commit.gpgsign", "false")
        (root / "record.txt").write_text("before introduction\n", encoding="utf-8"); first = commit("before introduction")
        write(original, allowed)
        with patch.object(scanner, "HERE", root):
            ok_ = passes(original, allowed)
            check("RV-3088: readable first introduction with no earlier list succeeds" + refused[0], ok_)
            initial = commit("introduce launch ratchet")
            ok_ = passes(original, allowed)
            check("RV-3088: readable absent introduction parent succeeds" + refused[0], ok_)
            git("checkout", "-qb", "shrinking"); write(smaller, small_keys); shrunk = commit("migrate historical version launch")
            ok_ = passes(smaller, small_keys)
            check("RV-3088: committed one-to-zero fixture migration succeeds" + refused[0], ok_)
            write(original, allowed)
            check("RV-3088: working-tree resurrection refuses readable history", not passes(original, allowed))
            hidden = root / ".git-hidden"
            (root / ".git").rename(hidden)
            try:
                check("RV-3088: actual unavailable Git history refuses", proof_refuses())
                records = []
                try:
                    with redirect_stdout(io.StringIO()):
                        scanner.run_ratchet_controls(fixture, lambda name, result: records.append((name, result)))
                except Exception:
                    records = []                         # incidental exception is not the deliberate outer failing check
                check("RV-3088: unavailable history deliberately fails the outer ratchet gate", any(not value and "history" in name for name, value in records))
            finally:
                hidden.rename(root / ".git")
            check("RV-3088: restored actual history still rejects working-tree resurrection", not passes(original, allowed))
            git("checkout", "-fqb", "records", initial)
            (root / "record.txt").write_text("records branch\n", encoding="utf-8"); records_base = commit("records-only branch")
            git("merge", "--no-ff", "--no-commit", "shrinking"); write(original, allowed); bad_merge = commit("merge retaining stale source and list")
            check("RV-3088: merge retaining a stale parent key refuses", not passes(original, allowed))
            (root / "record.txt").write_text("after bad merge\n", encoding="utf-8"); commit("records after bad merge")
            check("RV-3088: records descendant cannot hide bad merge", not passes(original, allowed))
            write(smaller, small_keys); commit("shrink again after bad merge")
            check("RV-3088: later shrink cannot hide historical growth", not passes(smaller, small_keys))
            (root / "record.txt").write_text("after later shrink\n", encoding="utf-8"); commit("records after later shrink")
            check("RV-3088: records descendant of later shrink still refuses bad history", not passes(smaller, small_keys))
            git("replace", bad_merge, records_base)
            try:
                check("RV-3088: actual replace object cannot hide the bad merge transition", proof_refuses())
            finally:
                git("replace", "-d", bad_merge)
            git("checkout", "-fqb", "valid-merge", records_base); git("merge", "--no-ff", "-m", "valid shrinking merge", "shrinking")
            ok_ = passes(smaller, small_keys)
            check("RV-3088: valid merge retaining the reduction succeeds" + refused[0], ok_)
            for label, rev in (("list blob", "HEAD:" + ALLOWLIST_PATH), ("root tree", "HEAD^{tree}"), ("required parent commit", initial)):
                sha = git("rev-parse", rev); obj = root / ".git" / "objects" / sha[:2] / sha[2:]; hidden_obj = obj.with_name(obj.name + ".hidden")
                obj.rename(hidden_obj)
                try:
                    check("RV-3088: actual unavailable " + label + " refuses", proof_refuses())
                finally:
                    hidden_obj.rename(obj)
            for label, raw in (("invalid JSON", b"not JSON\n"), ("empty JSON", b""), ("invalid UTF-8", b'["\xff"]'),
                               ("invalid JSON shape", b'{"keys":[]}'), ("invalid JSON key", b'[null]')):
                git("checkout", "-fqb", label.replace(" ", "-"), initial)
                (root / ALLOWLIST_PATH).write_bytes(raw); commit("historical " + label); write(original, allowed)
                check("RV-3088: " + label + " in reachable history refuses deliberately", proof_refuses())
            git("checkout", "-fqb", "empty-list", first); write(original, []); commit("explicit empty metadata list")
            try:
                zero_, said_ = scanner.previous_allowlists(fixture), ""
            except scanner.RatchetHistoryError as error:   # that type only: it fails here, on its own line, and the suite goes on (RV-3251)
                zero_, said_ = None, f" (refused: {error})"
            check("RV-3088: valid explicit zero-entry historical list is readable" + said_, zero_ == [[]])
            git("checkout", "-fqb", "duplicate-growth", initial); write(original, allowed + allowed[:1]); commit("duplicate multiset growth"); write(original, allowed)
            check("RV-3088: historical duplicate-key growth refuses", proof_refuses())
            git("checkout", "-fqb", "deleted-list", initial); (root / ALLOWLIST_PATH).unlink(); commit("delete introduced list"); write(original, allowed)
            check("RV-3088: deletion after introduction refuses", proof_refuses())
            git("checkout", "-fqb", "read-faults", shrunk); write(smaller, small_keys)
            for label, command in (("HEAD read", "rev-parse"), ("graph read", "log"), ("object batch read", "cat-file")):
                hits = []
                def failed(argv, _command=command, **options):
                    if _command in argv and "--no-replace-objects" in argv:
                        hits.append(argv)
                        return subprocess.CompletedProcess(argv, 128, b"", b"fixture read denied")
                    return real_run(argv, **options)
                with patch.object(scanner.subprocess, "run", side_effect=failed):
                    check("RV-3088: failed " + label + " refuses", proof_refuses() and len(hits) == 1)
            hits = []
            def invalid_revision(argv, **options):
                if "--no-replace-objects" in argv and "HEAD^{commit}" in argv:
                    hits.append(argv)
                    return subprocess.CompletedProcess(argv, 0, b"invalid-revision\n", b"")
                return real_run(argv, **options)
            with patch.object(scanner.subprocess, "run", side_effect=invalid_revision):
                check("RV-3088: successful malformed revision output refuses", proof_refuses() and len(hits) == 1)
            graft = root / ".git" / "info" / "grafts"
            graft.write_text(shrunk + "\n", encoding="ascii")
            try:
                check("RV-3088: actual graft cannot hide a required parent transition", proof_refuses())
            finally:
                graft.unlink()
            git("checkout", "--orphan", "root-introduction", initial); write(original, allowed); commit("genuine root introduction")
            ok_ = passes(original, allowed)
            check("RV-3088: readable genuine root introduction succeeds" + refused[0], ok_)
        clone = root / "shallow"
        real_run(["git", "clone", "-q", "--depth=1", root.as_uri(), str(clone)], capture_output=True, check=True, env=env)
        (clone / CEILING_PATH).write_bytes(ceiling_bytes)
        with patch.object(scanner, "HERE", clone):
            check("RV-3088: actual shallow required history refuses", proof_refuses())
