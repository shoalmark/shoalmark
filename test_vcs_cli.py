"""FM-044: bounded CLI capability and copied-command controls.

The pure API is not main-entry integration or full SVN qualification. Fixtures use real
Git and SVN for setup; a separate production process runs in an SVN WC without Git.
"""

import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("cli_fm", HERE / "shoalmark.py")
fm = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(fm)

# The signed scope retains this existing main order; the expectations are explicit,
# rather than read back from the implementation's declaration.
OPERATIONS = (
    ("vendor", ["--vendor", "tool"]), ("brand", ["--brand"]), ("init", ["--init"]),
    ("install_hook", ["--install-hook"]), ("session_trailer", ["--session-trailer", "message"]),
    ("whoami", ["--whoami"]), ("session_check", ["--session-check"]), ("commit_msg", ["--commit-msg", "message"]),
    ("session", ["--session", "new"]), ("sessions", ["--sessions"]), ("ratio", ["--ratio"]),
    ("ratio_window", ["--since", "2026-10-01"]), ("queue", ["--queue"]), ("schema", ["--schema"]),
    ("new", ["--new", "FM", "title"]), ("invite", ["--invite", "FM-044"]), ("notify", ["--notify"]),
    ("owner", ["--owner"]), ("answered", ["--answered"]), ("answer", ["--answer", "FM-044", "accept"]),
    ("done", ["--done", "FM-044", "where"]), ("due", ["--due", "FM-044", "2026-10-14T12:00Z"]),
    ("revoke", ["--revoke", "FM-044", "why"]), ("clear_ask", ["--clear-ask", "FM-044", "build"]),
    ("standup", ["--standup"]), ("next", ["--next"]), ("triage", ["--triage"]),
    ("related", ["--related", "FM-044"]),
)
GIT_ONLY = {"session_trailer": 4, "whoami": 4, "session_check": 4, "commit_msg": 4, "sessions": 4,
            "ratio": 2, "queue": 3, "answer": 4, "done": 4, "due": 4, "revoke": 4}
TOKENS = ("", "FM-044", "two words", "O'Brien", 'say "yes"', "C:\\Program Files\\O'Brien\\result.txt",
          '$env:USERPROFILE; $(Write-Output "x")', "`a · Grüße", "a\nb\tc", "*?[x]", "--leading", "$(touch nope)")


