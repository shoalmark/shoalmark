"""FM-058: the signed run-bound classes, exercised at the program entry point.

Run directly with --mutants to prove the required regressions are caught.
Only a disposable tool's first configure call is replaced: the real startup,
argument classification and watchdog run before a child that outlasts the bound.
"""

import argparse
import builtins
import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
from unittest.mock import patch


HERE = Path(__file__).resolve().parent
STARTUP = 'WATCHDOG_MODE = watchdog_mode(sys.argv[1:]) if __name__ == "__main__" else None'
HOOK_LINE = ("shoalmark: the hook's run took longer than 1 s and was stopped — "
             "the commit is refused; SHOALMARK_BOARD_SECONDS gives it longer\n")
BOARD_LINE = "the board's run took longer than 1 s and was stopped\n"


def load_tool(source):
    spec = importlib.util.spec_from_file_location("bounds_tool", source)
    tool = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(tool)
    return tool


def classification_filesystem_calls(tool, argv, repository, copy):
    """RV-3370: watch resolved tool/repository paths from classification through watchdog arming."""
    roots = {tool.HERE.resolve(), tool.ROOT.resolve(), repository.resolve()}
    calls, resolving, armed = [], [False], [False]

    class Timer:
        def __init__(self, *args):
            pass

        def start(self):
            armed[0] = True

    def spy(original, label):
        def watched(path=".", *args, **kwargs):
            if not resolving[0] and isinstance(path, (str, bytes, os.PathLike)):
                resolving[0] = True
                try:
                    resolved = Path(os.fsdecode(path)).resolve()
                    for root in roots:
                        try:
                            resolved.relative_to(root)
                        except ValueError:
                            continue
                        calls.append((label, str(resolved)))
                        break
                finally:
                    resolving[0] = False
            return original(path, *args, **kwargs)
        return watched

    with contextlib.ExitStack() as stack:
        stack.enter_context(patch.object(tool, "HOOK_RUN", copy))
        stack.enter_context(patch.object(tool.threading, "Timer", Timer))
        for module, names in ((os, ("stat", "lstat", "scandir", "listdir", "open")),
                              (builtins, ("open",)), (io, ("open",)),
                              (Path, ("stat", "lstat", "exists", "is_dir", "is_file", "iterdir", "open"))):
            for name in names:
                original = getattr(module, name)
                stack.enter_context(patch.object(module, name, spy(original, module.__name__ + "." + name)))
        mode = tool.watchdog_mode(argv)
        if mode is not None:
            tool.board_watchdog(board=mode == "board")
            assert armed[0], "the filesystem spy must extend through watchdog arming"
    return calls


def board_spellings(tool):
    """RV-3371: derive every accepted --html-only prefix from this parser's own option names."""
    with patch.object(tool.argparse.ArgumentParser, "parse_args", lambda parser, argv: parser):
        parser = tool.parse_args([], classification_only=True)
    options = tuple(parser._option_string_actions)
    target = "--html-only"
    return [target[:length] for length in range(3, len(target) + 1)
            if [option for option in options if option.startswith(target[:length])] == [target]]


