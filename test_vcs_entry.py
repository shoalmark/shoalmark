"""Proposed local SVN entry controls, using actual __main__ invocations.

The ordinary runner uses current payloads. An explicit development baseline
can compare immutable-before output; it is never fetched by the tests.
There are no handler, VCS result, history-reader or authority substitutions.
Local file:// authors are fixture strings, never authenticated identities.
"""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import runpy
import shlex
import shutil
import subprocess
import sys
import tempfile
import time
import traceback

HERE = Path(__file__).resolve().parent
LIMIT = "Subversion: this local run cannot verify commit signatures or server-authenticated authors; protected SVN acceptance remains held."
MARKER = "__ENTRY_OBSERVATION__"
STATUS = ["svn", "status", "--verbose", "--no-ignore", "--ignore-externals", "--depth", "infinity", ".", "--xml"]
TOOL_FILES = ("VERSION", "NOTICE", "LICENSE-APACHE", "LICENSE-MIT", "CHANGELOG.md", "README.md", "vendor/marked-18.0.13.umd.js")


def actual_entry(spec):
    """Observe product calls without replacing a handler or a process result."""
    tool = str(Path(spec["tool"]).resolve())
    events, phases, bindings, main_calls, returns, normalized = [], [], [], [], [], []
    active = [True]
    # Import descriptor helpers before the product can arm its import tripwire.
    if sys.platform == "darwin":
        import fcntl
    elif os.name == "nt":
        import ctypes
        import msvcrt
        final_path = ctypes.windll.kernel32.GetFinalPathNameByHandleW
        final_path.argtypes = [ctypes.c_void_p, ctypes.c_wchar_p, ctypes.c_uint, ctypes.c_uint]
        final_path.restype = ctypes.c_uint
    def path(raw):
        if isinstance(raw, (str, bytes, os.PathLike)):
            return os.path.abspath(os.fsdecode(raw))
        if isinstance(raw, int):
            try:
                if sys.platform == "darwin":
                    return os.fsdecode(fcntl.fcntl(raw, 50, b"\0" * 1024)).split("\0", 1)[0]
                if os.name == "nt":
                    buffer = ctypes.create_unicode_buffer(32768)
                    length = final_path(msvcrt.get_osfhandle(raw), buffer, len(buffer), 0)
                    if 0 < length < len(buffer):
                        return buffer.value.removeprefix("\\\\?\\")
                else:
                    return os.readlink("/proc/self/fd/" + str(raw))
            except (OSError, ValueError):
                pass
        return "<fd:%s>" % raw
    def audit(event, args):
        if not active[0]:
            return
        if event == "subprocess.Popen":
            argv = list(map(str, args[1])) if isinstance(args[1], (list, tuple)) else [str(args[1])]
            stack = [f.name for f in traceback.extract_stack() if f.filename == tool]
            environment = dict(os.environ if args[3] is None else args[3])
            frame = sys._getframe()
            while frame and not (frame.f_code.co_name == "run" and frame.f_globals.get("__name__") == "subprocess"):
                frame = frame.f_back
            options = dict(frame.f_locals["kwargs"]) if frame else {}
            options.pop("cwd", None); options.pop("env", None)
            events.append({"event": event, "argv": argv, "cwd": path(args[2]) if args[2] is not None else os.getcwd(), "stack": stack,
                           "env_mode": "inherited" if args[3] is None else "explicit",
                           "environment_sha256": hashlib.sha256(json.dumps(environment, sort_keys=True).encode()).hexdigest(),
                           "options": options})
        elif event == "open":
            mode, flags = args[1:3]
            write = (isinstance(mode, str) and any(c in mode for c in "wax+")) or (isinstance(flags, int) and bool(flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND)))
            names = [f.name for f in traceback.extract_stack()] if write else []
            events.append({"event": event, "path": path(args[0]), "write": write,
                           "tempdir_discovery": "_get_default_tempdir" in names and "arm_tripwire" in names})
        elif event in ("os.mkdir", "os.remove", "os.rmdir", "os.rename", "os.symlink", "os.link", "os.chmod", "os.truncate"):
            names = [f.name for f in traceback.extract_stack()]
            destinations = [args[1]] if event == "os.symlink" else list(args[:2]) if event in ("os.rename", "os.link") else [args[0]]
            for destination in destinations:
                events.append({"event": event, "path": path(destination), "write": True,
                               "tempdir_discovery": "_get_default_tempdir" in names and "arm_tripwire" in names})
        elif event.startswith("socket.") or event in ("os.system", "os.exec", "os.spawn", "os.posix_spawn", "webbrowser.open"):
            events.append({"event": event, "alternate_process_or_network": True})
    def profile(frame, event, argument):
        if frame.f_code.co_filename != tool:
            return
        name = frame.f_code.co_name
        if event == "call":
            if name == "main":
                main_calls.append({"argv": frame.f_locals.get("argv"), "notice": frame.f_locals.get("_notice")})
            if name in ("load_trackers", "run_deriver", "lint", "board_run", "svn_last_worked_on", "ship_problems"):
                phases.append({"function": name, "root": str(frame.f_globals.get("ROOT")), "requested_root": str(frame.f_locals.get("root"))})
        elif event == "return":
            if name == "configure":
                bindings.append({"root": str(frame.f_globals.get("ROOT")), "backend": [str(x) for x in (frame.f_globals.get("_VCS") or ())]})
            elif name == "tsvn_arguments":
                normalized.append(argument if isinstance(argument, list) else None)
            elif name == "main":
                returns.append({"code": argument, "root": str(frame.f_globals.get("ROOT"))})
    sys.addaudithook(audit); sys.setprofile(profile)
    sys.argv = [tool, *spec["argv"]]
    code, exception = 0, None
    try:
        runpy.run_path(tool, run_name="__main__")
    except SystemExit as error:
        code = error.code or 0
    except BaseException as error:
        code = 90; exception = {"type": type(error).__name__, "detail": str(error)}
        traceback.print_exc()
    finally:
        sys.setprofile(None); active[0] = False
        print(MARKER + json.dumps({"events": events, "phases": phases, "bindings": bindings,
              "main_calls": main_calls, "main_returns": returns, "normalized": normalized,
              "exception": exception, "git_absent": shutil.which("git") is None}), file=sys.stderr)
    raise SystemExit(code)


