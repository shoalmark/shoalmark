"""FM-044 A: bounded local SVN board and installation controls.

Run directly, or call run_shared_controls(tool, check) from the serial integration seat.
The fixture server and Git executable are unavailable during measured SVN board runs.
These controls do not certify authority/history, native Windows or the complete shared CLI.
"""

from contextlib import redirect_stderr, redirect_stdout
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import socket
import subprocess
import sys
import tempfile
import time
import traceback
from unittest.mock import patch
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
STATUS = ["svn", "status", "--verbose", "--no-ignore", "--ignore-externals", "--depth", "infinity", ".", "--xml"]


def load_tool(source=None):
    source = source or os.environ.get("SHOALMARK_SHARED_SOURCE") or HERE / "shoalmark.py"
    spec = importlib.util.spec_from_file_location("shared_tool", source)
    tool = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(tool)
    return tool


def probe(root, scenario):
    """Separate interpreter: observe attempts BEFORE the product hook, including refused attempts."""
    events = []
    active = [False]
    def observe(event, args):
        if not active[0]:
            return
        if event == "subprocess.Popen":
            if args[0] is None and isinstance(args[1], str):
                # Windows' audit shape (RV-3061): no program, one command line. Windows starts its first word; the raw line is kept for
                # exact checks, and its argv is read back as the suite reads one (`fm.split_cmdline`, as `_watch_git` does).
                argv = fm.split_cmdline(args[1])
                events.append([event, argv[0] if argv else "", argv, str(args[2]), args[1]])
            else:
                events.append([event, str(args[0]), [str(a) for a in args[1]], str(args[2])])
        elif event == "socket.connect":
            events.append([event, str(args[1])])
        elif event == "open":
            flags = args[2] if isinstance(args[2], int) else 0
            if any(c in str(args[1] or "") for c in "wax+") or flags & (os.O_WRONLY | os.O_RDWR | os.O_APPEND | os.O_CREAT | os.O_TRUNC):
                events.append([event, str(args[0])])
    sys.addaudithook(observe)
    fm = load_tool()
    tempfile.gettempdir()                           # fixture initializes stdlib's one-time temporary-directory probe before measurement
    operation = "--html-only"
    correction = json.loads(scenario[len("corrective:"):]) if scenario.startswith("corrective:") else None
    completed = []
    if correction is not None:
        original = fm.vcs_process
        def corrected_query(program, *args, **options):
            if program == "svn" and args == tuple(STATUS[1:]) and correction.get("cwd"):
                options["cwd"] = correction["cwd"]
            if program == "svn" and args[:1] == (correction.get("xml_command"),):
                return subprocess.CompletedProcess([], 0, correction["xml"].encode(), b"")
            result = original(program, *args, **options)
            completed.append([program, list(args), str(options.get("cwd")), result.returncode])
            return result
        fm.vcs_process = corrected_query
    if scenario.startswith("setup:"):
        _, mode, *fault = scenario.split(":")
        operation = "--init" if mode == "init" else "--install-hook"
        if fault:
            original = fm.vcs_process
            def failed(program, *args, **options):
                if program == "svn" and args[:1] == (fault[0],):
                    return subprocess.CompletedProcess([], 1, b"", b"svn: E155004: injected setup failure") if not options.get("text") else subprocess.CompletedProcess([], 1, "", "svn: E155004: injected setup failure")
                return original(program, *args, **options)
            fm.vcs_process = failed
    if scenario.startswith("start:"):
        cmd = json.loads(scenario[6:])
        original = fm.render_html
        def render(trackers):
            subprocess.run(cmd, capture_output=True)
            return original(trackers)
        fm.render_html = render
    elif scenario == "network":
        fm.render_html = lambda trackers: socket.create_connection(("127.0.0.1", 9), timeout=0.1)
    elif scenario == "write":
        fm.render_html = lambda trackers: (Path(root) / "forbidden.txt").write_text("bad", encoding="utf-8")
    elif scenario in ("malformed_xml", "failed_status"):
        original = fm.vcs_process
        def query(program, *args, **options):
            if program == "svn" and args == tuple(STATUS[1:]):
                return subprocess.CompletedProcess([], 0 if scenario == "malformed_xml" else 1, b"<broken>" if scenario == "malformed_xml" else b"", b"" if scenario == "malformed_xml" else b"svn: E155004: working copy locked")
            return original(program, *args, **options)
        fm.vcs_process = query
    out, err = io.StringIO(), io.StringIO()
    active[0] = True
    try:
        with redirect_stdout(out), redirect_stderr(err):
            try:
                if correction is not None and correction.get("mode") == "properties":
                    fm.configure(root)
                    fm.svn_local_properties(correction.get("rel", "."))
                    code = 0
                elif correction is not None and correction.get("mode") == "install":
                    code = fm.main(["--root", str(root), "--install-hook"])
                elif correction is not None:
                    code = fm.board_run(root)
                else:
                    code = fm.main(["--root", str(root), operation])
            except fm.SvnUnreadable as e:
                code = 4
                print(str(e), file=sys.stderr)
            except SystemExit as e:
                code = e.code
    finally:
        active[0] = False
    print(json.dumps({"code": code, "out": out.getvalue(), "err": err.getvalue(), "events": events,
                      "git_absent": shutil.which("git") is None, "svn_present": shutil.which("svn") is not None, "completed": completed}))


def command(root, *argv):
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update(GIT_AUTHOR_NAME="fixture", GIT_AUTHOR_EMAIL="fixture@example.invalid", GIT_COMMITTER_NAME="fixture", GIT_COMMITTER_EMAIL="fixture@example.invalid")
    return subprocess.run(list(argv), cwd=root, env=env, capture_output=True, check=True)


