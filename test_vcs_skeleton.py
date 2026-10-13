"""FM-044 common-skeleton controls, also run by test_core.py. Expectations come from the signed Builder brief.

These are boundary/metadata controls, not full shared-command no-Git or required-platform qualification.
"""

import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from unittest.mock import patch


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