def command(root, *argv):
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull, GIT_AUTHOR_NAME="fixture-only",
               GIT_AUTHOR_EMAIL="fixture@example.invalid", GIT_COMMITTER_NAME="fixture-only",
               GIT_COMMITTER_EMAIL="fixture@example.invalid", GIT_AUTHOR_DATE="2026-10-13T00:00:00+00:00",
               GIT_COMMITTER_DATE="2026-10-13T00:00:00+00:00")
    return subprocess.run(list(argv), cwd=root, env=env, capture_output=True, text=True, encoding="utf-8", check=True, timeout=30).stdout


def snapshot(root):
    return {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in root.rglob("*") if p.is_file() and not p.is_symlink() and not any(x in (".svn", ".git") for x in p.relative_to(root).parts)}


def corpus(root):
    (root / "shoalmark.toml").write_text('name = "entry fixture"\ntracker_dir = "work-tracker"\n[kinds]\nWORK = "Work"\n', encoding="utf-8")
    folder = root / "work-tracker"; folder.mkdir()
    (folder / "WORK-001-local.md").write_text('---\nid: WORK-001\nstatus: Proposed\nconsidered: none\nhook: "local entry fixture"\n---\n\n# WORK-001 — local\n\n## What is true now\n\nPrepare the local entry behavior.\n\n## Done when\n\nLocal output can be read.\n', encoding="utf-8")
    (folder / "TRIAGE.md").write_text('# Triage\n\n## The intent\n\nRead local records.\n\n## The current path\n\nPrepare local entry behavior.\n', encoding="utf-8")
    (root / "documents").mkdir()
    (root / "documents" / "O'Neil & ü.txt").write_text("local affected data\n", encoding="utf-8")


def tool_copy(root, source, payload):
    target = root / "tools" / "shoalmark"; target.mkdir(parents=True, exist_ok=True)
    for rel in TOOL_FILES:
        path = target / rel; path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(payload / rel, path)
    tool = target / "shoalmark.py"; tool.write_bytes(Path(source).read_bytes())
    files = ["shoalmark.py", *TOOL_FILES]
    (target / "PIN").write_text("".join(hashlib.sha256((target / rel).read_bytes().replace(b"\r\n", b"\n")).hexdigest() + "  " + rel + "\n" for rel in files), encoding="utf-8")
    return tool