def svn_only(folder):
    """The measured runs' search folder, as test_vcs_entry.svn_search builds it: svn under the name svn has — `svn.exe` on Windows, which a
    start of `svn` looks for there — its DLLs beside it on Windows, and no Git. A link named `svn` alone is no program on Windows (PR #173)."""
    from test_vcs_entry import svn_search          # imported here: the probe this file also runs loads nothing more before it measures
    return svn_search(folder, shutil.which("svn"))


def svn_property(root, name, rel):
    """A property's value as svn stores it, the same on every system: `svn propget --xml` prints it only escaped (svn 1.14.5 cmdline.c:792-825),
    where plain `propget` turns an `svn:` property's line ends into the system's, `\\r\\n` on Windows, and adds one (propget-cmd.c:219-229).
    None where svn answers with another property or an encoded one; a property not set is svn's own refusal (exit 1), as plain `propget`'s."""
    node = ET.fromstring(command(root, "svn", "propget", "--xml", name, rel).stdout).find("target/property")
    return None if node is None or node.get("name") != name or node.get("encoding") else node.text or ""


def exact_start(event, argv):
    """A probe's recorded start is exactly `argv`: in Windows' shape its raw line (the fifth field) against CPython's own spelling, in POSIX's its list."""
    from test_vcs_entry import same_start
    return same_start(event[2], event[4] if len(event) > 4 else None, argv)


def saw(got):
    """What a measured run or the CLI said: its exit code and the first 300 characters of its stderr, so a failing check explains itself."""
    if isinstance(got, subprocess.CompletedProcess):
        return f"saw {got.returncode}, stderr {got.stderr[:300]!r}"
    return f"saw {got['code']}, stderr {got['err'][:300]!r}"


def fixture_saw(error):
    """What a fixture step that failed saw, as `guarded` caught it: the command, its exit code and the first 300 characters of its stderr, or the
    error; then the block's line it stopped at, and the innermost suite line where that differs (a helper such as `command`)."""
    if isinstance(error, subprocess.CalledProcessError):
        stderr = error.stderr.decode("utf-8", "replace") if isinstance(error.stderr, bytes) else str(error.stderr or "")
        cmd = error.cmd if isinstance(error.cmd, str) else " ".join(map(str, error.cmd))
        said = f"`{cmd}` exited {error.returncode}, stderr {stderr[:300]!r}"
    else:
        said = f"{type(error).__name__}: {str(error)[:300]!r}"
    ours = [f"{Path(f.filename).name}:{f.lineno}" for f in traceback.extract_tb(error.__traceback__)[1:] if Path(f.filename).name.startswith("test_")]
    return said + (f" at {ours[0]}" if ours else "") + (f" (innermost {ours[-1]})" if len(ours) > 1 else "")


def guarded(block, check, controls, /, *args, **kwargs):
    """Run one block of controls. A fixture step that fails — a setup command `check=True` refuses, a program that does not start, a fixture's
    own precondition — is a named FAIL with what it saw, and the next block runs; the block's later checks cannot run without it. Before,
    the traceback ended the whole suite (PR #173's run 38539381661, Windows, A1: `svn add` of a page no measured run had written)."""
    try:
        controls(*args, **kwargs)
    except (subprocess.SubprocessError, OSError, AssertionError) as error:
        check(f"{block}: a fixture step failed, and the block's later checks did not run ({fixture_saw(error)})", False)


def corpus(root):
    (root / "shoalmark.toml").write_text('name = "local fixture"\ntracker_dir = "work-tracker"\n[kinds]\nWORK = "Work"\n', encoding="utf-8")
    folder = root / "work-tracker"
    folder.mkdir(parents=True)
    (folder / "WORK-001-local.md").write_text('---\nid: WORK-001\nstatus: In Progress\nconsidered: none\nhook: "local content"\n---\n\n# WORK-001 — local\n\n## What is true now\n\nRecorded content.\n\n## Done when\n\nRead locally.\n', encoding="utf-8")
    return folder


def board_snapshot(folder):
    paths = [folder / "index.html", *sorted((folder / "view").glob("*"))]
    return {p.relative_to(folder).as_posix(): p.read_bytes() for p in paths if p.is_file() and not p.is_symlink()}


def measured(root, search, scenario="normal"):
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update(PATH=str(search), PYTHONDONTWRITEBYTECODE="1")
    r = subprocess.run([sys.executable, "-B", str(Path(__file__).resolve()), "--probe", str(root), scenario], env=env, capture_output=True, text=True, encoding="utf-8", timeout=30)
    if r.returncode:
        raise AssertionError(f"probe failed {r.returncode}: {r.stderr[:600]}")
    return json.loads(r.stdout)


