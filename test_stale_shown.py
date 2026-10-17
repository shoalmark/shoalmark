"""FM-032, R22: a STALE line shows what differs. Where `--check` finds a generated file stale, it prints the lines that differ
between the file as it stands and what the tool would write: a unified diff with no context, at most 40 lines and then how
many more. A carriage return, a tab, a byte-order mark, a space at a line's end and a missing final newline each show as a
mark, so a drift no one can see on screen, a Windows one among them, reads as itself. The exit code (3) and the STALE line's
`Run:` stay. Also run by test_core.py.

Run alone: `python3 test_stale_shown.py`. It tests the shoalmark.py beside this file, as a program, in a throwaway repository.
The derived file's case needs a deriver (`<tracker folder>/derive`), which the tool runs as a program.
"""

import os
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
TRACKERS = "docs/work-tracker"
INDEX = f"{TRACKERS}/INDEX.md"
BOUND = 40                                  # R22's bound: lines of the difference printed, before "… and <n> more lines"
STALE = f"{INDEX} is STALE — a tracker changed without regenerating. Run: python3 shoalmark.py"
_ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
_ENV.update(GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t", GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@t",
            SHOALMARK_CMD="python3 shoalmark.py", PYTHONIOENCODING="utf-8")
DERIVER = ("#!/usr/bin/env python3\nimport json, sys\njson.load(sys.stdin)\n"
           "json.dump({'_files': {'docs/RELEASES.md': '# Releases\\n\\n1.2.0\\n'}}, sys.stdout)\n")


def _tracker(tid):
    return (f'---\nid: {tid}\nstatus: Proposed\nhook: "the hook of {tid}"\n---\n\n# {tid} — x\n\n'
            "## What is true now\n\n**One thing is left.**\n\n## Done when\n\nit is.\n").encode("utf-8")


def _row(text, tid):
    return next(line for line in text.split("\n") if line.startswith(f"| [{tid}]("))


def _cases(base):
    """(name, the bytes INDEX.md is given, the lines the difference must hold — each a whole printed line, in this order)."""
    two, one = _row(base, "FEAT-002"), _row(base, "FEAT-001")
    edited = two.replace("the hook of FEAT-002", "the hook of FEAT-002, edited by hand")
    lines = base.split("\n")
    at = lines.index(two)
    return [
        ("a changed row", base.replace(two, edited).encode("utf-8"),
         [f"  -{edited}", f"  +{two}"]),
        ("an added and a removed line", base.replace(two + "\n", "").replace(one, one + "\n| [FEAT-099](FEAT-099-x.md) | hand-added |").encode("utf-8"),
         [f"  +{two}", "  -| [FEAT-099](FEAT-099-x.md) | hand-added |"]),
        ("CRLF — a Windows checkout, one row changed: that row alone shows, its carriage return marked",
         base.replace(two, edited).replace("\n", "\r\n").encode("utf-8"),
         [f"  @@ -{at + 1} +{at + 1} @@", f"  -{edited}␍", f"  +{two}"]),
        ("CRLF — a carriage return inside a row", base.replace(two, two.replace(" | Proposed", "\r | Proposed")).encode("utf-8"),
         [f"  -{two.replace(' | Proposed', '␍ | Proposed')}", f"  +{two}"]),
        ("a trailing space", base.replace(two, two + "  ").encode("utf-8"),
         [f"  -{two}␠␠", f"  +{two}"]),
        ("a tab", base.replace(two, two.replace("| [FEAT-002]", "|\t[FEAT-002]")).encode("utf-8"),
         [f"  -{two.replace('| [FEAT-002]', '|␉[FEAT-002]')}", f"  +{two}"]),
        ("a byte-order mark", b"\xef\xbb\xbf" + base.encode("utf-8"),
         ["  @@ -1 +1 @@", f"  -⟨BOM⟩{lines[0]}", f"  +{lines[0]}"]),
        ("no final newline", base.rstrip("\n").encode("utf-8"),
         [f"  -{one}", "  \\ No newline at end of file", f"  +{one}"]),
    ]