def run_controls(source, check, *, only=None):
    """FM-058's contract: real children, unchanged COPY classification, defaults and fail-safe cases."""
    tool = load_tool(source)
    source = Path(source).read_text(encoding="utf-8")
    anchor = "\nconfigure()\nSAFE_READS = False\n"
    assert source.count(anchor) == 1, "the first configure call must be instrumented exactly once"
    probe = '''
if __name__ == "__main__":
    subprocess.run([sys.executable, "-I", "-c", "import time; time.sleep(" + os.environ.get("FM058_TEST_WAIT", "0") + ")"],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(json.dumps({"seconds": BOARD_RUN_SECONDS, "copy": HOOK_RUN}))
    sys.exit(0)
configure()
SAFE_READS = False
'''
    with tempfile.TemporaryDirectory(prefix="fm058-bounds-") as directory:
        base = Path(directory)
        paths, message = base / "paths.txt", base / "message.txt"
        paths.write_text(str(base) + "\n", encoding="utf-8")
        message.write_text("FM-058\n", encoding="utf-8")
        tools = {}
        for kind in ("tree", "copy"):
            folder = base / kind
            folder.mkdir()
            tools[kind] = folder / "shoalmark.py"
            tools[kind].write_text(source.replace(anchor, "\n" + probe), encoding="utf-8")
            if kind == "copy":
                (folder / "COPY").write_text("{}\n", encoding="utf-8")
        env = {key: value for key, value in os.environ.items()
               if not key.startswith("GIT_") and key not in ("SHOALMARK_BOARD_SECONDS", "FM058_TEST_WAIT")}

        def launch(kind, argv, bounded=None, wait="0"):
            child_env = dict(env, FM058_TEST_WAIT=wait)
            if bounded is not None:
                child_env["SHOALMARK_BOARD_SECONDS"] = bounded
            started = time.monotonic()
            result = subprocess.run([sys.executable, "-I", str(tools[kind]), *argv], cwd=base,
                                    env=child_env, capture_output=True, text=True, encoding="utf-8", timeout=12)
            return result, time.monotonic() - started

        classes = (("copy", ["--session-check"], "hook"),
                   ("copy", ["--html-only"], "board"),
                   ("tree", ["--html-only"], "board"),
                   ("copy", ["--answer", "FM-058", "accept"], "person"),
                   ("tree", ["--answer", "FM-058", "accept"], "person"))
        for kind, argv, run in classes:
            if only is not None:
                continue
            calls = classification_filesystem_calls(tool, argv, base, kind == "copy")
            check("RV-3370 early pass: " + kind + " " + repr(argv) + " — " + repr(calls), not calls)
            result, _ = launch(kind, argv)
            expected = {"seconds": 60, "copy": kind == "copy"}
            check("FM-058 default: " + kind + " " + run + " reads 60 s without waiting",
                  result.returncode == 0 and not result.stderr and json.loads(result.stdout) == expected)

        # Person cases come first so the over-bounding mutant has a direct witness.
        waits = [("copy", ["--answer", "FM-058", "accept"], "person"),
                 ("tree", ["--answer", "FM-058", "accept"], "person"),
                 ("copy", ["--root", str(base), "--check"], "person"),
                 ("tree", ["--check"], "person"),
                 ("copy", ["--session-check"], "hook"),
                 ("copy", ["--session-trailer", "message", ""], "hook"),
                 ("copy", ["--commit-msg", "message"], "hook"),
                 ("copy", ["--print-written"], "hook"),
                 ("copy", ["--html-only"], "board"),
                 ("tree", ["--html-only"], "board"),
                 ("copy", ["--tsvn-hook", "pre"], "hook"),
                 ("copy", ["--answer", "FM-058", "accept", "--session-check"], "hook"),
                 ("copy", ["--check", "--print-written"], "hook"),
                 ("copy", ["--sess"], "hook"),
                 ("copy", ["--answer"], "hook"),
                 ("copy", ["--unknown"], "hook"),
                 ("copy", [], "hook")]
        for kind in ("tree", "copy"):
            waits.extend((kind, ["--tsvn-hook", *layout], "hook") for layout in (
                ["start", str(paths), str(message), str(base)],
                ["pre", str(paths), "3", str(message), str(base)]))
            for spelling in board_spellings(tool):
                case = (kind, [spelling], "board")
                if case not in waits:
                    waits.append(case)
        waits.extend(("tree", argv, run) for argv, run in (
            ([], "person"), (["--unknown"], "person"), (["--answer"], "person"),
            (["--session-check"], "hook"), (["--session-trailer", "message", ""], "hook"),
            (["--commit-msg", "message"], "hook"), (["--print-written"], "hook"),
            (["--answer", "FM-058", "accept", "--session-check"], "hook"),
            (["--check", "--html-o"], "board")))
        for kind, argv, run in waits:
            if only is not None and not only(kind, argv, run):
                continue
            calls = classification_filesystem_calls(tool, argv, base, kind == "copy")
            check("RV-3370 early pass: " + kind + " " + repr(argv) + " — " + repr(calls), not calls)
            result, elapsed = launch(kind, argv, bounded="1", wait="2")
            label = "FM-058 short bound: " + kind + " " + repr(argv)
            if run == "person":
                expected = {"seconds": 1, "copy": kind == "copy"}
                passed = (result.returncode == 0 and not result.stderr and elapsed >= 2
                          and json.loads(result.stdout) == expected)
            else:
                passed = (result.returncode == 4 and not result.stdout
                          and result.stderr == (BOARD_LINE if run == "board" else HOOK_LINE))
            check(label + " (exit %d, %.3f s)" % (result.returncode, elapsed), passed)
        # The last bounded run's child is finite but outlives its stopped parent.
        # Wait for it before removing the fixture and handing back.
        time.sleep(2)