def svn_search(folder, svn):
    folder.mkdir()
    executable = folder / Path(svn).name
    try:
        executable.symlink_to(svn)
    except OSError:
        shutil.copy2(svn, executable)
        # Windows copies need their runtime DLLs, never another VCS executable.
        for dll in Path(svn).parent.glob("*.dll"):
            shutil.copy2(dll, folder / dll.name)
    assert shutil.which("svn", path=str(folder))
    assert shutil.which("git", path=str(folder)) is None
    return folder


def invoke(tool, root, argv, cwd, search=None):
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update(PYTHONDONTWRITEBYTECODE="1", GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull)
    if search is not None:
        env["PATH"] = str(search)
    spec = {"tool": str(tool), "argv": argv}
    before = snapshot(root)
    done = subprocess.run([sys.executable, "-B", str(Path(__file__).resolve()), "--entry-probe", json.dumps(spec)],
                          cwd=cwd, env=env, capture_output=True, text=True, encoding="utf-8", timeout=40)
    lines = done.stderr.splitlines(keepends=True)
    marker = [line[len(MARKER):] for line in lines if line.startswith(MARKER)]
    if len(marker) != 1:
        raise AssertionError("actual entry observer did not complete: " + done.stderr[-1200:])
    observed = json.loads(marker[0]); err = "".join(line for line in lines if not line.startswith(MARKER))
    after = snapshot(root)
    observed.update(code=done.returncode, out=done.stdout, err=err, argv=argv, tool=str(tool), root=str(root), invocation_cwd=str(cwd),
                    changed=[p for p in sorted(set(before) | set(after)) if before.get(p) != after.get(p)],
                    notice_count=(done.stdout + err).count(LIMIT), source_sha256=hashlib.sha256(Path(tool).read_bytes()).hexdigest())
    return observed