def run_board_local_controls(fm, check):
    print("\nFM-044 A1: local SVN board, real no-Git and unavailable-server fixtures")
    original_root = fm.ROOT
    check("A1: exact SVN list and tuple are admitted", fm.read_only_svn(STATUS) and fm.read_only_svn(tuple(STATUS)))
    bad = [STATUS + ["x"], STATUS[:-1], ["/usr/bin/svn", *STATUS[1:]], ["svn.exe", *STATUS[1:]],
           ["svn", "status", "-u", ".", "--xml"], ["svn", "status", "--show-updates", ".", "--xml"],
           ["svn", "status", "--include-externals", ".", "--xml"], ["svn", "status", "https://example.invalid/repo", "--xml"],
           ["svn", "status", "-r", "HEAD", ".", "--xml"], ["svn", "log", "."], ["svn", "blame", "file"],
           ["svn", "cat", "file"], ["svn", "info", "."], ["svn", "update"], ["svn", "commit"], ["svn", "add", "x"],
           ["svn", "propset", "p", "v", "."], ["sh", "-c", "svn status"], "svn status", None]
    for n, argv in enumerate(bad):
        check(f"A1: local predicate refuses altered argv {n}", not fm.read_only_svn(argv))
    if not (shutil.which("svn") and shutil.which("svnadmin")):
        print("  SKIP A1 real SVN fixtures: svn and svnadmin required")
        return
    try:
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp).resolve()
            server, root, search = base / "server", base / "wc", base / "no-git-bin"
            command(base, "svnadmin", "create", str(server))
            command(base, "svn", "checkout", "-q", server.as_uri(), str(root))
            folder = corpus(root)
            svn_only(search)
            command(root, "svn", "add", "shoalmark.toml", "work-tracker")
            command(root, "svn", "commit", "-q", "-m", "local fixture", "--username", "fixture-author")
            states = base / "board-states"
            command(base, "svn", "checkout", "-q", server.as_uri(), str(states))
            state_folder = states / "work-tracker"; (state_folder / "view").mkdir()
            (state_folder / "index.html").write_bytes(b"versioned page\n")
            (state_folder / "view" / "WORK-001.js").write_bytes(b"versioned view\n")
            command(states, "svn", "add", "work-tracker/index.html", "work-tracker/view")
            command(states, "svn", "commit", "-q", "-m", "versioned board controls")
            nested_wc = base / "nested-working-copy"
            command(base, "svn", "checkout", "-q", server.as_uri(), str(nested_wc))
            server.rename(base / "server-unavailable")
            got = measured(root, search)
            check(f"A1: real public SVN board succeeds with Git absent and server unavailable ({saw(got)}; git absent {got['git_absent']}, svn present {got['svn_present']})",
                  got["code"] == 0 and got["git_absent"] and got["svn_present"] and "Recorded content" in (folder / "view" / "WORK-001.js").read_text(encoding="utf-8"))
            starts = [e for e in got["events"] if e[0] == "subprocess.Popen"]
            check(f"A1: one exact local consumer status start and no Git or network attempt ({saw(got)}; starts {str([e[1:] for e in starts])[:300]})",
                  len(starts) == 1 and exact_start(starts[0], STATUS) and starts[0][3] == str(root) and not any(e[0] == "socket.connect" for e in got["events"]))
            writes = [e[1] for e in got["events"] if e[0] == "open" and not e[1].isdigit()]
            check(f"A1: actual successful writes are confined to page and views ({saw(got)}; writes {str(writes)[:300]})",
                  bool(writes) and all(Path(p) == folder / "index.html" or Path(p).parent == folder / "view" for p in writes))
            before = board_snapshot(folder)
            env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
            env.update(PATH=str(search), PYTHONDONTWRITEBYTECODE="1")
            cli = subprocess.run([sys.executable, "-B", str(HERE / "shoalmark.py"), "--root", str(root), "--html-only"], env=env, capture_output=True, text=True, encoding="utf-8", timeout=30)
            check(f"A1: direct production CLI succeeds with no Git and unavailable server ({saw(cli)})",
                  cli.returncode == 0 and "file://" in cli.stdout and cli.stderr == "Subversion: this local run cannot verify commit signatures or server-authenticated authors; protected SVN acceptance remains held.\n")
            for scenario in ("malformed_xml", "failed_status"):
                got = measured(root, search, scenario)
                check(f"A1: injected unreadable query refuses before writes ({scenario}; {saw(got)})", got["code"] == 4 and "metadata could not be read" in got["err"] and board_snapshot(folder) == before and not any(e[0] == "open" and not e[1].isdigit() for e in got["events"]))
            empty_search = base / "no-vcs-bin"; empty_search.mkdir()
            got = measured(root, empty_search)
            check(f"A1: actually absent SVN refuses without changing the board ({saw(got)})", got["code"] == 4 and "svn could not be run" in got["err"] and not got["svn_present"] and board_snapshot(folder) == before)
            source = root / "tools" / "shoalmark"; source.mkdir(parents=True)
            for name in ("shoalmark.py", "VERSION"):
                shutil.copy2(HERE / name, source / name)
            for name in ("vendor", "brand"):
                shutil.copytree(HERE / name, source / name)
            cli = subprocess.run([sys.executable, "-B", str(source / "shoalmark.py"), "--root", str(root), "--html-only"], cwd=source, env=env, capture_output=True, text=True, encoding="utf-8", timeout=30)
            # the product prints `board: ` and the page's resolved URI (`board_link`); the same form, resolved the same way, on every system (RV-3230)
            board_ = "board: " + (folder / "index.html").resolve().as_uri()
            check(f"A1: installed source below ROOT refreshes the consumer board without Git ({saw(cli)}; stdout {cli.stdout[:300]!r}; expected {board_!r})",
                  cli.returncode == 0 and board_ in cli.stdout.splitlines() and not (source / "work-tracker").exists())
            # The fixed local query includes ignored boards, so they remain writable after ordinary ignore setup.
            command(root, "svn", "propset", "svn:ignore", "index.html\nview\n", "work-tracker")
            got = measured(root, search)
            check(f"A1: actual ignored board paths are writable through the same local snapshot ({saw(got)})", got["code"] == 0 and "file://" in got["out"])
            for scenario in ("start:" + json.dumps(["svn", "log", "."]), "start:" + json.dumps(["git", "version"]), "start:" + json.dumps([sys.executable, "-c", "pass"]), "network", "write"):
                got = measured(root, search, scenario)
                check(f"A1: actual audit refusal precedes side effect ({scenario[:45]}; {saw(got)})", got["code"] == 4 and "was stopped" in got["err"] and board_snapshot(folder) == before and not (root / "forbidden.txt").exists())
                check(f"A1: independent observer records refused attempt ({scenario[:45]}; {saw(got)}; events {str([e[:2] for e in got['events']])[:300]})",
                      len([e for e in got["events"] if e[0] == "subprocess.Popen"]) == 2 if scenario.startswith("start:") else any(e[0] == ("socket.connect" if scenario == "network" else "open") for e in got["events"]))
            fm.configure(root)
            with patch.object(fm, "_VCS", ("svn", root)):
                for executable, cwd in (("other-program", root), ("svn", base), ("svn", None)):
                    try:
                        fm.board_judge("subprocess.Popen", (executable, STATUS, cwd, None))
                        refused = False
                    except fm.ReadOnlyRun:
                        refused = True
                    check(f"A1: audit refuses executable/cwd substitution ({executable}, {cwd})", refused)
            # Parser controls hold the path/status contract independently of svn's XML serializer.
            def xml(item="normal", attrs="", path="work-tracker/index.html"):
                return ET.fromstring(f'<status><target path="."><entry path="."><wc-status item="normal" props="none"/></entry><entry path="{path}"><wc-status item="{item}" props="none" {attrs}/></entry></target></status>')
            for item in ("normal", "modified", "added", "replaced", "deleted", "missing", "conflicted", "merged"):
                with patch.object(fm, "svn_run", return_value=xml(item)):
                    check(f"A1: versioned status {item} protects the page", fm.tracked_board_rels() == ["work-tracker/index.html"])
            for item in ("unversioned", "ignored"):
                with patch.object(fm, "svn_run", return_value=xml(item)):
                    check(f"A1: successful explicit {item} status permits ordinary write rules", fm.tracked_board_rels() == [])
            malformed = [None, ET.fromstring("<info/>"), ET.fromstring('<status><target path="."/></status>'),
                         xml("incomplete"), xml("external"), xml("obstructed"), xml("unknown"), xml("none"),
                         xml(attrs='switched="true"'), xml(attrs='tree-conflicted="true"'), xml(path="../escape"), xml(path="/absolute")]
            malformed.append(ET.fromstring('<status><target path="."><entry path="."><wc-status item="normal" props="none"/></entry><entry path="work-tracker/index.html"><wc-status item="normal"/></entry></target></status>'))
            for n, status in enumerate(malformed):
                with patch.object(fm, "svn_run", return_value=status):
                    try:
                        fm.tracked_board_rels()
                        refused = False
                    except fm.SvnUnreadable:
                        refused = True
                    check(f"A1: unavailable/inconsistent status refuses {n}", refused)
            # Actual scheduled page: neither page nor existing view bytes change, and no usable link is printed.
            command(root, "svn", "add", "--no-ignore", "work-tracker/index.html")
            before = board_snapshot(folder)
            got = measured(root, search)
            check(f"A1: actual scheduled page and its views stay byte identical without a link ({saw(got)})", got["code"] == 0 and board_snapshot(folder) == before and "Subversion versions it" in got["err"] and "file://" not in got["out"])
            command(root, "svn", "revert", "work-tracker/index.html")
            command(root, "svn", "add", "--no-ignore", "work-tracker/view")
            views = {k: v for k, v in board_snapshot(folder).items() if k.startswith("view/")}
            got = measured(root, search)
            page = (folder / "index.html").read_text(encoding="utf-8")
            check(f"A1: scheduled view directory is unchanged and page is inert ({saw(got)})", got["code"] == 0 and all(board_snapshot(folder).get(k) == v for k, v in views.items()) and "default-src 'none'" in page and not any(s in page for s in ("<script", "<style", "<img", "<link")) and "Subversion versions" in got["err"])
            command(root, "svn", "revert", "-R", "work-tracker/view")
            # Valid explicit subtree and reconfiguration never reuse another root's inventory.
            sub = root / "sub"; sub.mkdir(); corpus(sub)
            command(root, "svn", "add", "sub")
            got = measured(sub, search)
            check(f"A1: actual explicit SVN subdirectory works without Git or server ({saw(got)})", got["code"] == 0 and got["git_absent"] and [e[3] for e in got["events"] if e[0] == "subprocess.Popen"] == [str(sub)])
            gitroot = base / "git-root"; gitroot.mkdir(); gitfolder = corpus(gitroot)
            command(gitroot, "git", "init", "-q")
            (gitfolder / "index.html").write_text("committed page", encoding="utf-8")
            command(gitroot, "git", "add", ".")
            command(gitroot, "git", "-c", "core.hooksPath=/dev/null", "-c", "commit.gpgsign=false", "commit", "-qm", "Git fixture")
            fm.configure(gitroot)
            git_inventory = fm.tracked_board_files()
            fm.configure(sub)
            svn_inventory = fm.tracked_board_files()
            # the inventory holds the product's `_norm` of paths under its resolved ROOT (`find_root`): both sides compared so (RV-3231)
            git_page_, git_home_ = fm._norm(gitfolder.resolve() / "index.html"), fm._norm(gitroot.resolve())
            check(f"A1: real Git-to-SVN reconfigure clears the inventory (saw git {str(sorted(git_inventory))[:300]}, svn {str(sorted(svn_inventory))[:300]}; "
                  f"expected {git_page_!r})", git_page_ in git_inventory and all(git_home_ not in p for p in svn_inventory))
            out, err = io.StringIO(), io.StringIO()
            with redirect_stdout(out), redirect_stderr(err):
                code = fm.board_run(gitroot)
            check(f"A1: real retained Git tracked-page protection (saw {code}, stderr {err.getvalue()[:300]!r})", code == 0 and (gitfolder / "index.html").read_text(encoding="utf-8") == "committed page" and "git tracks it" in err.getvalue())
            before = board_snapshot(state_folder)
            got = measured(states, search)
            check(f"A1: actual normal versioned page/views stay byte identical ({saw(got)})", got["code"] == 0 and board_snapshot(state_folder) == before and "file://" not in got["out"])
            (state_folder / "index.html").write_bytes(b"locally modified versioned page\n")
            (state_folder / "view" / "WORK-001.js").write_bytes(b"locally modified versioned view\n")
            before = board_snapshot(state_folder)
            got = measured(states, search)
            check(f"A1: actual modified versioned page/views stay byte identical ({saw(got)})", got["code"] == 0 and board_snapshot(state_folder) == before)
            command(states, "svn", "revert", "-R", "work-tracker")
            for state in ("deleted", "missing", "replaced", "obstructed"):
                page_path = state_folder / "index.html"
                if state in ("deleted", "replaced"):
                    command(states, "svn", "delete", "work-tracker/index.html")
                    if state == "replaced":
                        page_path.write_bytes(b"scheduled replacement page\n")
                        command(states, "svn", "add", "work-tracker/index.html")
                else:
                    page_path.unlink()
                    if state == "obstructed":
                        page_path.mkdir()
                before = board_snapshot(state_folder)
                got = measured(states, search)
                check(f"A1: actual {state} board path is never overwritten/recreated ({saw(got)})", got["code"] == (4 if state == "obstructed" else 0) and board_snapshot(state_folder) == before and (page_path.is_dir() if state == "obstructed" else not page_path.exists() if state in ("missing", "deleted") else page_path.read_bytes() == b"scheduled replacement page\n"))
                if page_path.is_dir():
                    page_path.rmdir()
                command(states, "svn", "revert", "work-tracker/index.html")
            command(states, "svn", "copy", "work-tracker/view/WORK-001.js", "work-tracker/view/WORK-002.js")
            before = board_snapshot(state_folder)
            got = measured(states, search)
            check(f"A1: actual scheduled copied view remains protected ({saw(got)})", got["code"] == 0 and board_snapshot(state_folder) == before)
            saved_view = base / "saved-view"
            (folder / "view").rename(saved_view); nested_wc.rename(folder / "view")
            before = board_snapshot(folder)
            got = measured(root, search)
            check(f"A1: actual nested WC ambiguity refuses before board writes ({saw(got)})", got["code"] == 4 and "nested Subversion working copy" in got["err"] and board_snapshot(folder) == before)
            (folder / "view").rename(nested_wc); saved_view.rename(folder / "view")
            # Actual metadata failure occurs before the first board write.
            before = board_snapshot(folder)
            (root / ".svn" / "wc.db").rename(root / ".svn" / "wc.db-hidden")
            got = measured(root, search)
            check(f"A1: real missing working-copy metadata refuses before every board write ({saw(got)})", got["code"] == 4 and board_snapshot(folder) == before and not any(e[0] == "open" and not e[1].isdigit() for e in got["events"]))
            (root / ".svn" / "wc.db-hidden").rename(root / ".svn" / "wc.db")
    finally:
        fm.configure(original_root)