def run_mutants(source, check):
    text = Path(source).read_text(encoding="utf-8")
    mutations = (
        ("person copy treated as hook", STARTUP,
         'WATCHDOG_MODE = ("board" if SAFE_READS else "hook") if __name__ == "__main__" and (SAFE_READS or HOOK_RUN) else None'),
        ("hook treated as unbounded person", STARTUP, 'WATCHDOG_MODE = "board" if SAFE_READS else None'),
        ("default remains 35 s", 'os.environ.get("SHOALMARK_BOARD_SECONDS") or 60',
         'os.environ.get("SHOALMARK_BOARD_SECONDS") or 35'),
        ("RV-3370 early theme discovery", 'add("--from", dest="theme", metavar="THEME", help=argparse.SUPPRESS)',
         'add("--from", dest="theme", metavar="THEME", help=argparse.SUPPRESS if (HERE / "brand" / "themes").is_dir() else argparse.SUPPRESS)'),
    )
    for name, before, after in mutations:
        assert text.count(before) == 1, "each mutant must change exactly one decision"
        with tempfile.TemporaryDirectory(prefix="fm058-mutant-") as directory:
            candidate = Path(directory) / "shoalmark.py"
            candidate.write_text(text.replace(before, after, 1), encoding="utf-8")

            def fail_fast(label, passed):
                if not passed:
                    raise AssertionError(label)

            try:
                run_controls(candidate, fail_fast)
            except AssertionError as error:
                check("FM-058 mutant rejected: " + name + " — " + str(error), True)
            else:
                check("FM-058 mutant rejected: " + name, False)

    # The copy-only mutant must fail every affected tree layout and board spelling,
    # rather than being stopped at the first unrelated hook failure.
    assert text.count(STARTUP) == 1
    with tempfile.TemporaryDirectory(prefix="fm058-copy-only-") as directory:
        candidate = Path(directory) / "shoalmark.py"
        candidate.write_text(text.replace(STARTUP,
            'WATCHDOG_MODE = watchdog_mode(sys.argv[1:]) if __name__ == "__main__" and HOOK_RUN else None', 1), encoding="utf-8")
        rejected = []

        def expect_failure(label, passed):
            if "short bound:" in label:
                rejected.append(not passed)
                check("RV-3371 copy-only mutant rejected: " + label, not passed)
            else:
                check(label, passed)

        run_controls(candidate, expect_failure, only=lambda kind, argv, run:
                     kind == "tree" and bool(argv) and (argv[0] == "--tsvn-hook" or argv[0].startswith("--ht")))
        check("RV-3371 copy-only mutant fails Tortoise layouts and every accepted board spelling", bool(rejected) and all(rejected))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mutants", action="store_true")
    args = parser.parse_args()
    failures = []

    def check(label, passed):
        print(("ok   " if passed else "FAIL ") + label, flush=True)
        if not passed:
            failures.append(label)

    run_controls(HERE / "shoalmark.py", check)
    if args.mutants:
        run_mutants(HERE / "shoalmark.py", check)
    return bool(failures)


if __name__ == "__main__":
    sys.exit(main())