def run_stale_shown_controls(fm, check):
    """FM-032, R22: STALE shows the differing lines, bounded, with what is invisible marked."""
    print("\nFM-032 · R22: a STALE line shows what differs — bounded, the invisible marked")
    tool = Path(fm.__file__).resolve()
    with tempfile.TemporaryDirectory() as tmp:
        root, hooks = Path(tmp).resolve() / "repo", Path(tmp).resolve() / "no-hooks"
        (root / TRACKERS).mkdir(parents=True)
        hooks.mkdir()

        def git(*a):
            subprocess.run(["git", "-C", str(root), *a], check=True, capture_output=True, env=_ENV)

        def run(*argv):
            r = subprocess.run([sys.executable, str(tool), "--root", str(root), *argv], capture_output=True, env=_ENV, cwd=str(root))
            return r.returncode, r.stdout.decode("utf-8", errors="replace"), r.stderr.decode("utf-8", errors="replace")   # as bytes: a raw CR stays one

        git("init", "-q")
        for key, value in (("core.hooksPath", str(hooks)), ("core.autocrlf", "false"), ("commit.gpgsign", "false")):
            git("config", key, value)
        (root / "shoalmark.toml").write_bytes(b'name = "stale"\n[kinds]\nFEAT = "Features"\n[considered_from]\nFEAT = 10\n')
        (root / ".gitignore").write_bytes(f"{TRACKERS}/index.html\n{TRACKERS}/view/\n".encode("utf-8"))
        (root / TRACKERS / "TRIAGE.md").write_bytes("# Triage\n\n## The intent\n\n- **for** — stale\n\n## The current path\n\n"
                                                    "1. [FEAT-002](FEAT-002-x.md) to its end.\n\n## Passes\n\nNewest first.\n\n*None yet.*\n".encode("utf-8"))
        for tid in ("FEAT-001", "FEAT-002", "FEAT-003"):
            (root / TRACKERS / f"{tid}-x.md").write_bytes(_tracker(tid))
        written = run()
        git("add", "-A")
        git("commit", "-qm", "the base")
        index = root / INDEX
        base_bytes = index.read_bytes()
        base = base_bytes.decode("utf-8")
        green = run("--check")
        check(f"FM-032 · R22 · the fixture: written, and `--check` green (saw {written[0]}, {green[0]}: {(written[2] + green[2]).strip()[:300]!r})",
              written[0] == green[0] == fm.EXIT_OK and "STALE" not in green[2] and base.endswith("|\n"))

        # The control: a Windows checkout's CRLF line ends alone are not drift — the check reads them as LF, as it did before R22.
        index.write_bytes(base_bytes.replace(b"\n", b"\r\n"))
        code, _, err = run("--check")
        check(f"FM-032 · R22 · a CRLF checkout with nothing else changed is not STALE: exit 0, no difference printed (saw {code}: {err.strip()[:300]!r})",
              code == fm.EXIT_OK and "STALE" not in err and "as it stands" not in err)

        for name, given, want in _cases(base):
            index.write_bytes(given)
            code, _, err = run("--check")
            said = err.split("\n")
            start = said.index(STALE) if STALE in said else -1
            shown = said[start + 1:] if start >= 0 else []
            ordered, at = True, 0
            for line in want:
                if line not in shown[at:]:
                    ordered = False
                    break
                at = shown.index(line, at) + 1
            check(f"FM-032 · R22 · {name}: exit {fm.EXIT_DRIFT}, the STALE line with its Run:, then the difference with "
                  f"{want} in it (saw {code}: {err.strip()[:900]!r})",
                  code == fm.EXIT_DRIFT and start >= 0
                  and shown[:2] == [f"  --- {INDEX}, as it stands", f"  +++ {INDEX}, as the tool would write it"] and ordered
                  and "\r" not in err and "\t" not in err and "\ufeff" not in err)
            if name.startswith("CRLF — a Windows"):
                diff = [line for line in shown[2:] if line.startswith(("  @@", "  -", "  +", "  \\"))]
                check(f"FM-032 · R22 · {name}: the difference is that row and nothing else — the CRLF line ends do not flood it (saw {diff})",
                      len(diff) == 3)
            if any(m in "".join(want) for m in ("␍", "␉", "␠", "⟨BOM⟩")):
                check(f"FM-032 · R22 · {name}: the marks it used are named, once", sum(line.startswith("  marks: ") for line in shown) == 1)
        index.write_bytes(base_bytes)

        # The bound: a 500-line drift prints 40 lines of its difference and says how many more.
        index.write_bytes((base + "".join(f"| hand-added {i} |\n" for i in range(500))).encode("utf-8"))
        code, _, err = run("--check")
        said = err.split("\n")
        start = said.index(STALE) if STALE in said else len(said)
        body = [line for line in said[start + 3:] if line.startswith(("  @@", "  -", "  +", "  \\"))]
        more = [line for line in said[start + 3:] if line.startswith("  … and ")]
        check(f"FM-032 · R22 · a 500-line drift keeps the bound: exit {fm.EXIT_DRIFT}, {BOUND} lines of its difference, then "
              f"'… and 461 more lines' (saw {code}, {len(body)} lines, {more})",
              code == fm.EXIT_DRIFT and len(body) == BOUND and more == ["  … and 461 more lines"] and len(err) < 6000)
        index.write_bytes(base_bytes)

        # A derived file the tool writes beside INDEX.md: its STALE line shows its difference the same way.
        deriver = root / TRACKERS / "derive"
        deriver.write_bytes(DERIVER.encode("utf-8"))
        deriver.chmod(0o755)
        run()
        releases = root / "docs" / "RELEASES.md"
        releases.write_bytes(b"# Releases\n\n1.2.0 \n")
        code, _, err = run("--check")
        check(f"FM-032 · R22 · a derived file: exit {fm.EXIT_DRIFT}, its STALE line and its difference (saw {code}: {err.strip()[:600]!r})",
              code == fm.EXIT_DRIFT and "docs/RELEASES.md is STALE — regenerate. Run: python3 shoalmark.py\n"
              "  --- docs/RELEASES.md, as it stands\n  +++ docs/RELEASES.md, as the tool would write it\n"
              "  @@ -3 +3 @@\n  -1.2.0␠\n  +1.2.0\n" in err)
        deriver.unlink()


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

    run_stale_shown_controls(_fm, _check)
    print(f"\n{'FAILED: ' + str(len(_fails)) if _fails else 'all green'}")
    sys.exit(1 if _fails else 0)