def run_shared_controls(fm, check):
    guarded("A1", check, run_board_local_controls, fm, check)
    guarded("A2", check, run_svn_setup_controls, fm, check)
    guarded("A corrections", check, run_corrective_controls, fm, check)


def run_svn_setup_controls(fm, check):
    print("\nFM-044 A2: honest local SVN initialization/property installation")
    if not (shutil.which("svn") and shutil.which("svnadmin")):
        print("  SKIP A2 real SVN fixtures: svn and svnadmin required")
        return
    previous = fm.ROOT
    try:
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp).resolve(); server = base / "server"; search = base / "bin"
            command(base, "svnadmin", "create", str(server))
            svn_only(search)
            roots = {}
            for name in ("init", "info-fail", "add-fail", "propset-fail", "install", "install-info-fail", "install-proplist-fail", "install-propset-fail", "bad-db", "foreign"):
                root = base / name
                command(base, "svn", "checkout", "-q", server.as_uri(), str(root))
                roots[name] = root
                if name.startswith("install"):
                    corpus(root)
                    command(root, "svn", "add", "shoalmark.toml", "work-tracker")
                    source = root / "tools" / "shoalmark"; source.mkdir(parents=True)
                    (source / "shoalmark.py").write_bytes((HERE / "shoalmark.py").read_bytes())
            server.rename(base / "server-unavailable")
            root = roots["init"]
            got = measured(root, search, "setup:init")
            folder = root / "docs" / "work-tracker"
            ignored = svn_property(root, "svn:ignore", "docs/work-tracker") if got["code"] == 0 and folder.is_dir() else None
            check(f"A2: actual no-Git/server-free init schedules tracker folder and ignores the board ({saw(got)}; svn:ignore {ignored!r})",
                  got["code"] == 0 and got["git_absent"] and (folder / "TRIAGE.md").is_file() and ignored == "index.html\nview\n")
            check("A2: SVN init advice has no Git session setup or client-hook claim", "git config" not in got["out"] and "--session new" not in got["out"] and "SVN CLI runs no client hook" in got["out"])
            before = {p.relative_to(root).as_posix(): p.read_bytes() for p in root.rglob("*") if p.is_file() and ".svn" not in p.parts}
            got = measured(root, search, "setup:init")
            after = {p.relative_to(root).as_posix(): p.read_bytes() for p in root.rglob("*") if p.is_file() and ".svn" not in p.parts}
            check("A2: repeat no-Git init leaves scaffold and property bytes unchanged", got["code"] == 0 and before == after and not any(e[0] == "subprocess.Popen" and e[2][1:2] in (["add"], ["propset"]) for e in got["events"]))
            fm.configure(root)
            check("A2: genuine absent directory properties return an empty mapping", fm.svn_local_properties(".") == {})
            value = "a pattern with spaces\n--literal-pattern\n"
            command(root, "svn", "propset", "--", "svn:ignore", value, "docs/work-tracker")
            out, err = io.StringIO(), io.StringIO()
            with redirect_stdout(out), redirect_stderr(err):
                code = fm.svn_ignore_board()
            expected = value + "index.html\nview\n"
            try:
                read_ = fm.svn_local_properties("docs/work-tracker").get("svn:ignore") if code == 0 else None
            except fm.SvnUnreadable as e:
                read_ = f"<unreadable: {e}>"
            check(f"A2: ignore setup preserves raw existing patterns/newlines (saw {code}, stderr {err.getvalue()[:300]!r}; svn:ignore {read_!r})",
                  code == 0 and read_ == expected)
            # Local option/peg-like paths stay literal rather than options or remote revision selectors.
            for name in ("-local", "peg@HEAD"):
                (root / name).mkdir()
                command(root, "svn", "add", "./" + name + "@")
                check(f"A2: local property target is literal ({name})", fm.svn_local_properties(name) == {})
            for rel in ("../escape", "/absolute", "https://example.invalid/repo", "C:/foreign", ".svn"):
                with patch.object(fm, "svn_run") as query:
                    try:
                        fm.svn_local_properties(rel); refused = False
                    except fm.SvnUnreadable:
                        refused = True
                    check(f"A2: foreign/ambiguous/admin target refuses before query ({rel})", refused and not query.called)
            linked = root / "linked"; linked.symlink_to(roots["foreign"], target_is_directory=True)
            with patch.object(fm, "svn_run") as query:
                try:
                    fm.svn_local_properties("linked"); refused = False
                except fm.SvnUnreadable:
                    refused = True
                check("A2: symlink property target refuses before query", refused and not query.called)
            original = fm.svn_run
            invalid_properties = [None, ET.fromstring("<info/>"), ET.fromstring('<properties><target path="foreign"/></properties>'),
                                  ET.fromstring('<properties><target path="."><property name="p">one</property><property name="p">two</property></target></properties>'),
                                  ET.fromstring('<properties><target path="."><property>unnamed</property></target></properties>'),
                                  ET.fromstring('<properties><target path="."><property name="p" encoding="unknown">value</property></target></properties>')]
            for n, bad in enumerate(invalid_properties):
                def read(*args, xml=False, answers=()):
                    return bad if args[0] == "proplist" else original(*args, xml=xml, answers=answers)
                with patch.object(fm, "svn_run", side_effect=read):
                    try:
                        fm.svn_local_properties("."); refused = False
                    except fm.SvnUnreadable:
                        refused = True
                    check(f"A2: malformed/mismatched property snapshot refuses {n}", refused)
            with patch.object(fm, "svn_run", return_value=ET.fromstring(f'<info><entry kind="dir" path="."><wc-info><wcroot-abspath>{roots["foreign"]}</wcroot-abspath><schedule>normal</schedule></wc-info></entry></info>')) as query:
                try:
                    fm.svn_local_properties("."); refused = False
                except fm.SvnUnreadable:
                    refused = True
                check("A2: foreign working-copy binding refuses before property read", refused and query.call_count == 1)
            for shape in ("missing-path", "missing-root", "relative-root", "duplicate-entry"):
                bad = ET.fromstring(ET.tostring(original("info", "./.@", xml=True)))
                entry = bad.find("entry")
                if shape == "missing-path":
                    del entry.attrib["path"]
                elif shape == "missing-root":
                    entry.find("wc-info").remove(entry.find("wc-info/wcroot-abspath"))
                elif shape == "relative-root":
                    entry.find("wc-info/wcroot-abspath").text = "."
                else:
                    bad.append(ET.fromstring(ET.tostring(entry)))
                with patch.object(fm, "svn_run", return_value=bad) as query:
                    try:
                        fm.svn_local_properties("."); refused = False
                    except fm.SvnUnreadable:
                        refused = True
                    check(f"A2: incomplete local binding refuses before property read ({shape})", refused and query.call_count == 1)
            for name, fault in (("info-fail", "info"), ("add-fail", "add"), ("propset-fail", "propset")):
                got = measured(roots[name], search, "setup:init:" + fault)
                check(f"A2: actual init path propagates injected {fault} failure", got["code"] == 4 and "already initialised" not in got["out"] and "failed" in got["err"] if fault != "info" else got["code"] == 4 and "nothing is written" in got["err"] and not (roots[name] / "shoalmark.toml").exists())
                if fault != "info":
                    check(f"A2: partial init is explicit after legitimate writes ({fault})", (roots[name] / "shoalmark.toml").exists() and "earlier" in got["err"] and "did not complete" in got["err"])
            install = roots["install"]
            got = measured(install, search, "setup:install")
            fm.configure(install)
            props = fm.svn_local_properties(".")
            check("A2: actual no-Git/server-free property install retains generated format", got["code"] == 0 and got["git_absent"] and props == {prop: f"python %REPOROOT%/tools/shoalmark/shoalmark.py --tsvn-hook {kind}\ntrue\nhide\n" for prop, kind in fm.TSVN_HOOKS.items()})
            got = measured(install, search, "setup:install")
            check("A2: repeat installed properties perform no mutation", got["code"] == 0 and not any(e[0] == "subprocess.Popen" and e[2][1:2] in (["add"], ["propset"]) for e in got["events"]))
            for name, fault in (("install-info-fail", "info"), ("install-proplist-fail", "proplist"), ("install-propset-fail", "propset")):
                got = measured(roots[name], search, "setup:install:" + fault)
                check(f"A2: actual install path refuses injected {fault} failure", got["code"] == 4 and "no successful installation is claimed" in got["err"])
                fm.configure(roots[name])
                check(f"A2: failed initial install does not invent installed properties ({fault})", fm.svn_local_properties(".") == {})
            command(install, "svn", "propset", "--", "tsvn:startcommithook", "another tool\ntrue\nhide\n", ".")
            got = measured(install, search, "setup:install")
            fm.configure(install)
            check("A2: existing non-shoalmark property is retained with refusal", got["code"] == 4 and fm.svn_local_properties(".")["tsvn:startcommithook"] == "another tool\ntrue\nhide\n" and "left alone" in got["err"])
            (install / "tools" / "shoalmark" / "shoalmark.py").unlink()
            got = measured(install, search, "setup:install")
            check("A2: missing consumer tool refuses before any property mutation", got["code"] == 4 and "vendor it before installing" in got["err"] and not any(e[0] == "subprocess.Popen" and e[2][1:2] == ["propset"] for e in got["events"]))
            broken = roots["bad-db"]
            (broken / ".svn" / "wc.db").write_bytes(b"not a working-copy database")
            got = measured(broken, search, "setup:init")
            check("A2: actual corrupt WC refuses init before the first scaffold byte", got["code"] == 4 and not (broken / "shoalmark.toml").exists() and not any(e[0] == "open" and not e[1].isdigit() for e in got["events"]))
    finally:
        fm.configure(previous)


