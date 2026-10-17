"""FM-058: the signed run-bound classes, exercised at the program entry point.

Run directly with --mutants to prove the three required regressions are caught.
Only a disposable tool's first configure call is replaced: the real startup,
argument classification and watchdog run before a child that outlasts the bound.
"""

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time


HERE = Path(__file__).resolve().parent
STARTUP = "if SAFE_READS or (HOOK_RUN and hook_watchdog_required(sys.argv[1:])):"
HOOK_LINE = ("shoalmark: the hook's run took longer than 1 s and was stopped — "
             "the commit is refused; SHOALMARK_BOARD_SECONDS gives it longer\n")
BOARD_LINE = "the board's run took longer than 1 s and was stopped\n"


def run_controls(source, check):
    """FM-058's contract: real children, unchanged COPY classification, defaults and fail-safe cases."""
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
            result, _ = launch(kind, argv)
            expected = {"seconds": 60, "copy": kind == "copy"}
            check("FM-058 default: " + kind + " " + run + " reads 60 s without waiting",
                  result.returncode == 0 and not result.stderr and json.loads(result.stdout) == expected)

        # Person cases come first so the over-bounding mutant has a direct witness.
        waits = (("copy", ["--answer", "FM-058", "accept"], "person"),
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
                 ("copy", [], "hook"))
        for kind, argv, run in waits:
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
        ("person copy treated as hook", STARTUP, "if SAFE_READS or HOOK_RUN:"),
        ("hook treated as unbounded person", STARTUP, "if SAFE_READS:"),
        ("default remains 35 s", 'os.environ.get("SHOALMARK_BOARD_SECONDS") or 60',
         'os.environ.get("SHOALMARK_BOARD_SECONDS") or 35'),
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