class CliControls(unittest.TestCase):
    def tearDown(self):
        fm.configure(HERE)

    def test_selected_handlers_and_default_modes(self):
        for name, argv in OPERATIONS:
            with self.subTest(operation=name):
                self.assertEqual(fm.cli_operation(fm.parse_args(argv)), name)
        self.assertEqual(fm.cli_operation(fm.parse_args([])), "write")
        self.assertEqual(fm.cli_operation(fm.parse_args(["--check"])), "check")

    def test_earlier_selected_operation_retains_precedence(self):
        for position, (name, argv) in enumerate(OPERATIONS):
            for later_name, later_argv in OPERATIONS[position + 1:]:
                with self.subTest(selected=name, ignored=later_name):
                    args = fm.parse_args(argv + later_argv)
                    self.assertEqual(fm.cli_operation(args), name)
                    diagnostic, code = fm.cli_preflight(args, "svn")
                    expected = GIT_ONLY.get(name, 2 if name == "ratio_window" else 0)
                    self.assertEqual(code, expected)
                    self.assertEqual(diagnostic is None, expected == 0)

    def test_empty_and_nonempty_optional_values_remain_selected(self):
        for argv, expected in ((["--brand", "", "--queue"], "brand"),
                               (["--standup", "", "--next"], "standup"),
                               (["--standup", "agenda.ics", "--triage"], "standup")):
            self.assertEqual(fm.cli_operation(fm.parse_args(argv)), expected)
        self.assertEqual(fm.cli_operation(fm.parse_args(["--vendor", "", "--queue"])), "queue")

    def test_ratio_window_barrier_remains_after_earlier_handlers(self):
        for backend in ("git", "svn"):
            self.assertEqual(fm.cli_preflight(fm.parse_args(["--until", "2026-10-14", "--queue"]), backend),
                             ("--since and --until go with --ratio", 2))
            self.assertEqual(fm.cli_preflight(fm.parse_args(["--init", "--until", "2026-10-14", "--queue"]), backend), (None, 0))

    def test_git_admission_continues_existing_handler_proof(self):
        for name, argv in OPERATIONS:
            if name != "ratio_window":
                self.assertEqual(fm.cli_preflight(fm.parse_args(argv), "git"), (None, 0))

    def test_each_selected_git_only_refusal_is_one_line_with_retained_code(self):
        for name, argv in OPERATIONS:
            if name in GIT_ONLY:
                diagnostic, code = fm.cli_preflight(fm.parse_args(argv), "svn")
                self.assertEqual(code, GIT_ONLY[name])
                self.assertEqual(len(diagnostic.splitlines()), 1)
                self.assertTrue(diagnostic.startswith("--" + name.replace("_", "-") + ":"))

    def test_pure_api_does_not_discover_read_start_print_or_write(self):
        arguments = [fm.parse_args(argv) for _, argv in OPERATIONS]
        out, err = io.StringIO(), io.StringIO()
        with patch.object(fm, "vcs", side_effect=AssertionError("backend discovery")), \
             patch.object(fm.subprocess, "run", side_effect=AssertionError("process")), \
             patch.object(Path, "read_text", side_effect=AssertionError("read")), \
             patch.object(Path, "write_text", side_effect=AssertionError("write")), \
             contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            for args in arguments:
                fm.cli_operation(args)
                fm.cli_preflight(args, "svn")
        self.assertEqual((out.getvalue(), err.getvalue()), ("", ""))

    def test_shared_session_removed_words_and_usage_remain(self):
        with patch.object(fm, "vcs", return_value="svn"), patch.object(fm, "session_rows", side_effect=AssertionError("Git history")):
            for words, expected in ((["new"], 0), (["open"], 2), (["close"], 2), (["nonsense"], 4), (["new", "extra"], 4)):
                out, err = io.StringIO(), io.StringIO()
                with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                    self.assertEqual(fm.session_cmd(words), expected)
                if expected == 0:
                    self.assertRegex(out.getvalue(), r"^[0-9a-f]{8}\n$")

    def test_posix_spelling_matches_shlex_exactly(self):
        with patch.object(fm.sys, "platform", "darwin"):
            for token in TOKENS:
                self.assertEqual(fm.printed_arg(token), shlex.quote(token))

    def test_powershell_literal_spelling_and_literal_recovery(self):
        with patch.object(fm.sys, "platform", "win32"):
            for token in TOKENS:
                spelling = fm.printed_arg(token)
                self.assertEqual(spelling, "'" + token.replace("'", "''") + "'")
                self.assertEqual(spelling[1:-1].replace("''", "'"), token)

    @unittest.skipUnless(shutil.which("sh"), "POSIX shell unavailable")
    def test_real_posix_shell_preserves_single_argument_bytes(self):
        with tempfile.TemporaryDirectory() as directory:
            capture = Path(directory) / "capture argv.py"
            capture.write_text("import json,sys; print(json.dumps(sys.argv[1:],ensure_ascii=False))\n", encoding="utf-8")
            with patch.object(fm.sys, "platform", "darwin"):
                for token in TOKENS:
                    command = " ".join((shlex.quote(sys.executable), shlex.quote(str(capture)), fm.printed_arg(token)))
                    result = subprocess.run([shutil.which("sh"), "-c", command], capture_output=True, text=True, encoding="utf-8", check=True)
                    self.assertEqual(json.loads(result.stdout), [token])
            self.assertFalse((Path(directory) / "nope").exists())

    def test_retry_commands_keep_configured_prefix_and_normalized_arguments(self):
        prefix = "python3 tools/shoalmark.py"
        text = 'O\'Brien $HOME; $(echo yes) "same"'
        tracker = {"id": "FM-044", "file": "FM-044-test.md", "title": "test", "status": "In Progress",
                   "ask": "a decision", "ask_kind": "ruling", "next": "owner", "due": "2026-10-14T12:00Z"}
        captures = []
        with patch.object(fm, "CMD", prefix), patch.object(fm, "vcs", return_value="git"), \
             patch.object(fm, "owner_change", side_effect=lambda _id, _tracker, how: captures.append(how) or 0), \
             patch.object(fm, "result_facts", return_value=""), \
             patch.object(fm.subprocess, "run", return_value=subprocess.CompletedProcess([], 128, "", "")):
            for platform in ("darwin", "win32"):
                with patch.object(fm.sys, "platform", platform):
                    fm.answer_cmd(["fm-044", "accept", text], [tracker])
                    self.assertTrue(captures[-1]["again"].startswith(prefix + " --answer "))
                    self.assertEqual(captures[-1]["again"], f"{prefix} --answer {fm.printed_arg('FM-044')} accept {fm.printed_arg(text)}")
                    fm.done_cmd(["fm-044", text], [tracker])
                    self.assertEqual(captures[-1]["again"], f"{prefix} --done {fm.printed_arg('FM-044')} {fm.printed_arg(text.replace(chr(34), chr(39)))}")
                    fm.due_cmd(["fm-044", "2026-10-14T12:00Z"], [tracker])
                    self.assertEqual(captures[-1]["again"], f"{prefix} --due {fm.printed_arg('FM-044')} {fm.printed_arg('2026-10-14T12:00Z')}")
                    fm.revoke_cmd(["fm-044", text], [{**tracker, "done": "2026-10-13T12:00Z · result"}])
                    self.assertEqual(captures[-1]["again"], f"{prefix} --revoke {fm.printed_arg('FM-044')} {fm.printed_arg(text.replace(chr(34), chr(39)))}")

    @unittest.skipUnless(shutil.which("svn") and shutil.which("svnadmin"), "SVN fixture tools unavailable")
    def test_real_svn_wc_policy_and_session_new_without_git_or_any_process(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            repo, wc, empty_path = base / "repository", base / "working copy", base / "empty PATH"
            empty_path.mkdir()
            subprocess.run([shutil.which("svnadmin"), "create", str(repo)], check=True, capture_output=True)
            subprocess.run([shutil.which("svn"), "checkout", repo.as_uri(), str(wc)], check=True, capture_output=True)
            script = base / "production_control.py"
            script.write_text("""import contextlib,importlib.util,io,json,sys
attempts=[]
def audit(event,args):
    if event=='subprocess.Popen':
        attempts.append(str(args[0])); raise AssertionError('unexpected production process')
sys.addaudithook(audit)
spec=importlib.util.spec_from_file_location('production',sys.argv[1])
fm=importlib.util.module_from_spec(spec); spec.loader.exec_module(fm)
assert fm.vcs()=='svn'
results=[]
for argv in json.loads(sys.argv[2]):
    results.append(fm.cli_preflight(fm.parse_args(argv),fm.vcs()))
out=io.StringIO()
with contextlib.redirect_stdout(out):
    code=fm.session_cmd(['new'])
print(json.dumps({'backend':fm.vcs(),'results':results,'session':out.getvalue(),'code':code,'attempts':attempts}))
""", encoding="utf-8")
            before = {p.relative_to(wc).as_posix(): p.read_bytes() for p in wc.rglob("*") if p.is_file()}
            cases = [(name, argv) for name, argv in OPERATIONS if name in GIT_ONLY]
            env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
            env.update(PATH=str(empty_path), PYTHONDONTWRITEBYTECODE="1")
            result = subprocess.run([sys.executable, "-B", str(script), str(HERE / "shoalmark.py"), json.dumps([argv for _, argv in cases])],
                                    cwd=wc, env=env, capture_output=True, text=True, encoding="utf-8", check=True)
            observed = json.loads(result.stdout)
            self.assertEqual(observed["backend"], "svn")
            self.assertEqual(observed["attempts"], [])
            self.assertEqual([r[1] for r in observed["results"]], [GIT_ONLY[name] for name, _ in cases])
            self.assertEqual(observed["code"], 0)
            self.assertRegex(observed["session"], r"^[0-9a-f]{8}\n$")
            after = {p.relative_to(wc).as_posix(): p.read_bytes() for p in wc.rglob("*") if p.is_file()}
            self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main(verbosity=2)