def run_corrective_controls(fm, check):
    """RV-3089/3090/3091: malformed local evidence never grants permission to overwrite."""
    print("\nFM-044 A corrections: actual armed board and property-mutation observations")
    if not (shutil.which("svn") and shutil.which("svnadmin")):
        print("  SKIP A corrective real SVN fixtures: svn and svnadmin required")
        return
    with tempfile.TemporaryDirectory() as temp:
        base = Path(temp).resolve(); server = base / "server"; root = base / "wc"; foreign = base / "foreign"; search = base / "bin"
        command(base, "svnadmin", "create", str(server))
        command(base, "svn", "checkout", "-q", server.as_uri(), str(root))
        folder = corpus(root); (folder / "view").mkdir()
        (folder / "index.html").write_bytes(b"versioned page\n")
        (folder / "view" / "WORK-001.js").write_bytes(b"versioned view\n")
        command(root, "svn", "add", "shoalmark.toml", "work-tracker")
        command(root, "svn", "commit", "-qm", "immutable board fixture")
        command(base, "svn", "checkout", "-q", server.as_uri(), str(foreign))
        command(foreign, "svn", "delete", "work-tracker")
        command(foreign, "svn", "commit", "-qm", "foreign WC has no versioned board")
        (foreign / "foreign-marker").write_bytes(b"foreign status marker\n")
        (root / "a" / "b").mkdir(parents=True); (foreign / "x" / "y" / "z").mkdir(parents=True)
        (root / "a" / "b" / "escape").symlink_to(foreign / "x" / "y" / "z", target_is_directory=True)
        cwd = str(root / "a" / "b" / "escape") + "/../../.."
        # POSIX resolves `..` after the link, so this spelling of the root reaches the foreign copy; Windows resolves `..` by name first, and it
        # stays a spelling of the root. The refusal below is of the spelling, so it holds on both; only the resolution is POSIX's (PR #173).
        assert os.path.abspath(cwd) == str(root) and (os.name == "nt" or Path(cwd).resolve() == foreign)
        svn_only(search)
        setup = base / "setup"; command(base, "svn", "checkout", "-q", server.as_uri(), str(setup))
        source = setup / "tools" / "shoalmark" / "shoalmark.py"; source.parent.mkdir(parents=True); source.write_bytes((HERE / "shoalmark.py").read_bytes())
        server.rename(base / "server-unavailable")
        baseline = board_snapshot(folder)
        def run(target=root, **fault):
            return measured(target, search, "corrective:" + json.dumps(fault))
        def restore():
            for rel in set(board_snapshot(folder)) - set(baseline):
                (folder / rel).unlink()
            for rel, data in baseline.items():
                (folder / rel).write_bytes(data)
        got = run()
        check("RV-3089: positive exact configured cwd preserves versioned board bytes", got["code"] == 0 and board_snapshot(folder) == baseline and len(got["completed"]) == 1 and got["completed"][0][2] == str(root) and got["git_absent"])
        got = run(cwd=cwd)
        check("RV-3089: symlink-parent cwd refuses before child completion and board writes", got["code"] == 4 and not got["completed"] and not any(e[0] == "open" for e in got["events"]) and board_snapshot(folder) == baseline)
        restore()
        template = '<status><target path="."><entry path="."><wc-status item="normal" props="none"/></entry>{}</target></status>'
        node = '<entry path="work-tracker/index.html">{}</entry>'
        status_cases = {
            "contradictory singleton": template.format(node.format('<wc-status item="unversioned" props="none"/><wc-status item="normal" props="none"/>')),
            "unknown props": template.format(node.format('<wc-status item="unversioned" props="malformed"/>')),
            "unknown item": template.format(node.format('<wc-status item="future" props="none"/>')),
            "unknown boolean": template.format(node.format('<wc-status item="unversioned" props="none" copied="maybe"/>')),
            "unknown switched boolean": template.format(node.format('<wc-status item="unversioned" props="none" switched="maybe"/>')),
            "unknown conflict boolean": template.format(node.format('<wc-status item="unversioned" props="none" tree-conflicted="maybe"/>')),
            "status structural text": template.format(node.format('lost metadata<wc-status item="unversioned" props="none"/>')),
            "nested status": template.format(node.format('<wrapper><wc-status item="unversioned" props="none"/></wrapper>')),
            "unexpected target node": template.format('<wrapper>' + node.format('<wc-status item="unversioned" props="none"/>') + '</wrapper>'),
            "status tail text": template.format(node.format('<wc-status item="unversioned" props="none"/>lost metadata')),
        }
        for label, xml in status_cases.items():
            got = run(xml_command="status", xml=xml)
            check(f"RV-3090: {label} refuses through board_run before writes", got["code"] == 4 and "metadata could not be read" in got["err"] and not any(e[0] == "open" for e in got["events"]) and board_snapshot(folder) == baseline)
            restore()
        # Healthy SVN groups changelist entries outside target; these still protect actual versioned bytes.
        command(root, "svn", "changelist", "board", "work-tracker/index.html", "work-tracker/view/WORK-001.js")
        got = run()
        check("RV-3090: real changelist inventory preserves both versioned board files", got["code"] == 0 and board_snapshot(folder) == baseline and len(got["completed"]) == 1)
        command(root, "svn", "changelist", "--remove", "work-tracker/index.html", "work-tracker/view/WORK-001.js")
        info = ET.fromstring(command(setup, "svn", "info", "./.@", "--xml").stdout)
        info_cases = {}
        for label in ("duplicate wc-info", "duplicate root", "duplicate schedule", "binding text", "binding tail"):
            bad = ET.fromstring(ET.tostring(info)); wc = bad.find("entry/wc-info")
            if label == "duplicate wc-info":
                bad.find("entry").append(ET.fromstring(ET.tostring(wc)))
            elif label == "duplicate root":
                ET.SubElement(wc, "wcroot-abspath").text = str(foreign)
            elif label == "duplicate schedule":
                ET.SubElement(wc, "schedule").text = "delete"
            elif label == "binding text":
                wc.text = "lost binding data"
            else:
                wc.find("schedule").tail = "lost binding data"
            info_cases[label] = ET.tostring(bad).decode()
        for label, xml in info_cases.items():
            got = run(setup, mode="properties", xml_command="info", xml=xml)
            check(f"RV-3091: {label} refuses before proplist or mutation", got["code"] == 4 and not got["completed"] and not any(e[0] == "open" for e in got["events"]))
            for prop in fm.TSVN_HOOKS:
                command(setup, "svn", "propdel", "--", prop, ".")
            got = run(setup, mode="install", xml_command="info", xml=xml)
            check(f"RV-3091: install rejects {label} before first actual mutation", got["code"] == 4 and not any(e[0] == "subprocess.Popen" and e[2][1:2] in (["propset"], ["add"], ["proplist"]) for e in got["events"]))
        property_cases = {
            "nonempty empty-container text": '<properties>lost property data</properties>',
            "nonempty target text": '<properties><target path=".">lost property data</target></properties>',
            "target tail text": '<properties><target path="."/>lost property data</properties>',
            "property tail text": '<properties><target path="."><property name="x">raw value</property>lost property data</target></properties>',
        }
        for label, xml in property_cases.items():
            got = run(setup, mode="properties", xml_command="proplist", xml=xml)
            check(f"RV-3091: {label} refuses instead of declaring absence", got["code"] == 4 and not any(e[0] == "open" for e in got["events"]))
            for prop in fm.TSVN_HOOKS:
                command(setup, "svn", "propdel", "--", prop, ".")
            got = run(setup, mode="install", xml_command="proplist", xml=xml)
            check(f"RV-3091: install rejects {label} before property mutation", got["code"] == 4 and not any(e[0] == "subprocess.Popen" and e[2][1:2] in (["propset"], ["add"]) for e in got["events"]))
        previous = fm.ROOT
        try:
            fm.configure(setup)
            original = fm.svn_run
            def formatted(*args, **kwargs):
                return ET.fromstring('<properties>\n <target path=".">\n <property name="raw">  raw\n\nvalue  </property>\n </target>\n</properties>') if args[0] == "proplist" else original(*args, **kwargs)
            with patch.object(fm, "svn_run", side_effect=formatted):
                check("RV-3091: formatting whitespace preserves exact raw value text", fm.svn_local_properties(".") == {"raw": "  raw\n\nvalue  "})
        finally:
            fm.configure(previous)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--probe":
        probe(Path(sys.argv[2]), sys.argv[3])
    else:
        failures, count = [], [0]
        def check(label, condition):
            count[0] += 1
            print(f"  {'ok  ' if condition else 'FAIL'} {label}")
            if not condition:
                failures.append(label)
        started = time.monotonic()
        run_shared_controls(load_tool(), check)
        print(f"\n{count[0] - len(failures)}/{count[0]} shared controls passed in {time.monotonic() - started:.3f}s")
        raise SystemExit(bool(failures))