def run_entry_controls(source, check, baseline=None, report_path=None, payload=None):
    """Portable proposed runner; P supplies production source and aggregate wiring later."""
    source = Path(getattr(source, "__file__", source)).resolve()
    baseline = Path(baseline).resolve() if baseline is not None else None
    payload = Path(payload).resolve() if payload is not None else source.parent
    if not all((payload / rel).is_file() for rel in TOOL_FILES):
        raise RuntimeError("entry controls need the current repository tool payload directory")
    if not all(shutil.which(x) for x in ("git", "svn", "svnadmin")):
        raise RuntimeError("entry qualification requires real git, svn and svnadmin")
    started = time.monotonic(); observations = []; setup_observations = []
    with tempfile.TemporaryDirectory(prefix="fm044-local-entry-") as temp:
        base = Path(temp).resolve(); cwd = base / "unrelated"; cwd.mkdir()
        search = svn_search(base / "svn-only", shutil.which("svn"))
        server = base / "server"; seed = base / "seed"
        command(base, "svnadmin", "create", str(server)); command(base, "svn", "checkout", "-q", server.as_uri(), str(seed))
        corpus(seed); command(seed, "svn", "add", "shoalmark.toml", "work-tracker", "documents")
        command(seed, "svn", "commit", "-qm", "untrusted local fixture string", "--username", "fixture-only")
        number = [0]
        def fresh(name, chosen=source):
            number[0] += 1; root = base / ("wc-%02d-%s" % (number[0], name))
            command(base, "svn", "checkout", "-q", server.as_uri(), str(root))
            return root, tool_copy(root, chosen, payload)
        def run(name, root, tool, flags, offline=True, raw=False):
            argv = flags if raw else ["--root", str(root), *flags]
            absent = base / "server-unavailable"
            if offline:
                server.rename(absent)
            try:
                got = invoke(tool, root, argv, cwd, search)
            finally:
                if offline:
                    absent.rename(server)
            got.update(case=name, server_available=not offline, backend="svn")
            observations.append(got)
            return got
        def checks(name, got, code=0, readonly=False, local=False):
            check("entry: " + name + " emits the complete verification limit exactly once", got["notice_count"] == 1)
            check("entry: " + name + " has its deliberate result and no exception", got["code"] == code and got["exception"] is None)
            processes = [e for e in got["events"] if e["event"] == "subprocess.Popen"]
            check("entry: " + name + " attempts no Git or alternate network/process API", got["git_absent"] and all(e["argv"][0] == "svn" for e in processes) and not any(e.get("alternate_process_or_network") for e in got["events"]))
            def correct_cwd(event):
                if event["argv"] == ["svn", "log", "-v", "--xml", str(Path(got["root"]) / "work-tracker")] and "svn_last_worked_on" in event["stack"]:
                    return event["cwd"] == got["invocation_cwd"] and got["server_available"]
                return event["cwd"] == got["root"]
            # Invalid Tortoise argv is deliberately refused before consumer binding.
            bound = got["bindings"] and got["bindings"][-1]["root"] == got["root"]
            refused_before_binding = name == "tsvn-binding-refusal" and got["code"] == 4 and not processes and not got["phases"] and got["normalized"] == [None]
            check("entry: " + name + " keeps local query cwd and required consumer binding", all(correct_cwd(e) for e in processes) and all(p["root"] == got["root"] or (p["function"] == "board_run" and p["requested_root"] == got["root"]) for p in got["phases"]) and (bound or refused_before_binding))
            probes = [e for e in got["events"] if e.get("write") and e.get("tempdir_discovery")]
            check("entry: " + name + " retains only paired stdlib tempdir probes before tripwire", not probes or (len(probes) == 2 and [e["event"] for e in probes] == ["open", "os.remove"] and probes[0]["path"] == probes[1]["path"] and not Path(probes[0]["path"]).exists()))
            writes = [e for e in got["events"] if e.get("write") and not e.get("tempdir_discovery")]
            check("entry: " + name + " writes only inside its consumer", all(e["path"] == got["root"] or e["path"].startswith(got["root"] + os.sep) for e in writes) and not any(p.startswith("tools/") for p in got["changed"]))
            if readonly:
                check("entry: " + name + " changes no consumer byte or Python write", not got["changed"] and not writes)
            if local:
                check("entry: " + name + " uses no history/server command", not got["server_available"] and all(len(e["argv"]) > 1 and e["argv"][1] in ("status", "info", "proplist", "propset", "add") for e in processes))
            return processes

        for name, flags, code in (("schema", ["--schema"], 0), ("session-new", ["--session", "new"], 0),
                                   ("unsupported-whoami", ["--whoami"], 4), ("unsupported-queue", ["--queue"], 3),
                                   ("unsupported-ratio", ["--ratio"], 2)):
            root, tool = fresh(name); got = run(name, root, tool, flags)
            processes = checks(name, got, code, readonly=True, local=True)
            check("entry: " + name + " makes zero child-process attempts", not processes)
            if name.startswith("unsupported"):
                check("entry: " + name + " refuses before tracker consumers", not got["phases"])
            if name == "session-new":
                check("entry: session-new preserves its eight-hex-token stdout", re.fullmatch(r"[0-9a-f]{8}\n", got["out"]) is not None)

        root, tool = fresh("board"); got = run("board", root, tool, ["--html-only"])
        processes = checks("board", got, local=True)
        check("entry: board uses exactly its allowed local status tuple", [e["argv"] for e in processes] == [STATUS])
        check("entry: board writes its page/views and no canonical or Git-basis record", "work-tracker/index.html" in got["changed"] and "work-tracker/view/WORK-001.js" in got["changed"] and "work-tracker/view/built.json" not in got["changed"] and all(p == "work-tracker/index.html" or p.startswith("work-tracker/view/") for p in got["changed"]))

        root, tool = fresh("damaged-board"); (root / ".svn" / "wc.db").write_bytes(b"broken WC metadata")
        got = run("damaged-board", root, tool, ["--html-only"]); checks("damaged-board", got, 4, readonly=True, local=True)

        root, tool = fresh("init")
        shutil.rmtree(root / "work-tracker"); (root / "shoalmark.toml").unlink()
        got = run("init", root, tool, ["--init"]); checks("init", got, local=True)
        check("entry: init really scaffolds the local contract", (root / "AGENTS.md").exists() and any(p.endswith("TRIAGE.md") for p in got["changed"]))

        root, tool = fresh("install"); got = run("install", root, tool, ["--install-hook"])
        processes = checks("install", got, local=True)
        check("entry: install really sets local properties without changing tracker bytes", any(e["argv"][1] == "propset" for e in processes) and not got["changed"])
        properties = {kind: command(root, "svn", "propget", "--strict", prop, ".")
                      for kind, prop in (("start", "tsvn:startcommithook"), ("pre", "tsvn:precommithook"))}
        check("entry: installed Tortoise properties retain command/true/hide format", all(value.splitlines()[1:] == ["true", "hide"] and value.endswith("\n") for value in properties.values()))
        paths, message = base / "paths.txt", base / "message.txt"
        paths.write_text(str(root / "documents" / "O'Neil & ü.txt") + "\n", encoding="utf-8")
        message.write_text("Keep this message exactly unchanged.\n", encoding="utf-8")
        message_bytes = message.read_bytes()
        for kind in ("start", "pre"):
            words = shlex.split(properties[kind].splitlines()[0])
            installed_tool = Path(words[1].replace("%REPOROOT%", str(root)))
            check("entry: installed " + kind + " command names the actual local source and handler", words[0] == "python" and installed_tool == tool and words[2:] == ["--tsvn-hook", kind])
            appended = [str(paths), str(message), str(root)] if kind == "start" else [str(paths), "3", str(message), str(root)]
            got = run("installed-tsvn-" + kind, root, installed_tool, words[2:] + appended, offline=False, raw=True)
            checks("installed-tsvn-" + kind, got, readonly=kind == "pre")
            check("entry: installed " + kind + " binds exact consumer before phases", got["normalized"] == [["--root", str(root)] + (["--check"] if kind == "pre" else [])] and all(p["root"] == str(root) for p in got["phases"]))
            check("entry: installed " + kind + " never reads or changes the message", not any(e.get("path") == str(message) for e in got["events"]) and message.read_bytes() == message_bytes)
        bad = run("tsvn-binding-refusal", root, tool, ["--tsvn-hook", "pre", str(paths), "invalid", str(message), str(root)], raw=True)
        checks("tsvn-binding-refusal", bad, 4, readonly=True, local=True)
        check("entry: invalid Tortoise binding precedes all processes and tracker handlers", not any(e["event"] == "subprocess.Popen" for e in bad["events"]) and not bad["phases"])

        root, tool = fresh("new"); got = run("new", root, tool, ["--new", "WORK", "another local product issue", "--tags", "bug"])
        checks("new", got, local=True)
        check("entry: new really files one additional local record", len(got["changed"]) == 1 and got["changed"][0].startswith("work-tracker/WORK-002-"))

        root, tool = fresh("index"); got = run("index", root, tool, [], offline=False); checks("index", got)
        check("entry: index really generates INDEX and board", "work-tracker/INDEX.md" in got["changed"] and "work-tracker/index.html" in got["changed"])
        got = run("check", root, tool, ["--check"], offline=False); checks("check", got, readonly=True)

        root, tool = fresh("triage"); got = run("triage-worksheet", root, tool, ["--triage"], offline=False); checks("triage-worksheet", got)
        sheet = root / "work-tracker" / "evidence" / "triage" / ("triage-" + datetime.date.today().isoformat() + ".md")
        rows = sheet.read_text(encoding="utf-8").splitlines(keepends=True); filled = False
        for n, row in enumerate(rows):
            if row.startswith("|") and "WORK-001" in row and "[WORK-001]" in row:
                cells = row.rstrip("\n").split("|"); cells[-3] = " keep P2 #1 build "; cells[-2] = " bounded local worksheet fixture "
                rows[n] = "|".join(cells) + "\n"; filled = True; break
        check("entry: recursive triage fixture fills a real generated worksheet row", filled)
        sheet.write_text("".join(rows), encoding="utf-8")
        got = run("triage-applied-refresh", root, tool, ["--triage"], offline=False); checks("triage-applied-refresh", got)
        record = (root / "work-tracker" / "WORK-001-local.md").read_text(encoding="utf-8")
        check("entry: triage actually applies its verdict and refreshes INDEX", "triaged: " in record and "rank: 1" in record and "work-tracker/INDEX.md" in got["changed"])
        check("entry: recursive triage is one public invocation with a silent inner notice", len(got["main_calls"]) == 2 and [r["notice"] for r in got["main_calls"]] == [True, False])

        # Git output comparison uses identical consumer paths and no production substitutions.
        groot = base / "git-consumer"; groot.mkdir(); command(groot, "git", "init", "-q", "--initial-branch=main"); corpus(groot)
        command(groot, "git", "config", "user.name", "fixture-only"); command(groot, "git", "config", "user.email", "fixture@example.invalid")
        command(groot, "git", "add", "shoalmark.toml", "work-tracker", "documents")
        command(groot, "git", "-c", "core.hooksPath=/dev/null", "-c", "commit.gpgsign=false", "commit", "-qm", "WORK-001 local fixture")
        for name, flags in (("schema", ["--schema"]), ("new", ["--new", "WORK", "another local product issue", "--tags", "bug"]),
                            ("index", []), ("board", ["--html-only"]), ("check", ["--check"]), ("triage", ["--triage"]),
                            ("session-new", ["--session", "new"])):
            pair = []
            for chosen in ((baseline, source) if baseline is not None else (source,)):
                command(groot, "git", "restore", "--worktree", "work-tracker", "shoalmark.toml")
                for p in list((groot / "work-tracker").iterdir()):
                    if p.name not in ("WORK-001-local.md", "TRIAGE.md"):
                        shutil.rmtree(p) if p.is_dir() else p.unlink()
                tool = tool_copy(groot, chosen, payload)
                if name == "check":
                    setup_observations.append(invoke(tool, groot, ["--root", str(groot)], cwd))
                got = invoke(tool, groot, ["--root", str(groot), *flags], cwd); got.update(case="Git-" + name, backend="git", variant="before" if baseline is not None and chosen == baseline else "candidate")
                observations.append(got); pair.append(got)
            current = pair[-1]
            if name == "schema":
                behavior = "| Key | Value | Written by | Says |" in current["out"] and "`id:`" in current["out"] and "`triaged:`" in current["out"] and not current["changed"]
            elif name == "new":
                behavior = len(current["changed"]) == 1 and current["changed"][0].startswith("work-tracker/WORK-002-") and "wrote " + current["changed"][0] in current["out"]
            elif name in ("index", "board"):
                behavior = "work-tracker/index.html" in current["changed"] and "work-tracker/view/WORK-001.js" in current["changed"] and "board: " in current["out"] and (name != "index" or "work-tracker/INDEX.md" in current["changed"])
            elif name == "check":
                behavior = "work-tracker/INDEX.md is up to date" in current["out"] and not current["changed"]
            elif name == "triage":
                behavior = len(current["changed"]) == 1 and current["changed"][0].startswith("work-tracker/evidence/triage/") and "Worksheet:" in current["out"]
            else:
                behavior = re.fullmatch(r"[0-9a-f]{8}\n", current["out"]) is not None and not current["changed"]
            check("entry: Git " + name + " keeps its actual output/write contract", current["code"] == 0 and not current["err"] and current["exception"] is None and behavior)
            check("entry: Git " + name + " emits no SVN limitation or SVN start", all(g["notice_count"] == 0 and all(e["argv"][0] == "git" for e in g["events"] if e["event"] == "subprocess.Popen") for g in pair))
            if baseline is not None:
                a, b = pair
                output_equal = (a["out"], a["err"], a["code"]) == (b["out"], b["err"], b["code"])
                if name == "session-new":
                    output_equal = a["code"] == b["code"] == 0 and not a["err"] and not b["err"] and all(re.fullmatch(r"[0-9a-f]{8}\n", g["out"]) for g in pair)
                check("entry: Git " + name + " output/result behavior equals explicit development baseline", output_equal)
    proof = {"kind": "outside local entry preparation, no protected/historical acceptance",
             "development_baseline": str(baseline) if baseline is not None else None, "payload": str(payload), "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
             "seconds": time.monotonic() - started, "observations": observations, "setup_observations": setup_observations}
    if report_path:
        Path(report_path).write_text(json.dumps(proof, indent=2) + "\n", encoding="utf-8")
    return proof


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--entry-probe":
        actual_entry(json.loads(sys.argv[2]))
    else:
        parser = argparse.ArgumentParser(description="Actual local CLI entry controls; no history is fetched by this runner")
        parser.add_argument("--source", type=Path, default=HERE / "shoalmark.py")
        parser.add_argument("--baseline", type=Path, help="optional explicit development comparison source")
        parser.add_argument("--payload", type=Path, help="current tool assets; defaults to source directory")
        parser.add_argument("--report", type=Path)
        args = parser.parse_args()
        rows = []
        def check(name, passed):
            rows.append({"name": name, "pass": bool(passed)}); print(("ok   " if passed else "FAIL ") + name, flush=True)
        proof = run_entry_controls(args.source, check, baseline=args.baseline, payload=args.payload)
        proof["checks"] = rows
        if args.report:
            args.report.write_text(json.dumps(proof, indent=2) + "\n", encoding="utf-8")
        print("%d/%d proposed entry controls passed in %.3fs" % (sum(c["pass"] for c in rows), len(rows), proof["seconds"]))
        raise SystemExit(not all(c["pass"] for c in rows))
