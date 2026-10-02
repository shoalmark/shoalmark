"""One check of `test_shoalmark.py`, alone, against the tool as a revision had it — a security test's negative control (FM-006, *The release bar*).

The suite is one script; this runs its definitions and the ONE top-level block that holds the named check, in a temporary clone of this
repository checked out at `--tool` (the tool as it was — before a fix, its parent: `<fix>~1`), with this branch's `test_shoalmark.py` put
beside it. The block's own lines are printed as the suite prints them. Exit 0 where every check whose name holds the text passed; 1 where one
failed, or the block stopped — a test that cannot run against the old tool fails there too; 2 where no check by that name ran.

    python3 work-tracker/evidence/FM-006/run-one-check.py --tool <fix>~1 "<the check's name, or a part of it>"

A check whose name the suite builds from a table (`case {key}: {what}`) is reached with `--block "<text of its block's source>"` beside the name of the
one case. Without `--tool` it runs against HEAD. It writes nothing in this repository.
"""

import argparse
import ast
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile

REPO = pathlib.Path(subprocess.run(["git", "-C", str(pathlib.Path(__file__).resolve().parent), "rev-parse", "--show-toplevel"],
                                   capture_output=True, text=True, check=True).stdout.strip())
HEAVY = {"_block_run", "_chrome_run", "_chrome_probe", "_browser"}      # a definition that starts a browser is not run for one check


def calls(node):
    for n in ast.walk(node):
        if isinstance(n, ast.Call):
            f = n.func
            yield f.id if isinstance(f, ast.Name) else f.attr if isinstance(f, ast.Attribute) else ""


def patches(node):
    """Whether a statement replaces something of `subprocess` or `os` — a stub the suite puts back later, in a block this does not run."""
    targets = getattr(node, "targets", None) or [getattr(node, "target", None)]
    return any(isinstance(t, ast.Attribute) and getattr(t.value, "id", "") in ("subprocess", "os") for t in targets if t is not None)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("name", help="the check's name, or a part of it")
    ap.add_argument("--tool", default="HEAD", help="the revision whose tool the check runs against (default HEAD)")
    ap.add_argument("--block", help="text of the block's own source, where the check's name is built from a table and appears in no block")
    args = ap.parse_args()
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    with tempfile.TemporaryDirectory() as d:
        clone = pathlib.Path(d) / "clone"
        subprocess.run(["git", "clone", "--quiet", "--shared", str(REPO), str(clone)], check=True, capture_output=True, env=env)
        subprocess.run(["git", "-C", str(clone), "checkout", "--quiet", "--detach", args.tool], check=True, capture_output=True, env=env)
        tests = clone / "test_shoalmark.py"
        shutil.copyfile(REPO / "test_shoalmark.py", tests)
        src = tests.read_text(encoding="utf-8")
        tree = ast.parse(src)
        parts = [p.strip() for p in args.name.split("·") if p.strip()]       # a name the suite builds from parts is found by its parts:
        blocks = [n for n in tree.body if not isinstance(n, (ast.FunctionDef, ast.ClassDef)) and "check" in set(calls(n))]     # the block that holds most of them
        scored = [(sum(p in (ast.get_source_segment(src, n) or "") for p in parts), -i, n) for i, n in enumerate(blocks)]
        best = max(scored, default=(0, 0, None), key=lambda x: (x[0], x[1]))
        target = best[2] if best[0] else None
        if args.block:                                      # the block named by its own text
            target = next((n for n in blocks if args.block in (ast.get_source_segment(src, n) or "")), None)
        if target is None:
            print(f"run-one-check: no block of test_shoalmark.py holds {args.name!r}", file=sys.stderr)
            return 2
        g = {"__name__": "__run_one_check__", "__file__": str(tests)}
        os.chdir(clone)
        sys.argv = [str(tests)]
        for node in tree.body:
            code = compile(ast.Module(body=[node], type_ignores=[]), str(tests), "exec")
            if node is target:
                ran, told = [], g.get("check")
                g["check"] = lambda name, ok, told=told: (ran.append((name, bool(ok))), told(name, ok))[1]     # what ran, by name
                try:
                    exec(code, g)
                except BaseException as e:                  # the block stopped: against an old tool, a test that cannot run fails
                    print(f"run-one-check: the block stopped — {type(e).__name__}: {e}")
                    return 1
                break
            definition = isinstance(node, (ast.Import, ast.ImportFrom, ast.FunctionDef, ast.ClassDef))
            statement = isinstance(node, (ast.Assign, ast.AugAssign, ast.AnnAssign, ast.Expr)) and not patches(node)
            if definition or (statement and not ({"check", "skip"} | HEAVY) & set(calls(node))):
                try:
                    exec(code, g)
                except Exception:
                    pass                                    # a definition the old tool cannot give: the block will say so
    named = [ok for name, ok in ran if args.name in name]
    if not named:
        print(f"run-one-check: no check holding {args.name!r} ran against {args.tool} — it skipped here, or its block holds it under another name")
        return 2
    failed = named.count(False)
    print(f"run-one-check: {'FAILED' if failed else 'passed'} against {args.tool} — {len(named)} check(s) holding {args.name!r}" + (f", {failed} failed" if failed else ""))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
